# Snapshots du dashboard MAISON — onglet ÉNERGIE

Sauvegarde de la vue `dashboard-maison` › `ÉNERGIE` (`config["views"][3]`),
avant et après le travail de lisibilité des graphiques.

Ces fichiers ne font pas partie de l'intégration Ambrogio : ils sont ici
uniquement pour garder une trace, parce qu'un dashboard Home Assistant en
mode `storage` ne conserve aucun historique de version.

| Fichier | Contenu |
|---|---|
| `energie-avant.json` | la vue telle qu'elle était avant les modifications |
| `energie-apres.json` | la vue telle qu'elle est maintenant |

## Ce qui a changé

- **Dates décalées d'un jour** — les histogrammes utilisaient
  `statistics.align: end`, ce qui datait chaque barre à minuit du lendemain.
  Passé à `align: middle` : la date sous une barre est bien celle du jour mesuré.
- **Lisibilité des axes** — les graduations étaient écrites dans la couleur néon
  de la série (violet, or, vert) en 10 px sur fond noir. Elles sont maintenant
  en gris clair neutre (`#c7d2de`) en 11 px ; le néon reste réservé aux données.
- **Grille** — remontée de 8 % à 16 % d'opacité, lignes horizontales seulement.
- **Échelle** — `yaxis.min: 0` partout, pour que la hauteur des barres et de la
  courbe soit proportionnelle à la valeur.
- **Format des dates** — `dd/MM` sous les histogrammes, `HH:mm` sous la courbe
  24 h, infobulles en toutes lettres, le tout avec une locale française.
- **Étiquettes qui se chevauchaient** — sur 30 jours, le nombre de graduations
  est limité (`tickAmount`) au lieu d'une par jour.
- **Courbe 24 h** — `curve: straight` au lieu de `smooth` (le lissage inventait
  des valeurs entre deux mesures) et repères sur le pic et le creux du jour.
- **Unités dans le graphique** — l'axe vertical affiche directement `45 kWh`,
  `12 €`, `1,7 kW` (formatters `EVAL:` d'apexcharts-card), et les étiquettes
  au-dessus des barres portent leur unité, avec la virgule décimale française.
  Plus besoin de légende écrite pour savoir ce qu'on lit.
- **Textes d'explication supprimés** — les blocs de texte sous chaque titre ont
  été retirés ; l'information est portée par le graphique lui-même.
- **Graphiques agrandis** — hauteurs portées à 260–290 px (l'espace libéré par
  les textes), et `forceNiceScale` pour des graduations rondes.
- **Onglet** — la vue a maintenant un chemin stable (`/dashboard-maison/energie`)
  et un titre (`ÉNERGIE`) ; elle n'avait qu'une icône.

## Revenir en arrière

Restaurer `energie-avant.json` dans `config["views"][3]` du dashboard
`dashboard-maison`, en gardant la structure du reste du dashboard intacte.
