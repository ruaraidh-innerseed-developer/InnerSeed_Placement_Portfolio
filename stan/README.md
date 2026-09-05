# STAN — Steroid Awareness Network

**Status: foundation, pre-launch. Nothing here is published or citable yet.**

STAN is a planned UK non-profit **support network** for people affected by
performance-enhancing drug use — those using, those trying to stop, those living
with the consequences, and the clinicians who encounter them without a pathway to
follow.

Support network, not library. The gap is filled by people as much as by pages:
navigation, trained peer support, facilitated groups, seminars, and clinical
consultation through vetted partners. The published information exists to make
that support accurate; it is not the whole service.

This directory is the foundation. It is deliberately **not a website**. No
platform decision has been made, and none is needed yet, because everything here
survives any platform decision made later.

---

## Why the evidence register comes first

The website is a renderer. The asset is the register.

STAN's entire proposition is that it can be trusted in a field where almost
nothing can be. That trust is not produced by design or by tone of voice. It is
produced by a governance apparatus that can be inspected — and the register is
that apparatus in its most concrete form.

It also happens to be the thing that makes the pitch to a clinical partner
possible. A prospective clinical lead does not want to see a homepage. They want
to know what happens when someone writes something wrong.

And it is what makes the *support* safe. A peer supporter's most useful sentence
is "I can't answer that, but here's what we know and here's who can." Both halves
of that sentence come out of the register. Support without it is just opinion
delivered kindly.

## What's here

```
stan/
├── BACKEND-PLAN.md        How content gets sourced, claimed and composed
├── QA-ENGINE.md           How the AI-assisted search works, and its limits
├── DATA-NOTE.md           Information in, information out; licence decision
├── governance/            Scope, evidence policy, interim standard,
│                          support model, crisis protocol
├── knowledge/
│   ├── schema/            marker · claim · question · answer
│   ├── questions/         68 catalogued, 0 answered. The roadmap.
│   ├── claims/            20, all draft — quotes not yet verified
│   ├── answers/           EMPTY — no claims to compose from yet
│   └── markers/           16 identity-only stubs
├── evidence/sources/      10 records, 1 read (one chapter)
├── evidence/reference-chase/  Numbered refs inside a source, waiting to be obtained
├── services/              Crisis signposting, Scotland and England
├── sources-inbox/         Drop documents here. Gitignored — copyright.
├── content/pages/         Prose that makes no clinical claim
├── content/articles/      The article stack — what is writeable, and what each still needs
├── data/                  Routes, sessions and the service ladder for the front end
├── outreach/              The clinical lead approach
├── prototype/             template.html (edit) · index.html (GENERATED)
├── dist/                  GENERATED static site. Not committed.
└── tools/                 validate · build · prerender · design-pdf ·
                           coverage · query · new · bibliography
```

## Using it

```bash
python3 stan/tools/validate.py         # check every register against policy
python3 stan/tools/build.py            # compile into the single-file preview
python3 stan/tools/build.py --mode site  # compile into dist/ with real URLs
python3 stan/tools/prerender.py        # one indexable HTML file per destination
python3 stan/tools/design-pdf.py       # a PDF of the front end, to show someone
python3 stan/tools/new.py page shbg    # scaffold a new content page
python3 stan/tools/new.py source x-2024-y
python3 stan/tools/query.py --unread   # the reading list
python3 stan/tools/query.py --topic asih --format full
```

Requires Python 3.11+ and PyYAML.

## The knowledge base — claims, questions, answers

**See `BACKEND-PLAN.md` and `QA-ENGINE.md` for the full design.** In short:

```
sources/    a document someone has READ in full
   ↓
claims/     one statement · one source · one VERBATIM quote
   ↓
answers/    one question answered, composed only of claims
   ↓
questions/  what people ask. Asserts nothing. Outnumbers answers.
markers/    an index over claims, not a container for prose
```

