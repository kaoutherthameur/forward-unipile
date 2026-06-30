#!/usr/bin/env python3
"""B6 - Auto-accepter les invitations reçues + message de bienvenue. Récurrent (cron).

Accepte les invitations entrantes et envoie un message de bienvenue.
ÉCRITURE -> DRY_RUN. Garde-fous : plafond/jour, jitter.
"""
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from lib import unipile_helpers as u  # noqa: E402


def welcome_text(template, first_name):
    """Pure: fill the welcome message. Testable offline."""
    return template.format(first_name=first_name or "")


def run(cfg):
    template = cfg.get("welcome_template", "Merci pour la connexion {first_name} !")
    send_welcome = cfg.get("send_welcome", True)
    done = 0
    cap = u.daily_cap()
    for inv in u.paginate("users/invitations/received"):
        if done >= cap:
            print("Daily cap reached (%d)." % cap)
            break
        inv_id = inv.get("id") or inv.get("invitation_id")
        u.sleep_jitter()
        u.request("PATCH", "users/invitations/%s" % u.encode_urn(inv_id),
                  json={"action": "accept"}, is_write=True)
        if send_welcome:
            provider_id = inv.get("provider_id") or (inv.get("from") or {}).get("provider_id")
            first = inv.get("first_name") or (inv.get("from") or {}).get("first_name", "")
            u.post("chats", json={"provider_id": provider_id, "text": welcome_text(template, first)}, is_write=True)
        print("accepted: %s (%s)" % (inv_id, "DRY_RUN" if u.dry_run() else "LIVE"))
        done += 1
    print("Done. %d invitation(s) %s." % (done, "simulated" if u.dry_run() else "accepted"))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
