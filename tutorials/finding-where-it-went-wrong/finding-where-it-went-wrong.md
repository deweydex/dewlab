---
title: "Debugging: from a report to the line that caused it"
year: "2026-2027"
version: 2026.09.26.1
covers:
  a-star-goes-missing:
    covers: [CMPS-LO8]
  keeping-a-log:
    covers: [CMPS-LO8, CMPS-LO12]
  four-more-reports:
    covers: [CMPS-LO8]
  checking-halfway:
    covers: [CMPS-LO8, CMPS-LO12]
  the-smallest-example-that-still-goes-wrong:
    covers: [CMPS-LO8]
  fixing-the-symptom-or-the-cause:
    covers: [CMPS-LO10]
  what-you-did-has-names:
    covers: [CMPS-LO12]
---

# Debugging: from a report to the line that caused it

This page has nine short programs, and each one has a bug. Each program
comes with a report from the person who found the bug. The report says
what went wrong. It does not say why. Your job is to find the line that
caused it, and fix it.

The bugs are the kind everybody writes, beginners and experts. Finding
them is detective work on code. A bug is a fact about a program. It is
not a fact about the person who wrote it.

If a program stops with an error message, start with
[Reading an error message](tutorial:reading-an-error-message). Most
programs on this page do not stop. They run to the end and give a wrong
answer, which is harder to catch.

## A star goes missing

Here is the first report.

> "My program should list the five brightest stars in the night sky,
> numbered from 1. Sirius is the brightest star of all, and it is
> missing."

Here is the program.

```python exec
id: a-star-goes-missing-1
stars = ["Sirius", "Canopus", "Rigil Kentaurus", "Arcturus", "Vega"]

for number in range(1, len(stars)):
    print(number, stars[number])
```

```predict
type: choice

Before you run it: what will the first line of the output be?

- 1 Sirius
  - The loop counts from 1, and Sirius is the first star.
- 1 Canopus
  - The loop counts from 1, and the list counts from 0.
- 0 Sirius
  - `range` always starts at 0.
```

It prints `1 Canopus` first, and only four stars. We can see that
something is wrong. We cannot yet see why.

Before we change anything, let's write down a guess. Here is ours: *the
loop starts one star too late.*

A guess is only useful if we can test it. What number does `number` hold
the first time round the loop? Print it and see.

```python exec
id: a-star-goes-missing-2
for number in range(1, len(stars)):
    print("number is", number)
```

`number` is 1 the first time round, and 4 the last time. The list counts
from 0. `stars[0]` is Sirius, and `stars[4]` is Vega. So the loop never
visits 0, and Sirius is never printed. The test agrees with the guess, and
it shows why.

The writer wanted the numbers on the screen to start at 1, and they made
the loop start at 1 too. The fix keeps those two numbers apart. The loop
visits every index, from 0, and the screen shows the index plus 1.

```python exec
id: a-star-goes-missing-3
for index in range(len(stars)):
    print(index + 1, stars[index])
```

We did three things, in order:

1. We made a **guess** about the cause.
2. We ran a **test** that could show whether the guess was right.
3. We looked at **what happened**, and it told us why.

Written down, these three lines are a *log*. With a log, you do not test
the same idea twice, and somebody else can see what you have already
tried. From now on, every program on this page has a log at the top, for
you to write.

## Keeping a log

> "Four players typed in their scores. The high-score table says the best
> score is 9. I scored 30!"

`input()` always returns text, even when somebody types a number. The list
`typed` holds the four scores as `input()` returned them.

```python exec
id: keeping-a-log-1
# Guess:
# Test:
# What happened:

typed = ["9", "30", "12", "7"]

best = max(typed)
print("Best score:", best)
```

Can you write your log, and then fix the program? A good first test
prints something the program uses, to see if it is what you expected.

```hint
What kind of thing is `"30"`? How does Python put two pieces of text in
order? Try `print("30" < "9")`.
```

```inputs
best
```

