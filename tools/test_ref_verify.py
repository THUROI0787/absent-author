#!/usr/bin/env python3
"""Offline tests for ref_verify.py (stdlib unittest, no network). Run: python -m unittest tools/test_ref_verify.py"""
import io
import json
import os
import sys
import unittest
import urllib.error
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_verify as RV  # noqa: E402

FIX = os.path.join(HERE, "fixtures", "refs")
LOIHI = "Advancing neuromorphic computing with Loihi: A survey of results and outlook"
LOIHI_TRUE = ["Mike Davies", "Andreas Wild", "Garrick Orchard", "Yulia Sandamirskaya", "Gabriel A. Fonseca Guerra",
              "Prasad Joshi", "Philipp Plank", "Sumedh R. Risbud", "Daniel Ben Dayan Rubin", "Lin Song"]


def crossref_json(title, authors, year=2021, venue="Proceedings of the IEEE"):
    items = [{"title": [title], "issued": {"date-parts": [[year]]}, "container-title": [venue],
              "author": [{"given": " ".join(a.split()[:-1]), "family": a.split()[-1]} for a in authors]}]
    return json.dumps({"message": {"items": items}})


def http_error(url, code):
    return urllib.error.HTTPError(url, code, "err", {}, None)


class FakeFetch:
    """Routes URLs by host to canned responses; a value that is an int raises that HTTP status."""

    def __init__(self, routes):
        self.routes, self.calls = routes, []

    def __call__(self, url, headers):
        self.calls.append(url)
        host = urllib.parse.urlparse(url).netloc
        resp = self.routes.get(host)
        if resp is None:
            raise urllib.error.URLError("no route")
        if isinstance(resp, int):
            raise http_error(url, resp)
        return resp


EMPTY_ATOM = '<feed xmlns="http://www.w3.org/2005/Atom"></feed>'


def verifier(routes):
    return RV.Verifier(fetch_text=FakeFetch(routes), sleep=lambda s: None)


class TestSplitter(unittest.TestCase):
    def test_numbered_pdf_text_with_wrapped_lines(self):
        entries, dropped = RV.load_entries(os.path.join(FIX, "numbered.txt"))
        self.assertEqual(len(entries), 5)
        self.assertEqual(dropped, 0)
        self.assertEqual([e["id"] for e in entries], ["1", "2", "3", "4", "5"])
        self.assertEqual(entries[2]["title"], "Deep residual learning for image recognition")  # de-hyphenated
        self.assertEqual(len(entries[3]["authors"]), 10)
        self.assertEqual(entries[3]["arxiv"], "2001.08361")
        self.assertEqual(entries[1]["doi"], "10.1109/JPROC.2021.3067593")
        self.assertEqual(entries[1]["year"], 2021)

    def test_author_year_and_duplicate_list_dropped(self):
        entries, dropped = RV.load_entries(os.path.join(FIX, "authoryear.txt"))
        self.assertEqual(len(entries), 5)
        self.assertEqual(dropped, 5)
        self.assertEqual(entries[0]["title"], LOIHI)
        self.assertEqual(entries[3]["title"], "Visualizing data using t-SNE")
        self.assertEqual([RV.name_key(a) for a in entries[3]["authors"]], ["maaten", "hinton"])
        self.assertEqual(RV.name_key(entries[4]["authors"][-1]), "polosukhin")

    def test_page_stamp_and_trailing_appendix_not_absorbed(self):
        stamp = "Confidential reviewer copy, do not distribute"
        text = "\n".join([
            "Intro text.", stamp, "References",
            "[1] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N.",
            "Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Advances in", stamp,
            "Neural Information Processing Systems, 2017.",
            "[2] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image",
            "recognition. In CVPR, 2016.",
            "[3] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In",
            "International Conference on Learning Representations, 2015.", stamp,
            "A Prompts", "You are a world-class architect. Propose a revolutionary block."])
        entries = [RV.parse_text_entry(i, t) for i, t in RV.split_text_entries(text)[0]]
        self.assertEqual(len(entries), 3)
        self.assertEqual(len(entries[0]["authors"]), 8)
        self.assertNotIn("Confidential", entries[0]["raw"])
        self.assertEqual(entries[2]["title"], "Adam: A method for stochastic optimization")
        self.assertEqual(len(entries[2]["authors"]), 2)


