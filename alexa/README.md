# Skill Alexa personnalisée → Home Assistant

Permet de parler à un Echo en texte libre pour qu'un agent conversationnel pilote
Home Assistant, au lieu de se limiter aux commandes Smart Home.

```
Echo → skill Alexa → Lambda (relais) → /api/alexa → intent_script → script HA → agent → TTS Echo
```

## Pourquoi un relais Lambda

C'est le point qui coûte le plus de temps à découvrir seul.

Une skill Alexa personnalisée transmet le jeton du compte lié **dans le corps
JSON** de la requête, à `session.user.accessToken`. Or `AlexaIntentsView`, la vue
qui sert `/api/alexa`, ne désactive pas `requires_auth`, et le middleware HTTP de
Home Assistant n'authentifie que par en-tête `Authorization: Bearer`, chemin signé
ou socket Unix du Superviseur — **jamais** depuis le corps de la requête.

Les deux ne se rencontrent donc jamais : Home Assistant répond `401` et Alexa dit
« un problème est survenu avec la réponse de la Skill ». Le liage de compte seul
ne suffit pas.

Le Lambda comble cet écart : il reçoit la requête de la skill, la réexpédie telle
quelle à Home Assistant avec l'en-tête attendu, et renvoie la réponse sans la
modifier. Une fois en place, le liage de compte devient inutile.

## Déploiement

**Fonction Lambda** — région `eu-west-1` (Alexa n'accepte que quatre régions ;
c'est celle de l'Europe), runtime Python 3.13, code = `lambda_function.py`.

- Timeout : **10 s**. Le défaut de 3 s coupe avant Home Assistant.
- Déclencheur : **Alexa Skills Kit**, avec vérification du Skill ID.
- Variables d'environnement :

| Clé | Valeur |
|---|---|
| `HA_URL` | `https://<instance>.ui.nabu.casa` (sans slash final) |
| `HA_TOKEN` | jeton d'accès longue durée Home Assistant |
| `SKILL_ID` | `amzn1.ask.skill.<uuid>` |

**Console Alexa** — *Build → Endpoint → AWS Lambda ARN*, ARN de la fonction dans
*Default Region*.

**Home Assistant** — `alexa:` et `intent_script:` dans `configuration.yaml`
(aucune interface graphique pour ces deux clés ; redémarrage obligatoire, elles ne
se rechargent pas à chaud) :

```yaml
alexa: {}
intent_script:
  ClaudeIntent:
    # Répond tout de suite sans attendre l'agent : Alexa coupe à 8 secondes
    async_action: true
    speech:
      type: plain
      text: "C'est parti, je m'en occupe."
    action:
      - action: script.turn_on
        target:
          entity_id: script.claude_demande_vocale
        data:
          variables:
            question: "{{ Query }}"
```

## Le modèle d'interaction, et le piège des énoncés

Le slot `Query` est de type `AMAZON.SearchQuery`, qui **ne peut jamais constituer
un énoncé à lui seul** : Amazon impose au moins un mot porteur devant.

Piège supplémentaire en français : dans « demande à \<skill\> **de** … », le « de »
appartient à la formule d'invocation et est consommé par Alexa. Le modèle ne reçoit
que ce qui suit. Un énoncé `de {Query}` ne matche donc jamais, alors que
`me dire {Query}` capte bien « demande à \<skill\> de me dire bonjour » avec
`Query = "bonjour"`.

Il faut une ligne par verbe employé : `dire {Query}`, `me dire {Query}`,
`allumer {Query}`, `éteindre {Query}`, `mettre {Query}`…

Supprimer aussi `HelloWorldIntent` du gabarit : ses énoncés français captent les
phrases courtes avant l'intent personnalisé.

## Garde-fous côté Home Assistant

- `input_boolean.agent_claude_actif` — coupe-circuit unique.
- Filtre de sécurité dans le script : toute phrase touchant alarme, portail,
  verrouillage ou sirène est refusée avant d'atteindre l'agent. Il reste la seule
  barrière côté voix, d'autant qu'un jeton à accès complet vit dans les variables
  d'environnement AWS.
- `input_text.claude_derniere_demande` / `..._reponse` — journal des deux derniers
  échanges.

## Notes

- `async_action: true` est indispensable : une skill doit répondre en 8 secondes,
  un agent qui manipule la maison met bien plus. La réponse réelle arrive ensuite
  en TTS.
- La réponse sort toujours du haut-parleur codé en dur dans le script, pas de
  l'Echo auquel on a parlé — Alexa transmet bien l'identifiant de l'appareil, mais
  `intent_script` ne l'expose pas aux templates.
- Les valeurs propres à l'installation (URL Nabu Casa, Skill ID, jeton) sont
  volontairement absentes de ce dépôt.
