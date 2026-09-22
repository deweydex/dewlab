#!/usr/bin/env python3
"""The drawn diagrams for Web Authoring's "A site with several pages" series.

    python3 dev/graphics/web_pages.py          # report what would change
    python3 dev/graphics/web_pages.py --write  # write it

A companion to `web_authoring.py`, whose drawing helpers it borrows, for
the series built on the project starter and the three context pages
beside it. Each picture shows one thing a student cannot see in a
single live preview: where spare space goes, what an empty grid column
looks like, a menu at two widths, a file at two sizes, a form's answers
leaving the page, thirty years of versions, and a circle stored two ways.

Same rule as the other generators: where a picture shows a tutorial's
own example, the words and numbers in it are read from that tutorial's
own cell, so the picture cannot drift from the code a reader runs.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, PAPER, RULE, SANS  # noqa: E402,F401
from web_authoring import (  # noqa: E402
    LABEL_PT, PANEL_GAP, SMALL_PT, TUTORIALS, _caption, _cell, _drawing, _elements, _window,
)


def _number(pattern: str, code: str, slug: str) -> float:
    """The first number a regular expression captures in a cell, or stop."""
    match = re.search(pattern, code)
    if not match:
        raise SystemExit(f"{slug}: the cell no longer matches {pattern!r}")
    return float(match.group(1))


def _arrow(drawing, group, start, end, *, dashed: bool = False) -> None:
    """A straight line with a small filled head at `end`."""
    (x1, y1), (x2, y2) = start, end
    group.add(drawing.line(start=start, end=end, stroke=INK, stroke_width=1.6,
                           stroke_dasharray="5 3" if dashed else None))
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 7
    left = (x2 - size * math.cos(angle - 0.45), y2 - size * math.sin(angle - 0.45))
    right = (x2 - size * math.cos(angle + 0.45), y2 - size * math.sin(angle + 0.45))
    group.add(drawing.polygon([end, left, right], fill=INK))


def spare_space_shared() -> str:
    """The cards example's row, with and without a share of the spare space.

    Drawn to scale at one pixel per pixel, for a row a little wider than
    the cards need. Each card is split into its basis (content, padding
    and border, since the live cells use `content-box`) and, on the
    second row, the share of spare space it grew by, tinted. The first
    row leaves the same spare space empty at the end, so the two rows
    show one quantity: moved, not made.
    """
    slug = "cards-in-a-row"
    html, css = _cell(slug, "cards-html"), _cell(slug, "cards-css")
    names = re.findall(r'<div class="card">([^<]+)</div>', html)
    basis = _number(r"flex:\s*\d+\s+\d+\s+(\d+)px", css, slug)
    padding = _number(r"padding:\s*(\d+)px", css, slug)
    border = _number(r"border:\s*(\d+)px", css, slug)
    gap = _number(r"gap:\s*(\d+)px", css, slug)

    outer = basis + 2 * padding + 2 * border
    row_w, card_h = 640, 46
    spare = row_w - len(names) * outer - (len(names) - 1) * gap
    share = spare / len(names)
    margin = 16
    top = margin + 22
    row_gap = 96
    height = top + row_gap + card_h + 58
    drawing = _drawing(margin * 2 + row_w, height)
    root = drawing.g()

    def row(y: float, grow: bool, title: str) -> None:
        root.add(drawing.text(title, insert=(margin, y - 10),
                              font_size=f"{LABEL_PT}px", font_family=MONO))
        root.add(drawing.rect(insert=(margin, y), size=(row_w, card_h),
                              fill="none", stroke=RULE, stroke_width=1.2, rx=4))
        x = margin
        for name in names:
            root.add(drawing.rect(insert=(x, y), size=(outer, card_h),
                                  fill=PANEL, stroke=INK, stroke_width=1.2, rx=4))
            root.add(drawing.text(name, insert=(x + 10, y + 19), font_size=f"{LABEL_PT}px"))
            root.add(drawing.text(f"basis {basis:.0f}px", insert=(x + 10, y + 36),
                                  font_size=f"{SMALL_PT}px", fill=MUTED))
            if grow:
                root.add(drawing.rect(insert=(x + outer, y + 1), size=(share, card_h - 2),
                                      fill=FILL_AMBER, stroke="none"))
                root.add(drawing.rect(insert=(x, y), size=(outer + share, card_h),
                                      fill="none", stroke=INK, stroke_width=1.2, rx=4))
                root.add(drawing.text("+ share", insert=(x + outer + share / 2, y + 28),
                                      text_anchor="middle", font_size=f"{SMALL_PT}px"))
                x += outer + share + gap
            else:
                x += outer + gap
        if not grow:
            left = x - gap
            root.add(drawing.rect(insert=(left + 4, y + 4), size=(row_w - (left - margin) - 8, card_h - 8),
                                  fill="none", stroke=MUTED, stroke_width=1, stroke_dasharray="4 3", rx=3))
            root.add(drawing.text("spare space, left empty",
                                  insert=(left + (row_w - (left - margin)) / 2, y + 28),
                                  text_anchor="middle", font_size=f"{SMALL_PT}px", fill=MUTED))

    row(top, False, f"flex: 0 0 {basis:.0f}px")
    row(top + row_gap, True, f"flex: 1 1 {basis:.0f}px")
    _caption(drawing, root, margin + row_w / 2, top + row_gap + card_h + 28,
             [("Each card starts at its basis, then grows by an equal share", False),
              ("of the spare space. The spare space is the same size in both rows.", False)])
    drawing.add(root)
    return drawing.tostring()


def auto_fit_and_auto_fill() -> str:
    """Two tiles in a grid with room for four columns, both ways.

    The column sizes come from the gallery cell's own `minmax()` and gap,
    and the width is chosen so that exactly four columns fit. With
    `auto-fill` the two empty tracks are drawn dashed, because they are
    really there; with `auto-fit` they have collapsed, and the two tiles
    have taken their space.
    """
    slug = "a-grid-gallery"
    css = _cell(slug, "gallery-css")
    smallest = _number(r"minmax\((\d+)px", css, slug)
    gap = _number(r"gap:\s*(\d+)px", css, slug)
    columns = 4
    grid_w = columns * smallest + (columns - 1) * gap + 20
    tile_h = 44
    margin = 16
    top = margin + 22
    row_gap = 96
    height = top + row_gap + tile_h + 40
    drawing = _drawing(margin * 2 + grid_w, height)
    root = drawing.g()

    def tile(x: float, y: float, w: float, name: str) -> None:
        root.add(drawing.rect(insert=(x, y), size=(w, tile_h),
                              fill=PANEL, stroke=INK, stroke_width=1.2, rx=4))
        root.add(drawing.text(name, insert=(x + w / 2, y + tile_h / 2 + 5),
                              text_anchor="middle", font_size=f"{LABEL_PT}px"))

    def frame(y: float, word: str) -> None:
        root.add(drawing.text(f"repeat({word}, minmax({smallest:.0f}px, 1fr))",
                              insert=(margin, y - 10), font_size=f"{LABEL_PT}px", font_family=MONO))
        root.add(drawing.rect(insert=(margin - 4, y - 4), size=(grid_w + 8, tile_h + 8),
                              fill="none", stroke=RULE, stroke_width=1.2, rx=5))

    # auto-fill: four real tracks, two of them empty.
    y0 = top
    frame(y0, "auto-fill")
    track = (grid_w - (columns - 1) * gap) / columns
    for index in range(columns):
        x = margin + index * (track + gap)
        if index < 2:
            tile(x, y0, track, str(index + 1))
        else:
            root.add(drawing.rect(insert=(x, y0), size=(track, tile_h), fill="none",
                                  stroke=MUTED, stroke_width=1, stroke_dasharray="4 3", rx=4))
            root.add(drawing.text("empty column", insert=(x + track / 2, y0 + tile_h / 2 + 4),
                                  text_anchor="middle", font_size=f"{SMALL_PT}px", fill=MUTED))

    # auto-fit: the empty tracks collapse; two tiles share the row.
    y1 = top + row_gap
    frame(y1, "auto-fit")
    wide = (grid_w - gap) / 2
    tile(margin, y1, wide, "1")
    tile(margin + wide + gap, y1, wide, "2")

    _caption(drawing, root, margin + grid_w / 2, y1 + tile_h + 30,
             [("Room for four columns, and only two tiles", False)])
    drawing.add(root)
    return drawing.tostring()


def wrap_or_stack() -> str:
    """The phone-navigation example in a narrow window, wrapped and stacked.

    The link and logo words come from the tutorial's own cell. The left
    panel is the alternative the tutorial argues against, the links left
    to wrap (the cell itself never sets `flex-wrap` on the list): two fit
    on a line and the third drops, alone, onto the next. On the right,
    the media query has made both flex containers columns. Widths are
    schematic, chosen so that the wrap leaves exactly one link over.
    """
    slug = "navigation-on-a-phone"
    html = _cell(slug, "phone-nav-html")
    logo = re.search(r'class="logo">([^<]+)<', html).group(1)
    links = [text for text in _elements(html, "a") if text != logo]

    width, view_h = 190, 150
    margin = 16
    top = margin + 14 + 4
    height = top + view_h + 58
    drawing = _drawing(margin * 2 + width * 2 + PANEL_GAP, height)
    root = drawing.g()
    char_w = 7.2
    line_h = 24

    def word(x: float, y: float, text: str, *, bold: bool = False) -> None:
        root.add(drawing.text(text, insert=(x, y), font_size=f"{LABEL_PT}px",
                              font_weight="bold" if bold else "normal"))
        if not bold:
            root.add(drawing.line(start=(x, y + 3), end=(x + len(text) * char_w, y + 3),
                                  stroke=INK, stroke_width=0.8))

    # Wrapped: the logo, then as many links per line as fit.
    x0 = margin
    word(x0 + 12, top + 26, logo, bold=True)
    y = top + 26 + line_h + 6
    x = x0 + 12
    placed_rows: list[list[str]] = [[]]
    for link in links:
        need = len(link) * char_w
        if x + need > x0 + width - 60 and placed_rows[-1]:
            y += line_h
            x = x0 + 12
            placed_rows.append([])
        word(x, y, link)
        placed_rows[-1].append(link)
        x += need + 16
    lone_y = y
    root.add(drawing.rect(insert=(x0 + 6, lone_y - 16), size=(width - 12, 24),
                          fill="none", stroke=MUTED, stroke_width=1, stroke_dasharray="4 3", rx=3))
    root.add(drawing.text("a half-row", insert=(x0 + width - 12, lone_y),
                          text_anchor="end", font_size=f"{SMALL_PT}px", fill=MUTED))
    _window(drawing, root, x0, top, width, view_h)

    # Stacked: the logo on top, then one link per line.
    x1 = margin + width + PANEL_GAP
    word(x1 + 12, top + 26, logo, bold=True)
    for index, link in enumerate(links):
        word(x1 + 12, top + 26 + line_h + 6 + index * line_h, link)
    _window(drawing, root, x1, top, width, view_h)

    base = top + view_h + 26
    _caption(drawing, root, x0 + width / 2, base, [("flex-wrap: wrap", True), ("one link alone on a line", False)])
    _caption(drawing, root, x1 + width / 2, base, [("flex-direction: column", True), ("the same order, one per line", False)])
    drawing.add(root)
    return drawing.tostring()


def twice_as_wide() -> str:
    """A small grid of pixels, and the same picture at twice the width.

    Counted squares, not a photo: the point is the arithmetic, that
    doubling the width doubles the height too, so the number of pixels,
    and roughly the file, grows four times.
    """
    cell = 16
    small_cols, small_rows = 4, 3
    big_cols, big_rows = small_cols * 2, small_rows * 2
    margin = 16
    top = margin + 6
    gap = 90
    small_w, big_w = small_cols * cell, big_cols * cell
    height = top + big_rows * cell + 64
    drawing = _drawing(margin * 2 + small_w + gap + big_w + 40, height)
    root = drawing.g()

    def grid(x: float, y: float, cols: int, rows: int, fill: str) -> None:
        for r in range(rows):
            for c in range(cols):
                root.add(drawing.rect(insert=(x + c * cell, y + r * cell), size=(cell, cell),
                                      fill=fill, stroke=INK, stroke_width=0.8))

    small_x = margin + 20
    small_y = top + (big_rows - small_rows) * cell / 2
    grid(small_x, small_y, small_cols, small_rows, PANEL)
    big_x = small_x + small_w + gap
    grid(big_x, top, big_cols, big_rows, FILL_BLUE)
    _arrow(drawing, root, (small_x + small_w + 14, top + big_rows * cell / 2),
           (big_x - 14, top + big_rows * cell / 2))
    root.add(drawing.text("twice as wide", insert=(small_x + small_w + gap / 2, top + big_rows * cell / 2 - 8),
                          text_anchor="middle", font_size=f"{SMALL_PT}px", fill=MUTED))

    base = top + big_rows * cell + 26
    _caption(drawing, root, small_x + small_w / 2, base,
             [(f"{small_cols} × {small_rows}", True), (f"{small_cols * small_rows} pixels", False)])
    _caption(drawing, root, big_x + big_w / 2, base,
             [(f"{big_cols} × {big_rows}", True),
              (f"{big_cols * big_rows} pixels: four times as many", False)])
    drawing.add(root)
    return drawing.tostring()


def form_sent() -> str:
    """A form's answers leaving the browser for a server, and a reply coming back.

    The pairs on the arrow are the ones the context page's own cell
    prints for its example answers, so the label matches what a reader
    sees when they press the button. The server is drawn as a plain box
    with what it does, because what it is made of does not matter here.
    """
    width, view_h = 180, 150
    margin = 16
    top = margin + 14 + 4
    server_w, server_h = 190, 110
    span = 250
    total_w = margin * 2 + width + span + server_w
    height = top + view_h + 30
    drawing = _drawing(total_w, height)
    root = drawing.g()

    x0 = margin
    # The form inside the browser window.
    for index, name in enumerate(["Name", "Email"]):
        y = top + 16 + index * 44
        root.add(drawing.text(name, insert=(x0 + 14, y + 8), font_size=f"{SMALL_PT}px", font_weight="bold"))
        root.add(drawing.rect(insert=(x0 + 14, y + 13), size=(width - 28, 18),
                              fill=PAPER, stroke=MUTED, stroke_width=1, rx=3))
    root.add(drawing.rect(insert=(x0 + 14, top + 108), size=(56, 24), fill=FILL_BLUE,
                          stroke=INK, stroke_width=1, rx=4))
    root.add(drawing.text("Send", insert=(x0 + 42, top + 124), text_anchor="middle",
                          font_size=f"{SMALL_PT}px"))
    _window(drawing, root, x0, top, width, view_h)

    sx = x0 + width + span
    sy = top + (view_h - server_h) / 2
    root.add(drawing.rect(insert=(sx, sy), size=(server_w, server_h),
                          fill=PANEL, stroke=INK, stroke_width=1.6, rx=6))
    root.add(drawing.text("server", insert=(sx + 12, sy + 22), font_size=f"{LABEL_PT}px", font_weight="bold"))
    for index, line in enumerate(["a program that receives", "the answers. It checks", "every answer again, then",
                                  "stores it or emails it."]):
        root.add(drawing.text(line, insert=(sx + 12, sy + 44 + index * 16), font_size=f"{SMALL_PT}px"))

    out_y = top + 44
    back_y = top + 112
    _arrow(drawing, root, (x0 + width + 10, out_y), (sx - 10, out_y))
    root.add(drawing.text("name=Ana&email=ana%40example.com", insert=(x0 + width + span / 2, out_y - 10),
                          text_anchor="middle", font_size=f"{SMALL_PT}px", font_family=MONO))
    _arrow(drawing, root, (sx - 10, back_y), (x0 + width + 10, back_y))
    root.add(drawing.text("a reply page: “Thank you”", insert=(x0 + width + span / 2, back_y - 10),
                          text_anchor="middle", font_size=f"{SMALL_PT}px"))
    drawing.add(root)
    return drawing.tostring()


# (year, label) — every date here is also stated in the page's own prose.
HTML_EVENTS = [
    (1991, "first HTML"), (1995, "HTML 2.0"), (1997, "HTML 3.2"), (1999, "HTML 4.01"),
    (2004, "WHATWG starts"), (2008, "HTML5 draft"), (2014, "HTML5 standard"), (2019, "one living standard"),
]
CSS_EVENTS = [(1996, "CSS1"), (1998, "CSS2"), (2011, "CSS2.1"), (2017, "Grid in every major browser")]


def timeline() -> str:
    """Thirty years of HTML and CSS on one axis, one lane each.

    Labels alternate above and below their lane, since several events sit
    only a year or two apart. After CSS2.1 the CSS lane turns into a
    tinted band, because from there CSS has no single version to mark:
    the modules move on their own.
    """
    first, last = 1989, 2021
    scale = 22
    margin = 20
    axis_w = (last - first) * scale
    width = margin * 2 + axis_w + 20
    html_y, css_y, axis_y = 78, 190, 262
    height = axis_y + 40
    drawing = _drawing(width, height)
    root = drawing.g()

    def x_of(year: float) -> float:
        return margin + 10 + (year - first) * scale

    root.add(drawing.line(start=(x_of(first), axis_y), end=(x_of(last), axis_y), stroke=INK, stroke_width=1.2))
    for year in range(1990, last + 1, 5):
        root.add(drawing.line(start=(x_of(year), axis_y), end=(x_of(year), axis_y + 5), stroke=INK, stroke_width=1))
        root.add(drawing.text(str(year), insert=(x_of(year), axis_y + 20), text_anchor="middle",
                              font_size=f"{SMALL_PT}px", fill=MUTED))

    def lane(y: float, name: str, events: list[tuple[int, str]]) -> None:
        root.add(drawing.text(name, insert=(margin, y - 34), font_size=f"{LABEL_PT}px", font_weight="bold"))
        root.add(drawing.line(start=(x_of(first), y), end=(x_of(last), y), stroke=RULE, stroke_width=2))
        for index, (year, label) in enumerate(events):
            x = x_of(year)
            above = index % 2 == 0
            root.add(drawing.circle(center=(x, y), r=4.5, fill=INK))
            ty = y - 12 if above else y + 22
            root.add(drawing.line(start=(x, y), end=(x, ty + (4 if above else -12)), stroke=MUTED, stroke_width=0.8))
            root.add(drawing.text(label, insert=(x, ty), text_anchor="middle", font_size=f"{SMALL_PT}px"))

    lane(html_y, "HTML", HTML_EVENTS)
    # CSS after 2.1: a band, not a point.
    root.add(drawing.rect(insert=(x_of(2011), css_y - 7), size=(x_of(last) - x_of(2011), 14),
                          fill=FILL_GREEN, stroke="none", rx=7))
    root.add(drawing.text("separate modules", insert=(x_of(2016), css_y - 12), text_anchor="middle",
                          font_size=f"{SMALL_PT}px", fill=MUTED))
    lane(css_y, "CSS", CSS_EVENTS)
    drawing.add(root)
    return drawing.tostring()


def pixels_and_shapes() -> str:
    """The context page's circle, enlarged, stored as pixels and as a shape.

    The left circle is rasterised here on a coarse grid, a square filled
    wherever its centre falls inside the circle, which is what stretching
    a small bitmap looks like. The right one is the same circle drawn as
    a circle. The radius and centre come from the page's own example.
    """
    page = (TUTORIALS / "image-formats-and-compression" / "image-formats-and-compression.md").read_text()
    match = re.search(r'<circle cx="(\d+)" cy="(\d+)" r="(\d+)"', page)
    if not match:
        raise SystemExit("image-formats-and-compression: no <circle> example any more")
    cx, cy, r = (float(v) for v in match.groups())
    grid_n = int(cx * 2)            # the drawing's own size in its units
    pixel = 2                       # each stored pixel covers 2 units: a 20 x 20 bitmap
    side = 200                      # drawn size of each panel: "shown much bigger"
    unit = side / grid_n
    margin = 16
    top = margin + 4
    height = top + side + 56
    drawing = _drawing(margin * 2 + side * 2 + PANEL_GAP, height)
    root = drawing.g()

    x0 = margin
    for gy in range(0, grid_n, pixel):
        for gx in range(0, grid_n, pixel):
            px, py = gx + pixel / 2, gy + pixel / 2
            if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                root.add(drawing.rect(insert=(x0 + gx * unit, top + gy * unit),
                                      size=(pixel * unit, pixel * unit), fill=FILL_GREEN,
                                      stroke=INK, stroke_width=0.6))
    root.add(drawing.rect(insert=(x0, top), size=(side, side), fill="none", stroke=RULE, stroke_width=1))

    x1 = margin + side + PANEL_GAP
    root.add(drawing.circle(center=(x1 + cx * unit, top + cy * unit), r=r * unit,
                            fill=FILL_GREEN, stroke=INK, stroke_width=1.2))
    root.add(drawing.rect(insert=(x1, top), size=(side, side), fill="none", stroke=RULE, stroke_width=1))

    base = top + side + 26
    _caption(drawing, root, x0 + side / 2, base, [("Stored as pixels", False), ("the edge is a staircase", False)])
    _caption(drawing, root, x1 + side / 2, base, [("Stored as a shape (SVG)", False), ("the edge stays smooth", False)])
    drawing.add(root)
    return drawing.tostring()


DIAGRAMS = {
    "cards-in-a-row/spare-space-shared.svg": spare_space_shared,
    "a-grid-gallery/auto-fit-and-auto-fill.svg": auto_fit_and_auto_fill,
    "navigation-on-a-phone/wrap-or-stack.svg": wrap_or_stack,
    "images-and-file-size/twice-as-wide.svg": twice_as_wide,
    "what-happens-when-a-form-is-sent/form-sent.svg": form_sent,
    "how-html-and-css-got-here/timeline.svg": timeline,
    "image-formats-and-compression/pixels-and-shapes.svg": pixels_and_shapes,
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
