# Verification procedures

## References (P03/P04) — ~5 minutes for a triage sample
1. Extract the bibliography (from .bib/.bbl, or the PDF references section).
2. Sample: triage = 5 (2 intro, 3 elsewhere; prefer unfamiliar venues, arXiv IDs, recent years); full = **all** intro references + ≥10 others.
3. For each, query an API that returns **author lists and pages**, not just titles: OpenAlex `https://api.openalex.org/works?search=<title>`, Crossref `https://api.crossref.org/works?query.bibliographic=<title>`, DBLP `https://dblp.org/search/publ/api?q=<title>&format=json`; fall back to arXiv / Semantic Scholar / venue site. A real title with invented co-authors or pages is a P03 candidate (blind test example 6 was only caught this way). Record:
   - exists? (title match)
   - authors match? (overlap < 60% = suspicious; fully invented names = fabrication)
   - year/venue plausible?
   - for key claims: does the abstract support the citing sentence?
4. Typical fabrication patterns: plausible title + real-sounding authors that don't exist together; real paper with all authors wrong; "John Doe"/"A. Author"; arXiv IDs with X's or impossible numbers (month > 12); two papers merged.
5. Benign errors to not over-read: Google Scholar BibTeX listing editors as authors; outdated arXiv → published venue; minor title drift; wrong year or venue (P03 requires the error to be in the authors or title). Unindexed workshop papers, non-English venues and technical reports are often "not found" without being fabricated: confirm in ≥2 databases and on the venue's own site before flagging.
6. If `refchecker` is available: `refchecker --paper <arxiv_id_or_pdf>`.

## Numbers (R09)
1. List all numbers in abstract, contributions, conclusion, figure captions.
2. Locate each in a table/figure. Recompute: relative improvement = (new − old)/old; absolute vs. relative points; mean ± std consistency with per-seed tables if given.
3. Check identical quantities across sections (dataset counts, model sizes, number of runs).
4. **Integer feasibility:** for every "x% of n", check that x·n/100 is within rounding of an integer ("12.4% of 207" = 25.7 → impossible). Recompute any reported CI or test threshold (t-critical for the stated df; Fisher z for correlations). Check precision against eval size (4 decimals on 200 items is suspicious).
5. A single mismatch is a normal review comment; ≥2 types of mismatch (e.g., delta arithmetic + prose/table disagreement + caption contradiction) indicate no one verified the final draft.

## Plan vs. execution (R07/R08)
- Make two lists: (a) every analysis, metric, figure type, technique *mentioned* (abstract, intro, method, discussion); (b) every one actually *reported*. Items in (a) not in (b) are phantom.
- Compare title/section headings with what the experiments do.

## Data provenance (R10)
- Is each dataset named with version/split? Any "we generate"/"synthetic" data — how, and is train/test overlap ruled out?
- Was the evaluation metric the field-standard one? If changed, is it explained?
- Is model selection on validation?

## Novelty sanity (R12) — ~3 minutes
- Take the core idea in one phrase; search it plus 2–3 synonyms (Semantic Scholar, Google Scholar), including older work and adjacent fields.
- Check whether the closest hit is cited and compared. If a well-known technique is renamed, note the original name.

## PDF-only input
The lint parses references from PDF text only partially. Scan the list manually: `XXXX` arXiv IDs, impossible months (>12), one reference number used for two different works, missing years. Figures cannot be checked from garbled text: mark P08 "not checked".

## Pivot detection (R01)
- Title/abstract framing words: audit, diagnostic, pitfalls, lessons, revisiting, "contrary to our expectations", "we find that X does not".
- Body residue: a named method/component with its own section, hyperparameters, or ablations; an acronym introduced and then rarely used; discussion defending a claim results no longer make.
- If arXiv history is public, earlier versions with a method framing are strong corroboration.
- Distinguish from a genuine diagnostic paper: the question is motivated on its own terms, prior diagnostic work is cited, and the analysis is designed (not leftover). A timestamped pre-registration or earlier version stating the diagnostic aim is artifact-backed H06 and answers R01.

## Source comments (P06) — if arXiv source is public
`curl -L https://arxiv.org/e-print/<id> | tar xz` (or download "TeX Source"). Run lint with `--source`. Look for literal pipeline strings: Sakana-style per-paragraph plan comments, `DATA_NEEDED`, `[VERIFY]`, pipeline files (P13). Ordinary comments and Semantic-Scholar-style bib keys (`Vaswani2017AttentionIA`, which S2's own export produces) are **not** evidence; co-author notes (`%\MB{…}`, `TODO(alice)`) are H06.
