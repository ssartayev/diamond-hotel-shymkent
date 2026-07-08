#!/usr/bin/env python3
"""Download the curated royalty-free placeholder photos (Unsplash) as WebP.

Each entry maps to a semantic filename so swapping in official Diamond Hotel
photos later is a pure file replacement — no HTML changes. See IMAGES.md.
Every photo below was visually verified to match its slot.
"""
import os
import sys
import urllib.request

BASE = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

# slug -> (unsplash photo id, params)
PHOTOS = {
    # hero / home
    "hero/hero-main":        ("photo-1618773928121-c32242e63f39", "w=2000&q=68"),
    "hero/hero-mobile":      ("photo-1618773928121-c32242e63f39", "w=1100&q=70&fit=crop&ar=4:5"),
    # about / interiors
    "about/lobby":           ("photo-1621293954908-907159247fc8", "w=1200&q=72"),
    "about/facade":          ("photo-1551038247-3d9af20df552",    "w=1200&q=72"),
    "about/detail-bed":      ("photo-1505693416388-ac5ce068fe85", "w=900&q=72"),
    "about/gym":             ("photo-1534438327276-14e5300c3a48", "w=1200&q=72"),
    "about/interior":        ("photo-1566665797739-1674de7a421a", "w=1200&q=72"),
    "about/business":        ("photo-1590490359683-658d3d23f972", "w=1200&q=72"),
    # rooms
    "rooms/standard-double": ("photo-1631049307264-da0ec9d70304", "w=1200&q=72"),
    "rooms/standard-twin":   ("photo-1631049035182-249067d7618e", "w=1200&q=72"),
    "rooms/deluxe-balcony":  ("photo-1591088398332-8a7791972843", "w=1200&q=72"),
    "rooms/family-suite":    ("photo-1631049552057-403cdb8f0658", "w=1200&q=72"),
    "rooms/bathroom":        ("photo-1584622650111-993a426fbf0a", "w=900&q=72"),
    # dining
    "dining/restaurant":     ("photo-1517248135467-4c7edcad34c4", "w=1400&q=72"),
    "dining/breakfast":      ("photo-1478145046317-39f10e56b5e9", "w=1200&q=72&fit=crop&ar=4:3"),
    "dining/bar":            ("photo-1470337458703-46ad1756a187", "w=1200&q=72"),
    "dining/dish":           ("photo-1414235077428-338989a2e8c0", "w=900&q=72"),
    "dining/terrace":        ("photo-1560624052-449f5ddf0c31",    "w=1000&q=62"),
    "dining/coffee":         ("photo-1495474472287-4d71bcdd2085", "w=900&q=72"),
    "dining/evening":        ("photo-1519999482648-25049ddd37b1", "w=1200&q=72"),
    # events
    "events/conference":     ("photo-1540575467063-178a50c2df87", "w=1400&q=72"),
    "events/banquet":        ("photo-1519167758481-83f550bb49b3", "w=1200&q=72"),
    "events/meeting":        ("photo-1431540015161-0bf868a2d407", "w=1200&q=72"),
}

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


def fetch(slug: str, pid: str, params: str) -> tuple[str, int]:
    url = f"https://images.unsplash.com/{pid}?fm=webp&auto=compress&{params}"
    dest = os.path.join(BASE, slug + ".webp")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest, os.path.getsize(dest)


def main() -> None:
    failed = []
    for slug, (pid, params) in PHOTOS.items():
        try:
            _, size = fetch(slug, pid, params)
            kb = size // 1024
            print(f"ok  {slug}.webp  {kb} KB")
            if kb < 15:
                failed.append(slug)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {slug}: {e}")
            failed.append(slug)
    if failed:
        print("\nFAILED:", ", ".join(failed))
        sys.exit(1)
    print("\nAll images downloaded.")


if __name__ == "__main__":
    main()
