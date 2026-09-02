# STAN — Interim Publishing Standard

**Status: DRAFT v0.1.** The fallback. In force from adoption until a clinical
lead is appointed, then superseded by the full standard in `EVIDENCE-POLICY.md`.

---

## 1. The problem this solves

`EVIDENCE-POLICY.md` §8 requires a named, registered clinical reviewer before
anything publishes. That is the right long-term rule. It is also, today, a
deadlock: STAN has no clinical lead, so nothing can be approved, so the hub
cannot go live, so there is nothing to show a prospective clinical lead.

Waiting is not neutral. A hub that never launches helps nobody, and an
organisation with nothing live is much harder to recruit to than one with a
working site and real visitors.

This document is the way through. It defines a narrower class of content that
can be published responsibly with no clinician in the room, and it is explicit
about what stays locked until one arrives.

## 2. The line: reporting is not advising

Everything turns on one distinction.

**Reporting** describes what someone else has established, and attributes it.
*"UK guidance from the Society for Endocrinology says that where SHBG is
abnormal, total testosterone may not reflect biological androgen effect."*
That is a true statement about a document, and anyone can verify it.

**Advising** tells a person what is true of them, or what to do about it.
*"Your total testosterone is misleading — you need a free testosterone test."*
That is a clinical judgment about an individual and it requires a clinician.

The word to watch is **should**. Almost every sentence that goes wrong contains
it, or implies it.

## 3. Tier A — publishable now, no clinician required

Five permitted forms. A page that stays inside them can go live under this
standard.

| Form | What it is | Example |
|---|---|---|
| **Signpost** | Naming and linking a service or authority | "The BSSM publishes UK guidance on testosterone deficiency. Read it here." |
| **Attributed report** | What a named source found, stated as theirs | "Rasmussen and colleagues (2016) found former users had lower testosterone than controls years after stopping." |
| **Settled definition** | Uncontested textbook fact | "LH is made by the pituitary gland. It signals the testicles to make testosterone." |
| **Question set** | Things to ask, making no claim | "Ask whether your LH was measured alongside your testosterone." |
| **Lived experience** | One person's account, labelled | "When I came off, this is what the first month was like for me." |

Requirements for every Tier A page:

1. **Attribution on every substantive statement.** If you cannot name whose
   finding it is, it is not a report — it is your opinion, and it waits.
2. **No synthesis across sources.** Reporting two studies is Tier A. Concluding
   something from the pair of them is Tier B.
3. **No numbers attached to prognosis.** No timelines, no recovery odds, no
   "most men". These are the highest-harm claims in this field and they are
   locked regardless of tier.
4. **A second reader.** Not a clinician — anyone competent and not the author.
   One person publishing unchecked is how errors reach the public.
5. **The visible notice** in §5.
6. **Sources named in the register**, even at `added` status. Tier A does not
   require an approved record, because it makes no claim from the record — but
   the record must exist so the trail is auditable.

## 4. Tier B — waits for a clinician

Locked until a clinical lead is appointed, whatever the demand:

- Anything containing *should*, *recommended*, *best*, or *safe*.
- Synthesis: conclusions drawn from combining sources.
- Interpretation of results, including worked examples using realistic numbers.
- Any timeline or probability of recovery.
- Anything about what a treatment does, or whether to have it.
- Anything comparing options.

The flagship draft `content/drafts/how-the-system-works.md` is **Tier B as it
stands** — the primary/secondary table interprets a pattern of results, and that
is a clinical judgment however well established. It could be cut down to a Tier A
version; the interpretation table would have to come out, which would remove most
of its value. Better to leave it drafted and unpublished, and use it as the
specimen when approaching a clinician.

## 5. The notice

Every Tier A page carries this, visibly, near the top — not in a footer:

> **This page has not been reviewed by a clinician.** We are building STAN in the
> open, and we would rather tell you where we are up to than pretend to be
> finished. Everything here either points you at someone qualified or reports what
> a named source found, with the source shown. Nothing here is advice about you.

That notice is a strength, not an embarrassment. Stating your stage plainly reads
as more trustworthy than a polished site making unattributable claims — which
describes most of what else is available in this field.

## 6. What Tier A does not eliminate

Being honest about the residual risk, because pretending it is zero would be the
same error this whole framework exists to prevent.

- **Selection is editorial.** Choosing which guideline to point at, and which
  study to report, is a judgment. A page can mislead through what it omits while
  every individual sentence is true.
- **Framing carries weight.** "Only one study found this" and "a study found this"
  are both accurate and land very differently.
- **Readers infer advice from information.** Someone will read a Tier A page and
  act on it as though it told them what to do. That cannot be prevented, only
  reduced — which is what the notice and the question sets are for.

The second reader in §3.4 exists mostly to catch these three.

## 7. Learning from what people actually look for

The site is the research instrument. What visitors search for and fail to find is
the content plan, and it beats guessing.

The prototype already captures the hook: a search returning nothing says so and
invites the visitor to say what they wanted. Formalise it:

- **Log every search that returns nothing.** No account, no personal data — the
  query string and a date, nothing else.
- **Log which "Why are you here?" route is chosen.** Counts only.
- **Ask, at the point of failure**, in one optional free-text box.
- **Review monthly.** The top unmet queries become the next content, in order.

Two rules on this. Keep it anonymous — search terms in this field are disclosures,
and a logged query tied to a person is special category data STAN has no reason to
hold. And publish the top unmet queries openly; a public list of what STAN does
not yet cover is a recruitment advert aimed precisely at people who could help.

## 8. When this expires

This standard is superseded the moment a clinical lead is appointed. At that
point:

- Every Tier A page already live is re-read by the clinical lead.
- Pages that pass become fully approved and the §5 notice comes off.
- Pages that do not are corrected or withdrawn, and the withdrawal is recorded.
- Tier B unlocks.

**Nothing published under this standard is grandfathered.** Interim means interim.

## 9. Review trigger

This document is reviewed at whichever comes first:

- **6 months** from adoption;
- **a clinical lead being appointed**;
- **1,000 visitors**, or the first month in which unmet-search logging produces
  a clear pattern nobody anticipated;
- **any incident** where a reader reports being misled.

The honest position is that we do not yet know whether this tiering works in
practice. It is a reasonable first attempt, it is written down so it can be
argued with, and real usage will show where it is wrong. That is the correct
state to be in at this stage — not certainty, but a defensible starting point
with a date on it.

---

*Open for legal review alongside `SCOPE.md`: whether Tier A as drafted stays
clear of being construed as medical advice, and whether the §5 notice is
sufficient.*
