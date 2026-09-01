# The exam experiments, corrected

This folder holds the two hand-built browser exams from the 2025–2026
academic year, each in its student version and its sample-answers
version, with their known code faults repaired. The exams are released
past papers; committing them here breaks no rule about exam secrecy,
which applies to exams that have not yet been sat and to student
submissions. They are kept as working examples of what came before
dewmark, and
[`../planning/LESSONS_FROM_THE_EXPERIMENTS.md`](../planning/LESSONS_FROM_THE_EXPERIMENTS.md)
records what they taught. The dewmark design documents, not these
files, define what gets built.

Only faults were fixed. The structural habits that the lessons document
criticises — saving answers by position, hand-maintaining several
copies of the same facts, embedding content inside program code — were
left as they were, because these files are kept as a record, and
repairing their structure properly is dewmark's job.

## The files

`hvit-database-exam.student.html` is the Database Methods practical:
six tasks answered as live Python code, with a small database embedded
in the page. `hvit-database-exam.answers.html` is the same paper with
worked sample answers in every task. Both versions need an internet
connection to download the in-browser Python system and code editor
when they open.

`mit-5n18396-maths.student.html` is the Maths for Information
Technology paper in its fully offline form; it can be sat from a
double-clicked file with no network at all.
`mit-5n18396-maths.assessor.html` is the version with runnable Python
cells that fills every answer space with the model answers when it
opens; its Run buttons need the internet once, and everything else
works without it.

## The corrections

The following faults were repaired in the database exam, in both
versions.

- The two spreadsheet files the exam uses are now encoded as text and
  embedded inside the page, as the database already was, instead of
  being fetched from beside the page when the exam starts. The fetch
  fails silently when the page is opened from a local file, and two of
  the six tasks then failed during the exam.
- The `slider` helper function is now imported by the set-up code, so
  the sidebar's documentation of it no longer points at a function that
  produced an error when called.
- The sidebar's reference card now states the helper functions' real
  parameter names, which it had misstated.
- Cancelling the choose-a-save-file step now shows a persistent "file
  saving is off" notice instead of failing silently, and the same
  notice appears whenever file saving is unavailable.
- The manually downloaded answer file is now named with the student's
  name and the date instead of a bare timestamp.
- Clicking Run while another task's code is still running now says so
  instead of ignoring the click.
- A comment that named a file which does not exist now names the right
  file.

The following faults were repaired in the database exam's answers
version only.

- The sample answer for the ten-mark form task called a helper function
  with parameter names it does not accept, so the model answer failed
  with an error when run. It now runs.
- The chart task's sample answer labelled a line for a legend but never
  drew the legend, so the label appeared nowhere. It now draws it.

The following faults were repaired in the mathematics paper, in both
versions.

- Saved answer files now record which version of the paper wrote them,
  and each version refuses to restore a file from the other, with an
  explanation. The two versions save different lists of answers in
  positional order, so restoring across versions filed answers into the
  wrong boxes; in the offline version it also crashed partway through,
  because the restore code referred to a variable that only the other
  version defines. That code is removed.
- "Clear saved data" now clears the answer boxes on screen as well as
  the browser's stored copy. Previously the answers stayed visible, and
  the next keystroke saved them all again.

The following faults were repaired in the mathematics paper's assessor
version only.

- The model answers are now filled in after the saved-state restore
  finishes, in a fixed order. Previously they were filled in after a
  fixed delay of a fifth of a second, racing the restore.
- The fixed "ASSESSOR VERSION" banner no longer appears on printouts,
  where it printed over the first page of the marking scheme. The
  printed header already identifies the document as the answer key.
