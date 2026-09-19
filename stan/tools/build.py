#!/usr/bin/env python3
"""Compile the STAN repository into the hub page.

The repository is the source of truth. This script reads the content pages,
routes, sessions, services and evidence records, and injects them into
prototype/template.html to produce prototype/index.html.

Nothing in the hub is hand-written any more: to change what the site says, edit
the data and rebuild.

    python3 stan/tools/build.py
    python3 stan/tools/build.py --check    # fail if index.html is out of date
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "content" / "pages"
MARKERS_DIR = ROOT / "knowledge" / "markers"
QUESTIONS_DIR = ROOT / "knowledge" / "questions"
ANSWERS_DIR = ROOT / "knowledge" / "answers"
ROUTES_PATH = ROOT / "data" / "routes.yaml"
SESSIONS_PATH = ROOT / "data" / "sessions.yaml"
LADDER_PATH = ROOT / "data" / "services.yaml"
SITE_PATH = ROOT / "data" / "site.yaml"
SERVICES_PATH = ROOT / "services" / "crisis-services.yaml"

# Service ladder statuses, and how the front end treats each.
LADDER_STATUSES = {"ready", "soon", "planned"}
SOURCES_DIR = ROOT / "evidence" / "sources"
TEMPLATE_PATH = ROOT / "prototype" / "template.html"
OUTPUT_PATH = ROOT / "prototype" / "index.html"
DIST_DIR = ROOT / "dist"

# Which service kinds appear in the hub's crisis footer.
HUB_CRISIS_KINDS = {"emergency", "crisis-emotional"}

# An hours string that does not say one of these is a part-hours service, and
# gets flagged amber. Derived rather than hand-set, so a new part-hours service
# is caught automatically.
ALWAYS_OPEN = ("24 hours", "always")


def read_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter delimited by --- lines at the top of a file."""
    text = path.read_text()
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: no frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError(f"{path.name}: unterminated frontmatter")
    data = yaml.safe_load(text[3:end])
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: frontmatter is not a mapping")
    return data


def load_pages() -> dict:
    pages = {}
    for path in sorted(PAGES_DIR.glob("*.md")):
        fm = read_frontmatter(path)
        pid = fm.get("id") or path.stem
        if pid != path.stem:
            raise ValueError(f"{path.name}: id '{pid}' does not match filename")
        if pid in pages:
            raise ValueError(f"duplicate page id '{pid}'")
        pages[pid] = fm
    return pages


def build_index(pages: dict, markers: dict) -> list:
    """The searchable index: prose pages plus Q&A generated from the markers.

    Ordered so written content sorts above gaps, and the gaps still appear —
    the hub tells you what it hasn't got rather than returning nothing.
    """
    rank = {"live": 0, "draft": 1, "planned": 2, "retired": 9}
    rows = []
    for pid, fm in pages.items():
        status = fm.get("status", "planned")
        if status == "retired":
            continue
        rows.append({
            "id": pid,
            "t": fm.get("title", pid),
            "s": status,
            "u": fm.get("units") or "",
            "d": " ".join(str(fm.get("blurb", "")).split()),
            "k": " ".join(str(fm.get("keywords", "")).split()).lower(),
        })
    rows.extend(marker_qa(markers))
    rows.extend(question_entries(load_questions(), {}))
    rows.sort(key=lambda r: (rank.get(r["s"], 5), r["t"]))
    return rows


def load_markers() -> dict:
    markers = {}
    for path in sorted(MARKERS_DIR.glob("*.yaml")):
        rec = yaml.safe_load(path.read_text())
        if not isinstance(rec, dict):
            continue
        mid = rec.get("id") or path.stem
        if mid != path.stem:
            raise ValueError(f"{path.name}: id '{mid}' does not match filename")
        markers[mid] = rec
    return markers


def dig(obj, path):
    for part in path.split("."):
        if not isinstance(obj, dict):
            return None
        obj = obj.get(part)
    return obj


