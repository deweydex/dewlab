"""Draw a state diagram: states, and the labelled arrows between them.

The standard picture of a Markov chain, and the thing a transition matrix
is when you write it down as a shape instead of a grid. Putting the two
side by side is the point — the rows of the matrix are the arrows leaving
each state, and a row summing to one is every arrow out of a state summing
to one.

Two things it has to get right to be that picture rather than a sketch. A
state's arrow back to itself is drawn, not left out: it is a row entry like
any other, and dropping it would make the row look as though it did not sum
to one. And the two directions between a pair are drawn as separate curved
arcs, because one line with two arrowheads cannot carry two probabilities.
"""

from __future__ import annotations

import math

import svgwrite

from palette import INK, MUTED, PANEL, RULE, SANS

RADIUS = 44
SPACING = 210           # centre to centre
LOOP_R = 27
LABEL_PT = 11
STATE_PT = 13
ARROW = 7.5


def _arrowhead(drawing, group, tip, angle, size: float = ARROW) -> None:
    """A filled head, so direction reads at a glance and at a distance."""
    spread = math.radians(26)
    points = [
        tip,
        (tip[0] - size * math.cos(angle - spread), tip[1] - size * math.sin(angle - spread)),
        (tip[0] - size * math.cos(angle + spread), tip[1] - size * math.sin(angle + spread)),
    ]
    group.add(drawing.polygon(points=points, fill=INK, stroke="none"))


def _chip(drawing, group, text, x, y) -> None:
    """A probability, set on the page rather than on the line it labels."""
    width = len(text) * LABEL_PT * 0.62 + 10
    group.add(drawing.rect(
        insert=(x - width / 2, y - 9), size=(width, 18),
        fill=PANEL, stroke=RULE, stroke_width=0.8, rx=4))
    group.add(drawing.text(
        text, insert=(x, y + 4), text_anchor="middle",
        font_size=f"{LABEL_PT}px", fill=INK))


def render(states: list[str], matrix: list[list[float]], fmt=lambda p: f"{p:g}") -> str:
    """`matrix[i][j]` is the chance of moving from `states[i]` to `states[j]`."""
    if len(states) != 2:
        raise ValueError("two states for now; more needs a layout that spreads them")

    margin = 18
    width = SPACING + RADIUS * 2 + margin * 2
    # The loops rise above the states and nothing hangs below them, so the
    # room they need is added at the top only.
    height = RADIUS * 2 + LOOP_R + 12 + margin * 2
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}", debug=False)
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    group = drawing.g(transform=f"translate({margin},{margin + LOOP_R + 12})")

    centres = [(RADIUS, RADIUS), (RADIUS + SPACING, RADIUS)]

    # Between the two states: one arc each way, bowed in opposite directions
    # so neither label has to share space with the other's line.
    for source, target, bow in ((0, 1, -1), (1, 0, 1)):
        probability = matrix[source][target]
        if not probability:
            continue
        start = centres[source]
        end = centres[target]
        direction = 1 if end[0] > start[0] else -1
        from_edge = (start[0] + direction * RADIUS, start[1])
        to_edge = (end[0] - direction * RADIUS, end[1])
        lift = 46 * bow
        control = ((from_edge[0] + to_edge[0]) / 2,
                   (from_edge[1] + to_edge[1]) / 2 + lift)
        group.add(drawing.path(
            d=f"M {from_edge[0]},{from_edge[1]} Q {control[0]},{control[1]} "
              f"{to_edge[0]},{to_edge[1]}",
            fill="none", stroke=INK, stroke_width=1.7))
        # The tangent at the end of a quadratic curve points from the control
        # point at the endpoint, which is the direction the head must face.
        angle = math.atan2(to_edge[1] - control[1], to_edge[0] - control[0])
        _arrowhead(drawing, group, to_edge, angle)
        _chip(drawing, group, fmt(probability),
              (from_edge[0] + to_edge[0]) / 2, (from_edge[1] + to_edge[1]) / 2 + lift * 0.62)

    # Staying put: a loop above the state, which is a row entry like any other.
    for index, centre in enumerate(centres):
        probability = matrix[index][index]
        if not probability:
            continue
        top = (centre[0], centre[1] - RADIUS)
        group.add(drawing.path(
            d=f"M {top[0] - 15},{top[1] - 4} "
              f"C {top[0] - 34},{top[1] - LOOP_R * 2} "
              f"{top[0] + 34},{top[1] - LOOP_R * 2} "
              f"{top[0] + 15},{top[1] - 4}",
            fill="none", stroke=INK, stroke_width=1.7))
        _arrowhead(drawing, group, (top[0] + 15, top[1] - 4), math.radians(70))
        _chip(drawing, group, fmt(probability), top[0], top[1] - LOOP_R - 10)

    for centre, name in zip(centres, states):
        group.add(drawing.circle(
            center=centre, r=RADIUS, fill=PANEL, stroke=INK, stroke_width=1.8))
        group.add(drawing.text(
            name, insert=(centre[0], centre[1] + 5), text_anchor="middle",
            font_size=f"{STATE_PT}px", fill=INK))

    drawing.add(group)
    return drawing.tostring()
