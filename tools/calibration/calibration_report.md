# slop_lint.py calibration report

Calibration date: **2026-10-05**. Script: `run_calibration.py` (stdlib only). Raw numbers:
`calibration_results.json` (per-paper features and per-feature statistics) and
`calibration_tables.md` (all tables, including every sub-pattern and per-word lexicon row).
The downloaded corpus is **not** in the project. Only IDs and provenance are stored:
`human_corpus.json` and `ai_set_provenance.json`.

> Read this first: the AI-heavy set is small (n=20), mostly from 2024-2025, and dominated by one
> pipeline (13 of 20 papers are Sakana AI Scientist outputs). The AUCs below describe **this** corpus.
> They are not detector accuracies and should not be quoted as such. Every check in the tool still
> produces candidates for a human reader, never verdicts.

## 1. Corpora

### Human baseline (n = 59 used, of 60 downloaded)

- **Sampling.** I used arXiv listing pages (`arxiv.org/list/<cat>/<YYYY-MM>`) because the export API
  returned HTTP 429 from this network. For each of cs.LG, cs.CL, cs.CV and stat.ML, and for each year
  from 2018 to 2022, I drew a random month and a random listing offset (seeded RNG, `seed=20261005`).
  I kept papers whose **primary** category matched and took the first 3 that had LaTeX source.
  That gives 4 categories x 5 years x 3 papers = 60 papers. Downloads were spaced 3 s apart.
- **Version.** I always fetched **v1** (`/e-print/<id>v1`), so the text predates ChatGPT (Nov 2022) even
  if the paper was revised later.
- **Mix.** The arXiv comments show a broad sample, not a set of famous papers. 19 mention a venue
  (NeurIPS/ICML/AISTATS/CVPR/ACL/journals...), 2 mention a workshop, and 26 have no comment at all.
- **Excluded.** 1805.08395 was dropped because its source only wraps a PDF (2 prose words). Two
  sampled IDs had no LaTeX and were replaced during sampling.

### AI-heavy set (n = 20; 16 LaTeX, 4 PDF-extracted text)

Each paper's provenance and the reason we label it AI-heavy are in `ai_set_provenance.json`. In short:

| group | n | era | how we know | source format |
|---|---:|---|---|---|
| Sakana AI Scientist v1 `example_papers` | 10 | 2024 | released as end-to-end system output | LaTeX |
| Sakana AI Scientist v2, ICLR 2025 workshop experiment | 3 | 2025 | Sakana's disclosed experiment | PDF -> text (reviewer margin notes and line numbers stripped) |
| Intology Zochi: Tempest 2503.10619, CS-ReFT 2503.10617 | 2 | 2025 | Intology: AI did research and writing; humans fixed figures, citations and small issues | LaTeX |
| Agents4Science 2025: 2510.21341, 2510.16194, 2509.04504 | 3 | 2025 | venue requires an AI first author; AI-involvement checklists say mostly or fully AI (2510.16194: hypothesis came from humans) | LaTeX |
| 2609.34292 (Claude Opus 4.7 research agent) | 1 | 2026 | abstract and method section self-declare an autonomous research agent | LaTeX |
| ARIS community paper UAV-CC | 1 | 2026 | ARIS README: full pipeline, Claude Opus 4.6 executor + GPT-5.5 reviewer | PDF -> text |

The Agents4Science checklists and the `% ...` instruction blocks were removed before scoring. The tool
drops everything from a `\section*{...Checklist}` heading onward, as well as acknowledgements,
bibliography, math, tables, algorithms, and figure bodies (captions are kept).

## 2. Method

- **Prose extraction.** I used the tool's own extraction (`slop_lint.analyze`), so calibration and use
  see exactly the same text. Every metric is a count per 1,000 prose words, with three exceptions:
  L15 is the coefficient of variation (CV) of sentence length, P06 is the share of paragraphs directly
  preceded by a natural-language `%` comment, and L10 is list items per 1,000 words (see 4.3).
