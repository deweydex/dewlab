# Pedagogical style guide

How dewlab tutorials are written, and why. This merges two documents — Josh's
general guide for his QQI Level 5 classes, which governs all his teaching
materials, and an earlier dewlab-specific guide — into one that describes this
repository rather than a repository somebody imagined.

Where the two disagreed, section 8 says which won and on what grounds. Where
either disagreed with the code, the code won and the guide was corrected.

---

## 1. Who this is for

QQI Level 5, Irish further education, in Dublin. Adult learners, most returning
to education after a break, many balancing work and family with study. Prior
academic experience varies enormously inside one room, and confidence varies
more than ability does.

The practical consequences are specific rather than sentimental. Assume five to
seven hours a week including three or four contact hours, so a tutorial is an
hour of somebody's evening and not a chapter. Assume no prior knowledge without
saying so. Assume somebody in the room is reading this in their second language
and somebody else has not done mathematics since school and expects to be bad at
it.

The teaching this is rooted in is Freire's problem-posing education, Dewey on
experience, Kohn on what grades do to motivation, hooks on engaged pedagogy,
Finn on literacy and power, and Moses on mathematics as a civil right. That
lineage is not decoration. It is why nothing here is scored, why every answer is
visible to the student who wants it, and why the tutorials ask questions before
they give names.

---

## 2. What dewlab is for

Mathematics and programming as mutual partners rather than one serving the
other. Code is an instrument for building mathematical intuition; mathematics is
the structure underneath computational thinking. A student who has watched a
sequence of secant slopes settle onto a number has met the derivative in a way
that a definition cannot deliver.

The two things this makes possible, which paper cannot:

**You can just try it.** A limit is an argument on paper and an experiment here.
So is a probability, a sorting algorithm's cost, and the floating-point floor.

**Being wrong is cheap and visible.** A cell that raises an error in front of a
reader is better teaching than a warning that they might. Errors are diagnostic
information, not failures, and the runtime trims its own frames out of the
traceback so that what is left is the student's line.

---

## 3. How a tutorial is shaped

Not a rule, a rhythm. Most tutorials move through these and some earn a
different order.

**Open with the question.** What is this for, and where would somebody meet it?
The opening paragraph should be answerable to "why am I reading this", and a
reader who stops after it should have learned something.

**Give them something to run.** The first cell should work on the first click,
before anything has been explained. Confidence comes from the machine doing
something, and it comes early or not at all.

**Then the explanation.** Connect what the code did to what the mathematics
says. Formalise here, not before.

**Then their turn.** An active task with a starter cell, and a `hint:` if the
step is not obvious. A hint scaffolds; it does not answer.

**Then a check, where one is honest.** `check()` gives instant feedback and
records nothing. Not every task has a checkable answer, and forcing one produces
questions shaped by the checker rather than by the subject.

**Close by looking back.** What surprised you, what connects to what you already
built, what is still unclear. These are not decoration — for many students the
reflection is where the learning lands.

### Discover first, name afterwards

The order that matters most. Let a student halve a sorted list until the search
space collapses, and *then* say the words binary search and divide and conquer.
Let them multiply a transition matrix until the state vector stops moving, and
then say stationary distribution. A name given before the experience is a name
to memorise; a name given after it is a name for something they already have.

---

## 4. Voice

**Prose, not bullets.** Explanations are paragraphs. Bullets are for genuinely
discrete items — a checklist, a list of operators, four things that do not
follow from each other. An explanation broken into fragments has had its joins
removed, and the joins were the reasoning.

**Invitational, not commanding.** "Let's try", "what happens when", "how might
you". Not "Solve this problem" or "Complete the following". The difference is
whether the sentence positions the reader as somebody being told what to do or
somebody being invited to find something out.

This licenses "let's" and rules out imperatives aimed at the student. Both
halves matter and they are easy to confuse — see section 8.

**Warm without condescension.** Adult learners hear the difference immediately.
"This is easy" is the worst sentence available: if they find it hard, they now
have a second problem.

