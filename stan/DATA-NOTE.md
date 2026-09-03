# Working note — information in, information out

**Not policy. A working note on a workstream we agreed to keep in view.**
Decisions marked ⟨OPEN⟩ need a call before they harden.

---

## Part one — what comes in

### The four inputs, and how much each can be trusted

| Input | Good for | Not good for |
|---|---|---|
| **Documents you obtain** (`sources-inbox/`) | Everything. The only way to read a paper in full. | Nothing — this is the gold standard. Bottleneck is your time. |
| **Live web search** | Finding what exists; confirming DOIs, authors, journals; checking a service is still running. | Knowing what a paper actually says. Returns abstracts and snippets only. |
| **Claude's general knowledge** | Settled physiology — Tier 1 fields. Fast, and reliable for uncontested textbook material. | Anything specific, recent, contested, or thin. Which is exactly the ASIH literature. |
| **What readers search for** | Deciding what to write next. | Deciding what is true. Never confuse the two. |

The sourcing tiers are written into `knowledge/schema/marker.schema.yaml` so they
sit where they get used rather than in a document nobody opens.

### The bottleneck, stated plainly

Claude cannot fetch journal articles from the session environment — publisher
domains are blocked. Tier 3 content (suppression, recovery) therefore moves at
the speed of you downloading PDFs. Everything else can move faster.

Two free downloads unblock the most: **Grant 2023** and **Solanki 2023**.

### What we collect from readers

Almost nothing, on purpose.

- **Unmet searches.** The query string and a date. Nothing else, no account, no
  identifier. In the prototype this sits in the reader's own browser and is sent
  nowhere.
- **Route choices.** Counts only — how many people picked "I've stopped and I
  feel wrong". Not who.

That is the whole list, and it should stay close to it. A search term in this
field is a disclosure. "My SHBG is 78 and I can't get an erection" typed into a
box is health data about an identifiable person the moment it is tied to
anything. So: **no accounts to read anything, no analytics that fingerprint, no
search term ever stored against a person.**

Collecting nothing is also a feature we can say out loud. Almost nobody in this
space can.

⟨OPEN⟩ When the bloodwork tracker exists, that changes — it necessarily holds
health data. Different question, needs its own answer before it is built.

## Part two — what goes out

### The formats

The same knowledge base should reach people in more than one shape. It already
supports this: fill a field once, and it can render as any of these.

1. **Q&A** — the search answers. Already working.
2. **Marker pages** — the encyclopedia entry, read whole.
3. **The consultation brief** — the sheet handed to a GP. Drafted.
4. **Print** — a leaflet a needle exchange can put on a counter. Costs almost
   nothing once the records are filled, and reaches people who will never visit
   a website.
5. **Spoken** — seminar scripts drawn from the same records, so what is said in a
   room matches what is written.

Point 4 is worth remembering. The people at highest risk are often not the ones
Googling at 2am; they are the ones already walking into a service.

### Licensing our own content — DECIDED: all rights reserved, for now

**Decision (founder, this session): STAN's content is not openly licensed.
No CC licence until provenance is established and content is clinically
reviewed.** Revisit once the register carries approved sources and a clinical
lead is in place.

The reasoning, worst risk first:

1. **A CC licence is irrevocable.** Perpetual for every version released under
   it. Future versions can be relicensed; copies already out cannot be recalled.
   If a page later proves wrong we can correct ours and not theirs — and theirs
   still carries our name.
2. **Attribution runs backwards.** CC-BY obliges downstream users to credit us,
   which guarantees our name travels with modified content we no longer control.
3. **Modification is the point of CC-BY.** Someone may lawfully strip
   `does_not_tell_you`, add a dosing section, and republish attributed to STAN.
   NoDerivatives blocks that and also blocks the legitimate reuse — a service
   reformatting a page as a leaflet — that was the reason to license at all.
4. **We would be licensing unverified content.** Every source record still says
   `full_text_read: false` and nothing is clinically reviewed. Granting
   perpetual redistribution over material whose provenance we cannot yet prove
   is backwards, and settles it on its own.
5. **It makes the clinical lead harder to recruit.** Asking someone to stake
   their registration on content that is also freely modifiable by anyone is a
   worse offer.

**A superseded suggestion, recorded so it is not repeated:** "CC-BY plus a
clause requiring the status label and caveats to travel with the text" does not
work. Adding restrictions to a CC licence stops it being one — losing the single
real benefit, that another organisation's legal team recognises it instantly —
and leaves a bespoke licence enforceable only by litigation a small non-profit
will never bring.

**What a restrictive licence does not do:** protect against AI scraping or
regurgitation. A publicly readable page gets crawled whatever its licence.
Closed licensing guards against irrevocability and modification; it does nothing
for misinformation. The defences against *that* are the provenance chain, the
status labels, `claims_not_supported`, and refusing to publish figures we cannot
stand behind — all of which work regardless of who copies us.

⟨CHECK⟩ The GitHub repository holding all of this — is it public? If so the
content is already readable and crawlable. That does not change the licence
position (no licence stated means all rights reserved) but "private first" and
"public repo" are in tension and the actual setting should be known.

### Sharing with researchers — the asset nobody else has

Over time the unmet-search log becomes something genuinely novel: **a record of
what people affected by PED use actually ask, in their own words, at the moment
they need an answer.**

No one has that. It cannot be obtained by surveying clinicians, and it is the
kind of thing that seeds real research questions. Offered to a group like
Jayasena's — anonymous, aggregated, freely — it is worth more than anything else
STAN can put on the table early, and it costs nothing to give.

It is also a reason for a researcher to stay involved after the first
conversation, which is the harder problem.

### Publishing what we don't cover ⟨OPEN⟩

Proposal: publish the top unmet searches openly, as a live page.

It is an unusually honest thing to do, it is a standing advert aimed exactly at
people who could help fill the gaps, and it makes the case for funding better
than any pitch. The risk is that it reads as a list of failures. I think it reads
as confidence, but that is a judgement call.

---

### The corrections log ⟨PROPOSED⟩

If STAN is to be the thing people check *against*, it needs something it does not
yet have: **a public, dated record of what we published, what turned out to be
wrong, when we found out, and what changed.**

Nobody in this field does this. It costs almost nothing. And it answers the
misinformation worry in the only way that is actually available — not by
preventing errors, which is impossible, but by proving they get caught and named.

It also converts the project's biggest vulnerability into its strongest signal.
"We got this wrong in March and here is the correction" is a demonstration of the
system working. Silence, when someone eventually finds an error, is not.

Suggested shape: one entry per correction — date found, what was wrong, how it
was found, what changed, who checked it. Committed to the repository like
everything else, so the history is not editable after the fact.

## Next actions from this note

1. Get **Grant 2023** and **Solanki 2023** into `sources-inbox/`. Free, five
   minutes each, and they unblock the most.
2. ~~Decide the licence~~ — decided: all rights reserved for now. Revisit when
   sources are verified and a clinical lead is appointed.
3. Check whether the GitHub repository is public ⟨CHECK⟩.
4. Keep reader data collection at "almost nothing" until the tracker forces the
   question, then answer it properly.
5. Put the search-log offer in the clinician approach as a second-email card, not
   the first — the first email should stay a small ask.
6. Decide on the corrections log ⟨PROPOSED⟩.
