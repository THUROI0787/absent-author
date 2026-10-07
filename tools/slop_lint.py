#!/usr/bin/env python3
"""slop_lint.py -- deterministic surface-trace screen for "sloppy AI" ML papers.

Maps every check to an evidence ID in the evidence catalog (EVIDENCE.md at the project root;
references/evidence-catalog.md inside a skill) (L = language, S = structure,
R = research, P = process/artifact). Python 3.9+, standard library only.

    python slop_lint.py PATH [PATH ...] [--format md|json] [--source] [--max-examples N]

PATH may be a .tex / .md / .txt file or a directory (a directory is ONE document:
its .tex files are read -- the file with \\begin{document} is used as the root and
\\input/\\include are inlined; otherwise all .tex are concatenated -- and its .bib
files feed the citation checks).

READ THIS BEFORE USING THE OUTPUT
  * Every hit is a CANDIDATE for a human to read in context, never a verdict.
  * L-layer hits can at most support "the writing was not polished by a person".
    They never imply that the research is slop (evidence catalog, iron rule 1).
  * Absence of hits means nothing: 2026 pipelines scrub these surface traces.
  * Bands ("typical / elevated / high") compare one paper with a small corpus of
    pre-ChatGPT arXiv papers; with n=59, "p99" is essentially the corpus maximum.
  * Non-native writers and heavily copy-edited papers trip L-layer checks too.

License: MIT. Pattern ideas were informed by several MIT-licensed
anti-slop projects (Anti-Autoresearch, avoid-ai-writing, humanizer, de-slop,
slop-forensics); no code was copied.
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

VERSION = "0.3.0"

# ---------------------------------------------------------------------------
# Calibration (written by tools/calibration/run_calibration.py --write-tool).
# Values are per-1k-prose-word densities unless "metric" says otherwise.
# BEGIN CALIBRATION
# Calibrated 2026-10-05 by tools/calibration/run_calibration.py on 59 human arXiv papers
# (v1 e-prints 2018-2022) and 20 AI-heavy papers. Bands: typical <= human p90 < elevated
# <= human p99 < high (L15 uses the low tail: p10 / p01). With n~50, p99 ~ corpus max.
CALIBRATION_META = {
 "date": "2026-10-05",
 "l_cluster": {
  "checks": [
   "L03",
   "L04",
   "L05",
   "L08",
   "L10",
   "L15"
  ],
  "auc": 0.9444915254237288,
  "human_share_ge": {
   "1": 0.5084745762711864,
   "2": 0.1694915254237288,
   "3": 0.01694915254237288,
   "4": 0.0,
   "5": 0.0,
   "6": 0.0
  },
  "ai_share_ge": {
   "1": 0.95,
   "2": 0.9,
   "3": 0.9,
   "4": 0.8,
   "5": 0.5,
   "6": 0.2
  },
  "ai_flags": {
   "sakana_v1/adaptive_dual_scale_denoising": 5,
   "sakana_v1/data_augmentation_grokking": 6,
   "sakana_v1/dual_expert_denoiser": 6,
   "sakana_v1/gan_diffusion": 5,
   "sakana_v1/grid_based_noise_adaptation": 5,
   "sakana_v1/layerwise_lr_grokking": 6,
   "sakana_v1/mdl_grokking_correlation": 4,
   "sakana_v1/multi_style_adapter": 6,
   "sakana_v1/rl_lr_adaptation": 5,
   "sakana_v1/weight_initialization_grokking": 5,
   "sakana_v2/compositional-regularization": 4,
   "sakana_v2/label-noise": 4,
   "sakana_v2/pest-detection": 5,
   "arXiv:2503.10619": 4,
   "arXiv:2503.10617": 4,
   "arXiv:2510.21341": 3,
   "arXiv:2510.16194": 3,
   "arXiv:2509.04504": 4,
   "arXiv:2609.34292": 0,
   "ARIS/UAV-CC": 1
  }
 },
 "n_human": 59,
 "n_ai": 20,
 "n_ai_tex": 16,
 "human_corpus": "arXiv v1 e-prints 2018-2022, cs.LG/cs.CL/cs.CV/stat.ML (see calibration/human_corpus.json)",
 "ai_corpus": "AI Scientist v1/v2, Zochi, Agents4Science, autonomous-agent and ARIS papers (see calibration/ai_set_provenance.json)",
 "weak_checks": [
  "L02",
  "L14",
  "L16",
  "S02",
  "S04",
  "S06",
  "S13",
  "R01",
  "R05",
  "P02-todo",
  "P03",
  "P06",
  "P07"
 ],
 "rare_checks": [
  "S01",
  "S03",
  "S05",
  "R16",
  "P01",
  "P02-meta"
 ],
 "specific_checks": [
  "L06",
  "P05"
 ],
 "min_prose_words": 1500
}
CALIBRATION = {
 "L01": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.9776,
  "p95": 1.8362,
  "p99": 2.9336,
  "auc": 0.6674,
  "ai_median": 0.379,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L02": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.2466,
  "p95": 0.3308,
  "p99": 0.5728,
  "auc": 0.4754,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L03": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.604,
  "p90": 1.7776,
  "p95": 2.4215,
  "p99": 5.9211,
  "auc": 0.9267,
  "ai_median": 5.953,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L04": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.5256,
  "p95": 0.8508,
  "p99": 0.9785,
  "auc": 0.8068,
  "ai_median": 0.617,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L05": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.3922,
  "p95": 0.434,
  "p99": 0.6882,
  "auc": 0.8686,
  "ai_median": 0.877,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L06": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.092,
  "auc": 0.6432,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L07": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.2094,
  "p95": 0.2472,
  "p99": 0.4297,
  "auc": 0.725,
  "ai_median": 0.1405,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L08": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.202,
  "p95": 0.3872,
  "p99": 0.8089,
  "auc": 0.9614,
  "ai_median": 1.175,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L10": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.649,
  "p90": 2.8384,
  "p95": 4.2611,
  "p99": 8.4813,
  "auc": 0.9068,
  "ai_median": 4.8865,
  "direction": "high",
  "n_human": 59,
  "metric": "list_items_per_1k"
 },
 "L14": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.1123,
  "p99": 1.5501,
  "auc": 0.6161,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "L15": {
  "p01": 0.354,
  "p10": 0.4194,
  "p50": 0.5056,
  "p90": 0.6181,
  "p95": 0.641,
  "p99": 0.6911,
  "auc": 0.7701,
  "ai_median": 0.3755,
  "direction": "low",
  "n_human": 59,
  "metric": "sentence_len_cv"
 },
 "L16": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.2406,
  "p95": 0.6592,
  "p99": 1.168,
  "auc": 0.5127,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "S01": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.1971,
  "p99": 0.485,
  "auc": 0.4805,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "S02": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.153,
  "p99": 0.1951,
  "auc": 0.5695,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "S03": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.0,
  "auc": 0.525,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "S04": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.1988,
  "p95": 0.2233,
  "p99": 0.2553,
  "auc": 0.4237,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "S05": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.0,
  "auc": 0.5,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "S06": {
  "p01": 0.0,
  "p10": 0.1966,
  "p50": 0.646,
  "p90": 1.762,
  "p95": 1.9199,
  "p99": 2.6498,
  "auc": 0.3996,
  "ai_median": 0.403,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "S13": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.2487,
  "p99": 0.6498,
  "auc": 0.5411,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "R01": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0241,
  "p99": 0.5743,
  "auc": 0.5737,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "R05": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.0638,
  "auc": 0.5424,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "R16": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.0,
  "auc": 0.5,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "P01": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.0,
  "auc": 0.525,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "P02-meta": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.0,
  "auc": 0.525,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "P02-todo": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.1558,
  "p95": 0.4358,
  "p99": 0.5628,
  "auc": 0.6492,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "P03": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.1752,
  "p95": 0.3996,
  "p99": 4.3123,
  "auc": 0.5894,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 52,
  "metric": "per_1k"
 },
 "P05": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.0,
  "p99": 0.0,
  "auc": 0.75,
  "ai_median": 0.143,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 },
 "P06": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0345,
  "p90": 0.1434,
  "p95": 0.1805,
  "p99": 0.2879,
  "auc": 0.3427,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "comment_para_ratio"
 },
 "P07": {
  "p01": 0.0,
  "p10": 0.0,
  "p50": 0.0,
  "p90": 0.0,
  "p95": 0.2453,
  "p99": 3.004,
  "auc": 0.5331,
  "ai_median": 0.0,
  "direction": "high",
  "n_human": 59,
  "metric": "per_1k"
 }
}
# END CALIBRATION
# ---------------------------------------------------------------------------

# Checks whose signal did not separate the corpora (AUC close to 0.5) or that
# are dominated by legitimate human use. They are still reported, but marked weak.
WEAK_CHECKS = set(CALIBRATION_META.get("weak_checks", []))
RARE_CHECKS = set(CALIBRATION_META.get("rare_checks", []))
SPECIFIC_CHECKS = set(CALIBRATION_META.get("specific_checks", []))


def calib_status(cid: str) -> str:
    """How well the check separated human vs AI-heavy papers in calibration."""
    if cid in RARE_CHECKS:
        return "rare (not measurable on corpus)"
    if cid in SPECIFIC_CHECKS:
        return "specific, low recall"
    if cid in WEAK_CHECKS:
        return "weak (did not separate)"
    c = CALIBRATION.get(cid)
    if not c or c.get("auc") is None:
        return "uncalibrated"
    return "strong" if c["auc"] >= 0.8 else "moderate"

LAYER_NAMES = {
    "L": "L - language layer (writing polish only; never evidence of research slop)",
    "S": "S - structure / argument layer",
    "R": "R - research / experiment layer (surface candidates only)",
    "P": "P - process / artifact layer",
}

# ============================================================================
# Document loading
# ============================================================================


class Para:
    """A prose paragraph: text plus a char-offset -> source-line map."""

    __slots__ = ("text", "starts", "lines", "section", "kind")

    def __init__(self, pieces: List[Tuple[int, str]], section: str, kind: str = "body"):
        # pieces: list of (combined_line_index, prose text of that line)
        self.starts: List[int] = []
        self.lines: List[int] = []
        buf = []
        pos = 0
        for li, t in pieces:
            self.starts.append(pos)
            self.lines.append(li)
            buf.append(t)
            pos += len(t) + 1
        self.text = " ".join(buf)
        self.section = section
        self.kind = kind

    def line_at(self, offset: int) -> int:
        i = bisect.bisect_right(self.starts, offset) - 1
        return self.lines[max(i, 0)]


class Doc:
    def __init__(self, path: str):
        self.path = path
        self.kind = "txt"  # tex | md | txt
        self.raw_lines: List[str] = []  # combined source lines
        self.linemap: List[Tuple[str, int]] = []  # combined idx -> (file, line no)
        self.bib_texts: List[Tuple[str, str]] = []
        self.files: List[str] = []
        self.paras: List[Para] = []
        self.headings: List[Tuple[int, int, str]] = []  # (combined line idx, level, title)
        self.comments: List[Tuple[int, str, bool]] = []  # (line idx, text, full_line)
        self.title = ""
        self.counts: Dict[str, int] = {}
        self.body_range = (0, 0)
        self.bbl_keys: set = set()
        self.bbl_texts: List[Tuple[str, str]] = []  # (file, text) of .bbl files (scanned for residue)
        self.ref_lines: List[Tuple[int, str]] = []  # txt input: lines of the references section
        self.tree: List[str] = []  # relative paths of every file/dir under a directory input (P13)
        self.texttt_tokens: set = set()  # identifiers set in \texttt / inline code (excluded from P07)

    @property
    def raw(self) -> str:
        return "\n".join(self.raw_lines)

    def loc(self, idx: int) -> str:
        if 0 <= idx < len(self.linemap):
            f, ln = self.linemap[idx]
            base = os.path.relpath(f, self.path) if os.path.isdir(self.path) else os.path.basename(f)
            return f"{base}:{ln}"
        return "?"


def _read(path: str) -> str:
    with open(path, "rb") as fh:
        data = fh.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", "replace")


_INPUT_RX = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")


def _strip_comment(line: str) -> str:
    m = re.search(r"(?<!\\)%", line)
    return line[: m.start()] if m else line


def _resolve_input(name: str, base_dir: str, all_tex: List[str]) -> Optional[str]:
    name = os.path.normpath(name.strip().strip('"'))
    cands = [name, name + ".tex"]
    for c in cands:
        p = os.path.normpath(os.path.join(base_dir, c))
        if os.path.isfile(p):
            return p
    # fall back: match by flattened path or by basename (handles flattened archives)
    flat = name.replace("/", "__")
    want = {os.path.basename(c) for c in cands} | {flat, flat + ".tex"}
    hits = [t for t in all_tex if os.path.basename(t) in want]
    return hits[0] if len(hits) == 1 else (hits[0] if hits else None)


def _inline_tex(path: str, all_tex: List[str], depth: int, seen: set,
                out_lines: List[str], out_map: List[Tuple[str, int]]):
    seen.add(os.path.abspath(path))
    base = os.path.dirname(path)
    for ln, line in enumerate(_read(path).split("\n"), 1):
        code = _strip_comment(line)
        m = _INPUT_RX.search(code)
        if m and depth < 10:
            target = _resolve_input(m.group(1), base, all_tex)
            if target and os.path.abspath(target) not in seen:
                before, after = line[: m.start()], line[m.end():]
                if before.strip():
                    out_lines.append(before)
                    out_map.append((path, ln))
                _inline_tex(target, all_tex, depth + 1, seen, out_lines, out_map)
                if after.strip():
                    out_lines.append(after)
                    out_map.append((path, ln))
                continue
        out_lines.append(line)
        out_map.append((path, ln))


def load(path: str) -> Doc:
    doc = Doc(path)
    if os.path.isdir(path):
        tex, bib, other = [], [], []
        for root, dirs, files in os.walk(path):
            for dn in dirs:
                doc.tree.append(os.path.relpath(os.path.join(root, dn), path) + "/")
            for f in sorted(files):
                p = os.path.join(root, f)
                doc.tree.append(os.path.relpath(p, path))
                fl = f.lower()
                if fl.endswith(".tex"):
                    tex.append(p)
                elif fl.endswith(".bib"):
                    bib.append(p)
                elif fl.endswith(".bbl"):
                    doc.bbl_keys |= _bbl_keys(_read(p))
                    doc.bbl_texts.append((p, _read(p)))
                elif fl.endswith((".md", ".txt")):
                    other.append(p)
        tex.sort()
        if tex:
            doc.kind = "tex"
            roots = [t for t in tex if re.search(r"\\begin\s*\{document\}", _strip_all_comments(_read(t)))]
            if roots:
                # choose the root that yields the most material after inlining
                best = None
                for r in roots:
                    lines, lmap = [], []
                    _inline_tex(r, tex, 0, set(), lines, lmap)
                    if best is None or len("".join(lines)) > len("".join(best[0])):
                        best = (lines, lmap, r)
                doc.raw_lines, doc.linemap = best[0], best[1]
                used = {f for f, _ in best[1]}
                doc.files = sorted(used)
            else:
                for t in tex:
                    _inline_tex(t, [], 99, set(), doc.raw_lines, doc.linemap)
                doc.files = tex
        elif other:
            p = other[0]
            doc.kind = "md" if p.lower().endswith(".md") else "txt"
            doc.raw_lines = _read(p).split("\n")
            doc.linemap = [(p, i + 1) for i in range(len(doc.raw_lines))]
            doc.files = [p]
        doc.bib_texts = [(b, _read(b)) for b in bib]
    else:
        pl = path.lower()
        if pl.endswith(".tex"):
            doc.kind = "tex"
            d = os.path.dirname(os.path.abspath(path))
            all_tex = [os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(".tex")]
            _inline_tex(path, all_tex, 0, set(), doc.raw_lines, doc.linemap)
            doc.bib_texts = [(os.path.join(d, f), _read(os.path.join(d, f)))
                             for f in sorted(os.listdir(d)) if f.lower().endswith(".bib")]
            for f in os.listdir(d):
                if f.lower().endswith(".bbl"):
                    doc.bbl_keys |= _bbl_keys(_read(os.path.join(d, f)))
                    doc.bbl_texts.append((os.path.join(d, f), _read(os.path.join(d, f))))
        else:
            doc.kind = "md" if pl.endswith(".md") else "txt"
            doc.raw_lines = _read(path).split("\n")
            doc.linemap = [(path, i + 1) for i in range(len(doc.raw_lines))]
        doc.files = [path]
    # bib entries embedded via filecontents (AI Scientist v1 does this)
    if doc.kind == "tex":
        for m in re.finditer(r"\\begin\{filecontents\*?\}(?:\[[^\]]*\])?\{[^}]*\.bib\}(.*?)\\end\{filecontents\*?\}",
                             doc.raw, re.S):
            doc.bib_texts.append(("<filecontents>", m.group(1)))
    {"tex": _parse_tex, "md": _parse_md, "txt": _parse_txt}[doc.kind](doc)
    # acknowledgements / funding text is not part of the argument (and is full of agency acronyms)
    doc.paras = [p for p in doc.paras if not re.search(r"acknowledg|funding", p.section or "", re.I)]
    return doc


# Text the authors did not write as prose: prompt dumps printed in an appendix, venue checklist
# questions, statement templates. Counting it inflates L07/L16/P07 and similar checks (feedback 2026-10-07).
NON_AUTHOR_SECTION_RX = re.compile(
    # dump-style titles only: "Prompts", "A.3 Prompts used in ...", "System prompt", "Prompt templates";
    # a main-text section such as "Prompt Optimization" is author prose and stays in
    r"^(?:appendix\s*[:.]?\s*)?(?:[A-Z](?:\.\d+)*\.?\s+|\d+(?:\.\d+)*\.?\s+)?"
    r"(?:(?:full|all|llm|agent|system|user|evaluation|judge|example)\s+)?prompts?"
    r"(?:\s+(?:used\b.*|templates?|text|details|for\b.*|in\b.*))?\s*$|"
    r"\bchecklist\b|broader\s+impact\s+statement\s+template", re.I)
# NeurIPS-style checklist item titles; in PDF text they look like top-level numbered headings.
CHECKLIST_ITEM_RX = re.compile(
    r"^(claims|limitations|theory|experiment(al)?\b|open\s+access|code\s+of\s+ethics|broader\s+impacts?|"
    r"safeguards|licen[sc]es|new\s+assets|crowdsourcing|institutional\s+review|declaration\s+of\s+llm|llm\s+usage)",
    re.I)
_HEAD_NUM_PREFIX = re.compile(r"^\s*((?:\d+|[A-H])(?:\.\d+)*)\.?\s+[A-Z]")


def exclude_non_author_sections(doc: Doc, extra_rx: Optional[str] = None, default: bool = True) -> List[str]:
    """Drop paragraphs under headings that hold non-author text (and their sub-headings).
    Returns the excluded heading titles, reported at the top of the lint report."""
    rxs = ([NON_AUTHOR_SECTION_RX] if default else []) + ([re.compile(extra_rx, re.I)] if extra_rx else [])
    if not rxs or not doc.headings:
        return []
    heads = sorted(doc.headings)
    ranges, titles = [], []

    def prefix(li):  # "A.1" / "3.2" numbering of a plain-text heading line (txt headings are all level 1)
        m = _HEAD_NUM_PREFIX.match(doc.raw_lines[li]) if li < len(doc.raw_lines) else None
        return m.group(1) if m else None

    for k, (li, lvl, t) in enumerate(heads):
        if any(rx.search(t) for rx in rxs):
            pf, is_ck = prefix(li), bool(re.search(r"checklist", t, re.I))

            def ends_range(l2, lv2, t2):
                if lv2 > lvl:
                    return False
                p2 = prefix(l2)
                if pf and p2 and p2.startswith(pf + "."):
                    return False  # numbered child (A.2 under A) in PDF text
                # "1. Claims", "2. Limitations", ... (but not a lettered appendix such as "A Experimental details")
                return not (is_ck and CHECKLIST_ITEM_RX.match(t2) and (p2 is None or p2[0].isdigit()))
            end = next((l2 for l2, lv2, t2 in heads[k + 1:] if ends_range(l2, lv2, t2)), float("inf"))
            ranges.append((li, end))
            titles.append(t)
    if not ranges:
        return []
    def inside(li):
        return any(a <= li < b for a, b in ranges)
    kept = []
    for p in doc.paras:  # filter per source line: a paragraph can straddle a heading with no blank line
        flags = [inside(li) for li in p.lines]
        if not any(flags):
            kept.append(p)
        elif not all(flags):
            ends = p.starts[1:] + [len(p.text) + 1]
            pieces = [(li, p.text[s:e - 1]) for li, s, e, f in zip(p.lines, p.starts, ends, flags) if not f]
            kept.append(Para(pieces, p.section, p.kind))
    doc.paras = kept
    return titles


def _bbl_keys(text: str) -> set:
    keys = set(re.findall(r"\\bibitem\s*(?:\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\{([^}]+)\}", text))
    keys |= set(re.findall(r"\\entry\{([^}]+)\}", text))
    return {k.strip() for k in keys}


def _strip_all_comments(text: str) -> str:
    return "\n".join(_strip_comment(l) for l in text.split("\n"))


# ============================================================================
# LaTeX -> prose (newline-preserving masking, so offsets map back to lines)
# ============================================================================


def _nl(s: str) -> str:
    """Replacement that keeps the newline count of s (so line numbers survive)."""
    n = s.count("\n")
    return (" " + "\n" * n + " ") if n else " "


def _match_brace(s: str, i: int) -> int:
    """s[i] == '{'; return index just past the matching '}' (or len(s))."""
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return len(s)


def _skip_ws(s: str, i: int) -> int:
    while i < len(s) and s[i] in " \t":
        i += 1
    return i


def _parse_args(s: str, i: int, max_opt: int = 3, max_req: int = 3):
    """Parse [..] and {..} args starting at i. Returns (end, opts, reqs) with spans."""
    opts, reqs = [], []
    j = _skip_ws(s, i)
    while j < len(s) and len(opts) < max_opt and s[j] == "[":
        k = s.find("]", j)
        if k < 0 or "\n\n" in s[j:k]:
            break
        opts.append((j + 1, k))
        j = _skip_ws(s, k + 1)
    while j < len(s) and len(reqs) < max_req and s[j] == "{":
        k = _match_brace(s, j)
        reqs.append((j + 1, k - 1))
        j = k
        jj = _skip_ws(s, j)
        if jj < len(s) and s[jj] == "{" and len(reqs) < max_req:
            j = jj
        else:
            break
    return j, opts, reqs


MATH_ENVS = ("equation|align|alignat|gather|multline|eqnarray|displaymath|math|flalign|split|"
             "IEEEeqnarray|dmath|subequations")
DROP_ENVS = (MATH_ENVS + "|tabular|tabularx|tabulary|longtable|tabu|array|algorithm|algorithmic|algorithm2e|"
             "algorithmicx|lstlisting|verbatim|Verbatim|minted|tikzpicture|pgfpicture|filecontents|"
             "thebibliography|comment|forest|axis|lstinputlisting|code|python|ack|acks|acknowledgments|acknowledgements")
FLOAT_ENVS = "figure|table|wrapfigure|wraptable|subfigure|subtable|figwindow|sidewaystable|sidewaysfigure|floatrow"

DROP_CMDS_1 = {  # commands whose arguments are not prose
    "cite", "citep", "citet", "citealp", "citealt", "citeauthor", "citeyear", "citeyearpar", "parencite",
    "textcite", "autocite", "footcite", "nocite", "Cite", "Citep", "Citet", "citenum", "shortcite",
    "ref", "eqref", "autoref", "Autoref", "cref", "Cref", "pageref", "nameref", "vref", "Vref", "cpageref",
    "label", "url", "includegraphics", "bibliography", "bibliographystyle", "vspace", "hspace",
    "setlength", "addtolength", "setcounter", "addtocounter", "newcommand", "renewcommand",
    "providecommand", "DeclareMathOperator", "definecolor", "input", "include", "usepackage",
    "documentclass", "pagestyle", "thispagestyle", "hypersetup", "graphicspath", "addbibresource",
    "color", "fontsize", "linewidth", "resizebox", "scalebox", "raisebox", "rule", "hyperref",
    "hyperlink", "hypertarget", "tikz", "pgfplotsset", "newtheorem", "crefname", "Crefname",
    "multicolumn", "multirow", "cline", "cmidrule", "affil", "author", "address", "email", "institute",
    "icmlauthor", "icmlaffiliation", "icmlcorrespondingauthor", "icmlkeywords", "keywords",
    "begin", "end", "todo", "missingfigure", "thanks", "orcid", "date", "markboth", "fancyhead",
    "fancyfoot", "lhead", "rhead", "chead", "lfoot", "rfoot", "cfoot", "def", "let", "acks", "acknowledgments",
    "acknowledgements",
}
HEADING_CMDS = {"part": 0, "chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3,
                "paragraph": 4, "subparagraph": 5}


def _parse_tex(doc: Doc):
    src = doc.raw

    def line_of(off: int) -> int:
        # every masking step preserves newline counts, so counting in the current string is exact
        return s.count("\n", 0, off)

    # --- comments (kept separately for P06) -------------------------------
    lines = src.split("\n")
    for i, line in enumerate(lines):
        m = re.search(r"(?<!\\)%", line)
        if m:
            txt = line[m.start() + 1:]
            doc.comments.append((i, txt, not line[: m.start()].strip()))
    s = "\n".join(_strip_comment(l) for l in lines)
    s = re.sub(r"\\iffalse\b.*?\\fi\b", lambda m: _nl(m.group(0)), s, flags=re.S)

    # title (from the preamble) and the body range
    tm = re.search(r"\\(?:icml)?title\s*(?:\[[^\]]*\])?\s*\{", s)
    if tm:
        e = _match_brace(s, tm.end() - 1)
        doc.title = re.sub(r"\s+", " ", re.sub(r"\\[A-Za-z]+|[{}]", " ", s[tm.end(): e - 1])).strip()
    bd = re.search(r"\\begin\s*\{document\}", s)
    if bd:
        s = re.sub(r"[^\n]", " ", s[: bd.end()]) + s[bd.end():]
    ed = re.search(r"\\end\s*\{document\}", s)
    if ed:
        s = s[: ed.start()] + re.sub(r"[^\n]", " ", s[ed.start():])
    # paper checklists are template boilerplate, not author prose
    ck = re.search(r"\\section\*?\s*\{[^}]*Checklist[^}]*\}", s, re.I)
    if ck:
        nxt = None
        for m in re.finditer(r"\\section\*?\s*\{([^}]*)\}", s[ck.end():]):
            if "checklist" not in m.group(1).lower():
                nxt = ck.end() + m.start()
                break
        stop = nxt if nxt is not None else len(s)
        s = s[: ck.start()] + re.sub(r"[^\n]", " ", s[ck.start(): stop]) + s[stop:]

    raw_body = s  # comment-free body (used for structure counts below)
    # identifiers deliberately typeset as code are not "leaked" code identifiers (P07)
    for cm in re.finditer(r"\\(?:texttt|verb|lstinline|code|path)\s*(?:\{([^{}]*)\}|([|!+])(.*?)\2)", raw_body):
        body = (cm.group(1) if cm.group(1) is not None else cm.group(3) or "").replace("\\_", "_")
        doc.texttt_tokens.update(re.findall(r"[A-Za-z0-9_]+", body))
    doc.counts["itemize"] = len(re.findall(r"\\begin\{itemize\}", raw_body))
    doc.counts["enumerate"] = len(re.findall(r"\\begin\{enumerate\}", raw_body))
    doc.counts["item"] = len(re.findall(r"\\item\b", raw_body))
    doc.counts["paragraph_cmd"] = len(re.findall(r"\\paragraph\*?\s*\{", raw_body))
    doc.counts["todo_macro"] = len(re.findall(r"\\todo\b", raw_body))

    # --- drop non-prose environments ---------------------------------------
    s = re.sub(r"\\begin\{(%s)\*?\}.*?\\end\{\1\*?\}" % DROP_ENVS, lambda m: _nl(m.group(0)), s, flags=re.S)

    # floats: keep captions only
    def _float(m):
        body = m.group(0)
        keep = []
        for cm in re.finditer(r"\\(?:sub)?caption(?:of)?\*?\s*(?:\[[^\]]*\])?\s*\{", body):
            e = _match_brace(body, cm.end() - 1)
            keep.append(body[cm.end(): e - 1])
        cap = " ".join(keep)
        n_body = body.count("\n")
        cap_flat = cap.replace("\n", " ")
        return " " + cap_flat + " . " + "\n" * n_body + " "

    s = re.sub(r"\\begin\{(%s)\*?\}.*?\\end\{\1\*?\}" % FLOAT_ENVS, _float, s, flags=re.S)

    # --- math --------------------------------------------------------------
    s = re.sub(r"\$\$.*?\$\$", lambda m: _nl(m.group(0)), s, flags=re.S)
    s = re.sub(r"\\\[.*?\\\]", lambda m: _nl(m.group(0)), s, flags=re.S)
    # inline math becomes a visible [MATH] token so quoted snippets stay faithful (counts as one word)
    s = re.sub(r"\\\(.*?\\\)", lambda m: " \u27e6MATH\u27e7 " + "\n" * m.group(0).count("\n"), s, flags=re.S)
    s = re.sub(r"(?<!\\)\$(?:[^$\\]|\\.)+?(?<!\\)\$", lambda m: " \u27e6MATH\u27e7 " + "\n" * m.group(0).count("\n"), s,
               flags=re.S)

    # --- headings / abstract / appendix ----------------------------------
    in_appendix_at = None
    am = re.search(r"\\appendix\b", s)
    if am:
        in_appendix_at = am.start()
    heads = []
    abs_m = re.search(r"\\begin\{abstract\}", s)
    if abs_m:
        heads.append((line_of(abs_m.start()), 1, "Abstract"))
    abs_e = re.search(r"\\end\{abstract\}", s)
    if abs_e:
        heads.append((line_of(abs_e.start()), 1, "Front matter"))

    out = []
    pos = 0
    rx = re.compile(r"\\([A-Za-z@]+)\*?|\\(.)", re.S)
    while True:
        m = rx.search(s, pos)
        if not m:
            out.append(s[pos:])
            break
        out.append(s[pos: m.start()])
        name = m.group(1)
        if name is None:  # escaped char
            ch = m.group(2)
            rep = {"%": "%", "&": "&", "_": "_", "#": "#", "$": "$", "{": "", "}": "",
                   "\\": " ", ",": " ", ";": " ", "!": "", " ": " ", "-": "", "@": "", "/": "",
                   "\n": "\n", "'": "", "`": "", '"': "", "^": "", "~": "", "=": "", ".": ""}.get(ch, " ")
            out.append(rep)
            pos = m.end()
            continue
        if name in HEADING_CMDS:
            end, opts, reqs = _parse_args(s, m.end(), 1, 1)
            if reqs:
                title = re.sub(r"\\[A-Za-z]+|[{}]", " ", s[reqs[0][0]: reqs[0][1]])
                title = re.sub(r"\s+", " ", title).strip()
                lvl = HEADING_CMDS[name]
                if in_appendix_at is not None and m.start() > in_appendix_at and lvl <= 1:
                    title = "Appendix: " + title
                heads.append((line_of(m.start()), lvl, title))
                out.append(_nl(s[m.start(): end]))
                pos = end
                continue
        if name in ("item",):
            end, _o, _r = _parse_args(s, m.end(), 1, 0)
            out.append(" ")
            pos = end
            continue
        if name in ("href",):
            end, _o, reqs = _parse_args(s, m.end(), 0, 2)
            keep = s[reqs[1][0]: reqs[1][1]] if len(reqs) > 1 else ""
            out.append(" " + keep + " " + "\n" * s[m.start(): end].count("\n"))
            pos = end
            continue
        if name in ("texorpdfstring",):
            end, _o, reqs = _parse_args(s, m.end(), 0, 2)
            keep = s[reqs[0][0]: reqs[0][1]] if reqs else ""
            out.append(keep + "\n" * s[m.start(): end].count("\n"))
            pos = end
            continue
        if name in ("ldots", "dots", "cdots", "textellipsis"):
            out.append("...")
            pos = m.end()
            continue
        if name in ("textemdash",):
            out.append("---")
            pos = m.end()
            continue
        if name in ("textendash",):
            out.append("--")
            pos = m.end()
            continue
        if name in DROP_CMDS_1 or name.startswith("cite"):
            end, _o, _r = _parse_args(s, m.end(), 3, 2 if name in ("newcommand", "renewcommand", "providecommand",
                                                                     "definecolor", "setlength", "hypertarget",
                                                                     "hyperlink", "resizebox", "scalebox",
                                                                     "multicolumn", "multirow") else 1)
            if name in ("multicolumn", "multirow"):
                end, _o, _r = _parse_args(s, m.end(), 1, 3)
            if name in ("begin", "end"):
                end, _o, _r = _parse_args(s, m.end(), 0, 1)
                # \begin{env}[opt] -> drop optional theorem titles too
                end2, _o2, _r2 = _parse_args(s, end, 1, 0)
                end = end2
            out.append(_nl(s[m.start(): end]))
            pos = end
            continue
        # generic: drop the command name and optional args, keep {content}
        end, _o, _r = _parse_args(s, m.end(), 2, 0)
        out.append(" " if name not in ("emph", "textbf", "textit", "texttt", "textsc", "underline",
                                       "mbox", "text", "textrm", "textsf", "textsl", "textup",
                                       "mathrm", "uline") else "")
        out.append("\n" * s[m.start(): end].count("\n"))
        pos = end
    s = "".join(out)
    s = s.replace("{", "").replace("}", "").replace("\u27e6MATH\u27e7", "[MATH]")
    s = s.replace("``", '"').replace("''", '"').replace("~", " ")
    doc.headings = sorted(heads)

    # --- paragraphs from source blank lines --------------------------------
    plines = s.split("\n")
    src_lines = lines
    doc.paras = []
    heads_sorted = doc.headings
    block: List[Tuple[int, str]] = []
    top_heads = [(li, t) for (li, lvl, t) in heads_sorted if lvl <= 1]

    def section_at(li: int) -> str:
        name = "Front matter"
        for hl, t in top_heads:
            if hl <= li:
                name = t
            else:
                break
        return name

    def flush():
        if block:
            text_pieces = [(li, t) for li, t in block if t.strip()]
            if text_pieces:
                doc.paras.append(Para(text_pieces, section_at(text_pieces[0][0])))
        block.clear()

    for i, pl in enumerate(plines):
        if i < len(src_lines) and not src_lines[i].strip():
            flush()
            continue
        if re.search(r"\\par\b", src_lines[i] if i < len(src_lines) else ""):
            block.append((i, pl))
            flush()
            continue
        block.append((i, pl))
    flush()


# ============================================================================
# Markdown and plain text
# ============================================================================


def _parse_md(doc: Doc):
    lines = list(doc.raw_lines)
    in_code = False
    in_html_comment = False
    out = []
    for i, line in enumerate(lines):
        if re.match(r"^\s*(```|~~~)", line):
            in_code = not in_code
            out.append("")
            continue
        if in_code:
            out.append("")
            continue
        # html comments
        while True:
            if in_html_comment:
                e = line.find("-->")
                if e < 0:
                    doc.comments.append((i, line, True))
                    line = ""
                    break
                doc.comments.append((i, line[:e], True))
                line = line[e + 3:]
                in_html_comment = False
            st = line.find("<!--")
            if st < 0:
                break
            e = line.find("-->", st)
            if e < 0:
                doc.comments.append((i, line[st + 4:], not line[:st].strip()))
                line = line[:st]
                in_html_comment = True
                break
            doc.comments.append((i, line[st + 4: e], not line[:st].strip() and not line[e + 3:].strip()))
            line = line[:st] + line[e + 3:]
        hm = re.match(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if hm:
            lvl = len(hm.group(1))
            doc.headings.append((i, lvl, hm.group(2).strip()))
            if not doc.title and lvl == 1:
                doc.title = hm.group(2).strip()
            out.append(None)  # paragraph break
            continue
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            doc.counts["item"] = doc.counts.get("item", 0) + 1
            if i == 0 or not re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i - 1]):
                doc.counts["itemize"] = doc.counts.get("itemize", 0) + 1
            line = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", line)
        if re.match(r"^\s*\|.*\|\s*$", line):  # tables
            out.append("")
            continue
        line = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)
        line = re.sub(r"\$\$.*?\$\$|\$[^$]+\$", " [MATH] ", line)
        for cm in re.finditer(r"`([^`]+)`", line):
            doc.texttt_tokens.update(re.findall(r"[A-Za-z0-9_]+", cm.group(1)))
        line = line.replace("`", "")
        out.append(line)
    doc.counts.setdefault("itemize", 0)
    doc.counts.setdefault("item", 0)
    doc.counts["paragraph_cmd"] = 0
    top = min([lvl for _, lvl, _ in doc.headings], default=1)
    sec_level = top + 1 if sum(1 for _, l, _ in doc.headings if l == top) <= 1 else top

    def section_at(li):
        name = "Front matter"
        for hl, lvl, t in doc.headings:
            if hl <= li and lvl <= sec_level:
                name = t
        return name

    block = []
    for i, line in enumerate(out):
        if line is None or not line.strip():
            if block:
                doc.paras.append(Para(block, section_at(block[0][0])))
            block = []
            continue
        block.append((i, line))
    if block:
        doc.paras.append(Para(block, section_at(block[0][0])))


_TXT_HEAD = re.compile(
    r"^\s*(?:(?:\d+(?:\.\d+){0,2}|[A-H](?:\.\d+)?)\.?\s+)?([A-Z][A-Za-z\-:,&/' ]{2,70})\s*$")
_TXT_KNOWN = re.compile(r"^(abstract|introduction|related work|background|method(s|ology)?|approach|"
                        r"experiments?|experimental (setup|results)|results|discussion|conclusions?|"
                        r"limitations?|references|bibliography|acknowledg(e)?ments?|appendix.*|"
                        r"supplementary.*|broader impact.*|ethics.*|future work)$", re.I)


def _parse_txt(doc: Doc):
    lines = doc.raw_lines
    numbered_head = re.compile(r"^\s*(\d+(?:\.\d+){0,2}|[A-H](?:\.\d+)?)\.?\s+[A-Z]")
    in_refs = False
    block = []
    section = "Front matter"
    if lines:
        doc.title = next((l.strip() for l in lines if l.strip()), "")
    for i, line in enumerate(lines):
        st = line.strip()
        # undo "I NTRODUCTION" small-caps splits produced by PDF extraction
        st_fix = re.sub(r"\b([A-Z]) ([A-Z]{2,})\b", r"\1\2", st)
        is_head = False
        if st and len(st.split()) <= 9 and not st.endswith((".", ",", ";")):
            m = _TXT_HEAD.match(st_fix)
            if m:
                title = m.group(1).strip()
                if _TXT_KNOWN.match(title) or (numbered_head.match(st_fix) and title[:1].isupper()
                                               and sum(c.isalpha() for c in title) >= 4
                                               and not re.search(r"\d{2,}", title)):
                    is_head = True
        if is_head:
            if block:
                if not in_refs:
                    doc.paras.append(Para(block, section))
                block = []
            title = _TXT_HEAD.match(st_fix).group(1).strip()
            title = title.title() if title.isupper() else title
            low = title.lower()
            if low in ("references", "bibliography"):
                in_refs = True
            elif in_refs and (low.startswith(("appendix", "supplementary")) or re.match(r"^[A-H]\b", st_fix)):
                in_refs = False
            if not in_refs:
                doc.headings.append((i, 1, title))
                section = title
            continue
        if not st:
            if block and not in_refs:
                doc.paras.append(Para(block, section))
            block = []
            continue
        if not in_refs:
            block.append((i, st))
        else:
            doc.ref_lines.append((i, st))
    if block and not in_refs:
        doc.paras.append(Para(block, section))
    doc.counts.update({"itemize": 0, "item": 0, "paragraph_cmd": 0})


# ============================================================================
# Text utilities
# ============================================================================

WORD_RX = re.compile(r"[A-Za-z][A-Za-z'\u2019\-]*")
ABBREV = re.compile(
    r"(?:\b(?:e\.g|i\.e|et al|etc|vs|cf|Fig|Figs|Eq|Eqs|Sec|Secs|Tab|Ref|Refs|No|resp|approx|Dr|Prof|Mr|Ms|"
    r"ca|viz|Def|Thm|Lem|Prop|Alg|App|Ch|Vol|pp|Appx|Fig|w\.r\.t|a\.k\.a|Corr|Inc|Ltd|St|Jr|Sr|Eqn|Thms)|"
    r"\b[A-Z])\.$")
SENT_END = re.compile(r"[.!?][\"'\u201d\u2019)\]]*\s+(?=[\"'\u201c(\[]?[A-Z0-9])")


def split_sentences(text: str) -> List[Tuple[int, str]]:
    out = []
    start = 0
    for m in SENT_END.finditer(text):
        head = text[start: m.start() + 1]
        if ABBREV.search(head.rstrip()):
            continue
        out.append((start, text[start: m.end()].strip()))
        start = m.end()
    tail = text[start:].strip()
    if tail:
        out.append((start, tail))
    return out


def words(text: str) -> List[str]:
    return WORD_RX.findall(text)


def snippet(text: str, a: int, b: int, width: int = 70) -> str:
    lo = max(0, a - width)
    hi = min(len(text), b + width)
    s = text[lo:hi]
    s = re.sub(r"\s+", " ", s).strip()
    return ("..." if lo > 0 else "") + s + ("..." if hi < len(text) else "")


# ============================================================================
# Check machinery
# ============================================================================


class Analysis:
    def __init__(self, doc: Doc, max_examples: int = 5, source: bool = False):
        self.doc = doc
        self.max_ex = max_examples
        self.source = source
        self.n_words = sum(len(words(p.text)) for p in doc.paras)
        self.sentences: List[Tuple[Para, int, str]] = []
        for p in doc.paras:
            for off, s in split_sentences(p.text):
                self.sentences.append((p, off, s))
        self.results: Dict[str, dict] = {}

    def per1k(self, n: float) -> float:
        return round(1000.0 * n / self.n_words, 3) if self.n_words else 0.0

    def new(self, cid: str, title: str, evidence: str) -> dict:
        r = {"id": cid, "title": title, "evidence": evidence, "count": 0, "per_1k": 0.0,
             "sub": {}, "examples": [], "available": True, "notes": []}
        self.results[cid] = r
        return r

    def add_example(self, r: dict, line_idx: int, text: str, tag: str = ""):
        if len(r["examples"]) < self.max_ex:
            r["examples"].append({"loc": self.doc.loc(line_idx), "tag": tag, "text": text})

    def scan(self, r: dict, patterns: List[Tuple[str, str, int]], weak: Tuple[str, ...] = (),
             paras: Optional[List[Para]] = None, sections: bool = False, skip=None, dedupe: bool = False):
        """patterns: (subname, regex, flags). Weak subs are reported but not added to count.
        skip(sub, para, match) -> True drops a match entirely (known false-positive contexts)."""
        sec_hits: Dict[str, int] = {}
        hits = []
        for sub, rx, flags in patterns:
            r["sub"].setdefault(sub, 0)
            crx = re.compile(rx, flags)
            for p in (paras if paras is not None else self.doc.paras):
                for m in crx.finditer(p.text):
                    if skip is not None and skip(sub, p, m):
                        continue
                    r["sub"][sub] += 1
                    hits.append((sub, p, m))
        if dedupe:  # overlapping matches of different sub-patterns count once
            kept, spans = [], {}
            for h in sorted(hits, key=lambda h: (id(h[1]), h[2].start())):
                sp = spans.setdefault(id(h[1]), [])
                if any(h[2].start() < e and s < h[2].end() for s, e in sp):
                    r["sub"][h[0]] -= 1
                    continue
                sp.append((h[2].start(), h[2].end()))
                kept.append(h)
            hits = kept
        for sub, p, m in sorted(hits, key=lambda h: (h[1].line_at(h[2].start()))):
            if sub in weak:
                continue
            r["count"] += 1
            sec_hits[p.section] = sec_hits.get(p.section, 0) + 1
            self.add_example(r, p.line_at(m.start()), snippet(p.text, m.start(), m.end()), sub)
        if weak:
            r["weak_subpatterns"] = list(weak)
        r["per_1k"] = self.per1k(r["count"])
        # always report where hits sit, so text that is not author prose stands out (feedback 2026-10-07)
        r["by_section"] = sec_hits
        return hits


I = re.I

# ----------------------------------------------------------------------------- L layer


# CRediT contributor-role names ("Writing -- original draft", "Writing -- review & editing") are a
# publisher-mandated taxonomy, not prose. Matches inside them are dropped by L01 and S03 (issue #1).
CREDIT_ROLE_RX = re.compile(r"\bWriting\s*(?:\u2013|\u2014|---|--|-)\s*(?:original\s+draft|review\s*(?:&|\\&|and)\s*editing)",
                            re.I)


def _in_credit_role(text: str, m) -> bool:
    return any(c.start() <= m.start() < c.end() for c in CREDIT_ROLE_RX.finditer(text))


def _credit_skip(sub, para, m) -> bool:
    return _in_credit_role(para.text, m)


def check_L01(a: Analysis):
    r = a.new("L01", "Em dashes", "L01")
    pats = [
        ("unicode_em_dash", "\u2014", 0),
        ("latex_triple_hyphen", r"(?<!-)---(?!-)", 0),
        ("spaced_double_hyphen", r"(?<=[A-Za-z,)\"'])\s+--\s+(?=[A-Za-z(\"'])", 0),
        ("spaced_en_dash", r"(?<=[A-Za-z,)])\s+\u2013\s+(?=[A-Za-z(])", 0),
    ]
    a.scan(r, pats, skip=_credit_skip)


L02_PATTERNS = [
    ("not_just_X_but", r"\bnot\s+(?:just|merely|simply)\b[^.;:!?]{1,90}?\bbut\b", I),
    ("not_only_X_but", r"\bnot\s+only\b[^.;:!?]{1,90}?\bbut\b", I),
    ("its_not_X_its_Y", r"\b(?:it|this|that)(?:'s|\u2019s|\s+is)\s+not\b[^.;!?]{1,70}?(?:[;,]|\u2014|---)\s*"
                        r"(?:it|this|that)(?:'s|\u2019s|\s+is)\b", I),
    ("not_X_but_rather_Y", r"\bnot\b[^.;!?]{1,70}?,?\s+but\s+rather\b", I),
    ("not_X_comma_but_Y", r"\bnot\s+(?!only\b|just\b|merely\b|simply\b|necessarily\b)[^.;,!?]{1,50},\s+but\s+"
                          r"(?!rather\b|also\b)", I),
    ("not_X_colon_Y", r"\b(?:is|are|was|were)\s+not\s+(?:merely\s+|just\s+|simply\s+|only\s+)?(?:an?\s+|the\s+)?"
                      r"[^.;:!?]{1,60}:\s+(?:it|this|they|rather|instead)\b|"
                      r"\bnot\s+(?:merely|just|simply)\s+[^.;:!?]{1,50}:\s|"
                      r"\b(?:is|are)\s+not\s+an?\s+(?:incremental|minor|simple|mere|small)\b[^.;:!?]{0,50}:", I),
    ("rather_than", r"\brather\s+than\b", I),
    ("the_real_X_is", r"\bthe\s+real\s+(?!world\b|data\b|number\b|line\b|part\b|valued?\b|time\b|images?\b)"
                      r"\w+(?:\s+\w+)?\s+(?:is|lies)\b", I),
    ("not_about_X_about_Y", r"\bnot\s+(?:just\s+|only\s+|merely\s+)?about\b[^.!?]{1,80}?\babout\b", I),
    ("not_because_but_because", r"\bnot\s+because\b[^.!?]{1,90}?\bbut\s+because\b", I),
    ("less_about_more_about", r"\bless\s+about\b[^.!?]{1,60}?\bmore\s+about\b", I),
]


def check_L02(a: Analysis):
    r = a.new("L02", "Negative parallelism ('not X, but Y')", "L02")
    # 'rather than' and 'not only ... but (also)' are everyday academic English: measured, not counted.
    a.scan(r, L02_PATTERNS, weak=("rather_than", "not_only_X_but"))


L03_LEXICON = [
    # (canonical, era, regex)
    ("delve", "gpt4", r"\bdelv(?:e|es|ed|ing)\b"),
    ("tapestry", "gpt4", r"\btapestr(?:y|ies)\b"),
    ("testament", "gpt4", r"\btestament\b"),
    ("intricate", "gpt4", r"\bintricate(?:ly)?\b|\bintricacies\b"),
    ("meticulous", "gpt4", r"\bmeticulous(?:ly)?\b"),
    ("realm", "gpt4", r"\brealms?\b"),
    ("boasts", "gpt4", r"\bboast(?:s|ed|ing)?\b"),
    ("align with", "4o", r"\balign(?:s|ed|ing)?\s+(?:well\s+|closely\s+)?with\b"),
    ("foster", "4o", r"\bfoster(?:s|ed|ing)?\b"),
    ("showcase", "4o", r"\bshowcas(?:e|es|ed|ing)\b"),
    ("underscore", "4o", r"\bunderscor(?:e|es|ed|ing)\b"),
    ("pivotal", "4o", r"\bpivotal\b"),
    ("landscape", "4o", r"(?<!loss )(?<!optimization )(?<!energy )(?<!fitness )(?<!error )(?<!reward )"
                        r"(?<!objective )(?<!likelihood )(?<!value )\blandscapes?\b"),
    ("interplay", "4o", r"\binterplay\b"),
    ("garner", "4o", r"\bgarner(?:s|ed|ing)?\b"),
    ("bolster", "4o", r"\bbolster(?:s|ed|ing)?\b"),
    ("emphasize", "gpt5", r"\bemphasi[sz](?:e|es|ed|ing)\b"),
    ("enhance", "gpt5", r"\benhanc(?:e|es|ed|ing|ement|ements)\b"),
    ("highlight", "gpt5", r"\bhighlight(?:s|ed|ing)?\b"),
    ("seamless", "gpt5", r"\bseamless(?:ly)?\b"),
    ("crucial", "gpt5", r"\bcrucial(?:ly)?\b"),
    ("comprehensive", "gpt5", r"\bcomprehensive(?:ly)?\b"),
    ("notably", "gpt5", r"\bnotably\b"),
    ("additionally", "gpt5", r"\badditionally\b"),
    ("leverage", "gpt5", r"\bleverag(?:e|es|ed|ing)\b"),
    ("nuanced", "gpt5", r"\bnuanced?\b"),
    ("multifaceted", "gpt5", r"\bmulti-?faceted\b"),
    ("groundbreaking", "gpt5", r"\bground-?breaking\b"),
    ("transformative", "gpt5", r"\btransformative\b"),
    # v0.2: load-bearing / principled / first-class are counted in L14 only (no double counting)
]


def check_L03(a: Analysis):
    r = a.new("L03", "AI-associated lexicon cluster", "L03")
    per_word: Dict[str, int] = {}
    per_era: Dict[str, int] = {"gpt4": 0, "4o": 0, "gpt5": 0}
    hits = []
    for canon, era, rx in L03_LEXICON:
        crx = re.compile(rx, I)
        for p in a.doc.paras:
            for m in crx.finditer(p.text):
                per_word[canon] = per_word.get(canon, 0) + 1
                per_era[era] += 1
                hits.append((p.line_at(m.start()), canon, p, m))
    for li, canon, p, m in sorted(hits, key=lambda h: h[0]):
        a.add_example(r, li, snippet(p.text, m.start(), m.end()), canon)
    r["count"] = len(hits)
    r["per_1k"] = a.per1k(len(hits))
    r["sub"] = {f"era_{k}": v for k, v in per_era.items()}
    r["per_word"] = dict(sorted(per_word.items(), key=lambda kv: -kv[1]))
    top = max(per_word.items(), key=lambda kv: kv[1]) if per_word else ("", 0)
    r["max_repeat"] = {"word": top[0], "count": top[1]}
    if top[1] >= 6:
        r["notes"].append(f"'{top[0]}' repeats {top[1]} times (EVIDENCE L03: >=6 repeats of one word is a ** signal)")
    r["notes"].append("'robust' is deliberately not counted (technical term in ML).")


L04_WORDS = ("Additionally", "Notably", "Moreover", "Furthermore", "Importantly", "Interestingly",
             "Crucially", "Remarkably", "Ultimately", "Overall")


# Calibration (2026-10-05): "Moreover"/"Furthermore" are used MORE by the pre-ChatGPT human corpus
# (AUC 0.30/0.38), so they are reported but not counted; "Additionally" separated best (AUC 0.80).
L04_WEAK = ("Moreover", "Furthermore")


def check_L04(a: Analysis):
    r = a.new("L04", "Sentence-initial transition pipeline", "L04")
    rx = re.compile(r"^[\"'(\[]?(%s)\s*," % "|".join(L04_WORDS))
    sub: Dict[str, int] = {w: 0 for w in L04_WORDS}
    for p, off, s in a.sentences:
        m = rx.match(s)
        if m:
            w = m.group(1)
            sub[w] += 1
            if w in L04_WEAK:
                continue
            r["count"] += 1
            a.add_example(r, p.line_at(off), snippet(s, 0, len(m.group(0)), 90), w)
    r["sub"] = sub
    r["weak_subpatterns"] = list(L04_WEAK)
    r["per_1k"] = a.per1k(r["count"])
    r["share_of_sentences"] = round(r["count"] / max(1, len(a.sentences)), 4)


def check_L05(a: Analysis):
    r = a.new("L05", "Copula avoidance / distanced reporting", "L05")
    pats = [
        ("serves_as", r"\bserv(?:es|ed|ing|e)\s+as\s+(?!(?:an?\s+|the\s+)?(?:inputs?|outputs?|baselines?|targets?|"
                      r"labels?|features?|queries|query|keys?|values?|anchors?|ground\s+truth|training|test|"
                      r"validation|supervision|proxy|reference)\b)", I),
        ("stands_as", r"\bstand(?:s|ing)?\s+as\b", I),
        ("plays_X_role", r"\bplay(?:s|ed|ing)?\s+(?:a|an)\s+(?:crucial|pivotal|key|vital|central|critical|"
                         r"significant|important|essential|fundamental|instrumental)\s+role\b", I),
        ("our_findings_indicate", r"\bour\s+(?:findings|results|analysis|analyses|experiments|observations)\s+"
                                  r"(?:indicate|reveal|demonstrate|suggest|underscore|highlight)\b", I),
    ]
    a.scan(r, pats)


HEDGE_WORDS = {"may", "might", "could", "possibly", "potentially", "perhaps", "arguably", "presumably",
               "conceivably", "seemingly", "somewhat", "plausibly", "maybe"}


def check_L06(a: Analysis):
    r = a.new("L06", "Stacked hedges", "L06")
    explicit = re.compile(r"\b(?:could|may|might)\s+(?:potentially|possibly|arguably|perhaps|conceivably|"
                          r"plausibly)\b|\bpossibly\s+(?:could|may|might)\b|\bperhaps\s+(?:could|may|might)\b", I)
    sub = {"explicit_pair": 0, "window_pair": 0}
    for p, off, s in a.sentences:
        found = False
        for m in explicit.finditer(s):
            sub["explicit_pair"] += 1
            r["count"] += 1
            found = True
            a.add_example(r, p.line_at(off), snippet(s, m.start(), m.end()), "explicit_pair")
        if found:
            continue
        toks = [(m.start(), m.group(0).lower()) for m in WORD_RX.finditer(s)]
        idx = [i for i, (_, t) in enumerate(toks) if t in HEDGE_WORDS]
        for x, y in zip(idx, idx[1:]):
            if 0 < y - x <= 8 and toks[x][1] != toks[y][1]:
                sub["window_pair"] += 1
                r["count"] += 1
                a.add_example(r, p.line_at(off), snippet(s, toks[x][0], toks[y][0] + len(toks[y][1])),
                              "window_pair")
                break
    r["sub"] = sub
    r["per_1k"] = a.per1k(r["count"])


def check_L07(a: Analysis):
    r = a.new("L07", "Hype / self-promotion", "L07")
    pats = [
        ("seamless", r"\bseamless(?:ly)?\b", I),
        ("elegant", r"\belegant(?:ly)?\b", I),
        ("remarkable", r"\bremarkabl[ey]\b", I),
        ("unprecedented", r"\bunprecedented\b", I),
        ("paradigm_shift", r"\bparadigm\s+shifts?\b", I),
        ("unlock", r"\bunlock(?:s|ed|ing)?\b", I),
        ("revolutionize", r"\brevolution(?:i[sz]e[sd]?|i[sz]ing|ary)\b", I),
        ("game_changing", r"\bgame-?chang(?:er|ers|ing)\b", I),
        ("significant_step", r"\ba\s+(?:significant|major|crucial|important|substantial)\s+step\s+"
                             r"(?:forward|towards?)\b", I),
        ("groundbreaking", r"\bground-?breaking\b", I),
    ]
    a.scan(r, pats)


def check_L08(a: Analysis):
    r = a.new("L08", "Trailing -ing clauses", "L08")
    pats = [(w.replace(" ", "_"), r",\s+(?:thereby\s+|thus\s+)?%s\b" % w, I) for w in (
        "highlighting", "underscoring", "emphasizing", "emphasising", "showcasing", "reflecting",
        "paving the way", "demonstrating", "ensuring", "fostering", "illustrating", "signaling",
        "offering", "revealing")]
    a.scan(r, pats)


def check_L10(a: Analysis):
    r = a.new("L10", "List-ification (items) / bold inline headers", "L10")
    d = a.doc
    if d.kind == "txt":
        r["available"] = False
        r["notes"].append("Formatting is not recoverable from plain text.")
        return
    raw = d.raw
    bold = 0
    if d.kind == "tex":
        body_start = 0
        bm = re.search(r"\\begin\s*\{document\}", raw)
        if bm:
            body_start = bm.end()
        crx = re.compile(r"\\textbf\s*\{[^{}\n]{1,80}?[:.]\s*\}|\\textbf\s*\{[^{}\n]{1,80}\}\s*:|"
                         r"\{\\bf(?:series)?\s+[^{}\n]{1,80}?[:.]\s*\}")
        lines_off = [0]
        for line in d.raw_lines:
            lines_off.append(lines_off[-1] + len(line) + 1)
        seen_lines = set()
        for m in crx.finditer(raw, body_start):
            li = bisect.bisect_right(lines_off, m.start()) - 1
            line = d.raw_lines[li]
            if re.match(r"\s*%", line) or li in seen_lines:
                continue
            pre = line[: m.start() - lines_off[li]]
            if "%" in re.sub(r"\\%", "", pre):
                continue
            seen_lines.add(li)
            bold += 1
            a.add_example(r, li, line.strip()[:160], "bold_inline_header")
        r["notes"].append("count = \\item occurrences in the body; bold inline headers are a sub-pattern.")
    else:
        for i, line in enumerate(d.raw_lines):
            if re.search(r"\*\*[^*\n]{1,80}?:\*\*|\*\*[^*\n]{1,80}\*\*\s*:", line):
                bold += 1
                a.add_example(r, i, line.strip()[:160], "bold_inline_header")
    lists = d.counts.get("itemize", 0) + d.counts.get("enumerate", 0)
    r["count"] = d.counts.get("item", 0)
    r["per_1k"] = a.per1k(r["count"])
    # Calibration (2026-10-05): bold headers and \paragraph did not separate the corpora (AUC ~0.5),
    # list items did (AUC ~0.9), so the band uses list items per 1k words.
    r["metric"] = "list_items_per_1k"
    r["value"] = a.per1k(d.counts.get("item", 0))
    r["sub"] = {"bold_inline_header": bold, "paragraph_cmd": d.counts.get("paragraph_cmd", 0),
                "list_envs": lists, "items": d.counts.get("item", 0)}
    r["paragraph_cmd_per_1k"] = a.per1k(d.counts.get("paragraph_cmd", 0))
    r["list_envs_per_1k"] = a.per1k(lists)
    r["notes"].append("Contribution bullet lists are field convention and are included in list counts.")


def check_L14(a: Analysis):
    r = a.new("L14", "Register-mismatch words / model tics", "L14")
    pats = [
        ("audit", r"\baudit(?:s|ed|ing)?\b", I),
        ("forensic", r"\bforensics?\b", I),
        ("surgical", r"\bsurgical(?:ly)?\b", I),
        ("load-bearing", r"\bload-bearing\b", I),
        ("principled", r"\bprincipled\b", I),
        ("first-class", r"\bfirst-class\b", I),
        ("honest", r"\bhonest(?:ly)?\b", I),
        ("genuinely", r"\bgenuinely\b", I),
        ("crisp", r"\bcrisp(?:ly)?\b", I),
    ]
    a.scan(r, pats)


def _pct(vals: List[float], q: float) -> float:
    if not vals:
        return 0.0
    v = sorted(vals)
    k = (len(v) - 1) * q
    f = math.floor(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def check_L15(a: Analysis):
    r = a.new("L15", "Rhythm uniformity (sentence-length statistics)", "L15")
    lens = [len(words(s)) for _p, _o, s in a.sentences]
    lens = [n for n in lens if n >= 3]
    if len(lens) < 20:
        r["available"] = False
        r["notes"].append("Too few sentences for rhythm statistics.")
        return
    mean = sum(lens) / len(lens)
    sd = math.sqrt(sum((x - mean) ** 2 for x in lens) / (len(lens) - 1))
    r["sentences"] = len(lens)
    r["sentence_len_mean"] = round(mean, 2)
    r["sentence_len_sd"] = round(sd, 2)
    r["sentence_len_cv"] = round(sd / mean, 4) if mean else 0.0
    r["metric"] = "sentence_len_cv"
    r["value"] = r["sentence_len_cv"]
    r["count"] = len(lens)
    if a.doc.kind != "txt":
        n_par = sum(1 for p in a.doc.paras if len(words(p.text)) >= 20)
        r["paragraphs_per_1k"] = a.per1k(n_par)
        plens = [len(words(p.text)) for p in a.doc.paras if len(words(p.text)) >= 20]
        if len(plens) >= 5:
            pm = sum(plens) / len(plens)
            psd = math.sqrt(sum((x - pm) ** 2 for x in plens) / (len(plens) - 1))
            r["paragraph_len_cv"] = round(psd / pm, 4)
    r["notes"].append("Lower CV = more uniform rhythm. Highest false-positive rate of all checks (EVIDENCE L15).")
    r["per_1k"] = None


def check_L16(a: Analysis):
    r = a.new("L16", "Rhetorical questions / chatty register", "L16")
    q = 0
    for p, off, s in a.sentences:
        st = s.rstrip()
        if st.endswith("?") and not re.search(r"[\"\u201c][^\"\u201d]*\?[\"\u201d]?\s*$", st) \
                and not st.startswith(('"', "\u201c")) and len(words(st)) >= 3:
            q += 1
            r["count"] += 1
            a.add_example(r, p.line_at(off), snippet(st, 0, len(st), 0)[:200], "question")
    r["sub"]["question"] = q
    a.scan(a.new("_tmp", "", ""), [
        ("lets", r"\bLet(?:'s|\u2019s)\b", 0),
        ("let_us_chatty", r"\bLet\s+us\s+(?:take|look|dive|explore|unpack|turn|break|step|now\s+turn)\b", 0),
    ])
    tmp = a.results.pop("_tmp")
    r["sub"].update(tmp["sub"])
    r["count"] += tmp["count"]
    for e in tmp["examples"]:
        if len(r["examples"]) < a.max_ex:
            r["examples"].append(e)
    r["per_1k"] = a.per1k(r["count"])


# ----------------------------------------------------------------------------- S layer

EXCLUDED_SECTION_RX = re.compile(r"limitation|related|prior work|background|ethic|broader|impact|"
                                 r"checklist|acknowledg|societal|reproducib", I)


# "it does not imply" between mathematical objects is a precise, checkable statement in theory
# writing, not a defensive hedge (issue #3).
_MATH_SUBJECT_RX = re.compile(r"(?:\b(?:assumptions?|lemmas?|propositions?|theorems?|corollar(?:y|ies)|definitions?|"
                              r"conditions?|propert(?:y|ies)|constraints?|inequalit(?:y|ies)|equations?|axioms?|"
                              r"hypothes[ie]s|bounds?|claims?\s+\d)\b|\u27e6MATH\u27e7|\(\d+\)|"
                              r"\b(?:Eq|Eqn|Thm|Lem|Prop|Cor|Def|Assump)\.)", re.I)


def _s01_skip(sub, para, m) -> bool:
    if sub != "this_does_not_mean" or not re.search(r"imply\b", m.group(0), re.I):
        return False
    text = para.text
    starts = [o for o, _s in split_sentences(text)]
    sent_start = max([o for o in starts if o <= m.start()] or [0])
    return bool(_MATH_SUBJECT_RX.search(text[sent_start:m.start()]))


def check_S01(a: Analysis):
    r = a.new("S01", "Defensive pre-emptive hedging", "S01")
    pats = [
        ("we_do_not_claim", r"\bwe\s+(?:do\s+not|don't|don\u2019t|make\s+no|are\s+not)\s+(?:claim|claiming)\b|"
                            r"\bwe\s+make\s+no\s+claims?\b", I),
        ("we_do_not_argue", r"\bwe\s+(?:do\s+not|don't|don\u2019t)\s+(?:argue|suggest|intend\s+to|purport|mean\s+to)\b", I),
        # procedural in most human papers ("we do not consider matches within ..."): measured, not counted
        ("we_do_not_address", r"\bwe\s+(?:do\s+not|don't|don\u2019t)\s+(?:address|consider|study|aim|seek)\b", I),
        ("this_is_not_to_say", r"\b(?:this|that)\s+is\s+not\s+to\s+(?:say|suggest|claim|imply)\b|"
                               r"\bnot\s+to\s+(?:suggest|claim|imply)\s+that\b", I),
        ("this_does_not_mean", r"\b(?:this|that|these|it)\s+(?:does|do)\s+not\s+(?:mean|imply|suggest)\b", I),
        ("our_goal_is_not", r"\bour\s+(?:goal|aim|intent|intention|purpose|focus)\s+is\s+not\b", I),
        ("important_to_note_that_our", r"\bit\s+is\s+important\s+to\s+(?:note|emphasi[sz]e|stress)\s+that\s+"
                                       r"(?:this|our|these|we)\b", I),
        ("we_emphasize_that", r"\bwe\s+(?:emphasi[sz]e|stress|caution|reiterate)\s+that\b", I),
        ("to_be_clear", r"\bto\s+be\s+clear\b", I),
    ]
    hits = a.scan(r, pats, weak=("we_do_not_address",), sections=True, skip=_s01_skip)
    hits = [h for h in hits if h[0] != "we_do_not_address"]
    # Anti-Autoresearch-style density rule on distinct sentences outside excluded sections
    sents = {}
    for sub, p, m in hits:
        if EXCLUDED_SECTION_RX.search(p.section or ""):
            continue
        starts = [o for o, _s in split_sentences(p.text)]
        sent_start = max([o for o in starts if o <= m.start()] or [0])
        sents[(id(p), sent_start)] = p.section
    secs = set(sents.values())
    fired = len(sents) >= 4 and len(secs) >= 2
    r["rule"] = {"hedge_sentences_outside_excluded": len(sents), "sections": sorted(secs),
                 "fired": fired,
                 "in_abstract_or_intro": any(re.search(r"abstract|introduction|front", s, I) for s in secs)}
    if fired:
        r["notes"].append("Density rule fired: >=4 defensive-hedge sentences across >=2 sections outside "
                          "Limitations/Related Work (EVIDENCE S01 *** shape). Read them: do they constrain a "
                          "conclusion, or placate an imagined reviewer?")


def check_S02(a: Analysis):
    r = a.new("S02", "Caveat diffusion across sections", "S02")
    pats = [
        ("interpreted_with_caution", r"\b(?:should|must|need\s+to)\s+be\s+interpreted\s+with\s+(?:caution|care)\b", I),
        ("further_research_needed", r"\bfurther\s+(?:research|work|investigation|study|studies|analysis|experiments?)\s+"
                                    r"(?:is|are|would\s+be)\s+(?:needed|required|warranted|necessary)\b", I),
        ("warrants_further", r"\bwarrants?\s+further\s+(?:investigation|study|research|analysis|exploration)\b", I),
        ("open_question", r"\bremains?\s+an\s+open\s+(?:question|problem)\b", I),
        ("beyond_scope", r"\bbeyond\s+the\s+scope\s+of\s+(?:this|the\s+present|our)\s+(?:paper|work|study|article)\b", I),
        ("leave_to_future_work", r"\b(?:we\s+)?leave\b[^.]{0,80}?\b(?:to|for)\s+future\s+(?:work|research|study)\b|"
                                 r"\bleft\s+(?:to|for)\s+future\s+(?:work|research)\b", I),
    ]
    a.scan(r, pats, sections=True)
    secs = [s for s, n in r["by_section"].items() if n]
    r["sections_with_caveats"] = len(secs)
    r["rule"] = {"fired": len(secs) >= 3, "sections": secs}
    if len(secs) >= 3:
        r["notes"].append(f"Caveat formulas appear in {len(secs)} sections (>=3): check whether limitations "
                          "are diffused as local hedges instead of collected in one place (review-loop fingerprint).")


def check_S03(a: Analysis):
    r = a.new("S03", "Instruction / revision leakage", "S03")
    pats = [
        ("in_response_to", r"\bin\s+response\s+to\s+(?:the\s+)?(?:concerns?|reviewers?'?|feedback|comments?|"
                           r"critiques?|suggestions?)\b", I),
        ("we_have_now_added", r"\bwe\s+have\s+(?:now\s+)?(?:added|included|revised|expanded|clarified|removed)\b", I),
        ("as_requested_by", r"\bas\s+(?:requested|suggested|recommended|pointed\s+out|noted)\s+by\s+(?:the\s+)?"
                            r"(?:reviewers?|referees?|area\s+chair|AC|editor)\b", I),
        ("per_the_reviewer", r"\bper\s+(?:the\s+)?reviewers?'?\b|\bfollowing\s+(?:the\s+)?reviewers?'?\s+"
                             r"(?:suggestions?|comments?|advice|feedback)\b", I),
        ("does_not_consider", r"\b(?:this|our|the\s+present)\s+(?:paper|work|study|article)\s+does\s+not\s+"
                              r"(?:consider|address|discuss|cover|examine|study)\b", I),
        ("we_do_not_discuss", r"\bwe\s+do\s+not\s+discuss\b", I),
        # v0.2: drafts referring to their own earlier versions (agent revision loops)
        ("earlier_version", r"\b(?:earlier|previous|prior)\s+(?:versions?|drafts?)\s+(?:of\s+(?:this|the|our)\s+"
                            r"(?:paper|manuscript|draft|work|article|study)\s+)?(?:called|described|reported|stated|"
                            r"claimed|said|misstated|incorrectly|overstated)\b|"
                            r"\bin\s+(?:an?\s+|the\s+)?(?:earlier|previous|prior)\s+(?:versions?|drafts?)\b"
                            r"(?![^.]{0,60}\b(?:appeared|presented|published\s+(?:in|at)|accepted|available|"
                            r"workshop|proceedings|conference)\b)", I),
        ("published_draft", r"\b(?:the\s+)?(?:published|submitted|first|original)\s+draft\b", I),
        ("in_this_revision", r"\bin\s+(?:this|the\s+current|the\s+present)\s+revision\b", I),
        ("originally_reported", r"\b(?:we|that\s+we|which\s+we)\s+(?:had\s+)?originally\s+(?:reported|claimed|stated|"
                                r"described)\b", I),
    ]
    a.scan(r, pats, sections=True, skip=_credit_skip)


def check_S04(a: Analysis):
    r = a.new("S04", "Work-log narration", "S04")
    pats = [
        ("we_first_tried", r"\bwe\s+(?:first|initially)\s+(?:tried|attempted|experimented)\b", I),
        ("initially_we", r"\binitially,?\s+we\b", I),
        ("after_several_attempts", r"\bafter\s+(?:several|many|multiple|numerous|repeated|a\s+few)\s+"
                                   r"(?:attempts|tries|iterations|failed)\b", I),
        ("unfortunately", r"\bunfortunately\b", I),
        ("this_failed", r"\b(?:this|that|which|the\s+(?:first|initial))\s+(?:approach\s+|attempt\s+|run\s+|"
                        r"version\s+)?(?:failed|did\s+not\s+work|didn't\s+work|crashed)\b", I),
        ("we_then", r"\bwe\s+then\b", I),
    ]
    # 'we then' is a normal procedural phrase; measured but not counted.
    a.scan(r, pats, weak=("we_then",), sections=True)


def check_S05(a: Analysis):
    r = a.new("S05", "Performative honesty", "S05")
    pats = [
        ("spirit_of_transparency", r"\bin\s+the\s+(?:spirit|interest)s?\s+of\s+(?:full\s+|complete\s+)?"
                                   r"(?:transparency|honesty|openness|candou?r)\b", I),
        ("we_transparently_report", r"\bwe\s+(?:transparently|honestly|candidly|openly)\s+(?:report|"
                                    r"acknowledge|disclose|note|admit)\b", I),
        ("for_completeness_failed", r"\bfor\s+completeness,?\s+we\s+(?:also\s+)?report\s+(?:the\s+|our\s+|all\s+)?"
                                    r"(?:failed|negative|unsuccessful)\b", I),
        ("we_report_all_failed", r"\bwe\s+report\s+(?:all|every)\s+(?:failed|negative|unsuccessful)\b", I),
        ("we_candidly", r"\bwe\s+candidly\b|\bto\s+be\s+(?:fully\s+)?(?:transparent|candid|honest)\b", I),
    ]
    a.scan(r, pats, sections=True)


def check_S06(a: Analysis):
    r = a.new("S06", "Coined terms / invented codenames (candidates)", "S06")
    acr_rx = re.compile(r"\(\s*([A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9\-]*?)(s?)\s*\)")
    defs = []
    seen = set()
    all_text = [(p, p.text) for p in a.doc.paras]
    # global offsets for "use after definition"
    glob = []
    pos = 0
    for p, t in all_text:
        glob.append(pos)
        pos += len(t) + 1
    big = "\n".join(t for _, t in all_text)
    for pi, (p, t) in enumerate(all_text):
        for m in acr_rx.finditer(t):
            acr = m.group(1)
            if len(acr) > 12 or acr in seen or not re.search(r"[A-Z].*[A-Z]", acr):
                continue
            prev = words(t[max(0, m.start() - 120): m.start()])[-8:]
            if len(prev) < 2:
                continue
            initials = [w[0].upper() for w in prev]
            if acr[0].upper() not in initials:
                continue
            seen.add(acr)
            gstart = glob[pi] + m.end()
            uses = len(re.findall(r"(?<![A-Za-z0-9\-])%s(?:s|es)?(?![A-Za-z0-9])" % re.escape(acr), big[gstart:]))
            long_form = " ".join(prev[-max(2, min(len(prev), len(re.findall('[A-Z]', acr)) + 1)):])
            defs.append({"acronym": acr, "long_form_tail": long_form, "uses_after_def": uses,
                         "loc": a.doc.loc(p.line_at(m.start()))})
    low = [d for d in defs if d["uses_after_def"] <= 2]
    coin = [
        ("we_term_this", r"\b(?:we|which\s+we|that\s+we|what\s+we)\s+(?:term|call|dub|name|refer\s+to|coin)\b"
                         r"(?:\s+(?:this|these|it|them|as))?", I),
        ("dubbed_termed", r"\b(?:dubbed|termed|coined)\b", I),
        ("hyphen_cap_compound", r"\b[A-Z][a-z]+(?:-[A-Z][A-Za-z0-9]*)+\b", 0),
        ("quoted_coinage", r"[\"\u201c](?:[A-Za-z][\w\-]*)(?:\s+[A-Za-z][\w\-]*){0,3}[\"\u201d]", 0),
    ]
    a.scan(r, coin, weak=("hyphen_cap_compound", "quoted_coinage"))
    for d in low[: a.max_ex]:
        if len(r["examples"]) < a.max_ex * 2:
            r["examples"].append({"loc": d["loc"], "tag": "low_use_acronym",
                                  "text": f"{d['acronym']} (... {d['long_form_tail']}) used {d['uses_after_def']}x after definition"})
    r["sub"]["acronym_definitions"] = len(defs)
    r["sub"]["low_use_acronyms"] = len(low)
    r["count"] += len(low)
    r["per_1k"] = a.per1k(r["count"])
    r["acronyms"] = defs[:60]
    r["notes"].append("Acronym use counts only see prose: uses inside tables/figures/macros are invisible, "
                      "so a low count is a prompt to check, not a finding.")


def check_S13(a: Analysis):
    r = a.new("S13", "Reviewer-Q&A / claim-matrix structure", "S13")
    hq = 0
    for li, lvl, t in a.doc.headings:
        if re.match(r"^\s*(?:R?Q\d+|Question\s+\d+)\b", t, I) or t.strip().endswith("?"):
            hq += 1
            a.add_example(r, li, t, "qa_heading")
    pats = [
        ("experiment_tests_claim", r"\b(?:this|the\s+following)\s+(?:experiment|section|analysis|ablation)\s+"
                                   r"(?:tests|addresses|examines|evaluates|supports)\s+(?:Claim|Hypothesis|RQ|Q)\s*"
                                   r"[A-Z]?\d+\b", I),
        ("claim_C_n", r"\bClaims?\s+C\d+\b", 0),
        ("H_n_colon", r"(?<![A-Za-z0-9])H\d\s*[:)]", 0),
        ("RQ_n", r"\bRQ\d+\b", 0),
        ("Q_n_colon", r"(?<![A-Za-z0-9])Q\d+\s*:", 0),
    ]
    a.scan(r, pats, weak=("RQ_n",))
    r["sub"]["qa_heading"] = hq
    r["count"] += hq
    r["per_1k"] = a.per1k(r["count"])


# ----------------------------------------------------------------------------- R layer


def check_R01(a: Analysis):
    r = a.new("R01", "Pivot / diagnostic-reframing vocabulary (candidates)", "R01")
    pats = [
        ("contrary_to_expectations", r"\bcontrary\s+to\s+(?:our\s+)?(?:initial\s+)?(?:expectations?|hypothes[ie]s|"
                                     r"intuition)\b", I),
        ("surprisingly_we_find", r"\b(?:surprisingly|unexpectedly|counterintuitively),?\s+(?:we\s+(?:find|found|"
                                 r"observe|observed)|our)\b", I),
        ("pitfall", r"\bpitfalls?\b", I),
        ("an_audit_of", r"\ban\s+audit\s+of\b", I),
        ("diagnostic_study", r"\bdiagnostic\s+(?:study|analysis|evidence|experiments?|investigation)\b", I),
        ("lessons_learned", r"\blessons?\s+learn(?:ed|t)\b", I),
        ("negative_result", r"\bnegative\s+results?\b", I),
    ]
    a.scan(r, pats, sections=True)
    t = a.doc.title or ""
    if re.search(r"audit|pitfall|diagnos|lessons|negative result|revisit|what (?:really|actually)", t, I):
        r["notes"].append(f"Title has diagnostic framing: \"{t}\". Check whether a method-paper skeleton "
                          "(proposed component, ablation of it, abandoned acronym) survives in the body.")


def check_R05(a: Analysis):
    r = a.new("R05", "'3-3-3' recipe: exactly three seeds", "R05")
    pats = [
        ("three_seeds", r"\b(?:3|three)\s+(?:different\s+|independent\s+)?(?:random\s+)?seeds?\b", I),
        ("seed_list_3", r"\bseeds?\s*(?:=|:)?\s*\{?\s*0\s*,\s*1\s*,?\s*(?:and\s+)?2\s*\}?(?!\s*,\s*3)", I),
        ("three_runs", r"\b(?:3|three)\s+(?:independent\s+|random\s+|separate\s+)?(?:runs|trials)\b", I),
    ]
    a.scan(r, pats, weak=("three_runs",))
    r["notes"].append("Three seeds is common practice; this is only a signal together with unexplained choice "
                      "of exactly three datasets / baselines (check manually).")


def check_R16(a: Analysis):
    r = a.new("R16", "AI-reviewer scores used as evidence", "R16")
    pats = [
        ("automated_reviewer", r"\bautomated\s+reviewers?\b", I),
        ("ai_reviewer_score", r"\b(?:AI|LLM)[- ]reviewers?\s+(?:score|rating|assessment)s?\b", I),
        ("scored_by_ai_reviewer", r"\bscored?\b[^.]{0,60}\bby\s+(?:an?\s+)?(?:LLM|AI|automated|agentic)\s+reviewers?\b", I),
        ("agentic_reviewer", r"\bagentic\s+reviewer\b|\bpaperreview\.ai\b|\bCSPaper\b", I),
    ]
    a.scan(r, pats)


# ----------------------------------------------------------------------------- P layer


def _scan_raw(a: Analysis, r: dict, pats, include_comments: bool = True):
    """Scan the raw source line by line (P01 artifacts can hide in comments/preamble)."""
    for sub, rx, flags in pats:
        crx = re.compile(rx, flags)
        r["sub"].setdefault(sub, 0)
        for i, line in enumerate(a.doc.raw_lines):
            is_comment = a.doc.kind == "tex" and bool(re.match(r"\s*%", line))
            if is_comment and not include_comments:
                continue
            for m in crx.finditer(line):
                r["sub"][sub] += 1
                r["count"] += 1
                a.add_example(r, i, snippet(line, m.start(), m.end()), sub + (" (comment)" if is_comment else ""))
    r["per_1k"] = a.per1k(r["count"])


def _reference_texts(d: Doc) -> List[Tuple[str, List[Tuple[int, str]]]]:
    """Reference-list text that is not part of the prose: .bbl files and the references section of
    PDF text. Returns [(label, [(line_no, text), ...])]. Line numbers are 1-based within the source."""
    out = []
    for f, text in d.bbl_texts:
        out.append((os.path.basename(f), [(i + 1, ln) for i, ln in enumerate(text.split("\n"))]))
    if d.ref_lines:
        f = d.linemap[0][0] if d.linemap else d.path
        out.append((os.path.basename(f), [(li + 1, ln) for li, ln in d.ref_lines]))
    return out


def _scan_refs(a: Analysis, r: dict, pats, skip=None, weak: Tuple[str, ...] = ()):
    """Scan .bbl text and PDF reference sections (agent notes and placeholders hide there)."""
    for label, lines in _reference_texts(a.doc):
        for sub, rx, flags in pats:
            crx = re.compile(rx, flags)
            r["sub"].setdefault(sub, 0)
            for ln, text in lines:
                for m in crx.finditer(text):
                    if skip is not None and skip(sub, text, m):
                        continue
                    r["sub"][sub] += 1
                    if sub in weak:
                        continue
                    r["count"] += 1
                    if len(r["examples"]) < a.max_ex * 2:
                        r["examples"].append({"loc": f"{label}:{ln}", "tag": sub + " (references)",
                                              "text": snippet(text, m.start(), m.end())})
    r["per_1k"] = a.per1k(r["count"])


# Agent research notes that leaked into a rendered reference list (seen in a 2026 agent paper's .bbl)
AGENT_NOTE_PATS = [
    ("agent_note_in_references", r"\bVerified\s+(?:by|via|on|against|with)\b|\bVerdict\s*:|\bkill-question\b|"
                                 r"\bnear-hit\b|\bverified\s+NOT\s+PRESENT\b|\btools/\w+\.py\b|\bnote\s+to\s+self\b", I),
]


def check_P01(a: Analysis):
    r = a.new("P01", "Chatbot / tool residue", "P01")
    pats = [
        ("as_an_ai", r"\bas\s+an\s+AI(?:\s+language)?\s+model\b", I),
        ("certainly", r"\bCertainly!|\bCertainly,\s+here\s+is\b|\bSure!\s+Here\b", 0),
        ("hope_this_helps", r"\bI\s+hope\s+this\s+helps\b", I),
        ("regenerate_response", r"\bregenerate\s+response\b", I),
        ("content_reference", r"contentReference|oaicite|\boai_citation\b", I),
        ("utm_chatgpt", r"utm_source=chatgpt|utm_source=openai", I),
        ("turn_search", r"\bturn\d+(?:search|news|view|fetch)\d+\b", 0),
        ("knowledge_cutoff", r"\bas\s+of\s+my\s+(?:last\s+)?(?:knowledge\s+)?(?:update|training|cutoff)\b|"
                             r"\bknowledge\s+cut-?off\b", I),
        ("here_is_revised", r"\bHere\s+is\s+(?:the|a|your)\s+(?:revised|rewritten|improved|updated|polished)\s+"
                            r"(?:version|paragraph|text|section)\b", 0),
        ("im_sorry", r"\bI(?:'m|\s+am)\s+sorry,?\s+but\s+I\b", 0),
    ]
    _scan_raw(a, r, pats)
    _scan_refs(a, r, pats + AGENT_NOTE_PATS)


# ---- P02: two tiers ---------------------------------------------------------------------------
P02_META_PATS = [
    ("bracket_insert", r"\[\s*(?:INSERT|CITATION\s+NEEDED|CITE\s+HERE|PLACEHOLDER|ADD\s+\w+|FILL)[^\]]{0,60}\]", I),
    ("please_fill", r"\bPLEASE\s+(?:FILL|INSERT|REPLACE)\b|\bplease\s+add\s+(?:\w+\s+){0,3}here\b", I),
    ("fill_in_here", r"\b(?:FILL|INSERT|ADD|PUT)\s+(?:IN\s+)?(?:[A-Z]+\s+){0,3}HERE\b|"
                     r"\bfill\s+in\s+(?:the\s+)?\w+(?:\s+\w+)?\s+here\b", 0),
    ("conclusions_here", r"\bConclusions?\s+Here\b|\bAbstract\s+Here\b|\bYour\s+(?:text|abstract|title)\s+here\b", I),
    ("lorem_ipsum", r"\blorem\s+ipsum\b", I),
    ("illustrative_data", r"\billustrative\s+(?:only|data|values|numbers|results)\b|"
                          r"\b(?:data|table|values|numbers|results)\b[^.]{0,40}\b(?:are|is)\s+(?:purely\s+|only\s+)?"
                          r"illustrative\b", I),
    ("placeholder", r"\bPLACEHOLDER\b|\bplaceholder\s+(?:text|caption|figure|table|citation|results?|numbers?|"
                    r"values?\s+(?:for|until))\b|\b(?:this|the)\s+(?:figure|table|section|paragraph|caption|value)\s+"
                    r"is\s+(?:a|only\s+a)\s+placeholder\b", 0),
    ("as_requested", r"\bas\s+requested\b", I),
]
P02_TODO_PATS = [
    ("bracket_todo", r"\[\s*(?:TODO|TBD|REF|CITE)\b[^\]]{0,60}\]", I),
    ("todo", r"\bTODO\b|\bFIXME\b", 0),
    ("tbd", r"\bTBD\b", 0),
    ("xxx", r"\bXXX+\b", 0),
    ("unresolved_cite", r"\(\s*\?\s*\)|\[\s*\?\s*\]", 0),
    ("unresolved_ref", r"\?\?", 0),
]


def _p02_skip(sub, text_or_para, m) -> bool:
    text = text_or_para.text if isinstance(text_or_para, Para) else text_or_para
    ctx = text[max(0, m.start() - 45): m.end() + 3]
    if sub == "xxx":
        # IEEE / journal running headers: "VOL. XX, NO. XX, XXXX"; arXiv IDs with X are P03, not P02
        if re.search(r"VOL\.\s*X+|NO\.\s*X+|\bVOLUME\s+X+", ctx, I):
            return True
        if re.search(r"\d{4}\.X*$", text[max(0, m.start() - 12): m.start()]):
            return True
    return False


def check_P02_meta(a: Analysis):
    r = a.new("P02-meta", "LLM meta-commentary / unfilled template text", "P02")
    a.scan(r, P02_META_PATS, skip=_p02_skip, dedupe=True)
    _scan_refs(a, r, P02_META_PATS, skip=_p02_skip)
    r["notes"].append("Iron-clad candidate when confirmed: text addressed to the author or template filler "
                      "that no one removed (e.g. 'PLEASE FILL IN CAPTION HERE').")


def _brace_args(s: str, i: int, n: int):
    """Read up to n balanced {...} arguments starting at s[i]; returns (args, end) or (None, i)."""
    args = []
    while len(args) < n:
        while i < len(s) and s[i] in " \t\n%":
            i += 1
        if i < len(s) and s[i] == "[":  # optional argument
            j = s.find("]", i)
            if j < 0:
                return None, i
            i = j + 1
            continue
        if i >= len(s) or s[i] != "{":
            return None, i
        depth, j = 0, i
        while j < len(s):
            if s[j] == "{" and s[j - 1] != "\\":
                depth += 1
            elif s[j] == "}" and s[j - 1] != "\\":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j >= len(s):
            return None, i
        args.append(s[i + 1:j])
        i = j + 1
    return args, i


def _macro_labels(body: str):
    """Labels created inside user macros, e.g. \\newcommand{\\fig}[3]{...\\label{#3}} called as \\fig{a}{b}{fig:x}
    (issue #2). Returns (labels, has_label_macros)."""
    found, macros = set(), {}
    for m in re.finditer(r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z@]+)\}?\s*\[(\d)\](?:\[[^\]]*\])?\s*", body):
        args, _ = _brace_args(body, m.end(), 1)
        if args:
            idx = re.findall(r"\\label\s*\{\s*#(\d)\s*\}", args[0])
            if idx:
                macros[m.group(1)] = (int(m.group(2)), [int(k) for k in idx])
    for m in re.finditer(r"\\def\s*\\([A-Za-z@]+)((?:#\d)+)\s*", body):
        args, _ = _brace_args(body, m.end(), 1)
        if args:
            idx = re.findall(r"\\label\s*\{\s*#(\d)\s*\}", args[0])
            if idx:
                macros[m.group(1)] = (m.group(2).count("#"), [int(k) for k in idx])
    for name, (nargs, idx) in macros.items():
        for c in re.finditer(r"\\" + re.escape(name) + r"(?![A-Za-z@])", body):
            args, _ = _brace_args(body, c.end(), nargs)
            if args:
                for k in idx:
                    if 1 <= k <= len(args):
                        found.add(args[k - 1].strip())
    has_any = bool(re.search(r"\\label\s*\{\s*#\d", body))
    return found, has_any


