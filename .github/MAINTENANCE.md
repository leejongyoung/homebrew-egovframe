# Maintenance / 유지 관리

This document is fork-only. `.github/`, `scripts/`, `tests/` and README `work-only` blocks are excluded by `scripts/open_upstream_pr.sh` when preparing a PR to eGovFramework/homebrew-egovframe.
이 문서는 이 저장소 전용입니다. 공식 저장소로 제출할 때 `.github/` 전체와 `scripts/`, `tests/`, README의 `work-only` 블록은 제외합니다.

## Branches / 브랜치

- `main` mirrors upstream [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). The daily [sync-upstream.yml](workflows/sync-upstream.yml) fast-forwards it and opens a `main` → `work` PR when upstream commits are missing from `work`. It never force-pushes.
- `work` is the default and development branch. CI, automation, community documents and badges live here.
- `upstream-submit` contains only the commits selected for the current upstream PR, based on upstream `main`. `upstream-submit-*` branches are disposable snapshots made by the preparation script; the hyphen avoids a Git ref-name collision with the fixed branch.

`main`은 공식 저장소 미러이며 일일 동기화는 fast-forward만 합니다. 개발·자동화는 기본 브랜치 `work`, 선택한 변경의 공식 저장소 제출은 `upstream-submit`에서 합니다. 스크립트의 일회용 스냅샷은 이름이 충돌하지 않도록 `upstream-submit-*`을 씁니다.

## New releases / 새 버전 감지

Daily [update-casks.yml](workflows/update-casks.yml) reads the [official release list](https://www.egovframe.go.kr/home/sub.do?menuNo=40), also used by cask `livecheck`. For versions newer than `egovframedev-latest`, it checks both macOS architectures, downloads available DMGs, computes SHA-256, adds a versioned cask, removes older patches in the same X.Y series, updates `egovframedev-latest` and both README install lists/badges, and runs `brew style` before opening a PR into `work`. Nothing is merged automatically.

매일 공식 릴리스 목록을 확인하고 양쪽 macOS DMG가 모두 있는 새 버전에 대해 해시를 계산해 cask·최신 버전·설치 목록·배지를 갱신합니다. 같은 X.Y의 이전 패치는 제거하고 style 검사 후 `work` 대상 PR을 엽니다. 자동 머지는 하지 않습니다.

```bash
python3 scripts/update_casks.py --dry-run
python3 scripts/update_casks.py
python3 -m unittest discover -s tests -v
gh workflow run update-casks.yml -f verify=5.0.2
```

A PR opened with `GITHUB_TOKEN` does not itself trigger another workflow. The update job therefore checks generated casks before opening the PR; normal CI also runs when a maintainer merges it.
`GITHUB_TOKEN`으로 생성한 PR 자체는 후속 CI를 실행하지 않으므로 생성 작업에서 검사합니다. 관리자가 머지하면 일반 CI가 실행됩니다.

## GitHub Releases

Merging an update to `Casks/egovframedev-latest.rb` into `work` triggers [release.yml](workflows/release.yml). It publishes the IDE version as the tag, with both download URLs and SHA-256 values. Existing Releases are left unchanged; an older backfill does not replace a newer Latest release.

최신 cask 변경이 `work`에 머지되면 IDE 버전 태그와 다운로드 URL·해시를 담은 Release를 게시합니다. 기존 Release는 유지하고 과거 버전 추가가 Latest를 낮추지 않습니다.

For a missing historical Release, choose a commit containing its cask:
과거 Release는 해당 cask가 있는 커밋을 지정합니다.

```bash
gh workflow run release.yml -f version=5.0.1 -f ref=b4b7b30
```

## Submitting upstream / 공식 저장소 PR

```bash
scripts/open_upstream_pr.sh --dry-run
scripts/open_upstream_pr.sh -m "fix: modernize cask macOS requirements and installation guides"
```

The script excludes fork-only files and README blocks and leaves `work` untouched. Shared installation documentation, eGovFrame/license badges and language links stay in the submission. Only the `latest-badge` automation comment delimiters are removed. Review the printed diff before submitting. See [CONTRIBUTING.md](CONTRIBUTING.md).
스크립트는 저장소 전용 파일·README 블록만 제외하고 `work`를 바꾸지 않습니다. 공용 설치 안내·eGovFrame/라이선스 배지·언어 링크는 제출에 포함하며 배지 갱신용 주석만 제거합니다. 제출 전 diff를 확인하세요.

### Prepared submission / 제출 준비 (2026-10-24)

- Source: `leejongyoung/homebrew-egovframe:upstream-submit`
- Target: `eGovFramework/homebrew-egovframe:main`
- Contents: one clean commit containing seven cask fixes and both shared READMEs; no fork-only infrastructure.
- PR title and verified body: [UPSTREAM_PR.md](UPSTREAM_PR.md). This document is fork-only and is not part of the submission branch.
- Exact snapshot verification: all-platform `brew readall`, `Homebrew/OSDependsOn`, and audit passed. Full style passed for six casks; the existing `egovframedev@4.2.1` legacy `postflight` limitation is disclosed in the PR body. No IDE install/uninstall was performed.

The branch is pushed; no public upstream PR has been opened as part of preparation. To submit from the `work` checkout:
브랜치는 push했으며 준비 단계에서는 공개 PR을 열지 않았습니다. 제출할 때 `work` 체크아웃에서 실행하세요.

```bash
gh pr create --repo eGovFramework/homebrew-egovframe --base main \
  --head leejongyoung:upstream-submit \
  --title "fix: modernize cask macOS requirements and installation guides" \
  --body-file .github/UPSTREAM_PR.md
```


## Security reports / 보안 접수

Use [private vulnerability reporting](https://github.com/leejongyoung/homebrew-egovframe/security/advisories/new), not public issues. See [SECURITY.md](SECURITY.md).
취약점은 공개 이슈가 아니라 비공개 신고를 이용하세요.