def marker_qa(markers: dict) -> list:
    """Generate reader-facing Q&A entries from the marker records.

    This is the point of the knowledge base: filling in a field produces an
    answer, rather than someone remembering to write that particular sentence.
    A record with all four states filled yields four searchable answers, and
    they read consistently because they came from the same shape.
    """
    # (question template, field path, extra keywords)
    SHAPES = [
        ("What is {name}?",              "what_it_is",                      "what is explain define"),
        ("My {name} is high — what does that mean?",
                                          "states.high.meaning",             "high raised elevated too much over"),
        ("My {name} is low — what does that mean?",
                                          "states.low.meaning",              "low under below deficient too little"),
        ("What happens to {name} on steroids?",
                                          "states.suppressed.what_happens",  "suppressed suppression steroids aas cycle on"),
        ("Does {name} recover after stopping?",
                                          "states.recovery.what_is_known",   "recover recovery after stopping off pct"),
    ]
    status_of = {"reviewed": "live", "complete": "draft", "partial": "draft"}

    rows = []
    for mid, rec in markers.items():
        name = rec.get("name", mid)
        fill = rec.get("fill_status", "stub")
        base_kw = " ".join([
            mid.replace("-", " "), name,
            str(rec.get("full_name", "")),
            " ".join(rec.get("aka") or []),
        ]).lower()
        units = f"Typical UK units: {rec['units']}" if rec.get("units") else ""

        if fill == "stub":
            rows.append({
                "id": f"marker:{mid}",
                "m": mid,
                "t": f"{name} — {rec.get('full_name', '')}",
                "s": "planned",
                "u": units,
                "d": ("Planned. This marker is in the encyclopedia but nobody has "
                      "written it up yet."),
                "k": base_kw,
            })
            continue

        for template, path, kw in SHAPES:
            text = dig(rec, path)
            if not (isinstance(text, str) and text.strip()):
                continue
            rows.append({
                "id": f"marker:{mid}:{path}",
                "m": mid,
                "t": template.format(name=name),
                "s": status_of.get(fill, "draft"),
                "u": units,
                "d": " ".join(text.split()),
                "k": f"{base_kw} {kw}",
            })
    return rows


def load_questions() -> list:
    rows = []
    for path in sorted(QUESTIONS_DIR.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text())
        if not isinstance(doc, dict):
            continue
        for q in doc.get("questions") or []:
            q["_topic"] = doc.get("topic", path.stem)
            rows.append(q)
    return rows


def question_entries(questions: list, answers: dict) -> list:
    """Put the question bank in the search index.

    Unanswered questions are included deliberately. Someone searching "why am I
    so tired since I stopped" should find that STAN knows the question and is
    working on it, rather than finding nothing at all. The variants are what
    make that match — 186 real phrasings beat any amount of clever ranking.
    """
    rows = []
    for q in questions:
        aid = q.get("answer")
        answered = aid in answers if aid else False
        rows.append({
            "id": f"q:{q['id']}",
            "m": (q.get("markers") or [None])[0],
            "t": q["question"],
            "s": "draft" if answered else "planned",
            "u": "",
            "d": (answers[aid].get("summary", "") if answered else
                  "Catalogued, not answered yet. We know people ask this and it "
                  "is on the list — we will not guess at it in the meantime."),
            "k": " ".join([q["id"].replace("-", " "), q["_topic"].replace("-", " ")]
                          + (q.get("variants") or [])).lower(),
        })
    return rows


