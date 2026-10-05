# Positioning: what we detect, and why

> English version of [POSITIONING_CN.md](POSITIONING_CN.md). If they differ, the Chinese version wins.
>
> v0.4 · 2026-10-05 (v0.4 adds §9 on dual use and the long-term view; v0.2.1 was revised after feedback from an independent reviewer agent, a fact-checking agent and a blind test) · Source keys are in [`SOURCES.md`](SOURCES.md) (in Chinese with English quotes)

## In one sentence

**We detect "the absent author", not "the presence of AI".** Research and writing can be automated. Authorship cannot.

AI can come up with ideas, run experiments and write first drafts, but a paper must have a human who is responsible for it: who makes its tradeoffs, verifies it and answers for its taste. Sloppy AI means this person is absent. In the words of the NeurIPS 2026 Position Track program committee, such text "externalises the cost of verifying that work, imposing it on reviewers" `[NeurIPS26-PP]`. **At its core, slop outsources the cost of verification to reviewers.**

---

## 1. Why we do not build an "AI detector"

| Reason | Evidence |
|---|---|
| Detecting "was this written by AI" is neither reliable nor fair | 2023 detectors misclassified about 61% of TOEFL essays by non-native English writers as AI `[Liang23]`; with the false-positive rate held at 1%, some detectors catch almost no AI text `[NAACL25-detect]`; 17 HCI reviewers could not tell AI text from human text `[Hadan24]` |
| Surface traces are being systematically cleaned | ARIS's writing skill actively removes "delve, pivotal, landscape, tapestry…" `[ARIS-paper-write]`. Our calibration also found that two papers produced by a 2026 Claude pipeline had an AI-lexicon cluster density **below the human median** (`tools/calibration/calibration_report.md`) |
| Venues care about "who is responsible", not "who typed" | ICLR 2027 allows AI use but requires disclosure and holds the authors fully responsible `[ICLR27-policy]`. The COLM 2026 program committee put it this way: "If a paper has an authentic human-vouched contribution, the use of AI to write the paper is not automatically disqualifying" `[COLM26]` |
| Still, readers' impressions are real | Reviewers do become suspicious because of dashes and stock phrases `[ZH-Reddit-1rtll1h]` `[Hadan24]`; the higher the share of text a detector labels as AI, the lower the paper's score `[Pangram25]`, which at least shows that impressions affect scores. So the writing side cannot ignore the L layer, and the reviewing side cannot use the L layer as grounds for a verdict. This follows the distinction, from co-author Zhehao Zou's evidence-bound writing skill, between "perceived risk" and "verifiable defects" `[Zhehao-EBW]` |

## 2. The three kinds of "absence" we detect

| Type of absence | Definition | Main evidence layers | Examples |
|---|---|---|---|
| **Polish absent** (care deficit) | The writing is AI-led, and nobody turned it into their own expression | L layer, plus S01, S04–S06, S08, S10 and others (see the W list under "Grading" in EVIDENCE) | Floods of dashes and "not X but Y", coined terms, defensive writing, performative honesty |
| **Steering absent** (steering deficit) | No human judgement went into the research direction, topic, scale, or what to do after a failure | R layer (R01–R06 etc.), S12, S17 | A method that does not work is turned into an "audit" paper; theoryslop; toy scale with grand claims; a problem without taste |
| **Verification absent** (verification deficit) | Nobody checked the final product item by item | P layer, R07–R10 | Hallucinated references, chatbot residue, text–table contradictions, phantom experiments |

The three can occur independently. **The papers we most want to handle strictly are those high on the R axis (steering or verification absent)**: if the writing was also left unpolished, the paper is D, genuine AI waste; if the writing is clean, it is C, and it is likewise reviewed item by item on R-layer evidence. Absent polish on its own is "salvageable but not encouraged".

There is a fourth thing we do **not** detect: ordinary quality problems (insufficient baselines, overstated conclusions, an uninteresting problem). These go into a separate **Q axis**, which is part of normal reviewing and **does not enter the "absence" narrative**. A bad paper written by a human is a bad paper and should not be labelled "AI slop".

### Four quadrants (consistent with the four quadrants under "Grading" in [EVIDENCE.md](../EVIDENCE.md))

```
                       Research steered (R0–R1)          Research not steered (R2–R3)
Writing polished  A Normal AI-assisted work          C "Gilded" shell: hardest to spot, expected to grow
(W0–W1)           → review normally                  → bypass the L layer; review R/P items on substance

Writing AI-led    B Sound content, sloppy writing    D Genuine AI waste
(W2–W3)           → give an actionable rewrite list; → handle strictly on verifiable defects; refer to the AC
                    do not reject on writing alone
```

