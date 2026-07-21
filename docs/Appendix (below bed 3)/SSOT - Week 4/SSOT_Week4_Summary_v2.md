# InnerSeed Garden — Week 4 Summary
**SSOT | UX Development Manifesto**
*22–24 June 2026 | Author: Ruaraidh | App: innerseed.garden | Status: In progress*

---

## Week 4 Context

Week 4 turns the full audit lens onto Builder mode — the app's most commercially significant feature and the one most likely to differentiate InnerSeed Garden in the market. The same structured four-part evaluation is applied to each finding (what was found, why it matters, suggested fix, priority), keeping the Manifesto actionable for development without requiring academic translation.

**Guiding principle:** Builder mode is where the money is. Getting this right matters more than anything else in the audit.

**Builder Mode Evaluation Framework — tagged officially** as the evaluative approach for this week's work.

---

## Session Log — 22–24 June 2026

### Builder mode — first look

Arriving in Builder mode drops the user directly into three active pillars with controls already set and no orientation for a first-time user. The experience assumes prior knowledge (D-39). The three-column layout reads closer to audio production software than a wellness tool — a recurring tonal concern connecting back to D-06 from Week 2.

### Ambient Music pillar — four functions, one small card

Four distinct functions are compressed into one small card: track selection, loop control, volume and Spotify integration. The track selector reads as a placeholder rather than an invitation (D-40). Dutch content surfaces in the Guided Breaths pillar — the fourth distinct context for the language instability pattern (D-41). The Spotify integration — a genuinely differentiating feature — is hidden behind an unlabelled icon that nothing in the interface explains (D-43). The four functions together make the card feel fiddly and overcrowded (D-44).

### The Spotify finding — a buried differentiator

The playlist icon on the Ambient Music pillar opens a "Playlist" modal offering a curated "Garden Playlist" on Spotify and a field to paste a personal playlist URL. This is the most commercially interesting discovery of the whole audit — it allows a user's own Spotify playlists to become the soundtrack to a breathwork session, which no mainstream competitor currently offers in this form. It is currently invisible to any user who doesn't click an unlabelled icon by accident.

Comparable products researched: Calm uses Spotify for distribution (pushing content out), not for user playlist integration (pulling user content in). Endel integrates with streaming platforms for its own AI-generated soundscapes but doesn't allow user playlist import. InnerSeed Garden's Spotify integration is therefore genuinely distinct — and urgently needs to be surfaced as a named feature rather than a hidden utility.

### Transport bar — breaking down each icon

Each of the five transport bar icons was tapped in turn:

- **Library icon (three bars)** → opens Filter mode, with six filter options all in Dutch: Intentie, Duur, Gear, Stem, Music, Alleen gratis (D-45, D-46)
- **Wind/flow icon** → switches to Session/Preset mode — a mode toggle, unlabelled (D-47)
- **Mixer/sliders icon** → switches back to Builder mode — the same mode toggle from the other direction (D-47)
- **Stop icon** → stops the session
- **Three-dot menu** → reveals Share session and Save Session — two of the most important actions in Builder mode, both hidden (D-48)

### Guided Voices

Guided Voices expands to show a "Select voice…" dropdown and a volume slider. Clicking the dropdown produces no options — no voices currently available or displayable (D-49). Volume toggle works correctly across all three pillars — positive note.

### Proposed layout — full-width stacked Builder

The three-column compressed layout prompted a full rethink. Proposal: full-width stacked sequence — Music (1), Breaths (2), Voice (3) — each pillar occupying the full screen width with numbered steps, clear labels, and consistent four-column function panels. Each pillar header shows the current selection at a glance. Spotify sits as a named, visible fourth column in Step 1. Filter mode is brought into the browsing experience where it belongs rather than buried in the transport bar. Visual representations developed for application development purposes. Sixteen figures embedded in the Week 4 Manifesto: raw testing screenshots (Figs. 1–13) and visual concepts (Figs. 14–16).

### Proposed session share card

