# Maintenance / 유지 관리

This document is fork-only. `.github/`, `scripts/`, `tests/` and README `work-only` blocks are excluded by `scripts/open_upstream_pr.sh` when preparing a PR to eGovFramework/homebrew-egovframe.
이 문서는 이 저장소 전용입니다. 공식 저장소로 제출할 때 `.github/` 전체와 `scripts/`, `tests/`, README의 `work-only` 블록은 제외합니다.

## Branches / 브랜치

- `main` mirrors upstream [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). The daily [sync-upstream.yml](workflows/sync-upstream.yml) fast-forwards it and opens a `main` → `work` PR when upstream commits are missing from `work`. It never force-pushes.
- `work` is the default and development branch. CI, automation, community documents and badges live here.
- `upstream-submit` contains only the upstream-ready commits based on upstream `main` (shared casks and shared README changes, never fork-only files). When `work` pushes pass CI and no upstream PR is currently open from `upstream-submit`, CI updates `upstream-submit` automatically. `upstream-submit-*` branches are disposable snapshots made by the preparation script; the hyphen avoids a Git ref-name collision with the fixed branch.

`main`은 공식 저장소 미러이며 일일 동기화는 fast-forward만 합니다. 개발·자동화는 기본 브랜치 `work`, 선택한 변경의 공식 저장소 제출은 `upstream-submit`에서 합니다. `work`의 CI가 통과하고 열린 upstream PR이 없으면 `upstream-submit`도 자동으로 갱신됩니다.

## New releases / 새 버전 감지

Daily [update-casks.yml](workflows/update-casks.yml) reads the [official release list](https://www.egovframe.go.kr/home/sub.do?menuNo=40), also used by cask `livecheck`. For versions newer than `egovframedev-latest`, it checks both macOS architectures, downloads available DMGs, computes SHA-256, adds a versioned cask, removes older patches in the same X.Y series, updates `egovframedev-latest` and both README install lists/badges, and runs the unit tests plus `scripts/check_tap.sh` (`brew readall`, `brew style`, `brew audit`) before opening a PR into `work`. Nothing is merged automatically.

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

The script excludes fork-only files and README blocks and leaves `work` untouched. Shared installation documentation, eGovFrame/license badges and language links stay in the submission. Only the `latest-badge` automation comment delimiters are removed. Review the printed diff before submitting. See [CONTRIBUTING.md](CONTRIBUTING.md).
스크립트는 저장소 전용 파일·README 블록만 제외하고 `work`를 바꾸지 않습니다. 공용 설치 안내·eGovFrame/라이선스 배지·언어 링크는 제출에 포함하며 배지 갱신용 주석만 제거합니다. 제출 전 diff를 확인하세요.

### Prepared submission / 제출 준비 (2026-10-24)

- Source: `leejongyoung/homebrew-egovframe:upstream-submit`
- Target: `eGovFramework/homebrew-egovframe:main`
- Contents: one clean commit containing seven cask fixes, shared READMEs, community/security docs, and automatic cask update/CI/Release workflows; no fork-only infrastructure.
- PR title and verified body: [UPSTREAM_PR.md](UPSTREAM_PR.md). This document is fork-only and is not part of the submission branch.
- Exact snapshot verification: all-platform `brew readall`, `Homebrew/OSDependsOn`, and audit passed. Full style passed for six casks; the existing `egovframedev@4.2.1` legacy `postflight` limitation is disclosed in the PR body. No IDE install/uninstall was performed.

Submitted as upstream PR [#6](https://github.com/eGovFramework/homebrew-egovframe/pull/6). While that PR is open, automatic updates to `upstream-submit` are skipped so the open PR is not overwritten.
공식 저장소 PR [#6](https://github.com/eGovFramework/homebrew-egovframe/pull/6)로 제출했습니다. 이 PR이 열려 있는 동안에는 `upstream-submit` 자동 덮어쓰기를 건너뜁니다.

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
