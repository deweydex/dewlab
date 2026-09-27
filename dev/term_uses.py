"""Where a later page might mark a term it inherited, for an author to decide.

A term shows its definition on hover only where the author marked it: the
italicised first use, or a later use written `*term*{.term}`
(docs/WRITING_TUTORIALS.md#marking-a-term, DECISIONS_LOG 7.273). Nothing
marks a later use automatically, because a word match cannot tell the
everyday "set a seed" from a set (7.94). This lists the candidates instead:
for each built page, each concept it inherits from an earlier page that
appears in its prose as a whole word, unmarked, with the sentence around
the first appearance. An author reads each and marks the ones that mean the
term.

Prose is what the author wrote: a cell, with its label and report panel,
and a predict block's buttons are left out. A longer term holding a shorter
one wins ("selection sort" is not a use of "selection"), and a term with a
capital (None, ASCII) is matched as written, so "there is none" is not None.
A plain plural counts, so a page that only says "functions" lists *function*.

Reads the built site, so run `python3 build.py` first.

    python3 dev/term_uses.py                 # every page
    python3 dev/term_uses.py doubling-and-halving
    python3 dev/term_uses.py --check         # marks to look at
    python3 dev/term_uses.py --common        # terms marked only near the start

`--common` lists, for each course, the terms marked only near the start
(7.281): the site's own words (cell, toolkit, illustration) and any term
the course uses on three in five of its pages after introducing it. They
are marked only on the tutorial that introduces them and the next three,
with their practice pages, and the candidate list leaves them out after
that.

`--check` lists every `{.term}` mark the page would show no definition for:
its words are not a concept in that page's glossary, or they are two
concepts' (a table's frequency and a wave's) and neither is the page's own.
It also lists a mark on a term past its start, in every course that lists
the page.
Either the word or the glossary needs a look. It matches more strictly than the page does (no
stemming beyond a plural), so a listed mark may still work; open the page
to be sure.
"""

from __future__ import annotations

import html
import json
from html.parser import HTMLParser
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site" / "tutorials"
MANIFEST_RE = re.compile(r'<script type="application/json" id="dewlab-manifest">(.*?)</script>', re.S)
BODY_RE = re.compile(r'<main[^>]*id="dl-body"[^>]*>(.*?)</main>', re.S)
# What is never prose: code, cells, maths, headings, links, anything already
# in italics (marked, or stress the author chose), and the words the page
# adds round the author's own: a cell's label and report panel, and a predict
# block's buttons. Those say "cell" on every page, so leaving them in would
# list "cell" everywhere.
SKIP_TAGS = {"pre", "code", "script", "style", "h1", "h2", "h3", "h4", "h5", "h6",
             "a", "em", "summary", "button"}
SKIP_CLASSES = {"dl-cell", "dl-math", "dl-predict-sure", "dl-predict-unsure",
                "dl-predict-after", "dl-predict-footer", "dl-compare", "dl-world-chooser"}
TAG_RE = re.compile(r"<[^>]+>")
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
             "meta", "source", "track", "wbr"}


class _Prose(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skipping: tuple[str, int] | None = None  # (tag, depth of that tag)

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        if self.skipping:
            if tag == self.skipping[0]:
                self.skipping = (tag, self.skipping[1] + 1)
            return
        classes = set((dict(attrs).get("class") or "").split())
        if tag in SKIP_TAGS or classes & SKIP_CLASSES:
            self.skipping = (tag, 1)
        else:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if self.skipping and tag == self.skipping[0]:
            depth = self.skipping[1] - 1
            self.skipping = (tag, depth) if depth else None
            if not depth:
                self.parts.append(" ")
        elif not self.skipping:
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.skipping:
            self.parts.append(data)

# assets/search-words.js's STOPWORDS: a comma part that is only one of these
# names nothing (term-definitions.js drops it the same way).
STOPWORDS = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is",
             "are", "with", "by", "at", "from", "your", "what", "how"}

ROOT = Path(__file__).resolve().parent.parent
# Two kinds of term are marked only near the start (DECISIONS_LOG 7.281): the
# site's own furniture, which a reader uses on every page, and a term a
# course uses on three in five of its pages after introducing it. Meeting either
# every page or two keeps it fresh; a definition on the fortieth page is
# clutter. "Near the start" is the tutorial that introduces it and the next
# three, with their practice pages.
APP_WORDS = {"cell", "toolkit", "illustration"}
COMMON_SHARE = 0.6
COMMON_MIN_PAGES = 10
WINDOW = 4


