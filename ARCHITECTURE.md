# Architecture

This is the other door in — for someone reading the code rather than writing
a tutorial. If you want to write a tutorial, read `docs/WRITING_TUTORIALS.md`
instead; it covers the markdown format, cells, practice pages, versioning, and
the authoring editor from a tutorial writer's side. This document assumes you
have read that, and goes underneath it: how a tutorial's markdown becomes a
page a student can run Python in, what runs where, and how the pieces talk to
each other. `DECISIONS_LOG.md` is the record of *why* a given
piece works the way it does, entry by entry; this document is the map of
*what the pieces are*, so you know where to go looking.

The short version, before the long one: there is no backend. Nothing here is
a server you deploy, a database you migrate, or an API you version. There are
three separate programs, none of which know the others are running:

1. **`build.py`** — a Python script, run once per push by GitHub Actions, that
   turns the markdown in `tutorials/` into the static HTML in `site/`, which
   GitHub Pages then just serves as files.
2. **`assets/tutorial-runtime.js`** — JavaScript that ships inside every built
   page and runs entirely in a *student's* browser tab. It boots a real
   Python interpreter (Pyodide, Python compiled to WebAssembly) client-side
   and executes cells there. No student code ever reaches a server dewlab
   controls, because there is no server for it to reach.
3. **`assets/editor.js`** — JavaScript that ships inside `editor.html` and
   runs entirely in an *author's* browser tab. It reads and writes tutorial
   markdown by calling GitHub's own API directly, using a token the author
   supplies, and opens a pull request. It is a client of GitHub, not a
   client of anything dewlab hosts.

Three programs, three moments, no shared runtime between them. Keeping them
that way is worth protecting: the build never needs to know how a cell
executes, the runtime never needs to know how a tutorial got written, and the
editor never needs either of the other two to be running.

---

## 1. The build: markdown in, static site out

`build.py` is a single script (one file on purpose — see DECISIONS_LOG for why
it was never split) that reads `tutorials/**/*.md` and writes `site/`. It runs
locally when an author previews their work, and it runs again, identically, in
`.github/workflows/deploy.yml` on every push to `main`. `site/` itself is never
committed — it is gitignored, rebuilt from scratch every time, which is what
stops the published pages from ever drifting out of sync with the markdown that
describes them.

A tutorial is a folder, `tutorials/<module>/<slug>/`, holding its markdown at
`<slug>.md`, its practice page, its glossary, any frozen past releases as
`v<version>.md`, and any pictures or recordings it uses. Where a page ends up
is decided by its frontmatter's `module` and `slug`, never by where its source
file sits — which is what let that layout change without moving a single
published URL or storage key.

The pipeline, roughly in the order the code runs it:

1. **Parse frontmatter.** `split_frontmatter()` reads the YAML block at the
   top of a tutorial and validates it — required fields, a version that
   actually looks like `2026.09.15.1`, a `status` from the known set. A
   tutorial that fails this stops the whole build, on purpose: a build that
   silently skips a broken file is a build that ships a stale page nobody
   asked for.

2. **Pull code and maths out before markdown ever sees them.** `extract_blocks()`
   replaces every fenced code block — `exec`-tagged or not — with a numbered
   HTML comment placeholder, and separately records each block as a `Cell`
   (if tagged `exec`, with its `id`/`hint` header parsed off) or a `CodeBlock`
   (if not). `extract_math()` does the same for `$…$` and `$$…$$`. Both exist
   for the same reason: Python's `markdown` library does not know dewlab's
   conventions, and `$a_i + b_j$` run through a generic markdown converter
   comes back with the subscript read as emphasis. Pulling both out first and
   reinserting rendered markup afterward is what keeps a tutorial author from
   ever having to think about escaping.

3. **Convert what's left with `markdown.Markdown()`**, then reinsert. Every
   placeholder gets swapped for its real markup — `render_cell()` for a live
   cell (an empty shell: a CodeMirror mount point, a Run button, an output
   div — nothing about *how* it runs lives here), `render_code_block()` for
   illustrative code (pre-escaped, so it reads correctly even with JavaScript
   off), `render_math()` for a marked span KaTeX will fill in client-side.

