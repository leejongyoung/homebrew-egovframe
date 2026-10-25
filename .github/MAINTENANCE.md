# Maintenance / 유지 관리

This document is fork-only. `scripts/open_upstream_pr.sh` excludes the fork's maintenance, PR preparation, mirror-sync and submission tooling, and removes `work-only` blocks from shared documents/workflows. Shared documentation, CI and cask/release tools are included.
이 문서는 이 저장소 전용입니다. 공식 저장소 제출 시 유지 관리·PR 준비 문서와 미러 동기화·제출 도구 및 `work-only` 블록만 제외합니다. 공용 문서·CI·Cask/Release 도구는 포함합니다.

## Branches / 브랜치

- `main` mirrors upstream [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). The daily [sync-upstream.yml](workflows/sync-upstream.yml) fast-forwards it and opens a `main` → `work` PR when upstream commits are missing from `work`. It never force-pushes.
- `work` is the default and development branch. CI, automation, community documents and badges live here.
- `upstream-submit` contains only the upstream-ready commits based on upstream `main` (shared casks and shared README changes, never fork-only files). When `work` pushes pass CI and no upstream PR is currently open from `upstream-submit`, CI updates `upstream-submit` automatically. `upstream-submit-*` branches are disposable snapshots made by the preparation script; the hyphen avoids a Git ref-name collision with the fixed branch.

`main`은 공식 저장소 미러이며 일일 동기화는 fast-forward만 합니다. 개발·자동화는 기본 브랜치 `work`, 선택한 변경의 공식 저장소 제출은 `upstream-submit`에서 합니다. `work`의 CI가 통과하고 열린 upstream PR이 없으면 `upstream-submit`도 자동으로 갱신됩니다.

## New releases / 새 버전 감지

