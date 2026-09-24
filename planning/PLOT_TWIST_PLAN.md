# Plot Twist: a plan

*Maths and programming for people who are sure they hate both.*

A new track that teaches all of Programming and Design Principles (5N2927)
and all of Maths for Information Technology (5N18396) as one subject. It
sits beside "Programming and Maths, Integrated", which keeps its pages. None
of this track's pages is a copy of those; some link to them for readers who
want more.

**The name.** A *plot* is a graph, and a *plot twist* is the moment a story
turns out differently from what you expected. Both are the promise: you will
draw a lot of graphs, and this is not the maths or programming you remember.
Alternatives if it doesn't land: *Count Me In*, *Surprisingly Doable*. The
course id is `plot-twist` either way; the title can change later without
touching any page.

---

## 1. Why a second track

The existing integrated course covers every outcome of both modules (see
`planning/CURRICULUM_MAP.md`), but its shape works against the students it
most needs to keep:

- **It is two blocks.** Thirteen programming pages, then twenty-one maths
  pages. No programming page points forward to maths, and no maths page
  points out to databases, the web or computational methods.
- **Most maths is taught once and never used again.** Trigonometry, limits,
  derivatives, statistics, probability and Venn diagrams each get one page;
  the curriculum map's "used in" column is empty for almost all of them.
  The capstone draws on algebra alone.
- **Nothing carries over.** Every page is its own Python session, so the
  functions a student wrote last week are gone. Two cells in *Solving
  equations* failed for exactly that reason until the maths pass fixed them
  (DECISIONS_LOG 7.216).

A reader who arrives sure they are "not a maths person" or "not a computer
person" is the one this hurts most: a topic met once and never needed again
confirms that it was never for them.

## 2. Principles

1. **A question first, from the world.** Every page opens with something a
   person might want to know: *Is this password safe? Which queue should I
   join? Where do these two roads meet?* The maths and the code arrive
   because the question needs them.
2. **Each subject pays for the other.** A programming idea is introduced when
   a maths question needs it (a loop, to add up a hundred numbers), and a maths
   idea when a program needs it (a logarithm, to say why binary search is
   fast). No page is "the maths page" or "the programming page".
3. **Picture, then numbers, then symbols.** A graph or a count comes before
   the formula. The formula is said in words, then written, then checked by
   running it.
4. **Predict, run, explain.** Before any cell that shows something new, the
   reader guesses. Being wrong is expected and useful, and the page says so.
5. **Errors are information.** Reading an error message is taught in the
   first unit, and every later unit has a "fix the broken code" problem.
6. **Nothing is taught once.** Every page starts with two short warm-up
   questions from earlier units, and every unit ends with a mixed practice
   page drawing on everything so far.
7. **The toolkit.** Readers build one module of their own, `toolkit.py`,
   across the whole track: `mean`, `distance`, `solve_quadratic`,
   `derivative_at` and about thirty more, each with its own tests. Later
   units call the functions earlier units built. The capstone is "use your
   toolkit". See §5 for how this works in the browser.
8. **Low floor, high ceiling.** The first task on a page is one every reader
   can finish. The last is one a confident reader will enjoy.

## 3. Practice

Every tutorial has a practice page, and every unit a mixed practice page.
Problems come in four kinds and three levels:

| Kind | What the reader does |
|---|---|
| Predict | Say what a cell will print, then run it |
| Make | Write a small function or calculation to a clear target |
| Fix | Find and repair one realistic mistake in working-looking code |
| Explain | Answer in words: why does this work, when would it fail |

Levels: **Warm-up** (one step, anyone can do it), **Core** (what the page
teaches), **Stretch** (combines it with an earlier unit). Every problem has
an answer fold and, where it helps, a hint fold.

**Diverse contexts.** Each unit rotates through settings so no reader meets
only one kind of example: music and playlists, sport, cooking and recipes,
money and rent, travel and maps, health and fitness, games, weather and
climate, Irish data (rainfall, bus times, the census), art and colour. A
context is chosen because the maths genuinely fits it, never as decoration.

## 4. The units

