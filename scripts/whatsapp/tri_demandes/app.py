#!/usr/bin/env python3
"""A3 - Classer chaque message WhatsApp (SAV / commande / réservation / spam) et router. Récurrent (webhook message_received)."""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))


def own_ids():
    raw = os.environ.get("UNIPILE_OWN_PROVIDER_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def classify(text):
    """Pure : catégorise un message sur mots-clés. Testable hors-ligne.

    Retourne l'une de : "sav", "commande", "reservation", "spam", "autre".
    """
    t = (text or "").lower()
    if any(k in t for k in ("gagné", "gagne", "loterie", "crypto", "bitcoin", "cliquez ici", "http://", "https://bit")):
        return "spam"
    if any(k in t for k in ("réserv", "reserv", "table", "rendez-vous", "rdv", "créneau", "creneau", "booking")):
        return "reservation"
    if any(k in t for k in ("commande", "livraison", "colis", "suivi", "expédi", "expedi", "facture")):
        return "commande"
    if any(k in t for k in ("problème", "probleme", "panne", "cassé", "casse", "sav", "garantie", "retour", "remboursement", "défectueux", "defectueux")):
        return "sav"
    return "autre"


def process_event(payload, our_provider_ids):
    """Pure : classe et prépare le routage. Testable hors-ligne."""
    if payload.get("event") != "message_received":
        return {"action": "ignore", "reason": "not a message_received event"}
    sender = (payload.get("sender") or {}).get("attendee_provider_id")
    if sender and sender in our_provider_ids:
        return {"action": "ignore", "reason": "message sortant (de nous)"}
    categorie = classify(payload.get("message", ""))
    return {"action": "route", "categorie": categorie,
            "chat_id": payload.get("chat_id", ""),
            "sender_name": (payload.get("sender") or {}).get("attendee_name", ""),
            "text": payload.get("message", "")}


def route_to(categorie, chat_id, sender_name, text):
    """Stub : print. À câbler (file SAV, outil commandes, agenda, corbeille spam)."""
    print("ROUTAGE [%s]:" % categorie, json.dumps(
        {"chat_id": chat_id, "sender_name": sender_name, "text": text}, ensure_ascii=False))


try:
    import modal

    app = modal.App("whatsapp-tri_demandes")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        result = process_event(payload, own_ids())
        if result["action"] == "route":
            route_to(result["categorie"], result["chat_id"],
                     result["sender_name"], result["text"])
        return {"ok": True, "action": result["action"],
                "categorie": result.get("categorie")}
except ImportError:
    pass
