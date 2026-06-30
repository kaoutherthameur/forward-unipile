#!/usr/bin/env python3
"""E6 - "Warm touch" : visite de profil déclenchée. Récurrent (cron drip).

Consulte le profil d'une liste de cibles avec notify=true : la cible voit votre
visite dans "qui a vu votre profil" (touche douce avant outreach). La visite a un
effet visible -> traitée comme une écriture (respecte UNIPILE_DRY_RUN) + garde-fous.
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


def slug_of(linkedin):
    return linkedin.rstrip("/").split("/")[-1]


def run(cfg):
    done = 0
    cap = u.daily_cap()
    for t in cfg.get("targets", []):
        if done >= cap:
            print("Daily cap reached (%d)." % cap)
            break
        if not u.in_send_window(t.get("country")):
            print("skip (outside local window): %s" % t.get("linkedin"))
            continue
        slug = slug_of(t["linkedin"])
        u.sleep_jitter()
        # notify=true -> the visit is visible to the target. is_write so DRY_RUN simulates it.
        u.get("users/%s" % u.encode_urn(slug), params={"notify": "true"}, is_write=True)
        print("visited: %s (%s)" % (slug, "DRY_RUN" if u.dry_run() else "LIVE"))
        done += 1
    print("Done. %d profile visit(s) %s." % (done, "simulated" if u.dry_run() else "triggered"))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
