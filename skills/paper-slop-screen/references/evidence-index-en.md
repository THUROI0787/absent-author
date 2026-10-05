<!-- AUTO-SYNCED from docs/evidence-index-en.md by tools/sync_evidence.py. Do not edit here; edit the master in the project repository and re-run the sync. -->

# Evidence index (English, one line per ID)

v0.2.1 · 2026-10-05. A lookup aid for the evidence catalog (`EVIDENCE.md` in English and `EVIDENCE_CN.md` in Chinese at the project root; `references/evidence-catalog.md` and `evidence-catalog-cn.md` inside each skill). The catalog is authoritative: it holds the typical forms, false-positive notes, sources, the paper-type exemptions and the grading rules ("Grading"). If this index and the catalog disagree, the catalog wins; please report the discrepancy. Maintained by hand at `docs/evidence-index-en.md` and copied into both skills by `tools/sync_evidence.py`.

**Strength** (of evidence that no responsible human author was present, not of "AI wrote it"): ☠ iron-clad once personally verified · ★★★ strong · ★★ medium (needs 2–3 from different families) · ★ weak (never decisive alone) · i background only (not scored) · "⚑ misconduct" for P12.
**Axis:** W = writing left AI-led and unpolished · R = research steering / verification absent · Q = ordinary quality (normal review, not "absence") · ⚑ = flag reported separately · i = background.
**Calibration:** "cal ✓" = the lint check separated human from AI papers on our small corpus (AUC ≥ 0.65 or specific); "cal ✗" = tested but did not separate, or too rare to measure. No mark = no lint check.
**Families** (count once per axis): F1 defensive/apologetic caveats S01, S02, S16 · F2 promised but not delivered R07, R08, S12 · F3 repetition L11, S10 · F4 pivot R01 with S05, S17, L14.
**Junior ≠ absent:** L04–L06, L11, L13, S01, S04, S09 count only together with R/P evidence.

## L — language (axis W only; L evidence never raises R)

| ID | Name | Strength | Axis |
|---|---|---|---|
| L01 | Em-dash flood (density above human p99 ≈ 2.9 per 1k words) | ★ · cal ✓ | W |
| L02 | "Not X but Y" negative parallelism with a strawman X | ★ · cal ✗ | W |
| L03 | AI-lexicon cluster (enhance, crucial, comprehensive, highlight, …) | ★ single / ★★ cluster or one word ≥6× · cal ✓ | W |
| L04 | Sentence-initial transition chains (Additionally, Notably, …) | ★ · cal ✓ | W |
| L05 | Distanced reporting and copula avoidance ("Our findings indicate", "serves as") | ★★ · cal ✓ | W |
| L06 | Stacked hedges ("could potentially") | ★★ · cal ✓ (specific, low recall) | W |
| L07 | Marketing hype, self-promotion (seamless, remarkable, paradigm shift) | ★★ · cal ✓ | W |
| L08 | Trailing -ing clauses (", highlighting the importance of …") | ★★ · cal ✓ | W |
| L09 | Aphorisms and punchy dramatic fragments | ★★ | W |
| L10 | Lists instead of reasoning; bold inline headers | ★★ · cal ✓ (list density) | W |
| L11 | Table numbers restated in prose without interpretation (F3) | ★★ | W |
| L12 | Term-list sentences ("a robust, scalable, interpretable … framework") | ★★ | W |
| L13 | Several names for one object, causing ambiguity | ★★ | W |
| L14 | Register-mismatch words / model tics ("audit", "load-bearing", "principled") | ★ · cal ✗ | W |
| L15 | Smooth but voiceless: uniform sentence and paragraph rhythm | ★ · cal ✓ (highest false-positive risk) | W |
| L16 | Chatty register, rhetorical self-questions | ★★ · cal ✗ | W |

Reviewer-salient L items (used in W2): L01, L02, L07, L09, L11, L12, L14, L16.
L-layer cluster: ≥3 of L03, L04, L05, L08, L10, L15 above human p90 (supports W only; never a detector).

## S — structure and argument

