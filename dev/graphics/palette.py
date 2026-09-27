"""The colours a generated diagram is allowed to use.

Every value here is a CSS custom property from `assets/tutorial-style.css`,
written straight into the SVG rather than as a hex literal that
`dev/normalise_svg.py` would have to map back. svgwrite passes them through
untouched once its validator is off (`Drawing(debug=False)`), so a generated
diagram needs no normalising pass at all — that tool's job is a contributor's
draw.io export, which cannot name a token.

Two families, and the split matters. `INK`/`MUTED`/`RULE` are for strokes and
text, and resolve to colours tuned to stay legible against the page in light,
dark and both high-contrast modes. `FILL_*` are for areas, and resolve to the
highlight tints, which were chosen to sit behind body text without shouting.
"""

INK = "currentColor"          # follows --dl-fg, so theme and contrast are free
MUTED = "var(--dl-muted)"     # secondary text: a column's type
RULE = "var(--dl-rule)"       # a hairline between rows
PANEL = "var(--dl-cell-bg)"   # a table's header band
PAPER = "var(--dl-bg)"        # masking, where something must hide what is under it

FILL_AMBER = "var(--dl-highlight-bg)"
FILL_GREEN = "var(--dl-highlight-green)"
FILL_BLUE = "var(--dl-highlight-blue)"
FILL_PINK = "var(--dl-highlight-pink)"

MONO = "'SF Mono', 'Cascadia Mono', Menlo, Consolas, monospace"
SANS = "'Helvetica Neue', Inter, system-ui, sans-serif"


# Patterns for readers who cannot tell the tints apart (DECISIONS_LOG 7.279).
#
# A tinted area keeps its tint. `add_patterns()` lays a copy of it on top,
# filled with stripes, and gives the copy the class `dl-pattern`. The
# stylesheet hides that class unless the reader turns on "Patterns in
# pictures" or high contrast, so a picture looks the same as before for
# everyone else. Each tint has its own pattern, so a part can be named by
# its pattern as well as its colour.
PATTERN_FOR = {
    FILL_AMBER: "stripes",        # stripes one way: /
    FILL_BLUE: "back-stripes",    # stripes the other way: \
    FILL_GREEN: "cross",          # both: where amber columns cross blue rows
    FILL_PINK: "dots",
}

_PATTERN_BODY = {
    "stripes": ('patternTransform="rotate(45)"',
                '<line x1="0" y1="0" x2="0" y2="7" stroke="currentColor" stroke-width="1.6"/>'),
    "back-stripes": ('patternTransform="rotate(-45)"',
                     '<line x1="0" y1="0" x2="0" y2="7" stroke="currentColor" stroke-width="1.6"/>'),
    "cross": ('patternTransform="rotate(45)"',
              '<line x1="0" y1="0" x2="0" y2="7" stroke="currentColor" stroke-width="1.4"/>'
              '<line x1="0" y1="0" x2="7" y2="0" stroke="currentColor" stroke-width="1.4"/>'),
    "dots": ("", '<circle cx="3.5" cy="3.5" r="1.3" fill="currentColor"/>'),
}

# Anything smaller than this, a bead or a dot on a line, is too small to
# carry a pattern; its tint stays as it is.
_SMALLEST_PATTERNED = 9


def add_patterns(svg: str, prefix: str) -> str:
    """Return `svg` with a hidden pattern layer over each tinted area.

    `prefix` makes the pattern ids unique to one picture, so two pictures
    on one page never share an id. The layer copies each tinted shape
    (rect, path, polygon, and circles big enough to hold a pattern), fills
    the copy with its tint's pattern, and marks it `dl-pattern` and
    `aria-hidden`: it repeats what the shape under it already says.
    """
    import re
    shape_re = re.compile(r'<(rect|path|polygon|circle)\b([^>]*?)(/?)>')
    used: set[str] = set()

    def overlay(match: re.Match) -> str:
        tag, attrs, closing = match.group(1), match.group(2), match.group(3)
        fill = re.search(r'\sfill="([^"]*)"', attrs)
        if not fill or fill.group(1) not in PATTERN_FOR:
            return match.group(0)
        if tag == "circle":
            radius = re.search(r'\sr="([^"]*)"', attrs)
            if not radius or float(radius.group(1)) < _SMALLEST_PATTERNED:
                return match.group(0)
        kind = PATTERN_FOR[fill.group(1)]
        used.add(kind)
        copy = re.sub(r'\s(fill|stroke|stroke-width|stroke-dasharray)="[^"]*"', "", attrs)
        copy += f' fill="url(#{prefix}-{kind})" stroke="none" class="dl-pattern" aria-hidden="true"'
        whole = match.group(0)
        if closing:
            return whole + f"<{tag}{copy}/>"
        return whole  # an open tag with children is not a shape this draws
    patterned = shape_re.sub(overlay, svg)
    if not used:
        return svg
    defs = "".join(
        f'<pattern id="{prefix}-{kind}" width="7" height="7" patternUnits="userSpaceOnUse" '
        f'{_PATTERN_BODY[kind][0]}>{_PATTERN_BODY[kind][1]}</pattern>'
        for kind in sorted(used)
    )
    opening_end = patterned.index(">", patterned.index("<svg")) + 1
    return patterned[:opening_end] + f'<defs class="dl-pattern-defs">{defs}</defs>' + patterned[opening_end:]