def check_P02_todo(a: Analysis):
    r = a.new("P02-todo", "TODO markers / unresolved references", "P02")
    a.scan(r, P02_TODO_PATS, skip=_p02_skip)
    _scan_refs(a, r, P02_TODO_PATS, skip=_p02_skip)
    d = a.doc
    if d.kind == "tex":
        body = _strip_all_comments(d.raw)
        labels = set(re.findall(r"\\label\s*\{([^}]+)\}", body))
        macro_labels, label_macros = _macro_labels(body)
        labels |= macro_labels
        refs = re.findall(r"\\(?:ref|eqref|autoref|Autoref|cref|Cref|pageref|nameref|vref)\s*\{([^}]+)\}", body)
        missing = sorted({k.strip() for rr in refs for k in rr.split(",")
                          if k.strip() and "#" not in k and k.strip() not in labels})
        cites = _cite_keys(d)
        bibkeys = {e["key"] for e in _bib_entries(d)}
        bibkeys |= _bbl_keys(d.raw) | d.bbl_keys
        missing_cites = sorted(k for k in cites if k not in bibkeys) if bibkeys else []
        if missing and label_macros:
            # a label macro we could not expand: report as info for the compile log, do not count
            r["notes"].append("Some labels are set inside user macros; check the LaTeX log for undefined "
                              "references before treating these as unresolved: " + ", ".join(missing[:10]))
            missing = []
        r["sub"]["undefined_ref_labels"] = len(missing)
        r["sub"]["cite_keys_missing_from_bib"] = len(missing_cites)
        r["sub"]["todo_macro"] = d.counts.get("todo_macro", 0)
        r["count"] += len(missing) + len(missing_cites) + d.counts.get("todo_macro", 0)
        if missing:
            r["examples"].append({"loc": "-", "tag": "undefined_ref_labels", "text": ", ".join(missing[:10])})
        if missing_cites:
            r["examples"].append({"loc": "-", "tag": "cite_keys_missing_from_bib", "text": ", ".join(missing_cites[:10])})
        r["notes"].append("Undefined \\ref labels / missing cite keys render as '??' / '(?)' in the PDF; "
                          "they can also come from files missing from the source archive.")
    r["per_1k"] = a.per1k(r["count"])
    r["notes"].append("Weak: about 15% of pre-ChatGPT human sources contain TODO/??-type leftovers.")


