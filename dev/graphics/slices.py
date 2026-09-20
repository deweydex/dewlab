"""Draw a sequence, the cuts between its items, and what a slice takes.

Every beginner's off-by-one with `items[2:5]` comes from reading the two
numbers as *items* — so `2` to `5` ought to be four of them, and the end
one ought to be included. Both mistakes go away the moment the numbers
are drawn where they actually are: not on the items but in the gaps
between them, the way fence posts sit between panels. Ten items have
eleven places to cut, and a slice is just the span between two cuts.

So this draws the cut positions along the bottom edge, deliberately
offset from the item indices along the top, and each slice as a span
between two of them. The gap between the two rows of numbers is the
whole lesson.
"""

from __future__ import annotations

import svgwrite

from palette import FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, RULE, SANS

CELL_W = 42
CELL_H = 32
INDEX_PT = 10
VALUE_PT = 12
CUT_PT = 10
SPAN_PT = 11
SPAN_H = 26          # room for one slice's bracket and its label
TOP_LABELS = 16      # the row of item indices above the cells
CUT_ROW = 15         # the row of cut positions below them
BRACKET_DROP = 7     # how far a bracket's end ticks hang

SPAN_FILLS = (FILL_AMBER, FILL_BLUE, FILL_GREEN)


def slicing_cuts(items: list, slices: list[tuple[int | None, int | None]]) -> str:
    """One row of `items`, its cut positions, and a span per slice.

    `slices` holds the (start, stop) pairs exactly as the page writes
    them, `None` standing for an omitted end — so the label can read
    `[:3]` where the page writes `[:3]`, while the bracket is drawn from
    the real cut the omission means. The values under each span are
    sliced from `items` here rather than typed, so a span cannot claim a
    result the same slice would not produce.
    """
    count = len(items)
    row_w = count * CELL_W

    # A span's label starts at the span's right-hand end, so the widest
    # thing on the canvas is a label's *end*, not its length. Measuring
    # the length alone clipped the last slice, whose band finishes at the
    # right edge of the row and whose label then runs past it.
    rightmost = row_w
    for start, stop in slices:
        shown = f"[{'' if start is None else start}:{'' if stop is None else stop}]"
        taken = items[start:stop]
        text = f"{shown} takes {', '.join(str(v) for v in taken)}"
        ends_at = (count if stop is None else stop) * CELL_W - 1
        rightmost = max(rightmost, ends_at + 8 + len(text) * SPAN_PT * 0.55)

    width = rightmost + 8
    height = TOP_LABELS + CELL_H + CUT_ROW + len(slices) * SPAN_H
    margin = 14
    total_w, total_h = width + margin * 2, height + margin * 2

    drawing = svgwrite.Drawing(
        size=(f"{total_w:.0f}px", f"{total_h:.0f}px"),
        viewBox=f"0 0 {total_w:.0f} {total_h:.0f}",
        debug=False)
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    group = drawing.g(transform=f"translate({margin},{margin})")

    # The item indices, centred over each cell.
    for index in range(count):
        group.add(drawing.text(
            str(index), insert=(index * CELL_W + CELL_W / 2, TOP_LABELS - 5),
            text_anchor="middle", font_size=f"{INDEX_PT}px", fill=MUTED))

    # The items themselves.
    for index, value in enumerate(items):
        left = index * CELL_W
        group.add(drawing.rect(
            insert=(left, TOP_LABELS), size=(CELL_W - 2, CELL_H),
            fill=PANEL, stroke=INK, stroke_width=1.2, rx=3))
        group.add(drawing.text(
            str(value), insert=(left + (CELL_W - 2) / 2, TOP_LABELS + CELL_H / 2 + 4),
            text_anchor="middle", font_size=f"{VALUE_PT}px", font_family=MONO, fill=INK))

    # The cuts: one more than there are items, sitting on the boundaries
    # rather than under the cells. A short tick ties each number to the
    # edge it names, so the offset reads as deliberate and not as sloppy
    # alignment.
    cut_y = TOP_LABELS + CELL_H
    for cut in range(count + 1):
        x = cut * CELL_W - 1
        group.add(drawing.line(
            start=(x, cut_y), end=(x, cut_y + 4), stroke=MUTED, stroke_width=1))
        group.add(drawing.text(
            str(cut), insert=(x, cut_y + CUT_ROW),
            text_anchor="middle", font_size=f"{CUT_PT}px",
            font_family=MONO, fill=MUTED))

    # One span per slice, drawn between the two cuts it runs between.
    for row, (start, stop) in enumerate(slices):
        first = 0 if start is None else start
        last = count if stop is None else stop
        top = TOP_LABELS + CELL_H + CUT_ROW + row * SPAN_H + 6
        x1, x2 = first * CELL_W - 1, last * CELL_W - 1
        fill = SPAN_FILLS[row % len(SPAN_FILLS)]

        group.add(drawing.rect(
            insert=(x1, top - 4), size=(x2 - x1, 8), fill=fill, stroke="none", rx=2))
        for x in (x1, x2):
            group.add(drawing.line(
                start=(x, top - BRACKET_DROP), end=(x, top + BRACKET_DROP),
                stroke=INK, stroke_width=1.2))

        shown = f"[{'' if start is None else start}:{'' if stop is None else stop}]"
        taken = items[start:stop]
        group.add(drawing.text(
            f"{shown} takes {', '.join(str(v) for v in taken)}",
            insert=(x2 + 8, top + 4), font_size=f"{SPAN_PT}px", fill=INK))

    drawing.add(group)
    return drawing.tostring()
