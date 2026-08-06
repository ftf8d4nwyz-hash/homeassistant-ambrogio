# Carte Présence — détection réelle du déplacement

Dashboard `dashboard-maison` › vue `Favoris` › `views[4].sections[0].cards[0].cards[1]`
(carte `custom:html-template-card`).

## Le problème

La carte affichait « 🚗 EN ROUTE » dès que la personne n'était pas dans une zone
maison. C'était la seule condition :

```jinja
{% set home=('zone.home' in _z) or ('zone.zone_maison_burtoncourt' in _z) %}
{% if home %} À LA MAISON {% else %} 🚗 EN ROUTE {% endif %}
```

Voiture garée au bureau, en courses, chez quelqu'un : la carte annonçait
quand même « EN ROUTE » avec une heure d'arrivée calculée sur un trajet qui
n'avait pas commencé.

## Pourquoi il a fallu construire le signal

L'app Home Assistant sur iPhone ne remonte **ni vitesse ni activité** :
`device_tracker.iphone_de_maryline` ne fournit que position, précision GPS et
batterie. Aucun capteur existant ne disait si la voiture roulait.

La vitesse est donc dérivée de la distance routière Waze, qui elle change
uniquement quand la personne se déplace (contrairement à la durée, qui bouge
aussi avec le trafic).

## Helpers créés

| Helper | Type | Détail |
|---|---|---|
| `sensor.distance_maryline_maison` | template | expose l'attribut `distance` de `sensor.cuisine_waze_trajet_maryline_maison` en km |
| `sensor.distance_faure_maison` | template | idem pour Faure |
| `sensor.vitesse_maryline` | derivative | dérivée de la distance, `unit_time: h`, fenêtre 5 min → km/h |
| `sensor.vitesse_faure` | derivative | idem pour Faure |

`derivative` est le helper prévu pour un taux de variation (cf. guide des
helpers) — pas un capteur template qui calculerait le delta à la main.

Le signe porte l'information : **négatif = se rapproche**, positif = s'éloigne.

## Les trois états

| Condition | Affichage |
|---|---|
| dans une zone maison | 🏠 À LA MAISON |
| vitesse < −5 km/h | 🚗 EN ROUTE + distance, durée, heure d'arrivée, vitesse d'approche |
| vitesse > +5 km/h | ↗️ S'ÉLOIGNE + vitesse et adresse |
| \|vitesse\| ≤ 5 km/h | 🅿️ À L'ARRÊT + distance et adresse |

L'adresse vient de `sensor.*_geocoded_location`. L'heure d'arrivée n'est plus
affichée que lorsque la personne se rapproche réellement.

## Accès carte

Deux boutons apparaissent sous les infos quand la personne n'est pas à la maison :

- **🗺️ CARTE** — navigation interne vers le tableau de bord `/map` (carte HA
  live), via `history.pushState` + événement `location-changed` pour éviter un
  rechargement complet de la page.
- **🚦 WAZE** — `https://www.waze.com/ul?ll=<lat>,<lon>&navigate=yes`, construit
  avec les coordonnées courantes de la personne ; ouvre l'app Waze en navigation
  vers sa position.

Un clic sur la carte elle-même ouvre toujours la fiche détaillée HA de la
personne, qui contient déjà une carte live avec l'historique de trajet.

## Limites connues

- **Latence de détection.** L'intégration Waze Travel Time interroge toutes les
  ~5 min, et la dérivée lisse sur 5 min : le passage en « EN ROUTE » arrive donc
  5 à 10 min après le démarrage réel. Réduire la fenêtre de la dérivée à 0 rend
  la détection plus rapide mais plus sensible au bruit GPS.
- **Après un redémarrage de HA**, la dérivée repart de 0 et affiche « À L'ARRÊT »
  jusqu'à avoir accumulé deux relevés Waze.
- La vitesse mesurée est une **vitesse d'approche le long de l'itinéraire**, pas
  la vitesse du véhicule : un trajet perpendiculaire à la maison la sous-estime.
  C'est suffisant pour distinguer « roule » de « garée », pas pour un compteur.

## Revenir en arrière

Remplacer le bloc de statut par l'ancienne condition ci-dessus, et supprimer les
quatre helpers dans Paramètres → Appareils et services → Aides.
