## 변경 요약

### 1. Cask의 macOS 의존성 선언을 최신 Homebrew 규칙(`Homebrew/OSDependsOn`)에 맞게 수정
- `egovframedev-latest`, `egovframedev@4.3.1`, `egovframedev@5.0.2`의 `depends_on macos: ">= :big_sur"`를 `depends_on :macos`로 변경했습니다.
- `egovframedev@3.10.0`, `egovframedev@4.0.0`, `egovframedev@4.1.1`, `egovframedev@4.2.1`에 `depends_on :macos`를 추가했습니다.
- 최신 Homebrew에서는 문자열 비교 형식(`">= :big_sur"`)이 deprecated 처리되어 오류로 거부되며, macOS 전용 Cask에는 `depends_on :macos` 선언을 요구합니다.

### 2. 6개 국어 README(`README.md`, `README.ko.md`, `docs/README.{es,vi,ar,fr}.md`) 및 커뮤니티·보안 문서 추가
- 루트에는 기본 영문(`README.md`)과 국문(`README.ko.md`)을 두고, 표준프레임워크 주요 해외 수출·협력 권역 공용어 4종(스페인어 `docs/README.es.md`, 베트남어 `docs/README.vi.md`, 아랍어 `docs/README.ar.md`, 프랑스어 `docs/README.fr.md`)을 `docs/` 하위에 구성했습니다.
- 각 문서 상단에 언어별 표준프레임워크 버전 배지(5.0.2), CI·업데이트·Apache-2.0 라이선스 배지, 그리고 클릭해 언어를 전환할 수 있는 **다국어 선택 배지 버튼(`EN`, `KO`, `ES`, `VI`, `AR`, `FR`)**을 추가했습니다.
- 공식 Tap 추가(`brew tap egovframework/egovframe`), 최신 버전 Cask(`egovframedev-latest`) 설치·업그레이드 명령, 버전별 설치 명령과 아키텍처·앱 경로 안내를 실제 Cask 정의에 맞게 정리했습니다.
- 보안 취약점 비공개 접수 안내(`.github/SECURITY.md`), 기여 가이드(`.github/CONTRIBUTING.md`), 이슈·PR 템플릿(`.github/ISSUE_TEMPLATE/*`, `.github/PULL_REQUEST_TEMPLATE.md`)을 추가했습니다.

### 3. 새 IDE 릴리스 자동 감지·Cask 갱신 도구 및 CI/Release 워크플로 추가
- **`scripts/update_casks.py` & `.github/workflows/update-casks.yml`:** 표준프레임워크 포털 개발환경 페이지(`menuNo=40`)에서 새 버전을 감지하면 Apple Silicon·Intel DMG 배포 여부를 확인하고 SHA-256 해시를 계산해 `Casks/egovframedev@X.Y.Z.rb`, `Casks/egovframedev-latest.rb`, 6개 국어 README의 버전 목록과 언어별 배지를 한 번에 갱신한 뒤 전체 검증 통과 시 PR을 생성합니다.
- **`scripts/check_tap.sh` & `.github/workflows/ci.yml`:** 단위 테스트(`tests/`)와 Homebrew 구문·스타일·감사(`brew readall`, `brew style`, `brew audit`)를 자동으로 검사합니다.
- **`scripts/publish_releases.py`, `scripts/release_notes.py` & `.github/workflows/release.yml`:** 3.x·4.x·5.x 각 마이너 계열의 최종 정식 버전에 대해 아키텍처별 다운로드 링크와 SHA-256을 포함한 GitHub Release를 게시합니다.

> 이 PR은 공식 `main` 브랜치 위의 단일 커밋입니다. 기존 Cask의 버전, 다운로드 URL, SHA-256 해시, 앱 번들 경로 및 설치 동작은 변경하지 않았으며, 개인 포크 전용 동기화·제출 스크립트는 제외했습니다.

## 검증 내역

격리된 로컬 Tap 환경(Homebrew `7.0.10-65-g786fc9e`)과 GitHub Actions에서 검증했습니다.