# ---- P05 -------------------------------------------------------------------------------------
# separator tolerant of LaTeX line breaks, spacing commands, braces and font switches
_SEP = (r"(?:\s|\\\\(?:\*?\[[^\]]*\])?|\\(?:newline|linebreak|par|sffamily|bfseries|itshape|rmfamily|ttfamily|"
        r"large|Large|LARGE|huge|Huge|small|centering|quad|qquad)\b|\\[,;! ]|\\vspace\*?\{[^}]*\}|[{}~])+")
P05_PATS = [
    ("ai_scientist", r"(?:generated{S}by{S}(?:the{S})?AI(?:{S}|-)Scientist\b|\bAI-Scientist\b)"),
    ("generated_by_agent", r"\bthis{S}(?:paper|work|manuscript|report){S}was{S}(?:autonomously{S}"
                           r"(?:generated|written|produced)|(?:(?:entirely|fully){S})?(?:generated|written|produced)"
                           r"{S}by{S}(?:an?{S})?(?:AI|LLM|agent|autonomous|language{S}model|the{S}AI))\b"),
    ("agent_laboratory", r"\bAgent{S}Laboratory\b"),
]
LLM_AUTHOR_RX = re.compile(r"\b(?:GPT-?4o|GPT-?[345](?:\.\d)?(?:-?turbo)?|ChatGPT|Claude|Gemini|"
                           r"AI\s+Scientist|Agent\s+Laboratory|Zochi)\b", I)


