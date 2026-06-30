#!/usr/bin/env python3
"""D5 - Veille de contenu d'un concurrent / influenceur. Récurrent (cron).

Récupère les posts récents d'un profil cible et produit un digest markdown
(accroche + engagement de chaque post). Lecture seule.

Porté de forward-graph (sync_posts / W1).
"""
import os
import sys
import argparse
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from lib import unipile_helpers as u  # noqa: E402


def _preview(text, n=160):
    return " ".join((text or "").split())[:n]


def digest_markdown(posts, identifier, days):
    """Pure: render a list of Post payloads into a markdown digest. Testable offline."""
    lines = ["# Veille contenu - %s" % identifier,
             "_Posts des %d derniers jours - %d post(s)_" % (days, len(posts)), ""]
    for p in posts:
        eng = "👁 %s · 👍 %s · 💬 %s · 🔁 %s" % (
            p.get("impressions_counter", 0), p.get("reaction_counter", 0),
            p.get("comment_counter", 0), p.get("repost_counter", 0))
        lines.append("## %s" % (p.get("date", "?")))
        lines.append(eng)
        lines.append("")
        lines.append("> " + _preview(p.get("text", "")))
        url = p.get("share_url")
        if url:
            lines.append("")
            lines.append("[Voir le post](%s)" % url)
        lines.append("")
    return "\n".join(lines)


def run(cfg):
    identifier = cfg["identifier"]
    days = int(cfg.get("days_window", 30))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    posts = []
    for p in u.paginate("users/%s/posts" % u.encode_urn(identifier), max_items=cfg.get("max_posts", 30)):
        dt = p.get("parsed_datetime")
        if dt and datetime.fromisoformat(dt.replace("Z", "+00:00")) < cutoff:
            break
        posts.append(p)
    out = cfg.get("output_path") or "examples/veille-concurrent.md"
    u.write_output(out, digest_markdown(posts, identifier, days))
    return posts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
