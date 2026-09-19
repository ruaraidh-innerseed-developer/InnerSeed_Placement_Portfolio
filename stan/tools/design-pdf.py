#!/usr/bin/env python3
"""Render the prototype to a PDF anyone can be shown, without a browser.

For handing the design to a person who is not going to click a link — a
prospective clinical partner, a funder, someone whose opinion is wanted before
the site is public.

Fonts are downloaded and inlined as data URIs first. Without that step the
capture falls back to Georgia and Arial, and the person looking at it is
judging a design STAN is not proposing.

    python3 stan/tools/design-pdf.py
    python3 stan/tools/design-pdf.py --look reverse --out /tmp/alt.pdf
"""

from __future__ import annotations

import argparse
import base64
import io
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "prototype" / "index.html"
DEFAULT_OUT = ROOT / "dist" / "stan-design.pdf"
CHROMIUM = "/opt/pw-browsers/chromium"

WIDTH = 1280          # capture width in CSS pixels
SCALE = 2             # device pixel ratio, so the PDF is not soft
PAGE_RATIO = 1.414    # slice long captures to roughly A4 proportions

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0 Safari/537.36")

FONT_CSS = ("https://fonts.googleapis.com/css2"
            "?family=Archivo:wght@400;500;600"
            "&family=Bitter:wght@600;700"
            "&family=IBM+Plex+Mono:wght@400;500&display=swap")

# What to capture, in order. Each becomes one section of the PDF.
SHOTS = [
    ("",                      "Home"),
    ("#/p/what-costs",        "What costs money here, and why"),
    ("#/o/walkthrough",       "A service page — bloods walkthrough"),
    ("#/m/shbg",              "A marker page — the empty state as a destination"),
    ("#/g/cohort-comingoff",  "A group page — the coming-off cohort"),
    ("#/q/how-do-i-come-off-safely", "A catalogued question, not yet answered"),
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def inline_fonts(html: str) -> str:
    """Replace the Google Fonts link with @font-face rules carrying the files."""
    css = fetch(FONT_CSS).decode()
    for font_url in sorted(set(re.findall(r"https://fonts\.gstatic\.com[^)]+", css))):
        try:
            data = base64.b64encode(fetch(font_url)).decode()
        except Exception as exc:                      # noqa: BLE001
            print(f"  ! could not fetch {font_url.rsplit('/', 1)[-1]}: {exc}",
                  file=sys.stderr)
            continue
        kind = "woff2" if font_url.endswith(".woff2") else "truetype"
        css = css.replace(font_url, f"data:font/{kind};base64,{data}")

    html = re.sub(
        r'<link rel="preconnect"[^>]*>\s*', "", html)
    html = re.sub(
        r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">',
        f"<style>{css}</style>", html)
    return html


def slice_tall(img, page_h: int):
    """Cut one long capture into page-sized pieces so it reads like a document."""
    from PIL import Image
    if img.height <= page_h:
        return [img]
    pieces = []
    top = 0
    while top < img.height:
        bottom = min(top + page_h, img.height)
        piece = img.crop((0, top, img.width, bottom))
        if piece.height < page_h:                     # pad the last one
            padded = Image.new("RGB", (img.width, page_h), (234, 236, 233))
            padded.paste(piece, (0, 0))
            piece = padded
        pieces.append(piece)
        top = bottom
    return pieces


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--look", default="stan",
                    choices=("stan", "paper", "reverse", "mixed"))
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--no-fonts", action="store_true",
                    help="skip font inlining (offline; type will be substituted)")
    args = ap.parse_args()

    if not SOURCE.exists():
        print(f"{SOURCE} missing — run build.py first", file=sys.stderr)
        return 1
    try:
        from PIL import Image
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        print(f"missing dependency: {exc}\n  pip install pillow playwright",
              file=sys.stderr)
        return 1

    html = SOURCE.read_text()
    if args.no_fonts:
        print("Skipping fonts — the capture will not show STAN's typography.")
    else:
        print("Fetching fonts...")
        html = inline_fonts(html)

    staged = ROOT / "dist" / "_pdf-source.html"
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_text(html)

    page_h = int(WIDTH * SCALE * PAGE_RATIO)
    pages = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page(viewport={"width": WIDTH, "height": 900},
                                device_scale_factor=SCALE)
        base = staged.as_uri()

        for frag, label in SHOTS:
            page.goto(base + frag, wait_until="load")
            page.wait_for_timeout(400)
            page.evaluate(
                "look => { const b = document.querySelector("
                "`#looks button[data-look='${look}']`); if (b) b.click(); }",
                args.look)
            # The prototype bar and the look switcher are scaffolding, not design.
            page.evaluate(
                "() => { const p = document.querySelector('.protobar');"
                " if (p) p.style.display = 'none'; }")
            page.wait_for_timeout(250)
            shot = page.screenshot(full_page=True)
            img = Image.open(io.BytesIO(shot)).convert("RGB")
            pieces = slice_tall(img, page_h)
            pages.extend(pieces)
            print(f"  {label:<52} {len(pieces)} page(s)")

        # One mobile capture, because most of this audience is on a phone.
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(base, wait_until="load")
        page.wait_for_timeout(400)
        page.evaluate("() => { const p = document.querySelector('.protobar');"
                      " if (p) p.style.display = 'none'; }")
        mob = Image.open(io.BytesIO(page.screenshot(full_page=True))).convert("RGB")
        canvas = Image.new("RGB", (WIDTH * SCALE, page_h), (234, 236, 233))
        ratio = min((page_h - 80) / mob.height, 1.0)
        mob = mob.resize((max(1, int(mob.width * ratio)),
                          max(1, int(mob.height * ratio))))
        canvas.paste(mob, ((canvas.width - mob.width) // 2, 40))
        pages.append(canvas)
        print(f"  {'Home, on a phone':<52} 1 page(s)")

        browser.close()

    staged.unlink(missing_ok=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    pages[0].save(args.out, save_all=True, append_images=pages[1:],
                  resolution=SCALE * 72)
    size = args.out.stat().st_size / 1_000_000
    print(f"\nWrote {args.out.relative_to(ROOT.parent)} "
          f"— {len(pages)} pages, {size:.1f} MB, look '{args.look}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
