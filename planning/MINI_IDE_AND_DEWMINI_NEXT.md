# Mini IDE and dewmini: what's next, and whether they should become one thing

Written after a working session that fixed a real bug (Mini IDE's output
never actually rendered — a stale CSS class, not the Worker migration, was
hiding it), added several requested features to both IDEs, and along the
way surfaced a few things worth deciding on purpose rather than by
accident. This is that plan: what's genuinely still worth building, and
the merger question asked directly — is one tool, not two, doable and
better for a student?

Short answer to the second question, up front, since it's the one with the
most riding on it: **no, not a merger of the two experiences a student
chooses between — but yes, quite a bit more sharing of the code
underneath them than exists today.** The reasoning is in
[§4](#4-the-merger-question).

**Superseded, directly, by the person this recommendation was written
for — see the addendum after §5.** §4's own reasoning stands as written
below (it was correct given what it was weighing), but the actual
decision it fed into went the other way: not a "two modes in one page"
merger — §4 is right that this loses more than it gains — but dewmini
adopting all of Mini IDE's capabilities while keeping its own smaller
style, with Mini IDE retiring once that parity is reached. This is a
call only the person the tool is for gets to make, not something a
written recommendation overrides on its own; see the addendum for what
actually changed and why it isn't a contradiction of §4's reasoning so
much as a different question being asked.

---

## 1. Where things actually stand

`planning/MINI_IDE_REDESIGN.md` shipped all eight of its phases: Mini IDE
now runs Pyodide in a Worker (real Stop button, real autocomplete), has a
file manager, SQLite via `run_query()`, `.ipynb`/`.py` import and export,
and a folder-based offline distribution. dewmini stayed deliberately
smaller — main-thread Pyodide (no Stop button, by design, not by gap),
one file, no file manager — with its own additions since: `sqlite3` and
Pillow in its default packages, a practice-problem bank, student-authored
documentation-cell images.

This session's own work, in one pass:

- Fixed the actual output-rendering bug in Mini IDE (a static `.empty`
  CSS class never got cleared after a cell's first run — `dewmini`
  never had this bug, since its own code already removed and re-added
  the equivalent class correctly).
- Added, to both: a non-destructive per-cell and toolbar "reset output"
  (distinct from the existing, destructive "clear everything"), a
  run-time stat under each cell's output with a Settings toggle, an
  idle-state rail that no longer shows a permanent grey line, a
  two-click "arm then confirm" delete in place of a single accidental
  click, and a Jupyter-import compatibility scanner that flags magic
  commands, shell escapes, and structurally-impossible imports
  (`tkinter`, `subprocess`, and the like) before a reader wonders why
  an imported cell they didn't write themselves is erroring.
- Shipped the first three real datasets dewlab has ever had in `data/`
  (`co2-emissions.csv`, `life-expectancy.csv`, `pride-and-prejudice.txt`,
  all real, cited, correctly licensed) and four worked-example notebooks
  built on them, reachable from both IDEs' own Import section.
- Fixed a site-wide bug in the Texture "Size" slider (it resized reading
  prose but not panels, buttons, or either IDE's own workspace math,
  because the CSS variable was set on `body` where `rem` units don't
  read from) and the desktop side-panel-covers-content problem, on the
  IDEs and on ordinary tutorial pages both.
- Settled on **Reference** as the panel's name across code, tests and
  docs — only `DECISIONS_LOG.md` keeps the older name, in its own
  entries — and gave it its own in-panel search, alongside a new
  cross-tutorial search on the contents and topic pages.

None of that is a foundation problem anymore. What's left is real, but
it's feature and polish work, not architecture repair.

---

## 2. Mini IDE: what's still worth building

**A real "download once, work locally" story, tested, not assumed.**
Phase 7 of the redesign vendors Pyodide for the offline export, but
nothing currently proves the downloaded folder actually boots with the
network disconnected on a fresh machine — worth a standing manual check
before every release, or a CI job that serves the built folder from a
loopback address with outbound network blocked.

**Multiple simultaneous files, properly.** The file manager can hold many
files, but only one notebook is "the" notebook at a time — there's no way
to have two `.py` scripts, or a notebook and a `.db` file, both open as
tabs the way a real local IDE would let you switch between. This is the
single feature most likely to matter as a "project meant to stand on its
own" (Mini IDE's own stated purpose) actually grows past one file.

**A genuine multi-cursor / find-and-replace inside the editor.**
CodeMirror supports both; neither is wired up. Low effort relative to
value once a notebook gets past a screen or two of code.

**Package installation beyond the fixed set.** `numpy`/`pandas`/
`matplotlib`/`sqlite3` cover the curriculum; a project a student builds on
their own initiative will eventually want something else. Pyodide
supports `micropip` for pure-Python packages already on PyPI — worth a
Settings section ("Install a package") gated behind a clear warning about
what will and won't work (anything needing a C extension without a
pre-built Pyodide wheel simply won't install, and that failure needs to
read as informative, not broken).

