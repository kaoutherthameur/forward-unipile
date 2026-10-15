#!/usr/bin/env python3
"""E2 - Accountability WhatsApp : le coaché répond son avancement, l'IA relance/encourage. Récurrent (webhook message_received)."""
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


def classify_progress(text):
    """Pure : classe l'avancement du coaché à partir de son message. Testable hors-ligne.

    Retourne "done" (action réalisée), "blocked" (bloqué/pas fait) ou "unclear".
    """
    t = (text or "").lower()
    if any(k in t for k in ("fait", "terminé", "termine", "fini", "réussi", "reussi", "ok c'est bon", "c'est bon", "done")):
        return "done"
    if any(k in t for k in ("pas eu le temps", "pas fait", "bloqué", "bloque", "j'ai pas", "je n'ai pas", "galère", "galere", "dur", "difficile")):
        return "blocked"
    return "unclear"


def coach_reply(text):
    """Stub : renvoie un message d'encouragement/relance selon l'avancement. Testable hors-ligne.

    À remplacer par un appel LLM pour personnaliser. Ici : déterministe sur la
    classification, pour un comportement prévisible et testable.
    """
    status = classify_progress(text)
    if status == "done":
        return "Bravo, ça c'est de la régularité ! Une fois posé, quelle est la prochaine petite action ?"
    if status == "blocked":
        return "Pas de souci, ça arrive. C'est quoi le plus petit pas que tu peux faire aujourd'hui, même 5 minutes ?"
    return "Merci pour ton retour ! Dis-m'en un peu plus : tu as pu avancer ou quelque chose t'a bloqué ?"


def log_progress(chat_id, sender_name, text, status):
    """Stub : print. À câbler (Sheet/CRM/DB) pour historiser la progression."""
    print("PROGRESS:", json.dumps(
        {"chat_id": chat_id, "sender_name": sender_name, "status": status, "text": text},
        ensure_ascii=False))


def process_event(payload, our_provider_ids):
    """Pure : décide de la relance et loggue la progression. Testable hors-ligne."""
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "message sortant (de nous)"}
    text = payload.get("message", "")
    status = classify_progress(text)
    return {
        "action": "reply",
        "chat_id": payload.get("chat_id", ""),
        "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
        "text": text,
        "status": status,
        "reply": coach_reply(text),
    }


def send_reply(chat_id, reply):
    """Envoi de la relance/encouragement sur le fil WhatsApp. ÉCRITURE -> respecte UNIPILE_DRY_RUN."""
    from lib import unipile_helpers as u
    u.post("chats/%s/messages" % chat_id, json={"text": reply}, is_write=True)
    print("RELANCE %s -> chat %s : %s" % (
        "DRY_RUN" if u.dry_run() else "LIVE", chat_id, reply))


try:
    import modal

    app = modal.App("whatsapp-accountability")
    image = modal.Image.debian_slim().pip_install("fastapi", "httpx", "python-dotenv")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "reply":
            log_progress(result["chat_id"], result["sender_name"], result["text"], result["status"])
            send_reply(result["chat_id"], result["reply"])
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