- **Percentiles.** Human percentiles use linear interpolation. **With n=59, p99 is effectively the
  corpus maximum.**
- **Bands, written into the `CALIBRATION` block of `slop_lint.py`.**
  - `typical`: value <= human p90.
  - `elevated`: human p90 < value <= human p99.
  - `high`: value > human p99.
  - L15 uses the low tail instead: elevated below p10, high below p01.
  - Checks that never fired on the human baseline (p99 = 0) are `high` on any hit. That is intended for
    P01/P02/P05, which are marked as iron-clad evidence when verified.
- **Separation.** AUC is the Mann-Whitney statistic P(AI paper > human paper), with ties counted as
  0.5. It is computed on all 20 AI papers, and separately on the 16 LaTeX ones, because PDF text
  extraction has different artifacts. L15 is compared on LaTeX only, because PDF text breaks sentence
  segmentation.
- **Status labels in the tool.**
  - `strong`: AUC >= 0.8.
  - `moderate`: AUC 0.65-0.8.
  - `weak`: AUC < 0.65.
  - `specific, low recall`: fires on <= 5% of human papers and >= 20% of AI papers.
  - `rare`: fires on < 10% of both sets, so it cannot be measured on this corpus.

## 3. Results: main checks (v0.2 re-run)

| ID | metric | human p50 | p90 | p95 | p99 | AI median | AUC all | AUC LaTeX-only | human >0 | AI >0 | AI > human p99 | status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| L01 | per 1k words | 0.000 | 0.978 | 1.836 | 2.934 | 0.379 | 0.67 | 0.64 | 27% | 55% | 15% | moderate |
| L02 | per 1k words | 0.000 | 0.247 | 0.331 | 0.573 | 0.000 | 0.48 | 0.47 | 29% | 20% | 0% | weak |
| L03 | per 1k words | 0.604 | 1.778 | 2.421 | 5.921 | 5.953 | 0.93 | 0.93 | 85% | 95% | 55% | strong |
| L04 | per 1k words | 0.000 | 0.526 | 0.851 | 0.978 | 0.617 | 0.81 | 0.78 | 46% | 90% | 30% | strong |
| L05 | per 1k words | 0.000 | 0.392 | 0.434 | 0.688 | 0.877 | 0.87 | 0.88 | 42% | 85% | 60% | strong |
| L06 | per 1k words | 0.000 | 0.000 | 0.000 | 0.092 | 0.000 | 0.64 | 0.68 | 2% | 30% | 30% | specific (low recall) |
| L07 | per 1k words | 0.000 | 0.209 | 0.247 | 0.430 | 0.141 | 0.72 | 0.80 | 15% | 55% | 40% | moderate |
| L08 | per 1k words | 0.000 | 0.202 | 0.387 | 0.809 | 1.175 | 0.96 | 0.95 | 14% | 95% | 70% | strong |
| L10 | list items per 1k words | 0.649 | 2.838 | 4.261 | 8.481 | 4.886 | 0.91 | 0.91 | 68% | 100% | 31% | strong |
| L14 | per 1k words | 0.000 | 0.000 | 0.112 | 1.550 | 0.000 | 0.62 | 0.62 | 7% | 30% | 0% | weak |
| L15 | sentence-length CV (low = uniform) | 0.506 | 0.618 | 0.641 | 0.691 | 0.376 | 0.77 | 0.77 | 100% | 100% | 25% | moderate |
| L16 | per 1k words | 0.000 | 0.241 | 0.659 | 1.168 | 0.000 | 0.51 | 0.48 | 25% | 25% | 5% | weak |
| S01 | per 1k words | 0.000 | 0.000 | 0.197 | 0.485 | 0.000 | 0.48 | 0.49 | 8% | 5% | 0% | rare |
| S02 | per 1k words | 0.000 | 0.000 | 0.153 | 0.195 | 0.000 | 0.57 | 0.60 | 7% | 20% | 15% | weak |
| S03 | per 1k words | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.53 | 0.53 | 0% | 5% | 5% | rare |
| S04 | per 1k words | 0.000 | 0.199 | 0.223 | 0.255 | 0.000 | 0.42 | 0.42 | 15% | 0% | 0% | weak |
| S05 | per 1k words | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.50 | 0.50 | 0% | 0% | 0% | rare |
| S06 | per 1k words | 0.646 | 1.762 | 1.920 | 2.650 | 0.403 | 0.40 | 0.45 | 97% | 80% | 0% | weak |
| S13 | per 1k words | 0.000 | 0.000 | 0.249 | 0.650 | 0.000 | 0.54 | 0.56 | 7% | 15% | 5% | weak |
| R01 | per 1k words | 0.000 | 0.000 | 0.024 | 0.574 | 0.000 | 0.57 | 0.53 | 5% | 20% | 5% | weak |
| R05 | per 1k words | 0.000 | 0.000 | 0.000 | 0.064 | 0.000 | 0.54 | 0.56 | 2% | 10% | 10% | weak |
| R16 | per 1k words | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.50 | 0.50 | 0% | 0% | 0% | rare |
| P01 | per 1k words | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.53 | 0.53 | 0% | 5% | 5% | rare |
| P02-meta | per 1k words | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.53 | 0.53 | 0% | 5% | 5% | rare |
| P02-todo | per 1k words | 0.000 | 0.156 | 0.436 | 0.563 | 0.000 | 0.65 | 0.63 | 14% | 40% | 25% | weak |
| P03 | per 1k words | 0.000 | 0.175 | 0.400 | 4.312 | 0.000 | 0.59 | 0.60 | 13% | 30% | 0% | weak |
| P05 | per 1k words | 0.000 | 0.000 | 0.000 | 0.000 | 0.143 | 0.75 | 0.81 | 0% | 50% | 50% | specific (low recall) |
| P06 | comment-preceded paragraph ratio | 0.035 | 0.143 | 0.181 | 0.288 | 0.000 | 0.34 | 0.34 | 63% | 38% | 0% | weak |
| P07 | per 1k words | 0.000 | 0.000 | 0.245 | 3.004 | 0.000 | 0.53 | 0.55 | 8% | 15% | 5% | weak |

