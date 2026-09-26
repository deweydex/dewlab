---
title: "Project: a scale model of the solar system"
year: "2026-2027"
version: 2026.09.26.1
---

<!-- TEMPLATE: a project brief. A group version and an individual version
of the same project. It ends with reflection questions only: no rubric is
shown to students. How a class runs it (time, groups, what is handed in)
is the teacher's decision, so the brief does not say (#page-shapes). -->

# Project: a scale model of the solar system

How far apart are the planets, really? Pictures in books put them side by
side, because the real gaps would not fit on the page. In this project you
build a model where the gaps are true to scale, and see them for yourself.

NASA gives each planet's average distance from the Sun, in millions of
kilometres:

| Planet | Distance from the Sun (million km) |
|---|---|
| Mercury | 57.9 |
| Venus | 108.2 |
| Earth | 149.6 |
| Mars | 228.0 |
| Jupiter | 778.5 |
| Saturn | 1432.0 |
| Uranus | 2867.0 |
| Neptune | 4515.0 |

The gap between two planets is the difference between their distances.
Walking out from the Sun, gap by gap, each planet's distance is the running
total of the gaps before it. That is what makes the model work.

```python exec
id: the-gaps-1
distances = [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0]
gaps = []
previous = 0
for distance in distances:
    gaps.append(round(distance - previous, 1))
    previous = distance
print(gaps)
```

## The group version

You need a long space: a corridor, a car park, a playing field. At a scale
of one metre for every 100 million km, Neptune stands 45.15 m from the Sun.

1. Choose a scale that fits your space. Can you find one where Mercury is
   still far enough from the Sun to see the gap?
2. Share the planets out. Each person measures one gap, starting from the
   planet before theirs, and stands there.
3. When everybody is standing, measure from the Sun to Neptune. Does it
   match the running total you expected?

## The individual version

Make the same model on a long strip of paper, or on the screen. A program
can print a line of dots with a letter at each planet: `M` at Mercury, `V`
at Venus. At a scale where one dot is 50 million km, how long is the line?

```python exec
id: the-individual-version-1
names = ["Mercury", "Venus", "Earth", "Mars",
         "Jupiter", "Saturn", "Uranus", "Neptune"]
distances = [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0]
```

## Looking back

Whichever version you made, write a few lines on each of these, or talk
about them with somebody:

- What surprised you most about the gaps?
- The planets' widths are much smaller than the gaps. At your scale, how
  wide would the Earth be? Could you still see it?
- Where did a running total help, and where was it no help at all?
- If you did this again, what would you do differently?

## Read more

The distances are from NASA's
[Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/).
