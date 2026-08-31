# dewmark

dewmark is a set of tools for running exams in a web browser. A teacher
writes an exam as a single file, and dewmark turns that file into a web
page that students open on an ordinary computer. The page works without a
server and, for most exams, without an internet connection. While a
student works, the page saves their answers continuously. When the
student finishes, the page produces a small set of files that the teacher
collects, marks on their own computer, and turns into graded papers for
the students and a marks spreadsheet for an assessor.

No part of this process sends anything to a server. The exam is a file,
each student's submission is a file, and the marks are a file. Every
stage works from a folder on one computer.

## Who this is for

dewmark is being built inside dewlab, an open teaching project for QQI
Level 5 and 6 computing and mathematics modules in Ireland. The first
users are the teachers of those modules. The design aims further than
that: any teacher who can write an exam in a word processor should be
able to run it through dewmark, whatever the subject. An exam can contain
any mixture of question types — multiple choice, written answers of any
length, essays, calculations, diagram labelling, and live Python
programming tasks — and the documents in this folder explain each type
and each way of marking it in full.

## The parts

dewmark has five parts. Each has its own document in the
[`planning/`](planning/) folder.

1. **The exam file.** A teacher describes a whole exam — the questions,
   the marks, the model answers, and any data files — in one plain-text
   file. [`planning/THE_EXAM_FILE.md`](planning/THE_EXAM_FILE.md)
   explains the file's layout. A teacher can write this file directly,
   or hand an existing exam (a Word document, for example) to an
   assistant that converts it;
   [`planning/TRANSLATING_AN_EXISTING_EXAM.md`](planning/TRANSLATING_AN_EXISTING_EXAM.md)
   explains that route.
2. **The question types and the ways of marking.** One shared catalogue
   defines every kind of question an exam can ask and every way an
   answer can be marked. Any exam may use any mixture.
   [`planning/QUESTION_TYPES_AND_MARKING.md`](planning/QUESTION_TYPES_AND_MARKING.md)
   is the catalogue, and it is the most important document in this
   folder.
3. **The exam builder.** A program checks the exam file for mistakes —
   for example, marks that do not add up — and produces the finished
   web pages: the paper the students sit, a practice version, an answer
   key, and a marking scheme file for the teacher.
   [`planning/THE_EXAM_BUILDER.md`](planning/THE_EXAM_BUILDER.md)
   describes it.
4. **The exam page.** This is the web page a student opens to sit the
   exam. It shows the questions, saves the student's work as they type,
   and packages their answers into a submission when they finish.
   [`planning/THE_EXAM_PAGE.md`](planning/THE_EXAM_PAGE.md) describes
   the sitting from start to finish, and
   [`planning/THE_SUBMISSION.md`](planning/THE_SUBMISSION.md) describes
   exactly what the student hands in.
5. **The marking workbench.** After the exam, the teacher gathers the
   submissions into one folder and opens the marking workbench, a web
   page that reads that folder. The teacher marks each answer against
   the marking scheme, writes feedback, and exports two things: a
   graded paper for each student and a marks spreadsheet for the
   assessor.
   [`planning/THE_MARKING_WORKBENCH.md`](planning/THE_MARKING_WORKBENCH.md)
   describes marking and the exports.

Two further documents cut across the parts.
[`planning/APPEARANCE_AND_READABILITY.md`](planning/APPEARANCE_AND_READABILITY.md)
sets out how the pages look, how they print, and what they promise
students with accessibility needs.
[`planning/OPEN_QUESTIONS.md`](planning/OPEN_QUESTIONS.md) records the
decisions that are not yet made. The order of building is in
[`planning/ROADMAP.md`](planning/ROADMAP.md).

## What already exists

Nothing in this folder is built yet. These documents are the plan. Before
the plan, three exams were built by hand and used in the 2025–2026
academic year; they proved that a browser exam with no server works in a
real exam room, and their faults shaped many of the rules in these
documents.
[`planning/LESSONS_FROM_THE_EXPERIMENTS.md`](planning/LESSONS_FROM_THE_EXPERIMENTS.md)
records what those exams taught, and the [`experiments/`](experiments/)
folder holds corrected copies of them.

## Where exam content lives

This repository is public. Real exam content is secret before students
sit it, and student submissions are personal data at all times, so
neither is ever committed here. This folder holds the tools, the
documentation, and openly shareable sample exams only. Teachers keep
their real exam files and their students' submissions on their own
computers or in private storage.

## Planned folder layout

```text
dewmark/
  README.md         this file
  planning/         the design documents listed above
  experiments/      the corrected 2025-2026 hand-built exams
  build_exam.py     the exam builder (planned)
  assets/           the exam page template and styles (planned)
  workbench/        the marking workbench page (planned)
  samples/          openly shareable sample exams (planned)
  docs/             guides for teachers (planned)
```
