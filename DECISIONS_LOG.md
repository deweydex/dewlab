# Decision log

A record of the choices made while building dewlab that the planning documents
did not settle — and, for each one, what it would cost to change your mind.

The second half is the point. Any project accumulates decisions; what makes
them hard to revisit later is not that they were undocumented but that nobody
wrote down how much they cost. An entry marked *trivial* is an invitation to
change it if you disagree. An entry marked *large* is a warning that several
other things are resting on it, and that changing it is a piece of work rather
than an edit.

`planning/` holds what was decided before any code existed, and nothing here
overrides it. This file records the gaps: places the plan named something
without specifying it, places two settled decisions left a genuine choice
between them, and places the build met something the plan had not anticipated.

Entries are grouped by build phase and numbered so that code comments and
commit messages can point at them.

---

## Phase 0 — Foundations

### Reconstructing tutorial_tools.py

`planning/DECISIONS.md` commits to six functions — `text_input`, `dropdown`,
`button`, `show`, `show_table` and `check` — and pins down exactly one
signature, `check(actual, expected)`. Everything else about how these behave
had to be designed rather than looked up. Each choice is written down here
rather than left implicit in the code, so that a later disagreement has
something to argue with.

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
every page load. The planning documents imply this without stating it.
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
Not in the plan. It is the shortcut every notebook user reaches for first,
and it is three lines.
*Cost to change: trivial.*

**0.26 — Each cell has a "reset" button restoring the author's starter code.**
Not in the plan. A student who has edited a cell into an unrecoverable state
otherwise has to reload the page and lose everything else. Cheap now, and it
interacts with Phase 2's restore, so better decided before that is built than
after.
*Cost to change: small, but decide it before Phase 2.*

### Repository

**0.27 — dewlab is its own repository. Resolved.**
`planning/REPO_AND_EDITOR.md` specifies a standalone repository publishing to
GitHub Pages, and that is what this is. The first phase of work was built
elsewhere while this repository did not yet exist, and was moved here with its
history intact once it did; every file arrived unchanged.

Phase 4 is therefore unblocked: Pages can be switched on whenever there is
something worth publishing.
*Resolved. No remaining cost.*

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

---

## Phase 1 — Build script v1

**1.1 — `build.py` depends on Python-Markdown and PyYAML.**
DECISIONS.md names markdown-it plus markdown-it-texmath as the reference
toolchain, which is JavaScript; BUILD_PLAN.md and REPO_AND_EDITOR.md put
`build.py` at the repository root, which is Python. Rather than pull Node into
the build for the prose half, the converter is Python-Markdown with the `extra`,
`sane_lists` and `toc` extensions, and frontmatter is parsed with PyYAML. Both
are pure Python, build-time only, and pinned loosely in `requirements-build.txt`
— nothing here reaches a student's browser. The one thing this loses is the
texmath half of that toolchain; see 1.5.
*Cost to change: moderate. Swapping the converter means re-checking the prose
output, not rewriting the cell or link handling, which do not go through it.*

**1.2 — `exec` fences are lifted out before markdown conversion, not after.**
Each one is replaced by an HTML comment placeholder, the remaining prose goes
through the converter, and the cell markup is substituted back in. Handing
`python exec` to the markdown library as an info string and trying to catch it
in a fence-handling extension is the other route; it means fighting the library
for control of the one construct dewlab most needs to be exact about. Doing the
split first means a cell's Python is never seen by the markdown parser at all,
so nothing in it can be reinterpreted as markup.
*Cost to change: large. It is the shape of the whole converter.*

**1.3 — Built pages mirror the source tree: `site/tutorials/<module>/<slug>.html`.**
`/site/` was already the output directory named in `.gitignore` at the end of
Phase 0. Mirroring `tutorials/<module>/` rather than flattening keeps the
built tree legible against the source, and means a new module folder needs no
build change. Cross-tutorial links are computed with `os.path.relpath`, so a
link between two tutorials in the same module comes out as a bare filename
rather than a walk up to the site root and back down.
*Cost to change: small, but Phase 3's navigation and Phase 4's Pages deploy
will both assume this layout once written.*

