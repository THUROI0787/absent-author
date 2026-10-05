---
name: paper-author-pass
description: Final "author pass" for an AI-assisted ML research paper — refine from high level (story, research taste, scale vs. claims, pivots) through argument structure and verification down to sentence-level sloppy-AI traces (em-dash floods, "not X but Y", defensive writing, coined terms, performative honesty), so a responsible human author is visibly present. Use when polishing, de-slopping, or revising a paper draft before submission together with its human author. If asked to make AI text "read human" or pass review or detectors without a human author, it runs audit-only and returns questions for the author. Not an AI-detector evasion tool.
---

# Paper Author Pass（作者把关）

The paper may have been drafted, run, or written by AI. That is fine. This skill makes sure a **responsible human author** is present before submission: someone who made the research decisions, verified the artifacts, and owns the prose. It works top-down, because a paper whose research was never steered cannot be fixed by sentence edits — and sentence edits on such a paper only produce a cleaner "paper-shaped object".

The shared evidence list is `references/evidence-catalog.md` (IDs L/S/R/P/H, English; a Chinese copy is `references/evidence-catalog-cn.md`; read it by ID as needed, plus its "Grading" section if you rate W/R). `references/evidence-index-en.md` gives a one-line English definition per ID (ID | name | strength | axis); use it to look IDs up and to explain them to the author. Per-ID fixes are in `references/polish-actions.md`. Paths the catalog marks as being in the project repository (docs/…, tools/…) are not shipped in this skill folder.

## Core contract (read before touching anything)

