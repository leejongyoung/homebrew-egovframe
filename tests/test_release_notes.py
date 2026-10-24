"""Tests for scripts/release_notes.py against the checked-in casks."""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import release_notes as rn  # noqa: E402
import update_casks as uc  # noqa: E402


class ReleaseNotesTest(unittest.TestCase):
    def test_notes_match_the_cask_hashes_and_urls(self):
        version = uc.latest_version(REPO / "Casks")
        cask = (REPO / "Casks" / f"egovframedev@{version}.rb").read_text()
        sha = uc.SHA_BLOCK.search(cask)
        notes = rn.render(REPO, version)
        self.assertIn(f"`{sha.group(3)}`", notes)
        self.assertIn(f"`{sha.group(6)}`", notes)
        self.assertIn(f"eGovFrameDev-{version}-macOS-AArch64.dmg", notes)
        self.assertIn(f"eGovFrameDev-{version}-macOS-x86_64.dmg", notes)
        major_minor = ".".join(version.split(".")[:2])
        self.assertIn(f"/egovframework_v{major_minor}/2_DevelopmentEnvironment/eGovFrame-Dev/{version}/", notes)
        self.assertIn(f"brew install egovframedev@{version}", notes)

    def test_latest_hint_only_for_the_latest_version(self):
        latest = uc.latest_version(REPO / "Casks")
        self.assertIn("egovframedev-latest", rn.render(REPO, latest))
        notes = rn.render(REPO, "4.3.1")  # older cask, different DMG naming (Mac instead of macOS)
        self.assertIn("eGovFrameDev-4.3.1-Mac-AArch64.dmg", notes)
        self.assertNotIn("egovframedev-latest", notes)

    def test_unknown_version_fails(self):
        with self.assertRaises(SystemExit):
            rn.render(REPO, "0.0.1")


if __name__ == "__main__":
    unittest.main()
