#!/usr/bin/env python3
"""G4 - Monitoring de la santé des comptes. Récurrent (service webhook).

Reçoit le webhook Unipile account_status et alerte si un compte se déconnecte ou
tombe sur un checkpoint (pour réagir vite avant que les workflows ne cassent).
Déployé comme endpoint web Modal.
"""
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

OK_STATUSES = {"OK", "CONNECTED", "SYNC_SUCCESS"}


def should_alert(payload):
    """Pure: True if the account_status event needs attention. Testable offline."""
    if payload.get("event") != "account_status":
        return False
    status = (payload.get("status") or payload.get("account_status") or "").upper()
    return status not in OK_STATUSES


def alert(payload):
    """Notify (Slack/email). Stub: prints. Wire to your channel."""
    print("ACCOUNT ALERT:", json.dumps({
        "account_id": payload.get("account_id"),
        "status": payload.get("status") or payload.get("account_status"),
    }, ensure_ascii=False))


try:
    import modal

    app = modal.App("unipile-monitoring-comptes")
    image = modal.Image.debian_slim().pip_install("fastapi")

    @app.function(image=image, secrets=[modal.Secret.from_name("unipile")])
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        if should_alert(payload):
            alert(payload)
        return {"ok": True, "alerted": should_alert(payload)}
except ImportError:
    pass
