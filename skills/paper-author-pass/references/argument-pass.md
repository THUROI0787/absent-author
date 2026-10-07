# Pass 2 — Argument and structure

## 2.1 Reverse outline (do this first)
For each section: thesis sentence; then one line per paragraph = its message; then the evidence under it. Every paragraph must map to the thesis; every piece of evidence to a paragraph message. Paragraphs that can be swapped without loss, or that restate a previous paragraph, are cut or merged (S10). Adapted from Master-cai / Peng Sida's notes `[MC]`.

## 2.2 Defensive writing → claim-forward + one Limitations block (S01, S02, S16)
Classify every hedge/caveat sentence:

| Type | Example | Action |
|---|---|---|
| **Scope condition** that actually constrains a claim | "on in-distribution splits", "for models below 1B parameters" | **Keep**, attach to the claim it constrains (in the same sentence if possible) |
| **Material limitation** | small datasets, single compute regime, an assumption | Move into **one** Limitations paragraph with 2–4 specific items; keep the strongest version |
| **Pre-emptive defence** against an imagined reviewer | "We do not claim that…", "This is not to say…", "Our goal is not X but Y" | Rewrite as a positive scope statement ("We study X under Y") or delete |
| **Caveat diffusion** | "should be interpreted with caution", "further research is needed" in many sections | Keep at most once (Limitations/Conclusion) |
| **Limitation self-defence** | "however, this does not affect our main conclusions" | Delete the defence; if the author has an actual argument for why it doesn't matter, state the argument |
| **Stacked hedge** | "may potentially suggest" | One hedge, naming the uncertainty source ("suggests, though only on two datasets") |

Before/after:
- ✗ "We do not claim that our method solves long-context reasoning in general; rather, we aim to provide a first step toward understanding…"
- ✓ "We study long-context retrieval on sequences up to 32k tokens."

## 2.3 Instruction / revision leakage (S03)
Delete sentences that refuse topics nobody raised ("This paper does not consider RL-based approaches"), narrate revisions ("In response to concerns about…", "we have now added…"), or echo a drafting instruction. If an exclusion matters for scope, state the scope positively once.

## 2.4 Lab notebook → argument order (S04)
Results are ordered by the claim they support, not by when they were run. Remove "we first tried…/after several attempts/unfortunately/intermediate errors". A failed alternative stays only if it answers a reader's obvious question ("why not just use X?"), stated in one sentence with its result.

## 2.5 Performative honesty → argumentative use (S05)
For each reported failure/negative result ask: *what does it rule out or bound?*
- If it rules out an explanation or bounds the method's scope → keep, move next to the claim it qualifies, state that function ("This rules out the possibility that the gain comes from longer training").
- If it is relevant but not to the main line → appendix, one-sentence pointer.
- If it informs the main conclusion and is uncomfortable → **it stays in the main text.** Never delete to improve tone.
- Remove the ceremony: "In the spirit of full transparency", "we candidly report", apology adjectives ("unfortunately", "disappointingly").

## 2.6 Term table for coined terms (S06, L13)
List every capitalized coinage, acronym, quoted term, "we call/term/dub this", and internal codename (Regime-B, Set Gamma, run_v3). For each:

| Term | First use (loc) | Defined? (formal/operational) | Distinguishes something no standard term does? | Uses after definition | Decision |
|---|---|---|---|---|---|

Decisions: **keep + define at first use** (if it does real work and appears ≥3 times) · **replace with the field's standard term** · **delete** (acronym for something mentioned twice) · **unify** (one object, one name — the "Banana Rule" in `[ARIS-paper-write]`). Coined terms in the abstract must be essential.

## 2.7 Focus and arc (S07, S08)
- Intro motivation must lead to the actual contribution, not to a minor implementation detail. If the paper is really about the detail, re-motivate at that level.
- Abstract = context → gap → what we did → evidence → strongest number, as prose, not a dump of results.
- Every section should be referenced by the argument; numbers must be identical across sections (cross-check in Pass 3).

**Coherence pass (S08).** The most common complaint from human co-authors about agent-written drafts is that sentences "each say their own thing" and sections do not hand over to one another. Fix it at three levels, in this order:
1. **Section openings.** The first sentence of each section says what the previous sections established and what this section asks. ✗ "We now analyze the training dynamics." ✓ "Sections 4 and 5 showed that SG and InfoNCE share a minimizer and an unbiased estimator; away from the optimum, the two can prefer different representations, which this section examines."
2. **Paragraph endings.** End a paragraph on the result that the next paragraph builds on, so the reader can predict why the next paragraph exists.
3. **Sentence to sentence.** Link sentences through content: start a sentence with what the previous one ended on (given → new), or name the relation (because, so, which means). Connective words alone do not create coherence; a chain of "Moreover / Additionally" is L04, not a fix.

Test: read only the first sentence of every paragraph in a section. If they do not form an argument, the section needs this pass. Do not add new claims to build bridges; if a bridge needs a fact the paper does not have, that is an AQ.

## 2.8 Related work: from roster to comparison (S09)
- Group by the *dimension of difference* that matters for this paper (assumptions, supervision, cost, what is measured), not by "category" headings for their own sake.
- Each group: what they share with us, where we differ, and why the difference matters — once, not "Unlike these works, we…" after every paragraph.
- Check canonical works are present and characterized accurately (no LSTM→Goodfellow 2016).

## 2.9 Orphan formalism and Q&A templates (S12, S13)
- Every definition/theorem must be used by a later argument or experiment; otherwise cut or move to appendix with its use stated.
- Replace "Q1: Does the gain come from…?" headings and "This experiment tests Claim C2" with normal descriptive subsection titles and a topic sentence stating the finding ("Gains persist when training length is matched").

## 2.10 Appendix triage (S15)
Keep: proofs, full hyperparameters, extra results referenced from the main text, failure cases. Remove: duplicate figures, per-seed copies of aggregated plots, unreferenced runs, ablations no claim depends on.

## 2.11 Post-hoc framing (S17)
If losses on standard metrics are described as "a deliberate tradeoff", ask the author for the reason the tradeoff is desirable that existed before the results; if there is none, report the loss plainly and let the reader weigh it.
