#!/usr/bin/env python3
"""G3 - Tâches auto depuis WhatsApp : un message entrant qui appelle une action
crée une tâche. Récurrent (webhook message_received).

Unipile pousse chaque nouveau message WhatsApp. Ce service filtre les messages
ENTRANTS (pas les vôtres), détecte ceux qui demandent une action ("tu peux
m'envoyer", "il faudrait", "n'oublie pas") et crée une tâche. `create_task()`
est un stub à câbler (Notion, tasks.md, Todoist...).
"""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# Marqueurs d'intention d'action (français). Volontairement simple et lisible :
# 3 familles de formulations qui, dans un message reçu, appellent une tâche.
ACTION_MARKERS = (
    "tu peux m'envoyer",
    "tu peux m envoyer",
    "peux-tu m'envoyer",
    "il faudrait",
    "il faut que",
    "n'oublie pas",
    "n oublie pas",
    "pense à",
    "pense a",
    "tu me fais",
    "tu peux me",
    "tu pourrais",
    "merci de",
    "peux-tu",
)


def own_ids():
    raw = os.environ.get("UNIPILE_OWN_PROVIDER_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def is_actionable(text):
    """Pure : True si le texte contient une intention d'action. Testable hors-ligne."""
    if not text:
        return False
    low = text.lower()
    return any(marker in low for marker in ACTION_MARKERS)


def process_event(payload, our_provider_ids):
    """Pure : décide quoi faire. Testable hors-ligne.

    Retourne {"action": "ignore"|"create_task", ...}.
    """
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "outbound message (from us)"}
    text = payload.get("message", "")
    if not is_actionable(text):
        return {"action": "ignore", "reason": "no action intent detected"}
    return {
        "action": "create_task",
        "chat_id": payload.get("chat_id"),
        "message_id": payload.get("message_id"),
        "title": text.strip(),
        "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
        "sender_id": sender,
    }


def create_task(task):
    """Crée la tâche dans votre outil. Stub : affiche. À câbler (Notion/tasks.md/Todoist)."""
    print("NOUVELLE TÂCHE:", json.dumps(task, ensure_ascii=False))


# --- Endpoint web Modal (protégé pour que le fichier s'importe sans modal installé) ---
try:
    import modal

    app = modal.App("whatsapp-todo-auto")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "create_task":
            create_task(result)
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
