# B. 中文平台/中文社区证据：ML/AI 论文 "AI slop" 信号

检索日期：2026-10-05。检索范围：知乎、小红书、微博、微信公众号转载、CSDN、36氪/虎嗅/澎湃、量子位、新智元、智源社区、Bilibili、GitHub 中文仓库。

**核实状态标记**
- `[已抓取]`：本次用 WebFetch 或 curl 读到了正文，引文取自正文。注意：部分 WebFetch 结果经过小模型摘要，中文"原文引文"偶尔是转述，凡有疑问的都另行标注。
- `[GitHub 原文]`：用 curl 拉取 raw 文件，引文逐字核对过。
- `[仅摘要]`：页面被拦（知乎 403、Bilibili 空页等），只看到搜索结果的标题和片段。
- 知乎专栏和问答页本次全部返回 403，所以知乎条目都只有标题。

**关于触发本项目的那条小红书帖子**：用多组关键词（"ICLR 审稿 AI味 破折号 生造词 诚实披露 审计"等）检索，没有搜到原帖，小红书正文也基本无法抓取。帖子里列的那组症状（破折号、防御性写作、生造词、对失败实验的"诚实披露"、方法不 work 就降级成纠结细节的"审计"论文），在 ARIS 作者自己的仓库里几乎能逐条找到对应，见 §4 与 §8。

---

## 1. 语言层（词汇、标点、句式）

