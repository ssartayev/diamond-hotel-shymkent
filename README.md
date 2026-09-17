# Diamond Hotel Shymkent — Official Website

Production website for Diamond Hotel Shymkent, a real 4★ hotel in Shymkent,
Kazakhstan (opened 2024, rated 4.8★ from 1300+ reviews on 2GIS).

Russian-language, mobile-first, and built with **zero runtime dependencies** —
the output is plain HTML/CSS/JS that deploys to any static host.

![Diamond Hotel Shymkent](assets/img/hero/hero-main.webp)

[Русская версия README →](README.ru.md)

---

## What it is

Nine pages — home, rooms, restaurant, events, gallery, about, reviews, contacts,
and a 404 — covering everything a guest needs before booking.

Booking deliberately routes to 2GIS, WhatsApp and phone rather than a custom
booking engine. The hotel already takes reservations through those channels, so
building a booking system would have added failure modes without adding bookings.

## How it is built

The machine this was developed on has **no Node.js**, so instead of reaching for
a JavaScript framework the site uses a **small static site generator written in
Python with no third-party packages**:

```
tools/
  build.py       the generator
  pages/         per-page content
  partials/      shared header, footer, meta blocks
```

```bash
python3 tools/build.py    # rebuild all HTML after editing content
```

Shared markup lives in one place, so a change to the header updates all nine
pages instead of nine copies drifting apart.

## Design system

A documented design system in `design-system/MASTER.md` defines the type scale,
spacing and palette:

- **Typography** — Prata for headings, Manrope for body, both with Cyrillic support
- **Palette** — porcelain, ink and bronze
- **Images** — WebP throughout, sized for mobile-first delivery

## Engineering notes

Two problems worth recording:

**`backdrop-filter` breaks `position: fixed` children.** Applying
`backdrop-filter` to the fixed header made it the containing block for the fixed
mobile menu, so the menu was trapped inside the header instead of covering the
screen. Fix: the menu must be a **sibling** of `<header>`, not a child.

**Performance-first images.** All photography is WebP with explicit dimensions to
avoid layout shift, and the hero ships separate desktop and mobile crops instead
of downscaling one large file.

## Tech stack

HTML5 · CSS3 (custom properties, grid, flexbox) · vanilla JavaScript ·
Python 3 static site generator · WebP assets · semantic markup with Open Graph
and sitemap for SEO

## Project layout

```
index.html  rooms.html  restaurant.html  events.html
gallery.html  about.html  reviews.html  contacts.html  404.html
assets/
  css/  js/  img/
design-system/
  MASTER.md          type scale, palette, spacing rules
tools/
  build.py  pages/  partials/
IMAGES.md            image inventory and replacement map
```
