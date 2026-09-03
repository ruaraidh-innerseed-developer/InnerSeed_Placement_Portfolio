#!/usr/bin/env python3
"""Validate the STAN evidence register against source.schema.yaml.

Usage:
    python3 stan/tools/validate.py            # validate and summarise
    python3 stan/tools/validate.py --quiet    # errors only

Exit status is 1 if any record fails validation, 0 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "evidence" / "schema" / "source.schema.yaml"
SOURCES_DIR = ROOT / "evidence" / "sources"
SERVICE_SCHEMA_PATH = ROOT / "services" / "schema" / "service.schema.yaml"
SERVICES_PATH = ROOT / "services" / "crisis-services.yaml"

TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "list": list,
    "bool": bool,
    "map": dict,
}

# Crisis information goes stale faster than anything else STAN holds.
MAX_SERVICE_REVIEW_DAYS = 183

REVIEW_INTERVAL_DAYS = {
    "guideline": 365,
    "position-statement": 365,
    "regulatory": 365,
    "service-record": 183,
}
DEFAULT_REVIEW_INTERVAL_DAYS = 730


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.failed: set[str] = set()

    def error(self, record: str, message: str) -> None:
        self.errors.append(f"{record}: {message}")
        self.failed.add(record)

    def warn(self, record: str, message: str) -> None:
        self.warnings.append(f"{record}: {message}")


def check_value(report, rec_id, path, value, spec, enums):
    """Check one field value against its spec fragment."""
    expected = TYPE_MAP.get(spec.get("type", "str"), str)

    # bool is a subclass of int in Python, so guard the int case explicitly.
    if expected is int and isinstance(value, bool):
        report.error(rec_id, f"{path}: expected int, got bool")
        return
    if not isinstance(value, expected):
        report.error(
            rec_id, f"{path}: expected {spec.get('type')}, got {type(value).__name__}"
        )
        return

    if spec.get("required") and isinstance(value, (str, list, dict)) and not value:
        report.error(rec_id, f"{path}: required field is empty")
        return

    enum_name = spec.get("enum")
    if enum_name:
        permitted = enums.get(enum_name, [])
        values = value if isinstance(value, list) else [value]
        for item in values:
            if item not in permitted:
                report.error(
                    rec_id,
                    f"{path}: '{item}' is not a permitted {enum_name} "
                    f"(allowed: {', '.join(map(str, permitted))})",
                )

    pattern = spec.get("pattern")
    if pattern and isinstance(value, str) and not re.match(pattern, value):
        report.error(rec_id, f"{path}: '{value}' does not match required pattern {pattern}")

    for sub_name, sub_spec in spec.get("subfields", {}).items():
        sub_path = f"{path}.{sub_name}"
        if sub_name not in value or value[sub_name] in (None, ""):
            if sub_spec.get("required"):
                report.error(rec_id, f"{sub_path}: missing required subfield")
            continue
        check_value(report, rec_id, sub_path, value[sub_name], sub_spec, enums)


def parse_date(value):
    try:
        return dt.date.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None


def check_rules(report, rec_id, record, today):
    """Cross-field rules from the 'rules' section of the schema."""
    review = record.get("review") or {}
    status = review.get("status")
    verification = record.get("verification") or {}

    if not (record.get("identifiers") or {}):
        report.error(rec_id, "identifier-present: no identifiers given")
    elif not any(
        (record["identifiers"] or {}).get(k)
        for k in ("doi", "pmid", "pmcid", "isbn", "url")
    ):
        report.error(
            rec_id, "identifier-present: need at least one of doi, pmid, pmcid, isbn, url"
        )

    if status == "approved":
        if not review.get("clinical_reviewer"):
            report.error(rec_id, "approved-requires-reviewer: no clinical_reviewer named")
        for field in ("reviewed_on", "next_review_due"):
            if not review.get(field):
                report.error(rec_id, f"approved-requires-reviewer: review.{field} missing")

        if verification.get("bibliographic") != "verified":
            report.error(
                rec_id,
                "approved-requires-verified-bibliography: bibliographic verification is "
                f"'{verification.get('bibliographic')}', must be 'verified'",
            )
        if not verification.get("full_text_read"):
            report.error(
                rec_id,
                "approved-requires-verified-bibliography: full_text_read is false",
            )
        if not record.get("claims_supported"):
            report.error(rec_id, "approved-requires-claims: claims_supported is empty")

        due = parse_date(review.get("next_review_due"))
        if due and due < today:
            report.warn(
                rec_id, f"review overdue: next_review_due was {due.isoformat()}"
            )

    if status == "retired" and not (record.get("notes") or "").strip():
        report.error(rec_id, "retired-requires-reason: notes must explain the retirement")

    # An approved record whose interval exceeds policy is a governance drift signal.
    if status == "approved":
        reviewed = parse_date(review.get("reviewed_on"))
        due = parse_date(review.get("next_review_due"))
        if reviewed and due:
            allowed = REVIEW_INTERVAL_DAYS.get(
                record.get("type"), DEFAULT_REVIEW_INTERVAL_DAYS
            )
            if (due - reviewed).days > allowed:
                report.warn(
                    rec_id,
                    f"review interval {(due - reviewed).days}d exceeds the "
                    f"{allowed}d policy for type '{record.get('type')}'",
                )


def validate_services(report) -> dict:
    """Validate the crisis services register. Returns counts for the summary."""
    counts = {"total": 0, "verified": 0}
    if not SERVICES_PATH.exists():
        report.warn("services", f"no services register at {SERVICES_PATH}")
        return counts

    schema = yaml.safe_load(SERVICE_SCHEMA_PATH.read_text())
    enums = schema["enums"]
    fields = schema["fields"]

    try:
        doc = yaml.safe_load(SERVICES_PATH.read_text())
    except yaml.YAMLError as exc:
        report.error("services", f"YAML parse error: {exc}")
        return counts

    for name, spec in schema["top_level"].items():
        if name not in doc or doc[name] in (None, ""):
            if spec.get("required"):
                report.error("services", f"{name}: missing required field")
            continue
        check_value(report, "services", name, doc[name], spec, enums)

    last = parse_date(doc.get("last_full_review"))
    nxt = parse_date(doc.get("next_full_review"))
    if last and nxt:
        interval = (nxt - last).days
        if interval > MAX_SERVICE_REVIEW_DAYS:
            report.error(
                "services",
                f"review-interval: {interval}d between reviews exceeds the "
                f"{MAX_SERVICE_REVIEW_DAYS}d maximum for crisis information",
            )
    if nxt and nxt < dt.date.today():
        report.error(
            "services",
            f"review-interval: crisis register review was due {nxt.isoformat()} "
            "and is overdue — treat every entry as unverified until rechecked",
        )

    seen: set[str] = set()
    for entry in doc.get("services") or []:
        if not isinstance(entry, dict):
            report.error("services", "a service entry is not a mapping")
            continue
        sid = entry.get("id", "<no id>")
        label = f"services/{sid}"

        if sid in seen:
            report.error(label, "unique-ids: duplicate service id")
        seen.add(sid)

        for name, spec in fields.items():
            if name not in entry or entry[name] in (None, ""):
                if spec.get("required"):
                    report.error(label, f"{name}: missing required field")
                continue
            check_value(report, label, name, entry[name], spec, enums)

        contact = entry.get("contact") or {}
        if not any(contact.get(k) for k in ("phone", "text", "email", "web")):
            report.error(label, "contact-present: need one of phone, text, email, web")

        counts["total"] += 1
        if (entry.get("verification") or {}).get("status") == "verified":
            counts["verified"] += 1

    return counts


MARKERS_DIR = ROOT / "knowledge" / "markers"

# Fields that must be filled before a record may claim fill_status "complete".
MARKER_COVERAGE = [
    "what_it_is", "made_where", "controlled_by", "functions",
    "on_a_panel.range_note", "states.high.meaning", "states.low.meaning",
    "states.suppressed.what_happens", "states.recovery.what_is_known",
    "does_not_tell_you",
]


def dig(obj, path):
    for part in path.split("."):
        if not isinstance(obj, dict):
            return None
        obj = obj.get(part)
    return obj


def is_filled(value) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value) if value is not None else False


def validate_markers(report) -> dict:
    """Validate the marker encyclopedia."""
    counts = {"total": 0, "written": 0, "reviewed": 0}
    if not MARKERS_DIR.exists():
        return counts

    records = {}
    for path in sorted(MARKERS_DIR.glob("*.yaml")):
        label = f"markers/{path.stem}"
        try:
            rec = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            report.error(label, f"YAML parse error: {exc}")
            continue
        if not isinstance(rec, dict):
            report.error(label, "record is not a mapping")
            continue

        mid = rec.get("id")
        if mid != path.stem:
            report.error(label, f"id-matches-filename: id is '{mid}'")
        records[path.stem] = rec

        for field in ("id", "name", "full_name", "category", "applies_to",
                      "units", "related", "fill_status"):
            if field not in rec or (rec[field] is None and field != "units"):
                report.error(label, f"{field}: missing required field")

        applies = rec.get("applies_to") or []
        if not applies:
            report.error(label, "applies_to: must name at least one of male, female")
        for who in applies:
            if who not in ("male", "female"):
                report.error(label, f"applies_to: '{who}' is not male or female")

        fill = rec.get("fill_status")
        if fill not in ("stub", "partial", "complete", "reviewed"):
            report.error(label, f"fill_status: '{fill}' is not a permitted value")

        if fill == "reviewed":
            if not rec.get("clinical_reviewer"):
                report.error(label, "reviewed-requires-reviewer: no clinical_reviewer")
            if not rec.get("reviewed_on"):
                report.error(label, "reviewed-requires-reviewer: no reviewed_on")

        if fill in ("complete", "reviewed"):
            missing = [f for f in MARKER_COVERAGE if not is_filled(dig(rec, f))]
            if missing:
                report.error(
                    label,
                    "complete-requires-coverage: unfilled — " + ", ".join(missing),
                )

        # A stub claiming filled content is a bookkeeping slip worth catching.
        if fill == "stub":
            filled = [f for f in MARKER_COVERAGE if is_filled(dig(rec, f))]
            if filled:
                report.warn(
                    label,
                    "fill_status is 'stub' but content exists — promote to "
                    "'partial' so coverage reports it: " + ", ".join(filled),
                )

        counts["total"] += 1
        if fill in ("partial", "complete", "reviewed"):
            counts["written"] += 1
        if fill == "reviewed":
            counts["reviewed"] += 1

    # related-must-exist: the edges are what turn records into a map.
    for mid, rec in records.items():
        for other in rec.get("related") or []:
            if other not in records:
                report.error(
                    f"markers/{mid}", f"related-must-exist: no marker '{other}'"
                )

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="print errors only")
    args = parser.parse_args()

    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    enums = schema["enums"]
    fields = schema["fields"]
    today = dt.date.today()

    report = Report()
    records: dict[str, dict] = {}

    paths = sorted(SOURCES_DIR.glob("*.yaml"))
    if not paths:
        print(f"No source records found in {SOURCES_DIR}", file=sys.stderr)
        return 1

    for path in paths:
        stem = path.stem
        try:
            record = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            report.error(stem, f"YAML parse error: {exc}")
            continue
        if not isinstance(record, dict):
            report.error(stem, "record is not a mapping")
            continue

        rec_id = record.get("id", stem)
        if rec_id != stem:
            report.error(stem, f"id-matches-filename: id is '{rec_id}'")
        if rec_id in records:
            report.error(stem, f"duplicate id '{rec_id}'")
        records[rec_id] = record

        for name, spec in fields.items():
            if name not in record or record[name] in (None, ""):
                if spec.get("required"):
                    report.error(rec_id, f"{name}: missing required field")
                continue
            check_value(report, rec_id, name, record[name], spec, enums)

        unknown = set(record) - set(fields)
        for name in sorted(unknown):
            report.warn(rec_id, f"{name}: field not in schema, will be ignored downstream")

        check_rules(report, rec_id, record, today)

    service_counts = validate_services(report)
    marker_counts = validate_markers(report)

    # A record that failed validation is never citable, whatever its status says.
    citable = [
        rec_id
        for rec_id, record in records.items()
        if (record.get("review") or {}).get("status") == "approved"
        and rec_id not in report.failed
    ]

    if not args.quiet:
        counts: dict[str, int] = {}
        for record in records.values():
            status = (record.get("review") or {}).get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1

        print(f"STAN evidence register — {len(records)} record(s) in {SOURCES_DIR}")
        for status in sorted(counts):
            print(f"  {status:<12} {counts[status]}")
        print(f"\nCitable in published content (approved): {len(citable)}")
        if not citable:
            print(
                "  None yet. No record may be cited until it has been read in full\n"
                "  and approved by a named clinical reviewer (EVIDENCE-POLICY.md §4, §8)."
            )

        mt, mw, mr = (marker_counts["total"], marker_counts["written"],
                      marker_counts["reviewed"])
        if mt:
            print(f"\nMarker encyclopedia: {mw} written of {mt}, {mr} clinically reviewed")

        total, verified = service_counts["total"], service_counts["verified"]
        print(f"\nCrisis services: {total} listed, {verified} verified")
        if total and verified < total:
            print(
                f"  {total - verified} entr(y/ies) NOT confirmed against the provider's\n"
                "  own website. No support channel may open until all are verified\n"
                "  (SUPPORT-MODEL.md §10, CRISIS-PROTOCOL.md §1)."
            )

    if report.warnings and not args.quiet:
        print(f"\n{len(report.warnings)} warning(s):")
        for line in report.warnings:
            print(f"  ! {line}")

    if report.errors:
        print(f"\n{len(report.errors)} error(s):", file=sys.stderr)
        for line in report.errors:
            print(f"  x {line}", file=sys.stderr)
        return 1

    if not args.quiet:
        print("\nAll records valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
