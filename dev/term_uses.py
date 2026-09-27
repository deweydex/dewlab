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

Reads the built site, so run `python3 build.py` first.

    python3 dev/term_uses.py                 # every page
    python3 dev/term_uses.py doubling-and-halving
    python3 dev/term_uses.py --check         # marks that name no term

`--check` lists every `{.term}` mark whose words are not a concept in that
page's glossary. The page would show nothing for it, so either the word or
the glossary needs a look. It matches more strictly than the page does (no
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
    inherited = [e for e in manifest.get("glossary") or [] if e.get("kind") == "concept" and e.get("origin")]
    words = re.sub(r"\s+", " ", prose(text))
    rows = []
    for entry in inherited:
        for name in (part.strip() for part in entry["term"].split(",")):
            if len(name) < 3:
                continue
            uses = list(re.finditer(rf"\b{re.escape(name)}\b", words, re.I))
            if uses:
                first = uses[0]
                around = words[max(0, first.start() - 60): first.end() + 60].strip()
                rows.append((name, len(uses), around))
    return rows


MARK_RE = re.compile(r'<em class="term">(.*?)</em>|<strong class="term"><em>(.*?)</em></strong>', re.S)


def unmatched_marks(page: Path) -> list[str]:
    text = page.read_text(encoding="utf-8")
    found = MANIFEST_RE.search(text)
    names = set()
    if found:
        for entry in json.loads(found.group(1)).get("glossary") or []:
            if entry.get("kind") == "concept":
                names.update(part.strip().lower() for part in entry["term"].split(","))
    bad = []
    for plain, bold in MARK_RE.findall(text):
        word = re.sub(r"\s+", " ", html.unescape(TAG_RE.sub("", plain or bold))).strip().lower()
        singulars = {word, word[:-1] if word.endswith("s") else word, word[:-2] if word.endswith("es") else word}
        if not singulars & names:
            bad.append(word)
    return bad


def check(pages: list[Path]) -> int:
    problems = 0
    for page in pages:
        for word in unmatched_marks(page):
            problems += 1
            print(f"{page.stem}: *{word}*{{.term}} names no concept in this page's glossary")
    print(f"{problems} marks name no term.")
    return 1 if problems else 0


def main(argv: list[str]) -> int:
    if not SITE.exists():
        print("No built site: run `python3 build.py` first.", file=sys.stderr)
        return 1
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
