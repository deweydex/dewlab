# Pedagogical style guide

How a dewlab tutorial talks to the person reading it, and why. Not a set of
essays to read once — a working reference to check a page against before it
ships.

---

## 1. Who this is for

QQI Level 5, Irish further education, in Dublin. Adult learners, most
returning to education after a break, many balancing work and family with
study. Prior academic experience varies enormously inside one room, and
confidence varies more than ability does.

Assume five to seven hours a week including three or four contact hours, so a
tutorial is an hour of somebody's evening, not a chapter. Assume no prior
knowledge without saying so. Assume somebody in the room is reading this in
their second language, and somebody else has not done mathematics since
school and expects to be bad at it.

Nothing here is scored. Every answer is visible to the student who wants it.
The tutorials ask a question before they give it a name. That is the whole
shape of the thing, and everything below is one consequence of it or another.

---

## 2. What dewlab is for

Mathematics and programming as partners, not one serving the other. Code is
an instrument for building mathematical intuition; mathematics is the
structure underneath computational thinking. A student who has watched a
sequence of secant slopes settle onto a number has met the derivative in a
way a definition cannot deliver.

Two things this makes possible that paper cannot:

**You can just try it.** A limit is an argument on paper and an experiment
here. So is a probability, a sorting algorithm's cost, a cipher's blind spot.

**Being wrong is cheap and visible.** A cell that raises an error in front of
a reader is better teaching than a paragraph saying it might. An error is
diagnostic information about a line, not a verdict on the person who ran it —
the runtime trims its own frames out of the traceback so what is left is the
student's own.

---

## 3. How a tutorial is shaped

Not a rule, a rhythm. Most tutorials move through these, and some earn a
different order.

**Open with the question.** What is this for, and where would somebody meet
it? A reader who stops after the opening paragraph should already have
learned something, not just been told what is coming.

**Give them something to run.** The first cell should work on the first
click, before anything has been explained. Confidence comes from the machine
doing something, and it comes early or not at all.

**Then the explanation.** Connect what the code did to what the mathematics
says. Formalise here, not before.

**Then their turn.** An active task with a starter cell, and a `hint:` if the
step is not obvious. A hint scaffolds; it does not answer.

**Then a check, where one is honest.** `check()` gives instant feedback and
records nothing. Not every task has a checkable answer, and forcing one
produces questions shaped by the checker rather than by the subject.

**Close by looking back.** What surprised you, what connects to what you
already built, what is still unclear. Not decoration — for many students the
reflection is where the learning actually lands.

### Discover first, name afterwards

The order that matters most. Let a student halve a sorted list until the
search space collapses, and *then* say the words binary search and divide
and conquer. A name given before the experience is a name to memorise; a
name given after it is a name for something the student already has.

Three steps, in that order: explore the problem, then the general principle
underneath it, then the name — and say what the name is *for*. It is not a
label awarded at the end for having paid attention. It is the word that lets
a student talk to somebody else about the thing they just did: a tutor, a
classmate, a search box, the next tutorial.

### Hints that wait for an attempt

A `hint:` line on a cell is there from the first click. A `hint` fence
(`docs/WRITING_TUTORIALS.md`) is not — it appears only once the cell above it
has run, and failed, some number of times, and the reader is never shown the
count. The delay is the point: help given too early saves a moment of
frustration and costs the learning; help given only after a real attempt
teaches the habit of asking a question before reaching for one.

Three folds, in order, and never more than a page needs:

**The first fold asks.** A question about what the reader can see and what
they expected — *what does the last line of the error name; which line of
your cell is it pointing at; what did you expect that line to produce?* A
question, not an instruction, because the habit worth teaching is asking it
unprompted, and an instruction just teaches obedience to the instruction.

**The second fold gives steps** — numbered, ending in a **Think about** and a
**Try this next** (§6 has the exact shape).

**A third fold, if any, gives the shape of the code with a gap in it.**
Never the answer. An answer belongs in a `dl-answer` fold the reader opens
for themselves.

Ration these the way §9 rations everything else that speaks to a stuck
reader: a "your turn" cell and a stub earn one; a worked cell does not. A
page where every cell produces a fold on the fifth error teaches readers to
stop reading them.

---

## 4. Voice

**Invitational, not commanding.** *Let's have a look*, *what happens if*,
*how might you write this*, *shall we?* Not *Solve this problem* or
*Complete the following*. The test is whether the sentence positions the
reader as somebody being invited to find something out, or somebody being
told what to do. This is the rule most worth protecting when a page gets
edited down for length — a trimmed sentence has a way of turning back into a
command if nobody is watching for it.

