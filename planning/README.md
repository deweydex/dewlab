# Planning

What was decided before any code existed, and why. Seven documents, each
answering one question.

Read `DECISIONS.md` first — the others expand on entries in it.

- **`DECISIONS.md`** — every settled decision, with its reasoning: libraries,
  visual style, hosting, versioning, the editor, mathematics. Ends with a short
  list of things assumed rather than settled, which are the ones most likely to
  need revisiting.
- **`BUILD_PLAN.md`** — the build in dependency order, five phases, ending in a
  pilot before converting a whole series.
- **`CONTENT_AND_FILE_ARCHITECTURE.md`** — the markdown format a tutorial is
  written in, and how a tutorial refers to a dataset, to shared setup code, or
  to another tutorial.
- **`VERSIONING_AND_PROGRESS.md`** — what happens to a student's saved work when
  you edit a tutorial they have already started.
- **`REPO_AND_EDITOR.md`** — the repository layout, how publishing works, and
  what the authoring editor is for in its first version.
- **`VERSIONS.md`** — the proposal to give each tutorial released versions a
  student can return to, and an archive in place of deletion. Not built; it
  supersedes the second half of `VERSIONING_AND_PROGRESS.md` if adopted.
- **`WINDOW_AUDIT.md`** — the four things that become contracts the day the
  first class uses dewlab, looked at once while changing them was still free.
  Two defects came out of it.

`OPEN_QUESTIONS.md` sits alongside them: the questions raised at the start,
which are settled and which are not.

## Why it is written down

Two authors, and a project that will be picked up and put down across a term.
Most of what these documents record is not hard to work out — it is hard to
work out *twice*, the same way, six weeks apart. Writing the reasoning next to
the decision is what makes it possible to disagree with it later on the merits
rather than re-deriving it from scratch.

The same habit continues after the build starts, in `DECISIONS_LOG.md` and
`QUESTIONS.md` at the root of the repository.

## What is fixed and what is not

Fixed: this is not tied to a single course; two authors, both comfortable with
git; and the module and academic year are fields a tutorial declares for
itself, so a new module is a new value and a new folder rather than an
architectural change.

Not fixed: everything in the "Still open" half of `OPEN_QUESTIONS.md`, which is
mostly questions about content rather than about the tool.
