# AI Contribution Statement — template

Purpose: make human steering and verification **visible**. Fill only with facts the author confirms; mark gaps `[AUTHOR TO CONFIRM]`. Adapt to the target venue's required fields (e.g., ICLR 2027 requires an AI-use statement `[ICLR27-policy]`: disclosure is required for synthetic data, theory and frameworks, math claims, methodology, implementation, interpretation and proofs, and recommended for code, figures, literature work, brainstorming and drafting). Draft it only when a human author is available to confirm the facts; omit it in pipeline runs and in audit runs without an author.

## Short form (fits a paper's disclosure section)

> **Use of AI tools.** ⟨Stage⟩: ⟨what the AI did⟩; ⟨what humans decided/verified⟩. … All claims, numbers, and references were verified by ⟨who⟩ against ⟨results files/logs/original sources⟩. The authors take full responsibility for the content.

Example:
> **Use of AI tools.** *Idea:* the research question and hypotheses were formulated by the authors; an LLM was used to search for related work, and all cited papers were read by the authors. *Implementation and experiments:* a coding agent implemented the training scripts and executed 412 runs under configurations specified by the authors; logs and configs are released with the code. *Analysis:* the authors selected which analyses to run and interpreted all results; the diagnostic study in §5 was added after the initial method failed, a decision made by the authors because ⟨reason⟩. *Writing:* an LLM drafted parts of §2 and §4 from author outlines; the authors rewrote and verified all text. *Verification:* every reference was checked against DBLP/DOI and every number against the released logs by ⟨initials⟩.

## Long form (appendix; for heavily automated work — this is where AI involvement can be a strength)

| Stage | AI role (none / assist / draft / execute / autonomous) | Human decisions | Human verification | Artifact |
|---|---|---|---|---|
| Problem choice | | | | |
| Hypotheses / design | | | | |
| Implementation | | | | code link |
| Experiment execution | | | | logs link |
| Analysis & interpretation | | | | |
| Pivots / changes of plan | | why, decided by whom | | |
| Writing | | | | version history |
| References | | | checked n/N | |

## Notes
- A specific statement is positive evidence (H06). A vague one ("AI tools were used for editing") is neutral; a false one is P10.
- Pivots are not shameful when a human chose them for a stated reason — say so.
- Keep it factual; do not use it to pre-empt criticism (that becomes S01).
