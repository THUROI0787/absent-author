#!/usr/bin/env python3
"""Smoke tests for slop_lint.py (stdlib unittest). Run: python -m unittest tools/test_slop_lint.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slop_lint as SL  # noqa: E402

SLOP = os.path.join(HERE, "fixtures", "synthetic_slop")
CLEAN = os.path.join(HERE, "fixtures", "clean_human.md")
REFS_TXT = os.path.join(HERE, "fixtures", "synthetic_refs.txt")


class TestFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.slop = SL.analyze(SLOP)
        cls.clean = SL.analyze(CLEAN)

    def test_slop_triggers_every_layer(self):
        must_fire = ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L10", "L14", "L16",
                     "S01", "S02", "S03", "S04", "S05", "S06", "S13", "R01", "R05", "R16",
                     "P01", "P02-meta", "P02-todo", "P03", "P05", "P06", "P07", "R17"]
        for cid in must_fire:
            self.assertGreater(self.slop["checks"][cid]["count"], 0, cid)

    def test_slop_rules(self):
        self.assertTrue(self.slop["checks"]["S01"]["rule"]["fired"])
        self.assertTrue(self.slop["checks"]["S02"]["rule"]["fired"])
        self.assertEqual(self.slop["checks"]["L03"]["sub"]["era_gpt4"] > 0, True)
        p03 = self.slop["checks"]["P03"]["sub"]
        self.assertEqual((p03["doe_author"], p03["et_al_in_author"], p03["arxiv_id_with_X"]), (1, 1, 1))
        self.assertIn("fig:missing", json.dumps(self.slop["checks"]["P02-todo"]["examples"]))
        self.assertIn("run_3", self.slop["checks"]["P07"]["identifiers"])

    def test_line_numbers_point_at_source(self):
        ex = self.slop["checks"]["S03"]["examples"][0]
        self.assertTrue(ex["loc"].startswith("main.tex:"))
        line = int(ex["loc"].split(":")[1])
        with open(os.path.join(SLOP, "main.tex")) as fh:
            self.assertIn("In response to reviewer concerns", fh.read().split("\n")[line - 1])

    def test_clean_is_quiet(self):
        for cid, r in self.clean["checks"].items():
            if cid == "P06":  # the fixture's own header comment is a legitimate candidate
                continue
            self.assertEqual(r["count"] if cid != "L15" else 0, 0, cid)
            self.assertIn(r["band"], ("typical", "n/a", "uncalibrated", "info"), cid)

    def test_math_cites_and_floats_are_stripped(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.tex")
            with open(p, "w") as fh:
                fh.write("\\documentclass{article}\\begin{document}\n"
                         "We show $x_1 = run\\_3$ holds \\cite{delve2020}.\n"
                         "\\begin{table}\\begin{tabular}{c} delve \\\\ seamless \\end{tabular}"
                         "\\caption{A plain caption.}\\end{table}\n"
                         "% delve into the realm\n"
                         "\\end{document}\n")
            r = SL.analyze(p)
            self.assertEqual(r["checks"]["L03"]["count"], 0)
            self.assertEqual(r["checks"]["L07"]["count"], 0)
            self.assertEqual(r["checks"]["P07"]["count"], 0)

    def test_numeric_ranges_are_not_dashes(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.tex")
            with open(p, "w") as fh:
                fh.write("\\begin{document}\nSee pages 3--5 and epochs 10 -- 20 for details.\n\\end{document}\n")
            self.assertEqual(SL.analyze(p)["checks"]["L01"]["count"], 0)

    # ---- v0.2 regressions from the blind test -------------------------------------------------
    def test_p05_watermark_across_latex_linebreaks_and_llm_authors(self):
        sub = self.slop["checks"]["P05"]["sub"]
        self.assertEqual(sub["ai_scientist"] + sub["generated_by_agent"], 1)  # one watermark, counted once
        self.assertEqual(sub["llm_in_author_block"], 2)  # GPT-4o, Claude

    def test_p02_tiers(self):
        meta = self.slop["checks"]["P02-meta"]["sub"]
        self.assertEqual(meta["please_fill"] + meta["fill_in_here"], 1)  # PLEASE FILL IN CAPTION HERE once
        self.assertGreater(meta["bracket_insert"], 0)
        self.assertIn("P02-meta", SL.TOMBSTONE_IDS)
        self.assertNotIn("P02-todo", SL.TOMBSTONE_IDS)
        self.assertGreater(self.slop["checks"]["P02-todo"]["sub"]["todo"], 0)

    def test_bbl_agent_notes(self):
        self.assertGreater(self.slop["checks"]["P01"]["sub"]["agent_note_in_references"], 0)

    def test_txt_references_p03_and_ieee_header(self):
        r = SL.analyze(REFS_TXT)
        sub = r["checks"]["P03"]["sub"]
        for k in ("arxiv_id_with_X", "arxiv_impossible_month", "et_al_sole_author", "duplicate_ref_number",
                  "doe_author"):
            self.assertEqual(sub[k], 1, k)
        self.assertEqual(r["checks"]["P02-todo"]["count"], 0)  # "VOL. XX, NO. XX, XXXX" is not a TODO
        self.assertEqual(r["checks"]["P02-meta"]["count"], 0)

    def test_p06_h06_and_s2_info_only(self):
        p06 = self.slop["checks"]["P06"]
        self.assertEqual(p06["info"]["possible_human_collaboration_traces_H06"]["comment_lines"], 1)
        self.assertNotIn("s2_style_bib_keys", p06["sub"])
        self.assertEqual(p06["info"]["s2_style_bib_keys"]["count"], 1)

    def test_p07_skips_texttt_and_keeps_run_config(self):
        ids = self.slop["checks"]["P07"]["identifiers"]
        self.assertNotIn("shakespeare_char", ids)  # typeset with \texttt
        for k in ("run_3", "config_A2", "val_bpb"):
            self.assertIn(k, ids)

    def test_no_double_count_l03_l14(self):
        self.assertNotIn("load-bearing", self.slop["checks"]["L03"]["per_word"])
        self.assertGreater(self.slop["checks"]["L14"]["sub"]["load-bearing"], 0)

    def test_l02_colon_and_s03_revision(self):
        self.assertGreater(self.slop["checks"]["L02"]["sub"]["not_X_colon_Y"], 0)
        s03 = self.slop["checks"]["S03"]["sub"]
        for k in ("earlier_version", "published_draft", "in_this_revision"):
            self.assertGreater(s03[k], 0, k)

    def test_math_placeholder_in_snippets(self):
        ex = json.dumps(self.slop["checks"]["L02"]["examples"])
        self.assertIn("[MATH]", ex)

    def test_r17_and_p13_info_only(self):
        r17 = self.slop["checks"]["R17"]
        self.assertEqual(r17["band"], "info")
        self.assertEqual(r17["sub"]["pct_of_n_inconsistent"], 1)  # 12.4% of 207 is impossible
        self.assertEqual(r17["sub"]["pm_zero"], 1)
        self.assertTrue(SL._grim_ok("12.56", 207))
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "paper.tex"), "w") as fh:
                fh.write("\\begin{document}\nA short body.\n\\end{document}\n")
            for name in ("CLAUDE.md", "review_round2.md", "results.tsv"):
                with open(os.path.join(d, name), "w") as fh:
                    fh.write("commit\tscore\tstatus\nabc\t0.9\tkeep\n" if name == "results.tsv" else "x\n")
            os.mkdir(os.path.join(d, ".claude"))
            p13 = SL.analyze(d)["checks"]["P13"]
            self.assertEqual(p13["band"], "info")
            for k in ("claude_md", "review_round", "dot_claude", "results_tsv_keep_discard"):
                self.assertEqual(p13["sub"][k], 1, k)

    def test_cli_json_and_md(self):
        out = subprocess.run([sys.executable, os.path.join(HERE, "slop_lint.py"), SLOP, CLEAN, "--format", "json"],
                             capture_output=True, text=True, check=True).stdout
        data = json.loads(out)
        self.assertEqual(len(data), 2)
        md = subprocess.run([sys.executable, os.path.join(HERE, "slop_lint.py"), CLEAN],
                            capture_output=True, text=True, check=True).stdout
        self.assertIn("CANDIDATES, not verdicts", md)
        self.assertIn("Absence of hits means nothing", md)

    def test_bands_are_monotone(self):
        r = {"id": "L03", "available": True, "count": 1, "per_1k": 0.0}
        if "L03" not in SL.CALIBRATION:
            self.skipTest("uncalibrated")
        c = SL.CALIBRATION["L03"]
        seq = []
        for v in (c["p50"], c["p90"] + 1e-6, c["p99"] + 1e-6):
            r["per_1k"] = v
            seq.append(SL.band(r))
        self.assertEqual(seq, ["typical", "elevated", "high"])


class TestReportedFalsePositives(unittest.TestCase):
    """Regression tests for false positives reported on GitHub (issues #1-#3)."""

    def _run(self, tex):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.tex")
            with open(p, "w") as fh:
                fh.write("\\documentclass{article}\\begin{document}\n" + tex + "\n\\end{document}\n")
            return SL.analyze(p)["checks"]

    def test_issue1_credit_roles(self):
        c = self._run("\\section*{CRediT authorship contribution statement}\n"
                      "Alice: Conceptualization; Writing -- original draft; Writing -- review and editing.\n"
                      "Bob: Writing \u2013 review \\& editing.")
        self.assertEqual(c["L01"]["count"], 0)
        self.assertEqual(c["S03"]["count"], 0)
        # real revision leakage and real dashes still fire
        c = self._run("\\section{Method}\nThe original draft overstated the gain -- we fixed it.")
        self.assertGreater(c["S03"]["count"], 0)
        self.assertGreater(c["L01"]["count"], 0)

    def test_issue2_label_inside_macro(self):
        c = self._run("\\newcommand{\\paperfigure}[3]{\\begin{figure}\\caption{#2}\\label{#3}\\end{figure}}\n"
                      "\\section{Results}\nSee Figure~\\ref{fig:es}.\n"
                      "\\paperfigure{Figure_1.pdf}{Exposure gradient.}{fig:es}")
        self.assertEqual(c["P02-todo"]["sub"]["undefined_ref_labels"], 0)
        c = self._run("\\section{Results}\nSee Figure~\\ref{fig:missing}.")
        self.assertEqual(c["P02-todo"]["sub"]["undefined_ref_labels"], 1)

    def test_issue3_logical_non_implication(self):
        c = self._run("\\section{Model}\nAssumption 2 is imposed at level $s_0$, and it does not imply "
                      "its own analogue at neighboring levels.")
        self.assertEqual(c["S01"]["count"], 0)
        c = self._run("\\section{Discussion}\nOur results are strong. This does not imply that the method "
                      "is optimal in every setting.")
        self.assertGreater(c["S01"]["count"], 0)


class TestNonAuthorSections(unittest.TestCase):
    def test_prompt_and_checklist_sections_are_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.tex")
            with open(p, "w") as fh:
                fh.write("\\documentclass{article}\\begin{document}\n\\section{Method}\nWe train a model.\n\n"
                         "\\appendix\n\\section{Prompts}\n\\subsection{Stage 1}\nRevolutionary groundbreaking design! "
                         "So, what does this mean? Let's take a closer look.\n\n"
                         "\\section{NeurIPS Paper Checklist}\nDo the main claims made in the abstract reflect the scope?\n\n"
                         "\\section{Extra Results}\nRevolutionary results.\n\\end{document}\n")
            r = SL.analyze(p)
            self.assertTrue(any("Prompts" in t for t in r["excluded_sections"]))
            self.assertEqual(r["checks"]["L16"]["count"], 0)
            # text after the excluded sections is still scanned
            self.assertGreater(r["checks"]["L07"]["count"], 0)
            # no blank line before \section: the paragraph straddles the heading
            p3 = os.path.join(d, "u.tex")
            with open(p3, "w") as fh:
                fh.write("\\documentclass{article}\\begin{document}\n\\section{Method}\nWe train a model.\n"
                         "\\appendix\n\\section{Prompts}\nSo, what does this mean? Isn't it amazing?\n"
                         "\\end{document}\n")
            self.assertEqual(SL.analyze(p3)["checks"]["L16"]["count"], 0)
            # PDF text: numbered checklist items and A.1/A.2 sub-headings all parse as level-1 headings
            p4 = os.path.join(d, "v.txt")
            with open(p4, "w") as fh:
                fh.write("Title\n\n1 Introduction\nWe train a model on data.\n\nA Prompts\n\nA.1 Mutation\n"
                         "So, what does this mean?\n\nA.2 Crossover\nIsn't it amazing?\n\n"
                         "B NeurIPS Paper Checklist\n\n1. Claims\nQuestion: Do the main claims reflect the scope?\n\n"
                         "2. Limitations\nQuestion: Does the paper discuss the limitations?\n\n"
                         "C Extra Results\nRevolutionary results. Why does this work?\n")
            r4 = SL.analyze(p4)
            self.assertEqual(r4["checks"]["L16"]["count"], 1)  # only the question in "C Extra Results"
            r2 = SL.analyze(p, default_excludes=False)
            self.assertEqual(r2["excluded_sections"], [])
            self.assertGreater(r2["checks"]["L16"]["count"], 0)


class TestPromptHeadingScope(unittest.TestCase):
    def test_main_text_prompt_section_is_kept(self):
        self.assertFalse(SL.NON_AUTHOR_SECTION_RX.search("Prompt Optimization"))
        self.assertFalse(SL.NON_AUTHOR_SECTION_RX.search("Prompting strategies"))
        for t in ("Prompts", "Appendix: Prompts", "A.3 Prompts used in the search", "System prompt",
                  "Prompt templates", "NeurIPS Paper Checklist"):
            self.assertTrue(SL.NON_AUTHOR_SECTION_RX.search(t), t)


if __name__ == "__main__":
    unittest.main()
