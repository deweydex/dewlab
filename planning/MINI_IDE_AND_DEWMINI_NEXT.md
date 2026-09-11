# Mini IDE and dewmini: what's next, and whether they should become one thing

Written after a working session that fixed Mini IDE's output-rendering bug,
added several features to both IDEs, and raised the question of whether they
should merge.

Short answer: **no, not a merger of the two experiences a student chooses
between — but yes, more sharing of the code underneath them than existed at
the time.** The reasoning is in [§4](#4-the-merger-question).

**Superseded, directly, by the person this recommendation was written
for — see the addendum after §5.** §4's reasoning stands as written (it
was correct given what it was weighing), but the actual decision went the
other way: not a "two modes in one page" merger — §4 is right that this
loses more than it gains — but dewmini adopting all of Mini IDE's
capabilities while keeping its own smaller style, with Mini IDE retiring
once that parity was reached. See the addendum for what changed and why
it is a different question from §4's, not a contradiction of it.

---

## 1. Where things actually stand

`planning/MINI_IDE_REDESIGN.md` shipped all eight of its phases: Mini IDE
runs Pyodide in a Worker (real Stop button, real autocomplete), has a
file manager, SQLite via `run_query()`, `.ipynb`/`.py` import and export,
and a folder-based offline distribution. dewmini stayed deliberately
smaller — main-thread Pyodide (no Stop button, by design), one file, no
file manager — with its own additions: `sqlite3` and Pillow in its
default packages, a practice-problem bank, student-authored
documentation-cell images.

This session, in one pass: fixed Mini IDE's output-rendering bug (a
static `.empty` CSS class never cleared after a cell's first run —
dewmini didn't have this bug, since its own code already removed and
re-added the equivalent class correctly); added to both a non-destructive
per-cell and toolbar "reset output", a run-time stat under each cell's
output, an idle-state rail without a permanent grey line, a two-click
"arm then confirm" delete, and a Jupyter-import compatibility scanner
that flags magic commands, shell escapes, and structurally-impossible
imports (`tkinter`, `subprocess`); shipped dewlab's first real datasets
(`co2-emissions.csv`, `life-expectancy.csv`, `pride-and-prejudice.txt`)
and four worked-example notebooks; fixed a site-wide Texture "Size"
slider bug and the desktop side-panel-covers-content problem; and settled
on **Reference** as the panel's name across code, tests and docs, with
its own in-panel search and a new cross-tutorial search on the contents
and topic pages.

None of that is a foundation problem anymore. What's left is feature and
polish work, not architecture repair.

---

## 2. Mini IDE: what's still worth building

**A real "download once, work locally" story, tested, not assumed.**
Phase 7 of the redesign vendors Pyodide for the offline export, but
nothing proves the downloaded folder actually boots with the network
disconnected on a fresh machine — worth a standing manual check before
every release, or a CI job that serves the built folder from a loopback
address with outbound network blocked.

**Multiple simultaneous files, properly.** The file manager can hold many
files, but only one notebook is "the" notebook at a time — no way to have
two `.py` scripts, or a notebook and a `.db` file, open as tabs the way a
real local IDE would. The single feature most likely to matter as a
project actually grows past one file.

**A genuine multi-cursor / find-and-replace inside the editor.**
CodeMirror supports both; neither is wired up.

**Package installation beyond the fixed set.** Pyodide supports
`micropip` for pure-Python packages already on PyPI — worth a Settings
section gated behind a clear warning that anything needing a C extension
without a pre-built wheel simply won't install.

**Collaborative or shareable state.** Everything lives in one browser,
the right privacy default (`OPEN_QUESTIONS.md` #17) — but a lightweight
"export a shareable link" for a single cell's code (not the whole
notebook) would let a reader ask for help on one thing without exporting
a whole file.

---

## 3. dewmini: what's still worth building

**Nothing that makes it bigger.** dewmini is deliberately the smaller,
quieter sibling, and every feature below is evaluated against "does this
still feel like a five-second tool for one calculation," not "does this
catch up to Mini IDE."

**The Stop button gap, if it turns out to matter.** dewmini runs Python
on the main thread on purpose — the Worker migration Mini IDE went
through is real architectural cost (`planning/CELL_CONTROLS.md` §2). If
reports of students getting stuck on a runaway `while True` pile up, that
migration is the answer. Until then, correctly deferred, not neglected.

**A quieter, dewmini-scoped version of the two site-wide fixes this
session made.** If dewmini ever grows a third panel the way tutorial
pages have, the same pattern is already proven and cheap to extend.

**Nothing else.** A short list is the right length for a tool whose whole
design point is staying short.

---

## 4. The merger question

