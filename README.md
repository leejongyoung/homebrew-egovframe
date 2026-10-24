# homebrew-egovframe

<!-- latest-badge:start -->
[![eGovFrame 5.0.2](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/5.0.2/flat.svg)](https://www.egovframe.go.kr/)
<!-- latest-badge:end -->
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[한국어](README.ko.md)

<!-- work-only:start -->
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)

> This fork tracks [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). To install from this fork, replace `egovframework/egovframe` with `leejongyoung/egovframe` in the commands below. Maintainer documentation: [Maintenance](.github/MAINTENANCE.md).
<!-- work-only:end -->

## About

Homebrew casks for the macOS eGovFrame development environment (IDE). Downloads come from the official eGovFrame server.

- [eGovFrame website](https://www.egovframe.go.kr/)
- [Development environment downloads](https://www.egovframe.go.kr/home/sub.do?menuNo=40)

## Installation

### Add the official tap

Install [Homebrew](https://brew.sh/) first, then add this tap once:

```bash
brew tap egovframework/egovframe
```

### Install the latest release

```bash
brew install --cask egovframework/egovframe/egovframedev-latest
```

The latest cask in this tap is named `egovframedev-latest`. Use that name explicitly rather than treating a versioned cask as having an optional version suffix.

### Install a specific version

Choose one of the available casks:

```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

These commands assume the official tap above. If another tap provides the same cask name, use the fully qualified form `egovframework/egovframe/egovframedev@<version>` with your chosen version.

### Update the latest cask

```bash
brew update
brew upgrade --cask egovframework/egovframe/egovframedev-latest
```

## Architectures and application paths

- The listed casks other than 3.10.0 and 4.0.0 provide Apple Silicon (ARM64) and Intel (x86_64) downloads; Homebrew selects the matching architecture.
- Versions 3.10.0 and 4.0.0 provide Intel (x86_64) downloads only, not native Apple Silicon builds.
- Applications are installed under `/Applications/`:
  - 3.10.0 and 4.0.0: `eGovFrameDev-X.X.X-Mac-64bit.app`
  - Dual-architecture casks using the older `Mac` naming: `eGovFrameDev-X.X.X-Mac-AArch64.app` or `eGovFrameDev-X.X.X-Mac-x86_64.app`
  - Dual-architecture casks using the newer `macOS` naming: `eGovFrameDev-X.X.X-macOS-AArch64.app` or `eGovFrameDev-X.X.X-macOS-x86_64.app`

## License

See [LICENSE](LICENSE). eGovFrame names and logos belong to their respective owners.
