# Architecture

The other door in, for reading the code rather than writing a tutorial —
read `docs/WRITING_TUTORIALS.md` first if you're writing one; this document
assumes that and goes underneath it. `DECISIONS_LOG.md` records why specific
choices were made; this document maps what the pieces are and how they fit
together.

There is no backend: nothing here is a server you deploy, a database you
migrate, or an API you version. Three separate programs, none aware of the
others:

1. **`build.py`** — runs once per push, turns `tutorials/` markdown into the
   static HTML in `site/`, which GitHub Pages serves as files.
2. **`assets/tutorial-runtime.js`** — ships in every built page and runs in
   the *student's* browser tab. Boots Pyodide (Python compiled to
   WebAssembly) client-side and executes cells there. No student code ever
   reaches a dewlab-controlled server, because there isn't one.
3. **`assets/editor.js`** — ships inside `editor.html` and runs in an
   *author's* browser tab. Reads and writes tutorial markdown through
   GitHub's own API, using a token the author supplies, and opens a pull
   request. A client of GitHub, not of anything dewlab hosts.

None of the three needs the others running.

---

## 1. The build: markdown in, static site out

`build.py` is a single script that reads `tutorials/*/*.md` and `courses/*.yaml`
and writes
`site/`. It runs locally for a preview and again in
`.github/workflows/deploy.yml` on every push to `main`. `site/` is gitignored
and rebuilt from scratch each time, so a published page never drifts from the
markdown that describes it.

A tutorial is a folder, `tutorials/<id>/`, holding its markdown at
`<id>.md`, its practice page, its glossary, any frozen past releases as
`v<version>.md`, its images/recordings, and any downloadable sibling file
linked with `href=` rather than shown with `src=` (a standalone `.html` a
reader can take as a starting point, say). Both are found by reading the
folder rather than a frontmatter list (`tutorial_assets()`) and get their
file name rewritten to survive the current release sitting one level above
its own folder (`resolve_assets()`) — a missing `src=` target fails the
build like a dead `tutorial:` link; a missing `href=` target is left alone,
since plenty of links aren't a local asset at all. Where a page ends up is
decided by its id — its folder name — and nothing in its frontmatter:
`tutorials/<id>.html`.

The pipeline, in order:

1. **Parse frontmatter.** `split_frontmatter()` validates the YAML block —
   required fields, a version shaped like `2026.09.15.1`, a `status` from
   the known set. A tutorial that fails this stops the whole build.

2. **Pull code and maths out before markdown sees them.** `extract_blocks()`
   replaces every fenced code block with a numbered placeholder and records
   each as a `Cell` (`exec`-tagged, with `id`/`hint` parsed off), a
   `SitePane` (an `html`/`css`/`js` fence tagged `site`, grouped by
   `site:` name into one `SiteEditor` — a live preview with no Pyodide
   involved), an `AppPane` (the same three languages tagged `app` instead,
   grouped by `app:` name into one `AppCell` — a full-stack cell whose
   JavaScript can reach the page's own shared `db`, `DECISIONS_LOG.md`
   7.180), or a `CodeBlock` (anything else). `extract_math()` does the
   same for `$…$`/`$$…$$`, since Python's `markdown` library doesn't know
   dewlab's conventions and would otherwise read `$a_i + b_j$`'s subscript
   as emphasis.

3. **Convert what's left with `markdown.Markdown()`**, then reinsert each
   placeholder as real markup: `render_cell()` for a live cell (an empty
   shell — CodeMirror mount point, Run button, output div; nothing about how
   it runs lives here), `render_code_block()` for illustrative code
   (pre-escaped), `render_math()` for a span KaTeX fills client-side.

4. **Resolve cross-tutorial links and validate structure.** A
   `tutorial:slug#anchor` link becomes a real relative href or the build
   fails. `<img>` without `alt` fails the same way, as does a `<details>`
   fold without `dl-hint`/`dl-answer`. `problems()` in `editor.js` (§3) runs
   the same checks client-side, before a commit rather than after CI.

