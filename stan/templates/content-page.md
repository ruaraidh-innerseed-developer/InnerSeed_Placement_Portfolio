---
# STAN content page template — copy this file to start a new page.
# Every field is required before the page can move past status: draft.

id: <kebab-case-slug>
title: <plain-English title, written as the question a reader would ask>
content_class: information        # information | signposting | lived-experience
status: draft                     # draft | in-review | approved | retired

# Which standard this page publishes under. See governance/INTERIM-STANDARD.md.
#   A — signpost, attributed report, settled definition, question set, or lived
#       experience. No clinician required, but needs a second reader and the
#       visible notice. Nothing that says "should".
#   B — synthesis, interpretation, prognosis, or anything advising. Locked until
#       a clinical lead is appointed.
publishing_tier: B
second_reader:                    # required for Tier A, must not be the author

author: <name>
clinical_reviewer:                # must be filled and registered before approval
reviewed_on:
next_review_due:
version: 0.1

# Every id here must exist in stan/evidence/sources/ AND be at status: approved.
cites: []

reading_age_checked: false        # NHS content style guide
accessibility_checked: false      # WCAG 2.2 AA
---

# <Title as a question the reader is actually asking>

<!--
  RED FLAG BLOCK — mandatory on any page touching acute symptoms.
  Goes here, above everything else. Delete only if genuinely not applicable,
  and record that decision in the review notes.
-->

> **If you have chest pain, breathlessness, fainting, swelling or pain in one
> leg, or thoughts of harming yourself, this page is not what you need right
> now.** Call 999 or go to A&E. For urgent but non-emergency advice call NHS 111.
> For mental health crisis support, Samaritans are on 116 123, free, any time.

## In short

<!-- Three or four sentences. A reader who stops here should not be misled. -->

## What we know

<!--
  Every substantive claim carries an inline citation to a register id, like
  [rasmussen-2016-former-abusers]. Before writing a claim, check it against that
  record's claims_supported list. If the claim is not in that list, either find a
  source that supports it, or move it to "What we don't know".
-->

## What we don't know

<!--
  This section is mandatory and must not be empty on any page in this field.
  It is the section that makes the rest of the page trustworthy.
  Name the gaps plainly: what has not been studied, what is contested, where
  clinical practice runs ahead of the evidence.
-->

## What this means for a conversation with your doctor

<!--
  Questions to ask. Not answers to expect. Link to the relevant consultation
  brief where one exists.
-->

## Where to get help

<!-- Signposting. Verified at the last review date shown below. -->

---

<!-- Auto-generated footer at build time. Kept here so drafts show the shape. -->

**Sources for this page:** *(generated from `cites`)*

**Written by** <author> · **Clinically reviewed by** <reviewer, registration>
**Last reviewed** <date> · **Next review due** <date> · **Version** <n>

*This page is general information, not medical advice about you. STAN does not
assess, diagnose or prescribe. See our [scope of practice](../governance/SCOPE.md).*
