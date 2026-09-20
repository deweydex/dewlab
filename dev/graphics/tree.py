"""Draw a tree: nodes on levels, each joined to what it leads to.

Three tutorials want one — a folder that contains folders, a recursion that
asks smaller versions of its own question, a probability that branches. They
differ in what the nodes say and what the edges carry, not in shape, so they
share a layout: each level is a row, children sit under their parent, and a
node is as wide as its own label.

Layout is the tidy-tree rule, in its simple form. A leaf takes the next free
column; a parent centres over the children it has. That is enough for a tree
a reader can hold in their head, which is the only size worth drawing.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import svgwrite

from palette import FILL_AMBER, INK, MONO, MUTED, PANEL, RULE, SANS

NODE_H = 28
LEVEL_GAP = 52          # vertical room, which the edge labels sit in
SIBLING_GAP = 26   # room for an edge label between two subtrees
PAD_X = 12
LABEL_PT = 11.5
EDGE_PT = 9.5


@dataclass
class Node:
    """One node, and what hangs below it.

    `note` is a second line inside the box — what a folder holds, say.
    `edge` labels the line arriving from this node's parent, which is where
    a probability lives. `marked` draws attention to the node: the repeated
    subtree in a recursion, the one a reader is meant to notice twice.
    """

    label: str
    children: list["Node"] = field(default_factory=list)
    note: str = ""
    edge: str = ""
    marked: bool = False


def _width_of(text: str, point_size: float) -> float:
    return len(text) * point_size * 0.62


def _measure(node: Node) -> float:
    own = max(
        _width_of(node.label, LABEL_PT),
        _width_of(node.note, EDGE_PT) if node.note else 0,
    ) + PAD_X * 2
    node.box_width = own                                    # type: ignore[attr-defined]
    if not node.children:
        node.span = own                                     # type: ignore[attr-defined]
        return own
    below = sum(_measure(child) for child in node.children)
    below += SIBLING_GAP * (len(node.children) - 1)
    node.span = max(own, below)                             # type: ignore[attr-defined]
    return node.span                                        # type: ignore[attr-defined]


def _place(node: Node, left: float, depth: int, placed: list) -> None:
    if node.children:
        cursor = left + (node.span - (                      # type: ignore[attr-defined]
            sum(c.span for c in node.children)              # type: ignore[attr-defined]
            + SIBLING_GAP * (len(node.children) - 1))) / 2
        for child in node.children:
            _place(child, cursor, depth + 1, placed)
            cursor += child.span + SIBLING_GAP              # type: ignore[attr-defined]
        first, last = node.children[0], node.children[-1]
        centre = (first.centre + last.centre) / 2           # type: ignore[attr-defined]
    else:
        centre = left + node.span / 2                       # type: ignore[attr-defined]
    node.centre = centre                                    # type: ignore[attr-defined]
    node.top = depth * (NODE_H + LEVEL_GAP)                 # type: ignore[attr-defined]
    placed.append(node)


def render(root: Node, note_style: str = "plain") -> str:
    _measure(root)
    placed: list[Node] = []
    _place(root, 0.0, 0, placed)

    margin = 16
    width = max(n.centre + n.box_width / 2 for n in placed) + margin * 2
    height = max(n.top for n in placed) + NODE_H + margin * 2
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}",
        debug=False,
    )
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    group = drawing.g(transform=f"translate({margin},{margin})")

    for node in placed:
        for child in node.children:
            start = (node.centre, node.top + NODE_H)
            end = (child.centre, child.top)
            group.add(drawing.line(
                start=start, end=end, stroke=INK, stroke_width=1.5,
                stroke_linecap="round"))
            if child.edge:
                # Set on the line, with the page behind it, so a label never
                # has to compete with what it is labelling.
                mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
                group.add(drawing.rect(
                    insert=(mid[0] - _width_of(child.edge, EDGE_PT) / 2 - 3, mid[1] - 8),
                    size=(_width_of(child.edge, EDGE_PT) + 6, 15),
                    fill=PANEL, stroke=RULE, stroke_width=0.8, rx=3))
                group.add(drawing.text(
                    child.edge, insert=(mid[0], mid[1] + 3.5), text_anchor="middle",
                    font_size=f"{EDGE_PT}px", fill=MUTED))

    for node in placed:
        left = node.centre - node.box_width / 2
        group.add(drawing.rect(
            insert=(left, node.top), size=(node.box_width, NODE_H),
            fill=FILL_AMBER if node.marked else PANEL,
            stroke=INK, stroke_width=1.8 if node.marked else 1.3, rx=5))
        baseline = node.top + (NODE_H / 2 + 4 if not node.note else NODE_H / 2 - 1)
        group.add(drawing.text(
            node.label, insert=(node.centre, baseline), text_anchor="middle",
            font_size=f"{LABEL_PT}px",
            font_family=MONO if note_style == "code" else SANS, fill=INK))
        if node.note:
            group.add(drawing.text(
                node.note, insert=(node.centre, node.top + NODE_H / 2 + 10),
                text_anchor="middle", font_size=f"{EDGE_PT}px", fill=MUTED))

    drawing.add(group)
    return drawing.tostring()
