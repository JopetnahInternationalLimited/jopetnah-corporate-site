#!/usr/bin/env python3
"""Self-host the Unsplash photos the site currently hot-links.

Why: every page view otherwise depends on a third party (availability, privacy, speed) and
the link checker cannot see breakage. After this runs, the pages use files in assets/photos/.

Run ONCE, from the repository root, on a machine with normal internet access:
    python3 tools/localise_images.py --dry-run     list what would be downloaded and rewritten
    python3 tools/localise_images.py               download, verify, then rewrite the pages
Then commit assets/photos/ and the rewritten pages together.

Safe by design: a page reference is rewritten only if its local file was downloaded and
verified as a real JPEG; anything that fails is left pointing at Unsplash and reported.
Re-running is harmless (existing files are kept). Standard library only.
"""
import html
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL_RE = re.compile(r'https://images\.unsplash\.com/(photo-[0-9a-zA-Z\-]+)\?([^"\'\s,)<>]*)')
PRECONNECT_RE = re.compile(r'[ \t]*<link[^>]*(?:preconnect|dns-prefetch)[^>]*images\.unsplash\.com[^>]*>\n?')


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "jil-site-image-localiser/1.0", "Accept": "image/jpeg"})
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(1 + attempt)
    raise last


def plan(root):
    """Return {(photo, width): (local_filename, download_url)} for every Unsplash URL in the pages."""
    found = {}
    for page in sorted(root.glob("*.html")):
        for m in URL_RE.finditer(page.read_text(encoding="utf8")):
            photo, query = m.group(1), html.unescape(m.group(2))
            params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
            width = params.get("w", "orig")
            key = (photo, width)
            if key not in found:
                dl = f"https://images.unsplash.com/{photo}?{query}"
                if "fm=" not in query:
                    dl += "&fm=jpg"
                found[key] = (f"{photo}-w{width}.jpg", dl)
    return found


def run(root=ROOT, dry=False, fetcher=fetch):
    out = root / "assets" / "photos"
    found = plan(root)
    print(f"{len(found)} distinct image files referenced")
    ok, failed, downloaded, size = set(), [], 0, 0
    for (photo, width), (name, dl) in found.items():
        dest = out / name
        if dest.exists() and dest.stat().st_size > 1000:
            ok.add((photo, width)); continue
        if dry:
            print(f"  would download {name}"); continue
        try:
            data = fetcher(dl)
            if not data.startswith(b"\xff\xd8\xff") or len(data) < 1000:
                raise ValueError("response is not a valid JPEG")
        except Exception as e:  # noqa: BLE001 - report every kind of failure, keep going
            failed.append((name, str(e))); continue
        out.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        ok.add((photo, width)); downloaded += 1; size += len(data)
    if dry:
        print("Dry run only: nothing downloaded or changed."); return 0
    changed = 0
    for page in sorted(root.glob("*.html")):
        text = page.read_text(encoding="utf8")

        def repl(m):
            params = dict(p.split("=", 1) for p in html.unescape(m.group(2)).split("&") if "=" in p)
            key = (m.group(1), params.get("w", "orig"))
            return f"assets/photos/{found[key][0]}" if key in ok else m.group(0)

        new = URL_RE.sub(repl, text)
        if not URL_RE.search(new):
            new = PRECONNECT_RE.sub("", new)
        if new != text:
            page.write_text(new, encoding="utf8"); changed += 1
            print(f"  rewrote {page.name}")
    print(f"Downloaded {downloaded} new file(s) ({size/1024:.0f} KB); {len(ok)} of {len(found)} available locally; {changed} page(s) rewritten.")
    for name, why in failed:
        print(f"  FAILED {name}: {why}")
    if failed:
        print("Some images could not be fetched and still point at Unsplash. Re-run when online.")
        return 1
    print("Done. Commit assets/photos/ and the rewritten pages. You can now drop images.unsplash.com from .lychee.toml excludes.")
    return 0


if __name__ == "__main__":
    sys.exit(run(dry="--dry-run" in sys.argv[1:]))
