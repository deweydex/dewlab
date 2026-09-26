---
title: "The team project: design, build, release and review"
year: "2026-2027"
version: 2026.09.25.2
datasets: [exoplanets]
covers:
  the-brief:
    covers: [PDP-LO12]
  choose-a-world:
    covers: [PDP-LO7]
    touches: [PDP-LO8]
  roles-in-the-team:
    covers: [PDP-LO12]
  design-before-code:
    covers: [PDP-LO12, PDP-LO7]
    touches: [PDP-LO5]
  building-in-small-releases:
    covers: [PDP-LO12]
  testing-as-you-go:
    covers: [PDP-LO10]
  releasing-and-reviewing:
    covers: [PDP-LO12, PDP-LO7]
    touches: [PDP-LO11]
  agreeing-what-done-means:
    covers: [PDP-LO12]
  looking-back:
    covers: [PDP-LO12]
---

# The team project: design, build, release and review

You have a toolkit of about sixty functions, written and tested across
this course. Each one is small. What happens when you join them into
something bigger: a weather station, a game, a map of other worlds, a
display that draws numbers in pixels?

That is this project, in a team of three to five or on your own. This
page is a brief: the description of a piece of work, and the habits
that get it done. It has no practice page. The project is the
practice.

> **The space we're in.** A team of three to five, or one person,
> working over several weeks, with a teacher who agrees the plan. A
> team can use any tested function in any member's toolkit. The page's
> Python runs in a browser, so values a user would type are names at
> the top of a cell. One thing usually goes unsaid: most of what goes
> wrong in a team project is about people, not code.

## Warm-up

