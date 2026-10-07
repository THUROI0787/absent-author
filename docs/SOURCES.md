# 来源登记（Sources）

> v0.2.1 · 2026-10-05（已根据事实核查 agent 的 62 项核对修正；v0.2.1 补充了内部来源键和若干吸收内容）。EVIDENCE.md、POSITIONING.md 和两个 skill 里引用的来源键都在这里。
> 原始调研笔记（含逐条引文和核实标记）放在 [`research_notes/`](research_notes/)：A 英文社媒、B 中文平台、C 学术文献、D GitHub skills、E 管线指纹。

**核实标记**：
- **V**：本次调研抓取过原文，引文或数字可以在原文中找到（WebFetch 返回的是模型摘录，正式引用前请再核对一次原文措辞）。
- **V-git**：克隆了仓库，读的是原文件。
- **S**：只看到搜索结果的标题或摘要，原页面打不开。
- **U**：未核实，或者是二手转述。
- **★**：来自作者之一 Zhehao Zou 的前期调研材料。本次复核过的已标 V，未复核的保留原标记。

**来源类型权重**：会议官方政策或博客 > 同行评审论文 > 预印本 > 审稿人或编辑的实名博客 > 匿名社交帖子（只算"读者观察"）。

---

## 1. 会议与出版方官方材料

