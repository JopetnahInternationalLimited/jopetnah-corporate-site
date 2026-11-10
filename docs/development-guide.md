# Development Guide

This guide explains how the Jopetnah International Limited website is built, why it's built this way, and how to safely make changes to it.

## Tech Stack

**Plain HTML, CSS, and JavaScript. No frameworks, no build tools, no dependencies.**

- No React, Vue, or any JS framework
- No Sass/Less — just one hand-written CSS file
- No npm, no `package.json`, no bundler (Webpack/Vite/etc.)
- No templating engine — each `.html` file is a complete, standalone document

This is a deliberate choice, not an oversight. For a site of this size (10 real pages, no dynamic data, no user accounts), a build pipeline would add maintenance overhead without adding capability. If the site grows substantially — hundreds of pages, a CMS, multiple contributors needing shared components — that calculation changes, and it would be worth migrating to a static site generator (see "When to reconsider this architecture" below).

## File Structure

```
├── index.html              Home
├── about.html              About Us
├── services.html           Our 16 Sectors (accordion)
├── sustainability.html     ESG / Governance / HSE / CSR
├── contact.html            Contact form + office locations
├── careers.html            Coming soon (CV submission CTA)
├── news.html               Coming soon (social links CTA)
├── projects.html           Coming soon (portfolio placeholder)
├── privacy.html            Privacy Policy
├── terms.html              Terms of Service
├── 404.html                Custom error page
├── sectors.html            Redirect → services.html (SEO alias)
├── industries.html         Redirect → services.html (SEO alias)
│
├── css/
│   └── style.css           Single shared stylesheet (all pages)
├── js/
│   └── script.js           Mobile nav toggle + services accordion
├── assets/
│   └── icon.png             Logo mark (globe + "j")
├── favicon.ico
├── robots.txt
├── sitemap.xml
└── .gitignore
```

**Every page includes the same nav and footer, copy-pasted into each file.** There is no `<!-- include header.html -->` mechanism — plain static HTML can't do that natively without a server-side language (PHP) or a build step. This means: **if you change the nav or footer, you must update it in every single HTML file.** See "Making Site-Wide Changes" below for how this is actually done in practice (via a Python build script, not by hand).

## How the site is actually built (not by hand-editing HTML)

Although the *deployed* files are plain static HTML, they were *generated* using a small set of Python scripts, because hand-editing the same nav/footer across 13 files is error-prone. These build scripts are **not part of the deployed site** — they're a development convenience that lives outside this repo. If you have access to them:

- `content_data.py` — all text content as Python data structures (the 16 sectors, core values, strategic objectives, contact info, social links)
- `page_shell.py` — the shared nav/footer template, and the `page_shell()` function that wraps page content in a complete HTML document
- `build_home.py`, `build_about.py`, `build_services.py`, etc. — one script per page, importing from the two files above and writing the final `.html` file

**If you don't have these scripts:** you're editing the static HTML directly, which is fine for small text tweaks, but be aware that any nav/footer change needs to be manually repeated across all 13 files. Search-and-replace across all files (`grep -rl "old text" *.html`) is your friend here.

## Design System Reference

All colors, fonts, and spacing are defined once as CSS custom properties at the top of `style.css`:

```css
:root {
  --navy: #1B1E23;       /* primary text color */
  --red: #E0151B;        /* brand accent */
  --blue: #0E86D4;       /* brand accent */
  --blue-tint: #EAF4FC;  /* light card backgrounds */
  --red-tint: #FDEAEA;   /* light card backgrounds */
  --hairline: #E3E5E8;   /* borders/dividers */
  --gray: #53555B;       /* secondary text */
  --lgray: #8A8D93;      /* tertiary/muted text */
  --paper: #FBFBFC;      /* off-white section backgrounds */
  --white: #FFFFFF;

  --font-display: 'Poppins', 'Segoe UI', sans-serif;  /* headings, nav, buttons */
  --font-body: 'Lora', Georgia, serif;                 /* paragraph text */
}
```

**Always use these variables (`var(--blue)`, etc.) rather than hardcoding hex values** when writing new CSS — this is what makes a future rebrand or color tweak a one-line change instead of a find-and-replace across the whole file. See `brand-guidelines.md` for the full rationale behind these specific choices.

## Common Tasks

### Adding or editing a sector/division
Sector content lives in `services.html`, inside `.accordion-item` blocks. Each has:
```html
<div class="accordion-item" id="division-N">
  <button class="accordion-trigger">...</button>
  <div class="accordion-panel">
    <div class="accordion-panel-inner">
      <p>[description]</p>
      <div class="core-services-label">Core Services</div>
      <div class="chip-list">
        <span>[service 1]</span>
        <span>[service 2]</span>
      </div>
    </div>
  </div>
</div>
```
If a sector's name changes, also update its corresponding entry in `index.html`'s division-preview grid (`.div-chip` elements, linked via `href="services.html#division-N"`).

### Adding a new page
1. Copy the nav (`.site-header`) and footer (`.site-footer`) blocks exactly from an existing page
2. Add the new page to the `<nav class="nav-links">` block **on every page** if it should appear in primary navigation, or just to the footer's Company column if it's a secondary page (this is what we did for Careers/News/Projects)
3. Add it to `sitemap.xml` (unless it's a redirect or error page — see that file's existing entries for the pattern)

### Testing locally
No build step needed:
```bash
# Quick view
open index.html

# Or serve it (recommended — avoids relative-path quirks)
python3 -m http.server 8000
# visit http://localhost:8000
```

## Known Limitations

- **Fonts require internet** — Poppins/Lora load from Google Fonts CDN. If self-hosting them becomes a priority, fonts would need to be downloaded into `assets/fonts/` and referenced via `@font-face` instead of the current `<link>` tag.
- **Contact form has no backend** — it submits via `mailto:`, which opens the visitor's email client rather than posting to a server. Fine for low volume; consider a form service (e.g., Formspree) if inquiry volume grows.
- **No image optimization pipeline** — if/when photography is added, images should be manually compressed and sized appropriately before committing (no automated build step will do this for you).

## When to reconsider this architecture

This plain-HTML approach stops being the right choice if any of the following happen:
- The page count grows into the dozens and duplicated nav/footer edits become genuinely error-prone
- Multiple people need to edit content simultaneously without stepping on each other
- Content needs to come from a CMS or database rather than hand-written HTML

At that point, migrating to a static site generator (e.g., Eleventy, Astro, or Jekyll — the last of which GitHub Pages supports natively) would be worth the added complexity. Not needed today.