4. **Resolve cross-tutorial links and validate structure.** A
   `tutorial:slug#anchor` link becomes a real relative href, or the build
   fails — a dead link is treated as a bug, not a warning. `<img>` without
   `alt` fails the same way. A `<details>` fold without `dl-hint`/`dl-answer`
   fails the same way. This is the build acting as the thing that catches a
   mistake before a student does, and it is the reason `problems()` in
   `editor.js` (§3) exists at all: it is the *same* set of checks, run
   client-side, so an author sees them before committing rather than after
   CI fails.

5. **Assemble navigation.** `series_of()`, `versions_of()`, `practice_pairs()`,
   `archived_of()` read the `.order.yaml` files and each tutorial's
   frontmatter to work out reading order, which release is "current," which
   tutorial a practice page belongs to, and what has been retired. This is
   also where a whole class of authoring mistakes gets caught structurally —
   a slug listed in an order file with no tutorial behind it, a series with
   no order file at all — rather than left to be noticed by a student
   clicking a broken "next" link.

6. **Render into `assets/shell.html`.** Every page — a tutorial, the
   contents page, the topic tree, `editor.html` itself — is the same
   template with `{{TOKEN}}` placeholders substituted. A token the template
   doesn't fill, or a page that doesn't fill every token the template has,
   fails the build. `write_editor_page()` (build.py, search for it) is the
   one that assembles `editor.html` specifically, and it is worth reading
   directly if you are touching the authoring editor, since it is where the
   `<script type="module" src="editor.js">` tag and the vendored Milkdown
   stylesheet actually get wired onto the page.

7. **Write the manifest.** Every page carries a
   `<script type="application/json" id="dewlab-manifest">` with everything
   the client-side runtime needs and cannot otherwise know: the cell list (id,
   starter code, hint), which extra Python packages this tutorial needs
   beyond the default three, whether the page contains maths, and
   content-hashed asset versions. This manifest is the *entire* contract
   between `build.py` and `tutorial-runtime.js` — the two never share code,
   only this one blob of JSON, read once at `readManifest()` (runtime.js) and
   trusted from then on.

Two supporting scripts worth knowing about: `dev/curriculum_map.py`
regenerates `planning/CURRICULUM_MAP.md` from `outcomes.yaml`, `topics.yaml`
and every tutorial's `covers:` frontmatter, and is what the `tests` CI job
runs with `--check` to fail if that map has gone stale. `vendor-src/build-vendor.mjs`
is a separate, one-directory Node project (§4) that produces the committed
`assets/vendor/*.bundle.js` files — CodeMirror, KaTeX, and now Milkdown —
so that neither CI nor an author previewing a tutorial locally needs Node
installed at all for the ordinary case.

---

## 2. The runtime: what a student's browser actually does

`assets/tutorial-runtime.js` is the JavaScript a student loads on every
*tutorial* page (dewmini is a separate page with its own JavaScript —
see §4), and it owns exactly three things, stated in its
own opening comment: the settings panel, the CodeMirror editors for
cells, and booting Pyodide to run one. Deliberately thin on rendering —
everything a cell's *output* looks like is decided in
`assets/tutorial_tools.py`, in Python, so those rules are unit-testable
without a browser and only have to be right in one place.

What happens when a page loads:

- `readManifest()` reads the JSON blob build.py wrote (§1, step 7). If a
  tutorial has no cells at all, Pyodide is never fetched — a prose-and-maths
  page loads instantly, because there is nothing here for it to wait on.
- Each cell gets a CodeMirror instance (`createCodeEditor`, from the vendored
  `codemirror.bundle.js`) mounted over its `.dl-editor` placeholder, seeded
  with the starter code from the manifest, or with whatever the student
  saved last time (`localStorage`, keyed `dewlab:progress:<module>:<slug>`,
  scoped per cell by its stable `id`).
- Pyodide itself boots lazily, on the *first* Run click (`ensureBooted()`),
  not on page load — loading a ~10 MB WebAssembly runtime before a student
  has even decided to run anything would be exactly the kind of cost this
  project exists to avoid paying. `pyodide.loadPackage(manifest.packages)`
  pulls in `numpy`, `pandas`, `matplotlib` by default, or whatever a
  tutorial's `packages:` frontmatter widened that to.

