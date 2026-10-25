"""Tests for scripts/open_upstream_pr.sh against local bare repos (no network, no gh)."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "open_upstream_pr.sh"

README_UPSTREAM = """# homebrew-egovframe

## Introduction
Hello.

```bash
brew install egovframedev@1.0.0
```

### Application Installation Path
* app
"""

README_WORK = """# homebrew-egovframe

<!-- work-only:start -->
<!-- latest-badge:start -->
[![badge](https://example.invalid/badge.svg)](https://example.invalid/)
<!-- latest-badge:end -->

> fork note
<!-- work-only:end -->

## Introduction
Hello.

```bash
brew install egovframedev@1.0.1
brew install egovframedev@1.0.0
```

### Application Installation Path
* app
<!-- work-only:start -->

## Maintenance
fork only
<!-- work-only:end -->
"""


def git(cwd, *args, check=True):
    return subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *args], cwd=cwd,
                          check=check, capture_output=True, text=True)


def write(root, rel, text):
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


class OpenUpstreamPrTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        up_bare, origin_bare = self.tmp / "up.git", self.tmp / "origin.git"
        for bare in (up_bare, origin_bare):
            git(self.tmp, "init", "-q", "--bare", "-b", "main", str(bare))

        seed = self.tmp / "seed"
        git(self.tmp, "clone", "-q", str(up_bare), str(seed))
        git(seed, "checkout", "-q", "-b", "main")
        write(seed, "README.md", README_UPSTREAM)
        write(seed, "Casks/a.rb", "a v1\n")
        write(seed, "Casks/c.rb", "c\n")
        write(seed, "Casks/d.rb", "d\n")
        git(seed, "add", "-A")
        git(seed, "commit", "-qm", "upstream base")
        git(seed, "push", "-q", "origin", "main")
        git(seed, "push", "-q", str(origin_bare), "main")

        git(seed, "checkout", "-q", "-b", "work")
        write(seed, "README.md", README_WORK)
        write(seed, "Casks/a.rb", "a v2\n")        # modified
        write(seed, "Casks/b.rb", "b new\n")       # added
        (seed / "Casks/c.rb").unlink()             # deleted
        write(seed, ".github/workflows/ci.yml", "ci\n# work-only:start\n  sync-upstream-submit:\n# work-only:end\n")
        write(seed, ".github/SECURITY.md", "https://github.com/leejongyoung/homebrew-egovframe/security (`work`)\n")
        write(seed, "scripts/update_casks.py", "tool\n")
        write(seed, "tests/test_update_casks.py", "test\n")
        write(seed, ".github/MAINTENANCE.md", "fork maintenance\n")
        write(seed, ".github/UPSTREAM_PR.md", "pr body\n")
        write(seed, ".github/workflows/sync-upstream.yml", "sync\n")
        write(seed, "scripts/open_upstream_pr.sh", "submit\n")
        write(seed, "tests/test_open_upstream_pr.py", "submit test\n")
        git(seed, "add", "-A")
        git(seed, "commit", "-qm", "work changes")
        git(seed, "push", "-q", str(origin_bare), "work")

        self.repo = self.tmp / "repo"
        git(self.tmp, "clone", "-q", str(origin_bare), str(self.repo))
        git(self.repo, "checkout", "-q", "work")
        git(self.repo, "remote", "add", "upstream", str(up_bare))

    def run_script(self, *args, extra_env=None):
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        if extra_env:
            env.update(extra_env)
        return subprocess.run(["bash", str(SCRIPT), *args], cwd=self.repo, capture_output=True, text=True, env=env)

    def submission_branches(self):
        out = git(self.repo, "branch", "--list", "upstream-submit-*").stdout
        return [l.strip().lstrip("* ") for l in out.splitlines()]

    def files_on(self, ref):
        return sorted(git(self.repo, "ls-tree", "-r", "--name-only", ref).stdout.split())

    def test_builds_one_clean_commit_on_top_of_upstream(self):
        result = self.run_script("--no-push", "-m", "feat: submit")
        self.assertEqual(result.returncode, 0, result.stderr)
        (branch,) = self.submission_branches()

        # one commit on top of upstream/main, message as given
        self.assertEqual(git(self.repo, "rev-list", "--count", f"upstream/main..{branch}").stdout.strip(), "1")
        self.assertEqual(git(self.repo, "log", "-1", "--format=%s", branch).stdout.strip(), "feat: submit")

        # casks, shared docs and automation follow work; fork-only files are absent
        self.assertEqual(self.files_on(branch), [
            ".github/SECURITY.md",
            ".github/workflows/ci.yml",
            "Casks/a.rb",
            "Casks/b.rb",
            "Casks/d.rb",
            "README.md",
            "scripts/update_casks.py",
            "tests/test_update_casks.py",
        ])
        self.assertEqual(git(self.repo, "show", f"{branch}:Casks/a.rb").stdout, "a v2\n")
        self.assertEqual(git(self.repo, "show", f"{branch}:.github/SECURITY.md").stdout,
                         "https://github.com/eGovFramework/homebrew-egovframe/security (`main`)\n")
        self.assertEqual(git(self.repo, "show", f"{branch}:.github/workflows/ci.yml").stdout, "ci\n")

        # README: install list kept, fork-only blocks gone, no stray blank lines
        readme = git(self.repo, "show", f"{branch}:README.md").stdout
        expected = README_UPSTREAM.replace("brew install egovframedev@1.0.0\n",
                                           "brew install egovframedev@1.0.1\nbrew install egovframedev@1.0.0\n")
        self.assertEqual(readme, expected)

        # work and the working tree are left as they were
        self.assertEqual(git(self.repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip(), "work")
        self.assertEqual(git(self.repo, "status", "--porcelain").stdout, "")
        self.assertEqual(git(self.repo, "rev-parse", "work").stdout, git(self.repo, "rev-parse", "origin/work").stdout)

    def test_snapshot_preparation_preserves_existing_upstream_submit(self):
        git(self.repo, "branch", "upstream-submit", "origin/main")
        before = git(self.repo, "rev-parse", "upstream-submit").stdout
        result = self.run_script("--no-push", "-m", "feat: isolated snapshot")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git(self.repo, "rev-parse", "upstream-submit").stdout, before)
        (snapshot,) = self.submission_branches()
        self.assertEqual(git(self.repo, "show", f"{snapshot}:Casks/a.rb").stdout, "a v2\n")

    def test_public_readme_badge_and_content_survive_fork_stripping(self):
        badge = "[![eGovFrame 5.0.2](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/5.0.2/flat.svg)](https://www.egovframe.go.kr/)"
        public_block = f"<!-- latest-badge:start -->\n{badge}\n<!-- latest-badge:end -->\n\n"
        text = README_WORK.replace("# homebrew-egovframe\n\n",
                                   "# homebrew-egovframe\n\n" + public_block, 1)
        text = text.replace("Hello.", "Updated public installation instructions.")
        write(self.repo, "README.md", text)
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-qm", "docs: update public installation guide")
        git(self.repo, "push", "-q", "origin", "work")

        result = self.run_script("--no-push", "-m", "docs: share installation guide")
        self.assertEqual(result.returncode, 0, result.stderr)
        (snapshot,) = self.submission_branches()
        submitted = git(self.repo, "show", f"{snapshot}:README.md").stdout
        self.assertIn(badge, submitted)
        self.assertIn("Updated public installation instructions.", submitted)
        self.assertIn("brew install egovframedev@1.0.1", submitted)
        self.assertNotIn("fork note", submitted)
        self.assertNotIn("## Maintenance", submitted)
        self.assertNotIn("work-only:", submitted)
        self.assertIn("<!-- latest-badge:start -->", submitted)

    def test_nested_documentation_keeps_navigation_and_drops_fork_blocks(self):
        paths = (
            "docs/README.en.md",
            "docs/README.ko.md",
            "code-signing-guideline.md",
            "docs/code-signing-guideline/code-signing-guideline.ko.md",
            ".github/CONTRIBUTING.md",
            ".github/SECURITY.md",
            "docs/contributing/CONTRIBUTING.ko.md",
            "docs/security/SECURITY.ko.md",
        )
        for path in paths:
            write(self.repo, path,
                  "# Guide\n\n[English](code-signing-guideline.en.md)\n"
                  "[Badge](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/flat.svg)\n"
                  "[CI](https://github.com/leejongyoung/homebrew-egovframe/actions)\n"
                  "<!-- work-only:start -->\nPrivate maintenance\n<!-- work-only:end -->\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "docs: reorganize translated guides")
        git(self.repo, "push", "-q", "origin", "work")

        result = self.run_script("--no-push", "-m", "docs: submit translated guides")
        self.assertEqual(result.returncode, 0, result.stderr)
        (snapshot,) = self.submission_branches()
        for path in paths:
            with self.subTest(path=path):
                text = git(self.repo, "show", f"{snapshot}:{path}").stdout
                self.assertIn("[English](code-signing-guideline.en.md)", text)
                self.assertIn("leejongyoung/egovframe-badge/", text)
                self.assertIn("https://github.com/eGovFramework/homebrew-egovframe/actions", text)
                self.assertNotIn("Private maintenance", text)
                self.assertNotIn("work-only:", text)

    def test_submission_preserves_original_workflow_badges_and_result_links(self):
        status_lines = (
            "[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)]"
            "(https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)\n"
            "[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)]"
            "(https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)\n"
        )
        write(self.repo, "README.md", "# Guide\n\n" + status_lines)
        write(self.repo, "docs/README.en.md", "# Guide\n\n" + status_lines)
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "docs: keep original workflow badges")
        git(self.repo, "push", "-q", "origin", "work")

        result = self.run_script("--no-push", "-m", "docs: submit workflow definitions")
        self.assertEqual(result.returncode, 0, result.stderr)
        (snapshot,) = self.submission_branches()
        for path in ("README.md", "docs/README.en.md"):
            text = git(self.repo, "show", f"{snapshot}:{path}").stdout
            self.assertIn(status_lines, text)
            self.assertNotIn("docs/badges/", text)
        self.assertIn(status_lines, git(self.repo, "show", "work:README.md").stdout)

    def test_only_restricts_what_is_sent(self):
        self.run_script("--no-push", "-m", "x", "--only", "Casks/b.rb")
        (branch,) = self.submission_branches()
        self.assertEqual(self.files_on(branch), sorted(self.files_on("upstream/main") + ["Casks/b.rb"]))
        self.assertEqual(git(self.repo, "show", f"{branch}:Casks/a.rb").stdout, "a v1\n")

    def test_dry_run_creates_nothing(self):
        result = self.run_script("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Casks/b.rb", result.stdout)
        self.assertIn(".github/SECURITY.md", result.stdout.split("would be sent")[1])
        self.assertNotIn("MAINTENANCE.md", result.stdout.split("would be sent")[1])
        self.assertEqual(self.submission_branches(), [])
        self.assertEqual(git(self.repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip(), "work")

    def test_only_fork_only_differences_means_nothing_to_submit(self):
        result = self.run_script("--dry-run", "--only", ".github/MAINTENANCE.md")
        self.assertEqual(result.returncode, 0)
        self.assertIn("nothing to submit", result.stdout)
        self.assertEqual(self.submission_branches(), [])

    def test_message_is_required_to_build(self):
        result = self.run_script("--no-push")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.submission_branches(), [])

    def test_refuses_a_dirty_working_tree(self):
        write(self.repo, "Casks/a.rb", "local edit\n")
        result = self.run_script("--no-push", "-m", "x")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.submission_branches(), [])
        self.assertEqual((self.repo / "Casks/a.rb").read_text(), "local edit\n")

    def test_update_branch_syncs_and_is_idempotent_unless_upstream_pr_is_open(self):
        # 1. Initial sync creates and pushes origin/upstream-submit with 1 clean commit
        res1 = self.run_script("--update-branch", "upstream-submit", "-m", "feat: sync upstream-submit",
                               extra_env={"UPSTREAM_OPEN_PR": ""})
        self.assertEqual(res1.returncode, 0, res1.stderr)
        self.assertEqual(self.submission_branches(), [])
        self.assertEqual(git(self.repo, "rev-list", "--count", "upstream/main..origin/upstream-submit").stdout.strip(), "1")
        self.assertIn(".github/SECURITY.md", self.files_on("origin/upstream-submit"))
        self.assertNotIn(".github/MAINTENANCE.md", self.files_on("origin/upstream-submit"))
        first_sha = git(self.repo, "rev-parse", "origin/upstream-submit").stdout.strip()
        # upstream-submit commit is 100% included as an ancestor of work
        self.assertEqual(git(self.repo, "merge-base", "--is-ancestor", "origin/upstream-submit", "origin/work").returncode, 0)

        # 2. Second run with no upstream-ready change (even after a fork-only edit on work) is a no-op
        write(self.repo, ".github/MAINTENANCE.md", "fork doc change\n")
        git(self.repo, "add", ".github/MAINTENANCE.md")
        git(self.repo, "commit", "-qm", "docs: fork-only update")
        git(self.repo, "push", "-q", "origin", "work")
        res2 = self.run_script("--update-branch", "upstream-submit", "-m", "feat: sync again",
                               extra_env={"UPSTREAM_OPEN_PR": ""})
        self.assertEqual(res2.returncode, 0, res2.stderr)
        self.assertIn("already up to date", res2.stdout)
        self.assertEqual(git(self.repo, "rev-parse", "origin/upstream-submit").stdout.strip(), first_sha)

        # 3. When an upstream PR is open on upstream-submit, an upstream-ready change on work does not overwrite it
        write(self.repo, "Casks/a.rb", "a v3\n")
        git(self.repo, "add", "Casks/a.rb")
        git(self.repo, "commit", "-qm", "feat: bump a")
        git(self.repo, "push", "-q", "origin", "work")
        res3 = self.run_script("--update-branch", "upstream-submit", "-m", "feat: should skip",
                               extra_env={"UPSTREAM_OPEN_PR": "6"})
        self.assertEqual(res3.returncode, 0, res3.stderr)
        self.assertIn("upstream PR #6 is already open", res3.stdout)
        self.assertEqual(git(self.repo, "rev-parse", "origin/upstream-submit").stdout.strip(), first_sha)


if __name__ == "__main__":
    unittest.main()
