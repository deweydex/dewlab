# dewlab decision log

Decisions made while building that the planning packet does not settle.

DECISIONS.md is the source of truth and nothing here overrides it. This file
records the gaps: places the packet named a thing without specifying it, places
two settled decisions left a choice between them, and places the build hit
something the packet did not anticipate. Every entry says what was decided, why,
and how expensive it would be to change.

Entries are grouped by build phase and numbered so they can be referred to.

---

## Phase 0 — Foundations

### Reconstructing tutorial_tools.py

DECISIONS.md commits to `text_input`, `dropdown`, `button`, `show`,
`show_table` and `check`, and gives exactly one signature: `check(actual,
expected)`. `exam_tools.py` no longer exists to read the rest off. Everything
below is reconstruction, flagged here rather than left implicit in the code.

**0.1 — Widgets return a handle; `.value` reads the live DOM.**
`text_input("Your name")` returns an object whose `.value` property reads the
input element each time it is asked, rather than returning a snapshot taken
when the widget was created. Without this a cell could render a text box but
never read what was typed into it, which would make the widget bridge useless.
The alternative — widgets that only render, with values fetched by a separate
`get_value(id)` call — is clumsier at the call site.
*Cost to change: small. One class, and the tutorials that use it.*

**0.2 — Widget values survive a re-run.**
Running a cell clears its output area, which destroys the widgets in it. Values
are therefore remembered per `(cell_id, widget_id)` and restored when the
widget is rebuilt. Without this, a student types an answer, presses Run, and
watches it vanish. VERSIONING_AND_PROGRESS.md anticipates the related problem
(a restored widget "needs a re-run to reinstantiate the live Python-side
object") but does not address the re-run case itself.
*Cost to change: small, but the behaviour without it is bad enough that it
should not change.*

**0.3 — Widget ids: explicit, else derived from the label, else positional.**
`text_input("Your name")` gets the id `your-name-1`; `id="answer"` overrides.
Ids have to be stable across re-runs for 0.2 to work at all. Deriving from the
label means an author gets stable ids without thinking about it, and the
positional suffix keeps two identically-labelled widgets apart.
*Cost to change: small.*

**0.4 — `check` takes two optional extras: `tolerance` and `label`.**
The settled signature is `check(actual, expected)` and that still works
unchanged. `tolerance=` makes a numeric tolerance explicit where a tutorial
wants one; `label=` replaces the default "That's right." with an
author-written question. Both default to `None`.
*Cost to change: small — dropping them would not break existing calls.*

**0.5 — `check` compares by meaning, not by `==`.**
Floats compare with `math.isclose` rather than exactly, so `check(0.1 + 0.2,
0.3)` passes — a student meeting floating point for the first time should not
be told their correct answer is wrong. numpy arrays and pandas objects compare
elementwise instead of raising "truth value of an array is ambiguous". `True`
does not equal `1`, despite Python, because it is not the answer they meant.
Lists report which position differs.
*Cost to change: moderate. It is the behaviour tutorials will be written
against.*

**0.6 — `button(label, on_click)` calls the function; it does not re-run the cell.**
The callback runs with the cell's output area still current, so anything it
prints or `show`s appends beneath the button. Re-running the whole cell on
every click was the other option; it would discard everything above the button
and make a button useless for anything incremental.
*Cost to change: small.*

**0.7 — `show(*values, label=None)` mirrors what a cell's last expression does.**
The explicit form of the automatic behaviour, for use mid-cell or when one cell
should show several things.
*Cost to change: small.*

**0.8 — `show_table(frame, max_rows=20, caption=None)` truncates by default.**
A tutorial that renders a 50,000-row dataset in full produces an unusable page.
Truncation is visible: the note under the table says how many rows there are.
*Cost to change: small.*

**0.9 — `load_csv(name)` added, beyond the six named functions.**
CONTENT_AND_FILE_ARCHITECTURE.md spells out the fetch-into-Pyodide-then-read
pattern inline in a setup snippet. That pattern is four lines of boilerplate
that every data tutorial would repeat, so it is wrapped as
`df = await load_csv("life-expectancy.csv")`. The raw pattern still works; this
is a convenience, not a replacement.
*Cost to change: small — it can be dropped without affecting anything else.*

### The execution path

**0.10 — Output rendering rules.**
A cell renders, in the order produced: printed text; anything passed to `show`,
`show_table` or `check`; the value of the last expression; then any matplotlib
figure the cell created but did not return. `None` renders nothing, so a cell
ending in an assignment stays quiet. DataFrames and Series render as tables,
figures as PNGs, everything else as `repr`. This is the notebook convention,
which is what a student who has seen Jupyter or Colab will expect.
*Cost to change: moderate.*

**0.11 — matplotlib is captured as PNG via the AGG backend.**
`MPLBACKEND=AGG` is set before matplotlib can be imported, and figures are
saved to an in-memory PNG and embedded as a data URI. The alternative,
Pyodide's HTML5 canvas backend, draws to a target element chosen globally,
which fights with per-cell output areas. PNG also means a figure survives being
saved into Phase 2's `output_html` with no extra work.
*Cost to change: small, and Phase 2 gets easier because of it.*

**0.12 — Cells on one page share one namespace, in document order.**
The notebook model: cell 3 sees what cell 1 defined. This does not extend
across pages — each tutorial page is its own Pyodide instance, exactly as
CONTENT_AND_FILE_ARCHITECTURE.md says, so an included setup cell re-executes on
every page load. The packet implies this without stating it.
*Cost to change: large. Everything else assumes it.*

**0.13 — The whole cell lifecycle lives in Python, not split with JavaScript.**
`tutorial_tools.run_cell(cell_id, output_element, code)` is the single entry
point; the JavaScript runtime boots Pyodide and calls it. Output ordering and
traceback formatting therefore have one implementation rather than two that can
disagree — and, because the module imports under plain CPython with a recording
stub in place of the DOM, that implementation is unit-testable without a
browser.
*Cost to change: large.*

**0.14 — Tracebacks are trimmed to the student's own frames.**
A `NameError` shows the line they wrote, not dewlab's plumbing or
`eval_code_async`'s. If trimming would leave nothing — a syntax error, say —
the full traceback is shown instead of an empty one.
*Cost to change: small.*

**0.15 — Printed output is `textContent`, never `innerHTML`.**
A student printing `<b>hi</b>` sees `<b>hi</b>`, and a CSV containing markup
cannot inject anything into the page. Everything that does emit markup —
tables, check verdicts, widget labels — escapes its inputs. There is no
untrusted author here, but a dataset is not always trustworthy and the cost of
getting this right is zero.
*Cost to change: none, it should not change.*

**0.16 — A prose-only tutorial never loads Pyodide.**
CONTENT_AND_FILE_ARCHITECTURE.md makes a zero-`exec`-cell tutorial a normal
tutorial. If the manifest lists no cells the runtime skips the whole Pyodide
boot, so a maths tutorial that is prose and KaTeX costs nothing to open.
*Cost to change: small.*

### Assets and dependencies

**0.17 — Pyodide loads from the CDN by default, through one overridable constant.**
`DEWLAB_PYODIDE_BASE` overrides the default jsdelivr URL. The e2e tests use it
to run against a self-hosted copy, and it is the switch to flip if
OPEN_QUESTIONS.md 32 turns out to bite — a school network blocking the CDN.
Self-hosting the runtime plus the baseline three packages measures **30 MB**
(`dev/fetch_pyodide.py` produces exactly that directory), which is the number
to weigh against putting 30 MB of binary wheels in the repo. Not committed
either way; the default stays CDN until someone checks.
*Cost to change: one line, plus 30 MB in the repo.*

**0.18 — CodeMirror and KaTeX are vendored, not loaded from a CDN.**
Unlike Pyodide these are small (700 KB together, mostly KaTeX's woff2 fonts)
and CodeMirror 6 is ESM-only, so it needs a bundling step regardless. Bundling
once into `assets/vendor/` costs less than every page paying a CDN round trip,
and removes two of the three external dependencies a school network could
block.
*Cost to change: small.*

**0.19 — The vendor bundle is committed, and built by a separate script.**
`vendor-src/` holds the pins and the esbuild script; `assets/vendor/` holds the
output and is committed. REPO_AND_EDITOR.md keeps *generated HTML* out of the
repo because it goes stale against its markdown source. A third-party bundle
has no such source in the repo to drift from, and committing it means neither
the GitHub Actions workflow nor an author previewing locally needs Node
installed. Re-run `npm run build` in `vendor-src/` when a pin changes.
*Cost to change: small.*

**0.20 — Pyodide 0.28.3.**
Current stable at the time of building, and it carries numpy 2.2.5, pandas
2.3.1 and matplotlib 3.8.4 as official packages — so the baseline three load in
one `loadPackage` call with no micropip, which is what Phase 0 was asked to
confirm. BUILD_PLAN.md flags that package availability shifts between releases;
the version is pinned in one constant in `tutorial-runtime.js` and in
`dev/fetch_pyodide.py`.
*Cost to change: small, but re-run the e2e tests after.*

**0.21 — A tutorial can widen the package list; the default stays the three.**
The manifest carries a `packages` list defaulting to numpy, pandas and
matplotlib. This is how scipy would arrive if the assumed-not-settled item in
DECISIONS.md turns out to be wrong — a frontmatter field on the one tutorial
that needs it, not a change to the baseline everyone pays for.
*Cost to change: none, the mechanism is already there.*

### Layout and files

**0.22 — The shell template lives at `assets/shell.html`.**
REPO_AND_EDITOR.md lists three files under `/assets/` and does not say where
the template goes. It sits beside the CSS and JS it references. It is not
served to students — `build.py` reads it — but it belongs with them.
*Cost to change: trivial.*

**0.23 — Cells are carried in one JSON block, not per-cell markup attributes.**
`<script type="application/json" id="dewlab-manifest">` holds every cell's id,
hint and starter code, with `<` escaped so nothing in a cell can close the
script element. Putting Python source in HTML attributes or in `<textarea>`
elements means escaping problems that show up months later on the one tutorial
that prints an angle bracket.
*Cost to change: moderate — it is the contract between `build.py` and the
runtime.*

**0.24 — `dev/make_harness.py` is Phase 0 scaffolding, replaced by `build.py`.**
Phase 0 has to prove the shell and the execution path work, but `build.py` is
Phase 1. This script fills the shell's tokens with a fixed set of cells chosen
to exercise every rendering branch. The markup it emits is the contract
`build.py` has to match. It is a test fixture, not a preview tool, and Phase 1
should delete it once `build.py` can build the same page.
*Cost to change: none, it is meant to be thrown away.*

**0.25 — Ctrl/Cmd+Enter runs a cell.**
Not in the packet. It is the shortcut every notebook user reaches for first,
and it is three lines.
*Cost to change: trivial.*

**0.26 — Each cell has a "reset" button restoring the author's starter code.**
Not in the packet. A student who has edited a cell into an unrecoverable state
otherwise has to reload the page and lose everything else. Cheap now, and it
interacts with Phase 2's restore, so better decided before that is built than
after.
*Cost to change: small, but decide it before Phase 2.*

### Repository

**0.27 — Built inside `everlearning/dewlab/`, not its own repo. Needs a decision.**
REPO_AND_EDITOR.md wants a standalone repo with GitHub Pages, and there is no
`deweydex/dewlab` yet. This session's GitHub access is scoped to four existing
repositories and cannot create a fifth (`create_repository` returns 403), so
the work went into `everlearning/` — the closest thing to an infrastructure
repo — laid out so that the `dewlab/` directory *is* the intended repository
root. `git subtree split -P dewlab` extracts it with its history intact once
the repo exists.
Phase 4 (Pages deployment) cannot be done from here at all. Nothing before it
is blocked.
*Cost to change: small if done before Phase 4, and it has to be done by then.*

---

## Open questions this build did not need to answer

Recorded so the next phase does not have to re-derive that they were skipped.

- **OPEN_QUESTIONS.md 32** (school network blocking a CDN) is not resolved, but
  0.17 makes it a one-line change rather than a redesign, and
  `dev/fetch_pyodide.py` measures the cost at 30 MB.
- **9** (sympy) and **10** (interactive plots) did not come up. 0.21 is the
  mechanism for the first.
- **33** (build-time checks beyond markdown-to-HTML) is Phase 1's question, not
  Phase 0's.
- The **assumed-not-settled** items in DECISIONS.md — scipy staying out, the
  editor previewing through `build.py` rather than a live Pyodide pane, live
  hover documentation deferred — were all built against as written. None of
  them turned out to be load-bearing for Phase 0.

---

## Phase 0 addenda — found by looking at the rendered page

Three things the tests passed but a screenshot showed were wrong. Recorded
because each is a deliberate divergence from what a notebook does.

**0.28 — matplotlib artist reprs are suppressed.**
`plt.plot(...)` returns a list of `Line2D`; `plt.title(...)` returns a `Text`.
A notebook prints those reprs above the figure. For someone meeting matplotlib
for the first time it is noise that looks like an error, so a cell whose last
expression is an artist renders the figure and nothing else. Figures and every
other type are unaffected.
*Cost to change: trivial.*

**0.29 — a cell ending in `check(...)` does not print a bare `True`/`False`.**
`check` returns a bool so a cell can branch on it, but ending a cell with a
check is going to be the common shape in these tutorials, and repeating
`False` under a verdict that already says "Not quite yet" reads as a second,
more cryptic failure. Suppressed only when the check's verdict is the last
thing rendered and the value is that same result; any other bool renders
normally.
*Cost to change: trivial.*

**0.30 — figures are saved transparent, with one theme-neutral ink.**
A figure saved with matplotlib's default white background sits in a bright
white box on a dark page, so figures are saved with `transparent=True` and the
page background shows through.

That leaves the chrome — title, axis labels, ticks, spines, legend text. The
obvious approach, painting it in the current theme's foreground, was tried and
rejected: a PNG is baked at render time, so every figure already on the page
turns near-invisible the moment the reader switches theme, and keeping every
figure open for the life of the page purely to repaint it is not worth it. The
chrome is therefore drawn in a single grey (`#7a7a7a`) that holds about 4.15:1
against both the light and the dark page background — slightly less contrast
than a theme-matched ink at its best, and never wrong. The plotted data keeps
whatever colours the student's code chose.
*Cost to change: small.*
