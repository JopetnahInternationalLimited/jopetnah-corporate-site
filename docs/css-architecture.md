# CSS Architecture and Design System

Jopetnah International Limited (JIL) website. This document is the reference for anyone editing styles. It covers the technology decisions, the file structure, the design tokens, the conventions, and how to test a change.

> Guiding idea: **one coherent identity, one design system, sixteen sectors, one coordinated partner.** Every page uses the same tokens, components and breakpoints.

---

## 1. The stack and why

The site is a static GitHub Pages site with no build step. The CSS stack is therefore **plain modern CSS in two files**:

| File | Loaded on | Purpose |
|---|---|---|
| `css/style.css` | every page | fonts, tokens, base, layout, shared components, page components, utilities, responsive rules, accessibility, motion, print |
| `css/news-articles.css` | `news.html` and the `news-*.html` articles only | news listing and the "jn-" article template |

### Technology verdicts

| Technology | Verdict | Reasoning |
|---|---|---|
| Vanilla CSS | **Adopt (retain)** | Zero dependencies, zero build, works on GitHub Pages as is. |
| CSS custom properties (design tokens) | **Adopt and extend** | The site already relied on them. Tokens grew from 21 (colour and font only) to 89 (colour roles, type, radius, spacing, layout). |
| CSS Grid and Flexbox | **Retain** | Already used for every layout; no change needed. |
| `clamp()` fluid type | **Adopt (limited)** | Used for the hero, page title and article title only, with a static fallback inside `@supports`. |
| Utility and pattern classes | **Adopt (small set)** | About 40 named classes replaced 726 of the 903 repeated inline styles. They are named by role (`.copy-muted`, `.media-frame`, `.wrap--860`), not a utility framework. |
| BEM | **Retain the existing naming; use `--` modifiers in new code** | Class names are already descriptive component names (`.accordion-trigger`, `.footer-brand`). A mass rename adds risk and no benefit. New variants use the BEM modifier style (for example `.cta-band--dark`). |
| Logical properties | **Adopt for new code only** | The site is English, left to right. Retrofitting existing rules gives no user benefit. |
| Mobile-first media queries | **Partly: new components only** | The existing layout is desktop-first (`max-width`). Converting it is a rewrite with no visible gain. The breakpoints were consolidated instead. |
| CSS Cascade Layers (`@layer`) | **Defer** | Supported from Chrome 99, Safari 15.4, Firefox 97, Samsung Internet 18. A browser that does not understand `@layer` ignores the layered styles entirely, which would leave the page unstyled. StatCounter (June to July 2026) shows about 83% Chrome, 7% Safari, 5.5% Opera and 2% Samsung Internet on mobile in Uganda, so around 6% of visits come from Opera, UC and similar browsers whose engine versions are unknown. The benefit on a 40 KB single stylesheet is small, because ordering the file gives the same specificity control. Revisit when that audience share is clearly safe. |
| Native CSS nesting | **Defer** | Same risk: older engines drop whole nested rules. The saving is a few hundred bytes. |
| Container queries | **Defer** | No component currently needs to adapt to its container rather than the viewport. |
| SCSS/Sass | **Reject** | Needs a build pipeline. Native custom properties already provide variables. |
| CSS Modules | **Reject** | Needs a bundler and JavaScript imports; irrelevant to static HTML. |
| Tailwind CSS | **Reject** | Needs a build step (or a runtime script), and would replace every class and inline style on 47 pages. No gain over the current system. |
| Bootstrap | **Reject** | Heavy, overlapping with the existing system, and would fight the brand styling. |

---

## 2. File structure of `css/style.css`

Read top to bottom. A later rule of equal specificity overrides an earlier one, so put new rules in the correct section.

| # | Section | Contains |
|---|---|---|
| 0 | Fonts | `@font-face` for self-hosted Poppins and Lora |
| 1 | Design tokens | palette, semantic roles, inverse surfaces, scales, light and dark themes |
| 2 | Base | box-sizing, body, links, images |
| 3 | Typography | headings, `.eyebrow`, `.section-head` |
| 4 | Layout | `.wrap`, sections, `.hero`, `.page-header` |
| 5 | Components | buttons, header and nav, cards, accordion, forms, stats and CTA bands, footer, compare table, quick-contact, leadership |
| 6 | Page components | home hero, orbit and sector grid; sector lists and "Discuss this sector" buttons; About collapsibles; contact; sustainability; policy pages |
| 7 | Utilities | small helpers (see section 5 below) |
| 8 | Responsive | every media query, grouped by breakpoint |
| 9 | Accessibility | focus rings, skip link, selection |
| 10 | Motion and print | reduced motion, print |

Fonts are in `assets/fonts/` (Latin subset, SIL Open Font License; see `assets/fonts/LICENSES.txt`). Only Poppins 700 and Lora 400 are preloaded in each page's `<head>`.

---

## 3. Design tokens

### Brand palette (raw values)

