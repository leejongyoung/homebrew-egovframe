# Contributing / 기여 안내

## Branches / 브랜치

| Branch | Purpose |
| --- | --- |
| `main` | Exact mirror of [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). Synced daily, never commit here. |
| `work` | Default branch. This fork's own changes: CI, automation, docs, and cask fixes. Open pull requests against it. |
| `upstream-submit` | Selected upstream-ready commits based on official `main`. |
| `upstream-submit-*` | Disposable snapshots made by `scripts/open_upstream_pr.sh`; separate from the fixed submission branch. |

`main` 은 공식 저장소의 미러라 직접 커밋하지 않습니다. 변경은 기본 브랜치 `work` 로 보내 주세요.

Operational details, schedules and Release backfills: [MAINTENANCE.md](MAINTENANCE.md).
운영·자동화·과거 Release 추가 절차는 별도 유지 관리 문서를 참고하세요.

## Before you open a pull request / PR 전에

```bash
python3 -m unittest discover -s tests -v   # script tests
brew style leejongyoung/egovframe/egovframedev-latest   # needs the tap: brew tap leejongyoung/egovframe
```

CI (`ci.yml`) runs the tests plus `brew readall`, `brew style` and `brew audit` on every cask.

- Commit messages follow the style already used upstream: `feat(casks): add egovframedev@X.Y.Z`,
  `fix(casks): …`, `docs(readme): …`, `ci: …`.
- Do not edit the SHA-256 of a cask by hand. New versions come from `scripts/update_casks.py`
  (the `Update casks` workflow); to re-check an existing hash run `gh workflow run update-casks.yml -f verify=<version>`.
- One cask per minor series: when `5.0.3` is added, `5.0.2` is removed (same convention as upstream).

## Sending something to the official repository / 공식 저장소로 보낼 때

Use the script instead of pushing `work` itself. It builds one clean commit on top of upstream's branch from the
differences between upstream and `work`, and leaves out everything fork-only (`.github/`, `scripts/`, `tests/`
and the README blocks marked `work-only`):

```bash
scripts/open_upstream_pr.sh --dry-run                        # what would be sent
scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
```

## Security / 보안

Do not report vulnerabilities in issues; see [SECURITY.md](SECURITY.md).
취약점은 이슈가 아니라 [SECURITY.md](SECURITY.md) 절차로 알려 주세요.