5. **Assemble navigation.** `series_of()`, `versions_of()`, `practice_pairs()`,
   `mixed_practice()`, `context_pages()`, `archived_of()` read
   `courses/*.yaml` and each tutorial's frontmatter to work out reading
   order, the current release, which tutorial a practice or context page
   belongs to, and what's retired. Practice pages (`practice_for`,
   `practice_across`) and context pages (`context_for`, optional background
   reading in a folder of its own) are *companion* pages
   (`Tutorial.is_companion`): off the route, out of search and coverage,
   placed and glossed through the tutorial(s) they name. An id listed in a course file with
   no tutorial behind it fails the build here rather than surfacing as a
   broken "next" link; a tutorial on no course builds, and is noted. A
   tutorial listed on two courses builds once, with the tree and
   previous/next of the first course that lists it and a line under its
   heading naming the other; `write_routes()` writes every course's
   contents to `assets/routes.json` for the runtime to redraw that chrome
   per course (§2), and `write_redirects()` writes a small page at every
   old address `courses/redirects.yaml` lists.

6. **Render into `assets/shell.html`.** Every page — tutorial, contents
   page, topic tree, `editor.html` — is the same template with `{{TOKEN}}`
   placeholders filled. A token the template doesn't fill, or a page that
   leaves one unfilled, fails the build. `write_editor_page()` assembles
   `editor.html` specifically, wiring on its `<script type="module"
   src="editor.js">` tag and the vendored Milkdown stylesheet. A hand-written
   page with no curriculum data of its own — About, the home page, and the
   features page today — has its content in `pages/<name>.md`, not a string
   in `build.py`: `read_page()` reads its minimal `title`-only frontmatter
   and converts the body with the same `to_html()` a tutorial's own prose
   uses, and one `write_page(name)` (`SITE_PAGES` holds what differs: the
   file name, the crumb, the bottom-nav link) assembles the shell around
   what it returns. Two things a page can
   have that ordinary prose can't: a ` ```card ` fence (`url:`/`status:`/
   `meta:`/`wide:` header lines, then a heading and a paragraph —
   `parse_card()`/`render_card()`), the markup a module tile on the home
   page used to be hand-written six times over, with adjacent cards sharing
   one `.dl-module-grid` wrapper automatically; and a `[[name]]` marker for
   infrastructure a page can point at but never author directly
   (`GENERATED_BLOCKS`): `[[search-box]]`, the live search, and
   `[[course-cards]]`, one tile per course from the course files.
   A `<div class="dl-hero">`/`<div class="dl-audience">`/`<div
   class="dl-attribution">`/`<ul class="dl-feature-list">` section or list
   wrapper gets `markdown="1"` added to it before conversion
   (`mark_markdown_wrappers()`), the same mark a `<details class="dl-hint">`
   fold gets. Python-Markdown treats a raw HTML block as opaque through to
   its closing tag, so a heading, paragraph, or list item written inside one
   would otherwise reach the page as literal, unconverted text; the
   `md_in_html` extension parses inside any element carrying that attribute
   and strips the attribute from the output.

7. **Write the manifest.** Every page carries a `<script
   type="application/json" id="dewlab-manifest">` with what the runtime
   needs and can't otherwise know: the cell list (id, starter code, hint),
   extra Python packages beyond the default three, whether the page has
   maths, content-hashed asset versions. This manifest is the entire
   contract between `build.py` and `tutorial-runtime.js` — read once at
   `readManifest()` and trusted from then on.

