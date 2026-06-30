#!/usr/bin/env python3
"""B2 - Séquence invitation -> message. Récurrent (cron quotidien).

Séquence stateful : invite la cible, attend l'acceptation (détectée au degré de
connexion), puis envoie le 1er message. État minimal dans un fichier JSON local.
ÉCRITURE -> DRY_RUN. Garde-fous : plafond/jour, fenêtre locale, jitter.
"""
import os
import sys
import json
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from lib import unipile_helpers as u  # noqa: E402


def next_action(entry, is_connected):
    """Pure: decide the next step for a target. Testable offline.

    Returns 'invite' | 'message' | 'wait' | 'done'.
    """
    status = entry.get("status", "new")
    if status == "new":
        return "invite"
    if status == "invited":
        return "message" if is_connected else "wait"
    if status == "messaged":
        return "done"
    return "done"


def load_state(path, targets):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {t["linkedin"].rstrip("/").split("/")[-1]: {"linkedin": t["linkedin"],
            "first_name": t.get("first_name", ""), "status": "new"} for t in targets}


def save_state(path, state):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def run(cfg):
    state_path = cfg.get("state_path", "scripts/sequence_invitation_message/state.local.json")
    state = load_state(state_path, cfg.get("targets", []))
    invite_note = cfg.get("invite_note", "Bonjour {first_name}, ravi de se connecter.")
    first_message = cfg.get("first_message", "Merci pour la connexion {first_name} !")
    cap = u.daily_cap()
    acted = 0
    for slug, entry in state.items():
        if acted >= cap:
            break
        prof = u.get("users/%s" % u.encode_urn(slug))
        connected = (prof.get("network_distance") in ("FIRST_DEGREE", "DISTANCE_1")) or bool(prof.get("is_relationship"))
        action = next_action(entry, connected)
        fn = prof.get("first_name") or entry.get("first_name", "")
        if action == "invite":
            u.sleep_jitter()
            u.post("users/invite", json={"provider_id": prof.get("provider_id"),
                                         "message": invite_note.format(first_name=fn)[:300]}, is_write=True)
            entry["status"] = "invited"; acted += 1
            print("invited: %s (%s)" % (slug, "DRY_RUN" if u.dry_run() else "LIVE"))
        elif action == "message":
            u.sleep_jitter()
            u.post("chats", json={"provider_id": prof.get("provider_id"),
                                  "text": first_message.format(first_name=fn)}, is_write=True)
            entry["status"] = "messaged"; acted += 1
            print("messaged: %s (%s)" % (slug, "DRY_RUN" if u.dry_run() else "LIVE"))
        else:
            print("%s: %s" % (slug, action))
    save_state(state_path, state)
    print("Done. %d action(s) %s." % (acted, "simulated" if u.dry_run() else "executed"))
    return acted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
