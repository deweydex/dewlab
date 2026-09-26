#!/usr/bin/env python3
"""The pictures for Dewey Track Units 1 to 5 (issue #354).

    python3 dev/graphics/dewey_units_1_5.py          # report what would change
    python3 dev/graphics/dewey_units_1_5.py --write  # write it

Same rule as the other generators: every number in a picture is computed
here, and wherever a page's own cell holds the numbers, they are read out of
that cell, so a picture cannot quietly disagree with the arithmetic the page
teaches. If a page stops defining a value this relies on, generation stops
and names the cell rather than drawing yesterday's numbers.

Colours are the site's theme tokens from `palette.py`, so every picture reads
in light, dark and both high-contrast modes. A tint is never the only signal:
wherever a fill marks something, a label or a number says it too.

The pages inline these files (`build.py`, `inline_local_svg`), several to a
page, so nothing here uses an `id`: an arrowhead is a small triangle drawn
where it is needed, not a shared marker.
"""

from __future__ import annotations

import argparse
import ast
import math
import sys
from fractions import Fraction
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (FILL_AMBER, FILL_BLUE, FILL_GREEN, FILL_PINK, INK,  # noqa: E402
                     MONO, MUTED, PANEL, PAPER, RULE, SANS)

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL = 14          # ordinary label size, in px of the viewBox
SMALL = 12
MARGIN = 16


# --------------------------------------------------------------------------
# Reading the pages' own cells
# --------------------------------------------------------------------------

def _cell(slug: str, cell_id: str) -> str:
    """The source of one exec cell on a tutorial page, header lines removed."""
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    marker = f"id: {cell_id}\n"
    if marker not in page:
        raise SystemExit(f"{slug}: no cell called {cell_id!r} any more")
    block = page.split(marker, 1)[1].split("```", 1)[0]
    lines = [line for line in block.splitlines()
             if not line.startswith(("toolkit:", "hint:", "expect:"))]
    return "\n".join(lines)


def _assigned(slug: str, cell_id: str, name: str):
    """The literal a cell assigns to `name`, the first time it does."""
    tree = ast.parse(_cell(slug, cell_id))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise SystemExit(f"{slug}/{cell_id}: no literal assigned to {name!r}")


def _run(slug: str, cell_id: str, namespace: dict | None = None) -> dict:
    """Run one of the page's cells, quietly, and hand back its names.

    Only for cells that need nothing the browser gives a page (no files, no
    toolkit), so that the value a picture shows is the value the cell makes.
    """
    namespace = {} if namespace is None else namespace
    namespace.setdefault("print", lambda *args, **kwargs: None)
    exec(compile(_cell(slug, cell_id), f"{slug}/{cell_id}", "exec"), namespace)
    return namespace


def _functions(slug: str, cell_id: str) -> dict:
    """Only the `def`s from a cell, run, so the rest of the cell is not needed."""
    tree = ast.parse(_cell(slug, cell_id))
    tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    namespace: dict = {}
    exec(compile(tree, f"{slug}/{cell_id}", "exec"), namespace)
    return namespace


def _loop_names(slug: str, cell_id: str) -> list[str]:
    """The loop variables of a cell's nested `for` loops, outermost first."""
    names = []
    for node in ast.walk(ast.parse(_cell(slug, cell_id))):
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            names.append(node.target.id)
    return names


# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------

def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _text(drawing, text: str, x: float, y: float, *, size: float = LABEL,
          anchor: str = "middle", fill: str = INK, bold: bool = False,
          mono: bool = False, italic: bool = False) -> None:
    extra = {}
    if bold:
        extra["font_weight"] = "bold"
    if mono:
        extra["font_family"] = MONO
    if italic:
        extra["font_style"] = "italic"
    drawing.add(drawing.text(text, insert=(round(x, 2), round(y, 2)),
                             text_anchor=anchor, font_size=f"{size}px",
                             fill=fill, **extra))


def _width_of(text: str, size: float = LABEL) -> float:
    return len(text) * size * 0.58


def _head(drawing, tip: tuple[float, float], towards_from: tuple[float, float],
          *, size: float = 8, fill: str = INK) -> None:
    """A filled arrowhead at `tip`, pointing away from `towards_from`."""
    dx, dy = tip[0] - towards_from[0], tip[1] - towards_from[1]
    length = math.hypot(dx, dy) or 1
    ux, uy = dx / length, dy / length
    back = (tip[0] - ux * size, tip[1] - uy * size)
    left = (back[0] - uy * size * 0.5, back[1] + ux * size * 0.5)
    right = (back[0] + uy * size * 0.5, back[1] - ux * size * 0.5)
    drawing.add(drawing.polygon([tuple(round(v, 2) for v in p) for p in (tip, left, right)],
                                fill=fill, stroke="none"))


