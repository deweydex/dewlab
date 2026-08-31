# Open questions

This document records the design decisions that are not yet made. Each
entry states the question, the assumption the project builds on until
the question is answered, what changing that assumption later would
cost, and what the open question blocks in the meantime. When a
question is settled, the answer moves into the relevant design document
and the entry here is removed, with the decision recorded in the
repository's decision log.

**Q1 — Where do real exam files and submissions live?**
The question: this repository is public, real exams are secret before
they are sat, and submissions are personal data, so all of it must live
somewhere else — but where, exactly, and organised how?
Assumed for now: teachers keep exam files in private storage of their
own choosing and submissions in ordinary folders on their own machines.
Cost of changing later: low, because no tool depends on the location.
Blocked meanwhile: the teacher guide's advice on organising folders.

**Q2 — How are all the graded papers turned into PDF files in one step?**
The question: the marking workbench produces a printable graded paper
per student, and printing thirty of them one at a time through the
browser's print dialog is tedious; a one-step export needs either a
PDF-generating library inside the workbench or a small helper program
run beside it.
Assumed for now: print-per-student, with the workbench advancing to the
next paper automatically after each print.
Cost of changing later: low; the graded page layout stays the same
either way.
Blocked meanwhile: nothing, but marking a large class is slower than it
should be at the final step.

**Q3 — Should the marks export include a real Excel file?**
The question: the workbench exports CSV files, which Excel opens, but a
native Excel file could hold the marks and the column explanations as
two sheets of one document.
Assumed for now: two CSV files with matching names.
Cost of changing later: trivial; an Excel export is an addition.
Blocked meanwhile: nothing.

**Q4 — Should the exam page show a timer?**
The question: the page knows the time allowed but does not count it
down; a countdown adds pressure and misleads whenever a student has
been granted extra time.
Assumed for now: no timer; the time allowed appears on the opening
screen only, and the room's clock governs.
Cost of changing later: none; a timer is an addition.
Blocked meanwhile: nothing.

**Q5 — Should the exam know the class list?**
The question: students typing their own name and number produces
spelling variations and typing mistakes; building the class list into
the exam would fix matching but would put personal data inside a widely
distributed file.
Assumed for now: students type their details; the marking workbench
matches on student number, accepts a class list on the teacher's side
for cross-checking, and reports numbers it cannot match.
Cost of changing later: low.
Blocked meanwhile: nothing.

**Q6 — What is the right counting rule for "answer any N" sections?**
The question: when a student answers more questions than the rule
allows to count, the workbench counts the best N by default — but an
institution might instead require the first N, or the N the student
nominated.
Assumed for now: mark everything, count the best N, let the marker
override, and record which questions were counted.
Cost of changing later: none in the data, since attempts and selections
are recorded; the policy is applied at counting time.
Blocked meanwhile: the final wording of the finish screen, and this
question should be put to quality-assurance colleagues before a real
sitting.

**Q7 — How does the Python system reach an exam room reliably?**
The question: Python exams download a thirty-megabyte runtime on first
use; exam-room networks are slow, filtered, or absent, so the download
must have happened beforehand or be served locally.
Assumed for now: a documented room checklist with two options — open
the page on every machine the day before, or serve the files from a
laptop in the room — plus a rehearsal before any first real sitting.
Cost of changing later: none; both options already work.
Blocked meanwhile: confidence, which only a rehearsal provides.

**Q8 — Is "close the page and reopen" an acceptable remedy for frozen
code?**
The question: a student's endless loop can freeze the exam page, and
the current design has no Stop button (the technique that provides one
is unavailable to a page opened as a local file); the remedy is to
close and reopen, losing nothing but the running Python session.
Assumed for now: yes, because continuous saving makes the reopening
cheap and the remedy is printed on the page before it is needed.
Cost of changing later: substantial — a Stop button would require
hosting the exam differently.
Blocked meanwhile: nothing for exams without code questions.

**Q9 — What about answers that want to be drawn or handwritten?**
The question: some questions are best answered with a freehand drawing
or handwritten working, and dewmark has no drawing type; the
describe-a-sketch type covers graph sketching, but not, say, a freehand
biological drawing.
Assumed for now: exams needing freehand work put those parts on paper
("complete this part in the answer booklet provided") and everything
else in dewmark.
Cost of changing later: a drawing or photograph type would be an
addition, with real design work around fairness and file handling.
Blocked meanwhile: nothing, but authors must know the limit when
choosing question types.

