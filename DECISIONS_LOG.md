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

**7.58 — Three wrong citations in the matrices strand's bibliographies,
caught by checking each video id rather than trusting the author's own
memory of it.** The style guide asks for a bibliography in every tutorial
(section 6) and the matrices strand is the first to actually have one in
every file — worth a second pass precisely because it is the first, and a
pattern of small factual slips here would spread to every strand that copies
its shape.

Checked every entry against the video id or paper it links to, not against
what seemed plausible. Three did not match what they claimed:

**`Multiplying Grids`** attributed the 3Blue1Brown video at `aircAruvnKk` to
"Ben Eater and Grant Sanderson (2022)". It is Grant Sanderson alone,
published 2017 — *But what is a neural network? | Deep learning, chapter 1*.
Ben Eater had no part in it.

**`Solving Systems`** labelled the video at `P2LTAUO1TdA` "Chapter 9" of
*Essence of Linear Algebra*. It is chapter 13. Chapter 9 of that series is
*Dot products and duality*, a different video entirely.

**`Where Chains Lead`** cited "Grant Sanderson (3Blue1Brown) (2022). *Markov
Chains.*" at `JGSaEwGZoDE` — a video id that does not resolve to anything,
and 3Blue1Brown has no video by that title. Replaced with a real one that
fits the same role and the guide's own list of preferred sources: Josh
Starmer's StatQuest video *Markov Chains Clearly Explained! Part 1*
(`i3AkTO9HLXo`, 2020). The same tutorial's Page and Brin citation had the
authors in reverse order from how the paper is conventionally cited — fixed
to Brin first, matching the paper itself and every index of it.

Every other entry across the six tutorials — five more 3Blue1Brown chapter
numbers, the Strang, Downey, Hughes et al., BetterExplained, Shannon and
Dickens citations — checked out against a real search rather than being
assumed correct by association with the ones that did not.

*Cost to change: four lines, once each. The failure mode this guards
against is a plausible-sounding citation nobody follows — see 7.54 on why a
bibliography of dead or wrong links is worse than none.*

**7.59 — The editor's prose surface is now a Milkdown (Crepe) block editor,
vendored the same way as CodeMirror and KaTeX, with no framework adopted.**
`planning/REPO_AND_EDITOR.md` specified this for editor v1 from the start —
"live, borderless block editing" rather than raw markdown in a box — and what
shipped instead was a plain `<textarea>` wrapped in the reordering,
frontmatter, and release machinery around it. That gap sat unnoticed until an
outside critique of dewlab (mistakenly diagnosing it as an unoptimised React
single-page app, which it has never been) happened to recommend a React
block-editor library for the wrong reasons, on the wrong codebase — and
pointed at a real gap between this repository's own plan and what it had
actually built.

Milkdown's Crepe preset was chosen over the critique's own suggestions
(BlockNote, Tiptap, Lexical, Novel.sh) for one reason none of those satisfy:
its API is plain JavaScript, not React. `deweydex/faq` already uses it, and
only wraps it in Preact because FAQ itself is a Preact app — the underlying
`new Crepe({ root, defaultValue, features })` needs no component framework at
all. Bundled with esbuild in `vendor-src/` into `assets/vendor/milkdown.bundle.js`,
committed like the other two vendored libraries, so neither CI nor an author
previewing a tutorial locally needs Node installed for the ordinary case.

Two things were true of Crepe that the library's own documentation does not
warn about, both found by actually driving the built editor in a real browser
rather than trusted from reading the API: it fires its `markdownUpdated`
callback once while still parsing the *starting* document, before a reader
has touched anything, which without a guard made opening any tutorial and
touching nothing look like an edit; and its code-block feature keeps only the
first word of a fence's info string as its "language", which round-trips
`python exec` back out as plain `python` — silently turning a runnable cell
into inert illustrative code the moment it passed through an unmodified
save. Both are fixed (`vendor-src/milkdown-entry.js`'s hydration guard,
`editor.js`'s `restoreExecTag()`, keyed off the same `id:`-first-line
convention `build.py` already uses to mean "this fence is a cell") and both
have browser tests driving the real editor rather than a stand-in, in
`tests/e2e/test_editor.py`.

*Cost to change: moderate. Reverting to a `<textarea>` is small — delete the
Crepe mount, restore the input listener — but would be giving up exactly what
this entry exists to close. Swapping to a different block editor later means
re-solving the exec-tag round-trip problem, if the replacement has the same
one-word-language limitation; nothing else here should be library-specific,
since `restoreExecTag()`, `problems()`, and the release logic all operate on
plain markdown text rather than on Crepe's own document model.*

**7.60 — The editor gained code completion and a dead-link check; a hover
docstring in Crepe's own code blocks was attempted and pulled back out.**
Three of these landed and are covered by tests/e2e/test_editor.py and
tests/e2e/test_autocomplete.py: `problems()` now checks `tutorial:slug#anchor`
links against every other tutorial's real slugs and anchors — the one class
of mistake build.py already refused that the editor's own report did not
catch, closing that gap rather than leaving it for CI to find first
(`tutorialLinkProblems()`, `assets/editor.js`); both the editor's code
blocks and a student's own cells gained keyword/builtin and locally-typed-name
completion, wired from CodeMirror's already-vendored `@codemirror/autocomplete`
and `@codemirror/lang-python` — genuinely close to free, since both packages
were already dependencies for close-brackets and syntax highlighting; and a
student's cell additionally gained *live* completion and a real hover
docstring, reading `tutorial_tools._page_globals` and `inspect.getdoc()` off
the actual interpreter running that page (`pageNamesCompletion`, `docFor`,
`assets/tutorial-runtime.js`) — accurate by construction, since there is
nothing bundled to fall out of date with the running interpreter.

The fourth piece — the same hover docstring inside the *editor's* own code
blocks, for `module.name` written out in full (plt.plot, pd.DataFrame, …) —
does not have a live interpreter to read from, so it was built to answer
from `assets/editor-doc-snippets.js` instead: real docstrings, captured once
from a real Pyodide by `dev/generate_doc_snippets.py`, for a small,
grep-derived set of names the curriculum actually calls (that script's own
comment has the full account, including why numpy is not in the list — it is
not currently called as `np.anything` anywhere in `tutorials/` or `setup/`).
The CodeMirror wiring — `hoverTooltip()`, the identical extension shape
`codemirror-entry.js` uses successfully for a student's own cells — compiled,
ran with no error, and simply never surfaced a tooltip inside Crepe's
code-block feature specifically: not from a real mouse hover, not from a
Playwright-driven one, despite confirming the underlying `mousemove` event
genuinely reaches the code block's DOM node. Ruled out along the way: a
`hoverTooltip()`-returns-a-wrapper-object mistake (`{ active, extension }`,
not a plain `Extension` — real, fixed in both files, and worth having fixed
regardless of whether it was the cause here) and Crepe's code-block instance
not yet existing at hover time (it was — the same click-then-hover sequence
that works for a student's cell was tried here too). Not chased past that;
Crepe's code-block feature is evidently doing something to the CodeMirror
instances it hosts that `autocompletion()` — confirmed working in the same
file — does not run into, and finding what wants reading Crepe's own
ProseMirror node-view integration for the code-block feature more closely
than this pass had the budget for.

*Cost to change: the three landed pieces, small — each is a self-contained
static function plus a documented CodeMirror extension. The fourth: the data
and the generator are real and committed, unused only because nothing reads
them yet. Whoever picks it back up should start from confirming whether
Crepe's other hover-driven UI (the link-edit popover, the language picker)
uses `hoverTooltip()` internally or something else entirely — if it is
something else, that is probably the answer.*

**7.61 — `load()` reads a repository's files in concurrent batches of 16,
not one at a time.** Noticed live, not in a test: the editor's own
Playwright-driven suite never caught this because its fake GitHub client
resolves instantly, with no network latency to expose a loop that awaits
each request before starting the next. Against the real repository — 90-odd
files under `tutorials/`, each its own GitHub Contents API round-trip — that
loop was 15-25 seconds of an author staring at "Reading the repository…"
before seeing a single tutorial, entirely serial for no reason the code
itself needed.

Batched rather than one `Promise.all()` over every file: GitHub's secondary
rate limiting is real, and 90-odd simultaneous requests from one token reads
as closer to abuse than a person opening a page. 16 at a time is a guess at
a reasonable middle, not a measured optimum — nothing here needed it to be
exact, only better than fully serial. `tests/e2e/test_editor.py`'s
`TestLoadingManyTutorialsAtOnce` covers the part a fake client's own instant
resolution could otherwise hide: a 40-tutorial repository, read once with
requests resolving in call order and once with a random delay on each so
they resolve out of order, checked both times for the same thing — every
tutorial present, its title matched to its own slug, no batch-index mistake
scrambling one request's text onto another's path.

*Cost to change: trivial — one constant (`READ_CONCURRENCY`). Raising it
trades a faster load for a higher chance of a real GitHub rate-limit
response on a large enough repository; nothing currently retries or backs
off if that happens, which would be the next thing to add before raising it
much.*

**7.62 — The editor gained a search-and-insert tutorial link picker, and it
uncovered a real bug in `@milkdown/utils`'s own `insert()` helper.**
`tutorialLinkProblems()` (7.60) catches a `tutorial:slug#anchor` link after
it is typed wrong; this is the other half — a toggle above the prose editor
that searches every known tutorial by title, slug or module
(`matchTutorials()`, `assets/editor.js`) and inserts a real link at the
cursor, so an author reaches for a tutorial that exists rather than
remembering a slug and finding out it was wrong from the report afterward.

The first working version used `@milkdown/utils`'s own `insert(markdown,
true)` — the obvious, documented way to put markdown at a selection — and
it silently produced a link with no href every time. Two separate bugs, both
found by asserting on what `getBody()` actually returned in
`tests/e2e/test_editor.py`'s `TestLinkPicker`, not by trusting either call's
default behaviour: (1) `insert()`'s inline path round-trips the parsed
content through a real DOM node — `DOMSerializer.serializeFragment()` then
`DOMParser.parseSlice()` — before inserting it, and the commonmark preset's
link mark sanitizes `href` down to empty for any scheme outside
http/https/mailto/tel/ftp (`sanitizeLinkHref`, a real and correct guard
against a mark rendering as `<a href="javascript:...">` in the editable
DOM) — which means it also erases `tutorial:` before the round trip's
second half ever reads the href back, a case that guard was never meant to
catch and had no way to tell apart from one it was. (2) Once past that, by
building the link mark directly instead of going through `insert()`,
`replaceSelectionWith(node, true)` — `true` is the default — still dropped
it: `inheritMarks: true` means prosemirror-state's own implementation calls
`node.mark(marksAtCursor)`, which *replaces* the node's marks with whatever
is active at the cursor rather than merging, and a cursor at the end of a
paragraph typically carries none. `insertLink(title, href)`
(`vendor-src/milkdown-entry.js`) now builds the text node and its link mark
straight against the schema, with no DOM step in between, and calls
`replaceSelectionWith(node, false)`.

*Cost to change: small — `matchTutorials()` is a pure function over
`allTutorials()`'s existing shape (already computed for
`tutorialLinkProblems()`); the picker itself is plain DOM, no ProseMirror
plugin surgery, which is why this one shipped where 7.60's hover tooltip did
not — nothing here depends on Crepe's own code-block internals. Both
`insertLink()` bugs are worth remembering if anything else in this codebase
ever reaches for `@milkdown/utils`'s `insert()` for a mark-bearing inline
node, or for `replaceSelectionWith` at all: check what's active at the
cursor before assuming `inheritMarks: true` is harmless.*

**7.63 — The slash menu was fully transparent and the text cursor never
appeared, because Crepe's structural stylesheet reads ~25 custom properties
that only one of its own skins defines, and this editor loads neither.**
Reported live, by a person actually using the editor rather than surfacing
in a test: the `/` command menu was there but unreadable, sitting
transparent over whatever text was behind it, and typing produced no
visible caret to type against at all.

`milkdown-entry.js` deliberately imports only `@milkdown/crepe/theme/
common/style.css` — the structural rules — and none of Crepe's skins
(`crepe`, `crepe-dark`, `frame`, `nord-dark`), because a skin is a fixed
colour scheme and this editor retextures the same elements from dewlab's
own `--dl-*` variables instead, so it follows the reader's light/dark
choice like the rest of the site. What that comment did not yet reckon
with: the structural stylesheet does not carry its own colours at all — it
reads them from `--crepe-color-*`, `--crepe-font-*` and `--crepe-shadow-*`
custom properties (surface colours, hover/selected backgrounds, even the
virtual text cursor's own colour), and only a skin defines those. With
none loaded, every one of ~25 properties was undefined, and a `var()`
reference to an undefined custom property with no fallback is invalid at
computed-value time — which resolves to that property's own *initial*
value, not anything Crepe intended: `background: var(--crepe-color-
surface)` on the slash menu came out `transparent` (background's initial
value), and the replacement caret `prosemirror-virtual-cursor` draws after
hiding the real one (`caret-color: transparent` on the `.ProseMirror`
element itself — correct, deliberate, how that package works at all) got
its own `border-color` from `--crepe-color-outline`, equally undefined,
and came out invisible too.

The existing fix for the one instance of this already found (7.60's
editor styling pass had already patched the slash menu, block handle, and
link/latex popovers' *background* by hand, four class selectors at a
time) turned out not to be reliably winning the cascade at all — verified
live with `getComputedStyle()`, not assumed, the override rule and Crepe's
own rule are equal specificity, and source order between two separately
built stylesheets is not something to depend on. The real fix is
upstream of all of that: define the ~25 `--crepe-*` custom properties
themselves, once, mapped to the matching `--dl-*` token
(`.dl-editor-body .milkdown` in `tutorial-style.css`) — every downstream
`var(--crepe-color-surface)` across Crepe's *entire* structural
stylesheet then resolves correctly from that one place, including
elements this pass never went looking for individually (the code block's
own surface, list markers, table borders, the image-block and AI
features' own popovers even though neither is enabled) — which is also
why the four-selector override block shrank down to just a `border` (Crepe's
own popovers use box-shadow alone for definition; this editor still wants
a crisper edge) once the variables underneath it were actually real.

Worth remembering for its own sake: the first attempt at this fix silently
did nothing, for a third, unrelated reason — the explanatory comment
written above the new rule contained the literal text
"`--crepe-color-*` and `--crepe-font-*`" side by side, and the `*` ending
one word immediately followed by the `/` starting the next formed a
literal `*/`, which closed the CSS comment early. Everything from there to
the block's real closing `*/` was then parsed as CSS source, not comment —
found by checking `getComputedStyle()` in a real browser and seeing the
custom property come back empty despite the rule visibly being present,
byte for byte, in the served file; a syntax error inside a CSS comment
produces no error anywhere, only a silently different stylesheet.

*Cost to change: the mapping itself is cheap — one block of `--dl-*`
references, no new colours invented. The real cost is trusting a browser's
CSS cascade or its comment parsing by reading the rule rather than
querying `getComputedStyle()` against a real, rendered page; both bugs
this entry describes, and the meta-bug in fixing the first one, would have
shipped unnoticed by any amount of re-reading the CSS text.*

**7.64 — The reading page gained a cheat sheet, assembled per tutorial so it
never shows a reader something they have not been taught yet.** Full design
in `planning/CHEAT_SHEETS.md`; this is the shape of what landed.

A glossary file (`<slug>.glossary.yaml`) says what one specific tutorial
introduces — a new sibling of the tutorial's own `.md`, not frontmatter,
because a build already reads frontmatter for other reasons and a bad
glossary entry should fail the build the same way a bad `covers:` entry
does (`own_glossary()`'s `kind`/`term`/`definition` checks, `build.py`).
`cumulative_glossary()` walks a series in `order.yaml` order — the same
`members` list `nav_for()` already uses for previous/next — accumulating
each member's own entries into the next, so a tutorial's manifest carries
its own glossary plus everything before it and nothing after. A practice
page has no series position that means anything of its own
(`practice_for`/`practice_across` name what it tests, not where it sits),
so its cheat sheet is the union of the tutorial(s) it names instead —
resolved through the exact same `registry` lookup `practice_pairs()`
already validates, not a parallel mechanism.

The panel itself reuses `.dl-settings`'s own floating-card positioning
rather than inventing a second panel language, anchored to the same corner
on purpose — and the two now close each other on open
(`closeCheatSheet()`/`closeSettings()`, `tutorial-runtime.js`), since
showing both at once would overlap. The toggle is the one new thing with no
existing analogue: pinned to the page's own top-left corner, independent of
the masthead (which already gives its left side to the wordmark), starting
`hidden` in `shell.html` and revealed only when `initCheatSheet()` finds a
non-empty `manifest.glossary` — a tutorial with nothing accumulated yet,
which is every tutorial for a while, offers no button at all rather than
one that opens onto an empty panel.

That toggle's own CSS shipped broken on the first pass, caught by
`tests/e2e/test_cheat_sheet.py`'s `TestVisibility` rather than by reading
the rule: `.dl-cheatsheet-toggle`'s unconditional `display: inline-flex`
has the same specificity as the browser's own `[hidden] { display: none }`
and, loading later, won the tie — showing the button regardless of the
`hidden` attribute JS uses to hide it. `.dl-cheatsheet-toggle[hidden] {
display: none }`, stated explicitly rather than assumed, fixed it. The
`.dl-settings-toggle` this was modelled on never hit this, because that
button is never itself hidden — only its panel is — which is exactly the
kind of difference that is invisible until a test actually asserts on it.

Producing the glossary files themselves — the part that makes any of this
show real content — is `.claude/skills/tutorial-glossary/SKILL.md`, run
tutorial by tutorial in series order, deliberately built on top of the
first-use `*emphasis*` convention `dev/curriculum_map.py` already relies on
(`EMPHASIS_RE`/`terms_of()`) rather than reading each tutorial cold: most of
a tutorial's glossary candidates are already marked, by an author who was
told to mark them, before the skill reads a word of prose.

*Cost to change: the schema and accumulation logic, small — one YAML shape,
one pure function per concern (`own_glossary`, `cumulative_glossary`), fully
covered by `tests/test_build.py`'s `TestTheCheatSheet` without touching a
browser. The panel and toggle, small — CSS and markup mirroring
`.dl-settings` throughout. The real cost is everything this entry is not
about: actually running the skill across the curriculum, tutorial by
tutorial, in series order, which is most of the remaining work and is
tracked separately rather than bundled into this PR.*

**7.65 — Every tutorial in both live modules now has a glossary file, so the
cheat sheet described in 7.64 shows real content everywhere rather than only
where a handful of hand-written examples put it.** Run per `.claude/skills/
tutorial-glossary/SKILL.md`, series by series, in `order.yaml` order:
`computational-methods`' `python-fundamentals` and `matrices` series (8
tutorials), then `mit-pdp-maths-prog-integration`'s `maths-and-programming`
series (all 31), then its `reflections-and-review` series (2). A handful of
tutorials — `bringing-it-all-together`, `critique-and-reflection`,
`the-team-project` — got an empty `entries: []` rather than no file at all,
each with a comment saying why (a stated review with nothing new, or a
project brief with no code), which keeps "this tutorial was deliberately
considered and has nothing to add" distinguishable from "nobody has gotten
to this one yet" (the latter still resolves to an empty list either way, by
`own_glossary()`'s missing-file case in 7.64 — the file's only audience is a
future reader of the repo, not the build).

One same-word collision surfaced doing this: *tangent* already names the
trig ratio (`the-unit-circle.glossary.yaml`), and `rates-of-change.md`
introduces an unrelated *tangent line* for the derivative. Reusing the term
string `tangent` there would have `cumulative_glossary()`'s
first-definition-wins dedup silently keep the trig definition and drop the
calculus one — caught only by writing the tangent-line entry and finding it
missing from a rebuilt manifest. Fixed by using the distinct term string
"tangent line" for the second meaning rather than teaching the dedup logic
about senses of a word, with a comment at the top of the file recording why
the two are separate entries on purpose. `making-decisions.glossary.yaml`
already carries a related note from earlier in this rollout, about a
tutorial's own prose citing the wrong predecessor for where N/Z/Q/R were
first covered; the glossary there follows the real `order.yaml` sequence
rather than the tutorial's own (incorrect) claim, and does not re-teach
those names in `numbers-and-their-families.glossary.yaml` where the
same content is genuinely first covered per the tutorial's prose — a
content fix for the prose itself is tracked as a follow-up task rather than
made part of this rollout.

Practice-page resolution was verified against real builds rather than only
unit tests, across both modules: every single-target practice page compared
equal to its target tutorial's own manifest glossary, and all four
`practice_across` "mixed" pages in `mit-pdp-maths-prog-integration`
(`mixed-programming`, `mixed-algebra`, `mixed-data`, `mixed-trigonometry`)
compared equal to the union of their named targets' manifest glossaries —
confirming `cumulative_glossary()`'s practice-page branch, exercised so far
mostly by hand-written fixtures in `tests/test_build.py`, holds up against
the full, real curriculum.

*Cost to change: none of this changes the mechanism from 7.64 — it is
content, not code. Adding a glossary for a tutorial written after this
entry, or correcting one, is exactly the workflow `.claude/skills/
tutorial-glossary/SKILL.md` already describes: one tutorial, the cumulative
glossary of what came before it in its series, one YAML file out.*

**7.66 — A cheat sheet may cross series within a module; it still never
crosses modules.** Answers `QUESTIONS.md`'s open question from 7.64:
matrices comes after Python fundamentals for a reader working through
`computational-methods` in the obvious order, so a matrices tutorial's
cheat sheet should carry fundamentals' vocabulary too, not stop at its own
series' boundary the way 7.64 originally shipped.

An optional `tutorials/<module>/series.yaml` (`order:`, a list of series
slugs — the same shape `tutorials/modules.yaml` already uses for the
module-display order it is modelled on) says the order a module's series
accumulate in. `series_chain()` builds the walk: every tutorial in every
series listed *before* this one, each in its own `order.yaml` order,
followed by this series' own members in theirs. `cumulative_glossary()`
now walks that chain instead of one series' `members` list, so its
signature dropped `members` entirely — `series_chain()` already has
everything it needs from `groups`, the same dict the function already
took.

The one thing this could not be allowed to break silently:
`reflections-and-review`, in `mit-pdp-maths-prog-integration`, is not on
any linear route through its module — its own `.order.yaml` comment
already explains why: "it is not the last thing you do — it is the thing
you come back to whenever you have finished something worth looking at
again." A series left off `series.yaml` (or a module with no such file at
all) keeps 7.64's original series-only accumulation unchanged, which is
exactly what leaves `reflections-and-review` alone — nothing about it
needed to change, because that module's `series.yaml` (if it had one)
would simply never list it. `computational-methods/series.yaml` lists
`[python-fundamentals, matrices]`; `mit-pdp-maths-prog-integration` gets no
file at all, since it has only one series with a real position to begin
with.

`check_series_order()` fails the build if a `series.yaml` names a series
that is not real in that module — the same reasoning `series_of()` already
applies to a slug listed in an `order.yaml` with no tutorial behind it: a
typo here would otherwise silently exclude a series from cross-series
accumulation, with nothing else ever saying why a cheat sheet was missing
content.

*Cost to change: small. `series_chain()` and `check_series_order()` are
each a short, pure function, covered by `tests/test_build.py`'s
`TestCrossSeriesGlossary` (inherits across a listed order, stays
series-only with no file, stays series-only when left off an existing
file, fails loudly on an unknown series name). Verified against a real
build too: `grid-of-numbers`, the first matrices tutorial, now carries
`working-with-tables`' 8 fundamentals entries ahead of its own 11.*

**7.67 — A cell's control bar moved below the editor and output, and its
hint stopped floating.** Two real usability problems, reported directly
against the live site rather than found in review: the bar (slug, hint,
reset, run) sat above the code, so a reader met controls for code they had
not read yet; and the hint's "?" opened a hover popover
(`position: absolute`) that could float over the editor or output beneath
it, and gave a touch reader no way to open it at all.

`render_cell()`'s markup order changed — bar now last inside `.dl-cell` —
with no change to how `tutorial-runtime.js` binds to any of it, since
every binding is a class lookup (`.dl-editor`, `.dl-output`,
`.dl-btn-run`, `.dl-btn-reset`) rather than a DOM-position assumption. The
hint became a real click toggle: `.dl-hint-icon` is a button with
`aria-expanded`, `.dl-hint-text` is `hidden` by default and a plain block
when open (not `position: absolute`), so opening it grows the cell and
pushes whatever follows it down the page — the same "push down, cover
nothing" shape the prose-level `<details class="dl-hint">` fold already
had, reached by a different mechanism because `<details>` does not fit as
one icon inside a horizontal bar. `[hidden]` gets the same explicit
`.dl-hint-text[hidden] { display: none }` rule 7.64 already needed for the
cheat sheet toggle, for the same specificity-tie reason.

A second ask alongside this — the Run button becoming a Stop button while
a cell runs — was investigated and not built: `planning/CELL_CONTROLS.md`
§2 has the finding. Pyodide runs on the page's own main thread with no Web
Worker anywhere in the codebase, so a genuinely blocking loop leaves no
thread free to even handle a Stop click; the only real fix is a Worker
plus `pyodide.setInterruptBuffer()`, which needs `SharedArrayBuffer`,
which needs cross-origin-isolation response headers GitHub Pages does not
let this project set without a service-worker shim. Raised in
`QUESTIONS.md` as its own decision rather than folded into this PR.

*Cost to change: small for what shipped — `tests/test_build.py` gained two
tests (hint starts closed and is a toggle not `role="tooltip"`, bar comes
after editor/output in the markup) and `tests/e2e/test_cell_hint.py` is new
(starts closed, a click opens it in normal flow — asserted directly via
`getComputedStyle(...).position === "static"` and a real bounding-box
height rather than trusting the CSS — a second click closes it again),
run against a real browser with no cell run and no Pyodide boot required,
same reasoning `test_autocomplete.py`'s first class already established.
The Stop button is not a cost deferred cheaply — see `QUESTIONS.md`, the
Worker migration is real architecture work whenever it happens.*

**7.68 — A new skill reviews a tutorial's own code for naming and comment
quality, the same way `tutorial-glossary` reviews it for vocabulary.**
`PEDAGOGICAL_STYLE_GUIDE.md` §5 had cell-length, boilerplate, and tool
rules but nothing on variable naming or comment style — a real gap, since
"clearer, semantic variable names" needs somewhere authoritative to check
against, the same reason `tutorial-glossary` defers to `terms_of()`'s
existing emphasis convention rather than deciding term-worthiness itself.
§5 gained rules (semantic names over mathy single letters; comments that
say why, not what; two named exceptions — a formula's own letters
matching the prose above a cell, and "discover first, name afterwards"
applying to a variable's specificity the same way it already applies to
prose) before `.claude/skills/cell-code-review/SKILL.md` was written
against them.

The skill treats a rename as whole-tutorial, not per-cell — cells in one
tutorial share a namespace in document order, so a name reused across
cells has to be renamed everywhere it appears or the tutorial breaks
rather than improves — and requires validating an edited cell still
compiles and, where checkable, still produces the same output, before
calling a rename done.

Run once, by hand, across a handful of real tutorials rather than the
whole curriculum, to prove the process before committing to a full pass
(the same staged approach `tutorial-glossary` took, `CHEAT_SHEETS.md` §7):
`multiplying-grids.md` and `grid-of-numbers.md` needed nothing — `a`/`b`
in `dot(a, b)` and `A`/`B`/`C`/`D`/`S`/`M` for matrices both match names
already established in the surrounding prose, `pixels`/`ramp` were
already semantic. `how-we-got-here.md`'s `to_binary(n)` was left alone —
a general-purpose numeric conversion function's single parameter, already
explained by its own docstring, is the same shape as `dot(a, b)`'s
generic arguments. One real change: `undoing-it.md`'s `polygon_area()`
renamed its point-count variable from `n` to `point_count` (`i`/`j` left
alone as loop indices, exempted by name); confirmed identical output
(`area of the original square: 1.0`, before and after) and a clean
rebuild.

*Cost to change: small — the skill is a process document, no code of its
own. The style-guide rules it depends on are new text in an existing
section, not a new document. Running it across the rest of the curriculum
is real, separate work — tracked as a follow-up rather than attempted in
one pass, the same reasoning that kept `tutorial-glossary`'s own curriculum
run as several PRs rather than one.*

**7.69 — The cheat sheet stopped hiding on a phone; it becomes a bottom
sheet instead, the same treatment `.dl-settings` already had.** Settles
`QUESTIONS.md`'s mobile question from 7.64. The `@media (max-width: 34rem)`
rule that used to read `.dl-cheatsheet-toggle, .dl-cheatsheet { display:
none; }` now gives `.dl-cheatsheet` the exact same `top: auto; bottom: 0;
left: 0; right: 0; ...` block `.dl-settings` already had, rather than a
separate, parallel rule — one selector list, one set of rules, for two
panels that already behave identically at this width. The toggle needed no
change at all: it was always a small fixed corner button, not a floating
card, so it was never the thing that stopped working on a phone — only the
panel's shape was.

`tests/e2e/test_cheat_sheet.py`'s `TestMobile` — previously one test
asserting the toggle was hidden — is now two: the toggle stays visible, and
opening it produces a panel actually anchored to the bottom edge, checked
with `getComputedStyle()` (`position: fixed`, `bottom/left/right: 0`)
rather than trusted from the CSS alone.

*Cost to change: small — CSS only, one selector list gained a second
target, no JavaScript or markup changed. `tutorial-runtime.js` was
untouched, so `standalone.bundle.js` did not need rebuilding this time.*

**7.70 — Two progress indicators, both read from the saved-progress
record `saveNow()` already writes.** `planning/PROGRESS_INDICATORS.md`
designed both; this is what shipped, unchanged from that design in shape.

`saveNow()` gained one field per cell — `errored: !!cell.outputEl.
querySelector(".dl-error")` — captured once rather than re-parsing saved
`output_html` wherever the question "did this cell's last run fail" comes
up. `progressCounts()` is the one place that turns a list of
`{started, errored}` into `{total, done, errored}`, shared by both
surfaces below rather than two separate counting implementations.

**The contents page** gets a small badge (`1/2`, red background only when
at least one counted cell errored) next to a tutorial's title —
`render_index()` already knows `len(member.cells)` at build time, so a new
`progress_attrs()` helper writes it straight onto the link as
`data-module`/`data-slug`/`data-cells`, no fetch needed for
`renderContentsProgress()` to read that tutorial's own `localStorage`
record client-side. A tutorial with no saved record, or one where nothing
has been run yet, gets no badge — a `0/9` would read as a judgment on a
page nobody has opened. A new Settings toggle ("Show progress on the
tutorials list") governs this specifically, because it is the one
*ambient* piece — visible on every visit to the contents page whether or
not a reader wants a visible tally.

**A tutorial's own page** gets a plain summary line — "4 of 9 cells run ·
1 with an error" — folded into a new "Progress" section in Settings
(`updateProgressSummary()`, called after every save) rather than a
persistent bar competing with the cheat sheet's toggle for a screen edge,
per the original framing's own reconsideration in the design doc. Hidden
whenever nothing has been run yet, same reasoning as the contents page's
badge. No second toggle: unlike the contents-page badge, this line is
only ever seen by a reader who already opened Settings, which is opt-in
by where it lives.

One wrinkle the design doc called out and the implementation resolves the
same way: `#dl-settings-progress`, unlike `#dl-settings-work`, is **not**
removed on a page with zero cells — its toggle also governs the contents
page's own badges, and the contents page itself has no cells at all, so
the section has to survive there; only the summary line inside it stays
hidden in that case.

