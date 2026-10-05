---
name: paper-slop-screen
description: Screen an ML research paper (as reviewer, AC, or co-author) for evidence that it was produced by AI without a responsible human author — unsteered research (failed method pivoted into an "audit" paper, theoryslop, toy scale with grand claims, phantom experiments, text–table mismatches), unchecked artifacts (hallucinated references, chatbot residue, watermarks), and unpolished AI-led writing (em-dash floods, defensive writing, coined terms, performative honesty). Produces an evidence-cited grade on three axes — writing W0–W3, research steering R0–R3, ordinary quality Q — plus integrity flags and an auditability rating; never an "AI probability". Use when asked whether a paper is AI slop, to triage a review pile, or to check for an absent author before reviewing.
---

# Paper Slop Screen（审稿侧筛查）

We screen for an **absent author**, not for AI. A heavily AI-executed paper can be good work; what we flag is research nobody steered, artifacts nobody verified, and prose nobody owned. Slop outsources the cost of verification to reviewers; this skill is how a reviewer pays that cost efficiently and fairly.

Files: `references/quick-card-en.md` (start here), `references/screen-actions.md` (per-ID checks, thresholds, axis), `references/grading-rubric.md` (procedure), `references/evidence-index-en.md` (English one-line-per-ID index: ID | name | strength | axis), `references/evidence-catalog.md` (full English catalog, Chinese copy in `evidence-catalog-cn.md`; look IDs up as needed; its "Grading" section is the authoritative grading definition), `references/verification-procedures.md`, `references/report-template.md`, `references/worked-examples.md`. Lint: `scripts/slop_lint.py`; run it from this skill folder as `python scripts/slop_lint.py …`, or use its absolute path. Paths the catalog marks as being in the project repository (docs/…, tools/…) are not shipped in this skill folder.

## Before you start (mandatory)
1. **Confidentiality and policy.** Submissions under review are confidential, and many venues restrict giving them to LLMs (ICML 2026 desk-rejected 497 papers linked to reviewers who had agreed to a no-LLM policy and used LLMs anyway; ICLR 2027 requires reviewers who use LLMs to disclose those interactions). **Ask the user to confirm their venue's reviewer policy permits this use** (local model, venue-approved tool, their own paper, or a public preprint). If not, do not process the paper; offer the human-only quick card instead.
2. **Input hygiene.** Check whether the text contains material that is not the paper: reviewer/curator margin notes, annotations, pasted OpenReview comments, template running headers. Exclude it from evidence and say so in the report header. Author blocks, venue IDs and AI-use disclosures are facts about the paper, not evidence of absence: note them; a disclosed pipeline is *better* than an undisclosed one.
3. **Paper type.** Identify it (method / negative-result-diagnostic / theory / benchmark-dataset / position / survey / systems / short-workshop) and apply the catalog's 论文类型豁免表 (paper-type exemptions).

