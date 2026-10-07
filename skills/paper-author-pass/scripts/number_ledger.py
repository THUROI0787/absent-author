#!/usr/bin/env python3
"""number_ledger.py: list every number in a paper and flag internal inconsistencies (R09, R17).

Usage: python tools/number_ledger.py paper.(tex|md|txt)|dir [--json] [-o out.md] [--min-values 2]

Steps: (1) extract numbers with ~8 words of context and file:line/section; (2) map each to an
entity (gpu_hours, duration:search, elites, ...) with a keyword+unit dictionary, or to a generic
entity keyed by the noun after an integer; (3) flag entities stated with >= 2 distinct values;
(4) recompute arithmetic stated in text; (5) recompute Avg/Total/Delta/Ratio cells in tables.
Everything is a candidate for a human to read, never a verdict. Stdlib only, Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slop_lint as SL  # noqa: E402  (file loading, \input inlining, line map, md/txt headings)

HEADER = ("Candidates only: a human must read each context. Rounding, different settings and "
          "different subsets are common legitimate reasons.")
NUM = r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+)"
MULT = {"k": 1e3, "K": 1e3, "M": 1e6, "B": 1e9}
TOKEN_RX = re.compile(
    r"(?P<sum>%(n)s(?:\s*\+\s*%(n)s)+(?:\s*=\s*%(n)s)?)"
    r"|(?P<prod>%(n)s\s*[×x]\s*%(n)s(?:\s*[×x]\s*%(n)s)*(?:\s*\(?\s*=\s*%(n)s[kKMB]?)?)"
    r"|(?P<approx>[~≈]\s*)?(?P<num>%(n)s)(?:(?P<rsep>–|-)(?P<num2>%(n)s))?"
    r"(?P<suf>\s?%%|[kKMB](?![A-Za-z])|\s?×)?" % {"n": NUM})
REF_WORD = re.compile(
    r"(?:\b(?:table|tab|figure|fig|figs|section|sec|secs|eq|eqs|equation|appendix|app|algorithm|alg|"
    r"line|lines|theorem|lemma|definition|corollary|proposition|chapter|ch|example|claim|hypothesis|rq|"
    r"listing|footnote|page|pp|p|version|v|round|iteration|generation|epoch|step|stage|phase|seed|"
    r"layer|trial|task|block|level|item|row|column|col)\.?\s*)$", re.I)
YEAR = re.compile(r"^(19|20)\d\d$")
STOP = set("""of the and or to in on for with by at as from than that which who is are was were be been
times time points point percent percentage pp more fewer less higher lower out per vs versus each all
these those this it its their our we a an not only same other first last next previous also about
approximately roughly nearly over under up down into across between after before during while
hour hours day days week weeks month months year years minute minutes second seconds""".split())
FILLER = {"different", "distinct", "independent", "separate", "additional", "unique", "new"}

# Entity dictionary: (key, regex on the ~4 words AFTER the number, regex on the ~6 words BEFORE it).
ENTITIES = [
    ("gpu_hours", r"^(?:gpu|[ahv]100|h200|tpu)s?[\s-]?(?:hours?|hrs?|h)\b",
     r"(?:gpu|[ahv]100|tpu)[\s-]?hours?\s*(?:total|in total|of|=|:|was|were|is|are|≈|~)?\s*$"),
    ("n_gpus", r"^(?:x\s*|×\s*)?(?:nvidia\s+)?(?:[ahv]100s?|h200s?|gpus?|tpus?)\b(?![\s-]?(?:hours?|hrs?|h)\b)",
     r"(?:number of gpus|gpus)\s*(?:=|:)\s*$"),
    ("duration", r"^(?:hours?|hrs?|days?|weeks?|months?)\b", None),
    ("iterations", r"^(?:[a-z-]+\s+)?(?:iterations|rounds|generations)\b",
     r"(?:iterations|rounds|generations)\s*(?:of|=|:|is|was|to|set to)?\s*$"),
    ("candidates_evaluated", r"^(?:[a-z-]+\s+)?(?:candidates|architectures|programs|designs)\b",
     r"(?:candidates|architectures)\s*(?:evaluated|generated|sampled)?\s*(?:=|:)\s*$"),
    ("elites", r"^(?:elites?|elite\s+\w+|parents|survivors)\b",
     r"(?:\bk|top-k|elites?(?: per round)?)\s*(?:=|:)\s*$"),
    ("islands", r"^(?:islands?|populations|sub-?populations|demes)\b", r"(?:islands|populations)\s*(?:=|:)\s*$"),
    ("seeds", r"^(?:random\s+|independent\s+|different\s+)?seeds\b|^independent\s+runs\b",
     r"(?:seeds|number of runs)\s*(?:=|:)\s*$"),
    ("epochs", r"^(?:training\s+)?epochs\b", r"epochs\s*(?:=|:|of|to)?\s*$"),
    ("batch_size", None, r"batch[\s-]?sizes?\s*(?:of|=|:|is|was|to|set to)?\s*$"),
    ("hidden_dim", r"^-?dim(?:ensional)?\b|^hidden\s+(?:units|dimensions?)\b",
     r"(?:hidden|embedding|model|latent)\s*(?:size|dim(?:ension)?s?)\s*(?:of|=|:|is|to)?\s*$|d_?model\s*=\s*$"),
    ("params", r"^-?(?:parameters?|params)\b", r"(?:parameters|params)\s*(?:=|:|of)?\s*$"),
    ("dataset_size_n", None, r"(?:^|\s)n\s*=\s*$"),
    ("learning_rate", None, r"(?:learning rate|\blr|η)\s*(?:of|=|:|is|was|to|set to)?\s*$"),
]
ENTITIES = [(k, re.compile(a) if a else None, re.compile(b) if b else None) for k, a, b in ENTITIES]
ACTIVITY = re.compile(r"\b(search|training|train|fine-?tun\w*|evaluation|evolution|optimi[sz]ation|"
                      r"experiments?|run|runs|annotation|collection)\b", re.I)
PCT_VALID = re.compile(r"\b(valid|validity|passed|pass rate|filtered|compil\w*|executable|feasible|"
                       r"success rate|accepted)\b", re.I)
DAYS = {"hour": 1 / 24, "hr": 1 / 24, "day": 1, "week": 7, "month": 30}
COMPOSITION = re.compile(r"\b(split|breakdown|composition|composed|consist\w*|compris\w*|distribut\w*|"
                         r"proportion|share|fraction|accounts? for|categor\w*|mix)\b", re.I)
DROP_HEAD = re.compile(r"^(references|bibliography|works cited|literature cited)$|"
                       r"^(?:[A-Z](?:\.\d+)*\.?\s+|\d+(?:\.\d+)*\.?\s+)?(?:(?:full|all|llm|agent|system|user|evaluation|judge|example)\s+)?"
                       r"prompts?(?:\s+(?:used\b.*|templates?|text|details|for\b.*|in\b.*))?\s*$|checklist", re.I)
DERIVED = re.compile(r"\b(avg|average|mean|total|sum|ratio|diff\w*|gain|delta)\b|Δ|\\delta", re.I)


def fnum(s: str) -> float:
    return float(s.replace(",", ""))


def decs(s: str) -> int:
    return len(s.split(".")[1]) if "." in s else 0


def half_unit(s: str) -> float:
    return 0.5 * 10 ** -decs(s)


# ============================================================================ text preparation

def _blank(m) -> str:
    return SL._nl(m.group(0))


def _clean_math(body: str) -> str:
    for a, b in ((r"\times", "×"), (r"\cdot", "×"), (r"\approx", "≈"), (r"\sim", "~"), (r"\pm", "±"),
                 (r"\%", "%"), (r"\Delta", "Δ"), (r"\{,\}", ","), ("{,}", ",")):
        body = body.replace(a, b)
    body = re.sub(r"[_^](\{[^{}]*\}|\\?[A-Za-z0-9])", " ", body)
    body = re.sub(r"\\[A-Za-z]+", " ", body)
    return body.replace("{", "").replace("}", "").replace("\n", " ")


def _tex_headings(s: str) -> List[Tuple[int, int, str]]:
    lv = {"part": 0, "chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3, "paragraph": 4}
    app = re.search(r"\\appendix\b", s)
    out = []
    for m in re.finditer(r"\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\s*(?:\[[^\]]*\])?"
                         r"\s*\{((?:[^{}]|\{[^{}]*\})*)\}", s):
        t = re.sub(r"\s+", " ", re.sub(r"\\[A-Za-z]+|[{}]", " ", m.group(2))).strip()
        if app and m.start() > app.start() and lv[m.group(1)] <= 1:
            t = "Appendix: " + t
        out.append((s.count("\n", 0, m.start()), lv[m.group(1)], t))
    a = re.search(r"\\begin\{abstract\}", s)
    if a:
        out.append((s.count("\n", 0, a.start()), 1, "Abstract"))
    return sorted(out)


def _split_cells(row: str, sep: str) -> List[str]:
    return [c.strip() for c in re.split(r"(?<!\\)" + re.escape(sep), row)]


def _tex_tables(s: str) -> List[dict]:
    tables = []
    for m in re.finditer(r"\\begin\{(tabular\*?|tabularx|longtable|tabulary)\}(.*?)\\end\{\1\}", s, re.S):
        base = s.count("\n", 0, m.start())
        body = m.group(2)
        rows, header, pos = [], None, 0
        for chunk in re.split(r"\\\\", body):
            first = pos + len(chunk) - len(chunk.lstrip())
            pos += len(chunk) + 2
            if re.match(r"\s*\\(midrule|hline)", chunk) and rows and header is None:
                header = len(rows) - 1
            line = re.sub(r"\\(toprule|midrule|bottomrule|hline)|\\cmidrule(\([^)]*\))?\{[^}]*\}", " ", chunk)
            if not rows:  # column spec {lcc} right after \begin{tabular}
                line = re.sub(r"^\s*(\{[^}]*\})+", " ", line)
            cells = [_cell_text(c) for c in _split_cells(line, "&")]
            if any(cells):
                rows.append((base + body.count("\n", 0, first), cells))
        tables.append({"rows": rows, "header": header if header is not None else 0})
    return tables


def _cell_text(c: str) -> str:
    c = re.sub(r"\$([^$]*)\$", lambda m: _clean_math(m.group(1)), c)
    c = re.sub(r"\\multi(?:column|row)\{[^}]*\}\{[^}]*\}", " ", c)
    c = c.replace(r"\%", "%").replace("--", "–")
    c = re.sub(r"\\[A-Za-z]+\*?", " ", c)
    return re.sub(r"\s+", " ", c.replace("{", "").replace("}", "")).strip()


def prepare(doc) -> Tuple[List[str], List[Tuple[int, int, str]], List[dict], set]:
    """Return (cleaned prose lines aligned with doc.raw_lines, headings, tables, dropped line idx)."""
    n = len(doc.raw_lines)
    tables, dropped = [], set()
    if doc.kind == "tex":
        s = "\n".join(SL._strip_comment(l) for l in doc.raw_lines)
        bd, ed = re.search(r"\\begin\s*\{document\}", s), re.search(r"\\end\s*\{document\}", s)
        if bd:
            s = re.sub(r"[^\n]", " ", s[:bd.end()]) + s[bd.end():]
        if ed:
            s = s[:ed.start()] + re.sub(r"[^\n]", " ", s[ed.start():])
        s = re.sub(r"\\begin\{(filecontents|thebibliography|verbatim|lstlisting|minted|comment|tikzpicture|"
                   r"equation|align|gather|multline|eqnarray|displaymath|algorithmic|algorithm)\*?\}.*?"
                   r"\\end\{\1\*?\}", _blank, s, flags=re.S)
        heads = _tex_headings(s)
        tables = _tex_tables(s)
        s = re.sub(r"\\begin\{(tabular\*?|tabularx|longtable|tabulary)\}.*?\\end\{\1\}", _blank, s, flags=re.S)
        s = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", _blank, s, flags=re.S)
        s = re.sub(r"(?<!\\)~", " ", s)
        s = re.sub(r"(?<!\\)\$((?:[^$\\]|\\.)+?)(?<!\\)\$|\\\((.*?)\\\)",
                   lambda m: _clean_math(m.group(1) or m.group(2) or "") + "\n" * m.group(0).count("\n"), s,
                   flags=re.S)
        s = re.sub(r"\\(cite\w*|ref|eqref|autoref|[cC]ref|pageref|label|url|includegraphics|bibliography\w*|"
                   r"vspace|hspace|input|include|href|footnotemark)\*?(\[[^\]]*\])*\{[^}]*\}", " ", s)
        s = re.sub(r"\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\s*(\[[^\]]*\])?\s*"
                   r"\{((?:[^{}]|\{[^{}]*\})*)\}", _blank, s)
        s = s.replace("---", "—").replace("--", "–").replace(r"\textasciitilde", "~").replace(r"\texttimes", "×")
        s = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?", " ", s)
        s = re.sub(r"\\([%&_#$])", r"\1", s)
        s = re.sub(r"\\[,;!: ]", " ", s)
        s = re.sub(r"\\[A-Za-z@]+\*?(\[[^\]\n]*\])?", " ", s)
        lines = s.replace("{", "").replace("}", "").split("\n")
    else:
        heads = list(doc.headings)
        dropped |= {i for i, _ in getattr(doc, "ref_lines", [])}
        lines, in_code, tab = [], False, None
        for i, line in enumerate(doc.raw_lines):
            if doc.kind == "md" and re.match(r"^\s*(```|~~~)", line):
                in_code = not in_code
                line = ""
            if in_code or any(h[0] == i for h in heads):
                line = ""
            if doc.kind == "md" and re.match(r"^\s*\|.*\|\s*$", line):
                raw_cells = [c.strip() for c in line.strip().strip("|").split("|")]
                cells = [_cell_text(c) for c in raw_cells]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in raw_cells if c):
                    tab["header"] = len(tab["rows"]) - 1 if tab else 0
                else:
                    if tab is None:
                        tab = {"rows": [], "header": 0}
                        tables.append(tab)
                    tab["rows"].append((i, cells))
                lines.append("")
                continue
            tab = None
            line = re.sub(r"!\[[^\]]*\]\([^)]*\)|<!--.*?-->", " ", line)
            line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)
            line = re.sub(r"\$([^$]+)\$", lambda m: _clean_math(m.group(1)), line)
            lines.append(line.replace("`", ""))
    lines = [re.sub(r"\[\d+(?:\s*[,–-]\s*\d+)*\]", " ", l) for l in lines]  # numeric citations
    lines += [""] * (n - len(lines))
    for k, (hi, lvl, title) in enumerate(heads):
        if DROP_HEAD.search(re.sub(r"^Appendix:\s*", "", title).strip()):
            end = next((h[0] for h in heads[k + 1:] if h[1] <= lvl), n)
            dropped |= set(range(hi, end))
    return lines, heads, tables, dropped


# ============================================================================ step 1+2: extraction

def _section(heads, i: int) -> str:
    name = "Front matter"
    for hi, lvl, t in heads:
        if hi > i:
            break
        if lvl <= 2:
            name = t
    return name


def _words(t: str) -> List[str]:
    return [w for w in re.split(r"\s+", t) if w and w not in ("|",)]


def assign_entity(value: float, raw: str, kind: str, before: str, after: str, window: str
                  ) -> Optional[Tuple[str, float, str]]:
    b, a = before.lower(), after.lower()
    if kind == "pct":
        return ("pct_valid", value, "") if PCT_VALID.search(window) else None
    for key, arx, brx in ENTITIES:
        m = arx.search(a) if arx else None
        if m or (brx and brx.search(b)):
            if key == "duration":
                act = sorted((w.lower() for w in ACTIVITY.findall(window)),
                             key=lambda w: w.startswith(("run", "experiment")))  # prefer specific activities
                if not act:
                    return None
                unit = re.match(r"(hour|hr|day|week|month)", a).group(1)
                note = "" if unit == "day" else "normalized %s→days" % unit
                act0 = re.sub(r"^train$", "training", act[0])
                return "duration:" + re.sub(r"s$", "", act0), value * DAYS[unit], note
            return key, value, ""
    return None


def generic_entity(after: str) -> Optional[str]:
    ws = [w.lower().strip(".,;:()\"'") for w in _words(after)[:2]]
    if ws and ws[0] in FILLER and len(ws) > 1:
        ws = ws[1:]
    if not ws or not re.fullmatch(r"[a-z][a-z-]{2,}", ws[0]) or ws[0] in STOP or ws[0].endswith(("ed", "ing", "ly")):
        return None
    w = ws[0]
    return "noun:" + (w[:-1] if w.endswith("s") and not w.endswith("ss") and len(w) > 3 else w)


def _sentences(text: str) -> List[Tuple[int, int]]:
    spans, st = [], 0
    for m in re.finditer(r"(?<=[.!?])\s+(?=[A-Z(\[])", text):
        spans.append((st, m.start()))
        st = m.end()
    spans.append((st, len(text)))
    return spans


def _occ(raw, value, kind, unit_raw, loc, section, ctx, table=False):
    return {"raw": raw, "value": value, "kind": kind, "half_unit": unit_raw, "loc": loc, "section": section,
            "context": ctx, "entity": None, "note": "", "table": table}


def extract(doc, lines, heads, tables, dropped) -> Tuple[List[dict], List[Tuple[str, str, str, int]]]:
    """Return (occurrences, sentences) where sentences are (text, loc, section, para_line)."""
    occs, sents, block = [], [], []
    paras = []
    for i, l in enumerate(lines + [""]):
        if i in dropped or not l.strip():
            if block:
                paras.append(SL.Para(block, _section(heads, block[0][0])))
            block = []
        else:
            block.append((i, l))
    for p in paras:
        text = p.text
        for s0, s1 in _sentences(text):
            sent = text[s0:s1]
            loc = doc.loc(p.line_at(s0))
            sents.append((sent, loc, p.section))
            start = len(occs)
            for m in TOKEN_RX.finditer(sent):
                st = m.start()
                pre = sent[max(0, st - 2):st]
                if pre[-1:] and (pre[-1].isalnum() or pre[-1] in "_./" or (pre[-1] == "-" and pre[:1].isalnum())):
                    continue
                if re.match(r"[A-Za-z]", sent[m.end():m.end() + 1]):
                    continue
                before_txt, after_txt = sent[:st], sent[m.end():]
                bw, aw = _words(before_txt), _words(after_txt)
                ctx = " ".join(bw[-8:] + ["«" + m.group(0).strip() + "»"] + aw[:8])
                where = doc.loc(p.line_at(s0 + st))
                if m.group("sum") or m.group("prod"):
                    parts = [fnum(x) for x in re.findall(NUM, m.group(0))]
                    kind = "sum" if m.group("sum") else "product"
                    o = _occ(m.group(0).strip(), tuple(parts), kind, 0, where, p.section, ctx)
                    g = generic_entity(after_txt) if kind == "sum" else None
                    if g:
                        o["entity"] = "composition:" + g[5:]
                    occs.append(o)
                    continue
                raw, suf = m.group("num"), (m.group("suf") or "").strip()
                if REF_WORD.search(before_txt) or (re.search(r"\(\s*$", before_txt) and after_txt.startswith(")")):
                    continue
                if m.group("num2"):
                    o = _occ(m.group(0).strip(), (fnum(raw), fnum(m.group("num2"))), "range", 0, where,
                             p.section, ctx)
                    occs.append(o)
                    continue
                v = fnum(raw)
                kind = "pct" if suf == "%" else ("multiplier" if suf == "×" else "num")
                v *= MULT.get(suf, 1)
                o = _occ(m.group(0).strip(), v, kind, half_unit(raw) * MULT.get(suf, 1), where, p.section, ctx)
                o["approx"] = bool(m.group("approx"))
                window = " ".join(bw[-8:] + aw[:8])
                ent = assign_entity(v, raw, kind, " ".join(bw[-6:]), " ".join(aw[:4]), window)
                if YEAR.match(raw) and not suf and not ent:
                    continue
                if ent:
                    o["entity"], o["value"], o["note"] = ent
                    if o["note"]:
                        o["half_unit"] = None  # cross-unit: compare by relative tolerance only
                elif kind == "num" and "." not in raw and not suf:
                    o["entity"] = generic_entity(after_txt)
                occs.append(o)
            occs += _derive_gpu_hours(occs[start:])
    for t in tables:
        occs += _table_occs(doc, t, heads)
    return occs, sents


def _derive_gpu_hours(sent_occs) -> List[dict]:
    """'160 GPUs for 21 hours' in one sentence implies 3,360 GPU-hours: add a derived occurrence."""
    gpus = [o for o in sent_occs if o["entity"] == "n_gpus"]
    hrs = [o for o in sent_occs if o["kind"] == "num" and o["entity"] != "gpu_hours"
           and re.search(r"»\s+(hours?|hrs?|days?)\b", o["context"])]
    if len(gpus) != 1 or len(hrs) != 1:
        return []
    g, h = gpus[0], hrs[0]
    days = re.search(r"»\s+days?", h["context"])
    hours = fnum(h["raw"].lstrip("~≈ ")) * (24 if days else 1)
    d = _occ("%s GPUs × %s %s" % (g["raw"], h["raw"], "days" if days else "h"), g["value"] * hours, "derived", None, g["loc"],
             g["section"], g["context"])
    d.update(entity="gpu_hours", note="derived = n_gpus × hours")
    return [d]


def _cell_num(c: str) -> Optional[Tuple[float, str]]:
    c = re.sub(r"\s*(±|\+/-)\s*" + NUM + r".*$|\s*\([^)]*\)\s*$", "", c).strip().rstrip("%").strip()
    c = c.replace("−", "-").replace("×", "")
    m = re.fullmatch(r"([+-]?)\s*(" + NUM + r")\s*([kKMB]?)", c)
    if not m:
        return None
    return (-1 if m.group(1) == "-" else 1) * fnum(m.group(2)) * MULT.get(m.group(3), 1), m.group(2)


def _table_occs(doc, t, heads) -> List[dict]:
    out, rows = [], t["rows"]
    if not rows:
        return out
    header = rows[t["header"]][1] if t["header"] < len(rows) else rows[0][1]
    for ri, (idx, cells) in enumerate(rows):
        if ri <= t["header"]:
            continue
        label = " ".join(c for c in cells if _cell_num(c) is None)
        for j, c in enumerate(cells):
            cn = _cell_num(c)
            if cn is None:
                continue
            h = header[j] if j < len(header) else ""
            ctx = "table row '%s', column '%s': «%s»" % (label, h, c)
            o = _occ(c, cn[0], "pct" if "%" in c or "%" in h else "num", half_unit(cn[1]), doc.loc(idx),
                     _section(heads, idx), ctx, table=True)
            ent = None
            for after in (h, label):
                ent = ent or assign_entity(cn[0], cn[1], o["kind"], label + " " + h, after, label + " " + h)
            # a column header names the quantity only for a Total row or a one-row table
            if ent and not ent[0].startswith("duration") and (
                    assign_entity(cn[0], cn[1], o["kind"], label, label, label)
                    or re.search(r"\b(total|sum|overall|all)\b", label, re.I) or len(rows) - t["header"] == 2):
                o["entity"], o["value"], o["note"] = ent
            out.append(o)
    return out


# ============================================================================ step 3: same quantity

def same(a: dict, b: dict) -> bool:
    va, vb = a["value"], b["value"]
    if isinstance(va, tuple) or isinstance(vb, tuple):
        return va == vb
    if abs(va - vb) <= 0.02 * max(abs(va), abs(vb)) + 1e-12:
        return True
    ua, ub = a.get("half_unit"), b.get("half_unit")
    return ua is not None and ub is not None and abs(va - vb) <= max(ua, ub) + 1e-9


def group_entities(occs, min_values=2):
    groups: Dict[str, List[dict]] = {}
    for o in occs:
        if o["entity"]:
            groups.setdefault(o["entity"], []).append(o)
    cands, consistent = [], 0
    for ent, os_ in groups.items():
        clusters: List[List[dict]] = []
        for o in os_:
            for c in clusters:
                if same(c[0], o):
                    c.append(o)
                    break
            else:
                clusters.append([o])
        if len(clusters) >= min_values:
            cands.append({"entity": ent, "values": [_fmt(c[0]["value"]) for c in clusters],
                          "generic": ent.startswith(("noun:", "composition:")), "occurrences": os_})
        elif len(os_) >= 2:
            consistent += len(os_)
    cands.sort(key=lambda c: (c["generic"], c["entity"]))
    return groups, cands, consistent


def _fmt(v) -> str:
    if isinstance(v, tuple):
        return "(" + ", ".join(_fmt(x) for x in v) + ")"
    return ("%.4g" % v) if abs(v) < 1e5 else "{:,.0f}".format(v)


# ============================================================================ step 4: arithmetic

def arithmetic(occs, sents) -> Tuple[List[dict], int]:
    bad, ok = [], 0

    def flag(kind, sent, loc, claim, expect):
        bad.append({"check": kind, "claim": claim, "expected": expect, "loc": loc, "sentence": sent.strip()})

    for sent, loc, _sec in sents:
        for m in re.finditer(r"(%s)\s*[×x]\s*(%s)((?:\s*[×x]\s*%s)*)\s*\(?\s*=\s*(%s)([kKMB]?)" % (NUM, NUM, NUM, NUM),
                             sent):
            fs = [fnum(x) for x in re.findall(NUM, m.group(0))][:-1]
            prod, c = 1.0, fnum(m.group(4)) * MULT.get(m.group(5), 1)
            for f in fs:
                prod *= f
            if abs(prod - c) <= max(0.01 * abs(prod), half_unit(m.group(4)) * MULT.get(m.group(5), 1)):
                ok += 1
            else:
                flag("product", sent, loc, m.group(0), _fmt(prod))
        for m in re.finditer(r"(%s)(?:\s*\+\s*(%s))+\s*=\s*(%s)" % (NUM, NUM, NUM), sent):
            parts = [fnum(x) for x in re.findall(NUM, m.group(0))]
            tol = sum(half_unit(x) for x in re.findall(NUM, m.group(0)))
            if abs(sum(parts[:-1]) - parts[-1]) <= tol + 1e-9:
                ok += 1
            else:
                flag("sum", sent, loc, m.group(0), _fmt(sum(parts[:-1])))
        for m in re.finditer(r"(%s)\s*%%\s+of\s+(?:the\s+|all\s+)?(\d[\d,]*)(?![.\d])" % NUM, sent):
            x, n = fnum(m.group(1)), int(fnum(m.group(2)))
            if n <= 0:
                continue
            k = round(x * n / 100)
            if any(abs(100 * kk / n - x) <= half_unit(m.group(1)) + 1e-9 for kk in (k - 1, k, k + 1)):
                ok += 1
            else:
                flag("percent_of_n (GRIM; overlaps lint R17)", sent, loc, m.group(0),
                     "%.2f items, not an integer" % (x * n / 100))
        if COMPOSITION.search(sent):
            for m in re.finditer(r"%s\s*%%(?:\s*(?:/|,|;|,?\s*and)\s*%s\s*%%){2,}" % (NUM, NUM), sent):
                ps = re.findall(NUM, m.group(0))
                tot, tol = sum(fnum(p) for p in ps), sum(half_unit(p) for p in ps) + 0.5
                if abs(tot - 100) <= tol:
                    ok += 1
                else:
                    flag("percent_parts_sum", sent, loc, m.group(0), "parts sum to %s, not 100" % _fmt(tot))
        pairs = [(m.group(1), m.group(2), m.end(), "→") for m in
                 re.finditer(r"from\s+(%s)\s*%%?\s+to\s+(%s)" % (NUM, NUM), sent)]
        vs = list(re.finditer(r"(%s)\s*%%?\s*(?:vs\.?|versus)\s*(%s)" % (NUM, NUM), sent))
        if len(vs) == 1:
            pairs.append((vs[0].group(1), vs[0].group(2), vs[0].end(), "vs"))
        if len(pairs) != 1:
            continue
        a_s, b_s, end, arrow = pairs[0]
        a, b = fnum(a_s), fnum(b_s)
        rest = sent[end:]
        prec = max(10 ** -decs(a_s), 10 ** -decs(b_s))
        for dm in re.finditer(r"\(\s*[+−-]\s*(%s)\s*(?:points|pp|%%)?\s*\)|(%s)\s*(?:percentage\s+|absolute\s+)?"
                              r"(?:points|pp)\b" % (NUM, NUM), rest):
            d_s = dm.group(1) or dm.group(2)
            d, tol = fnum(d_s), half_unit(d_s) + prec + 1e-9
            if abs(d - abs(b - a)) <= tol or (max(a, b) <= 1 and abs(d - 100 * abs(b - a)) <= tol * 100):
                ok += 1
            else:
                flag("difference", sent, loc, "%s %s %s, stated %s" % (a_s, arrow, b_s, dm.group(0).strip()),
                     _fmt(abs(b - a)))
        for rm in re.finditer(r"(%s)\s*%%\s*(?:relative\s+)?(?:improvement|gain|increase|reduction|decrease|boost|"
                              r"drop|better|higher|lower)|(?:improvement|gain|increase|reduction|decrease) of\s+"
                              r"(%s)\s*%%" % (NUM, NUM), rest):
            x_s = rm.group(1) or rm.group(2)
            x = fnum(x_s)
            opts = [abs(b - a) / abs(a) * 100 if a else None, abs(b - a)]
            if re.search(r"\berror", sent, re.I) and a < 100:
                opts.append(abs(b - a) / (100 - a) * 100)
            if any(c is not None and abs(x - c) <= half_unit(x_s) + 0.02 * c + 0.05 for c in opts):
                ok += 1
            else:
                flag("relative_change", sent, loc, "%s %s %s, stated %s" % (a_s, arrow, b_s, rm.group(0).strip()),
                     "%.1f%% relative (%.3g absolute)" % (opts[0] or 0, opts[1]))
        for xm in re.finditer(r"(%s)\s*(?:×|x\b|-fold|\s+times\b)" % NUM, rest):
            r = max(a, b) / min(a, b) if min(a, b) > 0 else None
            x_s = xm.group(1)
            if r is None:
                continue
            if abs(fnum(x_s) - r) <= half_unit(x_s) + 0.03 * r:
                ok += 1
            else:
                flag("ratio", sent, loc, "%s vs %s, stated %s" % (a_s, b_s, xm.group(0).strip()), "%.2f×" % r)
    return bad, ok


# ============================================================================ step 5: tables

def tables_check(doc, tables) -> Tuple[List[dict], int]:
    bad, ok = [], 0
    for t in tables:
        rows, hi = t["rows"], t["header"]
        if len(rows) <= hi + 1:
            continue
        header = rows[hi][1]
        dcols = {j for j, h in enumerate(header) if DERIVED.search(h)}
        block: List[List] = []
        for idx, cells in rows[hi + 1:]:
            nums = [_cell_num(c) for c in cells]
            label = cells[0].lower() if cells else ""
            if re.fullmatch(r"(total|sum|avg\.?|average|mean)", label) and len(block) >= 2:
                for j in range(1, len(cells)):
                    col = [r[j] if j < len(r) else None for r in block]
                    if nums[j] is None or any(c is None for c in col):
                        continue
                    vals = [c[0] for c in col]
                    want = sum(vals) if label in ("total", "sum") else sum(vals) / len(vals)
                    tol = half_unit(nums[j][1]) + len(vals) * max(half_unit(c[1]) for c in col) + 1e-9
                    if abs(want - nums[j][0]) <= tol:
                        ok += 1
                    else:
                        bad.append({"loc": doc.loc(idx), "row": " | ".join(cells),
                                    "column": header[j] if j < len(header) else "?", "stated": nums[j][1],
                                    "recomputed": _fmt(want), "rule": "%s of column" % label})
                block = []
                continue
            block.append(nums)
            if len(cells) != len(header):
                continue
            for j in dcols:
                if nums[j] is None:
                    continue
                ins = [nums[k] for k in range(j) if k not in dcols and nums[k] is not None]
                h = header[j].lower()
                tol_in = max((half_unit(c[1]) for c in ins), default=0)
                stated, tol = nums[j][0], half_unit(nums[j][1]) + 1e-9
                if re.search(r"avg|average|mean", h) and len(ins) >= 2:
                    wants = [sum(c[0] for c in ins) / len(ins)]
                    tol += tol_in
                elif re.search(r"total|sum", h) and len(ins) >= 2:
                    wants = [sum(c[0] for c in ins)]
                    tol += len(ins) * tol_in
                elif re.search(r"ratio", h) and len(ins) == 2 and ins[0][0] and ins[1][0]:
                    wants = [ins[1][0] / ins[0][0], ins[0][0] / ins[1][0]]
                    tol += 0.02 * stated
                elif len(ins) == 2:  # Δ / diff / gain
                    d = ins[1][0] - ins[0][0]
                    wants = [d, -d] + ([d / ins[0][0] * 100] if ins[0][0] else [])
                    tol += 2 * tol_in
                else:
                    continue
                if any(abs(stated - w) <= tol for w in wants):
                    ok += 1
                else:
                    bad.append({"loc": doc.loc(idx), "row": " | ".join(cells), "column": header[j],
                                "stated": nums[j][1], "recomputed": _fmt(wants[0]),
                                "rule": "%s of the %d cells to its left" % (header[j], len(ins))})
    return bad, ok


# ============================================================================ driver + report

def analyze(path: str, min_values: int = 2) -> dict:
    doc = SL.load(path)
    lines, heads, tables, dropped = prepare(doc)
    occs, sents = extract(doc, lines, heads, tables, dropped)
    groups, cands, consistent = group_entities(occs, min_values)
    arith, arith_ok = arithmetic(occs, sents)
    tbad, tok = tables_check(doc, tables)
    return {"path": path, "numbers": occs, "candidates": cands, "arithmetic": arith, "tables": tbad,
            "summary": {"numbers_extracted": len(occs), "entities": len(groups),
                        "entities_repeated": sum(1 for g in groups.values() if len(g) >= 2),
                        "candidates": len(cands), "arithmetic_mismatches": len(arith),
                        "table_mismatches": len(tbad), "tables_parsed": len(tables),
                        "consistent_repeated_numbers": consistent, "arithmetic_checks_ok": arith_ok,
                        "table_checks_ok": tok, "checked_consistent": consistent + arith_ok + tok}}


def to_markdown(r: dict) -> str:
    s = r["summary"]
    out = ["# Number ledger: %s" % r["path"], "", HEADER, "", "## Same quantity, different values", ""]
    if not r["candidates"]:
        out.append("None found.")
    for c in r["candidates"]:
        tag = " (generic, low confidence)" if c["generic"] else ""
        out.append("### `%s`%s: %s" % (c["entity"], tag, " vs ".join(c["values"])))
        for o in c["occurrences"]:
            note = " [%s]" % o["note"] if o["note"] else ""
            out.append("- %s (%s): %s%s" % (o["loc"], o["section"], o["context"], note))
        out.append("")
    out += ["", "## Arithmetic mismatches", ""]
    out += ["- %s [%s]: `%s`, recomputed %s. Sentence: \"%s\"" % (a["loc"], a["check"], a["claim"], a["expected"],
                                                                  a["sentence"][:220]) for a in r["arithmetic"]] \
        or ["None found."]
    out += ["", "## Table recomputation", ""]
    out += ["- %s: column '%s' states %s, recomputed %s (%s). Row: %s" % (t["loc"], t["column"], t["stated"],
                                                                          t["recomputed"], t["rule"], t["row"])
            for t in r["tables"]] or ["None found (%d tables parsed)." % s["tables_parsed"]]
    out += ["", "## Summary", "",
            "- Numbers extracted: %d" % s["numbers_extracted"],
            "- Entities: %d (%d stated more than once)" % (s["entities"], s["entities_repeated"]),
            "- Candidates (same quantity, different values): %d" % s["candidates"],
            "- Arithmetic mismatches: %d; table mismatches: %d" % (s["arithmetic_mismatches"], s["table_mismatches"]),
            "- Numbers checked consistent: %d (%d repeated numbers agree, %d arithmetic checks pass, "
            "%d table cells recompute)" % (s["checked_consistent"], s["consistent_repeated_numbers"],
                                           s["arithmetic_checks_ok"], s["table_checks_ok"]), ""]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    ap.add_argument("-o", "--output", help="write the report to this file")
    ap.add_argument("--min-values", type=int, default=2, help="distinct values needed to flag an entity")
    a = ap.parse_args(argv)
    if not os.path.exists(a.path):
        ap.error("no such file or directory: %s" % a.path)
    r = analyze(a.path, a.min_values)
    text = json.dumps(r, indent=1, ensure_ascii=False) if a.json else to_markdown(r)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
