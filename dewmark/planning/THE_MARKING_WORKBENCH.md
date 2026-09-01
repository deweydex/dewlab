# The marking workbench

The marking workbench is the web page a teacher uses to mark a dewmark
exam. Like every part of dewmark it needs no server: the teacher points
it at a folder on their own computer containing the students'
submissions, marks each answer against the marking scheme, and exports
the results. Everything the workbench writes — the marking in progress,
the graded papers, the marks spreadsheet — goes back into that same
folder, so when marking is finished the folder holds the complete
record of the exam: submissions in, scheme, marks, feedback, and
exports.

## 1. Opening a marking session

The workbench needs two inputs.

The first is the **marking scheme file**. When an exam is built, the
exam builder produces this file alongside the student paper (see
[THE_EXAM_BUILDER.md](THE_EXAM_BUILDER.md)). It contains everything
that was stripped out of the students' page: the model answers, the
expected values, the marking guidance, the points lists, and the
criteria grids, all attached to the permanent names of the questions
and answer spaces. It stays on the teacher's machine and is never
distributed.

The second is the **submissions folder**: the folder into which the
teacher has downloaded every student's submission file (see
[THE_SUBMISSION.md](THE_SUBMISSION.md)). In Chrome and Edge, the
workbench opens the folder directly and can save its own files into it;
this is the supported way to mark. Other browsers can open submissions
as individual files but cannot save into the folder, so the marking
record must be exported by hand there — workable, but second-best, and
the workbench says so on its opening screen.

On opening, the workbench reads every submission, checks each one — is
it readable, does it belong to this exam, does its version match the
scheme's — and reports problems as a list rather than stopping: an
unreadable file, a submission from a different exam, two files from the
same student number. For duplicates it selects the newest by save time,
keeps the others visible, and lets the marker change the selection.

A student whose file arrived without the finishing step — a sitting cut
short by a power failure, for example — appears with a note saying so.
Their answers are marked like anyone else's.

The workbench treats everything inside a submission as data to display,
never as instructions to follow. Answers are shown as text, numbers,
tables, and pictures; nothing from a submission is ever executed while
the workbench displays it. This matters because submissions are the
one input that students author, and a marking tool must stay safe even
against a hostile file.

## 2. The class list

The opening view is a table with one row per student: name, number,
when they handed in, how many questions they attempted in each "answer
any N" section, marking status (not started, in progress, finished),
and their running total. From here the marker opens a paper, or
switches to marking by question (section 4).

## 3. Marking one paper

The marking screen shows two columns. On the left is the student's
answer for the current answer space, with the question's wording
available above it (folded away by default, one click to show). On the
right is the marking scheme for that answer space: the model answer or
expected values, and the marking controls for whichever marking method
the answer space uses (the three methods are defined in
[QUESTION_TYPES_AND_MARKING.md](QUESTION_TYPES_AND_MARKING.md),
section 2).

- For **marks out of a total**, the marker types the mark, in half-mark
  steps, with the guidance lines shown alongside.
- For **a points list with a limit**, each point appears with a
  checkbox; the workbench totals the ticked points, stops at the limit,
  and lets the marker adjust the result by hand.
- For **a criteria grid**, the criteria appear with their mark bands and
  descriptions; the marker picks a band and an exact mark per criterion,
  and can comment on each.

The keyboard is enough for the whole flow: digits enter a mark, the
Enter key moves to the next answer space, and a shortcut opens the
feedback box. This matters at scale — a class of twenty-five with
sixty answer spaces each is over a thousand marking decisions, and
reaching for the mouse at each one adds real time.

Every answer space accepts a written feedback comment, and each paper
accepts a closing comment; both appear on the student's graded paper.
The workbench keeps a list of the marker's frequently used phrases —
"show your working", "state the units" — which can be inserted with two
keys and then edited freely; an inserted phrase becomes ordinary text
on that paper, so later changes to the phrase list never alter feedback
already given.

For Python code questions the workbench shows the student's code and
its recorded output, with a clear warning when the submission records
that the code was edited after its last run — in that case the output
on file did not come from the code on screen. The workbench can also
re-run the student's code, using the same data files the exam embedded,
when the marker wants to verify behaviour; the recorded output remains
the primary evidence, since it shows what the student actually saw.

Totals update as marks are entered: the answer space's question, its
section (with any "answer any N" rule applied and the counted questions
indicated), and the paper. The marker can override which questions
count towards an "answer any N" section; the workbench records the
final selection.

## 4. Marking by question

The workbench also marks across papers: pick one answer space — every
student's answer to question A3, say — and mark down the stack with the
same controls. Marking this way applies the same standard to the first
and the twenty-fifth answer more consistently than paper-by-paper
marking does, and many markers prefer it for written questions. A
checkbox hides students' names in this view, for markers who want to
judge answers without seeing whose they are. Both views read and write
the same marking record, so a marker can switch freely.

## 5. How the marking is saved

The workbench saves the marking record into the submissions folder
after every change, under a name built from the exam's code. The record
holds every mark against its answer space's name, every ticked point
and chosen band, every comment, the counted-question selections, and
the marker's name. Totals are recalculated from the individual marks
whenever the record is loaded, so an inconsistency cannot survive
unnoticed. Because the record sits in the folder, marking can stop and
resume across days or move to another computer along with the folder.

## 6. The exports

When marking is finished, the workbench writes its exports into an
`exports` folder beside the submissions.

**A graded paper for each student.** This is the student's own paper
with the marks and feedback laid into it: each answer followed by its
mark, the counted questions indicated, the totals at the top, and the
closing comment at the end. The workbench produces it as a printable
page per student; the teacher prints each to PDF for return through
Moodle. Producing all the PDFs in one step, rather than one print
dialog per student, is planned but not yet designed — the options are
recorded in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

**The marks spreadsheet.** A table with one row per student and one
column per question, plus section totals (with "answer any N" applied),
the paper total, and the marking status. The column headings carry the
question names and their available marks, for example `a3 (4)`. The
file is CSV — comma-separated values, a plain table format that Excel
and every spreadsheet program open directly. A companion CSV lists
every question name with its marks, its topic, and its wording, so an
assessor reading the spreadsheet can see what every column means
without opening any other tool.

**The marking record itself** stays in the folder as the audit trail.
An assessor or external authenticator who is handed the folder has the
submissions, the scheme, every marking decision, and the exports, and
can follow any mark from the spreadsheet back to the student's answer.

## 7. What the workbench does not do

The workbench awards no marks on its own. It does not compare a typed
answer against the expected value and pre-fill anything, even for
multiple choice — the marker confirms every mark. Automatic checking
may be worth revisiting once the human workflow has proved itself, and
that question is recorded in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md)
rather than decided here.

The workbench is also not a grade book. It knows one exam at a time,
and combining results across assessments remains the job of the
institution's own records.
