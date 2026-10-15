#!/usr/bin/env python3
"""G2 - Enrichissement CRM automatique. Récurrent (cron).

Pour une liste de profils (ex. nouvelles entrées CRM), récupère le profil + l'entreprise
et pousse une fiche enrichie. CRM générique : point d'extension to_crm() (stub).
Lecture LinkedIn (pas d'écriture LinkedIn).
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


def enrich_record(profile, company=None):
    """Pure: build an enriched CRM record from profile (+ company). Testable offline."""
    company = company or {}
    emails = (profile.get("contact_info") or {}).get("emails") or []
    return {
        "name": ("%s %s" % (profile.get("first_name", ""), profile.get("last_name", ""))).strip(),
        "headline": profile.get("headline", ""),
        "location": profile.get("location", ""),
        "country": (profile.get("primary_locale") or {}).get("country", ""),
        "network_distance": profile.get("network_distance", ""),
        "follower_count": profile.get("follower_count", ""),
        "email": emails[0] if emails else "",
        "company": company.get("name", ""),
        "company_industry": company.get("industry", ""),
        "public_identifier": profile.get("public_identifier", ""),
    }


def to_crm(record):
    """Push to your CRM. Stub: prints. Wire to Attio/HubSpot/Sheet/etc."""
    print("CRM UPSERT:", json.dumps(record, ensure_ascii=False))


def run(cfg):
    records = []
    for slug in cfg.get("profiles", []):
        slug = slug.rstrip("/").split("/")[-1]
        profile = u.get("users/%s" % u.encode_urn(slug))
        company = None
        cid = cfg.get("with_company") and profile.get("current_company_id")
        if cid:
            company = u.get("linkedin/companies/%s" % u.encode_urn(cid))
        rec = enrich_record(profile, company)
        to_crm(rec)
        records.append(rec)
        u.sleep_jitter(1.0, 3.0)
    out = cfg.get("output_path")
    if out:
        u.write_csv(out, records)
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
