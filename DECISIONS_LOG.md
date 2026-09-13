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
Outcomes `MIT-4.1`–`MIT-4.4` form their own tutorial, *Lines and Distances*,
between Drawing Functions and Angles and Waves. Pythagoras is one of the topic
tree's six gateways, unlocking seven downstream topics, so it needs a
dedicated tutorial rather than a subsection of graphing — and having one also
means *The Unit Circle* doesn't have to introduce Cartesian coordinates as an
aside.
*Cost to change: none yet.*

**7.38 — Connections between whole things, rather than things merged.**
Venn diagrams (`MIT-2.3`) get a dedicated short tutorial, *Drawing Sets*,
linked to *Logic and Truth* and *Sets as Sorted Lists* — three distinct,
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
*The Unit Circle* (radians, sine/cosine definitions, exact values), *Sine and
Cosine Waves* (unrolling circular motion into wave functions), and *Solving
Triangles* (Sine/Cosine Rules, area, right-triangle applications) — each a
distinct conceptual activity with room for exercises. *Parabolas* was split
from *Drawing Functions* on the same principle.
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
that are already problems or reflection (*Bringing It All Together*, *Looking
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
*First Steps*, *Numbers and Their Families*, *What Are the Chances*, and
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
`PEDAGOGICAL_STYLE_GUIDE.md` §5 had cell-length, boilerplate, and tool rules
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

**It was withdrawn because the links were wrong too often to ship.** The glossary's terms include ordinary English words — *set*, *shape*, *limit*, *function*, *list* — and a regex cannot tell which sense a sentence means. Sampling eight uses of *shape* on one page: six were the everyday word, two were a matrix's shape. That is worse than not linking, and specifically worse for the adult learners `PEDAGOGICAL_STYLE_GUIDE.md` §1 describes, many expecting to be bad at mathematics — sending one of them to a tutorial on set theory because the prose said "set a seed" costs confidence.

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

**7.111 — The style guide gained a plain-language section, and the four student-facing surfaces were rewritten to it.** The contents page, About page, topic tree, and 251 glossary definitions all passed §4 of `PEDAGOGICAL_STYLE_GUIDE.md` as written — invitational, warm, prose not bullets — and were still hard to read: §4 governed stance, not sentence architecture, and §1 says a reader may be working in a second language.

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
verdict regardless of caption (style guide §11). `run_cell()` still
returns a boolean, since dewmini and `pyodide-engine.js` depend on that.

**What clears nothing.** A hint once shown stays; Reset keeps the
counters (a reader resetting code is still stuck); two Settings rows
control whether hints appear at all (default on) and whether Restart
Python hides them (default keep). Counters and revealed folds travel in
the saved-work record.

**The first fold asks, not tells.** The style guide's new §3 subsection
sets three stages — a question, then steps, then the shape of the code,
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
`database-methods` as fully checked against
`PEDAGOGICAL_STYLE_GUIDE.md` §4; every other module, `web-authoring`
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
