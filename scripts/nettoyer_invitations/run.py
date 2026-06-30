#!/usr/bin/env python3
"""B5 - Nettoyer les invitations en attente. Récurrent (cron hebdo).

Retire (withdraw) les invitations envoyées depuis plus de N jours et toujours
en attente, pour libérer le quota hebdomadaire LinkedIn. ÉCRITURE -> DRY_RUN.
"""
import os
import sys
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from lib import unipile_helpers as u  # noqa: E402


def _to_dt(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):  # epoch ms
        return datetime.fromtimestamp(val / 1000.0, tz=timezone.utc)
    try:
        return datetime.fromisoformat(str(val).replace("Z", "+00:00"))
    except ValueError:
        return None


def is_stale(sent_at, days, now=None):
    """Pure: True if the invitation is older than `days`. Testable offline."""
    now = now or datetime.now(timezone.utc)
    dt = _to_dt(sent_at)
    if not dt:
        return False
    return (now - dt).total_seconds() / 86400.0 >= days


def run(cfg):
    days = int(cfg.get("older_than_days", 21))
    withdrawn = 0
    for inv in u.paginate("users/invitations/sent"):
        sent_at = inv.get("sent_at") or inv.get("created_at") or inv.get("date")
        if not is_stale(sent_at, days):
            continue
        inv_id = inv.get("id") or inv.get("invitation_id")
        u.request("DELETE", "users/invite/%s" % u.encode_urn(inv_id), is_write=True)
        print("withdrawn: %s (%s)" % (inv_id, "DRY_RUN" if u.dry_run() else "LIVE"))
        withdrawn += 1
    print("Done. %d invitation(s) %s." % (withdrawn, "simulated" if u.dry_run() else "withdrawn"))
    return withdrawn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
