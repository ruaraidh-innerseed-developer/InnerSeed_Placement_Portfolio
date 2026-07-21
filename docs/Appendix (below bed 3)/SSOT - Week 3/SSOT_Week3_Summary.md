# InnerSeed Garden — Week 3 Summary
**SSOT | UX Development Manifesto**
*15–18 June 2026 | Author: Ruaraidh | App: innerseed.garden | Status: Complete*

---

## Week 3 Context

Week 3 opened by closing out the two items carried over from Week 2 — the Preset session completion flow and Filter mode. In the course of that work, several pieces of new evidence emerged that confirm and sharpen two existing Week 2 findings (the Dutch language issue, D-03, and the session metadata anomaly, D-16), alongside a number of new findings and a proposed full-screen "cinematic mode" for the Preset player. Builder mode becomes the headline focus for the remainder of the week.

**Guiding principle, unchanged:** Keep It Simple, Stupid (KISS).

**External input still incoming:** the external UX professional's informal review remains expected in Week 3 or 4.

---

## Session Log — 15 June 2026

### Session completion flow — remains untested

The progress scrubber cannot be dragged. This was confirmed as a deliberate design choice, intended to discourage starting and stopping sessions and to encourage full completion. As a result, there is currently no practical way to preview the end of a session without a full play-through, and no short-duration Preset exists to make that quick to do (D-22).

### Preset default state and session selection

The empty Preset state ("Choose a preset to begin") was reviewed and accepted as reasonable for now. Selecting "Choose preset" opens the Load Session modal already logged in Week 2 (D-19, D-20) — but this time, the same three presets (Breathe Deep Loop, Monsoon Vault, Ethereal Voyager) were observed rendering their descriptions in Dutch in one instance and English in another. This confirms the Week 2 language finding (D-03) extends to actual session content, not only a page-level translation prompt (D-23).

### Metadata anomaly — confirmed and pinpointed

The "CONTACT · Connect" anomaly first logged against Ethereal Voyager (D-16) reproduced identically against a second preset, Breathe Deep Loop, confirming it is systemic. Comparing this against the Load Session modal — where the same field renders correctly — pinpoints the fault specifically to the player banner template (D-24).

### Banner image — affordance and meaning

Clicking the large banner artwork above the player reopens the Load Session modal, allowing a different preset to be chosen. This is functional but undiscoverable — nothing about the banner signals it is interactive, and its artwork is not tied to the InnerSeed Garden identity (D-25).

### Sidebar during playback — towards a "cinematic mode"

The sidebar and full transport bar remain visible throughout playback, with no transition to a calmer state once a session begins (D-26). A proposed "cinematic mode" was sketched in response: sidebar and chrome recede, replaced by a single full-screen visual — breathing rings pulsing in a slow, breath-paced rhythm, with a quiet countdown beneath, and the visual itself acting as the only control (a tap anywhere on it pauses or resumes playback). Grounded in Hick's Law, calm technology principles (Case, 2015) and cognitive load theory (Sweller, 1988). Offered as a direction for discussion, not a finished specification.

### Builder mode — first glance

A brief look at Builder mode ahead of the full audit showed the three content pillars (Ambient Music, Guided Breaths, Guided Voices) surfaced directly as toggles. No findings logged yet — the full structured audit begins once Preset mode is fully closed out.

### "Recent" — discoverability and behaviour

"Recent" continued to show "No sessions played yet" despite Ethereal Voyager having been played more than once in the same sitting (D-27). A minor labelling inconsistency was also noted — "Recent" in most views, "Recents" in the default empty state (D-28). Separately, a "Green House" sidebar item was found to appear in some Preset-mode views and not others, with no clear rule — connecting to the structural concern already raised in D-21 (D-29).

---

## Session Log — 17 June 2026

### Session completion — observed live

Ethereal Voyager was played through to completion, finally resolving D-22. The only change on screen at completion is the timer resetting to 00:00 and a single "Go To Green House" prompt appearing — no acknowledgment that the session has ended, no summary, no sense of arrival. Coming directly out of an intensive breathwork session, this was experienced as anticlimactic, with the more likely reaction being to close the app rather than engage further (D-30).

### Naming conflict — "Green House" and "Garden"

The completion prompt raised a bigger question: what the Green House actually is, and how it relates to the wider Garden identity. The two currently read as overlapping, undifferentiated concepts — it isn't clear whether Green House is part of the Garden, a separate destination, or another name for the same thing. The term itself works against the brand: "greenhouse" suggests an enclosed, artificial growing space, sitting at odds with the open, natural quality the Garden identity is built around (D-31). Connects directly to D-29.

A written summary of this point was prepared and sent to Jeroen separately, to be raised at the Thursday 18 June discussion (12pm–2pm) alongside other agenda items. The Green House destination itself has not yet been opened or tested — needed to ground the naming discussion before it is finalised.

---

## Session Log — 18 June 2026

### Immediately after completion — a locked interface