### L-layer cluster

This counts how many of the six L-cluster checks (L03, L04, L05, L08, L10, L15; L15 is moderate, the rest strong) are above the human p90
(below p10 for L15). Human values are leave-one-out: each human paper is compared with the other 58.

| flags >= k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| human share | 51% | 17% | 2% | 0% | 0% | 0% |
| AI-heavy share | 95% | 90% | 90% | 80% | 50% | 20% |

The AUC of the count is 0.94. Per paper:

| group | flags |
|---|---|
| Sakana v1 | 4-6 each |
| Sakana v2 | 4-5 |
| Zochi | 4, 4 |
| Agents4Science | 3, 3, 4 |
| **2609.34292 (Claude Opus 4.7 agent, 2026)** | **0** |
| **ARIS UAV-CC (Claude Opus 4.6, 2026)** | **1** |

The tool prints this count at the top of every report.

## 4. Discussion: what discriminates and what does not

The figures quoted in this section are from v0.1. Where the v0.2 re-run changed them materially, the
new values are in the table above and are summarised in section 7.

### 4.1 Signals that separate this corpus

1. **L08, trailing -ing clauses (AUC 0.96).** These are sentences ending in ", highlighting ... /
   demonstrating ... / ensuring ... / offering ...". 95% of AI papers have them, compared with 14% of
   human papers. Per pattern:
   - ", highlighting": 50% of AI papers vs 2% of human papers.
   - ", demonstrating": 55% vs 5%.
