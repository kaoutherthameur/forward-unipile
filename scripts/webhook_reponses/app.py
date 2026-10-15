#!/usr/bin/env python3
"""F2 - Réponse temps réel : webhook Unipile message_received. Récurrent (service).

Unipile pousse chaque nouveau message LinkedIn ; ce service filtre les messages
ENTRANTS (pas les vôtres) et déclenche une notification (Slack/log) en quelques
secondes. Déployé comme endpoint web Modal.

Porté de forward-graph webhooks/unipile_replies.py.
"""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def own_ids():
    raw = os.environ.get("UNIPILE_OWN_PROVIDER_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def process_event(payload, our_provider_ids):
    """Pure: decide what to do with a webhook event. Testable offline.

    Returns {"action": "ignore"|"notify", ...}.
    """
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "outbound message (from us)"}
    return {
        "action": "notify",
        "chat_id": payload.get("chat_id"),
        "message_id": payload.get("message_id"),
        "text": payload.get("message", ""),
        "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
        "sender_id": sender,
    }


def notify(reply):
    """Send the reply somewhere actionable. Stub: prints. Wire to Slack/email/CRM."""
    print("NEW LINKEDIN REPLY:", json.dumps(reply, ensure_ascii=False))


# --- Modal web endpoint (guarded so this file imports without modal installed) ---
try:
    import modal

    app = modal.App("unipile-webhook-reponses")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "notify":
            notify(result)
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