**Quadrant C deserves particular emphasis.** We **expect** it to grow, because pipelines have learned to clean surface traces, for example the writing contract ARIS adopted after 2026-08-26 `[ARIS-PR423]`. There are no data on its size yet, but a typical example has already appeared in the blind test (`skills/paper-slop-screen/references/worked-examples.md`, example 6). A paper with clean writing and unsupervised research cannot be caught by any style detection; it shows only at the research level: pivot traces, a mismatch between scale and claims, phantom experiments, design choices without reasons. This is why we treat the R layer as the core.

## 3. Why this matters

1. **A time-saving triage tool for reviewers.** According to unofficial reports, ICLR 2027 received more than 60,000 abstract registrations `[ICLR27-60k]`; TMLR's desk-reject rate rose from about 6% to about 53% `[TMLR26]`; one reviewer said that for half the papers on his list he spent more time than the authors had `[36kr-ICLR26]`. Using the evidence list in the first 15 minutes to decide whether a paper deserves a close reading leaves time for the papers that do.
2. **Evidence in place of intuition and detector scores, to protect due process.** The community has already pushed back hard against "desk rejection based on detector scores" `[NeurIPS26-PP-backlash]`. Our reports say only "page 4, paragraph 2 says X, while Table 3 on page 7 says Y", never "AI probability 87%". Authors who are wrongly suspected can respond item by item.
3. **A final "author pass" for authors.** We are not against auto-research; AI is often more honest than people at running experiments and keeping logs. What we ask is that **before submission, a human checks the paper in the role of author**. The writing skill is designed so that "the skill asks the questions and the human makes the decisions" (see Section 6).
4. **Capturing community consensus and taste.** What counts as a slop paper currently exists only in scattered complaints on Xiaohongshu, Reddit, HN and various venue blogs. A maintained list with sources and strength levels lets new reviewers and students learn how senior reviewers judge.
5. **Actionable evidence types for venue policy.** The ICLR 2027 CfP requires papers to represent "significantly more work than … can be produced autonomously by any current AI agent" `[ICLR27-CfP]`. What does "the level an autonomous agent can produce" look like? The R layer is one concrete answer.

## 4. The future: AI involvement may become worth highlighting

Our view: **the dimension "AI involvement" will become neutral, and in some places positive. The dimension that will keep discriminating is "the visibility of human steering and verification".**

- Today, heavy AI involvement correlates strongly with low scores: among the 50 COLM 2026 papers with the highest detector AI scores, preliminary counts show that **none was recommended for acceptance** `[COLM26]`. Note that these numbers come from detectors themselves and may partly reflect reviewer bias against "AI flavour". **Our working hypothesis** is that the correlation comes mainly from "nobody steered, nobody verified", rather than from "AI was used". The hypothesis is testable: among papers that disclose heavy AI execution and provide logs, are scores still low?
- As agents get stronger, the following will become **points in a paper's favour**: AI ran more seeds, did more thorough ablations, automatically checked every number and every reference, and left complete experiment logs. Luo et al. found that auditing the flaws of AI-scientist systems from the paper alone reached 55% accuracy, rising to 82% with logs and code `[Luo25]`. Transparent AI execution makes a paper **more auditable**.
- **Credit for auditability.** Review reports have a separate "auditability" field: A+ = runnable code, configurations, full logs (including failed runs), a specific AI contribution statement or version history; A = code plus statement; A0 = main text only. Auditability does not cancel ⚑. But when the R axis is in doubt, **for an A+ paper you should check the logs instead of guessing**. The model we encourage is heavy AI execution + high auditability + a human signing off on the topic and conclusions.
- So this project should maintain **two tables** at once:
  - **Negative evidence** (L/S/R/P layers): traces of human absence.
  - **Positive evidence** (H layer): signs of human presence, such as design rationale, scale matching claims, checkable examples, traceable artifacts and a specific AI-use statement.
- We also provide an **AI contribution statement template** (`skills/paper-author-pass/references/ai-contribution-statement.md`), similar to CRediT, which states for each of "topic / design / implementation / experiment execution / analysis / writing / verification" what the AI did, what decisions humans made and who checked it. It maps directly onto the mandatory disclosure items of ICLR 2027 `[ICLR27-policy]`. In future a paper could well state with pride: "Experiments were executed by an agent, 412 runs in total, logs in the appendix; problem selection, hypotheses and conclusions were decided by the authors and checked item by item." At that point, our H layer is the standard for evaluating it.
- **A pivot is not a sin in itself.** A paper that deliberately chose a "diagnostic/negative-results" direction, on a problem that really matters, is a good paper. R01 targets **the pivot as the cheapest way out**: the method failed, the agent switched narratives `[ARIS-README-run]` (its review loop stops when the LLM review score is ≥6/10 and the verdict is ready/almost `[ARIS-review-loop]`), and no human judged whether the new question was worth pursuing.