| 键 | 来源 | 要点 | 核实 |
|---|---|---|---|
| `[ICLR27-blog]` | ICLR 2027 PCs, "Submission policies for ICLR 2027", https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/ | "paper-shaped objects"；"current AI systems seem to have poor taste in research questions"；每位作者最多 20 篇 | V |
| `[ICLR27-60k]` | 36氪 https://eu.36kr.com/en/p/3920743531228550 ；KuCoin 快讯 https://www.kucoin.com/news/flash/iclr-2027-submissions-surpass-60-000-breaking-previous-records | ICLR 2027 摘要注册超过 6 万篇（**非官方数字**；摘要注册数不等于有效投稿数） | V（二手） |
| `[ICLR27-policy]` | https://iclr.cc/Conferences/2027/AIPolicyForAuthors （另有 …/AIPolicyForReviewers） | 作者必须附 AI 使用声明（不计页数）：合成数据、理论与框架、数学主张、方法、实现、结果解读、证明**必须**披露，代码、图、文献工作、头脑风暴、起草、参考文献格式**建议**披露（见 research_notes/C §6）；LLM 产生的虚假内容属于伦理违规，可 desk reject；**使用了 LLM 的**审稿人须披露其交互 | V |
| `[CMSA26]` | https://cmsa.fas.harvard.edu/media/2026/09/Summit-on-PhD-Math-Education-in-the-Age-of-AI.pdf （峰会页面 https://cmsa.fas.harvard.edu/aimathphd_summit/ ，2026-09-17/18） | Harvard CMSA "Summit on PhD Math Education in the Age of AI" 报告：“AI use should accelerate understanding, not bypass understanding”；“maintain responsibility for the correctness and understanding of the mathematics that appears under your name”；“always disclose AI use”；“A PhD should not be awarded primarily on the basis of the text of the dissertation”；“A rigorous thesis defense that requires complete mastery of the thesis content”。网站、README 和 POSITIONING §9 的"三个问题"（你是否透彻理解它？你敢当面捍卫它吗？你愿意以自己的名字为它背书吗？）改写自中文媒体对该峰会的评论（例如 https://baijiahao.baidu.com/s?id=1877836085213224669 ），不是报告原文 | V |
| `[ICLR27-CfP]` | https://iclr.cc/Conferences/2027/CallForPapers | 论文应体现 "significantly more work than … can be produced autonomously by any current AI agent" | V |
| `[ICLR26-resp]` | https://blog.iclr.cc/2025/11/19/iclr-2026-response-to-llm-generated-papers-and-reviews/ | 大量未披露的 LLM 使用可导致 desk reject；幻觉审稿违反伦理守则 | V |
| `[ICLR26-retro]` | "A Retrospective on the ICLR 2026 Review Process"，https://blog.iclr.cc/2026/03/31/a-retrospective-on-the-iclr-2026-review-process/ | 19,525 篇有效投稿，779 篇 desk reject；**凡确认含幻觉引用的论文全部 desk reject** | V |
| `[COLM26]` | Greg Durrett 等（COLM 2026 PCs），"AI submissions at COLM: theoryslop, slopterpretability, and papers in the age of agents"，https://gregdurrett.github.io/colm2026-blog/ai-papers.html | 提出 theoryslop、slopterpretability；约 5% 的论文高度 AI 生成；AI 分数最高的 50 篇中 0 篇被推荐接收（初步统计，"do not reflect final PC decisions"；注意这是按检测器分数挑出来的）；"human-vouched contribution" 原则；没有一篇论文仅凭检测器结果被 desk reject | V |
| `[NeurIPS26-PP]` | https://blog.neurips.cc/2026/06/02/ai-generated-papers-in-the-neurips-2026-position-paper-track/ | 用 Pangram 筛查，178 篇（18.4%）被 desk reject；"externalises the cost of verifying that work"；接受版本历史作为人类参与的申诉证据 | V |
| `[NeurIPS26-PP-backlash]` | Startup Fortune，https://startupfortune.com/neurips-is-facing-backlash-over-ai-detector-desk-rejections/ | 检测器在没有验证其在该人群上的误报率的情况下当了守门人 | V |
| `[ICML26]` | https://blog.icml.cc/2026/03/18/on-violations-of-llm-review-policies/ | 用 PDF 隐藏水印抓到 506 名审稿人的 795 份违规审稿（这些审稿人此前同意了 Policy A，即不用 LLM），关联的 497 篇投稿被 desk reject | V |
| `[TMLR26]` | TMLR EiCs，"Asking authors about their own papers"，https://medium.com/@TmlrOrg/asking-authors-about-their-own-papers-3d2e04e5dee0 | desk reject 率从约 6% 涨到约 53%（不全是 AI 造成的）；抽查 10 篇、其中 7 篇的作者接受了问答，3 篇（均为单作者）答不上关于自己论文的基本问题；由一位 EiC 撰写 | V |
| `[AISTATS27]` | https://virtual.aistats.org/Conferences/2027/SubmissionFAQ | 缺少 AI 使用声明即 desk reject；把不清楚、填充式的写作列为质量问题 | V（页面是 FAQ 而非 CfP）★ |
| `[arXiv-ban]` | 404 Media，https://www.404media.co/new-arxiv-rules-ai-generated-papers-ban/ | 含有确凿未核查 LLM 输出（幻觉引用、元评论）的投稿，封禁 1 年 | V |
| `[arXiv-survey]` | 404 Media，https://www.404media.co/arxiv-changes-rules-after-getting-spammed-with-ai-generated-research-papers/ | 综述"little more than annotated bibliographies" | V |
| `[arXiv-mod26]` | Unite.AI 引述 arXiv 博客（2026-10-01），https://www.unite.ai/fighting-ai-slop-in-science-papers/ | "thin papers of narrow scope"，"salami papers" | V（二手） |
| `[Wiley-FAQ]` | https://www.wiley.com/en-be/publish/editor-insights/editor-faqs-ai-researcher-guidelines/ | 语气突变、tortured phrases、不真实引用 | ★（未复核） |
| `[SAGE25]` | https://www.sagepub.com/explore-our-content/blogs/posts/sage-perspectives/2025/06/11/ai-detection-for-peer-reviewers-look-out-for-red-flags | 复述、过度解释、刻板的段落模板、图注和图不符 | V |
| `[Nature-artifacts]` | https://www.nature.com/articles/d41586-025-01180-2 | 已发表论文中出现聊天残留 | ★（未复核） |
| `[Nature-injection]` | https://www.nature.com/articles/d41586-025-02172-y | arXiv 论文中藏有给 LLM 审稿人的提示注入 | S |

## 2. 研究论文与报告

