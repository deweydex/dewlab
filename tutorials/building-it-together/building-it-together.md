---
title: "The team project: design, build, release and review"
year: "2026-2027"
version: 2026.09.24.1
covers:
  the-brief:
    covers: [PDP-LO12]
  three-projects-to-choose-from:
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
---

# The team project: design, build, release and review

Four people, one program, a few weeks. Each of you has a toolkit of
about sixty functions, written and tested across this course. Can the
four of you build something together that none of you would build
alone, without losing a week to code that does not fit?

This page is a brief: the description of a piece of work, and the
habits that get it done. There is less code on it than on other pages,
and no practice page. The project is the practice.

On this page we:

- set out what the team project asks for
- look at three projects, and which units and toolkit functions each
  one uses
- share out the roles in a team
- design with the four questions before anyone writes code
- build in small releases, testing as we go
- release, review, and look back
- agree with the teacher what "done" means, and read the rubric

> **The space we're in.** A team of three to five, working over several
> weeks, with a teacher who agrees the plan. Every person has a toolkit;
> the team can use any function in any member's toolkit, as long as it
> is tested. The page's Python runs in a browser, so a program here
> cannot ask for typed input or save files: values the user would type
> are names at the top of a cell. One thing usually goes unsaid: most of
> what goes wrong in a team project is about people, not code.

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

As a team of three to five, you design, build, release and review one
program. It must:

1. use functions from your toolkits, from **at least four units** of
   this course;
2. have its own new functions too, each with a docstring and tests;
3. come out in **three releases**, a week or more apart;
4. be reviewed, by people who did not write it, before each release.

This project takes the place of a single final assignment. The course
has been building toward it: each toolkit function you wrote is a part
your team can use without writing it again.

## Three projects to choose from

Each suggestion below names the units and toolkit functions it would
draw on. The starter cells are there to show that the first step is
small. Your team may bring its own idea instead, if the teacher agrees
it meets the brief.

### A fitness tracker, with statistics and charts

A week, or a month, of runs, walks or swims: how far, how fast, and is
it getting better?

