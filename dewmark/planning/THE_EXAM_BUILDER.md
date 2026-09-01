# The exam builder

The exam builder is the program that turns an exam file into the
finished exam. It reads the file, checks it thoroughly, and writes out
the web pages and the marking scheme. Nothing reaches a student without
passing through the builder, which is what makes the checks trustworthy:
an exam whose marks do not add up, or whose model answers would leak to
students, cannot be built at all.

## 1. Running the builder

The builder is a Python program, `build_exam.py`, run from a command
line:

```sh
python dewmark/build_exam.py my-exam.md --output finished/
```

For one exam file it produces four things.

- **The exam paper** — the page students sit
  ([THE_EXAM_PAGE.md](THE_EXAM_PAGE.md)). It contains no model answers,
  no expected values, and no marking material.
- **The practice paper** — the same page with the hints kept in (see
  [THE_EXAM_FILE.md](THE_EXAM_FILE.md), section 6), for revision use.
- **The answer key** — a readable copy of the paper with the model
  answers shown in place, for the teacher, a second marker, or an
  external examiner to read on paper.
- **The marking scheme file** — the machine-readable file the marking
  workbench loads
  ([THE_MARKING_WORKBENCH.md](THE_MARKING_WORKBENCH.md)). It never
  leaves the teacher's hands.

A `--check` option runs every check without writing anything, and a
`--preview` option rebuilds automatically whenever the exam file is
saved and opens the result in a browser, so a teacher editing an exam
sees each change within a few seconds. Sitting the built paper
yourself, in the preview, is the single most effective check an exam
gets, and the teacher documentation says so prominently.

The command line will not suit every teacher, and it does not need to:
the translation assistant
([TRANSLATING_AN_EXISTING_EXAM.md](TRANSLATING_AN_EXISTING_EXAM.md))
runs the builder on the teacher's behalf, and a point-and-click version
of building and previewing is planned once the builder itself has
settled.

## 2. What the builder checks

The builder refuses to build a file with any of the following problems,
and reports each one with the line it occurs on and a plain
description.

- The marks of a question's answer spaces do not add up to the
  question's marks, or the questions (after "answer any N" rules) do not
  add up to the exam's stated total.
- A name (of a section, question, or answer space) is missing,
  repeated, or malformed.
- An answer space uses a question type that the catalogue
  ([QUESTION_TYPES_AND_MARKING.md](QUESTION_TYPES_AND_MARKING.md)) does
  not define, or is missing a setting its type requires.
- A picture or data file named in the exam does not exist, or a picture
  lacks the written description that screen-reader users need.
- A section's "answer any N" rule is absent from the front-page
  instructions, so students would not be told about it.
- A `marking` block sits somewhere other than directly after an answer
  space, or an answer space that needs a marking scheme has none.
- Any fragment of a model answer, expected value, or marking scheme
  appears in the built student paper. The builder performs this check
  on its own output, as a final safeguard against its own mistakes.

The builder also produces identical output when run twice on the same
file. That property makes review possible: when a teacher changes one
question and rebuilds, comparing the old and new files shows exactly
that one change and nothing else.

## 3. How the finished pages are put together

Two facts about the builder's output shape everything else, so they are
stated here even though they are technical.

First, the finished exam page is one file with everything inside it.
Pictures and data files are encoded into the page itself, mathematics
is typeset during the build rather than in the student's browser, and
the page's own program code is embedded. The page therefore behaves the
same whether it is opened from Moodle, a network drive, or a USB stick,
and an exam without Python questions runs with no internet connection
at all.

Second, the builder includes only what the exam's question types need.
The catalogue's types each bring their own machinery — a code editor
for Python questions, a picture-and-boxes layout for diagram labelling
— and an exam that does not use a type does not carry its weight. This
is why a purely written exam produces a small page that opens
instantly, while a Python practical produces a larger one that warns
about its one-time download.

## 4. Where the builder lives

The builder is part of the dewlab repository and follows its
conventions: it is one well-commented Python file with a companion
explanation document, and every check listed above has an automated
test. The exam files it reads, being real exam content, live outside
the repository (see the project [README](../README.md)); the repository
carries the builder, these documents, and openly shareable sample
exams.