| 键 | 文献 | 要点 | 核实 |
|---|---|---|---|
| `[Kobak25]` | Kobak et al., *Science Advances* 11(27), 2025, doi:10.1126/sciadv.adt3813 | 2024 年 PubMed 摘要中至少 13.5% 经过 LLM 处理；delves 是预期频率的 28 倍，underscores 13.8 倍，showcasing 10.7 倍（v5 版本）；增多的词 66% 是动词 | V |
| `[Liang24a]` | Liang et al., "Mapping the Increasing Use of LLMs in Scientific Papers", COLM 2024, arXiv:2404.01268 | CS 摘要中 17.5% 的句子被 LLM 修改过；realm / intricate / showcasing / pivotal | V |
| `[Liang24b]` | Liang et al., "Monitoring AI-Modified Content at Scale", ICML 2024, arXiv:2403.07183 | 审稿意见中 6.5–16.9% 被 LLM 修改；"meticulous" 34.7 倍 | V |
| `[Juzek25]` | Juzek & Ward, "Why Does ChatGPT 'Delve' So Much?", COLING 2025, https://aclanthology.org/2025.coling-main.426 | 21 个过度使用的词，delves 增长 6697%；原因指向 RLHF | V ★ |
| `[Kousha25]` | Kousha & Thelwall, arXiv:2509.09596 | underscore 与 pivotal 的共现相关从 0.03 升到 0.45 | V |
| `[GengTrotta]` | Geng & Trotta, arXiv:2404.08627；Findings of ACL 2025 (657) | CS 摘要中 is/are 下降 14–17%；"delve" 在 2024 年后被刻意回避，说明词表会过时 | V |
| `[Czuma26]` | Czuma, arXiv:2606.29540（预注册） | medRxiv Discussion 部分含破折号的比例：ChatGPT 之前 4.23%，之后 11.58%；按年份 2023 年约 4%，2024 年 8.0%，2025 年 20.3%；作者明确说这是"总体层面的指标，不是单篇检测器" | V |
| `[Pew26]` | Bestvater et al., "How Much of the Internet Is Written With AI?", Pew Research, 2026-08-20, https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/ | 2023→2026 年：破折号翻倍，"it's not just X, it's Y" 接近三倍 | V ★ |
| `[Liang23]` | Liang et al., "GPT detectors are biased against non-native English writers", *Patterns* 2023, arXiv:2304.02819 | 7 个检测器在非母语 TOEFL 作文上的平均误报率 61.22%（2023 年的检测器、作文而非论文） | V ★ |
| `[NAACL25-detect]` | Tufts, Zhao, Li, "A Practical Examination of AI-Generated Text Detectors", Findings of NAACL 2025, https://aclanthology.org/2025.findings-naacl.271/ | 误报率限制在 1% 时，有的检测器召回为 0% | V ★ |
| `[Hadan24]` | Hadan et al., "The great AI witch hunt", *Computers in Human Behavior: Artificial Humans* 2(2), doi:10.1016/j.chbah.2024.100095 | 17 位 HCI 审稿人分不清 AI 文本和人类文本；他们给出的判断线索互相矛盾 | V ★ |
| `[SciSlop26]` | Oh et al., "Science or Slop?", arXiv:2610.00531（2026-09-30，未经同行评审） | 390 对 AI 与人类论文；六个指标：结构（跨节引用缺失 0.905、宏观冗余 0.723）、论证（引言关键主张缺乏铺垫 0.586、引用孤立 0.793）、产物（方法图塞入无关内容 0.809、有结果表却没有任何具体实例 0.764）；综合 0.859，Binoculars 0.687；"direct slop-aware prompting" 会导致 reward hacking | V ★ |
| `[Beel25]` | Beel et al., arXiv:2502.14297 | AI Scientist：42% 的实验失败；引用数中位数为 5 且大多过时；占位符文本；幻觉数字；把已有方法当成新方法 | V |
| `[Luo25]` | Luo, Kasirzadeh, Shah, "The More You Automate, the Less You See", arXiv:2509.08713 | 基准选择、泄漏、指标误用、事后选择偏差四类陷阱；只看论文的审计准确率 55%，加上日志和代码后 82% | V |
| `[Si25]` | Si, Hashimoto, Yang, "The Ideation-Execution Gap", arXiv:2506.20803 | LLM 提出的想法在执行之后得分下降得更多，排序发生反转 | V |
| `[Gupta25]` | Gupta & Pruthi, "All That Glitters is Not Novel", ACL 2025, arXiv:2502.16487 | 24% 的 AI 研究文档存在 idea 剽窃，剽窃检测器没有发现 | V |
| `[A4S25]` | Bianchi et al., "Exploring the use of AI authors and reviewers at Agents4Science", arXiv:2511.15534 | 约 56% 的投稿至少有一条可疑引用；过度宣称；"technically correct but … lacking creativity" | V |
| `[Yamada26]` | Yamada, Lange, Lu et al., arXiv:2606.15497 | AI Scientist 自述的失败模式：图在正文和附录中重复、引用不准确 | V |
| `[BadScientist25]` | Jiang et al., "BadScientist", arXiv:2510.18003 | 伪造的论文在 LLM 审稿下接收率最高达 82% | V |
| `[AIRev26]` | Yang, Sha, …, Liu, Wang, "No Hidden Prompts Needed! You Can Game AI Peer Review with Presentation-Only Revisions", arXiv:2606.13044 | "AI reviewers can confuse the appearance of addressing a limitation with actually resolving it"；只改表述的闭环对抗搜索平均提分 +1.21/10，攻击成功率 75.1% | V |
| `[HalluCite26]` | Sakai et al., "HalluCitation Matters", arXiv:2601.18724 | ACL 系列会议中含幻觉引用的论文从 20 篇（2024）增加到 275 篇（2025） | V |
| `[Topaz26]` | Topaz et al., arXiv:2609.14988 | 26 个 LLM 生成的生物医学参考文献中 55.4% 是编造的 | V ★ |
| `[Antislop25]` | Paech et al., "Antislop", arXiv:2510.15061 | 部分 slop 模式在 LLM 输出中的频率是人类文本的 1000 倍以上 | V |
| `[Cornell25]` | Kusumegi, Yin, Ginsparg et al. (*Science*)，https://www.news.cornell.edu/stories/2025/12/ai-gives-scientists-boost-cost-too-many-mediocre-papers | 对人类论文来说文字复杂度是正向的质量信号，对 LLM 辅助的论文则不是 | V |
| `[Sanger26]` | Sanger & Maurer, arXiv:2602.03864 | LLM 辅助的摘要：词汇多样性**更高**、对冲**更少**、语气更自信 | V |
| `[Pangram25]` | https://www.pangram.com/blog/pangram-predicts-21-of-iclr-reviews-are-ai-generated | ICLR 2026：21% 的审稿意见完全由 AI 生成，约 9% 的论文 AI 内容超过一半（"1%/199 篇完全由 AI 生成"只见于二手报道，原页写的是 "several hundred"）；论文的 AI 内容越多，得分越低 | V |
| `[GPTZero-NeurIPS]` | https://gptzero.me/news/neurips/ | 扫描 4,841 篇 NeurIPS 2025 已接收论文，51–53 篇中共确认 100 条幻觉引用 | V |
| `[GPTZero-ICLR]` | https://gptzero.me/news/iclr-2026/ | 抽样的 300 篇 ICLR 2026 投稿中，50 篇确认含幻觉引用 | V |
| `[WP-AISIGNS]` | Wikipedia: Signs of AI writing，https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing | 社区整理的观察目录，按模型时代给出 AI 词表；明确说这些只是描述性线索 | V ★ |

