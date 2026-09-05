# dewlab

Markdown in, a static site out. A tutorial is prose with editable Python cells
set into it; `build.py` turns `tutorials/**/*.md` into `site/`, and the Python
runs in the student's own browser tab. There is no backend, no database and no
API. `ARCHITECTURE.md` has the map; `DECISIONS_LOG.md` has the reasoning.

## Running things

```bash
pip install -r requirements-build.txt   # first time only
python3 build.py                        # writes site/ from scratch
python3 -m pytest                        # ~420 tests, under a minute
```

`site/` is gitignored and rebuilt every time. Never edit it. If you change
anything under `vendor-src/`, rebuild `assets/vendor/` with
`npm ci && npm run build` in `vendor-src/` and commit the result, or CI fails.

## Before you write a word a student will read

**Read `planning/PEDAGOGICAL_STYLE_GUIDE.md` §4, including its "Plain
language" subsection.** This is the rule that gets broken most often here,
because prose can satisfy every other rule in the guide and still be hard for
the reader §1 describes: an adult learner, often returning to education, often
reading in a second language, often expecting to be bad at maths.

Student-facing means the contents page, the About page, the topic tree, every
glossary definition, `planning/curriculum/topics.yaml`, every tutorial and
practice page, `docs/FOR_STUDENTS.md`, and any string in `build.py` that ends
up on a page. It does not mean code comments, planning documents or this file.

Nine checks. Run them over anything you write before you commit it:

1. **Does every sentence have a verb?** *Two ways of measuring an angle.* is a
   fragment. *There are two ways to measure an angle.* is a sentence. The one
   exception is a function or operator glossary entry, where the house form
   drops the subject and leads with the verb: *Displays whatever is inside its
   parentheses.*
2. **Does every clause earn its place?** Read the sentence back, then try a
   shorter version. If it still says the same thing, the clause that vanished
   was never necessary — whatever the sentence's length was. Length itself
   isn't the target; a list of four things may run long because the reader is
   counting, and a short sentence can still hide a clause that doesn't survive
   the trim.
3. **Is the meaning after an em dash?** A short main clause plus a dash
   carrying the real content reads well to somebody who already understands it
   and costs everybody else a re-read. One dash to a paragraph, never the one
   holding the definition.
4. **Does it say what a thing is before what it is not?** Contrast is a second
   pass. *Not x but y* only works for a reader who already has x.
5. **Is a sequence marked?** *First… then… then…* Two actions folded into one
   clause with an *and then* hide the order inside a single breath.
6. **Is a metaphor carrying the meaning?** It may follow a plain statement. It
   may not replace one. *How much skin a solid has* asks a reader to unpack an
   image before they can find the fact.
7. **Any idiom that assumes Irish or British English?** *Already behind you*,
   *paging through*, *it earns its keep*. The most invisible barrier here,
   because a native speaker cannot see them.
8. **Is a claim stated flat that is not a binary?** Hedge it — *usually comes
   afterwards*. State flatly only what is genuinely flat.
9. **Any idiom from another dialect, or a rare word where a common one would
   do?** Rule 7 covers Irish and British idiom specifically; this one covers
   every dialect, plus phrasal verbs with a one-word replacement (*carry on*
   → *continue*) and words like *obtain* or *commence* where *get* or *start*
   say the same thing. Pitched at a reader with a working vocabulary of about
   two thousand English words.

Two more things the guide settles that are easy to guess wrong:

- **"We" for the learning, "you" for what is the reader's own.** *We explore,
  then we name what we found.* *Your work is saved on this device.*
- **Explore, then the principle, then the name — and say what the name is
  for.** It is the word that lets a student talk to somebody else about the
  thing they just did. §3 has this.

`planning/PLAIN_LANGUAGE_PASS.md` records which surfaces have been through
this pass and which have not. Read it before starting on any of them, and
update it when you finish one.

## Where the rest lives

| Doing | Read |
|---|---|
| Writing or editing a tutorial | `docs/WRITING_TUTORIALS.md`, then the style guide |
| Writing a glossary file | `.claude/skills/tutorial-glossary/SKILL.md` |
| Reviewing a tutorial's cell code | `.claude/skills/cell-code-review/SKILL.md` |
| Working an issue opened through the report doors | `.claude/skills/triage-report/SKILL.md` |
| Changing the build or the runtime | `CONTRIBUTING.md`, then `ARCHITECTURE.md` |
| Wondering why something works the way it does | `DECISIONS_LOG.md` |

`CONTRIBUTING.md` has the rule that matters most when you touch code: a change
is not finished until the document describing that behaviour describes the new
behaviour. A stale comment is worse than no comment.

## Two traps

**Section numbers in the style guide are referenced from elsewhere** — the two
skills above, several planning documents, and `DECISIONS_LOG.md` all cite it as
"§4", "section 5" and so on. Add a subsection rather than renumbering.

**Cell ids are a contract.** Once a tutorial has been in front of a class, a
cell id is the key somebody's saved work lives under. Renaming one throws that
work away.
