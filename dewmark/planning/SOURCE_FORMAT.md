# The exam source format

One exam is one source file. From it the composer produces every variant —
student paper, no-Python backup, assessor key, marking pack — so the source
must carry everything: prose, structure, marks, answer fields, model
answers, scaffolding, embedded files, and the reference material the student
may use. This document specifies the format; it is also the document an LLM
is handed when translating an old paper, so it errs toward explicitness over
cleverness.

There are two authoring surfaces and one truth:

- **Markdown source** (`.md`) — the primary format. Prose-first, close
  enough to dewlab's tutorial format that an author moves between them
  without relearning fences.
- **Python source** (`.py`) — a small builder API for exams whose content is
  computed: parameterised numbers, generated option plots, per-cohort
  variation. It executes to produce the same structure the markdown parses
  to.
- **The canonical model** (`exam.json`) — what both compile to, and what the
  runner, workbench, and marking pack are defined against. Authors normally
  never see it; the spec for it is at the end of this file, and it is the
  contract the other specs cite.

The compiler validates hard and fails loudly. Every rule below marked
*build error* is enforced, not advised. This is what makes LLM translation
of old exams workable: the model drafts, the compiler refuses everything
malformed, and the loop converges.

## 1. Frontmatter

YAML frontmatter opens the file. Required and optional fields:

```yaml
---
title: "Maths for Information Technology — Final Examination"
exam_id: mit-5n18396-2026-summer     # stable id; goes into every submission
module: "5N18396"
module_title: "Maths for Information Technology"
session: "2025–2026"
version: 2026.05.01.1                # dewlab version format YYYY.MM.DD.N
duration_minutes: 120                # informational unless a timer is enabled
total_marks: 120                     # asserted against the summed structure
python: false                        # false, or a package list: [numpy, pandas]
files: []                            # embedded files; see §6
identity:                            # what the student is asked for
  fields: [name, student_id]
instructions: |
  Answer any ten questions from Section A and any four from Section B.
  Show your working; a correct answer alone may not receive full marks.
---
```

`exam_id`, `title`, `module`, `version`, `total_marks` are required (*build
error* if absent). `exam_id` is the join key across the whole system — it
names storage keys, submission files, and the marking pack — and must never
change across versions of the same exam. `version` disambiguates a revised
paper; the workbench warns when a submission's version differs from the
marking pack's.

## 2. Structure: sections, questions, parts

Headings are presentation. Structure is declared in fences, because the
experiments proved that structure regexed out of headings drifts and breaks
(LESSONS: "Fragile identity plumbing"). The spine is three fence kinds:

````markdown
## Section A — Short questions

```section
id: A
choose: 10          # answer any 10 of the questions in this section
marks_each: 4       # optional assertion: every question in A is worth 4
```

### Question A1 — Sets

```question
id: a1
marks: 4
topic: sets         # optional; feeds the marks-sheet descriptions
outcomes: [MIT-2.1] # optional; validated against curriculum data if present
```

The universal set U contains the whole numbers 1 to 12...

```answer
id: a1.a
type: text
marks: 2
rows: 3
prompt: "List the elements of A ∪ B."
```

```answer
id: a1.b
type: text
marks: 2
rows: 3
prompt: "Is 7 a member of A ∩ B? Explain how you know."
```
````

Scoping rules: a `section` fence opens a section that runs to the next
`section` fence or end of file; a `question` fence opens a question that
runs to the next `question` or `section` fence; `answer` fences belong to
the open question. Prose and illustrative code between fences belongs to
whatever scope is open. An `answer` outside a question, a duplicate id
anywhere, or a question whose part marks do not sum to its declared `marks`
are each a *build error*, as is a file whose questions do not sum to
`total_marks` under the declared choose-N rules.

Ids are lowercase, dot-separated, and permanent (`a1.b`). They are the keys
in saved work, submissions, and mark sheets. Renaming an id after an exam
has been sat orphans data; the compiler cannot prevent that, so the format
documentation says it in bold and the workbench reports unmatched ids
loudly rather than guessing.