**Plain titles.** *Lines and Distances*, not *Coordinate Geometry*. *How We Got
Here*, not *The Computing Time Machine*. A title names what the reader gets in
words they already have.

**Define every technical term where it first appears**, and mark it in italics
the first time it means something particular. The build's vocabulary report
reads those italics and will tell you when a term is used before it is
introduced, or introduced twice with different meanings.

**No emoji**, unless Josh asks for them.

**Do not over-format.** Bold that appears in every paragraph has stopped meaning
anything.

---

## 5. Code in a tutorial

**Short cells.** Five to fifteen lines. A thirty-line cell has usually got two
ideas in it and wants to be two cells.

**No unmotivated boilerplate.** Every import earns its place. A student should
not meet a configuration line whose purpose cannot be explained yet.

**The seven tools are already there.** `show`, `show_table`, `check`,
`text_input`, `dropdown`, `button` and `load_csv` are injected into the page
namespace before any cell runs. Do not write `from tutorial_tools import check`
— it works, and it teaches an import that is not part of how the page functions.

**Figures need no `plt.show()`.** Creating a figure is enough; the runtime
collects it. `plt.show()` is harmless and two tutorials use it, which is a small
inconsistency worth removing rather than spreading.

**Cell ids are a contract.** Lowercase, hyphenated, `<section-slug>-<n>`. Once a
tutorial has been in front of a class, a cell id is the key somebody's saved work
lives under, and renaming one throws that work away. The editor warns about this;
believe it.

**Deliberate failure is a teaching tool.** A cell that divides by zero, in a
tutorial about what happens when you divide by zero, is better than a paragraph
saying it would. Say in the prose that it is meant to fail, so a reader does not
think they broke it.

---

## 6. Practice pages

Every tutorial has one, at `<slug>-practice.md`, declared with `practice_for:`.
Sets that draw on several tutorials use `practice_across:` and appear on the
contents page under their module.

**Answers go behind a fold beside the problem**, not in a key at the end:

```html
<details class="dl-answer"><summary>answer</summary>

The answer, with the working.

</details>
```

The `dl-answer` class is load-bearing — the styling and the fold marker come from
it. The site is public, so an answer that exists can be read and no arrangement
changes that; what is worth protecting is the moment before looking, and a fold
is that moment made physical.

**Hints go in a fold of their own, before the answer**, for problems where a
student can get genuinely stuck:

```html
<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first thing to work out.
2. What that lets you do next.
3. The step people usually miss.

**Think about:** the question that makes the method make sense.

**Try this next:** a related problem the same steps solve.

</details>
```

Two folds, opened in order, so a stuck student gets a route rather than the
answer. The reflection and the follow-on question at the end matter as much as
the steps — a hint that ends at the answer teaches the answer, and one that ends
in a related question teaches the method.

**A few tools per section, not a cell per problem.** One `python exec` cell
holding the helpers that section needs. Sixty editors on a page is a slow page,
and a cell under every question invites running it instead of thinking.

**Answers are shown with complete working.** Every step, including the ones that
look obvious. Note the common mistake where there is one, and give the second
method where a second method is illuminating.

**Every number in an answer gets run before it is published.** Twenty-one wrong
numbers were caught this way in one afternoon and none of them would have failed
a test, because no test asserts on prose.

---

## 7. Terminology

Moving between mathematics and programming makes some words ambiguous. These are
settled.

| Use | Not | Because |
|---|---|---|
| **power**, **exponent** — $x^2$, $2^n$ | *index*, *indices* for exponents | *Index* is reserved for a position in a list, `list[i]`, and for a summation bound. The syllabus says *laws of indices*; recognise it, and say power. |
| **mathematical function** $f(x) = x^2$, distinct from **Python function** `def f(x):` | conflating the two silently | One is a mapping, the other is a subroutine that may have side effects and may not be a mapping at all. |
| **spread** or **dispersion** for data; **`range()`** for the Python generator | "range" unqualified | The statistical range and the loop generator are unrelated and both come up in the same tutorial. |
| **set** $\{1, 2, 3\}$ | *list*, when order does not matter | Uniqueness and unorderedness are the point. |

