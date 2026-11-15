#!/usr/bin/env python3
"""Build the version-PR title, branch and body from update_casks.py's added/removed lists.

A run can add several patches of one series (e.g. 5.0.3 and 5.0.4): the intermediate
cask is created and then removed again, so only the casks that still exist in the final
tree are listed with hashes. Intermediate versions are reported separately.

Usage: pr_summary.py --root . --added 5.0.3,5.0.4 --removed 5.0.2,5.0.3 --body-file body.md
Prints `title=...`, `branch=...` and `versions=...` lines (append them to $GITHUB_OUTPUT).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from update_casks import cask_versions, vtuple


def split_csv(value: str) -> list[str]:
    return [v for v in (value or "").split(",") if v]


def summarize(root: Path, added: list[str], removed: list[str]) -> dict:
    present = cask_versions(root / "Casks")
    final = sorted((v for v in added if v in present), key=vtuple)
    intermediate = sorted((v for v in added if v not in present), key=vtuple)
    # Removed casks that were not added in this run were replaced by a newer patch.
    replaced = sorted((v for v in removed if v not in added), key=vtuple)
    title = "feat(casks): add " + ", ".join(f"egovframedev@{v}" for v in final)
    branch = "auto/egovframedev-" + "-".join(added)
    lines = ["Detected on https://www.egovframe.go.kr/home/sub.do?menuNo=40 and downloaded from the official host.", ""]
    for v in final:
        text = (present[v]).read_text(encoding="utf-8")
        block = re.search(r"sha256[^\n]*(?:\n[^\n]*intel:[^\n]*)?", text)
        lines.append(f"### {v}")
        if block:
            lines.extend("    " + re.sub(r"^\s*(sha256\s+)?", "", l) for l in block.group(0).split("\n"))
        lines.append("")
    if intermediate:
        lines.append("Detected in the same run but superseded by a newer patch of the same series "
                     f"(not part of this PR): {', '.join(intermediate)}")
        lines.append("")
    if replaced:
        lines.append(f"Removed older patch casks of the same series: {', '.join(replaced)}")
        lines.append("")
    lines += ["Merging this publishes the GitHub Release for the new version (release.yml).", "",
              "Check before merging: `gh workflow run update-casks.yml -f verify=<version>` "
              "re-downloads the DMGs and compares the hashes."]
    return {"title": title, "branch": branch, "versions": final, "body": "\n".join(lines) + "\n"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--added", default="")
    ap.add_argument("--removed", default="")
    ap.add_argument("--body-file", type=Path, required=True)
    args = ap.parse_args()
    added = split_csv(args.added)
    if not added:
        print("no added versions", file=sys.stderr)
        return 1
    result = summarize(args.root, added, split_csv(args.removed))
    if not result["versions"]:
        print("none of the added versions exists in the final tree", file=sys.stderr)
        return 1
    args.body_file.write_text(result["body"], encoding="utf-8")
    print(f"title={result['title']}")
    print(f"branch={result['branch']}")
    print(f"versions={','.join(result['versions'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
