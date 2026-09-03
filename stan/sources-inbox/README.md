# Sources inbox

**Drop source documents here. They are not committed to git.**

This is how STAN gets information it can actually stand behind.

---

## Why this exists

Claude cannot read journal articles from the session environment. Egress is
restricted: PLoS, Endocrine Connections, PubMed Central and most publisher
domains are blocked. Web search works and returns titles, abstracts and
snippets, which is enough to confirm a citation exists and roughly what it
found — but it is **not** enough to fill in what a paper actually says, which
population it studied, or what its limitations were.

That gap is why every record in `evidence/sources/` currently reads
`full_text_read: false`.

The fix is manual and it is yours: get the document, put it here, and it can be
read properly.

## The workflow

1. **You obtain the document.** Publisher site, PubMed Central, an institutional
   login, an author request — however you get it.
2. **Drop it in this folder**, named to match its register id where one exists:
   `rasmussen-2016-former-abusers.pdf`.
3. **Say so in the session.** Claude reads it, fills in what it actually says,
   and updates the register: `full_text_read: true`, corrected claims, real
   limitations, the conflict-of-interest declaration.
4. **The PDF stays out of git.** Only the record produced from it is committed.

## The copyright line

Journal PDFs and guideline documents are copyrighted. Committing them to a
public repository is infringement however they were obtained, so `.gitignore`
keeps them out.

The distinction that matters for the whole project: **facts are not
copyrightable, expression is.** STAN can report that a guideline recommends
calculated free testosterone when SHBG is abnormal. STAN cannot paste the
guideline. That is the same line as Tier A in `INTERIM-STANDARD.md` — report and
attribute, never reproduce — so the legal constraint and the editorial one point
the same way.

Open-access papers under CC-BY (PLoS, Endocrine Connections, BMJ Open and
similar) may be quoted more freely with attribution, but the reporting discipline
applies regardless. Check the licence before quoting at length.

## What to get first

Highest value first. The first five are already in the register as unread.

| Priority | Document | Why |
|---|---|---|
| 1 | **Grant et al. 2023**, *Reproduction & Fertility*, doi:10.1530/RAF-22-0097 | The evidence that no agreed pathway exists. STAN's reason to exist, and the paper the outreach email is built on. Open access. |
| 2 | **Solanki et al. 2023**, *Endocrine Connections*, doi:10.1530/EC-23-0358 | Resolves the withheld recovery-timeline figure. Until it is read, that number stays unpublished. Open access. |
| 3 | **Jayasena et al. 2022**, SfE guidelines, *Clin Endocrinol*, doi:10.1111/cen.14633 | The anchor for anything about SHBG, free testosterone, monitoring. Likely paywalled. |
| 4 | **Rasmussen et al. 2016**, *PLoS ONE*, doi:10.1371/journal.pone.0161208 | The landmark recovery study. Open access, CC-BY. |
| 5 | **Vilar Neto et al. 2021**, *Andrologia*, doi:10.1111/and.14062 | Reversibility of ASIH. Currently in the register with almost no claims, because only the title is known. |
| 6 | A current **UK endocrinology or andrology textbook chapter** on the HPG axis | The backstop for every `what_it_is` / `made_where` / `controlled_by` field across all sixteen markers. One chapter covers most of the encyclopedia's foundations. |
| 7 | **BSSM** guidance on adult testosterone deficiency | Second UK guideline voice alongside SfE. |

Numbers 1 and 2 are the two that change what STAN can publish. Number 6 is the
one that unlocks the fastest coverage sweep.

## Non-PDF sources

Also useful here, and easier to get:

- **NHS website pages** on relevant topics — published under the Open Government
  Licence, so reusable with attribution. A good model for reading level as well
  as a citable source.
- **Lab reference range documents** from UK laboratories, if you can get them —
  useful for understanding how much ranges actually vary, though STAN will still
  never quote one as authoritative.
- **Anything a clinical reviewer sends you.** Put it here.