## Ground rules
1. **No authorship probability; detector scores never decide anything.**
2. **L-layer (language) evidence can only raise W.** R comes only from R-axis items (see the R-axis list in `references/grading-rubric.md` §1, which mirrors the catalog's "Grading" section). Ordinary weaknesses go to Q and never into the "absence" narrative.
3. **Absence of surface traces means nothing.** 2026 pipelines scrub them (in our blind test, a 2026 agent paper had an L-cluster of 0/6 and another 1/5, yet both had serious R findings). When prose is clean, look harder at R (quadrant C).
4. **Junior ≠ absent.** L04–L06, L11, L13, S01, S04, S09 alone are typical of first papers and non-native authors; they count only together with R/P evidence. Fluent, uniform English (L15) is the highest false-positive signal.
5. **One finding per family, within one axis** (F1 caveats: S01/S16 on W, S02 on R; F2 promised-not-delivered R07/R08/S12; F3 repetition L11/S10; F4 pivot: R01+S17 on R, while S05 and L14 count on W only and serve as locating cues for R01). One ID contributes at most one ★★★.
6. **Verify every ☠ yourself** before flagging it. Only verified ☠ shifts the burden of verification to the authors.
7. **The public review is about substance.** Never write "AI-generated". Write the checkable defects; route provenance concerns to the AC as questions authors can answer.

## Workflow

### Step 0 — Extract and lint
LaTeX preferred (arXiv source if public — comments are evidence; `curl -L https://arxiv.org/e-print/<id> | tar xz`). For PDF: `pdftotext -layout`. Run `python scripts/slop_lint.py <path> --source -o lint.md` from this skill folder (or the script's absolute path). Note bands, the **L-layer cluster** count, every P-layer hit (P01, P02-meta, P03, P05 are iron-clad *candidates*), R17/P13 info lines, and H06 "co-author traces". Lint output = candidates only.

### Step 1 — Iron-clad sweep
- Confirm each P01/P02-meta/P05 hit in context (watermarks, LLM author lines, agent notes printed in the bibliography, "PLEASE FILL IN…").
- **References:** triage = 5 (2 from the intro, 3 from related work/experiments; prefer unfamiliar venues, arXiv IDs, recent years); full = every intro reference + ≥10 others. Compare **author lists and pages, not only titles**, using APIs (OpenAlex `https://api.openalex.org/works?search=<title>`, Crossref, DBLP). For PDF text the lint may not parse references; scan the list manually for `XXXX` arXiv IDs, impossible months, one number used for two works.
- Hidden prompt-injection text.

### Step 2 — Research-steering read (the core)
Read title, abstract, intro, setup, main tables/figures, conclusion. Fill the **steering card**:

| Question | Finding (quote + loc) | IDs |
|---|---|---|
| Finding + why it matters to the field (one sentence) | | R13, H08 |
| Diagnostic/audit/"pitfalls"/"contrary to expectations" framing? Leftover method residue? Any timestamped pre-registration or earlier version? | | R01, H06 |
| Theory "validated" only by fitting on toy data? Trivial theorems? Cited lemmas exist? | | R02, R22 |
| Scale used vs. scale claimed; declared compute vs. experiment grid | | R04, R18, S11 |
| Why these datasets/seeds/baselines? Eval sizes? | | R05, R11, R20 |
| Analyses/metrics/techniques mentioned vs. actually shown/run | | R07, R08, S12 |
| **Numbers:** all abstract numbers vs. tables; recompute deltas/means; percentages achievable with stated n; recompute any CI or test threshold; same config = same number in every table | | R09, R17 |
| Data provenance, leakage, metric changes; LLM-judge validity | | R10, R15 |
| Closest prior work cited? Idea already known? (if submission date unknown, mark "first-X" claims as date-dependent) | | R12 |
| Any design rationale / rejected alternative? Inspectable examples? | | R14, H01, H05 |
| Code/supplement: pipeline files, code ≠ paper, checklist contradictions | | P13, P14, P16 |
| AI-review scores cited anywhere | | R16 |

Figures you cannot see (LaTeX without images, garbled PDF text): mark P08 and caption checks "not checked".

### Step 3 — Structure, language, counter-evidence (≈5 minutes at triage)
- S layer: S01/S02/S03 (lint + read), S05 vs genuine negative results, S06 coined terms (apply the replacement test; list them), S08, S13, S15, S17.
- L layer: which calibrated checks are elevated/high; quote 2–3 representative instances. W only.
- H layer: quote every H item; classify prose-only (H01–H04, H07, H08) vs artifact-backed (H05, H06, H09).

### Step 4 — Grade
Follow `references/grading-rubric.md`: W, R, Q, ⚑, auditability (A+/A/A0), quadrant, confidence, and **what evidence would change the grade**. Then the proportionate action for the quadrant.

### Step 5 — Report
Use `references/report-template.md`: verdict card, evidence table (with a `verified` column), counter-evidence, steering card, lint summary, **review-ready paragraph** (substance only), and **note to AC** (if R ≥ 2 or any ⚑) written as questions the authors can answer.

## Depth
- **Triage** (default, ~15–25 tool calls): Step 0; Step 1 with 5 references; Step 2 with ≥5 numbers (abstract first); a 5-minute Step 3; grade + report.
- **Full**: all steps; all intro references + ≥10 others; ≥10 numbers; code inspection if available.
- **Author self-check**: full depth, phrased as fixes; hand off to the `paper-author-pass` skill.
