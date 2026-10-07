# Polish actions per evidence ID (writing side)

Keyed to `evidence-catalog.md` (English one-liners per ID: `evidence-index-en.md`). "AQ" = turn into an author decision question; do not resolve by inventing content. Pass = where in the workflow it is handled. In audit mode (including every pipeline run) nothing in the Action column is applied; it is reported. Sentence-level actions draw on `[BH]`, `[AV]`, `[humanizer-zh]` (pattern lists are reading cues, not a word blacklist) and `[DS]` (hollow paragraphs are flagged, never filled with invented content).

| ID | Name | Pass | Action |
|---|---|---|---|
| L01 | Em-dash flood | 4 | Keep functional dashes; replace clause-gluing/reveal dashes with period, colon, parentheses or subordinate clause; target ≤2–3 per page unless the author's voice sample uses more |
| L02 | "Not X but Y" | 4 | State Y directly; keep X only if it is a real reader belief or a tested alternative |
| L03 | AI lexicon cluster | 4 | Replace with plain word or the specific fact; break any word repeated ≥6 times; keep technical senses |
| L04 | Transition chains | 4 | Keep only connectives with real logical relation; prefer thus/therefore/because |
| L05 | Distanced reporting / copula avoidance | 4 | "we find/show"; restore is/are; remove "plays a crucial role in" |
| L06 | Stacked hedges | 4 | One hedge naming the uncertainty source |
| L07 | Hype | 4 | Delete uncheckable evaluatives; replace with numbers or scope |
| L08 | -ing tails | 4 | Split into a separate claim with evidence, or delete |
| L09 | Aphorisms / punchy fragments | 4 | End on the result or its consequence |
| L10 | Bold inline headers / list-ified reasoning | 4 | Reasoning back into prose; keep contributions list and true enumerations |
| L11 | Table numbers dumped into prose | 4 | Interpret 1–2 key numbers; leave the rest to the table |
| L12 | Term-list sentences | 4 | Name the one property demonstrated, with evidence |
| L13 | Synonym cycling | 2→4 | Term table; one object, one name |
| L14 | Register words / model tics | 4 | audit→analyze; load-bearing→essential/why; principled→which principle |
| L15 | Flat rhythm, no voice | 4 | Vary length by content; consult voice sample; never fragment for effect |
| L16 | Chatty register / rhetorical questions | 4 | Declarative topic sentences |
| S01 | Defensive writing | 2 | Classify hedges (scope / limitation / defence / diffusion); defences → positive scope or delete |
| S02 | Caveat diffusion ("confession letter") | 2 | One Limitations block with 2–4 specific items; remove repeated "interpret with caution / further research is needed" |
| S03 | Instruction / revision leakage | 2 | Delete; restate scope positively if needed |
| S04 | Lab-notebook narration | 2 | Reorder by argument; keep a failed alternative only if it answers an obvious reader question |
| S05 | Performative honesty | 2 | State what the failure rules out/bounds and place it there; remove ceremony; **never delete material negative results** |
| S06 | Coined terms / codenames | 2 | Term table: keep+define / replace with standard / delete / unify; AQ if the author must define |
| S07 | Focus drift | 1–2 | Re-motivate at the level of the real contribution, or restructure; AQ if story choice needed |
| S08 | Broken arc / stitched feel | 2 | Rewrite abstract as prose arc; coherence pass (section openings hand over, paragraph endings lead on, sentences linked by content); align numbers and cross-references |
| S09 | Related-work roster | 2 | Group by dimension of difference; one positioning statement; add missing canonical work (AQ to verify) |
| S10 | Cross-section repetition | 2 | Merge; keep only necessary abstract–conclusion echo |
| S11 | Summary overreaches evidence | 1 | Claim–evidence map; narrow verbs/scope; report every narrowing |
| S12 | Orphan formalism | 2 | Use it or cut/move it; AQ if the author intended a use |
| S13 | Reviewer-Q&A / claim-matrix headings | 2 | Descriptive titles; topic sentence states the finding |
| S14 | Pipeline template skeleton | 2 | Only change if it hurts the argument; don't restructure for disguise |
| S15 | Appendix dumping ground | 2 | Keep proofs, full settings, referenced extras, failure cases; cut duplicates and unreferenced runs |
| S16 | Limitation self-defence | 2 | Delete the "does not affect our conclusions" reflex; keep a real argument if the author has one |
| S17 | "Lost? change the contest" | 1 | AQ: pre-existing reason for the tradeoff? If none, report the loss plainly |
| S18 | Templated abstract / backronym title | 2 | Abstract as a prose arc with 1–2 key numbers; drop forced backronyms unless the name is established |
| R01 | Failed method → audit/diagnostic paper | 1 | AQ with options: own the diagnostic question (rebuild intro, remove method residue) / own the loss / don't submit yet |
| R02 | Theoryslop | 1 | AQ: out-of-sample prediction or narrow to "descriptive fit"; check assumptions are tested |
| R03 | Slopterpretability | 1 | AQ: what does the finding change? Narrow claims to what the tools show |
| R04 | Toy scale, grand claims | 1 | Narrow claims to the tested setting; AQ for larger-scale evidence |
| R05 | 3-3-3 recipe | 1 | AQ for the reason behind dataset/seed/baseline choices; add it to the paper |
| R06 | Sweep framed as finding | 1 | Reframe as tuning, or AQ for what is learned beyond the sweep |
| R07 | Phantom experiments | 3 | Show the result or delete the mention; never fabricate |
| R08 | Plan ≠ execution | 3 | Rename to what was actually done; AQ if the planned technique is the claimed contribution |
| R09 | Text–table mismatch, numeric drift | 3 | Trace to results files; recompute deltas and means; check the comparator. Fix a number only in revise mode with the author's confirmation; in audit mode report logged vs. paper value |
| R10 | Undisclosed synthetic/subsampled data, leakage, metric switch | 3 | Disclose provenance; check overlap; explain or revert metric change (AQ) |
| R11 | Missing/weak baselines, single runs | 1 | AQ: add strongest recent baseline / seeds; otherwise narrow claims |
| R12 | False novelty | 1 | AQ with closest prior work; state what is actually new |
| R13 | No taste ("paper-shaped object") | 1 | AQ: who would change what because of this result? If no answer, say so |
| R14 | No design rationale | 1 | AQ for decisions and rejected alternatives; add only confirmed rationale |
| R15 | Unvalidated LLM judge / fake GT | 1–3 | AQ: human agreement check or independent judge; disclose |
| R16 | AI-review scores as evidence | 2 | Remove from paper/appendix |
| R17 | Numeric-forensics anomalies | 3 | Recompute percentages vs. n, check variance reporting, fix bolding; AQ if raw numbers unavailable |
| R18 | Compute inconsistent with claims | 3 | Add a compute statement consistent with the experiments (AQ for real figures) |
| R19 | Pipeline-friendly topic (prior only) | 1 | No action by itself; make sure the so-what (R13) and verification (Pass 3) are airtight |
| R20 | Eval size set by API budget | 1 | Report CIs; AQ for larger evaluation or narrow claims |
| R21 | Qualitative examples don't support claims | 1/3 | Choose representative examples (state selection rule); add failure cases |
| R22 | Hollow math | 1/3 | AQ: is the theorem non-trivial? Verify cited lemmas exist; fix notation drift |
| P01 | Chatbot/tool residue | 3 | Remove; then re-verify the surrounding passage |
| P02 | Placeholders | 3 | Fill from real material or delete; AQ if content missing |
| P03 | Hallucinated references | 3 | Verify all entries; REPLACE/REMOVE; never from memory |
| P04 | Citation misattribution | 3 | Cite primary/most relevant source; fix the claim to match the cited work |
| P05 | Pipeline watermark | 3 | Remove **only together with** a human-confirmed disclosure (AI statement); never remove it in audit or pipeline runs, where removal alone is concealment |
| P06 | LaTeX source residue | 3 | Strip `%` plan comments, `DATA_NEEDED`, `[VERIFY]` before arXiv upload (arxiv-latex-cleaner); bib keys need no change |
| P07 | Code identifiers in prose | 3 | Readable names in text, legends, tables |
| P08 | AI-generated figure traces | 3 | Regenerate from data/scripts; fix garbled text; match diagram to method; dedupe |
| P09 | Author can't defend paper | — | Pre-submission: every author should be able to answer the AQ list unaided |
| P10 | Missing/false AI statement | 3/5 | Draft from `ai-contribution-statement.md` with confirmed facts |
| P11 | Batch production / salami | — | Out of scope for one paper; consider merging thin companion papers (AQ) |
| P12 | Hidden prompt injection | 3 | Remove immediately; this is misconduct |
| P13 | Pipeline files in supplement/repo | 5 | Fine to keep if disclosed; ensure the AI statement covers them; remove secrets/internal notes |
| P14 | Code ≠ paper | 3 | Align defaults, splits, metrics; AQ which is correct |
| P15 | Anachronisms / wrong model facts | 3 | Verify every model version, size, date |
| P16 | Checklist / statement boilerplate | 5 | Answer checklists specifically; make statements match the paper |
| P17 | Cross-submission template similarity | — | If submitting several papers, make sure each has its own motivation and design |
| P18 | Rebuttal anomalies | — | In rebuttals: reconcile any new numbers with the paper; don't promise contradictory changes |
| H01–H09 | Positive evidence | 1, 5 | Ask the author for each; add only if true; these make human steering visible |
