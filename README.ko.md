# homebrew-egovframe

<!-- latest-badge:start -->
[![전자정부표준프레임워크 5.0.2](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/5.0.2/flat-ko.svg)](https://www.egovframe.go.kr/)
<!-- latest-badge:end -->
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

> 이 저장소는 공식 [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe)를 추적합니다. 이 저장소에서 설치하려면 아래 단계의 `egovframework/egovframe` 대신 `leejongyoung/egovframe`를 tap 하세요. [유지 관리](#유지-관리)를 참고하세요.

## 소개

이곳은 eGovFrame의 Homebrew Tap(3rd party repository)입니다. 여기에는 eGovFrame의 통합 개발 환경(IDE)용 Cask들이 포함되어 있습니다.

## eGovFrame에 대하여

- 이름: egovframe
- 설명: eGovFrame은 대한민국 정부에서 제공하는 오픈 소스 프레임워크입니다. 이는 웹 기반 공공 서비스 개발을 위해 설계되었습니다. 정부 표준 개발 플랫폼으로서, eGovFrame은 공공 부문 IT 프로젝트에 중요한 역할을 합니다. 전 세계의 사용자가 사용할 수 있도록 공개되어 있습니다.
- 홈페이지: [eGovFrame 공식 웹사이트](https://www.egovframe.go.kr/)

## 사용 방법

eGovFrame IDE의 최신 버전을 설치하려면:

```bash
brew install egovframedev
```

특정 버전의 eGovFrame IDE를 설치하려면 다음 단계를 따르세요:

1. eGovFrame 저장소를 Homebrew에 추가합니다(최초 1회):

```bash
brew tap egovframework/egovframe
```

1. 최신 버전의 eGovFrame IDE를 설치합니다:

Apple Silicon ARM64 및 Intel/AMD x64 바이너리가 모두 제공됩니다.

```bash
brew install egovframedev-latest
```

1. 원하는 버전의 eGovFrame IDE를 설치합니다:
  4.0 및 v3.10은 Intel/AMD x64 바이너리만 제공됩니다.

```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

버전을 지정하는 것은 선택사항입니다. 생략하면 최신 버전이 설치됩니다.

## 앱 설치 경로

`/Applications/` 디렉토리(응용 프로그램 디렉토리) 아래에 설치되며, 다음 형식의 앱 이름으로 확인 가능합니다 (X.X.X는 버전을 의미합니다).

- 4.3.1 이하 버전: `eGovFrameDev-X.X.X-Mac-AArch64.app` 또는 `eGovFrameDev-X.X.X-Mac-x86_64.app`
- 5.0.0 이상 버전: `eGovFrameDev-X.X.X-macOS-AArch64.app` 또는 `eGovFrameDev-X.X.X-macOS-x86_64.app`

## 유지 관리

- `main`은 upstream `eGovFramework/homebrew-egovframe`와 똑같이 유지합니다. 매일 실행되는 워크플로([`sync-upstream.yml`](.github/workflows/sync-upstream.yml))가 fast-forward하고, `work`가 뒤처지면 `work`로 들어가는 풀 리퀘스트를 엽니다.
- `work`(기본 브랜치)에는 이 저장소만의 변경(CI, 자동화, README 배지)을 둡니다.
- 매일 실행되는 워크플로([`update-casks.yml`](.github/workflows/update-casks.yml))가 [egovframe.go.kr](https://www.egovframe.go.kr/home/sub.do?menuNo=40)의 릴리스 목록(Cask `livecheck`과 같은 페이지)을 읽습니다. `egovframedev-latest`보다 새롭고 두 아키텍처의 macOS DMG가 모두 있는 릴리스가 있으면 DMG를 내려받아 SHA-256을 계산하고, `Casks/egovframedev@X.Y.Z.rb`를 추가하고, 같은 X.Y 계열의 이전 패치 Cask를 지우고, `egovframedev-latest`·위의 설치 목록·배지를 갱신한 뒤 `brew style`을 통과하면 풀 리퀘스트를 엽니다. 자동으로 머지하지는 않습니다.
- 직접 실행: `python3 scripts/update_casks.py --dry-run`(감지만) 또는 `python3 scripts/update_casks.py`. 테스트: `python3 -m unittest discover -s tests -v`.

