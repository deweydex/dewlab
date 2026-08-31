# Roadmap

This document sets the order of building. The order follows two rules.
Each phase must end with something a real exam could use, and the
riskiest unknowns — whether the exam file format can express real
papers, and whether the marking workbench suits a real marking session
— must meet reality as early as possible.

Exams without Python code questions come first throughout, because they
exercise the whole pipeline (file, builder, exam page, saving,
submission, marking, exports) while needing no internet connection at
any point, which is the strictest and simplest case to prove.

## Phase 1 — the exam file, the builder, and the exam page

Build the exam builder with its full set of checks, and the exam page
for every question type except Python code: multiple choice,
fill-in-the-blank, short and long written answers, essays, numeric
answers, table completion, sketch description, and diagram labelling.
Build the three layers of saving, the finish step, and the submission
file.

The phase is finished when two real past papers, converted into exam
files, can each be sat start to finish on a computer with its network
disabled, producing a valid submission: one structured mathematics
paper, and one paper that mixes written types — fill-in-the-blank,
diagram labelling, and long answers — to prove that mixing works from
the first version. An openly shareable sample exam using every
non-code question type is published in the `samples/` folder.

## Phase 2 — the marking workbench

Build the workbench: opening a submissions folder, the class list,
marking paper by paper and question by question, all three marking
methods, feedback, the saved marking record, and the exports (graded
papers and the marks spreadsheet with its companion sheet).

The phase is finished when a full mock marking session has been run —
a folder of realistic submissions marked end to end — and the exports
have been read cold by someone outside the project, standing in for an
assessor. This phase is expected to send corrections back into the
earlier documents; no part of dewmark has less precedent than the
workbench, so its design earns trust only through use.

## Phase 3 — Python code questions

Add the Python code question type: the in-browser code editor and
runner, set-up code, provided read-only code, embedded data files, the
recording of code and outputs into the submission, and the workbench's
display and re-run of code answers.

The phase is finished when a real database practical, converted into
an exam file, has been sat under the exam-room checklist — including
one run in a room whose internet was deliberately unavailable, using a
locally served copy of the Python system.

## Phase 4 — translation and guided creation

Build the translation assistant described in
[TRANSLATING_AN_EXISTING_EXAM.md](TRANSLATING_AN_EXISTING_EXAM.md),
including the draft-labelling rules and the checking loop against the
builder, and the descriptor-reading assistant that suggests question
types. Write the teacher-facing guides: converting an exam, the
exam-room checklist, and the marking guide. Then, if direct use by
other teachers demands it, build the point-and-click creation tool with
its question-type checklist.

## Phase 5 — improvements that use has justified

Later additions are taken up only when a real session has shown the
need, and each is listed in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md)
until then: one-step export of all graded papers as PDF files, a native
Excel marks file, passage-level comments on essays, and further
question types.

## Standing rules for every phase

Every program file lands together with its explanation document and its
automated tests, following dewlab's conventions. Every decision that
closes an open question is recorded in the repository's decision log.
Before any real exam is sat, the saved-data formats — the exam file,
the submission, the marking record — are frozen and documented, because
real submissions must remain readable for years. And no real exam
content or student submission is ever committed to this repository.
