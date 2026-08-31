# dewmark

Exams that run in a browser, are sat offline, and are marked from a folder.

dewmark is the assessment track of the dewlab project. It takes an exam
written in one source file — markdown or Python, in a documented format — and
compiles it into a self-contained HTML exam a student can sit with no server
and, for exams without code, no internet at all. While the student works, the
exam saves itself. When they finish, it produces a small set of files the
teacher can collect, open in a local marking workbench, mark against the
scheme, and export as graded PDFs for the students and a marks sheet for an
assessor.

Nothing here talks to a server. The exam is a file, the submission is a file,
the marks are a file. Every stage works from a folder on one machine.

## Why this exists

Last semester's exams were hand-built HTML experiments — a Pyodide database
exam, a practice exam for image-space maths, and a two-variant maths paper
with a model-answer copy. They worked in the room, and they taught us most of
what is in these specifications, largely by what went wrong in them:
hand-duplicated data that drifted, answers saved by position instead of by
name, marks that existed only as prose, silent failure paths in the save
machinery, and a "grading workflow" that was a stack of PDFs and a biro.
[`planning/LESSONS_FROM_THE_EXPERIMENTS.md`](planning/LESSONS_FROM_THE_EXPERIMENTS.md)
is the full audit. dewmark is the same idea built deliberately, as one system
with one source of truth per exam.

## The five pieces

Three experiences, joined by two formats:

1. **The source format** — one file per exam, markdown or Python, that a
   teacher writes directly, edits in the composer, or produces by translating
   an old paper (a job an LLM does well when the format is documented and the
   compiler validates hard). Spec: [`planning/SOURCE_FORMAT.md`](planning/SOURCE_FORMAT.md).
2. **The composer** — compiles a source file into the exam's variants
   (student paper, no-Python backup, assessor key, marking pack), first as a
   command-line builder, later as a page with preview and structured editing.
   Spec: [`planning/COMPOSER.md`](planning/COMPOSER.md).
3. **The exam runner** — the page the student sits. Identity, questions,
   answer fields, code cells where the exam has them, autosave to browser and
   to a file, and a finish step that packages the submission. Spec:
   [`planning/EXAM_RUNNER.md`](planning/EXAM_RUNNER.md).
4. **The submission format** — what leaves the student's machine: one zip
   holding a machine-readable answers file and a human-readable snapshot.
   Spec: [`planning/SUBMISSION_FORMAT.md`](planning/SUBMISSION_FORMAT.md).
5. **The grading workbench** — points at a folder of submissions, shows each
   answer beside the marking scheme, records part-by-part marks and feedback,
   and exports graded PDFs and a marks sheet. Spec:
   [`planning/GRADING_WORKBENCH.md`](planning/GRADING_WORKBENCH.md).

Two cross-cutting documents:
[`planning/STYLE_AND_READABILITY.md`](planning/STYLE_AND_READABILITY.md) for
the visual family, print rules, and accessibility, and
[`planning/OPEN_QUESTIONS.md`](planning/OPEN_QUESTIONS.md) for everything not
yet decided, in the same four-part form the rest of the repository uses.
Build order is in [`planning/ROADMAP.md`](planning/ROADMAP.md).

## How dewmark relates to dewlab

dewlab's pre-build questions settled this boundary before dewmark existed:
assessment tooling does not merge into the tutorials — anything exam-shaped
stays on its own track, offline, though it should look like it belongs to the
same family of materials (planning/OPEN_QUESTIONS.md, Q4 in the root
planning folder). dewmark lives inside this repository because the two tracks
share machinery and an author, not because they share a surface. Concretely:

- **Shared**: the `--dl-*` design tokens and typeface family from
  `assets/tutorial-style.css`; the vendored CodeMirror and KaTeX bundles; the
  fence-with-header-lines source convention; the Pyodide engine and the
  classic-script standalone build; the repository's habits — one
  `docs/<file>-explained.md` per code file, numbered decisions, questions
  recorded with their costs.
- **Separate**: dewmark has its own builder (an exam is a sealed single-file
  artefact with no site navigation — a different compilation target from a
  tutorial page), its own storage keys, and its own planning folder. Student
  tutorial pages never link to dewmark, and tutorials continue not to name
  assessments (DECISIONS_LOG 7.9).
- **Never in this repository**: real exam content. dewlab is public and
  published. Exam sources are secret until sat, and student submissions are
  personal data always. Both live outside the repo — see OPEN_QUESTIONS
  DM-1 for where. What is committed here is the tooling, the format
  documentation, and openly-shareable sample exams.

## Where things will live

```text
dewmark/
  README.md            this file
  planning/            the specifications and open questions
  build_exam.py        source in, exam variants out          (phase 1)
  assets/              runner shell, styles, exam runtime    (phase 1)
  workbench/           the grading workbench page            (phase 2)
  composer/            the web composer page                 (phase 4)
  samples/             openly-shareable sample exams          (phase 1)
  docs/                format guide for authors and for LLM translation
```

## Status

Specification. Nothing is built yet; no assessments or students are waiting
on it. The specifications are written to be argued with first.
