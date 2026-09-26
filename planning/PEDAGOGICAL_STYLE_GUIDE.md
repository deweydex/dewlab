# Pedagogical style guide

Why a dewlab page teaches the way it does. The mechanics (fences, folds,
cell ids, the tools a cell can call) are in
[`docs/WRITING_TUTORIALS.md`](../docs/WRITING_TUTORIALS.md). This page
keeps only the reasons, so it can be read in one sitting and held up
against a page before it ships.

Cite a part of it by its anchor, as `PEDAGOGICAL_STYLE_GUIDE.md#voice`,
never by a number. `dev/check_doc_links.py` fails on an anchor that does
not exist here, and on a citation by section number.

<a id="who-reads-this"></a>
## Who reads this

QQI Level 5, Irish further education, in Dublin. Adults, most coming back
to education after a break, many fitting study around work and family.
In one room, experience runs from none at all to a degree in something
else, and confidence varies more than ability does. Somebody is reading
in their second language. Somebody has not done mathematics since school
and expects to be bad at it. Somebody already programs and is bored.

Some readers have needs the page cannot see: dyslexia, a screen reader,
low vision, a phone as their only screen. Short paragraphs, real
headings, a description on every picture, and colour that is never the
only signal serve all of them and cost nobody else anything.

A page is read in two places. In class, a teacher is in the room and a
stuck reader can ask. At home, at ten at night, nobody is. Write for
home: a page that works there works in class too.

About five to seven hours a week, three or four of them in class. A
tutorial is an hour of somebody's evening, not a chapter.

<a id="how-learning-happens"></a>
## How learning happens here