def _author_block(d: Doc) -> List[Tuple[int, str]]:
    """(line index, text) of the author block."""
    out = []
    if d.kind == "tex":
        raw = _strip_all_comments(d.raw)  # same line count as d.raw
        offs = [0]
        for ln in raw.split("\n"):
            offs.append(offs[-1] + len(ln) + 1)
        for m in re.finditer(r"\\(?:author|icmlauthor|IEEEauthorblockN|name)\s*(?:\[[^\]]*\])?\s*\{", raw):
            li = bisect.bisect_right(offs, m.start()) - 1
            e = _match_brace(raw, m.end() - 1)
            block = raw[m.end(): e - 1]
            # \thanks{...} footnotes are where honest AI-use disclosures live; they are not author names
            while True:
                tm = re.search(r"\\thanks\s*\{", block)
                if not tm:
                    break
                block = block[: tm.start()] + block[_match_brace(block, tm.end() - 1):]
            out.append((li, block))
    else:
        for i, ln in enumerate(d.raw_lines[:40]):
            if re.match(r"\s*(?:#+\s*)?abstract\b", ln, I):
                break
            out.append((i, ln))
    return out


def check_P05(a: Analysis):
    r = a.new("P05", "Pipeline watermark / signature", "P05")
    d = a.doc
    joined = "\n".join(d.raw_lines)
    offs = [0]
    for ln in d.raw_lines:
        offs.append(offs[-1] + len(ln) + 1)
    spans: List[Tuple[int, int]] = []
    for sub, rx in P05_PATS:
        r["sub"].setdefault(sub, 0)
        crx = re.compile(rx.replace("{S}", _SEP), I)
        for m in crx.finditer(joined):
            if any(m.start() < e and s < m.end() for s, e in spans):
                continue  # one watermark matched by two sub-patterns counts once
            spans.append((m.start(), m.end()))
            li = bisect.bisect_right(offs, m.start()) - 1
            r["sub"][sub] += 1
            r["count"] += 1
            txt = re.sub(_SEP, " ", m.group(0)).strip()
            a.add_example(r, li, txt, sub)
    r["sub"]["llm_in_author_block"] = 0
    for li, txt in _author_block(d):
        for m in {mm.group(0).lower(): mm for mm in LLM_AUTHOR_RX.finditer(txt)}.values():
            r["sub"]["llm_in_author_block"] += 1
            r["count"] += 1
            a.add_example(r, li, re.sub(r"\s+", " ", txt).strip()[:160], "llm_in_author_block")
    if re.match(r"\s*Research\s+Report\s*:", d.title or "", I):
        r["count"] += 1
        r["sub"]["research_report_title"] = 1
        r["examples"].append({"loc": "title", "tag": "research_report_title", "text": d.title})
    r["per_1k"] = a.per1k(r["count"])
    r["notes"].append("Matches are normalized across line breaks and LaTeX spacing; a system name in prose may be "
                      "a citation of that system - read the line.")