def build_views(pages, markers, questions, sessions, ladder) -> dict:
    """Every destination behind a card, as a routable inner page.

    The artifact is one file, so "inner pages" are client-side views addressed
    by hash — #/m/shbg, #/q/how-do-i-come-off-safely. Generated from the same
    data as everything else, so a card and the page it opens can never drift.

    The important case is `unwritten`. 84 of 86 destinations have no content
    yet, so the empty state is not an edge case — it is most of the site. Each
    one gets a real page that admits the gap, says what it will cover, routes
    onward to something that does exist, and captures that somebody needed it.
    """
    views = {}
    status_of = {"reviewed": "live", "complete": "draft",
                 "partial": "draft", "stub": "unwritten"}

    for mid, rec in markers.items():
        st = status_of.get(rec.get("fill_status", "stub"), "unwritten")
        views["m/" + mid] = {
            "kind": "marker",
            "s": st,
            "title": rec.get("name", mid),
            "sub": rec.get("full_name", ""),
            "units": rec.get("units", ""),
            "applies": rec.get("applies_to") or [],
            "what": rec.get("what_it_is") or "",
            "made": rec.get("made_where") or "",
            "controls": rec.get("controlled_by") or "",
            "does": rec.get("functions") or [],
            "female": rec.get("female_note") or "",
            "high": dig(rec, "states.high.meaning") or "",
            "low": dig(rec, "states.low.meaning") or "",
            "supp": dig(rec, "states.suppressed.what_happens") or "",
            "recov": dig(rec, "states.recovery.what_is_known") or "",
            "notme": rec.get("does_not_tell_you") or [],
            "related": [
                {"id": "m/" + o, "name": markers[o].get("name", o)}
                for o in (rec.get("related") or []) if o in markers
            ],
            "sources": rec.get("sources") or [],
            "willcover": [
                "What it is and where your body makes it",
                "What it does, and what controls it",
                "What a high or low result points to",
                "What happens to it on steroids, and afterwards",
                "What the number does NOT tell you",
            ],
        }

    for q in questions:
        views["q/" + q["id"]] = {
            "kind": "question",
            "s": "draft" if q.get("answer") else "unwritten",
            "title": q["question"],
            "sub": q["_topic"].replace("-", " "),
            "asked": q.get("variants") or [],
            "priority": q.get("priority", 3),
            "note": " ".join(str(q.get("notes", "")).split()),
            "related": [
                {"id": "m/" + m, "name": markers[m].get("name", m)}
                for m in (q.get("markers") or []) if m in markers
            ],
            "willcover": [],
        }

    service_for_group = {s["group"]: s["id"] for s in ladder["services"] if s["group"]}
    for g in sessions["groups"]:
        views["g/" + g["id"]] = {
            "kind": "group", "s": "draft",
            "title": g["name"],
            "sub": g["when"] + " · " + g["time"] + " · " + g["duration"],
            "who": g["who"], "shape": g["shape"], "by": g["by"],
            "size": g["size"], "cameras": g["cameras"], "joining": g["joining"],
            "service": service_for_group.get(g["id"], ""),
        }

    for s in sessions["seminars"]:
        views["s/" + s["id"]] = {
            "kind": "seminar", "s": "draft",
            "title": s["title"],
            "sub": s["when"] + " · " + s["time"] + " · " + s["duration"],
            "name": s["name"], "role": s["role"], "org": s["org"],
            "tbc": s["tbc"], "summary": s["summary"], "audience": s["audience"],
        }

    stage_label = {s["id"]: s["label"] for s in ladder["stages"]}
    for sv in ladder["services"]:
        views["o/" + sv["id"]] = dict(sv, **{
            "kind": "service",
            "s": {"ready": "live", "soon": "draft"}.get(sv["status"], "unwritten"),
            "title": sv["name"],
            "sub": sv["line"],
            "stage_label": stage_label[sv["stage"]],
        })

    # The one place the whole ladder is shown: a transparency page, not a shop.
    # Every service, its status, its blocker, and the fee rule — reached from
    # the footer and from the service pages, never from the front door.
    if "what-costs" in pages:
        raise ValueError("content page id 'what-costs' is reserved for the generated ladder page")
    views["p/what-costs"] = {
        "kind": "ladder",
        "s": "draft",
        "title": "What costs money here, and why",
        "sub": "Everything you can read is free. What costs is a person's time. "
               "This is the whole list, including the parts that do not exist yet.",
        "stages": [
            dict(st, services=[s for s in ladder["services"] if s["stage"] == st["id"]])
            for st in ladder["stages"]
        ],
        "willcover": [],
    }

    doc = yaml.safe_load(ROUTES_PATH.read_text())
    for r in doc.get("routes", []):
        for it in r.get("items", []):
            if it.get("page") or it.get("marker"):
                continue
            views["x/" + slug(it["title"])] = {
                "kind": "planned",
                "s": "unwritten",
                "title": it["title"],
                "sub": " ".join(str(it.get("note", "")).split()),
                "willcover": [],
            }

    for pid, fm in pages.items():
        views["p/" + pid] = {
            "kind": "content",
            "s": fm.get("status", "planned").replace("planned", "unwritten"),
            "title": fm.get("title", pid),
            "sub": "",
            "blurb": " ".join(str(fm.get("blurb", "")).split()),
            "tier": fm.get("publishing_tier", ""),
            "willcover": [],
        }

    # Value-first, enforced: a paid service is offered only on the pages its
    # offer_on names, and only if that page actually delivers something. An
    # empty page followed by a price is the fastest way to lose someone.
    for sv in ladder["services"]:
        for key in sv["offer_on"]:
            if key not in views:
                raise ValueError(f"service '{sv['id']}': offer_on names unknown page '{key}'")
            if views[key]["s"] == "unwritten":
                raise ValueError(
                    f"service '{sv['id']}': may not be offered on '{key}' — "
                    f"that page has no content yet"
                )
            views[key].setdefault("offers", []).append(sv["id"])

    return views


