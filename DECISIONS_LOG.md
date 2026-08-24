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

## Phase 4 addendum — the downloadable copy

**4.1 — One source, two outputs; the export is built, not duplicated.**
A student should be able to take a tutorial away as a file and still run it.
The obvious way to get that — keeping a hand-maintained HTML copy of each
tutorial — is the thing worth refusing: it puts every tutorial in two places,
and the second one goes stale the first time somebody is in a hurry.

`build.py` therefore writes both from the same markdown in the same run. Editing
a tutorial regenerates the page and its downloadable twin together, and neither
can drift from the other because neither is written by hand. The download link
on each page points at that twin.
*Cost to change: small. The export is a transformation of the built page, so it
follows the page rather than needing to be kept level with it.*

**4.2 — The export is one file that still needs the internet once.**
A page opened from a file cannot load an ES module, cannot fetch a neighbouring
file, and cannot resolve a link to a page that is not beside it. So the export
inlines the stylesheet, the editor, the maths renderer and its fonts, and the
Python tools; it loads Pyodide through its classic script rather than as a
module; and it drops the navigation rather than shipping links that would break.

What it does not do is carry Python itself. That is 30 MB and would make the
file unwieldy for the common case, where a student has a connection the first
time they open it. If school filtering turns out to block the runtime — the
risk `OPEN_QUESTIONS.md` 32 tracks — this is the decision to revisit, and the
runtime can be inlined the same way everything else was.

The runtime says so plainly rather than failing obscurely: with no connection,
the reading works and a single line explains why the cells do not.
*Cost to change: moderate. Inlining Python is a size decision, not a redesign.*

**4.3 — The classic bundle is committed, and CI checks it is not stale.**
`assets/vendor/standalone.bundle.js` is the whole runtime rebuilt in the older
script format, committed like the rest of `vendor/` so that `build.py` needs no
Node. Unlike the rest of that directory it depends on `assets/tutorial-runtime.js`
rather than on a pinned version, so it goes stale whenever the runtime changes —
and a stale copy would mean downloaded tutorials quietly behaving like an older
version of the tool.

CI rebuilds it and fails if the committed copy differs. That turns a silent
divergence into a failed check.
*Cost to change: small, but do not remove the check without replacing it.*

**4.4 — A whole series downloads as one archive, built from the same files.**
One tutorial at a time is right for a student who wants the one they are on.
It is the wrong shape for a teacher setting up a room or filling a memory stick
for a class, who would otherwise click through eighteen pages.

So the build gathers each series into `site/download/<series>.zip` and the
contents page links to it. The archive holds the very files the per-tutorial
links point at — byte for byte, copied rather than regenerated — so there is no
third thing that can go stale. A build without the downloadable copies writes no
archive and the contents page shows no link, which keeps a quick local preview
quick.
*Cost to change: small. It is a dozen lines around the files that already exist.*

**5.1 — One Settings menu, not a row of small buttons.**
The masthead grew a control per feature: "progress" when saving arrived, then
"texture", with the download sitting in the navigation row because that is where
there was space. Three unrelated things in two places, each too small to read as
an invitation, and the navigation row paying for one of them.

They are now one **Settings** button opening one panel with three sections —
your work, this tutorial, texture. A student who finds Settings once has found
all of it, and each section can grow without another button appearing beside the
wordmark. The panel closes on Escape and on a click outside, because a panel
that can only be dismissed by finding the same small button again is one that
gets left open.
*Cost to change: small. It is one panel and one controller.*

**5.2 — The masthead follows the reader down the page.**
A tutorial is long. With the header at the top only, the way back to the
contents and the way into Settings were both a scroll to one end — and on a
phone that is most of a page of scrolling to change the text size.

The masthead is now sticky. Everything that has to clear it measures from
`--dl-header-h` rather than guessing: the status line, the settings panel, and
an anchored jump, which would otherwise land its heading underneath the header.
The parts of the masthead are sized in rem and do not follow the reader's text
size, so that one number holds at every width.
*Cost to change: small, but change the variable rather than the three places
that read it.*

**5.3 — The navigation row is a grid, and the phone gets its own shape.**
Previous / contents / next was a flex row with `margin-inline: auto` holding the
middle link in place. That works until a title is long or an outer link is
missing — the first and last tutorial of every series — and then the row goes
lopsided or pushes a title off the screen.

It is a three-column grid now, so the contents link stays centred whether or not
the outer two exist, and each title wraps inside its own column. Under 34rem the
grid becomes previous and next side by side with the contents link beneath, and
the module name in the masthead gives up its space to the Settings button.
*Cost to change: small.*

**5.4 — `plt.show()` renders the figure instead of warning about a canvas.**
Every textbook ends a plot with `plt.show()`, so students write it. Under the
non-interactive backend dewlab uses, matplotlib's own show() has nothing to draw
on and says so — a `UserWarning` about `FigureCanvasAgg`, arriving in the cell's
error colour, under a plot that rendered perfectly well. For someone meeting
matplotlib for the first time that is indistinguishable from having done
something wrong.

dewlab replaces `plt.show` with its own, which renders the open figures at the
point of the call. A cell that draws, prints, then draws again now reads in the
order it was written. The replacement is installed lazily, since pyplot may not
be imported yet; a warning filter covers the one cell that imports pyplot and
calls show() before that lands.
*Cost to change: small, but any change should keep both halves — the
replacement and the filter behind it.*

**5.5 — The chapter navigation sticks with the masthead, as one group.**
Making the masthead sticky (5.2) left the previous/next row scrolling away, so
moving on to the next tutorial still meant a scroll to one end of a long page.
They now stick together.

One group rather than two sticky elements, because everything below has to clear
whatever is up there: the status line, the settings panel, and an anchored jump,
which would otherwise land its heading underneath. That height is no longer a
constant — it depends on how far the neighbouring tutorials' titles wrap, which
depends on the window and on the reader's text size — so the runtime measures it
into `--dl-chrome-h` and remeasures on every resize.
*Cost to change: small, but the measured variable is load-bearing for three
other rules.*

**5.6 — A minimal header, chosen rather than imposed.**
Sticking the navigation costs vertical space, and on a phone with two long
titles it costs a lot: 143px of a 780px screen. The obvious fix is to drop
things at narrow widths automatically, which takes the choice away from the
reader who wanted them.

**Header: full or minimal** in Settings instead. Minimal tightens the masthead
and truncates the neighbouring titles to one line each — 70px, and nothing is
removed: every link is still there and still reaches the same place. It is a
reading-comfort preference like text size, and it lives beside them.
*Cost to change: small.*

