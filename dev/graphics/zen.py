#!/usr/bin/env python3
"""The pictures for The Zen of Slashes and Surds.

    python3 dev/graphics/zen.py          # report what would change
    python3 dev/graphics/zen.py --write  # write it

The module's readers meet each idea as a thing before they meet it as
symbols, the way a Montessori classroom hands a child fraction circles and
golden beads before it writes anything down
(planning/outlines/zen-of-slashes-and-surds.md). These are those things,
drawn: a pizza cut into equal slices, a wall of fraction bars, a sheet of
paper folded again and again, and the golden beads.

Same rule as the other generators: every count in a picture is computed
here from the numbers the page uses, never typed, so a picture cannot show
five slices where the page says six.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import FILL_AMBER, FILL_BLUE, INK, MUTED, PANEL, SANS  # noqa: E402

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
              room_for: int = 1) -> str:
    """A row of pizzas, each (slices, shaded), with a label under each.

    `room_for` makes the canvas as wide as that many pizzas and centres
    the row in it. A page scales a picture to its column, so one pizza on
    a canvas of its own is drawn as wide as the page, far bigger than the
    same pizza in a row of four; room for three keeps the sizes close.
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