def build_relations(markers: dict) -> dict:
    """The marker graph, resolved for the UI.

    A panel is not a list of independent facts. These edges are what let the hub
    answer "what else should I be looking at" without anyone writing that
    sentence for each marker.
    """
    status_of = {"reviewed": "live", "complete": "draft",
                 "partial": "draft", "stub": "planned"}
    out = {}
    for mid, rec in markers.items():
        edges = []
        for other in rec.get("related") or []:
            if other not in markers:
                continue
            edges.append({
                "id": other,
                "name": markers[other].get("name", other),
                "s": status_of.get(markers[other].get("fill_status", "stub"), "planned"),
            })
        out[mid] = {"name": rec.get("name", mid), "related": edges}
    return out


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def resolve_next(owner: str, nxt: dict, sessions: dict, ladder: dict,
                 pages: dict) -> dict:
    """One hand-off. Exactly one of page / group / seminar / service, existing.

    This is the funnel mechanism: every door ends in a single next step. The
    build refuses a dangling one, because a dead end at the moment somebody
    has decided to act is the most expensive defect the site can have.

    Value-first: a door may only hand to something free. A paid service is
    offered from the places its `offer_on` names, after the person has been
    given something — never from the front door.
    """
    keys = [k for k in ("page", "service", "group", "seminar") if nxt.get(k)]
    if len(keys) != 1:
        raise ValueError(f"{owner}: next must name exactly one of page/group/seminar/service")
    kind = keys[0]
    target = nxt[kind]
    line = " ".join(str(nxt.get("line", "")).split())
    if kind == "page":
        if target not in pages:
            raise ValueError(f"{owner}: next points at unknown page '{target}'")
        fm = pages[target]
        return {"kind": kind, "view": "p/" + target, "title": fm.get("title", target),
                "line": line, "price": "Free", "status": "ready",
                "time": fm.get("format", "Read it here")}
    if kind == "service":
        match = [s for s in ladder["services"] if s["id"] == target]
        if match and match[0]["price"] != "Free":
            raise ValueError(
                f"{owner}: a door may not hand to a paid service — "
                f"offer '{target}' via its offer_on list instead"
            )
        match = [s for s in ladder["services"] if s["id"] == target]
        if not match:
            raise ValueError(f"{owner}: next points at unknown service '{target}'")
        s = match[0]
        return {"kind": kind, "view": "o/" + target, "title": s["name"],
                "line": line, "price": s["price"], "status": s["status"],
                "time": s["time"]}
    if kind == "group":
        match = [g for g in sessions["groups"] if g["id"] == target]
        if not match:
            raise ValueError(f"{owner}: next points at unknown group '{target}'")
        g = match[0]
        return {"kind": kind, "view": "g/" + target, "title": g["name"],
                "line": line, "price": "Free", "status": "soon",
                "time": g["when"] + " · " + g["time"]}
    match = [s for s in sessions["seminars"] if s["id"] == target]
    if not match:
        raise ValueError(f"{owner}: next points at unknown seminar '{target}'")
    s = match[0]
    return {"kind": kind, "view": "s/" + target, "title": s["title"],
            "line": line, "price": "Free", "status": "soon",
            "time": s["when"] + " · " + s["time"]}


