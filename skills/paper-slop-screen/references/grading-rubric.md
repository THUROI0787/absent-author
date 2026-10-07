# Grading procedure

The authoritative definitions of W/R/Q, flags, auditability and quadrants are in `evidence-catalog.md` → "Grading". This file restates them in English for convenience and adds the procedure. If the two ever disagree, the catalog wins — and please report the discrepancy.

## 1. Counting rules
- Use only findings with a location and a verbatim quote.
- **Axis by ID** (mirrors the catalog's "Grading" section): L → W only. W-axis S IDs: S01, S04–S06, S08, S10, S13–S16, S18. R-axis IDs: S02, S03, S12, S17, R01–R10, R12 (only when the borrowed source can be named), R15–R18, R20, R22, P02 (TODO form, ★ only), P06–P09, P14–P18. Q IDs: S07, S09, S11, R04 (non-template), R11–R14, R21, P04. P13 is i/⚑ (supports P10), never R.
- **Reviewer-salient L items**: L01, L02, L07, L09, L11, L12, L14, L16.
- **One finding per family, within one axis** (F1 S01/S02/S16; F2 R07/R08/S12; F3 L11/S10; F4 R01 with S05/S17/L14). Report all instances, count once per axis. In F4, L14 and S05 count on W only and serve as locating cues for R01; they never add to R. In F1, S02 counts on R; S01/S16 count once on W.
- **One ID contributes at most one ★★★** (multiple R09 mismatches = one R09 finding, ★★★ if ≥2 mismatch types; a single mismatch is ★ and goes to Q).
- Junior-pattern IDs (L04–L06, L11, L13, S01, S04, S09) count only if R/P evidence also exists.
- Apply paper-type exemptions first.

## 2. W — writing left AI-led and unpolished
- **W0**: isolated ★ only.
- **W1**: some traces (L-cluster 1–2; a few defensive sentences), author voice present, terms defined.
- **W2**: families co-occur: L-cluster ≥3; or ≥2 reviewer-salient L items + ≥1 of S01/S05/S06; or ≥3 W-axis S findings from different families (e.g., F1, S06, S08).
- **W3**: W2, and F1 defensive/apologetic caveats (S01/S16 on the W axis) in ≥3 sections, or AI-led traces pervasive throughout.

If the language layer is clean (L-cluster ≤1) and W2 rests only on S-layer structure items, write "W2 (structure only)" in the verdict card so readers know the prose itself is not the problem. Empty headings and stub subsections ("See Fig. X." and nothing else) are unfinished artifacts: count them as P02 (TODO form, ★, R axis), not as S08.

S02 and S03 are R-axis items and do not enter W.

## 3. R — research steering / verification absent
- **R0**: no R-axis finding (higher confidence when artifact-backed H evidence exists). State "numbers verified: n checked / n consistent": R0 resting on many recomputed numbers is worth more than R0 resting on not having looked.
- **R1**: 1–2 ★/★★ R-axis findings (note whether H evidence explains them).
- **R2**: one verified ★★★, or ≥3 ★★ from different families.
- **R3**: any of (a) pivot/construct signature (R01, R02, R03 with inflated claims) + any verification failure (R07–R10, R17, P14, P15); (b) ≥2 verified verification failures of different types (a type is an evidence ID: R07, R08, R09, R10, R17, P14, P15, P16 each count once; many contradictions under R09 are one type and only decide whether R09 is ★ or ★★★); (c) ≥3 ★★★ from different families — **and** no artifact-backed H item (H05, H06, H09) that directly answers them.

**H weighting.** Prose-only H items can downgrade one ★★ finding they directly answer; they never cancel ★★★ or ⚑. Artifact-backed H can cancel a finding they directly answer (e.g., a timestamped pre-registration answers R01; released logs showing the analysis was run answer R07 only if the result is then reported). Nothing cancels a verified ⚑.

## 4. Q — ordinary scientific quality
Normal review judgment. Determines the score. Does not enter the absence narrative: a W0/R0 paper with poor Q is just a weak paper.

## 5. Flags ⚑ (separate; each personally verified)
Verified ☠: P01 residue (incl. agent notes printed in the bibliography); P02-meta LLM placeholder/meta-comment; P03 fabricated reference (wrong authors/title, not just year/venue; checked in ≥2 databases); P05 watermark / LLM author line; P15 knowledge-cutoff text / nonexistent model; R16 AI-review score in the paper; R22 nonexistent cited lemma. Separately: P12 prompt injection (⚑ misconduct, not ☠ — evidence of a *present* author acting badly; venue canaries are input hygiene, not P12). Plus P10 policy violation.

## 6. Auditability
A+ runnable code + configs + full logs (incl. failures) + specific AI statement or version history · A code + statement · A0 text only. **If R is uncertain and auditability is A+, recommend checking the logs rather than guessing.** Auditability never cancels a ⚑.

## 7. Quadrants (W×R) and actions
| | R0–R1 | R2–R3 |
|---|---|---|
| **W0–W1** | **A** normal review | **C veneer**: review on substance; list R findings concretely; R3 → AC note recommending logs/code or author Q&A |
| **W2–W3** | **B salvageable**: concrete rewrite list (each coined term → community term; where to merge defensive passages); state "the substantive contribution stands; presentation impedes evaluation"; do not reject on writing alone unless claims can't be verified | **D AI waste**: reject-level score justified only by verifiable R/P defects (no "AI-generated" in the public review); confidential evidence table for the AC as answerable questions; cite the venue policy clause for any ⚑; recommend logs/code/author Q&A; second-person check of ≥1 piece of evidence when D + accusatory ⚑ |

**The B/D boundary is R, not how bad the writing is.**

## 8. Confidence
- **High**: ≥2 ★★★ verified personally, or a verified ☠.
- **Medium**: clear findings partly resting on judgment (R13, S07) or on samples.
- **Low**: mostly ★/★★; PDF-only text with extraction noise; short paper; likely non-native writing.
Always state what would change the grade.

## 9. Must NOT drive the grade
Detector percentages · a single em dash or "delve" · fluent or non-idiomatic English · nationality/affiliation · fashionable topic (R19 is a prior only) · short length · honest disclosure of AI use · presence of disclosed pipeline files.