Share session and Save Session surfaced as visible, labelled actions on a completed session card — artwork banner, session title, all three components summarised, Spotify status, favourites status, and a play button. The session as a finished, shareable product rather than a configuration screen with an overflow menu.

---

## Findings Logged This Week

| Ref | Finding | Type | Priority | Connects to |
|-----|---------|------|----------|-------------|
| D-39 | Builder mode provides no orientation — user lands in three active pillars with no guidance | UX / Onboarding | High | D-05, D-08 |
| D-40 | "Select ambient music…" reads as a placeholder; Loop and volume active with no track chosen | UX / Interaction | Medium | — |
| D-41 | Dutch content in Guided Breaths pillar — fourth context for language instability | Technical | Critical | D-03, D-23, D-35 |
| D-42 | Transport bar: five unlabelled icons with no visual hierarchy | UX / Navigation | Critical | D-17 |
| D-43 | Spotify integration hidden behind an unlabelled icon — invisible to almost all users | UX / Discoverability | High | D-25 |
| D-44 | Four Ambient Music functions compressed into one small card | UX / Layout | High | D-06, D-39 |
| D-45 | Five unlabelled transport icons performing critical functions | UX / Navigation | Critical | D-17, D-21 |
| D-46 | Filter mode in Dutch, hidden inside the transport bar | Technical / UX | Critical | D-03, D-23, D-35, D-41 |
| D-47 | Mode switching duplicated across two disconnected, unlabelled locations | UX / Navigation | High | D-21 |
| D-48 | Share session and Save Session hidden in the three-dot overflow menu | UX / Navigation | High | — |
| D-49 | Guided Voices dropdown produces no options — no voices currently available | Technical | Medium | — |

Running total: **D-01 to D-49**, plus carry-over findings W1-01 to W1-05.

---

## Still to Cover

- Mobile testing — Builder and Preset journeys, including Filter mode (deferred since Week 2)
- Analytics framework — Jeroen mentioned implementation in Week 3 focus call; details to be confirmed
- Human testing — Jade Ciao identified as potential external tester; to be confirmed and budget cleared with Jeroen
- Guided Voices — audit cannot be completed until voices are available for selection
- Friday 13 June focus call notes — still not formally logged

---

*InnerSeed Garden · UX Development Manifesto · Week 4 Summary · Ruaraidh · 22–24 June 2026 · innerseed.garden*

---

## Phase 1 Close-Out — 27 June 2026

**Status: Phase 1 Complete. Sealed 29 June 2026.**

### Focus call — 27 June 2026 (Ruaraidh & Jeroen)

- Phase 1 audit reviewed and acknowledged complete — 49 findings (D-01 to D-49) plus W1-01 to W1-05
- Spotify integration (D-43) confirmed as the standout commercial discovery of the four weeks
- Phase 2 scope agreed — shift from audit to build
- Three workstreams confirmed for July onwards:
  - **User Testing System** — proprietary ISD-owned research capability; first deployment mobile
  - **Brand Book** — visual identity, tone of voice, digital marketing templates; anchor content is the founder interview
  - **Digital Marketing Strategy** — channel strategy, content framework, campaign templates
- Brand expansion discussed — international markets, retreats, phase two concepts (logged in Seed Vault)
- **Founder interview agreed** — Ruaraidh to travel to Enschede; filmed interview with Jeroen in his studio; cornerstone brand and launch marketing content
- Analytics implementation to be reviewed in Phase 2 and mapped against findings

### Still open — carried into Phase 2

- Mobile testing — first User Testing System deployment
- Guided Voices (D-49) — open until voices available
- D-03 (Dutch, five surfaces) — one consolidated development ticket
- Jade Ciao — first human testing participant, to be confirmed
- Analytics framework — review with Jeroen in Phase 2

### Phase 2 begins Week 5

Brand Book workstream opens. User Testing System protocol drafted. Founder interview brief written. Enschede visit planned.

---

*InnerSeed Garden · UX Development Manifesto · Week 4 Summary · Phase 1 Complete · Sealed 29 June 2026 · innerseed.garden*