- Unit 3: `total`, and `simulate` for "how likely is a week over 30 km?"
- Unit 4: `speed`, `travel_time`, and `close_enough` for tests
- Unit 5: `mean`, `median`, `std_dev`, `largest`, `count_if`,
  `frequency_table`, and an honest chart from
  [Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts#a-chart-that-tells-the-truth)
- Unit 6: `insertion_sort` for a table of best times
- Unit 7 or 8: `line_through`, for a trend line through the weeks
- Unit 9, if you want it: `derivative_at`, for speed at one moment

The starter uses a made-up week. Before you run it, add up the week's
distance in your head. What do you expect?

```python exec
id: building-it-fitness-1
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
run_km = [5.0, 0, 3.2, 6.1, 0, 10.0, 4.5]
run_minutes = [27.5, 0, 18.0, 33.4, 0, 58.0, 24.8]

speeds = []
for day in range(len(days)):
    if run_km[day] > 0:
        speeds.append(speed(run_km[day], run_minutes[day] / 60))

print("distance this week:", round(total(run_km), 1), "km")
print("mean speed:", round(mean(speeds), 1), "km/h")
print("fastest:", round(largest(speeds), 1), "km/h")
plt.bar(days, run_km)
plt.ylabel("km run")
```

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
  [How far apart?](tutorial:how-far-apart#did-the-ball-hit-the-player)

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
different count. The exact answer is half a circle of radius
1.5, because the player is on the edge, over the pitch's area of 100.
A simulation and a formula that agree are a good first test.

### A trip planner, with distances and bearings

A list of places to visit. How far is the whole trip, how long will it
take, which way do you set off, and which order of stops is shortest?

- Unit 1: `split_bill`, to share the cost of fuel
- Unit 3: `factorial` and `permutations`, to count the orders of stops
- Unit 4: `travel_time`, `distance_travelled`
- Unit 5: `mean` and `largest`, for the legs of the trip
- Unit 6: `selection_sort` and `linear_search`, to list and find stops
- Unit 8: `distance`, `midpoint` for a meeting point, `angle_between`,
  and the `bearing` function from
  [How tall is that tree?](tutorial:how-tall-is-that-tree#bearings),
  which your team adds to its own code

The towns below are placed roughly, in kilometres east and north of
Cork, on a flat map. The distances are straight lines, so a road is
longer. What total do you expect?

```python exec
id: building-it-trip-1
TOWNS = {"Cork": (0, 0), "Limerick": (-11, 84), "Galway": (-39, 152), "Dublin": (148, 161)}
AVERAGE_SPEED = 80   # km/h along a straight line: a made-up speed

route = ["Cork", "Limerick", "Galway", "Dublin"]
trip_km = 0
for stop in range(len(route) - 1):
    leg = distance(TOWNS[route[stop]], TOWNS[route[stop + 1]])
    trip_km = trip_km + leg
    print(route[stop], "to", route[stop + 1], round(leg), "km")

print("total", round(trip_km), "km, about", round(travel_time(trip_km, AVERAGE_SPEED), 1), "hours")
print(factorial(len(route) - 1), "orders for the stops after Cork")
```

About 345 km of straight lines, and six orders to compare. Ask the fourth question here: the map
is flat, and Ireland is on a sphere. On
[How tall is that tree?](tutorial:how-tall-is-that-tree), a triangle on
a globe broke the flat plane's rules. Over the size of Ireland, the
error is small; over the Atlantic, it is not.

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
people are builders.

## Design before code

The first week has no Python in it. The team answers the four questions
about the program, and writes the answers down. That written answer is
the *design*.

1. **What is named here?** The things the program keeps, and their
   shape. For the trip planner: towns, as a dictionary from a name to
   an `(x, y)` pair; a route, as a list of names.
2. **What is promised?** Every function the team will write, as a name,
   its inputs, and a docstring, with no body yet. Which toolkit
   functions each one will call.
3. **What happens when?** The main program in pseudocode, as on
   [Recipes are algorithms](tutorial:recipes-are-algorithms#writing-a-plan-in-pseudocode).
4. **What does this space let us do?** What the program assumes: a flat
   map, no typed input, straight lines, a speed that never changes.

The second answer matters most. When two parts of a program meet, one
calls the other. The promises one part makes to the rest (each
function's name, inputs and result) are its *interface*. Agree the
interfaces in week one, and write them as stubs, so that each builder
can work at the same time as the others. Here is one for the trip
planner, as the design would hold it:

```python
def route_length(route, towns):
    """Return the length in km of route, a list of town names in the order visited.

    towns is a dictionary from each town's name to its (x, y) position in km.
    A route of one town has length 0. Uses distance() from the toolkit.
    """
    ...
```

```text
SET towns, route and speed
FOR each leg of the route:
    FIND its length with distance
SHOW each leg, the total, and the time with travel_time
```

## Building in small releases

A *release* is a version of the program that someone outside the team
could use on the day it comes out, however little it does. Each release
gets a *version number*, such as 0.1, 0.2 and 1.0, and a date, and old
releases are kept, not overwritten.

| Release | For the trip planner | The question it answers |
|---|---|---|
| 0.1 | the length of one fixed route, printed | do the parts connect? |
| 0.2 | any route, with times, bearings and a map drawn | does the main feature work? |
| 1.0 | the shortest order of stops, tidied, tested and documented | would we give this to someone? |

Release 0.1 should feel almost too small to show. Its job is to find
out, in week two and not in week six, whether one person's code fits
another's.

Between releases, put the parts together often, at least twice a
week. Two parts that were each tested alone can still disagree where
they meet.

## Testing as you go

Every function the team writes has tests before anyone else uses it.
The tests come from the design: the docstring's promise, its edges, and
a second route. Here is `route_length`, written, with the tests its
design asked for. Which test would catch a builder who forgot the last
leg?

```python exec
id: building-it-tests-1
def route_length(route, towns):
    """Return the length in km of route, a list of town names in the order visited.

    towns is a dictionary from each town's name to its (x, y) position in km.
    A route of one town has length 0. Uses distance() from the toolkit.
    """
    length = 0
    for stop in range(len(route) - 1):
        length = length + distance(towns[route[stop]], towns[route[stop + 1]])
    return length


assert route_length(["Cork"], TOWNS) == 0, "one town, no legs"
assert close_enough(route_length(["Cork", "Dublin"], TOWNS), distance((0, 0), (148, 161)))
assert close_enough(route_length(route, TOWNS), trip_km), "the same as the starter cell"
assert close_enough(route_length(route, TOWNS), route_length(route[::-1], TOWNS)), "there and back"
print("route_length keeps its promise.")
```

The third test would catch it: it compares the whole route with the
starter cell's total, found a second way. `route[::-1]` is the route
backwards, and a trip is as long in either direction.

Three habits from
[Does it work?](tutorial:does-it-work) keep a team's code working:

- **A test suite, run before every share.** Keep all the team's tests
  in one cell, like `test_toolkit`, and run it before you pass code to
  anyone.
- **A structured walkthrough before each release.** The builder talks
  the team through their part, line by line, and the others ask
  questions.
- **When a test fails, trace it.** Predict each value, then check it
  with a trace table or with `step_through`. Read any traceback from its
  last line, as on
  [When Python says no](tutorial:when-python-says-no#the-last-line-first).

## Releasing and reviewing

A release is more than the code. Each one comes with:

- the code, which runs from top to bottom with no errors;
- the version number and the date;
- *release notes*: a few lines on what is new, what changed, and what
  is known not to work yet;
- a note of who did what.

By release 1.0, the program also has a short page for the person who
will use it: what it does, how to run it, and one example.

**Before each release**, someone who did not write a part reviews it,
with the checklist. The builder answers each comment: they change the
code, or they say why not. Write down what you decided, in a line.

**After the last release**, the team holds a *retrospective*: a meeting
that looks back at how the team worked, to learn from it. Four
questions are enough. What went as planned? What surprised us? Where
did the time go? What would we do differently next time? Then each
person writes about a page, in their own words.

If you are stuck, say so the same day. If someone in the team has said
little for a few days, ask how they are getting on. A team often loses more time to
silence than to bugs.

## Agreeing what done means

"Done" means different things to different people, so the team and the
teacher agree it in writing, in the first week. A *definition of done*
is a short list of what must be true before anything counts as
finished. A good one for this project:

- [ ] Every function has a docstring that says its promise.
- [ ] Every function has tests, and the whole test suite passes.
- [ ] Someone who did not write it has reviewed it.
- [ ] The program runs from top to bottom with no errors.
- [ ] The release notes say what changed.

The teacher and the team also agree what each release will do, and the
dates. When the plan has to change, and it usually does, the team says
so early, in writing, with what it will drop. Dropping one feature on
time is usually better than delivering all of them late.

### A rubric in plain words

A *rubric* is a table that says what the work is judged on, and what
each level looks like. This one is the starting point; your teacher may
change it.

| What is judged | Not yet | Done | Beyond |
|---|---|---|---|
| It works | crashes, or gives wrong answers | runs and keeps its promises | handles odd inputs with a clear message |
| It uses the course | fewer than four units | toolkit functions from four units | the maths is explained where it is used |
| It is tested | few or no tests | tests for every function, all passing | tests at every edge, and a second route |
| It can be read | a stranger cannot follow it | names, docstrings and layout pass the checklist | a user's page that a stranger can follow alone |
| It grew over time | one release at the end | three releases, each kept, with notes | each release acted on the last review |
| The team worked | one or two people did most of it | roles shared and changed, reviews done | the retrospective led to a real change |

<details class="dl-why"><summary>Why this way?</summary>

This project asks every team to use its toolkits, from at least four
units. Many courses end with a free project instead: any program the
team wants to build, judged on how well it is made.

A free project is good for motivation. A team building something it
cares about works harder, and some of the best projects are ones no
teacher would think of.

We tied the project to the toolkits because that is the point the
course has been building to: small tested promises, written by you,
joined into something bigger. The cost is choice. A team with a great
idea that needs only one unit has to widen it, or talk to the
teacher.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the program's data and its shape, agreed in the design; roles, so everyone knows who looks after what |
| What is promised? | interfaces agreed in week one as stubs; a definition of done, agreed with the teacher |
| What happens when? | design, then three releases, each tested and reviewed; the retrospective last |
| What does this space let us do? | a flat map and a browser's Python; a team of three to five, where saying you are stuck early costs least |

## What we have now

| Term | What it means |
|---|---|
| design | the four questions, answered in writing, before any code |
| interface | the promises one part of a program makes to the others: names, inputs and results |
| release, version number | a version someone outside the team could use, with a number and a date |
| release notes | a few lines on what is new, what changed, and what does not work yet |
| retrospective | a meeting after the work, to look back at how the team worked |
| definition of done | a list, agreed at the start, of what must be true before work counts as finished |
| rubric | a table of what is judged, and what each level looks like |

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
