# A question a tutorial can ask without writing Python: a design note

Written 2026-09-15, in answer to Josh asking for dropdowns and multiple
choice in a tutorial, and for a format that dewnote can write and dewlab
can build.

**Nothing here is built yet.** This document exists so the shape can be
argued with before either repository writes a line of it. §8 says what
would be built, in what order, and where.

---

## 1. What is being asked for, and what already answers part of it

A tutorial wants to stop and ask the reader something. Not to score them
— dewlab scores nothing and records nothing — but because a question the
reader answers before reading on is worth more than a paragraph telling
them the same thing.

Two shapes cover almost all of it:

- **Multiple choice.** A question, a few options, one of them right.
- **A choice inside a sentence.** A sentence with a gap in it, and a
  small list to pick the missing words from. Often several in a row.

dewlab can already do both, and has been able to for some time.
`assets/tutorial_tools.py` has `dropdown`, `text_input`, `button` and
`check`, so a question today is written as Python inside an exec cell:

````markdown
```python exec
id: right-angle
answer = dropdown("A 90 degree angle is called:",
                  ["a right angle", "a straight angle", "an acute angle"])
button("Check", lambda: check(answer.value, "a right angle"))
```
````

That works, and it is the reason this is a small piece of work rather
than a large one: the runtime question — what happens when a reader
answers — is already settled. Three things are wrong with it as the way
an author writes a question.

**It downloads Pyodide to ask a question.** A tutorial page loads the
Python runtime the first time a cell runs. Several megabytes, and a wait,
so that a reader can pick one of three words. On a phone, on a slow
connection, in a room of thirty students on the same wifi, that is the
whole cost of the page paid for the smallest thing on it.

**It cannot be read as a question.** The markdown says `dropdown(...)`
and `lambda`. Somebody reviewing a tutorial for whether its questions are
any good has to read Python to find out what is being asked.

**It cannot be written without Python.** Every other thing an author does
in a tutorial is prose, a fold, a picture or a link. A question is the
one thing that requires a second language, and it requires it of exactly
the author least likely to have it.

So this is not a missing capability. It is a missing *form* for a
capability dewlab already has.

## 2. The shape: a `question` fence, with dewlab's own header grammar

````markdown
```question
id: right-angle
type: multiple-choice
correct: 2

Which of these is a right angle?

- 45 degrees
- 90 degrees
- 180 degrees
```
````

The header is flat `key: value` lines, read exactly the way
`parse_cell()` reads an exec fence's `id:` and `hint:` — the same
`HEADER_RE`, the same "stop at the first line that isn't a header"
rule. What follows the blank line is ordinary markdown: the prose before
the first list is the question, and the first list is the options.

Three header lines, and only three:

- **`id:`** — required, and a contract on the same terms a cell id is. It
  is the key the reader's own answer is saved under, so renaming one
  throws that answer away. Ids are unique across a page, questions and
  cells together, because they share one saved-work record.
- **`type:`** — required. Spelled out in full, which is dewmark's own
  rule for the same field: *"the type names are deliberately spelled out
  in full, so that anyone reading the exam file can say what each part of
  the exam is without a reference card."*
- **`correct:`** — the right option's position in the list as written,
  counting from 1. Also dewmark's convention.

### 2.1 Why markdown after the header, rather than YAML throughout

dewmark's exam blocks are YAML from top to bottom, options included:

```answer
type: multiple-choice
options:
  - y = 2x + 1
  - y = x^2 + 1
correct: 1
```

That is right for an exam file, where a question is short and the
machine-checkable facts are the point. It is wrong here, and the reason
is that a tutorial's question is *student-facing prose*.

Everything a student reads in dewlab goes through the same checks —
`PEDAGOGICAL_STYLE_GUIDE.md` §4, the plain-language pass,
`tools/measure_sentences.py`. Prose inside a YAML scalar is prose those
checks and tools do not see as prose. It also loses markdown: no code
span in an option, no emphasis in a prompt, no picture, and quoting rules
to remember for any option that happens to start with a digit or contain
a colon.

Putting the prose in markdown costs the copy-paste: an exam question and
a tutorial question are not the same text. What ports is everything that
matters — `type:` names, `correct:` by position, and §3's `{...}` — so an
author who knows one can read the other.

## 3. A choice inside a sentence

````markdown
```question
id: angle-names
type: fill-in-the-blank

An angle of 90 degrees is a {right angle|straight angle|acute angle}.
An angle of 180 degrees is a {straight angle|right angle}.
```
````

The whole body is the sentence. Each `{...}` is a gap, and the first
thing in it is the answer. A gap with no `|` in it is a typing box rather
than a list, which is dewmark's `fill-in-the-blank` exactly:

