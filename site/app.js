/* Absent Author site. No framework, no build step. */
(function () {
  "use strict";

  // Set this once the GitHub repo exists (tools/set_repo.sh does it for you).
  const REPO = "https://github.com/THUROI0787/absent-author";

  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  /* ---------------- i18n ---------------- */
  const ZH = {
    nav_why: "为什么", nav_quad: "四象限", nav_ev: "证据", nav_skills: "Skills", nav_cal: "校准", nav_vision: "愿景",
    h1a: "<span class=\"nb\">科研和写作</span><span class=\"nb\">可以自动化，</span>", h1b: "署名的责任不能。",
    lede: "审稿人现在常常读到这样的论文：由 agent 从头到尾产出，却没有人类引导、核查或为之负责。Absent Author 是一份证据清单、两个 agent skill 和一个 lint，让这种“作者缺席”变得可见：每条判断都给出位置和原文，不输出“AI 概率”。",
    cta_ev: "浏览 83 条证据", cta_skills: "安装 skills",
    f1: "条证据，从措辞到产物", f2: "个 skill：作者用一个，审稿人用一个", f3: "盲测论文落在预期象限（首次小规模测试）",
    n0: "-ing 尾巴，只算写作", n1: "防御性写作", n2: "方法失败，改名叫审计", n3: "3-3-3 配方，没有理由", n4: "(78.0−73.1)/73.1 是 6.7%", n5: "承诺了，从未展示",
    verdict: "W2 · R3 → D 象限", verdict2: "只看语言痕迹最多只能给 W",
    deskp: "一段虚构的摘要。黄色标记是审稿人能指出来的证据；印章是筛查 skill 由此得出的结论。", replay: "再筛一次",
    why_h: "我们找的是缺席的作者，不是 AI。",
    why_p: "auto-research 没有问题，agent 可以完整地跑实验、记日志。问题在于一篇没有人引导、核查、负责的论文。这种缺席有三种。",
    a1h: "没人打磨", a1p: "写作由 AI 主导、无人认领：破折号泛滥、“不是 X 而是 Y”、防御性 caveat、没人定义的生造词、对失败实验的表演性诚实。",
    a2h: "没人引导", a2p: "没有人判断哪个问题值得问、计划失败后该怎么办：转成“审计”论文、theoryslop、玩具规模配宏大结论。",
    a3h: "没人核查", a3p: "最终产物从未被核对：编造的引用、聊天残留、正文和表格对不上的数字、承诺了却从未展示的分析。",
    defn: "slop 把核查一篇论文的成本转嫁给了审稿人。",
    defn_c: "转述 NeurIPS 2026 Position Paper Track 主席的说法：AI 生成的文本 “externalises the cost of verifying that work, imposing it on reviewers”。",
    q_h: "两个问题，四种论文。",
    q_p: "W 问写作是否由 AI 主导、无人打磨；R 问研究是否无人引导、无人核查。普通的质量问题记在单独的 Q 轴上，所以人类写的差论文永远不会被叫作 slop。",
    ax_r01: "R0–R1 · 研究有人引导", ax_r23: "R2–R3 · 引导或核查缺席", ax_w01: "W0–W1 · 有人打磨", ax_w23: "W2–W3 · AI 主导",
    qa_n: "正常的 AI 辅助工作", qa_s: "像审任何论文一样审。", qc_n: "镀金空壳", qc_s: "文字干净，研究没人管。",
    qb_n: "可以挽救", qb_s: "贡献真实，写作 AI 主导。", qd_n: "AI waste", qd_s: "没人引导，也没人核查。",
    sl_w: "写作 W", sl_r: "研究 R", sl_hint: "拖动滑块看论文落在哪里。圆点是六篇盲测论文。", strongest: "最强", prompts_h: "然后对你的 agent 说：", cite_h: "引用",
    p_h: "“审计论文”是怎么来的。",
    p_p: "auto-review loop 优化的是 LLM 审稿人的分数。主张失败时，换叙事比做新实验便宜，于是分数一路上涨，主张却消失了。下面这次运行引自",
    p_p2: " 的 README；其维护者后来也加入了反过度防御的规则，并开发了自己的审稿侧工具。",
    e_h: "证据清单。",
    e_p: "每一条都有强度、可以计入哪个轴、诚实的人类为什么也会触发它，以及来源。痕迹越容易被洗掉，它能证明的就越少。",
    all: "全部", lay_L: "L 语言", lay_S: "S 结构", lay_R: "R 研究", lay_P: "P 产物", lay_H: "H 人类迹象", any: "任意强度",
    search_l: "搜索证据", search_ph: "搜索：破折号、转向、引用……", loading: "正在加载证据清单……",
    s_h: "两个 skill，共用一份清单。",
    s_p: "纯 Markdown 的 skill，适用于 Claude Code、Codex 或任何能读 SKILL.md 的 agent。作者在投稿前跑把关，审稿人在写审稿意见前跑筛查。",
    ap_for: "给作者。自上而下：skill 提问，人类决定。",
    ap1: "故事与品味。", ap1d: "一句话测试、steering card、转向检查、规模与结论对照。",
    ap2: "论证。", ap2d: "caveat 收进一个 Limitations，生造词建术语表，related work 写成比较。",
    ap3: "核查。", ap3d: "每一条引用、每一个数字、代码与论文对照。",
    ap4: "句子，放在最后。", ap4d: "只修妨碍阅读的痕迹。绝不注入假的“人味”错别字或碎句。",
    ap5: "作者检查点。", ap5d: "针对这篇论文提出三个问题，由作者在署名前回答：是否理解、能否当面捍卫、是否愿意署名。",
    ap_rule: "没有人类作者时，skill 只审读、只返回问题。把一篇没人引导的论文打磨干净，只会把 D 变成 C。",
    sc_for: "给审稿人、AC 和合作者。证据优先，不给 AI 概率。",
    sc1: "铁证扫描。", sc1d: "按作者列表核对引用，查残留和水印。",
    sc2: "Steering card。", sc2d: "转向、承诺与展示、数字、规模、新颖性。",
    sc3: "结构、语言、反证。", sc3d: "五分钟；H 层证据可以抵消发现。",
    sc4: "分级与报告。", sc4d: "W、R、Q、标记、可审性；一段只谈研究内容的审稿意见，以及经 AC 转给作者的问题，按理解、捍卫、署名分组。",
    sc_rule: "对在审论文使用之前，请先确认会议的审稿人 LLM 政策。",
    copy: "复制", copied: "已复制",
    c_h: "我们测了什么，以及它不能告诉你什么。",
    c_p: "我们用 59 篇 ChatGPT 之前的 arXiv 论文对照 20 篇 AI 生成论文校准了 lint，然后在六篇事后才揭晓标签的文档上盲测了筛查 skill。",
    c_cap: "样本内、混杂时代因素：20 篇 AI 论文里 13 篇来自同一条管线。这些数字是表层痕迹的地图，不是检测器准确率。",
    bt1: "实际是什么", bt2: "筛查结果",
    bt_a: "人类写的 ACL 2018 论文", bt_b: "人类写的 2021 年论文，非母语作者", bt_c: "AI Scientist v2 workshop 论文（已披露）",
    bt_d: "AI Scientist v1 示例论文（已披露）", bt_e: "2026 年自主 agent 论文，已披露 agent 使用", bt_f: "2026 年全流程 auto-research 论文",
    bt_note: "两篇 2026 年论文几乎没有语言痕迹（L 簇 0/6 和 1/6）。暴露它们的是算术：同一配置在一张表里是 63.4、另一张表里是 57.2；“207 的 12.4%”不是整数；一条引用的 arXiv 号是 2409.XXXXX。",
    r_h: "它不是什么。",
    r1: "不是 AI 检测器。", r1d: "不给概率。2023 年的一项研究中，AI 检测器把约 61% 的非母语 TOEFL 作文判为 AI 所写。",
    r2: "语言痕迹从不定罪。", r2d: "L 层痕迹只计入写作轴，永远不计入研究轴。",
    r3: "新手不等于缺席。", r3d: "第一篇论文和非母语写作会触发好几条；它们只在和 R/P 层证据同时出现时才计数。",
    r4: "不是公开指控。", r4d: "审稿意见只写可核查的缺陷；来源问题作为作者能回答的问题交给 AC。",
    r5: "不是洗稿服务。", r5d: "写作 skill 不会替作者回答自己的问题，也不会在没有人类作者时打磨论文。",
    r6: "不反对 AI。", r6d: "重度 AI 执行，加上日志、代码和具体的 AI 声明，可审性评为 A+。",
    k_h: "一起让这份清单保持诚实。",
    k_p: "词表会过时，管线会学会清洗痕迹。只有审稿人持续提供真实案例，包括清单判错的案例，它才有用。",
    k1: "提议新证据", k1d: "你反复见到的一种模式，附一个例子，以及人类也会这样写的一种情形。",
    k2: "提交 field report", k2d: "一次已经结束的审稿中的匿名化案例，以及后来发生了什么。",
    k3: "报告误判", k3d: "筛查把一篇人类论文判错了。这类报告最重要。",
    foot: "© 2026 Ruoyu Zhao, Zhehao Zou, Jinheng Zhang, Yuting Chen, Jiaqi Wu, Chenyu Zhu。MIT 许可。建立在许多审稿人、skill 作者和会议主席的工作之上；所有参考见 SOURCES。",
    au_h: "作者", au_note: "* 共同一作 · † 项目负责人",
    v_h: "接下来会怎样。",
    v_p: "我们公开这份清单时就清楚：会有人用它来掩盖作者的缺席，而这正是清单要找的东西。",
    v1h: "它可能被滥用。", v1p: "任何人都可以把证据清单导入写作 agent，洗掉表层痕迹，包括聊天残留和管线水印。现有的改写工具已经能做到不少。这份清单不靠保密起作用。",
    v2h: "文字再干净，也藏不住没人核查的研究。", v2p: "洗文本最多降低写作轴的评级，降不了研究轴。一篇没人引导、没人核查的论文，洗干净后最多从 D 移到 C，而 C 正是筛查查得最严的地方：引用是否真实，数字能否复现，设计选择有没有人说得清。这些清单都给不了。我们有意不在措辞上较劲。",
    v3h: "文本能证明的越来越少。", v3p: "对很多论文来说，写作已经不是最难的部分，写得漂亮也越来越说明不了谁在为它负责。我们预计评价会转向只有在场的作者才能提供的东西：如实披露 AI 的使用，别人可以核查的产物（代码、日志、形式化证明），以及当面捍卫这项工作的能力。我们公开这份清单，也是为了让表层痕迹更早失去作用。",
    vq_l: "在一篇论文上署名之前，无论用没用 AI，先回答三个问题。",
    vq1: "你是否透彻理解它？", vq2: "你敢当面捍卫它吗？", vq3: "你愿意以自己的名字为它背书吗？",
    vq_src: "改写自中文媒体对", vq_src_a: "哈佛 CMSA“AI 时代的数学博士教育”峰会",
    vq_src2: "（2026 年 9 月）的评论。报告原文要求 AI 的使用应当“accelerate understanding, not bypass understanding”（加速理解，而非绕过理解），并要求学生对署在自己名下的数学内容的正确性与理解负责。",
    vc_h: "我们的承诺",
    vc1: "skill 只提出这些问题，从不代答。skill 以 MIT 许可开源，任何人都能改，所以这是我们坚持的默认做法，不是一把锁。", vc2: "不给 AI 概率。每条发现都附位置和原文。",
    vc3: "只有经人亲自核实的 ☠ 级证据，才能把举证责任转给作者。", vc4: "误判公开登记，并据此修改清单。",
  };
  const JA = {
    nav_why: "背景", nav_quad: "4 象限", nav_ev: "証拠", nav_skills: "スキル", nav_cal: "較正", nav_vision: "展望",
    h1a: "<span class=\"nb\">研究も執筆も、</span><span class=\"nb\">自動化できる。</span>", h1b: "<span class=\"nb\">著者の責任は、</span><span class=\"nb\">自動化できない。</span>",
    lede: "いま査読者のもとには、エージェントが最初から最後まで作り上げ、誰も方向づけず、確認もせず、責任も負っていない論文が届いています。Absent Author は、その「著者の不在」を見えるようにするための証拠リスト、2つのエージェント用スキル、そして lint です。判断にはすべて該当箇所と原文を添え、「AI 確率」は出しません。",
    cta_ev: "83 項目の証拠を見る", cta_skills: "スキルを導入する",
    f1: "項目の証拠（言い回しから成果物まで）", f2: "スキル（著者用と査読者用）", f3: "ブラインドテストで想定どおりの象限に入った論文（小規模な初回テスト）",
    n0: "-ing の文末：執筆のみ", n1: "防御的な書き方", n2: "失敗した手法を「監査」と言い換え", n3: "3-3-3 の構成、理由なし", n4: "(78.0−73.1)/73.1 は 6.7%", n5: "示すと言って、示していない",
    verdict: "W2 · R3 → 象限 D", verdict2: "言語の痕跡だけなら W にしか効かない",
    deskp: "架空の要旨です。黄色の箇所は査読者が指摘できる証拠、スタンプはスクリーニング用スキルがそこから下す結論です。", replay: "もう一度スクリーニング",
    why_h: "探しているのは AI ではなく、不在の著者です。",
    why_p: "自動化された研究そのものは問題ではありません。エージェントは実験を回し、ログを漏れなく残すことができます。問題は、誰も方向づけず、確認せず、責任を負わない論文です。その不在には3つの形があります。",
    a1h: "誰も推敲していない", a1p: "文章が AI 主導のまま放置されている：ダッシュの多用、「X ではなく Y」、防御的な但し書き、定義されない造語、失敗した実験についての演技的な正直さ。",
    a2h: "誰も方向づけていない", a2p: "どの問いに価値があるか、計画が失敗したらどうするかを、人間が判断していない：「監査」論文への転換、理論もどき、小さな実験に大きな主張。",
    a3h: "誰も確認していない", a3p: "最終成果物が一度も検証されていない：存在しない参考文献、チャットの残骸、本文と表で食い違う数値、予告されたまま示されない分析。",
    defn: "スロップとは、論文を検証するコストを査読者に押しつけることだ。",
    defn_c: "NeurIPS 2026 Position Paper Track のチェアの言葉を要約すると：AI が生成した文章は “externalises the cost of verifying that work, imposing it on reviewers”。",
    q_h: "2つの問い、4 種類の論文。",
    q_p: "W は、文章が AI 主導のまま推敲されていないかを問います。R は、研究が方向づけも検証もされていないかを問います。通常の弱点は別の品質軸 Q に記録するので、人間が書いた出来の悪い論文がスロップと呼ばれることはありません。",
    ax_r01: "R0–R1 · 研究は方向づけられている", ax_r23: "R2–R3 · 方向づけか検証が不在", ax_w01: "W0–W1 · 推敲されている", ax_w23: "W2–W3 · AI 主導",
    qa_n: "通常の AI 支援研究", qa_s: "他の論文と同じように査読する。", qc_n: "見せかけ", qc_s: "文章はきれい、研究は未確認。",
    qb_n: "立て直せる", qb_s: "貢献は本物、文章は AI 主導。", qd_n: "AI waste", qd_s: "誰も方向づけず、誰も確認していない。",
    sl_w: "執筆 W", sl_r: "研究 R", sl_hint: "スライダーを動かすと、論文がどこに入るかが分かります。点は 6 本のブラインドテスト論文です。", strongest: "最も強い", prompts_h: "そのうえでエージェントに：", cite_h: "引用",
    p_h: "「監査論文」はどこから来るのか。",
    p_p: "自動査読ループが最適化するのは LLM 査読者のスコアです。主張が崩れたとき、新しい実験より語り直しのほうが安上がりなので、スコアは上がり、主張は消えていきます。以下の実行例は",
    p_p2: " の README からの引用です。その開発者はその後、過剰な防御を抑えるルールと、査読者側のツールを自ら加えています。",
    e_h: "証拠リスト。",
    e_p: "各項目には、強さ、どの軸に数えてよいか、誠実な人間がなぜそれに引っかかりうるか、そして出典が付いています。消しやすい痕跡ほど、証拠としての重みを小さくしています。",
    all: "すべて", lay_L: "L 言語", lay_S: "S 構成", lay_R: "R 研究", lay_P: "P 成果物", lay_H: "H 人間の痕跡", any: "強さを問わない",
    search_l: "証拠を検索", search_ph: "検索（英語・中国語）：dash、pivot、references…", loading: "証拠リストを読み込んでいます…",
    s_h: "2つのスキルが1つのリストを共有する。",
    s_p: "Claude Code、Codex、または SKILL.md を読めるあらゆるエージェント向けの、プレーンな Markdown のスキルです。著者は投稿前に author-pass を、査読者は査読コメントを書く前に slop-screen を実行します。",
    ap_for: "著者向け。大きな問題から順に：スキルが問い、人間が決める。",
    ap1: "ストーリーと研究センス。", ap1d: "一文テスト、方向づけカード、転換のチェック、規模と主張の照合。",
    ap2: "論証。", ap2d: "但し書きは1つの Limitations 節にまとめ、造語には用語表を作り、関連研究は比較として書く。",
    ap3: "検証。", ap3d: "すべての参考文献、すべての数値、コードと論文の突き合わせ。",
    ap4: "文は最後に。", ap4d: "読みにくさにつながる痕跡だけを直す。「人間らしさ」を装った誤字や断片文は決して入れない。",
    ap5: "著者チェックポイント。", ap5d: "署名する前に著者が答える、その論文に即した3つの問い：理解しているか、面と向かって擁護できるか、名前を懸けられるか。",
    ap_rule: "人間の著者がいない場合、スキルは監査を行い、質問を返すだけです。方向づけのない論文を磨いても、D が C になるだけです。",
    sc_for: "査読者、AC（エリアチェア）、共著者向け。証拠が先、AI 確率は出さない。",
    sc1: "決定的証拠の確認。", sc1d: "著者リストで参考文献を照合し、残骸や透かしを探す。",
    sc2: "方向づけカード。", sc2d: "転換、予告された分析と実際の提示の照合、数値、規模、新規性。",
    sc3: "構成、言語、反証。", sc3d: "5 分程度。H 項目は指摘を打ち消せる。",
    sc4: "評価とレポート。", sc4d: "W、R、Q、フラグ、監査可能性。研究内容だけを扱う査読コメントの段落と、AC を通じて著者に送る質問（理解・擁護・署名の3つに分類）。",
    sc_rule: "審査中の投稿に使う前に、投稿先（会議・論文誌）の査読者向け LLM ポリシーを確認してください。",
    copy: "コピー", copied: "コピーしました",
    c_h: "測ったこと、そしてそこから言えないこと。",
    c_p: "ChatGPT 以前の arXiv 論文 59 本と AI 生成論文 20 本で lint を較正し、その後、ラベルを事後に明かす6つの文書でスクリーニング用スキルをブラインドテストしました。",
    c_cap: "サンプル内での評価であり、時期（ChatGPT 以前か以後か）による交絡もあります。AI 論文 20 本のうち 13 本は同じパイプライン由来です。この数値は表層の痕跡の地図として見てください。検出器の精度ではありません。",
    bt1: "実際の正体", bt2: "スクリーニング結果",
    bt_a: "人間が書いた ACL 2018 論文", bt_b: "人間が書いた 2021 年の論文、非ネイティブの著者", bt_c: "AI Scientist v2 のワークショップ論文（開示あり）",
    bt_d: "AI Scientist v1 のサンプル論文（開示あり）", bt_e: "2026 年の自律エージェント論文、エージェント使用を開示", bt_f: "2026 年の完全自動研究パイプライン論文",
    bt_note: "2026 年の2本には言語の痕跡がほとんどありませんでした（L クラスタ 0/6 と 1/6）。決め手は計算でした。同じ設定が一方の表では 63.4、別の表では 57.2。「207 の 12.4%」は整数にならない。arXiv ID が 2409.XXXXX の参考文献。",
    r_h: "これは何ではないか。",
    r1: "AI 検出器ではない。", r1d: "確率は出しません。2023 年のある研究では、AI 検出器が非ネイティブの TOEFL エッセイの約 61% を AI 生成と誤判定しました。",
    r2: "言語だけで断定しない。", r2d: "L 層の痕跡は執筆軸にのみ数え、研究軸には数えません。",
    r3: "未熟は不在ではない。", r3d: "初めての論文や非ネイティブの文章はいくつかの項目に引っかかります。R 層か P 層の証拠と同時にある場合にだけ数えます。",
    r4: "公開の告発ではない。", r4d: "公開される査読コメントには確認可能な欠陥だけを書きます。出自への懸念は、著者が答えられる質問として AC に伝えます。",
    r5: "ロンダリングの道具ではない。", r5d: "執筆用スキルは、著者への質問に自分で答えることも、人間の著者がいない論文を磨くこともしません。",
    r6: "AI に反対しているのではない。", r6d: "AI を大きく使っていても、ログ、コード、具体的な AI 使用の記述があれば、監査可能性は A+ になります。",
    v_h: "これからのこと。",
    v_p: "このリストを公開すれば、まさにそれが見つけようとする著者の不在を隠すために使う人も出てくるでしょう。それを承知のうえで公開します。",
    v1h: "悪用はされうる。", v1p: "証拠リストを執筆エージェントに読み込ませ、チャットの残骸やパイプラインの透かしも含めて表層の痕跡を消すことは、誰にでもできます。既存の言い換えツールでもかなりのことができます。このリストは、秘密にしておくことで機能するものではありません。",
    v2h: "文章を整えても、確認されていない研究は隠せない。", v2p: "文章を整えて下がるのは執筆軸の評価だけで、研究軸の評価は下がりません。誰も方向づけず確認もしていない論文は、せいぜい D から C に移るだけです。そして C こそ、スクリーニングが最も厳しく見る場所です。参考文献は実在するか、数値は再現するか、設計の理由を誰かが説明できるか。どんなチェックリストも、それの代わりにはなりません。言い回しで競うことは、意図してやめています。",
    v3h: "文章が証明できることは減っていく。", v3p: "多くの論文にとって、執筆はもはやいちばん難しい部分ではなく、よく書けた文章は、誰がそれに責任を負うのかをほとんど語りません。評価は、その場にいる著者にしか出せないものへ移っていくと考えています。AI 使用の開示、他人が確認できる成果物（コード、ログ、形式的証明）、そして対面で研究を擁護する力です。このリストを公開するのは、表層の痕跡が早く意味を失うようにするためでもあります。",
    vq_l: "論文に署名する前に、AI を使ったかどうかにかかわらず、3つの問いに答えてください。",
    vq1: "その論文を、隅々まで理解していますか？", vq2: "面と向かって問われても、擁護できますか？", vq3: "その論文に、自分の名前を懸けられますか？",
    vq_src: "この3つの問いは、", vq_src_a: "Harvard CMSA の Summit on PhD Math Education in the Age of AI",
    vq_src2: "（2026 年 9 月）をめぐる中国語メディアの論評を翻案したものです。同サミットの報告書自体は、AI の使用は “accelerate understanding, not bypass understanding”（理解を加速するものであって、理解を飛ばすものではない）べきだとし、学生は自分の名前で出す数学の正しさと理解に責任を持ち続けるべきだとしています。",
    vc_h: "私たちの約束",
    vc1: "スキルはこれらの問いを投げかけるだけで、代わりに答えることはしません。スキルは MIT ライセンスで誰でも書き換えられるので、これは私たちが守る既定の動作であって、鍵ではありません。", vc2: "AI 確率は出しません。すべての指摘に該当箇所と原文を添えます。",
    vc3: "立証責任を著者に移せるのは、人が自ら確認した決定的（☠）な証拠だけです。", vc4: "誤判定は公開で記録し、リストの修正に反映します。",
    k_h: "リストを正直に保つために。",
    k_p: "単語リストは古くなり、パイプラインは痕跡を消すことを覚えます。リストが役に立ち続けるのは、査読者が実際の事例を、リストが間違えた事例も含めて送り続けてくれる場合だけです。",
    k1: "証拠を提案する", k1d: "繰り返し目にするパターンを、例と、人間がそれを書いてしまう場合の一例とともに。",
    k2: "フィールドレポートを送る", k2d: "終わった査読からの匿名化した事例と、その後どうなったか。",
    k3: "誤判定を報告する", k3d: "スクリーニングが人間の論文に印を付けてしまった。こうした報告がいちばん重要です。",
    foot: "© 2026 Ruoyu Zhao, Zhehao Zou, Jinheng Zhang, Yuting Chen, Jiaqi Wu, Chenyu Zhu。MIT ライセンス。多くの査読者、スキル作者、会議のチェアの仕事の上に成り立っています。すべての参考文献は SOURCES にあります。",
    au_h: "著者", au_note: "* 同等貢献 · † プロジェクトリーダー",
  };
  const EN = {};
  const PH_EN = {};
  $$("[data-i18n]").forEach((el) => { EN[el.dataset.i18n] = el.innerHTML; });
  $$("[data-i18n-ph]").forEach((el) => { PH_EN[el.dataset.i18nPh] = el.placeholder; });
  EN.copied = "Copied";
  const DICT = { en: EN, zh: ZH, ja: JA };
  const HTML_LANG = { en: "en", zh: "zh-CN", ja: "ja" };
  // English by default; ?lang=zh|ja in a shared link, or the visitor's last choice, overrides it.
  const urlLang = (new URLSearchParams(location.search).get("lang") || "").toLowerCase();
  let lang = DICT[urlLang] ? urlLang : (DICT[store.get("aa-lang")] ? store.get("aa-lang") : "en");

  function t(k) { return (DICT[lang] && DICT[lang][k]) || EN[k] || k; }
  function pick(o) { return o[lang] || o.en; }

  function applyLang() {
    document.documentElement.lang = HTML_LANG[lang];
    $$("[data-i18n]").forEach((el) => {
      const v = t(el.dataset.i18n);
      if (v !== undefined) el.innerHTML = v;
    });
    $$("[data-i18n-ph]").forEach((el) => {
      el.placeholder = lang === "en" ? PH_EN[el.dataset.i18nPh] : (DICT[lang][el.dataset.i18nPh] || PH_EN[el.dataset.i18nPh]);
    });
    $$(".langs button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
    $$("img[data-fig]").forEach((img) => {
      const base = "assets/" + img.dataset.fig + (lang === "zh" ? "_cn" : "");
      img.src = base + ".svg";
      let src = img.parentElement.querySelector("source");
      if (!src && img.parentElement.tagName !== "PICTURE") {
        const pic = document.createElement("picture");
        img.replaceWith(pic); pic.appendChild(img);
        src = document.createElement("source"); src.media = "(prefers-color-scheme: dark)";
        pic.insertBefore(src, img);
      }
      if (src) src.srcset = base + "_dark.svg";
    });
    renderQuad();
    renderEvidence();
  }
  $$(".langs button").forEach((b) => b.addEventListener("click", () => {
    lang = b.dataset.lang; store.set("aa-lang", lang);
    const u = new URL(location.href);
    if (lang === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", lang);
    try { history.replaceState(null, "", u.pathname + u.search + u.hash); } catch (e) { /* sandboxed */ }
    applyLang();
  }));

  /* ---------------- repo links ---------------- */
  $$("a.repo").forEach((a) => { a.href = REPO; });
  $$("a.repo-link").forEach((a) => { a.href = REPO + (a.dataset.path || ""); });
  const code = $("#install-code");
  code.innerHTML = code.innerHTML.replace("https://github.com/THUROI0787/absent-author", REPO);

  /* ---------------- manuscript screening (the one orchestrated moment) ---------------- */
  const manuscript = $(".manuscript");
  function placeNotes() {
    if (window.innerWidth <= 640) { $$(".note").forEach((n) => { n.style.top = ""; }); return; }
    const base = manuscript.getBoundingClientRect().top;
    let last = -1000;
    $$(".note").forEach((n) => {
      const m = $(`mark[data-n="${n.dataset.n}"]`, manuscript);
      const rects = m.getClientRects();
      let y = (rects[0] ? rects[0].top : m.getBoundingClientRect().top) - base - 2;
      y = Math.max(y, last + 6);
      n.style.top = y + "px";
      last = y + n.offsetHeight;
    });
  }
  let timers = [];
  function screen() {
    timers.forEach(clearTimeout); timers = [];
    $$("mark, .note, #verdict", manuscript).forEach((el) => el.classList.remove("on"));
    placeNotes();
    const steps = $$(".note");
    if (reduce) {
      $$("mark, .note, #verdict", manuscript).forEach((el) => el.classList.add("on"));
      return;
    }
    steps.forEach((n, i) => {
      timers.push(setTimeout(() => {
        n.classList.add("on");
        $(`mark[data-n="${n.dataset.n}"]`, manuscript).classList.add("on");
      }, 500 + i * 520));
    });
    timers.push(setTimeout(() => $("#verdict").classList.add("on"), 500 + steps.length * 520 + 300));
  }
  $("#replay").addEventListener("click", screen);
  window.addEventListener("resize", placeNotes);

  /* ---------------- quadrants ---------------- */
  const QUAD = {
    en: {
      A: { h: "A · Normal AI-assisted work", who: "R0–R1 and W0–W1", li: ["Review it like any other paper.", "Using AI is not the problem; nothing to flag.", "If the paper is weak, that is a Q-axis judgement, not slop."] },
      B: { h: "B · Salvageable", who: "R0–R1 but W2–W3", li: ["The contribution stands; the writing is AI-led and unowned.", "Give a concrete rewrite list: which coined term to replace with which community term, where defensive passages should merge.", "Do not reject on writing alone, unless the prose stops you from verifying the claims."] },
      C: { h: "C · Veneer", who: "W0–W1 but R2–R3", li: ["Clean prose, unchecked research. Surface checks see nothing here.", "Review on substance: list the R findings one by one, with locations.", "At R3, suggest the AC ask for logs, code or a short author Q&A."] },
      D: { h: "D · AI waste", who: "W2–W3 and R2–R3", li: ["Score at reject level on verifiable R/P defects, and keep “AI-generated” out of the public review.", "Give the AC a confidential evidence table, phrased as questions the authors can answer.", "For any verified flag, cite the venue policy. Have a second person check one piece of evidence."] },
    },
    zh: {
      A: { h: "A · 正常的 AI 辅助工作", who: "R0–R1 且 W0–W1", li: ["像审任何论文一样审。", "用了 AI 不是问题，没有什么需要标记。", "如果论文本身较弱，那是 Q 轴的判断，不是 slop。"] },
      B: { h: "B · 可以挽救", who: "R0–R1 但 W2–W3", li: ["贡献成立；写作由 AI 主导、无人认领。", "给出具体的重写清单：哪个生造词换成哪个社区术语，哪些防御性段落该合并到哪里。", "不因写作单独拒稿，除非表述已经让你无法核实主张。"] },
      C: { h: "C · 镀金空壳", who: "W0–W1 但 R2–R3", li: ["文字干净，研究没人核查。表层检查在这里什么也看不到。", "按实质审：把 R 层发现逐条写出，并给出位置。", "R3 时，建议 AC 要求日志、代码或简短的作者问答。"] },
      D: { h: "D · AI waste", who: "W2–W3 且 R2–R3", li: ["以可核实的 R/P 层缺陷给出 reject 级评分，公开审稿意见里不写“AI 生成”。", "给 AC 一张保密的证据表，写成作者可以回答的问题。", "对已核实的标记引用会议政策；请第二个人复核至少一条证据。"] },
    },
    ja: {
      A: { h: "A · 通常の AI 支援研究", who: "R0–R1 かつ W0–W1", li: ["他の論文と同じように査読する。", "AI を使ったこと自体は問題ではない。指摘すべきことはない。", "論文が弱いなら、それは Q 軸の判断であってスロップではない。"] },
      B: { h: "B · 立て直せる", who: "R0–R1 だが W2–W3", li: ["貢献は成り立っている。文章は AI 主導で、誰も引き受けていない。", "具体的な書き直しリストを渡す：どの造語を、分野で定着したどの用語に置き換えるか、防御的な段落をどこにまとめるか。", "文章だけを理由にリジェクトしない。ただし、文章のせいで主張を検証できない場合は別。"] },
      C: { h: "C · 見せかけ", who: "W0–W1 だが R2–R3", li: ["文章はきれいで、研究は未確認。表層のチェックではここに何も見えない。", "実質で査読する：R の指摘を箇所とともに一つずつ挙げる。", "R3 なら、ログ、コード、または著者への短い質疑を求めるよう AC に提案する。"] },
      D: { h: "D · AI waste", who: "W2–W3 かつ R2–R3", li: ["検証可能な R/P の欠陥にもとづいてリジェクト相当のスコアをつけ、公開される査読コメントには「AI 生成」と書かない。", "AC には非公開の証拠表を、著者が答えられる質問の形で渡す。", "検証済みのフラグには投稿先のポリシーを引用する。少なくとも一つの証拠を別の人に確認してもらう。"] },
    },
  };
  let q = "D";
  function quadOf(w, r) { return (w >= 2 ? (r >= 2 ? "D" : "B") : (r >= 2 ? "C" : "A")); }
  function renderQuad() {
    const d = pick(QUAD)[q];
    $("#qp-h").textContent = d.h;
    $("#qp-who").textContent = d.who;
    $("#qp-list").innerHTML = d.li.map((x) => `<li>${x}</li>`).join("");
    $$(".qcell").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.q === q)));
  }
  $$(".qcell").forEach((b) => b.addEventListener("click", () => {
    q = b.dataset.q;
    const w = q === "B" || q === "D" ? 2 : 0, r = q === "C" || q === "D" ? 3 : 0;
    $("#sw").value = w; $("#sr").value = r; syncOut();
    renderQuad();
  }));
  function syncOut() { $("#ow").textContent = "W" + $("#sw").value; $("#or").textContent = "R" + $("#sr").value; }
  ["#sw", "#sr"].forEach((s) => $(s).addEventListener("input", () => {
    syncOut(); q = quadOf(+$("#sw").value, +$("#sr").value); renderQuad();
  }));

  /* ---------------- evidence explorer ---------------- */
  let EV = [], SRC = {}, showAll = false;
  const JA_NOTE = "（各項目の本文は英語です）";
  const filt = { layer: "all", str: "all", q: "" };
  const STARS = { skull: "☠", "3": "★★★", "2": "★★", "1": "★", i: "i", flag: "⚑" };
  const AXIS_LABEL = { en: { W: "W", R: "R", Q: "Q", H: "H" }, zh: { W: "W", R: "R", Q: "Q", H: "H" } };
  function shortAxis(a) { return strip(a).split("(")[0].replace(/\s+/g, " ").trim() || "?"; }
  function strip(html) { const d = document.createElement("div"); d.innerHTML = html; return d.textContent; }
  function matches(e) {
    if (filt.layer !== "all" && e.layer !== filt.layer) return false;
    if (filt.str !== "all") {
      if (filt.str === "strong" && !(e.sclass === "3" || e.sclass === "skull")) return false;
      if ((filt.str === "2" || filt.str === "1") && e.sclass !== filt.str) return false;
    }
    if (filt.q) {
      const hay = (e.id + " " + strip(e.en.name + e.en.form + e.en.fp + e.cn.name + e.cn.form + e.cn.fp + e.en.typ + e.en.effect)).toLowerCase();
      if (!hay.includes(filt.q)) return false;
    }
    return true;
  }
  function renderEvidence() {
    const box = $("#ev-list");
    if (!EV.length) return;
    const L = lang === "zh" ? "cn" : "en";
    const lab = pick({
      zh: { form: "典型表现", fp: "误判提醒", src: "来源", typ: "类型", eff: "效力", strength: "强度" },
      ja: { form: "典型的な形", fp: "誤判定についての注意", src: "出典", typ: "種類", eff: "効果", strength: "強さ" },
      en: { form: "Typical form", fp: "False-positive note", src: "Sources", typ: "Type", eff: "Effect", strength: "Strength" },
    });
    let rows = EV.filter(matches);
    const isDefault = filt.layer === "all" && filt.str === "all" && !filt.q;
    const total = rows.length;
    const truncated = isDefault && !showAll && !location.hash.startsWith("#ev-");
    if (truncated) rows = rows.filter((e) => ["R01","R02","R07","R09","P03","P01","S01","S02","S05","S06","L01","L08","R04","S17","H06","P14"].includes(e.id));
    $("#count").textContent = pick({ zh: `显示 ${rows.length} / ${EV.length} 条`, ja: `${EV.length} 件中 ${rows.length} 件を表示`, en: `Showing ${rows.length} of ${EV.length}` }) + (lang === "ja" ? JA_NOTE : "");
    if (!rows.length) {
      box.innerHTML = `<p style="padding:18px">${pick({ zh: "没有匹配的证据。换个关键词，或清除筛选。", ja: "一致する証拠はありません。別の語で検索するか、絞り込みを解除してください。", en: "No evidence matches. Try another word or clear the filters." })}</p>`;
      return;
    }
    box.innerHTML = rows.map((e) => {
      const x = Object.assign({}, e[L]);
      x.name = x.name.replace(/\s*[（(](?:F\d|merged into F\d[^)）]*|与 R01 同时出现时并入 F4|见 [A-Z]\d\d|see [A-Z]\d\d)[)）]\s*/g, " ").trim();
      const srcs = e.src.map((k) => {
        const s = SRC[k];
        return s && s.url ? `<a href="${s.url}" title="${(s.label || "").replace(/"/g, "&quot;")}">${k}</a>` : `<span>${k}</span>`;
      }).join("");
      const sym = e.layer === "H" ? "" : (STARS[e.sclass] || "");
      const body = e.layer === "H"
        ? `<div><h4>${lab.typ}</h4><p>${x.typ}</p></div><div><h4>${lab.eff}</h4><p>${x.effect}</p></div>`
        : `<div><h4>${lab.form}</h4><p>${x.form}</p></div><div><h4>${lab.strength}</h4><p>${x.strength}</p></div><div><h4>${lab.fp}</h4><p>${x.fp}</p></div>${srcs ? `<div><h4>${lab.src}</h4><div class="srcs">${srcs}</div></div>` : ""}`;
      return `<details class="ev" id="ev-${e.id}"><summary><span class="eid">${e.id}</span><span class="ename">${x.name}</span><span class="estr ${e.sclass}">${sym}</span><span class="eaxis" title="${strip(e.axis).replace(/"/g, "&quot;")}">${shortAxis(e.axis)}</span></summary><div class="body">${body}</div></details>`;
    }).join("");
    if (truncated) {
      box.insertAdjacentHTML("beforeend", `<button class="pill more" id="more" type="button">${pick({ zh: `显示全部 ${total} 条`, ja: `${total} 件すべてを表示`, en: `Show all ${total} items` })}</button>`);
      $("#more").addEventListener("click", () => { showAll = true; renderEvidence(); });
      $("#count").textContent = pick({ zh: `精选 ${rows.length} 条（共 ${total} 条）`, ja: `${total} 件から ${rows.length} 件を抜粋`, en: `A selection of ${rows.length} (of ${total})` }) + (lang === "ja" ? JA_NOTE : "");
    }
    openFromHash();
  }
  function openFromHash() {
    const m = location.hash.match(/^#ev-([LSRPH]\d\d)$/);
    if (!m) return;
    const el = document.getElementById("ev-" + m[1]);
    if (el) { el.open = true; }
  }
  function segment(id, key) {
    $$(`#${id} button`).forEach((b) => b.addEventListener("click", () => {
      $$(`#${id} button`).forEach((x) => x.setAttribute("aria-pressed", "false"));
      b.setAttribute("aria-pressed", "true");
      filt[key] = b.dataset.v;
      renderEvidence();
    }));
  }
  segment("f-layer", "layer");
  segment("f-str", "str");
  $("#q").addEventListener("input", (ev) => { filt.q = ev.target.value.trim().toLowerCase(); renderEvidence(); });
  // links to evidence ids anywhere on the page: reset filters so the row exists, then open it
  document.addEventListener("click", (ev) => {
    const a = ev.target.closest('a[href^="#ev-"]');
    if (!a) return;
    filt.layer = "all"; filt.str = "all"; filt.q = ""; $("#q").value = ""; showAll = true;
    $$("#f-layer button, #f-str button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === "all")));
    renderEvidence();
    setTimeout(() => { const el = document.getElementById(a.getAttribute("href").slice(1)); if (el) { el.open = true; } }, 0);
  });
  window.addEventListener("hashchange", openFromHash);

  Promise.all([fetch("data/evidence.json").then((r) => r.json()), fetch("data/sources.json").then((r) => r.json())])
    .then(([ev, src]) => { EV = ev; SRC = src; renderEvidence(); })
    .catch(() => {
      $("#ev-list").innerHTML = `<p style="padding:18px">${pick({ zh: "证据清单加载失败。请直接阅读 GitHub 上的 EVIDENCE.md。", ja: "証拠リストを読み込めませんでした。GitHub の EVIDENCE.md をご覧ください。", en: "The evidence list could not load. Read EVIDENCE.md on GitHub instead." })}</p>`;
    });

  /* ---------------- copy ---------------- */
  $("#copy").addEventListener("click", () => {
    const text = $("#install-code").innerText.split("\n").map((l) => l.replace(/\s+#.*$/, "")).join("\n");
    (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => {
      $("#copy").textContent = t("copied");
      setTimeout(() => { $("#copy").textContent = t("copy"); }, 1600);
    }).catch(() => {});
  });

  /* ---------------- start ---------------- */
  applyLang();
  syncOut();
  const start = () => setTimeout(screen, reduce ? 0 : 400);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start); else start();
})();
