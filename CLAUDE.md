# CLAUDE.md

Intégration personnalisée Home Assistant pour les robots tondeuses Ambrogio
(`custom_components/ambrogio_robot`), distribuée via HACS.

## Commandes utiles

- `scripts/setup` — prépare l'environnement : paquets système (bluez), copie de `configuration-template.yaml` vers `configuration.yaml` si absent, puis `requirements_dev.txt` ou `requirements.txt` selon `BUILD_TYPE` (`dev` / `run`)
- `scripts/develop` — lance Home Assistant en debug sur la racine du dépôt (`hass -c . --debug`)
- `scripts/lint` — `ruff check . --fix` (configuration dans `.ruff.toml`)
- `pytest` — tests (basés sur `pytest-homeassistant-custom-component`, fixtures dans `tests/fixtures/`)

## Bibliothèque de prompts

Les prompts Claude Code réutilisables sont enregistrés dans
[`.claude/prompts/prompt-library.md`](.claude/prompts/prompt-library.md) :
classés par phase (découvrir / concevoir / construire / livrer / exploiter),
avec un exemple rempli pour chacun et une section finale adaptée à ce dépôt.
Consulte ce fichier quand une demande correspond à un de ces cas d'usage.