```solution
typed = ["9", "30", "12", "7"]

scores = [int(score) for score in typed]
best = max(scores)
print("Best score:", best)
---
`max` compares text in alphabetical order, one character at a time.
`"9"` comes after `"3"`, so `"9"` is after `"30"`. `int()` turns
each piece of text into a whole number, and then `max` compares numbers.

A log for this one might say:

- Guess: `max` is choosing the wrong score.
- Test: `print(max(["9", "30"]))`, and `print(type(typed[0]))`.
- What happened: `max` chose `"9"`, and each score is a `str`, not an
  `int`.
```

## Four more reports

Each of these has a report, a program, and a log at the top. Try each one
before you open anything under it.

### A dimmed copy

> "I made a dimmed copy of one row of my rocket sprite, for the night
> level. Now the day level is dim too."

Each number is how bright one pixel is, from 0 (dark) to 255 (bright).

```python exec
id: a-dimmed-copy-1
# Guess:
# Test:
# What happened:

rocket = [0, 120, 255, 120, 0]

dimmed = rocket
for i in range(len(dimmed)):
    dimmed[i] = dimmed[i] // 2

print("rocket:", rocket)
print("dimmed:", dimmed)
```

```predict
type: choice

Before you run it: what will the line `rocket:` show?

- [0, 120, 255, 120, 0]
  - The loop changes `dimmed`, not `rocket`.
- [0, 60, 127, 60, 0]
  - `dimmed = rocket` does not make a new list.
```

```hint
How many lists are there in this program? Count the times a new list is
made, with square brackets.
```

```inputs
rocket
dimmed
```

```solution
rocket = [0, 120, 255, 120, 0]

dimmed = rocket[:]
for i in range(len(dimmed)):
    dimmed[i] = dimmed[i] // 2

print("rocket:", rocket)
print("dimmed:", dimmed)
---
`dimmed = rocket` gives the one list a second name. It does not make a
copy. So the loop changes the only list there is, and both names show the
change. `rocket[:]` makes a new list, as in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).
```

### The heaviest fossil

> "The museum's screen says the heaviest fossil weighs 2.1 tonnes. The
> T. rex alone weighs 8.4 tonnes."

The masses below are made up.

```python exec
id: the-heaviest-fossil-1
# Guess:
# Test:
# What happened:

def heaviest(masses):
    best = masses[0]
    for mass in masses:
        if mass > best:
            best = mass
        return best

print(heaviest([2.1, 8.4, 6.5, 1.2]))
```

```hint
How many times does the loop go round before the function returns? Can
you put a `print` inside the loop to count?
```

```inputs
heaviest([2.1, 8.4, 6.5, 1.2])
heaviest([8.4, 2.1])    # the heaviest comes first
heaviest([5.0])         # only one fossil
```

```solution
def heaviest(masses):
    best = masses[0]
    for mass in masses:
        if mass > best:
            best = mass
    return best

print(heaviest([2.1, 8.4, 6.5, 1.2]))
---
`return best` was indented one step too far, so it was inside the loop.
`return` ends the function at once, so the loop stopped after the first
fossil. Moved out one step, it runs once, after the loop has looked at
every fossil.

The bug hides when the heaviest fossil comes first in the list. A test on
that list alone gives the right answer.
```

### Stage separation

> "Our rocket drops its first stage 2.5 minutes after launch. The
> simulation goes one tenth of a minute at a time, and it never drops
> the stage."

```python exec
id: stage-separation-1
# Guess:
# Test:
# What happened:

time = 0.0          # minutes since launch
separated = False

for step in range(50):
    time = time + 0.1
    if time == 2.5:
        separated = True
        print("First stage away at", time, "minutes")

print("Separated:", separated)
```

```predict
type: choice

Before you run it: will the line "First stage away" appear?

- Yes, once
  - 25 steps of 0.1 make 2.5.
- No
  - Something about adding 0.1 so many times.
```

```hint
What is `time` after each step? Print it inside the loop, and look at the
steps near 2.5.
```

```inputs
separated
```

```solution
time = 0.0          # minutes since launch
separated = False

for step in range(50):
    time = time + 0.1
    if round(time, 1) == 2.5:
        separated = True
        print("First stage away at", time, "minutes")

print("Separated:", separated)
---
After 25 steps, `time` is `2.500000000000001`, not `2.5`. A computer
stores 0.1 very nearly, but not exactly, and 25 small differences add up.
`==` asks whether two numbers are exactly the same, so it is never true
here. `round(time, 1)` compares the time to one decimal place.

Another way is to count whole steps, which are stored exactly:
`if step == 24`.
```