## 5. Boundaries and ethics

1. **No AI probability, no authorship attribution.** We output only "evidence + location + strength + three-axis grading (W/R/Q) + flags + auditability + what evidence would overturn the judgement".
2. **L-layer evidence never supports a negative research judgement on its own.** Calibration shows that the L layer separates 2024–25 AI papers well (AUC up to 0.96), but almost fails on 2026 pipelines and is confounded by era (`tools/calibration/calibration_report.md`).
3. **Care for non-native authors.** Smooth English is not evidence (L15 is marked as having the highest false-positive rate). Our writing skill never suggests deliberately introducing grammatical errors or reducing clarity to "sound human".
4. **Review confidentiality.** Giving a submitted PDF to an external LLM may violate a venue's reviewing policy: ICML 2026 used watermarks to catch 795 non-compliant reviews, which led to 497 associated submissions being desk-rejected `[ICML26]`; ICLR 2027 requires reviewers who used LLMs to disclose those interactions `[ICLR27-policy]`. The reviewing skill may be used only within what the venue's policy allows (a local model, or tools the venue permits); otherwise use it only to train the human eye, that is, read the list and check by hand.
5. **Dual-use risk of the writing skill.** The writing skill could be used to "launder" slop: sentence-level polishing would turn a quadrant-D paper into a quadrant-C paper, which is worse. Our response: the skill has a hard rule that when no human author is involved (for example, when an autonomous pipeline calls it), it **outputs only review comments and a list of questions, does not edit the manuscript and does not answer questions on the author's behalf**; the writing skill turns R/S-layer problems into **questions that the human author must answer**, rather than having the agent answer them; it does not fabricate results, examples or references; it keeps real negative results. A pipeline with no human author that calls it gets only a list of questions to answer, not a laundered paper. Plenty of open-source tools already do surface cleaning `[BH]` `[Leey21]`; our added value is at the higher levels. Misuse of the list itself, and why we publish it anyway, is discussed in §9.
6. **Due process.**
   - For quadrant-D papers, reviewers give scores on the grounds of verifiable defects; in the confidential comments they give the AC an evidence table phrased as questions the authors can answer and, where needed, suggest requesting logs, code or an author Q&A (following TMLR's practice `[TMLR26]`). **The public review does not say "this was written by AI".**
   - Only a ☠ you have personally verified shifts the burden of verification back to the authors; "unable to respond" does not mean "guilty", especially when there is a language barrier.
   - For quadrant D with an accusatory ⚑, we suggest that a second person independently re-check at least one item.
   - False positives are recorded in `docs/field_reports/false_positives/`; any increase in strength requires checking human counter-examples, so that the list does not only move in the stricter direction.
7. **This tool is not for**: complaints against peers, reporting students, hiring or promotion evaluations, or public accusations against published papers.

## 6. Use cases

| Scenario | What to use | How |
|---|---|---|
| **In-house writing, last round before submission** | `paper-author-pass` skill | From high level to low: story, taste and scale → argument structure → verification → sentences. Output: a list of decision questions for the authors, an edit diff, a draft AI contribution statement |
| **Collaborator / advisor reading** | [EVIDENCE.md](../EVIDENCE.md) plus `slop_lint.py` | Go through the R/S layers in 15 minutes; use the lint report to locate clustered L-layer regions |
| **Reviewer triage** | `paper-slop-screen` skill (when the venue's policy allows) or the manual list | Produce an "evidence card" in the first 15 minutes and decide how deeply to read; the review comments cover only substantive problems |
| **AC / meta-review** | The ⚑ items and R-layer evidence in the screen report | Decide whether to request logs, code or an author Q&A |
| **Teaching / supervising students** | The R and H layers of [EVIDENCE.md](../EVIDENCE.md) | Train research taste: what research steered by a person looks like |
| **Community building** | `docs/field_reports/` and CONTRIBUTING | Anonymize the slop met in real reviewing and add it to the list |
| **Calibration research** | `tools/calibration/` | Expand the corpus (especially 2025–26 human papers) and re-check how well each item discriminates |

## 7. Relation to existing work

| Work | What it does | How we differ |
|---|---|---|
| **Anti-Autoresearch** `[AA]` (a reviewing-side tool built by the ARIS authors themselves) | 46 integrity-hack patterns (numbers, baselines, leakage, references…), plus 13 style impressions with **zero weight in the verdict** | We keep its principle that "style does not convict", but **add a layer for "absent steering/taste"** (R01–R03; plus R12–R14 on the Q axis), and we cover the writing side; style evidence is still used to support the "polish absent" judgement (quadrant B) |
| **evidence-bound-paper-writing** by co-author Zhehao Zou (unpublished) `[Zhehao-EBW]` | Quality first; separates perceived risk from verifiable defects; very cautious | We keep its evidence grading and its contract of "not altering the scientific content"; on top of that we give **negative judgements** more explicitly (quadrant D is handled strictly) and add pipeline fingerprints |
| **Humanizer-type tools** (`[BH]` `[AV]` `[Leey21]` etc.) | Sentence-level de-AI-ing | We use them as sources for L-layer rules; our focus is on the S/R layers, and we require decisions from the human author |
| **Research-paper writing skills** (`[MC]` etc.) | How to write a good paper | We borrow claim-evidence mapping and reverse outlining, and connect them to slop evidence |
| **AI detectors** (Pangram, GPTZero, Binoculars) | Output probabilities | Used only as a weak prior, never for a verdict |

## 8. Roadmap

- **v0.3 (carried over, not completed in v0.2):** collect 2025–26 human papers as a modern control group and recalibrate the lint; add real field reports from the reviewing side.
- **v0.3 (continued):** turn reference checking and number checking into executable scripts (integrating refchecker `[refchecker]`); find real review-loop samples for S01–S05, such as papers produced by ARIS between March and August 2026, to test how well they discriminate.
- **Long term:** work with venues to make the H layer and AI contribution statements a norm, so that "transparent AI execution + visible human steering" becomes the encouraged practice.

## 9. Dual use and the long-term view

**We know this list will be misused.** Anyone can load EVIDENCE.md or the two skills into a writing agent and scrub the L-layer and some S-layer traces, plus the easy-to-fix P-layer residue (chatbot residue, pipeline watermarks, placeholders); existing paraphrasing tools already do much of that `[BH]` `[Leey21]`. Publishing the list will make surface traces lose their value sooner. We accept that, for three reasons:

1. **Scrubbing text cannot lower R.** Under the grading rules, L-layer evidence counts only toward W, and B (salvageable) and D (AI waste) differ only on the R axis. A quadrant-D paper with perfectly clean prose keeps its R2–R3 grade: it moves from D to the harder-to-spot C at best, never to A or B, and C is exactly where our review procedure concentrates (§2). Lowering R takes real verification, judgement about failures, scale that matches the claims, logs and code. That is the research itself. We gave up the arms race over wording on purpose.
2. **Some things no checklist can supply.** Whether references are real, whether numbers reproduce from logs and code, whether the design rationale holds up, whether the authors can answer follow-up questions: all of these need a person who was there. What can still be faked cheaply is surface material (invented logs, an empty AI contribution statement). Against that, only a ☠ that someone **verified personally** shifts the burden of proof, and we suggest asking for logs, code or a short author Q&A `[TMLR26]`.
3. **By default, the writing skill does not work for an absent author.** With no human author it only audits and returns questions (§5, item 5), and every run ends with three questions only the author can answer (below). This is a default, not a safeguard: the skill cannot verify that a human is present, and it is MIT-licensed, so anyone can change it. Points 1 and 2 are what actually hold.

**The long-term view: text will prove less and less.** For many papers, writing is no longer the hard part, and polished prose already says little about who stands behind it. In September 2026, a summit of mathematicians convened by Harvard CMSA recommended that "a PhD should not be awarded primarily on the basis of the text of the dissertation", asked for "a rigorous thesis defense that requires complete mastery of the thesis content", and stated that "AI use should accelerate understanding, not bypass understanding" `[CMSA26]`. We expect the evaluation of papers to take the same road: away from "can you produce the text" and toward what only a present author can supply, namely disclosed AI use, artifacts others can check (code, logs, formal proofs, pre-registration), and the ability to defend the work in person. If this project speeds that shift up by making surface traces worthless sooner, that is what we want.

**Three questions.** The standard can be put as three questions (adapted from Chinese-language commentary on the summit, not from the report itself):

> Do you understand it thoroughly? Would you defend it face to face? Will you put your name behind it?

`paper-author-pass` ends every run with three paper-specific questions of these kinds (Understand / Defend / Sign) for the author to answer before signing; the skill never answers them. `paper-slop-screen` groups its questions for the AC the same way. When TMLR editors phoned authors, the authors of three papers could not answer basic questions about their own work `[TMLR26]`; the questions are meant to surface that before submission.

**Our commitments.** The skills ask and never answer for the author; no AI probabilities, and every finding carries a location and a quote; only disqualifying (☠) evidence that a person has checked shifts the burden of proof to the authors; false positives are logged in public and change the list.