| ID | Name | Strength | Axis |
|---|---|---|---|
| S01 | Defensive writing: pre-emptive defences outside Limitations (F1) | ★★ (★★★ if ≥4 sentences in ≥2 sections incl. abstract/contributions) · cal ✗ | W |
| S02 | "Confession letter" caveat diffusion across sections (F1) | ★★ (★★★ with S03) · cal ✗ | R |
| S03 | Responding to criticism nobody raised; revision narrative leaking into an initial submission | ★★★ (weak form ★) · cal ✗ | R |
| S04 | Lab-notebook narration (chronological, abandoned attempts in main text) | ★★ · cal ✗ | W |
| S05 | Performative "honest disclosure" of failures with no argumentative role | ★★ · cal ✗ | W |
| S06 | Coined terms presented as established (replacement test; 5 criteria) | ★★ (★★★ at ≥3 criteria or ≥3 terms) · cal ✗ | W |
| S07 | Focus drift to a minor detail | ★★ | Q |
| S08 | Broken arc, stitched feel (log-dump abstract, sections not referencing each other) | ★★ | W |
| S09 | Related work as a roster, or misrepresented / missing canonical work | ★★ | Q |
| S10 | Cross-section repetition (F3) | ★ | W |
| S11 | Summaries that overreach the evidence | ★★ | Q |
| S12 | Formalism set up and never used (F2) | ★★ | R |
| S13 | Reviewer-Q&A or claim-matrix headings | ★★ · cal ✗ | W |
| S14 | Pipeline template skeleton | ★ (★★ on an exact template match) | W |
| S15 | Appendix as a dumping ground | ★★ | W |
| S16 | Limitation followed by self-defence ("does not affect our conclusions") (F1) | ★ | W |
| S17 | "Lost? Change the contest": loss on standard metric reframed post hoc (F4) | ★★ | R |
| S18 | Templated abstract; forced backronym title | ★ | W |

## R — research and experiments

| ID | Name | Strength | Axis |
|---|---|---|---|
| R01 | Failed method pivoted into an "audit / diagnostic" paper with leftover method skeleton (F4) | ★★★ (with residue) · cal ✗ | R |
| R02 | Theoryslop: new "law", trivial theorems, "validated" by fitting on toy data | ★★★ | R |
| R03 | Slopterpretability: narrow question, off-the-shelf tools, inflated claims | ★★ | R |
| R04 | Toy scale with grand claims | ★★ (★★★ template dataset + grand claim) | R if template match, else Q |
| R05 | "3-3-3" recipe without justification | ★ (only with R04 template data) · cal ✗ | R |
| R06 | Hyperparameter sweep framed as a finding | ★★ | R |
| R07 | Phantom experiments: analyses mentioned but never shown (F2) | ★★★ | R |
| R08 | Plan ≠ execution: named technique absent from experiments (F2) | ★★★ | R |
| R09 | Text–table contradictions, numbers drifting across sections | ★★★ (≥2 types); single mismatch ★ → Q | R |
| R10 | Undisclosed synthetic data / subsampling, leakage, silent metric switch | ★★★ | R |
| R11 | Missing or weak baselines, single runs | ★★ | Q |
| R12 | False novelty (renamed method, settled question, borrowed idea) | ★★ | Q; R when the borrowed source can be named |
| R13 | No research taste ("paper-shaped object") | ★★ (reason required) | Q |
| R14 | No design rationale for any key choice | ★★ | Q |
| R15 | Unvalidated LLM-as-judge / fake ground truth | ★★ (★★★ in benchmark papers without human check) | R |
| R16 | AI-review scores cited as support | ☠ in the paper / ★★★ in repo or README · cal ✗ | R (⚑ when in the paper) |
| R17 | Numeric-forensics anomalies (x% of n not an integer, zero variance, bolding errors) | ★★ (★★★ several) | R |
| R18 | Compute inconsistent with the claimed experiments | ★★ | R |
| R19 | Pipeline-friendly topic (prior only; never scored) | i | i |
| R20 | Evaluation size set by API budget, no CIs | ★ | R |
| R21 | Qualitative examples do not support the claims | ★★ | Q |
| R22 | Hollow math (trivial theorem, definition as theorem, nonexistent cited lemma) | ★★ (nonexistent lemma ☠) | R / Q (⚑ for nonexistent lemma) |

## P — process and artifacts