## 3. 审稿人、编辑、研究者的公开发言

| 键 | 来源 | 要点 | 核实 |
|---|---|---|---|
| `[Geospatial26]` | Robinson & Corley, "Q&A from the slop trenches", https://geospatialml.com/posts/reviewing-ai-slop/ （2026-07-30） | "It's not X, it's Y"、粗体和破折号；正文数字和表格对不上；幻觉作者名；"Claude freaking loves to condense all possible numbers"；22 篇里有 15 篇有问题 | V |
| `[Buschek25]` | Daniel Buschek, "When LLMs Write Our Papers", https://dbuschek.medium.com/when-llms-write-our-papers-1cc746373cd0 | 营销词；引了文献但不是最相关的；误述被引论文；结果总结超出结果 | V |
| `[DailyNous25]` | Ohlhorst, Daily Nous, https://dailynous.com/2025/10/28/reviewing-an-llm-written-paper-guest-post/ | "wading through cotton candy"；核心概念始终没有说清 | V |
| `[DailyNous26]` | Daily Nous, https://dailynous.com/2026/07/24/if-you-think-youre-refereeing-an-ai-written-submission-what-should-you-do/ | 形式化搭起来却从不使用（Easwaran）；句子只是一串术语（Harman）；看起来像 AI 写的论文通常还有别的实质问题（Greco） | V |
| `[Oppenheim25]` | Jonathan Oppenheim, "We are in the era of Science Slop", https://superposer.substack.com/p/we-are-in-the-era-of-science-slop | 假新颖："the form of scholarship without the substance" | V |
| `[Cook-TC25]` | TechCrunch 引述 Mike Cook（KCL），https://techcrunch.com/2025/03/12/sakana-claims-its-ai-paper-passed-peer-review-but-its-a-bit-more-nuanced-than-that | "it's arguably easier to get an AI to write about a failure convincingly" | V |
| `[RG-emdash]` | ResearchGate 讨论，https://www.researchgate.net/post/Is_the_frequent_use_of_em-dashes_becoming_a_false_positive_for_AI-generated_text_in_academic_peer_review | 反对意见：如果为了躲避检测而回避破折号，学术写作会变得更扁平 | V |
| `[HN-cge]` | https://news.ycombinator.com/item?id=49535005 | "reads like Claude writing up a lengthy report, down to the needless sectioning"；作者贡献声明与文本不符 | V |
| `[HN-loadbearing]` | https://news.ycombinator.com/item?id=49932739 | Claude 的口头禅 "load-bearing" | V |
| `[HN-SkyPuncher]` | https://news.ycombinator.com/item?id=49420009 | "terminology that's technically correct but practically meaningless" | V |
| `[HN-jsrozner]` | https://news.ycombinator.com/item?id=48981988 | ACL 审稿人：一篇 AI 剽窃 idea 的论文，文笔很好，被 desk reject | V |
| `[HN-Schwartz]` | https://news.ycombinator.com/item?id=49933593 | 一人短期内在多个不相关领域发表大量论文 | V |
| `[36kr-ICLR26]` | 36氪（2025-11-13），https://eu.36kr.com/zh/p/3551362253731718 | 亚马逊审稿人："充斥着未经定义的新术语、缺失引用"；"列表上一半的论文他花的时间比作者还多" | V |
| `[Luna26]` | 公众号"露娜读博历险记"《审稿人一眼就知道你用了AI：这5个痕迹，藏不住》（2026-10-03），通过转载读到：https://www.aboluowang.com/2026/1003/2440920.html | 太干净、段落等长、术语从头到尾一个说法、引用撒得太匀；**同时认为破折号和插入语反而是人味**，与其他来源冲突 | V（转载） |
| `[Huxiu-notXbutY]` | 虎嗅《「不是，而是」：AI写作留给文字世界的特洛伊木马》，https://m.huxiu.com/article/4890032.html | 否定对照句在企业文件中的使用频率翻倍 | V |
| `[XHS-origin]` | 用户提供的小红书截图：吐槽 ICLR 审稿遇到的 AI slop | 大量破折号、防御性写作、生造词、实验失败的"诚实披露"、方法不 work 降级为"审计"论文 | U（原帖未找到）。这是项目发起人的动机观察；它和 ARIS 文档记录的行为一致（见 `[ARIS-*]`），但注意是我们按这条线索去找的，不算独立证据 |
| `[ZH-Reddit-1rtll1h]` | https://www.reddit.com/r/AskAcademia/comments/1rtll1h/dealing_with_slop_as_a_reviewer/ | 审稿人从破折号和可疑引用出发，查出虚构文献 | ★（本次无法访问 Reddit） |
| `[ZH-Reddit-1t7o1ob]` | https://www.reddit.com/r/Professors/comments/1t7o1ob/peer_reviewing_a_probably_aigenerated_manuscript/ | 清单式文献综述、像提示词的段首短语、缺结果表、乱码图 | ★ |
| `[ZH-Reddit-sx3dk7]` | https://www.reddit.com/r/AskAcademia/comments/1sx3dk7/suspect_article_im_reviewing_is_written_with_ai/ | 聊天腔、punchy 短句、X 项后来变成 Y 项、标题误导 | ★ |
| `[ZH-Reddit-ooqify]` | https://www.reddit.com/r/AskAcademia/comments/1ooqify/academic_integrity_violations_from_ai_are_making/ | 相同的过渡语和句型 | ★ |
| `[ZH-Reddit-1wpvs22]` | https://www.reddit.com/r/academia/comments/1wpvs22/i_keep_getting_slop_to_review/ | 大量术语和自造指标 | ★ |

