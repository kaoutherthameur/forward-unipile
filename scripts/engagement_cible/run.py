#!/usr/bin/env python3
"""D3 - Liker/réagir à des posts ciblés (nurturing). Récurrent (cron).

Réagit à une liste de posts ciblés (entretien d'une relation sur des comptes
cibles). ÉCRITURE -> respecte UNIPILE_DRY_RUN. Garde-fous : plafond/jour, jitter.
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


def social_id_from(url_or_id):
    """Pure: derive the social_id URN from a post URL or raw id. Testable offline."""
    s = str(url_or_id)
    for kind in ("activity", "ugcPost", "share"):
        marker = kind + ":"
        if marker in s:
            return "urn:li:%s:%s" % (kind, s.split(marker, 1)[1].split("/")[0].split("-")[-1])
    if s.startswith("urn:li:"):
        return s
    # last path segment like ...-activity-<ID>-xxxx
    if "activity-" in s:
        return "urn:li:activity:" + s.split("activity-", 1)[1].split("-")[0]
    return s


def run(cfg):
    reaction = cfg.get("reaction", "LIKE")
    done = 0
    cap = u.daily_cap()
    for target in cfg.get("posts", []):
        if done >= cap:
            print("Daily cap reached (%d)." % cap)
            break
        sid = social_id_from(target)
        u.sleep_jitter()
        u.post("posts/%s/reactions" % u.encode_urn(sid), json={"value": reaction}, is_write=True)
        print("reacted %s to %s (%s)" % (reaction, sid, "DRY_RUN" if u.dry_run() else "LIVE"))
        done += 1
    print("Done. %d reaction(s) %s." % (done, "simulated" if u.dry_run() else "sent"))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
