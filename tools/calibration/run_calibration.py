#!/usr/bin/env python3
"""Calibrate slop_lint.py bands on a human (pre-ChatGPT arXiv) corpus vs an AI-heavy corpus.

The corpus itself is NOT stored in the project (only IDs and provenance). To reproduce:
  1. download the human set listed in human_corpus.json (arXiv e-print, version v1) into
     <scratch>/lint/corpus/human/<arXiv id>/ (one directory of .tex/.bib/.bbl per paper);
  2. obtain the AI-heavy set listed in ai_set_provenance.json (paths relative to <scratch>);
  3. python run_calibration.py --scratch <scratch> [--write-tool]

Outputs (next to this script): calibration_results.json, calibration_tables.md, and, with
--write-tool, the CALIBRATION block inside ../slop_lint.py.
Standard library only.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import slop_lint as SL  # noqa: E402

MIN_WORDS = 1500
CAL_DATE = "2026-10-05"


def pct(vals, q):
    return SL._pct(list(vals), q)


def auc(pos, neg, direction="high"):
    """P(score_pos > score_neg) + 0.5 P(tie) (Mann-Whitney). direction='low' flips the sign."""
    if not pos or not neg:
        return None
    s = 0.0
    for p in pos:
        for n in neg:
            if direction == "low":
                p_, n_ = -p, -n
            else:
                p_, n_ = p, n
            s += 1.0 if p_ > n_ else (0.5 if p_ == n_ else 0.0)
    return s / (len(pos) * len(neg))


def features(res):
    """Flatten an analyze() result into {feature_name: value} (None = not available)."""
    f = {}
    n = res["prose_words"] or 1
    for cid, r in res["checks"].items():
        avail = r.get("available", True)
        f[cid] = SL.metric_value(r) if avail else None
        if not avail:
            continue
        for k, v in (r.get("sub") or {}).items():
            if isinstance(v, (int, float)):
                f[f"{cid}.{k}"] = 1000.0 * v / n
        for k in ("paragraphs_per_1k", "sentence_len_mean", "sentence_len_sd", "paragraph_len_cv",
                  "s2_key_fraction", "paragraph_cmd_per_1k", "list_envs_per_1k", "share_of_sentences",
                  "sections_with_caveats"):
            if k in r:
                f[f"{cid}.{k}"] = r[k]
        if cid == "L03":
            f["L03.max_repeat"] = (r.get("max_repeat") or {}).get("count", 0)
            for w, c in (r.get("per_word") or {}).items():
                f[f"L03.word.{w}"] = 1000.0 * c / n
        if cid in SL.INFO_ONLY_IDS:
            continue
        if cid in ("S01", "S02") and r.get("rule"):
            f[f"{cid}.rule_fired"] = 1.0 if r["rule"].get("fired") else 0.0
    return f


def collect(scratch):
    docs = []
    hman = json.load(open(os.path.join(HERE, "human_corpus.json")))
    for e in hman:
        p = os.path.join(scratch, "lint", "corpus", "human", e["id"])
        docs.append(("human", e["id"], p, e))
    for e in json.load(open(os.path.join(HERE, "ai_set_provenance.json"))):
        rel = e["path"].split(" -> ")[-1]
        docs.append(("ai", e["id"], os.path.join(scratch, rel), e))
    out = []
    for setname, did, path, meta in docs:
        if not os.path.exists(path):
            print(f"missing: {path}", file=sys.stderr)
            continue
        res = SL.analyze(path, max_examples=0)
        if res["prose_words"] < MIN_WORDS:
            print(f"skip (only {res['prose_words']} prose words): {did}", file=sys.stderr)
            continue
        out.append({"set": setname, "id": did, "kind": res["kind"], "words": res["prose_words"],
                    "features": features(res), "bands": {c: r["band"] for c, r in res["checks"].items()}})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, help="scratch root containing lint/corpus and repos/")
    ap.add_argument("--write-tool", action="store_true")
    args = ap.parse_args()
    rows = collect(args.scratch)
    H = [r for r in rows if r["set"] == "human"]
    A = [r for r in rows if r["set"] == "ai"]
    A_tex = [r for r in A if r["kind"] == "tex"]
    feats = sorted({k for r in rows for k in r["features"]})
    # zero-fill: a sub-pattern / word that never fired in an available check is a 0, not missing
    for r in rows:
        for k in feats:
            if k not in r["features"] and "." in k and r["features"].get(k.split(".")[0]) is not None:
                r["features"][k] = 0.0
    stats = {}
    for k in feats:
        hv = [r["features"][k] for r in H if r["features"].get(k) is not None]
        av = [r["features"][k] for r in A if r["features"].get(k) is not None]
        atv = [r["features"][k] for r in A_tex if r["features"].get(k) is not None]
        if k == "L15" or k.startswith("L15."):
            # PDF-extracted text breaks sentence segmentation; rhythm is compared on LaTeX only
            av = atv
        if not hv:
            continue
        direction = "low" if k == "L15" else "high"
        st = {
            "n_human": len(hv), "n_ai": len(av), "direction": direction,
            "p01": pct(hv, 0.01), "p10": pct(hv, 0.10), "p50": pct(hv, 0.50), "p90": pct(hv, 0.90),
            "p95": pct(hv, 0.95), "p99": pct(hv, 0.99), "max": max(hv),
            "ai_median": pct(av, 0.5) if av else None, "ai_p10": pct(av, 0.1) if av else None,
            "ai_p90": pct(av, 0.9) if av else None,
            "human_nonzero": sum(1 for v in hv if v) / len(hv),
            "ai_nonzero": (sum(1 for v in av if v) / len(av)) if av else None,
            "auc": auc(av, hv, direction), "auc_tex_only": auc(atv, hv, direction),
        }
        if av:
            thr = st["p99"] if direction == "high" else st["p01"]
            st["ai_above_p99"] = sum(1 for v in av if (v > thr if direction == "high" else v < thr)) / len(av)
            thr90 = st["p90"] if direction == "high" else st["p10"]
            st["ai_above_p90"] = sum(1 for v in av if (v > thr90 if direction == "high" else v < thr90)) / len(av)
        stats[k] = st

    main_ids = [c for c in SL.CHECK_IDS if c not in SL.INFO_ONLY_IDS]
    weak, rare, specific = [], [], []
    for c in main_ids:
        st = stats.get(c)
        if not st:
            continue
        if st["human_nonzero"] < 0.10 and (st["ai_nonzero"] or 0) < 0.10:
            rare.append(c)
        elif st["human_nonzero"] <= 0.05 and (st["ai_nonzero"] or 0) >= 0.20:
            specific.append(c)  # low recall, but almost never fires on the human baseline
        elif st["auc"] is None or st["auc"] < 0.65:
            weak.append(c)
    # Composite: how many "strong" L checks exceed the human p90 (p10 for L15). Human values are
    # leave-one-out (each human paper is compared with the other human papers) to avoid self-reference.
    strong = [c for c in main_ids if c.startswith("L") and c in stats and c not in weak + rare + specific
              and (stats[c]["auc"] or 0) >= 0.75]

    def n_flags(doc, ref):
        n = 0
        for c in strong:
            v = doc["features"].get(c)
            if v is None:
                continue
            hv = [x["features"][c] for x in ref if x["features"].get(c) is not None]
            n += (v < pct(hv, 0.10)) if c == "L15" else (v > pct(hv, 0.90))
        return int(n)

    hf = [n_flags(x, [y for y in H if y is not x]) for x in H]
    af = [n_flags(x, H) for x in A]
    l_cluster = {"checks": strong, "auc": auc(af, hf),
                 "human_share_ge": {k: sum(1 for v in hf if v >= k) / len(hf) for k in range(1, len(strong) + 1)},
                 "ai_share_ge": {k: sum(1 for v in af if v >= k) / len(af) for k in range(1, len(strong) + 1)},
                 "ai_flags": {x["id"]: v for x, v in zip(A, af)}}
    meta = {"date": CAL_DATE, "l_cluster": l_cluster, "n_human": len(H), "n_ai": len(A), "n_ai_tex": len(A_tex),
            "human_corpus": "arXiv v1 e-prints 2018-2022, cs.LG/cs.CL/cs.CV/stat.ML (see calibration/human_corpus.json)",
            "ai_corpus": "AI Scientist v1/v2, Zochi, Agents4Science, autonomous-agent and ARIS papers "
                         "(see calibration/ai_set_provenance.json)",
            "weak_checks": weak, "rare_checks": rare, "specific_checks": specific, "min_prose_words": MIN_WORDS}
    def _r(o):
        if isinstance(o, float):
            return round(o, 4)
        if isinstance(o, dict):
            return {k: _r(v) for k, v in o.items()}
        if isinstance(o, list):
            return [_r(v) for v in o]
        return o
    with open(os.path.join(HERE, "calibration_results.json"), "w") as fh:
        json.dump(_r({"meta": meta, "stats": stats, "docs": rows}), fh, separators=(",", ":"))

    def f(v, nd=3):
        if v is None:
            return "-"
        return f"{v:.{nd}f}" if isinstance(v, float) else str(v)

    T = []
    T.append(f"Human n={len(H)} (all LaTeX); AI-heavy n={len(A)} ({len(A_tex)} LaTeX, {len(A) - len(A_tex)} PDF text). "
             f"Docs with < {MIN_WORDS} prose words dropped.\n")
    T.append("### Main checks\n")
    T.append("| ID | metric | human p50 | p90 | p95 | p99 | AI median | AUC all | AUC LaTeX-only | human >0 | AI >0 | AI > human p99 | status |")
    T.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for c in main_ids:
        st = stats.get(c)
        if not st:
            continue
        metric = {"L15": "sentence-length CV (low = uniform)", "P06": "comment-preceded paragraph ratio",
                  "L10": "list items per 1k words"}.get(c, "per 1k words")
        status = ("rare" if c in rare else "specific (low recall)" if c in specific else "weak" if c in weak
                  else ("strong" if (st["auc"] or 0) >= 0.8 else "moderate"))
        T.append(f"| {c} | {metric} | {f(st['p50'])} | {f(st['p90'])} | {f(st['p95'])} | {f(st['p99'])} | "
                 f"{f(st['ai_median'])} | {f(st['auc'], 2)} | {f(st['auc_tex_only'], 2)} | {st['human_nonzero']:.0%} | "
                 f"{(st['ai_nonzero'] or 0):.0%} | {(st.get('ai_above_p99') or 0):.0%} | {status} |")
    T.append("\n### L-layer cluster (number of strong L checks above the human p90; human values leave-one-out)\n")
    T.append(f"Checks: {', '.join(strong)}; AUC of the count = {l_cluster['auc']:.2f}\n")
    T.append("| flags >= k | " + " | ".join(str(k) for k in range(1, len(strong) + 1)) + " |")
    T.append("|---|" + "---:|" * len(strong))
    T.append("| human share | " + " | ".join(f"{l_cluster['human_share_ge'][k]:.0%}" for k in range(1, len(strong) + 1)) + " |")
    T.append("| AI-heavy share | " + " | ".join(f"{l_cluster['ai_share_ge'][k]:.0%}" for k in range(1, len(strong) + 1)) + " |")
    T.append("\nPer AI paper: " + ", ".join(f"{k}={v}" for k, v in l_cluster["ai_flags"].items()))
    T.append("\n### Sub-patterns and auxiliary features (per 1k words unless named otherwise)\n")
    T.append("| feature | human p50 | p90 | p99 | AI median | AUC all | human >0 | AI >0 |")
    T.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for k in feats:
        if k in main_ids or k not in stats:
            continue
        st = stats[k]
        if st["human_nonzero"] == 0 and not st["ai_nonzero"]:
            continue
        T.append(f"| {k} | {f(st['p50'])} | {f(st['p90'])} | {f(st['p99'])} | {f(st['ai_median'])} | "
                 f"{f(st['auc'], 2)} | {st['human_nonzero']:.0%} | {(st['ai_nonzero'] or 0):.0%} |")
    T.append("\n### Per-document values of key checks (AI-heavy set)\n")
    keys = ["L01", "L02", "L03", "L04", "L05", "L08", "L15", "S01", "S06", "P03", "P06", "P07"]
    T.append("| doc | kind | words | " + " | ".join(keys) + " |")
    T.append("|---|---|---:|" + "---:|" * len(keys))
    for r in A:
        T.append(f"| {r['id']} | {r['kind']} | {r['words']} | " +
                 " | ".join(f(r['features'].get(k), 2) for k in keys) + " |")
    open(os.path.join(HERE, "calibration_tables.md"), "w").write("\n".join(T) + "\n")
    print("\n".join(T[:40]))

    if args.write_tool:
        calib = {}
        for c in main_ids:
            st = stats.get(c)
            if not st:
                continue
            calib[c] = {k: (round(st[k], 4) if isinstance(st[k], float) else st[k])
                        for k in ("p01", "p10", "p50", "p90", "p95", "p99", "auc", "ai_median", "direction",
                                  "n_human")}
            calib[c]["metric"] = {"L15": "sentence_len_cv", "P06": "comment_para_ratio",
                                  "L10": "list_items_per_1k"}.get(c, "per_1k")
        block = ("# BEGIN CALIBRATION\n"
                 f"# Calibrated {CAL_DATE} by tools/calibration/run_calibration.py on {len(H)} human arXiv papers\n"
                 f"# (v1 e-prints 2018-2022) and {len(A)} AI-heavy papers. Bands: typical <= human p90 < elevated\n"
                 "# <= human p99 < high (L15 uses the low tail: p10 / p01). With n~50, p99 ~ corpus max.\n"
                 f"CALIBRATION_META = {json.dumps(meta, indent=1)}\n"
                 f"CALIBRATION = {json.dumps(calib, indent=1)}\n"
                 "# END CALIBRATION")
        block = block.replace(": null", ": None").replace(": true", ": True").replace(": false", ": False")
        tool = os.path.join(os.path.dirname(HERE), "slop_lint.py")
        src = open(tool).read()
        src = re.sub(r"# BEGIN CALIBRATION.*?# END CALIBRATION", lambda m: block, src, flags=re.S)
        open(tool, "w").write(src)
        print(f"wrote calibration block into {tool}")


if __name__ == "__main__":
    main()
