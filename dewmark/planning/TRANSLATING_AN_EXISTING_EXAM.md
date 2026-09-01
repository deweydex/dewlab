# Translating an existing exam

Most exams already exist before dewmark meets them: as Word documents,
as PDFs, or as plain text written for last year's paper sitting. And
most teachers will keep writing exams the way they already do. dewmark
therefore treats conversion, not hand-writing, as the normal way an
exam file gets made: a teacher hands over their existing exam, an
assistant converts it into the exam file format, the exam builder
checks the result, and the teacher approves the finished paper by
reading it — not by reading the converted file.

The assistant is a program built on a large language model (an AI
system that reads and writes text). This document sets out how the
conversion works and, more importantly, the rules that keep it
trustworthy, because an exam is exactly the kind of document where a
plausible-looking mistake matters.

## 1. How a conversion runs

1. The teacher provides the exam in whatever form it exists — a Word
   document, a PDF, plain text — along with the marking scheme if it is
   a separate document.
2. The assistant reads the dewmark format documentation and produces a
   draft exam file: the questions as written content, the structure and
   marks in settings blocks, and the marking material in marking
   blocks.
3. The exam builder checks the draft
   ([THE_EXAM_BUILDER.md](THE_EXAM_BUILDER.md)). Every error — marks
   that do not add up, a missing name, an unusable question type — goes
   back to the assistant, which corrects the draft and tries again.
   This loop continues until the builder accepts the file. The
   builder's checks are strict on purpose: they are what makes it safe
   to let a machine write the file.
4. The teacher reviews the result by opening the built preview and
   reading the paper as a student would see it, alongside the answer
   key. The teacher checks the paper, because the paper is what they
   already know how to judge; nobody needs to proof-read settings
   blocks to approve an exam.
5. The teacher makes corrections — either by telling the assistant what
   to change, or by editing the exam file directly — and rebuilds until
   the paper reads exactly as intended.

## 2. The rules the assistant follows

Three rules bound what the assistant may do, and they exist because a
conversion that quietly invents content is worse than no conversion at
all.

- **Marks are never invented.** Every mark in the converted file must
  come from the original. If the original does not state how a
  question's marks split across its parts, the assistant asks the
  teacher instead of guessing, and the builder's adding-up checks catch
  any split that disagrees with the stated totals.
- **Drafted answers are labelled as drafts.** Old exams often survive
  without their marking schemes. The assistant may draft model answers
  and marking guidance in that case — that is useful — but everything
  it drafted rather than transcribed is marked `draft` in the file, the
  answer key displays those entries with a clear "draft — not yet
  approved" label, and the marking workbench shows the same label to
  the marker until the teacher removes it. An unnoticed wrong model
  answer would quietly misdirect the marking of every paper, which is
  why this labelling is a rule rather than a courtesy.
- **Uncertainty becomes a question, not a guess.** Where the original
  is ambiguous — a question type that could be read two ways, an
  illegible mark allocation in a scanned PDF — the assistant lists the
  ambiguity for the teacher rather than resolving it silently.

## 3. Suggesting question types from a module descriptor

A module descriptor is the official document that states what a module
teaches and how it is assessed. When a teacher is composing a new exam
rather than converting an old one, the assistant can read the
descriptor and suggest which question types from the catalogue
([QUESTION_TYPES_AND_MARKING.md](QUESTION_TYPES_AND_MARKING.md)) suit
the module — and which are unlikely, such as Python code questions for
a module with no programming content. The suggestions come with the
descriptor passages that prompted them, so the teacher can see the
reasoning.

These are suggestions and nothing more. The teacher chooses the
question types, can include a type the assistant considered unlikely,
and can ignore the suggestions entirely. No dewmark tool ever refuses a
question type on a descriptor's account.

## 4. What this route replaces

Because conversion is the normal route, dewmark does not depend on
teachers learning the exam file format, and the point-and-click exam
editor that such tools usually require becomes a convenience to add
later rather than a prerequisite. The format documentation
([THE_EXAM_FILE.md](THE_EXAM_FILE.md)) is still written for people, and
teachers who prefer to write the file directly can; but the format's
first duty is to be checkable, and the assistant's first duty is to
make that checkability available to teachers who will never open a text
editor.
