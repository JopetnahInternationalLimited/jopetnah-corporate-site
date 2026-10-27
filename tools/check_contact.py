#!/usr/bin/env python3
"""Fail if contact details or retired wording drift from tools/contact.json.

Run: python3 tools/check_contact.py     (CI runs it on every push and pull request)
Checks every .html page, README.md, docs/*.md and manifest.webmanifest for:
  - any "Rise Road" address that is not exactly the master street or full address
  - phone numbers not in the master list / format (tel: links must be the same numbers, digits only)
  - email addresses other than the master list
  - retired or forbidden wording (e.g. the old Mutungo-Luzira HQ, "conglomerate")
Standard library only; changes nothing.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
M = json.loads((ROOT / "tools" / "contact.json").read_text(encoding="utf8"))
files = sorted(ROOT.glob("*.html")) + [ROOT / "README.md", ROOT / "manifest.webmanifest"] + sorted((ROOT / "docs").glob("*.md"))
digits = lambda s: re.sub(r"\D", "", s)
phone_digits = {digits(p) for p in M["phones"]}
problems = []

for f in files:
    if not f.exists():
        continue
    raw = f.read_text(encoding="utf8", errors="replace")
    text = html.unescape(raw)
    name = f.relative_to(ROOT)
    for m in re.finditer(r"U\.?N\.? Rise Road[^<\"'\n]*", text):
        found = m.group(0).rstrip(" ,*")
        if found not in (M["address_street"], M["address_full"]) and not found.startswith(M["address_full"]):
            problems.append(f"{name}: address differs from master: '{found[:90]}'")
    for m in re.finditer(r"(?<!tel:)\+256[ \d()\-]{9,}", text):
        p = m.group(0).strip()
        if p not in M["phones"]:
            problems.append(f"{name}: phone '{p}' is not one of {M['phones']}")
    for m in re.finditer(r'href="tel:([^"]+)"', raw):
        if digits(m.group(1)) not in phone_digits or re.search(r"[^\d+]", m.group(1)):
            problems.append(f"{name}: tel link '{m.group(1)}' does not match the master numbers (digits only)")
    for m in re.finditer(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", text):
        if m.group(0).lower() not in M["emails"] + M.get("emails_ignored", []):
            problems.append(f"{name}: email '{m.group(0)}' is not in the master list")
    for bad in M["forbidden"]:
        if re.search(re.escape(bad), text, re.I):
            problems.append(f"{name}: contains retired/forbidden wording '{bad}'")

if problems:
    print("\n".join(sorted(set(problems))))
    print(f"\n{len(set(problems))} problem(s). Fix the pages or, if the detail really changed, update tools/contact.json.")
    sys.exit(1)
print(f"OK: contact details and wording consistent across {sum(1 for f in files if f.exists())} files")
