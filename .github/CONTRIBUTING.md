# Contributing / 기여 안내

## Before you open a pull request / PR 전에

```bash
python3 -m unittest discover -s tests -v   # script tests
brew style egovframework/egovframe/egovframedev-latest   # needs the tap: brew tap egovframework/egovframe
```

CI (`ci.yml`) runs the tests plus `scripts/check_tap.sh` (`brew readall`, `brew style` and `brew audit`).

- Commit messages follow the style already used upstream: `feat(casks): add egovframedev@X.Y.Z`,
  `fix(casks): …`, `docs(readme): …`, `ci: …`.
- Do not edit the SHA-256 of a cask by hand. New versions come from `scripts/update_casks.py`
  (the `Update casks` workflow); to re-check an existing hash run `gh workflow run update-casks.yml -f verify=<version>`.
- One cask per minor series: when `5.0.3` is added, `5.0.2` is removed (same convention as upstream).

## GitHub Actions & Billing / Actions 비용 안내

- **Free on public repositories / 공개 저장소 무료:** Standard GitHub-hosted runners (`ubuntu-latest`, `macos-latest`) are **free without minute limits on public repositories** under GitHub's billing policy. DMGs are hashed in-stream during `update-casks.yml` and are never uploaded as Actions artifacts or Release assets, so no Actions storage quota is consumed either.
- **공개(Public) 저장소에서는 `ubuntu-latest`, `macos-latest` 러너 모두 무료(무제한)로 제공되어 비용이 청구되지 않습니다.** DMG 파일도 해시 계산 후 아티팩트로 저장하지 않으므로 스토리지 비용이 발생하지 않습니다. (단, 비공개 저장소로 복제해 실행하는 경우에만 계정의 무료 제공 분에서 차감됩니다.)

## Security / 보안

Do not report vulnerabilities in issues; see [SECURITY.md](SECURITY.md).
취약점은 이슈가 아니라 [SECURITY.md](SECURITY.md) 절차로 알려 주세요.