What happens when a student clicks Run (`runCell()`, tutorial-runtime.js):
the button disables, `tools.run_cell(cell.id, outputEl, code)` is called —
`tools` is the Python module `tutorial_tools.py`, imported once into the
Pyodide interpreter and called back into from JavaScript for every run — and
Python takes over the output area for the duration of that call. Anything
printed, the value of a trailing expression, a DataFrame rendered as a real
table, a matplotlib figure captured as a transparent PNG, a traceback trimmed
to the student's own line: all of that is decided inside
`tutorial_tools.py`, not in JavaScript, which is why that file's own tests
(`tests/test_tutorial_tools.py`) can check rendering behaviour under plain
CPython with no browser at all. When the call returns, the runtime saves the
cell's code and output to `localStorage` — after the run, not during it, so
what's persisted is what the student actually finished looking at.

Everything a Pyodide-backed cell can call beyond ordinary Python is defined
once, in `tutorial_tools.py`, and listed there in `__all__`.
`docs/WRITING_TUTORIALS.md`'s "What your cells can call" table is the
reader-facing description of the same set. If you are changing what a cell can
do, that file is where you start; if you are changing what a cell *looks
like*, `tutorial-runtime.js` is.

Two more pieces worth knowing where they live: `assets/tree.js` draws the
topic-tree and knowledge-map SVGs from data `build.py` computes and embeds
(`tree_data()`), and `vendor-src/build-vendor.mjs` also produces
`assets/vendor/standalone.bundle.js` — the entire runtime rebuilt as one
classic script rather than an ES module, which is what a **Download to
keep** file actually runs, since a page opened via `file://` cannot load a
module.

