# Back end — re-evaluated content plan

**Supersedes the marker-first design.** Written after the first Tier 1 sweep
produced sixty fields of prose citing nothing and was scrapped.

---

## 1. What actually went wrong

Not carelessness — a design fault. The marker schema let anyone write into
`what_it_is` while `sources` stayed `[]`, and the validator passed it. The model
permitted unbacked content, so unbacked content appeared.

There was a second, subtler problem. Writing prose and *then* looking for
citations produces **confirmation-shaped citation**: the search becomes a hunt
for sources that agree with what is already written, rather than reading a
source and reporting what it says. Even with honest intent, the result is
sourcing that decorates rather than supports.

Both are fixed the same way: **make the source come first in the data model, not
in someone's good intentions.**

## 2. The new atom: the claim

The unit of knowledge is no longer a marker field. It is a **claim**: one
statement, one source, and the verbatim quote from that source that carries it.
Schema at `knowledge/schema/claim.schema.yaml`.

```yaml
id: lh-secreted-by-anterior-pituitary
statement: LH is secreted by the anterior pituitary gland.
source: endotext-testis-endocrinology
locator: "Section: Hypothalamic-pituitary control of testicular function"
quote: "…verbatim text from the chapter…"
quote_verified: true
kind: direct
population: Healthy adult men, no androgen exposure
does_not_support:
  - Anything about LH under exogenous androgen exposure
```

Three fields do the work:

**`quote`** — verbatim source text. If no passage can be quoted that carries the
statement, there is no claim to make. This single requirement makes writing
before sourcing impossible.

**`population`** — who the source's statement is actually about. The commonest
way health information goes wrong is losing the distinction between the study's
population and the reader's. Recorded per claim, at extraction, while the source
is open.

**`does_not_support`** — foreseeable misuse, written while the limits are fresh
rather than reconstructed later from the statement alone.

There is deliberately **no "inference" kind**. A statement that goes beyond the
source is an opinion, and opinions do not enter the register at any status.

## 3. The pipeline

```
  DOCUMENT            you obtain it, sources-inbox/
      │
      ▼  read in full → evidence/sources/*.yaml, full_text_read: true
  SOURCE
      │
      ▼  extract, one statement at a time, each with its quote
  CLAIMS ──────────────► knowledge/claims/*.yaml
      │
      ▼  compose: an answer to one real question, made only of claims
  ANSWERS ─────────────► knowledge/answers/*.yaml
      │
      ▼  index by marker and topic; render
  THE HUB
```

**Answers** are what readers actually meet. One answer addresses one question a
person genuinely asks — *"my LH is undetectable, what does that mean?"* — and
lists the claims it is built from. Every sentence on the site can be traced back
through a claim to a quote in a document.

Markers and topics stop being containers and become **indexes**: "everything we
can say about SHBG" is a query across claims, not a hand-written page.

## 4. What this structurally prevents

| Failure | What stops it |
|---|---|
| Prose with no source | A claim without a quote is invalid |
| Writing first, citing after | The quote is the input, not the output |
| Stretching a source past its population | `population` recorded per claim |
| Losing track of what a bad source contaminated | Answers list their claims; retire a claim, find every answer |
| Silent drift as sources are superseded | Claims carry status and can be retired without deletion |
| A confident answer where evidence is thin | No claims means no answer. The gap shows. |

That last row matters most. Under the old model an empty area could be filled
with plausible prose. Under this one it simply stays empty, and the hub says so.

## 5. The domain — wider than markers

Markers alone cannot answer *"how do I come off"*. The topic map, expanded per
the brief to cover unsupervised hormonal manipulation generally rather than
anabolic steroids alone:

**The system**
`hpg-axis` · `feedback-and-suppression` · `reading-a-panel`

**The journey**
`considering-starting` · `on-cycle-harm-reduction` · `coming-off` ·
`after-stopping-asih` · `recovery-evidence`

**Consequences**
`fertility` · `cardiovascular` · `mental-health-and-dependence` ·
`liver-and-kidney` · `metabolic`

**Unsupervised hormonal manipulation beyond AAS** — under-served everywhere,
and squarely in scope
`self-managed-trt` · `hcg-and-gonadotrophins` · `serms-and-ai` · `sarms` ·
`peptides-and-gh` · `thyroid-hormone-misuse` · `insulin-misuse` ·
`diuretics-and-dnp`

**People**
`women-and-peds` · `adolescents` · `partners-and-family`

**Getting help**
`uk-services` · `talking-to-a-clinician` · `what-to-ask`

Every topic starts empty. It fills only as claims arrive.

## 6. Order of build

1. **Documents in.** Nothing below can start without them. The four open-access
   foundation chapters listed in `sources-inbox/README.md` are free and cover
   the physiology for the whole encyclopedia.
2. **Read and promote.** Source records move to `full_text_read: true` with real
   authorship, limitations and conflicts recorded.
3. **Extract claims.** Many per source. This is the bulk of the work and it is
   where AI genuinely helps: reading a chapter and proposing claims with quotes
   and locators, for a person to verify.
4. **Verify quotes.** A human compares each quote against the document. This is
   the second-reader job and it needs no clinical qualification — only care.
5. **Compose answers.** From verified claims only.
6. **Tooling** to match: extend `validate.py` to enforce the claim rules, extend
   `build.py` to render answers with their provenance visible, extend
   `coverage.py` to report claims per topic.

Steps 1, 2 and 4 need a person. Steps 3, 5 and 6 are mine.

## 7. What the front end shows meanwhile

Unchanged in design, honest in content. Search returns the sixteen marker names
and says they are not written yet. The counters read zero. That is the correct
state of a project that has scrapped its unbacked content and not yet read its
first source.

The prototype was never the problem and is not being touched.

## 8. Consequence worth stating plainly

Scrapping the unbacked pages means **the clinician approach email currently has
nothing to link to.** That was going to be the specimen.

This is the right cost. Showing a prospective clinical lead a well-written page
that cites nothing would fail worse than showing them nothing — it would tell
them exactly what they most fear about an AI-assisted health project.

What replaces it is better: one answer, built from verified claims, with its
provenance visible from the reader's side. That is a stronger thing to put in
front of a clinician than the page that was there before, and it cannot exist
until a source has been read.