2. **L03, AI lexicon cluster (AUC 0.94 in v0.1; 0.93 in v0.2).** Almost all of the signal comes from the 4o-era and
   GPT-5/Claude-era lists:
   - era_4o: AUC 0.87.
   - era_gpt5: AUC 0.93. The main words are enhance, crucial, comprehensive and highlight, each with
     a per-word AUC of about 0.83. "Additionally" has 0.74 and "nuanced" fires in 40% of AI papers vs
     2% of human papers.

   The GPT-4-era words did **not** separate: delve, tapestry, meticulous, realm and intricate were
   essentially absent from both sets (era_gpt4 AUC 0.55). This matches EVIDENCE L03: those words have
   been scrubbed from output since 2024. The repeat count of the single most frequent lexicon word is
   also informative: median 6 for AI vs 2 for human papers, AUC 0.91. That supports the ">= 6 repeats"
   rule in EVIDENCE.
3. **L10 as list-ification (AUC 0.91).** List items per 1k words separate well: every AI paper has
   contribution or summary bullets, compared with 68% of human papers. Bold inline headers
   (AUC 0.53) and `\paragraph` (0.50) did **not** separate, because human ML papers use
   `\textbf{Dataset:}`-style run-in headers just as often.
4. **L05, distanced reporting (AUC 0.87).** The sub-pattern "our findings/results/analysis
   indicate/reveal/demonstrate/suggest" does the work: AUC 0.85, 75% of AI papers vs 12% of human
   papers. "serves as" (0.59) and "plays a key role" (0.53) are ordinary academic English.
5. **L04, sentence-initial transitions (AUC 0.81, after an adjustment).**
   - With all ten words, the AUC was **0.54**.
   - "Moreover" and "Furthermore" are used **more** by the 2018-2022 humans (AUC 0.30 / 0.38).
   - "Additionally" separates (0.80).
   - The tool now reports Moreover/Furthermore but does not count them. This was a post-hoc change on
     the same data, so 0.81 is optimistic (see section 5).
6. **L15, rhythm (AUC 0.78 in v0.1; 0.77 in v0.2).** AI papers have more uniform sentence lengths:
   - Median CV is 0.38 vs 0.51.
   - The SD of sentence length is 7.4 vs 10.3 words, close to the 10.1 vs 12.3 cited in EVIDENCE [AG].
   - AI papers also have more, shorter paragraphs: 17.1 vs 11.7 per 1k words, AUC 0.79.

   This is still the check with the highest false-positive risk: one 2022 human CV paper (2203.04446)
   falls below the human p10.

### 4.2 Moderate or specific signals

- **L01, em dashes (AUC 0.67).** The signal depends on the model generation.
  - Sakana v1 (2024) uses almost none: 8 of 10 papers have zero.
  - The 2025-2026 Claude and Zochi papers are the heaviest users of the whole corpus:
    - ARIS UAV-CC: 6.3 per 1k.
    - 2609.34292: 5.6 per 1k.
    - Tempest: 4.6 per 1k.
    - Human p99 is 2.9 (v0.2 re-run; the v0.1 figure was 3.3).

  Only 2% of human papers contain a literal Unicode em dash, vs 30% of AI papers. Human authors type
  `---` or ` -- `.
- **L07, hype (AUC 0.72; 0.80 on LaTeX).** "remarkable" appears in 50% of AI papers vs 10% of human
  papers. "a significant step toward" appears in 25% vs 2%.
- **P02, placeholders (v0.1 AUC 0.67; split in v0.2).** Undefined `\ref` labels appear in 25% of AI
  sources vs 5% of human ones. In v0.2, `P02-todo` (AUC 0.65, weak) and `P02-meta` (rare: one AI paper,
  no human paper) replace this check.
- **L06, stacked hedges (specific, low recall).** These fire on 30% of AI papers and on 1 of 59 human
  papers. A single hit is unusual for a human paper, but most AI papers have none.