## 4. GitHub：auto-research 管线（用来提取"管线指纹"）

| 键 | 仓库 | 吸收了什么 | 核实 |
|---|---|---|---|
| `[ARIS]` | https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep （MIT） | 算力上限（PILOT_MAX_HOURS=2，先导实验合计 MAX_TOTAL_GPU_HOURS=8，DEFAULT_SEEDS=3，MAX_BASELINE_FAMILIES=3）；用 Gemini 生成插图；README 里展示 AI 审稿分数；`skills/research-pipeline/SKILL.md` 的停滞检测会触发 "forced structural pivot"（research_notes/E 第 32 行）；`citation-audit` 对每条引用给出 KEEP / FIX / REPLACE / REMOVE（research_notes/D 第 172 行） | V-git |
| `[ARIS-README-run]` | 同上，README §5 "Score Progression (Real Run)" 第 2–4 轮 | "Key claim failed to reproduce, pivoted narrative" → "Large seed study killed main improvement claim" → "Diagnostic evidence solidified, submission ready"（7.5/10）：这是 **R01 最直接的机制证据** | V-git |
| `[ARIS-xhs]` | 同上，`xhs_post.md`（官方小红书文案） | "核心claim翻车，转叙事 … 诊断证据确立，可投稿" | V-git |
| `[ARIS-review-loop]` | 同上，`skills/auto-review-loop/SKILL.md` | 达到 "score ≥ 6/10 AND verdict ∈ {ready, almost}" 即停止；"Prefer reframing/analysis over new experiments when both address the concern"；"Be honest — include negative results"；默认 HUMAN_CHECKPOINT=false | V-git |
| `[ARIS-paper-write]` | 同上，`skills/paper-write/SKILL.md`、`paper-plan`、`writing-principles.md` | Related work 至少一整页并用 `\paragraph{}` 分类；2–4 条 contribution 加一句 roadmap；删除 AI 词；Banana Rule（同一对象始终用同一个名字）；2026-09 加入 "Pick the contest the paper wins"、"deliberate tradeoff"；`<!-- DATA_NEEDED -->` | V-git |
| `[ARIS-PR423]` | 同上，commit `e9e51ff`（2026-08-26），"papers stop reading like confessions" | 引述社区用户反馈 "ARIS papers read like 忏悔书"，维护者承认 "The mechanics were ours."；"telling the model not to mention X produces 'we do not address X'"；"every criticism absorbed as a new hedge" | V-git |
| `[HERO]` | https://github.com/wanshuiyin/HERO-Anti-OverDefense | "agent 在优化不被追责，而不是活儿干得好"；"论文是发布会，不是工作汇报"；SIB-003（"reads as an apology for itself"） | V-git |
| `[Sakana-v1]` | https://github.com/SakanaAI/AI-Scientist （RAIL 许可，只引述不复制） | 模板数据集（shakespeare_char、2D moons/dino、grokking）；水印 "This work was generated by The AI Scientist"；每段前加 `%` 计划注释；Semantic Scholar 风格的 bib key（v0.2 起不算证据：这是 S2 自身的导出格式） | V-git |
| `[Sakana-v2]` | https://github.com/SakanaAI/AI-Scientist-v2 | num_seeds: 3；"THREE HuggingFace dataset"；默认 matplotlib 并且每个面板都有标题；正文和附录的图重复 | V-git |
| `[Sakana-ICBINB]` | https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment | Sakana 自己对 3 篇全 AI 论文的人工审查：幻影实验、计划与执行不符、图注和图矛盾、约 57% 训练/测试重叠、LSTM 引 Goodfellow 2016 | V-git |
| `[AgentLab]` | https://github.com/SamuelSchmidgall/AgentLaboratory | 正文行内写 "(arXiv 2308.11483v1)"；标题以 "Research Report:" 开头；"the paper MUST BE LONG" | V-git |
| `[HKUDS]` | https://github.com/HKUDS/AI-Researcher | 固定的实验章节骨架；3–4 条 contribution | V-git |
| `[CycleResearcher]` | https://github.com/zhu-minjun/Researcher | 只在代码 docstring 中找到 "generated by CycleResearcher"，模板里没有水印文字 | U（已从 EVIDENCE P05 和 lint 的 P05 检查中移除；仅记录，未引用） |
| `[DeepScientist]` | https://github.com/ResearAI/DeepScientist | "reviewer-question blocks"；5–10 组分析；附录按审稿人的关切组织 | V-git |
| `[autoresearch]` | https://github.com/karpathy/autoresearch | 5 分钟单卡运行；val_bpb 爬山 | V-git |
| `[Zochi]` | https://github.com/IntologyAI/Zochi | 单一 benchmark、单一模型尺寸；README 里自报 AI 审稿分数 | V-git |

