# The Dewey Track: a plan

*Python and maths for people who want something different. Learn by dewing.*

A new track that teaches all of Programming and Design Principles (5N2927)
and all of Maths for Information Technology (5N18396) as one subject. It
sits beside "Programming and Maths, Integrated", which keeps its pages. None
of this track's pages is a copy of those; some link to them for readers who
want more.

**The name.** The track is named after John Dewey, who argued that people
learn by doing: by working on real questions rather than memorising answers
first. Its tagline, "learn by dewing", is his idea with the site's name in
it. It was called *Plot Twist* while its first units were written; Josh
renamed it (DECISIONS_LOG 7.226), and the course id moved from `plot-twist`
to `dewey-track`, with a redirect from the old address.

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

## 2. Four ideas under everything

Josh's framing, and the spine of the track. Maths and programming rest on
the same few ideas, and a reader who can ask four questions of any
situation can reason in either:

| Idea | The question a reader asks | In programming | In maths |
|---|---|---|---|
| **Naming** | What is named here, and what does the name point at? | variables, references; two names for one list; renaming changes nothing, repointing changes everything | letters for numbers; substitution; "let *u* stand for…"; a value used as a name (an index, a key) |
| **Functions** | What is promised, given what? | a function as a named promise: inputs in, a result that keeps the promise out; small promises composed into big ones; tests that check the promise | a formula; a rule; an inverse that undoes the promise |
| **Sequence** | What happens when, and after what? | order of lines; repeating; choosing a path ("control flow" is said once and not leaned on) | order of operations; the steps of rearranging; a proof's lines; a limit's approach |
| **Environment** | What does this space let us do, and what does it assume? | what comes free (`print`, making a new name); what a function can see; ints that never overflow and floats that round | the number families, each a bigger space with moves the last one forbade; a flat plane where a triangle's angles make 180°, and a sphere where three right angles make 270° |

Students meet these as the four questions, not as vocabulary to learn. The
fourth matters most to readers who have been told they are bad at maths: a
move that "doesn't work" is usually a move from a different space, and
naming the space turns the mistake into a discovery. School maths tends to
penalise the move; this track asks which space it belongs to.

How the track carries them:

- **A first page, "Four questions"**, asks them of a board game (pieces are
  names, moves are functions, turns are sequence, the board and its rules
  are the environment), then of a recipe, then of one line of Python.
- **"The space we're in"**, a short box near the top of every page, says
  out loud the assumptions and the moves allowed: "whole numbers only",
  "a flat plane", "Python gives you `print` without asking".
- **Each unit leans on one idea**, and uses all four: naming in Units 1
  and 5, functions in 4 and 7, sequence in 3 and 6, environment in 2, 8
  and 9. Unit 7's complex numbers are "building a bigger space"; Unit 8
  puts triangles on a sphere beside the 180° rule.

## 3. Principles

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
7. **The toolkit.** Readers build one module of their own, toolkit.py,
   across the whole track: `mean`, `distance`, `solve_quadratic`,
   `derivative_at` and about thirty more, each with a comparison against a
   solution. Later
   units call the functions earlier units built. The capstone is "use your
   toolkit". See §6 for how this works in the browser.
8. **Never measure the reader.** A page never says how easy or obvious
   something is: not "simply", "obviously", "clearly", "of course",
   "trivially", "easy", "as you can see" or "it's straightforward". A reader
   who expects to fail reads those as proof. Every other word is allowed
   when it means something: "the cell you just ran", "Python actually
   prints 0.30000000000000004".
9. **Low floor, high ceiling.** The first task on a page is one every reader
   can finish. The last is one a confident reader will enjoy.
10. **Show the choices.** The reader sees why the course is built as it
    is, what the usual alternative is, and what each costs, so they can
    judge the approach and say when it is not working for them. Three
    layers, each small:
    - **A page on how this course is built**, beside *Four questions* at
      the start: the usual shape of a course like this and what it does to
      a reader who expects to fail, what this track does instead, what that
      costs (slower in places; some things arrive later than a textbook
      puts them), and an invitation to say when it is not working. Written
      as a letter from the people who made it, not a mission statement.
    - **"Why this way?"** on every tutorial: a closed fold near the end
      that names one choice the page made and the alternative it turned
      down, in a few sentences. One choice per page, so the explaining
      never becomes the lesson.
    - **The reader as judge**, where it fits: an Explain problem in the
      practice asking which way the reader would have taught something,
      and why.

