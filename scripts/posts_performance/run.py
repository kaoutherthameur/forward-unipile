#!/usr/bin/env python3
"""D4 - Performance de vos posts LinkedIn. Récurrent (cron quotidien).

Pour chaque post récent du compte : impressions, réactions, commentaires,
reposts, + analytics (visiteurs de profil et followers générés par ce post).
Snapshot CSV daté. Lecture seule (aucune écriture).

Porté de forward-graph (capture_metrics / W3).
"""
import os
import sys
import argparse
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dotenv import load_dotenv  # noqa: E402
load_dotenv()
from lib import unipile_helpers as u  # noqa: E402


def metrics_row(post, captured_at):
    """Pure: map a Unipile Post payload to a metrics row. Testable offline."""
    analytics = post.get("analytics") or {}
    return {
        "captured_at": captured_at,
        "social_id": post.get("social_id") or post.get("id"),
        "share_url": post.get("share_url", ""),
        "text_preview": (post.get("text", "") or "").replace("\n", " ")[:80],
        "impressions": post.get("impressions_counter", 0),
        "reactions": post.get("reaction_counter", 0),
        "comments": post.get("comment_counter", 0),
        "reposts": post.get("repost_counter", 0),
        "profile_viewers_from_post": analytics.get("profile_viewers_from_this_post", 0),
        "followers_gained_from_post": analytics.get("followers_gained_from_this_post", 0),
    }


def run(cfg):
    identifier = cfg.get("identifier") or u.get("users/me").get("public_identifier")
    days = int(cfg.get("days_window", 21))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    rows = []
    for post in u.paginate("users/%s/posts" % u.encode_urn(identifier), max_items=cfg.get("max_posts", 50)):
        dt = post.get("parsed_datetime")
        if dt and datetime.fromisoformat(dt.replace("Z", "+00:00")) < cutoff:
            break  # posts are newest-first; stop past the window
        social_id = post.get("social_id") or post.get("id")
        detail = u.get("posts/%s" % u.encode_urn(social_id))
        rows.append(metrics_row(detail, captured_at))
        u.sleep_jitter(1.0, 3.0)

    out = cfg.get("output_path") or "examples/posts-performance.csv"
    u.write_csv(out, rows)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
