# Decision log

A record of the choices made while building dewlab that the planning documents
did not settle — and what each would cost to change. An entry marked *trivial*
is an invitation to change it if you disagree; one marked *large* means several
other things rest on it.

`planning/` holds what was decided before any code existed, and nothing here
overrides it. This file records the gaps: places the plan named something
without specifying it, places two settled decisions left a genuine choice, and
places the build met something the plan had not anticipated.

Entries are grouped by build phase and numbered so that code comments and
commit messages can point at them.

---

## Phase 0 — Foundations

### Reconstructing tutorial_tools.py

`planning/DECISIONS.md` commits to six functions — `text_input`, `dropdown`,
`button`, `show`, `show_table` and `check` — pinning down only one signature,
`check(actual, expected)`. Everything else below was designed rather than
looked up.

**0.1 — Widgets return a handle; `.value` reads the live DOM.**
`text_input("Your name")` returns an object whose `.value` reads the input
element live, each time it is asked, rather than a snapshot taken at creation
— otherwise a cell could render a text box but never read what was typed
into it.
*Cost to change: small. One class, and the tutorials that use it.*

**0.2 — Widget values survive a re-run.**
Running a cell clears its output area, destroying its widgets. Values are
remembered per `(cell_id, widget_id)` and restored when the widget is rebuilt,
so a re-run does not erase what a student typed.
*Cost to change: small, but the behaviour without it is bad enough that it
should not change.*

**0.3 — Widget ids: explicit, else derived from the label, else positional.**
`text_input("Your name")` gets the id `your-name-1`; `id="answer"` overrides.
Ids must stay stable across re-runs for 0.2 to work; the positional suffix
keeps two identically-labelled widgets apart.
*Cost to change: small.*

**0.4 — `check` takes two optional extras: `tolerance` and `label`.**
The settled signature `check(actual, expected)` still works unchanged.
`tolerance=` sets a numeric tolerance; `label=` replaces the default "That's
right." with an author-written question. Both default to `None`.
*Cost to change: small — dropping them would not break existing calls.*

**0.5 — `check` compares by meaning, not by `==`.**
Floats compare with `math.isclose`, so `check(0.1 + 0.2, 0.3)` passes. numpy
arrays and pandas objects compare elementwise instead of raising on an
ambiguous truth value. `True` does not equal `1`. Lists report which position
differs.
*Cost to change: moderate. It is the behaviour tutorials will be written
against.*

**0.6 — `button(label, on_click)` calls the function; it does not re-run the cell.**
The callback runs with the cell's output area still current, so anything it
prints or `show`s appends beneath the button, rather than discarding
everything above it by re-running the whole cell.
*Cost to change: small.*

**0.7 — `show(*values, label=None)` mirrors what a cell's last expression does.**
The explicit form of the automatic behaviour, for use mid-cell or when one cell
should show several things.
*Cost to change: small.*

**0.8 — `show_table(frame, max_rows=20, caption=None)` truncates by default.**
A 50,000-row dataset rendered in full produces an unusable page. Truncation is
visible: the note under the table says how many rows there are.
*Cost to change: small.*

**0.9 — `load_csv(name)` added, beyond the six named functions.**
`df = await load_csv("life-expectancy.csv")` wraps the fetch-into-Pyodide-
then-read pattern CONTENT_AND_FILE_ARCHITECTURE.md spells out as boilerplate;
the raw pattern still works, this is a convenience.
*Cost to change: small — it can be dropped without affecting anything else.*

### The execution path

**0.10 — Output rendering rules.**
A cell renders, in order: printed text; anything passed to `show`,
`show_table` or `check`; the value of the last expression; then any
matplotlib figure created but not returned. `None` renders nothing.
DataFrames and Series render as tables, figures as PNGs, everything else as
`repr` — the notebook convention.
*Cost to change: moderate.*

**0.11 — matplotlib is captured as PNG via the AGG backend.**
`MPLBACKEND=AGG` is set before matplotlib can be imported; figures are saved
to an in-memory PNG and embedded as a data URI, rather than using Pyodide's
canvas backend, which draws to a globally-chosen target and fights with
per-cell output areas. PNG also means a figure survives into Phase 2's
`output_html` with no extra work.
*Cost to change: small, and Phase 2 gets easier because of it.*

**0.12 — Cells on one page share one namespace, in document order.**
The notebook model: cell 3 sees what cell 1 defined. This does not extend
across pages — each tutorial page is its own Pyodide instance, so an included
setup cell re-executes on every page load.
*Cost to change: large. Everything else assumes it.*

**0.13 — The whole cell lifecycle lives in Python, not split with JavaScript.**
`tutorial_tools.run_cell(cell_id, output_element, code)` is the single entry
point; the JavaScript runtime boots Pyodide and calls it. Output ordering and
traceback formatting have one implementation rather than two that can
disagree, and the module imports under plain CPython with a recording stub in
place of the DOM, so it is unit-testable without a browser.
*Cost to change: large.*

**0.14 — Tracebacks are trimmed to the student's own frames.**
A `NameError` shows the line they wrote, not dewlab's plumbing. If trimming
would leave nothing, the full traceback is shown instead of an empty one.
*Cost to change: small.*

**0.15 — Printed output is `textContent`, never `innerHTML`.**
A student printing `<b>hi</b>` sees `<b>hi</b>`, and a CSV containing markup
cannot inject anything into the page. Everything that emits markup — tables,
check verdicts, widget labels — escapes its inputs.
*Cost to change: none, it should not change.*

**0.16 — A prose-only tutorial never loads Pyodide.**
A tutorial whose manifest lists no cells skips the Pyodide boot entirely, so a
maths tutorial that is prose and KaTeX costs nothing to open.
*Cost to change: small.*

### Assets and dependencies

**0.17 — Pyodide loads from the CDN by default, through one overridable constant.**
`DEWLAB_PYODIDE_BASE` overrides the default jsdelivr URL — the switch to flip
if a school network blocks the CDN. Self-hosting the runtime plus the three
baseline packages measures **30 MB** (`dev/fetch_pyodide.py` produces exactly
that directory). Not committed either way; default stays CDN.
*Cost to change: one line, plus 30 MB in the repo.*

**0.18 — CodeMirror and KaTeX are vendored, not loaded from a CDN.**
Unlike Pyodide these are small (700 KB together, mostly KaTeX's woff2 fonts)
and CodeMirror 6 is ESM-only, so it needs bundling regardless. Vendoring also
removes two of the three external dependencies a school network could block.
*Cost to change: small.*

**0.19 — The vendor bundle is committed, and built by a separate script.**
`vendor-src/` holds the pins and the esbuild script; `assets/vendor/` holds
the output and is committed, so neither CI nor a local preview needs Node
installed. Re-run `npm run build` in `vendor-src/` when a pin changes.
*Cost to change: small.*

**0.20 — Pyodide 0.28.3.**
Carries numpy 2.2.5, pandas 2.3.1 and matplotlib 3.8.4 as official packages,
so the baseline three load in one `loadPackage` call with no micropip.
Pinned in one constant in `tutorial-runtime.js` and in `dev/fetch_pyodide.py`.
*Cost to change: small, but re-run the e2e tests after.*

**0.21 — A tutorial can widen the package list; the default stays the three.**
The manifest carries a `packages` list defaulting to numpy, pandas and
matplotlib; a tutorial needing more widens its own frontmatter rather than
the baseline everyone pays for.
*Cost to change: none, the mechanism is already there.*

### Layout and files

**0.22 — The shell template lives at `assets/shell.html`.**
Not served to students — `build.py` reads it — but it belongs beside the CSS
and JS it references.
*Cost to change: trivial.*

**0.23 — Cells are carried in one JSON block, not per-cell markup attributes.**
`<script type="application/json" id="dewlab-manifest">` holds every cell's id,
hint and starter code, with `<` escaped so nothing in a cell can close the
script element — rather than Python source living in HTML attributes or
`<textarea>` elements, where escaping problems surface only once a cell prints
an angle bracket.
*Cost to change: moderate — it is the contract between `build.py` and the
runtime.*

**0.24 — `dev/make_harness.py` is Phase 0 scaffolding, replaced by `build.py`.**
It fills the shell's tokens with a fixed set of cells exercising every
rendering branch; the markup it emits is the contract `build.py` must match.
A test fixture, not a preview tool.
*Cost to change: none, it is meant to be thrown away.*

**0.25 — Ctrl/Cmd+Enter runs a cell.**
Not in the plan. The shortcut every notebook user reaches for first, and it
is three lines.
*Cost to change: trivial.*

**0.26 — Each cell has a "reset" button restoring the author's starter code.**
Not in the plan. A student who has edited a cell into an unrecoverable state
otherwise has to reload the page and lose everything else.
*Cost to change: small, but decide it before Phase 2.*

### Repository

**0.27 — dewlab is its own repository. Resolved.**
`planning/REPO_AND_EDITOR.md` specifies a standalone repository publishing to
GitHub Pages, and that is what this is; Phase 0 was moved here with its
history intact once the repository existed. Phase 4 is unblocked: Pages can
be switched on whenever there is something worth publishing.
*Resolved. No remaining cost.*

---

## Open questions this build did not need to answer

Recorded so the next phase does not have to re-derive that they were skipped.

- **OPEN_QUESTIONS.md 32** (school network blocking a CDN) is not resolved,
  but 0.17 makes it a one-line change rather than a redesign, and
  `dev/fetch_pyodide.py` measures the cost at 30 MB.
- **9** (sympy) and **10** (interactive plots) did not come up. 0.21 is the
  mechanism for the first.
- **33** (build-time checks beyond markdown-to-HTML) is Phase 1's question,
  not Phase 0's.
- The **assumed-not-settled** items in DECISIONS.md — scipy staying out, the
  editor previewing through `build.py` rather than a live Pyodide pane, live
  hover documentation deferred — were all built against as written and none
  turned out to be load-bearing for Phase 0.

---

## Phase 0 addenda — found by looking at the rendered page

Three deliberate divergences from what a notebook does.

**0.28 — matplotlib artist reprs are suppressed.**
`plt.plot(...)` returns a list of `Line2D`; `plt.title(...)` returns a `Text`.
A notebook prints those reprs above the figure, which reads as an error to
someone meeting matplotlib for the first time. A cell whose last expression is
an artist renders the figure and nothing else; every other type is unaffected.
*Cost to change: trivial.*

**0.29 — a cell ending in `check(...)` does not print a bare `True`/`False`.**
`check` returns a bool so a cell can branch on it, but ending a cell with a
check is the common shape here, and repeating `False` under a verdict that
already says "Not quite yet" reads as a second, cryptic failure. Suppressed
only when the check's verdict is the last thing rendered and the value is
that same result; any other bool renders normally.
*Cost to change: trivial.*

**0.30 — figures are saved transparent, with one theme-neutral ink.**
Figures are saved with `transparent=True` so the page background shows
through, rather than matplotlib's white default sitting in a bright box on a
dark page. Chrome — title, axis labels, ticks, spines, legend text — is drawn
in a single grey (`#7a7a7a`), holding about 4.15:1 contrast against both
light and dark backgrounds; painting it in the theme's own foreground was
rejected, since a PNG baked at render time would turn near-invisible on the
next theme switch. Plotted data keeps whatever colours the student's code
chose.
*Cost to change: small.*

---

## Phase 1 — Build script v1

**1.1 — `build.py` depends on Python-Markdown and PyYAML.**
DECISIONS.md names markdown-it plus markdown-it-texmath (JavaScript) as the
reference toolchain; `build.py` is Python. The converter is Python-Markdown
with the `extra`, `sane_lists` and `toc` extensions, frontmatter parsed by
PyYAML — both pure Python, build-time only, pinned loosely in
`requirements-build.txt`. This loses the texmath half of that toolchain; see
1.5.
*Cost to change: moderate. Swapping the converter means re-checking the prose
output, not rewriting the cell or link handling, which do not go through it.*

**1.2 — `exec` fences are lifted out before markdown conversion, not after.**
Each fence is replaced by an HTML comment placeholder, the remaining prose
goes through the converter, and the cell markup is substituted back in —
rather than handing `python exec` to the markdown library as an info string.
A cell's Python is never seen by the markdown parser, so nothing in it can be
reinterpreted as markup.
*Cost to change: large. It is the shape of the whole converter.*

**1.3 — Built pages mirror the source tree: `site/tutorials/<module>/<slug>.html`.**
Mirroring `tutorials/<module>/` rather than flattening keeps the built tree
legible against the source, and a new module folder needs no build change.
Cross-tutorial links are computed with `os.path.relpath`, so a link between
two tutorials in the same module is a bare filename rather than a walk up to
the site root and back down.
*Cost to change: small, but Phase 3's navigation and Phase 4's Pages deploy
will both assume this layout once written.*

**1.4 — A dead cross-link fails the build; a missing `alt` fails it too.**
A warning in a CI log is a warning nobody reads, so both are errors: an
`<img>` with no `alt` attribute stops the build, while an explicit `alt=""`
passes, marking a decorative image. Anchors are checked as well as slugs, and
a cell id counts as an anchor.
*Cost to change: trivial to downgrade to warnings, and a bad idea.*

**1.5 — Math is not rendered yet, and nothing in Phase 1 touches `$`.**
DECISIONS.md settles KaTeX rendered at build time, but `assets/vendor/`
carries KaTeX's CSS with no KaTeX JavaScript, so the converter leaves `$…$`
alone as literal text rather than guessing at a mechanism.
*Cost to change: none yet — this is deferred, not decided.*

**1.6 — CI runs the unit tests and a full build; the e2e suite stays manual.**
`.github/workflows/tests.yml` runs the unit modules and then
`build.py --clean`, so a broken build fails the PR even if unit tests pass.
The e2e suite needs a 30 MB Pyodide download and a browser, not worth paying
on every push before Phase 4 exists.
*Cost to change: small — the e2e job is a handful of lines whenever it earns
its place.*

**1.7 — The two `pytest.importorskip` calls became per-class `skipif` marks.**
Both sat at module level in `tests/test_tutorial_tools.py`, so a machine
without pandas skipped the entire file — indistinguishable from a pass at a
glance. The guards now sit on the two classes that need the libraries: 49
tests run and 12 skip visibly where pandas and numpy are absent.
*Cost to change: none, it should not change.*

**1.8 — Maths renders in the browser, from marked spans, with KaTeX vendored.**
This reverses 1.5's build-time plan: the parsing-cost argument for build-time
rendering was judged not worth avoiding, and 0.19's reasoning for vendoring
rules out calling Node from `build.py` instead. KaTeX is bundled into
`assets/vendor/katex.bundle.js` (266 KB) and imported dynamically, only on
pages the manifest flags as containing maths.

`build.py` still finds the maths, lifting `$…$` and `$$…$$` out before the
markdown converter runs (otherwise `$a_i + b_j$` comes back with subscripts
turned into emphasis) and emitting a `<span class="dl-math">` holding the
source TeX — the render input, and the fallback if KaTeX never loads. KaTeX's
auto-render contrib script is unused, since the build already marks every
maths span.
*Cost to change: moderate. Moving to build-time rendering later means a Node
step in `build.py` and in CI, and nothing else — the marking is already done.*

**1.9 — Illustrative code is highlighted by a read-only CodeMirror, not a second
highlighter.**
Pygments at build time was rejected: it would mean a second syntax theme to
keep in step with the CodeMirror pair the texture panel already switches, and
the two would drift. The same `createReadOnlyCode` view is used instead,
sharing its theme compartment with live cells. `build.py` emits
`<pre class="dl-static" data-lang="…"><code>` with the source escaped inside;
the runtime upgrades that in place, readable with JavaScript off and
highlighted with it on.
*Cost to change: small.*

**1.10 — Pages and Actions confirmed; the build stays Python for now.**
GitHub Pages with an automated build on push is confirmed, per
`planning/REPO_AND_EDITOR.md`. Wanting a local preview does not force a
JavaScript rewrite: `python3 build.py` plus a static server is a local
preview today, on any machine with Python. A preview *inside* a browser-based
editor, or on a machine with no Python at all, is a Phase 4 question, left
open deliberately so nothing built in between assumes an answer.
*Cost to change: rises with everything built on `build.py`. Decide before the
editor is built.*

**1.11 — `dev/from_notebook.py` converts notebooks; three things it drops on purpose.**
The first series is converted from eighteen Jupyter notebooks. Three decisions
worth stating:

*Saved outputs are dropped* — dewlab re-runs everything in the reader's
browser, so a stored output is redundant at best.

*Magics and shell escapes are dropped, and reported* — `%matplotlib inline`
is unnecessary and `!pip install …` cannot work; keeping either would produce
a cell that fails on first run, so both are dropped and named in the
conversion report.

*Cell ids come from the section heading, not from position* — ids are what
saved progress matches on, and a positional id rebinds a student's work to
the wrong cell the first time one is inserted above it.

`SOLUTION_` variants are not converted, since `check()` makes them redundant.
*Cost to change: small. The conversion is a one-off — after it, the markdown is
the source and the script has done its job.*

**1.12 — A list written tight against a paragraph is given its blank line.**
This converter does not allow a list to start immediately after a paragraph
with no blank line; left alone it quietly runs the items into the paragraph
with no error or warning. `build.py` now inserts the blank line automatically
rather than leaving the trap open, since a line beginning with a bullet under
a sentence ending in a colon is unambiguously a list.
*Cost to change: small, and the tests pin the edge cases — a hyphenated
sentence, a dash inside a fence, a list that already had its blank line.*

## Phase 2 — Saved work

**2.1 — Autosave is silent; the restore is not.**
VERSIONING_AND_PROGRESS.md makes autosave the primary mechanism, so a student
never has to think about saving. The moment they do need to — coming back to
a tutorial that changed underneath them — has to announce itself: work is
restored either way, and the notice is visible, dismissable, and never blocks
the page. It says up to three things: that the tutorial was updated, that
some saved cells no longer exist, and that a cell with a widget or button
needs running again, since the live Python object behind a restored widget
does not come back.
*Cost to change: small.*

**2.2 — A saved cell with nowhere to go is reported, not discarded.**
Restore matches on cell id, so reordering or inserting a cell is harmless.
Deleting one is not: whatever the student wrote there has no home, and they
should be told it is gone rather than quietly losing it.
*Cost to change: trivial.*

**2.3 — Saved output is written back as markup, and that is safe here.**
Restoring writes stored HTML back into the output area. Safe because
everything that lands there was already escaped on the way in (0.15), the
record never leaves the student's own browser, and the only person who can
write to it is the person reading it.
*Cost to change: it should not change while the record stays device-local. If
progress ever syncs between machines, this needs revisiting first.*

**2.4 — Export is a file the student can keep; import replaces what is there.**
Import overwrites rather than merging: merging two versions of a student's own
work raises questions neither they nor the tool can answer, and export exists
to carry work between machines, not combine it.
*Cost to change: small, but merging is a design problem rather than an
implementation one.*

## Phase 4 addendum — the downloadable copy

**4.1 — One source, two outputs; the export is built, not duplicated.**
`build.py` writes both the page and its downloadable twin from the same
markdown in the same run, rather than hand-maintaining a separate HTML copy —
which would put every tutorial in two places and go stale the first time
somebody is in a hurry. Editing a tutorial regenerates both together; neither
can drift from the other since neither is written by hand.
*Cost to change: small. The export is a transformation of the built page, so it
follows the page rather than needing to be kept level with it.*

**4.2 — The export is one file that still needs the internet once.**
A page opened from a file cannot load an ES module, fetch a neighbouring
file, or resolve a link to a page not beside it. So the export inlines the
stylesheet, editor, maths renderer and fonts, and the Python tools; loads
Pyodide via its classic script rather than as a module; and drops navigation
rather than shipping links that would break. It does not inline Python
itself — 30 MB, unwieldy for the common case of a connection on first open.
With no connection, the runtime says so plainly: reading works, and one line
explains why the cells do not.
*Cost to change: moderate. Inlining Python is a size decision, not a redesign.*

**4.3 — The classic bundle is committed, and CI checks it is not stale.**
`assets/vendor/standalone.bundle.js` is the whole runtime rebuilt in the
older script format, committed so `build.py` needs no Node. Unlike the rest
of `vendor/` it depends on `assets/tutorial-runtime.js` rather than a pinned
version, so it goes stale whenever the runtime changes. CI rebuilds it and
fails if the committed copy differs.
*Cost to change: small, but do not remove the check without replacing it.*

**4.4 — A whole series downloads as one archive, built from the same files.**
`site/download/<series>.zip` gathers each series for a teacher setting up a
room, rather than making them click through eighteen pages. The archive holds
the same files the per-tutorial links point at — copied, not regenerated — so
nothing else can go stale. A build without the downloadable copies writes no
archive and shows no link.
*Cost to change: small. It is a dozen lines around the files that already
exist.*

**5.1 — One Settings menu, not a row of small buttons.**
One **Settings** button now opens one panel with three sections — your work,
this tutorial, texture — replacing three separate controls in two places
("progress", "texture", and download in the navigation row for lack of
anywhere else). A student who finds Settings once has found all of it. The
panel closes on Escape and on a click outside.
*Cost to change: small. It is one panel and one controller.*

**5.2 — The masthead follows the reader down the page.**
The masthead is sticky, so the way to the contents and to Settings is not a
scroll to one end of a long page. Everything that has to clear it measures
from `--dl-header-h` rather than guessing: the status line, the settings
panel, an anchored jump. The masthead's parts are sized in rem and do not
follow the reader's text size, so that one number holds at every width.
*Cost to change: small, but change the variable rather than the three places
that read it.*

**5.3 — The navigation row is a grid, and the phone gets its own shape.**
Previous / contents / next is a three-column grid rather than a flex row, so
the contents link stays centred whether or not the outer two links exist, and
each title wraps inside its own column. Under 34rem the grid becomes previous
and next side by side with contents beneath, and the module name gives up its
space to the Settings button.
*Cost to change: small.*

**5.4 — `plt.show()` renders the figure instead of warning about a canvas.**
Under the non-interactive backend dewlab uses, matplotlib's own `show()` has
nothing to draw on and warns — indistinguishable, to someone meeting
matplotlib for the first time, from having done something wrong under a plot
that rendered fine. dewlab's replacement renders the open figures at the
point of the call instead, installed lazily since pyplot may not be imported
yet, with a warning filter covering the one cell that calls `show()` before
that lands.
*Cost to change: small, but any change should keep both halves — the
replacement and the filter behind it.*

**5.5 — The chapter navigation sticks with the masthead, as one group.**
The previous/next row sticks together with the masthead as one group rather
than a second sticky element, since everything below has to clear whatever is
up there. That combined height is not constant — it depends on how far the
neighbouring titles wrap — so the runtime measures it into `--dl-chrome-h`
and remeasures on resize.
*Cost to change: small, but the measured variable is load-bearing for three
other rules.*

**5.6 — A minimal header, chosen rather than imposed.**
**Header: full or minimal** lives in Settings, rather than dropping things
automatically at narrow widths. Minimal tightens the masthead and truncates
the neighbouring titles to one line each — a reading-comfort preference like
text size, living beside it. Nothing is removed; every link still reaches the
same place.
*Cost to change: small.*

**5.7 — Every page carries its own contents list, built from its headings.**
Generated from the same heading tree that gives the headings their ids, so it
cannot disagree with the anchors it links to. Closed by default. A page with
fewer than two sections gets no list, and a sub-heading whose text repeats
within the tutorial is left out of the listing, though its anchor still
works.
*Cost to change: small.*

**5.8 — Line width has three presets and a slider, not one or the other.**
The slider alone gave no idea what a good value was; presets alone would take
away a control some readers had already set. Narrow, medium and wide write to
the same number the slider does, and a value between presets leaves none of
the three pressed.
*Cost to change: small.*

**5.9 — The contents page opens with a map, not just a list.**
A numbered list cannot show the shape of the material — that four tutorials
cover programming before any mathematics, or that Tutorial 17 leans on five
earlier ones. Inline SVG generated by `build.py`, not a diagramming library:
the layout is a few dozen lines of arithmetic. Nodes are grouped into the
strand a tutorial mostly covers, read optionally from
`planning/curriculum/outcomes.yaml`, so the site still builds without it.
Reading-order arrows are solid and dark, an instruction to the reader;
"builds on" arrows are dashed and faint, a fact about the material found by
reading each tutorial for the earlier ones it names.
*Cost to change: moderate. The layout arithmetic is the part to be careful
with.*

**5.10 — The map is not bound by the reading measure.**
A diagram reads worse squeezed to prose width, so the figure centres on the
column and takes up to 58rem, scrolling inside its own box on a narrow
screen. The page still never scrolls sideways.
*Cost to change: small.*

**5.11 — The curriculum map asks the tutorials about their own vocabulary.**
It reuses the existing convention of single-asterisk emphasis for a term
being introduced — evidence of what an author considered new, not a list to
maintain. Two checks follow: a term emphasised in two tutorials is being
introduced twice or means two things, and the tool cannot tell which; a term
used before the tutorial that explains it appears was used as though the
reader already knew it. Neither is a verdict.
*Cost to change: small. The stress-word list is the only hand-maintained part,
and a wrong entry there costs a little noise, not a wrong answer.*

**5.12 — Asset URLs carry a content hash.**
Every asset URL ends in a short hash of that file's contents, hashed per file
rather than one version for the lot, so editing the stylesheet does not also
force a fresh download of the maths bundle — this is what stops a browser
serving a stale cached asset against a newly built page. `tutorial_tools.py`
is not named in the markup and so cannot be busted this way; its version
travels in the manifest instead. `vendor/katex.bundle.js` is deliberately left
unversioned, since the standalone export can only bundle that import into one
file if the specifier is a plain string.
*Cost to change: small. But removing it brings the cache-staleness bug back
invisibly.*

**5.13 — The standalone export fails loudly when a substitution finds nothing.**
The export works by replacing markup this same file wrote moments earlier.
Every replacement now raises if it finds nothing, naming what it could not
find, rather than letting `str.replace` no-op silently.
*Cost to change: small, and it is the guard that made 5.12 safe.*

**6.1 — The map became a topic tree, on its own page.**
A full-page diagram of all 67 outcomes, laid out left to right by prerequisite
order and grouped top to bottom by subject, replacing the tutorial map's
cramped spot above the contents list and shifting the subject from tutorials
to topics. Drag to pan, scroll to zoom, choose a topic to read it; no library
— the layout is computed in `build.py` and arrives as data.
*Cost to change: moderate. The layout arithmetic and the pan/zoom clamping are
the parts to be careful with.*

**6.2 — The tutorial map moved rather than being deleted.**
It shows something the topic tree does not: which tutorials lean on which,
found by reading each tutorial for the earlier ones it names. That evidence
exists nowhere else, so it sits under the tree on the same page rather than
being replaced by it.
*Cost to change: small.*

**6.3 — Light and dark cost nothing because the tree uses the same shell.**
Built on the shell every tutorial uses, it inherits the masthead, the
settings panel, the theme tokens and the reader's saved preferences — "works
in dark mode" was a consequence of not building a second thing, not a feature
to build.
*Cost to change: small, but building it standalone would have cost far more.*

**6.4 — The contents page introduces rather than illustrates.**
With the map gone it says what dewlab is to somebody who has just arrived —
nothing to install, nothing to break, work saved in this browser — and then
gets out of the way of the list they came for.
*Cost to change: small.*

**7.1 — Reading order lives in one file per series, not in every tutorial.**
`order: 12` in each tutorial's frontmatter meant inserting one tutorial in the
middle was an edit to every file after it. `<series>.order.yaml` — a list of
slugs — replaces it: moving a tutorial moves a line, inserting one adds a line.

The build fails if a tutorial is missing from the file, if a slug in the file
has no tutorial, or if a tutorial still carries `order:` in its frontmatter.
This keeps the editor small (it edits one list) and optional, since the list
can be reordered by hand.
*Cost to change: moderate, and it should not change again.*

**7.2 — The numbers are gone from titles, slugs and prose.**
"Tutorial 14: Expressions Come Alive" is now "Expressions Come Alive", at
`expressions-come-alive.html`, with prose references using the name rather
than the number. Published URLs changed as a result.

Nothing carries a position except the order file, so inserting a tutorial
anywhere is now free.
*Cost to change: high — putting them back would be as much work again.*

**7.3 — A slug is unique within its module, not across the site.**
A built path already carries the module, so there is no real ambiguity in two
modules sharing a slug — only a global uniqueness check that would force names
around a constraint that does not exist.

`tutorial:slug` links look in the linking tutorial's own module first, fall
back to another module when exactly one has that slug, and stop the build when
more than one does.
*Cost to change: small.*

**7.4 — "Builds on" is found by title now.**
The map's dashed arrows used to match "Tutorial 11" in the prose; with numbers
gone they match titles instead — what a tutorial would naturally write anyway,
and it found the same seven references.
*Cost to change: small.*

**7.5 — A downloadable copy lives under its module, like its page.**
Scoping slugs to the module (7.3) left the flat `site/download/` folder keyed
by slug alone: two modules sharing `first-steps` meant one silently overwrote
the other. Caught by the 4.3 publish guard on main.

Copies now sit under `download/<module>/`, with four tests covering the
crossing (each checked to fail against the unfixed build).
*Cost to change: small, and the guard is what makes it safe.*

**7.6 — Dependencies answer "can I start this now?", not "what comes next?".**
The topic tree built topic by topic asks "what does this one obviously need?",
which produces edges that are individually reasonable and collectively
arbitrary. The real intent is reachability — letting students explore freely,
find where they need more practice, and letting instructors plan module
coverage — and a reachability map wants as few edges as it can honestly get
away with, since every edge closes a door.

Three candidate trees are recorded in `planning/curriculum/DEPENDENCIES.md`,
with the places they disagree left visible. Tree C — five gateway topics with
everything else hanging off one — shipped. It added one edge rather than
removing seven from the prior version, and moved longest path from 6 to 5
while opening one more topic from a standing start.
*Cost to change: small. It is one `needs:` list per topic in `topics.yaml`.*

**7.7 — Discover first, name afterwards.**
Concepts are discovered through concrete reasoning before formal terminology
is introduced, and this determines dependency direction: divide and conquer no
longer precedes searching and sorting, since binary search is the reason to
care about it, so it now comes after. Substitution comes before the chain rule
for the same reason, and because it is algebra students have already
practiced.
*Cost to change: small, and reversible per topic.*

**7.8 — The tree reads downwards.**
Roots at the top, nothing points upwards. A first attempt kept the old
horizontal, one-column-per-subject layout and measured 5854×756px — wide and
useless on a phone. Subject stopped being an axis and became a colour-coded
sort instead; a tier wider than five topics wraps, subjects stay grouped
within a tier. The tree is now 1058×1768 and fits a phone.

Two bugs fell out of the change: the zoom controls sat inside the pannable
frame and never worked, since any non-topic press started a pan; and the zoom
floor (0.35) was tuned for the old short tree and stopped "fit" from fitting
the new tall one.
*Cost to change: small.*

**7.9 — The tutorials do not name the assessments.**
Prose named specific institutional assessments throughout ("you are now ready
for Skills Demo 1") — thirteen references across nine tutorials — tying the
material to one institution's schedule, the thing most likely to change. Each
was rewritten to say what readiness consists of instead ("you are now ready to
build these tools fresh, from nothing but the ideas").

A test guards against this recurring, since prose written later tends to reach
for whatever surrounds it.

**7.10 — Reflection is its own series, not the last tutorial.**
"Looking Back Before Moving Forward" sat at position eighteen of eighteen,
implying it was an end-of-course task, when it is really something to return
to after finishing anything worth reviewing. It now lives in its own
`Reflections and review` series, with text no longer assuming one specific
handed-in piece of work.

Splitting it surfaced three latent bugs, since no module had ever had two
series before: the contents page headed each series by filename slug rather
than its order-file name; the archive link read "Download all 1 as single
files"; and the curriculum map's sequence graph keyed nodes on `order`, which
restarts at 1 per series, producing two nodes called T1 and a self-loop arrow
(the back-reference finder had the same fault).
*Cost to change: small. Moving it back is a line in each of two order files.*

**7.11 — The editor edits content, and previews structure rather than appearance.**
A full live browser preview of rendered HTML would need a parallel
client-side renderer alongside the Python-Markdown build pipeline, which would
drift from `build.py` and give inaccurate feedback. The editor instead
previews structural validity — runnable cell counts, cell IDs, headings,
build-breaking syntax issues (unclosed fences, missing or duplicate IDs) — and
visual rendering is checked on the built site.
*Cost to change: small. The parser is pure and tested on its own.*

**7.12 — Renaming a cell id destroys saved work, and only the editor can say so.**
A cell's id is the key a student's work is stored under; renaming one orphans
that work rather than moving it, and the build cannot warn about this because
by the time it runs the old id is gone. The editor is the only place both
versions exist at once, so it names the ids that vanished before the commit is
made.
*Cost to change: small, but the warning is the reason the feature is safe.*

**7.13 — Divide and conquer sits beside searching and sorting, not before it.**
Searching and sorting are split into distinct tutorials (`finding-things`,
`putting-things-in-order`), with divide and conquer presented within both —
binary search halving a sorted list, merge sort halving an unsorted one. In
`topics.yaml`, divide and conquer depends on iterating by index, matching
both, with neither configured as the other's prerequisite.
*Cost to change: one line.*

**7.14 — Some things a student needs are nobody's learning outcome.**
Foundational precursors (e.g. categorizing triangles, the Cartesian plane for
the unit circle) are necessary but not enumerated in curriculum descriptors.
Topics may now carry a `PRE-` code meaning **groundwork**: assumed, met in
passing wherever first needed, belonging to no outcome. They show on the map
as groundwork rather than "planned", and carry their own `strand:` rather than
falling into a meaningless "other". The typo guard survives — a `MIT-`/`PDP-`
code must still be a real outcome.
*Cost to change: small. One code prefix and one branch in the state.*

**7.15 — The colours on the tree are explained where they are used.**
Every node carries its subject as a coloured edge, but the only way to learn
what a colour meant was to open a topic and read its panel. A key now sits on
the page, generated from the strands actually present, so it can't list an
unused colour or omit one that's there.
*Cost to change: small.*

**7.16 — The zoom controls are above the tree, not on it.**
They used to float over the canvas, covering whichever topics sat underneath
and stealing their clicks — invisibly, differently at every zoom level,
noticed only when a layout change put a tested node underneath them. The 7.8
guard against the frame stealing presses is removed along with them, since
outside the frame it guards nothing.
*Cost to change: small.*

**7.17 — A tutorial is archived, not deleted.**
Deleting a tutorial's file was the only way to retire it, which would strand
any student's saved work — kept in local storage keyed to a page that no
longer exists, with no way back and no trace. The editor was built with no
delete button for this reason, fixed before the first cohort rather than
after.

`status: archived` in frontmatter keeps the page built and runnable, still
holding saved work, but removes it from the reading order (no previous/next),
the series archive, and lists it under *Archive* on the contents page with a
notice that it's not part of the course. `live` is the default, so nothing
already written needs to say anything; deleting a file is still the right
move for something published in error.
*Cost to change: small.*

**7.18 — An archived tutorial teaches nothing the map can point at.**
A student today cannot be sent to an archived tutorial, so counting it as
coverage would let the map claim an outcome is covered when nothing on the
course covers it — the exact lie the map exists to prevent. Both the topic
tree and `dev/curriculum_map.py` skip archived tutorials when working out
where an outcome is taught. (The alternative reading — coverage means "we have
written this" — would make the map a record of work rather than a guide to
the course.)
*Cost to change: small — two `continue`s.*

**7.19 — Listing an archived tutorial in the order file stops the build.**
A reading order is a route through the course; a retired tutorial is not on
that route, so listing it there is a contradiction the build now catches
rather than leaving the order file to disagree with the site. Archiving the
last tutorial in a series leaves `order:` empty, which is accepted (the series
stops appearing) — `order:` missing entirely is still an error.
*Cost to change: small.*

**7.20 — The version field is a readable date.**
`2026.08.20.1` — year, month, day, and which release of that day — replaces an
integer. The restore comparison stringifies both sides and checks equality,
not ordering, and restore itself matches on cell id, so a string version
works unchanged. It also removes a redundant `released:` field, since
`version:` already carries the date.

Sorting uses the four parsed numbers (`2026.08.20.10` sorts before `.9` as a
string). The label a student reads stays prose ("20 August 2026"), with the
dotted form kept for the file, frontmatter, and URL.
*Cost to change: small while nothing is versioned yet; large once tutorials
carry dated versions and students have saved against them.*

**7.21 — Saved work is keyed on the module and the slug, not the slug alone.**
Since a slug is only unique within its module (7.3), two tutorials sharing a
slug shared one `progressKey()` record, so answers in one overwrote the other.
The manifest now carries the module, and the key is the `(module, slug)` pair
— the same pairing required of built pages and downloadable copies.
*Cost to change: small today, a migration inside every student's browser
after the first class.*

**7.22 — Loading a saved file checks before it overwrites.**
"Load a copy" used to write the JSON it was handed straight into the page's
key and only then discover the cells didn't match — by which point the
student's real work was already gone. The saved record now carries its
module, the exported filename carries the module, and a file from elsewhere
is refused by name with nothing changed. Lenient one way: a record with no
module still loads on a matching slug, so files written before the module was
recorded don't hit a cliff.
*Cost to change: small.*

**7.23 — Four contracts, audited once while changing them was free.**
Before publishing to a live cohort, slugs, cell ids, the save record's shape,
and the version field were audited (`planning/WINDOW_AUDIT.md`). Cell ids
checked out sound — 228 of them, none non-conforming, and the twelve reused
across tutorials are safe because storage is keyed per tutorial. The
version-field restore already compared versions as strings and tolerates the
dotted date.
*Cost to change: this window closes on the day the first class opens the
site.*

**7.24 — A version is a release date, and the newest live one answers the
tutorial's URL.**
`version: 1` became `version: 2026.09.15.1`. One field carries identity,
order, and the date a student reads; a separate `released:` would be a second
copy of the same numbers, and two fields that can disagree are worse than one
that can't.

The unversioned URL serves the newest `live` version, so every link written
before versions existed keeps working and keeps meaning "the current one".
Other versions sit beneath it at `<slug>/v<version>.html`. This one rule also
supports the beta workflow with no extra machinery: freeze the current
release, mark the working copy `beta`, and students keep the frozen live one
until the beta is promoted.
*Cost to change: high now, in the sense that undoing it would be as much
work.*

**7.25 — Status is about the course; default is about the release.**
`status` (`draft`/`beta`/`live`/`archived`) says how a tutorial stands to the
curriculum. Whether a version is the *default* says which release students
get — a superseded release is still `live`, just no longer the default.
Conflating the two during early implementation meant marking a superseded
version `archived`, which wrongly presented it as having left the course
rather than as an older valid release.
*Cost to change: small.*

**7.26 — A draft is the only honest way to have something unpublished.**
The site is static and public — anything built has a URL, and a URL is public
— so "not finished" has exactly two meanings that differ by whether a page
exists. A draft is not built; a beta is built, findable only by link, and
says so unmissably.
*Cost to change: small.*

**7.27 — Setting a status is two files, and that is why it belongs in the editor.**
The frontmatter field alone would be trivial to hand-edit, but only a live
tutorial belongs on the reading order and the build refuses an order file
listing anything else (7.19) — so the frontmatter and the order line have to
move together or the next build stops. The editor does both in one commit,
and its tutorial list shows all four statuses with the current one marked,
rather than only the tutorials still on the reading order.
*Cost to change: small.*

**7.28 — Modules appear in a declared order, not an alphabetical accident.**
The contents page sorted modules by folder name — the same invisible ordering
the series order files (7.1) were introduced to end, surviving one level up.
`tutorials/modules.yaml` now lists module names in display order. Lenient
where the series files are strict: an unlisted module still appears (at the
end) rather than failing the build.
*Cost to change: small.*

**7.29 — Log consolidation and duplicate sequence resolution.**
Entries 7.11–7.15 were reconciled after branch merges; two branches had both
numbered an entry 7.20, so the second was reindexed to 7.28 with citations
kept consistent.
*Cost to change: none.*

**7.30 — The picker tells a reader what will happen instead of warning them.**
Switching tutorial versions now gives exact, checkable counts of which cells
carry over, rather than an ambiguous warning — restore matches on cell id, so
which answers survive a move is knowable in advance. The manifest carries
every release's cell ids, and each option in the list states, e.g.:

> **2 June 2026** — 2 of your 3 answers carry over. 1 cell is not in that
> version, so that answer stays saved but is not shown there.

"Stays saved but is not shown" rather than "will be lost", since the record
is keyed by tutorial, not by release, and the answer reappears on returning to
a version with that cell.
*Cost to change: small. The counts are one function and the ids are one build
step.*

**7.31 — Which release a reader gets is the last one they worked in.**
The build determines what the unversioned URL serves (the newest live
release) for first-time visitors. For returning visitors, the browser
resolves to the version last worked in, unless explicitly chosen otherwise.
The pin is written on selecting a release and again on saving work in one;
working in a release outranks older selections. Where no pin exists, the
saved record's `tutorial-version` is the fallback.
*Cost to change: small. "The version last worked in" guarantees seamless
continuity.*

**7.32 — The marker is conditional rather than invisible, and it is a date.**
Single-release tutorials show no version badge. Tutorials with multiple
releases show a persistent date marker (e.g. "15 September 2026") rather than
a hover tooltip, so touchscreens and mobile keep the indicator.
*Cost to change: none. It is built from the manifest at load.*

**7.33 — A downloaded copy has no version list.**
Only the default release gets a standalone copy, so other releases aren't on
the reader's disk — offering a picker that points at files that don't exist
would be worse than no picker, so the version list is stripped from the
standalone manifest and the runtime removes the section that would have shown
it.
*Cost to change: one line, and a test that fails without it.*

**7.34 — An older release tells search engines which one is current.**
Two releases of a tutorial are near-identical pages at two URLs and would
compete in search results without a `<link rel="canonical">`. Every
non-default page points to the canonical URL; the default itself carries
none, since it is already canonical.
*Cost to change: one line and one shell token.*

**7.35 — The restore notice says what happened instead of guessing.**
When a tutorial has releases, the page names both which release the work was
written in and which one is active. Answers whose cells don't exist in the
current release stay preserved in local storage and restore when a release
containing those cells is opened.
*Cost to change: none.*

**7.36 — Automated curriculum coverage reporting in CURRICULUM_MAP.md.**
Coverage metrics are generated directly by `dev/curriculum_map.py` from
`outcomes.yaml`, `out-of-scope.yaml`, `proposed.yaml`, and tutorial `covers:`
frontmatter. `planning/CURRICULUM_MAP.md` reports outcomes with no proposal,
and `tests/test_curriculum_map.py` asserts a proposal never claims an
already-covered outcome.
*Cost to change: none.*

**7.37 — Coordinate geometry is a tutorial, because Pythagoras is a gateway.**
Outcomes `MIT-4.1`–`MIT-4.4` form their own tutorial, *Straight lines: slope, midpoint and distance*,
between Drawing Functions and Angles and Waves. Pythagoras is one of the topic
tree's six gateways, unlocking seven downstream topics, so it needs a
dedicated tutorial rather than a subsection of graphing — and having one also
means *The unit circle: sine, cosine and tangent* doesn't have to introduce Cartesian coordinates as an
aside.
*Cost to change: none yet.*

**7.38 — Connections between whole things, rather than things merged.**
Venn diagrams (`MIT-2.3`) get a dedicated short tutorial, *Venn diagrams: drawing sets and their overlaps*,
linked to *Logic: truth tables, XOR and De Morgan's laws* and *Sets: building them from sorted lists* — three distinct,
cross-linked modules are easier to discover, sequence, and maintain than one
overloaded composite. Matplotlib draws the diagrams directly from set
operations, framing them as computed output rather than manual notation.
*Cost to change: none.*

**7.39 — Editor path resolution supports versioned folders.**
When a tutorial has multiple releases it lives in a folder of release files
rather than a single `<slug>.md`. The editor's `pathOf` resolves the active
live release (falling back to the newest available), matching `versions_of`
in `build.py`.
*Cost to change: resolved in editor test fixtures.*

**7.40 — The release workflow freezes existing content before publishing edits.**
The editor keeps two copies of every file: the fetched text
(`state.original`) and the working buffer. Releasing freezes `state.original`
as the prior release and publishes the active buffer as the new release, so
students can always return to the exact text of a prior release.
*Cost to change: fundamental release lifecycle guarantee.*

**7.41 — Unified warning for cell ID mutations across edits and releases.**
Renaming a cell ID in an in-place edit orphans saved student progress;
releasing a new version preserves prior cell IDs in the frozen release. The
editor surfaces both outcomes in sequence, guiding authors toward releasing
when structural cell changes occur.
*Cost to change: two sentences in editor UI.*

**7.42 — Plain titles and modular scope grounded in pedagogy.**
Titles use plain language for what the reader builds or explores — "Lines
and Distances" rather than "Coordinate Geometry", "How We Got Here" rather
than "The Computing Time Machine". Tutorial scope follows pedagogical
cohesion rather than a strict 1:1 outcome count: two related outcomes stay
together, a complex outcome with distinct activities splits into separate
modules.
*Cost to change: none.*

**7.43 — Trigonometry partitioned into three focused tutorials.**
*The unit circle: sine, cosine and tangent* (radians, sine/cosine definitions, exact values), *Sine and cosine waves: amplitude, period and shift* (unrolling circular motion into wave functions), and *Solving triangles: the sine rule and the cosine rule* (Sine/Cosine Rules, area, right-triangle applications) — each a
distinct conceptual activity with room for exercises. *Parabolas: completing the square* was split
from *Functions and their graphs* on the same principle.
*Cost to change: none.*

**7.44 — Geometric grounding for exact trigonometric ratios.**
Exact values in surd form (`MIT-4.7`) are taught geometrically on the unit
circle rather than by rote-memorized triangles: surds represent coordinates
derived via Pythagoras on landmark angles. With this, every outcome in the
curriculum descriptors is in scope and mapped to an existing or proposed
tutorial.
*Cost to change: none.*

**7.45 — Practice problem sets and worksheet conversion architecture.**
Practice problem sets derived from worksheets (e.g. `deweydex/Mathematics`)
put answers behind collapsible folds beside each problem, allowing immediate
self-verification while preserving the reflective moment before viewing the
solution.
*Cost to change: free at planning stage.*

**7.46 — Clean exception traceback formatting for syntax errors.**
`_format_exception` trims tracebacks to student execution frames. For
compile-time syntax errors, where no runtime execution frame exists, dewlab
renders the exception's own location directly (filename, line, caret) instead
of exposing internal `tutorial_tools.py` plumbing:

```
  File "<cell your-turn-4>", line 2
    result = (5 + 3
             ^
SyntaxError: '(' was never closed
```

Narrow by design: an exception with no user frames *and* no location of its
own still shows the full traceback, since that signals a bug in dewlab and
hiding our own frames would make it harder to find.
*Cost to change: five lines in runtime tools.*

**7.47 — The first two tutorials to close outcomes since the map existed.**
*How We Got Here* (`PDP-LO1`, `PDP-LO3`) and *When It Goes Wrong* (`PDP-LO9`),
converted from everlearning notebooks, brought outcomes covered from
forty-one to forty-four.

Three things worth recording for the next conversion: the converter
(`dev/from_notebook.py`) is a first draft, not an output — it produced
slugified cell ids and titles that need a human's judgment, so both
tutorials were written by hand from the notebook rather than patched from its
output. Only half of the second notebook came across, since most of it
duplicated testing content *Building Reusable Tools* already covers. And
deliberately broken cells work better here than in a notebook — a cell that
raises its error in front of the reader beats a commented-out example, and is
what turned up 7.46.
*Cost to change: these are tutorials now, so their slugs and cell ids are
contracts from the first class that uses them. The window is still open.*

**7.48 — Every tutorial has a page of problems, and some problems have no
tutorial.**
Fourteen practice pages became thirty-two — one per tutorial except the three
that are already problems or reflection (*Review problems: combining numbers, polynomials and equations*, *Looking
Back Before Moving Forward*, *The Team Project*).

Three sources fed them. `deweydex/Mathematics`'s twenty-six worksheets, twenty
of which carry an in-file answer key (the remaining six have answers only as
PDFs, and cover material not yet taught, so nothing was lost).
`deweydex/everlearning`'s thirty-eight blank programming-problem stubs gave
questions with every answer written fresh. And every tutorial's own
unanswered "your turn" prompts became problems in their own right — the
largest source of the three.
*Cost to change: thirty-two files. The frontmatter contract is one line each.*

**7.49 — `practice_across:` for a set of problems with no single owner.**
Some problems only make sense once several tutorials are behind the reader,
and giving one of them ownership would misstate what the page needs — so a
page may name several tutorials instead of one. Deliberately asymmetric: a
mixed set links to everything it draws on, and nothing links back, since a
tutorial has one companion practice page reachable from its own last
paragraph, and a reader who just finished it shouldn't be sent somewhere
assuming six more. Mixed sets are the only pages nothing else links to, so
they're listed on the contents page under their module, after the series and
before the archive.
*Cost to change: about ninety lines of build.py and fourteen tests. The four
pages using it are content, and would survive a different mechanism.*

**7.50 — Twenty-one numbers in answer keys were wrong before they were run.**
Not a decision, a measurement: among the errors, binary search costing 9
comparisons instead of 8, two roots of an ambiguous triangle, a wrong Heron
semi-perimeter, a standard deviation out by a tenth, a password-cracking time
out by a quarter, and where `2**x` overtakes `x**3`. Every one was plausible
and none would have failed a test, since no test asserts on prose — only
running the arithmetic finds them, and that has to be done deliberately. Two
answers were also written as a wrong attempt followed by its own correction;
straightened, since a student checking their work against a self-contradicting
key learns the page is unreliable.
*Cost to change: nothing. This is a note to the next person writing an
answer.*

**7.51 — Tutorials link back to the mixed sets after all.**
7.49 decided a mixed set links out with nothing linking back; Josh asked for
the reverse, since discoverability was the weaker half of that argument — a
page nothing links to is a page nobody finds, and the contents page isn't
where a reader stands when they finish a tutorial.

A tutorial now shows its own practice page first ("worth doing when you have
finished reading"), then any mixed set naming it, marked "for later, once
more of the course is behind you", followed by the other tutorials it draws
on — so a reader can see at a glance whether it's for them yet.
*Cost to change: about thirty lines of build.py and four tests.*

**7.52 — Two folds, and a build check that a fold names one of them.**
Per Josh's request for hint dropdowns with steps and a follow-up reflection:
`dl-hint` holds numbered steps and closes with a **Think about** and a **Try
this next**; `dl-answer` holds the answer. The hint comes first, in a warmer
colour, so opening it doesn't feel like giving up — and the closing
reflection is what makes it more than a spoiler, teaching the method rather
than just the answer.

`build.py` now fails on any `<details>` whose class is neither `dl-hint` nor
`dl-answer`, since a bare `<details><summary>` renders as an unstyled
browser-default triangle with no visible failure.
*Cost to change: the classes are in the markdown of every practice page. The
check is six lines and five tests.*

**7.53 — Four tutorials re-released, and what the trial found.**
Josh asked for the versioning system (7.20–7.24) to be tried on real content:
*First Steps*, *Number types, powers and logarithms*, *What Are the Chances*, and
*Putting Things in Order* — four diverse subjects, each converted from
notebooks. Each became a folder: a working copy at `2026.08.23.2`, the
previous release frozen at `v2026.08.23.1.md`. Thirty-one tutorials became a
hundred and fifty-two pages.

Three defects turned up, none of which any test would have caught. The
curriculum map read every `.md` under `tutorials/`, so a re-released tutorial
counted twice — fixed with a `newest_live` function matching `build.py`'s own
rule, with five tests, four failing against the old behaviour. Two releases
on the same day showed identical dates in the picker, indistinguishable to a
student choosing between them — fixed by showing the sequence number, only
where needed. And one cell (`explore_number` calling a not-yet-written
`classify_number`) had never worked on a fresh page — it now reports what's
missing instead of raising `NameError`, and the frozen release deliberately
keeps the bug.
*Cost to change: the folder layout is what build.py already expected. Undoing
a release means moving the file back and deleting the frozen copy, and is
free while no class has seen either.*

**7.54 — The first bibliographies.**
Josh's style guide requires one in every tutorial; none had one. Four now do,
four or five entries each, chosen to be worth an hour rather than to fill a
section (Bingmann's sorting visualisation, 3Blue1Brown on logarithms, the
Python docs on floating point, Downey's *Think Python*). Thirty-one to go —
the largest style-work item outstanding, and not mechanical: a bibliography of
plausible-looking links is worse than none, since a student who follows one
dead link stops trusting the rest.
*Cost to change: per tutorial, and each needs a person who knows the
sources.*

**7.55 — 5N0554's thirteen outcomes, and where the examples went.**
Transcribed from the descriptor PDF into `outcomes.yaml`, under a new `CMPS`
module. The descriptor's "e.g." examples (Google PageRank, ASCII art, PKI, …)
are suggested content, not the outcome itself, so measuring coverage against
them would let a tutorial that taught PageRank and nothing else read as
having taught the whole outcome. `outcomes.yaml` keeps the outcome stripped
of its examples; every example moved to that code's `uses:` in
`topics.yaml`.

Two outcomes bundle more than one idea under one descriptor number (LO1
pairs data structures with recursion; several of LO7–LO13 read like a
paragraph). Left as one code each, matching the descriptor's own numbering
rather than inventing sub-codes it doesn't have, since `covers:` answers to
that document.
*Cost to change: two files, twenty-six entries between them. The wording is a
paraphrase, so restating any one entry costs nothing the descriptor would
object to.*

**7.56 — The first 5N0554 strand: six tutorials, and PageRank rides along
rather than getting its own.**
Built as six tutorials in a new `matrices` series under
`computational-methods`: *A Grid of Numbers*, *Multiplying Grids*, *What a
Matrix Does to a Picture*, *Undoing It*, *Solving Systems*, and *Where Chains
Lead* — the last folding weather prediction, convergence, text generation,
and a hand-checkable PageRank example into one tutorial rather than four,
closing the open question `planning/outlines/matrices.md` had left about
where PageRank goes: a three-page link graph solved by the repeated-
multiplication technique already built for weather is three cells, not a
tutorial's worth of new machinery.

Sourced from three worksheets whose answer keys exist only as PDFs (`07a`,
`07b`, `07d`), so every number that reached a tutorial or its practice page
was worked fresh in Python and checked against the worksheet's own claims
where one existed. The Markov word-transition example uses the opening
sentence of Dickens' *A Tale of Two Cities* (public domain, and already used
the same way in `everlearning`).

Closes `CMPS-LO4` in full; touches `CMPS-LO1`'s data-structures half and
`CMPS-LO2`'s randomness half. Nine outcomes (`CMPS-LO3`, `LO5`–`LO13`) remain
untouched.
*Cost to change: six tutorials, six practice pages, one series file. Nothing
downstream depends on this strand yet, so reshaping it costs only the
content.*

**7.57 — What the browser QA pass caught, run before this pushed.**
Every cell of the six new matrices tutorials was run in a real Chromium
against self-hosted Pyodide, with a correct solution injected into every
blank "your turn" cell first — otherwise a `NameError` from an unstarted
exercise tests nothing but the fact the cell is blank. Practice pages needed
no injection, since their runnable cells are all tool cells and worked
solutions live in inert `dl-answer` folds.

Two real bugs turned up, both about what carries over between pages rather
than arithmetic. `Multiplying Grids`'s prose claimed `transpose` was already
defined "from the last tutorial", but each tutorial is its own Pyodide
instance with nothing carried over — fixed with a one-line recap cell rather
than a "your turn", since the point of this tutorial is multiplication. And
in `Undoing It`, the QA script's own harness had overwritten a "your turn"
cell's shipped starter (`import matplotlib.pyplot as plt`), producing a
false-positive `NameError` that was the harness's fault, not the tutorial's —
recorded so a future QA pass checks the starter before assuming a failure is
the tutorial's.
*Cost to change: two lines, once each. The QA script itself is not
committed — it lives in the scratchpad as a tool rather than a test.*

**7.58 — Three wrong citations in the matrices strand's bibliographies,
caught by checking each video id rather than trusting memory.** Every
bibliography entry across the six tutorials was checked against the video id
or paper it links to. Three didn't match: `Multiplying Grids` attributed a
3Blue1Brown video to "Ben Eater and Grant Sanderson (2022)" when it is
Sanderson alone, 2017 (Eater had no part in it). `Solving Systems` labelled a
video "Chapter 9" of *Essence of Linear Algebra* when it is chapter 13
(chapter 9 is a different video entirely). `Where Chains Lead` cited a
3Blue1Brown "Markov Chains (2022)" video whose id doesn't resolve to anything
real — replaced with Josh Starmer's actual StatQuest video on the same topic;
the same tutorial's Page-and-Brin citation also had the authors in the wrong
order, fixed to match the paper.

Every other entry across the six tutorials checked out against a real search.
*Cost to change: four lines, once each. The failure mode this guards against
is a plausible-sounding citation nobody follows — see 7.54 on why a
bibliography of dead or wrong links is worse than none.*

**7.59 — The editor's prose surface is now a Milkdown (Crepe) block editor,
vendored the same way as CodeMirror and KaTeX, with no framework adopted.**
`planning/REPO_AND_EDITOR.md` specified "live, borderless block editing" for
editor v1 from the start; what had actually shipped was a plain
`<textarea>`. Milkdown's Crepe preset was chosen over alternative
React-based block editors (BlockNote, Tiptap, Lexical, Novel.sh) for the one
reason none of those satisfy: its API is plain JavaScript, not React, so no
component framework is needed. Bundled with esbuild in `vendor-src/` into
`assets/vendor/milkdown.bundle.js`, committed like the other two vendored
libraries.

Two undocumented Crepe behaviours were found and fixed: `markdownUpdated`
fires once while still parsing the *starting* document, which without a
guard made opening a tutorial and touching nothing look like an edit (fixed
with a hydration guard); and its code-block feature keeps only the first word
of a fence's info string as its "language", silently round-tripping `python
exec` back out as plain `python` and turning a runnable cell inert on save
(fixed by `restoreExecTag()`, keyed off the same `id:`-first-line convention
`build.py` already uses).
*Cost to change: moderate. Reverting to a `<textarea>` is small but gives up
what this entry exists to close. Swapping to a different block editor later
means re-solving the exec-tag round-trip problem if it has the same
limitation.*

**7.60 — The editor gained code completion and a dead-link check; a hover
docstring in Crepe's own code blocks was attempted and pulled back out.**
Three landed: `problems()` now checks `tutorial:slug#anchor` links against
every other tutorial's real slugs and anchors, closing a gap `build.py`'s own
checks didn't cover; both the editor's code blocks and a student's own cells
gained keyword/builtin and locally-typed-name completion, wired from
CodeMirror's already-vendored autocomplete packages; and a student's cell
additionally gained live completion and a real hover docstring, read directly
off the running interpreter (`tutorial_tools._page_globals`,
`inspect.getdoc()`) — accurate by construction, with nothing bundled to fall
out of date.

The fourth piece — the same hover docstring for `module.name` written in the
*editor's* own code (no live interpreter to read from) — was built from
captured real Pyodide docstrings (`dev/generate_doc_snippets.py`) instead,
for a small, grep-derived set of names the curriculum actually calls. The
CodeMirror wiring compiled and worked for a student's own cells but never
surfaced a tooltip specifically inside Crepe's code-block feature, in either
a real or scripted hover, despite confirming the mouse event reaches the DOM
node. Not chased further; Crepe's code-block feature is evidently doing
something to its hosted CodeMirror instances that plain `autocompletion()`
doesn't run into.
*Cost to change: the three landed pieces, small, each a self-contained static
function plus a documented CodeMirror extension. The fourth: data and
generator are real and committed, unused only because nothing reads them
yet.*

**7.61 — `load()` reads a repository's files in concurrent batches of 16,
not one at a time.**
Against a real 90-file repository under `tutorials/`, an
await-each-request-before-the-next loop took 15-25 seconds before showing a
single tutorial — the editor's own fake-client test suite never caught this
since it resolves instantly with no latency to expose it. Batched at 16
rather than one `Promise.all()`, since GitHub's secondary rate limiting
treats 90 simultaneous requests from one token as closer to abuse than a
person opening a page — 16 is a reasonable middle guess, not a measured
optimum. `TestLoadingManyTutorialsAtOnce` covers both in-order and
out-of-order resolution against a 40-tutorial fake repository.
*Cost to change: trivial — one constant (`READ_CONCURRENCY`). Raising it
trades a faster load for a higher chance of a real rate-limit response;
nothing currently retries or backs off if that happens.*

**7.62 — The editor gained a search-and-insert tutorial link picker, and it
uncovered a real bug in `@milkdown/utils`'s own `insert()` helper.**
A toggle above the prose editor searches every known tutorial by title, slug,
or module (`matchTutorials()`) and inserts a real link at the cursor, so an
author reaches for a tutorial that exists rather than guessing a slug.

The first version used `@milkdown/utils`'s documented `insert(markdown,
true)`, which silently produced a link with no href every time — two
separate bugs. `insert()`'s inline path round-trips content through a real
DOM node, and the commonmark preset's link-mark sanitizer strips `href` for
any scheme outside http/https/mailto/tel/ftp — a real guard against
`javascript:` links, but one that also erases `tutorial:` before the round
trip's second half reads the href back. And building the link mark directly
and calling `replaceSelectionWith(node, true)` still dropped it, since
`inheritMarks: true` *replaces* the node's marks with whatever is active at
the cursor rather than merging, and a cursor at a paragraph's end typically
has none. `insertLink()` now builds the text node and mark straight against
the schema, with no DOM step, and calls `replaceSelectionWith(node, false)`.
*Cost to change: small — `matchTutorials()` is a pure function over
already-computed data; the picker is plain DOM. Worth remembering for
anything else that reaches for `@milkdown/utils`'s `insert()` on a
mark-bearing inline node.*

**7.63 — The slash menu was fully transparent and the text cursor never
appeared, because Crepe's structural stylesheet reads ~25 custom properties
that only one of its own skins defines, and this editor loads neither.**
`milkdown-entry.js` deliberately imports only Crepe's structural CSS, not any
of its skins, since this editor retextures the same elements from dewlab's
own `--dl-*` variables instead. What that missed: the structural stylesheet
has no colours of its own — it reads them from
`--crepe-color-*`/`--crepe-font-*`/`--crepe-shadow-*` custom properties that
only a skin defines. With none loaded, every `var()` reference to an
undefined property resolved to its CSS initial value: the slash menu's
background came out `transparent`, and the replacement text-cursor's border
came out invisible.

A prior patch (7.60) had hand-fixed a few elements' backgrounds directly, but
that override and Crepe's own rule turned out to be equal specificity — not
reliably winning the cascade, confirmed with `getComputedStyle()`. The real
fix defines the ~25 `--crepe-*` custom properties once, mapped to the
matching `--dl-*` token, so every downstream `var()` across Crepe's entire
stylesheet resolves correctly from one place — including elements this pass
never went looking for individually.

Worth remembering: a first attempt at this fix silently did nothing because
the explanatory comment above the new rule contained the literal text `*`
immediately followed by `/`, closing the CSS comment early and turning the
intended comment into parsed (and broken) CSS — a syntax error inside a
comment produces no error anywhere, only a silently different stylesheet.
*Cost to change: the mapping itself is cheap. The real cost is trusting a
browser's cascade or comment parsing by reading the rule, rather than
querying `getComputedStyle()` against a real rendered page.*

**7.64 — The reading page gained a cheat sheet, assembled per tutorial so it
never shows a reader something they have not been taught yet.**
Full design in `planning/CHEAT_SHEETS.md`. A glossary file
(`<slug>.glossary.yaml`) says what one tutorial introduces — a sibling of the
tutorial's `.md`, not frontmatter, so a bad entry fails the build the same
way a bad `covers:` entry does. `cumulative_glossary()` walks a series in
`order.yaml` order, accumulating each member's entries into the next, so a
tutorial's manifest carries its own glossary plus everything before it. A
practice page's cheat sheet is the union of the tutorial(s) it names, through
the same registry lookup `practice_pairs()` already validates.

The panel reuses `.dl-settings`'s floating-card positioning, and the two
close each other on open. The toggle is pinned to the page's top-left
corner, starting `hidden` and revealed only when the manifest's glossary is
non-empty — a tutorial with nothing accumulated yet gets no button at all.

Producing the glossary files is `.claude/skills/tutorial-glossary/SKILL.md`,
run tutorial by tutorial in series order, built on top of the first-use
`*emphasis*` convention `dev/curriculum_map.py` already relies on.
*Cost to change: the schema and accumulation logic, small — one YAML shape,
one pure function per concern, fully covered by unit tests. The real cost is
running the skill across the curriculum, tracked separately.*

**7.65 — Every tutorial in both live modules now has a glossary file, so the
cheat sheet described in 7.64 shows real content everywhere.**
Run series by series in `order.yaml` order across all of
`computational-methods` and `mit-pdp-maths-prog-integration` (33 tutorials
plus two reflections). A handful of tutorials with nothing to add —
`bringing-it-all-together`, `critique-and-reflection`, `the-team-project` —
got an empty `entries: []` with a comment explaining why, distinguishing
"deliberately considered, nothing to add" from "nobody has gotten to this one
yet".

One collision surfaced: *tangent* already named the trig ratio, and
`rates-of-change.md` introduces an unrelated *tangent line* for the
derivative — reusing the string `tangent` would have had
`cumulative_glossary()`'s first-definition-wins dedup silently keep the trig
meaning and drop calculus's. Fixed with the distinct term string "tangent
line" rather than teaching the dedup logic about word senses.

Verified against real builds: every single-target practice page's cheat
sheet matched its tutorial's manifest, and all four `practice_across` mixed
pages matched the union of their targets'.
*Cost to change: none of this changes the mechanism from 7.64 — it is
content, not code.*

**7.66 — A cheat sheet may cross series within a module; it still never
crosses modules.**
Matrices comes after Python fundamentals in `computational-methods`, so a
matrices tutorial's cheat sheet should carry fundamentals' vocabulary too,
rather than stopping at its own series boundary as 7.64 originally shipped.
An optional `tutorials/<module>/series.yaml` (`order:`, a list of series
slugs) says the order a module's series accumulate in; `series_chain()`
walks every tutorial in every series listed before this one, then this
series' own members. `cumulative_glossary()` now walks that chain instead of
one series' member list.

A series left off `series.yaml` (or a module with no such file) keeps 7.64's
original series-only accumulation — which is what leaves
`reflections-and-review`, not on any linear route through its module,
unaffected. `check_series_order()` fails the build if `series.yaml` names a
series that doesn't exist in that module.
*Cost to change: small. `series_chain()` and `check_series_order()` are each
short, pure, and covered by tests. Verified against a real build:
`grid-of-numbers` now carries `working-with-tables`'s 8 fundamentals entries
ahead of its own 11.*

**7.67 — A cell's control bar moved below the editor and output, and its
hint stopped floating.**
Two real usability problems reported against the live site: the bar (slug,
hint, reset, run) sat above the code, so a reader met controls for code they
hadn't read yet; and the hint's "?" opened a `position: absolute` hover
popover that could float over the editor or output beneath it, with no way
for a touch reader to open it at all.

`render_cell()`'s markup order changed — bar now last inside `.dl-cell` —
with no change to how `tutorial-runtime.js` binds to it, since every binding
is a class lookup rather than a DOM-position assumption. The hint became a
real click toggle, `hidden` by default and a plain block when open, growing
the cell and pushing what follows down the page — the same "push down, cover
nothing" shape the prose-level hint/answer fold already had.

A separate ask — turning Run into Stop while a cell runs — was investigated
and not built: Pyodide runs on the page's own main thread with no Web
Worker, so a blocking loop leaves no thread free to handle a click; the real
fix needs a Worker plus `SharedArrayBuffer`, which needs headers GitHub Pages
won't let this project set without a service-worker shim. Raised as its own
open question rather than folded into this change.
*Cost to change: small for what shipped. The Stop button is real
architecture work whenever it happens.*

**7.68 — A new skill reviews a tutorial's own code for naming and comment
quality, the same way `tutorial-glossary` reviews it for vocabulary.**
The style guide's code section (then §5, now `PEDAGOGICAL_STYLE_GUIDE.md#code`) had cell-length, boilerplate, and tool rules
but nothing on variable naming or comment style — a real gap, since
"clearer, semantic variable names" needs somewhere authoritative to check
against. §5 gained rules (semantic names over mathy single letters; comments
that say why, not what; two named exceptions — a formula's own letters
matching the prose above it, and "discover first, name afterwards" applying
to a variable's specificity) before `.claude/skills/cell-code-review/SKILL.md`
was written against them.

The skill treats a rename as whole-tutorial, not per-cell, since cells in
one tutorial share a namespace, and requires validating an edited cell still
compiles and produces the same output before calling a rename done.

Run once by hand across a handful of real tutorials to prove the process.
Most existing code needed nothing; one real change — `undoing-it.md`'s
`polygon_area()` renamed `n` to `point_count`, confirmed identical output
before and after.
*Cost to change: small — the skill is a process document, no code of its
own. Running it across the rest of the curriculum is tracked as a
follow-up.*

**7.69 — The cheat sheet stopped hiding on a phone; it becomes a bottom
sheet instead, the same treatment `.dl-settings` already had.**
The mobile rule used to simply hide `.dl-cheatsheet-toggle`/`.dl-cheatsheet`.
It now gives `.dl-cheatsheet` the same `top: auto; bottom: 0; left/right: 0`
block `.dl-settings` already has, sharing one selector list rather than a
parallel rule. The toggle needed no change, since it was always a small
fixed corner button, not a floating card — it was never what broke on a
phone.
*Cost to change: small — CSS only, no JavaScript or markup changed.*

**7.70 — Two progress indicators, both read from the saved-progress record
`saveNow()` already writes.**
`planning/PROGRESS_INDICATORS.md` designed both; shipped unchanged in shape.
`saveNow()` gained one field per cell (`errored`), captured once rather than
re-parsed from saved HTML wherever needed. `progressCounts()` is the one
shared function turning a list of `{started, errored}` into `{total, done,
errored}`.

**The contents page** gets a small badge (`1/2`, red only if a counted cell
errored) next to a tutorial's title, computed client-side from that
tutorial's own localStorage record, gated by a new Settings toggle since it's
the one *ambient* piece visible on every visit. A tutorial with no saved
record gets no badge — a `0/9` would read as a judgment on a page nobody
opened.

**A tutorial's own page** gets a plain summary line ("4 of 9 cells run · 1
with an error") folded into a Settings "Progress" section rather than a
persistent bar competing with the cheat sheet toggle for screen edge. No
second toggle needed, since this line is only ever seen by a reader who
already opened Settings. `#dl-settings-progress`, unlike `#dl-settings-work`,
is **not** removed on a zero-cell page, since its toggle also governs the
contents page's badges.
*Cost to change: small. Each function is short and pure or near-pure, with
unit and e2e coverage across both a build-time and a real-cell-run path.*

**7.71 — The cell-code-review skill's curriculum pass, finished.**
7.68 proved the process on a handful of tutorials; this is the rest — all of
`computational-methods` and both series of `mit-pdp-maths-prog-integration`
(roughly eighty documents total), batched across several commits with a full
clean build after each.

Three real changes, all renames or comments, none changing what a cell does:
`where-chains-lead.md`'s word-chain loop renamed generic `a, b` to `word,
next_word`, matching the tutorial's own later naming; `inverse(M)`'s `e`
(standing in for the determinant-taken `d`) got a one-line comment
explaining why; and `storing-and-computing.md`'s bare `x, y, z, w` for four
different typed results, contradicting the tutorial's own stated naming
rule, were renamed to `text_value`, `number_value`, `decimal_value`,
`number_as_text`.

Everything else needed nothing — single letters earned their place
constantly (matching a formula or a triangle's own notation, loop indices,
coordinates, the conventional `f, g, h` for "a function"), and two "discover
first" names were confirmed as deliberate rather than flagged. Deliberately
broken cells that are the exercise itself were left alone. One dead
algebraic expression in `parabolas.md` was noticed and deliberately not
touched, since restructuring logic is outside this skill's charter — flagged
as a follow-up instead.
*Cost to change: small, same reasoning as 7.68 — a process applied to
content, not new code.*

**7.72 — Students can write their own notes, distinct from a tutorial's
author-written pedagogical notes, saved on the same record as their cell
work.**
A `notes` field on the record `saveNow()` already writes, a `<textarea>` in
Settings' "Your work" section, riding on the existing export/import button —
no new save path, no new file format.

The one real design change forced by this: `initProgressSection()` and
`saveNow()` used to bail out on zero cells, on the reasoning that a page with
nothing executable has nothing to save. That broke once notes existed — a
prose-only tutorial can still have something worth writing down. Both now
check membership in a small `NON_TUTORIAL_PAGES` set (`index`, `tree`,
`about`) instead.

Only the smaller of the design doc's two nudge proposals shipped: a
first-use hint line under the textarea. The staleness marker on the export
button was left for later (shipped in 7.75).
*Cost to change: small. `saveNow()`/`restoreSaved()` each gained a few lines;
four new e2e tests cover autosave, reload survival, clearing, and export,
plus a separate zero-cell-case test file.*

**7.73 — A left-anchored panel lets a reader jump to any tutorial in the
current series, not just the one immediately before or after it.**
`render_series_nav(tutorial, members)` server-renders an `<ol>` of every
series member in reading order, current one marked (not a link), every
other one a link via the existing `link_between()` helper. A tutorial with
nowhere in a series to sit — archived — gets nothing.

Between the design and the build, an external PR moved the cheat sheet panel
from right- to left-anchored, invalidating the design's assumption that
"left" was open ground — so the series nav panel joined the cheat sheet at
the same left anchor instead, and joined the existing Settings/cheat-sheet
mutual-exclusion group as a third member.

Scope was cut from the original sketch: this ships series-listing only, not
a duplicate of the inline "Contents" table of contents that already answers
"where am I on this page" — this panel only answers "where am I in the
series."

Two failures surfaced from the standalone/downloadable export path, which
strips navigation-dependent markup: the new toggle and panel weren't covered
by the existing stripping rules, and once added, the bundle's own string
literals (`"dl-navpanel-toggle"`) collided with an existing test asserting no
`dl-nav`-prefixed substring survives outside `<style>` blocks — fixed by
renaming `navpanel`→`seriesnav` throughout, since the collision was real
evidence the original name was too close to an existing convention.
*Cost to change: small-to-moderate. One new build.py function, one new token
threaded through five call sites, new CSS mirroring the cheat sheet's own;
new e2e and unit test coverage for ordering, current-item marking, and the
archived case.*

**7.74 — Pedagogical notes and dataset attribution, both shipped as
extensions to the existing cheat sheet panel rather than a third one.**
Neither is cumulative across a series the way the glossary is — a note or a
dataset belongs to the specific tutorial that declared it — so both ride on
`write()`'s manifest the same way `glossary` already does, without going
through `series_chain()`.

**Notes** are authored as `<aside class="dl-note" id="...">` in the body;
`extract_notes()` pulls each out of `body_html` entirely, since notes surface
in the sidebar, not mid-paragraph. A real correction made while building
this: raw HTML blocks aren't re-run through the markdown converter by this
project's existing pipeline, so `extract_notes()` runs each note's captured
inner text through `to_html()` on its own — meaning an image inside a note
becomes a real `<img>`, checked directly. `check_alt_text()` was extended to
scan every note's html too, since it would otherwise go unchecked after
removal from `body_html`.

**Datasets** use `data/<name>.yaml` beside `data/<name>.csv`, plus a
`datasets:` frontmatter list cross-referenced the same fail()-on-mismatch way
`practice_pairs()` checks `practice_for`. Both the CSV and its attribution
file (`source`, `license`, `description`, all required) fail the build if
missing, rather than shipping a nameless, sourceless dataset.

The panel's intro copy was reworded to scope its one real promise — "nothing
here is something you have not been taught yet" — to the glossary
specifically, since it never applied to notes or datasets. Each of the three
now gets its own heading in the panel.
*Cost to change: moderate. New `Note` dataclass, `Tutorial.notes`/`.datasets`
fields, extraction and validation functions, and a restructured
`renderCheatSheet()` — thoroughly covered by unit and e2e tests.*

**7.75 — The export button gets a small marker once notes have grown since
the last export, opt-out in Settings.**
The larger of `STUDENT_NOTES.md`'s two nudge proposals, left for later at
7.72, is now built: a `.dl-nudge` class on the export button once the notes
textarea has grown by `NOTES_NUDGE_THRESHOLD` (120) characters since the
last export, rendered as a small coloured dot via `::after`. It changes only
on an edit to notes, an export, an import, or "Start again" — never
mid-keystroke elsewhere.

The baseline is not a new field on the saved-progress record — that would
conflate "as of the last autosave" with "as of the last export" — but its
own lightweight per-tutorial localStorage key, the same pattern
`rememberVersion()`/`writePin()` already use. An import counts as an export,
since an imported file's notes already exist outside this browser by
definition. "Start again" clears both the progress key and this baseline.

The opt-out mirrors the existing progress-badges toggle exactly; turning it
off always removes the dot rather than merely showing it less often.
*Cost to change: small. Five small functions plus one more toggle-init
function following an existing pattern; five new e2e tests cover the marker,
the clearing, and the toggle.*

**7.76 — All three tooltip options built together: builtins, signature
help, and Jedi's pre-run answer for a name that has not been executed yet.**
`planning/CELL_TOOLTIPS.md` had recommended staging (a)/(b) first and
leaving (c) documented only. A prototype against the real pinned Pyodide
confirmed (a) cost nothing extra and (c)'s Jedi genuinely resolves a
function defined but never run, from source text alone, in low tens of
milliseconds — closing the open question about whether pre-run completion
was worth a second mechanism, so all three were built as one feature.

**(a) Builtins**: `docFor`/`signatureFor` check `__builtins__` via a shared
`lookupLiveName()`, live namespace first, builtins second, never shadowing a
student's own name.

**(b) Signature help**: `pythonSignatureHelp()`, a CodeMirror
`StateField`/`ViewPlugin` pair rather than `hoverTooltip()`, since nothing
triggers on typing the way hover triggers on the pointer. `callContextAt()`
scans backward from the cursor for the nearest open paren and its
identifier, counting commas for the argument index.

**(c) Jedi**: loaded in the background well after boot, since jedi+parso is
a ~1.6 MB download nothing about a first cell run depends on. Two Python
helpers live in `pyodide.globals`, never visible to or shadowable by a
student's own code, both wrapped in Python since a malformed mid-edit source
string can raise a wider variety of exceptions than a single JS catch should
enumerate.

**Live always wins** — the live-interpreter answer is tried first and Jedi
only fills the gap it can't reach, so the two can never disagree about a name
they both know.

One false start: a first hand-check of Jedi's pre-run signature help
returned nothing, which read like a real limitation but was an off-by-one in
the column passed to `get_signatures()`.
*Cost to change: moderate. Several new functions across `tutorial-runtime.js`
and `codemirror-entry.js`; the self-hosted Pyodide mirror grew from ~30 MB to
~32 MB for the jedi/parso dependency. Fifteen new e2e tests against the real
self-hosted Jedi.*

**7.77 — The Worker migration was built: Pyodide now runs off the main
thread on the hosted site, and "Run" genuinely becomes "Stop."**
`planning/CELL_CONTROLS.md` §2 had found the main-thread setup couldn't
support this at all, since a blocking Python loop leaves no thread free to
handle a click; this is the answer, built rather than re-weighed.

Two execution paths, chosen by `currentManifest.standalone`: the offline
export keeps running Pyodide on the main thread, since a `file://` page
can't use a module Worker and has no Stop button to justify the cost. Every
function that talks to Pyodide now exists twice — unchanged under an `MT`
suffix for that path, and behind a `workerRequest()` postMessage round-trip
for the hosted path.

`assets/pyodide-worker.js` runs the same `tutorial_tools.py` and
hover/completion machinery behind one uniform request/response protocol. The
interrupt itself is `pyodide.setInterruptBuffer()` against a
`SharedArrayBuffer`, which needs cross-origin isolation headers GitHub Pages
won't let this project set — `coi-serviceworker` (vendored) is the
same-origin service-worker shim that adds them anyway. `dewlab.canStop()`
reports the real achieved state, not merely "requested", since the shim's
first registration needs one reload before headers apply.

Cell output crosses the postMessage boundary through a new `_MessageSink` in
`tutorial_tools.py`, parallel to the existing `_DomSink`; `applyOutputEvent()`
replays the same stream/append/clear semantics on the main thread.
`KeyboardInterrupt` renders as a plain "Stopped.", not a traceback.

The widget bridge (`text_input`/`dropdown`/`button`) hands back a live DOM
element a Worker cannot supply — `_require_dom_sink()` now raises a clear
error naming the reason rather than degrading silently; zero published
tutorials used any of the three, so nothing live breaks.
*Cost to change: large, matching the earlier estimate. Touches the file both
execution paths depend on; eighteen e2e tests, full unit and e2e suites
green.*

**7.78 — dewmini gained `sqlite3`, Pillow, and a fourth widget,
`image_input`, plus a way to attach an image to a documentation cell — none
of it touching a tutorial page's own defaults.**
sqlite3 was deliberately excluded from tutorial content, as the one library
needing unvendoring beyond a single `loadPackage()` call — a real cost for
curriculum shipped to every published tutorial. dewmini is not curriculum
content, so that cost buys something there it wouldn't on a tutorial page.
`DM_PACKAGES` in `compose/dewmini.js` is dewmini's own wider default;
`tutorial-runtime.js`'s `DEFAULT_PACKAGES` is untouched.

`image_input(label, id)` joins the other three widgets in
`tutorial_tools.py`: a file input reads via the JS File API, decodes through
Pillow when loaded and falls back to raw bytes otherwise, landing in the
same out-of-band `_widget_values` dict the others use. Nothing published
uses any of the four widgets.

A documentation cell's own image attachment, unrelated to `image_input`,
lives entirely in `compose/dewmini.js`: a picture-frame button reads a pick
as a `data:` URL and appends it as inline markdown — deliberately restricted
to `data:` rather than a remote URL, since that's the only thing this button
ever writes. Capped at 3 MB raw before the read starts, since base64
inflates the stored size by roughly a third.
*Cost to change: small. `image_input` and the doc-cell attachment are
independent; `DM_PACKAGES` is one array read by both the live boot and the
standalone template.*

**7.79 — Mini IDE's output never actually rendered: a stale CSS class, not
the Worker migration, was hiding it — fixed, alongside a non-destructive
per-cell/toolbar output reset, a run-time stat, a quieter idle rail, and side
panels that no longer cover a wide cell.**
Reported directly: clicking Run in Mini IDE produced no visible output. The
worker path was writing real output the whole time; the bug was a stale
`.empty` class set once at cell creation and never removed, unlike
`.dl-output`'s `:empty` pseudo-class which re-evaluates on every DOM change.
Fixed by dropping the static class and matching `.dl-output`'s pattern.

**Non-destructive reset** joins the existing destructive Clear All: a small
↺ button per cell, and a toolbar-level Clear Output across all cells, with
no confirmation dialog needed since code stays untouched.

**A run-time stat** ("Ran in `<duration>`") under each cell's output, gated
by a new Settings toggle, timed with `performance.now()` and persisted on
the cell even while the setting is off.

**The idle-state coloured rail** (navy for Python, grey for text) is gone;
the rail now stays transparent until a cell is focused (orange) or errored
(red), keeping its reserved width so nothing shifts.

**Settings/Help panels overlapped a cell's own buttons at ordinary laptop
widths (1280-1440px)**, confirmed by measuring. A new `watchPanelOverlap()`
(a `MutationObserver` on each panel's `hidden` state) keeps `<html
data-dl-panel-open>` in sync, and each page's stylesheet left-anchors its
workspace and reserves margin for the open panel — scoped to Mini IDE and
dewmini's own stylesheets rather than `tutorial-style.css`, since the problem
was confirmed only on these two wider-workspace pages.
*Cost to change: small for the output fix and the rail; small-to-moderate
for reset/stats/panel-reach — each of the four features is independent and
any one could be reverted alone.*

**7.80 — Two more reported directly, both fixed: a cell's × now needs two
clicks, and the Texture "Size" slider now actually resizes Settings, Help,
and every other control, not just reading prose.**
A single accidental click on × used to delete a cell outright with no way
back. Both IDEs' delete buttons now arm on a first click (turning solid red,
"Click again to delete this cell") and only delete on a second —
auto-disarming after three seconds, on blur, or on any other click
elsewhere. Deliberately not a native `confirm()` dialog, since that needs a
mouse trip elsewhere where this needs only a second press of the button
already under the pointer.

**The size slider bug was a one-line root cause, in a rule every page
shares**: `--dl-font-size` was set on `body`, but nearly everything sized in
`rem` resolves against the *root* element's font-size, not body's — so the
slider visibly grew reading prose but left every panel and button its
original size. Fixed by moving the declaration to `html`. A second,
narrower bug this exposed — Mini IDE's own h1/intro/toolbar sizing through
the ordinary `.dl-page` column rather than its wider workspace override —
got the same fix extended to `.dl-page`.
*Cost to change: small. The delete confirmation and the font-size fix are
unrelated and either could be reverted independently.*

**7.81 — A Jupyter-import compatibility warning, three real shared datasets
(the first ever committed to `data/`), and four worked-example notebooks
reachable from both IDEs' own Import section.**
Three separate requests landed together, since each depended on groundwork
the last built.

**The compatibility scan** (`scanPyodideCompatibility()`, ported identically
into both IDEs) checks an imported notebook's Python source before its cells
land in the page, for an import Pyodide can't satisfy (`tkinter`, `torch`,
`subprocess`, `socket`, …) or a Jupyter magic/shell escape valid only inside
a real IPython kernel — not a full parser, just the regexes worth the
trouble. A dismissible banner lists what it found and which cell.

**Three real datasets**: `co2-emissions.csv` and `life-expectancy.csv`, both
trimmed from Our World in Data (CC BY 4.0), and `pride-and-prejudice.txt`
(public domain, kept byte-for-byte with its Gutenberg licence header, which a
worked example itself strips as a real data-cleaning step). `load_csv()`'s
docstring had cited `life-expectancy.csv` as its example since before the
file existed — it now does.

**Four worked-example notebooks** in `assets/examples/` (real `.ipynb`
files, importing through the same path a reader's own file would): SQL over
the CO₂ data, a life-expectancy convergence investigation, a Monte Carlo π
estimate, and a Zipf's-law word-frequency check on the novel. Every stated
finding was actually computed against the real shipped data, and every cell
ran end-to-end with zero errors. Reachable as four buttons in Settings →
Import, sharing every step after parsing with a reader's own imported file
via a newly factored `applyImportedCells()`.
*Cost to change: small-to-moderate. Three independent pieces, but the worked
examples depend on the datasets and would need rewriting, not just deleting,
if those were ever removed.*

**7.82 — A search box on the contents page and "Browse by topic"; the cheat
sheet renamed to "Reference" everywhere, with its own search added inside
it.**
**Search** (`assets/search.js`, new) matches a query against every live
tutorial's title, module, series, and its own glossary's specifically-
introduced terms. `write_search_index()` writes `assets/search-index.json`
after every build (archived and practice-only pages excluded) using
`own_glossary()` rather than `cumulative_glossary()`, so a search for a term
points at where it was actually taught. Matching is client-side: lower-cased,
a conservative rule-based stemmer, and a small curated synonym table — good
enough for a few hundred tutorials. Scored by field, so a title hit outranks
a glossary-term hit, which outranks a module-name hit.

**The cheat sheet is "Reference" now**, top to bottom, across code, tests,
and every planning/docs file — reported directly, on the reasoning that
"cheat sheet" reads as something a student should feel bad about needing,
when nothing in the panel is ahead of where the reader actually is.
`DECISIONS_LOG.md` and `QUESTIONS.md` deliberately keep the old name in
already-written entries, per this project's convention of not rewriting
finished history.

**The reference panel got a search of its own**
(`filterReferenceContent()`), deliberately simpler than `search.js`: a plain
substring match over the page's own already-in-DOM content, shown only once
a page has more than a handful of entries.

**Settings can now stay open alongside the reference or series nav**,
instead of force-closing whichever was open — only the stale three-way
exclusion (a carryover from before the reference panel moved to the left
corner) was removed; the reference and series nav still close each other,
since they'd otherwise overlap.
*Cost to change: small for search; moderate for the rename, purely because
of its breadth rather than complexity.*

**7.83 — Reference, Settings, and the series nav became docked sidebars,
toggled from the masthead instead of the page's corners.**
Reported directly, asking for the reference panel (and Settings) to become a
permanent, header-toggled sidebar rather than a corner popover — a placement
and shape change to already-proven panels, not a new feature.

**Toggle placement**: all three toggle buttons moved into a new
right-aligned `.dl-masthead-actions` row in the sticky masthead. Below the
phone breakpoint, where three full-text buttons plus the wordmark no longer
fit, each toggle collapses to icon-only with an `aria-label` carrying the
accessible name — confirmed by an actual screenshot at 390px, not assumed
fine.

**Panel shape**: the three panels went from floating cards to full-height
docked sidebars, flush to their edge with a single border in place of the
shadow.

**The margin-push mechanism had a latent bug this surfaced**: it pushed the
page clear by a flat 25rem regardless of a panel's actual width, never wrong
before since a floating card's `max-width` stayed under that — but a
genuine sidebar, resized wider by a reader, has no reason to.
`watchPanelOverlap()` now also runs a `ResizeObserver`, writing each panel's
live width into a CSS variable the margin rule reads, with the flat value
only as a one-frame fallback.

**Open state now survives navigating to the next tutorial in a series**
(`saveSidebarState()`/`restoreSidebarState()`), stored in localStorage. A
genuine ordering bug was caught before shipping: the existing overlap-sync
ran once at startup before restore had a chance to run, persisting
"everything closed" over whatever a reader had actually saved — fixed by
splitting the unconditional attribute update from the persisting sync.
*Cost to change: moderate — three coordinated CSS rewrites plus two
genuinely new runtime mechanisms, each independently small and tested, but
real work rather than a rename.*

**7.84 — Mini IDE and dewmini's own Settings/Help panels became docked
sidebars too, and a real resize bug 7.83 shipped with got caught and fixed
on all three surfaces.**
Both IDEs already shared `.dl-settings` from `tutorial-style.css`, so 7.83's
docked shape landed there automatically; the actual work was their own Help
panel and the existing margin-push mechanism, which got the same
width-tracking treatment via a `ResizeObserver` writing a single
`--dl-panel-w` (since both IDEs' panels dock to the same right edge and are
mutually exclusive). Open state is now persisted per IDE the same way.

**A real bug in 7.83's own right-docked panel, caught only once this pass
actually dragged the resize handle**: native `resize: horizontal` always
draws its handle at a box's bottom-right corner and grows the box away from
it — correct for left-docked panels (dragging right, into the page) but
wrong for anything right-docked and flush to the browser's edge, since
growing it would need dragging past the window's own edge. Fixed on all
three right-docked panels by removing native resize in favour of
`makeRightEdgeResizable()`, a plain pointer drag on a thin strip along the
panel's own left edge.

**A second bug found alongside the first**: the browser's native resize
sets width as an inline style, which beats any stylesheet media-query rule —
so a panel resized wide on desktop, then viewed at phone width, would keep
that pixel width instead of becoming a bottom sheet. Fixed with `!important`
on the phone-breakpoint width rule across all three panels.
*Cost to change: moderate — the docked-shape port was small, but the resize
bug it surfaced was real, touched three already-shipped panels, and needed a
genuine new mechanism.*

**7.85 — The README was split by audience: a short overview at the root, and
one document each for students, tutorial writers, code contributors, and
anyone reporting a problem.**
The README had grown to 671 lines addressing four readers at once — a
student, an author, a developer, and someone reporting a wrong answer —
each having to scroll past the other three, and reading as a project
walkthrough rather than a way in.

`docs/FOR_STUDENTS.md` takes everything a tutorial's reader needs;
`docs/WRITING_TUTORIALS.md` takes the whole authoring format;
`docs/REPORTING_A_PROBLEM.md` is new, since there was nowhere to send
someone with a found mistake; `CONTRIBUTING.md` absorbed the setup/test/CI
material. The README itself dropped to 161 lines: what dewlab does, a table
pointing each reader to their own document, a feature tour, and how to run
it locally.

The pass also closed real staleness the README had accumulated (Mini IDE,
dewmini, PDF/Jupyter export, search — all undocumented or wrong), and
merging 7.83/7.84 in mid-review caught `docs/FOR_STUDENTS.md` still
describing a panel layout that had just changed underneath it.
*Cost to change: small. Reversing it is a `git revert` plus deciding what to
do with the staleness fixes. The ongoing cost is that four documents can now
drift apart where one couldn't.*

**7.86 — The cheat-sheet rename finished in `QUESTIONS.md`: two dead file
paths fixed, and the term itself changed there too, reversing 7.82's
carve-out for that file.**
7.82 renamed `CHEAT_SHEETS.md` to `REFERENCE_PANEL.md` and its test file, and
kept the old term in already-written entries of `DECISIONS_LOG.md`/
`QUESTIONS.md` per this project's convention. Two references to the old
*paths* survived that convention regardless, since it never covered
signposts — fixed to name the files that actually exist.

Then the term itself, in two passes: `QUESTIONS.md`'s seven mentions became
"reference panel" (it's a live document a reader consults, not a historical
record, and shouldn't require working out the two names are the same
thing), then the last two mentions elsewhere in planning docs.

**`DECISIONS_LOG.md` is the sole exception, and stays that way** — a
decision record edited to match later decisions stops being evidence of
anything.

A sweep for the same mistake elsewhere turned up two more (a link to a
never-written outline, a section titled for a file that doesn't exist), both
left alone as somebody else's call.
*Cost to change: none worth naming. Twelve string edits across four files,
no code and no behaviour.*

**7.87 — dewmini can import a `.py` file now, closing out one of the five
items on the Mini IDE/dewmini parity list — and turned out to already be
most of the way there.**
A gap analysis found dewmini already had `.ipynb`/`.py`/`.html` export and
the compatibility scanner ported; only `.py` *import* was missing.
`run_query()` (the SQLite half of the same list) needed no work, since it
already lives in shared `tutorial_tools.py`, which dewmini's own seed
globals already expose — it was reachable in a cell before this session,
just unmentioned.

**`parsePyCells()` is the counterpart to `downloadAsPython()`, not to Mini
IDE's own `.py` parser.** Mini IDE's export/import pair uses a plain `# %%`
marker for Python-only cells; dewmini's own export already predates this
port and handles both cell types via its own `# ---- cell N ----`/
`# ---- note ----` markers, so the new parser reverses that exact prefixing
rather than adopting Mini IDE's narrower one and losing note-cell
round-tripping. A file with none of those markers imports as a single
Python cell, matching Mini IDE's own fallback.

Verified with an actual export-then-reimport round trip (three cells,
including a text note) confirmed identical, plus a separate
plain-script-import check.

Deliberately not done: recognizing Mini IDE's own `# %%` convention for
cross-tool import, since nothing today produces a file needing that.
*Cost to change: small — self-contained new parsing, a two-line dispatch
change, and a label update.*

**7.88 — dewmini can mount a persistent filesystem now: a real folder,
OPFS, or IDBFS, the same three backends Mini IDE already had, tucked into
Settings' own "Files" section rather than a sidebar tree.**
The second parity item. Asked directly which shape to take, since Mini
IDE's own file-tree sidebar is exactly the visual weight dewmini avoids — a
compact Settings section was picked over a fourth docked sidebar, matching
dewmini's "nothing to configure before typing code" ethos.

`compose/dewmini-fs.js` is a close port of `assets/mini-ide-fs.js`, trimmed
for the one real architectural difference: dewmini's Pyodide only ever runs
on the main thread, so the FS primitives call `pyodide.FS` directly with no
dispatching layer.

**A real collision this port had to design around**: Mini IDE's OPFS
backend mounts the origin's one shared storage root directly; unmodified,
dewmini would silently see the identical underlying files. dewmini's own
OPFS mount gets a named `"dewmini"` subdirectory instead, and the
native-folder backend's IndexedDB handle storage got a separate database
name for the same reason.

**A real gap this pass's own testing surfaced**: neither this port nor Mini
IDE's original synced the filesystem after a cell's Python code wrote to
the mount directly (e.g. `sqlite3.connect()` or plain `open().write()`) —
found by an actual write-then-reload test coming back empty. Fixed with a
new `sync()`, called fire-and-forget after every cell finishes running,
covering a cell's writes regardless of API. A second bug, also present in
Mini IDE's original, left a stale `<li>` in the hidden file list after
deleting a mount's last file — fixed by clearing the list unconditionally
rather than per-branch.

`DEWLAB_PYODIDE_BASE` (the self-hosted-Pyodide override the other two
runtimes already had) was added to dewmini, both on its own merits and
because it was the only way to test any of this against a locally-vendored
Pyodide.

Deliberately smaller than Mini IDE's own file manager: a flat root-only
list, not a recursive tree.
*Cost to change: moderate — the FS module is a largely mechanical port, but
the OPFS namespace collision and the missing post-run sync were genuine
design decisions this port had to make, each caught by an actual end-to-end
Playwright test.*

**7.89 — dewmini's Python now runs in a Worker, with a genuine Stop button,
closing out the Mini IDE/dewmini parity list.**
The last of the four parity items, deliberately last since every earlier
item could be tested against dewmini's original main-thread interpreter;
this one replaces that interpreter itself.

Rather than duplicate Mini IDE's ~700-line worker/interrupt/postMessage
engine, `mini-ide-engine.js` was renamed to `assets/pyodide-engine.js` and
generalized into a shared module both tools import — a deliberate exception
to this codebase's usual "each page owns a thin copy" convention, justified
by the file's size (a real maintenance cost) and Mini IDE's planned
retirement, after which this file simply keeps existing under dewmini
alone. `dewmini-fs.js` was rewritten to delegate every filesystem primitive
to the shared engine instead of calling `pyodide.FS` directly, since a
Worker-hosted Pyodide isn't reachable from the main thread.

Two genuine bugs turned up, both specific to dewmini being a second page
sharing a module written for one: the engine's internal URL resolution used
the *page's* location, correct for Mini IDE at the site root but wrong for
dewmini one directory down — fixed by resolving against the module's own
location (`import.meta.url`) instead. And dewmini's `runCell()` checked
whether Stop was available *before* awaiting the engine's own boot, so the
button rendered permanently non-stoppable on a fresh page — fixed by
reordering to match Mini IDE's own sequencing.

Also gave dewmini genuinely new capability: Jedi-backed hover docs and
signature help on code that hasn't run yet.

Verified end-to-end against a real, locally-vendored Pyodide on both pages:
cross-origin isolation lands on each, a tight infinite loop is genuinely
interrupted on the first click of a page's very first cell, and the
interpreter survives and runs further cells afterward.
*Cost to change: high — not the line count, but the risk: this replaces
dewmini's actual execution engine and touches the file both tools now
depend on, and both bugs above were exactly the kind that only show up when
a real browser runs the thing.*

**7.90 — Every tutorial is a folder, from the moment it is created.** A
tutorial lives at `tutorials/<module>/<slug>/`, holding its markdown
(`<slug>.md`), practice page, glossary, frozen past releases (`v<version>.md`),
and any images or recordings — never as a lone file at module level.
`Tutorial.out_path` and saved-work keys are computed from frontmatter
(`module`/`slug`), not from the source path, so this layout never affects a
page's URL or a student's storage key. `resolve_assets()` rewrites a plain
`src="picture.png"` per page so an author never has to account for the
current release and a frozen one living at different folder depths — a
reference to a file the folder doesn't hold fails the build, like a dead
`tutorial:` link. `<slug>.md` is always the current release; `v<version>.md`
is always a past one; releasing adds a file and moves nothing.
*Cost to change: low to reverse the layout mechanically, but rising with
every release added under it. Reverting also means giving up a place for
assets to live.*

**7.91 — Mini IDE has retired.** dewmini reached parity with Mini IDE (7.87–7.89), the trigger for retirement already decided earlier in this session. There is one Python workspace now, not two.

`assets/mini-ide.html` becomes a short notice page (a `<meta http-equiv="refresh">` plus a JS `location.replace()`) forwarding a visitor to `compose/dewmini.html`, so an old bookmark or link lands somewhere useful rather than a 404.

The original app survives, unlinked, renamed to `assets/mini-ide-offline-app.html`: `write_mini_ide_bundle()` in `build.py` now sources the downloadable Mini IDE bundle from that file rather than the (now short) hosted page, keeping the offline, run-without-a-server Python workspace working — dewmini has no offline distribution of its own yet. `mini-ide.js`, `mini-ide-fs.js`, and `mini-ide-style.css` stay for the same reason; they import the same shared `pyodide-engine.js` dewmini does (shared since 7.89), so nothing there needed to change.

The homepage's two-workspace chooser (`write_index()`) became a single dewmini card; the about page dropped its Mini IDE mention; `docs/DEWMINI.md` absorbed the file-manager/SQLite/Stop-button/import material that used to live only in `docs/MINI_IDE.md`, which became a short pointer; `docs/mini-ide-engine-explained.md` was renamed to `docs/pyodide-engine-explained.md` and rewritten to describe the shared module; the JS/FS explainer docs were brought current. Historical planning docs (`planning/MINI_IDE_REDESIGN.md`, `planning/DOCS_AND_COMMENTS_PASS.md`) were left untouched, describing what was true when written.

*Cost to change: moderate — mechanically straightforward (a rename, a short new page, prose updates across nearly thirty files that reference Mini IDE by name), but the hosted-vs-offline split needed care in `build.py`, verified against the actual downloadable bundle rather than just the redirect page.*

---

**7.92 — dewmini has its own downloadable, offline-capable copy now, and a real bug in both offline bundles' core promise got found and fixed.** The one item never brought over from the original four-item parity list (`planning/MINI_IDE_AND_DEWMINI_NEXT.md` §6) stopped being optional once Mini IDE retired (7.91) — dewmini is the only Python workspace there is now.

`write_dewmini_bundle()` mirrors the hosted site's actual folder shape (`compose/`, `assets/`, `data/` as untouched siblings) rather than flattening like Mini IDE's bundle does, since dewmini's hosted page sits one directory down with relative paths baked in — zero rewriting of app code, solved instead with a tiny top-level `index.html`.

**Neither offline bundle's "reopen it, no server needed" claim was actually true.** dewmini.js and pyodide-engine.js use real ES module `import`/`export`; a browser blocks that kind of cross-file import from a `file://` page with no origin for CORS to approve, so the page's JavaScript never runs — no visible error, just a blank toolbar. Mini IDE's own already-shipped bundle carried the identical, equally untested claim and hits the identical failure.

Fixed with `serve.py` — a zero-dependency wrapper around `http.server` (added to both bundles via `write_offline_serve_script()`) that serves the unzipped folder to `localhost` and opens a browser tab there, rather than rewriting either app to avoid ES modules (which would fork the shared engine). dewmini's `index.html` checks `location.protocol`: served, it forwards to `compose/dewmini.html`; opened bare, it explains `serve.py` instead of coming up blank. Mini IDE's bundle gets `serve.py` plus a plain `README.txt` instead of an in-page check.

The bundle includes `compose/` wholesale, the shared engine and worker, `tutorial_tools.py`, CodeMirror, the four worked-example `.ipynb` files and the `data/` folder they read from (found missing from `MINI_IDE_ASSET_FILES` too, left that way), and `assets/vendor/pyodide/` when fetched.

Verified served the way a downloader actually would (`python3 serve.py`): Stop-button test passes, a worked example loads, `load_csv()` reaches the bundled data, and the `file://`-opened case shows the new instructions.

*Cost to change: moderate — the bundle itself is a mechanical port of `write_mini_ide_bundle()`, but the `file://` finding applies to both offline bundles this codebase has ever shipped, and this pass's own freshly-written bundle would have carried the same bug had "has the right files" been treated as the same question as "actually opens."*

---

**7.93 — Highlight a word, and the reference offers to look it up — but only when it actually knows the word.** The reference panel could already be searched by opening it and typing; this closes the gap when a reader is already looking at a half-remembered term mid-sentence.

**The design decision that matters is the silence.** The offer appears only when the selected text matches a term this page's reference has actually taught — never on every selection, since most selections are just copying text, and a panel that lurches in response would be an interruption. Select an ordinary word and nothing happens, which is the common case.

Matching is against term *names* only, never definitions (matching definitions would fire on ordinary words appearing inside some entry's prose). A selection matches when it contains a term or a term contains it.

Three real defects, found by driving it in a browser: the manifest's glossary is a flat list, not grouped by kind — `renderReference()` does the grouping, and the first draft read it as already grouped, producing an empty term list and a feature that never appeared; the click-outside handler that closes the panel also closed it on the button that had just opened it, now named as an exemption; and a selection can be off-screen, which put the lookup button off-screen too — it now declines to appear for a selection nobody can see, and clamps to the viewport otherwise.

The button releases the selection when used, which stops it re-offering the same lookup twice.

*Cost to change: low. One function in `assets/tutorial-runtime.js`, one CSS block, one exemption inside `initReference()` — no new storage, no manifest change, no build change. Removing it would leave no trace.*

---

**7.94 — "Where did I meet this?" answered in the reference panel, after the prose-linking version was built, measured and withdrawn.** `planning/ROADMAP.md` Phase 5 proposed linking every later occurrence of a taught term in the prose back to the tutorial that introduced it. It was built and worked structurally: 347 links across the site, first occurrence per section, skipping code/headings/existing links.

**It was withdrawn because the links were wrong too often to ship.** The glossary's terms include ordinary English words — *set*, *shape*, *limit*, *function*, *list* — and a regex cannot tell which sense a sentence means. Sampling eight uses of *shape* on one page: six were the everyday word, two were a matrix's shape. That is worse than not linking, and specifically worse for the adult learners `PEDAGOGICAL_STYLE_GUIDE.md#who-reads-this` describes, many expecting to be bad at mathematics — sending one of them to a tutorial on set theory because the prose said "set a seed" costs confidence.

**The goal survives; the mechanism does not.** Each reference entry a reader inherited from an earlier tutorial now carries "Introduced in *Title*", linking to the section that teaches it (`origin_of()`, `origin_anchor()` in build.py; rendered in `renderReference()`). A tutorial's own new terms carry no origin. This can't be wrong about sense, because it never guesses at one: the entry a reader is looking at *is* the term. It composes with 7.93 — select a word, get the panel, see where you met it.

Worth recording: the obstacle for anyone revisiting prose-linking is sense disambiguation, not matching — stemming or a `forms:` list solve a different problem than the one that bit here.

*Cost to change: low. `origin_of()` adds one optional key to a manifest entry and nothing else reads it; the prose-rewriting code is gone rather than disabled.*

---

**7.95 — The edges audit: the offline bundle proved, two phone-width failures fixed, one heading-order break corrected.** `planning/EDGES_AUDIT.md` has the full account. Three things had been asserted and never tested; testing found two real defects.

**The offline bundle works, now as a measurement rather than a belief.** Built with a vendored Pyodide, served from loopback, with every non-loopback request aborted: zero blocked requests, a cell printing `42` with the network off.

**At 375px the page scrolled sideways, for two reasons, both URLs.** A bibliography DOI pushed a tutorial to 381px, and a Pyodide failure message naming a failed URL pushed the page to 511px — precisely when the reader is on a poor connection and least able to cope with an unreadable page. `#dl-body` now breaks inside a word where needed, `.dl-status` wraps anywhere, and every page fits 375px.

`tests/e2e/test_narrow_screen.py` was checked against the un-fixed stylesheet first — two of its three tests fail without the fix, confirming it actually catches the regression.

**The contents page jumped `h1` to `h3`**, which a screen reader hears as a missing section — deliberate, so a test helper could read every `h2` as a module heading. Module headings now carry `.dl-module-heading`, so telling them apart no longer depends on level.

**What this audit is not:** structural checks (control names, `alt`, one `h1`, landmarks, `lang`) say nothing about whether reading order, sidebar announcement, or cell-run feedback actually work with a screen reader — still open, and stated as such.

*Cost to change: nil to reverse — two CSS declarations and a class name. The value is in the three claims now tested and the one left honestly open.*

---

**7.96 — Five defects in 7.91 and 7.92, found by reviewing my own work before it merged.** Four were invisible to the tests meant to cover them; one repeats the mistake 7.94 was written about.

**The lookup offered ordinary words.** `termFor()` matched a selection against a term by plain substring, either way round — selecting "and" offered *pandas*, "excellent" offered *cell*: the same false-positive class that got prose-linking withdrawn (7.94), arriving through 7.93 instead. Matching is now whole-word in both directions, exact match preferred.

**A page with few entries stayed filtered.** `renderReference()` hides the search box below six entries, and the lookup skipped setting its value in that case; `initReference()`'s observer clears the filter on close by reading that value, so such a page reopened still filtered with no visible box to clear it. The value is now set whether or not the box shows.

**The origin anchor could land in the bibliography.** `origin_anchor()`'s fallback searched raw HTML and matched a citation title, sending a reader looking for "Monte Carlo method" to *Where to Read More*. It now searches per `h2` section's text (not markup) and skips the bibliography.

**A practice page resolved origins from the wrong directory.** `cumulative_glossary()` recursed with the target tutorial, computing hrefs relative to the wrong folder — a 404 once either page has a frozen release. The page being rendered is now passed down explicitly.

**A regression test that tested nothing.** 7.93's narrow-screen test appended its own `.dl-status` *inside* `#dl-body`, inheriting a rule that made it pass even with the real rule deleted — and the check meant to prove the test worked had reverted both rules at once, so the passing half was never isolated. The test now drives the real element, a sibling of `#dl-body`.

*Cost to change: nil — this is the fix, not a decision. Two of the five were found only by running the thing in a browser and reading its actual values; one was a test agreeing with itself.*

---

**7.97 — Six defects the Worker migration (7.89) left behind, found by reviewing it after it merged.** The first of these makes both workspaces unusable until the page is reloaded.

**"Restart Python" wedged the tool it exists to unwedge.** `pyodide-engine.js`'s `restart()` terminated the worker and called `pendingRequests.clear()`, dropping in-flight promises rather than rejecting them — so an awaited `run-cell` never settled, and dewmini's `running` guard stayed set forever, ignoring every later Run. `restart()` now rejects what it drops. The engine is shared, so Mini IDE had the same bug.

**Two follow-ons only reachable once it rejected.** `runAllCells()` reset each cell's Run button *after* its await with no per-cell `try`, so a mid-batch rejection left a button stuck showing "running." `uploadFsFiles()` returned silently on a boot failure it assumed was already reported elsewhere; a boot failure now propagates out.

**An open output stream survived a re-render it should not have.** `applyOutputEvent()` caches the open `<pre>`, and reordering or inserting a cell mid-run replaces the output area underneath it, so appended text vanished into a detached node. A cached `<pre>` no longer in the current output area is now treated as no open stream.

**Two documentation claims the migration falsified.** dewmini's Help panel and `docs/DEWMINI.md` claimed the interactive widgets "work here exactly as they do on a tutorial page" and that a runaway cell had to be waited out — both false once execution moved off the main thread (widgets now raise `RuntimeError`, and a Stop button exists). Both docs corrected.

**And `__name__` disagreed with itself.** The live page is seeded `__dewlab__`; dewmini's standalone export still said `__dewmini__`. The export now matches.

*Cost to change: nil — these are fixes. Every one was created by moving execution off the main thread, and none was caught by a test; three needed a browser to see at all, and two were documentation that quietly became false while the code around it stayed correct.*

---

**7.98 — Mini IDE is removed, not just retired.** 7.91 retired the hosted page but kept the app alive underneath, on the reasoning that dewmini had no offline distribution yet. 7.92 ended that reasoning by giving dewmini its own offline bundle; this entry acts on the expiry. The four asset files, `write_mini_ide_bundle()` and its output, the tombstone `docs/MINI_IDE.md`, and the two explainer docs for the deleted code are all gone, and every present-tense reference across code, docs, tests, and planning was reworded.

**The redirect goes too — because there was never anyone to redirect.** 7.91 kept `assets/mini-ide.html` as a redirect on the reasoning that an old bookmark should land somewhere useful. The site has never been deployed or shared with students, so no such bookmark exists anywhere but this repository's own history — a redirect with no possible visitors is furniture, not continuity, and was removed. (Had the URL ever been shared, 7.91's reasoning would have been right; it simply rested on a premise that turned out false.)

**Historical records stay historical** — the earlier planning docs and this log's own earlier entries keep their original wording; present-tense documents now describe one workspace.

**Found while removing: the deploy guard never excluded dewmini's own bundle.** `.github/workflows/deploy.yml` excluded `site/download/mini-ide/` from its built-page count but not `site/download/dewmini/`, shipped since 7.92. Fixed to name the bundle that actually exists.

*Cost to change: low — the deletions are the easy half; the care was in the sweep, since nearly forty files mentioned the old workspace, and in deciding which mentions were history (kept) and which were description of the present (reworded). Nothing removed here was ever in anyone's hands.*

---

**7.99 — dewmini becomes a workbench: tabs, two rails, and tools for looking at your own work.** Asked for directly: tabs, sidebars on both sides carrying file imports and variable inspectors, a fuller reference with search and category navigation, data import, and a right-hand side moved from settings towards notes and pedagogy. Widgets — the one real capability gap — were explicitly deferred. `planning/DEWMINI_WORKBENCH.md` is the design; this entry is what was decided along the way.

**The smallness rule is restated, not abandoned.** dewmini's planning docs all say it is the small one, small *against* Mini IDE — which 7.91 removed. A tool with no alternative cannot also refuse to grow, so the discipline becomes **quiet by default, everything one press away**: nothing new opens on a first visit, the notebook keeps full width until a rail is asked for.

**Three panels across two edges, on a layout that already existed.** Library (left, what you look up), Workbench (right, your own work), and Settings (stays right, stops being the headline — Notes and Files moved out of it). Help became Library sections rather than its own panel. `tutorial-style.css` already carried independent left/right panel widths since 7.83; dewmini had collapsed that to one attribute while both its panels docked right — deleting that override *is* the two-rail layout. A docked rail must not close on an outside click, unlike a popover.

**Tabs re-point one variable rather than rewriting the file.** `notebooks[]` holds `{id, name, cells}`; the module-level `cells` *is* that array, not a copy, so existing functions kept working untouched — at the cost of one hazard (assigning `cells` alone detaches it), guarded by making `setCells()` the only sanctioned way to swap. Storage moved to `dewmini:notebooks:v1` with a tested one-way migration, old key left in place as a fallback.

**One Python session shared by every tab, made visible rather than silent.** Giving each tab its own kernel would mean threading a namespace identifier through the shared engine and across the worker boundary — too large a change to make overnight. Instead the Workbench's Variables list says plainly that it is one shared session. If that confuses people, a per-tab namespace is the documented fix.

**The reference drops tutorial pages' spoiler rule, on purpose.** `REFERENCE_PANEL.md` §1 protects a reader's position in a sequence; dewmini's readers have no such position. `write_reference_index()` emits the deduplicated union of all terms (248 today) from the same source the tutorial pages use. Each entry names its origin tutorial but does not link to it, since the offline bundle carries no tutorials.

**The variable inspector is Python, not JavaScript.** `describe_globals()` walks `_page_globals` and returns plain strings — testable under CPython, and nothing crosses the worker boundary as a proxy.

**Data: one claim this environment could not test, so it is not made.** The sandbox blocked `ourworldindata.org` outright, so remote fetching could not be tried; `load_csv()` was extended to fail informatively (naming CORS, pointing at downloading and importing via Files) and the untested check is logged in `tests/MANUAL_CHECKLIST.md`.

**dewmini has e2e coverage for the first time** — twelve browser-driven tests, which immediately found that an empty cell container has zero height, so "visible" is not what a test should wait on.

*Cost to change: substantial and mostly additive — ~900 lines across dewmini's three files, one shared-engine message, a vendored CodeMirror addition. Risk concentrates in the `cells` aliasing and the shared engine, where the new message follows an existing path exactly rather than inventing a second shape.*

---

**7.100 — Ordinary Python HTTP code works here now, and `https` was never the thing that was missing.** Prompted by a real failure on the live site: pasting Our World in Data's own fetch snippet gives `urllib.error.URLError: unknown url type: https` in 8ms.

**Two claims I made about this were wrong.** I said `requests` "isn't available and can't be," and that reading a URL with pandas could not work in a browser. Both false: Pyodide ships `requests`, `httpx`, `aiohttp`, `urllib3`, and `pyodide-http` (which reroutes Python's HTTP machinery through the browser's own fetching) — simply not loaded at boot. Tested in a real browser: after `pyodide_http.patch_all()`, the snippet works verbatim.

**The fix is 9.6 KB, so it is on by default.** `pyodide-http` alone (without `requests`, ~470 KB heavier) is enough to make `pandas.read_csv(url)` work, since pandas goes through `urllib`. Loaded at boot in both engine paths, wrapped in try/except so an older vendored Pyodide still boots without it.

**`https` was never unavailable — Python had no handler for it.** A Pyodide build ships no TLS library, so `urllib` rejects the scheme before any connection is attempted; that is the absence of Python's *own* encryption, not of encryption. Through the patch, the browser performs the TLS with its own certificate validation — verified against a real TLS server with Chromium pinned to that one certificate by fingerprint, not told to ignore certificate errors.

**The cost, named: a hung request cannot be stopped.** The patched path is synchronous inside the Worker, so Stop does nothing while it waits — a new way to be stuck, traded for because "instant unhelpful failure" is not better than "works, but a slow server can hang you." The async route (`await load_csv(url)`) does not block and remains what the docs lead with. A timeout on the patched path is the obvious follow-up, not done.

**Errors that are about the browser now say so.** `_ERROR_HINTS` matches a short list of failures with an unhelpful Python message and appends a plain-English note under the traceback.

*Cost to change: small in code, wide in reach — this touches the shared engine's boot, so it changes tutorial pages too, justified on the same grounds: a tutorial cell hits the identical wall.*

---

**7.101 — The reference's categories are derived, never tagged; and the rail's smallest text gets a floor.** Three asks about the Library rail, the one that changed the design being: "the layers are actually a great proxy for beginner/intermediate/advanced... if we change the tree later it automatically changes the search."

**That is the whole scheme.** The first pass had subject and level as hand-maintained fields. Now:
- **Subject** comes from the learning-outcome code *prefix* a tutorial already claims in `covers:` (not `strand`, which cuts across the maths/computing line). Tutorials claiming outcomes from both sides are filed under both — not a fudge, since a term introduced there genuinely belongs to both.
- **Level** comes from `topic_tiers()`, the prerequisite depth of the `needs:` graph — nothing hand-tagged, so rearranging the tree re-files every term on the next build with nobody retagging anything. A test rebuilds after sliding groundwork under a topic and checks a term moves tiers.

**Deepest outcome, not shallowest.** `min()` was tried first and rated a tutorial by its easiest moment, putting 150 of 222 terms in "beginner." Erring deep is the kinder error; bands at ≤2/≤3 tiers give a real spread (22/16/5 tutorials) where the obvious ≤1/≤3 alternative collapses to 10/28/5.

**A tutorial claiming no outcomes is left unfiled, not guessed at** — "Unfiled" is offered as a value of its own so those terms stay reachable.

**The topic row is a `<details>` in the normal flow, not a popover**, so opening it pushes the list down rather than covering it — tested by measuring the row's bottom edge against the list's top edge. Subject and level stay on the surface; topic and kind fold away, with the summary reporting its own state ("Topics · 1 on").

**The group list is read off the data too** — found by a test: the topic row was drawing from a hand-kept list of group keys that would silently miss a new group. Curated short labels stay as an *override*; an unlabelled group's key is turned back into words, a visible prompt to name it.

**"A bit small for tired eyes" was measurably right.** At the old 15px floor, filter chips rendered at 10.2px. The slider minimum moves to 16px and small labels take a `max(…, 12px)` floor. A sweep test walking every element in the rail (not just the four just changed) found five more elements below the floor.

*Cost to change: small. The bands are one tuple; the subject map is one dict; the disclosure is one `<details>`. Going back to hand-tagging would be the expensive direction.*

---

**7.102 — The boot patch was not universal, and the toolbar had two buttons for one job.**

**The networking patch (7.100) reached two of four boot paths, not four.** dewlab starts Pyodide in four places; the patch had only reached the hosted worker path and dewmini's no-worker fallback. Missed were `tutorial-runtime.js`'s own `bootMainThread()` — used by **a downloaded tutorial** — and `compose/dewmini.js`'s export template — used by **an exported notebook**: the worst possible place to miss, since those are exactly the copies opened with no second machine to compare against. Fixed in both, same try/except guard. Verified against a real downloaded export reading `https://` from a real, certificate-pinned TLS server.

**The lesson is about how the gap was found:** not by reading the diff, but by being asked whether the claim held everywhere, then enumerating every `loadPyodide(` in the repository instead of every one remembered. "Is this universal?" is a different question from "is this right?"

**The toolbar's Python and Text buttons are gone** — the seams between cells already add a cell, where you're looking, so two buttons for the same action was one too many. The freed space takes **See an example** and **Start with imports**, previously findable only in the empty-notebook block and so invisible after the first cell.

**Which exposed a hole:** the first seam was suppressed over an empty notebook (a seam with nothing on either side looks like debris), which with the toolbar gone would have left no way to start a *blank* cell. The seam is now drawn from the start.

**And a fixture bug main exposed:** a test fixture guarded a Pyodide override with `if "DEWLAB_PYODIDE_BASE" not in html`, satisfied merely by a code *comment* mentioning the name, silently disabling the injection. Fixed to match the actual assignment and assert the result — a guard a sentence can satisfy is not a guard.

*Cost to change: small. Two four-line boot additions, one markup move, one deleted conditional.*

---

**7.103 — Both rails drag the same way, and a width someone chose survives the reload.** Asked whether the side rails are resizable "so one could work split screen" — they were, and measuring found the answer was worse than yes.

**Two rails, two different affordances, unified into one.** The right-docked panels had a full-height drag strip (native `resize: horizontal`'s grip sits flush with the browser's own edge there, unusable); the left-docked ones were left on native resize, which genuinely works for a panel growing rightward into the page — but native resize is a small corner triangle, not findable next to the strip's obvious full-height highlight. `makeRightEdgeResizable` becomes `makeEdgeResizable(panel, side, …)`, and native resize is gone from both files.

**The strips were hung outside their panels, losing half their width.** The handle sat straddling the panel's edge, but a docked panel is a scroll container that clips absolutely-positioned children to its padding box — half of every strip was being thrown away. It worked by luck on the right (the clip's leading edge is inclusive) and not on the left, where the first drag test moved nothing; hit-testing the strip's midpoint returned the panel itself, which named the cause. Both strips now sit flush inside the edge. Nearly missed because the DOM, class, and CSS all looked right — only a real pointer drag showed it doing nothing.

**A width nobody remembers is not a split screen.** `saveSidebarState()` stored only which rail was open, not how wide it had been dragged, so a rail pulled to half the screen snapped back on reload. It now stores and restores a width per panel.

**Measured rather than asserted**, at 1440px: Library at 560px and Workbench at 612px leave the notebook column at 191px with no overlap — 1363 of 1440px accounted for.

*Cost to change: small, and it deletes more than it adds — one shared function in place of two, three `resize: horizontal` declarations gone.*

---

**7.104 — The union reference is settled, on a better reason than the one I gave for it.** 7.99 dropped the tutorial Reference panel's spoiler rule for dewmini and flagged it as Josh's to overrule. He confirmed it, on stronger reasoning: *"we just don't know what the student will be doing when they open dewmini... maybe they have done all the tutorials online and we just can't see them?"*

My argument was about dewmini's nature — a workspace with no position in a series has no position to protect. His is about the reader's: the spoiler rule assumes the page knows where its reader has got to, which dewmini cannot know, since nothing is tracked anywhere (a deliberate property of the whole project). Hiding two thirds of the reference would mean guessing, wrongly, against a reader who may have finished the course.

Worth recording because it changes what would reopen this: under my reasoning, revisiting would follow from dewmini becoming more curriculum-shaped; under his, it only reopens if dewmini gains a way to *know* a reader's progress — which would mean tracking them, refused on other grounds entirely. Settled harder than I had it.

*Cost to change: unchanged — one function, both behaviours tested. The reason to change it is now much narrower.*

---

**7.105 — A stale-output marker, strict from the start.** A proposal paired this with execution counters; Josh asked to leave the counters out, and the marker doesn't need them — it only needs to remember what a cell's content looked like when it last ran and compare that to what's on screen now.

**Any difference counts, whitespace included.** Started strict, per the proposal's own recommendation: normalising before comparing is a judgement call about what counts as a "real" change, and a wrong judgement there hides a genuine edit rather than merely annoying someone over a harmless one. Loosen it later, with a reason in hand, if it turns out noisy.

**The marker does not survive a reload, on purpose.** `ranContent` is never written to or read back from saved state, the same treatment `lastRunMs` gets — nothing a cell's Python actually *did* survives a reload either, since the interpreter doesn't. A marker that persisted would claim a fact about a session that no longer exists.

*Cost to change: small — one field on the cell object, one comparison function, one CSS rule.*

---

**7.106 — Run above/below, behind a menu rather than two more buttons.** The practical repair once a reader notices (via 7.105's marker, or experience) that a cell's output no longer matches what's above it.

**The mechanics mostly already existed.** `runAllCells()` already did the batch loop, per-cell Stop-button state, and error tally — always over every cell and always after a reset. It became `runCellBatch()`, parameterised on which cells and whether to reset first, with `runAllCells()`/`runAbove()`/`runBelow()` as its three callers.

**The one real risk was getting `reset` backwards.** "Run above" resets the namespace first, like "Run all," so what's on screen matches what the code actually did; "Run below" must not, since its entire purpose is keeping the state the cells above it already built. Getting this boolean backwards would have shipped a feature that silently destroys work.

**Where the controls went:** both options live behind one "⋯" toggle rather than two more always-visible icons (which would cut against 7.102's own recent removal of duplicate buttons), using the same open-while-active, remove-on-close outside-click pattern `armDeleteButton()` already uses — needed here since a menu on every cell makes an unremoved listener a real leak, not theoretical.

*Cost to change: small-to-medium. The batch runner is one function used three ways; the menu is self-contained.*

---

**7.107 — Maths in dewmini text cells: a second implementation, on purpose, and the offline bundle takes the weight.** `$x^2 + 3x$` in a dewmini text cell now renders as maths, the way it already does in a tutorial.

**Ported, not called.** Tutorial maths runs through `build.py`'s Python, build-time `extract_math()`/`render_math()` against python-markdown's input; dewmini's text cells run through a hand-written JavaScript renderer, `renderDocMarkdown()`, not python-markdown at all — there was no function to reuse, only the pattern. `extractDocMath()` lifts `$…$`/`$$…$$` into the same placeholder scheme *before* the markdown pass runs, for the same reason the Python side does: an underscore inside TeX is otherwise eaten by an emphasis rule.

**A second maths renderer, and that is a deliberate, narrow choice.** dewlab already has at least three markdown surfaces outside the tutorial pipeline (including a fourth found in this session's own audit: `tutorial-runtime.js`'s copy of `renderDocMarkdown()`, for a reader's own cells on a tutorial page, which stays unaware of maths). Whether to converge on one client-side renderer is a real open question this smaller, proven change deliberately defers rather than answers blind.

**KaTeX's stylesheet loads unconditionally; its 266 KB renderer does not.** dewmini has no manifest to gate the JS on at build time, so the gate is behavioural: `loadKatexRenderMath()` fetches the bundle the first time a `.dl-math` span actually needs rendering, and never before.

**The offline bundle takes the ~590 KB.** A comment in `DEWMINI_ASSET_FILES` correctly said, before this, "dewmini renders no maths" as the reason KaTeX was excluded from the download. Lazy loading only helps a classroom *with* a connection on first use, so the offline bundle must now carry KaTeX (JS, CSS, all twenty font files) or maths silently fails exactly where the bundle exists to work. Included, on the reasoning that a downloadable copy which can't do what the hosted site can is a worse trade than 590 KB — but flagged as Josh's call, reversible by dropping three lines and the fonts copytree.

**The standalone-HTML export needed no change** — it already renders a text cell as plain, literal text, so headings and bold were never rendered there either; there was nothing to inline.

*Cost to change: medium. The extraction/render code is small and tested; the ongoing cost is the ~590 KB in every offline download and the standing question of unifying the project's several markdown renderers.*

---

**7.108 — Restart and run all, as one button.** Throw the interpreter away, then run every cell from the top — the reproducibility check that pairs with 7.105's marker.

**The two halves already existed and needed only wiring:** `restartPython()` (factored out of the existing "Restart Python": `engine.restart()`, `dfs.reset()`, then `ensurePyodide()`) followed by the existing `runAllCells()`.

**Whether this is "just a label" was the open question, and the answer is no.** `runAllCells()` only resets the *namespace* — clear and re-seed the same interpreter. `engine.restart()` is a genuinely fresh interpreter, also clearing Jedi's completion cache and the mounted filesystem handle, neither of which the namespace reset touches. So "Restart & run all" is a strictly stronger check, not a second name for the same thing, and Settings now offers both.

*Cost to change: very small — one factored-out function, one new button, two confirm dialogues.*

**7.109 — Three of dewmini's own cell features, ported onto tutorial and practice pages.** `planning/CELL_IDENTITY.md` asked directly: tutorials, practice, and dewmini show the same idea — a cell running Python against a shared session — in three different pieces of markup. Full unification (one rendering function shared by `build.py`'s static HTML and dewmini's live JS array) is a large, invasive change explicitly not chosen here. What shipped instead: the stale badge, the "⋯" Run above/below menu, and Restart & run all (7.105, 7.106, 7.108) ported onto `build.py`'s `render_cell()` and `assets/tutorial-runtime.js`, keeping the two engines and DOM systems separate, per the project's convention of a thin copy per page rather than a shared abstraction.

**Not ported:** the numbered identity pill (still an unbuilt design, dewmini included) and maths-in-text-cells (a tutorial's prose already renders `$…$` independently of dewmini's text-cell type).

**The one real engineering gap, closed here:** `assets/tutorial-runtime.js` had no `resetPageState()`/`restart()` equivalent at all. Both now exist, built the way `pyodide-engine.js`'s already were, reusing the existing worker message type and a newly-named `RESEED_GLOBALS_SOURCE` constant. Cell-run functions also now return whether a run raised, needed to count errors across a batch.

*Cost to change: small. Every new function names the dewmini original it was ported from. The real ongoing cost is the shared-implementation question this deliberately defers. 7.110 builds the identity pill, in dewmini.*

**7.110 — The full cell-identity design, built in dewmini.** The numbered pill, per-type colour, merged run-line, and collapse triangle `CELL_IDENTITY.md` designed and 7.109 left out — built now on request, with three amendments made because building surfaced questions the mockup hadn't:

**Collapse is for every cell type, not only code-bearing ones.** The design reasoned Text/HTML didn't need it since they already have a rendered form to shrink to — true once rendered, but a long Text cell in *edit* mode has no such fallback. Both types get the triangle now.

**A header-end group, with a genuinely new feature: Duplicate** — insert a copy of a cell right after itself. Not optional garnish: without it, the designed header-end layout (Edit, Duplicate, Delete) has a hole in it.

**The collapse triangle is one rotated chevron, not two swapped triangles** — the mockup's filled ▾/▸ read as confusingly similar to the Run button's own ▶ nearby; a single `›`, rotated by CSS, reads unambiguously.

**Run order resets on any reset, not only a full restart** — `runCellBatch()`'s reset path already cleared the Python namespace but never told the run-line, so a cell's line could disagree with the namespace state until a full restart. Fixed to reset alongside any namespace reset.

**Not ported to tutorial or practice pages** — those keep 7.109's narrower slice; the type-colour system needs real content to colour (tutorials are Python-only) and the layout move is separate work on the primary reading surface.

*Cost to change: medium. `createCellElement()` is substantially rewritten as one well-organised function rather than several scattered ones. `lastRunMs` is no longer persisted, since it's meaningless without `ranOrder`, which was never persisted either — no migration needed.*

**7.111 — The style guide gained a plain-language section, and the four student-facing surfaces were rewritten to it.** The contents page, About page, topic tree, and 251 glossary definitions all passed the style guide's voice section (then §4) as written — invitational, warm, prose not bullets — and were still hard to read: §4 governed stance, not sentence architecture, and §1 says a reader may be working in a second language.

Six habits ran through all four surfaces: a short main clause with an em dash carrying the actual meaning; definitions written as participles rather than sentences; contrast before definition; metaphor replacing the plain statement rather than following it; Irish/British idiom; and a closing aphorism.

Measured before and after: the About page went from 29.7 words/sentence (Flesch–Kincaid 14.1) to 17.7 (FK 8.2); the contents page 17.7→11.5 (FK 9.4→6.1); `topics.yaml`'s descriptions 18.7→15.8 (FK 9.3→7.9); the glossary 15.8→13.4 (FK 8.5→7.4). 25 of 81 topic descriptions and 64 of 251 glossary definitions were rewritten — only those breaching the new rules.

The rule went into §4 as a subsection, since several planning documents and a skill cite this guide by section number.

*Cost to change: small for the guide, large for the prose — reverting means putting back text across `build.py`, `topics.yaml`, and 30-odd glossary files. `tests/test_build.py`'s contents-page test checks that the introduction exists, not its exact wording — update the phrase there rather than working around it.*

**7.112 — The contents page introduction is one paragraph and six points, in the order a reader meets them.** Six paragraphs and 254 words answered several independent questions in prose — what is a cell, can I break this, where does my work go, how is the list organised, where do I start — so a reader with one question had to read the rest to find it. §4's prose-over-bullets rule is about an *explanation*, where the joins between sentences carry the reasoning; six separate answers to six separate questions have no joins to remove, so this is a noted exception, not a breach.

Two points were reframed after the first draft got them wrong: "we try things before we name them" is really about the sequence — explore, then the principle, then the name, since the name is how a student talks to somebody else about what they just did (now in §3); the practice point's answers sit below the problems because the answer was never the thing worth protecting.

§4 gained the sentence-level rules this exposed: mark a sequence with *first… then… then*, don't make a reader hold a negative before there's anything to hold it against, "we" for the learning and "you" for what is theirs, hedge any non-binary claim.

*Cost to change: trivial for the wording, small for the shape — the points live in one list in `render_index()`; reverting means deleting `.dl-intro-points` and both exception notes.*

**7.113 — The pill and the run line, ported onto tutorial and practice pages too.** 7.110 built the numbered pill and merged run-line in dewmini, leaving tutorial/practice pages on 7.109's narrower slice; this carries both over. `build.py`'s `render_cell()` now renders a `.dl-cell-pill` (`Cell N`, a coloured "Python" badge) and a single `.dl-cell-runline` span in place of the old bare id and separate stats/stale-badge pair; the run-line machinery in `assets/tutorial-runtime.js` is a close copy of dewmini's, adapted to read code from CodeMirror directly.

**The pill's number is static, not live** — a tutorial page's cells can't be reordered, so `render_cell()` takes the fixed 1-based position as an argument; no drag handle exists for the same reason.

**No new colour token, and no drag/collapse/Duplicate.** Every authored cell is Python, so the badge always reads "Python." Custom (reader-added) cells were left out of this port. There is no header→footer move needed here: `render_cell()`'s bar was already positioned correctly before dewmini had one — dewmini was the side that needed to move to match.

*Cost to change: small. The only real new surface is `render_cell()`'s `number` parameter.*

**7.114 — Collapse and Duplicate, the rest of dewmini's cell anatomy, ported to tutorial and practice pages.** Duplicate needed a real design decision: every dewmini cell is the reader's own, so "duplicate" means "copy something I own." An authored tutorial cell is the tutorial's fixed content. Chose to have Duplicate drop a copy in as a new *custom* cell right after the original — keeps the button meaningful everywhere the pill/run-line are, and turns "try it yourself" into one click.

**Duplicate reuses the existing custom-cell insertion seam** via `duplicateAsCustomCell(cell, type)`, landing right after the copied cell using `cell.element.nextElementSibling` — the first version used `lastDividerFor(cell.id)`, which finds the *last* divider under an anchor, so a second duplication landed after a reader's own inserted cell instead of after the original.

**Collapse applies to every cell with editable content**, the same table `CELL_IDENTITY.md` §4 settled for dewmini. One function, `setCellCollapsed(cell, collapsed)`, serves both authored and custom cells by reading fields off whichever cell object it's given, since this file builds the two kinds through different functions unlike dewmini's single closure.

**Collapse must save immediately, not on the debounced timer** — the first pass wired it through the same debounced save every keystroke uses, and an e2e test caught reload beating the 500ms timer. Fixed to save directly, matching dewmini's own behaviour.

**Corrected while writing this: 7.113 overstated what was left** — it claimed the header→footer layout move stayed dewmini-only, which was never true. Fixed in both entries. (Renumbered from 7.111/7.112 to 7.113/7.114 while merging main, since those numbers were taken by the plain-language pass landing first from a sibling branch.)

*Cost to change: small. Any new way to mutate `cell.collapsed` needs an immediate save call alongside it — easy to reintroduce by copying the pattern every other mutation in this file follows.*

**7.115 — A text cell's chrome finally goes quiet until touched, in dewmini and on tutorial and practice pages both.** `CELL_IDENTITY.md` §4 described this from the start — a Text cell renders by default and hides its own chrome (`opacity: 0; pointer-events: none`, not `display: none`, so a keyboard user tabbing onto a hidden control still reveals it) until touched. Earlier entries implied dewmini already had this; checked directly, it never did.

**One rule, no JavaScript, on either side.** `.dm-cell-text:not(:hover):not(:focus-within)` fades the head/collapse column; `@media (hover: none)` keeps chrome on for touch devices. No JS class-toggling needed — focusing the textarea already makes the cell match `:focus-within`.

**Deliberately not changed:** a single click on the rendered view still starts editing directly, with an explicit Edit/View toggle as the accessible alternative — established behaviour, outside this entry's scope.

*Cost to change: trivial. Pure CSS on both sides.*

**7.116 — HTML, the first of the four new cell types §8 designed, built in dewmini.** Source is a CodeMirror editor; rendering is a sandboxed `<iframe sandbox="allow-scripts" srcdoc="…">`, no `allow-same-origin` — a reader's HTML cannot reach the page's own window, storage, or DOM.

**Rendering, not source, is the click target — unlike Text**, since a click inside a cross-origin iframe never bubbles to the parent document; the header's Edit/View toggle is the only way in.

**A real bug: `if {} else {} else if {}` is invalid JavaScript**, hidden by this file's `.js` extension from `node --check`, which parses a plain `.js` file as CommonJS rather than the ES module it runs as in the browser. Checking against a temporary `.mjs` copy reproduces the real `SyntaxError` — worth reaching for on any future change to `dewmini.js` or `tutorial-runtime.js`.

**Another real bug, caught by an e2e test:** `readCells()`'s type whitelist would have silently dropped every saved HTML cell on reload. Fixed to check membership in `CELL_TYPES` generally, correct for future types too.

**A test-tooling wrinkle:** hovering a cell's geometric centre doesn't reliably trigger `:hover` when that point is inside a sandboxed iframe under Playwright's synthetic input; the test helper now hovers the header row instead.

*Cost to change: small. The HTML branch mirrors Text's shape closely enough that the next type should be a similarly small addition.*

**7.117 — CSS, the second of the four new cell types, built in dewmini.** Close to a copy of 7.116's HTML branch, with two differences settled beforehand: the iframe's `srcdoc` is a fixed little sample page with the reader's rule injected ahead of it, not the reader's own markup; and styling the HTML cell above it was set aside, since that would make a CSS cell's behaviour depend on cell order.

**A UX bug caught before shipping:** a new CSS cell opened with its editor already hidden, since the first pass called `showRendered()` unconditionally. Fixed to the same rule HTML and Text use — only a cell restored with existing content opens to its preview.

`READ_NOT_RUN_TYPES` (`text`, `html`, `css`) replaced an accumulating `||` chain, reading as what it means rather than a growing exception list.

*Cost to change: small, and getting smaller — CSS took noticeably less new code than HTML. SQL and JavaScript won't get the same discount: both need a genuinely new execution engine.*

**7.118 — SQL, the third of the four new cell types, built in dewmini — on Python's own `sqlite3`, not the *sql.js* engine `CELL_IDENTITY.md` §8 had specified.** Implementation started on sql.js (a second WebAssembly interpreter alongside Pyodide) but was set aside mid-build: dewmini already runs Python, and Python already ships `sqlite3` as an ordinary loadable Pyodide package. Two engines would mean two data models with nothing bridging them; one engine means a SQL cell's `CREATE TABLE` is immediately readable from a Python cell via `pd.read_sql()`. All sql.js groundwork was reverted before anything was committed.

**What got built.** `_run_sql_cell(conn, script, max_rows=20)` in `tutorial_tools.py` splits a script on a bare `;` (a plain split, not a real parser), runs every statement but the last, and renders only the last statement's result — a table if it has columns, otherwise "N rows affected." A SQL cell's content is wrapped by `buildSqlCellCode()` into one generated Python line, the script `JSON.stringify()`-encoded (a strict subset of Python's own escaping) rather than hand-rolled triple-quoting.

**`db`: a fresh in-memory `sqlite3.connect(":memory:")` connection**, created at boot and on every reset.

**The bug this caught before it shipped:** the rarely-used main-thread fallback got `db`, but the Worker path most sessions actually take — shared with hosted tutorial pages — carries its own separate copy of the seed source and was never touched, so `db` would have been silently absent for almost everyone. Fixed by gating a new worker-side seed source behind a `seedDb` flag set only by dewmini's own boot message.

**Verified in a real browser**, since the point was interoperability no Python-only test could prove: a multi-statement script renders only the final result with no duplicate; a Python cell reading `db` sees exactly what a SQL cell wrote; the worker-mode wiring specifically (not only the fallback) actually took effect.

*Cost to change: the sql.js redirect cost nothing already spent — caught before a build ran against it. JavaScript, next, does not get this same discount: a persistent sandboxed session is a real second runtime.*

**7.119 — JavaScript, the fourth and last of the four new cell types, built in dewmini — and a redeclaration bug in its own design doc, caught by actually running the code.** `compose/js-cell-engine.js` plays the role `pyodide-engine.js` plays for Python — one persistent session, created lazily, needing no Worker: a sandboxed `<iframe sandbox="allow-scripts">` with no `allow-same-origin` is already a memory-isolated realm with its own JS engine. No Stop button exists here, since the iframe runs on the tab's main thread.

**The bug:** the design's first draft said code gets "posted into that iframe and evaluated there," read as inserting a `<script>` tag — wrong, because a `<script>` tag's top-level `let`/`const` join the realm's one permanent global environment, so re-running an edited cell throws a redeclaration error. Not caught by reading the design; caught by actually re-running a `let`-declaring cell in a browser.

**The fix: indirect `eval`, `(0, eval)(code)`.** Its top-level `let`/`const` live in a scope private to that one call, so a cell can always be re-run — at the cost of those bindings no longer visible to a *later* cell. Only `var`/`function` still persist across cells: a real, named gap from what the design promised, documented plainly (without JS jargon) in the design doc, the engine's file banner, and dewmini's help panel. A proper fix needs a real JS parser, out of scope here, the same trade SQL made with its plain-split parser.

Indirect eval also simplified error handling (a synchronous error caught directly around the `eval()` call); an unhandled promise rejection still needs a `window` listener, since it fires after `eval()` returns. Top-level `await` stays unsupported, since wrapping code in an `async` function would swallow its own top-level declarations into that function's scope.

**Wiring** reuses `applyOutputEvent()` (exported from `pyodide-engine.js` rather than duplicated) for output, since both engines share a realm with `dewmini.js` and the same cellId lookup. `runCellBatch()` only boots each cell's engine right before its own turn, so an all-JavaScript batch never downloads Python.

**Verified in a real browser:** re-running an unmodified `let`-declaring cell without error, `var`-declared state surviving into a later cell, Restart confirmed by checking a previously-`var`-declared name reads back `undefined`, a mixed Python+JavaScript "Run all." Nine new e2e tests cover the same ground.

*Cost to change: real, unlike SQL's — a persistent sandboxed session plus its own message protocol is genuinely new surface. The redeclaration bug is the clearest evidence yet that verifying in a real browser is not optional once a genuinely new execution model is involved.*

**7.120 — HTML and CSS, retired as separate types and merged into one: Web.** Not a bug fix — both worked as designed on their own. The merge came from using both: a CSS cell could only ever style a fixed sample page, never a reader's own markup, and an HTML cell had no CSS of its own reachable at all — a pairing 7.117's design had explicitly declined to guess at. One cell with both halves removes the question rather than answering it differently.

**What changed.** `CELL_TYPES.WEB` replaces `HTML`/`CSS`. A cell gains a second content field, `style`, alongside `content` (now HTML) — the first time any dewmini cell needed two independent source fields, touching cell creation/duplication, save/restore, and a new `destroyCellEditors(cell)` helper replacing six separate teardown call sites.

**Two editors, always both visible, one Render button** rather than auto-render-on-blur (which would double-fire for one edit). `READ_NOT_RUN_TYPES` narrowed to Text alone. An empty HTML half still falls back to the fixed sample page, so the old standalone-CSS use case still works.

**Migration: each old cell becomes its own new web cell, never merged with a neighbour.** `migrateLegacyCellType()` maps a standalone HTML cell to a web cell with an empty CSS half and vice versa — deliberately not smarter than that, since guessing that a neighbouring pair was meant together risks silently combining cells a reader didn't intend combined.

**Export paths that would have silently dropped the CSS half** — all three export paths used to read only `cell.content`. A new `cellExportContent(cell)` helper folds a non-empty CSS half into the exported text for all three.

**Verified in a real browser:** both editors independently editable with no toggle; a CSS rule genuinely styling the same cell's own HTML; Render staying inert until clicked; reload persistence for both halves; the migration path itself. Ten e2e tests replace the eleven the two old types had, covering more.

*Cost to change: smaller than SQL's or JavaScript's — no new engine or sandboxing model. The real cost was breadth: six teardown call sites, three export paths, a data migration, and every doc/design surface that named HTML and CSS as two things rather than one.*

**7.121 — Site: an .html file opens as a small website, on the same mounted filesystem — and a first design for it, built and then thrown away before it was ever committed, because `main` had moved underneath it.** The follow-on from 7.116–7.120: dewmini can run HTML, CSS and JavaScript separately; showing them together as three real files, not three cells, is the obvious next step.

A first version was built directly on this branch's own base, with a fixed `site/index.html`/`style.css`/`script.js`, a bespoke Workbench section with its own load/save/debounce plumbing, and the three files hidden inside a `site/` subfolder so Files' flat list wouldn't show them. Checking `origin/main` before committing found it had moved three commits past this branch's base in the meantime — a notebook-as-one-Python-file view, Files becoming a real file manager with open/write-back/rename, and a rail-position swap — producing real conflicting edits, resolved by hand keeping whichever side had become more complete.

**Why the first version was abandoned rather than merged forward.** Main's file-manager commit already builds almost exactly the "open into a tab, edit, debounce a write back to the real filesystem" mechanism the bespoke Site panel was reinventing. Building Site as its own section made sense only while Files couldn't open anything — once it can, a second open/edit/save path next to it is duplication.

**What shipped instead: a third tab kind, not a fourth panel.** `VIEWS` gains `SITE` alongside the existing `CELLS`/`FILE` enum. `openWorkspaceFile()` now also accepts `.html`, looks for a same-base-name `.css`/`.js` beside it (base-name pairing, not three fixed names), and opens a tab with no cells. The three files' live text sits directly on the notebook object, persisted the same "localStorage cache, debounced real write" way `.path` already is. The HTML file is always written; CSS/JS only once there's something in them. Neither sibling file needs to exist for the tab to open.

**Split screen, not a Render button** — editors on one side, a live sandboxed iframe on the other, updating on every keystroke: a site is something a reader keeps looking at continuously while building it, unlike a Web cell's one-shot question. The Python-notebook-only toolbar buttons hide themselves behind one shared class for a site tab.

**One CSS bug worth naming, because it recurs:** hiding those toolbar groups via the `hidden` attribute did nothing, since an author stylesheet's `display: flex` always beats the browser's own `[hidden] { display: none }` rule regardless of specificity — fixed with the same explicit `[hidden]` override every other conditionally-hidden element in this file already carries.

**Verified in a real browser:** opening an `.html` renders a live split-screen preview; a sibling `.css`/`.js` pair opens beside it and all three reflect in the preview; a lone `.html` with no siblings still opens; the CSS/JS halves write back to their real files, readable from a Python cell elsewhere; a site tab survives reload. Seven new e2e tests, one needing a longer wait since two debounces stack before a site's file is durable on disk.

*Cost to change: mostly absorbed by main's file-manager commit already having built the mechanism this reuses. The real cost was the false start — a working, tested implementation built and discarded because it was designed against a base three commits behind the one it needed to ship against. The lesson: a design decision made while a sibling branch is landing large, overlapping surface area has a short shelf life.*

**7.122 — Five smaller things, from actually using what 7.116–7.121 built: a cell-type toggle, a real notebook location, two layout bugs, and one CSS trap caught twice in one session.**

**Web and SQL cells default off, behind a per-type Settings toggle.** Not every reader wants all four new cell types offered on every seam. Web and SQL start off, JavaScript starts on, Python and Text carry no toggle — they are the notebook, not an extra. The toggle only gates what `createInsertDivider()` offers next; a cell already in the notebook keeps showing, running, and exporting regardless of its type's current toggle state.

**A notebook now shows up in Files, without writing it to disk.** A notebook holding cells had nowhere to show up in Files at all, and writing every notebook out as a real file on the mounted filesystem would mean booting Pyodide on every page load — against the project's own "nothing opens on a first visit" rule. `renderNotebookList()` instead lists every open notebook with no `.path` directly in the Files panel (labelled as living in this browser), drawing instantly with no filesystem read. A notebook already backed by a real file is excluded, since it already appears under its own name.

**Two layout bugs found by screenshot, not by reading CSS.** Library and Workbench opened 3rem wider than Settings by default — fixed to match on dewmini's side rather than touching the shared rule every tutorial page's Settings also uses. The per-cell "⋯" menu could run off-screen once its button sat close to the edge — fixed by measuring its own bounding rect after becoming visible and flipping to a left-anchored class when it would overflow, rather than predicting in advance.

**The same CSS trap, twice.** The Site tab's note reused a class written for a row-flex parent inside a column-flex wrapper, so it flex-grew to fill the whole column — given its own class instead. And `.dm-toolbar-group`'s `display: flex` again silently beat `[hidden]`'s `display: none` for the cell-type toggle's Settings groups, fixed the same way as 7.121's own instance of the identical bug.

*Cost to change: each small in isolation, none architectural. The pattern behind all five: every one was found by using the just-shipped feature in a real browser, not by re-reading the code that built it.*

**7.123 — Two accessible reading fonts, and a High contrast switch that is its own toggle rather than a sixth font choice.** Framed directly: "high contrast means font and colours as a toggle" — one switch changing two things together, not a new entry in the Font row. Atkinson Hyperlegible (Braille Institute of America) and OpenDyslexic sit as two ordinary Font choices; High contrast is a second, independent row forcing a black-on-white (or reversed in dark theme) palette and Atkinson Hyperlegible specifically, regardless of whichever font a reader separately picked.

**Self-hosted, not a Google Fonts `<link>`** — this is exactly the offline bundle a CDN link would leave broken, and this sandbox's own network policy blocks `fonts.googleapis.com` outright (confirmed with `curl`). Both fonts come from `@fontsource` packages, vendored like every other pinned asset, four faces each — the minimum for bold/italic markdown to render as a real face. The woff2 files land flat in `vendor/fonts/` beside KaTeX's own, reusing `standalone_html()`'s existing `FONT_URL_RE` inlining step unchanged rather than needing a second copy of the regex.

**Shared with every tutorial page, not dewmini-only** — `data-font`/`data-contrast` live in the same shared reading-preference system every dewlab page uses, so both new fonts and the contrast switch went into `assets/shell.html` as well as `compose/dewmini.html`. **`dewmini.js` duplicates this mechanism rather than importing it** — the first attempt at wiring the contrast toggle only touched the shared file and did nothing in a real dewmini page, caught by watching the CSS variables stay unchanged after clicking the toggle in a real browser.

**Two tests needed narrowing, not the behaviour changed:** one broke outright on an unhandled new stylesheet link (fixed by inlining the accessible-fonts CSS the same way KaTeX's is); one asserted no font data at all on a maths-free page, true only because KaTeX's fonts were previously the sole source of that marker — narrowed to look for a KaTeX-specific class rather than a family name the page was already carrying regardless.

*Cost to change: real but contained — wiring the toggle rode entirely on an existing generic sync mechanism needing one new key. The one real trap: a shared mechanism that has been duplicated needs its fix applied twice, and only a real browser catches the copy that was missed.*

**7.124 — High contrast redefined four variables and called it done; turning it on and looking said otherwise.** Reported the day after 7.123 shipped: it touched only `--dl-fg`/`--dl-bg`/`--dl-muted`/`--dl-rule` and the font, on the unstated assumption that body text was the whole of "can I read this." A heading, a link, a cell-type pill, a cell's border, a pass/fail message each have their own variable, untouched. Measured with WCAG's contrast formula: `--dl-link` at 3.6:1 was failing the *ordinary* AA minimum (4.5:1), let alone the ~7:1 AAA the toggle exists to promise; `--dl-cell-border` at 1.4:1 was worse, against a 3:1 floor for a graphical boundary.

**Fixed by moving each colour, not replacing it** — asked directly whether to flatten everything to black/white or keep the hue and fix the ratio; kept the hue, so a returning reader's learned colour associations (teal=SQL, purple=HTML) survive the toggle too. Each failing colour was darkened/lightened along its own hue until it cleared 7:1. `--dl-cell-border` is the exception: a boundary carries no signal worth preserving, so it borrows `--dl-rule` outright.

**The bug worth naming: an inline style beats a stylesheet, always, regardless of specificity.** `--dl-link`'s new rule did nothing because the texture panel's own reader-settable link colour is written via `root.style.setProperty()` — an inline style on `<html>`, which the cascade always prefers over any stylesheet selector. Fixed at the source: `applyTexture()` now skips (and removes) that inline write while high contrast is on.

**The second copy, found the same way the first one was (7.123)** — `tutorial-runtime.js` carries an identical `applyTexture()`, needing the identical fix, found by testing a tutorial page after fixing dewmini and finding the link colour still wrong there.

*Cost to change: small in lines, real in the lesson — a claim about what a toggle does is worth nothing until the toggle has actually been turned on and looked at, and a duplicated mechanism stays duplicated for every fix aimed at it, not only its first.*

**7.125 — Opening a plain `.py` file in the File view silently turned it into something that looks like a dewmini export.** Writing a markerless script from a cell, then opening it in the File view, showed it *with* a `# %%` marker already added, before a keystroke — and saving from there wrote that marker to disk permanently. The cause: `cellsToPercentText()`, used both by the File view's display and by save-back to a notebook's own path, always put a marker before every cell even a lone one, though `parsePyCells()`'s own markerless-file fallback already made that unnecessary for a single cell.

**Fixed at the two call sites that reflect a real file, not at the function itself.** `cellsToPercentText()` took a `bare` option: on, a lone cell serializes with no marker. `writeNotebookToWorkspace()` and the File view's editor seed both pass `bare: true`. `downloadAsPython()` was deliberately left on the default — it carries its own second mechanism (an explanatory header above the first marker, stripped back out on reimport by checking for it) that only makes sense with a marker present to mark where the header ends; applying `bare` there broke the export/reimport/export regression test, since a markerless file with the header inline fell into the single-cell fallback and read the header back as content.

**Verified:** a markerless file stays markerless through open/edit/save; a genuine multi-cell file keeps all its markers; the export/reimport regression test passes again once `downloadAsPython()` was excluded.

*Cost to change: one parameter and two call sites, once two false alarms elsewhere were ruled out as flaws in the test script, not the product. A single serialization function fed by more than one caller does not mean one caller's needs generalize to the others.*

**7.126 — A long Settings label wrapped into a narrow ribbon, most of its own row sitting empty beside it.** "Show progress on the tutorials list" broke across four cramped lines because `.dl-texture-row`'s grid (`4.6rem 1fr`) was sized for one-word labels; a longer label wraps inside its own column instead of borrowing room from the wide one beside it. Two more rows ("Remind me to export new notes", "Web (HTML+CSS)") were found wrapping the same way once the shape of the bug was known, by grepping every row's actual label rather than guessing which looked long.

**Fixed with a modifier rather than widening the shared column.** A `.dl-texture-row-wide` class drops to a single `1fr` column so the label stacks above the toggle instead of beside it — applied only to the three affected rows, since widening the shared column would have pushed every short-label row's toggle rightward for no reason.

*Cost to change: five lines of CSS and three class attributes. A component built for the common case needs a second look the moment real content is longer than the case it was designed around.*

**7.127 — Atkinson Hyperlegible swapped for Lexend, on Josh's own call after using both.** Not a bug — Josh preferred Lexend (Google's font built to reduce reading-difficulty complexity) over Atkinson Hyperlegible after trying both, and wanted High contrast to force Lexend too.

**Vendored the same way, with one real difference the switch surfaced: Lexend ships no italic face at all** — only regular and bold from `@fontsource`, versus the other two fonts' four faces each. `ACCESSIBLE_FONTS` now lists each font's own faces rather than assuming one shared list; a page asking for italic Lexend gets the browser's synthetic slant, the same fallback any font missing that face gets.

**The rest was a name swapped in four places** once the CSS rule was renamed — the `data-font` value, the Font row's button, and High contrast's forced font. No JavaScript changed, since `data-font` is read/set generically with no fixed value list. A reader with the old value saved falls back gracefully to the base rule, same as any unrecognised value.

*Cost to change: small, once the italic gap was found. `ACCESSIBLE_FONTS` no longer assumes every accessible font ships the same four faces the first two happened to share.*

**7.128 — A cell left blank vanished the moment the File view was opened and closed again, with nothing said about it.** Insert a fresh cell, glance at the File view, switch back, and the cell was gone — the same happened to a cell a reader had cleared mid-edit, losing visible work.

**The cause: `parsePyCells()`'s `flush()` kept a cell only `if (content.trim())`** — correct for a genuinely empty document, but also true for a stretch between two real markers with nothing typed yet; both trim to the empty string and `flush()` couldn't tell them apart.

**Fixed by making the marker itself the signal, not the content.** A marker line sets `currentType` away from `null`; `flush()` now keeps whatever it collected once that's happened, blank or not, dropping a blank stretch only when `currentType` is still `null` (the case with no marker asking for a cell at all).

**A narrower edge case was left alone, on purpose** — a notebook of exactly one blank cell serialized `bare` (no marker) still reads back as zero cells, since an empty file and "one empty cell" are genuinely the same bytes with no marker to distinguish them.

*Cost to change: one condition in one function. A parser that reads "no content" as "no cell" is only safe when there is truly no other signal — once a format has an explicit marker, that marker is the thing to trust.*

**7.129 — Three comments in `compose/dewmini.html` described the Library/Workbench/Settings panels' own docking backwards.** Found during an open-ended review, not a visible bug. The toolbar-order, Library, and Workbench comments each claimed the wrong docking side — checked against the actual CSS and `wirePanel()`'s conflict list, Library and Settings are the two right-docked panels sharing an edge, and Workbench is the one left-docked panel, free beside either.

**Fixed by rewriting each to cite the actual mechanism** (`wirePanel()` and its `conflicts` list) rather than restating a claim. No behaviour changed — only the prose was wrong.

*Cost to change: three comments, once actually checked against the code rather than trusted on read. A comment that claims a wrong thing confidently can sit uncorrected for a long time, since nothing tests it.*

**7.130 — Every segmented control in Settings announced itself to a screen reader as a row of independent toggle buttons, when picking one option always deselects the others.** About two dozen `.dl-seg` groups (Theme, Font, Width, Density, Cursor, …) read out as independent pressed/not-pressed buttons, with nothing telling a screen reader they formed one mutually-exclusive group — inferred at a glance by a sighted reader, invisible otherwise.

**The cause: `aria-pressed`**, correct for an independent toggle and wrong for a mutually exclusive set — copied to every new `.dl-seg` group because the first one written used it and nothing since questioned it. WAI-ARIA has a purpose-built radiogroup pattern, unused here.

**Fixed by moving every `.dl-seg` onto the APG radiogroup pattern:** `role="radiogroup"`/`role="radio"`, a label via `aria-labelledby` or `aria-label`, `aria-checked` in place of `aria-pressed` through two small shared helpers, and roving tabindex so the checked (or first) button is the group's one tab stop. A single keyboard-nav function adds arrow keys and Home/End, each routing through the same `.click()` a mouse uses so the two paths can never disagree.

*Cost to change: two roles and a label per group in the HTML, one attribute rename and one small helper in the JS, written once and reused. `aria-pressed` and a radiogroup's `aria-checked` render identically on screen, which is exactly why the wrong one went unnoticed long enough for every later group to copy it.*

**7.133 — A large plotted figure could blow this browser's storage quota and cost a reader their code and notes along with it, not just the figure.** Every matplotlib figure is embedded as a base64 PNG straight into a cell's output HTML — easily a few hundred KB. `saveNow()` writes one JSON record covering every cell's code, output, and notes with a single `localStorage.setItem()`; when that throws because the record is now too big, the whole save failed silently except for a line in Settings a reader would have to go looking for. The previous saved value is untouched, so the real damage was ongoing: every future autosave kept failing the same way while the oversized output remained, silently discarding new code and notes from that point on.

**Fixed with a retry inside `saveNow()`'s existing `catch`:** on failure, check whether any cell's output is over a threshold (100,000 characters) and, if so, save again with just that cell's output blanked rather than dropping the whole record. A blanked output restores as "not run," so a reader gets the figure back with one more Run press. Only if the slimmed record still doesn't fit does it fall through to the original all-or-nothing message. The new message names what happened rather than repeating a generic one.

*Cost to change: one length check and one map inside an already-existing `catch`, no new UI. `localStorage.setItem()` either writes the whole new value or leaves the old one alone — not the transaction most code assumes until a failure path is actually read closely.*

**7.131 — Three more small accessibility gaps in the reader's own runtime, found in the same review that turned up 7.130.** None crashed or looked wrong on screen — all three only showed up to a keyboard or a screen reader.

**A collapsed cell's one-line summary was a `<div>` pretending to be a button** — `tabindex="0"` and a click handler, but no `role="button"` (so a screen reader announced it as plain text) and its keydown handler only checked Enter, not Space. Fixed with `role="button"` at all three markup sites and Space added to both keydown checks.

**The "⋯" run menu was the one panel on the page that didn't close on Escape**, unlike Settings, Reference and SeriesNav, which all already do. Added the same pattern: Escape closes the menu and returns focus to its button.

**A cell finishing a run said nothing to a screen reader.** The run-line ticker is deliberately not a live region (ticking noise), but nothing replaced it with an announcement on completion. Added one shared visually-hidden `role="status"` region, updated once a run completes ("Ran — output below" or "Ran — error"), cleared first and set a tick later so running the same cell twice in a row still announces the second time.

*Cost to change: an attribute and a key check for the fake button, one keydown listener matching three already-written ones, one hidden live region. None needed new UI — every element was already interactive, just only fully for a mouse.*

**7.132 — dewmini's own run announcement had 7.131's "same result twice in a row" bug, not 7.131's original gap.** dewmini already announced every run via `updateStatus()` writing into its own live region — it just lacked 7.131's fix for the narrower bug underneath: setting identical text twice in a row (e.g. "Ran." after two successive runs) is invisible to a live region. Fixed inside `updateStatus()` itself: when the incoming message equals what's already showing, clear it and set the real text a tick later, the same pattern 7.131 used elsewhere. Every other call, where the message differs, keeps its exact previous synchronous behaviour.

*Cost to change: one branch inside one already-existing function. The task this was filed as ("dewmini has no run announcement") was wrong — it already had one — and the real gap only turned up by reading the code directly instead of trusting the title on the task.*


## Phase 8 — Student feedback pathway

Planned in an artifact worked through with Josh before any code existed:
GitHub already has the receiving end (Issues, an issue form, labels, a
Project), so the gap was at the student's end, and the further choice to
teach the account rather than route around it, since dewstack's students
already make one and dewlab's own reporting document already assumed one.
This phase is the first slice of that plan: a link on every page, the
issue form it opens, and a switch to turn the link off. The "three doors"
panel, the cell-level report button with code capture, and the two new
debugging/GitHub-reading tutorials are deliberately not part of this
slice — see the artifact for the fuller design and why they were held
back.


**8.1 — The kill switch is a YAML file, read fresh on every call, not a
`build.py` constant.** `planning/feedback.yaml` holds one key, `enabled:`,
read fresh from `ROOT` on every call (matching `module_order()`'s
reasoning, ARCHITECTURE.md §1 step 5) rather than as a module-level
constant, so a test's temporary `ROOT` is seen. Missing the file, or
missing `enabled:` inside it, both mean on: the switch exists to make
turning the link off fast, not to make on the careful path.
*Cost to change: trivial. One file, one function, six call sites of
`site_footer()` that already pass it a page.*

**8.2 — Every page gets a report link, not only tutorial pages.** The
contents page, topic tree, "browse by topic," About page, and the editor
all call `site_footer()` with their own slug and version, the same as
their existing `{{SLUG}}`/`{{VERSION}}` tokens — a bug in the editor or
topic tree should be no harder to report than one in a tutorial.
*Cost to change: small — dropping a page from the list is removing one
call site's arguments.*

**8.3 — The prefilled link carries only `page` and `version`; browser and
the cell's code are not captured yet.** `report_issue_url()` builds a
GitHub "new issue" address from these two query parameters, matching the
two fields in `.github/ISSUE_TEMPLATE/report.yml` marked "filled in for
you." Browser/device and a cell's current code/output need JavaScript on
the page (the report panel, not yet built) to capture automatically; the
issue template's `kind:` dropdown already has a "gives an error" option
so a student can name the check they tried without it.
*Cost to change: small on its own — adding fields to `report_issue_url()`
and the template is additive — but the report panel and the cell-level
button both need to exist before those fields can fill themselves in.*

**8.4 — The "three doors" choice is a static `<details>` disclosure, not
JavaScript.** A question needs sorting away from a bug report before it
is sent, since it is the wrong container for whoever answers it later.
`report_doors_html()` renders three plain links inside a
`<details>`/`<summary>`: a question to `/discussions/new`, and two to
`report_issue_url()` with `kind` set to one of
`.github/ISSUE_TEMPLATE/report.yml`'s dropdown options, matched exactly
so GitHub pre-selects it. Revealing the list pushes the footer down in
normal flow — the same shape `.dl-hint-text` uses — rather than a
floating dropdown. `report_issue_url()` gained an optional third
argument, `kind`, backward compatible with its two existing call sites.

The Discussions link ships live even though Discussions itself is still
off for both repositories (a manual switch, not code), so it 404s until
that switch is flipped — correct once it is, with nothing to remember to
add later.
*Cost to change: small. The two option strings are the coupling point
between `build.py` and the issue template — a wording change to one
without the other, and `test_report_doors_html_kinds_match_the_issue_template`
catches it.*

**8.5 — The cell-level report control is an icon, not a fourth button,
and its panel is filled in at open time, not build time.** It sits as
`.dl-report-icon`, the same small circular toggle as `.dl-hint-icon`
beside it, rather than a fifth `.dl-btn` crowding the cell bar. Its panel
(`.dl-report-doors.dl-cell-report-doors`) opens as a plain block after the
bar, the same push-down shape `.dl-hint-text` uses, reusing
`report_doors_links()` — the inner half of the footer's own three-doors
markup, split out so both call sites share it.

`page`, `version`, and the cell's own id are build-time constants,
threaded through `place_blocks()` from `load()` into `render_cell()`. A
cell's current code and its last output are not — they depend on what
the reader has typed and run, which doesn't exist until their browser tab
does. Those two fields ship blank from `build.py` and are filled in once,
at the moment the panel opens, by `updateCellReportLinks()` in
`tutorial-runtime.js` — not kept live on every keystroke, since nobody
reads a report link before opening the panel. `report_doors_links()`
marks its two issue links with `class="dl-report-issue-link"` so the
runtime can select them without re-parsing `href`s, distinguishing them
from the Discussions link, which needs no code or output.

A custom cell (the reader's own, created at runtime) gets none of this —
there is nothing to report about code nobody but the reader wrote.
*Cost to change: moderate. Two files agree on the shape of a report link
now (`build.py`'s markup, `tutorial-runtime.js`'s
`updateCellReportLinks()`), and the `dl-report-issue-link` class is the
seam between them — rename or restructure one without the other, and the
runtime silently stops finding anything to update.*

**8.6 — A written triage procedure, and a one-shot scheduled off switch,
both added before the first real report arrives.**
`.claude/skills/triage-report/SKILL.md` sets the inbox procedure: read
before acting, re-sort the student's guessed `kind` rather than trusting
it, reproduce an error report from `code`/`output` before touching
anything, and two hard stops — a maths or curriculum question is Josh's
call, and nothing closes without a person having looked.

`.github/workflows/auto-disable-feedback.yml` turns the doors off on
Tuesday, 2026-09-08, without anyone having to remember to. It is a
genuine one-shot (the date is cron's day-of-month/month fields, not
day-of-week), and its last step deletes its own workflow file in the same
commit that flips `planning/feedback.yaml`, so nothing is left to misfire
next year. `workflow_dispatch` on the same workflow doubles as a manual
"turn it off now" trigger — a real alternative to editing
`planning/feedback.yaml` by hand, not a test mode.
*Cost to change: trivial for the switch itself (edit or delete the
workflow file, the same as any other scheduled job). Extending the
deadline means editing the cron date before it fires, since the file
that would let you edit it again is gone once it has.*

**8.7 — Labels are created by a workflow, at the moment they are first
needed, rather than by anyone clicking through GitHub's settings.** An
issue form's own `labels:` key can only apply fixed text — it cannot know
in advance which page or which kind a report will name. `label-report.yml`
fires on every newly opened issue and calls `dev/label_report.py`, which
reads the issue back through GitHub's REST API, parses its rendered
fields (the `### <label>` pattern GitHub always renders an issue form's
fields as), and applies a `page: <slug>` and a `kind:
<error|unclear|question>` label — creating either the first time it is
used.

`report-patterns.yml` runs weekly and calls `dev/report_patterns.py`,
which re-derives page and cell from the same parsed fields (the fields
are the one source of truth, not the labels above) and opens or updates
one `pattern` issue per page that crosses a threshold: three open reports
on the page, or two on one cell, within a fortnight. A hidden
`<!-- pattern-key: <page> -->` marker is how a second run finds the issue
it already opened rather than doubling it; the body is replaced wholesale
each run, so a pattern issue reflects the current count, not the count
from its last run.

Both scripts talk to `api.github.com` directly with `urllib`, matching
every other `dev/` script's "no dependency beyond the standard library"
rule. The parsing logic (`parse_fields()`) is duplicated between the two
files on purpose, so each script stays readable and runnable on its own;
`tests/test_report_patterns.py`'s `test_label_report_uses_the_same_parser`
guards against the two copies quietly diverging.
*Cost to change: small for the thresholds themselves (two named
constants). Changing what counts as a "page" or a "cell" means changing
the field-label strings in both scripts and in
`.github/ISSUE_TEMPLATE/report.yml` at once, or the parser silently stops
finding what it is looking for.*

**7.134 — dewmini's Site view gains a console under its preview, and its
JavaScript pane runs on Run rather than on every keystroke.** Until now a
site's script that threw did the one thing a learner cannot read: the
preview stopped changing, with no message anywhere.

Ported in shape from dewstack's site editor. **HTML and CSS stay live**,
because a stylesheet is a state and the lesson is watching the box change
under your hand; **JavaScript runs when asked**, because a program is not
a state and half-typed code is a syntax error on most keystrokes — a
console flashing red between characters would teach a reader to ignore
it. Until Run (or Ctrl/Cmd+Enter inside the pane), the preview keeps the
last script that ran, so retyping a colour does not silently re-run a
half-edited program.

**The mechanism:** a small ES5 relay (`SITE_RELAY`) goes into the preview
document's head ahead of the reader's CSS, replaces `console.log` and its
siblings with versions that also `postMessage` to this page, and listens
for the window's `error` event (uncaught runtime errors and inline syntax
errors alike) and `unhandledrejection`. Line numbers arrive relative to
the whole `srcdoc`, so `buildSiteDocument()` records where the HTML and
JavaScript panes start and the console subtracts, naming the pane and its
line; a Go to line button selects that line in the right editor. Under
the browser's message, a plain-language second line for the four errors a
first term meets most (`SITE_FRIENDLY`), styled like `_ERROR_HINTS` gives
a Python traceback. `</script` typed into the pane is escaped rather than
ending the script element.

**One bug carried from dewstack's twin:** several synchronous `srcdoc`
writes in one task loaded only the *first* document in a real Chromium,
so a site opened on an empty preview. The Site view now treats the frame
as one resource: a document is written only once no earlier one is still
loading, later ones wait, newest wins, and the frame's load event flushes
the next — coalescing on load rather than on a timer keeps a fast
typist's last keystroke from being the one dropped.
*Cost to change: `renderSiteView()` grew by the relay, the assembly
arithmetic and the console; the CSS by a preview column. The friendly map
is data. Not shared with dewstack as a file — "port in shape" stays the
rule between the two repositories — so a wording change there is a
change to make here by hand, and the banner on each names the other.*

**7.135 — Staged hints: a fold that waits for an attempt.** After an
error recurs, a "pause and ponder" fold can appear with a question, and
later another with steps — inviting habits rather than giving commands.
`planning/CELL_HINTS.md` is the design note; this entry records what was
built.

**The authoring surface is a fence, not HTML.** A ```` ```hint ```` fence
after a cell, with optional `for:`, `after:` and `title:` headers in the
same `key: value` shape the exec cell uses — chosen because it survives
the Milkdown editor, which keeps only a fence's first word. Defaults: the
exec cell above, `5 errors`, *Let's slow down a moment…*. `after:`
accepts both `5 errors` and `errors:5`, canonicalised to the second and
rejected if unknown. A cell may carry `expect:`, a Python expression
checked after each run; once it holds, no further hint appears. A
fence's body converts separately (`render_staged_hint()`), because
Python-Markdown treats a `<details>` block as raw HTML — the same reason
hand-written `dl-hint` folds had been shipping markdown as literal text
(§12 of the design note, not fixed here).

**What the runtime counts, and what it never shows.** `run_cell_report()`
returns each run's outcome (raised or not, exception type/first line,
whether `check()`/`expect` hold); `tutorial-runtime.js` keeps per-cell
counters from it — runs, errors, consecutive identical errors, unchanged
code, failed checks, time since first run. At most one fold appears per
run, with a dot on the cell's bar until opened and one sentence for a
screen reader. No count is ever shown — a number on a cell reads as a
verdict regardless of caption (`PEDAGOGICAL_STYLE_GUIDE.md#no-verdicts`). `run_cell()` still
returns a boolean, since dewmini and `pyodide-engine.js` depend on that.

**What clears nothing.** A hint once shown stays; Reset keeps the
counters (a reader resetting code is still stuck); two Settings rows
control whether hints appear at all (default on) and whether Restart
Python hides them (default keep). Counters and revealed folds travel in
the saved-work record.

**The first fold asks, not tells.** The style guide's new subsection on
hints (now `PEDAGOGICAL_STYLE_GUIDE.md#stuck`) sets three stages — a question, then steps, then the shape of the code,
never the answer.

Written first in `finding-where-it-went-wrong`, `grid-of-numbers`
(computational methods), `the-moves-you-already-know`,
`testing-what-a-class-does` (FOOP). dewstack's own half is designed but
not yet built.
*Cost to change: two attributes and a fence in `build.py`; one report
function in `tutorial_tools.py`; ~250 lines in `tutorial-runtime.js`; two
Settings rows; a CSS block. The grammar is a table (`TRIGGER_KEYS`).*

**7.136 — A tutorial page's Python cell and a dewmini cell, made to
match.** A single cell's chrome and behaviour should feel the same
wherever a student meets it — not the whole platform, just one Python
cell. `planning/CELL_IDENTITY.md` §9 is the design note.

Four mismatches fixed: Run sat after the output on a tutorial page and
between code and output in dewmini — `render_cell()`'s three rows
reordered to match, `createCustomCellElement()`'s hand-built copy along
with it. Reset (destroys typed code) and dewmini's Clear (only clears
output) looked like the same button doing different things — now a
clockwise ↻ with a red-ish border against dewmini's unchanged
counterclockwise ↺. A tutorial page's buttons were plain words and
dewmini's were bare icons — now both carry an icon and a label
(`icon_button()`/`iconButtonHtml()`/`iconButton()`, one
`.dl-btn-icon`/`.dl-btn-label` pair regardless of page) behind one new
shared Settings row, "Cell buttons" (icons, text, or both), riding the
existing Texture panel's `"dewlab:texture"` key rather than a setting of
its own. dewmini's own traceback named a cell by its internal id, now by
whatever `label` `run_cell()` was given — a reader's own name or `Cell
N`, never the id.

Alongside those: a name beside the identity pill — `name:`, a fourth cell
header line, on a tutorial page's authored cells, and a genuinely
editable `<input>` next to the pill on every dewmini cell, since a
dewmini cell is already the reader's own.

Two real bugs turned up in code this work never touched but only now had
reason to exercise end to end: a reader's own custom cell threw the
moment it was run, because `noteAttempt()`/`maybeRevealHint()` (7.135's
staged-hints counters) read `cell.attempts`/`cell.hints` unconditionally
and a custom cell had never been given either; and `applyOutputEvent()`,
the worker path's output router, searched only `cells`, so a custom
cell's own output was silently dropped the whole time staged hints has
existed. Both fixed with `cells.find(...) || customCells.find(...)`, the
pattern `downloadAsIpynb()` already used.
*Cost to change: `render_cell()` rewritten to three rows
(`.dl-cell-head`/`.dl-cell-body-row`/`.dl-cell-footbar`), mirrored by
hand in `createCustomCellElement()`; a `label` parameter through
`run_cell()`/`run_cell_report()`/`_begin()`/`_CellContext`/
`cell_filename()` and both JS engines; a `name`/`nameEl` field on both
cell models; one Settings row shared by both pages' Texture machinery;
`setBtnLabel()`/`getBtnLabel()` helpers in each file (markup, not a
shared component). Two unrelated, pre-existing e2e failures surfaced
during this pass and were left alone —
`test_cell_hints_staged.py::test_opening_the_fold_clears_the_marker` and
`test_phase0_golden_path.py::test_python_started_with_no_console_errors`
— neither touches code changed here. PR: deweydex/dewlab#163.*

**7.137 — Two real bugs in 7.136, caught by a second review after it
merged.**

**A cell's own code could be misread as its `name:` header.** `name`
joined `id`/`hint`/`expect` in `HEADER_RE`'s alternation, matched against
a cell's first lines regardless of whether they are actually a header —
the same shape a type-annotated assignment has. `name: str = "Ada"` as a
cell's first line was silently stripped out and stored as a garbage pill
label instead of running; `print(name)` on the next line then raised
`NameError`. `id:`/`hint:`/`expect:` share the same theoretical ambiguity
but never collide with real code in practice; `name` is a bare identifier
common enough in ordinary code that it always would. Fixed without
touching the `key: value` header shape itself: a `name:` line whose value
contains `=` was never a header — a real name is a short label, never an
expression — so `parse_cell()` checks for that character before consuming
it, and reads the rest as code instead.

**`cell_filename()`'s docstring claimed something the code didn't do.**
It said a label only changes what a reader *sees*, and that an id "still
decides `linecache`'s key" — false: the function returns `label or
cell_id` as the whole filename, so a label replaces the id everywhere,
`linecache`'s key included. Unlike an id, a label isn't guaranteed
unique, so two same-named dewmini cells share one `linecache` entry — but
`_register_source()` always re-registers a cell's source immediately
before it runs and `_format_exception()` always formats its traceback
immediately after, before any other cell gets a turn, so a run's own
traceback always reads back correctly regardless. The docstring now
states this honestly instead of the wrong, stronger uniqueness claim; the
code was already correct.

Neither bug shipped to a student: the first only bites a tutorial author
previewing their own build (both the pill and the failure to run are
immediately visible), and the second never manifested given how the
module runs today. `docs/WRITING_TUTORIALS.md` never documented `name:`
at all — added alongside, with the `=` rule spelled out for authors.
*Cost to change: one `if` in `parse_cell()` (`build.py`), two corrected
docstrings/doc passages (`tutorial_tools.py`, `planning/CELL_IDENTITY.md`,
`docs/tutorial-tools-explained.md`), one new section in
`docs/WRITING_TUTORIALS.md`, two new tests in `tests/test_build.py`.*

**7.138 — The two known e2e failures 7.136 flagged, chased down.** One
turned out to be a real, if minor, test bug; the other wasn't a bug at
all.

**`test_opening_the_fold_clears_the_marker` — not reproducible.**
Isolated, it passed every time; run alongside another heavy e2e file to
recreate the resource pressure of the original failure, it still passed,
while a genuinely timing-sensitive test in that other file failed with
an ordinary timeout under the same load. The original failure was
resource contention from running many heavy suites at once, not a defect
in the marker-clearing code. Nothing changed; recorded so it isn't
re-chased.

**`test_python_started_with_no_console_errors` — two real, unrelated
problems hiding behind one assertion.** `page.inner_text("#dl-status") ==
""` reliably failed even though `#dl-status` was correctly hidden and its
own status-text span was correctly empty — a hidden element's
`innerText` isn't reliably `""` just because it isn't rendered. Fixed the
assertion to check what `setStatus("")` actually promises: `is_hidden()`,
plus the status-text span's own emptiness. That unmasked a second,
genuine `console.error` from `assets/vendor/coi-serviceworker.js`
(third-party): it forces exactly one reload on a genuinely first visit to
pick up cross-origin-isolation headers, and its own `fetch` handler logs
any request that reload cancels. The `page` fixture
(`tests/e2e/conftest.py`) now clears its collected `problems` once the
boot-wait it already does resolves — "no console errors" now means from
a stable, booted page onward, not through the one-time reload every
fresh browser context goes through by design.
*Cost to change: two assertions in one test
(`tests/e2e/test_phase0_golden_path.py`), one `problems.clear()` in the
shared `page` fixture (`tests/e2e/conftest.py`).*

**7.139 — The hand-written `dl-hint`/`dl-answer` folds now convert their
own markdown.** Python-Markdown treats a `<details>` block as raw HTML
through to its closing tag, so every practice page's hand-written
`dl-hint`/`dl-answer` folds had been shipping their numbered steps and
backtick-wrapped code as literal text — no `<ol>`, no `<code>` — while the
`hint` fence's own folds were already correct because
`render_staged_hint()` converts its body separately. The fix follows the
same shape: a new `convert_fold_bodies()` in `build.py`, run on the page
right after its main markdown conversion and before `place_hints()` sees
it, finds each hand-written `<details class="dl-hint">`/`<details
class="dl-answer">` block with a new `FOLD_RE` and runs its unconverted
body through `to_html()` on its own — the same trick `extract_notes()`
already uses for a pedagogical note's raw aside. Only the body between
summary and closing tag is replaced. `convert_fold_bodies()` runs while a
staged hint is still just a placeholder comment, so its later
`dl-hint-staged` class is never in scope for `FOLD_RE` to match.
*Cost to change: one regex (`FOLD_RE`) and one function
(`convert_fold_bodies()`) in `build.py`, one call added to `load()`.*

**7.140 — A `sql exec` fence for tutorial pages, distinct from dewstack's
grammar.** dewstack's `sql cell=`/`sql check=` grammar assumes several
named databases per page and a hand-written `check_*` function per task —
a different cell-identity model from dewlab's shared `_page_globals`
namespace and generic `check()`. The fence here is `sql exec` instead,
reusing `parse_cell()`'s existing `id:`/`hint:`/`expect:` grammar
unchanged — a SQL cell differs from a `python exec` cell only in its
language and what the runtime does with it before it reaches Python.

`Cell` gained a `type` field (`"python"`/`"sql"`, reusing dewmini's
vocabulary), validated against a new `CELL_TYPES` set; `Tutorial` gained
`has_sql`; the manifest gets `needsSqlite: true` under the same "only
pay for what you use" reasoning `math` already uses; `render_cell()`'s
pill now reads the cell's real type.

In `tutorial-runtime.js`, a SQL cell gets CodeMirror's SQL mode (already
vendored for dewmini); a new `wrapSqlCode()`/`codeToRun()` pair turns the
editor's raw SQL into a call to `tutorial_tools._run_sql_cell(db, ...)`,
invoked only at the points code actually leaves for Python —
`cell.getCode()` still returns the reader's own SQL everywhere else.
`bootWorker()` sets `seedDb: true` whenever `manifest.needsSqlite` is
set; the standalone export path needed its own `db`-seeding from
scratch, a pre-existing gap shared with dewmini's main-thread fallback,
closed here only for tutorial pages.

Two real bugs surfaced while confirming a duplicated SQL cell survives a
reload: `duplicateAsCustomCell` was hardcoded to `"python"` regardless of
the cell's real type; and the code that reads a custom cell's
saved/shared `type` back collapsed anything but `"text"` to `"python"`,
silently corrupting a duplicated SQL cell into Python holding raw SQL as
code. Both now recognise `"sql"`.

`assets/editor.js` had two matching gaps: `restoreExecTag()`'s regex was
hardcoded to `` ```python\n ``, so a `sql exec` cell edited there would
come back demoted to inert illustrative code on save; `parseCells()`,
which warns an author before save that a cell id changed, had the same
`python`-only regex. Both now accept either of `CELL_TYPES`'s words.
*Cost to change: a `type` field threaded through `Cell`, the manifest,
and three functions in `tutorial-runtime.js`; two regexes in
`assets/editor.js`; one CSS rule. No tutorial content used this fence at
the time — `tutorials/database-methods/` was the next piece of the
rollout.*

**7.141 — `database-methods` ported from dewstack.** All 12 tutorials of
dewstack's data track ported into `tutorials/database-methods/`,
rewritten in dewlab's own voice and cell grammar (7.140's `sql exec`
fence) rather than copied verbatim. One exception kept deliberately:
`loading-a-real-dataset` and the three pages built on it still fetch
dewstack's exact `ourworldindata.org` CSV, because the dataset itself is
part of what the page teaches. The quiz page reimplements dewstack's
five hand-written `check_*` functions as five `python exec` cells calling
`PRAGMA table_info`/`db.execute` directly against the page's shared `db`
— dewstack's separate named-connection model has no equivalent here, by
design.

`outcomes.yaml` gained an 11-outcome `DBM` module block; `topics.yaml`
gained the matching 12 topics; `topic-groups.yaml` gained three browse
groups. `DBM-LO1` ("typical uses for databases... in business
decision-making") stays uncovered, and `CURRICULUM_MAP.md` says so in the
open. Every `covers:`/`touches:` mapping is keyed by heading anchor
(`dev/curriculum_map.py`'s `anchor_for()`), not cell id — the two are
different contracts, and cell ids alone are the saved-work key.

Two CI checks caught real gaps: `dev/build_topic_editor.py --check`
refused all eleven new DBM topics because six new fine strands had no
column in `strands.yaml`'s `from_strand` map — all six went to the
existing `programming` column, since a query or a table's design is the
same kind of skill as an algorithm or a class in this file's terms.
`dev/build_topic_game.py --check` was separately stale for the same
topics; both generated files are regenerated and check clean now.

The homepage's module grid had pointed the Database Methods card off-site
at dewstack's repository with a "Coming soon" badge; it now points at
the module's own page with the same "Beta" badge as the other two
modules.

`planning/PLAIN_LANGUAGE_PASS.md` had only the module's first series
marked done. A second pass covered the other eight: five were already
clean, three had small real fixes (a passive definition, a table
described as "answers to `SELECT`", a "not x but y" reversal, a recap
list of fragments rewritten into a marked sequence).
*Cost to change: 12 tutorial files and 12 glossary files under
`tutorials/database-methods/`, three `.order.yaml` files, an 11-outcome
block in `outcomes.yaml`, 12 entries in `topics.yaml`, three groups in
`topic-groups.yaml`, one line in `modules.yaml`, six lines in
`strands.yaml`, one module card in `build.py`, and the two files
`dev/build_topic_editor.py`/`dev/build_topic_game.py` generate.*

**7.142 — A live HTML/CSS/JS site editor for tutorial pages, sharing one
engine with dewmini's own Site tab.** dewmini's Site tab
(`compose/dewmini.js`, 7.121) already had the mechanics — a sandboxed
`srcdoc` iframe, live HTML/CSS with JavaScript on Run, a relayed console
with friendly error hints — near-twin to dewstack's own site editor after
the two were ported between each other across 2026-09-04/09-06 (7.134).

Two real gaps forced a fence design different from dewstack's:
`renderSiteView()` is a singleton over module state, so it shows only one
site at a time, while a tutorial page needs several independent live
editors on one page. And dewstack's `site=name` puts a site's identity in
the fence's own info string, which dewlab's Crepe-based authoring editor
cannot round-trip — it keeps only a fence's first word, and has nothing
inside the fence to recover an identity from, unlike every other
exec-family fence, which reads its id from an `id:` line inside the fence
itself.

**The fence, decided:** `html site`/`css site`/`js site`, each with the
same `id:` header every exec-family fence has, plus a `site:` line naming
the group it joins. Consecutive fences sharing one `site:` value group
into one `SiteEditor` (`build.py`'s `extract_blocks()`, tracked by fence
position so an actual intervening fence breaks the run). Panes are
optional — `render_site_editor()` draws only the panes an editor actually
has, unlike dewmini's Site tab, which always shows three. An id collides
with a cell's id the same way two cells colliding does.

**The engine, shared rather than ported a third time.** "Port in shape,
not code" is the rule for the boundary between dewlab and dewstack, not
for two files in one repository heading toward the same drift an
unshared copy always causes. The relay script, the friendly-error map,
the document assembly, and the in-flight-coalescing flush all moved out
of `compose/dewmini.js` into `assets/site-relay.js`, exporting
`mountSitePreview(iframe, {onReset, onConsole, onError})` — a factory,
not a singleton. `renderSiteView()` now only builds its own DOM and calls
into the shared mount; `tutorial-runtime.js`'s new `buildSiteEditors()`
does the tutorial page's equivalent with its own `dl-site-*` chrome. One
unrelated bug surfaced by putting both copies side by side: dewmini's
`buildSiteDocument()` was missing `<base href="about:srcdoc">` — without
it, a relative link inside a dewmini site preview navigates the dewmini
page itself rather than the preview. Fixed in the shared version, so
both products get the fix at once.

**Persistence follows dewlab's own convention, not dewstack's.**
dewstack's site editor deliberately saves nothing; dewlab's promise is
the opposite for every cell, so a tutorial's site editor follows suit:
each pane's current text and whether Run had been pressed travel in the
same per-page `localStorage` record every cell's code and output already
do, keyed by each pane's own `id`. A reload that had been run re-runs on
load; a fresh page never auto-runs JavaScript — the two states are told
apart by one saved boolean per editor.
`render_site_editor()`; a new file, `assets/site-relay.js`; a refactor of
`compose/dewmini.js`'s `renderSiteView()`/`destroySiteEditors()` down to
its own DOM-drawing code; a new `buildSiteEditors()` plus
`saveNow()`/`restoreSaved()` additions in `assets/tutorial-runtime.js`; a
new CSS section in `assets/tutorial-style.css`.*

**7.143 — dewmini web: a second, standalone product sharing the
site-relay engine.** `compose/dewminiweb.html`/`dewminiweb-style.css`/
`dewminiweb.js`: several named sites kept in one `localStorage` record
(`dewminiweb:sites:v1`), each with its own HTML/CSS/JS and a live
preview, New/Delete/Load files/Download acting on whichever site is
open. Shaped like dewstack's own `workspace.js` (multi-file, no notebook
cells) rather than dewmini's own Site tab (one file per language inside
a bigger notebook) — a standalone workspace needs the file concept a
tutorial's embedded editor and dewmini's Python-first Site tab
deliberately don't have.

The engine underneath is a third consumer of `assets/site-relay.js`'s
`mountSitePreview()`: the same live-HTML/CSS, run-on-demand-JS,
friendly-error-hint behaviour a tutorial's site editor and dewmini's
Site tab already have. The console's own DOM-drawing code is written
fresh here rather than shared with `tutorial-runtime.js`'s
`buildSiteEditors()` — two independently maintained look-alikes, the
same relationship `render_cell()` has with dewmini's own cell markup,
worth sharing once one drifts from the other, not before.

Two behaviours ported in shape from dewstack's `workspace.js`: a
debounced save flushed on `pagehide`, and two clicks to delete a site
(the first arms a "click again" state for four seconds). A reader's
first visit shows one working site already run, not empty panes —
`openSite()` calls `run()`, not `render()`, on every load including the
first.

*Cost to change: three new files
(`compose/dewminiweb.html`/`dewminiweb-style.css`/`dewminiweb.js`) and
one paragraph in `build.py`'s `render_index()`. No change to
`assets/site-relay.js`, `assets/tutorial-runtime.js`, or
`compose/dewmini.js` — this product adds a third consumer to an engine
already shaped to take one.*

**7.144 — `getting-started`/`reference` ported from dewstack into
`web-authoring`, with two real `resolve_assets()` gaps found along the
way.** Twelve pages: the `welcome` series (how the pieces fit, a GitHub
account, issues and pull requests, an editor, your copy of the starter,
publish it, the two loops, the browser inspector) and the `shelf` series
(FAQ, troubleshooting, quick reference, project ideas), plus three small
demo `.html` files `project-ideas` links to, copied verbatim. None of
the twelve get a glossary file — an orientation/reference module
introduces GitHub concepts once each rather than building a vocabulary a
later page depends on, the same reasoning that keeps a practice page
glossary-free. `planning/curriculum/topic-groups.yaml` gained two groups
for reachability, with no `covers:`/QQI mapping, since nothing here
teaches a QQI outcome the way an `exec` cell does.

Every dewstack-specific reference was rewritten to dewlab's own
equivalents (its own repository, a real merged PR in place of a
dewstack-specific one) rather than carried over. dewstack's SQL/site-editor
persistence story doesn't describe dewlab at all — dewstack special-cases
one saved box with its own Download/Load pair; dewlab saves every cell's
code and result the same uniform way, so the FAQ/troubleshooting pages'
"where is my work saved" sections were rewritten around that rule
instead of carrying the special case across.

`resolve_assets()` had two real gaps this content needed: it had never
rewritten a plain `href=` the way it rewrites `src=` (now handled,
deliberately permissive — a missing `href=` target is left alone rather
than failing the build, since plenty of links aren't a local asset); and
a literal `src="…"` shown as text inside a code span was being read as a
real attribute and failing the build over an example — `<code>`/
`<pre><code>` spans are now masked out before substitution and restored
after. Both are new tests in `TestTutorialAssets`.

The homepage's Web Authoring card stays "Coming soon" — getting-started
and reference are scaffolding, not a lesson in HTML or CSS, and a card
promising the module before it teaches anything would cost more than it
saves.

*Cost to change: twelve new tutorial folders under
`tutorials/web-authoring/`, two new `.order.yaml` files, `web-authoring`
added to `tutorials/modules.yaml`, two new topic-groups,
`resolve_assets()`'s `href=` handling and its `CODE_SPAN_RE` masking in
`build.py`, two new `TestTutorialAssets` cases. No change to
`outcomes.yaml`/`topics.yaml` — this content was never QQI-mapped.*

**7.145 — The 30-page `web-authoring` series, and a real gap in the
site-editor engine only live content could have found.** Both of
dewstack's web series ported: `first-site` (22 pages — a page's own
files, the head/body split, semantic HTML, the box model, selectors,
position, hover/focus, transitions, media queries, flexbox, grid, BEM,
keyframes) and `several-pages` (8 — planning a multi-page site,
consistent navigation, cards and a gallery, a phone-safe nav, an
accessible form, image file size, documenting what got built). Every
`html site=name`/`css site=name` fence became dewlab's own `id:`/
`site:`-header grammar, every id chosen fresh. No QQI mapping here
either, for the same reason as 7.144. Reachability comes from five new
`topic-groups.yaml` groups, split by what each sub-arc actually teaches.

Four pages ask a reader to narrow the preview to watch a media query, a
flex row, or a named grid area change — the engine had no preview-width
control until now. `render_site_editor()` and `buildSiteEditors()`
gained the same slider `dewminiweb.js` already has: a 30%-100% range
setting `.dl-site-frame`'s inline width, not persisted between visits (a
viewing preference, not saved work).

The slider alone wasn't enough: `.dl-site-split`'s side-by-side layout
left the preview only 64-212px wide across the whole range — nowhere
near a realistic breakpoint. The split itself, not the slider, was the
mistake: `.dl-site-split` now stacks unconditionally, panes above a
full-width preview, widening the range to 131-437px. Safe to change now,
since no tutorial content had shipped against the side-by-side layout
and neither dewmini's Site tab nor `dewmini web` reuses `.dl-site-split`.
Three pages needed their own breakpoint numbers adjusted once the real
range was known: `cards-in-a-row`'s demo from `flex: 1 1 200px` to
`90px`; `flexbox-first-steps` from `100px` to `80px`; `named-grid-areas`
from `min-width: 500px` to `350px`.

*Cost to change: 30 new tutorial folders, two new `.order.yaml` files,
five new `topic-groups.yaml` groups, the preview-width slider added to
`render_site_editor()`/`buildSiteEditors()`/`tutorial-style.css`, and
`.dl-site-split` changed from a side-by-side flex row to a stacked
column. The module still needs a real QQI descriptor before
`covers:`/`outcomes.yaml` entries can honestly follow.*

**7.146 — QQI 5N1910 mapped from the real descriptor; a stale DBM-LO6/
LO7 gap-claim fixed along the way.** Fourteen outcomes added to
`outcomes.yaml`/`topics.yaml`, paraphrased the way DBM's eleven are,
honest about where dewlab's approach — a hand-written in-browser site
editor, GitHub Pages instead of an ISP, no WYSIWYG tool, no CMS, no code
generator — parts ways with the descriptor's GUI/vendor assumptions. 40
of the 42 web-authoring pages carry `covers:`/`touches:` frontmatter;
`faq.md` and `issues-and-pull-requests.md` teach nothing on the list.
Ten of the fourteen codes land on real content; WA-LO1 (HTML/CSS version
history), WA-LO5 (desktop publishing/CMS tools) and WA-LO12 (code
generators) have no dewlab equivalent, the same shape as DBM-LO1.

The database-methods comment block and DBM-LO7's own title still called
DBM-LO6's data-entry half and DBM-LO7 uncovered — false since "A Form
That Writes a Row", "Exporting a Query to a File" and "Charting a
Query's Result" already cover them. Rewritten to match
`CURRICULUM_MAP.md`, which already showed both green. DBM-LO1 is the one
real DBM gap left.

`dev/curriculum_map.py`'s `anchor_for()` re-implements Python-Markdown's
slugify by hand and has no notion of a repeated heading, so
`keyframes-and-the-checkbox-hack.md`'s second "Why this happens" heading
(`why-this-happens_1` in the built HTML) can't be addressed on its own —
its `covers:` frontmatter merges both headings' coverage into the one
addressable key instead. `strands.yaml` gained WA's eight fine strands:
`web-history`/`html-tags`/`css` in the `programming` column alongside
DBM's own; `tooling`/`design-principles`/`process`/`testing`/
`independence` in `software-development`, the same column
FOOP-LO5/9/10/11 and PDP-LO7/9/10/12 sit in for the same reason — a
practice, not a way of writing code.

*Cost to change: the DBM comment/title fix; the WA-LO module block in
`outcomes.yaml` and matching `topics.yaml` entries; `covers:`/`touches:`
frontmatter on 40 of 42 web-authoring pages; eight new fine strands in
`strands.yaml` and the two regenerated static pages that depend on it.
No engine or build.py change this time.*

**7.147 — DBM-LO1 closed with an intro, plus a two-part addition: a
five-table capstone and a many-to-many practice quiz.** `a-table-is-a-list-of-rows.md`
gained a short "Where databases already show up" section — the module's
only remaining outcome with no dewlab content, closed the way its own
`topics.yaml` entry always said it could be: a discussion, not a build.
DBM is now the first fully-mapped module, all eleven outcomes covered.

**"A College Timetable"**, the last page of `several-tables`, is a
five-table design (`programmes`, `teachers`, `rooms`, `modules`,
`sessions`) built around one real problem a flat list can't answer: has
anyone been double-booked. A real gotcha surfaced while writing it —
`session_date` started as a weekday name (`'Monday'`) until the page's
own `ORDER BY` sorted Friday before Monday, alphabetically; switched to
an actual ISO date, which sorts the same way as text or as a calendar
date, and folded the reasoning into the design section itself rather
than quietly fixing it. The centrepiece is a self-join: two made-up
sessions worked by hand first (does each one start before the other
ends), then the same rule as SQL, comparing `sessions` against itself
with `s1.id < s2.id` ruling out a row matching itself or a pair
reported twice. A parallel teacher-clash query is left for the reader,
with a hint and a worked answer.

**"The Library Loans Quiz"**, a third page in `practice` after
`sql-practice` and `the-tentacular-plushies-quiz`, pushes past
one-to-many into many-to-many: a `book_authors` junction table with a
composite primary key, `PRIMARY KEY (book_id, author_id)`, checked by
reading `PRAGMA table_info`'s own `pk` column rather than trusting
column names alone. Same six-task, check-cell-per-task shape as the
plushies quiz.

Two real bugs found only by running every cell in a real browser
against a self-hosted Pyodide, not by reasoning about the SQL in the
abstract: `find-teacher-clashes`'s stub comment had a semicolon in its
own prose ("adapting find-room-clashes; the answer") that
`_run_sql_cell`'s bare-`;` statement splitter — documented as "not a
real SQL parser" — read as a statement boundary, breaking the comment
into a syntax error; reworded to drop the semicolon. Three of the
library quiz's check cells (tasks 4-6) queried `authors`/`books`/
`loans` directly with no existence guard, so running them before the
earlier tasks were done raised a raw Python traceback instead of a
plain-language message — given the same `PRAGMA table_info` guard every
earlier check cell in the module already uses.

*Cost to change: one new section in `a-table-is-a-list-of-rows.md`; two
new tutorial folders (`a-college-timetable`, `the-library-loans-quiz`)
with their own glossary files; both `.order.yaml` files and
`topic-groups.yaml` updated. No engine or build.py change.*

**7.148 — "Conclusions and Next Steps" closes WA-LO1 and WA-LO5, leaving
WA-LO12 as the module's one real gap.** A new last page in
`several-pages`, after `documenting-what-you-built`: a short history of
HTML and CSS (Tim Berners-Lee's original ~18 tags in 1993, HTML2 through
HTML4.01, the 2004 WHATWG split that produced HTML5, and HTML5's own
shift to a living standard with no successor number; CSS1 through
CSS2.1, then CSS3's split into independently-released modules — flexbox
and grid, both already taught, are two of them), then GitHub Pages named
plainly as the website management system this course has used the whole
time, alongside WordPress, Carrd and Solo as three different trade-offs
against hand-writing HTML and CSS. Every date and product claim checked
against a live search before writing it, not reconstructed from memory.

Closing WA-LO5 surfaced the same stale-title bug DBM-LO7 had: its own
`outcomes.yaml` title still said "not yet covered by anything in
dewlab" after the page covering it existed. Fixed the same way, and
trimmed WA-LO5 out of the WA module comment's own list of uncovered
codes, leaving WA-LO12 (code generators) as the only one left — dewlab
teaches HTML and CSS by hand throughout, and a generator's output has
nowhere honest to sit next to that without a real decision about what
it would mean to "employ" one.

*Cost to change: one new tutorial folder with its own glossary file
(the first in web-authoring — the module's other 42 pages have never
had one, a pre-existing gap this doesn't close); both `.order.yaml` and
`topic-groups.yaml` updated; two outcomes.yaml corrections. 115 of 116
outcomes now in place.*

**7.149 — web-authoring's series order, and glossary files for its 42
pre-existing pages.** Added `tutorials/web-authoring/series.yaml` with
`order: [welcome, first-site, several-pages, shelf]`. Without it, both
the module page's display order and the reference panel's cumulative
accumulation fell back to alphabetical by series key, which put
"Welcome" — the series a reader is meant to start with — last.

Wrote a `<slug>.glossary.yaml` for every one of the module's other 42
pages (`conclusions-and-next-steps` already had one from 7.148), read
in the corrected series order so each file's own new terms build on
what came before. Two homonyms needed a disambiguated term name to
avoid colliding with an earlier, unrelated meaning already in the
reference: "element" (an HTML element, from `a-page-is-files`) versus
"element (BEM)" (a named part of a block, from
`css-variables-and-bem`); "max-width" (an element-sizing property, from
`the-container`) versus "max-width (media query)" (a screen-width
condition, from `media-queries`).

Two things surfaced worth a look rather than fixed here. `named-grid-
areas.md`'s own prose says `auto-fill` sits "alongside the auto-fit
already shown on a grid gallery" — but `a-grid-gallery` is in
several-pages, which this same series order puts after first-site, so
the reference runs backward relative to how a reader actually meets the
two pages. `quick-reference.md`'s tables also name a handful of tags
and properties — `<table>`/`<tr>`/`<th>`/`<td>`, `line-height`, `gap`,
the `em`/`vh`/`vw` units, `:link`/`:visited`/`:active`,
`target="_blank"`, `placeholder` — that no narrative tutorial in the
module actually teaches; it may be deliberate completeness for a cheat
sheet, or a real gap.

*Cost to change: one new `series.yaml`; 41 new glossary files, no
tutorial prose changed. `dev/curriculum_map.py`'s vocabulary section is
unaffected — it tracks italicised emphasis in prose, not glossary
files, so this pass could not introduce a new "used before it was
introduced" warning even where it added a disambiguated term.*

**7.150 — A staged hint can now wait for a SQL query that comes back
empty.** Josh, thinking through what a hint system could do for
`database-methods` beyond translating a raw sqlite3 message: "maybe we
can really look at code and help a student when the output is
unexpectedly empty" — the failure a raw error message can't help with
at all, since nothing raises. A missing comma between two `SELECT`
columns doesn't error, it silently becomes an alias; a case-mismatched
`WHERE` doesn't error, it silently matches nothing. `check_*`-style
authored checks already catch this on a page that has one; most `sql
exec` cells don't.

`after: 2 empty results` (also `empty-result:2`) is a new trigger key,
same shape as `check-fails` and everything else in the grammar
(`TRIGGER_KEYS`, `build.py`). `_run_sql_cell()`
(`assets/tutorial_tools.py`) already builds a DataFrame from a `SELECT`
statement's rows before this — the only new work is recording whether
that frame came out empty, on the `_CellContext` the same way
`last_check`/`last_error` already are, and reporting it as `"empty"`
in `_report()`'s JSON. `assets/tutorial-runtime.js`'s `freshAttempts()`/
`noteAttempt()`/`triggerHolds()` — the exact machinery `errors`/
`same-errors`/`checkFails` already use — gained one more counter,
`emptyResults`, reset on any non-empty result and left untouched by a
run whose last statement wasn't a query at all (a `CREATE`/`INSERT`
cell reports `empty: None`, which the counter treats as "no signal
either way," not as an empty result).

Nothing here inspects *why* a result was empty — that stays the harder,
not-yet-built idea from the same conversation (relaxed re-runs of a
`WHERE` clause to spot a case mismatch or a missing row). This is only
the cheap half: the fact that it came back empty, for an author's own
hint to react to, the same division of labour every other trigger in
this system already keeps between "when" (the infrastructure decides)
and "what" (the author writes).

*Cost to change: one field on `_CellContext`, one line in
`_run_sql_cell()`, one field in `_report()` (`assets/tutorial_tools.py`);
one counter in three functions (`assets/tutorial-runtime.js`); two
entries in `TRIGGER_KEYS` plus the error message they extend
(`build.py`). Three new tests in `tests/test_tutorial_tools.py`
(`TestRunSqlCell`, `TestRunReport`), one in `tests/test_build.py`
(`TestStagedHints`). Full unit suite green; a fresh full-site build
confirmed clean. No browser end-to-end test yet — the existing
`tests/e2e/test_cell_hints_staged.py` only exercises a Python exec
cell; worth extending once a second staged-hints signal needs the same
proof.*

**7.151 — A SQL cell now looks at the actual schema and data before
giving up on a plain error message.** Josh: "let's also think through
the steps a student might make like mistyping a name of a variable or
not having the right syntax or order for where or another filter."
Four additions to `assets/tutorial_tools.py`, all inside
`_run_sql_cell()`'s own path, none touching the trigger/attempts
machinery 7.150 added:

**A typo gets the same "did you mean" CPython already gives its own
exceptions.** `no such table: prodcuts` and `no such column: pricee`
name the mistake and nothing else; sqlite3 has no equivalent of the
`NameError`/`AttributeError` suggestion Python 3.10+ added natively.
`_sqlite_typo_suggestion()` reads the real table names from
`sqlite_master` (and every real column, via `PRAGMA table_info`, when
the message names a column) and offers `difflib`'s closest match above
its own default similarity cutoff — silent rather than wrong when
nothing is close enough to trust.

**An aggregate in `WHERE` gets pointed at `HAVING`.** `misuse of
aggregate function COUNT()` is accurate and unhelpful — sqlite3 spots
the mistake but never names the fix, one of §2's own two rows in this
file's own SQL survey.

**Clauses out of order get a structural note**, checked only once a
statement has already failed to run: `_clause_order_note()` finds
which of `SELECT`/`FROM`/`WHERE`/`GROUP BY`/`HAVING`/`ORDER BY` the
statement actually contains, in what order, and says so when that
order doesn't match SQL's own — the same regex-not-a-parser
approximation `_run_sql_cell()`'s `;`-split already makes, and never
run against a statement that worked, so a keyword inside a string
literal can only ever add noise to an already-broken query, not to a
correct one.

**All three fold into the exception's own message**, via a new
`_execute_sql()` every statement now runs through instead of calling
`conn.execute()` directly — not a separate block underneath the way
`_ERROR_HINTS` adds one, because `_describe_error()` only reads a
message's first line for the `same-errors` trigger, and keeping the
addition on that same line was the only way to add it without a second
plumbing path from `_run_sql_cell()` all the way out to
`render_error()`.

**The empty-results signal 7.150 built now explains itself, immediately,
whether or not an author staged a hint for it.** `_empty_result_notes()`
runs once a `SELECT` has already come back empty: it counts the rows in
the table named after `FROM` (empty table, or a filter that excluded
real rows — two different problems with the same symptom), and, for a
`column = 'literal'` comparison, quietly reruns the same query
case-insensitively and reports how many rows that would have matched.
Both are facts the database itself confirms, never a guess dressed up
as one — the case note only appears when the relaxed rerun actually
found more, and both can appear together (a case mismatch is still a
row the table really has).

*Cost to change: six new functions and one changed call site in
`assets/tutorial_tools.py` (`_sqlite_table_names()`,
`_sqlite_typo_suggestion()`, `_clause_order_note()`,
`_sqlite_error_note()`, `_execute_sql()`, `_empty_result_notes()`); ten
new tests in `tests/test_tutorial_tools.py`. No change to `build.py`,
`tutorial-runtime.js`, or the trigger grammar — this is what a SQL cell
itself shows, not a new signal for a staged hint to wait on. Full unit
suite green; a fresh full-site build confirmed clean.*

**7.152 — the `named-grid-areas.md` forward reference from 7.149 is
fixed; `quick-reference.md`'s scope is still open.** Of the two things
7.149 surfaced, one was a plain bug: the page's own prose claimed
`auto-fit` was "already shown" on `a-grid-gallery`, a page the
corrected series order actually places later. Reworded to point
forward — "`a-grid-gallery`, later in this course, covers `auto-fit`
itself" — instead of claiming a reader has seen something they have
not yet.

The other, `quick-reference.md` naming syntax no tutorial teaches
directly, is not a bug in the same sense. Its own page says it is not
meant to be read start to finish, which argues for a cheat sheet
reaching past exactly what was taught; nothing else in the repository
settles whether that is the intended scope or an oversight. Left as is
until that is decided.

*Cost to change: one sentence in one tutorial, and its glossary file's
own note updated to match. No frontmatter, no covers:, no test
affected.*

**7.153 — `web-authoring` is the second module through the full
plain-language pass.** `planning/PLAIN_LANGUAGE_PASS.md` records
`database-methods` as fully checked against the style guide's voice
section (then §4); every other module, `web-authoring`
included, had only had the sentence-length and metaphor rules run over
it, if that. Ran the complete nine-point check over all 43 tutorials
(welcome's 8, first-site's 22, several-pages' 9, shelf's 4), series by
series in `series.yaml`'s reading order.

Eight genuine violations across seven files, not the systemic patterns
`database-methods`'s own pass found — this content was written or
ported against the guide already, so the pass mostly confirmed rather
than rewrote. Two "not X but Y" reversals, one em dash holding a
term's whole definition, one meaning-after-the-dash sentence
reordered, one verbless opening fragment, two idioms, and one stray
reference to "the older course" a student reading only dewlab would
have no way to parse. `planning/PLAIN_LANGUAGE_PASS.md`'s own "Done"
section has the full list, sentence by sentence.

*Cost to change: eight one- or two-sentence edits across seven
tutorial files; no cell code, no frontmatter, no covers: touched.
`dev/curriculum_map.py`'s vocabulary section is unaffected — none of
the eight edits touched an italicised term. Full unit suite green; a
fresh full-site build confirmed clean.*

**7.154 — Two `database-methods` pages carry the first live `empty
results` staged hints.** 7.150 and 7.151 built the machinery and the
on-page facts; nothing had actually used either in front of a student.
`asking-questions-of-a-table`'s WHERE section, right where the prose
already invites a reader to try their own condition, now carries two
folds on `query-carnivores`: the first, at `2 empty results`, asks
whether the text after `WHERE diet =` matches the table's own spelling
letter for letter; the second, at `5 empty results`, gives the steps —
`SELECT DISTINCT diet FROM dinosaurs;`, then compare. A case mismatch
there is also exactly what 7.151's own case-insensitive fact already
names on the page, so the fold and the fact now point at the same
thing from two directions.

**The tentacular plushies quiz** binds its pair to `quiz-workspace`,
the one `sql exec` cell every task reuses, rather than to a dedicated
query cell — Task 5 is where a filter is most likely to come back
empty, but the counter tracks the whole box across all five tasks, so
the fold's own wording had to stay true regardless of which task is
open: it points the reader at the row-count note 7.151 already prints
under the empty result, rather than re-describing what might be wrong,
since by Task 5 an empty result is exactly as likely to mean "the
table still has no matching data" as "the filter is wrong."

Checked in a real Chromium against the self-hosted Pyodide build,
scripted rather than by hand — the fixture harness `test_cell_hint.py`
and `test_cell_hints_staged.py` use only drives one `python exec`
cell, so this ran the actual built pages instead: two empty-result
runs on `query-carnivores` (`WHERE diet = 'carnivore'` against a table
storing `'Carnivore'`) surfaced both 7.151 facts and the first fold;
two on `quiz-workspace` against a real one-row `products` table did
the same. No end-to-end test committed yet for a `sql exec` cell's
staged hints — `test_cell_hints_staged.py` still only exercises the
Python path — so this is still checked by hand each time rather than
in CI.

*Cost to change: prose and two `hint` fences in each of two tutorial
files, no cell id renamed, no frontmatter or `covers:` touched, no
`version:` bump since no cell's own code changed. Full unit suite
green; a fresh full-site build confirmed clean; manual Chromium
verification above, not yet a committed e2e test.*

---

**7.155 — `ROADMAP.md` Phases 3 and 4 retired unbuilt, in favour of persistent highlights and margin notes.** Neither "practice that regenerates" nor "the portfolio export" had been started, and both still carried unsettled open questions of their own. Rather than let either sit half-decided, both were dropped by direct choice and replaced with a single new design: a reader marks a passage of prose and, optionally, attaches a note to it — the persistent-highlighting idea Phase 5 had already raised and set aside as needing real anchoring work.

**The anchoring answer, not previously worked out, turned out cheap.** Phase 5 worried that prose has no id the way a cell has a `task_id`, and that building one means a build-time scheme `WINDOW_AUDIT.md` would have to freeze. `HIGHLIGHTS_AND_NOTES.md` §3 answers it without a build.py change at all: a highlight records its selected text, a little surrounding context, and its ordinal position among the page's prose blocks, all computed at read time; restoring one searches nearby blocks for the same text before giving up. A highlight that can't be relocated is dropped and reported, the same "a notice, never a block" posture `VERSIONING_AND_PROGRESS.md` already uses for a cell whose id disappeared — so nothing about this needs to be perfect, only honest when it fails.

**Both retired phases stay in `ROADMAP.md`**, marked and pointing at this entry and at git history, rather than deleted — the same treatment past retirements in this log get. Phase 3's slot became the new design's home, since something was going to be built there; Phase 4 became a one-line pointer to it, since one feature does not need two phase numbers. Phase 5's own numbering, and every place that cites it by number, is untouched.

*Cost to change: nil, so far — nothing described in `HIGHLIGHTS_AND_NOTES.md` has been built yet. The document itself is the plan to build against; changing the anchoring approach before any code exists costs a rewrite of one section, not a migration.*

---

**7.156 — The highlight anchoring lookup, built and tested on its own before anything calls it.** `HIGHLIGHTS_AND_NOTES.md` §3/§14 planned this as its own step, isolated from the selection toolbar and the save schema, on the reasoning that a mistake in the one genuinely new algorithm here is worth catching before UI gets built on top of it. `assets/tutorial-runtime.js` gains `proseBlocks()` (every anchorable passage in reading order, a block nested inside another matching block skipped in favour of the inner one), `describeQuote()` (a block plus offsets to the `{quote, prefix, suffix}` triple an anchor stores), and `locateHighlightAnchor()` (rebuilding `{block, index}` from a saved anchor: the exact block first, then a search of five blocks either side before giving up). Nothing in the page calls any of these yet — exposed on `globalThis.dewlab` for their own tests only.

**Ambiguity is resolved by exact context, not guessed at.** A block with the same short phrase twice ("the pivot" appearing twice in one paragraph, in the test fixture) can't be told apart by the quote text alone; `findQuoteInBlockText()` requires an exact match on the surrounding `prefix`/`suffix` text in that case, and treats failing to disambiguate the same as not finding the quote at all rather than picking one.

**Found while writing the test fixture: adding a single cell to a page adds three more anchorable blocks, not zero.** A page with a cell — any cell — gains the (hidden) report-a-problem paragraph (`planning/feedback.yaml` `enabled: true` since 7.14x's era) and PRACTICE.md's "Try something of your own" heading and paragraph below the last cell. Both are real, readable prose and are correctly not excluded — only a cell's own `.dl-editor`/`.dl-output` are — but the fixture's own expected block count was wrong until this was noticed, a reminder that "prose" here means "matches the selector and isn't inside a cell's own chrome," not "written by the tutorial's author."

Tested in `tests/e2e/test_highlight_anchoring.py`, against a purpose-built fixture tutorial rather than the shared e2e fixture, since the repeated phrase and the deliberate paragraph count needed to be exact: the three outcomes `HIGHLIGHTS_AND_NOTES.md` §13 named (same block, moved-but-findable block, genuinely gone) plus the disambiguation case, all driven directly against `dewlab.proseBlocks()`/`describeQuote()`/`locateHighlightAnchor()` rather than through real selection or DOM wrapping, which are the next rollout step.

*Cost to change: low — nothing in the running page depends on this yet, so the algorithm can still change shape freely. `vendor-src/`'s `standalone.bundle.js` was rebuilt, since this touches `assets/tutorial-runtime.js` directly.*

---

**7.157 — `highlights` joins the saved-progress record, and the restore summary learns a wording rule that has nothing to do with version numbers.** `HIGHLIGHTS_AND_NOTES.md` §4/§14, rollout step 3. `saveNow()` gains one more field alongside `notes` and `cells`; `restoreSaved()` re-locates each saved highlight via 7.156's `locateHighlightAnchor()` before trusting it, keeping what still resolves and dropping the rest — the same drop-and-report shape a cell whose id disappeared already gets, not a new mechanism. The in-memory array is `const` and mutated in place (`highlights.length = 0` then pushed into), the same discipline `cells` already follows, so a reference taken once — `globalThis.dewlab`'s own included — never goes stale if restore ever runs a second time in one page load.

**A dropped highlight can happen with no version change at all, so its message couldn't reuse the cell one.** `VERSIONING_AND_PROGRESS.md` bumps `tutorial-version` only for executable-cell changes, never for prose — so an ordinary copy-edit can strand a highlight while leaving every version check green. `announceRestore()` gets its own line for this, worded around the text having changed rather than "this version does not have," and its early-return guard now also fires the box for a highlight-only drop on a page with zero cells, a case that could not previously happen and so had never needed the guard's attention.

Tested in `tests/e2e/test_highlight_schema.py`: a highlight round-trips through save and a real reload; a dropped highlight's own note survives in the stored record even once the highlight itself is gone from the live page (only the anchor goes stale, not the text a student wrote); the restore box appears with singular and plural wording; and — the one worth stating on purpose — a *successful* highlight restore stays silent, the same as it always has for cells, since nothing here should announce itself for working as expected.

*Cost to change: low — nothing renders a highlight yet (rollout step 4 does the DOM wrapping), so this is still schema and message wording, not behaviour a reader can see. `vendor-src/`'s `standalone.bundle.js` rebuilt, since this touches `assets/tutorial-runtime.js` directly.*

---

**7.158 — A highlight is visible now: `<mark>` wrapping, and the bridge that makes a restored one show up without a reader touching anything.** `HIGHLIGHTS_AND_NOTES.md` §6, rollout step 4. `wrapRange()` wraps a `Range` in one or more `<mark class="dl-highlight">` elements sharing one `data-highlight-id` — several, not one, whenever the range crosses a child element (an `<em>`, a `<code>`), since `Range.surroundContents()` throws on exactly that case; `unwrapHighlight()` reverses it, `normalize()`-ing the block afterward so repeated highlight/unhighlight cycles don't fragment its text nodes further each time.

**The genuinely new piece: turning a number back into something on screen.** `locateHighlightAnchor()` (7.156) only ever hands back a character offset into a block's flattened `textContent`; `wrapRange()` only ever accepts a live `Range`. Nothing bridged the two, which meant a highlight restored by 7.157 had nowhere to go — the record came back, but nothing showed. `rangeForOffsets()` is that bridge: the same `[start, end)` numbers `describeQuote()`/`findQuoteInBlockText()` already work in, walked back into a real `Range` however many text nodes it spans. `restoreSaved()` now calls it for every highlight `locateHighlightAnchor()` finds, so a highlight a reader made yesterday is visibly marked again the moment the page loads — the first genuinely visible piece of this feature, four rollout steps in.

---

**7.159 — The About page's content moved out of `build.py` and into `pages/about.md`, the first of what a `pages/` directory is for.** Raised discussing dewnote (the separate markdown-editor project, `deweydex/dewnote`) and its own dealings with dewlab's content: a hardcoded HTML string in `write_about_page()` is not a page any markdown editor, dewnote included, can open, and it is the one piece of real student-facing prose on the site that a course maintainer could not already edit the way a tutorial is edited. `read_page()` is the new, small reader — a page's frontmatter is `title` only, none of `split_frontmatter()`'s module/series/version machinery applying to something that isn't part of the curriculum — and the body converts through the exact `to_html()` a tutorial's own prose already uses, so an About-page link or a bold name renders exactly as it would in a tutorial, no second rendering path to keep in sync. `write_about_page()` itself shrank to assembling the shell around whatever `read_page("about")` returns. The wording is unchanged, checked directly by rebuilding and diffing the page: the only visible difference is that its headings now carry `id` attributes, the same as any tutorial's, since `to_html()`'s `toc` extension is always on — previously absent because the hardcoded string simply never had a fold or a link a heading id would matter to.

The `repo` test fixture (`tests/test_build.py`) gained a `pages/about.md` of its own, written from the real file the same way it already carries a copy of `assets/shell.html` — necessary because `write_about_page()` runs on every one of this suite's 310-odd calls to `b.build()`, and a missing page now fails the build loudly (`fail()`, the same as a tutorial with broken frontmatter) rather than silently rendering nothing. The one existing About-page test (`(repo/"site"/"about.html").is_file()`) was a real, previously unremarked gap: it could not have caught a wrong word, a broken link, or a missing title, since nothing about the page's own content was ever exercised. `TestTheAboutPage` closes that — content actually comes from the file, a link renders as a link, the page's own title comes from its frontmatter, a missing file or a missing `title` fails the build with a message naming which.

Left for later, not attempted here: the home page (`render_index()`) is still a hardcoded string, and is real, separate scope — it has actual tutorial data threaded through it (module cards, counts) that an About-style plain-markdown page never had to contend with, so the same move there needs a real design for how a markdown source names "put the module list here" rather than an assumption that copying this pattern verbatim would just work.
*Cost to change: low. `read_page()` is additive — nothing about a tutorial's own `split_frontmatter()`/`to_html()` path changed — and reverting would mean pasting `pages/about.md`'s content back into a Python string, exactly as easy a move backward as it was forward.*

**One new custom property, sized against the theme it lives in, not a fixed colour.** `--dl-highlight-bg` (`#fbe8a6` light, `#4a3a12` dark) keeps `--dl-fg` at 8.6:1+ against it in both themes — comfortably past the 4.5:1 AA minimum `test_link_contrast.py` already measures for `--dl-link`, extended here to `.dl-highlight` the same way. High-contrast mode was deliberately left alone, matching how `--dl-cell-bg`/`--dl-pass-bg` already work: neither is overridden by `:root[data-contrast="high"]` either, so this follows existing precedent rather than inventing a new rule for one more decorative background.

Tested in `tests/e2e/test_highlight_wrapping.py`: wrapping a selection that spans a child element produces exactly the marks expected with the prose's own text untouched; unwrapping restores plain text without disturbing the surrounding markup; `rangeForOffsets()` round-trips the same text `describeQuote()` saw; a highlight seeded into storage renders as a real `<mark>` after a reload with no selection made; and the AA contrast check, parametrized light/dark the same way the link one already is.

*Cost to change: low — still no reader-facing way to *create* a highlight (rollout step 5, the selection toolbar); everything here only makes an already-saved one visible. `vendor-src/`'s `standalone.bundle.js` rebuilt.*

---

**7.159 — A reader can make a highlight now: the selection toolbar's Highlight button.** `HIGHLIGHTS_AND_NOTES.md` §5, rollout step 5. Extends `initReferenceLookup()`'s existing `selectionchange` listener — until now only ever offering Look Up — with a second, independently `position: fixed` button, `.dl-highlight-btn`, shown for any selection that fits inside one prose block (`blockFor()`, `.closest(PROSE_BLOCK_SELECTOR)` on both ends of the range) and long enough not to be a stray character. Clicking it calls `createHighlight()`: read the selection's own `[start, end)` offsets (`offsetsForRange()`, the same `pre-range.toString().length` trick used for a comparable problem in enough editors that it counts as the standard one), build the anchor with `describeQuote()`, `wrapRange()` it visible immediately, and `scheduleSave()` — the exact same three functions 7.156–7.158 built and tested with nothing yet calling them.

**The button gets no glossary requirement, on purpose, and that meant undoing an early return.** `initReferenceLookup()` used to bail out entirely (`if (!terms.length) return;`) on any tutorial with no glossary — reasonable when the only thing in the function was Look Up, wrong now that Highlight lives in the same function and needs no glossary at all. The early return is gone; a termless tutorial simply never has `termFor()` match anything, which was already true.

**Two buttons, not one toolbar with a shared wrapper — `test_reference.py` decided that, without meaning to.** It already asserts `.dl-lookup` carries `hidden` directly (`page.is_hidden(".dl-lookup")`, `wait_for_selector(".dl-lookup:not([hidden])")`); wrapping both buttons in a container whose own `hidden` attribute gated visibility would have made that attribute alone stop meaning "this button is showing." Two independently fixed, independently hidden buttons, laid out side by side by a small shared `layout()` helper, preserves that contract exactly — and the highlight button gets its own class, `.dl-highlight-btn`, rather than sharing `.dl-lookup`'s, so the two are never ambiguous under the same selector either.

**"Add a note" is not in this toolbar yet — deliberately, not an oversight.** The rollout sketch named a three-button toolbar for this step; building it turned up that "Add a note" has nowhere to send a reader without step 6's edit/remove popover existing first; that button waits for step 7, the one-step combination the popover makes possible. A highlight made now can still gain a note later, once step 6 ships — clicking the highlight it made.

Tested in `tests/e2e/test_highlight_creation.py`: a tutorial with no glossary at all still offers to highlight; a known glossary term offers both buttons together; a selection crossing two paragraphs offers neither the highlight (nor, separately, is expected to match a term); clicking Highlight produces a real `<mark>`, saves it, and both buttons disappear afterward; and a highlight made this way — not seeded into storage by a test, the actual button — survives a real reload. `test_reference.py`'s existing 28 tests all still pass unchanged.

*Cost to change: low. `vendor-src/`'s `standalone.bundle.js` rebuilt, since this touches `assets/tutorial-runtime.js` directly.*

---

**7.160 — A highlight can be edited or removed now: the popover on an existing `<mark>`.** `HIGHLIGHTS_AND_NOTES.md` §7, rollout step 6. One shared `.dl-highlight-popover`, not one per highlight — clicking any `<mark class="dl-highlight">`, or reaching it by Tab and pressing Enter or Space, opens it against that mark's own note (`highlights.find(h => h.id === id)`), positioned the same fixed, viewport-clamped way `initReferenceLookup()`'s own buttons already are. Save writes the textarea back into the highlight's `note` field and calls `scheduleSave()`; Remove calls `unwrapHighlight()` (step 4) and drops the record from the in-memory array, then also saves.

**Only the first fragment of a multi-`<mark>` highlight is a tab stop.** `wrapRange()` (step 4) already produces several `<mark>`s sharing one `data-highlight-id` when a selection crosses a child element; giving every fragment its own `tabindex="0"` would have made one highlight into several identical tab stops. `marks.length === 0` inside that same function's own loop is the only change needed — it already builds every fragment of one highlight in a single call, so "first" is unambiguous.

**A highlight with a note gets a confirmation before Remove; a bare one doesn't — the same reasoning that split Reset from Clear on a cell.** Losing a plain highlight costs nothing (select the text again); losing one with a note loses a sentence a reader actually wrote, so `confirm("Remove this highlight and its note?")` guards only that case. Declining leaves both the highlight and its note exactly as they were.

**Click-outside had to explicitly exempt a click that lands on a highlight, not just the popover itself** — otherwise the very click that opens the popover (or switches it to a different highlight) also bubbles to the document-level "close on outside click" listener and immediately undoes what it just did. The same shape `initReference()`'s own click-outside handling already has for the highlight-to-look-up button's click (`DECISIONS_LOG.md` around 7.93).

Tested in `tests/e2e/test_highlight_popover.py`: opening by click and by keyboard, Escape and click-outside both closing it, a note round-tripping through save and a reopen, a bare highlight removed with no dialog at all (asserted by failing the test if one appears, not by auto-accepting it), a noted highlight's removal asking first, and declining that confirmation leaving the highlight and its note untouched. `test_reference.py` and the earlier highlight test files stay green — 63 tests total across all six highlight test files plus `test_reference.py`.

*Cost to change: low. `vendor-src/`'s `standalone.bundle.js` rebuilt.*

---

**7.161 — The home page's content moved out of `build.py` too, into `pages/home.md`, closing the pages/ pattern 7.159 started — and it needed two new pieces `read_page()` didn't have yet.** `render_index()` hardcoded six `.dl-module-card` tiles by hand and a `render_search_box()` call inline; unlike the About page, this content threads real markup (a badge, a meta line, a live search widget) through what looks like plain prose, so a straight copy of decision 7.159's approach wasn't enough on its own.

A ` ```card ` fence is the new fourth fence kind, alongside `exec`, `hint`, and `site` — the same header-line idiom (`HEADER_RE`, `SITE_HEADER_RE`, `HINT_HEADER_RE`) applied to a `url:`/`status:`/`meta:`/`wide:` block, followed by a markdown heading and an optional paragraph. `parse_card()`/`render_card()` build exactly the `.dl-module-card` markup `render_index()` used to write out by hand; `extract_page_cards()`/`place_page_cards()` follow `extract_blocks()`'s own extract-a-placeholder-then-substitute-the-real-markup shape. The `.dl-module-grid` wrapper is never written by hand at all — `place_page_cards()` wraps every run of one or more adjacent card placeholders in one automatically, the exact same "adjacent fences of a kind become one enclosing structure" rule `extract_blocks()` already applies to a site editor's consecutive html/css/js panes, so a page's own markdown never has to spell a grid out and get it wrong.

A `[[name]]` marker is the second new piece — infrastructure a page can point at but never author directly, `GENERATED_BLOCKS` mapping a name to a zero-argument renderer (`search-box`, today, wrapping `render_search_box()`). A bracketed marker rather than an HTML comment in the source, on purpose: a future markdown editor (dewnote, this decision's own reason for existing) renders a visible, clickable line, not an invisible comment node a reader could delete without noticing.

The third piece was not in the plan when this decision was raised, and was found rather than designed: `<div class="dl-hero">`/`<div class="dl-audience">` section wrappers in the markdown source came out of `to_html()` completely unconverted — headings, paragraphs, and all, as literal text — because Python-Markdown treats a raw HTML block as opaque through to its closing tag. This is not a new bug; it is the exact problem `convert_fold_bodies()`'s own docstring already names for a `<details>` fold, just met for the first time on a `<div>`. `convert_page_div_bodies()` is the same fix, generalised to `dl-hero`/`dl-audience`/`dl-attribution` (the attribution line moved from a bare `<p class="dl-attribution">` to a `<div>` of the same class for exactly this reason — `.dl-attribution` was already a bare class selector in `tutorial-style.css`, so the element changing costs nothing visually). `read_page()`'s pipeline is now: extract cards, extract generated-block markers, convert the whole body once, convert each section div's body a second time, then place cards and generated blocks back in — checked directly against a real build's HTML output at every step, not assumed from reading the code.

`write_index()` shrank the same way `write_about_page()` did in 7.159: `read_page("home")` replaces `render_index()`, which is deleted outright rather than left as dead code. `render_module_body()`'s own docstring, found stale while touching this area (it credited `render_index()` with a job that had actually moved to `render_tutorials_list()` when `all-tutorials.html` split off the module listing, well before this decision), is corrected alongside it — not this decision's own drift, but the kind CONTRIBUTING.md's "a stale comment is worse than no comment" rule exists for regardless of who caused it.

A real, pre-existing test-organisation bug was also found and fixed here, not introduced by it: 7.159's own edit had inserted `TestTheAboutPage` in the middle of `TestTheFrontPage`'s method list rather than after it, which — since a Python class's membership is decided by indentation and position, not by which docstring a test was written to sit under — silently moved three genuine front-page tests (`test_it_ends_with_the_short_attribution`, `test_it_links_to_current_courses_and_the_detail_pages`, `test_the_features_page_is_written_at_the_site_root`) into `TestTheAboutPage`. They still ran and still passed either way, so nothing was ever actually broken; it was a naming and organisation defect discovered while adding home-page tests to the same area, corrected by regrouping both classes properly.

One test needed more than a fixture update: `test_it_ends_with_the_short_attribution` asserted an exact single-line string, which no longer matches once the attribution is real markdown source wrapped at a comfortable line width — Python-Markdown keeps a paragraph's own internal line breaks rather than collapsing them to spaces the way the old hardcoded Python string did. Rewritten to normalise whitespace before comparing, which checks the same content without being coupled to how the source happens to be wrapped.

*Cost to change: low. Neither the card fence nor the generated-block marker touches how a tutorial's own `exec`/`hint`/`site` fences parse; `convert_page_div_bodies()` is scoped to three known class names, the same way `FOLD_RE` is scoped to `dl-hint`/`dl-answer`, so it can't reach into content it wasn't meant for.*

---

**7.162 — The masthead's Panels disclosure gave up Reference and Settings to four corner docks; Settings itself split into Notes+Report and Appearance+Imports & Exports.** Grew out of the resize-handle fixes in 7.15x (unnumbered in this log, but shipped as PR #220) and a real interactive prototype, `planning/mockups/corner-docks.html`, built on the site's own stylesheet rather than a design canvas. Series nav stays exactly where it was — its own toggle, still inside `#dl-panels-group`, still opening `.dl-seriesnav` — since nothing about it needed to move.

**Each side keeps one open panel at a time, not two floating independently — a deliberate simplification of the mockup, not a faithful build of it.** The mockup let all four corners open simultaneously, each a `position: absolute` panel sized to its own content. The real Reference and Settings panels are long, full-height, `position: fixed` sidebars, and letting a second one open on the same edge risked two panels visually colliding on a short viewport with no reservation logic to keep them apart. Instead the left edge became a three-way exclusion (Reference, Series, Documentation — `closeReference()`/`closeSeriesNav()`/`closeDocumentation()` each close the other two), and the right edge a two-way one (`closeNotesReport()`/`closeAppearance()`), extending the exact mutual-exclusion pattern Reference and Series already had. Only the *toggle button's* position moved to a corner; the panel it opens still docks full-height to its side exactly as `.dl-settings`/`.dl-reference` always did, so `watchPanelOverlap()`'s width-reservation math needed no change beyond adding the new panels to its `leftPanels`/`rightPanels` arrays.

**A real substring bug, caught by an existing test rather than by eye.** The natural name for the Notes+Report panel — `dl-notesreport`, and its corner toggle `dl-notes-toggle` — silently contains `dl-note` as a prefix, the exact literal string `test_a_note_is_removed_from_the_page_body` (`tests/test_build.py`) greps the pre-manifest page HTML for, to prove a `<aside class="dl-note">` pedagogical note never leaks into the static body instead of being extracted into the Reference panel's data. Renamed to `dl-yourwork`/`dl-yourwork-toggle` — a callback to the section's own original heading, "Your work" — once the false failure traced back to the id, not the actual note-extraction code. Any future id here needs to avoid starting with `dl-notes` for the same reason.

**`compose/dewmini.html` and the Mini IDE (7.84) both still have their own, unrelated `.dl-settings` panel, sharing `tutorial-style.css`.** Renaming the real `.dl-settings` panel's CSS to `.dl-yourwork`/`.dl-appearance` would have silently unstyled both — no test caught this until `test_dewmini_workbench.py` was checked by hand, since dewmini's own suite never asserts on computed style. Fixed by adding `.dl-settings` back into every shared selector list this rebuild touched (base panel positioning, the mobile bottom-sheet rule, the print rule, the minimal-header rule, the mobile toggle-padding rule) alongside the new panel classes, with a comment at the first one explaining why a class dead in `shell.html` is still there.

**Where the old eight Settings sections went is an editorial call, not something the mockup specified.** The mockup only sketched Appearance and Imports & Exports as names; it never said where "Running Python" (restart, hints) or "Progress" (the badges toggle) belonged. Appearance took Texture plus both of those, on the reasoning that all three are about how the page behaves and displays rather than moving data in or out; Imports & Exports kept Your own cells, Versions, Download, and Export unchanged. Every section kept its existing id (`dl-settings-work`, `dl-settings-texture`, and so on) even though none of them sit inside anything called `#dl-settings` any more — cheaper than renaming ids eleven call sites and several tests already key off, and the ids were never user-visible.

**The footer's "three doors" disclosure survives unchanged; the new Report tab is a second door to the same three links, not a replacement.** `report_doors_html()`'s own docstring already says why: it is a plain `<details>` element specifically so a reader can report a problem even if `tutorial-runtime.js` never finished loading. Folding it into a JavaScript-driven corner panel instead would have quietly lost that guarantee. `report_doors_panel_html()` is new, reuses `report_doors_links()` for the actual three links, and checks `feedback_enabled()` the same way `site_footer()` does — missed on the first pass and caught by `test_doors_gone_when_switched_off`.

**Documentation (bottom-left) is a real feature, not a placeholder** — Josh's call, reversing an earlier plan to leave that corner empty. `planning/curriculum/docs-links.yaml` is a small, hand-maintained `term: url` table (eight entries to start); `write()` filters it down to whatever also appears in the page's own cumulative glossary, the same "nothing not yet taught" rule `cumulative_glossary()` already enforces for Reference, and shows an empty-state message rather than hiding the toggle when nothing matches yet, since the table is expected to grow slowly rather than launch complete.

Tested in a live Playwright pass against the real built site (local Pyodide, not the CDN) rather than new named test files, given the scale of the rewrite: every corner's open/close/Escape/click-outside, both mutual-exclusion groups, Documentation's real matched links and their hrefs, the Report pane's real content, the Appearance/Imports & Exports pane switch and its search scoped to whichever pane is active, the notes textarea's autogrow surviving the move into its new panel, resize-and-persist-across-reload on the new panels, and the mobile bottom-sheet treatment applying to Documentation. Existing suites updated in place rather than rewritten: `test_reference.py`, `test_series_nav.py`, `test_saved_progress.py`, `test_student_notes_prose_only.py`, `test_progress_summary.py`, `test_progress_badges.py`, `test_versions.py`, `test_custom_cells.py`, `test_cell_hints_staged.py`, `test_cell_run_menu.py`, `test_phase0_golden_path.py`, and `tests/test_build.py`; `test_dewmini_workbench.py` needed no change at all, confirming the compatibility fix above actually worked.

*Cost to change: medium. The panel split (which sections live in which pane) is easy to re-shuffle — each section is still its own id-addressable unit. The corner-anchor-vs-independent-panel simplification is the part that would cost more to undo, since reversing it means designing the height-sharing/overlap-avoidance logic this rebuild deliberately avoided. `vendor-src/`'s `standalone.bundle.js` rebuilt.*

---

**7.163 — The wordmark, search, and Series toggle move out of `<header class="dl-masthead">` into the top-left corner dock, matching what the mockup actually showed; mobile becomes a genuinely different paradigm; the breadcrumb becomes a real, independently-collapsible tree.** 7.162 rebuilt the four corner docks but left the old masthead bar in place, which is most of why mobile looked doubled-up — two header rows stacked, one of them (the masthead's own search) fighting the corner tabs for the same cramped strip. `planning/mockups/corner-docks.html` had already folded the wordmark, orientation text, search, and Series into the top-left dock's own identity block; PR #227 built that. `compose/dewmini.html` keeps its own unrelated masthead untouched — it was never part of this dock system and nothing about it changed.

**Mobile is not a shrunk desktop layout — Josh's own call, explicitly inviting a different one.** A thumb has room for one button, not six, so all six corner-tab toggles collapse into a single launcher on narrow viewports: `.dl-mobile-fab`, the wordmark's own small orange dot grown into a real 3.25rem control, opening `.dl-mobile-menu`, a bottom-sheet list of plain buttons. Each forwards a real `.click()` to the actual (CSS-hidden) desktop toggle rather than duplicating any open/close/exclusivity logic a second time. This surfaced one genuine event-ordering bug: the forwarded click's *original* event kept bubbling to the same document-level outside-click listener that had just reacted to the forwarded click opening the panel, reading the original click's later arrival as "outside" and closing it right back. Fixed with `ev.stopPropagation()` on the menu item's own handler — the forwarded click and the original are two separate dispatches, and only one of them should ever reach the outside-click listener.

**The breadcrumb is a real tree, not a string.** `crumb_trail_html()` (`build.py`) builds three independently collapsible native `<details>` levels — all tutorials, this tutorial's module, its series — from `groups`/`members`, the same data `series_of()` already handed `write()` for the series-nav panel, so no second site-wide pass was needed. Only the innermost (series) level defaults open; a module or series with many members otherwise made the whole tree tall enough to push the Reference tab off the bottom of a shorter viewport (measured: `y=811` in a 600px-tall one before this, `y=548` after), so the top-left dock also caps its own height and scrolls internally as a backstop. Built with `role="list"`/`role="listitem"` on plain `<div>`s rather than real `<ul>`/`<li>` markup — the exact class of bug `report_doors_links()`'s own docstring already warns about, where an element that "reaches every page" silently inflates an unrelated test that counts a page's total `<li>` tags, and did in fact inflate six of them (`TestListsWrittenTightAgainstProse`) on the first pass.

**Column-width reservation became permanent, not conditional on a panel being open.** `watchPanelOverlap()` previously reserved `--dl-panel-left-w`/`--dl-panel-right-w` only while something was open over a corner; the identity block folded into this rebuild is wide enough on its own that a medium desktop width (measured at 800–1000px) could overlap real reading text with nothing open at all. `syncWidths()` now takes the wider of each side's resting corner-dock width or an open panel's.

**A second, more serious overlap was found afterwards, auditing every non-tutorial page type for the same chrome (index, tree, about, features, editor, all-tutorials, topics, module pages) — the identity block and the Notes+Report strip can each visually collide with the panel that opens beneath them.** Every panel (`.dl-reference`, `.dl-documentation`, `.dl-seriesnav`, `.dl-yourwork`, `.dl-appearance`) is a full-height `position: fixed` sidebar running from `top: 0` (or to `bottom: 0`) on its own edge, while that edge's own corner docks sit in front of it in z-index specifically so a toggle stays reachable while its panel is open (7.162's own reasoning). Nothing had ever reserved the *panel's own* header or scrolled-to-the-bottom content from that overlap — invisible for Reference (whose reference-toggle usually lands well below its identity block, since the block's own height already pushed it down) until a page with little breadcrumb depth, or an open Notes/Report panel on any page, put the two in exactly the same few dozen pixels: on one tutorial page, opening Reference put its own search box and glossary directly underneath the wordmark, breadcrumb tree, and search — fully illegible, not merely crowded. `trackCornerDockHeights()` (`tutorial-runtime.js`), the same pattern `trackChromeHeight()` already used for `--dl-chrome-h`, measures all four corner docks' real rendered height via `ResizeObserver` and publishes `--dl-corner-{tl,tr,bl,br}-h`. Each panel's `top`/`bottom` now clears the dock on its own side by that live amount (`.dl-reference`/`.dl-documentation`/`.dl-seriesnav` against `tl`/`bl`; `.dl-yourwork`/`.dl-appearance` against `tr`/`br`) instead of running flush to the viewport edge — correct whether a dock's content is a single fixed-height button row or a breadcrumb tree that grows and shrinks with how deep a page's series nesting runs. Mobile is unaffected: its own media query already overrides every one of these panels to a bottom-anchored sheet, further down the cascade, since none of the four corner docks other than the identity block itself even render past `34rem`.

**The "Panels" disclosure survived the fold-in as dead weight, and this audit is what surfaced it.** Once Reference got its own corner-tab button (this same PR), `#dl-panels-group` could only ever hold one button — Series — so `initPanelsDisclosure()`'s `hasChoice = available.length > 1` could never be true again. The details element was therefore *always* forced open and its own summary *always* hidden, on every page, which is a roundabout way of saying the disclosure had stopped disclosing anything; a caught-by-test symptom (`#dl-panels` reported `open: true` on load, when a test written for the old two-button group expected it closed) is what turned this up. Simplified rather than patched: `#dl-panels`/`#dl-panels-group`/the "Panels" summary are gone from `assets/shell.html`, and `#dl-seriesnav-toggle` sits directly in the identity block as a plain corner-tab button — it already carried its own complete standalone styling (border, padding, hover, `aria-expanded` state) from when it briefly needed to look right inside the group, so nothing about its appearance changed. `initPanelsDisclosure()` deleted from `tutorial-runtime.js` outright rather than left unreachable.

Tested with a live Playwright audit against every non-tutorial page type at desktop width (no console errors, no dock/reading-column overlap on any of them, Documentation correctly absent everywhere it should be) and against a real tutorial page's five panels individually (Reference, Documentation, Notes, Report, Appearance, Imports & Exports all open clear of the docks on every edge, confirmed both numerically via `getBoundingClientRect()` and visually via screenshot). Four new regression tests in `tests/e2e/test_reference.py` (`TestPanelClearsTheCornerDocks`) pin the geometry directly — a panel's edge against its paired dock's edge, with a 1px tolerance for the sub-pixel rounding `Math.round()` in `trackCornerDockHeights()` allows. `TestPanelsDisclosure` renamed to `TestIdentityCornerControlsAreDirect` and rewritten around the now-simpler markup rather than deleted, since "Series is a direct button, not a disclosure" is still a real property worth pinning down.

*Cost to change: low for the dock-height tracking (it is purely additive — a panel that stops needing it just gets an unused CSS variable) and the Panels-disclosure removal (already fully dead code by the time it was found). Medium for the mobile paradigm and the breadcrumb tree, the same way 7.162 rated the corner-anchor decision: both assume the current six-toggle, three-level shape, and a further toggle or a fourth breadcrumb level would need deliberate room made for it rather than falling out for free. `vendor-src/`'s `standalone.bundle.js` rebuilt again.*

---

**7.164 — A screenshot pass against the mockup, on every page type at three widths, found the phone identity block floating over the page and the desktop search popover clipped to nothing; the tabs and the top-left strip were brought back to what `planning/mockups/corner-docks.html` actually draws.** Josh's report was "I don't see the header moved to the upper left on PC everywhere, and on mobile I see just outlines, oddly placed." The live site deploys from `main` only (`.github/workflows/deploy.yml`), so what he was looking at was the #226 state — but the phone half of it was true of this branch as well, and a systematic pass (`full_pass.py`: ten page types × 1400/1024/390, every panel opened, geometry checked with `getBoundingClientRect()` rather than by eye) turned up four things 7.163's audit had not, because that audit ran at one desktop width.

**On a phone the top-left corner cannot float, because there is no column to reserve for it.** On desktop the identity block is kept clear of the reading column by `--dl-panel-left-w`; that reservation lives inside `@media (min-width: 34rem)` and is inert on a phone, where `.dl-page` has a 1rem gutter and nothing else. So `position: fixed` at the top-left put the wordmark, the search summary and the Series toggle — the last two reduced to icon-only squares by the mobile `.dl-toggle-label { display: none }` rule — directly over the Contents box and the first lines of every page. The old `<header class="dl-masthead">` never had this problem because it was in flow. The fix is the same shape: on a phone `.dl-corner-dock-tl` is `position: static`, one slim row under the nav with the wordmark at one end and search at the other, scrolling away with the page; Series joins the launcher as "This series" so the row holds nothing that needs a label a phone has no room for. That surfaced an ordering bug of its own: `initMobileLauncher()` mirrors each toggle's `hidden` once at load, and ran before `initSeriesNav()` had unhidden the Series toggle, so the launcher row stayed hidden on every page — moved after it.

**A scroll box clips what is positioned outside it, and the search popover is exactly that.** 7.163 had capped `.dl-corner-dock-tl` with `max-height` and `overflow-y: auto` so a deep breadcrumb tree could not push the Reference tab off a short screen. `overflow-y: auto` forces `overflow-x` to `auto` too, and the `.dl-search-results` dropdown is absolutely positioned 26rem wide below a dock 12rem wide — so on desktop the results rendered entirely outside the dock's box and were clipped to nothing; the input itself was cut off at the dock's right edge. The cap moved to `.dl-crumbtrail`, the one thing in the dock that actually grows, with 12rem held back for the wordmark, search and strip beneath it.

**Two departures from the mockup that had no reason behind them.** The mockup's tabs are filled white with a drop shadow; the build's `.dl-corner-tab` had `background: none`, so over the page's own off-white a tab read as a stray border — "just outlines" is an accurate description of a transparent bordered button. Filled with `--dl-panel-bg` and given `0 2px 8px var(--dl-shadow)` now, so it reads as a control docked in front of the page in both themes. And the mockup shows one two-button strip directly under the identity text; the build had Series as a rounded button inside the identity block and Reference as a corner tab outside it, two styles stacked. Both are `.dl-corner-tab` in one `.dl-corner-strip` now, joined the way Notes+Report already were, with `.dl-seriesnav-toggle`'s duplicate button styling deleted rather than left to drift.

The pass is published as a contact sheet (every screenshot, the mockup checklist, before/after pairs) rather than described, since the question was visual. The remaining differences from the mockup are the deliberate ones 7.162 already records — Documentation in the bottom-left instead of the top-left strip, full-height sidebars instead of floating cards.

*Cost to change: low. The phone row is one media-query block; the tab fill is two declarations; the strip is markup. The launcher ordering is the one thing to keep in mind — any new toggle the launcher mirrors has to settle its own `hidden` before `initMobileLauncher()` runs. `vendor-src/`'s `standalone.bundle.js` rebuilt.*

---

**7.165 — Two upper docks and nothing above the page: the top bar, the Series panel, the Documentation panel and the in-page Contents list are gone; the where-you-are tree runs five rungs deep, down to this page's own sections; the right side is one vertical stack; on a phone the launcher is a full-width sheet rising from a bottom-centre dot.** Josh's direction after the 7.164 contact sheet, first as a playable mockup (`planning/mockups/upper-docks.html`, built on the real stylesheet the way `corner-docks.html` was), then built for real once he had clicked through it. Every choice below is his; what follows is what each one cost to make true.

**The top bar's four jobs all already had a home in the tree, so the bar went rather than being thinned.** "All tutorials" is the tree's first rung; previous and next are the two neighbours of the bold line in its series rung, and survive as the page's own bottom navigation for anyone who reads to the end; search is the bar beneath the tree; Contents is the tree's new innermost rung. `#dl-chrome` is gone from `assets/shell.html`, and `trackChromeHeight()` publishes `--dl-chrome-h: 0px` when it finds no bar — the stylesheet's own 6rem default still serves `compose/dewmini.html`, which keeps a real bar — so the status line and anchored jumps measure from the top edge. Docks and panels stopped depending on the variable at all: they start at `1rem`.

**Contents became a rung of the tree rather than a list in the page, and the same code serves both the page and its downloadable copy.** `contents_rung_html()` (`build.py`) is `render_toc()`'s logic — sections at heading level 2, non-repeating sub-headings nested under them, nothing for a page with fewer than two sections — emitting `role="list"` divs like the rest of the tree instead of `<ul>`/`<li>` (7.163's reason). It hangs off a fourth rung, this tutorial's own name, which opens by default so a reader sees there is something beneath it; a page with too few sections for a contents rung gets its name as a plain line, not a caret with nothing behind it. `standalone_html()` used to strip the whole tree from a downloadable copy because its links cross files; now it keeps exactly the contents rung, whose links point inside the file and work from a student's disk — the one part of the tree the old inline list had always kept.

**Series went as a panel because the tree already showed everything it did.** `render_series_nav()`, `initSeriesNav()`, `closeSeriesNav()`, the `{{SERIES_NAV}}` token, `.dl-seriesnav*` and `tests/e2e/test_series_nav.py` are all deleted rather than left reachable from nowhere; the series rung's own build tests (`TestTheSeriesRung`, formerly `TestSeriesNav`) pin what the panel's did — order from the order file, the current page marked and unlinked, an archived page listing only itself. Documentation went the same way — `load_docs_links()`, `planning/curriculum/docs-links.yaml`, `initDocumentationDock()`, `renderDocumentation()`, the `docsLinks` manifest field — on Josh's "we currently have no use for it"; 7.162's reasoning for it stands if it ever comes back, and a lookup table is a small thing to re-add.

**The block is as wide as the panel beneath it, but gives ground before the reading column does.** `--dl-side` is `clamp(14rem, calc((100vw - 30rem) / 2), 22rem)`: 22rem on a wide screen so a line like "Programming and Maths, Integrated" reads whole, shrinking on a laptop-sized window because `.dl-page` reserves twice the wider dock and would otherwise fall below its 26rem floor at 1024px. The Reference panel takes the same width so block and panel read as one column; the panel's top follows the dock's tracked height, which now changes whenever a rung opens or closes, so `trackCornerDockHeights()`'s `ResizeObserver` earns its keep.

**A rung of the tree is not a click away from the panel beneath it.** Found by the screenshot pass, not by eye: with Reference open, opening the Contents rung closed it, because Reference's own outside-click listener exempted only the *right* dock (so the right-hand panels can be used alongside it) and never its own. Both docks carry an id now (`dl-dock-left`, `dl-dock-right`) and sit in `LEFT_DOCK_IDS`/`RIGHT_DOCK_IDS`, so anything inside a dock — a rung, the search bar — counts as inside for every panel on that side.

**On a phone, one row at the top and one dot at the bottom, and everything else rises from the dot.** The launcher moved from the bottom-right corner to bottom centre — the wordmark's own dot, at the one place on a phone nothing else lives — and its menu is a full-width sheet of rows at least 3.25rem tall in 1rem type, with 5rem left under the last row so the dot never covers a control; every panel sheet leaves the same room. The tree, which has no place in a one-line identity row, is "Where you are" in that menu: `initWhereYouAre()` moves the one real `.dl-crumbtrail` node into a sheet of its own on a narrow viewport and back into the dock on a wide one, rather than rendering the tree twice, so which rungs are open stays one fact. Following any link in it closes the sheet, since the jump was the point.

**Icons on every tab**, Josh's ask, as inline SVG in `currentColor` — the same choice `nav_search_html()`'s magnifier already made, so they follow the palette in both themes. Reference keeps the CSS-drawn book it had.

*Cost to change: medium, for the same reason 7.162 rated the corner-anchor decision so — the tree now carries navigation the page has nowhere else on desktop, so putting a bar back is a design reversal rather than a restore. The deletions are cheap to undo from history if either panel is wanted again. `vendor-src/`'s `standalone.bundle.js` rebuilt.*

---

**7.166 — The search bar is the search field.** Josh, clicking through #228: "the search isn't happening in the search field." It wasn't: `nav_search_html()` had been a `<details>` since the masthead days, and 7.164 styled its summary to look like a field — so a reader saw a bar, typed, and nothing happened until they noticed the popover with the real input inside. A control that looks like a field has to be one. `nav_search_html()` now returns `render_search_box()`'s own widget directly — the same `.dl-search` markup the front page and "All tutorials" carry, which `assets/search.js` already finds by class and wires without knowing where it sits — with the input styled as the bar, the label kept for screen readers only, the hint paragraph hidden (a placeholder does its job in a bar), and the results list floating beneath as a wider dropdown. `search.js` lost its `<details>`-specific outside-click and Escape handling, since no popover exists to close any more; the results list still closes on an outside click, as every panel does. On a phone the input takes the rest of the row beside the wordmark and its results hang the full width of the screen.

*Cost to change: trivial. One function, one block of CSS, and the widget underneath is the one every other search on the site already uses.*

---

**7.167 — Five right-hand panels instead of two; the page's own title in the tree is the rung that opens onto its sections; a page of problems sits under its tutorial; Versions moves out of a panel and into the tree.** Josh, after merging #228: "think through the panels on the right as I think there are some divisions within Appearance etc that we could break off to make clearer" — then "go for it", and mid-build, "instead of 'contents' and then another dropdown we can just have it in the title of the tutorial … not sure where practice goes btw."

**The split follows what a reader is doing, not what the code happened to group.** The old right side was two tabs — Notes+Report and Appearance — and Appearance had become the panel for everything that was not notes: how the page looks, how Python runs, which release you are on, your own cells, downloads, exports. Those are five different errands. The five panels are now Notes (your notes and your progress), Report (the report doors), Python (execution — what used to be Appearance's "Execution" section, and the one people open when a cell will not run), Appearance (texture only, with its search now scoped to just that), and Imports & Exports (your own cells, download, export). Each is one `.dl-right-panel` in `assets/shell.html`, and `RIGHT_PANELS` in `tutorial-runtime.js` is the single list the mutual exclusion, the outside-click rule, the saved-open-state and the overlap watcher all read from, so a sixth panel is one markup block and one string. The tabs keep their order top to bottom as the errands run from "mine" (notes) to "leave with it" (exports).

**The tree's own line is the caret.** #228 put a "Contents · N sections" rung under the bold current-page line in the series list, which printed the same title twice a line apart and asked for two clicks to reach a section. Josh's fix is the honest one: the page's own item in the series list *is* the `<details>` — `<summary>First Steps <span>5 sections</span></summary>`, closed by default, opening straight onto the sections (and, at the end, the page's own practice) — and a page with nothing behind its name is a plain bold line, no caret. `crumb_trail_html()` (`build.py`) renders it in place of the current-page item; `contents_items_html()` (the renamed `contents_rung_html()`) provides just the list. The caret hangs in the list's left padding (`margin-left: -0.6em` on the summary, the caret's width at its own font size) so the title stays aligned with its sibling links. `initVersionsSection()` still finds it by `.dl-crumb-level-4` — the leaf keeps that class beside `dl-crumb-current` for exactly that reason — and the standalone copy's `keep_contents` keeps the same `<details>` it did.

**Practice goes under the tutorial it belongs to, both ways.** On a tutorial page, its practice page (and any mixed-problems page that covers it) is the last line behind its own caret, in the orange link colour and by its own title — "First Steps — Practice", "Mixed Problems — Programming" — with no "Practice:" prefix, since every practice title on the site already says what it is and a prefix made the line say it twice. On the practice page, the tree is the *owner's* series rung, with the owner as a plain link and the page of problems nested one level under it as the bold current line, opening onto its own sections. So the relation reads the same from either end without either page being marked twice.

**Versions is a where-you-are question.** Which release of a tutorial you are reading belongs beside the other answers to "where am I", not in a panel about exporting. The `#dl-settings-versions` section is still marked up in Imports & Exports (the shell is one file; the tree is built per page), and `initVersionsSection()` moves it under the page's own rung at runtime when the page has two or more releases, at the tree's own size; a one-release page removes it as before. Judgement call recorded: since the rung starts closed, Versions is only visible once a reader opens their own page's line — the page's own dated switch under the `<h1>` remains the first place a reader meets the choice, and the tree's copy is the fuller one with "where I left off / the newest".

**What the pass checked.** All five panels open, clear of the dock, on desktop, laptop and phone, with no console errors; the tree open on a tutorial, on its practice page, and on a two-release tutorial with Versions under the rung; the phone sheet with the tree open. Unit tests: `TestTheContentsOfAPage`, `TestTheCrumbTrail` (two new cases — the own rung is the line in the series list and is printed once; a page of problems sits one level under its tutorial), `TestTheStickyChrome` (five tabs, five icons). The affected e2e files pass except the two failures already present on `main` in this sandbox.

*Cost to change: low for the panel split (a section is still an id-addressable unit; moving one between panels is a cut and paste in `shell.html`), low for the practice lines (one list comprehension). The own-rung-in-the-series-list shape is what `initVersionsSection()`, `keep_contents` and the golden-path e2e all address by class, so changing its markup means changing those three together. `vendor-src/`'s `standalone.bundle.js` rebuilt.*

---

**7.168 — The search is a line of text under the wordmark that opens into the field; the Python tab wears the Python logo; the "Header: full / minimal" setting is removed as a setting for a header that no longer exists.** Josh, on the 7.167 screenshots: "maybe we have the search for a topic as text with a search icon below dewlab and then on click or tap it becomes a search bar which searches all tutorials (trying to eliminate redundancy and make things grouped semantically)… can we have a Python logo next to Python instead of the arrow and is there any other setting that we need to move or change?"

**The block is lines, and the search is one of them.** 7.166 made the search a full field beneath the tree, which was right about *what* it was (an input) and wrong about *where*: a field-shaped control under a column of small text read as a second thing in the block. `nav_search_html()` is now a `<details>` whose summary is a magnifier and "Search for a topic", set exactly like the tree's rungs and placed between the wordmark and "All tutorials" — search everything, then where you are. Open, it is the same `render_search_box()` input as before, so 7.166's lesson holds: what appears is the field itself, not something styled to look like one. `search.js` focuses the input on `toggle` (a reader clicks once, not twice) and Escape on an empty field folds it back up and returns focus to the summary. On a phone the summary sits at the far end of the top row from the wordmark and the field drops below the row at the screen's full width, results in flow beneath it in the same sheet, capped at 70vh.

**The Python logo, in one colour, from the tab's own `currentColor`.** The Python Software Foundation's trademark policy allows the logo, unaltered in shape, to be used to refer to Python; a single-colour rendering is one of the forms it names. The path is the widely used monochrome path (Simple Icons, CC0), in a 24-unit box like the other tab icons. The policy does not permit reshaping it, so it is not restyled to match the stroke weight of the hand-drawn icons beside it — recorded so nobody "tidies" it later.

**A setting whose object is gone is not a setting.** "Header: full / minimal" tightened the old masthead bar; with the bar gone (7.165), "minimal" had come to mean "hide the where-you-are tree and shrink the tabs", which nobody asked for and the label did not say. The row is gone from Appearance, `data-header` from the runtime's defaults, `applyTexture()` and the shell's early-apply script, its rules (and the `.dl-nav-top` rules that only the old bar used) from the stylesheet, and its e2e test. A saved `header` key in an existing reader's `dewlab:texture` is simply ignored. `docs/FOR_STUDENTS.md` no longer promises it. Looked for and kept: everything else in Appearance describes something still on the page.

**One panel with tabs, or five tabs each with a panel — the same thing, and the dock already is the tab strip.** Josh asked whether all settings would be better in one panel with tabs between them. The five right-hand tabs are mutually exclusive and open in the same place, so switching between them is switching tabs; a second tab strip inside the panel would be the same control twice. What the question points at is visual: the open tab and its panel do not yet read as one object, since the panel starts below the whole stack. That is a styling pass (join the pressed tab to the panel's top edge), left for a later decision rather than folded into this one.

*Cost to change: trivial for the search (one function, two CSS blocks, a dozen lines of `search.js`); trivial for the icon (one path); the header setting is cheap to restore from history but there is nothing for it to act on. `vendor-src/`'s `standalone.bundle.js` rebuilt.*

---

**7.169 — The search line is the field: no fold, no second bar, on any width.** Josh, on 7.168: "a tap or click on the icon or text puts a cursor in front of the text and then as the user types the text 'search for a topic' goes away and the results just appear below without another search bar … I don't think we need our border button on mobile with this behavior."

7.168 had the right line and the wrong mechanism: a `<details>` whose summary was the words and whose body was the field, so a reader saw one bar, clicked, and got a second. The line is now `render_search_box()`'s own input, drawn with no border or background, "Search for a topic" as its placeholder set in the tree's small capitals (on `::placeholder` only — `text-transform` on the input would capitalise what a reader types), the magnifier over its left padding with `pointer-events: none` so a click on it lands in the input. Native placeholder behaviour does the rest: the words vanish at the first character and the results drop beneath. `search.js` loses the fold code it had gained a day earlier; `nav_search_html()` is back to one `<div>`.

**No focus ring, deliberately.** Chromium treats every focused text input as `:focus-visible`, so a ring "for keyboard users only" boxed the line on every mouse click — the bordered control Josh was asking to be rid of. The caret is a text field's own focus indicator; the magnifier and the words turn orange on focus and hover as well.

**On a phone the row is the wordmark and the words, and the results drop below the whole row.** `.dl-search` (the widget's own wrapper) is `position: relative` by default, which made the results hang from the field rather than the row; on a phone it is static, the row is the positioned ancestor, and the list runs edge to edge beneath it. The identity-row e2e test, which had pinned `position: static` on the row as its "in flow" check, now accepts relative too — relative is in flow — and the fold's summary-focus e2e check is replaced by a click on the magnifier landing in the input.

*Cost to change: trivial — the same three files as 7.168, with less in each.*

---

**7.170 — The reading column sits between the docks, reserving each side for what is on it; the Width control works again.** Josh: "can you check that the settings stuff isn't broken (I think width in particular is still behaving oddly)." Measured, it was: at 1440px the column was 598px whatever Width said, at 1280px 490px, and on a 1024px laptop opening Appearance left 218px of text. The rule was `min(--dl-line-width, 100vw - 2 * max(left, right) - 1rem)` — the column centred on the viewport, so *both* margins reserved the wider side, the 22rem left dock, and 824px of a 1440px screen went to margins before the reader's setting was consulted. The runtime comment even said so ("reserves TWICE whichever side's panel is wider, so the centered column doesn't skew").

Now each side reserves its own dock or open panel plus a gutter, the column takes the room between them up to the chosen Width, and it is centred on the viewport whenever that fits — shifted only as far as the docks demand (a `clamp()` on `margin-left` between the left reservation and the right one). A 26rem floor, the narrowest Width preset, holds even when a panel is open on a small screen: there the panel overlaps the column's edge, which is the lesser evil against text 218px wide, and the reader opened that panel. (`.dl-page` is border-box, so the reader's Width has always included its own 2.5rem of side padding; the first cut of this rule subtracted that again and shorted the column by 45px — caught by the new test's floor assertion.) `makeEdgeResizable()`'s drag cap mirrored the old arithmetic and now mirrors the new. Measured after (root font 18px, so 34rem is 612px): at 1440px with the panels closed, narrow is 612px and the widest setting 724px — capped by the docks, honestly; with Appearance open, the 22rem left dock and the panel leave 571px whatever the setting, so the control shows its effect once the panel closes; at 1280px the default fits with the panels closed; at 1024px the 26rem floor holds with Appearance open, where the old rule gave 218px. What remains is the docks' own width: a narrower left dock would hand the column more, and that is a design choice about the tree's long lines rather than a bug.

The two things wider than the column — the knowledge map and the tree page's layout — centred themselves on the column with a 50% margin and a -50% translate; with the column off-centre that pushed the tree page 34px past the right edge of a 900px window (its own never-scrolls-sideways e2e test caught it). They centre on the viewport now, stepping back over the column's offset, which the column rule publishes as `--dl-col-left`.

**And the column starts level with the docks.** Josh, reviewing: "the top of the text… I think they are now on 3 different levels?" They were: the docks sit 1rem down, the column started at 0, so the Python status line (and the heading, once that line has gone) sat above the wordmark and the first tab. Measured: wordmark line box at 25px, the Notes label at 28px, the status box at 0 and the heading at 112px. The column takes `padding-top: 1rem` in the same desktop rule, which puts the status box's top edge on the docks' top edge, its text level with the wordmark and the tab label, and the heading's cap height level with both once the line hides. The phone row is in flow and unaffected.

*Cost to change: trivial — two CSS rules and one function, and an e2e test that pins both the live control and the floor.*

---

**7.171 — A Programming and Design Principles module of its own, made of tutorials the integrated module owns: an order file may list `module/slug`.** Josh: "can we make a separate programming design principles module that isn't integrated with the maths module? But let's put that card last after web authoring … we should already have the content so it's just a matter of a new set of series and maybe a couple links."

The content is the programming half of `mit-pdp-maths-prog-integration` — the Programming Foundations series (ten tutorials, first cell to reusable tools, which `planning/CURRICULUM_MAP.md` maps onto all twelve PDP outcomes) and the two team-project tutorials that are how the module is assessed. Moving those files into a new folder would take them out of the integrated course; copying them would make every future edit a two-file edit and split the saved work of anyone who had been reading the copy. So neither. A series' order file may now name a tutorial from another module as `module/slug`, and `series_of()` puts that tutorial in the listing series as well as its own: it appears in the listing module's series list, module page and downloads, while its page, its URL, its place in the where-you-are tree and its previous/next stay with the module that owns it. Its `order` — its position in its home series, which the reference panel's "earlier in the series" accumulation reads — is left alone. Listing a slug from the same module in that form, or a slug that no live tutorial has, stops the build.

`tutorials/programming-design-principles/` therefore holds two order files and nothing else: `programming-foundations` and `working-in-a-team` (critique and reflection, then the team project). A module with no tutorial has no frontmatter to be named from, so `module_titles()` — now the one place all four callers get a module's name — falls back to a `title` in `MODULE_INFO`, where the module's code and description already lived. It is last in `tutorials/modules.yaml` and last among the course cards on the front page, after Web Authoring, as asked. Capstone Project is not in it: it draws on the maths series.

*Cost to change: low. The borrowed form is a dozen lines in `series_of()` and one resolution table; the module itself is two small files, one card and one dictionary entry, and deleting those returns the site to what it was.*

---

**7.172 — The features page's content moved out of `build.py` too, into `pages/features.md`, closing the last hand-written page.** `write_features_page()` was the third and last page rendering from a hardcoded HTML string; every list on it is a `<ul class="dl-feature-list">` (a grid layout, not a plain bulleted list — `tutorial-style.css`), which raised the same problem `convert_page_div_bodies()` (7.161) already solved for `<div class="dl-hero">`/`<div class="dl-audience">`, met on a different tag: Python-Markdown treats a `<ul>` opening a raw HTML block exactly the way it treats a `<div>` one, so a markdown bullet list written inside it would otherwise reach the page as literal, unconverted text.

Reusing the fix outright didn't quite work, though: a markdown bullet list converts to its own `<ul>…</ul>`, and splicing that whole thing inside a `<ul class="dl-feature-list">` wrapper that already supplies the real opening tag produces `<ul class="…"><ul><li>…</li></ul></ul>` — invalid HTML, since a `<ul>` can only directly hold `<li>` children. `convert_page_div_bodies()` is renamed `convert_page_wrapper_bodies()` (its own name no longer fit once a `<ul>` joined the `<div>` classes it started with) and gains one small branch: when the wrapper tag is `ul`, the freshly re-converted body's own redundant `<ul>`/`</ul>` is stripped before splicing, keeping only its `<li>` items — `PAGE_DIV_RE` becomes `PAGE_WRAPPER_RE`, now matching either tag with a backreference (`(?P<tag>div|ul)` … `</(?P=tag)>`) so the open and close always agree.

Wording, structure, and every link are unchanged — checked directly by rebuilding and diffing against the previous hardcoded output, the same discipline 7.159 and 7.161 both used. Naming settled directly rather than guessed at: dewlab's own `Cell`/`CELL_TYPES`/`render_cell()` already reserve "cell" for something that runs, with real state and a saved-progress contract behind it (CLAUDE.md's own warning about renaming a cell id), so a card — no output, nothing to save — stays a **card**, "fence" reserved for prose specifically describing the markdown mechanism it rides on. dewnote's own vocabulary has no such collision (its own plan already uses "cell" for any boxed unit, not only a runnable one), so it is free to call its rendered version of the same thing a "card cell" without stepping on anything.

*Cost to change: low. The `ul`-stripping branch is additive to `convert_page_wrapper_bodies()` and does nothing for a `div` wrapper; the rename touches only this file's own two names and their one call site in `read_page()`, not any dialect a tutorial or another page's frontmatter depends on.*

---

**7.173 — Placement moves out of the tutorials and into `courses/`; a tutorial's id is its folder name, site-wide; one page per tutorial at `tutorials/<id>.html`, drawn for whichever course the reader is following.** Josh, after 7.171 shipped: "how would you suggest we solve this problem if tutorials and practice can be part of multiple modules and multiple series?" and then, from scratch, "if someone challenged you to make an even simpler process… would you change anything?" — then "Let's merge and make the whole thing happen!" The planning lived in a temporary `refactor/` folder (deleted with the last step; the pull request that carried it is the record).

**What a tutorial's file knows about itself: nothing about where it sits.** `slug`, `module`, `module_title` and `series` are gone from the frontmatter, and the build refuses them (`MOVED_FRONTMATTER`), since an ignored field is a field somebody will keep writing. `tutorials/` is flat: `tutorials/<id>/<id>.md`, its practice page `<id>-practice.md` beside it, frozen releases `v<version>.md`, the glossary, the pictures. The id is the folder name (`id_of()`), site-wide; the filesystem refuses a second folder and `load_all()` refuses the other way it can happen. Exactly one id collided: Computational Methods' `first-steps` is `first-steps-cm` now, with a redirect and a storage migration (below).

**Where it sits is a course file.** `courses/<course>.yaml` holds the title, code, status, card text and description, and `contents:` — a list of series, each a heading with the ids under it in reading order; `mixed:` lists mixed problem sets; `courses/index.yaml` orders the courses. A tutorial on two courses is listed twice, and that is the whole of it: 7.171's borrowed `module/slug` form, `tutorials/modules.yaml`, every `<series>.order.yaml` and `series.yaml`, and `MODULE_INFO` in `build.py` are gone. A series is keyed by its heading (`series_key()`, "Python fundamentals" → `python-fundamentals`), which names its zip and the page's series meta, so the old download names survive. The reference panel accumulates through the course the reader is following, series by series in the course file's order — the special case 7.104 gave an unlisted series is not needed once a series a course leaves unlisted is simply not on that course.

**One page, one address, chrome per course.** The build writes each page once, with the tree, previous/next and "This page is also part of …" of its default course — the first in `courses/index.yaml` that lists it — and writes `assets/routes.json` (every course's contents, by id) for the runtime. A page on more than one course carries a course chooser on the tree's course rung; a course page remembers itself in `dewlab:course` on arrival, so opening First Steps from the Programming and Design Principles card shows that course's tree, previous and next, and the other course in the line under the heading (`initCourse()`, `drawCourseChrome()`). The reference panel's accumulation stays the default course's for now; a per-course accumulation is the one part of the plan left for another day, and nothing breaks without it. Course pages stay at `<course>.html` at the site root, where the home page and every list already pointed.

**Keys and addresses survive.** Saved work was keyed `dewlab:<kind>:<module>:<slug>`; it is `dewlab:<kind>:<id>`. The manifest of every page that had an older address carries `legacy` (the old `module:slug`, read from `courses/redirects.yaml`), and `migrateStorage()` renames that page's keys on the first visit, never overwriting work saved under the new key since. `write_redirects()` writes a small page at every old address the same file lists; a line that would sit on a real page, or point at nothing, stops the build. A saved-work file names its page by `tutorial-id`; an older file naming module and slug still fits the page whose `legacy` says so.

**What the build says rather than refuses.** An id a course lists with no folder behind it stops the build, naming the course file and the series (the dangerous direction: the file looks complete and the course is quietly short). A tutorial no course lists builds, at its address, with a note. A draft a course lists is skipped with a note. Two pages with one title are noted, naming both and their courses; two live tutorials covering three or more of the same outcomes are noted. An archived tutorial may stay listed and lands in the course's Archive, off the route — the previous rule made listing it an error, and a line a contributor has to delete on archiving is a line they will forget.

**The suite is re-cut around the objects the build has.** `tests/test_build.py` (407 tests, one file) is `tests/build/`, one file per thing the build reads or writes, with helpers that write the new layout; the browser suite's fixtures are a course file; new tests pin the charter in the plan — the id collision, the placement field left in a file, the typo in a course file, the unlisted tutorial, the renamed key, the old address, the course chooser, "also part of", accumulation not crossing courses, the repeated title, the overlapping coverage. `check.py` at the root is the contributor's tool (`docs/CHECK_YOUR_WORK.md`): every Problem it reports is a build failure — a parametrised test runs both over the same trees, one mistake each, and that test moved an empty `contents:` from Problem to Note, since the build accepts a course with nothing on it yet — and when a check of one thing is clean it offers to open a pull request from GitHub's own new-pull-request page, with the title and description written from what was checked. CI gains a `browser` job for the four e2e files that never run a cell (the reference panel, the phone layout, link contrast, the course chooser); the phone identity-row regression in #230 reached `main` with CI green because none of them ran there, and this is what the tests charter said would have caught it.

*Cost to change: high, and meant to be. Folder names are addresses and storage keys now, so the layout is a contract with every reader's browser; the course files are the one place placement lives, so a return to placement-in-frontmatter would be the migration run backwards. The parts that are cheap: the warnings (a threshold each), the also-part-of line, the chooser, and routes.json, each additive.*

---

**7.174 — One idea of word matching for every search box: `assets/search-words.js`.** Josh, after #235 (prefix matching on the contents-page search, from another session): "make all search boxes involve prefixes … perhaps prefixes and stemming? … we want the most semantic and easy to use search generally — the same should be true of our tooltips and other searching and helping."

`search.js` already stemmed (loops → loop), mapped a modest synonym list (chance → probability) and, since #235, took a prefix of three letters or more. The other four boxes — the Reference panel and its two Basics tabs (`tutorial-runtime.js`), dewmini's Library (`compose/dewmini.js`) and the editor's link picker (`editor.js`) — matched a raw substring and nothing else, so "loops" found *Loops and Lists* on the search line and nothing in the Reference panel one click away. The stopwords, synonyms, stemmer, tokeniser and hit rule move out of `search.js` into one module the five import, plus `textMatches(text, query)` for the filters: the raw substring first (what every filter did before, kept so a two-letter fragment or `print(` still narrows), else every query word, normalised, is a word of the text or a prefix of one. The runtime's import bundles into the standalone copy as its other imports do; dewmini's offline bundle gains the file in `DEWMINI_ASSET_FILES`. Two browser tests in `test_reference.py` pin a stem, a synonym, a prefix and a fragment on the panel, and a synonym and a stem on the search line; both run in CI's browser job.

Not done, and named so it is not mistaken for forgotten: the pre-run tooltips are jedi's, over Python's own names, and the highlight-to-look-up offer matches a glossary term exactly on purpose (a reader has selected a word, not typed a guess). Neither is a search box.

*Cost to change: trivial. One module, five one-line imports; the synonym list is the part that will grow, and it grows in one place now.*

---

**7.175 — The site's own pages: one writer, a section in the writing guide, and the home page reordered.** Josh: "what is the story with pages? Are there documentation things about that?" — and then a new order for the home page.

`pages/home.md`, `about.md` and `features.md` were described in one paragraph of ARCHITECTURE.md written for whoever changes the build, and nowhere for the person who wants to reword the About page; that paragraph also still called the search box the one `[[name]]` marker, a day after `[[course-cards]]` joined it. `docs/WRITING_TUTORIALS.md` gains "The site's own pages": the three files, the one frontmatter field, the card fence, the two markers, the four wrappers, and where the built page lands. `write_index()`, `write_about_page()` and `write_features_page()` — three copies of one function differing in a file name, a crumb and a bottom-nav link — become `write_page(name)` over a `SITE_PAGES` table, the tidy the refactor's document review named and did not require.

The home page, in Josh's order: the two opening paragraphs, then the "What dewlab can do" tile inside that first section, then one section — *What do you want to learn?* — holding the sentence about searching, the search box, a sentence pointing at the courses, the recommendation, and the course tiles; then the attribution, now ending with where to find out more (the About page and the repository). Gone: the separate "Find a tutorial" and "Choose a course" sections, the "All tutorials" tile (every page's bottom nav carries that link), and the line under the search box saying what a search matches — on this page only (`render_search_box(hint=False)`), since the sentence above the box already says it; the all-tutorials and topics pages keep theirs. Josh's draft lines went through the nine checks and `planning/PLAIN_LANGUAGE_PASS.md` records what changed and why.

One test fixed in passing: the check that a downloaded copy carries no navigation looked at everything after the last `</style>`, which since 7.173 includes the inlined runtime, whose course-chrome code names `.dl-nav-bottom`; it now checks the markup outside style and script, which is what it meant.

*Cost to change: trivial. Prose in one file; `write_page()` is a table entry per page.*

---

**7.176 — A line off the home page, and what taking it off turned up: the build suite CI was not running.** Josh: "Can we remove the horizontal line?" — the rule between the home page's opening and *What do you want to learn?*, which was `.dl-audience`'s top border and padding in `tutorial-style.css`. Gone; only the home page uses that wrapper.

Rebuilding to check it, without `--clean`, stopped on `courses/redirects.yaml`: a page from before 7.173 was still under `site/tutorials/computational-methods/`, and `write_redirects()` read "a file is here" as "this build wrote a page here" and told the contributor to delete the line — the wrong advice, for anyone who built before the addresses moved and builds again. It now takes the list of pages the build wrote and consults only that; a stale file at an old address is overwritten by the stub, which is what the address is for. CLAUDE.md said a plain build writes `site/` from scratch, which only `--clean` does; it says `--clean` now.

Then the build tests: two failed, on `main`, with CI green. `pytest tests --ignore=tests/e2e` collected 208 tests here and in CI, and `tests/build/` alone holds 446, because pytest's default `norecursedirs` skips any folder named `build` — so from the moment 7.173 moved the build tests into that folder, neither CI nor the documented `python3 -m pytest` ran them, and 7.175's "one test fixed in passing" fixed a test nobody ran and left it failing. `pytest.ini` sets `norecursedirs` to pytest's own list minus `build` (plus `site` and `vendor-src`), and the same command collects 654. The two failures: the practice test for a `mixed:` id that is not a mixed set listed the id under a series too, so the build's earlier check ("under `mixed:` and under a series") fired first — the test now lists it under `mixed:` only; and the downloadable copy carried the search line (7.169), which fetches the site's index to find other pages, neither of which is on a student's disk — `standalone_html()` strips it with the rest of the cross-file navigation.

*Cost to change: trivial each. The lesson is the collection count: a green job that ran 208 tests looked the same as one that ran 654, and the number in CLAUDE.md is now the one to compare against.*

---

**7.177 — The build suite, re-cut from one fact per test to one scenario per test: 446 tests become 199.** Josh: "Can we make the test suite less arduous? That's just a lot of tests" — and, while it was being done, "let's make sure that our tests still are testing sensible things given all the recent changes."

The shape was the problem. Each test in `tests/build/` wrote a tiny repository, ran the whole build over it, and checked one fact; a class like the series-archive tests ran ten builds of the same two tutorials to check ten facts about one zip. Measured before the change: 654 unit tests in about 2 minutes 40 seconds single-threaded, of which the 446 build tests were all but six seconds. Offered three readings of "less arduous" — fewer and richer tests, the same tests made faster, or pruning — Josh chose the first.

The rule applied, file by file: tests that describe the same scenario (the same files, or filler that does not matter — placeholder prose, a slug, an asset's bytes) become one test that builds once and carries every assertion; single-rule bodies (nine maths fragments, eight lists against prose) combine into one page where every assertion still passes on it; failure-path tests stay one per `pytest.raises`, and so does anything that asserts an exact count or list of the whole output, which no richer page can satisfy. Nothing checked was dropped: the multiset of `assert` lines before and after differs only in the local renames the merges forced (663 both times), and the suite is 407 with CI's own command, in about a minute.

The "sensible things" pass, done alongside, found and fixed: a `dl-seriesnav` assertion that was true whatever the build did, since 7.165 deleted the class; a releases test named for date-versus-text ordering that could not tell them apart (the date parts are zero-padded; the release number is not, so it now compares `.9` with `.10`, and the build's own docstring, which made the same claim, says so too); a helper in the same file still reading the pre-7.173 `python-fundamentals.order.yaml`, which no build reads; a reading-order assertion that only checked three strings appeared somewhere on the page, now the actual next link; an issue-link test still passing a `course/slug` page id; class and test names, docstrings and comments that spoke of module folders, order files and the Series panel; and a class the writing guide still named. Two things noted and left: the origin-anchor assertions for "never the bibliography" and "ignores markup" pass through the emphasised-use pass before either rule is needed, so they would not catch a regression in those rules; and the asset-version cache test asserts absolute-path keys rather than building two repositories as its old name promised.

*Cost to change: low. A merged test that fails names its assertion; splitting one back out is a copy of its setup.*

---

**7.178 — Highlight-to-look-up gets the same stemming and synonyms as every search box; nine more `MODULE` fixture constants become `COURSE`.** Josh, back when #235 added prefix matching to the contents search: "the same should be true of our tooltips and other searching and helping." #239 gave every search box one shared matcher (`search-words.js`); the one search-shaped surface it missed was `initReferenceLookup()`'s `termFor()` in `tutorial-runtime.js`, which decides whether a reader's text selection names a glossary entry — a plain whole-word match either way round, so selecting "gradients" over a page whose entry is "gradient" found nothing.

`termFor()` keeps its exact and whole-word checks first — a phrase like "running estimate" still prefers the phrase over half of it — and falls back to a token-for-token comparison using `tokenize()`/`tokenHits()` from `search-words.js` when those find nothing: the selection and a candidate term each split into their normalized (stemmed, synonym-mapped) words, and it's a match when they're the same length and every pair agrees, exactly or by prefix. "gradients" now stems to "gradient" the same way typing either into a search box would; "iterating" meets an entry written as "loop" through the same synonym table that already equates them. Checked with a browser test selecting "gradients" against an entry for "gradient", and the existing lookup tests unchanged.

Doing this turned up two more files (of the five #237 missed) still calling their course-id fixture constant `MODULE`, and a search for the rest found nine — `test_reference.py` among them, since it's the file this change touches — plus one, in `test_versions.py`, that turned out to be dead: defined, never read. All renamed to `COURSE`; the dead one deleted outright.

*Cost to change: trivial. One function gained a fallback branch; the renames are mechanical.*

---

**7.179 — A `question` fence: multiple-choice and fill-in-the-blank, built the way the design note argued rather than a straight port of dewmark's own grammar.** Josh, on the design note (`planning/QUESTION_BLOCKS.md`, from a linked session): "let's implement the part that it gets right and implement the stuff that we know is better than its spec."

`assets/tutorial_tools.py` could already ask a multiple-choice question — `dropdown`, `button` and `check` have been there a while — but only as Python inside an exec cell, which meant downloading Pyodide to ask which of three words is right, a question unreadable without reading `lambda`s, and no way for an author who does not write Python to write one at all. What was missing was a form, not a capability, and the form is now a fifth fence kind beside `exec`, `hint`, `card` and `html`/`css`/`js site` in `extract_blocks()`: `parse_question()` reads `id:`/`type:`/`correct:` off the top with the same header loop `parse_cell()` uses, and everything after is ordinary markdown — the prompt and, for multiple-choice, the options list under it; for fill-in-the-blank, the sentence itself, with `{word}` a typing box and `{word|word|word}` a dropdown, the first item the expected one, both dewmark's own convention.

Where the design note gave two answers, this took the one it argued for over the one dewmark's exam file actually does: markdown after the header rather than YAML throughout, because the prompt and every option are student-facing prose the plain-language pass and `tools/measure_sentences.py` have to be able to read as prose, not as a YAML scalar; and the options are shuffled at runtime (`buildQuestions()`, `shuffle()`), where dewmark deliberately never shuffles, because a tutorial has no marker and no appeal needing "option 3" to mean the same thing twice. Correctness lives on the DOM node itself — `data-correct="true"` on an option or a select's `<option>`, `data-expected` on a typing box's own `<input>` — not in a manifest, which is what makes shuffling safe without a second, parallel record of which one moved where, and is the trade the design note named outright: right for a self-check, wrong for anything that has to keep its answer from a reader who opens the page's source.

Ids are shared with cells in one namespace, the same duplicate check `extract_blocks()` already ran for cells and site panes extended to a third kind, since a question and a cell are two keys into one saved-work record (`saveNow()`'s `questions` array, restored the same way `cells` and `siteEditors` already are — a selected option's own written position for multiple-choice, one string per gap for fill-in-the-blank, and whether Check had been pressed, redrawn on restore through a pure `evaluateQuestion()` rather than the click handler's own `checkQuestion()`, so restoring a page does not also schedule a fresh save of what it just read). Feedback reuses `check()`'s own `.dl-check`/`.dl-check-pass`/`.dl-check-fail` classes and its "That's right."/"Not quite yet." wording rather than a second voice for what is, formatively, the same kind of thing.

One real tutorial carries it: `counting-carefully.md` gets a multiple-choice recognition check right where the prose already asks the reader to notice whether order matters, the exact "checking recognition and quick judgement" case dewmark's own spec describes multiple choice for.

**What this deliberately does not do.** No LaTeX inside a prompt or an option — `to_html()` runs with no `extract_math`/`render_math` pass either side of it, so `$...$` in a question would render as literal text; every worked example so far has needed none, and wiring maths through is additive whenever one does. (Wired through in 7.182.) No per-option feedback under a wrong choice, no scoring, no attempt count. Several gaps in one fill-in-the-blank question check together, on one Check button, not one at a time — the design note's own "probably right" guess, taken as the answer rather than revisited.

*Cost to change: low. The fence sits in `extract_blocks()`'s existing table of kinds; the runtime half is one small module (`buildQuestions()` and what it calls) with no state outside the DOM it reads and the one array in the saved-work record.*

---

**7.180 — `full-stack`: a new course, and a sixth fence kind rather than a third site-pane language.** `planning/DEWSTACK_MERGE.md` §7 left one piece of dewstack's own three unscheduled — a page whose own script reads the database a `sql exec` cell built. The purpose ports; dewstack's own code does not, the standing rule for the boundary between the two repositories, and this piece needed more than a rewrite because dewlab's architecture genuinely differs on every axis that matters here: dewstack runs Pyodide on the main thread with one named `sqlite3` connection per `site=name`-style cell, while a hosted dewlab page runs it in a Worker, behind a `postMessage` boundary, against one shared `db` every `sql exec` cell already reads and writes.

**Why not a third `site` pane language.** A site editor's whole point is the opposite of what this needed: its `srcdoc`-equivalent preview is sandboxed specifically to stop a reader's script reaching anything else on the page, and there is no channel back into the page for a reason. Full stack's JavaScript needs exactly the channel the sandbox exists to block. Reusing the fence grammar (`id:`/`app:` mirrors `id:`/`site:` exactly, for the same reason a site pane has that shape — the authoring editor keeps only a fence's first word) but keeping it a separate cell kind, `AppPane`/`AppCell` beside `SitePane`/`SiteEditor` in `build.py`, means nothing about loosening a site editor's own sandbox can happen by editing the wrong branch of `extract_blocks()` by accident. `extract_blocks()` now returns a seven-tuple; every call site (`load()`, `place_blocks()`) threads the new list through the same way `questions` joined it in 7.179.

**The bridge.** `tutorial_tools._query_rows(sql, params)` runs one `SELECT` against `_page_globals["db"]` and returns a list of plain dicts, column name to value — no Pyodide proxy, no pandas, the same JSON-safe shape `describe_globals()` already crosses the Worker boundary with. `pyodide-worker.js` gets a matching `"query-rows"` dispatch branch; `tutorial-runtime.js`'s `queryRows()` awaits `ensureBooted()` and then branches on `currentManifest.standalone` the same way every other dual-path call here already does, landing on `queryRowsMT()` for a downloaded export or a `workerRequest("query-rows", …)` round trip for a hosted page. Unlike `_run_sql_cell()`, `_query_rows()` takes no `_require_cell()` — an app cell's JavaScript calls it from outside the normal cell-run lifecycle, so a bad query's own `sqlite3.Error` is left to propagate rather than rendered into a sink that does not exist here.

**Naming it `dewlabQueryRows` on `globalThis`, only when a page actually has an app cell, `dlQuery` only inside the generated wrapper.** A reader's own JavaScript pane never sees the long name — the injected script wraps their code as `(async function (root, dlQuery) { … })(document.getElementById(previewId), window.dewlabQueryRows)`, so `root` and `dlQuery` reach it as plain parameters, added to nothing global a page-wide name could collide with. The long name on `globalThis` only exists for that one wrapper to close over, and is never installed on a page with no app cell at all.

**Preview: no iframe, `@scope` instead of a sandbox boundary.** An app cell's HTML and CSS render straight into `.dl-app-preview`, and its JS pane's code runs as a real `<script>` element appended to the page — the one deliberate difference from a site editor, for the reason above. A pane's CSS is wrapped in `@scope (#dl-app-preview-N) { … }` on Run rather than left unscoped, so one app cell's stylesheet cannot reach another cell's preview, or the page around it, the way an ordinary `<style>` tag would. HTML/CSS panes are live without pressing Run, the same rule a site editor's own panes follow; only the JS pane needs it, since only running code can reach the shared database. The head-level button is Clear, not Reset, matching the confirm-guarded destructive convention a site editor's own head button already uses.

**A real, pre-existing gap found while building this, and left alone rather than fixed.** `assets/editor.js`'s `restoreExecTag()` — the function that recovers a fence's second word after a round trip through the Crepe-based authoring editor, which keeps only a fence's first word — has only ever handled `python`/`sql exec`. A site editor's `html site`/`css site`/`js site` fence has been silently demoted to inert illustrative HTML on save through that editor since the site editor shipped, with no tutorial content yet in place to surface it. This entry's own app fence has the identical shape and would inherit the identical bug, so `restoreExecTag()` now recognises both site and app fences together, reading whichever of the pair of header lines (`id:`/`site:` or `id:`/`app:`) appears in either order, since `parse_site_pane()`/`parse_app_pane()` read them as an unordered pair rather than a fixed sequence. Fixing app without also fixing the older, identical site-fence bug would have left one of the two silently broken for no reason a future reader could tell apart from "not yet needed."

**First content: "A page that reads from a database."** One tutorial, `tutorials/a-page-that-reads-from-a-database/`, adapted from `staging/dewstack-import/`'s own reference page in shape rather than copied — dewlab's single shared connection drops dewstack's `dlQuery(name, sql, params)` first argument entirely, since there is only ever one database to name. Registered the current way: `courses/full-stack.yaml`, one series, added to `courses/index.yaml`'s order — no `.order.yaml`, no `tutorials/modules.yaml`, neither of which exists any more (7.172). No `covers:` frontmatter: `full-stack` has no QQI descriptor behind it the way `database-methods`/`web-authoring` do, so none was invented. `planning/curriculum/topic-groups.yaml` still gained one group, `full-stack-basics` — reachability from the topics page is enforced separately from QQI mapping (`TestTopicGroupsMatchRealTutorials`), unrelated to whether a course carries a real accreditation code.

*Cost to change: `APP_LANGS`/`APP_HEADER_RE`/`AppPane`/`AppCell` and their `extract_blocks()`/`render_app_cell()`/manifest-serialisation branches in `build.py`; `_query_rows()` in `assets/tutorial_tools.py`; a `"query-rows"` branch in `assets/pyodide-worker.js`; `buildAppCells()`/`queryRows()`/`queryRowsMT()` and `saveNow()`/`restoreSaved()` additions in `assets/tutorial-runtime.js`; the site/app extension to `restoreExecTag()` in `assets/editor.js`; a new `.dl-app-*` CSS section; a `## Full-stack cells` section in `docs/WRITING_TUTORIALS.md`; one new tutorial folder and its glossary; `courses/full-stack.yaml` and its `courses/index.yaml` line; a new `tests/build/test_app_cells.py` and `tests/e2e/test_app_cell.py`. `planning/DEWSTACK_MERGE.md` §9's ledger row for `full-stack` now points here.*

---

**7.181 — The six known-failing browser tests, run down one by one: every root cause was in the test, not the product.** Josh: "let's continue here" — offered the browser suite's pre-existing failures as the day's first thread, and took it.

Each turned out to be its own kind of mistake, none shared with another:

- **`test_the_contents_page_never_scrolls_sideways`** opened `index.html`, "the contents page" from before 7.175 split the home page from the tutorial listing. The listing — what the codebase itself calls the contents page (`write_all_tutorials_page()`) — is `all-tutorials.html` now; the test goes there.
- **`TestLinkPicker.test_picking_a_tutorial_inserts_a_link_to_it`** clicked the editor's ProseMirror root, then pressed Control+End to reach the document's true end. When the fixture's last cell was a code fence, the click could land on Crepe's CodeMirror node view, and Control+End moved the caret to the end of *that*, inside the cell — where `insertLink()`'s mark gets silently dropped (code nodes carry none), so the link's title lands as plain text mid-fence. Clicking the trailing paragraph directly, whatever it says, sidesteps Control+End's cross-node behaviour entirely.
- **`test_both_rails_drag_wider_and_the_notebook_gives_up_the_room`** dragged dewmini's two docks wide enough that, at the suite's default 1280px viewport, under 26rem was left between them — the reading column's documented floor (7.170: "the lesser evil against text 218px wide"), which dewmini's own main column shares via `.dl-page`. Not a bug; the test's own numbers didn't leave room for the floor they were about to hit. A wider context does.
- **`TestTheSwitchInSettings.test_it_starts_on_where_i_left_off`** checked `aria-pressed`; the versions-follow control is a `role="radiogroup"` (`setSegChecked()` sets `aria-checked`, correctly) — never `aria-pressed` to begin with.
- **`test_a_stopped_cell_can_be_run_again`** clicked `.dl-btn-reset` expecting it to restore the starter code before typing something new. It doesn't — `.dl-btn-reset` clears run state and output only; `.dl-btn-clear`, behind a confirm(), is the one that resets code (`planning/CELL_IDENTITY.md`'s own "a same-shaped button did two different things" already says so — the doc had this right, only the test didn't follow it). The infinite loop just typed stayed in the cell; appending `2 + 2` after it left Python still hung on the loop before ever reaching the new line. Select-all, then replace.
- **`test_a_web_cells_chrome_is_also_quiet_until_touched`**, flagged flaky, was a real race: `head_opacity()` slept a fixed 150ms against a 0.1s CSS transition, then read the value once — comfortable margin most of the time, and reproducibly not always (caught failing at opacity `0.0165266`, `0.0165` short of settled). `expect(...).to_have_css()` polls instead, replacing the helper everywhere it was used, nine call sites across five tests, not just the one that had been seen to fail.

No product code changed; `assets/tutorial-runtime.js`, `compose/dewmini.js` and `assets/editor.js` all did what their own logic already said they should. Confirmed each fix in isolation first — a genuinely reproducible failure before the change, three-plus clean passes after, the flaky one specifically stress-tested a dozen runs — then the whole browser suite once, clean.

*Cost to change: trivial, all six. Each fix is local to the one test that had drifted from what it was actually exercising.*

---

**7.182 — Maths in every markdown surface the build has, not only the tutorial body and a staged hint.** Josh: "let's see how we can add maths to every type of cell or fence."

The main tutorial pipeline has always run `extract_math()` once in `load()` and resolved every `$...$`/`$$...$$` token in one pass at the end of `place_blocks()`, so the tutorial's own prose and a staged `hint` fence both got KaTeX. Nothing else did, because nothing else was in that pass: a `question` fence's prompt and options (7.179's own gap, above), a `card` fence's body, a hand-written page's own prose and its `<aside>`/`<div class="dl-audience">` wrappers, a hand-written fold, and a pedagogical note all called `to_html()` directly, with no `extract_math`/`render_math` either side of it. Auditing every `to_html()` call site in `build.py` found six placed this way.

**One self-contained helper, not a shared list threaded through six call sites.** The tutorial pipeline's own pattern — extract once at the top, resolve once at the bottom — depends on nothing running `to_html()` on the same text in between; `place_blocks()` owns that timing already, and adding a second, page-wide `maths` list for these six sites would mean coordinating with it from places that have no reason to know it exists. `convert_prose_with_math(text)` instead extracts, converts and resolves within one call — a card's body, a fold's body, a note's body and a page's own prose each get their own local list and lose nothing by it, since none of them share a token with the others.

**A gap's `{...}` is tokenised before maths is extracted, not after.** `render_question()` already turns `{word|word}` into a bare token so a dollar sign or a pipe inside a gap survives markdown untouched; running `extract_math()` first would have let a literal price like `{$5|$10}` in a fill-in-the-blank sentence read as an opening `$` for maths it was never meant to be. Gaps go first, so nothing inside a gap is visible to `extract_math()` at all.

**The `has_math` manifest flag was wrong before this, and would still have been wrong after fixing only the six call sites.** `tutorial-runtime.js`'s `renderMaths()` gates loading the KaTeX bundle on `manifest.math`, and `load()` computed that flag as `bool(maths)` — the count from the tutorial body's own top-level `extract_math()` call, which a fold's or a note's maths never passed through, since `convert_fold_bodies()` and `extract_notes()` run after that count is taken and produce their own HTML separately. A tutorial whose only maths sat inside a fold or a note would render `<span class="dl-math">` correctly and then never fetch the renderer that reads it. Fixed by checking `"dl-math" in body_html or any("dl-math" in note.html for note in notes)` instead of trusting the count. A hand-written page had no `math` manifest key at all; `write_page()` now sets one whenever `"dl-math"` appears in the page's rendered body.

Ten new tests cover the eight surfaces this touches — question prompt, question option, a gap alongside maths, the dollar-inside-a-gap edge case, a card body, a page's wrapped section, a page's own top-level prose (plus its manifest flag, present and absent), a hand-written fold, and a pedagogical note.

*Cost to change: low. `convert_prose_with_math()` is a pure function beside `to_html()`, called in place of it; nothing about `extract_blocks()`'s table of fence kinds or `place_blocks()`'s own pass changed.*

---

**7.183 — The five right-hand panels share one dock width, and stop repeating their own tab's label.** Josh: switching tabs shifted the reading column, and each panel's own heading just said again what its corner tab already showed.

Both bugs traced to the same cause: each panel was built as an independent thing, not a pane of one dock. `loadPanelWidth`/`savePanelWidth` keyed a resize by the panel's own DOM id, so dragging one didn't touch the other four — opening an untouched one after a resized one snapped the dock back to its CSS default, and `watchPanelOverlap()`'s reading-column margin followed it. Fixed by giving all five one shared storage key (`RIGHT_DOCK_WIDTH_KEY`) and syncing a drag's new width to the other four live, not just on the next page load. The per-panel `<h2>` is now `dl-sr-only`: the id stays, for `aria-labelledby`, but nothing shows it twice on screen.

*Cost to change: low. `makeEdgeResizable()` takes an optional shared key instead of always defaulting to `panel.id`; reverting either panel to its own key or the heading to visible is a one-line change in each spot.*

---

**7.184 — A `planning/archive/` folder for design notes about shipped, uncontested features, and `dev/check_doc_links.py` stops holding it to link currency.** Josh: the accumulating count of planning documents was making it harder, not easier, for anyone (human or agent) reading the repository to tell what still describes the current state.

Eleven documents moved there: `PRACTICE.md`, `BUILD_PLAN.md`, `REPO_AND_EDITOR.md`, `MINI_IDE_AND_DEWMINI_NEXT.md`, `MINI_IDE_REDESIGN.md`, `STUDENT_NOTES.md`, `PROGRESS_INDICATORS.md`, `CELL_CONTROLS.md`, `CELL_TOOLTIPS.md`, `DOCS_AND_COMMENTS_PASS.md`, `DOCS_AND_COMMENTS_PLAN.md` — each already describing something built, settled, and not under active reconsideration. `planning/WHERE_WE_ARE.md` and `planning/WHAT_IS_LEFT_TO_WRITE.md` were deleted outright rather than archived: both already said, in their own text or by having zero inbound references, that they had nothing left to say. `planning/DECISIONS.md` (pre-code choices) is renamed to `planning/PRE_BUILD_DECISIONS.md`, so its name stops colliding with this file's at a skim.

`ELSEWHERE` in `dev/check_doc_links.py` — previously just `planning/curriculum/` and `planning/outlines/`, generated or per-module content the checker never held to prose-currency standards — now includes `planning/archive/` too, replacing the five one-off `HISTORY` entries that used to name individual archived files by hand. A link *into* the archive from an active document is still checked; a link that goes stale *inside* an archived document is not, since nobody is expected to keep it current.

This repo's own git history is not a substitute for any of this — checked directly rather than assumed: 713 commits back to 2026-08-21, not the 4 days a shallow clone had briefly suggested, but ordinary commit and squash-merge messages here are typically just the PR title, not the reasoning; PR descriptions that touch this kind of decision usually cite `DECISIONS_LOG.md` by entry number rather than repeat it (`git log` on PR #230, checked directly). Moving a document to `planning/archive/` is therefore about relevance to a reader today, not about whether the reasoning survives somewhere else if the file were simply deleted.

*Cost to change: low. Each move is `git mv`; reversing one is the same in the other direction. Anything that turns out to still need active upkeep moves back with no scar tissue — nothing about `RIGHT_PANELS`-style code depends on where its design note lives.*

---

**7.185 — The right dock goes from five corner tabs to three: Notes, Python, and Settings, the last folding Give Feedback, Appearance and Imports & Exports behind one internal tablist; Python gains Variables, Functions and a collapsed Packages triangle.** Josh, on a screenshot of the Notes panel opening under the five-tab stack: "can you see how strange this ui choice looks?"

The five tabs shared one border and shadow as a single joined stack (7.162's `.dl-corner-dock-tr .dl-corner-tab` rules), so nothing marked where the pressed one, navy-filled, stopped being a highlighted row in that stack and started being a panel's own header — the panel opening beneath it then read as a second, unrelated box, not a continuation of the tab that opened it. Reference (the left dock's own single-toggle-plus-tablist pattern, `dl-reference-tabs`/`dl-reference-tab`) already solves exactly this for its own three sections, so the fix is that pattern reused on the right rather than a new one invented: one "Settings" toggle, `dl-settings-toggle`, opening `#dl-settings`, with a `role="tablist"` (`dl-settings-tabs`/`dl-settings-tab`) switching Appearance, Give Feedback and Imports & Exports inside it — full word labels, not icons (Josh: "I want the words there as icons aren't enough in this kind of context"; a flag glyph for Give Feedback reads as ambiguously as a report door), wrapping to a second row rather than being squeezed onto one, since two of the three labels are longer than any of Reference's own. Defaults to Appearance, the one of the three actually reached for often.

Notes and Python both stay their own external doors rather than folding in. Notes because it is about to grow (Josh: "I think we have a lot of work to do on notes anyway" — left for a separate pass); Python because a cell-heavy page opens it as often as Notes, and because it now holds something worth a door of its own: Variables and Functions, shown directly, and Packages, collapsed by default (Josh: "no one needs to look at that"). All three read straight off `describe_globals()`'s existing `kind` field (`tutorial_tools.py`) — `data` for Variables, `callable` for Functions (a reader's own functions, and classes, since Python doesn't tell the two apart by calling convention), `module` for Packages — the same bridge dewmini's own Variables panel (`compose/dewmini.js`) already used, here wired into `tutorial-runtime.js` for the first time: `describeGlobalsMT()` mirrors `pyodideMT`'s existing `pageNamesMT()`, and the worker path calls `"describe-globals"`, a message `pyodide-worker.js` already answered (dewmini's own client, `pyodide-engine.js`, just never shared its worker with a tutorial page). `refreshPythonState()` runs when the panel opens and after every `runCell()` completes; a closed panel skips the round trip entirely.

*Cost to change: low for Python's own three additions — `describeGlobalsMT()`/`describeGlobalsForPanel()` are one new call each on an already-proven bridge, easy to drop again. Medium for the Settings merge: `RIGHT_PANELS` (`tutorial-runtime.js`) shrank from five names to three, so a future fourth "occasional" panel goes back to weighing a corner tab of its own against a fourth tab inside Settings, the same choice this entry made for the three it holds now.*

---

**7.186 — Three settled planning docs deleted outright, not archived; every citation to them stripped from the code, not repointed.** Josh: past planning that no longer describes an open question is not worth the read, git already keeps it, and a citation to a closed document is dead weight in the same way the document itself was.

`planning/CELL_HINTS.md` and `planning/curriculum/DECISIONS_NEEDED.md` — light citation counts, deleted along with their few pointers. `planning/DEWSTACK_MERGE.md` was heavier: cited by section number from about a dozen places, mostly `build.py` and `tutorial-runtime.js` comments explaining the full-stack app-cell feature. First instinct was to archive it so those citations stayed resolvable — overruled: a citation to a merge that already happened is exactly the kind of thing a future maintainer should never have to chase down. Every one of those comments now stands on its own, describing what the code does without pointing at why a now-closed migration made it that way. The one fact still true today — `web-authoring` and `full-stack` are built and ported but held off the homepage pending a real classroom run — moved to `planning/STATUS.md`, the live doc that already owns "what is actually true right now".

`planning/CELL_IDENTITY.md`, `planning/HIGHLIGHTS_AND_NOTES.md` and `planning/DEWMINI_WORKBENCH.md` show the same section-cited-from-code pattern, at higher density (dozens of sites each, some inside `compose/dewmini.js` itself) — flagged, not yet acted on, pending confirmation given the size of the cleanup.

*Cost to change: low for the two light deletions. Low-ish for DEWSTACK_MERGE.md — every stripped comment still describes real, current behaviour correctly; only the "why this shape" pointer is gone, recoverable from git history if it is ever genuinely needed again.*

---

**7.187 — `planning/archive/` deleted wholesale — all sixteen files, no replacements.** Josh: no text here is holy; git history is the real archive, so a folder that exists only to hold closed design notes for their reasoning is not worth the read either, and every citation into it is one more thing a future maintainer has to chase down instead of trusting the code in front of them.

Four of the sixteen (`CONTENT_AND_FILE_ARCHITECTURE.md`, `EDITOR.md`, `PRE_BUILD_DECISIONS.md`, `WINDOW_AUDIT.md`) already had a fresh, tightened rewrite living at their original path from 7.186's companion PR, so only the `planning/archive/`-prefixed citations to those four needed stripping; bare-name mentions still point at something real. The other twelve had no active counterpart, so every citation — bare or prefixed — was stripped or reworded to describe current behaviour on its own terms, in `build.py`, `dev/check_doc_links.py` (the folder's own link-currency exemption, now gone with it), and a dozen test and doc files. `planning/README.md`'s "Archived" section is gone too, not repointed.

*Cost to change: low. Every stripped comment still describes real, current behaviour correctly; only the "why this shape, historically" pointer is gone, recoverable from git history if it is ever genuinely needed again.*

---

**7.188 — `planning/QUESTION_BLOCKS.md` deleted; its section citations across `build.py`, `tutorial-runtime.js` and a test stripped rather than repointed.** Josh: the same standard as 7.186/7.187 applies to any pre-build design note for a feature that has since shipped (here, the `question` fence, 7.179) — a citation to a closed design argument is dead weight a future maintainer has to chase down for no benefit, once the code already says what it does.

Seven sites in `build.py` alone cited it by section number for parsing and rendering detail that is now just described in place. The note itself was already an outlier in `planning/README.md`'s own index — it was never listed there, despite being the densest citation source in this batch.

*Cost to change: low. Every stripped comment still describes real, current behaviour correctly.*

---

**7.189 — `planning/PEDAGOGICAL_STYLE_GUIDE.md` rewritten from scratch, 579 lines to under 390, against five of Josh's own teaching handouts rather than a trim of the old text.** Josh: the old guide, however accurate its content, was not effective, and documentation should describe the current state in the plain, invitational register the tutorials themselves are supposed to use — not carry the history of how it got that way.

Read directly rather than through memory: a "Dear Student" course letter, and handouts on figurate numbers, ciphers as functions, sequences, and derivatives. The shared voice across all five — invitational "we"/"let's", questions doing the actual teaching rather than introducing it, warmth that admits a topic is hard, concrete before formal, naming a concept only after using it informally — mostly confirmed rather than overturned what the old guide already argued for; what it did not survive was the guide's own bloat: a "these two documents were merged, and here is where they disagreed" section, a formal academic bibliography with press and year, an in-progress bibliography-coverage audit ("49 of 60 tutorials"). All of that is cut. Section numbers 1, 3, 4 (with its "Plain language" subsection), 5 and 6 are kept in place on purpose — `CLAUDE.md`, two skills, `build.py`, `dev/check_doc_links.py`'s citers, and several tests all cite this guide by section number, and renumbering them for a document that is not actually reordering its load-bearing content would have been change for its own sake.

*Cost to change: low. Nothing that cites this guide by section number needed to change; the content each citation depends on (the emphasis-on-first-use rule, the cell-id-as-contract line, the hint-fold rationing, the "Plain language" checks) is still at the section number it was.*

---

**7.190 — Notes, Python and Settings drop their own header row — no repeated title, no close button — and the Python panel's Variables/Functions/Packages stop showing the toolbox every page starts with.** Josh, on a screenshot of the merged Settings panel: "I dont think we need the second settings header and I think since we have the click to open and click to close behavior we dont need the X to close on each of them, this saves us some nice vertical real estate" — then, on the panels once open, noticing the Functions list: "I dont think those functions were the ones defined by the user?"

The close button was never the only way to close a panel — Escape and a click outside both already worked — so it was purely redundant with the corner tab's own toggle behaviour (`p.toggle.addEventListener("click", () => setOpen(...))`, already there since 7.162). Settings kept a visible `<h2>Settings</h2>` because it names three different things folded behind one door; dropping the row it sat in means dropping the visible title too, so it goes back to `dl-sr-only` like its two siblings always were — the corner tab already shows the name, same reasoning 7.183 gave for not repeating a tab's own label inside its panel. `.dl-panel-sticky-head` stays only where something still needs pinning while its panel scrolls: Reference and Where You Are keep their head (title, close button); Settings keeps its tablist and Appearance's search; Notes and Python drop the wrapper entirely, since nothing in either needs to stay reachable mid-scroll once the close button is gone.

The Functions leak was `describe_globals()` (`tutorial_tools.py`) doing exactly what its own docstring already promised — "callable — functions and classes, theirs or ours" — which is right for dewmini's Variables panel (compose has no pre-seeded toolbox to distinguish from) and wrong for a tutorial page, where `RESEED_GLOBALS_SOURCE` binds all ten `__all__` names into the shared namespace before a reader's first keystroke. Every entry now carries `builtin`: true for a name still bound to whatever `tutorial_tools` itself put there (checked by identity against the module's own globals, so a reader who shadows `show` with their own function still shows up as theirs), and true by name alone for `db` — a fresh `sqlite3.Connection` every boot, with no fixed object an identity check could catch. `refreshPythonState()` (`tutorial-runtime.js`) filters `!entry.builtin` across all three of Variables, Functions and Packages, so "what's defined right now" means what a reader's own code made.

Verified against a real, self-hosted Pyodide (`dev/fetch_pyodide.py`) rather than the CDN this sandbox can't reach: running a plain cell (`readings = np.array(...)`) showed `readings` under Variables and `np` under Packages, with all ten toolbox names and `db` correctly absent from every list.

*Cost to change: low throughout. A close button is one `<button>` and one `if (p.close)` branch (already null-safe) to restore in any of the three; `builtin` is an additive field on `describe_globals()`'s existing return shape, so dewmini's own Variables panel (which ignores it) is untouched.*

---

**7.191 — Both corner-dock stacks shrink to their own tab's label at rest, on both sides, instead of a fixed width guessed for whatever panel might open beneath them.** Josh: "should these be horizontal bars if they start out smaller? maybe these are as small as the text allows (note they should grow when the text grows from the appearences panel) for both the right and the left side."

A bordered button wider than its own label is the same defect 7.190 had just fixed one level up — empty space inside a box that had no content-driven reason to be that wide. `.dl-corner-dock-tr .dl-corner-stack`'s `12.5rem` and `.dl-corner-dock-tl .dl-corner-stack`'s `var(--dl-side)` were both exactly that: a resting width sized for the panel that might open beneath the stack, not for the stack's own label. Both go to `width: max-content` instead — measured directly: "Notes"/"Python"/"Settings" now hug their widest label at 225px→(intrinsic), "Reference" at 396px→(intrinsic), instead of the panel-sized 12.5rem/22rem guesses. Growing with the reader's own text-size choice needed nothing new: `html { font-size: var(--dl-font-size) }` already makes every `rem` on the page, this stack's own padding included, scale with it — confirmed directly at a 24px base.

Widening to match the panel once it opens already existed on the right (`initRightPanels()`'s `setOpen()`, RIGHT_DOCK_WIDTH_KEY-driven); the left dock's Reference tab gets the identical treatment for the first time — `initReference()`'s own `setOpen()` now sets the left stack's width inline to Reference's rendered width, `closeReference()` (the mobile-sheet-takeover path `closeRightPanels()` already had a counterpart for) clears it back to `max-content`, and `watchPanelOverlap()`'s `makeEdgeResizable()` call for the left panel gained the same live-drag sync the right side's already had. `.dl-corner-identity` (wordmark, search, breadcrumb tree) keeps its fixed `--dl-side` width throughout — that block needs real room to wrap its own text whether or not Reference is open, unlike the tab sitting under it, so it was never part of this problem.

Left unaddressed this round: reordering controls within a panel, and whether Give Feedback still belongs as a peer tab next to Appearance and Imports & Exports inside Settings (7.185 flagged the second one as Josh's call, not decided here either) — both need a panel-by-panel pass rather than one mechanical fix.

*Cost to change: low. One CSS value per side and the matching JS block, mirroring a pattern already proven on the right; reverting either side to a fixed rest width is a one-line change.*

---

**7.192 — Eleven more planning docs deleted: the app-architecture notes nobody writing a tutorial ever opens.** Josh: no plans for new dewlab features are being discussed, new tutorials will be written by teachers and collaborators rather than planned as engineering work, and most of `planning/` was written for a phase of active feature design that has ended.

`STATUS.md`, `ROADMAP.md`, `PRE_BUILD_DECISIONS.md`, `WINDOW_AUDIT.md`, `EDITOR.md`, `OPEN_QUESTIONS.md`, `SIDEBAR_CONTENT.md`, `EDGES_AUDIT.md`, `CURRICULUM_NOTES.md` go with no replacement — closed design and status notes for a build phase that finished. `CONTENT_AND_FILE_ARCHITECTURE.md` was worse than redundant with `docs/WRITING_TUTORIALS.md`: its frontmatter example still showed `module`/`order`/`series` fields and `version: 1` as a plain integer, none of which match the real format — an actively wrong document, not just an overlapping one. `VERSIONS.md` had two facts nowhere else: the draft/beta/live/archived status table and `topic:MIT-X.Y` linking, both moved into `docs/WRITING_TUTORIALS.md` before the file went, including fixing that same doc's own frontmatter table, which had never mentioned `draft`/`beta` despite `build.py` implementing both.

Kept: anything a person writing, reviewing, or troubleshooting a tutorial actually opens — the style guide, `EXERCISES.md`, `REFERENCE_PANEL.md` (leaned on directly by the `tutorial-glossary` skill), `DOT_DOCK.md` (kept on Josh's standing instruction regardless of this pass), the curriculum data and the three `.claude/skills/`. Citations into the eleven deleted files were stripped and reworded across `build.py`, several tests, nine `data/*.yaml` attribution files, and `planning/README.md`'s index, the same way the archive batch was handled — not repointed, since a citation to a closed design phase is exactly the thing this pass exists to remove.

*Cost to change: low for the nine straightforward deletions. Low-ish for `CONTENT_AND_FILE_ARCHITECTURE.md` and `VERSIONS.md` — their still-true facts now live in `docs/WRITING_TUTORIALS.md`, so nothing described there was actually lost, only moved to the one file a tutorial writer already has open.*

---

**7.193 — `planning/README.md` and `PLAIN_LANGUAGE_PASS.md` deleted; `REFERENCE_PANEL.md` §6 rewritten to describe the panel's current shape instead of its shipped-then-superseded one.** Josh, continuing 7.192's pass: `planning/README.md` was an index for a folder now down to five files, whose names already say what they are; `PLAIN_LANGUAGE_PASS.md` was 355 lines, of which perhaps twenty were not a dated log of already-shipped editorial passes — the nine checks it explained are already in the style guide's voice section (then §4) verbatim, so the log was the only thing left, and it is exactly the kind of history git already keeps.

`REFERENCE_PANEL.md` stayed, since `docs/WRITING_TUTORIALS.md` and the `tutorial-glossary` skill both lean on its accumulation logic (§1-5), but its §6 had drifted into the same problem in miniature: it described the panel "as it originally shipped," then a paragraph underneath correcting that to the real, current shape. Rewritten to state the current shape once — a tab in the left corner dock, a docked sidebar with three internal tabs (Reference/Math Basics/Python Basics), not a floating card — with no "here's what changed" framing needed once there is only one shape being described.

Citations into the two deleted files were stripped from `CLAUDE.md`, `build.py`, `docs/WRITING_TUTORIALS.md`, and `planning/curriculum/review/split-plan.md`.

*Cost to change: low. `PLAIN_LANGUAGE_PASS.md`'s small open backlog (a vocabulary sweep, some verbless fragments, thin bibliographies) is gone with the file rather than moved somewhere else — recoverable from git history if anyone picks that work back up.*

---

**7.194 — Give Feedback drops out of Settings into its own circle at the bottom-right; the tab it leaves behind becomes Behavior, holding what 7.190/7.191 left flagged as undecided; Appearance's flat eleven-row list splits into three named groups; two lingering pieces of duplicate text are gone.** Josh, asked what he'd change about the panels' own contents: "I wonder if you could look at the contents of the panels and make things more efficient and clean and easy to understand by changing how ui elements are grouped or which ones are used etc." Then, on the two open questions this round raised: "lets move ambiguous stuff and general stuff to something like 'behavior' maybe? I think we could have report as a little circle at the bottom right of the screen? What do you think?" — and, on the rest: "I think the rest of your suggestions are solid and you should move them as you see fit."

Give Feedback was never a preference the way Appearance's rows are, or a page it opens and closes with — it's something a reader reaches for once, at whatever moment something is wrong, so competing for a tab slot next to two settings panes never fit it well. It is now `.dl-report-fab`, a fixed circle (`#dl-report-toggle`) at the bottom-right of every wide-enough screen, sharing `RIGHT_PANELS`' open/close/Escape/outside-click machinery so it still closes Notes/Python/Settings the way a fourth corner tab would have — but excluded from `dockLinked`, the subset `initRightPanels()` now uses for the width-sync and edge-resize that Notes/Python/Settings still share, since a circle has no width to sync. Folds into the mobile launcher's menu below 34rem, same as the three corner tabs. The footer's own no-JS "Something wrong on this page?" disclosure (`report_doors_html()`) is untouched — this is a second, always-reachable door to the same three doors, not a replacement.

The tab Give Feedback left behind is now Behavior: `dl-settings-tab-feedback`/`dl-settings-pane-feedback` renamed to `-behavior`, and it picks up the controls 7.190's Functions fix and 7.191's dock-shrink left with nowhere obviously right to live — Run time, Hints as you work, After a restart (moved out of the Python panel, where they read as page behaviour rather than "what Python is doing right now") and the progress-badges toggle (moved out of Notes, where it controlled the tutorials list rather than this page's own notes). Both moves are markup-only: `refreshPythonState()`'s DOM ids, and the `[data-progress-badges]`/`[data-run-stats]`/`[data-staged-hints]` selectors both `applyTexture()`-style wiring and several e2e tests use, are unqualified by container, so nothing but the id list a handful of tests open first needed to change.

Appearance's own eleven rows were one flat list with no structure beyond top-to-bottom order, asking a reader to scan past Code and Accessibility toggles to find the next Reading one. Three `<h3>`-headed sections now group them by what they're actually about: Reading (Theme, Font, its Lexend/OpenDyslexic row, Size, Width, Links), Code (Cell buttons, Code line height, Code indent, Line numbers), Accessibility (High contrast, Reduce motion, the reset-to-defaults button, moved here from its old spot mid-list since it acts on the whole pane, not just Reading). `initTexture()`'s root query — `document.getElementById("dl-settings-texture")`, one panel wrapping every row — had to move to `"dl-settings-pane-appearance"`, the tab pane that still wraps all three new sections; missing this on the first pass would have silently broken every Appearance control on the page, since the function returns early when its root query finds nothing.

Two duplicate-text fixes: Notes' two adjacent paragraphs both explaining that notes are saved in this browser only merged into one. Imports & Exports' Export section dropped a sentence ("Two more ways to take this page with you") that said nothing the Download and Export section headings weren't already saying on their own — Download and Export stay two separate `<section>`s rather than merging into one, since `tests/build/test_site.py` matches `<section class="dl-settings-section" id="dl-settings-download">` as an exact, sometimes-empty string.

Versions was flagged mid-round as misplaced inside Imports & Exports and slated to move to Behavior — reversed after reading `initVersionsSection()`: it already relocates itself into the where-you-are tree at runtime on every page, so the earlier read was static-markup-only and wrong. Left in place.

*Cost to change: low throughout — a tab rename, a handful of moved `<div>`s whose ids and `data-*` selectors didn't change, and one root-query fix. The one thing worth remembering if Behavior grows a fourth section: 7.191's dock-width-sync split (`dockLinked`) means a fifth corner-dock panel, unlike Report, would need adding to that filter's exclusion list explicitly, not just to `RIGHT_PANELS`.*

---

**7.195 — A highlight can take one of four colours now; the Notes panel gets a live "Your highlights" list; and My Notes (`all-notes.html`) gathers every highlight and note across every tutorial this browser holds, into one page with a search box and a plain-text download.** Josh, told the base highlight-and-note feature (7.155–7.160) already existed and asked what would make it more useful: "lets make those happen in the notes panel, but feel free to go wild and make a really dynamic highlight feature here! What else would highlighters want? What other things do note takers want? Different colors? Ways of carrying between pages? A central place for notes?" — naming, unprompted, the three things this entry builds.

**Colour rides in the same schema slot `note` already uses.** `HIGHLIGHT_COLORS` names four — amber (the default, matching the existing `--dl-highlight-bg`, so an un-migrated highlight saved before this round needs no data migration at all), green, blue, pink — each contrast-checked per theme the same way 7.158 checked amber (11.8–14.3:1 light, 8.6–10.5:1 dark, comfortably past the 4.5:1 AA minimum `test_highlight_colors_and_list.py` measures directly, parametrized across all three new colours and both themes). The popover gains a swatch row that recolours a highlight immediately on click, independent of the Save button below it — a colour is a single click, not something a reader is still composing the way a note's text might be. `recolorHighlight()` sets or clears `[data-highlight-color]` on every `<mark>` sharing one highlight id, since a highlight crossing an inline element is more than one `<mark>` (`wrapRange()`'s own comment). A fresh highlight starts in whichever colour a reader used last, read from its own `localStorage` key across every tutorial rather than per page — a reader who has settled on "amber means important" wants that meaning to hold everywhere, not reset itself on the next tutorial. Deliberately not given fixed meanings ("important", "confusing") — a plain colour name leaves what each one means up to whoever is highlighting, the same way a paper highlighter set does, and guessing wrong about a first-time student's own categories seemed worse than leaving the choice open.

**"Carrying between pages" turned out to be the cheap one, once colour and the list existed — a highlight already anchors to a passage, not a build-time id, so nothing about the schema needed to change for it to travel.** `jumpToHighlight()` scrolls a highlight into view and pulses it (`.dl-highlight-flash`, a CSS `@keyframes` that needs nothing extra to respect Reduce Motion, since the existing global `[data-motion="reduced"]` rule already zeroes every animation's duration); called from a row in the Notes panel's own list it also opens the popover, since a reader clicking their own highlight from a list of them is visiting to manage it. Called from a URL's own hash (`#dl-highlight-<id>`, checked once at boot, after `renderMaths()` settles the page's layout so a KaTeX block below the passage can't still shift it out from under the jump) it leaves the popover shut — arriving from a link is visiting a passage to re-read it, not asking to edit it. The one real trap building this: Playwright's `page.goto()` to a URL differing only by hash, from a page already on that path, is a same-document fragment navigation the same way clicking a same-page `<a href="#x">` link is — it does not reload the document or re-run its boot script, so `test_highlight_colors_and_list.py`'s own hash tests open the hash URL as a fresh tab rather than reusing the page already loaded, the same way a reader arriving from another page genuinely would.

**"A central place for notes" is `all-notes.html`, a plain fourth site-wide page (`write_all_notes_page()`, alongside `write_all_tutorials_page()`/`write_tree_page()`) built the same way `tree.html` is — the same shell, its own client-side script (`assets/my-notes.js`, not bundled into `tutorial-runtime.js`, so this needed no vendor-bundle rebuild for its own sake).** `localStorage` is shared per browser origin, not per page, so a page that never ran any tutorial's own boot code can still read every `dewlab:progress:*` record this browser holds and build a card per tutorial with something saved — its own free-text notes, then every highlight, each linking back to `tutorials/<slug>.html#dl-highlight-<id>`. The one thing storage can't supply is a human title for a bare slug (a saved record only carries `tutorial-slug`), so the build bakes in a `{slug: title}` map as a JSON data island the same way `tree.js` already reads its own topic-graph data — the only piece of this page that isn't pure client-side reconstruction. A search box reuses `search-words.js`'s `textMatches()`, the same stemming-and-synonyms matcher every other search box on the site already shares (7.178's own reasoning — "the same should be true of our tooltips and other searching and helping" — extended once more here). "Download as text" turns the same data into a plain-text study sheet, grouped and ordered exactly the way the on-page cards are, so the two never say different things about what "your notes" means; it is not the raw-JSON backup each tutorial's own "Export a copy" already offers, and does not replace it — one is a machine-readable restore point, the other something meant to be read.

A quiet fifth link, `{{ROOT_BASE}}all-notes.html`, sits under the wordmark on every page (`.dl-corner-identity`, `assets/shell.html`) — reusing the `{{ROOT_BASE}}` token every page type already substitutes correctly, rather than threading a new root-relative-path parameter through `site_footer()`'s seven call sites for a link `site_footer()` was never built to carry.

*Cost to change: low. Colour is one more field on an already-additive schema (an un-migrated highlight simply has none, and reads as amber); the Notes panel list and `jumpToHighlight()` are pure UI reading the same `highlights` array every other highlight function already shares; `all-notes.html` is a fully separate file and page, deletable on its own without touching anything a tutorial page depends on. The one thing genuinely out of reach without a real architecture change: none of this crosses devices or browsers — dewlab has no accounts and no backend, so "my notes, from my phone and my laptop both" stays a non-goal, the same one the Notes panel's own "saved in this browser, on this device" line (`assets/shell.html`) already sets for every other piece of saved work.*

---

**7.196 — Reference drops the same redundant header row and close button 7.190 already dropped from Notes, Python and Settings.** Josh, on a screenshot of the panel open: pointed out "Reference" reading twice — once on the pressed corner tab, once again on a visible label directly under it — "also, reference appears twice here and has the x instead of the 'click the header again' behavior."

7.190 explicitly chose to leave Reference (and Where You Are) with their own title-plus-close row, reasoning that "something still needs pinning while its panel scrolls" — true, but the part that needed pinning was always the search bar and the internal tablist beneath it, not the title or the close button sitting above them; those two just rode along in the same `.dl-panel-sticky-head` wrapper without anyone asking whether they still earned their place once Notes/Python/Settings had already dropped theirs. They didn't: `initReference()`'s own toggle listener already does `setOpen(panel.hasAttribute("hidden"))` on every click — re-clicking the pressed corner tab already closes the panel, the same as the other three, and Escape and an outside click both already worked too. Where You Are is the one real exception, left alone: it is a phone-only full-screen sheet with no persistent tab to re-tap, opened from the mobile launcher's own menu rather than a corner dock, so its close button is the only way back and stays.

`<h2 id="dl-reference-title">Reference</h2>` plus `#dl-reference-close` inside a `.dl-reference-head` wrapper becomes a single `<h2 id="dl-reference-title" class="dl-sr-only">Reference</h2>`, matching Settings' own sr-only title exactly (7.190's own reasoning: the corner tab already shows the name, so a second visible copy at the panel's own top is the same word twice — 7.183). The search input and the Reference/Math Basics/Python Basics tablist stay exactly where they were, still the two things this sticky head actually needs to keep visible while a long glossary scrolls underneath them. `.dl-reference-close` (the CSS class) and `.dl-reference-head` (the wrapper) both stay in the stylesheet, still used by Where You Are's own head.

*Cost to change: trivial — one `<div>` unwrapped into its own `<h2>`, one now-orphaned `if (close)` listener removed, and one test (`test_the_close_button_closes_it`) renamed to assert the toggle-re-click behaviour it should have been testing already.*

---

**7.197 — A dragged panel's edge-resize handle now widens its corner-dock tab stack live, not only on release; a new CI-run test file catches the class of bug that let this one ship unnoticed.** Josh: "I think there is some odd drag behavior on the right panel where only the bottom part moves and not the tabs themselves? does that make sense?"

It made sense the moment `makeEdgeResizable()` (`tutorial-runtime.js`) was read straight through. `onMove` already set the dragged panel's own width on every pointer move, and a separate `ResizeObserver` (`watchPanelOverlap()`) already reflowed the reading column live from that — but the callback that widens the corner-dock's tab stack to match, and syncs the other two panels sharing that width (`RIGHT_DOCK_WIDTH_KEY`), only ever ran once, from `onUp`. So a drag looked half-finished the whole time it was happening: the panel body and the page around it tracked the mouse smoothly, and the row of tabs sitting above the panel sat frozen at its old width until release, then jumped to catch up in one visible snap. Left (Reference) and right (Notes/Python/Settings) both call `makeEdgeResizable()` the same way and had the same bug. The fix is one line moved: the sync callback now runs from `onMove` too, reading the same `panel.style.width` `onMove` just set, so the tabs move with the same motion as the panel beneath them; `onUp` keeps only the save-to-`localStorage` step, which only ever needed the final value.

**Caught with the drag held open, not released** — `page.mouse.down()`, several `page.mouse.move()` steps, an assertion, then `page.mouse.up()` — since a test that only checked the state after release would have passed against the bug exactly as it passed against the fix; the corner-dock stack was always correct by the time the mouse came up, which is exactly why nobody had noticed. Verified against the bug directly: reverting the fix and re-running `tests/e2e/test_panel_resize_drag.py` fails all three tests with the stack's width still equal to its pre-drag value, confirming the test measures the thing that was actually broken rather than something adjacent to it.

**Added to the `browser` CI job, not left local-only.** Asked to check the test architecture before pushing a new file, rather than assuming: `tests/e2e/` is deliberately *not* covered by the blanket `pytest tests --ignore=tests/e2e` the `unit` job runs — the whole directory needs Pyodide fetched and a browser per cell, which the top-of-file comment says stays a local, manual step on purpose. CI instead names four specific files in the `browser` job, chosen because they prove chrome and layout without ever running a cell; 7.173's own account of why is a real regression (#230, a phone identity-row bug) that reached `main` with CI green because nothing there covered it. `test_panel_resize_drag.py` is prose-only, the same shape as those four, and this bug is the same class of regression 7.173 already names — so it joins the named list rather than sitting as coverage nothing ever runs, which is worse than no test at all: it looks like protection and isn't.

*Cost to change: low. The moved callback call is a two-line diff with no new state; the test file is one more entry in one list, deletable on its own if the resize handle itself is ever redesigned away.*

---

**7.198 — A panel's resize handle is a sibling of `<body>` now, not a child of the panel it resizes, so it can finally reach up past the corner-dock tabs sitting above it; the same fix ported into `compose/dewmini.js`'s own duplicated copy.** Josh, before merging 7.197's fix: "is there an equivalent bug on the left panel? (I think there is, also in the sense that the 'drag highlight' doesn't go all the way up." There was — on both sides, and it was never the tab-sync bug 7.197 had just fixed. `.dl-right-panel`/`.dl-left-panel` both set `overflow-y: auto` for their own scrolling content, and a `position: absolute` child can never visually extend past the top edge of the container clipping it — so the handle, prepended into the panel itself, was clipped at exactly the panel's own top, well below where the corner-dock's tab stack sits. The highlighted strip, and the actually-grabbable hit area, both stopped short of the tabs a reader would reasonably expect to be able to grab past.

Detached to `document.body`, `position: fixed` instead of `absolute`, spanning the full viewport height. Nothing about a fixed sibling keeps its `left` glued to the panel's own edge for free the way a child's `left: 0`/`right: 0` did, so `positionHandle()` now sets it explicitly from `panel.getBoundingClientRect()` — called once on creation, from a `ResizeObserver` on the panel (any width change, whatever the cause: this drag, a sibling sharing the same width, a font-size change, the window itself), from a `MutationObserver` on the panel's `hidden` attribute (so the handle still hides and shows in lockstep with its panel, which came for free before), and directly inside `onMove()` for this drag specifically — the one path that needed to feel perfectly synchronous with the panel's own width change, not merely eventually consistent with it. `handle.dataset.for = panel.id` replaces `panel.querySelector(".dl-panel-resize-handle")` as how a handle is found or told apart from any other panel's own, now that several can be siblings under `<body>` at once; `panel.dataset.resizable` (already there, previously redundant with the `querySelector` check) is now the only re-entry guard. `.dl-panel-resize-handle-right`, the CSS class that used to flip the handle to the panel's right edge for left-docked panels, is gone — `positionHandle()` always sets `left` directly now, so a side-specific rule had nothing left to do.

**Checked for the same bug elsewhere, on Josh's standing instruction** ("in general when there is an issue one place we want to see if there are other places where this exists") **and found it in `compose/dewmini.js`'s own copy of `makeEdgeResizable()`** — duplicated by hand rather than shared, per `docs/dewmini-js-explained.md` and 7.159, but `compose/dewmini.html` links `../assets/tutorial-style.css` directly (before its own `dewmini-style.css`), so `.dl-panel-resize-handle` is CSS the two products already share even though the function that positions it is not. `.dm-panel`'s own `position: fixed; overflow-y: auto` is the identical clipping shape, so the identical fix applies: ported the detached-handle version into dewmini's copy, with `onResize` left firing only from `onUp` as before — dewmini's `.dm-toolbar` is a fixed top bar, not a per-panel width-matched dock the way the tutorial page's corner stack is, so there was no analogous "needs to move on every pointer move" concern to bring across with it.

**A near-miss, caught before it shipped:** the first pass at the CSS fix dropped `left: 0` from `.dl-panel-resize-handle` entirely, reasoning that `positionHandle()` always sets it inline now. True in `tutorial-runtime.js` — but at that point dewmini's own `makeEdgeResizable()` still had its *old* JS, which never set `left` at all and relied on the CSS rule doing it. Removing the fallback would have left every dewmini resize handle with an undefined position the moment this shipped, discovered only by the same "look for it elsewhere" check that caught the missing port in the first place. `left: 0` went back in as a safe default for any handle whose JS hasn't (yet) taken over positioning it.

Existing coverage needed updating rather than extending: `tests/e2e/test_dewmini_workbench.py`'s `test_both_rails_drag_wider_and_the_notebook_gives_up_the_room` and `test_a_rails_width_survives_a_reload` both located a handle as `"#dm-library .dl-panel-resize-handle"` — a selector that stopped matching anything the moment the handle stopped being a descendant of the panel. Rewritten against a `_handle(panel_id)` helper matching `.dl-panel-resize-handle[data-for="..."]`, the same pattern `test_panel_resize_drag.py` already used for the tutorial-page side of this fix. `test_panel_resize_drag.py` itself gained two new assertions (`test_the_handle_reaches_all_the_way_up_past_the_tab_stack`, one per dock) checking the handle's own `getBoundingClientRect().top` sits at or above the corner dock's, plus a horizontal-tracking test for the left dock verifying the detached handle's `left` still follows the panel's edge mid-drag, not just at rest.

*Cost to change: low-ish. The detach-and-reposition pattern is now duplicated across two files by the same hand-porting convention 7.159 already accepted for this codebase; a future shared-UI-mechanics module (raised as an open question this round, not acted on) would remove that duplication but is a larger, deliberately deferred change, not a cost of this fix itself.*

---

**7.199 — Reference and the right-hand dock (Notes/Python/Settings/Report) stop closing on a click outside them; only their own header (a re-click of the pressed corner tab) or Escape closes them now.** Josh, after opening Reference on the left and Settings on the right and watching a click in the reading column take both away at once: "we want the panels to be able to both be left open? the idea is that the header itself is the close button, not that whenever we lose the focus or click in the document the panels go away."

This was never a new decision to make — 7.99 had already made it, for dewmini's own docked rails, in one sentence: "a docked rail must not close on an outside click, unlike a popover" (`test_a_rail_survives_clicking_your_own_notebook`'s own docstring on the dewmini side says the same thing: "A docked rail is a pane, not a popover"). The tutorial pages' four panels were simply never brought into line with that ruling — they trace back further, to 5.1's original one-Settings-panel design ("The panel closes on Escape and on a click outside"), from before dewmini's rails existed to set the newer precedent. Once dewmini had ruled the other way for what is structurally the same kind of element, carrying two contradictory answers to the same UI question forward was the actual defect, not merely an inconvenience Josh happened to hit first on the tutorial side.

**The removal exposed a second, real bug along the way, not just the design question.** `makeEdgeResizable()`'s resize handle (7.198, this same session) is now a sibling of `<body>` rather than a child of the panel it resizes — so `p.panel.contains(ev.target)` no longer recognized a click landing on the handle as "inside," and neither `LEFT_DOCK_IDS` nor `RIGHT_DOCK_IDS` (built before the handle existed as a detached element) covered it either. A stray click on either dock's own resize handle was silently closing both panels at once, which is almost certainly the shape of what Josh actually saw. Deleting the two outside-click listeners removes this failure mode along with the deliberate design it was riding on top of — there was no narrower fix that kept outside-click-close and also patched the handle gap, since the handle's exact position changes on every drag and every font-size change.

**`LEFT_DOCK_IDS`, `RIGHT_DOCK_IDS`, and `clickIsInsidePanels()` go with the listeners that were their only callers** — the "which ids count as inside this dock" bookkeeping they existed for is now nothing to reconcile, since there is no more "outside" to check against. `initRightPanels()`'s own toggle-forwarding comment (used by the mobile launcher's menu items) needed the same correction: its `stopPropagation()` had explained itself as guarding *every* panel's outside-click listener, but only the Where You Are sheet's own listener (a different, phone-only full-screen takeover, deliberately kept on 7.196's own reasoning — it has no persistent tab to re-tap) still has anything to guard against; the toggle-forwarding path no longer needs it at all, but one unconditional `stopPropagation()` still covers both shapes that handler can take.

Escape and the close button (where one exists) are untouched — dewmini's own rails keep Escape too, and Josh's own framing ("we lose the focus or click in the document") named outside-click specifically, not every dismiss path.

*Cost to change: low. Two `document.addEventListener("click", …)` blocks and their now-unused supporting code, removed outright rather than disabled; reverting to close-on-outside-click is the same two blocks pasted back, unchanged in shape from before this entry.*

---

**7.200 — The site editor's preview-width control steps by 1 and reads out pixels beside the percentage, and the two CSS layout diagrams built last round become things a reader changes rather than pictures of things changing.** Josh, on the four markup-built diagrams: "couldn't we build live examples there like the ones in WADB_tutorials? Especially where we can resize a little window with various numbers to see how that works instead of having an image? ... I just think if we can create really nice small examples of draggable or clickable or resizable things like grid and flexbox, thats better than us trying to draw pictures."

He is right, and the apparatus was nearly all there already: every site editor has had a preview-width slider since the `media-queries` port, and a layout tutorial's question is nearly always *at what width*. What the slider could not do was answer it. It stepped by 5%, so a reader could not land near a threshold, and it reported a percentage of a column whose own width depends on their font, their window and whether a panel is open — a number that means nothing outside the moment it was read. It steps by 1 now, and its `<output>` carries the frame's own rendered width in pixels: `65% · 369px`. Measured from the frame with a `ResizeObserver` rather than computed from the percentage, so it stays true when the column changes underneath it.

**The frame's width is not the width inside it**, and on a page that names a threshold the difference is the whole story. The preview iframe is `sandbox="allow-scripts"` without `allow-same-origin`, deliberately (a reader's script must not reach the page), so the runtime can only measure the frame. A previewed page's default `body` margin puts 16px between the two. `flexbox-first-steps`, which now tells the reader to watch the pixel figure and find where the row wraps, sets `body { margin: 0 }` in its own CSS cell so the number beside the slider is the number the arithmetic underneath explains. A test asserts that, because removing one line of CSS would silently put the page's own claim 16px out.

**`named-grid-areas`' two drawn maps become one grid the reader resizes**, laid out by the tutorial's own two `grid-template-areas`, with a container query at the same 350px the page's media query uses and a slider that reads out the width it is setting.

Two wrong turns on the way there, both worth keeping. `resize: horizontal` was the first attempt and is the nicer gesture — and it is mouse-only, so on a phone, where the reading column is narrow enough that a reader would never reach the wide map, the diagram would quietly show half of itself. A pair of radios replaced it, and that was a self-inflicted constraint rather than a finding: it came from a rule of "no JavaScript" that does not apply here. Josh: "so wait... we can't use a slider?" A range input cannot drive CSS without script, but the script does not have to live beside the diagram — `wireDiagramWidthSliders()` in `assets/tutorial-runtime.js` is generic (`data-dl-width-for="<id>"` sizes that element and fills the `<output>` beside it), waits on no Run button, and reaches a downloaded page because `build.py` inlines the standalone bundle into every one. Verified on both. The control ships `hidden` and the runtime reveals it, so a reader without JavaScript gets the diagram at its starting width rather than a slider that does nothing.

**And the slider caught a bug the buttons had been hiding.** With the dashed frame's padding and border on the same element the container query measured, `* { box-sizing: border-box }` meant a declared 350px left a content box of about 324 — so the map changed shape at an outer 376px while its own caption, and the tutorial's media query, said 350. Two fixed widths never showed it; a slider with a number on it showed it immediately. The frame moved to a child element, and a test now forbids padding or a border on the queried element. It is the same mistake `flexbox-first-steps` is about, made one diagram later.

**What stays drawn, and why it is not a retreat.** The box model and the annotated traceback keep their markup diagrams: neither is a thing you resize, and both carry annotation — four named regions, a responsible line against a failing one — which is precisely what a live demo cannot hold still long enough to say. `flexbox-first-steps` keeps one card at full size, because "your 80px is 114px once the border and padding are outside it" is a fact about a single card that no amount of dragging reveals; the three-card row it used to sit beside is gone, since the preview does that better.

Flexbox Froggy, Grid Garden and Anchoreum are linked from the three nearest tutorials, on Josh's ask. Anchoreum teaches CSS anchor positioning, which this course does not cover; it is framed as where `position` has gone since rather than as required reading.

*Cost to change: low for the diagrams themselves, each self-contained markup and CSS. Two changes touch `assets/tutorial-runtime.js` and so the committed vendor bundle, which is what cannot be reverted by editing a tutorial — the preview's pixel readout and `wireDiagramWidthSliders()`. Both are additive: the preview slider behaves as before for a page that ignores the number, and the width-slider wiring does nothing on a page with no `data-dl-width-for` on it.*

---

**7.201 — The web-authoring demos get the plushie shop the database course already sells from, and `the-box`'s demo gets a second box, without which its own prose describes something the reader cannot see.** Josh: "lets make sure that we use examples that really show the user what is going on and that have a bit of whimsy."

Two separate things, and the first is not decoration. **`the-box` had one box.** Its "Why this happens" says margin "pushes neighbouring boxes away rather than changing this box's own size" — and the demo had no neighbour, so a reader changing `margin` saw the box shift relative to the page edge and nothing else. That is the weaker half of what margin does, and not the half the page claims. Two boxes now, and the page says what the reader will actually see: set `margin` to `4rem` and the gap between them is `4rem`, not `8rem`, because two margins that meet do not add up. Measured in a browser before it was written down — 64px, not 128.

**The whimsy is the house's own, not a new one.** The database course sells Squishy Squid, Cuddly Cuttlefish, Nautical Nautilus and Octo Buddy, with descriptions like "six arms too many to count correctly"; every web-authoring demo said `One`, `Two`, `Three`, `Header`, `Button`. So the web course now builds that shop's page: three plushies on the flexbox cards, the shop's own header, menu, main and footer on the grid. It costs nothing and it joins two courses that had no reason to look like different products.

**One trap, checked rather than assumed.** A flex item's automatic minimum size is its min-content width, so a card label whose longest word is wider than the 80px `flex-basis` stops the row wrapping where `flexbox-first-steps`' arithmetic says it does — and the 366px the page names, and the diagram under it, quietly go wrong while the demo carries on working. Measured at the cell's own 16px sans-serif: "Cuttlefish" is 67px, the longest word in the set, and the threshold is still exactly 366. A test caps the longest word on a card and says what to do if a future one goes over.

The grid diagram's cells still read `header`, `nav`, `main`, `footer`. Those are literal strings from `grid-template-areas`, not labels — whimsy there would break the one correspondence the diagram exists to make.

*Cost to change: nil. Content in three markdown cells and two paragraphs of prose.*

---

**7.202 — Arc 2 gets the door Arc 1 always had: a page that introduces and links `project_wad`, which eight tutorials sent readers to a fork of without anything ever naming it.** Josh, remembering two starter repositories and asking whether they were still there: "I thought we had linked to two repositories under my handle that were basically the playgrounds for them to jump through hoops and learn how things work. Is that still in those tutorials or have we kind of lost that somehow?"

The repositories are fine. `deweydex/portfolio_wad` and `deweydex/project_wad` are both public and both current. What was missing is the second door. `portfolio_wad` has a whole tutorial devoted to it — `your-copy-of-the-starter`, in Welcome, which explains the two ways to take a copy and links it. `project_wad` appeared in eight tutorials, always as "Let's open your fork of `project_wad`", always in backticks, **never once as a link**, and introduced nowhere. A grep for any mention that is not "your fork of" returns nothing.

So the Arc 2 series opened on `planning-a-site`, whose first "Your turn" reads "Let's open your fork of `project_wad` and its `planning.md`" — addressed to a reader who has never heard of that repository, has never been told to take a copy, and has no link to follow. The consolidation plan calls `project_wad` "the second starter, section 15's Arc 2 door"; the starter was built on 2026-09-05 and the door never was.

`your-copy-of-the-project-starter` is that door, first in "A site with several pages". It mirrors the Arc 1 page's shape rather than repeating it — the two buttons are named, and the explanation of what each does stays where it already is, one link away. What it adds is what a reader actually needs at that point: that this is a *second* starter and why, that it is a skeleton rather than a finished site, what the five pages and three documents are, and that `planning.md` comes before any HTML. Written from the repository's own files rather than from the plan's description of them.

**Two structures had to learn about it, and only one of them said so.** `courses/web-authoring.yaml` places it; `planning/curriculum/topic-groups.yaml` is the one that fails a test when you forget (`test_every_real_tutorial_is_reachable_from_some_group`), which is how this was caught rather than shipped as a tutorial reachable from the series but not from the topics page.

No glossary file. The one term the Arc 1 page defines is *fork*, and redefining it here would be the vocabulary report's own complaint.

*Cost to change: nil. One folder, two list entries.*

---

**7.203 — Database Methods opens with the three GitHub pages Web Authoring already had, shared rather than copied. Only three of that series' eight pages were track-neutral, and one sentence had to change.** Josh: "I think we need to have the web authoring and database methods start with our github series... then we can link to that series if they haven't done it already."

**The link he wanted comes free, because the machinery already existed.** A tutorial can sit on more than one course — twelve already do, the whole of Programming Foundations across `programming-design-principles` and `mit-pdp-maths-prog-integration` — and it brings the course chooser, the tree drawn for whichever course the reader came from, and one saved-progress key across both. So a reader who did these pages on the web track arrives on the database track with them already behind them, which is exactly "link to that series if they haven't done it already" without a link.

**But the Welcome series is not a GitHub series, and sharing it whole would have been wrong.** Counting web-specific words across its eight pages: `issues-and-pull-requests` has none at all, `a-github-account` has three (one of them the sentence "Everything in this course, on either track, starts with a GitHub account" — written for both tracks, listed on one), and `an-editor` has three, all in one opening sentence. The other five are web through and through: `how-the-pieces-fit` has sixteen, `your-copy-of-the-starter` is about `portfolio_wad`, `publish-it` is GitHub Pages, `the-two-loops` is edit-save-refresh against commit-push-Pages, and `the-inspector` is browser devtools. A database student sent through those would be reading about publishing a website.

So three pages move, not eight, and the one sentence that assumed a track — "HTML and CSS files are plain text" — becomes "Code is plain text, whatever language it is written in". The alternative generalisations were worse: naming SQL and Python files would promise the database track something it does not ask for, since its SQL lives in cells rather than in files.

**Web Authoring is untouched.** Its Welcome series keeps all eight in their order; the three simply also appear under a new "A GitHub account and an editor" at the head of Database Methods. Nothing about the web track's shape changes, which is the cheapest way to get what was asked. `topic-groups.yaml` needs nothing either: its test asks that every tutorial be reachable from *some* group, and these three already are, through `web-authoring-orientation`.

Left undone deliberately, and worth a decision later: Database Methods has no starter repository of its own, and `how-the-pieces-fit` has no database counterpart — so a database student now meets GitHub without meeting a reason to use it. That is a gap this entry narrows rather than closes.

*Cost to change: nil. One sentence and one list of three.*

---

**7.204 — Give Feedback stops being a full-height rail and becomes a small popover above its own circle; the My Notes link leaves the wordmark block and goes to the top of the Notes panel, where a reader looking for their notes would actually look.** Josh: "the report button makes an odd side bar where it should be a more user friendly… the 'my notes' at the top left under the logo and name should clearly be in the notes tab as a link."

**A rail is a shape for something you read beside the page; a report is something you read once.** 7.194 gave Give Feedback its own circle at the bottom-right, on exactly that reasoning — "a report is something you reach for, not a preference you set" — but left the thing the circle opened as `.dl-right-panel`, the same full-height column Notes, Python and Settings use. So one paragraph, three links and a line about signing in were handed a box the height of the screen, docked to the top-right edge, nowhere near the corner that had just been clicked, with the reading column shoved sideways to clear a panel that was empty for four fifths of its length. The circle had already been moved for the right reason; what it opened had not followed it.

`#dl-report` keeps `.dl-right-panel` — its type, its colours, its phone bottom sheet, its place in `RIGHT_PANELS`' one-open-at-a-time rule — and gains `.dl-report-popover`, which overrides only the geometry: anchored `bottom: 4.25rem; right: 1rem`, directly above its own circle and sharing its right edge, as wide as 21rem and no taller than its contents. The rule sits between `.dl-right-panel`'s own geometry and the phone rules at the foot of the stylesheet, so the same-specificity cascade resolves correctly at both ends — this overrides the rail, and the phone's bottom sheet overrides this, with no `!important` needed on either side.

**Two behaviours follow from being a popover rather than a rail, and both are the opposite of what the rails do.** It closes on a click outside it, where 7.199 deliberately stopped the rails from doing so: that entry's own governing quote is "a docked rail must not close on an outside click, *unlike a popover*", so this is not a reversal of 7.199 but the other half of the sentence finally having something to apply to. And it is no longer remembered from one page to the next — `saveSidebarState()`/`restoreSidebarState()` now read `RIGHT_DOCK_PANELS`, the three rails, rather than `RIGHT_PANELS`. A rail left open is a way of working, worth carrying forward; a feedback box reopening over every page a reader visited afterwards is not. `watchPanelOverlap()` reads the same shorter list, which is what stops the reading column reserving a gutter for a box floating in the bottom corner over margin the docks already hold.

**Its `<h2>` is visible, alone among the panels.** 7.183 made every panel title screen-reader-only on the grounds that the corner tab opening it already shows its name. That reasoning does not reach this one: the circle is an icon with no label, so with an sr-only title nothing on screen said what the box was. The rule it came from is intact; this is the case it never covered.

**The My Notes link had the same problem from the other direction — right content, wrong place.** 7.195 put it under the wordmark, in `.dl-corner-identity`, because `{{ROOT_BASE}}` was already substituted there and threading a new root-relative path through `site_footer()`'s seven call sites was not worth it for one link. That reasoning was about where the *token* was convenient, not where a *reader* would look — and the top-left block answers "where am I", which is not the question somebody wondering what they wrote last week is asking. It moves into `#dl-yourwork`, above this page's own notes: the panel is the one place on the page that is already about the reader's own writing, and the token substitutes there exactly as it did before, so the convenience that chose the old home comes along unchanged. Freed of having to stay quiet enough not to compete with the wordmark above it, the link can look like a link — link colour, an arrow, a rule under it separating every page's notes from this one's, and a line saying what it gathers.

*Cost to change: low. One CSS rule block for the popover's geometry and one for the link's new setting; one constant split in two in `tutorial-runtime.js` (`RIGHT_DOCK_PANELS`, with `RIGHT_PANELS` built from it, so every existing use that meant all four still means all four); one `pointerdown` listener, scoped to this one panel by name; and one element moved between two places in `shell.html`. Reverting is the same pieces taken back out — nothing here changed what a report or a note *is*, only where the box holding it sits.*

---

**7.205 — Computer graphics arrives as a three-page series on Computational Methods and a three-page series on Web Authoring, built round one division, with the same ball and the same cube on both.** Josh, with a link to Gabriel O'Flaherty-Chan's *Divide by depth for instant 3D*: "help to make a little series in computational methods about the basics of computer graphics using matrices … a few little tutorials in web development involving animation perhaps with python or JavaScript or even just pure css."

**The post's own order is the series' order, and it is the right order for this course.** The post starts with $x' = x/z$, adds a camera position, then a rotating cube, and ends at the 4×4 projection matrix with its field of view and its near and far planes. That is discover-first-name-afterwards already: the divide is met as a fence-post picture before anything is called a projection, and the matrix that a graphics card is handed is the last thing on the page, not the first. So `a-point-on-the-screen` is the divide, the camera, and the post's orbiting ball; `turning-a-cube` is the rotation matrix and the post's cube; `the-fourth-number` is homogeneous coordinates, and the closing matrix. The series sits after Matrices, whose `multiply` it uses unchanged, and the third page gathers that toolkit into `setup/cube.py` rather than pasting thirty lines at the top of a page.

**Hand-rolled lists, not numpy.** Every Matrices page multiplies with the reader's own `dot`/`transpose`/`multiply` over nested lists, and nothing on the course has met numpy. Eight corners and a 4×4 are small enough that the cost is nil, and a cube drawn by the function the reader wrote three tutorials ago is the point.

**Our camera looks along positive $z$; the post's looks along negative $z$.** The post follows OpenGL, so its projection matrix has a $-1$ where ours has a $1$ and its $w$ is $-z$. A course that has just told a reader "depth is how far in front of you" cannot then say depth is negative without an aside on every page. The third tutorial names the difference once, beside the matrix, and says the arithmetic is the same.

**Web Authoring's series comes after Arc 2, not inside Arc 1.** The three pages need `transform`, `@keyframes` and `animation`, all taught at the end of *Your first site*; placing them there would have split the site-building arc to fit in an orbit. After *A site with several pages* they are a coda, and the reference panel still inherits everything before them. The pure-CSS orbit is written so that the first editor has a flaw the reader watches for (the ball is a disc glued to a turntable and vanishes edge-on), and the second editor fixes it; the CSS cube is six pushes and five turns, with the transform order read right to left and linked to *Two Turns at Once*. The third page is the course's first JavaScript, and the first `js site` pane on the site: an animation loop on a canvas, with the divide written by hand and the painter's algorithm doing what CSS did for free on the previous two pages. No practice pages, because no Web Authoring tutorial has one.

**One topic group for all six, across both modules**, since a reader who wants "the 3D stuff" wants both halves, and `topic-groups.yaml` exists for exactly the reader who is not following a course in order.

**Checked, not assumed.** Every Python cell, and every number in the three practice pages, was run. The three site editors were screenshotted in Chromium with their animations paused at several moments, which is how the ball's edge-on vanishing was confirmed as a real effect worth teaching rather than a guess.

*Cost to change: nil to reorder or drop a page; the series are two list entries each. `setup/cube.py` is read by `the-fourth-number` and its practice page only. The link from `the-fourth-number` to `an-orbit-in-css` is the one cross-course dependency, and the build would name it if the web page went.*

---

**7.206 — A matplotlib animation left at the end of a cell plays on the page, as an animated PNG, so the graphics series can show the ball going round and the cube turning rather than only a strip of frames.** Josh, looking at Pyodide's package list: "Is there a way of doing animation with any of those packages listed here?"

**The answer was nearly yes already.** matplotlib's `FuncAnimation` runs in Pyodide as it does anywhere, and its `PillowWriter` writes frames with Pillow, which every page loads for `image_input()`. What was missing was on dewlab's side: `_render_value()` knew figures and tables and fell back to `repr` for everything else, so an animation at the end of a cell printed `<matplotlib.animation.FuncAnimation object at 0x…>`. One more branch renders it.

**Animated PNG, not GIF, and not matplotlib's own HTML player.** `Animation.to_jshtml()` is the notebook answer, and it is a block of HTML with a script in it; the page appends cell output with `innerHTML`, where a script does not run, and the hosted page runs Python in a Worker with no DOM on the far side anyway (7.77). A GIF plays anywhere but has 256 colours and one-bit transparency, so matplotlib's smooth edges go jagged and the transparent background every figure gets (so it never sits in a white box on a dark page) becomes a halo. APNG keeps full alpha and every browser dewlab runs in plays it. It goes through matplotlib's own `PillowWriter`, so the frames are what `save()` would produce, with one change: each frame is cleared to transparent before the next is drawn. The stock writer never asks for that because its frames are opaque; with transparent frames and no disposal, a moving ball leaves a trail of itself round the loop, which was checked by reading a frame back rather than assumed.

**The figure is shown once.** The frames are drawn on a figure, and a cell's leftover figures are flushed as stills at its end. Rendering the animation marks that figure as rendered, so the moving picture is not followed by a frozen copy of its last frame.

**Where it is used.** Only after the flip-book, in both tutorials that have one. The strip of frames is what teaches that a film is arithmetic repeated; the moving picture is the reward, and a reader who saw only the moving picture would have learned less. The style guide says so now.

*Cost to change: low. One predicate, one renderer and one branch in `assets/tutorial_tools.py`, with a unit test; two cells and one glossary entry in the tutorials. The `assetVersions` hash on `tutorial_tools.py` already tells a cached page the file changed.*

---

**7.207 — The six graphics pages are rewritten in the register of Josh's own class handouts: worked numbers in the prose, small numbered steps, short lists of what each part of a cell does, key terms in bold italics, and every animation idea explained from a still picture up.** Josh: "let's see if we can really simplify the language and explain everything that is going on as animation would be new to folks … Nice bold key words and introduce context and connections where possible", and then, with five of his handouts attached: "Let's use these as our style guide here—we want real concrete texts but we can use more bullet points."

**What the handouts do that the first draft did not.** They work an example with real values in the running text (*encrypt(albatross) → grhgzxuyy*), not only in a cell. They break a task into small numbered steps. They put "things to keep in mind" in a short list. They ask the reader a question and leave it there. They name the feeling ("brain-pain") and hand over a route. And they are warm without being soft: the register is a person talking, footnotes and all. The rewrite takes each of those. Every page now walks at least one number through by hand beside the cell that computes it, every "your turn" that has steps lists them, and the animation pages explain frame, frame rate and loop before any animation runs, because a reader who has never thought about how a screen moves has nothing to hang `interval=60` on.

**Bold italics, not bold.** The style guide's italics are what `dev/curriculum_map.py` and `origin_anchor()` read to find where a term is introduced, and a plain `**term**` would have made these six pages invisible to both. `***term***` renders as `<strong><em>`, so the term machinery still sees the `<em>`, the reader sees bold, and `EMPHASIS_RE` now reads the triple form too. Whether every page should move to bold is Josh's call for another day; the guide says a page *may*.

**Lists, with a rule.** §9 asked "are the explanations prose rather than bullets?" and the honest answer on these pages is now "mostly". The checklist line says where a list earns its place: the small steps of a task, what each part of a cell does, things to keep in mind, things to try one at a time. An explanation of *why* stays prose.

**Cells untouched.** The rewrite was assembled by pasting each fence back in by its id, so no cell's code, id or hint changed and no saved work is at risk. Every number quoted in the new prose was run.

*Cost to change: nil for the prose. The regex change is one alternation with a test.*

---

**7.208 — A third companion page, the context page (`context_for:`): optional background reading beside a tutorial, off the reading order the way a practice page is, and linked both ways with a line saying nothing on it is needed.** Written so that tutorials can be held to a length a student can finish in about an hour.

**Why it exists: a tutorial should be doable in about an hour, and most of what makes one run long is not the task.** Where an idea is used in the wild, why browsers behave as they do, a piece of history, the deeper detail behind a simplification — all worth having, none of it needed to finish. Left in the tutorial it lengthens the one page a student must read. Deleted, it is lost to the student who wanted it. A context page is the third option: the material moves out, onto a page the tutorial links to and says plainly is optional. The same sorting sends the other kinds of overflow elsewhere. Common mistakes are practice, and belong on the practice page, where a student meets them as problems rather than as warnings read in advance. And a tutorial that is long because it teaches two ideas is split into two tutorials rather than trimmed — trimming it keeps both ideas and teaches each worse, while splitting keeps each at the length it needs. Only what is left over, the background, goes on a context page.

**Mechanically it is a practice page with a different job.** It is an ordinary tutorial file in its own folder, `tutorials/<id>/<id>.md`, like a mixed set, since it may serve several tutorials and so belongs to no one folder. `Tutorial.is_companion` (practice or context) is the gate for "not a teaching page on the route": `series_of()`, the search index, the reference index and its facets, the title/overlap notes, the "no course lists X" note. Its placements, crumbs and course come from its first owner, the same as a `practice_for` page in `crumb_trail_html()`, and its Reference panel is the union of its owners' cumulative glossaries through the same branch of `cumulative_glossary()`, now reading `Tutorial.owners`. The gates that stayed `is_practice` are the ones about problems specifically: `practice_pairs()`/`mixed_practice()`'s own checks, the practice link itself, and the "practice" tag in a downloaded folder's start page. Context pages are not put in the series or course zips — they are optional, and a folder of files numbered in the order to open them is the wrong place for something nobody needs to open.

**Refused, each as a build error:** an unknown id; naming a practice page or another context page; naming itself or an id twice; also setting `practice_for`/`practice_across` (a reader has to be able to tell optional reading from work); `covers:` (nothing on it is needed, so it cannot be where an outcome is taught, on the same reasoning as a practice page); being listed in a course file. The other direction is refused too: `practice_for:` or `practice_across:` naming a context page, since practice sets problems on what a tutorial teaches.

**Unlike practice, a tutorial may have several.** A practice page is the one set of problems for a tutorial; background splits naturally by subject, and each context page is read only by whoever wants that subject. So `context_pages()` returns a list per tutorial, in title order, and each gets its own link block.

**What the runtime does not know.** `assets/routes.json` carries no context pages, so on a tutorial listed on two courses, the runtime's redraw of the tree for the second course (`drawCourseChrome()`) leaves a context page's own series rung as the default course's. The tutorial's own rung, which lists its context pages, is moved intact and keeps them. Teaching the runtime about them would mean rebuilding the vendor bundle, and nothing is wrong in the meantime, only less specific.

*Cost to change: low. One validation function, four properties on `Tutorial`, one link function, one contents-page helper, and the `is_practice` → `is_companion` swap at the gates listed above; no page uses `context_for:` yet, so dropping the feature costs nothing but the code. Allowing `covers:` later would be the one change with reach, since it would put optional reading into the curriculum map.*

---

**7.209 — Web Authoring is rolled out to the one-hour model: pages that taught two ideas are split, every tutorial with a task gets a practice page, background moves to context pages, and a context page's own glossary joins its reference.** Josh, after the layout pilot (7.208): "no students have touched any of the stuff yet, so we do not need to worry about them losing work … splitting does not have a cost", and on the pilot's plan: "go ahead in that order".

**Split, not trimmed.** Six pages carried two ideas and became twelve: `images-and-alt-text` (paths) and `describing-an-image`; `keyframes-and-the-checkbox-hack` (keyframes) and `the-checkbox-hack`; `named-grid-areas` and `order-on-screen`, with `auto-fill` moving to `a-grid-gallery` beside `auto-fit`, the only page that teaches `repeat()`; `position-and-the-sticky-header` and `footer-at-the-bottom` (the pilot); `an-orbit-in-css` and `a-ball-that-faces-you`, which comes after `a-cube-in-css` because it leans on the transform order that page teaches; `drawing-frames-with-javascript` and `a-cube-on-a-canvas`. This supersedes 7.205's three-page *Movement and depth* and its "no practice pages": the series is now five pages, two context pages, and a practice page for each. `css-variables-and-bem` stopped re-teaching variables and became a naming page.

**Cells changed where no student could have saved work.** The orbit's `.stage` carried both `transform-style: preserve-3d` and the dark background, which puts the background into the scene as a sheet at depth 0; the ball vanished for the back half of every turn, not only behind the sun, so the page's own claim was false. The background moved to `body`, checked in Chromium before and after, and the broken version became a practice problem. Moved cells kept their ids; pages that lost or changed cells were bumped.

**Practice is where the mistakes went.** Warnings a tutorial made in prose (a forgotten closing tag, a capital letter in a path, `margin: 0 auto` with no width, a sticky header with no `top`) became broken pages to fix. Every broken cell and every answer was rendered in headless Chromium and measured, and every own-site task names only rules and classes that exist in `portfolio_wad` or `project_wad` and ends in a commit, so the work is evidence in the student's own repository. Reading pages got a practice page only where a real task fits.

**A context page's own glossary is read.** 7.208 gave a context page the union of its tutorials' references and no glossary of its own, on the practice-page reasoning. But background reading defines what its tutorials never needed (*specificity*, *DNS*, *viewport meta tag*), and a reader of that page should find those terms on its panel. `cumulative_glossary()` now appends the page's own entries after the union; the reference index still leaves them out, as optional reading.

**One outcome stays on a tutorial.** `conclusions-and-next-steps` was the only page covering WA-LO1, the history of HTML and CSS versions. A context page cannot declare `covers:`, so the full history moved to `how-html-and-css-got-here` and the conclusions page keeps a short section that carries the outcome.

*Cost to change: splits are course-file lines and folders; merging two back is a paste and a `covers:` edit. Practice and context pages are independent files a course never lists, so dropping any of them touches nothing else.*

---

**7.210 — Programming Foundations is reordered so that no page uses what a later page teaches: functions get one page of their own, dictionaries get a page, the error page is split, and the history page moves to the end.** Josh, on the order problems a language pass surfaced: "I agree with your suggestions", and that the titles "could also use some clearer titles (almost all of them)". No student had used these pages, so cells moved freely.

**What was out of order.** `how-we-got-here`, third, set decoding tasks that needed loops and functions and showed the same program in four styles. `when-it-goes-wrong`, fifth, taught `IndexError`, `KeyError` and tracebacks through functions before lists, dictionaries or functions existed. Functions were introduced three times, in `lists-and-sequences`, `finding-things` and `building-reusable-tools`. Dictionaries and f-strings were used and never taught. Each page coped with a note saying "we meet this later", which made each page readable and the series harder to trust.

**The new order.** first-steps, storing-and-computing (now with f-strings), making-decisions, `reading-an-error-message` (new: syntax errors, the runtime errors a beginner can hit with variables and arithmetic, a one-step traceback), repeating-yourself, `writing-your-own-functions` (new: assembled from the three introductions, with no lists in it so that it can come before them), lists-and-sequences, `looking-things-up-by-name` (new: dictionaries), finding-things, putting-things-in-order, building-reusable-tools, `when-it-goes-wrong` (now the later half: errors from lists and dictionaries, tracebacks through several functions, logic errors, debugging habits), how-we-got-here. Functions come before lists, not after, because the lists page already writes functions for its sequences and dot product. The history page is last because it carries PDP-LO1 and LO3, so it cannot be a context page, and at the end its four-styles comparison leads into the OOP module.

**Outcomes moved with their sections.** PDP-LO8 and MIT-6.2 follow the function sections to the new page; PDP-LO9 is covered on both error pages. No outcome has a dictionary in it, so the dictionaries page only touches PDP-LO4.

**Titles say what a page teaches**, as on Web Authoring (7.209): "Repeating steps with loops", "Searching a list: linear and binary search", and so on. Ids are unchanged, so addresses are too.

*Cost to change: the order is one list in each of two course files. Moving a page back means re-checking its "earlier/later" sentences, which a sweep did once for this order.*

---

**7.211 — Fundamentals of OOP and Computational Methods get the same treatment as Programming: one idea per page, pages in the order they are needed, and titles that say what a page teaches. Computational Methods lists the Programming Foundations pages it depends on, and *Working With a Table* moves to Database Methods.** Josh: "Computational methods take the maths class alongside … There is no problem with linking through", and "Lets move working with a table to database methods!"

**OOP.** `the-moves-you-already-know` used a class before `objects-and-classes` taught one, so it now comes second, as the bridge from the four familiar moves to methods. `objects-and-classes` taught classes, encapsulation and inheritance in one page; it now teaches classes and objects, with `__str__`/`__repr__` and class against instance attributes added, and encapsulation has a page of its own (`keeping-details-inside-an-object`), which also corrects the old claim that outside code had "no other route" to a field: in Python it does, and the page now teaches the underscore convention instead. Inheritance lives only in `one-parent-many-children`, which now teaches it from the start; composition, which was a section of that page, is `objects-inside-objects`, straight after it, with an "is a / has a" test. `a-front-end-for-a-class` gets the course's missing practice page, driven by a fake `input()` so the menu loop can be tested in a cell.

**Computational Methods.** Its opening series was a page on running cells and a pandas page; from the third page on, the matrices used functions, nested lists and comprehensions nothing in the course had taught. The series now lists seven Programming Foundations pages after `first-steps-cm` (variables and f-strings, decisions, reading errors, loops, functions, lists, dictionaries), each one checked against what the course's cells use. A tutorial may sit on two courses, and a student doing both meets the same page once. Comprehensions, used on a dozen pages and taught nowhere, are a section of `lists-and-sequences`, so both courses have them. `a-point-on-the-screen` taught dividing by depth and then a camera and an orbit; the second idea is `a-ball-in-orbit`. The Algorithms pair is swapped so that recursion (`finding-everything-inside-a-folder`) comes before the page built on it (`three-ways-to-make-change`), and that page's coins are euro cents.

**Checked, not assumed.** Every new or changed cell and practice answer was run, and a good number of claims failed on running: a text counted as ten words that has sixty, a learning-rate lesson that does not hold when the weights start at zero, a greedy exercise with no answer, a seed that did not show the repeat the prose promised, practice answers that contradicted their own tutorials. Each is corrected where it stood.

**`working-with-tables` moves to Database Methods**, before `loading-a-real-dataset`, the first page there to use pandas. Nothing in Computational Methods built on it; in Database Methods each pandas step sits beside the SQL it matches.

*Cost to change: orders are course-file lines; a page listed on two courses is one file. Undoing a split is a paste and a `covers:` edit.*

---

**7.212 — Every table in Database Methods follows one naming convention: singular names ending in `_tbl`, primary keys named after their table (`product_id`, never `id`), foreign keys named after the key they point at and placed directly under the primary key.** Josh, passing on his co-teacher: "tables should have _tbl at end and id should be named after table such as product_id. Would also be consistent about fk location, either under id or at bottom of table. Also on PK side I'd link from id not table name", and, on the examples: "we can keep the original topics (which are more fun) but just fit the convention … having multiple examples is better as they don't get too focused on the one thing."

**Why a name should say what it is.** With every key called `id`, a join reads `ON dinosaurs.id = sightings.dinosaur_id`, and a line in an entity relationship diagram runs from a row labelled `id` that could belong to any table. Named after its table, the key reads the same at both ends, `dinosaur_tbl.dinosaur_id = sighting_tbl.dinosaur_id`, and the diagram's line runs from `dinosaur_id` to `dinosaur_id`. `_tbl` tells a reader, in a query of many names, which of them are tables. `erd.py` already drew each relationship from the parent's key row; a test now fails if it ever moves to the name band.

**Foreign keys under the primary key**, the arrangement every existing table already had, is now the rule, so every table and every diagram opens the same way: its own key, then the keys it points through, then its data.

**The topics stay.** Dinosaurs, students, plushies, the library, the timetable and the published datasets keep their subjects; only names changed, across every page, the quizzes' check cells, the full-stack page, the reference shelf and the four diagrams, which regenerate from the pages' own `CREATE TABLE` statements. Two exceptions, each explained on its page: a table loaded straight from a CSV keeps the CSV's column names, and `country_region_tbl` keeps `country` as its key, because the join to the income data is by country name.

*Cost to change: a rename throughout the course's SQL, its quiz checks and `dev/graphics/database_methods.py`; the diagrams follow by regenerating.*

---

**7.213 — Every page title names its subject in the words a student would search for, the entity relationship diagrams stack tables in whichever order crosses fewest lines, and the portfolio starter's known faults are written down in dewlab until they are fixed there.** Josh: "make a note of the issues in portfolio_wad in a md file and fix the other non-video issues … see if we can improve some tutorial or practice titles in all series."

**Titles.** Forty-nine pages still carried titles from before 7.209–7.211. They were in Title Case, and often a phrase that only makes sense once the page has been read: *Cracking Equations*, *Expressions Come Alive*, *When There Is No Answer*, *A Table Is a List of Rows*. They now follow the pattern the other series already use, a familiar term and then what the page does with it: *Solving equations: linear, quadratic and simultaneous*, *Polynomials: representing and combining them in Python*, *Complex numbers: roots that are not real*, *Tables in SQL: CREATE TABLE, INSERT and SELECT*. Mixed-problem pages read "Mixed problems: …". The practice pages follow their tutorials, the stale `**Maths for IT**` label lines under the old titles are gone, and every link, italic mention and generator docstring naming an old title now names the new one. `dev/curriculum_map.py` finds a dependency by its title in prose, so a missed mention would have lost it one. Ids are unchanged. The only cell touched is one comment in `complex-roots`, which named the old title. The curriculum map's sequence graph cut every title at its first colon, a leftover from "Tutorial 14: …" numbering, which had already clipped the Programming titles from 7.210 to "keeping many values in order". It now drops only that numbering prefix.

**Diagrams.** `erd.py` stacked the tables in a column alphabetically and gave out lanes in whatever order it met the edges. In the timetable diagram, that sent `room_tbl`'s line across `programme_tbl`'s, and its line and `teacher_tbl`'s crossed twice below the boxes. Lanes are now handed out by rule: the line leaving highest takes the lane furthest out, and the lines that drop below the boxes nest. `_arrange` then tries every order of tables within each column and keeps the one with the fewest crossings, preferring alphabetical on a tie. That costs little for a student's schema, and it stops trying past 2,000 orders. The timetable now has no crossings. The library diagram keeps one, which no order avoids. The first lane also moved clear of the "one" bar, so no line turns a corner on top of it.

**The starter.** A browser audit of `portfolio_wad` found fourteen problems; `planning/PORTFOLIO_WAD_ISSUES.md` lists them with tested fixes, for fixing in that repository. Three touched dewlab pages, which now say what a student will see:
- *Changing the layout for phones* told students to delete only the comment markers around Exercise 24. That drops the whole block, because the instruction shares a line with `/*`. It now says to delete both whole lines.
- The hover-and-focus practice claimed every other button kept a visible outline. The hero's button is invisible in the same way.
- The transitions practice has students hover the contact button, whose label turns white on near-white. Its answer now says so, and gives the fix.

*Cost to change: a title is one frontmatter line plus a text sync. The arrangement is one function, and returning to alphabetical is `_arrange` returning its first candidate.*

---

**7.214 — Completion asks Jedi first, in the tutorial cells and in dewmini, and it reads the live namespace as well as the text.** Josh: "Can you check that pyodide is using Jedi and that Jedi is used in dewmini and the Python cells themselves?"

**What the check found.** Jedi was loaded in both engines (7.76, 7.77), but only for hover docs and signature help. `vendor-src/codemirror-entry.js` had a `jediCompletionSource` and a `getJediCompletions` option, but no editor passed one and no engine could answer one, so completion never reached Jedi. Its four sources were keywords and builtins, names typed in the cell, and names on the page. None of them looks inside an object. In a real cell, `math.sq` and `word.up` offered nothing, before or after a run.

**What changed.** A third Jedi helper, `_dewlab_complete`, sits beside the other two in the worker and in both main-thread engines. It is a `jedi.Interpreter`, not a `jedi.Script`: it reads `_page_globals` as well as the cell's text. So after a cell has run, a name completes the attributes its live object has, including ones no reading of the source could find. While a definition is still in the same cell, Jedi reads that text in preference to the live object, so the live answer shows from the next cell on. Names starting with an underscore wait until the reader types one, and file paths inside strings are left out. Both are noise for a beginner reaching for `upper`.

In the editor, Jedi answers first and the older sources are each gated behind it, so nothing is listed twice. They answer as before when Jedi is silent: still loading, a Worker busy with a long cell, or nothing to offer here. A keystroke waits at most 400ms for Jedi.

**The first answer is slow, and is kept.** Jedi's first look at a module reads its stubs. In the self-hosted Pyodide, a first `math.` took 461ms and a first string method list took 729ms; after that, 13 to 50ms. Those first answers would have been lost behind the 400ms patience. They are kept instead, and the list reopens with them if the cursor has not moved. The alternatives were worse. A longer patience makes every keystroke wait behind a busy Worker. Warming Jedi up at boot would block the first Run for about a second.

The tutorial cells and dewmini's cell and file editors share the wiring. Four new e2e tests cover it:
- a module's attribute before any run;
- an attribute only the live object has;
- underscore names waiting for an underscore;
- dewmini's own editor.

They ran green four times in a row against the self-hosted Pyodide.

*Cost to change: one Python helper in three copies, one engine function in two, and `pythonCompletion()` in the editor entry. Turning Jedi completion off is leaving out `getJediCompletions`, which restores the old sources exactly.*

---

**7.215 — The glossary's Python entries are checked against Python itself, and the reference shows each function's signature as Python gives it; the definitions stay hand-written.** Josh asked whether Jedi could take over the glossary and reference panel "so we can simplify that". Having seen what it would replace, he chose two narrower steps: "let's do 1 and 2".

**Why not replace the glossary.** Of 688 entries, 437 are concepts and 52 are formulas, and many of the functions and keywords are CSS, HTML or SQL. At most about one in ten names something Jedi can describe, and for those, Python's docstrings are written for programmers. `len()`'s is plain enough. `super()`'s begins "super() -> same as super(__class__, <first argument>)", and pandas' `to_csv()` runs to several pages. The panel's own rule, that it shows only what a reader has met, is course order, which Python cannot know. The real docstrings already reach a reader: hovering a name in a cell shows them (7.76).

**What changed.** An entry that names something in Python says exactly what, with `python:`: `list.append`, `[math.sin, math.cos]`, `tutorial_tools.check`, `elif`. Eighty entries, and two in Python Basics, now carry one; 87 names in all.

`dev/glossary_python.py` checks each against the real thing:
- **The name exists.** It is a keyword, or it imports and every attribute is there.
- **The example fits the signature.** Every call in the example to that function is bound against its own signature, without running anything, so too many arguments, too few, or a keyword it does not take all fail. An example that is not Python, such as CSS in a Web Authoring entry, is left alone.

Injected mistakes were each caught by name: `list.apend`, `len(scores, 2)`, and `random.sample(deck, size=5)`, whose `k` is required. The script also writes `assets/python-signatures.json`. `with_python()` in `build.py` attaches each entry's signatures, and the tutorial reference, Python Basics and dewmini's reference all show them under the definition, labelled **Signature** and outlined rather than filled, so a signature never reads as an example to copy.

**What gets a signature.** Built-ins, the standard library and the course's own `tutorial_tools` do, the last under its bare names (`check(...)`), since that is how a cell calls them. Third-party libraries are checked but show no signature, because twenty-odd parameters or a trailing `**kwargs` does not help a beginner. Signatures keep Python's `/` and `*` markers. They carry rules: in `random.choices(population, weights=None, *, cum_weights=None, k=1)` the `*` is why `k` must be given by name, and deleting it would teach a call that fails. Python Basics gains a **Signature** entry that says how to read one.

**Versions.** A signature depends on the Python version, so the file is written with the one Pyodide runs (3.13). A new CI job, `glossary-python`, runs the check on 3.13, with numpy and pandas pinned to Pyodide 0.28.3's versions, and fails on a stale file. The unit job's pytest module checks names and examples on 3.12.

*Cost to change: a `python:` line per entry, one script, one build helper and three renderers. Dropping the signatures is deleting the JSON file; the build treats a missing file as none.*

---

**7.216 — The maths pages had the same language pass as Programming: plain, inviting prose, terms defined where they are first used, worked numbers after formulas, and pages that only lean on what came before them.** Josh: "Let's Continue!", after the Programming pass (7.210) had named maths as the next series.

**What the pass did.** Twenty-two tutorials and the three mixed-problem pages, with their practice pages and glossaries, went through the brief the Programming pass used, with rules added for maths:
- Every formula is said in words first, then shown, then followed by one worked number.
- "Simply", "obviously", "clearly" and "trivially" are gone, since they tell a struggling reader they are slow.
- Old numbered references ("Tutorial 14", "the last four tutorials") became links by title.
- Each page leans only on what the course has taught before it.

Many terms the maths pages had always used were never defined anywhere: *correlation*, *polynomial*, *coefficient*, *degree*, *hypotenuse*, *chord*. They are now defined in italics where they first matter, with glossary entries. The pages are 20–55% longer, almost all of it definitions, worked numbers, tables and numbered steps rather than more explanation.

**Errors the pass found**, each checked by running it or by hand:
- *Three doors* stated its own conclusion backwards: the 50/50 argument is right for a careless host and wrong for the original game.
- Four cells contradicted their pages or failed. The "exactly a half: False" cell was one. A sine fit peaked in July while its comment said June. Pay data meant to lie on a line had slopes 12.5, 12.79, 12.5. Two cells in *Solving equations* called helpers defined only on the polynomials page, and raised `NameError`.
- A counting answer said four passphrase words give "slightly fewer" choices than a 10-character password; it is about 370 times fewer.
- Other corrections:
  - a 3% difference on a cut-off axis "looks threefold" (it looks fourfold);
  - ⊂ written for "is a subset of";
  - *not* given four truth-table rows;
  - "four extensions" of the number system, where there are three;
  - a tangent line said to touch a curve at only one point;
  - a pen puzzle whose fence arithmetic needed 80 m, not 60;
  - 2^x said to lead x³ a thousandfold at x = 20 (it is about 131);
  - one radian of the Earth set at Ireland to the Sahara;
  - seven wrongly rounded answers.

**Integration.** No page gained a failing cell: every page was run old and new in one shared namespace, and the only difference is the `NameError` now fixed. The cells that still stop are the deliberate division-by-zero lessons, and cells that wait on a student's own "Your turn" function. Two terms the vocabulary report found introduced twice were resolved:
- *range* on the functions page now says it differs from the statistics range;
- the statistics page refers back to where *standard deviation* was first taught, in place of introducing it again.

The five headings the pass renamed (three in *Complex numbers*, one each in *Rearranging formulae* and *Limits*) carry their `covers:` keys with them, and the curriculum map is regenerated. The glossary check now covers 92 Python names, since the inverse trigonometric functions, `lambda` and `import` gained entries.

*Cost to change: prose only, page by page; the cells that changed carry version 2026.09.24.1.*

---

**7.217 — A reader's own functions travel from page to page: toolkit cells, with the reference as a fallback per function.** The Plot Twist plan (§6) asked for both the reader's own code and a reference version. Josh: "lets do both a 'student code' and a 'no student code' version".

**Authoring.** A Python exec cell carries `toolkit: yes`. An optional `python toolkit-reference` fence (`for: <cell id>`) holds the complete version and is never shown; a cell without one is its own reference. The build fails on a `for:` that names a missing or non-toolkit cell, and on two reference fences for one cell.

**Which pages get what.** `toolkit_for()` in `build.py` lists every toolkit cell on an earlier tutorial of the course, walking `series_chain()` as the glossary does, and never the page's own. A practice page gets its own tutorial's toolkit and everything before it. A mixed page gets all its tutorials' toolkits and everything before the latest. A page on several courses takes the first course with a toolkit.

**Whose code.** In "My code" mode (`dewlab:toolkit-mode`, site-wide), each entry runs the reader's saved code from `dewlab:progress:<tutorial>`, and each function the reference defines is taken from the reference where the reader's code leaves it out or unwritten. Unwritten means a body of only a docstring, `...`, `pass` or `raise NotImplementedError`, read with `ast`. If the reader's code raises, the whole reference replaces it. "Reference" mode runs the references only; a downloaded page always does. The toolkit loads after the namespace is seeded at boot and again after every reset, through a `"load-toolkit"` worker message or the main-thread path, with its output discarded. One line above the first cell says what loaded and why, and holds the switch.

**Why per function.** Pilot pages leave stubs that define without error. A per-cell rule would have loaded empty functions and broken every later page for a reader who skipped one exercise. The page writers found this before it shipped.

*Cost to change: additive. The manifest key and the worker message can be ignored or removed; renaming a toolkit cell's id sends later pages to the reference, the usual rule about ids.*

---

**7.218 — Plot Twist's first two units are written, and its rule on words is "never measure the reader".** The plan, `planning/DEWEY_TRACK_PLAN.md`, called for a pilot of Units 1 and 2 before the rest is written.

**The pilot.**
- Nine tutorials, each with a practice page and a glossary, and a mixed practice page for each unit.
- Units: *Instructions for a machine* and *Decisions and the logic under them*.
- Pages run from *Four questions for any puzzle* to *Bits that flip*.
- The course file `courses/plot-twist.yaml` lists them as a beta course, second on the contents page.

Every page follows the plan:
- a question from the world first;
- a "space we're in" box;
- two warm-up questions from earlier pages;
- predict, run, explain;
- a closing look back through the four questions.

Every practice page mixes predict, make, fix, explain and "another way" problems across three levels. Seven toolkit functions are built across the two units, and later pages use them: `split_bill`, `to_binary`, `to_hex`, `between`, `truth_table`, `same_rule` and `parity_bit`. Every cell was run through the real toolkit loader twice: as given, with the stubs unfinished, and finished, with the references in place. Only the cells the pages mean to fail fail.

**The rule on words.** The Programming and maths passes banned a list of words (7.210, 7.216). For this track Josh asked whether to keep the ban. The part that stays is the part that protects a reader who expects to fail: a page never says how easy or obvious something is. That rules out "simply", "obviously", "clearly", "of course", "trivially", "easy", "as you can see" and "it's straightforward". Words that were banned only as filler ("just", "actually") are allowed where they mean something: "the cell you just ran"; "Python actually prints 0.30000000000000004", marking the surprise predict-run-explain depends on. The plan's principle 8 says so; the earlier series are not reopened for it.

*Cost to change: the course file and eleven folders; nothing else depends on them.*

---

**7.219 — Plot Twist Units 3 and 4 are written; toolkit entries load like modules; a long toolkit line becomes a count and a list; and the track will show its choices.** Josh, after the pilot: "lets carry on and keep going!"

**The pages.** Ten tutorials, each with a practice page and a glossary, and a mixed page for each unit:
- *Again and again: loops, counting and chance*, from *Doing it again* to *Chances that combine*, whose mixed page builds a password-strength checker;
- *Making your own tools*, from *Machines that take a number* to *What a function can see*, whose mixed page builds a unit converter tested both ways.

They add 28 functions to the toolkit, from `total` and `product` to `close_enough`. Every page was run through the real loader twice, as for the pilot, and only the cells the pages mean to fail fail. *Does it work?* defines a small `step_through()` on `sys.settrace`, since the browser has no debugger. It was checked in Pyodide, where it matches the page's hand trace row for row.

**Each toolkit entry runs in a namespace of its own.** Two page writers found the same fault on their own. *Untangling a condition*'s toolkit cell does `from itertools import product`; *Doing it again*'s defines `product(values)`. With every entry run into the page's one namespace, the second replaced the first, and `same_rule()` raised a `TypeError` on every later page. Editing 2.3's cell would not have helped a reader whose saved copy still had the import. `_load_toolkit()` now runs each entry in a copy of the page's namespace and copies back only the names the entry defines, never the names its `import` lines bind. A later entry still sees the earlier ones. A page cell that reuses a helper's name (`RATE = …`) no longer changes what a toolkit function sees. A page cell can still hide a toolkit function by reusing its name, as `total = 0` hides `total()`; `docs/WRITING_TUTORIALS.md` says to avoid that. The 2.3 glossary term is now `itertools.product()`, so the Reference panel doesn't show two entries called `product()`.

**A long toolkit line.** By *Does it work?* the line named 34 functions in one paragraph, and by Unit 10 it would name about a hundred. Past eight it gives a count ("Your toolkit has 34 functions. They come from 14 earlier pages."), and a closed list under it names them page by page. The list marks the functions that came from the reference when the reader wrote some of their own. Eight or fewer are still named in the sentence.

**Show the choices.** Josh asked whether the four ideas could open a window on why the course is built as it is, as "participatory and transparent teaching": a student sees the choices made, what the alternatives would mean, and what larger ideas are at stake. The plan gains principle 10:
- a page on how the course is built, next to *Four questions*;
- a closed "Why this way?" box on every tutorial, naming one choice the page made and the alternative it turned down;
- Explain problems that ask the reader which way they would have taught something.

Josh: "lets go for all of those suggestions". These are written after this entry, across Units 1–4 at once so that they share one voice.

*Cost to change: the course file and twelve folders; the loader change is internal, and a toolkit that relied on one entry's import reaching the page would now need its own import.*

---

**7.220 — Plot Twist shows its choices; Units 5 and 6 are written; two context pages; Units 1–4 fact-checked.** Josh on principle 10: "lets go for all of those suggestions". Then: "lets continue with as much as we can".

**Show the choices.**
- "How this course is built" is the second page of the course. It is a letter covering:
  - the usual shape of a course like this, and what that shape does to a reader who expects to fail;
  - eight choices this course makes instead, each with its reason;
  - what those choices cost;
  - how to say when the approach is not working.
- Each of the 19 tutorials in Units 1–4 has a closed "Why this way?" fold (`dl-why`, a third fold class the build accepts and styles). It names one choice the page made and the alternative it turned down. No choice repeats.
- Ten practice pages gained an Explain problem that asks the reader to judge a choice. Its answer fold says what a good answer weighs, not what to conclude.
- Units 5 and 6 were written with their folds from the start.

**Units 5 and 6.**
- *Many values: lists, sets and data*: lists taught properly, as Unit 3 promised; averages and spread built up step by step; kinds of data and honest charts; sets; Venn diagrams. It uses the Irish rows of `life-expectancy.csv`, and its mixed page builds a report on a dataset.
- *Algorithms that scale*: searching, sorting, a race between sorts measured by counted steps, recursion, and doubling and halving. Its mixed page builds a phone-book search that stays fast at 100,000 names.
- Both units add 15 toolkit functions.
- Every page ran through the real loader both ways. The heaviest four also ran cell by cell in Pyodide in a browser.
- `data/co2-emissions.csv` gained the attribution file every declared dataset needs. The file came from Our World in Data under CC BY 4.0, as the entry that added it records.
- Two headings used an en dash, which the build's slug drops, so each page's own `covers:` key no longer matched its heading. They now use a hyphen.

**Context pages.**
- "How a computer stores a number" sits beside the four pages where a float surprises.
- "Maths that runs the world" sits beside four pages: Monty Hall (linking to *Three doors*), birthday collisions in hashes, Hamming codes through to QR codes and Voyager, and running out of IPv4 addresses.

**The fact check.** A read-only pass checked every real-world claim in Units 1–4 against sources. Two claims were wrong:
- a parkrun with prizes;
- a GPS satellite placed at the Moon's distance.

About seventeen more needed a fix or a hedge, among them:
- Java named as having a separate linker step;
- the 2005 metric limits on regional roads;
- the 13.5% VAT rate after July 2026;
- Met Éireann's wind thresholds;
- the de Méré story told as history;
- the YouTube counter;
- two pages that disagreed on the distance from Dublin to Galway.

Everything the page writers had flagged as unsure checked out. Every changed number was followed through its cells and answers.

**Still open.**
- Several pages are 2,700–3,500 words against a 2,600 target. *Doing it again* teaches `for` and `while` on one page, and by 7.208's rule it should be split.
- Units 3 and 4 use list indexing and `append` before Unit 5 teaches lists. The letter names this as a cost.
- The diagrams the page writers asked for (about thirty) wait for a single pass.

*Cost to change: the course file, the new folders and one attribution file; `dl-why` is additive.*

---

**7.221 — Plot Twist Units 7 and 8 are written.** They follow 7.220 and the plan's §5.

**Pages.**
- *Algebra you can run*:
  - letters as names;
  - polynomials as coefficient lists, with expanding as a nested loop;
  - drawing a rule;
  - linear and quadratic equations, with factorising by inspection;
  - complex numbers, as a bigger space where $x^2 = -1$ has an answer, at the cost of order;
  - the top of a curve, with completing the square;
  - simultaneous equations in two and three unknowns.

  Every answer is checked by substituting it back. The mixed page builds a phone-plan chooser and a shop's best price.
- *Shapes, angles and waves*:
  - slope, with a ramp whose gradients come from Technical Guidance Document M;
  - distance and Pythagoras, proved by rearranging four triangles, and collisions;
  - the unit circle and radians;
  - waves and octaves;
  - solving triangles, with bearings.

  The mixed page builds a collision checker for a 2D game.
- The triangle on a sphere that the plan promised is on 8.3: three right angles make 270°. The page names parallel lines as the move the plane gives and the sphere does not.
- 13 toolkit functions are added.

**Length.** The brief held pages to 1,800–2,600 words of prose, and asked writers to report a page that would not fit rather than write past the limit. Every page landed at or near it. 7.3 is the one over the plain count, at about 2,600.

**One word, one definition.** When one writer defined a term, the writers still working were told to link back to it rather than define it again: *root* and *parabola* on 7.2, *hypotenuse* on 8.2.

**Coverage on subsections.** The curriculum map counts only `##` headings as sections, so 8.3's coverage for its tangent subsection moved to the section that holds it.

*Cost to change: the course file and thirteen folders.*

---

**7.222 — Plot Twist Units 9 and 10 are written, and so is the last context page. All ten units of the plan now exist.**

**Pages.**
- *Change*:
  - limits as a sequence closing in, with a hole in a graph, one-sided limits and e;
  - the derivative as a sprinter's speed right now, and why the chord's step can be neither 0 nor too small;
  - the four rules, the quotient rule included, which the existing course leaves out. Each rule is found from tables of slopes before it is written, and checked against `derivative_at`. The page closes 7.5's promise by setting the slope to 0.
  - bisection as binary search on a number line, and Newton's method, with the case where it fails.

  The mixed page builds a best-moment finder on Ireland's CO₂ data.
- *Programs for people*:
  - the history from Lovelace and Note G to Python, every claim checked against a named source and anything unconfirmed left out;
  - one job in Python, SQL, JavaScript and BASIC. The first two run on the page. The other two are to read, and were run elsewhere to check them.
  - reviewing the reader's own toolkit as a stranger would: a checklist, refactoring under tests, docstrings as promises, a small linter;
  - the team project for three to five people (PDP-LO12). It offers three projects that name the toolkit functions they draw on, roles that change at each release, a definition of done and a rubric.

  Unit 10 has no mixed page: the project is its practice.
- *Sets in databases*, the third context page, sits beside 5.4 and 5.5. It shows union, intersection, difference and the Cartesian product as `UNION`, `INTERSECT`, `EXCEPT` and `CROSS JOIN`, with a `JOIN` as the matching pairs.
- Units 9 and 10 add 3 toolkit functions: `derivative_at`, `bisect_root` and `newton`.

**A stub no longer blocks the rest of a page.** On earlier pages every cell after a toolkit stub waits for the reader to write it. From Unit 9 on, each stub's reference code sits in an answer fold directly under its tests, and the next cell that needs the tool says to copy it in. It is a content-only change. The earlier pages could take the same fold, or the runtime could fall back to the reference on the reader's own page; that choice is still open.

**The course description** now says all ten units are written and in beta.

*Cost to change: the course file and ten folders.*

---

**7.223 — dewmini: a first cell from an empty notebook, a delete that deletes, and both workspaces on the home page.** Josh reported: "there is no way to start from nothing and just add a cell", and "delete cell wasn't working", and asked for "an easy card to access dewmini and dewmini web on the front page".

**Starting from nothing.** The toolbar's own Python and Text buttons were removed as duplicates of the insert seams. That left the seam over an empty notebook, a faint line of small buttons at 40% opacity, as the only way to add a blank cell. On a page with nothing above or below it, the seam reads as a divider rather than a control. The empty notebook's "Nothing here yet" box now has **Python cell** and **Text cell** buttons of its own. The toolbar still has no duplicate. Once there is a cell, the box hides and the seams take over.

**Delete.** A cell's delete is arm-then-confirm: the first press arms it, the second deletes. The outside-click listener that disarms it compared `e.target` to the button. The button holds an icon and a label, so a second press almost always lands on one of them. The listener then disarmed the button in the capture phase, just before its own click handler ran, and the second press armed it again instead of deleting. Delete worked only on the button's padding. The listener now uses `btn.contains(e.target)`, with a test that presses the icon and then the label. That was the only comparison of its kind in `compose/` and `assets/`.

**The home page** gains two cards beside "What dewlab can do": dewmini, a blank notebook, and dewmini web, a blank web workspace. Adjacent cards inside the hero came out as a grid each. Inside an `md_in_html` wrapper their placeholders are one newline apart, not two, and `CARD_RUN_RE` wanted two. It now takes any whitespace, with a test case for cards inside a wrapper.

**Also.** `docs/WRITING_TUTORIALS.md` said all four widgets fail on a hosted page. `text_input` and `dropdown` work there; only `button` and `image_input` need the main thread, as `tests/e2e/test_phase0_golden_path.py` has shown since the round trip was built.

*Cost to change: small and local; the empty-state buttons can go if the seam is made visible enough on its own.*

---

**7.224 — dewmini: controls that broke under a redraw, a keyboard or a finger.** After 7.223's two-press delete, Josh asked to "see if there are other similar bugs". A hunt for the same kinds of fault found ten, each with an e2e test that fails on the old code.

**A running cell's output.** `createCellElement()` gave every cell a fresh, empty output element. A cell still running when the notebook was redrawn (a cell added or deleted, a tab left and come back to) wrote the rest of its output into an element hidden as empty. `executeCell()` then saved what the old element held, and the Run button came back reading Run rather than Stop. A running cell now keeps its output element through a redraw and gets its Stop state back. The engine's `getOutputEl` looks through every notebook, because a cell keeps running after its tab is left.

**Switching notebooks.** `openNotebook()` and `closeNotebook()` never repainted the Cells/File switch or the toolbar. New from the File view left File pressed over a notebook of cells, and New from a site tab left Run all hidden. Both now call `updateViewSwitch()`. They also call `flushFileEditor()` first, as `insertCellAt()` and Practice now do, so text typed in the File view in the last 400 ms is kept.

**Touch.** A rendered note's header (Edit, Delete, Duplicate and the rest) was quiet until hovered. The `(hover: none)` rule meant to undo that on a phone had the lower specificity and never applied, so the header was invisible and could not be tapped. The quiet rule now sits inside `(hover: hover)`. `assets/tutorial-style.css` had the same fault for a tutorial page's own notes and is fixed the same way, with a touch-screen test in `tests/e2e/test_custom_cells.py`.

**Keyboard.**
- Escape now closes a cell's ⋯ menu.
- When Escape closes an editor's suggestion list, it no longer also closes the open panel.
- Escape from inside a panel returns focus to that panel's toggle, as its close button does.
- A collapsed cell's summary is `role="button"` and opens on Space as well as Enter.
- A panel closed by its neighbour sets its own toggle's `aria-expanded` to false.

**Smaller.** Clear output also clears the File view's output. On a site tab, the Library's dataset button and "Load the example" say why they add no cell, rather than saving a cell nobody can see.

*Cost to change: small and local; each fix is a few lines with its own test.*

---

**7.225 — dewmini web: fresh editors per site, focus kept on the site list, and three smaller state fixes.** The same hunt, in dewmini web, found five faults, each with an e2e test that fails on the old code.

- **Switching sites.** `openSite()` loaded each site into the same three CodeMirror editors with `setValue()`, which is an undoable edit. So Ctrl+Z after a switch brought the previous site's code into the new one, and the debounced save kept it. Its change event also re-rendered the new site with the previous site's last-run script before `run()` replaced it. Each switch now builds fresh editors holding the site's code (`mountEditors()`). The bundle does not export `Transaction`, so an edit that skips undo history would have meant changing `vendor-src`. Load files still uses `setValue()`, so undoing a load still works.
- **Keyboard.** `renderList()` rebuilt the list and dropped the focused button, so choosing a site with Enter sent focus to `<body>`. Focus now returns to the current site's button.
- **Also.** An emptied Name box is refilled with the name the site kept. `openSite()` records the site it actually shows: with a stale saved id, Delete's `findIndex` returned −1 and `splice(-1, 1)` removed the last site instead of the one on screen.
- **Left for Josh.** A download gives separate `.html`, `.css` and `.js` files, and the HTML does not link the other two, so the downloaded page opens unstyled.

*Cost to change: local to `compose/dewminiweb.js`.*

---

**7.226 — Plot Twist is now the Dewey Track.** Josh: "for the series let's call it the Dewey Track and the tagline can involve python and math for those who want something different: learn by dewing".

- **The name.** John Dewey argued that people learn by doing. The tagline, "learn by dewing", is his idea with the site's name in it. Second-language readers may not catch the pun, so the course description says where it comes from in plain words.
- **The card:** "Python and maths for people who want something different. Learn by dewing — every page starts with a question from the world, and the maths and the code arrive because the question needs them."
- **The address.** The course id moved from `plot-twist` to `dewey-track`, so the course page is now `dewey-track.html`. `courses/redirects.yaml` sends `plot-twist.html` there. A course id is not a key for anyone's saved work (tutorial and cell ids are), and a reader's remembered course falls back to the page's first course when the id is no longer listed.
- **The plan** is now `planning/DEWEY_TRACK_PLAN.md`, and its name section says why. The topic groups show "Dewey Track:" in their names. Their keys stay `plot-twist-…`, since the generated topic game and editor are keyed on them and no reader sees them. One practice question that named the course now says "This course".
- **Earlier entries keep the old name.** They describe what was done under it. Only the plan's file path in them was updated.

*Cost to change: the title and card are text; changing the id again means another redirect line.*

---

**7.227 — dewmini and dewmini web become the Notebook and the Workspace, at new addresses.** Josh: "let's just change the name to notebook and workspace but let's also change the urls to reflect the change".

**The new names.** Readers now see the *dewlab Notebook* (`compose/notebook.html`) and the *dewlab Workspace* (`compose/workspace.html`). Pages say "dewlab Notebook" or "dewlab Workspace" where the brand helps, and "the Notebook" or "the Workspace" elsewhere. The offline copy is `download/notebook.zip`. A notebook still under its default name gives its page the title "dewlab Notebook", rather than "notebook — dewlab Notebook".

**What keeps the old name.** Everything saved work is keyed on stays as it was:
- the `dewmini:*` and `dewminiweb:*` localStorage keys;
- the `dewmini-fs` IndexedDB database, `/mnt/dewmini` and the `dewmini` OPFS folder;
- the `# dewmini export` first line that the `.py` import recognises, and `metadata.dewmini` in an `.ipynb` export.

Renaming any of these would strand work a student already has. The code keeps its own names too (`dewmini.js`, `dewminiweb.js`, the `dm-` and `dl-ws-` classes, `write_dewmini_bundle()`), as the internal name. ARCHITECTURE §4 and `docs/DEWMINI.md` say so.

**Old addresses.** `compose/dewmini.html` and `compose/dewminiweb.html` are now hand-written redirects. Each uses `location.replace()` to keep the query string and hash, with a meta refresh and a plain link for readers without JavaScript. They are not lines in `courses/redirects.yaml`, for two reasons: that mechanism only points at pages the build writes one by one (`compose/` is copied whole), and its stub drops the query and hash. `COMPOSE_REDIRECTS` in `build.py` keeps them out of the offline bundle, which has no bookmarks to honour. An e2e test (`test_old_compose_addresses.py`) and a build test cover them.

*Cost to change: the two page names now appear in links on the home, features and about pages, in a tutorial and in the docs, so a further rename means another pair of redirects. The internal names can change later only with a migration of the stored keys.*

---

**7.228 — The Dewey Track's contexts, characters and projects.** Josh answered the questions from the context audit on 25 September 2026.

- **Contexts: computing first.** Pixels, files, sensors, fonts and games come first, physics where the maths is physics, and real Irish data wherever it exists. A made-up everyday setting is the last choice. `DEWEY_TRACK_PLAN.md` §4 has the rule and the two warnings that go with it: explain science terms for second-language readers, and don't swap a fear of maths for a fear of physics.
- **Unit 1 builds a digit display, not a bill splitter.** Josh: "What about something like making a 7 pixel display or small 7 by 4 display for numbers". It comes in two stages: a seven-segment display, then a small pixel font. `//` and `%` find a pixel's row and column and a number's digits, and `2 ** 7` counts the segment patterns. `split_bill` leaves the toolkit.
- **Schlomo and Schlomi.** Schlomo comes from Josh's 2017 handouts, where he has a reasonable idea that doesn't work. The track gives Fix and Explain problems to him and Schlomi, so the reader tests somebody else's reasoning first. Neither is ever the joke, and neither is always right.
- **Choose your project.** Josh: "we don't have to pick one of these we can have a variety of projects and examples that the student can choose between". Where one idea has several good uses, the page offers two to four short projects. The first is Unit 9, where the derivative finds the bottom of a letter's curve (typographic overshoot), an edge in an image, a line of best fit, or a minimum by gradient descent.
- **Headings, cell ids and toolkit names may change.** Josh: "No one has used these yet so no need to worry about getting rid of old stuff". This holds until the track leaves beta. `waves` was thought to be in the MIT–PDP course, so it kept its headings and ids in the rewrite; in fact that course lists `sine-and-cosine-waves`, so `waves` is as free as the rest.
- **The letter is unsigned** until Josh has read it. A comment in the file says to sign it again.
- **The tagline** says "maths".

*Cost to change: each is text in the plan until the unit rewrites land. After that, the contexts are page content, and the toolkit names are in every later page that calls them.*

---

**7.229 — Feelings named rarely, with a route, across the site.** The revision plan (#306) and its style-guide issue (#310) name feelings rarely and always with a route to help. The Dewey Track's "Warmth that survives translation" said to name the feeling before the reader has to. Josh chose #310's rule for the whole site, the Dewey Track included, on 25 September 2026. The guide's bullet now reads "Name a feeling rarely, and always with a route", and the brief for the remaining Dewey Track units follows it. Units 1, 2, 3 and 9, written to the older bullet, get a light pass (tracked in an issue). The course letter keeps its opening until Josh has read it.

*Cost to change: one bullet in the guide; the pages written to it are the cost.*

---

**7.230 — The style guide keeps the reasons, and the principles of the 2026 revision are written into it.** The revision plan (#306) and its style-guide issue (#310). The guide had grown to 441 lines: a voice manual with a thin account of how people learn, three checklists, practice-page mechanics repeated in three files, and rules that pulled against each other.

**The principles.** The guide's "How learning happens here" section now holds the ones #306 decided, each with its own anchor:
- no verdicts: the site shows what code did, and never says a reader is right or wrong (`check()` goes in #314);
- mistakes are part of the process;
- discover, then name;
- predict in writing, then run;
- worked, then completed, then your own;
- nothing is taught once: earlier problems on every practice page, and a mixed set for every series;
- low floor, high ceiling;
- the reader chooses the world;
- a misconception gets a "closer look" page of its own, and is never flagged on an answer.

**Three contradictions, settled.**
- "A reader who stops after the opening paragraph should already have learned something" lost to "discover first". The opening now runs or shows something and asks about it; it does not define.
- "Invitational, not commanding" sat beside tasks that were all lists of commands. A task is now a question, a challenge or an invitation, and the steps inside it may be plain instructions. What is never an order is the thinking.
- The plain-language checks banned "earns its keep" while the guide said "earn" six times. Phrasal verbs are now named as the main barrier for a second-language reader, with idioms beside them, and the guide was read against its own list.

**Mechanics moved to `docs/WRITING_TUTORIALS.md`.** How to mark a new term (`#marking-a-term`), the shape of a cell id (`#cell-ids`), notes in the Reference panel, figures without `plt.show()`, the tools a cell can call without an import, and a practice page's title. The guide points there and keeps none of it.

**Anchors, not numbers.** Every part of the guide has a named anchor, and it is cited that way: `PEDAGOGICAL_STYLE_GUIDE.md#voice`. `dev/check_doc_links.py` now reads every hand-written file in the repository and fails on an anchor that is not in the guide (or in `WRITING_TUTORIALS.md`), and on a citation of the guide by section number. Numbers had already gone wrong: an entry here cited a section 11 that never existed, and the guide's own rationing note pointed at the wrong section. Run over the tree before this change, the checker finds 24 numbered citations: in CLAUDE.md, three skills, `WRITING_TUTORIALS.md`, `build.py`, `dev/curriculum_map.py`, a test, a glossary file, three planning documents and this log. All of them were changed, and one more it cannot see ("the style guide's new §3 subsection"). In this log, a sentence about what the guide said at the time keeps the old number in brackets ("then §4"); a sentence that sends a reader somewhere now names the anchor. CLAUDE.md's trap about section numbers is gone, since the check replaces it. The checker also reads CLAUDE.md and `.claude/skills/` now, which found the glossary skill still naming `order.yaml` files that 7.173 removed.

**Also removed:** "No emoji, unless Josh asks for them". It was about Josh, not about a reader.

*Cost to change: the guide is prose, and changing a principle means changing the pages written to it. Renaming an anchor means changing its citations, and the checker lists every one.*

---

**7.231 — The page templates, and the syntax for blocks and worlds.** The templates issue (#311), part of #306. `docs/templates/` holds six real pages, one of each shape: a tutorial, its practice page, a closer look, a mixed set, a series-end making task and a project brief. Together they make a small series, *Running totals*, taught with the rocky planets' widths from NASA and offered in three worlds (planets, the sea floor, pixel art). They are real pages rather than skeletons because an author copies a page, not a description of one. `tests/build/test_templates.py` builds them in a temporary repository on every run, and they are never published.

**The syntax, decided here so the platform issues build to it:**
- **A block is a fence after its cell**, with the same `key: value` header lines as a cell; `for:` names another cell instead. This is the rule the `hint` fence already follows, so there is one rule for every block.
- **`solution`** is Python, then optionally a `---` line and markdown notes. Two solutions make two tiers, and the comparison uses the first.
- **`inputs`** is one Python expression per line: a call, or a name the cell makes. A `#` comment labels a case. The author never writes an expected value.
- **The comparison** runs the solution in a copy of the page's namespace taken after the reader's cell, so both see the same data. A starter cell that defines the data is then enough for the solution to use it.
- **`predict`** has `type: choice`, `number` or `text`. An option's note is an indented line under it. It follows its cell in the source like every other block, and the page shows it above the cell.
- **Tests the reader writes** go in a cell marked `tests: <cell id>`, and an `inputs` block with `guess: yes` adds a column of the reader's own expectations.
- **`python challenge`** (and `html`, `css`, `js`) holds a closer's starter code, the same shape as `python exec` and `python toolkit-reference`.
- **Worlds** are a `worlds:` mapping in the frontmatter, the first being the page's own, and a `<div class="dl-world" data-world="…">` wrapper around each variant. A variant's cell id is the section's with `--<world>` added. The wrapper follows the `<div class="dl-hero">` convention the site's own pages already use, rather than a new fence that would have to nest cells inside it.

Until each platform issue lands (#312, #313, #315, #316), its syntax builds as plain text, and `docs/WRITING_TUTORIALS.md` says so beside each one.

Also: `planning/EXERCISES.md` now points to the templates and keeps only where the first problems came from and what is left. Its counts were stale (41 tutorials), and its frontmatter example still had `slug:`, which `check.py` rejects. The same stale line is gone from `WRITING_TUTORIALS.md`'s mixed-set example. `planning/outlines/README.md` no longer says a tutorial explains before it demonstrates.

*Cost to change: until #312 lands, only these six templates and the docs use the syntax. After it, every page written with blocks does.*

---

**7.232 — Solutions, inputs and the comparison view: the site shows two values and never a verdict.** The block-model issue (#312), part of #306, building the syntax 7.231 agreed.

**What a reader sees.** Under a cell, a table of the author's cases. A **Compare with a solution** button runs the cell as it stands, then fills in what the reader's code gives for each case beside what one solution gives. A row where the two differ gets the cell background and the word "different": nothing red, nothing green, no tick, no score. The solution itself is a closed fold. With `guess: yes`, a column of boxes comes first for the reader's own expectations, saved with the cell. A cell marked `tests: <cell id>` holds the reader's own tests; each statement runs on both sides, before the author's cases, which are then headed "Cases you may not have tried". A cell with inputs and no solution gets **Try these on your code** and one column.

**Copies, not the page.** `tutorial_tools.compare()` deep-copies the page namespace twice, once for each side, through one shared memo. The solution runs in its copy after the reader's cell has run, so it sees the same data (a starter cell that defines `giants` is enough), and whatever it defines replaces the reader's only there. Pressing the button changes nothing the reader has: their `total_of` is still theirs afterwards. Printed output is swallowed and new figures closed.

**When two values are "the same".** Close floats are (`0.1 + 0.2` beside `0.3` would be noise). `True` and `1` are not. Two separately defined classes with equal attributes are, since the reader's class and the solution's are never one class object. An error is an outcome, shown by name, and two of the same kind read as the same.

**The build runs every solution.** `check_solutions()` runs the page's Python cells in order in a separate Python, with the runtime's own `tutorial_tools`, then calls the same `compare()` for every solution. A solution that raises stops the build. An input the solution cannot name (a `NameError` or `SyntaxError` on the solution's side) stops it too, as a typo in the page. Other errors are outcomes. A cell that fails as written is fine, and each cell has 20 seconds under `SIGALRM` where the platform has it, so a deliberate endless loop does not hang the build. A missing package is a note, not a failure, because it says nothing about the solution. Pages without solutions start no process at all.

**Not done here.** `check()`, `expect:` and the `failed checks` signal stay until #314 retires them. The predict block is #313.

*Cost to change: `compare()` and `render_inputs()` are the two places the comparison's meaning lives; the saved record gains `guesses`, which an older page ignores.*

---

**7.233 — A Workspace download is a page that links its own CSS and JS.** 7.225 left this for Josh: a downloaded site opened unstyled, because the HTML pane holds only the body and the saved `.html` had no `<link>` or `<script src>`. Issue #350 offered three fixes: one self-contained file, three linked files, or a zip. The Workspace keeps three files, and the `.html` becomes a whole page that links the other two by name. Web Authoring teaches that a page is made of separate files joined by these two tags, so the download shows the reader how their own site fits together rather than hiding it inside one file. Load files strips the frame again, so a site can go out and come back unchanged. An e2e test (`test_a_downloaded_page_links_its_css_and_js_and_loads_back`) covers both directions.

*Cost to change: two small functions in `compose/dewminiweb.js`; switching to a single file means inlining the CSS and JS in `pageFile()`.*

---

**7.234 — The predict block: a guess written before the run, set beside the output, never marked.** The predict issue (#313), part of #306, building on 7.232.

**Why.** The pages ask for a prediction about 230 times, almost always as "What do you think…? Run the cell to check" in one breath, so the guess stays in the reader's head. The `question` fence met a wrong choice with "Not quite yet." A written guess turns the output into an answer to the reader's own question.

**What a reader sees.** Above the cell, the question, a way to answer (options, a number, or a few words) and how sure they are: *sure*, *a hunch* or *I'm not sure yet*. "Guess first, or just run it": skipping is always allowed. After the run, their guess and what the cell printed sit side by side. If they say the same thing, the page says so. If not, it says nothing about it, shows the note for the option they chose (the thinking that leads there, with a link to a closer look where one exists), and asks "Which line explains what you saw?" No option is ever labelled right or wrong.

**"I'm not sure yet"** opens the cell's first hint at once, whatever the Settings toggle says (the reader asked, and the first hint is the one that asks a question), and offers two ways on: make a guess now, or run it and see.

**Matching.** A number is compared with the last number the cell printed, within the block's `tolerance:` (0 by default), commas ignored. Anything else is compared with the whole output or its last line, spacing ignored and case kept, because `SEA` and `sea` are different answers. Anything else (9.70 beside 9.7 in a text guess) is the reader's to judge.

**Surprises.** A page with a prediction ends with a section listing the cells where a guess and the output differed, and the ones marked not sure, each linked back. Predictions save with the cell (the record's `prediction`), so the JSON export carries them, and the notebook export writes a guess as a markdown cell above its code.

**Signals.** Two new staged-hint signals, `unsure` and `guess differed`, written bare (`after: unsure`) or with a count, so an author can hang a hint on either moment in the syntax they already know.

**A block that follows its cell, drawn above it.** Every block follows its cell in the source (7.231); `render_cell()` draws the prediction above, since the guess comes first.

*Cost to change: the matching rules live in `guessMatches()`; the record gains `prediction`, which an older page ignores. #314 converts the `question` fences and retires `check()`.*

---

**7.235 — `check()` is retired, and a question shows the page's answer only when the reader asks, beside their own.** The verdict issue (#314), part of #306, building on 7.232 and 7.234.

**Why.** Mistakes are part of the process, and a site that answers every attempt with a pass or a "Not quite yet." feels like it is always checking. The comparison (7.232) and the predict block (7.234) already put the reader's result beside another one without a verdict. This entry takes the verdict out everywhere else.

**What went.** `check()`, its comparison and its markup (`_compare`, `_check_html`) are gone from `tutorial_tools.py`, with "That's right." and "Not quite yet." and the pass and fail styles. The `failed checks` hint signal is gone too: the build now rejects it as a term it does not know. `expect:` stays, as it was, an internal signal only: it stops further hints once it holds, and the reader never sees it.

**Where the calls went.** The `check()` calls on thirteen pages each became what the task was asking for. Where the task was a function to write (the matrices and graphics pages: `transpose`, `inverse`, `rotate_x`, `rotation_y` and others), a `solution` block and an `inputs` block. Where it was a guess about a value (`working-with-tables`), a predict block. Where the point was to see two numbers agree (`multiplying-grids`, `putting-the-derivative-to-work`, some practice pages), the cell prints both and the prose says what to look for. Tasks that asked the reader to print PASS or FAIL themselves (`cracking-equations`, its practice page, `expressions-come-alive`) now ask for both values side by side, and a question about what they show. A few sentences that told the reader their answer was right ("If the two columns match, your derivative is right.") now say what the match shows. Pages that teach testing, where a test prints PASS or FAIL about the reader's *code* (`building-reusable-tools`), keep it. The two database quizzes print what the checker found ("Found author_tbl and book_tbl, with every column this task names.") and hang their hints on `expect:` and a count of runs.

**Questions stay questions.** The issue asked for the multiple-choice questions to become predict blocks. They have not. A predict block belongs to a cell and is answered by its run, and most of the 95 questions (the warm-ups, the questions about an idea) have no cell whose output answers them. So the `question` fence keeps its place and takes the predict block's manners. Every option now has a note, the page's own included, naming the thinking that leads to it. Nothing happens when a reader picks an option. **Show the page's answer** marks the page's option, shows the note for the reader's, and says "You chose the same as the page." when they match. The reader can pick again, and the note follows. A fill-in-the-blank question's button is **Show the page's words**, and each gap gets the page's word beside it, leaving what the reader typed alone. `answer:` names the page's option; `correct:`, the older spelling, still builds. A question whose answer a run would show is a predict block's job, and new pages should use one.

**One rule for options and notes.** 7.231 wrote an option's note as an indented line under it. That misreads a long option that wraps, and one already had: the second line of the BASIC question on `many-languages-one-idea` was being cut off. Now an option is a bullet at the left margin, a bullet indented under it is its note, and an indented line that is not a bullet carries on the option or note above it. `options_and_notes()` applies this to predict blocks and questions alike, so an author learns it once.

**Two answers reworded.** A practice answer that opened "Not quite." now opens "Not on this list.", and "Nothing appears. That is correct" on `recipes-are-algorithms` now reads "Nothing appears, and nothing should." Prose that calls *code* wrong ("Each of these runs, and each one is wrong") stays, because it judges a program, not a reader.

**Ids.** No question id or cell id changed, so saved answers and saved code still match. The twelve pages whose cells changed have a new `version:`.

*Cost to change: the reveal lives in `revealAnswer()`; the note rule in `options_and_notes()`. Bringing back a verdict would mean restoring `check()` and the two strings, which this entry argues against.*

---

**7.236 — The world switcher: one task, a variant per world, chosen per page.** The world-switcher issue (#315), part of #306, building the syntax 7.231 agreed.

**What a reader sees.** A box under the page's title lists the worlds the page offers, each with its line from the frontmatter. The reader picks one, and each task shows that world's variant. The choice is kept in the browser for that page (`dewlab:world:<id>`) and can change at any time. Each variant's cells have their own ids, so a reader who tries the planets and then the sea floor keeps both.

**One number per task.** Every variant of a task counts from the same cell number, and the cell after it follows the longest variant, so "Cell 4" is the same cell whichever world is on show. The surprises list names a cell by the number on its pill for the same reason.

**What follows the world.** Running the cells above or below a cell, the surprises, the progress count and the notebook export take only the cells on show. A reader in the pixels world who runs everything above should not get an error from a planets cell they cannot see. The saved record carries the choice as `world`, so the JSON export says which world the work was in.

**A task in one world only** shows the page's own world's variant, then the first written. An author can add worlds one task at a time without a gap on the page.

**Without JavaScript** the chooser stays hidden and every variant shows under its world's name, so nothing is lost. A printed page has the chosen world, with its name. A downloaded page keeps every variant and the chooser, which works offline.

**The build holds the contract.** A cell in a variant must end in `--<world>`; a block (solution, inputs, predict, hint) and a cell of tests must be in the same world as their cell, since they show and hide with it. `world_spans()` reads the source with fences blanked, so a `</div>` in an HTML example does not close a variant. `check_solutions()` runs a page once per world, with the cells a reader in that world would run, so a solution that leans on another world's names fails at build time.

**Names from keys.** A world's name is its key with a capital and spaces (`sea-floor` is "Sea floor"). That keeps the agreed frontmatter, one line per world, and a name worth more than that can come later without changing a page.

*Cost to change: the grouping and fallback live in `applyWorld()`; the build's rules in `world_spans()` and `extract_blocks()`. A world's name that differs from its key would need a richer `worlds:` form, read by `page_worlds()`.*

---

**7.237 — A closer's challenge opens in the Notebook or the Workspace, ready to work on.** The challenge-links issue (#316), part of #306, building the syntax 7.231 agreed.

**The block.** A ```` ```python challenge ```` fence is starter code for the Notebook; ```` ```html challenge ````, ```` ```css challenge ```` and ```` ```js challenge ```` fences side by side are one site for the Workspace. The page shows the starter read-only, since it is not a cell, with one button: **Open it in the Notebook**, or **in the Workspace**.

**The link carries the starter.** The button is an ordinary link to `compose/notebook.html` or `compose/workspace.html`, with the starter in its address (`#challenge=` and a JSON object). Nothing has to pass between two open pages, the tutorial can be closed, and the link works without the tutorial's JavaScript. A starter is a few lines, so the address stays short.

**Never over the reader's work.** The Notebook opens it as a new tab, and the Workspace as a new site, named after the page's id. A tab of that name already there makes this one `running-totals 2`. The same starter opened twice goes back to the tab it made, if that tab still holds it unchanged, so a reader who clicks twice does not get two copies. Both clear the address at once, so a reload does not open it again, and both listen for the address changing, since following the link in a tab that already shows the Notebook does not reload the page.

**Offline.** A downloaded page has no Notebook beside it. There the runtime hides the link and shows **Save it as a file**, which saves `running-totals.py`, or one `running-totals.html` with the CSS and JavaScript inside it, since a single file is what opens from a student's disk.

*Cost to change: the address format is read in three places, `render_challenge()` writing it and `openChallengeFromAddress()` and `takeChallengeFromAddress()` reading it; a change to one is a change to all three.*

---

**7.238 — What a student reads first: choosing a course, studying here, and reading helpers.** The student-docs issue (#317), part of #306.

**Two site pages, not only a guide on GitHub.** `studying.html` ("Studying here") says what each course is for and how the integrated course and the Dewey Track differ, and says plainly that in a class the teacher decides. It then gives the habits the revision is built on: guess before you run, come back after a gap, try the "from earlier" problems, and, when stuck, the hint, "I'm not sure yet", an earlier page, the Reference, then a person, in that order. `reading-helpers.html` covers dewlab's own Appearance settings and the browser's translation, read-aloud and Edge's Immersive Reader. Both are site pages (`pages/`), linked from the home page and About, because a student meets the site on 2 October, not the repository. `FOR_STUDENTS.md` and the FAQ link to them rather than repeating them.

**Translation leaves code alone.** The reading-helpers page says translation leaves the code, a cell's output and the maths as they are. Nothing made that true, so the runtime now marks them `translate="no"` (`keepCodeFromTranslation()`). A translated `print` would not run.

**Directions to controls, checked against the page.** The page has three corner panels (Notes, Python, Settings) and a feedback circle. Hints and the contents-page badge are switched in Settings → Behavior, and Export a copy and Start again are in Notes, Restart Python in Python. The FAQ, the guide, the README and three tutorials said otherwise in places, and now agree. The eight "Double-click this cell to write your thoughts" lines on the OOP pages pointed at nothing; they now point at Your notes. "Each page starts fresh" is true except for the Dewey Track's toolkit, and now says so.

**Course cards.** Each card says who the course is for, what you do in it, which worlds it offers, and ends as an invitation; no time estimates. Descriptions no longer repeat their cards, and Database Methods and Web Authoring have one. The worlds named are the ones #306 plans; the content issues bring them to the pages.

*Cost to change: the two pages are `pages/studying.md` and `pages/reading-helpers.md`, listed in `SITE_PAGES`; the course text is in `courses/*.yaml`.*

---

**7.239 — Programming Foundations, part 2: the lists page splits, a project page arrives, and the series ends by making something.** The content issue (#319), part of #306, applying the page rules of #318.

**The split keeps the old id for the first half.** "Lists and looping over them" stays `lists-and-sequences`, so the twenty-odd links to it from other pages keep working, and the new second half is `comprehensions-and-grids`. Links that meant comprehensions, grids or the dot product now point at the new page. The slicing picture stays with slicing, drawn from the page's own `letters` list, and aliasing has a section of its own with a predict block. The dot product and sequences-as-functions went to the second page, because they need comprehensions and a function passed as a value.

**Binary and hexadecimal live in one place.** They moved from `storing-and-computing` to `how-we-got-here`, where the history already explained why they exist. MIT-1.4 is now claimed there, and the glossary entries moved with the teaching. `len()`, `.upper()`, `ord()` and `chr()` stay early, in `storing-and-computing`, and `.split()` is introduced where a list of words first appears.

**A project page, with no solutions.** "A program of your own" follows the dictionaries page: three starting points with a low floor and room to grow, a plan, a Release-1 checklist and reflection questions. It asks nothing a solution could answer, so it has none, and no practice page.

**Tests the reader writes start at `building-reusable-tools`.** Every task there and after has a `tests:` cell beside it, as 7.232's stages said. `assert` and `raise` are taught on that page, and printing an error message is shown failing: the caller gets `None` and the error surfaces a line later.

**What the history page keeps of other languages' ideas.** `map`, `lambda` and `reduce` are cut; functional style is shown with a function handed to another function, which the reader has already met in `sorted(key=)`. One small `class` stays, to be read and not written, because recognising object-oriented code is part of PDP-LO3 and the OOP course builds classes properly.

*Cost to change: a page's id is part of the key its saved work lives under (7.12); after 2 October, renaming `comprehensions-and-grids` or `a-program-of-your-own` loses that work.*

---

**7.240 — From cells to a program: `input()` is written in advance on the page, and the team project is set in the worlds.** The content issue (#320), part of #306.

**A cell cannot wait for typing, so the page says so and writes the typing down.** `input()` needs somebody at a keyboard, and a cell running in Pyodide has no way to pause for one; the existing pages commented `input()` lines out. The new page, "From cells to a program", keeps the programs whole instead. Each keeps its answers in a list, `typed`, and a four-line `ask()` takes the next one and prints it beside its prompt, so the output reads like a session at a keyboard. The page says in the same breath that on a computer the whole of `ask` becomes `ask = input`. A reader sees `while True`, `break` and a validation loop run from start to end, and the typed list doubles as a test: change it, and the program meets different answers. A second point follows: the deciding is kept apart from the asking (`first_valid(answers, low, high)`), which is what lets a `tests:` cell check it.

**`main()` is called plainly on the page.** The runtime names the page namespace `__dewlab__` (7.97), so `if __name__ == "__main__":` in a cell would skip `main()` and print nothing. The cell calls `main()`, and the guard is shown as what goes at the end of a file, with the reason.

**The team project brief asks for a game or tool in one of the worlds,** with a worked Release 1 (a two-room text adventure), and drops ideas that need what the course never teaches: renaming files, a dataset with plots. What is handed in, and when, is left to the teacher; the page keeps the process advice and the reflection questions. Its interface agreement and review checklist point at the templates on the new page.

**Reflections go in Your notes.** `critique-and-reflection` points at "A program of your own" as the work to look back on, and its answers leave the cells of Python comments for the Notes panel, since the block model has no text block yet.

*Cost to change: `from-cells-to-a-program` is a new id; renaming it after 2 October loses the work saved under it (7.12).*

---

**7.241 — A page can include shared prose, and Computational Methods opens with a trailer.** The first-steps-cm issue (#321), part of #306.

**Markdown includes.** `{{include: setup/x.py}}` already pasted shared code into a cell. A line holding only `{{include: setup/x.md}}` now pastes shared markdown into a page, before the page is read, so an included heading gets its anchor and an included cell is the page's own (`expand_prose_includes()`). The issue asked for `first-steps` and `first-steps-cm` to share their section on what to do when a cell fails, as an include rather than a copy, and two copies had already drifted: one said the report circle sits "beside a cell's hint", the other "on a cell's bar". The shared file is `setup/when-a-cell-does-not-do-what-you-expect.md`. An include that shares its line with other words fails the build with a clear message, rather than leaving `{{include: …}}` on the page; includes do not nest. The authoring editor shows the include line as written, not what it pulls in.

**The trailer.** `first-steps-cm` opens by running something the course builds: 100,000 darts estimating π, in plain Python, so it runs on the first click with no package to load. Of the three the issue offered, a spinning wireframe or a matrix-flipped photo would need matplotlib or an image on the first click, and the first run of a page should not be its slowest. The page then says what the course does and which worlds it offers. Its copy of `first-steps`' arithmetic is cut, and a line points Computational Methods readers, who never see `first-steps`, to its operators section, since the next pages use `%`.

*Cost to change: two pages read the shared section; a change to it is a change to both, which is the point.*

---

**7.242 — The first half of the OOP course grows one class, in the reader's world, and the debugging page moves up.** The OOP rebuild, part 1 (#322), part of #306.

**Four worlds, one class that grows.** `BankAccount`, pasted into cell after cell, is gone from `objects-and-classes`, `the-moves-you-already-know`, `the-tools-around-your-code`, `keeping-details-inside-an-object` and `one-class-many-methods`. Each page offers a game world, an ocean expedition, a solar system, or the reader's own, and teaches in one of them, in turn: game, solar system, game, ocean, solar system. Three pages end with a milestone that is the next version of one class in the reader's world: `__init__` and `__str__` first; then one rule kept by a method, with the field it protects made private and a getter; then a method that answers a question, used by another method, and a class attribute. The versions live once, in `setup/oop/<world>-<n>.py`, and each milestone's solution and the next milestone's starter include the same file, so the chain cannot drift. Reader code is not carried from page to page: toolkit cells were built for functions and have not been tried with classes or worlds, so the your-own world asks the reader to copy their class from the page before.

**Each version keeps its rules, and leaves one door open.** From the encapsulation page on, no class goes back to public fields and an unguarded method. But each world's class keeps one rule that another method can go around: `heal(-50)` in the game, `rise(-500)` in the ocean, `burn(-50)` for the probe. The milestone notes ask the reader about it. That gap is left on purpose, for part 2 (#323), where the testing page needs a real bug to find.

**The opening is the problem a class solves.** `objects-and-classes` starts from a list of dictionaries in which a misspelt key quietly makes a new field and a rule is broken elsewhere. The old "five hundred variable names" argument ignored that readers already know dictionaries. Class attributes moved to `one-class-many-methods`, where a value shared by every planet has a reason to exist.

**`the-moves-you-already-know` is a labelling page.** A fill-in-the-blank question labels each line of a method as storing, sequence, selection or iteration. Storing is now taught, not assumed; tuples are gone. The page's new point is where a value is stored inside a class: on `self`, where it lasts between calls, or in a plain name, where it vanishes when the method ends. A cell that forgets `self.` and prints 0 shows it.

**`the-tools-around-your-code` teaches debugging, and comes third.** It had two cells and no task. It now reads tracebacks through two method calls, where a class's bugs live: first a slip on the bottom line, then a caller that passes the wrong value, so the error shows one call further in than the mistake. Then it prints what a method holds, for bugs that raise nothing. It moves from fifth to third, so the reader has these tools before the milestones start to grow; FOOP-LO5 needs nothing before it. Merging it with the testing page, the issue's other option, would have put debugging after five pages of classes.

**`Polynomial` moves to a project page of its own.** In `one-class-many-methods` it was the one class outside banking, and the one most likely to make a reader anxious about the mathematics rather than the code; a `Planet` with the minutes light takes to reach it teaches the same idea. But a polynomial class, built a method at a time, makes a good project for a class, so it has its own page, `a-polynomial-class`, straight after, and the page before says a reader may go on to inheritance instead. It follows a thrown ball, and its stages are `evaluate`, `degree` (where the trailing zero in `[1, 2, 0]` is the trap), an `__init__` that keeps two rules (no zero at the top; a copy of the caller's list, since the caller's list is another name for the same one), a `__str__` that writes `-5x^2 + 20x + 1.5`, `add`, which returns a new polynomial that keeps the same rules, and, for readers who have met the power rule, `derivative`, which finds that the ball is highest at 2 seconds. The stages include the class as it stands from `setup/polynomial/`, so each starter is the stage before's answer. It has no worlds: it is the one page in the course set in mathematics, by design.

*Cost to change: `the-tools-around-your-code` now sits third in `courses/fundamentals-of-oop.yaml`, `topic-groups.yaml` and the mixed page's list; moving it again means all three. The `setup/oop/` files are read by two pages each.*

---

**7.243 — A video library in `planning/video-library/`: 895 hand-picked YouTube and Nebula videos, keyed to the tutorials they would sit beside.** Josh supplied a list of 119 channels and asked for something filterable to reach for when building pages, and to browse for ideas: coding projects, algorithms, simulations.

**Three CSV files, not a page on the site.** Nothing links to a video yet, and the list is for people writing tutorials, which is what 7.192 kept `planning/` for. A spreadsheet filters by tutorial slug or topic with no tooling. `picks.csv` is the judgement; `channels.csv` says which channels were read and why the rest were not; `all-videos.csv` keeps every title from the 58 reviewed channels, so a search for a technique does not depend on what was picked.

**Picked from titles, not from watching.** Every title on the reviewed channels was read, and each pick names the tutorial folders it fits, checked against `tutorials/`. The README says plainly that a video must be watched before it goes on a page, and that its `note` column is written for authors and is never the sentence a student reads.

**Nebula by channel and by title.** Twenty channels appear in Nebula's public channel list; for six of them, videos were matched to YouTube titles one to one, which gave 90 Nebula links among the picks.

*Cost to change: low. Plain data with no reader in `build.py` or the tests; a row can be added or removed by hand. If a page ever embeds or lists videos, it should read `picks.csv` rather than copy from it.*

---

**7.244 — The Dewey Track: exoplanet data kept with its acknowledgment; length is not a limit; the judging-words sweep.** Josh, 26 September 2026: "I believe acknowledgement is enough if it is public data since we are using it for educational purposes... sure lets sweep for judging words and no we don't need to trim, so long as its good, i think the length is less of an issue".

- **`data/exoplanets.csv`** stays. The NASA Exoplanet Archive states no licence and asks for an acknowledgment, which `data/exoplanets.yaml` carries; the site uses the data for teaching.
- **Length.** The 1,800–2,600-word range the unit rewrites were briefed to is dropped. A page is as long as it needs to be to read well. Several Dewey Track tutorials run to 3,000–3,600 words and stay that way.
- **The sweep.** Every Dewey Track page is swept for *right*, *wrong*, *correct*, *good*, *bad* and *mistake* about the reader's work, and for feelings named without a route (7.229), to match the style guide's no-verdicts principle. Geometry (*right angle*), quoted UI labels and error text are left alone.

*Cost to change: none for the data and length; the sweep is page prose.*

---

**7.245 — The second half of the OOP course keeps growing the reader's class, to a world someone else can play.** The OOP rebuild, part 2 (#323), part of #306.

**One project from the first page to the last.** The milestones of 7.242 go on, one version a page, each in `setup/oop/<world>-<n>.py`: a child class with one sentence that says why (`Healer`, `Bathyscaphe`, `Lander`); a container that holds the reader's objects (`Room`, `Expedition`, `Mission`); five tests, and the open door from 7.242 closed; docstrings, with examples doctest can run; a `run_choice` front end. A new page at the end, `your-world-playable`, runs each world's eighth version with its five tests passing and a menu to play from, then asks the reader to add one rule the way the series did: test first, then the rule, the docstring, the command. Where a page's task changes a class, its starter includes the version before and its solution the version after; where it adds a new class, a cell of its own holds the classes so far, so the task cell shows only what is new.

**A new design page, `from-a-description-to-classes`, before inheritance.** A paragraph about the expedition becomes CRC cards, then a skeleton that runs. Three designs are shown and weighed, not ranked; the reader does the same with a paragraph about their own world. The cave paragraph gives heroes and monsters that share most of what they know, which is the next page's question.

**Inheritance shows the class-attribute trap.** Part 1's classes read their limits as `Character.max_health`, `Submarine.hull_limit` and `Probe.tank_size`. A child with its own limit is then ignored: a troll with a limit of 20 heals *down* to 10. The page predicts it, then reads the limit through `self`, and every world's fourth version makes the same change. The contrast the issue asked to keep is a troll that goes through `super()`, because the parent's rules still hold, and a phoenix that cannot, because the parent's rule is the one it breaks.

**Composition adds four cases that are not clear-cut:** a dictionary or a class; a child class or a flag (Pluto, which changed kind in 2006, against a new kind being named); `Square(Rectangle)`, where doubling the width quadruples the area; and an astronaut who is two things at once. None is given a single answer.

**Testing is a hunt.** Five versions of the submarine, four with one bug each, and a `check` the reader grows until one is left standing; three of the bugs sit at a boundary. Then a ten-line runner over `globals()`, the same idea as pytest; a test written before the fix, for the open door; and a test that is wrong, because `0.1` is stored nearly. The old `expect: callable(...)`, which only checked that a function existed, is gone. The reader's own tests go in a `tests:` cell, so the comparison runs them against their class and against the next version.

**The second front end is a menu, not a button.** The issue asked for one built from `text_input` and `button`. `button()` raises on a tutorial page: the page runs Python in a Worker (7.77), and a click has no way to call Python there. `text_input()` and `dropdown()` do work, since their values reach the Worker as messages, so the second front end is a `dropdown` of commands, and the cell's own Run is the Go button. The page says so, and turns the limit into a design point: a menu makes a mistyped command impossible. `docs/WRITING_TUTORIALS.md` listed `button()` among what any cell can call; it now says which widgets need a downloaded copy. Making `button()` work in the Worker is runtime work, left for its own issue.

**The mixed set** covers every page of the series in the worlds, with one problem that adds a method to the reader's own container.

*Cost to change: the `setup/oop/` files are a chain, each read by the page that makes it and the page that builds on it, and the last by `your-world-playable` and the mixed set; a change to one version belongs in every later one too. `from-a-description-to-classes` and `your-world-playable` are new ids.*

---

**7.246 — 99 videos from the video library added to "Where to read more" on 89 tutorials and 10 practice pages.** Josh asked for a video or two at the bottom of the pages, and then narrowed it: only videos from the channels on the list behind `planning/video-library/` (7.243).

**One video per page, two where each does a different job.** Most pages got one: the video that sits closest to what the page teaches, at a length a reader might watch the same evening. A second goes in only when it adds something the first does not, such as the 100 prisoners puzzle and its solution, or a short lesson next to a long story. Pages that already had a read-more section keep everything in it; the video goes at the end, before any line that points to the practice page. Pages without one get a `## Where to read more` heading, in the style guide's sentence case.

**Practice pages get a problem, not a repeat.** A practice page gets a video only when it poses something more to try, such as a puzzle, a coupon-collector run to simulate, or a sine pattern to check, and the entry asks the reader to try before watching. The other practice pages are unchanged, as are all the web, SQL and OOP pages the channel list has nothing for.

**Checked before writing, not watched.** Each video's title, date, description and chapter list were read, and captions where they could be fetched. That caught three picks that were wrong for their page (a "perspective" video about physics, a card puzzle that was not the Wason task, and a "gibberish generator" about fake handwriting). One strong fit, a Tantacrul interface critique for `critique-and-reflection`, was left out because its language could not be checked. Each entry is cited in the form the pages already use, and gives the video's length so a reader knows what they are starting.

*Cost to change: low. Each entry is one paragraph at the end of a page, with no cell or id involved, so it can be removed or replaced by hand. A dead link is the likely failure over time, since the build does not check outside links.*

---

**7.247 — A SQL cell's result table leaves out pandas' row numbers.** `_run_sql_cell()` builds a DataFrame from the cursor and rendered it through `_table_html()`, which called `to_html()` with the index shown, so every `sql exec` result had an unlabelled 0, 1, 2 … column on its left. On `changing-what-is-in-it` that column sat beside `dinosaur_id` values 1, 2, 3, 4, 6, where the prose asks the reader to look at the ids and see the gap a `DELETE` left: two columns of numbers, one with a gap and one without, and nothing to say which is the table's.

`_table_html()` gained `index=True`, and `_run_sql_cell()` passes `False`. A SQL result has no index of its own; the numbers were pandas', added on the way to HTML. A Python cell that shows a DataFrame keeps them, since the pandas pages teach the index and a reader there needs to see it. `run_query()`, the public one-statement version called from a Python cell, still shows the index; no tutorial calls it, and whether it should follow the SQL cell is left until one does.

*Cost to change: trivial. One argument in one call, and one test in `TestRunSqlCell`.*

---

**7.248 — The first three pages of "A table of your own" get pictures, bold key terms, predictions, and a `DROP TABLE IF EXISTS` that makes their boxes safe to run twice.** Josh, 26 September 2026: "see if maybe that first introduction to tables and the next couple pages couldn't use a few more graphics and maybe an edit? I also don't see some of the bold or terminology focus things that we had discussed previously".

**The bold terms had never reached this course.** 7.207 brought bold-italic key terms to six graphics pages and left the rest for later; the glossary file for `a-table-is-a-list-of-rows` already noted that the whole series had no marked terms at all. The three pages now mark theirs as 7.207 did (`***term***`), so the Reference panel links back to where each is introduced. Page one gains the terms it used without defining: *database*, *query* (which every later page in the course leans on), *cell*, *record*, *attribute*, *header*, *comment*, *data type* and *primary key*. Page two gains *condition* and the six comparison operators. *Cell* is the table's own word here, which is why these pages call the code editor a *box* throughout.

**Six pictures, drawn from the pages' own SQL.** `dev/graphics/database_methods.py` gains a table drawer beside its ERDs. Every value in a picture comes from running the page's cell in sqlite at generation time, the same rule the ERDs follow, so a picture cannot show a row the box does not build. Page one: the parts of a table, on a shopping list (Josh's own example from his opening paragraph), and what `CREATE TABLE`, `INSERT` and `SELECT` each leave behind. Page two: `SELECT` picking columns and `WHERE` picking rows, with the result as the cells in both; and `WHERE` then `ORDER BY` as two steps. Page three: `UPDATE` and `DELETE`, each with and without its `WHERE`, side by side. Each picture has labels as well as tints, so colour is never the only signal.

**Three things the old prose said that the runtime does not do.** Running a box a second time never rebuilt the table: it failed with `table dinosaur_tbl already exists`, because a page's database lives for as long as the page is open. The per-cell Reset (↺) clears output and never touched the table. And page three's "run it without the `WHERE` and watch every length become 2.5" could not show that, since the box's own `SELECT` kept its `WHERE` too. The fix is `DROP TABLE IF EXISTS` at the top of each dinosaur box, the idiom `sets-in-databases` and `many-languages-one-idea` already use, taught on page one with an experiment that fails on purpose when it is commented out. The reader's own-table steps start with it too. Page three now asks the reader to remove both `WHERE`s.

**Cell ids unchanged,** so no saved work moves. `version:` is bumped on all three, because a cell's starter code changed.

**Left alone:** the tail of page two's recap, where the video pull request (7.246) adds a "Where to read more". The pandas row numbers that sat beside every SQL result, next to `dinosaur_id`, are gone since 7.247, which page three's look at the ids 1, 2, 3, 4 and 6 relies on.

*Cost to change: low. Prose and six generated SVGs; a picture changes by editing its function and re-running the generator. Removing `DROP TABLE IF EXISTS` would need the "run it again" sentences on all three pages changed back.*

---

**7.249 — The rest of Database Methods gets `DROP TABLE IF EXISTS` wherever a page asks for a create box to run again.** A follow-up to 7.248, which fixed the first three pages of "A table of your own".

**The same bug, in more places than the first three pages.** A page's sqlite database lasts for as long as the page is open, so a `CREATE TABLE` that has already run stops the next run with `table X already exists`. Neither per-cell button changes that. Reset (↺) clears the output, and Clear (↻) puts back the starter code; neither touches the database. A sweep of every page in `courses/database-methods.yaml` found four more pages that ask for a create box to run a second time:

- `a-second-table-and-a-join`: both dinosaur boxes, and the reader's own box, which the page asks them to grow a second table in and run again. Each worked box drops its own table. The prose tells the reader to drop their second table before their first. No foreign key is declared in the worked boxes, so their order does not matter.
- `joining-two-real-tables`: "Change `'USA'` to `'United States'` in the `INSERT` above, then re-run both cells" could never work.
- `a-college-timetable`: "Run that box again to rebuild the whole database with your row included" could never work either. Five drops, in the reverse of the `CREATE` order, `session_tbl` first, because the box declares its foreign keys.
- Both quizzes: the workspace says "Run this box after every change", and the reader's own `CREATE TABLE` from Task 1 failed on every run after the first, so Task 2's table was never built. The workspace starter now carries the drop lines, with the tables that point into others first, so a reader never meets the error. The worked solutions start with the same lines.

**Pre-filled in the quizzes, taught elsewhere.** A quiz assesses the tables, not the drop idiom, and a reader stuck on `already exists` halfway through a quiz is stuck on the wrong thing. So the quizzes put the lines in the starter code. The worked pages explain them where they appear.

**Order was run, not reasoned.** Each worked solution was run twice with `PRAGMA foreign_keys = ON`, the setting under which a parent table cannot be dropped while a child table still points into it.

**`working-with-tables`** said "Reset brings back the code the page started with". That is Clear. The sentence now names both buttons, with their symbols.

**Left alone:** `sql-practice` and `a-form-that-writes-a-row` each have a create box that fails on a second run, but neither page asks for one. `version:` is bumped on every page whose cell code changed. Cell ids are unchanged, so no saved work moves. A reader's saved copy of an old box keeps its old code, without the drop lines.

*Cost to change: low. Each drop line is one line of starter code. Removing one would need the "run it again" sentence on its page changed back.*

---

**7.250 — Datasets are fetched live, with a saved copy as the backup, and every copy says where it came from and when.** The datasets issue (#324), part of #306. Josh's decision in the issue: live from the source, with a dated snapshot in `data/` as the backup.

**One loader, three outcomes.** `load_csv` and `load_text` fetch a `live: true` dataset from its source, shape it with its recipe into the snapshot's own columns (`tutorial_tools.shape_live()`), and use the snapshot on any failure: no answer in 10 seconds, a page offline, or a source whose columns no longer fit. A dataset that is not live comes from its snapshot. Either way one quiet line under the cell says which copy it got and when that copy was saved. The line is HTML, not printed output, so a prediction or a comparison never reads its date as the cell's answer. The same recipe makes the snapshot (`dev/datasets.py --refresh`), so on the day a snapshot is saved the live copy and the saved one are the same table.

**Live only where a browser may read the source.** A page can only fetch from a website that says other pages may (`Access-Control-Allow-Origin`). Our World in Data, the Paleobiology Database, the Marine Institute and NASA POWER do; the NASA Exoplanet Archive, JPL Horizons and Project Gutenberg do not, so those datasets are snapshots only, and their yaml says why. CO₂ is snapshot only by choice: its source file is 14 MB, too much to fetch on every run.

**Provenance is checked, not hoped for.** Every file in `data/`, declared by a page or not, needs a yaml with its source, url, licence, snapshot date, what was trimmed, and a description; the build fails without them. Tracing the old files found two gaps: `the-montessori-method.txt` is Project Gutenberg #39863 with its header removed, and `democracy-and-education.txt` is the Internet Archive's OCR of a Google scan; neither yaml said so. The Paleobiology Database's own service states CC0, not the CC BY this work assumed until it asked.

**The page's numbers name their copy.** `{{snapshot: life-expectancy}}` in prose becomes the date in the yaml, so a refresh cannot leave a page naming the old date. `life-expectancy.csv` was refreshed to Our World in Data's current release (1950 to 2023, and renamed and revised countries), and every page that quotes it was run against both copies and corrected: 17 cells' output changed with the data, and the answers in folds with them. Two pages changed more than a number: Nigeria's spread is no longer the widest of three, and the derivative page fits its line to 1990–2019, the thirty years before the pandemic, with 2020 and 2021 left as the next question. `kinds-of-data-and-honest-charts` moved to 2023, and its histogram's last edge to 95: `range(50, 90, 5)` had been quietly leaving out every place above 85.

**A page carries its datasets.** A page's download now holds the datasets it declares, gzipped, so it works offline. A page must declare every file from `data/` it loads, or the build fails. The four Database Methods pages load an Our World in Data address, as they teach; `data/` keeps a copy of that exact file (`address: true`), which stands in when the address cannot be reached.

**New datasets for the worlds.** Dinosaur genera and finds (Paleobiology Database, older than 66 million years, so early birds such as Archaeopteryx are in: a sets question of its own), tides at Dublin Port for March 2026 (Marine Institute), Dublin's daily weather for 2023–2025 (NASA POWER), sunrise and sunset in four places through 2026 (NASA/JPL Horizons, `dev/daylight.py`), and chapters and character names in six novels (`dev/book_counts.py`). Planetary data is `planet-orbits.csv`, already here. A transit network, a star catalogue and handwritten digits wait for the issues that need them.

*Cost to change: moderate. The note's wording and the recipe steps are small; the pages that quote life expectancy name their copy by token, so a refresh moves their dates for free, and their numbers still need a run each time.*

---

**7.251 — A weekly check that every linked video is still there.** Josh, after 7.246 put 99 videos on the pages: "lets do a link check". `dev/check_video_links.py` asks YouTube's oEmbed endpoint about every video linked from a tutorial, a practice page (frozen releases included) or a site page, and `.github/workflows/video-links.yml` runs it every Monday, keeping one `video-link` issue open while anything has gone.

**On a schedule, not in the tests.** A video disappears on YouTube's timetable, not on a commit's, so checking in `tests.yml` would turn an unrelated pull request red the week a video went, and a YouTube outage would turn every pull request red. A weekly issue reaches the same people without blocking anyone. For the same reason the check never counts a timeout or a 5xx as a dead link: those are retried, and if more than a quarter of the checks fail that way the run changes no issue at all.

**Private is listed, not assumed.** oEmbed answers 401 both for a private video and for one whose creator turned embedding off, and the second still plays for a reader. So 401 is reported under its own heading for a person to open, and a video found to play goes in `EMBEDDING_OFF` in the script, with a date, so it does not reopen the issue every week. The first one there is the Random Noise Lights Out video on `solving-systems`.

**The first run found two links that never worked.** Computerphile entries on `first-steps` and `three-ways-to-make-change` pointed at IDs YouTube has no record of, most likely written wrong when the pages were drafted. Both entries are removed rather than replaced: the channel is not on the list behind `planning/video-library/`, and both pages keep other reading.

*Cost to change: low. One script, one workflow, one issue label. Removing the workflow stops the checks and leaves the script runnable by hand.*

---

**7.252 — 39 more videos from the list, on 36 pages that had none.** Josh, having watched every channel on the list: "we can certainly fill in some gaps". The same rules as 7.246, applied to the pages it left empty, searching every title in `planning/video-library/all-videos.csv` rather than only the picks.

Two kinds of fit. Some pages have a twin in another course (`repeating-yourself` and `doing-it-again`, `making-decisions` and `choosing-a-path`, `sorting-a-hand-of-cards` and `putting-things-in-order`), and take the same video, since a reader only meets one of the pair. The rest get a video aimed at one section: Cramer's rule for "One formula for every pair", gradient descent and curve fitting for the two derivative projects, point-to-line distance for "Did the ball hit the player?", Russell's paradox for "Where the picture stops helping". The Tantacrul critique 7.246 left out now goes on `critique-and-reflection`.

Most of the HTML, CSS, SQL and OOP pages still have nothing: no channel on the list teaches those subjects. Filling them needs channels added to the list first.

*Cost to change: low, as for 7.246.*

---

**7.253 — A fifth Simulation tutorial: a ball stepped forward in time.** Josh, after the video library: "I like the stepping forward in time", with MinuteLabs and Sebastian Lague as the models rather than Primer. `stepping-forward-in-time` drops a ball from Liberty Hall with Euler's method, checks it against the physics formula, shrinks the time step, and then makes the ball bounce. It goes last in the Simulation series, after the queue, which already moves in steps of time.

**Nothing on the page is random.** The four pages before it all use chance. This one shows the other half of simulation, a rule run forward from where the last step finished, and its practice page asks whether a seed would change anything (it would not).

**The error is shown, not hidden.** The page keeps the order of the two lines that most readers write first (move the ball, then change its velocity), because that order makes the error easy to see: the ball does not move in its first second, lands late by about one time step, and a perfectly bouncy ball climbs from 60 metres to 80. The practice page swaps the two lines, finds the ball losing height instead, and says that most games choose that order. The tutorial could have taught the better order from the start; it would then have had no error worth looking at.

**Outcomes.** CMPS-LO3 and LO13 as the main ones; LO7, because the formula and the loop are two ways to get answers from one model; LO11 touched, since checking a simulation against a known answer is validation, but not against the real world, which the air-resistance challenge only points at. The comparison with the darts page (ten times the steps for one more decimal place, against a hundred times the darts) is deliberate: it is the first time the series compares two numerical methods by cost.

*Cost to change: `stepping-forward-in-time` is a new id, and its cell ids become a contract once a class has used it. Moving it within the series is one line in `courses/computational-methods.yaml`.*

---

**7.254 — A module of its own for readers who struggle with maths: The Zen of Slashes and Surds, with a calm check on every page.** Josh, 26 September 2026, first asking for a fractions lesson and an exponents lesson, then: "a separate maths preliminaries module that is for folks who struggle with maths ... fill in for primary and secondary school ... emphasize things like 'we aren't trying to memorize' and talk about 'gaining fluency' ... notice when our curiosity and optimism gets replaced by frustration, and work on calm as the goal." On the name: "the whole track is 'the Zen of Slashes and Surds' for both fractions and exponents". On roots and logarithms: "we can do the definitions or notation at the end after there has been shown need for the notation, and we can use some other notation first ... because surds and logs are often scary for people." The plan is `planning/outlines/zen-of-slashes-and-surds.md`.

**A module, not a series inside another course.** The first proposal was a review series in the integrated maths course, with the Drake equation as its spine. A reader who arrives unsure of themselves in the subject, not only of a topic, needs smaller steps, more practice and a different stance than any existing course takes, so the module is `courses/zen-of-slashes-and-surds.yaml`. The Drake equation, *Fractions in the Wild* and the Grade 8 scale sheets become each strand's last page, a "view from the top", not its opening.

**A departure from 7.229, on purpose.** 7.229 names a feeling rarely, and always with a route, across the site. This module names one more often, because noticing when curiosity has turned into frustration is part of what it teaches. What 7.229 protects is kept: every mention carries a route, and none is a verdict on the reader. What changes is how often, and why: a fixed "calm check" twice on every page, in the same words each time so it becomes a habit rather than a surprise. The words live once, in `setup/zen-calm-check.md`, and every page includes that file, so changing them changes every page. The rest of the site keeps 7.229 as it is.

**Squiggles, letters and numbers are worlds.** The same problem can be written with shapes (♡, △, ★), with letters, or with numbers, and the reader chooses. The site's worlds mechanism (`docs/WRITING_TUTORIALS.md#worlds`) already does exactly this for contexts, so these pages use it for notation, with `numbers`, `squiggles` and `letters` as the world keys. Squiggles stay in prose and questions, since Python cannot use them as names.

**Pictures are drawn, not typed.** `dev/graphics/zen.py` draws the pizzas, the fraction walls, the folded paper and the golden beads in the site's theme colours, so they read in light, dark and high contrast, and computes every count it shows. The pizza a reader can change is a matplotlib pie in the page's own cell, eight lines long, not a hidden helper: a cell that draws a picture is the Montessori material made runnable, and there is no way to hide a setup cell.

**Friendly notation first for roots and logarithms.** In strand C, a root is *side(49)*, the side of a square of 49 beads, and a logarithm is *hops(10 → 1000)*, until the reader has used the friendly name often enough to want something shorter. The signs $\sqrt{\;}$ and $\log$ come last on each page, under a heading that says they mean exactly the friendly name.

**Plainer than plain.** Josh, while the pages were being written: "lets make sure we use really simple friendly language (especially for ESL learners)". The pages go further than the style guide's plain-language rules: short sentences with one idea each, common words (*normal*, *scary*, *aloud*), every hard word explained where it appears, frustration included ("annoyed, tired or stuck"), no idioms or phrasal verbs, lists in place of long sentences, and one gap per line in a fill-in-the-blank question. The outline's "Language: plainer than plain" section has the list, for whoever writes the next page.

**A pilot, with both halves.** Written now: `before-we-start`, `one-whole-many-slices`, `same-amount-different-names` and `the-long-way`, each with a practice page longer than the tutorial. Two fraction pages and one powers page, so a class meets both slashes and powers. The course is `status: beta`. What the pilot should answer: are the steps small enough, does the calm check help or annoy, and do readers use the notation switch.

*Cost to change: the four page ids and their question ids become a contract once a class has used them. The calm check's words are one file. Moving the course on the front page is one line in `courses/index.yaml`.*

---

**7.255 — A dropdown gap starts on a blank "choose", not on the page's word.** Found while checking the Zen of Slashes and Surds pages (7.254) in a browser: every dropdown in a fill-in-the-blank question opened showing its own answer. `build.py` writes the page's word as the first `<option>`, so the browser selects it, and `buildQuestions()` then shuffled the options without touching which one was selected. The page's word moved, and stayed selected wherever it landed. Loading one page five times showed the answer selected in all 20 dropdowns.

**The fix is in both places.** `build.py` now writes `<option value="" selected disabled>choose</option>` first, so a page with no JavaScript, or one whose runtime has not started yet, shows the blank too. The runtime shuffles every option except that one. A reader cannot pick "choose" back, so a saved value is always a real choice or nothing. One leftover: a record saved before the fix holds whatever the dropdown showed, which was usually the page's word whether or not the reader chose it, and it restores that way. It clears when the reader picks again.

**Why not `selectedIndex = -1`.** A select with nothing selected is an empty box with no word in it, which reads as broken. "choose" says what to do.

*Cost to change: low. One line in `build.py`, one in the runtime (and the rebuilt `standalone.bundle.js`), and a browser test that the dropdown starts blank. Every page with a dropdown gap changes on the next build; no saved work moves.*

---

**7.256 — Say it directly: a style rule against clever framing, and a sweep of every page.** Josh, 26 September 2026, after a review of the recent pull requests: "those gerunds and weird indirect framing are just not the same as simple friendly prose… lets see if we can get rid of all those!"

**What the review found.** Five readers, each given a different group of recent pages (Programming Foundations, both halves of OOP, the long Dewey Track pages, and the newest merges), found the same drift on their own. Sentences had not grown longer: the recent groups average 12.5 to 14 words, against a site median of 12.4, and dashes were nearly gone. The drift was in how sentences were built. Colons carried the main point where dashes used to (about 130 to 170 mid-sentence colons in each OOP half). Paragraphs ended on a saying ("'has a' bends where 'is a' breaks"). Verbs became nouns ("the deciding… kept apart from the asking"). Sentences put the point last ("What changes is where…") or had no verb at all. Planning words reached students ("This one has no top"). Quiet verdicts slipped past the #376 sweep ("not yet", "a fair answer", "the tests are the judge"). Each reads well to a native speaker and asks a second-language reader to read twice.

**The rule.** `PEDAGOGICAL_STYLE_GUIDE.md#say-it-directly`: somebody or something does something, in that order. It lists the eight shapes with an example of each from a real page, and a line joins the checklist. The quiet verdicts join `#no-verdicts`, and the phrasal verbs that kept coming back (*work out*, *give back*, *go through*, *reach in*, *throw away*, *out of order*) join `#plain-language`. Length was left alone: 7.244 still holds, and the long Dewey Track pages are long mostly because of their guess-run-explain cycles.

**One stock line.** "One way through; yours may differ and work as well." sat in 75 answer folds on 29 pages: an idiom with a semicolon in it. It is now "Here is one answer. Yours may be different and work too." everywhere.

**A fact the review turned up.** Four pages (the shared "When a cell does not do what you expect" section, `first-steps-cm-practice`, `four-questions` and the FAQ) said Reset brings back the starter code. Reset (↺) clears the output; Clear (↻) puts the code back (`build.py`, `dl-btn-reset` and `dl-btn-clear`). 7.249 fixed the same sentence on `working-with-tables` and missed these.

**The sweep.** Every current page in `tutorials/` was read by one of eight readers against the rule, who rewrote only the sentences that break it. Code, frontmatter, headings' wording (their slugs are `covers:` keys), cell ids and frozen releases were not touched; Title Case headings became sentence case. No `version:` bump, since no cell changed. Four more readers then read the whole diff against the old text, looking only for damage: about 120 sentences, one in forty, had come out ungrammatical, lost a reason (why gradient descent stops in the wrong valley), or changed a fact (a binary search that "removed" names it only skipped). Those were fixed. A rewrite that is simpler and less true is the cost this rule has to watch for.

**Left for later.** Four sideline sections on long Dewey Track pages could move to a context page (7.208): the Timsort aside in `racing-the-sorts`, "Three weights for a curve" in `rules-with-letters-in-them`, the Pascal detour in `machines-that-take-a-number`, and the $x^2$ against $2^x$ race in `drawing-a-rule`. The data-copy note is written by hand on 10 pages in 5 wordings, and its runtime strings in `assets/tutorial-runtime.js` and `assets/tutorial_tools.py` need the same plain rewrite and a vendor rebuild. Glossary files were not swept. Nor were the Zen of Slashes and Surds pages (7.254), which reached `main` during the sweep, or the Data, Chance and Logic pages that #385 rewrites; each should be read against `#say-it-directly` on its own.

*Cost to change: none for the rule. The sweep is prose only; a rewritten sentence can be changed back by hand.*

---

**7.257 — Data, Chance and Logic is reordered so each page builds on the one before, plays each game before counting it, and draws on the worlds' real data.** The content issue (#325), part of #306.

**The order.** Sets, Venn diagrams, logic, counting, probability, three doors, statistics, charts, and a new making task, `a-chart-that-tells-the-truth`. Events are sets, so probability now comes after the pages that teach union, intersection and complement, and uses them by name: "or" is a union, and the addition rule is inclusion-exclusion with probabilities. With Venn diagrams before logic, a term had to be introduced where it is first used: the complement on Venn diagrams, De Morgan's laws, XOR and the truth table on logic. The Venn page states the two laws on sets without naming them, and the logic page names them. `dev/curriculum_map.py`'s "used before it was introduced" table is how those were found.

**Play it, then count it.** `three-doors` was already guess, play once, play ten thousand times, read the line that makes the difference, count the cases, change the host, and it is now the pattern for every probability page. `what-are-the-chances` starts with ten thousand rolls of two dice and the histogram before the 36 outcomes. The medical test moved from the practice page into the tutorial: a million people simulated, then the same million counted as a table (natural frequencies), then $P(B \mid A)$, and each world asks one conditional probability both ways round (Jurassic given Portugal against Portugal given Jurassic). `counting-carefully` lists the cases with `itertools` before each formula, and answers its opening dinner-table question at the end. `three-doors` gets a practice page with the three hosts the issue named (a favourite door, an offer only sometimes, four doors) and a glossary.

**The data pages use the worlds' own data.** The quiz scores are gone. The statistics page's prose world is the exoplanet archive, and it begins with where the data comes from: the file of 6,372 planets has 507 the size of the Earth and none of them with a year of 200 to 500 days, because a small planet with a long year is the hardest kind to find. That sampling bias is the thread through both pages. Drawing the planets' orbits against their radii showed a flat line near 13 Earth radii: radial-velocity planets whose radius the archive estimated from their mass. They are 48 of the 59 planets at the mode, 12.8, so the page says the mode reflects how the numbers were made; an earlier draft blamed rounding. The ideas that lived only in answer folds are short "go further" sections: percentiles and box plots, and the binomial distribution, on the statistics page; the central limit theorem by simulation (the means of 50-planet samples make a bell, though the radii have two humps), and the 68–95–99.7 rule, which the sample means follow and the orbits break, on the charts page. The misleading-axes problems moved into the charts tutorial, on real numbers: 260 and 245 planets drawn four to one; "discoveries collapse by 87%" from a window starting at Kepler's 2016; the dinosaur genera's unfinished 2020s.

**Every page has blocks and a closer that belongs to it.** Predict blocks where the misconceptions are, tasks with `solution` and `inputs` in each world, practice pages in blocks with problems from earlier pages, and a "Looking back" question about that page with a challenge for the Notebook. About twenty card problems that repeated one kind of task were cut; one card example stays, for drawing without replacement.

**The mixed set** covers all nine pages, three doors included (the three prisoners), and the making task (a headline drawn from two small samples on a cut axis).

**Every number was run.** Each page was run with its solutions in place of its starters, one world at a time, and every figure in the prose checked against the output. That found a password figure a thousand times too large, a decade-pace claim that was wrong, and a narrator who does have a row in the data after all.

**`dev/curriculum_map.py` finds "Where to read more" whatever its capitals.** It matched only "Where to Read More", which 35 pages use, so the titles in the other hundred-odd pages' bibliographies were counted as terms (*the python tutorial* in five pages). The build already matched the heading case-insensitively; the map now does too, with a test.

**Read against `#say-it-directly` (7.256).** These pages were rewritten before that rule reached `main`, so the merge keeps this branch's versions of the sixteen pages #386 swept. All eighteen pages were then read against the rule, and about 490 sentences changed. As elsewhere, the glossary files were not swept. A second pass after the merge compared every rewritten sentence with the one it replaced, and found 16 whose meaning had changed: a lost "among them" or "can" or "knowing", "almost never" turned into "only", a spike that no longer "stands out" among smaller ones, a line that contradicted the sentence before it. Each was put back to what the old sentence said, in the new style.

*Cost to change: moderate. The order lives in the course file and topic groups; the pages' cross-references assume it, so moving logic back before Venn diagrams would mean moving the names of the two laws back as well. Cell ids are new throughout, which is free until 2 October.*

---

**7.258 — Matrices start from pictures, and multiplication is one move after another.** The content issue (#326), part of #306.

**The order.** A grid of numbers, a matrix moving a picture, multiplication, undoing, systems, a new NumPy page (`matrices-in-numpy`), Markov chains, and a making task, `a-filter-or-a-sprite`, with a mixed set, `mixed-matrices`. The rules used to be taught on abstract $A$, $B$ and $C$, with the geometry arriving on the third page. Composition, which is the reason row-times-column exists, never appeared in two dimensions.

**Pictures first.** `grid-of-numbers` adds, scales and transposes pictures, and keeps the diamond and the `IndexError` from scaling past the ramp as a planned surprise. `what-a-matrix-does-to-a-picture` moves an F, because the unit square hides a flip, and has a matching game and one playground cell in place of four copied plotting cells. `multiplying-grids` starts from "a shear, then a quarter turn: which one matrix does both?", and the row-times-column rule comes out of that, with the `zip` warning kept. `undoing-it` measures the F's area with the shoelace formula, lets the quarter turn break the $a \times d$ guess before $ad - bc$ appears, and shows the flip's $-8$ without `abs`.

**The reader does the elimination.** `solving-systems` opens with two lines crossing, solved with the inverse, then draws parallel lines and one line drawn twice, and links a determinant of 0 to the F flattened onto a line: a point off that line is never reached, and a point on it is reached by a whole line of points. The site has no Parsons block, so the row operations come as shuffled lines in an ordinary cell. Run as they are, they stop with a `NameError`, and the error says what has to come first. The reader then writes `eliminate(M)` as a toolkit cell. Back substitution and `solve(M)` come with it, so `solve` is there on the NumPy page and in the Markov practice.

**NumPy as a check, not a replacement.** `matrices-in-numpy` checks each of the reader's functions against its one line in NumPy, shows `A * B` beside `A @ B`, times a 200×200 multiply both ways, solves a 5×5 system chosen answer-first, and moves a planet 1,000 steps with `matrix_power`.

**Markov chains.** The page names the switch from a column times a matrix to a row times a matrix, splits its word-counting cell into three, and adds a chain built from real data: NASA's daily sunlight for Dublin, with each day bright or dull against the middle day of its own month. A bright day is followed by another 61% of the time, and a dull day by another 62%. After two bright days, the next is bright 65% of the time, and after a dull day then a bright one, 55%: the page says this, because it is where a one-day chain falls short.

**Solutions carry their own setup.** The build runs each solution after the page's starter cells, where a toolkit function from an earlier page is a stub. A world solution that calls `transform`, `inverse` or `solve` therefore includes the matching file from `setup/matrices/`, which holds the reference versions.

**Found while checking.** Every page was run with its solutions, one world at a time. That found a brightness claim the matrix contradicted, a flip described as a turn, two claims about the Plough that were not true, "the one kind of move where order does not matter" (there are others), and an explanation of the $a \times d$ guess that did not say which way it was off.

*Cost to change: moderate. The order lives in the course file and topic groups. Cell ids are new throughout, which is free until 2 October; after that, the toolkit cell ids (`grid-scale`, `matrix-move`, `matrix-dot-multiply`, `matrix-det-inverse`, `systems-eliminate`, `systems-solve` and the rest) are keys for the reader's saved functions on every later page.*

---

**7.259 — The Dewey Track gets its diagrams, an aside on every practice page, and the Irish Lotto's new numbers.** Issues #354 and #352.

- **Diagrams.** 53 figures across 38 Dewey Track tutorials, drawn by `dev/graphics/dewey_units_1_5.py` and `dev/graphics/dewey_units_6_10.py` in the way `planning/VISUAL_LIST.md` describes: every number computed, often by running the page's own cell; theme colours only; full-sentence alt text. Two text drawings (the seven-segment block and the outfit tree) became pictures. A figure never shows an answer the page asks the reader to predict, and a chart or animation a cell already draws is not repeated as a still. Places considered and turned down are listed in the PR.
- **Asides.** Each of the 47 practice pages and 9 mixed pages has one `dl-note` beside the problem it belongs to: a bit of history, a word's origin or a real system doing the same thing, each checked against a source (listed in the PR). Things a tutorial already tells were left out.
- **The Irish Lotto** draws 6 numbers from 45 since 5 September 2026, not from 47 (lottery.ie, "Change is coming"; RTÉ, 16 July 2026). *Orders and choices*, its practice page, *How likely is it?*'s practice page and *Counting carefully*'s practice page now use C(45, 6) = 8,145,060, with every derived number run again.

*Cost to change: a diagram is a function in its generator; an aside is a paragraph.*

---

**7.260 — Graphics ends with a scene the reader builds, and each page gains worlds and a NumPy fold.** The content issue (#327), part of #306.

**Your own scene.** Until now, readers of the Graphics series only changed numbers in other people's shapes. The new closing page, `your-own-scene`, has three steps. The first is a wireframe of the reader's own: a pyramid to start from, or a lighthouse, a small solar system or the F from the matrices series in 3D, one per world. The second places three copies with translation and rotation, through one camera with a chosen field of view. The third is a turntable, a camera that flies, or edges sorted by depth (the painter's algorithm), each with working code in a fold so that every step can be reached. The tools from the four pages are gathered in `setup/graphics/scene.py`: 4×4 matrices, `chain`, `place`, `combine`, and a `draw_wireframe` that leaves out any edge behind the near plane, so the reader never meets the broken orbit by accident. There is a version for one person and a version for a group, and the page ends with reflection questions only.

**Worlds and folds.** Each page now has world tasks: the Moon and the Sun (their sizes over their distances differ by about 3%, which is why eclipses happen), a photo on a wall seen at an angle, a starship and its model, a moon on a moving planet, a lane of beacons flown through, a spire, a sprite on a turning card, a castle's three towers, and a planet placed by "move out, then turn about the star". Each page also has a short "the same in NumPy" fold, following `matrices-in-numpy` (7.258).

**Kept.** The deliberately broken orbit in "Through the camera" stays as it was. "Keep three things in mind" now appears once, on the first page; the second page says the same in one line.

**Practice.** `a-ball-in-orbit-practice` grew from 3 problems to 10: frame rates, the hoop at eye level (a predict), how distance flattens the front-to-back difference, the near plane, two world orbits and two from earlier pages. The other practice pages gain a predict on the shape of a product, a house to build as a wireframe, and a `multiply(cube4, camera)` that silently uses 4 of the 8 corners, because `setup/cube.py`'s `dot` uses `zip`, which is the warning from `multiplying-grids`.

**Found while checking.** `turning-a-cube` still named `rotate90` and "that gallery", both renamed in #326, and two pages said they began "with no code from earlier pages", which the matrices toolkit has made untrue. Drawing the planet task at first showed the quarter-turn planet behind the star; `rotation_y` sends it towards the camera, and the text now says so.

*Cost to change: small. `your-own-scene` is a new id, the world cells' ids are new, and `setup/graphics/scene.py` is used only by the new page. Cell ids become a contract on 2 October.*

---

**7.261 — Fourteen closer-look pages, each beside the page it serves.** The content issue (#337), part of #306. Josh, 26 September 2026, chose where they sit: "beside the page they serve", and all fourteen written now, with links only where the home page is already rewritten.

**The shape.** Each page follows `docs/templates/where-the-total-starts.md`. It links back to its home page, states two ideas, and runs one experiment whose predict block names the idea behind each option. It says which idea matches what happens, explains why the other is so easy to believe, and ends with a second, smaller case ("Where else it happens") and somewhere to read more. None says the reader held the idea. Each experiment uses only what its home page and the pages before it have taught: the running-total page loops over `range`, because lists come a page later; the vertex page shows a shifted $x^3$, not a sine wave, because trigonometry comes after algebra; the two-methods page avoids `continue`.

**The fourteen, and where each sits.**

| Page | Home page | Placed |
|---|---|---|
| `powers-in-python` (`^`, `**`, `-3 ** 2`) | `first-steps` | after it, and after `first-steps-cm` |
| `dividing-in-python` (`-7 // 2`, `0.1 * 3`) | `storing-and-computing` | after it, three courses |
| `equals-three-ways` | `making-decisions` | after it, three courses |
| `a-total-that-starts-again` | `repeating-yourself` | after it, three courses |
| `two-names-one-list` | `comprehensions-and-grids` | after it, three courses |
| `small-samples` (8 sevens against 9) | `what-are-the-chances` | after it |
| `when-two-methods-agree` (a die with faces 0 to 5) | `three-doors` | after it |
| `when-is-a-breaks` (`Square(Rectangle)`) | `one-parent-many-children` | after it |
| `dividing-every-term` | `rearranging-formulae` | not yet |
| `the-hidden-bracket` (`v - u / a`) | `rearranging-formulae` | not yet |
| `squaring-a-sum` | `expressions-come-alive` | not yet |
| `the-vertex-sign` | `parabolas` | not yet |
| `degrees-and-radians` | `the-unit-circle` | not yet |
| `why-we-have-seasons` | `sine-and-cosine-waves` | not yet |

**Not yet placed.** The last six have homes in Algebra and Functions and in Trigonometry and Calculus, which #328 and #330 rewrite and reorder. Putting them in the course file now would collide with those rewrites. They build, are in the topics page's new "Closer looks" group, and wait for those two PRs to add each one after its home page and link to it.

**The misconception list, adjusted.** "Correlation, chance and small samples" became a page on small samples only: correlation is taught on `pictures-worth-numbers`, two pages later, so a page beside `what-are-the-chances` cannot use it. "Degrees and radians" does not repeat the `math.sin(90)` surprise, which its home page already has; it tests whether 0.894 means anything, by taking 14 whole turns away from 90 radians.

**Links in.** Eight home pages got one link each, in a predict note where one option shows the idea (`comprehensions-and-grids`, `when-it-goes-wrong`, the 0.1 + 0.2 problem on `storing-and-computing-practice`) or in one sentence where it arises (`first-steps`, `making-decisions`, `what-are-the-chances`, `three-doors`, and the "Is it a kind?" answer on `one-parent-many-children-practice`).

**Every number was run**, including that only `1 ^ 0` and `1 ** 0` agree for whole numbers up to 20, that 8 or fewer sevens in 54 rolls happens 44% of the time, that a face is missing from 12 rolls 56% of the time, and the 1.07 against 3.8 in the seasons.

*Cost to change: new ids, free until 2 October. Moving a page means its line in each course file and its home page's link.*

---

**7.262 — Problem Solving becomes a set of nine broken programs, each with a report, and the reader keeps a log.** The content issue (#334), part of #306.

**What it replaces.** `finding-where-it-went-wrong` was one story: a temperature pipeline with one planted bug, and the syllabus's five habits named after the fact. The critique asked for practice instead of a story, and the temperature conversion was one of the contexts #306 retires.

**Nine programs, each with a report.** Every program arrives with a report from the person who found the bug, in the words a user would use ("Sirius is missing", "I scored 30!"). The bugs are the ones the issue listed: an index that starts at 1, text from `input()` compared as text, two names for one list, a `return` indented into the loop, `==` on a float after 25 steps of 0.1, and an old name left over from an earlier cell. Three more carry the methods. A four-stage pipeline (light from the Sun, which should take about 8 minutes) is found by checking the middle stage first. A ship's log whose most common word is `''` is found by shrinking the text to an a, two spaces and a b. A dungeon game that crashes only sometimes is made repeatable with a seed. The contexts come from the Computational Methods worlds (stars, sprites, fossils, rockets, dungeons), one per program, so the page has no world switcher: moving between worlds is part of the practice.

**Each idea is named after the reader has used it.** The first program is worked together as a guess, a test and what happened, and only then are those three lines called a *log*. From the second program on, every cell opens with the log for the reader to write. *Bisection* is named after two checks have found the stage, *minimal reproduction* after the four-character text, and *symptom* and *cause* in the dungeon game, where a fix that sends the crashing turns to the hall hides the crash and makes the hall twice as likely. That second bug is found by counting 6,000 rooms, which the reader can do because the Simulation pages came first.

**The syllabus words.** "Pragmatic problem-solving" and "semantic analysis" are no longer the names the page teaches with. They appear once, after the plain words, as the course description's names, so a reader can recognise them in an assessment (the same approach as *indices* in `#terms`). The five habits of CMPS-LO12 are named in a short section at the end, each tied to a moment on the page where the reader used it.

**Left out: the mutable default argument.** The issue listed it. No Computational Methods page teaches default arguments, so a bug in one would be a bug in something the reader has never used. The pipeline bug takes its place. It belongs on a page after default arguments are taught, if one is added.

**No `assert`.** Computational Methods never teaches `assert` (it arrives in `building-reusable-tools`, which is not on this course), so the page's tests are prints compared with an answer found by hand. For the same reason `when-it-goes-wrong` is linked from "Where to read more" and not added to the course: its debugging section uses `assert` without teaching it.

**The practice page.** Three reports that use ideas from earlier pages (a grid built as one row three times, `counts = {}` inside the loop, `random.seed()` inside the loop), a Caesar cipher that crashes on `x`, `y` and `z` and is found by halving the sentence, two questions about symptom and cause, and one problem with no bug: how many right-and-down paths cross a four-by-four dungeon (20). The problem walks through understanding the question, trying smaller dungeons, a plan and looking back, and then names Pólya's four steps.

**Every number was run.** Including the ten empty words in the ship's log, against seven of *the*; seed 4 as one that crashes; and eight heads in ten flips with seed 42.

*Cost to change: cell ids are new throughout, which is free until 2 October. The tutorial's id is unchanged.*

---

**7.263 — Algebra and Functions draws its graphs third, and is set in four worlds.** The content issue (#328), part of #306.

**Order.** The series now runs numbers, expressions, drawing functions, rearranging, equations, parabolas and complex roots. `drawing-functions` came sixth of seven, although it says that much of the rest of the course depends on its habit. Third, it opens by drawing the rocket that the polynomials page evaluated, and later pages read answers from crossings and vertices. Complex roots move to the end, after parabolas, so that "the vertex is above the axis" comes before "the roots are not on this line". Every link that named a page as "next" or "earlier" was checked against the new order. `lambda` is now introduced where it is first used, in `drawing-functions`, and not in `rearranging-formulae`.

**Worlds.** Each page chooses from four: music (a semitone as $2^{1/12}$, octaves as logarithms, beats against a tuning fork), electronics (a 12 V supply with 2 ohms inside, whose power $12I - 2I^2$ is evaluated, drawn and maximised across three pages; a voltage divider; an impedance), rockets (a height polynomial, Kepler's $a^{3/2}$, a fuel fraction, two launches meeting) and fantasy maps (zoom levels, map scale, roads as lines, a catapult's arc). A series-end making task, `a-tool-of-your-own`, asks for a tuning calculator, a circuit designer, a launch planner or a route finder.

**Pages.** Numbers and powers opens with `Fraction(0.1)`, which shows that every float is rational. It teaches the division rule, fractional powers and $\log(x^n) = n\log x$, which the practice page and mixed-algebra Q7 already asked for. Nine geometry functions become three, and a doubling investigation. Polynomials asks for expansion by hand before `multiply_poly` checks it, and names an identity. The graphs page has the reader write `plot_line`, restores the outline's translation cells, and draws the logarithm as the inverse of $2^x$. Rearranging keeps its voice, and adds a subject behind a minus sign, a subject that appears twice, and `v - u / a`. Equations adds balancing by hand, and derives simultaneous equations from a break-even point in the chosen world, read from the graph and then solved by elimination. The formula that arrived from nowhere is now derived in a fold, with the determinant. Parabolas uses $a(x - h)^2 + k$ from its first mention, and the reader writes `complete_the_square(a, b, c)`. Complex roots slides $c$ through $x^2 - 2x + c$ and marks both roots on the complex plane. It has the reader check Bombelli's $(2 + i)^3$, explains the solver's `+0j`, and draws multiplying by $i$ as a quarter turn.

**Seams.** Predict blocks take the places where Python and maths disagree: `3 ^ 2` is 1, `-3 ** 2` is $-9$, `x = x + 1` prints 6, `(x + 3) ** 2` is not `x ** 2 + 9`, and `v - u / a` is not $\frac{v - u}{a}$. The closer looks from #337 (7.261) that wait on this series now sit beside their pages in the course: `squaring-a-sum` after the polynomials page, `dividing-every-term` and `the-hidden-bracket` after rearranging, and `the-vertex-sign` after parabolas. The predict notes and the sentences where each idea arises link to them, and to `powers-in-python` and `equals-three-ways`. A number predict is compared with the last number the cell prints, so each of these cells ends on the line its question asks about.

**Practice.** Every practice page lost the problems that repeated a tutorial task word for word, and gained predicts, a problem in each world and two from earlier pages. Checks that needed the quadratic formula or factorising, before the page that teaches them, now check by substitution. `mixed-algebra` keeps its hint folds and gains a problem that joins the vertex form to complex roots.

*Cost to change: small. `a-tool-of-your-own` and every world cell are new ids, and cell ids become a contract on 2 October. The course order is one list in `courses/mit-pdp-maths-prog-integration.yaml`.*

---

**7.264 — `slider()`: moving it runs its own cell, and the slider lives above the output.** Issue #329, part of #306.

`slider(label, low, high, step=None, value=None, id=None)` joins `text_input` and `dropdown`. `.value` is a number, an `int` when the ends and the step are whole. Moving it runs the cell again, so a plot drawn from `.value` follows the thumb.

**Where it lives.** A run clears the cell's output, so a slider left there would disappear from under the reader's pointer halfway through a drag. After each run the page moves a new slider up into a strip between the Run bar and the output, which no run clears, and drops the copy of one already there (matched by its DOM id; edited ends, step or label are copied across). A slider the latest run did not make is removed. The cost: a slider always appears above what the cell prints, wherever the code calls it.

**How often it runs.** At most one run in flight per cell. A drag fires far faster than a plotting cell runs, so each run takes the thumb's value when it starts, and one more follows the last move. Measured on the fixture's sine wave: about 120 ms a run, and the plot redrawn 19 times in a 30-step drag in the Worker and 30 times on the main thread.

**How Python hears it.** Before every run, the page sends each slider's value in (`widget-changed` in the Worker, `_set_widget_value` on the main thread), and `.value` reads only that. One path serves the hosted page and the downloaded copy, and it is also how a slider restored after a reload is heard: the strip is saved with the page (`sliders_html`) and the first run afterwards reads where the reader left it.

**Quiet runs.** A slider's run counts as exploring. It does not count as an attempt for a staged hint, does not settle a prediction, and is not announced to a screen reader; twenty announcements in one drag would drown the page. The Run button still turns into Stop while it runs, so a slow cell can be stopped.

**Not done.** The issue offered re-running "the cell, or a named function". Only the cell: a named function would need a second output area inside the cell and a callback path into the Worker, for a gain a short cell already gives. In the Notebook a slider draws but does not run its cell yet, and its guide says so.

*Cost to change: small. The markup is `.dl-slider` inside `.dl-widget`; the page's half is six functions beside `runCell()`; the saved record's `sliders_html` is optional, so older saves load unchanged.*

---

**7.265 — The Dewey Track's letter is signed "dewlab".** Josh, 26 September 2026, closing #351: "dewlab should sign it not me". 7.228 left the letter unsigned until he had read it. The letter's "I" is now the site's voice, not a person's, which also keeps the style guide's rule that a page never invents the writer's history.

*Cost to change: one line at the end of `how-this-course-is-built`.*

---

**7.266 — Programming and Design Principles is the first card on the front page, through a `cards:` list rather than `order:`.** Josh, 26 September 2026: "move the Programming Design Principles card to the top of the list." 7.171 put it last. `courses/index.yaml`'s `order:` sets the tiles, but it also sets each shared page's default course (7.172's "first in `courses/index.yaml` that lists it"), and every one of this course's pages is shared with the integrated maths course. Moving it to the top of `order:` would have given those pages this course's tree, previous/next and reference-panel accumulation by default, which drops the maths pages from the integrated course's "earlier in the series". So the index gains an optional `cards:` list: the courses it names come first on the front page, the rest follow `order:`, and nothing else reads it (`course_card_order()`). The contents page keeps `order:`.

*Cost to change: delete the `cards:` lines and the tiles follow `order:` again.*

---

**7.267 — Trigonometry and Calculus finds its coordinates before it names them, and the calculus reaches the waves.** The content issue (#330), part of #306.

**Pages.** `lines-and-distances` (26 cells) became two pages: `slope-and-lines` (slope as a rate, parallel and perpendicular, the vertical line and the general form) and `distance-and-pythagoras` (the distance formula, checking the theorem at 80, 90 and 100 degrees, the midpoint). Its old address redirects to the first. `rates-of-change` became two as well: the derivative and turning points stay, and `derivative-rules` finds each rule by experiment. The power rule is checked on powers the table lacked. The product rule keeps the moment where multiplying the derivatives gives 48 against 80, and then tests three guesses against the numbers. The chain rule asks whether multiplying works this time. A new page, `the-slope-of-a-wave`, differentiates `math.sin` numerically, finds cos, and measures how fast Dublin's days grow: about 4.7 minutes a day at the equinox by the fitted wave and 4.2 by the data, and 0 at the solstice. Before it, the series called itself Trigonometry and Calculus, and the calculus never touched a wave. `a-model-of-your-own` is the series-end making task: navigate by two lighthouses, build a chord, chart the Moon's rise, or survey a kingdom.

**Coordinates first.** `the-unit-circle` built `unit_point` from `cos` and `sin` and then named the columns cosine and sine, which was circular. Now a clock hand's tip walks round in ten thousand steps, each at right angles to the hand. That is the quarter turn from the lines page and from multiplying by $i$. A predict asks how far up it is after an eighth of a turn (0.71, where many guess 0.5), and only then are the columns named and compared with `math.cos` and `math.sin`. Radians follow as the distance walked. The same walk later explains why the slope of sine is cosine.

**Moving pictures.** Three `FuncAnimation`s from the outlines: the circle unrolling into a wave, the side of 6 swinging to meet the line twice in the ambiguous case, and chords closing on a tangent. Each is kept to about 24 frames of a small figure, a few hundred kilobytes. Five sliders from #329 (7.264): the tip of the hand, the four numbers of a wave against a target, a daylight fit, the swinging side's length, and a day on the daylight curve with its tangent. The wave sliders print a measured gap (`gap_to_data`, the average distance from the points), so the reader sees how close a fit is and gets no verdict.

**Data.** `data/daylight.csv` and `data/dublin-tides.csv` (#324) now carry the waves: Dublin's daylight fitted from the numbers read off the year (a gap of about 10 minutes; the shift lands on the equinox), the tide at Dublin Port, Cape Town half a year out of step, and Reykjavik further from a sine than Dublin.

**The step size.** `approaching-a-limit` draws the error against the gap on log axes. The V it makes explains the silent 0.0 at $10^{-16}$, and why `derivative_at` uses `1e-6`, near the bottom of its own V.

**Worlds.** Each page chooses from four: sea and sky (a submarine, a lighthouse and a sextant, tides, the rule of twelfths), sound (thunder, a guitar's note, beats, a chord), planets and moons (Voyager 1, the Moon's orbit, Venus's elongation, Aristarchus, sunlight on a spacecraft), and fantasy maps (roads, a windmill, a survey by triangles, a catapult).

**Closer looks.** `degrees-and-radians` and `why-we-have-seasons` (7.261) sit after the unit circle and the waves page in the course, and the `math.sin(90)` predict and the seasons paragraph link to them.

**Practice.** Sixteen problems that repeated a tutorial task word for word are gone, or the tutorial's task changed so the problem no longer repeats it. Every practice page gained predicts, a problem in each world and two from earlier. `mixed-calculus` is new, and `mixed-trigonometry` gains problems that join the pages. The outline's own rationale and the line telling adults they "did not enjoy" geometry are gone.

**Not done.** `derivative_at` is repeated as a setup cell on each calculus page and not made a toolkit cell (#395): a toolkit cell would add a line to every later page of the course, including the project pages that never use it.

*Cost to change: moderate. The new ids (`slope-and-lines`, `distance-and-pythagoras`, `derivative-rules`, `the-slope-of-a-wave`, `a-model-of-your-own`, `mixed-calculus`) and every world cell become a contract on 2 October. The order is one list in `courses/mit-pdp-maths-prog-integration.yaml`, and the old address is one line in `courses/redirects.yaml`.*

**7.268 — On the Dewey Track, a test the page writes against the reader's code becomes a comparison with a solution.** Josh, 26 September 2026, deciding the open question on #353: "yeah two is the correct option for sure".

**The question.** Toolkit pages ended with a cell of `assert` lines the page had written, followed by a line such as "The flat-shape tools keep their promises." Schlomo's Fix problems did the same: "the test fails", then a praise line once it passed. #314 retired `check()` because the page decided the answer in advance and reported pass or fail; a page-written assert does the same job. It shows its expected values, and an assert is a real tool, but a reader who meets an `AssertionError` from a test they did not write hears "wrong".

**What changed.** 279 asserts are gone from 66 files. In their place are 74 comparisons, each an `inputs` block (the same calls, with no expected values) and a `solution` block. For a toolkit cell, the solution is its reference fence. The reader presses **Compare with a solution** and sees their answer beside a solution's, row by row. A relation between two calls (`2 * triangle_area(6, 5)` and `rectangle_area(6, 5)`) is two rows side by side, and a loop over hundreds of cases is a few sample rows. Fix problems state the symptom as a fact about the code ("For 18 degrees, this function says `False`"), and their answer folds become solution notes. Every "keeps its promise", "All tests pass" and "checks out" line printed about the reader's work is gone.

**What stays.** There are 141 asserts left, and none of them is the page judging the reader:
- the ones on `does-it-work` and its practice page, where testing is the lesson;
- asserts the reader writes, and the model answers to those tasks;
- asserts in teaching cells that show what `assert` does on the page's own code.

**Found on the way.** The build checks a comparison against the page up to its own cell. Four helper cells that the new tables need were therefore moved above the toolkit cells they serve: `likely-fixed-trials`, `solving-by-bisect-rules`, `solving-by-tank-rule` and `row-is-cold`. Duplicate answer folds that repeated the new solution were removed. Some toolkit hints still appear only after errors, as they did before. An unfinished stub raises none, so those hints now wait for the reader's own code to fail.

`planning/DEWEY_TRACK_PLAN.md` says the same. Nothing in the style guide changed, because `#no-verdicts` already covered this case.

*Cost to change: moderate. The comparisons are ordinary blocks, and bringing a test cell back means writing its expected values again. The deleted test cells' ids were free while the track is in beta.*