**1.4 — A dead cross-link fails the build; a missing `alt` fails it too.**
CONTENT_AND_FILE_ARCHITECTURE.md asks for a failure "or at minimum a loud
warning" on an unresolved link; a warning in a CI log is a warning nobody reads,
so it is an error. The same treatment answers OPEN_QUESTIONS.md 33 for images:
an `<img>` with no `alt` attribute at all stops the build, while an explicit
`alt=""` passes, which is how a decorative image is meant to be marked. Anchors
are checked as well as slugs, and a cell id counts as an anchor.
*Cost to change: trivial to downgrade to warnings, and a bad idea.*

**1.5 — Math is not rendered yet, and nothing in Phase 1 touches `$`.**
DECISIONS.md settles KaTeX rendered at build time, and `assets/vendor/` carries
KaTeX's CSS but no KaTeX JavaScript — so the markup has to be produced by the
build, and there is no client-side fallback. Phase 1's brief does not include
math, so the converter leaves `$…$` alone as literal text rather than guessing
at a mechanism. The question of how a Python build script produces KaTeX markup
is in `QUESTIONS.md`.
*Cost to change: none yet — this is deferred, not decided.*

**1.6 — CI runs the unit tests and a full build; the e2e suite stays manual.**
`.github/workflows/tests.yml` runs both unit modules and then `build.py --clean`,
so a change that breaks the build fails the pull request even if every unit test
passes. The e2e tests need a 30 MB Pyodide download and a browser, which is not
worth paying on every push before Phase 4 exists.
*Cost to change: small — the e2e job is a handful of lines whenever it earns
its place.*

**1.7 — The two `pytest.importorskip` calls became per-class `skipif` marks.**
Both sat at module level in `tests/test_tutorial_tools.py`, so a machine without
pandas skipped the entire file and reported "1 skipped" — indistinguishable from
a pass at a glance, and about to become CI's problem. The guards now sit on the
two classes that need the libraries: 49 tests run and 12 skip visibly where
pandas and numpy are absent.
*Cost to change: none, it should not change.*

**1.8 — Maths renders in the browser, from marked spans, with KaTeX vendored.**
The reason `planning/DECISIONS.md` gave for rendering at build time was to keep
the parsing cost off students' machines. That cost was reviewed and judged not
worth avoiding, which leaves 0.19 deciding the question instead: `assets/vendor/` is committed precisely so neither CI nor an author
previewing locally needs Node, and calling Node from `build.py` to render maths
would undo exactly that. So KaTeX is bundled into `assets/vendor/katex.bundle.js`
(266 KB) and the runtime imports it dynamically, only on pages the manifest
flags as containing maths.

`build.py` still owns finding the maths. It lifts `$…$` and `$$…$$` out before
the markdown converter runs — otherwise `$a_i + b_j$` comes back with the
subscripts turned into emphasis — and emits a `<span class="dl-math">` holding
the source TeX. That span is the input KaTeX renders from and the fallback if it
never loads, so a reader with JavaScript off sees the TeX rather than a gap.
KaTeX's auto-render contrib script is deliberately unused: the build already
knows where every maths span is, so there is nothing for a delimiter scan to
find that is not already marked.
*Cost to change: moderate. Moving to build-time rendering later means a Node
step in `build.py` and in CI, and nothing else — the marking is already done.*

**1.9 — Illustrative code is highlighted by a read-only CodeMirror, not a second
highlighter.**
An untagged fence had no highlighting at all; only `exec` cells did. Pygments at
build time was the obvious alternative and was rejected: it means a second
syntax theme to keep in step with the CodeMirror pair the texture panel already
switches (0.26, DECISIONS.md "Code cell theme"), and two themes drift. The same
`createReadOnlyCode` view is used instead — same theme compartment, so one
texture change repaints live cells and illustrative blocks together.

`build.py` emits `<pre class="dl-static" data-lang="…"><code>` with the source
escaped inside it, reusing the class Phase 0's stylesheet already defined for
this and never had anything to apply it to. The runtime upgrades that in place,
so the code is readable with JavaScript off and highlighted with it on.
*Cost to change: small.*

**1.10 — Pages and Actions confirmed; the build stays Python for now.**
GitHub Pages with an automated build on push is confirmed as the hosting, which
is what `planning/REPO_AND_EDITOR.md` already specified and what Phase 4 will
build. A local preview is wanted. The authoring editor is to follow an existing
markdown editor pattern rather than being designed from scratch — a starting
point rather than a decision.

