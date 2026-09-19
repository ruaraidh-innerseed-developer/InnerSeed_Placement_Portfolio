# STAN — working rules

Read the root `CLAUDE.md` too. This file covers what is specific to STAN.

STAN is an independent UK resource for people affected by anabolic steroid use.
It is **not the business**. The business is Ruaraidh's practice as a recovery
coach specialising in coming off; STAN gives it credibility and reach. See
`STRATEGY.md`.

**Read `DECISIONS.md` first.** It lists what is settled and what is open. Do not
reopen anything on the settled list, and do not treat anything on the open list
as decided — especially prices, which are placeholders.

STAN has no affiliation with InnerSeed. Nothing in here references it.

## The three rules that keep getting broken

**1. `prototype/index.html` is generated. Never edit it.**
Edit the data, or `prototype/template.html`, then rebuild. Hand edits are
overwritten and lost.

```bash
python3 stan/tools/build.py              # single-file preview → prototype/index.html
python3 stan/tools/build.py --mode site  # static site → dist/
python3 stan/tools/prerender.py          # one real page per destination + sitemap
python3 stan/tools/validate.py           # every register against policy
python3 stan/tools/design-pdf.py         # PDF of the front end, to show someone
```

**2. No claim without a verbatim quote from a source someone has read.**
This is the whole point of the repository. A statement about physiology, risk or
treatment exists only as a record in `knowledge/claims/` carrying the exact words
from the source and the page they came from. The quote comes first; the sentence
is written from it. Never the other way round.

The schema enforces most of this and `validate.py` checks it. Do not work around
either.

**3. No dosing. Ever.**
No doses, cycle lengths, stacking, tapering or post-cycle protocols on any
published page — including while explaining why something doesn't work.
`governance/SCOPE.md` governs. Claims may record what a source says, because a
register that omits things is not a register; publication is separate and
forbidden.

## Writing for readers

`governance/EDITORIAL-VOICE.md` is the standard. Its spine: **true, proven and
safe are three different questions.** Grant what is true, name the specific
untested link, and never let "it works" imply "it's safe".

Don't fight everything, don't moralise, and don't repeat a belief in STAN's own
voice when the source is only reporting that users hold it.

## Data and marketing

Binding, and in `DECISIONS.md`:

- **No advertising or analytics pixels** on any page about steroid use, coming
  off, or symptoms. That leaks health data to ad platforms.
- **Never infer** someone's drug use from their behaviour and market on it.
- **Email is consent-based and segmented by what people tell us.** An address
  given for one purpose is not used for another. This is special category health
  data under UK GDPR, and PECR governs the marketing.
- **No list is ever sold, rented or shared.**
- Forming groups from what people have told us is a service, and fine.
- The aggregate — the unmet-question log, outcomes later — is anonymous and is
  the long-term asset.

## Still open

`DECISIONS.md` has the full list. The ones that bite most often: where Ruaraidh
is based, what the coaching is called and costs, the domain, and the entity.

## Current state, honestly

- 20 claims, all draft, **no quote verified against the page**.
- 10 sources, one read, and only one chapter of it.
- 68 questions catalogued, 0 answered.
- 2 articles drafted, neither publishable.
- No public site, no email address, no clinician, no second person.

The apparatus is well ahead of the content, and the content is well ahead of the
people. Building more apparatus does not move the project.
