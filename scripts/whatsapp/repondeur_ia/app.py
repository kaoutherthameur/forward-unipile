#!/usr/bin/env python3
"""A2 - Réponse IA de 1er niveau sur WhatsApp (FAQ), sinon escalade humaine. Récurrent (webhook message_received)."""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def own_ids():
    raw = os.environ.get("UNIPILE_OWN_PROVIDER_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def answer_faq(text):
    """Pure : réponse déterministe de 1er niveau sur mots-clés. Testable hors-ligne.

    Retourne une réponse (str) si un motif est reconnu, sinon None (-> escalade).
    """
    t = (text or "").lower()
    if any(k in t for k in ("horaire", "ouvert", "fermé", "ferme")):
        return "Nous sommes ouverts du lundi au samedi, de 9h à 19h. Fermé le dimanche."
    if any(k in t for k in ("prix", "tarif", "combien", "coûte", "coute")):
        return "Nos tarifs démarrent à 29 EUR. Dites-moi le produit qui vous intéresse et je vous précise le prix exact."
    if any(k in t for k in ("dispo", "disponible", "stock")):
        return "Je vérifie la disponibilité et je vous confirme sous quelques minutes."
    if any(k in t for k in ("adresse", "où", "ou etes", "où êtes", "localisation")):
        return "Nous sommes au 12 rue des Lilas, 75011 Paris. Métro Voltaire."
    return None


def process_event(payload, our_provider_ids):
    """Pure : décide de la réponse (FAQ) ou de l'escalade. Testable hors-ligne."""
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "message sortant (de nous)"}
    text = payload.get("message", "")
    answer = answer_faq(text)
    if answer is None:
        return {"action": "escalate",
                "chat_id": payload.get("chat_id", ""),
                "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
                "text": text}
    return {"action": "answer", "chat_id": payload.get("chat_id", ""), "reply": answer}


def escalate(chat_id, sender_name, text):
    """Stub : print. À câbler (Slack/CRM) pour prise en charge humaine."""
    print("ESCALADE HUMAINE:", json.dumps(
        {"chat_id": chat_id, "sender_name": sender_name, "text": text}, ensure_ascii=False))


def send_reply(chat_id, reply):
    """Envoi de la réponse FAQ sur le fil WhatsApp. ÉCRITURE -> respecte UNIPILE_DRY_RUN."""
    from lib import unipile_helpers as u
    u.post("chats/%s/messages" % chat_id, json={"text": reply}, is_write=True)
    print("REPONSE FAQ %s -> chat %s : %s" % (
        "DRY_RUN" if u.dry_run() else "LIVE", chat_id, reply))


try:
    import modal

    app = modal.App("whatsapp-repondeur_ia")
    image = modal.Image.debian_slim().pip_install("fastapi", "httpx", "python-dotenv")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "answer":
            send_reply(result["chat_id"], result["reply"])
        elif result["action"] == "escalate":
            escalate(result["chat_id"], result["sender_name"], result["text"])
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