def build_routes(pages: dict, markers: dict, sessions: dict, ladder: dict) -> dict:
    doc = yaml.safe_load(ROUTES_PATH.read_text())
    marker_status = {"reviewed": "live", "complete": "draft",
                     "partial": "draft", "stub": "planned"}
    out = []
    for r in doc.get("routes", []):
        items = []
        for it in r.get("items", []):
            page_id, marker_id = it.get("page"), it.get("marker")
            if page_id and marker_id:
                raise ValueError(
                    f"route '{r['id']}' item '{it['title']}' sets both page and marker"
                )
            if page_id:
                if page_id not in pages:
                    raise ValueError(
                        f"route '{r['id']}' links to unknown page '{page_id}'"
                    )
                status = pages[page_id].get("status", "planned")
            elif marker_id:
                if marker_id not in markers:
                    raise ValueError(
                        f"route '{r['id']}' links to unknown marker '{marker_id}'"
                    )
                status = marker_status.get(
                    markers[marker_id].get("fill_status", "stub"), "planned"
                )
            else:
                status = it.get("status", "planned")
            items.append({
                "title": it["title"],
                "note": " ".join(str(it.get("note", "")).split()),
                "status": status,
                # Where the card goes. A card with no destination is a dead end,
                # and dead ends are what the audit found everywhere.
                "view": ("m/" + marker_id) if marker_id
                        else ("p/" + page_id) if page_id
                        else "x/" + slug(it["title"]),
            })
        if not r.get("next"):
            raise ValueError(f"route '{r['id']}' has no next step — every door ends somewhere")
        out.append({
            "id": r["id"],
            "label": r["label"],
            "sub": r.get("sub", ""),
            "said": " ".join(str(r.get("said", "")).split()),
            "items": items,
            "next": resolve_next(f"route '{r['id']}'", r["next"], sessions,
                                 ladder, pages),
        })
    return {"default_open": doc.get("default_open"), "routes": out}


def build_sessions() -> dict:
    """Seminars and groups, validated against the filter vocabularies.

    Seminars and groups are separated deliberately: a talk with questions is a
    different thing from a room of people, with different risk and different
    governance (SUPPORT-MODEL.md §4).
    """
    doc = yaml.safe_load(SESSIONS_PATH.read_text())
    valid = {c["id"] for c in doc["countries"]} - {"all"}
    kinds = {k["id"] for k in doc["kinds"]} - {"all"}

    seminars = []
    for s in doc.get("seminars", []):
        sp = s.get("speaker") or {}
        seminars.append({
            "id": s["id"],
            "title": s["title"],
            "name": sp.get("name", ""),
            "role": sp.get("role", ""),
            "org": sp.get("org", ""),
            "when": s.get("when", ""),
            "time": s.get("time", ""),
            "duration": s.get("duration", ""),
            "recording": s.get("recording", ""),
            "audience": s.get("audience", ""),
            "summary": " ".join(str(s.get("summary", "")).split()),
            "tbc": "not yet recruited" in sp.get("name", "").lower(),
        })

    groups = []
    for g in doc.get("groups", []):
        unknown = set(g["coverage"]) - valid
        if unknown:
            raise ValueError(f"group '{g['id']}': unknown coverage {sorted(unknown)}")
        if g["kind"] not in kinds:
            raise ValueError(f"group '{g['id']}': unknown kind '{g['kind']}'")
        groups.append({
            "id": g["id"],
            "name": g["name"],
            "kind": g["kind"],
            "when": g.get("when", ""),
            "time": g.get("time", ""),
            "duration": g.get("duration", ""),
            "c": g["coverage"],
            "by": g.get("facilitated_by", ""),
            "size": g.get("size", ""),
            "cameras": g.get("cameras", ""),
            "who": " ".join(str(g.get("who_for", "")).split()),
            "shape": [" ".join(str(x).split()) for x in (g.get("what_happens") or [])],
            "joining": g.get("joining", ""),
        })

    return {
        "countries": doc["countries"],
        "kinds": doc["kinds"],
        "seminars": seminars,
        "groups": groups,
    }