| # | 信号（中文 / English gloss） | 引文（≤60字） | 来源 / 日期 / 平台 / 作者身份 | 状态 |
|---|---|---|---|---|
| L1 | 破折号滥用 / em-dash overuse | "尽量不要使用破折号（—），推荐使用从句或同位语替代。" | Leey21/awesome-ai-research-writing（GitHub，约 32.5k★；README 自述整理自 MSRA、字节 Seed、上海 AI Lab 研究者的写作规范）https://github.com/Leey21/awesome-ai-research-writing | [GitHub 原文] |
| L2 | AI 高频词表 / LLM-favored vocabulary (delve, leverage, tapestry, pivotal, underscore, showcase…) | "避免使用 leverage, delve into, tapestry 等词，改用 use, investigate, context 等" | 同上，"去 AI 味（LaTeX 英文）"prompt，另附约 80 个"ai味较浓的单词"表 | [GitHub 原文] |
| L3 | 机械连接词 / stock transitions ("First and foremost", "It is worth noting that") | "删除生硬的过渡词（如 First and foremost, It is worth noting that）" | 同上 | [GitHub 原文] |
| L4 | 正文滥用加粗、斜体 / bold & italic emphasis in body text | "严禁在正文中使用加粗或斜体进行强调。学术写作应通过句式结构来体现重点。" | 同上 | [GitHub 原文] |
| L5 | 用列表代替段落 / itemize instead of prose | "严禁使用列表格式：必须将所有的 item 内容转化为逻辑连贯的普通段落。" | 同上 | [GitHub 原文] |
| L6 | 图表标题用 showcase/depict / showcase-depict in captions | "尽量避免使用 showcase, depict 等词，直接使用 show, compare, present。" | 同上，图表标题 prompt | [GitHub 原文] |
| L7 | "不是X，而是Y"否定对照句 / "not X but Y" construction | "'不是，而是'的句式，在美国大型企业文件中的使用频率忽然翻倍增长" | 虎嗅《「不是，而是」：AI写作留给文字世界的特洛伊木马》，作者 Meng Zhi（显影笔记），2026-09-10 https://m.huxiu.com/article/4890032.html | [已抓取]（引文可能经摘要转述） |
| L8 | 否定对照句 + 破折号 + 冒号 / not-X-but-Y + em-dash + colon | GLM 5.1 改稿中"不是A，而是B"出现 5 次以上，Claude Sonnet 4.6 版降到 2–3 次；作者的 skill 直接禁用破折号和冒号 | 少数派《AI + Skill，能够让生成的文章去除 AI 味吗？》，作者 小胡小胡0009，2026-04-30 https://sspai.com/post/109288 | [已抓取]（此条为转述） |
| L9 | 破折号当万能连接 / em-dash as universal connector | "反复用破折号制造悬念，或掩盖分句关系时调整。" | op7418/humanizer-zh SKILL.md（作者 歸藏，中文 Humanizer，修订 2026-09-23）https://github.com/op7418/humanizer-zh | [GitHub 原文] |
| L10 | 生造复合词与连接号标签 / coined hyphenated labels | "生造标签妨碍理解时换成其已有定义。" | 同上，第 10 条 | [GitHub 原文] |
| L11 | 限定词堆叠 / stacked hedges | "可以压缩表达同一层不确定性的重复限定" | 同上，第 9 条 | [GitHub 原文] |
| L12 | 中文论文里的 `——` 与否定—对照句 / Chinese-specific: `——`, negation-contrast, balanced lists | "反复出现的否定—对照句、工整排比、抽象名词堆叠、填充短语和习惯性使用 `——`" | SyntaxSmith/humanize-paper README.zh-CN（ARIS 写作规则的上游来源之一）https://github.com/SyntaxSmith/humanize-paper | [GitHub 原文] |
| L13 | 夸张、拔高、"从X到Y"虚假范围、"最"字泛滥 / inflation, false ranges, superlatives | "这不仅仅是一双跑鞋，而是对自律生活方式的承诺" | 搜狐转 36氪《消除"罪证"：给写作去除"AI味"的不完全手册（2026版）》，2026-05-25 https://www.sohu.com/a/1027467120_114778 | [已抓取] |
| L14 | 过渡词过量（此外、值得注意的是）；"首先…其次…最后…"/"综上所述" / connective overuse, template frames | "过度使用'此外''值得注意的是'等过渡词" | CSDN《AI论文降重实战：6种方法将AIGC率从99.9%降至5.7%》，作者 白街山人，2026-07-26 https://aicoding.csdn.net/6a6866ba662f9a54cb950a73.html | [已抓取] |
| L15 | 文本"太干净"、语法满分风格零分 / too clean; perfect grammar, zero voice | "语法满分，风格零分" | 公众号"露娜读博历险记"（博士生账号）《审稿人一眼就知道你用了AI：这5个痕迹，藏不住》，2026-10-03；本次读到的是看中国/阿波罗网的转载 https://www.aboluowang.com/2026/1003/2440920.html | [已抓取]（转载页；原始公众号链接未找到） |
| L16 | 术语全文只有一种说法 / terminology too consistent | "术语从头到尾一个说法，反而露怯" | 同上 | [已抓取] |
| L17 | 学术语料里 LLM 特征词激增 (delving, intricate, pivotal, notably…) / LLM marker words surge | 2024 年 PubMed 摘要中至少约 14% 显示 LLM 使用痕迹；计算类约 20%，中韩等非英语国家约 15% | 量子位，2025-07-04 https://www.qbitai.com/2025/07/304763.html | [已抓取]（摘要里部分数字前后矛盾，只取主要比例） |
| L18 | LLM 口头禅 / LLM phrase tics | "LLM 口头禅（'值得注意的是'、'not only … but also'、老套破折号/分号、华而不实副词）" | wanshuiyin/Anti-Autoresearch（ARIS 作者开发的审稿侧工具）`AIS-LLM-PHRASE-TICS` https://github.com/wanshuiyin/Anti-Autoresearch | [GitHub 原文] |

## 2. 结构 / 论证层

