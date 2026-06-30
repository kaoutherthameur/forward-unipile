#!/usr/bin/env python3
"""A5 - Social listening : posts LinkedIn sur un mot-clé. Récurrent (cron).

Recherche les posts récents correspondant à des mots-clés et produit un CSV
(repérer qui parle d'un sujet -> prospects à engager). Lecture seule.
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


def post_row(hit):
    """Pure: map a post search hit to a row. Testable offline."""
    author = hit.get("author") or {}
    if isinstance(author, str):
        author = {"name": author}
    return {
        "author": author.get("name", ""),
        "author_url": author.get("profile_url", ""),
        "date": hit.get("date", ""),
        "text_preview": " ".join((hit.get("text", "") or "").split())[:160],
        "reactions": hit.get("reaction_counter", 0),
        "comments": hit.get("comment_counter", 0),
        "post_url": hit.get("share_url") or hit.get("url", ""),
    }


def run(cfg):
    body = {"api": cfg.get("api", "classic"), "category": "posts",
            "keywords": cfg.get("keywords", "")}
    rows = []
    limit = int(cfg.get("limit", 50))
    cursor = None
    while len(rows) < limit:
        params = {"limit": min(50, limit - len(rows))}
        if cursor:
            params["cursor"] = cursor
        res = u.post("linkedin/search", params=params, json=body)
        items = res.get("items") or res.get("data") or []
        rows.extend(post_row(h) for h in items)
        cursor = res.get("cursor") or (res.get("paging") or {}).get("cursor")
        if not cursor or not items:
            break
    out = cfg.get("output_path") or "examples/social-listening.csv"
    u.write_csv(out, rows)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