**5.7 — Every page carries its own contents list, built from its headings.**
A tutorial runs to eight sections. Getting back to one a student half-remembers
meant scrolling, and the series contents page is no help — it lists tutorials,
not what is inside them.

The list is generated from the same heading tree that gives the headings their
ids, so it cannot disagree with the anchors it links to. Closed by default: a
reader arriving at a tutorial should meet the tutorial, not a list of its parts.

Two rules keep it useful rather than exhaustive. A page with fewer than two
sections gets none, because a contents list for a single heading is furniture.
And a sub-heading whose text repeats within the tutorial is left out — five
entries reading "Your turn" are a list nobody can choose from. The headings keep
their anchors either way; only the listing drops them.
*Cost to change: small.*

**5.8 — Line width has three presets and a slider, not one or the other.**
The slider alone gave no idea what a good value was, and three buttons alone
would have taken away a control some readers had already set. So both: narrow,
medium and wide write to the same number the slider does, and setting something
between the presets leaves none of the three pressed, which is the honest way to
show it.
*Cost to change: small.*

**5.9 — The contents page opens with a map, not just a list.**
A numbered list says what order to read in. It cannot say that the course spends
four tutorials on programming before any mathematics appears, or that Tutorial
17 leans on five earlier ones and is therefore the expensive one to move. Those
are facts about the shape of the material, and a student deciding where they are
and what they need first is asking about shape.

Inline SVG generated by `build.py`, not a diagramming library: the layout is a
few dozen lines of arithmetic, and adding a runtime dependency to draw twenty
boxes would cost more than it saves. Nodes are grouped into the strand a
tutorial mostly covers, read from `planning/curriculum/outcomes.yaml` — and
optionally, so that the site still builds from the tutorials alone if the
planning folder is not there.

The two kinds of arrow do different jobs. Reading order is solid and dark
because it is an instruction to the reader. "Builds on" is dashed and faint
because it is a fact about the material — and it is *found*, by reading each
tutorial for the earlier ones it names, rather than declared somewhere that
could go stale.
*Cost to change: moderate. The layout arithmetic is the part to be careful with.*

**5.10 — The map is not bound by the reading measure.**
Everything else on a dewlab page is sized to a comfortable line length. A
diagram is not prose and reads worse squeezed, so the figure centres itself on
the column and takes up to 58rem, scrolling inside its own box on a narrow
screen. The page still never scrolls sideways.
*Cost to change: small.*

**5.11 — The curriculum map asks the tutorials about their own vocabulary.**
The tutorials already mark a term being introduced: single-asterisk emphasis,
the first time a word means something particular. That convention was there
before anybody thought to check it, which is exactly what makes it usable — it
is evidence of what an author considered a new word, not a list to maintain.

Two questions come free from it. A term emphasised in two tutorials is being
introduced twice, or means two things; the tool cannot tell which and says so.
A term appearing in an earlier tutorial than the one that explains it was used
as though the reader already knew it.

Neither is a verdict. `index` turned up under the first question and cost a
rewrite; `modular` turned up the same way and is merely said twice.
*Cost to change: small. The stress-word list is the only hand-maintained part,
and a wrong entry there costs a little noise, not a wrong answer.*

**5.12 — Asset URLs carry a content hash.**
The map rendered as black boxes and filled blobs on a phone that had visited the
site before. Nothing was wrong with the markup or the stylesheet: the browser was
still serving the stylesheet it had downloaded on an earlier visit, so the page
was new and the CSS was old.

That failure does not look like caching. It looks like the site is broken, and
only for people who have been here before — which is every student after their
first lesson, on a school machine that caches aggressively.

Every asset URL the markup names now ends in a short hash of that file's
contents. Hashed per file rather than one version for the lot, so editing the
stylesheet does not also force a fresh download of the 266 KB maths bundle. The
one file the runtime fetches for itself, `tutorial_tools.py`, is not in the
markup and so cannot be busted by it; its version travels in the manifest
instead.

`vendor/katex.bundle.js` is deliberately left unversioned: the standalone export
can only bundle that import into one file if the specifier is a plain string,
and the bundle is vendored and pinned, so it changes only when we re-vendor on
purpose.
*Cost to change: small. But removing it brings the bug back invisibly.*

**5.13 — The standalone export fails loudly when a substitution finds nothing.**
The export works by replacing markup this same file wrote moments earlier.
`str.replace` with no match is a silent no-op, so when the asset URLs gained a
version the export quietly stopped inlining the stylesheet, and only the tests
noticed. Every replacement now raises instead, naming what it could not find.
*Cost to change: small, and it is the guard that made the previous entry safe.*

**6.1 — The map became a topic tree, on its own page.**
The map on the contents page was of *tutorials*, and it had to fit above a list
without pushing it off the screen. Both of those were limits, and the second was
the reason it could never be more than a diagram.

On its own page it can take the window, and it can be about topics rather than
tutorials: all 67 outcomes in both descriptors, laid out left to right by what
has to come first and grouped top to bottom by subject. Two axes doing two jobs,
so a strand reads as a band across the whole tree and nothing ever points
backwards.

Drag to pan, scroll to zoom, choose a topic to read it. No library — the layout
is computed in `build.py` and arrives as data, so the page has nothing to fetch
and the interaction is the forty lines of pointer handling a library would have
needed anyway.
*Cost to change: moderate. The layout arithmetic and the pan/zoom clamping are
the parts to be careful with.*

**6.2 — The tutorial map moved rather than being deleted.**
It shows something the topic tree does not: which tutorials lean on which, found
by reading each tutorial for the earlier ones it names. That is evidence about
our own material and it exists nowhere else, so it sits under the tree on the
same page rather than being replaced by it.
*Cost to change: small.*

**6.3 — Light and dark cost nothing because the tree uses the same shell.**
It could have been a standalone page with its own styling. Built on the shell
every tutorial uses, it inherits the masthead, the settings panel, the theme
tokens and the reader's saved preferences — so "works in dark mode" was not a
feature to build, it was a consequence of not building a second thing.
*Cost to change: small, but building it standalone would have cost far more.*

**6.4 — The contents page introduces rather than illustrates.**
With the map gone it says what dewlab is to somebody who has just arrived —
nothing to install, nothing to break, work saved in this browser — and then gets
out of the way of the list they came for.
*Cost to change: small.*