- **Not a check, but worth knowing.** The share of Semantic-Scholar-style bib keys
  (`Vaswani2017AttentionIA`) has AUC 0.76 (56% of AI vs 10% of human papers). It is reported inside P06.

### 4.3 Signals that did not separate on this corpus (marked weak or rare in the tool)

- **L02, negative parallelism (AUC 0.45 in v0.1; 0.48 in v0.2).** "Rather than" was the concern raised in the task:
  - It appears in 31% of human papers (p90 = 0.27 per 1k).
  - It is somewhat more frequent in AI papers (55%, AUC 0.69).
  - Even so, it is ordinary academic English, so it is reported as a weak, uncounted sub-pattern, as
    is "not only ... but also".
  - The remaining L02 patterns ("it's not X, it's Y", "not X but rather Y", "the real X is") were
    near zero in **both** sets.
  - EVIDENCE attributes the "not X but Y" surge to 2025-2026 chat models [Pew26]. The AI set is mostly
    2024-2025 pipelines, so this check is **untested**, not refuted.
- **S01-S05 and S13, defensive / review-loop structure.**
  - Almost no hits in either set.
  - The AI set contains no paper produced by an auto-review loop of the ARIS-PR423 kind, which is
    exactly where EVIDENCE says S02/S03 should appear. Only one ARIS paper is included, and it is PDF
    text.
  - Human papers do use "we emphasize that" and "unfortunately" (S04 fires on 15% of human papers vs
    0% of AI papers).
  - Treat these checks as unvalidated pattern lists. Neither the S01 density rule (>= 4 hedge sentences
    in >= 2 sections outside Limitations/Related Work) nor the S02 rule (caveat formulas in >= 3
    sections) fired on any human or AI paper in the corpus.
- **S06, coined terms (AUC 0.40).** Human papers define *more* acronyms and use "we refer to this as"
  more often (41% vs 5%). Acronyms used <= 2 times after their definition are common in human papers:
  median 0.49 per 1k, often funding agencies, metrics, or terms used only in tables. The S06 list is
  useful as a reading aid, not as a score.
- **P06, plan comments (AUC 0.34).** Human sources keep many comments: commented-out drafts, notes,
  section dividers. Sakana's LaTeX has almost none. The "% paragraph plan" artifact described in
  EVIDENCE P06 for ARIS-style pipelines is not present in this AI set, so the ratio cannot be validated.
  `DATA_NEEDED` and `[VERIFY]` never occurred in either set.
- **P03, bibliography anomalies (AUC 0.59).**
  - Duplicate keys and titles occur in human .bib files too: one human paper has 25 duplicate keys.
  - A "Doe" author, "et al." inside an author field, and arXiv IDs with X never occurred in the AI set.
  - Note that this AI set is mostly *published showcase* papers, which tends to remove the most
    obvious hallucinations.
- **P07, code identifiers (AUC 0.55).** This fires on human papers that describe APIs, SQL or code in
  `\texttt`, and on Sakana papers that name `shakespeare_char`.
- **L14, L16, R01, R05.** Low frequency in both sets.
- **Rare checks: P01, R16, S03, S05 and P02-meta.** Zero or near-zero hits in both sets. (P05 left this
  group in v0.2; see section 7.) Their bands therefore mean "any hit
  is above everything in the human baseline". For P01 and P05 that is correct: a confirmed hit is
  iron-clad evidence.

### 4.4 The most important finding for the project

The two 2026 Claude-based pipeline papers (2609.34292 and ARIS UAV-CC) score **0 and 1** on the L-layer
cluster, and below the human median on L03. Their only clear L-layer surface trace is heavy em-dash
use. This is the C-class problem from EVIDENCE: clean surface text over research that may not have
been guided by a person. It confirms the project's position:

- L-layer absence means nothing.
- R-layer and P-layer evidence has to be read by a person in context.

