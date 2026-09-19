# STAN — Crisis Protocol

**Status: DRAFT v0.1.** Not adopted. No support channel opens until §1 is
satisfied and every supporter has been trained on this document.

**STAN operates no crisis service.** It has no out-of-hours cover, no clinical
staff on call, and no ability to intervene. What it has is a duty to route
people correctly and without hesitating, and to not leave anyone waiting on an
inbox nobody is reading.

---

## 1. Before any channel opens

1. Every entry in `stan/services/crisis-services.yaml` confirmed against the
   provider's own website and promoted to `verification.status: verified`.
   Run `python3 stan/tools/validate.py` — it reports how many remain unverified.
2. This protocol adopted and every supporter trained on it, including the founder.
3. A named person on call, and a named deputy. Never one person.
4. The email safeguards in §4 implemented and tested with a real send.
5. Crisis signposting visible on **every page** of the website, not only a
   contact page — someone in trouble does not navigate, they land and scroll.

## 2. Where a disclosure will actually arrive

There is no live chat on the site, which removes the highest-risk channel. What
remains:

| Channel | Timing | The specific danger |
|---|---|---|
| Group session | Live, facilitated | Others present; group safety as well as the individual's |
| One-to-one conversation | Live | Supporter is alone with it |
| **Email / contact form** | **Asynchronous** | **May sit unread for hours. See §4.** |
| Social media replies and comments | Asynchronous, public | Public visibility; may be seen by many before anyone responds |

## 3. Live disclosure — what to do

Someone in a group or a conversation says something that frightens you.

**1. Say out loud that you have heard it.** Do not move past it, do not soften
it, do not change the subject. "I'm really glad you told me. I want to stop and
stay with this for a minute."

**2. Ask directly.** "Are you thinking about ending your life?"

Ask it plainly, in those words. Asking someone directly about suicide does not
put the idea in their head — this is established suicide prevention practice and
it is the single most common thing people get wrong out of fear. The vague
question gets a vague answer, and a vague answer is where people slip through.

**3. Establish whether they are in immediate danger.** Have they done something
already? Have they taken something? Do they have a plan and the means to hand?

- **Immediate danger → 999. Now.** Stay with them, on the line or in the room,
  until help is with them if you possibly can.
- **Not immediate → stay with it, then route.** Samaritans on 116 123, any hour.
  Check the day and time before offering a part-hours service (see §7).

**4. Do not promise confidentiality you cannot keep.** If they ask you to keep
it between you: "I can't promise that, and I won't lie to you. If I think your
life is at risk I will act on it. What I can promise is that I'll tell you what
I'm doing before I do it."

**5. Do not try to fix it.** Do not argue them out of it, do not list reasons to
live, do not offer your own recovery as proof it gets better. Listening is the
intervention. Reassurance is for you, not for them.

**6. Do not become the service.** Your job is to get them to someone who can
hold this properly. "I'm going to stay with you while you call them" is support.
"Message me any time, I'll always answer" is a promise that will break, and the
breaking will land on someone who cannot afford it.

**7. Report it the same day.** To the on-call person, always, whoever you are.
**Nobody holds a crisis alone.** That rule protects the person disclosing and it
protects you.

**8. Get debriefed.** Not optional, not "if I feel I need it". Scheduled.

### In a group

The same, plus: you have a room to look after. If the group has two facilitators
— and it must — one stays with the person, one holds the group. If a disclosure
needs more than a few minutes, take it out of the group rather than letting the
session become a crisis. Close the session properly afterwards; do not let people
leave straight from that into their own evening with nothing said.

## 4. Email — the channel that needs engineering, not just training

A live conversation is frightening but you are present. **An email sent at 2am
saying "I can't do this any more" may sit unread until the following afternoon.**
That gap is the most foreseeable harm in STAN's whole design, and unlike a live
conversation it can be engineered against.

**Required, all of them:**

1. **A STAN address, never a personal one.** The founder's personal inbox cannot
   carry an auto-response, cannot be handed to anyone else, and cannot be covered
   when he is away. Every public contact route goes to a STAN address.

