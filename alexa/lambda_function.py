"""
Relais Alexa -> Home Assistant.

Alexa place le jeton du compte lie dans le corps JSON (session.user.accessToken),
alors que /api/alexa n'accepte qu'un en-tete `Authorization: Bearer`. Ce Lambda
fait le pont : il recoit la requete de la skill, la reexpedie telle quelle a Home
Assistant avec l'en-tete attendu, et renvoie la reponse de HA sans la modifier.

Variables d'environnement a definir sur la fonction :
  HA_URL    https://xxxxxxxx.ui.nabu.casa        (sans slash final)
  HA_TOKEN  jeton d'acces longue duree Home Assistant
  SKILL_ID  amzn1.ask.skill.xxxxxxxx-xxxx-...    (optionnel mais recommande)
"""

import json
import os
import urllib.error
import urllib.request

HA_URL = os.environ["HA_URL"].rstrip("/")
HA_TOKEN = os.environ["HA_TOKEN"]
SKILL_ID = os.environ.get("SKILL_ID", "")

# Alexa abandonne a 8 s. On coupe avant pour pouvoir journaliser l'echec.
TIMEOUT_SECONDS = 7


def _application_id(event):
    """L'applicationId se trouve dans session pour un IntentRequest, dans
    context pour les requetes sans session."""
    session = event.get("session") or {}
    if app_id := (session.get("application") or {}).get("applicationId"):
        return app_id
    system = (event.get("context") or {}).get("System") or {}
    return (system.get("application") or {}).get("applicationId")


def lambda_handler(event, context):
    # Sans cette verification, n'importe quelle skill connaissant l'ARN
    # pourrait piloter la maison.
    if SKILL_ID:
        received = _application_id(event)
        if received != SKILL_ID:
            raise ValueError(f"applicationId refuse : {received}")

    request = urllib.request.Request(
        f"{HA_URL}/api/alexa",
        data=json.dumps(event).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as err:
        # 401 = jeton invalide ou expire. 404 = `alexa:` absent de configuration.yaml.
        detail = err.read().decode("utf-8", "replace")[:500]
        print(f"Home Assistant a repondu {err.code} : {detail}")
        raise
    except Exception as err:
        print(f"Appel a Home Assistant impossible : {err}")
        raise

    return json.loads(body) if body.strip() else {}
