#!/usr/bin/env python3
"""C4 - Demande d'avis après une prestation. Récurrent (cron).

X jours après une prestation, envoie UNE demande de note + un lien d'avis
Google. ÉCRITURE -> respecte UNIPILE_DRY_RUN.

Idempotence : clé stable (chat_id, "avis"). Une demande déjà envoyée n'est
jamais réémise. En prod, `already_sent` vient de votre base.
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

DEFAULT_DELAY_DAYS = 3
DEFAULT_WINDOW_DAYS = 3  # fenêtre de tir après le délai (le cron n'est pas à la seconde près)


def _parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def eligible_for_review(done_at, now=None, delay_days=DEFAULT_DELAY_DAYS, window_days=DEFAULT_WINDOW_DAYS):
    """Pure : True si la prestation date d'au moins `delay_days` jours sans
    dépasser la fenêtre de tir. Testable hors-ligne."""
    now = now or datetime.now(timezone.utc)
    dt = _parse_dt(done_at)
    if not dt:
        return False
    age_days = (now - dt).total_seconds() / 86400.0
    return delay_days <= age_days < delay_days + window_days


def dedup_key(chat_id):
    """Clé stable d'idempotence : (chat_id, avis)."""
    return "%s|avis" % chat_id


def build_message(template, review_link):
    """Pure : insère le lien d'avis dans le gabarit. Testable hors-ligne."""
    return template.replace("{lien}", review_link or "")


def run(cfg):
    now = datetime.now(timezone.utc)
    already_sent = set(cfg.get("already_sent", []))
    delay = int(cfg.get("delay_days", DEFAULT_DELAY_DAYS))
    review_link = cfg.get("review_link", "")
    sent = 0
    cap = u.daily_cap()
    for p in cfg.get("prestations", []):
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        if not eligible_for_review(p.get("done_at"), now, delay):
            continue
        key = dedup_key(p["chat_id"])
        if key in already_sent:
            print("skip (déjà envoyé) : %s" % key)
            continue
        message = build_message(p.get("message", ""), p.get("review_link", review_link))
        if not message.strip():
            print("skip (pas de message) : %s" % p["chat_id"])
            continue
        if not u.in_send_window(p.get("country")):
            print("skip (hors fenêtre locale) : %s" % p["chat_id"])
            continue
        u.sleep_jitter()
        u.post("chats/%s/messages" % p["chat_id"], json={"text": message}, is_write=True)
        print("demande d'avis -> %s (%s)" % (p["chat_id"], "DRY_RUN" if u.dry_run() else "LIVE"))
        sent += 1
    print("Terminé. %d demande(s) %s." % (sent, "simulée(s)" if u.dry_run() else "envoyée(s)"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
