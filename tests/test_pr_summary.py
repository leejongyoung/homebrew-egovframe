"""Tests for scripts/pr_summary.py: the version PR must describe the final tree only."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "tests"))
import pr_summary  # noqa: E402
import sync_readme  # noqa: E402
import update_casks as uc  # noqa: E402
from test_update_casks import FakeMaven, page  # noqa: E402


class PrSummaryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        shutil.copytree(REPO / "tests/fixtures/Casks", self.tmp / "Casks")
        shutil.copytree(REPO / "tests/fixtures/docs", self.tmp / "docs")
        sync_readme.sync(self.tmp, groups=("languages",))
        self.maven = FakeMaven()
        self.addCleanup(self.maven.close)
        original_delay = uc.RETRY_DELAY
        uc.RETRY_DELAY = 0
        self.addCleanup(setattr, uc, "RETRY_DELAY", original_delay)

    def run_update(self, *versions):
        for v in versions:
            self.maven.publish(v)
        return uc.run(self.tmp, page(*versions), self.maven.base, False, badge_check=False)

    def test_same_series_patches_list_only_the_final_cask(self):
        result = self.run_update("5.0.3", "5.0.4")
        # 계약: added 는 중간 패치를 포함하고, removed 에도 5.0.3 이 들어간다.
        self.assertEqual(result["added"], ["5.0.3", "5.0.4"])
        self.assertIn("5.0.3", result["removed"])
        s = pr_summary.summarize(self.tmp, result["added"], result["removed"])
        self.assertEqual(s["versions"], ["5.0.4"])
        self.assertEqual(s["title"], "feat(casks): add egovframedev@5.0.4")
        self.assertIn("### 5.0.4", s["body"])
        self.assertNotIn("### 5.0.3", s["body"])
        self.assertIn("superseded", s["body"])
        self.assertIn("Removed older patch casks of the same series: 5.0.2", s["body"])
        # 본문에 나오는 해시는 실제 파일에서 읽은 것이다.
        import re
        shas = re.findall(r"[0-9a-f]{64}", (self.tmp / "Casks/egovframedev@5.0.4.rb").read_text(encoding="utf-8"))
        self.assertEqual(len(shas), 2)
        for sha in shas:
            self.assertIn(sha, s["body"])
        self.assertFalse((self.tmp / "Casks/egovframedev@5.0.3.rb").exists())

    def test_two_new_minor_series_are_both_included(self):
        result = self.run_update("5.0.3", "5.1.0")
        s = pr_summary.summarize(self.tmp, result["added"], result["removed"])
        self.assertEqual(s["versions"], ["5.0.3", "5.1.0"])
        self.assertEqual(s["title"], "feat(casks): add egovframedev@5.0.3, egovframedev@5.1.0")
        self.assertIn("### 5.0.3", s["body"])
        self.assertIn("### 5.1.0", s["body"])
        self.assertNotIn("superseded", s["body"])

    def test_cli_writes_body_and_prints_outputs(self):
        result = self.run_update("5.0.3", "5.0.4")
        body = self.tmp / "body.md"
        import io
        import contextlib
        out = io.StringIO()
        argv = ["pr_summary.py", "--root", str(self.tmp), "--added", ",".join(result["added"]),
                "--removed", ",".join(result["removed"]), "--body-file", str(body)]
        old = sys.argv
        sys.argv = argv
        try:
            with contextlib.redirect_stdout(out):
                self.assertEqual(pr_summary.main(), 0)
        finally:
            sys.argv = old
        self.assertIn("title=feat(casks): add egovframedev@5.0.4", out.getvalue())
        self.assertIn("branch=auto/egovframedev-5.0.3-5.0.4", out.getvalue())
        self.assertTrue(body.read_text(encoding="utf-8").startswith("Detected on"))


if __name__ == "__main__":
    unittest.main()
