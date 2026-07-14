# 🐕 Mode Chien — chien seul à la maison

Documentation du pack d'automatisations créé directement dans Home Assistant
(via l'API de configuration) pour s'occuper du chien quand personne n'est à la
maison en journée. Un onglet **CHIEN** a été ajouté au tableau de bord **Demo**
(`/dashboard-demo/chien`) avec le bouton d'activation.

## Entités créées

| Entité | Rôle |
|--------|------|
| `input_boolean.mode_chien` | Interrupteur maître « 🐕 Mode Chien » (le bouton du dashboard Demo) |
| `script.chien_musique_relaxante` | Volume Echo Dot à 40 % puis musique relaxante pour chiens (Alexa Media Player, commande `custom`) |
| `script.chien_stop_musique` | Coupe la musique sur l'Echo Dot |

## Automatisations

Toutes conditionnées par `input_boolean.mode_chien` = `on`. La présence est
mesurée par le compteur de personnes de `zone.home` (robuste face à la zone
personnalisée « Zone maison Burtoncourt »).

### 1. `automation.chien_seul_depart_de_la_maison`
- **Déclencheur** : `zone.home` passe sous 1 personne pendant 3 min (anti-rebond GPS).
- **Conditions** : Mode Chien actif, entre 06:00 et 21:00.
- **Actions** : musique relaxante sur l'Echo Dot ; si le salon dépasse 26 °C,
  clim salon en `cool` à 24 °C ; notification sur les deux iPhones.

### 2. `automation.chien_seul_confort_temperature`
- **Déclencheur** : température courante de `climate.salon` > 27 °C pendant 10 min.
- **Conditions** : Mode Chien actif, personne à la maison.
- **Actions** : clim salon à 24 °C + notification.

### 3. `automation.chien_seul_point_de_midi`
- **Déclencheur** : tous les jours à 13:00.
- **Conditions** : Mode Chien actif, personne à la maison.
- **Actions** : notification aux deux iPhones avec la température du salon et
  une photo de `camera.camera_jardin_fluide`.

### 4. `automation.chien_seul_retour_a_la_maison`
- **Déclencheur** : `zone.home` repasse au-dessus de 0 personne.
- **Conditions** : Mode Chien actif.
- **Actions** : coupe la musique de l'Echo Dot si elle joue encore.

## Onglet dashboard « CHIEN » (Demo)

Vue `sections` avec :
- le bouton bascule **Mode Chien** (tuile ambre pleine largeur) + explication ;
- boutons **Lancer la musique** / **Stop musique** + tuile Echo Dot avec volume ;
- surveillance : personnes (Faure, Maryline) et clim salon ;
- tuiles des 4 automatisations pour les activer/désactiver individuellement.

## Utilisation

1. Ouvrir le tableau de bord **Demo** → onglet **CHIEN**.
2. Activer **Mode Chien** le matin quand le chien reste seul.
3. Tout est ensuite automatique ; la musique se coupe au retour.
4. Le mode reste actif tant qu'il n'est pas désactivé manuellement.
