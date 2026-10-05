# C. Academic literature and reports on AI-slop signals in research papers (2023-2026)

Compiled 2026-10-05. Every item below was checked against a primary page (arXiv abstract/API, ACL Anthology, venue site, or the publisher's blog) unless marked **[UNVERIFIED]** or **[SECONDARY]** (secondary = news/aggregator report only). Numbers are quoted as the source gives them. Some numbers came through a summarising fetch tool; where they matter, check them against the PDF before you publish.

Fetch problem: the arXiv HTML full text of 2610.00531 (SciSlop) returned HTTP 429 (rate-limited), so the six SciSlop measures are **not** listed individually below. Only the abstract (via the arXiv API) and the project page were read.

---

## 0. Verification verdicts for the collaborator's citations (task item 5)

| Citation as given | Exists? | Actual title / authors | Key finding |
|---|---|---|---|
| arXiv:2610.00531 "Science or Slop?" (Oh et al.) | **YES** (posted 2026-09-30, cs.AI) | "Science or Slop?: Benchmarking and Mitigating Scientific Slop in AI-Generated Papers", Yerim Oh, Young-Jun Lee, Jaewoo Ahn, Gunhee Kim, Dongyeop Kang | SciSlopBench: 390 AI papers, each paired with a human paper matched on problem and contribution type. Six paper-level measures across **Structure, Argument, Artifacts** identify the AI paper in each pair with **85.9%** accuracy, vs **68.7%** for Binoculars. Higher slop goes with lower ICLR ratings and separates rejected from accepted papers above chance in every year 2017-2025. Prompting the model to optimise the measures directly causes reward hacking. SciSlopHarness, which allows revisions only where experiment records support them, cuts the remaining AI-human gap by **63%** vs the best revision baseline. |
| Pew Research "How much of the internet is written with AI", 2026-08-20 | **YES** | Pew Research Center (Data Labs), Samuel Bestvater, Aaron Smith, Carson TerBush, Chris Baronavski, Janakee Chavda. https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/ | About 490k English Common Crawl pages scored with Open Pangram. About **10%** of a July 2026 random sample show significant signs of AI authorship, and **over one-third** of pages published after Nov 2022 do. By domain: .com about 10%, .org 4.6%, .edu/.gov about 1%. Between 2023 and 2026: em dashes **doubled**, Oxford commas **+63%**, AI vocabulary (delve, pivotal, testament) **doubled**, negative parallelism ("it's not just X, it's Y") **nearly tripled**. |
| Hadan et al. 2024, *Computers in Human Behavior: Artificial Humans*, doi 10.1016/j.chbah.2024.100095 | **YES** (the DOI resolves to Elsevier pii S2949882124000550; DOAJ lists vol 2(2), article 100095) | "The great AI witch hunt: Reviewers' perception and (mis)conception of generative AI in research writing", Hilda Hadan, Derrick M. Wang, Reza Hadi Mogavi, Joseph Tu, Leah Zhang-Kennedy, Lennart E. Nacke (Waterloo). arXiv:2407.12015 | 17 experienced HCI reviewers rated human, AI-paraphrased and AI-generated snippets. They **could not reliably tell them apart**: medians about 5/10 on an AI-involvement scale, human mean 4.44 vs AI-generated mean 5.12. AI-*paraphrased* text was seen as the **least** AI (median 2, mean 2.74) and as more honest. Quality judgments did not change with perceived AI involvement. Reviewers' cues (structure, word choice, problematic statements) were inconsistent. **Implication: reviewers' gut "this sounds AI" judgments are unreliable.** |
| aclanthology.org/2025.coling-main.426 | **YES** | Tom S. Juzek and Zina B. Ward, "Why Does ChatGPT 'Delve' So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models", COLING 2025 (arXiv:2412.11385). Wikipedia mislabels it as ACL Findings. | Identifies **21 focal words** overused due to LLMs (list with % increases in section 1). Rules out model architecture, algorithms and training data as the cause. Points to RLHF as a likely contributor. |
| NAACL 2025 Findings 271 (aclanthology.org/2025.findings-naacl.271) | **YES** | Brian Tufts, Xuandong Zhao, Lei Li, "A Practical Examination of AI-Generated Text Detectors for Large Language Models" | Evaluates 7 detectors (RADAR, Wild, T5Sentinel, Fast-DetectGPT, PHD, LogRank, Binoculars) on unseen domains and models. Some have a **TPR as low as 0% at 1% FPR**. Even moderate prompting effort evades detection. **Implication: per-paper detector scores are fragile.** |
| arXiv:2609.14988 on model-generated reference errors | **YES** (posted 2026-09-14, cs.CL) | Maxim Topaz, Zhihong Zhang, Nir Roguin, Pallavi Gupta, Zichao Li, Laura-Maria Peltonen, "Biomedical Reference Generation Remains Unreliable across 26 Large Language Models" | 26 LLMs (2023-2026) asked to supply a missing reference for 69 biomedical passages. Across all models, **55.4%** of responses were fabricated and only **14.9%** correct in every field (2026 models: 35.3% fabricated, 31.8% fully correct). Fabrication ranged from 10.2% (Claude Opus 4.8, which declined 52.1% of prompts) to 98.4% (Ministral 3B). No model was fully correct in more than **54.6%** of responses. **Real papers with wrong metadata (authors, year, venue) are a distinct error class:** Claude Sonnet 4.5 named authors correctly in only 28.7% of verifiable references. |
| ICLR 2027 AI policy page | **YES** | https://iclr.cc/Conferences/2027/AIPolicyForAuthors and https://iclr.cc/Conferences/2027/AIPolicyForReviewers, linked from the Author Guidelines | See section 6. A **mandatory AI use statement** is required (it does not count toward the page limit). An LLM-produced falsehood, plagiarism or misrepresentation is a Code of Ethics violation and can lead to desk rejection. Reviewers must submit their original self-written assessment plus all LLM interactions. |
| AISTATS 2027 CFP AI policy | **YES** (read on the Submission FAQ page https://virtual.aistats.org/Conferences/2027/SubmissionFAQ; I did not open the CFP page itself) | AISTATS 2027 | An **AI Use Statement** is mandatory and placed before the references. **Missing it means desk rejection.** Substantive AI help with proofs, hypotheses, experiments, analysis and similar must be disclosed. Hidden prompts are scientific misconduct. Reviewers may not use an LLM to generate reviews. Every submission gets an AI review that checks **factual correctness only**. |

**Bottom line: all 8 citations are real.** One caveat: the Juzek & Ward venue is COLING 2025, not ACL.

---

## 1. Lexical and stylistic fingerprints of LLM text in scientific writing

### 1.1 Kobak, González-Márquez, Horvát, Lause (2025). "Delving into LLM-assisted writing in biomedical publications through excess vocabulary." *Science Advances* 11(27), 2 July 2025. doi:10.1126/sciadv.adt3813. arXiv:2406.07016
- Corpus: about 15M PubMed abstracts, 2010-2024. Method: excess frequency versus a counterfactual extrapolated from 2021-2022.
- **At least 13.5% of 2024 abstracts** were LLM-processed (lower bound). Up to about **40%** in some subgroups (v4 text: computational fields about 20%; China, South Korea and Taiwan over 15%; MDPI 19% vs Nature/Science/Cell 6%; combined subgroups up to 38%).
- Excess-word ratios (r = observed/expected frequency, v4): **delves r = 28.0** (the earlier version reported 25.2, the source of the widely quoted "25x"), **underscores r = 10.9**, **showcasing r = 10.2**. Common words by frequency gap δ: **potential δ = 0.045, findings δ = 0.031, crucial δ = 0.029**.
- 2024 excess words were **style words**: 319 excess words, **66% verbs, 16% adjectives**. COVID-era excess words (2020-2022) were content nouns (coronavirus, lockdown, pandemic; r up to over 1000).
- Marker set used for subgroup estimates: *across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within*.
- Other named style words: intricate, notably, pivotal, meticulously.
- **Signal:** many low-content style verbs and adjectives together (delve/underscore/showcase/intricate/pivotal/meticulous/notably/additionally). The LLM effect on vocabulary exceeds the effect of COVID.

### 1.2 Liang et al. (2024). "Mapping the Increasing Use of LLMs in Scientific Papers." COLM 2024. arXiv:2404.01268
- About 950k papers (arXiv, bioRxiv, Nature portfolio), Jan 2020 to Feb 2024. Distributional GPT quantification at corpus level.
- Estimated LLM-modified sentences by Feb 2024. Abstracts: **CS 17.5%**, EESS 14.4%, Math 4.9%, Nature portfolio 6.3%. Introductions: CS 15.5%, EESS 12.4%, Math 3.9%, Nature 4.3%.
- Higher LLM use goes with: first authors who **post preprints more often**, **crowded research areas**, and **shorter papers**.
- The top LLM-disproportionate words in CS abstracts: **realm, intricate, showcasing, pivotal**. They were flat from 2010 to 2022 and surged in 2023.
- **Signal:** realm/intricate/showcasing/pivotal. Short papers in crowded subfields from prolific preprinters show higher population-level LLM share. That is weak evidence at the individual level.

### 1.3 Liang et al. (2024). "Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews." ICML 2024. arXiv:2403.07183
- Estimated share of review text substantially LLM-modified: **ICLR 2024 10.6%, NeurIPS 2023 9.1%, EMNLP 2023 16.9%, CoRL 2023 6.5%** (overall range 6.5-16.9%). Nature portfolio reviews showed no significant rise.
- Indicative adjectives in reviews: **"meticulous" about 34.7x, "intricate" about 11.2x, "commendable" about 9.8x** (frequency-ratio increases). Others: innovative, notable, versatile.
- Correlates of LLM-heavy reviews: **submitted within 3 days of the deadline**, **no scholarly citations**, **lower reviewer confidence**, **reviewer did not respond to the rebuttal**, and **homogenized** (less diverse) reviews in embedding space.
- **Signal (reviews):** praise adjectives (commendable/meticulous/intricate/innovative/notable/versatile), no citations, generic and homogeneous content.

### 1.4 Gray (2024). "ChatGPT 'contamination': estimating the prevalence of LLMs in the scholarly literature." arXiv:2403.16887
- Keyword-based estimate: **at least 60,000 papers (slightly over 1% of all articles) in 2023** were LLM-assisted. Words used include intricate, meticulous/meticulously, commendable, notable/notably, innovative, pivotal, showcasing (word list from memory, **[verify the exact list in the PDF]**).

### 1.5 Geng & Trotta
- (a) "Is ChatGPT Transforming Academics' Writing Style?" arXiv:2404.08627 (ICML 2024 workshop). About 1M arXiv abstracts, May 2018 to Jan 2024. Estimated about **35% of CS abstracts** show ChatGPT-revision patterns (calibrated by simulating "revise the following sentences" with GPT-3.5). **"significant" +99% in CS**; **"is"/"are" down 14-17% in CS**.
- (b) "Human-LLM Coevolution: Evidence from Academic Writing." Findings of ACL 2025 (2025.findings-acl.657). Words that got publicity, such as **"delve", dropped sharply after early 2024**, while others such as **"significant" kept rising**. Authors are editing LLM output, so detection by the famous words decays over time.
- **Signal:** fewer simple copulas (is/are), replaced by "serves as / stands as / represents". Word lists **age**: delve is now a weak 2023-24 signal.

### 1.6 Juzek & Ward (2025), COLING 2025, 21 focal words (2020 to 2024 % change in PubMed abstracts)
delves +6697%, delved +2240%, delving +1817%, showcasing +1396%, delve +1375%, boasts +918%, underscores +904%, comprehending +899%, intricacies +773%, surpassing +667%, intricate +611%, underscoring +537%, garnered +437%, showcases +422%, emphasizing +397%, underscore +391%, realm +381%, surpasses +368%, groundbreaking +330%, advancements +278%, aligns +267%.
- Follow-up: Juzek & Ward, "Word Overuse and Alignment in LLMs: The Influence of Learning from Human Feedback", arXiv:2508.01930. Experimentally links lexical overuse to learning from human feedback: human raters prefer text variants that contain certain words.

### 1.7 Kousha & Thelwall (2025). "How much are LLMs changing the language of academic papers after ChatGPT? A multi-database and full text analysis." ISSI 2025. arXiv:2509.09596
- 12 LLM terms, 6 databases, 2.4M open-access full texts. 2022-2024: **delve +1500%, underscore +1000%, intricate +700%**. Papers using "underscore" **6 or more times** rose more than 10,000% from 2022 to 2025.
- **Co-occurrence:** the correlation between underscore and pivotal rose from **0.032 (2022) to 0.449 (2024)**.
- **Signal:** clusters of these words matter more than any single word. Repeated use of the same word (e.g., "underscore" 6 or more times) is a strong signal.

### 1.8 Em dash studies
- Czuma (2026). "Em-ergence of the em-dash: a population-level rise in em-dash frequency in medRxiv preprints." arXiv:2606.29540, pre-registered (OSF HFT8C). N = 69,632 medRxiv Discussions. **Share with at least one em dash: 4.23% before ChatGPT, 11.58% after** (OR 2.96). By year: about 4% through 2023, **8.0% in 2024, 20.3% in 2025**. Placebo split showed no change. The author explicitly says it is **"a population-level indicator, not a per-paper detector."**
- Freeburg (2026). "The Last Fingerprint: How Markdown Training Shapes LLM Prose." arXiv:2603.27006. 12 models from 5 providers. Em dashes range from 0.0 per 1k words (Llama) to 9.1 per 1k (GPT-4.1, even when told to avoid markdown). The author argues em dashes are markdown habits leaking into prose and survive suppression in most models.
- Blog (pieceofk.fr, [SECONDARY]): ecology abstracts on OpenAlex, 2021 vs 2025. Em dash relative frequency **more than doubled**, the largest change of any character.
- Pew 2026 (above): em dashes doubled on the web, 2023 to 2026.
- **Caveat:** Wikipedia "Signs of AI writing" (Sept 2026 note) says newer models suppress em dashes. It cites a July 2026 study finding that **only Claude used em dashes more than professional writers, and ChatGPT used fewer** ([UNVERIFIED]: underlying study not located). Treat em dashes as a weak, model-dependent signal.

### 1.9 Negative parallelism ("not X but Y" / "it's not just X, it's Y")
- Pew 2026: **nearly tripled** on the web, 2023 to 2026. This is the only quantitative large-scale figure found.
- Wikipedia "Signs of AI writing" covers three variants: "Not just X, but also Y", "Not X, but Y", "Y rather than X".
- Robinson & Corley's reviewer report (section 4.4) lists "It's not X, it's Y" marketing-speak in submissions they reviewed.
- No peer-reviewed study with a per-paper frequency ratio was found. **[GAP]**

### 1.10 Lexical diversity, structure, and other population-level shifts
- Sanger & Maurer (2026), arXiv:2602.03864. 149k ASCE civil and environmental engineering abstracts, 2000-2025. Abstracts classed as likely LLM-assisted show **higher lexical diversity, more commas, more complexity, less passive voice and less hedging**: prose that is "more segmented, complex, and confident." This contradicts the folk belief that LLM text has *lower* lexical diversity in abstracts. **Reduced hedging / overconfidence** is the useful signal.
- Ben-Zion et al. (2026), arXiv:2603.01718. All 109k PLOS ONE articles, 2019-2025. Manuscripts got longer (+14.8% for African-affiliated, +11.7% Asian, +5.3% native English). Non-native-English teams shrank (6.54 to 6.06) and collaborated 36% less with native-English coauthors.
- Liang et al. 2024 (reviews): higher LLM share goes with less diverse reviews in embedding space (homogenization).

### 1.11 Wikipedia: Signs of AI writing (WP:AISIGNS), community guide, raw wikitext read 2026-10-05
Section headings and their example cues:
- **Content:** undue emphasis on significance, legacy and broader trends ("stands/serves as", "is a testament/reminder", "a pivotal/crucial/key role", "underscores its importance", "reflects broader", "setting the stage for", "evolving landscape", "indelible mark", "deeply rooted"); superficial analyses; promotional language; vague attributions ("experts argue", "observers have cited", "several sources" when few are cited); outline-like conclusions ("Despite its ..., faces several challenges", "Future Outlook").
- **Language:** high density of "AI vocabulary" (additionally, align with, boasts, bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance, fostering, garner, highlight, interplay, intricate, key, landscape, meticulous, pivotal, robust, showcase, tapestry, testament, underscore, valuable, vibrant); avoidance of is/are ("serves as", "features", "offers"); negative parallelisms; rule of three.
- **Style:** title case headings, overuse of boldface, inline-header bullet lists, em dashes, emoji, unusual tables, curly quotes, skipped heading levels.
- **Communication:** text addressed to the user ("I hope this helps"), knowledge-cutoff disclaimers, placeholder text.
- **Markup:** Markdown in the wrong context; tool artifacts such as `contentReference`, `oaicite`, `turn0search0`, `utm_source=chatgpt.com`, Gemini `[cite: 1]`, Grok `grok_card`.
- **Citations:** broken or invented links.
- **Word "eras":** 2023 to mid-2024 (GPT-4): delve, tapestry, testament, meticulous, intricate, boasts. Mid-2024 to mid-2025 (GPT-4o): align with, fostering, showcasing, underscore. Mid-2025 onward (GPT-5): emphasizing, enhance, highlighting, showcasing, plus canned notability claims.
- **Signal for papers:** leftover tool markup, placeholder text, or user-directed phrases in a manuscript are near-conclusive. The vocabulary cues are probabilistic.

---

## 2. AI-generated full papers / AI scientist systems and their failure modes

### 2.1 Sakana AI Scientist v1: Lu et al. 2024, arXiv:2408.06292; independent evaluation by Beel, Kan, Baumgart (2025), "Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future?", SIGIR Forum 2025, arXiv:2502.14297
- **42% of experiments failed** from coding errors. Others produced flawed or misleading results. Code changes per iteration were small (about 8% more characters).
- Novelty checks were poor: it labelled established ideas (e.g., micro-batching for SGD) as novel.
- Manuscripts had a **median of 5 citations, mostly outdated (5 of 34 from 2020 or later)**, plus **missing figures, repeated sections, placeholder text ("Conclusions Here"), and hallucinated numerical results**.
- Cost **$6-15 per paper with about 3.5 h of human involvement**. Quality: "a rushed undergraduate paper."
- **Signals:** few and old references, placeholder text, duplicated sections, numbers not backed by experiments, known ideas claimed as novel.

### 2.2 AI Scientist v2: Yamada et al. 2025, arXiv:2504.08066; Sakana blog https://sakana.ai/ai-scientist-first-publication/
- 3 fully AI-generated papers were submitted to the ICLR 2025 **ICBINB ("I Can't Believe It's Not Better")** workshop. **1 of 3 scored 6, 7, 6 (avg 6.33)**, above the average acceptance threshold. It was withdrawn by protocol. Workshop acceptance runs about 60-70%; Sakana's own reviewers judged that none met the main-conference bar.
- Errors Sakana found in its own paper: **citation misattribution (an LSTM attributed to Goodfellow 2016 instead of Hochreiter & Schmidhuber 1997)**, missing figures and citations, formatting issues.

### 2.3 Luo, Kasirzadeh, Shah (2025). "The More You Automate, the Less You See: Hidden Pitfalls of AI Scientist Systems." arXiv:2509.08713 (NeurIPS 2025 workshop)
- Tested Agent Laboratory and AI Scientist v2 against four pitfalls:
  1. **Inappropriate benchmark selection.** Agent Laboratory: **82.4% picked the first four listed benchmarks** (positional bias). AI Scientist v2 favoured easier datasets when SOTA references were shown (p < 1e-30).
  2. **Data leakage.** No direct test-set access, but both systems **made their own synthetic data or subsampled the provided datasets without saying so in the paper**.
  3. **Metric misuse.** Choices followed metric order in the prompt. AI Scientist v2 **swapped user-specified metrics (e.g., to F1) without explanation**.
  4. **Post-hoc selection bias.** When test performance was artificially inverted, Agent Laboratory's choice of the top candidate fell from 78.5% to 43.5%. AI Scientist v2 picked the worst-ranked candidate 49% of the time. Both select on test-set results.
- LLM auditor detecting these pitfalls: **paper alone 55% accuracy (F1 0.51), paper + logs + code 82% (F1 0.81)**, p = 6.3e-5. The authors recommend that venues require trace logs and code.
- **Signals:** undocumented synthetic or subsampled data; metric switched from the stated task; benchmarks that are easy or simply listed first; reported best-of-N without selection protocol; no code or logs.

### 2.4 Si, Yang, Hashimoto (2024/2025). "Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers." arXiv:2409.04109 (ICLR 2025)
- LLM ideas were judged **more novel than expert ideas (p < 0.05)** and slightly less feasible. LLMs **cannot evaluate their own ideas** and produce **little diversity** (many duplicates at scale).

### 2.5 Si, Hashimoto, Yang (2025). "The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas." arXiv:2506.20803 (ICLR 2026 poster)
- 43 experts each spent over 100 hours executing randomly assigned ideas and wrote 4-page papers, reviewed blind.
- After execution, **LLM-idea scores fell significantly more than human-idea scores on every metric (p < 0.05)**, and the **ranking flipped** on several metrics.
- **Signal:** AI work looks novel on paper but delivers weak results when executed. Check whether the evidence supports the headline novelty.

### 2.6 Gupta & Pruthi (2025). "All That Glitters is Not Novel: Plagiarism in AI Generated Research." ACL 2025 (2025.acl-long.1249), arXiv:2502.16487
- 13 experts reviewed 50 LLM-generated research documents. **24% were paraphrased or substantially borrowed** from prior work with one-to-one methodological mapping, confirmed by the original authors. Most of the rest showed varying degrees of similarity to existing work.
- **Automated plagiarism detectors failed** to catch the plagiarised ideas.
- **Signal:** "novel" methods that map step by step onto an uncited existing paper. Text-overlap checks miss this kind of idea plagiarism.

### 2.7 Agents4Science 2025: Bianchi, Queen, Thakkar, Sun, Zou, "Exploring the use of AI authors and reviewers at Agents4Science", arXiv:2511.15534; Science News coverage
- **315 submissions** (62 desk-rejected as incomplete), 253 reviewed, **48 accepted**.
- Fully AI-driven research (≥95% AI at every stage): **23.3% of submissions vs 14.9% of accepted papers**. AI was more autonomous in **analysis and writing** than in hypothesis and design.
- **Only about 44% of submissions (111) had no hallucinated references.** Authors themselves reported "a high proportion of references were hallucinated", plus technical errors and lack of creativity.
- LLM reviewers: average pairwise correlation 0.48. Mean absolute difference from humans: GPT-5 0.91, Claude Sonnet 4 1.09, Gemini 2.5 Pro 2.73 (sycophantic).
- Human reviewer quote (Risa Wechsler, via Science News [SECONDARY]): papers were "technically correct" but "**neither interesting nor important**". AI technical skill can "mask poor scientific judgment."

### 2.8 Other systems (claims are self-reported)
- **Agent Laboratory** (Schmidgall et al. 2025, arXiv:2501.04227): research quality improves with human feedback (co-pilot mode); **84%** lower cost than earlier autonomous systems.
- **CycleResearcher** (Weng et al., ICLR 2025, arXiv:2411.00816): simulated review scores were 5.36 for generated papers vs 5.24 for human preprints vs 5.69 for accepted papers. CycleReviewer has 26.89% lower MAE than individual human reviewers. These are *simulated* reviews, so treat with caution.
- **AI-Researcher** (Tang, Xia, Li, Huang 2025, arXiv:2505.18705): introduces Scientist-Bench. Claims "approaching human-quality" papers, self-assessed.

### 2.9 Paper-level verification benchmarks (related to whole-paper checks)
- **SPOT** (Son et al. 2025, arXiv:2505.11855): 83 published papers with 91 errata- or retraction-level errors. The best LLM (o3) reaches **21.1% recall, 6.1% precision**. LLMs are poor at verifying papers.
- **FLAWS** (Xi et al. 2025, arXiv:2511.21843): 713 paper-error pairs with claim-invalidating errors inserted. The best model (GPT-5) gets **39.1% identification at k = 10**.
- **CiteAudit** (Shi et al. 2026, arXiv:2602.23452): benchmark plus multi-agent pipeline for detecting hallucinated citations.

---

## 3. Hallucinated and fabricated citations

- **GPTZero, NeurIPS 2025** (https://gptzero.me/news/neurips/, 21 Jan 2026): scanned **4,841 accepted papers** and found **100+ hallucinated citations in 53 papers**. Types: invented authors, nonexistent DOIs/URLs, wrong volume and pages, half-real titles, wrong arXiv IDs, added or dropped authors. Submissions grew 9,467 to 21,575 (+220%) from 2020 to 2025.
- **Ansari (2026). "Compound Deception in Elite Peer Review: A Failure Mode Taxonomy of 100 Fabricated Citations at NeurIPS 2025."** arXiv:2602.05930. About 1% of acceptances were affected. Taxonomy: **Total Fabrication 66%, Partial Attribute Corruption 27%, Identifier Hijacking 4%, Placeholder Hallucination 2%, Semantic Hallucination 1%**. 100% showed compound failure modes. 92% of affected papers had 1-2 bad citations; 8% had 4-13. Recommends mandatory automated citation checks.
- **GPTZero, ICLR 2026** (https://gptzero.me/news/iclr-2026/, 6 Dec 2025): sampled **300 of about 20k submissions** and found **50 with at least one confirmed hallucinated citation** (about 1 in 6 of those sampled). Some had review averages as high as 8.0.
- **ICLR 2026 PC response** (blog.iclr.cc, 19 Nov 2025): hallucinated references are a **Code of Ethics violation** and lead to **desk rejection**. Detectors are used, with AC/SAC verification. **Retrospective** (blog.iclr.cc, 31 Mar 2026): 19,525 valid submissions, 779 desk rejections (all causes), 76,139 reviews. LLM detectors were run on all reviews. Automated reference checking had a high false-positive rate, so PCs checked every flagged reference by hand. Confirmed hallucinations led to desk rejection with appeal.
- **arXiv policy** ([SECONDARY], aiweekly.co citing moderator Thomas Dietterich, early 2026): a **1-year ban** for "unambiguous AI-generated errors, including hallucinated references". Afterwards, peer review at a reputable venue is required before posting. The same source says about **1 in 277** arXiv submissions had hallucinated citations by early 2026 (10x since 2023) and "20% of sampled ICLR 2026 submissions" had at least one hallucination. **[Verify on arXiv's blog]**
- **Topaz et al. 2026** (arXiv:2609.14988, section 0): 55.4% fabrication across 26 LLMs. A separate error class is real papers with wrong metadata.
- **Agents4Science**: only about 44% of submissions were free of hallucinated references.
- **Signal hierarchy:** (1) a reference that does not resolve or does not exist (strong). (2) A real title with wrong authors, year or venue, or an arXiv ID pointing to a different paper (strong; GPTZero and Topaz both show this is common). (3) A real paper cited for a claim it does not make (semantic). (4) Few and outdated references (AI Scientist median 5).

---

## 4. Detection of AI papers and reviews at venues; detector bias

### 4.1 Pangram Labs, ICLR 2026 (https://www.pangram.com/blog/pangram-predicts-21-of-iclr-reviews-are-ai-generated, 18 Nov 2025)
- About 19.5k papers and about 75.8k reviews analysed. **21% of reviews (15,899) fully AI-generated**; over half show some AI involvement.
- Papers: **61% mostly human-written**, **9% have more than 50% AI content**, several hundred fully AI-generated.
- **Papers with more AI content got lower scores**, falling nearly linearly. **Fully AI reviews gave higher scores** (about 4.4 vs 4.1 for human reviews); AI reviews of human papers scored about 1 point higher than reviews of fully AI papers ([SECONDARY], via PlagiarismToday). AI reviews were longer with less information density.
- Claimed false-positive rate about **1 in 10,000** on human text. Vendor claim; the 2022 control set came out almost entirely human.
- **Signal:** a high AI share in a paper predicts lower peer-review scores. This agrees with the SciSlop ICLR correlation.

### 4.2 Liang, Yuksekgonul, Mao, Wu, Zou (2023). "GPT detectors are biased against non-native English writers." *Patterns* 4(7), arXiv:2304.02819
- 7 detectors misclassified **about 61% of TOEFL essays** (non-native writers) as AI-generated, while native essays were classified correctly. Simple prompting both removes the bias and evades detection.
- **Caveat for screening:** never use detector scores or "plain/formulaic English" as slop evidence against non-native authors.

### 4.3 Other detector reliability evidence
- Tufts, Zhao, Li (NAACL Findings 2025): TPR as low as 0% at 1% FPR out of domain; easily evaded.
- Hadan et al. (2024): human reviewers cannot tell AI from human snippets.
- SciSlop: token-level Binoculars reaches 68.7% on paired AI vs human papers; structural measures reach 85.9%.

### 4.4 Reviewer field report ([SECONDARY], blog): Robinson & Corley, "Reviewing AI slop", geospatialml.com, 30 Jul 2026
- 22 submissions across NeurIPS (Datasets & Benchmarks, Position tracks), WACV and the TerraBytes ECCV workshop. **15 (68%)** were AI slop or had fabricated citations. Two papers flagged for fake citations were still accepted as orals, with fixes required.
- Observed signs: invented authors on real papers (e.g., "Yuyang Cong, Saurabh Khanna" for "Yezhen Cong, Samar Khanna"), dense hard-to-parse sentences, many em dashes and semicolons, "It's not X, it's Y", heavy bold, **numbers in prose that contradict the tables**, SOTA claims on gains under 1% with no statistics, 40-50 pages of jargon, **leftover LLM notes beside citations**.

### 4.5 ICML 2026 enforcement against reviewers (blog.icml.cc, 18 Mar 2026)
- Hidden-instruction watermarks in PDFs (two of about 170k phrases per PDF) caught **506 reviewers** who had chosen the no-LLM policy but used one anyway (795 reviews, about 1%). **497 papers desk-rejected** because the reviewer was also an author on them.
- Kim et al. (2026), "Use and Effects of LLMs in Peer Review: A Randomized Experiment and Survey at ICML 2026", arXiv:2609.19420. The policy arm had minimal effect on scores and decisions; permissive-arm reviews were 5.5-7% longer. **22.5% of restrictive-arm reviewers admitted using LLMs anyway**; 36.5% of the permissive arm admitted prohibited uses.

---

## 5. Whole-paper coherence measures

- **Oh et al. 2026, "Science or Slop?"** (arXiv:2610.00531) is the only work found that measures **paper-level coherence** of AI papers directly. The project page says it checks whether "sections build on each other, claims and citations are argued, and the method and evidence can be inspected" through six measures under Structure, Argument and Artifacts. **Exact definitions not retrieved** (HTML rate-limited). Get them from the PDF or the GitHub/HF release before quoting. Key claims: 85.9% pairwise accuracy; ICLR rating correlation 2017-2025; revisions need grounding in evidence, and plain prose polishing does not remove the slop.
- Luo, Kasirzadeh, Shah 2025: paper-only audits are near chance (55%); adding logs and code raises accuracy to 82%. The artifacts carry the evidence.
- SPOT and FLAWS show that LLM verifiers are still weak at finding errors that invalidate claims.

---

## 6. Venue LLM policies

| Venue | Authors | Reviewers | Penalties / notes |
|---|---|---|---|
| **ICLR 2026** (iclr.cc/FAQ/LLM; blog 19 Nov 2025) | Any LLM use must be disclosed (paper and form). Authors are accountable. | Disclose; keep confidentiality. | LLM-produced falsehoods, plagiarism or **hallucinated references are a Code of Ethics violation and lead to desk rejection**. Low-quality LLM reviews can get the reviewer's own papers desk-rejected. Hidden prompt injection counts as collusion. |
| **ICLR 2027** (AIPolicyForAuthors/Reviewers; blog "Submission policies for ICLR 2027", 2 Sep 2026) | **Mandatory AI use statement** (outside the page limit). Disclosure *required* for synthetic data, theory and frameworks, math claims, methodology, implementation, interpretation, proofs. *Recommended* for code, figures, literature work, brainstorming, drafting, reference formatting. | Limited use allowed. Must submit the **original self-written assessment plus all LLM interactions**. Hallucinations or mismatches with the self-report are penalised. | Desk rejection of all of the reviewer's papers possible. Also: **20-submission cap per author**; first-time authors limited to 1 paper without a qualified reciprocal reviewer; all papers de-anonymised after review. The PCs say AI makes "paper-shaped objects" easy to produce. |
| **NeurIPS 2025** (neurips.cc/Conferences/2025/LLM) | Describe LLM use if it is an important, original or non-standard part of the method. Grammar tools exempt. LLMs cannot be authors. **Unverified LLM-generated references are a violation.** | Must not share submissions with any LLM. May use LLMs for concepts or wording without confidential content. | Can revoke publication status even after acceptance. |
| **NeurIPS 2026** (MainTrackHandbook) | Describe agent/LLM use in the experimental setup if non-standard. Warns about hallucinated plots and citations. No AI authors. | **No LLM use except on papers where it is specifically allowed, and then only the sanctioned LLM** (IRB randomized experiment). | Prompt injection is prohibited. Penalties include rejection, removal, sharing identities with other conferences, and notifying institutions. |
| **ICML 2026** (icml.cc/Conferences/2026/LLM-Policy) | Authors choose whether their paper requires Policy A (no reviewer LLM use) or allows Policy B. | **Policy A:** no LLM use. **Policy B:** privacy-compliant LLMs to understand and polish only, never to judge, list strengths and weaknesses, or write the review. Reciprocity applies. | Hallucinated review content is subject to discipline. **497 papers desk-rejected** after watermark detection (above). |
| **AISTATS 2027** (SubmissionFAQ) | **Mandatory AI Use Statement; missing it means desk rejection.** Required disclosure covers substantive help with proofs, hypotheses, methods, experiments, analysis, synthetic data. LLMs cannot be authors. | May not delegate judgment or write reviews with an LLM. | Hidden prompts count as misconduct (retroactive rejection). Every paper gets an **AI factual-correctness review** (no score). |
| **ACL** (Policy on Publication Ethics, AI writing assistance) | No disclosure needed for grammar, spelling, predictive keyboards, or polishing your own content. **Disclose** literature search, generated text about existing ideas, and AI-inspired ideas. Using AI for primary content or drafts without disclosure is not allowed. | No AI-drafted reviews or meta-reviews. Do not upload manuscripts to non-private tools. Paraphrasing allowed. | Public correction or retraction under the ethics process. |

---

## 7. Consolidated evidence signals (for the slop checklist)

**Strong (near-conclusive individually):**
1. Nonexistent references, or real titles with wrong authors, year, venue or ID (GPTZero; Ansari; Topaz; Agents4Science only about 44% clean).
2. Leftover tool markup or LLM notes (`oaicite`, `turn0search0`, `utm_source=chatgpt.com`, "[cite: 1]", "Certainly! Here is…", placeholder text such as "Conclusions Here") (WP:AISIGNS; Beel et al.; Robinson & Corley).
3. Numbers in the text that contradict tables; numbers without any experiment behind them (Beel; Robinson & Corley).
4. Duplicated sections, missing figures referenced in text (Beel; Sakana).

**Moderate (methodological, from AI-scientist audits):**
5. Undocumented synthetic or subsampled data; a metric changed from the stated task; easy or arbitrary benchmarks; best-of-N reported without a selection protocol; no code or logs (Luo, Kasirzadeh, Shah).
6. Few, outdated references (median 5) (Beel).
7. "Novel" method that maps one-to-one onto an uncited prior paper (Gupta & Pruthi: 24%).
8. Novel-sounding framing but trivial, "technically correct but not interesting" results; SOTA claims on gains under 1% without statistics (Si et al. ideation-execution gap; Agents4Science; Robinson & Corley).
9. Sections that do not build on each other; claims not argued from evidence (SciSlop's Structure/Argument/Artifacts).

**Weak (population-level stylistic; never decisive alone; aging):**
10. Clusters of AI vocabulary: delve(s) (r 25-28), underscore(s) (r about 10.9), showcasing (r about 10.2), intricate, realm, pivotal, meticulous(ly), commendable, notably, additionally, crucial, comprehensive, enhance, fostering, garner, groundbreaking, surpass, boasts, align(s) with, tapestry, testament, landscape, interplay (Kobak; Liang; Juzek & Ward; Kousha & Thelwall). **The same word repeated 6 or more times** is a stronger cue.
11. Negative parallelism, "not just X but Y" (Pew: about 3x on the web).
12. Em dashes (medRxiv Discussions 4.2% to 20.3% by 2025; Pew 2x). **Model-dependent and now often suppressed.**
13. Copula avoidance (is/are down 10-17%; "serves as", "stands as"); significance puffery ("a testament to", "pivotal role", "evolving landscape"); rule of three; boldface and inline-header bullet lists; reduced hedging and overconfident tone (Geng & Trotta; WP:AISIGNS; Sanger & Maurer).
14. Review-specific: praise adjectives (meticulous about 34.7x, intricate about 11.2x, commendable about 9.8x), no citations, generic, submitted at the deadline (Liang et al. 2024).

**Cautions to include in any screening skill:**
- Detector and stylistic judgments are biased against non-native writers (61% false positives on TOEFL essays) and are easily evaded (0% TPR at 1% FPR in some settings). Humans cannot reliably spot AI text (Hadan).
- Word lists drift: delve dropped after 2024 (Geng & Trotta; WP word eras).
- Polishing the prose does not fix slop. SciSlop shows prompting to reduce slop causes reward hacking; only revisions grounded in the experiment records help. A writing-polish skill should not make polished prose its target and should check claims against the evidence.

## Unverified / gaps
- Exact definitions of the six SciSlop measures (HTML rate-limited).
- Gray 2024 exact keyword list.
- The July 2026 em dash study cited by Wikipedia (only Claude above professional writers).
- arXiv hallucination-ban details and "1 in 277" figure (secondary source only).
- No peer-reviewed per-paper frequency ratio found for "not X but Y".
