# Guía de contribución

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/flat.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](CONTRIBUTING.fr.md)

<!-- work-only:start -->
## Ramas

| Rama | Propósito |
| --- | --- |
| `main` | Espejo exacto de [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). Se sincroniza a diario; nunca hagas commits aquí. |
| `work` | Rama predeterminada. Cambios propios de este fork: CI, automatización, documentación y correcciones de casks. Abre los pull requests contra ella. |
| `upstream-submit` | Commit listo para el repositorio oficial, basado en su `main`; se actualiza automáticamente cuando pasa el CI de `work` y no hay ningún PR abierto hacia el repositorio oficial. |
| `upstream-submit-*` | Instantáneas desechables creadas por `scripts/open_upstream_pr.sh`; independientes de la rama de envío fija. |

`main` es un espejo del repositorio oficial, así que no hagas commits directamente en ella. Envía los cambios a la rama predeterminada, `work`.

Detalles operativos, calendarios y regeneración de Releases anteriores: [MAINTENANCE.md](../../.github/MAINTENANCE.md).
<!-- work-only:end -->

## Antes de abrir un pull request

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # pruebas de los scripts
brew style leejongyoung/egovframe/egovframedev-latest   # requiere el tap: brew tap leejongyoung/egovframe
```

El CI (`ci.yml`) ejecuta las pruebas y además `scripts/check_tap.sh` (`brew readall`, `brew style` y `brew audit`). Ejecuta los comandos desde la raíz del repositorio; las pruebas de los scripts necesitan PyYAML, que el CI instala del mismo modo.

- Los mensajes de commit siguen el estilo que ya se usa en el repositorio oficial: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- No edites a mano el SHA-256 de un cask. Las versiones nuevas salen de `scripts/update_casks.py` (el flujo de trabajo `Update casks`); para volver a comprobar un hash existente ejecuta `gh workflow run update-casks.yml -f verify=<version>`.
- Un cask por serie menor: al añadir `5.0.3` se elimina `5.0.2` (misma convención que en el repositorio oficial).

## GitHub Actions y facturación

- **Gratis en repositorios públicos:** según la política de facturación de GitHub, los runners estándar alojados por GitHub (`ubuntu-latest`, `macos-latest`) son **gratuitos y sin límite de minutos en repositorios públicos**. Los DMG se procesan para calcular su hash en flujo durante `update-casks.yml` y nunca se suben como artefactos de Actions ni como recursos de Release, por lo que tampoco se consume cuota de almacenamiento de Actions.
- Los minutos solo se descuentan de la cuota gratuita de tu cuenta si copias el repositorio a uno privado y lo ejecutas allí.

<!-- work-only:start -->
## Enviar cambios al repositorio oficial

Usa el script en lugar de empujar `work` directamente. Crea un único commit limpio sobre la rama del repositorio oficial a partir de las diferencias entre este y `work`, y deja fuera los archivos exclusivos del fork (`.github/MAINTENANCE.md`, `.github/UPSTREAM_PR.md`, `.github/workflows/sync-upstream.yml`, `scripts/open_upstream_pr.sh`, `tests/test_open_upstream_pr.py` y los bloques marcados como `work-only`):

```bash
scripts/open_upstream_pr.sh --dry-run                        # qué se enviaría
scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
```
<!-- work-only:end -->

## Seguridad

No notifiques vulnerabilidades en issues; sigue el proceso descrito en [SECURITY.es.md](../security/SECURITY.es.md).