The first question is from
[Recipes are algorithms](tutorial:recipes-are-algorithms#writing-a-plan-in-pseudocode),
and the second from
[Code other people can read](tutorial:code-other-people-can-read#changing-the-code-keeping-the-promise).

```question
id: building-it-warm-up-1
type: fill-in-the-blank

Pseudocode is a plan for a program, laid out like a program, and
written for {people|computers|Python}.
```

```question
id: building-it-warm-up-2
type: multiple-choice
correct: 1

You are about to refactor a function. What comes first?

- tests that record what it does now
- new names for everything in it
- deleting its comments
```

## The brief

You design, build, release and review one program in one of the worlds
below, or in a world of your own that the teacher agrees to. There are
two versions of the brief. Choose one with your teacher.

**The team version**, for three to five people. The program:

1. uses functions from your toolkits, from **at least four units** of
   this course;
2. has its own new functions too, each with a docstring and tests;
3. comes out in **three releases**, a week or more apart;
4. is reviewed, by people who did not write it, before each release.

**The individual version**, for one person. The program:

1. uses toolkit functions from **at least three units**;
2. has its own new functions, each with a docstring and tests;
3. comes out in **two releases**, a week or more apart;
4. is reviewed before each release by a partner, with the checklist,
   or by you, reading it a few days later as a stranger would.

Both versions end with the questions in
[Looking back](tutorial:building-it-together#looking-back), answered in
your own words.

## Choose a world

Each world below names the units and toolkit functions it would draw
on, and has a starter cell to show that the first step is small. Read
all four before you choose. What you build in a world is yours to
decide.

### A weather station, or a home-energy dashboard

A temperature chip on a windowsill sends a reading every two hours.
What was the day like? Was it colder or warmer than usual, and how
steady? The same program works for an energy meter's readings, in
kilowatt-hours.

- Unit 4: `celsius_to_fahrenheit`, and `close_enough` for tests; the
  TMP36's `sensor_celsius` from
  [Machines that take a number](tutorial:machines-that-take-a-number)
- Unit 5: `mean`, `median`, `std_dev`, `largest`, `smallest`,
  `count_if`, `frequency_table`, and an honest chart from
  [Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts#a-chart-that-tells-the-truth)
- Unit 6: `shell_sort`, for the warmest hours in order
- Unit 7 or 8: `line_through`, for a trend over the days
- Unit 9, if you want it: `derivative_at`, for when it warmed fastest

The starter uses a made-up day. Before you run it, look at the
readings. Will the mean be above or below the median?

```python exec
id: building-it-weather-1
import matplotlib.pyplot as plt

hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
readings_c = [9.5, 8.5, 8.0, 7.5, 9.0, 12.5, 15.0, 16.5, 16.0, 14.0, 12.0, 10.5]

print("mean:", round(mean(readings_c), 1), "°C")
print("median:", median(readings_c), "°C")
print("spread (standard deviation):", round(std_dev(readings_c), 1), "°C")
print("from", smallest(readings_c), "to", largest(readings_c), "°C")
plt.plot(hours, readings_c, marker="o")
plt.xlabel("hour of the day")
plt.ylabel("°C")
```

The mean, 11.6 °C, sits a little above the median, 11.25 °C. The warm
afternoon pulls the mean up, and the median does not move.

### A small game, with collision and probability

A ball, a player and a pitch. Does the ball hit? How likely is a hit
from a random throw? What is a fair score?

- Unit 2: `between`, for "is the ball still on the pitch?"
- Unit 3: `simulate`, `at_least_one`, `combinations`
- Unit 4: `circle_area`, for the exact chance of a hit
- Unit 6: `insertion_sort` and `binary_search`, for a high-score table
- Unit 7: `solve_quadratic` and `vertex`, for when a thrown ball lands,
  and how high it goes
- Unit 8: `distance`, `point_on_circle`, `angle_between`, as in
  [How far apart?](tutorial:how-far-apart)

The collision checker from
[Unit 8's mixed problems](tutorial:mixed-shapes-angles-and-waves) is an
engine to start from, and its last section,
[Play it: your checker in a real game](tutorial:mixed-shapes-angles-and-waves#play-it-your-checker-in-a-real-game),
turns it into a game you move with the arrow keys: a Python cell sets
the level, and a JavaScript engine plays it on a canvas. For more on
how a page draws one frame after another,
[Drawing frames with JavaScript](tutorial:drawing-frames-with-javascript)
goes further.

The player stands on the edge of a 10 by 10 pitch. Before you run it,
guess: out of 10,000 random throws, about how many hit?

```python exec
id: building-it-game-1
import random

PLAYER = (5, 0)
PLAYER_RADIUS = 1.0
BALL_RADIUS = 0.5


def hits_player(ball):
    """Return True when a ball centred at this point touches the player."""
    return distance(ball, PLAYER) <= PLAYER_RADIUS + BALL_RADIUS


def random_throw():
    """Throw the ball to a random point on the pitch, and return True if it hits."""
    ball = (random.uniform(0, 10), random.uniform(0, 10))
    return hits_player(ball)


print(hits_player((5.8, 0.9)))
print("simulated chance of a hit:", simulate(random_throw, 10000))
print("exact chance:", circle_area(1.5) / 2 / 100)
```

About 3.5% of throws hit, and each run of the cell gives a slightly
different count. The exact answer is half a circle of radius 1.5,
because the player is on the edge, over the pitch's area of 100. A
simulation and a formula that agree are a first test worth having.

### A planet tracker

NASA's list of planets around other stars, from
[Finding things fast](tutorial:finding-things-fast): how were they
found, when, and how far away are they? Which are most like the Earth?

- Unit 4: `travel_time`, for how long light takes to arrive from each
  star
- Unit 5: `frequency_table`, `median`, `count_if`, and an honest chart
- Unit 6: `binary_search` and `shell_sort`, to find a planet by name
- Unit 7: Kepler's third law, $T^2 = a^3$, from
  [Unit 7's mixed problems](tutorial:mixed-algebra-you-can-run), on
  NASA's eight planets
- Unit 8: `point_on_circle`, to draw an orbit

Before you run it: which year do you think found the most planets?

```python exec
id: building-it-planets-1
import matplotlib.pyplot as plt

df = await load_csv("exoplanets.csv")
methods = frequency_table(df["method"].tolist())
by_year = frequency_table(df["discovered"].tolist())

print(len(df), "planets in the list")
print(methods["Transit"], "found by watching a star dim as a planet passes it")
years = sorted(by_year)
counts = []
for year in years:
    counts.append(by_year[year])
print("most in one year:", largest(counts))
plt.bar(years, counts)
plt.xlabel("year found")
plt.ylabel("planets")
```

The tallest bar is 2016, with 1,504 planets. In May 2016, NASA
announced 1,284 new planets at once, found by the Kepler space
telescope. One announcement changed the whole chart. I find that the
most surprising bar on this page.

### A digit display, in pixels

Unit 1's project, grown up: a display that draws any number in a
4 by 7 pixel font, then a clock, a score, or a countdown. How many
different glyphs could the font hold? Can a parity bit catch a pixel
that flipped?

- Unit 1: `digit_at`, `to_binary`, `to_hex`, `pixel_row`, and
  Schlomi's one-number font from
  [the mixed problems](tutorial:mixed-instructions-for-a-machine)
- Unit 2: `parity_bit`, to check each row of a glyph
- Unit 3: `permutations` and `combinations`, to count glyphs and
  patterns
- Unit 6: `binary_search`, to look a glyph up in a sorted table
- Unit 8: `point_on_circle`, if the display grows a clock face

The starter draws one digit from the font. Which digit is at place 8?

```python exec
id: building-it-digits-1
FONT = 0x69971166996996F122444688E996F8E11961359F116916196691248F26222276999996

glyph = digit_at(FONT, 8, 16 ** 7)
for row in range(7):
    print(pixel_row(digit_at(glyph, 6 - row, 16)))
```

It is the 8. Schlomi's font keeps each digit at the place with its own
number, so `digit_at` finds a glyph the way it finds a digit.

## Roles in the team

Everyone writes code, and everyone tests. On top of that, each person
holds one role for a release, and the roles change at each release, so
each of you tries more than one.

| Role | What it looks after |
|---|---|
| **Coordinator** | the plan, the dates, and a short meeting each week; says early when the team falls behind |
| **Tester** | the team's test suite; runs it before anything is shared |
| **Reviewer** | the review before each release, with the checklist from [Code other people can read](tutorial:code-other-people-can-read#a-checklist-for-a-review) |
| **Documenter** | the docstrings, the release notes, and the page that says how to use the program |
| **Builder** | one part of the program, and its promises to the other parts |

In a team of three, one person holds two roles. In a team of five, two
people are builders. On your own, you hold every role, one at a time:
for an hour you are the tester, and for another the reviewer.

## Design before code

The first week has no Python in it. You answer the four questions about
the program, and write the answers down. That written answer is the
*design*. Here it is for the digit display.

1. **What is named here?** The things the program keeps, and their
   shape: the font, as one whole number; a glyph, as 7 hex digits; a
   row of pixels, as text like `.##.`.
2. **What is promised?** Every function you will write, as a name, its
   inputs, and a docstring, with no body yet. Which toolkit functions
   each one will call.
3. **What happens when?** The main program in pseudocode, as on
   [Recipes are algorithms](tutorial:recipes-are-algorithms#writing-a-plan-in-pseudocode).
4. **What does this space let us do?** What the program assumes:
   whole numbers 0 or more, glyphs 4 pixels wide, no typed input.

The second answer matters most. When two parts of a program meet, one
calls the other. The promises one part makes to the rest (each
function's name, inputs and result) are its *interface*. Agree the
interfaces in week one, and write them as stubs, so that each builder
can work at the same time as the others. Here is one, as the design
would hold it:

```python
def number_rows(number):
    """Return the 7 rows of pixels that draw number, a whole number 0 or more.

    Each row is text: 4 pixels for each digit, one space between digits.
    Uses glyph_of, digit_at and pixel_row.
    """
    ...
```

```text
SET the font and the number to show
FOR each of the 7 rows, top to bottom:
    FOR each digit of the number, left to right:
        FIND that digit's glyph, and draw its row with pixel_row
SHOW the 7 rows
```

## Building in small releases

A *release* is a version of the program that someone outside the team
could use on the day it comes out, however little it does. Each release
gets a *version number*, such as 0.1, 0.2 and 1.0, and a date, and old
releases are kept, not overwritten.

| Release | For the digit display | The question it answers |
|---|---|---|
| 0.1 | 2026, one fixed number, printed in pixels | do the parts connect? |
| 0.2 | any number, and a clock from `digit_at` in base 60 | does the main feature work? |
| 1.0 | a parity check on every row, tidied, tested and documented | would we give this to someone? |

On your own, release 0.2 can be your last. Release 0.1 should feel
almost too small to show. Its job is to find out, in week two and not
in week six, whether one person's code fits another's.

Between releases, put the parts together often, at least twice a
week. Two parts that were each tested alone can still disagree where
they meet.

## Testing as you go

Every function the team writes has tests before anyone else uses it.
The tests come from the design: the docstring's promise, its edges, and
a second route. Here is `number_rows`, written, with the tests its
design asked for. Before you run it: which test would catch a builder
who forgot the last digit?

```python exec
id: building-it-tests-1
FONT = 0x69971166996996F122444688E996F8E11961359F116916196691248F26222276999996


def glyph_of(digit):
    """Return the 4 by 7 glyph for digit, 0 to 9, as a whole number of 7 hex digits."""
    return digit_at(FONT, digit, 16 ** 7)


def number_rows(number):
    """Return the 7 rows of pixels that draw number, a whole number 0 or more.

    Each row is text: 4 pixels for each digit, one space between digits.
    Uses glyph_of, digit_at and pixel_row.
    """
    places = len(str(number))
    rows = []
    for row in range(7):
        line = ""
        for place in range(places - 1, -1, -1):
            glyph = glyph_of(digit_at(number, place))
            line = line + pixel_row(digit_at(glyph, 6 - row, 16))
            if place > 0:
                line = line + " "
        rows.append(line)
    return rows


assert number_rows(8)[0] == ".##.", "the top row of an 8"
assert len(number_rows(0)) == 7, "every number is 7 rows tall"
for line in number_rows(2026):
    assert len(line) == 4 * 4 + 3, "four digits and three gaps"
assert number_rows(2026)[6] == "#### .##. #### .##.", "the bottom row from Unit 1"
for line in number_rows(2026):
    print(line)
```

The width test catches it: a display with three digits has rows 14
pixels long, not 19. The last test is a second route. It compares the
bottom row with the one the Unit 1 mixed page printed by hand, glyph by
glyph.

Three habits from
[Does it work?](tutorial:does-it-work) keep a team's code working:

- **A test suite, run before every share.** Keep all the team's tests
  in one cell, like `test_toolkit`, and run it before you pass code to
  anyone.
- **A structured walkthrough before each release.** The builder talks
  the team through their part, line by line, and the others ask
  questions.
- **When a test stops the cell, trace it.** Predict each value, then
  check it with a trace table or with `step_through`. Read any
  traceback from its last line, as on
  [When Python says no](tutorial:when-python-says-no#the-last-line-first).

## Releasing and reviewing

A release is more than the code. Each one comes with:

- the code, which runs from top to bottom with no errors;
- the version number and the date;
- *release notes*: a few lines on what is new, what changed, and what
  is known not to work yet;
- a note of who did what.

By the last release, the program also has a short page for the person
who will use it: what it does, how to run it, and one example.

**Before each release**, someone who did not write a part reviews it,
with the checklist. The builder answers each comment: they change the
code, or they say why not. Write down what you decided, in a line.

If you are stuck, say so the same day, to the team or to the teacher.
If someone in the team has said little for a few days, ask how they
are getting on. A team often loses more time to silence than to bugs.

## Agreeing what done means

"Done" means different things to different people, so you and the
teacher agree it in writing, in the first week. A *definition of done*
is a short list of what must be true before anything counts as
finished. Here is one to start from:

- [ ] Every function has a docstring that says its promise.
- [ ] Every function has tests, and the whole test suite passes.
- [ ] Someone who did not write it has reviewed it.
- [ ] The program runs from top to bottom with no errors.
- [ ] The release notes say what changed.

You and the teacher also agree what each release will do, and the
dates. When the plan has to change, and it usually does, say so early,
in writing, with what you will drop. Dropping one feature on time
usually costs less than delivering all of them late.

## Looking back

After the last release, a team holds a *retrospective*: a meeting that
looks back at how the team worked, to learn from it. Then each person
answers the questions below in writing, in their own words. On your
own, answer the questions for everyone, and the ones for one person.
They are a record of what building this was like, not a mark.

**For everyone**

1. Which toolkit function saved you the most work? Which did you have
   to change, and why?
2. Where did a test stop the cell before anyone else saw the problem?
3. Which review comment changed your code most? Was there one you
   decided not to act on, and why?
4. What did release 0.1 show you that you could not have known from
   the design?
5. If you started again tomorrow, what would you do the same, and what
   would you do another way?

**For a team**

6. How did the roles work out? Did they change at each release, as
   planned?
7. When was someone stuck, and how long was it before the team knew?
8. What did the interfaces you agreed in week one save you, and what
   did they miss?

**For one person**

6. What did reading your own code a few days later show you?
7. When you were stuck, where did you go first, and did it help?

<details class="dl-why"><summary>Why this way?</summary>

This project asks you to use your toolkit, from three or four units,
in one of a few worlds. Many courses end with a free project instead:
any program at all, marked against a table of levels. A free project is
good for motivation, and some of the best projects are ones no teacher
would think of.

We tied the project to the toolkit because that is what the course has
been building to: small tested promises, written by you, joined into
something bigger. We ask questions at the end, not levels, because the
questions are where you notice what you learned. The cost is choice. A
great idea that needs only one unit has to widen, or be talked over
with the teacher.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the program's data and its shape, agreed in the design; roles, so everyone knows who looks after what |
| What is promised? | interfaces agreed in week one as stubs; a definition of done, agreed with the teacher |
| What happens when? | design, then releases, each tested and reviewed; the questions for looking back last |
| What does this space let us do? | a browser's Python and your toolkit; a team of three to five, or one person, where saying you are stuck early costs least |

## What we have now

| Term | What it means |
|---|---|
| design | the four questions, answered in writing, before any code |
| interface | the promises one part of a program makes to the others: names, inputs and results |
| release, version number | a version someone outside the team could use, with a number and a date |
| release notes | a few lines on what is new, what changed, and what does not work yet |
| retrospective | a meeting after the work, to look back at how the team worked |
| definition of done | a list, agreed at the start, of what must be true before work counts as finished |

## Where to read more

The dewlab page [The Team Project](tutorial:the-team-project) is a
brief for the same kind of project, with more on sharing out the work
so that four people can build at once. The page
[Reviewing code and reflecting on your work](tutorial:critique-and-reflection)
has written questions for reading each other's code, and your own.

Martin Fowler's article
[Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
is how professional teams put everyone's work together many times a
day.
