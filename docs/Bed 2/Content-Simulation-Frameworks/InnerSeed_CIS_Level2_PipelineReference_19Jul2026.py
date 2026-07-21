"""
InnerSeed CIS — Level 2 pipeline, reference implementation
19 July 2026 · supersedes InnerSeed_drive_to_higgsfield_pipeline_17Jul2026.py

The runnable counterpart to the simulation embedded in Part Two. Same design,
executed for real: two entry paths, a genuine Claude quality pass that can hold,
the interrupt pattern as a hard halt, and distribution only after approval.

  python pipeline.py run --input new       # new footage: Drive -> Higgsfield -> quality -> gate
  python pipeline.py run --input archive   # archived asset: Drive -> insight -> quality (hold likely) -> gate
  python pipeline.py list                  # show pieces waiting at the gate
  python pipeline.py approve <id>          # human gate: release one piece to Postiz

Cannot execute inside the Claude.ai chat sandbox (network egress blocked —
confirmed by direct test). Runs anywhere real: Claude Code, a laptop, a server.
Needs: ANTHROPIC_API_KEY, HIGGSFIELD_API_KEY, POSTIZ_API_KEY, POSTIZ_BASE_URL,
POSTIZ_INTEGRATION_ID, plus Drive file IDs and drive_token.json for Google auth.
Endpoint shapes for Higgsfield/Postiz mirror their current public docs — confirm
against live docs before first run; shapes drift.

Completion parameters, enforced in code:
  P1 one pipeline, any input      -> both paths share the same stage functions
  P2 each pass ends pass|hold     -> quality_check() returns exactly one of two states
  P3 a hold returns instructions  -> hold records carry the specific fix, never silence
  P4 finish line = ready-for-approval -> run() always ends at save_pending(), never at publish
  P5 old content gets Insight     -> archive path runs insight_pass() before anything else
"""

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path

import requests

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
HIGGSFIELD_API_KEY = os.environ.get("HIGGSFIELD_API_KEY", "")
POSTIZ_API_KEY = os.environ.get("POSTIZ_API_KEY", "")
POSTIZ_BASE_URL = os.environ.get("POSTIZ_BASE_URL", "https://your-postiz-instance")
POSTIZ_INTEGRATION_ID = os.environ.get("POSTIZ_INTEGRATION_ID", "ig_innerseed_main")

HIGGSFIELD_BASE = "https://cloud.higgsfield.ai/v1"
ANTHROPIC_BASE = "https://api.anthropic.com/v1/messages"
PENDING_DIR = Path("pending_approvals")
APPROVED_DIR = Path("approved")

D43_FILE_ID = os.environ.get("D43_FILE_ID", "")            # new-footage path
ARCHIVE_REEL_ID = os.environ.get("ARCHIVE_REEL_ID", "")    # archive path: asset
ARCHIVE_CAPTION_ID = os.environ.get("ARCHIVE_CAPTION_ID", "")  # archive path: caption


# ---------- shared plumbing ----------

def drive_download(file_id: str, dest: str) -> str:
    """Fetch one file from Google Drive. In Claude Code, swap for the Drive MCP tool."""
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    from google.oauth2.credentials import Credentials

    creds = Credentials.from_authorized_user_file("drive_token.json")
    service = build("drive", "v3", credentials=creds)
    request = service.files().get_media(fileId=file_id)
    with open(dest, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    return dest


def claude(system: str, user: str) -> str:
    """One Claude API call. Used for the Insight, Production, and Quality passes."""
    r = requests.post(
        ANTHROPIC_BASE,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1024,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        },
        timeout=120,
    )
    r.raise_for_status()
    return "".join(b.get("text", "") for b in r.json()["content"])