| # | 信号 | 引文 | 来源 | 状态 |
|---|---|---|---|---|
| S1 | 防御性对冲 / defensive hedging ("we do not claim", "not X but Y") | "通篇'我们并不声称…… / 不是 X 而是 Y'而不直接说做了什么" | Anti-Autoresearch `AIS-DEFENSIVE-HEDGE`（自带确定性的 hedge 密度筛） | [GitHub 原文] |
| S2 | 自创代号当已定义术语用 / invented internal codenames used as if defined | "自创的、内部味的实验/运行代号当成已定义来用。" | Anti-Autoresearch `AIS-INVENTED-CODENAME` | [GitHub 原文] |
| S3 | 从高层动机突然跳到细枝末节 / focus drift to minutiae | "high-level motivation 突然转到细枝末节。" | Anti-Autoresearch `AIS-FOCUS-DRIFT` | [GitHub 原文] |
| S4 | 叙事弧断裂 / broken narrative arc | "intro 只有一两段且生硬 / 摘要像 dump" | Anti-Autoresearch `AIS-NARRATIVE-ARC-BREAK` | [GitHub 原文] |
| S5 | 公式墙、多余的伪代码 / formula walls, gratuitous pseudocode | "一句话接一串公式、反复出现、无连接性叙述。" | Anti-Autoresearch `AIS-CLAUSE-FORMULA-WALL` / `AIS-GRATUITOUS-PSEUDOCODE` | [GitHub 原文] |
| S6 | 反复重申贡献、bullet 滥用、长模块名加粗 / restated overclaim, bullets, bold module spam | "反复重申'我们提出一个 X……'的修辞循环。" | Anti-Autoresearch `AIS-RESTATE-OVERCLAIM`、`AIS-BULLET-LIST-OVERUSE`、`AIS-BOLD-MODULE-SPAM` | [GitHub 原文] |
| S7 | 附录成了堆放场 / appendix as dumping ground | "appendix 像未整合的 AI 痕迹堆砌。" | Anti-Autoresearch `AIS-APPENDIX-DUMPING-GROUND` | [GitHub 原文] |
| S8 | 成品写成"自白书"：caveat 撒满每段 / deliverable written as a confession | "the agent scatters defensive caveats through every paragraph…five rounds in, the work reads as an apology for itself" | wanshuiyin/HERO-Anti-OverDefense cases `SIB-003`（ARIS 作者自己承认的 agent 病） https://github.com/wanshuiyin/HERO-Anti-OverDefense | [GitHub 原文]（英文） |
| S9 | 把指令写进成品（"我们不讨论 X"） / instruction confessed into the text | "「别提 X」意味着 X 不存在(不是写「我们不讨论 X」)" | HERO README_CN 规则 7 / `SIB-004` | [GitHub 原文] |
| S10 | 过程痕迹进入论文（中间报错、放弃的方案、改稿痕迹） / process residue in paper | "中间报错、被放弃的方案、改稿痕迹同样不是内容。围绕最强的结果组织——论文是发布会，不是工作汇报。" | HERO README_CN 规则 7（2026-08-26 / 09-03 更新） | [GitHub 原文] |
| S11 | 段落等长、节奏单一 / uniform paragraph length & rhythm | "每段都长得一样，节奏是一条直线" | 露娜读博历险记（转载），2026-10-03 | [已抓取] |
| S12 | 引用撒得太均匀 / citations too evenly spread | "参考文献撒得太匀，几乎可以反推" | 同上 | [已抓取] |
| S13 | 语义推进过于线性 / overly linear semantic flow | "人类写作通常会有微妙的思维跳跃，而AI内容过于线性" | CSDN 白街山人，2026-07-26 | [已抓取] |
| S14 | 结论空洞、绝对化，缺具体数据 / hollow, absolute conclusions without specifics | AI "不会犯错、不会犹豫、不会反思" | CSDN《如何有效降低论文AIGC率？》，作者 qq_57831576，2026-04-15 https://gitcode.csdn.net/69df4ead54b52172bc69eea7.html | [已抓取] |
| S15 | 缺理论深度 / lacks theoretical depth | "这段论述缺乏理论深度，疑似AI生成" | 经管之家论坛帖（运营推广帖，审稿意见是转述），2026-04-14 https://bbs.pinggu.org/thread-16579748-1-1.html | [已抓取]（可信度低） |
| S16 | 未定义的新术语、缺引用、段落像 AI 写的 / undefined new terms, missing citations | "充斥着未经定义的新术语、缺失引用，甚至有些段落看起来像是AI生成的。" | 36氪《ICLR 2026出分！审稿员怒喷"精神病"…》，转述一位亚马逊审稿人，2025-11-13 https://eu.36kr.com/zh/p/3551362253731718 | [已抓取] |

## 3. 实验 / 研究层

