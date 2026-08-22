# Practice problems

A file of problems beside each tutorial: type an answer, work it through, check
it, and — around the problems — say how you felt about the topic before starting
and after finishing. Students can also write their own problems and pass them
on.

Not built. Planned only, at Josh's request.

---

## What already exists

More than expected, which is the encouraging part.

- **`text_input`, `dropdown`, `button`** — widgets a cell can mount and read
  back. Written in Phase 0, tested, working.
- **`check(actual, expected, tolerance)`** — compares an answer against a
  target and renders a pass or a fail with a reason. This is the
  check-your-answer mechanism, already built.
- **Autosave and restore** — everything typed is kept in the browser, per
  tutorial, matched by cell id. Reflections are just typed text; they are saved
  by the machinery that saves everything else.
- **Export and import** — a student's work leaves as a JSON file and comes back.
  That is the sharing mechanism, already built and already tested.

So the first honest observation: **most of a practice page could be written
today**, as an ordinary dewlab tutorial made of `text_input` and `check` cells.
Worth doing that first for one tutorial, before building anything, to find out
what is actually missing rather than guessing.

## What is genuinely missing

**A student cannot make a new cell.** Every cell is written into the markdown at
build time and mounted at load. "Write your own problem and share it" needs a
cell that did not exist when the page was built — and that is the one real gap.

It is not small. It touches:

- **Where the code lives.** A student-made cell is not in the manifest, so its
  source has to live in saved progress, which currently stores edits to known
  cells rather than the existence of unknown ones.
- **Ids.** Restore matches by cell id. Student-made cells need ids that cannot
  collide with build-time ones or with another student's.
- **Version compare.** A tutorial that changes underneath saved work already
  warns; a student-made cell belongs to no version, so it should survive an
  edit that invalidates everything else.
- **Trust.** An imported problem is somebody else's code, and running it is
  running their code. In Pyodide that is sandboxed from the machine but not from
  the page — it can read and change anything on it. Acceptable between students
  in one class; not acceptable as a general "paste a link and run it" feature.
  Whatever ships should say so where the student can see it.

## Shape

**One file per tutorial**, as asked: `practice/<slug>.md`, built by the same
build into the same kind of page, linked from the tutorial and from the contents
page. Not a section inside the tutorial — a student should be able to work
through problems without scrolling past the teaching, and a teacher should be
able to set the problems without setting the reading.

**Three bands to a practice page:**

1. **Before.** Two or three prompts, plain text boxes. *What do you already know
   about this? What are you expecting to find hardest?* No marking, no checking.
   The point is that it is answered before the work rather than after.
2. **The problems.** Each one: a statement, a box to work in, a way to check.
   Graded from "the answer is a number" through to "write the function". `check`
   handles the first; the later ones are the student running their own tests,
   which is the habit Tutorial 8 teaches anyway.
3. **After.** The same prompts again, plus *what surprised you?* The before and
   after sitting on one page, both visible, is the part that makes it worth
   doing.

**Writing your own.** A button that adds an empty problem — a statement box, a
code box, an expected answer — and an export that produces a small file with
just that problem in it. Import puts somebody else's into your page. The
existing progress export is the model and possibly the mechanism.

## Order of work

1. **Write one practice page by hand**, using only what exists today, for a
   tutorial that is already good. Find out what is actually missing.
2. **Build the page type** — `practice/` in the build, the three-band template,
   the links both ways.
3. **Runtime cells**, once 1 has shown what they really need to do.
4. **Sharing**, last, and with the trust question answered in writing before any
   of it is written in code.

Steps 1 and 2 are worth doing regardless. Step 3 is the one that needs a design
of its own before it needs an implementation.

## What this is not

Not a marking system. Nothing here reports to a teacher, stores a score, or
leaves the student's browser unless they export it themselves — which is the
same promise the tutorials already make, and the reason a student can be honest
in the reflection boxes.