## 4. Practice

Every tutorial has a practice page, and every unit a mixed practice page.
Problems come in four kinds and three levels:

| Kind | What the reader does |
|---|---|
| Predict | Say what a cell will print, then run it |
| Make | Write a small function or calculation to a clear target |
| Fix | Find and repair one realistic mistake in working-looking code |
| Explain | Answer in words: why does this work, when would it fail |
| Another way | Reach the same answer by a second route, or find the space where a "wrong" answer is right |

Levels: **Warm-up** (one step, anyone can do it), **Core** (what the page
teaches), **Stretch** (combines it with an earlier unit). Every problem has
an answer fold and, where it helps, a hint fold.

**Contexts: computing first.** A context is chosen because the maths
fits it, never as decoration. Computing comes first: pixels, screens,
files, packets, sensors, fonts, games. Physics comes in where the maths
*is* physics: falling, bouncing, orbits, waves, light. Real Irish data
stays wherever it exists (rainfall, emissions, the census). A made-up
everyday setting (a café bill, a runner, a cupcake stall) is the last
choice, and needs a reason. Two warnings from the audit: a reader's
English may be a second language, so a science setting gets its terms
explained on the page; and a reader who fears maths should not be handed
a fear of physics instead, so the physics is always the kind you can see
(a ball, a raindrop, a ray of light).

**Schlomo and Schlomi.** The track borrows Schlomo from Josh's 2017
handouts, where he has a plausible idea that turns out not to work
(shifting a cipher twice to make it "more secure"). Here he has a sister
or friend, Schlomi. Fix and Explain problems give their ideas to one of
them, so the reader tests somebody else's reasoning before their own:
"Schlomo says 0.1 + 0.2 should print 0.3. Is he wrong?" Rules:

- Their ideas are *reasonable*. Each is the idea a thoughtful reader
  might have. Neither of them is ever the butt of the joke.
- Neither is always right. Sometimes Schlomo is right and Schlomi is
  wrong, and sometimes both are right in different spaces (the fourth
  idea, §2).
- One or two appearances per practice page, not every problem.
- They make mistakes; the reader never gets called one.

**Choose your project.** Where one idea has several good uses, the page
offers two to four short projects and the reader picks one: "choose one
of these, or do more than one if you like". Each project is complete on
its own, is a few cells long, and ends with its own check. The first
use is Unit 9, where the derivative finds the bottom of a letter's curve,
the edge of a shape in an image, the best line through data, or the
lowest point of a cost by walking downhill (gradient descent). A mixed
page may offer a choice of products in the same way.

## 5. The units

Forty-nine tutorials of roughly an hour each, in ten units, with nine mixed
pages and the letter *How this course is built*. Outcome codes are
from `planning/curriculum/outcomes.yaml`. Every PDP and MIT outcome appears
at least once (checked by a script: see §8).

### Unit 1 — Instructions for a machine

*A computer does exactly what it is told. So what do we tell it, and what
can it hold?*

| # | Tutorial | Question it opens with | Outcomes |
|---|---|---|---|
| 1.0 | Four questions | What do a board game, a recipe and a line of Python have in common? | PDP-LO5, MIT-6.1 |
| 1.1 | Recipes are algorithms | How would you teach a robot to make tea? | PDP-LO2, PDP-LO5, PDP-LO6, MIT-6.1 |
| 1.2 | Numbers a computer can hold | A microwave clock keeps one number: how does it take it apart into digits, and why does Python give three answers to 7 ÷ 2? | PDP-LO4, MIT-1.1 |
| 1.3 | Everything is ones and zeros | Can you see the 8 in `0x6996996`? And how does `#FF8800` make orange? | MIT-1.4 |
| 1.4 | When Python says no | What is an error message trying to tell you? | PDP-LO9 |

