# Decisions

Settled things, with the date they were settled. **A future session does not
reopen anything on this list.** If something here is wrong, change the line and
date the change — do not argue it in chat and leave the file behind.

Open questions are at the bottom. Those are fair game.

---

## Settled

**2026-09-15 — STAN is not the business.**
STAN is the public, evidence-governed resource. The business is Ruaraidh's
practice as a recovery coach specialising in coming off anabolic steroids. STAN
provides credibility and reach; the coaching is what earns. Documents that treat
STAN as the revenue-generating entity are out of date.

*Validation outstanding.* This is a decision, not a proven finding. Three checks
have not been done: search volume via Google Keyword Planner, who else offers
coming-off coaching on Instagram and TikTok, and the language people use in
forums. Do not write as though the market is confirmed.

**2026-09-15 — The disclosure rule.**
Wherever STAN points at the founder's paid coaching, the page says plainly that
it is run by the same person who built STAN, that he charges for it, and shows
other routes including free ones. STAN's value is that it is not selling. An
undisclosed funnel to the founder destroys that on the day someone notices.

**2026-09-15 — No behavioural advertising, ever.**
No advertising or analytics pixels on any page about steroid use, coming off, or
symptoms. That leaks health data to ad platforms. No inferring drug use from
browsing and marketing on the inference. No selling, renting or sharing any
contact list.

**2026-09-15 — Email is consent-based and segmented by what people tell us.**
People say what they want to hear about and get only that. An address given for
one purpose is not used for another. Under UK GDPR this is special category
health data and under PECR marketing to individuals needs consent; both are
binding, and the trust cost of getting it wrong is larger than the legal one.

**2026-09-15 — Group formation is a legitimate use of the data, and a product.**
Matching people who want the same kind of room at the same time is useful to
them and is the best commercial use of what STAN knows. It is a service, not
marketing.

**2026-09-15 — Aggregate data is the long-term asset.**
The unmet-question log and, later, outcomes over time. Anonymous, no individual
identifiable. That is what a researcher or a commissioner will pay for.

**2026-09-05 — No dosing, ever.**
No doses, cycle lengths, stacking, tapering or post-cycle protocols on any
published page, including while explaining why something does not work.
`governance/SCOPE.md` governs. Claims may record what a source says; publication
is separate and forbidden.

**2026-09-05 — No claim without a verbatim quote from a source someone read.**
The quote comes first and the sentence is written from it. Enforced by
`knowledge/schema/claim.schema.yaml` and `tools/validate.py`.

**2026-09-05 — Editorial position: true, proven and safe are three questions.**
`governance/EDITORIAL-VOICE.md`. Do not fight everything, do not moralise, and
concede plainly that steroids work.

**2026-09-05 — Value first on the website.**
No price appears on the front door. Every route hands to something free. Paid
services are offered only on pages that have already given the reader something,
enforced by the build.

**2026-09-15 — STAN is independent of InnerSeed.**
No affiliation of any kind. STAN moves to its own repository. Nothing in STAN
references InnerSeed and nothing should.

---

## Open

- **Where Ruaraidh is based.** Scotland or England. Affects commissioning,
  signposting, and whether the Edinburgh IPED clinic is a doorstep conversation.
  Asked repeatedly, never recorded.
- **What the coaching is called.** Not "recovery coaching" generically.
- **What it costs.** No figure has been set by Ruaraidh. Every price currently
  in `data/services.yaml` and `COMMERCIAL.md` is provisional, and some were
  invented by an assistant and should be treated as placeholders.
- **Coaching training and insurance.** Which qualification, and whether it is
  needed before taking a first client.
- **The domain name.** `data/site.yaml` holds a placeholder and the build warns.
- **The entity.** Sole trader, limited company, or something with a charity
  alongside. Nothing exists yet.
- **Whether STAN stays free-standing or becomes part of the coaching brand.**
  Currently free-standing, with disclosure.
