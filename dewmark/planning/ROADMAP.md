# dewmark roadmap

Order chosen so that each phase produces something a real exam could use,
and so the riskiest unknowns (the format's expressiveness, the marking
workflow) meet reality earliest. Maths before Python throughout: a
no-code exam exercises the entire pipeline — format, builder, runner,
persistence, submission, marking, exports — with none of the Pyodide
weight, and maths is where the offline requirement is absolute.

## Phase 0 — Specifications (this folder)

Argue with these documents, settle DM-12 (naming) and any DM the
arguing settles for free, and translate one old maths paper and one old
database paper into draft source by hand — not to keep, but to find
where the format spec fails before the parser exists.

## Phase 1 — Format, builder, runner: the maths paper

`build_exam.py` parsing the markdown source into the canonical model
with the full validation suite; the runner shell and runtime for
non-code answer types (text, numeric, mcq, table, sketch); build-time
KaTeX; the three-layer persistence; the finish flow and submission zip.
Exit test: the MIT 5N18396 paper, translated, sits fully offline from a
double-clicked file on a machine with networking disabled, and produces
a valid submission zip — the standing manual check inherited from the
experiments. A sample exam ships in `dewmark/samples/`.

## Phase 2 — The workbench: a real marking session

Folder open, roster, per-paper and per-question marking, grading
record, marks-sheet CSVs, graded HTML + print-to-PDF flow. Exit test: a
full mock marking session — last year's submissions reconstructed from
the experiment JSONs plus fresh mock sittings — marked end to end, and
the exports opened cold by someone who wasn't in the room (the
assessor's seat is the test of the marks sheet). Expect this phase to
send corrections back into the format and workbench specs; that is its
job.

## Phase 3 — Python exams

Code answer type, setup/provided cells, embedded files, pyodide-engine
integration, structured output capture, the backup variant. Exit test:
the HVIT database exam, translated, sat with the room checklist from
DM-7 — including once against a blocked CDN with the local override.

## Phase 4 — The composer page and the graded-PDF spike

Load-validate-preview-package in the browser (DM-11 decided by then),
then structured editing if phase 1–3 authoring friction justifies it;
in parallel, the client-side PDF generation spike (DM-2). Also the
teacher-facing documentation set in `dewmark/docs/`: the author's
format guide, the translation guide, the exam-room checklist, the
marking guide.

## Phase 5 — Polish that earned its place

Rubric-line marking, comment bank refinements, anonymised marking,
diagram-label answers, xlsx export, practice builds of past papers
published to the tutorial side — each contingent on someone having
missed it during a real session, not on the spec having imagined it.

## Standing rules across phases

Every code file lands with its `docs/<file>-explained.md` and tests in
the same PR; every settled DM gets a numbered entry in the root
DECISIONS_LOG; the storage-key and format contracts get a
WINDOW_AUDIT-style freeze document before any student sits a real
paper; and no real exam content or submission ever enters this
repository (DM-1).