The bands mostly reflect 2024-2025 pipeline style and will age quickly.

## 5. Limitations

- **Small, pipeline-heavy AI set.**
  - n=20, of which 13 are Sakana. Effectively there are about 6 independent "pipelines". AUCs are
    dominated by Sakana's 2024 GPT-4o style.
  - Confidence intervals are wide. With 20 vs 59 papers, an AUC of 0.8 has a rough 95% interval of
    about +/-0.1.
- **Post-hoc tuning on the same data.**
  - The L04 word subset (Moreover/Furthermore set to weak) was chosen after seeing the data, as were
    the L10 metric switch to list items, the S01 split ("we do not consider/address" set to weak), and
    the P03 rule counting duplicates within one file only.
  - Their AUCs are optimistic.
  - The pre-adjustment AUCs were L04 0.54, L10 (bold headers) 0.53, and S01 0.47.
  - The L-cluster uses leave-one-out human percentiles, but its check list was chosen in-sample.
- **Era confound.** The human set is 2018-2022 and the AI set is 2024-2026. Part of the separation is
  probably general drift in ML writing ("leverage" and "comprehensive" were rising before ChatGPT),
  not AI authorship. A modern (2025-2026) human spot set was not collected; it is the most useful
  next step.
- **Mixed formats.** 4 AI papers come from PDF text. Their extraction drops lists and formatting
  (L10 and P06 are n/a), adds hyphenation and page artifacts, and breaks sentence statistics (L15
  excluded for them). The Sakana v2 PDFs carried reviewer annotations, which were stripped
  heuristically, so a few annotation words may remain.
- **Labels are self-reported.** Labels come from self-declaration or venue rules, and human
  involvement varies: 2510.16194 says its hypothesis came from humans, Zochi had human edits, and the
  arXiv versions may be post-review revisions.
- **Field coverage.** Only cs.LG, cs.CL, cs.CV and stat.ML. Theory-heavy stat.ML papers have little
  prose, and math stripping affects them most.
- **Short texts.** Densities from papers under about 1,500 prose words are unstable. The tool warns,
  and calibration excluded them.
- **No error rates.** None of this estimates a false-positive or false-negative rate for real review
  use. Bands only say where a paper sits relative to the 2018-2022 human sample.

## 6. Reproducing

1. Download the human set listed in `human_corpus.json` (all v1 e-prints) into
   `<scratch>/lint/corpus/human/<id>/`.
2. Fetch the AI set as described in `ai_set_provenance.json`. The PDF-text files were produced with
   `pypdf`, dropping line-number lines and "Comment:" margin blocks.
3. Run:

```
python tools/calibration/run_calibration.py --scratch <scratch> --write-tool
```

`--write-tool` rewrites the block between `# BEGIN CALIBRATION` and `# END CALIBRATION` in
`tools/slop_lint.py`.

## 7. v0.2 changes (2026-10-05, after the blind test of the review skill)

A blind test on 6 papers found false negatives on iron-clad items and some false positives. Changes:

