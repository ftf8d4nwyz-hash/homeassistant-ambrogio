# home-assistant-config

Config et documentation de la maison (Burtoncourt, 57) pour Home Assistant,
pensée pour être exploitée par **Claude** via MCP.

## Pourquoi ce dossier ?
Donner à Claude une **source de vérité versionnée** (pièces, conventions, règles)
pour qu'il génère des automatisations cohérentes et évite de casser les entités.

## Contenu
- **`CLAUDE.md`** — contexte + règles lues automatiquement par Claude.
- `automations/`, `scripts/`, `scenes/`, `packages/`, `dashboards/`, `blueprints/`
  — exports YAML de HA à déposer au fur et à mesure.

## Comment alimenter
1. Depuis HA, exporte les YAML (automatisations, dashboards) dans les dossiers.
2. Commit. Claude lira `CLAUDE.md` + les YAML pour proposer des changements.

## Repos GitHub utiles (Claude + HA)

| Dépôt | Lien |
|---|---|
| voska/hass-mcp | https://github.com/voska/hass-mcp |
| modelcontextprotocol/servers | https://github.com/modelcontextprotocol/servers |
| modelcontextprotocol/python-sdk | https://github.com/modelcontextprotocol/python-sdk |
| home-assistant/core | https://github.com/home-assistant/core |
| frenck/awesome-home-assistant | https://github.com/frenck/awesome-home-assistant |
| home-assistant/example-configs | https://github.com/home-assistant/example-configs |
| hacs/integration | https://github.com/hacs/integration |
| thomasloven/hass-config | https://github.com/thomasloven/hass-config |
| custom-cards/button-card | https://github.com/custom-cards/button-card |
| RomRider/apexcharts-card | https://github.com/RomRider/apexcharts-card |
| thomasloven/lovelace-card-mod | https://github.com/thomasloven/lovelace-card-mod |