Unit product: a digit display, in two stages, built on the mixed page.
Stage 1 is a seven-segment display drawn in text: `//` and `%` take a
number apart, $2^7 = 128$ counts the segment patterns, and each digit's
pattern is a byte. Stage 2 is a pixel font 4 pixels wide and 7 tall,
where each row is one hex digit and a digit is seven. The digit display
runs through the unit: pixels and segments in 1.2, bits and glyphs in
1.3, errors in display code in 1.4. Toolkit starts with `digit_at`
(1.2), then `to_binary`, `to_hex` and `pixel_row` (1.3).

### Unit 2 — Decisions and the logic under them

*Every "if" in a program is a small piece of logic. What rules does logic
follow?*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 2.1 | Choosing a path | How does a phone decide when to slow its processor down? | PDP-LO4, PDP-LO6, MIT-1.11 |
| 2.2 | True, false and every case | Can we list every way a condition can come out? | MIT-2.4 |
| 2.3 | Untangling a condition | Why does `not (a and b)` mean the same as `not a or not b`? | MIT-2.5 |
| 2.4 | Bits that flip | How can one bit catch a mistake in a message? | MIT-2.4, MIT-1.4 |

Contexts: a phone's temperature rules, a drone's battery and a laptop's
fan speeds (2.1); an app's unlock and login rules, and which segments of
a seven-segment display light for the digits 0 to 7 (2.2); a delivery
app's Order button and a drone that stays grounded in rain or wind (2.3);
an Irish weather buoy's radio message and its parity bit (2.4). Unit
product: a quiz that marks binary answers and explains why. Toolkit gains
`between`, `truth_table`, `same_rule` and `parity_bit`.

### Unit 3 — Again and again: loops, counting and chance

*Computers are good at doing one thing many times. So are they good at
counting, and at chance?*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 3.1 | Doing it again | A ball keeps 80% of its height at each bounce. When does it stop, and how far does it travel? | PDP-LO6, MIT-6.4 |
| 3.2 | Counting every outfit | How many outfits are in your wardrobe, and how many colours can one pixel show? | MIT-5.1, MIT-5.2 |
| 3.3 | Orders and choices | Eight drones, five chargers: how many flight teams, and how many if each drone has a job? | MIT-5.3, MIT-5.4, MIT-5.5 |
| 3.4 | How likely is it? | Is a coin that lands heads 7 times in 10 unfair? | MIT-5.6, MIT-5.7 |
| 3.5 | Chances that combine | How likely is it that two people in the class share a birthday, and two files a hash code? | MIT-5.8 |

A bouncing ball runs through 3.1: a `for` loop over the bounces, a
running total of the distance, sigma for a geometric series (endless
bounces that add up to 9 metres), pi for the height kept after $n$
bounces, and `while` until a bounce is under 1 cm, with an animation
the reader steers by editing `keep`. Sigma and pi notation arrive as "a
loop, written by mathematicians". Every counting formula is checked
against a loop that lists every case, and 3.2 and 3.3 count pixels,
colours, PINs, passwords and the 128 seven-segment patterns from Unit 1.
3.4 simulates rain on a 10 × 10 grid as well as the coin, with an
animation of the grid. Unit product: a password-strength checker.
Toolkit gains `total`, `product`, `all_pairs`, `factorial`,
`permutations`, `combinations`, `simulate` and `at_least_one`.

### Unit 4 — Making your own tools

*A formula is a small machine: numbers in, a number out. So is a function.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 4.1 | Machines that take a number | A temperature chip gives out a voltage, and a rule turns it into °C. Why does the rule say −350 °C for a voltage the chip never gives? | PDP-LO8, MIT-3.1, MIT-6.2 |
| 4.2 | Measuring rooms and tins | How much paint does a room need, how long is the track on a CD, and how many Moons would fill the Earth? | MIT-1.2, MIT-1.3 |
| 4.3 | Running a formula backwards | Sunlight takes 8 minutes 19 seconds to reach us: how far is the Sun? How fast is the space station, and how long does a message to Mars take? | MIT-1.7, MIT-3.1 |
| 4.4 | Does it work? Testing your tools | A spacecraft was lost at Mars because of a unit mix-up that raised no error. How do you know your function is right? | PDP-LO10, PDP-LO11 |
| 4.5 | What a function can see | Why can't the function see my variable? | PDP-LO8 |

