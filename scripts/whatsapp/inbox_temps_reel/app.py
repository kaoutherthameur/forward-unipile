#!/usr/bin/env python3
"""A1 - Notifier chaque message WhatsApp entrant (Slack/CRM). Récurrent (webhook message_received)."""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))


def own_ids():
    raw = os.environ.get("UNIPILE_OWN_PROVIDER_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def process_event(payload, our_provider_ids):
    """Pure : décide quoi faire d'un message entrant. Testable hors-ligne. Retourne {"action": ...}."""
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "message sortant (de nous)"}
    reply = {
        "chat_id": payload.get("chat_id", ""),
        "message_id": payload.get("message_id", ""),
        "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
        "sender_id": sender or "",
        "text": payload.get("message", ""),
    }
    return {"action": "notify", "reply": reply}


def notify(reply):
    """Stub : print. À câbler (Slack/CRM). Ex. POST vers un webhook Slack ou une fiche CRM."""
    print("NOTIF ENTRANT:", json.dumps(reply, ensure_ascii=False))


try:
    import modal

    app = modal.App("whatsapp-inbox_temps_reel")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "notify":
            notify(result["reply"])
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
