# Matrix History Card

Carte Lovelace personnalisée pour Home Assistant : un **journal écrit animé
« style Matrix »** (pluie de code verte, effet terminal CRT, lueur) qui liste
les derniers évènements importants de la maison, avec pour chaque appareil ses
informations associées (coût €, énergie kWh).

Elle lit l'historique via le **logbook** de Home Assistant
(`logbook/get_events`). Si le logbook n'est pas disponible, elle se rabat
automatiquement sur le `last_changed` des entités configurées.

![style](https://img.shields.io/badge/style-matrix-00ff41)

## Installation

### Option A — Ressource inline (déjà déployée)
La carte a été enregistrée comme ressource *inline* directement dans Home
Assistant (aucun fichier à copier). Rien à faire.

### Option B — Fichier local
1. Copier `matrix-history-card.js` dans `/config/www/`.
2. Réglages → Tableaux de bord → menu ⋮ → **Ressources** →
   **Ajouter une ressource** :
   - URL : `/local/matrix-history-card.js`
   - Type : `Module JavaScript`
3. Vider le cache du navigateur (Ctrl+Maj+R).

## Configuration

```yaml
type: custom:matrix-history-card
title: "MAISON // JOURNAL"
count: 12          # nombre de lignes du journal
hours: 96          # profondeur d'historique (heures)
entities:          # entités suivies dans le journal
  - binary_sensor.machine_a_laver_lave_linge_termine
  - binary_sensor.seche_linge_en_marche
  - binary_sensor.voiture_en_charge
  - vacuum.roborock_s7_maxv
  - person.faure
  - alarm_control_panel.alarmo
context:           # infos ajoutées en fin de ligne pour une entité
  binary_sensor.seche_linge_en_marche:
    - { entity: sensor.cout_seche_linge, label: "coût", unit: "EUR" }
    - { entity: sensor.seche_linge_energie, label: "énergie" }
stats:             # bandeau de valeurs "live" en bas de carte
  - { entity: sensor.cout_prise_garage, label: "Coût garage" }
```

### Options

| Option | Type | Défaut | Description |
|--------|------|--------|-------------|
| `title` | string | `SYSTEME // JOURNAL` | Titre affiché en tête |
| `count` | number | `12` | Nombre d'évènements affichés |
| `hours` | number | `96` | Fenêtre d'historique en heures |
| `scroll` | bool | `true` | Fait défiler chaque ligne horizontalement (marquee) si elle dépasse |
| `direction` | string | `ltr` | Sens du défilement : `ltr` (gauche→droite) ou `rtl` (droite→gauche) |
| `speed` | number | `28` | Vitesse en pixels/seconde — plus petit = plus lent |
| `entities` | list | `[]` | Entités suivies dans le logbook |
| `context` | map | `{}` | `entity_id` → liste `{entity, label, unit}` d'infos ajoutées à la ligne |
| `stats` | list | `[]` | Cartouches de valeurs live `{entity, label, unit}` |

> Astuce : `unit: "EUR"` est automatiquement affiché `€`. Sans `unit`, la carte
> utilise `unit_of_measurement` de l'entité.

## Notes

- Le journal se rafraîchit au maximum toutes les 60 s (le bandeau `stats` et
  l'horloge sont mis à jour en temps réel).
- L'animation de fond est volontairement limitée (~18 fps) pour rester légère.
- Aucun capteur d'eau (litres/m³) n'est requis ; il apparaîtra dans `context`
  ou `stats` dès qu'un tel capteur existe.
