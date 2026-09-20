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