### A star that was added

This one has two cells. The writer ran the first cell, and later wrote
the second.

```python exec
id: a-star-that-was-added-1
bright = ["Sirius", "Canopus", "Arcturus", "Vega"]
```

> "I made a new list with Deneb added, and ran it. Deneb is not printed.
> And when my friend runs my new cell, it stops with an error."

```python exec
id: a-star-that-was-added-2
# Guess:
# Test:
# What happened:

bright_stars = ["Sirius", "Canopus", "Arcturus", "Vega", "Deneb"]

for star in bright:
    print(star)
```

Run both cells, in order. Can you find why Deneb is missing, and why the
friend sees an error?

```hint
Which list does the loop use? What would happen in a Python that has never
run the first cell? Reloading the page starts Python again, fresh, and
keeps the code you have saved.
```

```inputs
bright_stars
```

```solution
bright_stars = ["Sirius", "Canopus", "Arcturus", "Vega", "Deneb"]

for star in bright_stars:
    print(star)
---
The loop still uses the old name, `bright`. Python keeps every name a cell
makes, until the page is reloaded. So `bright` is still there, from the
first cell, with only four stars in it.

The friend never ran the first cell, so for them `bright` does not exist,
and the loop stops with a `NameError`. The same code gave two different
results, because the two Pythons remembered different things.
```

When code works for you and fails for somebody else, an old name is often
the cause. The small ⋯ button beside Run opens "Run this cell and all
above". After a reload, it runs every cell above from the top, the way
somebody new would.

## Checking halfway

> "The table says light from the Sun takes 0.0083 minutes to reach the
> Earth. That is half a second. I read that it takes about 8 minutes."

This program has four stages. Each stage is a small function, and each
gives its result to the next.

```python exec
id: checking-halfway-1
# Guess:
# Test:
# What happened:

def read_distance(line):
    name, millions = line.split()
    return name, float(millions)

def to_km(millions):
    return millions * 1000

def light_seconds(km):
    return km / 299792          # light travels 299,792 km each second

def to_minutes(seconds):
    return seconds / 60

name, millions = read_distance("Earth 149.6")
print(name, to_minutes(light_seconds(to_km(millions))))
```

The Earth is 149.6 million km from the Sun. The bug could be in any of the
four stages. We could check them one at a time, from the top. There is a
quicker way. We check the middle first.

What should the second stage give for the Earth, if it is right? Write
your number down first, then run the cell.

```python exec
id: checking-halfway-2
print(to_km(149.6))
```

149.6 million is 149,600,000. The second stage gives 149,600. So the
first answer that is wrong comes from the first stage or the second. The
third and fourth stages are not the cause. They were given a wrong number,
and used it.

One more check splits the two stages that are left.

```python exec
id: checking-halfway-3
print(read_distance("Earth 149.6"))
```

The first stage gives `('Earth', 149.6)`, as it should. So the bug is in
the second stage, `to_km`. Can you fix it?

```python exec
id: checking-halfway-4
def to_km(millions):
    return millions * 1000

print(name, to_minutes(light_seconds(to_km(millions))))
```

```inputs
to_km(149.6)
to_minutes(light_seconds(to_km(227.9)))    # Mars
```

```solution
def to_km(millions):
    return millions * 1000000

print(name, to_minutes(light_seconds(to_km(millions))))
---
A million is 1,000,000, not 1,000. Light takes about 8.3 minutes to reach
the Earth, and about 12.7 minutes to reach Mars.
```

Two checks found the stage, out of four. Each check cut the search in
half. This is called *bisection*. You check the middle, keep the half that
still goes wrong, and then check the middle of that half. With sixteen
stages, four checks are enough.

Bisection needs the right answer at the middle, found without the program.
We knew the distance, and we could multiply by a million in our heads.
That is why we wrote our number down first.

## The smallest example that still goes wrong

> "My chain reads a ship's log and finds its most common word. It says
> the most common word is `''`, which is nothing at all."

The log below is made up. It has two spaces after each full stop, as many
older typed texts do.