2. **An automatic reply on every inbound message**, carrying the crisis numbers
   and stating plainly that nobody is reading right now. Draft below.

3. **The same information on the contact page, above the form.** The auto-reply
   arrives after they have already written and possibly closed the laptop. The
   warning has to be in front of them *before* they type.

4. **A stated checking schedule, and honour it.** "Checked weekday mornings" that
   is true beats "we aim to respond quickly" that is not.

5. **Crisis emails answered first.** Always, ahead of everything else in the inbox.

6. **Never leave the inbox unattended without cover.** Going away means either a
   deputy has it or the auto-response says so explicitly.

### Draft auto-reply

> **Subject: We've got your message — please read this first**
>
> Thanks for writing to STAN. Your message has arrived and someone will read it.
>
> **Please read this bit before anything else.**
>
> This inbox is checked *[state exactly when — e.g. "on weekday mornings"]*. It
> is **not monitored overnight or at weekends**, and nobody is reading it right
> now.
>
> If you are struggling tonight, please use one of these instead. They are free,
> they are open, and they are better at this than we are:
>
> - **In immediate danger, or you've taken something — call 999.**
> - **Samaritans** — 116 123, any hour of any day. Or email jo@samaritans.org
> - **Prefer to text?** Text SHOUT to 85258, any hour.
> - **In Scotland, evenings and weekends** — Breathing Space, 0800 83 85 87
>
> We'll reply within *[state a real number of working days]*. If things get worse
> before then, please use the numbers above rather than waiting for us.
>
> STAN is not a crisis service and cannot offer urgent help.

*Fill the bracketed parts in with what is actually true, and confirm every number
against §7 before this goes live.*

## 5. Social media

Same auto-response problem, less control. If STAN has public accounts:
respond publicly with the crisis numbers, move to private contact if the person
engages, and never leave a public disclosure without a visible reply — others
are reading it too. Do not open direct messages as a support channel unless
someone is actually monitoring them to a stated schedule.

## 6. Afterwards

- **Log it**, minimally: date, channel, what was disclosed, what was done, who
  was told. Enough for safeguarding and supervision, no more. Everything logged
  is discoverable and this is special category data — see `SUPPORT-MODEL.md` §9.
- **Debrief the supporter**, same week.
- **Review the protocol** after any incident where it did not work cleanly.
- **Follow up with the person** only if that was agreed with them and someone is
  genuinely able to. An unfulfilled "I'll check in on you" is worse than never
  offering.

## 7. The numbers

Authoritative list, with hours and coverage:
[`stan/services/crisis-services.yaml`](../services/crisis-services.yaml)

Two traps worth memorising, because both will otherwise send someone to a closed
line at the worst moment:

- **CALM is not 24 hours.** 5pm to midnight only.
- **Breathing Space is not 24 hours on weekdays.** 6pm–2am Monday to Thursday;
  continuous from Friday 6pm to Monday 6am.

**Samaritans, 116 123, is always open.** When in doubt, or when you cannot
remember the hours of anything else, that is the one to give.

## 8. The founder

This applies to you exactly as it applies to everyone else, and there are two
reasons it will be harder for you to follow.

Your name is on this. People will write to you personally and speak to you
personally, and they will do it precisely because you are not a service — which
is the thing that makes it work and the thing that makes it dangerous.

**Nobody holds a crisis alone includes you.** You report it, you get debriefed,
and you have supervision. A founder who is the only person who never gets
debriefed is the person most likely to be the reason this stops.

And you carry a specific vulnerability that a supporter recruited from outside
does not: these are your own drugs, your own history, and some of these
conversations will land somewhere personal. That is not a weakness in you, it is
the predictable cost of the thing that makes you good at this. Plan for it now,
while it is abstract, because you will not want to plan for it later.

---

*Evidence gap: this document asserts that asking directly about suicide does not
increase risk. That is established suicide prevention practice, but STAN holds no
record for it yet. Add one under the `mental-health` topic — this protocol should
not rest on an unsourced claim, however well accepted.*