*Cost to change: small. `progressCounts()`/`liveProgressCounts()`/
`renderContentsProgress()`/`updateProgressSummary()` are each short, pure
or near-pure functions. Two new unit tests cover the build-time
attributes (`TestTheContentsPage`), and two new e2e files cover the rest:
`tests/e2e/test_progress_summary.py` runs real cells (a real traceback,
not a seeded fake, is what proves the `errored` capture reads what
`tutorial_tools.py` actually renders) against the shared Pyodide fixture,
and `tests/e2e/test_progress_badges.py` seeds `localStorage` directly and
never boots Pyodide at all, the same reasoning `test_cheat_sheet.py`
already established for anything that only ever needs `index.html`.
`standalone.bundle.js` rebuilt for the `tutorial-runtime.js` change.*

**7.71 — The cell-code-review skill's curriculum pass, finished.** 7.68 proved
the process on a handful of tutorials; this is the rest of it — the whole of
`computational-methods` and both series of `mit-pdp-maths-prog-integration`
(`maths-and-programming`'s 30 tutorials and `reflections-and-review`'s 2),
every practice page, and the four `mixed-*` practice_across pages. Batched
the same way `tutorial-glossary`'s own curriculum run was (`CHEAT_SHEETS.md`
§7) — several commits, not one, with a full `build(clean=True)` after each.

Three real changes, all renames or comments, none of them changing what a
cell does:

- `computational-methods/where-chains-lead.md` and its practice page: a
  word-chain loop built a transition-count matrix with `for a, b in
  zip(words, words[1:])`, reusing `dot(a, b)`'s generic-operand letters for
  two concrete, temporally-ordered things (a word and the word after it)
  that the same tutorial's own `generate()` already calls by a real name.
  Renamed to `word, next_word`; confirmed identical counts before and after.
- `computational-methods/undoing-it-practice.md` (twice) and
  `solving-systems.md`: `inverse(M)` swaps in `e` for the formula's own `d`
  — already taken by the determinant variable — with no explanation.
  Added a one-line comment at the destructuring line saying why.
- `mit-pdp-maths-prog-integration/storing-and-computing.md`: the "Type
  Conversion" cell used bare `x, y, z, w` for four different results (a
  string, an int, a float, a string built from an int) — directly
  contradicting the tutorial's own stated rule one section earlier
  (`temperature` is a good name; `t` is not). Renamed to `text_value`,
  number_value, decimal_value, number_as_text.

Everything else needed nothing — which, across roughly eighty documents,
is itself worth recording rather than assumed. The pattern from 7.68 held
at scale: single letters earn their place constantly (`a, b, c, d` matching
a quadratic or a triangle's own notation on the page above; `i, j, k` as
loop indices; `x, y` as coordinates; `f, g, h` as the standard names for
"a function," used in dozens of cells across both modules; `p, q` for
truth-table propositions; `n, r` matching `P(n, r)`/`C(n, r)` in *Counting
Carefully*; `m, c` for a line's slope and intercept, which *Drawing
Functions* names as conventional in its own prose). Two "discover first"
names were confirmed rather than flagged: `where-chains-lead.md`'s `state`
variable, used before the tutorial says "stationary distribution" out
loud, is the same example the style guide itself gives. Several cells are
deliberately bad code as the exercise itself — `when-it-goes-wrong.md`'s
`largest = 0` and `>` -for-`>=` cells, `building-reusable-tools-practice.md`'s
`def f(a, b): return (a + b) / 2` — and renaming any of those would erase
the thing the reader is meant to find. `bringing-it-all-together.md` and
`critique-and-reflection.md`/`the-team-project.md` have no code to review
at all — the first is all stub cells, the other two are pure prose.

One thing noticed and deliberately left alone, outside this skill's scope:
`parabolas.md`'s second `every-quadratic-is-the-same-curve` cell contains a
dead expression, `(x + 3) ** 2 - 4 + 4 - (x + 3) ** 2 + x ** 2`, which
algebraically collapses to plain `x ** 2` and does nothing the next few
lines don't already do properly on a second figure. That is a content bug,
not a naming or comment problem, and the skill's own charter is explicit
that restructuring logic is not its job — flagged here, and as a follow-up
task, rather than touched.

*Cost to change: small, same reasoning as 7.68 — this is a process applied
to content, not new code. The one thing worth remembering for next time:
running the skill this far confirms the proof-of-concept's finding scales
— most existing naming in this curriculum was already good, and the real
value was in the handful of places it wasn't, plus the confidence that
comes from having actually looked at all of them instead of assuming.*

**7.72 — Students can write their own notes, distinct from a tutorial's
author-written pedagogical notes, saved on the same record as their cell
work.** `planning/STUDENT_NOTES.md`'s plain version, shipped as designed:
a `notes` field on the record `saveNow()` already writes, a `<textarea>`
in Settings' "Your work" section (`#dl-progress-notes`), riding along on
the export/import button that already existed there — no new save path,
no new file format.

The one real design change this forced: `initProgressSection()` and
`saveNow()` both used to bail out on `cells.length === 0`, on the
reasoning that a page with no cells has nothing to save. That reasoning
broke the moment notes existed — a prose-only tutorial has nothing
*executable* to save but can still have something worth writing down. Both
now check membership in a small `NON_TUTORIAL_PAGES` set (`index`, `tree`,
`about` — `build.py`'s three non-tutorial `write_*_page()` slugs) instead,
which is the actual question that matters: is this a tutorial at all, not
whether it happens to have cells today.

From §4's two nudge proposals, only the smaller one shipped: a first-use
hint line under the textarea ("Notes are saved in this browser only.
Download a copy below to keep them anywhere else."). The staleness marker
on the export button was left for later per the design doc's own staging,
and is now `QUESTIONS.md`'s open question on this feature.

*Cost to change: small. `saveNow()`/`restoreSaved()` each gained a few
lines; `notesEl` is one module-level reference set once, read from three
places. Four new e2e tests in `tests/e2e/test_saved_progress.py`
(`TestStudentNotes` — autosave, survives a reload, "Start again" clears
it, and the export download actually contains it, checked via
`page.expect_download()` rather than trusting the button click alone)
against the shared Pyodide fixture, and a new
`tests/e2e/test_student_notes_prose_only.py` (three tests, no Pyodide
needed, same reasoning `test_cheat_sheet.py` already established) proving
the zero-cell case specifically: the section is not removed, a note still
autosaves with `cells: []`, and the contents page itself — which has no
tutorial to have notes about — correctly gets no notes field at all.
`standalone.bundle.js` rebuilt for the `tutorial-runtime.js` change.*

**7.73 — A left-anchored panel lets a reader jump to any tutorial in the
current series, not just the one immediately before or after it.**
`planning/SIDEBAR_CONTENT.md` §4b, shipped in scaled-down form: a new
`render_series_nav(tutorial, members)` in `build.py` server-renders an
`<ol>` of every member of the series, in reading order, with the current
one marked (`aria-current="page"`, not a link) and every other one a link
via the existing `link_between()` helper. A tutorial with nowhere in a
series to sit — archived, same as `nav_for()`'s own case — gets nothing,
rather than a guess. `write()` and the four other shell-template writers
(`write_index()`, `write_tree_page()`, `write_about_page()`, the editor
page) all gained the `{{SERIES_NAV}}` token, since an unfilled token fails
the build in any of them.

Between writing the design doc and building this, an external PR (#65, not
mine) moved the cheat sheet panel from right-anchored to left-anchored —
which quietly invalidated §4b's assumption that "left" was open ground for
a spatially separate nav panel. Rather than re-litigate that placement,
the series nav panel joined the cheat sheet at the same left anchor,
stacked below its toggle, and joined the existing Settings/cheat-sheet
mutual-exclusion group as a third member (`closeSeriesNav()` alongside
`closeSettings()`/`closeCheatSheet()`, each panel's open path now closing
both of the others).

Scope was cut down from §4b's original sketch: this ships series-listing
only, not a duplicate of the inline "Contents" table of contents
(`render_toc()`) that already exists on every page. Duplicating that here
would have doubled the maintenance surface for no reader benefit — the TOC
already answers "where am I on this page," and this panel only needed to
answer "where am I in the series."

Two failures surfaced building this, both from the standalone/downloadable
export path (`standalone_html()`), which strips navigation-dependent
markup that can't survive as a single downloaded file: the new toggle and
panel weren't covered by the existing stripping rules, and after adding
targeted ones, the inlined JS bundle's own string literals (element-ID
lookups like `"dl-navpanel-toggle"`) tripped the test asserting no
`dl-nav`-prefixed substring survives outside `<style>` blocks — a
collision with the pre-existing `<nav class="dl-nav...">` prev/next
element's own naming, not a real bug. Fixed by renaming
`navpanel`→`seriesnav` throughout, rather than carving the test's
assertion around script blocks: the collision was real evidence the
original name was too close to an existing convention, and the new name
is more specific regardless.

*Cost to change: small-to-moderate. One new function in `build.py`, one
new token threaded through five call sites, new shell markup and CSS
mirroring the cheat sheet's own (including its mobile bottom-sheet
treatment), and `initSeriesNav()`/`closeSeriesNav()` in
`tutorial-runtime.js` following the same open/close/mutual-exclusion shape
`initCheatSheet()` already established. Two new `re.sub` rules in
`standalone_html()` for the stripping gap. New
`tests/e2e/test_series_nav.py` (visibility, open/close, three-way mutual
exclusion with the cheat sheet, series content and ordering, mobile sheet)
and a `TestSeriesNav` class in `tests/test_build.py` for
`render_series_nav()` itself (ordering, current-item marking, the
order-file-decides-not-filename case, and the archived/no-series-position
empty case). `standalone.bundle.js` rebuilt for the
`tutorial-runtime.js` change.*

**7.74 — Pedagogical notes and dataset attribution, both shipped as
`planning/SIDEBAR_CONTENT.md` §2–§4 settled: extending the existing cheat
sheet panel rather than a third one.** Neither is cumulative across a
series the way the glossary is — a note or a dataset belongs to the
specific tutorial that declared it, full stop, so both ride on `write()`'s
manifest the same way `glossary` already does (present only when
non-empty), just never accumulated through `series_chain()` first.

