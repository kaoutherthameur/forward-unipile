#!/usr/bin/env python3
"""A4 - Accusé de réception auto hors des heures d'ouverture. Récurrent (webhook message_received)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ACCUSE_DEFAUT = "Bien reçu, merci pour votre message. On revient vers vous sous 2h ouvrées."


def own_ids():
    raw = os.environ.get("UNIPILE_OWN_PROVIDER_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def process_event(payload, our_provider_ids, in_window):
    """Pure : décide d'envoyer un accusé si le message arrive HORS fenêtre horaire.

    `in_window` (bool) = résultat de u.in_send_window() injecté par l'appelant.
    Testable hors-ligne.
    """
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "message sortant (de nous)"}
    if in_window:
        return {"action": "ignore", "reason": "dans les heures d'ouverture"}
    return {"action": "ack", "chat_id": payload.get("chat_id", "")}


def send_ack(chat_id, message):
    """Envoi de l'accusé de réception. ÉCRITURE -> respecte UNIPILE_DRY_RUN."""
    from lib import unipile_helpers as u
    u.post("chats/%s/messages" % chat_id, json={"text": message}, is_write=True)
    print("ACCUSE %s -> chat %s : %s" % (
        "DRY_RUN" if u.dry_run() else "LIVE", chat_id, message))


try:
    import modal

    app = modal.App("whatsapp-accuse_reception")
    image = modal.Image.debian_slim().pip_install("fastapi", "httpx", "python-dotenv", "pyyaml")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        from lib import unipile_helpers as u
        country = os.environ.get("UNIPILE_SEND_COUNTRY", "FR")
        result = process_event(payload, own_ids(), u.in_send_window(country))
        if result["action"] == "ack":
            send_ack(result["chat_id"], os.environ.get("WHATSAPP_ACK_TEXT", ACCUSE_DEFAUT))
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