**The rule that holds it together:** a claim needs a quote from a source that
has been read. No quote, no claim. No claims, no answer. That makes
"backed" a property the schema can check rather than a promise someone made.

This replaced a marker-first design after the first content sweep produced
sixty fields of prose citing nothing. The fault was structural — the schema
permitted it — so the schema is where it got fixed.

**The AI split, from `QA-ENGINE.md`:** at build time AI reads sources and
proposes claims and drafts, all reviewed before publication. At query time it
matches a reader's messy question to an already-approved answer and **writes
nothing**. Every answer a reader sees was reviewed before they asked. That is
what a clinician can actually sign off.

```bash
python3 stan/tools/coverage.py         # marker encyclopedia completeness
python3 stan/tools/validate.py         # all registers against policy
python3 stan/tools/build.py            # compile the hub
```

## How the hub is built

**The repository is the source of truth. The site is a generated artefact.**

`prototype/index.html` is compiled and must never be hand-edited — your changes
would be overwritten on the next build. To change what the site says, change the
data:

| To change | Edit |
|---|---|
| What search finds, and its status badge | `content/pages/*.md` frontmatter |
| The "Why are you here?" routes and their cards | `data/routes.yaml` |
| Group sessions, countries, session types | `data/sessions.yaml` |
| The service ladder — what can be booked, at which stage, for how much, and where it may be offered | `data/services.yaml` |
| The page's colour rhythm — three looks switchable in the prototype bar (`LOOKS` in the template) | `prototype/template.html` |
| The crisis numbers in the footer | `services/crisis-services.yaml` |
| What a source may and may not be cited for | `evidence/sources/*.yaml` |
| A statement STAN can make, its quote and its page | `knowledge/claims/*.yaml` |
| Which articles are next, and what blocks each | `content/articles/README.md` |
| Layout, styling, copy | `prototype/template.html` |
| The domain, and whether it is confirmed | `data/site.yaml` |

Then `python3 stan/tools/build.py` and republish. `build.py --check` fails if the
generated page has drifted from the data, which is what a CI step would run.

The build enforces a few things quietly. A route card pointing at a page pulls
that page's real status, so badges cannot go stale. A route pointing at a page
that does not exist fails the build. A session naming an unknown country or type
fails the build. And a crisis service whose hours do not say "24 hours" is
automatically flagged amber on the page — so a new part-hours service is caught
without anyone remembering to mark it.

The counters in the site footer are read from the repository too: pages reviewed
and drafted, sources approved, crisis services verified. The site reports its own
real state rather than a claim about it.

## The two fields that matter

Every source record carries `claims_supported` and `claims_not_supported`.

A bibliography records what was read. This register records **what each source
may and may not be used to claim.** The dominant failure in this field is not
fabrication, it is *stretching* — citing a real study of 60-year-old men with
age-related hypogonadism to support a claim about someone four years off
400mg/week. The populations differ, the study does not support the claim, and the
citation makes the claim look sourced.

A reviewer checks a draft against those two fields, not against the paper's title.

The register carries a second axis for the same reason: `population_relevance`.
A grade A guideline can still be only *partially* relevant, and a claim about
post-AAS recovery may not rest on indirect sources alone.

## Current state — read this before assuming anything is usable

All five seeded records are at `status: added`. **None is citable.**

Abstracts have been read; full texts have not. Bibliographic verification is
`partial` across the board — DOIs, PMIDs, journals and years are confirmed, but
page ranges and full author lists came from secondary sources. No clinical
reviewer exists yet, and per `EVIDENCE-POLICY.md` §8 the founder cannot
self-approve clinical content.

This is the register working, not the register being incomplete. A system that
can represent its own uncertainty is worth more than one that cannot.

## Next actions

**Evidence**
1. Obtain and read the five full texts. Promote `bibliographic` to `verified`
   against publisher records; set `full_text_read: true`.
