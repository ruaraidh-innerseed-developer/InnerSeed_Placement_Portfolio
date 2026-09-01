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
├── governance/
│   ├── SCOPE.md              What STAN does and — more importantly — does not do
│   ├── EVIDENCE-POLICY.md    How sources are graded, reviewed and approved
│   └── SUPPORT-MODEL.md      How human support is governed: tiers, boundaries,
│                             crisis protocol, groups, supervision
├── evidence/
│   ├── schema/
│   │   └── source.schema.yaml   The record schema. Editing it is a governance act.
│   └── sources/                 One YAML file per source. 5 seeded.
├── tools/
│   ├── validate.py           Enforces the policy. Exits non-zero on breach.
│   └── query.py              Search and filter the register.
└── templates/
    ├── content-page.md       The governed content unit
    └── consultation-brief.md The document a reader takes to their GP
```

## Using it

```bash
python3 stan/tools/validate.py                  # check the register
python3 stan/tools/query.py                     # list everything
python3 stan/tools/query.py --unread            # the reading list
python3 stan/tools/query.py --topic asih --format full
python3 stan/tools/query.py --citable           # what may be cited today
```

Requires Python 3.11+ and PyYAML.

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

**Support** — governed by `SUPPORT-MODEL.md`
7. Collect evidence under the `peer-support` and `mental-health` topics. The
   crisis protocol depends on knowing the actual risk profile of AAS cessation,
   and the tier model should be built on established peer support practice
   rather than invented here.
8. Write the crisis protocol. It is the first thing needed and the thing most
   likely to be deferred.
9. Complete the jurisdiction-dependent crisis signposting list once STAN's base
   and coverage are settled.
10. Start with recorded seminars. Lowest risk, reviewable in advance, and the
    best demonstration of quality to a prospective clinical partner.

**People** — the binding constraint, not the code
11. Recruit a clinical lead. The author group on
    `grant-2023-endocrinologist-survey` (Grant, Pradeep, Minhas, Dhillo, Quinton,
    Jayasena) is effectively a shortlist of UK academics and clinicians working in
    exactly this area. Approach academics before clinics.
12. Reproductive urology, andrology and male fertility services see
    AAS-related presentations far more often than general endocrinology. Target
    accordingly.
13. Define the founder's role per `SUPPORT-MODEL.md` §7 — designing and holding
    the standard, not being the always-on contact. Includes arranging supervision
    for the founder, which is the step most likely to be skipped.

**Product**
14. Build one content page to full publishable standard, using the index case
    (high SHBG, low calculated free testosterone, symptomatic on transdermal
    replacement after prolonged supraphysiological exposure). That page, plus its
    consultation brief, is the specimen to put in front of a prospective clinical
    lead. Not a deck — a specimen.

**Deferred on purpose**
15. Platform. Current lean is Next.js + Postgres + Payload CMS, with
    Django + Wagtail the serious alternative if Python is the more comfortable
    language. Nothing above depends on that choice. Make it when there is content
    to render and a second person to hand it to.

---

*Draft foundation documents. Not adopted, not legally reviewed, not clinically
signed off.*