**Collaborative or shareable state.** Everything lives in one browser,
which is the right privacy default (`OPEN_QUESTIONS.md` #17 already
settles this deliberately) — but a lightweight "export a shareable link"
for a single cell's code (not the whole notebook, not the student's
saved progress) would let a reader ask for help on one specific thing
without exporting a whole file. Worth weighing against the privacy
position it sits next to, not a given.

---

## 3. dewmini: what's still worth building

**Nothing that makes it bigger.** That's the actual finding here, not a
dodge: dewmini is deliberately the smaller, quieter sibling, and every
feature considered below is evaluated against "does this still feel like
a five-second tool for one calculation," not "does this catch up to Mini
IDE."

**The Stop button gap, if it turns out to matter.** dewmini runs Python
on the main thread on purpose — the Worker migration Mini IDE went
through is real architectural cost (`planning/CELL_CONTROLS.md` §2 has
the full accounting: cross-origin isolation, a service-worker shim, every
call site crossing a postMessage boundary). If reports of students
genuinely getting stuck on a runaway `while True` in dewmini start
piling up, that migration is the answer and the cost is already fully
understood, not a research problem. Until then, this is correctly
deferred, not neglected.

**A quieter, dewmini-scoped version of the two site-wide fixes this
session made.** The panel-resize and "don't cover content" work applied
to Settings/Help on both IDEs already. If dewmini ever grows a third
panel the way tutorial pages have (Settings, Reference, series nav), the
same pattern is already proven and cheap to extend — not something to
build ahead of the need.

**Nothing else.** A genuinely short list is the right length for a tool
whose whole design point is staying short.

---

## 4. The merger question

Could Mini IDE and dewmini become one tool? Mechanically, yes — nothing
stops it. Whether it's better for a student is a different question, and
the answer is no, for a reason that's already written down elsewhere in
this repository and worth restating plainly: **dewmini's whole design
point is not being Mini IDE.** What `docs/DEWMINI.md` describes —
somewhere to run a few lines that isn't tied to one topic, reachable
in effectively no clicks, nothing to configure before typing code — is a
real, different use case from "a project meant to stand on its own,"
not a smaller version of the same use case. A student who wants to check
one thing and a student starting a real project are asking dewlab for
different things, and merging the tools that serve them either:

- **forces the quick-check student through the bigger tool's own
  weight** — a file manager they don't need, a wider settings panel, a
  concept ("this is a whole workspace with files in it") that gets in
  the way of "I just want to try this one line," or
- **keeps two modes inside one tool, switched by a setting or a URL
  parameter** — which is a merger in name only: the code shares a
  shell, but a student still picks a mode, the UI still has to explain
  the difference, and now there's a state-migration problem (what
  happens to a dewmini-mode notebook's cells if a reader flips to
  Mini-IDE-mode?) that doesn't exist today because they're just two
  pages.

Neither outcome is better for the student than what exists now: two
pages, one link between them ("Outgrowing a quick notebook?"), no
decision to make until outgrowing it is a real, felt thing rather than a
menu a first-time visitor has to parse.

