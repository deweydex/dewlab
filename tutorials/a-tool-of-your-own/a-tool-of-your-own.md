---
title: "Make it: a tool of your own, built from formulas"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  music: A tuning calculator for notes, octaves and strings.
  electronics: A circuit designer for resistors and power. The numbers are made up.
  rockets: A launch planner for rockets and the arcs they fly. The numbers are made up.
  fantasy-maps: A route finder for a made-up kingdom and its roads.
---

# Make it: a tool of your own, built from formulas

This series turned the tools of algebra into programs: powers and
logarithms, polynomials, graphs, rearranged formulas, solved equations,
vertex forms and complex numbers. Now you use them to make a tool of
your own, in the world you choose. A tool here means a few functions
that answer real questions, and a picture that shows the answers.

## A first step

In every world, the first step is the same. Take one formula from your
world, write it as a function, and write its rearrangement as a second
function. Then check the pair with a round trip, as in
[Rearranging formulae: changing the subject](tutorial:rearranging-formulae).

```python exec
id: a-first-step-1
def final_speed(u, a, t):
    return u + a * t


def time_taken(v, u, a):
    return (v - u) / a


for t in [0, 1.5, 4]:
    v = final_speed(5, 2, t)
    print(t, v, time_taken(v, 5, 2))
```

Once your own pair of functions passes a round trip, you have the first
piece of your tool. Everything after this is yours to decide.

## Make it yours

<div class="dl-world" data-world="music">

Make a tuning calculator. The note $n$ semitones above the orchestra's
A is $440 \times 2^{n/12}$ Hz. Turned round, a frequency is
$12 \log_2 \frac{f}{440}$ semitones above the A. A *cent* is a
hundredth of a semitone.

Some questions your calculator could answer:

- What is the frequency of each note in an octave?
- A guitar string sounds at 437 Hz. Which note is it nearest, and how
  many cents flat or sharp is it?
- Draw the frequencies of two octaves. Why does the curve bend?

```python exec
id: make-it-yours-1--music
import math

names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def frequency(n):
    """The frequency n semitones above the A at 440 Hz."""
    return 440 * 2 ** (n / 12)


for n in range(13):
    print(names[n % 12], round(frequency(n), 2))
```

</div>

<div class="dl-world" data-world="electronics">

Make a circuit designer. Two resistors in a line add, $a + b$. Side by
side they combine as $\frac{ab}{a + b}$. A voltage divider gives
$V_\text{out} = \frac{V_\text{in} R_2}{R_1 + R_2}$. A supply of $E$
volts with $r$ ohms inside delivers $EI - rI^2$ watts.

Some questions your designer could answer:

- Which resistor, beside a 100 ohm one, makes 60 ohms?
- Which $R_2$ turns 12 V into 3.3 V with $R_1 = 1000$ ohms?
- What is the most power a supply can deliver, and to which resistor?
  Draw the power against the current, and mark the vertex.

```python exec
id: make-it-yours-1--electronics
def series(a, b):
    """Two resistors in a line."""
    return a + b


def parallel(a, b):
    """Two resistors side by side."""
    return a * b / (a + b)


print(series(100, 220), parallel(100, 220))
```

</div>

<div class="dl-world" data-world="rockets">

Make a launch planner. A rocket launched at $u$ m/s from $s$ metres up
has a height of $s + ut - 4.9t^2$ metres after $t$ seconds. Its vertex
is the top of the flight, and its roots tell you when it lands.

Some questions your planner could answer:

- For a launch speed you choose, when is the rocket highest, how high
  does it go, and when does it land?
- What launch speed is needed to reach 50 m?
- A second rocket is launched 2 seconds later, faster. Do the two ever
  meet? Draw both heights on one picture.

```python exec
id: make-it-yours-1--rockets
import math


def height(u, s, t):
    """The height after t seconds, launched at u m/s from s metres up."""
    return s + u * t - 4.9 * t ** 2


for t in [0, 1, 2, 3]:
    print(t, round(height(15, 2, t), 2))
```

</div>

<div class="dl-world" data-world="fantasy-maps">

Make a route finder. Keep each town as a point on the map's grid, in
km, and each straight road as a line $y = mx + c$. Two roads cross
where their equations are both true. A map at 1 : $s$ turns $d$ cm on
paper into $\frac{ds}{100\,000}$ km.

Some questions your route finder could answer:

- What is the equation of the road between two towns?
- Where do two roads cross? Draw the roads, and mark the crossing.
- Walking at 5 km/h or riding at 20 km/h after a half-hour walk to the
  road: which is quicker to each town?

```python exec
id: make-it-yours-1--fantasy-maps
towns = {"Millford": (-4, 1), "Castle": (4, 5), "Harbour": (6, -2)}


def road_between(start, end):
    """The slope m and intercept c of the straight road from start to end."""
    (x1, y1), (x2, y2) = start, end
    m = (y2 - y1) / (x2 - x1)
    return m, y1 - m * x1


print(road_between(towns["Millford"], towns["Castle"]))
```

</div>

## If you want more

- Can your tool draw a picture of every answer it gives?
- Can it refuse a question with no answer, in plain words, the way a
  good solver refuses to divide by zero?
- Can it check its own answers, with a round trip or by substituting
  back?

## Show somebody

Show your tool to somebody, or write a few lines for yourself:

- What does your tool do, and which page of this series did each part
  come from?
- Which answer surprised you when the tool gave it?
- What did you try that did not work, and what did it teach you?
- What would you add with another hour?
