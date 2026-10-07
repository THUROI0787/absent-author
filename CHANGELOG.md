# Changelog

## v0.4.1 — 2026-10-07（误判修复与连贯性）
- **lint 0.2.1，修复三条社区报告的误判**（感谢 @kaysonhu 提供最小复现）：
  - #1：CRediT 角色名（"Writing -- original draft"）不再触发 L01 和 S03。
  - #2：在自定义宏里设置的 `\label{#n}` 会被展开，不再误报为未解析引用；展开不了时只给提示，不计数。
  - #3：理论论文中"Assumption 2 … does not imply …"这类逻辑陈述不再计入 S01。
  - 三条都进了误判登记（FP-001 到 FP-003）和回归测试，EVIDENCE 中 S01、S03 的误判提醒同步更新。
- **连贯性**：根据一位作者人工润色 agent 起草论文后的反馈（`[Internal-20261007-coherence]`），S08 的典型表现补上"章节开头不承接上文、段落内每句各说各的"；`paper-author-pass` 的 Pass 2 加入 coherence pass（章节开头承上、段尾启下、句子靠内容而不是连接词衔接），句子规则加入"否定句改正面陈述"和"拆分逗号串起来的长从句"；审稿侧 S08 的检查加上"只读每段首句，看能否连成论证"。

## v0.4.0 — 2026-10-05（标语、长期判断、日语）
- **标语**：从 "AI can write the paper. Someone still has to be the author." 改为 **"Research and writing can be automated. Authorship cannot."**（中文：科研和写作可以自动化，署名的责任不能。日文：研究も執筆も、自動化できる。著者の責任は、自動化できない。）。新标语覆盖整条研究流程，而不只是写作；网站首屏、banner（新增日文版）、分享卡片、README 同步更新。
- **长期判断**：网站新增 "Where this is going" 一节，README 新增同名一节，`docs/POSITIONING*.md` 新增 §9"双重用途与长期判断"：坦白清单可能被用来洗掉表层痕迹；说明为什么洗文本换不来更好的结论（L 层只计 W，B 与 D 只差 R）；论证评价会从文本转向披露、可核查的产物和当面答辩；提出三个问题（是否透彻理解、敢否当面捍卫、愿否署名背书），并列出四条承诺。引用 Harvard CMSA 峰会报告原文（新增来源键 `[CMSA26]`），三问注明改写自中文媒体对该峰会的评论，不是报告原文。文案明确承认：洗文本能让 D 变成 C（降不了 R），P 层容易修的残留也会被洗掉，skill 的"不替缺席作者工作"只是默认做法、不是安全机制。
- **skill**：`paper-author-pass` 每次运行结束增加 **Author's checkpoint**：针对具体论文的三个问题（Understand / Defend / Sign），由作者在署名前回答，skill 从不代答、不打分；在审读模式、管线调用和提前停止时也照常输出；`paper-slop-screen` 的报告模板中，给作者的问题按同样三类分组。
- **日语**：网站支持 EN / 中文 / 日本語 三种语言，默认英文（`?lang=zh` / `?lang=ja` 可直接分享对应语言的链接，访客的选择会被记住）；证据条目正文在日语界面下显示英文。新增 `README_JA.md`（概要版）。
- **作者与致谢**：作者为 Ruoyu Zhao（项目负责人）、Zhehao Zou（与 Ruoyu Zhao 共同一作）、Jinheng Zhang、Yuting Chen、Jiaqi Wu、Chenyu Zhu，单位和邮箱写入 README（三种语言）、网站、`CITATION.cff`、BibTeX 和 `LICENSE`。致谢改为分类列出并逐条链接本项目参考过的 skill、auto-research 管线、论文，以及公开分享所见的会议主席和审稿人。`docs/research_notes/` 新增说明：内容均为公开资料，引用只为说明审稿人观察到了什么，不针对个人或具体论文。
- **去 slop 与复核**：三个独立 agent 分别做了三件事：用本项目自己的 lint 和 sentence rules 审读网站与 README 文案（删去自我表扬的结尾句、"清洗无用"之类的过度表述、空泛开场和反问句）；以日语母语编辑的视角审读日文（修正两处语义错误、统一"查読コメント／指摘／リジェクト／チェア"等术语、改进三问的日文）；独立复核事实与功能（核对 CMSA 引文原文、举证责任只由已核实的 ☠ 转移、三语切换与手机端无横向溢出、语言选择在带 `?lang=` 的链接里也能记住）。