## 5. GitHub：写作、审稿、检测 skill（吸收了什么、没吸收什么）

| 键 | 仓库 | 吸收进我们的内容 | 不足或注意 |
|---|---|---|---|
| `[AA]` | https://github.com/wanshuiyin/Anti-Autoresearch （MIT） | 文风不定罪的原则；防御性 hedge 的确定性阈值（≥4 句、≥2 节、不计 Limitations 和 Related Work）；46 个诚信模式（8 族）+ 13 条文风印象（零权重）；HP 诚信模式（增量算错、最好的 seed 冒充平均、范围虚夸、假 GT、幻影结果）；低误报的残留字符串列表 | 没有"品味 / 引导"这一层 |
| `[humanize-paper]` | https://github.com/SyntaxSmith/humanize-paper | "audit" 属于跨语域用词；实验代号泄漏进正文；结果按实验时间而不是论证角色组织；"A single `Moreover` or em dash is not a finding" | — |
| `[KD]` | https://github.com/Kiterlin/anti-defensive-writing （MIT） | Claim-forward；把 "we do not claim" 改成正面陈述适用范围；caveat 收拢到一处 | — |
| `[LB]` | https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill （MIT） | 修改前先写 claim-ceiling 契约；删除码 D1–D8 和保留码 K1–K4；回归测试 | 社科语境较重 |
| `[Zhehao-EBW]` | 作者之一 Zhehao Zou 的 `evidence-bound-paper-writing` skill（前期材料，未收入本仓库） | 感知风险和可核实缺陷分开写；不改动科学内容的契约；证据账本格式 | 立场很审慎，没有负面判定 |
| `[BH]` | https://github.com/blader/humanizer （MIT） | 按强度排序的模式表；"标出痕迹 → 起草 → 自问哪里还像 AI → 定稿"的循环 | 有独立测试发现它会装上自己的一套碎句式口吻 |
| `[AV]` | https://github.com/conorbronsdon/avoid-ai-writing （MIT） | 候选 → 发现 → 修改的三步；分级词表（1B 级属于啰嗦，**不是** AI 证据）；"never inject" 清单（不编造经历和立场，不刻意制造碎句）；在 376 篇 2023 年前的人类文档上做过误报校准 | 面向博客类文本 |
| `[AG]` | https://github.com/ashgreat/humanizer （MIT） | GitHub README 中作者自测的数据（营销学论文语料，**非同行评审**），但是我们找到的唯一对学术文本做过配对测量的来源：LLM 的破折号是人类的 6.3 倍，additionally 5.4 倍，notably 6.2 倍；句长标准差 10.1 对 12.3；三连结构在学术文本中**没有差异** | 语料是营销学论文 |
| `[CB]` | https://github.com/cbsteh/anti-ai-writing （MIT） | 优先级：引用真实性 > 主张与研究设计是否匹配 > 具体性 > 文风；动词阶梯 prove > demonstrate > show > indicate > suggest；保留程序性被动语态 | — |
| `[DS]` | https://github.com/isatimur/de-slop （MIT） | 区分"可改写"段落和"空心"段落（空心段落只标出，不替作者编内容）；最多 3 轮 | — |
| `[PW]` | https://github.com/shreyashankar/plain-writing-skill | 每条规则配 before/after；不造术语，不用花哨小标题 | — |
| `[Leey21]` | https://github.com/Leey21/awesome-ai-research-writing （**无许可证文件**，只引述） | 去 AI 味的 prompt；"宁缺毋滥"：没有问题就输出 [检测通过]；约 80 个 AI 词；"不要把表达问题误判成方法缺陷" | 禁用破折号和列表的规则过硬 |
| `[humanizer-zh]` | https://github.com/op7418/humanizer-zh | 31 类中文模式；"模式清单是检查线索，不是词语黑名单" | — |
| `[OR]` | https://github.com/Orchestra-Research/AI-Research-SKILLs （MIT） | rigor-reviewer：证据类型要匹配主张类型；"A tree with zero dead-ends or only trivial failures is suspicious"；从不凭记忆写 BibTeX | 其中 "Explain why limitations don't undermine core claims" 一条反而会制造 S16 |
| `[MC]` | https://github.com/Master-cai/Research-Paper-Writing-Skills （源自彭思达老师的笔记，MIT；项目文件夹中的 `Research-Paper-Writing-Skills-main.zip`（Master-cai 仓库的下载包）） | 反向大纲；`Claim | Evidence | Status` 映射；五维拒稿清单 | 没有 slop 视角 |
| `[YSLAB]` | https://github.com/YSLAB-ai/manuscript-writing | Phase 0–5 清单；"缺少支撑不是换成一个更弱的主张的理由" | — |
| `[refchecker]` | https://github.com/markrussinovich/refchecker （MIT） | 多数据库引用核查；作者重合率低于 60% 时报警 | — |

