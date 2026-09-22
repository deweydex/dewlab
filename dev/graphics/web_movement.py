#!/usr/bin/env python3
"""The drawn diagrams for Web Authoring's "Movement and depth" pages.

    python3 dev/graphics/web_movement.py          # report what would change
    python3 dev/graphics/web_movement.py --write  # write it

Every one of these is a view the reader cannot get from the preview: the
stage seen from the side or from above, with the viewer's eye drawn in, or
the order of work a browser does for each frame. A preview only ever shows
the picture on the screen, so what put it there has to be drawn.

Same rules as `web_authoring.py`: the colours are the palette's tokens, so
the pictures follow the page into dark mode, and where a picture names a
number from a tutorial's own cell, the number is read from that cell.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import FILL_AMBER, FILL_BLUE, INK, MONO, MUTED, PANEL, RULE, SANS  # noqa: E402

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL_PT = 12
SMALL_PT = 10.5


def _cell(slug: str, cell_id: str) -> str:
    """The code of one cell on a tutorial page, header lines removed."""
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    match = re.search(rf"^```\w+ site\nid: {re.escape(cell_id)}\n(.*?)^```", page, re.S | re.M)
    if not match:
        raise SystemExit(f"{slug}: no site cell called {cell_id!r} any more")
    return "\n".join(line for line in match.group(1).splitlines() if not line.startswith("site:"))


def _number(code: str, pattern: str) -> int:
    match = re.search(pattern, code)
    if not match:
        raise SystemExit(f"no match for {pattern!r} in a cell any more")
    return int(match.group(1))


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _text(drawing, group, text, x, y, *, size=LABEL_PT, anchor="start", code=False,
          muted=False, bold=False) -> None:
    group.add(drawing.text(
        text, insert=(x, y), text_anchor=anchor, font_size=f"{size}px",
        font_family=MONO if code else SANS, fill=MUTED if muted else INK,
        font_weight="bold" if bold else "normal"))


def _eye(drawing, group, x: float, y: float, *, facing: str) -> None:
    """A small eye: an almond outline and a pupil, looking right or up."""
    if facing == "right":
        group.add(drawing.path(
            d=f"M {x - 12} {y} Q {x} {y - 11} {x + 12} {y} Q {x} {y + 11} {x - 12} {y} Z",
            fill="none", stroke=INK, stroke_width=1.6))
        group.add(drawing.circle(center=(x + 3, y), r=4, fill=INK))
    else:
        group.add(drawing.path(
            d=f"M {x} {y + 12} Q {x - 11} {y} {x} {y - 12} Q {x + 11} {y} {x} {y + 12} Z",
            fill="none", stroke=INK, stroke_width=1.6))
        group.add(drawing.path(
            d=f"M {x - 12} {y} Q {x} {y - 11} {x + 12} {y} Q {x} {y + 11} {x - 12} {y} Z",
            fill="none", stroke=INK, stroke_width=1.6))
        group.add(drawing.circle(center=(x, y), r=4, fill=INK))


def _arrowhead(drawing, group, tip, angle: float, size: float = 7) -> None:
    """A filled arrowhead with its point at `tip`, pointing along `angle` (radians)."""
    x, y = tip
    left = (x - size * math.cos(angle - 0.45), y - size * math.sin(angle - 0.45))
    right = (x - size * math.cos(angle + 0.45), y - size * math.sin(angle + 0.45))
    group.add(drawing.polygon(points=[tip, left, right], fill=INK))


def perspective_glass() -> str:
    """The orbit's stage seen from the side, with the eye `perspective` away.

    Two balls of the same size, one 100px in front of the screen and one
    100px behind it, and the rays from the eye through each ball's edges to
    the screen. Where those rays cross the screen is the picture the browser
    draws. The ball in front is drawn bigger and further from the middle,
    the ball behind smaller and nearer to it, which is all `perspective`
    does. Distances along the depth are to scale; the balls are drawn much
    larger than 24px, or their pictures would be too small to label.
    """
    code = _cell("an-orbit-in-css", "orbit-css")
    distance = _number(code, r"perspective:\s*(\d+)px")
    push = _number(code, r"translateZ\((\d+)px\)")

    scale = 0.6                      # drawn pixels per CSS pixel along the depth
    eye_x, axis_y = 56, 170
    screen_x = eye_x + distance * scale
    radius, offset = 22, 52          # drawn; the same for both balls
    width, height = screen_x + push * scale + 200, 330
    drawing = _drawing(width, height)
    root = drawing.g()

    # The line straight ahead from the eye, and the screen across it.
    root.add(drawing.line(start=(eye_x + 14, axis_y), end=(width - 20, axis_y),
                          stroke=RULE, stroke_width=1, stroke_dasharray="2 4"))
    root.add(drawing.line(start=(screen_x, 36), end=(screen_x, 286), stroke=INK, stroke_width=2.4))
    _text(drawing, root, "the screen", screen_x, 26, anchor="middle", bold=True)
    _eye(drawing, root, eye_x, axis_y, facing="right")
    _text(drawing, root, "your eye", eye_x, axis_y + 30, anchor="middle")

    balls = [
        (screen_x - push * scale, axis_y - offset, FILL_AMBER, "in front: drawn bigger", -1),
        (screen_x + push * scale, axis_y + offset, FILL_BLUE, "behind: drawn smaller", 1),
    ]
    for ball_x, ball_y, fill, label, side in balls:
        ratio = (screen_x - eye_x) / (ball_x - eye_x)
        top = axis_y + (ball_y - radius - axis_y) * ratio
        bottom = axis_y + (ball_y + radius - axis_y) * ratio
        for edge_y, hit_y in ((ball_y - radius, top), (ball_y + radius, bottom)):
            far_x, far_y = (screen_x, hit_y) if ball_x < screen_x else (ball_x, edge_y)
            root.add(drawing.line(start=(eye_x + 12, axis_y), end=(far_x, far_y),
                                  stroke=MUTED, stroke_width=1, stroke_dasharray="4 3"))
        root.add(drawing.circle(center=(ball_x, ball_y), r=radius, fill=fill,
                                stroke=INK, stroke_width=1.4))
        # The picture on the screen: a thick bar where the rays cross it.
        root.add(drawing.rect(insert=(screen_x - 4, top), size=(8, bottom - top),
                              fill=fill, stroke=INK, stroke_width=1.4, rx=2))
        if side < 0:
            _text(drawing, root, label, screen_x + 12, top - 12)
        else:
            _text(drawing, root, label, screen_x - 12, bottom + 34, anchor="end")

    _text(drawing, root, f"translateZ({push}px)", screen_x - push * scale, axis_y - offset - radius - 10,
          anchor="middle", size=SMALL_PT, code=True)
    _text(drawing, root, f"translateZ(-{push}px)", screen_x + push * scale, axis_y + offset + radius + 18,
          anchor="start", size=SMALL_PT, code=True)

    # How far the screen stands from the eye.
    rule_y = 306
    root.add(drawing.line(start=(eye_x, rule_y), end=(screen_x, rule_y), stroke=INK, stroke_width=1.2))
    _arrowhead(drawing, root, (eye_x, rule_y), math.pi)
    _arrowhead(drawing, root, (screen_x, rule_y), 0)
    _text(drawing, root, f"perspective: {distance}px", (eye_x + screen_x) / 2, rule_y - 8,
          anchor="middle", code=True)
    drawing.add(root)
    return drawing.tostring()


def _orbit_from_above(drawing, group, cx: float, cy: float, *, facing: bool) -> None:
    """One panel: the orbit seen from above, the viewer below it."""
    radius, half = 74, 13
    group.add(drawing.circle(center=(cx, cy), r=radius, fill="none", stroke=MUTED,
                             stroke_width=1.2, stroke_dasharray="4 3"))
    group.add(drawing.circle(center=(cx, cy), r=15, fill=FILL_AMBER, stroke=INK, stroke_width=1.2))
    _text(drawing, group, "sun", cx, cy + 4, anchor="middle", size=SMALL_PT)
    for step in range(8):
        angle = step * math.pi / 4
        # rotateY carries the front point (towards the viewer, down the page)
        # round to the right first.
        bx, by = cx + radius * math.sin(angle), cy + radius * math.cos(angle)
        if facing:
            dx, dy = half, 0.0
        else:
            dx, dy = half * math.cos(angle), -half * math.sin(angle)
        side_on = not facing and step in (2, 6)
        group.add(drawing.line(start=(bx - dx, by - dy), end=(bx + dx, by + dy),
                               stroke=INK, stroke_width=5 if side_on else 3.4,
                               stroke_linecap="round"))
    # Which way it goes round.
    start, end = math.radians(20), math.radians(55)
    arc_r = radius + 16
    p0 = (cx + arc_r * math.sin(start), cy + arc_r * math.cos(start))
    p1 = (cx + arc_r * math.sin(end), cy + arc_r * math.cos(end))
    group.add(drawing.path(d=f"M {p0[0]:.1f} {p0[1]:.1f} A {arc_r} {arc_r} 0 0 0 {p1[0]:.1f} {p1[1]:.1f}",
                           fill="none", stroke=INK, stroke_width=1.2))
    _arrowhead(drawing, group, p1, -end)
    _eye(drawing, group, cx, cy + radius + 44, facing="up")
    _text(drawing, group, "you", cx, cy + radius + 72, anchor="middle")


def ball_from_above() -> str:
    """The orbit from above, the ball drawn as the flat disc it is.

    The whole point is the disc's direction, so it is drawn edge-on, as a
    short thick line, at eight places round the orbit. On the left it stays
    square to the orbit, as a disc glued to a turntable does, and at the far
    left and right it points straight at the viewer: all they can see is its
    edge. On the right it has been turned back by the same angle, so it is
    square to the viewer everywhere.
    """
    panel_w, gap, margin = 250, 30, 12
    cy = 116
    height = 330
    drawing = _drawing(margin * 2 + panel_w * 2 + gap, height)
    root = drawing.g()
    for index, facing in enumerate((False, True)):
        cx = margin + panel_w / 2 + index * (panel_w + gap)
        _orbit_from_above(drawing, root, cx, cy, facing=facing)
        title = "turned back each time" if facing else "carried round, never turned back"
        note = "it always faces you" if facing else "at the sides, only its edge faces you"
        _text(drawing, root, title, cx, height - 30, anchor="middle")
        _text(drawing, root, note, cx, height - 12, anchor="middle", size=SMALL_PT, muted=True)
    drawing.add(root)
    return drawing.tostring()


def push_then_turn() -> str:
    """One face of the cube, seen from above, in three steps.

    The cube's outline is dashed, the face is a thick line, and the viewer
    is below. Start: the face lies across the middle of the cube. Push: it
    moves out to the front edge. Turn: it swings a quarter turn about the
    cube's middle and ends on the right-hand edge, facing right. That the
    turn is about the middle of the cube, and not about the face, is why
    pushing first and turning second puts the face on a side.
    """
    code = _cell("a-cube-in-css", "cube-css")
    size = _number(code, r"\.cube \{\n  width: (\d+)px")
    push = _number(code, r"\.front\s*\{ transform: translateZ\((\d+)px\)")

    box, panel_w, margin = 110, 180, 14
    half = box / 2
    offset = box * push / size
    top = 30
    height = 270
    drawing = _drawing(margin * 2 + panel_w * 3, height)
    root = drawing.g()
    titles = [
        ("1. Where it starts", "across the middle", False),
        (f"2. translateZ({push}px)", "pushed towards you", True),
        ("3. rotateY(90deg)", "turned about the middle", True),
    ]
    for index, (title, note, code_title) in enumerate(titles):
        cx = margin + panel_w / 2 + index * panel_w
        cy = top + half + 10
        root.add(drawing.rect(insert=(cx - half, cy - half), size=(box, box), fill="none",
                              stroke=MUTED, stroke_width=1.2, stroke_dasharray="4 3"))
        root.add(drawing.circle(center=(cx, cy), r=2.5, fill=MUTED))
        if index == 0:
            start, end = (cx - half, cy), (cx + half, cy)
        elif index == 1:
            start, end = (cx - half, cy + offset), (cx + half, cy + offset)
        else:
            start, end = (cx + offset, cy - half), (cx + offset, cy + half)
            arc_r = offset
            root.add(drawing.path(
                d=f"M {cx:.1f} {cy + arc_r:.1f} A {arc_r} {arc_r} 0 0 0 {cx + arc_r:.1f} {cy:.1f}",
                fill="none", stroke=MUTED, stroke_width=1.2, stroke_dasharray="3 3"))
            _arrowhead(drawing, root, (cx + arc_r, cy + 1), -math.pi / 2, size=6)
            root.add(drawing.line(start=(cx - half, cy + offset), end=(cx + half, cy + offset),
                                  stroke=MUTED, stroke_width=1.2, stroke_dasharray="2 3"))
        root.add(drawing.line(start=start, end=end, stroke=INK, stroke_width=4, stroke_linecap="round"))
        if index == 1:
            root.add(drawing.line(start=(cx, cy), end=(cx, cy + offset - 5), stroke=INK, stroke_width=1.2))
            _arrowhead(drawing, root, (cx, cy + offset - 3), math.pi / 2, size=6)
        _eye(drawing, root, cx, cy + half + 30, facing="up")
        _text(drawing, root, title, cx, height - 36, anchor="middle", code=code_title and index > 0)
        _text(drawing, root, note, cx, height - 18, anchor="middle", size=SMALL_PT, muted=True)
    _text(drawing, root, "Seen from above. The dashed square is the cube; the thick line is the face.",
          margin + panel_w * 1.5, 16, anchor="middle", size=SMALL_PT, muted=True)
    drawing.add(root)
    return drawing.tostring()


def canvas_coordinates() -> str:
    """The orbit canvas, with where its numbers put things.

    A canvas counts from its top-left corner, across and down. The middle,
    which `project` adds to every point, is half the width across and half
    the height down. The size is read from the tutorial's own `<canvas>`.
    """
    code = _cell("drawing-frames-with-javascript", "orbit-canvas-html")
    width_px = _number(code, r'width="(\d+)"')
    height_px = _number(code, r'height="(\d+)"')

    scale = 1.0
    left, top = 120, 44
    w, h = width_px * scale, height_px * scale
    drawing = _drawing(left + w + 90, top + h + 60)
    root = drawing.g()
    root.add(drawing.rect(insert=(left, top), size=(w, h), fill=PANEL, stroke=INK, stroke_width=1.6))
    root.add(drawing.circle(center=(left, top), r=4, fill=INK))
    _text(drawing, root, "(0, 0)", left - 8, top - 8, anchor="end", code=True)

    # x across, y down.
    root.add(drawing.line(start=(left, top - 22), end=(left + 110, top - 22), stroke=INK, stroke_width=1.4))
    _arrowhead(drawing, root, (left + 112, top - 22), 0)
    _text(drawing, root, "x grows to the right", left + 122, top - 18)
    root.add(drawing.line(start=(left - 22, top), end=(left - 22, top + 110), stroke=INK, stroke_width=1.4))
    _arrowhead(drawing, root, (left - 22, top + 112), math.pi / 2)
    _text(drawing, root, "y grows", left - 30, top + 134, anchor="end")
    _text(drawing, root, "downwards", left - 30, top + 150, anchor="end")

    mx, my = left + w / 2, top + h / 2
    root.add(drawing.line(start=(mx - 8, my), end=(mx + 8, my), stroke=INK, stroke_width=1.6))
    root.add(drawing.line(start=(mx, my - 8), end=(mx, my + 8), stroke=INK, stroke_width=1.6))
    _text(drawing, root, f"({width_px // 2}, {height_px // 2})", mx + 12, my - 8, code=True)
    _text(drawing, root, "middleX, middleY", mx + 12, my + 18, size=SMALL_PT, muted=True)

    root.add(drawing.circle(center=(left + w, top + h), r=4, fill=INK))
    _text(drawing, root, f"({width_px}, {height_px})", left + w + 8, top + h + 18, code=True)
    drawing.add(root)
    return drawing.tostring()


def frame_steps() -> str:
    """The steps a browser takes to draw one frame, and which ones a change needs.

    Three rows. The top row names the steps in order. The next two show a
    change to a size or a position, which needs every step, and a change to
    `transform` or `opacity`, which can skip layout and paint: the browser
    moves or fades a picture it has already painted. Skipped steps are drawn
    dashed and empty, so the row still lines up under the names. Running
    the page's own JavaScript comes before all four, and only when a script
    asked for the frame, so the context page says it in words and the
    picture leaves it out.
    """
    steps = ["Style", "Layout", "Paint", "Composite"]
    rows = [
        ("width or left", [True, True, True, True]),
        ("transform or opacity", [True, False, False, True]),
    ]
    box_w, box_h, gap = 110, 38, 14
    label_w, margin = 170, 12
    left = margin + label_w
    top = 44
    width = left + len(steps) * (box_w + gap) + margin
    height = top + box_h + 26 + len(rows) * (box_h + 22) + 20
    drawing = _drawing(width, height)
    root = drawing.g()

    _text(drawing, root, "One frame, from left to right", left, 20, muted=True, size=SMALL_PT)
    for index, name in enumerate(steps):
        x = left + index * (box_w + gap)
        root.add(drawing.rect(insert=(x, top), size=(box_w, box_h), fill=PANEL,
                              stroke=INK, stroke_width=1.4, rx=4))
        _text(drawing, root, name, x + box_w / 2, top + box_h / 2 + 4, anchor="middle", bold=True)
        if index:
            ax = x - gap + 2
            root.add(drawing.line(start=(ax, top + box_h / 2), end=(x - 3, top + box_h / 2),
                                  stroke=INK, stroke_width=1.2))
            _arrowhead(drawing, root, (x - 2, top + box_h / 2), 0, size=5)

    y = top + box_h + 26
    _text(drawing, root, "When a frame changes...", margin, y - 8, muted=True, size=SMALL_PT)
    for label, needed in rows:
        _text(drawing, root, label, margin, y + box_h / 2 + 4, code=True)
        for index, used in enumerate(needed):
            x = left + index * (box_w + gap)
            if used:
                root.add(drawing.rect(insert=(x, y), size=(box_w, box_h), fill=FILL_BLUE,
                                      stroke=INK, stroke_width=1.2, rx=4))
                _text(drawing, root, "needed", x + box_w / 2, y + box_h / 2 + 4, anchor="middle")
            else:
                root.add(drawing.rect(insert=(x, y), size=(box_w, box_h), fill="none",
                                      stroke=MUTED, stroke_width=1.2, stroke_dasharray="4 3", rx=4))
                _text(drawing, root, "can skip", x + box_w / 2, y + box_h / 2 + 4,
                      anchor="middle", muted=True)
        y += box_h + 22
    drawing.add(root)
    return drawing.tostring()


DIAGRAMS = {
    "an-orbit-in-css/perspective-glass.svg": perspective_glass,
    "a-ball-that-faces-you/ball-from-above.svg": ball_from_above,
    "a-cube-in-css/push-then-turn.svg": push_then_turn,
    "drawing-frames-with-javascript/canvas-coordinates.svg": canvas_coordinates,
    "how-a-browser-draws-a-frame/frame-steps.svg": frame_steps,
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
