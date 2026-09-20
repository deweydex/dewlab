"""Draw nested sets: rings inside rings, with examples placed where they live.

For the number domains, where the prose says "nested like Russian dolls" and
then writes the containment as a chain of symbols. The picture says the same
thing in a way a reader can point at: to answer "which families does −5
belong to", find −5 and read outwards.

Rounded rectangles rather than ellipses, because a label and its examples
have to sit side by side without the corners eating them, and because a
reader is meant to see boxes-within-boxes rather than a Venn diagram, where
overlapping would mean something these sets never do.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import svgwrite

from palette import INK, MONO, SANS

STEP_X = 26             # how far each ring insets from the one outside it
STEP_Y = 38   # room for a band of examples under each ring
LABEL_PT = 13
EXAMPLE_PT = 12
INNERMOST_W = 132
INNERMOST_H = 52


@dataclass
class Ring:
    """One set: its name, what to show living in it, and what it contains."""

    label: str
    examples: str
    inside: "Ring | None" = None
    note: str = ""


def _depth(ring: Ring) -> int:
    return 1 if ring.inside is None else 1 + _depth(ring.inside)


def render(outermost: Ring) -> str:
    levels = _depth(outermost)
    width = INNERMOST_W + STEP_X * 2 * (levels - 1)
    height = INNERMOST_H + STEP_Y * 2 * (levels - 1)
    margin = 16

    drawing = svgwrite.Drawing(
        size=(f"{width + margin * 2:.0f}px", f"{height + margin * 2:.0f}px"),
        viewBox=f"0 0 {width + margin * 2:.0f} {height + margin * 2:.0f}",
        debug=False)
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    group = drawing.g(transform=f"translate({margin},{margin})")

    ring, level = outermost, 0
    while ring is not None:
        inset_x, inset_y = STEP_X * level, STEP_Y * level
        w = width - inset_x * 2
        h = height - inset_y * 2
        group.add(drawing.rect(
            insert=(inset_x, inset_y), size=(w, h),
            # No ring is filled. A fill on the innermost one only shows up
            # as a notch where its own name masks the border, and position
            # already says which ring is innermost.
            fill="none",
            stroke=INK, stroke_width=1.6, rx=12))
        # The name sits on the ring's own top edge, with the page behind it,
        # so it reads as belonging to that boundary and not to the one
        # outside it.
        name_x = inset_x + 22
        label_width = len(ring.label) * LABEL_PT * 0.7 + 12
        group.add(drawing.rect(
            insert=(name_x - 6, inset_y - 10), size=(label_width, 20),
            fill="var(--dl-bg)", stroke="none"))
        group.add(drawing.text(
            ring.label, insert=(name_x, inset_y + 5),
            font_size=f"{LABEL_PT}px", font_weight="bold", fill=INK))
        # Examples go in the band below the next ring in, not above it.
        # Above, they collide with that ring's own name sitting on its top
        # edge; below, they fill the band that would otherwise be empty, and
        # they are still inside this ring and outside the next — which is
        # exactly the region that means "this kind of number and no smaller
        # kind".
        group.add(drawing.text(
            ring.examples,
            insert=(inset_x + w / 2, inset_y + (h / 2 + 5 if ring.inside is None
                                                else h - STEP_Y + 22)),
            text_anchor="middle", font_size=f"{EXAMPLE_PT}px",
            font_family=MONO, fill=INK))
        ring, level = ring.inside, level + 1

    drawing.add(group)
    return drawing.tostring()
