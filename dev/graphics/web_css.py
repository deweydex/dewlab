#!/usr/bin/env python3
"""The drawn diagrams Web Authoring's first CSS pages use, and where each goes.

    python3 dev/graphics/web_css.py          # report what would change
    python3 dev/graphics/web_css.py --write  # write it

The pages are "CSS rules and stylesheets", "Colours, and naming them
with variables", "Text size, units and alignment", "Choosing what to
style: selectors and classes", and the context page "The cascade: which CSS rule wins".
Each diagram shows how one piece of CSS reaches, or fails to reach, an
element: a file shared by two pages, a variable read by two rules, a
unit measured against the root, lines of text lined up four ways, a
selector matching one branch of a tree, and a rule crossed out in the
inspector.

Same rule as dev/graphics/web_authoring.py: where a picture shows a
tutorial's own example, the words in it are read from that tutorial's
own cell, so the picture cannot drift from the code a reader runs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (  # noqa: E402
    FILL_AMBER, FILL_BLUE, INK, MONO, MUTED, PANEL, PAPER, RULE, SANS,
)

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

LABEL_PT = 12
SMALL_PT = 10.5
CODE_PT = 11.5
MONO_W = 0.6           # a monospace character's width, as a fraction of its size


def _cell(slug: str, cell_id: str) -> str:
    """The code of one cell on a tutorial page, header lines removed."""
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    match = re.search(rf"^```\w+ site\nid: {re.escape(cell_id)}\n(.*?)^```", page, re.S | re.M)
    if not match:
        raise SystemExit(f"{slug}: no site cell called {cell_id!r} any more")
    lines = [line for line in match.group(1).splitlines() if not line.startswith("site:")]
    return "\n".join(lines)


def _elements(code: str, tag: str) -> list[str]:
    """The text of every `<tag …>text</tag>` in a cell, in order."""
    return [m.group(1).strip() for m in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", code, re.S)]


def _declaration(code: str, prop: str) -> str:
    """The value of the first `prop: value;` in a cell."""
    match = re.search(rf"(?<![\w-]){re.escape(prop)}\s*:\s*([^;]+);", code)
    if not match:
        raise SystemExit(f"no {prop!r} declaration in the cell any more")
    return match.group(1).strip()


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _code(drawing, group, text: str, x: float, y: float, *, size: float = CODE_PT,
          fill: str = INK, struck: bool = False, anchor: str = "start") -> None:
    """One line of code; `struck` draws a line through it, as the inspector does.

    SVG collapses leading spaces, so indentation becomes an offset instead.
    """
    indent = len(text) - len(text.lstrip(" "))
    text = text.lstrip(" ")
    if anchor == "start":
        x += indent * size * MONO_W
    group.add(drawing.text(
        text, insert=(x, y), font_family=MONO, font_size=f"{size}px",
        fill=fill, text_anchor=anchor))
    if struck:
        width = len(text) * size * MONO_W
        group.add(drawing.line(
            start=(x - 1, y - size * 0.33), end=(x + width + 1, y - size * 0.33),
            stroke=fill, stroke_width=1.3))


def _arrow(drawing, group, start, end) -> None:
    """A plain line with a small filled head at `end`."""
    (x1, y1), (x2, y2) = start, end
    group.add(drawing.line(start=start, end=end, stroke=INK, stroke_width=1.4))
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    head, half = 8, 4
    base = (x2 - ux * head, y2 - uy * head)
    group.add(drawing.polygon(
        points=[(x2, y2),
                (base[0] - uy * half, base[1] + ux * half),
                (base[0] + uy * half, base[1] - ux * half)],
        fill=INK))


def _file(drawing, group, x: float, y: float, width: float, height: float, name: str) -> None:
    """A file: a sheet with its name in a band across the top."""
    group.add(drawing.rect(insert=(x, y), size=(width, height),
                           fill=PAPER, stroke=INK, stroke_width=1.4, rx=4))
    group.add(drawing.rect(insert=(x + 0.7, y + 0.7), size=(width - 1.4, 22),
                           fill=PANEL, stroke="none", rx=3))
    group.add(drawing.line(start=(x, y + 22.5), end=(x + width, y + 22.5),
                           stroke=RULE, stroke_width=1))
    group.add(drawing.text(name, insert=(x + 10, y + 15.5), font_family=MONO,
                           font_size=f"{LABEL_PT}px", font_weight="bold"))


def one_stylesheet_two_pages() -> str:
    """Two page files whose `<link>` tags both point at one stylesheet.

    The rule inside the stylesheet is the tutorial's own, read from its
    cell, so the picture shows the file the reader's rule would live in.
    """
    rule = _cell("a-rule-and-where-it-lives", "rule-css").strip().splitlines()

    margin, page_w, page_h, gap = 16, 230, 118, 40
    sheet_w, sheet_h = 250, 36 + len(rule) * 18
    width = margin * 2 + page_w * 2 + gap
    sheet_x = (width - sheet_w) / 2
    sheet_y = margin + page_h + 70
    height = sheet_y + sheet_h + margin
    drawing = _drawing(width, height)
    root = drawing.g()

    link = '<link rel="stylesheet"'
    href = '      href="styles.css">'
    for index, name in enumerate(["index.html", "about.html"]):
        x = margin + index * (page_w + gap)
        _file(drawing, root, x, margin, page_w, page_h, name)
        _code(drawing, root, "<head>", x + 12, margin + 44, fill=MUTED)
        root.add(drawing.rect(insert=(x + 20, margin + 52), size=(page_w - 30, 38),
                              fill=FILL_BLUE, stroke="none", rx=3))
        _code(drawing, root, link, x + 26, margin + 67)
        _code(drawing, root, href, x + 26, margin + 83)
        _code(drawing, root, "</head>", x + 12, margin + 108, fill=MUTED)
        start = (x + page_w / 2, margin + page_h + 4)
        end = (sheet_x + sheet_w * (0.3 if index == 0 else 0.7), sheet_y - 4)
        _arrow(drawing, root, start, end)

    _file(drawing, root, sheet_x, sheet_y, sheet_w, sheet_h, "styles.css")
    for index, line in enumerate(rule):
        _code(drawing, root, line, sheet_x + 14, sheet_y + 44 + index * 18)

    drawing.add(root)
    return drawing.tostring()


def one_variable_two_rules() -> str:
    """The variables example: one definition in `:root`, read by two boxes.

    The definition and the two boxes' words come from the tutorial's
    cells. Both boxes are drawn in the same solid ink, because the point
    is that they cannot differ: neither names a colour of its own.
    """
    css = _cell("variables-and-colour", "variables-css")
    html = _cell("variables-and-colour", "variables-html")
    value = _declaration(css, "--brand-color")
    labels = _elements(html, "div")
    reader = "background: var(--brand-color);"

    margin, gap = 16, 70
    root_w, root_h = 230, 74
    box_w, box_h = 290, 70
    width = margin * 2 + root_w + gap + box_w
    height = margin * 2 + box_h * 2 + 24
    drawing = _drawing(width, height)
    group = drawing.g()

    root_y = (height - root_h) / 2
    group.add(drawing.rect(insert=(margin, root_y), size=(root_w, root_h),
                           fill=FILL_AMBER, stroke=INK, stroke_width=1.4, rx=4))
    _code(drawing, group, ":root {", margin + 12, root_y + 22)
    _code(drawing, group, f"  --brand-color: {value};", margin + 12, root_y + 42)
    _code(drawing, group, "}", margin + 12, root_y + 62)

    box_x = margin + root_w + gap
    for index, label in enumerate(labels):
        y = margin + index * (box_h + 24)
        selector = f".{label.lower()}"
        group.add(drawing.rect(insert=(box_x, y), size=(box_w, box_h),
                               fill=INK, stroke="none", rx=4))
        group.add(drawing.text(label, insert=(box_x + 14, y + 24),
                               font_size=f"{LABEL_PT + 2}px", font_weight="bold", fill=PAPER))
        _code(drawing, group, selector, box_x + box_w - 12, y + 24,
              size=CODE_PT - 0.5, fill=PAPER, anchor="end")
        _code(drawing, group, reader, box_x + 14, y + 50, size=CODE_PT - 0.5, fill=PAPER)
        _arrow(drawing, group, (margin + root_w + 4, root_y + 38),
               (box_x - 6, y + box_h / 2))

    drawing.add(group)
    return drawing.tostring()


def px_and_rem() -> str:
    """The units example at a root size of 16px and of 40px, drawn to scale.

    The padding is tinted, and the only thing that changes between the
    two panels, apart from the text, is the tinted band of the rem box.
    The text grows in both boxes because neither sets a font size of its
    own; the tutorial says so, and the picture must not pretend otherwise.
    """
    css = _cell("text-and-units", "units-css")
    html = _cell("text-and-units", "units-html")
    names = _elements(html, "div")
    px_pad = float(_declaration(css.split(".box-px")[1], "padding").rstrip("px"))
    rem_pad = float(_declaration(css.split(".box-rem")[1], "padding").rstrip("rem"))

    margin, gap = 16, 44
    roots = [16, 40]
    panel_w = [220, 480]
    drawing_h = 0
    layouts = []
    for root, inner in zip(roots, panel_w):
        pads = [px_pad, rem_pad * root]
        heights = [p * 2 + root * 1.25 for p in pads]
        layouts.append((root, inner, pads, heights))
        drawing_h = max(drawing_h, sum(heights) + 8 + 30)
    width = margin * 2 + sum(panel_w) + gap
    height = margin + drawing_h + 56
    drawing = _drawing(width, height)
    group = drawing.g()

    x = margin
    for root, inner, pads, heights in layouts:
        y = margin
        for name, pad, box_h in zip(names, pads, heights):
            group.add(drawing.rect(insert=(x, y), size=(inner, box_h),
                                   fill=FILL_AMBER, stroke=INK, stroke_width=1))
            group.add(drawing.rect(insert=(x + pad, y + pad),
                                   size=(inner - pad * 2, box_h - pad * 2),
                                   fill=PAPER, stroke="none"))
            group.add(drawing.text(name, insert=(x + pad, y + pad + root * 0.95),
                                   font_size=f"{root}px"))
            group.add(drawing.text(f"{pad:.0f}px", insert=(x + inner - 4, y + pad / 2 + 4),
                                   text_anchor="end", font_size=f"{SMALL_PT}px",
                                   font_family=MONO, fill=INK))
            y += box_h + 8
        group.add(drawing.text(f"html {{ font-size: {root}px; }}",
                               insert=(x + inner / 2, margin + drawing_h + 14),
                               text_anchor="middle", font_family=MONO,
                               font_size=f"{LABEL_PT}px"))
        x += inner + gap

    group.add(drawing.rect(insert=(margin, height - 24), size=(14, 12),
                           fill=FILL_AMBER, stroke=INK, stroke_width=1))
    group.add(drawing.text("padding, with its size in pixels", insert=(margin + 20, height - 14),
                           font_size=f"{SMALL_PT}px", fill=MUTED))
    drawing.add(group)
    return drawing.tostring()


TEXT_ALIGN_WORDS = [5, 3, 7, 2, 6, 4, 8, 3, 5, 2, 7, 4, 3, 6, 5, 2, 4, 7, 3, 5, 6]


def text_align_values() -> str:
    """One paragraph, as bars for words, lined up four ways.

    Words are drawn as bars so that the edges of the lines are the only
    thing to look at. The lines are broken once and reused, so all four
    panels hold exactly the same lines; only where the lines sit changes.
    `justify` stretches the gaps on every line but the last.
    """
    unit, space, bar_h, line_gap = 7.0, 7.0, 9, 8
    col_w, margin, gap = 150, 16, 28
    lines: list[list[float]] = [[]]
    used = 0.0
    for letters in TEXT_ALIGN_WORDS:
        word = letters * unit
        extra = word if not lines[-1] else word + space
        if used + extra > col_w:
            lines.append([word])
            used = word
        else:
            lines[-1].append(word)
            used += extra

    values = ["left", "right", "center", "justify"]
    para_h = len(lines) * (bar_h + line_gap)
    width = margin * 2 + col_w * 4 + gap * 3
    height = margin + para_h + 40
    drawing = _drawing(width, height)
    group = drawing.g()

    for index, value in enumerate(values):
        x0 = margin + index * (col_w + gap)
        group.add(drawing.line(start=(x0 - 5, margin - 4), end=(x0 - 5, margin + para_h),
                               stroke=RULE, stroke_width=1))
        group.add(drawing.line(start=(x0 + col_w + 5, margin - 4),
                               end=(x0 + col_w + 5, margin + para_h),
                               stroke=RULE, stroke_width=1))
        for row, words in enumerate(lines):
            total = sum(words) + space * (len(words) - 1)
            gaps = space
            if value == "left":
                x = x0
            elif value == "right":
                x = x0 + col_w - total
            elif value == "center":
                x = x0 + (col_w - total) / 2
            else:
                x = x0
                if row < len(lines) - 1 and len(words) > 1:
                    gaps = (col_w - sum(words)) / (len(words) - 1)
            y = margin + row * (bar_h + line_gap)
            for word in words:
                group.add(drawing.rect(insert=(x, y), size=(word, bar_h),
                                       fill=FILL_BLUE, stroke=INK, stroke_width=0.8, rx=2))
                x += word + gaps
        group.add(drawing.text(f"text-align: {value}", insert=(x0 + col_w / 2, height - 12),
                               text_anchor="middle", font_family=MONO,
                               font_size=f"{LABEL_PT}px"))
    drawing.add(group)
    return drawing.tostring()


def descendant_tree() -> str:
    """The selectors example as a tree, with the one matched paragraph shaded.

    The words on the two paragraphs, and the class on the box, are read
    from the tutorial's cell. The path from the box down to the matched
    paragraph is drawn heavier, because that path is what the descendant
    selector checks: is there a `.highlight` somewhere above?
    """
    html = _cell("selectors-and-classes", "selectors-html")
    css = _cell("selectors-and-classes", "selectors-css")
    selector = css.strip().splitlines()[0].rstrip(" {")
    inside, outside = _elements(html, "p")
    box_class = re.search(r'<div class="([^"]+)"', html).group(1)

    margin = 16
    node_h = 30
    width, height = 560, 226
    drawing = _drawing(width, height)
    group = drawing.g()

    def node(cx: float, y: float, label: str, *, matched: bool = False, words: str = "") -> None:
        w = max(len(label) * CODE_PT * MONO_W + 24, 64)
        group.add(drawing.rect(insert=(cx - w / 2, y), size=(w, node_h),
                               fill=FILL_AMBER if matched else PAPER,
                               stroke=INK, stroke_width=1.8 if matched else 1.2, rx=4))
        _code(drawing, group, label, cx, y + 19, anchor="middle")
        if words:
            group.add(drawing.text(f"“{words}”", insert=(cx, y + node_h + 16),
                                   text_anchor="middle", font_size=f"{SMALL_PT}px", fill=MUTED))

    body = (width / 2, margin)
    div = (width * 0.3, margin + 70)
    p_out = (width * 0.72, margin + 70)
    p_in = (width * 0.3, margin + 150)

    group.add(drawing.line(start=(body[0], body[1] + node_h), end=(div[0], div[1]),
                           stroke=INK, stroke_width=1.2))
    group.add(drawing.line(start=(body[0], body[1] + node_h), end=(p_out[0], p_out[1]),
                           stroke=INK, stroke_width=1.2))
    group.add(drawing.line(start=(div[0], div[1] + node_h), end=(p_in[0], p_in[1]),
                           stroke=INK, stroke_width=3))

    node(*body, "body")
    node(*div, f'div class="{box_class}"')
    node(*p_out, "p", words=outside)
    node(*p_in, "p", matched=True, words=inside)

    group.add(drawing.text(f"matched by {selector}", insert=(p_in[0] + 50, p_in[1] + 19),
                           font_size=f"{LABEL_PT}px", font_weight="bold"))
    group.add(drawing.text(f"not matched: no .{box_class} above it",
                           insert=(p_out[0], p_out[1] + node_h + 34), text_anchor="middle",
                           font_size=f"{SMALL_PT}px", fill=INK))
    drawing.add(group)
    return drawing.tostring()


# What Chrome's Styles pane lists for a <p>, from its built-in stylesheet.
# Checked against Chromium 141 through the DevTools protocol
# (CSS.getMatchedStylesForNode); only the first three of its five
# declarations are drawn, to keep the picture small.
USER_AGENT_P = ["display: block;", "margin-block-start: 1em;", "margin-block-end: 1em;"]


def inspector_crossed_out() -> str:
    """The Styles pane for the boxed paragraph in "The cascade: which CSS rule wins".

    The two author rules come from the page's own cell, in the order the
    inspector lists them: the winner first. The losing `color` line is
    struck through. The built-in rule sits last, with its label on the
    right, as Chrome and Edge draw it.
    """
    css = _cell("which-rule-wins", "cascade-css")
    rules = re.findall(r"^([^{\n]+?)\s*\{\n(.*?)^\}", css, re.S | re.M)
    rules = [(sel.strip(), [d.strip() for d in body.strip().splitlines()]) for sel, body in rules]
    # Most specific first: the rule with a class in it wins.
    rules.sort(key=lambda rule: "." not in rule[0])
    winner_props = {decl.split(":")[0] for decl in rules[0][1]}

    margin, pane_w, line_h = 16, 380, 18
    blocks = rules + [("p", USER_AGENT_P)]
    height = margin + 34 + sum(line_h * (len(d) + 2) + 10 for _, d in blocks) + margin
    width = margin * 2 + pane_w
    drawing = _drawing(width, height)
    group = drawing.g()

    group.add(drawing.rect(insert=(margin, margin), size=(pane_w, height - margin * 2),
                           fill=PAPER, stroke=INK, stroke_width=1.4, rx=4))
    group.add(drawing.rect(insert=(margin + 0.7, margin + 0.7), size=(pane_w - 1.4, 26),
                           fill=PANEL, stroke="none", rx=3))
    group.add(drawing.text("Styles", insert=(margin + 12, margin + 18),
                           font_size=f"{LABEL_PT}px", font_weight="bold"))
    group.add(drawing.text("the paragraph in the box is selected",
                           insert=(margin + pane_w - 12, margin + 18), text_anchor="end",
                           font_size=f"{SMALL_PT}px", fill=MUTED))

    y = margin + 34
    for index, (selector, decls) in enumerate(blocks):
        built_in = index == len(blocks) - 1
        y += line_h
        _code(drawing, group, f"{selector} {{", margin + 12, y, fill=MUTED if built_in else INK)
        if built_in:
            group.add(drawing.text("user agent stylesheet", insert=(margin + pane_w - 12, y),
                                   text_anchor="end", font_size=f"{SMALL_PT}px",
                                   font_style="italic", fill=MUTED))
        for decl in decls:
            y += line_h
            lost = index > 0 and not built_in and decl.split(":")[0] in winner_props
            _code(drawing, group, decl, margin + 28, y,
                  fill=MUTED if built_in else INK, struck=lost)
            if lost:
                group.add(drawing.text("lost: the rule above wins",
                                       insert=(margin + pane_w - 12, y), text_anchor="end",
                                       font_size=f"{SMALL_PT}px", fill=MUTED))
        y += line_h
        _code(drawing, group, "}", margin + 12, y, fill=MUTED if built_in else INK)
        y += 10
        if index < len(blocks) - 1:
            group.add(drawing.line(start=(margin, y - 2), end=(margin + pane_w, y - 2),
                                   stroke=RULE, stroke_width=1))
    drawing.add(group)
    return drawing.tostring()


DIAGRAMS = {
    "a-rule-and-where-it-lives/one-stylesheet-two-pages.svg": one_stylesheet_two_pages,
    "variables-and-colour/one-variable-two-rules.svg": one_variable_two_rules,
    "text-and-units/px-and-rem.svg": px_and_rem,
    "text-and-units/text-align-values.svg": text_align_values,
    "selectors-and-classes/descendant-tree.svg": descendant_tree,
    "which-rule-wins/inspector-crossed-out.svg": inspector_crossed_out,
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