## 3. Answer types

The set is deliberately small; each type earns its place by having appeared
in a real paper. Common fields on every `answer`: `id`, `type`, `marks`,
optional `prompt` (rendered above the field), optional `scaffold` (see §5),
optional `model` (see §5), optional `rubric` (see §7).

**`text`** — free written answer. `rows` defaults from marks (see
STYLE_AND_READABILITY: the marks-to-rows rule) and may be overridden.
Accepts typed maths in the notation the reference panel teaches (`x^2`,
`sqrt(x)`, `pi`); dewmark does not attempt live maths rendering of student
input in phase 1.

**`numeric`** — one short blank, optionally several labelled blanks:

```yaml
type: numeric
blanks:
  - {id: root1, label: "Root 1: x ="}
  - {id: root2, label: "Root 2: x ="}
```

Stored as strings; no correctness checking at sitting time — marking is
human.

**`mcq`** — options as text, or as small plots rendered at build time by an
options-generating snippet (the MIT cubic-shape picker, generalised).
Exactly one selectable unless `select: many`. The correct option, if
declared, lives under `model` and is stripped from student variants.

**`table`** — a grid with some cells given and some answerable:

```yaml
type: table
columns: ["x", "-2", "-1", "0", "1", "2"]
rows:
  - ["y", "?", "?", "0", "?", "?"]
```

`?` cells become inputs, each keyed `a3.t.r0c1`-style automatically.

**`sketch`** — the structured graph description: a shape choice plus
feature fields.

```yaml
type: sketch
shape:
  label: "The parabola opens"
  options: ["upward (∪)", "downward (∩)"]
features:
  - {id: root1, label: "Root at ( _ , 0 )", parts: 1}
  - {id: vertex, label: "Vertex at ( _ , _ )", parts: 2}
```

**`code`** — a Python cell, only valid when frontmatter `python` is a
package list. The fence body is the starter code the student sees:

````markdown
```answer
id: t2.a
type: code
marks: 4
```

```python starter
# Task 2a — your answer here

```
````

A `python starter` fence must immediately follow its code answer (*build
error* otherwise). Two supporting fence kinds, unchanged in spirit from the
experiments and from dewlab's tutorial format: `python setup` (runs
automatically at start, never shown) and `python provided` (shown read-only,
runs when the student reaches it or on Run — which, is an open question,
DM-8).

**`diagram-label`** — an inline SVG diagram (authored or build-generated)
with declared input slots for sides, angles, or names. Phase 2; the MIT
triangles justify it but the first exams can present the diagram as an image
with `numeric` blanks beside it.

## 4. Prose, maths, and reference material

Prose between fences is dewlab-dialect markdown: KaTeX maths in `$…$` and
`$$…$$` (rendered at build time, so a no-Python exam ships no maths JS),
tables, images (embedded at build; see §6), and untagged code fences as
read-only illustration. No HTML passthrough — the compiler escapes anything
that is not markdown it understands (*the experiments trusted authored HTML;
an exam file that gets edited under deadline pressure should not*).

A `reference` fence declares the sanctioned support panel — formula sheet,
notation guide, glossary — either inline or by including a shared file:

````markdown
```reference
include: shared/mit-formula-sheet.md
```
````

The compiler refuses a `python`-less exam whose reference includes code-API
sections, and vice versa, to keep the panel honest about what the sitting
provides.

## 5. Model answers and scaffolding

Both live in the source, beside the thing they answer, so one file is the
whole truth (the MIT paper's separate hand-aligned answer array is the
counterexample). Both are stripped or kept per variant at build time.

- `model:` on an answer holds the model answer — text, the correct option
  index, expected values, or for code answers a `python model` fence
  following the starter. Student and backup variants never contain a byte of
  it (*checked by a build-time assertion that greps the emitted student
  HTML for model content and fails on a hit*).