Forty-seven tutorials of roughly an hour each, in ten units. Outcome codes are
from `planning/curriculum/outcomes.yaml`. Every PDP and MIT outcome appears
at least once (checked by a script: see §7).

### Unit 1 — Instructions for a machine

*A computer does exactly what it is told. So what do we tell it, and what
can it hold?*

| # | Tutorial | Question it opens with | Outcomes |
|---|---|---|---|
| 1.1 | Recipes are algorithms | How would you teach a robot to make tea? | PDP-LO2, PDP-LO5, PDP-LO6, MIT-6.1 |
| 1.2 | Numbers a computer can hold | Why does Python say `7 / 2` is `3.5` but `7 // 2` is `3`? | PDP-LO4, MIT-1.1 |
| 1.3 | Everything is ones and zeros | How does `#FF8800` make orange? | MIT-1.4 |
| 1.4 | When Python says no | What is an error message trying to tell you? | PDP-LO9 |

Unit product: a tip calculator that splits a restaurant bill. Toolkit starts
with `to_binary`, `to_hex`.

### Unit 2 — Decisions and the logic under them

*Every "if" in a program is a small piece of logic. What rules does logic
follow?*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 2.1 | Choosing a path | How does a ticket machine know you get the student price? | PDP-LO4, PDP-LO6, MIT-1.11 |
| 2.2 | True, false and every case in between | Can we list every way a condition can come out? | MIT-2.4 |
| 2.3 | Untangling a condition | Why does `not (a and b)` mean the same as `not a or not b`? | MIT-2.5 |
| 2.4 | Bits that flip | How can one bit catch a mistake in a message? | MIT-2.4, MIT-1.4 |

Unit product: a quiz that marks answers and explains why. Toolkit gains
`truth_table`.

### Unit 3 — Again and again: loops, counting and chance

*Computers are good at doing one thing many times. So are they good at
counting, and at chance?*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 3.1 | Doing it again | How much does a daily coffee cost over a year? | PDP-LO6, MIT-6.4 |
| 3.2 | Counting every outfit | How many different outfits are in your wardrobe? | MIT-5.1, MIT-5.2 |
| 3.3 | Orders and choices | How many ways can a five-a-side team be picked? | MIT-5.3, MIT-5.4, MIT-5.5 |
| 3.4 | How likely is it? | Is a coin that lands heads 7 times in 10 unfair? | MIT-5.6, MIT-5.7 |
| 3.5 | Chances that combine | How likely is it that two people in the class share a birthday? | MIT-5.8 |

Sigma and pi notation arrive as "a loop, written by mathematicians" (3.1).
Every counting formula is checked against a loop that lists every case.
Unit product: a password-strength checker. Toolkit gains `factorial`,
`combinations`, `simulate`.

### Unit 4 — Making your own tools

*A formula is a small machine: numbers in, a number out. So is a function.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 4.1 | Machines that take a number | What does it mean for a function to have an input and an output? | PDP-LO8, MIT-3.1, MIT-6.2 |
| 4.2 | Measuring rooms and tins | How much paint does a room need? | MIT-1.2, MIT-1.3 |
| 4.3 | Running a formula backwards | If a trip took 3 hours at 80 km/h, how far was it? And how fast, if it was 200 km? | MIT-1.7, MIT-3.1 |
| 4.4 | Does it work? Testing your tools | How do you know your function is right? | PDP-LO10, PDP-LO11 |
| 4.5 | What a function can see | Why can't the function see my variable? | PDP-LO8 |

4.4 starts `toolkit.py` properly: every function in it gets `assert` tests,
and the reader learns walkthroughs (tracing a function by hand) and the
debugger's step-through. Unit product: a unit converter with tested
conversions both ways.

### Unit 5 — Many values: lists, sets and data

*One number is a fact. A list of numbers is a story. How do we read it?*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 5.1 | A row of numbers | How do we keep a week of temperatures? | MIT-6.3, MIT-6.5, MIT-6.7 |
| 5.2 | What is typical? | Is the average rent in your area the rent most people pay? | MIT-5.12, MIT-5.13 |
| 5.3 | Kinds of data, and honest charts | Why is this chart misleading? | MIT-5.9, MIT-5.10, MIT-5.11 |
| 5.4 | Collections without repeats | Which songs are on both playlists? | MIT-2.1, MIT-2.2 |
| 5.5 | Circles that overlap | How many people answered yes to two questions out of three? | MIT-2.3 |