```python exec
id: the-smallest-example-that-still-goes-wrong-1
log = ("day one.  the ship left the moon.  the crew slept.  "
       "day two.  the engine made a noise.  the captain fixed it.  "
       "day three.  the crew saw mars.  the ship turned.  ")

def count_words(text):
    counts = {}
    for word in text.split(" "):
        counts[word] = counts.get(word, 0) + 1
    return counts

def most_common(counts):
    best_word = None
    best_count = 0
    for word in counts:
        if counts[word] > best_count:
            best_word = word
            best_count = counts[word]
    return best_word

print(repr(most_common(count_words(log))))
```

`repr` shows text with its quotes, so an empty piece of text shows as
`''` and does not disappear.

The log is three lines long. The bug is somewhere in those three lines.
Here is a different way to find it. Make the text shorter, and keep
making it shorter, as long as it still goes wrong. Can you find the
smallest text that still gives `''` in `count_words`?

```python exec
id: the-smallest-example-that-still-goes-wrong-2
# Guess:
# Test:
# What happened:

print(count_words("day one.  the ship left the moon."))
```

```hint
Delete one word at a time. After each change, look for `''` in the
counts. If it is gone, undo your last change.
```

```hint
after: 8 runs
title: some steps
1. In the cell, delete words from the end of the text, and keep the two
   spaces after `one.`. Is `''` still there?
2. Try a text of only four characters: an a, two spaces, and a b.
3. Print that text split with `.split(" ")`. What is between `'a'` and
   `'b'`?

**Think about:** what `split(" ")` does when there are two spaces in a
row, and nothing between them.
```

```python exec
id: the-smallest-example-that-still-goes-wrong-3
def count_words(text):
    counts = {}
    for word in text.split(" "):
        counts[word] = counts.get(word, 0) + 1
    return counts

print(repr(most_common(count_words(log))))
```

Now can you fix `count_words`?

```inputs
count_words("a  b")     # two spaces between a and b
most_common(count_words(log))
count_words("")       # no text at all
```

```solution
def count_words(text):
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

print(repr(most_common(count_words(log))))
---
`split(" ")` splits at every single space. Between two spaces there is
nothing, so it makes an empty word, `''`, at every double space. In the
log it makes ten empty words, and there are only seven of *the*, so `''`
wins.
`split()` with nothing in the brackets splits at any run of spaces and new
lines, and makes no empty words. The most common word is then `'the'`.
```

The bug was two spaces in a row. A text of four characters, an a, two
spaces and a b, shows it as well as the whole log does. In an example that small, there is
nowhere else for the bug to hide.

The smallest program, or the smallest input, that still shows a bug is
called a *minimal reproduction*. It is also the best thing to send when you
ask somebody for help. Nobody has to read your whole program to see the
problem.

## Fixing the symptom or the cause

> "Our dungeon game picks a random room for each turn. Sometimes it
> crashes. When I run it again, it works."

```python exec
id: fixing-the-symptom-or-the-cause-1
import random

rooms = ["hall", "armoury", "library", "crypt", "treasury"]

def random_room():
    index = random.randint(0, len(rooms))
    return rooms[index]

for turn in range(5):
    print(random_room())
```

Run it a few times. What happens?

A bug that happens only sometimes is hard to test, because a test can pass
by luck. In
[Random numbers: pseudo-random numbers and seeds](tutorial:leaving-it-to-chance),
a seed made random numbers repeat. Here a seed makes the crash repeat. Can
you find a seed that crashes every time?

```python exec
id: fixing-the-symptom-or-the-cause-2
# Guess:
# Test:
# What happened:

random.seed(1)
for turn in range(5):
    print(random_room())
```

```hint
Change the 1 to 2, then 3, and so on. Run the cell after each change. When
it crashes, run it again with the same seed. Does it crash again?
```

With `random.seed(4)`, the program crashes every time, at the same turn.
Now we can test it. The error is an `IndexError`. It means an index that is
not in the list. The list has five rooms, with indexes 0 to 4.
`random.randint(0, len(rooms))` gives a whole number from 0 to 5,
*including* 5, so about one turn in six asks for `rooms[5]`.

