#!/usr/bin/env python3
"""Query the STAN evidence register.

Examples:
    python3 stan/tools/query.py --topic shbg-free-testosterone
    python3 stan/tools/query.py --grade A B --relevance direct
    python3 stan/tools/query.py --search "free testosterone" --format full
    python3 stan/tools/query.py --citable --format citation
    python3 stan/tools/query.py --unread          # what to read next
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "evidence" / "sources"


def load_records() -> list[dict]:
    records = []
    for path in sorted(SOURCES_DIR.glob("*.yaml")):
        record = yaml.safe_load(path.read_text())
        if isinstance(record, dict):
            records.append(record)
    return records


def searchable_text(record: dict) -> str:
    parts = [
        str(record.get("title", "")),
        " ".join(record.get("authors") or []),
        str(record.get("venue", "")),
        " ".join(record.get("claims_supported") or []),
        " ".join(record.get("claims_not_supported") or []),
        str(record.get("notes", "")),
        str((record.get("population_relevance") or {}).get("notes", "")),
    ]
    return " ".join(parts).lower()


def matches(record: dict, args) -> bool:
    review = record.get("review") or {}
    level = record.get("evidence_level") or {}
    relevance = record.get("population_relevance") or {}
    verification = record.get("verification") or {}

    if args.topic and not set(args.topic) & set(record.get("topics") or []):
        return False
    if args.grade and level.get("grade") not in args.grade:
        return False
    if args.relevance and relevance.get("rating") not in args.relevance:
        return False
    if args.status and review.get("status") not in args.status:
        return False
    if args.type and record.get("type") not in args.type:
        return False
    if args.since and (record.get("year") or 0) < args.since:
        return False
    if args.citable and review.get("status") != "approved":
        return False
    if args.unread and verification.get("full_text_read"):
        return False
    if args.search and args.search.lower() not in searchable_text(record):
        return False
    return True


def format_citation(record: dict) -> str:
    authors = record.get("authors") or []
    if len(authors) > 3:
        author_str = f"{authors[0]}, et al."
    else:
        author_str = ", ".join(authors)
    ident = record.get("identifiers") or {}
    tail = f" doi:{ident['doi']}" if ident.get("doi") else ""
    title = " ".join(str(record.get("title", "")).split())
    return f"{author_str} {title}. {record.get('venue')}. {record.get('year')}.{tail}"


def format_row(record: dict) -> str:
    level = record.get("evidence_level") or {}
    relevance = record.get("population_relevance") or {}
    review = record.get("review") or {}
    read = "read" if (record.get("verification") or {}).get("full_text_read") else "UNREAD"
    return (
        f"{record.get('id', '?'):<44} "
        f"{level.get('grade', '?'):<2} "
        f"{relevance.get('rating', '?'):<9} "
        f"{review.get('status', '?'):<10} "
        f"{read:<7} "
        f"{record.get('year', '?')}"
    )


def format_full(record: dict) -> str:
    wrap = lambda s: textwrap.fill(" ".join(str(s).split()), 78, subsequent_indent="    ")
    level = record.get("evidence_level") or {}
    relevance = record.get("population_relevance") or {}
    review = record.get("review") or {}
    ident = record.get("identifiers") or {}

    out = [
        "=" * 78,
        record.get("id", "?"),
        "=" * 78,
        wrap(record.get("title", "")),
        f"  {format_citation(record)}",
        "",
        f"  type       {record.get('type')}",
        f"  grade      {level.get('grade')} ({level.get('scheme')})",
        f"  relevance  {relevance.get('rating')}",
        f"  status     {review.get('status')}"
        + (f" — reviewer {review['clinical_reviewer']}" if review.get("clinical_reviewer") else ""),
        f"  full text  {'read' if (record.get('verification') or {}).get('full_text_read') else 'NOT READ'}",
        f"  ids        " + ", ".join(f"{k}:{v}" for k, v in ident.items() if k != "url"),
        f"  topics     " + ", ".join(record.get("topics") or []),
        "",
        "  MAY be cited for:",
    ]
    for claim in record.get("claims_supported") or ["  (none recorded)"]:
        out.append("    + " + wrap(claim).replace("\n", "\n      "))
    out.append("")
    out.append("  MUST NOT be cited for:")
    for claim in record.get("claims_not_supported") or ["  (none recorded)"]:
        out.append("    - " + wrap(claim).replace("\n", "\n      "))
    if record.get("notes"):
        out += ["", "  Notes:", "    " + wrap(record["notes"]).replace("\n", "\n    ")]
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--topic", nargs="+", help="filter by topic (any match)")
    parser.add_argument("--grade", nargs="+", help="filter by evidence grade, e.g. A B")
    parser.add_argument("--relevance", nargs="+", help="direct | partial | indirect | unclear")
    parser.add_argument("--status", nargs="+", help="added | in-review | approved | retired")
    parser.add_argument("--type", nargs="+", help="filter by source type")
    parser.add_argument("--since", type=int, help="published in this year or later")
    parser.add_argument("--search", help="free-text search across title, claims and notes")
    parser.add_argument("--citable", action="store_true", help="approved records only")
    parser.add_argument("--unread", action="store_true", help="records whose full text is unread")
    parser.add_argument(
        "--format", choices=["table", "full", "citation", "json"], default="table"
    )
    args = parser.parse_args()

    records = [r for r in load_records() if matches(r, args)]

    if not records:
        print("No matching records.")
        return 0

    if args.format == "json":
        print(json.dumps(records, indent=2, default=str))
    elif args.format == "citation":
        for record in records:
            print(format_citation(record))
    elif args.format == "full":
        for record in records:
            print(format_full(record))
    else:
        print(f"{'id':<44} {'G':<2} {'relevance':<9} {'status':<10} {'text':<7} year")
        print("-" * 84)
        for record in records:
            print(format_row(record))
        print(f"\n{len(records)} record(s).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
