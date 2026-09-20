"""Draw grids of numbers, with one row and one column picked out.

For the moment when a reader meets $c_{ij} = \\sum_k a_{ik} b_{kj}$. The
formula is exact and hard to read cold; the picture says the same thing by
showing which row and which column produce which single entry, and writing
the products underneath.

Everything is a box with a number in it, so this is svgwrite rather than
matplotlib: there are no axes, no scale, and nothing to plot. The colours
are theme tokens written straight in, which means no normalising pass.
"""

from __future__ import annotations

import svgwrite

from palette import FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, SANS

CELL = 38
GAP = 4
LABEL_PT = 13
CELL_PT = 13
NOTE_PT = 11.5
BETWEEN = 58            # between one grid and the next


def _grid_width(matrix) -> float:
    return len(matrix[0]) * CELL + (len(matrix[0]) - 1) * GAP


def _grid_height(matrix) -> float:
    return len(matrix) * CELL + (len(matrix) - 1) * GAP


def _draw_grid(drawing, group, matrix, x, y, name, *,
               row=None, column=None, cell=None) -> None:
    """One grid. `row`, `column` and `cell` are what gets picked out."""
    group.add(drawing.text(
        name, insert=(x + _grid_width(matrix) / 2, y - 12), text_anchor="middle",
        font_size=f"{LABEL_PT}px", font_style="italic", fill=MUTED))
    for r, values in enumerate(matrix):
        for c, value in enumerate(values):
            fill = PANEL
            if cell == (r, c):
                fill = FILL_AMBER
            elif row is not None and r == row:
                fill = FILL_GREEN
            elif column is not None and c == column:
                fill = FILL_BLUE
            left, top = x + c * (CELL + GAP), y + r * (CELL + GAP)
            group.add(drawing.rect(
                insert=(left, top), size=(CELL, CELL),
                fill=fill, stroke=INK, stroke_width=1.3, rx=4))
            group.add(drawing.text(
                str(value), insert=(left + CELL / 2, top + CELL / 2 + 5),
                text_anchor="middle", font_size=f"{CELL_PT}px",
                font_family=MONO, fill=INK))


def row_times_column(left_matrix, right_matrix, result, row: int, column: int,
                     names=("A", "B", "AB")) -> str:
    """The two grids, the result, and the one entry the picked row and
    column produce — with the products spelled out beneath."""
    products = [
        f"{left_matrix[row][k]}×{right_matrix[k][column]}"
        for k in range(len(right_matrix))
    ]
    working = " + ".join(products) + f" = {result[row][column]}"

    widths = [_grid_width(m) for m in (left_matrix, right_matrix, result)]
    margin, top = 18, 34
    width = sum(widths) + BETWEEN * 2 + margin * 2
    height = top + max(_grid_height(m) for m in
                       (left_matrix, right_matrix, result)) + 42 + margin

    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}", debug=False)
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    group = drawing.g(transform=f"translate({margin},{top})")

    x = 0.0
    _draw_grid(drawing, group, left_matrix, x, 0, names[0], row=row)
    x += widths[0] + BETWEEN
    group.add(drawing.text(
        "×", insert=(x - BETWEEN / 2, _grid_height(left_matrix) / 2 + 6),
        text_anchor="middle", font_size="17px", fill=MUTED))
    _draw_grid(drawing, group, right_matrix, x, 0, names[1], column=column)
    x += widths[1] + BETWEEN
    group.add(drawing.text(
        "=", insert=(x - BETWEEN / 2, _grid_height(right_matrix) / 2 + 6),
        text_anchor="middle", font_size="17px", fill=MUTED))
    _draw_grid(drawing, group, result, x, 0, names[2], cell=(row, column))

    group.add(drawing.text(
        working,
        insert=((width - margin * 2) / 2, max(_grid_height(m) for m in
                (left_matrix, right_matrix, result)) + 30),
        text_anchor="middle", font_size=f"{NOTE_PT}px", font_family=MONO, fill=INK))

    drawing.add(group)
    return drawing.tostring()