def _names(term: str) -> set[str]:
    parts = {p.strip().lower() for p in term.split(",")} | {term.strip().lower()}
    return {p for p in parts if len(p) >= 3} - STOPWORDS


def _singulars(word: str) -> set[str]:
    word = word.lower()
    return {word, word[:-1] if word.endswith("s") else word, word[:-2] if word.endswith("es") else word}


def course_orders() -> dict[str, list[str]]:
    """Each course's title and its tutorials, in order."""
    import yaml

    orders = {}
    for path in sorted((ROOT / "courses").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("contents"):
            orders[data.get("title", path.stem)] = [
                slug for series in data["contents"] for slug in (series.get("tutorials") or [])
            ]
    return orders


def introductions() -> dict[str, set[str]]:
    """Each concept name, and the tutorials whose own glossary defines it."""
    import yaml

    found: dict[str, set[str]] = {}
    for path in (ROOT / "tutorials").glob("*/*.glossary.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for entry in data.get("entries") or []:
            if isinstance(entry, dict) and entry.get("kind", "concept") == "concept" and entry.get("term"):
                for name in _names(str(entry["term"])):
                    found.setdefault(name, set()).add(path.parent.name)
    return found


_WORDS: dict[str, str] = {}


def page_words(slug: str) -> str:
    """A built page's prose, lower case, with its marked later uses counted."""
    if slug not in _WORDS:
        path = SITE / f"{slug}.html"
        text = path.read_text(encoding="utf-8").replace('<em class="term">', "<span>") if path.exists() else ""
        _WORDS[slug] = re.sub(r"\s+", " ", prose(text)).lower()
    return _WORDS[slug]


def _pages(tutorials: list[str]) -> list[tuple[str, str]]:
    return [(tutorial, slug) for tutorial in tutorials for slug in (tutorial, f"{tutorial}-practice")
            if (SITE / f"{slug}.html").exists()]


_WINDOWS: dict[str, dict[str, tuple[set[str], float]]] | None = None


def windows() -> dict[str, dict[str, tuple[set[str], float]]]:
    """For each course, each term marked only near the start: the pages where
    it may be marked, and the share of later pages that use it."""
    global _WINDOWS
    if _WINDOWS is None:
        _WINDOWS = {}
        intro = introductions()
        for course, order in course_orders().items():
            pages = _pages(order)
            found = {}
            for name, homes in intro.items():
                starts = [i for i, slug in enumerate(order) if slug in homes]
                if not starts:
                    continue
                start = starts[0]
                window = {slug for tutorial, slug in _pages(order[start:start + WINDOW])}
                later = [slug for tutorial, slug in pages if order.index(tutorial) > start]
                pattern = re.compile(rf"\b{re.escape(name)}(s|es)?\b")
                share = sum(bool(pattern.search(page_words(slug))) for slug in later) / len(later) if later else 0
                if name in APP_WORDS or (len(later) >= COMMON_MIN_PAGES and share >= COMMON_SHARE):
                    found[name] = (window, share)
            _WINDOWS[course] = found
    return _WINDOWS


def after_its_start(slug: str, word: str) -> bool:
    """Whether page `slug` is past the start of the term `word` in every
    course that lists it. A course that does not mark the term only near
    the start wants it marked everywhere, so it keeps the mark."""
    tutorial = slug[: -len("-practice")] if slug.endswith("-practice") else slug
    listed = False
    for course, order in course_orders().items():
        if tutorial not in order:
            continue
        listed = True
        window = next((w for name, (w, share) in windows()[course].items() if name in _singulars(word)), None)
        if window is None or slug in window:
            return False
    return listed


def prose(page_html: str) -> str:
    match = BODY_RE.search(page_html)
    parser = _Prose()
    parser.feed(match.group(1) if match else page_html)
    return "".join(parser.parts)


def candidates(page: Path) -> list[tuple[str, int, str]]:
    text = page.read_text(encoding="utf-8")
    found = MANIFEST_RE.search(text)
    if not found:
        return []
    manifest = json.loads(found.group(1))
    concepts = [e for e in manifest.get("glossary") or [] if e.get("kind") == "concept"]
    words = re.sub(r"\s+", " ", prose(text))
    every = [part.strip() for entry in concepts for part in entry["term"].split(",")]
    names = [part.strip() for entry in concepts if entry.get("origin") for part in entry["term"].split(",")]
    rows = []
    for name in names:
        # "order of not, and, or" is one term; a bare "and" is not a name.
        if len(name) < 3 or name.lower() in STOPWORDS or after_its_start(page.stem, name):
            continue
        # A longer term that holds this one wins: "selection sort" is not a
        # use of "selection". A name with a capital (None, ASCII) is matched
        # as written, so "there is none" is not None.
        searched = words
        for longer in every:
            if len(longer) > len(name) and re.search(rf"\b{re.escape(name)}\b", longer, re.I):
                searched = re.sub(rf"\b{re.escape(longer)}\b", " ", searched, flags=re.I)
        flags = 0 if name != name.lower() else re.I
        uses = list(re.finditer(rf"\b{re.escape(name)}(s|es)?\b", searched, flags))
        if uses:
            first = uses[0]
            around = searched[max(0, first.start() - 60): first.end() + 60].strip()
            rows.append((name, len(uses), around))
    return rows


MARK_RE = re.compile(r'<em class="term">(.*?)</em>|<strong class="term"><em>(.*?)</em></strong>', re.S)


def unmatched_marks(page: Path) -> list[str]:
    """Each `{.term}` mark to look at, as "word (why)": one the page would
    show no definition for (naming no concept, or naming two with neither
    the page's own, as term-definitions.js's pick() decides), or one on a
    term marked only near the start, past that start."""
    text = page.read_text(encoding="utf-8")
    found = MANIFEST_RE.search(text)
    entries = []
    if found:
        for entry in json.loads(found.group(1)).get("glossary") or []:
            if entry.get("kind") == "concept":
                names = ({p.strip().lower() for p in entry["term"].split(",")}
                         | {entry["term"].strip().lower()}) - STOPWORDS
                entries.append((names, bool(entry.get("origin"))))
    bad = []
    for plain, bold in MARK_RE.findall(text):
        word = re.sub(r"\s+", " ", html.unescape(TAG_RE.sub("", plain or bold))).strip().lower()
        singulars = {word, word[:-1] if word.endswith("s") else word, word[:-2] if word.endswith("es") else word}
        matches = [inherited for names, inherited in entries if singulars & names]
        if after_its_start(page.stem, word):
            bad.append(f"{word} (marked after its first pages)")
        elif not matches:
            bad.append(f"{word} (names no concept)")
        elif len(matches) > 1 and [inherited for inherited in matches if not inherited] != [False]:
            bad.append(f"{word} (names {len(matches)} concepts)")
    return bad


def check(pages: list[Path]) -> int:
    problems = 0
    for page in pages:
        for word in unmatched_marks(page):
            problems += 1
            print(f"{page.stem}: {word}")
    print(f"{problems} marks to look at.")
    return 1 if problems else 0


def main(argv: list[str]) -> int:
    if not SITE.exists():
        print("No built site: run `python3 build.py` first.", file=sys.stderr)
        return 1
    if argv[:1] == ["--common"]:
        for course, found in windows().items():
            if found:
                print(f"\n{course}")
                for name, (window, share) in sorted(found.items(), key=lambda item: -item[1][1]):
                    why = "the site's own" if name in APP_WORDS else f"on {share:.0%} of later pages"
                    first = sorted({slug.removesuffix("-practice") for slug in window}, key=course_orders()[course].index)
                    print(f"  {name} ({why}): marked only on {', '.join(first)}")
        return 0
    if argv[:1] == ["--check"]:
        rest = argv[1:]
        return check([SITE / f"{slug}.html" for slug in rest] if rest else sorted(SITE.glob("*.html")))
    pages = [SITE / f"{slug}.html" for slug in argv] if argv else sorted(SITE.glob("*.html"))
    total = 0
    for page in pages:
        if not page.exists():
            print(f"\n{page.stem}: no such page in site/tutorials", file=sys.stderr)
            continue
        rows = candidates(page)
        if not rows:
            continue
        print(f"\n{page.stem}")
        for name, count, around in rows:
            total += 1
            print(f"  {name} ({count}×): …{around}…")
    print(f"\n{total} candidates. Mark the ones that mean the term: *{{word}}*{{.term}}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