**7.1 — Reading order lives in one file per series, not in every tutorial.**
`order: 12` in each tutorial's frontmatter meant inserting one in the middle was
an edit to every file after it. In `<series>.order.yaml` — a list of slugs —
moving a tutorial is moving a line and inserting one is adding a line.

The build checks both directions. A tutorial the file forgets stops the build;
so does a slug with no tutorial behind it, which is the more dangerous of the
two because the file looks complete and the series is quietly short. And a
tutorial still carrying `order:` in its frontmatter stops the build rather than
having that field silently ignored — half-migrated is worse than either state,
since the ignored field is exactly the one somebody would edit.

This is what makes the editor small: it edits one list. It is also what makes
the editor optional, because one list is something a person can reorder by hand
in the GitHub web interface.
*Cost to change: moderate, and it should not change again.*

**7.2 — The numbers are gone from titles, slugs and prose.**
"Tutorial 14: Expressions Come Alive" is now "Expressions Come Alive", at
`expressions-come-alive.html`, and the fifty prose references say the name
rather than the number. Published URLs changed, which is the real cost and the
reason to do it exactly once.

What it buys is that inserting a tutorial anywhere is now free. Nothing carries
a position except the order file, so the re-planned series — splitting Tutorial
13, adding the maths tutorials, putting the two conversions near the front — no
longer implies a fifty-place edit that nothing verifies.
*Cost to change: high, in the sense that putting them back would be as much
work again.*

**7.3 — A slug is unique within its module, not across the site.**
The rename made both modules want `first-steps`, and the built path already
carries the module, so there was never any real ambiguity — only a global check
that would have forced tutorials to be named around a constraint that does not
exist.

`tutorial:slug` links now look in the linking tutorial's own module first, fall
back to another module when exactly one has that slug, and stop the build when
more than one does. Guessing would be the only other option.
*Cost to change: small.*

**7.4 — "Builds on" is found by title now.**
The map's dashed arrows were found by matching "Tutorial 11" in the prose. With
the numbers gone they match titles instead — which is what a tutorial would
naturally write anyway, and turned out to find exactly the same seven
references.
*Cost to change: small.*

**7.5 — A downloadable copy lives under its module, like its page.**
Scoping slugs to the module (7.3) left one thing keyed by slug alone: the flat
`site/download/` folder. Two modules each having a `first-steps` meant one
silently overwrote the other, and the loser simply never appeared.

The publish guard from 4.3 caught it — *"20 tutorial pages but 19 downloadable
copies"* — on main, which is later than it should have been. The unit tests had
a case for two modules sharing a slug and a case for the downloadable copies,
and neither exercised both at once.

Copies now sit under `download/<module>/`, and four tests cover the crossing.
Each was checked against the broken build first: all four fail without the fix.
*Cost to change: small, and the guard is what makes it safe.*

**7.6 — Dependencies answer "can I start this now?", not "what comes next?".**
The topic tree was built topic by topic — "what does this one obviously need?" —
which produces edges that are individually reasonable and collectively
arbitrary. The core architectural intent is reachability: giving students the
opportunity to explore freely, discover areas requiring extra practice, and
enabling instructors to plan module coverage flexibly.

That inverts the design rule. A route wants few branches and one clear line; a
reachability map wants as few edges as it can honestly get away with, because
**every edge closes a door**. Three trees built on three different rules are
written up in `planning/curriculum/DEPENDENCIES.md`, with the places they
disagree left visible rather than quietly resolved. Tree C — five gateway topics
with everything else hanging off one — is what shipped.

The measured result is not the one predicted: it added an edge rather than
removing seven. What actually moved was depth, from a longest path of 6 to 5,
with one more topic open from a standing start.
*Cost to change: small. It is one `needs:` list per topic in `topics.yaml`.*

**7.7 — Discover first, name afterwards.**
Pedagogical principle: Discover first, name afterwards. Rather than introducing
formal terminology upfront before practical motivation, concepts are discovered
through step-by-step concrete reasoning. Applied systematically, this determines
dependency directions. Divide and conquer no longer comes before searching and
sorting — binary search is the reason to care about the idea, so it now comes
after it. Substitution comes before the chain rule for the same reason, and
because substitution is algebra students have already practiced.
*Cost to change: small, and reversible per topic.*

**7.8 — The tree reads downwards.**
Roots at the top, and nothing ever points upwards. The first attempt was the
direct flip of the old horizontal layout — one column per subject — which
measured 5854px wide against 756px tall: a horizontal tree wearing a hat, and
useless on a phone. With twelve subjects there is no width to spend, so subject
stopped being an axis and became a sort. A tier wider than five topics wraps,
subjects stay grouped within a tier, and each node carries its subject as a
colour. The tree is now 1058 × 1768 and fits a phone.

Two bugs fell out of the change. The zoom controls sit inside the frame, and the
frame starts a pan on any press that is not a topic — so pressing +, − or fit
captured the pointer and swallowed the click. They had never worked. And the
zoom floor of 0.35 was set against the old short tree; against the tall one it
stopped "fit" from fitting.
*Cost to change: small.*

**7.9 — The tutorials do not name the assessments.**
The prose named them throughout: *"you are now ready for Skills Demo 1"*, *"the
last tutorial before Skills Demo 2B"*, *"in the next set of tutorials and Skills
Demo 2"*. Thirteen references across nine tutorials.

That ties the material to one institution's assessment schedule, and the
schedule is the thing most likely to change. Every reference had a version that
said the same thing about the student's own work — "you are now ready to build
these tools fresh, from nothing but the ideas" says more than "you are now ready
for Skills Demo 1" did, because it says what readiness consists of.

A test guards it. Not because anybody would put them back deliberately, but
because prose written next year will reach for whatever the prose around it
does.

**7.10 — Reflection is its own series, not the last tutorial.**
"Looking Back Before Moving Forward" sat at position eighteen of eighteen, which
said it was the thing you do at the end. It is not: it is the thing you come
back to whenever you have finished something worth looking at again. It now
lives in a `Reflections and review` series of its own, and its text no longer
assumes you have just handed in one particular piece of work.

Splitting it surfaced three things that had never been exercised, because no
module had ever had two series:

- The contents page headed each series with its **filename slug** rather than
  the name in its order file.
- The archive link read *"Download all 1 as single files"*.
- The curriculum map's sequence graph keyed nodes on `order`, which restarts at
  1 per series — so it emitted two nodes called `T1` and an arrow from one of
  them to itself. The back-reference finder had the same fault.

*Cost to change: small. Moving it back is a line in each of two order files.*

