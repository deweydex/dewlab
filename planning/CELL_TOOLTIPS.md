# Tooltips in a student's cell: what exists, what is missing, what is out there

Research note, built in full — DECISIONS_LOG.md 7.76: (a), (b), and (c) all
shipped together rather than staged, once prototyping against the real
pinned Pyodide showed (c)'s pre-run answer genuinely worked and removed the
open question §4 left about whether it was worth its cost. Written in
response to "let's see what libraries exist to provide tooltips that we
might use in the cells for students."

---

## 1. What is already there

This is not starting from zero. `DECISIONS_LOG.md` 7.60 and
`assets/tutorial-runtime.js` already wire up two layers, both real:

- **Static, no interpreter needed.** `@codemirror/lang-python`'s
  `globalCompletion`/`localCompletionSource` (keywords, builtins by name,
  locally-typed identifiers) — already vendored for close-brackets and
  syntax highlighting, so this was close to free.
- **Live, from the actual interpreter.** `pageNamesCompletion` and `docFor`
  read `tutorial_tools._page_globals` — the exact dict a cell executes
  against — and call Pyodide's own `inspect.getdoc()` on a real object
  sitting in it, surfaced through CodeMirror's `hoverTooltip()` extension.
  Accurate by construction: there is nothing bundled to fall out of sync
  with the interpreter a student is actually running.

So "is there a Pyodide-flavoured way to do this" already has a working
answer for one big piece of the problem: a name the student defined or
imported, hovered after the cell that defines it has run.

## 2. What that leaves uncovered

Three real gaps, all noted or implied where `docFor` is defined:

1. **Builtins.** `docFor`'s own comment says this outright: `print`, `len`,
   `range` and the rest are deliberately out of scope — they are not in
   `_page_globals`, and reaching into `__builtins__` too "was a bigger
   surface than this needed for a first pass." A beginner is at least as
   likely to want to know what `len()` does as what their own function
   does.
2. **Before the cell has run.** `docFor` looks an existing name up in a live
   namespace. A student who has typed `def average(numbers):` but not yet
   run the cell gets nothing on hover, because that name does not exist
   anywhere yet.
3. **Signature help while typing a call.** Seeing `average(` and getting a
   parameter hint (`average(numbers)`) as you type the open paren is a
   different UI moment than hovering a name that is already there, and nothing
   currently offers it.

## 3. What is out there, and what it would cost

### (a) Widen `docFor` to also check `__builtins__`

Not a library — the same function, one more lookup. `inspect.getdoc(print)`
works exactly the way `inspect.getdoc()` on a student's own function
already does; Pyodide's interpreter has `__builtins__` sitting right there
whether or not a cell has run. Closes gap 1 entirely, for every builtin,
with no new dependency and no bundle-size cost.

*Cost: small — a few lines in `docFor`, covered by the same style of test
`tests/e2e/test_autocomplete.py` already uses.*

### (b) Signature help on typing `(`, from `inspect.signature()`

Also not a library. The same live interpreter that answers `docFor`
already has `inspect.signature(obj)`, which is exactly what a parameter
hint needs. The missing piece is entirely on the CodeMirror side: a second
`hoverTooltip`-shaped extension (or the same one, retriggered) that fires on
typing `(` rather than on mouse hover, positioned at the cursor instead of
under the pointer. Confirmed by checking CodeMirror's own discussion forum:
`@codemirror/autocomplete` has no built-in signature-help feature for any
language, and the documented way to add one *is* a custom tooltip extension
— exactly the shape `codemirror-entry.js` already has a working, tested
example of for hover docs.

*Cost: moderate — new UI logic (trigger-on-paren rather than trigger-on-hover,
tracking which argument index the cursor is in for bolding), but the data
source and the rendering primitive are both already proven in this codebase.
Still covers only names that already exist in the running interpreter, same
as `docFor` — gap 2 remains.*

### (c) Jedi, run inside Pyodide itself, for static (pre-run) completion and hover