S2_KEY_RX = re.compile(r"^[A-Z][A-Za-z'\-]+\d{4}[A-Z][a-z]+[A-Z0-9]{1,3}$")


def _cite_keys(d: Doc) -> List[str]:
    keys = []
    body = _strip_all_comments(d.raw) if d.kind == "tex" else ""
    for m in re.finditer(r"\\(?:[Cc]ite[a-zA-Z]*|[a-z]*cite[a-z]*)\*?\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}", body):
        for k in m.group(1).split(","):
            k = k.strip()
            if k and k not in keys:
                keys.append(k)
    return keys


def _bib_entries(d: Doc) -> List[dict]:
    cached = getattr(d, "_bib_cache", None)
    if cached is not None:
        return cached
    out = []
    for fname, text in d.bib_texts:
        for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]*)\s*,", text):
            typ = m.group(1).lower()
            if typ in ("string", "preamble", "comment"):
                continue
            # find entry end by brace matching from the '{'
            st = text.find("{", m.start())
            en = _match_brace(text, st)
            body = text[m.end(): en - 1]
            fields = {}
            for fm in re.finditer(r"(\w+)\s*=\s*", body):
                j = fm.end()
                if j < len(body) and body[j] == "{":
                    k = _match_brace(body, j)
                    val = body[j + 1: k - 1]
                elif j < len(body) and body[j] == '"':
                    k = body.find('"', j + 1)
                    val = body[j + 1: k if k > 0 else len(body)]
                else:
                    mm = re.match(r"[^,\n}]*", body[j:])
                    val = mm.group(0)
                fields.setdefault(fm.group(1).lower(), re.sub(r"\s+", " ", val).strip())
            out.append({"key": m.group(2), "type": typ, "fields": fields, "file": fname})
    d._bib_cache = out
    return out