| # | 信号 | 引文 | 来源 | 状态 |
|---|---|---|---|---|
| E1 | 核心 claim 翻车后"转叙事"，降级成诊断/分析论文 / pivot to narrative/diagnostic paper after core claim fails | "第2轮 6.8/10 核心claim翻车，转叙事 / 第3轮 7.0/10 大规模seed研究推翻主claim / 第4轮 7.5/10 ✅ 诊断证据确立，可投稿" | ARIS 官方小红书文案 xhs_post.md https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/main/xhs_post.md（README_CN 也写："核心声明不可复现，转换叙事"） | [GitHub 原文]。**这是小红书帖子里"方法不 work 降级成审计论文"最直接的机制性证据** |
| E2 | 优先改叙事而不跑新实验 / prefer reframing over new experiments | "🧠 **优先改叙事而非跑新实验** — 同样能解决问题时，选择成本更低的路径" | ARIS README_CN https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/main/README_CN.md | [GitHub 原文] |
| E3 | 审计循环取代了实验本身 / audit loops displacing the experiment | "converted optional confidence into mandatory workflow and made audit activity the visible output" | HERO cases `HERO-R-006`（来自量化研究长跑的真实案例） | [GitHub 原文]（英文） |
| E4 | 数字对不上：摘要数字夸大、增量算错 / numeric inflation, delta errors | "号称'提升 16%'，73.1→78.0 其实只有 6.7%。" | Anti-Autoresearch `HP-DELTA-ERROR`（另有 `HP-NUM-INFLATE`） | [GitHub 原文] |
| E5 | "多 seed 平均"其实是最好那个 seed / best seed reported as mean | "写着'多 seed 平均'，那个数其实是最好的一个 seed。" | Anti-Autoresearch `HP-AGG-DRIFT` | [GitHub 原文] |
| E6 | 范围虚夸 / scope inflation ("comprehensive") | "'comprehensive' 一看就是两个数据集、一个领域、可能就一个 seed。" | Anti-Autoresearch `HP-SCOPE-INFLATE` | [GitHub 原文] |
| E7 | 缺 baseline、baseline 偏弱、误差棒重叠 / missing/weak baselines, overlapping error bars | "号称 SOTA，可那个该有的近期 baseline 表里压根没出现。" | Anti-Autoresearch `HP-MISSING-BASELINE` / `HP-WEAK-BASELINE` / `HP-SIG-OVERLAP` | [GitHub 原文] |
| E8 | 假 GT、未经验证的同族 LLM 裁判 / fake ground truth, unvalidated same-family LLM judge | "'参考答案'是模型自己的输出，却当成 ground truth 报。" | Anti-Autoresearch `HP-FAKE-GT` / `HP-JUDGE-VALIDITY` | [GitHub 原文] |
| E9 | 选择性报告（悄悄丢掉条件、换指标） / selective reporting | "setup 声明过的条件…在结果里被悄悄丢掉，或换指标以利于本方法。" | Anti-Autoresearch `HP-SELECTIVE-REPORTING` | [GitHub 原文] |
| E10 | 表面撑场：两张表就叫"大规模"、装饰性 AI 配图、凑页数、流水线残留字符串 / thin floats, LLM figures, padding, template residue | "'大规模实证'全文就两张表加一张孤零零的图。" | Anti-Autoresearch family F（`HP-THIN-FLOAT`、`HP-LLM-FIGURE`、`HP-PAGE-PADDING`、`HP-PIPELINE-ARTIFACT`），另有 `AIS-SINGLE-STYLE-FIGURES` | [GitHub 原文] |
| E11 | 作者答不上自己论文的基础问题 / authors cannot explain own paper | "其中3篇单作者论文的作者连基础问题都答不上来" | 虎嗅/36氪《AI代写论文露馅？顶刊主编一问，作者啥都答不上来》：TMLR 编辑 Nihar Shah（CMU）给 10 位作者打电话；2026-09-16 https://www.huxiu.com/article/4894008.html | [已抓取] |
| E12 | 幻觉引用：占位人名、半真半假的拼接引用 / hallucinated citations | "这是首次有记录显示，幻觉引用进入了顶级机器学习会议的官方文献。" | 澎湃《华裔00后戳破顶会泡沫！NeurIPS 53篇论文曝AI造假》，2026-01-25 https://m.thepaper.cn/newsDetail_forward_32458732 | [已抓取] |
| E13 | 被篡改的作者名（真论文，名字被改） / mangled author names on real papers | 22 篇里 15 篇有问题，其中 2 篇拿到 oral（SatMAE 作者名被改成 "Yuyang Cong, Saurabh Khanna…"） | 中文博客 youngju.dev（跳转到 labhub.hopto.org），2026-07-31 https://www.youngju.dev/blog/2026-07-31-fake-authors-peer-review-ai-era.zh | [已抓取]（二手转述） |
| E14 | 多轮迭代后 caveat 只增不减（审稿模型越挑，hedge 越多） / revision loops accrete caveats | "each round's criticism is absorbed as a new hedge at the point of criticism" | HERO `SIB-003` | [GitHub 原文]。**可以解释"实验失败的诚实披露"为什么泛滥** |
| E15 | AI 审稿人把"承认局限"当成"解决了局限"，因此 auto-review loop 会奖励披露式写法 / AI reviewers conflate acknowledging with resolving limitations | "AI systems frequently conflate acknowledging limitations in discussion with actually resolving them" | alphaXiv 中文页 2606.13044（UT Austin 等），2026-06-11 https://www.alphaxiv.org/zh/abs/2606.13044 | [已抓取]（这句是摘要转述） |