def build_ladder() -> dict:
    """The service ladder: what can be bought, at which stage, for how much.

    This is the commercial spine (COMMERCIAL.md §2–3) as data. Validated
    against its own stage vocabulary so a card can never claim a stage the
    funnel does not have, and every non-ready rung must say what unblocks it —
    an unexplained "coming soon" is the thing this site refuses to do.
    """
    doc = yaml.safe_load(LADDER_PATH.read_text())
    stages = doc.get("stages") or []
    stage_ids = [s["id"] for s in stages]
    if len(set(stage_ids)) != len(stage_ids):
        raise ValueError("services.yaml: duplicate stage id")

    rows = []
    seen = set()
    for s in doc.get("services", []):
        sid = s["id"]
        if sid in seen:
            raise ValueError(f"services.yaml: duplicate service id '{sid}'")
        seen.add(sid)
        if s["stage"] not in stage_ids:
            raise ValueError(f"service '{sid}': unknown stage '{s['stage']}'")
        status = s.get("status", "planned")
        if status not in LADDER_STATUSES:
            raise ValueError(f"service '{sid}': unknown status '{status}'")
        if status != "ready" and not s.get("blocker"):
            raise ValueError(f"service '{sid}': status '{status}' needs a blocker")
        if status == "ready" and s.get("price") != "Free" and not s.get("unlock"):
            raise ValueError(f"service '{sid}': a ready paid service must say what unlocks it")

        rows.append({
            "id": sid,
            "stage": s["stage"],
            "group": s.get("group", ""),
            "name": s["name"],
            "line": " ".join(str(s.get("line", "")).split()),
            "time": s.get("time", ""),
            "price": str(s.get("price", "")),
            "fee": " ".join(str(s.get("fee", "")).split()),
            "status": status,
            "offer_on": list(s.get("offer_on") or []),
            "by": s.get("who_delivers", ""),
            "steps": [" ".join(str(x).split()) for x in (s.get("what_happens") or [])],
            "not": " ".join(str(s.get("not_this", "")).split()),
            "unlock": " ".join(str(s.get("unlock", "")).split()),
            "blocker": " ".join(str(s.get("blocker", "")).split()),
            "detail": " ".join(str(s.get("detail", "")).split()),
        })

    # A service may be tied to a group (the cohort). The group then offers the
    # waiting list, and the page for either points at the other.
    sess = yaml.safe_load(SESSIONS_PATH.read_text())
    group_ids = {g["id"] for g in sess.get("groups", [])}
    for r in rows:
        if r["group"] and r["group"] not in group_ids:
            raise ValueError(f"service '{r['id']}': unknown group '{r['group']}'")

    return {
        "stages": [{"id": s["id"], "label": s["label"],
                    "line": " ".join(str(s.get("line", "")).split())}
                   for s in stages],
        "services": rows,
    }


def build_crisis() -> list:
    doc = yaml.safe_load(SERVICES_PATH.read_text())
    lines = []
    for s in doc.get("services", []):
        if s.get("kind") not in HUB_CRISIS_KINDS:
            continue
        contact = s.get("contact") or {}
        num = contact.get("phone") or contact.get("text") or contact.get("web", "")

        # Make it dialable. On a phone, at 3am, an untappable crisis number is
        # a defect — the person has to memorise it and switch apps.
        href = ""
        if contact.get("phone"):
            href = "tel:" + re.sub(r"[^0-9+]", "", contact["phone"])
        elif contact.get("text"):
            shortcode = re.search(r"\b(\d{5,6})\b", contact["text"])
            if shortcode:
                href = "sms:" + shortcode.group(1)
        elif contact.get("web"):
            href = contact["web"]
        hours = " ".join(str(s.get("hours", "")).split())
        always = any(tok in hours.lower() for tok in ALWAYS_OPEN)
        lines.append({
            "b": s["name"],
            "num": num,
            "href": href,
            "hrs": hours,
            "warn": not always,
        })
    return lines