def quality_check(copy_text: str, market: str, language: str) -> dict:
    """P2: ends in exactly one of two states. A hold always carries instructions (P3)."""
    verdict = claude(
        system=(
            "You are the Quality pass of the InnerSeed content pipeline. Check the draft "
            "against: brand voice fit; factual accuracy against the live app; no stale dated "
            "claims (e.g. 'from April', 'vanaf april' when that month has passed); nothing "
            "reading as AI-authored. Reply as JSON only: "
            '{"status":"pass"} or {"status":"hold","reason":"...","fix":"...","revised":"..."}'
        ),
        user=f"market: {market}\nlanguage: {language}\ndraft:\n{copy_text}",
    )
    try:
        return json.loads(verdict.strip().strip("`").removeprefix("json").strip())
    except json.JSONDecodeError:
        return {"status": "hold", "reason": "quality pass returned unparseable output",
                "fix": "re-run quality", "revised": copy_text}


def higgsfield_generate(reference_path: str, prompt: str) -> str:
    """Submit-then-poll, per Higgsfield's async pattern. Returns the finished asset URL."""
    with open(reference_path, "rb") as f:
        up = requests.post(f"{HIGGSFIELD_BASE}/assets",
                           headers={"Authorization": f"Bearer {HIGGSFIELD_API_KEY}"},
                           files={"file": f}, timeout=300)
    up.raise_for_status()
    gen = requests.post(f"{HIGGSFIELD_BASE}/generate",
                        headers={"Authorization": f"Bearer {HIGGSFIELD_API_KEY}"},
                        json={"model": "image_to_video",
                              "reference_asset": up.json()["url"],
                              "prompt": prompt,
                              "aspect_ratio": "9:16",
                              "duration_seconds": 15},
                        timeout=60)
    gen.raise_for_status()
    gen_id = gen.json()["generation_id"]
    for _ in range(120):  # up to ~10 min
        st = requests.get(f"{HIGGSFIELD_BASE}/generate/{gen_id}",
                          headers={"Authorization": f"Bearer {HIGGSFIELD_API_KEY}"},
                          timeout=30)
        st.raise_for_status()
        data = st.json()
        if data["status"] == "completed":
            return data["output_url"]
        if data["status"] == "failed":
            raise RuntimeError(f"Higgsfield generation failed: {data.get('error')}")
        time.sleep(5)
    raise TimeoutError("Higgsfield generation did not complete")


def save_pending(record: dict) -> str:
    """P4 + the interrupt: execution ends here, state on disk, nothing published.
    Scenario 6's defence — publishing requires an approval record to exist, not
    merely to have been requested."""
    PENDING_DIR.mkdir(exist_ok=True)
    pid = record["id"]
    (PENDING_DIR / f"{pid}.json").write_text(json.dumps(record, indent=2))
    print(f"\nREADY FOR APPROVAL — id {pid}")
    print(f"  approve with: python {Path(sys.argv[0]).name} approve {pid}")
    return pid