8. **Stamp the footer.** `site_footer()` builds the copyright line and,
   unless `feedback_enabled()` says otherwise, the "three doors" reporting
   disclosure. `report_doors_html(page, version)` renders three plain links,
   no JavaScript: a question goes to `/discussions/new`; the other two call
   `report_issue_url(page, version, kind)`, a GitHub "new issue" address
   with `page`/`version`/`kind` as query parameters the issue template
   (`.github/ISSUE_TEMPLATE/report.yml`) reads back and shows the reader
   before submission — `kind` must match one of that form's dropdown
   options, checked by
   `test_report_doors_html_kinds_match_the_issue_template`
   (tests/test_build.py). `report_doors_links()` is the shared inner markup,
   reused by `render_cell()` for a cell's own report panel with that cell's
   id as a fourth parameter.

Two supporting scripts: `dev/curriculum_map.py` regenerates
`planning/CURRICULUM_MAP.md` from `outcomes.yaml`, `topics.yaml` and every
tutorial's `covers:` frontmatter — the `tests` CI job runs it with `--check`
to fail on a stale map. `vendor-src/build-vendor.mjs` (§5) produces the
committed `assets/vendor/*.bundle.js` files — CodeMirror, KaTeX, Milkdown —
so neither CI nor a local preview needs Node.

---

## 2. The runtime: what a student's browser does

`assets/tutorial-runtime.js` loads on every tutorial page (dewmini is
separate — §4) and owns three things: the settings panel, the CodeMirror
editors for cells, and booting Pyodide to run one. Rendering a cell's
*output* is decided in `assets/tutorial_tools.py`, in Python, so those rules
are unit-testable without a browser.

A site editor (`buildSiteEditors()`) sits beside this rather than inside it —
no Pyodide, no cells: an `html site`/`css site`/`js site` fence group
becomes a live HTML/CSS/JS editor with a sandboxed preview `<iframe>`,
mounted through `assets/site-relay.js`'s `mountSitePreview()`, the same
engine `compose/dewmini.js`'s Site tab and the standalone `dewmini web`
workspace (§4) both use. A page with one of these but no cells never boots
Pyodide.

**A full-stack cell (`buildAppCells()`) reuses that fence shape for the
opposite purpose.** An `html app`/`css app`/`js app` group renders straight
into the page — no iframe, CSS scoped to its own preview with `@scope`
rather than a sandbox boundary — because its JavaScript needs exactly what
a site editor's sandbox exists to block: a route to the page's own shared
`db`. That route is `dlQuery`, a parameter the runtime closes over when it
wraps a pane's code as `(async function (root, dlQuery) { … })(…)` before
running it, backed by `tutorial_tools._query_rows()` on the far side —
`queryRowsMT()` directly on a downloaded export, or a `"query-rows"`
Worker round trip (`queryRows()`) on a hosted page, the same fork every
other dual-path call in this file already makes. A page with an app cell
but no cells still boots Pyodide, unlike a page with only a site editor,
since a query needs `sqlite3` running even with nothing to execute.
`DECISIONS_LOG.md` 7.180 has the full design, including why this is a
separate cell kind rather than a third site-pane language.

What happens on load:

- `readManifest()` reads the JSON blob from §1 step 7. A tutorial with no
  cells never fetches Pyodide — a prose-and-maths page loads instantly.
- Each cell gets a CodeMirror instance mounted over its `.dl-editor`
  placeholder, seeded from the manifest's starter code or from whatever the
  student saved last (`localStorage`, keyed `dewlab:progress:<id>`,
  scoped per cell by its stable `id`). Before that, `migrateStorage()`
  renames the page's keys from the older `<module>:<slug>` form the
  manifest's `legacy` names, once; and `initCourse()` reads which course
  the reader is following (`dewlab:course`, set by a course page on
  arrival or by the chooser on the tree) and, on a page listed by more
  than one course, redraws the tree, previous/next and the "also part
  of" line from `assets/routes.json` (`drawCourseChrome()`).
- Pyodide boots lazily, on the first Run click (`ensureBooted()`), not on
  page load. `pyodide.loadPackage(manifest.packages)` pulls in `numpy`,
  `pandas`, `matplotlib` by default, or whatever a tutorial's `packages:`
  frontmatter widens that to.

