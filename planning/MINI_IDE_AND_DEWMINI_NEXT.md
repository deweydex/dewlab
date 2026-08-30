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
- Renamed the "cheat sheet" to "Reference" everywhere — code, tests,
  docs, planning history excepted — and gave it its own in-panel search,
  alongside a new cross-tutorial search on the contents and topic pages.

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
point is not being Mini IDE.** `README.md`'s own description of it —
"good for a quick calculation or a single practice problem," reachable
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
