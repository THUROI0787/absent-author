# Pass 4 — Sentence-level rules (L layer)

Do this **last**. Fix a trace only if (a) it obscures meaning, or (b) it is reviewer-salient enough to cost credibility. Priority follows our calibration (in the project repository: tools/calibration/calibration_report.md) and reviewer reports.

## Priority order
1. **L08 -ing tails** (AUC 0.96): ", highlighting/demonstrating/underscoring/showcasing/ensuring/paving the way for…"
2. **L03 lexicon clusters** (AUC 0.93; 4o/GPT-5-era words): enhance, crucial, comprehensive, highlight, nuanced, notably, additionally, seamless, pivotal, landscape, interplay, underscore, showcase, leverage; any single such word used ≥6 times.
3. **L10 list-ification / bold inline headers** (AUC 0.91)
4. **L05 distanced reporting & copula avoidance** (AUC 0.87)
5. **L04 sentence-initial transition chains** (AUC 0.81)
6. **L15 flat rhythm** (AUC 0.77; moderate, highest false-positive risk)
7. Reviewer-salient even when weakly discriminative (the catalog's reviewer-salient set is L01, L02, L07, L09, L11, L12, L14, L16): **L01 dash floods**, **L02 "not X but Y"**, **L07 hype**, **L11 number dumps**, **L12 term-list sentences**, **L09 punchy aphorisms**, **L16 chatty register**, **L14 register-mismatch words** ("audit", "load-bearing", "principled", "surgical").

## Rules with before/after (ML-paper register)

**L08 -ing tails** — turn the tail into a separate claim with its evidence, or delete it.
- ✗ "Our method improves accuracy by 2.1 points, highlighting the importance of temporal context."
- ✓ "Our method improves accuracy by 2.1 points. Removing the temporal encoder erases most of this gain (Table 4), so the improvement comes from temporal context."

**L03 lexicon** — replace with the plain word or, better, the specific fact.
- ✗ "This comprehensive analysis underscores the pivotal role of data quality."
- ✓ "Filtering the 12% noisiest samples recovers 80% of the gap (Fig. 3)."
- Plain substitutes: utilize→use, leverage→use, enhance→improve (or say by how much), crucial→(delete or say why), showcase→show, underscore→show, facilitate→enable/allow, comprehensive→(say what was covered).
- Do **not** touch technical senses: robust estimator, statistically significant, comprehensive search (if exhaustive).

**L10 lists & bold headers** — reasoning goes in prose. Keep the contributions list (field convention) and genuinely enumerable items (datasets, hyperparameters).
- ✗ `\textbf{Key insight:} attention heads specialize.`  ✓ "Attention heads specialize: …"

**L05 distanced reporting** — use "we find/show"; restore is/are.
- ✗ "Our findings indicate that the encoder serves as a bottleneck."  ✓ "We find that the encoder is the bottleneck."

**L04 transition chains** — keep only connectives that encode a real relation; prefer thus/therefore/because over Moreover/Additionally/Notably/Furthermore.

**L15 rhythm** — vary sentence length by content: short for the claim, longer for the mechanism. **Never** chop into fragments to look human.

**L01 em dashes** — keep a dash where it does a job (a true parenthetical, an appositive list). Replace dashes that (i) glue two independent clauses, (ii) stage a reveal ("— and the answer is surprising"), (iii) appear more than ~2–3 per page. Use a period, a colon, parentheses, or a subordinate clause. Keep en dashes for ranges (2–4).

**L02 "not X but Y"** — state Y directly unless X is a belief the reader actually holds or the contrast *is* the finding.
- ✗ "The gain is not merely a regularization effect, but a fundamental change in representation."
- ✓ "The gain persists when we match regularization strength (Table 5), so it is not explained by regularization alone." (X kept because the paper tests it.)

**Negation → positive statement** (beyond L02). A bare "not" makes the reader reconstruct the claim. State what holds.
- ✗ "The bound does not depend on the isotropic model."  ✓ "The bound applies beyond the isotropic model."
- Keep the negation when the negative is the finding ("X does not improve Y in any of our settings") or a logical statement ("Assumption 2 does not imply Assumption 3").

**Comma-chained clauses** — when a sentence strings three or more clauses together with commas, or wraps a parenthetical in commas inside another clause, split it. One sentence, one step of the argument. Reviewers describe the effect as "it reads like one long subordinate clause".
- ✗ "The estimator, which is unbiased under (A1), converges, as shown in Theorem 2, at rate O(1/n), which, in practice, is fast."
- ✓ "Under (A1) the estimator is unbiased. Theorem 2 shows it converges at rate O(1/n), which is fast enough for the dataset sizes we use."

**L06 stacked hedges** — one hedge naming its source.  ✗ "may potentially suggest"  ✓ "suggests, on the two datasets we tested,"

**L07 hype** — delete evaluative adjectives the reader can't check (seamless, elegant, remarkable, unprecedented, paradigm shift, unlock). Replace "significant" outside statistics with the number.

**L09 aphorisms / punchy fragments** — end paragraphs on the result or its consequence, not a slogan ("Data is the new architecture.").

**L11 number dumps** — prose interprets 1–2 key numbers; the table holds the rest.

**L12 term-list sentences** — "a robust, scalable, interpretable, and efficient framework" → name the one property you demonstrate, with its evidence.

**L13 synonym cycling** — one object, one name (term table from Pass 2).

**L14 register words** — "audit" for an ordinary analysis → analyze/examine/measure; "load-bearing" → essential/central or say why; "principled" → say which principle.

**L16 chatty register** — "Let's take a closer look", "So, what does this mean?" → declarative topic sentence.

## Keep list (do not "fix")
Procedural passive in Methods · "Figure 2 shows" · the intro roadmap sentence (one) · "thus/therefore" · a necessary single hedge · field-standard acronyms · deliberate parallelism in a contributions list · the author's documented habits from their voice sample.

## Never inject
Typos or grammar errors · staccato fragments · invented anecdotes or "when we first ran this…" stories · forced informal asides · rhetorical questions · fake uncertainty · random synonym swaps of technical terms. These create a new fingerprint and damage clarity.

## Self-check after rewriting a paragraph
1. Did any number, citation, claim strength, or technical term change? (must be no)
2. Does every sentence carry information specific to this paper?
3. Read it aloud — does it sound like *this author* (voice sample) rather than a different template?
4. Would a reader miss the paragraph if deleted? If not, flag it as hollow (don't invent content for it).
