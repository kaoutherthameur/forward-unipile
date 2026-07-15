#!/usr/bin/env python3
"""C1 - Rappel de RDV à J-1 et H-2 avant un rendez-vous. Récurrent (cron).

Pour chaque rendez-vous à venir, envoie UN rappel la veille (J-1) puis UN
rappel deux heures avant (H-2). Réduit le no-show. ÉCRITURE -> respecte
UNIPILE_DRY_RUN.

Idempotence : clé stable (chat_id, étape, jour de l'étape). Une étape déjà
envoyée n'est jamais réémise. En prod, `already_sent` est alimenté par votre
base (les clés déjà traitées) ; ici il vient de la config pour l'exemple.
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

# Étapes de rappel : (libellé, heures avant le RDV, fenêtre de tir en heures).
# La fenêtre absorbe le fait qu'un cron ne tourne pas à la seconde près ; la
# clé d'idempotence garantit malgré tout un seul envoi par étape.
DEFAULT_STEPS = [
    {"label": "J-1", "hours_before": 24, "window_hours": 12},
    {"label": "H-2", "hours_before": 2, "window_hours": 2},
]


def _parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def dedup_key(chat_id, step_label, step_time):
    """Clé stable d'idempotence : (chat_id, étape, jour de l'étape)."""
    return "%s|%s|%s" % (chat_id, step_label, step_time.date().isoformat())


def reminders_due(appointments, now=None, steps=None, already_sent=None):
    """Pure : renvoie les rappels dus maintenant. Testable hors-ligne.

    Un rappel est dû si l'on vient de passer l'instant cible (starts_at moins
    hours_before) sans dépasser la fenêtre de tir, et si sa clé n'a pas déjà
    été envoyée. Un RDV déjà passé n'émet plus rien.
    """
    now = now or datetime.now(timezone.utc)
    steps = steps or DEFAULT_STEPS
    already_sent = set(already_sent or [])
    due = []
    for appt in appointments:
        starts_at = _parse_dt(appt.get("starts_at"))
        if not starts_at or starts_at <= now:
            continue
        for step in steps:
            target = starts_at - _hours(step["hours_before"])
            elapsed_h = (now - target).total_seconds() / 3600.0
            if not (0 <= elapsed_h < step["window_hours"]):
                continue
            key = dedup_key(appt["chat_id"], step["label"], target)
            if key in already_sent:
                continue
            due.append({
                "chat_id": appt["chat_id"],
                "country": appt.get("country"),
                "step": step["label"],
                "message": appt.get("messages", {}).get(step["label"], ""),
                "key": key,
            })
    return due


def _hours(n):
    from datetime import timedelta
    return timedelta(hours=n)


def run(cfg):
    now = datetime.now(timezone.utc)
    sent = 0
    cap = u.daily_cap()
    due = reminders_due(cfg.get("appointments", []), now,
                        already_sent=cfg.get("already_sent", []))
    for r in due:
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        if not r["message"]:
            print("skip (pas de message pour %s) : %s" % (r["step"], r["chat_id"]))
            continue
        if not u.in_send_window(r.get("country")):
            print("skip (hors fenêtre locale) : %s" % r["chat_id"])
            continue
        u.sleep_jitter()
        u.post("chats/%s/messages" % r["chat_id"], json={"text": r["message"]}, is_write=True)
        print("rappel %s -> %s (%s)" % (r["step"], r["chat_id"], "DRY_RUN" if u.dry_run() else "LIVE"))
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
