#!/usr/bin/env python3
"""The drawn diagrams Web Authoring's responsive-layout pages use, and where each goes.

    python3 dev/graphics/web_responsive.py          # report what would change
    python3 dev/graphics/web_responsive.py --write  # write it

The pages are media-queries, flexbox-first-steps and order-on-screen, and the
two context pages beside them, designing-for-many-screens and flexbox-or-grid.
Same approach as `web_authoring.py`, whose helpers this borrows: each picture
shows something a cell does across widths, or across two ways of reading one
page, which is easier to hold still as a drawing than as markup.

Where a picture shows a tutorial's own example, its numbers and words are read
from that tutorial's own cell, so the picture cannot drift from the code a
reader runs. The flex picture works out where each card goes from the cell's
own `flex`, `padding`, `border` and `gap` — the same sum the page does by hand,
and one that was checked against Chromium's layout when this was written.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, RULE  # noqa: E402
from web_authoring import LABEL_PT, SMALL_PT, TUTORIALS, _caption, _cell, _drawing, _elements  # noqa: E402

PANEL_GAP = 56


def _px(code: str, pattern: str) -> int:
    """The first whole number of pixels a pattern captures in a cell."""
    match = re.search(pattern, code)
    if not match:
        raise SystemExit(f"no match for {pattern!r} in a cell this diagram reads")
    return int(match.group(1))


def _arrow(drawing, group, start, end, *, colour=INK, width=1.4) -> None:
    """A straight line with a small filled head at `end`."""
    (x1, y1), (x2, y2) = start, end
    group.add(drawing.line(start=start, end=end, stroke=colour, stroke_width=width))
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 or 1
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    head = [(x2, y2), (x2 - 7 * ux + 3.5 * uy, y2 - 7 * uy - 3.5 * ux),
            (x2 - 7 * ux - 3.5 * uy, y2 - 7 * uy + 3.5 * ux)]
    group.add(drawing.polygon(points=head, fill=colour))


def media_query_ranges() -> str:
    """The two width conditions as two bands on one line of widths.

    The breakpoint is read from the tutorial's cell. `max-width` is drawn
    above the line and reaches left to 0; `min-width` is drawn below and
    runs to the right-hand end, where the line's arrow says it goes on.
    """
    code = _cell("media-queries", "media-css")
    breakpoint = _px(code, r"max-width:\s*(\d+)px")

    top_px, scale = 600, 0.9
    left = 30
    band_h = 30
    max_y = 44                      # top of the max-width band
    axis_y = max_y + band_h + 20
    min_y = axis_y + 30             # top of the min-width band, under the tick labels
    width = left * 2 + top_px * scale + 20
    height = min_y + band_h + 58
    drawing = _drawing(width, height)
    root = drawing.g()

    def x(px: float) -> float:
        return left + px * scale

    # max-width: from 0 up to the breakpoint, above the line.
    root.add(drawing.text(f"applies at {breakpoint}px or narrower", insert=(x(0), max_y - 8),
                          font_size=f"{SMALL_PT}px", fill=MUTED))
    root.add(drawing.rect(insert=(x(0), max_y), size=(x(breakpoint) - x(0), band_h),
                          fill=FILL_AMBER, stroke=INK, stroke_width=1, rx=3))
    root.add(drawing.text(f"max-width: {breakpoint}px", insert=(x(0) + 10, max_y + band_h / 2 + 4),
                          font_size=f"{LABEL_PT}px", font_family=MONO))

    # The line of widths, with ticks and numbers every 100px.
    _arrow(drawing, root, (x(0), axis_y), (x(top_px) + 16, axis_y))
    for px in range(0, top_px + 1, 100):
        root.add(drawing.line(start=(x(px), axis_y - 4), end=(x(px), axis_y + 4), stroke=INK, stroke_width=1))
        root.add(drawing.text(f"{px}", insert=(x(px), axis_y + 18), text_anchor="middle",
                              font_size=f"{SMALL_PT}px", fill=MUTED))

    # min-width: from the breakpoint up, below the line.
    root.add(drawing.rect(insert=(x(breakpoint), min_y), size=(x(top_px) + 16 - x(breakpoint), band_h),
                          fill=FILL_BLUE, stroke=INK, stroke_width=1, rx=3))
    root.add(drawing.text(f"min-width: {breakpoint}px", insert=(x(breakpoint) + 10, min_y + band_h / 2 + 4),
                          font_size=f"{LABEL_PT}px", font_family=MONO))
    root.add(drawing.text(f"applies at {breakpoint}px or wider", insert=(x(breakpoint) + 10, min_y + band_h + 16),
                          font_size=f"{SMALL_PT}px", fill=MUTED))
    root.add(drawing.text("viewport width, in pixels", insert=(x(0), min_y + band_h / 2 + 4),
                          font_size=f"{SMALL_PT}px", fill=MUTED))

    # The breakpoint itself.
    root.add(drawing.line(start=(x(breakpoint), max_y - 4), end=(x(breakpoint), min_y + band_h + 4),
                          stroke=INK, stroke_width=2, stroke_dasharray="4 3"))
    root.add(drawing.text(f"breakpoint: {breakpoint}px", insert=(x(breakpoint) + 8, max_y - 8),
                          font_size=f"{LABEL_PT}px", font_weight="bold"))
    drawing.add(root)
    return drawing.tostring()


def _flex_lines(total: float, basis: float, gap: float, count: int) -> list[list[float]]:
    """Where each flex item goes in a wrapping row that lets items grow.

    Items are placed at their full starting size (content, padding and
    border) until the next one would not fit; then each line shares its
    spare space out evenly. Returns, for each line, the items' widths.
    """
    lines, current = [], []
    for _ in range(count):
        if current and basis * (len(current) + 1) + gap * len(current) > total:
            lines.append(current)
            current = []
        current.append(basis)
    lines.append(current)
    grown = []
    for line in lines:
        spare = total - basis * len(line) - gap * (len(line) - 1)
        grown.append([basis + spare / len(line)] * len(line))
    return grown


def flex_row_wraps() -> str:
    """The flexbox-first-steps cards at three widths: roomy, exact, too narrow.

    The exact width is worked out from the cell, not typed in, so if the
    card's padding or basis changes the middle row still shows the width
    at which three cards just fit.
    """
    code = _cell("flexbox-first-steps", "cards-css")
    names = re.findall(r'<div class="card">(.*?)</div>', _cell("flexbox-first-steps", "cards-html"))
    basis = _px(code, r"flex:\s*1 1 (\d+)px")
    padding = _px(code, r"\.card\s*{[^}]*padding:\s*(\d+)px")
    border = _px(code, r"\.card\s*{[^}]*border:\s*(\d+)px")
    gap = _px(code, r"gap:\s*(\d+)px")
    card = basis + 2 * padding + 2 * border
    exact = 3 * card + 2 * gap
    widths = [exact + 54, exact, exact - 26]

    scale, card_h, line_gap = 1.0, 34, 8
    margin, label_w = 16, 132
    row_h = 2 * card_h + line_gap + 30
    width = margin * 2 + label_w + widths[0] * scale
    height = margin + row_h * len(widths)
    drawing = _drawing(width, height)
    root = drawing.g()

    for index, total in enumerate(widths):
        top = margin + index * row_h
        x0 = margin + label_w
        root.add(drawing.text(f"{total}px", insert=(margin, top + card_h / 2 + 5),
                              font_size=f"{LABEL_PT}px", font_family=MONO, font_weight="bold"))
        note = ["room to spare", "three just fit", "too narrow for three"][index]
        root.add(drawing.text(note, insert=(margin, top + card_h / 2 + 21),
                              font_size=f"{SMALL_PT}px", fill=MUTED))
        root.add(drawing.rect(insert=(x0, top - 4), size=(total * scale, 2 * card_h + line_gap + 8),
                              fill="none", stroke=RULE, stroke_width=1, stroke_dasharray="3 3"))
        item = 0
        for line_no, line in enumerate(_flex_lines(total, card, gap, len(names))):
            x = x0
            y = top + line_no * (card_h + line_gap)
            for item_w in line:
                root.add(drawing.rect(insert=(x, y), size=(item_w * scale, card_h),
                                      fill=PANEL, stroke=INK, stroke_width=1, rx=4))
                root.add(drawing.text(names[item], insert=(x + item_w * scale / 2, y + card_h / 2 - 1),
                                      text_anchor="middle", font_size=f"{SMALL_PT}px"))
                root.add(drawing.text(f"{item_w:.0f}px", insert=(x + item_w * scale / 2, y + card_h / 2 + 12),
                                      text_anchor="middle", font_size=f"{SMALL_PT}px", fill=MUTED,
                                      font_family=MONO))
                x += (item_w + gap) * scale
                item += 1
    drawing.add(root)
    return drawing.tostring()


def order_and_tab() -> str:
    """Source order on the left, screen order on the right, and the Tab path over it.

    The link names come from the cell's HTML, and the one that moves is the
    one the cell's CSS gives `order: -1`. Tab is numbered over the screen
    row in source order, so the third arrow visibly runs back to the left.
    """
    html = _cell("order-on-screen", "order-html")
    css = _cell("order-on-screen", "order-css")
    names = _elements(html, "a")
    moved_class = re.search(r"\.(\w+)\s*{\s*order:\s*-1;", css).group(1)
    classes = re.findall(r'class="item (\w+)"', html)
    moved = names[classes.index(moved_class)]
    screen = [moved] + [name for name in names if name != moved]

    margin = 16
    list_w, row_gap = 150, 12
    box_w, box_h = 96, 36
    row_w = len(names) * box_w + (len(names) - 1) * row_gap
    left_x = margin
    right_x = margin + list_w + PANEL_GAP
    top = margin + 26
    width = right_x + row_w + margin
    height = top + 176
    drawing = _drawing(width, height)
    root = drawing.g()

    # Source order: a numbered list, the way the HTML reads.
    root.add(drawing.text("In the HTML", insert=(left_x, margin + 8),
                          font_size=f"{LABEL_PT}px", font_weight="bold"))
    for index, name in enumerate(names):
        y = top + index * (box_h + 8)
        root.add(drawing.rect(insert=(left_x, y), size=(list_w, box_h), fill=PANEL, stroke=INK,
                              stroke_width=1, rx=4))
        root.add(drawing.text(f"{index + 1}  {name}", insert=(left_x + 12, y + box_h / 2 + 4),
                              font_size=f"{LABEL_PT}px"))

    # Screen order: the row as drawn, with the moved link tinted.
    row_y = top + 76
    root.add(drawing.text("On screen", insert=(right_x, margin + 8),
                          font_size=f"{LABEL_PT}px", font_weight="bold"))
    centres = {}
    for index, name in enumerate(screen):
        x = right_x + index * (box_w + row_gap)
        root.add(drawing.rect(insert=(x, row_y), size=(box_w, box_h),
                              fill=FILL_AMBER if name == moved else PANEL,
                              stroke=INK, stroke_width=1.6 if name == moved else 1, rx=4))
        root.add(drawing.text(name, insert=(x + box_w / 2, row_y + box_h / 2 + 4), text_anchor="middle",
                              font_size=f"{LABEL_PT}px"))
        centres[name] = x + box_w / 2
    root.add(drawing.text("order: -1", insert=(centres[moved], row_y + box_h + 16), text_anchor="middle",
                          font_size=f"{SMALL_PT}px", font_family=MONO, fill=MUTED))

    # The Tab path: numbered in source order, above the row.
    badge_y = row_y - 26
    for index, name in enumerate(names):
        cx = centres[name]
        root.add(drawing.circle(center=(cx, badge_y), r=10, fill=FILL_GREEN, stroke=INK, stroke_width=1))
        root.add(drawing.text(f"{index + 1}", insert=(cx, badge_y + 4), text_anchor="middle",
                              font_size=f"{SMALL_PT}px", font_weight="bold"))
    for a, b in zip(names, names[1:]):
        start, end = centres[a], centres[b]
        if end > start:
            _arrow(drawing, root, (start + 12, badge_y), (end - 12, badge_y))
        else:
            # Back to the left: an arc over the top of the badges.
            lift = badge_y - 44
            root.add(drawing.path(d=f"M {start} {badge_y - 10} C {start} {lift} {end} {lift} {end} {badge_y - 16}",
                                  fill="none", stroke=INK, stroke_width=1.4, stroke_dasharray="5 3"))
            _arrow(drawing, root, (end, badge_y - 18), (end, badge_y - 11))
    _caption(drawing, root, right_x + row_w / 2, height - 14,
             [("Tab follows the HTML, not the screen", False)])
    drawing.add(root)
    return drawing.tostring()


def viewport_meta() -> str:
    """One page on one phone, laid out two ways.

    Without the viewport line the phone lays the page out as if its screen
    were about 980px wide and shrinks the result, so everything is tiny.
    With it, the page is laid out at the phone's own width. The lines of
    "text" are bars: the point is their size, not their words.
    """
    phone_w, phone_h = 150, 260
    margin = 16
    top = margin
    width = margin * 2 + phone_w * 2 + PANEL_GAP * 2
    height = top + phone_h + 66
    drawing = _drawing(width, height)
    root = drawing.g()

    def phone(x: float) -> tuple[float, float, float, float]:
        root.add(drawing.rect(insert=(x, top), size=(phone_w, phone_h), fill="none",
                              stroke=INK, stroke_width=2, rx=16))
        sx, sy, sw, sh = x + 8, top + 22, phone_w - 16, phone_h - 44
        root.add(drawing.rect(insert=(sx, sy), size=(sw, sh), fill="none", stroke=RULE, stroke_width=1))
        root.add(drawing.line(start=(x + phone_w / 2 - 14, top + 11), end=(x + phone_w / 2 + 14, top + 11),
                              stroke=MUTED, stroke_width=3, stroke_linecap="round"))
        return sx, sy, sw, sh

    # Without: a wide page shrunk. Header bar, three columns, tiny lines.
    x0 = margin + PANEL_GAP / 2
    sx, sy, sw, sh = phone(x0)
    shrink = 0.3
    root.add(drawing.rect(insert=(sx, sy), size=(sw, 20 * shrink * 2), fill=PANEL))
    col_w = (sw - 8) / 3
    for col in range(3):
        cx = sx + 2 + col * (col_w + 2)
        for line in range(9):
            root.add(drawing.rect(insert=(cx + 2, sy + 18 + line * 5), size=(col_w - 6 - (line % 3) * 3, 2),
                                  fill=MUTED))
    root.add(drawing.text("tiny text", insert=(sx + sw / 2, sy + sh - 12), text_anchor="middle",
                          font_size=f"{SMALL_PT}px", fill=MUTED))

    # With: the same page at the phone's own width, one column, readable lines.
    x1 = x0 + phone_w + PANEL_GAP
    sx, sy, sw, sh = phone(x1)
    root.add(drawing.rect(insert=(sx, sy), size=(sw, 22), fill=PANEL))
    root.add(drawing.text("My Portfolio", insert=(sx + 8, sy + 15), font_size=f"{SMALL_PT}px",
                          font_weight="bold"))
    for line in range(8):
        root.add(drawing.rect(insert=(sx + 8, sy + 36 + line * 16), size=(sw - 16 - (line % 3) * 14, 6),
                              fill=MUTED))

    base = top + phone_h + 22
    _caption(drawing, root, x0 + phone_w / 2, base,
             [("Without the viewport line", False), ("laid out about 980px wide, then shrunk", False)])
    _caption(drawing, root, x1 + phone_w / 2, base,
             [("With it", False), ("laid out at the phone's own width", False)])
    drawing.add(root)
    return drawing.tostring()


def flex_or_grid() -> str:
    """Five items in a wrapping flex row and in a three-column grid.

    Same five items, same width, same gap. The first row looks the same in
    both. The difference is the last row: flex shares that row's space
    between its own two items, grid keeps them in the columns above and
    leaves the third cell empty. The context page's live cell shows it;
    this holds the two side by side.
    """
    code = _cell("flexbox-or-grid", "flex-or-grid-css")
    gap = _px(code, r"gap:\s*(\d+)px")
    html = _cell("flexbox-or-grid", "flex-or-grid-html")
    count = len(re.findall(r"<div>\d+</div>", html.split('class="grid"')[0]))

    panel_w, item_h = 240, 34
    margin = 16
    top = margin + 22
    width = margin * 2 + panel_w * 2 + PANEL_GAP
    height = top + 2 * item_h + gap + 70
    drawing = _drawing(width, height)
    root = drawing.g()

    def item(x, y, w, n, *, empty=False):
        if empty:
            root.add(drawing.rect(insert=(x, y), size=(w, item_h), fill="none", stroke=MUTED,
                                  stroke_width=1, stroke_dasharray="4 3", rx=4))
            return
        root.add(drawing.rect(insert=(x, y), size=(w, item_h), fill=PANEL, stroke=INK, stroke_width=1, rx=4))
        root.add(drawing.text(str(n), insert=(x + w / 2, y + item_h / 2 + 4), text_anchor="middle",
                              font_size=f"{LABEL_PT}px"))

    per_row = 3
    cell = (panel_w - gap * (per_row - 1)) / per_row

    # Flex: the second row shares its own width between two items.
    x0 = margin
    root.add(drawing.text("display: flex; flex-wrap: wrap", insert=(x0, margin + 8),
                          font_size=f"{SMALL_PT}px", font_family=MONO))
    n = 1
    for row_start in range(0, count, per_row):
        in_row = min(per_row, count - row_start)
        w = (panel_w - gap * (in_row - 1)) / in_row
        for k in range(in_row):
            item(x0 + k * (w + gap), top + (row_start // per_row) * (item_h + gap), w, n)
            n += 1

    # Grid: every row uses the same three columns.
    x1 = margin + panel_w + PANEL_GAP
    root.add(drawing.text("display: grid; 3 columns", insert=(x1, margin + 8),
                          font_size=f"{SMALL_PT}px", font_family=MONO))
    for k in range(per_row * 2):
        row, col = divmod(k, per_row)
        item(x1 + col * (cell + gap), top + row * (item_h + gap), cell, k + 1, empty=k >= count)

    base = top + 2 * item_h + gap + 28
    _caption(drawing, root, x0 + panel_w / 2, base,
             [("Flexbox", False), ("each row shares out its own space", False)])
    _caption(drawing, root, x1 + panel_w / 2, base,
             [("Grid", False), ("the columns line up in every row", False)])
    drawing.add(root)
    return drawing.tostring()


DIAGRAMS = {
    "media-queries/media-query-ranges.svg": media_query_ranges,
    "flexbox-first-steps/flex-row-wraps.svg": flex_row_wraps,
    "order-on-screen/order-and-tab.svg": order_and_tab,
    "designing-for-many-screens/viewport-meta.svg": viewport_meta,
    "flexbox-or-grid/flex-or-grid.svg": flex_or_grid,
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
