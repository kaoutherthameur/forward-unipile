#!/usr/bin/env python3
"""C2 - Entreprises qui recrutent un poste cible. Récurrent (cron hebdo).

Recherche les offres d'emploi LinkedIn correspondant à des mots-clés/lieux et
produit un CSV de signaux (entreprise + offre) - utile en prospection
("ils structurent") ou en veille RH. Lecture seule.

Variante native Unipile du job-signal de Melvin (qui passait par Apify).
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


def job_row(job):
    """Pure: map a LinkedIn job search hit to a signal row. Testable offline."""
    company = job.get("company") or job.get("company_name") or ""
    if isinstance(company, dict):
        company = company.get("name", "")
    return {
        "job_title": job.get("title") or job.get("name", ""),
        "company": company,
        "location": job.get("location", ""),
        "posted_at": job.get("posted_at") or job.get("date", ""),
        "job_url": job.get("url") or job.get("share_url", ""),
    }


def run(cfg):
    body = {"api": cfg.get("api", "classic"), "category": "jobs",
            "keywords": cfg.get("keywords", "")}
    if cfg.get("location"):
        body["location"] = cfg["location"]
    rows = []
    limit = int(cfg.get("limit", 50))
    # search endpoint is POST; paginate by re-requesting with cursor
    cursor = None
    while len(rows) < limit:
        params = {"limit": min(50, limit - len(rows))}
        if cursor:
            params["cursor"] = cursor
        res = u.post("linkedin/search", params=params, json=body)
        items = res.get("items") or res.get("data") or []
        rows.extend(job_row(j) for j in items)
        cursor = res.get("cursor") or (res.get("paging") or {}).get("cursor")
        if not cursor or not items:
            break
    out = cfg.get("output_path") or "examples/entreprises-qui-recrutent.csv"
    u.write_csv(out, rows)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
