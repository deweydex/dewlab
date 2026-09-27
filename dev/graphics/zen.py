#!/usr/bin/env python3
"""The pictures for The Zen of Slashes and Surds.

    python3 dev/graphics/zen.py          # report what would change
    python3 dev/graphics/zen.py --write  # write it

The module's readers meet each idea as a thing before they meet it as
symbols, the way a Montessori classroom hands a child fraction circles and
golden beads before it writes anything down
(planning/outlines/zen-of-slashes-and-surds.md). These are those things,
drawn: a pizza cut into equal slices, a wall of fraction bars, a sheet of
paper folded again and again, and the golden beads. Later strands add a
number line, a grid cut two ways for a fraction of a fraction, rows of
hearts to count and cancel for the rules of powers, squares and cubes of
beads for roots, and a line of hops for logarithms.

Same rule as the other generators: every count in a picture is computed
here from the numbers the page uses, never typed, so a picture cannot show
five slices where the page says six.
"""

from __future__ import annotations

import argparse
import math
import sys
from fractions import Fraction
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (  # noqa: E402
    FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MUTED, PANEL, SANS,
)

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL_PT = 13
RADIUS = 46
GAP = 34            # between two pizzas in a row
MARGIN = 14


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _label(drawing, text: str, x: float, y: float, *, size: float = LABEL_PT,
           fill: str = INK) -> None:
    drawing.add(drawing.text(text, insert=(x, y), text_anchor="middle",
                             font_size=f"{size}px", fill=fill))


def _point(cx: float, cy: float, radius: float, turn: float) -> tuple[float, float]:
    """A point on the circle, `turn` of the way round clockwise from the top."""
    angle = 2 * math.pi * turn - math.pi / 2
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def _pizza(drawing, cx: float, cy: float, slices: int, shaded: int,
           radius: float = RADIUS) -> None:
    """One pizza cut into `slices` equal slices, the first `shaded` of them filled.

    A slice is filled amber and an empty one is left as the page, so the
    picture reads in every theme: the fill is a highlight tint and the
    lines follow the text colour.
    """
    if shaded >= slices:
        drawing.add(drawing.circle((cx, cy), radius, fill=FILL_AMBER, stroke="none"))
    else:
        for index in range(shaded):
            x0, y0 = _point(cx, cy, radius, index / slices)
            x1, y1 = _point(cx, cy, radius, (index + 1) / slices)
            large = 1 if 1 / slices > 0.5 else 0
            path = drawing.path(d=f"M {cx:.2f} {cy:.2f} L {x0:.2f} {y0:.2f} "
                                  f"A {radius} {radius} 0 {large} 1 {x1:.2f} {y1:.2f} Z",
                                fill=FILL_AMBER, stroke="none")
            drawing.add(path)
    if slices > 1:
        for index in range(slices):
            x, y = _point(cx, cy, radius, index / slices)
            drawing.add(drawing.line((cx, cy), (x, y), stroke=INK, stroke_width=1.4))
    drawing.add(drawing.circle((cx, cy), radius, fill="none", stroke=INK, stroke_width=2.4))


def pizza_row(pizzas: list[tuple[int, int]], labels: list[str] | None = None,
              room_for: int = 1, between: list[str] | None = None) -> str:
    """A row of pizzas, each (slices, shaded), with a label under each.

    `room_for` makes the canvas as wide as that many pizzas and centres
    the row in it. A page scales a picture to its column, so one pizza on
    a canvas of its own is drawn as wide as the page, far bigger than the
    same pizza in a row of four; room for three keeps the sizes close.

    `between` puts a sign in each gap, so a row can read as a sum:
    ["+", "="] between three pizzas.
    """
    count = len(pizzas)
    slots = max(count, room_for)
    width = 2 * MARGIN + slots * 2 * RADIUS + (slots - 1) * GAP
    height = 2 * MARGIN + 2 * RADIUS + (26 if labels else 0)
    drawing = _drawing(width, height)
    offset = (slots - count) * (2 * RADIUS + GAP) / 2
    for place, (slices, shaded) in enumerate(pizzas):
        cx = offset + MARGIN + RADIUS + place * (2 * RADIUS + GAP)
        cy = MARGIN + RADIUS
        _pizza(drawing, cx, cy, slices, shaded)
        if labels:
            _label(drawing, labels[place], cx, cy + RADIUS + 22)
        if between and place < count - 1:
            _label(drawing, between[place], cx + RADIUS + GAP / 2, cy + 9, size=26)
    return drawing.tostring()


BAR_W = 480
BAR_H = 34


def fraction_wall(denominators: list[int], shade: dict[int, int] | None = None) -> str:
    """Bars of the same length, one cut into halves, one into thirds, and so on.

    `shade` maps a denominator to how many of its pieces are filled, so the
    page can show that two quarters cover exactly what one half covers.
    """
    shade = shade or {}
    rows = [1] + denominators
    height = 2 * MARGIN + len(rows) * BAR_H
    drawing = _drawing(BAR_W + 2 * MARGIN, height)
    for row, pieces in enumerate(rows):
        y = MARGIN + row * BAR_H
        piece_w = BAR_W / pieces
        for piece in range(pieces):
            x = MARGIN + piece * piece_w
            filled = piece < shade.get(pieces, 0)
            drawing.add(drawing.rect((x, y), (piece_w, BAR_H),
                                     fill=FILL_AMBER if filled else PANEL,
                                     stroke=INK, stroke_width=1.4))
            text = "1" if pieces == 1 else f"1/{pieces}"
            size = LABEL_PT if piece_w > 40 else 11
            _label(drawing, text, x + piece_w / 2, y + BAR_H / 2 + size / 3, size=size)
    return drawing.tostring()


SHEET_W = 96
SHEET_H = 68


