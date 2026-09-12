# dewmini as a workbench: two rails, tabs, and tools for looking at your own work

dewmini gains two docked side panels, tabbed notebooks, a reference with
search and filters, a variable inspector, and dataset import. Widgets are
the one capability gap and stay deferred.

This document is the design.

---

## 1. The tension worth naming first

dewmini's earlier documents treat smallness as the point — `MINI_IDE_AND_DEWMINI_NEXT.md`
§3 found "nothing that makes it bigger" — because dewmini used to be the
small tool next to a larger sibling. That sibling (Mini IDE) is retired.
dewmini is now the only place a student writes Python outside a tutorial,
and the only place a project can grow, so it cannot also refuse to grow.

The rule that replaces the old smallness discipline:

> **Quiet by default, everything one press away.**

Nothing new opens on a first visit. The notebook keeps the middle of the
screen and its full width until a reader asks for something else. Someone
who came to check `6 * 7` sees a heading, a toolbar, and a cell — exactly
what they see today. Someone building a project opens both rails and has
a workbench. The capability is additive; the weight is opt-in.

---

## 2. What goes where, and why

Three panels across two edges, replacing today's two-on-one-edge, divided
by subject: the left panel describes the project the student is working
on, the right holds what is outside it.

**Left — Workbench (`#dm-workbench`). The project.**
Files, variables and notes — what a student opens with a question about
the work in front of them.

**Right — Library (`#dm-library`). Everything outside the project.**
Reference, data and help — what a student opens with a question about the
world outside their notebook.

**Right — Settings (`#dl-settings`). Configuration, demoted.**
Still docked right, but no longer the headline; Notes and Files moved out
of it into the Workbench and Library.

The two right-docked panels are mutually exclusive, since they share an
edge; the left one is independent, so a reader can have the reference
open beside their own files. The shared stylesheet already supports this
(`data-dl-panel-left`/`data-dl-panel-right`, independent width variables,
`DECISIONS_LOG.md` 7.83) — dewmini had overridden it with a single-panel
simplification (7.84) that no longer applies now both its panels don't
dock to the same edge.

Help is a Library section rather than its own panel, per
`SIDEBAR_CONTENT.md` §4: extend a panel rather than add one. Three
toggles, not four.

---

## 3. Tabs

`cells` — a module-level array — becomes one notebook among several.
Storage moves from `dewmini:cells:v1` (a bare array) to
`dewmini:notebooks:v1` (`{active, notebooks: [{id, name, cells}]}`), with
a one-way migration that folds any existing saved array into a first
notebook called "Notebook". That migration is tested.

Each notebook carries its own name, which is also its export filename, so
"Keep a copy" downloads the tab you are looking at under its own name.

**One Python session, shared by every tab — deliberately.** Real Jupyter
gives each notebook its own kernel; dewmini has one interpreter, and a
namespace per tab would mean threading a namespace identifier through
every engine call and across the worker boundary — a change to the
shared engine, which `DECISIONS_LOG.md` 7.97 established touches every
surface that runs Python. Instead the sharing is made visible: the
Variables section shows one namespace and says so in plain words. A
student who defines `data` in one tab and finds it in another has been
told, and can see why. If that turns out to confuse people, a per-tab
namespace is the fix.

---

## 4. The reference, and the constraint it deliberately drops

The tutorial pages' Reference panel is assembled per page under one hard
rule (`REFERENCE_PANEL.md` §1): never show a reader something they have
not been taught yet.

dewmini's reference **drops that rule**. The rule protects a reader's
position in a curriculum sequence; a student in an open workspace has no
such position — that is what the workspace *is*. So dewmini shows the
union of every term from every tutorial's glossary, deduplicated on
`(term, kind)` — 248 entries today, from 43 glossary files — grouped by
the five kinds the schema defines (concept, function, operator, formula,
keyword), with search across both terms and definitions. Category
navigation and search make 248 entries navigable rather than a wall.

