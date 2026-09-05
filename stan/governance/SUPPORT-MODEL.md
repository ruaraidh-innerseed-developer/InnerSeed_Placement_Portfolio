# STAN — Support Model

**Status: DRAFT v0.1.** Not adopted. No support channel of any kind opens until
this is signed off, insured, and the prerequisites in §10 are met.

---

## 1. Why this document exists separately

STAN is a **support network**, not a library with a comment section. The gap it
fills is answered by people, not only by pages: conversation, group meetings,
seminars, and eventually consultation.

That makes the governance problem fundamentally harder, and it is worth being
precise about why.

Published content can be reviewed *before* it reaches anyone. A draft sits still
while a clinician checks it. **A conversation cannot be reviewed before it
happens.** It is live, unrepeatable, shaped by whoever is in the room, and by the
time anyone could review it the person has already acted on what they heard.

Every safeguard in `EVIDENCE-POLICY.md` operates in advance. Support needs
safeguards that operate *in the moment* — which means they have to live in the
trained instincts of the people doing the supporting, not in a review queue.

That is achievable. It is a recognised discipline with established practice. But
it has to be built deliberately and it has to be built first.

## 2. The tiers

Every support interaction sits at exactly one tier. Anyone providing support must
know which tier they are operating at, at all times.

| Tier | What it is | Who provides it | May they discuss clinical specifics? |
|---|---|---|---|
| **0 — Self-serve** | Published pages, consultation briefs, recordings | Nobody, live | N/A — governed by the evidence policy |
| **1 — Navigation** | Helping someone find the right service or page | Trained volunteers | **No.** Signposting only. |
| **2 — Peer support** | Listening; sharing lived experience; being alongside | Trained, supervised peer supporters | **No.** Experience, never advice. |
| **3 — Clinical** | Assessment, interpretation, treatment decisions | Registered clinicians only | **Yes.** This is the only tier where clinical advice exists. |

**The escalation rule: tiers escalate upward, never substitute downward.**

A peer supporter who is asked a clinical question does not answer it because they
happen to know the answer. They escalate or signpost. This holds *especially*
when the peer supporter genuinely does know more than the GP the person last saw
— that is the exact situation in which the rule is load-bearing, and the exact
situation in which it will feel wrong to follow.

## 3. The boundary: experience is not advice

This is the whole discipline of peer support, and it needs to be trainable, so
here it is concretely.

| Someone asks | Peer support answer (Tier 2) | Never |
|---|---|---|
| "How do I come off?" | "I can't tell you that, and I'd be doing you harm if I tried — it depends on things only someone who can see your bloods and your history can judge. What I can tell you is what it was like when I did it, and how I found someone who knew what they were doing." | Any protocol, taper, timeline, or drug name presented as a plan |
| "Is 400mg a lot?" | "I'm not able to make that judgement for you. Here's our page on what the research says about dose and duration, and here's how to get that assessed properly." | "That's fine" / "that's way too much" |
| "My bloods say X, what does it mean?" | "I can't interpret those — genuinely, not just for legal reasons; a number without your full picture can mislead badly. Our consultation brief will help you get them read by someone who can." | Any interpretation of any result |
| "My GP won't listen." | "That's really common and it's exhausting. Let's get you the consultation brief and look at whether a referral to andrology or a fertility service makes more sense than going back to the same conversation." | Criticism of the clinician, or "you'll have to go private" |
| "I feel like there's no point any more." | Crisis protocol, §5. Immediately. | Continuing the conversation as normal |

The general shape: **"here's what happened to me" and "here's how to get to someone
who can answer that" are always available. "Here's what you should do" never is.**

## 4. Channels

Each channel needs its own risk assessment before opening. In rough order of
increasing risk:

| Channel | Risk | Notes |
|---|---|---|
| Recorded seminars | Low | Reviewable in advance. Treat as published content. |
| Live seminars with Q&A | Medium | The Q&A is unreviewable. Needs a chair briefed to intercept clinical questions. |
| Moderated group meetings | Medium-high | See §6. |
| Group chat / forum | **High** | See §6. Do not open early. |
| One-to-one peer support | High | Needs trained supporters and supervision. |
| One-to-one with the founder | **High — see §7** | |
| Clinical consultation | Governed by the clinician's own registration and indemnity, not by STAN | STAN's duty is vetting and clear labelling of who is speaking in what capacity |

## 5. Crisis protocol

Depression and suicidality are documented features of anabolic steroid cessation.
**If STAN opens any human channel, STAN will receive disclosures of suicidal
intent.** This is not a possibility to plan for eventually; it is a certainty to
plan for first.

This is now covered in full by [`CRISIS-PROTOCOL.md`](CRISIS-PROTOCOL.md), with
the verified service list in
[`../services/crisis-services.yaml`](../services/crisis-services.yaml) covering
both Scotland and England.

In summary, requirements before any channel opens:

1. A written crisis protocol every supporter has been trained on and can execute
   without improvising.
2. A single, unambiguous escalation route, and a named person on call, plus a
   named deputy.
3. Every crisis service entry confirmed against the provider's own website.
   `validate.py` reports how many remain unverified.