On Run (`runCell()`): the button disables, `tools.run_cell(cell.id,
outputEl, code)` is called — `tools` is `tutorial_tools.py`, imported once
into Pyodide — and Python owns the output area for that call. Anything
printed, a trailing expression's value, a DataFrame as a real table, a
matplotlib figure as a transparent PNG, a trimmed traceback: all decided in
`tutorial_tools.py`, testable under plain CPython
(`tests/test_tutorial_tools.py`). After the run, the runtime saves the
cell's code and output to `localStorage`.

A cell's report panel (`.dl-report-icon`) opens the same way its hint does.
Its two issue links carry two fields `build.py` can't know ahead of time —
the cell's current code and output — filled in by `updateCellReportLinks()`
once, at the moment the panel opens.

**Staged hints** are the one place the page reacts to how a cell's runs
have gone, not only the latest one. `build.py`
turns a ```` ```hint ```` fence into a hidden `<details
class="dl-hint dl-hint-staged">` fold carrying `data-cell` and a canonical
`data-after` (`errors:5`, `same-errors:3 minutes:2`, …), and reads an
optional `expect:` line into the manifest. `tutorial_tools.run_cell_report()`
runs the cell like `run_cell()` and returns a JSON report — `ok`, the
exception's type and first line, whether `check()` passed, whether `expect`
holds — which `executeCell()` feeds into per-cell counters
(`noteAttempt()`), tests each fold's terms against (`triggerHolds()`), and
reveals at most one fold per run (`maybeRevealHint()`).

Everything a cell can call beyond ordinary Python is defined once in
`tutorial_tools.py` and listed in `__all__`; `docs/WRITING_TUTORIALS.md`'s
"What your cells can call" table is the reader-facing version. Changing what
a cell can do starts in `tutorial_tools.py`; changing what it looks like
starts in `tutorial-runtime.js`.

Two more pieces: `assets/tree.js` draws the topic-tree and knowledge-map
SVGs from data `build.py` computes (`tree_data()`); `vendor-src/build-vendor.mjs`
also produces `assets/vendor/standalone.bundle.js`, the entire runtime as one
classic script rather than an ES module, which is what a **Download to
keep** file runs, since `file://` can't load a module.