## v0.3.0 — 2026-10-05（打包为 GitHub 仓库）
- **仓库化**：项目更名为 Absent Author，仓库结构参考 ARIS 的呈现方式：英文 README 加 README_CN，带徽章、目录、快速开始、figure，以及 MIT LICENSE、CITATION.cff、install.sh，issue 模板（新证据 / field report / 误判），PR 模板，CI（ID 一致性检查、lint 测试、站点数据构建），以及 GitHub Pages 部署 workflow。
- **双语清单**：`EVIDENCE.md` 改为英文完整镜像，`EVIDENCE_CN.md` 为中文主版本；`docs/POSITIONING.md` 和 `CONTRIBUTING.md` 有英文版，中文版为 `*_CN.md`。`tools/sync_evidence.py` 检查中英 ID 一致，并在 `--check` 模式下检查两个 skill 里的副本是否最新。两个 skill 的 `evidence-catalog.md` 改为英文，另附 `evidence-catalog-cn.md`。
- **可视化**：`tools/figures/make_figures.py` 生成 6 张 SVG：banner、四象限、证据分层、两个 skill 的流程、一次转向的解剖、校准 AUC。
- **按展示审读意见修订**：README 顶部改为一句话定位 + "你是谁 / 用什么 / 得到什么"表格，快速开始提前，新增"What you get"（lint 真实输出和筛查报告节选），删去重复的"我们不反对 AI"和若干"X，而不是 Y"句式；所有 figure 生成浅色/深色 × 中/英四个版本，README 用 `<picture>` 适配深色模式，中文 README 用中文图；figure 最小字号提高；生成 `assets/social.png` 作链接预览和 GitHub social preview；网站补上 og/twitter 元信息、深色模式下的象限配色、中文竖排轴标签、只复制命令的复制按钮、证据名中隐藏内部家族代码、手机端证据行布局、1100px 以下单栏、引用区标题；CI 增加 OWNER 占位符检查；`install.sh` 覆盖旧安装时会提示。
- **网站**（`site/`）：交互式稿件演示（逐条标注后盖出判定章）、四象限探索器（带滑块）、可筛选、可搜索的证据浏览器（中英切换）、skill 介绍与安装、校准与盲测、原则、贡献入口；支持深色模式和手机端。数据由 `tools/build_site_data.py` 从清单生成。

## v0.2.1 — 2026-10-05（一致性修订）
依据两份反馈：全项目一致性审读（E/SO/PO/RM/C/SS/S-A/G/Q/WE/PA/VP/SR/AP/HL/AR/AC/T/CR 各项），以及写作 skill 在 3 个场景（审计、修改、红队）上的测试。
- **分级定义**：W 只用 W 轴条目。W2 增加一条路径（≥3 项来自不同家族的 W 轴 S 证据）；W3 改为"W2 + F1 遍布 ≥3 节，或 AI 主导的痕迹无处不在"；S02/S03 不再出现在 W 的定义里（它们是 R 轴）。R 轴清单补上 R12（能指出借用来源时）和 P02（TODO 型，仅 ★），去掉 P13（i / ⚑）。R0 不再要求产物型 H；R1 不再要求"能被 H 解释"（改为注明）。"审稿人敏感的 L 证据"有了定义（L01、L02、L07、L09、L11、L12、L14、L16）。家族去重在同一轴内进行（F4 中的 L14、S05 只计 W）。EVIDENCE、grading-rubric、screen-actions、quick card、英文索引同步修改。
- **P12** 的强度改为"⚑ 不端"（不是 ☠），从 ☠ 清单中移出，单独列在 ⚑ 下。
- **校准标记**：校准✓ 只给有区分度的检查（AUC ≥ 0.65 或 specific）；L02、L14、L16、S02、S04、S06、S13、R01、R05、P02-todo、P03、P06、P07 改为"校准✗（本语料不区分）"，S01、S03、S05、R16、P01、P02-meta 为"校准✗（本语料罕见，无法区分）"。
- **过时数字**：L01 人类 p99 3.3 → 2.9（EVIDENCE、screen-actions、校准报告 §4.2）；sentence-rules 的 L03 AUC 0.94 → 0.93、L15 0.78 → 0.77；lint 报告头 "n of about 40" → "n=59"；lint 的 P05 检查去掉 CycleResearcher。
- **screen-actions**：S01、S14 → W；R09、R10 → R；P11 → i；R09 单处不符 = ★（记 Q）；R01 去掉"不需要残留骨架"的分支；S06 阈值与清单一致。
- **worked examples**：按 v0.2 规则重评。例 3：P02-todo 是 ★，0 个标记，仍为 D。例 5：W3（F1 遍布 + S06 + S08 + L01 高）、R3（路径 b：已核实的 R09 + R17；H06 只回应 R01），v0.1 判 R2，象限不变（D）。标注 L 簇分母（PDF 文本为 k/5）。
- **来源**：新增 `[Internal-20261005-blindtest]`、`[Internal-reviewing]`，替换"审稿经验 / 本项目盲测"等自由文本；Banana Rule 改引 `[ARIS-paper-write]`；补引此前未用的键（`[Liang24b]` `[Sanger26]` `[Cornell25]` `[BadScientist25]` `[ICLR26-resp]` `[ARIS-xhs]` `[DailyNous25]` `[humanizer-zh]` `[DS]`）；SOURCES 记录 ARIS 的 forced structural pivot 和 citation-audit、AA 的 46 + 13 条、ICLR 2027 声明的必填项、ICML 2026 的 Policy A；`materials_Zhehao/` 与 `Research-Paper-Writing-Skills-main.zip` 的说明改正，并列入 README 目录。
- **写作 skill**（作者把关测试的建议）：管线规则覆盖所有改动（包括残留、数字和水印）；P05 水印只能在人类确认披露后去掉；"decide for me" 只能来自对话中的人类；先在论文源码旁找结果、日志和代码；只在 revise 模式且作者确认后改数字；人类论文默认不改，其余部分就是 voice sample，普通校对只列出不改；核查增加 comparator 检查、粗体最优、隐藏的运行、方法与代码对照、`EXAMPLE FIGURE` / `REPLACE AND ADD YOUR OWN` 占位符；输出增加 Pass 1 小结（一句话测试 + steering card）和停止原因，AI 贡献声明只在有作者时起草；短文本 lint 只看命中、不看分档；Pass 2 改为清单。
- **英文索引**：新增 `docs/evidence-index-en.md`（ID｜名称｜强度｜轴），`tools/sync_evidence.py` 把它同步进两个 skill，并检查它覆盖全部 ID；同步时把目录内链接改写为"在项目仓库中"。
- **其他**：EVIDENCE 增加页内导航、术语框、S06 判定标准注；速查卡改为"每项 1–3 分钟，前 15 分钟先做 1–4"，并补上 OpenAlex 和 XXXX；POSITIONING 的三种缺席、四象限措辞与 EVIDENCE 对齐，路线图的现代对照组顺延到 v0.3；README/CONTRIBUTING 的校准命令补上 `--scratch`；CONTRIBUTING 补上轴列、人类反例和内部来源键。