**7.11 — The editor edits content, and previews structure rather than appearance.**
The editor supports both series/tutorial management (reordering, inserting,
creating) and content editing (prose, frontmatter, and code cells).

A full live browser preview of rendered HTML would require maintaining a
parallel client-side renderer alongside the Python-Markdown build pipeline. A
secondary renderer that drifts from `build.py` provides inaccurate feedback.
Consequently, the editor previews structural validity: runnable cell counts,
cell IDs, headings, and build-breaking syntax issues (e.g. unclosed fences,
missing or duplicate IDs). Visual rendering is inspected via the built site.
*Cost to change: small. The parser is pure and tested on its own.*

**7.12 — Renaming a cell id destroys saved work, and only the editor can say so.**
A cell's id is the key a student's work is stored under. Renaming one does not
move their work; it orphans it, and the cell comes back empty. The build cannot
warn about this — by the time it runs, the old id is gone. The editor is the
only place both versions exist at once, so it names the ids that vanished
before the commit is made.
*Cost to change: small, but the warning is the reason the feature is safe.*

**7.13 — Divide and conquer sits beside searching and sorting, not before it.**
Searching and sorting are split into distinct tutorials (`finding-things` and
`putting-things-in-order`), with divide and conquer presented within both:
binary search halving a sorted list, and merge sort halving an unsorted list.
In `topics.yaml`, divide and conquer depends on iterating by index, matching
searching and sorting, with neither configured as a prerequisite of the other.
*Cost to change: one line.*

**7.14 — Some things a student needs are nobody's learning outcome.**
Certain foundational topics (e.g. categorization of triangles, the Cartesian
coordinate plane for the unit circle) are necessary precursors to syllabus
outcomes but are not explicitly enumerated in curriculum descriptors.

Topics may now carry a `PRE-` code, meaning **groundwork**: assumed, met in
passing wherever it is first needed, and belonging to no outcome. They show on
the map as groundwork rather than as "planned", which would have read as a gap
in the course. They also carry their own `strand:`, since strands come from
`outcomes.yaml` and a non-outcome would otherwise land in "other" — which is
not a subject, it is a shrug.

The guard against typos survives: a `MIT-` or `PDP-` code must still be a real
outcome.
*Cost to change: small. One code prefix and one branch in the state.*

**7.15 — The colours on the tree are explained where they are used.**
Every node carries its subject as a coloured edge, and the only way to learn
what a colour meant was to choose a topic and read the panel — the wrong way
round for a key. There is now one on the page, generated from the strands
actually on the tree, so it cannot list a colour nothing uses or miss one that
is there.
*Cost to change: small.*

**7.16 — The zoom controls are above the tree, not on it.**
They floated over the canvas, which meant they covered whichever topics
happened to sit under them and took the clicks meant for those topics —
invisibly, differently at every zoom level, and only noticed because adding one
topic moved the layout enough to put a tested node underneath them.

The guard added in 7.8, which stopped the frame stealing presses on the
controls, is gone with them: outside the frame it guards nothing.
*Cost to change: small.*

**7.17 — A tutorial is archived, not deleted.**
Deleting the file was the only way to retire a tutorial, and deleting it would
strand every student who had saved work in it: the work sits in local storage
keyed to a page that no longer exists, with no way back and no trace it was ever
there. That is why the editor was built without a delete button.

*Nobody has lost anything yet — the site has not been in front of a class, so
there is no saved work anywhere.* The property is a property of the design, and
it was worth fixing before the first cohort rather than after.

`status: archived` in the frontmatter. The page is still built, still runs, and
still holds whatever a student saved. What changes is everything about its
place on the course: it leaves the reading order, it has no previous and no
next, it is not in the series archive, it is listed under *Archive* on the
contents page rather than among the series, and it opens with a notice saying
it is not part of the course any more.

`live` is the default, so nothing already written has to say anything.
Deleting a file is still possible and still the right move for something
published in error — archiving is now the ordinary gesture.
*Cost to change: small.*

**7.18 — An archived tutorial teaches nothing the map can point at.**
It taught what it taught. But a student picking a topic today cannot be sent
there, so counting it as coverage would make the map claim an outcome is
covered when nothing on the course covers it — the exact lie the map exists to
prevent. Both the topic tree and `dev/curriculum_map.py` skip archived
tutorials when working out where an outcome is taught.

This is the entry most worth disagreeing with. The other reading is that
coverage means "we have written this", in which case an archived tutorial still
counts and the map is a record of work rather than a guide to the course.
*Cost to change: small — two `continue`s.*

**7.19 — Listing an archived tutorial in the order file stops the build.**
A reading order is a route through the course and a retired tutorial is not on
the route, so the two statements contradict each other. Ignoring the line
silently would leave the order file saying one thing and the site doing
another, which is the class of problem the order file was introduced to end.

The empty case falls out of it: archiving the last tutorial in a series leaves
`order:` with nothing under it, and that is a real state rather than a broken
file. It is accepted, and the series simply stops appearing. `order:` missing
altogether is still an error.
*Cost to change: small.*

**7.20 — The version field is a readable date.**
`2026.08.20.1` — year, month, day, and which release of that day — rather than
an integer.

The restore comparison is
`String(record["tutorial-version"]) !== String(currentManifest.version)`: both
sides stringified, compared for equality, not ordering. A string works with it
unchanged, and the restore itself matches on cell id rather than on version, so
no saved work depends on the type.

It also removes redundant metadata: having `version:` carry the release date
eliminates the need for a separate `released:` field.

Two details that matter: sort on the four parsed numbers, because
`2026.08.20.10` sorts before `2026.08.20.9` as a string. And the label a student
reads stays prose — "20 August 2026" — with the dotted form kept for the file,
the frontmatter and the URL.
*Cost to change: small while nothing is versioned yet; large once tutorials
carry dated versions and students have saved against them.*

**7.21 — Saved work is keyed on the module and the slug, not the slug alone.**
A slug is unique within its module (7.3), and both modules have a
`first-steps`. `progressKey()` was the prefix plus the slug, so the two
tutorials shared one record: answers written in one appeared in the other, and
each save overwrote the other. The manifest now carries the module and the key
is the pair.

