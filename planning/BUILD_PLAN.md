# Build plan

Six phases, in dependency order. Each rests on the one before it, and nothing
in a later phase should send you back to reopen an earlier one.

The order is not arbitrary. It puts the thing most likely to be wrong first —
whether Python actually runs acceptably in a browser — and the thing easiest to
change last. If the first phase had failed, nothing after it would have been
worth building.

---

## Phase 0 — Foundations *(complete)*

Prove that the hard part works before building anything on top of it.

- Stand up the repository structure, including a folder per module under
  `tutorials/`.
- Build the page template that every generated tutorial is rendered into,
  linking shared files in `assets/` rather than inlining them into each page.
- Confirm that numpy, pandas and matplotlib all load in one step, with no
  extra package-installation stage.
- Confirm that a plain cell running code from those libraries renders its
  output underneath itself correctly.
- Only then build the widget bridge in `tutorial_tools.py`. It is a useful
  layer, not a precondition — if plain execution does not work, widgets on top
  of it are worthless.

Worth re-checking whenever the Python runtime version changes: which packages
are available shifts between releases.

## Phase 1 — The build script *(complete)*

Turn markdown into pages.

- Parse frontmatter and body.
- Turn `exec`-tagged fences into runnable cells.
- Expand include directives into the setup code they name.
- Resolve cross-tutorial links into real relative addresses, and fail the build
  on any that do not resolve.
- Render the result into the page template.

Test it against one hand-written tutorial, start to finish, before pointing it
at real content. A converter that works on a file you wrote to exercise it is
not the same as one that works on a file someone wrote to teach with.

## Phase 2 — Saved progress

Let a student close the tab and come back.

- Build the save and restore logic against the schema in
  `VERSIONING_AND_PROGRESS.md`.
- Add the version comparison that document describes.
- Test the mismatch path deliberately — bump a tutorial's version on purpose
  and confirm the restore still works and the notice appears.

That last point is the whole phase, really. The happy path where nothing has
changed will work almost by accident; the path where you have edited a tutorial
under a student's feet is the one that matters and the one nobody tests.

## Phase 3 — Navigation

Make a series navigable as a series.

- A contents page per series.
- Previous and next links in the header of every generated page.

## Phase 4 — Publishing

- A workflow that runs the build on every push and publishes the result.
- Confirm that data files load correctly from the published address, not only
  from a local server. Path handling behaves differently once hosted, and this
  is a common place for it to differ.

## Phase 5 — Pilot

Convert two or three real tutorials end to end before converting a whole
series. Put them in front of students, or at the very least run them on a
machine that is not the one they were built on.

Converting everything first and discovering a problem afterwards is the
expensive order to do this in.

## Phase 6 — Closing the curriculum

Phases 0 to 5 were about the tool. This one is about whether the material it
carries actually covers the two module descriptors, which is a different
question and was not answerable until there was something to measure.

The measuring is done. [`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md) is generated
from the outcome data and each tutorial's own `covers:` frontmatter, so it
cannot drift from the tutorials, and CI fails if it is out of date. It reports
**41 of 65 outcomes in place**, with the gaps concentrated almost entirely in the
mathematics: calculus, trigonometry, function graphing and Boolean logic have no
coverage at all.

What is left is writing, and it divides into three kinds of work that cost very
different amounts.

**Conversions — cheapest.** `PDP-LO1`, `PDP-LO3` and `PDP-LO9` already exist as
finished notebooks in `everlearning`, and `dev/from_notebook.py` already converts
notebooks. Two tutorials, no new material, three outcomes closed. See
[`outlines/from-everlearning.md`](./outlines/from-everlearning.md).

**Short tutorials — cheap.** Rearranging Formulae, When There Is No Answer,
Approaching a Limit, Logic and Truth. Each closes one or two outcomes, each fits
in a sitting, and three of the four close a *quiet* gap — an outcome students
currently meet without being taught.

**Full tutorials — the real work.** Drawing Functions, then Angles and Waves,
then Rates of Change, in that order, because each needs the graphing habit the
one before it builds. This is the mathematics half of the course, and it is
roughly as much writing as everything converted so far.

Before any of it:

- Settle the three scope questions in `curriculum/out-of-scope.yaml` —
  coordinate geometry, right-triangle trigonometry, and radians. Each changes
  what Drawing Functions and Angles and Waves contain.
- Decide whether Tutorial 15 is revised or extended. Two of the outlines take
  material that arguably belongs in it.
- Decide whether the new tutorials go on the end or get slotted in. Slotting in
  is better teaching and renumbers everything after them.

`PDP-LO12`, the team project, is the one item here that dewlab cannot solve by
writing a tutorial. See [`outlines/team-project.md`](./outlines/team-project.md).
