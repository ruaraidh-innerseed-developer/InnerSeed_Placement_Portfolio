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

### Licensing our own content ⟨OPEN⟩

Should STAN's explainers be published under CC-BY, so other services can reuse
them with attribution?

**For:** the mission is that good information spreads. A needle exchange in
Dundee reusing our SHBG explainer is a win, not a loss. It is what a non-profit
does, and it is a credibility signal to academics and funders.

**Against:** someone can lift the useful half and drop the caveats, and the
caveats are the part that makes it safe. Our name may end up on a stripped
version.

My lean is **CC-BY with a clause requiring the status label and the "what this
does not tell you" section to travel with the text** — but this is a decision
for you, and it is easier to open a licence later than to close one.

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

## Next actions from this note

1. Get **Grant 2023** and **Solanki 2023** into `sources-inbox/`. Free, five
   minutes each, and they unblock the most.
2. Decide the licence ⟨OPEN⟩ — not urgent, but before anything publishes.
3. Keep reader data collection at "almost nothing" until the tracker forces the
   question, then answer it properly.
4. Put the search-log offer in the clinician approach as a second-email card, not
   the first — the first email should stay a small ask.
