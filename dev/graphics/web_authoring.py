#!/usr/bin/env python3
"""The drawn diagrams Web Authoring's layout pages use, and where each goes.

    python3 dev/graphics/web_authoring.py          # report what would change
    python3 dev/graphics/web_authoring.py --write  # write it

Most of this course's diagrams are built out of HTML and CSS on the page
itself (the `.dl-drawn` family in `assets/tutorial-style.css`), because a
diagram about boxes is best made of boxes. These three are the exceptions:
each one shows a page *moving* — scrolled, or with part of it taken out of
the flow — and a still picture of movement needs two states side by side,
with the part outside the window drawn as well. That is easier to get right
as a drawing than as markup.

Same rule as the other generators here: where a picture shows a tutorial's
own example, the words in it are read from the tutorial's own cell, so the
picture cannot drift from the code a reader runs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import FILL_AMBER, FILL_BLUE, INK, MONO, MUTED, PANEL, PAPER, RULE, SANS  # noqa: E402

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL_PT = 12
SMALL_PT = 10.5
CHROME_H = 14          # the strip across the top of a drawn browser window
PANEL_GAP = 64         # between the two states of one picture


def _cell(slug: str, cell_id: str) -> str:
    """The code of one cell on a tutorial page, header lines removed."""
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    match = re.search(rf"^```\w+ site\nid: {re.escape(cell_id)}\n(.*?)^```", page, re.S | re.M)
    if not match:
        raise SystemExit(f"{slug}: no site cell called {cell_id!r} any more")
    lines = [line for line in match.group(1).splitlines() if not line.startswith("site:")]
    return "\n".join(lines)


def _elements(code: str, tag: str) -> list[str]:
    """The text of every `<tag class=…>text</tag>` in a cell, in order."""
    return [m.group(1).strip() for m in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", code, re.S)]


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _window(drawing, group, x: float, y: float, width: float, height: float,
            *, chrome: bool = True) -> None:
    """A browser window's outline: a thin strip across the top, then the page area.

    `y` is the top of the page area, so the strip sits just above it and
    every coordinate inside the window can be measured from `y` alone.
    Without `chrome`, only the outline: where the page is drawn running
    past the window, a strip across the top would sit on top of the part
    of the page just above it and hide it.
    """
    if not chrome:
        group.add(drawing.rect(
            insert=(x, y), size=(width, height),
            fill="none", stroke=INK, stroke_width=1.8, rx=5))
        return
    group.add(drawing.rect(
        insert=(x, y - CHROME_H), size=(width, CHROME_H),
        fill=PANEL, stroke="none"))
    for index in range(3):
        group.add(drawing.circle(
            center=(x + 9 + index * 9, y - CHROME_H / 2), r=2.4, fill=MUTED))
    group.add(drawing.line(start=(x, y), end=(x + width, y), stroke=INK, stroke_width=1.2))
    group.add(drawing.rect(
        insert=(x, y - CHROME_H), size=(width, height + CHROME_H),
        fill="none", stroke=INK, stroke_width=1.8, rx=5))


def _caption(drawing, group, x: float, y: float, lines: list[tuple[str, bool]]) -> None:
    """One or two centred lines under a panel. `True` sets a line in code type."""
    for index, (text, code) in enumerate(lines):
        group.add(drawing.text(
            text, insert=(x, y + index * 16), text_anchor="middle",
            font_size=f"{LABEL_PT if index == 0 else SMALL_PT}px",
            font_family=MONO if code else SANS,
            fill=INK if index == 0 else MUTED))


def sticky_header_scrolled() -> str:
    """The sticky example at two scroll positions, with the page drawn whole.

    The window is solid and the page runs past it, dashed, above and below:
    what a reader has to see is that the page moved and the header did not,
    and the only way to show a page moving in a still picture is to show the
    part of it the window no longer covers. The header's own slot at the top
    of the page stays drawn in the scrolled state, empty, because sticky
    leaves that space where it was — the difference from `fixed`, which the
    tutorial's table spells out.
    """
    code = _cell("position-and-the-sticky-header", "sticky-html")
    header = _elements(code, "div")[0]
    sections = [text.split(".")[0] for text in _elements(code, "p")]

    width, view_h = 200, 170
    header_h, section_h = 30, 48
    scroll = header_h + section_h               # the header's slot and one section
    margin = 16
    top = margin + scroll                       # page area of both windows starts here
    page_h = header_h + section_h * len(sections)
    below = page_h - view_h                     # page drawn under the first window
    height = top + view_h + below + 84
    drawing = _drawing(margin * 2 + width * 2 + PANEL_GAP, height)
    root = drawing.g()

    clip_ids = []
    for index in range(2):
        x = margin + index * (width + PANEL_GAP)
        clip = drawing.defs.add(drawing.clipPath(id=f"sticky-window-{index}"))
        clip.add(drawing.rect(insert=(x, top), size=(width, view_h)))
        clip_ids.append(clip.get_funciri())

    def page(x: float, page_top: float, *, inside: bool, clip=None, keep_header: bool) -> None:
        group = drawing.g(clip_path=clip) if clip else drawing.g()
        dash = None if inside else "4 3"
        stroke = INK if inside else MUTED
        y = page_top + header_h
        for name in sections:
            group.add(drawing.rect(
                insert=(x + 0.5, y), size=(width - 1, section_h),
                fill=PAPER if inside else "none", stroke=stroke, stroke_width=1,
                stroke_dasharray=dash))
            group.add(drawing.text(
                name, insert=(x + 12, y + 20),
                font_size=f"{LABEL_PT}px", fill=INK if inside else MUTED))
            y += section_h
        if keep_header:
            group.add(drawing.rect(
                insert=(x + 0.5, page_top), size=(width - 1, header_h),
                fill="none" if not inside else PAPER, stroke=MUTED,
                stroke_width=1, stroke_dasharray="4 3"))
            group.add(drawing.text(
                "the header's own place", insert=(x + 12, page_top + header_h / 2 + 4),
                font_size=f"{SMALL_PT}px", fill=MUTED))
        root.add(group)

    def bar(x: float, y: float) -> None:
        root.add(drawing.rect(insert=(x + 1, y), size=(width - 2, header_h), fill=INK))
        root.add(drawing.text(
            header, insert=(x + 12, y + header_h / 2 + 4),
            font_size=f"{LABEL_PT}px", font_weight="bold", fill=PAPER))

    # Before scrolling: the page starts at the top of the window.
    x0 = margin
    page(x0, top, inside=False, keep_header=False)
    page(x0, top, inside=True, clip=clip_ids[0], keep_header=False)
    bar(x0, top)
    _window(drawing, root, x0, top, width, view_h, chrome=False)

    # Scrolled down: the page has moved up; the header is still at the top.
    x1 = margin + width + PANEL_GAP
    page(x1, top - scroll, inside=False, keep_header=True)
    page(x1, top - scroll, inside=True, clip=clip_ids[1], keep_header=False)
    bar(x1, top)
    _window(drawing, root, x1, top, width, view_h, chrome=False)

    base = top + view_h + below + 26
    _caption(drawing, root, x0 + width / 2, base, [("Before we scroll", False)])
    _caption(drawing, root, x1 + width / 2, base,
             [("After we scroll down", False), ("the page moves up, the header stays", False)])
    root.add(drawing.text(
        "Dashed: the parts of the page outside the window.",
        insert=(margin + width + PANEL_GAP / 2, base + 44), text_anchor="middle",
        font_size=f"{SMALL_PT}px", fill=MUTED))
    drawing.add(root)
    return drawing.tostring()


def footer_pushed_down() -> str:
    """The footer example's short page, without and with `margin-top: auto`.

    The empty space is the subject, so it is drawn in both panels: plain
    and unlabelled on the left, where it is only leftover room below the
    footer, and tinted and named on the right, where it has become the
    footer's own margin. That the space is the same size in both is the
    point: `margin-top: auto` moves it, it does not make it.
    """
    code = _cell("footer-at-the-bottom", "footer-push-html")
    paragraph = _elements(code, "p")[0]
    footer = _elements(code, "footer")[0]

    width, view_h = 190, 210
    text_h, footer_h = 32, 30
    margin = 16
    top = margin + CHROME_H + 4
    height = top + view_h + 58
    drawing = _drawing(margin * 2 + width * 2 + PANEL_GAP, height)
    root = drawing.g()

    def text_line(x: float) -> None:
        root.add(drawing.text(
            paragraph, insert=(x + 10, top + text_h / 2 + 5), font_size=f"{LABEL_PT}px"))

    def footer_bar(x: float, y: float) -> None:
        root.add(drawing.rect(insert=(x + 1, y), size=(width - 2, footer_h), fill=INK))
        root.add(drawing.text(
            footer, insert=(x + 10, y + footer_h / 2 + 4),
            font_size=f"{LABEL_PT}px", font_weight="bold", fill=PAPER))

    # Without the auto margin: the footer follows the text.
    x0 = margin
    text_line(x0)
    footer_bar(x0, top + text_h)
    root.add(drawing.text(
        "empty space", insert=(x0 + width / 2, top + text_h + footer_h + (view_h - text_h - footer_h) / 2 + 4),
        text_anchor="middle", font_size=f"{SMALL_PT}px", fill=MUTED))
    _window(drawing, root, x0, top, width, view_h)

    # With it: the same space, now above the footer, is the footer's margin.
    x1 = margin + width + PANEL_GAP
    text_line(x1)
    space_top, space_h = top + text_h, view_h - text_h - footer_h
    root.add(drawing.rect(
        insert=(x1 + 8, space_top + 4), size=(width - 16, space_h - 8),
        fill=FILL_AMBER, stroke=MUTED, stroke_width=1, stroke_dasharray="4 3", rx=3))
    middle = space_top + space_h / 2
    root.add(drawing.text(
        "margin-top: auto", insert=(x1 + width / 2, middle - 3),
        text_anchor="middle", font_size=f"{LABEL_PT}px", font_family=MONO))
    root.add(drawing.text(
        "takes the leftover space", insert=(x1 + width / 2, middle + 14),
        text_anchor="middle", font_size=f"{SMALL_PT}px", fill=INK))
    footer_bar(x1, top + view_h - footer_h)
    _window(drawing, root, x1, top, width, view_h)

    base = top + view_h + 26
    _caption(drawing, root, x0 + width / 2, base, [("Without margin-top: auto", False)])
    _caption(drawing, root, x1 + width / 2, base, [("With margin-top: auto", False)])
    drawing.add(root)
    return drawing.tostring()


def relative_and_absolute() -> str:
    """Three boxes in normal flow, with the middle one moved two ways.

    The one thing to see is what happens to the space the middle box
    leaves. With `relative`, it stays behind, empty, and nothing else
    moves. With `absolute`, it closes up and the third box rises into it.
    The offsets are schematic: the captions name the value, not numbers,
    because the context page describes the idea, not a cell to match.
    """
    width, height_inner = 200, 176
    box_x, box_w, box_h, gap = 12, 150, 34, 22
    margin = 16
    top = margin + 4
    height = top + height_inner + 62
    drawing = _drawing(margin * 2 + width * 2 + PANEL_GAP, height)
    root = drawing.g()

    def frame(x: float) -> None:
        root.add(drawing.rect(
            insert=(x, top), size=(width, height_inner),
            fill="none", stroke=RULE, stroke_width=1.4, rx=4))

    def box(x: float, y: float, name: str, *, moved: bool = False, ghost: bool = False) -> None:
        if ghost:
            root.add(drawing.rect(
                insert=(x, y), size=(box_w, box_h), fill="none",
                stroke=MUTED, stroke_width=1.2, stroke_dasharray="4 3", rx=3))
            root.add(drawing.text(
                name, insert=(x + 8, y + 13), font_size=f"{SMALL_PT}px", fill=MUTED))
            return
        root.add(drawing.rect(
            insert=(x, y), size=(box_w, box_h), fill=FILL_BLUE if moved else PANEL,
            stroke=INK, stroke_width=1.8 if moved else 1.2, rx=3))
        root.add(drawing.text(
            name, insert=(x + box_w / 2, y + box_h / 2 + 4), text_anchor="middle",
            font_size=f"{LABEL_PT}px", font_weight="bold" if moved else "normal"))

    rows = [top + 12 + i * (box_h + gap) for i in range(3)]

    # relative: moved from where it was; its slot stays.
    x0 = margin
    frame(x0)
    box(x0 + box_x, rows[0], "One")
    box(x0 + box_x, rows[1], "its old place, kept", ghost=True)
    box(x0 + box_x, rows[2], "Three")
    box(x0 + box_x + 30, rows[1] + 20, "Two", moved=True)

    # absolute: out of the flow; Three closes the gap.
    x1 = margin + width + PANEL_GAP
    frame(x1)
    box(x1 + box_x, rows[0], "One")
    box(x1 + box_x, rows[1], "Three")
    box(x1 + 36, rows[2], "Two", moved=True)

    base = top + height_inner + 24
    _caption(drawing, root, x0 + width / 2, base,
             [("position: relative", True), ("Two moves; its old space stays", False)])
    _caption(drawing, root, x1 + width / 2, base,
             [("position: absolute", True), ("Two leaves the flow; Three moves up", False)])
    drawing.add(root)
    return drawing.tostring()


DIAGRAMS = {
    "position-and-the-sticky-header/sticky-header-scrolled.svg": sticky_header_scrolled,
    "footer-at-the-bottom/footer-pushed-down.svg": footer_pushed_down,
    "how-a-browser-lays-out-a-page/relative-and-absolute.svg": relative_and_absolute,
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
