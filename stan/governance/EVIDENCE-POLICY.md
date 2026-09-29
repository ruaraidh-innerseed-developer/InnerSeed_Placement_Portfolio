# STAN — Evidence Policy

**Status: DRAFT v0.1.** Not adopted. Requires sign-off by a named clinical lead.

This document defines how sources enter the STAN evidence register, how they are
graded, and how they may be used. The register is at `stan/evidence/sources/`.

---

## 1. Why a register rather than a bibliography

A bibliography records what was read. A register records **what each source may
and may not be used to claim**. That distinction is the whole point.

The dominant failure mode in this field is not fabrication — it is *stretching*:
citing a real study about 60-year-old men with age-related hypogonadism to
support a claim about a 32-year-old four years off 400mg/week of testosterone
enanthate. The populations are not the same, the study does not support the
claim, and the citation makes the claim look sourced.

Every record therefore carries two fields that do the real work:

- `claims_supported` — what this source may be cited for.
- `claims_not_supported` — what it must never be cited for, especially where
  misuse is foreseeable.

A reviewer checking a draft page checks the claim against these fields, not
against the title of the paper.

## 2. Evidence grade (`STAN-EL-1`)

This is STAN's own scheme. It is not GRADE, not SIGN, not Oxford CEBM, and is
not presented as equivalent to any of them.

| Grade | Meaning |
|---|---|
| **A** | Guideline or formal position statement from a recognised professional body; or a high-quality systematic review with a clearly defined and relevant population. |
| **B** | Peer-reviewed primary research with a control or comparison group, adequate sample, and a population that reasonably matches STAN's readership. |
| **C** | Peer-reviewed but limited: small sample, uncontrolled, cross-sectional with high confounding, indirect population, or a scoping/narrative review. |
| **D** | Grey literature, expert opinion, case report, conference abstract, regulatory or service documentation, or a lived-experience account. |

Grade D sources are legitimate and often necessary — a needle and syringe
programme's service description is grade D and is exactly the right citation for
a signposting page. Grade is about *what kind of weight a source can bear*, not
about whether it is any good.

## 3. Population relevance — the second axis

Grade alone is insufficient. A grade A guideline on age-related hypogonadism may
have low relevance to a post-AAS population. Every record carries:

| Value | Meaning |
|---|---|
| `direct` | Study population is PED users or former users. |
| `partial` | Population overlaps but differs materially (e.g. hypogonadal men of mixed aetiology, including but not limited to AAS). |
| `indirect` | Population does not match; the source is cited for a mechanism, method, or reference range that generalises. |
| `unclear` | Not determinable from the abstract; requires full-text read. |

**A claim about post-AAS recovery may not rest solely on `indirect` sources.**
If that is all that exists, the page must say so.

## 4. Lifecycle of a source

```
  added ──▶ bibliographic verification ──▶ full-text read ──▶ clinical review ──▶ approved
                                                                                     │
                                                                        scheduled re-review
                                                                                     │
                                                                          approved / retired
```

- **added** — record exists, fields may be incomplete. Not citable.
- **in-review** — full text read, claims fields drafted. Not citable.
- **approved** — clinical reviewer named, review date recorded, next review due.
  Citable in published content.
- **retired** — superseded, withdrawn, or found unreliable. Never deleted; the
  record stays with `status: retired` and a reason, because pages that once
  cited it must remain auditable.

**Nothing at `added` or `in-review` may be cited in published content.** The
validator enforces this once content pages exist.

## 5. Re-review intervals

| Source type | Interval |
|---|---|
| Guideline / position statement | 12 months (bodies revise, and a superseded guideline is worse than none) |
| Primary research / reviews | 24 months |
| Service and signposting records | 6 months (services close, move, and change referral criteria) |
| Regulatory / legal | 12 months |

## 6. Verification honesty

`verification.bibliographic` records how confident we are in the citation
metadata itself:

- `verified` — checked against the publisher record or PubMed.
- `partial` — core identifiers confirmed, some fields (page range, full author
  list) taken from a secondary source.
- `unverified` — entered from memory or a single secondary mention. **Never
  citable.**

This field exists because a wrong DOI in a credibility project is worse than a
missing one. A register that can represent its own uncertainty is more
trustworthy than one that cannot.

## 7. Conflicts of interest

Where a source has funding or author conflicts material to its conclusions
(industry-funded TRT trials being the obvious case), record them in
`conflicts_of_interest`. Absence of a declaration is recorded as
`"not stated in source"`, never as "none".

## 8. Who may approve

Approval to `status: approved` requires a named clinical reviewer with relevant
registration (GMC, GPhC, NMC, or equivalent) recorded in `review.clinical_reviewer`.

**The founder cannot self-approve clinical content.** Lived experience
determines which questions matter; it does not determine what publishes as
guidance. This constraint is not a formality — it is the specific thing that
makes STAN's knowledge safe to use and makes the organisation credible to the
clinicians it needs.

---

## Appendix — controlled vocabulary for `topics`

```
asih                      anabolic-steroid-induced hypogonadism
hpg-axis-recovery         recovery of the HPG axis after cessation
trt-initiation            starting testosterone replacement
trt-monitoring            monitoring on replacement
shbg-free-testosterone    SHBG, calculated free testosterone, bioavailability
oestradiol-management     aromatisation, oestradiol, AI use
fertility-spermatogenesis fertility, sperm parameters, gonadotrophins
cardiovascular            cardiac and vascular consequences
mental-health             mood, dependence, suicidality, psychiatric effects
pct-restart               post-cycle therapy and restart approaches
delivery-routes           esters, gels, pellets, pharmacokinetics
harm-reduction            harm-reduction practice and services
peer-support              peer support models, effectiveness, and governance
women-and-peds            PED use in women
adolescents               use in under-18s
service-access-uk         UK service provision, pathways, and gaps
epidemiology              prevalence and population data
```

New topics are added by amending this list, not by inventing them in a record.
The validator rejects unknown topics.