A tutorial is allowed a "we" that puts the writer beside the reader in the
work — *we've been making codes with the same alphabet*, *let's see what
happens when we compose these* — right up until the sentence is about
something that belongs to the reader alone, their own file, their own
answer, where "we" would be a pretence.

**Talk to the person, not the room.** *You should know that the concept of
functions is one of the most powerful ideas in mathematics* reaches one
reader; *students should know* reaches nobody. Second person, always, for
anything the reader is doing right now.

**Warm, without condescension, and honest about the difficulty.** Say
plainly that a topic causes "brain-pain," that a question is meant to be
harder than the last one, that the reader is allowed to find it hard. "This
is easy" is the worst sentence available — if a reader finds it hard
anyway, they now have a second problem. A joke, an aside, a footnote
confessing that nobody has agreed how to pluralise *gnomon* — these cost
nothing and tell a reader a person wrote this for them, not a system.

**Questions carry the content, not just introduce it.** *Can you write
triangle(4k) in terms of triangle(k)? Is there a picture that makes it make
sense?* does more teaching than the equivalent instruction, because it
leaves the reader something to do with their own thinking rather than a
fact to accept. Reach for a question before reaching for an assertion
wherever the reader could plausibly answer it themselves.

**Plain titles.** *Straight lines: slope, midpoint and distance*, not
*Coordinate Geometry*. A title names what the reader gets, in words they
already have. The usual shape is the term a student would search for,
then a colon and what the page does with it: *Inheritance: one class
built on another*, *Solving equations: linear, quadratic and
simultaneous*. Titles are in sentence case, and a practice page's title
is its tutorial's with " — Practice" added (see `DECISIONS_LOG.md` 7.213).

**Define every technical term where it first appears**, and mark it in
italics the first time it means something particular. The build's
vocabulary report reads those italics and flags a term used before it is
introduced, or introduced twice with different meanings. A page whose
key terms should stand out may set them in bold italics, `***term***`;
the italics are still what marks the term, and the tooling reads both.

**No emoji, unless Josh asks for them. Don't over-format.** Bold that
appears in every paragraph has stopped meaning anything.

### Plain language

Everything above governs *stance* — who the sentence positions the reader
as. Nothing above governs *sentence architecture*, and §1 says a reader may
be working in their second language and may not have done mathematics since
school. Prose can satisfy every rule above and still be hard for that
reader. Nine checks close the gap:

1. **Does every sentence have a verb?** *Two ways of measuring an angle* is
   a fragment. *There are two ways to measure an angle* is a sentence. The
   one exception is a function or operator glossary entry, which drops the
   subject and leads with the verb: *Displays whatever is inside its
   parentheses.*
2. **Does every clause earn its place?** Read the sentence back, then try a
   shorter version. If it still says the same thing, the clause that
   vanished was never necessary — whatever the sentence's length was.
3. **Is the meaning after an em dash?** A short main clause plus a dash
   carrying the real content reads well to somebody who already understands
   it, and costs everybody else a re-read. One dash per paragraph, never
   the one holding the definition.
4. **Does it say what a thing is before what it is not?** *Not x but y*
   only works for a reader who already has x.
5. **Is a sequence marked?** *First… then… then…* Two actions folded into
   one clause with an *and then* hide the order inside a single breath.
6. **Is a metaphor carrying the meaning?** It may follow a plain statement.
   It may not replace one.
7. **Any idiom that assumes Irish or British English?** *Already behind
   you*, *it earns its keep* — the most invisible barrier here, because a
   native speaker cannot see them.
8. **Is a claim stated flat that is not a binary?** Hedge it — *usually
   comes afterwards*. State flatly only what is genuinely flat.
9. **Any idiom from another dialect, or a rare word where a common one
   would do?** *Get*, not *obtain*. *Continue*, not *carry on*. Pitched at a
   reader with a working vocabulary of about two thousand English words.

### Warmth that survives translation

The plain-language checks above can be met by prose that is correct and
flat, and pages written to them have drifted that way. The voice this
guide is drawn from, Josh's own handouts (*Dear Student*, *Introduction
to Cryptography*, *Codes as Functions*), is plain and lively at once.
Its moves all survive a reader working in their second language, as long
as the words stay common:

