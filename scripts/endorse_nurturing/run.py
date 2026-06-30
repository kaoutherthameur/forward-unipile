#!/usr/bin/env python3
"""E5 - Recommander des compétences (endorse) en nurturing. Récurrent (cron).

Endosse des compétences de contacts cibles (entretien relationnel léger).
ÉCRITURE -> respecte UNIPILE_DRY_RUN. Garde-fous : plafond/jour, jitter.
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


def run(cfg):
    sent = 0
    cap = u.daily_cap()
    for t in cfg.get("targets", []):
        if sent >= cap:
            print("Daily cap reached (%d)." % cap)
            break
        skill_id = t.get("skill_id")
        if not skill_id:
            print("skip (no skill_id): %s" % t.get("member"))
            continue
        u.sleep_jitter()
        u.post("linkedin/skills/%s/endorse" % u.encode_urn(skill_id), is_write=True)
        print("endorsed: %s skill=%s (%s)" % (t.get("member"), skill_id, "DRY_RUN" if u.dry_run() else "LIVE"))
        sent += 1
    print("Done. %d endorsement(s) %s." % (sent, "simulated" if u.dry_run() else "sent"))
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