- `python3 -m unittest discover -s tests -v`: Cask 자동 갱신·Release 노트·Release 정책 단위 테스트 통과
- `brew readall --aliases --os=all --arch=all`: 전체 Cask 로드 통과 (아래에 적은 기존 `4.2.1`의 `postflight` 경고만 출력)
- `brew style --only-cops=Homebrew/OSDependsOn`: 전체 파일 위반 없음(0 offenses)
- 전체 `brew style`: `egovframedev@4.2.1`(`.github/style-exempt.txt`에 명시)을 제외한 6개 Cask 모두 통과
- `brew audit --cask --except=installed`: 7개 Cask 모두 통과

## 변경 범위 밖의 참고 사항

- `egovframedev@4.2.1`에 기존부터 포함된 `postflight` 블록은 최신 Homebrew의 `Cask/InstallSteps` 규칙에서 선언형 `postflight_steps`로의 전환을 권장합니다. 이 전환은 실제 설치 동작에 영향을 줄 수 있어 이번 PR에서는 기존 코드를 그대로 유지하고 `.github/style-exempt.txt`로만 분리했습니다.
- 이번 PR은 메타데이터·의존성 문법·문서 및 자동화 추가이므로 실제 대용량 DMG 설치/삭제 테스트는 수행하지 않았습니다.

## 병합 후 권장 저장소 설정 (관리자 참고)

워크플로와 보안·이슈 템플릿은 추가 설정 없이도 실패하지 않도록 방어 처리되어 있으나, 아래 저장소 설정을 켜 두시면 모든 기능이 100% 자동으로 동작합니다.

1. **자동 PR 생성 허용 (`Settings → Actions → General → Workflow permissions`)**
   - **`Allow GitHub Actions to create and approve pull requests`** 체크
   - 활성화 시 `update-casks.yml`이 새 IDE 버전 감지 후 `auto/egovframedev-X.Y.Z` 브랜치 푸시와 함께 `main` 대상 PR을 자동으로 생성합니다. (비활성화 상태여도 브랜치 푸시는 정상 완료되며 Actions 실행 요약에 수동 PR 생성 링크가 출력됩니다.)
2. **비공개 보안 취약점 신고 활성화 (`Settings → Code security`)**
   - **`Private vulnerability reporting`** 활성화 시 `.github/SECURITY.md` 및 이슈 템플릿의 비공개 취약점 접수 링크(`/security/advisories/new`)가 작동합니다.
3. **Issues 탭 활성화 (`Settings → General → Features → Issues`, 선택)**
   - 활성화 시 `.github/ISSUE_TEMPLATE/`에 포함된 Cask 설치 오류 제보·새 버전 요청 서식과 보안 취약점 비공개 접수 안내가 적용됩니다.

## GitHub Actions 비용 안내 (공개 저장소 무료)

- **공개(Public) 저장소 무료 제공:** GitHub 정책상 공개 저장소(`eGovFramework/homebrew-egovframe`)에서 실행되는 표준 GitHub 호스팅 러너(`ubuntu-latest`, `macos-latest`)는 **시간·분(Minutes) 제한 없이 100% 무료**이며 별도의 비용이 청구되지 않습니다.
- **스토리지(Storage) 과금 없음:** 새 버전 감지 시 DMG 파일은 러너에서 스트리밍으로 SHA-256 해시만 계산하고 아티팩트(Artifact)나 Release 첨부파일로 업로드하지 않으므로 GitHub Actions 스토리지 용량도 소비하지 않습니다. (Release는 공식 배포 서버 URL만 안내합니다.)
- **비공개(Private) 저장소 복제 시 참고:** 만약 저장소를 비공개(Private)로 전환하거나 비공개로 복제해 사용하는 경우에만 계정/조직의 무료 제공 분(Minutes)에서 차감되며, 이때 `macos-latest` 러너는 Linux 대비 10배 분 차감율이 적용됩니다.