- **A person is writing.** A page may say *I* for the writer's own
  stance: *I think this is the most surprising result on the page*. A
  letter is signed. Never invent the writer's history or experiences: a
  story about "when I was at school" is only written if the writer told
  it.
- **Name a feeling rarely, and always with a route.** Where a page
  knows a step is hard, it may say so once, and say what to do about it:
  *if this feels like hard work, open the hint under the cell, or come
  back to it after the next section*. A feeling named with nothing under
  it is a verdict on the reader (see "Name the feeling, then hand over
  the route" below; decided for #306/#310, 7.229).
- **Stop and wait.** *Pause here and guess. I'll wait.* A question the
  page does not answer straight away.
- **Give permission.** Skip ahead, come back, write in the margin, use
  your own names and notation as long as someone else can follow them.
  An answer fold says its answer is one good answer, and that the
  reader's may be more interesting.
- **Enjoy the surprise.** When a result is surprising, say so: *that is
  a strange result, isn't it?* Surprise is where interest comes from.
- **Asides.** A short story, a bit of history, a word from another
  language, a book worth reading. Put a long one in a note
  (`<aside class="dl-note">`), where it waits in the reference panel for
  a reader who wants it.
- **Humour in plain words.** A joke that needs an idiom (*it says on the
  tin*, *old chestnuts*) is lost on a second-language reader; a joke about
  a situation is not. A recurring character who makes the mistakes, and
  takes the blame for them, is funnier than any pun and makes an error
  something that happens to someone else first.

None of this relaxes the checks above. It is what the checks are for:
a reader who can follow every sentence, and wants to read the next one.

**"We" for the learning, "you" for what is the reader's own.** *We explore,
then we name what we found.* *Your work is saved on this device.*

**The test.** Not whether the sentence is elegant. Whether a reader who is
unsure of themselves comes out of it feeling more able than they went in.

---

## 5. Code in a tutorial

**Short cells.** Five to fifteen lines. A thirty-line cell has usually got
two ideas in it and wants to be two cells.

**No unmotivated boilerplate.** Every import earns its place. A student
should not meet a configuration line whose purpose cannot be explained yet.

**The tools are already there.** `show`, `show_table`, `check`,
`text_input`, `dropdown`, `button`, `image_input`, `load_csv`, `load_text`
and `run_query` are injected into the page namespace before any cell runs
(the full, current list is `docs/WRITING_TUTORIALS.md`'s own table — check
there rather than trusting a count here). Do not write
`from tutorial_tools import check` — it works, and it teaches an import
that is not part of how the page functions.

**Figures need no `plt.show()`.** Creating a figure is enough; the runtime
collects it. A `FuncAnimation` left as a cell's last expression is
collected too, as a moving picture, and it is worth reaching for wherever
the point is that something moves — after the reader has seen the frames
one at a time, not instead of it.

**Cell ids are a contract.** Lowercase, hyphenated, `<section-slug>-<n>`.
Once a tutorial has been in front of a class, a cell id is the key
somebody's saved work lives under, and renaming one throws that work away.
The editor warns about this; believe it.

**Deliberate failure is a teaching tool.** A cell that divides by zero, in a
tutorial about what happens when you divide by zero, is better than a
paragraph saying it would. Say in the prose that it is meant to fail, so a
reader does not think they broke it.

**Variable names read as words, not as the symbols a textbook would use.**
`count`, `total`, `midpoint`, `is_valid` — not `n`, `s`, `m`, `ok`, and not
the single letter a formula happens to use for the same quantity (`a`, `b`,
`c` for a quadratic's coefficients is the one common exception: it matches
the formula on the page directly above the cell). `i`/`j` for a loop index
and `x`/`y` for a coordinate are established enough, in code and in the
maths above it, to need no defence.

**"Discover first, name afterwards" (§3) applies to variable names too.** A
cell exploring towards a stationary distribution before that term has been
said out loud is not better for a variable called `stationary_distribution`
— `state` or `vector` is the honest name for what the reader has actually
met so far. Read the surrounding prose, not just the cell in isolation, to
tell the two cases apart.

**Comments explain why, not what the code already says.**
`# average the two coordinates` on `midpoint = (x1 + x2) / 2` tells a reader
nothing the name `midpoint` did not already. A comment worth having says why
this particular step matters, or what a reader might mistake it for — and a
cell that is itself the prose's worked example, walked through in the
paragraphs around it, often needs none at all.

**A "your turn" stub follows none of the naming or comment rules above** —
there is no variable to name in a cell that has none.

---

## 6. Practice pages

Every tutorial has one, at `<slug>-practice.md`, declared with
`practice_for:`. Sets that draw on several tutorials use
`practice_across:` and appear on the contents page under their module.

**Answers go behind a fold beside the problem**, not in a key at the end:

```html
<details class="dl-answer"><summary>answer</summary>

The answer, with the working.

</details>
```

The `dl-answer` class is load-bearing — the styling and the fold marker
come from it. The site is public, so an answer that exists can be read, and
no arrangement changes that; what is worth protecting is the moment before
looking, and a fold is that moment made physical.

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
answer. A hint that ends at the answer teaches the answer; one that ends in
a related question teaches the method.

**A few tools per section, not a cell per problem.** One `python exec` cell
holding the helpers that section needs. Sixty editors on a page is a slow
page, and a cell under every question invites running it instead of
thinking.

**Answers are shown with complete working**, every step including the ones
that look obvious, and **every number gets run before it is published** —
not reasoned about. A test asserts on code, never on prose, so a wrong
number in an answer is the one kind of mistake nothing catches for you.

---

## 7. Terminology

Moving between mathematics and programming makes some words ambiguous.
These are settled.

| Use | Not | Because |
|---|---|---|
| **power**, **exponent** — $x^2$, $2^n$ | *index*, *indices* for exponents | *Index* is reserved for a position in a list, `list[i]`, and for a summation bound. The syllabus says *laws of indices*; recognise it, and say power. |
| **mathematical function** $f(x) = x^2$, distinct from **Python function** `def f(x):` | conflating the two silently | One is a mapping, the other is a subroutine that may have side effects and may not be a mapping at all. |
| **spread** or **dispersion** for data; **`range()`** for the Python generator | "range" unqualified | The statistical range and the loop generator are unrelated and both come up in the same tutorial. |
| **set** $\{1, 2, 3\}$ | *list*, when order does not matter | Uniqueness and unorderedness are the point. |

---

## 8. Struggle, effort and self-worth

An error can quietly turn into a verdict on the reader instead of staying
information about a line. This section is about the moment right after a
mistake, where that turn happens or doesn't.

**An error is a fact about a line, not about the person who ran it.** Say
this directly, where a tutorial is already in the middle of demonstrating
it, rather than assume the point makes itself.

**Structural before verbal.** A reader who is stuck needs a real place to
go — the Reference panel, the topic tree, a step back to an earlier
tutorial — more than a sentence telling them they can do this. Naming the
route earns more trust than naming the feeling alone, for the same number
of words.

**Name the feeling, then hand over the route.** *Frustrated*, *stuck*,
*unsure what to do next* are fine to say plainly, and better than talking
around them. What is not fine is naming a feeling and leaving it to float
with nothing under it.

**Ration this.** Said once, at the place a tutorial is already
demonstrating it, this stays a real statement. Said in every tutorial's
error message, it becomes exactly the kind of maxim a reader learns to skim
past.

**The test.** Whether a reader who is stuck has somewhere real to go, not
only something reassuring to read.

---

## 9. Before publishing

- Is the opening welcoming, and does it say why this is worth an hour?
- Can a student click **Run** and see something happen within a minute of
  arriving?
- Does the code produce something visible — a plot, a table, a number that
  means something?
- Are the cell ids unique, lowercase, hyphenated, and stable?
- Is every technical term defined where it first appears, and italicised
  once?
- Does the frontmatter declare `covers:` for what is taught and `touches:`
  for what is referenced?
- Are the explanations prose, with a list only where it earns its
  place: the small steps of a task, what each part of a cell does, a
  few things to keep in mind, a set of things to try one at a time?
- Read each sentence back: does every clause survive a shorter version, and
  does it still sound right said aloud?
- Any idiom that assumes Irish or British English, or a rare word where a
  common one would do?
- Any command language aimed at the student? Any emoji?
- Has every number in the tutorial and its practice page actually been run?
- Does the practice page exist, and do hard problems carry a stepped hint?
- Where a mistake or a stuck moment is named, is a real next step named
  with it — not only the fact that it is normal? See §8.
- If this tutorial's own bibliography is thin, is there a real source to
  add — Khan Academy or MDN for reference, 3Blue1Brown for visual
  mathematics, StatQuest for statistics, Computerphile for computer
  science, Ben Eater for architecture, Sebastian Lague for algorithms? The
  original paper or a textbook, where one exists, beats all of them.