_ARXIV_X_RX = re.compile(r"\b\d{4}\.[\dX]*X{2,}[\dX]*\b|\b\d{4}\.(?:\d{0,4}[Xx]{2,}\d{0,3})\b")
_ARXIV_MONTH_RX = re.compile(r"(?:arXiv\s*:?\s*|abs/|arxiv\.org/(?:abs|pdf)/)(\d{2})(\d{2})\.\d{4,5}", I)


def _ref_entries(d: Doc) -> List[Tuple[str, str, str]]:
    """Reference entries from .bbl text or a PDF references section: [(loc, number_or_key, text)]."""
    out = []
    for f, text in d.bbl_texts:
        for m in re.finditer(r"\\bibitem\s*(?:\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\}|$)",
                             text, re.S):
            ln = text.count("\n", 0, m.start()) + 1
            out.append((f"{os.path.basename(f)}:{ln}", m.group(1).strip(), re.sub(r"\s+", " ", m.group(2))))
    if d.ref_lines:
        f = os.path.basename(d.linemap[0][0]) if d.linemap else "input"
        cur = None
        for li, text in d.ref_lines:
            m = re.match(r"\s*\[(\d{1,4})\]\s*(.*)", text)
            if m:
                if cur:
                    out.append(cur)
                cur = (f"{f}:{li + 1}", m.group(1), m.group(2))
            elif cur:
                cur = (cur[0], cur[1], cur[2] + " " + text)
            else:  # author-year style without numbers: one line per pseudo-entry
                out.append((f"{f}:{li + 1}", "", text))
        if cur:
            out.append(cur)
    return out


