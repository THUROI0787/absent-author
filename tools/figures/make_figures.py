#!/usr/bin/env python3
"""Render the README / site figures as self-contained SVGs (stdlib only).

    python tools/figures/make_figures.py

Writes assets/<name>.svg, <name>_dark.svg, <name>_cn.svg and <name>_cn_dark.svg for
banner, quadrant, layers, workflow, pivot and calibration. Every figure carries its own
background card. Fonts are system stacks, because GitHub does not load web fonts inside
<img>-embedded SVG.
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

THEMES = {
    "light": dict(CARD="#E9EDF1", PAPER="#FFFFFF", INK="#1D2430", MUTED="#5B6675", RULE="#D5DBE2",
                  COBALT="#2747C7", COBALT2="#7D93E0", GREY="#B8C0CA", GREY2="#D9DEE4", TRACK="#EEF1F4",
                  HILITE="#FFE45C", HILITE_EDGE="#C8B23A", FLAG="#C4362E", SHADOW="#C9D1DA", PAGE_LINE="#E3E7EC",
                  QA="#2F8F6B", QB="#B7791F", QC="#6A4BC4", QD="#C4362E", ON_CHIP="#FFFFFF"),
    "dark": dict(CARD="#151A21", PAPER="#1F2630", INK="#E5E9EF", MUTED="#9AA6B5", RULE="#2E3743",
                 COBALT="#93A6FF", COBALT2="#5E73C9", GREY="#4A5563", GREY2="#3A4350", TRACK="#2A323D",
                 HILITE="#FFE45C", HILITE_EDGE="#C8B23A", FLAG="#F07167", SHADOW="#0E1217", PAGE_LINE="#E3E7EC",
                 QA="#4FC08D", QB="#E0A040", QC="#A68BFF", QD="#F07167", ON_CHIP="#0E1217"),
}
SERIF = "Georgia, 'Times New Roman', 'Songti SC', 'Noto Serif CJK SC', 'Noto Serif SC', serif"
SANS = "'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif"
MONO = "ui-monospace, Menlo, Consolas, monospace"
C = {}  # current theme colours


def t(x, y, s, size=16, fill=None, family=SANS, weight="normal", anchor="start", style="normal"):
    fill = fill or C["INK"]
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}">{escape(s)}</text>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n'
            f'<rect width="{w}" height="{h}" rx="18" fill="{C["CARD"]}"/>\n{body}\n</svg>\n')


def silhouette(cx, top, s=1.0, color=None, width=2.2):
    color = color or C["COBALT"]
    return (f'<circle cx="{cx}" cy="{top + 14*s}" r="{12*s}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="5 4"/>'
            f'<path d="M {cx-24*s} {top+62*s} Q {cx-24*s} {top+32*s} {cx} {top+32*s} Q {cx+24*s} {top+32*s} {cx+24*s} {top+62*s}" '
            f'fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="5 4" stroke-linecap="round"/>')


def text_w(label, size):
    w = 0.0
    for ch in label:
        w += size * (1.0 if ord(ch) > 0x2E80 else 0.58)
    return w


def chip(x, y, label, color, size=15, h=34, pad=28):
    w = text_w(label, size) + pad
    return (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{C["PAPER"]}" stroke="{color}" stroke-width="1.6"/>'
            + t(x + w / 2, y + h / 2 + size * 0.36, label, size, color, SANS, "bold", "middle")), w


S = {
    "en": {
        "banner_title": "Absent Author",
        "banner_l1": "Research and writing can be automated.",
        "banner_l2": "Authorship cannot.",
        "banner_size": 27,
        "banner_sub1": "An evidence list, two agent skills and a lint for papers",
        "banner_sub2": "produced by AI with no responsible human author.",
        "chips": ["83 evidence items", "2 agent skills", "calibrated lint"],
        "notes": [("L08", "-ing tail"), ("S01", "defensive writing"), ("R01", "pivot to an audit"), ("R09", "16%? It is 6.7%")],
        "q_title": "Two questions, four kinds of paper",
        "q_sub": "W: was the writing left AI-led and unpolished?   R: was the research left unsteered and unchecked?",
        "q_cells": {
            "A": ("Normal AI-assisted work", ["Review it like any paper.", "Using AI is not the problem."]),
            "C": ("Veneer", ["Clean prose, unchecked research.", "Review the substance;", "ask the AC for logs or code."]),
            "B": ("Salvageable", ["Real contribution, AI-led prose.", "Give a concrete rewrite list;", "don't reject on writing alone."]),
            "D": ("AI waste", ["Reject on verifiable defects.", "Evidence to the AC as questions;", "venue policy for any flag."]),
        },
        "q_ax": ["R0–R1  research steered", "R2–R3  steering or checking absent", "W0–W1", "polished", "W2–W3", "AI-led"],
        "q_foot1": "Dots: blind test of 6 papers, labels revealed afterwards (2 human → A, 1 pipeline paper → C, 3 AI papers → D).",
        "q_foot2": "B and D are separated by the research axis alone. Ordinary weaknesses go to a separate Q axis.",
        "l_title": "Four layers, and what each may prove",
        "l_sub": "The easier a trace is to scrub, the less it is allowed to prove.",
        "l_rows": [("L", "Language", "words, punctuation, sentence moulds", "16 items", "trivial to scrub", 0.92, "W only", "W"),
                   ("S", "Structure", "caveats, coined terms, narrative", "18 items", "takes rewriting", 0.62, "W or R", "W"),
                   ("R", "Research", "pivots, scale vs. claims, numbers", "22 items", "takes real research", 0.30, "R", "R"),
                   ("P", "Artifacts", "references, residue, code, rebuttal", "18 items", "one slip is enough", 0.18, "R or flag", "F")],
        "l_cols": ["how easy to scrub", "counts toward"],
        "l_foot1": "Plus 9 H items, signs of a present author. Prose-only H can soften a ★★ finding;",
        "l_foot2": "artifacts (logs, code, pre-registration) can cancel one. Nothing cancels a verified flag.",
        "w_title": "Two skills, one evidence list",
        "w_lanes": [
            ("paper-author-pass", "for authors: the skill asks, the human decides",
             [("Story & taste", ["one-sentence test,", "pivot check,", "scale vs. claims"]),
              ("Argument", ["one Limitations", "section, term table,", "related-work synthesis"]),
              ("Verification", ["every reference,", "every number,", "code vs. paper"]),
              ("Sentences, last", ["fix what hurts", "reading; never fake", "human features"])],
             "Output: questions only a human author can answer. No human reachable → audit only."),
            ("paper-slop-screen", "for reviewers and ACs: evidence first, no AI probability",
             [("Iron-clad sweep", ["references checked", "by author list,", "residue, watermarks"]),
              ("Steering card", ["pivot, promised vs.", "shown, numbers,", "scale, novelty"]),
              ("Counter-evidence", ["structure and", "language; signs of", "a present author"]),
              ("Grade & report", ["W, R, Q, flags,", "auditability; review", "+ note to the AC"])],
             "Output: every finding with a location and a verbatim quote."),
        ],
        "w_pre": "lint",
        "p_title": "Anatomy of a pivot",
        "p_sub": "Blue: score progression of a real run, quoted from ARIS's README (rounds 1–4). Red: illustrative.",
        "p_rounds": [("Added standard metrics,", "found metric decoupling"), ("Key claim failed to", "reproduce; pivoted narrative"),
                     ("Large seed study killed", "main improvement claim"), ("Diagnostic evidence", "solidified; submission ready")],
        "p_leg": ["LLM-reviewer score", "original claim", "(illustrative)"],
        "p_foot1": "The score rises while the original claim disappears. A reader later sees evidence item R01:",
        "p_foot2": "a diagnostic framing on top of a leftover method skeleton.",
        "c_title": "What the surface lint can and cannot see",
        "c_sub": "AUC per check: {h} pre-ChatGPT arXiv papers vs {a} AI-generated papers (0.5 = no separation).",
        "c_foot1": "Strong in-sample separation on 2024–25 papers, but two 2026 Claude-pipeline papers showed almost none of it.",
        "c_foot2": "Language traces may only support the writing axis, and a clean lint report proves nothing.",
        "c_names": {"L08": "-ing tails", "L03": "AI lexicon cluster", "L10": "list-ification", "L05": "distanced reporting",
                    "L04": "transition chains", "L15": "flat rhythm", "P05": "pipeline watermark", "L07": "hype words",
                    "L01": "em-dash density", "P02-todo": "TODO / (?) placeholders", "L06": "stacked hedges",
                    "L14": "register words", "S02": "caveat diffusion", "R01": "pivot vocabulary", "L16": "chatty register",
                    "L02": "'not X but Y'", "S01": "defensive hedges", "S06": "coined-term candidates", "P06": "LaTeX comments"},
    },
    "cn": {
        "banner_title": "Absent Author",
        "banner_l1": "科研和写作可以自动化，",
        "banner_l2": "署名的责任不能。",
        "banner_size": 31,
        "banner_sub1": "一份证据清单、两个 agent skill 和一个 lint，",
        "banner_sub2": "用来识别没有负责任的人类作者的 AI 论文。",
        "chips": ["83 条证据", "2 个 skill", "校准过的 lint"],
        "notes": [("L08", "-ing 尾巴"), ("S01", "防御性写作"), ("R01", "转成审计论文"), ("R09", "16%？其实是 6.7%")],
        "q_title": "两个问题，四种论文",
        "q_sub": "W：写作是否由 AI 主导、无人打磨？   R：研究是否无人引导、无人核查？",
        "q_cells": {
            "A": ("正常的 AI 辅助工作", ["像审任何论文一样审。", "用了 AI 不是问题。"]),
            "C": ("镀金空壳", ["文字干净，研究没人核查。", "按实质审；", "请 AC 要求日志或代码。"]),
            "B": ("可以挽救", ["贡献真实，写作 AI 主导。", "给出具体的重写清单；", "不因写作单独拒稿。"]),
            "D": ("AI waste", ["以可核实的缺陷拒稿。", "证据作为问题交给 AC；", "有标记时按会议政策处理。"]),
        },
        "q_ax": ["R0–R1  研究有人引导", "R2–R3  引导或核查缺席", "W0–W1", "有人打磨", "W2–W3", "AI 主导"],
        "q_foot1": "圆点：6 篇论文的盲测，标签事后揭晓（2 篇人类论文 → A，1 篇管线论文 → C，3 篇 AI 论文 → D）。",
        "q_foot2": "B 和 D 只由研究轴区分。普通的质量问题记在单独的 Q 轴。",
        "l_title": "四层证据，各自能证明什么",
        "l_sub": "痕迹越容易被洗掉，它能证明的就越少。",
        "l_rows": [("L", "语言", "词语、标点、句式模板", "16 条", "一洗就掉", 0.92, "只计 W", "W"),
                   ("S", "结构", "caveat、生造词、叙事", "18 条", "要重写才能去掉", 0.62, "W 或 R", "W"),
                   ("R", "研究", "转向、规模与结论、数字", "22 条", "要真做研究", 0.30, "R", "R"),
                   ("P", "产物", "引用、残留、代码、rebuttal", "18 条", "一次疏忽就够", 0.18, "R 或标记", "F")],
        "l_cols": ["多容易洗掉", "计入"],
        "l_foot1": "另有 9 条 H：作者在场的迹象。纯文字的 H 能把一条 ★★ 降一级；",
        "l_foot2": "产物（日志、代码、预注册）可以抵消一条发现。已核实的标记无法抵消。",
        "w_title": "两个 skill，一份证据清单",
        "w_lanes": [
            ("paper-author-pass", "给作者：skill 提问，人类决定",
             [("故事与品味", ["一句话测试、", "转向检查、", "规模与结论对照"]),
              ("论证", ["caveat 收进一个", "Limitations，术语表，", "related work 写成比较"]),
              ("核查", ["每一条引用、", "每一个数字、", "代码与论文对照"]),
              ("句子，最后做", ["只修妨碍阅读的；", "绝不伪造", "“人味”"])],
             "输出：只有人类作者能回答的问题。没有人类参与时只审读。"),
            ("paper-slop-screen", "给审稿人和 AC：证据优先，不给 AI 概率",
             [("铁证扫描", ["按作者列表", "核对引用，", "查残留与水印"]),
              ("Steering card", ["转向、承诺与展示、", "数字、规模、", "新颖性"]),
              ("反证", ["结构与语言；", "作者在场的", "迹象"]),
              ("分级与报告", ["W、R、Q、标记、", "可审性；审稿意见", "+ 给 AC 的说明"])],
             "输出：每条发现都带位置和原文。"),
        ],
        "w_pre": "lint",
        "p_title": "一次转向的解剖",
        "p_sub": "蓝线：一次真实运行的分数变化，引自 ARIS 的 README（第 1–4 轮）。红线：示意。",
        "p_rounds": [("加入标准指标，", "发现指标解耦"), ("核心主张无法复现，", "转换叙事"),
                     ("大规模 seed 实验", "推翻主要改进"), ("诊断证据确立，", "可以投稿")],
        "p_leg": ["LLM 审稿分数", "原始主张", "（示意）"],
        "p_foot1": "分数一路上涨，原始主张却消失了。读者后来看到的就是证据 R01：",
        "p_foot2": "诊断性的包装之下，留着一副方法论文的骨架。",
        "c_title": "表层 lint 能看到什么、看不到什么",
        "c_sub": "各检查的 AUC：{h} 篇 ChatGPT 之前的 arXiv 论文 对 {a} 篇 AI 生成论文（0.5 = 无法区分）。",
        "c_foot1": "在 2024–25 年的论文上样本内区分很强，但两篇 2026 年的 Claude 管线论文几乎没有这些痕迹。",
        "c_foot2": "所以语言痕迹只能支撑写作轴；lint 报告干净什么也证明不了。",
        "c_names": {"L08": "-ing 尾巴", "L03": "AI 词簇", "L10": "列表化", "L05": "疏离式报告",
                    "L04": "连接词流水线", "L15": "节奏单一", "P05": "管线水印", "L07": "营销腔",
                    "L01": "破折号密度", "P02-todo": "TODO / (?) 占位", "L06": "叠加对冲",
                    "L14": "跨语域用词", "S02": "caveat 弥散", "R01": "转向用词", "L16": "聊天腔",
                    "L02": "“不是 X 而是 Y”", "S01": "防御性对冲", "S06": "生造词候选", "P06": "LaTeX 注释"},
    },
}


S["ja"] = dict(S["en"], **{
    "banner_l1": "研究も執筆も、自動化できる。",
    "banner_l2": "著者の責任は、自動化できない。",
    "banner_size": 29,
    "banner_sub1": "著者が不在の AI 論文を見分けるための、",
    "banner_sub2": "証拠リスト、2つのエージェント用スキル、lint。",
    "chips": ["83 項目の証拠", "2つのスキル", "較正済みの lint"],
    "notes": [("L08", "-ing の文末"), ("S01", "防御的な書き方"), ("R01", "「監査」への転換"), ("R09", "16%？ 実は 6.7%")],
    "serif": "Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', 'Noto Serif JP', serif",
    "sans": "'Helvetica Neue', Helvetica, Arial, 'Hiragino Sans', 'Yu Gothic', 'Noto Sans CJK JP', sans-serif",
})


# ---- 1. banner ---------------------------------------------------------------------------
def banner(L):
    W, H = 1200, 440
    b = []
    px, py, pw, ph = 48, 40, 400, 360
    b.append(f'<rect x="{px+6}" y="{py+8}" width="{pw}" height="{ph}" rx="5" fill="{C["SHADOW"]}"/>')
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="5" fill="#FFFFFF"/>')
    cx = px + pw / 2
    b.append(t(cx, py + 46, "Adaptive Gradient Scaling:", 19, "#1D2430", SERIF, "bold", "middle"))
    b.append(t(cx, py + 70, "An Audit", 19, "#1D2430", SERIF, "bold", "middle"))
    b.append(f'<rect x="{cx-96}" y="{py+86}" width="192" height="30" rx="15" fill="none" stroke="#2747C7" stroke-width="1.6" stroke-dasharray="5 4"/>')
    b.append(t(cx, py + 107, "Anonymous Author(s)", 15, "#2747C7", SERIF, "normal", "middle", "italic"))
    lines = [("…scaling plays a pivotal role,", None), ("highlighting the need for robustness.", 0),
             ("We do not claim it is optimal;", 1), ("contrary to our expectations, it", 2),
             ("fails, so we audit the schedule.", None), ("Accuracy rises 16% (73.1 → 78.0).", 3)]
    yy = py + 150
    note_y = {}
    for text, tag in lines:
        if tag is not None:
            b.append(f'<rect x="{px+22}" y="{yy-15}" width="{pw-44}" height="20" fill="#FFE45C" opacity="0.85"/>')
            note_y[tag] = yy - 5
        b.append(t(px + 26, yy, text, 15.5, "#1D2430", SERIF))
        yy += 27
    for i in range(2):
        b.append(f'<rect x="{px+26}" y="{yy+4+i*16}" width="{pw-60-i*70}" height="6" rx="3" fill="{C["PAGE_LINE"]}"/>')
    for i, (tag, lab) in enumerate(L["notes"]):
        y = note_y[i]
        col = C["FLAG"] if tag == "R09" else C["COBALT"]
        b.append(f'<path d="M {px+pw-18} {y} L {px+pw+30} {y}" stroke="{col}" stroke-width="1.6"/>')
        b.append(f'<rect x="{px+pw+32}" y="{y-13}" width="52" height="26" rx="13" fill="{col}"/>')
        b.append(t(px + pw + 58, y + 5.5, tag, 15, C["ON_CHIP"], SANS, "bold", "middle"))
        b.append(t(px + pw + 92, y + 6, lab, 16, col))
    X = 700
    b.append(silhouette(X + 28, 66, 1.2))
    serif, sans = L.get("serif", SERIF), L.get("sans", SANS)
    bs = L.get("banner_size", 31)
    b.append(t(X + 82, 116, L["banner_title"], 50, C["INK"], SERIF, "bold"))
    b.append(t(X, 180, L["banner_l1"], bs, C["INK"], serif))
    b.append(t(X, 220, L["banner_l2"], bs, C["COBALT"], serif, "600"))
    b.append(f'<line x1="{X}" y1="250" x2="{X+450}" y2="250" stroke="{C["RULE"]}" stroke-width="1.5"/>')
    b.append(t(X, 284, L["banner_sub1"], 18, C["MUTED"], sans))
    b.append(t(X, 310, L["banner_sub2"], 18, C["MUTED"], sans))
    cx2 = X
    for i, lab in enumerate(L["chips"]):
        el, w = chip(cx2, 342, lab, C["COBALT"] if i == 1 else C["INK"], 14, 34, 24)
        b.append(el)
        cx2 += w + 10
    sep = "" if L["banner_l1"][-1] in "，。、" else " "
    return svg(W, H, "\n".join(b), f"Absent Author: {L['banner_l1']}{sep}{L['banner_l2']}")


# ---- 2. quadrant -------------------------------------------------------------------------
def quadrant(L):
    W, H = 1000, 720
    b = [t(56, 62, L["q_title"], 32, C["INK"], SERIF, "bold"), t(56, 94, L["q_sub"], 16.5, C["MUTED"])]
    ox, oy, cw, ch = 150, 146, 392, 220
    cols = {"A": C["QA"], "B": C["QB"], "C": C["QC"], "D": C["QD"]}
    pos = {"A": (0, 0), "C": (1, 0), "B": (0, 1), "D": (1, 1)}
    for k, (name, lines) in L["q_cells"].items():
        col, row = pos[k]
        x, y = ox + col * (cw + 14), oy + row * (ch + 14)
        c = cols[k]
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="{C["PAPER"]}" stroke="{c}" stroke-width="2"/>')
        b.append(f'<rect x="{x}" y="{y}" width="10" height="{ch}" rx="5" fill="{c}"/>')
        b.append(t(x + 32, y + 60, k, 48, c, SERIF, "bold"))
        b.append(t(x + 82, y + 52, name, 23, C["INK"], SERIF, "bold"))
        for i, ln in enumerate(lines):
            b.append(t(x + 32, y + 104 + i * 26, ln, 17, C["INK"]))
    ax = L["q_ax"]
    b.append(t(ox + cw / 2, oy - 14, ax[0], 15, C["MUTED"], SANS, "bold", "middle"))
    b.append(t(ox + cw * 1.5 + 14, oy - 14, ax[1], 15, C["MUTED"], SANS, "bold", "middle"))
    b.append(t(ox - 20, oy + ch / 2, ax[2], 15, C["MUTED"], SANS, "bold", "end"))
    b.append(t(ox - 20, oy + ch / 2 + 20, ax[3], 14, C["MUTED"], SANS, "normal", "end"))
    b.append(t(ox - 20, oy + ch * 1.5 + 14, ax[4], 15, C["MUTED"], SANS, "bold", "end"))
    b.append(t(ox - 20, oy + ch * 1.5 + 34, ax[5], 14, C["MUTED"], SANS, "normal", "end"))
    dots = [(0, 0, 0.84), (0, 0, 0.90), (1, 0, 0.90), (1, 1, 0.78), (1, 1, 0.84), (1, 1, 0.90)]
    for col, row, fx in dots:
        x = ox + col * (cw + 14) + cw * fx
        y = oy + row * (ch + 14) + 40
        b.append(f'<circle cx="{x:.0f}" cy="{y}" r="7" fill="{C["INK"]}" stroke="{C["PAPER"]}" stroke-width="2"/>')
    fy = oy + 2 * ch + 14 + 44
    b.append(t(56, fy, L["q_foot1"], 15, C["MUTED"]))
    b.append(t(56, fy + 26, L["q_foot2"], 15, C["INK"], SANS, "bold"))
    return svg(W, H, "\n".join(b), "Quadrant chart: writing axis W by research axis R")


# ---- 3. layers ---------------------------------------------------------------------------
def layers(L):
    W, H = 1000, 600
    b = [t(56, 62, L["l_title"], 32, C["INK"], SERIF, "bold"), t(56, 94, L["l_sub"], 17, C["MUTED"])]
    b.append(t(560, 132, L["l_cols"][0], 14, C["MUTED"], SANS, "bold"))
    b.append(t(944, 132, L["l_cols"][1], 14, C["MUTED"], SANS, "bold", "end"))
    for i, (k, name, what, n, scrub, frac, axis, kind) in enumerate(L["l_rows"]):
        y = 146 + i * 96
        b.append(f'<rect x="56" y="{y}" width="888" height="82" rx="12" fill="{C["PAPER"]}" stroke="{C["RULE"]}"/>')
        b.append(t(92, y + 56, k, 44, C["COBALT"], SERIF, "bold", "middle"))
        b.append(t(132, y + 36, name, 22, C["INK"], SERIF, "bold"))
        b.append(t(132, y + 62, what, 16.5, C["MUTED"]))
        b.append(t(560, y + 30, n, 14.5, C["MUTED"], SANS, "bold"))
        b.append(f'<rect x="560" y="{y+40}" width="190" height="11" rx="5.5" fill="{C["TRACK"]}"/>')
        b.append(f'<rect x="560" y="{y+40}" width="{190*frac:.0f}" height="11" rx="5.5" fill="{C["HILITE"]}" stroke="{C["HILITE_EDGE"]}" stroke-width="0.8"/>')
        b.append(t(560, y + 72, scrub, 14.5, C["MUTED"]))
        col = {"W": C["COBALT"], "R": C["INK"], "F": C["FLAG"]}[kind]
        el, w = chip(0, 0, axis, col, 15, 34, 30)
        b.append(f'<g transform="translate({924 - w:.0f},{y+24})">{el}</g>')
    b.append(t(56, 548, L["l_foot1"], 15.5, C["MUTED"]))
    b.append(t(56, 572, L["l_foot2"], 15.5, C["MUTED"]))
    return svg(W, H, "\n".join(b), "Evidence layers and what each may count toward")


# ---- 4. workflow -------------------------------------------------------------------------
def workflow(L):
    W, H = 1000, 640
    b = [f'<defs><marker id="arr" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto">'
         f'<path d="M0 0 L9 4 L0 8 z" fill="{C["MUTED"]}"/></marker></defs>',
         t(56, 62, L["w_title"], 32, C["INK"], SERIF, "bold")]
    for li, (name, sub, steps, tail) in enumerate(L["w_lanes"]):
        y = 112 + li * 262
        col = C["COBALT"] if li == 0 else C["INK"]
        b.append(t(56, y, name, 22, col, MONO, "bold"))
        b.append(t(56, y + 26, sub, 16.5, C["MUTED"]))
        el, w = chip(56, y + 91, L["w_pre"], C["MUTED"], 14, 30, 26)
        b.append(el)
        x0 = 56 + w + 22
        b.append(f'<line x1="{56+w+2:.0f}" y1="{y+106}" x2="{x0-4:.0f}" y2="{y+106}" stroke="{C["MUTED"]}" stroke-width="1.6" marker-end="url(#arr)"/>')
        bw, gap = 186, 18
        for i, (head, body) in enumerate(steps):
            bx = x0 + i * (bw + gap)
            b.append(f'<rect x="{bx:.0f}" y="{y+42}" width="{bw}" height="128" rx="12" fill="{C["PAPER"]}" stroke="{col}" stroke-width="1.7"/>')
            b.append(t(bx + 16, y + 72, f"{i+1}  {head}", 17, C["INK"], SANS, "bold"))
            for j, ln in enumerate(body):
                b.append(t(bx + 16, y + 100 + j * 21, ln, 15, C["MUTED"]))
            if i < len(steps) - 1:
                b.append(f'<line x1="{bx+bw+2:.0f}" y1="{y+106}" x2="{bx+bw+gap-3:.0f}" y2="{y+106}" stroke="{C["MUTED"]}" stroke-width="1.6" marker-end="url(#arr)"/>')
        b.append(t(56, y + 202, tail, 16, col, SANS, "bold"))
    return svg(W, H, "\n".join(b), "Workflow of the two skills")


# ---- 5. pivot ----------------------------------------------------------------------------
def pivot(L):
    W, H = 1000, 540
    b = [t(56, 60, L["p_title"], 32, C["INK"], SERIF, "bold"), t(56, 92, L["p_sub"], 16, C["MUTED"])]
    x0, x1, ytop, ybot = 140, 740, 150, 360
    xs = [x0 + i * (x1 - x0) / 3 for i in range(4)]
    scores = [6.5, 6.8, 7.0, 7.5]
    claim = [0.95, 0.55, 0.25, 0.10]

    def ys(v):
        return ybot - (v - 6.0) / (8.0 - 6.0) * (ybot - ytop)

    def yc(c):
        return ybot - c * (ybot - ytop)
    b.append(f'<polyline points="{" ".join(f"{x:.0f},{yc(c):.0f}" for x, c in zip(xs, claim))}" fill="none" stroke="{C["FLAG"]}" stroke-width="3" stroke-dasharray="8 6"/>')
    b.append(f'<polyline points="{" ".join(f"{x:.0f},{ys(v):.0f}" for x, v in zip(xs, scores))}" fill="none" stroke="{C["COBALT"]}" stroke-width="4"/>')
    for i, (x, v, c) in enumerate(zip(xs, scores, claim)):
        b.append(f'<circle cx="{x:.0f}" cy="{yc(c):.0f}" r="5.5" fill="{C["FLAG"]}"/>')
        b.append(f'<circle cx="{x:.0f}" cy="{ys(v):.0f}" r="7.5" fill="{C["COBALT"]}" stroke="{C["CARD"]}" stroke-width="2.5"/>')
        red_above = yc(c) < ys(v)
        ly = ys(v) + 30 if red_above else ys(v) - 16
        b.append(t(x, ly, f"{v}/10", 17, C["COBALT"], SANS, "bold", "middle"))
        l1, l2 = L["p_rounds"][i]
        b.append(t(x, 404, l1, 15, C["INK"], SANS, "normal", "middle"))
        b.append(t(x, 425, l2, 15, C["INK"], SANS, "normal", "middle"))
    b.append(f'<line x1="{x0-60}" y1="{ybot+14}" x2="{x1+70}" y2="{ybot+14}" stroke="{C["RULE"]}" stroke-width="1.5"/>')
    lg = L["p_leg"]
    b.append(t(x1 + 90, ys(7.5) + 6, lg[0], 16, C["COBALT"], SANS, "bold"))
    b.append(t(x1 + 90, yc(0.10) + 6, lg[1], 16, C["FLAG"], SANS, "bold"))
    b.append(t(x1 + 90, yc(0.10) + 28, lg[2], 15, C["FLAG"]))
    b.append(t(56, 480, L["p_foot1"], 16.5, C["INK"]))
    b.append(t(56, 506, L["p_foot2"], 16.5, C["INK"]))
    return svg(W, H, "\n".join(b), "Anatomy of a pivot: reviewer score rises while the claim disappears")


# ---- 6. calibration ----------------------------------------------------------------------
def calibration(L):
    d = json.loads((ROOT / "tools" / "calibration" / "calibration_results.json").read_text())
    st = d["stats"]
    names = L["c_names"]
    keys = sorted(names, key=lambda k: -st[k]["auc"])
    W, rowh = 1000, 30
    H = 160 + rowh * len(keys) + 100
    b = [t(56, 60, L["c_title"], 32, C["INK"], SERIF, "bold"),
         t(56, 92, L["c_sub"].format(h=d["meta"]["n_human"], a=d["meta"]["n_ai"]), 16, C["MUTED"])]
    x0, x1, y0 = 330, 900, 132

    def X(a):
        return x0 + (a - 0.3) / 0.7 * (x1 - x0)
    for a in (0.3, 0.5, 0.7, 0.9, 1.0):
        b.append(f'<line x1="{X(a):.0f}" y1="{y0-8}" x2="{X(a):.0f}" y2="{y0 + rowh*len(keys)}" stroke="{C["RULE"]}" stroke-width="{2 if a == 0.5 else 1}"/>')
        b.append(t(X(a), y0 + rowh * len(keys) + 22, f"{a:.1f}", 14, C["MUTED"], SANS, "normal", "middle"))
    for i, k in enumerate(keys):
        a = st[k]["auc"]
        y = y0 + i * rowh
        col = C["COBALT"] if a >= 0.8 else (C["COBALT2"] if a >= 0.65 else C["GREY"])
        b.append(t(x0 - 14, y + 19, f"{k.split('-')[0]}  {names[k]}", 15.5, C["INK"], SANS, "normal", "end"))
        if a >= 0.5:
            b.append(f'<rect x="{X(0.5):.0f}" y="{y+5}" width="{max(2, X(a)-X(0.5)):.0f}" height="18" rx="3" fill="{col}"/>')
        else:
            b.append(f'<rect x="{X(a):.0f}" y="{y+5}" width="{X(0.5)-X(a):.0f}" height="18" rx="3" fill="{C["GREY2"]}"/>')
        b.append(t(max(X(a), X(0.5)) + 8, y + 19, f"{a:.2f}", 14.5, C["MUTED"]))
    yb = y0 + rowh * len(keys) + 62
    b.append(t(56, yb, L["c_foot1"], 15.5, C["INK"]))
    b.append(t(56, yb + 24, L["c_foot2"], 15.5, C["INK"], SANS, "bold"))
    return svg(W, H, "\n".join(b), "Calibration chart: AUC per lint check")


if __name__ == "__main__":
    makers = {"banner": banner, "quadrant": quadrant, "layers": layers, "workflow": workflow,
              "pivot": pivot, "calibration": calibration}
    n = 0
    for lang in ("en", "cn"):
        for theme in ("light", "dark"):
            C.clear()
            C.update(THEMES[theme])
            for name, fn in makers.items():
                suffix = ("_cn" if lang == "cn" else "") + ("_dark" if theme == "dark" else "")
                (OUT / f"{name}{suffix}.svg").write_text(fn(S[lang]), encoding="utf-8")
                n += 1
    for theme in ("light", "dark"):  # Japanese: banner only (README_JA); other figures use English
        C.clear()
        C.update(THEMES[theme])
        (OUT / f"banner_ja{'_dark' if theme == 'dark' else ''}.svg").write_text(banner(S["ja"]), encoding="utf-8")
        n += 1
    print(f"wrote {n} figures to {OUT}")
