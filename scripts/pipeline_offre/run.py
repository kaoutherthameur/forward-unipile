#!/usr/bin/env python3
"""C5 - Gérer la pipeline d'une offre. Récurrent (cron).

Liste les candidats d'une offre LinkedIn et signale les CV disponibles.
Lecture seule (le téléchargement de CV se fait via l'URL retournée).
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


def applicant_row(a):
    """Pure: map an applicant payload to a row. Testable offline."""
    return {
        "name": a.get("name") or ("%s %s" % (a.get("first_name", ""), a.get("last_name", ""))).strip(),
        "headline": a.get("headline", ""),
        "applied_at": a.get("applied_at") or a.get("date", ""),
        "profile_url": a.get("profile_url", ""),
        "resume_available": bool(a.get("resume") or a.get("has_resume")),
        "applicant_id": a.get("id", ""),
    }


def run(cfg):
    job_id = cfg["job_id"]
    rows = [applicant_row(a) for a in u.paginate("linkedin/jobs/%s/applicants" % u.encode_urn(job_id))]
    out = cfg.get("output_path") or "examples/pipeline-offre.csv"
    u.write_csv(out, rows)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
