#!/usr/bin/env python3
"""A6 - Détecter les messages WhatsApp de churn/urgence et alerter en priorité. Récurrent (webhook message_received)."""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

MOTS_URGENCE = ("annuler", "résilier", "resilier", "remboursement", "rembourser",
                "déçu", "decu", "urgent", "inadmissible", "scandaleux",
                "avocat", "porter plainte", "arnaque", "inacceptable")


def own_ids():
    raw = os.environ.get("UNIPILE_OWN_PROVIDER_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def is_urgent(text):
    """Pure : True si le message contient un signal de churn/urgence. Testable hors-ligne."""
    t = (text or "").lower()
    return any(k in t for k in MOTS_URGENCE)


def matched_keywords(text):
    """Pure : liste des mots-clés déclencheurs présents. Testable hors-ligne."""
    t = (text or "").lower()
    return [k for k in MOTS_URGENCE if k in t]


def process_event(payload, our_provider_ids):
    """Pure : décide s'il faut lever une alerte prioritaire. Testable hors-ligne."""
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "message sortant (de nous)"}
    text = payload.get("message", "")
    if not is_urgent(text):
        return {"action": "ignore", "reason": "aucun signal d'urgence"}
    return {"action": "alert",
            "chat_id": payload.get("chat_id", ""),
            "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
            "keywords": matched_keywords(text),
            "text": text}


def alert(chat_id, sender_name, keywords, text):
    """Stub : print. À câbler (alerte prioritaire Slack/CRM, mention responsable)."""
    print("ALERTE URGENCE:", json.dumps(
        {"chat_id": chat_id, "sender_name": sender_name,
         "keywords": keywords, "text": text}, ensure_ascii=False))


try:
    import modal

    app = modal.App("whatsapp-detection_urgence")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "alert":
            alert(result["chat_id"], result["sender_name"],
                  result["keywords"], result["text"])
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