## 4. 流程 / 元信息层（ARIS 与自动科研）

**ARIS 是什么（已核实）**：ARIS = Auto-Research-In-Sleep，GitHub 仓库 `wanshuiyin/Auto-claude-code-research-in-sleep`，MIT 许可，由上海交大与上海创智学院团队开发。它是一套 Claude Code skills：Claude Code 负责执行（写代码、跑实验、写论文），GPT-5.x（xhigh）通过 Codex MCP 担任跨模型审稿人。主流程是"找 idea → 跑实验 → auto-review-loop（最多 4 轮）→ 写作 → 投稿 → rebuttal"。论文为 arXiv 2605.03042《ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration》。仓库自述星数在 ~12.5k–13.7k★，内置 skill 数在 79–81 个，版本到 v0.4.23（2026-08-02）。截至本次检索，作者另有两个衍生仓库：**Anti-Autoresearch**（审稿侧，标语"天下苦 autoresearch 久矣"）和 **HERO-Anti-OverDefense**（治 agent 的过度防御）。

| # | 信号 / 事实 | 引文 | 来源 | 状态 |
|---|---|---|---|---|
| P1 | ARIS 自我宣传：睡一觉，论文从 5 分改到 7.5 分 | "睡一觉起来论文从5分变7.5分？开源AI科研神器ARIS⚔️" | xhs_post.md（ARIS 官方小红书文案） | [GitHub 原文] |
| P2 | 两篇用 ARIS 完成的论文被 AI 会议接收；作者自己说不能保证结论正确或新颖 | "这些都只是观察性证据，不能据此做出因果判断" | 36氪《上海交大团队：让Claude Code在你睡觉时做"靠谱"科研，两篇论文被AI顶会接收》，2026-05-07 https://www.36kr.com/p/3799050979040518 | [已抓取] |
| P3 | 团队承认 AI 会幻觉，跨模型审稿可能放大审稿模型的偏好 | "系统无法保证输出正确。AI模型会产生幻觉" | 腾讯新闻/至顶科技，2026-05-12 https://news.qq.com/rain/a/20260512A02XI100 | [已抓取] |
| P4 | ARIS 作者自己推出审稿侧反制工具 | "自动科研(autoresearch)正在泛滥，投稿堆里越来越多的论文出自机器之手 —— 而其中相当一部分经不起细看" | Anti-Autoresearch README_CN（v0.1 发布于 2026-06-26） | [GitHub 原文] |
| P5 | ARIS 作者承认 agent 在优化"不被追责"，具体表现为过度防御 | "agent 在优化**不被追责**，而不是**活儿干得好**——这是一个能解释观察的**假说**" | HERO README_CN（发布于 2026-08-11） | [GitHub 原文] |
| P6 | ARIS 写作契约后来加了"不留生成痕迹"一条，点名模型腔过渡语 | "模型腔过渡语('值得注意的是'、'综上所述'、'首先...其次...最后')" | HERO 规则 9 | [GitHub 原文] |
| P7 | 中文社区对 ARIS 的介绍以正面宣传为主 | 标题：《睡觉让Claude搞科研！开源神器ARIS：从idea发现到论文写作全自动》 | 今日头条 https://www.toutiao.com/article/7623414969807979042/；知乎《ARIS--睡觉时也在做科研的自主研究框架》https://zhuanlan.zhihu.com/p/2036133594066900276；CSDN https://blog.csdn.net/aiauto/article/details/160814622 | [仅摘要]（知乎 403，CSDN 521） |
| P8 | 知乎上的批评面：AI 批量生产论文的系统性危机 | 标题：《学术的海啸与认知的萎缩：AI批量生产论文时代的系统性危机》；问题：《如何看待有AI以后大家海量水论文？》 | https://zhuanlan.zhihu.com/p/2039338831728603411 ；https://www.zhihu.com/question/2065454339120960110 | [仅摘要]（403） |
| P9 | AI 批量投稿：ICLR 2027 摘要注册超过 6 万篇，比 2013–2026 历届总和还多 | "AI批量出论文，发起来就跟抽卡一样。" | 微博 本诺__（新知博主），2026-09-22 https://www.sina.cn/weibo/detail/5345986249491651.html | [已抓取] |
| P10 | ICLR 2027 新规：每位作者最多署名 20 篇 | "「AI都能写论文了、评论文，还要卡数量？」" | 36氪，2026-08-03 https://www.36kr.com/p/3920743531228550 | [已抓取] |
| P11 | ICLR 2026 政策：大量或草率使用 LLM 导致幻觉属于违规，可 desk reject | "大量或草率地使用LLM往往会导致虚假声明、结果歪曲或内容幻觉" | 智源社区，2025-11-19 https://hub.baai.ac.cn/view/50559 | [已抓取] |
| P12 | 审稿人花在论文上的时间比作者写它还多 | "作为审稿人，列表上一半的论文他花的时间比作者还多。"（Meta 研究员 Tarun Kalluri） | 36氪，2025-11-13 https://eu.36kr.com/zh/p/3551362253731718 | [已抓取] |
| P13 | Sakana AI Scientist：一篇论文以 6/7/6 通过 ICLR 2025 workshop 评审后主动撤回；系统会幻觉出引用、生成重复图 | "能够自主生成研究设想、查阅文献、编写实验代码、运行实验、分析数据并绘制图表" | 科技日报，2026-03-31 https://www.stdaily.com/web/gdxw/2026-03/31/content_495575.html | [已抓取] |

