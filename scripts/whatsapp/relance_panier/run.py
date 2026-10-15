#!/usr/bin/env python3
"""C5 - Relance de panier / réservation abandonné. Récurrent (cron).

Un panier ou une réservation laissé en plan (événements fournis dans la config)
déclenche UN rappel unique après un délai. ÉCRITURE -> respecte UNIPILE_DRY_RUN.

Idempotence : clé stable (chat_id, event_id). Un rappel déjà envoyé n'est
jamais réémis. En prod, `already_sent` vient de votre base.
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

DEFAULT_DELAY_HOURS = 4
DEFAULT_WINDOW_HOURS = 20  # fenêtre de tir après le délai (le cron n'est pas à la seconde près)


def _parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def dedup_key(chat_id, event_id):
    """Clé stable d'idempotence : (chat_id, event_id)."""
    return "%s|%s" % (chat_id, event_id)


def eligible_for_reminder(abandoned_at, now=None, delay_hours=DEFAULT_DELAY_HOURS, window_hours=DEFAULT_WINDOW_HOURS):
    """Pure : True si l'abandon date d'au moins `delay_hours` heures sans
    dépasser la fenêtre de tir. Testable hors-ligne."""
    now = now or datetime.now(timezone.utc)
    dt = _parse_dt(abandoned_at)
    if not dt:
        return False
    age_hours = (now - dt).total_seconds() / 3600.0
    return delay_hours <= age_hours < delay_hours + window_hours


def reminders_due(events, now=None, delay_hours=DEFAULT_DELAY_HOURS, already_sent=None):
    """Pure : renvoie les rappels de panier dus, dédupliqués. Testable hors-ligne."""
    now = now or datetime.now(timezone.utc)
    already_sent = set(already_sent or [])
    due = []
    for e in events:
        if not eligible_for_reminder(e.get("abandoned_at"), now, delay_hours):
            continue
        key = dedup_key(e["chat_id"], e.get("event_id", ""))
        if key in already_sent:
            continue
        due.append({
            "chat_id": e["chat_id"],
            "country": e.get("country"),
            "message": e.get("message", ""),
            "key": key,
        })
    return due


def run(cfg):
    now = datetime.now(timezone.utc)
    delay = int(cfg.get("delay_hours", DEFAULT_DELAY_HOURS))
    sent = 0
    cap = u.daily_cap()
    for r in reminders_due(cfg.get("events", []), now, delay, cfg.get("already_sent", [])):
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        if not r["message"].strip():
            print("skip (pas de message) : %s" % r["chat_id"])
            continue
        if not u.in_send_window(r.get("country")):
            print("skip (hors fenêtre locale) : %s" % r["chat_id"])
            continue
        u.sleep_jitter()
        u.post("chats/%s/messages" % r["chat_id"], json={"text": r["message"]}, is_write=True)
        print("relance panier -> %s (%s)" % (r["chat_id"], "DRY_RUN" if u.dry_run() else "LIVE"))
        sent += 1
    print("Terminé. %d rappel(s) %s." % (sent, "simulé(s)" if u.dry_run() else "envoyé(s)"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