Contexts: a TMP36 temperature chip, a 10-bit board reading and the
order of two drawing moves (4.1); the paint job, a CD's 5.4 km track, a
3D-printed ball and cone, and the Earth and the Moon (4.2); light from
the Sun, the space station, a message to Mars, Mars in Fahrenheit, the
James Webb telescope's mirror and a drone into the wind (4.3); the Mars
Climate Orbiter, a boiling-point bug, Irish January nights and the size
of an image (4.4); a download's speed, a packet counter, a ball dropped
on Earth and on the Moon, a sensor log and a unit-factor closure (4.5).
No page uses money. 4.4 starts toolkit.py properly: the reader learns
`assert` tests, walkthroughs (tracing a function by hand) and the
debugger's step-through. Outside 4.4, a page never writes tests against
the reader's functions; each toolkit function comes with a comparison
against a solution instead (7.268). Unit product (on
`mixed-making-your-own-tools`): a converter for reading about space,
km and miles, kg and pounds, °C and °F, with astronomical units and
a 1 TB drive in GiB on the way, every conversion checked both ways.
Toolkit gains `compose`, the shape tools, `speed`, `travel_time`,
`distance_travelled`, `celsius_to_fahrenheit`, `fahrenheit_to_celsius`
and `close_enough`.

### Unit 5 — Many values: lists, sets and data

*One number is a fact. A list of numbers is a story. How do we read it?*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 5.1 | A row of numbers | How do we keep a week of temperatures? | MIT-6.3, MIT-6.5, MIT-6.7 |
| 5.2 | What is typical? | A website's average response time is 639 ms, but most pages load in 200 ms. Is the average lying? | MIT-5.12, MIT-5.13 |
| 5.3 | Kinds of data, and honest charts | Why is this chart misleading, when every number on it is true? | MIT-5.9, MIT-5.10, MIT-5.11 |
| 5.4 | Collections without repeats | Which songs are on both playlists, and how many words do two novels share? | MIT-2.1, MIT-2.2 |
| 5.5 | Circles that overlap | How many of 20 laptops have exactly two of updates, antivirus and backups? | MIT-2.3 |

Contexts: a week of temperatures, sound as a list of samples (mixing
two notes is adding element by element), and 67 years of Ireland's life
expectancy (5.1); skewed website response times, where the median beats
the mean, ping times and jitter for spread, and life expectancy in 226
places (5.2); a made-up advert's misleading bar chart of real life
expectancy data, and a class survey (5.3); playlists, the words of *The
Lost World* and *The War of the Worlds* from the data folder, and the
power set of a pixel's red, green and blue lights, which gives the eight
Teletext colours (5.4); a laptop security audit, and an audit report
that gives only totals (5.5). Real data comes from the `data/` folder:
Our World in Data's life expectancy series and two Project Gutenberg
novels; small made-up lists say so. 5.4 ends with the link to SQL: a
JOIN is an intersection, a CROSS JOIN is the Cartesian product. Unit
product (on `mixed-many-values`): a one-page report on life expectancy
in Ireland and a country the reader chooses, with typical values,
spread, a frequency table and one honest chart. Toolkit gains
`largest`, `smallest`, `count_if`, `mean`, `median`, `mode`, `std_dev`,
`frequency_table`.

### Unit 6 — Algorithms that scale

*Finding a name in 10 names is quick. In 10 million? The maths of "how
many steps" decides.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 6.1 | Finding things fast | How does a computer find one planet in NASA's list of over six thousand, in about a dozen looks? | MIT-6.6, MIT-6.8, MIT-1.1 |
| 6.2 | Sorting a hand of cards | How would you sort a hand of cards, and how many moves does it take? | MIT-6.8 |
| 6.3 | Racing the sorts | Which sort wins on 1,000 numbers, and which can we wait for on six thousand planets? | MIT-6.8, PDP-LO2 |
| 6.4 | A function that calls itself | How many files are in this folder, counting every folder inside it? | MIT-6.8, PDP-LO8 |
| 6.5 | Doubling and halving | Why does a rumour, or a computer worm, spread so fast, and why is binary search so quick? | MIT-1.1 |

Logarithms arrive as "how many halvings" (6.1) and powers as "how many
doublings" (6.5), the same idea from both ends. Step counts are plotted, so
growth rates are seen before they are named. Shell sort is in 6.3.

