# Screening actions per evidence ID (review side)

Keyed to `evidence-catalog.md` (its "Grading" section is the authoritative grading definition; the Axis column here mirrors it). "Counts when" = the threshold at which the item enters the report as a finding. Every finding needs **location + verbatim quote**. Strength symbols as in the catalog.

| ID | Name | How to check | Counts when | Axis |
|---|---|---|---|---|
| L01 | Em-dash flood | lint L01 band | band = high (> human p99 ≈ 2.9/1k words) **and** used as clause glue | W |
| L02 | "Not X but Y" | lint L02 + read | ≥3 strawman contrasts in main text (★ only; did not discriminate in calibration) | W |
| L03 | AI lexicon cluster | lint L03 (era breakdown, max repeat) | band ≥ elevated, or one word ≥6× | W |
| L04 | Transition chains | lint L04 | band ≥ elevated | W |
| L05 | Distanced reporting | lint L05 | band ≥ elevated | W |
| L06 | Stacked hedges | lint L06 | any hit (rare in humans) | W |
| L07 | Hype | lint L07 + read abstract/intro | band = high or hype in abstract | W |
| L08 | -ing tails | lint L08 | band ≥ elevated | W |
| L09 | Aphorisms / punchy fragments | read | ≥3 in main text | W |
| L10 | Bold headers / list-ification | lint L10 | band ≥ elevated | W |
| L11 | Number dumps | read results prose | paragraphs restating ≥5 table numbers without interpretation | W |
| L12 | Term-list sentences | read | recurring | W |
| L13 | Synonym cycling | read method section | causes ambiguity about which object is meant | W |
| L14 | Register words | lint L14 | cluster only | W |
| L15 | Flat rhythm | lint L15 (CV) | band = high (low CV) — never alone | W |
| L16 | Chatty register | lint L16 + read | recurring | W |
| S01 | Defensive writing | lint S01 (density rule) + read | ≥4 defence sentences across ≥2 sections outside Limitations/RW; ★★★ if in abstract/contributions | W (a failure it masks is scored under its own R ID) |
| S02 | Caveat diffusion | lint S02 per-section + read | caveat phrases in ≥3 sections, or caveats positioned at each likely objection | R (review-loop sign) |
| S03 | Instruction/revision leakage | lint S03 + read | responds to criticism nobody raised / revision narration in an initial submission (★★★); bare "we do not consider X" is only ★ | R |
| S04 | Lab-notebook narration | lint S04 + read | results ordered chronologically with abandoned attempts in main text | W |
| S05 | Performative honesty | lint S05 + read | failures displayed without stated role in the argument; distinguish from genuine negative results | W (F4 with R01) |
| S06 | Coined terms | lint S06 list + read | ≥1 coinage meeting ≥2 of the 5 catalog criteria (★★); ≥3 criteria or ≥3 such coinages (★★★); note those in the abstract | W |
| S07 | Focus drift | read intro vs. body | motivation and actual contribution at different levels | Q |
| S08 | Broken arc | read abstract/intro; read the first sentence of each paragraph in one section; cross-section numbers | abstract is a log dump, sections contradict, or paragraph openings do not form an argument | W |
| S09 | Related-work roster | read RW; check canonical works | roster only, or key canonical work missing/misrepresented | Q |
| S10 | Repetition | read | substantial restatement across ≥3 sections | W |
| S11 | Overreaching summaries | claim–evidence map for abstract/conclusion | any headline claim broader than its evidence | Q |
| S12 | Orphan formalism | trace each definition/theorem to a use | ≥1 substantial unused formal apparatus | R (F2) |
| S13 | Q&A / claim-matrix headings | read | present with other pipeline signs | W |
| S14 | Template skeleton | compare to pipeline templates (catalog) | exact match only | W |
| S15 | Appendix dump | skim appendix | duplicates / unreferenced runs dominate | W |
| S16 | Limitation self-defence | read limitations | each limitation immediately neutralized | W |
| S17 | Change of contest | compare headline metric to subfield norm; read tradeoff claims | loss on standard metric reframed post hoc | R |
| S18 | Templated abstract | read abstract/title | only in cluster with L07/L08 | W |
| R01 | Pivot to audit/diagnostic | title/abstract framing vs. body skeleton | diagnostic framing **plus** leftover method residue (an unargued diagnostic question without residue goes under R13, Q) | R ★★★ |
| R02 | Theoryslop | look at how theory is "validated" | coefficient fitting on toy data only, assumptions untested | R ★★★ |
| R03 | Slopterpretability | ask "so what" | narrow question, off-the-shelf tools, inflated claims | R |
| R04 | Toy scale, grand claims | compare scale to claim wording | claims about LLMs/generalization from toy/template settings | R if template match, else Q |
| R05 | 3-3-3 recipe | experiment setup | only with R04 template datasets (★) | R |
| R06 | Sweep as finding | results | main "finding" is a hyperparameter sweep | R |
| R07 | Phantom experiments | list analyses mentioned vs. shown | any mentioned-but-absent result | R (F2) |
| R08 | Plan ≠ execution | title/section names vs. experiments | named technique absent | R (F2) |
| R09 | Text–table mismatch | cross-check ≥10 numbers incl. all in abstract; recompute deltas | 1 confirmed mismatch = ★ (normal review comment, Q); ≥2 mismatch types = ★★★ | R |
| R10 | Data provenance / leakage / metric switch | data section, metrics | undisclosed synthetic/subsampled data, likely overlap, unexplained metric change | R |
| R11 | Baselines / variance | tables | missing strongest recent baseline, no variance on close results | Q |
| R12 | False novelty | quick search for nearest prior work | known technique renamed; settled question | Q (R if borrowed source identified) |
| R13 | No taste | reviewer judgment, with a written reason | only together with other R evidence | Q |
| R14 | No design rationale | steering card | no rationale for any key decision | Q |
| R15 | LLM judge / fake GT | eval section | same-family judge, no human agreement | R |
| R16 | AI-review scores cited | search paper/appendix/repo | in the paper itself = ☠ ⚑; in repo/README = ★★★ | R/⚑ |
| R17 | Numeric forensics | lint R17 (info) + check pct×n integrality, zero/identical std, precision vs. eval size, monotone ablations, bolding | ≥1 impossible number (★★); several (★★★) | R |
| R18 | Compute vs. claims | compare declared compute to the experiment grid | clear inconsistency or none stated for a large grid | R |
| R19 | Pipeline-friendly topic | note only | never scored; raises scrutiny of R07–R10 | i |
| R20 | API-budget eval sizes | eval section | fine-grained claims from 50–100 samples without CIs | R |
| R21 | Examples vs. claims | look at qualitative figures | examples contradict or are clearly cherry-picked | Q |
| R22 | Hollow math | read theorems; check cited lemmas | trivial theorem / definition-as-theorem (★★); nonexistent cited lemma (☠) | R/Q |
| P01 | Chatbot residue | lint P01 + PDF search | any confirmed | ⚑ ☠ |
| P02 | Placeholders | lint P02-meta / P02-todo + PDF | P02-meta (LLM meta-comment, PLEASE FILL…) confirmed = ⚑ ☠; P02-todo (TODO, (?), ??) = ★ only | ⚑ / R |
| P03 | Hallucinated refs | verify all intro refs + ≥10 random others | any confirmed nonexistent or fabricated author list | ⚑ ☠ |
| P04 | Misattribution | open cited abstracts for key claims | ≥2 instances | Q |
| P05 | Pipeline watermark | lint P05 + PDF | any | ⚑ ☠ |
| P06 | Source residue | arXiv source if public; lint --source | literal pipeline strings only (DATA_NEEDED, [VERIFY], Sakana-style per-paragraph plan blocks) = ★★★; ordinary comments and S2-style bib keys do NOT count; co-author notes are H06 | R |
| P07 | Code identifiers | lint P07 + figures | run IDs / snake_case in prose or legends | R |
| P08 | AI-figure traces | inspect figures | garbled text (★★★), diagram–method mismatch, duplicates | R |
| P09 | Author can't defend | rebuttal / discussion phase | generic, non-responsive rebuttal | R |
| P10 | AI statement | check statement vs. evidence | missing where required, or contradicted | ⚑ (policy) |
| P11 | Batch production | usually not visible to reviewers; AC level | — | i (AC note) |
| P12 | Prompt injection | search for hidden text (select-all in PDF) | any | ⚑ misconduct (strength "⚑ 不端", not ☠: evidence of a present author acting badly) |
| P13 | Pipeline files | inspect supplement / anonymous repo; lint P13 (info) | present and undisclosed → supports P10 | i/⚑ |
| P14 | Code ≠ paper | compare paper hyperparameters/splits/metrics with code defaults | clear mismatch on something the claims depend on | R ★★★ |
| P15 | Anachronisms | check model versions/facts | nonexistent model / knowledge-cutoff text (☠); wrong baseline facts (★★) | ⚑/R |
| P16 | Checklist boilerplate | compare checklist answers to the paper | contradiction (★★★); generic boilerplate (★★) | R |
| P17 | Cross-submission similarity | AC/PC only | shared skeleton/configs/coinage style across a batch | R (AC) |
| P18 | Rebuttal anomalies | discussion phase | new numbers contradict paper; contradictory promises; answering unasked questions | R |
| H01–H09 | Human presence | actively search; quote | prose-only H (H01–H04, H07, H08) can downgrade one ★★ finding it directly answers; artifact H (H05, H06, H09) can cancel a finding it directly answers; nothing cancels a verified ⚑ | counter-evidence |