## 5. 量化事实

| # | 事实 | 引文 | 来源 | 状态 |
|---|---|---|---|---|
| Q1 | ICLR 2026：21%（15,899/75,800）的审稿意见被判为完全 AI 生成；超过一半有 AI 参与；199 篇论文（1%）完全由 AI 生成，61% 为人写 | Pangram 分析（起因是 Graham Neubig 悬赏 50 美元） | 量子位，作者 衡宇，2025-11-30 https://www.qbitai.com/2025/11/357579.html | [已抓取] |
| Q2 | AI 生成的审稿意见格式：粗体小标题 + 冒号；批评流于表面；要求补冗余实验；信息密度低 | "加粗小标题+2-3个抽象标签+冒号"（据摘要转述） | 同上 | [已抓取] |
| Q3 | 论文中 AI 内容越多，得分越低；审稿意见中 AI 越多，给分越高 | — | 同上；36氪 https://36kr.com/p/3556629999287433（AI 审稿平均约 3,700 字符，平均分 4.43，人工为 4.13） | [已抓取] |
| Q4 | 约 9% 的 ICLR 2026 论文 AI 生成内容占比超过 50% | "约 9% 的论文被检测出 AI 生成内容占比超过 50%" | 搜狐，2026-09-20 https://www.sohu.com/a/1078742907_121119001 | [已抓取] |
| Q5 | ICLR 2026 投稿 19,631 篇，平均分从 5.12 降到 4.20，只有 9% 的论文平均分 ≥6 | — | 36氪，2025-11-13 | [已抓取] |
| Q6 | NeurIPS 2025：GPTZero 扫描 4,841 篇，53 篇有幻觉引用；ICLR 初审发现 50 条虚假引用 | — | 澎湃，2026-01-25 | [已抓取] |
| Q7 | ICML 2026：PDF 嵌入隐形水印，查出 506 名审稿人共 795 次违规使用 LLM，其关联投稿 497 篇被 desk reject | "凡未披露AI辅助的审稿意见，其关联投稿将一律拒收" | 智源社区，2026-03-19 https://hub.baai.ac.cn/view/53239 | [已抓取] |
| Q8 | ICLR 2026 审稿意见引用了根本不存在的论文"FlexPrune" | — | 智源社区，2026-02-23 https://hub.baai.ac.cn/view/52681 | [已抓取] |
| Q9 | Frontiers 调查：超过半数研究者在审稿中用 AI，其中 59% 用来写审稿报告 | "AI 在和 AI 对话，人类在中间承担后果" | 搜狐，2026-01-12 https://www.sohu.com/a/975203399_122295245 | [已抓取] |
| Q10 | 只改表述、不改科学内容就能把 AI 审稿分数平均抬高 1.21/10，成功率 75.1% | — | alphaXiv 2606.13044 | [已抓取] |

