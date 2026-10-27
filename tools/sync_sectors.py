#!/usr/bin/env python3
"""Keep sector and pillar wording identical across the whole site.

Master record : tools/sectors.json   (the ONLY place names should be edited)
Usage         : python3 tools/sync_sectors.py            rewrite pages from the master
                python3 tools/sync_sectors.py --check    report drift, change nothing (used by CI)

Standard library only. Nothing is rewritten except the sector/pillar text that the
master record controls; every other character in every page is left untouched.
Each location is matched by an invisible key (id="sector-NN", data-sector="NN" or an
href anchor) or by the pillar number, so a renamed sector is updated everywhere. Sector
numbers are NOT shown to visitors; they exist only as these anchors/keys.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "tools" / "sectors.json"

errors = []      # structural problems that need a human
changes = []     # (file, description) for every text value that was out of sync


def esc(s):
    return s.replace("&", "&amp;")


def load():
    data = json.loads(MASTER.read_text(encoding="utf8"))
    pillars = {p["n"]: p["name"] for p in data["pillars"]}
    sectors = {s["id"]: s for s in data["sectors"]}
    if len(sectors) != 16:
        sys.exit("sectors.json must contain exactly 16 sectors")
    if len(pillars) != 4:
        sys.exit("sectors.json must contain exactly 4 pillars")
    for s in sectors.values():
        if s["pillar"] not in pillars:
            sys.exit(f"sector {s['id']} refers to unknown pillar {s['pillar']}")
        for field in ("name", "scope"):
            if not s[field].strip() or any(c in s[field] for c in '<>"'):
                sys.exit(f"sector {s['id']}: '{field}' is empty or contains < > or \"")
    for n, name in pillars.items():
        if not name.strip() or any(c in name for c in '<>"'):
            sys.exit(f"pillar {n}: name is empty or contains < > or \"")
    return pillars, sectors


def sync(fname, text, pattern, value_for, label, expect, flags=re.S):
    """Replace group 'old' wherever `pattern` matches, using value_for(match) -> escaped text.
    `pattern` must define named groups: pre, old, post (and whatever value_for needs)."""
    found = 0

    def repl(m):
        nonlocal found
        found += 1
        new = value_for(m)
        if m.group("old") != new:
            changes.append((fname, f"{label}: '{m.group('old')}' -> '{new}'"))
        return m.group("pre") + new + m.group("post")

    out = re.sub(pattern, repl, text, flags=flags)
    if found != expect:
        errors.append(f"{fname}: expected {expect} x {label}, found {found}")
    return out


HEAD_RE = r'(?P<pre><span class="pillar-n">Pillar (?P<key>\d\d)</span><span class="pillar-name">)(?P<old>.*?)(?P<post></span>)'


def check_groups(fname, text, id_re, sectors):
    """Sectors must sit under the pillar heading the master record gives them."""
    chunks = re.split(r'(?=<div class="sector-group-head)', text)[1:]
    if len(chunks) != 4:
        errors.append(f"{fname}: expected 4 pillar group headings, found {len(chunks)}")
    for ch in chunks:
        pn = re.search(r'Pillar (\d\d)</span>', ch).group(1)
        ids = set(re.findall(id_re, ch))
        want = {i for i, s in sectors.items() if s["pillar"] == pn}
        if ids != want:
            errors.append(f"{fname}: under Pillar {pn} found sectors {sorted(ids)}, master says {sorted(want)}")


def process(fname, text, pillars, sectors):
    S = lambda m: esc(sectors[m.group("key")]["name"])      # sector short name
    P = lambda m: esc(pillars[m.group("key")])              # pillar name

    if fname == "index.html":
        text = sync(fname, text,
                    r'(?P<pre>href="services\.html#sector-(?P<key>\d\d)">.*?<span class="sector-name">)(?P<old>.*?)(?P<post></span>)',
                    S, "homepage sector name", 16)
        text = sync(fname, text,
                    r'(?P<pre><span class="pillar-n">Pillar (?P<key>\d\d)</span><span class="pillar-name">)(?P<old>.*?)(?P<post></span>)',
                    P, "homepage pillar name", 4)
        # grouping check (cannot be auto-fixed: it is page structure)
        for grp in text.split('<div class="sector-group">')[1:]:
            pn = re.search(r'Pillar (\d\d)</span>', grp).group(1)
            ids = set(re.findall(r'services\.html#sector-(\d\d)"', grp.split("</div>\n          </div>")[0]))
            want = {i for i, s in sectors.items() if s["pillar"] == pn}
            if ids != want:
                errors.append(f"{fname}: Pillar {pn} lists sectors {sorted(ids)}, master says {sorted(want)}")

    elif fname == "services.html":
        parts = re.split(r'(?=<div class="accordion-item" id="sector-\d\d">)', text)
        out = [parts[0]]
        for chunk in parts[1:]:
            sid = re.match(r'<div class="accordion-item" id="sector-(\d\d)">', chunk).group(1)
            s = sectors[sid]
            f = f"{fname} (sector {sid})"
            K = lambda fn: (lambda m: fn(s))
            chunk = sync(f, chunk, r'(?P<pre><span class="pill">)(?P<old>.*?)(?P<post></span>)',
                         K(lambda s: esc(pillars[s["pillar"]])), "pillar label", 1)
            chunk = sync(f, chunk, r'(?P<pre><span class="title">)(?P<old>.*?)(?P<post></span>)',
                         K(lambda s: esc(s["name"])), "sector title", 1)
            chunk = sync(f, chunk, r'(?P<pre><p><strong>Scope:</strong> )(?P<old>.*?)(?P<post></p>)',
                         K(lambda s: esc(s["scope"])), "scope line", 1)
            chunk = sync(f, chunk, r'(?P<pre>aria-label="Discuss this sector: )(?P<old>.*?)(?P<post>")',
                         K(lambda s: esc(s["name"])), "button label", 1)
            chunk = sync(f, chunk,
                         r'(?P<pre>href="contact\.html\?sector=)(?P<old>\d\d)(?P<post>#enquiry-form")',
                         K(lambda s: s["id"]), "button target", 1)
            out.append(chunk)
        text = "".join(out)
        if len(parts) - 1 != 16:
            errors.append(f"{fname}: expected 16 sector panels, found {len(parts) - 1}")
        text = sync(fname, text, r'(?P<pre><h3>(?P<key>0[1-4]) · )(?P<old>.*?)(?P<post></h3>)',
                    P, "pillar heading", 4)
        text = sync(fname, text, HEAD_RE, P, "pillar group heading", 4)
        check_groups(fname, text, r'id="sector-(\d\d)"', sectors)

    elif fname == "about.html":
        text = sync(fname, text,
                    r'(?P<pre><div class="value-card" data-sector="(?P<key>\d\d)">\s*<h3>)(?P<old>.*?)(?P<post></h3>)',
                    S, "about sector name", 16)
        text = sync(fname, text, HEAD_RE, P, "about pillar group heading", 4)
        check_groups(fname, text, r'data-sector="(\d\d)"', sectors)

    elif fname == "impact.html":
        # Other sections of this page use similar card markup for unrelated lists, so
        # only the section that lists the sectors is touched.
        m = re.search(r'<h2>Impact Applied in Context</h2>.*?</section>', text, re.S)
        if not m:
            errors.append(f"{fname}: section 'Impact Applied in Context' not found")
        else:
            region = sync(fname, m.group(0),
                          r'(?P<pre><div class="value-card" data-sector="(?P<key>\d\d)"><h3>)(?P<old>.*?)(?P<post></h3>)',
                          S, "impact sector name", 16)
            region = sync(fname, region, HEAD_RE, P, "impact pillar group heading", 4)
            check_groups(fname, region, r'data-sector="(\d\d)"', sectors)
            text = text[:m.start()] + region + text[m.end():]

    elif fname == "sustainability.html":
        text = sync(fname, text,
                    r'(?P<pre><p data-sector="(?P<key>\d\d)">)(?P<old>.*?)(?P<post></p>)',
                    S, "sustainability sector name", 16)
        text = sync(fname, text,
                    r'(?P<pre><span class="eyebrow">Pillar (?P<key>\d\d)</span><h3>)(?P<old>.*?)(?P<post></h3>)',
                    P, "sustainability pillar name", 4)
        for grp in re.split(r'(?=<span class="eyebrow">Pillar \d\d</span>)', text)[1:]:
            pn = re.match(r'<span class="eyebrow">Pillar (\d\d)</span>', grp).group(1)
            ids = set(re.findall(r'<p data-sector="(\d\d)">', grp.split("</div>")[0]))
            want = {i for i, s in sectors.items() if s["pillar"] == pn}
            if ids != want:
                errors.append(f"{fname}: Pillar {pn} lists sectors {sorted(ids)}, master says {sorted(want)}")

    elif fname == "contact.html":
        lines = ['          <select id="service" name="service">',
                 '            <option value="">Select a service area</option>',
                 '            <option value="General enquiry / not sure yet">General enquiry / not sure yet</option>']
        for pn, pname in sorted(pillars.items()):
            lines.append(f'            <optgroup label="{esc(pname)}">')
            for sid, s in sorted(sectors.items()):
                if s["pillar"] == pn:
                    value = f'{s["name"]} ({s["scope"]})'
                    lines.append(f'              <option value="{esc(value)}" data-sector="{sid}">{esc(s["name"])}</option>')
            lines.append("            </optgroup>")
        lines.append("          </select>")
        new = "\n".join(lines)
        m = re.search(r'          <select id="service" name="service">.*?          </select>', text, re.S)
        if not m:
            errors.append(f"{fname}: service dropdown not found")
        else:
            if m.group(0) != new:
                changes.append((fname, "service dropdown regenerated from master"))
            text = text[:m.start()] + new + text[m.end():]
    return text


def main():
    check = "--check" in sys.argv[1:]
    pillars, sectors = load()
    pending = {}
    for fname in ("index.html", "services.html", "about.html", "impact.html", "sustainability.html", "contact.html"):
        path = ROOT / fname
        old = path.read_text(encoding="utf8")
        new = process(fname, old, pillars, sectors)
        if new != old:
            pending[path] = new
    for f, c in changes:
        print(("DRIFT  " if check else "UPDATED ") + f"{f}: {c}")
    for e in errors:
        print("ERROR  " + e)
    if check:
        if changes or errors:
            print("\nSector wording is out of sync with tools/sectors.json. Run: python3 tools/sync_sectors.py")
            sys.exit(1)
        print("OK: all sector and pillar wording matches tools/sectors.json")
        return
    for path, new in pending.items():
        path.write_text(new, encoding="utf8")
    if errors:
        print("\nSome problems need a manual fix (see ERROR lines above).")
        sys.exit(1)
    print(f"Done. {len(pending)} file(s) rewritten, {len(changes)} value(s) changed." if pending else "Already in sync. Nothing to do.")


if __name__ == "__main__":
    main()
