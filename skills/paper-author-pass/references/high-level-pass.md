# Pass 1 — Story, taste, and steering

Goal: make sure a human made (and the paper shows) the decisions that an agent cannot be trusted to make: *which problem is worth solving, what scale supports what claim, and what to do when the plan fails.* Most "AI waste" is decided here, not in the prose.

## 1.1 The one-sentence test
Write, from the paper alone:

> This paper shows **⟨finding⟩** about **⟨object⟩**, using **⟨evidence type⟩**, which matters because **⟨who in the field would change what⟩**.

Failure modes and what they usually mean:
- You can only fill ⟨finding⟩ with a method name ("we propose FooNet") → contribution is a mechanism without a finding; ask what we learned.
- ⟨so-what⟩ is generic ("advances the field", "has broad implications") → R13 risk; AQ: "Who would use this result, and how would their practice change?"
- Two different sentences are equally plausible → the paper has two half-stories (often from an overnight pivot: `[ARIS]` "forced structural pivot"); AQ: pick one.

## 1.2 Steering card
Fill this table from the paper. Each empty "human rationale" cell is an author question.

| Decision | What the paper did | Human rationale stated? (quote) | Evidence ID if missing |
|---|---|---|---|
| Problem / question choice | | | R13, H08 |
| Why this approach over the obvious alternative | | | R14, H01 |
| Datasets / benchmarks chosen | | | R05, R10 |
| Model scale / compute | | | R04 |
| Baselines chosen | | | R11 |
| Metrics chosen (and any change of metric) | | | R10, S17 |
| What happened when something failed | | | R01, S05 |
| What was dropped and why | | | S04, H01 |

Rule: a rationale counts only if it is specific to this paper ("CIFAR-10 because the effect requires label noise we can control exactly" — yes; "a widely used benchmark" — no).

## 1.3 Pivot check (R01, S17)
Symptoms of an unsteered pivot:
- Diagnostic/"audit"/"pitfalls"/"lessons"/"contrary to our expectations" framing in title/abstract, **while** the body still contains a proposed component, its ablation table, a hyperparameter section for it, or an acronym that is introduced and then barely used.
- Headline metric is unusual for the subfield; standard metrics where the method loses are explained as "a deliberate tradeoff" / "different design goal" without a pre-stated reason.
- Discussion keeps defending a claim the results section no longer makes.

What to do (author decides):
- **(a) Own the diagnostic paper.** Ask: "If you had started out to study this diagnostic question, would it be worth a paper? Why?" If yes: rewrite intro around that question with its own motivation and related work; remove method residue (or present the method explicitly as the probe that revealed the finding); make the finding the contribution; delete apology language.
- **(b) Own the loss.** If the method genuinely trades X for Y, state the reason the tradeoff is desirable *before* showing results, and report the standard metric plainly.
- **(c) Don't submit yet.** If neither the diagnostic question nor the tradeoff is valuable, say so. This is a legitimate outcome of an author pass.

Never: relabel a failed method paper as an audit with search-and-replace.

## 1.4 Scale vs. claims (R02–R05, S11)
Build the claim–evidence map for every claim in abstract, intro contributions, and conclusion:

| # | Claim (quote) | Evidence (Tab/Fig/Thm) | Scope supported (data, model size, seeds, conditions) | Status: supported / narrow it / needs evidence |

Heuristics:
- Verb ladder: prove > demonstrate > show > indicate > suggest. Pick the strongest verb the evidence licenses, no stronger `[CB]`.
- "generalizes", "robust", "scalable", "LLMs" need varied conditions / multiple scales; one synthetic task or a ~50M model licenses a claim about *that setting*.
- Causal claims need an isolating ablation.
- Theory ("law", "theorem predicts") validated only by fitting coefficients on toy data → R02; ask for an out-of-sample prediction or narrow the claim to "a descriptive fit".
- Interpretability findings from off-the-shelf tools → R03; ask "what does this finding change?"
- "3 seeds, 3 datasets, 3 baselines" is fine **if** the choice is justified; otherwise add the justification (AQ) or the missing strong baseline (AQ).

## 1.5 Novelty sanity (R12)
- Name the 2–3 closest prior works (search if tools allow). Is the canonical one cited and compared?
- Is the "new" method a known technique under a new name (micro-batching, EMA, temperature scaling, label smoothing...)? If so, say what is actually new.
- Was this question answered long ago in another subfield? (Oppenheim's "known for 35 years" case `[Oppenheim25]`.)

## 1.6 Positive evidence to add (only if true)
Ask the author for, and add if they confirm: the design rationale and the rejected alternative (H01), the scope sentence (H02), one inspectable example / failure case (H05), artifact availability and a specific AI contribution statement (H06), the disagreement with the strongest competing work (H07).

## 1.7 Output of Pass 1
A numbered list of author questions `AQ-n [ID] location: quote — question — options`, plus the claim–evidence map. In revise mode, do not proceed to Pass 2 edits on sections whose story depends on an unanswered AQ.