Could Mini IDE and dewmini become one tool? Mechanically, yes. Whether
it's better for a student is no, because **dewmini's whole design point
is not being Mini IDE.** What `docs/DEWMINI.md` describes — somewhere to
run a few lines that isn't tied to one topic, reachable in effectively no
clicks, nothing to configure before typing code — is a real, different
use case from "a project meant to stand on its own," not a smaller
version of the same one. Merging the tools that serve these two students
either:

- **forces the quick-check student through the bigger tool's own
  weight** — a file manager they don't need, a wider settings panel, a
  concept ("this is a whole workspace with files in it") that gets in the
  way of "I just want to try this one line," or
- **keeps two modes inside one tool, switched by a setting or a URL
  parameter** — a merger in name only: the code shares a shell, but a
  student still picks a mode, the UI still has to explain the
  difference, and a state-migration problem appears (what happens to a
  dewmini-mode notebook's cells if a reader flips to Mini-IDE-mode?) that
  doesn't exist today because they're just two pages.

Neither outcome beats what exists: two pages, one link between them
("Outgrowing a quick notebook?"), no decision to make until outgrowing it
is a real, felt thing.

**What genuinely is worth doing, and is a real form of "merging," is
sharing more of the code underneath the two pages.** The codebase's
stated convention — "each page owns a thin copy rather than a shared
runtime module," per `pyodide-engine.js`'s own comment — made sense when
there was one page. With three surfaces now running overlapping logic
(tutorial pages, Mini IDE, dewmini), and this session adding a fourth
near-duplicate pass (`scanPyodideCompatibility()`,
`armDeleteButton()`/`disarmDeleteButton()`, `applyImportedCells()`, each
written twice), the balance has shifted:

- **Keep duplicating** (the status quo). Every page stays fully
  independent — at the cost of every shared fix needing to land twice, by
  hand, with the same drift risk Mini IDE's output-visibility bug shows.
- **Extract a genuinely shared module** for pieces that are pure logic
  with no page-specific DOM assumptions — `scanPyodideCompatibility()` is
  the cleanest candidate (takes an array of plain cell objects, returns
  an array of strings, touches no DOM) — imported by both pages rather
  than pasted into both.

The second option is the recommendation, done gradually: the next time a
shared fix needs to land in both places, extract that piece into a
shared module instead of copying it a third time, and let the shared
layer grow function by function. `assets/tutorial_tools.py` is already
this pattern on the Python side.

---

## 5. If picking one thing to do next

In order, by how much a student would actually notice:

1. **Mini IDE: multiple files/tabs open at once** — the single feature
   most likely to matter as a real project grows.
2. **Extract `scanPyodideCompatibility()` into a shared module** — small,
   low-risk, and the clearest proof the "share more code" recommendation
   is worth acting on.
3. **A tested offline story for Mini IDE's download** — closing the gap
   between "should work offline" and "verified to work offline."
4. **`micropip` package installation in Mini IDE**, gated behind a clear
   warning — the next real ceiling a growing project will hit.

Nothing on dewmini's own list is urgent enough to lead with — for a tool
whose entire design point is staying small, that's the right state to be
in.

---

## 6. Addendum: the direction actually taken

Written in a later session, after the person dewlab is built for read this
plan and answered the merger question directly: "I think dewmini wins out
in our little ide competition here... can we make sure all of the
features of mini-ide are in dewmini but we keep dewmini's style and
layout?" Asked to choose between keeping both indefinitely or retiring
Mini IDE once parity was reached, the answer was retirement.

This is not §4 turning out to be wrong. §4 weighed a *merger* — one page,
a mode switch — against keeping them separate, and correctly found the
merger worse for a student. What actually got decided is a third thing §4
never evaluated: a **replacement** — dewmini grows to cover everything
Mini IDE does, in dewmini's own smaller style, and Mini IDE stops
existing once that's true. No mode switch, no state-migration problem —
the two objections §4 raised against a merger. One tool remains; it
simply isn't the one this document originally assumed would survive.

The work was staged:

1. **A shared sidebar system first** (`planning/SIDEBAR_CONTENT.md`,
   `DECISIONS_LOG.md` 7.83/7.84) — Settings, Reference, and (on tutorial
   pages) the series nav became genuine docked panels, toggled from a
   sticky masthead action row, on tutorial pages, Mini IDE, and dewmini
   alike. Chosen first because both IDEs' Settings panel already share
   `.dl-settings` with tutorial pages, so this proved the pattern once
   rather than building it three times.
2. **Feature parity**, next: the file manager, SQLite persistence,
   Worker-based Pyodide with a genuine Stop button, and `.ipynb`/`.py`
   import+export that Mini IDE had and dewmini didn't, ported into
   dewmini's own codebase — keeping dewmini's simpler visual language
   rather than adopting Mini IDE's. The goal was dewmini gaining Mini
   IDE's *capability*, not its *weight*.

   A gap check before starting found it smaller than expected: dewmini
   already had `.ipynb`/`.py`/`.html` export and the compatibility
   scanner, and `run_query()` was already reachable in a cell (it lives
   in the shared `tutorial_tools.py`, already exposed by dewmini's
   `SEED_GLOBALS_CODE`). **Done: `.py` import** (`DECISIONS_LOG.md`
   7.87). **Done: the file manager and genuine SQLite persistence**
   (`DECISIONS_LOG.md` 7.88) — a mounted filesystem (real folder, OPFS,
   or IDBFS, in Settings' own "Files" section rather than a sidebar tree)
   plus a `sync()`-after-every-cell-run fix neither this port nor Mini
   IDE's original had, without which a `.db` file's writes never reached
   persistent storage. **Done: the Worker/Stop migration**
   (`DECISIONS_LOG.md` 7.89) — the largest and last of the four, since
   nothing else on this list depended on it. `pyodide-engine.js` became
   the shared `assets/pyodide-engine.js`, both tools now import from;
   dewmini's Python runs in a Worker with a genuine Stop button. Two real
   bugs (`tutorial_tools.py` 404ing from dewmini's deeper path, the Stop
   button never appearing on a page's first-ever run) were caught by
   testing and fixed. **Feature parity is complete** — all four items on
   this list are done.
3. **Done: Mini IDE's retirement** (`DECISIONS_LOG.md` 7.91), now that
   parity was real. `assets/mini-ide.html` (the hosted URL) redirected to
   dewmini rather than being removed outright; the app itself was
   renamed to `assets/mini-ide-offline-app.html` and kept, unlinked, as
   the source `write_mini_ide_bundle()` in `build.py` still packages into
   a working offline download. Every link, doc (`docs/DEWMINI.md`,
   `docs/MINI_IDE.md`, `docs/FOR_STUDENTS.md`, `README.md`,
   `ARCHITECTURE.md`, the explainer docs under `docs/`), and this
   document's own §4 recommendation were updated to match — one Python
   workspace now, not two.
4. **Done: dewmini's own offline, downloadable copy**
   (`DECISIONS_LOG.md` 7.92) — out of scope for step 2, while Mini IDE's
   own offline bundle still met the "an offline workspace exists" need on
   its own; stopped being optional the moment step 3 retired Mini IDE.
   Found and fixed a real bug shared by both offline bundles while
   building it: neither could actually be opened by double-clicking (a
   browser blocks the `import` statements this codebase's JavaScript is
   built from, from a file opened straight off disk) — both now ship a
   small *serve.py* that serves the unzipped folder locally instead.

§1–§5 above are kept as written: the accounting of what each tool needed
next was accurate at the time, and most of it (the file manager, SQLite,
`.ipynb` import/export, Worker-based Pyodide) is exactly what step 2 went
on to port, not work that stopped mattering.

---

## Addendum 3 — what the shared engine taught

The parity checklist this document carried while the retirement was
still ahead is gone: it planned work that has since been done, and its
table recorded two gaps — Jedi autocomplete and a downloadable bundle —
that dewmini now has.

One lesson outlasts the plan. Reviewing the Worker migration *after* it
merged turned up six defects (`DECISIONS_LOG.md` 7.97), and the worst of
them — a "Restart Python" that permanently wedged the tool it exists to
unwedge — sat in `assets/pyodide-engine.js`, so it affected both
workspaces at once. Now that one engine is the only engine, a change to
it is a change to every surface that runs Python, and worth reviewing as
such rather than as a change to whichever one prompted it.

---

## Addendum 4 — the removal, finishing what retirement started

Step 3's retirement deliberately kept three things: the hosted URL as a
redirect, the renamed offline app as the source of a still-offered
download, and the app's own code and stylesheet that download needed.
The reasoning for the second and third — dewmini had no offline
distribution of its own yet — expired the moment step 4 built one.

A later pass (`DECISIONS_LOG.md` 7.98) acted on that: the offline app,
`mini-ide.js`, `mini-ide-fs.js`, `mini-ide-style.css`, the
`write_mini_ide_bundle()` build step and its download, the tombstone
`docs/MINI_IDE.md`, and the two explainer docs for the deleted code are
all gone, and every present-tense reference across code and
documentation was reworded. The redirect at the old hosted URL nearly
survived on 7.91's bookmark reasoning — until it turned out the site had
never been deployed or shared with students, so there were no bookmarks
to protect; it went too. This document, and `MINI_IDE_REDESIGN.md`
beside it, stay as the history of how dewlab came to have the one
workspace it has.
