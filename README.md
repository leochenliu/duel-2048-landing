# Duel 2048 — Promo Landing Page

Single-file SEO landing page for [Duel 2048](https://lp2048.767880.xyz/) (promo) — game itself lives at `https://duel-2048.leochenliu.workers.dev/`.

## What's in here

```
duel-2048-landing/
├── index.html          # The landing page (single-page, semantic HTML)
├── style.css           # All styles — vanilla CSS, no frameworks
├── robots.txt
├── sitemap.xml
├── assets/
│   └── favicon.svg     # 64×64 SVG favicon (mirrors the dual-board motif)
└── README.md           # this file
```

## What's inside `index.html`

- **SEO**: title, meta description, keywords, canonical, robots
- **Social cards**: Open Graph + Twitter Card (uses `./assets/og.png`)
- **Structured data**: `VideoGame` + `FAQPage` JSON-LD for Google rich results
- **Content sections**:
  - Hero with a CSS-rendered mock of the dual-board + event stream
  - "How it works" (4 steps)
  - "Five sync modes" (5 cards, Lockstep highlighted)
  - "Why this matters" (4 cards + a pull-quote)
  - FAQ (7 questions, optimized for featured snippets)
  - Press kit + copy-paste snippets for X / Reddit / HN / Product Hunt / streamers
  - Final CTA band
- **A11y**: skip-link, semantic landmarks, focus styles, ARIA labels
- **No JavaScript required** (the page works without it; native `<details>` for collapsibles)
- **No external dependencies** — no fonts, no CDN, no trackers

## Generate the OG image (one-time)

The HTML references `./assets/og.png` (1200×630). You need to create it once.

### Option A — Python (Pillow)

```bash
pip install Pillow
python make_og.py        # see script below
```

### Option B — Use the included og-generator.html

Open `og-generator.html` in a browser at 1200×630 viewport (or use a tool like
[Puppeteer](https://pptr.dev/), [Polypane](https://polypane.app/), or Chrome DevTools' device
emulator at 1200×630) and save a PNG.

After generating, drop it at `./assets/og.png` and update the path in `index.html`
if you change the filename.

## Deploy

This is a static site. Drop the folder on any static host:

| Host | Steps |
|---|---|
| **Cloudflare Pages** | Push to a GitHub repo → Pages → connect → no build command needed. |
| **Cloudflare Workers (existing)** | Bundle `index.html`, `style.css`, `assets/`, `robots.txt`, `sitemap.xml` into your worker's static-asset handler (your existing `/` route already serves `index.html`). |
| **GitHub Pages** | Commit to a repo, enable Pages on the branch. |
| **Netlify / Vercel** | Drag-and-drop the directory; zero config. |
| **Any static server** | `python -m http.server` works out of the box. |

## After deploy — promotional checklist

Use the snippets already in the **Press kit** section (`#press` in `index.html`):

1. **X / Twitter** — paste the tweet snippet, attach `assets/og.png`
2. **Reddit** — `r/indiegaming`, `r/AI_Games`, `r/ArtificialIntelligence`, `r/webgames`
3. **Hacker News** — "Show HN" with the HN-formatted snippet
4. **Product Hunt** — maker-side submission
5. **Indie game newsletters / YouTube curators** — use the long description
6. **Submit the URL to Google Search Console** for indexing

## Customization

Search `index.html` for `lp2048.767880.xyz` (landing page URL) and `duel-2048.leochenliu.workers.dev` (game URL) and replace both if you redeploy on different domains.
on a different domain. Everything else (title, description, OG) is inline.