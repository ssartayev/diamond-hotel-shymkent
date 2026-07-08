# Diamond Hotel Shymkent — Design System (Master)

Generated with ui-ux-pro-max design intelligence. This file is the source of truth
for every visual decision on the site. Page-level deviations live in `pages/`.

## Positioning

Premium modern business hotel, opened 2024. Not palatial luxury — quiet, warm,
confident. The design must communicate: trust, comfort, elegance, premium service,
business convenience, hospitality of southern Kazakhstan.

Pattern: **Hero-Centric + Social Proof** (real 4.8★ / 1 329 ratings on 2GIS is the
strongest conversion asset — surface it everywhere).

Style: **Quiet luxury / exaggerated minimalism, adapted**: generous negative space
on desktop, compact rhythm on mobile, oversized Prata display headings, thin rules,
champagne-bronze accents used sparingly.

## Color tokens

Warm porcelain base + deep ink + champagne bronze. Single light theme with dark
inverted sections (hero overlays, footer) — consistent brand presentation.

| Token          | Hex       | Usage                                        |
|----------------|-----------|----------------------------------------------|
| `--ink`        | `#1C2430` | Headings, body strong, primary buttons       |
| `--text`       | `#3D4653` | Body text on light (≥9:1)                    |
| `--text-2`     | `#6A7280` | Secondary text, captions (≥4.5:1)            |
| `--bg`         | `#FAF8F5` | Page background (warm porcelain)             |
| `--surface`    | `#FFFFFF` | Cards, sheets                                |
| `--line`       | `#E7E1D6` | Hairline borders, dividers                   |
| `--bronze`     | `#A98A56` | Large accents, icons, stars, hover states    |
| `--bronze-deep`| `#8A6C3C` | Small accent text on light (≥4.5:1)          |
| `--dark`       | `#141B24` | Footer, dark sections                        |
| `--dark-2`     | `#1B2531` | Cards on dark                                |
| `--on-dark`    | `#EDE8DF` | Text on dark                                 |
| `--on-dark-2`  | `#A7ADB8` | Secondary text on dark                       |
| `--gold-dark`  | `#C9A96A` | Accent on dark (≥5:1)                        |

Rules: bronze is an accent, never a full CTA background (contrast). Primary CTA =
ink button, white text. On dark = white/`--gold-dark` outline or light button.

## Typography

- **Headings / prices:** Prata (Cyrillic ✓), regular only. Tight leading (1.08–1.2),
  slight negative tracking on display sizes.
- **Body / UI:** Manrope variable (Cyrillic ✓), 400/500/600/700. Line-height 1.6.
- **Eyebrow labels:** Manrope 600, 12–13px, uppercase, letter-spacing 0.16–0.2em,
  `--bronze-deep`.
- Self-hosted woff2 (latin + cyrillic subsets), `font-display: swap`.

Scale (fluid): display `clamp(2.1rem, 6.5vw, 3.9rem)`; h2 `clamp(1.55rem, 4.2vw, 2.4rem)`;
h3 `1.18–1.35rem`; body `1rem/1.6`; small `0.875rem`. Prices: Prata with tabular
feel (spaces as thousand separators: «от 25 000 ₸»).

## Spacing & layout

4/8px rhythm. Section padding: 56–64px mobile → 104px desktop. Container:
`max-width: 1180px`, gutters 20px mobile / 32px tablet / 48px desktop.
Mobile-first; merge related content, horizontal snap-scroll rows for card sets on
mobile to fight vertical scroll. Radius: 16px cards, 12px small, 999px pills.
Shadows: one soft ambient level only (`0 10px 30px -12px rgb(28 36 48 / .12)`),
elevation via hairlines + tone, not stacked shadows.

## Motion

Subtle (3/10). Durations 200–500ms, ease-out `cubic-bezier(.22,.61,.36,1)`.
- Reveal-on-scroll: fade + 12px rise, stagger 60ms, IntersectionObserver, once.
- Images: gentle zoom on hover (scale 1.05, 700ms) inside fixed-ratio crops.
- Header: tone shift after scroll. Drawer/modal: 280ms slide+fade.
- Everything gated behind `prefers-reduced-motion`.
- No parallax, no scroll-jacking, max 1–2 animated elements per view.

## Components

Buttons (44px+ touch): `.btn-primary` ink→hover lift; `.btn-ghost` hairline;
`.btn-light` on dark. Cards: room card (4:3 photo, name, facts row, price, CTA),
review card (stars, quote, name, «2ГИС» source chip), amenity tile (SVG icon
+ label). Booking sheet: bottom-sheet on mobile / centered dialog on desktop with
three actions: 2ГИС (primary, rating badge), WhatsApp, phone. Lightbox for gallery.
Icons: single stroke set (Lucide-style, 1.75px stroke), never emoji.

## Anti-patterns (avoid)

Poor photos, complex booking flows, bronze-on-white small text below 4.5:1,
generic hotel template look, parallax, more than one primary CTA per view.
