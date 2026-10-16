"""Where each block of a rendered page came from in its markdown file.

The in-page editor (planning/IN_PAGE_EDITOR.md) edits one block at a time and
writes it back over the exact bytes it came from. That needs the build to say,
for every top-level block of a page, which range of the file produced it.
Python-Markdown records no positions, so this module does it from outside:

1. `blocks()` splits a page's markdown body into its top-level blocks the way
   Python-Markdown would see them, each with a start and end offset.
2. `mark()` puts an HTML comment, `<!--dl-src:START:END-->`, on the line before
   each block. Python-Markdown passes a comment between blank lines through
   untouched, so it reaches the finished page in front of the element the block
   became.
3. `attach()` turns each comment into a `data-md="START:END"` attribute on that
   element, and removes any comment with nothing to attach to (a block that
   renders to nothing, such as a link reference definition).

Offsets are into the file as committed, including the frontmatter, because that
is what the editor splices into. `splice()` is that splice.

Nothing here changes how a page reads. `tests/build/test_source_map.py` checks
that, across every tutorial: the page built with markers and stripped of its
`data-md` attributes is the page built without them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from markdown.util import BLOCK_LEVEL_ELEMENTS

MARKER_RE = re.compile(r"<!--dl-src:(\d+):(\d+)-->")
ATTR_RE = re.compile(r' data-md="\d+:\d+"')

FENCE_RE = re.compile(r"^ *```(?P<info>[^\n]*)$")
HTML_OPEN_RE = re.compile(r"^ {0,3}<(?P<tag>[a-zA-Z][a-zA-Z0-9]*)\b")
LIST_ITEM_RE = re.compile(r"^ *([-*+]|\d+[.)])[ \t]+")
ATX_RE = re.compile(r"^ {0,3}#{1,6}([ \t]|$)")
QUOTE_RE = re.compile(r"^ {0,3}>")
BLOCK_TAGS = {name.lower() for name in BLOCK_LEVEL_ELEMENTS}

# A fence of one of these belongs to the cell above it, so it is part of that
# cell's block: the editor shows a cell and its hint, solution and inputs as
# one thing (build.py extract_blocks() attaches them the same way).
ATTACHED = {"hint", "solution", "inputs", "typed", "predict"}


@dataclass
class Block:
    start: int
    end: int
    kind: str


def _fence_kind(info: str, body: str = "") -> str:
    words = info.split()
    if not words:
        return "fence:code"
    if words[0] in ("html", "css", "js") and ("site" in words or "app" in words):
        which = "site" if "site" in words else "app"
        named = re.search(rf"^{which}:[ \t]*(\S+)", body, re.MULTILINE)
        return f"fence:{which}:{named.group(1) if named else ''}"
    if "exec" in words:
        return "fence:cell"
    if "toolkit-reference" in words:
        return "fence:toolkit-reference"
    return f"fence:{words[0]}"


def blocks(body: str) -> list[Block]:
    """The top-level blocks of `body`, with offsets into `body`."""
    lines = body.split("\n")
    starts: list[int] = []
    at = 0
    for line in lines:
        starts.append(at)
        at += len(line) + 1

    out: list[Block] = []
    i = 0
    n = len(lines)

    def fence_end(index: int) -> int:
        """Index of the line that closes the fence opened at `index`."""
        j = index + 1
        while j < n and not re.match(r"^ *```[ \t]*$", lines[j]):
            j += 1
        return min(j, n - 1)

    def end_of(index: int) -> int:
        """Offset just past the last character of line `index`."""
        return starts[index] + len(lines[index])

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        first = i

        fence = FENCE_RE.match(line)
        if fence:
            j = i + 1
            while j < n and not re.match(r"^ *```[ \t]*$", lines[j]):
                j += 1
            last = min(j, n - 1)
            kind = _fence_kind(fence.group("info"), "\n".join(lines[i + 1:last]))
            if out and out[-1].kind == "list" and re.match(r"^ {2,}", line):
                # Indented under a list item: part of the list, not a block.
                out[-1].end = end_of(last)
            else:
                _add(out, starts[first], end_of(last), kind)
            i = last + 1
            continue

        if line.lstrip().startswith("<!--"):
            j = i
            while j < n and "-->" not in lines[j]:
                j += 1
            last = min(j, n - 1)
            _add(out, starts[first], end_of(last), "comment")
            i = last + 1
            continue

        opener = HTML_OPEN_RE.match(line)
        if opener and opener.group("tag").lower() in BLOCK_TAGS:
            tag = opener.group("tag")
            open_re = re.compile(rf"<{tag}\b[^>]*?(?<!/)>", re.IGNORECASE)
            close_re = re.compile(rf"</{tag}\s*>", re.IGNORECASE)
            depth = 0
            j = i
            closed = False
            in_fence = False
            while j < n:
                if re.match(r"^ *```", lines[j]):
                    # Tags shown inside a code fence are text, not structure.
                    in_fence = not in_fence
                elif not in_fence:
                    code_free = re.sub(r"`[^`]*`", "", lines[j])  # `<tag>` in prose is text
                    depth += len(open_re.findall(code_free)) - len(close_re.findall(code_free))
                    if depth <= 0:
                        closed = True
                        break
                j += 1
            if not closed:
                # Unbalanced: Python-Markdown reads to the blank line.
                j = i
                while j + 1 < n and lines[j + 1].strip():
                    j += 1
            kind = f"html:{tag.lower()}"
            if tag.lower() == "div" and re.search(r'class="dl-world"', line):
                kind = "html:world"
            _add(out, starts[first], end_of(min(j, n - 1)), kind)
            i = min(j, n - 1) + 1
            continue

        if ATX_RE.match(line):
            _add(out, starts[first], end_of(i), "heading")
            i += 1
            continue

        kind = _prose_kind(line)
        j = i
        in_math = False
        while True:
            in_math ^= (lines[j].count("$$") % 2 == 1)
            nxt = j + 1
            if nxt >= n:
                break
            if lines[nxt].strip():
                if FENCE_RE.match(lines[nxt]) and kind == "list" and re.match(r"^ {2,}", lines[nxt]):
                    j = fence_end(nxt)  # a fence inside a list item, taken whole
                    continue
                if FENCE_RE.match(lines[nxt]) or ATX_RE.match(lines[nxt]):
                    break
                if kind == "paragraph" and re.match(r" {0,3}([-*+]|\d+[.)])[ \t]+\S", lines[nxt]):
                    # A list that starts on the line after a paragraph line is
                    # its own block, as the finished page shows it.
                    break
                j = nxt
                continue
            if in_math:
                j = nxt
                continue
            # A blank line: does the same block carry on after it?
            k = nxt
            while k < n and not lines[k].strip():
                k += 1
            if k >= n:
                break
            after = lines[k]
            if kind == "list" and (LIST_ITEM_RE.match(after) or re.match(r"^ {2,}\S", after)):
                j = fence_end(k) if FENCE_RE.match(after) else k
                continue
            if kind == "quote" and QUOTE_RE.match(after):
                j = k
                continue
            if kind == "indented" and re.match(r"^( {4}|\t)", after):
                j = k
                continue
            break
        if kind == "paragraph" and j > first and re.match(r"^(=+|-+)[ \t]*$", lines[j]):
            kind = "heading"  # a setext heading: the text, underlined
        _add(out, starts[first], end_of(j), kind)
        i = j + 1
    return out


def _prose_kind(line: str) -> str:
    if LIST_ITEM_RE.match(line):
        return "list"
    if QUOTE_RE.match(line):
        return "quote"
    if re.match(r"^( {4}|\t)", line):
        return "indented"
    if line.lstrip().startswith("|"):
        return "table"
    return "paragraph"


# Blocks the build keeps together by adjacency: the html, css and js panes of
# one site editor or full-stack cell (it refuses panes that are not
# consecutive), and the world variants of one task (place_worlds() groups
# siblings). A marker between them would split the group.
GROUPED_PREFIXES = ("fence:site:", "fence:app:")
GROUPED_KINDS = {"html:world"}


def _add(out: list[Block], start: int, end: int, kind: str) -> None:
    word = kind.split(":", 1)[1] if kind.startswith("fence:") else ""
    if word in ATTACHED and out and out[-1].kind == "fence:cell":
        out[-1].end = end
        return
    if out and out[-1].kind == kind and (kind in GROUPED_KINDS or kind.startswith(GROUPED_PREFIXES)):
        out[-1].end = end
        return
    out.append(Block(start, end, kind))


def mark(body: str, base: int = 0) -> str:
    """`body` with a marker comment before each block that renders something.

    `base` is where `body` begins in the file, so the offsets in the markers
    are file offsets. Comments and nothing else are added, each followed by a
    blank line.
    """
    pieces: list[str] = []
    at = 0
    for block in blocks(body):
        if block.kind == "comment":
            continue
        pieces.append(body[at:block.start])
        pieces.append(f"<!--dl-src:{base + block.start}:{base + block.end}-->\n\n")
        at = block.start
    pieces.append(body[at:])
    return "".join(pieces)


_TAG_RE = re.compile(r"<[a-zA-Z][^>]*?(?=/?>)")


def attach(page: str) -> str:
    """Turn each marker comment into `data-md` on the element after it.

    A marker followed by anything but an opening tag (another marker, because
    its own block rendered nothing, or text) is dropped.
    """
    out: list[str] = []
    at = 0
    for match in MARKER_RE.finditer(page):
        out.append(page[at:match.start()])
        at = match.end()
        rest = page[at:]
        gap = len(rest) - len(rest.lstrip())
        # The blank lines after the marker go with it, so the page reads
        # exactly as it would have without one.
        at += gap
        tag = _TAG_RE.match(page, at)
        if not tag:
            continue
        out.append(tag.group(0))
        out.append(f' data-md="{match.group(1)}:{match.group(2)}"')
        at = tag.end()
    out.append(page[at:])
    return "".join(out)


EDIT_RE = re.compile(r',\s*"edit":\s*\{[^{}]*\}')


def strip(page: str) -> str:
    """The page without any trace of the map, for comparing with one built
    without it. That includes the `edit` entry a mapped page's manifest carries,
    which names the file and blob the ranges point into."""
    page = EDIT_RE.sub("", ATTR_RE.sub("", page))
    return re.sub(MARKER_RE.pattern + r"\s*", "", page)


def splice(text: str, edits: list[tuple[int, int, str]]) -> str:
    """Apply `(start, end, replacement)` edits to `text`, last first so that
    earlier offsets stay true. Edits must not overlap."""
    ordered = sorted(edits, key=lambda e: e[0])
    for (s1, e1, _), (s2, _e2, _) in zip(ordered, ordered[1:]):
        if e1 > s2:
            raise ValueError(f"edits overlap: {s1}:{e1} and {s2}")
    for start, end, replacement in reversed(ordered):
        text = text[:start] + replacement + text[end:]
    return text
