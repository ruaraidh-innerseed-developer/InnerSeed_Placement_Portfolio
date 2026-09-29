#!/usr/bin/env python3
"""Render the evidence register as a reviewable literature list.

Writes LITERATURE.md — a generated, always-current bibliography of everything
STAN holds, what state each item is in, and what each may be used to claim.

    python3 stan/tools/bibliography.py            # write LITERATURE.md
    python3 stan/tools/bibliography.py --stdout   # print instead
    python3 stan/tools/bibliography.py --check    # fail if out of date
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "evidence" / "sources"
OUT = ROOT / "LITERATURE.md"

# Reading order: what to pick up next is a function of state, not of interest.
STATE_ORDER = ["approved", "in-review", "added", "screened-out", "retired"]

STATE_LABEL = {
    "approved":     "Approved — citable",
    "in-review":    "Read, in review",
    "added":        "Held, not yet read",
    "screened-out": "Screened out",
    "retired":      "Retired",
}


def load() -> list:
    records = []
    for path in sorted(SOURCES_DIR.glob("*.yaml")):
        rec = yaml.safe_load(path.read_text())
        if isinstance(rec, dict):
            records.append(rec)
    return records


def cite(r: dict) -> str:
    authors = r.get("authors") or []
    if len(authors) > 3:
        who = f"{authors[0]} et al."
    else:
        who = ", ".join(authors)
    title = " ".join(str(r.get("title", "")).split())
    return f"{who} *{title}*. {r.get('venue')}, {r.get('year')}."


def ident(r: dict) -> str:
    ids = r.get("identifiers") or {}
    bits = []
    for key, label in (("doi", "doi"), ("pmid", "PMID"), ("pmcid", "PMC"),
                       ("isbn", "NCBI")):
        if ids.get(key):
            bits.append(f"{label}:{ids[key]}")
    if ids.get("url") and not bits:
        bits.append(ids["url"])
    return " · ".join(bits)


def render(records: list) -> str:
    today = dt.date.today().isoformat()
    total = len(records)
    read = sum(1 for r in records
               if (r.get("verification") or {}).get("full_text_read"))
    approved = sum(1 for r in records
                   if (r.get("review") or {}).get("status") == "approved")

    out = [
        "# Literature held by STAN",
        "",
        f"**Generated {today} by `tools/bibliography.py`. Do not edit by hand** —",
        "regenerate it. The register at `evidence/sources/` is the source of truth.",
        "",
        f"**{total} items · {read} read in full · {approved} approved for citation**",
        "",
        "Nothing may be cited in published content until it is approved, which",
        "requires the full text read and a named clinical reviewer",
        "(`governance/EVIDENCE-POLICY.md` §4, §8). Items screened out are kept",
        "rather than deleted — a register that shows what was considered and",
        "rejected is worth more than one that only shows what survived.",
        "",
        "---",
        "",
    ]

    by_state: dict[str, list] = {}
    for r in records:
        st = (r.get("review") or {}).get("status", "added")
        by_state.setdefault(st, []).append(r)

    for state in STATE_ORDER:
        rows = by_state.get(state)
        if not rows:
            continue
        out.append(f"## {STATE_LABEL.get(state, state)} ({len(rows)})")
        out.append("")

        rows.sort(key=lambda r: (str(r.get("year", "")), str(r.get("title", ""))))
        for r in rows:
            level = r.get("evidence_level") or {}
            rel = r.get("population_relevance") or {}
            ver = r.get("verification") or {}

            out.append(f"### {r.get('id')}")
            out.append("")
            out.append(cite(r))
            out.append("")
            meta = [
                f"`{r.get('type', '?')}`",
                f"grade **{level.get('grade', '?')}**",
                f"relevance **{rel.get('rating', '?')}**",
                f"bibliography **{ver.get('bibliographic', '?')}**",
                "**read**" if ver.get("full_text_read") else "**unread**",
            ]
            out.append(" · ".join(meta))
            identifiers = ident(r)
            if identifiers:
                out.append("")
                out.append(f"`{identifiers}`")

            supported = r.get("claims_supported") or []
            not_supported = r.get("claims_not_supported") or []
            if supported:
                out.append("")
                out.append("**May be cited for**")
                for c in supported:
                    out.append(f"- {' '.join(str(c).split())}")
            if not_supported:
                out.append("")
                out.append("**Must NOT be cited for**")
                for c in not_supported:
                    out.append(f"- {' '.join(str(c).split())}")

            notes = " ".join(str(r.get("notes", "")).split())
            if notes:
                out.append("")
                out.append(f"> {notes}")
            out.append("")
            out.append("---")
            out.append("")

    if read < total:
        out += [
            "## What to read next",
            "",
            "Unread items, in the order they unblock the most:",
            "",
        ]
        unread = [r for r in records
                  if not (r.get("verification") or {}).get("full_text_read")
                  and (r.get("review") or {}).get("status") != "screened-out"]
        # Open access first — no barrier, so no excuse.
        unread.sort(key=lambda r: (not r.get("open_access"), str(r.get("year", ""))))
        for r in unread:
            oa = "free" if r.get("open_access") else "may be paywalled"
            out.append(f"- **{r.get('id')}** — {oa}")
        out.append("")

    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    records = load()
    if not records:
        print(f"No source records in {SOURCES_DIR}", file=sys.stderr)
        return 1
    text = render(records)

    if args.stdout:
        print(text)
        return 0
    if args.check:
        current = OUT.read_text() if OUT.exists() else ""
        # The generated date changes daily; compare everything else.
        strip = lambda s: "\n".join(l for l in s.splitlines()
                                    if not l.startswith("**Generated "))
        if strip(current) != strip(text):
            print("LITERATURE.md is out of date — run bibliography.py",
                  file=sys.stderr)
            return 1
        print("LITERATURE.md is up to date.")
        return 0

    OUT.write_text(text)
    total = len(records)
    read = sum(1 for r in records
               if (r.get("verification") or {}).get("full_text_read"))
    print(f"Wrote {OUT.relative_to(ROOT.parent)} — {total} items, {read} read in full")
    return 0


if __name__ == "__main__":
    sys.exit(main())
