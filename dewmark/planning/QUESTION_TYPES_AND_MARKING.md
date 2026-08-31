# Question types and ways of marking

This document is the shared catalogue for every dewmark exam. It defines
each kind of question an exam can ask, and each way an answer can be
marked. Every other dewmark document refers back to it.

Three terms are used throughout, so here are their definitions. A
**question** is one numbered task on the paper, for example "Question A3".
A question contains one or more **answer spaces**: the concrete places
where a student puts something, such as a text box, a set of blanks in a
sentence, or a code editor. Every question and every answer space has a
short permanent **name**, such as `a3` or `a3.roots`. The name never
changes once an exam has been sat, because saved answers, marks, and
spreadsheet columns are all attached to these names.

The examples in this document show fragments of an exam file. An exam
file is one plain-text file that describes a whole exam; its full layout
is defined in [THE_EXAM_FILE.md](THE_EXAM_FILE.md). For reading this
document, one piece of that layout is enough: a **settings block**. A
settings block is a short list of labelled values. It begins with a line
of three backticks (the backtick is the ` character) followed by the
block's kind, it holds one setting per line in the form `marks: 4`, and
it ends with a line of three backticks.

## 1. An exam can mix any question types

An exam is not one kind of thing. A biology paper might use
fill-in-the-blank, diagram labelling, and long written answers. A
mathematics paper might use numeric answers, sketch descriptions, and
table completion. A programming practical might mix Python code tasks
with short written reflections. An English paper might consist of one
essay. All of these are ordinary dewmark exams, and one exam may combine
any of the types in this catalogue.

When a teacher creates an exam, they choose which question types it will
use. That choice can happen in three ways.

- **By writing the exam file directly.** The types an exam uses are
  simply the types that appear in the file. Nothing needs to be declared
  in advance.
- **By ticking a list.** The planned guided creation tool shows the
  catalogue as a list with checkboxes. The teacher ticks the types their
  exam will use, and the tool prepares an exam file skeleton containing
  only those.
- **By starting from a module descriptor.** A module descriptor is the
  official document that states what a module teaches and how it is
  assessed. A planned assistant reads the descriptor and suggests which
  question types fit the module and which are unlikely — for example, it
  would not suggest Python code tasks for a literature module. These are
  suggestions only. The teacher can always add or remove any type, and
  nothing in dewmark ever refuses a type because of what a descriptor
  says.

The choice of types has practical consequences. The exam builder
includes in the finished exam page only the machinery the chosen types
need. In particular, an exam with no Python code tasks produces a page
that works with no internet connection at all, while an exam with Python
code tasks needs to download the Python system once before the sitting
(see [THE_EXAM_PAGE.md](THE_EXAM_PAGE.md)). The marking workbench
likewise prepares a marking screen suited to each type.

## 2. The ways of marking

dewmark does not mark anything automatically. A person awards every
mark. What dewmark provides is structure: each answer space carries a
number of marks and a marking method, the marking workbench shows the
marker the student's answer beside the marking scheme, and the marks the
marker enters flow into the totals and the spreadsheet without any
retyping. The reason for keeping a person in charge is practical as well
as principled: written answers need judgement, and even a
multiple-choice answer is confirmed by the marker with a single
keypress, so that the person signing the results has seen every decision.

There are three marking methods. Every answer space uses exactly one of
them, and one exam may use all three across its questions.

### 2.1 Marks out of a total

This is the ordinary method. The answer space is worth a fixed number of
marks, and the marker awards any amount from zero up to that number, in
half-mark steps. The marking scheme may add short guidance lines that
say what each mark is for:

```marking
marks: 2
guidance:
  - 1 mark for a correct method, shown in the working
  - 1 mark for the correct final value
```

The guidance lines are advice for the marker. The marker still enters
one number for the answer space.

### 2.2 A points list with a limit

Many marking schemes take the form "any three of the following points,
two marks each". The scheme lists more creditable points than the
answer space is worth, and the total is capped. In dewmark this is
written as a list of points, each with its marks, plus a limit:

```marking
limit: 6
points:
  - 2 marks - names the optimum temperature or describes it
  - 2 marks - explains denaturation above the optimum
  - 2 marks - gives a named enzyme with its substrate
  - 2 marks - states that the rate rises with temperature below the optimum
```

In the marking workbench, each point appears as a line the marker ticks
when the student's answer contains it. The workbench adds up the ticked
points and stops counting at the limit. The marker can still adjust the
final number by hand, for example to award one mark for a half-made
point.

### 2.3 A criteria grid

Long pieces of writing are usually judged on qualities rather than
points: how well the argument holds together, how well the evidence is
used, how clear the language is. Each such quality is called a
**criterion**, and each criterion carries some of the marks and a set of
**mark bands** — ranges of marks with a description of the work that
earns them. A criteria grid for a 60-mark essay might look like this:

```marking
criteria:
  - name: Argument and structure
    marks: 20
    bands:
      - 16 to 20 - a sustained line of argument; each paragraph builds
        on the one before
      - 10 to 15 - a clear position, developed unevenly
      - 0 to 9 - description without an argument
  - name: Use of sources
    marks: 20
    bands:
      - 16 to 20 - sources are chosen well and woven into the argument
      - 10 to 15 - sources are present but summarised rather than used
      - 0 to 9 - little or no use of sources
  - name: Language and register
    marks: 20
    bands:
      - 16 to 20 - precise, controlled prose in an appropriate register
      - 10 to 15 - clear prose with lapses in precision or register
      - 0 to 9 - meaning is often unclear
```

In the marking workbench, the grid appears with the bands visible. The
marker reads the essay, chooses a band for each criterion, sets the
exact mark within the band, and may write a comment per criterion. The
criterion marks add up to the answer space's total.

### 2.4 Rules that apply to all three methods

**Feedback.** Whatever the method, the marker can write feedback: a
short comment on any answer space, and a longer closing comment on the
whole paper. Feedback appears on the graded paper the student receives.

**Blank answers.** An answer space the student never touched is shown to
the marker as "not attempted" and scores zero without any typing. An
answer space the student opened and left empty is shown as "left blank",
so the marker can tell the difference. Neither case ever blocks marking
the rest of the paper.

**"Answer any N" sections.** An exam section may tell students to answer
a subset of its questions, for example "answer any ten of the twelve
questions in Section A". dewmark handles this as follows. The exam page
counts how many questions the student has attempted and shows the count,
but it never prevents a student from attempting more than the required
number. At marking time, the workbench marks everything the student
attempted, counts the best N question totals towards the section total,
shows the marker which questions were counted, and lets the marker
change that selection. Whether "best N" is the right counting rule is a
policy decision for each institution; the workbench records which
questions were counted, so the rule can be checked afterwards.

**Where the marks go.** Every mark the marker enters is stored against
the answer space's name. The exported spreadsheet has one column per
question, with the question's name and its available marks in the column
heading, plus section totals and the paper total. A companion sheet
lists every name with the question text it belongs to, so an assessor
can read what each column means without opening any tool. The details
are in [THE_MARKING_WORKBENCH.md](THE_MARKING_WORKBENCH.md).

## 3. The catalogue of question types

Each entry below explains what the type is for, what the student sees on
the exam page, what the teacher writes in the exam file, and how the
type is usually marked, followed by the nuances worth knowing before
choosing it. The example fragments are complete enough to copy and
adapt.

The type of an answer space is written in its settings block as
`type: multiple-choice`, `type: fill-in-the-blank`, and so on. The type
names are deliberately spelled out in full, so that anyone reading the
exam file can say what each part of the exam is without a reference
card.

### 3.1 Multiple choice — `multiple-choice`

**What it is for.** Checking recognition and quick judgement: one
question, a small set of options, one correct choice (or several, if the
teacher says so).

**What the student sees.** The question text followed by the options,
each with a button to select it. The selected option is highlighted.
Options can be short texts or small pictures — for example, four small
graphs from which the student picks the correct shape.

**What the teacher writes.**

```answer
name: a7.choice
type: multiple-choice
marks: 2
options:
  - y = 2x + 1
  - y = x^2 + 1
  - y = 2^x
  - y = 1/x
correct: 3
```

The `correct` setting names the right option by its position in the
list. It goes only into the marking scheme and the answer key; the exam
page the students receive contains no trace of it.

**How it is marked.** Marks out of a total. The workbench shows the
student's choice beside the correct one, and the marker confirms with
one keypress.

**Nuances.** dewmark does not subtract marks for a wrong choice; a wrong
or missing choice simply scores zero. The options appear in the same
order for every student, because a fixed order keeps the printed paper,
the marking discussion, and any appeal talking about the same "option
3". To let a student choose more than one option, add
`choose: several`; the marking scheme then states which combination
earns which marks, and the marker applies it.

### 3.2 Fill in the blank — `fill-in-the-blank`

**What it is for.** Checking recall of specific terms inside a sentence
or short passage.

**What the student sees.** The sentence with typing boxes where words
have been removed.

**What the teacher writes.** The full sentence, with each removed word
wrapped in curly brackets:

```answer
name: b1.cell
type: fill-in-the-blank
marks: 3
text: |
  The {mitochondrion} is the site of aerobic respiration. The cell's
  genetic material is held in the {nucleus}, and proteins are assembled
  at the {ribosomes}.
```

The words in curly brackets become the blanks. The students see empty
boxes; the expected words go into the marking scheme.

**How it is marked.** Marks out of a total, normally one mark per blank.
The workbench shows each blank's expected word beside what the student
typed.

**Nuances.** Spelling and near-misses need a human decision: is
"mitochondria" acceptable for "mitochondrion"? The marking scheme can
list accepted alternatives for any blank, and the marker decides the
cases the list does not cover. If the removed words could be guessed
from grammar alone, the question tests reading rather than knowledge;
that is a question-writing matter, not a tool matter, but it is the most
common weakness of this type.

### 3.3 Short written answer — `short-written-answer`

**What it is for.** Definitions, single statements, and brief
calculations explained in a sentence or two. Typical worth: one to four
marks.

**What the student sees.** The prompt followed by a text box a few lines
tall. The box grows if the student writes more; the starting size only
suggests how much is expected.

**What the teacher writes.**

```answer
name: a4.catalyst
type: short-written-answer
marks: 2
prompt: State what is meant by a catalyst.
model_answer: |
  A substance that speeds up a chemical reaction without being used up
  by the reaction.
```

**How it is marked.** Marks out of a total, usually with a model answer
and a guidance line or two.

**Nuances.** Students type plain text. For science and mathematics
answers this raises the question of symbols: how does a student type
H₂O or x²? The exam page provides a small palette of common symbols and
accepts spelled-out forms such as `x^2`; the exact conventions are an
open question recorded in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md), and
markers are told to accept any unambiguous form.

### 3.4 Long written answer — `long-written-answer`

**What it is for.** Explanations, comparisons, and descriptions that
need a paragraph or more but are not full essays. Typical worth: five to
twelve marks.

**What the student sees.** The prompt above a larger text box, sized to
match the marks available.

**What the teacher writes.**

```answer
name: a4.temperature
type: long-written-answer
marks: 6
prompt: |
  Explain, with one named example, how temperature affects enzyme
  activity.
```

followed by a marking block, most often a points list with a limit (see
section 2.2), because that is how examining bodies usually publish
schemes for this kind of question.

**How it is marked.** Any of the three methods fits. The points list
with a limit is the usual choice.

**Nuances.** The size of the box quietly tells the student how much to
write, so the builder sets it from the marks available; the teacher can
override it. Answers are plain text with the same symbol conventions as
short written answers.

### 3.5 Essay — `essay`

**What it is for.** A sustained piece of writing judged on its quality
as a whole: literature, history, discussion questions, reflective
pieces. An essay is often the entire exam.

**What the student sees.** The essay title stays visible in a small
strip at the top, and the rest of the screen becomes a full-width
writing area with a live word count. If the exam sets a guide length,
the count shows progress against it without enforcing it. A separate
planning box sits above the writing area; whatever the student puts
there is saved and handed in, but it is labelled as planning and carries
no marks, so students can outline freely.

**What the teacher writes.**

```answer
name: e1.essay
type: essay
marks: 60
guide_words: 800
planning_box: yes
```

with a criteria grid (section 2.3) as its marking block. The essay
title and any source material are ordinary written content placed above
the answer block in the exam file.

**How it is marked.** A criteria grid. The workbench shows the full
essay beside the grid; the marker chooses a band and a mark for each
criterion and may comment on each.

**Nuances.** Exams commonly offer a choice of titles — "answer one of
the following three". That is an "answer any N" section with N equal to
one; each title is its own question. The marker's comments currently
attach to criteria and to the paper as a whole, not to particular
sentences; attaching a comment to a chosen passage of the essay is a
planned improvement, recorded in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
Finally, a note on scope: dewmark's essay type is for essays written
under exam conditions in a supervised room. Take-home assignments are
collected and managed perfectly well by systems such as Moodle, and
dewmark does not try to replace them.

### 3.6 Numeric answer — `numeric-answer`

**What it is for.** Calculations whose result is a number or a small set
of numbers, with the working shown.

**What the student sees.** One or more labelled boxes for the final
values, and a working box beneath them where the student shows the
steps.

**What the teacher writes.**

```answer
name: a3.roots
type: numeric-answer
marks: 4
boxes:
  - label: "x ="
    expected: 4
  - label: "x ="
    expected: -2
working_box: yes
```

**How it is marked.** Marks out of a total, with guidance lines that
usually split the marks between method and result. The expected values
go into the marking scheme, never into the students' page.

**Nuances.** Method marks are the reason the working box exists: a
wrong final value with correct method usually earns partial credit, and
the marker can only award it if the working is there. The marking
scheme can state an accepted range for rounded answers, for example
"accept 3.14 to 3.142". Units are part of the answer where they apply,
and the guidance should say whether a missing unit costs a mark.

### 3.7 Complete the table — `complete-the-table`

**What it is for.** Values calculated across a range, comparisons laid
out side by side, and any answer whose natural shape is a grid.

**What the student sees.** A table in which some cells already contain
values and the remaining cells are typing boxes.

**What the teacher writes.** The table with a question mark in each cell
the student must fill:

```answer
name: b2.table
type: complete-the-table
marks: 5
columns: [x, -2, -1, 0, 1, 2]
rows:
  - [y, "?", "?", 0, "?", "?"]
```

**How it is marked.** Marks out of a total, split across the cells; by
default each empty cell carries an equal share, and the marking block
can assign shares differently.

**Nuances.** Each cell is checked separately, so one wrong value costs
only that cell's share. If later cells depend on earlier ones, the
guidance should tell the marker whether to follow the student's own
earlier value through — examining bodies usually do, under the name
"error carried forward" — because that rule changes how the marks fall.

### 3.8 Describe a sketch — `describe-a-sketch`

**What it is for.** Graph-sketching questions, without asking anyone to
draw with a mouse. Drawing on a computer under time pressure is slow and
uneven across students, and the marks in a sketching question sit in a
handful of features anyway: which way the curve opens, where it crosses
the axes, where its turning points lie. This type asks for exactly those
features.

**What the student sees.** A choice between the possible overall shapes
(shown as small pictures where that helps), followed by labelled boxes
for the features: crossing points, turning points, and whatever else the
question asks for.

**What the teacher writes.**

```answer
name: a3.sketch
type: describe-a-sketch
marks: 4
shape:
  prompt: The parabola opens
  options: ["upward", "downward"]
  correct: 1
features:
  - label: "Crosses the x-axis at ( _ , 0 ) and ( _ , 0 )"
    boxes: 2
    expected: [4, -2]
  - label: "Lowest point at ( _ , _ )"
    boxes: 2
    expected: [1, -9]
```

**How it is marked.** Marks out of a total, split across the shape
choice and the features, with the expected values in the marking
scheme.

**Nuances.** This type trades away one thing: it cannot credit an
unusual but correct freehand sketch, because the features to be
credited are fixed in advance. In return, every student answers the
same well-defined thing, and marking is quick and consistent. For
questions where the drawing itself is the skill being examined, this
type is not a substitute, and dewmark currently has no drawing type; on
paper-based drawing an exam can fall back to "complete this part in the
answer booklet provided".

### 3.9 Label the diagram — `label-the-diagram`

**What it is for.** Anatomy, apparatus, maps, and any picture whose
parts must be named.

**What the student sees.** The picture with numbered pointers, and a
numbered list of typing boxes beside it.

**What the teacher writes.**

```answer
name: b3.cell_diagram
type: label-the-diagram
marks: 3
image: pictures/animal-cell.png
labels:
  - number: 1
    expected: cell membrane
  - number: 2
    expected: cytoplasm
  - number: 3
    expected: nucleus
```

The picture file is named in the exam file and embedded into the exam
page when the exam is built, so the finished page needs no other files.

**How it is marked.** Marks out of a total, normally one per label, with
accepted alternatives listed as for fill-in-the-blank.

**Nuances.** The picture must carry the numbered pointers itself; the
builder checks that the picture exists and that the numbers in the file
match the labels, but it cannot check that pointer 2 really points at
the cytoplasm — the teacher confirms that in the preview. Every picture
also needs a short written description for students using a screen
reader, and the builder refuses an exam whose pictures lack one.

### 3.10 Python code — `python-code`

**What it is for.** Programming and data-handling tasks in which the
student writes real code and runs it: querying a database, cleaning a
table of data, writing and testing a function, drawing a chart.

**What the student sees.** A code editor pre-filled with any starter
code the teacher provides, a Run button, and an output area that shows
whatever the code prints or draws. The code runs inside the student's
own browser using Pyodide, a version of the Python programming language
that runs inside a web page; nothing is sent anywhere.

**What the teacher writes.**

```answer
name: t2.query
type: python-code
marks: 6
starter_code: |
  # Task 2 - find all students enrolled in Temporal Engineering
  # Write your query here:

model_answer_code: |
  results = pd.read_sql(
      "SELECT * FROM students WHERE programme = 'Temporal Engineering'",
      connection)
  show(results)
```

An exam that uses this type can also declare set-up code that runs
before the student starts, provided code shown to the student read-only,
and data files (databases, spreadsheets) that are embedded into the exam
page. [THE_EXAM_FILE.md](THE_EXAM_FILE.md) covers those.

**How it is marked.** Marks out of a total, with guidance lines. The
submission records the student's code, everything the code printed or
drew on its last run, and whether the code was edited after that run —
so the marker knows whether the recorded output really came from the
code on screen. The workbench can also re-run the student's code for
verification.

**Nuances.** This is the one type with a real set-up cost. The Python
system is about thirty megabytes and downloads the first time the page
runs code; after that the browser keeps a copy. An exam room without
internet needs the copy put in place beforehand, either by opening the
page once on each machine the day before or by serving the files from a
laptop in the room. The details, and a checklist for the room, are in
[THE_EXAM_PAGE.md](THE_EXAM_PAGE.md). Because a student's code can also
freeze the page (an accidental endless loop, for example), the exam page
saves continuously and tells students plainly: if the page stops
responding, close it and open it again, and nothing is lost.

## 4. Adding a type later

The catalogue is expected to grow. A new type must state the same four
things as every entry above — purpose, what the student sees, what the
teacher writes, how it is marked — and must pick a spelled-out name that
needs no explanation when read aloud. Tools that meet an exam file
containing a type they do not know must say so clearly and refuse to
build or mark that exam, rather than guessing; a marker must never see
an answer displayed wrongly because their copy of the workbench was
older than the exam.
