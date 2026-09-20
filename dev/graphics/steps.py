"""Draw an algorithm one step at a time, as rows of cells.

A search that halves its range, a walk along two sorted lists — both are
sequences of small states over the same handful of values, and both are
argued about in prose by describing each state in turn. Laying the states
out as rows lets a reader compare them instead of remembering them.
"""

from __future__ import annotations

import svgwrite

from palette import FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, RULE, SANS

CELL_W = 34
CELL_H = 28
ROW_GAP = 16
VALUE_PT = 11.5
NOTE_PT = 11
MARK_PT = 9.5
MARK_H = 13


def binary_search_steps(items: list[int], target: int) -> str:
    """Each pass of a binary search, with the range that is still live.

    What the picture is for is the shrinking: a reader counts the shaded
    cells down the rows and sees the halving that the efficiency claim
    rests on. The `low`, `mid` and `high` marks are underneath so the
    off-by-one the pseudocode invites has somewhere to be checked against.
    """
    passes = []
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        passes.append((low, mid, high))
        if items[mid] == target:
            break
        if target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1

    note_x = len(items) * CELL_W + 16
    width = note_x + 116
    height = len(passes) * (CELL_H + MARK_H + ROW_GAP)
    margin = 14

    drawing = svgwrite.Drawing(
        size=(f"{width + margin * 2:.0f}px", f"{height + margin * 2:.0f}px"),
        viewBox=f"0 0 {width + margin * 2:.0f} {height + margin * 2:.0f}",
        debug=False)
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    group = drawing.g(transform=f"translate({margin},{margin})")

    for row, (low, mid, high) in enumerate(passes):
        top = row * (CELL_H + MARK_H + ROW_GAP)
        for index, value in enumerate(items):
            live = low <= index <= high
            left = index * CELL_W
            group.add(drawing.rect(
                insert=(left, top), size=(CELL_W - 2, CELL_H),
                fill=FILL_AMBER if index == mid else (PANEL if live else "none"),
                stroke=INK if live else RULE,
                stroke_width=1.3 if live else 0.8, rx=3))
            group.add(drawing.text(
                str(value), insert=(left + (CELL_W - 2) / 2, top + CELL_H / 2 + 4),
                text_anchor="middle", font_size=f"{VALUE_PT}px",
                font_family=MONO, fill=INK if live else MUTED))
        # By the last pass all three marks land on the same cell, and three
        # labels drawn at one position overlap into something unreadable.
        # Grouped by cell, they read as what they are: the range has closed
        # to a single item, which is where the search ends.
        together: dict[int, list[str]] = {}
        for index, name in ((low, "low"), (mid, "mid"), (high, "high")):
            together.setdefault(index, []).append(name)
        for index, names in together.items():
            group.add(drawing.text(
                " ".join(names),
                insert=(index * CELL_W + (CELL_W - 2) / 2, top + CELL_H + 11),
                text_anchor="middle", font_size=f"{MARK_PT}px", fill=MUTED))
        remaining = high - low + 1
        found = items[mid] == target
        note = f"found {target}" if found else f"{remaining} left, then {remaining // 2}"
        group.add(drawing.text(
            note, insert=(note_x, top + CELL_H / 2 + 4),
            font_size=f"{NOTE_PT}px", fill=INK if found else MUTED))

    drawing.add(group)
    return drawing.tostring()