Scoping slugs per module requires that every layer — built pages (#23),
downloadable copies (#24), and saved progress — identifies tutorials by the
`(module, slug)` pair rather than the slug alone.
*Cost to change: small today, a migration inside every student's browser after
the first class.*

**7.22 — Loading a saved file checks before it overwrites.**
"Load a copy" wrote whatever JSON it was handed into this page's key and only
then found the cells did not match. By then the student's real work was gone,
replaced by somebody else's, under a notice explaining that some cells could
not be placed.

The record now carries its module as well as its slug, the exported filename
carries the module, and a file from elsewhere is refused by name with nothing
changed. Lenient in one direction: a record with no module still loads on a
matching slug, so a file written before the module was recorded does not hit a
cliff.
*Cost to change: small.*

**7.23 — Four contracts, audited once while changing them was free.**
Before publishing to a live cohort, slugs, cell ids, the save record's
shape and the version field were audited (`planning/WINDOW_AUDIT.md`).

Cell ids are sound: 228 of them, none non-conforming, and the twelve reused
across tutorials are safe precisely because storage is keyed per tutorial. The
version field restore already compares versions as strings and so tolerates the
dotted date.
*Cost to change: this window closes on the day the first class opens the site.*

**7.24 — A version is a release date, and the newest live one answers the
tutorial's URL.**
`version: 1` became `version: 2026.09.15.1` — year, month, day, and which
release of that day. One field carries identity, order and the date a student
reads; a separate `released:` would be a second copy of the first three numbers,
and two fields that can disagree are worse than one that cannot (`VERSIONS.md`).

The unversioned URL serves the **newest `live`** version. Every link written
before versions existed — inside a tutorial, on the topic tree, in bookmarks —
keeps working and keeps meaning "the current one". Other versions sit beneath it
at `<slug>/v<version>.html`.

That one rule supports the beta workflow with no extra machinery: freeze the
current release, mark the working copy `beta`, and students keep the frozen live
one until the beta is promoted.
*Cost to change: high now, in the sense that undoing it would be as much work.*

**7.25 — Status is about the course; default is about the release.**
Two orthogonal concerns that read like one. `status` specifies how a tutorial
stands to the curriculum — `draft` (not built), `beta` (built, reachable,
never the default), `live` (standard), `archived` (retired from active route).
Whether a version is the *default* says which release students get, and a
superseded release is still `live`: it was a real release, it is simply not the
current default.

Conflating them during early test implementation highlighted the distinction:
marking a superseded version `archived` incorrectly presented it as having left
the course rather than as an older valid release.
*Cost to change: small.*

**7.26 — A draft is the only honest way to have something unpublished.**
The site is static and public: anything built has a URL, and a URL is public.
There is no server and no login, so "not finished" has exactly two meanings and
they differ by whether a page exists. A draft is not built. A beta is built and
findable only by someone given the link, and says so unmissably.
*Cost to change: small.*

**7.27 — Setting a status is two files, and that is why it belongs in the editor.**
The frontmatter field on its own would be trivial to edit by hand. What is not
trivial is that only a live tutorial is on the reading order, and the build
refuses an order file that lists anything else (7.19) — so the line has to move
with the field, or the next build stops. The editor does both in one commit.

The list shows the four statuses on every tutorial with the current one marked,
which also answers "what state is everything in?" at a glance.

Taking a tutorial off the reading order previously removed it from the editor
listing when the list was generated from the order file. The editor list now
displays all tutorials belonging to a series, with off-route tutorials clearly
demarcated.
*Cost to change: small.*

**7.28 — Modules appear in a declared order, not an alphabetical accident.**
The contents page sorted modules by folder name, so Computational Methods came
before Programming and Maths, Integrated for no reason anybody chose. That is
the same invisible ordering the series order files were introduced to end
(7.1), surviving one level up.

`tutorials/modules.yaml` lists module names in the order they should appear.
Lenient where the series files are strict: a tutorial missing from its order
file vanishes from the site (which stops the build), whereas an unlisted module
still appears at the end.
*Cost to change: small.*

**7.29 — Log consolidation and duplicate sequence resolution.**
Decisions 7.11 to 7.15 were reconciled after branch merges. Two branches both
numbered an entry 7.20, so the second was indexed as 7.28 with citation
continuity maintained.
*Cost to change: none.*

**7.30 — The picker tells a reader what will happen instead of warning them.**
Switching tutorial versions provides exact, checkable counts of which cells
carry over rather than ambiguous warnings. If work survives deterministically,
the interface should state that clearly.

Restore matches on cell id, so which answers survive a move is knowable before
the reader makes it. The manifest now carries every release's cell ids, a few
hundred bytes beside a payload that already holds every cell's source, and each
option in the list states:

> **2 June 2026** — 2 of your 3 answers carry over. 1 cell is not in that
> version, so that answer stays saved but is not shown there.

"Stays saved but is not shown" rather than "will be lost", because the record is
keyed by tutorial, not by release, and the answer reappears when returning to a
version containing the cell.
*Cost to change: small. The counts are one function and the ids are one build
step.*

**7.31 — Which release a reader gets is the last one they worked in.**
Two rules govern release resolution:
1. The build determines what the unversioned URL serves (the newest live
   release) for first-time visitors.
2. For returning visitors, the browser resolves to the version the user last
   worked in, unless explicitly chosen otherwise.

The pin is written when selecting a release from the list, and again whenever
saving work in one. Working in a release outranks older selections.

Where no pin exists, the saved record's `tutorial-version` provides the fallback.
*Cost to change: small. "The version last worked in" guarantees seamless continuity.*

**7.32 — The marker is conditional rather than invisible, and it is a date.**
Single-release tutorials show no version badge beside the title. Tutorials with
multiple releases display a persistent date marker (e.g. "15 September 2026")
rather than a hover tooltip, ensuring touchscreens and mobile devices retain the
indicator.
*Cost to change: none. It is built from the manifest at load.*

**7.33 — A downloaded copy has no version list.**
Only the default release gets a standalone copy, so the other releases are not
on the reader's disk. A picker offering to move to files that are not there is
worse than no picker, so the list is stripped from the standalone manifest and
the runtime removes the section that would have shown it.
*Cost to change: one line, and a test that fails without it.*

**7.34 — An older release tells search engines which one is current.**
Two releases of a tutorial are near-identical pages at two URLs. Without a
`<link rel="canonical">` they compete with each other in search results.

Every non-default page points to the release served at the canonical URL. The
default carries none, as it is already the canonical page.
*Cost to change: one line and one shell token.*

**7.35 — The restore notice says what happened instead of guessing.**
When a tutorial has releases, the page knows which release the work was written
in and which one is currently active, naming both explicitly. Answers whose
cells do not exist in the current release are preserved in local storage and
restored when opening a release that contains those cells.
*Cost to change: none.*

**7.36 — Automated curriculum coverage reporting in CURRICULUM_MAP.md.**
Coverage metrics are generated directly by `dev/curriculum_map.py` by inspecting
`outcomes.yaml`, `out-of-scope.yaml`, `proposed.yaml`, and tutorial `covers:`
frontmatter.

`planning/CURRICULUM_MAP.md` reports the number of outstanding outcomes with no
proposal, and `tests/test_curriculum_map.py` asserts that proposals do not claim
already-covered outcomes.
*Cost to change: none.*

**7.37 — Coordinate geometry is a tutorial, because Pythagoras is a gateway.**
Outcomes `MIT-4.1` through `MIT-4.4` form their own tutorial, *Lines and
Distances*, between Drawing Functions and Angles and Waves.

Pythagoras is one of the six gateways in the topic tree, unlocking seven
downstream topics. A gateway requires a dedicated tutorial rather than a
subsection within graphing to serve as a clean reference point.

Furthermore, *The Unit Circle* requires coordinate geometry prerequisites;
having a dedicated tutorial prevents trigonometry from having to introduce
Cartesian coordinates as an aside.
*Cost to change: none yet.*

**7.38 — Connections between whole things, rather than things merged.**
Venn diagrams (`MIT-2.3`) are structured as a dedicated short tutorial (*Drawing
Sets*), linked to *Logic and Truth* and *Sets as Sorted Lists*.

Three distinct modules with explicit cross-links are easier to discover,
sequence, and maintain than an overloaded composite tutorial.

Matplotlib draws diagrams directly from set operations, framing the diagram as
computed visual output rather than manual notation.
*Cost to change: none.*

**7.39 — Editor path resolution supports versioned folders.**
When a tutorial has multiple releases, it resides in a folder of release files
rather than a single `<slug>.md`. The editor's `pathOf` resolves the active live
release (falling back to the newest available release), matching `versions_of`
in `build.py`.
*Cost to change: resolved in editor test fixtures.*

**7.40 — The release workflow freezes existing content before publishing edits.**
The editor maintains two copies of every file: the fetched text (`state.original`)
and the working buffer.

Releasing freezes `state.original` as the prior release and publishes the active
buffer as the new release timestamp. This ensures students can return to the
exact text of prior releases.
*Cost to change: fundamental release lifecycle guarantee.*

**7.41 — Unified warning for cell ID mutations across edits and releases.**
Renaming a cell ID in an in-place edit orphans saved student progress. Releasing
a new version preserves prior cell IDs in the frozen release. The editor UI
presents both outcomes in sequence to guide authors toward releasing when
structural cell changes occur.
*Cost to change: two sentences in editor UI.*

**7.42 — Plain titles and modular scope grounded in pedagogy.**
Titles use plain language describing what the reader builds or explores:
"Lines and Distances" rather than "Coordinate Geometry"; "How We Got Here"
rather than "The Computing Time Machine".

Tutorial scoping is determined by pedagogical cohesion rather than strict 1:1
outcome counts. A tutorial introduces, explains, motivates, and provides
hands-on practice. Two related outcomes stay together; a complex outcome with
multiple distinct activities splits into separate modules.
*Cost to change: none.*

**7.43 — Trigonometry partitioned into three focused tutorials.**
Trigonometric content is structured into three focused tutorials:
- **The Unit Circle** — radians, sine and cosine definitions, exact values.
- **Sine and Cosine Waves** — unrolling circular motion into wave functions.
- **Solving Triangles** — Sine and Cosine Rules, area calculations, right-triangle applications.

Each covers a distinct conceptual activity with adequate room for exercises.
*Parabolas* was separated from *Drawing Functions* on the same principle.
*Cost to change: none.*

**7.44 — Geometric grounding for exact trigonometric ratios.**
Exact values in surd form (`MIT-4.7`) are taught geometrically on the unit circle
rather than through rote memorization of triangles. Surds represent coordinates
derived via the Pythagorean theorem on landmark angles.

With this, every outcome in the curriculum descriptors is in scope and mapped to
existing or proposed tutorials.
*Cost to change: none.*

**7.45 — Practice problem sets and worksheet conversion architecture.**
Practice problem sets derived from worksheets (e.g. `deweydex/Mathematics`) are
structured with answers placed behind collapsible folds beside each problem.

This enables immediate self-verification while preserving the reflective moment
before viewing the solution.
*Cost to change: free at planning stage.*

**7.46 — Clean exception traceback formatting for syntax errors.**
`_format_exception` trims tracebacks to student execution frames. For compile-time
syntax errors where runtime execution frames are absent, dewlab renders the
exception location directly (filename, line, caret) without exposing internal
`tutorial_tools.py` plumbing.
*Cost to change: five lines in runtime tools.*
caret — and Python renders those from the exception rather than from the stack.
So where the exception knows where it happened, the stack goes entirely:

```
  File "<cell your-turn-4>", line 2
    result = (5 + 3
             ^
SyntaxError: '(' was never closed
```

Narrow on purpose. An exception with no user frames *and* no location of its own
still shows the full traceback, because that is a bug in dewlab and hiding our
frames would make it harder to find.

*Cost to change: five lines. Found by writing a tutorial about error messages and
then reading what the page showed, which no test would have thought to check.*

**7.47 — The first two tutorials to close outcomes since the map existed.**
*How We Got Here* (`PDP-LO1`, `PDP-LO3`) and *When It Goes Wrong* (`PDP-LO9`)
are converted from everlearning notebooks. Forty-one outcomes in place became
forty-four.

Three things about the conversion are worth recording, because the next one will
hit all three.

**The converter is a first draft, not an output.** `dev/from_notebook.py`
produced a slug of `pdp-lo1-lo3-mit-14-the-computing-time-machine`, a title with
two emoji in it, and cell ids like
`stop-2-1945-machine-code-the-only-language-the-machine-understands-1`. A cell id
is the key a student's work is saved under and belongs in the frontmatter of
somebody's judgement, not in a slugified heading. Both tutorials were written by
hand from the notebook rather than patched from the converter's output.

**Only half of the second notebook came across.** It is called *Testing and
Debugging* and most of it is testing, which *Building Reusable Tools* already
covers. Taking the whole thing would have duplicated a tutorial that exists.

**Deliberately broken cells are better here than in a notebook**, which is the
one thing this conversion gains rather than merely survives. A cell that raises
the error in front of the reader beats a commented-out example they have to
uncomment — and it is what turned up 7.46.

*Cost to change: these are tutorials now, so their slugs and cell ids are
contracts from the first class that uses them. The window is still open.*

**7.48 — Every tutorial has a page of problems, and some problems have no
tutorial.**
Fourteen practice pages became thirty-two: one for every tutorial except the
three that are already problems or reflection — *Bringing It All Together*,
*Looking Back Before Moving Forward* and *The Team Project*.

Three sources fed them, and only one is a transcription in any sense.

**`deweydex/Mathematics`** has twenty-six worksheets under `markdown/`, twenty
of which carry an answer key in the file. The claim in `planning/EXERCISES.md`
that all of them do is wrong: `04e`, `07a`, `07c`, `07d`, `08a` and `08b` have
answers only as PDFs under `pdfs/solutions/`. Those six are also the ones whose
material is not yet taught, so nothing was lost.

**`deweydex/everlearning`** has thirty-eight programming problems in
`PracticeProblems/PDP-Practice-Problem-Bank.py`, as blank stubs with docstrings
and no answers at all. Those gave questions; every answer here was written.

**The tutorials themselves** are the third source, and the largest. Every "your
turn" prompt is a problem that was already set and never answered.

*Cost to change: thirty-two files. The frontmatter contract is one line each.*

**7.49 — `practice_across:` for a set of problems with no single owner.**
Some problems are only worth setting once several tutorials are behind you, and
giving one of them ownership would be a lie about what the page needs. So a page
may name several tutorials instead of one.

The asymmetry is deliberate: a mixed set links to everything it draws on, and
nothing links back. A tutorial has one companion page of problems, reachable from
its own last paragraph, and a reader who has just finished it does not want to be
sent somewhere that assumes six more.

That leaves mixed sets as the only pages on the site nothing else links to, so
they are listed on the contents page under their module — after the series,
before the archive, which is the only place in that list they belong.

*Cost to change: about ninety lines of build.py and fourteen tests. The four
pages using it are content, and would survive a different mechanism.*

**7.50 — Twenty-one numbers in answer keys were wrong before they were run.**
Not a decision, a measurement, and the reason the practice pages took as long as
the tutorials did.

Among them: binary search costing 9 comparisons where it costs 8; two roots of an
ambiguous triangle; a Heron semi-perimeter; a standard deviation out by a tenth;
a password-cracking time out by a quarter; where `2**x` overtakes `x**3`; and
when compound interest first beats simple by a hundred euro.

Every one was plausible, and none would have failed a test — no test asserts on
prose. The only thing that finds them is running the arithmetic, which is cheap
and has to be done deliberately.

Two answers were also written as a wrong attempt followed by its own correction,
on the theory that the correction was instructive. It is not, in an answer key:
a student checking their work against an answer that argues with itself learns
that the page is unreliable. Both were straightened.

*Cost to change: nothing. This is a note to the next person writing an answer.*

**7.51 — Tutorials link back to the mixed sets after all.**
7.49 decided that a mixed set links out and nothing links back, on the grounds
that a reader who has just finished one tutorial should not be sent somewhere
assuming six more. Josh asked for the reverse: "it would indeed be great if we
could reach more practice from each tutorial."

He is right that discoverability was the weaker half of that argument. A page
nothing links to is a page nobody finds, and the contents page is not where a
reader is standing when they finish a tutorial.

The objection is answered by saying so rather than by hiding the link. A tutorial
now shows its own practice page first — *worth doing when you have finished
reading* — and then any mixed set that names it, marked *for later, once more of
the course is behind you*, followed by the names of the other tutorials it draws
on. A reader can see at a glance whether it is for them yet.

*Cost to change: about thirty lines of build.py and four tests. Two existing
tests encoded the old decision; one was rewritten to assert what still holds,
and the other turned out to be asserting on the whole page when it meant the
navigation bar, which is a better test now than it was.*

**7.52 — Two folds, and a build check that a fold names one of them.**
Josh, on whether the harder problems should carry a hint: "the idea is to have
steps in a dropdown that they might follow if they are stuck, with some
reflection and next question at the end of each dropdown so they can think
things through in a related question."

So there are two folds. `dl-hint` holds numbered steps and closes with a
**Think about** and a **Try this next**; `dl-answer` holds the answer. The hint
comes first, in warmer colour, because opening it should not feel like giving up.

The reflection at the end is the part that makes this more than a spoiler. A
hint that ends at the answer teaches the answer; one that ends in a related
question the same steps solve teaches the method.

Twenty are written so far, across the four mixed sets — the hardest problems in
the repository and the ones Josh was asking about. The per-tutorial practice
pages have none yet.

`build.py` now fails on a `<details>` whose class is neither. This is worth the
six lines: bare `<details><summary>` is what plain HTML looks like, an earlier
draft of the style guide showed exactly that, and the failure mode is silent —
the fold renders as a browser-default triangle sitting in the prose.

*Cost to change: the classes are in the markdown of every practice page. The
check is six lines and five tests.*

**7.53 — Four tutorials re-released, and what the trial found.**
Josh asked for the versioning system to be tried on real content: "some of the
sections that are more traditional and use more imperatives — you can just pick
4 that are diverse in their subject matter."

*First Steps* (introductory programming), *Numbers and Their Families* (number
and algebra), *What Are the Chances* (probability) and *Putting Things in Order*
(algorithms). All four were among the highest in the repository for command
language, being converted from notebooks, and they cover four different
subjects.

Each is now a folder: the working copy at `2026.08.23.2` and the previous
release frozen at `v2026.08.23.1.md`. Thirty-one tutorials became a hundred and
fifty-two pages.

The trial did what a trial is for. **Three defects, none of which any test would
have caught:**

**The curriculum map counted every release as a tutorial.** It reads every `.md`
under `tutorials/`, so the four re-released ones appeared twice: the sequence
graph came out with two nodes called T1 and thirty-one tutorials became
thirty-five. Fixed by giving the map build.py's rule — newest live release
answers for the tutorial — in a `newest_live` function of its own, with five
tests, four of which fail against the old behaviour.

**Two releases on one day were indistinguishable.** The picker shows a date, and
both said "23 August 2026". A student choosing between two identical options is
choosing at random. The sequence number is now shown, and only where it is
needed, so an ordinary tutorial released once keeps a plain date.

**One cell had never worked on a fresh page.** *Numbers and Their Families* has a
`explore_number` that calls `classify_number`, which the student is asked to
write in an earlier cell that ships empty — so it raised `NameError` for anybody
who ran it before doing the exercise. It reports what is missing now instead.
The frozen release keeps the bug, which is what a frozen release is for.

*Cost to change: the folder layout is what build.py already expected. Undoing a
release means moving the file back and deleting the frozen copy, and is free
while no class has seen either.*

**7.54 — The first bibliographies.**
Josh's guide requires one in every tutorial; none had one. These four now do,
four or five entries each, chosen to be genuinely worth an hour rather than to
fill a section — Timo Bingmann's sorting visualisation, 3Blue1Brown on
logarithms, the Python documentation on floating point, Downey's *Think Python*.

Thirty-one to go. That is the largest single piece of style work outstanding and
it is not mechanical: a bibliography of plausible-looking links is worse than
none, because a student who follows a dead one stops following any of them.

*Cost to change: per tutorial, and each needs a person who knows the sources.*

**7.55 — 5N0554's thirteen outcomes, and where the examples went.**
Transcribed from the descriptor PDF into `outcomes.yaml`, under a new `CMPS`
module. The descriptor states each outcome and then, for most of them, an
"e.g." — Google PageRank, ASCII art, PKI, a server room's temperature. Those
examples are suggested content, not the outcome, and the map's coverage has to
be measured against the outcome or a tutorial that teaches PageRank and
nothing else would read as having taught LO4 in full. So the wording in
`outcomes.yaml` is the outcome stripped of its examples, and every example
moved to that code's `uses:` in `topics.yaml`, alongside the `name`, `plain`
and `needs` every other topic already carries.

Two outcomes bundle more than one idea under one descriptor number — LO1 pairs
data structures with iterative-versus-recursive algorithms, and several of
LO7–LO13 are closer to a paragraph than a sentence. Left as one code each,
matching the descriptor's own numbering rather than splitting further:
`covers:` is keyed on these codes, and inventing sub-codes the descriptor does
not have would be the tutorials disagreeing with the assessment document they
have to answer to.

`dev/curriculum_map.py` confirms what this is expected to say: thirteen new
red squares, all thirteen listed as having no proposal yet, because a
paraphrase of a descriptor is not a lesson plan.

*Cost to change: two files, twenty-six entries between them. The wording is a
paraphrase rather than a legal transcription, so restating any one of them
costs nothing the descriptor itself would object to.*

**7.56 — The first 5N0554 strand: six tutorials, and PageRank rides along
rather than getting its own.**
`planning/outlines/matrices.md` planned five tutorials plus a Markov chains
tutorial plus an open question about where PageRank goes. Built as six:
*A Grid of Numbers*, *Multiplying Grids*, *What a Matrix Does to a Picture*,
*Undoing It*, *Solving Systems*, and *Where Chains Lead* — the last folding
weather prediction, convergence, word-level text generation, and a
hand-checkable three-page PageRank example into one tutorial rather than
four. Module `computational-methods`, a new series called `matrices`,
alongside the existing `python-fundamentals`.

Sourced rather than invented, per the instruction that started this: worksheet
`07a_matrix_operations` gave the add/scale/transpose/multiply arithmetic in
*A Grid of Numbers* and *Multiplying Grids*, `07b_linear_systems` gave the
augmented-matrix and row-operation framing in *Solving Systems*, and
`07d_markov_chains` gave the Dublin weather example and the three-page
PageRank problem in *Where Chains Lead*. All three worksheets have their
answer keys only as PDFs, so every number that reached a tutorial or its
practice page was worked fresh in Python and checked against the worksheet's
own claims where one existed (problem 30 in `07a` asserts $(2,1)$ solves
$2x+3y=7, x-y=1$; that assertion is what *Solving Systems* opens with,
confirmed rather than copied). The word-transition example in *Where Chains
Lead* uses the opening sentence of Dickens' *A Tale of Two Cities*, which
`everlearning/OtherCourses/Markov-Chains-and-Text-Generation` also trains on
and which is public domain either way.

**PageRank rides along, closing the open question in `matrices.md`.** A
three-page link graph, solved by the same repeated-multiplication technique
the tutorial had just built for weather, is three cells — not a tutorial's
worth of new machinery, and building one anyway would have meant padding it
with material (crawling, a larger graph, damping factors) this module does
not ask for. A dedicated PageRank tutorial over a real link graph is still
open, and now a smaller piece of work than it was, since the core mechanism
is already taught.

**Closes `CMPS-LO4` in full**, touches `CMPS-LO1` (the data-structures half,
not the recursion half) and `CMPS-LO2` (the randomness half, not the
distributions or independence half) — see the curriculum map. Nine outcomes
remain untouched: `CMPS-LO3`, `LO5` through `LO13`. Those are the discrete
simulation, algorithmic complexity, and problem-solving strands STATUS.md
lists as not started.

*Cost to change: six tutorials, six practice pages, one series file. Nothing
downstream depends on this strand yet — matrices.md itself said so — so
reshaping it costs only the content, not any other page's links.*

**7.57 — What the browser QA pass caught, run before this pushed.**
Every cell of the six new tutorials was run in a real Chromium against a
self-hosted Pyodide, with a correct solution injected into every blank "your
turn" cell before running it — otherwise a NameError from an unstarted
exercise stops meaning anything, since it is not testing the tutorial, only
confirming a blank cell is blank. The practice pages needed no injection:
every runnable cell on a practice page is a tool cell, and the worked
solutions live in `dl-answer` folds as inert markdown, not as `exec` cells.

Two real bugs turned up, neither of which any of the numeric checking would
have caught, because both were about what does and does not carry over
between pages rather than about arithmetic.

**`Multiplying Grids` never defined `transpose`.** Its own prose says "you
already wrote something that turns columns into rows: `transpose`, from the
last tutorial" — true of the *tutorial*, false of the *page*: each tutorial
is its own Pyodide instance, nothing carries over, and a student arriving
fresh at tutorial 2 has no `transpose` in this page's namespace at all. Fixed
with a one-line recap cell, given rather than a "your turn" — the point of
this tutorial is multiplication, not making someone re-derive transpose a
second time.

**A "your turn" cell's own shipped starter was the fix, not the bug** — in
`Undoing It`, the QA script's first pass overwrote a cell whose entire
starter was `import matplotlib.pyplot as plt`, and broke on the resulting
`NameError: name 'plt' is not defined`. The tutorial was right; the harness
had dropped a line it should have kept. Recorded because it is the kind of
false positive that erodes trust in this exact check if it happens quietly —
worth naming so the next QA pass looks at the starter before assuming a
failure is the tutorial's fault.

*Cost to change: two lines, once each. The QA script itself is not
committed — it lives in the scratchpad, per the instruction that started
this, as a tool rather than a test.*