Real data throughout (Met Éireann rainfall, rent, bus punctuality). 5.4 ends
with the link to SQL: a JOIN is an intersection, a CROSS JOIN is the
Cartesian product. Unit product: a one-page report on a dataset of the
reader's choosing. Toolkit gains `mean`, `median`, `mode`, `std_dev`,
`frequency_table`.

### Unit 6 — Algorithms that scale

*Finding a name in 10 names is easy. In 10 million? The maths of "how many
steps" decides.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 6.1 | Finding things fast | How does a phone find one contact in thousands? | MIT-6.6, MIT-6.8, MIT-1.1 |
| 6.2 | Putting things in order | How would you sort a hand of cards, and how many moves does it take? | MIT-6.8 |
| 6.3 | Racing the sorts | Which sort wins on 1,000 numbers, and why? | MIT-6.8, PDP-LO2 |
| 6.4 | A function that calls itself | How many files are in this folder, counting every folder inside it? | MIT-6.8, PDP-LO8 |
| 6.5 | Doubling and halving | Why does a rumour spread so fast, and why is binary search so quick? | MIT-1.1 |

Logarithms arrive as "how many halvings" (6.1) and powers as "how many
doublings" (6.5), the same idea from both ends. Step counts are plotted, so
growth rates are seen before they are named. Shell sort is in 6.3.

### Unit 7 — Algebra you can run

*Algebra is a way of writing rules. A program is a way of running them.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 7.1 | Rules with letters in them | What is the difference between a rule and a question? | MIT-1.5, MIT-1.6, MIT-1.8 |
| 7.2 | Drawing a rule | What does `y = x² − 4` look like, and where does it cross zero? | MIT-3.2 |
| 7.3 | Solving for x | When will two phone plans cost the same? | MIT-1.9 |
| 7.4 | When there is no real answer | What does Python mean by `2j`? | MIT-1.10 |
| 7.5 | The top of the curve | What price gives a shop the most profit? | MIT-3.4 |
| 7.6 | Several unknowns at once | How many adult and child tickets were sold? | MIT-1.12 |

Polynomials are lists of coefficients, so expanding brackets is a loop. Every
algebraic answer is checked by substituting it back in code. Toolkit gains
`evaluate`, `solve_linear`, `solve_quadratic`, `solve_simultaneous`.

### Unit 8 — Shapes, angles and waves

*Games, maps and music are all geometry underneath.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 8.1 | Straight lines | Is this wheelchair ramp too steep? | MIT-4.1, MIT-4.2 |
| 8.2 | How far apart? | Did the ball hit the player? (collision detection) | MIT-4.3, MIT-4.4 |
| 8.3 | Going round in circles | How does a clock app draw the hands? | MIT-4.5, MIT-4.6, MIT-4.7 |
| 8.4 | Waves | What makes one note higher than another? | MIT-3.3, MIT-4.6 |
| 8.5 | Solving triangles | How tall is that tree, from where you stand? | MIT-4.8, MIT-4.9, MIT-4.10 |

8.3 links out to the CSS orbit and cube pages in Web Authoring, which use the
same sine and cosine. Toolkit gains `distance`, `midpoint`, `slope`,
`angle_between`.

### Unit 9 — Change

*How fast is it changing, right now? Every speedometer and every machine
learning model asks this.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 9.1 | Getting closer | What happens to a value as you zoom in on it? | MIT-3.5 |
| 9.2 | How fast, right now | What was the runner's speed at the 3-minute mark? | MIT-3.6 |
| 9.3 | Rules for change | Is there a shortcut for the slope of any curve? | MIT-3.7 |
| 9.4 | Solving by computing | How does a calculator find √2 when there is no formula for it? | MIT-3.6, MIT-6.6 |