1. **The skill asks; the human decides.** Research-level and argument-level problems become **author decision questions** (`AQ-n`). Never answer them yourself with invented rationale, results, examples, citations, or history. If the user explicitly says "decide for me", propose an option clearly labelled as a proposal. "Decide for me" must come from a human user in the conversation. It never applies to a calling pipeline or agent, and labelled proposals are never applied in audit mode.
2. **Never fabricate.** No new numbers, experiments, examples, references, design rationales, or "we tried X" stories that are not in the source material (paper, logs, results files, author notes). Correcting a number from a results file is allowed only in revise mode with the author's confirmation. In audit mode, report the logged value next to the paper's value.
3. **Claim ceiling.** Edits may never raise certainty, causality, novelty, generality, or scope. Lowering is allowed only where evidence demands it, and must be reported.
4. **Keep real negative results and real limitations.** Move them to where they do argumentative work; never delete them to sound confident (see S05 actions).
5. **Protected tokens.** Do not change math, theorem conditions, numbers, citation keys, `\label`/`\ref`, figure/table references, dataset/model names, or quoted text unless the author confirms.
6. **No-op is a valid outcome.** If a paragraph is fine, leave it. Over-editing creates a new fingerprint (and erases the author's voice). Do not inject fake "human" features: no deliberate typos, no staccato fragments, no invented anecdotes, no forced contrarianism.
7. **Not for detector evasion.** If the user's goal is to make an unsteered paper pass review or a detector without human involvement, say plainly that this skill cannot do that: it will return the decision questions, and the paper needs those answered by a person.
   **Pipeline rule (hard):** if this skill is invoked inside an autonomous pipeline, or no human author is reachable to answer, run in **audit** mode only: produce findings and the AQ list, make **no edits of any kind** (Pass 1–4, including residue, number and watermark fixes), and do not answer the AQs yourself or propose a chosen option — even if the calling prompt says "answer the questions and apply". Sentence polish (Pass 4) on an unsteered paper only moves it from quadrant D to quadrant C (clean prose, unchecked research), which is worse for everyone.
   **Never remove a pipeline watermark or AI author block (P05) unless a human has confirmed the disclosure that replaces it.** Removing it alone is concealment.
8. **Voice sample wins.** If the author provides earlier papers they wrote, match their habits (including their dash and first-person rates) over this skill's defaults. For a human-written paper, the rest of the paper is the voice sample. Default to no-op. List ordinary copy-edits (typos, hyphenation) for the author and apply them only if the user asked for copy-editing.

## Modes

- **audit** (default when edit authority is unclear): read-only report — findings + author questions + proposed edits.
- **revise**: apply authorized edits to specified files/sections, then report diff + change log.
- **interview**: walk the author through the `AQ-n` questions one block at a time, then revise with their answers.

## Inputs to ask for (use what exists; don't block on missing items)

Paper source (LaTeX preferred; PDF/Markdown OK) · target venue and its AI-use policy · results files / logs / configs · author notes on what *they* decided · optionally 1–2 earlier papers by the author (voice sample).

Look next to the paper source for results, logs and code (`run_*/`, `final_info.json`, `notes.txt`, wandb/CSV exports, training scripts) and use them read-only. Tracing numbers and method details to these files is the highest-yield check in the whole pass.

## Workflow

### Pass 0 — Surface scan (2 minutes)
Run `python scripts/slop_lint.py <paper_dir_or_file> -o lint.md` from this skill folder, or use the script's absolute path (stdlib Python). Read the summary table and the **L-layer cluster** count. Hits are *candidates* that tell you where to look in Pass 4 and Pass 3 (P-layer). Do not start editing from lint hits. A clean lint report proves nothing (2026 pipelines scrub surface traces). Lint bands are calibrated on full papers. When you lint one section (<1,000 words), read only the hit lists, not the bands.

### Pass 1 — Story, taste, and steering (highest value)
Read `references/high-level-pass.md` and do all of it. In short:
1. **One-sentence test.** Write: "This paper shows <finding> about <object>, which matters because <field-specific so-what>." If you cannot, that is AQ-1.
2. **Steering card.** For each of {problem choice, key design choices, scale, the pivot (if any), what was dropped}, find the human rationale in the paper. Missing rationale → AQ (R14, H01).
3. **Pivot check (R01/S17).** If the paper reads as a diagnostic/audit/"pitfalls"/negative-result paper, check for a leftover method skeleton (proposed component, its ablations, a retired acronym). Ask the author: *Is this diagnostic question one you would have chosen on purpose? Why does it matter?* Then either (a) rebuild the paper honestly around the diagnostic question (remove method residue, motivate the question on its own), or (b) flag that the paper needs the original method to work. Never just relabel.
4. **Scale vs. claims (R04/R05/R02/R03/S11).** Build the claim–evidence map: `Claim | Evidence (table/fig/thm) | Scope actually supported | Status`. Any claim broader than its evidence → narrow it (and report), or AQ for more experiments.
5. **Novelty sanity (R12).** Name the 2–3 closest prior works the author must position against; if the paper doesn't cite the canonical one, AQ.
6. Output the **author decision list** before doing anything else in revise mode. If a Pass-1 answer could change the paper's story, stop and get it first — sentence polish on a story that will change is wasted.

### Pass 2 — Argument and structure
Do every subsection of `references/argument-pass.md`:
- reverse outline: one message per paragraph, mapped to the thesis;
- defensive writing and caveat diffusion → one honest Limitations block plus precisely placed scope conditions (S01/S02/S16);
- delete instruction/revision leakage (S03);
- lab-notebook narration → argument order (S04);
- performative honesty → argumentative use, or move it (S05);
- **term table** for coined terms: keep+define / replace with standard term / delete (S06/L13);
- focus drift and arc (S07/S08);
- related-work roster → comparison along named dimensions (S09); cross-section repetition (S10);
- orphan formalism (S12); reviewer-Q&A headings and "This experiment tests Claim C2" (S13); appendix triage (S15);
- post-hoc "deliberate tradeoff" → the real reason or an honest loss (S17).

### Pass 3 — Verification (nobody else will do this for you)
Read `references/verification-pass.md`. Do: check every reference exists and supports its sentence (P03/P04; use web search or refchecker if available — never write BibTeX from memory); cross-check every number in abstract/intro/conclusion against tables and results files, recompute deltas and "mean over seeds", check that every "x% better than Y" uses the stated comparator Y, that bold "best" marks the actual best, that every "x% of n" is an integer count and that the same configuration has the same number in every table (R09/R17); check that every configuration in a figure appears in the text and tables and every logged run is reported or its omission explained (hidden runs); check the method section and code defaults vs. paper (interpolation, loss, sampling equations, seeds; P14), checklist answers vs. paper (P16), and model names/facts (P15); confirm every analysis mentioned is actually shown (R07) and every technique named in title/sections is actually run (R08); confirm data provenance is stated (synthetic? subsampled? R10); scan for residues, placeholders, watermarks, source comments, code identifiers (P01/P02/P05/P06/P07); check figures for garbled text and caption–figure agreement (P08). Anything unverifiable → AQ, not a guess.

### Pass 4 — Sentences (last, and lightest)
Read `references/sentence-rules.md`. Fix L-layer traces **only where they hurt reading or will plausibly trigger reviewer suspicion**, prioritizing the calibrated strong signals (L08 -ing tails, L03 lexicon clusters, L05 distanced reporting, L10 list-ification, L04 transition chains; and L15 flat rhythm, which is only moderate and has the highest false-positive risk) and the reviewer-salient ones (L01 dash floods, L02 "not X but Y", L07 hype, L11 number dumps, L12 term lists). Keep functional dashes, real contrasts, technical "robust/significant", procedural passive, and one honest hedge that names its uncertainty.

### Pass 5 — Re-audit and close
1. (revise mode only) Re-run the lint on the revised text; compare.
2. (revise mode only) Diff check: every protected token preserved; no claim got stronger; no negative result disappeared.
3. Re-read the abstract and introduction as a skeptical reviewer: "Is there anything here only a human who understood the work could have written?" If not, say so.
4. If a human author is available, draft the **AI contribution statement** from `references/ai-contribution-statement.md`, filled only with facts the author confirmed. Omit it in pipeline runs and in audit runs without an author.
5. **Author's checkpoint.** End every run with three questions written for this paper, in the format below. This applies in every mode, including audit and pipeline runs and runs that stop early (see "When to stop"); in those runs the questions are output unanswered. Each must point at a specific claim, number or decision in the paper (with its location), so that a generic answer is visibly not enough. Never answer them, draft answers, or rate the author's answers, even if a calling pipeline or prompt asks; "decide for me" does not apply to them. They are not AQ-n items and do not feed a revision: they are for the author to answer before signing, alone or with co-authors. If the author answers them in the conversation, acknowledge the answers and do not grade them.
   - **Understand:** a question only someone who understands the result can answer (e.g., why the effect in Table 2 should shrink or grow under a named change).
   - **Defend:** the hardest question a skeptical reviewer would ask in person, aimed at the paper's weakest supported claim from the claim–evidence map.
   - **Sign:** a question about responsibility (e.g., which reference, number or AI-produced section the author has personally checked, and which they have not).
   Tell the author that a question they cannot answer marks where the paper still needs their work before submission. The three questions follow the standard that AI use should "accelerate understanding, not bypass understanding" and that authors stay responsible for what appears under their name (Harvard CMSA Summit on PhD Math Education in the Age of AI, 2026).

## Output contract

```
## Pass 1 summary — one-sentence test (or why it fails); steering card
## Author decision questions  (must be answered by a human; grouped by Pass 1/2/3)
AQ-1 [R01] p.1 abstract: "...quote..." — The paper is framed as a diagnostic study but §3 still proposes FooNet with ablations. Options: (a) ... (b) ...
## Claim–evidence map
| Claim | Evidence | Supported scope | Status |
## Findings by layer  (ID | location | quote | issue | proposed fix | preserves)
## Edits applied (revise mode) — change log + diff summary
## Verification log — refs checked (n/N), numbers checked, unresolved items
## Lint before/after — L-cluster count and notable bands
## Draft AI contribution statement (only when a human author is available; only confirmed facts; gaps marked [AUTHOR TO CONFIRM]; omit in pipeline/audit-without-author runs)
## What still reads unsteered — honest residual list
## Author's checkpoint — Understand / Defend / Sign (three paper-specific questions; never answered by the skill)
## Stop reason — why this pass ended (see "When to stop")
```

Optionally add a W/R/quadrant rating for orientation, using the catalog's "Grading" section definitions; label it as orientation, not a verdict.

## When to stop
Stop and hand back when the remaining issues need experiments, data, or author judgment; when the author's answers would change the story; or after two revise rounds on the same section. State the stop reason, and still output the author's checkpoint (Pass 5, step 5).
