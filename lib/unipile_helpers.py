"""Shared REST client + anti-ban guardrails for the Unipile LinkedIn API.

Ported from proven production code (forward-graph ingest + Melvin tools/unipile.py).
Third-party deps (httpx, pyyaml) are imported lazily so this module imports cleanly
for structural checks even before `pip install -r requirements.txt`.

Env (via .env / python-dotenv):
    UNIPILE_DSN          e.g. apiXX.unipile.com:NNNN  (host[:port] of your Unipile node)
    UNIPILE_API_KEY      your Unipile API key (header X-API-KEY)
    UNIPILE_ACCOUNT_ID   the account_id of the connected LinkedIn account
    UNIPILE_DRY_RUN      "1" (default) = simulate writes; "0" = perform real writes
    UNIPILE_DAILY_CAP    max write actions / day / account (default 25)

Conventions (Unipile API):
    - Header X-API-KEY on every call, `account_id` query param on every call.
    - URN path values must be percent-encoded (use encode_urn()).
    - Pagination is cursor-based via the `cursor` field in the response.
"""

import os
import csv
import time
import random
import urllib.parse
from datetime import datetime, timezone

# ----- config -------------------------------------------------------------

DEFAULT_DAILY_CAP = 25
SEND_WINDOW_START = (7, 30)   # 07:30 local
SEND_WINDOW_END = (19, 30)    # 19:30 local

# Approx country -> UTC offset (hours) for the local send-window guardrail.
# Coarse on purpose (no DST): a send-window guard, not a clock. Extend as needed.
_COUNTRY_UTC_OFFSET = {
    "FR": 1, "BE": 1, "DE": 1, "ES": 1, "IT": 1, "NL": 1, "CH": 1,
    "GB": 0, "UK": 0, "PT": 0, "IE": 0,
    "US": -5, "CA": -5, "BR": -3,
    "AE": 4, "IN": 5, "SG": 8, "KR": 9, "JP": 9, "AU": 10,
}
_DEFAULT_COUNTRY = "FR"


def _env(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        raise RuntimeError(
            "Missing env var %s. Copy .env.example to .env and fill it in." % name
        )
    return val


def dry_run():
    """Writes are simulated by default. Set UNIPILE_DRY_RUN=0 to go live."""
    return _env("UNIPILE_DRY_RUN", "1") not in ("0", "false", "False", "")


def daily_cap():
    try:
        return int(_env("UNIPILE_DAILY_CAP", str(DEFAULT_DAILY_CAP)))
    except ValueError:
        return DEFAULT_DAILY_CAP


def _base_url():
    dsn = _env("UNIPILE_DSN", required=True)
    return "https://%s/api/v1" % dsn.rstrip("/")


def _headers():
    return {
        "X-API-KEY": _env("UNIPILE_API_KEY", required=True),
        "accept": "application/json",
        "content-type": "application/json",
    }


def account_id():
    return _env("UNIPILE_ACCOUNT_ID", required=True)


# ----- HTTP ---------------------------------------------------------------

def encode_urn(value):
    """Percent-encode a URN for use in a path, e.g. urn:li:activity:123 -> urn%3Ali%3A..."""
    return urllib.parse.quote(str(value), safe="")


def request(method, path, params=None, json=None, is_write=False, timeout=30):
    """Call the Unipile API. `account_id` is injected automatically.

    Writes (is_write=True) are skipped when dry_run() is on: a simulated payload
    is returned instead of hitting LinkedIn. This is the default safety mode.
    """
    import httpx  # lazy

    params = dict(params or {})
    params.setdefault("account_id", account_id())
    url = "%s/%s" % (_base_url(), path.lstrip("/"))

    if is_write and dry_run():
        print("[DRY_RUN] %s %s params=%s json=%s" % (method, path, params, json))
        return {"dry_run": True, "method": method, "path": path,
                "params": params, "json": json}

    with httpx.Client(timeout=timeout) as client:
        resp = client.request(method, url, headers=_headers(), params=params, json=json)
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return {}


def get(path, params=None, **kw):
    return request("GET", path, params=params, **kw)


def post(path, params=None, json=None, is_write=False, **kw):
    return request("POST", path, params=params, json=json, is_write=is_write, **kw)


def paginate(path, params=None, page_limit=100, max_items=None):
    """Yield items across cursor-based pages. Stops at max_items if set.

    Handles both top-level `cursor` and `paging.cursor` shapes seen in the API.
    """
    params = dict(params or {})
    params.setdefault("limit", page_limit)
    seen = 0
    cursor = None
    while True:
        if cursor:
            params["cursor"] = cursor
        data = get(path, params=params)
        items = data.get("items") or data.get("data") or []
        for it in items:
            yield it
            seen += 1
            if max_items and seen >= max_items:
                return
        cursor = data.get("cursor") or (data.get("paging") or {}).get("cursor")
        if not cursor or not items:
            return


def raw_voyager(request_url, method="GET", headers=None):
    """Proxy an internal LinkedIn (Voyager) endpoint via Unipile getRawData.

    Used for data not exposed by standard endpoints (e.g. profile viewers /
    wvmpCards). Ported from forward-graph linkedin_profile_views.
    """
    body = {
        "account_id": account_id(),
        "request_url": request_url,
        "method": method,
        "headers": headers or {"x-restli-protocol-version": "2.0.0"},
    }
    return post("linkedin", json=body)


# ----- anti-ban guardrails ------------------------------------------------

def sleep_jitter(min_s=2.0, max_s=6.0):
    """Random pause between actions. NEVER hammer the API at fixed intervals."""
    time.sleep(random.uniform(min_s, max_s))


def in_send_window(country_code=None, now_utc=None):
    """True if the prospect's local time is within [07:30, 19:30].

    Coarse offset (no DST). Defaults to FR. A guardrail to avoid sending at
    3am local time, not a precise scheduler.
    """
    cc = (country_code or _DEFAULT_COUNTRY).upper()
    offset = _COUNTRY_UTC_OFFSET.get(cc, _COUNTRY_UTC_OFFSET[_DEFAULT_COUNTRY])
    now_utc = now_utc or datetime.now(timezone.utc)
    local_hour = (now_utc.hour + offset) % 24
    local_minutes = local_hour * 60 + now_utc.minute
    start = SEND_WINDOW_START[0] * 60 + SEND_WINDOW_START[1]
    end = SEND_WINDOW_END[0] * 60 + SEND_WINDOW_END[1]
    return start <= local_minutes <= end


# ----- I/O helpers --------------------------------------------------------

def load_config(path):
    """Load a skill/script config.yaml (pyyaml imported lazily)."""
    import yaml  # lazy
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_output(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Wrote %s" % path)


def write_csv(path, rows, fieldnames=None):
    if not rows:
        print("No rows to write to %s" % path)
        return
    fieldnames = fieldnames or list(rows[0].keys())
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
    print("Wrote %s (%d rows)" % (path, len(rows)))