## v0.2 — 2026-10-05（同日迭代）
依据三份独立反馈修订：资深审稿人视角的 agent 批评、62 项事实核查、6 篇论文的盲测。
- **结构**：新增 Q 轴（普通质量），使"研究引导缺席"（R）不再和"论文质量差"混在一起；象限只由 W×R 决定。新增可审性评级（A+/A/A0）。新增"家族"规则，同一家族只按一条计。新增铁律 4（新手不等于缺席）和铁律 5（只有亲自核实过的 ☠ 才转移举证责任）。新增论文类型豁免表和 15 分钟速查卡（另附英文版）。
- **R3 放宽**：不必出现转向；有两种以上不同类型的核查失败也可以判 R3。
- **H 证据按可核实程度分级**：纯文字的 H 只能把一条 ★★ 降一级；产物型的 H 才能抵消发现。
- **新增条目**：S18、R17–R22、P13–P18。重写 S06 的判定方式（替换测试）。
- **强度调整**：S02 → ★★（未校准）；S03 拆成强、弱两种形式；S12、R12 → ★★；R05、L02 → ★；P02 拆分（元评论 ☠ / TODO ★）；P06 只认字面的管线字符串（S2 风格的 bib key 不再算证据）；R16 出现在论文正文中时 → ☠。
- **D 象限的操作化**："严格处理"包括做什么、不做什么、二人复核。B 象限给出可执行的重写清单。
- **事实修正**：Kobak 的比值（13.8、10.7）；ICLR 2027 "6 万"改为引非官方来源；COLM 的 0/50 是"推荐接收"的初步统计；Czuma 的数字口径；GPTZero 的数字口径；TMLR 的样本描述；ARIS 引文的完整句子和归属；OR 引文改为原文；补全 ICLR26-retro 的 URL；补上 AIRev26 的标题；补上 SciSlop 六项指标的定义。去掉 GitHub 星数。
- **lint v0.2.0**：修复盲测中漏掉的 ☠ 项（跨换行的水印、作者栏里的 LLM 名字、PLEASE FILL、.bbl 里的 agent 笔记），以及若干误报（IEEE 页眉、`\texttt` 里的代码名、合作者批注）；新增 R17 和 P13 两项仅供参考的检查。
- **skill**：写作 skill 加入"管线硬规则"（没有人类参与时只审不改）；审稿 skill 加入输入卫生检查、明确 triage 深度、基于 API 的引用核查、整数可行性检查和 worked examples。
- **补记**（v0.2.1 时补上）：共 83 条；P05 的来源中去掉 CycleResearcher（只在代码 docstring 里出现）；L03/L14 去重后 L03 AUC 0.94 → 0.93；重新校准后 L01 人类 p99 为 2.93；S02 计入 R 轴（review-loop 指纹）。

## v0.1 — 2026-10-05
- 第一版：定位文档、证据清单（L16 / S17 / R16 / P12 / H9，共 70 条）、两个 skill、slop_lint 及校准。
- 吸收了 Zhehao 的调研（证据分级、感知风险与可核实缺陷分开写），并复核了其中引用的 8 篇文献：都存在，只有一处会议名称有误（Juzek & Ward 是 COLING 2025，不是 ACL）。
- 校准（59 篇 2018–22 年人类论文，20 篇 AI 论文）：L08、L03、L10、L05、L04 区分度强；L02、S06 以及 R 层的词汇检查区分度弱。2026 年的 Claude 管线论文在 L 层几乎没有痕迹。据此把 L05、L08 上调到 ★★，并加入"L 层成簇规则"。
- 已知缺口：S01–S05（review-loop 痕迹）没有真实样本可以校准；没有 2025–26 年的现代人类对照组；Reddit 来源未复核。