2. Resolve the flag on `solanki-2023-asih-recovery-scoping-review` — a secondary
   summary reports gonadotrophin recovery over 3–6 months. That figure must not
   be quoted until the exposure profile of the underlying populations is known.
   It is the highest misuse risk currently in the register.
3. Expand coverage into the thin areas: `women-and-peds`, `adolescents`,
   `cardiovascular`, `harm-reduction`, `service-access-uk`.

**Governance**
4. Legal review of `SCOPE.md` (§4, §7) and `SUPPORT-MODEL.md` (§9 especially —
   confidentiality limits and disclosure of criminal activity).
5. Decide entity form. CIC limited by guarantee is the current working
   assumption; jurisdiction is unresolved and changes the answer.
6. Draft the safeguarding policy. Required before any public launch and before
   any support channel opens.

**Support** — governed by `SUPPORT-MODEL.md` and `CRISIS-PROTOCOL.md`
7. **Verify all nine crisis service entries** against each provider's own
   website and promote them to `verified`. Eight are currently unconfirmed.
   This is roughly ten minutes of work and it blocks every support channel.
8. Close the gaps listed at the foot of `crisis-services.yaml`: a Scottish
   drugs information route, needle and syringe programme access, and a decision
   on whether STAN's signposting covers Wales and Northern Ireland.
9. Set up the STAN email address and implement the auto-reply in
   `CRISIS-PROTOCOL.md` §4. Never use a personal address for a public contact
   route — it cannot carry an auto-response and cannot be covered.
10. Collect evidence under `peer-support` and `mental-health`. Two specific
    needs: the risk profile of AAS cessation, which the crisis protocol assumes,
    and the "asking directly does not increase risk" claim the protocol makes.
11. Start with recorded seminars. Lowest risk, reviewable in advance, and the
    best demonstration of quality to a prospective clinical partner.

**People** — the binding constraint, not the code
12. Recruit a clinical lead. The author group on
    `grant-2023-endocrinologist-survey` (Grant, Pradeep, Minhas, Dhillo, Quinton,
    Jayasena) is effectively a shortlist of UK academics and clinicians working in
    exactly this area. Approach academics before clinics.
13. Reproductive urology, andrology and male fertility services see
    AAS-related presentations far more often than general endocrinology. Target
    accordingly.
14. Define the founder's role per `SUPPORT-MODEL.md` §7 — designing and holding
    the standard, not being the always-on contact. Includes arranging supervision
    for the founder, which is the step most likely to be skipped.

**Content — the encyclopedia**

Fill the marker records. Do it by field across the whole set, not record by
record — `coverage.py --next` names the sweep. Every field filled becomes a
searchable answer without anyone writing it as prose.

15. Sweep `what_it_is`, `made_where`, `controlled_by`, `functions` across all 16
    markers. That alone gives the hub sixteen real answers to "what is X".
16. Then sweep the states: `low`, `high`, `suppressed`, `recovery`. These are the
    ones people actually search for, and `suppressed` is the one nobody else has.
17. Then `does_not_tell_you` and the `female_note` fields.
18. Add markers as gaps appear. `new.py` does not scaffold markers yet — copy an
    existing stub, or ask for that to be added.

Discipline throughout (`INTERIM-STANDARD.md`): report and attribute, never
advise. No reference range quoted as authoritative. No recovery timeline the
evidence does not support. Nothing containing the word "should".

**Product**
19. Build one content page to full publishable standard, using the index case
    (high SHBG, low calculated free testosterone, symptomatic on transdermal
    replacement after prolonged supraphysiological exposure). That page, plus its
    consultation brief, is the specimen to put in front of a prospective clinical
    lead. Not a deck — a specimen.

**Deferred on purpose**
20. Platform. Current lean is Next.js + Postgres + Payload CMS, with
    Django + Wagtail the serious alternative if Python is the more comfortable
    language. Nothing above depends on that choice. Make it when there is content
    to render and a second person to hand it to.

---

*Draft foundation documents. Not adopted, not legally reviewed, not clinically
signed off.*