Each entry names the tutorial that introduced it but does **not** link to
it: this file ships inside dewmini's offline bundle, which carries no
tutorials, so a link would 404 for every offline reader.

Generated at build time into `assets/reference-index.json` by
`write_reference_index()`, from the same `own_glossary()` the tutorial
pages use — one source of truth, so a glossary edit reaches both
surfaces.

**Settled (`DECISIONS_LOG.md` 7.104):** dewmini has no way of knowing
what a student has been taught, so hiding two-thirds of the reference
would mean guessing that, wrongly, against someone who may have finished
the whole course. What would reopen this is not dewmini becoming more
curriculum-shaped, but dewmini gaining a way to know where a reader is —
which would mean tracking readers, refused here on separate grounds.

### 4a. The filters, and why none of them is a field anyone maintains

Four facets, each read off data that exists for another purpose, so none
needs hand-maintenance and none can drift from the tree it describes:

| Facet | Read from | Consequence |
|---|---|---|
| Subject | the outcome prefixes in a tutorial's `covers:` | MIT is maths; PDP and CMPS are computing |
| Level | `topic_tiers()` — prerequisite depth of the `needs:` graph | editing the tree re-files the search |
| Topic | `topic-groups.yaml` | a new group gets a chip without a code change |
| Kind | the glossary schema | unchanged |

Level uses the **deepest** outcome a tutorial covers, not the shallowest
— the shallowest rates a tutorial by its easiest moment, which put 150 of
222 terms in "beginner" and would tell a student in week one that a
tutorial needing four layers of groundwork is approachable.

Subject and level sit on the surface; topic and kind fold into a
`<details>` that expands **in flow**, pushing the results down rather
than covering them, and reports what is on inside its summary — a folded
row that is silently filtering is a trap.

`DECISIONS_LOG.md` 7.101 has the band cut-points.

---

## 5. Variables, and why an inspector is a teaching tool

Without one, a student runs a cell, something happens, and the only
evidence is whatever they remembered to print — a variable that exists
but was never printed is invisible.