class TestAuthorChecks(unittest.TestCase):
    def test_head_correct_tail_fabricated_is_suspicious(self):
        cited = LOIHI_TRUE[:3] + ["Rahul Menon", "Laura Becker", "Tomas Lindqvist", "Hiro Tanaka",
                                  "Elena Petrova", "Marco Bellini", "Sara Okafor"]
        e = RV.make_entry("4", "raw", LOIHI, cited, year=2021, venue="Proc. IEEE")
        v = verifier({"export.arxiv.org": EMPTY_ATOM, "api.crossref.org": crossref_json(LOIHI, LOIHI_TRUE),
                      "api.semanticscholar.org": 429})
        r = v.check(e)
        self.assertEqual(r["verdict"], "suspicious")
        self.assertIs(r["first_author_match"], True)
        self.assertIs(r["last_author_match"], False)
        self.assertAlmostEqual(r["author_overlap"], 0.3)
        self.assertEqual(r["n_cited_authors"], 10)
        self.assertIn("crossref", r["found_in"])
        self.assertIn("confirm in a second one", " ".join(r["notes"]))
        self.assertIn("s2", v.unreachable)  # kept looking for a second database to confirm

    def test_tail_rule_alone(self):
        cited = LOIHI_TRUE[:7] + ["Invented Person"]  # 7/8 = 0.875 overlap: not suspicious, benign at most
        e = RV.make_entry("x", "raw", LOIHI, cited, year=2021)
        r = verifier({"api.crossref.org": crossref_json(LOIHI, LOIHI_TRUE[:8])}).check(e)
        self.assertEqual(r["verdict"], "benign_error")
        cited = LOIHI_TRUE[:6] + ["Invented One", "Invented Two"]  # 6/8 = 0.75 and last wrong
        r = verifier({"api.crossref.org": crossref_json(LOIHI, LOIHI_TRUE[:8])}).check(
            RV.make_entry("y", "raw", LOIHI, cited, year=2021))
        self.assertEqual(r["verdict"], "suspicious")

    def test_et_al_truncation_compares_listed_only(self):
        e = RV.parse_text_entry("2", "Davies, M., Wild, A., Orchard, G., et al. (2021). " + LOIHI
                                + ". Proceedings of the IEEE, 109(5), 911-934.")
        self.assertTrue(e["truncated"])
        self.assertEqual(len(e["authors"]), 3)
        r = verifier({"api.crossref.org": crossref_json(LOIHI, LOIHI_TRUE)}).check(e)
        self.assertEqual(r["verdict"], "ok")
        self.assertIsNone(r["last_author_match"])
        self.assertEqual(r["author_overlap"], 1.0)

    def test_year_off_by_one_is_benign(self):
        e = RV.make_entry("z", "raw", LOIHI, LOIHI_TRUE, year=2020)
        r = verifier({"api.crossref.org": crossref_json(LOIHI, LOIHI_TRUE)}).check(e)
        self.assertEqual((r["verdict"], r["year_diff"]), ("benign_error", -1))