A closer look confirmed that immediately after Ethereal Voyager finished, no on-screen control responded except "Go To Green House" — escalating D-30 into a forced single-path concern (D-33). Settings and save icons were also found missing from the transport bar after completion, persisting even when returning to the player via Recent (D-34).

### Load Session modal — content found to be unstable

Reopening the session picker later in the same sitting showed only one preset (Ethereal Voyager) listed under Presets, with an entirely different description ("The Garden's First Breath"), and the third tab relabelled "Shared By me" rather than "Shared With me." This extends D-23 well beyond language alone — preset availability, descriptions and tab labelling all appear unstable across viewings (D-35).

### Green House — finally seen

Following "Go To Green House" through revealed a genuine, distinct feature: "Your Rhythm" (sessions completed, sessions today, day streak), a twelve-month "Breathwork Moments" activity record, and three sub-sections — Progress, Coaches, Events. This resolves the structural half of D-31 — Green House is not a duplicate of the Garden dashboard — though the naming concern stands, sharpened by the literal greenhouse backdrop artwork used on the screen itself (D-36).

### Further consistency findings

The sidebar item used to reach Builder mode reads "Sessions" in later views rather than "Session Builder" — a fourth instance of the same labelling-instability pattern (D-37). Recent list items were also found to render inconsistently, correct on first appearance but later concatenating duration and host name with no separator ("21 minJeroen") (D-38). D-32 is refined accordingly: Recent appears to survive a Garden–Green House round trip but not a Garden–Sessions round trip — worth retesting deliberately during the Builder mode audit.

### Correction — comms and findings integration plan

The item previously logged against "the back garden" has been corrected: the intended reference throughout was always the Greenhouse, not a separate concept. With Green House now opened and understood, this item is ready for a proper scoping conversation rather than remaining an unscoped placeholder, and is raised directly in today's focus call with Jeroen (12pm UK / 1pm NL).

---

## Findings Logged This Week

| Ref | Finding | Type | Priority | Recommendation |
|-----|---------|------|----------|----------------|
| D-22 | Session completion flow remains untested — scrubber intentionally locked, no short Preset for a quick preview | UX / Testing constraint | Medium | Agree a short test/preview Preset or developer fast-forward option |
| D-23 | Same Load Session modal, same presets, render in Dutch in one instance and English in another | Technical | Critical | Escalates D-03 — investigate content-level language handling |
| D-24 | "CONTACT · Connect" metadata anomaly reproduced on a second preset; correct in the modal list view, faulty only in the player banner | Technical | High | Confirms and pinpoints D-16 — compare banner template against the correct modal template |
| D-25 | Banner artwork is clickable (swaps preset) but gives no visual indication of this; artwork unrelated to garden identity | UX / Affordance | Medium | Add a visible "change session" affordance; consider on-brand artwork |
| D-26 | Sidebar and transport chrome remain visible throughout playback; no immersive state during a session | UX / Visual Design | High | Proposed "cinematic mode" — full-screen visual, single tap-to-pause control |
| D-27 | "Recent" still reads "No sessions played yet" after multiple plays of the same session | Technical | Medium | Confirm what triggers a "Recent" entry; retest once completion is possible |
| D-28 | Sidebar section labelled "Recent" in most views, "Recents" in the default empty Preset state | UX / Consistency | Low | Standardise to a single label |
| D-29 | "Green House" sidebar item present in some Preset-mode views, absent in others, with no clear rule | UX / Consistency | Medium | Developer to confirm whether intentional; connects to D-21 and D-31 |
| D-30 | **Major** — Session completion under-acknowledged; only change is timer reset and a "Go To Green House" prompt, no acknowledgment session has ended | UX / Completion | High | Reconsider what should mark completion before any CTA is presented |
| D-31 | **Major** — "Green House" and "Garden" read as overlapping, undifferentiated concepts; the term works against the Garden identity | Strategy / Branding & IA | Critical | Now partly resolved by D-36; naming question remains for Thursday's discussion |
| D-32 | Recent history did not persist after navigating into Session Builder and back; later refined — appears to survive a Garden–Green House round trip | Technical | Medium | Retest deliberately whether Sessions navigation specifically clears Recent |
| D-33 | **Major** — Immediately after completion, no control responded except "Go To Green House" — a single forced path | UX / Completion | Critical | Escalates D-30 — reconsider locking the interface to one action after an intensive session |
| D-34 | Settings and save icons disappear from the transport bar after completion, persisting through later navigation | Technical | High | Confirm whether intentional or unintended state loss |
| D-35 | Load Session modal content unstable — preset count, descriptions, and third tab label all changed across viewings | Technical | Critical | Escalates D-23 — investigate as one underlying data/caching issue |
| D-36 | **Major** — Green House opened: a stats and community hub ("Your Rhythm," activity heatmap, Progress/Coaches/Events), not a duplicate dashboard | Discovery / Strategy | High | Resolves the structural half of D-31; naming question sharpened by literal greenhouse artwork |
| D-37 | Sidebar nav item labelled "Session Builder" in earlier views, "Sessions" in later ones | UX / Consistency | Medium | Fourth instance of the labelling-instability pattern; connects to D-21, D-28, D-29 |
| D-38 | Recent list item rendering inconsistent — correct with icon on first appearance, concatenated ("21 minJeroen") in later views | Technical | Medium | Likely a formatting issue specific to certain render contexts |