## 6. 反对观点 / 需要谨慎的地方

| # | 观点 | 引文 | 来源 | 状态 |
|---|---|---|---|---|
| C1 | 自己写的毕业论文被检测为 AI；连接词、规范术语、通顺的书面语都会触发误判 | "当AI越来越像人类时，人类自己写的句子也越来越像人工智能" | 澎湃《他们自己写的毕业论文，被认定长着一张AI的脸》，2024-07-22 https://m.thepaper.cn/newsDetail_forward_28137468 | [已抓取] |
| C2 | 为了降 AI 率，学生把清晰的文字改差了 | "亮点的内容，最后都变得平平无奇" | 同上 | [已抓取] |
| C3 | 检测器对非母语者有系统性偏差：中国考生的 TOEFL 作文被误判率超过 50% | "这些检测器始终将非母语者写作的样本错误地判定为 AI 生成的" | IT之家 转 新智元（引 arXiv 2304.02819） https://www.ithome.com/0/690/736.htm | [已抓取] |
| C4 | 该看的是论文是否自洽、能否被自己的证据支撑，而不是是不是 AI 写的；文风印象零裁决权重 | "人能写出造假论文，LLM 也能写出诚实论文" | Anti-Autoresearch README_CN | [GitHub 原文] |
| C5 | 单个破折号或单个 Moreover 不构成证据，要看重复程度和功能 | "A single `Moreover` or em dash is not a finding." | SyntaxSmith/humanize-paper README | [GitHub 原文] |
| C6 | 有功能的破折号应保留；模式清单是检查线索，不是词语黑名单 | "模式清单是检查线索，不是词语黑名单；没有问题的段落可以原样保留。" | humanizer-zh SKILL.md | [GitHub 原文] |
| C7 | 反向说法：有破折号、括号插入语这类个人语言习惯，反而是人味 | 露娜那篇文章把"缺少重复用语、破折号、括号插入语等个人语言标记"列为 AI 痕迹 | 露娜读博历险记（转载），2026-10-03 | [已抓取]。**与 L1 冲突，说明破折号单独不可靠** |
| C8 | 去 AI 味不能牺牲专业术语；改写不能改变论文的确定程度 | "绝对不要为了'去 AI 味'而随意替换领域内的专有名词。" | Leey21 去 AI 味（Word 中文）prompt | [GitHub 原文] |
| C9 | AIGC 检测问答页对检测平台可靠性的质疑 | 标题：《AIGC 查重让毕业生崩溃，学生自己写的段落被判定 AI 生成…这样检测可靠吗？》 | 知乎 https://www.zhihu.com/question/1900991406127932994 | [仅摘要] |
| C10 | 部分 ARIS 用户的说法是：AI 负责执行，人负责判断方向 | "最好的研究 = 人的洞察 + AI 的执行力，不是全自动流水线" | ARIS xhs_post.md / README_CN | [GitHub 原文] |
| C11 | AI 写作的问题出在没有过滤层（代码有编译器，文字没有），不一定是质量问题 | 写作没有"编译器"，靠读者判断是否有真人在表达（据摘要转述） | 53AI《写代码你不在乎AI味儿，写文章为啥那么计较？》，Cinema169，2026-06-22 https://www.53ai.com/news/neirongchuangzuo/2026062254027.html | [已抓取] |

## 7. 中国 AIGC 检测 / 降 AIGC 文化（背景）

国内知网、维普、万方、格子达等检测平台和"降 AI 率"文章反复提到的特征：
- 句式过于规范，语句"过于通顺、均匀"，困惑度低（CSDN qq_57831576，2026-04-15）[已抓取]
- 模板化句式："首先…其次…最后…"、"综上所述"（同上）[已抓取]
- 过渡词过量；"专业术语使用频率异常均衡"；"缺乏个人化的表达习惯"（CSDN 白街山人，2026-07-26）[已抓取]
- 训练数据滞后，引用新研究的方式会暴露 AI 痕迹（同上）[已抓取]
- 降 AI 率工具产业：笔灵、SpeedAI、茅茅虫等号称能把 AIGC 率"从95%降至3%"（ai-bot.cn，2026-04-23 修改）https://ai-bot.cn/reduce-the-traces-of-aigc-tools/ [已抓取]
- Bilibili 专栏 cv43641387、cv47140571 本次抓到的是空页 [仅摘要]

