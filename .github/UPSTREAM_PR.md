# fix: modernize cask macOS requirements and installation guides

## Summary

Update the macOS dependency declarations in the seven existing casks to match current Homebrew's `Homebrew/OSDependsOn` rules:

- Replace `depends_on macos: ">= :big_sur"` with `depends_on :macos` in `egovframedev-latest`, `egovframedev@4.3.1` and `egovframedev@5.0.2`.
- Add `depends_on :macos` to `egovframedev@3.10.0`, `egovframedev@4.0.0`, `egovframedev@4.1.1` and `egovframedev@4.2.1`.

The string-comparison form is deprecated in current Homebrew. Its style autocorrection also considers the Big Sur minimum redundant and recommends the explicit macOS-only declaration.

Refresh the shared English and Korean READMEs:

- Include the reusable eGovFrame version badge and Apache-2.0 license badge.
- Document the official tap and the explicit `egovframedev-latest` cask, with fully qualified install/upgrade commands.
- Keep the available version list and clarify architecture support and application paths, including the Intel-only `Mac-64bit` names for 3.10.0 and 4.0.0.
- Link the two language versions to each other.

This is a single commit based on upstream `main`. Cask versions, download URLs, SHA-256 values, application paths and installation/postflight commands are unchanged. The public installation documentation and shared badges are included; fork-specific CI, automation, maintenance documents, personal tap instructions and scripts are not.

## Validation

Checked the exact submission snapshot in an isolated local tap using Homebrew `7.0.10-65-g786fc9e`:

- `brew readall --aliases --os=all --arch=all`: passed across the tap; emits the existing `postflight` deprecation warning described below.
- `brew style --only-cops=Homebrew/OSDependsOn`: passed across the tap, with no offenses.
- Full `brew style`: passed for the six casks other than `egovframedev@4.2.1`.
- `brew audit --cask --except=installed`: passed for all seven casks.
- The submission contains seven cask files and both READMEs; README preparation preserves public content and shared badges while excluding fork-only blocks.

## Existing limitation outside this change

`egovframedev@4.2.1` has a pre-existing `postflight` block that current Homebrew's `Cask/InstallSteps` cop asks to migrate to `postflight_steps`. This PR intentionally leaves the installation steps unchanged. Full style compliance for that cask requires a separate change with installation verification.

A full IDE install/uninstall is not part of this dependency-declaration change's verification.
