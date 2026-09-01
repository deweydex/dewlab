# The exam page

The exam page is the web page a student opens to sit a dewmark exam. It
is a single file. The teacher distributes it however the class already
receives files — through Moodle, a shared folder, or a USB stick — and
the student opens it in an ordinary web browser. The page contains the
whole exam: every question, every picture, and every data file were
embedded into it when the exam was built. During the sitting the page
talks to no server, sends nothing anywhere, and, for exams without
Python code questions, needs no internet connection at all.

This document describes the sitting from the student's side, in order:
starting, working, saving, finishing, and what happens when something
goes wrong.

## 1. Starting

The page opens on a title screen: the institution and module, the exam's
title, the time allowed, and the front-page instructions from the exam
file. Below the instructions, the student types the identifying details
the exam asks for — usually their full name and student number.

When the student presses Begin, the page sets up saving. Saving works in
two ways at once, and the difference matters enough to explain to the
student on screen, in one sentence each.

- **Saving in the browser.** The browser has a small storage area of its
  own on that computer, and the page writes the student's answers into
  it after every change. This storage survives closing the page and
  restarting the computer, but it belongs to that browser on that
  machine, and some shared computers erase it between logins.
- **Saving to a file.** In Chrome and Edge, a web page can also save
  directly into a file the user chooses. On those browsers, the Begin
  step asks the student to pick a place for their answer file — for
  example their home folder or a USB stick — and from then on the page
  writes their answers into that file after every change. On browsers
  without this ability, the page shows a Save button instead, which
  downloads the current answer file, and it reminds the student to use
  it regularly.

If the student declines to pick a file, the page does not fail silently:
it shows a persistent notice reading "file saving is off — answers are
saved in this browser only", so the student and the invigilator can see
the situation at a glance.

The answer file and the browser copy hold the same content, and that
content is the same thing the student will eventually hand in (see
[THE_SUBMISSION.md](THE_SUBMISSION.md)). There is no separate "save
format": saving during the exam and submitting at the end write the same
file.

## 2. Working through the paper

The paper is one page that scrolls from top to bottom, with a slim bar
fixed at the top showing the exam title, the student's name, the two
saving indicators, and the Finish button. A side panel, which the
student can collapse, lists every question with its marks and shows
which ones have been answered; in a section that says "answer any ten of
twelve", the panel counts the attempts, for example "9 answered of
choose 10". Clicking a question in the panel jumps to it.

The side panel also holds whatever reference material the exam file
provides — a formula sheet, a guide to typing symbols, a list of the
data files in a Python exam — and nothing else. The reference material
comes from the exam file, so students in the room and students
practising at home see exactly the same support.

Each question type from the catalogue
([QUESTION_TYPES_AND_MARKING.md](QUESTION_TYPES_AND_MARKING.md))
displays in its own way: blanks appear inside their sentence, numeric
answers show labelled boxes with a working area, diagram labelling shows
the picture beside its numbered boxes, and Python questions show a code
editor with a Run button. Two types change the page's shape more
substantially.

- **Essays** switch the question into a writing view: the title stays in
  a small strip, the writing area takes the full width, a word count
  updates as the student types, and a separate planning box above the
  writing area is saved but clearly labelled as carrying no marks.
- **Python code questions** share one running Python session across the
  whole exam, like a notebook: a variable defined while answering one
  question is still defined in the next. The page runs any set-up code
  from the exam file automatically before the student starts, so no
  question depends on the student remembering to run something first.

## 3. Saving, restoring, and moving machines

The page saves after every change the student makes, to the browser
storage immediately and to the answer file within a couple of seconds.
Both indicators in the top bar show the time of their last successful
save. If either stops working — a USB stick pulled out, for example —
its indicator changes colour and the page offers to choose a new file,
while the other saving route continues unaffected.

If the page is closed and reopened, it restores the saved answers and
tells the student exactly what happened: "Restored 14 answers saved at
10:41." When the browser copy and an answer file disagree — which
happens when a student moves to a different machine mid-exam — the page
shows both, with their times and how many answers each contains, and
asks the student which to continue from. It never merges the two or
picks one silently.

One honest limit applies to Python questions: restoring brings back the
student's code and the recorded output of each run, but not the running
Python session itself. After a restore, the page states this and the
student re-runs their cells, top to bottom, to rebuild the live state.

## 4. Finishing

The Finish button leads to a checking screen; it does not end anything
by itself. The screen lists, in plain terms, everything worth a look
before handing in: answer spaces that are still empty, listed with their
marks; sections where the student has answered fewer questions than the
"answer any N" rule allows to count; Python code that was edited after
its last run, whose recorded output is therefore out of date; and the
student's name and number, shown for confirmation. Each item links back
to the question it concerns.

When the student confirms, the page produces the submission — one file,
described in [THE_SUBMISSION.md](THE_SUBMISSION.md) — as a download, and
shows the handing-in instructions from the exam file, typically "upload
this file to the Moodle assignment and show the confirmation screen to
your invigilator". Finishing is reversible: if the invigilator grants
more time, the student reopens the exam, continues, and downloads a new
submission. The newest file is the one that counts, and the marking
workbench resolves duplicates by their save times.

## 5. When something goes wrong

Every failure the page can detect produces a message that says three
things in order: what happened, whether the student's work is safe, and
what to do next. The situations designed for, rather than merely
handled, are these.

- **The page freezes.** A Python question can lock the page (an
  accidental endless loop, for example). The remedy is printed in the
  side panel before it is ever needed: close the page, open it again,
  and continue; everything up to the last change is saved.
- **The computer fails.** The student moves to another machine, opens
  the exam page there, and loads their answer file from their USB stick
  or network folder. Work saved only in the first machine's browser
  stays on that machine, which is why the file route exists.
- **The Python system fails to load.** The page says so, explains that
  every written answer still works normally, and offers a retry button.
  Written parts of a mixed exam are never blocked by the code parts.
- **The same exam is open in two windows.** The second window detects
  the first and opens read-only, with an explanation, so two copies
  never save over each other.

## 6. Internet, and the exam room

An exam whose question types include no Python code needs no internet at
any point: the page opens from a local file and everything, including
typeset mathematics, was prepared when the exam was built.

An exam with Python code questions uses Pyodide, a version of the Python
programming language that runs inside the browser. Pyodide is about
thirty megabytes and is downloaded the first time the page runs code;
the browser then keeps a copy. For an exam room this means one
preparation step: open the exam page and run one cell on each machine
the day before, or serve the Pyodide files from a laptop in the room
using the small helper program that dewlab already provides for its
offline bundles. The room checklist in the teacher documentation walks
through both options, and a rehearsal on the room's own machines is part
of the recommended preparation for a first sitting.

## 7. What the exam page does not do

The page does not supervise students. It has no lockdown mode, does not
watch which windows are open, and records no keystrokes; supervision is
the invigilator's job, and a web page that claimed to do it would be
making a false promise. The record it does keep is minimal and is
disclosed to students: when the sitting started, when each save
happened, when each Python cell ran, and when the exam was finished.

The page also awards no marks. It contains no correct answers — the
builder strips them out and verifies that none remain — so nothing about
the exam can be discovered by reading the page's contents, and every
mark a student eventually receives is awarded by a person in the marking
workbench.
