---
name: cell-code-review
description: Review a dewlab tutorial's Python code — every exec cell and every illustrative (untagged) code fence — for pedagogical code quality against PEDAGOGICAL_STYLE_GUIDE.md §5: semantic variable names over mathy single letters, comments that explain why rather than restate what, in context (surrounding prose, earlier cells in the same tutorial, whether naming is deliberately withheld as a "discover first" moment, whether a cell is a stub with nothing to name). Use when asked to review, clean up, or improve code quality/naming/comments in one or more tutorials' cells, or after writing new tutorial code that should be checked before it ships.
---

# Reviewing a tutorial's cell code

This is not the glossary skill. `.claude/skills/tutorial-glossary/SKILL.md`
asks "what does this tutorial teach"; this asks "is the code itself, that a
reader is looking at right now, written the way `PEDAGOGICAL_STYLE_GUIDE.md`
§5 says dewlab's code should be written." Read that section first — it has
the actual rules (semantic names, why-not-what comments, the "discover
first" exception, stub cells needing nothing) and the reasoning behind
each one; this file is the process for applying them to one tutorial.

**The one rule that matters more than any naming preference below: never
change what a cell does.** A rename is only ever a rename — the same
imports, the same structure, the same output, the same values. If making a
name clearer would require restructuring the logic, that is not this
skill's job; note it and move on rather than rewriting more than was
asked.

## What you need before you start

1. **The tutorial itself**, read whole — `tutorials/<module>/<slug>.md` or
   `tutorials/<module>/<slug>/<slug>.md` for a tutorial with releases. Not
   just the cells: the prose is what tells a mathy `a`/`b`/`c` apart from a
   `t` that should be `elapsed_time`.
2. **Every cell in it, in document order** — both `exec` cells (parsed the
   same way `build.py`'s `parse_cell()` does: an `id:` line, an optional
   `hint:` line, then code) and untagged fences (illustrative, read-only,
   no `id:`). Both get reviewed; only `exec` cells carry an `id:` you must
   preserve exactly.
3. If the tutorial has `practice_for:`/`practice_across:` in its
   frontmatter, it is still a real tutorial with real cells — review it
   the same way. It just is not part of a series' reading order, which is
   irrelevant here.

## Reading for context, before touching anything

Three things you need to know about a name or a missing comment before
deciding it is a problem:

**What does the prose around this cell already say?** A variable named
`a`/`b`/`c` right under a paragraph deriving the quadratic formula with
those same letters is matching the page, not failing to name itself —
`PEDAGOGICAL_STYLE_GUIDE.md`'s one named exception. A `t` under a
paragraph about elapsed time is not the same case at all.

**Is this a "discover first, name afterwards" moment?** Read forward, not
just at the cell itself — does the tutorial's own prose, shortly after
this cell, introduce a term the code is building toward? If so, a generic
name here (`state`, `result`, `total`) is doing its job correctly by not
saying the specific word before the prose does; a rename to the more
specific name would spoil the reveal the tutorial is deliberately setting
up. When genuinely unsure whether a generic name is a discovery moment or
just underspecified, read to the end of that section before deciding —
the answer is usually settled within a paragraph or two.

**Does an earlier cell in this same tutorial already use this name?** A
tutorial's cells share one namespace in document order — renaming `n` to
`count` in one cell without renaming every later cell that reads `n` back
would break the tutorial, not improve it. Read every cell first, note
which names are established and reused across cells, and treat a rename
as a whole-tutorial operation for any name that appears in more than one
cell — not a per-cell one.

**Is there anything to review at all?** A stub cell (`# Your code here.`,
`# Your investigation here.`) has no variable to rename and nothing to
comment — leave it alone. An illustrative fence that is genuinely
pseudocode, not real Python (rare, but it happens — check the fence's own
language tag and whether it would actually parse), is not held to Python
naming conventions at all; note it as pseudocode rather than flagging
names that were never meant to be identifiers.

## Deciding what to change

For each cell, having read the above:

- **A single-letter or abbreviated name with nothing earning its
  brevity** (not `i`/`j` in a loop, not `x`/`y` for a coordinate, not a
  formula's own letters matching the prose above it) — propose a semantic
  replacement, applied consistently everywhere that name appears in this
  cell and every later cell in the tutorial that shares it.
- **A comment that restates what the line already says** (`# add one to
  count` on `count += 1`) — either remove it, if the line is now
  self-explanatory with a clearer name, or replace it with one that says
  why this step matters, if there is a real "why" worth having. Do not
  add a comment where none is needed just to have commented the cell.
- **A cell with no comments where one would genuinely help** — a
  non-obvious step, a choice a reader might question, something the
  prose around the cell does not already explain. Propose one short
  comment, in the tutorial's own voice (`PEDAGOGICAL_STYLE_GUIDE.md` §4:
  plain, warm, no condescension) — not a comment for every line.
- **Anything that looks wrong but is a deliberate "discover first" name,
  a formula-matching letter, a stub, or pseudocode** — leave it, and say
  why in your report, so whoever reads it does not wonder whether it was
  simply missed.

## Making the change

Edit the `.md` source directly, inside the fence, leaving `id:`/`hint:`
header lines exactly as they were — a cell's `id` is a contract
(`PEDAGOGICAL_STYLE_GUIDE.md` §5: "the key somebody's saved work lives
under"), never touch it as part of a naming cleanup. After editing a
tutorial's cells:

1. **Every edited cell still has to be valid Python.** At minimum,
   `python3 -c "compile(open('cell.py').read(), 'cell', 'exec')"` on the
   cell's code (or the equivalent read straight from the fence) — a typo
   introduced while renaming is worse than the problem being fixed.
2. **Rebuild the tutorial** (`python3 -c "import build as b;
   b.build(clean=True)"`) and confirm it still builds clean — a broken
   `id:` line or a fence indentation slip fails loudly here.
3. Where you can run the actual cells (a real Pyodide, or by hand
   reasoning through pure-Python logic with no dependency on
   `tutorial_tools`' page-namespace bridge), confirm the renamed version
   produces the same output as before the edit — a rename that silently
   changes behaviour (shadowing an existing name, for instance) is the
   one mistake this whole process exists to avoid.

## What to report

Per tutorial: what changed and why, in enough detail that someone who has
not read the tutorial can see the reasoning (not just "renamed `n` to
`count`" — "renamed `n` to `count` in `first-run` and `second-run`, which
both use it for the same running total"), and what was deliberately left
alone and why (the discovery-moment names, the formula-matching letters,
the stub cells) — so a second pass over the same tutorial does not
re-litigate a decision already made on purpose. Flag, rather than
silently fix, anything you are not confident about — a rename you are
unsure would change behaviour, or a cell where the "right" name depends
on something outside the tutorial itself.