Contexts: eight phone contacts for tracing, then NASA's Exoplanet Archive
(`data/exoplanets.csv`, a snapshot of 25 September 2026, 6,372 planets),
binary-searched for Proxima Cen b (6.1); a hand of cards, and in the
practice the nearest known planets, file names and a weather buoy's
batteries (6.2); random lists, Ireland's life expectancy as a nearly
sorted list, and the orbits of 6,019 planets, where the formula says
which sorts are worth waiting for (6.3); a folder of photos, a website's
menus, zip files inside zip files and a recursive fractal tree (6.4); a
rumour and the Slammer worm, the chessboard, Moore's law from the Intel
4004 to the Apple M1, Ireland's CO₂ emissions and, in the practice, the
list of known planets doubling since 1995 (6.5). No page uses money.
Unit product (on `mixed-algorithms-that-scale`): a phone-book search
that stays fast, the same lookup done three ways on 10, 1,000 and
100,000 names, with the step counts and a sentence on why. Toolkit
gains `linear_search`, `binary_search`, `selection_sort`,
`insertion_sort`, `shell_sort`, `count_items` and `halvings`.

### Unit 7 — Algebra you can run

*Algebra is a way of writing rules. A program is a way of running them.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 7.1 | Rules with letters in them | How many rows of photos fit on a gallery page, and what is the difference between a rule and a question? | MIT-1.5, MIT-1.6, MIT-1.8 |
| 7.2 | Drawing a rule | What does `y = x² − 4` look like, and where does it cross zero? | MIT-3.2 |
| 7.3 | Solving for x | When are two servers equally fast, and when does a volleyed ball land? | MIT-1.9 |
| 7.4 | When there is no real answer | What does Python mean by `2j`? | MIT-1.10 |
| 7.5 | The top of the curve | Why does a round letter dip below the line, and how far? (typographic overshoot) | MIT-3.4 |
| 7.6 | Several unknowns at once | A server sent 230 requests and 2,060 KB: how many were images? | MIT-1.12 |

Polynomials are lists of coefficients, so expanding brackets is a loop. Every
algebraic answer is checked by substituting it back in code.

Contexts: a photo gallery's page height ($50n + 30$), a photo with a
strip and a caption bar, and the three weights $(1 - t)^2$, $2t(1 - t)$,
$t^2$ of a curve on a screen, expanded by the loop and adding up to 1
(7.1, with a de Casteljau animation of 7.5's letter bowl on its practice
page); a kicked ball's height against time, animated beside its graph,
three servers whose answer times cross, and a game's frame time,
$\frac{1000}{x}$ (7.2); the same servers solved exactly, a game's
sprite sheet, a volleyed ball's landing time from the quadratic formula,
and a stone dropped down a well on the practice page (7.3); a ship
turned by multiplying by `1j`, the history of "imaginary", and
alternating current as where engineers meet these numbers (7.4); a
server log of image and text requests, a game's coins and gems, backup
logs of photos, songs and clips, and on the practice page 7.5's letter
bowl found again from three of its pixels (7.6). No page uses money.
Unit product (on `mixed-algebra-you-can-run`): a server chooser (where
two servers are equally fast, the fastest for a crowd, an old server's
rule from two measurements) and a free-kick checker (the top of the
flight, whether it clears the wall, and why 5 m has only complex
roots), with a detour to Kepler's third law, $T^2 = a^3$, on NASA's
numbers for the eight planets (`data/planet-orbits.csv`). Toolkit gains
`evaluate`, `plot_rule`, `solve_linear`, `solve_quadratic`, `vertex`
and `solve_simultaneous`.

### Unit 8 — Shapes, angles and waves

*Games, maps and music are all geometry underneath.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 8.1 | Straight lines | Is this wheelchair ramp too steep? | MIT-4.1, MIT-4.2 |
| 8.2 | How far apart? | Did the ball hit the player? (collision detection) | MIT-4.3, MIT-4.4 |
| 8.3 | Going round in circles | How does a clock app draw the hands, and where are the planets? | MIT-4.5, MIT-4.6, MIT-4.7 |
| 8.4 | Waves | What makes one note higher than another? | MIT-3.3, MIT-4.6 |
| 8.5 | Solving triangles | How tall is that tree, from where you stand? | MIT-4.8, MIT-4.9, MIT-4.10 |