**Code intelligence** — completion and hover docs — is layered onto every
cell's CodeMirror instance in `vendor-src/codemirror-entry.js`, and it is
worth knowing which part is static and which is live. Keyword/builtin
completion and completion on names already typed in the cell
(`@codemirror/lang-python`'s `globalCompletion`/`localCompletionSource`) are
static: no interpreter involved, available the instant a cell mounts.
Layered on top, `tutorial-runtime.js`'s `pageNamesCompletion` and `docFor`
are live — they read `tutorial_tools._page_globals`, the exact dict every
cell actually executes against, and call `inspect.getdoc()` on a real object
sitting in it. Both are plain functions passed into `createCodeEditor()` and
each checks for a booted interpreter itself, at call time, rather than
needing to be reconfigured once boot finishes — a page left open through a
boot just starts offering real completions and real docs. See
DECISIONS_LOG.md 7.60 for what this looked like to build and what it does
and does not cover (Python builtins are deliberately out of scope for
`docFor` — see that entry for why).

**The reference** (`planning/REFERENCE_PANEL.md`, DECISIONS_LOG.md 7.64) is
the settings panel's sibling, not a separate subsystem: same floating-card
positioning, same open/close mechanics, mutually exclusive with it at
runtime because both anchor to the same corner. Its content is not
hand-written — `build.py`'s `cumulative_glossary()` assembles it per
tutorial from `<slug>.glossary.yaml` files (one per tutorial, produced by
`.claude/skills/tutorial-glossary/SKILL.md`), walking each series in
`<series>.order.yaml` order — and, where a module's `series.yaml` says so
(`series_chain()`, DECISIONS_LOG.md 7.66), every earlier series in that
module too — so a tutorial's manifest only ever carries what it and
everything before it actually taught, never anything from another module. A
tutorial with nothing accumulated
yet shows no toggle at all — the skill has now been run across every
tutorial in both live modules (DECISIONS_LOG.md 7.65), so in practice this
only affects a genuinely new tutorial before its own glossary file is
written, or one whose glossary is deliberately empty (see 7.65 for why a
few tutorials keep an explicit `entries: []` rather than no file).

---

## 3. The authoring editor: a GitHub client, not a server client

`editor.html` is never linked from a student page. It exists for the two
people who write tutorials, and everything about it follows from one fact:
**it has nowhere to send a change except GitHub itself.** There is no
dewlab-hosted API it talks to. `assets/editor.js`'s `githubClient()`
wraps GitHub's REST and Git Data APIs directly — list the tree at
`main`, read a blob, create blobs and a tree and a commit, push a branch, open
a **draft** pull request — using a fine-grained personal access token the
author pastes in once (`gate()`), which is then kept in that browser's own
`localStorage` and nowhere else. The token needs exactly two things:
`contents: write` and `pull requests: write`, scoped to `deweydex/dewlab`,
and nothing broader. That scope, not a login system, *is* the access model:
becoming someone who can propose a change to dewlab means someone with
GitHub admin rights on the repository issues them a token with those two
permissions (GitHub's own collaborator settings decide who that can be —
there is nothing in this codebase that manages who counts as an editor). The
token can propose commits; it cannot merge them. Every change the editor
makes lands as a draft PR against `main`, which still goes through whatever
review the repository already requires — the tool automates the git
mechanics of proposing a change, not the judgement of accepting one.

What the editor actually holds in memory (`start()`'s `state` object): every
file under `tutorials/` fetched once at load, both as a mutable working copy
(`state.files`) and an untouched original (`state.original`) — releasing
needs both, because freezing a release from the *edited* buffer rather than
the original would make the frozen copy a lie about what students actually
had. `state.dirty` and `state.removing` track exactly which paths a commit
needs to touch, so that, say, reordering one series never touches the
sixty-odd files it didn't change.

**The prose surface — as of this document, a real change from what shipped
before it.** Until now, the body of a tutorial was edited in a plain
`<textarea>`, despite `planning/REPO_AND_EDITOR.md` having specified a
Milkdown-based block editor from the start. That gap is closed:
`editorView()` now mounts `createProseEditor()` (`vendor-src/milkdown-entry.js`),
a thin wrapper around Milkdown's Crepe preset — the same block-editing engine
the `deweydex/faq` repository uses, in dewlab's case with no framework
underneath it at all. Crepe's own API is plain JavaScript; FAQ only wraps it
in Preact because FAQ itself is a Preact app. Vendored the same way
CodeMirror and KaTeX already were — `npm run build` inside `vendor-src/`
bundles it with esbuild into `assets/vendor/milkdown.bundle.js` (+ a sibling
`.css`), committed to the repo, so an author previewing locally and CI both
still need no Node install for the ordinary case. `.github/workflows/tests.yml`'s
`standalone-bundle-is-current` job is what catches a committed vendor bundle
going stale against `vendor-src/`.

Two things about that integration are worth knowing if you touch it:

- **Crepe reads its document once, at construction, and cannot swap it in
  place.** There is no `setValue`. Loading different content — switching
  which tutorial is open, or (in the test suite) driving the editor
  programmatically — means destroying the instance and creating a new one,
  which is exactly what `render()` already does on every state change
  (`root.replaceChildren()`); the only addition was tearing down the
  previous Crepe instance first (`state.editor.destroy()`) so a switch
  doesn't leak the old one. `globalThis.dewlabEditor.setBody(markdown)`
  drives this path.

- **Crepe's code-block feature keeps only the first word of a fence's info
  string as its "language."** dewlab's own convention repurposes that string
  to mean two things at once — `python` for syntax highlighting, ` exec` for
  "this is a runnable cell" — and Crepe's language picker has no way to
  preserve the second word. Round-tripped through Crepe unmodified, every
  `python exec` cell would silently come back as `python`, i.e. inert
  illustrative code, the moment an author saved through this editor.
  `restoreExecTag()` (`assets/editor.js`) fixes this on the way out, on the
  same signal `build.py` itself uses to mean a fence is a cell: an `id:`
  line as the very first thing inside it. This was caught by actually
  driving the editor in a real browser during this change, not by reading
  the library's docs — a reminder that a rich-text editor's markdown
  round-trip is exactly the kind of thing worth checking live rather than
  assuming, before trusting it with a tutorial's cells.

The structural report (`problems()`, the same checks `build.py` would fail
on, run here before a commit rather than after CI) also checks cross-tutorial
links now — `tutorialLinkProblems()` validates every `tutorial:slug#anchor`
against every other tutorial's real slugs and headings (`tutorialAnchors()`,
which reproduces Python-Markdown's toc heading-id algorithm in JavaScript,
checked directly against a real `markdown.Markdown(extensions=["toc"])` run
rather than guessed at). The cell-id-rename warning (`renamedCells()`, the
one thing the editor knows that the build cannot, because by the time the
build runs the rename has already happened) and the release mechanism
(`release()`: freeze what students have, publish the buffer as a new dated
version beside it) are unchanged by any of this. `assets/editor.js`'s own
comments describe all of it well enough that this document won't repeat
them — start there if you're changing that logic; start in
`vendor-src/milkdown-entry.js` if you're changing what the prose surface
itself can do, including its code blocks' own completion (the same static
sources §2 describes for a student's cells, minus the live layer — the
editor has no interpreter to read from). DECISIONS_LOG.md 7.60 also records
an attempt at a hover-docstring tooltip for the editor's code blocks,
specifically, that did not work and was pulled back out — worth reading
before trying it again.

