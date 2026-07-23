# CLAUDE.md — Contexte Home Assistant de la Maison

> Fichier lu automatiquement par Claude Code / Claude quand il travaille sur cette
> configuration. Il décrit **ma maison, mes conventions et mes règles**.
> But : que Claude génère des automatisations et des réponses cohérentes avec
> l'existant, sans casser les entités.

## 🏠 La maison

- **Localisation** : Burtoncourt, Lorraine (57), France
- **Fuseau / langue** : `Europe/Paris` / `fr`
- **Version HA** : 2026.7.x
- **Occupants (personnes)** :
  - `person.faure` → Bruno
  - `person.maryline` → Maryline
  - Enfant : Daphné (chambre + Vélux + clim dédiés)
- **Zones** : `Maison`, `Zone maison Burtoncourt`

## 🧭 Étages et pièces (source de vérité : registre HA)

### Rez-de-chaussée (`floor: rez_de_chaussee`, niveau 0)
- Extérieure devant · Chambre rez-de-chaussée · Couloir · Piscine · Garage
- Salle de bain rez de chaussée · Pièce chaudière

### 1er étage (`floor: 1er_etage`, niveau 1)
- Salon · Cuisine · Cinéma · Dressing · Salle de bain

### Pièces sans étage assigné (à ranger un jour)
- Chambre · Billiard · Séjour · Extérieures arrière · Escalier · Escalier 1ere étage · Dashboard

> ⚠️ Plusieurs pièces ne sont pas rattachées à un étage. Si tu crées des
> automatisations « par étage », vérifie d'abord le `floor_id` réel.

## 🔌 Équipements marquants

| Domaine | Matériel / notes |
|---|---|
| Aspirateur | Roborock S7 MaxV (`vacuum.roborock_s7_maxv`) — cartes : Salon, Bas, Billard |
| Caméras | Reolink (Porte d'entrée, Terrasse, Jardin, Garage), Box Reolink, Hub Reolink |
| Volets / Vélux | Somfy via **ESPSomfy RTS**, Vélux (cuisine, chambre, Daphné), volets cinéma/dressing/billard/amis |
| Éclairage | Hue + **Adaptive Lighting** (par pièce : billard, cuisine, dressing, 1er étage…) |
| Chauffage / clim | `climate.*` : Thermostat, Chambre, Chambre Daphné, Clim salon, Clim cinéma |
| Sécurité | **Alarmo** (`alarm_control_panel.alarmo`), sirènes Reolink, détecteurs de présence |
| Piscine | Filtration auto, déshumidificateur, capteur température |
| Réseau / box | Freebox v9, Home Assistant Cloud (Nabu Casa) |
| Assistants vocaux | Echo Dot, Google AI (Conversation/TTS/STT/Task), Piper, HA Cloud TTS |

## 📛 Conventions de nommage (IMPORTANT)

- Les **automatisations et scripts sont préfixés d'un emoji** décrivant le thème :
  - 🐕 / 🐶 = mode chien · 🛡️ / 🛑 = sécurité · 🔄 = reprise/reset
  - ☀️ / 🔥 = canicule · 🪟 = volets · ❤️ = ambiance · 🏠 = récap maison
  - **Respecte ce style** quand tu crées une nouvelle automatisation.
- Beaucoup d'entités ont des noms français avec accents et espaces. **Ne renomme
  jamais un `entity_id`** sans vérifier qui le consomme (automatisations, scripts,
  dashboards).
- Helpers d'override d'éclairage par pièce (pattern répété) :
  `input_number.override_luminosite_<piece>`, `input_number.override_couleur_<piece>`,
  `input_datetime.override_manuelle_<piece>` (billard, cuisine, dressing).

## ✅ Règles pour Claude (à respecter)

1. **`entity_id` plutôt que `device_id`** dans les triggers/conditions/actions.
2. Préférer les **helpers natifs** (input_boolean, input_number, timer…) et les
   conditions natives **plutôt que des templates Jinja2** quand c'est possible.
3. **Ne pas éditer `.storage` ni générer du YAML à coller à la main** : utiliser les
   outils HA (services / config) ou proposer un fichier de package clair.
4. Choisir le bon **mode d'automatisation** (`single` / `restart` / `queued` / `parallel`).
5. Avant de modifier une automatisation existante, **la lire d'abord** et conserver
   le style (emoji, langue FR).
6. Pour les boutons/télécommandes Zigbee, utiliser les **triggers `event`**
   (`event.interrupteur_*`, `event.porte_d_entree_sonnette`).
7. Toujours vérifier les entités **`unavailable`** avant de s'appuyer dessus
   (beaucoup de capteurs Reolink/Zigbee passent indispo).

## 🧩 Intégrations custom (HACS) présentes

Adaptive Lighting · ESPSomfy RTS · Alarmo · Roborock · Reolink · Battery Notes ·
Flightradar24 · Browser Mod · card-mod · button-card · apexcharts-card · EPG · Freebox.

## 📂 Organisation de ce dossier

```
home-assistant-config/
├── CLAUDE.md            ← ce fichier (contexte pour l'IA)
├── README.md            ← quoi / pourquoi
├── automations/         ← automatisations exportées (YAML)
├── scripts/             ← scripts
├── scenes/              ← scènes
├── packages/            ← packages HA (regroupe helpers+auto+scripts par thème)
├── dashboards/          ← dashboards Lovelace (YAML)
└── blueprints/          ← blueprints réutilisables
```

> Ce dossier est une **mémoire versionnée** : y déposer les exports YAML de HA
> permet à Claude de raisonner sur l'existant et de proposer des changements sûrs.
