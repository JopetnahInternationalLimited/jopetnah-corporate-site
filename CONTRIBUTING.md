# Contributing

Thank you for your interest in improving the Jopetnah International Limited website.

## Before you start

This is the official corporate website repository for Jopetnah International Limited. It is publicly visible for transparency, but content changes (company information, service descriptions, branding) should generally come from the company itself rather than external contributors. See `LICENSE` for usage terms.

**Technical improvements are welcome** — bug fixes, accessibility improvements, broken link reports, and performance suggestions.

## How to report an issue

1. Check existing [Issues](https://github.com/JopetnahInternationalLimited/jopetnah-corporate-site/issues) to see if it's already reported
2. Open a new issue describing:
   - What page/file is affected
   - What's wrong (broken link, display bug, typo, etc.)
   - Steps to reproduce, if applicable
   - Screenshots, if helpful

## How to submit a change

1. Fork the repository
2. Create a branch describing your change (e.g., `fix-broken-contact-link`)
3. Make your change
4. Test locally by opening the affected `.html` file(s) directly in a browser, or run:
   ```bash
   python3 -m http.server 8000
   ```
   and check `http://localhost:8000`
5. Open a Pull Request describing what changed and why

## Project conventions

See `docs/development-guide.md` for the site's architecture and conventions before making structural changes — in particular, note that:
- This is a plain HTML/CSS/JS site with **no build step** — don't introduce a bundler or framework without discussing it first
- The navigation and footer are duplicated across every page (no templating system exists) — if you change one, you must update all of them
- See `docs/brand-guidelines.md` before changing colors, fonts, or copy tone

## Code of Conduct

Participation in this project is governed by our [Code of Conduct](CODE_OF_CONDUCT.md).
