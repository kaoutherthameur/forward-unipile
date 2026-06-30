#!/usr/bin/env python3
"""G1 - Sync des nouvelles connexions dans un CRM. Récurrent (service webhook).

Reçoit le webhook Unipile new_relation (invitation acceptée / nouvelle connexion)
et crée une fiche CRM. CRM générique : point d'extension to_crm() (stub).
Déployé comme endpoint web Modal.
"""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def relation_to_contact(payload):
    """Pure: map a new_relation webhook to a CRM contact dict. Testable offline."""
    if payload.get("event") != "new_relation":
        return None
    return {
        "name": payload.get("name") or payload.get("attendee_name", ""),
        "linkedin_id": payload.get("user_id") or payload.get("provider_id", ""),
        "profile_url": payload.get("profile_url", ""),
        "source": "linkedin_new_relation",
    }


def to_crm(contact):
    """Push to your CRM. Stub: prints. Wire to Attio/HubSpot/Sheet/etc."""
    print("CRM UPSERT:", json.dumps(contact, ensure_ascii=False))


try:
    import modal

    app = modal.App("unipile-sync-connexions-crm")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        contact = relation_to_contact(payload)
        if contact:
            to_crm(contact)
        return {"ok": True, "synced": bool(contact)}
except ImportError:
    pass
