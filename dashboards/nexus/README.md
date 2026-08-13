# NEXUS — Poste de pilotage (Home Assistant)

Dashboard déployé : **NEXUS** → `/dashboard-nexus` (entrée dédiée dans la
barre latérale, icône `mdi:space-station`).

- `nexus_transform.py` — source de vérité. C'est le corps exact passé en
  `python_transform` à `ha_config_set_dashboard` : il définit les tokens
  de style une seule fois et génère les 4 vues par boucles.
- `nexus.lovelace.json` — config générée, telle que déployée (~237 Ko).

Régénérer / vérifier hors-ligne :

```bash
python3 -c "
import json; g={}; l={'config':{'views':[]}}
exec(open('nexus_transform.py').read(), g, l)
json.dump(l['config'], open('nexus.lovelace.json','w'), ensure_ascii=False, indent=1)"
```

> Le `exec` avec `globals`/`locals` séparés n'est pas un détail : c'est
> exactement ainsi que le bac à sable HA évalue le transform. Les fonctions
> n'y voient pas les noms du module — d'où les `lambda ..., _H=HUD:` qui
> capturent les constantes en argument par défaut. Un `def` classique
> échoue avec `NameError`.

---

## Les 4 ponts

| Vue | Accent | Contenu |
|-----|--------|---------|
| **Passerelle** | cyan `#00E5FF` | Hublot étoilé, indicateurs primaires, télémétrie texte, commandes rapides, secteurs éclairés, support-vie, soutes |
| **Réacteur** | ambre `#FFB020` | Flux 24 h, jauge radar, cycles 7 jours, paramètres |
| **Modules** | violet `#8B5CF6` | Modules d'habitation, sas & hublots, régulation thermique, ambiances |
| **Boucliers** | turquoise `#14F1D9` | Alarme, détecteurs de proximité, optiques externes, journal de bord |

## Palette

| Rôle | Hex |
|------|-----|
| Vide / coque | `#02040A` → `#0A1020` |
| HUD cyan | `#00E5FF` |
| Plasma turquoise | `#14F1D9` |
| Alerte ambre | `#FFB020` |
| Alarme rouge | `#FF3B5C` |
| Fusion magenta | `#FF2FB9` |
| Xénon violet | `#8B5CF6` |
| Texte | `#DFF6FF` · secondaire `#6C89A8` |

## Effets

| Effet | Mise en œuvre |
|-------|---------------|
| **Crochets d'angle HUD** | `ha-card::before`, 8 `linear-gradient` positionnés dans les 4 coins — pas d'image, pas de SVG |
| **Balayage scanline** | `ha-card::after`, bande lumineuse qui descend en boucle (`nxScan`, 6,5 s), décalée par carte |
| **Trame CRT** | `repeating-linear-gradient` 3 px dans le fond de chaque carte |
| **Séquence d'allumage** | `nxBoot` — surexposition + `scaleY` qui se résorbe, retard échelonné par carte |
| **Champ d'étoiles** | 52 `radial-gradient` générés par un LCG déterministe ; 30 fixes en fond du hublot, 22 sur une couche `::before` en dérive lente (`nxDrift`, 140 s) |
| **Radar** | `conic-gradient` en rotation derrière la jauge de charge (`nxRadar`, 3,8 s) |
| **Alerte pulsante** | Les détecteurs passent en rouge et pulsent (`nxAlert`) quand l'entité est `on` — template card-mod sur `config.entity` |
| **Halo néon** | `drop-shadow` sur les icônes, les courbes ApexCharts (`#graph`) et les titres |
| **Chips angulaires** | `clip-path: polygon(...)` sur la navigation — coins biseautés, pas d'arrondi |
| **Typographie** | Monospace système, majuscules, `letter-spacing` 0,14–0,28 em |

## Télémétrie

Carte markdown en bloc de code : jauge en caractères pleins (`▓▓▓▓░░░░░`),
lignes alignées au `format` Jinja. Aucune dépendance — juste du texte
monospace qui se met à jour en temps réel.

## Ce qui reste vrai

- **La barre de navigation ne rétrécit pas en largeur.** Les vues
  `sections` ne permettent pas à une section de changer de `column_span`
  selon un état. La bascule libellés ↔ icônes est l'équivalent honnête.
- **Les squelettes ne sont pas des états de chargement.** HA pousse l'état
  par websocket. Le squelette couvre le cas réel : entité indisponible.
- **Tout repose sur card-mod**, qui cible le shadow DOM du frontend :
  crochets d'angle, scanlines et halos sont à revérifier après chaque
  montée de version majeure de HA. `configuration.yaml` n'est pas touché.
- **Coût de rendu.** Une soixantaine de cartes portent chacune deux
  pseudo-éléments animés. C'est fluide sur un poste récent ; sur une
  tablette murale d'entrée de gamme, prévoir de désactiver les scanlines
  (supprimer le bloc `ha-card::after` de `HUD`).
