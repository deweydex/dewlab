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

**Tutorial body prose.** The largest surface, untouched by any of this, and the
one where flattening would cost the most. Worth doing deliberately, tutorial by
tutorial, rather than in a sweep.

**`docs/DEWMINI.md`.** Done. The guide a student reads to use dewmini, and
never covered by the first pass. It began at 116 issues and now reports none.

The commonest fault was the em dash carrying the sense: a short main clause,
a dash, and then the part a reader actually needed. Thirty-four sentences did
that. Forty-four ran past twenty-five words, several past forty, and one at
seventy-three. *Actually* appeared eleven times, and eight sentences had no
finite verb.

The count comes from `dev/check_plain_language.py`, which is new. It decides
what can be decided: sentences over twenty-five words, a sentence with no
finite verb, more than one em dash in a paragraph, the meaning falling after
the dash, *not x but y* reversals, the banned words, listed idioms, and emoji.
It says nothing about metaphor, hedging, or whether the sequence of a process
is marked, because those need a reader. A clean report is a floor and not a
pass, and this document was read as well as measured.

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
