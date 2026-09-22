#!/usr/bin/env python3
"""The drawn diagrams Web Authoring's interaction pages use, and where each goes.

    python3 dev/graphics/web_interaction.py          # report what would change
    python3 dev/graphics/web_interaction.py --write  # write it

The pages on hover and focus, transforms, keyframes and the checkbox hack,
and their context page. Each picture here shows something a live cell cannot
show on its own: a box's kept space next to where it is drawn, the frames
between two keyframes, which later siblings a `~` rule reaches, and the order
Tab visits a whole page in.

Same rule as web_authoring.py: where a picture shows a tutorial's own
example, the words and numbers in it are read from the tutorial's own cell,
so the picture cannot drift from the code a reader runs. The tab-order
picture shows the student's starter site, which lives outside this
repository, so its link texts are written out here and say where they came
from.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (  # noqa: E402
    FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, PAPER, RULE, SANS,
)

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL_PT = 12
SMALL_PT = 10.5
MARGIN = 16


def _cell(slug: str, cell_id: str) -> str:
    """The code of one cell on a tutorial page, header lines removed."""
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    match = re.search(rf"^```\w+ site\nid: {re.escape(cell_id)}\n(.*?)^```", page, re.S | re.M)
    if not match:
        raise SystemExit(f"{slug}: no site cell called {cell_id!r} any more")
    lines = [line for line in match.group(1).splitlines() if not line.startswith("site:")]
    return "\n".join(lines)


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _text(drawing, group, text, x, y, *, size=LABEL_PT, anchor="start", mono=False,
          fill=INK, bold=False):
    group.add(drawing.text(
        text, insert=(x, y), text_anchor=anchor, font_size=f"{size}px",
        font_family=MONO if mono else SANS, fill=fill,
        font_weight="bold" if bold else "normal"))


def _arrowhead(drawing, marker_id: str):
    marker = drawing.marker(id=marker_id, insert=(6, 3.5), size=(7, 7), orient="auto")
    marker.add(drawing.path(d="M0,0 L7,3.5 L0,7 z", fill=INK))
    drawing.defs.add(marker)
    return marker.get_funciri()


def transform_keeps_its_space() -> str:
    """The three transform boxes, plain, then with the middle one scaled.

    Step 3 of the tutorial asks the reader to try `scale(2)` on the middle
    box and look at the gaps. The picture is that moment: the middle box
    drawn twice as big over its neighbours, with its own kept space dashed
    underneath, and the neighbours exactly where they were in the row above.
    The other two boxes' own transforms are left out, so the only change
    between the rows is the one the caption names.
    """
    code = _cell("transitions-and-transforms", "transforms-html")
    classes = re.findall(r'class="box (\w+)"', code)
    box_w, box_h, gap = 96, 40, 20
    row_w = box_w * 3 + gap * 2
    width = MARGIN * 2 + row_w + 40
    left = MARGIN + 20
    top_row, bottom_row = 40, 176
    height = bottom_row + box_h + 96
    drawing = _drawing(width, height)
    root = drawing.g()

    def box(x, y, name, *, w=box_w, h=box_h, fill=PANEL, stroke=INK, dash=None, text_fill=INK):
        root.add(drawing.rect(insert=(x, y), size=(w, h), fill=fill, stroke=stroke,
                              stroke_width=1.4, stroke_dasharray=dash))
        _text(drawing, root, f".{name}", x + w / 2, y + h / 2 + 4, anchor="middle",
              mono=True, fill=text_fill)

    _text(drawing, root, "No transform", left, top_row - 14, size=SMALL_PT, fill=MUTED)
    for index, name in enumerate(classes):
        box(left + index * (box_w + gap), top_row, name)

    _text(drawing, root, "The middle box with transform: scale(2)", left, bottom_row - 44,
          size=SMALL_PT, fill=MUTED)
    first, middle, third = (left + i * (box_w + gap) for i in range(3))
    box(first, bottom_row, classes[0])
    box(third, bottom_row, classes[2])
    # The drawn box: twice the size, grown out from the centre of its space.
    cx, cy = middle + box_w / 2, bottom_row + box_h / 2
    root.add(drawing.rect(insert=(cx - box_w, cy - box_h), size=(box_w * 2, box_h * 2),
                          fill=FILL_BLUE, stroke=INK, stroke_width=1.8, fill_opacity=0.8))
    _text(drawing, root, f".{classes[1]}", cx, cy - box_h / 2 - 4, anchor="middle",
          mono=True, bold=True)
    # Its kept space, on top so it stays visible through the grown box.
    root.add(drawing.rect(insert=(middle, bottom_row), size=(box_w, box_h), fill="none",
                          stroke=INK, stroke_width=1.4, stroke_dasharray="5 3"))

    base = bottom_row + box_h + box_h / 2 + 30
    _text(drawing, root, "Dashed: the middle box's own space, which the page keeps.",
          width / 2, base, anchor="middle", size=SMALL_PT, fill=MUTED)
    _text(drawing, root, "The boxes on either side do not move.",
          width / 2, base + 16, anchor="middle", size=SMALL_PT, fill=MUTED)
    drawing.add(root)
    return drawing.tostring()


def pulse_on_a_timeline() -> str:
    """One pass of the pulse, with its three keyframes on a line of time.

    The stages, the duration and the values are all read from the cell. The
    buttons are drawn at their real scale and opacity, so the change is as
    small here as it is on screen, and the numbers under each one say what
    changed. The ticks between the keyframes are the point: many frames,
    none of them written by us.
    """
    css = _cell("keyframes-and-the-checkbox-hack", "pulse-css")
    html = _cell("keyframes-and-the-checkbox-hack", "pulse-html")
    label = re.search(r">(.*?)<", html).group(1)
    duration = float(re.search(r"animation:\s*\w+\s+([\d.]+)s", css).group(1))
    stages = []
    for block in re.finditer(r"([\d%, ]+)\{\s*transform:\s*scale\(([\d.]+)\);\s*opacity:\s*([\d.]+);", css):
        for stop in block.group(1).split(","):
            stages.append((int(stop.strip().rstrip("%")), float(block.group(2)), float(block.group(3))))
    stages.sort()

    axis_w = 440
    width = MARGIN * 2 + axis_w + 160
    x0 = MARGIN + 80
    axis_y = 128
    height = axis_y + 100
    drawing = _drawing(width, height)
    root = drawing.g()

    btn_w, btn_h = 84, 30
    for percent, scale, opacity in stages:
        x = x0 + axis_w * percent / 100
        w, h = btn_w * scale, btn_h * scale
        root.add(drawing.rect(insert=(x - w / 2, 60 - h / 2), size=(w, h), rx=5 * scale,
                              fill=INK, opacity=opacity))
        _text(drawing, root, label, x, 60 + 4, anchor="middle", size=SMALL_PT * scale,
              fill=PAPER)
        root.add(drawing.line(start=(x, axis_y - 12), end=(x, axis_y + 12), stroke=INK,
                              stroke_width=2))
        _text(drawing, root, f"{percent}%", x, axis_y + 28, anchor="middle", mono=True, bold=True)
        seconds = f"{duration * percent / 100:g}s"
        _text(drawing, root, seconds, x, axis_y + 44, anchor="middle", size=SMALL_PT, fill=MUTED)
        _text(drawing, root, f"scale({scale:g}), opacity {opacity:g}", x, 100,
              anchor="middle", size=SMALL_PT, mono=True, fill=MUTED)

    root.add(drawing.line(start=(x0, axis_y), end=(x0 + axis_w, axis_y), stroke=INK,
                          stroke_width=1.4))
    # The frames the browser fills in: one tick for each frame, at sixty a second.
    frames = int(duration * 60)
    keyframe_x = {round(x0 + axis_w * p / 100) for p, _, _ in stages}
    for index in range(1, frames):
        x = x0 + axis_w * index / frames
        if min(abs(x - k) for k in keyframe_x) < 4:
            continue
        root.add(drawing.line(start=(x, axis_y - 5), end=(x, axis_y + 5), stroke=MUTED,
                              stroke_width=0.8))
    _text(drawing, root, "Small ticks: the frames the browser fills in on its own",
          width / 2, axis_y + 70, anchor="middle", size=SMALL_PT, fill=MUTED)
    _text(drawing, root, "One pass of the animation", x0, 18, size=SMALL_PT, fill=MUTED)
    drawing.add(root)
    return drawing.tostring()


def one_parent_or_two() -> str:
    """Two questions, first sharing one parent, then each in its own div.

    The class names are read from the tutorial's cell. The second question
    is the one the reader writes in "Now add your own", so it has no cell of
    its own to read: it is drawn as the same three parts with `q2`. Arrows
    go from the ticked checkbox to every `.toggle-content` its `~` rule
    reaches, which is the whole lesson of step 4.
    """
    code = _cell("the-checkbox-hack", "accordion-html")
    toggle = re.search(r'<input[^>]*class="([\w-]+)"', code).group(1)
    label = re.search(r'<label[^>]*class="([\w-]+)"', code).group(1)
    content = re.search(r'<div class="([\w-]+)"', code).group(1)
    first_id = re.search(r'<input[^>]*id="(\w+)"', code).group(1)

    parts = [
        (f"checkbox {first_id}, ticked", toggle, "box"),
        (f"label for {first_id}", label, "label"),
        ("answer 1", content, "content"),
        ("checkbox q2", toggle, "box"),
        ("label for q2", label, "label"),
        ("answer 2", content, "content"),
    ]
    panel_w, part_w, part_h, step = 230, 170, 26, 36
    gap_between = 70
    width = MARGIN * 2 + panel_w * 2 + gap_between
    top = 44
    height = top + step * 6 + 40 + 70
    drawing = _drawing(width, height)
    root = drawing.g()
    arrow = _arrowhead(drawing, "reach")

    def part(x, y, text, kind, *, reached):
        fill = FILL_GREEN if reached else (FILL_AMBER if kind == "box" else PANEL)
        root.add(drawing.rect(insert=(x, y), size=(part_w, part_h), rx=3, fill=fill,
                              stroke=INK, stroke_width=1.8 if kind == "box" and "ticked" in text else 1))
        _text(drawing, root, text, x + 10, y + part_h / 2 + 4)

    def reach(x, y_from, y_to, bend):
        right = x + part_w
        path = drawing.path(
            d=f"M{right},{y_from} C{right + bend},{y_from} {right + bend},{y_to} {right + 2},{y_to}",
            fill="none", stroke=INK, stroke_width=1.4)
        path["marker-end"] = arrow
        root.add(path)

    # Left: one parent for all six parts.
    px = MARGIN
    root.add(drawing.rect(insert=(px, top - 14), size=(panel_w - 10, step * 6 + 18), rx=5,
                          fill="none", stroke=RULE, stroke_width=1.4))
    _text(drawing, root, "one parent", px, top - 20, size=SMALL_PT, fill=MUTED)
    ys = [top + i * step for i in range(6)]
    for (text, _, kind), y in zip(parts, ys):
        part(px + 12, y, text, kind, reached=kind == "content")
    reach(px + 12, ys[0] + part_h / 2, ys[2] + part_h / 2, 28)
    reach(px + 12, ys[0] + part_h / 2, ys[5] + part_h / 2, 44)

    # Right: each question in its own div.
    qx = MARGIN + panel_w + gap_between
    for index in range(2):
        y_top = top + index * step * 3 + (6 if index else 0)
        root.add(drawing.rect(insert=(qx, y_top - 10), size=(panel_w - 10, step * 3 - 2), rx=5,
                              fill="none", stroke=RULE, stroke_width=1.4))
        _text(drawing, root, "<div>", qx + panel_w - 16, y_top + 7, anchor="end", mono=True,
              size=SMALL_PT, fill=MUTED)
    for index, ((text, _, kind), y) in enumerate(zip(parts, ys)):
        shift = 6 if index >= 3 else 0
        part(qx + 12, y + shift, text, kind, reached=index == 2)
    reach(qx + 12, ys[0] + part_h / 2, ys[2] + part_h / 2, 28)

    base = top + step * 6 + 34
    _text(drawing, root, "Both answers open", MARGIN + panel_w / 2, base, anchor="middle")
    _text(drawing, root, "Only answer 1 opens", qx + panel_w / 2, base, anchor="middle")
    _text(drawing, root, f".{toggle}:checked ~ .{content}", width / 2, base + 30,
          anchor="middle", mono=True, size=SMALL_PT)
    _text(drawing, root, "reaches every later .%s with the same parent" % content,
          width / 2, base + 46, anchor="middle", size=SMALL_PT, fill=MUTED)
    drawing.add(root)
    return drawing.tostring()


# The student's home page, from portfolio_wad/index.html: every link and
# button in source order, once the contact section from "Links to pages,
# other sites and email" is added. The skills section has no link in it.
STARTER_STOPS = [
    ("page top", "Skip to main content"),
    ("header", "My Portfolio"),
    ("header", "Home"),
    ("header", "About"),
    ("header", "Skills"),
    ("header", "Contact"),
    ("hero", "Learn More About Me"),
    ("card", "Read More"),
    ("contact", "Send Me an Email"),
]


def tab_order() -> str:
    """The starter home page as bands, with each Tab stop numbered in order.

    The page is drawn as its regions, top to bottom, the way the HTML lists
    them: tab order is source order, so a picture in source order makes the
    numbers read in a plain line down the page, which is the point.
    """
    regions = []
    for region, text in STARTER_STOPS:
        if not regions or regions[-1][0] != region:
            regions.append((region, []))
        regions[-1][1].append(text)

    def chip_width(text: str) -> float:
        return 18 + len(text) * 6.4 + 10

    widest = max(sum(chip_width(t) + 6 for t in stops) for _, stops in regions)
    width = MARGIN * 2 + 74 + widest + 8
    inner = width - MARGIN * 2
    band_h = 44
    y = MARGIN + 18
    height = y + band_h * len(regions) + 60
    drawing = _drawing(width, height)
    root = drawing.g()
    _text(drawing, root, "Your home page, top to bottom", MARGIN, MARGIN + 4, size=SMALL_PT,
          fill=MUTED)

    number = 0
    for region, stops in regions:
        root.add(drawing.rect(insert=(MARGIN, y), size=(inner, band_h - 6), rx=4,
                              fill=PANEL, stroke=RULE, stroke_width=1))
        _text(drawing, root, region, MARGIN + 8, y + band_h / 2, size=SMALL_PT, fill=MUTED)
        x = MARGIN + 74
        for text in stops:
            number += 1
            chip_w = chip_width(text)
            root.add(drawing.rect(insert=(x, y + 8), size=(chip_w, band_h - 22), rx=3,
                                  fill=PAPER, stroke=INK, stroke_width=1))
            root.add(drawing.circle(center=(x + 10, y + band_h / 2 - 3), r=8, fill=INK))
            _text(drawing, root, str(number), x + 10, y + band_h / 2 + 1, anchor="middle",
                  size=SMALL_PT, fill=PAPER, bold=True)
            _text(drawing, root, text, x + 22, y + band_h / 2 + 1, size=SMALL_PT)
            x += chip_w + 6
        y += band_h

    _text(drawing, root, "Each press of Tab moves focus to the next number.",
          width / 2, y + 22, anchor="middle", size=SMALL_PT, fill=MUTED)
    _text(drawing, root, "Shift+Tab moves back.", width / 2, y + 38, anchor="middle",
          size=SMALL_PT, fill=MUTED)
    drawing.add(root)
    return drawing.tostring()


DIAGRAMS = {
    "transitions-and-transforms/transform-keeps-its-space.svg": transform_keeps_its_space,
    "keyframes-and-the-checkbox-hack/pulse-on-a-timeline.svg": pulse_on_a_timeline,
    "the-checkbox-hack/one-parent-or-two.svg": one_parent_or_two,
    "movement-focus-and-keyboards/tab-order.svg": tab_order,
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
