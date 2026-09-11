# Bibliothèque de prompts Claude Code

Prompts prêts à copier-coller, classés par phase du cycle de développement.
Source : documentation Anthropic (`Common workflows`, `Best practices`,
`How Anthropic teams use Claude Code`, `Scaling agentic coding`).

Les valeurs entre `{accolades}` sont à remplacer. Chaque entrée indique un
exemple rempli, la raison pour laquelle le prompt fonctionne, et, le cas
échéant, ce qu'il faut avoir connecté au préalable.

Une section [Adapté à ce dépôt](#adapte-a-ce-depot) en fin de fichier
reprend les prompts les plus utiles pour l'intégration `ambrogio_robot`.

---

## Par où commencer (5 prompts)

| # | Prompt | Section |
|---|--------|---------|
| 1 | `give me an overview of this codebase: architecture, key directories, and how the pieces connect` | [Découvrir](#1-decouvrir--discover) |
| 2 | `where do we {behavior}?` | [Découvrir](#1-decouvrir--discover) |
| 3 | `the {test} test is failing, find out why and fix it` | [Exploiter](#5-exploiter--operate) |
| 4 | `write tests for {path}, run them, and fix any failures` | [Construire](#3-construire--build) |
| 5 | `review my uncommitted changes and flag anything that looks risky before I commit` | [Construire](#3-construire--build) |

---

## 1. Découvrir — Discover

### Prendre ses marques dans un dépôt inconnu ★1

```text
give me an overview of this codebase: architecture, key directories, and how the pieces connect
```

- **Pourquoi ça marche** : décrire ce qu'on veut savoir, pas les fichiers à lire. Claude explore seul et renvoie une synthèse.
- **Pour aller plus loin** : `/init` pour créer `CLAUDE.md` et conserver ce contexte à chaque session.
- *Source : Common workflows*

### Expliquer du code inconnu

```text
explain what {path} does and how data flows through it. write it up as {format}
```

- **Exemple** : `path` = `src/scheduler/queue.ts`, `format` = `an HTML page with a diagram, then open it in my browser`
- **Pourquoi ça marche** : nommer le fichier **et** le format de sortie (diagramme, bullet points, page HTML).
- *Source : Common workflows*

### Trouver où se passe un comportement ★2

```text
where do we {behavior}?
```

- **Exemple** : `behavior` = `validate uploaded file types`
- **Pourquoi ça marche** : recherche par comportement et non par nom de fichier ; fonctionne même sans connaître l'arborescence.
- *Source : Common workflows*

### Vérifier ce qui casse avant de supprimer

```text
what would break if I deleted {target}?
```

- **Exemple** : `target` = `the retryWithBackoff helper`
- **Pourquoi ça marche** : la liste des appelants indique si c'est un nettoyage d'une ligne ou un changement à coordonner.
- *Source : Common workflows*

### Retracer l'évolution d'un fichier

```text
look through the commit history of {path} and summarize how it evolved and why
```

- **Exemple** : `path` = `internal/auth/session.go`
- **Pourquoi ça marche** : pointer l'historique quand la question est « pourquoi » et non « quoi ».
- *Source : Best practices*

### Cadrer un changement avant de le lancer

```text
which files would I need to touch to {change}?
```

- **Exemple** : `change` = `add a dark mode toggle to settings`
- **Rôles** : produit, design
- **Pourquoi ça marche** : dimensionne le travail avant de l'engager dans une roadmap.
- *Source : How Anthropic teams use Claude Code*

### Poser une question produit au code

```text
I am a {role}. walk me through what happens when a user {action}, from the UI down to the result
```

- **Exemple** : `role` = `PM`, `action` = `clicks Export to PDF`
- **Pourquoi ça marche** : préciser son rôle cale le niveau de la réponse.
- *Source : How Anthropic teams use Claude Code*

---

## 2. Concevoir — Design

### Planifier un changement multi-fichiers sans toucher au code

```text
plan how to refactor the {target} to {goal}. list the files you would change, but don't edit anything yet
```

- **Exemple** : `target` = `payment module`, `goal` = `support multiple currencies`
- **Pourquoi ça marche** : « don't edit yet » sépare l'exploration des modifications. `Shift+Tab` active le *plan mode* en permanence.
- *Source : Common workflows*

### Rédiger une spec par interview

```text
I want to build {feature}. interview me about implementation, UX, edge cases, and tradeoffs until we have covered everything, then write the spec to SPEC.md
```

- **Exemple** : `feature` = `per-workspace rate limits`
- **Pourquoi ça marche** : se faire interviewer plutôt qu'écrire la spec soi-même ; Claude pose les questions jusqu'à complétude.
- *Source : Best practices*

### Transformer des notes de réunion en tickets

```text
read {input} and write up the action items, then create a {tracker} ticket for each with acceptance criteria
```

- **Exemple** : `input` = `@meeting-notes.md`, `tracker` = `Linear`
- **Prérequis** : tracker connecté (connecteur claude.ai ou serveur MCP).
- **Pourquoi ça marche** : on relit les tickets, pas la transcription.
- *Source : How Anthropic teams use Claude Code*

### Cartographier les cas limites avant de construire

```text
list the error states, empty states, and edge cases for {feature} that the design needs to cover
```

- **Exemple** : `feature` = `the file upload flow`
- **Pourquoi ça marche** : demander ce qui manque, pas ce qui existe.
- *Source : How Anthropic teams use Claude Code*

### Transformer une maquette en prototype cliquable

```text
here is a mockup. build a working prototype I can click through, matching the layout and states shown
```

- **À faire avant** : coller / glisser / `@`-mentionner l'image de la maquette.
- **Pourquoi ça marche** : un prototype cliquable répond à des questions qu'une maquette statique ne peut pas.
- *Source : How Anthropic teams use Claude Code*

### Implémenter depuis une capture d'écran, avec auto-vérification

```text
implement this design, then take a screenshot of the result, compare it to the original, and fix any differences
```

- **À faire avant** : coller l'image du design.
- **Prérequis** : un moyen de rendre et capturer le résultat (app Desktop, extension Chrome, ou MCP Playwright).
- **Pourquoi ça marche** : Claude obtient une boucle de vérification et itère sans qu'on pointe chaque écart.
- *Source : Best practices*

---

## 3. Construire — Build

### Suivre un motif existant

```text
look at how {example} is implemented to understand the pattern, then build {new} the same way
```

- **Exemple** : `example` = `the GitHub webhook handler`, `new` = `a Stripe webhook handler`
- **Pourquoi ça marche** : sans référence Claude applique des bonnes pratiques génériques ; avec référence il suit vos conventions.
- *Source : Best practices*

### Documenter du code non documenté

```text
find {scope} without {format} comments and add them, matching the style already used in the file
```

- **Exemple** : `scope` = `the public functions in src/auth/`, `format` = `JSDoc`
- *Source : Common workflows*

### Ajouter une petite fonctionnalité bien définie

```text
add a {endpoint} endpoint that returns {payload}
```

- **Exemple** : `endpoint` = `/health`, `payload` = `the app version and uptime`
- **Pourquoi ça marche** : préciser entrées et sorties, pas la façon de coder.
- *Source : Common workflows*

### Construire un petit outil interne

```text
create a {tool} using HTML, CSS, and vanilla JavaScript, then open it in my browser
```

- **Exemple** : `tool` = `drag-and-drop Kanban board with three columns`
- *Source : How Anthropic teams use Claude Code*

### Traiter une issue de bout en bout

```text
read issue #{issue}, implement the fix, and run the tests
```

- **Exemple** : `issue` = `312`
- **Prérequis** : CLI `gh` authentifiée ou GitHub connecté.
- **Pourquoi ça marche** : donner le numéro, pas un résumé : Claude lit le ticket complet.
- *Source : Common workflows*

### Trouver et mettre à jour un texte dans tout le code

```text
find every place we say "{copy}" or a close variant, show me each one in context, then update them all to "{new}". leave tests and the changelog alone
```

- **Exemple** : `copy` = `Sign up free`, `new` = `Start free trial`
- **Pourquoi ça marche** : demander les variantes et dire quoi ignorer.
- *Source : How Anthropic teams use Claude Code*

### Rédiger à partir d'exemples passés

```text
read the {examples} in {folder} to learn the structure and voice, then draft a new one for {topic}
```

- **Exemple** : `examples` = `privacy impact assessments`, `folder` = `legal/pia/`, `topic` = `the new analytics integration`
- **Pourquoi ça marche** : pointer un dossier de travaux finis au lieu de décrire son style.
- *Source : How Anthropic uses Claude in Legal*

### Écrire des tests, les lancer, corriger les échecs ★4

```text
write tests for {path}, run them, and fix any failures
```

- **Exemple** : `path` = `app/parsers/feed.py`
- **Pourquoi ça marche** : demander écrire + lancer + corriger dans le même prompt pour que Claude itère sans s'arrêter.
- *Source : Common workflows*

### Piloter l'implémentation par les tests

```text
write tests for {feature} first, then implement it until they pass
```

- **Exemple** : `feature` = `the password reset flow`
- *Source : Scaling agentic coding guide*

### Combler les trous à partir d'un rapport de couverture

```text
read {report} and add tests for the lowest-covered files until each is above {target}%
```

- **Exemple** : `report` = `coverage/coverage-summary.json`, `target` = `80`
- *Source : Common workflows*

### Migrer un motif dans tout le code

```text
migrate everything from {from} to {to}: identify every place that needs to change, then make the changes
```

- **Exemple** : `from` = `the old logging API`, `to` = `the structured logger`
- **Pourquoi ça marche** : demander d'abord la liste des sites d'appel permet de vérifier qu'aucun n'est oublié. Pour une migration très large : `/batch`.
- *Source : Common workflows*

### Porter du code vers un autre langage

```text
port {source} to {target}, keeping the same {keep}
```

- **Exemple** : `source` = `this Python module`, `target` = `Rust`, `keep` = `public API and test behavior`
- **Pourquoi ça marche** : nommer ce qui doit rester identique donne un contrat vérifiable.
- *Source : How Anthropic teams use Claude Code*

### Optimiser vers une cible mesurable

```text
optimize {target} to bring {metric} from {current} down to under {goal}
```

- **Exemple** : `target` = `the search query`, `metric` = `p95 latency`, `current` = `2s`, `goal` = `500ms`
- *Source : Scaling agentic coding guide*

### Corriger un bug visuel précis

```text
the {element} extends {amount} beyond the {container} on {viewport}. fix it.
```

- **Exemple** : `element` = `login button`, `amount` = `20px`, `container` = `card border`, `viewport` = `mobile`
- *Source : Scaling agentic coding guide*

### Relire ses modifications avant de commiter ★5

```text
review my uncommitted changes and flag anything that looks risky before I commit
```

- **Pourquoi ça marche** : Claude lit les fichiers modifiés en entier, pas seulement les lignes du diff.
- **Pour aller plus loin** : `/code-review` fait la même chose en une commande.
- *Source : Common workflows*

### Relire une pull request

```text
review PR #{pr} and summarize what changed, then list any concerns
```

- **Exemple** : `pr` = `247`
- **Prérequis** : `gh` authentifiée ou GitHub connecté.
- *Source : Common workflows*

### Relire un changement d'infrastructure avant application

```text
here is my Terraform plan output. what is this going to do, and is anything here going to cause problems?
```

- **À faire avant** : coller la sortie du plan dans le prompt.
- *Source : How Anthropic teams use Claude Code*

### Lancer une revue de sécurité avec un sous-agent

```text
use a subagent to review {path} for security issues and report what it finds
```

- **Exemple** : `path` = `src/api/`
- **Pourquoi ça marche** : le sous-agent travaille dans sa propre fenêtre de contexte et ne remplit pas la session principale.
- *Source : Best practices*

### Relire un contenu avant envoi

```text
review {file} for {concerns} and list anything I should fix before it goes to {reviewer}
```

- **Exemple** : `file` = `launch-post.md`, `concerns` = `unsupported claims, missing attributions, and brand-guideline issues`, `reviewer` = `legal`
- *Source : How Anthropic uses Claude in Legal*

### Corriger une mauvaise approche en cours de route

```text
that is not right: {feedback}. try a different approach
```

- **Exemple** : `feedback` = `the function signature needs to stay backward-compatible`
- **Pourquoi ça marche** : nommer la contrainte manquée, pas seulement dire que c'est faux.
- **Astuce** : `Esc` `Esc` ouvre le menu de rewind pour repartir propre.
- *Source : Best practices*

### Réduire la portée d'un changement

```text
that is too much. keep only the changes to {scope} and undo your other edits
```

- **Exemple** : `scope` = `the validation logic in src/forms/`
- *Source : Best practices*

### Transformer une correction en règle

```text
you keep {mistake}. add a rule to CLAUDE.md so this stops happening
```

- **Exemple** : `mistake` = `using default exports when this project uses named exports`
- **Pourquoi ça marche** : une correction en chat se perd ; une règle dans `CLAUDE.md` est relue à chaque session et partagée avec l'équipe.
- *Source : Best practices*

---

## 4. Livrer — Ship

### Résoudre des conflits de merge

```text
resolve the merge conflicts in this branch and explain what you kept from each side
```

- **Pourquoi ça marche** : demander le raisonnement rend le merge relisible.
- *Source : Common workflows*

### Commiter avec un message généré

```text
commit these changes with a message that summarizes what I did
```

- *Source : Common workflows*

### Ouvrir une PR à partir d'un ticket

```text
find the {tracker} ticket about {topic} and open a PR that implements it
```

- **Exemple** : `tracker` = `Linear`, `topic` = `the login timeout`
- **Prérequis** : tracker connecté.
- *Source : Common workflows*

### Rédiger des notes de version depuis l'historique git

```text
compare {from} to {to} and draft release notes grouped by feature, fix, and breaking change
```

- **Exemple** : `from` = `v2.3.0`, `to` = `v2.4.0`
- *Source : Common workflows*

### Écrire un workflow CI

```text
write a GitHub Actions workflow that {steps} on every push to {branch}
```

- **Exemple** : `steps` = `runs the tests and deploys to staging`, `branch` = `main`
- *Source : Common workflows*

---

## 5. Exploiter — Operate

### Trouver et corriger un test qui échoue ★3

```text
the {test} test is failing, find out why and fix it
```

- **Exemple** : `test` = `UserAuth`
- **Pourquoi ça marche** : décrire le symptôme suffit ; Claude lance le test, remonte à la source et corrige.
- *Source : Common workflows*

### Enquêter sur une erreur signalée

```text
users are seeing {symptom} on {where}. investigate and tell me what is going on
```

- **Exemple** : `symptom` = `500 errors`, `where` = `/api/settings`
- *Source : Common workflows*

### Corriger une erreur de build à la racine

```text
here is a build error. fix the root cause and verify the build succeeds
```

- **À faire avant** : coller la sortie d'erreur.
- **Pourquoi ça marche** : demander cause racine + vérification évite les rustines qui masquent l'erreur.
- *Source : Best practices*

### Enquêter sur un incident de production

```text
{symptom}. check the logs, recent deploys, and config changes, then tell me the most likely cause
```

- **Exemple** : `symptom` = `the checkout endpoint started returning 500s an hour ago`
- **Pourquoi ça marche** : lister les sources de preuves à corréler, pas les étapes à suivre.
- *Source : Common workflows*

### Diagnostiquer depuis une capture de console

```text
here is a screenshot of {console}. walk me through why {resource} is failing and give me the exact commands to fix it
```

- **Exemple** : `console` = `the GCP Kubernetes dashboard`, `resource` = `this pod`
- **À faire avant** : coller la capture d'écran.
- *Source : How Anthropic teams use Claude Code*

### Interroger des logs en langage naturel

```text
show me all {events} for {scope} over {timeframe}. write the query, run it, and tell me what stands out
```

- **Exemple** : `events` = `failed logins`, `scope` = `the auth service`, `timeframe` = `the past 24 hours`
- **Prérequis** : entrepôt de données ou store de logs connecté (connecteur / MCP).
- *Source : How Anthropic uses Claude in Cybersecurity*

### Analyser un fichier de données

```text
read {file}, summarize the key patterns, and write the results to {output}
```

- **Exemple** : `file` = `@reports/q1-signups.csv`, `output` = `an HTML page with charts, then open it in my browser`
- *Source : How Anthropic teams use Claude Code*

### Générer des variantes à partir de données de performance

```text
read {file}, find the underperforming {items}, and generate {n} new variations that stay under {limit} characters
```

- **Exemple** : `file` = `@ads-performance.csv`, `items` = `headlines`, `n` = `20`, `limit` = `90`
- *Source : How Anthropic teams use Claude Code*

### Transformer une tâche récurrente en skill

```text
create a /{name} skill for this project that {steps}
```

- **Exemple** : `name` = `ship`, `steps` = `runs the linter and tests, then drafts a commit message`
- *Source : Common workflows*

### Ajouter un hook pour un comportement répété

```text
write a hook that {action} after every {event}
```

- **Exemple** : `action` = `runs prettier`, `event` = `edit to a .ts or .tsx file`
- **Pourquoi ça marche** : un hook rend le comportement automatique au lieu d'avoir à le redemander.
- *Source : Best practices*

### Connecter un outil via MCP

```text
set up the {server} MCP server so you can read my {data} directly
```

- **Exemple** : `server` = `Sentry`, `data` = `error reports`
- *Source : Common workflows*

### Capturer ce qu'il faut retenir

```text
summarize what we did this session and suggest what to add to CLAUDE.md
```

- **Pourquoi ça marche** : Claude sait ce qu'il a dû découvrir pendant la session et propose les entrées `CLAUDE.md` correspondantes.
- *Source : How Anthropic teams use Claude Code*

---

## Ce qui rend ces prompts efficaces

1. **Décrire le résultat, pas les étapes** — `add rate limiting to the public API and make sure existing tests still pass`
2. **Donner un moyen de s'auto-vérifier** — `write the migration, run it against the dev database, and confirm the schema matches`
3. **Pointer une référence** — `add a settings page that follows the same layout as the profile page`
4. **Énoncer une cible mesurable** — `get the bundle size under 200KB and show me what you removed`
5. **Fournir l'artefact** — `why is the build failing? @build.log`
6. **Dire quel format de réponse on veut** — `explain how the payment retry logic works as an HTML page with a diagram, then open it in my browser`

---

<a id="adapte-a-ce-depot"></a>
## Adapté à ce dépôt (`ambrogio_robot`)

Intégration personnalisée Home Assistant, tests via
`pytest-homeassistant-custom-component`, lint via `ruff` (`scripts/lint`).

```text
give me an overview of this codebase: architecture, key directories, and how the pieces connect
```

```text
explain what custom_components/ambrogio_robot/coordinator.py does and how data flows from the API to the entities
```

```text
where do we map robot status codes to Home Assistant vacuum states?
```

```text
look at how sensor.py is implemented to understand the pattern, then build a new sensor the same way
```

```text
write tests for custom_components/ambrogio_robot/coordinator.py, run them with pytest, and fix any failures
```

```text
the test_config_flow test is failing, find out why and fix it
```

```text
run scripts/lint and fix every issue it reports without changing behavior
```

```text
review my uncommitted changes and flag anything that looks risky before I commit
```

```text
compare the last release tag to HEAD and draft release notes grouped by feature, fix, and breaking change
```