1. **P05.** The watermark search now runs on the joined raw source and tolerates line breaks, `\\[0.5cm]`,
   spacing commands and braces. It found Sakana's `THIS PAPER WAS \\[0.5cm] AUTONOMOUSLY GENERATED
   \\[0.5cm] BY THE AI SCIENTIST`. LLM names in the author block (`\author{GPT-4o \& Claude}`) are now
   flagged too. Comments and `\thanks{}` footnotes are excluded from the author block, because that is
   where honest AI-use disclosures live (2609.34292).
   - Calibration: P05 now fires on **50% of AI papers** (the 10 Sakana v1 sources) and **0% of human
     papers**. Status moves from rare to "specific, low recall" (AUC 0.75).
2. **P02 is split into two checks.**
   - **P02-meta** (iron-clad candidate): "PLEASE FILL IN ... HERE", `[INSERT ...]`, "Conclusions Here",
     lorem ipsum, "as requested", "illustrative data", and a narrow "placeholder" (template sense only).
     It fires on 0 of 59 human papers and 1 of 20 AI papers, so its status is rare.
   - **P02-todo** (weak): TODO/TBD/XXX, `( ?)`/`??` (spaces are now allowed), undefined refs, missing
     cite keys. AUC 0.65; 14% of human papers have one.
   - IEEE running headers (`VOL. XX, NO. XX, XXXX`) and X'd arXiv IDs are excluded from P02-todo; the
     latter are counted in P03.
3. **Reference lists.** `.bbl` text and the references section of PDF text are now scanned for P01/P02
   residue, including agent research notes such as "Verified by HTML fetch", "Verdict:" and
   "kill-question". This hit 2609.34292's `.bbl`; no human `.bbl` was hit.
4. **P03 on PDF text and `.bbl`** (used when there are no `.bib` entries). It now flags X'd arXiv IDs,
   impossible arXiv months, "et al." as the only author, "Doe", and duplicated reference numbers.
   Human nonzero dropped from 23% to 13%, because papers with only a `.bbl` now count as checkable,
   which enlarges the denominator.
5. **P06.**
   - Semantic-Scholar-style bib keys are now info only.
   - Co-author notes (`% JS:`, `TODO(name)`, `\todo`, coloured note macros such as `\MB{}`) are
     reported as "possible human collaboration traces (H06)" and excluded from the plan-comment count.
   - P06 calibration is unchanged (AUC 0.34, weak).
6. **P07.** Tokens typeset as code (`\texttt`, `\verb`, inline code) and catalogue IDs (`DMRG_MLP_001`)
   are skipped. `run_N`, `vN_final` and `config_*` are always counted. Human p90 fell from 0.13 to 0;
   status is still weak.
7. **L03 / L14 overlap.** `load-bearing`, `principled` and `first-class` are now counted in L14 only.
   L03 AUC moved from 0.94 to 0.93, and the AI nonzero share from 100% to 95%.
8. **New patterns in counted checks.**
   - L02 gained colon-form contrasts ("is not X: it is Y"). AUC moved from 0.45 to 0.48; still weak.
   - S03 gained "earlier versions called/described", "published/first draft", "in this revision" and
     "we originally reported". They hit 2609.34292 (agent revision loop) and no human paper. S03 is
     still rare.
   - L05 "serves as" no longer counts technical objects ("serve as input/baseline/target"). L05 p90
     moved from 0.43 to 0.39; AUC unchanged at 0.87.
9. **Inline math** now appears as `[MATH]` in snippets instead of `x`, so quoted snippets stay faithful.
   It still counts as one word, but the bracket changes sentence segmentation slightly: L15 human p90
   moved from 0.636 to 0.618, and AUC from 0.78 to 0.77.
10. **New report-only checks.** These are never banded and are not part of the L-cluster.
    - **R17, numeric forensics:** GRIM-style "x% of n" consistency, `\pm 0.00` (saturated 0/100 values
      are skipped), and identical std down a table column.
    - **P13, pipeline files** in a directory input: CLAUDE.md, AGENTS.md, `.claude/`, review_round*,
      AUTO_REVIEW*, IDEA_REPORT*, NARRATIVE_REPORT*, and a results.tsv with keep/discard.

The L-layer cluster is essentially unchanged (AUC 0.94; human share >= 3 flags still 2%; AI 90%). The
v0.1 per-paper numbers are not kept; `calibration_results.json` and `calibration_tables.md` hold v0.2.

## 8. v0.2.1 note (2026-10-05)

- The P05 watermark patterns no longer include the string `CycleResearcher` (it was found only in a code
  docstring, never in a paper template; see `docs/SOURCES.md`). It had zero hits in both sets, so no
  calibrated number changes.
- The lint report header now says "n=59" (it still said "n of about 40", a v0.1 leftover).
