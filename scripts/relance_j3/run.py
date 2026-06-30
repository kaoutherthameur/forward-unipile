#!/usr/bin/env python3
"""B3 - Relance automatique des prospects sans réponse (J+3). Récurrent (cron).

Pour chaque lead contacté il y a 3 à 7 jours et resté silencieux, envoie UNE
relance dans la conversation existante. ÉCRITURE -> respecte UNIPILE_DRY_RUN.

Anti-collision : avant de relancer, relit la conversation et vérifie qu'aucun
message entrant n'est arrivé depuis le 1er contact (le webhook a pu rater une réponse).
Porté de Melvin followup_sender.
"""
import os
import sys
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from lib import unipile_helpers as u  # noqa: E402


def _parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def due_for_followup(contacted_at, now=None, min_days=3, max_days=7):
    """Pure: True if contacted between [min_days, max_days] ago. Testable offline."""
    now = now or datetime.now(timezone.utc)
    dt = _parse_dt(contacted_at)
    if not dt:
        return False
    age_days = (now - dt).total_seconds() / 86400.0
    return min_days <= age_days <= max_days


def has_inbound_since(messages, contacted_at, our_provider_id):
    """Pure: did the prospect reply after we contacted them? Testable offline."""
    cutoff = _parse_dt(contacted_at)
    for m in messages:
        sender = (m.get("sender") or {}).get("attendee_provider_id") or m.get("sender_id")
        ts = _parse_dt(m.get("timestamp") or m.get("date"))
        if sender and sender != our_provider_id and ts and cutoff and ts > cutoff:
            return True
    return False


def run(cfg):
    our_id = cfg.get("our_provider_id", "")
    sent = 0
    cap = u.daily_cap()
    for lead in cfg.get("leads", []):
        if sent >= cap:
            print("Daily cap reached (%d)." % cap)
            break
        if not due_for_followup(lead.get("contacted_at")):
            continue
        chat_id = lead["chat_id"]
        msgs = list(u.paginate("chats/%s/messages" % chat_id, max_items=20))
        if has_inbound_since(msgs, lead.get("contacted_at"), our_id):
            print("skip (already replied): %s" % chat_id)
            continue
        if not u.in_send_window(lead.get("country")):
            print("skip (outside local window): %s" % chat_id)
            continue
        u.sleep_jitter()
        u.post("chats/%s/messages" % chat_id, json={"text": lead["message"]}, is_write=True)
        print("followed up: %s (%s)" % (chat_id, "DRY_RUN" if u.dry_run() else "LIVE"))
        sent += 1
    print("Done. %d follow-up(s) %s." % (sent, "simulated" if u.dry_run() else "sent"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
