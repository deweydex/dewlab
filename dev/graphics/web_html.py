#!/usr/bin/env python3
"""The drawn diagrams Web Authoring's HTML pages use, and where each goes.

    python3 dev/graphics/web_html.py          # report what would change
    python3 dev/graphics/web_html.py --write  # write it

The pages in "Your first site" that teach HTML itself, before any CSS:
paths, heading levels, anchor links, and the two context pages beside
them. Each of these pictures shows something a live cell cannot: folders
a preview does not have, a page read as a list of contents, a jump down a
page too long for its window, the tree a browser builds from a file, and
a page as a screen reader might say it.

Same rule as web_authoring.py, which this follows: where a picture shows
a tutorial's own example, the words in it are read from the tutorial's
own cell or code fence, so the picture cannot drift from the code a
reader runs. Arrowheads are drawn as polygons, not SVG markers: these
files are inlined into the page, several to a page on the context pages,
and a marker's `id` would have to be unique across all of them.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import FILL_AMBER, FILL_BLUE, INK, MONO, MUTED, PANEL, PAPER, RULE, SANS  # noqa: E402

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL_PT = 12
SMALL_PT = 10.5
CODE_PT = 11
CHROME_H = 14          # the strip across the top of a drawn browser window
PANEL_GAP = 64         # between the two states of one picture
ARROW = 7.5


def _page(slug: str) -> str:
    return (TUTORIALS / slug / f"{slug}.md").read_text()


def _cell(slug: str, cell_id: str) -> str:
    """The code of one cell on a tutorial page, header lines removed."""
    match = re.search(rf"^```\w+ site\nid: {re.escape(cell_id)}\n(.*?)^```", _page(slug), re.S | re.M)
    if not match:
        raise SystemExit(f"{slug}: no site cell called {cell_id!r} any more")
    lines = [line for line in match.group(1).splitlines() if not line.startswith("site:")]
    return "\n".join(lines)


def _fence_starting(slug: str, first_line: str) -> list[str]:
    """The lines of the first plain ```html fence whose first line is `first_line`."""
    for match in re.finditer(r"^```html\n(.*?)^```", _page(slug), re.S | re.M):
        lines = match.group(1).rstrip("\n").splitlines()
        if lines and lines[0] == first_line:
            return lines
    raise SystemExit(f"{slug}: no html fence starting {first_line!r} any more")


def _elements(code: str, tag: str) -> list[str]:
    """The text of every `<tag …>text</tag>` in a piece of code, in order."""
    return [m.group(1).strip() for m in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", code, re.S)]


def _attribute(code: str, tag: str, name: str) -> list[str]:
    return re.findall(rf'<{tag}\b[^>]*\b{name}="([^"]*)"', code)


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _arrowhead(drawing, group, tip, angle, size: float = ARROW) -> None:
    """A filled head, so direction reads at a glance and at a distance."""
    spread = math.radians(26)
    points = [
        tip,
        (tip[0] - size * math.cos(angle - spread), tip[1] - size * math.sin(angle - spread)),
        (tip[0] - size * math.cos(angle + spread), tip[1] - size * math.sin(angle + spread)),
    ]
    group.add(drawing.polygon(points=points, fill=INK, stroke="none"))


def _route(drawing, group, points: list[tuple[float, float]], *, width: float = 1.4) -> None:
    """A line through `points`, square-cornered, with a head at the last one."""
    group.add(drawing.polyline(points=points, fill="none", stroke=INK, stroke_width=width))
    (x0, y0), (x1, y1) = points[-2], points[-1]
    _arrowhead(drawing, group, (x1, y1), math.atan2(y1 - y0, x1 - x0))


def _window(drawing, group, x: float, y: float, width: float, height: float,
            *, chrome: bool = True) -> None:
    """A browser window's outline, as in web_authoring.py."""
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


def paths() -> str:
    """Three paths from one HTML file, drawn as the folders they walk through.

    Folders are boxes inside boxes, because that is what "inside" means in
    a path, and each arrow starts at the one file every path is measured
    from. The three photos share a name on purpose: the name alone does
    not say which file we mean, the path does. The `../` arrow leaves the
    site's own folder, which is the one thing that makes it different.
    """
    file_w, file_h = 112, 32
    drawing = _drawing(560, 360)
    root = drawing.g()

    def folder(x, y, w, h, name):
        root.add(drawing.rect(
            insert=(x, y), size=(w, h), fill="none",
            stroke=RULE, stroke_width=1.6, rx=6))
        root.add(drawing.rect(
            insert=(x + 10, y - 9), size=(len(name) * 7.4 + 14, 18),
            fill=PANEL, stroke=RULE, stroke_width=1.2, rx=3))
        root.add(drawing.text(
            name, insert=(x + 17, y + 4), font_size=f"{LABEL_PT}px",
            font_family=MONO, font_weight="bold"))

    def file(x, y, name, *, start=False):
        root.add(drawing.rect(
            insert=(x, y), size=(file_w, file_h),
            fill=FILL_BLUE if start else PAPER, stroke=INK,
            stroke_width=1.8 if start else 1.1, rx=3))
        root.add(drawing.text(
            name, insert=(x + file_w / 2, y + file_h / 2 + 4), text_anchor="middle",
            font_size=f"{LABEL_PT}px", font_family=MONO,
            font_weight="bold" if start else "normal"))

    def label(text, x, y, anchor="start"):
        width = len(text) * CODE_PT * 0.62 + 10
        left = x if anchor == "start" else x - width
        root.add(drawing.rect(
            insert=(left, y - 11), size=(width, 17),
            fill=FILL_AMBER, stroke="none", rx=3))
        root.add(drawing.text(
            text, insert=(left + 5, y + 2), font_size=f"{CODE_PT}px", font_family=MONO))

    folder(12, 24, 536, 300, "projects/")
    folder(32, 84, 336, 226, "my-site/")
    folder(208, 176, 144, 118, "images/")

    index_x, index_y = 52, 118
    file(index_x, index_y, "index.html", start=True)
    file(index_x, 256, "photo.jpg")
    file(224, 238, "photo.jpg")
    file(412, 118, "photo.jpg")

    # photo.jpg: straight down, in the same folder.
    down_x = index_x + 40
    _route(drawing, root, [(down_x, index_y + file_h), (down_x, 256)])
    label("photo.jpg", down_x + 8, 206)

    # images/photo.jpg: out to the right, then into the images folder.
    into_x = 224 + file_w / 2
    _route(drawing, root, [(index_x + file_w, index_y + 12), (into_x, index_y + 12), (into_x, 238)])
    label("images/photo.jpg", index_x + file_w + 8, index_y + 34)

    # ../photo.jpg: up out of my-site, across, and down to the photo in projects.
    up_x = index_x + 76
    over_y = 56
    _route(drawing, root, [(up_x, index_y), (up_x, over_y), (412 + file_w / 2, over_y), (412 + file_w / 2, 118)])
    label("../photo.jpg", up_x + 60, over_y - 4)

    root.add(drawing.text(
        "Every path starts from index.html.", insert=(280, 350), text_anchor="middle",
        font_size=f"{LABEL_PT}px", fill=MUTED))
    drawing.add(root)
    return drawing.tostring()


# The longer page the headings tutorial draws. Not a cell: the tutorial's
# own cell has two headings, too few to show a list of contents nesting.
OUTLINE = [
    (1, "Plushie Shop"),
    (2, "New this week"),
    (3, "Squishy Squid"),
    (3, "Cuddly Cuttlefish"),
    (2, "Visit us"),
]


def heading_outline() -> str:
    """A page as a browser draws it, and its headings read on their own.

    The left panel keeps the default sizes (each level smaller than the
    one before) and grey bars for paragraphs, because what a reader should
    see is that the sizes follow the levels. The right panel is the same
    headings with everything else taken away, indented by level, which is
    what "a list of contents" means.
    """
    sizes = {1: 20, 2: 15.5, 3: 12.5}
    width, view_h = 230, 250
    margin = 16
    top = margin + CHROME_H + 4
    drawing = _drawing(margin * 2 + width * 2 + PANEL_GAP, top + view_h + 44)
    root = drawing.g()

    x0 = margin
    y = top + 10
    for index, (level, text) in enumerate(OUTLINE):
        size = sizes[level]
        y += size + 10
        root.add(drawing.text(
            text, insert=(x0 + 14, y), font_size=f"{size}px", font_weight="bold"))
        # A heading with nothing under it but a smaller heading gets no text.
        following = OUTLINE[index + 1][0] if index + 1 < len(OUTLINE) else 0
        if following <= level and level > 1:
            y += 9
            root.add(drawing.rect(
                insert=(x0 + 14, y), size=(width - 60, 7), fill=RULE, rx=3))
    _window(drawing, root, x0, top, width, view_h)

    # The arrow between the panels.
    mid_y = top + view_h / 2
    _route(drawing, root, [(x0 + width + 12, mid_y), (x0 + width + PANEL_GAP - 12, mid_y)])

    x1 = margin + width + PANEL_GAP
    root.add(drawing.rect(
        insert=(x1, top - CHROME_H), size=(width, view_h + CHROME_H),
        fill=PANEL, stroke=RULE, stroke_width=1.2, rx=5))
    row_h = 36
    first = top + 24
    for index, (level, text) in enumerate(OUTLINE):
        indent = (level - 1) * 26
        ty = first + index * row_h
        if level > 1:
            parent = max(i for i in range(index) if OUTLINE[i][0] == level - 1)
            px = x1 + 16 + (level - 2) * 26 + 10
            root.add(drawing.polyline(
                points=[(px, first + parent * row_h + 8), (px, ty - 4), (x1 + 16 + indent - 3, ty - 4)],
                fill="none", stroke=MUTED, stroke_width=1))
        tag = f"h{level}"
        root.add(drawing.rect(
            insert=(x1 + 16 + indent, ty - 14), size=(22, 17), fill=FILL_BLUE, rx=3))
        root.add(drawing.text(
            tag, insert=(x1 + 16 + indent + 11, ty - 1), text_anchor="middle",
            font_size=f"{SMALL_PT}px", font_family=MONO))
        root.add(drawing.text(
            text, insert=(x1 + 16 + indent + 28, ty), font_size=f"{LABEL_PT}px"))

    base = top + view_h + 24
    _caption(drawing, root, x0 + width / 2, base, [("The page", False)])
    _caption(drawing, root, x1 + width / 2, base, [("Its headings on their own", False)])
    drawing.add(root)
    return drawing.tostring()


def anchor_jump() -> str:
    """The navigation example's page, before and after clicking the second link.

    Drawn like the sticky header in web_authoring.py: the window is solid
    and the page runs past it, dashed, so that a still picture can show the
    page moving. The arrow in the first panel runs outside the page, from
    the link to its target, because the target is outside the window when
    the reader clicks.
    """
    code = _cell("navigation", "nav-demo-html")
    links = _elements(code, "a")
    hrefs = _attribute(code, "a", "href")
    headings = _elements(code, "h2")
    paragraphs = _elements(code, "p")
    ids = _attribute(code, "section", "id")
    target = hrefs[1].lstrip("#")

    width, view_h = 210, 124
    nav_h, section_h, gap = 50, 58, 70
    jump = nav_h + section_h + gap                 # where section two starts on the page
    # The last section is drawn as tall as the window: a browser cannot
    # scroll past the end of a page, so a target near the end only reaches
    # the top of the window when there is a window's height of page below it.
    last_h = view_h
    page_h = jump + last_h
    margin = 16
    top = margin + jump                            # the scrolled page needs this much room above
    below = page_h - view_h
    drawing = _drawing(margin * 2 + width * 2 + PANEL_GAP + 40, top + view_h + below + 84)
    root = drawing.g()

    clips = []
    for index in range(2):
        x = margin + index * (width + PANEL_GAP + 40)
        clip = drawing.defs.add(drawing.clipPath(id=f"anchor-window-{index}"))
        clip.add(drawing.rect(insert=(x, top), size=(width, view_h)))
        clips.append(clip.get_funciri())

    def page(x, page_top, *, inside, clip=None):
        group = drawing.g(clip_path=clip) if clip else drawing.g()
        stroke = INK if inside else MUTED
        dash = None if inside else "4 3"
        ink = INK if inside else MUTED
        # the menu
        group.add(drawing.rect(
            insert=(x + 0.5, page_top), size=(width - 1, nav_h),
            fill=PANEL if inside else "none", stroke=stroke, stroke_width=1, stroke_dasharray=dash))
        for index, text in enumerate(links):
            group.add(drawing.text(
                f"• {text}", insert=(x + 12, page_top + 20 + index * 18),
                font_size=f"{LABEL_PT}px", fill=ink, text_decoration="underline"))
        # the sections
        y = page_top + nav_h
        for index, heading in enumerate(headings):
            if index == 1:
                y += gap
            box_h = last_h if index == len(headings) - 1 else section_h
            group.add(drawing.rect(
                insert=(x + 0.5, y), size=(width - 1, box_h),
                fill=PAPER if inside else "none", stroke=stroke, stroke_width=1,
                stroke_dasharray=dash))
            group.add(drawing.text(
                heading, insert=(x + 12, y + 20), font_size=f"{LABEL_PT}px",
                font_weight="bold", fill=ink))
            group.add(drawing.text(
                paragraphs[index], insert=(x + 12, y + 38), font_size=f"{SMALL_PT}px", fill=ink))
            group.add(drawing.text(
                f'id="{ids[index]}"', insert=(x + width - 10, y + box_h - 8), text_anchor="end",
                font_size=f"{SMALL_PT}px", font_family=MONO, fill=MUTED))
            y += box_h
        root.add(group)

    # Before the click: the page starts at the top of the window.
    x0 = margin
    page(x0, top, inside=False)
    page(x0, top, inside=True, clip=clips[0])
    _window(drawing, root, x0, top, width, view_h, chrome=False)
    link_y = top + 20 + 18 - 4
    link_end = x0 + 12 + (len(links[1]) + 2) * LABEL_PT * 0.55
    target_y = top + jump + 16
    side = x0 + width + 18
    _route(drawing, root, [(link_end + 4, link_y), (side, link_y), (side, target_y), (x0 + width + 4, target_y)])
    root.add(drawing.text(
        f'href="{hrefs[1]}"', insert=(side + 6, (link_y + target_y) / 2),
        font_size=f"{SMALL_PT}px", font_family=MONO))

    # After the click: the page has moved up by `jump`, and `target` is at the top.
    x1 = margin + width + PANEL_GAP + 40
    page(x1, top - jump, inside=False)
    page(x1, top - jump, inside=True, clip=clips[1])
    _window(drawing, root, x1, top, width, view_h, chrome=False)

    base = top + view_h + below + 26
    _caption(drawing, root, x0 + width / 2, base, [("Before the click", False)])
    _caption(drawing, root, x1 + width / 2, base,
             [("After the click", False), (f'#{target} is at the top of the window', False)])
    root.add(drawing.text(
        "Dashed: the parts of the page outside the window.",
        insert=((x0 + x1 + width) / 2, base + 44), text_anchor="middle",
        font_size=f"{SMALL_PT}px", fill=MUTED))
    drawing.add(root)
    return drawing.tostring()


def page_tree() -> str:
    """The skeleton page's code, and the tree a browser builds from it.

    The code is read from the-skeleton's own whole-page fence and set on
    the left exactly as written, indents included, so the reader can match
    each indent to a level of the tree. The tree leaves out DOCTYPE, which
    is not an element, and puts the text each element holds under it in a
    lighter colour, as the inspector does.
    """
    lines = _fence_starting("the-skeleton", "<!DOCTYPE html>")
    code = "\n".join(lines)
    title = _elements(code, "title")[0]
    heading = _elements(code, "h1")[0]
    paragraph = _elements(code, "p")[0]

    char_w = CODE_PT * 0.61
    code_w = max(len(line) for line in lines) * char_w + 24
    line_h = 18
    margin = 16
    code_h = len(lines) * line_h + 20
    tree_x = margin + code_w + 48
    leaf_gap = 128
    tree_w = leaf_gap * 2 + 120
    height = max(code_h, 250) + margin * 2
    drawing = _drawing(tree_x + tree_w + margin, height)
    root = drawing.g()

    root.add(drawing.rect(
        insert=(margin, margin), size=(code_w, code_h),
        fill=PANEL, stroke=RULE, stroke_width=1, rx=5))
    for index, line in enumerate(lines):
        root.add(drawing.text(
            line.replace(" ", " "), insert=(margin + 12, margin + 22 + index * line_h),
            font_size=f"{CODE_PT}px", font_family=MONO,
            fill=MUTED if line.startswith("<!") else INK))

    _route(drawing, root, [(margin + code_w + 10, height / 2), (tree_x - 10, height / 2)])

    def node(cx, cy, name):
        w = len(name) * 8 + 22
        root.add(drawing.rect(
            insert=(cx - w / 2, cy - 12), size=(w, 24), fill=FILL_BLUE,
            stroke=INK, stroke_width=1.2, rx=4))
        root.add(drawing.text(
            name, insert=(cx, cy + 4), text_anchor="middle",
            font_size=f"{LABEL_PT}px", font_family=MONO))

    def edge(a, b):
        root.add(drawing.line(start=(a[0], a[1] + 12), end=(b[0], b[1] - 12),
                              stroke=INK, stroke_width=1.2))

    def words(cx, cy, text):
        # Wrap at roughly 18 characters, so the paragraph's text fits a column.
        out, line = [], ""
        for word in text.split():
            if len(line) + len(word) + 1 > 18 and line:
                out.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        out.append(line)
        out[0] = f"\u201c{out[0]}"
        out[-1] = f"{out[-1]}\u201d"
        for index, part in enumerate(out):
            root.add(drawing.text(
                part, insert=(cx, cy + index * 14),
                text_anchor="middle", font_size=f"{SMALL_PT}px", fill=MUTED))

    left = tree_x + 60
    html_at = (left + leaf_gap, margin + 30)
    head_at = (left + leaf_gap * 0.35, margin + 100)
    body_at = (left + leaf_gap * 1.5, margin + 100)
    title_at = (head_at[0], margin + 170)
    h1_at = (left + leaf_gap, margin + 170)
    p_at = (left + leaf_gap * 2, margin + 170)
    for a, b in [(html_at, head_at), (html_at, body_at), (head_at, title_at),
                 (body_at, h1_at), (body_at, p_at)]:
        edge(a, b)
    for at, name in [(html_at, "html"), (head_at, "head"), (body_at, "body"),
                     (title_at, "title"), (h1_at, "h1"), (p_at, "p")]:
        node(*at, name)
    words(title_at[0], title_at[1] + 30, title)
    words(h1_at[0], h1_at[1] + 30, heading)
    words(p_at[0], p_at[1] + 30, paragraph)

    drawing.add(root)
    return drawing.tostring()


def screen_reader_says() -> str:
    """The second half of the context page's example, seen and heard.

    The heading, the navigation's name and the link words are read from
    the cell. The spoken lines follow the accessibility tree Chromium
    builds for that markup (banner, heading level 1, a navigation named
    by aria-label, two links); the wording is typical, not any one screen
    reader's, and the picture says so.
    """
    code = _cell("who-reads-a-page", "readers-html")
    semantic = code[code.index("<header>"):]
    heading = _elements(semantic, "h1")[0]
    nav_name = _attribute(semantic, "nav", "aria-label")[0]
    links = _elements(semantic, "a")
    spoken = ["banner", f"heading, level 1, {heading}", f"{nav_name} navigation"]
    spoken += [f"link, {text}" for text in links]

    width, view_h = 220, 150
    margin = 16
    top = margin + CHROME_H + 26
    drawing = _drawing(margin * 2 + width * 2 + PANEL_GAP, top + view_h + 52)
    root = drawing.g()

    x0 = margin
    root.add(drawing.text(
        "A sighted visitor sees", insert=(x0 + width / 2, margin + 8),
        text_anchor="middle", font_size=f"{LABEL_PT}px", font_weight="bold"))
    root.add(drawing.text(
        heading, insert=(x0 + 16, top + 36), font_size="20px", font_weight="bold"))
    link_x = x0 + 16
    for text in links:
        root.add(drawing.text(
            text, insert=(link_x, top + 64), font_size=f"{LABEL_PT + 1}px",
            text_decoration="underline"))
        link_x += len(text) * 8 + 16
    _window(drawing, root, x0, top, width, view_h)

    x1 = margin + width + PANEL_GAP
    root.add(drawing.text(
        "A screen reader might say", insert=(x1 + width / 2, margin + 8),
        text_anchor="middle", font_size=f"{LABEL_PT}px", font_weight="bold"))
    root.add(drawing.rect(
        insert=(x1, top - CHROME_H), size=(width, view_h + CHROME_H),
        fill=PANEL, stroke=RULE, stroke_width=1.2, rx=5))
    for index, line in enumerate(spoken):
        y = top + 12 + index * 26
        root.add(drawing.rect(
            insert=(x1 + 12, y - 2), size=(4, 18), fill=FILL_AMBER, rx=1))
        root.add(drawing.text(
            f"“{line}”", insert=(x1 + 24, y + 12), font_size=f"{LABEL_PT}px",
            font_style="italic"))

    _route(drawing, root, [(x0 + width + 12, top + view_h / 2 - 7),
                           (x1 - 12, top + view_h / 2 - 7)])
    root.add(drawing.text(
        "The exact words differ from one screen reader to another.",
        insert=((x0 + x1 + width) / 2, top + view_h + 30), text_anchor="middle",
        font_size=f"{SMALL_PT}px", fill=MUTED))
    drawing.add(root)
    return drawing.tostring()


DIAGRAMS = {
    "images-and-alt-text/paths.svg": paths,
    "headings-and-emphasis/heading-outline.svg": heading_outline,
    "navigation/anchor-jump.svg": anchor_jump,
    "how-a-browser-reads-html/page-tree.svg": page_tree,
    "who-reads-a-page/screen-reader-says.svg": screen_reader_says,
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
