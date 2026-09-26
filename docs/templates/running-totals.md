---
title: "Running totals: adding up as you go"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  planets: The planets of the solar system, measured by NASA.
  sea-floor: A deep-sea submersible's dive. The numbers are made up.
  pixels: Pixel art on a grid five squares wide.
---

<!-- TEMPLATE: a tutorial. About an hour of somebody's evening, one idea.
The notes in these comments are for you, the author; delete them when you
copy the page. Each points to the reason in
planning/PEDAGOGICAL_STYLE_GUIDE.md. -->

# Running totals: adding up as you go

<!-- The opening runs or shows something, and asks about it. It does not
define anything yet (#discover-then-name). "On this page we:" is optional. -->

Line up the four rocky planets, Mercury, Venus, Earth and Mars, edge to
edge. Would they reach all the way round the Earth? Here are their widths
in kilometres, from NASA, and the distance round the Earth's equator.

```python exec
id: lining-them-up-1
widths = [4879, 12104, 12756, 6792]
equator = 40075

total = 0
for width in widths:
    total = total + width
print(total, "km of planet, and", equator, "km round the Earth")
```

<!-- A predict block follows its cell in the source, and the page shows it
above the cell. Two to four on a page, where the misconceptions are
(#predict-then-run). No option is right or wrong; a note names the thinking
that leads to it. -->

```predict
type: choice

Before you run it: do the four planets reach round the Earth?

- Yes, easily
  - Four whole planets sounds like a lot of planet.
- Nearly, but not quite
- Not even halfway
  - Earth is one of the four, and a planet is small beside the distance
    round it.
```

The four planets come to 36,531 km, about nine tenths of the way round.
That is closer than you might expect, and there is a reason. The distance round
a circle is $\pi$ times its width, so going round the Earth takes about
3.14 Earths. Venus is nearly as wide as the Earth, and Mercury and Mars
together are nearly one more. The four planets make about 2.86 Earths.

## What the loop does

<!-- "Try changing" comes first; the line-by-line walk-through waits in a
fold for the reader who wants it. -->

Let's see what changes the total. Can you change the order of the
planets in the list? Does the total change? What happens when `total`
starts at 100 instead of 0?

<details class="dl-answer"><summary>What each line does</summary>

- `total = 0` runs once, before the loop starts.
- `for width in widths:` takes the widths one at a time, in order. Each
  time round, `width` is the next one.
- `total = total + width` runs once for every width. It takes the total
  so far, adds this width, and keeps the answer under the name `total`.
- `print(total)` runs once, after the loop has finished.

</details>

## When the total starts again

Here is the same loop with one line moved: `total = 0` is now inside the
loop, just above the addition. Before you run it, write down what you think
it will print.

```python exec
id: when-the-total-starts-again-1
widths = [4879, 12104, 12756, 6792]

for width in widths:
    total = 0
    total = total + width
print(total)
```

```predict
type: number

What will the last line print?
```

It prints 6792, the width of Mars on its own. That's a strange result,
isn't it? Nothing is broken. The loop did exactly what it was told: every
time round, it started counting from nothing. Only the last planet, Mars,
was left in the total when the loop finished.

A name that collects something as a loop goes round, like `total`, is
called an *accumulator*. Where it starts decides everything: once, before
the loop.

<!-- A hint waits for an attempt. The first one asks a question
(#stuck). -->

```hint
after: 2 unchanged runs
Which lines run once, and which run every time round? Try putting
`print(total)` inside the loop too, and watch it change.
```

## Your turn

<!-- The task is an invitation (#invitations). Its variants follow the world
the reader chooses (#choice-of-world). Each variant's cell has its own id,
the section's id with the world added after two hyphens, so switching world
never overwrites saved work. -->

<div class="dl-world" data-world="planets">

The four giant planets are much wider. Jupiter is 142,984 km across,
Saturn 120,536, Uranus 51,118 and Neptune 49,528. Lined up edge to edge,
would they reach from the Earth to the Moon, 384,400 km away?

```python exec
id: your-turn-1--planets
giants = [142984, 120536, 51118, 49528]
moon = 384400
```

```inputs
total
moon - total    # how far short, or how far past
```

```hint
Which lines of the first cell could you copy? Which one word would you
change?
```

```solution
total = 0
for width in giants:
    total = total + width
print(total, "km of planets, and the Moon is", moon, "km away")
---
The same loop as the rocky planets, with a new list. The giants come to
364,166 km, about 95% of the way to the Moon.
```

</div>

<div class="dl-world" data-world="sea-floor">

A submersible logs how far it drops in each quarter of an hour of its dive.
The readings below are made up. The wreck of the Titanic lies about
3,800 m down. Has the submersible reached it yet?

```python exec
id: your-turn-1--sea-floor
drops = [540, 610, 580, 600, 590, 620]
wreck = 3800
```

```inputs
depth
wreck - depth    # how far to go
```

```hint
Which lines of the first cell could you copy? What name would say what
this total is?
```

```solution
depth = 0
for drop in drops:
    depth = depth + drop
print(depth, "m down, and the wreck is at", wreck, "m")
---
The accumulator here is a depth, so it has a better name than `total`.
The dive has reached 3,540 m, 260 m short of the wreck.
```

</div>

<div class="dl-world" data-world="pixels">

Here is a small picture, one row of text for each row of pixels. A `#` is a
lit pixel and a `.` is a dark one. How many pixels light up?

```python exec
id: your-turn-1--pixels
sprite = [
    "..#..",
    ".###.",
    "#####",
    ".###.",
    "..#..",
]
print(sprite[2].count("#"))
```

```inputs
lit
```

```hint
The last line counts the lit pixels in one row. How could a loop do that
for every row, and keep a total?
```

```solution
lit = 0
for row in sprite:
    lit = lit + row.count("#")
print(lit)
---
`row.count("#")` counts the lit pixels in one row, and the loop adds
the rows together. The picture has 13 lit pixels.
```

</div>

## Looking back

<!-- The closer: one question that belongs to this page, a challenge that
opens in the Notebook, and, from the predict blocks, the reader's own
surprises (added by the page, not written here). The practice page is
linked by the build. -->

Where does the start of a total belong, and why there? If you had to
explain it to somebody who put `total = 0` inside the loop, what would you
show them?

A challenge: can you make a running total that never goes below zero? A
wallet that refuses to pay more than it holds is one. A submersible that
cannot rise above the surface is another.

```python challenge
# A running total that never goes below zero.
changes = [5, -3, -4, 6, -10, 2]

total = 0
for change in changes:
    total = total + change
print(total)
```

## Read more

The planets' widths are from NASA's
[Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/).
Python's own tutorial has a short section on
[`for` statements](https://docs.python.org/3/tutorial/controlflow.html#for-statements).
