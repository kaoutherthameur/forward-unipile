#!/usr/bin/env python3
"""E5 - Rappel de l'exercice du jour + demande de preuve (photo/audio). Récurrent (cron).

Chaque jour, rappelle à chaque coaché son exercice et lui demande d'envoyer une
preuve (photo ou note vocale). ÉCRITURE -> respecte UNIPILE_DRY_RUN.

La RÉCEPTION de la pièce jointe (photo/audio) n'est pas gérée ici : elle arrive via
webhook `message_received` (voir E2 accountability et A1/inbox temps réel). Ce script
ne fait que la relance sortante.
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


def build_proof_request(coache, preuve_type="photo"):
    """Pure : compose la demande de preuve pour un coaché. Testable hors-ligne.

    `preuve_type` : "photo", "audio" ou "photo_ou_audio". Insère le prénom et l'exercice.
    """
    prenom = coache.get("prenom", "")
    exercice = coache.get("exercice_du_jour", "ton exercice du jour")
    demande = {
        "photo": "Envoie-moi une photo pour prouver que c'est fait.",
        "audio": "Envoie-moi une note vocale de 30 secondes pour me raconter.",
        "photo_ou_audio": "Envoie-moi une photo ou une note vocale pour me montrer.",
    }.get(preuve_type, "Envoie-moi une preuve (photo ou vocal).")
    return "Salut %s ! L'exercice du jour : %s. %s" % (prenom, exercice, demande)


def run(cfg):
    sent = 0
    cap = u.daily_cap()
    default_type = cfg.get("preuve_type", "photo_ou_audio")
    for coache in cfg.get("coaches", []):
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        if not u.in_send_window(coache.get("country")):
            print("skip (hors fenêtre locale) : %s" % coache.get("prenom", ""))
            continue
        message = build_proof_request(coache, coache.get("preuve_type", default_type))
        u.sleep_jitter()
        u.post("chats/%s/messages" % coache["chat_id"],
               json={"text": message}, is_write=True)
        print("demande de preuve %s -> %s : %s" % (
            "DRY_RUN" if u.dry_run() else "LIVE", coache.get("prenom", ""), message))
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