Running total: **D-01 to D-38**, plus carry-over findings W1-01 to W1-05.

---

## Design Proposal — "Cinematic Mode"

A direction, not a finished specification: on entering playback, the sidebar, transport icons, metadata line and progress scrubber recede entirely. In their place, a single full-screen visual — breathing rings pulsing in time with the guided pace, with a quiet countdown beneath — fills the screen. The visual itself becomes the only control: tapping it pauses or resumes the session. A single, unobtrusive way to exit remains available throughout.

Open questions before this is taken further: the right exit gesture, how prominent the countdown should be, and whether this treatment should extend to Builder and Creator playback as well as Preset.

---

---

## Additional Observation — Session Builder Settings Icon

A standalone written observation was produced this week on the settings cog icon within the Session Builder interface. The core finding: the cog communicates that something is interactive and configurable, but gives no indication of what type of configuration is available in this specific context. This places an interpretive burden on the user before the session-building process has even begun.

Grounded in Nielsen's (1994) recognition-over-recall principle, Norman's (2013) distinction between affordance and signifier, Sweller's (1988) cognitive load theory, and McDougall et al. (2000) on icon usability. Recommendation: add a short contextual label — "Session Settings" or "Builder Options" — or use progressive disclosure (tooltip/hover state) to resolve the ambiguity without altering the visual aesthetic.

The wider point this observation surfaces: InnerSeed Garden is currently designed with an expert user's mental model built in. The UX consultancy process running alongside development is specifically designed to surface and address the gap between that internal model and the first-time user's experience. This is a normal and well-documented stage in professional software development.

---

## Week 4 — What carries forward and what moves on

The sequencing below is proposed and fluid, to be refined in the light of the 18 June focus call and subsequent direction from ISD.

**Preset mode — complete.** Completion flow logged in full (D-22, D-30, D-33, D-34). Green House opened and contextualised (D-36). Cinematic mode proposal documented (D-26). Filter mode deferred to mobile testing by design — it falls naturally within the Preset browsing flow at that stage.

**Builder mode — Week 4 headline focus.** A first look produced initial findings (D-39 to D-43). The full structured audit continues in Week 4, applying the same lens used across Weeks 2 and 3. Jeroen's direction from the 18 June focus call — reduce noise, foreground the breath and the Root/Rise/Return story — directly frames this work.

**Mobile testing — Week 4 or 5.** Re-runs both Preset and Builder journeys on a touch device as a stress test of existing findings, particularly D-04 and D-21. Filter mode tested here. Timing confirmed in the weekly focus call.

**Analytics and human testing — Week 4 or 5.** Both follow the completion of Builder mode and mobile testing. Analytics framework is a "what to measure" list, not a build specification. Human testing brief to be written once the full audit is substantially complete.

**Comms and findings integration into Green House — active.** Moved from unscoped placeholder to live conversation following the 18 June focus call.

**Still open:** D-03 (Critical — Dutch language and content instability, escalated through D-23 and D-35) and D-21 (threefold consistency) remain the two highest-priority outstanding items. Friday 13 June focus call notes still not formally logged.



- Filter mode — not yet tested within the Preset browsing flow
- Builder mode — full UX audit, headline focus for the remainder of Week 3; includes a deliberate retest of D-32 (does Recent survive a Garden–Sessions round trip)
- Mobile testing — stress test of existing findings, particularly D-04 and D-21
- Analytics and human testing — groundwork for Week 4 delivery
- Comms and findings integration plan — scoped against the Greenhouse; now an active conversation following the 18 June focus call
- Friday 13 June focus call — not yet formally logged

---

## Folder Structure — Final Week 3 State

```
📁 INNERSEED GARDEN
    📁 SSOT - Raw & Background
        innerseed_appendix (master reference, updated 18 Jun 2026)
        innerseed_recovery_brief (updated 18 Jun 2026)
        📁 SSOT - Week 1 ✅
        📁 SSOT - Week 2 ✅
        📁 SSOT - Week 3 ✅
            RAW_NOTES_-_Week_3.docx
            UX_Observation_Session_Builder_Settings_Icon.docx
    📁 UX Dev Manifesto
        📁 UX Dev Logs
            Week 1 ✅
            Week 2 ✅
            Week 3 ✅ Complete — D-01 to D-38
    📁 University
        Markdown summaries (this document) ✅
        InnerSeed_Reflective_Captures_Sources.md ✅
    📁 Seed Vault
        InnerSeed_TheSeedVault.html ✅ Opened 18 Jun 2026
```

---

*InnerSeed Garden · UX Development Manifesto · Week 3 Summary · Ruaraidh · 15–18 June 2026 · Complete · innerseed.garden*
