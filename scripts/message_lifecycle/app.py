#!/usr/bin/env python3
"""F5 - Suivre le cycle de vie des messages. Récurrent (service webhook).

Reçoit les webhooks Unipile message_read / message_delivered / message_reaction
et les journalise (accusés de lecture/livraison, réactions sur vos messages).
Déployé comme endpoint web Modal. Lecture (notifications entrantes).
"""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

LIFECYCLE_EVENTS = {"message_read", "message_delivered", "message_reaction", "message_edited", "message_deleted"}


def process_event(payload):
    """Pure: classify a lifecycle webhook event. Testable offline."""
    event = payload.get("event")
    if event not in LIFECYCLE_EVENTS:
        return {"action": "ignore", "reason": "not a lifecycle event"}
    return {
        "action": "log",
        "event": event,
        "chat_id": payload.get("chat_id"),
        "message_id": payload.get("message_id"),
        "actor": (payload.get("sender") or {}).get("attendee_name", ""),
    }


def record(entry):
    """Persist the lifecycle event. Stub: prints. Wire to your store/dashboard."""
    print("MESSAGE LIFECYCLE:", json.dumps(entry, ensure_ascii=False))


try:
    import modal

    app = modal.App("unipile-message-lifecycle")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload)
        if result["action"] == "log":
            record(result)
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