**What genuinely is worth doing, and is a real form of "merging," is
sharing more of the code underneath the two pages than they share
today.** The codebase's own stated convention — "each page owns a thin
copy rather than a shared runtime module," per `mini-ide-engine.js`'s
own comment — was a reasonable call when there was one page (tutorial
pages) and Mini IDE was new. With three surfaces now genuinely running
overlapping logic (tutorial pages, Mini IDE, dewmini), and this session
adding a fourth near-duplicate pass (`scanPyodideCompatibility()`,
`armDeleteButton()`/`disarmDeleteButton()`, `applyImportedCells()`, each
now written out twice, once per IDE, by design, matching the existing
convention), the balance has shifted enough to be worth naming as a real
option rather than assuming the old default still holds:

- **Keep duplicating** (the status quo). Every page stays fully
  independent and easy to reason about in isolation — reading
  `mini-ide.js` never requires also understanding `dewmini.js` — at the
  cost of every shared fix (this session had several: the delete
  confirmation, the compatibility scanner, the built-in-examples
  loader) needing to land twice, by hand, with the ever-present risk of
  the two copies drifting the way Mini IDE's own output-visibility bug
  shows they already can.
- **Extract a genuinely shared module** for the pieces that are pure
  logic with no page-specific DOM assumptions baked in —
  `scanPyodideCompatibility()` is the cleanest candidate already
  (takes an array of plain cell objects, returns an array of strings,
  touches no DOM at all) — imported by both pages rather than pasted
  into both. This is a real, bounded piece of work, not a rewrite: it
  changes how three or four specific functions are packaged, not how
  either page behaves.

