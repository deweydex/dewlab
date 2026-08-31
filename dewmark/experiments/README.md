# The exam experiments, corrected

The two 2025–26 exam experiments that
[`../planning/LESSONS_FROM_THE_EXPERIMENTS.md`](../planning/LESSONS_FROM_THE_EXPERIMENTS.md)
audits, each in its student and its sample-answers form, with the concrete
code bugs the audit found repaired. They are past papers the author has
released; committing them here does not breach the no-real-exam-content
rule (OPEN_QUESTIONS DM-1), which concerns unsat exams and student
submissions. They sit here as working prior art and a source of ideas —
the dewmark specifications, not these files, define what gets built.

Only bugs were fixed. The architectural habits the audit criticises —
content in JS template literals, positional saving in the maths paper,
hand-duplicated sidebar data — are left as they were, because repairing
those properly is what dewmark is for and a rewrite here would blur what
the experiments teach.

## The files

**`hvit-database-exam.student.html`** — the Database Methods 5N0783
practical (Pyodide, SQLite, pandas, matplotlib): the paper a student
sits. **`hvit-database-exam.answers.html`** — the same paper with worked
sample answers in every cell, for an assessor. Both need the network for
the Pyodide and CodeMirror CDNs.

**`mit-5n18396-maths.student.html`** — the Maths for Information
Technology 5N18396 paper in its no-Python form: fully offline, sat from
a double-clicked file. **`mit-5n18396-maths.assessor.html`** — the
Python-enabled variant that fills every field with the model answers on
load; Run buttons need the Pyodide CDN, everything else works without it.

## Corrections applied

To the database exam, both variants:

- The two Excel files (`late_arrivals.xlsx`, `equipment_survey.xlsx`)
  are now embedded as base64 and written into the Pyodide filesystem
  like the database, instead of fetched from beside the HTML file — the
  fetch fails silently on a `file://` page and Tasks 5 and 6 then died
  with a bare `FileNotFoundError`. The workbook contents are
  reconstructed to the schemas the tasks describe.
- `slider` is imported by the setup cell, so the sidebar's advertised
  API no longer raises `NameError`.
- The sidebar API reference now states the real `number_input` and
  `slider` signatures (`min_val`/`max_val`, not `min`/`max`).
- Cancelling the save-location picker shows a persistent "File autosave
  off" state and a toast instead of failing silently, and the same
  state shows whenever autosave has no file to write to.
- The manual Save download is named `exam_<student>_<date>.json`
  instead of `exam_submission_<timestamp>.json`.
- Clicking Run while a cell is executing says so instead of silently
  dropping the click.
- A stale comment naming `late_enrolments.xlsx` is corrected.

To the database exam's answers variant:

- The Task 3 model answer called
  `number_input(..., min=1, max=3, ...)` against a signature of
  `min_val`/`max_val` and raised `TypeError` — the model answer for a
  ten-mark task did not run. Now it does.
- The Task 6c model answer gave `axvline` a label but never drew a
  legend, so "Midpoint" appeared nowhere. `ax.legend()` added.

To the maths paper, both variants:

- Save payloads now carry a `variant` tag (`nopy` / `assessor`), and
  restore refuses a save file from the other variant with an
  explanation — the two variants store answers positionally in
  different field orders, so a cross-variant restore misfiles answers.
  In the no-Python paper such a restore also hit an undeclared
  variable (`outputs`) and threw mid-restore; that dead code path is
  removed.
- "Clear saved data" now clears the fields on screen as well as the
  browser storage — previously the answers stayed visible and the next
  keystroke quietly re-saved everything just "cleared".

To the maths paper's assessor variant:

- The model answers were injected 200 ms after load on a timer, racing
  the saved-state restore. They now apply in sequence after the
  restore, no timer.
- The fixed "ASSESSOR VERSION" banner is hidden in print — it printed
  over the first page of the marking scheme. The print header already
  identifies the document as the model answer key.
