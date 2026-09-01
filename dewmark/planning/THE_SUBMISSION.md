# The submission

The submission is what a student hands in at the end of a dewmark exam.
It is one compressed folder — a `.zip` file — that the exam page
produces when the student finishes. The student uploads it to whatever
the class already uses for handing work in, usually a Moodle assignment,
and the teacher later downloads all the submissions into one folder for
marking.

This document describes what is inside the file, how the file is named,
and the rules its contents follow. The design goal throughout is that a
folder of submissions is a complete and self-explaining record of the
sitting: a person can open any submission and read it with no special
software, and the marking workbench can process it without a server.

## 1. The name of the file

Each submission is named from the exam's code and the student's details:

```text
dewmark_sample-algebra-2027_s12345_nitt-agnes.zip
```

The pattern is `dewmark_<exam code>_<student number>_<surname>-<first
name>.zip`, with everything reduced to plain lower-case letters,
numbers, and hyphens. A folder listing of submissions therefore already
reads as a class list. The name is a convenience; the authoritative
copy of the student's details lives inside the file, so a renamed file
loses nothing.

## 2. What is inside

The zip contains exactly two files.

**`answers.json`** holds the student's answers in a structured form.
JSON is a widely used plain-text format for structured data; it can be
opened in any text editor, and programs can read it reliably. The file
records:

- which exam and which version of it was sat, by its code;
- the student's identifying details as typed;
- when the sitting started, when it was last saved, and when it was
  finished;
- every answer, stored under the answer space's permanent name — the
  text typed into a written answer, the option chosen in a multiple
  choice question, the value of each blank, each table cell, and each
  numeric box, and for Python questions the student's code, everything
  it printed or drew on its last run, and whether the code was edited
  after that run;
- which questions were attempted in each "answer any N" section.

Three rules keep this file trustworthy. Every answer is stored under a
name, never by position, so adding a question to next year's paper can
never shift this year's answers into the wrong places. The file
contains only data — text, numbers, and images — and no formatting or
program code, so the marking workbench can display a submission without
running anything from it. And the file carries a format version number,
so a future tool that meets an older submission knows exactly what it
is reading.

**`your-exam.html`** is a readable copy of the whole paper with the
student's answers shown in place. It is an ordinary web page with no
program code inside; opening it in any browser shows the exam as the
student left it, and printing it produces a paper copy. This file
exists for people rather than for tools: it is the student's own
record, the copy an external examiner can leaf through, and the
document that settles a query years later. The marking workbench never
reads it — marking works entirely from `answers.json`.

## 3. Saving during the exam uses the same file

While the student works, the exam page continuously saves
`answers.json` — to the browser's own storage and, where the student
chose one, to an answer file on disk. The file saved during the exam
and the file inside the submission are the same thing in the same
format. Finishing adds nothing except the readable copy and the zip
wrapping. Two consequences follow. A student whose sitting ended
abruptly — a power cut, a fire alarm — has lost nothing: their answer
file, as last saved, can be handed in directly and the marking
workbench accepts it exactly as it accepts a finished submission,
marked as "collected without a finish step" so the marker knows. And
restoring an interrupted sitting is the same operation as opening a
submission, so that code path is exercised constantly rather than only
in emergencies.

## 4. Duplicates and versions

Students sometimes hand in twice — most often when an invigilator
grants extra time after a first download. Every saved file carries the
time of its last save, and the marking workbench treats the newest file
for each student number as the one to mark, keeps the older ones
visible, and lets the marker override the choice. The workbench also
compares each submission's exam version against the marking scheme's
version and flags any mismatch, which catches the case where a
corrected paper was issued after some students had already downloaded
the original.

## 5. Privacy

A submission contains a student's name, student number, and exam
answers, and it must be handled as personal data. Submissions are never
committed to a public place, and dewmark's own tools never transmit
them anywhere: the exam page writes the submission to the student's own
machine, and the marking workbench reads submissions from a folder on
the teacher's machine. Storage between those two points — Moodle, a
college network drive — is governed by the institution's existing
policies, which already cover exam scripts.
