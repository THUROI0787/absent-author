#!/usr/bin/env python3
"""Build site/data/*.json from EVIDENCE.md (English), EVIDENCE_CN.md (Chinese), docs/SOURCES.md and
tools/calibration/calibration_results.json, and copy assets/*.svg into site/assets/.

    python tools/build_site_data.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
ROW = re.compile(r"^\|\s*([LSRPH]\d{2})\s*\|(.*)\|\s*$", re.M)
KEY = re.compile(r"`\[([A-Za-z0-9\-]+)\]`")


def cells(line_rest):
    # split on | not inside backticks
    out, cur, tick = [], "", False
    for ch in line_rest:
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return out


def md_inline(s):
    """Tiny markdown → HTML for table cells (bold, code, links)."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def strength_class(s):
    s0 = s.strip()
    if s0.startswith("☠"):
        return "skull"
    if s0.startswith("⚑"):
        return "flag"
    if s0.startswith("★★★"):
        return "3"
    if s0.startswith("★★"):
        return "2"
    if s0.startswith("★"):
        return "1"
    if s0.startswith("i"):
        return "i"
    return "?"


def parse(path):
    text = path.read_text(encoding="utf-8")
    items = {}
    for m in ROW.finditer(text):
        iid, rest = m.group(1), cells(m.group(2))
        layer = iid[0]
        if layer == "L":
            name, form, strength, fp, src = (rest + [""] * 5)[:5]
            axis = "W"
        elif layer == "H":
            name, typ, effect = (rest + [""] * 3)[:3]
            items[iid] = dict(id=iid, layer="H", name=md_inline(name), form="", strength="", fp="",
                              axis="H", typ=md_inline(typ), effect=md_inline(effect), src=[])
            continue
        else:
            name, form, strength, axis, fp, src = (rest + [""] * 6)[:6]
        items[iid] = dict(id=iid, layer=layer, name=md_inline(name), form=md_inline(form),
                          strength=md_inline(strength), sclass=strength_class(strength), axis=axis.strip(),
                          fp=md_inline(fp), src=KEY.findall(src))
    return items


def sources():
    text = (ROOT / "docs" / "SOURCES.md").read_text(encoding="utf-8")
    out = {}
    last_url = None
    for line in text.splitlines():
        m = re.match(r"^\|\s*`\[([A-Za-z0-9\-]+)\]`\s*\|(.*)$", line)
        if not m:
            continue
        url = re.search(r"https?://[^\s)|，；]+", m.group(2))
        label = re.sub(r"\s+", " ", m.group(2).split("|")[0]).strip()
        u = url.group(0).rstrip(".,") if url else None
        if u is None and label.startswith(("同上", "Same as above")):
            u = last_url
        if u:
            last_url = u
        out[m.group(1)] = {"url": u, "label": label[:160]}
    return out


def main():
    en, cn = parse(ROOT / "EVIDENCE.md"), parse(ROOT / "EVIDENCE_CN.md")
    assert en.keys() == cn.keys(), set(en) ^ set(cn)
    order = sorted(en, key=lambda k: ("LSRPH".index(k[0]), k))
    data = []
    for k in order:
        e, c = en[k], cn[k]
        data.append({"id": k, "layer": e["layer"], "axis": e["axis"], "sclass": e.get("sclass", ""),
                     "src": e["src"],
                     "en": {f: e.get(f, "") for f in ("name", "form", "strength", "fp", "typ", "effect")},
                     "cn": {f: c.get(f, "") for f in ("name", "form", "strength", "fp", "typ", "effect")}})
    (SITE / "data").mkdir(parents=True, exist_ok=True)
    (SITE / "data" / "evidence.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    (SITE / "data" / "sources.json").write_text(json.dumps(sources(), ensure_ascii=False), encoding="utf-8")
    cal = json.loads((ROOT / "tools" / "calibration" / "calibration_results.json").read_text())
    slim = {"meta": {k: cal["meta"][k] for k in ("date", "n_human", "n_ai")},
            "l_cluster": cal["meta"]["l_cluster"],
            "auc": {k: v["auc"] for k, v in cal["stats"].items() if "." not in k and "auc" in v}}
    (SITE / "data" / "calibration.json").write_text(json.dumps(slim), encoding="utf-8")
    (SITE / "assets").mkdir(exist_ok=True)
    for f in list((ROOT / "assets").glob("*.svg")) + list((ROOT / "assets").glob("*.png")):
        shutil.copy2(f, SITE / "assets" / f.name)
    print(f"site data: {len(data)} evidence items, {len(sources())} sources")


if __name__ == "__main__":
    main()