Mathematics and programming are partners here. Code is where a reader
tries an idea; mathematics is the structure under the code. Two things
follow that paper cannot offer: a reader can just try it, and being
wrong is cheap and visible. These principles were decided for the
2026 revision (#306; `DECISIONS_LOG.md` 7.230). Everything else on this
page follows from them.

<a id="no-verdicts"></a>
**No verdicts.** The site never tells a reader they are right or wrong.
It shows what their code did and, when they ask, what a solution does
with the same inputs. A mismatch is information about a line, not a
judgement of a person. `check()` and its ticks were retired for this
reason (#314). The quiet verdicts count too: *not yet*, *fair*,
*strong*, *honest*, *sound*, *the tests are the judge*. So does a
verdict raised only to deny it: *Is that a foolish move? No.*

<a id="mistakes"></a>
**Mistakes are part of the process.** A wrong prediction is the most
useful kind. An error is a fact about one line, on one run. Pages make
mistakes on purpose, say that they are doing it, and enjoy what the
mistake shows.

<a id="discover-then-name"></a>
**Discover, then name.** Let a reader halve a sorted list until there is
nothing left to search, and then say *binary search*. A name given
before the experience is a word to memorise. A name given after it is a
handle for something the reader already has, and a way to talk about it
with somebody else. The opening of a page still teaches: it runs or
shows something, and asks about it. It does not define.

<a id="predict-then-run"></a>
**Predict in writing, then run.** A guess written down before a cell
runs turns the output into an answer to the reader's own question. "What
do you think? Run the cell to check" in one breath is not a prediction.
The page has to stop and wait.

<a id="worked-completed-own"></a>
**Worked, then completed, then your own.** First an example the reader
runs and changes. Then one with a gap to fill. Then a task with no
scaffold at all. A page moves along that line, and so does a series.

<a id="nothing-taught-once"></a>
**Nothing is taught once.** Every practice page carries two or three
problems from earlier pages, and every series and course has a mixed
set. Remembering something a week later does more than a second example
today.

<a id="low-floor-high-ceiling"></a>
**Low floor, high ceiling.** Every task has a first step anyone can take,
and no top. A reader who finishes early finds more to do.

<a id="choice-of-world"></a>
**The reader chooses the world.** A series offers several worlds
(planets, the sea floor, pixel art, ciphers, games) and the reader picks
one, page by page. A page teaches in one world, and its tasks, practice
and project steps follow the reader's choice. Wonder beats worthiness: a
dinosaur's mass beats a bank balance. Invented data is fine when the
page says it is invented. (Choosing one:
`docs/WRITING_TUTORIALS.md#choosing-a-context`.)

<a id="closer-look"></a>
**A misconception gets a page of its own.** A misconception worth
teaching is taught on a "closer look" page, experiment first: both ideas
make a prediction, and only one matches what happens. It is never
flagged on a reader's answer, because that would be a verdict.

<a id="page-shapes"></a>
## Page shapes

Five kinds of page, each with its own job. Each has a working template in
[`docs/templates/`](../docs/templates/README.md), and
[`docs/WRITING_TUTORIALS.md`](../docs/WRITING_TUTORIALS.md#page-templates)
has the mechanics. A mixed set is a practice page that draws on a whole
series or course.

- **A tutorial** teaches one idea in about an hour. It opens by running
  or showing something ("On this page we:" is optional). A line-by-line
  walk through a cell sits in a fold, after a prompt to try changing
  something. It closes with one question that belongs to this page, a
  challenge, the reader's own surprises, and links to its practice page
  and to the Notebook or the Workspace.
- **A practice page** mixes kinds of problem (predict, make, fix,
  explain, another way, open-ended) in whatever mix suits the page, and
  adds two or three from earlier pages. A solution can come in two
  tiers: "with what you've met so far" and "a shorter way you'll meet
  later". Mathematics done by hand gets a "one way through it" fold.
- **A series-end making task** is something the reader makes of their
  own, in their world, with the whole series.
- **A project brief** has a group version and an individual version. It
  is judged by reflection questions only, with no rubric shown to
  students. How a class runs it is the teacher's decision.
- **A closer look** takes one misconception, experiment first, and then
  explains why the wrong idea is so natural to hold.

Every page ends with somewhere real to read more: the original paper or
a textbook where one exists, or a channel such as 3Blue1Brown,
Computerphile, Numberphile or Sebastian Lague.

<a id="voice"></a>
## Voice

<a id="plain-and-alive"></a>
**Plain and alive.** Common words, short sentences, a person writing.
This is the voice, from the plan:

> Here's a loop that adds up a week of spending. Before you run it,
> guess what the last line will print. I'll wait.
>
> Did you say 12? Most people do.
>
> Now move `spent = 0` inside the loop, just above the addition, and run
> it again. You get 4. That's a strange result, isn't it? Nothing is
> broken. The loop did exactly what it was told: every time round, it
> started counting from nothing.

A guess is invited and waited for, and the surprise is enjoyed. A page
may say *I* for the writer's own view, but never invents the writer's
history. Humour is about a situation, never an idiom. A recurring
character who makes the mistakes, and takes the blame for them, makes an
error something that happens to somebody else first.

<a id="plain-language"></a>
**Plain language.** Write for a reader with about two thousand common
English words, who may be reading in their second language.

- Every sentence has a verb. A glossary entry for a function may start
  with its verb: *Displays whatever is inside its parentheses.*
- Try a shorter version of each sentence. If it says the same, keep it.
- Say what a thing is before what it is not.
- Mark a sequence: *first… then… then*.
- A metaphor may follow a plain statement. It never replaces one.
- Never hide the meaning after a dash. One dash in a paragraph, at most.
- Hedge a claim that is not a yes or a no: *usually comes afterwards*.
- Use the common word: *get*, not *obtain*.
- **Phrasal verbs are the main barrier** for a second-language reader,
  and a native speaker cannot see them. *Work out*, *carry on*, *turn
  out*, *set up* and *give up* each mean several things. Use one word
  where a common one exists: *find*, *continue*, *happen*, *prepare*,
  *stop*. Idioms from any dialect go the same way: *already behind you*,
  *says on the tin*. The ones that keep coming back: *work out* (use
  *find*), *give back* (use *return*), *go through* and *reach in* (use
  *use*), *throw away* (use *delete*), *left behind*, *read off*, and
  *out of order*, which in Dublin means *broken*.

<a id="say-it-directly"></a>
**Say it directly.** Somebody or something does something, in that
order. Clever framing reads well to the writer and costs a
second-language reader two reads. Each of these came from a real page.

- **A verb, not a noun made from one.** Not *the deciding can be tested
  if it is kept apart from the asking*. Write *you can test the code
  that decides, if it is in its own function*.
- **A sentence has a subject and a verb.** Not *Two front ends, one set
  of classes: the classes never knew which one was asking*. Write *We
  now have two front ends. The classes do not know which one is
  asking.* A heading may be a label; a sentence may not.
- **Say the thing first.** Not *What changes is where the rules live*.
  Write *A class changes where the rules live*. Not *Getting stuck is
  where most of the learning happens*. Write *You learn most when you
  are stuck*.
- **A colon brings in a list or an example.** The main point never
  waits behind one. Not *Where does the rule live? Nowhere: every line
  has to remember it*. Write *The rule is not in one place. Every line
  has to remember it.*
- **End on the fact, not a saying.** A closing line that says the
  paragraph again, cleverly, goes. *"Has a" bends where "is a" breaks*,
  *only as good as*, *the tests are the judge*.
- **No reversals or mirror pairs.** *The first thing the cell does is
  the last thing it shows* makes the reader solve a puzzle. Write *The
  cell prints this line first, so it is at the top of the output.*
- **No private words.** A metaphor or a planning word the reader was
  never given stays off the page: *no top*, *floor*, *ceiling*, *a door
  left open*, *earns its place*, *that is sequence, our third
  question*. If a metaphor is worth using across a series, say it
  plainly on the page where it first appears.
- **A sentence that repeats across pages is written once.** The line in
  an answer fold is *Here is one answer. Yours may be different and
  work too.*

<a id="invitations"></a>
**Tasks are invitations.** A task is a question, a challenge, or a
"let's see what happens when…": *Can you make the loop count backwards?
What happens to the total when the list is empty?* Once a task is posed,
the steps for doing it may be plain instructions, as in the voice above:
*move `spent = 0` inside the loop, and run it again*. What is never an
order is the thinking itself: not *Explain why…*, not *Complete the
following*.

<a id="feelings"></a>
**Name a feeling rarely, and always with a route.** Where a page knows a
step is hard, it may say so once, with what to do about it: *if this
feels like hard work, open the hint under the cell, or come back after
the next section*. A feeling named with nothing under it becomes a
verdict on the reader (7.229). A route helps more than reassurance.

**"We" for the learning, "you" for what is the reader's own.** *We
explore, then we name what we found.* *Your work is saved on this
device.*

**Plain titles.** The term a student would search for, a colon, and what
the page does with it: *Inheritance: one class built on another*.
Sentence case.

<a id="before-and-after"></a>
**Two pairs from real pages.**

> *Before* (`lists-and-sequences`): Which scores will each version keep?
> Run the cell to check.
>
> *After:* Which scores will each version keep? Write your guess in a
> comment first. Then run the cell. Did the two versions agree with each
> other, and with you?

> *Before* (`finding-things-practice`): Write a function that finds *all*
> the indexes where a target appears.
>
> *After:* Our search stops at the first match. Can you make one that
> keeps going, and gives back every index where the target appears? What
> should it give back when there are none?

<a id="stuck"></a>
## When a reader is stuck

Help waits for an attempt. Help given too early saves a moment of
frustration and costs the learning. Help given after a real attempt
teaches the habit of asking a question before reaching for an answer.

- **The first hint asks.** It is a question about what the reader can
  see and what they expected: *what does the last line of the error
  name?* The second gives steps, ending in something to think about and
  a related problem. A third, if there is one, gives the shape of the
  code with a gap in it. None of them gives the answer.
- **An answer is opened, never pushed.** It sits in a fold the reader
  opens for themselves, and it says it is one good answer. The reader's
  may be more interesting.
- **A prediction has a way out.** "I'm not sure yet" is always a choice,
  and it leads to a hint, not a penalty (#313).
- **Ration it.** A "your turn" cell gets staged hints; a worked cell
  does not. A page where every cell grows a hint teaches readers to
  ignore them.
- **The route is real.** A stuck reader needs somewhere to go: a hint,
  the Reference panel, an earlier page. Say where, once, at the place it
  is needed.

<a id="code"></a>
## Code

- **Short cells**, five to fifteen lines. A thirty-line cell usually has
  two ideas in it, and wants to be two cells.
- **Every import has a reason** the reader can be given now.
- **Deliberate failure teaches.** A cell that divides by zero, on a page
  about dividing by zero, beats a paragraph saying it would. The prose
  says it is meant to fail, so the reader does not think they broke it.
- **Names read as words**, not as the letters a textbook uses: `count`,
  `total`, `midpoint`, not `n`, `s`, `m`. `a`, `b`, `c` for a quadratic
  match the formula above the cell; `i`, `j` for an index and `x`, `y`
  for a coordinate need no defence.
- **Discover, then name, applies to variables.** Before the page has
  said *stationary distribution*, a variable called `state` is the
  honest name for what the reader has met.
- **Comments say why**, never what the code already says.
  `# average the two coordinates` above `midpoint = (x1 + x2) / 2` adds
  nothing.
- **A "your turn" stub** has nothing to name, and follows none of this.
- <a id="show-what-changed"></a>**Show only what changed.** When a cell
  needs code the reader has already seen, do not paste it again for them
  to read past. Put shared setup in one cell the page runs first, or in
  a shared include or toolkit cell, and let the new cell hold only the
  new lines. Where a whole class must be repeated to add one method,
  mark the new lines with a comment.
- **Every number is run.** A number in a page or an answer is executed
  before it is published, never reasoned about. A test checks code, not
  prose, so a wrong number in an answer is the one mistake nothing else
  catches.

<a id="terms"></a>
## Terms

Define every technical term where it first appears, in words the reader
already has, and once. (How a page marks a new term is mechanics:
`docs/WRITING_TUTORIALS.md#marking-a-term`.) Moving between mathematics
and programming makes some words ambiguous. These are settled:

| Use | Not | Because |
|---|---|---|
| **power**, **exponent**: $x^2$, $2^n$ | *index*, *indices* for exponents | *Index* is kept for a position in a list, `list[i]`, and for a summation bound. The syllabus says *laws of indices*; recognise it, and say power. |
| **mathematical function** $f(x) = x^2$, apart from **Python function** `def f(x):` | mixing the two silently | One is a mapping; the other is a subroutine that may have side effects, and may not be a mapping at all. |
| **spread** for data; **`range()`** for the Python function | "range" on its own | The statistical range and the loop's range are unrelated, and both appear on one page. |
| **set** $\{1, 2, 3\}$ | *list*, when order does not matter | That there are no repeats and no order is the point. |

<a id="checklist"></a>
## Before a page ships

One list. Each line points to its reason. The mechanical checks (ids,
frontmatter, the build) are in
[`docs/WRITING_TUTORIALS.md`](../docs/WRITING_TUTORIALS.md#before-you-open-a-pull-request).

- Does the page open by running or showing something, and asking about
  it? [discover, then name](#discover-then-name)
- Is there a moment to predict, and does the page wait?
  [predict](#predict-then-run)
- Does any line say right, wrong, correct, not yet, or show a tick?
  [no verdicts](#no-verdicts)
- Is every task a question, a challenge or an invitation?
  [invitations](#invitations)
- Does every sentence pass the plain-language checks, phrasal verbs
  included? [plain language](#plain-language)
- Does every sentence have somebody doing something, with no saying at
  the end of a paragraph and no main point after a colon?
  [say it directly](#say-it-directly)
- Is a feeling named only rarely, and with a route?
  [feelings](#feelings)
- Does every task have a first step anyone can take, and room above it?
  [low floor](#low-floor-high-ceiling)
- Does the practice page have problems from earlier pages?
  [nothing taught once](#nothing-taught-once)
- Is the world one a reader would choose, and is invented data called
  invented? [worlds](#choice-of-world)
- Is every term defined where it first appears? [terms](#terms)
- Is every number run, and every cell short? [code](#code)
- Is there somewhere real to read more? [page shapes](#page-shapes)
