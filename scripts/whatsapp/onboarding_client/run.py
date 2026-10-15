#!/usr/bin/env python3
"""C3 - Séquence d'onboarding post-achat. Récurrent (cron).

Après un achat, déroule une séquence : J0 (bienvenue), J+2 (conseil), J+7
(check). Un message par jour dû. ÉCRITURE -> respecte UNIPILE_DRY_RUN.

Idempotence : clé stable (client, étape). Une étape déjà envoyée n'est jamais
réémise. En prod, `already_sent` vient de votre base.
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

# Séquence par défaut : (libellé, jour depuis l'achat).
DEFAULT_STEPS = [
    {"label": "J0", "day": 0},
    {"label": "J+2", "day": 2},
    {"label": "J+7", "day": 7},
]


def _parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def step_due(signup_at, now=None, steps=None):
    """Pure : renvoie l'étape à envoyer aujourd'hui (ou None). Testable hors-ligne.

    Une étape est due le jour où l'âge du client (en jours entiers) atteint le
    jour de l'étape. Au plus une étape par jour.
    """
    now = now or datetime.now(timezone.utc)
    steps = steps or DEFAULT_STEPS
    dt = _parse_dt(signup_at)
    if not dt or now < dt:
        return None
    age_days = int((now - dt).total_seconds() // 86400)
    for step in steps:
        if step["day"] == age_days:
            return step
    return None


def dedup_key(client_id, step_label):
    """Clé stable d'idempotence : (client, étape)."""
    return "%s|%s" % (client_id, step_label)


def run(cfg):
    now = datetime.now(timezone.utc)
    already_sent = set(cfg.get("already_sent", []))
    sent = 0
    cap = u.daily_cap()
    for client in cfg.get("clients", []):
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        step = step_due(client.get("signup_at"), now)
        if not step:
            continue
        key = dedup_key(client["client_id"], step["label"])
        if key in already_sent:
            print("skip (déjà envoyé) : %s" % key)
            continue
        message = client.get("messages", {}).get(step["label"], "")
        if not message:
            print("skip (pas de message pour %s) : %s" % (step["label"], client["client_id"]))
            continue
        if not u.in_send_window(client.get("country")):
            print("skip (hors fenêtre locale) : %s" % client["chat_id"])
            continue
        u.sleep_jitter()
        u.post("chats/%s/messages" % client["chat_id"], json={"text": message}, is_write=True)
        print("onboarding %s -> %s (%s)" % (step["label"], client["chat_id"], "DRY_RUN" if u.dry_run() else "LIVE"))
        sent += 1
    print("Terminé. %d message(s) %s." % (sent, "simulé(s)" if u.dry_run() else "envoyé(s)"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
