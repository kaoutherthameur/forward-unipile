#!/usr/bin/env python3
"""C2 - Relance douce d'un devis ou d'une facture sans réponse. Récurrent (cron).

Un devis / une facture envoyé et resté sans réponse déclenche une relance
douce à J+N. Un seul envoi par palier. ÉCRITURE -> respecte UNIPILE_DRY_RUN.

Idempotence : clé stable (chat_id, palier en jours). Un palier déjà relancé
n'est jamais réémis. En prod, `already_sent` vient de votre base.
"""
import os
import sys
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from lib import unipile_helpers as u  # noqa: E402

# Fenêtre de tir : une fois le palier atteint, on relance dans les jours qui
# suivent (le cron peut ne pas tourner pile au bon jour). La clé d'idempotence
# garantit un seul envoi par palier.
DEFAULT_WINDOW_DAYS = 2


def _parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def due_for_followup(sent_at, now=None, days=4, window_days=DEFAULT_WINDOW_DAYS):
    """Pure : True si l'envoi date d'au moins `days` jours, sans dépasser la
    fenêtre de tir. Testable hors-ligne."""
    now = now or datetime.now(timezone.utc)
    dt = _parse_dt(sent_at)
    if not dt:
        return False
    age_days = (now - dt).total_seconds() / 86400.0
    return days <= age_days < days + window_days


def dedup_key(chat_id, palier_days):
    """Clé stable d'idempotence : (chat_id, palier en jours)."""
    return "%s|J+%d" % (chat_id, palier_days)


def followups_due(quotes, now=None, already_sent=None):
    """Pure : renvoie les relances dues (un palier par devis au plus). Testable."""
    now = now or datetime.now(timezone.utc)
    already_sent = set(already_sent or [])
    due = []
    for q in quotes:
        for palier in sorted(q.get("paliers", [])):
            if not due_for_followup(q.get("sent_at"), now, palier):
                continue
            key = dedup_key(q["chat_id"], palier)
            if key in already_sent:
                continue
            due.append({
                "chat_id": q["chat_id"],
                "country": q.get("country"),
                "palier": palier,
                "message": q.get("messages", {}).get("J+%d" % palier, ""),
                "key": key,
            })
            break  # un seul palier à la fois par devis
    return due


def run(cfg):
    now = datetime.now(timezone.utc)
    sent = 0
    cap = u.daily_cap()
    for r in followups_due(cfg.get("quotes", []), now, cfg.get("already_sent", [])):
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        if not r["message"]:
            print("skip (pas de message pour J+%d) : %s" % (r["palier"], r["chat_id"]))
            continue
        if not u.in_send_window(r.get("country")):
            print("skip (hors fenêtre locale) : %s" % r["chat_id"])
            continue
        u.sleep_jitter()
        u.post("chats/%s/messages" % r["chat_id"], json={"text": r["message"]}, is_write=True)
        print("relance J+%d -> %s (%s)" % (r["palier"], r["chat_id"], "DRY_RUN" if u.dry_run() else "LIVE"))
        sent += 1
    print("Terminé. %d relance(s) %s." % (sent, "simulée(s)" if u.dry_run() else "envoyée(s)"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
