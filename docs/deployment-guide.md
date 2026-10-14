# Deployment Guide

How to deploy, update, and troubleshoot the Jopetnah International Limited website on GitHub Pages.

## Current live URLs

- **GitHub Pages URL:** `https://jopetnahinternationallimited.github.io/jopetnah-corporate-site/`
- **Custom domain:** not yet connected (see "Connecting a Custom Domain" below)

## One-Time Setup (already done, documented for reference)

1. Repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: **/ (root)**
4. Save — GitHub Pages auto-deploys on every push to `main` from that point on. No workflow file, no build step, no manual "publish" action needed.

## Uploading / Updating Files

### If drag-and-drop upload isn't working
This repo's maintainer encountered unreliable behavior with GitHub's drag-and-drop upload UI (files silently failing to attach, no error message shown). **Folder-scoped direct upload URLs** proved to be the reliable workaround:

- Root files: `https://github.com/JopetnahInternationalLimited/jopetnah-corporate-site/upload/main`
- Into `css/`: `.../upload/main/css`
- Into `js/`: `.../upload/main/js`
- Into `assets/`: `.../upload/main/assets`

Visiting a folder-scoped URL like this tells GitHub which folder you're uploading into — even if the folder doesn't exist yet, it's created automatically on commit. **Use the "choose your files" text link** (opens your OS file picker) rather than dragging, if drag-and-drop continues to be unreliable.

### Uploading dotfiles (`.gitignore`, `.nojekyll`)
Some file pickers hide files starting with a dot by default. If you can't select a dotfile from the upload dialog, use GitHub's web-based "Create new file" button instead and type the filename (including the leading dot) directly into the path field, then paste the contents.

## Connecting a Custom Domain (`www.jopetnah.com`)

1. Repo **Settings → Pages → Custom domain** → enter `www.jopetnah.com` → Save (this auto-commits a `CNAME` file to the repo root)
2. At your domain registrar, add a **CNAME record**:

   | Type | Name/Host | Points to |
   |---|---|---|
   | CNAME | `www` | `jopetnahinternationallimited.github.io` |

3. *(Recommended)* Also cover the bare domain (`jopetnah.com` without `www`) with four **A records**:

   | Type | Name/Host | Points to |
   |---|---|---|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |

4. Wait for DNS propagation (up to 24 hours, often much faster)
5. Back in **Settings → Pages**, once the DNS check passes, enable **Enforce HTTPS**
6. Verify: `dig www.jopetnah.com +noall +answer` should show a CNAME pointing to the `github.io` address

**Important — do this after connecting the domain:** `sitemap.xml` and `robots.txt` both hardcode the current `.github.io` URL. Once the custom domain is live, both files must be regenerated with the new domain, and the sitemap must be re-submitted in Search Console under a **new property** for the custom domain (see below).

## Search Engine Indexing

### Google Search Console setup
1. Add property using the exact URL: `https://jopetnahinternationallimited.github.io/jopetnah-corporate-site/`
2. Verify ownership (Search Console provides an HTML verification file or meta tag)
3. **Indexing → Sitemaps** → submit `sitemap.xml`
4. For faster individual-page indexing: **URL Inspection** → paste the page URL → **Request Indexing**

### Known issue: "Sitemap could not be read"
During initial setup, Search Console repeatedly reported this error even though the sitemap file was independently confirmed to be valid, well-formed XML (verified by opening it directly in a browser), correctly scoped, and properly linked from `robots.txt`. This is a **documented, recurring false-positive in Search Console's sitemap validator** — multiple independent reports describe the exact same symptom with no underlying file problem.

**What actually worked:** bypassing the sitemap entirely and using **URL Inspection → Request Indexing** on each page individually. This got pages indexed successfully despite the sitemap report continuing to show an error. **Conclusion: don't block on getting the sitemap report to show "Success" — indexing works fine through direct URL submission regardless of that report's status.**

If troubleshooting this again in the future, things already ruled out during the original investigation:
- ❌ Invalid XML (confirmed valid)
- ❌ Wrong property scope (confirmed matching)
- ❌ `robots.txt` blocking or misconfigured (confirmed correct)
- ❌ BOM/encoding issues (confirmed clean UTF-8, no BOM, no CRLF)
- ✅ Likely just a Search Console UI quirk — proceed via URL Inspection instead

### `.nojekyll`
GitHub Pages runs sites through Jekyll processing by default unless a `.nojekyll` file exists in the repo root. This site includes one as a precaution — it's not strictly fixing an active bug, but it (a) speeds up deploys slightly since Jekyll processing is skipped, and (b) prevents Jekyll from silently excluding any future folder/file that happens to start with an underscore (e.g. `_data/`).

## Post-Deployment Checklist

After any content update:
- [ ] Click through all nav links on both desktop and mobile widths
- [ ] Confirm the services accordion still expands/collapses correctly
- [ ] Confirm the contact form's `mailto:` opens with the right address
- [ ] If new pages were added: update `sitemap.xml` and re-submit in Search Console
- [ ] If nav/footer changed: confirm the change was applied to **all** HTML files, not just some (see `development-guide.md` for why this is a manual, per-file step)
