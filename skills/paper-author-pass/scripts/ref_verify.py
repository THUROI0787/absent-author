#!/usr/bin/env python3
"""ref_verify.py: check a reference list against bibliographic databases (P03 candidates).

Compares title AND the full cited author list (including the last author) with what
arXiv / Crossref / Semantic Scholar / OpenAlex / DBLP return. A real title with a correct
head and an invented tail of authors is the pattern this tool exists to catch.

  python tools/ref_verify.py refs.bib|refs.bbl|refs.txt [--sample N] [--ids 1,4,7]
         [--cache ~/.cache/absent-author/ref_cache.json] [--mailto you@x] [--json] [-o out.md] [--offline]

Stdlib only. Output is a list of candidates, never a verdict on the paper.
"""
import argparse
import difflib
import json
import os
import re
import socket
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HEADER = "Candidates only; a suspicious entry needs a second database before it counts as P03 (☠)."
ML_VENUE = re.compile(r"\b(ICLR|ICML|NeurIPS|NIPS|OpenReview|PMLR|Proceedings of Machine Learning Research|"
                      r"Neural Information Processing Systems|International Conference on "
                      r"(?:Learning Representations|Machine Learning))\b", re.I)
ML_NOTE = ("not_found_in_reachable_sources (Crossref does not index ML conferences; "
           "check OpenReview/PMLR/proceedings.neurips.cc)")
ARXIV_RE = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d])")
ARXIV_X_RE = re.compile(r"\b\d{4}\.[\dX]*X[\dX]*\b")
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s,;\"{}]+)")
YEAR_RE = re.compile(r"\b((?:19|20)\d{2})[a-z]?\b")
TITLE_MATCH = 0.9
UA_BASE = "absent-author-ref-verify/0.1 (+polite bibliographic checks)"
MIN_INTERVAL = {"export.arxiv.org": 3.0}  # arXiv asks for >= 3 s between calls; 1 s elsewhere


class SourceUnavailable(Exception):
    pass