---

## 8. Where the two guides disagreed

Recorded rather than silently resolved, because somebody will meet the same
question again.

**Whether "let's" is allowed.** The two versions of Josh's general guide differ
on this, and it is the only substantive difference between them. The earlier one
bans command language and names *"Let's do this!"* and *"Now we'll…"* as
examples. The revised one — `Josh_Educational_Reference_Document.md` — drops
those examples, narrows the ban to imperatives aimed at the student (*"Solve
this problem!"*, *"Complete this"*), and adds a positive requirement to use
"welcoming and invitational or reflective language, like 'let's try' or 'what
happens when' or 'how might you'".

**The revised one governs.** "Let's" is invitational — it puts the writer and
the reader on the same side of the problem — and the thing worth banning is the
imperative that puts the writer above the reader. This matters practically: the
tutorials are full of "let's", and reading the earlier guide literally would
have meant rewriting thirty-five files to remove the warmth Josh asked for.

**Bibliographies.** Josh's guide requires one in every tutorial, naming Khan
Academy, 3Blue1Brown, StatQuest, Computerphile, Ben Eater, Sebastian Lague and
others as the sources to prefer. **No tutorial in this repository has one.** That
is a real gap rather than a disagreement, and it is the largest single piece of
outstanding style work — thirty-five tutorials, each needing three or four
genuinely useful further-reading entries with working links.

**Stating learning outcomes at the start.** Josh's guide asks for them
explicitly; dewlab puts them in frontmatter under `covers:`, where the build and
the curriculum map read them and the student never sees them. The revised guide
softens this to "when relevant". Whether a student-visible outcome line is worth
adding is an open question for Josh — it would be a build change and a line on
every page.

**The `check()` example.** The earlier dewlab guide showed
`from tutorial_tools import check`. Unnecessary and now removed from this guide;
see section 5.

**The fold markup.** The earlier dewlab guide showed a bare
`<details><summary>Check solution</summary>`. The class is required; see section
6.

---

## 9. Before publishing

- Is the opening welcoming, and does it say why this is worth an hour?
- Can a student click **Run** and see something happen within a minute of
  arriving?
- Does the code produce something visible — a plot, a table, a number that means
  something?
- Are the cell ids unique, lowercase, hyphenated, and stable?
- Is every technical term defined where it first appears, and italicised once?
- Does the frontmatter declare `covers:` for what is taught and `touches:` for
  what is referenced?
- Are the explanations prose rather than bullets?
- Any command language aimed at the student? Any emoji?
- Has every number in the tutorial and its practice page actually been run?
- Does the practice page exist, and do hard problems carry a stepped hint?
- Is there a bibliography? (Today the honest answer is no. See section 8.)

---

## 10. Sources

The pedagogy this rests on:

Freire, P. (1970). *Pedagogy of the Oppressed.* Continuum.

Dewey, J. (1938). *Experience and Education.* Kappa Delta Pi.

Kohn, A. (1993). *Punished by Rewards.* Houghton Mifflin.

hooks, b. (1994). *Teaching to Transgress: Education as the Practice of
Freedom.* Routledge.

Finn, P. J. (1999). *Literacy with an Attitude: Educating Working-Class Children
in Their Own Self-Interest.* SUNY Press.

Moses, R. P. and Cobb, C. E. (2001). *Radical Equations: Civil Rights from
Mississippi to the Algebra Project.* Beacon Press.

QQI (Quality and Qualifications Ireland). Level 5 award requirements and module
descriptors. <https://www.qqi.ie/>

Sources to prefer when writing a tutorial's own bibliography: 3Blue1Brown for
visual mathematics, StatQuest for statistics, Computerphile for computer science
concepts, Ben Eater for architecture and low-level work, Sebastian Lague for
algorithms, Welch Labs for machine learning, and Khan Academy or MDN for
straightforward reference. Cite the original paper or a textbook where one
exists.