def check_P03(a: Analysis):
    r = a.new("P03", "Bibliography anomalies (hallucination candidates)", "P03")
    d = a.doc
    ents = _bib_entries(d)
    refs = _ref_entries(d)
    if not ents and not refs:
        r["available"] = False
        r["notes"].append("No .bib, .bbl or references section found - nothing to check.")
        return
    cites = set(_cite_keys(d))
    use = [e for e in ents if not cites or e["key"] in cites]
    sub = {"doe_author": 0, "et_al_in_author": 0, "arxiv_id_with_X": 0, "arxiv_impossible_month": 0,
           "missing_year": 0, "missing_author": 0, "duplicate_title": 0, "duplicate_key": 0, "key_None": 0,
           "et_al_sole_author": 0, "duplicate_ref_number": 0}

    def ex(loc, tag, text):
        if len(r["examples"]) < a.max_ex * 2:
            r["examples"].append({"loc": loc, "tag": ",".join(tag), "text": text})

    def bad_month(blob):
        return any(int(mo) == 0 or int(mo) > 12 for _yy, mo in _ARXIV_MONTH_RX.findall(blob))

    titles: Dict[Tuple[str, str], str] = {}
    keys_seen = set()
    for e in use:
        f = e["fields"]
        au = f.get("author", "")
        tag = []
        if re.search(r"\bDoe\b", au):
            sub["doe_author"] += 1
            tag.append("doe_author")
        if re.search(r"\bet\s*\.?\s*al\b", au, I):
            sub["et_al_in_author"] += 1
            tag.append("et_al_in_author")
        blob = " ".join(f.values())
        if _ARXIV_X_RX.search(blob):
            sub["arxiv_id_with_X"] += 1
            tag.append("arxiv_id_with_X")
        if bad_month(blob):
            sub["arxiv_impossible_month"] += 1
            tag.append("arxiv_impossible_month")
        if not f.get("year") and not f.get("date"):
            sub["missing_year"] += 1
            tag.append("missing_year")
        if not au and not f.get("editor") and e["type"] not in ("misc", "online", "software", "manual"):
            sub["missing_author"] += 1
            tag.append("missing_author")
        if e["key"] == "None":
            sub["key_None"] += 1
            tag.append("key_None")
        # duplicates are only counted within one file: arXiv sources often ship several overlapping .bib files
        tnorm = re.sub(r"[^a-z0-9]", "", f.get("title", "").lower())
        fk = (e["file"], e["key"])
        if fk in keys_seen:
            sub["duplicate_key"] += 1
            tag.append("duplicate_key")
        elif tnorm and (e["file"], tnorm) in titles and titles[(e["file"], tnorm)] != e["key"]:
            sub["duplicate_title"] += 1
            tag.append("duplicate_title")
        keys_seen.add(fk)
        if tnorm:
            titles.setdefault((e["file"], tnorm), e["key"])
        if tag:
            ex(os.path.basename(e["file"]), tag, f"@{e['type']}{{{e['key']}, title={f.get('title', '')[:80]!r}, "
                                                 f"author={au[:60]!r}, year={f.get('year', '')!r}}}")
    # rendered references (.bbl / PDF text) - only when no .bib entries were checked, to avoid double counting
    if not use and refs:
        nums: Dict[str, int] = {}
        for loc, num, text in refs:
            tag = []
            if num and re.fullmatch(r"\d+", num):
                nums[num] = nums.get(num, 0) + 1
                if nums[num] == 2:
                    sub["duplicate_ref_number"] += 1
                    tag.append("duplicate_ref_number")
            if _ARXIV_X_RX.search(text):
                sub["arxiv_id_with_X"] += 1
                tag.append("arxiv_id_with_X")
            if bad_month(text):
                sub["arxiv_impossible_month"] += 1
                tag.append("arxiv_impossible_month")
            if re.search(r"\b(?:J(?:ohn|ane)?\.?\s+Doe|Doe,\s+J(?:ohn|ane)?\.?)\b", text):
                sub["doe_author"] += 1
                tag.append("doe_author")
            if re.match(r"\s*(?:\\newblock\s*)?et\s+al\.?(?:\s*,|\s+\"|\s+\u201c|\s+\()", text):
                sub["et_al_sole_author"] += 1
                tag.append("et_al_sole_author")
            if tag:
                ex(loc, tag, text[:200])
    strong = ("doe_author", "et_al_in_author", "arxiv_id_with_X", "arxiv_impossible_month", "duplicate_key",
              "duplicate_title", "key_None", "et_al_sole_author", "duplicate_ref_number")
    r["sub"] = sub
    r["count"] = sum(sub[k] for k in strong)
    r["entries_checked"] = len(use) if use else len(refs)
    r["source_checked"] = ".bib" if use else ("rendered references (.bbl / PDF text)" if refs else "-")
    r["weak_subpatterns"] = ["missing_year", "missing_author"]
    r["per_1k"] = a.per1k(r["count"])
    r["notes"].append("Candidates only: verify each against a bibliographic database (OpenAlex/Crossref/DBLP). "
                      "Scholar exports also produce odd entries; a wholly invented author list does not come from BibTeX.")


# co-author notes are human-presence evidence (EVIDENCE H06), not pipeline artifacts
_H06_COMMENT_RX = re.compile(r"^\s*%*\s*(?:[A-Z]{2,3}\s*:|TODO\s*\(\s*\w+\s*\)|\\[A-Z]{2,3}\s*\{|"
                             r"\\todo\b|\\textcolor\s*\{\s*(?:red|blue|magenta|orange|purple|cyan)\s*\})")


def _h06_traces(a: Analysis) -> Tuple[set, List[dict], int]:
    d = a.doc
    lines = set()
    exs = []
    for li, txt, _full in d.comments:
        if _H06_COMMENT_RX.search(txt) or re.search(r"\\[A-Z]{2,3}\s*\{[^}]*\}", txt):
            lines.add(li)
            if len(exs) < a.max_ex:
                exs.append({"loc": d.loc(li), "tag": "coauthor_comment", "text": txt.strip()[:140]})
    n_body = 0
    if d.kind == "tex":
        body = _strip_all_comments(d.raw)
        # macros defined as coloured notes, e.g. \newcommand{\MB}[1]{\textcolor{red}{MB: #1}}
        note_macros = set()
        for m in re.finditer(r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z]+)\}?\s*(?:\[\d\])?\s*\{(.{0,80})", body):
            if re.search(r"textcolor|color\{|todo|marginpar", m.group(2)):
                note_macros.add(m.group(1))
        rx_parts = [r"\\todo\b", r"\\textcolor\s*\{\s*(?:red|blue|magenta|orange|purple|cyan)\s*\}"]
        if note_macros:
            rx_parts.append(r"\\(?:%s)\s*\{" % "|".join(sorted(re.escape(n) for n in note_macros)))
        bm = re.search(r"\\begin\s*\{document\}", body)
        start = bm.end() if bm else 0
        for m in re.finditer("|".join(rx_parts), body[start:]):
            n_body += 1
            if len(exs) < a.max_ex:
                ln = body.count("\n", 0, start + m.start())
                exs.append({"loc": d.loc(ln), "tag": "note_macro_in_body",
                            "text": body[start + m.start(): start + m.start() + 100].replace("\n", " ")})
    return lines, exs, n_body


def check_P06(a: Analysis):
    r = a.new("P06", "LaTeX source artifacts", "P06")
    d = a.doc
    if d.kind not in ("tex", "md"):
        r["available"] = False
        r["notes"].append("Needs the LaTeX/Markdown source.")
        return
    h06_lines, h06_ex, h06_body = _h06_traces(a)

    def _is_plan(txt: str) -> bool:
        t2 = txt.strip().lstrip("%").strip()
        if len(re.findall(r"[A-Za-z]{2,}", t2)) < 3:  # separators, '%-----', '%%%%'
            return False
        if t2.startswith("\\") or re.search(r"\\(?:begin|end|includegraphics|label|section|item)\b", t2):
            return False  # commented-out LaTeX
        return True

    full_comment_lines = {li for li, _t, full in d.comments if full and _is_plan(_t) and li not in h06_lines}
    paras = [p for p in d.paras if len(words(p.text)) >= 25 and p.kind == "body"]
    with_plan = 0
    for p in paras:
        first = p.lines[0]
        prev = [first - 1, first - 2]
        if any(li in full_comment_lines for li in prev):
            with_plan += 1
            if len(r["examples"]) < a.max_ex:
                li = next(li for li in prev if li in full_comment_lines)
                r["examples"].append({"loc": d.loc(li), "tag": "comment_before_paragraph",
                                      "text": d.raw_lines[li].strip()[:160]})
    ratio = round(with_plan / len(paras), 4) if paras else 0.0
    sub = {"comment_preceded_paragraphs": with_plan, "data_needed": 0, "verify_tag": 0, "inline_arxiv_id": 0,
           "comment_todo": 0}
    for li, t, _full in d.comments:
        if re.search(r"DATA_NEEDED|DATA-NEEDED", t):
            sub["data_needed"] += 1
            a.add_example(r, li, t.strip()[:160], "data_needed")
        if re.search(r"\[VERIFY\]|\bVERIFY:", t):
            sub["verify_tag"] += 1
            a.add_example(r, li, t.strip()[:160], "verify_tag")
        if re.search(r"\bTODO\b|\bFIXME\b", t):
            sub["comment_todo"] += 1
            if a.source and len(r["examples"]) < a.max_ex * 2:
                r["examples"].append({"loc": d.loc(li), "tag": "comment_todo (--source)", "text": t.strip()[:160]})
    for p in d.paras:
        for m in re.finditer(r"\(\s*arXiv[:\s]+\d{4}\.\d{4,5}(?:v\d+)?\s*\)", p.text):
            sub["inline_arxiv_id"] += 1
            a.add_example(r, p.line_at(m.start()), snippet(p.text, m.start(), m.end()), "inline_arxiv_id")
    keys = _cite_keys(d) or [e["key"] for e in _bib_entries(d)]
    s2 = [k for k in keys if S2_KEY_RX.match(k)]
    r["sub"] = sub
    r["comment_para_ratio"] = ratio
    r["paragraphs_checked"] = len(paras)
    r["count"] = with_plan + sub["data_needed"] + sub["verify_tag"] + sub["inline_arxiv_id"]
    r["per_1k"] = a.per1k(r["count"])
    r["metric"] = "comment_para_ratio"
    r["value"] = ratio if len(paras) >= 8 else None  # too few paragraphs for a stable ratio
    if len(paras) < 8:
        r["notes"].append("Fewer than 8 paragraphs: the comment ratio is reported but not banded.")
    r["weak_subpatterns"] = ["comment_todo"]
    # info only (not counted)
    r["info"] = {
        "s2_style_bib_keys": {"count": len(s2), "fraction": round(len(s2) / len(keys), 4) if keys else 0.0,
                              "examples": s2[:6],
                              "note": "Semantic Scholar's BibTeX export produces these keys; humans use it too. Info only."},
        "possible_human_collaboration_traces_H06": {
            "comment_lines": len(h06_lines), "note_macros_in_body": h06_body, "examples": h06_ex,
            "note": "Co-author notes (initials + colon, TODO(name), \\todo, coloured note macros) are H06 "
                    "evidence of human involvement, not pipeline artifacts. Excluded from the P06 count."},
    }
    r["s2_key_fraction"] = r["info"]["s2_style_bib_keys"]["fraction"]
    if a.source:
        r["comment_lines"] = len(d.comments)


_CATALOGUE_ID_RX = re.compile(r"^[A-Z0-9]+(?:_[A-Z0-9]+)+$")


def check_P07(a: Analysis):
    r = a.new("P07", "Code identifiers in prose", "P07")
    # prefix and suffix of >= 2 chars, so math subscripts that leak into prose (a_1, x_i) are ignored
    snake = re.compile(r"(?<![\\/\w.])[A-Za-z][A-Za-z0-9]+_[A-Za-z0-9_]*[A-Za-z0-9]{2,}(?![\w/(])")
    special = re.compile(r"\brun_\d+\b|\bv\d+_final\b|\b\w+_final\b|\bconfig_\w+\b")
    sub = {"snake_case": 0, "run_or_final": 0}
    skipped = {"typeset_as_code": 0, "catalogue_id": 0}
    toks: Dict[str, int] = {}
    for p in a.doc.paras:
        spans = {}
        for m in snake.finditer(p.text):
            spans[(m.start(), m.end())] = ("snake_case", m)
        for m in special.finditer(p.text):
            hit = next(((s, e) for (s, e) in spans if s <= m.start() < e), None)
            if hit is None:
                spans[(m.start(), m.end())] = ("run_or_final", m)
            else:
                spans[hit] = ("run_or_final", spans[hit][1])
        for (s, e), (tag, m) in sorted(spans.items()):
            tok = m.group(0)
            if tag == "snake_case":
                # deliberate code typesetting (\texttt, \verb, `code`) and catalogue IDs (DMRG_MLP_001) are not leaks
                if tok in a.doc.texttt_tokens:
                    skipped["typeset_as_code"] += 1
                    continue
                if _CATALOGUE_ID_RX.match(tok) and re.search(r"\d", tok):
                    skipped["catalogue_id"] += 1
                    continue
            sub[tag] += 1
            r["count"] += 1
            toks[tok] = toks.get(tok, 0) + 1
            a.add_example(r, p.line_at(s), snippet(p.text, s, e), tag)
    r["sub"] = sub
    r["skipped"] = skipped
    r["per_1k"] = a.per1k(r["count"])
    r["distinct_identifiers"] = len(toks)
    r["identifiers"] = dict(sorted(toks.items(), key=lambda kv: -kv[1])[:20])
    r["notes"].append("Tokens typeset as code (\\texttt, \\verb, inline code) and catalogue IDs are skipped; "
                      "run_N / vN_final / config_* patterns are always counted.")


def _grim_ok(pct_s: str, n: int) -> bool:
    """Is there an integer k with round(100*k/n, d) == pct (d = decimals reported)?"""
    pct = float(pct_s)
    d = len(pct_s.split(".")[1]) if "." in pct_s else 0
    k0 = int(round(pct * n / 100.0))
    tol = 0.5 * 10 ** (-d) + 1e-9
    return any(0 <= k <= n and abs(100.0 * k / n - pct) <= tol for k in (k0 - 1, k0, k0 + 1))


def check_R17(a: Analysis):
    r = a.new("R17", "Numeric forensics (percentage/n consistency, zero or identical std)", "R09")
    r["info_only"] = True
    sub = {"pct_of_n_inconsistent": 0, "pct_with_n_eq_inconsistent": 0, "pm_zero": 0, "identical_std_column": 0}
    pct_of = re.compile(r"(\d{1,3}(?:\.\d{1,3})?)\s*(?:\\?%|percent)\s+(?:of\s+(?:the\s+|all\s+)?|out\s+of\s+)(\d{1,3}(?:,\d{3})*|\d+)\b")
    n_eq = re.compile(r"\b[nN]\s*=\s*(\d{1,6})\b")
    pct_any = re.compile(r"(?<![\d.])(\d{1,3}\.\d{1,3})\s*(?:\\?%|percent)")
    for p, off, s in a.sentences:
        found = set()
        for m in pct_of.finditer(s):
            n = int(m.group(2).replace(",", ""))
            if 2 <= n <= 1000000 and float(m.group(1)) <= 100 and not _grim_ok(m.group(1), n):
                sub["pct_of_n_inconsistent"] += 1
                r["count"] += 1
                found.add(m.start(1))
                a.add_example(r, p.line_at(off), snippet(s, m.start(), m.end(), 60), "pct_of_n_inconsistent")
        ns = [int(x) for x in n_eq.findall(s)]
        if len(set(ns)) == 1 and ns[0] >= 2:
            for m in pct_any.finditer(s):
                if m.start(1) in found or float(m.group(1)) > 100:
                    continue
                if not _grim_ok(m.group(1), ns[0]):
                    sub["pct_with_n_eq_inconsistent"] += 1
                    r["count"] += 1
                    a.add_example(r, p.line_at(off), snippet(s, m.start(), m.end(), 60), "pct_with_n_eq_inconsistent")
    pm_zero = re.compile(r"(?:\\pm|\u00b1|\+/-)\s*\$?\s*\{?\s*0\.0+(?![0-9]*[1-9])")
    for i, line in enumerate(a.doc.raw_lines):
        if a.doc.kind == "tex" and re.match(r"\s*%", line):
            continue
        for m in pm_zero.finditer(line):
            # 0.0 +/- 0.0 or 100.0 +/- 0.0 is a saturated metric, not a suspicious std
            if re.search(r"(?:^|[^\d.])(?:0|100|1)(?:\.0+)?\s*\$?\s*[_^]?\s*\{?\s*$", line[: m.start()]):
                continue
            sub["pm_zero"] += 1
            r["count"] += 1
            a.add_example(r, i, snippet(line, m.start(), m.end(), 50), "pm_zero")
    if a.doc.kind == "tex":
        raw = _strip_all_comments(a.doc.raw)
        for tm in re.finditer(r"\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}", raw, re.S):
            rows = [row for row in re.split(r"\\\\", tm.group(0)) if "\\pm" in row]
            if len(rows) < 4:
                continue
            per_row = [re.findall(r"\\pm\s*\{?\s*([0-9]*\.?[0-9]+)", row) for row in rows]
            ncol = min(len(x) for x in per_row)
            for c in range(ncol):
                vals = {x[c] for x in per_row}
                if len(vals) == 1 and float(next(iter(vals))) != 0.0:
                    sub["identical_std_column"] += 1
                    r["count"] += 1
                    ln = raw.count("\n", 0, tm.start())
                    a.add_example(r, ln, f"{len(rows)} rows share std = {next(iter(vals))} in column {c + 1}",
                                  "identical_std_column")
    r["sub"] = sub
    r["per_1k"] = a.per1k(r["count"])
    r["notes"].append("Report-only, uncalibrated. A percentage that no integer count out of n can produce "
                      "(GRIM-style), '+/- 0.00', or the same std in every row deserves a recomputation.")


P13_PATTERNS = [
    ("claude_md", r"(?:^|/)CLAUDE\.md$"), ("agents_md", r"(?:^|/)AGENTS\.md$"), ("dot_claude", r"(?:^|/)\.claude/"),
    ("review_round", r"(?:^|/)review_round[^/]*$"), ("auto_review", r"(?:^|/)AUTO_REVIEW[^/]*$"),
    ("idea_report", r"(?:^|/)IDEA_REPORT[^/]*$"), ("narrative_report", r"(?:^|/)NARRATIVE_REPORT[^/]*$"),
]


def check_P13(a: Analysis):
    r = a.new("P13", "Pipeline files in the submission tree", "P13")
    r["info_only"] = True
    d = a.doc
    if not d.tree:
        r["available"] = False
        r["notes"].append("Only applies to a directory input.")
        return
    for sub, rx in P13_PATTERNS:
        r["sub"][sub] = 0
        for f in d.tree:
            if re.search(rx, f, I if sub == "dot_claude" else 0):
                r["sub"][sub] += 1
                r["count"] += 1
                if len(r["examples"]) < a.max_ex * 2:
                    r["examples"].append({"loc": f, "tag": sub, "text": f})
    r["sub"]["results_tsv_keep_discard"] = 0
    for f in d.tree:
        if os.path.basename(f) == "results.tsv":
            try:
                head = _read(os.path.join(d.path, f))[:20000]
            except OSError:
                continue
            if re.search(r"\b(?:keep|discard)\b", head):
                r["sub"]["results_tsv_keep_discard"] += 1
                r["count"] += 1
                r["examples"].append({"loc": f, "tag": "results_tsv_keep_discard", "text": f})
    r["per_1k"] = a.per1k(r["count"])
    r["notes"].append("Info only: files left by autoresearch/agent pipelines (CLAUDE.md, review_round*, ...).")


CHECKS = [check_L01, check_L02, check_L03, check_L04, check_L05, check_L06, check_L07, check_L08,
          check_L10, check_L14, check_L15, check_L16,
          check_S01, check_S02, check_S03, check_S04, check_S05, check_S06, check_S13,
          check_R01, check_R05, check_R16, check_R17,
          check_P01, check_P02_meta, check_P02_todo, check_P03, check_P05, check_P06, check_P07, check_P13]
CHECK_IDS = ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L10", "L14", "L15", "L16",
             "S01", "S02", "S03", "S04", "S05", "S06", "S13", "R01", "R05", "R16", "R17",
             "P01", "P02-meta", "P02-todo", "P03", "P05", "P06", "P07", "P13"]
