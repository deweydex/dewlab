# The exam runner

The page the student sits. It is compiled per exam by the composer — one
self-contained HTML file per variant — so "the runner" names a template and
a runtime, not a hosted app. A student receives the file (Moodle download,
shared folder, USB stick), opens it in a browser, and everything from the
first screen to the finish step happens in that one page.

Two hard constraints shape everything here:

1. **Offline by class of exam.** An exam without code cells must run with
   zero network access from a double-clicked `file://` page: maths rendered
   at build time, fonts embedded or system, no CDN, no service worker
   requirement. An exam with code cells needs Pyodide, which is too large
   to embed; it loads from the CDN by default, from a room-local server via
   the same `DEWLAB_PYODIDE_BASE` override dewlab already uses when the
   room has no internet (delivery options: OPEN_QUESTIONS DM-7). Everything
   except running cells still works while Pyodide loads or if it fails —
   the MIT paper's graceful degradation, kept.
2. **Nothing is lost.** The student's work survives a browser crash, a
   machine swap, an accidental close, and a power cut, to the limit of what
   a browser permits. Persistence is specified in §4 and is the most
   safety-critical part of dewmark.

## 1. The sitting, start to finish

**Start screen.** Institution and module header, exam title, duration,
instructions from the source frontmatter, then the identity fields the
exam declares (name, student id). On Begin: on browsers with the File
System Access API, the runner immediately asks the student to choose a
save-file location (suggested name derived from exam id + student id +
name) and explains why in one sentence; elsewhere it says plainly that
saving is to this browser plus manual downloads, and shows a visible
Download-progress button. Cancelling the picker is not silent: the page
shows a persistent amber "file autosave off — browser only" state
(LESSONS: "Silent failure paths").

**The paper.** A single scrolling main column of sections, questions, and
answer fields, with a slim fixed header (exam title, student name, save
indicators, finish button) and a collapsible side panel holding: question
navigator (generated from the model — ids, marks, answered state),
reference panel (formula sheet, notation guide, glossary from the
`reference` blocks), files panel (for code exams: filename +
copy-to-clipboard, generated from `files:`), and for code exams a Python
status chip. All generated, none hand-maintained.

**Answer fields** per SOURCE_FORMAT §3. Text areas auto-grow and start at
the marks-derived height. Code cells are CodeMirror with the dewlab
conventions (Ctrl/Cmd-Enter to run, Tab indents four spaces); one shared
Python namespace, cells run in any order the student chooses, with the
same honest consequences as a notebook. A Run is disabled while another
runs, with the button visibly in a running state rather than a silently
dropped click.

**Choose-N sections.** The navigator shows "answered 8 of choose 10" per
choose-N section and counts a question as attempted when any of its fields
is non-empty. The runner never blocks answering more than N — students
change their minds — but the finish step reports the count, and the
submission records which questions were attempted so the marking policy
(OPEN_QUESTIONS DM-6) has data to work with.

**Finish.** The finish button opens a checklist screen, not a trapdoor:
unanswered parts listed by id and marks, choose-N counts per section, code
cells edited since last run flagged (their recorded output is stale), and
the identity fields shown for confirmation. Confirming produces the
submission zip (SUBMISSION_FORMAT) as a download, marks the sitting
finished in the saved state, and shows the handover instructions compiled
from the source (typically: upload the zip to Moodle; if asked, also print
to PDF as a backup — print remains available). Finishing is reversible
until the student leaves — reopening the page after finish shows a
"finished, re-open to amend" state rather than a wall, because exam-room
reality includes "the invigilator said we have ten more minutes."

## 2. Runtime architecture

One template (`dewmark/assets/runner-shell.html`) plus one runtime module
compiled in classic-script form so `file://` works (the
`standalone.bundle.js` precedent). The exam's canonical model rides in
`<script type="application/json" id="dewmark-exam">`; embedded files in
their own base64 script blocks; never in JS literals (LESSONS: "Content
inside JS template literals"). The runtime reads the model and builds the
page — the same manifest-and-runtime contract the tutorial pages use.

For code exams the runner reuses `assets/pyodide-engine.js` and the
`tutorial_tools.py` lineage rather than a fresh `exam_tools` fork; the
widget subset an exam needs (`show`, `show_table`, form inputs, `button`)
already exists there. Exams run Pyodide on the main thread (single-file
`file://` pages cannot carry the worker + COI service worker apparatus),
which forfeits the Stop button; the runner therefore ships the engine's
main-thread mode and says so in the reference panel. Whether that
trade-off is acceptable for long-running student loops is OPEN_QUESTIONS
DM-9.

Cell output is captured as structured records — `{kind: stdout|image|
table|error, ...}` — at the engine boundary, both for display and for
persistence. No innerHTML scraping (LESSONS: "Output persisted as scraped
innerHTML").

## 3. What the runner does not do

No lockdown, no proctoring, no telemetry, no network calls beyond Pyodide
delivery. dewmark exams are invigilated in a room or openly take-home;
pretending a browser page can police either would be theatre. The
submission's light event record (start, saves, finish — SUBMISSION_FORMAT
§2) exists for recovery and honest timestamps, not surveillance, and the
format documentation says so where students can read it.

No auto-marking at sitting time. Nothing in the student file knows a
correct answer (asserted at build; SOURCE_FORMAT §5), which also means
view-source reveals nothing.

## 4. Persistence

Three layers, all writing the same submission-shaped record (one format
everywhere — the save file is the submission file minus packaging):

1. **localStorage**, key `dewmark:sitting:<exam_id>:<student_id-or-anon>`,
   debounced 2 s after any input or run, plus a synchronous write on
   `beforeunload` and `visibilitychange`. Keys are namespaced separately
   from `dewlab:*` and documented in a WINDOW_AUDIT-style contract before
   phase 1 ships.
2. **A real file** via the File System Access API where available, written
   whole on the same debounce. Two independent indicators — browser ✓,
   file ✓, each with a last-saved time — and every failure visibly demotes
   the indicator and offers a re-pick.
3. **Manual download** of the same JSON, always present, prominent on
   browsers without layer 2.

Restore on open: newest valid record wins among localStorage and an
offered file restore, with an explicit prompt when they disagree
(timestamps shown; policy detail DM-15). Restore validates against the
exam id and format version before touching the page, restores by answer
id, reports "restored N answers, M unknown ids skipped", and for code
exams states what a restore brings back: your code and its recorded
outputs; run cells again to rebuild live state.

## 5. Failure states worth designing, not patching

- Pyodide fails to load → banner with the cause and what still works;
  written answers unaffected; retry button.
- Save file handle dies (USB pulled, permission revoked) → indicator goes
  amber, one toast, re-pick offered; localStorage continues regardless.
- Storage quota exceeded (large figures in outputs) → oldest non-current
  figure data dropped from the localStorage layer first, file layer keeps
  everything; the student is told.
- Clock skew / no clock: timestamps are recorded as claims, and the
  workbench treats them as such.
- The same exam opened in two tabs → second tab detects the storage lock
  and opens read-only with a plain explanation.

Every one of these states has copy written for a nervous eighteen-year-old
forty minutes into a two-hour paper: short, calm, and specific about
whether their work is safe.
