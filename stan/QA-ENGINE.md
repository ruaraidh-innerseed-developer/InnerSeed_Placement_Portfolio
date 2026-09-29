# The Q&A engine — design

**How the search bar works, what the AI is allowed to do, and where the line
sits.** This is the architectural spine of the platform.

---

## 1. The rule everything else follows from

> **The AI writes nothing at the moment a reader asks.**

Answers are authored, sourced and reviewed in advance. When someone types a
question, the AI's job is to work out *which already-approved answer* they need
— not to compose one.

That single constraint is what makes the rest defensible.

## 2. Why not the obvious approach

The standard build for "AI search over documents" is retrieval-augmented
generation: chunk the sources, retrieve relevant passages, hand them to a model,
let it write the reply. It is what most products do and it is wrong here.

**A clinician cannot approve text that does not exist until it is asked for.**
That alone rules it out. STAN's whole proposition is that a qualified person has
signed off what readers see. Runtime generation makes that impossible in
principle, not just in practice.

**Generation across passages invents.** Given two retrieved chunks — "A happens"
and "B happens" — a model will reliably produce "A, and therefore B." That
connective tissue is not in either source. In a field where the evidence is
genuinely thin, the fabricated half is exactly the part a reader will act on.

**It cannot say "nobody knows".** Retrieval always returns *something*, and a
model handed something will use it. The honest answer to many questions here is
that the research has not been done, and a RAG pipeline structurally cannot
produce that answer.

**Provenance lands at the wrong grain.** RAG can tell you which document a reply
drew on. It cannot tell you which sentence supports which clause, which is what
a reviewer needs and what a corrections process requires.

## 3. The two AIs

| | **Build time** | **Query time** |
|---|---|---|
| Role | Author, under supervision | Librarian |
| Speed | Slow. Days, not milliseconds. | Instant |
| Reviewed | Yes, before publication | Nothing to review — it authors nothing |
| Reads sources | Yes | No |
| Writes prose | Yes, as drafts | **Never** |
| Can be wrong how | Proposes a bad claim, caught in review | Shows the wrong answer, or none |

The failure modes are what matter. A build-time mistake is a bad draft that a
human catches. A query-time mistake is showing someone a real, reviewed answer
to a question they did not quite ask — recoverable, visible, and nothing like
inventing clinical content on the fly.

## 4. Build time — how content comes into being

```
  SOURCE (read in full)
      │
      ▼   AI proposes; human verifies every quote
  CLAIMS            one statement · one source · verbatim quote
      │
      ▼   AI drafts; composed ONLY from claims
  ANSWER            addresses one question · lists its claims
      │
      ▼   second reader, then clinical reviewer
  APPROVED ANSWER   enters the servable corpus
```

AI is genuinely useful at three points, and each output is checkable:

1. **Reading a source and proposing claims.** Statement, verbatim quote,
   locator, population. A person verifies the quote against the document — no
   clinical qualification needed, only care.
2. **Proposing questions.** Enumerating what people would ask about a topic
   asserts nothing, so this is safe and it is where the question bank comes from.
3. **Drafting answers from approved claims.** Constrained composition, then
   reviewed.

**The hard rule for drafting:** an answer body may contain no substantive
statement that is not carried by a claim in its own `claims` list. A reviewer
checks the answer against its claims, sentence by sentence. Connective prose is
permitted; new assertions are not.

## 5. Query time — what the search bar actually does

A reader types something messy. *"why am i so tired since i came off"*

```
  1. UNDERSTAND    map the phrasing to intent and topics
  2. MATCH         semantic match against the QUESTION BANK
  3. SERVE         return the approved ANSWER attached to the matched question
  4. SHOW WORKING  provenance visible: claims, sources, review date
  5. SUGGEST       related questions from the graph
  6. ADMIT         no confident match → say so, signpost, log the gap
```

Steps 1, 2 and 6 use AI. Steps 3, 4 and 5 are lookups.

