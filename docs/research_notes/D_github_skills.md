# D. GitHub skills, prompts and tools: anti-slop, academic writing, reviewing, detection

Research date: 2026-10-05. Scope: public GitHub repos of SKILL.md-style skills, prompt collections and tools relevant to (a) an evidence list of "AI slop paper" signals, (b) a writing-polish skill for AI-assisted papers, and (c) a review-screening skill that estimates unsteered AI production of ML papers.

## 0. Method and access notes

- `gh search repos` and `gh api repos/...` are blocked in this session (403, session bound to configured repos). Every repo below was instead verified by a shallow `git clone` of the public repo, and its files were read locally. Star counts come from `img.shields.io/github/stars/<owner>/<repo>.json` on 2026-10-05 (rounded the way shields rounds them).
- Raw texts of every skill file I read are saved in `research/raw/` (one file per repo, with `<!-- ===== FILE: path ===== -->` separators). The Sakana human reviews of the AI Scientist papers (PDFs) were converted to text and are saved there too.
- Not found or not verifiable: a public repo for Stanford's "Agentic Reviewer" (paperreview.ai), ReviewerToo (my guessed path `hao-ai-lab/ReviewerToo` does not exist), Pangram and GPTZero (closed source; there is no public detector repo), `daveshap/AntiSlop`, and `jxzhangjhu/awesome-ai-research-writing`. I name none of these as a source below.

## 1. Repo inventory (verified)

Legend for "Use": W = writing-polish skill, E = evidence list of slop signals, R = review-screening skill.