**Code intelligence** — completion and hover docs — layers onto every
cell's CodeMirror instance in `vendor-src/codemirror-entry.js`.
Keyword/builtin completion and completion on names already typed
(`@codemirror/lang-python`'s `globalCompletion`/`localCompletionSource`) are
static, available the instant a cell mounts. `tutorial-runtime.js`'s
`pageNamesCompletion` and `docFor` are live — they read
`tutorial_tools._page_globals`, the dict every cell executes against, and
call `inspect.getdoc()` on real objects in it. Both check for a booted
interpreter at call time, so a page left open through a boot starts
offering real completions and docs without being reconfigured. Python
builtins are out of scope for `docFor`.

Completion asks **Jedi** first (`getJediCompletions`, answered by
`_dewlab_complete` in the worker or the main-thread engine). It is a
`jedi.Interpreter` over the cell's text and `_page_globals` together, so
it offers attributes as well as names: `math.` offers `sqrt`, and a name
bound by a cell that has run offers what the live object really has. The
three sources above answer only when Jedi is silent: before it has
loaded, while a Worker is busy with a long cell (a keystroke waits at
most 400ms for it), or where it has nothing to offer. Jedi's first look
at a module can take most of a second; an answer that arrives after the
older sources have been shown is kept, and the list reopens with it if
the cursor has not moved. The tutorial cells and dewmini's editors take
the same wiring. DECISIONS_LOG.md 7.214.

**The reference** (`planning/REFERENCE_PANEL.md`) is the settings panel's
sibling — same floating-card positioning and open/close mechanics, mutually
exclusive with it since both anchor to the same corner. Its content isn't
hand-written: `build.py`'s `cumulative_glossary()` assembles it per tutorial
from `<slug>.glossary.yaml` files (produced by
`.claude/skills/tutorial-glossary/SKILL.md`), walking the series of the
course the reader is following in the course file's order, and every
earlier series of that course — so a tutorial's manifest only ever
carries what it and everything before it on that course actually taught.

---

## 3. The authoring editor: a GitHub client, not a server client

`editor.html` is never linked from a student page. It exists for tutorial
authors, and everything about it follows from one fact: it has nowhere to
send a change except GitHub. `assets/editor.js`'s `githubClient()` wraps
GitHub's REST and Git Data APIs directly — list the tree at `main`, read a
blob, create blobs/a tree/a commit, push a branch, open a **draft** pull
request — using a fine-grained personal access token the author pastes in
once (`gate()`), kept in that browser's own `localStorage` and nowhere else.
The token needs `contents: write` and `pull requests: write`, scoped to
`deweydex/dewlab`, nothing broader — that scope is the access model, since
GitHub's own collaborator settings decide who can be issued one. The token
can propose commits; it cannot merge them. Every change lands as a draft PR
against `main`, going through whatever review the repository already
requires.

What the editor holds in memory (`start()`'s `state` object): every file
under `tutorials/` fetched once at load, as both a mutable working copy
(`state.files`) and an untouched original (`state.original`) — releasing
needs both, since freezing from the edited buffer rather than the original
would misrepresent what students actually had. `state.dirty` and
`state.removing` track exactly which paths a commit needs to touch.

**The prose surface.** The body of a tutorial is edited with
`createProseEditor()` (`vendor-src/milkdown-entry.js`), a thin wrapper
around Milkdown's Crepe preset, vendored the same way CodeMirror and KaTeX
are: `npm run build` inside `vendor-src/` bundles it with esbuild into
`assets/vendor/milkdown.bundle.js` (+ a sibling `.css`), committed so neither
a local preview nor CI needs Node. `.github/workflows/tests.yml`'s
`standalone-bundle-is-current` job fails if the committed bundle goes stale
against `vendor-src/`.

Two things worth knowing if you touch this integration:

- **Crepe reads its document once, at construction, and cannot swap it in
  place.** Loading different content — switching tutorials, or driving the
  editor from a test — means destroying the instance and creating a new
  one. `render()` already does this on every state change
  (`root.replaceChildren()`); it also tears down the previous Crepe
  instance first (`state.editor.destroy()`).
  `globalThis.dewlabEditor.setBody(markdown)` drives this path.

- **Crepe's code-block feature keeps only the first word of a fence's info
  string as its "language."** dewlab's convention repurposes that string to
  mean two things — `python` for highlighting, ` exec` for "this is a
  runnable cell" — which Crepe's language picker can't preserve.
  `restoreExecTag()` (`assets/editor.js`) restores it on the way out, using
  the same signal `build.py` uses to mean a fence is a cell: an `id:` line
  as the fence's first content.

The structural report (`problems()`, the same checks `build.py` fails on,
run here before a commit) also checks cross-tutorial links —
`tutorialLinkProblems()` validates every `tutorial:slug#anchor` against
every other tutorial's real slugs and headings (`tutorialAnchors()`, which
reproduces Python-Markdown's toc heading-id algorithm in JavaScript). The
cell-id-rename warning (`renamedCells()` — the one thing the editor knows
that the build can't, since by build time the rename has happened) and the
release mechanism (`release()`: freeze what students have, publish the
buffer as a new dated version beside it) are separate from this. Start in
`assets/editor.js` for that logic, or `vendor-src/milkdown-entry.js` for the
prose surface itself, including its code blocks' completion (the same
static sources as §2, minus the live layer — the editor has no interpreter
to read from).

The link picker (`matchTutorials()`, the toggle above the prose editor)
searches every tutorial by title, id or course and inserts
`[title](tutorial:slug#anchor)` at the cursor. Insertion is
`insertLink(title, href)` (`vendor-src/milkdown-entry.js`), which builds the
text node and its link mark directly against the schema rather than going
through `@milkdown/utils`'s `insert()` helper, since that helper's inline
path sanitizes any link scheme outside http/https/mailto/tel/ftp — which
would silently strip a `tutorial:` link.

`tutorial-style.css` defines the full set of `--crepe-color-*`/`--crepe-
font-*`/`--crepe-shadow-*` custom properties Crepe's structural stylesheet
expects, mapped to the matching `--dl-*` token — importing only the
structural stylesheet, with none of Crepe's skins, otherwise leaves those
undefined.

---

## 4. dewmini: a Python workspace outside any tutorial

`compose/dewmini.html` is not a tutorial — no markdown source, nothing
`build.py` generates from `tutorials/`. It's a plain page giving a student
somewhere to write and run Python that isn't tied to one lesson. It shares
`tutorial_tools.py` with every tutorial page (§2), so `show`/`show_table`/
`check`/widgets behave identically everywhere.

`compose/dewmini.js` runs Python through `assets/pyodide-engine.js`, a
shared client of `assets/pyodide-worker.js` — the same Worker-based runtime
a tutorial page's own `tutorial-runtime.js` boots (§2), reused rather than
duplicated. That's what gives dewmini a genuine Stop button: a runaway cell
blocks the Worker, not the page. `pyodide-engine.js` is its own module,
decoupled from the page's markup. `compose/dewmini-fs.js` sits between
dewmini and the actual filesystem, delegating every primitive (mount, list,
read, write, delete) to the shared engine and choosing among three backends
— a real local folder via the File System Access API, its own named OPFS
subdirectory, or IDBFS — so the file manager, SQL support (`sqlite3` against
a mounted `.db` file), and uploads all work without knowing which backend is
active. `pyodide-engine.js` falls back to running Pyodide on the main thread
when a module Worker isn't available (e.g. opened from `file://`, which
dewmini's downloadable copy avoids by serving itself from
`http://localhost` instead) — same interpreter, same `tutorial_tools.py`,
just without a genuine Stop button.

A JavaScript cell runs through neither of those — `compose/js-cell-engine.js`
is a second, smaller engine: one persistent sandboxed `<iframe
sandbox="allow-scripts">` per notebook, with no Worker, since a sandboxed
iframe with no `allow-same-origin` is already a separate, isolated realm. A
SQL cell needs no engine of its own: `compose/dewmini.js` generates a call
to `tutorial_tools.py`'s `_run_sql_cell()` against a shared `sqlite3`
connection (`db`) and runs it through `pyodide-engine.js` like any other
Python — SQL and Python share one engine; only JavaScript gets a second.

**dewmini is a workbench, not one column.** Notebooks open in tabs
(`notebooks[]` in `dewmini.js`, with `cells` re-pointed at whichever is
active), and two docked rails sit either side: a **Workbench** (left)
carrying a live variable inspector, notes and a file manager, and a
**Library** (right) carrying the cross-tutorial reference, a dataset
catalogue, help text, and Settings.

A tab need not hold a notebook of cells at all. The file manager's
`openWorkspaceFile()` can open a real workspace file directly: a `.py` as
one editor, a `.ipynb` as cells, an `.html` as a small website — its own
editor split-screen against a live sandboxed preview, discovering whatever
`.css`/`.js` of the same base name sit beside it.

Two pieces reach outside `compose/`. `write_reference_index()` in
`build.py` emits `assets/reference-index.json`, the union of every
tutorial's glossary — deliberately dropping the "never show what hasn't
been taught" rule the tutorial pages' Reference is built around, since a
workspace has no position in a series to protect. And
`tutorial_tools.describe_globals()` walks `_page_globals` and returns plain
`{name, type, summary, kind}` data, reached through the engine's
`describeGlobals()` and a `describe-globals` worker message, in Python
rather than JavaScript so it's unit-testable without a browser.

Each of these files has its own `docs/<file>-explained.md` walking through
its internal structure — start with
[`docs/pyodide-engine-explained.md`](docs/pyodide-engine-explained.md) for
the worker/main-thread split, or
[`docs/dewmini-js-explained.md`](docs/dewmini-js-explained.md) for the rest
of dewmini (cell CRUD, drag reorder, the standalone HTML export).

**dewmini has a downloadable, offline-capable copy**
(`write_dewmini_bundle()`, `build.py`) — it mirrors the hosted site's
`compose/`/`assets/`/`data/` folder shape rather than flattening, since
`compose/dewmini.html`'s relative paths assume that shape. The bundle ships
a *serve.py*: a zero-dependency wrapper around `http.server`, since a
browser blocks the JavaScript's `import` statements when a page is opened
straight off disk (no origin for a CORS check to approve).

**`compose/dewminiweb.html` is a separate product, not another dewmini
tab.** dewmini is a Python-and-SQL notebook; `dewmini web` is a
multi-file HTML/CSS/JS workspace with no notebook cells at all, shaped
like dewstack's own `workspace.js`. `compose/dewminiweb.js` owns the part
that differs — several named sites in one `localStorage` record, which one is
open, New/Delete/Load files/Download — and hands the preview, the Run
model and the console to `assets/site-relay.js`'s `mountSitePreview()`,
the same engine a tutorial's own site editor (§2) and dewmini's Site tab
mount. Its console DOM (one line per message, "Go to line", the friendly
hint) is written fresh rather than shared with `tutorial-runtime.js`'s
matching code, the same look-alike-rather-than-coupled relationship
`render_cell()` has with dewmini's own cell markup.

---

## 5. Two build systems, on purpose

Two separate `package.json`s, deliberately:

- **`vendor-src/`** exists purely to produce `assets/vendor/`. Never run in
  CI's main `tests` job, never run by an author building tutorials — its
  output, not its source, is what everything else depends on. Run `npm
  install && npm run build` inside it only when a pin in
  `vendor-src/package.json` changes, then commit the result in
  `assets/vendor/`.
- **`build.py`** and everything under `tutorials/`, `assets/*.py`, `data/`,
  `setup/` need nothing but Python. `requirements-build.txt` is the entire
  dependency list.

Cloning the repository and running `python3 build.py` works with no Node
installed, because the only things that would have needed Node already sit
in `assets/vendor/` as plain JavaScript. Node is a tool for updating three
vendored libraries, not a project dependency.

---

## 6. Tests: what each suite checks

```
python3 -m pytest                    everything
python3 -m pytest tests --ignore=tests/e2e   the fast ones, no browser
```

- **`tests/test_*.py`** — unit tests, no browser, no Pyodide. Mostly
  `build.py`'s own logic (`tests/build/`, one file per thing the build
  reads or writes) and `tutorial_tools.py`'s
  rendering rules under plain CPython (`test_tutorial_tools.py`). This is
  what CI's `tests` job runs on every push and PR.
