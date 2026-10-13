"""Downloads cached for the day in validate/.cache/<YYYY-MM-DD>/<source>/ (gitignored; the
workflow keeps it in actions/cache so a re-run the same day downloads nothing twice).
Older days are deleted at start (prune())."""
import hashlib
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, ".cache")
DAY = time.strftime("%Y-%m-%d", time.gmtime())
STATS = {"downloads": 0, "hits": 0, "bytes": 0}


def path(source, name):
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in name)
    if len(safe) > 120:
        safe = safe[:80] + "-" + hashlib.sha1(name.encode()).hexdigest()[:12]
    return os.path.join(ROOT, DAY, source, safe)


def prune(keep=2):
    """Delete cached days except the newest `keep`."""
    if not os.path.isdir(ROOT):
        return
    days = sorted(d for d in os.listdir(ROOT) if len(d) == 10 and d[4] == "-")
    for d in days[:-keep]:
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)


def _store(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, p)


def get_bytes(source, name, url, headers=None, timeout=120, pause=0.0, tries=4):
    p = path(source, name)
    if os.path.exists(p):
        STATS["hits"] += 1
        with open(p, "rb") as f:
            return f.read()
    err = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            _store(p, data)
            STATS["downloads"] += 1
            STATS["bytes"] += len(data)
            if pause:
                time.sleep(pause)
            return data
        except urllib.error.HTTPError as e:
            if e.code in (400, 403, 404):           # will not change on retry
                raise
            err = e
        except Exception as e:                    # noqa: BLE001 - timeouts, resets: retry
            err = e
        print("  %s %s failed (%s), retrying" % (source, name, str(err)[:80]), file=sys.stderr)
        time.sleep(10 * (attempt + 1))
    raise err


def get_text(source, name, url, headers=None, timeout=120, pause=0.0):
    return get_bytes(source, name, url, headers, timeout, pause).decode("utf-8", "replace")


def load_json(source, name):
    p = path(source, name)
    try:
        with open(p) as f:
            STATS["hits"] += 1
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_json(source, name, obj):
    _store(path(source, name), json.dumps(obj, separators=(",", ":")).encode())

