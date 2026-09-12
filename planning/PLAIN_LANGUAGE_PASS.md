# The plain-language pass

Tracks what has been rewritten to `PEDAGOGICAL_STYLE_GUIDE.md` §4 "Plain
language", what has not, and what to do next.

---

## Why this exists

Section 4 governs *stance* — invitational, warm, prose not bullets — but not
sentence architecture, and section 1 says a reader may be working in a second
language and may not have done mathematics since school. Text can pass every
stance rule and still be hard to read. Nine rules in section 4 close that gap:

1. Meaning before the em dash, not after it.
2. Definitions as full sentences, not participles.
3. What a thing is before what it is not.
4. A plain statement before any metaphor, not instead of one.
5. No idiom that assumes Irish or British English.
6. No more than one aphorism per unit.
7. Sequences marked — first, then, then — not folded into one clause.
8. Claims hedged unless genuinely a binary.
9. (Vocabulary) rare words and idiom common to more than one dialect,
   pitched at a reader with roughly a two-thousand-word (B1) vocabulary.

`DECISIONS_LOG.md` 7.111 and 7.112 record the reasoning behind each rule and
what changing one would cost. Section 3 says what a name is *for* — the
reason the explore-then-name order matters and not only its ordering.

Two related threads are folded in below rather than tracked on a ledger of
their own: naming struggle and mistakes directly rather than only assuming
them in the design (section 11), and pointing a stuck reader at a real route
— the Reference panel, the topic tree, search — rather than only reassurance.

---

## Done

- **Contents page** (`render_index()` in `build.py`). Rewritten to cover what
  a cell is, the explore-then-name sequence, why answers are visible, that
  errors cost nothing, and where work is saved. 17.7 words/sentence down to
  9.6; longest sentence 37 down to 21; Flesch–Kincaid 9.4 down to 4.6.
- **About page** (`write_about_page()`). Split into three headings, and
  gained a short paragraph on why nothing is scored. 29.7 words/sentence down
  to 13.0; longest sentence 61 down to 27; Flesch–Kincaid 14.1 down to 5.8.
- **`docs/FOR_STUDENTS.md`.** A new "If a Page Stops Making Sense" section
  pointing a stuck reader at a real route rather than only reassurance, plus
  its reset-button and practice-fold paragraphs.
- **`docs/FAQ.md`** — new: orientation and logistics questions that come
  before a feature walkthrough, distinct from `FOR_STUDENTS.md`'s job.
- **The topic tree page furniture** — its introduction, colour key, and
  knowledge-map caption.
- **25 of 81 topic descriptions** in `planning/curriculum/topics.yaml`, and
  **64 of 251 glossary definitions** — the ones that broke the
  sentence-length or metaphor rules. Descriptions already plain were left
  alone.
- **35 topic descriptions written fresh**, for the thirteen topics later
  split into the parts a student meets separately — written to the checks
  directly rather than cut out of the parent's sentences.
- **All twelve database-methods tutorials**, across all three of its series
  (`first-database`, `several-tables`, `practice`). Recurring fixes: a
  `Term — definition` recap line, on every tutorial's "What you have now"
  list, rewritten as a full sentence with the term as subject; two double
  negatives about Reset rewritten as the plain positive claim each one
  meant; one em-dash mechanism explanation (`a-second-table-and-a-join`)
  reordered to say the mechanism before the cost; one idiom (*a football
  squad*) replaced with *a sports team*; a passive relationship definition
  (`designing-a-table-before-you-build-it`) rewritten to name the id column
  as the agent; a personifying idiom, a table that "answers to `SELECT`"
  (`loading-a-real-dataset`), replaced with a plain claim that you can query
  it.

Also picked up in the sibling repository `deweydex/dewstack`: the same
reset/practice-fold language in its README, its own new `FOR_STUDENTS.md`,
and a new FAQ page, adapted for a real difference between the two projects —
dewstack's two projects and exam are graded, so its reassurance is scoped to
the exercises rather than a blanket "nothing is scored."