The second option is the recommendation, done gradually rather than as
one big refactor: the next time a shared fix needs to land in both
places (and on this session's evidence, that will be soon), extract
that one piece into a shared module instead of copying it a third time,
and let the shared layer grow function by function rather than declaring
a migration up front. `assets/tutorial_tools.py` is already exactly this
pattern on the Python side — one file, imported everywhere, changed
once — there's no reason the JavaScript side can't grow the same way for
the parts that are genuinely page-agnostic.

---

## 5. If picking one thing to do next

In order, by how much a student would actually notice:

1. **Mini IDE: multiple files/tabs open at once** — the single feature
   most likely to matter as a real project actually grows.
2. **Extract `scanPyodideCompatibility()` into a shared module** — small,
   low-risk, and the clearest proof this session's own "share more code"
   recommendation is worth acting on rather than just writing down.
3. **A tested offline story for Mini IDE's download** — not a new
   feature, just closing the gap between "should work offline" and
   "verified to work offline."
4. **`micropip` package installation in Mini IDE**, gated behind a clear
   warning about what won't install — the next real ceiling a growing
   project will hit after "multiple files."

Nothing on dewmini's own list is urgent enough to lead with — which, for
a tool whose entire design point is staying small, is exactly the
right state to be in.

---

## 6. Addendum: the direction actually taken

Written in a later session, after the person dewlab is built for read this
plan and answered the merger question directly rather than by proxy:
"I think dewmini wins out in our little ide competition here... can we
make sure all of the features of mini-ide are in dewmini but we keep
dewmini's style and layout?" Asked to choose between keeping both
indefinitely or retiring Mini IDE once parity was reached, the answer was
retirement.

This is not §4 turning out to be wrong. §4 weighed a *merger* — one page,
a mode switch, both experiences folded into a single tool — against
keeping them genuinely separate, and correctly found the merger worse for
a student than two pages. What actually got decided is a third thing §4
never evaluated: not a merger, but a **replacement** — dewmini grows to
cover everything Mini IDE does, in dewmini's own smaller style rather than
Mini IDE's, and Mini IDE stops existing once that's true. There is no
mode switch, no "which experience am I in" for a student to parse, no
state-migration problem between two coexisting shapes — the two objections
§4 raised against a merger. One tool remains; it simply isn't the one this
document originally assumed would be the survivor.

The work is being staged, not done in one pass:

1. **A shared sidebar system first** (`planning/SIDEBAR_CONTENT.md`,
   `DECISIONS_LOG.md` 7.83/7.84) — Settings, Reference, and (on tutorial
   pages) the series nav became genuine docked panels, toggled from a
   sticky masthead action row rather than floating corner popovers, on
   tutorial pages, Mini IDE, and dewmini alike. Chosen to go first because
   both IDEs' Settings panel already share `.dl-settings` with tutorial
   pages — proving the pattern once and reusing it, rather than building
   it three times.
2. **Feature parity**, next: the file manager, SQLite persistence,
   Worker-based Pyodide with a genuine Stop button, and `.ipynb`/`.py`
   import+export that Mini IDE has and dewmini doesn't, ported into
   dewmini's own codebase — keeping dewmini's simpler visual language
   rather than adopting Mini IDE's, per the explicit instruction. §3's "a
   tool whose entire design point is staying small" framing above is
   itself now something to hold onto deliberately during this work, not
   evidence against doing it: the goal is dewmini gaining Mini IDE's
   *capability*, not its *weight*.

   A gap check before starting this step found it smaller than it reads:
   dewmini already had `.ipynb`/`.py`/`.html` export and the
   compatibility scanner from an earlier session, and `run_query()` was
   already reachable in a cell (it lives in the shared
   `tutorial_tools.py`, which dewmini's `SEED_GLOBALS_CODE` already
   exposes in full). **Done: `.py` import** (`DECISIONS_LOG.md` 7.87) —
   closes out the import/export item entirely. **Done: the file manager
   and genuine SQLite persistence** (`DECISIONS_LOG.md` 7.88) — a
   mounted filesystem (real folder, OPFS, or IDBFS, tucked into
   Settings' own "Files" section rather than a sidebar tree, per an
   explicit choice against Mini IDE's own heavier shape) plus a
   `sync()`-after-every-cell-run fix neither this port nor Mini IDE's
   own original had, without which a `.db` file's own writes never
   actually reached persistent storage. **Done: the Worker/Stop
   migration** (`DECISIONS_LOG.md` 7.89) — the largest and most
   structurally invasive of the four, and the last one, since it was the
   one nothing else on this list actually depended on. `mini-ide-engine.js`
   became the shared `assets/pyodide-engine.js`, both tools now import
   from; dewmini's Python runs in a Worker with a genuine Stop button,
   matching Mini IDE's own since `MINI_IDE_REDESIGN.md`; two real bugs
   (`tutorial_tools.py` 404ing from dewmini's own deeper path, the Stop
   button never appearing on a page's first-ever run) were caught by
   testing and fixed, not left as known gaps. **Feature parity is
   complete** — all four items on this list are done.
3. **Done: Mini IDE's retirement** (`DECISIONS_LOG.md` 7.90), now that
   parity was real — per an explicit instruction that this was a given,
   not a further decision point. `assets/mini-ide.html` (the hosted
   URL) redirected to dewmini rather than being removed outright, so a
   bookmark or an old link still lands somewhere useful; the app itself
   was renamed to `assets/mini-ide-offline-app.html` and kept, unlinked,
   as the source `write_mini_ide_bundle()` in `build.py` still packages
   into a working, self-contained offline download — dewmini has no
   offline distribution of its own yet to replace it with, and the
   download costs nothing to keep working. Every link, doc
   (`docs/DEWMINI.md`, `docs/MINI_IDE.md`, `docs/FOR_STUDENTS.md`,
   `README.md`, `ARCHITECTURE.md`, the explainer docs under `docs/`),
   and this document's own §4 recommendation were updated to match — one
   Python workspace now, not two.

§1–§5 above are kept as written: the accounting of what each tool needed
next was accurate at the time, and most of it (the file manager, SQLite,
`.ipynb` import/export, Worker-based Pyodide) is exactly what step 2
went on to actually port, not work that stopped mattering.
