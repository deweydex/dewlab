---
title: "Make it: a running total you can see"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  planets: The planets of the solar system, measured by NASA.
  sea-floor: A deep-sea submersible's dive. The numbers are made up.
  pixels: Pixel art on a grid five squares wide.
---

<!-- TEMPLATE: a series-end making task. The reader makes something of
their own, in their world, with everything from the series. It has a first
step anyone can take and no top (#low-floor-high-ceiling). There is no
solution block: the work is the reader's own, so there is nothing to
compare it with. -->

# Make it: a running total you can see

This series was about totals that grow as a loop goes round. Now you make
one you can see growing, a line at a time, in the world you choose.

## A first step

In every world, the first step is the same. Take a loop that adds things
up, and move `print` inside it, so it prints the total every time round.

```python exec
id: a-first-step-1
widths = [4879, 12104, 12756, 6792]
total = 0
for width in widths:
    total = total + width
print(total)
```

Once the total prints four times, you have a running total you can watch.
Everything after this is yours to decide.

## Make it yours

<div class="dl-world" data-world="planets">

Draw the planets as a line of text: one `#` for every 1,000 km of width,
with the running total beside each. Mercury would be `#####` (4,879 km,
rounded). Can you add the giants, and the gaps between them?

```python exec
id: make-it-yours-1--planets
names = ["Mercury", "Venus", "Earth", "Mars"]
widths = [4879, 12104, 12756, 6792]
```

</div>

<div class="dl-world" data-world="sea-floor">

Make a dive log: after each quarter of an hour, print the depth so far,
with one `~` for every 100 m. Where would you mark the wreck, 3,800 m down?

```python exec
id: make-it-yours-1--sea-floor
drops = [540, 610, 580, 600, 590, 620]
```

</div>

<div class="dl-world" data-world="pixels">

Draw a picture of your own, five squares wide or wider. Print each row
with the number of lit pixels so far beside it. Which row lights up the
most?

```python exec
id: make-it-yours-1--pixels
sprite = [
    "..#..",
    ".###.",
    "#####",
    ".###.",
    "..#..",
]
```

</div>

## If you want more

- Can the total count down instead, from a starting amount?
- Can you print only the steps where something changes a lot?
- Can your picture use two kinds of pixel, and count each kind?

## Show somebody

Show your work to somebody, or write a few lines for yourself:

- What did you make, and what does the running total show?
- What did you try that did not work, and what did it teach you?
- What would you add with another hour?