Wanting a local preview does not, on its own, force a JavaScript rewrite.
`python3 build.py` followed by a static server is a local preview today, on any
machine with Python. What Python cannot give is a preview *inside* a
browser-based editor, or on a machine with no Python at all — and whether
either is worth roughly 400 lines and 49 tests is a Phase 4 question, not one
Phases 2 and 3 need answered. Left open deliberately, so that nothing built in
between quietly assumes an answer.
*Cost to change: rises with everything built on `build.py`. Decide before the
editor is built.*

**1.11 — `dev/from_notebook.py` converts notebooks; three things it drops on purpose.**
The first real series comes from eighteen Jupyter notebooks rather than being
written from scratch. Converting them is a script rather than an afternoon of
copying, and the script makes three decisions worth stating.

*Saved outputs are dropped.* A notebook stores the output of the last run
alongside the code. dewlab re-runs everything in the reader's browser, so a
stored output is redundant at best and, once the code above it changes, a
confident answer to a question nobody asked.

*Magics and shell escapes are dropped, and reported.* `%matplotlib inline` is
unnecessary here and `!pip install …` cannot work. Silently keeping either
would produce a cell that fails on the student's first run; silently dropping
them would hide a change from the author. They are dropped and named in the
conversion report.

*Cell ids come from the section heading, not from position.* Ids are what saved
progress matches on. A positional id rebinds a student's work to the wrong cell
the first time one is inserted above it, which is precisely the failure
VERSIONING_AND_PROGRESS.md exists to avoid. `counting-carefully-1` also happens
to be readable, which matters when an author later edits the markdown by hand.

The `SOLUTION_` variants are not converted. They exist because a notebook
cannot check a student's answer; dewlab has `check()`, so converting them would
duplicate the series to no purpose.
*Cost to change: small. The conversion is a one-off — after it, the markdown is
the source and the script has done its job.*

**1.12 — A list written tight against a paragraph is given its blank line.**
Markdown converters disagree about whether a list may start on the line
immediately after a paragraph. Most of the ones an author has met before — a
notebook, GitHub — say yes. The converter here says no, and quietly runs the
items together into the paragraph instead. Nobody notices until a student is
reading it: there is no error, no warning, just prose where a list should be.
Six places in the first converted series were like this.

`build.py` now inserts the blank line rather than leaving the trap open. The
alternative — warning and asking the author to fix it — trades a silent
rendering bug for a noisy one, and the author's intent is not in doubt: a line
beginning with a bullet under a sentence ending in a colon is a list.
*Cost to change: small, and the tests pin the edge cases — a hyphenated
sentence, a dash inside a fence, a list that already had its blank line.*

## Phase 2 — Saved work

**2.1 — Autosave is silent; the restore is not.**
VERSIONING_AND_PROGRESS.md makes autosave the primary mechanism, so a student
never has to think about saving. That means the moment they *do* need to think
about it — coming back to a tutorial that changed underneath them — has to
announce itself. Work is restored either way; the notice is visible,
dismissable, and never blocks the page.

The notice says three separate things when they apply: that the tutorial was
updated, that some saved cells no longer exist here, and that a cell with a box
or a button in it needs running again before it works. The third is the
limitation the plan anticipated — a widget's saved HTML comes back, but the
live Python object behind it does not.
*Cost to change: small.*

**2.2 — A saved cell with nowhere to go is reported, not discarded.**
Restore matches on cell id, so reordering a tutorial or inserting a cell is
harmless. Deleting one is not: whatever the student wrote there has no home.
Silently dropping it is the easy path and the wrong one — they wrote it, and
they should be told it is gone rather than quietly losing it.
*Cost to change: trivial.*

**2.3 — Saved output is written back as markup, and that is safe here.**
Restoring means putting stored HTML back into the output area. Everything that
lands there was escaped on the way in by `tutorial_tools` (0.15), the record
never leaves the student's own browser, and the only person who can write to it
is the person reading it. There is no second party for this to be dangerous to.
*Cost to change: it should not change while the record stays device-local. If
progress ever syncs between machines, this needs revisiting first.*

**2.4 — Export is a file the student can keep; import replaces what is there.**
The panel offers a copy to export, a copy to load, and starting again. Import
overwrites rather than merging: merging two versions of a student's own work
raises questions neither they nor the tool can answer, and the export exists to
carry work between machines, not to combine it.
*Cost to change: small, but merging is a design problem rather than an
implementation one.*