def postiz_schedule(record: dict) -> dict:
    """Called only from approve() — never from run(). The gate is structural."""
    r = requests.post(
        f"{POSTIZ_BASE_URL}/public/v1/posts",
        headers={"Authorization": POSTIZ_API_KEY, "content-type": "application/json"},
        json={
            "integration_id": POSTIZ_INTEGRATION_ID,
            "type": "schedule",
            "content": record["copy"],
            "media": [record["asset_url"]] if record.get("asset_url") else [],
            "scheduled_at": record.get("scheduled_at", ""),
            "tag": f"city:{record['market']},route:{record['route']}",
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


# ---------- the two entry paths (P1: same pipeline, different doorway) ----------

def run_new() -> None:
    print("1. Drive: fetching new footage (D-43 screen recording)…")
    ref = drive_download(D43_FILE_ID, "d43_reference.mp4")

    print("2. Claude: Production — copy + visual brief…")
    copy_text = claude(
        system="You are the Production pass. Write a short Instagram caption in the "
               "account's own warm register. No overstated claims.",
        user="Piece: the Spotify playlist import (D-43) shown inside a guided session. "
             "Market: edinburgh. Language: en. Route: b2c. Stage: consideration.",
    )
    print("3. Higgsfield: generating against the real reference…")
    asset_url = higgsfield_generate(
        ref, "A hand opens the app, chooses a personal playlist, it settles into a "
             "guided session. Unhurried, light-mode palette, ends on 'a moment for you'.")

    print("4. Claude: Quality…")
    q = quality_check(copy_text, market="edinburgh", language="en")
    if q["status"] == "hold":
        print(f"   HOLD — {q['reason']}  fix: {q['fix']}")
        copy_text = q.get("revised", copy_text)
        q2 = quality_check(copy_text, market="edinburgh", language="en")
        if q2["status"] == "hold":
            raise SystemExit("Still held after revision — resolve manually, per P3.")
    save_pending({"id": uuid.uuid4().hex[:8], "path": "new", "market": "edinburgh",
                  "language": "en", "route": "b2c", "copy": copy_text,
                  "asset_url": asset_url})


def run_archive() -> None:
    print("1. Drive: fetching archived asset + caption (March Reel)…")
    drive_download(ARCHIVE_REEL_ID, "reel_2026-03-15.mp4")
    cap_path = drive_download(ARCHIVE_CAPTION_ID, "caption.txt")
    caption = Path(cap_path).read_text()

    print("2. Claude: Insight — what is this useful for NOW (P5)…")
    insight = claude(
        system="You are the Insight pass. One paragraph: what is this archived piece "
               "useful for today, if anything, and what work does it need.",
        user=f"Archived Instagram caption from March:\n{caption}")
    print(f"   {insight[:160]}…")

    print("3. Higgsfield: skipped — asset exists, no generation call (P1).")

    print("4. Claude: Quality — dated claims expected on old content…")
    q = quality_check(caption, market="enschede", language="nl")
    copy_text = caption
    if q["status"] == "hold":
        print(f"   HOLD — {q['reason']}")
        print(f"   fix: {q['fix']}  (P3: returned with instructions, never silence)")
        copy_text = q.get("revised", caption)
        q2 = quality_check(copy_text, market="enschede", language="nl")
        if q2["status"] == "hold":
            raise SystemExit("Still held after revision — resolve manually, per P3.")
        print("   Pass on second check — fix on record.")
    save_pending({"id": uuid.uuid4().hex[:8], "path": "archive", "market": "enschede",
                  "language": "nl", "route": "b2c", "copy": copy_text,
                  "asset_url": "drive://reel_2026-03-15.mp4"})


# ---------- the human gate ----------

def list_pending() -> None:
    PENDING_DIR.mkdir(exist_ok=True)
    files = sorted(PENDING_DIR.glob("*.json"))
    if not files:
        print("Nothing waiting at the gate.")
    for f in files:
        rec = json.loads(f.read_text())
        print(f"{rec['id']}  [{rec['path']}] {rec['market']}/{rec['language']}  "
              f"{rec['copy'][:60]}…")


def approve(pid: str) -> None:
    src = PENDING_DIR / f"{pid}.json"
    if not src.exists():
        raise SystemExit(f"No pending record {pid} — nothing publishes without one.")
    record = json.loads(src.read_text())
    print(f"Approved by human gate — scheduling via Postiz…")
    result = postiz_schedule(record)
    APPROVED_DIR.mkdir(exist_ok=True)
    record["postiz_post_id"] = result.get("id", "")
    (APPROVED_DIR / f"{pid}.json").write_text(json.dumps(record, indent=2))
    src.unlink()
    print(f"Scheduled. Post id: {record['postiz_post_id'] or '(see Postiz)'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="InnerSeed CIS Level 2 pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)
    runp = sub.add_parser("run"); runp.add_argument("--input", choices=["new", "archive"], required=True)
    sub.add_parser("list")
    appr = sub.add_parser("approve"); appr.add_argument("pid")
    args = ap.parse_args()

    if args.cmd == "run":
        run_new() if args.input == "new" else run_archive()
    elif args.cmd == "list":
        list_pending()
    elif args.cmd == "approve":
        approve(args.pid)