| Token | Value | Use |
|---|---|---|
| `--brand-blue` | `#0E86D4` | primary corporate blue: backgrounds, borders, icons, gradients |
| `--brand-blue-deep` | `#0A5F94` | blue used as text on light surfaces (6.7:1) |
| `--brand-blue-solid` | `#0B72B8` | solid blue behind white text, and the end of the brand gradient (5.1:1) |
| `--brand-red` | `#E0151B` | accent and gradient start |
| `--brand-red-deep` | `#B10E13` | small red text on tinted backgrounds |
| `--brand-ink` | `#1B1E23` | deep navy / ink |

### Semantic roles (these change with the theme)

| Token | Light | Dark | Use |
|---|---|---|---|
| `--color-bg` | `#FFFFFF` | `#121418` | page background |
| `--color-surface` | `#FBFBFC` | `#1A1D22` | alternate sections, inputs |
| `--color-ink` | `#1B1E23` | `#EDEFF2` | headings and primary text |
| `--color-ink-muted` | `#53555B` | `#A9ADB5` | secondary text |
| `--color-ink-subtle` | `#5F636A` | `#888D96` | tertiary text |
| `--color-line` | `#E3E5E8` | `#343941` | borders and dividers |
| `--color-line-strong` | `#C9D6E2` | `#4A515C` | form control borders |
| `--color-tint-blue` / `--color-tint-red` | `#EAF4FC` / `#FDEAEA` | `#13232F` / `#2A1517` | card backgrounds |
| `--color-link` | `#0A5F94` | `#5FB6EF` | blue text |
| `--color-accent` | `#0E86D4` | same | blue backgrounds and borders |
| `--color-focus` | `#075F9A` | same | focus ring and form focus border |

### Fixed inverse surfaces (the same in both themes)

`--surface-inverse` (`#1B1E23`) with `--on-inverse`, `--on-inverse-2`, `--on-inverse-3`, `--on-inverse-muted`, `--on-inverse-line`, `--on-inverse-accent`. Use these for the footer, stats band, CTA band and hero overlays. Do not use `--color-bg` or `--color-ink` on those surfaces, because they flip in dark mode and the text would disappear.

### Scales

| Group | Tokens |
|---|---|
| Type (rem) | `--fs-2xs` 11px, `--fs-xs` 12, `--fs-sm` 13, `--fs-md` 14, `--fs-lg` 15, `--fs-base` 16, `--fs-xl` 17, `--fs-2xl` 18, `--fs-3xl` 19, `--fs-4xl` 24, `--fs-5xl` 26, `--fs-6xl` 28, `--fs-7xl` 34 |
| Fluid type | `--fs-hero` 30 to 46px (homepage headline), `--fs-page-title` 28 to 34px (34px above about 486px) |
| Radius | `--radius-xs` 4, `-sm` 6, `-md` 8, `-lg` 10, `-xl` 12, `-pill` 999 |
| Spacing | `--space-1` 4px up to `--space-10` 64px (4, 8, 12, 16, 20, 24, 32, 40, 48, 64) |
| Layout | `--maxw` 1180px, `--gutter` 28px (20px on phones), `--section-y` 68px (52px on phones), `--section-y-tight` 48px (38px) |
| Elevation | `--shadow-card`, `--shadow-soft`, `--shadow-hover`, `--shadow-header` |
| Fonts | `--font-display` Poppins (navigation, headings, labels, buttons); `--font-body` Lora (paragraphs and long-form text) |

Font sizes use `rem`, so text follows the visitor's browser font-size setting. A few legacy sizes that are not on the scale (for example 12.5px, 13.8px, 14.5px) are kept as exact `rem` values so the existing design does not shift. Move them onto the scale in a future design pass.

### Legacy aliases

`--navy`, `--white`, `--paper`, `--hairline`, `--gray`, `--lgray`, `--blue`, `--blue-text`, `--blue-tint`, `--red-tint`, `--red` still exist because page HTML uses them in inline styles. They point at the semantic tokens above. Use `--color-*` in new CSS.

---

## 4. Themes (light and dark)

- `js/script.js` sets `<html data-theme="light|dark">` from the saved choice, otherwise from the system preference.
- `:root[data-theme="dark"]` redefines **semantic tokens only**. Components should not need dark-specific overrides. If you find yourself writing `:root[data-theme="dark"] .something`, check whether a token is missing instead.
- `color-scheme` is set per theme so scrollbars, form controls and autofill follow the theme.
- Text sitting on a surface that stays dark in both themes must use the `--on-inverse*` tokens.

---

## 5. Conventions

**Naming.** Descriptive component names with a hyphenated child (`.accordion-trigger`, `.footer-brand`). Variants use a double hyphen modifier (`.cta-band--dark`). No IDs in selectors.

**Specificity.** Keep selectors to one or two classes. Do not use `!important` except in reduced-motion, print and the `.mt-0` utility.

