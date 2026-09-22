#!/usr/bin/env python3
"""The drawn diagrams Web Authoring's Welcome series uses, and where each goes.

    python3 dev/graphics/web_welcome.py          # report what would change
    python3 dev/graphics/web_welcome.py --write  # write it

The Welcome pages have no live cells: they are about where a file goes
between an editor and a visitor's screen. So every picture here is a
picture of places and of the steps between them — the path one change
takes, the two loops a change goes round, the parts of a web address, the
requests a browser makes, and a line of commits. Each is drawn in the
palette's tokens and inlined by the build, so it follows the reader's
theme like the rest of the page.

Same rule as the other generators here: where a picture names a page's own
example (the address `janedoe.github.io/web`), the words in it are the
words the page uses.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (  # noqa: E402
    FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, PAPER, SANS,
)

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL_PT = 12
SMALL_PT = 10.5
TITLE_PT = 13
HEAD = 7               # an arrowhead's length


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _head(drawing, group, x: float, y: float, angle: float, colour: str = INK) -> None:
    """A filled arrowhead with its point at (x, y), pointing along `angle` (radians)."""
    back = [(x - HEAD * math.cos(angle + turn), y - HEAD * math.sin(angle + turn))
            for turn in (0.42, -0.42)]
    group.add(drawing.polygon([(x, y), *back], fill=colour, stroke="none"))


def _arrow(drawing, group, start, end, *, dashed: bool = False, colour: str = INK) -> None:
    """A straight arrow from `start` to `end`, the head drawn at `end`."""
    (x1, y1), (x2, y2) = start, end
    angle = math.atan2(y2 - y1, x2 - x1)
    stop = (x2 - (HEAD - 1) * math.cos(angle), y2 - (HEAD - 1) * math.sin(angle))
    group.add(drawing.line(
        start=start, end=stop, stroke=colour, stroke_width=1.5,
        stroke_dasharray="5 4" if dashed else None))
    _head(drawing, group, x2, y2, angle, colour)


def _box(drawing, group, x: float, y: float, w: float, h: float, lines: list[str],
         *, fill: str = PAPER, bold_first: bool = True, mono: bool = False) -> None:
    """A labelled box: the first line in the label size, any others smaller."""
    group.add(drawing.rect(insert=(x, y), size=(w, h), fill=fill, stroke=INK,
                           stroke_width=1.3, rx=6))
    total = len(lines)
    for index, text in enumerate(lines):
        first = index == 0
        offset = (index - (total - 1) / 2) * 15
        group.add(drawing.text(
            text, insert=(x + w / 2, y + h / 2 + offset + 4), text_anchor="middle",
            font_size=f"{LABEL_PT if first else SMALL_PT}px",
            font_weight="bold" if first and bold_first else "normal",
            font_family=MONO if mono and first else SANS,
            fill=INK if first else MUTED))


def _text(drawing, group, text: str, x: float, y: float, *, size: float = SMALL_PT,
          anchor: str = "start", colour: str = INK, mono: bool = False,
          bold: bool = False) -> None:
    group.add(drawing.text(
        text, insert=(x, y), text_anchor=anchor, font_size=f"{size}px",
        font_family=MONO if mono else SANS, fill=colour,
        font_weight="bold" if bold else "normal"))


def path_of_a_change() -> str:
    """One change, from the editor to anyone's browser, in the page's five steps.

    Two bands, because the page's own point is that the path has two
    stages: everything in the top band happens on the student's computer,
    everything in the bottom band on GitHub. The numbers on the arrows are
    the numbers of the page's own list. The dashed route down the left is
    GitHub's editor, which puts a commit straight into the repository, so
    stage one and stage two happen together — the page says so in words,
    and the picture shows it as a short cut past steps 3 and 4.
    """
    col = [16, 226, 436]
    w, h = 150, 42
    width, height = col[2] + w + 16, 372
    drawing = _drawing(width, height)
    root = drawing.g()

    top_band, bottom_band = (6, 186), (196, 300)
    for (y0, y1), fill, title in (
        (top_band, FILL_BLUE, "Stage one: on your computer"),
        (bottom_band, FILL_GREEN, "Stage two: on GitHub"),
    ):
        root.add(drawing.rect(insert=(6, y0), size=(width - 12, y1 - y0), fill=fill,
                              stroke="none", rx=8))
        # The bottom title sits at the right, clear of the push arrow.
        right_side = fill == FILL_GREEN
        _text(drawing, root, title, width - 16 if right_side else 16, y0 + 20,
              size=TITLE_PT, bold=True, anchor="end" if right_side else "start")

    row_a, row_b, row_c, row_d = 44, 126, 236, 322
    _box(drawing, root, col[0], row_a, w, h, ["Your editor"])
    _box(drawing, root, col[1], row_a, w, h, ["The file", "saved on your computer"])
    _box(drawing, root, col[2], row_a, w, h, ["Your browser", "only you see it"])
    _box(drawing, root, col[1], row_b, w, h, ["A commit", "recorded by Git"])
    _box(drawing, root, col[1], row_c, w, h, ["Your repository"])
    _box(drawing, root, col[2], row_c, w, h, ["Your published site"])
    _box(drawing, root, col[2], row_d, w, h, ["Anyone's browser", "at your site's address"])

    mid_a, mid_c = row_a + h / 2, row_c + h / 2
    _arrow(drawing, root, (col[0] + w, mid_a), (col[1], mid_a))
    _text(drawing, root, "1 save", (col[0] + w + col[1]) / 2, mid_a - 7, anchor="middle")
    _arrow(drawing, root, (col[1] + w, mid_a), (col[2], mid_a))
    _text(drawing, root, "2 refresh", (col[1] + w + col[2]) / 2, mid_a - 7, anchor="middle")

    centre = col[1] + w / 2
    _arrow(drawing, root, (centre, row_a + h), (centre, row_b))
    _text(drawing, root, "3 commit", centre + 8, (row_a + h + row_b) / 2 + 4)
    _arrow(drawing, root, (centre, row_b + h), (centre, row_c))
    _text(drawing, root, "4 push", centre + 8, (row_b + h + row_c) / 2 + 8)

    _arrow(drawing, root, (col[1] + w, mid_c), (col[2], mid_c))
    _text(drawing, root, "5 publish", (col[1] + w + col[2]) / 2, mid_c - 7, anchor="middle")
    right = col[2] + w / 2
    _arrow(drawing, root, (right, row_c + h), (right, row_d))

    # GitHub's editor: straight from the editor into the repository.
    left = col[0] + w / 2
    root.add(drawing.polyline(
        [(left, row_a + h), (left, mid_c)], fill="none", stroke=INK,
        stroke_width=1.5, stroke_dasharray="5 4"))
    _arrow(drawing, root, (left, mid_c), (col[1], mid_c), dashed=True)
    _text(drawing, root, "GitHub's editor:", col[0] + 4, mid_c + 22)
    _text(drawing, root, "a commit goes straight here", col[0] + 4, mid_c + 36)

    drawing.add(root)
    return drawing.tostring()


def two_loops() -> str:
    """The two loops, side by side, and the step that joins them.

    Each loop is drawn as a real circle of steps with arrows round it,
    because the point of the word "loop" is that the last step leads back
    to the first. Under each, how long one turn takes: seconds on the
    student's computer, a minute or two on GitHub — the difference that
    makes "why is my change not showing?" worth asking.
    """
    width, height = 560, 330
    drawing = _drawing(width, height)
    root = drawing.g()
    radius, cy = 76, 158

    def loop(cx: float, title: str, steps: list[tuple[str, float]], note: tuple[str, str], fill: str) -> dict:
        root.add(drawing.circle(center=(cx, cy), r=radius + 30, fill=fill, stroke="none"))
        _text(drawing, root, title, cx, 30, size=TITLE_PT, anchor="middle", bold=True)
        places = {}
        angles = [a for _, a in steps]

        def pill_of(label: str) -> float:
            return 16 + len(label) * 7

        def gap_of(label: str) -> float:
            # The angle at which the circle leaves the pill, worst case
            # (a horizontal pill on a vertical stretch of the circle).
            return math.degrees(2 * math.asin((pill_of(label) / 2 + 4) / (2 * radius)))

        labels = [label for label, _ in steps]
        for index, (label, angle) in enumerate(steps):
            nxt = angles[(index + 1) % len(angles)]
            if nxt <= angle:
                nxt += 360
            after = labels[(index + 1) % len(labels)]
            a1, a2 = math.radians(angle + gap_of(label)), math.radians(nxt - gap_of(after))
            x1, y1 = cx + radius * math.cos(a1), cy + radius * math.sin(a1)
            x2, y2 = cx + radius * math.cos(a2), cy + radius * math.sin(a2)
            large = 1 if (nxt - angle - gap_of(label) - gap_of(after)) > 180 else 0
            root.add(drawing.path(
                d=f"M {x1:.1f} {y1:.1f} A {radius} {radius} 0 {large} 1 {x2:.1f} {y2:.1f}",
                fill="none", stroke=INK, stroke_width=1.5))
            _head(drawing, root, x2, y2, a2 + math.pi / 2)
        for label, angle in steps:
            a = math.radians(angle)
            x, y = cx + radius * math.cos(a), cy + radius * math.sin(a)
            pill = pill_of(label)
            root.add(drawing.rect(insert=(x - pill / 2, y - 12), size=(pill, 24),
                                  fill=PAPER, stroke=INK, stroke_width=1.3, rx=12))
            _text(drawing, root, label, x, y + 4, size=LABEL_PT, anchor="middle")
            places[label] = (x, y, pill)
        for line, words in enumerate(note):
            _text(drawing, root, words, cx, cy + radius + 50 + line * 14, anchor="middle",
                  colour=MUTED)
        return places

    left = loop(140, "On your computer",
                [("change", -150), ("save", -30), ("refresh", 90)],
                ("Refresh the file in your browser.", "One turn takes a few seconds."), FILL_BLUE)
    right = loop(420, "On GitHub",
                 [("commit", -135), ("push", -45), ("wait", 45), ("refresh", 135)],
                 ("Refresh your published site.", "One turn takes a minute or two."), FILL_GREEN)

    # The bridge: from the saved file on the left to the commit on the right.
    sx, sy, spill = left["save"]
    cx_, cy_, cpill = right["commit"]
    start = (sx + spill / 2 + 4, sy)
    end = (cx_ - cpill / 2 - 4, cy_)
    _arrow(drawing, root, start, end)
    _text(drawing, root, "ready to publish?", (start[0] + end[0]) / 2 + 6,
          min(start[1], end[1]) - 10, anchor="middle")

    _text(drawing, root, "In GitHub's editor, saving is a commit: only the second loop.",
          width / 2, height - 8, anchor="middle", colour=MUTED)
    drawing.add(root)
    return drawing.tostring()


def address_pattern() -> str:
    """The page's example address, cut into its parts, and each part named.

    Each part is its own text element with a fixed `textLength`, so the
    boxes fit the letters whatever monospace font the reader's machine
    picks. The second row is the same address with no file named at the
    end, which is how the home page is reached: GitHub Pages sends
    `index.html` for it.
    """
    size = 17
    advance = size * 0.6
    pad = 12
    x0, width = 16, 560
    drawing = _drawing(width, 250)
    root = drawing.g()

    def address(y: float, parts: list[tuple[str, str | None, str]]) -> list[tuple[float, float]]:
        x = x0
        centres = []
        for text, fill, _ in parts:
            w = len(text) * advance + pad
            root.add(drawing.rect(insert=(x, y), size=(w, 32),
                                  fill=fill or "none", stroke=INK if fill else "none",
                                  stroke_width=1.1, rx=4))
            root.add(drawing.text(
                text, insert=(x + pad / 2, y + 22), font_size=f"{size}px", font_family=MONO,
                textLength=f"{len(text) * advance:.1f}", lengthAdjust="spacingAndGlyphs",
                fill=INK if fill else MUTED))
            centres.append((x + w / 2, w))
            x += w
        return centres

    parts = [
        ("https://", None, ""),
        ("janedoe", FILL_BLUE, "your username"),
        (".github.io", PANEL, "GitHub Pages"),
        ("/web", FILL_GREEN, "your repository"),
        ("/about.html", FILL_AMBER, "one page in it"),
    ]
    centres = address(20, parts)
    # Labels alternate between two rows, so neighbours never overlap.
    for index, ((cx, _), (_, _, label)) in enumerate(zip(centres, parts)):
        if not label:
            continue
        low = index % 2 == 0
        root.add(drawing.line(start=(cx, 52), end=(cx, 84 if low else 64), stroke=INK,
                              stroke_width=1.1))
        _text(drawing, root, label, cx, 98 if low else 78, size=LABEL_PT, anchor="middle")

    home = [part if index < 4 else ("/", FILL_AMBER, "") for index, part in enumerate(parts)]
    centres = address(146, home)
    cx, _ = centres[-1]
    root.add(drawing.line(start=(cx, 178), end=(cx, 192), stroke=INK, stroke_width=1.1))
    _text(drawing, root, "no file named:", cx - 12, 206, size=LABEL_PT)
    _text(drawing, root, "GitHub Pages sends index.html", cx - 12, 222, size=LABEL_PT)
    _text(drawing, root, "The home page", x0, 138, size=SMALL_PT, colour=MUTED)
    _text(drawing, root, "Another page", x0, 14, size=SMALL_PT, colour=MUTED)
    drawing.add(root)
    return drawing.tostring()


def request_and_response() -> str:
    """What the browser says to DNS and to GitHub's server, in order.

    A sequence diagram: one column for each computer, time running down.
    The page's own example address is the one being fetched, and the
    second request, for the stylesheet, is drawn in full because it is the
    point the page makes after it — one page is several requests, and any
    one of them can fail on its own.
    """
    cols = {"browser": 84, "dns": 280, "server": 466}
    width, height = 552, 420
    drawing = _drawing(width, height)
    root = drawing.g()
    heads = {"browser": ["Your browser"], "dns": ["DNS", "the address book"],
             "server": ["GitHub's server", "where your files are"]}
    for key, x in cols.items():
        root.add(drawing.line(start=(x, 58), end=(x, height - 58), stroke=MUTED,
                              stroke_width=1.2, stroke_dasharray="4 4"))
        _box(drawing, root, x - 72, 12, 144, 46, heads[key], fill=PANEL)

    def message(y: float, frm: str, to: str, words: str, *, mono: bool = False,
                note: str | None = None) -> None:
        x1, x2 = cols[frm], cols[to]
        _arrow(drawing, root, (x1, y), (x2 - (4 if x2 > x1 else -4), y))
        # Words for the server go in the gap past the DNS line, clear of it.
        middle = (cols["dns"] + cols["server"]) / 2 if "server" in (frm, to) else (x1 + x2) / 2
        _text(drawing, root, words, middle, y - 7, size=LABEL_PT, anchor="middle",
              mono=mono)
        if note:
            _text(drawing, root, note, middle, y + 15, anchor="middle", colour=MUTED)

    message(92, "browser", "dns", "Where is janedoe.github.io?")
    message(134, "dns", "browser", "At 185.199.108.153")
    message(186, "browser", "server", "GET /web/about.html", mono=True, note="a request")
    message(236, "server", "browser", "200 OK, here is the HTML", note="a response")
    message(290, "browser", "server", "GET /web/styles.css", mono=True,
            note="the HTML names a stylesheet")
    message(340, "server", "browser", "200 OK, here is the CSS")

    _box(drawing, root, cols["browser"] - 72, height - 50, 144, 38,
         ["draws the page"], fill=FILL_GREEN, bold_first=False)
    _text(drawing, root, "time runs down the page", width - 16, height - 20,
          anchor="end", colour=MUTED)
    drawing.add(root)
    return drawing.tostring()


def commits_and_push() -> str:
    """A line of commits on the student's computer, and the copy on GitHub.

    The same four commits, drawn twice, one row per place, with the
    newest commit on the computer not yet on GitHub: that gap is exactly
    what `git push` closes, and the dashed circle is where it will land.
    `main` is drawn as a label on the newest commit in each row, because a
    branch is only that: a name that points at one commit.
    """
    xs = [60, 170, 280, 390]
    ids = ["e41b9d2", "7ac03f5", "b2d7e18", "5f60c9a"]
    messages = [("Change the", "page title"), ("Rewrite the", "introduction"),
                ("Add a skills", "section"), ("Add a contact", "section")]
    width, height = 540, 342
    drawing = _drawing(width, height)
    root = drawing.g()
    r = 11

    def row(y: float, title: str, count: int, fill: str, *, ghost: bool, notes: bool) -> None:
        root.add(drawing.rect(insert=(6, y - 58), size=(width - 12, 112 if notes else 110),
                              fill=fill, stroke="none", rx=8))
        _text(drawing, root, title, 16, y - 38, size=TITLE_PT, bold=True)
        last = xs[count - 1]
        root.add(drawing.line(start=(xs[0], y), end=(last, y), stroke=INK, stroke_width=1.6))
        if ghost:
            root.add(drawing.line(start=(last, y), end=(xs[count], y), stroke=MUTED,
                                  stroke_width=1.4, stroke_dasharray="4 3"))
            root.add(drawing.circle(center=(xs[count], y), r=r, fill="none", stroke=MUTED,
                                    stroke_width=1.4, stroke_dasharray="4 3"))
        for index in range(count):
            root.add(drawing.circle(center=(xs[index], y), r=r, fill=PAPER, stroke=INK,
                                    stroke_width=1.6))
            _text(drawing, root, ids[index], xs[index], y - 18, anchor="middle",
                  mono=True, colour=MUTED)
            if notes:
                for line, text in enumerate(messages[index]):
                    _text(drawing, root, text, xs[index], y + 30 + line * 14, anchor="middle")
        if ghost:
            # The name sits under the newest commit GitHub has, pointing up.
            top = y + r + 16
            root.add(drawing.rect(insert=(last - 23, top), size=(46, 22), fill=PANEL,
                                  stroke=INK, stroke_width=1.2, rx=4))
            _text(drawing, root, "main", last, top + 15, size=LABEL_PT, anchor="middle",
                  mono=True)
            _arrow(drawing, root, (last, top), (last, y + r + 2))
        else:
            left = last + r + 18
            root.add(drawing.rect(insert=(left, y - 11), size=(46, 22), fill=PANEL,
                                  stroke=INK, stroke_width=1.2, rx=4))
            _text(drawing, root, "main", left + 23, y + 4, size=LABEL_PT, anchor="middle",
                  mono=True)
            _arrow(drawing, root, (left, y), (last + r + 2, y))

    row(80, "On your computer", 4, FILL_BLUE, ghost=False, notes=True)
    row(236, "On GitHub", 3, FILL_GREEN, ghost=True, notes=False)

    _arrow(drawing, root, (xs[3], 80 + r + 34), (xs[3], 236 - r - 3))
    _text(drawing, root, "git push copies", xs[3] + 12, 176, size=LABEL_PT, mono=False)
    _text(drawing, root, "the new commit", xs[3] + 12, 191, size=LABEL_PT)
    _text(drawing, root, "older  →  newer", width / 2, height - 8, anchor="middle",
          colour=MUTED)
    drawing.add(root)
    return drawing.tostring()


DIAGRAMS = {
    "how-the-pieces-fit/path-of-a-change.svg": path_of_a_change,
    "the-two-loops/two-loops.svg": two_loops,
    "publish-it/address-pattern.svg": address_pattern,
    "how-a-browser-fetches-a-page/request-and-response.svg": request_and_response,
    "how-git-keeps-history/commits-and-push.svg": commits_and_push,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    written = parser.parse_args().write
    changed = 0
    for relative, draw in sorted(DIAGRAMS.items()):
        target = TUTORIALS / relative
        fresh = draw()
        if target.exists() and target.read_text() == fresh:
            print(f"  unchanged  {relative}")
            continue
        changed += 1
        if written:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(fresh)
            print(f"  written    {relative}")
        else:
            print(f"  would write {relative}")
    if changed and not written:
        print(f"\n{changed} diagram(s) differ. Re-run with --write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