| ID | Name | Strength | Axis |
|---|---|---|---|
| P01 | Chatbot / tool residue (incl. agent notes printed in the bibliography) | ☠ · cal ✗ (rare) | ⚑ |
| P02 | Placeholders: LLM meta-comment ("PLEASE FILL IN …") ☠; ordinary TODO / "(?)" ★ | ☠ / ★ · cal ✗ | ⚑ (meta) / R (TODO, ★ only) |
| P03 | Hallucinated references (nonexistent paper or fabricated author list) | ☠ · cal ✗ | ⚑ |
| P04 | Citation misattribution, skewed citation distribution | ★★ | Q |
| P05 | Pipeline watermark / LLM in the author block | ☠ · cal ✓ (specific) | ⚑ |
| P06 | Literal pipeline strings in LaTeX source (DATA_NEEDED, [VERIFY], per-paragraph plan blocks) | ★★★ (ordinary comments and S2-style bib keys: not evidence) · cal ✗ | R |
| P07 | Code identifiers in prose or legends (run_v3_final) | ★★ · cal ✗ | R |
| P08 | AI-generated figure traces (garbled text ★★★, diagram–method mismatch, duplicates) | ★★ | R |
| P09 | Authors cannot defend the paper (post-submission) | ★★★ | R |
| P10 | Missing or false AI-use statement | ★★ | ⚑ (policy) |
| P11 | Batch production, salami slicing | ★★ | i (AC/PC level) |
| P12 | Hidden prompt injection (misconduct by a present author) | ⚑ misconduct | ⚑ |
| P13 | Pipeline files in supplement or repo (CLAUDE.md, review_round_*.json) | i (strong support for P10 if undisclosed) | i / ⚑ |
| P14 | Code ≠ paper | ★★★ | R |
| P15 | Anachronisms and factual errors (knowledge-cutoff text ☠; wrong baseline facts ★★) | ☠ / ★★ | ⚑ / R |
| P16 | Checklist and statement boilerplate (contradiction with the paper ★★★) | ★★ | R |
| P17 | Cross-submission template similarity (AC/PC only) | ★★★ | R |
| P18 | Substantive rebuttal anomalies | ★★ (★★★ contradictions) | R |

## H — positive evidence (human presence)

| ID | Name | Type | Effect |
|---|---|---|---|
| H01 | Design decisions with reasons and rejected alternatives | prose | downgrades one ★★ |
| H02 | Scale matches claims; scope stated | prose | downgrades one ★★ |
| H03 | Failures placed where they do argumentative work (also cancels S05) | prose | downgrades one ★★ |
| H04 | Stable, recognizable author voice and field idiom | prose | downgrades one ★★ |
| H05 | Inspectable concrete examples, qualitative samples, failure cases | artifact | can cancel the R finding it answers |
| H06 | Code, configs, full logs, version history, timestamped pre-registration, specific AI statement, co-author notes in source | artifact | can cancel; basis of auditability |
| H07 | Judgement in citations: classic and strongest competing work, with explicit disagreement | prose | downgrades one level |
| H08 | Clear "so what" in the field's own terms | prose | downgrades one level |
| H09 | Authors defend the paper; specific rebuttal | artifact (post-submission) | can cancel |

Prose-only H never cancels ★★★ or ⚑. Nothing cancels a verified ⚑.

## Grading at a glance (full definitions in the catalog's "Grading" section)

- **W2:** L-cluster ≥3; or ≥2 reviewer-salient L items + S01/S05/S06; or ≥3 W-axis S findings from different families. **W3:** W2 plus F1 caveats in ≥3 sections, or AI-led traces everywhere.
- **R-axis IDs:** S02, S03, S12, S17, R01–R10, R12 (named source), R15–R18, R20, R22, P02 (TODO, ★ only), P06–P09, P14–P18.
- **R0:** no R findings. **R1:** 1–2 ★/★★. **R2:** one verified ★★★ or ≥3 ★★ from different families. **R3:** pivot/construct signature + a verification failure; or ≥2 verified failures of different types; or ≥3 ★★★ from different families; and no artifact H answering them.
- **Quadrants:** A = W0–1 × R0–1 (normal review) · B = W2–3 × R0–1 (rewrite list; don't reject on writing alone) · C = W0–1 × R2–3 (veneer; review substance) · D = W2–3 × R2–3 (reject on verifiable defects; evidence to the AC as questions).
