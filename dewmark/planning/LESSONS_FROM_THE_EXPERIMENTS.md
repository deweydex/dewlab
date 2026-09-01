# Lessons from the exam experiments

Before dewmark was designed, three browser-based exams were built by
hand and used, or prepared for use, in the 2025–2026 academic year.
They proved the central idea: an exam that runs entirely in a web
browser, with no server, works in a real exam room. They also failed in
specific, instructive ways. This document records what each experiment
was, what it got right, and which dewmark rule each failure produced.
Corrected copies of the exams themselves are in the
[`experiments/`](../experiments/) folder.

The three experiments were:

1. **A database practical.** A two-hour exam for the Database Methods
   module, with six tasks answered as live Python code in the browser.
   It embedded a small database inside the page, saved answers to a
   file as the student worked, and produced a file of answers for
   marking.
2. **A practice paper on image arithmetic.** A simpler cousin of the
   database exam, mixing Python tasks with written answers, saved in
   the browser only.
3. **A mathematics paper in two versions.** A 120-mark Maths for
   Information Technology exam: one version that worked completely
   offline with written and structured answers, and a second version
   with runnable Python cells whose "assessor" copy filled every answer
   space with the model answers on loading.

## What the experiments got right

**One file, no server, no installation.** Each exam was a single file
that could be sent by email, put on a USB stick, or placed in a shared
folder, and the offline mathematics paper ran with the network cable
unplugged. For an exam room, no other property matters as much. dewmark
keeps it: a built exam page is one self-contained file.

**Several versions from one paper.** The mathematics exam shipped as a
student paper, a fully offline backup, and an answer key. That is the
right set of outputs. It was produced the wrong way — three separately
hand-edited copies of the same hundred-kilobyte page — and dewmark's
exam builder exists to produce all the versions from one exam file
instead.

**Describing a sketch instead of drawing one.** The mathematics paper
replaced graph drawing with a shape choice plus typed boxes for the
features that carry the marks. Students could answer it quickly under
time pressure, markers could mark it consistently, and it became
dewmark's describe-a-sketch question type.

**Saving twice, and saying so.** The mathematics paper saved to the
browser's storage and to a file the student chose, showed a separate
indicator for each, and explained the difference in plain words on
screen. dewmark keeps the whole arrangement.

**Printing treated seriously.** Before printing, the pages expanded
every answer box to full height, put the student's name on the printout,
and kept questions from splitting across pages. dewmark's printing
rules grew from these.

**Answer boxes sized by marks.** A one-mark answer got a one-line box; a
five-mark answer got six lines. The box size quietly told students how
much was expected. dewmark makes this a rule applied by the builder.

## What failed, and the rule each failure produced

**Answers were saved by position.** The mathematics paper saved all
answers as a single list, in the order the answer boxes appeared on the
page, and restored them the same way. Its model-answer version relied
on a hand-maintained list of 115 entries lining up with those boxes by
counting alone. Inserting one answer box anywhere would have shifted
every saved answer into the wrong place, silently.
*The rule: every answer space has a permanent name, and every saved
answer, mark, and spreadsheet column is stored under that name. Saving
by position is forbidden.*

**The same facts were written out several times, and drifted.** The
database exam carried three separate hand-written copies of its own
structure — a task list for navigation, a table of files, and a
reference card for its helper functions — beside the exam content that
already contained the same facts. Two copies disagreed in the version
that shipped: the reference card documented settings the helper
functions did not accept, and the ten-mark model answer, written from
the card, failed with an error when run.
*The rule: navigation, mark totals, file lists, and reference material
are generated from the exam file. Nothing is written twice.*

**Marks existed only as wording.** In the mathematics paper, "(2
marks)" was decoration in the question text, and "answer any ten of
twelve" existed only as a sentence. Nothing could add the marks up,
check them, or count the choices.
*The rule: marks and choice rules are settings the builder reads and
verifies, and the wording shown to students is generated from them.*

**Files the exam needed were fetched at sitting time.** The database
exam embedded its database inside the page but fetched its two
spreadsheet files from alongside the page when it started. Opened from
a local file, as an offline exam is, that fetch fails without any
visible error, and two of the six tasks then failed mid-exam with a
misleading message.
*The rule: everything an exam names is embedded when the exam is built.
A missing file stops the build; it never surprises a student.*

**Failures were silent.** Cancelling the choose-a-save-file step
disabled file saving without a word. A broken save quietly fell back to
browser-only saving. A click on Run while code was already running was
ignored without feedback. Answers edited but not yet run were never
saved at all.
*The rule: every saving route has a visible indicator, every
degradation announces itself, and saving happens on every change rather
than only at chosen moments.*

**Restoring promised more than it delivered.** The database exam's Load
button put code and old outputs back on the page, but the running
Python session was gone, and nothing said so; buttons restored from old
output looked alive and did nothing. Separately, loading a save file
from one version of the mathematics paper into the other crashed
partway through restoring, because the two versions saved different
lists of answers under the same file name.
*The rules: a restore states exactly what came back and what must be
re-run; saved files carry the exam code and version and are checked
before anything touches the page; and one saved-answer format serves
every version of a paper.*

**Displayed answers were trusted as program content.** The database
exam saved each answer's output as ready-made page markup and put it
back into the page on loading. Page markup can carry program code, so a
marking tool built the same way would have run whatever a submission
contained.
*The rule: submissions contain data only — text, numbers, and images —
and the marking workbench displays them without executing anything.*

**There was no marking tool at all.** The "assessor" version of the
mathematics paper was an answer key, not a marking tool: marking meant
a printed key beside a stack of printed papers, and the answer files
from one saving route did not even include the student's name in the
file name.
*The rule: marking is a full part of dewmark, submissions are named by
exam, student number, and student name, and the marking workbench is
built and tested with the same seriousness as the exam page.*

## The summary

The experiments established that the exam room does not need a server,
and demonstrated, one inconsistency at a time, that everything beyond
that idea must be generated from a single checked file rather than
maintained by hand.
