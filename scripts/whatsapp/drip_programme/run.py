#!/usr/bin/env python3
"""E3 - Drip d'un programme de coaching WhatsApp (un module/exercice par jour). Récurrent (cron).

Chaque jour, délivre à chaque coaché le module correspondant à son avancement dans
le programme (jour 1, 2, ... N depuis sa date de démarrage). Pièce jointe possible.
ÉCRITURE -> respecte UNIPILE_DRY_RUN.

Idempotence sur (coaché, jour) : un journal local évite de renvoyer deux fois le
même module si le cron tourne plusieurs fois dans la journée.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from lib import unipile_helpers as u  # noqa: E402


def _parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def day_index(start_at, now=None):
    """Pure : numéro de jour (1-based) depuis le démarrage. Testable hors-ligne.

    Jour du démarrage = 1. Retourne None si la date est invalide ou future.
    """
    now = now or datetime.now(timezone.utc)
    start = _parse_dt(start_at)
    if not start:
        return None
    delta_days = (now.date() - start.date()).days
    if delta_days < 0:
        return None
    return delta_days + 1


def module_for_day(start_at, now, modules):
    """Pure : renvoie le module du jour (dict) ou None si hors programme. Testable hors-ligne.

    `modules` est une liste ordonnée (jour 1 = index 0). Au-delà de la longueur,
    le programme est terminé -> None.
    """
    idx = day_index(start_at, now)
    if idx is None or idx < 1 or idx > len(modules):
        return None
    return modules[idx - 1]


def _load_sent(path):
    if not path or not os.path.exists(path):
        return set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except (ValueError, OSError):
        return set()


def _save_sent(path, sent_keys):
    if not path:
        return
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sorted(sent_keys), f, ensure_ascii=False, indent=2)


def run(cfg, now=None):
    now = now or datetime.now(timezone.utc)
    modules = cfg.get("modules", [])
    state_path = cfg.get("state_path", "")
    already = _load_sent(state_path)
    sent = 0
    cap = u.daily_cap()
    for coache in cfg.get("coaches", []):
        if sent >= cap:
            print("Plafond quotidien atteint (%d)." % cap)
            break
        mod = module_for_day(coache.get("start_at"), now, modules)
        if mod is None:
            print("skip (hors programme) : %s" % coache.get("prenom", ""))
            continue
        key = "%s:%s" % (coache["chat_id"], mod.get("jour", ""))
        if key in already:
            print("skip (déjà envoyé aujourd'hui) : %s" % key)
            continue
        if not u.in_send_window(coache.get("country")):
            print("skip (hors fenêtre locale) : %s" % coache.get("prenom", ""))
            continue
        message = "%s\n\n%s" % (mod.get("titre", ""), mod.get("texte", ""))
        body = {"text": message}
        if mod.get("attachment_url"):
            body["attachments"] = [mod["attachment_url"]]
        u.sleep_jitter()
        u.post("chats/%s/messages" % coache["chat_id"], json=body, is_write=True)
        print("module J%s %s -> %s : %s" % (
            mod.get("jour", "?"), "DRY_RUN" if u.dry_run() else "LIVE",
            coache.get("prenom", ""), mod.get("titre", "")))
        already.add(key)
        sent += 1
    _save_sent(state_path, already)
    print("Terminé. %d module(s) %s." % (sent, "simulé(s)" if u.dry_run() else "envoyé(s)"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
