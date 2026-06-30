#!/usr/bin/env python3
"""B1 - Invitation automatique de votre cible. Récurrent (cron quotidien).

À partir d'une liste de cibles (slugs/URLs LinkedIn, ou export d'une recherche),
envoie un drip quotidien d'invitations + note personnalisée, dans la limite
des garde-fous anti-ban. ÉCRITURE -> respecte UNIPILE_DRY_RUN (simulé par défaut).

Garde-fous (portés de Melvin tools/unipile.py) :
  - plafond quotidien (UNIPILE_DAILY_CAP, défaut 25)
  - fenêtre horaire locale [07:30-19:30] du prospect
  - espacement aléatoire entre envois (jitter)
  - les 1er degré (déjà connectés) sont ignorés
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


def render_note(template, target):
    """Pure: fill the note template with target fields. Testable offline.

    LinkedIn invitation notes are capped at 300 chars; we truncate defensively.
    """
    note = template.format(
        first_name=target.get("first_name", ""),
        company=target.get("company", ""),
    )
    return note[:300]


def already_connected(profile):
    """Pure: a 1st-degree connection doesn't need an invitation."""
    dist = (profile.get("network_distance") or "").upper()
    return dist in ("FIRST_DEGREE", "DISTANCE_1") or bool(profile.get("is_relationship"))


def run(cfg):
    template = cfg.get("note_template", "Bonjour {first_name}, ravi de se connecter !")
    targets = cfg.get("targets", [])
    sent = 0
    cap = u.daily_cap()
    for t in targets:
        if sent >= cap:
            print("Daily cap reached (%d). Remaining queued for next run." % cap)
            break
        slug = t["linkedin"].rstrip("/").split("/")[-1]
        profile = u.get("users/%s" % u.encode_urn(slug))
        if already_connected(profile):
            print("skip (already 1st degree): %s" % slug)
            continue
        country = (profile.get("primary_locale") or {}).get("country") or t.get("country")
        if not u.in_send_window(country):
            print("skip (outside local send window): %s" % slug)
            continue
        provider_id = profile.get("provider_id")
        note = render_note(template, {**t, "first_name": profile.get("first_name", t.get("first_name", ""))})
        u.sleep_jitter()
        u.post("users/invite", json={"provider_id": provider_id, "message": note}, is_write=True)
        print("invited: %s (%s)" % (slug, "DRY_RUN" if u.dry_run() else "LIVE"))
        sent += 1
    print("Done. %d invitation(s) %s." % (sent, "simulated" if u.dry_run() else "sent"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