def _arrow(drawing, start, end, *, stroke: str = INK, width: float = 1.6,
           dashed: bool = False, head: float = 8) -> None:
    """A straight arrow from `start` to `end`, the head ending exactly at `end`."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy) or 1
    shaft_end = (end[0] - dx / length * head * 0.8, end[1] - dy / length * head * 0.8)
    extra = {"stroke_dasharray": "5,4"} if dashed else {}
    drawing.add(drawing.line(tuple(round(v, 2) for v in start),
                             tuple(round(v, 2) for v in shaft_end),
                             stroke=stroke, stroke_width=width, **extra))
    _head(drawing, end, start, size=head, fill=stroke)


def _box(drawing, x, y, w, h, *, fill=PANEL, stroke=INK, width=1.3, rx=4,
         dashed=False) -> None:
    extra = {"stroke_dasharray": "5,4"} if dashed else {}
    drawing.add(drawing.rect((round(x, 2), round(y, 2)), (round(w, 2), round(h, 2)),
                             fill=fill, stroke=stroke, stroke_width=width, rx=rx, **extra))


def _minus(number) -> str:
    """A number as a page writes it in prose: a real minus sign, not a hyphen."""
    text = f"{number:g}" if isinstance(number, float) else str(number)
    return text.replace("-", "−")


# ==========================================================================
# Unit 1
# ==========================================================================

def ten_plus_four() -> str:
    """*Four questions*: the same move, 10 + 4, on a number line and on a clock.

    The page's point is that the move is the same and the space decides the
    answer. Side by side, the four hops are visibly the same four hops, and
    only where they land differs. The clock's answer is computed by the
    clock's own rule, going round after 12, not typed.
    """
    start, hours, face = 10, 4, 12
    on_the_line = start + hours
    on_the_clock = (start + hours - 1) % face + 1

    width, height = 660, 290
    drawing = _drawing(width, height)

    # The number line: 0 to 16, with four hops from 10.
    left, right, line_y = 24, 330, 165
    top_number = 16
    step = (right - left) / top_number
    drawing.add(drawing.line((left, line_y), (right, line_y), stroke=INK, stroke_width=1.5))
    for number in range(top_number + 1):
        x = left + number * step
        drawing.add(drawing.line((x, line_y - 5), (x, line_y + 5), stroke=INK, stroke_width=1))
        if number % 2 == 0 or number in (start, on_the_line):
            _text(drawing, str(number), x, line_y + 22, size=SMALL,
                  bold=number in (start, on_the_line))
    for hop in range(hours):
        x0 = left + (start + hop) * step
        x1 = x0 + step
        mid = (x0 + x1) / 2
        drawing.add(drawing.path(d=f"M {x0:.2f} {line_y - 4} Q {mid:.2f} {line_y - 34} "
                                   f"{x1 - 2:.2f} {line_y - 7}",
                                 fill="none", stroke=INK, stroke_width=1.5))
        _head(drawing, (x1, line_y - 5), (x1 - 6, line_y - 16), size=7)
        _text(drawing, str(hop + 1), mid, line_y - 30, size=SMALL - 1, fill=MUTED)
    drawing.add(drawing.circle((left + start * step, line_y), 5, fill=PAPER, stroke=INK, stroke_width=2))
    drawing.add(drawing.circle((left + on_the_line * step, line_y), 5, fill=INK))
    _text(drawing, "On a number line", (left + right) / 2, 22, bold=True)
    _text(drawing, f"{start} + {hours} = {on_the_line}", (left + right) / 2, 272)

    # The clock: the same four hops, round the face.
    cx, cy, radius = 505, 158, 82

    def at(number: float, r: float) -> tuple[float, float]:
        angle = 2 * math.pi * number / face - math.pi / 2
        return cx + r * math.cos(angle), cy + r * math.sin(angle)

    drawing.add(drawing.circle((cx, cy), radius, fill=PANEL, stroke=INK, stroke_width=2))
    for number in range(1, face + 1):
        x, y = at(number, radius - 18)
        _text(drawing, str(number), x, y + 5, size=SMALL + 1,
              bold=number in (start, on_the_clock))
        tx, ty = at(number, radius)
        ix, iy = at(number, radius - 6)
        drawing.add(drawing.line((round(tx, 2), round(ty, 2)), (round(ix, 2), round(iy, 2)),
                                 stroke=INK, stroke_width=1))
    for hop in range(hours):
        a = start + hop
        b = a + 1
        x0, y0 = at(a + 0.12, radius + 8)
        x1, y1 = at(b - 0.12, radius + 8)
        mx, my = at(a + 0.5, radius + 22)
        drawing.add(drawing.path(d=f"M {x0:.2f} {y0:.2f} Q {mx:.2f} {my:.2f} {x1:.2f} {y1:.2f}",
                                 fill="none", stroke=INK, stroke_width=1.5))
        bx, by = at(b - 0.3, radius + 14)
        _head(drawing, (x1, y1), (bx, by), size=7)
        lx, ly = at(a + 0.5, radius + 30)
        _text(drawing, str(hop + 1), lx, ly + 4, size=SMALL - 1, fill=MUTED)
    sx, sy = at(start, radius - 18)
    ex, ey = at(on_the_clock, radius - 18)
    drawing.add(drawing.circle((round(sx, 2), round(sy, 2)), 12, fill="none", stroke=INK, stroke_width=1.2,
                               stroke_dasharray="3,3"))
    drawing.add(drawing.circle((round(ex, 2), round(ey, 2)), 12, fill="none", stroke=INK, stroke_width=2))
    _text(drawing, "On a clock", cx, 22, bold=True)
    _text(drawing, f"{start} + {hours} → {on_the_clock}", cx, 272)
    return drawing.tostring()


def names_point_at_values() -> str:
    """*Recipes are algorithms*: why `water_ml` still says 750 after `cups = 5`.

    The page's surprise is about when a line runs. Drawn as names pointing
    at values, the second picture shows `cups` moving to a new value while
    nothing moves `water_ml`, because no line pointed it anywhere new. The
    values are the ones the page's two cells make, run here.
    """
    first = _run("recipes-are-algorithms", "recipes-names-1")
    before = {"cups": first["cups"], "water_ml": first["water_ml"]}
    second = _run("recipes-are-algorithms", "recipes-names-2", dict(first))
    after = {"cups": second["cups"], "water_ml": second["water_ml"]}
    if after["water_ml"] != before["water_ml"]:
        raise SystemExit("recipes-are-algorithms: water_ml changed, so the picture's point is gone")

    width, height = 660, 210
    drawing = _drawing(width, height)

    def panel(x0: float, title: str, values: dict, old: dict | None) -> None:
        _text(drawing, title, x0 + 110, 26, mono=True, size=SMALL + 1)
        for row, name in enumerate(("cups", "water_ml")):
            y = 64 + row * 70
            _box(drawing, x0, y, 100, 34, fill=PANEL)
            _text(drawing, name, x0 + 50, y + 22, mono=True)
            vx = x0 + 150
            _box(drawing, vx, y, 70, 34, fill=FILL_AMBER, rx=17)
            _text(drawing, str(values[name]), vx + 35, y + 22, bold=True)
            _arrow(drawing, (x0 + 100, y + 17), (vx, y + 17))
            if old and old[name] != values[name]:
                ox = vx + 80
                _box(drawing, ox, y, 50, 34, fill="none", stroke=MUTED, dashed=True, rx=17)
                _text(drawing, str(old[name]), ox + 25, y + 22, fill=MUTED)
                _text(drawing, "no name points here now", ox + 25, y + 52, size=SMALL - 1,
                      fill=MUTED)

    panel(16, "after the first cell", before, None)
    panel(316, "after cups = 5", after, before)
    drawing.add(drawing.line((300, 40), (300, 190), stroke=RULE, stroke_width=1))
    return drawing.tostring()


SEGMENT_ORDER = "abcdefg"      # bit worth 1 is a, bit worth 64 is g, as the page says


def _segments_lit(pattern: int) -> set[str]:
    return {letter for place, letter in enumerate(SEGMENT_ORDER) if pattern >> place & 1}


def _seven_segment(drawing, x: float, y: float, lit: set[str], *, letters: bool,
                   w: float = 70, h: float = 120, t: float = 12) -> None:
    """One digit: seven bars, the lit ones filled, each optionally lettered."""
    half = h / 2
    bars = {
        "a": (x + t, y, w - 2 * t, t, "h"),
        "g": (x + t, y + half - t / 2, w - 2 * t, t, "h"),
        "d": (x + t, y + h - t, w - 2 * t, t, "h"),
        "f": (x, y + t, t, half - 1.5 * t, "v"),
        "b": (x + w - t, y + t, t, half - 1.5 * t, "v"),
        "e": (x, y + half + t / 2, t, half - 1.5 * t, "v"),
        "c": (x + w - t, y + half + t / 2, t, half - 1.5 * t, "v"),
    }
    for letter, (bx, by, bw, bh, _kind) in bars.items():
        on = letter in lit
        _box(drawing, bx, by, bw, bh, fill=FILL_AMBER if on else "none",
             stroke=INK if on else MUTED, width=1.6 if on else 0.9, rx=3,
             dashed=not on)
        if letters:
            _text(drawing, letter, bx + bw / 2, by + bh / 2 + 5, size=SMALL + 1, bold=True)


def seven_segments() -> str:
    """*Numbers a computer can hold*: the seven segments, named a to g.

    The page drew this in `#` and letters, which a screen reader spells out
    character by character. Here the named bars sit beside the two digits
    the prose uses, 1 and 8, and which bars those two light is read from the
    bit patterns on *Everything is ones and zeros*, so the two pages cannot
    disagree about which bar is which.
    """
    source = _cell("everything-is-ones-and-zeros", "everything-is-bytes-1")
    patterns = [ast.literal_eval(line.strip()[len("print("):-1])
                for line in source.splitlines() if line.strip().startswith("print(0b")]
    one, eight = patterns[0], patterns[1]
    if _segments_lit(one) != {"b", "c"} or _segments_lit(eight) != set(SEGMENT_ORDER):
        raise SystemExit("everything-is-ones-and-zeros: the patterns for 1 and 8 changed")

    width, height = 520, 200
    drawing = _drawing(width, height)
    places = [(70, set(SEGMENT_ORDER), True, "the names, a to g"),
              (225, _segments_lit(one), False, "1 lights " + " and ".join(sorted(_segments_lit(one)))),
              (380, _segments_lit(eight), False, "8 lights all seven")]
    for x, lit, letters, caption in places:
        if letters:
            _seven_segment(drawing, x, 22, set(), letters=True)
        else:
            _seven_segment(drawing, x, 22, lit, letters=False)
        _text(drawing, caption, x + 35, 174, size=SMALL + 1)
    return drawing.tostring()


def eight_as_bits() -> str:
    """*Everything is ones and zeros*: the pixel 8, a row of bits per row.

    The page says each row of 4 pixels is 4 bits and so one hex digit, and
    then asks the reader to trust that `0x6996996` is the 8. Laid out row
    by row, the digits of the number can be read straight down the right
    edge. Each row is taken from the number the page's cell holds, with the
    same `// 16 ** place % 16` the page's `digit_at` uses.
    """
    glyph = _assigned("everything-is-ones-and-zeros", "everything-is-glyph-1", "eight")
    rows = 7
    digits = [glyph // 16 ** place % 16 for place in range(rows - 1, -1, -1)]

    cell, gap = 26, 3
    width, height = 470, rows * (cell + gap) + 90
    drawing = _drawing(width, height)
    left, top = 40, 34
    _text(drawing, "pixels", left + 2 * (cell + gap), top - 12, size=SMALL, fill=MUTED)
    _text(drawing, "bits", 230, top - 12, size=SMALL, fill=MUTED)
    _text(drawing, "hex", 330, top - 12, size=SMALL, fill=MUTED)
    for row, digit in enumerate(digits):
        y = top + row * (cell + gap)
        bits = format(digit, "04b")
        for column, bit in enumerate(bits):
            x = left + column * (cell + gap)
            on = bit == "1"
            drawing.add(drawing.rect((x, y), (cell, cell), fill=INK if on else "none",
                                     stroke=INK if on else RULE, stroke_width=1))
        _text(drawing, " ".join(bits), 230, y + cell / 2 + 5, mono=True)
        _text(drawing, "→", 290, y + cell / 2 + 5, fill=MUTED)
        _text(drawing, format(digit, "X"), 330, y + cell / 2 + 5, mono=True, bold=True)
    bottom = top + rows * (cell + gap)
    _text(drawing, "read down:", 330, bottom + 18, size=SMALL, fill=MUTED)
    _text(drawing, "0x" + format(glyph, "X"), 330, bottom + 36, mono=True, bold=True)
    _arrow(drawing, (372, top + 4), (372, bottom - 8), stroke=MUTED, width=1.2, head=7)
    return drawing.tostring()


# ==========================================================================
# Unit 2
# ==========================================================================

def _number_line(drawing, left: float, right: float, y: float, low: int, high: int,
                 every: int, *, labels: bool = True) -> callable:
    """A horizontal number line; returns the function from a value to its x."""
    def x_of(value: float) -> float:
        return left + (value - low) / (high - low) * (right - left)

    drawing.add(drawing.line((left, y), (right, y), stroke=INK, stroke_width=1.3))
    for value in range(low, high + 1, every):
        x = x_of(value)
        drawing.add(drawing.line((round(x, 2), y - 5), (round(x, 2), y + 5), stroke=INK, stroke_width=1))
        if labels:
            _text(drawing, _minus(value), x, y + 21, size=SMALL)
    return x_of


def two_rules_on_a_line() -> str:
    """*Choosing a path*: "below 0" and "80 and over", drawn as the page describes.

    The prose describes this picture in full, circle by circle, and then
    asks the reader to hold it in their head. The rules are data here: the
    limit, which way the rule runs and whether the limit is included decide
    the ray, and whether the circle is filled.
    """
    low, high = -20, 100
    rules = [  # (rule, when, limit, runs towards, limit included), from the page's table
        ("Do not charge the battery", "below 0 °C", 0, low, False),
        ("Slow the processor a lot", "80 °C and over", 80, high, True),
    ]
    width, height = 640, 230
    drawing = _drawing(width, height)
    left, right = 40, 600
    for row, (words, when, limit, towards, included) in enumerate(rules):
        y = 62 + row * 94
        x_of = _number_line(drawing, left, right, y, low, high, 10)
        end = x_of(towards)
        drawing.add(drawing.line((round(x_of(limit), 2), y), (round(end, 2), y),
                                 stroke=INK, stroke_width=6))
        _head(drawing, (end + (8 if towards > limit else -8), y), (end, y), size=14)
        drawing.add(drawing.circle((round(x_of(limit), 2), y), 7,
                                   fill=INK if included else PAPER, stroke=INK, stroke_width=2.5))
        if towards < limit:
            _text(drawing, f"{words}: {when}", left - 8, y - 20, size=SMALL + 1, anchor="start")
        else:
            _text(drawing, f"{words}: {when}", right + 8, y - 20, size=SMALL + 1, anchor="end")
    _text(drawing, "temperature, °C", (left + right) / 2, height - 8, size=SMALL, fill=MUTED)
    return drawing.tostring()


def turning_the_line_round() -> str:
    """*Choosing a path*: multiplying by −1 turns the number line round.

    The page states it and then tests it; the picture shows the order of two
    numbers swapping as each one crosses to its mirror place. The two
    numbers and the factor are the ones in the page's sign cell.
    """
    small, large = 3, 5
    factor = -1
    if not (small < large and small * factor > large * factor):
        raise SystemExit("the order should turn round, and it did not")
    width, height = 600, 200
    drawing = _drawing(width, height)
    top_y, bottom_y = 58, 150
    left, right = 40, 560
    x_top = _number_line(drawing, left, right, top_y, -6, 6, 1)
    x_bottom = _number_line(drawing, left, right, bottom_y, -6, 6, 1)
    for value, fill in ((small, FILL_BLUE), (large, FILL_AMBER)):
        drawing.add(drawing.circle((round(x_top(value), 2), top_y), 8, fill=fill, stroke=INK, stroke_width=1.6))
        target = value * factor
        drawing.add(drawing.circle((round(x_bottom(target), 2), bottom_y), 8, fill=fill, stroke=INK, stroke_width=1.6))
        _arrow(drawing, (x_top(value), top_y + 30), (x_bottom(target), bottom_y - 12),
               stroke=MUTED, width=1.2, dashed=True, head=7)
    _text(drawing, f"{small} < {large}: {small} is further left", left, 22, anchor="start", size=SMALL + 1)
    _text(drawing, f"times {_minus(factor)}", right, 22, anchor="end", size=SMALL + 1, fill=MUTED)
    _text(drawing, f"{_minus(small * factor)} > {_minus(large * factor)}: "
                   f"now {_minus(large * factor)} is further left",
          left, height - 8, anchor="start", size=SMALL + 1)
    return drawing.tostring()


def _sideways_tree(drawing, root_label: str, options_after, leaves_note,
                   *, left: float, top: float, row_gap: float, column_gap: float,
                   titles: list[str] | None = None) -> float:
    """A tree that grows left to right, one column per choice, leaves stacked.

    `options_after(path)` gives the choices open after the path so far, and
    an empty list ends a branch, so a choice can shrink what is left (songs)
    or leave it alone (outfits). `leaves_note(index, path)` labels each leaf.
    Returns the bottom y.
    """
    children_of = options_after
    rows: list[tuple[str, ...]] = []

    def walk(path: tuple) -> None:
        options = children_of(path)
        if not options:
            rows.append(path)
            return
        for option in options:
            walk(path + (option,))

    walk(())
    depth = max(len(row) for row in rows)
    widths = [max(_width_of(str(row[level]), SMALL + 1) + 18 for row in rows)
              for level in range(depth)]
    root_w = _width_of(root_label, SMALL + 1) + 18
    xs = [left + root_w + column_gap]
    for level in range(1, depth):
        xs.append(xs[-1] + widths[level - 1] + column_gap)
    node_h = row_gap - 8

    centre: dict[tuple, float] = {}
    for index, row in enumerate(rows):
        centre[row] = top + index * row_gap + row_gap / 2
    for level in range(depth - 1, 0, -1):
        for row in rows:
            prefix = row[:level]
            kids = [c for p, c in centre.items() if len(p) == level + 1 and p[:level] == prefix]
            centre[prefix] = (min(kids) + max(kids)) / 2
    root_y = (min(centre[row] for row in rows) + max(centre[row] for row in rows)) / 2

    if titles:
        for level, title in enumerate(titles):
            _text(drawing, title, xs[level] + widths[level] / 2, top - 8, size=SMALL, fill=MUTED)

    def node(x: float, y: float, w: float, label: str) -> None:
        _box(drawing, x, y - node_h / 2, w, node_h)
        _text(drawing, label, x + w / 2, y + 5, size=SMALL + 1)

    node(left, root_y, root_w, root_label)
    for path, y in sorted(centre.items(), key=lambda item: len(item[0])):
        level = len(path) - 1
        parent_y = root_y if level == 0 else centre[path[:-1]]
        parent_right = (left + root_w) if level == 0 else xs[level - 1] + widths[level - 1]
        drawing.add(drawing.line((round(parent_right, 2), round(parent_y, 2)),
                                 (round(xs[level], 2), round(y, 2)), stroke=INK, stroke_width=1.2))
        node(xs[level], y, widths[level], str(path[-1]))
    note_x = xs[-1] + widths[-1] + 18
    for index, row in enumerate(rows):
        _text(drawing, leaves_note(index, row), note_x, centre[row] + 5, anchor="start",
              size=SMALL + 1, mono=True)
    return top + len(rows) * row_gap


def rows_as_a_tree() -> str:
    """*True, false and every case*: why n inputs give 2ⁿ rows, counting in binary.

    The loops on the page make the rows; the tree is those loops seen from
    the side. Each column doubles the branches, and the leaves, read top to
    bottom, are 0 to 7 in binary, which is the page's surprise. The input
    names are the loop variables of the page's own cell.
    """
    names = _loop_names("true-false-and-every-case", "true-false-rows-1")
    if len(names) != 3:
        raise SystemExit("true-false-and-every-case: the rows cell no longer has three loops")

    def options(path):
        return [False, True] if len(path) < len(names) else []

    width, height = 620, 8 * 30 + 60
    drawing = _drawing(width, height)

    def note(index, row):
        bits = "".join(str(int(value)) for value in row)
        if int(bits, 2) != index:
            raise SystemExit("the rows no longer count in binary")
        return f"{' '.join(bits)}   row {index}"

    _sideways_tree(drawing, "start", options, note, left=MARGIN, top=36, row_gap=30,
                   column_gap=30, titles=names)
    return drawing.tostring()


def grey_out_grids() -> str:
    """*Untangling a condition*: two rules as two 2-by-2 grids.

    A truth table with two inputs is a grid, and "True in three rows" against
    "True in one row" is the whole difference between the rule and the
    tempting arithmetic move. Each square is filled by calling the page's own
    functions on that square's inputs.
    """
    rules = _functions("untangling-a-condition", "untangling-two-tests")
    rules.update(_functions("untangling-a-condition", "untangling-arithmetic-move"))
    pictured = [("grey_out_a", "not (is_open and has_stock)"),
                ("grey_out_c", "not is_open and not has_stock")]

    cell_w, cell_h = 92, 50
    width, height = 700, 230
    drawing = _drawing(width, height)
    for panel, (name, words) in enumerate(pictured):
        rule = rules[name]
        x0 = 130 + panel * 350
        y0 = 70
        _text(drawing, words, x0 + cell_w, 24, mono=True, size=SMALL + 1)
        _text(drawing, "has_stock", x0 + cell_w, 46, mono=True, size=SMALL, fill=MUTED)
        for column, stock in enumerate((False, True)):
            _text(drawing, str(stock), x0 + column * cell_w + cell_w / 2, y0 - 6,
                  size=SMALL, fill=MUTED)
        _text(drawing, "is_open", x0 - 56, y0 + cell_h + 5, mono=True, size=SMALL,
              fill=MUTED, anchor="end")
        greyed = 0
        for row, is_open in enumerate((False, True)):
            _text(drawing, str(is_open), x0 - 8, y0 + row * cell_h + cell_h / 2 + 5,
                  size=SMALL, fill=MUTED, anchor="end")
            for column, has_stock in enumerate((False, True)):
                result = rule(is_open, has_stock)
                greyed += result
                x, y = x0 + column * cell_w, y0 + row * cell_h
                drawing.add(drawing.rect((x, y), (cell_w, cell_h),
                                         fill=FILL_AMBER if result else PAPER,
                                         stroke=INK, stroke_width=1.3))
                _text(drawing, "greyed out" if result else "Order works",
                      x + cell_w / 2, y + cell_h / 2 + 5, size=SMALL,
                      bold=bool(result))
        _text(drawing, f"True in {greyed} of 4 squares", x0 + cell_w, y0 + 2 * cell_h + 34,
              size=SMALL + 1)
    return drawing.tostring()


def parity_check() -> str:
    """*Bits that flip*: one flip changes the count of 1s from odd to even; two flips do not.

    The bytes are the page's own: 14, and the two noise masks from its two
    cells. The count of 1s and what the check says are computed with the
    page's rule, XOR of all the bits, so the picture shows the same verdict
    the cells print, about the message and never about the reader.
    """
    sent = _assigned("bits-that-flip", "bits-catch-1", "sent_byte")
    one_flip = _assigned("bits-that-flip", "bits-catch-1", "noise")
    two_flips = _assigned("bits-that-flip", "bits-catch-2", "noise")

    def parity(value: int) -> int:
        result = 0
        for bit in format(value, "08b"):
            result ^= int(bit)
        return result

    sent_parity = parity(sent)
    sent_kind = "odd" if sent_parity else "even"
    rows = [("sent", sent, 0), ("one bit flips", sent ^ one_flip, one_flip),
            ("two bits flip", sent ^ two_flips, two_flips)]
    cell = 28
    width, height = 700, 50 + len(rows) * 66
    drawing = _drawing(width, height)
    left = 120
    _text(drawing, "the byte", left + 4 * cell, 22, size=SMALL, fill=MUTED)
    _text(drawing, "parity bit", left + 8 * cell + 36, 22, size=SMALL, fill=MUTED)
    for index, (words, value, mask) in enumerate(rows):
        y = 34 + index * 66
        _text(drawing, words, left - 12, y + cell / 2 + 5, anchor="end", size=SMALL + 1)
        bits = format(value, "08b")
        flips = format(mask, "08b")
        flipped_at = [place for place, flag in enumerate(flips) if flag == "1"]
        for place, bit in enumerate(bits):
            flipped = place in flipped_at
            x = left + place * cell
            drawing.add(drawing.rect((x, y), (cell - 2, cell),
                                     fill=FILL_PINK if flipped else PANEL,
                                     stroke=INK, stroke_width=2.2 if flipped else 1))
            _text(drawing, bit, x + (cell - 2) / 2, y + cell / 2 + 5, mono=True, bold=flipped)
        if flipped_at:
            middle = left + (flipped_at[0] + flipped_at[-1] + 1) / 2 * cell - 1
            _text(drawing, "flipped", middle, y + cell + 14, size=SMALL - 1, fill=MUTED)
        px = left + 8 * cell + 22
        drawing.add(drawing.rect((px, y), (cell - 2, cell), fill=FILL_BLUE, stroke=INK, stroke_width=1))
        _text(drawing, str(sent_parity), px + (cell - 2) / 2, y + cell / 2 + 5, mono=True)
        ones = bits.count("1")
        kind = "odd" if ones % 2 else "even"
        count_words = f"{ones} one{'s' if ones != 1 else ''} in the byte: {kind}"
        if index == 0:
            second = f"so the parity bit is {sent_parity}"
        elif parity(value) == sent_parity:
            second = f"was {sent_kind}: the check sees nothing"
        else:
            second = f"was {sent_kind}: the check sees a change"
        nx = px + cell + 16
        _text(drawing, count_words, nx, y + 10, anchor="start", size=SMALL + 1)
        _text(drawing, second, nx, y + 28, anchor="start", size=SMALL + 1, bold=index > 0)
    return drawing.tostring()


# ==========================================================================
# Unit 3
# ==========================================================================

def pairing_the_ends() -> str:
    """*Doing it again*: 1 + 2 + … + n, twice, is an n by n + 1 rectangle.

    The page pairs the ends in a table of numbers; drawn as squares, the two
    staircases fit together and the rectangle is there to count. The count
    under it is checked against a plain sum before anything is drawn.
    """
    n = 6
    forwards = sum(range(1, n + 1))
    if 2 * forwards != n * (n + 1):
        raise SystemExit("the two staircases do not make the rectangle")
    size = 30
    width, height = 640, n * size + 64
    drawing = _drawing(width, height)
    left, top = 100, 20
    for row in range(n):
        forward = row + 1
        y = top + row * size
        for column in range(n + 1):
            ours = column < forward
            drawing.add(drawing.rect((left + column * size, y), (size - 2, size - 2),
                                     fill=FILL_AMBER if ours else FILL_BLUE,
                                     stroke=INK, stroke_width=1))
        _text(drawing, str(forward), left - 12, y + size / 2 + 4, anchor="end", size=SMALL + 1)
        _text(drawing, str(n + 1 - forward), left + (n + 1) * size + 10, y + size / 2 + 4,
              anchor="start", size=SMALL + 1)
    _text(drawing, "forwards", left - 12, top - 4 + n * size + 22, anchor="end", size=SMALL, fill=MUTED)
    _text(drawing, "backwards", left + (n + 1) * size + 10, top - 4 + n * size + 22,
          anchor="start", size=SMALL, fill=MUTED)
    notes_x = left + (n + 1) * size + 70
    lines = [
        f"left staircase: 1 + 2 + … + {n}",
        f"right staircase: {n} + {n - 1} + … + 1",
        f"each row: {n + 1} squares",
        f"{n} rows: {n} × {n + 1} = {n * (n + 1)} squares",
        f"so the sum is {n * (n + 1)} ÷ 2 = {forwards}",
    ]
    for index, line in enumerate(lines):
        _text(drawing, line, notes_x, top + 26 + index * 30, anchor="start", size=SMALL + 1,
              bold=index == len(lines) - 1)
    return drawing.tostring()


def outfit_tree() -> str:
    """*Counting every outfit*: the tree the page drew in box-drawing characters.

    Drawn from the page's own lists, so a fourth top added to the cell is a
    fourth branch here after a regeneration. The leaves are numbered, which
    is the count the page asks for.
    """
    tops = _assigned("counting-every-outfit", "counting-every-outfits-1", "tops")
    trousers = _assigned("counting-every-outfit", "counting-every-outfits-1", "trousers")

    def options(path):
        return [tops, trousers][len(path)] if len(path) < 2 else []

    rows = len(tops) * len(trousers)
    width, height = 560, rows * 32 + 50
    drawing = _drawing(width, height)
    _sideways_tree(drawing, "an outfit", options, lambda index, row: str(index + 1),
                   left=MARGIN, top=34, row_gap=32, column_gap=34,
                   titles=["top", "trousers"])
    return drawing.tostring()


def song_order_tree() -> str:
    """*Orders and choices*: 3 choices, then 2, then 1, as a tree.

    The shrinking is the point, so each branch offers only the songs not yet
    played; the tree is built by that rule, not drawn from a list of the six
    answers, and it checks that it found 3! of them.
    """
    songs = _assigned("orders-and-choices", "orders-songs-1", "songs")

    def options(path):
        return [song for song in songs if song not in path]

    leaves = math.factorial(len(songs))
    width, height = 620, leaves * 32 + 50
    drawing = _drawing(width, height)
    count = []

    def note(index, row):
        count.append(row)
        return str(index + 1)

    _sideways_tree(drawing, "shuffle", options, note, left=MARGIN, top=34, row_gap=32,
                   column_gap=30,
                   titles=[f"first: {len(songs)} choices", f"second: {len(songs) - 1} left",
                           f"third: {len(songs) - 2} left"])
    if len(count) != leaves:
        raise SystemExit("the tree did not find n! orders")
    return drawing.tostring()


def sensor_pairs() -> str:
    """*Orders and choices*: 12 ordered picks are 6 choices, each met twice.

    The grid is every (first, second) pick; the diagonal is a sensor picked
    twice, which the page rules out. The page's loop starts the second pick
    after the first, which is the upper triangle, numbered in the loop's own
    order. Each lower square carries the same number: the same two sensors,
    the other way round. That is the division by 2! the prose then states.
    """
    sensors = _assigned("orders-and-choices", "orders-sensors-1", "sensors")
    count = len(sensors)
    numbering = {}
    for first in range(count):
        for second in range(first + 1, count):
            numbering[(first, second)] = len(numbering) + 1
    if len(numbering) * 2 != count * (count - 1):
        raise SystemExit("the choices do not halve the ordered picks")

    cell = 80
    left, top = 110, 64
    width, height = left + count * cell + 200, top + count * cell + 16
    drawing = _drawing(width, height)
    _text(drawing, "second sensor", left + count * cell / 2, 14, size=SMALL, fill=MUTED)
    _text(drawing, "first sensor", left - 10, top - 12, anchor="end", size=SMALL, fill=MUTED)
    for index, name in enumerate(sensors):
        _text(drawing, name, left + index * cell + cell / 2, top - 10 - (index % 2) * 16, size=SMALL)
        _text(drawing, name, left - 10, top + index * cell + cell / 2 + 5, anchor="end", size=SMALL)
    for first in range(count):
        for second in range(count):
            x, y = left + second * cell, top + first * cell
            if first == second:
                drawing.add(drawing.rect((x, y), (cell, cell), fill=PAPER, stroke=INK, stroke_width=1))
                drawing.add(drawing.line((x + 8, y + 8), (x + cell - 8, y + cell - 8),
                                         stroke=MUTED, stroke_width=1))
                continue
            key = (min(first, second), max(first, second))
            upper = second > first
            drawing.add(drawing.rect((x, y), (cell, cell), fill=FILL_GREEN if upper else PANEL,
                                     stroke=INK, stroke_width=1))
            _text(drawing, str(numbering[key]), x + cell / 2, y + cell / 2 + 6,
                  size=LABEL + 2, bold=upper, fill=INK if upper else MUTED)
    notes_x = left + count * cell + 20
    notes = [f"{count * (count - 1)} ordered picks", "each choice of two", "appears twice,",
             "once each way round", f"so {len(numbering)} choices"]
    for index, line in enumerate(notes):
        _text(drawing, line, notes_x, top + 40 + index * 24, anchor="start", size=SMALL + 1,
              bold=index == len(notes) - 1)
    return drawing.tostring()


def _dice_grid(drawing, left: float, top: float, cell: float, fill_of, text_of,
               *, row_name: str, column_name: str) -> None:
    faces = range(1, 7)
    _text(drawing, column_name, left + 3 * cell, top - 30, size=SMALL, fill=MUTED)
    _text(drawing, row_name, left - 34, top + 3 * cell + 4, size=SMALL, fill=MUTED, anchor="end")
    for index, face in enumerate(faces):
        _text(drawing, str(face), left + index * cell + cell / 2, top - 8, size=SMALL + 1, bold=True)
        _text(drawing, str(face), left - 10, top + index * cell + cell / 2 + 5, size=SMALL + 1,
              bold=True, anchor="end")
    for row, first in enumerate(faces):
        for column, second in enumerate(faces):
            x, y = left + column * cell, top + row * cell
            fill, strong = fill_of(first, second)
            drawing.add(drawing.rect((x, y), (cell, cell), fill=fill, stroke=INK,
                                     stroke_width=2.2 if strong else 1))
            _text(drawing, text_of(first, second), x + cell / 2, y + cell / 2 + 5,
                  size=SMALL + (1 if strong else 0), bold=strong,
                  fill=INK if strong else MUTED)


def sum_of_seven() -> str:
    """*How likely is it?*: the 36 pairs, each with its sum, the 7s marked.

    The page counts the sevens with a loop; the grid shows why there are six
    of them (a diagonal) and one twelve (a corner). Every sum is computed.
    """
    faces = _assigned("how-likely-is-it", "likely-dice-1", "faces")
    sevens = sum(1 for red in faces for blue in faces if red + blue == 7)
    twelves = sum(1 for red in faces for blue in faces if red + blue == 12)
    cell = 44
    left, top = 110, 56
    width, height = left + 6 * cell + 230, top + 6 * cell + 20
    drawing = _drawing(width, height)

    def fill_of(red, blue):
        total = red + blue
        if total == 7:
            return FILL_AMBER, True
        if total == 12:
            return FILL_BLUE, True
        return PAPER, False

    _dice_grid(drawing, left, top, cell, fill_of, lambda r, b: str(r + b),
               row_name="red", column_name="blue")
    notes_x = left + 6 * cell + 24
    _text(drawing, f"sum 7: {sevens} of {len(faces) ** 2}", notes_x, top + 40, anchor="start", bold=True)
    _text(drawing, "a line from corner to corner", notes_x, top + 60, anchor="start", size=SMALL, fill=MUTED)
    _text(drawing, f"sum 12: {twelves} of {len(faces) ** 2}", notes_x, top + 110, anchor="start", bold=True)
    _text(drawing, "one corner only", notes_x, top + 130, anchor="start", size=SMALL, fill=MUTED)
    return drawing.tostring()


def two_sixes() -> str:
    """*Chances that combine*: the grid the page asks the reader to draw.

    A six on the first die is one row in six; inside it, a six on the second
    is one square in six. Row and square are both labelled with their
    fraction of the grid, computed, so "of means multiply" can be read off.
    """
    faces = _assigned("chances-that-combine", "chances-dice-1", "faces")
    total = len(faces) ** 2
    row_share = Fraction(len(faces), total)
    square_share = Fraction(1, total)
    if row_share * Fraction(1, len(faces)) != square_share:
        raise SystemExit("one sixth of one sixth is no longer one thirty-sixth")
    cell = 44
    left, top = 110, 56
    width, height = left + 6 * cell + 250, top + 6 * cell + 20
    drawing = _drawing(width, height)
    six = max(faces)

    def fill_of(first, second):
        if first == six and second == six:
            return FILL_AMBER, True
        if first == six:
            return FILL_BLUE, False
        return PAPER, False

    _dice_grid(drawing, left, top, cell, fill_of,
               lambda first, second: f"{first},{second}",
               row_name="first die", column_name="second die")
    notes_x = left + 6 * cell + 24
    row_y = top + 5 * cell + cell / 2
    _text(drawing, f"row {six}: {row_share.numerator}/{row_share.denominator} of the grid",
          notes_x, row_y - 40, anchor="start")
    _text(drawing, f"square {six},{six}: 1/{len(faces)} of that row,", notes_x, row_y - 10,
          anchor="start", bold=True)
    _text(drawing, f"which is {square_share.numerator}/{square_share.denominator} of the grid",
          notes_x, row_y + 10, anchor="start", bold=True)
    return drawing.tostring()


# ==========================================================================
# Unit 4
# ==========================================================================

def _machine(drawing, x: float, y: float, w: float, h: float, lines: list[str]) -> None:
    """A machine: a box with a slot on the left and a tray on the right."""
    _box(drawing, x, y, w, h, fill=PANEL, width=2, rx=10)
    drawing.add(drawing.rect((x - 6, y + h / 2 - 12), (12, 24), fill=PAPER, stroke=INK, stroke_width=1.6))
    drawing.add(drawing.rect((x + w - 6, y + h / 2 - 12), (12, 24), fill=PAPER, stroke=INK, stroke_width=1.6))
    for index, line in enumerate(lines):
        _text(drawing, line, x + w / 2, y + h / 2 + 5 + (index - (len(lines) - 1) / 2) * 22,
              mono=index > 0, size=LABEL + (1 if index == 0 else -1), bold=index == 0)


def one_slot_machine() -> str:
    """*Machines that take a number*: the machine the page asks the reader to picture.

    The input is the page's 0.75 volts, and the output is what the page's
    own `sensor_celsius` returns for it, so the number in the tray is the
    number under the cell.
    """
    functions = _functions("machines-that-take-a-number", "machines-slot-1")
    volts = 0.75
    celsius = functions["sensor_celsius"](volts)
    width, height = 620, 150
    drawing = _drawing(width, height)
    _machine(drawing, 190, 26, 240, 96, ["f(x) = 100x − 50", "sensor_celsius"])
    _text(drawing, "in the slot", 80, 50, size=SMALL, fill=MUTED)
    _box(drawing, 40, 58, 80, 34, fill=FILL_AMBER, rx=17)
    _text(drawing, f"{volts}", 80, 80, bold=True)
    _text(drawing, "volts", 80, 110, size=SMALL, fill=MUTED)
    _arrow(drawing, (122, 75), (180, 75))
    _arrow(drawing, (440, 75), (498, 75))
    _text(drawing, "in the tray", 540, 50, size=SMALL, fill=MUTED)
    _box(drawing, 500, 58, 80, 34, fill=FILL_GREEN, rx=17)
    _text(drawing, str(celsius).replace("-", "\u2212"), 540, 80, bold=True)
    _text(drawing, "°C", 540, 110, size=SMALL, fill=MUTED)
    return drawing.tostring()


def walls_unfolded() -> str:
    """*Measuring rooms and tins*: the four walls unfolded into one strip.

    The strip's length is the walk round the room, wall by wall, and its
    height the room's; both come from the page's cell. The area is left off
    on purpose: the page asks for it straight after the picture.
    """
    length = _assigned("measuring-rooms-and-tins", "measuring-rooms-area-1", "length")
    width_m = _assigned("measuring-rooms-and-tins", "measuring-rooms-area-1", "width")
    height_m = _assigned("measuring-rooms-and-tins", "measuring-rooms-area-1", "height")
    walls = [length, width_m, length, width_m]
    perimeter = sum(walls)
    scale = 36
    left, top = 70, 40
    width, height = left + perimeter * scale + 40, top + height_m * scale + 80
    drawing = _drawing(width, height)
    x = left
    fills = [FILL_AMBER, FILL_BLUE, FILL_AMBER, FILL_BLUE]
    for index, wall in enumerate(walls):
        w = wall * scale
        drawing.add(drawing.rect((round(x, 2), top), (round(w, 2), round(height_m * scale, 2)),
                                 fill=fills[index], stroke=INK, stroke_width=1.6))
        _text(drawing, f"wall {index + 1}", x + w / 2, top + height_m * scale / 2 + 5, size=SMALL + 1)
        _text(drawing, f"{wall:g} m", x + w / 2, top - 10, size=SMALL + 1)
        x += w
    y = top + height_m * scale + 18
    drawing.add(drawing.line((left, y), (left + perimeter * scale, y), stroke=INK, stroke_width=1.2))
    for end in (left, left + perimeter * scale):
        drawing.add(drawing.line((end, y - 6), (end, y + 6), stroke=INK, stroke_width=1.2))
    _text(drawing, f"{' + '.join(f'{wall:g}' for wall in walls)} = {perimeter:g} m, the perimeter",
          left + perimeter * scale / 2, y + 22, size=SMALL + 1)
    _text(drawing, f"{height_m:g} m", left - 12, top + height_m * scale / 2 + 5, anchor="end",
          size=SMALL + 1)
    return drawing.tostring()


def triangle_half_rectangle() -> str:
    """*Measuring rooms and tins*: a triangle is half the rectangle round it.

    The two pieces left over are drawn again, each turned half a turn, and
    they fit together into a second copy of the triangle, which is the
    argument the prose makes in words. Base and height are the page's.
    """
    base = _assigned("measuring-rooms-and-tins", "measuring-rooms-triangle-1", "base")
    tall = _assigned("measuring-rooms-and-tins", "measuring-rooms-triangle-1", "height")
    apex = base * 0.35                      # anywhere along the top; it changes nothing
    scale = 60
    b, h, a = base * scale, tall * scale, apex * scale
    width, height = 2 * b + 170, h + 90
    drawing = _drawing(width, height)
    x0, y0 = 70, 30

    def poly(points, fill, dx=0.0):
        drawing.add(drawing.polygon([(round(x0 + dx + px, 2), round(y0 + py, 2)) for px, py in points],
                                    fill=fill, stroke=INK, stroke_width=1.6))

    poly([(0, 0), (a, 0), (0, h)], FILL_BLUE)
    poly([(a, 0), (b, 0), (b, h)], FILL_GREEN)
    poly([(0, h), (b, h), (a, 0)], FILL_AMBER)
    _text(drawing, "1", x0 + a * 0.3, y0 + h * 0.33, bold=True)
    _text(drawing, "2", x0 + b - (b - a) * 0.3, y0 + h * 0.33, bold=True)
    _text(drawing, "the triangle", x0 + a + (b - a) * 0.35, y0 + h * 0.8, size=SMALL + 1)
    drawing.add(drawing.line((round(x0 + a, 2), y0), (round(x0 + a, 2), y0 + h), stroke=INK,
                             stroke_width=1.2, stroke_dasharray="4,3"))
    _text(drawing, "height", x0 + a + 5, y0 + h * 0.42, anchor="start", size=SMALL)
    drawing.add(drawing.line((x0 - 10, y0), (x0 - 10, y0 + h), stroke=INK, stroke_width=1.2))
    for end in (y0, y0 + h):
        drawing.add(drawing.line((x0 - 15, end), (x0 - 5, end), stroke=INK, stroke_width=1.2))
    _text(drawing, f"{tall:g} m", x0 - 16, y0 + h / 2 + 5, anchor="end", size=SMALL + 1)
    _text(drawing, f"base {base:g} m", x0 + b / 2, y0 + h + 22, size=SMALL + 1)

    # Pieces 1 and 2, each turned half a turn, side by side: a second triangle.
    dx = b + 50
    poly([(a, h), (0, h), (a, 0)], FILL_BLUE, dx)
    poly([(b, h), (a, h), (a, 0)], FILL_GREEN, dx)
    _text(drawing, "1", x0 + dx + a * 0.7, y0 + h * 0.75, bold=True)
    _text(drawing, "2", x0 + dx + a + (b - a) * 0.25, y0 + h * 0.75, bold=True)
    _text(drawing, "pieces 1 and 2, turned round:", x0 + dx + b / 2, y0 + h + 22, size=SMALL + 1)
    _text(drawing, "the same triangle again", x0 + dx + b / 2, y0 + h + 40, size=SMALL + 1)
    return drawing.tostring()


def circle_into_rectangle() -> str:
    """*Measuring rooms and tins*: a circle cut into slices, laid top to tail.

    Sixteen slices, half pointing up and half down, make a shape whose
    height is the radius and whose length is half the way round, πr. Every
    slice is drawn at its true angle, so the scalloped top and bottom are
    what sixteen slices really give, not a tidied rectangle.
    """
    slices = 16
    radius = 64
    theta = 2 * math.pi / slices
    width, height = 660, 2 * radius + 90
    drawing = _drawing(width, height)
    cx, cy = 20 + radius, 30 + radius

    def sector(apex, facing: float, fill: str) -> None:
        start = facing - theta / 2
        end = facing + theta / 2
        p0 = (apex[0] + radius * math.cos(start), apex[1] + radius * math.sin(start))
        p1 = (apex[0] + radius * math.cos(end), apex[1] + radius * math.sin(end))
        drawing.add(drawing.path(
            d=f"M {apex[0]:.2f} {apex[1]:.2f} L {p0[0]:.2f} {p0[1]:.2f} "
              f"A {radius} {radius} 0 0 1 {p1[0]:.2f} {p1[1]:.2f} Z",
            fill=fill, stroke=INK, stroke_width=1))

    for index in range(slices):
        facing = -math.pi / 2 + (index + 0.5) * theta - math.pi / 2
        upper = math.sin(facing) < 0
        sector((cx, cy), facing, FILL_AMBER if upper else FILL_BLUE)
    _text(drawing, f"{slices} slices", cx, cy + radius + 26, size=SMALL + 1)

    chord = 2 * radius * math.sin(theta / 2)
    left = 2 * radius + 110
    top = cy - radius / 2 - 6
    base_y = top + radius * math.cos(theta / 2)
    for index in range(slices // 2):
        x = left + index * chord
        sector((x + chord / 2, base_y), -math.pi / 2, FILL_AMBER)        # point at the bottom
        sector((x + chord, top), math.pi / 2, FILL_BLUE)                   # point at the top
    span = slices // 2 * chord + chord / 2
    _arrow(drawing, (cx + radius + 16, cy), (left - 18, cy), stroke=MUTED, width=1.2, dashed=True)
    y = base_y + 22
    drawing.add(drawing.line((left, y), (left + span, y), stroke=INK, stroke_width=1.2))
    for end in (left, left + span):
        drawing.add(drawing.line((round(end, 2), y - 6), (round(end, 2), y + 6), stroke=INK, stroke_width=1.2))
    _text(drawing, "half the way round: πr", left + span / 2, y + 22, size=SMALL + 1)
    rx = left + span + 18
    drawing.add(drawing.line((round(rx, 2), round(top, 2)), (round(rx, 2), round(base_y, 2)),
                             stroke=INK, stroke_width=1.2))
    _text(drawing, "r", rx + 10, (top + base_y) / 2 + 5, anchor="start", italic=True)
    return drawing.tostring()


def undo_in_reverse() -> str:
    """*Running a formula backwards*: forwards on top, the way back underneath.

    The way back runs right to left under the way forwards, so each undoing
    step sits under the step it undoes and the last step forwards is visibly
    the first step back. Every value is computed with exact fractions from
    the page's −76 °F.
    """
    fahrenheit = _assigned("running-a-formula-backwards", "running-a-reverse-2", "fahrenheit")
    celsius = (Fraction(fahrenheit) - 32) * Fraction(5, 9)
    middle = celsius * Fraction(9, 5)
    if middle + 32 != fahrenheit:
        raise SystemExit("the forward formula no longer lands on the page's Fahrenheit")

    def show(value: Fraction) -> str:
        return _minus(int(value)) if value.denominator == 1 else _minus(float(value))

    width, height = 660, 200
    drawing = _drawing(width, height)
    xs = [70, 330, 590]
    top_y, bottom_y = 60, 150
    values_top = [f"{show(celsius)} °C", show(middle), f"{show(Fraction(fahrenheit))} °F"]
    values_bottom = [f"{show(celsius)} °C", show(middle), f"{show(Fraction(fahrenheit))} °F"]
    steps_top = ["× 9/5", "+ 32"]
    steps_bottom = ["× 5/9", "− 32"]
    _text(drawing, "forwards", 12, 22, anchor="start", size=SMALL, fill=MUTED)
    _text(drawing, "back: the last step forwards is undone first", 12, bottom_y + 44,
          anchor="start", size=SMALL, fill=MUTED)
    for row_y, values, steps_words, forwards in ((top_y, values_top, steps_top, True),
                                                  (bottom_y, values_bottom, steps_bottom, False)):
        for index, text in enumerate(values):
            w = max(80, _width_of(text) + 20)
            _box(drawing, xs[index] - w / 2, row_y - 17, w, 34,
                 fill=FILL_AMBER if index != 1 else PANEL, rx=17)
            _text(drawing, text, xs[index], row_y + 5, bold=index != 1)
        for index, words in enumerate(steps_words):
            a, b = xs[index] + 50, xs[index + 1] - 50
            if forwards:
                _arrow(drawing, (a, row_y), (b, row_y))
            else:
                _arrow(drawing, (b, row_y), (a, row_y))
            _text(drawing, words, (a + b) / 2, row_y - 10, mono=True, size=SMALL + 1)
    return drawing.tostring()


def one_list_two_names() -> str:
    """*What a function can see*: `=` moves a name, `append` changes the list.

    Two panels, each the page's space beside the call's space at the moment
    the call ends. On the left, `points` was pointed at a new number and
    `score` never moved; on the right, `readings` and `today` point at the
    one list, which has grown. The values come from running the page's cells.
    """
    bonus = _run("what-a-function-can-see", "what-function-args-3")
    reading = _run("what-a-function-can-see", "what-function-list-1")
    score = bonus["score"]
    doubled = bonus["add_bonus"](score)
    today = reading["today"]
    if not (score != doubled and len(today) == 3):
        raise SystemExit("what-a-function-can-see: the cells no longer show the two moves")

    width, height = 680, 262
    drawing = _drawing(width, height)

    def space(x, y, w, h, title):
        _box(drawing, x, y, w, h, fill="none", stroke=MUTED, dashed=True, rx=8)
        _text(drawing, title, x + 8, y + 16, anchor="start", size=SMALL - 1, fill=MUTED)

    def name(x, y, text):
        _box(drawing, x, y, 84, 28, fill=PANEL)
        _text(drawing, text, x + 42, y + 19, mono=True, size=SMALL + 1)

    def value(x, y, text, w=58, fill=FILL_AMBER, dashed=False, stroke=INK, colour=INK):
        _box(drawing, x, y, w, 28, fill=fill, rx=14, dashed=dashed, stroke=stroke)
        _text(drawing, text, x + w / 2, y + 19, bold=not dashed, fill=colour)

    # Left: add_bonus(score)
    _text(drawing, "add_bonus(score)", 160, 20, mono=True, size=SMALL + 1)
    space(10, 34, 300, 70, "the page")
    space(10, 120, 300, 130, "add_bonus's space")
    name(24, 58, "score")
    value(200, 58, str(score))
    _arrow(drawing, (108, 72), (198, 72))
    name(24, 150, "points")
    value(200, 150, str(doubled))
    _arrow(drawing, (108, 164), (198, 164))
    value(200, 192, str(score), fill="none", dashed=True, stroke=MUTED, colour=MUTED)
    _arrow(drawing, (108, 170), (198, 204), stroke=MUTED, dashed=True, width=1.1)
    _text(drawing, "where points started, before the = line", 160, 242, size=SMALL - 1, fill=MUTED)

    # Right: add_reading(today, 15.1)
    _text(drawing, "add_reading(today, 15.1)", 510, 20, mono=True, size=SMALL + 1)
    space(350, 34, 150, 70, "the page")
    space(350, 120, 150, 130, "add_reading's space")
    name(364, 58, "today")
    name(364, 150, "readings")
    list_x, list_y = 530, 104
    cell_w = 44
    for index, item in enumerate(today):
        new = index == len(today) - 1
        drawing.add(drawing.rect((list_x + index * cell_w, list_y), (cell_w, 30),
                                 fill=FILL_GREEN if new else PANEL, stroke=INK, stroke_width=1.3))
        _text(drawing, f"{item:g}", list_x + index * cell_w + cell_w / 2, list_y + 20, size=SMALL,
              bold=new)
    _text(drawing, "one list", list_x + len(today) * cell_w / 2, list_y + 50, size=SMALL - 1, fill=MUTED)
    _arrow(drawing, (448, 72), (list_x, list_y + 8))
    _arrow(drawing, (448, 164), (list_x, list_y + 24))
    drawing.add(drawing.line((330, 30), (330, 250), stroke=RULE, stroke_width=1))
    return drawing.tostring()


# ==========================================================================
# Unit 5
# ==========================================================================

def indexes_both_ways() -> str:
    """*A row of numbers*: every position with its index from the front and from the back.

    The list and the day names are the page's own, and each negative index
    is computed as `i - len(week)`, the rule the page states in words.
    """
    week = _assigned("a-row-of-numbers", "row-week-1", "week")
    days = _assigned("a-row-of-numbers", "row-by-index-1", "days")
    if len(days) != len(week):
        raise SystemExit("a-row-of-numbers: days and week are not the same length")
    cell = 64
    left, top = 150, 60
    width, height = left + len(week) * cell + 20, top + 80
    drawing = _drawing(width, height)
    _text(drawing, "day", left - 16, top - 36, anchor="end", size=SMALL, fill=MUTED)
    _text(drawing, "index", left - 16, top - 10, anchor="end", size=SMALL, fill=MUTED)
    _text(drawing, "week", left - 16, top + 25, anchor="end", mono=True)
    _text(drawing, "negative index", left - 16, top + 62, anchor="end", size=SMALL, fill=MUTED)
    for index, value in enumerate(week):
        x = left + index * cell
        _text(drawing, days[index], x + cell / 2, top - 36, size=SMALL, fill=MUTED)
        _text(drawing, f"[{index}]", x + cell / 2, top - 10, mono=True, size=SMALL + 1)
        drawing.add(drawing.rect((x, top), (cell - 4, 40), fill=PANEL, stroke=INK, stroke_width=1.3, rx=4))
        _text(drawing, str(value), x + (cell - 4) / 2, top + 26, bold=True)
        _text(drawing, f"[{_minus(index - len(week))}]", x + cell / 2, top + 62, mono=True, size=SMALL + 1)
    return drawing.tostring()


def _labelled_list(drawing, x, y, values, highlight=None, cell=40):
    for index, value in enumerate(values):
        marked = index == highlight
        drawing.add(drawing.rect((x + index * cell, y), (cell, 30),
                                 fill=FILL_AMBER if marked else PANEL, stroke=INK, stroke_width=1.2))
        _text(drawing, str(value), x + index * cell + cell / 2, y + 20, size=SMALL + 1, bold=marked)


def two_labels_one_box() -> str:
    """*A row of numbers*: the "picture in words" of labels on strings, drawn.

    Left, `forecast = week` ties a second label to the one list, so the 16
    shows through both names; right, `.copy()` makes a second list. Both
    sides come from running the page's two cells.
    """
    shared = _run("a-row-of-numbers", "row-two-names-1")
    copied = _run("a-row-of-numbers", "row-two-names-2")
    changed = 6
    if shared["week"] is not shared["forecast"] or copied["week"] is copied["forecast"]:
        raise SystemExit("a-row-of-numbers: the two cells no longer show one list and two lists")

    width, height = 680, 230
    drawing = _drawing(width, height)
    cell = 34

    def tag(x, y, text):
        _box(drawing, x, y, 84, 28, fill=PANEL)
        _text(drawing, text, x + 42, y + 19, mono=True, size=SMALL + 1)

    _text(drawing, "forecast = week", 160, 22, mono=True, size=SMALL + 1)
    tag(16, 60, "week")
    tag(16, 140, "forecast")
    _labelled_list(drawing, 120 + 30, 100, shared["week"], highlight=changed, cell=cell - 6)
    _arrow(drawing, (100, 74), (150, 106))
    _arrow(drawing, (100, 154), (150, 124))
    _text(drawing, "one list, two names", 150 + 7 * (cell - 6) / 2, 158, size=SMALL - 1, fill=MUTED)

    drawing.add(drawing.line((345, 30), (345, 210), stroke=RULE, stroke_width=1))

    _text(drawing, "forecast = week.copy()", 510, 22, mono=True, size=SMALL + 1)
    tag(366, 60, "week")
    tag(366, 140, "forecast")
    _labelled_list(drawing, 470, 60, copied["week"], cell=cell - 6)
    _labelled_list(drawing, 470, 140, copied["forecast"], highlight=changed, cell=cell - 6)
    _arrow(drawing, (450, 74), (470, 74))
    _arrow(drawing, (450, 154), (470, 154))
    _text(drawing, "two lists, one name each", 470 + 7 * (cell - 6) / 2, 196, size=SMALL - 1, fill=MUTED)
    return drawing.tostring()


def adding_two_notes() -> str:
    """*A row of numbers*: two sounds added sample by sample.

    Each sound is drawn as its samples, one stem per index, and the mixed
    sound is the page's element-by-element sum, computed here. One index is
    followed down all three rows, so "the first sample of one to the first
    sample of the other" becomes something to point at.
    """
    low = _assigned("a-row-of-numbers", "row-add-1", "low_note")
    high = _assigned("a-row-of-numbers", "row-add-1", "high_note")
    both = [a + b for a, b in zip(low, high)]
    rows = [("low_note", low), ("high_note", high), ("both_notes", both)]
    biggest = max(abs(v) for _, series in rows for v in series)
    unit = 4.2
    band = 2 * biggest * unit + 26
    left = 130
    step = 60
    width, height = left + len(low) * step + 20, 20 + len(rows) * band + 30
    drawing = _drawing(width, height)
    followed = 1
    for row, (name, series) in enumerate(rows):
        zero = 20 + row * band + band / 2
        _text(drawing, name, left - 20, zero + 5, anchor="end", mono=True, size=SMALL + 1)
        drawing.add(drawing.line((left, zero), (left + len(series) * step - 20, zero),
                                 stroke=RULE, stroke_width=1))
        for index, value in enumerate(series):
            x = left + index * step + 10
            y = zero - value * unit
            drawing.add(drawing.line((x, zero), (x, round(y, 2)), stroke=INK, stroke_width=2))
            drawing.add(drawing.circle((x, round(y, 2)), 5,
                                       fill=FILL_AMBER if index == followed else PANEL,
                                       stroke=INK, stroke_width=1.4))
            _text(drawing, _minus(value), x + 14, y + (5 if value >= 0 else 12), anchor="start",
                  size=SMALL - 1, fill=INK if index == followed else MUTED, bold=index == followed)
    for index in range(len(low)):
        _text(drawing, f"[{index}]", left + index * step + 10, height - 8, mono=True,
              size=SMALL - 1, fill=MUTED)
    x = left + followed * step + 10
    drawing.add(drawing.line((x, 12), (x, height - 24), stroke=MUTED, stroke_width=1,
                             stroke_dasharray="3,4"))
    return drawing.tostring()


def _dot_axis(drawing, left, right, y, low, high, every, unit):
    def x_of(value):
        return left + (value - low) / (high - low) * (right - left)
    drawing.add(drawing.line((left, y), (right, y), stroke=INK, stroke_width=1.2))
    for value in range(low, high + 1, every):
        x = x_of(value)
        drawing.add(drawing.line((round(x, 2), y), (round(x, 2), y + 5), stroke=INK, stroke_width=1))
        _text(drawing, f"{value:,}", x, y + 20, size=SMALL - 1)
    _text(drawing, unit, right, y + 38, anchor="end", size=SMALL - 1, fill=MUTED)
    return x_of


def three_typical_values() -> str:
    """*What is typical?*: the eleven response times, with the three averages on them.

    Nine loads sit in a heap at the left and two slow ones far to the right;
    the mode and the median sit in the heap, and the mean is pulled out
    towards the tail. All three are computed from the page's list with the
    page's definitions (the mode's tie rule included).
    """
    times = _assigned("what-is-typical", "typical-response-1", "response_ms")
    mean = sum(times) / len(times)
    in_order = sorted(times)
    median = in_order[len(in_order) // 2]
    mode = times[0]
    for value in times:
        if times.count(value) > times.count(mode):
            mode = value

    width, height = 680, 250
    drawing = _drawing(width, height)
    left, right, axis_y = 30, 650, 190
    x_of = _dot_axis(drawing, left, right, axis_y, 0, 3500, 500, "milliseconds")
    marks = [("mode", mode, 44), ("median", median, 70), ("mean", mean, 120)]
    for word, value, label_y in marks:
        x = x_of(value)
        drawing.add(drawing.line((round(x, 2), label_y - 4), (round(x, 2), axis_y - 2),
                                 stroke=INK, stroke_width=1.4, stroke_dasharray="4,3"))
        drawing.add(drawing.line((round(x, 2), label_y - 4), (round(x + 22, 2), label_y - 4),
                                 stroke=INK, stroke_width=1.4))
        shown = f"{value:.2f}" if isinstance(value, float) else str(value)
        _text(drawing, f"{word} {shown} ms", x + 26, label_y, anchor="start", size=SMALL + 1, bold=True)
    placed: list[tuple[float, float]] = []
    for value in sorted(times):
        x = x_of(value)
        y = axis_y - 7
        while any(abs(x - px) < 9 and abs(y - py) < 9 for px, py in placed):
            y -= 9.5                     # a dot that would cover another sits on top of it
        placed.append((x, y))
        drawing.add(drawing.circle((round(x, 2), y), 4.5, fill=PANEL, stroke=INK, stroke_width=1.3))
    for value in sorted(times)[-2:]:
        _text(drawing, f"{value:,}", x_of(value), axis_y - 22, size=SMALL - 1, fill=MUTED)
    slow = sorted(times)[-2:]
    drawing.add(drawing.line((round(x_of(slow[0]), 2), axis_y - 44), (round(x_of(slow[-1]), 2), axis_y - 44),
                             stroke=MUTED, stroke_width=1))
    _text(drawing, f"{len(slow)} slow loads: the tail", (x_of(slow[0]) + x_of(slow[-1])) / 2, axis_y - 52,
          size=SMALL, fill=MUTED)
    return drawing.tostring()


def two_connections() -> str:
    """*What is typical?*: the same mean, two very different spreads.

    Each ping is a dot, in the order it arrived, joined to the mean by its
    deviation. The lines are short for A and long for B, which is the spread
    the next sections measure. The pings are the page's own lists.
    """
    connection_a = _assigned("what-is-typical", "typical-spread-1", "connection_a")
    connection_b = _assigned("what-is-typical", "typical-spread-1", "connection_b")
    width, height = 660, 330
    drawing = _drawing(width, height)
    left, right = 60, 640
    for row, (name, pings) in enumerate((("connection A", connection_a), ("connection B", connection_b))):
        top = 20 + row * 150
        axis_y = top + 110
        mean = sum(pings) / len(pings)
        spread = max(pings) - min(pings)
        x_of = _dot_axis(drawing, left, right, axis_y, 0, 110, 10, "ms" if row == 1 else "")
        _text(drawing, f"{name}: mean {mean:g}, range {spread}", left, top + 4, anchor="start",
              size=SMALL + 1, bold=True)
        mx = x_of(mean)
        drawing.add(drawing.line((round(mx, 2), top + 12), (round(mx, 2), axis_y), stroke=INK,
                                 stroke_width=1.4, stroke_dasharray="4,3"))
        for index, ping in enumerate(pings):
            y = top + 20 + index * 12
            drawing.add(drawing.line((round(mx, 2), y), (round(x_of(ping), 2), y), stroke=MUTED,
                                     stroke_width=2))
            drawing.add(drawing.circle((round(x_of(ping), 2), y), 5, fill=FILL_AMBER if row == 0 else FILL_BLUE,
                                       stroke=INK, stroke_width=1.2))
    return drawing.tostring()


# The three circles and where each region's number sits, as the page's own
# drawing cell places them (circles-draw-three), in the same units.
VENN_CENTRES = [(-0.65, 0.45), (0.65, 0.45), (0.0, -0.65)]
VENN_RADIUS = 1.3
VENN_REGIONS = {  # which circles a region is inside -> where its label goes
    (0,): (-1.2, 0.8), (1,): (1.2, 0.8), (2,): (0.0, -1.3),
    (0, 1): (0.0, 1.0), (0, 2): (-0.75, -0.25), (1, 2): (0.75, -0.25),
    (0, 1, 2): (0.0, 0.1),
}


def counted_how_many_times() -> str:
    """*Circles that overlap*: how often each region has been counted, step by step.

    The page follows one laptop from each kind of region through a table.
    Drawn on the circles, the three steps show the middle going from 3 to 0
    and back to 1, which is why the formula ends by adding it back. Each
    number is computed: the circles a region is in, less the pairs of
    circles it is in, plus one if it is in all three.
    """
    for inside, (px, py) in VENN_REGIONS.items():
        found = tuple(i for i, (cx, cy) in enumerate(VENN_CENTRES)
                      if math.hypot(px - cx, py - cy) < VENN_RADIUS)
        if found != inside:
            raise SystemExit(f"a region label at {(px, py)} is not in the region it names")

    steps = [
        ("add the circles", lambda k: k),
        ("take away the pairs", lambda k: k - math.comb(k, 2)),
        ("add back the middle", lambda k: k - math.comb(k, 2) + math.comb(k, 3)),
    ]
    scale = 44
    panel = 226
    width, height = 3 * panel + 10, 262
    drawing = _drawing(width, height)
    for index, (words, count) in enumerate(steps):
        ox = 10 + index * panel + panel / 2
        oy = 132
        for cx, cy in VENN_CENTRES:
            drawing.add(drawing.circle((round(ox + cx * scale, 2), round(oy - cy * scale, 2)),
                                       VENN_RADIUS * scale, fill="none", stroke=INK, stroke_width=1.6))
        for inside, (px, py) in VENN_REGIONS.items():
            value = count(len(inside))
            _text(drawing, str(value), ox + px * scale, oy - py * scale + 6, size=LABEL + 2,
                  bold=value != 1)
            if value != 1:
                drawing.add(drawing.circle((round(ox + px * scale, 2), round(oy - py * scale, 2)), 13,
                                           fill="none", stroke=INK, stroke_width=1.4,
                                           stroke_dasharray="3,2"))
        _text(drawing, f"{index + 1}. {words}", ox, 22, size=SMALL + 1, bold=True)
    _text(drawing, "Each number is how many times that region has been counted so far.",
          width / 2, height - 10, size=SMALL, fill=MUTED)
    return drawing.tostring()


DIAGRAMS = {
    # Unit 1
    "four-questions/ten-plus-four.svg": ten_plus_four,
    "recipes-are-algorithms/names-point-at-values.svg": names_point_at_values,
    "numbers-a-computer-can-hold/seven-segments.svg": seven_segments,
    "everything-is-ones-and-zeros/eight-as-bits.svg": eight_as_bits,
    # Unit 2
    "choosing-a-path/two-rules-on-a-line.svg": two_rules_on_a_line,
    "choosing-a-path/turning-the-line-round.svg": turning_the_line_round,
    "true-false-and-every-case/rows-as-a-tree.svg": rows_as_a_tree,
    "untangling-a-condition/grey-out-grids.svg": grey_out_grids,
    "bits-that-flip/parity-check.svg": parity_check,
    # Unit 3
    "doing-it-again/pairing-the-ends.svg": pairing_the_ends,
    "counting-every-outfit/outfit-tree.svg": outfit_tree,
    "orders-and-choices/song-order-tree.svg": song_order_tree,
    "orders-and-choices/sensor-pairs.svg": sensor_pairs,
    "how-likely-is-it/sum-of-seven.svg": sum_of_seven,
    "chances-that-combine/two-sixes.svg": two_sixes,
    # Unit 4
    "machines-that-take-a-number/one-slot-machine.svg": one_slot_machine,
    "measuring-rooms-and-tins/walls-unfolded.svg": walls_unfolded,
    "measuring-rooms-and-tins/triangle-half-rectangle.svg": triangle_half_rectangle,
    "measuring-rooms-and-tins/circle-into-rectangle.svg": circle_into_rectangle,
    "running-a-formula-backwards/undo-in-reverse.svg": undo_in_reverse,
    "what-a-function-can-see/one-list-two-names.svg": one_list_two_names,
    # Unit 5
    "a-row-of-numbers/indexes-both-ways.svg": indexes_both_ways,
    "a-row-of-numbers/two-labels-one-box.svg": two_labels_one_box,
    "a-row-of-numbers/adding-two-notes.svg": adding_two_notes,
    "what-is-typical/three-typical-values.svg": three_typical_values,
    "what-is-typical/two-connections.svg": two_connections,
    "circles-that-overlap/counted-how-many-times.svg": counted_how_many_times,
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
