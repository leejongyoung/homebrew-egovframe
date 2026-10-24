#!/usr/bin/env bash
# Validate every cask. Only the documented legacy style exemption is skipped;
# all casks still go through readall and audit. Run from the checkout root.
set -euo pipefail

tap=${1:-leejongyoung/egovframe}
all=()
style=()
for file in Casks/*.rb; do
  name=$(basename "$file" .rb)
  all+=("$tap/$name")
  if grep -qxF "$name" .github/style-exempt.txt; then
    echo "style-exempt: $name (see .github/style-exempt.txt)"
  else
    style+=("$tap/$name")
  fi
done

brew readall --aliases --os=all --arch=all "$tap"
brew style "${style[@]}"
brew audit --cask --except=installed "${all[@]}"
