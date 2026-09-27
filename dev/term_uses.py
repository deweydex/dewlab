"""Where a later page might mark a term it inherited, for an author to decide.

A term shows its definition on hover only where the author marked it: the
italicised first use, or a later use written `*term*{.term}`
(docs/WRITING_TUTORIALS.md#marking-a-term, DECISIONS_LOG 7.272). Nothing
marks a later use automatically, because a word match cannot tell the
everyday "set a seed" from a set (7.94). This lists the candidates instead:
for each built page, each concept it inherits from an earlier page that
appears in its prose as a whole word, unmarked, with the sentence around
the first appearance. An author reads each and marks the ones that mean the
term.

Reads the built site, so run `python3 build.py` first.

    python3 dev/term_uses.py                 # every page
    python3 dev/term_uses.py doubling-and-halving
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site" / "tutorials"
MANIFEST_RE = re.compile(r'<script type="application/json" id="dewlab-manifest">(.*?)</script>', re.S)
BODY_RE = re.compile(r'<main[^>]*id="dl-body"[^>]*>(.*?)</main>', re.S)
# What is never prose: code, cells, maths, headings, links, and anything
# already in italics (marked, or stress the author chose).
NOT_PROSE_RE = re.compile(
    r"<(pre|code|script|style|h[1-6]|a|em|summary|button)\b.*?</\1>"
    r'|<span class="dl-math[^"]*">.*?</span>',
    re.S,
)
TAG_RE = re.compile(r"<[^>]+>")


def prose(page_html: str) -> str:
    match = BODY_RE.search(page_html)
    body = match.group(1) if match else page_html
    body = NOT_PROSE_RE.sub(" ", body)
    return html.unescape(TAG_RE.sub(" ", body))


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


def main(argv: list[str]) -> int:
    if not SITE.exists():
        print("No built site: run `python3 build.py` first.", file=sys.stderr)
        return 1
    pages = [SITE / f"{slug}.html" for slug in argv] if argv else sorted(SITE.glob("*.html"))
    total = 0
    for page in pages:
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