The Workbench's Variables section lists what is in the session — name,
type, and a one-line summary (a DataFrame's shape, a list's length, a
number's value) — refreshed after every run, with a student's own data
separated from the functions and modules that share the namespace.

The introspection is Python (`describe_globals()` in
`tutorial_tools.py`), not JavaScript: it is where `_page_globals` lives,
it returns only strings so nothing crosses the worker boundary as a
proxy, and it is unit-testable under plain CPython.

---

## 6. Data, and one thing this environment could not verify

The catalogue (`compose/data-catalogue.json`) lists datasets with their
real source, licence and description, and inserts working starter code
into the notebook when picked. It covers the three datasets already in
`data/`, and a curated set of Our World in Data releases.

**The remote half carries a caveat.** A browser only fetches a file from
another site if that site permits it (CORS). Our World in Data's CSV
endpoints are widely used from browsers and are expected to permit it,
but this was built in a sandbox whose network policy blocks
`ourworldindata.org` outright, so the fetch could not be tried even once
— and this repository has twice shipped an untested network claim before
(`DECISIONS_LOG.md` 7.92), so it isn't happening a third time.

`load_csv()` now accepts a full URL as well as a local name; when a
remote fetch fails it raises an error explaining that the other site has
to allow it, and that the reliable route is to download the file and add
it through the Workbench's Files section. `tests/MANUAL_CHECKLIST.md`
carries the one check nobody here could run: open dewmini on a real
network, pick a remote dataset, and see which way it goes.

---

## 7. Smaller things, from the same review

- **Undo for a destructive import.** Picking an `.ipynb` used to replace
  the whole notebook with no confirmation and no way back. Imports now
  land in a *new tab* instead — better than a confirmation dialog, and
  something tabs make possible.
- **Shift+Enter runs and advances**, matching every notebook tool a
  student will meet later; Ctrl/Cmd+Enter runs in place.
- **Find and replace** in the editor, which CodeMirror has always
  supported and dewmini had never wired up.

---

## 8. Deliberately not done

- **Widgets off the main thread** — the real capability gap, deferred by
  instruction. `text_input`, `dropdown`, `button` and `image_input` still
  raise on the hosted page.
- **A namespace per tab** — §3.
- **`micropip` package installation** — the next ceiling a self-directed
  project hits.
- **Notebooks saved into the mounted filesystem** — they remain in
  browser storage. Tabs make this more attractive, not less.

---

## 9. What was verified, and how

1. **Unit tests.** `describe_globals()` over every type it claims to
   summarise, including a value whose `__repr__` raises; and
   `write_reference_index()`'s union, deduplication, sorting, and its
   presence in the offline bundle.
2. **A real build.** `python3 build.py --clean`, with the index emitted
   (248 entries) and the bundle carrying it.
3. **A real browser.** Twelve tests in
   `tests/e2e/test_dewmini_workbench.py` drive Chromium against a
   self-hosted Pyodide: tabs keeping their own cells across a switch, the
   migration from pre-tabs storage, both rails open at once, same-edge
   panels excluding each other, a rail surviving a click on your own
   code, reference search and kind filters, a dataset writing its own
   cell, and the inspector reading variables out of live Python.
4. **The downloaded bundle, served and opened** the way a student would
   — 248 terms, six datasets, no failed requests.
5. **Two screen widths**, by screenshot: 1440px with both rails open, and
   375px, where the rails become bottom sheets and nothing scrolls
   sideways.

Two things this could not verify: remote dataset fetching (§6, and
`tests/MANUAL_CHECKLIST.md`), and two pre-existing `test_stop_button.py`
failures — an interrupt timing out under this sandbox's CPU, not a
regression.

---

## 10. Site: an `.html` file opens as a small website (added later, `DECISIONS_LOG.md` 7.121)

Once the notebook's own HTML/CSS/JavaScript cell types existed, the
obvious follow-on was serving them together, the way a real static site
is three real files rather than three cells.

**A tab kind, not a fourth panel.** The first design put three fixed
editors in their own Workbench section; it was thrown away before it was
committed, once Files (§2) already had `openWorkspaceFile()`, which opens
a real file into a tab of its own with a debounced write back to the file
it came from — a second copy of that mechanism would be duplication, not
a feature. Site is instead a third value of `VIEWS`, alongside `CELLS`
and `FILE`. Opening an `.html` from Files opens it as a site the same way
opening a `.py` opens it as a file.

**No fixed three files.** An `.html` file pairs with a `.css` and a `.js`
that share its own base name — not three fixed names — and neither has to
exist. Files' own flat list (§2) shows these as the ordinary files they
are, unlike the first design's now-abandoned `site/` subfolder.

**Split screen, not a Render button.** Editors on one side, a live
sandboxed `<iframe sandbox="allow-scripts">` on the other (the same
isolation the Web cell already uses), updating on every keystroke. A Web
cell's Render button suits a notebook cell answering a one-shot question;
a site is what a reader keeps looking at continuously while they build
it, closer to an ordinary code-and-preview IDE than to a cell.

Verified in a real browser: opening an `.html` from Files renders a
split-screen tab reflecting its real content; a same-base-name `.css`/
`.js` pair opens beside it, including a script mutating the DOM the HTML
half produced; a lone `.html` with no siblings still opens; typing in any
pane updates the preview without a separate press; the CSS and JS halves
each write back to their own file, readable from a Python cell in
another tab; the toolbar's cell-only controls hide for a site tab and
reappear on a notebook tab; and a site tab survives a full page reload.

**Added later (`DECISIONS_LOG.md` 7.134): a console, and Run for
JavaScript.** The right-hand column is now the preview with a console
under it: what the site's script printed, and every uncaught error with
the pane and line it came from, a Go to line button, and a plain-language
second line for the common errors. HTML and CSS stay live; the
JavaScript pane runs on Run or Ctrl/Cmd+Enter, and the preview keeps the
last-run script until then. Ported in shape from dewstack's site editor,
where the pair was decided first.