The report catches a dead link after it is typed; the link picker
(`matchTutorials()`, the toggle above the prose editor) is the other half —
search every tutorial by title, slug or module, then insert
`[title](tutorial:slug#anchor)` at the cursor without typing a slug from
memory in the first place. Insertion is `insertLink(title, href)`
(`vendor-src/milkdown-entry.js`), and it does not go through
`@milkdown/utils`'s own `insert()` helper: that helper's inline path
round-trips the parsed link through a real DOM node before inserting it,
and the commonmark preset's link `toDOM` sanitizes `href` to empty for any
scheme outside http/https/mailto/tel/ftp — which silently stripped
`tutorial:` before the round trip's second half ever read it back.
`insertLink` builds the text node and its link mark directly against the
schema, with no DOM in between, and calls `replaceSelectionWith(node,
false)` — `inheritMarks: true` (the default) replaces a node's own marks
with whatever marks are active at the cursor, which is empty in the common
case and silently dropped the link mark the node exists to carry. Both were
found by asserting on the markdown `getBody()` actually produced in
`tests/e2e/test_editor.py`'s `TestLinkPicker`, not by reading past either
call's default behaviour and assuming it was fine.

Importing only Crepe's structural stylesheet, not one of its skins (this
section's opening paragraph, and the comment above `.dl-editor-body
.milkdown` in `tutorial-style.css`), turned out to have a real gap: the
structural stylesheet reads roughly two dozen `--crepe-color-*`/`--crepe-
font-*`/`--crepe-shadow-*` custom properties that only a skin defines, and
with none loaded they were simply undefined — silently producing a fully
transparent slash menu and no visible text cursor at all, not merely wrong
colours. `tutorial-style.css` now defines that whole set once, mapped to
the matching `--dl-*` token, rather than hand-patching each broken consumer
as found. DECISIONS_LOG.md 7.63 has the full account, including a second,
unrelated bug (a CSS comment closed early by its own text) that made the
first attempt at this fix silently do nothing.

---

## 4. dewmini: a Python workspace outside any tutorial

`compose/dewmini.html` is not a tutorial — no markdown source, nothing
`build.py` generates from `tutorials/`. It's a plain page built
directly, giving a student a place to write and run Python that isn't
tied to one lesson. It shares `tutorial_tools.py` with every tutorial
page (§2), so `show`/`show_table`/`check`/widgets all behave identically
everywhere.

`compose/dewmini.js` runs Python through `assets/pyodide-engine.js`, a
shared client of `assets/pyodide-worker.js` — the same Worker-based
runtime a tutorial page's own `tutorial-runtime.js` boots (§2), reused
rather than duplicated. That's what gives dewmini a genuine Stop button:
a runaway cell blocks the Worker, not the page. `pyodide-engine.js` is
its own module rather than part of `dewmini.js` because 700 lines of
tricky Worker/interrupt logic deserve their own file, decoupled from
the page's markup — see that file's own top comment.
`compose/dewmini-fs.js` sits between dewmini and
the actual filesystem, delegating every primitive (mount, list, read,
write, delete) to the shared engine and choosing among three backends —
a real local folder via the File System Access API, its own named OPFS
subdirectory, or IDBFS — so the
file manager, SQL support (`sqlite3` against a mounted `.db` file), and
uploads all work without knowing which backend is active. Opened from
`file://` — which dewmini's own downloadable copy (see below) avoids
by serving itself from `http://localhost` instead, since a browser
blocks the page's own `import` statements from a bare file entirely,
not just the Worker specifically — a module Worker isn't reliably
available either, so `pyodide-engine.js` falls back to running Pyodide
on the main thread when it is reachable at all: same interpreter, same
`tutorial_tools.py`, just without a genuine Stop button.

