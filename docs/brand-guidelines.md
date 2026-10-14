# Brand Guidelines

Reference for anyone creating new marketing materials, web pages, or documents for Jopetnah International Limited, so new work stays visually and tonally consistent with what already exists (website, letterhead, company profile, and social media assets).

## Logo

The mark is a stylized "j" set inside a globe, wrapped by an orbit ring — literally depicting "Empowering Businesses, Worldwide."

- **Icon-only mark** (globe + "j", no wordmark) is the primary version used across the website nav, favicon, and social profile photo. This was a deliberate choice over the full wordmark logo: the icon reads clearly at small sizes (nav bar, favicon, circular social avatars) where a full wordmark would become illegible.
- **Full wordmark lockup** (icon + "JOPETNAH INTERNATIONAL LIMITED" text) is used on the letterhead and the README banner, where there's more horizontal space to work with.
- When rendering the company name as text (not the logo image), split the coloring: **"JOPETNAH" in blue, "INTERNATIONAL LIMITED" in red** — established on the letterhead and carried through consistently.

**Minimum clear space:** keep at least the height of the "j" stroke as empty margin around the mark on all sides. Don't crop the orbit ring.

## Color Palette

These are defined as CSS custom properties in `css/style.css` — always reference the variable, never hardcode the hex value in new CSS:

| Variable | Hex | Use |
|---|---|---|
| `--navy` | `#1B1E23` | Primary text, headings |
| `--red` | `#E0151B` | Brand accent, "INTERNATIONAL LIMITED" text, alternating accents |
| `--blue` | `#0E86D4` | Brand accent, "JOPETNAH" text, links, primary interactive color |
| `--blue-tint` | `#EAF4FC` | Light card/section backgrounds |
| `--red-tint` | `#FDEAEA` | Light card/section backgrounds (alternates with blue-tint) |
| `--hairline` | `#E3E5E8` | Borders, dividers |
| `--gray` | `#53555B` | Secondary/body text |
| `--lgray` | `#8A8D93` | Muted/tertiary text, placeholders |
| `--paper` | `#FBFBFC` | Off-white section backgrounds |
| `--white` | `#FFFFFF` | Base background |

**Signature gradient:** red → blue (`linear-gradient(90deg, #E0151B, #0E86D4)`), used as a recurring accent rule under headings, on primary buttons, and framing the Facebook cover photo. This pairing (rather than either color alone) is the most recognizable brand signature — use it for section dividers and emphasis bands, not for large background fills.

**What to avoid:** don't introduce new accent colors (e.g., gold, green) without a specific reason — the two-color red/blue system is deliberately minimal and is what makes materials instantly recognizable as Jopetnah's across the website, letterhead, and social presence.

## Typography

| Font | Use | Fallback stack |
|---|---|---|
| **Poppins** (weights 400–700) | Headings, navigation, buttons, labels, company name | `'Segoe UI', sans-serif` |
| **Lora** (regular + italic) | Body paragraphs, taglines | `Georgia, serif` |

This pairing — a geometric sans for structure/headings alongside a warm serif for body text — is intentional: Poppins gives the geometric, "global/orbit" feel that matches the logo mark, while Lora adds institutional warmth to long-form text (About/Sustainability copy) rather than reading as cold or purely corporate.

**For print documents (letterhead, Word docs):** use **Cambria** (headings) and **Calibri** (body/footer text) instead — these are guaranteed available in Microsoft Word, whereas Poppins/Lora are web fonts loaded from Google Fonts and may not render identically across all desktop software.

## Voice & Tone

Established across the website, letterhead copy, and company profile:

- **Lead with concrete numbers, not adjectives.** "15 divisions, 20+ countries" lands better than "a leading, world-class provider." This was a deliberate correction made early in the site's copywriting — avoid words like "premier," "world-class," or "leading" as the primary claim; let scale and specificity do the work instead.
- **Institutional, not stiff.** Full sentences, professional register — but not so dense or jargon-heavy that it reads like a legal filing. The Sustainability page content is a good register reference: substantive but readable.
- **One clear call-to-action per section**, not three competing ones. Home page CTAs are deliberately limited to "Explore Our Services" + "Let's Collaborate" rather than a longer list of buttons.
- **Tagline usage:** "Empowering Businesses, Worldwide" is the primary tagline and should appear on all major brand touchpoints (site header area, letterhead, social profiles). Avoid inventing alternate taglines for individual campaigns unless there's a specific reason — consistency here is more valuable than novelty.

## Component Patterns (Website)

For anyone extending the site, these are the established reusable patterns — reuse them rather than inventing new ones for the same purpose:

- **`.pillar`** — bordered card, used for the 4 business pillars on Home
- **`.value-card`** — tinted background card (alternating blue-tint/red-tint), used for Core Values and "Jopetnah Advantage" grids
- **`.accordion-item`** — expand/collapse pattern, used for the 16 sectors on the Services page
- **`.chip-list` / `.tag-cloud`** — pill-shaped tags, used for "Core Services" lists and country/city presence lists
- **`.cta-band`** — full-width gradient band with centered heading + buttons, used to close out most pages
- **`.orbit-*`** classes — the literal orbit-ring world map on the homepage hero; this is the site's one deliberately bold, illustrative moment. Don't add additional large illustrations elsewhere — the orbit graphic works precisely because it's the *only* big visual flourish on an otherwise disciplined, text-forward site.

## Photography (when added)

Not yet in place as of this writing. When sourcing images:
- **Only use free-to-use sources** (Unsplash, Pexels, Pixabay) or properly licensed stock — never pull images directly from generic web search results, which are predominantly copyrighted stock-agency previews (Alamy, iStock, Getty) requiring a paid license
- Favor authentic, specific imagery over generic "handshake"/stock-business-people clichés
- Maintain the same restraint as the rest of the site — photography should support the content, not overwhelm the minimal aesthetic established elsewhere