def folded_sheets(folds: int) -> str:
    """A sheet of paper unfolded after 0, 1, 2 … `folds` folds, creases drawn.

    Each fold doubles the number of rectangles the creases make, and halves
    each one. The folds go the long way, then the short way, as a real sheet
    is folded, so the pieces stay close to the sheet's own shape.
    """
    count = folds + 1
    gap = 20            # tighter than a pizza row: five sheets must fit a column
    width = 2 * MARGIN + count * SHEET_W + (count - 1) * gap
    height = 2 * MARGIN + SHEET_H + 52
    drawing = _drawing(width, height)
    for place in range(count):
        x = MARGIN + place * (SHEET_W + gap)
        y = MARGIN
        across = 2 ** ((place + 1) // 2)
        down = 2 ** (place // 2)
        drawing.add(drawing.rect((x, y), (SHEET_W, SHEET_H), fill=PANEL,
                                 stroke=INK, stroke_width=2))
        for cut in range(1, across):
            cx = x + cut * SHEET_W / across
            drawing.add(drawing.line((cx, y), (cx, y + SHEET_H), stroke=INK,
                                     stroke_width=1, stroke_dasharray="4,3"))
        for cut in range(1, down):
            cy = y + cut * SHEET_H / down
            drawing.add(drawing.line((x, cy), (x + SHEET_W, cy), stroke=INK,
                                     stroke_width=1, stroke_dasharray="4,3"))
        middle = x + SHEET_W / 2
        # Five sheets are scaled down to fit a column, so the labels are
        # drawn bigger than a pizza's to stay readable after scaling.
        _label(drawing, f"{place} fold" + ("" if place == 1 else "s"), middle,
               y + SHEET_H + 22, size=16)
        pieces = across * down
        _label(drawing, f"{pieces} piece" + ("" if pieces == 1 else "s"), middle,
               y + SHEET_H + 44, size=16, fill=MUTED)
    return drawing.tostring()


BEAD = 4.2          # a bead's radius
PITCH = 10          # centre to centre


def golden_beads() -> str:
    """The Montessori golden beads: a unit, a ten-bar, a hundred-square, a thousand-cube.

    The cube is drawn as three faces of ten by ten, which is what a child
    sees of the real one; the beads inside are the ones nobody can see, and
    the page asks how many there are.
    """
    ten = 10 * PITCH
    cube_depth = ten * 0.5
    width = 2 * MARGIN + 3 * GAP + PITCH + PITCH + ten + ten + cube_depth
    height = 2 * MARGIN + ten + cube_depth + 44
    drawing = _drawing(width, height)
    base = MARGIN + cube_depth + ten      # the bottom edge every shape stands on

    def bead(x: float, y: float) -> None:
        drawing.add(drawing.circle((x, y), BEAD, fill=FILL_AMBER, stroke=INK,
                                   stroke_width=0.9))

    x = MARGIN
    bead(x + PITCH / 2, base - PITCH / 2)
    _label(drawing, "1", x + PITCH / 2, base + 22)

    x += PITCH + GAP
    for index in range(10):
        bead(x + PITCH / 2, base - ten + PITCH * index + PITCH / 2)
    _label(drawing, "10", x + PITCH / 2, base + 22)

    x += PITCH + GAP
    for row in range(10):
        for col in range(10):
            bead(x + PITCH * col + PITCH / 2, base - ten + PITCH * row + PITCH / 2)
    _label(drawing, "100", x + ten / 2, base + 22)

    x += ten + GAP
    shift = cube_depth / 10
    front = (x, base - ten)
    # The top and right faces, drawn as grids, then the front face of beads.
    for step in range(11):
        drawing.add(drawing.line(
            (front[0] + step * PITCH, front[1]),
            (front[0] + step * PITCH + cube_depth, front[1] - cube_depth),
            stroke=INK, stroke_width=0.8))
        drawing.add(drawing.line(
            (front[0] + step * shift, front[1] - step * shift),
            (front[0] + ten + step * shift, front[1] - step * shift),
            stroke=INK, stroke_width=0.8))
        drawing.add(drawing.line(
            (front[0] + ten + step * shift, front[1] - step * shift),
            (front[0] + ten + step * shift, front[1] + ten - step * shift),
            stroke=INK, stroke_width=0.8))
        drawing.add(drawing.line(
            (front[0] + ten, front[1] + step * PITCH),
            (front[0] + ten + cube_depth, front[1] + step * PITCH - cube_depth),
            stroke=INK, stroke_width=0.8))
    drawing.add(drawing.rect(front, (ten, ten), fill=FILL_BLUE, stroke=INK,
                             stroke_width=1.2))
    for row in range(10):
        for col in range(10):
            bead(front[0] + PITCH * col + PITCH / 2, front[1] + PITCH * row + PITCH / 2)
    _label(drawing, "1000", x + ten / 2, base + 22)
    return drawing.tostring()


LINE_W = 480


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def number_line(marks: list[Fraction], end: int = 1, landmarks: bool = True) -> str:
    """A number line from 0 to `end`, with a dot and a label for each mark.

    The landmarks are 0, one half and 1 (and each whole number up to
    `end`), drawn as ticks under the line, so a reader can see which one a
    fraction is closest to. The marks sit above the line.
    """
    height = 2 * MARGIN + 86
    drawing = _drawing(LINE_W + 2 * MARGIN + 20, height)
    left = MARGIN + 10
    y = MARGIN + 46

    def x_of(value: Fraction) -> float:
        return left + float(value) / end * LINE_W

    drawing.add(drawing.line((left, y), (left + LINE_W, y), stroke=INK, stroke_width=2.2))
    ticks = [Fraction(n) for n in range(end + 1)]
    if landmarks:
        ticks += [Fraction(2 * n + 1, 2) for n in range(end)]
    for tick in sorted(ticks):
        big = tick.denominator == 1
        drawing.add(drawing.line((x_of(tick), y - (9 if big else 6)),
                                 (x_of(tick), y + (9 if big else 6)),
                                 stroke=INK, stroke_width=2 if big else 1.4))
        _label(drawing, _fraction_text(tick), x_of(tick), y + 30,
               fill=INK if big else MUTED)
    for mark in marks:
        drawing.add(drawing.circle((x_of(mark), y), 6, fill=FILL_AMBER, stroke=INK,
                                   stroke_width=1.6))
        _label(drawing, _fraction_text(mark), x_of(mark), y - 16)
    return drawing.tostring()


GRID = 150          # the side of the square cut two ways


def area_grids(grids: list[tuple[int, int, int, int]], labels: list[str]) -> str:
    """Squares cut one way into columns and the other way into rows.

    Each grid is (columns, shaded columns, rows, shaded rows). The shaded
    columns are amber, the shaded rows blue, and where they cross is green:
    the green part is the fraction of a fraction. Half of a third is one
    cell of six, and the picture shows it without a rule.
    """
    count = len(grids)
    width = 2 * MARGIN + count * GRID + (count - 1) * GAP
    height = 2 * MARGIN + GRID + 30
    drawing = _drawing(width, height)
    for place, (cols, shade_cols, rows, shade_rows) in enumerate(grids):
        x0 = MARGIN + place * (GRID + GAP)
        y0 = MARGIN
        cell_w, cell_h = GRID / cols, GRID / rows
        for col in range(cols):
            for row in range(rows):
                in_col, in_row = col < shade_cols, row < shade_rows
                fill = (FILL_GREEN if in_col and in_row else FILL_AMBER if in_col
                        else FILL_BLUE if in_row else PANEL)
                drawing.add(drawing.rect((x0 + col * cell_w, y0 + row * cell_h),
                                         (cell_w, cell_h), fill=fill, stroke=INK,
                                         stroke_width=1.2))
        drawing.add(drawing.rect((x0, y0), (GRID, GRID), fill="none", stroke=INK,
                                 stroke_width=2.4))
        _label(drawing, labels[place], x0 + GRID / 2, y0 + GRID + 22)
    return drawing.tostring()


TOKEN = 30          # a heart's square
TOKEN_GAP = 6


def _token(drawing, x: float, y: float, symbol: str, fill: str,
           struck: bool = False) -> None:
    drawing.add(drawing.rect((x, y), (TOKEN, TOKEN), rx=5, fill=fill, stroke=INK,
                             stroke_width=1.3))
    _label(drawing, symbol, x + TOKEN / 2, y + TOKEN / 2 + 7, size=19)
    if struck:
        drawing.add(drawing.line((x - 3, y + TOKEN + 3), (x + TOKEN + 3, y - 3),
                                 stroke=INK, stroke_width=2.2))


def _run(count: int) -> float:
    return count * TOKEN + max(count - 1, 0) * TOKEN_GAP


def joined_stacks(left: int, right: int, symbol: str = "♡") -> str:
    """Two stacks written the long way, multiplied, then joined into one.

    The left stack is amber and the right is blue, and the joined row keeps
    their colours, so a reader can count where each heart came from. The
    picture prints no sum: the page asks the reader to count, and a label
    reading "2 + 3 = 5" would give the rule away before they find it.
    """
    sign_w = 34
    width = 2 * MARGIN + _run(left) + sign_w + _run(right) + sign_w + _run(left + right)
    height = 2 * MARGIN + TOKEN
    drawing = _drawing(width, height)
    x, y = MARGIN, MARGIN
    for _ in range(left):
        _token(drawing, x, y, symbol, FILL_AMBER)
        x += TOKEN + TOKEN_GAP
    _label(drawing, "×", x - TOKEN_GAP + sign_w / 2, y + TOKEN / 2 + 8, size=24)
    x += sign_w - TOKEN_GAP
    for _ in range(right):
        _token(drawing, x, y, symbol, FILL_BLUE)
        x += TOKEN + TOKEN_GAP
    _label(drawing, "=", x - TOKEN_GAP + sign_w / 2, y + TOKEN / 2 + 8, size=24)
    x += sign_w - TOKEN_GAP
    for index in range(left + right):
        _token(drawing, x, y, symbol, FILL_AMBER if index < left else FILL_BLUE)
        x += TOKEN + TOKEN_GAP
    return drawing.tostring()


def cancelled_stacks(top: int, bottom: int, symbol: str = "♡") -> str:
    """A stack over a stack, written the long way, with pairs crossed out.

    Each heart on the top that has a partner below is crossed out with its
    partner, since one heart divided by one heart is 1. What is left
    uncrossed is the answer: on the top when the top had more, on the
    bottom when the bottom had more, and nothing (so 1) when they matched.
    """
    longest = max(top, bottom)
    width = 2 * MARGIN + _run(longest)
    height = 2 * MARGIN + 2 * TOKEN + 22
    drawing = _drawing(width, height)
    pairs = min(top, bottom)
    y_top, y_line = MARGIN, MARGIN + TOKEN + 11
    for index in range(top):
        _token(drawing, MARGIN + index * (TOKEN + TOKEN_GAP), y_top, symbol,
               PANEL if index < pairs else FILL_AMBER, struck=index < pairs)
    drawing.add(drawing.line((MARGIN - 4, y_line), (MARGIN + _run(longest) + 4, y_line),
                             stroke=INK, stroke_width=2.4))
    for index in range(bottom):
        _token(drawing, MARGIN + index * (TOKEN + TOKEN_GAP), y_line + 11, symbol,
               PANEL if index < pairs else FILL_BLUE, struck=index < pairs)
    return drawing.tostring()


def stacks_of_stacks(inner: int, outer: int, symbol: str = "♡") -> str:
    """`outer` boxes, each holding a stack of `inner` hearts.

    A power of a power, the long way: (♡²)³ is three boxes of two hearts,
    and counting every heart gives the exponent 6.
    """
    box_pad = 7
    box_w = _run(inner) + 2 * box_pad
    width = 2 * MARGIN + outer * box_w + (outer - 1) * 16
    height = 2 * MARGIN + TOKEN + 2 * box_pad + 26
    drawing = _drawing(width, height)
    for box in range(outer):
        bx = MARGIN + box * (box_w + 16)
        drawing.add(drawing.rect((bx, MARGIN), (box_w, TOKEN + 2 * box_pad), rx=9,
                                 fill="none", stroke=INK, stroke_width=1.8))
        for index in range(inner):
            _token(drawing, bx + box_pad + index * (TOKEN + TOKEN_GAP), MARGIN + box_pad,
                   symbol, FILL_AMBER if box % 2 == 0 else FILL_BLUE)
    _label(drawing, f"{outer} boxes of {inner} = {outer * inner}", width / 2,
           MARGIN + TOKEN + 2 * box_pad + 22, fill=MUTED)
    return drawing.tostring()


SQ_PITCH = 13       # bead spacing in the bead squares


def bead_squares(sides: list[int], leftover: int = 0) -> str:
    """Squares of beads with 1, 2, 3 … beads on a side, each labelled.

    With `leftover`, one more drawing follows: the largest square that fits
    in (side² + leftover) beads, and the beads that are left over, which is
    what a number that is not a square number looks like.
    """
    extra = sides[-1] if leftover else None
    shapes = sides + ([extra] if leftover else [])
    # A slot is never narrower than its label, so "1 bead" and "4 beads"
    # under the two smallest squares do not run into each other.
    widths = [max(n * SQ_PITCH + (SQ_PITCH * (leftover // n + 1) + 6
                                  if (leftover and i == len(shapes) - 1) else 0), 60)
              for i, n in enumerate(shapes)]
    tallest = max(shapes) * SQ_PITCH
    width = 2 * MARGIN + sum(widths) + (len(shapes) - 1) * GAP
    height = 2 * MARGIN + tallest + 44
    drawing = _drawing(width, height)
    base = MARGIN + tallest
    x = MARGIN
    for index, n in enumerate(shapes):
        is_leftover = leftover and index == len(shapes) - 1
        bx = x if is_leftover else x + (widths[index] - n * SQ_PITCH) / 2
        for row in range(n):
            for col in range(n):
                drawing.add(drawing.circle(
                    (bx + col * SQ_PITCH + SQ_PITCH / 2, base - n * SQ_PITCH + row * SQ_PITCH + SQ_PITCH / 2),
                    BEAD + 0.8, fill=FILL_AMBER, stroke=INK, stroke_width=0.9))
        if is_leftover:
            for bead in range(leftover):
                col, row = divmod(bead, n)
                drawing.add(drawing.circle(
                    (x + n * SQ_PITCH + 6 + col * SQ_PITCH + SQ_PITCH / 2,
                     base - n * SQ_PITCH + row * SQ_PITCH + SQ_PITCH / 2),
                    BEAD + 0.8, fill=FILL_BLUE, stroke=INK, stroke_width=0.9))
            _label(drawing, f"{n * n + leftover} beads", x + widths[index] / 2, base + 20)
            _label(drawing, f"{leftover} left over", x + widths[index] / 2, base + 38, fill=MUTED)
        else:
            _label(drawing, f"{n * n} bead" + ("" if n == 1 else "s"), x + widths[index] / 2, base + 20)
            _label(drawing, f"side {n}", x + widths[index] / 2, base + 38, fill=MUTED)
        x += widths[index] + GAP
    return drawing.tostring()


def bead_cubes(edges: list[int]) -> str:
    """Cubes of beads with 1, 2, 3 … beads along each edge.

    Drawn the way the thousand-cube is: a front face of beads, and the top
    and right faces as grids going back.
    """
    pitch = 14
    depth_of = lambda n: n * pitch * 0.5  # noqa: E731
    sizes = [n * pitch + depth_of(n) for n in edges]
    tallest = max(sizes)
    width = 2 * MARGIN + sum(sizes) + (len(edges) - 1) * GAP
    height = 2 * MARGIN + tallest + 44
    drawing = _drawing(width, height)
    base = MARGIN + tallest
    x = MARGIN
    for n, size in zip(edges, sizes):
        side = n * pitch
        depth = depth_of(n)
        shift = depth / n
        front = (x, base - side)
        for step in range(n + 1):
            drawing.add(drawing.line((front[0] + step * pitch, front[1]),
                                     (front[0] + step * pitch + depth, front[1] - depth),
                                     stroke=INK, stroke_width=0.9))
            drawing.add(drawing.line((front[0] + step * shift, front[1] - step * shift),
                                     (front[0] + side + step * shift, front[1] - step * shift),
                                     stroke=INK, stroke_width=0.9))
            drawing.add(drawing.line((front[0] + side + step * shift, front[1] - step * shift),
                                     (front[0] + side + step * shift, front[1] + side - step * shift),
                                     stroke=INK, stroke_width=0.9))
            drawing.add(drawing.line((front[0] + side, front[1] + step * pitch),
                                     (front[0] + side + depth, front[1] + step * pitch - depth),
                                     stroke=INK, stroke_width=0.9))
        drawing.add(drawing.rect(front, (side, side), fill=FILL_BLUE, stroke=INK,
                                 stroke_width=1.3))
        for row in range(n):
            for col in range(n):
                drawing.add(drawing.circle((front[0] + col * pitch + pitch / 2,
                                            front[1] + row * pitch + pitch / 2),
                                           BEAD + 1.2, fill=FILL_AMBER, stroke=INK,
                                           stroke_width=0.9))
        _label(drawing, f"{n ** 3} bead" + ("" if n == 1 else "s"), x + size / 2, base + 20)
        _label(drawing, f"edge {n}", x + size / 2, base + 38, fill=MUTED)
        x += size + GAP
    return drawing.tostring()


UNIT = 60           # one square of the grid under the tilted square


def tilted_squares(grids: list[int]) -> str:
    """An n-by-n grid of unit squares, with a square drawn corner to corner inside.

    The tilted square joins the middles of the big square's sides, so it
    covers exactly half the grid: 2 squares of area for n = 2, 8 for n = 4.
    For n = 2 each side of the tilted square is the diagonal of one unit
    square, which is where side(2) lives.
    """
    sizes = [n * UNIT for n in grids]
    width = 2 * MARGIN + sum(sizes) + (len(grids) - 1) * GAP
    height = 2 * MARGIN + max(sizes) + 44
    drawing = _drawing(width, height)
    base = MARGIN + max(sizes)
    x = MARGIN
    for n, size in zip(grids, sizes):
        top = base - size
        half = size / 2
        corners = [(x + half, top), (x + size, top + half), (x + half, top + size), (x, top + half)]
        drawing.add(drawing.polygon(corners, fill=FILL_AMBER, stroke=INK, stroke_width=2.6))
        for step in range(n + 1):
            drawing.add(drawing.line((x + step * UNIT, top), (x + step * UNIT, top + size),
                                     stroke=INK, stroke_width=1 if 0 < step < n else 2))
            drawing.add(drawing.line((x, top + step * UNIT), (x + size, top + step * UNIT),
                                     stroke=INK, stroke_width=1 if 0 < step < n else 2))
        area = Fraction(n * n, 2)
        _label(drawing, f"grid of {n * n}", x + half, base + 20, fill=MUTED)
        _label(drawing, f"tilted square: {_fraction_text(area)}", x + half, base + 38)
        x += size + GAP
    return drawing.tostring()


def hop_line(base: int, hops: int, halfway: bool = False) -> str:
    """1, then base, base², … along a line, with an arc labelled ×base for each hop.

    With `halfway`, each hop gets a stop in its middle too, and two smaller
    arcs under the line: two half-hops make one whole hop.
    """
    stops = hops + 1
    step_w = 120 if not halfway else 150
    width = 2 * MARGIN + 40 + hops * step_w
    height = 2 * MARGIN + (150 if halfway else 104)
    drawing = _drawing(width, height)
    left = MARGIN + 20
    y = MARGIN + 66
    drawing.add(drawing.line((left - 10, y), (left + hops * step_w + 10, y), stroke=MUTED,
                             stroke_width=1.2))
    half_root = math.isqrt(base) if halfway else None
    for index in range(stops):
        x = left + index * step_w
        drawing.add(drawing.circle((x, y), 7, fill=FILL_AMBER, stroke=INK, stroke_width=1.6))
        _label(drawing, f"{base ** index:,}", x, y + 30)
        if index < hops:
            x2 = x + step_w
            drawing.add(drawing.path(d=f"M {x + 8} {y - 8} Q {(x + x2) / 2} {y - 62} {x2 - 8} {y - 8}",
                                     fill="none", stroke=INK, stroke_width=1.8))
            _label(drawing, f"×{base}", (x + x2) / 2, y - 40)
            if halfway:
                mid = (x + x2) / 2
                value = base ** index * half_root
                drawing.add(drawing.circle((mid, y), 5, fill=FILL_BLUE, stroke=INK,
                                           stroke_width=1.4))
                _label(drawing, f"{value:,}", mid, y + 30, fill=MUTED)
                for a, b in ((x, mid), (mid, x2)):
                    drawing.add(drawing.path(d=f"M {a + 6} {y + 42} Q {(a + b) / 2} {y + 74} {b - 6} {y + 42}",
                                             fill="none", stroke=MUTED, stroke_width=1.4))
                    _label(drawing, f"×{half_root}", (a + b) / 2, y + 76, size=12, fill=MUTED)
    return drawing.tostring()


def fraction_hops(base: int, parts: int, whole_hops: int = 1) -> str:
    """1 to base (and on), with each ×base hop cut into `parts` equal smaller hops.

    Under each stop is how far along it is, as a fraction of one whole hop:
    0, 1/3, 2/3, 1 … . The small hops multiply by the number that, done
    `parts` times, makes base; it is computed, and must be whole.
    """
    step = round(base ** (1 / parts))
    assert step ** parts == base, f"{base} has no whole {parts}-part hop"
    stops = parts * whole_hops + 1
    step_w = 110
    width = 2 * MARGIN + 60 + (stops - 1) * step_w
    height = 2 * MARGIN + 170
    drawing = _drawing(width, height)
    left = MARGIN + 30
    y = MARGIN + 100
    drawing.add(drawing.line((left - 10, y), (left + (stops - 1) * step_w + 10, y),
                             stroke=MUTED, stroke_width=1.2))
    for index in range(stops):
        x = left + index * step_w
        whole = index % parts == 0
        drawing.add(drawing.circle((x, y), 7 if whole else 5,
                                   fill=FILL_AMBER if whole else FILL_BLUE,
                                   stroke=INK, stroke_width=1.6))
        _label(drawing, f"{step ** index:,}", x, y + 28)
        _label(drawing, _fraction_text(Fraction(index, parts)), x, y + 52, size=12, fill=MUTED)
        if index < stops - 1:
            x2 = x + step_w
            drawing.add(drawing.path(d=f"M {x + 7} {y - 8} Q {(x + x2) / 2} {y - 40} {x2 - 7} {y - 8}",
                                     fill="none", stroke=MUTED, stroke_width=1.4))
            _label(drawing, f"×{step}", (x + x2) / 2, y - 28, size=12, fill=MUTED)
        if whole and index < stops - 1:
            x2 = x + parts * step_w
            drawing.add(drawing.path(d=f"M {x} {y - 12} Q {(x + x2) / 2} {y - 150} {x2} {y - 12}",
                                     fill="none", stroke=INK, stroke_width=1.8))
            _label(drawing, f"×{base}", (x + x2) / 2, y - 88)
    _label(drawing, "how far along, in whole hops", left + (stops - 1) * step_w / 2, y + 76,
           size=12, fill=MUTED)
    return drawing.tostring()


RULER_W = 600       # the slide rule's length, 1 to 10


def slide_rule(a: int | None = None, b: int | None = None) -> str:
    """Two rulers marked 1 to 10, each number placed at its hops of 10 from 1.

    With `a` and `b`, the top ruler slides right until its 1 sits over `a`
    on the bottom ruler; then `b` on the top ruler sits over a × b on the
    bottom, because sliding adds the two distances.
    """
    shift = RULER_W * math.log10(a) if a else 0
    width = 2 * MARGIN + RULER_W + shift + 30
    height = 2 * MARGIN + 150
    drawing = _drawing(width, height)
    left = MARGIN + 15

    def ruler(x0: float, top: float, fill: str, ticks_down: bool) -> None:
        drawing.add(drawing.rect((x0, top), (RULER_W, 40), fill=fill, stroke=INK, stroke_width=1.8))
        edge = top + 40 if not ticks_down else top
        for n in range(1, 11):
            x = x0 + RULER_W * math.log10(n)
            y1 = edge - 12 if not ticks_down else edge + 12
            drawing.add(drawing.line((x, edge), (x, y1), stroke=INK, stroke_width=1.6))
            anchor = "start" if n == 1 else "end" if n == 10 else "middle"
            nudge = 5 if n == 1 else -5 if n == 10 else 0
            drawing.add(drawing.text(str(n), insert=(x + nudge, top + 25), text_anchor=anchor,
                                     font_size=f"{LABEL_PT}px", fill=INK))

    ruler(left + shift, MARGIN + 20, FILL_BLUE, ticks_down=False)
    ruler(left, MARGIN + 60, FILL_AMBER, ticks_down=True)
    if a and b:
        product = a * b
        assert product <= 10
        for x in (left + shift, left + RULER_W * math.log10(product)):
            drawing.add(drawing.line((x, MARGIN + 8), (x, MARGIN + 112), stroke=INK,
                                     stroke_width=1.2, stroke_dasharray="4 3"))
        _label(drawing, f"1 over {a}", left + shift, MARGIN + 130, size=12, fill=MUTED)
        _label(drawing, f"{b} over {product}", left + RULER_W * math.log10(product),
               MARGIN + 130, size=12, fill=MUTED)
    return drawing.tostring()


def paper_sizes() -> str:
    """A3, A4, A5 and A6 drawn to scale, each half of the one before.

    Each sheet sits in the corner of the one before it, so a reader can see
    that halving a sheet keeps its shape. The sizes are the ISO 216 sizes in
    millimetres.
    """
    sizes = [("A3", 297, 420), ("A4", 210, 297), ("A5", 148, 210), ("A6", 105, 148)]
    scale = 0.62
    width = 2 * MARGIN + 420 * scale + 160
    height = 2 * MARGIN + 297 * scale + 10
    drawing = _drawing(width, height)
    fills = [PANEL, FILL_AMBER, FILL_BLUE, FILL_GREEN]
    for (name, short, long_), fill in zip(sizes, fills):
        landscape = sizes.index((name, short, long_)) % 2 == 0
        w, h = (long_, short) if landscape else (short, long_)
        drawing.add(drawing.rect((MARGIN, MARGIN), (w * scale, h * scale), fill=fill,
                                 stroke=INK, stroke_width=1.8))
        _label(drawing, name, MARGIN + w * scale - 22, MARGIN + h * scale - 10)
    x = MARGIN + 420 * scale + 16
    for row, (name, short, long_) in enumerate(sizes):
        drawing.add(drawing.text(f"{name}: {short} × {long_} mm", insert=(x, MARGIN + 30 + row * 26),
                                 font_size=f"{LABEL_PT}px", fill=INK))
    return drawing.tostring()


def narrowing(start: int, steps: list[tuple[Fraction, str]], unit: str = "") -> str:
    """A bar for a count, then a shorter bar for each fraction of it that is kept.

    Each step is (fraction kept, what it keeps). The counts are computed
    here, so a bar cannot disagree with the sum the page does.
    """
    bar_h = 30
    row_h = 58
    label_w = 190
    width = 2 * MARGIN + label_w + BAR_W + 70
    height = 2 * MARGIN + row_h * (len(steps) + 1)
    drawing = _drawing(width, height)
    count = Fraction(start)
    left = MARGIN + label_w
    rows = [(None, "start", count)]
    for kept, text in steps:
        count *= kept
        rows.append((kept, text, count))
    for index, (kept, text, value) in enumerate(rows):
        y = MARGIN + index * row_h + 10
        length = max(BAR_W * float(value) / start, 2)
        drawing.add(drawing.rect((left, y), (length, bar_h), fill=FILL_AMBER, stroke=INK,
                                 stroke_width=1.4))
        drawing.add(drawing.text(f"{_fraction_text(value)}{unit}", insert=(left + length + 8, y + 21),
                                 font_size=f"{LABEL_PT}px", fill=INK))
        drawing.add(drawing.text(text, insert=(MARGIN, y + 13), font_size=f"{LABEL_PT}px", fill=INK))
        if kept is not None:
            drawing.add(drawing.text(f"× {_fraction_text(kept)}", insert=(MARGIN, y + 30),
                                     font_size="12px", fill=MUTED))
    return drawing.tostring()


def signed_line(marks: list[Fraction], start: int, end: int, halves: bool = False) -> str:
    """A number line from `start` to `end`, through 0, with a dot for each mark.

    Whole numbers get ticks and labels; with `halves`, the halves get small
    ticks too. Numbers below 0 are to the left of 0, as far from it as the
    same number above 0 is to the right.
    """
    span = end - start
    height = 2 * MARGIN + 86
    drawing = _drawing(LINE_W + 2 * MARGIN + 30, height)
    left = MARGIN + 15
    y = MARGIN + 46

    def x_of(value: Fraction) -> float:
        return left + float(value - start) / span * LINE_W

    drawing.add(drawing.line((left - 8, y), (left + LINE_W + 8, y), stroke=INK, stroke_width=2.2))
    for n in range(start, end + 1):
        big = n == 0
        drawing.add(drawing.line((x_of(Fraction(n)), y - (11 if big else 8)),
                                 (x_of(Fraction(n)), y + (11 if big else 8)),
                                 stroke=INK, stroke_width=2.4 if big else 1.8))
        _label(drawing, str(n).replace("-", "−"), x_of(Fraction(n)), y + 30)
        if halves and n < end:
            drawing.add(drawing.line((x_of(Fraction(2 * n + 1, 2)), y - 5),
                                     (x_of(Fraction(2 * n + 1, 2)), y + 5),
                                     stroke=MUTED, stroke_width=1.2))
    for mark in marks:
        drawing.add(drawing.circle((x_of(mark), y), 6, fill=FILL_AMBER, stroke=INK,
                                   stroke_width=1.6))
        _label(drawing, _fraction_text(mark).replace("-", "−"), x_of(mark), y - 16)
    return drawing.tostring()


CELL = 34           # one square of the coordinate grid


def coordinate_grid(points: list[tuple[int, int, str]], low: int = 0, high: int = 6) -> str:
    """Two lines at right angles, with a grid, and a labelled dot at each point.

    The across line and the up line both run from `low` to `high`. Each
    point is (across, up, name).
    """
    n = high - low
    size = n * CELL
    width = 2 * MARGIN + size + 100
    height = 2 * MARGIN + size + 50
    drawing = _drawing(width, height)
    x0 = MARGIN + 36
    y0 = MARGIN + 14 + size

    def at(a: int, u: int) -> tuple[float, float]:
        return x0 + (a - low) * CELL, y0 - (u - low) * CELL

    for k in range(n + 1):
        drawing.add(drawing.line((x0 + k * CELL, y0), (x0 + k * CELL, y0 - size), stroke=MUTED,
                                 stroke_width=0.8))
        drawing.add(drawing.line((x0, y0 - k * CELL), (x0 + size, y0 - k * CELL), stroke=MUTED,
                                 stroke_width=0.8))
    ax, ay = at(0, 0)
    drawing.add(drawing.line((x0, ay), (x0 + size + 14, ay), stroke=INK, stroke_width=2.2))
    drawing.add(drawing.line((ax, y0), (ax, y0 - size - 14), stroke=INK, stroke_width=2.2))
    for k in range(low, high + 1):
        x, _ = at(k, 0)
        if k != 0:
            _label(drawing, str(k).replace("-", "−"), x, ay + 18, size=12, fill=MUTED)
        _, y = at(0, k)
        if k != 0:
            _label(drawing, str(k).replace("-", "−"), ax - 12, y + 4, size=12, fill=MUTED)
    _label(drawing, "0", ax - 10, ay + 16, size=12, fill=MUTED)
    drawing.add(drawing.text("across", insert=(x0 + size + 18, ay + 4), font_size="12px", fill=MUTED))
    _label(drawing, "up", ax, y0 - size - 20, size=12, fill=MUTED)
    for a, u, name in points:
        x, y = at(a, u)
        drawing.add(drawing.circle((x, y), 6, fill=FILL_AMBER, stroke=INK, stroke_width=1.6))
        _label(drawing, name, x + 13, y - 9)
    return drawing.tostring()


def dot_plots(rows: list[tuple[str, list[int]]], top: int) -> str:
    """Side by side plots: 1, 2, 3 … across, and each row's numbers up.

    Every plot has the same up scale, 0 to `top`, so a reader can compare
    them: one pattern climbs in equal steps, another in bigger and bigger
    ones.
    """
    plot_w, plot_h = 200, 190
    count = len(rows)
    width = 2 * MARGIN + count * (plot_w + 50)
    height = 2 * MARGIN + plot_h + 60
    drawing = _drawing(width, height)
    for place, (title, values) in enumerate(rows):
        x0 = MARGIN + 34 + place * (plot_w + 50)
        y0 = MARGIN + 20 + plot_h
        drawing.add(drawing.line((x0, y0), (x0 + plot_w, y0), stroke=INK, stroke_width=1.8))
        drawing.add(drawing.line((x0, y0), (x0, y0 - plot_h), stroke=INK, stroke_width=1.8))
        for tick in range(0, top + 1, max(1, top // 4)):
            y = y0 - tick / top * plot_h
            drawing.add(drawing.line((x0 - 4, y), (x0, y), stroke=INK, stroke_width=1.2))
            _label(drawing, str(tick), x0 - 16, y + 4, size=11, fill=MUTED)
        step = plot_w / (len(values) + 1)
        for index, value in enumerate(values, start=1):
            x = x0 + index * step
            _label(drawing, str(index), x, y0 + 16, size=11, fill=MUTED)
            drawing.add(drawing.circle((x, y0 - value / top * plot_h), 5, fill=FILL_AMBER,
                                       stroke=INK, stroke_width=1.4))
        _label(drawing, title, x0 + plot_w / 2, y0 + 40)
    return drawing.tostring()


# The planets' mean distance from the Sun, in millions of km: NASA's
# Planetary Fact Sheet (nssdc.gsfc.nasa.gov/planetary/factsheet).
PLANETS = [("Mercury", 57.9), ("Venus", 108.2), ("Earth", 149.6), ("Mars", 228.0),
           ("Jupiter", 778.5), ("Saturn", 1432.0), ("Uranus", 2867.0), ("Neptune", 4515.0)]


def planet_scales(log: bool) -> str:
    """The eight planets on one line, by distance from the Sun.

    On the normal scale, equal gaps are equal distances. On the hops
    scale, equal gaps are equal ×10 hops: 10, 100, 1000, 10,000 million km.
    """
    width = 2 * MARGIN + LINE_W + 60
    height = 2 * MARGIN + 240
    drawing = _drawing(width, height)
    left = MARGIN + 20
    y = MARGIN + 190
    low, high = (10, 10_000) if log else (0, 5000)

    def x_of(value: float) -> float:
        if log:
            return left + (math.log10(value) - math.log10(low)) / (math.log10(high) - math.log10(low)) * LINE_W
        return left + (value - low) / (high - low) * LINE_W

    drawing.add(drawing.line((left, y), (left + LINE_W, y), stroke=INK, stroke_width=2))
    ticks = [10, 100, 1000, 10_000] if log else [0, 1000, 2000, 3000, 4000, 5000]
    for tick in ticks:
        drawing.add(drawing.line((x_of(tick), y - 6), (x_of(tick), y + 6), stroke=INK, stroke_width=1.6))
        _label(drawing, f"{tick:,}", x_of(tick), y + 24, size=12, fill=MUTED)
    _label(drawing, "millions of km from the Sun", left + LINE_W / 2, y + 44, size=12, fill=MUTED)
    inner = [x_of(distance) for _, distance in PLANETS[:4]]
    crowded = inner[-1] - inner[0] < 60
    for index, (name, distance) in enumerate(PLANETS):
        x = x_of(distance)
        drawing.add(drawing.circle((x, y), 5, fill=FILL_BLUE, stroke=INK, stroke_width=1.4))
        if crowded and index < 4:
            continue
        drawing.add(drawing.text(name, insert=(x + 4, y - 12), font_size="12px", fill=INK,
                                 transform=f"rotate(-90 {x + 4} {y - 12})"))
    if crowded:
        drawing.add(drawing.text("Mercury, Venus, Earth, Mars", insert=(inner[-1] + 4, y - 12),
                                 font_size="12px", fill=INK,
                                 transform=f"rotate(-90 {inner[-1] + 4} {y - 12})"))
    return drawing.tostring()


def _superscript(number: int) -> str:
    return str(number).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))


def ten_ladder(low: int, high: int) -> str:
    """The powers of ten from 10^low to 10^high, a box each, big numbers on the right.

    Each box shows the power and the number written the long way, so a
    reader can count the zeros, or the places after the decimal point.
    """
    count = high - low + 1
    box_w, box_h = 86, 58
    width = 2 * MARGIN + count * (box_w + 8)
    height = 2 * MARGIN + box_h + 30
    drawing = _drawing(width, height)
    for place, power in enumerate(range(low, high + 1)):
        x = MARGIN + place * (box_w + 8)
        drawing.add(drawing.rect((x, MARGIN), (box_w, box_h), rx=6,
                                 fill=FILL_AMBER if power == 0 else PANEL,
                                 stroke=INK, stroke_width=1.4))
        text = f"{10 ** power:,}" if power >= 0 else "0." + "0" * (-power - 1) + "1"
        _label(drawing, "10" + _superscript(power), x + box_w / 2, MARGIN + 24)
        _label(drawing, text, x + box_w / 2, MARGIN + 46, size=12, fill=MUTED)
    _label(drawing, "each box is ×10 the one on its left", width / 2, MARGIN + box_h + 22,
           size=12, fill=MUTED)
    return drawing.tostring()


def balance(left: tuple[int, int], right: tuple[int, int], box: str = "?") -> str:
    """A level balance: each pan holds (boxes, beads).

    A box is a closed box with an unknown number of beads inside, drawn as
    a square marked `box`; a bead is one bead.
    """
    width = 2 * MARGIN + 460
    height = 2 * MARGIN + 190
    drawing = _drawing(width, height)
    cx = width / 2
    beam_y = MARGIN + 70
    drawing.add(drawing.polygon([(cx, beam_y), (cx - 22, MARGIN + 176), (cx + 22, MARGIN + 176)],
                                fill=PANEL, stroke=INK, stroke_width=1.8))
    drawing.add(drawing.line((cx - 190, beam_y), (cx + 190, beam_y), stroke=INK, stroke_width=3))
    for side, (boxes, beads) in ((-1, left), (1, right)):
        px = cx + side * 150
        pan_y = beam_y + 60
        for dx in (-70, 70):
            drawing.add(drawing.line((px, beam_y), (px + dx, pan_y), stroke=MUTED, stroke_width=1))
        drawing.add(drawing.path(d=f"M {px - 80} {pan_y} Q {px} {pan_y + 26} {px + 80} {pan_y}",
                                 fill=PANEL, stroke=INK, stroke_width=1.8))
        items = [("box", None)] * boxes + [("bead", None)] * beads
        per_row = 6
        for index, (kind, _) in enumerate(items):
            row, col = divmod(index, per_row)
            in_row = min(per_row, len(items) - row * per_row)
            x = px - (in_row - 1) * 11 + col * 22
            y = pan_y - 12 - row * 22
            if kind == "box":
                drawing.add(drawing.rect((x - 10, y - 10), (20, 20), fill=FILL_BLUE, stroke=INK,
                                         stroke_width=1.4))
                _label(drawing, box, x, y + 5, size=12)
            else:
                drawing.add(drawing.circle((x, y), 7, fill=FILL_AMBER, stroke=INK, stroke_width=1.2))
    return drawing.tostring()


DIAGRAMS = {
    "one-whole-many-slices/one-pizza.svg": lambda: pizza_row([(1, 0)], room_for=3),
    "one-whole-many-slices/cut-again.svg": lambda: pizza_row(
        [(2, 0), (4, 0), (8, 0)], ["2 slices", "4 slices", "8 slices"]),
    "one-whole-many-slices/one-of-four.svg": lambda: pizza_row([(4, 1)], room_for=3),
    "one-whole-many-slices/more-of-four.svg": lambda: pizza_row(
        [(4, 1), (4, 2), (4, 3), (4, 4)], ["1 of 4", "2 of 4", "3 of 4", "4 of 4"]),
    "one-whole-many-slices/every-slice.svg": lambda: pizza_row(
        [(3, 3), (5, 5), (8, 8), (12, 12)],
        ["3 of 3", "5 of 5", "8 of 8", "12 of 12"]),
    "one-whole-many-slices/very-thin.svg": lambda: pizza_row(
        [(1, 1), (10, 1), (24, 1)], ["1 of 1", "1 of 10", "1 of 24"]),
    "same-amount-different-names/half-in-three-ways.svg": lambda: pizza_row(
        [(2, 1), (4, 2), (8, 4)], ["1 of 2", "2 of 4", "4 of 8"]),
    "same-amount-different-names/wall-of-halves.svg": lambda: fraction_wall(
        [2, 4, 8]),
    "same-amount-different-names/wall-shaded.svg": lambda: fraction_wall(
        [2, 4, 8], shade={2: 1, 4: 2, 8: 4}),
    "same-amount-different-names/wall-of-thirds.svg": lambda: fraction_wall(
        [3, 6, 12], shade={3: 2, 6: 4, 12: 8}),
    "the-long-way/folded-paper.svg": lambda: folded_sheets(4),
    "the-long-way/golden-beads.svg": golden_beads,

    # Strand A: slashes
    "which-is-bigger/same-bottom.svg": lambda: pizza_row(
        [(8, 3), (8, 5)], ["3 of 8", "5 of 8"], room_for=3),
    "which-is-bigger/same-top.svg": lambda: pizza_row(
        [(3, 1), (4, 1), (6, 1)], ["1 of 3", "1 of 4", "1 of 6"]),
    "which-is-bigger/landmarks.svg": lambda: number_line(
        [Fraction(1, 4), Fraction(2, 3), Fraction(9, 10)]),
    "which-is-bigger/empty-line.svg": lambda: number_line([]),
    "which-is-bigger/two-thirds-in-twelfths.svg": lambda: fraction_wall(
        [3, 12], shade={3: 2, 12: 8}),
    "which-is-bigger/three-quarters-in-twelfths.svg": lambda: fraction_wall(
        [4, 12], shade={4: 3, 12: 9}),
    "adding-slices/same-size-sum.svg": lambda: pizza_row(
        [(8, 3), (8, 2), (8, 5)], ["3 of 8", "2 of 8", "5 of 8"], between=["+", "="]),
    "adding-slices/half-and-third.svg": lambda: pizza_row(
        [(2, 1), (3, 1)], ["1 of 2", "1 of 3"], between=["+"], room_for=3),
    "adding-slices/half-in-sixths.svg": lambda: fraction_wall([2, 6], shade={2: 1, 6: 3}),
    "adding-slices/third-in-sixths.svg": lambda: fraction_wall([3, 6], shade={3: 1, 6: 2}),
    "adding-slices/into-sixths.svg": lambda: pizza_row(
        [(6, 3), (6, 2), (6, 5)], ["3 of 6", "2 of 6", "5 of 6"], between=["+", "="]),
    "taking-slices-away/take-away-same.svg": lambda: pizza_row(
        [(8, 5), (8, 2), (8, 3)], ["5 of 8", "2 of 8", "3 of 8"], between=["−", "="]),
    "taking-slices-away/whole-minus-quarter.svg": lambda: pizza_row(
        [(4, 4), (4, 1), (4, 3)], ["4 of 4", "1 of 4", "3 of 4"], between=["−", "="]),
    "taking-slices-away/half-minus-third.svg": lambda: pizza_row(
        [(6, 3), (6, 2), (6, 1)], ["3 of 6", "2 of 6", "1 of 6"], between=["−", "="]),
    "a-fraction-of-a-fraction/half-of-a-half.svg": lambda: area_grids(
        [(2, 1, 1, 0), (2, 1, 2, 1)], ["a half", "half of that half"]),
    "a-fraction-of-a-fraction/half-of-a-third.svg": lambda: area_grids(
        [(3, 1, 1, 0), (3, 1, 2, 1)], ["a third", "half of that third"]),
    "a-fraction-of-a-fraction/two-thirds-of-three-quarters.svg": lambda: area_grids(
        [(4, 3, 1, 0), (4, 3, 3, 2)], ["three quarters", "two thirds of that"]),
    "how-many-fit/three-pizzas-in-quarters.svg": lambda: pizza_row(
        [(4, 4), (4, 4), (4, 4)], ["4 quarters", "4 quarters", "4 quarters"]),
    "how-many-fit/half-in-quarters.svg": lambda: fraction_wall([2, 4], shade={2: 1, 4: 2}),

    # Strand B: powers
    "joining-two-stacks/join-two-and-three.svg": lambda: joined_stacks(2, 3),
    "joining-two-stacks/join-four-and-one.svg": lambda: joined_stacks(4, 1),
    "sharing-out/cancel-five-over-two.svg": lambda: cancelled_stacks(5, 2),
    "sharing-out/cancel-seven-over-three.svg": lambda: cancelled_stacks(7, 3),
    "when-everything-cancels/cancel-four-over-four.svg": lambda: cancelled_stacks(4, 4),
    "more-on-the-bottom/cancel-two-over-five.svg": lambda: cancelled_stacks(2, 5),
    "more-on-the-bottom/cancel-three-over-four.svg": lambda: cancelled_stacks(3, 4),
    "a-power-of-a-power/two-in-three-boxes.svg": lambda: stacks_of_stacks(2, 3),
    "a-power-of-a-power/three-in-two-boxes.svg": lambda: stacks_of_stacks(3, 2),

    # Strand C: undoing a power
    "the-side-of-a-square/bead-squares.svg": lambda: bead_squares([1, 2, 3, 4, 5]),
    "the-side-of-a-square/ten-beads.svg": lambda: bead_squares([3], leftover=1),
    "the-side-of-a-square/bead-cubes.svg": lambda: bead_cubes([1, 2, 3]),
    "sides-that-never-end/tilted-squares.svg": lambda: tilted_squares([2, 4]),
    "halfway-steps/halfway-hops.svg": lambda: hop_line(4, 2, halfway=True),
    "how-many-hops/hops-of-ten.svg": lambda: hop_line(10, 3),
    "how-many-hops/hops-of-two.svg": lambda: hop_line(2, 4),
    "stretching-the-halfway-steps/thirds-of-eight.svg": lambda: fraction_hops(8, 3),
    "stretching-the-halfway-steps/halves-of-nine.svg": lambda: fraction_hops(9, 2, whole_hops=2),
    "hops-that-add/two-rulers.svg": lambda: slide_rule(),
    "hops-that-add/two-times-three.svg": lambda: slide_rule(2, 3),
    "hops-that-add/two-times-four.svg": lambda: slide_rule(2, 4),
    "surds-and-logs-in-the-wild/paper-sizes.svg": paper_sizes,

    # Views from the top
    "narrowing-it-down/a-town.svg": lambda: narrowing(1000, [
        (Fraction(1, 2), "like tea"), (Fraction(1, 5), "have a bike"),
        (Fraction(1, 10), "can juggle")]),
    "powers-of-ten/ten-ladder.svg": lambda: ten_ladder(-3, 3),

    # Strand D: seeing it
    "the-number-line/whole-numbers.svg": lambda: signed_line([], -5, 5),
    "the-number-line/some-points.svg": lambda: signed_line(
        [Fraction(-3), Fraction(-1, 2), Fraction(2), Fraction(7, 2)], -5, 5, halves=True),
    "two-lines-at-right-angles/three-points.svg": lambda: coordinate_grid(
        [(2, 3, "A"), (5, 1, "B"), (0, 4, "C")]),
    "two-lines-at-right-angles/four-corners.svg": lambda: coordinate_grid(
        [(2, 3, "A"), (-3, 2, "B"), (-2, -3, "C"), (4, -1, "D")], low=-5, high=5),
    "a-pattern-as-dots/two-patterns.svg": lambda: dot_plots(
        [("2, 4, 6, 8, 10", [2, 4, 6, 8, 10]), ("2, 4, 8, 16, 32", [2, 4, 8, 16, 32])], top=32),
    "drawing-across-scales/planets-normal.svg": lambda: planet_scales(log=False),
    "drawing-across-scales/planets-hops.svg": lambda: planet_scales(log=True),

    # Strand E: the balance
    "a-box-with-something-in-it/box-and-three.svg": lambda: balance((1, 3), (0, 7)),
    "keeping-it-level/take-three.svg": lambda: balance((1, 0), (0, 4)),
    "keeping-it-level/two-boxes.svg": lambda: balance((2, 1), (0, 9)),
    "a-box-with-something-in-it/three-boxes.svg": lambda: balance((3, 0), (0, 12)),
    "keeping-it-level/three-boxes.svg": lambda: balance((3, 0), (0, 12)),
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
