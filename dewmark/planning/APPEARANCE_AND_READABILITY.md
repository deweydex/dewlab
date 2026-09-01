# Appearance and readability

This document sets out how dewmark's pages look, how they behave when
printed, and what they promise to students who need adjustments. The
audience for these pages is adult learners on QQI Level 5 and 6
courses, many returning to education, reading under the pressure of an
exam. Readability decisions therefore carry more weight here than in
ordinary teaching materials.

## 1. The shared look, and telling an exam apart

dewmark belongs to the dewlab project and uses dewlab's visual
language: the same navy and orange colours, the same serif reading
typeface for question text, the same plainer typeface for buttons and
controls. A student who has used the dewlab tutorials recognises a
dewmark page at once.

At the same time, an exam must never be mistaken for practice material,
in either direction. A dewmark exam page carries a formal header band —
the institution's name, the module, and the word "Examination" — that
no tutorial or practice page uses, and a practice paper built from the
same exam file replaces that band with a clearly labelled "Practice"
header. The exact design of the band will be settled by putting real
pages side by side; the requirement it must meet is fixed: a glance
from across a room should be enough to tell an exam from anything else.

## 2. Reading the paper

- Question text is set in a serif typeface at a comfortable reading
  size, in lines no wider than roughly twelve words, because long lines
  are measurably harder to track.
- The two things a student scans for under time pressure — question
  numbers and marks — are visually prominent, and the marks are always
  written the same way: "(4 marks)" at the question heading, "(2)" at
  the answer space. The builder generates these from the exam file, so
  the displayed marks can never disagree with the marks being counted.
- Mathematics is typeset when the exam is built, so fractions, powers,
  and symbols display properly without any internet connection.
- Answer spaces are visibly distinct from question text: a box with a
  tinted background and a coloured left edge. When an answer space has
  content, the edge changes colour, so scrolling through the paper
  shows at a glance what remains unanswered. Colour is never the only
  signal — a small mark accompanies the colour change — because some
  students do not distinguish the colours involved.
- Writing boxes start at a size that reflects the marks available (a
  two-mark answer starts around three lines, a six-mark answer around
  ten) and grow as the student types. The starting size is a hint about
  expectations, never a limit.
- Nothing on the page requires hovering a mouse pointer to be seen.
  Anything that opens — the reference panel, a symbol palette — opens
  on a click or a keyboard command and closes with the Escape key, so
  keyboard-only students and touchscreen students lose nothing.

## 3. The shape of the screen

The page is one document that scrolls normally, with a slim fixed bar
at the top (title, student, saving indicators, Finish) and a
collapsible side panel (question list, reference material). The page
never traps scrolling inside inner regions, and only two things may
scroll sideways within their own box: wide tables and code. Exam rooms
supply laptops or desktops, and the layout is designed for those
first, but the page remains usable on a tablet or phone for students
practising at home.

Students can adjust the text size and the line width from a small
settings control, and the choice is remembered on that browser. The
page offers a light and a dark colour scheme on screen; printing always
uses dark text on a white background.

## 4. Printing

Three different documents in the dewmark flow end up printed or saved
as PDF files — a student's own copy of their paper, the readable copy
inside every submission, and the graded papers the marker exports — and
one set of printing rules covers them all.

- Before printing, every answer box is expanded to show its full
  content, so nothing is ever cut off mid-answer.
- Every printed page repeats the student's name, student number, and
  the exam code at the top, because printed pages become separated.
- A question is never split across a page break between its wording and
  its answer, and long questions begin on a fresh page.
- An empty answer space prints with a visible border and the words "not
  attempted", so an absence on paper reads as a fact rather than a
  printing fault.
- Code prints as dark text on white regardless of the screen scheme,
  and buttons, panels, and saving indicators do not print at all.

## 5. Accessibility

The following are commitments for the first released version, checked
by the exam builder and by tests, not aspirations for later.

- Every answer space has a proper text label that assistive technology
  can read, and the paper can be navigated by headings and in a sensible
  keyboard order, with the focused element always visibly outlined.
- Every picture in an exam carries a written description supplied by
  the exam's author; the builder refuses to build an exam with an
  undescribed picture.
- Text and background colours meet the WCAG AA contrast standard (a
  widely used accessibility benchmark) in both colour schemes.
- Meaning is never carried by colour alone.

Beyond that baseline, honesty is owed about the harder cases. Sitting
a full exam with a screen reader involves real difficulties that a
checklist does not capture — live code editors and typeset mathematics
remain awkward for assistive technology — and dewmark
does not yet claim to be a complete answer for a blind student.
Institutions already operate alternative arrangements for exactly such
cases, and those remain the fallback while this work proceeds; the open
item is recorded in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). What is
promised now is narrower and firm: the structure is built accessibly
from the start, because retrofitting accessibility later is the most
expensive way to get it.

## 6. The words on the page

Instructions, notices, and error messages follow one register: calm,
specific, and short. Every error message answers three questions in
order — what happened, whether the student's work is safe, and what to
do next. The finish screen leads with counts ("2 answer spaces empty,
worth 6 marks") rather than sentences, because its reader may have
forty seconds left. Nothing on the page uses an exclamation mark.