| Repo | Stars | License | What it is | Use |
|---|---|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | 54k | MIT | Canonical "humanizer" SKILL.md (v3.1.0). 26 patterns derived from Wikipedia "Signs of AI writing", ranked by strength | W, E |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 18k | MIT | Short skill plus phrase and structure references, with a 5-dimension score | W |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 4.8k | MIT | The most engineered anti-AI-writing skill (v3.36). Tiered word lists, about 80 named patterns, P0/P1/P2 severity, detect/rewrite/edit modes, deterministic detector, preservation validator, human-control corpus | W, E, R |
| [ashgreat/humanizer](https://github.com/ashgreat/humanizer) | 4 | MIT | Academic humanizer fitted to 495 LLM-draft vs. published-human paragraph pairs from 26 marketing papers. Gives measured ratios. Ships a `detect_ai.py` | W, E, R |
| [cbsteh/anti-ai-writing](https://github.com/cbsteh/anti-ai-writing) | 1 | MIT | Academic-science anti-AI skill that ranks substance above style: citations, then epistemic verbs, then specificity, then surface prose | W, E, R |
| [brandonwise/humanizer](https://github.com/brandonwise/humanizer) | 127 | MIT | JS CLI and MCP server. 24-pattern catalog, tiered AI vocabulary, burstiness and type-token-ratio statistics | E, R |
| [isatimur/de-slop](https://github.com/isatimur/de-slop) | 3 | MIT | Detect, rewrite, self-score loop. Separates "rewordable" from "hollow" paragraphs. `flag_slop.py` regex flags with documented blind spots | W, R |
| [welttowelt/stop-slop-refined](https://github.com/welttowelt/stop-slop-refined) | 12 | MIT | Fork of stop-slop with words, patterns and a reader-fit reference | W |
| [shreyashankar/plain-writing-skill](https://github.com/shreyashankar/plain-writing-skill) | 461 | MIT | "Plain and boring" style skill: 25 rules, each with a before and after, plus a `deslopify` command | W |
| [jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing) | 499 | (none found) | Banned words, phrases and openers, with first-word tells per model and AI vocabulary by era | E |
| [Kiterlin/anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing) | 787 | MIT | Removes defensive caveats and "we do not claim" framing while keeping necessary limits | W, E |
| [lensback940701/Evidence-Bound-Press-Conference-Revision-Skill](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill) | 254 | MIT | Defensive-writing triage for one manuscript (D1-D8 cut codes, K1-K4 keep codes), with a claim-ceiling contract and a regression protocol | W |
| [sam-paech/slop-forensics](https://github.com/sam-paech/slop-forensics) | 373 | MIT | Toolkit that computes over-represented words, bigrams and trigrams per model. Includes slop lists per domain (essays, varied prompts, creative writing, human writing) | E, R |
| [sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler) | 355 | Apache-2.0 | Backtracking sampler. Ships 2,000 slop words, 2,500 slop phrases and a few slop regexes | E |
| [EQ-bench/creative-writing-bench](https://github.com/EQ-bench/creative-writing-bench) | 145 | (none found) | Defines the "slop index": weighted hits from the slop list per 1,000 words | R |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 13k | MIT | `20-ml-paper-writing/ml-paper-writing` (Nanda, Farquhar, Gopen & Swan, Lipton, Steinhardt, Perez), citation-verification workflow, `rigor-reviewer` (6-dimension epistemic review) | W, R |
| [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) | 2.4k | MIT | Evidence-bound `scientific-writing` and `peer-review` skills with no-fabrication rules (biomedical lean). Sibling repo claude-scientific-skills has 48k stars | W, R |
| [YSLAB-ai/manuscript-writing](https://github.com/YSLAB-ai/manuscript-writing) | 12 | MIT | Revision and review modes driven by one sequential checklist (Phase 0-5), with a "Needs Verification" output | W, R |
| [write-with-ai/paper-writing-guide](https://github.com/write-with-ai/paper-writing-guide) | 1 | CC BY 4.0 | Section-by-section guidance for academic papers (one main result, limitations, conclusion as forward-looking) | W |
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | 7.2k | MIT | ML/CV paper-writing skill: reverse outlining, claim-evidence map, five-dimension adversarial self-review | W, R |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 50k | (copyright Cheng-I Wu, see repo) | Large research pipeline. `writing_quality_check.md` is an explicitly non-humanizer checklist with discipline exceptions. Experiment provenance gate | W, R |
| [wanshuiyin/Auto-claude-code-research-in-sleep (ARIS)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 17k | MIT | 78+ research skills: `paper-write` (5 audit passes), `citation-audit` (KEEP/FIX/REPLACE/REMOVE), `paper-claim-audit` (number-to-file matching), `auto-review-loop`, `integrity-forensics` | W, R |
| [wanshuiyin/Anti-Autoresearch](https://github.com/wanshuiyin/Anti-Autoresearch) | 157 | MIT | Reviewer-side integrity forensics: 46 hack patterns in 8 families, 13 AI-style impressions that carry zero verdict weight, deterministic GRIM/GRIMMER/statcheck/hedge-density/pipeline-artifact checks | E, R (top) |
| [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) | 35k | (none found) | Chinese prompt collection (MSRA, Seed, Shanghai AI Lab, PKU, USTC, SJTU): 去AI味 prompts for English LaTeX and Chinese Word, polishing, logic check, reviewer-perspective prompt, AI-flavored word list | W, R |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) / [-v2](https://github.com/SakanaAI/AI-Scientist-v2) | 15k / 7.3k | AI Scientist Source Code License (RAIL-based) | Reviewer prompt using the NeurIPS form, a strict "reject if unsure" system prompt, and a VLM figure/caption/figref review | R |
| [SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment](https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment) | 307 | (none found) | Three fully AI-generated ICBINB submissions, with Sakana's own human reviews and code reviews. Ground-truth failure modes of unsteered AI papers | E, R (top) |
| [maxidl/openreviewer](https://github.com/maxidl/openreviewer) | 17 | (none found) | Llama-OpenReviewer-8B, fine-tuned on 79k ICLR/NeurIPS reviews. Reviewer-guideline system prompt | R |
| [allenai/marg-reviewer](https://github.com/allenai/marg-reviewer) | 64 | Apache-2.0 | MARG multi-agent review generation (specialized agents for experiments, clarity and impact) | R |
| [Ahren09/AgentReview](https://github.com/Ahren09/AgentReview) | 519 | Apache-2.0 | Simulates the peer-review process with LLM agents (EMNLP 2024) | R |
| [zhu-minjun/Researcher](https://github.com/zhu-minjun/Researcher) / [ResearAI/DeepReviewer-v2](https://github.com/ResearAI/DeepReviewer-v2) | 405 / 578 | CycleResearcher License / MIT | CycleReviewer and DeepReviewer (Fast, Standard and Best modes). `AIDetector` wraps Fast-DetectGPT. v2 is a tool-grounded agent loop (pdf_read_lines, pdf_annotate, paper_search) | R |
| [markrussinovich/refchecker](https://github.com/markrussinovich/refchecker) | 533 | MIT | Reference verification against Semantic Scholar, OpenAlex, CrossRef, DBLP and ACL Anthology, plus LLM web search for hallucinated references. Bulk scans of OpenReview venues | E, R (top) |
| [ahans30/Binoculars](https://github.com/ahans30/Binoculars) | 421 | BSD-3 | Zero-shot detector using a cross-perplexity ratio from Falcon-7B and Falcon-7B-instruct. Low-FPR threshold 0.8536 (chosen at 0.01% FPR); accuracy threshold 0.9015 | R |
| [vivek3141/ghostbuster](https://github.com/vivek3141/ghostbuster) | 183 | CC | Feature search over weak-LM probabilities plus a classifier. Reports 99.0 F1 in-domain | R |
| [eric-mitchell/detect-gpt](https://github.com/eric-mitchell/detect-gpt) | 480 | MIT | Detector based on probability curvature | R |
| [anthropics/skills](https://github.com/anthropics/skills) | 180k | per-skill | Reference SKILL.md format (skill-creator, doc-coauthoring, docx). No anti-slop skill | format |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills), [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 15k / 76k | various | Lists. They led me to plain-writing-skill and anti-ai-slop-writing | discovery |

## 2. Per-repo findings

### 2.1 Humanizer and anti-slop writing skills

**blader/humanizer (54k, MIT).** This is the de facto standard and the one Leey21 recommends to Chinese researchers.
- Theory: a model picks the choice that fits the widest range of readers, so every tell is a "default choice". It groups six families: Staging, Rhythm by rule, Inflation, Formatting by rule, Leftovers, and Wrong reader. "Word habits change with every model release. The structural habits persist, so they lead the list."
- Strength ranking: patterns 1-5 justify an edit on one sighting. A pattern marked "weak alone" (dashes, stacked qualifiers, hyphenated pairs, passive voice, curly quotes, a single self-description) needs other tells nearby before acting. Rule: "Every sentence you keep must add something the reader did not already have."
- Workflow: (1) mark the tells, including at paragraph scale; (2) draft a rewrite with no new fact, name, number, quote or citation; (3) check by reading aloud, ask "what still sounds AI-generated?", and re-check the tells that most often survive a rewrite (contrasts, closers, triads, dashes, bold labels); (4) write the final version. Output modes: pasted text returns draft, remaining patterns and final; file mode writes only the final text and changes only prose; embedded mode returns the final text only.
- Voice: a user writing sample overrides every rule, including the dash rule. Reference and technical text stays neutral.
- "When not to act": quotations, titles, proper names, salutations, text written before 2022-11-30. "People who judge by feel do little better than chance... several tells together are the safeguard."
- Weaknesses for academic use: it is tuned for Wikipedia and blogs. Its blanket no-dash rule and its push toward active voice can be wrong for papers. It has no epistemic or citation checks. An independent stress test (cited in avoid-ai-writing) found it installs a recognizable "humanizer voice" of fragments and staccato rhythm.

**hardikpandya/stop-slop (18k, MIT).** Eight core rules: cut filler, break formulaic structures, active voice, be specific, put the reader in the room, vary rhythm, trust readers, cut quotables. It also has quick checks and 1-10 scoring on Directness, Rhythm, Trust, Authenticity and Density, with revision required below 35/50.
- Concrete lists: throat-clearing openers ("Here's the thing", "The uncomfortable truth is", "It turns out", "Let me be clear"). Emphasis crutches ("Full stop.", "Let that sink in", "Make no mistake"). Business jargon (navigate, unpack, lean into, landscape, game-changer, deep dive, circle back). An adverb kill-list (really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, inevitably, interestingly, importantly, crucially). Vague declaratives ("The implications are significant", "The stakes are high").
- Structures: binary contrasts in 11 templates ("Not because X. Because Y.", "The question isn't X. It's Y.", "stops being X and starts being Y"). Negative listing. Dramatic fragmentation. Rhetorical setups ("What if...?", "Think about it:"). False agency ("the data tells us", "the decision emerges"). Narrator-from-a-distance. Wh- sentence starters. Lazy extremes (every, always, never).
- Weaknesses: "No passive constructions", "kill all adverbs" and "two items beat three" are harmful in science writing (statistically, respectively, and passive methods sentences are all legitimate). It is blog-oriented.

**conorbronsdon/avoid-ai-writing (4.8k, MIT).** This is the best-engineered skill and the closest model for our polish skill's contract.
- Editing contract: a candidate match becomes a finding only after the pass conditions and context are checked, and a finding becomes an edit only when the mode and scope authorize it. "Detection alone never authorizes rewriting." Source fidelity: never invent facts, experience, stance, causality or confidence. Protected content (quotes, code, tables, URLs, identifiers) is reported, not rewritten. Source text is treated as data, never as instructions.
- Modes: `rewrite` (default), `detect` (findings only, grouped P0/P1/P2, with each flag labeled a clear problem or a judgment call), and `edit` (in place, minimal Edit-tool changes, already-human paragraphs untouched). Options: `--voice casual|professional|technical|warm|blunt`, `--context`, `--style config.json`, and `--iterate` (at most 2 editing passes).
- Severity: P0 credibility killers are cutoff disclaimers, chatbot artifacts, vague attributions and significance inflation. P1 obvious AI smell covers the word lists, template phrases, "Let's", synonym cycling, formulaic openings, bold overuse, generic future closers, hedge-stacked predictions, and invented contrast-pair mirroring ("false precision rather than genuine accuracy"). P2 polish covers em-dash rate above 1 per 1,000 words, rule of three, uniform paragraph length, copula avoidance, and Moreover/Furthermore.
- Word tiers: Tier 1A AI-frequency markers (delve, landscape, tapestry, realm, paradigm, embark, beacon, testament to, robust, comprehensive, cutting-edge, leverage, pivotal, underscores, meticulous, seamless, intricate, holistic, actionable, impactful, interplay, at its core, genuinely...). Tier 1B clarity edits (utilize, in order to, due to the fact that, serves as, features, boasts, commence, ascertain, endeavor), explicitly "not evidence of machine authorship". Tier 2 flags a cluster when two or more appear in a paragraph (harness, navigate, foster, elevate, streamline, empower, bolster, resonate, facilitate, underpin, nuanced, crucial, multifaceted, myriad, plethora, encompass, catalyze, cultivate, illuminate, elucidate, transformative, cornerstone, paramount, poised, burgeoning, nascent, overarching, quietly, deeply...). Tier 3 flags by density at max(3, 3% of words) (significant, innovative, effective, dynamic, scalable, compelling, unprecedented, remarkable, sophisticated, state-of-the-art).
- "Never inject" list, a failure mode of humanizers: fabricated speaker perspective, manufactured stakes, forced contrarianism, performed candor, em-dash theatrics, staccato conversion, invented specifics.
- Measured calibration: on a 376-document pre-2023 human control corpus, threshold 0 rejects 31.4% of human documents and threshold 6 findings rejects 1.9%. Em-dash rate "is writing-quality guidance, not evidence of machine authorship... do not score or invert it as an authorship signal." It cites detector false-positive rates above 60% for non-native writers (Liang et al. 2023).
- Structure tests: the paragraph-reshuffle test (if body paragraphs can be swapped, it is a list, not an argument) and the treadmill test (if 40-60% can be cut with no loss of information).
- Weaknesses: very long (107 KB of patterns). Its registers are marketing, LinkedIn, crypto and docs, with no academic profile. Several rules (title case, hashtags) do not matter for papers.

**ashgreat/humanizer (4 stars, MIT).** This is the most useful empirical academic source in the scan. It measures 495 paragraph pairs (published human paragraph vs. an LLM rewrite of the same paragraph). Values per 1,000 words:
- Paragraphs per passage: human 1.00 vs. LLM 2.52 (LLMs over-split). Em dashes: 1.11 vs. 7.02 (6.3x). En dashes: humans use more (0.60x for LLM). Characters per word 6.93 vs. 7.32. Copulas 24.2 vs. 19.1 (LLMs avoid "is"). Sentence-length SD 12.3 vs. 10.1. Short sentences under 8 words: 5.6% vs. 3.3%. Long sentences over 30 words: 22.1% vs. 18.4%. Mean sentence length is about equal (23.1 vs. 22.7). Takeaway: LLM rhythm regresses to the mean.
- LLM-leaning words (log-odds z): additionally 5.2, findings 5.1, primary 4.8, comprehensive 4.0, notably 3.8, primarily 3.8, presents, significant, established, approach, assess, observed, reveals, distinct, demonstrates, diverse, utilizing, practical, utilize, essential, solely, critical, outlined, consistently. Rates vs. human: crucial 6x, underscore 5x, notably 6x, utilize 5-10x, delve 0 vs. 4, "in conclusion" 0 in human text.
- Human-leaning words: we, be, find, is, thus, effect, different, shows, because, might, will, vs, use, help, suggests. Bigrams: we find, find that, the effect, we use, shows that.
- LLM bigrams: our findings, compared to (36:1 LLM), our analysis, the primary, indicate that, these findings, this approach, demonstrates that, as a result, rather than, designed to, to address, reveals that, underscores the, is essential, this study.
- Tier 1 fixes: deflate Latinate verbs (utilize/employ/leverage to use, demonstrate to show, assess to measure, facilitate to help, elucidate to explain); turn "our findings indicate that" into "we find that"; cut stance adverbs; deflate boosters (never stack two, never pair a booster with "significant"); remove em-dash asides; merge over-split paragraphs; remove roadmap scaffolding.
- "Do NOT over-correct": the rule of three is not a tell in this corpus (2.8 vs. 3.0 per 1k). Keep thus, thereby and therefore. Keep en dashes, long sentences, precise vocabulary, acknowledgment boilerplate, numbers and citations.
- Weaknesses: one domain (marketing and business), one LLM rewrite direction (LLM paraphrasing a human paragraph, not LLM-originated papers), a small repo.

**cbsteh/anti-ai-writing (1 star, MIT).** This is the closest existing match to our academic needs.
- Severity order: (1) citation integrity, (2) epistemic accuracy, (3) specificity, then (4) surface prose. "A perfectly de-slopped sentence built on a fabricated citation is still worthless."
- Epistemic verb ladder: prove (almost never), demonstrate (alternatives eliminated), show, indicate (confounders present), suggest (preliminary), imply (not directly tested). "AI writing defaults to 'demonstrate' or 'show' regardless of design."
- Other rules: "significant" means statistical only; no "highly significant" without an exact p value. Calibrated hedges must name the source of uncertainty; "More research is needed" is not a conclusion. No causal language for observational data. Report n, statistic, df, exact p and effect size. A null result is not proof of no effect. Data is plural.
- Specificity: fake scope claims ("comprehensive analysis" without n, range or period); vague quantifiers ("many studies have found"); "first study to" must give a search scope and date ("As of [year]").
- Citations: verify that each DOI supports the claim; cite primary sources, not reviews; cite the paper that describes a method; avoid citation stacking; label preprints.
- Technical vs. rhetorical use table (robust, optimize, facilitate, enhance, dynamic, comprehensive, framework, significant, impact, model). Words "almost never technical": delve, underscore (verb), pivotal, crucial, transformative, groundbreaking, seamless, holistic, actionable, cutting-edge.
- Keep scientific metonymy ("Figure 2 shows", "the data suggest"). Remove real anthropomorphization ("the study aims to prove"). Passive voice is not an AI tell in science, so do not rewrite procedural passives. Keep functional signposting.
- Scoring: Citation integrity, Epistemic accuracy and Specificity (high weight); Directness and Density (medium). Revise below 35/50 or if any of the first three is under 6.
- Weaknesses: soil-science examples, forces US spelling, bans all em dashes. One star, so it is untested.

**brandonwise/humanizer (127, MIT).** A 24-pattern catalog (content, language, style, communication, filler). The vocabulary tiers that avoid-ai-writing inherited claim "5-20x higher than pre-2023" with no published method. `stats.js` computes sentence-length CV, burstiness (mean consecutive-length difference divided by mean length; it treats human as about 0.5-1.0 and AI as 0.1-0.3), type-token ratio and paragraph statistics into a "uniformity score". Useful as an R-skill feature idea. Its thresholds are unvalidated.

**isatimur/de-slop (3, MIT).** The key idea is triage into rewordable (a real claim under the filler, so rewrite) and hollow (no point, so flag and do not fabricate). It scores each paragraph strong, moderate, weak or fail ("hostile-editor test: does removing it lose anything?"). It iterates at most 3 passes and reports a before-band to after-band change log without overwriting. Its slop catalogue lists regex-detectable tells (hedge, listicle stem, dead transition, manufactured stakes, performed candor, not-only-but-also, negparallel, wrap-up scaffolding, transformation chain "X becomes Y. Y becomes Z.", corrective reveal, forced cohesion, copula inflation, hedge stack). It also lists model-judgment-only tells: hollowness, fabricated stance, smooth-but-empty specificity ("modern technologies that ensure reliability"), and plausible-but-wrong claims.

**shreyashankar/plain-writing-skill (461, MIT).** Every rule has a Before/After pair (good skill design). Rules relevant to papers: no invented jargon or hyphenated coinages ("if not in the dictionary, don't"); no catchy labels in headings ("# The alignment loop" becomes "# Iterative refinement using development disagreements"); no fake agency; no analogies; no negative parallelism; no stacked rhetorical questions; avoid vague demonstrative "This" at sentence start; do not open with a count ("Two cautions."); prefer long explanatory sentences over punchy ones. Weakness: "no en dashes even in ranges" and "contractions OK" conflict with academic conventions.

**jalaalrd/anti-ai-slop-writing (499).** Gives banned openers ("Moreover,", "Furthermore,", "Additionally,", "Interestingly,", "Notably,", "Importantly,", "Indeed,", "Overall,") and first-word tells per model. Its AI vocabulary by era, consistent with Wikipedia's page: 2023 to mid-2024 (GPT-4): additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulous, pivotal, underscore, tapestry, testament, valuable, vibrant. Mid-2024 to mid-2025 (GPT-4o): align with, fostering, highlighting, showcasing, enhance. Mid-2025 onward (GPT-5): emphasizing, enhance, highlighting, showcasing. Implication: word lists decay, and structure lasts.

**Kiterlin/anti-defensive-writing (787, MIT)** and **lensback940701 (254, MIT).** Defensive writing is a distinct AI-paper smell, and Anti-Autoresearch's hedge screen adopts Kiterlin's list.
- Kiterlin: "Write as an author explaining an argument, not negotiating with an imagined critic." Classify each defensive sentence as unnecessary disclaimer, necessary scope condition, real methodological limitation, useful conceptual contrast, evidence-based qualification, or redundant clarification. Convert negative limitations to positive scope ("The analysis focuses on cases from 2015-2023", not "We do not claim these are representative"). Put limitations once, in Limitations or Discussion, not in topic sentences, abstract or contribution bullets.
- Discouraged phrases: "This paper does not claim", "We do not attempt to", "This is not to say", "The goal is not X but Y", "Rather than arguing X", "Of course, this does not fully capture", "To be clear".
- lensback: a contribution-and-scope contract (core contribution, claim ceiling, load-bearing cautions, edit authority) is written before editing. Its regex cue families: D1 self-deprecation (unfortunately, merely, falls short, fails to); D2 pre-emptive defence; D3 hedge cluster (two hedges within 72 characters); D4 work-log narration (we first, initially, then tried, after several attempts); D6 volunteered comparison loss. Keep codes: K1 scope, K2 source-status (plan, authorization, report, observation, inference), K3 rival or negative finding, K4 ethics or method limit. Each changed sentence gets a three-part test: same or narrower claim, same source status, same citation role.

**sam-paech/slop-forensics + antislop-sampler + EQ-bench.**
- Method: count words, bigrams and trigrams per model, excluding stopwords and words frequent in normal English, then aggregate across models into canonical slop lists. The slop index is the weighted sum of slop-term hits divided by word count, times 1,000.
- Top essay-domain trigrams: "plays a crucial role", "plays a pivotal role", "make informed decisions", "extends far beyond", "long term success", "culture of continuous improvement", "one must first", "provide valuable insights", "pivotal role in shaping", "compelling case study", "extends beyond mere", "data driven decision". Bigrams: crucial role, pivotal role, extends beyond, technological advancements, essay delve, continues evolve, fostering culture, complex interplay, underscores importance, role shaping.
- Varied prompts: "here's comprehensive overview/breakdown", "serves powerful reminder", "testament power", "double edged sword", "multi faceted approach", "rich cultural heritage", "last knowledge update", "feel free ask".
- antislop regexes: `not [^.!?]{3,60} but`, `each ... a`, `every ... a`. The main 2,000-word list is dominated by fiction (elara, nodded, whispered, shadows) and is not useful for papers. Use the essays and varied-prompts lists instead.

### 2.2 Academic writing skills

**Orchestra-Research ml-paper-writing (13k, MIT).**
- Narrative principle (Nanda): the What (1-3 claims), Why (evidence), So What. "If you cannot state your contribution in one sentence, you don't yet have a paper." Farquhar's 5-sentence abstract. Spend equal time on abstract, intro, figures and the rest. Reviewers read abstract (100%), intro (90%+), then figures.
- Gopen & Swan's 7 principles: subject-verb proximity, stress position, topic position, old before new, one unit one function, action in the verb, context before new.
- Perez: minimize pronouns ("This result shows"), delete filler (actually, a bit, very, really, basically, quite, essentially).
- Lipton: be specific ("accuracy", not "performance"), drop "may/can" unless genuinely uncertain, delete intensifiers. Steinhardt: consistent terminology.
- Delete the first abstract sentence if it could open any ML paper. Add "This experiment tests whether [claim]" before each experiment.
- Citation rule: never write BibTeX from memory. Search Semantic Scholar or Exa, verify in 2+ sources, fetch BibTeX by DOI, verify the claim appears in the paper, else mark `[CITATION NEEDED]` and tell the user. It claims "AI-generated citations have ~40% error rate" without a source.
- `rigor-reviewer`: D1 evidence relevance with type-aware entailment. Causal wording needs an isolating ablation; "generalizes/robust/across" needs heterogeneous conditions; "outperforms" needs a baseline; descriptive claims need representative sampling; scoping claims need declared bounds. D2 falsifiability, D3 scope calibration (universal markers vs. narrow experiments), D4 argument coherence, D5 exploration integrity ("a tree with zero dead-ends is suspicious"), D6 methodological rigor (single-run results, missing variance). Each is scored 1-5 with anchors.
- Weaknesses: recommends "In this section, we show X" signposting, which conflicts with the anti-slop skills. It is drafting-proactive ("deliver a full draft"), which is the opposite of human steering.

**K-Dense scientific-writer (2.4k, MIT).**
- "AI is not an author, and generated fluency is never evidence." A no-fabrication list covers citations, DOIs, values, denominators, units, effect estimates, methods, software versions, ethics, CRediT, funding and AI disclosures. Every factual claim maps to verified evidence IDs.
- Peer-review `common_issues.md` separates "not reported", "potential design problem", "demonstrated inconsistency" and "integrity concern". Claim-evidence mismatches: causal from observational; mechanistic from association; unlabeled post hoc; "no effect/equivalent/safe" from non-significant results; abstracts omitting harms or null results; novelty broader than the search.
- Weakness: clinical and biomedical framing.

**YSLAB manuscript-writing (12, MIT).** Revision and review modes. Phases: 0 scope; 1 precision (specify vague language, quantify qualitative adverbs, standardize terminology, remove "elegant variation", tautologies, orphan acronyms); 2 concision and flow (nominalizations, merge into property-to-consequence sentences, verify each sentence's purpose, remove argument echoing, transitions only for real logical relations); 3 tone (strip hyperbole, calibrate certainty, convert bullets to prose, remove dashes); 4 rigor (problem statement, citation coverage, classify each claim as evidence, interpretation, limitation or implication, limitations and boundaries, citation specificity, data consistency including percentage denominators, figure sequencing, equation variables); 5 output audit with a "Needs Verification" list. Key rule: "Missing support does not justify substituting a different or weaker claim."

**Master-cai Research-Paper-Writing-Skills (7.2k, MIT).** One message per paragraph, stated in the first sentence. Reverse outlining (topic sentences should map to the thesis). Output contract: outline, paragraphs with explicit roles, self-review checklist, and a claim-evidence map (`Claim | Evidence | Status: supported/needs evidence`). Rejection dimensions: insufficient contribution, unclear writing, weak empirical effect, incomplete evaluation, problematic method design. Each self-review item is marked pass, needs revision, or needs new experiment.

**write-with-ai/paper-writing-guide (1, CC BY 4.0).** Rules: "A paper is an argument, not a report." Don't open generically ("deep learning has achieved remarkable success"). One paper, one main result. Related work is "a short argument for why your work is the natural next step, not a bibliography." "If you show it, don't explain it again in prose." Limitations get their own section. The conclusion is forward-looking with specific open questions, not "we discuss implications". Overclaiming and over-hedging both erode trust.

**Imbad0202 writing_quality_check (50k-star repo).** Explicit design boundary: "It is NOT a humanizer. We do not aim to fool AI detectors." Flagged terms come with a discipline exception rule (paradigm shift in philosophy of science, landscape in ecology, robust estimator in statistics). Keep intro roadmap sentences. Similar paragraph or sentence lengths are acceptable; "do not introduce variation for its own sake". Mirror-structure warning: every section built as topic sentence, then 3 evidence points, then synthesis. Its experiment-provenance gate (`planned_vs_executed[]`, `negative_results[]`, claims audited as ALIGNED, OVERSTATED or NOT_SUPPORTED_BY_PROVENANCE) is directly relevant to the "human steering" question.

**ARIS paper-write (17k, MIT).** Five audit passes: clutter table; active voice (passive allowed for methods); sentence architecture (flag sentences over 40 words, "don't start consecutive sentences with This or We", vary paragraph molds); the Banana Rule for keyword consistency; numeric and citation integrity (N in abstract equals Table 1, percentages equal raw counts). Cross-model review prompt: "Judge claim calibration in BOTH directions... Flag stacked hedges, self-defence ('we do not claim'), instruction confessions ('we do not address X'), and generic caveats outside Limitations as writing defects. Tone fixes must never alter facts, negation, modality, scope, comparison direction, or numbers." Reverse-outline test. Final checks: no TODO/FIXME/[VERIFY], references.bib contains only cited entries, no stale section files. AI-isms list: delve, pivotal, landscape, tapestry, underscore, noteworthy, intriguingly.

### 2.3 Review and integrity tools (for the screening skill)

**wanshuiyin/Anti-Autoresearch (157, MIT).** This is the most directly relevant repo for skill (c). Design: a span-anchored hashed evidence ledger, then LLM auditors that only propose findings, then a rules-only reporter. It refuses to output an authorship probability. AI-style items are a quarantined track with zero verdict weight ("a paper can be CLEAN and still list many").
- Integrity families: A numeric (HP-NUM-INFLATE headline above own table, DELTA-ERROR, AGG-DRIFT best reported as mean, DENOM-DRIFT, UNIT-DIR-MISMATCH, CAPTION-MISMATCH, APPENDIX-CONTRA, GRANULARITY-IMPOSSIBLE (GRIM), VARIANCE-IMPOSSIBLE (GRIMMER), STAT-INCONSISTENCY (statcheck)). B method and scope (METHOD-DRIFT, RESOURCE-IDENTITY-MISMATCH, ABLATION-ATTRIB, SCOPE-INFLATE, THEOREM-SCOPE-DRIFT, ARGUMENT-CHAIN-BREAK, CAUSAL-EVIDENCE-LEAP, ACRONYM-DRIFT). C baselines (MISSING, WEAK, SIG-OVERLAP "outperforms" without separation). D experiments (FAKE-GT, SELF-NORM, PHANTOM-RESULT, DEAD-METRIC, SUSPICIOUS-REGULARITY "constant offsets, identical decimals", PLACEHOLDER-DATA, RESULT-ARTIFACT-MISMATCH, MISSING-REPRO-ARTIFACT). E citations (HALLUC, CONTEXT, RETRACTED). F presentation, capped at minor (DUP-TABLE, PIPELINE-ARTIFACT, THIN-FLOAT, LLM-FIGURE, PAGE-PADDING). G proofs (OBLIGATION-GAP, CIRCULARITY, DERIVATION-INVALID, SYMBOL-SEMANTIC-DRIFT, ASSUMPTION-SMUGGLE, UNDEFINED-NOTATION). H evaluation (EVAL-LEAKAGE, JUDGE-VALIDITY, SELECTIVE-REPORTING). Advisories: trivial combination ("stapling" A+B+C) and duplicate publication.
- The 13 AIS impressions: NARRATIVE-ARC-BREAK, LLM-PHRASE-TICS, DEFENSIVE-HEDGE, JARGON-STUFF, INVENTED-CODENAME ("Experiment Set Gamma"), CLAUSE-FORMULA-WALL, GRATUITOUS-PSEUDOCODE, BULLET-LIST-OVERUSE, BOLD-MODULE-SPAM, RESTATE-OVERCLAIM, FOCUS-DRIFT, SINGLE-STYLE-FIGURES, APPENDIX-DUMPING-GROUND. Each has a stated false-positive case and a routing rule to an integrity pattern if it turns out to be substantive.
- Deterministic hedge screen: at least 4 hedge sentences across at least 2 non-excluded sections, and at least 25% of scope sentences. Limitations, related work, ethics, broader impact and acknowledgments are excluded.
- `PIPELINE_ARTIFACT_PHRASES`: "as an ai language model", "as a large language model", "as of my last knowledge update", "regenerate response", "i cannot fulfill", "<your text here>", "[insert ", "todo: cite", "[citation needed]", "lorem ipsum". This follows the Problematic Paper Screener (Cabanac, Labbé, Magazinov).
- Weaknesses: heavy infrastructure (pinned commits, GPT auditors). Needs LaTeX, code and results for L1/L2 checks.

**SakanaAI AI-Scientist reviewer (15k).** The NeurIPS review form in JSON (Summary, Strengths, Weaknesses, Originality/Quality/Clarity/Significance 1-4, Questions, Limitations, Ethics, Soundness/Presentation/Contribution 1-4, Overall 1-10, Confidence 1-5, Decision Accept/Reject). System prompt variants: "If a paper is bad or you are unsure, give it bad scores and reject it." Uses reflections and an ensemble with an area-chair meta-review. v2 adds a VLM pass: figure description, figure review, caption review and figref review, catching captions that do not match plots.

**SakanaAI ICLR2025 workshop experiment.** These are human expert reviews of three fully AI-generated papers and the best available evidence of unsteered-AI failure modes. Observed defects:
- Method text vague or misleading about where the regularizer applies; only the code revealed it.
- Textbook cited instead of the primary source (Goodfellow et al. instead of Hochreiter & Schmidhuber 1997). Missing citations rendered "(?)".
- Wrong figure caption (it says loss falls when it rises). Text claims parity where a figure shows a large gap. Duplicate figures in the appendix. A figure missing for a mentioned dataset.
- Results described that are not shown (ECE discussed but not plotted). Methods claimed but never run: temperature scaling was implemented in code and never executed, yet the paper describes it.
- Planned-vs-executed drift: "domain adaptation" and "multi-dataset training" are named, but the code that ran trained separate models per dataset because the real implementation failed.
- About 57% train-test overlap in a synthetic data generator.
- "Too confident interpretation", trivial hyperparameter studies framed as findings, and related work that "dismisses efforts by the community".

**OpenReviewer, MARG, AgentReview, DeepReviewer.** OpenReviewer's system prompt is a good reviewer-guideline template: objective, strong/weak points, four key questions (problem, motivation, claim support, significance), questions for authors. MARG splits the work among specialized agents. DeepReviewer-v2 grounds the review in tool calls on a parsed PDF (line-anchored annotations) and uses paper_search for novelty. `zhu-minjun/Researcher` exposes `AIDetector` built on Fast-DetectGPT (Llama-3.1-8B) that returns a probability and a confidence level. This is an authorship classifier of the kind Anti-Autoresearch deliberately avoids.

### 2.4 Detection and citation tools

- **refchecker (533, MIT).** Stage 1 is a deterministic pre-filter: unverified in all five databases; author overlap below 60% (for 3+ authors); a DOI or arXiv ID that resolves to a different paper; a broken or wrong URL. Year off by one and venue variants do not count. Stage 2 is an LLM web search that must find a dedicated page, not a mention in someone else's reference list. Stage 3 re-verifies against the metadata the LLM found. Headline from its companion paper "Phantom References" (arXiv 2607.00738, per README): in 2025 about 1 in 20 NeurIPS and USENIX Security papers carried at least 2 likely hallucinated references, at about $0.04 per paper.
- **ARIS citation-audit.** A fresh cross-model reviewer per bib entry gives KEEP, FIX (metadata), REPLACE (wrong context) or REMOVE (hallucinated). Only FIX may be auto-applied. ARIS paper-claim-audit matches every number in the paper to a results file: exact_match, rounding_ok, config_mismatch, aggregation_mismatch, number_mismatch, scope_overclaim or unsupported_claim, then PASS, WARN or FAIL.
- **Binoculars, Ghostbuster, DetectGPT, Fast-DetectGPT.** Perplexity and curvature detectors. Binoculars ships fixed thresholds (low-FPR mode). These give document-level probabilities with known false positives on non-native and edited text (avoid-ai-writing cites more than 60% FPR on non-native writers and an 88% accuracy drop under paraphrase). They suit a weak prior, not a verdict.

### 2.5 Chinese prompts (学术去AI味)

**Leey21/awesome-ai-research-writing (35k).** The 去AI味 (LaTeX English) prompt:
- Prefer plain, precise academic words; avoid leverage, delve into and tapestry.
- No list format; convert items into paragraphs.
- Remove mechanical connectors (First and foremost, It is worth noting that). Reduce em dashes.
- No bold or italics for emphasis.
- Change threshold: "宁缺毋滥" (better none than bad). If the text is already natural, output it unchanged with "[检测通过]" ("check passed").
- Output: Part 1 LaTeX, Part 2 Chinese literal translation, Part 3 modification log. A self-check rejects edits made only to swap words.

The AI-flavored word list: Accentuate, Ador, Amass, Ameliorate, Amplify, Alleviate, Ascertain, Advocate, Articulate, Bear, Bolster, Bustling, Cherish, Conceptualize, Conjecture, Consolidate, Convey, Culminate, Decipher, Demonstrate, Depict, Devise, Delineate, Delve, Diverge, Disseminate, Elucidate, Endeavor, Engage, Enumerate, Envision, Enduring, Exacerbate, Expedite, Foster, Galvanize, Harmonize, Hone, Innovate, Inscription, Integrate, Interpolate, Intricate, Lasting, Leverage, Manifest, Mediate, Nurture, Nuance, Nuanced, Obscure, Opt, Originates, Perceive, Perpetuate, Permeate, Pivotal, Ponder, Prescribe, Prevailing, Profound, Recapitulate, Reconcile, Rectify, Rekindle, Reimagine, Scrutinize, Substantiate, Tailor, Testament, Transcend, Traverse, Underscore, Unveil, Vibrant.

The Chinese Word prompt:
- Remove empty rhetoric: 毋庸置疑 (beyond doubt), 不可磨灭的贡献 (indelible contribution), 范式转移 (paradigm shift), 颠覆性 (disruptive), 深刻 (profound), 切中要害 (hits the nail on the head), 本质 (essence), 痛点 (pain point), 令人惊叹 (astonishing).
- Break English-style long attributive chains (一个...的...的..., "a ... of ... of ...").
- Limit 被 passives.
- Avoid mechanical 首先...其次...最后 ("first... second... finally...") unless the content is truly steps.
- Use no Markdown.

The polish prompt also says: no contractions, avoid "METHOD's" possessives, never add bold, never turn paragraphs into lists. The "logic check" prompt sets a high tolerance and reports only fatal contradictions, terminology drift and serious grammar errors; otherwise it outputs "[检测通过，无实质性问题]" ("check passed, no substantive issues"). The reviewer prompt asks for Summary, Strengths 1-3, Critical Weaknesses (each tied to a specific experiment or argument) and a Rating, then strategic advice, and it explicitly asks the model not to mistake a presentation problem for a method flaw. No license file was found.

ARIS and Anti-Autoresearch also carry Chinese cues: 值得注意的是 ("it is worth noting that"), 意义在于 ("the significance lies in"), 本文并不声称 ("this paper does not claim"), 这并不意味着 ("this does not mean"), 目的不是...而是 ("the goal is not... but..."). lensback's work-log cues include 经过多次尝试 ("after many attempts"), 我们先 ("we first"), 后来 ("later") and 最终 ("finally").

## 3. Merged, de-duplicated catalog of AI-writing tells

Source codes: BH blader/humanizer · SS stop-slop · AV avoid-ai-writing · AG ashgreat/humanizer (measured) · CB cbsteh/anti-ai-writing · BW brandonwise · DS de-slop · PW plain-writing · JA anti-ai-slop-writing · KD anti-defensive-writing · LB lensback · YS YSLAB · OR Orchestra · AR ARIS · AA Anti-Autoresearch · IM Imbad0202 · LY Leey21 · SP slop-forensics/antislop · SK Sakana human reviews · MC Master-cai · WG write-with-ai.

"Strength" summarizes what the sources say: S means strong on one sighting, M means it needs a cluster, W means weak alone or contested.

### 3.1 Words (single tokens)

| Group | Items | Sources | Strength / note |
|---|---|---|---|
| Core AI lexicon | delve, tapestry, testament, underscore(s) (verb), pivotal, intricate/intricacies, meticulous(ly), vibrant, realm, landscape (figurative), interplay, showcase/showcasing, garner, bolster(ed), enduring, crucial | BH, AV, BW, JA, CB, AG, AR, LY, IM, PW, SP | S in clusters. Era-dependent: delve and tapestry are GPT-4-era; showcasing, highlighting, emphasizing and enhance are later (JA) |
| Inflated Latinate verbs | utilize, employ, leverage, facilitate, elucidate, encompass, endeavor, ascertain, commence, demonstrate (where "show" fits), reveal, assess, enhance, foster, harness, navigate, streamline, empower, spearhead, catalyze, cultivate, illuminate, augment, operationalize | AG (measured), AV (1B and Tier 2), BW, LY, JA, CB | M. AV: 1B items are "clarity, not authorship evidence". AG: utilize 5-10x |
| Boosters / evaluative adjectives | comprehensive, robust, crucial, essential, critical, vital, compelling, multifaceted, nuanced, holistic, seamless, cutting-edge, groundbreaking, transformative, unprecedented, remarkable, paramount, cornerstone, actionable, impactful, profound, invaluable, significant (non-statistical) | AG, AV, BW, CB, IM, JA, YS | M. CB: keep technical senses (robust estimator, statistically significant). AG: never stack two; never pair a booster with "significant" |
| Stance / transition adverbs (sentence-initial) | Additionally, Notably, Importantly, Moreover, Furthermore, Interestingly, Remarkably, Crucially, Clearly, Evidently, Ultimately, Fundamentally, Essentially, Specifically, Particularly, Consistently, Indeed, Overall, Intriguingly, Noteworthy | AG (additionally z 5.2, 5.4x; notably 6.2x), AV, BW, CB, SS, JA, AR, YS | S for additionally and notably in academic prose (AG). YS: allow only for real logical links |
| Intensifiers / filler | genuinely, truly, really, actually, simply, deeply, quietly, very, quite, basically, literally, honestly | SS, AV, OR (Perez), PW, DS | M. AV: keep "actually" when it marks a real correction |
| Copula substitutes | serves as, stands as, functions as, represents, marks, boasts, features, offers, presents, constitutes, is characterized by, hinges on | BH, AV, AG (copulas 0.79x of human), BW, DS | M. Restore is/are/has |
| Possessive avoidance and "of" chains | "the performance of X" everywhere; LLM strips apostrophe-s | AG (human uses consumers' etc.) vs. LY (prefers "of" over METHOD's) | Contested |
| Human-leaning words (missing in AI text) | we, find, is, thus, because, effect, shows, might, vs., use, help, different | AG | Absence is a signal: LLM text under-uses "we find" and "thus" |
| Vague quantifiers | many, several, various, numerous, a wide variety of, a number of, myriad, plethora | CB, AV, DS, YS | M. Replace with a count or a citation |
| Lazy extremes | every, always, never, all, nobody | SS, CB | W. A falsifiability trap in science |
| Jargon coinage | undefined internal codenames ("Experiment Set Gamma"), invented hyphenated compounds, term-stuffing | AA, PW, AV | M, high false-positive risk |

### 3.2 Phrases

| Group | Examples | Sources |
|---|---|---|
| Throat-clearing / meta openers | It is important to note that; It is worth noting/mentioning that; It should be noted that; It goes without saying; Here's the thing; Here's what...; The truth is; It turns out; Let me be clear; Let's dive in/explore/break this down; Without further ado; In today's [fast-paced/rapidly evolving] world; In the realm of; When it comes to; At the end of the day | BH, SS, AV, BW, CB, JA, IM, AR, LY, DS |
| Significance inflation | plays a crucial/pivotal/vital/key role (in shaping); marking a pivotal moment; stands as a testament to; underscores the importance of; reflects a broader; setting the stage for; indelible mark; evolving landscape; serves as a powerful reminder; extends far beyond | BH, AV, BW, SP (top essay trigrams), CB |
| Academic AI frames | our findings indicate/reveal/demonstrate that; our analysis reveals; these findings suggest; this study aims to; the results underscore the importance of; this enhances our understanding of; a growing body of literature suggests; the findings have important implications for; compared to; as a result; to address this | AG (measured bigrams), CB |
| Empty conclusions | More research is needed; future work should explore; the future looks bright; only time will tell; In conclusion / In summary (0 occurrences in AG's human text); sheds new light on; this pioneering study | CB, AG, AV, BH, BW, AR |
| Vague attribution | experts believe; studies show; research suggests; the literature suggests (no citation); observers have cited; industry reports | BH, AV, BW, CB |
| Chatbot residue / pipeline artifacts | I hope this helps; Certainly!; Great question; Let me know if; as an AI language model; as of my last knowledge update; regenerate response; [INSERT X]; <your text here>; TODO: cite; [citation needed]; lorem ipsum; `citeturn0search0`, `contentReference[oaicite:0]`, `utm_source=chatgpt.com` | BH, AV, BW, AA (deterministic, low FP), JA |
| Knowledge-gap guessing | while specific details are limited; not widely documented; likely [grew up/began]; it is believed that; appears to have | BH, AV |
| Defensive hedges | we do not claim; this paper does not; this is not to say; this does not mean/imply; our goal is not X but Y; rather than arguing X; we do not address X ("instruction confession"); although this study has limitations; Of course, this does not fully capture; To be clear | KD, AA (deterministic screen), LB (D2), AR, BH (§5 arguing with no one) |
| Stacked hedges | could potentially; may possibly suggest; might arguably; may eventually; might ultimately | BH, AV, CB, DS, LB (D3: two hedges within 72 characters), KD |
| Self-deprecation / work-log | unfortunately; merely; falls short; fails to; we first tried; initially; after several attempts; eventually found | LB (D1, D4) |
| Template slot-fills | a [adj] step towards [adj] [noun]; Whether you're X or Y; from X to Y (false range); Imagine a world where; the intersection of X and Y; the integration of X with Y | AV, BW, JA |
| Aphorism formulas | X is the language/currency/architecture of Y; X becomes a trap; X is not a tool but a mirror; the real question is; at its core; the heart of the matter | BH, AV, SS |
| Generic ML openings | "Large language models have achieved remarkable success"; "In recent years, deep learning has..."; "Transformers have revolutionized AI" | OR, AR, WG |

### 3.3 Punctuation and typography

| Tell | Sources | Note |
|---|---|---|
| Em dashes (—, spaced —, `--`) | BH, SS, AV, AG (6.3x measured), CB, PW, LY, YS, IM, AA (clichéd em dash), DS (em-dash theatrics) | The most cited tell. AV disagrees with using it as an authorship signal (model-dependent). AG and BH treat one dash as weak and a flood as strong. Keep en dashes for ranges (AG: humans use more en dashes) |
| Bold as decoration, bold inline headers ("**Performance:** Performance improved...") | BH, AV, BW, LY (no bold or italics in body), AA (BOLD-MODULE-SPAM) | S in papers |
| Bullet-list overuse; sequential logic flattened into bullets; bullets of bare noun phrases | AV, AA, LY (严禁列表化, "lists strictly forbidden"), YS, PW | S in papers (LY: never turn paragraphs into items) |
| Title Case headings; emoji; arrows (→); horizontal rules between every section | BH, AV, BW, PW | W for LaTeX papers |
| Curly quotes in plain text | BH, AV, BW, PW | W. Most editors auto-curl |
| Colons gluing clauses; colon into a triple ("ports, processes, and local state") | AV, PW, IM | M |
| Semicolon overuse | AG (1.26x, weak), AA, IM | W |
| Hyphen misuse (hyphen kept predicatively, stacked compound modifiers) | BH, AV, CB | W |
| Contractions in formal academic text | LY (forbidden) vs. PW (allowed) | Venue-dependent |

### 3.4 Sentence-level structures

| Tell | Sources | Note |
|---|---|---|
| "Not X but Y" / "not just X, but (also) Y" / "It's not X, it's Y" / split across sentences / clipped tail ("..., no guessing") | BH (§1 strongest), SS, AV, CB, DS, PW, JA, SP (regex), AA, KD | S. Keep a contrast when the negative half corrects a real belief or is a substantive finding ("driven by temperature, not water stress", CB) |
| Negative listing ("Not A. Not B. C.") | SS, AV, CB, DS | S |
| Stranded auxiliary contrast ("The tool died; the data didn't.") | AV | M |
| Invented contrast-pair mirroring ("false precision rather than genuine accuracy") | AV | M |
| False concession ("While X is impressive, Y remains a challenge") | AV, BW | M |
| Forced triads (three adjectives, three examples, colon into three) | BH, SS, AV, BW, DS, IM | Contested. AG measured no difference (2.8 vs. 3.0 per 1k) in academic text; act only when padded |
| Shallow -ing riders ("..., highlighting/underscoring/reflecting/ensuring/fostering...") | BH, AV, BW, JA | S |
| Vague association (associated with, linked to, in connection with) | BH | M. Science also uses "associated with" correctly for correlation (CB) |
| False agency / anthropomorphism ("the data tells us", "the study aims to prove", "the decision emerges") | SS, AV, PW, CB | CB: keep metonymy ("Figure 2 shows", "the model predicts") |
| Transformation chain ("X becomes Y. Y becomes Z."; "stops being X and starts being Y") | DS, SS, AV | S |
| Rhetorical questions (openers, stacked) | SS, AV, DS, PW | S in papers |
| Wh- openers / "This" or "We" starting consecutive sentences / vague demonstrative "This" | SS, AR, OR (Perez), PW | M |
| Same-opener runs (3+ sentences starting with the same word) | BH, AV | M. Exempt deliberate anaphora |
| Synonym cycling / elegant variation for technical terms | AV, BW, YS, AR (Banana Rule), IM, OR | S in papers |
| Nominalizations ("performed an analysis of", "provides an estimation of") | CB, AG, YS, AR, OR (Gopen & Swan) | M (also a human habit) |
| Expletives ("There are X that...", "It is X that...") | CB | W. Keep "It was found that" |
| Epistemic overreach (demonstrate or prove where suggest fits; causal verbs on correlational data; "significant" without a test) | CB, YS, KW, OR (rigor-reviewer), AA (CAUSAL-EVIDENCE-LEAP, SCOPE-INFLATE), AR | S. The highest-value academic tell |
| Distanced reporting ("our findings indicate that" instead of "we find that") | AG | S in academic text (measured) |
| Clause-then-formula wall; gratuitous pseudocode restating prose | AA | M, high false positives |

### 3.5 Paragraph and document-level structures

| Tell | Sources | Note |
|---|---|---|
| Over-split paragraphs (2.5x more paragraphs at equal word count) | AG (measured) | S |
| Uniform paragraph length / mirror structure (topic sentence, 3 points, synthesis, everywhere); every paragraph runs problem, method, benefit, summary | AV, IM, AR | M |
| Metronomic sentence rhythm (low SD, few short and few long sentences, low burstiness) | AG (SD 10.1 vs. 12.3), BW (burstiness), SS, CB | M. Do not fix by chopping into fragments (AV "never inject staccato") |
| One-line closers and dramatic fragments; quotable pull-quote endings; "Let that sink in" | BH (§2), SS, AV | S in essays, rarer in papers |
| Heading restated in the first sentence | BH | M |
| Roadmap / meta-announcement ("In this section, we examine..."; "The following paragraph...") | AG, BH (§25), IM, SS | Contested. IM keeps intro roadmaps; OR recommends signposting; AG cuts them |
| Restatement loop / argument echoing / treadmill (each paragraph restates the premise) | AA (RESTATE-OVERCLAIM), YS, AV, WG | S |
| Paragraph-reshuffle immunity (paragraphs swappable, no argument) | AV, MC (reverse outline), AR | S. A structural test |
| Narrative-arc break (abrupt 1-2 paragraph intro; abstract as log dump; no background, contribution, evidence arc) | AA, OR, WG | M |
| Focus drift (motivation pivots to a minor implementation detail) | AA | M |
| Hollow paragraphs (no claim; removal loses nothing) | DS, BH, YS ("verify sentence purpose") | S, judgment only |
| Defensive caveats in high-impact positions (abstract, topic sentences, contributions) | KD, LB, AR | S |
| Formulaic "Challenges and Future Outlook" sections | BH, AV | M |
| Appendix as dumping ground; duplicate tables or figures; page padding; too few figures for the claimed scope | AA, SK | M (SK: duplicates observed in real AI papers) |
| Single-style generated figures; decorative figures | AA, SK | W |
| Prose re-describing what a figure or table already shows | WG, OR | M |

### 3.6 Substance-level tells (for the evidence list and review screening)

These recur in the academic and review repos, and the Sakana human reviews observed them in real unsteered AI papers.

1. Hallucinated or wrong-context citations: nonexistent papers, wrong authors or year, DOI pointing elsewhere, a real paper cited for a claim it does not make, a textbook instead of the primary source, unresolved "(?)" (CB, OR, AR, AA-E, refchecker, SK).
2. Results described but not shown, or methods described but never run (planned-vs-executed drift) (SK: temperature scaling, domain adaptation, multi-dataset; Imbad0202 provenance gate; AA PHANTOM-RESULT and DEAD-METRIC).
3. Captions that contradict the figure; text that contradicts a table or figure; appendix that contradicts the main text (SK, AA-A, Sakana VLM review).
4. Headline number above the table value; wrong delta arithmetic; best run reported as a mean; denominator drift; GRIM, GRIMMER and statcheck impossibilities (AA-A, AR claim-audit, YS percentage denominators).
5. Overclaiming scope or causality relative to the design: "robust/generalizes" from one synthetic task (SK, OR rigor D1/D3, CB, KW).
6. Missing or weak baselines; "outperforms" without variance; single-run results (AA-C, OR D6, MC).
7. Evaluation leakage (SK: about 57% train-test overlap; AA EVAL-LEAKAGE); unvalidated LLM-judge metrics (AA JUDGE-VALIDITY).
8. Suspiciously regular numbers: constant offsets, identical decimals (AA SUSPICIOUS-REGULARITY, advisory unless code is available).
9. Trivial findings framed as contributions (a learning-rate sweep presented as insight); trivial "A+B+C" combinations (SK, AA advisory, MC "insufficient contribution").
10. Related work that dismisses or omits the community's work; a bibliography dump instead of an argument (SK, WG, OR).
11. No dead ends documented; post-hoc narrative; "a tree with zero dead-ends is suspicious" (OR rigor D5). The inverse, work-log narration, is a separate tell (LB D4).
12. Defensive hedging clustered outside Limitations (AA hedge screen thresholds, KD, AR).

## 4. Where the sources disagree (decide explicitly in our skills)

- **Passive voice.** SS says never; BH treats it as weak alone. CB, AR, YS and IM say procedural passive is standard in science. Decision for papers: keep methods passives and flag only interpretive claims that hide their agent (CB §9).
- **Em dash as an authorship signal.** AG measured 6.3x and BH/SS/LY ban dashes. AV says the rate varies by model and vendor, so "do not score it as an authorship signal". Decision: treat it as a style fix in (b) and a weak, model-era-dependent feature in (c).
- **Rule of three.** Most blog skills flag it. AG's academic corpus shows no difference. Decision: act only on padded triads.
- **Signposting and roadmaps.** OR and IM keep them. AG, BH and SS cut them. Decision: keep one intro roadmap; cut "In this section we..." at every section start.
- **Hedging.** OR (Lipton) says drop may/can unless uncertain. KD, LB and AR say remove defensive hedges but keep scope conditions. CB says keep the single hedge that names its uncertainty source. All agree that stacked hedges are bad.
- **Transitions.** BH/AV/JA ban Moreover/Furthermore/Additionally. AG says keep "thus/therefore" (human-favored) and downgrade the rest. YS allows them when the logical relation is real.
- **Short vs. long sentences.** SS and BH want varied rhythm. PW prefers long explanatory sentences. AG says humans have more of both extremes. Decision: fix variance, not length.
- **Possessives.** LY says avoid "METHOD's"; AG says human text has more apostrophe-s. This is venue taste.
- **Authorship classification.** zhu-minjun AIDetector, Binoculars and Ghostbuster output probabilities. AA, AV, CB and IM refuse authorship verdicts because of false positives (more than 60% on non-native writers) and paraphrase fragility.

## 5. Skill-design patterns worth absorbing

1. **Rank tells by strength and require clusters** (BH strongest-first numbering plus "weak alone"; AV P0/P1/P2 and Tier 1/2/3 with density thresholds; AG "look for clusters"). Our (c) skill should score clusters and families, not single words.
2. **Separate style from integrity and give style zero or low verdict weight** (AA's quarantined AIS track; AV 1A vs. 1B; IM "not a humanizer"). In (c), report style impressions separately from substantive findings, and base the "unsteered AI" estimate mainly on substance tells (§3.6).
3. **Editing contract and fidelity** (AV: candidate, then finding, then edit; protected regions; source as data; "never inject"; DS "flag hollow, don't fabricate"; YS "missing support does not justify substituting a weaker claim"; LB claim-ceiling contract and three-part regression test; AR "tone fixes must never alter facts, negation, modality, scope, comparison direction, or numbers").
4. **No-op threshold** (LY 宁缺毋滥 and "[检测通过]"; AV clean no-op with 0 passes; DS idempotent). This prevents over-editing, the main way humanizers create a new fingerprint.
5. **Modes** (AV rewrite/detect/edit; YS revision/review; BH pasted/file/embedded). Output formats: final text plus a short "what still reads as AI" list plus a change log (BH, AG); a verification block (AV: passes, checks run, residuals, stop reason); a "Needs Verification" list (YS); a claim-evidence map (MC); KEEP/FIX/REPLACE/REMOVE for citations (AR); severity, location and fix per issue (AR reviewer prompt).
6. **Draft, then audit, then final** loop with "re-check the tells that most often survive a rewrite" (BH) and at most 2-3 passes (AV, DS).
7. **Deterministic pre-pass with candidate-only semantics** (AA `check_ai_style.py` thresholds; AV detector; DS `flag_slop.py`; LB `scan_defensive_cues.py`; AG `detect_ai.py`). Every one states that a regex hit is a candidate, not a verdict.
8. **Measured baselines** (AG's per-1k table; AV's human-control false-positive rate at threshold 6 = 1.9%; slop-forensics per-domain lists; EQ-bench slop index). The (c) skill needs a human baseline (pre-2023 ML papers) to calibrate thresholds.
9. **Academic-specific substance passes**: epistemic verb ladder (CB); type-aware claim-evidence entailment (OR rigor D1); reverse outline (MC, AR); keyword consistency (AR Banana Rule); numeric cross-checks (AR, YS, AA-A); citation verification pipeline (OR, refchecker, AR).
10. **Voice sample override** (BH, AG): if the author gives prior papers, match their rates (including dashes and first person) over the defaults.

## 6. Weaknesses and gaps across the ecosystem

- Most anti-slop skills are tuned for blogs, LinkedIn or Wikipedia. Only AG (one marketing corpus), CB (soil science, 1 star) and the IM, AR and LY checklists target papers, and none measures ML papers specifically. Opportunity: measure tells on pre-2023 vs. 2025-26 ML papers (arXiv/OpenReview) the way AG and SP did.
- Word lists decay with model generations (JA's eras; BH: "word habits change with every model release"). Skills should lead with structure and substance.
- Humanizers can install a new fingerprint (AV on blader). Guardrails against injection are essential.
- Almost no skill addresses human-steering evidence directly. The closest are Imbad0202's experiment-provenance gate (planned_vs_executed, negative_results), OR rigor D5 (dead ends), and Sakana's code reviews showing plan-vs-execution drift. These should anchor skill (c).
- Detector repos give probabilities with documented fragility. No open repo for Pangram or GPTZero exists to inspect.
- License caveats: Leey21, jalaalrd, EQ-bench creative-writing-bench, openreviewer and the Sakana workshop repo show no license file in the clone. AI-Scientist uses a RAIL-derived source license. Quote or paraphrase only; do not copy wholesale.

## 7. Files

- This report: `research/D_github_skills.md`
- Raw skill texts: `research/raw/*.md` (blader_humanizer, hardikpandya_stop-slop, conorbronsdon_avoid-ai-writing (SKILL plus 107 KB patterns), ashgreat_humanizer (SKILL, measured-signals, examples, taxonomy), cbsteh_anti-ai-writing, brandonwise_humanizer, isatimur_de-slop, welttowelt_stop-slop-refined, Kiterlin_anti-defensive-writing, shreyashankar_plain-writing-skill, jalaalrd_anti-ai-slop-writing, Orchestra_ml-paper-writing (plus rigor-reviewer), K-Dense_scientific-writer, YSLAB_manuscript-writing, write-with-ai_paper-writing-guide, lensback940701_evidence-bound-revision, Master-cai_Research-Paper-Writing-Skills, Leey21_awesome-ai-research-writing, Imbad0202_writing_quality_check, ARIS_paper-write_and_audits, Anti-Autoresearch (taxonomy, AIS skill, check scripts), SakanaAI_reviewer_prompts, SakanaAI_ICLR2025_human_reviews_of_AI_papers, openreviewer_prompt, sam-paech_slop_lists, sam-paech_essays_slop_phrases_top.jsonl, refchecker_README)
- Full clones (for deeper reading): `scratchpad/repos/`
