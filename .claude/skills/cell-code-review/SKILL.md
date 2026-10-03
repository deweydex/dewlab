---
name: cell-code-review
description: "Review a dewlab tutorial's Python code — every exec cell and every illustrative (untagged) code fence — for pedagogical code quality against PEDAGOGICAL_STYLE_GUIDE.md#code: semantic variable names over mathy single letters, and comments that explain why rather than restate what, judged in context (the surrounding prose, earlier cells, deliberate \"discover first\" names, stub cells). Use when asked to review or improve naming or comments in tutorial cells, or after writing new tutorial code."
---

# Reviewing a tutorial's cell code

This applies `PEDAGOGICAL_STYLE_GUIDE.md#code` to one tutorial. Read that section first; it has the rules and their reasons. This skill is only the process. (What a tutorial teaches is the glossary skill's question, not this one's.)

**Never change what a cell does.** A rename is only a rename: same imports, structure, output and values. If a clearer name would need restructuring, note it and move on.

## Read before touching anything

Read the whole tutorial, `tutorials/<id>/<id>.md`, and every cell in document order: `exec` cells (an `id:` line, an optional `hint:`, then code, as `parse_cell()` in `build.py` reads them) and untagged illustrative fences, which have no `id:`. Practice and context pages (`practice_for:`, `practice_across:`, `context_for:`) get the same review.

Cells share one namespace in document order. A name used in more than one cell is renamed across the whole tutorial or not at all.

## Leave alone, and say why in the report

- **Names that match the prose**, such as `a`, `b`, `c` under a paragraph deriving the quadratic formula with those letters. (`t` under a paragraph about elapsed time is a different case.) `i`, `j` and `x`, `y` need no defence.
- **Discover-first names.** A generic name (`state`, `result`, `total`) is correct if the prose soon introduces the specific term, because renaming would spoil the reveal. Read to the end of the section before deciding; it is usually clear within a paragraph or two.
- **Stub cells** (`# Your code here.`), which have nothing to name.
- **Pseudocode fences** that would not parse as Python.

## Change

- **A single-letter or abbreviated name with nothing earning its brevity:** a semantic replacement, applied in this cell and every later cell that shares the name.
- **A comment that restates its line:** remove it, or replace it with the reason if there is a real one.
- **A non-obvious step or questionable choice the prose does not explain:** one short comment in the tutorial's voice (`#voice`), never one per line.

## Edit and verify

Edit the `.md` inside the fence. Leave `id:` and `hint:` lines exactly as they were; an id is the key students' saved work lives under (`docs/WRITING_TUTORIALS.md#cell-ids`). Then:

1. Check each edited cell still compiles: `compile(code, 'cell', 'exec')`.
2. Run `python3 build.py --clean`. A broken `id:` line or fence indentation fails here.
3. Where you can run the cells without the page-namespace bridge, confirm the output matches the original. A silent change, such as a new name shadowing an existing one, is the mistake this review exists to prevent.

## Report

Per tutorial, say what changed and why, naming the cells ("renamed `n` to `count` in `first-run` and `second-run`, which both use it for one running total"). Say what you left alone and why, so a second pass does not re-decide it. Flag anything you suspect would change behaviour, or whose right name depends on something outside the tutorial.