**Notes** are authored as `<aside class="dl-note" id="...">` in the body —
§3's recommended option (b), the same reuse-over-invention trick the
hint/answer fold already established. Unlike a fold, a note does not stay
inline: `extract_notes()` pulls it out of `body_html` entirely once its id
and content are captured, because §4 settled that notes surface in the
sidebar, not mid-paragraph. One real design correction made while
building this, not in the original design doc: a raw HTML block's inner
content is *not* re-run through the markdown converter by this project's
existing pipeline — confirmed by checking what the hint/answer fold
already does with backticks and emphasis inside it (they show up literal,
not as `<code>`/`<em>`, a pre-existing limitation left alone here since
fixing it is out of this change's scope). §1's own design intent for
notes was explicit that this had to work — "a note that contains an image
is just markdown content" — so `extract_notes()` runs the captured inner
text through `to_html()` on its own, separately from the surrounding
document, which does convert correctly (checked directly: `![a
chart](chart.png)` inside a note becomes a real `<img>`). `check_alt_text()`
was extended to scan every note's own html alongside `body_html`, since an
image inside a note needs exactly the same alt-text requirement as one in
the body — it would otherwise go unchecked entirely, having already been
removed from `body_html` by the time that check runs.

**Datasets** use §2's `data/<name>.yaml` beside `data/<name>.csv` — the
same beside-the-file pattern `<slug>.glossary.yaml` already established —
plus a `datasets:` frontmatter list, cross-referenced the same
fail()-on-mismatch way `practice_pairs()` already checks `practice_for`.
Both the CSV and its attribution file are required once a tutorial
declares a dataset name, and the attribution file needs all three fields
(`source`, `license`, `description`) — an undocumented dataset would
defeat the entire point of declaring one, so this fails loudly rather than
shipping a nameless, sourceless entry.

The cheat sheet panel's intro copy was reworded (`shell.html`) to keep its
one real promise — "nothing here is something you have not been
taught yet" — scoped to the glossary specifically, since that guarantee
never applied to notes or datasets and saying it as a blanket claim would
now be false. Each of the three now gets its own heading inside the panel
(`renderCheatSheet()` in `tutorial-runtime.js` now takes the whole
manifest rather than just glossary entries), which is what keeps a reader
from mistaking a note for an examinable, taught term — the conceptual
cost §4 flagged when it settled on reusing one panel for three different
kinds of content.

*Cost to change: moderate. New `Note` dataclass and `Tutorial.notes`/
`Tutorial.datasets` fields, `extract_notes()` wired into `load()`,
`dataset_attribution()`/`check_datasets()` in `build.py`; `write()` gained
two more optional manifest fields following the same shape `glossary`
already has. `renderCheatSheet()` restructured to read from the whole
manifest and render three sections instead of one; `initCheatSheet()`'s
visibility guard now checks all three instead of just `glossary`. New
`TestNotes`/`TestDatasets` classes in `tests/test_build.py` (manifest
shape, extraction/removal from the body, duplicate-id and
missing-file/missing-attribution-field failures, non-inheritance across a
series, and the markdown-conversion-inside-a-note correction with its own
alt-text check) and new `TestNotes`/`TestDatasets` classes added to the
existing `tests/e2e/test_cheat_sheet.py` rather than a new file, since
this extends that panel rather than building a new one (toggle visibility
from a note or dataset alone, per-section headings, a note pulled out of
the page body, both a note and a glossary entry keeping their own separate
headings). `standalone.bundle.js` rebuilt for the `tutorial-runtime.js`
change.*

**7.75 — The export button gets a small marker once notes have grown
since the last export, opt-out in Settings.** `planning/STUDENT_NOTES.md`
§4's second, larger proposal — left for later at 7.72 — is now built too:
a `.dl-nudge` class on `#dl-progress-export` once the notes textarea has
grown by `NOTES_NUDGE_THRESHOLD` (120) characters since the last export,
rendered as a small coloured dot (`--dl-error-fg`, the same "something
here wants your attention" language `.dl-status-error` already uses) via
`::after` rather than any change to the button's own markup. Never a
banner, never mid-sentence — it can only change on an edit to the notes
field, an export, an import, or "Start again", none of which happen while
a reader is mid-keystroke elsewhere on the page.

The baseline it compares against is not a new field on the saved-progress
record — that would conflate "as of the last autosave" with "as of the
last export," which are different moments the whole feature exists to
tell apart. It is one more number in its own per-tutorial key
(`dewlab:notes-exported-len:<module>:<slug>`), tracked the same lightweight
way `rememberVersion()`/`writePin()` already track a small piece of
per-tutorial state outside the main record. An import counts as an export
too — an imported file's notes already exist outside this browser by
definition, which is the actual question the marker asks — so it resets
the baseline exactly like clicking "Export a copy" does. "Start again"
clears both the progress key and this one, so a fresh start does not carry
over a stale baseline pointed at notes that no longer exist.

The opt-out lives beside the existing progress-badges toggle in shape:
`NOTES_NUDGE_KEY` (`dewlab:notes-nudge`), a `[data-notes-nudge]` segmented
control in "Your work", `readNotesNudge()`/`writeNotesNudge()` mirroring
`readProgressBadges()`/`writeProgressBadges()` exactly. Off means
`updateNotesNudge()` always removes the class rather than skipping its own
check — a reader who turns this off should never see the dot again until
they turn it back on, not merely less often.

*Cost to change: small. Five small functions in `tutorial-runtime.js`
(`notesExportKey`, `readNotesNudge`/`writeNotesNudge`, `updateNotesNudge`,
`markNotesExported`) plus one more toggle-init function following
`initProgressBadgesToggle()`'s own shape exactly; one `.dl-texture-row` in
`shell.html` and eight lines of CSS for the dot. Five new e2e tests in
`tests/e2e/test_saved_progress.py` (`TestNotesNudge` — short notes get no
marker, long notes do, exporting clears it and the clearing survives a
reload, writing enough more after an export marks it again, and the
Settings toggle turns it off and holds across a reload) against the
shared Pyodide fixture, run alongside the full e2e suite and the full unit
suite, both green. `standalone.bundle.js` rebuilt for the
`tutorial-runtime.js` change.*

**7.76 — All three tooltip options built together: builtins, signature
help, and Jedi's pre-run answer for a name that has not been executed
yet.** `planning/CELL_TOOLTIPS.md` recommended building (a) and (b) first
and leaving (c) documented rather than built, on the reasoning that Jedi
was a second, heavier mechanism whose main extra value — pre-run
completion — was real but narrower once (a) had closed the builtins gap.
Prototyped against the real pinned Pyodide (0.28.3) and the real self-hosted
wheels before writing any of this: (a) confirmed the version cost nothing
(a computed builtin's `inspect.getdoc()` behaves exactly like a
`_page_globals` object's), and (c) confirmed Jedi's `.help()`/
`.get_signatures()` genuinely resolve a function defined but never run in
the same cell, from source text alone, in low tens of milliseconds warm.
That removed the open question `(c)`'s own writeup left — whether pre-run
completion was worth the second-mechanism cost — so all three were built
as one feature rather than staged.

**(a) Builtins.** `docFor`/the new `signatureFor` (`assets/tutorial-runtime.js`)
both now check `__builtins__` — via a new `lookupLiveName()` shared by
both, live-namespace first, builtins second, never shadowing a student's
own name — after `tools._page_globals` comes up empty. `builtinsModule =
pyodide.pyimport("builtins")`, set once at boot alongside `inspectModule`.

**(b) Signature help.** New in `vendor-src/codemirror-entry.js`:
`pythonSignatureHelp()`, a `StateField`/`ViewPlugin` pair rather than
`hoverTooltip()` — nothing in CodeMirror triggers on typing a character
the way `hoverTooltip` triggers on the pointer, so this needed its own
mechanism. `callContextAt()` scans backward from the cursor for the
nearest open, unclosed `(` and the identifier before it, counting
top-level commas along the way for the argument index; `highlightParam()`
bolds that argument in the returned signature string, splitting only
between the matching parens so a default value's own brackets or commas
are not mistaken for argument boundaries. `getDoc`'s calling convention
changed to match: `(name, wholeSource, line, col)` instead of `(name)`,
and it is now `async` — CodeMirror's hover source accepts a Promise of a
Tooltip natively, so no new plumbing was needed for that, only `await`.

**(c) Jedi.** Loaded in the background, well after `boot()` has already let
a student click Run — `loadJedi()`, fired without an `await` at the end of
`boot()` — since jedi+parso are a real ~1.6 MB download and nothing about
a first cell running depends on them; `dewlab.jediReady()` is how a test
(or a slower browser) knows the fallback has actually landed. Two Python
helpers (`_dewlab_hover_doc`/`_dewlab_signature`) live in `pyodide.globals`
— the interpreter's own top-level namespace, not
`tutorial_tools._page_globals` a student's cell runs against
(`run_cell()`'s `globals=`) — so `jedi` and both helpers are never visible
to, or shadowable by, anything a student writes. Both wrapped in Python
rather than left to a JS `try`/`catch`: the exception a malformed, mid-edit
source string can raise is more varied than one JS-side catch should have
to enumerate, and "no tooltip this time" is the only outcome that should
ever reach the caller.

**Live always wins.** `hoverDoc(name, source, line, col)` and
`signatureHelp(name, source, line, col, argIndex)` — what the CodeMirror
extensions actually call — try the live-interpreter answer first and only
reach for Jedi if that comes back empty. A name the interpreter already
knows about is authoritative; Jedi only fills the gap live cannot reach,
never the reverse, so the two can never disagree about a name they both
have an opinion on.

**One false start, corrected before it shipped.** A first hand-check of
Jedi's pre-run signature help against `average(numbers)` returned nothing
and read, briefly, like a real limitation. It was an off-by-one in the
column passed to `get_signatures()` — Jedi's own error message named the
valid range once the column was pushed one past it, which is what caught
it. Recorded because the same mistake would have been easy to carry
straight into `callContextAt()` unnoticed.

*Cost to change: moderate. `docFor`/`signatureFor`/`lookupLiveName`/
`jediDoc`/`jediSignature`/`hoverDoc`/`signatureHelp`/`loadJedi` in
`tutorial-runtime.js`; `pythonSignatureHelp`/`callContextAt`/
`highlightParam` plus the `getDoc` signature change in
`codemirror-entry.js`; a `.cm-dewlab-signature-tooltip` rule in
`tutorial-style.css`; `dev/fetch_pyodide.py`'s baseline gained `jedi`
(parso comes along as its own dependency), so the self-hosted mirror is
now ~32 MB rather than ~30. Fifteen e2e tests in
`tests/e2e/test_autocomplete.py` (`TestBuiltinTooltips`,
`TestPreRunTooltips`, plus the reconciliation case), all against the real
self-hosted Jedi rather than mocked — two needed `page.keyboard.insert_text()`
in place of `type()` once multi-line typed source turned out to double up
under CodeMirror's own auto-indent/auto-close handling, and hovering a
bare builtin needed a `view.coordsAtPos()`-based helper since "len" inside
"len([1, 2, 3])" gets no highlighting span of its own for a DOM text
locator to find. `standalone.bundle.js`/`codemirror.bundle.js` rebuilt.*

**7.77 — The Worker migration `QUESTIONS.md` left open was built: Pyodide
now runs off the main thread on the hosted site, and "Run" genuinely
becomes "Stop."** `planning/CELL_CONTROLS.md` §2 found the previous,
main-thread setup could not support this at all — a blocking Python loop
leaves no thread free to handle a click — and `QUESTIONS.md` recorded the
open question rather than guessing at an answer. This is that answer:
built, not merely re-weighed.

**Two execution paths, chosen by `currentManifest.standalone`.** The
offline, downloadable export (`build.py`'s `standalone_html()`) keeps
running Pyodide on the main thread exactly as before — a `file://` page
cannot use a module Worker, and the export has no Stop button to justify
the cost anyway. Every function that used to talk to Pyodide directly now
exists twice in `tutorial-runtime.js`: unchanged under an `MT` suffix for
that path, and behind a `workerRequest()` postMessage round-trip for the
hosted path. `boot(manifest)` picks the path once; nothing downstream
re-checks it per call.

**`assets/pyodide-worker.js`**, new, is a module Worker running the same
`tutorial_tools.py`, the same `docFor`/`signatureFor`/Jedi machinery moved
over verbatim, behind one uniform request/response protocol
(`{type, id, ...}` in, `{type:"response", id, result|error}` out, plus
one-way `status`/`jedi-ready`/`output` pushes). Every URL it fetches
(Pyodide's own base, `tutorial_tools.py`, the CSV data base) has to be
resolved to an absolute URL before being handed to the Worker — a relative
fetch inside a Worker resolves against the worker script's own location,
not the page's, which is not obvious until it silently 404s.

**The interrupt itself is `pyodide.setInterruptBuffer()`**, exactly as
`CELL_CONTROLS.md` §2 described: a `SharedArrayBuffer` the main thread
writes `2` (SIGINT) into on a Stop click, checked by the Worker's own
Python between bytecode steps regardless of what the running code is
doing. `SharedArrayBuffer` only exists when the page is cross-origin
isolated, which needs `Cross-Origin-Opener-Policy`/
`Cross-Origin-Embedder-Policy` response headers GitHub Pages will not let
this project set — `coi-serviceworker` (vendored, `assets/vendor/`,
registered from `shell.html`, excluded from the standalone export by
`build.py`) is the same-origin service-worker shim that adds them anyway.
`dewlab.canStop()` reports the real state — cross-origin isolation
achieved and a `SharedArrayBuffer` actually allocated — rather than
`interrupt buffer requested`, since `coi-serviceworker`'s own first
registration on a given browser needs one reload before headers apply,
and a run started before that reload should not show a Stop button it
cannot honor.

**Cell output crosses the postMessage boundary through a message-based
sink**, `_MessageSink` in `tutorial_tools.py`, parallel to the existing
`_DomSink` rather than replacing it — `run_cell(cell_id, output_target,
code)` picks one by whether `output_target` is callable. The Worker side
posts `{kind, cssClass, text, markup}` events; `applyOutputEvent()` on the
main thread replays `_DomSink`'s own stream/append/clear semantics against
the real DOM, so a reader sees byte-for-byte the same output shape either
way. `KeyboardInterrupt` — what a Stop click actually raises inside the
running Python — is caught ahead of the general exception handler and
renders as a plain "Stopped.", not a traceback.

**The widget bridge (`text_input`/`dropdown`/`button`) cannot work in a
Worker and now says so.** All three hand a live DOM element back to the
caller for `.value` reads and event listeners; a Worker has no DOM to hand
one back from. Rather than degrade silently into inert markup,
`_require_dom_sink()` raises a clear `RuntimeError` naming the reason
whenever a cell's sink is a `_MessageSink`. Checked before writing this:
zero published tutorials use any of the three, so nothing live breaks —
this closes a real gap the Worker migration would otherwise have left
open rather than trading one gap for another.

**Cost to change: large, matching `QUESTIONS.md`'s own estimate.**
`assets/pyodide-worker.js` (new); `tutorial-runtime.js`'s `MT`-suffixed
split plus `workerRequest`/`ensureWorker`/`bootWorker`/`applyOutputEvent`/
`requestInterrupt`; `_MessageSink`/`_require_dom_sink`/the
`KeyboardInterrupt` branch in `tutorial_tools.py`; `coi-serviceworker`
vendored via `vendor-src/package.json`/`build-vendor.mjs`, wired into
`shell.html`, copied and then stripped back out for the standalone export
in `build.py`; a `.dl-btn-stop` rule in `tutorial-style.css`. Eighteen e2e
tests: three new in `tests/e2e/test_stop_button.py` (cross-origin
isolation actually landed, a genuine infinite loop stopped and the button
recovers, a stopped cell runs again afterward), one rewritten in
`test_phase0_golden_path.py` replacing two widget tests that exercised
behavior this migration deliberately removed on the hosted path. The full
unit and e2e suites both green. `standalone.bundle.js` rebuilt.*

**7.78 — dewmini gained `sqlite3`, Pillow, and a fourth widget,
`image_input`, plus a way to attach an image to a documentation cell — none
of it touching a tutorial page's own defaults.** DECISIONS.md's "Core
libraries" row dropped sqlite deliberately, as the one library that needed
unvendoring beyond numpy/pandas/matplotlib's single `loadPackage()` call —
a real cost for curriculum content shipped to every published tutorial.
dewmini is not curriculum content; it is a general notebook a reader opens
for one session's worth of Python, so that cost buys something there it
would not buy on a tutorial page. `DM_PACKAGES` in `compose/dewmini.js`
(`numpy`, `pandas`, `matplotlib`, `sqlite3`, `Pillow`) is dewmini's own
wider default, used by both its live Pyodide boot and the standalone
`.html` export's embedded copy; `tutorial-runtime.js`'s `DEFAULT_PACKAGES`
for tutorial pages is untouched.

**`image_input(label="Choose an image", id=None)` joins `text_input`,
`dropdown`, and `button` in `tutorial_tools.py`** — beyond the six named
functions, the same way `load_csv` was (0.9). A file input limited to
`accept="image/*"`; picking a file reads it with the JS File API's
`arrayBuffer()`, decodes it through Pillow when Pillow is loaded and falls
back to raw bytes when it is not (`ImportError` caught, not assumed away),
and lands the result in `_widget_values` the same out-of-band dict
`text_input`/`dropdown` already use for a value a plain `.value` read on
the DOM element cannot supply — a file input's own `.value` is only ever
the filename string. `_Widget.value` gained one `self._kind ==
"image_input"` branch to read from there instead of `querySelector`.
Nothing published uses this widget either, same as the three before it, so
`_require_dom_sink`'s docstring gained a fourth name and nothing else
changed about the gap it already described.

**A documentation cell's own image attachment is unrelated to
`image_input` and lives entirely in `compose/dewmini.js` — a reader
illustrating a note, not a cell's code reading a file.** Its picture-frame
button (next to Delete in the cell head) opens a native file picker, reads
the pick as a data URL via `FileReader`, and appends `![image](data:...)`
to the cell's own markdown-lite source — one more inline pattern in
`renderDocInline`, deliberately restricted to a `data:` URL and nothing
else, since a `data:` URL is the one thing this button ever writes and a
remote image would need a loading and trust story this cell type has no
reason to take on. Capped at 3 MB of raw file size before the read even
starts (`MAX_DOC_IMAGE_BYTES`) — base64 inflates that by roughly a third
once it lands in `localStorage` alongside every other cell, and a reader
should see why a pick was refused rather than watch a save silently stop
taking effect later.
*Cost to change: small. `image_input` and the doc-cell attachment are
independent and either can be dropped without the other; `DM_PACKAGES` is
one array read by both the live boot and the standalone template (the
latter via `JSON.stringify`), so the two never drift apart on their own.*

**7.79 — Mini IDE's output never actually rendered: a stale CSS class,
not the Worker migration, was hiding it — fixed, alongside a
non-destructive per-cell/toolbar output reset, a run-time stat, a
quieter idle rail, and side panels that no longer cover a wide cell.**
Reported directly: clicking Run in Mini IDE produced no visible output
at all. `assets/mini-ide-engine.js`'s worker path was writing real output
into the DOM correctly the whole time — the bug was one CSS rule,
`.mini-ide-cell-output.empty, .mini-ide-cell-output:empty { display:
none; }` in `assets/mini-ide-style.css`, next to the matching JS at
`mini-ide.js` that set a literal `.empty` class on a cell's output `<div>`
once, at creation, and never removed it. Every tutorial page's own
`.dl-output` avoids exactly this by hiding on `:empty` alone — a
pseudo-class that re-evaluates on every DOM change, unlike a class a
script has to remember to clear — and Mini IDE's own implementation had
quietly drifted from that pattern. Fixed by dropping the static class
entirely and hiding on `:empty` only, matching `.dl-output`.

**Reset/clear output, non-destructive, joins the existing (destructive)
Clear All in both Mini IDE and dewmini.** Neither page had a way to clear
a cell's output without deleting the cell — "Clear All" only ever meant
"delete everything." Each Python cell gained a small ↺ button next to
Run (`resetCellOutput()`/`engine.clearOutput()` in Mini IDE,
`resetCellOutput()` in dewmini, mirroring `executeCell()`'s own
remove/re-add of dewmini's `dm-empty` class — the one place dewmini
already had the correct pattern Mini IDE's bug above shows it lacked),
and a toolbar-level **Clear Output** button runs it across every cell at
once. Both need no confirmation dialog, unlike Clear All: nothing is
lost, since the code stays untouched and a cell can simply be re-run.

**A cell now shows how long its last run took, `Ran in <duration>`
under its output, gated by a new Settings → Workspace → Python → **Run
time** on/off switch (`#dl-settings-execution` in Mini IDE, a new
`#dl-settings-execution` section in dewmini, following the existing
`.dl-seg` on/off pattern rather than a bare checkbox — no checkbox
appears anywhere else on either page).** Timed with `performance.now()`
around the existing `engine.runCell()`/`tools.run_cell()` call in both
`runCell()` and `runAllCells()`/`executeCell()`; the duration is kept on
the cell (and persisted through `saveState()`, alongside `output` and
`hasError`) even while the setting is off, so turning it on later doesn't
need a re-run to have something to show.

**The idle-state coloured rail (navy for Python, muted grey for text) is
gone from both pages; the rail itself stays, now transparent until a
cell is focused (orange) or its last run errored (red).** Reported
directly: "get rid of the grey line on the left of every cell." The rail
kept its reserved width and margin rather than collapsing to zero, so
nothing shifts when it lights up for the two states actually worth
flagging at a glance down a long notebook — only its at-rest colour
changed, from a low-opacity type indicator to nothing at all, since a
cell's type is already legible from its pill and its content.

**Settings and Help, both fixed-position overlays
(`tutorial-style.css`'s `.dl-settings` and `.mini-ide-panel`/`.dm-panel`),
covered a cell's own run/reset/delete buttons — sometimes its output —
at ordinary laptop widths (1280-1440px), because the workspace column
they float over reaches close enough to the screen's right edge for the
two to collide.** Confirmed by measuring: at 1280px, Mini IDE's
`.mini-ide-workspace` and dewmini's `.dl-page` (at a reader's own chosen
"wide" line width) both genuinely overlapped the open panel's horizontal
range, not just visually crowded it. A new `watchPanelOverlap()` in each
page's JS (a `MutationObserver` on each panel's `hidden` attribute/
property, rather than hooking every one of Settings/Help's several
open/close paths — toggle click, close button, Escape, click-outside)
keeps `<html data-dl-panel-open>` in sync; each page's own stylesheet
reads that attribute to left-anchor its workspace, with `margin-right`
reserving space for the wider of the two panels, instead of the usual
`margin: 0 auto`/`translateX(-50%)` centering trick — centering would
have split the reclaimed width evenly, wasting half of it as a matching
left margin nobody asked for. Scoped to `min-width: 34rem`, where a panel
is a right-anchored overlay at all rather than the phone-width bottom
sheet it already becomes below that. Deliberately scoped to Mini IDE and
dewmini's own stylesheets rather than changing `.dl-settings`/
`.mini-ide-panel` in `tutorial-style.css` directly, which would have
touched the panel's behaviour on every one of the site's 100+ tutorial
pages for a problem confirmed only on these two, wider-workspace pages.
*Cost to change: small for the output-visibility fix and the rail (both
CSS-only, one class each); small-to-moderate for reset/stats/panel-reach,
spread across `assets/mini-ide.js`, `assets/mini-ide-engine.js`,
`assets/mini-ide-style.css`, `compose/dewmini.js`,
`compose/dewmini-style.css`, and both HTML files, but each of the four
features is independent of the others and any one could be reverted on
its own without touching the rest.*

**7.80 — Two more reported directly, both fixed: a cell's × now needs two
clicks, and the Texture "Size" slider now actually resizes Settings,
Help, and every other control, not just reading prose.** A single
accidental click on × deleted a cell outright, with no way back short of
undoing whatever the reader was about to do next. Both Mini IDE and
dewmini's delete buttons now arm on a first click (turning solid red,
title changing to "Click again to delete this cell") and only delete on
a second — `armDeleteButton()`/`disarmDeleteButton()` in each page's own
JS, auto-disarming after three seconds, on blur, or the moment anything
else on the page is clicked, so a stale armed state from a click a
reader has since forgotten about can never cause the same accidental
delete a click straight through it was supposed to prevent. Deliberately
not a native `confirm()` dialog: that stops the whole page and needs a
mouse trip to a button elsewhere, where this needs only a second,
deliberate press of the button already under the pointer.

**The size slider bug was a one-line root cause, in a rule every page on
the site shares.** `tutorial-style.css` set `--dl-font-size` on `body`,
but nearly everything on any dewlab page — Settings, Help, buttons, cell
chrome, both IDEs' own workspace math — is sized in `rem`, relative to
the *root* element's font-size, not body's. Setting it on `body` only
ever resized the handful of things that inherit a font-size directly
rather than stating one in `rem`, which is why the slider visibly grew
reading prose but left every panel, button, and control exactly the size
it started at — not a Mini-IDE-or-dewmini-specific bug, since the
`.dl-settings`/`.mini-ide-panel`/`.dm-panel` panels the report named are
shared components rendered on every tutorial page too. Fixed by moving
the declaration to `html`, where `rem` actually resolves from. A `rem`
inside a media query is unaffected either way — the specification
defines it there as always relative to the root element's *initial*
size, never an author override — so no responsive breakpoint site-wide
shifts as a result.

**That fix exposed a second, narrower one it made visible: Mini IDE's own
h1/intro/toolbar/sample-notice, sized through the ordinary `--dl-line-width`-
constrained `.dl-page` column rather than through `.mini-ide-workspace`'s
own wider override, now widens along with the rest of the page at a
larger Size setting — enough, at the high end of the slider, to reach
under an open Settings/Help panel the same way `.mini-ide-workspace`
itself did in 7.79.** Same fix, same reasoning, extended to `.dl-page`
alongside the existing `.mini-ide-workspace` rule in
`assets/mini-ide-style.css`.
*Cost to change: small. The delete confirmation and the font-size fix
are unrelated and either could be reverted independently; the root-cause
`html`/`body` fix is one shared declaration, so reverting it reverts the
behavior everywhere it applies, all at once, by design.*

**7.81 — A Jupyter-import compatibility warning, three real shared
datasets (the first ever committed to `data/`, which had been empty
since launch), and four worked-example notebooks reachable from both
IDEs' own Import section.** Three separate requests, landed together
since each depended on groundwork the last one built.

**The compatibility scan** (`scanPyodideCompatibility()`, ported
identically into both `assets/mini-ide.js` and `compose/dewmini.js`)
checks an imported notebook's Python source, before its cells ever land
in the page, for the two mistakes an outside notebook actually tends to
carry: an import Pyodide cannot satisfy no matter what loads
(`PYODIDE_INCOMPATIBLE_MODULES` — `tkinter`, `torch`, `subprocess`,
`socket`, and similar, each with why), and a Jupyter magic (`%.../%%...`)
or shell escape (`!...`) — valid only inside a real IPython kernel, a
plain `SyntaxError` anywhere else. Not a full Python parser, just the
regexes worth the trouble for what an outside notebook realistically
contains. A new `#import-compat-notice` banner (styled off each page's
existing "empty state"/"sample loaded" notice, given a more serious red
accent since this one names things that will actually error) lists what
it found, naming which imported cell each one is in; dismissible, never
blocking the import itself.

**Three real datasets now live in `data/`**, `.gitkeep`'s own note ("delete
once this holds real content") finally acted on: `co2-emissions.csv`
(national CO₂ and greenhouse-gas emissions, 1950–2023, trimmed from
[Our World in Data's `owid-co2-data.csv`](https://github.com/owid/co2-data)
to real ISO-3 countries and fourteen columns worth teaching with,
~1.3 MB from an original ~14 MB), `life-expectancy.csv` (1950–2016,
trimmed from OWID's Gapminder/UN/IHME compilation), and
`pride-and-prejudice.txt` (Jane Austen, 1813, the standard Project
Gutenberg plain-text release, kept byte-for-byte including its licence
header/footer — Gutenberg's own terms ask for that, and the first
worked example that uses it strips the boilerplate back out itself as
a real data-cleaning step, not a hidden preprocessing step this project
did on the student's behalf). All three CC BY 4.0 (CO₂, life expectancy)
or US public domain (the novel); cited by name and licence in the
notebook that uses each one. `load_csv()`'s own docstring had said
`load_csv("life-expectancy.csv")` as its example since before any file
by that name existed — it now does.

**Four worked-example notebooks in `assets/examples/`** — real nbformat
4 `.ipynb` files, not hardcoded cell arrays, so they import through the
exact same `parseIpynb()` path (and the compatibility scan above) a
reader's own file would: **`sql-owid.ipynb`** (`sqlite3`, `run_query()`,
the CO₂ data), **`data-investigation.ipynb`** (has life expectancy
converged across countries since 1950? — a real, verified finding: the
country-average spread fell from a standard deviation of 12.0 years in
1950 to 7.3 in 2016 while the mean rose from 49.0 to 72.4), **`math-and-
charts.ipynb`** (estimating π by Monte Carlo — throwing random points at
a quarter-circle), and **`word-frequency.ipynb`** (counting words in the
novel and checking the result against Zipf's law — real, verified:
rank × frequency stays in roughly the same range across the first
hundred ranks). Every number any of the four states as a finding was
actually computed, against the actual shipped data, before being
written down — not reasoned about — and every code cell in all four was
run end-to-end against real Pyodide (self-hosted, `dev/fetch_pyodide.py
--packages numpy pandas matplotlib sqlite3`) with zero cells erroring,
not just checked for syntax.

**Reachable from Settings → Import (Mini IDE) / Settings → Keep a copy
(dewmini) as four buttons below the existing file picker**, each calling
a new `loadBuiltInExample(path, label)` — `fetch()` the `.ipynb`,
`parseIpynb()` it, hand the result to the same `applyImportedCells()`
(newly factored out of `handleImportNotebookFile()`/`handleImportFile()`,
so a built-in example and a reader's own file now share every step
after parsing rather than the built-in path skipping the compatibility
scan or the replace/append setting). dewmini has no replace/append
choice for import at all — its own `handleImportFile()` always replaced
the notebook outright already — so a built-in example does the same
there, stated plainly in its own button's neighbouring copy.
*Cost to change: small-to-moderate. The compatibility scan, the
datasets, and the worked-examples UI are three independent pieces —
any one could be reverted alone — but the worked examples depend on the
datasets existing, and would need rewriting (not just deleting) if the
datasets were ever removed.*

**7.82 — A search box on the contents page and "Browse by topic"; the
cheat sheet renamed to "Reference" everywhere, with its own search
added inside it.** Two related but separately reported requests.

**Search** (`assets/search.js`, new) matches a query against every live
tutorial's title, module, series, and — the part that makes it more
than a title search — the terms its own glossary entry says it
*specifically introduces*. `write_search_index()` in `build.py` writes
one `assets/search-index.json` after every build (archived and
practice-only pages excluded, the same "not a first thing to send a
reader to" reasoning those already have elsewhere), using
`own_glossary()` rather than `cumulative_glossary()` — a later tutorial
in a series has already inherited an earlier term, and searching for it
should point at where it was actually taught, not at every page
downstream of that. Matching runs client-side: lower-case, a
conservative rule-based stemmer (`sorting`/`sorted`/`sorts` all reduce
to `sort`, not Porter's full algorithm, just the common English
suffixes worth stripping), and a small curated synonym table (`loop` →
the same normalized form as `iterate`, and so on) — good enough for a
few hundred tutorials, not attempting to be good enough for the open
web. Scored by field — a title hit counts for more than a glossary-term
hit, which counts for more than a module/series-name hit — so a search
for "loop" ranks a tutorial titled "Loops" above one that merely lives
in a module called "Repeating Yourself." `render_search_box()` in
`build.py` generates identical markup on both pages so `search.js` only
has to know one shape; it is a no-op anywhere else, including every
tutorial page, since it only ever does anything once it finds
`#dl-search` in the page.

**The cheat sheet is "Reference" now, top to bottom** — `dl-cheatsheet`
→ `dl-reference`, `initCheatSheet()`/`closeCheatSheet()`/
`renderCheatSheet()` → `initReference()`/`closeReference()`/
`renderReference()`, `planning/CHEAT_SHEETS.md` →
`planning/REFERENCE_PANEL.md`, `tests/e2e/test_cheat_sheet.py` →
`tests/e2e/test_reference.py`, and every comment, docstring, and
student-facing string that named it, across `assets/shell.html`,
`assets/tutorial-runtime.js`, `assets/tutorial-style.css`, `build.py`,
`README.md`, `ARCHITECTURE.md`, both `docs/*-explained.md` files, and
several `planning/*.md` files. Reported directly, on the reasoning that
"cheat sheet" reads as something a student should feel a little bad
about needing, when the entire point of the panel is the opposite: nothing
in it is ahead of where the reader actually is. `DECISIONS_LOG.md` and
`QUESTIONS.md` keep the old name in their own already-written entries,
deliberately — this project's own convention is to not rewrite finished
history, and both files already explain the reasoning behind decisions
made under the old name; a glossary entry's own file
(`tutorials/*/*.glossary.yaml`) and `series.yaml` comments picked up the
same rename since they are live content, not a historical record.

**The reference panel got a search of its own**
(`filterReferenceContent()` in `tutorial-runtime.js`), separate from
`search.js` above and deliberately simpler: this panel's whole content
for one page is already sitting in the DOM, so filtering is a plain
substring match over each term's own name, definition, and any note's
text — hiding what doesn't match, no fetch, no cross-page index, no
stemming. Shown only once a page has more than a handful of entries to
search through (`renderReference()` decides that), and cleared via a
`MutationObserver` on the panel's own `hidden` attribute whenever it
closes — regardless of which of its several close paths did the
closing — so reopening it later never starts on a stale filter left
over from the last time it was open.

**This also folded in an unrelated but adjacent request: Settings can
now stay open alongside the reference or the series nav, instead of
force-closing whichever of them was open.** Settings anchors to the
page's right corner; the reference and series nav share the left one
and still genuinely conflict with each other (they would sit directly
on top of one another), so that pair still closes on open — only the
stale three-way exclusion involving Settings, a carryover from before
the reference panel moved to the left corner (PR #65), was removed.
Each panel's own "click outside closes this" handler needed a matching
fix (`clickIsInsidePanels()`, new): without it, opening a *compatible*
panel's toggle still read as "outside" the first one and closed it
anyway, even after the explicit force-close calls between them were
removed. `assets/vendor/standalone.bundle.js` was rebuilt
(`npm run build` in `vendor-src/`) after these `tutorial-runtime.js`
changes, since it's compiled from that file and the
`standalone-bundle-is-current` CI check would otherwise catch the drift.
*Cost to change: small for search (two independent, self-contained
features); moderate for the rename, purely because of its breadth
rather than any real complexity — a mechanical find-and-replace plus a
handful of files a first sweep missed (comments wrapped across two
source lines, a couple of test docstrings naming the old test file by
name), not a design decision to revisit.*

**7.83 — Reference, Settings, and the series nav became docked sidebars,
toggled from the masthead instead of the page's corners.** Reported
directly: "is there a way to make the reference document more useful as
a permanent sidebar that can be toggled? I think settings would be the
same... maybe those things would be sticky in the header as opposed to
in the upper corner?" — the panels themselves had already been proven
(7.73–7.82), so this is a placement and shape change, not a new feature.

**Toggle placement**: all three toggle buttons moved into
`.dl-masthead-actions` (new, `shell.html`), a right-aligned action row
in the sticky masthead alongside the wordmark and crumbs, replacing the
reference's and series nav's own fixed-position corner buttons (the
Settings toggle was already there). `.dl-crumbs` grew from `flex: 0 1
auto` to `flex: 1 1 auto` to make room. Below the phone breakpoint,
where three full-text buttons plus the wordmark no longer fit one row,
each toggle's label text is wrapped in a new `.dl-toggle-label` span and
hidden, leaving icon-only buttons — found by an actual screenshot at
390px width during this work, not assumed to be fine; `aria-label`
carries the accessible name once the visible text is hidden, since
`display: none` content does not contribute to a button's computed
accessible name.

**Panel shape**: `.dl-settings`/`.dl-reference`/`.dl-seriesnav` went
from floating cards (`top`/`left`/`right` inset by `1rem`, rounded
corners, `box-shadow`, height capped by `max-height`) to full-height
docked sidebars (`top: var(--dl-chrome-h); bottom: 0`, flush to their
edge, a single `border-left`/`border-right` in place of the shadow) —
the "typical offline IDE" shape asked for, where a panel is a permanent
pane a reader can work beside rather than a popover that happens to be
open. The reference and series nav still force-close each other on
open (both dock to the left edge and would overlap otherwise); Settings
still docks right and stays independent, unchanged from 7.82.

**The margin-push mechanism (7.x, `data-dl-panel-left`/`-right`) had a
latent bug this surfaced**: it pushed `.dl-page` clear by a flat 25rem
regardless of a panel's actual width, which was never wrong before
because a floating card's `max-width` kept it well under that — but a
genuine sidebar, resized wider by a reader dragging its own handle, has
no reason to stay under 25rem. `watchPanelOverlap()` now also runs a
`ResizeObserver` on each panel, writing its live `offsetWidth` (plus a
small gutter) into `--dl-panel-left-w`/`--dl-panel-right-w`, which the
margin rule reads with the old flat value only as a one-frame fallback.
Verified with an actual drag-the-resize-handle Playwright test, not
just read as correct from the CSS.

**Open state now survives navigating to the next tutorial in a series**
(`saveSidebarState()`/`restoreSidebarState()`, new) — a reader who opens
the reference once and pages through Prev/Next keeps it open, rather
than reopening it on every page, matching "permanent" in the request.
Stored in `localStorage["dewlab:sidebars"]` as `{left, right}` — `left`
is `"reference"`, `"seriesnav"`, or `null` rather than two independent
booleans, since only one can ever be open at a time. Restored by
clicking the matching toggle at startup rather than duplicating each
panel's own open logic, so the reference/series-nav exclusion and the
"toggle hidden on a page with nothing to show" checks are reused rather
than re-implemented. Deliberately not restored below the phone
breakpoint (checked with `matchMedia`, not the deprecated
`window.innerWidth` snapshot) — a bottom sheet covering most of a phone
screen is a deliberate, momentary action, not a pane to leave open by
default. A genuine ordering bug was caught and fixed before this
shipped: the existing `sync()` inside `watchPanelOverlap()` ran once,
synchronously, at startup, before `restoreSidebarState()` had a chance
to run — persisting "everything closed" over whatever a reader had
actually saved, every single page load. Split into an `updateAttrs()`
that runs unconditionally and a `sync()` (which also persists) that
only runs from the `MutationObserver` path, so the one startup call
updates the CSS attributes without also clobbering the stored
preference.

`assets/vendor/standalone.bundle.js` was rebuilt (`npm run build` in
`vendor-src/`) after the `tutorial-runtime.js` changes, same reason
7.82 needed it. `planning/REFERENCE_PANEL.md` §6 and
`planning/SIDEBAR_CONTENT.md` §4b describe the old corner-button/
floating-card shape; both got a short addendum pointing here rather
than being rewritten, matching this project's own convention for a
living design doc superseded by what actually shipped.

*Cost to change: moderate — three coordinated CSS rewrites (toggle,
panel, phone breakpoint) plus two genuinely new runtime mechanisms
(width-tracking, state persistence), each independently small and
tested (a resize-drag Playwright check, a narrow-viewport screenshot, a
reload-preserves-state check), but real work rather than a rename.
Reusing the existing `data-dl-panel-left/right` attribute mechanism and
each panel's own open/close functions kept this from being a rewrite of
working code — the sidebar concept was proven in 7.73, this changed its
shape and location, not its logic.*

**7.84 — Mini IDE and dewmini's own Settings/Help panels became docked
sidebars too, and a real resize bug 7.83 shipped with got caught and
fixed on all three surfaces.** Reported directly, as a follow-on to
7.83: "can we make sure all of the features of mini-ide are in dewmini...
I think its time to introduce more capable sidebars basically" — settled
into two phases, sidebars first (7.83), then IDE feature parity
(`planning/MINI_IDE_AND_DEWMINI_NEXT.md`'s own next task). This entry is
the first phase's second half: both IDEs already reused `.dl-settings`
from `tutorial-style.css` (a shared class, not a duplicate), so 7.83's
docked shape landed there automatically — the actual work was their own
Help panel (`.mini-ide-panel`/`.dm-panel`, each IDE's own class so
opening Help never fights the real `#dl-settings` node) and the
`data-dl-panel-open` margin-push both IDEs already had from an earlier
session (task 9 in that session's own list).

**Both IDEs' Help panel got the same docked-sidebar treatment `.dl-settings`
got in 7.83** — full height, flush to the right edge, border-left instead
of a floating card's shadow+radius — and the flat `26rem` margin-push
guess became width-tracked the same way, via a `ResizeObserver` writing
`--dl-panel-w` (a single property, not the tutorial pages' left/right
pair, since both IDEs' two panels dock to the same right edge and are
already mutually exclusive). Settings/Help open state is now also
persisted per IDE (`localStorage["dewlab:mini-ide:sidebar"]`/
`["dewlab:dewmini:sidebar"]`, each storing a single `"settings"|"help"|
null` rather than the tutorial pages' `{left, right}`), restored the
same way — clicking the saved toggle at startup, above the phone
breakpoint only — with the same startup-ordering fix 7.83 needed
(the DOM-attribute sync and the persisting sync split apart, so the one
unconditional call at the top of `watchPanelOverlap()` doesn't overwrite
a reader's actual saved state with "everything closed" before
`restoreSidebarState()` gets to read it).

**A real bug in 7.83's own right-docked panel shipped undetected until
this pass actually dragged the resize handle: a panel flush to the
browser window's own right edge has no room to grow.** Native CSS
`resize: horizontal` always draws its handle at a box's own bottom-right
corner and grows the box away from that corner, regardless of which
edges are anchored via `left`/`right` — correct for `.dl-reference`/
`.dl-seriesnav` (left-docked: the handle sits well inside the viewport,
and dragging right, into the page, is exactly how those grow) but wrong
for anything right-docked and flush to the edge (`.dl-settings`, and now
`.mini-ide-panel`/`.dm-panel`): that corner sits exactly on the browser
window's own edge, so growing it would require dragging the pointer
*past* the edge of the window itself, which a real user's mouse cannot
do. 7.83 shipped this already, unnoticed, because its own resize test
only exercised the left-docked reference panel. Fixed the same way on
all three surfaces: native `resize: horizontal` removed from the three
right-docked panels, replaced by `makeRightEdgeResizable()` (one copy
per file — `tutorial-runtime.js`, `mini-ide.js`, `dewmini.js`, matching
this codebase's own "thin copy per page" convention) — a plain pointer
drag on a new thin strip along the panel's own *left* edge instead, the
edge a right-docked sidebar's resize affordance actually belongs on (the
same edge a real IDE's own side panel uses). Verified by an actual
drag-the-new-handle Playwright test showing the panel grow, on top of
the drag-the-old-handle test from 7.83 that had wrongly read as passing
(it drags the *left*-docked reference panel, which was never broken).

**A second bug found alongside the first, before it shipped rather than
after: the browser's own native resize sets an element's width as an
inline style, which beats any stylesheet rule regardless of media
query.** A panel resized wider on a desktop-width screen, then viewed
(or resized down to) the phone breakpoint, would have kept that desktop
pixel width instead of becoming the intended full-width bottom sheet —
`width: auto` alone, already present in all three phone-breakpoint
rules, was never enough to override an inline `style.width` the same
element already carried. Fixed by adding `!important` to that one
declaration on all three panels across all three stylesheets, and
verified with a resize-then-shrink-the-viewport Playwright test rather
than assumed safe from reading the cascade rules alone.

`assets/vendor/standalone.bundle.js` was rebuilt again after this
pass's `tutorial-runtime.js` changes, same reason 7.82/7.83 needed it.

*Cost to change: moderate — the docked-shape port itself was small (both
IDEs already shared `.dl-settings`'s CSS, so only the Help panel and the
margin-push needed touching), but the resize-handle bug it surfaced was
real, affected three files' worth of already-shipped code (7.83's own
`.dl-settings`, still an open PR at the time this was caught, plus this
pass's two new panels), and needed a genuine new mechanism
(`makeRightEdgeResizable()`) rather than a CSS tweak — cheap to have
caught now, before 7.83 merged, rather than as a separate bug report
later.*

**7.85 — The README was split by audience: a short overview at the root,
and one document each for students, tutorial writers, code contributors,
and anyone reporting a problem.** The README had grown to 671 lines and
was addressing four readers at once — a student wondering what the
Settings button does, an author looking up frontmatter fields, a
developer setting up a build, and somebody who had found a wrong answer
in a practice page. Each of them had to scroll past the other three.
Read straight through, it was also a walkthrough of a project rather
than a way into one, which asks a new reader to learn the history before
they can do anything.

The split follows who is reading rather than what the subject is.
`docs/FOR_STUDENTS.md` takes everything a reader of a tutorial needs —
cells, saved work, Settings, the Reference panel, practice, their own
cells, the download and export options, and the two Python workspaces.
`docs/WRITING_TUTORIALS.md` takes the whole authoring format:
frontmatter, `order.yaml`, cells, mathematics, `check()`, includes,
links, practice pages, glossary files, curriculum coverage, releases,
and the pre-pull-request checks. `docs/REPORTING_A_PROBLEM.md` is new
rather than moved — there was nowhere to send somebody who had found a
mistake, and "open an issue" alone does not tell them what is useful to
include. `CONTRIBUTING.md` absorbed the setup, test and CI material the
README used to carry, so a code contributor now has one door rather than
two half-doors.

What stayed on the README is what a reader who does not yet know what
dewlab is needs: what it does, a table pointing each reader at their own
document, a tour of the features, how the site is put together, how to
run it locally, and where the project stands. It is 161 lines.

The pass also closed real staleness. The README described none of the
work of the last several sessions — Mini IDE, dewmini, reader-added
cells, PDF and Jupyter export, the site search, "Browse by topic" —
except as filenames in a directory listing. `planning/STATUS.md` still
said 71 pages and two `computational-methods` tutorials when the
matrices strand it describes further down the same file had brought
those to 83 and eight. `planning/README.md` still called reader-added
practice cells unbuilt. `ARCHITECTURE.md` and `QUESTIONS.md` pointed
tutorial writers at `README.md` for a format it no longer documents.

Merging 7.83/7.84 in mid-review made the point immediately: the docked
sidebars landed while this was open, so `docs/FOR_STUDENTS.md` was
describing a Reference button in the page's top-left corner that no
longer exists, and had no Series panel in it at all. Both were rewritten
against the shipped markup rather than the old README's description.
`docs/MINI_IDE.md` and `docs/DEWMINI.md` picked up the same correction —
7.84 changed both IDEs' panels without touching either document, leaving
`MINI_IDE.md` still saying Help and Settings "share the same corner".

*Cost to change: small. Nothing here is code, and no built page links to
any of these files; reversing it is a `git revert` plus deciding what to
do about the staleness fixes, which are worth keeping either way. The
ongoing cost is the opposite of the usual one — four documents can drift
apart where one could not, so `CONTRIBUTING.md`'s "who reads what"
section now names each of them explicitly rather than describing
categories.*


**7.86 — The cheat-sheet rename finished in `QUESTIONS.md`: two dead
file paths fixed, and the term itself changed there too, reversing
7.82's carve-out for that file.** 7.82 renamed
`planning/CHEAT_SHEETS.md` to `planning/REFERENCE_PANEL.md` and
`tests/e2e/test_cheat_sheet.py` to `tests/e2e/test_reference.py`, and
settled at the time that `DECISIONS_LOG.md` and `QUESTIONS.md` would
both keep the old term in entries already written, on this project's
convention of not rewriting finished history.

Two references to the old *paths* survived that, which the convention
never covered: `QUESTIONS.md` §"Is a structured YAML glossary file the
right format" pointed a reader at `planning/CHEAT_SHEETS.md` §3/§4 as
where the glossary format is documented, and §"What should the reference
panel become on a phone" pointed at `tests/e2e/test_cheat_sheet.py`'s
`TestMobile`. Both now name the files that exist; §3 and §4 of
`REFERENCE_PANEL.md` are still the glossary-file and skill sections the
first one meant, so only the filename was wrong. A settled entry's own
wording reads correctly as history, but a file path is a signpost, and a
signpost to a file nobody has is just broken.

**Then the term itself, asked for directly once the paths were fixed**,
and in two passes. First `QUESTIONS.md`: seven mentions across four
headings and three paragraphs became "reference panel", on the
reasoning that `QUESTIONS.md` is not a historical record the way
`DECISIONS_LOG.md` is — it is a live document a reader consults to find
out where a question landed, and a reader who has only ever seen the
panel called "Reference" should not have to work out that the two names
are the same thing.

Then the last two mentions anywhere outside the log, asked for once it
was clear how few were left.
`planning/MINI_IDE_AND_DEWMINI_NEXT.md`'s closing list had a bullet
announcing the rename in both names; it now names only the panel's
settled name and says where the older one survives.
`planning/DOCS_AND_COMMENTS_PASS.md` listed `CHEAT_SHEETS.md` among the
files one pass rewrote, and now names `REFERENCE_PANEL.md` — the same
file, under the name it has.

**`DECISIONS_LOG.md` is the sole exception, and stays that way.** It
keeps the old term throughout its own entries, 7.82's account of the
rename included, where the word is the subject rather than incidental.
A decision record edited to match later decisions stops being evidence
of anything: 7.82 would become an entry about renaming a thing to the
name it apparently always had. That is the line — every document that
describes how dewlab works now says "Reference"; the one document that
records what was decided when keeps the words used at the time.

A sweep for the same class of mistake across every markdown file except
`DECISIONS_LOG.md` turned up two more, both left alone as somebody
else's call rather than folded in here: `planning/BUILD_PLAN.md` links
to `outlines/from-everlearning.md`, an outline that was never written,
and `planning/EDITOR.md` §3 is titled for `assets/editor.html`, which
does not exist — the editor page's body is built in `build.py`'s
`write_editor_page()` and rendered into `shell.html`.

*Cost to change: none worth naming. Twelve string edits across four
files, no code and no behaviour. The headings that changed carry
anchors, but nothing in the repository links to a `QUESTIONS.md`
anchor.*
**7.87 — dewmini can import a `.py` file now, closing out one of the
five items on `planning/MINI_IDE_AND_DEWMINI_NEXT.md` §6's parity list —
and turned out to already be most of the way there.** A gap analysis
run before starting this work (per §6's own staged plan) found dewmini
already had `.ipynb`/`.py`/`.html` *export* and the Jupyter-compatibility
scanner — both had already been ported in an earlier session — and only
`.ipynb` *import* worked; `.py` was accepted nowhere. `run_query()` (the
other half of the SQLite item on that same list) turned out to need no
work at all: it already lives in the shared `assets/tutorial_tools.py`,
which dewmini's `SEED_GLOBALS_CODE` (`compose/dewmini.js`) already
exposes every name in `__all__` from — it was reachable in a dewmini
cell before this session started, just never mentioned as such.

**`parsePyCells()` (`compose/dewmini.js`) is the counterpart to
`downloadAsPython()`, not to Mini IDE's own `.py` parser.** Mini IDE's
own import/export pair uses a plain `# %%` marker and only ever carries
Python cells, since Mini IDE has no note/text-cell concept to preserve.
dewmini's own `.py` export already predates this port and already
handles both cell types, via its own `# ---- cell N ----`/
`# ---- note ----` markers (a text cell's content gets `#`-prefixed line
by line) — so the new parser recognizes *that* format, reversing the
exact prefixing `downloadAsPython()` applies, rather than adopting Mini
IDE's narrower one and losing note-cell round-tripping dewmini already
had on the export side. A file with none of those markers — a plain
script, or one from anywhere else — imports as a single Python cell,
the same fallback Mini IDE's own parser uses for an unmarked file.
`handleImportFile()` now dispatches on the picked file's extension
(`.py` vs `.ipynb`), and `#import-ipynb-file`'s `accept` attribute and
button label (`compose/dewmini.html`) were widened to match — the
`.ipynb`-suggestive element ids were left alone rather than renamed, to
avoid touching working wiring for a cosmetic-only change.

Verified with an actual export-then-reimport Playwright round trip
(three cells — Python, a text note with a blank line inside it, Python
— confirmed to come back identical, not just "some cells appeared") and
a separate plain-script-import check, alongside a re-run of the existing
`.ipynb` import path to confirm it still works unchanged.

Deliberately not done here: recognizing Mini IDE's own `# %%` marker
convention too, for cross-tool import. Nothing today produces a
Mini-IDE-format `.py` file that needs reopening in dewmini specifically
— worth adding if that becomes a real need (most likely once Mini IDE's
own retirement, `planning/MINI_IDE_AND_DEWMINI_NEXT.md` §6 step 3, means
someone's old exports are all that's left of it), not before.

*Cost to change: small — the parser is genuinely new code (there was no
existing `.py`-shaped parsing anywhere in dewmini to extend), but
self-contained: one new function, a two-line dispatch change, and an
`accept`/label update, with no engine or filesystem dependency the way
the next two items on §6's list (the file manager, and the Worker/Stop
migration) both have.*

**7.88 — dewmini can mount a persistent filesystem now: a real folder, OPFS,
or IDBFS, the same three backends Mini IDE already had, tucked into
Settings' own "Files" section rather than a sidebar tree.** The second
item on `planning/MINI_IDE_AND_DEWMINI_NEXT.md` §6's parity list. Asked
directly which shape this should take, since Mini IDE's own file-tree
sidebar is exactly the kind of visual weight dewmini is meant to avoid:
offered a compact Settings section, a fourth docked sidebar, or the
mounted filesystem alone with no browsing UI yet — a Settings section
was picked, matching dewmini's "nothing to configure before typing
code" ethos and adding no new permanent chrome to the page itself.

**`compose/dewmini-fs.js`** is a close port of `assets/mini-ide-fs.js`,
trimmed for the one real architectural difference: Mini IDE's version
sits behind `mini-ide-engine.js`'s Worker/main-thread dispatch, since
its Pyodide might be running in either place, while dewmini's only ever
runs on the main thread — so the FS primitives (mount/list/read/write/
delete/mkdir) call `pyodide.FS` directly, with no second dispatching
layer that would only ever have one path to dispatch to. `getPyodide`
is injected via `configure()` rather than imported directly, since
`dewmini.js` needs to call into this module (to mount once Pyodide
boots) and this module needs to call back into `dewmini.js` (to get the
live instance) — a genuine two-way dependency, which dependency
injection avoids turning into a circular-import tangle.

**A real collision this port had to design around, not just copy past:**
`mini-ide-fs.js`'s own OPFS backend mounts `navigator.storage.getDirectory()`
— the origin's one shared root — directly at its Pyodide-side mount
point. That was never a problem while Mini IDE was the only thing
mounting OPFS on this origin; it would be the moment dewmini did the
same thing unmodified, since both would be looking at the identical
underlying files, invisibly. dewmini's own OPFS mount gets a named
`"dewmini"` subdirectory of that shared root instead (`getDirectoryHandle`
with `create: true`), keeping its files separate from Mini IDE's own
un-namespaced mount — noted as a fix for the new arrival, not a
retrofit onto Mini IDE's already-shipped, soon-to-retire code. The
native-folder backend's own IndexedDB handle storage got the same
treatment for the same reason (a separate database name), so choosing a
folder in one tool never silently reconnects it in the other.

**A real gap this pass's own testing surfaced, not assumed safe from
reading the code: neither this port nor Mini IDE's own original synced
the filesystem after a cell's Python code writes to the mount directly.**
`writeFile()`/`deleteFile()`/`mkdir()` each schedule a debounced sync —
but only when *this JS module* makes the write. A cell running
`sqlite3.connect('/mnt/dewmini/x.db')` or plain `open(...).write(...)`
touches the mounted path entirely through Pyodide's own `FS`, never
through this module's functions, so nothing here ever knew to sync —
found by an actual write-then-reload test coming back empty, not a
theoretical review. The `beforeunload`/`visibilitychange` flush both
this file and Mini IDE's own copy already had doesn't cover this either,
by design of the web platform: a `beforeunload` handler that kicks off
async work has no guarantee the browser waits for it to finish. Fixed
with a new exported `sync()`, called (fire-and-forget, so a slow sync
never makes a fast cell feel slower) once after every cell finishes
running in `dewmini.js`'s `executeCell()` — covers a cell's own writes
regardless of what API it used, and doesn't require Mini IDE's own
already-shipped, soon-to-retire code to be touched to fix the same gap
there. Verified with an actual write-reload-readback round trip, first
with a plain text file, then with a real `sqlite3` `.db` file (the
motivating use case for this whole item) — both survive a page reload,
not just a same-session read.

**A second real bug this pass's testing caught, also present in Mini
IDE's own original: the empty-file-list branch never cleared the list
it was hiding.** `renderFileList()`'s "no files yet" branch set the
`<ul>` to `hidden` but never cleared its children, so deleting a mount's
only file left a stale `<li>` sitting in the (invisible) list — found by
an actual delete-then-recount test, where the count stayed unchanged
instead of dropping to zero. Fixed here by clearing the list
unconditionally at the top of the function rather than in each
individual branch, so no future branch can reintroduce the same gap.

**`DEWLAB_PYODIDE_BASE` — the self-hosted-Pyodide override
`tutorial-runtime.js` and `mini-ide-engine.js` both already carry — was
missing from dewmini entirely until this pass**, added on its own merits
(parity with the other two runtimes, and the standing answer if a school
network ever blocks the CDN, `OPEN_QUESTIONS.md` 32) rather than only
because this pass's own testing needed a way to point dewmini at a
locally-vendored Pyodide in a network-restricted environment — though it
did need exactly that, and its absence was the reason no automated
end-to-end verification of dewmini's actual filesystem behavior had ever
been possible before.

Deliberately smaller than Mini IDE's own file manager: the "Files" list
browses the mount's root only, not a full recursive tree — a flat list
fits a compact Settings section; a browsable tree does not, and Mini
IDE's own tree only ever browses one mount's root well anyway (per
`planning/MINI_IDE_AND_DEWMINI_NEXT.md`'s own §2, it was never true
multi-file *editing*, just browse/upload/delete). Real SQLite
persistence — the other half of §6's list, alongside this — needed no
separate work: `run_query()` was already reachable in a cell before this
session (`DECISIONS_LOG.md` 7.87's own finding), and a `.db` file under
the mount now simply persists the way any other file under it does.

*Cost to change: moderate — the FS module itself is a faithful, largely
mechanical port, but two of the three things worth naming here (the OPFS
namespace collision, the missing post-run sync) were genuine design
decisions this port had to make that Mini IDE's own code never had to
face or never got right, not just translation work. Each was caught by
an actual end-to-end Playwright test — upload-and-read, write-reload-
readback, delete-and-recount — run against a real, locally-vendored
Pyodide instance, not inferred from reading the ported code and trusting
it matched its source.*

**7.89 — dewmini's Python now runs in a Worker, with a genuine Stop
button, closing out `planning/MINI_IDE_AND_DEWMINI_NEXT.md` §6's parity
list.** The last of the four parity items, and deliberately last — every
earlier item (`.py` import, the file manager) could be built and tested
against dewmini's original main-thread-only interpreter; this one
replaces that interpreter itself.

Rather than duplicate Mini IDE's own ~700-line
worker/interrupt/postMessage engine a second time, `mini-ide-engine.js`
was renamed to `assets/pyodide-engine.js` and generalized into a shared
module both tools import — a deliberate, explicit exception to this
codebase's usual "each page owns a thin copy" convention (the same
convention `tutorial-runtime.js`'s own worker-communication block still
follows). Asked directly, sharing was preferred over a second copy for
two reasons specific to this file: its size makes duplication a real
maintenance cost, not a cosmetic one, and Mini IDE's own retirement is
now planned (`planning/MINI_IDE_AND_DEWMINI_NEXT.md` §6 step 3), at
which point this file simply keeps existing under dewmini alone rather
than needing to be merged back together. `dewmini-fs.js` was rewritten
to match — it now delegates every filesystem primitive to the shared
engine (`engine.mountNative`/`listDir`/`readFile`/`writeFile`/etc.)
instead of calling `pyodide.FS` directly, since a Worker-hosted Pyodide
isn't reachable from the main thread at all anymore. The OPFS
namespacing 7.88 already added (dewmini's own `"dewmini"` subdirectory,
kept separate from Mini IDE's un-namespaced root mount) needed no change
— mounting a named subdirectory handle and mounting a real folder handle
are the same operation from the engine's point of view.

Two genuine bugs turned up in testing, both specific to dewmini being a
second, differently-located page sharing a module written for one:

- **`tutorial_tools.py` 404'd on every dewmini boot.** The engine's
  internal `pageUrl()` helper resolved `"assets/tutorial_tools.py"`
  against `document.baseURI` — the *page's* URL. That's correct for
  Mini IDE, which lives at the site root, but dewmini lives one
  directory down (`compose/dewmini.html`), so the same relative path
  resolved to the nonexistent `compose/assets/tutorial_tools.py`
  instead. Fixed by resolving against `import.meta.url` (this module's
  own location, `assets/pyodide-engine.js`) rather than the page —
  correct for either page, since both import the same file from the
  same place. Renamed the helper `pageUrl()` → `assetUrl()` to match.
- **The Stop button never appeared on a cell's first-ever run.**
  dewmini's `runCell()` called `setRunButtonRunning()` — which reads
  `engine.canStop()` to decide whether the button becomes a real Stop or
  just a disabled "busy" indicator — *before* awaiting the engine's own
  boot. On a fresh page, `canStop()` reads its pre-boot default (false)
  at that point, so the button rendered as permanently non-stoppable, a
  busy-and-disabled "…", even after the worker finished booting and a
  Stop would have worked. Mini IDE's own `runCell()` avoids this by
  awaiting its own `ensureEngineAndFsReady()` *before* calling
  `setRunButtonRunning()`; dewmini's port had the two calls in the wrong
  order. Fixed by moving `ensurePyodide()` ahead of
  `setRunButtonRunning()` in dewmini's `runCell()`, matching Mini IDE's
  own sequencing. (`runAllCells()` already awaited the boot first and
  didn't have this bug.)

Also gave dewmini genuinely new capability dewmini's previous
live-namespace-only implementation had no way to offer: Jedi-backed
hover docs and signature help (`engine.hoverDoc`/`signatureHelp`, wired
into `createCodeEditor()` the same way Mini IDE's own already were) work
on code that hasn't run yet, not just on names already defined in the
running interpreter.

Verified end-to-end against a real, locally-vendored Pyodide, on both
pages sharing the now-common engine: cross-origin isolation actually
lands (`window.crossOriginIsolated === true`, `SharedArrayBuffer`
available) on each; a tight `while True` loop with no yield points is
genuinely interrupted by Stop, on the first click, on the first-ever run
of a page's very first cell; the interpreter survives an interrupt and
runs further cells afterward; Mini IDE's own Run/Stop, file manager, and
autocomplete were re-verified unchanged, confirming the rename and
generalization didn't regress the page this file originally belonged
to; dewmini's file manager and a write-reload-readback SQLite round trip
(7.88's own tests) still pass now that they run through the shared
engine instead of direct `pyodide.FS` calls; "Restart Python" (new in
Settings alongside the existing execution-mode status line) actually
produces a fresh interpreter, confirmed by a variable defined before
restart raising `NameError` after it rather than silently surviving.

*Cost to change: high — not the line count (most of it is generalizing
an existing, already-working file rather than writing new logic), but
the risk: this is the one item of the four that replaces dewmini's
actual execution engine, touches the file both tools now depend on, and
both bugs above were exactly the kind that only show up when a real
browser actually runs the thing — neither would have been caught by
reading the ported code and confirming it matched its source.*

---

**7.90 — Every tutorial is a folder, from the moment it is created.** A
tutorial was a lone markdown file at `tutorials/<module>/<slug>.md` that
grew a folder only when a second release was published — and when it did,
its practice page and its glossary stayed behind at module level. Four
tutorials were already in that state, so `ls` on a module showed a
`first-steps.glossary.yaml` and a `first-steps-practice.md` with no
`first-steps.md` anywhere near them, and every future release added
another. A tutorial is now `tutorials/<module>/<slug>/`, holding its
markdown at `<slug>.md`, its practice page, its glossary, its frozen past
releases as `v<version>.md`, and any pictures or recordings it uses.

**The migration cost nothing a reader could detect, and that was checkable
rather than hoped for.** Where a page is written and what a student's saved
work is keyed to are both computed from frontmatter — `Tutorial.out_path`
reads `module` and `slug`, never `self.path` — so moving source files could
not move a URL or orphan a storage key. Building the site before and after
and diffing the two trees produced no differences at all, which is the
strongest form the claim can take: not "the tests still pass" but "every
byte of all 87 pages is identical."

`glossary_path()` now reads `tutorial.path.parent` rather than rebuilding a
flat path from `(module, slug)`. That is a smaller change than it looks and
a more correct one: every release of a tutorial sits in the same folder, so
each one finds the same glossary without the function needing to know
anything about releases.

**Assets were the point of the folder, not a side effect.** There was
nowhere for a tutorial's own picture to live and no way to refer to one.
The obstacle was never storage, it was the reference: the current release
is served at `tutorials/<module>/<slug>.html`, one level *above* its own
folder, while a frozen release sits *inside* it at `v<version>.html`, so
any path an author wrote by hand would be correct for one and broken for
the other. `resolve_assets()` rewrites a plain `src="picture.png"` per
page, so the author writes the file name they can see beside the markdown
and never thinks about depth. A reference naming a file the folder does not
hold fails the build, on the same reasoning as a dead `tutorial:` link:
the alternative is a page that looks finished to everyone except the
student who opens it.

**The editor had two release shapes and now has one.** Its release path
branched on whether a tutorial was already a folder, and the two branches
disagreed about where the current release lives — one deleted `<slug>.md`
and left two `v<version>.md` files, the other kept `<slug>.md` holding the
*old* release while the new one became a `v` file. Neither matched what the
repository's own hand-made forks contained. Now `<slug>.md` is always the
current release and `v<version>.md` is always a past one, so "open the
tutorial" means the same file however many releases accumulate, and
releasing adds a file rather than moving any. `releasesOf()` had to start
naming release files exactly instead of taking every markdown file in the
folder — with the practice page now living there too, the old rule would
have offered a page of problems as a version students could be sent back
to. Two e2e expectations changed with it and one guard needed widening: the
report that warns "the cells have changed since the last release" compared
the buffer against whatever was committed at that path, which was right
only while a fresh release always landed at a fresh path. It now also
treats a version that differs from the committed one as a release rather
than an edit, which is what it always meant.

*Cost to change: low to reverse the layout mechanically — the moves are
scripted and nothing published depends on them — but rising, and that is
the reason for doing it now rather than later. The expensive half is not
the files, it is the two conventions that were quietly diverging: every
release published under the old editor added another folder in a shape no
document described. Reverting would also mean giving up assets entirely, or
rebuilding somewhere else for them to live.*

**7.91 — Mini IDE has retired.** dewmini's parity with Mini IDE
(7.87–7.89) was the trigger, not a further decision point — an explicit
instruction earlier in this same working session established retirement
as a given once parity landed, not something to re-confirm. There is one
Python workspace now, not two.

**The hosted URL redirects rather than 404s or silently disappearing.**
`assets/mini-ide.html` — the app itself for years — is now a short,
dependency-light notice page: a couple of sentences explaining that
dewmini covers everything Mini IDE did, a `<meta http-equiv="refresh">`
plus a JS `location.replace()` (belt and suspenders — the meta tag alone
still gets a reader there with JavaScript off) sending a visitor on to
`compose/dewmini.html` after a few seconds, and a link to go immediately.
A bookmark or an old link someone still has keeps landing somewhere
useful rather than a broken page — the assumption
`planning/ROADMAP.md`'s own Phase 6 open questions had already settled
on before this was built.

**The app itself survives, unlinked, only as the offline download's own
source.** The original `assets/mini-ide.html` was renamed to
`assets/mini-ide-offline-app.html` rather than deleted — `write_mini_ide_bundle()`
in `build.py` now sources the downloadable, self-contained Mini IDE
bundle from that renamed file instead of the (now short) hosted page,
so the offline download a student might already rely on keeps producing
a genuinely working copy of the original app, Stop button and all, not
the retirement notice. `assets/mini-ide.js`, `assets/mini-ide-fs.js`,
and `assets/mini-ide-style.css` all stay for the same reason — nothing
hosted links to them any more, but the bundle still needs them. Keeping
the offline download working, rather than retiring it along with the
hosted page, was a deliberate call: dewmini has no offline distribution
of its own yet (the one item of the original four-item parity list that
was never in scope for this pass), and the alternative — no offline,
run-without-a-server Python workspace at all until dewmini gets one — was
a real capability regression for anyone who already depends on that,
for the cost of keeping one already-working, self-contained artifact
building. `assets/pyodide-engine.js` — already shared with dewmini since
7.89 — is what makes this cheap: the renamed offline app imports the
exact same engine dewmini does, so nothing about the engine itself
needed touching for this.

**No bug this time, but only because it was checked rather than
assumed.** 7.89's own `pageUrl()`→`assetUrl()` fix (resolving
`tutorial_tools.py`'s path against the engine module's own location
rather than `document.baseURI`, the *page's* URL) was written to fix
dewmini specifically, before this file's own rename existed. Renaming
`assets/mini-ide.html` to `assets/mini-ide-offline-app.html` and
re-pointing `write_mini_ide_bundle()` at it changes what page is doing
the importing, again — exactly the kind of change 7.89's own bug grew
out of — so this got the same real-interrupt Stop-button test 7.89 used
on dewmini run against the actual downloadable bundle's own
`mini-ide.html`, rather than assuming a working hosted copy implies a
working offline one. It passed: `assetUrl()`'s fix generalizes correctly
regardless of which page imports the shared engine, confirmed rather
than assumed.

**Where the rest of the retirement went:** the homepage's two-workspace
chooser (`build.py`'s `write_index()`) became a single dewmini card —
`.dl-workspaces-grid`'s hardcoded two-column layout gained a `max-width`
so one card doesn't stretch into a lopsided bar; the about page dropped
its Mini IDE mention; `docs/DEWMINI.md` absorbed the file-manager/
SQLite/Stop-button/import material that used to live only in
`docs/MINI_IDE.md`, since dewmini now has all of it; `docs/MINI_IDE.md`
itself became a short pointer to `docs/DEWMINI.md` rather than staying
the several-hundred-line guide it was, on the same reasoning as the
hosted redirect page — a tombstone, not a 404; `docs/FOR_STUDENTS.md`,
`README.md`, and `ARCHITECTURE.md` §4 lost their two-workspace framing;
`docs/mini-ide-engine-explained.md` was renamed to
`docs/pyodide-engine-explained.md` (a rename `DECISIONS_LOG.md` 7.89's
own engine rename should have carried at the time, and didn't) and
rewritten to describe the shared module rather than a Mini-IDE-only
one; `docs/mini-ide-js-explained.md`, `docs/mini-ide-fs-explained.md`,
and `docs/dewmini-js-explained.md` (the last one substantially, since it
still described dewmini's pre-7.89 main-thread-only, no-file-manager
shape) were brought current. `planning/MINI_IDE_REDESIGN.md` and
`planning/DOCS_AND_COMMENTS_PASS.md` were deliberately left alone —
historical records of work already done, not descriptions of what's
live today, the same "tombstone, not rewrite" treatment
`planning/ROADMAP.md`'s own open question about retired planning docs
already anticipated.

*Cost to change: moderate — mechanically straightforward (a rename, a
short new page, prose updates across a genuinely large number of files),
but wide: nearly thirty files reference Mini IDE by name, and getting
the hosted-vs-offline split right (one URL now serves two different
purposes depending on whether it's `assets/mini-ide.html` the redirect
or `assets/mini-ide-offline-app.html` the packaged app) needed care in
`build.py` specifically, verified by testing the actual downloadable
bundle's Stop button, not just the redirect page and dewmini's own
already-covered behavior.*

---

**7.92 — dewmini has its own downloadable, offline-capable copy now, and
a real bug in *both* offline bundles' core promise got found and fixed
along the way.** The one item of the original four-item parity list
(`planning/MINI_IDE_AND_DEWMINI_NEXT.md` §6) never brought over —
explicitly out of scope for 7.87–7.91, on the reasoning that Mini IDE's
own offline bundle already covered "a workspace exists for a
no-connection classroom" well enough that dewmini going without one had
no visible cost. That reasoning stopped holding the moment Mini IDE
retired (7.91): dewmini is the only Python workspace there is now, so
its own offline bundle stopped being optional the same way its own Stop
button did in 7.89.

**`write_dewmini_bundle()` (`build.py`) mirrors `write_mini_ide_bundle()`
in shape, not in structure.** Mini IDE's own hosted page already sat at
the site root, so its bundle just flattens straight in. dewmini's hosted
page sits one directory down (`compose/`), with `../assets/...`,
`../data/`, and `../coi-serviceworker.js` references baked into
`dewmini.html`/`dewmini.js` themselves — so rather than rewriting any of
that (the path 7.89's own real bug came from, taken as a lesson rather
than repeated), the bundle instead mirrors the *hosted site's actual
folder shape*: `compose/`, `assets/`, and `data/` as untouched siblings,
exactly what those already-working relative paths already assume. Zero
rewriting of dewmini's own app code, at the cost of the real page sitting
one level down in the unzipped folder — solved with a tiny top-level
`index.html`, not by touching the real page.

**The offline promise both bundles made — "reopen it, no server needed"
— was never actually true, and nothing had tested it until this pass
did.** dewmini.js imports pyodide-engine.js and dewmini-fs.js with real
`import`/`export` statements, the same way any modern web app is built;
a browser only permits that kind of cross-file import from `http://` or
`https://`, never from a file opened by double-clicking off disk — a
`file://` page has no origin a CORS check can approve, so the browser
silently blocks the import and the page's own JavaScript never runs at
all, no visible error, just a blank toolbar. Building this bundle and
actually opening the result the way a downloader would — not assuming a
folder of files just works because the code inside it is correct — is
what surfaced this; it was checked, immediately, against Mini IDE's own
already-shipped bundle too, which turned out to carry the identical,
equally untested "reopen it, no server needed" claim in its own
docstring and hits the identical failure.

**Fixed with `serve.py`, not by restructuring either app to avoid ES
modules.** Rewriting dewmini.js/pyodide-engine.js/pyodide-worker.js into
non-module classic scripts just to satisfy `file://`'s CORS rule would
mean forking the exact shared engine 7.89 and 7.91 both went out of
their way to keep as one file, maintained twice from then on for every
future change — hugely disproportionate to what the actual problem
needs. `serve.py`, dropped into both bundles by the new shared
`write_offline_serve_script()`, is a zero-dependency wrapper around
`http.server` (the same module README.md's own "Running it on your own
machine" section already has a contributor run for the site itself) that
serves the unzipped folder to `localhost` and opens a browser tab there
— satisfying the CORS rule with nothing beyond what a machine able to
run the script at all already has. dewmini's own `index.html` goes
further and checks `location.protocol` itself: served, it forwards
straight to `compose/dewmini.html`; opened bare as a file, it explains
`serve.py` right there instead of forwarding into a page that would just
come up blank with no visible reason why. Mini IDE's own bundle gets the
same `serve.py` plus a plain `README.txt` beside it, rather than a
matching in-page check — editing that legacy, offline-only file for a
nicer error message was judged not worth the touch; a README a
downloader sees the moment they unzip says the same thing without it.

**What's actually in the dewmini bundle:** `compose/` copied wholesale
(no rewriting), the shared engine and worker, `tutorial_tools.py`, the
CodeMirror bundle, and — found missing from `MINI_IDE_ASSET_FILES` while
building this bundle's own equivalent list, and left that way there,
per the same "not this pass's tool to fix" reasoning as everywhere else
in 7.90–7.91 — the four worked-example `.ipynb` files Settings' "Keep a
copy" section offers, and the whole `data/` folder those examples (and
any `load_csv()` call) read from. `assets/vendor/pyodide/` is included
when a build has fetched it (same `dev/fetch_pyodide.py` mechanism
7.90/7.91 already use, asked for dewmini's own package list — Pillow in
particular, which Mini IDE's own bundle has never needed).

**Verified end-to-end, served the way a downloader actually would run
it** (`python3 serve.py`, not the hosted site): the same real-interrupt
Stop-button test 7.89/7.91 used elsewhere passes against the served
bundle specifically; a worked example loads correctly (the
`assets/examples/*.ipynb` fetch); `await load_csv("co2-emissions.csv")`
reaches the bundled `data/` folder and returns the real row count; the
`file://`-opened case shows the new instructions instead of a blank
page; and the existing hosted dewmini, the existing Mini IDE offline
bundle, the full unit suite, and `dev/check_doc_links.py` were all
re-run afterward to confirm none of this touched anything that used to
work.

*Cost to change: moderate — the bundle itself is a fairly mechanical
port of `write_mini_ide_bundle()`'s own shape, but the real cost was the
`file://` finding: it applies to both offline bundles this codebase has
ever shipped, not just the new one, and would have shipped a second time
(this pass's own bundle, freshly written, would have carried the exact
same bug its own docstring claimed not to have) had "does the folder
have the right files in it" been treated as the same question as "does
opening the folder actually work."*

---

**7.93 — Highlight a word, and the reference offers to look it up — but
only when it actually knows the word.** The reference panel could already
be searched, once a reader thought to open it and type. The gap this
closes is the moment a reader is *already* looking at a term they half
remember, in the middle of a paragraph, and would have to leave the
sentence to go and ask about it.

**The design decision that matters is the silence.** The obvious version
of this feature reacts to every selection — filtering the panel live as a
reader drags across text. That version is unusable: most selections are
someone copying a sentence, and having a panel lurch about in response is
exactly the kind of interruption `planning/VERSIONING_AND_PROGRESS.md`'s
"a notice, never a block" instinct exists to rule out. So the offer
appears only when the selected text matches a term this page's reference
has actually taught. Select an ordinary word and nothing happens at all,
which is the common case and the one worth optimising.

Matching is against term *names* only, never definitions, for the same
reason: matching definitions would fire on ordinary words like "number"
that happen to appear inside some entry's prose, and the feature would
become noise. A selection matches when it contains a term or a term
contains it, so "matrix" selected inside a sentence about a
transformation matrix finds the entry, and so does the whole phrase.

Three things were found by driving it in a real browser rather than by
reading the code, and each was a genuine defect rather than a polish item:

- **The manifest's glossary is a flat list of entries, not entries grouped
  by kind** — `renderReference()` does the grouping for display. The first
  draft read it as grouped, which produced an empty term list and a
  feature that silently never appeared.
- **`initReference()`'s click-outside handler closed the panel the button
  had just opened.** The button lives outside the panel and outside its
  toggle, so it looked like a click elsewhere. It is now named there as a
  way in, beside the existing exemption for Settings.
- **A selection can be off-screen**, restored on load or left behind by a
  scroll, and placing the button at its coordinates put the button
  off-screen too — invisible but still reachable by keyboard. It now
  declines to appear for a selection nobody can see, and clamps to the
  viewport otherwise, flipping above the selection where there is no room
  below.

The button releases the selection when used, which is what stops it
re-offering the same lookup a second time: the `mousedown` handler
deliberately preserves the selection long enough to read the term off it,
and the click is where that ends.

*Cost to change: low. One function in `assets/tutorial-runtime.js`, one
CSS block, one line of exemption inside `initReference()`, and no new
storage, no manifest change, no build change at all — it reads the
glossary the manifest already carries and calls the filter the panel's own
search box already uses. Removing it would leave no trace.*

---

**7.94 — "Where did I meet this?" answered in the reference panel, after
the prose-linking version was built, measured and withdrawn.**
`planning/ROADMAP.md` Phase 5 proposed linking every later occurrence of a
taught term in the prose back to the tutorial that introduced it. That was
built — a tag-walking rewrite of the rendered HTML, skipping code,
headings and existing links, linking the first occurrence per section, with
the anchor taken from the term's emphasised first use. It worked, produced
347 links across the site at about ten a page, and was structurally sound:
no nested anchors, nothing rewritten inside a cell.

**It was withdrawn because the links were wrong too often to ship.** The
glossary's terms include ordinary English words — *set*, *shape*, *limit*,
*function*, *list* — and a regex cannot tell which sense a sentence means.
Sampling the eight uses of *shape* on one page: six were the everyday word
("the shape of that improvement", "whatever shape a problem needs", "a
flattened shape"), and two were a matrix's shape. A majority of the matches
for that term pointed a reader at the wrong tutorial with complete
confidence.

That is worse than not linking at all, and specifically worse for the
readers this project exists for. `PEDAGOGICAL_STYLE_GUIDE.md` §1 describes
adult learners returning to education, many expecting to be bad at
mathematics; sending one of them to a tutorial on set theory because the
prose said "set a seed" costs confidence, not just a click. A false
positive here is not a small defect in a useful feature.

**The goal survives; the mechanism does not.** Each reference entry a
reader inherited from an earlier tutorial now carries "Introduced in
*Title*", linking to the section that teaches it (`origin_of()`,
`origin_anchor()` in build.py; the render in `renderReference()`). A
tutorial's own new terms carry no origin, since "you met this here" on the
page teaching it says nothing. There is no way for this to be wrong about a
sense, because it never guesses at one: the entry a reader is already
looking at *is* the term, so naming where it came from is a fact rather
than a match. It also composes with 7.91 — select a word, get the panel,
see where you met it — which is the whole journey the prose links were
trying to shortcut.

Worth recording for anyone who reaches for the prose-linking idea again:
the obstacle is sense disambiguation, not matching. Stemming, a `forms:`
list, or longest-match-first — all of which the roadmap anticipated — solve
a different problem than the one that actually bit.

*Cost to change: low. `origin_of()` adds one optional key to a manifest
entry and nothing reads it but the panel; the prose-rewriting code is gone
rather than disabled, and this entry is what remains of it.*

---

**7.95 — The edges audit: the offline bundle proved, two phone-width
failures fixed, one heading-order break corrected.**
`planning/EDGES_AUDIT.md` has the full account. Three things had been
asserted and never tested, and testing them found two real defects.

**The offline bundle works, and now that is a measurement rather than a
belief.** `planning/MINI_IDE_AND_DEWMINI_NEXT.md` §2 had said plainly that
nothing proved the downloaded folder boots without a network. It was built
with a vendored Pyodide, served from loopback, and loaded with every
non-loopback request aborted: zero blocked requests, and a cell printing
`42` under Python 3.13.2 with the network still off.

**At 375px the page scrolled sideways, for two separate reasons, both
URLs.** A bibliography DOI took a tutorial to 381px against a 375px
viewport — and every tutorial ends with a bibliography. Worse, a Pyodide
failure message names the URL that failed, and that took the page to
**511px**. The failures compound: the reader who sees that message is by
definition the reader on a poor connection, and the message itself then
made the page unreadable on their screen. `#dl-body` now breaks inside a
word where a word cannot fit, `.dl-status` wraps anywhere, and every page
fits 375px exactly.

`tests/e2e/test_narrow_screen.py` was checked against the un-fixed
stylesheet before being trusted — two of its three tests fail without the
fix. A regression test that passes either way is worse than none, because
it reports safety it is not providing.

**The contents page jumped `h1` to `h3`**, which a screen reader
navigating by heading level hears as a missing section. It was deliberate:
a comment explained that every `h2` on that page was read as a module
heading, by the markup and by a test helper. That is a convenience for
people reading the code, paid for by everyone navigating the page by ear.
Module headings carry `.dl-module-heading` now, so telling them apart no
longer depends on the level.

**What this audit is not.** The structural checks — every control named,
no missing `alt`, one `h1`, landmarks, `lang` — all pass, and they say
nothing about whether a tutorial page is usable with a screen reader.
Reading order, whether a sidebar announces itself, whether running a cell
says anything to someone who cannot see the output: all still need a
person. That is stated at the end of `EDGES_AUDIT.md` rather than left for
someone to infer from a green checklist.

*Cost to change: nil to reverse — two CSS declarations and a class name.
The value is not in the code, which is trivial, but in the three claims
that are now tested and the one that is honestly still open.*

---

**7.96 — Five defects in 7.91 and 7.92, found by reviewing my own work
before it merged.** Recorded because four of them were invisible to the
tests that were meant to cover them, and one is the same mistake 7.92 was
written about.

**The lookup offered ordinary words.** `termFor()` matched a selection
against a term by plain substring, either way round — so selecting "and"
offered *pandas*, and "excellent" offered *cell*. That is precisely the
false-positive class that got prose-linking withdrawn one entry ago,
arriving by a different door: 7.92 removed a feature for guessing wrong
about ordinary words while 7.91 shipped one doing the same thing. Matching
is now whole-word in both directions, with an exact match preferred, so
selecting "running estimate" offers that rather than *estimate*.

**A page with few entries stayed filtered.** `renderReference()` hides the
search box below six entries, and the lookup skipped setting its value in
that case. `initReference()`'s observer clears the filter on close by
reading that value, so such a page reopened still filtered to one term,
with no visible box to clear it. The value goes in whether or not the box
is shown.

**The origin anchor could land in the bibliography.** `origin_anchor()`
fell back to a term's first plain occurrence, searched over raw HTML —
which matched the Metropolis and Ulam citation title and sent a reader
looking for "Monte Carlo method" to *Where to Read More*, the one section
that does not teach it. It now searches per `h2` section, over each
section's text rather than its markup (a raw search also matches inside an
`href`), and skips the bibliography outright.

**A practice page resolved origins from the wrong directory.**
`cumulative_glossary()` recursed with the *target* tutorial, so hrefs were
computed relative to that tutorial's folder rather than the page the reader
is on. Identical for a default practice page and its default tutorial, and
one level short — a 404 — the moment either has a frozen release. The page
being rendered is now passed down explicitly. A practice page's own
tutorial's terms gained an origin as a side effect, which is right: on a
practice page every term came from somewhere else.

**A regression test that tested nothing.** 7.93's narrow-screen test built
its own `.dl-status` element and appended it *inside* `#dl-body`, where it
inherited that element's `overflow-wrap` and passed with the `.dl-status`
rule deleted. The real `#dl-status` is a sibling of `#dl-body` and inherits
nothing from it. Worse, the check that "proved" the test caught a
regression had reverted both rules at once, so the passing half was never
isolated. The test now drives the real element and asserts it is outside
`#dl-body`, so the day that stops being true the test says so rather than
quietly going hollow.

*Cost to change: nil — this is the fix, not a decision. Worth an entry
because the pattern is the point: two of the five were found only by
running the thing in a browser and reading the values it produced, and one
was a test agreeing with itself.*

---

**7.97 — Six defects the Worker migration (7.89) left behind, found by
reviewing it after it merged.** Reviewing a merged PR is not the usual
order, and it earned its place: the first of these makes both workspaces
unusable until the page is reloaded.

**"Restart Python" wedged the tool it exists to unwedge.**
`pyodide-engine.js`'s `restart()` terminated the worker and called
`pendingRequests.clear()` — dropping the in-flight promises rather than
rejecting them. No reply was ever coming, so an awaited `run-cell` never
settled, the caller's `finally` never ran, and dewmini's `running` guard
stayed set. Every later Run was ignored. Reproduced in a real browser
against a locally served Pyodide: without the fix, Run All is left visibly
`disabled` after a restart and nothing recovers it short of a reload; with
it, a later cell runs. `restart()` now rejects what it drops. The engine is
shared, so Mini IDE was exposed to the same path.

**Two follow-ons that only became reachable once it rejected.**
`runAllCells()` reset each cell's Run button *after* its await with no
per-cell `try`, so a rejection mid-batch unwound past that cell and left
its button showing "running" — Mini IDE's own loop already had the guard.
And `uploadFsFiles()` returned silently on a boot failure with a comment
saying `ensurePyodide()` had reported it; the rewritten `ensurePyodide()`
catches only the filesystem mount and lets a boot failure out, so an upload
after one did nothing and said nothing.

**An open output stream survived a re-render it should not have.**
`applyOutputEvent()` looks the output element up fresh each event but
caches the open `<pre>`. Reordering or inserting a cell mid-run replaces
the output area underneath, and text then appended to the detached node
vanished. Reachable precisely because the worker keeps the page responsive
while a cell runs. A cached `<pre>` no longer inside the current output
area is now treated as no open stream, and a fresh one is started.

**Two documentation claims the migration falsified.** dewmini's Help panel
listed `text_input`, `dropdown`, `button` and `image_input`, and
`docs/DEWMINI.md` said they "work here exactly as they do on a tutorial
page, since dewmini keeps Python in the main page" — which stopped being
true the moment it did not. All four raise `RuntimeError` off the main
thread (7.77's accepted gap, inherited here). That same document also still
said a runaway cell had to be waited out, describing the absence of the
button the PR added, and called the shared data folder empty when it holds
three datasets. `docs/WRITING_TUTORIALS.md` was wrong the same way and is
now explicit that the widgets error on the hosted site and work in a
downloaded copy.

**And `__name__` disagreed with itself.** The live page is seeded by the
shared engine (`__dewlab__`); dewmini's standalone export carries its own
seed and still said `__dewmini__`, so one notebook answered differently in
the page and in the file downloaded from it. The export now matches.

*Cost to change: nil — these are fixes. Recorded because of what the set
has in common: every one of them was created by moving execution off the
main thread, and none was caught by a test. Three needed a browser to see
at all, and two were documentation that quietly became false while the code
around it was correct.*

---

**7.98 — Mini IDE is removed, not just retired.** 7.91 retired the
hosted page but deliberately kept the app alive underneath: the renamed
`assets/mini-ide-offline-app.html`, its `mini-ide.js`/`mini-ide-fs.js`/
`mini-ide-style.css`, and `write_mini_ide_bundle()` still packaging them
into a downloadable bundle — on the reasoning that dewmini had no
offline distribution of its own yet, so retiring the only offline
workspace would have been a real capability regression. 7.92 ended that
reasoning by giving dewmini its own offline bundle; this entry acts on
the expiry. The four asset files, the bundle function and its
`site/download/mini-ide` output, the tombstone `docs/MINI_IDE.md`, and
the two explainer docs for the deleted code (`mini-ide-js-explained.md`,
`mini-ide-fs-explained.md`) are all gone, and every present-tense
reference across code comments, docs, tests, the deploy workflow, and
planning was reworded — a workspace that no longer exists should not
keep turning up by name in the description of the one that does.

**The redirect goes too — because there was never anyone to redirect.**
The first draft of this removal kept `assets/mini-ide.html` as an
instant redirect to `compose/dewmini.html`, on 7.91's own reasoning
that an old bookmark or link should land somewhere useful. The person
the site is for then supplied the fact that decides it: the site has
not been deployed or shared with students, so no bookmark to the old
URL exists anywhere but in this repository's own history. A redirect
with no possible visitors is furniture, not continuity — removed, along
with `build.py`'s copy of it to the site root. (If the URL had ever
been shared, the redirect would have been the right call; the reasoning
in 7.91 was sound and simply rested on a premise that turned out false.)

**Historical records stay historical.** `planning/MINI_IDE_REDESIGN.md`,
`planning/MINI_IDE_AND_DEWMINI_NEXT.md` (which gained a fourth addendum
recording this removal), `planning/DOCS_AND_COMMENTS_PASS.md`, and this
log's own earlier entries keep their original wording — they describe
what was true when written, which is the point of keeping them. Present-
tense documents (`ARCHITECTURE.md`, `STATUS.md`, `ROADMAP.md`'s Phase 6
records, the explainer docs, `CONTRIBUTING.md`'s examples) now describe
one workspace.

**Found while removing: the deploy guard never excluded dewmini's own
bundle.** `.github/workflows/deploy.yml` counts the built downloadable
copies against the built tutorial pages and excluded
`site/download/mini-ide/` from that count — but not
`site/download/dewmini/`, whose `index.html` and `compose/dewmini.html`
(shipped since 7.92) land in the same find. The exclusion now names the
bundle that actually exists.

*Cost to change: low — the deletions themselves are the easy half; the
care was in the sweep, since nearly forty files mentioned the old
workspace by name, and in deciding which mentions were history (kept)
and which were descriptions of the present (reworded). With the site
never deployed, nothing removed here was ever in anyone's hands: no
bookmark breaks and no downloaded bundle exists outside this
repository.*

---

**7.99 — dewmini becomes a workbench: tabs, two rails, and tools for
looking at your own work.** Asked for directly: tabs, sidebars on both
sides carrying file imports and "variable inspectors and other
pedagogical tools", a fuller reference with search and category
navigation on the left, data import from somewhere like Our World in
Data, and a right-hand side moved away from settings and towards notes
and pedagogy. Widgets — the one real capability gap — were explicitly
deferred. `planning/DEWMINI_WORKBENCH.md` is the design; this entry is
what was decided along the way.

**The smallness rule is not abandoned, it is restated.** Every planning
document dewmini has says it is the small one, and §3 of
`MINI_IDE_AND_DEWMINI_NEXT.md` made "nothing that makes it bigger" its
whole finding. That rule existed because dewmini had a larger sibling to
be small *against*. 7.91 removed the sibling. A tool with no alternative
cannot also refuse to grow, so the discipline becomes **quiet by
default, everything one press away**: nothing new opens on a first
visit, the notebook keeps the full width until a rail is asked for, and
someone who came to check `6 * 7` sees exactly what they saw before.
Every decision below was checked against that sentence.

**Three panels across two edges, and the layout was already built.**
Library (left) is what you look up; Workbench (right) is your own work;
Settings keeps the right edge with the Workbench and stops being the
headline — Notes and Files moved out of it, which is the substance of
"make the right bar more into notes and pedagogical ideas". Help stopped
being a panel and became Library sections, on `SIDEBAR_CONTENT.md` §4's
own reasoning that extending a panel beats adding one. The mechanism
needed almost nothing new: `tutorial-style.css` has carried
`data-dl-panel-left`/`-right` with independent width variables since
7.83, and dewmini had overridden it with a single attribute and one
width — a fair simplification while both its panels docked right (7.84),
and exactly wrong with a rail on each side. Deleting that override *is*
the two-rail layout. Two smaller corrections fell out of it: a
left-docked panel resizes with native CSS (it grows away from its own
edge, which is why the right-docked ones need the JS handle), and a
docked rail must not close on an outside click — dismiss-on-outside is
right for a popover and wrong for a pane the page has made room for,
where every click on your own code would shut the reference you opened
to read while writing it.

**Tabs re-point one variable rather than rewriting the file.**
`notebooks[]` holds `{id, name, cells}`; the module-level `cells` is not
a copy of the active notebook's array but *is* that array, so every
existing function kept working untouched. The cost is one real hazard —
assigning `cells` alone detaches it, leaving edits landing in an array
attached to nothing, visible until a tab switch silently reverts them —
so `setCells()` is the only sanctioned way to swap them, and the e2e
test covers exactly that round trip. Storage moved to
`dewmini:notebooks:v1` with a one-way migration from the old bare array,
tested, and the old key deliberately left in place rather than deleted:
if the migration is ever wrong, the original is still there.

**One Python session shared by every tab, made visible rather than
silent.** Real Jupyter gives each notebook its own kernel. Doing that
here means threading a namespace identifier through every engine call
and across the worker boundary — a change to the shared engine, which
7.97 established is a change to every surface that runs Python, and a
poor trade to make overnight without the person it is for available.
Instead the sharing is *shown*: the Workbench's Variables list is one
session, and says so in plain words whenever a second tab exists. A
student who defines `data` in one tab and finds it in another has been
told and can see why. If it turns out to confuse people, the per-tab
namespace is the fix and this paragraph is the brief for it.

**The reference drops the one rule the tutorial pages' own is built
around, on purpose.** `REFERENCE_PANEL.md` §1 is emphatic that a reader
must never be shown a term they have not been taught — a reference that
spoils next week's function names is worse than none. That rule protects
a reader's position in a sequence. dewmini's readers have no position in
a sequence; that is what a workspace *is*. So
`write_reference_index()` emits the union — 248 terms today, deduplicated
on `(term, kind)`, grouped by the five kinds the schema already defines,
searchable across terms and definitions, with category filters — from
the same `own_glossary()` the tutorial pages use, so neither can drift.
Each entry names the tutorial that introduced it but does **not** link
to it: this file ships inside the offline bundle, which carries no
tutorials, and a link that 404s for every offline reader is worse than a
title that tells them where to look.

**The variable inspector is Python, not JavaScript.**
`describe_globals()` walks `_page_globals` and returns plain
`{name, type, summary, kind}` strings: it belongs where the namespace
lives, nothing crosses the worker boundary as a proxy, and — the reason
that matters most here — it is unit-testable under plain CPython, which
the JavaScript half is not. Eleven unit tests cover it, including a
value whose `__repr__` raises, because that is a bug in a student's own
object and not a reason for every other variable to vanish from the
panel.

**Data: one claim this environment could not test, so it is not made.**
The catalogue lists local and remote datasets with real source and
licence, and writes working code into the notebook when picked. Remote
fetching depends on the other site permitting it (CORS), and the sandbox
this was built in blocks `ourworldindata.org` outright — the fetch could
not be tried once. Twice already this repository has shipped an untested
claim (7.92: two offline bundles that could not be opened at all), so
`load_csv()` was extended to take a URL *and* to fail informatively —
naming CORS, and pointing at the reliable route of downloading the file
and adding it through Files — and `tests/MANUAL_CHECKLIST.md` carries
the check nobody here could run.

**dewmini has e2e coverage for the first time.** Twelve tests driving
real Chromium against a self-hosted Pyodide: tabs keeping their own
cells across a switch, the migration from pre-tabs storage, both rails
open at once, same-edge panels excluding each other, a rail surviving a
click on your own code, reference search and kind filters, a dataset
writing its own cell, and the inspector reading variables out of live
Python. 7.96 and 7.97 were both rounds of defects in code that looked
right and had no browser test; this is the answer to that, and it found
one thing immediately — an empty cell container has zero height, so
"visible" is not what a test should wait on.

*Cost to change: substantial and mostly additive — ~900 lines across
dewmini's three files, one build step, one shared-engine message, and a
vendored CodeMirror addition for find-and-replace. The risk concentrates
in two places: the `cells` aliasing above, and the shared engine, where
`describeGlobals()` follows the existing `page-names` path exactly
rather than inventing a second shape. Everything else is a panel that
either renders or does not.*

---

**7.100 — Ordinary Python HTTP code works here now, and `https` was never
the thing that was missing.** Prompted by a real failure on the live site:
pasting Our World in Data's own copy-this-to-fetch snippet into a cell gives
`urllib.error.URLError: <urlopen error unknown url type: https>` in 8ms. That
message is accurate and useless, and the snippet is the obvious thing to
try, since it is the button on their page.

**Two claims I made about this were wrong, and the correction is the
entry.** I said `requests` "isn't available and can't be", and that reading
a URL with pandas could not work in a browser. Both false. Pyodide ships
`requests`, `httpx`, `aiohttp`, `urllib3` *and* `pyodide-http`, whose entire
job is to reroute Python's HTTP machinery through the browser's own
fetching. They are simply not loaded at boot. Tested in a real browser
against a local server: after `pyodide_http.patch_all()`, the snippet works
**verbatim**, `storage_options` and all.

**The fix is 9.6 KB, so it is on by default.** `pyodide-http` alone —
without `requests`, which drags ~470 KB of certifi/urllib3/idna behind it —
is enough to make `pandas.read_csv(url)` work, because pandas goes through
`urllib` and the patch covers `urllib`. Loaded and applied at boot in both
engine paths (`NETWORK_PATCH_SOURCE`), wrapped in try/except so a vendored
Pyodide built before this existed still boots, just without the
convenience. Added to `dev/fetch_pyodide.py`'s baseline so new offline
bundles carry it.

**`https` was never unavailable — Python just had no handler for it.**
Worth stating plainly because the error implies otherwise, and because it
is a thing students are taught to care about. A Pyodide build ships no TLS
library, so `urllib` registers no HTTPS handler and rejects the scheme
before any connection is attempted. That is not the absence of encryption;
it is the absence of Python's *own* encryption. Through the patch the
browser performs the TLS, with its own certificate validation and its own
trust store — the same one it uses for every other site. Verified rather
than reasoned: a real TLS server with a real certificate, and Chromium
pinned to that one certificate by public-key fingerprint (rather than told
to ignore certificate errors, which would have proved nothing).
`pd.read_csv("https://…")` and `await load_csv("https://…")` both read it.

**The cost, named: a hung request cannot be stopped.** The patched path is
synchronous inside the Worker, so it blocks the interpreter while waiting.
Tested: the Run button correctly offers Stop, and pressing it does nothing
— eight seconds later the cell is still waiting. Before this change that
request failed instantly instead, so this is a new way to be stuck. Taken
anyway, because "instant unhelpful failure" is not better than "works, and
a slow server can hang you", and because the async route
(`await load_csv(url)`) does not block and remains what the docs lead with.
A timeout on the patched path is the obvious follow-up and is not done.

**Errors that are about the browser now say so.** `_ERROR_HINTS` in
`tutorial_tools.py` matches a small, deliberately short list of failures
whose Python message explains nothing a student can act on, and appends a
plain-English note under the traceback — under, not instead of, so the real
error is still findable. Two entries today, both about reaching the network.
The import scanner gained the same libraries, so a pasted notebook is
warned before it runs rather than after.

*Cost to change: small in code, wide in reach — this touches the shared
engine's boot, so it changes tutorial pages too. Justified on the same
grounds: a tutorial cell hits the identical wall.*

---

**7.101 — The reference's categories are derived, never tagged; and the
rail's smallest text gets a floor.** Three asks in one message, all of them
about the Library rail: a topics row that drops down without covering what
it filters, a check that the whole rail obeys the Texture slider, and — the
one that changed the design — "the layers are actually a great proxy for
beginner intermediate advanced! That way if we change the tree later (which
we inevitably will) it automatically changes the search."

**That is the whole scheme, and it is better than what it replaced.** The
first pass had subject and level as things someone would maintain. Reading
them off data that already exists means they cannot drift from the thing
they describe:

- **Subject** comes from the learning-outcome codes a tutorial already
  claims in `covers:`. The *prefix* is the key and `strand` is not: PDP-LO2
  ("algorithms") shares a strand with several MIT outcomes, so strands cut
  across the maths/computing line rather than along it. MIT is the maths
  module; PDP and CMPS are the computing ones. Seven tutorials claim an
  outcome from each side and are filed under both, which is not a fudge to
  avoid choosing — a term introduced there genuinely belongs to both.
- **Level** comes from `topic_tiers()`, the prerequisite depth of the
  `needs:` graph. Nothing is hand-tagged, so rearranging the tree re-files
  every term on the next build with nobody having retagged anything. There
  is a test that does exactly that: slide three layers of groundwork under
  a topic, rebuild, watch a term move from beginner to advanced while its
  tutorial is untouched.

**Deepest outcome, not shallowest.** `min()` was tried first and is worse in
both directions: it rates a tutorial by its easiest moment, which put 150 of
222 terms in "beginner", and it would cheerfully tell someone in week one
that a tutorial needing four layers of groundwork is approachable. Erring
deep is the kinder error. Bands at ≤2 / ≤3 against the real spread
(22/16/5 tutorials); the obvious alternative ≤1 / ≤3 collapses to 10/28/5,
which makes "intermediate" mean almost everything and so mean nothing.

**A tutorial claiming no outcomes is left unfiled, not guessed at.** Two
real ones do, plus every practice page. The row offers "Unfiled" as a value
of its own, so those terms stay reachable instead of vanishing the moment
any subject is chosen.

**The topic row is a `<details>` in the normal flow, not a popover.** Asked
for directly — it must not cover the results. So opening it pushes the list
down, and there is a test that measures the row's bottom edge against the
list's top edge rather than trusting a screenshot. Subject and level stay on
the surface because they are the two anyone reaches for; topic and kind fold
away because they are longer rows that would push the results off-screen
before a reader had seen any. A folded row that is silently filtering is a
trap, so the summary reports its own state ("Topics · 1 on").

**The group list is read off the data too — found by a test, not by
reading.** The topic row was drawing from a hand-kept list of group keys in
`dewmini.js`, which meant a group added to `topic-groups.yaml` would get no
chip and nobody would notice. That is precisely the drift the rest of this
entry is about, arriving through the one door left open. The curated short
labels stay (the file's own names are page headings — "Trigonometry —
triangles, circles, and waves" — and far too long for a chip), but they are
now an *override*: the groups themselves come from the entries, and an
unlabelled one gets its key turned back into words, which is a visible
prompt to come and name it.

**"A bit small for tired eyes" was right, and measurably so.** The rail does
scale with the slider — everything is in `rem` off `--dl-font-size` on
`html`, which was already true — but at the old floor of 15px the filter
chips rendered at 10.2px, the kind badge at 9.6px. The slider minimum moves
to 16px and the small labels take a `max(…, 12px)` floor.

**The sweep found five more than the eyeball did.** Checking the four
elements I had just changed said the job was done. A test that walks *every*
element in the rail and reports the smallest computed size found `<kbd>` at
10.6px, `<code>` inside a panel note at 11.6px, the "from the web" badge at
11px, and the rail's own section heading at 11.5px — all `em` sizes
compounding inside an already-small container, which is the failure mode
eyeballing is worst at. That sweep is now the test, so the floor holds for
anything added later rather than for the five things that were looked at
today.

*Cost to change: small. The bands are one tuple; the subject map is one
dict; the disclosure is one `<details>`. What would be expensive is going
back to hand-tagging, which is the point.*

---

**7.102 — The boot patch was not universal, and the toolbar had two buttons
for one job.** Two asks in one message, plus main moving underneath.

**The networking patch reached two of four boot paths, not four.** 7.100
said ordinary Python HTTP code "works here now"; Josh asked whether that was
true of the whole application, and it was not. dewlab starts Pyodide in four
places, and the patch had been added to the two I was looking at:

| Boot path | Used by | Had the patch |
|---|---|---|
| `pyodide-worker.js` `boot()` | every hosted page | yes |
| `pyodide-engine.js` `bootMainThread()` | dewmini with no Worker | yes |
| `tutorial-runtime.js` `bootMainThread()` | **a downloaded tutorial** | no |
| `compose/dewmini.js`'s export template | **an exported notebook** | no |

Both misses are the *downloadable* copies — which is the worst possible
place for them, not an acceptable one. A downloaded tutorial is the copy
someone opens on a train with no second machine to compare against, and an
exported notebook is the file a reader sends to somebody else. A cell that
read a URL perfectly well on the hosted site would have failed with the
same "unknown url type: https" in both, after every other surface had
stopped saying it. Fixed in both, wrapped in the same try/except so a
Pyodide without the package still boots.

Verified rather than reasoned, because the claim being corrected here was
itself reasoned: a real downloaded export, served from disk, booting its own
Pyodide, reading `https://` from a real TLS server with Chromium pinned to
that one certificate by public-key fingerprint. Two rows, two columns, over
a connection whose certificate was actually checked.

**The lesson is about how the gap was found.** It was not found by reading
the diff — I wrote the diff. It was found by Josh asking whether the claim
held everywhere, and then by enumerating every `loadPyodide(` in the
repository instead of every one I remembered. "Is this universal?" is a
different question from "is this right?", and the second does not answer
the first.

**The toolbar's Python and Text buttons are gone.** Also Josh's, and
correct: the seams between cells already add a cell, and add it where you
are looking rather than at the end of a page you then scroll back up. Two
buttons for the same action, one of them worse, is one button. The freed
space takes **See an example** and **Start with imports**, which previously
lived only in the empty-notebook block and so vanished the moment a reader
had a single cell — the two openings hardest to find were the two only
findable before you needed them.

**Which exposed a hole the change would have left.** The first seam was
suppressed over an empty notebook, on the reasoning that a seam with
nothing on either side looks like debris. With the toolbar buttons gone
that would have left no way at all to start a *blank* cell — only "Start
with imports", which arrives with three lines in it. The seam is now drawn
from the start, which is also the better teaching: the affordance a reader
uses for every cell after the first is the one they meet for the first.

**And a fixture bug that main exposed.** The dewmini e2e fixture pointed the
page at a locally staged Pyodide only `if "DEWLAB_PYODIDE_BASE" not in
html`. PR #91 added a comment to `compose/dewmini.html` explaining what that
override does — containing the name — so the guard was satisfied by prose,
the injection silently stopped, and every test that runs Python failed
against a CDN this sandbox blocks. It now matches the assignment and
asserts the result, because a guard that a sentence can satisfy is not a
guard. Worth recording as its own mistake: the failure looked exactly like
a regression from the toolbar change, and treating it as one would have
meant "fixing" working code.

*Cost to change: small. Two four-line boot additions, one markup move, and
one deleted conditional.*

---

**7.103 — Both rails drag the same way, and a width someone chose survives
the reload.** Josh asked whether the side rails are resizable, "so that one
could work split screen if one wanted to". They were — and measuring it
found two reasons the answer was worse than yes.

**Two rails, two different affordances.** The right-docked panels got the
full-height drag strip 7.84 built for them, because native CSS `resize:
horizontal` is unusable there: its grip sits at the box's bottom-right
corner, flush with the browser window's own right edge, with no room to drag
outward. The left-docked ones — dewmini's Library, and a tutorial page's
Reference and Series nav — were left on native resize, because for them it
*works*: a left-docked panel grows rightward, into the page.

Working is not the same as findable. Native resize is a small triangle in
one corner; the strip is the full height of the panel and highlights on
hover. So one page offered two ways to drag a panel wider, one of them
plainly better, and which one you got depended on an implementation detail
about which edge the panel happened to be pinned to. `makeRightEdgeResizable`
becomes `makeEdgeResizable(panel, side, …)`, the sign of the drag flips with
the side, and the native grips are gone from both files.

**And the strips were hung outside their panels, losing half their width.**
The handle sat at `left: -3px`, straddling the panel's edge — but a docked
panel is a scroll container (`overflow-y: auto`), which clips absolutely
positioned children to its padding box. Half of every strip was being thrown
away, and the surviving half ended exactly on the boundary. On the right
edge that still worked by luck: the leading edge of a clip is inclusive. On
the new left-edge variant it did not, and the first drag test moved nothing
at all. Hit-testing the strip's midpoint returned the *panel*, which is what
named the cause. Both strips now sit flush inside the edge.

Worth keeping because of how it was nearly missed: the strip was in the DOM,
the class was right, the CSS was right, and the geometry printed correctly.
Only a real pointer drag showed it doing nothing.

**A width nobody remembers is not a split screen.** `saveSidebarState()`
stored which rail was open and not how wide it had been dragged, so a rail
pulled out to half the screen snapped back on the next load. It now stores a
width per panel and applies them before reopening, so a restored rail opens
at its own size rather than opening small and jumping.

**Measured rather than asserted**, on a 1440px viewport: with the Library at
560px and the Workbench dragged to 612px, the notebook column sits at x=598
with width 191 — no overlap on either side, the three of them accounting for
1363 of 1440px. Split screen works in the sense the question meant.

*Cost to change: small, and it deletes more than it adds — one shared
function in place of two, and three `resize: horizontal` declarations gone.*

---

**7.104 — The union reference is settled, on a better reason than the one I
gave for it.** 7.99 and `DEWMINI_WORKBENCH.md` §4 dropped the tutorial
Reference panel's rule (`REFERENCE_PANEL.md` §1: never show a reader a term
from a tutorial they have not reached) and flagged it as Josh's to overrule.
He has confirmed it, and his reasoning is the stronger of the two:

> *"we just don't know what the student will be doing when they open
> dewmini? Maybe they have done all the tutorials online and we just can't
> see them?"*

My argument was about **dewmini's** nature — a workspace has no position in
a series, so there is no position to protect. His is about the **reader's**,
and it is the one that actually decides the case: the spoiler rule assumes
the page knows where its reader has got to. A tutorial page does know, from
its own position in the series. dewmini cannot know. Nothing is recorded
anywhere — no accounts, no server, no tracking (a deliberate property of
this whole project) — so "what has this person been taught" is not a fact
dewmini has access to, and hiding two thirds of the reference would mean
guessing it, wrongly, against a reader who may well have finished the
course.

Worth writing down because it changes what would reopen this. Under my
reasoning, the decision would be up for revisiting if dewmini ever became
more curriculum-shaped. Under his, it only reopens if dewmini gains a way to
*know* where a reader has got to — which would mean tracking them, which
this project has refused on other grounds entirely. So this is settled
harder than I had it.

*Cost to change: unchanged — one function, and both behaviours are tested.
But the reason to change it is now much narrower.*

---

**7.105 — A stale-output marker, strict from the start.** A dewmini
proposal ("Five Jupyter features worth having in dewmini") argued for two
paired features: execution counters (the `In [3]` numbers) and a marker
for when a cell's output no longer matches its code. Josh asked to leave
the counters out for now; the marker does not actually need them — it only
needs to remember what a cell's content looked like the moment it last
ran, and compare that to what is on screen now — so it ships on its own.

**Any difference counts, whitespace included.** The proposal flagged this
as an open question: is `answer = 42` vs `answer  = 42` really "edited
since last run"? I started strict, per the proposal's own recommendation,
because the alternative — diffing after some kind of normalisation — is a
judgement call about what counts as a "real" change, and a wrong judgement
there hides a genuine edit rather than merely annoying someone over a
harmless one. If this turns out to be noisy in practice (a reader
reflowing a paragraph in a docstring, say), loosen it then, with a reason
in hand rather than a guess.

**The marker does not survive a reload, on purpose.** `ranContent` is
never written to `saveState()`'s serialized shape and never read back by
`readCells()` — the same treatment `lastRunMs` and (had it shipped)
`execution_count` would get, for the same reason: nothing a cell's Python
actually *did* survives a reload either, since the interpreter itself does
not. A marker that persisted would claim a fact about a session that no
longer exists.

*Cost to change: small — one field on the cell object, one comparison
function, one CSS rule.*

---

**7.106 — Run above/below, behind a menu rather than two more buttons.**
The same proposal's third feature: run every cell from the top through a
given one, or that cell and everything after it — the practical repair
once a reader notices (from 7.105's marker, or just experience) that a
cell's output no longer matches what is above it.

**The mechanics were mostly already there.** `runAllCells()` already did
the whole job — the batch loop, the per-cell Stop-button state, the error
tally — just always over every Python cell and always after a namespace
reset. It is now `runCellBatch()`, parameterised on which cells and
whether to reset first, with `runAllCells()`/`runAbove()`/`runBelow()` as
its three callers.

**The one real risk was getting `reset` backwards.** "Run above" resets
the namespace first, the same as "Run all" — the point of running from the
top is that what is on screen matches what the code actually did, which a
lingering value from a previous run could quietly fake. "Run below" must
not: its entire reason to exist is keeping what the cells above it already
defined, so resetting first would erase exactly the state it was built to
preserve. Written down because getting this one boolean backwards would
have shipped a feature that silently destroys work rather than saves it.

**Where the controls went.** `.dm-cell-actions` had its Python/Text
buttons removed only recently, as duplicates of the insert seams (7.102) —
adding two more always-visible icons per cell would cut straight back
against that. Both options live behind one "⋯" toggle instead, opened and
closed the same way `armDeleteButton()`'s outside-click already works: a
document-level listener added only while the menu is open and removed the
moment it closes, rather than one kept alive for the cell's whole
lifetime — with a menu on every cell, an unremoved listener would be a
real per-cell leak, not a theoretical one. The cost is one extra click to
reach either option; the alternative the proposal raised, keyboard-only
shortcuts, would have traded that for a beginner-facing tool learning
Jupyter's own trapdoor (see this file's "Two I would argue against", still
true and unrelated to this entry).

*Cost to change: small-to-medium. The batch runner is one function used
three ways; the menu is self-contained and does not touch anything else
`.dm-cell-actions` already had.*

---

**7.107 — Maths in dewmini text cells: a second implementation, on
purpose, and the offline bundle takes the weight.** The same proposal's
largest item, and the one it explicitly flagged as needing a decision
first. `$x^2 + 3x$` in a dewmini text cell now renders as maths, the way
it already does in a tutorial.

**Ported, not called.** Tutorial maths runs through `build.py`'s
`extract_math()`/`render_math()` — Python, at build time, working on
python-markdown's input. dewmini's text cells run through
`renderDocMarkdown()` — JavaScript, at read time, a small hand-written
renderer that is not python-markdown at all. There was no function to
reuse, only the pattern: `extractDocMath()` in `compose/dewmini.js` lifts
`$…$`/`$$…$$` out into the same bare-alphanumeric placeholder scheme
(`dlmath0z`, `dlmath1z`, …) *before* `renderDocMarkdown()`'s own line-by-
line pass runs, for the same reason `extract_math()`'s own comment gives:
`$a_i$` loses its underscore to `renderDocInline()`'s emphasis rule
exactly the way it loses it to python-markdown's, if the parser sees the
raw TeX at all.

**This is a second maths renderer, and that is a deliberate, narrow
choice — not an oversight.** The proposal's own §5 lays out that dewlab
already has at least three markdown surfaces outside the tutorial
pipeline (dewmini text cells, the authoring editor's Milkdown/KaTeX, and —
this session's own finding, which the proposal's enumeration missed —
`assets/tutorial-runtime.js`'s own copy of `renderDocMarkdown()`, ported
from dewmini's for a *reader's own* cells inside a tutorial page), and asks
whether dewlab should converge on one client-side renderer the build also
targets. That refactor is not this change. Shipping the smaller, proven
thing first — with this entry naming it plainly as a second
implementation — means the unification question gets decided with two
working examples in hand instead of zero. `assets/tutorial-runtime.js`'s
own copy stays exactly as unaware of maths as it already is; if it needs
the same treatment, that is the follow-up, not a silent gap in this one.

**KaTeX's stylesheet loads unconditionally; its 266 KB renderer does
not.** Tutorial pages already make this exact trade in `assets/shell.html`
(1.8) — the 23 KB CSS is cheap enough to always pay, the JS is not.
dewmini has no manifest to gate the JS on at build time (a cell's content
is not decided until a reader writes it), so the gate here is behavioural
instead: `loadKatexRenderMath()` fetches the bundle the first time
`renderMathsIn()` finds a `.dl-math` span to render, and never before, and
never again after. A notebook with no maths in it never pays for either
KaTeX file beyond the CSS.

**The offline bundle takes the ~590 KB.** `DEWMINI_ASSET_FILES`
(`build.py`) used to carry a comment saying, correctly at the time,
"dewmini renders no maths" as the reason `vendor/katex.min.css` was
missing from the downloadable copy. That comment is now false, and the
proposal named the trade this reopens plainly: lazy loading only helps a
classroom *with* a connection on first use; a classroom with none at all
cannot fetch what was never lazy-loaded in the first place, so the offline
bundle either carries KaTeX (JS, CSS, and all twenty font files, added to
`DEWMINI_ASSET_FILES` and a new `shutil.copytree` for the fonts directory)
or maths silently fails in exactly the setting the bundle exists for. I
have included it, on the reasoning that a downloadable copy which cannot
do something the hosted site can do is a worse trade than 590 KB — but the
proposal marked this explicitly as Josh's call, and it still is; this
entry is that decision recorded, reversible by dropping three lines from
`DEWMINI_ASSET_FILES` and the fonts copytree if he decides otherwise.

**The standalone-HTML export needed no change, and that is a finding worth
recording.** The proposal's own text flagged `buildStandaloneHtml()`'s
single-file export as a likely gap: if a notebook with maths gets
exported, does the maths survive? It turns out the question does not
arise. That export already renders a text cell's content as plain,
literal `white-space: pre-wrap` text — `body.textContent = cell.content`,
not `renderDocMarkdown()` — so headings, bold, and bullets were never
rendered there either, maths included. There was nothing to inline,
because there was already nothing rendered.

*Cost to change: medium. The extraction/render-span code is small and
tested; the real ongoing cost is the ~590 KB now in every offline
download, and the standing question of when (if ever) to unify the
project's several markdown renderers into one.*

---

**7.108 — Restart and run all, as one button.** The same proposal's
smallest item: throw the interpreter away, then run every cell from the
top — the reproducibility check that goes with 7.105's marker (*that*
shows a notebook might not survive a fresh run; *this* proves whether it
does).

**The two halves already existed and needed no new logic**, only wiring:
`restartPython()` (factored out of what "Restart Python" already did —
`engine.restart()`, `dfs.reset()`, then `ensurePyodide()` again so
Settings reflects real status immediately) followed by the existing
`runAllCells()`.

**Whether that makes this button "just a label" was the proposal's own
open question, and the answer is no.** `runAllCells()` already resets the
*namespace* first (`engine.resetPageState()`), which is the cheap version:
clear and re-seed the same interpreter. `engine.restart()` is stronger —
a genuinely fresh interpreter, which also clears Jedi's completion cache
and forgets the mounted filesystem handle (`dfs.reset()`), neither of
which `resetPageState()` touches. So "Restart & run all" is a strictly
better reproducibility check than "Run all" alone, not a second name for
the same thing, and Settings now offers both.

*Cost to change: very small — one factored-out function, one new button,
two confirm dialogues.*

**7.109 — Three of dewmini's own cell features, ported onto tutorial and
practice pages.** `planning/CELL_IDENTITY.md` asked the underlying
question directly: tutorials, practice, and dewmini are three surfaces
showing the same idea, a cell that runs Python against a shared session,
in three different pieces of markup. Full unification — one rendering
function shared by `build.py` (static HTML at build time) and dewmini
(a live JS `cells` array) — is a large, invasive change the same
document explicitly did not choose; a practice page turned out to need
no separate treatment at all, since `build.py` already treats one as "a
tutorial in every mechanical sense." What shipped instead: the stale
badge, the "⋯" Run above/below menu, and Restart & run all (7.105,
7.106, 7.108) ported onto `build.py`'s `render_cell()` and
`assets/tutorial-runtime.js`, keeping the two engines and DOM systems
separate — the project's own stated convention ("each page owns a thin
copy... extract only when a shared fix needs to land in both").

**Not ported: the numbered identity pill, or maths-in-text-cells.** The
pill is `CELL_IDENTITY.md`'s own still-unbuilt design (nowhere yet,
dewmini included) — shipping it for tutorials first would mean building
a feature its own design note calls "not yet built" out of order. Maths
needed nothing: a tutorial's prose already renders `$…$`/`$$…$$` via
`extract_math()`/KaTeX (`build.py`), independent of dewmini's Text-cell
type, which doesn't exist on this side at all.

**The one real engineering gap**, closed here rather than deferred:
`assets/tutorial-runtime.js` had no `resetPageState()`/`restart()`
equivalent at all before this. Both now exist, built the same way
`pyodide-engine.js`'s already did — `resetPageState()` reuses
`pyodide-worker.js`'s existing `reset-page-state` message type
(already there for dewmini's sake) and a newly-named
`RESEED_GLOBALS_SOURCE` constant (previously an inline string, used only
once, inside `bootMainThread()`); `restartPython()` terminates the
Worker or drops the main-thread Pyodide references, then leans on the
existing `ensureBooted()` to reboot. `runCellWorker()`/
`runCellMainThread()` also now return whether a cell's run raised,
previously discarded — needed to count errors across a batch, the one
behavioural gap between a single Run click and "Run above/below".

*Cost to change: small. Every new function names the dewmini original it
was ported from; a future change to one is a reminder to check the
other, not a search. The real ongoing cost is the one this decision
argues against paying yet: a true shared cell implementation, still
undecided. The numbered identity pill's own design was still unbuilt
anywhere when this was written; 7.110 changes that, in dewmini.*

**7.110 — The full cell-identity design, built in dewmini.** The
numbered pill, per-type colour, merged run-line, and collapse triangle
`planning/CELL_IDENTITY.md` designed and 7.109 explicitly left out —
built now in `compose/dewmini.js`, on request, rather than staying a
mockup. Three real amendments to the document along the way, made
because building the thing surfaced questions the mockup alone hadn't:

**Collapse is for every cell type, not only code-bearing ones.**
`CELL_IDENTITY.md` §4 reasoned that Text/HTML didn't need it, since they
already have a rendered form to shrink to. Fair for HTML, once it
exists — but a long Text cell in *edit* mode has no rendered form to
fall back on, and "shrink this out of the way without deleting it" is
exactly as true for a long note as for a long function. Both cell types
get the triangle now; `cell.collapsed` persists across a reload like any
other cell field.

**A header-end group, with a genuinely new feature in it.** Duplicate —
insert a copy of a cell right after itself, same type and code, no run
history — didn't exist in dewmini at all before this. It's not
optional garnish: without it, `CELL_IDENTITY.md`'s own header-end layout
(Edit, Duplicate, Delete) has a hole in it. `duplicateCell()` follows
`insertCellAt()`'s own shape exactly.

**The collapse triangle is one rotated chevron, not two swapped
triangles.** The mockup used ▾/▸ (`&#9662;`/`&#9656;`) — filled
triangles that, once actually sitting a few pixels above the Run
button's own ▶ in the footer bar, read as confusingly similar glyphs in
the same corner of the cell. A single `›` (`&#8250;`), rotated 90° by
CSS between states rather than swapped for a different character, reads
unambiguously as its own thing.

**Run order resets on any reset, not only a full restart.**
`runCellBatch()`'s `reset: true` path (Run all, Run above) already threw
away the Python namespace via `engine.resetPageState()`; it just never
told the run-line about it. `resetRunSequence()` now runs alongside that
reset too, so every cell's line correctly reads "Not yet run this
session" the moment the namespace is cleared, not only after a full
`restartPython()`.

**Not ported to tutorial or practice pages.** Those still carry 7.109's
narrower slice. The type-colour system needs real content to colour —
tutorials are Python-only today — and the header/footer layout move is
a bigger, separate piece of work on the primary reading surface;
neither was in scope here.

*Cost to change: medium. `createCellElement()` is substantially rewritten
— the header/body/footer split, the collapse mechanism, and the run-line
system are all new structure, not additions to the old one — so a future
change to a cell's anatomy touches one well-organised function rather
than several scattered ones. `lastRunMs` is no longer persisted to
`localStorage` (only `collapsed` is, alongside the existing fields) since
it's meaningless without `ranOrder`, which was never persisted either;
nothing reads the old field back, so no migration was needed.*

**7.111 — The style guide gained a plain-language section, and the four
student-facing surfaces were rewritten to it.**

The contents page, the About page, the topic tree and the 251 glossary
definitions all passed section 4 of `planning/PEDAGOGICAL_STYLE_GUIDE.md`
as it stood — invitational, warm, prose not bullets, no emoji — and were
still hard to read. Section 4 governed *stance*; nothing in it governed
sentence architecture, and section 1 says a reader may be working in a
second language.

Six habits ran through all four surfaces, in the same proportions on each:
a short main clause with an em dash carrying the actual meaning; definitions
written as participles rather than sentences (*"Standing in for a process
that…"*); contrast before definition (*not x but y*, before x was ever
said); metaphor standing in place of the plain statement rather than after
it (*how much skin a solid has*); Irish and British idiom (*already behind
you*, *paging through*, *it earns its keep*); and an aphorism closing
almost every unit.

Measured before and after, on the same extraction: the About page went from
29.7 words per sentence and a 61-word longest sentence to 17.7 and 31
(Flesch–Kincaid 14.1 → 8.2); the contents page 17.7 → 11.5 (FK 9.4 → 6.1);
`topics.yaml`'s topic descriptions 18.7 → 15.8 with the longest sentence
46 → 31 (FK 9.3 → 7.9); the glossary 15.8 → 13.4 with the longest 60 → 45
(FK 8.5 → 7.4). 25 of 81 topic descriptions and 64 of 251 glossary
definitions were rewritten — the ones that breached the new rules, not all
of them, so the diff stays reviewable and the entries that were already
plain keep their wording.

The rule went into section 4 as a subsection rather than a new numbered
section on purpose: `.claude/skills/cell-code-review/` and several planning
documents cite this guide by section number, and renumbering would have
broken every one of those references silently.

*Cost to change: small for the guide, large for the prose. Loosening the
rules is an edit to one file. Reverting the rewrites means putting back
text across `build.py`, `planning/curriculum/topics.yaml` and 30-odd
glossary files, and `tests/test_build.py` asserts on one phrase of the
contents page introduction (`test_the_contents_page_introduces_the_place_instead`)
— which is the check that stops the introduction being deleted rather than
a check on its wording, so update the phrase there rather than working
around it.*

**7.112 — The contents page introduction is one paragraph and six points, in
the order a reader meets them.**

Six paragraphs and 254 words was the wrong shape for the page somebody
lands on. It answered several independent questions in prose — what is a
cell, can I break this, where does my work go, how is the list organised,
where do I start — so a reader arriving with one of them had to read the
rest to find it. Section 4 of the style guide asks for prose over bullets;
that rule is about an *explanation*, where the joins between sentences are
the reasoning. Six separate answers to six separate questions have no
joins to remove, so this is an exception rather than a breach, and it is
noted in `render_index()` and in the stylesheet beside `.dl-intro-points`.

The framing of two of those points was rewritten after the first draft got
it wrong. "We try things before we name them" sold the running-first as
novelty. The point is the sequence: explore a problem, then the general
principle underneath it, then the name — and the name matters because it
is how a student talks to somebody else about what they just did. Section
3 now says that. Likewise the practice point: answers sit below the
problems not as a concession but because the answer was never the thing
worth protecting, and what is being learned is the steps — small first,
then multi-step, then more abstract.

Section 4 also gained the sentence-level rules this exposed: mark a
sequence with *first… then… then*, do not make a reader hold a negative
before there is anything to hold it against, "we" for the learning and
"you" for what is actually theirs, and hedge any claim that is not a real
binary.

*Cost to change: trivial for the wording, small for the shape. The points
live in one list in `render_index()`. Going back to prose means deleting
`.dl-intro-points` from the stylesheet and the exception note from both
comments — do not leave either behind claiming a list that is not there.*

**7.113 — The pill and the run line, ported onto tutorial and practice
pages too.** 7.110 built the numbered pill and the merged run-line in
dewmini and explicitly left tutorial/practice pages on 7.109's narrower
slice. This carries both over: `build.py`'s `render_cell()` now renders
a `.dl-cell-pill` (`Cell N`, a coloured "Python" type badge) and a single
`.dl-cell-runline` span in place of the old bare `.dl-cell-id` text and
the separate `.dl-cell-stats`/`.dl-cell-stale-badge` pair; the run-line
machinery in `assets/tutorial-runtime.js` — `runSequenceCounter`,
`renderCellRunLine()`, `resetRunSequence()`, the live ticker, "Running
next" for a queued batch cell — is a close copy of dewmini's own, adapted
the same way 7.109's staleness code already was: these cells ask their
CodeMirror editor for its code directly rather than comparing against a
mirrored `.content` field.

**The pill's number is static, not live.** dewmini recomputes a cell's
position on every drag, since its cells can be reordered. A tutorial
page's authored cells can't be — `build.py` generates static HTML once,
at build time — so `render_cell()` just takes the cell's fixed 1-based
position as a `number` argument. No drag handle exists here for the same
reason: there is nothing to pick up.

**No new colour token, and no drag/collapse/Duplicate.** The pill's type
badge always reads "Python", coloured with the `--dl-type-python` token
7.110 already defined — every authored cell on a tutorial page is
Python, so there was nothing new to colour. Custom cells (the reader's
own, added on the page) were left out of this port entirely; they keep
their old plain-text `.dl-cell-id` label and no run line, since they're
a separate system from authored cells (`docs/tutorial-runtime-explained.md`)
and the user's own request was scoped to "the pill and run-line design,"
not the fuller anatomy 7.110 also built — collapse and Duplicate stay
dewmini-only for now (7.114 closes that gap). One thing not left for
later: there is no header→footer move to make here at all — `build.py`'s
`render_cell()` had its `.dl-cell-bar` below the editor and output
already, before dewmini had one; 7.110 was the side that needed to move
to match this one, not the other way around.

*Cost to change: small. Both files' run-line functions name what they
were ported from, the same convention 7.109 established; the only real
new surface is `render_cell()`'s `number` parameter, a single call-site
change in `place_blocks()`.*

**7.114 — Collapse and Duplicate, the rest of dewmini's cell anatomy,
ported to tutorial and practice pages.** 7.113 carried over the pill and
run-line and left collapse and Duplicate dewmini-only, since the user's
request that time was scoped narrowly. Asked to keep going and bring
these two the rest of the way, both landed — but Duplicate needed a real
design decision first, not just a port, because of a difference between
the two surfaces this document hadn't had to reckon with yet: every
dewmini cell is the reader's own, so "duplicate" always meant "copy
something I already own." An authored tutorial cell is the opposite —
it's the tutorial's own fixed content, generated once by `build.py` and
never the reader's to change. Two shapes were on the table: leave
Duplicate off authored cells entirely (custom cells, the reader's own,
would still get it), or have it mean something adjacent — a copy that
*becomes* the reader's, dropped in as a new custom cell right after the
original. Chose the second, on request: it keeps the button meaningful
everywhere the pill and run-line already are, and it turns "try it
yourself" into one click on a specific example rather than a scroll down
to a generic "+Code" seam with nothing already in it.

**Duplicate reuses an existing seam rather than building a new one, and
lands right after the cell it copies — not at the end of whatever a
reader has already added there.** `initCustomCellsSection()` already
drops a "+Code / +Text" insertion point immediately after every real
cell (and `mountCustomCellAfter()` gives every custom cell its own
trailing one too) — built for "Try something of your own" placed
anywhere on the page, long before this decision needed it.
`duplicateAsCustomCell(cell, type)` calls the same `insertCustomCell()`
those buttons call, with the originating cell's current code instead of
an empty string. The first version found its insertion point via
`lastDividerFor(cell.id)` — the same helper `addCustomCell()` uses for
"append to the end of the trailing section" — but that finds the *last*
divider under an anchor, so duplicating an authored cell a second time,
after a reader had already added their own cell under the first
duplicate, put the new copy after that reader cell instead of the
tutorial's own. Switched to `cell.element.nextElementSibling`: every
cell this file ever mounts gets its own trailing `.dl-insert` right
there, permanently, so it's a stable handle on "immediately after this
specific cell" regardless of what else has since been added further
down the same chain — matching `planning/CELL_IDENTITY.md` §4's own
wording ("Duplicate inserts a copy of the cell right after itself")
precisely, where the divider-search version only approximated it.
Custom cells got
the button too, once the mechanism no longer specifically assumed
"copying an authored cell" — `cell.type` travels through so a text
cell's own Duplicate stays text. No new markup beyond one more button,
no new mounting logic.

**Collapse applies to every cell with editable content, authored or
custom, python or text** — the same table `planning/CELL_IDENTITY.md`
§4 already settled for dewmini, carried over rather than re-litigated.
Unlike the pill/run-line's `renderCellRunLine()`/`resetRunSequence()`
split, one function, `setCellCollapsed(cell, collapsed)`, now serves
`cells` and `customCells` alike — dewmini's own `setCollapsed()` is a
closure inside `createCellElement()`, one instance per cell, but this
file builds authored and custom cells through two different functions
(`buildCells()`, `mountCustomCellAfter()`) that needed to share the same
behavior, so it reads `cell.collapseBtn`/`contentRegion`/
`collapsedSummary` off whichever cell object it's given rather than
closing over element references of its own.

**A real bug caught by a test, not by inspection: collapse must save
immediately, not on the debounced timer.** The first pass wired the
collapse toggle through `scheduleSave()`/`scheduleCustomSave()` — the
same debounced save every keystroke already goes through — and a new
"collapse survives a reload" e2e test failed: reload beat the 500 ms
timer to the punch, so the very state the test had just set was gone.
dewmini's own `setCollapsed()` never had this problem because it calls
`saveState()` directly, not a scheduled version — a toggle is one
discrete click, not a burst of keystrokes worth coalescing, so nothing
was gained by debouncing it here either. Fixed to call `saveNow()`/
`saveCustomCells()` directly, matching dewmini.

**Corrected while writing this: 7.113's own text overstated what was
left.** It said the header→footer layout move stayed dewmini-only for
tutorial pages, alongside collapse and Duplicate. That was never true —
`build.py`'s `render_cell()` had `.dl-cell-bar` below the editor and
output since before dewmini's own cell existed at all; 7.110 was the
side that had to move to match this one. Fixed in 7.113's own entry
along with `planning/CELL_IDENTITY.md` §7, since both were still on this
same, not-yet-merged branch. (Renumbered from 7.111/7.112 to 7.113/7.114
while merging main: 7.111/7.112 landed there first, for the
plain-language pass, from a branch that split from the same point.)

*Cost to change: small. `setCellCollapsed()` and `duplicateAsCustomCell()`
are each one function, and Duplicate's whole implementation rides on
insertion machinery `initCustomCellsSection()` already had to build for
an unrelated reason. The one thing worth remembering for a future
change: any new way to mutate `cell.collapsed` needs an immediate save
call alongside it, not the debounced one — that mistake is easy to
reintroduce by copying the pattern every other cell mutation in this
file already follows.*

**7.115 — A text cell's chrome finally goes quiet until touched, in
dewmini and on tutorial and practice pages both.** `planning/CELL_IDENTITY.md`
§4 described this from the start — a Text cell renders by default and
hides its own chrome until a reader deliberately touches it, `opacity: 0;
pointer-events: none` rather than `display: none` so a keyboard user
tabbing onto a hidden control still reveals it. 7.110's own text ("built
this way in dewmini") and 7.114's ("the same instinct... has not been
carried over here") both said or implied dewmini already had this. It
never did — no `.dm-cell-text`-specific rule of any kind existed in
`compose/dewmini-style.css` before this entry, checked directly rather
than assumed. The design was real; the claim that it shipped wasn't.
Built now, in both places it was claimed for.

**One rule, no JavaScript, on either side.** `.dm-cell-text:not(:hover):not(:focus-within)`
fades `.dm-cell-head` and `.dm-cell-collapse-col` to `opacity: 0` (the
tutorial side does the same to `.dl-cell-bar`/`.dl-cell-collapse-col`,
its own equivalents); a plain `@media (hover: none)` keeps the chrome on
for a touch device, which has no hover to reveal anything with. No JS
class-toggling needed: a reader focusing the textarea to edit already
makes the whole cell match `:focus-within`, which is exactly when the
chrome should be back. `:not(:hover):not(:focus-within)` on the cell
covers hovering the rendered text itself too, not only the chrome —
reasonable, since a reader's cursor being anywhere in the cell is itself
a sign they're paying it attention.

**Deliberately not changed: the interaction that opens a Text cell for
editing.** The design doc's original mockup describes "a click to reveal
the chrome, a double-click to edit" — but the version that actually
shipped, in both dewmini and tutorial pages, has always used a single
click on the rendered view to start editing directly, with an explicit
Edit/View toggle as the keyboard- and touch-accessible alternative. That
behaviour is established, tested, and outside what was asked here; this
entry only fixes the chrome's own visibility, not the click semantics
the mockup separately described.

*Cost to change: trivial. Pure CSS on both sides, no new class, no new
JS state — a future cell type that also wants this only needs its own
selector added to the same rule.*

**7.116 — HTML, the first of the four new cell types
`planning/CELL_IDENTITY.md` §8 designed, built in dewmini.** `CELL_TYPES`
gains `html`; the insert seam gets a third button; `createCellElement()`
gets a third branch. An HTML cell's source is a CodeMirror editor (the
`@codemirror/lang-html` support 7.115's own groundwork commit added,
finally with a consumer) rather than Text's plain `<textarea>` — real
code deserves real highlighting, and nothing about the Edit/View
mechanism cared which kind of editor sat behind it. Rendering is a
sandboxed `<iframe sandbox="allow-scripts" srcdoc="…">`, `resize:
vertical` rather than measuring the frame's own content height, exactly
as §8 designed it, no `allow-same-origin` — a reader's own HTML, or one
they imported from somewhere else entirely, cannot reach this page's own
window, storage, or DOM, script tag or not.

**Rendering, not source, is the click target — unlike Text.** Text's
`renderEl.addEventListener("click", showEditor)` cannot work for HTML:
a click inside a cross-origin iframe is a click inside a different
document, and it never bubbles out to a listener on this one. The
header's own Edit/View toggle, already revealed by the same
quiet-until-touched hover this entry extends to `.dm-cell-html`, is the
one way in — not a regression from Text's affordance, a genuine
difference in what the two documents can tell each other.

**A real bug, caught by the browser rather than by `node --check`:
`if {} else {} else if {}` is invalid JavaScript, and this file's own
`.js` extension hid it.** The third branch was added after an existing
`if (PYTHON) {…} else {…text…}`, which needed to become `if (PYTHON) {…}
else if (TEXT) {…} else if (HTML) {…}` — an easy mistake, adding an
`else if` after a bare `else` that already closed the chain. `node
--check compose/dewmini.js` reported no error; `dewmini.js` loads in the
browser as an ES module (`<script type="module">`), and copying it to a
`.mjs` extension before checking reproduces the browser's own
`SyntaxError: Unexpected token 'else'` immediately — `node --check` on a
plain `.js` file parses it as a CommonJS script, and that parse did not
catch it here. `node --check` against a temporary `.mjs` copy (or
`--input-type=module`) is the check that actually matches how this file
runs, for `dewmini.js` and `tutorial-runtime.js` alike, and is worth
reaching for on every future change to either.

**Another real bug, caught by a browser-driven e2e test, not by
inspection: `readCells()`'s own type whitelist would have silently
dropped every saved HTML cell on reload.** `.filter((c) => c && c.id &&
[CELL_TYPES.PYTHON, CELL_TYPES.TEXT].includes(c.type))` — a deliberate
defense against a stray bad value crashing the notebook, written when
only two types existed and never revisited when a third arrived. Fixed
to `Object.values(CELL_TYPES).includes(c.type)`, so it stays correct the
next time a type gets added rather than needing another manual edit
found only by testing reload.

**A genuine test-tooling wrinkle, not a product bug: hovering a cell's
own geometric centre is not a reliable way to trigger CSS `:hover` when
that centre sits inside a sandboxed iframe.** `elementFromPoint` at that
coordinate correctly returns the iframe — the point genuinely is inside
the cell's box — but under Playwright's CDP-driven synthetic mouse
input, the outer document's `:hover` state did not consistently follow
the cursor across that particular boundary, confirmed by hovering the
same coordinate with a raw `page.mouse.move()` in an interactive
Chromium session both with and without success across repeated runs. A
real user's mouse does not appear to have this problem; the test suite's
own `hover_cell()` helper now moves to a point inside the cell's header
row instead, above where an HTML cell's iframe sits, which is reliable
for every cell type.

*Cost to change: small. `createCellElement()`'s HTML branch mirrors
Text's shape closely enough that a future CSS type (§8's next type in
line) should be a similarly small addition, not a redesign. The
`if`/`else if` chain bug is exactly the kind of mistake worth a linter
catching automatically rather than relying on remembering to check
against `.mjs`; not set up here, left as a known gap.*

**7.117 — CSS, the second of the four new cell types, built in dewmini.**
Close to a copy of 7.116's HTML branch — CodeMirror with
`@codemirror/lang-css`, a sandboxed `<iframe sandbox="allow-scripts">`
for the preview, the same Edit/View toggle, the same quiet-until-touched
chrome — with two differences, both settled in `planning/CELL_IDENTITY.md`
§8 before this was built: the iframe's `srcdoc` is
`CSS_PREVIEW_MARKUP` (a fixed little "page" — a heading, a paragraph
with a link, a button, a list) with the reader's own rule in a
`<style>` tag ahead of it, not the reader's own markup; and styling the
HTML cell sitting above it was considered and set aside, since that
would make a CSS cell's behaviour depend on cell order and type in a
way nothing else in dewmini's model does.

**A UX bug caught before it shipped, not after: a brand-new CSS cell
opened with its editor already hidden.** The first pass called
`showRendered()` unconditionally at the end of the branch, reasoning
that a CSS cell's preview "always has something to show, empty rule or
not" — true, but beside the point: every other cell type opens ready to
type, and a fixed preview with nothing to look at yet is worse than an
empty editor waiting for the reader's first keystroke. Fixed to the same
`if (cell.content.trim()) showRendered(); else syncPreviewBtn();` HTML
and Text already use — only a cell restored with existing content opens
straight to its preview.

The `READ_NOT_RUN_TYPES` set (`text`, `html`, `css`) replaced the
`cell.type === CELL_TYPES.TEXT || cell.type === CELL_TYPES.HTML` check
7.116 left behind — a third `||` clause for CSS would have worked, but
the set reads as what it actually means ("the types meant to be read,
not run") rather than an accumulating list of exceptions, and a fourth
type (JavaScript, which *does* run) won't need touching it at all. The
quiet-until-touched CSS rule got the same treatment, `:is(.dm-cell-text,
.dm-cell-html, .dm-cell-css)` in place of three separate comma-joined
selector lists.

*Cost to change: small, and getting smaller — CSS took noticeably less
new code than HTML did, most of it copied and adapted rather than
designed from scratch, which is roughly what §8's own build order bet
on. SQL and JavaScript won't get to make the same bet: both need a
genuinely new execution engine, not another coat of the same pattern.*

**7.118 — SQL, the third of the four new cell types, built in dewmini —
on Python's own `sqlite3`, not the *sql.js* engine `planning/
CELL_IDENTITY.md` §8 had specified.** That plan (SQLite compiled to
WebAssembly, a second interpreter alongside Pyodide) was where
implementation started — `sql.js` pinned in `vendor-src/package.json`,
`build-vendor.mjs` copying its WASM into `assets/vendor/`, the
groundwork any of §8's other three types didn't need. It was set aside
mid-build on a direct question: is a second engine actually the better
choice here, or just the first one that came to mind? The honest answer
was the latter. dewmini already runs a real Python interpreter, and
Python already ships `sqlite3` — unvendored as an ordinary loadable
Pyodide package as of Pyodide 0.28, not bundled into core, and already
in `compose/dewmini.js`'s `DM_PACKAGES` from `run_query()`'s own earlier
work (7.78). Two engines booting in the same tab would have meant two
data models with nothing bridging them — a SQL cell's own table
invisible to a pandas DataFrame, unless something translated between
them by hand. One engine, with the `db` global sqlite3 already gives it
for free, means a SQL cell's `CREATE TABLE` is a table a Python cell can
already read with `pd.read_sql("select * from t", db)`, no plumbing of
its own — friendlier for a student who has never opened a terminal, and
genuinely interoperable with the pandas/numpy tooling every other cell
already uses, rather than a second island next to it. Every sql.js file
change was reverted before anything was committed (`git checkout --` on
`vendor-src/package.json`/`build-vendor.mjs`/`package-lock.json`,
`rm -rf assets/vendor/sqljs`) — cheap, since it was caught before
`npm run build` even ran once against it.

**What actually got built.** `assets/tutorial_tools.py` gained
`_run_sql_cell(conn, script, max_rows=20)` — internal, not in
`__all__`, sitting right after `run_query()` (7.78) as its multi-
statement counterpart: `run_query()` runs exactly one query and is meant
to be called by name from a tutorial's own Python; `_run_sql_cell()` is
what a generated wrapper line reaches, never something a reader is
expected to type themselves. It splits a script on a bare `;` (a plain
split, not a real parser — a semicolon inside a string literal would
split somewhere it shouldn't, good enough for what a teaching notebook's
SQL cell needs), runs every statement but the last with `conn.execute()`,
and only renders the *last* statement's own result: a table via the same
`_table_html()` a Python DataFrame already renders through, if it has
columns; otherwise `cursor.rowcount` as "N rows affected" — the SQL
equivalent of a Python statement that prints nothing. Every statement
commits at the end, the same friendlier-than-raw-sqlite3 default
`run_query()` already chose. Six new tests in `tests/test_tutorial_tools.py`
(`TestRunSqlCell`) cover the split, the two render paths, state
persisting across separate calls on the same connection, and a bad
statement raising rather than rendering nothing.

`compose/dewmini.js` gained `CELL_TYPES.SQL`, an insert-divider button
and icon, a pill label and colour (`--dl-type-sql`, already defined
7.117 in preparation), and a `createCellElement()` branch — but unlike
HTML/CSS, a SQL cell's branch is Python-shaped: a bare CodeMirror editor
(`language: "sql"`, `@codemirror/lang-sql` — syntax highlighting only,
no Jedi-style semantic tooling, same as HTML/CSS's editors), no Edit/
View toggle, no quiet-until-touched. `READ_NOT_RUN_TYPES` (7.117) stayed
untouched — SQL was never a candidate for it — and gained a sibling,
`RUNS_AGAINST_SESSION` (`python`, `sql`), which replaced every
`cell.type === CELL_TYPES.PYTHON` check that actually meant "cells that
run against the shared session": the footer/footbar build, `isStale()`,
`resetCellOutput()`, `clearAllOutputs()`, `runCell()`'s own guard, and
the "Run all"/"Run above"/"Run below" filters. A SQL cell's raw content
is never handed to Pyodide as Python source — `executeCell()`'s new
`buildSqlCellCode()` wraps it into one generated line,
`tutorial_tools._run_sql_cell(db, <script>)`, with the script embedded
as a `JSON.stringify()`-encoded string literal rather than a hand-rolled
triple-quoted one (JSON's escaping — `\"`, `\\`, `\n`, control
characters as `\u00XX` — is a strict subset of what a Python
double-quoted literal accepts, so this is safe for any SQL text a reader
could type, including one containing its own quotes or backslashes,
where a raw triple-quoted string would simply break). The call is
assigned (`_ = tutorial_tools._run_sql_cell(...)`) rather than left as
the cell's own last expression on purpose: `_run_sql_cell()` already
renders its result directly into the cell's output, and the normal
auto-display of a cell's last value would otherwise render the same
table a second time underneath it.

**`db` itself: a fresh, in-memory `sqlite3.connect(":memory:")`
connection**, created once at boot and again on every reset, dewmini-
only per the scoping this whole phase of work was given. `assets/
pyodide-engine.js`'s `RESEED_GLOBALS_SOURCE` (the main-thread fallback
path, `bootMainThread()`/`resetPageStateMT()`) got it directly, closing
any previous connection first rather than leaving it to garbage
collection.

**The bug this caught before it shipped: that edit alone would have done
nothing for almost every reader.** `assets/pyodide-engine.js` is
dewmini's own file, but the path most sessions actually take is not its
main-thread fallback — it is `assets/pyodide-worker.js`, a Worker file
genuinely *shared* with the hosted tutorial pages
(`assets/tutorial-runtime.js` boots through the exact same file). That
worker carries its own separate copy of `RESEED_GLOBALS_SOURCE` (a
Worker cannot reach a JS constant defined in a different file's module
scope), which the first pass of this work never touched — meaning `db`
would have existed only on the rare main-thread fallback (no Worker
support, or no cross-origin isolation) and been silently absent
everywhere else, including this environment's own Playwright
verification, had that verification not caught it. The fix keeps the
worker file "purely additive" for dewmini the same way its filesystem-
mounting section already is (its own comment: "dewmini only … Tutorial
pages never send these message types, so this section is purely
additive"): `pyodide-worker.js` gained its own
`SEED_DEWMINI_DB_SOURCE` and a module-level `seedDewminiDb` flag, read
once from the boot message (`msg.seedDb`) and reused on every
`reset-page-state`; `assets/pyodide-engine.js`'s `bootWorker()` is the
only caller that ever sets `seedDb: true`, so a tutorial page's own boot
message — which never sets it — leaves the flag false and `db` never
created there.

**Verified in a real browser, not just unit tests**, since the whole
point of the Python/sqlite3 design was interoperability between a SQL
cell and a Python cell, which no Python-only test could actually prove.
This environment had no route to the sqlite3 wheel's usual home
(`cdn.jsdelivr.net`, blocked by egress policy) but did have one to
`github.com`'s own release assets, so the wheel came from Pyodide's own
GitHub release tarball instead, extracted without downloading the full
~350 MB archive to disk. Playwright against a locally staged build
confirmed: a multi-statement script (`CREATE TABLE` / `INSERT` /
`SELECT`) renders only the final `SELECT`'s table, with no duplicate
render; a non-`SELECT` script reports rows affected; a Python cell
reading `db` via `pd.read_sql()` after a SQL cell ran sees exactly what
that cell wrote; output and cell type both survive a reload without
re-running; Duplicate/Delete/collapse all work; and — the one that would
have been silent otherwise — the worker-mode `db` wiring actually took
effect, not only the main-thread fallback. `dev/fetch_pyodide.py`'s own
`BASELINE` gained `sqlite3` too, so the e2e suite's self-hosted Pyodide
(`dev/pyodide/`, gitignored, fetched fresh by anyone who needs it) keeps
having it without a special case; the seven new e2e tests in
`tests/e2e/test_dewmini_workbench.py` run against that same local
Pyodide, no CDN required.

*Cost to change: the redirect away from sql.js cost nothing already
spent (caught before a single build ran against it), and the corrected
design turned out to need noticeably less new surface than HTML did —
no new engine, no new sandboxing model, mostly a generated string and a
`Set` membership change threaded through code that already existed.
JavaScript is what's left, and it does not get this same discount: a
persistent sandboxed session is a real second runtime, the one thing
SQL turned out not to need after all.*

**7.119 — JavaScript, the fourth and last of the four new cell types,
built in dewmini — and a redeclaration bug in its own design doc, caught
by actually running the code rather than by reasoning about it.** A new
file, `compose/js-cell-engine.js`, plays the same role for a JS cell that
`assets/pyodide-engine.js` plays for Python: one persistent session the
whole notebook shares, created lazily on first run. Unlike Python's, it
needs no Worker and no interpreter download — a sandboxed `<iframe
sandbox="allow-scripts">` with no `allow-same-origin` (the same isolation
HTML's own preview iframe already uses, planning/CELL_IDENTITY.md §8) is
already a separate, memory-isolated realm, and every browser already has
a JS engine sitting inside it. What Python's Worker buys — a genuine Stop
button, via a shared interrupt buffer — has no equivalent here: this
iframe still runs on the tab's own main thread, so `canStop()` is always
false, the same limitation Pyodide's own main-thread fallback already
has.

**The bug, and how it was found.** `planning/CELL_IDENTITY.md` §8's own
first draft of this design said a cell's code gets "posted into that
iframe and evaluated there" — read as "inserted as a `<script>` tag,"
the obvious way to run arbitrary JS text. Implementation started that
way. It was wrong: a `<script>` tag's own top-level `let`/`const`
declarations join the realm's *one, permanent* global lexical
environment, and re-running the exact same declaration a second time —
which is to say, re-running an edited cell, an entirely ordinary
notebook action — throws `SyntaxError: Identifier 'x' has already been
declared`. This was not caught by reading the design or the code; it was
caught by actually re-running a `let`-declaring cell in a real browser
during this build's own verification pass and watching it break. No
amount of re-reading the plan would have surfaced it, because the plan
itself was the thing that was wrong — the same lesson 7.96/7.97 already
drew about defects only a browser can catch, applied here to a design
document's own assumption rather than to an implementation bug.

**The fix: indirect `eval` in place of a `<script>` tag.** `(0,
eval)(code)`, called from the iframe's own top level. Per spec, indirect
eval's top-level `let`/`const` bindings live in a scope private to that
one call, not the realm's shared global environment — so a cell can
always be re-run safely, at the cost of those bindings no longer being
visible to a *later* cell. Only `var` and `function` declarations still
persist across cells, since indirect eval attaches those to the real
global object exactly like a `<script>` tag would. This is a real,
user-visible gap from what §8 originally promised ("a `var`/function/
`const` declared in one cell is still there for a later one to read") —
worth naming honestly rather than quietly narrowing the design doc's own
wording to match what shipped. A proper fix (parsing each cell to hoist
its own top-level `let`/`const` onto the shared session by hand) would
need an actual JS parser vendored in for it, out of scope here the same
way SQL's own multi-statement split is a plain string split rather than
a real SQL parser. Documented in three places a reader could reasonably
look: `planning/CELL_IDENTITY.md` §8 itself, `compose/js-cell-engine.js`'s
own file banner, and dewmini's own help panel (`compose/dewmini.html`) —
plainly, without naming `let`/`const` by their JS jargon, since a reader
who has never met either term still deserves to know a cell can always
be safely re-run.

Indirect eval turned out to simplify the error path too, not only fix the
redeclaration bug: a synchronous error is now caught directly around the
`eval()` call itself (a plain `try`/`catch`), which is what answers the
run's own `ok` — no `window.onerror` handler needed, unlike the
`<script>`-tag design this replaced would have required. An unhandled
promise rejection (async work a cell scheduled but didn't itself catch)
still needs `window.addEventListener("unhandledrejection", …)`, since it
can only fire after the triggering `eval()` call already returned; it
still reports into the cell's output, just too late to change the `ok`
that run already recorded. Top-level `await` stays unsupported for the
same underlying reason: wrapping a cell's code in an `async` function to
permit it would swallow its own top-level `var`/`function` declarations
into that function's scope instead of the global one — trading away the
one persistence guarantee this design does keep.

**Everything else in dewmini.js's own wiring.** `CELL_TYPES.JAVASCRIPT`,
Python-shaped chrome via `RUNS_AGAINST_SESSION` (now three members, not
two), an insert-divider button and a code-braces icon, a CodeMirror
editor (`language: "javascript"`, already vendored — no new build-time
work). `console.log`'s arguments are serialised inside the iframe's own
runtime script the way `tutorial_tools.py` already serialises a Python
`print()`'s (a string passes through as-is; everything else gets a short
`JSON.stringify` rendering rather than `"[object Object]"`), and both
that and a reported error `postMessage` back to the parent as `stream`/
`append` events — the exact same event shape Python/SQL output already
produces. Rather than duplicating the ~25 lines that turn those events
into real DOM (`applyOutputEvent()`, previously private to
`assets/pyodide-engine.js`), that function was exported and reused
directly: both engines run in the same JS realm as `compose/dewmini.js`
itself (no Worker boundary between them), and both are configured with
the same cellId → output-element lookup anyway, so there was no reason
for a second copy of "how does a cell's output area get updated" to
exist.

Because `executeCell()` now dispatches to two genuinely different
engines rather than one, several functions that used to read
`engine.canStop()`/call `engine.requestInterrupt()` unconditionally now
go through `canStopFor(cell)`/`requestInterruptFor(cell)` instead —
small, mechanical, and covered by the same reasoning `RUNS_AGAINST_SESSION`
already established: one Set membership check, not scattered
special-casing, wherever "which engine does this cell actually run
against" matters. `runCellBatch()` (behind "Run all"/"Run above"/"Run
below") no longer boots Pyodide unconditionally before the whole batch
either — each cell's own session is ensured right before its own turn,
so a batch of JavaScript cells alone never pays to download Python at
all; a `reset` batch ("Run all"/"Run above") still tears the JS session
down too (`jsEngine.restart()`, no cheaper reset exists for it, alongside
`engine.resetPageState()`), for the same "what's on screen matches what
the code actually did" reason Python's own reset already exists.

**Verified in a real browser**, the same discipline that caught the
redeclaration bug in the first place: creating a cell, running it,
re-running an unmodified `let`-declaring cell without error,
`var`-declared state surviving into a later cell, an uncaught error
rendering with `dm-error`, Restart Python genuinely tearing the session
down (confirmed by checking a previously-`var`-declared name reads back
`undefined` afterward, not by trusting that `restart()` was called), and
a mixed Python+JavaScript "Run all" running both. Nine new e2e tests in
`tests/e2e/test_dewmini_workbench.py` cover the same ground, including
the exact re-run-a-`let`-cell scenario that caught the bug, so it can't
silently come back.

*Cost to change: real, unlike SQL's — a persistent sandboxed session
plus its own message protocol is genuinely new surface, not a generated
string handed to an engine dewmini already had. The redeclaration bug is
the clearest evidence yet, across all four of these new cell types, for
why "verify in a real browser" is not optional the moment a genuinely
new execution model is involved: every earlier catch this document
records of the same shape (7.96, 7.97, this one) was invisible from the
code and the design doc alike, and visible immediately the moment the
feature actually ran.*

**7.120 — HTML and CSS, retired as separate types and merged into one:
Web.** Not a bug fix the way 7.118's and 7.119's own mid-build design
corrections were — HTML and CSS worked exactly as designed, each on its
own. The merge came from actually using both once they existed: a CSS
cell could only ever style `CSS_PREVIEW_MARKUP`, a fixed sample page
that was never the reader's own markup, and an HTML cell had no CSS of
its own reachable at all — the pairing planning/CELL_IDENTITY.md §8's
own CSS design explicitly declined to guess at ("CSS styling an HTML
cell right above it… would make a CSS cell's behaviour depend on cell
order and type"), because that reasoning assumed two separate cells
where "which HTML is this CSS for" has no clean answer. One cell with
both halves removes the question rather than answering it differently.

**What changed.** `CELL_TYPES.HTML`/`CELL_TYPES.CSS` are gone;
`CELL_TYPES.WEB` replaces both. A cell object gains a second content
field, `style` (CSS), alongside the `content` field every type already
had (now HTML, for a web cell) — the first time any dewmini cell has
needed two independent source fields rather than one, which touched
more of `compose/dewmini.js` than the type's own `createCellElement()`
branch: `insertCellAt()`/`addCell()`/`duplicateCell()` all needed to
carry the second field through, `saveState()`/`readCells()` needed to
persist and restore it, and a new `destroyCellEditors(cell)` helper
replaced six separate `cell.editor?.destroy()` call sites so a web
cell's *second* CodeMirror instance (`cell.cssEditor`) stops leaking
too, not only its first.

**The cell itself: two editors, always both visible, one Render
button.** Neither editor swaps out for a rendered view the way HTML's
and CSS's own Edit/View toggle used to — both stay editable at once, so
`READ_NOT_RUN_TYPES` (compose/dewmini.js) narrowed to Text alone, the
only type left with an actual toggle. Rendering is the header's own
explicit Render button instead of either editor's own `focusout`: two
editors both auto-rendering on blur, the way HTML and CSS separately
did, would have fired the same preview update twice for one edit, and
shown a half-finished render mid-tab between the two. An empty HTML
half still falls back to `CSS_PREVIEW_MARKUP`, so the old standalone-CSS
use case — style a fixed little page, no markup of the reader's own
needed — still works exactly as it did.

**Migration: each old cell becomes its own new web cell, never merged
with a neighbour.** A notebook saved under the two-type model still
loads — `readCells()` runs every stored cell through a new
`migrateLegacyCellType()` first, mapping a standalone `type: "html"`
cell to a web cell with an empty CSS half, and a standalone `type:
"css"` cell to one with an empty HTML half. Deliberately not smarter
than that: guessing that an HTML cell and the CSS cell sitting next to
it were meant as a pair is exactly the ambiguity the new design exists
to no longer need, and a wrong guess would silently combine two things
a reader may not have intended combined. Two old cells just become two
new ones, each exactly where it already was — a reader who did mean
them as a pair can copy one CSS rule into the other cell's own CSS half
by hand, which costs one paste, not a filesystem-scale migration risk.

**Export paths that would have silently dropped the CSS half.**
`downloadAsPython()`, `downloadAsIpynb()`, and the standalone HTML
export's own generic non-Python rendering all used to read only
`cell.content` for every non-Python type — harmless before, since an
old CSS cell's *entire* content was `cell.content`, but a real,
silent data-loss bug for a web cell's separate `style` field if left
unchanged. A new `cellExportContent(cell)` helper folds a non-empty CSS
half into the exported text (wrapped in a `<style>` tag, clearly
labelled) for all three call sites, so a reader downloading a notebook
never loses the CSS half of a cell they can still see on screen.

**Verified in a real browser**: both editors visible and independently
editable with no toggle; a script inside the rendered iframe still
cannot reach the parent page (the sandboxing itself untouched by the
merge); a CSS rule now genuinely styling the *same* cell's own HTML,
not a fixed sample; the CSS-only fallback still rendering
`CSS_PREVIEW_MARKUP`; Render staying inert until clicked, confirming
no accidental auto-render survived the rewrite; reload persistence for
both halves at once; collapse/duplicate; and the migration path itself,
seeding raw `type: "html"`/`type: "css"` localStorage data and
confirming it becomes two independent web cells on load. Ten e2e tests
replace the eleven the two old types had (net one fewer, covering more:
the old suites never had a test proving CSS could style a cell's own
HTML, because until this change it never could).

*Cost to change: smaller than either SQL's or JavaScript's — no new
engine, no new sandboxing model, the same iframe HTML already used with
a second editor and one field threaded through the cell data model. The
real cost was breadth, not depth: six call sites for editor teardown,
three export paths, a data migration, and every doc/design surface that
named "HTML" and "CSS" as two things rather than one — more files
touched than either of the two harder builds that came before it, for a
change with no new runtime behaviour to speak of beyond the merge
itself.*

**7.121 — Site: an .html file opens as a small website, on the same
mounted filesystem — and a first design for it, built and then thrown
away before it was ever committed, because `main` had moved underneath
it.** The question 7.116–7.120 raised on the way past: dewmini can now
run HTML, CSS and JavaScript separately (the Web and JavaScript cell
types); the obvious follow-on is showing them together the way a real
static site actually is — three real files, not three cells.

A first version was built directly on this branch's own base
(`57c6604`): a fixed `site/index.html`/`style.css`/`script.js`, a
bespoke Workbench section of its own with its own load/save/debounce
plumbing, and the three files hidden inside their own `site/` subfolder
so Files' flat list (`DECISIONS_LOG.md` 7.88) would not show them
directly. Before it was committed, `origin/main` was checked against —
prompted directly, not discovered — and had moved three commits past
this branch's base while this and the Web-cell merge were being built:
`290829c` (a notebook shown as one Python file, `VIEWS.FILE`), `574d5c3`
(Files becomes a real file manager — `openWorkspaceFile`, a debounced
`writeNotebookToWorkspace`, rename, "New file…"), and `3325694`
(Workbench moved to the left rail, Library to the right). Rebasing onto
it produced real textual conflicts in `compose/dewmini.js`, `dewmini.html`
and `dewmini-style.css` — not just adjacency, competing edits to the same
functions (`runCellBatch`, `executeCell`'s post-run cleanup, the ipynb/
percent-text export helpers) — resolved by hand, kept whichever side had
since become the more complete version of each (main's dropped-output
save mechanism, this branch's per-engine `ensureSessionFor`/`canStopFor`
dispatch) rather than picking one side wholesale.

**Why the first version was abandoned rather than merged forward.**
`574d5c3` already builds almost exactly the mechanism a bespoke Site
panel was reinventing in miniature: open a workspace file into a tab,
edit it, debounce a write back to the real mounted filesystem, redraw
the file list without a race. Building Site as its own section, with its
own copy of that plumbing, made sense only while Files could not open
anything — the moment it can, a second "open, edit, save" path next to
it is duplication, not a feature. The `site/` subfolder-hiding trick
existed only to keep those three files out of a Files list that could not
do anything with them anyway; once Files can open an `.html` directly,
hiding it from that same list stops making sense.

**What shipped instead: a third tab kind, not a fourth panel.**
`VIEWS` gains `SITE` alongside `CELLS` and `FILE` — the same enum
`290829c` already introduced, extended rather than duplicated.
`openWorkspaceFile()`'s guard, which used to refuse anything but `.py`/
`.ipynb`, now also accepts `.html`: it reads the file, looks for a
same-base-name `.css` and `.js` beside it (`page.html` pairs with
`page.css`/`page.js` — Josh's own correction to the first design, which
had fixed on three exact names), and opens a tab with no cells at all.
The site's own three files' live text sits directly on the notebook
object (`siteHtml`/`siteCss`/`siteJs`, `siteCssPath`/`siteJsPath`),
persisted through `writeSavedState()`/`loadSavedState()` the same way
`.path` already is for a File-view tab — the same "localStorage is the
fast-path cache, the real file is the debounced write" pattern the rest
of the file manager already uses, not a new one. `writeNotebookToWorkspace()`
gained a Site branch (`writeSiteToWorkspace()`): the HTML file is always
written, since it is the file the tab is; the CSS and JS files are
written only once there is something in them, so a reader who never
touched the CSS pane does not find an empty `page.css` in their
workspace afterward. Neither file needs to exist for the tab to open — a
site with no styling and no script is still a site, and requiring all
three would reintroduce the fixed-files problem the base-name pairing
was meant to solve.

**Split screen, not a Render button.** Editors on one side, a live
sandboxed `<iframe sandbox="allow-scripts">` (no `allow-same-origin`,
the same isolation the Web cell already uses) on the other, updating on
every keystroke across all three panes rather than waiting for an
explicit press. Argued for directly: a Web cell's Render button suits a
notebook cell answering a one-shot question inside a wider document; a
site is what a reader keeps looking at continuously while they build it,
closer to an ordinary code-and-preview IDE than to a cell. `renderCells()`
gained a `VIEWS.SITE` branch (`renderSiteView()`) alongside the existing
`VIEWS.FILE` one; the Cells/File toggle and every Python-notebook-only
toolbar button (`See an example`, `Start with imports`, `Practice`,
`Run all`, `Clear output`, `Clear`) hide themselves for a site tab behind
one shared class, `.dm-cellview-only`, toggled in `updateViewSwitch()` —
none of them mean anything for a tab with no cells.

**One CSS bug worth naming, because it will recur.** The first attempt
at hiding those toolbar groups set their `hidden` attribute and nothing
happened — `.dm-toolbar-group { display: flex; }`, an author-stylesheet
rule, always wins over the browser's own `[hidden] { display: none }`
user-agent rule for the same property, regardless of selector
specificity or source order, because origin (author vs. user-agent)
decides before specificity does. Every other conditionally-hidden
element in `dewmini-style.css` already carries its own explicit
`.foo[hidden] { display: none; }` override for exactly this reason
(`.dm-panel[hidden]`, `.dm-tabs[hidden]`, six others) — `.dm-toolbar-group`
now does too. Caught by the e2e test written for it, not by inspection.

**Verified in a real browser**, not asserted: opening an `.html` from
Files renders a split-screen tab with a live preview of its actual
content; a same-base-name `.css`/`.js` pair opens beside it with the
preview reflecting all three (a JS cell mutating the DOM the HTML half
produced, not just running inertly); a lone `.html` with no siblings
still opens, its CSS/JS panes empty rather than erroring; typing in any
of the three panes updates the preview without a separate press; the CSS
and JS halves each write back to their own real file, readable from a
Python cell in another tab; the toolbar's cell-only controls hide for a
site tab and reappear switching back to a notebook tab; and a site tab
survives a full page reload. Seven new e2e tests in
`tests/e2e/test_dewmini_workbench.py` cover this ground — one of them
(the CSS write-back test) needing a 3-second wait rather than 1.5,
because two debounces still stack before a site's own file is durable on
disk: `scheduleWorkspaceWrite()`'s 600ms, then `dewmini-fs.js`'s own
internal sync debounce on top of that — the same discovery the abandoned
first design made about its own, differently-shaped debounce stack,
carried forward rather than rediscovered.

*Cost to change: mostly absorbed by `574d5c3` already having built the
file-open/write-back mechanism this reuses rather than reinvents — the
net new surface is `VIEWS.SITE` itself, the sibling-discovery logic, and
`renderSiteView()`'s split layout. The real cost was the false start:
a working, tested implementation built and then discarded whole, because
it was designed against a base three commits behind the one it needed
to ship against. The lesson worth keeping is not "check `main` before
building" in the abstract — that was already the working assumption —
it is that a design decision made while a *sibling* branch is still
landing large, overlapping surface area (the same `compose/dewmini.js`
regions, in this case) has a short shelf life, and is worth holding
loosely until both have actually met.*

**7.122 — Five smaller things, from actually using what 7.116–7.121
built: a cell-type toggle, a real notebook location, two layout bugs,
and one CSS trap caught twice in one session.** Not one build — a run
of small, direct fixes and one real feature, each found by looking at
what had just shipped rather than by planning ahead.

**Web and SQL cells default off, behind a per-type Settings toggle.**
Four cell types shipped in 7.116–7.120; not every reader wants all four
offered on every seam. Settings gains "Cell types": Web and SQL start
off, JavaScript starts on, Python and Text carry no toggle at all —
they are the notebook, not an extra. `enabledCellTypes`, read once at
boot and on every toggle click, gates which buttons
`createInsertDivider()` builds; nothing about a cell already in the
notebook changes when its type is later turned off — it still shows,
still runs, still exports, since the toggle only answers "what can be
added next," never "what already exists." The existing e2e suite
assumed all types were always offered, so the shared `dewmini` fixture
now seeds Web and SQL on before the rest of the suite loads — the
default-off behaviour, and the toggle itself, get their own tests
against a page that fixture never touches.

**A notebook now shows up in Files, without writing it to disk.**
Raised directly: a file a cell's own code writes already appears in
Files, but the notebook holding that cell had nowhere it showed up at
all — not even the default one, on a first-ever visit. The tempting fix
— write every notebook out as a real `.py` on the mounted filesystem —
has a real cost this repository has already ruled against once: mounting
that filesystem means booting Pyodide, and doing that on every page
load, before a reader has touched Python, is exactly what
`planning/DEWMINI_WORKBENCH.md` §1's "nothing opens on a first visit"
rule exists to prevent. `renderNotebookList()` instead lists every open
notebook with no `.path` directly in the Files panel, labelled as living
in this browser rather than as a file, switching to it on click — no
filesystem read, so it draws instantly regardless of whether Python has
ever booted, piggybacked on `renderTabs()` so it can never drift out of
sync with what is actually open. A notebook already backed by a real
file (opened `.py`/`.ipynb`/`.html` from Files) is left out of this list
on purpose — it already appears in the ordinary file list under its own
name, and listing it twice would be the same notebook claiming two
homes.

**Two layout bugs, both found by looking at a screenshot rather than
by reading the CSS.** Library and Workbench opened 3rem wider than
Settings by default (`.dm-panel`'s `min(24rem, 100vw)` against
`.dl-settings`' own `min(21rem, 100vw)` in the shared
`tutorial-style.css`) — fixed on dewmini's own side, matching `.dm-panel`
down to 21rem, rather than touching the shared rule and every tutorial
page's own Settings width along with it. And the per-cell "⋯" run
menu, right-anchored and growing left with no notion of the viewport's
own edge, could run itself off-screen once the button sat close enough
to it — increasingly reachable now that Workbench docks left (7.99).
`openMenu()` now measures its own `getBoundingClientRect()` after
becoming visible and flips to a left-anchored class when it would
overflow, rather than trying to predict in advance when that will
happen.

**The same CSS trap, twice.** The Site tab's own note picked up
`.dm-fileview-note`'s `flex: 1 1 20rem` by reusing that class outright
— a rule written for a *row* flex parent (`.dm-fileview-head`) that,
inside the Site tab's *column* flex wrapper, flex-grew the note to
absorb the entire column's spare height instead, leaving a sentence of
text sitting in a box hundreds of pixels tall. Given its own class,
`.dm-siteview-note`, with the same look and none of that. And
`.dm-toolbar-group`'s own `display: flex` was found, separately, to
silently beat the browser's `[hidden] { display: none }` rule for the
cell-type toggle's Settings groups — an author stylesheet always wins
over the user-agent one for the same property regardless of specificity
or order — fixed the same way every other conditionally-hidden element
in this file already is, with its own explicit `[hidden]` override.
Two different symptoms, the same one-line category of CSS mistake,
caught by a test in one case and a screenshot in the other — neither
readable from the rule that caused it.

*Cost to change: each of these was small in isolation and none touched
architecture — the toggle reuses `renderCells()`'s existing render
path, the notebook list reuses `renderTabs()`'s existing trigger points,
and both layout fixes are one CSS rule apiece. What is worth keeping is
the pattern behind all five: every one of them was found by using the
feature that had just shipped, in a real browser, rather than by
re-reading the code that built it — the same lesson 7.96, 7.97 and
7.119 already drew about defects invisible from the source and visible
immediately once a reader (or a screenshot) actually meets them.*

**7.123 — Two accessible reading fonts, and a High contrast switch that
is its own toggle rather than a sixth font choice.** Josh's own framing
settled the shape before any code did: "high contrast means font and
colours as a toggle" — one switch changing two things together, not a
new entry in the Font row asking a reader to somehow pick "high
contrast" as if it were a typeface. The two fonts (Atkinson Hyperlegible,
from the Braille Institute of America, and OpenDyslexic) sit in the Font
row as two ordinary choices; High contrast is a second, independent
row that forces both a black-on-white (or white-on-black in dark theme)
palette and Atkinson Hyperlegible specifically, regardless of whichever
of the five fonts a reader separately picked — legibility and contrast
are two different questions from "which typeface", and bundling all
three into one six-wide button group would have answered none of them
cleanly.

**Self-hosted, not a Google Fonts `<link>`.** The same reasoning KaTeX's
own fonts already settled here: this is exactly the offline bundle
(`write_dewmini_bundle()`, `DECISIONS_LOG.md` 7.92) a CDN link would
leave broken, and this sandbox's own network policy blocks
`fonts.googleapis.com` outright — confirmed with a direct `curl`, not
assumed. `npm`'s own registry was reachable where the CDN was not, so
both fonts come from `@fontsource/atkinson-hyperlegible` and
`@fontsource/opendyslexic` (SIL OFL 1.1, same license family as most of
the web's open fonts), vendored through `vendor-src/build-vendor.mjs`
exactly like every other pinned asset in that directory — four faces
each (regular/bold × roman/italic), the minimum for a page's own bold or
italic markdown to render as a real face rather than a synthetic one.
The woff2 files land flat in `vendor/fonts/`, beside KaTeX's own, rather
than in a subfolder of their own — a deliberate choice, once it became
clear `build.py`'s `standalone_html()` already has a `FONT_URL_RE`-based
inlining step for KaTeX's fonts (folding them into the single-file
tutorial download as base64 data) that a flat layout could reuse
unchanged rather than needing a second copy of the same regex.

**Shared with every tutorial page, not dewmini-only.** `data-font`/
`data-contrast` and the CSS behind them live in `tutorial-style.css`
and `tutorial-runtime.js` — the same reading-preference system every
dewlab page already shares (`TEXTURE_DEFAULTS`, `applyTexture()`) — so
the two new fonts and the contrast switch had to go in `assets/shell.html`
(the tutorial pages' own Settings markup) as well as
`compose/dewmini.html`, and `build.py` gained an
`{{ACCESSIBLE_FONTS_CSS_URL}}` template token linked from every one of
its six page-writing functions. **dewmini.js duplicates this whole
mechanism rather than importing it** (documented already, in the
duplicated code's own comment) — the first attempt at wiring the
contrast toggle only touched the shared `tutorial-runtime.js` copy and
did nothing in a real dewmini page, caught by watching `--dl-fg`/
`--dl-bg` stay unchanged after clicking the toggle in a real browser
rather than by re-reading the (correct) shared-file change and assuming
it was enough.

**One real test broken by a real behaviour change, both times fixed by
narrowing what the test actually checks rather than by changing the
behaviour.** `test_nothing_is_left_pointing_outside_the_file` failed
outright — an unhandled `<link>` this new stylesheet added, exactly
what that test exists to catch — fixed by giving
`standalone_html()` an `inline_accessible_fonts_css()` alongside
`inline_katex_css()`. `test_a_tutorial_without_maths_does_not_carry_them`
failed more subtly: it asserted no `data:font/woff2;base64,` at all for
a maths-free page, which was true only because KaTeX's own fonts were
the sole source of that marker — now that the accessible fonts are
inlined unconditionally, every standalone page carries some, maths or
not. The fix looks for `.katex-html` specifically (a class only
`katex.min.css` itself defines) rather than the family name `KaTeX_Main`,
which a first attempt reached for and which the very page under test
was already carrying anyway — `tutorial-style.css`'s own `.dl-math`
fallback rule names it, whether or not KaTeX's fonts travelled.

*Cost to change: real but contained. The vendoring step and the two new
CSS rules are genuinely new surface; wiring the toggle itself rode
entirely on a mechanism (`TEXTURE_DEFAULTS`, the generic `.dl-seg`
sync loop) that already existed and needed no change beyond one new
key — the same reason the two new font buttons could share the *same*
`data-texture="font"` group, on a second `.dl-texture-row`, and just
work. The one real trap, and worth remembering past this feature: a
shared mechanism that has been duplicated (dewmini.js's own texture
functions) needs the fix applied twice, and only a real browser catches
the copy that was missed.*
