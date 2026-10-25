# 기여 안내

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/flat.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](CONTRIBUTING.fr.md)

<!-- work-only:start -->
## 브랜치

| 브랜치 | 용도 |
| --- | --- |
| `main` | 공식 저장소 [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe)의 정확한 미러입니다. 매일 동기화되며 여기에는 절대 커밋하지 않습니다. |
| `work` | 기본 브랜치입니다. 이 포크의 자체 변경(CI, 자동화, 문서, cask 수정)이 들어갑니다. 풀 리퀘스트는 이 브랜치로 보내 주세요. |
| `upstream-submit` | 공식 `main` 을 기반으로 한 업스트림 제출용 커밋입니다. 열린 업스트림 PR이 없을 때 `work` CI가 통과하면 자동으로 갱신됩니다. |
| `upstream-submit-*` | `scripts/open_upstream_pr.sh` 가 만드는 일회용 스냅샷이며, 고정된 제출 브랜치와는 별개입니다. |

`main` 은 공식 저장소의 미러이므로 직접 커밋하지 않습니다. 변경은 기본 브랜치 `work` 로 보내 주세요.

운영, 일정, 과거 Release 추가 절차: [MAINTENANCE.md](../../.github/MAINTENANCE.md).
<!-- work-only:end -->

## 풀 리퀘스트를 열기 전에

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # 스크립트 테스트
brew style leejongyoung/egovframe/egovframedev-latest   # 탭이 필요합니다: brew tap leejongyoung/egovframe
```

CI(`ci.yml`)는 테스트와 함께 `scripts/check_tap.sh`(`brew readall`, `brew style`, `brew audit`)를 실행합니다. 명령은 저장소 루트에서 실행하세요. 스크립트 테스트에는 PyYAML이 필요하며 CI도 같은 방식으로 설치합니다.

- 커밋 메시지는 업스트림에서 이미 쓰는 형식을 따릅니다: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- cask의 SHA-256 은 직접 수정하지 마세요. 새 버전은 `scripts/update_casks.py`(`Update casks` 워크플로)로 만들어지며, 기존 해시를 다시 확인하려면 `gh workflow run update-casks.yml -f verify=<version>` 을 실행하세요.
- 마이너 시리즈당 cask 하나: `5.0.3` 을 추가하면 `5.0.2` 는 제거합니다(업스트림과 같은 규칙).

## GitHub Actions 및 비용

- **공개 저장소는 무료:** GitHub의 요금 정책에 따라 공개 저장소에서는 표준 GitHub 호스팅 러너(`ubuntu-latest`, `macos-latest`)를 **분 제한 없이 무료**로 사용할 수 있습니다. DMG 파일은 `update-casks.yml` 실행 중 스트림으로 해시만 계산하며 Actions 아티팩트나 Release 자산으로 업로드하지 않으므로 Actions 스토리지 할당량도 사용하지 않습니다.
- 저장소를 비공개 저장소로 복제해 실행하는 경우에만 계정의 무료 제공량에서 사용 시간이 차감됩니다.

<!-- work-only:start -->
## 공식 저장소로 보낼 때

`work` 자체를 푸시하지 말고 스크립트를 사용하세요. 업스트림과 `work` 의 차이로부터 업스트림 브랜치 위에 깨끗한 커밋 하나를 만들며, 포크 전용 파일(`.github/MAINTENANCE.md`, `.github/UPSTREAM_PR.md`, `.github/workflows/sync-upstream.yml`, `scripts/open_upstream_pr.sh`, `tests/test_open_upstream_pr.py`, 그리고 `work-only` 로 표시된 블록)은 제외합니다.

```bash
scripts/open_upstream_pr.sh --dry-run                        # 보낼 내용 미리 보기
scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
```
<!-- work-only:end -->

## 보안

취약점은 이슈로 신고하지 말고 [SECURITY.ko.md](../security/SECURITY.ko.md) 의 절차를 따라 알려 주세요.
