#!/usr/bin/env python3
"""The pictures for the Dewey Track, Units 6 to 10.

    python3 dev/graphics/dewey_units_6_10.py          # report what would change
    python3 dev/graphics/dewey_units_6_10.py --write  # write it

Units 6 to 10 are searching and sorting, algebra, geometry and
trigonometry, the derivative, and the history and craft of programming.
Most of their graphs are already matplotlib cells a reader can change,
and those stay where they are. These are the other pictures: the ones
where the page describes a shape in prose (a search closing in, a card
sliding left, a rectangle cut into four, a ramp seen from the side) and
the reader has to build the shape in their head before the sentence
makes sense.

Same rule as the other generators. Every number in a picture is
computed here, and where a page's own cell computes it, the cell is run
and its output read, so a picture cannot show a step the page's code
does not take. `_run_cells` runs a page's cells in order, in one space
of names, the way the page runs them.

Two things follow from the site inlining each SVG into the page
(`build.py`, `inline_local_svg`). Colours are the theme tokens from
`palette.py`, so a picture reads in light, dark and high contrast. And
several pictures can share one page, so nothing here uses an `id`.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import math
import re
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (  # noqa: E402
    FILL_AMBER, FILL_BLUE, FILL_GREEN, FILL_PINK, INK, MONO, MUTED, PANEL, PAPER, RULE, SANS,
)

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

MARGIN = 16
LABEL_PT = 13
SMALL_PT = 11.5
MINUS = "−"
TIMES = "×"


# --------------------------------------------------------------------------
# Reading a page, and drawing
# --------------------------------------------------------------------------

HEADER_RE = re.compile(r"^(id|hint|name|expect|toolkit|for):")


def _cell_code(slug: str, cell_id: str) -> str:
    """The code of one `python exec` cell, with its header lines removed."""
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    match = re.search(
        r"^```python exec\s*\nid: " + re.escape(cell_id) + r"\s*\n(.*?)^```",
        page, re.M | re.S)
    if match is None:
        raise SystemExit(f"{slug}: no cell called {cell_id!r} any more")
    lines = match.group(1).split("\n")
    while lines and HEADER_RE.match(lines[0]):
        lines.pop(0)
    return "\n".join(lines)


def _run_cells(slug: str, *cell_ids: str, given: dict | None = None):
    """Run a page's cells in order in one namespace, as the page does.

    Returns the namespace and each cell's printed output. `given` stands
    in for the toolkit tools a cell calls, so a picture never depends on
    a reader's own toolkit.
    """
    space: dict = dict(given or {})
    printed: dict[str, str] = {}
    for cell_id in cell_ids:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exec(compile(_cell_code(slug, cell_id), f"{slug}/{cell_id}", "exec"), space)
        printed[cell_id] = buffer.getvalue()
    return space, printed


def _printed_by(function, *arguments) -> tuple[object, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        answer = function(*arguments)
    return answer, buffer.getvalue()


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _text(drawing, text: str, x: float, y: float, *, size: float = LABEL_PT,
          anchor: str = "middle", fill: str = INK, mono: bool = False,
          bold: bool = False, italic: bool = False, parent=None) -> None:
    extra = {}
    if mono:
        extra["font_family"] = MONO
    if bold:
        extra["font_weight"] = "bold"
    if italic:
        extra["font_style"] = "italic"
    (parent or drawing).add(drawing.text(
        text, insert=(round(x, 2), round(y, 2)), text_anchor=anchor,
        font_size=f"{size}px", fill=fill, **extra))


def _width(text: str, size: float = LABEL_PT, mono: bool = False) -> float:
    """A rough width for laying out, not for measuring."""
    return len(text) * size * (0.6 if mono else 0.56)


def _line(drawing, x1, y1, x2, y2, *, stroke=INK, width=1.5, dash=None, parent=None):
    extra = {"stroke_dasharray": dash} if dash else {}
    (parent or drawing).add(drawing.line(
        (round(x1, 2), round(y1, 2)), (round(x2, 2), round(y2, 2)),
        stroke=stroke, stroke_width=width, stroke_linecap="round", **extra))


def _head(drawing, tip: tuple[float, float], towards: tuple[float, float],
          *, fill=INK, size: float = 8, parent=None) -> None:
    """An arrowhead at `tip`, pointing away from `towards`."""
    angle = math.atan2(tip[1] - towards[1], tip[0] - towards[0])
    left = (tip[0] - size * math.cos(angle - 0.42), tip[1] - size * math.sin(angle - 0.42))
    right = (tip[0] - size * math.cos(angle + 0.42), tip[1] - size * math.sin(angle + 0.42))
    points = [tuple(round(v, 2) for v in p) for p in (tip, left, right)]
    (parent or drawing).add(drawing.polygon(points, fill=fill, stroke="none"))


def _arrow(drawing, x1, y1, x2, y2, *, stroke=INK, width=1.5, head=8, dash=None,
           both=False, parent=None):
    _line(drawing, x1, y1, x2, y2, stroke=stroke, width=width, dash=dash, parent=parent)
    _head(drawing, (x2, y2), (x1, y1), fill=stroke, size=head, parent=parent)
    if both:
        _head(drawing, (x1, y1), (x2, y2), fill=stroke, size=head, parent=parent)


def _curve_arrow(drawing, start, control, end, *, stroke=INK, width=1.4, head=7,
                 both=False, dash=None, parent=None):
    """A quadratic curve with a head at its end, turned along the curve."""
    extra = {"stroke_dasharray": dash} if dash else {}
    (parent or drawing).add(drawing.path(
        d=f"M {start[0]:.2f} {start[1]:.2f} Q {control[0]:.2f} {control[1]:.2f} "
          f"{end[0]:.2f} {end[1]:.2f}",
        fill="none", stroke=stroke, stroke_width=width, **extra))
    _head(drawing, end, control, fill=stroke, size=head, parent=parent)
    if both:
        _head(drawing, start, control, fill=stroke, size=head, parent=parent)


def _box(drawing, x, y, w, h, *, fill=PANEL, stroke=INK, width=1.3, rx=4, dash=None,
         parent=None):
    extra = {"stroke_dasharray": dash} if dash else {}
    (parent or drawing).add(drawing.rect(
        (round(x, 2), round(y, 2)), (round(w, 2), round(h, 2)),
        fill=fill, stroke=stroke, stroke_width=width, rx=rx, **extra))


def _number(value: float, places: int = 2) -> str:
    """A number as a page would write it: no trailing zeros, a real minus sign."""
    text = f"{value:.{places}f}".rstrip("0").rstrip(".")
    if text in ("-0", ""):
        text = "0"
    return text.replace("-", MINUS)


def _ordinal(n: int) -> str:
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


# --------------------------------------------------------------------------
# Unit 6: searching and sorting
# --------------------------------------------------------------------------

def _binary_looks(values: list, target) -> tuple[list[tuple[int, int, int]], int, int]:
    """Every look a binary search makes, as (low, middle, high), the page's way.

    Returns the looks, the index found (or -1), and `low` and `high` as
    they were when the loop stopped.
    """
    looks = []
    low, high = 0, len(values) - 1
    while low <= high:
        middle = (low + high) // 2
        looks.append((low, middle, high))
        if values[middle] == target:
            return looks, middle, (low, high)
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return looks, -1, (low, high)


def _contacts():
    space, printed = _run_cells(
        "finding-things-fast", "finding-fast-linear-1", "finding-fast-binary-1")
    return space, printed["finding-fast-binary-1"]


def _page_middles(printed: str) -> list[int]:
    return [int(m) for m in re.findall(r"look at index (\d+) :", printed)]


SEARCH_CELL_W = 68
SEARCH_CELL_H = 30


def _search_rows(values: list[str], target: str) -> str:
    """Each look of a binary search, one row per look, with the part still live.

    The note on each row says what the look found and which end moves,
    because that sentence is the step a reader has to hold while the
    three indexes change.
    """
    looks, found, (last_low, last_high) = _binary_looks(values, target)
    count = len(values)
    width = 2 * MARGIN + count * SEARCH_CELL_W
    legend_h = 26
    row_h = 20 + 18 + SEARCH_CELL_H + 18 + 12
    closing_h = 0 if found >= 0 else 24
    height = 2 * MARGIN + legend_h + len(looks) * row_h + closing_h
    drawing = _drawing(width, height)

    _text(drawing, f"Shaded: the part still worth searching.   Dashed box: {target}, "
          "the name we want.", MARGIN, MARGIN + 12, size=SMALL_PT, anchor="start",
          fill=MUTED)
    target_at = values.index(target) if target in values else None

    for number, (low, middle, high) in enumerate(looks, start=1):
        top = MARGIN + legend_h + (number - 1) * row_h
        name = values[middle]
        if middle == found:
            outcome = f"That is {target}."
        elif name < target:
            outcome = f"{name} comes before {target}, so low becomes {middle + 1}."
        else:
            outcome = f"{target} comes before {name}, so high becomes {_number(middle - 1)}."
        _text(drawing, f"Look {number}: low {low}, high {high}, middle {middle}. {outcome}",
              MARGIN, top + 14, anchor="start")
        cells_top = top + 20 + 18
        for index, value in enumerate(values):
            left = MARGIN + index * SEARCH_CELL_W
            live = low <= index <= high
            fill = FILL_AMBER if index == middle else (PANEL if live else "none")
            _box(drawing, left + 2, cells_top, SEARCH_CELL_W - 4, SEARCH_CELL_H, fill=fill,
                 stroke=INK if live else RULE, width=1.3 if live else 0.8, rx=3)
            if index == target_at:
                _box(drawing, left - 1, cells_top - 3, SEARCH_CELL_W + 2, SEARCH_CELL_H + 6,
                     fill="none", stroke=INK, width=1.6, rx=5, dash="5,3")
            _text(drawing, value, left + SEARCH_CELL_W / 2, cells_top + SEARCH_CELL_H / 2 + 4.5,
                  fill=INK if live else MUTED)
            _text(drawing, str(index), left + SEARCH_CELL_W / 2, cells_top - 7,
                  size=10, fill=MUTED)
        # low, middle and high can share a cell; one label per cell keeps
        # them readable.
        together: dict[int, list[str]] = {}
        for index, mark in ((low, "low"), (middle, "middle"), (high, "high")):
            together.setdefault(index, []).append(mark)
        for index, marks in together.items():
            label = " ".join(marks)
            half = _width(label, SMALL_PT) / 2
            centre = MARGIN + index * SEARCH_CELL_W + SEARCH_CELL_W / 2
            centre = min(max(centre, MARGIN + half), width - MARGIN - half)
            _text(drawing, label, centre, cells_top + SEARCH_CELL_H + 14, size=SMALL_PT,
                  fill=MUTED)

    if found < 0:
        _text(drawing, f"Now low is {last_low} and high is {_number(last_high)}. Low is past "
              f"high, so it gives back {MINUS}1.",
              MARGIN, height - MARGIN - 4, anchor="start")
    return drawing.tostring()


def halving_the_contacts() -> str:
    """*Finding things fast*: the Priya search, in the sorted contacts.

    The page says in a paragraph what its two looks did, and then admits
    that three changing names are a lot to hold. This is that paragraph
    as rows.
    """
    space, printed = _contacts()
    in_order = space["in_order"]
    looks, _, _ = _binary_looks(in_order, "Priya")
    if [middle for _, middle, _ in looks] != _page_middles(printed):
        raise SystemExit("finding-things-fast: the page's binary search looks elsewhere now")
    return _search_rows(in_order, "Priya")


def searching_the_unsorted_list() -> str:
    """*Finding things fast*: binary search on the contacts as they were added.

    Aoife is there, at index 2, and the search says she is not. The rows
    show the look at which she falls outside the part still searched.
    """
    space, _ = _contacts()
    contacts = space["contacts"]
    _, printed = _printed_by(space["binary_steps"], contacts, "Aoife")
    looks, found, _ = _binary_looks(contacts, "Aoife")
    if [middle for _, middle, _ in looks] != _page_middles(printed) or found != -1:
        raise SystemExit("finding-things-fast: the unsorted search no longer fails the same way")
    return _search_rows(contacts, "Aoife")


CARD_W = 44
CARD_H = 40
CARD_GAP = 8


def _hand_rows(rows: list[tuple[str, list[int], dict]], note_x: float,
               width: float, arc_room: float = 22, legend: str = "") -> str:
    """Rows of cards. Each row is (label, cards, marks).

    `marks` may hold "sorted" (how many cards on the left are sorted),
    "amber" (indexes to fill amber), "arc" ((from, to, text) drawn above
    the row), "note" (the text on the right) and "note2" (a second line).
    """
    row_h = arc_room + CARD_H + 16
    legend_h = 24 if legend else 0
    height = 2 * MARGIN + legend_h + len(rows) * row_h
    drawing = _drawing(width, height)
    if legend:
        _text(drawing, legend, MARGIN, MARGIN + 12, size=SMALL_PT, anchor="start", fill=MUTED)
    first_x = MARGIN + 74
    for place, (label, cards, marks) in enumerate(rows):
        top = MARGIN + legend_h + place * row_h + arc_room
        _text(drawing, label, MARGIN, top + CARD_H / 2 + 5, anchor="start", fill=MUTED)
        for index, card in enumerate(cards):
            left = first_x + index * (CARD_W + CARD_GAP)
            if index in marks.get("amber", ()):
                fill = FILL_AMBER
            elif index < marks.get("sorted", 0):
                fill = FILL_GREEN
            else:
                fill = PANEL
            _box(drawing, left, top, CARD_W, CARD_H, fill=fill, width=1.4, rx=5)
            _text(drawing, str(card), left + CARD_W / 2, top + CARD_H / 2 + 5.5,
                  size=15, mono=True)
        if "arc" in marks:
            start, end, both = marks["arc"]
            x_start = first_x + start * (CARD_W + CARD_GAP) + CARD_W / 2
            x_end = first_x + end * (CARD_W + CARD_GAP) + CARD_W / 2
            lift = arc_room + 2
            _curve_arrow(drawing, (x_start, top - 3), ((x_start + x_end) / 2, top - lift),
                         (x_end, top - 3), both=both)
        if "note" in marks:
            _text(drawing, marks["note"], note_x, top + CARD_H / 2 - (2 if "note2" in marks else -5),
                  anchor="start")
        if "note2" in marks:
            _text(drawing, marks["note2"], note_x, top + CARD_H / 2 + 14, anchor="start",
                  fill=MUTED)
    return drawing.tostring()


def _parse_rows(printed: str, word: str) -> list[tuple[str, list[int]]]:
    rows = []
    for line in printed.splitlines():
        match = re.match(rf"{word} (\S+) : (\[.*\])$", line)
        if match:
            rows.append((match.group(1), eval(match.group(2))))   # a printed list of ints
    return rows


def selection_rounds() -> str:
    """*Sorting a hand of cards*: selection sort, round by round.

    Rows are what `selection_steps` prints, with the swap drawn above the
    two cards that changed places and the sorted part shaded, so the two
    parts of the list the page points at can be seen growing.
    """
    space, printed = _run_cells("sorting-a-hand-of-cards", "sorting-hand-selection-1")
    hand = space["hand"]
    rounds = _parse_rows(printed["sorting-hand-selection-1"], "place")
    rows = [("start", hand, {})]
    before = hand
    for number, (place, after) in enumerate(rounds, start=1):
        place = int(place)
        moved = [i for i in range(len(after)) if before[i] != after[i]]
        smallest = after[place]
        marks: dict = {"sorted": place + 1}
        if moved:
            other = moved[-1] if moved[0] == place else moved[0]
            marks["arc"] = (place, other, True)
            marks["note"] = f"The smallest left is {smallest}."
            marks["note2"] = f"It swaps with the {before[place]}."
        else:
            marks["note"] = f"The smallest left is {smallest}."
            marks["note2"] = "It is already in place."
        rows.append((f"round {number}", after, marks))
        before = after
    if before != sorted(hand):
        raise SystemExit("sorting-a-hand-of-cards: selection_steps no longer sorts the hand")
    note_x = MARGIN + 74 + len(hand) * (CARD_W + CARD_GAP) + 14
    return _hand_rows(rows, note_x, note_x + 200 + MARGIN,
                      legend="Green: the sorted part. Arrows: the two cards that swap.")


def insertion_rounds() -> str:
    """*Sorting a hand of cards*: insertion sort, one card placed per row.

    The amber card is the one being placed; the arrow runs from where it
    was to where it drops, over the cards it slid past.
    """
    space, printed = _run_cells("sorting-a-hand-of-cards", "sorting-hand-selection-1",
                                "sorting-hand-insertion-1")
    hand = space["hand"]
    placed = _parse_rows(printed["sorting-hand-insertion-1"], "placed")
    rows = [("start", hand, {"sorted": 1})]
    for number, (card, after) in enumerate(placed, start=1):
        card = int(card)
        place = number                      # insertion sort places index 1, 2, 3 ...
        final = after.index(card)
        slid = place - final
        marks: dict = {"sorted": place + 1, "amber": {final}}
        if slid == 0:
            marks["note"] = f"{card} stays where it is."
            marks["note2"] = f"The {after[place - 1]} to its left is lower."
        else:
            marks["arc"] = (place, final, False)
            past = "1 card" if slid == 1 else f"{slid} cards"
            marks["note"] = f"{card} slides left past {past}."
            marks["note2"] = ("It reaches the front." if final == 0
                              else f"It stops at the {after[final - 1]}.")
        rows.append((f"card {number + 1}", after, marks))
    if rows[-1][1] != sorted(hand):
        raise SystemExit("sorting-a-hand-of-cards: insertion_steps no longer sorts the hand")
    note_x = MARGIN + 74 + len(hand) * (CARD_W + CARD_GAP) + 14
    return _hand_rows(rows, note_x, note_x + 200 + MARGIN,
                      legend="Green: the sorted part. Amber: the card just placed.")


SHELL_CELL = 40


def shell_gaps() -> str:
    """*Racing the sorts*: Shell sort on 8 cards in reverse order.

    Each row is the list going into a pass, with the values that pass
    sorts together joined by arcs: pairs 4 apart, then every other value.
    Joined values sit in one group, and the arcs for alternate groups go
    above and below the row so they do not cross.
    """
    space, printed = _run_cells("racing-the-sorts", "racing-shell-1")
    code = _cell_code("racing-the-sorts", "racing-shell-1")
    start = eval(re.search(r"print\(shell_steps\((\[.*\])\)\)", code).group(1))
    passes = _parse_rows(printed["racing-shell-1"], "gap")
    rows: list[tuple[str, list[int], int | None]] = []
    label, before = "start", start
    for gap, after in passes:
        rows.append((label, before, int(gap)))
        label, before = f"after gap {gap}", after
    rows.append((label, before, None))
    if before != sorted(start):
        raise SystemExit("racing-the-sorts: shell_steps no longer sorts the list")

    count = len(start)
    first_x = MARGIN + 92
    note_x = first_x + count * SHELL_CELL + 18
    width = note_x + 250 + MARGIN
    row_h = 30 + SHELL_CELL + 30
    height = 2 * MARGIN + len(rows) * row_h
    drawing = _drawing(width, height)
    for place, (label, values, gap) in enumerate(rows):
        top = MARGIN + place * row_h + 30
        _text(drawing, label, MARGIN, top + SHELL_CELL / 2 + 5, anchor="start", fill=MUTED)
        for index, value in enumerate(values):
            left = first_x + index * SHELL_CELL
            _box(drawing, left + 2, top, SHELL_CELL - 4, SHELL_CELL, width=1.3, rx=4,
                 fill=FILL_GREEN if gap is None else PANEL)
            _text(drawing, str(value), left + SHELL_CELL / 2, top + SHELL_CELL / 2 + 5,
                  size=14, mono=True)
        if gap is None:
            _text(drawing, "Sorted.", note_x, top + SHELL_CELL / 2 + 5, anchor="start")
            continue
        if gap > 1:
            for group in range(gap):
                above = group % 2 == 0
                lift = 12 + 6 * (group // 2)
                members = list(range(group, count, gap))
                for left_index, right_index in zip(members, members[1:]):
                    x1 = first_x + left_index * SHELL_CELL + SHELL_CELL / 2
                    x2 = first_x + right_index * SHELL_CELL + SHELL_CELL / 2
                    edge = top - 2 if above else top + SHELL_CELL + 2
                    bend = edge - 2 * lift if above else edge + 2 * lift
                    drawing.add(drawing.path(
                        d=f"M {x1:.2f} {edge:.2f} Q {(x1 + x2) / 2:.2f} {bend:.2f} "
                          f"{x2:.2f} {edge:.2f}",
                        fill="none", stroke=INK, stroke_width=1.3,
                        stroke_dasharray="none" if above else "4,3"))
            groups = "pairs" if count // gap == 2 else "groups"
            _text(drawing, f"Next pass: gap {gap}.", note_x, top + SHELL_CELL / 2 - 3,
                  anchor="start")
            _text(drawing, f"Joined values, {gap} apart, are sorted", note_x,
                  top + SHELL_CELL / 2 + 13, anchor="start", size=SMALL_PT, fill=MUTED)
            _text(drawing, f"together, as {gap} {groups}.", note_x,
                  top + SHELL_CELL / 2 + 27, anchor="start", size=SMALL_PT, fill=MUTED)
        else:
            _text(drawing, "Next pass: gap 1, an ordinary", note_x, top + SHELL_CELL / 2 - 3,
                  anchor="start")
            _text(drawing, "insertion sort of the whole list.", note_x,
                  top + SHELL_CELL / 2 + 13, anchor="start")
    return drawing.tostring()


def _folder_rows(nested: list, depth: int, rows: list, name: str) -> None:
    rows.append((depth, name, "folder"))
    for item in nested:
        if isinstance(item, list):
            first = next(x for x in item if not isinstance(x, list))
            _folder_rows(item, depth + 1, rows, first.split("-")[0])
        else:
            rows.append((depth + 1, item, "photo"))


def holidays_folders() -> str:
    """*A function that calls itself*: the "Holidays" folder, level by level.

    Drawn as a file browser draws a folder, one item to a line, pushed
    right one step for each level. The four items directly inside
    Holidays are shaded, because `len(holidays)` counts those and no more.
    """
    space, printed = _run_cells("a-function-that-calls-itself", "calls-itself-folders-1")
    holidays = space["holidays"]
    rows: list[tuple[int, str, str]] = []
    _folder_rows(holidays, 0, rows, "Holidays")
    direct = len(holidays)
    if printed["calls-itself-folders-1"].strip() != str(direct):
        raise SystemExit("a-function-that-calls-itself: len(holidays) changed")
    photos = sum(1 for _, _, kind in rows if kind == "photo")

    step = 44
    row_h = 25
    deepest = max(depth for depth, _, _ in rows)
    width = 560
    header_h = 26
    height = 2 * MARGIN + header_h + len(rows) * row_h + 34
    drawing = _drawing(width, height)
    left = MARGIN + 6
    _text(drawing, "level", left, MARGIN + 12, size=SMALL_PT, anchor="start", fill=MUTED)
    for level in range(1, deepest + 1):
        _text(drawing, str(level), left + level * step + 8, MARGIN + 12, size=SMALL_PT,
              fill=MUTED)

    positions: list[tuple[float, float]] = []
    for place, (depth, label, kind) in enumerate(rows):
        y = MARGIN + header_h + place * row_h + row_h / 2
        x = left + depth * step
        positions.append((x, y))
        shaded = depth == 1
        if kind == "folder":
            fill = FILL_AMBER if shaded else PANEL
            drawing.add(drawing.path(
                d=f"M {x:.1f} {y - 6:.1f} l 0 13 l 18 0 l 0 -11 l -9 0 l -2 -3 l -7 0 z",
                fill=fill, stroke=INK, stroke_width=1.2))
            _text(drawing, label, x + 24, y + 4.5, anchor="start", bold=True)
        else:
            fill = FILL_AMBER if shaded else PANEL
            _box(drawing, x, y - 6, 16, 12, fill=fill, width=1.1, rx=1.5)
            drawing.add(drawing.polyline(
                [(x + 2, y + 4), (x + 7, y - 1), (x + 10, y + 2), (x + 12, y), (x + 14, y + 4)],
                fill="none", stroke=INK, stroke_width=0.9))
            _text(drawing, label, x + 24, y + 4.5, anchor="start", mono=True, size=12.5)
    # Connectors: from each folder's icon down to the rows inside it.
    for place, (depth, _, kind) in enumerate(rows):
        if kind != "folder":
            continue
        x, y = positions[place]
        children = []
        for later in range(place + 1, len(rows)):
            if rows[later][0] <= depth:
                break
            if rows[later][0] == depth + 1:
                children.append(later)
        if not children:
            continue
        stem = x + 7
        last_y = positions[children[-1]][1]
        _line(drawing, stem, y + 8, stem, last_y, stroke=RULE, width=1.2)
        for child in children:
            _line(drawing, stem, positions[child][1], positions[child][0] - 3,
                  positions[child][1], stroke=RULE, width=1.2)
    bottom = MARGIN + header_h + len(rows) * row_h + 20
    _text(drawing, f"Shaded: the {direct} items directly inside Holidays, which len counts.",
          MARGIN, bottom, anchor="start", size=SMALL_PT, fill=MUTED)
    _text(drawing, f"{photos} photos in all.", width - MARGIN, bottom, anchor="end",
          size=SMALL_PT, fill=MUTED)
    return drawing.tostring()


def calls_that_wait() -> str:
    """*A function that calls itself*: the five calls of `factorial_shown(4)`.

    Read from what the page's own cell prints. Each call sits one step
    lower and further right than the call that made it, as the cell
    indents it, and each says what it gives back and in which order it
    started and finished, since "starts first, finishes last" is the
    point of the section.
    """
    _, printed = _run_cells("a-function-that-calls-itself", "calls-itself-wait-1")
    calls: dict[int, dict] = {}
    for order, line in enumerate(printed["calls-itself-wait-1"].splitlines()):
        match = re.match(r"^( *)factorial_shown\((\d+)\) (starts|gives back (\d+))$", line)
        if not match:
            continue
        n = int(match.group(2))
        entry = calls.setdefault(n, {"depth": len(match.group(1)) // 4})
        if match.group(3) == "starts":
            entry["start"] = order
        else:
            entry["answer"] = int(match.group(4))
            entry["end"] = order
    by_start = sorted(calls, key=lambda n: calls[n]["start"])
    by_end = sorted(calls, key=lambda n: calls[n]["end"])

    box_w, box_h = 178, 34
    step_x, step_y = 40, 62
    width = 640
    height = 2 * MARGIN + (len(calls) - 1) * step_y + box_h + 8
    drawing = _drawing(width, height)
    for n in by_start:
        entry = calls[n]
        depth = entry["depth"]
        x = MARGIN + depth * step_x
        y = MARGIN + depth * step_y
        base = n == min(calls)
        _box(drawing, x, y, box_w, box_h, fill=FILL_AMBER if base else PANEL, width=1.4, rx=5)
        _text(drawing, f"factorial_shown({n})", x + box_w / 2, y + box_h / 2 + 5, mono=True,
              size=13)
        if base:
            gives = f"gives back {entry['answer']}: the base case"
        else:
            inner = calls[n - 1]["answer"]
            gives = f"gives back {n} {TIMES} {inner} = {entry['answer']}"
        _text(drawing, gives, x + box_w + 14, y + box_h / 2 - 1, anchor="start")
        _text(drawing, f"starts {_ordinal(by_start.index(n) + 1)}, "
              f"finishes {_ordinal(by_end.index(n) + 1)}",
              x + box_w + 14, y + box_h / 2 + 15, anchor="start", size=SMALL_PT, fill=MUTED)
        if not base:
            _arrow(drawing, x + 22, y + box_h + 2, x + 22, y + step_y - 3, head=7)
            _text(drawing, "waits for", x + 30, y + box_h + (step_y - box_h) / 2 + 4,
                  anchor="start", size=SMALL_PT, fill=MUTED)
    return drawing.tostring()


def one_more_than_all_before() -> str:
    """*Doubling and halving*: the first six squares of the chessboard.

    One grain is one small cell. Squares 1 to 5 laid end to end fall one
    grain short of square 6 on its own, which is the page's "one more
    grain than all the squares before it put together", counted.
    """
    space, _ = _run_cells("doubling-and-halving", "doubling-chess-1", given={"total": sum})
    grains = space["grains"]
    shown = 6
    before, last = grains[:shown - 1], grains[shown - 1]
    if sum(before) + 1 != last:
        raise SystemExit("doubling-and-halving: the chessboard no longer doubles")
    unit = 14
    first_x = MARGIN + 118
    width = first_x + last * unit + 70 + MARGIN
    row_gap = 58
    top = MARGIN + 22
    height = top + row_gap + unit + 40 + MARGIN
    drawing = _drawing(width, height)
    tints = [FILL_AMBER, FILL_BLUE]

    def run(start_cell: int, count: int, y: float, tint: str) -> None:
        for cell in range(count):
            _box(drawing, first_x + (start_cell + cell) * unit, y, unit, unit, fill=tint,
                 width=0.8, rx=0)

    cell = 0
    for square, amount in enumerate(before, start=1):
        run(cell, amount, top, tints[square % 2])
        middle = first_x + (cell + amount / 2) * unit
        _text(drawing, str(amount), middle, top - 6, size=SMALL_PT)
        _text(drawing, str(square), middle, top + unit + 15, size=SMALL_PT, fill=MUTED)
        cell += amount
    _box(drawing, first_x + cell * unit, top, unit, unit, fill="none", width=1.2, rx=0,
         dash="3,2")
    _text(drawing, "+1", first_x + (cell + 0.5) * unit, top - 6, size=SMALL_PT, bold=True)
    _text(drawing, f"squares 1 to {shown - 1}", MARGIN, top + unit - 2, anchor="start")
    _text(drawing, f"= {sum(before)} grains", first_x + last * unit + 10, top + unit - 2,
          anchor="start")
    second = top + row_gap
    run(0, last, second, tints[shown % 2])
    _text(drawing, str(last), first_x + last * unit / 2, second - 6, size=SMALL_PT)
    _text(drawing, str(shown), first_x + last * unit / 2, second + unit + 15, size=SMALL_PT,
          fill=MUTED)
    _text(drawing, f"square {shown}", MARGIN, second + unit - 2, anchor="start")
    _text(drawing, f"= {last} grains", first_x + last * unit + 10, second + unit - 2,
          anchor="start")
    _text(drawing, "One small square is one grain. Above: how many grains. Below, grey: "
          "which square.",
          MARGIN, height - MARGIN, anchor="start", size=SMALL_PT, fill=MUTED)
    return drawing.tostring()


# --------------------------------------------------------------------------
# Unit 7: algebra
# --------------------------------------------------------------------------

POWERS = {2: "²", 3: "³"}


def _term(coefficient: float, power: int, letter: str = "x") -> str:
    if power == 0:
        return _number(coefficient)
    if coefficient == 1:
        front = ""
    elif coefficient == -1:
        front = MINUS
    else:
        front = _number(coefficient)
    return f"{front}{letter}{POWERS.get(power, '')}"


def _polynomial(coefficients: list[float], letter: str = "x") -> str:
    """Highest power first, the way the page writes it; zero terms left out."""
    parts = []
    for power in range(len(coefficients) - 1, -1, -1):
        value = coefficients[power]
        if value == 0:
            continue
        text = _term(abs(value), power, letter)
        if not parts:
            parts.append(text if value > 0 else MINUS + text)
        else:
            parts.append(("+ " if value > 0 else f"{MINUS} ") + text)
    return " ".join(parts) or "0"


def _bracket(coefficients: list[float]) -> str:
    return f"({_polynomial(coefficients)})"


# (power across, power down): what the page calls each piece of the photo
PIECE_NAMES = {(1, 1): "photo", (0, 1): "strip", (1, 0): "bar", (0, 0): "corner"}

LETTER_PX = 170     # how long x is drawn: a length, never read as a number
UNIT_PX = 17        # how long 1 is drawn


def _bracket_area(across: list[int], down: list[int], expanded: list[int],
                  left_out_power: int | None = None) -> str:
    """A rectangle `across` wide and `down` tall, cut into one piece per pair of terms.

    Both brackets are `[number, 1]`, a letter plus a number, lowest power
    first as the page's lists are. The letter's piece is drawn first on
    each side, so the photo is the top-left square and the number's
    pieces are the strip and the bar. `left_out_power` marks the pieces
    of that power as the ones a hurried answer forgets.
    """
    if across[1] != 1 or down[1] != 1:
        raise SystemExit("rules-with-letters-in-them: the picture draws x + a number only")
    across_lengths = [LETTER_PX, across[0] * UNIT_PX]
    down_lengths = [LETTER_PX, down[0] * UNIT_PX]
    across_terms = [(1, 1), (across[0], 0)]      # (coefficient, power), letter first
    down_terms = [(1, 1), (down[0], 0)]

    left = MARGIN + 28
    top = MARGIN + 24
    rect_w, rect_h = sum(across_lengths), sum(down_lengths)
    text_x = left + rect_w + 34
    width = 620
    height = top + rect_h + MARGIN + 6
    drawing = _drawing(width, height)

    pieces = []
    y = top
    for (down_c, down_p), piece_h in zip(down_terms, down_lengths):
        x = left
        for (across_c, across_p), piece_w in zip(across_terms, across_lengths):
            coefficient, power = across_c * down_c, across_p + down_p
            label = _term(coefficient, power)
            pieces.append((coefficient, power))
            forgotten = left_out_power is not None and power == left_out_power
            if power == 2:
                fill = PANEL
            elif power == 0:
                fill = FILL_AMBER
            else:
                fill = FILL_PINK if forgotten else FILL_BLUE
            _box(drawing, x, y, piece_w, piece_h, fill=fill, width=1.6, rx=0,
                 dash="6,3" if forgotten else None)
            _text(drawing, label, x + piece_w / 2, y + piece_h / 2 + 3, size=15)
            name = PIECE_NAMES[(across_p, down_p)]
            _text(drawing, f"{name}, left out" if forgotten and piece_w > 90 else name,
                  x + piece_w / 2, y + piece_h / 2 + 19, size=SMALL_PT, fill=MUTED)
            if forgotten and piece_w <= 90:
                _text(drawing, "left out", x + piece_w / 2, y + piece_h / 2 + 33,
                      size=SMALL_PT, fill=MUTED)
            x += piece_w
        y += piece_h

    x = left
    for (coefficient, power), length in zip(across_terms, across_lengths):
        _text(drawing, _term(coefficient, power), x + length / 2, top - 8, size=15)
        x += length
    y = top
    for (coefficient, power), length in zip(down_terms, down_lengths):
        _text(drawing, _term(coefficient, power), left - 10, y + length / 2 + 5, size=15,
              anchor="end")
        y += length

    collected = [0] * (max(p for _, p in pieces) + 1)
    for coefficient, power in pieces:
        collected[power] += coefficient
    if collected != expanded:
        raise SystemExit(f"rules-with-letters-in-them: pieces give {collected}, "
                         f"the page's expand_brackets gives {expanded}")
    same = across == down
    written = f"{_bracket(across)}²" if same else f"{_bracket(across)}{_bracket(down)}"
    lines = [
        (written, INK),
        ("= " + " + ".join(_term(c, p) for c, p in pieces), INK),
        ("= " + _polynomial(expanded), INK),
    ]
    if left_out_power is not None:
        kept = [0] * len(expanded)
        for coefficient, power in pieces:
            if power != left_out_power:
                kept[power] += coefficient
        forgotten_term = _term(across[0] * down[1], left_out_power)
        lines += [("", INK), (f"{_polynomial(kept)} keeps the photo", MUTED),
                  ("and the corner, and leaves", MUTED),
                  (f"out the two {forgotten_term} pieces.", MUTED)]
    for place, (line, colour) in enumerate(lines):
        _text(drawing, line, text_x, top + 40 + place * 24, anchor="start", size=15,
              fill=colour)
    return drawing.tostring()


def _expand_space():
    return _run_cells("rules-with-letters-in-them", "rules-with-expand-1")[0]


def photo_with_bars() -> str:
    """*Rules with letters in them*: (x + 3)(x + 5) as a photo, a strip, a bar and a corner.

    The page asks the reader to picture this rectangle and gives a grid of
    four pieces as a table. The picture is the rectangle itself, with the
    same four pieces, and the sum they make, checked against the page's
    own `expand_brackets`.
    """
    space = _expand_space()
    return _bracket_area([3, 1], [5, 1], space["photo_with_bars"])


def the_square_forgotten() -> str:
    """*Rules with letters in them*: (x + 3)² and what x² + 9 leaves out.

    The page says that x² + 9 "keeps the photo and the small corner, and
    forgets the strip and the bar". Those two pieces are marked.
    """
    space = _expand_space()
    return _bracket_area([3, 1], [3, 1], space["expand_brackets"]([3, 1], [3, 1]),
                         left_out_power=1)


def sprite_sheet() -> str:
    """*Solving for x*: the sprite sheet the positive root describes.

    The page's cell finds the pair that adds to 3 and multiplies to −40;
    the roots follow from it, and the one that can be a count of rows is
    drawn, with its columns 3 more, and a number on every tile.
    """
    code = _cell_code("solving-for-x", "solving-inspection-1")
    more_columns = int(re.search(r"target_sum = (-?\d+)", code).group(1))
    tiles = -int(re.search(r"target_product = (-?\d+)", code).group(1))
    _, printed = _run_cells("solving-for-x", "solving-inspection-1")
    p, q = (int(v) for v in printed["solving-inspection-1"].split("\n")[0].split())
    roots = sorted({-p, -q})
    rows = max(roots)
    columns = rows + more_columns
    if rows * columns != tiles or min(roots) >= 0:
        raise SystemExit("solving-for-x: the sprite sheet's numbers changed")

    tile = 40
    left = MARGIN + 70
    top = MARGIN + 30
    width = 620
    height = top + rows * tile + MARGIN + 4
    drawing = _drawing(width, height)
    for row in range(rows):
        for column in range(columns):
            x, y = left + column * tile, top + row * tile
            _box(drawing, x + 2, y + 2, tile - 4, tile - 4, fill=PANEL, width=1.1, rx=3)
            _text(drawing, str(row * columns + column + 1), x + tile / 2, y + tile / 2 + 4,
                  size=10.5, fill=MUTED)
    _arrow(drawing, left + 4, top - 12, left + columns * tile - 4, top - 12, head=6, both=True,
           width=1.1)
    _text(drawing, f"w + {more_columns} = {columns} columns", left + columns * tile / 2, top - 18,
          size=13)
    _arrow(drawing, left - 12, top + 4, left - 12, top + rows * tile - 4, head=6, both=True,
           width=1.1)
    _text(drawing, f"w = {rows}", left - 20, top + rows * tile / 2 - 2, anchor="end")
    _text(drawing, "rows", left - 20, top + rows * tile / 2 + 14, anchor="end")
    text_x = left + columns * tile + 26
    _text(drawing, f"{rows} {TIMES} {columns} = {tiles} tiles", text_x, top + 40, anchor="start",
          size=15)
    _text(drawing, f"The other root, w = {_number(min(roots))},", text_x, top + 76,
          anchor="start", fill=MUTED)
    _text(drawing, "cannot be a count of rows.", text_x, top + 96, anchor="start", fill=MUTED)
    return drawing.tostring()


def quarter_turns() -> str:
    """*When there is no real answer*: multiplying by i, four times, on the plane.

    The points are the ones the page's cell prints as it multiplies 1 by
    `1j` again and again; each arrow is one multiply, a quarter turn.
    """
    _, printed = _run_cells("when-there-is-no-real-answer", "no-real-plane-1")
    points = [complex(line.strip()) for line in printed["no-real-plane-1"].split()]
    if points[4] != points[0] or any(abs(abs(p) - 1) > 1e-12 for p in points):
        raise SystemExit("when-there-is-no-real-answer: the quarter turns changed")
    scale = 120
    width, height = 620, 2 * MARGIN + 2 * 1.55 * scale + 10
    cx, cy = width / 2 - 20, height / 2 - 6
    drawing = _drawing(width, height)
    reach = 1.5 * scale
    _arrow(drawing, cx - reach, cy, cx + reach, cy, stroke=MUTED, width=1.1, head=6)
    _arrow(drawing, cx, cy + reach, cx, cy - reach, stroke=MUTED, width=1.1, head=6)
    _text(drawing, "real part:", cx + reach + 8, cy - 2, anchor="start", size=SMALL_PT,
          fill=MUTED)
    _text(drawing, "across", cx + reach + 8, cy + 13, anchor="start", size=SMALL_PT,
          fill=MUTED)
    _text(drawing, f"Each arrow is one {TIMES} 1j: a quarter turn, against the clock.",
          MARGIN, height - MARGIN, anchor="start", size=SMALL_PT, fill=MUTED)
    _text(drawing, "imaginary part: up", cx + 8, cy - reach + 4, anchor="start",
          size=SMALL_PT, fill=MUTED)
    names = {1: "1", 1j: "i, or 1j", -1: f"{MINUS}1", -1j: f"{MINUS}i, or {MINUS}1j"}
    offsets = {1: (10, -10, "start"), 1j: (10, -8, "start"), -1: (-10, -10, "end"),
               -1j: (10, 18, "start")}
    for point in points[:4]:
        key = complex(round(point.real), round(point.imag))
        x, y = cx + point.real * scale, cy - point.imag * scale
        drawing.add(drawing.circle((round(x, 2), round(y, 2)), 6, fill=FILL_AMBER, stroke=INK,
                                   stroke_width=1.4))
        dx, dy, anchor = offsets[key]
        _text(drawing, names[key], x + dx, y + dy, anchor=anchor, size=14)
    radius = 1.0 * scale
    for turn, (here, there) in enumerate(zip(points[:4], points[1:5])):
        start_angle = math.atan2(here.imag, here.real) + 0.16
        end_angle = math.atan2(there.imag, there.real) - 0.16
        if end_angle < start_angle:
            end_angle += 2 * math.pi
        middle_angle = (start_angle + end_angle) / 2
        control_r = radius / math.cos((end_angle - start_angle) / 2)
        start = (cx + radius * math.cos(start_angle), cy - radius * math.sin(start_angle))
        end = (cx + radius * math.cos(end_angle), cy - radius * math.sin(end_angle))
        control = (cx + control_r * math.cos(middle_angle), cy - control_r * math.sin(middle_angle))
        _curve_arrow(drawing, start, control, end, width=1.6, head=8)
        label_r = radius * 1.14
        _text(drawing, f"{TIMES} 1j", cx + label_r * math.cos(middle_angle),
              cy - label_r * math.sin(middle_angle) + 4,
              anchor="start" if math.cos(middle_angle) > 0 else "end", size=SMALL_PT,
              fill=MUTED)
    return drawing.tostring()


def _equations_from_check_cell() -> list[tuple[int, int, int]]:
    code = _cell_code("several-unknowns-at-once", "several-unknowns-elimination-1")
    found = []
    for first, second, total in re.findall(
            r"print\((\d+ \* )?images \+ (\d+ \* )?texts == (\d+)\)", code):
        found.append((int(first.strip(" *") or 1), int(second.strip(" *") or 1), int(total)))
    if len(found) != 2:
        raise SystemExit("several-unknowns-at-once: the check cell no longer holds two equations")
    return found


def the_determinant() -> str:
    """*Several unknowns at once*: the four numbers in a square, and the two diagonals.

    The page describes this in words, a square of four numbers and a
    product along each diagonal. Drawn with the page's own two equations,
    and the answer checked by the formula the determinant is the bottom of.
    """
    (a1, b1, c1), (a2, b2, c2) = _equations_from_check_cell()
    determinant = a1 * b2 - a2 * b1
    images = (c1 * b2 - c2 * b1) / determinant
    texts = (a1 * c2 - a2 * c1) / determinant
    if (images, texts) != (130, 100):
        raise SystemExit("several-unknowns-at-once: the solution changed")
    width, height = 660, 250
    drawing = _drawing(width, height)
    cell = 84
    left, top = MARGIN + 170, MARGIN + 30
    _text(drawing, f"{_term(a1, 1, 'a')} + {_term(b1, 1, 'c')} = {c1}", MARGIN,
          top + cell / 2 + 5, anchor="start", size=15)
    _text(drawing, f"{_term(a2, 1, 'a')} + {_term(b2, 1, 'c')} = {c2}", MARGIN,
          top + cell * 1.5 + 5, anchor="start", size=15)
    names = [["a₁", "b₁"], ["a₂", "b₂"]]
    values = [[a1, b1], [a2, b2]]
    for row in range(2):
        for column in range(2):
            x, y = left + column * cell, top + row * cell
            _box(drawing, x, y, cell, cell, fill=PANEL, width=1.4, rx=0)
            _text(drawing, str(values[row][column]), x + cell / 2, y + cell / 2 + 7, size=20,
                  mono=True)
            _text(drawing, names[row][column], x + cell / 2, y + cell - 9, size=SMALL_PT,
                  fill=MUTED, italic=True)
    _text(drawing, "a", left + cell / 2, top - 10, size=15, italic=True)
    _text(drawing, "c", left + cell * 1.5, top - 10, size=15, italic=True)
    near, far = 0.5 * cell + 17, 1.5 * cell - 17
    _arrow(drawing, left + near, top + near, left + far, top + far, width=1.8, head=9)
    _arrow(drawing, left + near, top + 2 * cell - near, left + far, top + 2 * cell - far,
           width=1.4, head=8, dash="5,3")
    text_x = left + 2 * cell + 30
    _text(drawing, f"one diagonal: {a1} {TIMES} {b2} = {a1 * b2}", text_x, top + 30,
          anchor="start", size=14)
    _text(drawing, f"the other, dashed: {a2} {TIMES} {b1} = {a2 * b1}", text_x, top + 56,
          anchor="start", size=14)
    _text(drawing, f"determinant: {a1 * b2} {MINUS} {a2 * b1} = {_number(determinant)}",
          text_x, top + 96, anchor="start", size=14, bold=True)
    _text(drawing, "Not 0, so there is one answer:", text_x, top + 124, anchor="start",
          size=SMALL_PT, fill=MUTED)
    _text(drawing, f"a = {_number(images)} and c = {_number(texts)}.", text_x, top + 142,
          anchor="start", size=SMALL_PT, fill=MUTED)
    return drawing.tostring()


def _clip(a: float, b: float, c: float, box: tuple[float, float, float, float]):
    """The part of the line ax + by = c inside box (x0, x1, y0, y1), as two points."""
    x0, x1, y0, y1 = box
    ends = [(x0, (c - a * x0) / b), (x1, (c - a * x1) / b)]
    (px, py), (qx, qy) = ends
    low, high = 0.0, 1.0
    for p, q in ((-(qx - px), px - x0), (qx - px, x1 - px),
                 (-(qy - py), py - y0), (qy - py, y1 - py)):
        if p == 0:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            low = max(low, t)
        else:
            high = min(high, t)
    if low > high:
        return None
    return ((px + low * (qx - px), py + low * (qy - py)),
            (px + high * (qx - px), py + high * (qy - py)))


def once_never_everywhere() -> str:
    """*Several unknowns at once*: the three ways two straight lines can meet.

    The page draws the first two with matplotlib, and describes the third,
    "one fact said twice", in words. Here are all three side by side, each
    with its determinant. The third pair is the second reading changed to
    the total that doubling the first reading gives.
    """
    (a1, b1, c1), (a2, b2, c2) = _equations_from_check_cell()
    readings = re.search(r"solve_simultaneous\(([\d, ]+)\)",
                         _cell_code("several-unknowns-at-once", "several-unknowns-none-1"))
    p1, s1, t1, p2, s2, t2 = (int(v) for v in readings.group(1).split(","))
    same_total = t1 * p2 // p1
    panels = [
        ("once", (a1, b1, c1), (a2, b2, c2), (0, 230, 0, 320), ("images", "texts")),
        ("never", (p1, s1, t1), (p2, s2, t2), (0, 25, 0, 45), ("photo MB", "song MB")),
        ("everywhere", (p1, s1, t1), (p2, s2, same_total), (0, 25, 0, 45),
         ("photo MB", "song MB")),
    ]
    panel_w, panel_h, gap = 170, 150, 26
    width = 2 * MARGIN + 3 * panel_w + 2 * gap
    top = MARGIN + 26
    height = top + panel_h + 70 + MARGIN
    drawing = _drawing(width, height)
    for place, (title, first, second, box, (across, up)) in enumerate(panels):
        left = MARGIN + place * (panel_w + gap)
        x0, x1, y0, y1 = box

        def at(point):
            return (left + (point[0] - x0) / (x1 - x0) * panel_w,
                    top + panel_h - (point[1] - y0) / (y1 - y0) * panel_h)

        _text(drawing, title, left + panel_w / 2, top - 10, size=15, bold=True)
        _line(drawing, left, top + panel_h, left + panel_w, top + panel_h, stroke=MUTED, width=1)
        _line(drawing, left, top, left, top + panel_h, stroke=MUTED, width=1)
        _text(drawing, across, left + panel_w, top + panel_h + 14, anchor="end", size=10,
              fill=MUTED)
        _text(drawing, up, left + 4, top + 10, anchor="start", size=10, fill=MUTED)
        for number, (a, b, c) in enumerate((first, second)):
            segment = _clip(a, b, c, box)
            start, end = at(segment[0]), at(segment[1])
            if number == 0:
                _line(drawing, *start, *end, width=4 if title == "everywhere" else 2.2)
            else:
                _line(drawing, *start, *end, width=2.2, dash="7,4",
                      stroke=PAPER if title == "everywhere" else INK)
        determinant = first[0] * second[1] - second[0] * first[1]
        if determinant:
            x = (first[2] * second[1] - second[2] * first[1]) / determinant
            y = (first[0] * second[2] - second[0] * first[2]) / determinant
            px, py = at((x, y))
            drawing.add(drawing.circle((round(px, 2), round(py, 2)), 5, fill=FILL_AMBER,
                                       stroke=INK, stroke_width=1.4))
            _text(drawing, f"({_number(x)}, {_number(y)})", px + 8, py - 8, anchor="start",
                  size=SMALL_PT)
        lines = {"once": "the lines cross at one point",
                 "never": "parallel: they never meet",
                 "everywhere": "the same line, drawn twice"}
        _text(drawing, lines[title], left + panel_w / 2, top + panel_h + 34, size=SMALL_PT)
        _text(drawing, f"determinant {_number(determinant)}", left + panel_w / 2,
              top + panel_h + 54, size=SMALL_PT, fill=MUTED)
    return drawing.tostring()


# --------------------------------------------------------------------------
# Unit 8: geometry and trigonometry
# --------------------------------------------------------------------------

def _assigned(code: str, name: str) -> float:
    match = re.search(rf"^{name} = (-?[\d.]+)", code, re.M)
    if match is None:
        raise SystemExit(f"no number assigned to {name!r} any more")
    return float(match.group(1))


def _dimension(drawing, x1, y1, x2, y2, label: str, *, side: float = 14,
               size: float = LABEL_PT, anchor: str = "middle", fill=INK) -> None:
    """A measurement line with arrows at both ends, and its label beside it."""
    _arrow(drawing, x1, y1, x2, y2, width=1.1, head=6, both=True, stroke=MUTED)
    length = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / length, (x2 - x1) / length
    _text(drawing, label, (x1 + x2) / 2 + nx * side, (y1 + y2) / 2 + ny * side + 4,
          size=size, anchor=anchor, fill=fill)


def the_ramp_from_the_side() -> str:
    """*Straight lines*: the hall's ramp, drawn to scale from the side.

    The page opens with "Picture the ramp from the side". Rise and run
    are the cell's two numbers, and the picture is to scale, so the ramp
    looks as gentle, or as steep, as 1 in 10 is. The slope itself is left
    off: the page asks for a guess first.
    """
    code = _cell_code("straight-lines", "straight-ramp-1")
    rise, run = _assigned(code, "rise"), _assigned(code, "run")
    scale = 150                          # pixels to the metre, both ways
    left = MARGIN + 20
    ground = MARGIN + 60 + rise * scale
    ramp_end = left + run * scale
    step_w = 90
    width = ramp_end + step_w + 150 + MARGIN
    height = ground + 60
    drawing = _drawing(width, height)
    drawing.add(drawing.polygon([(left, ground), (ramp_end, ground),
                                 (ramp_end, ground - rise * scale)],
                                fill=FILL_BLUE, stroke=INK, stroke_width=1.6))
    _box(drawing, ramp_end, ground - rise * scale, step_w, rise * scale, fill=PANEL, width=1.6,
         rx=0)
    _text(drawing, "step", ramp_end + step_w / 2, ground - rise * scale / 2 + 5, size=SMALL_PT)
    _line(drawing, MARGIN, ground, ramp_end + step_w + 20, ground, width=2)
    _text(drawing, "door", ramp_end + 8, ground - rise * scale - 26, anchor="start",
          size=SMALL_PT, fill=MUTED)
    _line(drawing, ramp_end, ground - rise * scale, ramp_end, ground - rise * scale - 44, width=3)
    _dimension(drawing, left, ground + 16, ramp_end, ground + 16,
               f"run, or going: {_number(run)} m", side=16)
    right = ramp_end + step_w + 26
    _dimension(drawing, right, ground, right, ground - rise * scale, "", side=0)
    _text(drawing, f"rise: {_number(rise)} m", right + 12, ground - rise * scale / 2 + 5,
          anchor="start")
    _text(drawing, "Drawn to scale: one metre is the same length across and up.",
          MARGIN, MARGIN + 12, anchor="start", size=SMALL_PT, fill=MUTED)
    return drawing.tostring()


def the_gap_between_two_circles() -> str:
    """*How far apart?*: the ball and the player as two circles, before they touch.

    Along the line between the centres, the player's radius, then the
    gap, then the ball's radius. The page states this in a paragraph and
    then as `d <= r1 + r2`; the picture puts the three lengths end to end
    so the sum can be seen.
    """
    across = _cell_code("how-far-apart", "how-far-across-1")
    hit = _cell_code("how-far-apart", "how-far-hit-1")
    player = eval(re.search(r"^player = (\(.*\))$", across, re.M).group(1))
    ball = eval(re.search(r"^ball = (\(.*\))$", across, re.M).group(1))
    ball_r, player_r = _assigned(hit, "ball_radius"), _assigned(hit, "player_radius")
    apart = math.dist(player, ball)
    gap = apart - ball_r - player_r

    scale = 4.2
    width = 640
    height = 2 * MARGIN + (player_r + abs(ball[1] - player[1]) + ball_r) * scale + 40
    drawing = _drawing(width, height)
    px, py = MARGIN + 20 + player_r * scale, height - MARGIN - 10 - player_r * scale

    def at(point):
        return (px + (point[0] - player[0]) * scale, py - (point[1] - player[1]) * scale)

    bx, by = at(ball)
    drawing.add(drawing.circle((round(px, 2), round(py, 2)), player_r * scale, fill=FILL_BLUE,
                               stroke=INK, stroke_width=1.6))
    drawing.add(drawing.circle((round(bx, 2), round(by, 2)), ball_r * scale, fill=FILL_AMBER,
                               stroke=INK, stroke_width=1.6))
    _text(drawing, "player", px - 18, py + 32, size=14)
    _text(drawing, "ball", bx + 4, by - ball_r * scale - 10, size=14)
    ux, uy = (bx - px) / (apart * scale), (by - py) / (apart * scale)
    edge_player = (px + ux * player_r * scale, py + uy * player_r * scale)
    edge_ball = (bx - ux * ball_r * scale, by - uy * ball_r * scale)
    for x, y in ((px, py), (bx, by)):
        drawing.add(drawing.circle((round(x, 2), round(y, 2)), 3.2, fill=INK))
    _line(drawing, px, py, *edge_player, width=2.4)
    _line(drawing, *edge_player, *edge_ball, width=2, dash="5,4")
    _line(drawing, *edge_ball, bx, by, width=2.4)
    nx, ny = -uy, ux                          # to the lower right of the centre line

    def label(a, b, text, side=16, anchor="start"):
        _text(drawing, text, (a[0] + b[0]) / 2 + nx * side, (a[1] + b[1]) / 2 + ny * side + 4,
              anchor=anchor, size=14)

    label((px, py), edge_player, f"{_number(player_r)}")
    label(edge_player, edge_ball, f"gap {_number(gap)}")
    label(edge_ball, (bx, by), f"{_number(ball_r)}")
    text_x = width - MARGIN - 250
    rows = [
        (f"between the centres: {_number(apart)}", INK),
        (f"the two radii: {_number(player_r)} + {_number(ball_r)} = "
         f"{_number(player_r + ball_r)}", INK),
        (f"{_number(apart)} {MINUS} {_number(player_r + ball_r)} = {_number(gap)}, "
         "a gap between", MUTED),
        ("the edges, so they do not touch.", MUTED),
    ]
    for place, (row, colour) in enumerate(rows):
        _text(drawing, row, text_x, height - MARGIN - 110 + place * 22, anchor="start",
              fill=colour)
    return drawing.tostring()


def _plane(drawing, cx, cy, scale, reach=1.35):
    _arrow(drawing, cx - reach * scale, cy, cx + reach * scale, cy, stroke=MUTED, width=1.1,
           head=6)
    _arrow(drawing, cx, cy + reach * scale, cx, cy - reach * scale, stroke=MUTED, width=1.1,
           head=6)
    drawing.add(drawing.circle((round(cx, 2), round(cy, 2)), scale, fill="none", stroke=INK,
                               stroke_width=1.5))


def _angle_arc(drawing, cx, cy, radius, start, end, *, width=1.3):
    """An arc about (cx, cy) from angle `start` to `end`, maths angles, y up."""
    x1, y1 = cx + radius * math.cos(start), cy - radius * math.sin(start)
    x2, y2 = cx + radius * math.cos(end), cy - radius * math.sin(end)
    large = 1 if (end - start) % (2 * math.pi) > math.pi else 0
    drawing.add(drawing.path(
        d=f"M {x1:.2f} {y1:.2f} A {radius} {radius} 0 {large} 0 {x2:.2f} {y2:.2f}",
        fill="none", stroke=INK, stroke_width=width))


UNIT_CIRCLE_ANGLE = 40      # degrees: any angle short of 90 shows both parts clearly


def a_point_on_the_unit_circle() -> str:
    """*Going round in circles*: cos θ across, sin θ up, for one point on the circle.

    The angle is not one of the page's; its three exact angles are found
    later from their own pictures, so this one stays general.
    """
    scale = 125
    width, height = 660, 2 * MARGIN + 2 * 1.3 * scale + 10
    cx, cy = MARGIN + 44 + 1.3 * scale, height / 2
    drawing = _drawing(width, height)
    _plane(drawing, cx, cy, scale, reach=1.3)
    theta = math.radians(UNIT_CIRCLE_ANGLE)
    x, y = cx + scale * math.cos(theta), cy - scale * math.sin(theta)
    _line(drawing, cx, cy, x, y, width=2)
    _line(drawing, cx, cy, x, cy, width=4, stroke=INK)
    _line(drawing, x, cy, x, y, width=2.2, dash="6,4")
    _box(drawing, x - 10, cy - 10, 10, 10, fill="none", width=1, rx=0)
    _angle_arc(drawing, cx, cy, 34, 0, theta)
    _text(drawing, "θ", cx + 44 * math.cos(theta / 2), cy - 44 * math.sin(theta / 2) + 5,
          size=15, italic=True)
    drawing.add(drawing.circle((round(x, 2), round(y, 2)), 5.5, fill=FILL_AMBER, stroke=INK,
                               stroke_width=1.4))
    _text(drawing, "(cos θ, sin θ)", x + 10, y - 10, anchor="start", size=14)
    _text(drawing, "1", (cx + x) / 2 - 10, (cy + y) / 2 - 6, anchor="end", size=14)
    _text(drawing, "cos θ: across", (cx + x) / 2, cy + 20, size=13)
    _text(drawing, "sin θ: up", x + 8, (cy + y) / 2 + 5, anchor="start", size=13)
    for (px, py), text, anchor, dx, dy in (((1, 0), "(1, 0)", "start", 6, 18),
                                            ((0, 1), "(0, 1)", "start", 8, -6),
                                            ((-1, 0), f"({MINUS}1, 0)", "end", -6, 18),
                                            ((0, -1), f"(0, {MINUS}1)", "start", 8, 16)):
        _text(drawing, text, cx + px * scale + dx, cy - py * scale + dy, anchor=anchor,
              size=SMALL_PT, fill=MUTED)
    text_x = cx + 1.3 * scale + 34
    for place, row in enumerate(["The circle has radius 1.",
                                 "θ is measured from (1, 0),",
                                 "turning anticlockwise.",
                                 "",
                                 "How far across is cos θ.",
                                 "How far up is sin θ."]):
        _text(drawing, row, text_x, cy - 50 + place * 21, anchor="start",
              fill=INK if place >= 4 else MUTED)
    return drawing.tostring()


def one_radian() -> str:
    """*Going round in circles*: one radian, and how many fit in a whole turn.

    The arc for one radian is as long as the radius. Ticks at 1, 2, 3 ...
    radians round the circle show that six fit, with a little over, since
    a whole turn is 2π.
    """
    scale = 112
    width, height = 660, 2 * MARGIN + 2 * 1.35 * scale
    cx, cy = MARGIN + 36 + 1.3 * scale, height / 2
    drawing = _drawing(width, height)
    drawing.add(drawing.circle((round(cx, 2), round(cy, 2)), scale, fill="none", stroke=INK,
                               stroke_width=1.3))
    end = (cx + scale * math.cos(1), cy - scale * math.sin(1))
    drawing.add(drawing.path(
        d=f"M {cx + scale:.2f} {cy:.2f} A {scale} {scale} 0 0 0 {end[0]:.2f} {end[1]:.2f}",
        fill="none", stroke=INK, stroke_width=6))
    _line(drawing, cx, cy, cx + scale, cy, width=2)
    _line(drawing, cx, cy, *end, width=2)
    _text(drawing, "radius 1", cx + scale / 2, cy + 18, size=13)
    _text(drawing, "1", (cx + end[0]) / 2 - 8, (cy + end[1]) / 2 + 2, anchor="end", size=13)
    arc_label = 1.2 * scale
    _text(drawing, "arc: 1", cx + arc_label * math.cos(0.5), cy - arc_label * math.sin(0.5) + 4,
          anchor="start", size=13)
    _angle_arc(drawing, cx, cy, 26, 0, 1)
    whole = 2 * math.pi
    for tick in range(1, int(whole) + 1):
        inner, outer = scale - 7, scale + 7
        _line(drawing, cx + inner * math.cos(tick), cy - inner * math.sin(tick),
              cx + outer * math.cos(tick), cy - outer * math.sin(tick), width=2)
        if tick > 1:
            label_r = scale + 20
            _text(drawing, str(tick), cx + label_r * math.cos(tick),
                  cy - label_r * math.sin(tick) + 5, size=SMALL_PT, fill=MUTED)
    text_x = cx + 1.35 * scale + 30
    rows = [
        (f"1 radian is about {_number(math.degrees(1), 1)}°.", INK),
        ("The arc is as long as the radius.", INK),
        ("", INK),
        ("The ticks are 1, 2, 3 ... radians", MUTED),
        (f"round. A whole turn is 2π, about {_number(whole)},", MUTED),
        ("so six fit, and a little more.", MUTED),
    ]
    for place, (row, colour) in enumerate(rows):
        _text(drawing, row, text_x, cy - 56 + place * 21, anchor="start", fill=colour)
    return drawing.tostring()


def measuring_the_tree() -> str:
    """*Solving triangles*: you, the tree, and the triangle between, to scale.

    The page adds 1.6 m after the tangent because the triangle starts at
    your eyes, not at the ground; the picture shows where that 1.6 m is.
    The height above your eyes is left as a question mark: the page asks
    for a guess before the cell runs.
    """
    code = _cell_code("how-tall-is-that-tree", "how-tall-tree-1")
    distance = _assigned(code, "distance_to_trunk")
    angle = _assigned(code, "angle_up")
    eye = _assigned(code, "eye_height")
    above = distance * math.tan(math.radians(angle))

    scale = 14.5
    left = MARGIN + 80
    ground = MARGIN + 30 + (above + eye) * scale
    width, height = 620, ground + 48
    drawing = _drawing(width, height)
    trunk_x = left + distance * scale
    eye_y = ground - eye * scale
    top_y = eye_y - above * scale
    _line(drawing, MARGIN, ground, trunk_x + 3.4 * scale + 10, ground, width=2)
    # the tree: a trunk, and a crown whose top is the point we look at
    drawing.add(drawing.ellipse((round(trunk_x, 2), round(top_y + 4.2 * scale, 2)),
                                (3.4 * scale, 4.2 * scale), fill=FILL_GREEN, stroke=INK,
                                stroke_width=1.3))
    _line(drawing, trunk_x, ground, trunk_x, top_y + 7 * scale, width=5)
    drawing.add(drawing.circle((round(trunk_x, 2), round(top_y, 2)), 4, fill=INK))
    # you: a figure whose eyes are eye_height above the ground
    head_r = 0.22 * scale
    _line(drawing, left, ground, left, eye_y + head_r * 2, width=2.2)
    drawing.add(drawing.circle((round(left, 2), round(eye_y + head_r * 0.6, 2)), head_r,
                               fill=PANEL, stroke=INK, stroke_width=1.6))
    _line(drawing, left, eye_y, trunk_x, eye_y, width=1.5, dash="6,4")
    _line(drawing, left, eye_y, trunk_x, top_y, width=2)
    _box(drawing, trunk_x - 9, eye_y - 9, 9, 9, fill="none", width=1, rx=0)
    _angle_arc(drawing, left, eye_y, 46, 0, math.radians(angle))
    _text(drawing, f"{_number(angle)}°", left + 54, eye_y - 8, anchor="start", size=14)
    _text(drawing, "level", (left + trunk_x) / 2, eye_y + 17, size=SMALL_PT, fill=MUTED)
    slope_angle = math.atan2(eye_y - top_y, trunk_x - left)
    mx, my = (left + trunk_x) / 2, (eye_y + top_y) / 2
    _text(drawing, "line of sight", mx - 8 * math.sin(slope_angle) - 6,
          my - 8 * math.cos(slope_angle), anchor="end", size=SMALL_PT, fill=MUTED)
    _dimension(drawing, left, ground + 18, trunk_x, ground + 18,
               f"{_number(distance)} m to the trunk", side=16)
    beside = trunk_x + 3.4 * scale + 16
    _dimension(drawing, beside, eye_y, beside, top_y, "", side=0)
    _text(drawing, "? m above", beside + 10, (eye_y + top_y) / 2, anchor="start", size=14)
    _text(drawing, "your eyes", beside + 10, (eye_y + top_y) / 2 + 18, anchor="start", size=14)
    _text(drawing, "you", left + 10, ground - 6, anchor="start", size=SMALL_PT, fill=MUTED)
    _dimension(drawing, left - 30, ground, left - 30, eye_y, "", side=0)
    _text(drawing, f"{_number(eye)} m", left - 38, (ground + eye_y) / 2 + 5, anchor="end",
          size=14)
    _dimension(drawing, beside, ground, beside, eye_y, "", side=0)
    _text(drawing, f"{_number(eye)} m", beside + 10, (ground + eye_y) / 2 + 5, anchor="start",
          size=14)
    return drawing.tostring()


def across_the_river() -> str:
    """*Solving triangles*: the oak across the river, and the triangle A, B, T.

    Drawn to scale from the page's numbers, with T placed by the sine
    rule the page uses. The 40° at B is outside the triangle and the 140°
    inside it; the picture shows both, since the page's argument turns on
    which is which.
    """
    code = _cell_code("how-tall-is-that-tree", "how-tall-sine-1")
    walked = _assigned(code, "walked")
    at_a = _assigned(code, "angle_at_a")
    outside_b = float(re.search(r"^angle_at_b = 180 - ([\d.]+)", code, re.M).group(1))
    inside_b = 180 - outside_b
    at_top = 180 - at_a - inside_b
    b_to_top = walked * math.sin(math.radians(at_a)) / math.sin(math.radians(at_top))
    top = (b_to_top * math.cos(math.radians(outside_b)), b_to_top * math.sin(math.radians(outside_b)))
    if round(at_top) != 12 or round(b_to_top, 1) != 33.9:
        raise SystemExit("how-tall-is-that-tree: the river triangle's numbers changed")

    scale = 12.5
    width = 620
    left = MARGIN + 30
    ground = MARGIN + 30 + top[1] * scale
    height = ground + 56

    def at(point):
        return (left + (point[0] + walked) * scale, ground - point[1] * scale)

    drawing = _drawing(width, height)
    a, b, t = at((-walked, 0)), at((0, 0)), at(top)
    foot = at((top[0], 0))
    river_from, river_to = at((4, 0))[0], at((top[0] - 4, 0))[0]
    _box(drawing, river_from, ground - 1, river_to - river_from, 12, fill=FILL_BLUE, stroke="none",
         rx=2)
    _text(drawing, "river", (river_from + river_to) / 2, ground + 28, size=SMALL_PT, fill=MUTED)
    _line(drawing, MARGIN, ground, foot[0] + 50, ground, width=2)
    drawing.add(drawing.ellipse((round(t[0], 2), round(t[1] + 3.2 * scale, 2)),
                                (2.6 * scale, 3.2 * scale), fill=FILL_GREEN, stroke=INK,
                                stroke_width=1.2))
    _line(drawing, foot[0], ground, foot[0], t[1] + 5.5 * scale, width=5)
    drawing.add(drawing.polygon([a, b, t], fill="none", stroke=INK, stroke_width=2))
    _line(drawing, b[0], b[1], b[0] + 70, b[1], width=1.2, dash="5,4")
    for point in (a, b, t):
        drawing.add(drawing.circle((round(point[0], 2), round(point[1], 2)), 4, fill=INK))
    _text(drawing, "A", a[0] - 4, a[1] + 20, size=15, bold=True)
    _text(drawing, "B", b[0] - 4, b[1] + 20, size=15, bold=True)
    _text(drawing, "T", t[0] + 12, t[1] - 4, size=15, bold=True, anchor="start")
    _dimension(drawing, a[0], ground + 36, b[0], ground + 36, f"{_number(walked)} m walked",
               side=15)
    rad = math.radians
    _angle_arc(drawing, a[0], a[1], 60, 0, rad(at_a))
    _text(drawing, f"{_number(at_a)}°", a[0] + 66, a[1] - 9, anchor="start", size=14)
    _angle_arc(drawing, b[0], b[1], 30, 0, rad(outside_b))
    _text(drawing, f"{_number(outside_b)}° outside", b[0] + 40, b[1] - 8, anchor="start",
          size=13)
    _angle_arc(drawing, b[0], b[1], 18, rad(outside_b), math.pi)
    _text(drawing, f"{_number(inside_b)}° inside", b[0] - 12, b[1] - 28, anchor="end",
          size=13)
    toward_a = math.atan2(-(a[1] - t[1]), a[0] - t[0])
    toward_b = math.atan2(-(b[1] - t[1]), b[0] - t[0])
    _angle_arc(drawing, t[0], t[1], 70, toward_a, toward_b)
    middle = (toward_a + toward_b) / 2
    _text(drawing, f"{_number(at_top)}°", t[0] + 84 * math.cos(middle),
          t[1] - 84 * math.sin(middle) + 5, anchor="end", size=14)
    return drawing.tostring()


# --------------------------------------------------------------------------
# Unit 9: the derivative
# --------------------------------------------------------------------------

def halfway_to_the_door() -> str:
    """*Getting closer*: the first walks towards the door, one row each.

    The distances are the ones the page's cell prints. The part still to
    go halves on every row and never reaches nothing, which is what the
    page's limit is about.
    """
    code = _cell_code("getting-closer", "getting-closer-door-1")
    door = _assigned(code, "door")
    _, printed = _run_cells("getting-closer", "getting-closer-door-1")
    walks = [(int(w), float(d)) for w, d in
             (line.split() for line in printed["getting-closer-door-1"].splitlines())]
    shown = walks[:5]
    scale = 44
    left = MARGIN + 60
    row_h = 38
    top = MARGIN + 30
    width = 620
    height = top + len(shown) * row_h + MARGIN
    drawing = _drawing(width, height)
    door_x = left + door * scale
    _line(drawing, door_x, top - 16, door_x, top + len(shown) * row_h - 12, width=3.5)
    _text(drawing, "0 m", left, top - 20, size=SMALL_PT, fill=MUTED)
    _text(drawing, f"the door, {_number(door)} m", door_x, top - 20, size=SMALL_PT, fill=MUTED)
    previous = 0.0
    for place, (walk, walked) in enumerate(shown):
        y = top + place * row_h
        _text(drawing, f"walk {walk}", MARGIN, y + 13, anchor="start", fill=MUTED)
        _box(drawing, left, y, walked * scale, 18, fill=FILL_BLUE, width=1.2, rx=0)
        _box(drawing, left + previous * scale, y, (walked - previous) * scale, 18,
             fill=FILL_AMBER, width=1.2, rx=0)
        _box(drawing, left + walked * scale, y, (door - walked) * scale, 18, fill="none",
             width=1, rx=0, dash="3,2")
        if place == 0:
            _text(drawing, "this walk", left + walked * scale / 2, y + 13, size=SMALL_PT)
        _text(drawing, f"{_number(walked, 4)} m walked, {_number(door - walked, 4)} m to go",
              door_x + 14, y + 13, anchor="start", size=SMALL_PT)
        previous = walked
    return drawing.tostring()


def the_product_rule_rectangle() -> str:
    """*Rules for change*: a rectangle whose two sides both grow a little.

    The page describes the change in area as three pieces: a strip along
    each side, and a tiny corner. The sizes here are chosen to make the
    pieces visible, and they are labelled in words, since the argument is
    about any two rules f and g.
    """
    f, g, change_f, change_g = 5.0, 3.0, 0.8, 0.6
    scale = 52
    left, top = MARGIN + 70, MARGIN + 30
    w, h, dw, dh = f * scale, g * scale, change_f * scale, change_g * scale
    width, height = 640, top + h + dh + 80
    drawing = _drawing(width, height)
    _box(drawing, left, top, w, h, fill=PANEL, width=1.6, rx=0)
    _box(drawing, left + w, top, dw, h, fill=FILL_BLUE, width=1.6, rx=0)
    _box(drawing, left, top + h, w, dh, fill=FILL_BLUE, width=1.6, rx=0)
    _box(drawing, left + w, top + h, dw, dh, fill=FILL_AMBER, width=1.6, rx=0)
    _text(drawing, "f(x) × g(x)", left + w / 2, top + h / 2 + 5, size=15)
    _text(drawing, "the area before", left + w / 2, top + h / 2 + 24, size=SMALL_PT, fill=MUTED)
    _text(drawing, "f(x) × change in g", left + w / 2, top + h + dh / 2 + 5, size=13)
    _text(drawing, "f(x)", left + w / 2, top - 10, size=14)
    _text(drawing, "change in f", left + w + dw / 2, top - 10, size=SMALL_PT, fill=MUTED)
    _text(drawing, "g(x)", left - 10, top + h / 2 + 5, size=14, anchor="end")
    _text(drawing, "change", left - 10, top + h + dh / 2, size=SMALL_PT, fill=MUTED, anchor="end")
    _text(drawing, "in g", left - 10, top + h + dh / 2 + 13, size=SMALL_PT, fill=MUTED,
          anchor="end")
    text_x = left + w + dw + 34
    _line(drawing, left + w + dw / 2, top + h * 0.3, text_x - 6, top + h * 0.3, stroke=MUTED,
          width=1)
    _text(drawing, "g(x) × change in f", text_x, top + h * 0.3 + 5, anchor="start", size=13)
    _line(drawing, left + w + dw / 2, top + h + dh / 2, text_x - 6, top + h + dh + 26,
          stroke=MUTED, width=1)
    _text(drawing, "the corner: change × change", text_x, top + h + dh + 30, anchor="start",
          size=13)
    _text(drawing, "For a very small change, it is", text_x, top + h + dh + 48, anchor="start",
          size=SMALL_PT, fill=MUTED)
    _text(drawing, "so small that it disappears.", text_x, top + h + dh + 64, anchor="start",
          size=SMALL_PT, fill=MUTED)
    return drawing.tostring()


def rates_that_multiply() -> str:
    """*Rules for change*: the ripple's two rates, one after the other.

    Seconds go into `ripple_radius`, metres come out and go into
    `circle_area`. Each rule has its own rate at that point, and the page's
    chain rule multiplies them. The numbers are the page's, at 6 seconds.
    """
    code = _cell_code("rules-for-change", "rules-for-chain-1")
    growth = float(re.search(r"return ([\d.]+) \* seconds", code).group(1))
    seconds = int(re.search(r"chain_rule_slope\((\d+)\)", code).group(1))
    radius = growth * seconds
    area = math.pi * radius ** 2
    area_rate = 2 * math.pi * radius
    together = area_rate * growth
    width, height = 660, 230
    drawing = _drawing(width, height)
    y = MARGIN + 50
    stops = [(f"{seconds} s", None), ("ripple_radius", "rule"), (f"{_number(radius)} m", None),
             ("circle_area", "rule"), (f"{_number(area)} m²", None)]
    widths = [64, 136, 64, 124, 96]
    gap = (width - 2 * MARGIN - sum(widths)) / (len(widths) - 1)
    x = MARGIN
    centres = []
    for (label, kind), box_w in zip(stops, widths):
        if kind == "rule":
            _box(drawing, x, y - 20, box_w, 40, fill=PANEL, width=1.4, rx=6)
            _text(drawing, label, x + box_w / 2, y + 5, mono=True, size=13)
        else:
            _text(drawing, label, x + box_w / 2, y + 5, size=15, bold=True)
        centres.append((x, x + box_w))
        x += box_w + gap
    for (_, right), (left, _) in zip(centres, centres[1:]):
        _arrow(drawing, right + 4, y, left - 4, y, head=7, width=1.4)
    rate_y = y + 54
    first = centres[1]
    second = centres[3]
    _text(drawing, f"+{_number(growth)} m", (first[0] + first[1]) / 2, rate_y, size=14)
    _text(drawing, "for each second", (first[0] + first[1]) / 2, rate_y + 18, size=SMALL_PT,
          fill=MUTED)
    _text(drawing, f"+2π {TIMES} {_number(radius)} ≈ {_number(area_rate)} m²",
          (second[0] + second[1]) / 2, rate_y, size=14)
    _text(drawing, "for each metre of radius", (second[0] + second[1]) / 2, rate_y + 18,
          size=SMALL_PT, fill=MUTED)
    _text(drawing, f"{_number(growth)} {TIMES} {_number(area_rate)} ≈ {_number(together)} "
          "m² for each second", width / 2, rate_y + 64, size=15, bold=True)
    _text(drawing, "The metres cancel: the two rates multiply.", width / 2, rate_y + 86,
          size=SMALL_PT, fill=MUTED)
    if round(together, 2) != round(3 * math.pi, 2):
        raise SystemExit("rules-for-change: the ripple's rate is no longer 3π")
    return drawing.tostring()


def bisection_squeeze() -> str:
    """*Solving by computing*: the first steps of bisection, as intervals.

    Every row is `low` to `high` as the page's loop prints them, on one
    number line from 1 to 2, with √2 marked through all of them. The
    shaded piece halves on each row and always holds the dashed line.
    """
    _, printed = _run_cells("solving-by-computing", "solving-by-squeeze-1",
                            "solving-by-bisect-1", given={"plot_rule": lambda *a, **k: None})
    steps = []
    for line in printed["solving-by-bisect-1"].splitlines():
        step, low, high = line.split()[:3]
        steps.append((int(step), float(low), float(high)))
    shown = [(0, 1.0, 2.0)] + steps[:6]
    root = math.sqrt(2)
    scale = 440
    left = MARGIN + 66
    top = MARGIN + 40
    row_h = 30
    width = 640
    height = top + len(shown) * row_h + MARGIN + 6
    drawing = _drawing(width, height)

    def at(value):
        return left + (value - 1) * scale

    for tenth in range(11):
        x = at(1 + tenth / 10)
        _line(drawing, x, top - 10, x, top - 4, stroke=MUTED, width=1)
        if tenth % 2 == 0:
            _text(drawing, _number(1 + tenth / 10, 1), x, top - 14, size=10.5, fill=MUTED)
    for place, (step, low, high) in enumerate(shown):
        y = top + place * row_h
        if not low <= root <= high:
            raise SystemExit("solving-by-computing: a step lost the root")
        _line(drawing, at(1), y + 9, at(2), y + 9, stroke=RULE, width=1)
        _box(drawing, at(low), y, (high - low) * scale, 18, fill=FILL_AMBER, width=1.3, rx=0)
        _text(drawing, "start" if step == 0 else f"step {step}", MARGIN, y + 13,
              anchor="start", fill=MUTED)
        _text(drawing, f"gap {_number(high - low, 6)}", at(2) + 14, y + 13, anchor="start",
              size=SMALL_PT)
    x = at(root)
    _line(drawing, x, top - 2, x, top + len(shown) * row_h - 6, width=1.5, dash="4,3")
    _text(drawing, f"√2 ≈ {_number(root, 5)}", x + 6, top + len(shown) * row_h + 8,
          anchor="start", size=SMALL_PT)
    return drawing.tostring()


# --------------------------------------------------------------------------
# Unit 10: programming, then and now
# --------------------------------------------------------------------------

def one_list_two_names() -> str:
    """*Code other people can read*: `log_c` and `l` are two names for one list.

    Before and after `l.sort()`, both read from the page's own cell: the
    log as the page writes it, and the log after the call. Both names
    point at the same list, so the sort changes what the caller sees.
    """
    code = _cell_code("code-other-people-can-read", "code-other-stranger-1")
    before = eval(re.search(r"^log_c = (\[.*\])$", code, re.M).group(1))
    space, _ = _run_cells("code-other-people-can-read", "code-other-stranger-1")
    after = space["log_c"]
    if after == before or after != sorted(before):
        raise SystemExit("code-other-people-can-read: m no longer sorts the caller's list")
    cell_w, cell_h = 58, 32
    width = 620
    panel_h = 110
    height = 2 * MARGIN + 2 * panel_h + 10
    drawing = _drawing(width, height)
    list_x = MARGIN + 250
    for place, (title, values) in enumerate((("before l.sort()", before),
                                             ("after l.sort()", after))):
        top = MARGIN + place * (panel_h + 10)
        _text(drawing, title, MARGIN, top + 14, anchor="start", bold=True, mono=True, size=13)
        list_y = top + 44
        for index, value in enumerate(values):
            _box(drawing, list_x + index * cell_w, list_y, cell_w, cell_h,
                 fill=FILL_AMBER if place == 1 else PANEL, width=1.3, rx=0)
            _text(drawing, _number(value, 1) if value != int(value) else f"{value:.1f}",
                  list_x + index * cell_w + cell_w / 2, list_y + cell_h / 2 + 5, mono=True)
        for row, (name, note) in enumerate((("log_c", "the caller's name"),
                                            ("l", "m's name, inside m"))):
            y = top + 36 + row * 36
            _box(drawing, MARGIN, y - 13, 60, 24, fill=PANEL, width=1.2, rx=4)
            _text(drawing, name, MARGIN + 30, y + 4, mono=True)
            _text(drawing, note, MARGIN + 70, y + 4, anchor="start", size=SMALL_PT, fill=MUTED)
            _arrow(drawing, MARGIN + 186, y, list_x - 4, list_y + cell_h / 2 + (row - 0.5) * 12,
                   head=7, width=1.3)
    return drawing.tostring()


def from_code_to_running() -> str:
    """*Many languages, one idea*: four ways a program gets from its text to running.

    The four the page names in its paragraph on compilers and
    interpreters: a compiler, an interpreter, Python's two steps, and a
    browser's JavaScript engine compiling while it runs. No numbers here,
    only the page's own words, laid out so the four can be compared.
    """
    lanes = [
        ("A compiler: the first BASIC, at Dartmouth",
         ["your code", "compiler: translates it all first", "machine instructions, then run"]),
        ("An interpreter: BASIC on a Spectrum or a Commodore 64",
         ["your code", "interpreter: reads a line, does it, reads the next"]),
        ("Python",
         ["your cell", "compiled to simpler instructions", "interpreter: runs those"]),
        ("JavaScript in Chrome",
         ["your code", "interpreter: starts running it", "while it runs, the parts that run "
          "most often are compiled to machine instructions"]),
    ]
    width = 680
    lane_h = 86
    height = 2 * MARGIN + len(lanes) * lane_h
    drawing = _drawing(width, height)
    for place, (title, steps) in enumerate(lanes):
        top = MARGIN + place * lane_h
        _text(drawing, title, MARGIN, top + 14, anchor="start", bold=True, size=13)
        box_y = top + 24
        box_h = 48
        widths = [96] + [(width - 2 * MARGIN - 96 - 30 * (len(steps) - 1)) / (len(steps) - 1)] * (
            len(steps) - 1)
        x = MARGIN
        for number, (step, box_w) in enumerate(zip(steps, widths)):
            _box(drawing, x, box_y, box_w, box_h, fill=PANEL if number else FILL_AMBER,
                 width=1.3, rx=6)
            words = step.split()
            lines, current = [], ""
            for word in words:
                trial = (current + " " + word).strip()
                if _width(trial, 12.5) > box_w - 14 and current:
                    lines.append(current)
                    current = word
                else:
                    current = trial
            lines.append(current)
            for row, text in enumerate(lines):
                _text(drawing, text, x + box_w / 2,
                      box_y + box_h / 2 + 4.5 + (row - (len(lines) - 1) / 2) * 15, size=12.5)
            if number < len(steps) - 1:
                _arrow(drawing, x + box_w + 4, box_y + box_h / 2, x + box_w + 26,
                       box_y + box_h / 2, head=7, width=1.4)
            x += box_w + 30
    return drawing.tostring()


# --------------------------------------------------------------------------

DIAGRAMS = {
    "finding-things-fast/halving-the-contacts.svg": halving_the_contacts,
    "finding-things-fast/searching-unsorted-contacts.svg": searching_the_unsorted_list,
    "sorting-a-hand-of-cards/selection-rounds.svg": selection_rounds,
    "sorting-a-hand-of-cards/insertion-rounds.svg": insertion_rounds,
    "racing-the-sorts/shell-sort-gaps.svg": shell_gaps,
    "a-function-that-calls-itself/holidays-folders.svg": holidays_folders,
    "a-function-that-calls-itself/calls-that-wait.svg": calls_that_wait,
    "doubling-and-halving/one-more-than-all-before.svg": one_more_than_all_before,
    "rules-with-letters-in-them/photo-with-bars.svg": photo_with_bars,
    "rules-with-letters-in-them/the-square-forgotten.svg": the_square_forgotten,
    "solving-for-x/sprite-sheet.svg": sprite_sheet,
    "when-there-is-no-real-answer/quarter-turns.svg": quarter_turns,
    "several-unknowns-at-once/the-determinant.svg": the_determinant,
    "several-unknowns-at-once/once-never-everywhere.svg": once_never_everywhere,
    "straight-lines/ramp-from-the-side.svg": the_ramp_from_the_side,
    "how-far-apart/gap-between-circles.svg": the_gap_between_two_circles,
    "going-round-in-circles/point-on-the-unit-circle.svg": a_point_on_the_unit_circle,
    "going-round-in-circles/one-radian.svg": one_radian,
    "how-tall-is-that-tree/measuring-the-tree.svg": measuring_the_tree,
    "how-tall-is-that-tree/across-the-river.svg": across_the_river,
    "getting-closer/halfway-to-the-door.svg": halfway_to_the_door,
    "rules-for-change/product-rule-rectangle.svg": the_product_rule_rectangle,
    "rules-for-change/rates-that-multiply.svg": rates_that_multiply,
    "solving-by-computing/bisection-squeeze.svg": bisection_squeeze,
    "code-other-people-can-read/one-list-two-names.svg": one_list_two_names,
    "many-languages-one-idea/from-code-to-running.svg": from_code_to_running,
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