A JavaScript cell (`DECISIONS_LOG.md` 7.119) runs through neither of
those — `compose/js-cell-engine.js` is a second, much smaller engine of
its own: one persistent sandboxed `<iframe sandbox="allow-scripts">` per
notebook, with no Worker at all, since a sandboxed iframe with no
`allow-same-origin` is already a separate, isolated realm and every
browser already has a JS engine sitting inside it. A SQL cell, by
contrast, needs no engine of its own: `compose/dewmini.js` generates a
call to `tutorial_tools.py`'s own `_run_sql_cell()` against a shared
`sqlite3` connection (`db`) and runs it through `pyodide-engine.js` like
any other Python code — SQL and Python share one engine; only
JavaScript gets a second.

**dewmini is a workbench, not one column** (`DECISIONS_LOG.md` 7.99;
design and reasoning in `planning/DEWMINI_WORKBENCH.md`). Notebooks open
in tabs — `notebooks[]` in `dewmini.js`, with `cells` re-pointed at
whichever is active rather than every function being routed through an
index — and two docked rails sit either side of them: a **Workbench**
(left) carrying a live variable inspector, notes and a real file
manager, and a **Library** (right) carrying the cross-tutorial
reference, a dataset catalogue and the help text, with Settings sharing
that right edge (`DECISIONS_LOG.md` 7.99, 7.121 — the sides swapped
after the layout first shipped).

A tab need not hold a notebook of cells at all. Files' own file manager
(`openWorkspaceFile()`) can open a real workspace file directly: a `.py`
as one editor, a `.ipynb` as cells, and an `.html` as a small website —
its own editor split-screen against a live sandboxed preview, discovering
whatever `.css`/`.js` of the same base name sit beside it rather than
requiring three fixed names (`DECISIONS_LOG.md` 7.121,
`planning/DEWMINI_WORKBENCH.md` §10).

Two pieces of that reach outside `compose/`. `write_reference_index()`
in `build.py` emits `assets/reference-index.json`, the union of every
tutorial's glossary — deliberately dropping the "never show what has not
been taught" rule the tutorial pages' own Reference is built around,
since a workspace has no position in a series to protect. And
`tutorial_tools.describe_globals()` walks `_page_globals` and returns
plain `{name, type, summary, kind}` data, reached through the engine's
`describeGlobals()` and a `describe-globals` worker message — the same
shape as the existing `page-names` path, and in Python rather than
JavaScript so it is unit-testable without a browser.

The rails themselves needed almost no new mechanism: `tutorial-style.css`
has carried `data-dl-panel-left`/`-right` with independent width
variables since 7.83, and dewmini had been overriding it with a
single-panel simplification that was right while both its panels docked
right (7.84). Deleting that override *is* the two-rail layout.

Each of these files has its own `docs/<file>-explained.md` walking
through its internal structure in more depth than belongs here — start
with [`docs/pyodide-engine-explained.md`](docs/pyodide-engine-explained.md)
for the worker/main-thread split specifically, or
[`docs/dewmini-js-explained.md`](docs/dewmini-js-explained.md) for the
rest of dewmini (cell CRUD, drag reorder, the standalone HTML export
that builds an entire second page as a string).

**dewmini has a downloadable, offline-capable copy**
(`write_dewmini_bundle()`, `build.py`; `DECISIONS_LOG.md` 7.92) —
it mirrors the hosted site's own `compose/`/`assets/`/`data/` folder
shape rather than flattening, since `compose/dewmini.html`'s own
relative paths already assume that shape and rewriting them was exactly
the risk 7.89's real bug came from. The bundle ships a *serve.py*:
a browser blocks the `import` statements this codebase's JavaScript is
built from when a page is opened straight off disk (no origin for a
CORS check to approve), so the bundle can't just be double-clicked —
*serve.py* is a zero-dependency wrapper around `http.server` that
serves the unzipped folder to `localhost` instead, found necessary by
actually opening a built bundle the way a downloader would, not assumed
from the code.

