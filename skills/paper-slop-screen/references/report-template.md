# Report template

```markdown
# Slop screen — ⟨paper title / ID⟩
Depth: triage | full · Input: PDF | LaTeX (+source comments) · Policy check: ⟨confirmed by user⟩

## Verdict card
| Axis | Grade | Confidence | Driven by |
|---|---|---|---|
| Writing (W) | W2 | medium | L08/L03/L10 elevated (L-cluster 4/6); S06: 3 undefined coinages; S01: 6 defensive sentences in 3 sections |
| Research steering (R) | R3 | high | R01 (diagnostic framing over leftover FooNet ablations); R07 (ECE discussed, never shown); R09 (abstract +16% vs. Table 2 = 6.7%) |
| Quality (Q) | weak | medium | missing strongest recent baseline (R11); overreaching abstract (S11) |
| Flags ⚑ | 1 | verified | P03: ref [12] does not exist (searched OpenAlex, DBLP, arXiv) |
| Auditability | A0 | | no code, no logs, generic AI statement |
| Paper type / exemptions | method paper | | none applied |
| Quadrant | **D** | | |

What would change this: ⟨e.g., logs showing the diagnostic question was planned; corrected numbers; verified references⟩

## Evidence table
| # | ID | Strength | Axis | Location | Verbatim quote (≤40 words) | Why it matters | Verified? |
|---|---|---|---|---|---|---|---|

## Counter-evidence (H)
| ID | Prose / artifact | Location | Quote | Which finding it addresses |

## Steering card
(the Step-2 table)

## Lint summary
L-cluster k/6 · bands of note · P-layer candidates checked (n confirmed / n false positive)

## Review-ready paragraph (substance only; no provenance claims)
"⟨Concrete weaknesses: e.g., The abstract reports a 16% improvement, but Table 2 shows 73.1→78.0 (6.7%). Section 5 discusses calibration (ECE) but no ECE results are reported. The paper is framed as a diagnostic study, yet Section 3 still presents FooNet and its ablations without explaining their role in the diagnostic question. Terms X, Y, Z are used without definition. Reference [12] could not be found in any database.⟩"

## Note to AC (only if R ≥ 2 or any ⚑)
Evidence summary (IDs + locations), what was verified personally, suggested process step (request code/logs; author Q&A; venue policy on hallucinated references), and caveats (e.g., possible non-native writing; PDF extraction noise).

Questions the authors can answer, grouped by what they test:
- **Understand:** ⟨e.g., "Why does the gain in Table 2 disappear at the largest model size?"⟩
- **Defend:** ⟨e.g., "Section 3 proposes FooNet, but the paper is framed as a diagnostic study. Was the diagnostic question planned before the experiments? Logs or an earlier version would settle this."⟩
- **Sign:** ⟨e.g., "Which parts of the paper were produced by AI tools, and which references and numbers did the authors check themselves?"⟩
```

Style rules for the report: quote, don't paraphrase; one finding per row; fill the Verified? column (yes / candidate / not checkable); count families once; keep the review-ready paragraph neutral and specific; write the AC note as questions the authors can answer (e.g., "Could the authors share the logs for the ECE analysis mentioned in §5?"), grouped as Understand / Defend / Sign.