- **`tests/e2e/test_editor.py`** — the authoring editor, driven with
  Playwright against a **fake** GitHub client injected in-page
  (`FAKE_CLIENT`, top of that file) — nothing here touches the network or
  needs a token. Since the prose editor is a real block editor, not a
  `<textarea>`, these tests drive it through
  `globalThis.dewlabEditor`'s `getBody()`/`setBody()`/`editBody()` rather
  than filling a field directly.
- **`tests/e2e/test_*.py`** (the rest) — a real Chromium against a real,
  self-hosted Pyodide, built from `tests/e2e/fixture/rendering-tour.md` by
  an actual `build.py` run. Needs `pip install playwright && playwright
  install chromium` and `python3 dev/fetch_pyodide.py` (~30 MB) first;
  skips with a message if either is missing.

None of the e2e suite runs in CI — it's a local, manual check, run before a
PR that touches the runtime or the editor.

---

## Where to start, by what you're changing

| Changing… | Start in |
|---|---|
| What a tutorial's markdown can express (a new frontmatter field, a new fence convention) | `build.py` |
| What a cell can do (a new tutorial-facing function) | `assets/tutorial_tools.py` |
| What a cell *looks like*, or the settings panel, save/restore behaviour | `assets/tutorial-runtime.js` |
| The live HTML/CSS/JS site editor's engine (preview, console, friendly errors) — shared by dewmini's Site tab, a tutorial's own site editor, and `dewmini web` | `assets/site-relay.js` |
| A tutorial page's own site editor: mounting, Run/Reset wiring, save/restore | `assets/tutorial-runtime.js`'s `buildSiteEditors()` |
| A full-stack cell: mounting, `@scope`-scoped preview, Run/Clear wiring, save/restore | `assets/tutorial-runtime.js`'s `buildAppCells()` |
| The full-stack `dlQuery` bridge (Python side, the Worker message, the JS dispatcher) | `tutorial_tools._query_rows()`, `pyodide-worker.js`'s `"query-rows"` branch, `assets/tutorial-runtime.js`'s `queryRows()`/`queryRowsMT()` |
| `dewmini web`'s own sites: the list, New/Delete/Load files/Download, per-site storage | `compose/dewminiweb.js` |
| dewmini's file manager, uploads, or storage backend | `compose/dewmini-fs.js` |
| The Python engine (boot, run a cell, hover/autocomplete, Stop) | `assets/pyodide-engine.js` |
| dewmini's cells, toolbar, or downloads | `compose/dewmini.js` |
| The offline, downloadable bundle (what's included, the local-server workaround) | `write_dewmini_bundle()` and `SERVE_SCRIPT` in `build.py` |
| The topic tree or knowledge map's layout | `assets/tree.js` and `build.py`'s `tree_data()`/`render_knowledge_map()` |
| The authoring editor's structural checks, release logic, GitHub calls | `assets/editor.js` |
| The authoring editor's prose-editing surface itself | `vendor-src/milkdown-entry.js` |
| A vendored library's version | `vendor-src/package.json`, then `npm run build` there |
| Code completion or hover docs, either surface | `vendor-src/codemirror-entry.js` (both surfaces' static sources, plus the extension points); `assets/tutorial-runtime.js` (the runtime's live sources) |
| The curated names the editor's future hover docs would cover | `dev/generate_doc_snippets.py`, then re-run it |
| The tutorial link picker (search-and-insert `tutorial:` links) | `matchTutorials()`/the picker UI in `assets/editor.js`; `insertLink()` in `vendor-src/milkdown-entry.js` |
| What a search box counts as a match — stems, synonyms, prefixes | `assets/search-words.js`, imported by `search.js`, the Reference panel filters in `tutorial-runtime.js`, dewmini's Library and the editor's picker (DECISIONS_LOG 7.174) |
| House styling, both reading pages and the editor | `assets/tutorial-style.css` |
| The reference's assembly logic (what counts as "already covered") | `cumulative_glossary()`/`own_glossary()` in `build.py` |
| What one tutorial's reference actually says | `<slug>.glossary.yaml` beside it, or run `.claude/skills/tutorial-glossary/SKILL.md` on it |
| Highlight-to-look-up (the button a selection offers) | `initReferenceLookup()` in `assets/tutorial-runtime.js`; `.dl-lookup` in `assets/tutorial-style.css` |
| The reference panel or toggle's look and behaviour | `assets/shell.html`, `assets/tutorial-style.css`, `initReference()`/`renderReference()` in `assets/tutorial-runtime.js` |
| *Why* something works the way it does, before you change it | `DECISIONS_LOG.md` (numbered, searchable) |
