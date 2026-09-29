#!/usr/bin/env python3
"""Report how complete the STAN marker encyclopedia is.

Two views, because there are two sensible ways to work:

  by marker  — finish one record at a time
  by field   — sweep one field across every record, which is usually faster
               and produces more consistent writing

    python3 stan/tools/coverage.py
    python3 stan/tools/coverage.py --by field
    python3 stan/tools/coverage.py --marker lh      # what's missing here
    python3 stan/tools/coverage.py --next           # suggest what to do next
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MARKERS_DIR = ROOT / "knowledge" / "markers"

# Field path -> label. A state counts as filled when its required subfield has
# content; a list or string counts when it is non-empty.
COVERAGE = [
    ("what_it_is",            "What it is"),
    ("made_where",            "Where it's made"),
    ("controlled_by",         "What controls it"),
    ("functions",             "What it does"),
    ("on_a_panel.range_note", "Range note"),
    ("states.high.meaning",   "When it's high"),
    ("states.low.meaning",    "When it's low"),
    ("states.suppressed.what_happens", "When suppressed"),
    ("states.recovery.what_is_known",  "Recovery"),
    ("does_not_tell_you",     "What it doesn't tell you"),
]

BAR_WIDTH = 24


def dig(obj, path):
    for part in path.split("."):
        if not isinstance(obj, dict):
            return None
        obj = obj.get(part)
    return obj


def filled(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def bar(done, total):
    if not total:
        return " " * BAR_WIDTH
    n = round(BAR_WIDTH * done / total)
    return "█" * n + "·" * (BAR_WIDTH - n)


def load():
    markers = {}
    for path in sorted(MARKERS_DIR.glob("*.yaml")):
        rec = yaml.safe_load(path.read_text())
        if isinstance(rec, dict):
            markers[rec.get("id", path.stem)] = rec
    return markers


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--by", choices=["marker", "field"], default="marker")
    ap.add_argument("--marker", help="show what is missing from one record")
    ap.add_argument("--next", action="store_true", dest="suggest",
                    help="suggest the highest-leverage next thing to write")
    args = ap.parse_args()

    markers = load()
    if not markers:
        print(f"No markers in {MARKERS_DIR}", file=sys.stderr)
        return 1

    grid = {
        mid: {path: filled(dig(rec, path)) for path, _ in COVERAGE}
        for mid, rec in markers.items()
    }
    total_cells = len(markers) * len(COVERAGE)
    done_cells = sum(v for row in grid.values() for v in row.values())

    if args.marker:
        mid = args.marker
        if mid not in markers:
            print(f"No marker '{mid}'. Have: {', '.join(sorted(markers))}",
                  file=sys.stderr)
            return 1
        rec = markers[mid]
        print(f"{rec.get('name', mid)} — {rec.get('full_name', '')}")
        print(f"status: {rec.get('fill_status')}\n")
        for path, label in COVERAGE:
            mark = "filled  " if grid[mid][path] else "MISSING "
            print(f"  {mark}{label}")
        return 0

    if args.suggest:
        # The field that is missing from the most records is the best sweep.
        gaps = [
            (sum(1 for m in grid if not grid[m][path]), path, label)
            for path, label in COVERAGE
        ]
        gaps.sort(reverse=True)
        n, path, label = gaps[0]
        missing = [m for m in sorted(grid) if not grid[m][path]]
        print(f'Highest-leverage sweep: "{label}"')
        print(f"  missing from {n} of {len(markers)} markers\n")
        print("  " + ", ".join(missing))
        print(f"\nWriting one field across every record keeps the voice consistent")
        print("and is usually faster than finishing records one at a time.")
        return 0

    if args.by == "field":
        print(f"Coverage by field — {done_cells}/{total_cells} "
              f"({100 * done_cells // total_cells}%)\n")
        rows = []
        for path, label in COVERAGE:
            done = sum(1 for m in grid if grid[m][path])
            rows.append((done, label))
        for done, label in rows:
            print(f"  {label:<28} {bar(done, len(markers))} {done:>2}/{len(markers)}")
        return 0

    print(f"Coverage by marker — {done_cells}/{total_cells} "
          f"({100 * done_cells // total_cells}%)\n")
    order = sorted(
        markers,
        key=lambda m: (-sum(grid[m].values()), m),
    )
    for mid in order:
        done = sum(grid[mid].values())
        status = markers[mid].get("fill_status", "?")
        print(f"  {mid:<20} {bar(done, len(COVERAGE))} {done:>2}/{len(COVERAGE)}  {status}")

    print(f"\n{len(markers)} markers · run --by field to see which section to sweep,")
    print("or --next for a suggestion.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
