# The exam file

A dewmark exam is described in one plain-text file, called the exam
file. The file holds everything the exam needs: the questions as the
students will read them, the answer spaces, the marks, the marking
scheme, the model answers, and the names of any pictures or data files
the exam uses. The exam builder (see
[THE_EXAM_BUILDER.md](THE_EXAM_BUILDER.md)) reads this file, checks it,
and produces the finished exam pages from it.

A teacher does not have to write this file by hand. Most teachers will
write their exam in a word processor as they always have, and let the
translation assistant convert it — that route is described in
[TRANSLATING_AN_EXISTING_EXAM.md](TRANSLATING_AN_EXISTING_EXAM.md).
Either way, the exam file is the single place where the exam is defined,
and this document explains its layout, because whoever checks a
converted exam, edits one question, or writes an exam directly will read
and change this file.

## 1. The ingredients of the file

The file is written in Markdown, a plain-text writing format: a line
that starts with `#` is a heading, blank lines separate paragraphs, and
text between dollar signs, such as `$x^2 - 2x - 8$`, is typeset as
mathematics when the exam is built. Everything a student will read —
question wording, instructions, source passages — is ordinary Markdown
text.

Mixed in with the text are **settings blocks**. A settings block is a
short list of labelled values that carries the machine-checkable facts:
names, marks, question types, correct answers. A block begins with a
line of three backticks (the backtick is the ` character) followed by
the block's kind, holds one setting per line in the form `marks: 4`, and
ends with a line of three backticks. There are six kinds of block:

- `exam` — one per file, at the top: the exam's overall settings.
- `section` — starts a section of the paper.
- `question` — starts a question.
- `answer` — creates an answer space inside the current question.
- `marking` — attaches a marking scheme to the answer space directly
  above it.
- `reference` — a titled piece of support material, such as a formula
  sheet or a guide to typing notation, shown in the exam page's side
  panel. A reference block carries a `title` and a `text`, and an exam
  may have any number of them.

Two rules govern how blocks relate to the text around them. First,
structure comes only from the blocks: a `section` block runs until the
next `section` block, a `question` block runs until the next `question`
or `section` block, and every `answer` block belongs to the question it
sits inside. Headings in the text are formatting for the reader, and the
tools never read meaning out of them. Second, ordinary text belongs to
whatever section or question is open where it appears, and it is shown
to the student exactly there.

## 2. A complete small example

The following file is a valid two-question exam. It mixes a numeric
question with a written one, which is the normal situation: any exam may
combine any of the question types in
[QUESTION_TYPES_AND_MARKING.md](QUESTION_TYPES_AND_MARKING.md).

````markdown
```exam
title: Sample Paper - Algebra and Reasoning
exam_code: sample-algebra-2027
version: 2027.01.10.1
total_marks: 10
time_allowed: 45 minutes
student_details: [full name, student number]
instructions: |
  Answer both questions. Show your working; a correct answer without
  working may not receive full marks.
```

## Section A

```section
name: A
```

### Question A1

```question
name: a1
marks: 6
topic: quadratic equations
```

Consider the function $f(x) = x^2 - 2x - 8$.

```answer
name: a1.roots
type: numeric-answer
marks: 4
boxes:
  - label: "x ="
    expected: 4
  - label: "x ="
    expected: -2
working_box: yes
```

```marking
marks: 4
guidance:
  - 2 marks for a correct method (factorising or the formula)
  - 1 mark for each correct root
```

```answer
name: a1.why_two
type: short-written-answer
marks: 2
prompt: Explain why this equation has exactly two solutions.
model_answer: |
  The graph of f is a parabola that crosses the x-axis twice, because
  the value under the square root in the formula is positive.
```

### Question A2

```question
name: a2
marks: 4
topic: reasoning
```

```answer
name: a2.always_never
type: long-written-answer
marks: 4
prompt: |
  "The square of a number is always larger than the number." Decide
  whether this claim is true, and justify your answer with examples.
```

```marking
limit: 4
points:
  - 2 marks - gives a counterexample between 0 and 1, or 0 or 1 itself
  - 1 mark - states clearly that the claim is false
  - 1 mark - shows a case where the claim holds
  - 1 mark - states the range of numbers for which the claim fails
```
````

## 3. The exam settings

The `exam` block at the top of the file states the facts about the exam
as a whole.

- `title` — the exam's name as students see it.
- `exam_code` — a short permanent code for this exam, such as
  `sample-algebra-2027`. The code appears in the names of every file the
  exam produces (submissions, marks, graded papers), so it must never
  change once students have sat the exam.
- `version` — a date-based version number in the form `2027.01.10.1`.
  When a teacher corrects a question after building the exam, they raise
  the version; the marking tools warn if a submission and a marking
  scheme come from different versions.
- `total_marks` — the total for the paper. The builder adds up all the
  questions, applies any "answer any N" rules, and refuses the file if
  the result does not equal this number. The teacher's stated total and
  the actual paper can therefore never disagree.
- `time_allowed` — shown to students on the opening screen. The exam
  page does not enforce it; the room's clock and the invigilator do.
- `student_details` — which identifying details the student is asked to
  type before starting, usually full name and student number.
- `calculator` — set to `scientific` to give the exam page a calculator
  in its side panel: a keypad and typed expressions, with square roots,
  powers, and trigonometry in degrees and radians. Leave the setting
  out and the page has no calculator. The calculator works offline,
  keeps no history, and puts nothing into the submission.
- `instructions` — the text of the front-page instructions, including
  any "answer any N of M" wording. The counting rules themselves are
  written in the `section` blocks, so the tools and the instructions
  cannot drift apart: the builder checks that each section's rule is
  mentioned in the instructions.
- `data_files` — a list of files the exam provides to students, such as
  a database or a spreadsheet for Python questions. Each entry names the
  file's `path` beside the exam file, an optional `as` name students see,
  and a one-line `description` for the side panel. Every listed file is
  embedded into the finished exam page when the exam is built. The page
  never fetches a file over the network during the sitting, so a missing
  file is a building error, discovered by the teacher, and never a
  surprise discovered by a student mid-exam.

Two further settings exist only for exams with Python code questions.
`python` lists the Python packages the exam uses (the list may be
empty), and is required whenever the exam contains a Python question, so
the decision to carry the Python system is always visible at the top of
the file. `setup_code` holds code that runs automatically before the
student starts — the place to open a database connection or import the
packages — so no question depends on the student remembering to run
something first. A `question` block may also carry `provided_code`:
read-only code shown to the student that runs automatically when the
exam starts, for questions of the form "here is a program; extend it".

## 4. Sections, questions, and "answer any N"

A `section` block carries the section's `name` and, when the section
lets students choose, a `choose` setting:

```section
name: A
choose: 10
```

This example means "answer any ten of the questions in this section".
How the choice is presented to students and counted at marking time is
described in [QUESTION_TYPES_AND_MARKING.md](QUESTION_TYPES_AND_MARKING.md),
section 2.4.

A `question` block carries the question's `name`, its `marks`, and
optionally a `topic` (a word or two used later in the marks
spreadsheet). The marks of a question's answer spaces must add up to the
question's marks, and the builder refuses the file when they do not.

## 5. Names

Every section, question, and answer space has a `name`: a short lower-case
identifier such as `a1` or `a1.roots`. Names are permanent. Students'
saved answers, the marker's marks, and the spreadsheet columns are all
stored against these names, so renaming a question after an exam has
been sat disconnects real data from it. The builder enforces what it
can — every name must be unique within the exam, and every answer space
must sit inside a question — and the documentation states the rest
plainly: choose names once, before the exam is sat, and never change
them afterwards.

## 6. What stays out of the students' hands

The exam file contains the correct answers: `expected` values, `correct`
options, `model_answer` texts, and every `marking` block. The exam
builder strips all of it out of the paper the students receive, and then
checks its own work by searching the built student page for every model
answer in the file; if any fragment is found, the build stops with an
error. The stripped material goes into two places instead: the answer
key (a readable copy of the paper with the model answers shown) and the
marking scheme file that the marking workbench reads.

Two settings control the amount of help students see, so one exam file
can produce both a practice paper and an exam paper. A `hint` setting on
an answer space holds a prompt that appears inside the empty answer box;
the practice build keeps hints and the exam build removes them. The
builder is told which build to produce; nothing about the file itself
needs to change.

## 7. Checking the file

The exam builder checks the file before it builds anything, and it
reports every problem with the line it occurs on and a plain
description. The full list of checks lives with the builder
([THE_EXAM_BUILDER.md](THE_EXAM_BUILDER.md)); the most important are
that all marks add up, that every name is unique, that every question
type is one the catalogue defines, that every picture and data file
named in the exam exists, that every picture — including one placed in
the question text as `![description](path)` — has a written description
for screen-reader users, and that no model answer leaks into the student
paper. A file that passes every check builds the same finished pages
every time.