**Nothing in that path generates clinical text.** The most the AI does is choose
a row, and choosing badly shows someone a real answer to a slightly different
question — which they can see, because the question is displayed above the
answer.

### The keyword and autocomplete layer

As the reader types, suggestions appear. Two mechanisms, both bounded:

- **Prefix and variant matching** against questions already in the bank. No AI,
  instant, cannot suggest something unanswerable.
- **Semantic expansion** — AI maps unfamiliar phrasing onto bank questions.
  "test levels rubbish" → "My testosterone is low, what does that mean?"

**Suggestions may only ever surface questions that exist in the bank.** The box
never proposes a question STAN cannot answer, because a suggestion is an implied
promise.

### When nothing matches

This path matters more than the matching one, because it is where trust is won
or lost.

- Say plainly that it is not covered. No approximation, no nearest-neighbour
  fudge.
- Signpost to someone who does know.
- Log the question — anonymously, query string and date only.
- Show tonight's crisis numbers if the phrasing suggests distress.

**The unmet log is the content plan.** Every question a reader could not get
answered is the next thing to write, in their own words, and it is the one
dataset nobody else in this field has.

## 6. The question bank

The bank is separate from the answers, and questions exist before answers do.

```
knowledge/
  questions/     what people ask.       Asserts nothing. Can outnumber answers.
  answers/       what STAN says back.   Composed only of claims.
  claims/        one statement, one source, one quote.
```

A question record carries the canonical phrasing plus **variants** — the ways
people actually type it, including slang, misspellings and gym vernacular. The
variants are what make matching work, and they cost nothing to add.

Questions arrive from four places: proposed by AI from the topic map, harvested
from the unmet-search log, remembered by the founder, and contributed by
clinicians who know what they get asked.

**Coverage becomes an honest public number:** *"312 questions catalogued, 47
answered."* That is the roadmap, the funding case and the recruitment advert in
one line, and it is the opposite of pretending to be complete.

## 7. Answering the credibility question

What a clinician will ask, and what the design answers:

| Their question | The answer |
|---|---|
| "Who wrote this?" | A named person, from claims, reviewed by a named clinician. |
| "Where did this sentence come from?" | Click it. Claim → quote → source → locator. |
| "Could the AI have made this up?" | Not at runtime. It authors nothing when a reader asks. |
| "What if a source turns out to be wrong?" | Retire the claim; every answer that used it is listed. |
| "What happens when you don't know?" | The site says so. There is no fallback to plausible prose. |
| "What am I signing off?" | A finite, reviewable corpus — not a model's future behaviour. |

That last row is the one that wins the argument. Asking a clinician to endorse a
generative system means asking them to vouch for everything it might ever say.
Asking them to review 47 answers is a Tuesday afternoon.

## 8. Build order

1. **Question bank first.** It asserts nothing, needs no sources, and is the
   roadmap for everything else. Startable immediately.
2. **Sources in, claims out.** Blocked on documents reaching `sources-inbox/`.
3. **First answers**, from verified claims, on the highest-frequency questions.
4. **Matching engine.** Until the corpus is large, keyword and variant matching
   is enough — semantic matching is worth adding at perhaps a hundred answers,
   not before.
5. **Unmet logging**, server-side, once there is a server.

Only step 4 needs anything clever. Steps 1 to 3 are the actual work, and they
are mostly reading and writing.

## 9. What this deliberately is not

- **Not a chatbot.** No conversation, no persona, no free-form generation. A
  question goes in, a reviewed answer comes out.
- **Not personalised.** It will not read your bloods and tell you what they
  mean. It answers general questions and gives you better ones to ask.
- **Not exhaustive.** The bank will always hold more questions than answers, and
  the gap is shown rather than hidden.
- **Not fast to build.** This is the slow path on purpose. The fast path is a
  RAG bot that sounds excellent and cannot be defended to a single clinician.