# ---------------------------------------------------------------- text helpers
def deaccent(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def delatex(s):
    s = re.sub(r"\\[`'^\"~=.uvHcdbk]\s*\{?\\?([a-zA-Z])\}?", r"\1", s)
    for _ in range(3):
        s = re.sub(r"\\[a-zA-Z]+\*?\s*\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(?:em|it|bf|sc|rm|tt)\b", "", s)
    s = s.replace("\\&", "&").replace("~", " ").replace("--", "-")
    s = re.sub(r"\\[a-zA-Z]+", "", s).replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def norm_title(t):
    t = deaccent(delatex(t or "")).lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def title_sim(a, b):
    na, nb = norm_title(a), norm_title(b)
    if not na or not nb:
        return 0.0
    r = difflib.SequenceMatcher(None, na, nb).ratio()
    short, long_ = sorted((na, nb), key=len)
    if len(short) >= 40 and long_.startswith(short):  # long title, subtitle dropped: same paper
        r = max(r, 0.92)
    return round(r, 3)


def is_initial(tok):
    return bool(re.fullmatch(r"(?:[A-Z]\.?-?){1,3}|(?:[A-Z]\.-?)+[A-Z]?\.?", tok))


def name_key(name):
    """Normalized surname key: 'A. Vaswani', 'Vaswani, A.', 'Vaswani A', 'Ashish Vaswani' -> 'vaswani'."""
    n = re.sub(r"\d+", "", deaccent(delatex(name))).strip(" .,;")
    if not n:
        return ""
    if "," in n:
        sur = n.split(",")[0]
    else:
        toks = n.split()
        non = [t for t in toks if not is_initial(t)]
        if not non:
            return ""
        sur = non[0] if (len(toks) > 1 and is_initial(toks[-1]) and not is_initial(toks[0])) else non[-1]
    parts = [re.sub(r"[^a-z]", "", p.lower()) for p in sur.split()]
    parts = [p for p in parts if p]
    return parts[-1] if parts else ""


def split_authors(s):
    """Split an author string into names; returns (names, truncated_by_et_al)."""
    s = delatex(s)
    truncated = bool(re.search(r"\bet\.?\s*al\b|\band others\b", s, re.I))
    s = re.sub(r"\bet\.?\s*al\.?|\band others\b", "", s, flags=re.I)
    s = re.sub(r"\s+(?:and|&)\s+|\s*&\s*", ",", s)
    chunks = [c.strip(" .;:") for c in re.split(r"[,;]", s)]
    names = []
    for c in chunks:
        if not c:
            continue
        if names and all(is_initial(t) for t in c.split()) and "," not in names[-1]:
            names[-1] = names[-1] + ", " + c          # 'Vaswani', 'A.' -> 'Vaswani, A.'
        elif len(c.split()) <= 6:
            names.append(c)
    return [n for n in names if name_key(n)], truncated


def split_sentences(s):
    s = re.sub(r"\bet al\.", "et al", s)
    return [p.strip() for p in re.split(r"(?:(?<=[^\s.][^\s.A-Z])|(?<=[A-Z]{3}))\.\s+|(?<=[?!])\s+", s)
            if p.strip()]


# ---------------------------------------------------------------- parsing
def make_entry(eid, raw, title="", authors=None, truncated=False, year=None, arxiv=None, doi=None, venue=""):
    return {"id": str(eid), "raw": raw, "title": (title or "").strip(" .,;:"), "authors": authors or [],
            "truncated": truncated, "year": year, "arxiv": arxiv, "doi": doi, "venue": venue,
            "flags": ["arxiv_id_with_X"] if ARXIV_X_RE.search(raw) else []}


def ids_and_year(s):
    a = ARXIV_RE.search(s)
    d = DOI_RE.search(s)
    rest = DOI_RE.sub(" ", ARXIV_RE.sub(" ", s))
    years = YEAR_RE.findall(rest)
    return (a.group(1) if a else None), (d.group(1).rstrip(".") if d else None), (int(years[-1]) if years else None)


def parse_text_entry(eid, raw):
    s = re.sub(r"^\s*(?:\[\d+\]|\d{1,4}\.)\s*", "", raw).strip()
    arxiv, doi, year = ids_and_year(s)
    q = re.search(r"[“\"]([^”\"]{8,})[”\"]", s)
    if q:
        auth, title = s[:q.start()], q.group(1)
    else:
        m = re.search(r"\(((?:19|20)\d{2})[a-z]?\)", s)
        if not m:
            m2 = re.search(r"[.,]\s+((?:19|20)\d{2})[a-z]?[.,]\s", s)
            if m2 and m2.start() < 0.45 * len(s) and ("," in s[:m2.start()] or " and " in s[:m2.start()]):
                m = m2
        if m:
            auth = s[:m.start()]
            year = int(m.group(1))
            sents = split_sentences(s[m.end():].lstrip(" .,:"))
            title = sents[0] if sents else ""
        else:
            sents = split_sentences(s)
            auth, title = sents[0], (sents[1] if len(sents) > 1 else "")
    title = re.split(r",\s+(?:in|In)\s", title)[0]
    authors, trunc = split_authors(auth)
    return make_entry(eid, raw, title, authors, trunc, year, arxiv, doi, venue=s)


AUTH_START = re.compile(
    r"^(?:[A-ZÀ-ÖØ-Þ][\w'’\-]+(?:\s(?:van|von|de|der|den|da|di|del|la|le|du))*,\s+(?:[A-Z]\.|[A-Z][a-z]+)"
    r"|[A-ZÀ-ÖØ-Þ][\w'’\-]+\s[A-Z]{1,3}[,.]"
    r"|(?:(?:van|von|de|der|den|di|da|du|la|le)\s)+[A-Z][\w'’\-]+,)")
ENDS_ENTRY = re.compile(r"(?:\.|(?:19|20)\d{2}[a-z]?\)?\.?)\s*$")
APPENDIX_HEAD = re.compile(r"^\s*(?:(?:APPENDIX|Appendix|Supplementary Material)\b.{0,60}|"
                           r"[A-H](?:\.\d+)?\s+[A-Z][\w\-']*(?:\s+[A-Z][\w\-']*){0,5})\s*$")
REF_HEAD = re.compile(r"^\s*(?:\d+\s+)?(references|bibliography|literature cited)\s*$", re.I)


def join_lines(lines):
    acc = ""
    for ln in lines:
        ln = ln.strip()
        if acc.endswith("-") and ln[:1].islower():
            acc = acc[:-1] + ln
        else:
            acc = (acc + " " + ln).strip()
    return acc


def split_text_entries(text):
    """Split PDF-extracted text into reference entries. Returns (list of (id, text), n_duplicates_dropped)."""
    lines = text.splitlines()
    # running headers/footers ("Confidential reviewer copy ...") repeat verbatim on every page: drop them
    rep = {}
    for ln in lines:
        if ln.strip():
            rep[ln.strip()] = rep.get(ln.strip(), 0) + 1
    lines = [ln for ln in lines if not (rep.get(ln.strip(), 0) >= 3 and len(ln.split()) <= 15
                                        and not REF_HEAD.match(ln))]
    for i, ln in enumerate(lines):
        if REF_HEAD.match(ln):
            lines = lines[i + 1:]
            break
    # an appendix after the list ("A Prompts", "Appendix B") is not part of the last entry: skip it
    # until another References heading (a duplicated list is deduplicated below)
    kept, skipping, last = [], False, ""
    for ln in lines:
        if REF_HEAD.match(ln):
            skipping = False
        elif not skipping and APPENDIX_HEAD.match(ln) and ENDS_ENTRY.search(last):
            skipping = True
        if not skipping:
            kept.append(ln)
        if ln.strip():
            last = ln
    lines = kept
    lines = ["" if (REF_HEAD.match(ln) or re.fullmatch(r"\s*\d{1,4}\s*", ln)) else ln for ln in lines]
    br = sum(bool(re.match(r"^\s*\[\d{1,4}\]", ln)) for ln in lines)
    dot = sum(bool(re.match(r"^\s*\d{1,4}\.\s+\S", ln)) for ln in lines)
    mode = "bracket" if br >= 3 else "dot" if dot >= 3 else "authyear"
    entries, cur, cur_id, last_num, prev = [], [], None, 0, ""
    for ln in lines:
        if not ln.strip():
            prev = ""
            continue
        start, num = False, None
        if mode == "bracket":
            m = re.match(r"^\s*\[(\d{1,4})\]", ln)
            start, num = bool(m), (m.group(1) if m else None)
        elif mode == "dot":
            m = re.match(r"^\s*(\d{1,4})\.\s+\S", ln)
            if m and (int(m.group(1)) in (last_num + 1, 1)):
                start, num = True, m.group(1)
                last_num = int(num)
        else:
            author_like = bool(AUTH_START.match(ln))
            # a line ending in a bare initial ("Aidan N.") is mid-name, not the end of an entry
            ends = bool(ENDS_ENTRY.search(prev)) and not re.search(r"\b[A-Z]\.\s*$", prev)
            start = (not prev and (ln[:1].isupper() or author_like)) or (ends and author_like)
        if start and cur:
            entries.append((cur_id, join_lines(cur)))
            cur = []
        if start or not cur:
            cur_id = num or str(len(entries) + 1)
        cur.append(ln)
        prev = ln
    if cur:
        entries.append((cur_id, join_lines(cur)))
    out, seen, dropped = [], set(), 0
    for eid, t in entries:
        if len(t) < 30:  # stray headings ("Appendix") and page furniture
            continue
        key = norm_title(re.sub(r"^\s*(?:\[\d+\]|\d{1,4}\.)\s*", "", t))[:120]
        if key in seen:
            dropped += 1
            continue
        seen.add(key)
        out.append((eid, t))
    return out, dropped


def _bib_value(body, i):
    if body[i] == "{":
        depth, j = 0, i
        while j < len(body):
            depth += {"{": 1, "}": -1}.get(body[j], 0)
            if depth == 0:
                return body[i + 1:j], j + 1
            j += 1
        return body[i + 1:], len(body)
    if body[i] == '"':
        j = body.find('"', i + 1)
        return body[i + 1:j], j + 1
    m = re.match(r"[^,]*", body[i:])
    return m.group(0).strip(), i + m.end()


def parse_bib(text):
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        if m.group(1).lower() in ("comment", "string", "preamble"):
            continue
        depth, j = 1, m.end()
        while j < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        body, fields, i = text[m.end():j - 1], {}, 0
        while True:
            fm = re.compile(r"\s*,?\s*([\w-]+)\s*=\s*").match(body, i)
            if not fm or fm.end() >= len(body):
                break
            val, i = _bib_value(body, fm.end())
            fields[fm.group(1).lower()] = val
        names = [a.strip() for a in re.split(r"\s+and\s+", fields.get("author", "")) if a.strip()]
        trunc = any(n.lower() == "others" for n in names)
        names = [delatex(n) for n in names if n.lower() != "others"]
        raw = text[m.start():j]
        arxiv = fields.get("eprint") or (ARXIV_RE.search(raw).group(1) if ARXIV_RE.search(raw) else None)
        yr = re.search(r"\d{4}", fields.get("year", ""))
        out.append(make_entry(m.group(2), raw, delatex(fields.get("title", "")), names, trunc,
                              int(yr.group(0)) if yr else None, arxiv, fields.get("doi"),
                              delatex(fields.get("journal") or fields.get("booktitle") or "")))
    return out


def parse_bbl(text):
    text = text.split("\\end{thebibliography}")[0]
    out = []
    for n, block in enumerate(re.split(r"\\bibitem", text)[1:], 1):
        m = re.match(r"\s*(?:\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\{([^}]*)\}", block)
        rest = block[m.end():] if m else block
        eid = m.group(1) if m else str(n)
        if "\\newblock" in rest:
            parts = [delatex(p).strip(" .,") for p in re.split(r"\\newblock", rest)]
            arxiv, doi, year = ids_and_year(" ".join(parts))
            authors, trunc = split_authors(parts[0])
            out.append(make_entry(eid, delatex(rest), parts[1], authors, trunc, year, arxiv, doi, " ".join(parts[2:])))
        else:
            e = parse_text_entry(eid, delatex(rest))
            out.append(e)
    return out


def load_entries(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    ext = os.path.splitext(path)[1].lower()
    if ext == ".bib":
        return parse_bib(text), 0
    if ext == ".bbl":
        return parse_bbl(text), 0
    raw, dropped = split_text_entries(text)
    return [parse_text_entry(eid, t) for eid, t in raw], dropped


def select_sample(entries, n):
    def score(e):
        return ((len(e["authors"]) >= 8) * 100 + min(max((e["year"] or 2000) - 2000, 0), 30)
                + (5 if e["arxiv"] else 0))
    order = {id(e): i for i, e in enumerate(entries)}
    longs = sorted([e for e in entries if len(e["authors"]) >= 8], key=lambda e: (-score(e), order[id(e)]))
    picked = longs[:min(2, n)]
    rest = sorted([e for e in entries if e not in picked], key=lambda e: (-score(e), order[id(e)]))
    picked += rest[:max(n - len(picked), 0)]
    return sorted(picked, key=lambda e: order[id(e)])


# ---------------------------------------------------------------- network
def http_get(url, headers, opener=None, sleep=time.sleep, tries=4, timeout=30):
    """GET with exponential backoff on 429/5xx and transient network errors."""
    opener = opener or urllib.request.urlopen
    for i in range(tries):
        try:
            with opener(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if (e.code != 429 and e.code < 500) or i == tries - 1:
                raise
            ra = e.headers.get("Retry-After") if e.headers else None
            sleep(min(float(ra) if ra and ra.isdigit() else 2.0 * 2 ** i, 30))
        except (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionError):
            if i == tries - 1:
                raise
            sleep(2.0 * 2 ** i)


def _rec(title, authors, year, venue):
    return {"title": delatex(title or ""), "authors": [a for a in authors if a], "year": year, "venue": venue or ""}


def parse_arxiv(xml_text):
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(xml_text).findall("a:entry", ns):
        if "api/errors" in (e.findtext("a:id", "", ns) or ""):
            continue
        pub = e.findtext("a:published", "", ns)
        out.append(_rec(re.sub(r"\s+", " ", e.findtext("a:title", "", ns)),
                        [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)],
                        int(pub[:4]) if pub[:4].isdigit() else None, "arXiv"))
    return out


def _crossref_item(it):
    yr = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
    names = [", ".join(x for x in (a.get("family"), a.get("given")) if x) or a.get("name", "")
             for a in it.get("author", [])]
    return _rec((it.get("title") or [""])[0], names, yr, (it.get("container-title") or [""])[0])


class Verifier:
    STEPS = [("arxiv_id", "arxiv"), ("crossref_doi", "crossref"), ("crossref", "crossref"),
             ("arxiv_title", "arxiv"), ("s2", "s2"), ("openalex", "openalex"), ("dblp", "dblp")]

    def __init__(self, fetch_text=None, cache=None, mailto="", sleep=time.sleep):
        self.sleep = sleep
        self.fetch_text = fetch_text or (lambda url, headers: http_get(url, headers, sleep=sleep))
        self.cache = cache if cache is not None else {}
        self.mailto = mailto
        self.ua = UA_BASE + (f" mailto:{mailto}" if mailto else "")
        self.unreachable, self.reachable, self._last = {}, set(), {}

    def get(self, source, url, headers=None, json_out=True):
        if source in self.unreachable:
            raise SourceUnavailable(self.unreachable[source])
        key = re.sub(r"[&?](?:api_key|mailto)=[^&]*", "", url)
        if key not in self.cache:
            host = urllib.parse.urlparse(url).netloc
            wait = MIN_INTERVAL.get(host, 1.0) - (time.monotonic() - self._last.get(host, -1e9))
            if wait > 0:
                self.sleep(wait)
            try:
                text = self.fetch_text(url, dict({"User-Agent": self.ua}, **(headers or {})))
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    self.reachable.add(source)
                    return None
                self.unreachable[source] = f"HTTP {e.code}"
                raise SourceUnavailable(self.unreachable[source])
            except Exception as e:  # network down, proxy refusal, timeouts
                self.unreachable[source] = type(e).__name__ + ": " + str(e)[:80]
                raise SourceUnavailable(self.unreachable[source])
            finally:
                self._last[host] = time.monotonic()
            if json_out:
                try:
                    json.loads(text)
                except ValueError:
                    self.unreachable[source] = "non-JSON response (anti-bot page?)"
                    raise SourceUnavailable(self.unreachable[source])
            self.cache[key] = text
        self.reachable.add(source)
        return json.loads(self.cache[key]) if json_out else self.cache[key]

    def search(self, step, e):
        q = urllib.parse.quote(e["title"])
        mt = urllib.parse.quote(self.mailto)
        if step == "arxiv_id":
            t = self.get("arxiv", f"https://export.arxiv.org/api/query?id_list={e['arxiv']}&max_results=1", json_out=False)
            return parse_arxiv(t) if t else []
        if step == "arxiv_title":
            phrase = re.sub(r"[^\w\s]", " ", e["title"])
            t = self.get("arxiv", "https://export.arxiv.org/api/query?search_query="
                         + urllib.parse.quote(f'ti:"{" ".join(phrase.split())}"') + "&max_results=3", json_out=False)
            return parse_arxiv(t) if t else []
        if step == "crossref_doi":
            d = self.get("crossref", f"https://api.crossref.org/works/{urllib.parse.quote(e['doi'])}"
                         + (f"?mailto={mt}" if self.mailto else ""))
            return [_crossref_item(d["message"])] if d else []
        if step == "crossref":
            d = self.get("crossref", f"https://api.crossref.org/works?query.bibliographic={q}&rows=3"
                         "&select=title,author,issued,container-title" + (f"&mailto={mt}" if self.mailto else ""))
            return [_crossref_item(it) for it in (d or {}).get("message", {}).get("items", [])]
        if step == "s2":
            h = {"x-api-key": os.environ["S2_API_KEY"]} if os.environ.get("S2_API_KEY") else {}
            d = self.get("s2", f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}"
                         "&limit=3&fields=title,authors,year,venue", h)
            return [_rec(p.get("title"), [a.get("name", "") for a in p.get("authors") or []], p.get("year"),
                         p.get("venue")) for p in (d or {}).get("data") or []]
        if step == "openalex":
            url = f"https://api.openalex.org/works?search={q}&per-page=3"
            if os.environ.get("OPENALEX_API_KEY"):
                url += "&api_key=" + urllib.parse.quote(os.environ["OPENALEX_API_KEY"])
            d = self.get("openalex", url + (f"&mailto={mt}" if self.mailto else ""))
            return [_rec(w.get("display_name") or w.get("title"),
                         [(a.get("author") or {}).get("display_name", "") for a in w.get("authorships", [])],
                         w.get("publication_year"),
                         (((w.get("primary_location") or {}).get("source")) or {}).get("display_name"))
                    for w in (d or {}).get("results", [])]
        if step == "dblp":
            d = self.get("dblp", f"https://dblp.org/search/publ/api?q={q}&format=json&h=3")
            out = []
            for h in (((d or {}).get("result") or {}).get("hits") or {}).get("hit", []):
                info = h.get("info", {})
                au = (info.get("authors") or {}).get("author", [])
                au = au if isinstance(au, list) else [au]
                yr = str(info.get("year", ""))
                out.append(_rec(info.get("title", "").rstrip("."), [a.get("text", "") if isinstance(a, dict) else a
                                                                    for a in au],
                                int(yr) if yr.isdigit() else None, info.get("venue")))
            return out
        raise ValueError(step)

    # ------------------------------------------------------------ comparison
    @staticmethod
    def compare(e, rec, sim):
        cited = [k for k in (name_key(a) for a in e["authors"]) if k]
        true = [k for k in (name_key(a) for a in rec["authors"]) if k]
        tokens = {re.sub(r"[^a-z]", "", t) for a in rec["authors"] for t in deaccent(a).lower().split()}

        def same(k, t):
            return k == t or (min(len(k), len(t)) >= 4 and (k.endswith(t) or t.endswith(k)))

        def found(k):
            return any(same(k, t) for t in true) or k in tokens
        m = {"title_sim": sim, "true_title": rec["title"], "n_cited_authors": len(cited), "n_true_authors": len(true),
             "author_overlap": round(sum(found(k) for k in cited) / len(cited), 2) if cited and true else None,
             "first_author_match": same(cited[0], true[0]) if cited and true else None,
             "last_author_match": (None if e["truncated"] or not cited or not true else same(cited[-1], true[-1])),
             "year_diff": (e["year"] - rec["year"]) if e["year"] and rec["year"] else None}
        m["missing_authors"] = [a for a in e["authors"] if name_key(a) and not found(name_key(a))]
        return m

    @staticmethod
    def judge(e, m):
        ov, notes = m["author_overlap"], []
        if ov is None:
            return "ok", ["authors not compared (none parsed or none returned); title-only check"]
        if ov < 0.6:
            return "suspicious", [f"author overlap {ov:.0%} < 60%"]
        if m["last_author_match"] is False and m["n_cited_authors"] >= 4 and ov < 0.8:
            return "suspicious", ["head correct, tail does not match (last author wrong, overlap < 80%)"]
        if m["year_diff"]:
            notes.append(f"year off by {m['year_diff']:+d}")
        if m["title_sim"] < 0.97:
            notes.append("minor title drift")
        if ov < 1.0 or m["first_author_match"] is False or m["last_author_match"] is False:
            notes.append("author list differs slightly")
        if not e["truncated"] and m["n_cited_authors"] != m["n_true_authors"]:
            notes.append(f"{m['n_cited_authors']} cited vs {m['n_true_authors']} indexed authors")
        return ("benign_error" if notes else "ok"), notes

    def check(self, e):
        res = {"id": e["id"], "title": e["title"], "found_in": [], "verdict": "unchecked", "notes": list(e["flags"]),
               "best_title_sim": None, "author_overlap": None, "first_author_match": None, "last_author_match": None,
               "n_cited_authors": len(e["authors"]), "n_true_authors": None, "year_diff": None,
               "truncated_et_al": e["truncated"]}
        if len(norm_title(e["title"])) < 8:
            res["notes"].append("no title parsed")
            return res
        matches, tried, confirming = [], set(), False
        for step, base in self.STEPS:
            if (step == "arxiv_id" and not e["arxiv"]) or (step == "crossref_doi" and not e["doi"]):
                continue
            if base in self.unreachable or any(mm["source"] == base for mm in matches):
                continue
            try:
                recs = self.search(step, e)
            except SourceUnavailable:
                continue
            tried.add(base)
            scored = sorted(((title_sim(e["title"], r["title"]), r) for r in recs), key=lambda x: -x[0])
            if scored and scored[0][0] >= TITLE_MATCH:
                mm = self.compare(e, scored[0][1], scored[0][0])
                mm["source"] = base
                mm["verdict"], mm["notes"] = self.judge(e, mm)
                matches.append(mm)
            elif step == "arxiv_id" and scored:
                res["notes"].append(f"arXiv {e['arxiv']} resolves to a different title: {scored[0][1]['title'][:60]}")
            if confirming and len(matches) >= 2:  # a second database has the paper: done
                break
            if matches:
                if matches[0]["verdict"] != "suspicious":
                    break
                confirming = True
        if matches:
            best = max(matches, key=lambda mm: (mm["author_overlap"] or 0, mm["title_sim"]))
            for k in ("author_overlap", "first_author_match", "last_author_match", "n_cited_authors",
                      "n_true_authors", "year_diff"):
                res[k] = best[k]
            res.update(found_in=[mm["source"] for mm in matches], best_title_sim=best["title_sim"],
                       verdict=best["verdict"], missing_authors=best["missing_authors"])
            res["notes"] += best["notes"]
            odd = [mm["source"] for mm in matches if mm["verdict"] == "suspicious" and mm is not best]
            if odd and best["verdict"] != "suspicious":
                res["notes"].append("same-title record with other authors in " + ", ".join(odd) + " (homonymous title?)")
            if best["verdict"] == "suspicious":
                n = sum(mm["verdict"] == "suspicious" for mm in matches)
                res["notes"].append(f"suspicious in {n} database(s)" + ("" if n >= 2 else "; confirm in a second one"))
        elif not tried:
            res["notes"].append("no source reachable")
        elif ML_VENUE.search(e["venue"] + " " + e["raw"]) and not (tried & {"s2", "openalex", "dblp"}):
            res["verdict"] = "not_found_in_reachable_sources"
            res["notes"].append(ML_NOTE)
        else:
            res["verdict"] = "not_found"
            res["notes"].append("searched: " + ", ".join(sorted(tried)) + "; confirm on the venue site before flagging")
        return res


# ---------------------------------------------------------------- report
def fmt(v):
    if v is None:
        return "–"
    if isinstance(v, bool):
        return "yes" if v else "**no**"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def markdown_report(path, results, n_total, dropped, ver):
    lines = [f"# Reference check: {os.path.basename(path)}", "", HEADER, "",
             "| id | title | found in | title sim | author overlap | first | last | cited/indexed | Δyear | verdict | notes |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        t = (r["title"][:70] + "…") if len(r["title"]) > 70 else r["title"]
        cnt = f"{r['n_cited_authors']}{'+et al.' if r['truncated_et_al'] else ''}/{fmt(r['n_true_authors'])}"
        v = f"**{r['verdict']}**" if r["verdict"] not in ("ok", "benign_error") else r["verdict"]
        notes = "; ".join(r["notes"])
        if r.get("missing_authors") and r["verdict"] == "suspicious":
            notes += "; unmatched: " + ", ".join(r["missing_authors"][:8])
        lines.append("| " + " | ".join(str(x).replace("|", "/") for x in (
            r["id"], t, ", ".join(r["found_in"]) or "–", fmt(r["best_title_sim"]), fmt(r["author_overlap"]),
            fmt(r["first_author_match"]), fmt(r["last_author_match"]), cnt, fmt(r["year_diff"]), v, notes)) + " |")
    counts = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    lines += ["", "## Summary", "",
              f"- Checked {len(results)} of {n_total} entries" + (f"; dropped {dropped} duplicated entries" if dropped else ""),
              "- Verdicts: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
              "- Reachable sources: " + (", ".join(sorted(ver.reachable)) or "none"),
              "- Unreachable sources: " + (", ".join(f"{k} ({v})" for k, v in ver.unreachable.items()) or "none")]
    if any(r["verdict"] == "suspicious" for r in results):
        lines.append("- Suspicious = title found but the cited author list does not match; verify against the "
                     "publisher page and a second database before recording P03.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("refs")
    ap.add_argument("--sample", type=int)
    ap.add_argument("--ids")
    ap.add_argument("--cache", default=os.path.join(os.path.expanduser("~"), ".cache", "absent-author", "ref_cache.json"))
    ap.add_argument("--mailto", default=os.environ.get("MAILTO", ""))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-o", "--output")
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args(argv)
    entries, dropped = load_entries(a.refs)
    sel = entries
    if a.ids:
        want = {x.strip() for x in a.ids.split(",")}
        sel = [e for e in sel if e["id"] in want]
    if a.sample:
        sel = select_sample(sel, a.sample)
    if a.offline:
        if a.json:
            out = json.dumps({"n_entries": len(entries), "duplicates_dropped": dropped,
                              "entries": [{k: v for k, v in e.items() if k != "venue"} for e in sel]},
                             indent=1, ensure_ascii=False)
        else:
            out = f"{len(entries)} entries ({dropped} duplicates dropped)\n" + "\n".join(
                f"[{e['id']}] ({e['year']}) {len(e['authors'])} authors{' +et al.' if e['truncated'] else ''}"
                f"{' arXiv:' + e['arxiv'] if e['arxiv'] else ''}{' doi:' + e['doi'] if e['doi'] else ''}\n"
                f"    title:   {e['title']}\n    authors: {'; '.join(e['authors'])}" for e in sel) + "\n"
    else:
        cache = {}
        if a.cache and os.path.exists(a.cache):
            try:
                with open(a.cache, encoding="utf-8") as f:
                    cache = json.load(f)
            except ValueError:
                cache = {}
        ver = Verifier(cache=cache, mailto=a.mailto)
        results = []
        for e in sel:
            print(f"checking [{e['id']}] {e['title'][:60]}", file=sys.stderr)
            results.append(ver.check(e))
        if a.cache:
            os.makedirs(os.path.dirname(os.path.abspath(a.cache)), exist_ok=True)
            with open(a.cache, "w", encoding="utf-8") as f:
                json.dump(ver.cache, f)
        if a.json:
            out = json.dumps({"header": HEADER, "n_entries": len(entries), "duplicates_dropped": dropped,
                              "reachable": sorted(ver.reachable), "unreachable": ver.unreachable,
                              "results": results}, indent=1, ensure_ascii=False)
        else:
            out = markdown_report(a.refs, results, len(entries), dropped, ver)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
