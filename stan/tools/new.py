#!/usr/bin/env python3
"""Scaffold a new record in the STAN repository.

    python3 stan/tools/new.py page shbg-and-thyroid
    python3 stan/tools/new.py source grant-2024-something

Creates the file with the required fields already in place, then tells you to
rebuild. It never overwrites an existing file.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

PAGE = """---
id: {id}
title: {title}
short_title: {title}
content_class: information
status: planned
publishing_tier: B
second_reader:
marker_type: hormone

blurb: >-
  One or two sentences. This is what shows in the hub's search results, so write
  it for someone who does not yet know what this marker is.
units: ""
keywords: {id_words}
topics: []
routes: []

author:
clinical_reviewer:
reviewed_on:
next_review_due:
version: 0.0
cites_pending: []
---

# {title}

**Planned — not written yet.**

Draft against `templates/hormone-explainer.md`. The two sections that make it
worth writing are **"When it's suppressed"** and **"What this number does not
tell you"**.

Set `publishing_tier: A` only if the finished page stays inside the five
permitted forms in `governance/INTERIM-STANDARD.md` §3 — signpost, attributed
report, settled definition, question set, or lived experience. Anything that
interprets or advises stays at B.
"""

SOURCE = """id: {id}
type: primary-research
title: >-
  FULL TITLE
authors:
  - Surname A
year: {year}
venue: JOURNAL OR ISSUING BODY
identifiers:
  doi:
  pmid:
  url:
open_access: false

evidence_level:
  scheme: STAN-EL-1
  grade: C
  rationale: >-
    Why this grade. Grade is about what weight the source can bear, not whether
    it is any good.

population_relevance:
  rating: unclear
  notes: >-
    Does the study population match STAN's readers? A guideline on age-related
    hypogonadism is only partially relevant to a post-AAS reader.

topics: []

claims_supported:
  - >-
    What this source may be cited for.

claims_not_supported:
  - >-
    What it must never be cited for. Foreseeable misuse goes here.

limitations: >-
  Design, population, and anything unassessed. Say plainly if the full text has
  not been read.

conflicts_of_interest: not yet assessed — full text not read

verification:
  bibliographic: unverified
  full_text_read: false
  verified_by: R. (founder)
  verified_on: '{today}'

review:
  status: added

provenance:
  added_by: R. (founder)
  added_on: '{today}'
  discovered_via: >-
    How this was found.

notes: >-
  Anything a reviewer needs to know.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["page", "source"])
    ap.add_argument("id", help="kebab-case slug, e.g. shbg or grant-2024-thing")
    ap.add_argument("--title", help="human title (defaults to the slug, title-cased)")
    args = ap.parse_args()

    if not SLUG.match(args.id):
        print(f"'{args.id}' is not a valid slug: lower case, digits and hyphens only",
              file=sys.stderr)
        return 1

    today = dt.date.today().isoformat()
    words = args.id.replace("-", " ")
    title = args.title or words[:1].upper() + words[1:]

    if args.kind == "page":
        path = ROOT / "content" / "pages" / f"{args.id}.md"
        body = PAGE.format(id=args.id, title=title, id_words=words)
    else:
        path = ROOT / "evidence" / "sources" / f"{args.id}.yaml"
        year = re.search(r"(19|20)\d{2}", args.id)
        body = SOURCE.format(id=args.id, today=today,
                             year=year.group(0) if year else today[:4])

    if path.exists():
        print(f"{path.relative_to(ROOT.parent)} already exists — not touching it",
              file=sys.stderr)
        return 1

    path.write_text(body)
    print(f"Created {path.relative_to(ROOT.parent)}")
    print("Next: fill it in, then")
    print("  python3 stan/tools/validate.py")
    if args.kind == "page":
        print("  python3 stan/tools/build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
