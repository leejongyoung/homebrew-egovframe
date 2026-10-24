#!/usr/bin/env python3
"""Sync README.md from the configured default language file."""

import sys
import yaml
from pathlib import Path


def main():
    repo_root = Path(".")
    docs_dir = Path("docs")

    # Load config
    with open(docs_dir / "config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    default_lang = config.get("default_language", "en")
    languages = config.get("languages", {})

    if default_lang not in languages:
        print(f"Error: default_language '{default_lang}' not found in languages mapping")
        return 1

    source_file = Path(languages[default_lang])
    if not source_file.exists():
        print(f"Error: source file {source_file} not found")
        return 1

    # Read source content
    source_content = Path(languages[default_lang]).read_text(encoding="utf-8")

    # Read current README.md
    readme_path = Path("README.md")
    current_content = readme_path.read_text(encoding="utf-8") if Path("README.md").exists() else ""

    if Path(languages["en"]).read_text() != Path("README.md").read_text():
        Path("README.md").write_text(Path("docs/README.en.md").read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Updated README.md from {languages['en']}")
        print("changed=true")
    else:
        print("README.md already up to date")
        print("changed=false")

    return 0


if __name__ == "__main__":
    sys.exit(main())