#!/usr/bin/env python3
"""E1 - Check-in quotidien WhatsApp aux coachés (action du jour). Récurrent (cron).

Chaque matin, envoie un message de check-in à chaque coaché opt-in listé en config
("C'est fait, ton action du jour ?"). ÉCRITURE -> respecte UNIPILE_DRY_RUN.

Envois OPT-IN uniquement (coachés qui ont accepté le suivi). Compte perso :
garde-fous plafond quotidien + fenêtre locale + jitter pour rester conversationnel.
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


def build_checkin(coache, templates, now=None):
    """Pure : compose le message de check-in pour un coaché. Testable hors-ligne.

    Choisit le template selon le jour de la semaine (rotation simple pour éviter
    la répétition mot pour mot) et insère le prénom + l'action du jour.
    """
    now = now or datetime.now(timezone.utc)
    if not templates:
        templates = ["Salut {prenom}, c'est fait, ton action du jour ?"]
    tpl = templates[now.timetuple().tm_yday % len(templates)]
    return tpl.format(
        prenom=coache.get("prenom", ""),
        action=coache.get("action_du_jour", "ton action du jour"),
    )


def run(cfg):
    sent = 0
    cap = u.daily_cap()
    templates = cfg.get("templates", [])
    for coache in cfg.get("coaches", []):
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        if not u.in_send_window(coache.get("country")):
            print("skip (hors fenêtre locale) : %s" % coache.get("prenom", ""))
            continue
        message = build_checkin(coache, templates)
        u.sleep_jitter()
        u.post("chats/%s/messages" % coache["chat_id"],
               json={"text": message}, is_write=True)
        print("check-in %s -> %s : %s" % (
            "DRY_RUN" if u.dry_run() else "LIVE", coache.get("prenom", ""), message))
        sent += 1
    print("Terminé. %d check-in(s) %s." % (sent, "simulé(s)" if u.dry_run() else "envoyé(s)"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
