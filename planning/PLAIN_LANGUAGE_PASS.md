# The plain-language pass

What has been rewritten to `PEDAGOGICAL_STYLE_GUIDE.md` section 4 "Plain
language", what has not, and what to do next. Written so that a session
picking this up months later does not have to rediscover the pattern.

---

## Why this exists

The student-facing text passed section 4 of the style guide as it stood —
invitational, warm, prose not bullets, no emoji — and was still hard to read.
Section 4 governed *stance*, and nothing in it governed sentence architecture,
while section 1 says a reader may be working in a second language and may not
have done mathematics since school.

Six habits ran through every surface in the same proportions:

1. A short main clause, an em dash, and then the part carrying the meaning.
2. Definitions written as participles rather than sentences.
3. Contrast before definition — *not x but y*, before x was ever said.
4. Metaphor standing in place of the plain statement rather than after it.
5. Irish and British idiom a native speaker cannot see.
6. An aphorism closing almost every unit.

Two more were named later, after the first pass had been through:

7. Steps folded into one clause with an *and then*, so the sequence is hidden.
8. Claims stated flat that are not binaries.

Section 4 now has a rule against each of the eight, and section 9 has a
checklist item for each. `DECISIONS_LOG.md` 7.111 and 7.112 record why, and
what changing any of it would cost. Section 3 says what a name is *for* — a student
talking to somebody else about the thing they just did — which is the reason
the explore-then-name order matters and not only its ordering.

A ninth was added later, in the "Vocabulary" subsection: the first eight
govern sentence architecture and dialect-specific idiom, and none of them
catches a rare word or an idiom common to more than one dialect — *having a
go*, *with the working* — that a B1-level reader still has to stop and guess
at. The test it sets is a reader with a working vocabulary of about two
thousand English words. Nothing has been swept against it yet; see "Not done"
below.

Alongside the plain-language pass, and not tracked by it, prose in a few
places has started naming struggle and mistakes directly rather than only
assuming them in the design (no scores, hints before answers, a resettable
cell). `docs/FOR_STUDENTS.md`'s reset-button and practice-fold paragraphs are
the first two; both also happened to fix rule 7 idiom violations from before
the ninth rule existed. This is a second, smaller axis than readability, and
it has no ledger of its own yet — see "Not done."

A second round added a "structural before verbal" version of the same idea:
a stuck reader is pointed at a real route (the Reference panel, the topic
tree, search) rather than told only that it is normal to be stuck. New in
`docs/FOR_STUDENTS.md` ("If a Page Stops Making Sense") and `docs/FAQ.md`
(new — orientation and logistics questions that come before a feature
walkthrough, distinct from `FOR_STUDENTS.md`'s job). The About page
(`write_about_page()` in `build.py`) gained a short paragraph saying why the
project exists and why nothing is scored, which it had never said despite
section 2 saying it at length. `dewstack`'s README, its own new
`docs/FOR_STUDENTS.md`, and its new FAQ page (`tutorials/reference/faq/`,
in the reference shelf) all picked up the same pattern, adapted to a real
difference the two projects have: dewstack's tutorials are not graded, but
the course's two projects and its exam are, so the reassurance there is
about the exercises specifically, not a blanket "nothing is scored."

---

## Done

**The contents page** (`render_index()` in `build.py`). One paragraph and six
points, in the order a reader meets them: what a cell is, the explore-then-name
sequence, practice problems and why the answers are visible, that errors cost
nothing, where the work is saved, and how the list below is organised. 17.7
words per sentence down to 9.6; longest sentence 37 down to 21; Flesch–Kincaid
9.4 down to 4.6. It grew from 254 words to 308 because it now covers three
things it did not cover at all.

**The About page** (`write_about_page()` in `build.py`). Three headings rather
than one run of paragraphs. 29.7 words per sentence down to 13.0; longest
sentence 61 down to 27; Flesch–Kincaid 14.1 down to 5.8.

**The topic tree page furniture** — its introduction, colour key and
knowledge-map caption.

**25 of 81 topic descriptions** in `planning/curriculum/topics.yaml`, and
**64 of 251 glossary definitions**, being the ones that breached the
sentence-length or metaphor rules. Descriptions already plain were left alone.

**35 topic descriptions written fresh** when thirteen topics were split into
the parts a student actually meets separately. Each child was written to the
eight checks rather than cut out of its parent's sentences, so none of them
carries the fragments or the em-dash definitions the pass exists to remove.
Fourteen of the older descriptions in the same file are still on the list
below.

---

## Not done — pick up here

**Verbless fragments, 96 of them.** Sentences with no finite verb at all:
noun-phrase definitions (*"One horizontal line of a matrix."*, *"Two ways of
measuring an angle."*) and participial openings (*"Answering a question by
generating many random cases…"*). They break down as five on the built pages,
14 in `topics.yaml` descriptions, and 77 in the glossaries.

Three things are *not* in that count, on purpose:

- **`uses:` bullets in `topics.yaml`.** They render as `<ul class="dl-tree-uses">`
  in `assets/tree.js`. A noun-phrase list item is correct in a list.
- **Verb-initial definitions** — *"Displays whatever is inside its
  parentheses."* These have a finite verb and an elliptical subject, which is
  the house convention for function and operator entries. There are roughly
  forty. Whether the dropped subject should also go is an open question.
- **Formula lines and label-value pairs** — *"Circle: area = pi*r^2"*,
  *"Contact: …"*. Not prose.

**The topic tree's own descriptions and the glossary in the new voice.** The
first pass fixed sentence length and metaphor. It did not apply the rules added
afterwards: sequence marked with *first / then / then*, no reversals, "we" for
the learning and "you" for what is the reader's own, hedging what is not a
binary. An open question worth settling before starting: 251 short definitions
written as *"we usually want…"* could get wearing where a reader is scanning
for a fact, and the glossary may want to stay closer to plain statement than
the tree descriptions do.

**A vocabulary sweep, against the ninth rule.** No surface has been checked
against it yet, including the ones already done for sentence architecture. A
mechanical first pass is possible — a list of the roughly two thousand most
common English words, flagged the way `tools/measure_sentences.py` (dewstack)
flags a sentence over the limit — but it still needs reading afterward, the
same way that script's own docstring says of itself.

**Tutorial body prose.** The largest surface, untouched by any of this, and the
one where flattening would cost the most. Worth doing deliberately, tutorial by
tutorial, rather than in a sweep.

**A tracked pass for the struggle/self-efficacy framing**, if it turns out to
need one. For now it is being added opportunistically wherever a page is
already being touched for another reason, not swept on its own — a larger,
dedicated set of pages on this was raised and deliberately deferred, to keep
this addition small until that decision is made.

**Bibliographies.** Unrelated to readability but still the largest outstanding
piece of style work — see section 8 of the style guide.

---

## How to check your own work

There is no linter for this. The checklist in section 9 of the style guide is
the tool. Two mechanical checks are worth running by hand over anything you
rewrite:

- **Sentence length.** Anything over twenty-five words wants a reason; past
  thirty it has two ideas in it.
- **Finite verb.** Read each sentence and find the verb. If there is not one,
  and the sentence is not a list item, a formula or a label, it is a fragment.

Both are faster to do by eye on a diff than to automate, and automating the
second needs a part-of-speech tagger this repository has no reason to depend
on.
