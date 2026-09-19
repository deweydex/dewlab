# Fixed choices

Constraints a contributor could otherwise reasonably assume don't hold.
Everything else about how dewlab works is visible in the code itself.

- **No package beyond numpy, pandas, matplotlib for a tutorial page.**
  All three ship as official Pyodide packages, no micropip step. dewmini
  (`compose/`) carries a wider default — sqlite3 and Pillow too — without
  changing this baseline for tutorial pages.
- **CSV only, never Excel.** `load_csv` has no Excel counterpart; add one
  only if a specific tutorial genuinely needs it.
- **Nothing is ever scored, submitted, or recorded.** `check()` is
  formative feedback in the cell's own output, unrelated to any grade.
  This is a constraint on every future feature, not a fact about the
  current ones.

## Assumed, not settled — flag if wrong

- scipy stays out unless a tutorial needs distributions or stats beyond
  pandas/numpy. Adding it later is a one-line change.
- The editor's code-output preview renders through `build.py`, not a
  live Pyodide pane in the editor itself.
- Live, IDE-style hover documentation (real docstrings pulled from a
  running Pyodide session) is plausible future work, not a gap in
  what's built now.
