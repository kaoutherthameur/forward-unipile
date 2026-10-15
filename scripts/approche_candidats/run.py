#!/usr/bin/env python3
"""C3 - Approche candidats automatisée. Récurrent (cron).

Pour chaque candidat ciblé : invitation + note, ou InMail Recruiter si hors réseau.
ÉCRITURE -> DRY_RUN. Garde-fous : plafond/jour, fenêtre locale, jitter.
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


def render(template, candidate):
    """Pure: fill the outreach template. Testable offline."""
    return template.format(first_name=candidate.get("first_name", ""),
                           role=candidate.get("role", "")) [:300]


def run(cfg):
    note_tpl = cfg.get("note_template", "Bonjour {first_name}, un poste de {role} pourrait vous intéresser.")
    use_inmail = cfg.get("use_inmail", False)
    done = 0
    cap = u.daily_cap()
    for c in cfg.get("candidates", []):
        if done >= cap:
            print("Daily cap reached (%d)." % cap)
            break
        slug = c["linkedin"].rstrip("/").split("/")[-1]
        if not u.in_send_window(c.get("country")):
            print("skip (outside local window): %s" % slug)
            continue
        msg = render(note_tpl, c)
        u.sleep_jitter()
        if use_inmail:
            u.post("chats", json={"inmail": True, "recipient_slug": slug,
                                  "linkedin_api": "recruiter", "text": msg}, is_write=True)
            print("inmail: %s (%s)" % (slug, "DRY_RUN" if u.dry_run() else "LIVE"))
        else:
            prof = u.get("users/%s" % u.encode_urn(slug))
            u.post("users/invite", json={"provider_id": prof.get("provider_id"), "message": msg}, is_write=True)
            print("invited: %s (%s)" % (slug, "DRY_RUN" if u.dry_run() else "LIVE"))
        done += 1
    print("Done. %d candidate outreach %s." % (done, "simulated" if u.dry_run() else "sent"))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
