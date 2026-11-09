#!/usr/bin/env python3
"""Make a verification code for one staff card and print the staff.json entry.

Usage:  python3 tools/jil-staff-token.py "JIL-0001" "Full Name" "Job Title" "Department" 2027-12-31 [base-url]

Prints:
  - the code to print on the back of the card (XXXX-XXXX-XXXX)
  - the URL to put in the QR code
  - the JSON line to paste inside "records" in data/staff.json
The code itself is never stored on the site; only its SHA-256 hash is.
To withdraw a card, change "status" to "withdrawn" in that entry.
"""
import hashlib, json, secrets, sys

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O/1/I

def main():
    if len(sys.argv) < 6:
        print(__doc__); sys.exit(1)
    staff_no, name, title, dept, valid_until = sys.argv[1:6]
    base = sys.argv[6] if len(sys.argv) > 6 else "https://jopetnahinternationallimited.github.io/jopetnah-corporate-site/"
    code = "".join(secrets.choice(ALPHABET) for _ in range(12))
    digest = hashlib.sha256(code.encode()).hexdigest()
    entry = {"staff_no": staff_no, "name": name, "title": title, "department": dept,
             "status": "active", "valid_until": valid_until}
    print("Card code : %s-%s-%s" % (code[:4], code[4:8], code[8:]))
    print("QR URL    : %sverify.html?t=%s" % (base, code))
    print('JSON entry: "%s": %s,' % (digest, json.dumps(entry)))

main()
