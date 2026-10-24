# homebrew-egovframe

<!-- latest-badge:start -->
[![eGovFrame 5.0.2](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/5.0.2/flat.svg)](https://www.egovframe.go.kr/)
<!-- latest-badge:end -->
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

> This repository tracks the official [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). To install from it, tap `leejongyoung/egovframe` instead of `egovframework/egovframe` in the steps below. See [Maintenance](#maintenance).

## Introduction
Welcome to eGovFrame's Homebrew Tap, an external repository for Homebrew. This Tap is dedicated to hosting Casks for eGovFrame's Integrated Development Environment (IDE).

## About eGovFrame
- Name: eGovFrame
- Description: eGovFrame is an open-source framework provided by the government of South Korea. It is designed for the development of web-based public services. As a government-standardized development platform, eGovFrame plays a crucial role in IT projects within the public sector in Korea. Its global availability allows it to be utilized by users worldwide.
- Homepage: [eGovFrame Official Website](https://www.egovframe.go.kr/)

## Installation Guide

### For the Latest Version of eGovFrame IDE:

Simply run the following command in your terminal:

```bash
brew install egovframedev
```

### For Specific Versions of eGovFrame IDE:

1. Tap into the eGovFrame's repository(only for the first time):

```bash
brew tap egovframework/egovframe
```

2. Install the latest version of eGovFrame IDE:

Both Apple Silicon ARM64 & Intel/AMD x64 binaries are provided.

```bash
brew install egovframedev-latest
```

3. Install the desired version of eGovFrame IDE:

v4.0 & v3.10 are provided as Intel/AMD x64 binaries only.
   
```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

Please note that specifying the version is optional. If omitted, the latest version will be installed.

### Application Installation Path

The application is installed under the `/Applications/` directory, and you can verify it with an app name in the following format (X.X.X represents the version number).

* Version 4.3.1 or earlier: `eGovFrameDev-X.X.X-Mac-AArch64.app` or `eGovFrameDev-X.X.X-Mac-x86_64.app`
* Version 5.0.0 or later: `eGovFrameDev-X.X.X-macOS-AArch64.app` or `eGovFrameDev-X.X.X-macOS-x86_64.app`

## Maintenance

- `main` mirrors upstream `eGovFramework/homebrew-egovframe` exactly. A daily workflow ([`sync-upstream.yml`](.github/workflows/sync-upstream.yml)) fast-forwards it and opens a pull request into `work` when `work` is behind.
- `work` (the default branch) holds this repository's own changes: CI, automation and the README badges.
- A daily workflow ([`update-casks.yml`](.github/workflows/update-casks.yml)) reads the release list on [egovframe.go.kr](https://www.egovframe.go.kr/home/sub.do?menuNo=40) (the same page the casks' `livecheck` uses). For a release newer than `egovframedev-latest` whose macOS DMGs exist for both architectures, it downloads them, computes SHA-256, adds `Casks/egovframedev@X.Y.Z.rb`, removes older patch casks of the same X.Y series, updates `egovframedev-latest`, the install list above and the badge, runs `brew style`, and opens a pull request. Nothing is merged automatically.
- Run it by hand: `python3 scripts/update_casks.py --dry-run` (detect only) or `python3 scripts/update_casks.py`. Tests: `python3 -m unittest discover -s tests -v`.
