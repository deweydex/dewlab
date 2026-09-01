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

Three steps, in that order: explore the problem, then the general principle
underneath it, then the name. And say what the name is *for*. It is not a label
the tutorial awards at the end for having paid attention. It is the word that
lets a student talk to somebody else about the thing they have just done — a
tutor, a classmate, a search box, the next tutorial. Saying that out loud is
what turns the naming step from a formality into the reason for it.

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

### Plain language

Everything above governs *stance* — who the sentence positions the reader as.
Nothing above governs *sentence architecture*, and section 1 says a reader may
be working in their second language and may not have done mathematics since
school. Prose can satisfy every rule in this section and still be hard for that
reader. These are the rules that close the gap.

**Say what a thing is before what it is not.** "An expression has a value; an
equation is a claim that two of them are equal" reaches a reader who knows
neither. "Not a value but a claim" only reaches one who already knows the first
half. Contrast is a second pass, not a first definition.

**A definition is a sentence with a subject and a verb.** *Standing in for a
process that would be slow to run for real, by working it out numerically
instead* is a participle with nothing to attach to; a reader has to supply the
missing "this topic is about" before they can start. Write "You work out what
would happen instead of running the real thing."

**One idea per sentence, and roughly twenty words.** Twenty-five is a ceiling
worth a reason; past thirty the sentence has two ideas in it and wants to be
two sentences. A list of four things is allowed to be longer, because the
reader is counting rather than following an argument.

**Put the meaning before the dash, not after it.** The habit this repository
fell into is a short main clause, an em dash, and then the part that actually
carries the sense. It reads beautifully to somebody who already understands
the sentence and it costs everyone else a re-read. One dash to a paragraph, and
never the one holding the definition.

**A labelled entry is still a sentence.** Reference material is a list of
labels, and the shape that suggests itself is *Name — what it is*. That is the
dash rule again, arriving once per entry because the genre invites it, so a
panel reference can break it eight times without any one of them looking
wrong. *Files — a real filesystem a cell can read and write to* becomes *Files
is a real filesystem a cell can read from and write to.* The label stays bold
and findable either way. Only the second one is a sentence the reader can
carry off.

**A metaphor illustrates a plain statement; it does not replace one.** *How
much skin a solid has*, *turning the probability toolkit outward onto the
machine*, *something to hang it on* — each asks a reader to unpack an image
before they can find the fact. Say the fact, then reach for the picture if it
earns its place. A picture that has to be decoded is a second problem, not a
help.

**No idiom that depends on knowing Irish or British English.** *Behind you*,
*paging through*, *cuts across that order*, *at the first dead end*, *it earns
its keep*, *the average that flatters*. These are the most invisible barrier in
the whole document, because a native speaker cannot see them.

**Ration the aphorism.** A unit that ends on a maxim rather than on information
is teaching the reader to expect a punchline, and at this density it trains
them to skim for it. Keep the best ones; that is what makes them the best ones.

**Put steps in the order they happen, and mark the order.** *First… then…
then…* Three short sentences in sequence show a reader where they are in a
process. Two actions folded into one clause with an *and then* hide the
sequence inside a single breath, and a reader who is not confident loses their
place in it. This is the cheapest fix on this page and the one that helps most.

**No reversals.** *Not the answer but the steps* asks a reader to hold a
negative in mind before there is anything to hold it against. *What we are
learning is the steps that get us there* says the same thing forwards. Put the
thing you actually mean in the subject of the sentence, and let it arrive in
the order it happens.

**"We" for the learning, "you" for what is theirs.** *We explore, then we name
what we found* puts the writer beside the reader in the work. *Your work is
saved on this device* is about their machine and their file, and a "we" there
would be a pretence. Keep the two apart and both stay honest.

**Hedge what is not a binary.** *Usually comes afterwards*, *is usually telling
us something useful*, *what usually comes first*. Most teaching claims have
exceptions, and a reader who meets the exception in their second tutorial
learns to distrust the flat ones. State flatly only what is genuinely flat —
*nothing you write leaves your browser* is a real binary, and hedging it would
read as evasion.

**The test.** Not whether the sentence is elegant. Whether a reader who is
unsure of themselves comes out of it feeling more able than they went in.

None of this asks for flat writing. Warmth is in the second person, in the
invitation, and in what the sentence does not assume about the reader — not in
figurative language. The plainest version of a sentence is usually also the
friendliest.

`CONTRIBUTING.md` ("Who reads what") has said most of this for the site's own
pages all along — *no jargon without explaining it, no metaphor for its own
sake, if you would not say it that way to a fifteen-year-old sitting next to
you, rewrite it*. It was never in the guide the tutorial writers read, so it
governed the homepage and not the teaching. It governs both now.

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

**Variable names read as words, not as the symbols a textbook would use.**
`count`, `total`, `midpoint`, `is_valid` — not `n`, `s`, `m`, `ok`, and not
the single mathematical letter a formula happens to use for the same
quantity (`a`, `b`, `c` for a quadratic's coefficients is the one common
exception: it matches the formula on the page directly above the cell, and
a reader translating between the two benefits from the names matching,
not diverging). A name earns its length by what it prevents a reader from
having to hold in their head — `row_total` over `t` in a cell with more
than one running sum, `left` and `right` over `a` and `b` once a cell is
about halves of something rather than about two arbitrary quantities.
`i`/`j` for a loop index and `x`/`y` for a coordinate are established
enough, in code and in the maths above it, to need no defence.

**One real exception: "discover first, name afterwards" (§3) can apply to
variable names too, not only to prose.** A cell exploring towards a
stationary distribution before that term has been said out loud is not
better for a variable called `stationary_distribution` — the generic
`state` or `vector` is the honest name for what the reader has actually
met so far, and the more specific name would spoil, in code, the exact
thing the prose is about to reveal in words. Reading the surrounding
prose, not just the cell in isolation, is what tells the two cases apart.

**Comments explain why, in the tutorial's own voice, not what the code
already says.** `# average the two coordinates` on `midpoint = (x1 + x2) /
2` tells a reader nothing `midpoint`'s own name did not; a comment worth
having says why this particular step matters or what a reader might
mistake it for. Not every cell needs one — a cell that is itself the
prose's worked example, walked through in the paragraphs around it, can
be more clearly commented needs no repeated commentary inside the code.
`hint:` (§ above) already carries this weight for a cell meant to make a
reader think before being told; a comment inside the cell is for
something worth knowing once you are already reading the code, not a
second hint competing with the first.

**Illustrative code and a "your turn" stub follow different rules from a
worked cell.** An untagged fence showing what a *finished* version of
something looks like earns the same naming and comment care as any other
cell. A stub cell — `# Your code here.`, with nothing to name yet — needs
none of this: there is no variable to rename in a cell that has none.

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
examples. The revised one — Josh's own educational reference document, kept outside
this repository — drops
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
- Is any sentence over twenty-five words, and does it need to be?
- Does every definition open with a subject and a verb, and say what the thing
  is before what it is not?
- Is any metaphor carrying the meaning rather than illustrating it? Any idiom
  that assumes Irish or British English?
- Where something happens in a sequence, is the sequence marked — first, then,
  then — rather than folded into one clause?
- Any reversal that makes the reader hold a negative before they have anything
  to hold it against?
- Is a claim stated flatly that is not actually a binary?
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
