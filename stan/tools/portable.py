#!/usr/bin/env python3
"""Produce one self-contained HTML file of the whole site.

Everything inline: data, styles, scripts and the webfonts as base64. No
network, no server, no link. Save it anywhere, email it, drop it in another
project, open it by double-clicking. It works offline and it does not expire.

    python3 stan/tools/build.py        # refresh prototype/index.html first
    python3 stan/tools/portable.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "prototype" / "index.html"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--no-fonts", action="store_true",
                    help="skip font inlining (offline build; type is substituted)")
    args = ap.parse_args()

    if not SOURCE.exists():
        print(f"{SOURCE} missing — run build.py first", file=sys.stderr)
        return 1

    # design-pdf.py already knows how to fetch and inline the fonts; reuse it
    # rather than keeping two copies of that logic.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "designpdf", ROOT / "tools" / "design-pdf.py")
    dp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dp)

    html = SOURCE.read_text(encoding="utf-8")
    if args.no_fonts:
        print("Skipping fonts — the file will fall back to system type.")
    else:
        print("Fetching fonts...")
        html = dp.inline_fonts(html)

    stamp = dt.date.today().isoformat()
    out = args.out or ROOT / "dist" / f"stan-site-{stamp}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    size = out.stat().st_size / 1_000_000
    external = "fonts.googleapis" in html or "fonts.gstatic" in html
    print(f"Wrote {out.relative_to(ROOT.parent)} — {size:.1f} MB")
    print("  self-contained: " + ("NO, still references Google Fonts"
                                  if external else "yes, works offline"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
