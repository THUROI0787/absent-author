# 15-minute quick card (reviewer edition; English mirror of the quick card in `evidence-catalog.md`)

For a one-line English definition of every evidence ID, see `evidence-index-en.md`.

**What we look for:** an *absent author*. That means research nobody steered, artifacts nobody verified, and prose nobody owned. We do not look for AI use as such.

## The 8 highest-yield checks (in order; in the first 15 minutes do 1–4, the rest as needed)
| # | Check | How (1–3 min each) | IDs |
|---|---|---|---|
| 1 | References | Pick 5 you don't recognize. Look up **title and author list** on OpenAlex, DBLP or Semantic Scholar. Flag invented author lists, nonexistent papers, and `XXXX` arXiv IDs | P03 P04 |
| 2 | Headline numbers | Find every abstract/intro number in the tables. Recompute "+x%". Check that the same config has the same number in every table and that percentages × n come out as integers | R09 R17 |
| 3 | Promised vs. delivered | List every analysis, metric and technique mentioned, then check whether its result appears | R07 R08 S12 |
| 4 | Pivot | Is the title/abstract "audit / diagnostic / pitfalls / contrary to expectations" while the body is still a method paper (a proposed component, its ablations, an unused acronym)? | R01 |
| 5 | Scale vs. claims | Compare model size, data, seeds and compute with claim wording ("LLMs", "generalizes") | R04 R18 |
| 6 | Any human decision | Look for one "we chose X over Y because…" or one inspectable concrete example | H01 H05 |
| 7 | Supplement / code | Look for pipeline files (`CLAUDE.md`, `review_round_*.json`, `IDEA_REPORT.md`). Check that the code matches the paper | P13 P14 |
| 8 | Coined-term replacement test | Swap the coined term for an existing one. Is anything lost? | S06 |

**Before concluding:** look for counter-evidence (H), apply the paper-type exemptions, and put language findings under "presentation" only.
**Never:** cite detector scores, write "AI-generated" in a public review, or penalize fluent or non-idiomatic English.

## Axes
- **W** writing AI-led and unpolished (language + some structure items)
- **R** steering/verification absent (pipeline fingerprints, pivot/construct signatures and verification failures only)
- **Q** ordinary quality (normal review)
- **⚑** flags, reported separately (e.g., residue, LLM placeholder, fabricated reference, watermark, prompt injection, knowledge-cutoff text, AI-review score in the paper; plus AI-policy violations)
- **Auditability** A+/A/A0

## Quadrants (W × R)
| | R0–R1 | R2–R3 |
|---|---|---|
| **W0–1** | A: normal | C: veneer. Review the substance; ask for logs |
| **W2–3** | B: salvageable. Give a concrete rewrite list; don't reject on writing alone | D: AI waste. Reject on verifiable defects; send evidence to the AC as questions; follow venue policy for ⚑ |

## Iron rules
1. Language evidence never raises R.
2. Every finding has a location and a verbatim quote.
3. Look for H evidence and apply type exemptions before grading.
4. Junior ≠ absent: first-paper and non-native patterns count only together with R/P evidence.
5. Only a personally verified ☠ shifts the burden of proof.