**Q10 — Does the guided creation tool reuse the builder's checking code
or reimplement it?**
The question: the planned point-and-click creation tool runs in the
browser, while the builder's checks are written in Python; two
implementations of the same checks would inevitably drift apart, and
running the Python checks inside the browser is possible but heavy.
Assumed for now: the builder's checking code is written so it can run
in the browser, and the decision is deferred until the guided tool is
designed.
Cost of changing later: high if a second implementation is written
first — which is why one will not be.
Blocked meanwhile: the guided creation tool's architecture.

**Q11 — Is "dewmark" the final name?**
The question: the project name appears in file names and stored data,
so it becomes expensive to change once real exams exist.
Assumed for now: dewmark.
Cost of changing later: a rename is cheap now and disruptive after
first real use.
Blocked meanwhile: nothing, but the question must close before a real
sitting.

**Q12 — How well must marking work outside Chrome and Edge?**
The question: only Chrome and Edge let a web page open a folder and
save into it, which the marking workbench relies on; Firefox and Safari
users can mark, but must manage files by hand.
Assumed for now: Chrome or Edge is the supported marking environment,
stated plainly in the teacher guide; the by-hand path exists but is not
polished.
Cost of changing later: moderate engineering if a marker who cannot use
Chromium-based browsers appears.
Blocked meanwhile: nothing known.

**Q13 — What exactly does the exam header look like?**
The question: the requirement — an exam page must be distinguishable
from practice material at a glance — is fixed, but the header's design
is not.
Assumed for now: a navy band carrying the institution, the module, and
the word "Examination".
Cost of changing later: none; this is presentation.
Blocked meanwhile: nothing; the design will be settled with real pages
side by side.

**Q14 — When saved copies disagree, which wins?**
The question: after an interruption, the browser's saved copy and the
answer file can differ — most sharply when the computer's clocks are
wrong, which is exactly when a student has moved machines.
Assumed for now: the page shows both copies with their save times and
answer counts and asks the student, whenever they differ by more than a
few seconds.
Cost of changing later: low.
Blocked meanwhile: the exact wording of that choice screen.

**Q15 — Should the workbench ever pre-check answers?**
The question: multiple choice, blanks, and numeric answers could be
compared against the expected values automatically, and a language
model could draft feedback; both would change the character of the tool
and the trust placed in it.
Assumed for now: no automatic checking of any kind; every mark is
entered by a person.
Cost of changing later: none now; any future step here needs its own
design, its own accuracy evidence, and its own conversation with the
people who rely on the results.
Blocked meanwhile: nothing.

**Q16 — What is promised to a student using a screen reader?**
The question: the accessibility baseline in
[APPEARANCE_AND_READABILITY.md](APPEARANCE_AND_READABILITY.md) is
firm, but a fully non-visual sitting of a code or mathematics exam
involves difficulties the baseline does not resolve.
Assumed for now: the baseline ships in the first version; full
non-visual sittings are investigated with the institution's disability
support staff rather than promised in advance, and alternative
arrangements remain available as they are today.
Cost of changing later: high wherever structure was built
inaccessibly — which is why the baseline is first-version work.
Blocked meanwhile: honest wording in the teacher guide.

**Q17 — How do students type symbols?**
The question: science and mathematics answers want H₂O, superscripts,
Greek letters, and similar; typed plain text needs either conventions
(`x^2`, `H2O`), a palette of insertable symbols, or a small formatting
toolbar.
Assumed for now: plain text with published conventions plus a symbol
palette, and marker guidance to accept any unambiguous form.
Cost of changing later: moderate — stored answers stay plain text under
every option considered, which keeps the choice reversible.
Blocked meanwhile: the palette's contents, and the conventions page in
the student-facing reference material.

**Q18 — Can a marker attach a comment to a chosen passage of an essay?**
The question: essay feedback currently attaches to criteria and to the
paper as a whole; pointing at a particular sentence is natural for
essay markers and is not yet designed.
Assumed for now: criterion-level and whole-paper comments suffice for
the first version.
Cost of changing later: an addition, though a substantial one.
Blocked meanwhile: nothing.

**Q19 — How far may the descriptor assistant go?**
The question: the assistant that reads a module descriptor currently
suggests question types; it could plausibly also draft whole questions
aligned to the descriptor's learning outcomes, which would be more
useful and easier to over-trust.
Assumed for now: suggestions of question types only, each tied to the
descriptor passage that prompted it.
Cost of changing later: none; drafting would be an addition governed by
the same rules as exam translation (drafts labelled, marks never
invented).
Blocked meanwhile: nothing.
