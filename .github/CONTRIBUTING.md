# Contributing

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/flat.svg)](/docs/contributing/CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](/docs/contributing/CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](/docs/contributing/CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](/docs/contributing/CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](/docs/contributing/CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](/docs/contributing/CONTRIBUTING.fr.md)

<!-- work-only:start -->
## Branches

| Branch | Purpose |
| --- | --- |
| `main` | Exact mirror of [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). Synced daily, never commit here. |
| `work` | Default branch. This fork's own changes: CI, automation, docs, and cask fixes. Open pull requests against it. |
| `upstream-submit` | Upstream-ready commit based on official `main`; updated automatically after `work` CI passes when no upstream PR is open. |
| `upstream-submit-*` | Disposable snapshots made by `scripts/open_upstream_pr.sh`; separate from the fixed submission branch. |

`main` is a mirror of the official repository, so do not commit to it directly. Send changes to the default branch, `work`.

Operational details, schedules and Release backfills: [MAINTENANCE.md](/.github/MAINTENANCE.md).
<!-- work-only:end -->

## Before you open a pull request

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # script tests
brew style leejongyoung/egovframe/egovframedev-latest   # needs the tap: brew tap leejongyoung/egovframe
```

CI (`ci.yml`) runs the tests plus `scripts/check_tap.sh` (`brew readall`, `brew style` and `brew audit`). Run the commands from the repository root; the script tests need PyYAML, which CI installs the same way.

- Commit messages follow the style already used upstream: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- Do not edit the SHA-256 of a cask by hand. New versions come from `scripts/update_casks.py` (the `Update casks` workflow); to re-check an existing hash run `gh workflow run update-casks.yml -f verify=<version>`.
- One cask per minor series: when `5.0.3` is added, `5.0.2` is removed (same convention as upstream).

## GitHub Actions & Billing

- **Free on public repositories:** Standard GitHub-hosted runners (`ubuntu-latest`, `macos-latest`) are **free without minute limits on public repositories** under GitHub's billing policy. DMGs are hashed in-stream during `update-casks.yml` and are never uploaded as Actions artifacts or Release assets, so no Actions storage quota is consumed either.
- Minutes are deducted from your account's free allowance only if you copy the repository into a private repository and run it there.

<!-- work-only:start -->
## Sending something to the official repository

Use the script instead of pushing `work` itself. It builds one clean commit on top of upstream's branch from the differences between upstream and `work`, and leaves out fork-only files (`.github/MAINTENANCE.md`, `.github/UPSTREAM_PR.md`, `.github/workflows/sync-upstream.yml`, `scripts/open_upstream_pr.sh`, `tests/test_open_upstream_pr.py`, and blocks marked `work-only`):

```bash
scripts/open_upstream_pr.sh --dry-run                        # what would be sent
scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
```
<!-- work-only:end -->

## Security

Do not report vulnerabilities in issues; follow the process in [SECURITY.en.md](/docs/security/SECURITY.en.md).