Contexts: a community hall's ramp checked against Ireland's Technical
Guidance Document M, then Unit 7's server A ($y = 2x + 8$) and the TMP36
temperature chip as lines $y = mx + c$ (8.1); a 2D game's ball and
player as circles, an animation where a fast ball tunnels through the
player, and a camera pointed at the midpoint of two players (8.2); a
clock app's hands, then the four inner planets animated on
`point_on_circle` from NASA's numbers (`data/planet-orbits.csv`), and a
triangle of three right angles on a ball (8.3); a guitar's strings, a
point going round animated into a sine wave, Irish mains electricity
(230 V, 50 Hz, a peak of about 325 V) as alternating current, piano
octaves and noise-cancelling (8.4); a beech tree, the Spire, bearings
in Wicklow, a triangle of phone masts, and Snell's law for light
entering water, with a ray diagram the reader turns past the critical
angle into total internal reflection, the way optical fibres carry data
(8.5). Practice pages give Fix and Explain problems to Schlomo and
Schlomi. No page uses money. 8.3 links out to the CSS orbit and cube
pages in Web Authoring, which use the same sine and cosine. Toolkit
gains `slope`, `line_through`, `distance`, `midpoint`,
`point_on_circle`, `wave` and `angle_between`.

Unit product (on `mixed-shapes-angles-and-waves`): a collision checker
for a 2D game (circles that touch, a slanted wall and its nearest
point, a bearing and distance to the goal), which then runs a small
real-time game in a full-stack app cell. A Python cell sets the level
and works out the ball's path with the reader's tools, saving it to the
page's `db`; a JavaScript engine plays it on a canvas with the arrow
keys or on-screen buttons. Unit 10's team project starts its game from
it.

### Unit 9 — Change

*How fast is it changing, right now? Every weather radar and every machine
learning model asks this.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 9.1 | Getting closer | Walking halfway to a door again and again, do you ever arrive? | MIT-3.5 |
| 9.2 | How fast, right now | How fast is a falling hailstone going 3 seconds after it starts? | MIT-3.6 |
| 9.3 | Rules for change | Is there a shortcut for the slope of any curve? | MIT-3.7 |
| 9.4 | Solving by computing | How does a calculator find √2 when there is no formula for it? | MIT-3.6, MIT-6.6 |
| 9.5 | Putting the derivative to work: choose a project | What is the derivative for? | touches MIT-3.4, 3.6, 3.7 |

9.1's one-sided limits are the sharp edge of a shape on a screen, which
9.5's edge-finding project comes back to. 9.2's hailstone falls in the
simplest air-resistance model (drag proportional to speed, said to be a
model), and a Doppler weather radar is the instrument that reads a speed
at an instant. 9.3 teaches all four rules, the quotient rule included; the
existing course narrows it out, and it finds 7.5's letter bottom again by
setting the slope to 0. 9.4 is bisection and Newton's method: limits,
derivatives, divide and conquer and binary search in one algorithm.
Toolkit gains `derivative_at`, `bisect_root`, `newton`.

9.5 is the first "choose your project" page (§4): after a short shared
opening (a slope of 0 marks a turn, a large slope marks fast change) the
reader picks one or more of four self-contained projects, each ending in
its own `check()`: the bottom of a letter drawn with a cubic Bézier curve,
an edge in a row of pixels and in a small picture, the least-squares line
through Ireland's life expectancy, and gradient descent. It has no practice
page: each project is its own practice, and the mixed page follows.

Unit product (on `mixed-change`): a best-moment finder, `best_point`, that
finds a rule's top or bottom (the letter's bowl first) and the moment it
changes fastest, then does the same for Ireland's CO₂ emissions.

### Unit 10 — Programs for people

*Code is read far more often than it is written, mostly by other people.*

| # | Tutorial | Question | Outcomes |
|---|---|---|---|
| 10.1 | Where programming came from | The first program was published in 1843, a century before a computer could run it, and it had a bug. What did it do? | PDP-LO1, PDP-LO3 |
| 10.2 | Many languages, one idea | Can you read four languages you have never written? One week of rain in Python, SQL, JavaScript and BASIC | PDP-LO3 |
| 10.3 | Code other people can read | Would a stranger understand your toolkit? (The stranger is usually you, six months later.) | PDP-LO7, PDP-LO11 |
| 10.4 | The team project | What happens when your small tested functions join into something bigger? | PDP-LO12, PDP-LO7, PDP-LO10 |

