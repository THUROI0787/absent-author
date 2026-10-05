#!/usr/bin/env python3
"""Sync the evidence list (EVIDENCE.md in English, EVIDENCE_CN.md in Chinese), the English index
(docs/evidence-index-en.md) and tools/slop_lint.py into both skills, and check that:
  * EVIDENCE.md and EVIDENCE_CN.md contain exactly the same IDs,
  * every evidence ID has a polish action, a screen action and a line in the English index.

Relative links in EVIDENCE.md (docs/..., tools/...) do not resolve inside a skill folder, so the
synced evidence-catalog.md rewrites them as plain text marked "in the project repository".

Usage:  python tools/sync_evidence.py          # sync + check
        python tools/sync_evidence.py --check  # check only, non-zero exit on problems
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "EVIDENCE.md"
EVIDENCE_CN = ROOT / "EVIDENCE_CN.md"
LINT = ROOT / "tools" / "slop_lint.py"
INDEX_EN = ROOT / "docs" / "evidence-index-en.md"
SKILLS = {
    "paper-author-pass": ROOT / "skills" / "paper-author-pass" / "references" / "polish-actions.md",
    "paper-slop-screen": ROOT / "skills" / "paper-slop-screen" / "references" / "screen-actions.md",
}
HEADER = (
    "<!-- AUTO-SYNCED from {src} by tools/sync_evidence.py. Do not edit here; "
    "edit {src} at the project root and re-run the sync. -->\n\n"
)
ID_RE = re.compile(r"^\|\s*([LSRPH]\d{2})\s*\|", re.M)
RANGE_RE = re.compile(r"\b([LSRPH])(\d{2})\s*[–-]\s*\1?(\d{2})\b")
LINK_RE = re.compile(r"\[([^\]]+)\]\((?!#|https?:|mailto:)([^)]+)\)")
INDEX_HEADER = (
    "<!-- AUTO-SYNCED from docs/evidence-index-en.md by tools/sync_evidence.py. Do not edit here; "
    "edit the master in the project repository and re-run the sync. -->\n\n"
)


def delink(text):
    """Rewrite repository-relative markdown links as plain text (they dangle inside a skill)."""
    def sub(m):
        label, target = m.group(1), m.group(2)
        if label.strip("`") == target:
            return f"`{target}` (in the project repository)"
        return f"{label} (in the project repository: {target})"
    return LINK_RE.sub(sub, text)


def ids_in(text):
    found = set(ID_RE.findall(text))
    for prefix, a, b in RANGE_RE.findall(text):
        for i in range(int(a), int(b) + 1):
            found.add(f"{prefix}{i:02d}")
    return found


def main():
    check_only = "--check" in sys.argv
    ev_text = EVIDENCE.read_text(encoding="utf-8")
    ev_ids = set(ID_RE.findall(ev_text))
    problems = []
    cn_text = EVIDENCE_CN.read_text(encoding="utf-8") if EVIDENCE_CN.exists() else None
    if cn_text is None:
        problems.append("EVIDENCE_CN.md is missing")
    else:
        cn_ids = set(ID_RE.findall(cn_text))
        if ev_ids != cn_ids:
            problems.append("EVIDENCE.md vs EVIDENCE_CN.md ID mismatch: only EN "
                            f"{sorted(ev_ids - cn_ids)}, only CN {sorted(cn_ids - ev_ids)}")
    if INDEX_EN.exists():
        idx_text = INDEX_EN.read_text(encoding="utf-8")
        idx_ids = set(ID_RE.findall(idx_text))
        if ev_ids - idx_ids:
            problems.append(f"docs/evidence-index-en.md: no line for {', '.join(sorted(ev_ids - idx_ids))}")
        if idx_ids - ev_ids:
            problems.append(f"docs/evidence-index-en.md: unknown IDs {', '.join(sorted(idx_ids - ev_ids))}")
    else:
        idx_text = None
        problems.append("docs/evidence-index-en.md is missing")
    for skill, actions in SKILLS.items():
        skill_dir = actions.parent.parent
        if not check_only:
            (skill_dir / "references").mkdir(parents=True, exist_ok=True)
            (skill_dir / "references" / "evidence-catalog.md").write_text(
                HEADER.format(src="EVIDENCE.md") + delink(ev_text), encoding="utf-8")
            if cn_text is not None:
                (skill_dir / "references" / "evidence-catalog-cn.md").write_text(
                    HEADER.format(src="EVIDENCE_CN.md") + delink(cn_text), encoding="utf-8")
            if idx_text is not None:
                (skill_dir / "references" / "evidence-index-en.md").write_text(INDEX_HEADER + idx_text,
                                                                               encoding="utf-8")
            (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy2(LINT, skill_dir / "scripts" / "slop_lint.py")
        else:
            expected = {
                "references/evidence-catalog.md": HEADER.format(src="EVIDENCE.md") + delink(ev_text),
                "references/evidence-catalog-cn.md": HEADER.format(src="EVIDENCE_CN.md") + delink(cn_text or ""),
                "references/evidence-index-en.md": INDEX_HEADER + (idx_text or ""),
            }
            for rel, want in expected.items():
                f = skill_dir / rel
                if not f.exists() or f.read_text(encoding="utf-8") != want:
                    problems.append(f"{skill}/{rel} is out of date: run python tools/sync_evidence.py")
            lint_copy = skill_dir / "scripts" / "slop_lint.py"
            if not lint_copy.exists() or lint_copy.read_bytes() != LINT.read_bytes():
                problems.append(f"{skill}/scripts/slop_lint.py is out of date: run python tools/sync_evidence.py")
        act_ids = ids_in(actions.read_text(encoding="utf-8")) if actions.exists() else set()
        missing = sorted(ev_ids - act_ids)
        extra = sorted(act_ids - ev_ids)
        if missing:
            problems.append(f"{skill}: no action for {', '.join(missing)}")
        if extra:
            problems.append(f"{skill}: actions for unknown IDs {', '.join(extra)}")
    print(f"Evidence IDs: {len(ev_ids)}")
    if problems:
        print("PROBLEMS:\n  " + "\n  ".join(problems))
        sys.exit(1)
    print("OK: " + ("checked" if check_only else "synced and checked") + " both skills.")


if __name__ == "__main__":
    main()