class TestSources(unittest.TestCase):
    def test_ml_conference_not_in_crossref(self):
        e = RV.parse_text_entry("5", 'D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," '
                                     'in International Conference on Learning Representations (ICLR), 2015.')
        v = verifier({"api.crossref.org": json.dumps({"message": {"items": []}}), "export.arxiv.org": 429,
                      "api.semanticscholar.org": 429, "api.openalex.org": 429,
                      "dblp.org": "<html>Please verify you are human</html>"})
        r = v.check(e)
        self.assertEqual(r["verdict"], "not_found_in_reachable_sources")
        self.assertIn("Crossref does not index ML conferences", " ".join(r["notes"]))
        self.assertIn("anti-bot", v.unreachable["dblp"])
        report = RV.markdown_report("x.txt", [r], 1, 0, v)
        self.assertTrue(report.splitlines()[2].startswith("Candidates only"))
        self.assertIn("Unreachable sources: ", report)

    def test_not_ml_venue_plain_not_found(self):
        e = RV.make_entry("6", "raw", "A completely invented title about quantum gardening", ["A. Nobody"],
                          venue="Journal of Imaginary Results")
        r = verifier({"api.crossref.org": json.dumps({"message": {"items": []}})}).check(e)
        self.assertEqual(r["verdict"], "not_found")

    def test_backoff_retries_429_then_succeeds(self):
        calls, sleeps = [], []

        def opener(req, timeout):
            calls.append(req.full_url)
            if len(calls) < 3:
                raise http_error(req.full_url, 429)
            return io.BytesIO(b'{"ok": 1}')
        out = RV.http_get("https://api.crossref.org/works?x", {"User-Agent": "t"}, opener=opener,
                          sleep=sleeps.append)
        self.assertEqual(json.loads(out), {"ok": 1})
        self.assertEqual(len(calls), 3)
        self.assertEqual(sleeps, [2.0, 4.0])

    def test_backoff_gives_up_and_404_not_retried(self):
        sleeps = []

        def always429(req, timeout):
            raise http_error(req.full_url, 429)
        with self.assertRaises(urllib.error.HTTPError):
            RV.http_get("https://x.org", {}, opener=always429, sleep=sleeps.append)
        self.assertEqual(len(sleeps), 3)

        def nf(req, timeout):
            raise http_error(req.full_url, 404)
        sleeps.clear()
        with self.assertRaises(urllib.error.HTTPError):
            RV.http_get("https://x.org", {}, opener=nf, sleep=sleeps.append)
        self.assertEqual(sleeps, [])

    def test_cache_and_arxiv_id(self):
        atom = ('<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/abs/2001.08361v1</id>'
                '<title>Scaling Laws for Neural\n Language Models</title><published>2020-01-23T00:00:00Z</published>'
                + "".join(f"<author><name>{n}</name></author>" for n in
                          ["Jared Kaplan", "Sam McCandlish", "Tom Henighan", "Tom B. Brown", "Benjamin Chess",
                           "Rewon Child", "Scott Gray", "Alec Radford", "Jeffrey Wu", "Dario Amodei"])
                + "</entry></feed>")
        entries, _ = RV.load_entries(os.path.join(FIX, "numbered.txt"))
        v = verifier({"export.arxiv.org": atom})
        r = v.check(entries[3])
        self.assertEqual((r["verdict"], r["found_in"], r["last_author_match"]), ("ok", ["arxiv"], True))
        n = len(v.fetch_text.calls)
        v.check(entries[3])
        self.assertEqual(len(v.fetch_text.calls), n)  # served from cache


class TestBib(unittest.TestCase):
    def test_bib_parsing(self):
        entries, _ = RV.load_entries(os.path.join(FIX, "sample.bib"))
        self.assertEqual([e["id"] for e in entries], ["davies2021loihi", "vaswani2017attention", "kaplan2020scaling"])
        d, v, k = entries
        self.assertEqual(d["title"], "Advancing Neuromorphic Computing With Loihi: A Survey of Results and Outlook")
        self.assertEqual(len(d["authors"]), 8)
        self.assertEqual(RV.name_key(d["authors"][4]), "guerra")
        self.assertEqual((d["year"], d["doi"], d["venue"]), (2021, "10.1109/JPROC.2021.3067593", "Proceedings of the IEEE"))
        self.assertTrue(v["truncated"])
        self.assertEqual(v["title"], "Attention is All you Need")
        self.assertEqual(v["year"], 2017)
        self.assertEqual(k["arxiv"], "2001.08361")

    def test_sample_prefers_long_author_lists(self):
        entries, _ = RV.load_entries(os.path.join(FIX, "numbered.txt"))
        picked = RV.select_sample(entries, 2)
        self.assertTrue(all(len(e["authors"]) >= 8 for e in picked))
        self.assertIn("4", [e["id"] for e in picked])  # 10 authors + arXiv + recent


class TestNames(unittest.TestCase):
    def test_name_keys(self):
        for n in ["A. Vaswani", "Vaswani, A.", "Vaswani A", "Ashish Vaswani", "VASWANI, Ashish"]:
            self.assertEqual(RV.name_key(n), "vaswani", n)
        self.assertEqual(RV.name_key("Aaron van den Oord"), "oord")
        self.assertEqual(RV.name_key("Jürgen Schmidhuber"), "schmidhuber")
        self.assertEqual(RV.name_key("Wei Wang 0001"), "wang")

    def test_short_title_prefix_is_not_a_match(self):
        self.assertLess(RV.title_sim("Attention is all you need", "Attention Is All You Need: An Analysis Of "
                                     "The Valuation Of Artificial Intelligence Tokens"), RV.TITLE_MATCH)
        self.assertGreaterEqual(RV.title_sim("Advancing neuromorphic computing with Loihi", LOIHI), RV.TITLE_MATCH)


if __name__ == "__main__":
    unittest.main()
