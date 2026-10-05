#!/usr/bin/env python3
"""Render assets/social.png (1200x630) for link previews and the GitHub social preview.
Needs Playwright + Chromium (optional; the PNG is committed, so CI does not need this)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
svg = (ROOT / "assets" / "banner.svg").read_text(encoding="utf-8")
html = f"""<html><body style="margin:0;width:1200px;height:630px;background:#E9EDF1;display:flex;
align-items:center;justify-content:center">{svg}</body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(html)
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(ROOT / "assets" / "social.png"))
    b.close()
print("wrote assets/social.png")
