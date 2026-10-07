#!/usr/bin/env python3
"""Tests for number_ledger.py (stdlib unittest). Run: python -m unittest tools/test_number_ledger.py"""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import number_ledger as NL  # noqa: E402

FIX = os.path.join(HERE, "fixtures", "numbers")
BAD_TEX = os.path.join(FIX, "inconsistent.tex")
GOOD_TEX = os.path.join(FIX, "consistent.tex")
BAD_MD = os.path.join(FIX, "inconsistent.md")


def entities(r):
    return {c["entity"]: c for c in r["candidates"]}


class TestInconsistentTex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = NL.analyze(BAD_TEX)
        cls.ents = entities(cls.r)

    def test_search_duration_month_vs_weeks(self):
        c = self.ents["duration:search"]
        self.assertEqual(set(c["values"]), {"30", "21"})
        self.assertTrue(any("week" in o["note"] for o in c["occurrences"]))
        self.assertEqual({o["section"] for o in c["occurrences"]} >= {"Introduction", "Method"}, True)

    def test_gpu_hours_derived_vs_table_total(self):
        c = self.ents["gpu_hours"]
        self.assertEqual(set(c["values"]), {"3360", "2880"})
        self.assertTrue(any(o["kind"] == "derived" for o in c["occurrences"]))

    def test_elites_text_vs_caption(self):
        self.assertEqual(set(self.ents["elites"]["values"]), {"16", "12"})

    def test_composition(self):
        self.assertIn("composition:feature", self.ents)
        self.assertTrue(self.ents["composition:feature"]["generic"])

    def test_relative_improvement(self):
        rel = [a for a in self.r["arithmetic"] if a["check"] == "relative_change"]
        self.assertEqual(len(rel), 1)
        self.assertIn("16%", rel[0]["claim"])
        self.assertIn("6.7%", rel[0]["expected"])

    def test_grim_ratio_difference(self):
        checks = {a["check"].split()[0] for a in self.r["arithmetic"]}
        self.assertTrue({"percent_of_n", "ratio", "difference"} <= checks, checks)

    def test_table_avg(self):
        self.assertEqual(len(self.r["tables"]), 1)
        t = self.r["tables"][0]
        self.assertEqual((t["column"], t["stated"], t["recomputed"]), ("Avg", "81.0", "78"))

    def test_references_dropped(self):
        self.assertFalse(any(o["raw"] == "99" for o in self.r["numbers"]))


class TestConsistentTex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = NL.analyze(GOOD_TEX)

    def test_zero_candidates(self):
        self.assertEqual(self.r["candidates"], [])
        self.assertEqual(self.r["arithmetic"], [])
        self.assertEqual(self.r["tables"], [])

    def test_positive_consistency_count(self):
        s = self.r["summary"]
        self.assertGreaterEqual(s["consistent_repeated_numbers"], 6)
        self.assertGreaterEqual(s["arithmetic_checks_ok"], 4)
        self.assertGreaterEqual(s["table_checks_ok"], 2)
        self.assertIn("Numbers checked consistent: %d" % s["checked_consistent"], NL.to_markdown(self.r))

    def test_ignored_numbers(self):
        raws = {o["raw"] for o in self.r["numbers"]}
        # years, Section 3.2 / Table 1, ResNet-50 / CIFAR-10 / GPT-4, Eq. 3, citations, prompt + checklist appendices
        for bad in ("2024", "2023", "3.2", "1", "50", "10", "3", "0.5", "5", "99"):
            self.assertNotIn(bad, raws)
        its = [o for o in self.r["numbers"] if o["entity"] == "iterations"]
        self.assertEqual({o["value"] for o in its}, {6.0})


class TestMarkdown(unittest.TestCase):
    def test_md_candidates_and_total_row(self):
        r = NL.analyze(BAD_MD)
        ents = entities(r)
        self.assertEqual(set(ents["iterations"]["values"]), {"6", "3"})
        self.assertEqual(set(ents["pct_valid"]["values"]), {"49", "4.2"})
        self.assertIn("duration:training", ents)
        self.assertEqual([t["stated"] for t in r["tables"]], ["1,600"])
        raws = {o["raw"] for o in r["numbers"]}
        self.assertNotIn("99", raws)  # user-prompt appendix dropped
        self.assertNotIn("12", raws)  # citation [12] and references dropped


class TestUnits(unittest.TestCase):
    def test_same_tolerance(self):
        o = lambda v, raw: {"value": v, "half_unit": NL.half_unit(raw)}  # noqa: E731
        self.assertTrue(NL.same(o(49, "49"), o(49.3, "49.3")))
        self.assertTrue(NL.same(o(2880, "2,880"), o(2900, "2.9")))
        self.assertFalse(NL.same(o(16, "16"), o(12, "12")))

    def test_cli_json_and_output(self):
        out = os.path.join(FIX, "_tmp_out.md")
        try:
            p = subprocess.run([sys.executable, os.path.join(HERE, "number_ledger.py"), GOOD_TEX, "-o", out],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            with open(out, encoding="utf-8") as fh:
                self.assertIn(NL.HEADER, fh.read())
        finally:
            if os.path.exists(out):
                os.remove(out)
        p = subprocess.run([sys.executable, os.path.join(HERE, "number_ledger.py"), BAD_TEX, "--json"],
                           capture_output=True, text=True)
        self.assertGreaterEqual(json.loads(p.stdout)["summary"]["candidates"], 3)


if __name__ == "__main__":
    unittest.main()
