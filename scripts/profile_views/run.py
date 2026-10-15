#!/usr/bin/env python3
"""E1 - Qui a visité mon profil LinkedIn. Récurrent (cron quotidien).

Récupère les visiteurs identifiés du profil via le proxy raw Voyager d'Unipile
(`wvmpCards`) - le seul endroit qui renvoie les NOMS des visiteurs. Lecture seule.

Porté de forward-graph ingest/linkedin_profile_views.py.
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

WVMP_URL = "https://www.linkedin.com/voyager/api/identity/wvmpCards"


def _union_items(d):
    """Yield (short_key, value) for a Voyager union dict {fqcn: value}."""
    if isinstance(d, dict):
        for k, v in d.items():
            yield k.rsplit(".", 1)[-1], v


def _union_get(d, short):
    for sk, v in _union_items(d):
        if sk == short:
            return v
    return None


def iter_profile_view_cards(payload):
    """Pure: flatten every WvmpProfileViewCard across insight packs. Testable offline."""
    elements = (payload.get("data") or {}).get("elements") or payload.get("elements") or []
    for el in elements:
        viewers_card = _union_get(el.get("value") or {}, "WvmpViewersCard")
        if not viewers_card:
            continue
        for ic in viewers_card.get("insightCards") or []:
            for _short, insight in _union_items(ic.get("value") or {}):
                if not isinstance(insight, dict):
                    continue
                for card in insight.get("cards") or []:
                    pvc = _union_get(card.get("value") or {}, "WvmpProfileViewCard")
                    if isinstance(pvc, dict):
                        yield pvc


def parse_viewer(pvc):
    """Pure: extract an identified viewer from a card. None if obfuscated/anonymous."""
    full = _union_get(pvc.get("viewer") or {}, "FullProfileViewer")
    if not isinstance(full, dict):
        return None
    profile = full.get("profile") or {}
    mini = profile.get("miniProfile") or {}
    dash = mini.get("dashEntityUrn") or mini.get("entityUrn") or ""
    provider_id = dash.rsplit(":", 1)[-1] if dash else None
    if not provider_id or not provider_id.startswith("ACo"):
        return None
    name = ("%s %s" % (mini.get("firstName", ""), mini.get("lastName", ""))).strip() or None
    slug = mini.get("publicIdentifier") or None
    insight_val = (pvc.get("insight") or {}).get("value") or {}
    cci = _union_get(insight_val, "ConnectionsInCommonInsight") or {}
    return {
        "name": name,
        "headline": mini.get("occupation") or "",
        "profile_url": ("https://www.linkedin.com/in/%s" % slug) if slug else "",
        "network_distance": (profile.get("distance") or {}).get("value", ""),
        "viewed_at_ms": pvc.get("viewedAt"),
        "connections_in_common": cci.get("numConnectionsInCommon", ""),
        "provider_id": provider_id,
    }


def viewers_from_payload(payload):
    """Pure: payload -> deduped list of identified viewers. Testable offline."""
    rows, seen = [], set()
    for pvc in iter_profile_view_cards(payload):
        v = parse_viewer(pvc)
        if not v or not v.get("viewed_at_ms"):
            continue
        key = "%s:%s" % (v["provider_id"], v["viewed_at_ms"])
        if key in seen:
            continue
        seen.add(key)
        rows.append(v)
    return rows


def run(cfg):
    payload = u.raw_voyager(WVMP_URL)
    rows = viewers_from_payload(payload)
    out = cfg.get("output_path") or "examples/profile-views.csv"
    cols = ["name", "headline", "profile_url", "network_distance", "viewed_at_ms", "connections_in_common"]
    u.write_csv(out, rows, fieldnames=cols)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