Daily [update-casks.yml](workflows/update-casks.yml) reads the [official release list](https://www.egovframe.go.kr/home/sub.do?menuNo=40), also used by cask `livecheck`. For versions newer than `egovframedev-latest`, it checks both macOS architectures, downloads available DMGs, computes SHA-256, adds a versioned cask, removes older patches in the same X.Y series, updates `egovframedev-latest`, all six localized README install lists/badges and the generated root README, and runs the unit tests plus `scripts/check_tap.sh` (`brew readall`, `brew style`, `brew audit`) before opening a PR into `work`. Nothing is merged automatically.

매일 공식 릴리스 목록을 확인하고 양쪽 macOS DMG가 모두 있는 새 버전에 대해 해시를 계산해 cask·최신 버전·설치 목록·배지를 갱신합니다. 같은 X.Y의 이전 패치는 제거하고 단위 테스트와 `brew readall`·`style`·`audit` 검사를 모두 통과하면 `work` 대상 PR을 엽니다. 자동 머지는 하지 않습니다.

```bash
python3 scripts/update_casks.py --dry-run
python3 scripts/update_casks.py
python3 -m unittest discover -s tests -v
gh workflow run update-casks.yml -f verify=5.0.2
```

A PR opened with `GITHUB_TOKEN` does not itself trigger another workflow. The update job therefore checks generated casks before opening the PR; normal CI also runs when a maintainer merges it.
`GITHUB_TOKEN`으로 생성한 PR 자체는 후속 CI를 실행하지 않으므로 생성 작업에서 검사합니다. 관리자가 머지하면 일반 CI가 실행됩니다.

## GitHub Releases

Merging a cask change into `work` triggers [release.yml](workflows/release.yml) (`scripts/publish_releases.py`). Only the final maintained version of each available 3.x, 4.x and 5.x minor series in `Casks/` is eligible for a GitHub Release (`5.0.2`, `4.3.1`, `4.2.1`, `4.1.1`, `4.0.0`, `3.10.0`). When a security/maintenance patch supersedes an initial `.0` or earlier patch in the same X.Y series, the superseded GitHub Release record is removed while its Git tag and commit remain intact.

`work`의 cask가 바뀌면 [release.yml](workflows/release.yml)(`scripts/publish_releases.py`)이 실행됩니다. 3.x·4.x·5.x 각 마이너 계열에서 현재 유지되는 최종 버전만 GitHub Release로 게시하며, 같은 X.Y 계열에서 후속 보안·유지보수 패치로 대체된 이전 Release 게시물은 제거하되 Git 태그와 커밋은 보존합니다.

```bash
python3 scripts/publish_releases.py --dry-run
gh workflow run release.yml -f dry_run=true
```

## Submitting upstream / 공식 저장소 PR

```bash
scripts/open_upstream_pr.sh --dry-run
scripts/open_upstream_pr.sh --update-branch upstream-submit -m "feat(casks): sync eGovFrame IDE 5.0.2 and installation guides"
```

The script excludes fork-only files and blocks and preserves shared documentation, badges and explicit language links, including the nested code-signing guides. The `latest-badge` delimiters remain because the cask updater uses them. Review the printed diff before submitting. See [CONTRIBUTING.md](CONTRIBUTING.md).
스크립트는 저장소 전용 파일·블록만 제외하고 공용 문서·배지·언어별 원본 링크와 중첩된 코드 서명 가이드를 포함합니다. `latest-badge` 주석은 Cask 갱신에 필요하므로 유지합니다. 제출 전 diff를 확인하세요.

Submission READMEs preserve the existing workflow badge image URLs, appearance and result links from `work`. Those badges report this fork's actual GitHub Actions runs; they are not claims about runs in the official repository. Do not rewrite their URLs to upstream or replace them with a different badge style.
제출본에서도 `work`의 기존 배지 이미지·스타일·실행 결과 링크를 그대로 유지합니다. CI·Update casks 배지는 이 포크의 실제 실행 상태이며 공식 저장소의 실행 결과라는 뜻은 아닙니다. URL을 공식 저장소로 치환하거나 새로운 배지 스타일로 바꾸지 않습니다.

### Prepared submission / 제출 준비 (2026-10-24)

- Source: `leejongyoung/homebrew-egovframe:upstream-submit`
- Target: `eGovFramework/homebrew-egovframe:main`
- Contents: one clean commit containing seven cask fixes, all six localized README and signing-guide sources, root entry generation, the original workflow badges, community/security docs, and automatic cask update/CI/Release workflows; no fork-only infrastructure.
- PR title and verified body: [UPSTREAM_PR.md](UPSTREAM_PR.md). This document is fork-only and is not part of the submission branch.
- Exact snapshot verification: all-platform `brew readall`, `Homebrew/OSDependsOn`, and audit passed. Full style passed for six casks; the existing `egovframedev@4.2.1` legacy `postflight` limitation is disclosed in the PR body. No IDE install/uninstall was performed.

Submitted as upstream PR [#6](https://github.com/eGovFramework/homebrew-egovframe/pull/6). While that PR is open, automatic updates to `upstream-submit` are skipped so the open PR is not overwritten.
공식 저장소 PR [#6](https://github.com/eGovFramework/homebrew-egovframe/pull/6)로 제출했습니다. 이 PR이 열려 있는 동안에는 `upstream-submit` 자동 덮어쓰기를 건너뜁니다.

The multilingual code-signing guide reorganization, documentation-sync fixes and original workflow badges are included when explicitly refreshing `upstream-submit`. Automatic updates still stop while PR #6 is open. Only after the user requests an update, `UPSTREAM_OPEN_PR= scripts/open_upstream_pr.sh --update-branch upstream-submit -m "<title>"` deliberately refreshes the existing submission using force-with-lease.
다국어 코드 서명 가이드·문서 동기화 수정·기존 워크플로 배지는 명시적인 제출본 갱신 시 함께 포함합니다. PR #6이 열려 있는 동안 자동 갱신을 막는 방침은 유지하며, 사용자 요청이 있을 때만 위 명령으로 기존 제출본을 갱신합니다.

The original workflow badges are retained; the replacement local SVG assets were removed at the user's request. No new PR, app install, signing or notarization was performed.
사용자 요청대로 기존 워크플로 배지를 유지하고 대체용 로컬 SVG를 제거했습니다. 별도 PR 생성이나 앱 설치·서명·공증은 하지 않았습니다.

Original-badge restoration: all seven submitted READMEs have byte-identical workflow badge lines to `work`; all 70 README badge images loaded on GitHub. The submission regression suite passed 11 tests and shellcheck passed. The original version/language/license badges were not restyled.
기존 배지 복원 검증: 제출 README 7개의 워크플로 배지 문구·이미지 URL·클릭 링크가 `work`와 정확히 같으며 GitHub에서 배지 70개가 모두 표시됩니다. 제출 회귀 테스트 11개와 shellcheck가 통과했습니다. 버전·언어·라이선스 배지 스타일은 바꾸지 않았습니다.

```bash
gh pr create --repo eGovFramework/homebrew-egovframe --base main \
  --head leejongyoung:upstream-submit \
  --title "fix: modernize cask macOS requirements and installation guides" \
  --body-file .github/UPSTREAM_PR.md
```


## GitHub Actions Billing / Actions 비용 안내

- Public repositories on GitHub get unlimited free minutes on standard GitHub-hosted runners (`ubuntu-latest`, `macos-latest`), and these workflows upload no Actions artifacts.
- 공개(Public) 저장소에서는 표준 GitHub 호스팅 러너(`ubuntu-latest`, `macos-latest`) 사용료가 무료이며 아티팩트도 저장하지 않아 비용이 청구되지 않습니다. (비공개 저장소에서만 무료 분량 차감 및 macOS 10배율이 적용됩니다.)

## Security reports / 보안 접수

Use [private vulnerability reporting](https://github.com/leejongyoung/homebrew-egovframe/security/advisories/new), not public issues. See [SECURITY.md](SECURITY.md).
취약점은 공개 이슈가 아니라 비공개 신고를 이용하세요.

## Multilingual documentation / 다국어 문서

- Canonical README sources: `docs/README.<lang>.md`; code-signing sources: `docs/code-signing-guideline/code-signing-guideline.<lang>.md`, for `en`, `ko`, `es`, `vi`, `ar`, `fr`.
- Community sources: `docs/contributing/CONTRIBUTING.<lang>.md` and `docs/security/SECURITY.<lang>.md`, with the same six languages and existing language badges. Keep `.github/CONTRIBUTING.md` and `.github/SECURITY.md` as generated default-language entrypoints so GitHub still discovers the contribution and security policies.
- Keep the language badge navigation, but do not add standalone “Back to README” links (including translated equivalents) to guides or other Markdown documents.
- `docs/config.yml` selects `default_language` and maps each document family to its sources. Edit the sources, then run `uv run scripts/sync_readme.py` to generate root `README.md`, `code-signing-guideline.md`, `.github/CONTRIBUTING.md` and `.github/SECURITY.md`. Root entrypoints rebase relative links; `.github/` entrypoints use repository-root-relative paths such as `/docs/security/SECURITY.ko.md`. GitHub supplies the viewed repository and branch in both file previews and the Security policy tab. Do not hardcode repository owners or branch names in internal document links; localized sources retain relative links.
- Every language badge targets an explicit localized source, including English. Do not link English to the root entry or reintroduce `README.ko.md`, `docs/README.md` or flat `docs/code-signing-guideline.*.md` duplicates.
- The documentation sync workflow watches all four source families/configuration and stages all four entrypoints when changed. The cask updater also refreshes the root README before opening its PR, because token-created commits do not trigger another sync workflow. Upstream preparation strips fork-only sections and rewrites reporting/package repository references, but document navigation stays relative and works on the unmerged `upstream-submit` branch as well as the official `main` branch after merging.
- 언어별 원본을 고친 뒤 동기화 명령을 실행합니다. 루트 진입점은 설정된 기본 언어에서 생성하며 상대 링크를 다시 계산합니다. 영어 버튼도 `docs/README.en.md` 또는 해당 가이드의 `.en.md` 원본으로 이동해야 합니다.

### Verification / 검증 (2026-10-24)

- `uv run --no-project --with PyYAML==6.0.3 python -m unittest discover -s tests -v`: 57 tests passed, including default-language selection, community navigation on both GitHub policy/file views, atomic handling of missing policy sources, changed/no-op Actions output, updater root freshness and nested upstream document preparation.
- `uv run scripts/sync_readme.py`: checked-in root entries already current. In an isolated copy with `default_language: ko`, both entries selected Korean, English buttons retained explicit `.en.md` destinations, and successive CLI runs reported `changed=true` then `changed=false` through the Actions output file.
- Markdown parsing resolved all 119 local links in the 14 root/localized README and signing-guide documents.
- `uv run scripts/update_casks.py --dry-run`: official release page reported current latest `5.0.2`, no additions/removals. `shellcheck` and `actionlint` passed.
- Signing/notarization commands are documentation examples only: no app was signed, uploaded or installed; no signing certificates or credentials were read. New translations have not received native-speaker review.

### Community policy verification / 기여·보안 문서 검증

- The two `.github/` entrypoints and twelve localized contribution/security sources have six existing language badges each; all 126 repository file targets resolve, including repository-root-relative paths generated for the entrypoints.
- A throwaway copy with `default_language: ko` generated Korean contribution and security entrypoints at GitHub's recognized paths, preserved the private-reporting URL and used repository-root-relative language/security links. Actions output listed all four generated entries; a second CLI run reported `changed=false`.
- No public vulnerability report, private advisory submission, repository security-setting change or new reporting contact was created.
- The language-navigation regression failed with the previous branch-pinned URLs and passed after switching to `/docs/...` links; the complete suite still passes 57 tests. This removes the former dependency on the official repository already containing the translated files before merging.
- Live GitHub verification clicked all six language buttons from each `upstream-submit` community entrypoint (12 destinations), observed the translated headings, and confirmed every destination stayed on that branch. The live Security policy tab also reached the Spanish source on `work`. The exact submitted snapshot passed 46 tests and regeneration changed no entrypoints.

