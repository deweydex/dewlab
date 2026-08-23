# The audit before the window shuts

Josh, while the versions work was being planned:

> There is no student work yet — we are still working to make the first version
> of this application so nothing can be lost yet.

Which is true, and which is why this document exists. **Four things become
contracts on the day the first class uses dewlab**, and all four are free to
change until then. This is the deliberate look at each of them, done once,
rather than an assumption that they are fine.

They were not fine. Two real defects, both of which would have needed a
migration inside every student's browser if found a term later.

---

## 1. Slugs — one defect, fixed

A slug is in every URL and, until now, was the whole key a student's saved work
was stored under.

**Slugs are unique within a module, not across the site** (DECISIONS_LOG 7.3).
Both modules have a `first-steps`. But `progressKey()` was
`dewlab:progress:` + the slug alone, so the two tutorials **shared one record**:
a student's answers in Computational Methods' First Steps appeared in Maths and
Programming's First Steps, and each save overwrote the other.

Fixed by keying on the module and the slug together, and by putting the module
in the page manifest so the runtime has it.

**This is the third time scoping slugs per module has left something keyed on
the slug alone.** The built pages were first (#23), the downloadable copies
second (#24), and the saved work third. Each was found separately, by something
different — a test, a publish guard, and this audit. The pattern is worth naming
in case there is a fourth: *anything that identifies a tutorial needs the pair,
not the slug.*

### One cosmetic thing, left alone

`critique-and-reflection` is the slug of a tutorial titled *Looking Back Before
Moving Forward*. The URL and the title do not match. It is free to rename today
and costs a redirect later — but it is only cosmetic, and Josh may prefer the
shorter URL. Flagged, not changed.

---

## 2. Cell ids — sound, and one thing that is now safe

The convention is `section-slug-n`. Measured across all 228 cells:

- **None non-conforming.** Every id is lowercase letters, digits and hyphens.
- **Lengths** run from 5 to 48 characters, mean 18. The longest is
  `classifying-numbers-a-mathematical-application-1`, which is long but
  descriptive and does no harm.
- **Twelve ids are reused across tutorials** — `your-turn-1` through
  `your-turn-6`, and similar. That is fine, and it is fine *because* the
  storage key is per-tutorial. It would have been a defect if work were keyed
  on the cell id alone, which is worth recording as the reason not to change
  that later.

No change needed. The one thing worth stating is what a cell id now means: it
is a promise that this is the same exercise, and the editor's rename warning
enforces it.

---

## 3. The save record — one defect, fixed

The record is `{tutorial-slug, tutorial-version, saved_at, cells[]}`, where each
cell carries `task_id`, `student_code` and `output_html`.

**Importing a file overwrote the current record before checking it belonged
here.** "Load a copy" wrote whatever JSON it was given into this page's key and
only then discovered the cells did not match — by which point the student's real
work was gone, replaced by somebody else's, with a notice saying some cells
could not be placed.

Three fixes:

- The record now carries `tutorial-module` as well as the slug, so a file can
  say where it came from.
- The exported filename carries the module. Two files called
  `first-steps-progress.json` in a downloads folder are indistinguishable and
  are from different tutorials.
- **Import checks before it writes.** A file from another tutorial is refused by
  name — *"That file is saved work from computational-methods / first-steps, not
  this tutorial. Nothing has been changed."* — and the existing record is left
  alone.

Lenient in one direction on purpose: a record with no module still loads on a
matching slug, so a file saved before the module was recorded does not hit a
cliff. There are no such files today; the leniency costs nothing and removes a
future edge.

---

## 4. The version field — no change needed now

`version` is an integer, written into every saved record, and the restore
compares it as `String(a) !== String(b)`. Step 2 of `VERSIONS.md` turns it into
a dotted date.

**The comparison already tolerates both**, because it stringifies. So the change
of type does not need a migration even in principle, and certainly not now,
when there is nothing to migrate. Nothing to do here beyond doing it in step 2.

---

## What this cost, and what it would have cost

Two defects, both in the path a student's work travels, both invisible until
somebody lost an afternoon's work and could not say why. Fixed today: two small
changes and eight tests. Fixed a term from now: the same changes, plus a
migration running inside every student's browser, plus however many people had
already been affected.

That is the whole argument for doing this once, deliberately, before the window
shuts — and the window shuts on the day the first class opens the site.
