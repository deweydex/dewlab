# The grading workbench

The teacher-side application: open a folder of submissions, mark each
paper against the scheme, write feedback, and export three things — graded
PDFs for students, a marks sheet for the assessor, and the grading record
itself. Like everything in dewmark it is a static page with no server; the
folder on the teacher's machine is the database.

This is the piece with no precedent in the experiments — the "Assessor"
file was a model-answer key, and marking meant printed papers and a biro —
so this spec is the least constrained by prior art and the most likely to
change once a real marking session has been run against it. It should be
prototyped early with last year's papers translated into the format
(ROADMAP, phase 2).

## 1. Opening a session

The workbench is one page (`dewmark/workbench/`), hosted or opened
locally. A session starts by loading two things:

1. **The marking pack** for the exam (SUBMISSION_FORMAT §4) — drag in or
   pick the file. Without it the workbench can display submissions but
   not the scheme; it says so rather than proceeding thinly.
2. **The submissions folder** — via `showDirectoryPicker()` where
   available, with read *and* write permission requested, because the
   grading record lives in that same folder (§5). Fallback on other
   browsers: multi-file selection (read-only), with the grading record
   kept in localStorage and exported by hand; the workbench states the
   difference up front (OPEN_QUESTIONS DM-13 covers whether Firefox/Safari
   marking is worth more engineering than that).

The workbench unpacks each zip in memory, validates every
`submission.json` (schema version, exam id, version against the pack),
and builds the roster. Problems are a report, not a crash: unreadable
zip, wrong exam, duplicate student — each listed with the file name and
what the workbench decided (e.g. duplicates: newest `saved_at` marked
active, others kept visible and swappable).

Everything the workbench renders from a submission is treated as data —
structured outputs rendered by type, all text escaped, images accepted
only as validated raster data URIs. Submissions are the least-trusted
input in the whole system and the workbench is where a malicious one
would aim (LESSONS: "Output persisted as scraped innerHTML").

## 2. The roster

A table: student, id, submission time, attempted-question counts per
choose-N section, marking status (untouched / in progress / done), running
total. Sortable; click through to a paper. The roster is also where
collection problems surface — a student with two submissions, a
submission whose version predates a corrected paper, a finish event
missing (the student never pressed finish; their autosave file was
collected instead — fully markable, flagged as such).

## 3. Marking a paper

The marking screen is a two-column layout, per part:

- **Left: the student's answer** — the question prose for context
  (collapsed to the prompt by default), then the answer as submitted.
  Code answers show code and recorded outputs, with the
  `run_matches_code: false` flag rendered as a visible caution. An
  optional "re-run" control (Pyodide in the workbench) executes the
  student's code against the exam's embedded files for verification —
  useful, but phase 3, and never a substitute for the recorded output.
- **Right: the scheme** — model answer, rubric lines if declared, the
  part's marks, a mark entry field, and a feedback box.

Mark entry is x-out-of-n in half-mark steps, keyboard-first: digits
enter the mark, Enter advances to the next part, the whole paper markable
without touching the mouse. Rubric-line marking (a mark per declared
line, summed) is phase 3. Question and section totals, the choose-N
selection, and the paper total update live and are always visible.

**Choose-N handling.** The workbench marks everything the student
attempted, then counts the best N toward the total by default, showing
which questions were counted and letting the marker override the
selection. The policy (best-N versus first-N versus student-declared) is
DM-6; the mechanism supports any of them, which is the reason `attempted`
is recorded in the submission.

**Feedback** exists at two levels: per part (a short box beside the mark)
and per paper (a closing comment). A comment bank — reusable snippets the
marker builds up while marking ("state units", "method right, arithmetic
slip") — is cheap and pays for itself by paper three; each insertion
remains editable text, not a reference, so later edits to the bank don't
rewrite past feedback.

## 4. Marking by question

The second view, and for consistency the better one: pick a part (say
`b2.t`), see every student's answer to it as a stack, mark down the stack
with the same keys. Markers who work this way apply the same standard to
the twentieth answer as the first. The workbench keeps both views in sync
with the same grading record; switching is free. Anonymised marking
(names hidden until done) is a checkbox on this view.

## 5. The grading record

`dewmark_<exam_id>_grading.json`, written into the submissions folder on
the same debounced schedule the runner uses, so a marking session
survives a crash and can move between machines with the folder:

```json
{
  "dewmark_grading": 1,
  "exam": {"exam_id": "...", "version": "..."},
  "marker": {"name": "..."},
  "papers": {
    "S12345": {
      "status": "done",
      "marks": {"a1.a": 2, "a1.b": 1.5, "t2.a": 3},
      "feedback": {"a1.b": "Say why 7 fails the intersection.",
                    "_overall": "Strong on sets and functions; ..."},
      "counted": {"A": ["a1", "a2", "..."], "B": ["b1", "b2", "b4", "b6"]},
      "total": 87.5
    }
  }
}
```

Marks keyed by answer id, totals recomputed on load rather than trusted,
schema versioned like everything else.

## 6. Exports

**Graded PDFs.** Per student: the snapshot layout with marks and feedback
set beside each part, the counted questions indicated, and the totals
box on page one — the document a student opens on Moodle. Mechanism, in
order of preference: (a) generate per-student graded HTML and drive the
browser's print-to-PDF per paper — works everywhere, tedious at thirty
papers; (b) a vendored client-side PDF generator producing a zip of PDFs
in one click — the right end state, with real open questions about maths
and figure fidelity (DM-2). Phase 2 ships (a) with a "next paper" flow
that makes the tedium bearable; (b) is attempted once the layout is
stable. Graded HTML files are themselves inert, like snapshots.

**The marks sheet.** CSV, openable in Excel: one row per student —
identity, per-part marks in id order, per-question and per-section
totals with choose-N applied, paper total, status. Column headers carry
id and marks (`a1.a (2)`), and a second file (or second region, DM-3
covers CSV-vs-xlsx) maps every id to its question text, topic, and
declared outcomes — the "sensible description of what the marks
represent" an assessor needs without opening any tool. Encoding is UTF-8
with BOM so Excel renders the maths symbols teachers will inevitably
have typed into feedback.

**The grading record itself** is already the archival export; the
workbench's Export All writes PDFs (or graded HTML), the marks sheet, and
a copy of the marking pack into an `exports/` subfolder, so the folder
ends the session as the complete audit trail: papers in, scheme, marks,
feedback, outputs.

## 7. What the workbench is not

Not an auto-marker — nothing in phase 1–3 computes correctness, including
for numeric and MCQ answers where it obviously could; that line is worth
holding until the human workflow is trusted (revisit: DM-16 discusses
assisted marking as a separate, later question with its own consent and
accuracy problems). Not a gradebook — it knows one exam at a time;
cross-exam aggregation is the institution's spreadsheet's job. Not a
plagiarism detector, for the same reasons the runner is not a proctor.