INFO_ONLY_IDS = {"R17", "P13"}  # report-only: never banded, not calibrated, not in the L-cluster

TOMBSTONE_IDS = {"P01", "P02-meta", "P03", "P05"}  # "iron-clad" if verified (EVIDENCE strength mark)


# ============================================================================
# Banding and reporting
# ============================================================================


def metric_value(r: dict) -> Optional[float]:
    if not r.get("available", True):
        return None
    if r.get("metric"):
        return r.get("value")
    return r.get("per_1k")


def band(r: dict) -> str:
    if r.get("info_only"):
        return "info"
    v = metric_value(r)
    if v is None:
        return "n/a"
    c = CALIBRATION.get(r["id"])
    if not c:
        return "uncalibrated"
    if c.get("direction", "high") == "low":
        if v >= c["p10"]:
            return "typical"
        return "elevated" if v >= c["p01"] else "high"
    if v <= c["p90"] or (r.get("count", 0) == 0):
        return "typical"
    return "elevated" if v <= c["p99"] else "high"


def analyze(path: str, max_examples: int = 5, source: bool = False, exclude_regex: Optional[str] = None,
            default_excludes: bool = True) -> dict:
    doc = load(path)
    excluded = exclude_non_author_sections(doc, exclude_regex, default_excludes)
    a = Analysis(doc, max_examples=max_examples, source=source)
    for fn in CHECKS:
        fn(a)
    out = {
        "tool": "slop_lint", "version": VERSION, "path": path, "kind": doc.kind,
        "files": [os.path.relpath(f, path) if os.path.isdir(path) else os.path.basename(f) for f in doc.files][:50],
        "title": doc.title, "prose_words": a.n_words, "sentences": len(a.sentences),
        "paragraphs": len(doc.paras), "sections": [t for _, lvl, t in doc.headings if lvl <= 1][:40],
        "calibration": CALIBRATION_META, "checks": {},
        "excluded_sections": excluded,
    }
    for cid, r in a.results.items():
        r["band"] = band(r)
        r["weak_check"] = cid in WEAK_CHECKS
        r["calibration_status"] = calib_status(cid)
        c = CALIBRATION.get(cid)
        if c:
            r["human_baseline"] = {k: c[k] for k in ("p50", "p90", "p99", "auc", "metric", "direction") if k in c}
        out["checks"][cid] = r
    lc = CALIBRATION_META.get("l_cluster")
    if lc:
        flagged = [c for c in lc["checks"] if out["checks"].get(c, {}).get("band") in ("elevated", "high")]
        avail = [c for c in lc["checks"] if out["checks"].get(c, {}).get("band") not in (None, "n/a")]
        out["l_cluster"] = {"flagged": flagged, "n_flagged": len(flagged), "n_available": len(avail),
                            "human_share_ge": lc["human_share_ge"].get(str(len(flagged)), lc["human_share_ge"].get(len(flagged))),
                            "ai_share_ge": lc["ai_share_ge"].get(str(len(flagged)), lc["ai_share_ge"].get(len(flagged)))}
    if a.n_words < 1500:
        out["warning"] = (f"Only {a.n_words} prose words: densities are unstable and bands were calibrated "
                          f"on full papers.")
    return out


DISCLAIMER = """> **These are CANDIDATES, not verdicts.** Every hit must be read in context by a person.
> * **L-layer hits can at most suggest that the writing was not polished by a human. They never imply that the
>   research is slop** (evidence catalog, iron rule 1). Research-layer judgements need R/P evidence read in context.
> * **Absence of hits means nothing.** 2026 pipelines scrub these surface traces; a clean report is not a pass.
> * Bands compare this paper with a small corpus of pre-ChatGPT arXiv papers (calibration report: `tools/calibration/` in the
>   project repository). With n=59, "p99" is essentially the corpus maximum. Non-native writers and heavily
>   copy-edited papers also trip L-layer checks (detectors misjudge ~61% of non-native essays, [Liang23]).
> * Look for H-layer (human presence) evidence before concluding anything."""


def _fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.3g}" if abs(v) < 100 else f"{v:.0f}"
    return str(v)


def to_markdown(res: dict, show_source: bool = False) -> str:
    L = []
    L.append(f"# slop_lint report: `{res['path']}`\n")
    L.append(DISCLAIMER + "\n")
    meta = res.get("calibration") or {}
    L.append(f"- Input kind: **{res['kind']}**, prose words: **{res['prose_words']}**, sentences: "
             f"{res['sentences']}, paragraphs: {res['paragraphs']}")
    if res.get("title"):
        L.append(f"- Title: {res['title']}")
    if meta:
        L.append(f"- Calibration: {meta.get('date', '?')}, human baseline n={meta.get('n_human', '?')}, "
                 f"AI-heavy set n={meta.get('n_ai', '?')} (bands: typical <= human p90 < elevated <= p99 < high)")
    if res.get("excluded_sections"):
        L.append("- **Excluded as non-author text** (prompt dumps, checklists; use --no-default-excludes to keep): "
                 + "; ".join(res["excluded_sections"][:10]))
    if res.get("warning"):
        L.append(f"- **Warning:** {res['warning']}")
    L.append("")
    lc = res.get("l_cluster")
    if lc:
        line = (f"- **L-layer cluster:** {lc['n_flagged']} of {lc['n_available']} L-cluster checks are "
                f"above the human p90 ({', '.join(lc['flagged']) or 'none'}).")
        if lc["n_flagged"] and lc.get("human_share_ge") is not None:
            line += (f" In calibration, {lc['human_share_ge']:.0%} of human papers (leave-one-out) and "
                     f"{lc['ai_share_ge']:.0%} of AI-heavy papers reached at least this many.")
        line += " Writing-polish signal only; 2026 Claude-based pipeline papers scored 0-1 here."
        L.append(line + "\n")
    L.append("## Summary\n")
    L.append("| ID | Check | Count | per 1k words (or metric) | Band | Human p50 / p90 / p99 | AUC | Discrimination; notes |")
    L.append("|---|---|---:|---:|---|---|---:|---|")
    for cid, r in res["checks"].items():
        hb = r.get("human_baseline", {})
        val = metric_value(r)
        metric_lbl = f" ({r['metric']})" if r.get("metric") else ""
        note = []
        note.append(r.get("calibration_status", ""))
        if r.get("info_only"):
            note.append("report-only")
        if cid in TOMBSTONE_IDS and r.get("count"):
            note.append("verify: iron-clad if confirmed")
        if (r.get("rule") or {}).get("fired"):
            note.append("density rule fired")
        if not r.get("available", True):
            note.append("n/a for this input")
        hbs = f"{_fmt(hb.get('p50'))} / {_fmt(hb.get('p90'))} / {_fmt(hb.get('p99'))}" if hb else "-"
        L.append(f"| {cid} | {r['title']} | {r['count'] if r.get('available', True) else '-'} | "
                 f"{_fmt(val)}{metric_lbl} | {r['band']} | {hbs} | {_fmt(hb.get('auc'))} | {'; '.join(note)} |")
    L.append("")
    for layer in "LSRP":
        items = [r for cid, r in res["checks"].items() if cid.startswith(layer)]
        L.append(f"## {LAYER_NAMES[layer]}\n")
        for r in items:
            L.append(f"### {r['id']} {r['title']} - band: {r['band']}\n")
            if not r.get("available", True):
                L.append("_Not available for this input._ " + " ".join(r.get("notes", [])) + "\n")
                continue
            facts = [f"count={r['count']}"]
            if r.get("per_1k") is not None:
                facts.append(f"per 1k={_fmt(r['per_1k'])}")
            for k in ("sentence_len_mean", "sentence_len_sd", "sentence_len_cv", "paragraphs_per_1k",
                      "paragraph_len_cv", "comment_para_ratio", "s2_key_fraction", "share_of_sentences",
                      "paragraph_cmd_per_1k", "list_envs_per_1k", "entries_checked", "sections_with_caveats"):
                if k in r:
                    facts.append(f"{k}={_fmt(r[k])}")
            L.append("- " + ", ".join(facts))
            if r.get("sub"):
                weak = set(r.get("weak_subpatterns", []))
                if any(r["sub"].values()):
                    L.append("- sub-patterns: " + ", ".join(
                        f"{k}={v}{' (weak, not counted)' if k in weak else ''}" for k, v in r["sub"].items() if v))
            if r.get("per_word"):
                L.append("- per word: " + ", ".join(f"{k}={v}" for k, v in list(r["per_word"].items())[:15]))
            if r.get("by_section"):
                L.append("- by section: " + ", ".join(f"{k}={v}" for k, v in r["by_section"].items()))
            if r.get("rule"):
                L.append(f"- rule: {json.dumps(r['rule'], ensure_ascii=False)}")
            if r.get("identifiers"):
                L.append("- identifiers: " + ", ".join(f"`{k}`x{v}" for k, v in list(r["identifiers"].items())[:10]))
            if r["id"] == "S06" and r.get("acronyms"):
                low = [x for x in r["acronyms"] if x["uses_after_def"] <= 2]
                if low:
                    L.append("- low-use acronyms: " + ", ".join(f"{x['acronym']}({x['uses_after_def']})" for x in low[:15]))
            if r.get("skipped") and any(r["skipped"].values()):
                L.append("- skipped (not counted): " + ", ".join(f"{k}={v}" for k, v in r["skipped"].items() if v))
            for k, v in (r.get("info") or {}).items():
                cnt = v.get("count", v.get("comment_lines", 0) + v.get("note_macros_in_body", 0))
                L.append(f"- info, {k.replace('_', ' ')}: {cnt}. {v.get('note', '')}")
                for e in (v.get("examples") or [])[:3]:
                    if isinstance(e, dict):
                        L.append(f"  - `{e['loc']}` [{e['tag']}]: {e['text']}")
                    else:
                        L.append(f"  - {e}")
            for n in r.get("notes", []):
                L.append(f"- note: {n}")
            if r["examples"]:
                L.append("")
                for e in r["examples"]:
                    tag = f" [{e['tag']}]" if e.get("tag") else ""
                    txt = e["text"].replace("|", "\\|")
                    L.append(f"  - `{e['loc']}`{tag}: {txt}")
            L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic sloppy-AI surface-trace screen (candidates only).")
    ap.add_argument("paths", nargs="+", help=".tex/.md/.txt file or directory (one document per path)")
    ap.add_argument("--format", choices=("md", "json"), default="md")
    ap.add_argument("--source", action="store_true",
                    help="also list TODO/FIXME source comments and comment totals under P06 "
                         "(P06 itself always runs when the source has comments)")
    ap.add_argument("--max-examples", type=int, default=5)
    ap.add_argument("-o", "--output", help="write report to this file instead of stdout")
    ap.add_argument("--exclude-regex", help="also skip sections whose heading matches this regex "
                                            "(e.g. 'rebuttal|dataset card')")
    ap.add_argument("--no-default-excludes", action="store_true",
                    help="do not skip prompt-dump / checklist sections (skipped by default)")
    args = ap.parse_args(argv)
    results = []
    for p in args.paths:
        if not os.path.exists(p):
            print(f"slop_lint: no such path: {p}", file=sys.stderr)
            continue
        results.append(analyze(p, args.max_examples, args.source, args.exclude_regex, not args.no_default_excludes))
    if args.format == "json":
        text = json.dumps(results if len(results) != 1 else results[0], indent=1, ensure_ascii=False)
    else:
        text = "\n\n---\n\n".join(to_markdown(r, args.source) for r in results)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
