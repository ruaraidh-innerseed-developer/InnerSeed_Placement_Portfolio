---
# STAN hormone explainer template.
#
# Every marker explainer uses these sections, in this order, with these
# headings. Consistency is the point: a reader who has read one should be able
# to navigate any other without relearning the layout, and should be able to
# compare two markers section by section.
#
# Sections may be short. No section may be silently dropped — if one genuinely
# does not apply, write one line saying so and why.

id: <marker-slug>
title: <Marker name — written as the reader would say it, not the lab abbreviation>
content_class: information
status: draft
marker_type: hormone            # hormone | binding-protein | blood-count | organ-marker | metabolic

author:
clinical_reviewer:
reviewed_on:
next_review_due:
version: 0.1
cites: []

reading_age_checked: false
accessibility_checked: false
---

# <Marker name>

> **Red flag block if applicable — see content-page.md. Delete deliberately, not by accident.**

## The short version

<!-- Two or three sentences. Someone who reads only this must not be misled. -->

<!--
  ============================================================================
  QUESTIONS FIRST. This is the part that makes STAN worth reading.

  Nobody arrives wanting "an article about SHBG". They arrive with a question,
  usually holding a result they don't understand:

      "My SHBG is high. What does that mean?"
      "My testosterone is normal but I feel terrible. Is this why?"
      "What number should mine be?"

  So lead with three to five of those, as headings, in the reader's own words.
  Answer each one directly and immediately — no throat-clearing, no working up
  to it. The systematic reference sections below then serve the reader who
  wants to go deeper, rather than standing between them and their answer.

  Write the questions from what people actually search for. Once the hub is
  live, the unmet-search log (INTERIM-STANDARD.md §7) supplies them directly.
  Until then, take them from what you were asking at the time.
  ============================================================================
-->

## "<Question, in the reader's words>"

<!-- Answer in the first sentence. Then explain. -->

## "<Second question>"

## "<Third question>"

---

<!--
  Reference sections below. Keep them — a reader who wants the whole picture
  should find it — but they come after the answers, not before.
-->

## What it is

<!-- One plain sentence first, then detail. No abbreviation used before it is spelled out. -->

## Where it comes from

<!-- Which gland, which cells. Name the organ, because "endogenous production"
     means nothing to someone who left school at sixteen. -->

## What controls it

<!-- What makes it go up and down. This is where the feedback loop gets
     introduced, and where you link to the axis overview. -->

## What it does

<!-- Its actual jobs in the body. Prioritise the ones the reader will care
     about — energy, mood, libido, muscle, fertility, bone — over the ones
     that are physiologically interesting but invisible. -->

## How it shows up on a blood test

<!-- Units used in the UK. Why reference ranges differ between labs. Anything
     about timing of the sample that changes the result. -->

## When it's low

<!-- Causes, then symptoms. Separate the two — readers conflate them. -->

## When it's high

<!-- Same. If high is not clinically meaningful for this marker, say so. -->

## When it's suppressed

<!--
  THE SECTION THAT MAKES THIS DOCUMENT WORTH EXISTING.

  Suppression is not the same as deficiency. Deficiency is the body failing to
  make enough. Suppression is the body being told, correctly, to stop — because
  something is arriving from outside.

  Cover: what suppression does to this marker specifically, why, how fast, and
  what the number typically looks like. Be concrete. This is the section no
  other explainer on the internet has, and the reason someone will read yours.
-->

## What recovery looks like

<!--
  Only where applicable. Be honest about the state of the evidence: for most
  markers the recovery trajectory after prolonged AAS exposure is poorly
  characterised, and saying so is more useful than a reassuring guess.
  Never give a timeline that the cited evidence does not support.
-->

## What this number does not tell you

<!--
  Required, always. The equivalent of claims_not_supported for a reader rather
  than a reviewer. The most common ways this marker gets over-read, stated
  plainly. Example for total testosterone: it does not tell you how much is
  biologically available, and on its own it cannot distinguish a suppressed
  axis from a failing one.
-->

## Questions worth asking about it

<!-- Questions for a clinician. Not answers. Links to the consultation brief. -->

## Related markers

<!--
  A panel is a system, not a list. Name the markers that move with this one and
  say briefly how. This is the cross-linking that turns a set of pages into an
  actual understanding.
-->

---

**Sources for this page:** *(generated from `cites`)*

**Written by** <author> · **Clinically reviewed by** <reviewer, registration>
**Last reviewed** <date> · **Next review due** <date> · **Version** <n>

*General information, not medical advice about you. STAN does not assess,
diagnose or prescribe. See our [scope of practice](../governance/SCOPE.md).*