Contexts: Babbage, Lovelace's Note G retold in Python with exact
fractions, and Bernoulli's sum of tenth powers checked by a loop; the
six ENIAC programmers, with Kay McNulty from Creeslough; Hopper, the
first compilers, BASIC, the web, JavaScript and Python; notes on Percy
Ludgate's 1909 analytical machine and on George Boole in Cork (10.1). A
week of rainfall done four ways, with a note on why SEQUEL became SQL
(10.2). A TMP36 windowsill log whose order of hours a side effect
destroys, `sensor_celsius`'s docstring left over from the LM35 and
caught by `doctest`, the Zen of Python, and `quick_review` run over the
reader's digit, pixel, converter and statistics tools (10.3). No page
uses money. Schlomo and Schlomi appear in each practice page.

Unit product: the team project (10.4), which replaces a separate
capstone page. It has a team version (three to five people, toolkit
functions from at least four units, three releases) and an individual
version (at least three units, two releases, reviewed by a partner or
by the reader a few days later). The reader chooses one of four worlds,
each with a starter cell: a weather station or home-energy dashboard
(statistics and a chart), a small game with collision and probability
(starting from Unit 8's collision checker), a planet tracker on NASA's
exoplanet list, and a digit display in Schlomi's pixel font from Unit
1. The digit display is the worked example for design, releases and
tests. The page ends with reflection questions for everyone, for a
team and for one person, in place of a rubric.

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

## 6. The toolkit in the browser

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

**Decided: both.** A toolkit cell carries the reader's own code from page to
page; a reader can switch to the reference version at any time, and a
function the reader has not written, or whose version raises an error, loads
from the reference. So "my code" and "the reference" are two modes of one
feature, and no later page breaks either way.

## 7. How it gets built

1. **Pilot: Units 1 and 2.** Nine tutorials, eight practice pages, one mixed
   practice page and glossaries, plus the toolkit cell. Built, checked in a
   browser, and read by you before anything else is written, so the voice,
   the warm-ups and the practice format are agreed on real pages.
2. **Units 3–9 in parallel**, one agent per unit, each from a brief written
   from the agreed pilot, with the same checks as every other pass: every
   cell run, every answer run, `check.py`, the build.
3. **Unit 10 and the context pages last**, since they draw on everything.
4. **The course file**, dewey-track.yaml in the courses folder, a topic-tree group, and a
   decisions-log entry. The course starts as `status: beta`.

## 8. Coverage check

Every outcome code in the tables above, against the full lists:

- **PDP (5N2927):** LO1–LO12, all present.
- **MIT (5N18396):** 1.1–1.12, 2.1–2.5, 3.1–3.7, 4.1–4.10, 5.1–5.13,
  6.1–6.8: all 55 present, and MIT-3.7 in full, where the existing course
  narrows it.

When the course file exists, `dev/curriculum_map.py` checks the same thing
from the pages' own `covers:` frontmatter, so the claim above cannot drift.

## 9. Decisions

Made by Josh on 24 September 2026:

1. **The name:** *Plot Twist*, for now; later renamed *the Dewey Track* (7.226).
2. **The toolkit:** both modes, the reader's own code and the reference (§6).
3. **Where it sits:** beside the existing integrated course, as a beta track.
4. **The four ideas** (§2) are the spine of the track.

Made by Josh on 25 September 2026 (7.228):

5. **Contexts:** computing first, physics where the maths is physics
   (§4). Unit 1's project is a digit display, in two stages: a
   seven-segment display first, then a small pixel font. It replaces the
   bill splitter.
6. **Schlomo and Schlomi** are the track's two characters (§4).
7. **Headings and ids may change.** No reader has used the track yet, so
   headings, cell ids and toolkit names can change freely until it
   leaves beta. `waves` kept its headings and cell ids in the rewrite,
   because it was thought to be in the MIT–PDP course; that course in
   fact lists `sine-and-cosine-waves`, so `waves` is as free as the rest.
8. **Choose your project** where one idea has several good uses (§4).
9. **The tagline** says "maths".