**Twelve `web-authoring` tutorials ported from dewstack**: the `welcome`
series (how the pieces fit, a GitHub account, issues and pull requests,
an editor, your copy of the starter, publish it, the two loops, the
browser inspector) and the `shelf` series (FAQ, troubleshooting, quick
reference, project ideas). The prose itself needed little — dewstack
already writes to this same guide — but the same bold-lead-fragment habit
the database-methods pass found kept recurring in a different shape: a
term introduced as "**A username.** This becomes part of…" rather than a
sentence, the same pattern already fixed once in this module's own recap
lists. Ten instances across three pages (`a-github-account`'s username,
email address and password; `project-ideas`'s five project types)
rewritten into full sentences with the term itself in italics rather
than bold, matching this guide's own term-introduction convention rather
than a documentation-style definition list. This port also needed
platform-fact corrections (dewlab's own repository and PR in place of
dewstack's, the real save/reset model in place of a special case dewlab
doesn't have) — a different, adjacent kind of accuracy check to the
plain-language one, but done in the same pass since both mean actually
reading the sentence rather than trusting it.

**An idiom and vocabulary sweep across the documentation pages and the
first tutorial's opening** (`docs/FOR_STUDENTS.md`, `docs/FAQ.md`,
`write_about_page()` and `render_index()` in `build.py`, and the opening
sections of `first-steps.md`). This is the first pass against rule 9
(vocabulary, dialect-neutral idiom) on any surface.

Changes in `docs/FOR_STUDENTS.md`: "how you get on" → "how you do"; "docked"
→ "fixed to" (three occurrences); "straight away" → "right after"; "dock to"
→ "open on"; "page through" → "move through"; "grip" → "handle"; "cut across
that order" → "organise things differently"; "straight with you about its
gaps" → "you can see where it has gaps"; "half recognising" → "not quite
remembering"; "two folds" → "two hidden sections you can open"; "memory stick"
→ "USB drive" (two occurrences); "has got stuck" → "is stuck"; the long
em-dash sentence about dewmini split into two; "at the foot" → "at the
bottom".

Changes in `docs/FAQ.md`: "a mark against you" → "tells you something about
the method, not about you"; "Nothing stops you jumping" → "Nothing stops you
from jumping"; "at the foot of" → "at the bottom of".

Changes in `build.py` (About page): "a mark against you" → "not about you";
"glad of help" → "welcome help"; "at the foot of" → "at the bottom of".

Changes in `build.py` (contents page): "general principle" → "general idea";
"run all the way through" → "appear throughout"; "more abstract" → "more
open-ended".

Changes in `first-steps.md`: opening paragraph rewritten to remove three uses
of "algorithm" before the word is defined (at "What is an Algorithm?", fifty
lines later), following the project's own discover-then-name principle;
"mathematically" → "about maths"; "everyone who can do this had a first week
too" → "Everyone starts here" (removes an implied comparison a B1 reader
would need to unpack); "Interleaved" → "Set into"; "hallmarks" → "shows what
makes"; "terminates" → "finishes"; "clever" → "smart"; "nothing more and
nothing less" → "and only that"; "follow along?" → removed trailing idiom;
"valuable" → "useful"; "core loop" → "main pattern"; "translate" → "turn it
into".

---

## Not done — pick up here

**96 verbless fragments.** Noun-phrase definitions (*"One horizontal line of
a matrix."*) and participial openings (*"Answering a question by generating
many random cases…"*), across 5 built pages, 14 `topics.yaml` descriptions,
and 77 glossary entries. Not counted, on purpose: `uses:` bullets in
`topics.yaml` (correct as noun phrases in a list); verb-initial function and
operator entries (*"Displays whatever is inside its parentheses."*) — the
house convention, roughly forty of them, whether the dropped subject should
also go is still open; and formula or label-value lines, which aren't prose.

**The topic tree's own descriptions and the glossary, in the rules added
after the first pass.** The first pass fixed sentence length and metaphor
only — not sequence marking, reversals, "we"/"you", or hedging. Open
question: 251 short glossary definitions written as "we usually want…" could
wear on a reader scanning for a fact, so the glossary may want to stay closer
to plain statement than the tree descriptions do.

**A vocabulary sweep, against rule 9.** No surface has been checked against
it yet, including the ones already done for sentence architecture. A
mechanical first pass (flagging words outside a common two-thousand-word
list) is possible, but still needs a human read afterward.

**Tutorial body prose.** The largest remaining surface, and the one where
flattening would cost the most. The whole database-methods module is done —
see "Done" above — every other module untouched. Worth doing tutorial by
tutorial rather than in a sweep.

**A vocabulary sweep, against the ninth rule.** The documentation pages
(`FOR_STUDENTS.md`, `FAQ.md`), the About page, the contents page and the
first tutorial's opening have been swept (see above). The remaining surfaces
— tutorial body prose beyond the opening, topic descriptions, glossary
definitions — have not. A mechanical first pass is possible — a list of the
roughly two thousand most common English words, flagged the way
`tools/measure_sentences.py` (dewstack) flags a sentence over the limit — but
it still needs reading afterward, the same way that script's own docstring
says of itself.

**A tracked pass for the struggle/self-efficacy framing (section 11), if it
turns out to need one.** For now it's added opportunistically wherever a
page is already being touched for another reason.

**Staged hints.** Written against section 4 already: the default fold
title, the two Settings rows and their note in `assets/shell.html`, and
the hint fences in the four tutorials that carry them. Each new hint an
author writes is a new surface for this pass.

**`dewmini web`'s page copy.** One new student-facing surface
(`compose/dewminiweb.html`'s title, subtitle, and note, plus the homepage
paragraph linking to it), written against §4 as it was added. Its own
examples are the model for the next new page's copy.

**Bibliographies.** Unrelated to readability but still the largest
outstanding piece of style work — see section 8 of the style guide.

---

## How to check your own work

There is no linter for this. The checklist in section 9 of the style guide
is the tool. Two mechanical checks are worth running by hand over anything
you rewrite:

- **Sentence length.** Anything over twenty-five words wants a reason; past
  thirty it has two ideas in it.
- **Finite verb.** Read each sentence and find the verb. If there is not
  one, and the sentence is not a list item, a formula, or a label, it is a
  fragment.

Both are faster to do by eye on a diff than to automate, and automating the
second needs a part-of-speech tagger this repository has no reason to depend
on.
