---
title: "Make it: a model of your own, built from angles and waves"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: Find a ship's place from the bearings of two lighthouses. The numbers are made up.
  sound: Build a chord from sine waves, and see how its notes fit together.
  planets-and-moons: Chart the Moon's rise, with its height in the sky as a wave. The model is made simpler than the real Moon.
  fantasy-maps: Survey a made-up kingdom with triangles, and draw its map. The numbers are made up.
---

# Make it: a model of your own, built from angles and waves

This series turned angles, circles, waves and slopes into programs:
lines and distances, the unit circle, waves with four numbers, the sine
and cosine rules, limits, derivatives, and the slope of a wave. Now you
use them to make a model of your own, in the world you choose. A model
here means a few functions that describe something real, answer
questions about it, and draw a picture of it.

## A first step

In every world, the first step is the same. Nearly every model here
turns an angle into a position, or a position into an angle. Here is
that pair for a circle of any radius. `math.atan2`, from
[Solving triangles: the sine rule and the cosine rule](tutorial:solving-triangles),
finds the angle from the two coordinates. Check the pair with a round
trip: an angle to a point, and back again.

```python exec
id: a-first-step-1
import math

def to_point(radius, degrees):
    """The point at this angle, anticlockwise from east, on a circle."""
    angle = math.radians(degrees)
    return radius * math.cos(angle), radius * math.sin(angle)


def to_angle(point):
    """The angle and the distance of a point from the centre."""
    x, y = point
    return math.degrees(math.atan2(y, x)), math.sqrt(x ** 2 + y ** 2)


for degrees in [30, 135, 250]:
    point = to_point(5, degrees)
    print(degrees, point, to_angle(point))
```

The round trip brings back 30 and 135, apart from rounding. 250 comes
back as $-110$. Is that the same angle? Once your own pair of functions
passes a round trip, you have the first piece of your model. Everything
after this is yours to decide.

## Make it yours

<div class="dl-world" data-world="sea-and-sky">

Find a ship's place from two lighthouses. A navigator measures the
*bearing* of each lighthouse from the ship: the angle clockwise from
north. The ship is on the line from each lighthouse back along its
bearing, so it is where the two lines cross. A bearing of $b$ degrees
points in the direction $(\sin b, \cos b)$ on a chart with north up.

Some questions your model could answer:

- Lighthouse A is on a bearing of 045° from the ship, and lighthouse B
  on 300°. Where is the ship? Draw the two lines, and mark it.
- How far is the ship from each lighthouse?
- A third lighthouse gives a third line. The three lines rarely meet at
  one point: they make a small triangle, which sailors call a *cocked
  hat*. How big is the triangle when each bearing is 1° out?

```python exec
id: make-it-yours-1--sea-and-sky
import math

lighthouses = {"A": (10, 12), "B": (-6, 9), "C": (2, -8)}    # km on the chart


def direction(bearing):
    """The chart direction of a bearing, clockwise from north."""
    angle = math.radians(bearing)
    return math.sin(angle), math.cos(angle)


print(direction(0), direction(90))
```

</div>

<div class="dl-world" data-world="sound">

Build a chord from sine waves. A note of $f$ Hz is a sine wave with $f$
waves each second. A chord is several notes at once, added together.
The A major chord is A at 440 Hz, C♯ at about 554.37 Hz and E at about
659.26 Hz, the notes a piano plays. Older tunings used exact
fractions of the A instead: $\frac{5}{4}$ and $\frac{3}{2}$ of 440, which
are 550 and 660.

Some questions your model could answer:

- Draw 20 milliseconds of each chord. Which one repeats, and how often?
- How many beats a second do the piano's notes make against the exact
  fractions?
- What does a chord of notes that do not fit well, such as 440 and 466
  Hz, look like when you draw it?

```python exec
id: make-it-yours-1--sound
import math
import matplotlib.pyplot as plt


def note(frequency):
    """A sine wave with this many waves each second."""
    return lambda t: math.sin(2 * math.pi * frequency * t)


piano = [note(440), note(554.37), note(659.26)]
seconds = [i / 100000 for i in range(2001)]    # 20 milliseconds

fig, ax = plt.subplots(figsize=(8, 3))
ax.plot([s * 1000 for s in seconds], [sum(n(s) for n in piano) for s in seconds])
ax.set_xlabel("milliseconds")
```

</div>

<div class="dl-world" data-world="planets-and-moons">

Chart the Moon's rise. Seen from one place, the Moon's height in the
sky, as an angle above the horizon, rises and falls like a wave. The
Moon comes back to the same place in the sky about every 24.84 hours,
which is why it rises about 50 minutes later each day. In this model
its height is a wave with an amplitude of 50°, a period of 24.84 hours,
a shift of 18 hours and a lift of $-5°$. The real Moon's wave changes
from night to night, so treat this one as a simpler version.

Some questions your model could answer:

- When does the Moon rise, when its height crosses 0 going up? When does
  it set?
- How fast is it climbing as it rises, in degrees an hour?
- How much later does it rise tomorrow? Draw three days of it.

```python exec
id: make-it-yours-1--planets-and-moons
import math


def moon_height(hours):
    """The Moon's angle above the horizon, in degrees, in this model."""
    return 50 * math.sin((hours - 18) / 24.84 * 2 * math.pi) - 5


for hours in [18, 19, 24]:
    print(hours, round(moon_height(hours), 1))
```

</div>

<div class="dl-world" data-world="fantasy-maps">

Survey the kingdom and draw its map. Surveyors measure one baseline
carefully, between two towers. Then from each tower they measure the
angle to a landmark, and the sine rule gives its distance. From that,
each landmark gets a place on the map, and new landmarks can be
measured from old ones.

Some questions your model could answer:

- The towers are at $(0, 0)$ and $(5, 0)$, in km. The mountain is 62°
  from the baseline at the first tower and 71° at the second. Where is
  it on the map?
- Add three more landmarks. Draw the map, with every triangle you used.
- A mistake of 1° in one angle: how far does it move a landmark?

```python exec
id: make-it-yours-1--fantasy-maps
import math

towers = [(0, 0), (5, 0)]


def sine_rule_side(known_side, known_angle, wanted_angle):
    ratio = known_side / math.sin(math.radians(known_angle))
    return ratio * math.sin(math.radians(wanted_angle))


print(sine_rule_side(5, 180 - 62 - 71, 71))    # from the first tower to the mountain
```

</div>

## If you want more

- Can your model draw a picture of every answer it gives?
- Can it say "there is no answer" in plain words, for a question with
  none: two parallel bearings, a Moon that never rises, a triangle
  whose angles are too big?
- Can it check its own answers two ways: with a round trip, with a
  second rule, or with `derivative_at` against a rule?

## Show somebody

Show your model to somebody, or write a few lines for yourself:

- What does your model do, and which page of this series did each part
  come from?
- Which answer surprised you when the model gave it?
- What did you try that did not work, and what did it teach you?
- Where is your model simpler than the real thing? What would you add
  with another hour?