This is the real answer to "I bet there are things we can use with Pyodide
out there." Jedi — the autocompletion/static-analysis library most Python
IDEs are built on — is pure Python (so is its parser, `parso`), both have
wheels on PyPI, and **both are already in Pyodide's own package index**:
they used to be vendored into Pyodide's core distribution outright, and were
split out into optional packages specifically to keep the core download
smaller — not because they stopped working in a WASM interpreter. More
concretely: **JupyterLite's own official Pyodide kernel uses Jedi for its
code completion**, in production, in exactly this browser-plus-WASM-Python
setup. This is not a hypothetical combination; it is one already running in
a well-known project built on the same interpreter dewlab uses.

What Jedi buys, that (a) and (b) do not: completion and hover **before**
a cell has ever run, because Jedi parses the source text itself rather than
inspecting a live namespace — so it also has answers for stdlib and
third-party names your code hasn't executed yet, not just builtins already
sitting in `__builtins__`.

What it costs: a real new dependency, loaded on every page with a cell
regardless of whether the tutorial needs it — `micropip.install("jedi")`
downloads both jedi and parso, which is why they were pulled out of
Pyodide's own core (a project that cares enough about download size to have
done that split). It is also a second source of truth for documentation
running alongside the first: Jedi's answer for a name the student *has*
already defined would need reconciling with (or replacing) what `docFor`'s
live `inspect.getdoc()` already gives correctly today, and the two working
side by side is more moving parts than either alone.

*Cost: real — a second, heavier mechanism, not a small addition, and it
substantially overlaps in value with what (a) already closes for free.
Worth doing only if "before the cell has run" turns out to matter enough
on its own to justify it; not needed to close the builtins gap, which (a)
closes without it.*

### (d) Ruled out without a prototype

- **A full language server (`python-lsp-server`, Pyright) behind a CodeMirror
  LSP client.** CodeMirror 6 has no built-in LSP client; one exists as a
  separate package, but pairing it with a real language server means either
  running one in a Web Worker (heavy — Pyright itself is a multi-megabyte
  TypeScript codebase, and there is no evidence of anyone running the
  Python-specific `pylsp` compiled for the browser) or a server round-trip
  dewlab's whole architecture deliberately avoids (`ARCHITECTURE.md`: no
  backend, static site). Disproportionate to what a beginner's tutorial cell
  needs, and the kind of stack growth this project has consistently avoided
  elsewhere (KaTeX's 266 KB was already weighed carefully as a cost in
  `QUESTIONS.md`'s "How should mathematics be rendered?"; an LSP stack is a
  much bigger ask than that).
- **Monaco Editor + its Python/Pyright integration.** Would mean replacing
  CodeMirror outright — a different editor, not an addition to this one —
  for a benefit (c) already gets most of, more cheaply. Not evaluated
  further; changing editors is its own large decision, not a tooltip one.

## 4. Recommendation — and what actually shipped

Written as: do (a) and (b) first, since both extend the exact mechanism
already built and tested (`docFor`, `pageNamesCompletion`, `hoverTooltip()`)
with no new dependency; leave (c) documented rather than built, since its
main extra value — pre-run completion — was a real but narrower win once
(a) had closed the builtins gap, and it is a second mechanism running
alongside `docFor` rather than a small extension of it.

**Built: all three, together — DECISIONS_LOG.md 7.76.** The question this
section raised for `QUESTIONS.md` — whether pre-run completion is worth
Jedi's cost, or whether (a)+(b) are enough — was answered by prototyping
(c) directly against dewlab's real pinned Pyodide before deciding: Jedi's
`.help()`/`.get_signatures()` genuinely resolve a function defined but
never run, from source text alone, in low tens of milliseconds warm. That
made "worth it" a settled yes rather than an open cost/benefit call, so
(c) was built alongside (a)/(b) rather than staged separately. Live
answers still win over Jedi's whenever both have one — see 7.76 for how.
