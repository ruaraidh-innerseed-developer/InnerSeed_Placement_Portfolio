# InnerSeed Garden — Week 2 Summary
**SSOT | UX Development Manifesto**
*9 June – 13 June 2026 | Author: Ruaraidh | App: innerseed.garden*

---

## Naming Update — Locked This Week

The primary working document — previously called the "InnerSeed Development & Strategy Log" or "Development & UX Log" — is now permanently named:

**The UX Development Manifesto**

It is also known internally as the **SSOT** (Single Source of Truth) — the two names refer to the same role, but the formal title for all deliverables, folders and footers is *UX Development Manifesto*.

**The appendix (`innerseed_appendix.html`) remains the project's master background reference** — separate from the Manifesto. The appendix holds the framework, deadlines, people, decisions and file index. The Manifesto holds the weekly UX findings, screenshots, and design work.

---

## Week 2 Context

Focus shifted fully onto the app itself — testing and improving it from a user's perspective, with Claude acting as both systems engineer and end user. Six areas agreed for this week:

- Preset mode — as a regular user
- Filter mode — intuitive and discoverable?
- Saving sessions
- Creating sessions
- Favouriting sessions
- Anything that feels unnatural or complex

**Guiding principle agreed this week:** Keep It Simple, Stupid (KISS).

**External input incoming:** A UX professional outside the project is reviewing the app informally (unpaid for now). Their feedback is expected in Week 3 or 4 and will be cross-referenced against these findings.

---

## Session Log — 10 June 2026, 14:29

### Opening Screen — Five-Question Audit ✅ Complete

**Q1 — Clarity:** ✅ Complete — raw answer logged
**Q2 — Orientation:** ✅ Complete — raw answer logged
**Q3 — Trust & tone:** ✅ Complete — sleek/intelligent but "game-like" rather than calming; tonal mismatch for wellness product
**Q4 — Friction:** ✅ Complete — no obvious single path to "experience something"; dominant CTA pushes toward building
**Q5 — Return user consideration:** ✅ Complete — layout too complex for a simple core task

---

## Session Log — 12 June 2026 (continued)

### Step 1 — Preset Mode (in progress)

Live testing began using **Ethereal Voyager**. Key observations:

- Attempting to open a Preset led into **Builder mode** instead — reproducing the Week 1 mode-confusion finding (W1-01) live, under real conditions
- Session cards on the dashboard are only clickable via a tiny play icon, not the whole card
- No way back from the Preset player to the dashboard — side nav doesn't offer a "home" route, and the split InnerSeed logo is ambiguous as a home button
- The player's control panel doesn't visually read as a breathwork session — connects to the Week 1 breathing visualiser idea (W1-05)
- The session metadata line ("21 min · CONTACT · Connect · ♂ Jeroen") is unclear and may be a labelling bug
- Transport bar icons (folder, settings, save) appear to be reused from Builder mode and don't fit a Preset playback context

**Pattern identified:** Builder-mode UI and language is bleeding into the Preset/playback experience — compounding the "discovery first" issue.

**Still to confirm:** what the play/stop/save/folder/settings icons actually do when pressed on the Preset player.

---

## Findings Logged This Week

| Ref | Finding | Type | Priority | Recommendation |
|-----|---------|------|----------|----------------|
| D-01 | "Presets" terminology confuses new users; observed causing disengagement | UX / Language | High | Rename to "Sessions" throughout |
| D-02 | "Build your breathwork" CTA creates hierarchy confusion; new users don't know what to do first | UX / IA | High | Restructure hero — discovery first, builder secondary |
| D-03 | App detected as Dutch by browser; translation prompt fires on load for English users | Technical | Critical | Correct HTML `lang` attribute and language metadata |
| D-04 | Left-hand navigation invisible on first load — only appears on hover | UX / Navigation | High | Nav should be visible by default with permanent labels or affordance |
| D-05 | No discovery layer for first-time users — app assumes prior knowledge | UX / Onboarding | High | First load should show what the app offers before asking the user to choose |
| D-06 | Tone leans "tech/gaming" rather than "wellness/calm" | UX / Visual Design | Medium | Consider warmer, softer treatment even within dark palette |
| D-07 | Hero banner image cuts off abruptly with a hard edge | UX / Visual Design | Low–Medium | Resize/crop properly or add gradient fade |
| D-08 | No single-click path to "experience something" | UX / IA | High | Dashboard hero should lead to listening, not building |
| D-09 | Left nav labels describe process/stats, not experience | UX / Navigation | High | Add a clear "listen now" entry point |
| D-10 | Complexity doesn't match simplicity of core task | UX / Overall | High | Redesign with radical simplicity — "usable by a three year old" |
| D-11 | Mode confusion reproduced live — opening a Preset led into Builder mode | UX / IA | High | Reinforces W1-01 — prioritise mode-switcher fix |
| D-12 | Session cards only clickable via tiny play icon | UX / Interaction | Medium | Make whole card a tap target |
| D-13 | No way back from Preset player to dashboard | UX / Navigation | High | Add back button or breadcrumb; reinforces W1-04 |
| D-14 | Split InnerSeed logo is ambiguous as a home/nav button | UX / Navigation | Medium | Make logo behave and look like a clear "home" link |
| D-15 | Player control panel doesn't visually read as a breathwork session | UX / Visual Design | Medium | Reinforces W1-05 — breathing visualiser would help |
| D-16 | Session metadata line ("CONTACT · Connect") unclear, possible bug | Technical | High | Developer check — likely showing field key instead of value |
| D-17 | Transport bar icons (folder/settings/save) don't fit Preset playback context | UX / IA | High | Builder-mode UI is bleeding into Preset mode — needs separate UI |

---

## Design Principle Emerging — "Discovery First"

A consistent theme across this week's findings: the app currently rewards users who already know what they want. It needs a first layer that helps users discover what the app offers before asking them to make a choice.

**The question the first load should answer is not** *"what do you want to build?"* **but** *"here's what this can do for you."*

---

## Visual Record

Five screenshots from the opening screen audit are embedded in the full Manifesto document (`InnerSeed_DevUX_Manifesto_Week2_10June.html`):

- Fig. 1 — Full dashboard on load
- Fig. 2 — "Presets" section close-up
- Fig. 3 — Nav expanded on hover (Root / Rise / Return)
- Fig. 4 — Nav in default collapsed state
- Fig. 5 — "Builds" section

---

## Still to Cover This Week

- Confirm what the play/stop/save/folder/settings icons actually do on the Preset player
- Step 2 — Builder/Creator mode: build a session from scratch, test saving and the build experience
- Filter mode and favouriting — to be tested within the above flows
- Anything unnatural — ongoing catch-all

All to be completed before the **Friday 13 June focus call with Jeroen** — Ruaraidh's first recorded presentation of findings.

---

## Folder Structure Confirmed This Week

```
📁 INNERSEED GARDEN
    📁 SSOT - Raw & Background
        innerseed_appendix (master reference)
        innerseed_recovery_brief
        📁 SSOT - Week 1
        📁 SSOT - Week 2
    📁 UX Dev Manifesto
        📁 UX Dev Logs
            Week 1 ✅
            Week 2 ✅
    📁 University
        Markdown summaries (this document)
```

---

*InnerSeed Garden · UX Development Manifesto · Week 2 Summary · Ruaraidh · 9–13 June 2026 · innerseed.garden*