9.3 teaches all four rules, the quotient rule included; the existing course
narrows it out. 9.4 is bisection and Newton's method: limits, derivatives,
divide and conquer and binary search in one algorithm. Toolkit gains
`derivative_at`, `bisect`, `newton`.

### Unit 10 — Programs for people

*Code is read far more often than it is written, mostly by other people.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 10.1 | Where programming came from | What did Ada Lovelace's program do, and what would it look like today? | PDP-LO1, PDP-LO3 |
| 10.2 | Many languages, one idea | The same task in Python, JavaScript, SQL and BASIC | PDP-LO3 |
| 10.3 | Code other people can read | Would a stranger understand your toolkit? | PDP-LO7, PDP-LO11 |
| 10.4 | The team project | Design, build, release and review a program together | PDP-LO12, PDP-LO7, PDP-LO10 |

The team project asks teams of three to five to build something that uses
their toolkits and at least four units: a fitness tracker with statistics and
charts, a small game with collision and probability, a trip planner with
distances and bearings. It replaces a separate capstone page.

### Context pages

Background reading, linked from the pages that need it:

- **How a computer stores a number.** Why `0.1 + 0.2` is not `0.3`, why
  answers end in `e-16`, and why `sqrt(2)/2` squared misses ½. Linked from
  1.2, 1.3, 7.4, 8.3, 9.1 and every other page where a float surprises.
- **Sets in databases.** How union, intersection and the Cartesian product
  become SQL. Linked from 5.4 and 5.5, and into Database Methods.
- **Maths that runs the world.** Short, true stories: Monty Hall, GPS
  trilateration, why Google ranks pages with a Markov chain. Linked from
  whichever unit each belongs to.

## 5. The toolkit in the browser

Every page is its own Python session, so a reader's functions do not carry
over today. Two ways to make them carry over, and which I recommend:

1. **A toolkit cell (recommended).** A cell marked `toolkit: true` on a
   page. Whatever the reader saved in it (already kept in `localStorage`,
   under the tutorial id and cell id) is loaded into every later page of the
   track before its first cell runs. If the reader never wrote it, a
   reference version loads instead, so no page breaks for someone who
   skipped ahead. This is one runtime feature in `tutorial-runtime.js`, with
   tests, and it is the reason the toolkit can be the reader's own work.
2. **Author-supplied only.** Each page includes the reference toolkit through
   `setup/` (`{{include: ...}}`), which works today. Readers still write the
   functions, but later pages use the author's versions. Simpler, and it
   loses the point.

Option 1 costs about a day of runtime work and is worth it. Option 2 is the
fallback if it proves fragile.

## 6. How it gets built

1. **Pilot: Units 1 and 2.** Eight tutorials, eight practice pages, one mixed
   practice page and glossaries, plus the toolkit cell. Built, checked in a
   browser, and read by you before anything else is written, so the voice,
   the warm-ups and the practice format are agreed on real pages.
2. **Units 3–9 in parallel**, one agent per unit, each from a brief written
   from the agreed pilot, with the same checks as every other pass: every
   cell run, every answer run, `check.py`, the build.
3. **Unit 10 and the context pages last**, since they draw on everything.
4. **The course file** `courses/plot-twist.yaml`, a topic-tree group, and a
   decisions-log entry. The course starts as `status: beta`.

## 7. Coverage check

Every outcome code in the tables above, against the full lists:

- **PDP (5N2927):** LO1–LO12, all present.
- **MIT (5N18396):** 1.1–1.12, 2.1–2.5, 3.1–3.7, 4.1–4.10, 5.1–5.13,
  6.1–6.8: all 55 present, and MIT-3.7 in full, where the existing course
  narrows it.

When the course file exists, `dev/curriculum_map.py` checks the same thing
from the pages' own `covers:` frontmatter, so the claim above cannot drift.

## 8. Decisions for Josh

1. **The name.** *Plot Twist*, or one of the alternatives.
2. **The toolkit cell** (§5, option 1): yes or no.
3. **Where it sits.** Beside the existing integrated course as a beta track,
   or as the recommended starting point on the contents page once it is
   finished.