- `scaffold:` holds the placeholder-level hint shown inside the empty field
  (`"Let each short side be s. By Pythagoras: ..."`). Variants declare
  whether scaffolds ship (practice: yes; exam-condition: no).

## 6. Embedded files

`files:` in frontmatter lists every data file the exam provides —
databases, spreadsheets, CSVs, images:

```yaml
files:
  - {path: data/hvit_registry.db, as: hvit_registry.db, desc: "Student registry"}
  - {path: data/late_arrivals.xlsx, as: late_arrivals.xlsx, desc: "Task 5"}
```

The compiler embeds each as base64 in the exam file and writes it into the
Pyodide filesystem at start. A file referenced anywhere (including in
prose tables) but not embedded is a *build error*; there is no runtime
fetch of sibling files, ever (LESSONS: "Half-embedded assets"). The files
panel in the runner is generated from this list.

## 7. Rubrics

Optional, per answer. Phase 1 marking is x-out-of-n per part, so a rubric
is guidance text for the marker plus an optional level breakdown:

```yaml
rubric:
  - {marks: 2, for: "Correct method shown"}
  - {marks: 1, for: "Correct final value"}
  - {marks: 1, for: "Units / interpretation"}
```

Rubric lines ship in the marking pack and the assessor variant only. The
workbench displays them beside the answer and can (phase 3) record marks
per line instead of per part.

## 8. The Python builder

For computed exams, the same structure via a small API:

```python
from dewmark import Exam

exam = Exam(title=..., exam_id=..., module="5N18396",
            version="2026.05.01.1", total_marks=120)

with exam.section("A", choose=10) as A:
    for n, (a, b) in enumerate(pair_variants(seed=2026), start=1):
        q = A.question(f"a{n}", marks=4, topic="quadratics")
        q.prose(f"Solve $x^2 - {a+b}x + {a*b} = 0$.")
        q.numeric(f"a{n}.roots",
                  blanks=[("r1", "x ="), ("r2", "x =")],
                  marks=4,
                  model={"r1": a, "r2": b})

exam.write("mit-2026-summer.exam.json")
```

The builder emits the canonical model; everything downstream is identical.
Its one hard obligation: determinism. Given the same source and seed it
must produce byte-identical output, so a regenerated paper can be diffed
and so the marking pack always matches the paper that was sat.

## 9. The canonical model (`exam.json`)

The compiler's output and the system's contract. Shape, abbreviated:

```json
{
  "dewmark": 1,
  "exam": {"exam_id": "...", "title": "...", "module": "...",
            "version": "...", "total_marks": 120, "duration_minutes": 120,
            "python": null, "identity": ["name", "student_id"],
            "instructions_html": "..."},
  "sections": [
    {"id": "A", "title_html": "...", "choose": 10,
     "questions": [
       {"id": "a1", "marks": 4, "topic": "sets", "outcomes": [],
        "blocks": [
          {"kind": "prose", "html": "..."},
          {"kind": "answer", "id": "a1.a", "type": "text", "marks": 2,
           "rows": 3, "prompt_html": "...", "scaffold": null}
        ]}
     ]}
  ],
  "files": [{"name": "hvit_registry.db", "desc": "...", "b64": "..."}],
  "reference": [{"title": "...", "html": "..."}]
}
```

Model answers and rubrics are carried in a parallel structure keyed by
answer id, emitted only into the marking pack and assessor variant
(SUBMISSION_FORMAT §4 covers the marking pack). `dewmark: 1` is the format
version; readers refuse a major version they do not know rather than
guessing (the MIT restore-across-variants crash is the cautionary tale).

## 10. Documentation for translation

`dewmark/docs/` will carry two author-facing documents: the format guide
(this spec, rewritten for authors rather than implementers) and a
translation guide for turning an old paper — Word, PDF, or a previous HTML
experiment — into source, written to be handed to an LLM together with the
old paper. The translation guide's core instruction: translate structure
first (sections, questions, marks — the compiler will verify the
arithmetic), prose second, model answers last, and never invent marks that
are not in the original.
