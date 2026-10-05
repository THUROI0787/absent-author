# Worked examples (from the v0.1 blind test, 2026-10-05; regraded under v0.2 rules)

Six public documents were screened blind at triage depth by an agent following the v0.1 skill. The grades below apply the current (v0.2) rubric to the same findings; where that changed a grade, the example says so. The labels were revealed afterwards. Papers are anonymized here, in keeping with the project rule of not publicly naming authors. The two self-declared AI Scientist papers are described by system, because their AI authorship was disclosed by their creators. Use these examples to calibrate borderline calls.

| # | What it really was | Screen result | Matched expectation? |
|---|---|---|---|
| 1 | Human ACL 2018 paper (semantic parsing) | W0 / R0 / no flags → **A** | ✓ |
| 2 | Human 2021 security paper by non-native authors | W0 / R1 / no flags → **A** | ✓ (non-native phrasing did **not** raise W) |
| 3 | Sakana AI Scientist v2 workshop paper (disclosed AI) | W2 / R3 / 0 flags → **D** | ✓ |
| 4 | Sakana AI Scientist v1 example paper (disclosed AI) | W2 / R3 / 3 flags → **D** | ✓ |
| 5 | 2026 autonomous-agent paper, agent use disclosed in a footnote | W3 / R3 / 1 flag → **D** | ✓ (hardest call; the v0.1 test graded R2) |
| 6 | 2026 paper produced with a full auto-research pipeline (Claude executor + GPT reviewer) | W1 / R3 / 2 flags → **C** | ✓ (clean prose, unchecked research) |

L-cluster denominators: k/6 for LaTeX input, k/5 for PDF-text input (L15 is excluded because PDF text breaks sentence segmentation). Examples 3 and 6 were PDF text; example 5 was LaTeX.

## Example 3 → D (the canonical unsteered paper)
- **R07, phantom analyses, ×4.** The abstract promises reliability diagrams; the text says "(not shown due to space constraints)", although appendix space was available. Robust-loss and label-smoothing results are claimed and never shown. An SVHN result reads "consistent with previous observations" and comes with no numbers.
- **R08, plan ≠ execution.** The mitigation section's figure compares two architectures instead of the technique the section is named after.
- **P04.** Temperature scaling is credited to the wrong paper.
- **P02-todo (★).** "CIFAR-10 (?), MNIST (?)": unresolved citations survived into the final document. This is ★ only and never a flag.
- **W2.** L-cluster 4/5 and "highlighting the need…" -ing tails. W2 alone would have meant B; **R3 came entirely from R/P evidence.**
- **Lesson.** The "mentioned vs. shown" row of the steering card catches this whole family in one read.

## Example 4 → D (template pipeline)
- **⚑ P05.** The watermark is split across LaTeX line breaks, and the author line names LLMs.
- **⚑ P02-meta.** "PLEASE FILL IN CAPTION HERE".
- **R04 + R05.** The paper uses the pipeline's template 2D datasets and runs a single seed.
- **R09.** The same claim is given three different KL improvements (41.6% / 36.8% / 16.8%). The paper also declares a metric and never reports it.
- **Lesson.** The v0.1 lint missed the split watermark; v0.2 fixed this. **Always grep the raw source yourself for watermarks.**

## Example 5 → D (the hard case)
- **Disclosure.** Agent use was disclosed honestly ("computation performed by an autonomous research agent operating under the author's direction"). This does not count against the paper.
- **Against (R):**
  - R09: the introduction and conclusion still say a check "passed", while the abstract and §6 say it is null (verified).
  - R17: a mis-specified statistical gate, "t ≥ 4.5 ≈ 3σ at df=3"; the correct threshold is t≈9.2 (verified by recomputing).
  - S03: revision leakage in an initial submission ("the published draft described … incorrectly").
  - R01 pivot shape: "the methodology is the central result".
- **Q (not absence):** baselines that are broken on their face (a comparison at perplexity 12,858), with nobody questioning them (R11).
- **Against (W):**
  - F1 defensive caveats (S01) in nearly every section.
  - Internal codenames used as terms (S06).
  - A 650-word abstract that reads as a log dump (S08).
  - L01 em-dash density high (above the human p99), although the L-cluster is 0/6.
- **⚑ P01.** Agent research notes printed in the bibliography ("Verified by HTML fetch… Verdict: …").
- **For (H06, artifact-backed):** a git-timestamped pre-registration *before* the data. This directly answers R01, so the pivot is not purely post hoc. Scope sentences (H02) and a full count of failures (H03) are also present.
- **Grade.**
  - W3 by the W2 route "≥3 W-axis S findings from different families" (F1, S06, S08; plus L01 high), with F1 spread across nearly every section.
  - R3 by route (b): two verified verification failures of different types (R09 stale "passed", R17 mis-specified t-gate). H06 answers only R01, not these.
  - The v0.1 test graded this R2, because the pre-registration answered the pivot. Under the v0.2 rules it is R3. The quadrant is unchanged: **D**.
- **What would change it:** fixing the stale "passed" sentences and the t-threshold removes route (b). The verified S03 leakage alone would still be R2 (one verified ★★★), so the revision narrative also has to go. With R at R1 or below and the writing still W3, the paper would sit in B.
- **Lesson.** Even a 2026 paper with an **L-cluster of 0/6** can reach W3 through W-axis S findings (pervasive caveats, coined codenames, a log-dump abstract). Pre-registration is the kind of H evidence that should actually change a grade: here it answered R01, but it cannot answer verification failures.

## Example 6 → C (the veneer)
- **Prose.** Clean and field-idiomatic: L-cluster 1/5. The only surface trace is em-dash density (6.3 per 1k words, above the human p99).
- **R09, ≥3 types.**
  - The same configuration scores 63.4 in three tables and 57.2 in a fourth.
  - "15th-percentile filter" applied to 2,524 pairs should leave 2,145, not the 2,077 reported.
  - "12.4% of 207 test pairs" is not an integer count.
  - Three different cost ratios are given for one comparison.
- **R10.** The limitations section names a geographic source region that matches neither dataset.
- **R15.** Reference answers (ground-truth labels) were generated by GPT-4o and only 25% were human-verified; a same-family model is then scored against them.
- **⚑ P03.**
  - Reference with "arXiv:2409.XXXXX".
  - Another reference with an invented co-author and wrong pages; the title is real. Only an OpenAlex lookup caught this, which a title search would have missed.
- **Lesson.** This is exactly the case a style detector misses. **The highest-yield check was arithmetic:** whether percentages are integer counts, recomputed filters, and the same configuration across tables.

## Examples 1–2 → A (do not over-flag)
- Example 2 had non-native phrasing, an abstract that mildly overstated a result, single runs, and a small bookkeeping mismatch. All of these are **Q / R1 at most**.
- Its LaTeX source held co-author comments ("%\MB{As I think you mentioned in your e-mail…}"). These are **H06 evidence of human collaboration, not P06 residue.**
- Example 1 had design rationale, released code, an oracle upper bound, and 5/5 references verified.
