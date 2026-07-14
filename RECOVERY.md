# Recovery Brief — The Night Garden ePortfolio

A short "what is where" note in case this repo, branch, or PR is ever lost.
Written 14 July 2026.

## Where the live work is

- **Repo:** `ruaraidh-innerseed-developer/InnerSeed_Placement_Portfolio` on GitHub.
- **Branch:** `claude/inner-seed-portfolio-blog-04mxik`
- **Pull request:** [#1](https://github.com/ruaraidh-innerseed-developer/InnerSeed_Placement_Portfolio/pull/1)
- **Base branch:** `main` (holds the original scaffold only — the full build lives on the branch above until the PR merges).

If the PR or branch is ever deleted before merging, GitHub still keeps the
commit history for a period under "Activity" on the repo, and any local
clone (`git fetch origin`) that still has the branch ref can restore it.
The safest single action, if you're worried about loss: merge PR #1 into
`main` — once merged, the work is on the repo's permanent history.

## What's in the repo

| Path | What it is | Source of truth |
|---|---|---|
| `index.html` | The whole landing page — single file, no build step, no dependencies. Open it directly or serve the folder with any static file server. | This repo. Rebuilding it means re-doing this Claude Code session's work; there is no separate draft elsewhere. |
| `docs/InnerSeed_DevUX_Manifesto_Week1_4June.html` … `Week4_22June.html`, `ManifestoWeek5_Reflections_Summary.html` | The five weekly manifestos, exported as styled HTML. | **Master copies live in Google Drive** (per the SSOT workflow described in the Week 5 manifesto itself). The copies in `docs/` are filed exports — if one goes missing from the repo, re-export from Drive rather than reconstructing from memory. |
| `assets/intro-poster.svg` | Illustrated placeholder shown in the video frame until real footage exists. | Generated for this build; safe to regenerate or replace. |
| `assets/photo-placeholder.svg` | Illustrated placeholder in the closing "Return" section until a real photo is added. | Generated for this build; safe to regenerate or replace. |
| `assets/intro.mp4` | **Not yet added.** Reserved path for the iPhone 16E intro recording. | Only exists once you upload it — back it up wherever the original recording lives (e.g. Photos/iCloud) until then. |

## What's still outstanding (not a recovery risk, just unfinished)

- Real video at `assets/intro.mp4` (currently just reserved space, per your instruction).
- Real photo to replace `assets/photo-placeholder.svg` in the Return section.
- Two placeholder links in the Return section still read "(add link)": Google Drive (SSOT folder) and LinkedIn.
- The five Content Integration Strategy parts, the Seed Vault, the Garden Lab Proposal and Field Notes are currently written *directly into* `index.html`'s reading-room content (the `DOCS` object in the `<script>` at the bottom) — they don't yet exist as separate filed documents in `docs/`. If you want them as standalone files later, the summaries in `index.html` are the first draft to split out.

## Fastest way to restore/redeploy from scratch

```bash
git clone https://github.com/ruaraidh-innerseed-developer/InnerSeed_Placement_Portfolio.git
cd InnerSeed_Placement_Portfolio
git checkout claude/inner-seed-portfolio-blog-04mxik
python3 -m http.server 8000   # or any static file server
# open http://localhost:8000/index.html
```

No build tooling, no `node_modules`, no environment variables — it's a
static site, so "recovery" is really just "don't lose the git history."