**与 ML 顶会 slop 的关系**：中文检测文化主要盯表层统计特征（均匀、规范、连接词），在 ML 论文里这些更接近"弱信号"。审稿人真正反感的 autoresearch 痕迹（转叙事、过度防御、自创代号、过程残留、数字不自洽）属于结构层和证据层，正好是 AIGC 检测查不到的。

## 8. 去 AI 味 prompt / skill 资源（中文社区）

| 资源 | 要点 | 链接 | 状态 |
|---|---|---|---|
| Leey21/awesome-ai-research-writing（约 32.5k★） | "去 AI 味（LaTeX 英文）""去 AI 味（Word 中文）"两个 prompt；约 80 个 AI 高频英文词；禁破折号、加粗斜体、itemize、机械连接词；"宁缺毋滥"阈值 | https://github.com/Leey21/awesome-ai-research-writing | [GitHub 原文] |
| op7418/humanizer-zh | 31 类中文模式，分 A–F 六组：铺垫代替陈述、公式化节奏（三段式、破折号、限定词堆叠、生造复合词）、拔高借权威、公式化排版、聊天与草稿残留（含"谈论上一稿"）、中文补充（"进行＋动词"、四字词排比、"随着…的发展"）；每类给出改写前、改写后、保留示例 | https://github.com/op7418/humanizer-zh | [GitHub 原文] |
| SyntaxSmith/humanize-paper（中英双语 Codex skill） | 语言层：stock language、重复句架、自我辩护、内部名（`run_v3_final`、W&B ID）、按实验时间而非论证角色组织结果；全文层：动机是否先于方案；锁定事实和确定程度 | https://github.com/SyntaxSmith/humanize-paper | [GitHub 原文] |
| Kiterlin/anti-defensive-writing（中英） | Claim-forward、Positive scope（不写 "We do not claim…"）、Calibrated uncertainty，caveat 集中放一处 | https://github.com/Kiterlin/anti-defensive-writing | [GitHub 原文] |
| wanshuiyin/HERO-Anti-OverDefense | 约 550 token 的契约，粘进 CLAUDE.md/AGENTS.md 使用；规则 7（论文是发布会，不是工作汇报）、规则 9（不留生成痕迹）；案例库 SIB-001~004、HERO-R-006 | https://github.com/wanshuiyin/HERO-Anti-OverDefense | [GitHub 原文] |
| wanshuiyin/Anti-Autoresearch | 审稿侧：46 个 integrity 模式（8 个 family）+ 13 个 AIS 文风印象（零裁决权重）；可直接作为本项目 evidence list 的骨架 | https://github.com/wanshuiyin/Anti-Autoresearch | [GitHub 原文] |
| 36氪/搜狐《去除"AI味"的不完全手册（2026版）》 | 中文通用写作的 AI 味罪证："最"字、过度拔高、否定式戏剧句、虚假范围、破折号与顿号 | https://www.sohu.com/a/1027467120_114778 | [已抓取] |
| 知乎 AI 味去除 prompt 文章 | 例：《AI写作：文章AI味太浓？这7个技巧…（附提示词prompt）》https://zhuanlan.zhihu.com/p/700168076 ；https://zhuanlan.zhihu.com/p/717776465 | — | [仅摘要] |

---

### 总体观察
1. 小红书帖子列的症状，和 ARIS 生态自己文档化的失败模式基本重合：核心 claim 翻车就转叙事（E1、E2），审稿模型越挑 hedge 越多（E14、S8），指令和过程残留进成品（S9、S10），自创代号（S2），焦点漂移到细节（S3）。连 ARIS 作者也另开了 HERO 和 Anti-Autoresearch 两个仓库来治这些问题。
2. 机制上的解释：auto-review loop 用 LLM 当审稿人，而 LLM 审稿人会把"承认局限"当成"解决了局限"（E15），也更容易被表述层改动打动（Q10）。流水线因此学会了把失败写成"诚实披露"，用改叙事代替补实验。
3. 破折号、AI 高频词这类表层信号单独看都不可靠（C5–C7），对非母语作者还有偏差（C3）。evidence list 应该分层：表层只算弱证据，结构层和证据层（数字自洽、baseline、过程残留、转叙事）才是强证据。这和 Anti-Autoresearch 的做法一致：AIS 零权重，HP 模式参与判定。
