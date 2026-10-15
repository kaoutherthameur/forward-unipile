#!/usr/bin/env python3
"""E6 - Note vocale WhatsApp reçue -> transcription + résumé pour le coach. Récurrent (webhook message_received)."""
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


def extract_audio(payload):
    """Pure : renvoie l'URL de l'audio si le message est une note vocale, sinon None.

    Le média arrive avec un attachment de type "audio" (ex : payload["attachment"]
    ou payload["message"]["attachment"]). Testable hors-ligne.
    """
    att = payload.get("attachment")
    if not att:
        msg = payload.get("message")
        if isinstance(msg, dict):
            att = msg.get("attachment")
    if isinstance(att, dict) and att.get("type") == "audio":
        return att.get("url")
    return None


def transcribe(audio_url):
    """Stub : renvoie une transcription factice. Testable hors-ligne.

    À remplacer par un appel STT (Whisper, etc.). Ici : déterministe pour les tests.
    """
    return "[transcription simulée de %s]" % (audio_url or "?")


def summarize(text):
    """Stub : renvoie un résumé factice de la transcription. Testable hors-ligne.

    À remplacer par un appel LLM. Ici : troncature simple pour un comportement prévisible.
    """
    text = (text or "").strip()
    if len(text) <= 140:
        return text
    return text[:137] + "..."


def process_event(payload, our_provider_ids):
    """Pure : détecte une note vocale entrante, transcrit et résume. Testable hors-ligne."""
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "message sortant (de nous)"}
    audio_url = extract_audio(payload)
    if not audio_url:
        return {"action": "ignore", "reason": "pas de note vocale (attachment audio)"}
    transcript = transcribe(audio_url)
    summary = summarize(transcript)
    return {
        "action": "digest",
        "chat_id": payload.get("chat_id", ""),
        "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
        "audio_url": audio_url,
        "transcript": transcript,
        "summary": summary,
    }


def deliver_to_coach(chat_id, sender_name, transcript, summary):
    """Stub : print. À câbler (Slack/CRM/note) pour livrer le résumé au coach."""
    print("VOCAL RESUME:", json.dumps(
        {"chat_id": chat_id, "sender_name": sender_name,
         "summary": summary, "transcript": transcript}, ensure_ascii=False))


try:
    import modal

    app = modal.App("whatsapp-transcription_vocale")
    image = modal.Image.debian_slim().pip_install("fastapi", "httpx", "python-dotenv")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "digest":
            deliver_to_coach(result["chat_id"], result["sender_name"],
                             result["transcript"], result["summary"])
        return {"ok": True, "action": result["action"]}
except ImportError:
    pass
