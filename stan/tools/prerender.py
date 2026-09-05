#!/usr/bin/env python3
"""Prerender the site build into one real HTML file per destination.

WHY THIS EXISTS

The hub's 120 destinations were hash fragments — #/m/shbg. A search engine
sees one page. STAN's first marketing channel is the question bank answering
searches nobody else answers (COMMERCIAL.md §4), and that channel does not
exist if the questions are not separately indexable. Sharing was broken the
same way: a link to a specific answer arrived as the homepage.

So each destination becomes /m/shbg/index.html, containing the fully rendered
markup, its own title, description and canonical link.

WHY A BROWSER RATHER THAN A PYTHON TEMPLATE

Rendering is already written once, in the page's own JavaScript. Writing it a
second time in Python would mean two renderers drifting apart, and the drift
would show up as pages that differ depending on how you arrived at them. So
this drives the real renderer: serve the site build, visit every route in
Chromium, and write out the DOM it produced. One renderer, no drift.

    python3 stan/tools/build.py --mode site
    python3 stan/tools/prerender.py
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import re
import socketserver
import sys
import threading
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SITE_PATH = ROOT / "data" / "site.yaml"

# Chromium is preinstalled in this environment; do not download another.
CHROMIUM = "/opt/pw-browsers/chromium"


class SPAHandler(http.server.SimpleHTTPRequestHandler):
    """Serve dist/, falling back to index.html so client routes resolve."""

    def translate_path(self, path):
        local = super().translate_path(path)
        p = Path(local)
        if p.is_dir():
            index = p / "index.html"
            return str(index) if index.exists() else str(DIST / "index.html")
        if not p.exists() and not p.suffix:
            return str(DIST / "index.html")
        return local

    def log_message(self, *args):
        pass


def serve(directory: Path):
    handler = functools.partial(SPAHandler, directory=str(directory))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, httpd.server_address[1]


def routes_from_build() -> list[str]:
    """Every destination, read from the data the page itself was built with."""
    data_js = (DIST / "data.js").read_text()
    blob = data_js[len("window.STAN_DATA="):].rstrip(";\n")
    data = json.loads(blob.replace("<\\/", "</"))
    return [""] + sorted(data["views"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if not (DIST / "index.html").exists():
        print("dist/index.html missing — run build.py --mode site first", file=sys.stderr)
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "playwright is not installed.\n"
            "  pip install playwright   (the browser itself is already present)",
            file=sys.stderr,
        )
        return 1

    site = yaml.safe_load(SITE_PATH.read_text())
    origin = site.get("origin", "").rstrip("/")
    if not site.get("origin_confirmed"):
        print(
            f"warning: data/site.yaml origin is the placeholder '{origin}'. "
            "Canonical links and sitemap.xml will be wrong until it is set.",
            file=sys.stderr,
        )

    paths = routes_from_build()
    httpd, port = serve(DIST)
    base = f"http://127.0.0.1:{port}"
    written, failures = 0, []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=CHROMIUM)
            page = browser.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda e: errors.append(str(e)))

            for route in paths:
                url = f"{base}/{route}/" if route else f"{base}/"
                before = len(errors)
                page.goto(url, wait_until="load")
                page.wait_for_timeout(60)

                title = page.title()
                if not title or (route and title == "STAN — Steroid Awareness Network"):
                    failures.append(f"{route or '/'}: head not set (title '{title}')")
                if len(errors) > before:
                    failures.append(f"{route or '/'}: {errors[-1]}")

                html = "<!doctype html>\n" + page.evaluate(
                    "document.documentElement.outerHTML"
                )
                out = DIST / route / "index.html" if route else DIST / "index.html"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(html)
                written += 1

            browser.close()
    finally:
        httpd.shutdown()

    # sitemap.xml — every destination, so the question bank is crawlable.
    urls = "".join(
        f"  <url><loc>{origin}/{r}/</loc></url>\n" if r
        else f"  <url><loc>{origin}/</loc></url>\n"
        for r in paths
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n"
    )

    (DIST / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {origin}/sitemap.xml\n"
    )

    if not args.quiet:
        print(f"Prerendered {written} page(s) into {DIST.relative_to(ROOT.parent)}")
        print(f"  sitemap.xml  {len(paths)} URLs")
        print("  robots.txt   written")

    if failures:
        print(f"\n{len(failures)} page(s) failed:", file=sys.stderr)
        for line in failures[:20]:
            print(f"  x {line}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