## 6. Zhehao Zou 前期材料中引用的核实结果

| 原引用 | 结论 |
|---|---|
| arXiv:2610.00531 *Science or Slop?* | 存在（2026-09-30），内容与描述一致 |
| Pew 2026-08-20 | 存在，内容一致 |
| Hadan et al. 2024（chbah.2024.100095） | 存在，内容一致 |
| aclanthology 2025.coling-main.426 | 存在。是 **COLING 2025**，不是 ACL |
| NAACL 2025 Findings 271 | 存在，内容一致 |
| arXiv:2609.14988 | 存在（Topaz et al.），内容一致 |
| ICLR 2027 AI 政策页 | 存在，内容一致 |
| AISTATS 2027 AI 政策 | 存在，在 Submission FAQ 页面上 |
| Reddit 系列帖子 | 本环境无法访问 Reddit，**未复核**，保留为 ★ |

## 7. 关键数字速查

- ICLR 2026：Pangram 判定 21% 的审稿意见完全由 AI 生成，约 9% 的论文 AI 内容超过一半 `[Pangram25]`；凡确认含幻觉引用的论文全部 desk reject `[ICLR26-retro]`。
- NeurIPS 2025 已接收论文：4,841 篇中 51–53 篇共确认 100 条幻觉引用 `[GPTZero-NeurIPS]`。
- COLM 2026：检测器 AI 分数最高的 50 篇中 0 篇被推荐接收（初步统计），全会接收率 29% `[COLM26]`。
- TMLR：desk reject 率从约 6% 涨到约 53% `[TMLR26]`。
- ICML 2026：水印抓到违规审稿，497 篇关联投稿被 desk reject `[ICML26]`。
- Luo 等人的 LLM 审计器只看论文时，识别 AI 科学家系统缺陷的准确率 55%；加上日志和代码后 82% `[Luo25]`。
- 本项目校准（59 篇 2018–22 年人类论文 对 20 篇 AI 论文；样本内、混杂时代因素）：-ing 尾巴 AUC 0.96，AI 词簇 0.93；但 2026 年的两篇 Claude 管线论文几乎没有 L 层痕迹（见 `tools/calibration/calibration_report.md`）。
- 本项目盲测（6 篇，标签事后揭晓）：两篇人类论文 → A；两篇 Sakana 论文 → D；一篇 2026 年自主 agent 论文 → D；一篇 2026 年全管线论文 → C（见 `skills/paper-slop-screen/references/worked-examples.md`；按 v0.2 规则重评，象限不变）。`[Internal-20261005-blindtest]`