---

## 5. Two build systems, on purpose

There are two separate `package.json`s in this repository, and that split is
deliberate rather than an accident of history:

- **`vendor-src/`** exists purely to produce `assets/vendor/`. It is never
  run in CI's main `tests` job, never run by an author building tutorials,
  and its output — not its source — is what everything else in the
  repository depends on. Run `npm install && npm run build` inside it only
  when a pin in `vendor-src/package.json` changes, then commit the result in
  `assets/vendor/`.
- **`build.py`** and everything under `tutorials/`, `assets/*.py`, `data/`,
  `setup/` need nothing but Python. `requirements-build.txt` is the entire
  dependency list for building and reading tutorials.

The practical upshot: cloning this repository and running
`python3 build.py` works with no Node installed at all, because the only
things that would have needed Node are already sitting in `assets/vendor/`
as plain JavaScript. Node is a tool for updating three vendored libraries,
not a dependency of the project.

---

## 6. Tests: what each suite actually checks

```
python3 -m pytest                    everything
python3 -m pytest tests --ignore=tests/e2e   the fast ones, no browser
```

- **`tests/test_*.py`** — unit tests, no browser, no Pyodide. Mostly
  `build.py`'s own logic (`test_build.py`) and `tutorial_tools.py`'s
  rendering rules under plain CPython (`test_tutorial_tools.py`). This is
  what CI's `tests` job runs on every push and PR.
- **`tests/e2e/test_editor.py`** — the authoring editor, driven with
  Playwright against a **fake** GitHub client injected in-page (see
  `FAKE_CLIENT` at the top of that file) — nothing here touches the network
  or needs a token, which is the whole reason the client is a parameter to
  `start()` rather than hardwired. Since the prose editor is a real block
  editor and not a `<textarea>`, these tests don't `fill()` it directly —
  see `globalThis.dewlabEditor`'s `getBody()` / `setBody()` / `editBody()`,
  documented at their definitions in `editor.js`, which is what a script
  drives instead.
- **`tests/e2e/test_*.py`** (the rest) — a real Chromium against a real,
  self-hosted Pyodide, built from `tests/e2e/fixture/rendering-tour.md` by an actual
  `build.py` run rather than a stand-in for one, so a change that breaks
  the markup a student receives fails here specifically. Needs
  `pip install playwright && playwright install chromium` and
  `python3 dev/fetch_pyodide.py` (~30 MB) first; skips with a message if
  either is missing, rather than failing.

None of the e2e suite runs in CI (see the comment at the top of
`tests.yml`) — it is a local, manual check, run before a PR that touches the
runtime or the editor.

---

## Where to start, by what you're changing

| Changing… | Start in |
|---|---|
| What a tutorial's markdown can express (a new frontmatter field, a new fence convention) | `build.py` |
| What a cell can do (a new tutorial-facing function) | `assets/tutorial_tools.py` |
| What a cell *looks like*, or the settings panel, save/restore behaviour | `assets/tutorial-runtime.js` |
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
| House styling, both reading pages and the editor | `assets/tutorial-style.css` |
| The reference's assembly logic (what counts as "already covered") | `cumulative_glossary()`/`own_glossary()` in `build.py` |
| What one tutorial's reference actually says | `<slug>.glossary.yaml` beside it, or run `.claude/skills/tutorial-glossary/SKILL.md` on it |
| Highlight-to-look-up (the button a selection offers) | `initReferenceLookup()` in `assets/tutorial-runtime.js`; `.dl-lookup` in `assets/tutorial-style.css` |
| The reference panel or toggle's look and behaviour | `assets/shell.html`, `assets/tutorial-style.css`, `initReference()`/`renderReference()` in `assets/tutorial-runtime.js` |
| *Why* something works the way it does, before you change it | `DECISIONS_LOG.md` (numbered, searchable) |
