#!/usr/bin/env bash
# Open a pull request against upstream eGovFramework/homebrew-egovframe with only what belongs
# upstream: the changes of `work` over upstream's default branch, minus fork-only files.
#
# The submission branch is built on top of upstream's branch (not on `work`), so the PR carries one
# clean commit and none of this fork's CI/automation history. `work` itself is never touched.
#
# Fork-only, never sent upstream:
#   - .github/  scripts/  tests/                      (CI, automation, tests)
#   - README blocks between `<!-- work-only:start -->` and `<!-- work-only:end -->`
#     (fork CI badges, personal tap note and maintenance links)
#
# Usage: scripts/open_upstream_pr.sh -m "<commit and PR title>" [options] [-- <gh pr create options>]
#   -m, --message TEXT   commit message, also the PR title (required unless --dry-run)
#       --only PATH      send only this file or directory (repeatable), e.g. --only Casks/egovframedev@4.2.1.rb
#       --base BRANCH    upstream branch to build on and target (default: main)
#       --dry-run        show what would be sent; create nothing
#       --no-push        build the local submission branch, do not push or open a PR
# Examples:
#   scripts/open_upstream_pr.sh --dry-run
#   scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
#   scripts/open_upstream_pr.sh -m "feat(casks): add egovframedev@5.0.3" -- --body-file /tmp/body.md
set -euo pipefail

UPSTREAM_REPO="eGovFramework/homebrew-egovframe"
UPSTREAM_URL="https://github.com/$UPSTREAM_REPO.git"
SOURCE="work"
DENYLIST=(".github/" "scripts/" "tests/")
STRIP_FILES=("README.md" "README.ko.md")

message=""
base="main"
dry=0
push=1
only=()
while [ $# -gt 0 ]; do
  case $1 in
    -m|--message) message=${2:?--message needs text}; shift 2 ;;
    --only) only+=("${2:?--only needs a path}"); shift 2 ;;
    --base) base=${2:?--base needs a branch}; shift 2 ;;
    --dry-run) dry=1; shift ;;
    --no-push) push=0; shift ;;
    --) shift; break ;;
    *) echo "unknown option: $1 (see the header of $0)" >&2; exit 2 ;;
  esac
done
gh_args=("$@")
if [ "$dry" = 0 ] && [ -z "$message" ]; then
  echo "--message is required (commit message and PR title)" >&2
  exit 2
fi

cd "$(git rev-parse --show-toplevel)"
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "working tree has uncommitted changes; commit or stash them first" >&2
  exit 1
fi
original=$(git rev-parse --abbrev-ref HEAD)

git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "$UPSTREAM_URL"
git fetch --quiet upstream "$base"
git fetch --quiet origin "$SOURCE"

in_denylist() {
  local path=$1 prefix
  for prefix in "${DENYLIST[@]}"; do
    case $path in "$prefix"*) return 0 ;; esac
  done
  return 1
}

selected() {
  local path=$1 want
  [ ${#only[@]} -eq 0 ] && return 0
  for want in "${only[@]}"; do
    case $path in "$want"|"$want"/*) return 0 ;; esac
  done
  return 1
}

# status<TAB>path for every difference between upstream and work (no rename detection: plain A/M/D).
changes=()
skipped=()
while IFS=$'\t' read -r status path; do
  [ -n "$path" ] || continue
  if in_denylist "$path"; then
    skipped+=("$path")
  elif selected "$path"; then
    changes+=("$status"$'\t'"$path")
  fi
done < <(git diff --name-status --no-renames "upstream/$base" "origin/$SOURCE")

if [ ${#skipped[@]} -gt 0 ]; then
  echo "fork-only, not sent (${#skipped[@]} files under: ${DENYLIST[*]})"
fi

# Hyphenated snapshots can coexist with the fixed `upstream-submit` branch.
# Git cannot store both `upstream-submit` and `upstream-submit/<timestamp>`.
branch="upstream-submit-$(date +%Y%m%d%H%M%S)"
cleanup() {
  # Only ever runs on the throwaway submission branch (the tree was clean when we started).
  git reset -q --hard
  git checkout -q "$original"
  git branch -D "$branch" >/dev/null 2>&1 || true
}

git checkout -q -B "$branch" "upstream/$base"
for entry in "${changes[@]}"; do
  status=${entry%%$'\t'*}
  path=${entry#*$'\t'}
  if [ "$status" = D ]; then
    git rm -q -- "$path"
  else
    git checkout "origin/$SOURCE" -- "$path"
  fi
done

# Drop fork-only README blocks; keep shared badges but remove their automation markers.
for file in "${STRIP_FILES[@]}"; do
  [ -f "$file" ] || continue
  tmp=$(mktemp)
  awk '
    /<!-- work-only:start -->/ { skip = 1 }
    /<!-- latest-badge:(start|end) -->/ { next }
    !skip { print }
    /<!-- work-only:end -->/   { skip = 0; if ((getline line) > 0 && line != "") print line }
  ' "$file" > "$tmp"
  cat "$tmp" > "$file"
  rm -f "$tmp"
  git add -- "$file"
done

if git grep --cached -l -e 'work-only:' -e 'latest-badge:' >/dev/null 2>&1; then
  echo "refusing: fork-only markers are still present:" >&2
  git grep --cached -l -e 'work-only:' -e 'latest-badge:' >&2
  cleanup
  exit 1
fi

if git diff --cached --quiet; then
  echo "nothing to submit: work differs from upstream/$base only by fork-only files"
  cleanup
  exit 0
fi

echo
echo "would be sent to $UPSTREAM_REPO ($base):"
git diff --cached --stat
if [ "$dry" = 1 ]; then
  cleanup
  exit 0
fi

git commit -q -m "$message"
if [ "$push" = 0 ]; then
  git checkout -q "$original"
  echo "built local branch $branch (not pushed)"
  exit 0
fi

git push -u origin "$branch"
gh pr create --repo "$UPSTREAM_REPO" --base "$base" --head "leejongyoung:$branch" --title "$message" "${gh_args[@]}"
git checkout -q "$original"
echo
echo "work stays untouched. Disposable submission branch: $branch"
