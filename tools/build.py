#!/usr/bin/env python3
"""Static site builder for Diamond Hotel Shymkent. Zero dependencies.

Sources:  tools/pages/*.html   (page content + meta block)
Partials: tools/partials/*.html ({{> name}} includes, e.g. {{> header}})
Layout:   tools/partials/layout.html
Output:   repo root *.html (deploy-ready, plain static files)

Usage: python3 tools/build.py
"""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
PAGES = os.path.join(ROOT, "tools", "pages")
PARTIALS = os.path.join(ROOT, "tools", "partials")

# Change when the hotel's real domain is connected (used for canonical/OG/sitemap).
SITE_URL = "https://diamond-hotel-shymkent.kz"

# Single source of truth for facts used across partials and pages.
GLOBALS = {
    "site_name": "Diamond Hotel Shymkent",
    "phone_pretty": "+7 700 505 75 75",
    "phone_href": "tel:+77005057575",
    "whatsapp_href": "https://wa.me/77005057575",
    "telegram_href": "https://t.me/+77005057575",
    "instagram_href": "https://www.instagram.com/diamond_hotel_shymkent",
    "gis_href": "https://2gis.kz/shymkent/firm/70000001075202985",
    "gis_reviews_href": "https://2gis.kz/shymkent/firm/70000001075202985/tab/reviews",
    "address": "Шымкент, Каратауский район, тупик Мирас, 424",
    "rating": "4,8",
    "ratings_count": "1 300+",
    "site_url": SITE_URL,
}

NAV_KEYS = ["home", "rooms", "restaurant", "events", "about", "gallery", "reviews", "contacts"]

META_RE = re.compile(r"^<!--meta\s*(.*?)-->\s*", re.S)
PARTIAL_RE = re.compile(r"\{\{>\s*([\w-]+)\s*\}\}")
VAR_RE = re.compile(r"\{\{\s*([\w-]+)\s*\}\}")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_meta(src: str) -> tuple[dict, str]:
    m = META_RE.match(src)
    if not m:
        sys.exit("page missing <!--meta ...--> block")
    meta = {}
    for line in m.group(1).strip().splitlines():
        line = line.strip()
        if line and "=" in line:
            k, v = line.split("=", 1)
            meta[k.strip()] = v.strip()
    return meta, src[m.end():]


def expand(text: str, ctx: dict, depth: int = 0) -> str:
    if depth > 6:
        sys.exit("partial recursion too deep")
    text = PARTIAL_RE.sub(
        lambda m: expand(read(os.path.join(PARTIALS, m.group(1) + ".html")), ctx, depth + 1),
        text,
    )
    return VAR_RE.sub(lambda m: str(ctx.get(m.group(1), "")), text)


def build_page(fname: str) -> str:
    meta, content = parse_meta(read(os.path.join(PAGES, fname)))
    out_name = meta.get("out", fname)
    ctx = dict(GLOBALS)
    ctx.update(meta)
    ctx.setdefault("body_class", "")
    ctx.setdefault("og_image", "/assets/img/hero/hero-main.webp")
    ctx["page_url"] = SITE_URL + ("/" if out_name == "index.html" else "/" + out_name)
    # nav active flags
    active = meta.get("active", "")
    for key in NAV_KEYS:
        ctx[f"active_{key}"] = ' aria-current="page"' if key == active else ""
    ctx["content"] = expand(content, ctx)
    html = expand(read(os.path.join(PARTIALS, "layout.html")), ctx)
    with open(os.path.join(ROOT, out_name), "w", encoding="utf-8") as f:
        f.write(html)
    return out_name


def write_seo_files(pages: list[str]) -> None:
    urls = []
    for p in sorted(pages):
        if p == "404.html":
            continue
        loc = SITE_URL + ("/" if p == "index.html" else "/" + p)
        urls.append(f"  <url><loc>{loc}</loc></url>")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")


def main() -> None:
    pages = [f for f in sorted(os.listdir(PAGES)) if f.endswith(".html")]
    built = [build_page(f) for f in pages]
    write_seo_files(built)
    print(f"built {len(built)} pages: " + ", ".join(built))


if __name__ == "__main__":
    main()