4. The email safeguards in `CRISIS-PROTOCOL.md` §4 implemented and tested.
   Asynchronous channels are the most dangerous ones here, because a message can
   sit unread for hours — that gap is engineered against, not trained against.
5. A rule that **no supporter holds a crisis alone**, the founder included. Every
   crisis contact is reported the same day and debriefed.
6. Recognition that STAN operates no crisis service, cannot offer out-of-hours
   cover, and must state this plainly wherever a channel is advertised.

## 6. Groups and moderation

An unmoderated group in this field becomes a source-sharing and dosing-advice
channel. This is the observed pattern, not a pessimistic guess, and it happens
within weeks.

Non-negotiables before a group opens:

- A published code of conduct, agreed on joining, that explicitly prohibits
  sharing sources, suppliers, dosing protocols, and prescription medicines.
- At least two trained moderators, never one.
- A defined removal process, and willingness to use it early.
- No private messaging between members through STAN infrastructure — STAN cannot
  moderate what it cannot see, and it must not provide the channel for the harm.
- Real-name policy for moderators; pseudonymity permitted for members.
- A review after 90 days with authority to close the group if it is not holding.

Start with **facilitated, scheduled group sessions** rather than an always-on
chat. Sessions have a start, an end, a facilitator, and an agenda. Open chat has
none of those and needs far more moderation capacity than a new organisation has.

## 7. The founder's role

This section is written directly, because it is the part most likely to go wrong
and the part hardest to see from the inside.

"People can speak to me" is the most natural thing to offer and the most
dangerous to build on. Three separate problems, all real:

**It doesn't scale, and the failure is not graceful.** Demand for this will exceed
one person's capacity quickly. The failure mode is not a queue — it is someone in
distress who was promised a person and got silence.

**It makes STAN a single point of failure.** An organisation whose support is one
man's availability cannot be handed to anyone, cannot be funded as a service, and
does not survive that man having a bad month.

**It is a risk to you personally.** You are a person who came through serious harm
from these drugs. Being the standing contact for other people's steroid crises —
including the suicidal ones — is a genuine hazard to your own health, and peer
supporters in every field are supervised for exactly this reason. You would need
supervision too, and the founder is usually the last person to get it.

The good version:

- Your story is STAN's most valuable asset. **Tell it once, properly, at scale** —
  a recorded piece, a seminar, a written account. That reaches thousands without
  costing you anything repeatable.
- Appear in **scheduled, bounded, group formats** rather than open one-to-one.
- Your role is to **design the support model, select and train the supporters, and
  hold the standard** — not to be the service.
- You get supervision as well. Written into the model, not left to willpower.

Your knowledge determines which questions matter. It does not have to be the
thing that answers every one of them.

## 8. Selecting, training and supervising supporters

- **Selection.** Lived experience is necessary and not sufficient. Screen for
  boundary-holding, for stability in their own recovery, and for the ability to
  say "I don't know." Anyone who wants to be a supporter primarily to share what
  they've worked out is the wrong candidate.
- **A minimum distance from their own use** before supporting others. Set a
  figure and hold it.
- **Training** covering: the tier model, the experience/advice boundary,
  crisis protocol, confidentiality and its limits, safeguarding, and self-disclosure
  discipline.
- **Supervision.** Regular, scheduled, with someone competent to provide it. Not
  optional and not informal.
- **DBS checks** where the role involves under-18s or vulnerable adults.
- **Supporter wellbeing.** Vicarious trauma is a real occupational risk. Caseload
  limits, debriefing, and a route to step back without stigma.

## 9. Confidentiality, data and its limits

- Support conversations concern health and drug use: **special category personal
  data** under UK GDPR. Lawful basis, retention period and access controls must be
  defined before any channel opens.
- Decide deliberately what is logged. Enough for safeguarding and supervision;
  no more. Everything logged is discoverable.
- **Confidentiality has limits and they must be stated up front**, not discovered
  later: risk to life, risk to a child or vulnerable adult, and legal compulsion.
- People will disclose criminal activity — possession is one thing, supply is
  another. Policy needed on what STAN does with such a disclosure, written with
  legal advice, before it happens rather than after.
- Insurance: professional indemnity and public liability. A support service
  without cover is exposed, and so is everyone volunteering for it.

## 10. Prerequisites — nothing opens before these exist

1. This document adopted, and reviewed by a lawyer.
2. Safeguarding policy adopted.
3. Crisis protocol written, and every supporter trained on it.
4. Insurance in place.
5. Named clinical lead appointed, and a defined Tier 3 escalation route that
   actually answers.
6. At least two trained supporters — never one.
7. Data protection: lawful basis, retention schedule, and privacy notice published.

**Recommended sequence:** recorded seminars first (lowest risk, reviewable,
demonstrates quality to prospective partners), then facilitated group sessions,
then one-to-one peer support, then anything always-on. Each step only once the
one before it is running well.

---

*Evidence gap to close: STAN holds no records yet on peer support effectiveness,
or on mental health and suicidality in AAS cessation. Both are needed — the first
to design this well, the second because §5 depends on it. See the `peer-support`
and `mental-health` topics in the register.*
