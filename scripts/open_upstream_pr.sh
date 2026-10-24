#!/usr/bin/env bash
# Open a pull request against upstream eGovFramework/homebrew-egovframe with only what belongs
# upstream: the changes of `work` over upstream's default branch, minus fork-only files.
#
# The submission branch is built on top of upstream's branch (not on `work`), so the PR carries one
# clean commit and none of this fork's CI/automation history. `work` itself is never touched.
#
# Fork-only, never sent upstream:
#   - .github/MAINTENANCE.md  .github/UPSTREAM_PR.md
#   - .github/workflows/sync-upstream.yml
#   - scripts/open_upstream_pr.sh  tests/test_open_upstream_pr.py
#   - blocks between `work-only:start` and `work-only:end` in shared docs/workflows
# Usage: scripts/open_upstream_pr.sh -m "<commit and PR title>" [options] [-- <gh pr create options>]
#   -m, --message TEXT   commit message, also the PR title (required unless --dry-run)
#       --only PATH      send only this file or directory (repeatable), e.g. --only Casks/egovframedev@4.2.1.rb
#       --base BRANCH    upstream branch to build on and target (default: main)
#       --dry-run        show what would be sent; create nothing
#       --no-push        build the local submission branch, do not push or open a PR
#       --update-branch B update branch B (e.g. upstream-submit) to the single clean commit and push it
#                         without opening a new PR; skips if an open upstream PR already uses B
# Examples:
#   scripts/open_upstream_pr.sh --dry-run
#   scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
#   scripts/open_upstream_pr.sh -m "feat(casks): add egovframedev@5.0.3" -- --body-file /tmp/body.md
set -euo pipefail

UPSTREAM_REPO="eGovFramework/homebrew-egovframe"
UPSTREAM_URL="https://github.com/$UPSTREAM_REPO.git"
SOURCE="work"
DENYLIST=(
  ".github/MAINTENANCE.md"
  ".github/UPSTREAM_PR.md"
  ".github/workflows/sync-upstream.yml"
  "scripts/open_upstream_pr.sh"
  "tests/test_open_upstream_pr.py"
)
STRIP_FILES=(
  "README.md"
  "README.ko.md"
  "docs/README.es.md"
  "docs/README.vi.md"
  "docs/README.ar.md"
  "docs/README.fr.md"
  ".github/CONTRIBUTING.md"
  ".github/SECURITY.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/workflows/ci.yml"
)
REWRITE_FILES=(
  "README.md"
  "README.ko.md"
  "docs/README.es.md"
  "docs/README.vi.md"
  "docs/README.ar.md"
  "docs/README.fr.md"
  ".github/CONTRIBUTING.md"
  ".github/SECURITY.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/ISSUE_TEMPLATE/config.yml"
)

message=""
base="main"
dry=0
push=1
only=()
update_branch=""
while [ $# -gt 0 ]; do
  case $1 in
    -m|--message) message=${2:?--message needs text}; shift 2 ;;
    --only) only+=("${2:?--only needs a path}"); shift 2 ;;
    --base) base=${2:?--base needs a branch}; shift 2 ;;
    --update-branch) update_branch=${2:?--update-branch needs a branch}; shift 2 ;;
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
if [ -n "$update_branch" ]; then
  git fetch --quiet origin "$update_branch" 2>/dev/null || true
  open_pr=""
  if [ -n "${UPSTREAM_OPEN_PR+x}" ]; then
    open_pr="$UPSTREAM_OPEN_PR"
  elif [ "$push" = 1 ] && [ "$dry" = 0 ]; then
    open_pr=$(gh api "repos/$UPSTREAM_REPO/pulls?state=open&head=leejongyoung:$update_branch" --jq '.[0].number // empty')
  fi
  if [ -n "$open_pr" ]; then
    echo "upstream PR #$open_pr is already open from $update_branch — skipping update so the open PR is not overwritten"
    exit 0
  fi
fi

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

# Drop fork-only blocks; keep shared badges and their `latest-badge` markers for update_casks.py.
for file in "${STRIP_FILES[@]}"; do
  if [ ! -f "$file" ] || ! selected "$file"; then continue; fi
  tmp=$(mktemp)
  awk '
    /<!-- work-only:start -->|^# work-only:start$/ { skip = 1 }
    !skip { print }
    /<!-- work-only:end -->|^# work-only:end$/ { skip = 0; if ((getline line) > 0 && line != "") print line }
  ' "$file" > "$tmp"
  cat "$tmp" > "$file"
  rm -f "$tmp"
  git add -- "$file"
done

for file in "${REWRITE_FILES[@]}"; do
  if [ ! -f "$file" ] || ! selected "$file"; then continue; fi
  tmp=$(mktemp)
  # shellcheck disable=SC2016
  sed \
    -e 's#leejongyoung/homebrew-egovframe#eGovFramework/homebrew-egovframe#g' \
    -e 's#leejongyoung/egovframe/#egovframework/egovframe/#g' \
    -e 's#tap leejongyoung/egovframe#tap egovframework/egovframe#g' \
    -e 's#(`work`)#(`main`)#g' \
    "$file" > "$tmp"
  cat "$tmp" > "$file"
  rm -f "$tmp"
  git add -- "$file"
done

if git grep --cached -l -e 'work-only:' >/dev/null 2>&1; then
  echo "refusing: fork-only markers are still present:" >&2
  git grep --cached -l -e 'work-only:' >&2
  cleanup
  exit 1
fi

if git diff --cached --quiet; then
  echo "nothing to submit: work differs from upstream/$base only by fork-only files"
  cleanup
  exit 0
fi
restack_source_onto() {
  local parent_ref=$1 new_work
  if git merge-base --is-ancestor "$parent_ref" "origin/$SOURCE" 2>/dev/null; then
    return 0
  fi
  new_work=$(git commit-tree "origin/$SOURCE^{tree}" -p "$parent_ref" \
    -m "chore(fork): add fork-only sync workflow, maintenance docs and PR tooling")
  if [ "$(git rev-parse --abbrev-ref HEAD)" = "$SOURCE" ]; then
    git reset -q --hard "$new_work"
  else
    git branch -f "$SOURCE" "$new_work"
  fi
  if [ "$push" = 1 ]; then
    git push --force-with-lease origin "$SOURCE:refs/heads/$SOURCE"
  fi
}

if [ -n "$update_branch" ] && git rev-parse --verify --quiet "origin/$update_branch" >/dev/null; then
  if git diff --cached --quiet "origin/$update_branch" && \
     [ "$(git rev-parse "origin/$update_branch^" 2>/dev/null || true)" = "$(git rev-parse "upstream/$base")" ]; then
    cleanup
    git branch -f "$update_branch" "origin/$update_branch"
    restack_source_onto "$update_branch"
    echo "$update_branch is already up to date with work's upstream-ready changes"
    exit 0
  fi
fi

echo
echo "would be sent to $UPSTREAM_REPO ($base):"
git diff --cached --stat
if [ "$dry" = 1 ]; then
  cleanup
  exit 0
fi

git commit -q -m "$message"
if [ -n "$update_branch" ]; then
  git branch -f "$update_branch" "$branch"
  cleanup
  if [ "$push" = 0 ]; then
    restack_source_onto "$update_branch"
    echo "updated local branch $update_branch (not pushed)"
    exit 0
  fi
  git push --force-with-lease origin "$update_branch:refs/heads/$update_branch"
  restack_source_onto "$update_branch"
  echo "updated origin/$update_branch with one clean commit on top of upstream/$base"
  exit 0
fi
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