def build_state(pages: dict, markers: dict) -> dict:
    """The honest counters shown in the footer."""
    src_total = src_approved = 0
    for path in SOURCES_DIR.glob("*.yaml"):
        rec = yaml.safe_load(path.read_text())
        if not isinstance(rec, dict):
            continue
        src_total += 1
        if (rec.get("review") or {}).get("status") == "approved":
            src_approved += 1

    svc = yaml.safe_load(SERVICES_PATH.read_text())
    svc_rows = svc.get("services") or []
    svc_verified = sum(
        1 for s in svc_rows if (s.get("verification") or {}).get("status") == "verified"
    )

    questions = load_questions()
    q_answered = sum(1 for q in questions if q.get("answer"))

    counts = {"live": 0, "draft": 0, "planned": 0}
    for fm in pages.values():
        st = fm.get("status", "planned")
        if st in counts:
            counts[st] += 1

    mcounts = {"stub": 0, "partial": 0, "complete": 0, "reviewed": 0}
    for rec in markers.values():
        st = rec.get("fill_status", "stub")
        if st in mcounts:
            mcounts[st] += 1

    return {
        "questions_total": len(questions),
        "questions_answered": q_answered,
        "markers_total": len(markers),
        "markers_written": mcounts["partial"] + mcounts["complete"] + mcounts["reviewed"],
        "markers_reviewed": mcounts["reviewed"],
        "pages_live": counts["live"],
        "pages_draft": counts["draft"],
        "pages_planned": counts["planned"],
        "sources_total": src_total,
        "sources_approved": src_approved,
        "services_total": len(svc_rows),
        "services_verified": svc_verified,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="exit non-zero if index.html differs from a fresh build",
    )
    parser.add_argument(
        "--mode", choices=("artifact", "site"), default="artifact",
        help=(
            "artifact: one file, hash routes, for the single-URL preview. "
            "site: real paths for a static site, to be prerendered. "
            "Hash routes are not separately indexed by search engines, so the "
            "question bank is invisible to search in artifact mode."
        ),
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="output file (default: prototype/index.html, or dist/index.html for --mode site)",
    )
    args = parser.parse_args()

    try:
        pages = load_pages()
        markers = load_markers()
        sessions = build_sessions()
        ladder = build_ladder()
        site = yaml.safe_load(SITE_PATH.read_text())
        data = {
            "index": build_index(pages, markers),
            "routes": build_routes(pages, markers, sessions, ladder),
            "relations": build_relations(markers),
            "views": build_views(pages, markers, load_questions(),
                                 sessions, ladder),
            "sessions": sessions,
            "ladder": ladder,
            "crisis": build_crisis(),
            "state": build_state(pages, markers),
            "mode": args.mode,
            "origin": site.get("origin", ""),
        }
    except (ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1

    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Never let a data string terminate the script element early.
    blob = blob.replace("</", "<\\/")

    built = dt.date.today().isoformat()
    html = TEMPLATE_PATH.read_text(encoding="utf-8")

    if args.mode == "site":
        datascript = '<script src="/data.js"></script>'
    else:
        datascript = "<script>window.STAN_DATA=" + blob + ";</script>"

    for token, value in (("{{DATASCRIPT}}", datascript), ("{{BUILT}}", built)):
        if token not in html:
            print(f"build failed: template is missing {token}", file=sys.stderr)
            return 1
        html = html.replace(token, value)

    out_path = args.out or (DIST_DIR / "index.html" if args.mode == "site" else OUTPUT_PATH)

    if args.mode == "site" and not site.get("origin_confirmed"):
        print(
            f"warning: data/site.yaml origin is still the placeholder "
            f"'{site.get('origin')}'. Canonical links, Open Graph URLs and "
            "sitemap.xml will all be wrong until a real domain is set.",
            file=sys.stderr,
        )

    if args.check:
        current = OUTPUT_PATH.read_text() if OUTPUT_PATH.exists() else ""
        if current != html:
            print("index.html is out of date — run build.py", file=sys.stderr)
            return 1
        print("index.html is up to date.")
        return 0

    # The artifact host wraps the file in its own document. A static site has
    # no such host, so site mode emits a complete document — without it the
    # browser guesses the encoding and every dash and middot arrives mangled.
    if args.mode == "site":
        html = (
            '<!doctype html>\n<html lang="en-GB">\n<head>\n'
            + html.replace("{{LANGHEAD}}", "")
            + "\n</body>\n</html>\n"
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    if args.mode == "site":
        (out_path.parent / "data.js").write_text(
            "window.STAN_DATA=" + blob + ";", encoding="utf-8")

    st = data["state"]
    print(f"Built {out_path.relative_to(ROOT.parent)}  [mode: {args.mode}]")
    print(f"  pages     {st['pages_live']} live · {st['pages_draft']} draft · "
          f"{st['pages_planned']} planned")
    print(f"  sources   {st['sources_approved']} approved of {st['sources_total']}")
    print(f"  services  {st['services_verified']} verified of {st['services_total']}")
    print(f"  questions {st['questions_answered']} answered of "
          f"{st['questions_total']} catalogued")
    print(f"  markers   {st['markers_written']} written of {st['markers_total']}"
          f" ({st['markers_reviewed']} reviewed)")
    print(f"  qa        {sum(1 for r in data['index'] if r['id'].startswith('marker:'))}"
          f" generated entries")
    print(f"  routes    {len(data['routes']['routes'])}")
    unwritten = sum(1 for v in data["views"].values() if v["s"] == "unwritten")
    print(f"  views     {len(data['views'])} inner pages "
          f"({unwritten} unwritten, each routing onward)")
    print(f"  seminars  {len(data['sessions']['seminars'])}")
    print(f"  groups    {len(data['sessions']['groups'])}")
    ld = data["ladder"]["services"]
    print(f"  ladder    {len(ld)} services · "
          f"{sum(1 for s in ld if s['status'] == 'ready')} ready · "
          f"{sum(1 for s in ld if s['status'] == 'soon')} soon · "
          f"{sum(1 for s in ld if s['status'] == 'planned')} planned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
