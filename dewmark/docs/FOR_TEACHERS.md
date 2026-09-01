# dewmark for teachers

This guide walks through running an exam with dewmark, from an exam you
already have to a marks spreadsheet. It assumes no programming
knowledge. Where a step differs between browsers, the guide says so;
Chrome and Edge support everything below, and the differences on other
browsers are noted where they occur.

## 1. Get your exam into a dewmark exam file

A dewmark exam lives in one plain-text file called the exam file. There
are two ways to get one.

**Convert an exam you already have.** Give your existing exam — a Word
document, a PDF, or plain text — together with its marking scheme to
the translation assistant, which produces the exam file and checks it.
You then read the result as a normal exam paper (not as a text file)
and correct anything that came through wrongly. The assistant follows
strict rules: it never invents marks, and any model answer it drafted
rather than copied is labelled as a draft until you approve it. The
full route is described in
[../planning/TRANSLATING_AN_EXISTING_EXAM.md](../planning/TRANSLATING_AN_EXISTING_EXAM.md).

**Write the exam file directly.** The file format is documented in
[../planning/THE_EXAM_FILE.md](../planning/THE_EXAM_FILE.md), and the
sample in [../samples/sample-mixed-paper.exam.md](../samples/sample-mixed-paper.exam.md)
shows a complete paper that mixes eight question types. Four further
samples show the shapes real papers take.

- [../samples/maths-for-it-5n18396.exam.md](../samples/maths-for-it-5n18396.exam.md)
  is a 120-mark mathematics paper with "answer any N" sections, a
  calculator, a formula sheet in the side panel, and diagrams in the
  questions.
- [../samples/hvit-database-practical.exam.md](../samples/hvit-database-practical.exam.md)
  is a database practical made entirely of Python code questions,
  with a database and two spreadsheets embedded.
- [../samples/sample-biology-paper.exam.md](../samples/sample-biology-paper.exam.md)
  is a science paper: fill-in-the-blank, diagram labelling, a table,
  a calculation, a sketch description, and long explanatory answers
  marked with guidance.
- [../samples/sample-essay-paper.exam.md](../samples/sample-essay-paper.exam.md)
  is a writing paper: reading questions on a passage, a choice of
  three 40-mark essay titles, and a formal letter, all marked with
  criteria grids.

Copying the sample nearest your paper and replacing its questions is
a reasonable way to start.

Every question type available to you — from multiple choice to essays
with marking criteria — is explained, with what students see and how
marking works, in
[../planning/QUESTION_TYPES_AND_MARKING.md](../planning/QUESTION_TYPES_AND_MARKING.md).

## 2. Build the exam

Building turns the exam file into the finished pages. On a computer
with Python installed, run:

```sh
python dewmark/build_exam.py my-exam.md --output finished/
```

If anything in the file is wrong — marks that do not add up, a missing
picture, a question that would reveal its own answer — the builder
stops and lists every problem with the line it is on. Fix the file and
run it again. When the file is clean, the `finished/` folder holds four
things:

- `my-exam-code.student.html` — the paper your students sit;
- `my-exam-code.practice.html` — the same paper with the hints kept,
  for revision;
- `my-exam-code.answer-key.html` — the paper with model answers shown,
  for you and any second marker;
- `dewmark_my-exam-code_marking_scheme.json` — the file the marking
  workbench reads. Keep this one to yourself.

Before the real sitting, open the student page and sit the paper
yourself. Reading your own exam as a student finds more problems than
any automatic check.

## 3. Distribute the paper and run the sitting

Give students the single student file through whatever you already use
— a Moodle assignment, a shared folder, or a USB stick. The page works
offline: a student can double-click the file with no internet
connection and sit the whole exam. (The exception is exams containing
Python programming tasks: the first time the page runs code it
downloads the Python system, about thirty megabytes, so those exams
need either an internet connection or a copy of the Python system
served from a machine in the room. Rehearse this on the room's own
computers before a real sitting.)

When a student opens the page they type their name and student number
and press Begin. On Chrome and Edge the page then asks them to choose
where their answer file is kept — their home folder or a USB stick —
and saves into it automatically as they work; on other browsers they
use the "Save a copy" button regularly instead. The page also saves
into the browser itself after every change, so a crash or an
accidental close loses nothing: reopening the page offers to continue
from the saved work.

When a student presses "Finish exam", the page shows them anything
still empty, confirms their details, and downloads one file named after
the exam and the student, for example
`dewmark_sample-mixed-2027_s12345_nitt-agnes.zip`. They upload that
file to the assignment you named. If you grant extra time, they keep
working and download again; you mark the newest file.

If a student's computer fails before they finish, their answer file —
the one chosen at Begin — can be handed in directly. The marking
workbench accepts it and tells you it arrived without the finish step.

## 4. Mark the exam

Download all the submissions into one folder. Open
`dewmark/workbench/index.html` in Chrome or Edge, load the marking
scheme file from step 2, and open the submissions folder. You will see
a class list with each student's attempts and marking status.

Open a paper and work through it: each answer appears beside its model
answer and marking scheme, and you enter the marks. Points-list schemes
("any three of the following") appear as boxes you tick, and the total
stops at the limit. Essay criteria appear with their mark bands. Every
answer takes an optional feedback comment, and each paper takes a
closing comment. You can also mark one question across every student,
which many markers find keeps their standard steadier.

Your marking saves into the submissions folder as you go, so you can
stop and continue another day, or move the folder to another computer.

In sections where students chose which questions to answer, the
workbench marks everything attempted and counts the best scores toward
the total, showing you which questions counted.

## 5. Return the papers and export the marks

From any marked paper, "Graded paper" opens a printable page with the
student's answers, marks, and your feedback; print it to PDF and return
it through Moodle. "Export marks" produces two spreadsheet files that
open in Excel: the marks, one row per student with one column per
question, and a companion file explaining what every column means, for
an assessor or external authenticator. The submissions folder itself —
submissions, scheme, marking record, exports — is the complete record
of the exam, and it never left your computer.

## Before a first real sitting

- Sit the built paper yourself, start to finish, on the kind of
  computer the exam room has.
- Run one rehearsal in the room: open the page on a machine with the
  network off and check that it works.
- Agree with your quality-assurance colleagues how "answer any N"
  sections are counted; the workbench defaults to counting the best N
  and records which questions counted.
- Decide where submissions will be stored after marking; they contain
  student names, numbers, and exam answers, and your institution's
  rules for exam scripts apply to them.