What we can see going wrong is called the *symptom*. Here the symptom is
the crash. The mistake in the code that makes it happen is the *cause*.
Here the cause is the 5.

Here is one way to stop the crash. It checks for the index that crashes,
and uses room 0 in its place.

```python exec
id: fixing-the-symptom-or-the-cause-3
def random_room():
    index = random.randint(0, len(rooms))
    if index == len(rooms):
        index = 0
    return rooms[index]

counts = {}
for turn in range(6000):
    room = random_room()
    counts[room] = counts.get(room, 0) + 1
print(counts)
```

It never crashes now. The cell picks 6,000 rooms and counts them.

```predict
type: choice

Before you run it: how often will the hall be picked, out of 6,000?

- About 1,200, the same as each other room
  - The game no longer crashes, so it must work.
- About 2,000
  - The hall gets its own turns and the turns that would have crashed.
```

The hall is picked about 2,000 times, and each other room about 1,000. The
crash has gone, and the cause is still there. The turns that crashed now go
to the hall, so the hall is picked twice as often as it should be. Nobody
would notice this by playing a few turns.

This fix treated the symptom. Can you fix the cause?

```python exec
id: fixing-the-symptom-or-the-cause-4
def random_room():
    index = random.randint(0, len(rooms))
    return rooms[index]

counts = {}
for turn in range(6000):
    room = random_room()
    counts[room] = counts.get(room, 0) + 1
print(counts)
```

```inputs
len(counts)          # how many different rooms came up
counts["hall"] > 1500
```

```solution
def random_room():
    index = random.randint(0, len(rooms) - 1)
    return rooms[index]

counts = {}
for turn in range(6000):
    room = random_room()
    counts[room] = counts.get(room, 0) + 1
print(counts)
---
`random.randint(0, len(rooms) - 1)` gives an index from 0 to 4, so every
room has the same chance, and no index is outside the list.
`random.choice(rooms)` does the same in one step, and has no index to get
wrong.
```

Running the game again until it works is also a fix for the symptom, the
most common one. The crash goes away for one run, and the cause stays.

The course description calls these two ways *pragmatic problem-solving*
(treating the symptom) and *semantic analysis* (finding the cause). You
may meet those words in an assessment.

## What you did has names

You have used five habits on this page. The course names each one.

- **Initiative.** In the fossil program, a test with the heaviest fossil
  first would have passed. Trying a second test, when nobody asked for
  one, catches the bug.
- **A methodical approach.** The log asks the same three questions for
  every bug, in the same order.
- **Logical reasoning.** In the light program, one check showed that
  stages three and four were not the cause. We used that to choose the
  next check.
- **Persistence.** In the dungeon game, the crash stopped, and we did not
  stop there. We counted the rooms, and found the bug that was still
  there.
- **Lateral thinking.** To test the light program, we did not use a
  planet. We used the one distance whose answer we already knew: about
  8 minutes from the Sun to the Earth.

## Looking back

You have met nine bugs. Which one would you have been slowest to find,
if it had not come with a report? What test would have caught it early?

A challenge: plant a bug of your own. Here is a program that works. Can
you change one character so that it runs with no error and gives a wrong
answer? Then write the report a user would send, and give the program and
the report to somebody else.

```python challenge
# A program that works. Change one character to plant a bug,
# then write the report somebody would send you.
widths = [4879, 12104, 12756, 6792]    # the rocky planets, in km (NASA)

widest = widths[0]
for width in widths:
    if width > widest:
        widest = width

print("The widest rocky planet is", widest, "km across.")
```

## Where to read more

[Finding bugs in bigger programs](tutorial:when-it-goes-wrong) has more
bugs of these kinds, and tracebacks through several functions.

Evans, J. (2022). *The Pocket Guide to Debugging*. Wizard Zines. A short,
drawn guide to the habits on this page, including keeping notes and
making the smallest example.

Zeller, A. (2009). *Why Programs Fail: A Guide to Systematic Debugging*
(2nd ed.). Morgan Kaufmann. It covers bisection and the smallest example
in full.

McConnell, S. (2004). *Code Complete* (2nd ed.). Microsoft Press. Chapter
23 is about debugging, and about finding the cause, not only the symptom.
