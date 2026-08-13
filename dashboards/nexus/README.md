# NEXUS — Blueprint dashboard premium (Home Assistant)

Dashboard déployé sur l'instance HA : **NEXUS** → `/dashboard-nexus`
(entrée dédiée dans la barre latérale, icône `mdi:hexagon-multiple-outline`).

- `build_nexus.py` — générateur de la config Lovelace (source de vérité).
- `nexus.lovelace.json` — config générée, telle que déployée.

Régénérer : `python3 build_nexus.py > nexus.lovelace.json`

---

## 1. Le blueprint 30 minutes

**Séquence de build** (ordre imposé — chaque étape débloque la suivante) :

| # | Étape | Durée | Pourquoi à ce moment |
|---|-------|-------|----------------------|
| 1 | Inventaire des entités réelles | 5 min | Un dashboard premium se casse sur un `entity not found`. Tout est vérifié avant la première carte. |
| 2 | Tokens de design (couleurs, rayons, ombres, easing) | 3 min | Figés une fois, réutilisés partout — c'est ce qui produit la cohérence. |
| 3 | Squelette de navigation + 4 vues vides | 4 min | La structure d'abord, le contenu ensuite. |
| 4 | Vue Accueil (hero + KPI + actions) | 8 min | La vue qui fait 90 % de l'impression. |
| 5 | Vue Énergie (charts animés) | 6 min | Le morceau « waouh », isolé pour ne pas alourdir l'accueil. |
| 6 | Vues Maison / Sécurité | 4 min | Densité utile, styling minimal assumé. |

**Layout** — vues `sections`, grille 12 colonnes, `max_columns: 4`.
Hero pleine largeur, puis paires de sections `column_span: 2` : l'œil lit
en Z, jamais en colonne infinie.

## 2. Data visualization

Trois formes, trois intentions — jamais deux fois la même pour la même question :

| Carte | Forme | Question posée |
|-------|-------|----------------|
| Puissance 24 h | aire lissée + dégradé | « comment ça évolue ? » |
| Énergie 7 j | barres arrondies | « comment on compare jour à jour ? » |
| Charge instantanée | radial | « où on en est *maintenant* ? » |

Animations ApexCharts : entrée `easeinout` 900 ms, `animateGradually`
150 ms (les séries se dessinent en cascade), `dynamicAnimation` 420 ms
pour que les mises à jour temps réel glissent au lieu de sauter.

## 3. Dark mode

| Rôle | Valeur |
|------|--------|
| Fond carte | `linear-gradient(155deg,#1c2333f0,#0e121bf7)` |
| Bordure | `#ffffff12` (≈ 7 % blanc) |
| Ombre | `0 12px 34px -16px #000000d9` + `inset 0 1px 0 #ffffff0d` |
| Texte principal | `#E6EAF2` |
| Texte secondaire | `#8B95A7` |
| Accents | cyan `#22D3EE` · bleu `#5B8DEF` · violet `#A78BFA` · vert `#34D399` · ambre `#FBBF24` · rouge `#F87171` |

Le liseré interne clair (`inset`) est ce qui donne l'effet « verre » :
sans lui les cartes sombres paraissent plates.
Contraste texte secondaire sur fond carte ≈ 5.6:1 — au-dessus du seuil AA
pour le texte courant.

## 4. Navigation

Barre pleine largeur en tête de chaque vue, deux états pilotés par
`input_boolean.nexus_navigation_compacte` :
**étendu** (icône + libellé) ↔ **compact** (icônes seules), bascule par le
bouton « Réduire ». L'onglet actif porte son accent en fond + bordure ;
les autres restent gris et ne se colorent qu'au survol.

## 5. États vides

Section « Lumières actives » : une carte `entity-filter` (`show_empty: false`)
affiche uniquement les lumières allumées. Quand il n'y en a aucune, une carte
d'état vide prend le relais — bordure pointillée, centrée :

> 🌙 **Tout est éteint**
> Aucune lumière allumée dans la maison. Les pièces actives apparaîtront ici
> automatiquement.

Elle se masque automatiquement dès qu'une lumière s'allume
(`display:none` conditionnel via template card-mod).

## 6. Squelettes de chargement

Toute tuile dont l'entité est `unavailable` / `unknown` bascule en squelette :
texte et icône passés en `transparent`, dégradé qui balaie la carte
(`nxSh`, 1.6 s, infini), interactions désactivées.
Visible en conditions réelles sur la tuile « Lave-linge ».

## 7. Résultat honnête

**Ce qui atteint vraiment le niveau « SaaS premium »** — la hiérarchie
typographique du hero, la cohérence des accents, les charts animés, les
états vides et squelettes, les micro-interactions au survol.

**Ce qui ne l'atteint pas, et pourquoi :**

- **Pas de vraie sidebar rétractable en largeur.** Les vues `sections` ne
  permettent pas à une section de changer de `column_span` selon un état.
  La barre horizontale rétractable est le meilleur équivalent honnête ;
  la sidebar native de HA (ou `kiosk-mode`, déjà installé) reste l'outil
  pour ça.
- **Les squelettes ne sont pas de vrais états de chargement.** HA pousse
  l'état par websocket, il n'y a pas de phase « loading » à masquer.
  Le squelette couvre le cas réel équivalent : l'entité indisponible.
- **Le styling repose sur card-mod**, qui cible le shadow DOM du frontend.
  À revérifier après chaque montée de version majeure de HA. Un thème
  (`frontend: themes:`) serait plus robuste, mais impose une modification
  de `configuration.yaml` — écartée ici volontairement.
