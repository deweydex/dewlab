# Design canvases

Source for the visual design canvases published alongside dewlab's planning
documents. One folder per canvas.

Each folder holds the artboards (`*.dc.html`, one file per frame) and a
`canvas.json` laying them out. **These are the editable source** — a later
change edits them and rebuilds the canvas from them. The assembled
single-file page is *not* kept here: it embeds a copy of the canvas editor,
runs to about 2.5 MB, and is regenerated rather than stored (see
`.gitignore`).

They are built with Claude Code's `design` skill, whose seed step assembles
the artboards into the published page. Nothing in dewlab's own build reads
this directory — `build.py` never looks at it, and it ships nothing to
`site/`.

## notebook-to-program

Six artboards illustrating the "path from notebook to program" argument in
`planning/DATABASE_MODULE_AND_BIGGER_IDEAS.md` §6.1: what a student's
notebook looks like today, the failure they hit when they try to turn it
into a program on their own, and the proposed extract-to-function flow.

`Main.dc.html` is the overview — the same code at three stages, showing what
moves and what holds it together. The other five read left to right as a
sequence: `Today`, `TheCliff`, `Extract`, `AfterExtract`, `RunProject`.

Static mockups, not a working prototype. The marks data is sample data, kept
consistent across every frame (an average of 71.2, banded as a Distinction)
so the numbers can be followed from screen to screen.

Colours, type and control shapes are lifted from `compose/dewmini-style.css`
and `assets/tutorial-style.css` rather than invented — Georgia body, navy
`#1b2a4a`, orange `#d4692a`, cell fill `#f6f4f0`, the mono stack at 15px. If
those tokens change, these frames will drift and want re-checking against
the real thing.