## 8. 本项目内部来源

| 键 | 来源 | 要点 | 核实 |
|---|---|---|---|
| `[Internal-20261005-blindtest]` | 本项目 2026-10-05 的两次测试：审稿 skill 对 6 篇公开论文的盲测（结果与教训见 `skills/paper-slop-screen/references/worked-examples.md`），以及写作 skill 在 3 个场景上的作者把关测试（审计、修改、红队） | 数字取证（百分比×n 是否为整数、同一配置跨表一致）是命中率最高的检查；表层干净的 2026 年管线论文仍有严重的 R 层问题；写作 skill 的管线规则需要覆盖所有改动 | 内部测试，样本小（6 篇 + 3 个场景） |
| `[Internal-20261007-coherence]` | 一位作者对另一篇由 agent 起草的论文做人工润色后的反馈（2026-10-07）：改动约 19 行，集中在章节承接、把否定句改成正面陈述、拆分逗号串起来的长从句 | "有几个部分每句话各说各的，没有啥 connection"；"每一个 section 如何承上启下"；"comma 用得太多了，读起来像是一直在说从句"。据此扩充了 S08 的典型表现，并在 `paper-author-pass` 中加入 coherence pass 和两条句子规则 | 内部观察，单篇论文 |
| `[Internal-reviewing]` | 维护者自己的审稿经验 | R18、R20、R21、R22、P14、P16、S18 等条目的初始依据 | **U**：未核实，属于个人经验；有了匿名化 field report（`docs/field_reports/`）后逐条替换成 `[Internal-YYYYMMDD-缩写]` |
