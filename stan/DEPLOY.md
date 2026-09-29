# Getting STAN live

What it takes to move from a private preview link to a public site that can be
found, shared, and eventually booked against. Written as a runbook, because
almost none of it is engineering and the parts that are are already done.

---

## The problem this solved

Every destination on the hub used to be a hash fragment: `#/m/shbg`. A browser
handles that fine. A search engine sees **one page**.

That matters more than it sounds. `COMMERCIAL.md §4` ranks search first among
acquisition channels: 68 catalogued questions, each one something people type
into Google and get nothing useful back for. That is the whole top of the
funnel, and it was architecturally impossible. The pages could not be indexed,
could not be linked to individually, and could not be shared — send someone a
link to one answer and they landed on the homepage.

So the build now has two modes:

| Mode | Output | For |
|---|---|---|
| `artifact` | one self-contained file, hash routes | the preview link, the PDF |
| `site` | real paths, prerendered to one HTML file each | the public site |

```bash
python3 stan/tools/build.py                  # artifact — the preview
python3 stan/tools/build.py --mode site      # site shell into dist/
python3 stan/tools/prerender.py              # one real HTML file per destination
```

The prerenderer drives the page's own JavaScript in a real browser and writes
out the DOM it produced, rather than reimplementing the rendering in Python.
One renderer, so the static pages and the live app cannot drift apart.

It also writes `sitemap.xml` and `robots.txt`, and each page gets its own
`<title>`, description, canonical link and Open Graph tags.

## What is still needed, in order

### 1. A domain — an evening, about £12/year

Nothing else can happen first. `.org.uk` or `.org`. Register anywhere
reputable; Cloudflare Registrar sells at cost and keeps everything in one
place.

Then set it in `data/site.yaml`:

```yaml
origin: "https://stan.org.uk"     # whatever it turns out to be, no trailing slash
origin_confirmed: true
```

Until that flag is true, both the build and the prerenderer warn, because
canonical links, Open Graph URLs and the sitemap are all wrong without it and
all three are the things search depends on.

### 2. Hosting — an hour, £0

**Cloudflare Pages.** Free for what STAN needs, global CDN, free TLS, free
custom domain, and no request limits on static files. Connect the repo, set
the build command, done.

```
Build command:      python3 stan/tools/build.py --mode site && python3 stan/tools/prerender.py
Build output:       stan/dist
```

Netlify and GitHub Pages both work too. The reason to prefer Cloudflare is
step 4: the email capture wants a small serverless function, and having it on
the same platform as the site is one less account and one less thing to
explain to whoever maintains this next.

### 3. An email address — an evening, £0 to £60/year

`hello@` and `founder@` at the new domain, which the outreach to clinicians
needs before it goes anywhere. A message from a Gmail address asking a
consultant endocrinologist to take referrals does not read as an organisation.

- **Cloudflare Email Routing** — free, forwards to an existing inbox. Fine to
  start, but you can only *send* from it with extra setup.
- **Google Workspace** — about £60/year for one user, sends and receives
  properly.

Start with routing. Move when someone replies.

### 4. Email capture — half a day, £0

Every capture on the site currently writes to `localStorage`, which means it
writes to nowhere. Three forms, one mechanism, one storage key, tagged by
stage — that part was built to be swappable, so this is one function to
implement rather than three.

Cheapest honest options:

- **A Cloudflare Worker** writing to KV or D1. Thirty lines, free tier, same
  platform as the site. Recommended.
- **Formspree or Buttondown** free tier. Zero code, but a third party holds
  the addresses, which needs a line in the privacy notice.
- **A plain `mailto:` link.** No infrastructure at all. Ugly, works, and is
  honest about the state of things. Acceptable for week one.

Whatever it is, it needs a privacy notice and a lawful basis before it
collects a single address. That is not optional and it is not hard.

### 5. Booking and payment — an afternoon, £0 plus fees

**Do not build this.** It is the classic place a technical founder loses a
month.

- **Cal.com** free tier for the calendar. Or Calendly.
- **Stripe Payment Link** for the £45. No integration: create a link in the
  dashboard, put it on the page.

Stripe takes roughly 1.5% + 20p on a UK card, so about 88p on £45. Cal.com can
collect the payment at booking if you connect Stripe to it, which makes the
whole wedge product two links and no code.

The service pages are already built to hold this: `data/services.yaml` has a
`status: ready` and an `unlock` field saying "a calendar link and a payment
link. Nothing else." That was literal.

## What year one costs

| | |
|---|---|
| Domain | £12 |
| Hosting (Cloudflare Pages) | £0 |
| Email routing | £0, or £60 for Workspace |
| Cal.com, Stripe | £0 + ~88p per £45 booking |
| **Fixed cost of being live** | **£12 to £72 for the year** |

Worth stating plainly: **the infrastructure is essentially free.** Whatever has
been holding STAN back, it has never been hosting costs and it has never been
code. `STRATEGY.md §6` named the binding constraint as a second human being
involved, and that has not moved.

## The honest note about this document

Everything above is a weekend, and only step 4 involves writing anything.

The engineering that mattered was the routing fix, because shipping the site
without it would have meant doing the marketing twice: once into a site search
engines could not read, and again after somebody noticed. That is now done.

Beyond it, further building is procrastination. The next thing that changes
STAN's odds is not in this repository.