```
The {mitochondrion} is the site of aerobic respiration.
```

So one type covers both, and which one a gap is depends only on whether
the author offered a choice.

**The page shows the choices in a shuffled order.** If it did not, the
answer would always be first, and a reader would learn that faster than
they learn the material. `correct:` in §2 does not need this because the
build knows which option is right and can shuffle the display while
keeping the written order for the saved answer; here the same applies.
dewmark deliberately does *not* shuffle, for a reason that does not hold
here: a printed paper and a marking discussion have to be able to say
"option 3" and mean the same thing to everybody. A tutorial has no marker
and no appeal.

## 4. What the reader sees, and what is deliberately not there

The question, the options, and a **Check** button. Before the button is
pressed, nothing says anything. After it:

- **Right** — a line saying so, and the question stays answerable, so a
  reader can go back and see why the others were wrong.
- **Not yet** — a line saying so, and the reader can choose again.

No score. No count of attempts shown to the reader. No "3 out of 5". A
tutorial that keeps score turns a reader who is learning into a reader
who is performing, and §2 of the style guide is explicit about which of
those dewlab is for.

**Per-option feedback is not in this version, on purpose.** It is the
obvious next thing to want — *that is half a right angle* under the
wrong choice — and it is one more header line or one more list to add
when somebody has written enough questions to know what they want to say
under them. dewlab already has a better-developed answer for "the reader
is stuck": the `hint` fence, staged, which `planning/CELL_HINTS.md`
settles at length. A question can sit above one.

## 5. The answer is in the page, and that is the trade

There is no backend. `correct:` reaches the browser, so a reader who
opens the page source can read it.

This is the right trade for a self-check and the wrong one for an
assessment, and the format should not pretend otherwise. dewmark is where
assessment lives: its exam builder keeps `correct:` out of the student
paper entirely, and that is the whole reason it is a separate program
with a separate file format. A `question` fence is for a tutorial asking
whether the last three paragraphs landed.

## 6. What it costs dewlab's build, which is less than it looks

`extract_blocks()` already lifts every fence out of the markdown and
leaves an HTML comment placeholder, before the markdown converter runs.
A `question` fence joins `exec`, `hint`, `card` and `html|css|js site` as
a fifth kind handled there, and it inherits the property that makes that
architecture worth having: nothing inside a fence can be reinterpreted as
markup.

It also inherits a useful accident. **An unknown fence tag does not fail
the build today** — `extract_blocks()` falls through to an illustrative,
read-only code block. So a `question` fence written before dewlab knows
the word renders as a visible code block on the page: wrong, obvious, and
harmless. That is the migration path. dewnote can write these the day the
format is agreed, and no site breaks while dewlab catches up.

What has to be written:

- `parse_question()`, beside `parse_cell()`. The header loop is the same
  loop; the tail is a markdown split rather than `expand_includes()`.
- Checks that fail the build, in the house style — every one of these is
  an error a real author will make:
  - no `id:`, or an `id:` a cell on the same page already uses;
  - a `type:` that is not one of the two;
  - `correct:` naming a position the list does not have, or missing on a
    `multiple-choice`;
  - fewer than two options;
  - a `fill-in-the-blank` with no `{...}` in it;
  - an unclosed `{`.
- Rendering, which is HTML plus a small piece of the existing tutorial
  runtime — the `check` styling (`_check_html`) is already written and
  already looks right.
- Saving the answer under the question's id, in the record that already
  holds cell code.

None of it needs Pyodide, which is the point: a page whose only
interactive thing is a question loads no Python runtime at all.

## 7. What is still open

**Per-option feedback.** §4 says why it is out of this version. It is a
question about what authors actually want to say, and the honest answer
is that nobody here has written twenty of these yet.

**Whether several gaps in one sentence should be checked together or
one at a time.** §3's example has two sentences with one gap each, which
is the easy case. A sentence with three gaps could check on each choice
or wait for a Check button. Waiting is probably right — checking as you
go turns it into a guessing game — but this is a guess.

**Whether a question should be able to close a fold, or open one.** A
right answer revealing the next section is a real teaching move and a
real complication. Not now.

## 8. What would be built, and in what order

1. **Here, in dewlab.** `parse_question()`, the build checks in §6, the
   rendering, and the saved answer. One tutorial converted to use it, so
   the format is proved against real writing rather than an example in
   this document.
2. **In dewnote.** A **Question** item in the block menu that writes the
   §2 form with its placeholders, the way **Practice problem** writes
   §6 of the style guide's form. It is a template, so it costs one entry
   in a table — the menu was rebuilt in dewnote's own decision 45 to make
   exactly this cheap.

In that order, because the editor should write a form the build already
reads. dewnote's decision 44 took the same view about practice pages and
it was right.