**Utility, pattern and modifier classes replace repeated inline styles.** They live in section 7. Three kinds:
- *Utilities*: `.mt-0`, `.visually-hidden`, `.bg-surface`, `.link-plain`, `.text-muted`, `.u-my-2`, `.u-mt-5`, `.u-mt-6`, `.u-mb-4`, `.u-m-0`.
- *Content patterns* named by role: `.lede-muted`, `.copy-muted`, `.copy-muted-75`, `.list-muted`, `.prose-list`, `.footnote`, `.subhead`, `.subhead-sm`, `.subhead-md`, `.label-caps`, `.link-strong`, `.card-head`, `.card-title`, `.card-meta`, `.note-sm`, `.note-italic`, `.title-xl`, `.title-section`, `.media-frame`, `.photo-wide`, `.pad-article`.
- *Modifiers* that extend a component, in BEM style: `.eyebrow--tight`, `.eyebrow--center`, `.cta-row--center`, `.value-card--roomy`, `.wrap--760`, `.wrap--860`, `.wrap--center-640`, `.hero--center`, `.lede--measure-center`, `.cta-band--dark`.

Each is written as `element.class` (for example `p.copy-muted`) so it matches the specificity of component rules such as `.value-card p`, as the inline style it replaced always did. Add a new class only when the same inline style appears several times.

**Inline styles.** 177 inline `style=""` attributes remain (903 before the refactor). They are one-off layout tweaks. When you edit a page, turn any pattern that appears more than a few times into a class rather than copying the inline style.

**Adding a component.**
1. Put the rule in section 5 or 6 of `style.css` (or in `news-articles.css` if only news pages use it).
2. Use tokens for every colour, font size, radius and shadow.
3. Add responsive rules to the matching breakpoint block in section 8, not next to the component.
4. Check light mode, dark mode and keyboard focus.

---

## 6. Responsive design

Media queries cannot read custom properties, so use only these six values. The CSS is desktop-first (`max-width`).

| Breakpoint | What changes |
|---|---|
| 1180px (= `--maxw`) | header switches to the menu button |
| 900px | 3- and 4-column grids become 2 columns; two-column pages stack; footer becomes 2 columns |
| 720px | comparison table and small two-column blocks become one column; stats become 2 columns |
| 600px | phones: tighter gutters and sections, single-column grids, header CTA hidden |
| 480px | thumbnails in the services accordion are hidden |
| 360px | very small phones: grid cells may shrink below their longest word and long words wrap |

Every page has the same seven header links (Home, About, Services, Sustainability, Transparency, News, Contact). That header needs about 1095px with Poppins, so it collapses to the menu button at 1180px (the container width).

---

## 7. Accessibility rules

- Text contrast of at least 4.5:1 (3:1 for large text) in both themes. White text on `--brand-blue` is only 3.9:1, so solid backgrounds behind small white text use `--brand-blue-solid`. Button labels over the red-to-blue gradient stay white in both themes (measured minimum 5.8:1); the label must never use `--color-bg`, which turns near-black in dark mode.
- Automated checkers cannot test text over a gradient. Measure it: hide the text, sample the background pixels beneath it, and compute the ratio.
- Heading levels must not skip (h1, then h2, then h3). The W3C Nu HTML Checker reports 0 errors on all pages; keep it that way.
- Every interactive element shows a visible focus ring (3px, `--color-focus`). Do not set `outline: none` without a replacement indicator.
- The skip link is the first element in `<body>`; the page's `<main>` is `id="main-content" tabindex="-1"` so focus moves into it.
- Touch targets: buttons are at least 44px tall; keep other targets at least 24px or spaced apart (WCAG 2.5.8).
- `prefers-reduced-motion: reduce` switches off animations and smooth scrolling.

---

## 8. Performance notes

- No third-party requests for styles or fonts. Seven Latin `woff2` files total about 95 KB, loaded with `font-display: swap`; two are preloaded.
- Give every image `width` and `height` attributes to avoid layout shift.
- The two stylesheets are about 11.2 KB and 2.0 KB gzipped. Keep new CSS lean and remove rules you replace.
- Cached copies: GitHub Pages caches CSS for several minutes. After a deploy, a hard refresh may be needed to see changes.

---

## 9. Testing a CSS change

1. Serve the folder locally (`python3 -m http.server`) and open `index.html`, `services.html`, `contact.html` and a policy page.
2. Check both themes, using the toggle in the header.
3. Resize from 320px to 1920px. Check 320, 360, 600, 720, 900, 1024, 1180 and 1280 in particular. Nothing should scroll sideways, and the header should stay on one line above 640px.
4. Tab through the page with the keyboard. Focus must always be visible.
5. If you touch sector wording, run `python3 tools/sync_sectors.py --check`.
6. Run an accessibility checker (for example axe DevTools or Lighthouse) in both themes, and validate the HTML with the W3C Nu checker (`java -Xss1m -jar vnu.jar --errors-only *.html`).
