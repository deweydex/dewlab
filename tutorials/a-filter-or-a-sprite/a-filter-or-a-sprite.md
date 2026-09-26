---
title: "Make it: a photo filter, or a sprite that moves"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  photos: Photographs, and the filters that change them.
  pixel-art: Pictures made of small squares, the way a screen draws them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
datasets: [grace-hopper]
---

# Make it: a photo filter, or a sprite that moves

This series added and scaled grids, moved shapes with matrices, joined
two moves into one, undid them, and solved systems. Now you make
something with a matrix you design yourself. In the photos world, it
is a filter that changes every pixel's colour. In the other worlds, it
is a shape that moves, drawn one frame at a time.

## A first step

Every world starts the same way, with one matrix applied again and again.
This cell turns a small arrow by the same matrix eight times, and draws
each frame a little further to the right. Change `step`, and run it
again.

```python exec
id: a-first-step-1
import math

import matplotlib.pyplot as plt
import numpy as np

arrow = np.array([(0, 1), (0.6, 0), (0.2, 0), (0.2, -1), (-0.2, -1), (-0.2, 0), (-0.6, 0)])
angle = math.radians(45)
step = np.array([[math.cos(angle), -math.sin(angle)],
                 [math.sin(angle), math.cos(angle)]])

plt.figure(figsize=(9, 2))
plt.axis("off")
frame = arrow
for k in range(8):
    shape = frame + np.array([3 * k, 0])
    plt.fill(shape[:, 0], shape[:, 1])
    frame = frame @ step.T
plt.gca().set_aspect("equal")
```

`frame @ step.T` moves every corner at once, as on the NumPy page. Try
a `step` that shrinks as well as turns, or one with determinant 0.

## Make it yours

For your world, make:

1. **The thing itself**: a filter, or a shape that moves.
2. **One matrix you designed**, with its determinant. Say in a sentence
   what the determinant tells you about your matrix.
3. **The undo.** Use the inverse to put everything back, and check that
   it worked. If your matrix cannot be undone, show what happens,
   and say why.
4. **One surprise**: something your matrix did that you did not expect.

<div class="dl-world" data-world="photos">

A colour filter is a 3×3 matrix that takes each pixel's red, green and
blue and mixes them into new ones. This cell gives the photograph of
Grace Hopper three equal colour channels, then tones it with the
classic sepia filter. Design your own filter: warmer, colder, a night
vision green, or something else.

```python exec
id: make-it-yours-1--photos
import matplotlib.pyplot as plt
import numpy as np

text = await load_text("grace-hopper.csv")
grey = np.array([[int(value) for value in line.split(",")] for line in text.splitlines()])
photo = np.stack([grey, grey, grey], axis=-1)

sepia = np.array([[0.393, 0.769, 0.189],
                  [0.349, 0.686, 0.168],
                  [0.272, 0.534, 0.131]])
toned = photo @ sepia.T
print("determinant:", np.linalg.det(sepia))

plt.figure(figsize=(6, 4))
plt.axis("off")
plt.imshow(np.clip(np.hstack([photo, toned]) / 255, 0, 1))
```

The sepia filter's determinant is about 0.00000012. That is not 0, so
it has an inverse, but its rows point in nearly the same direction.
Does undoing it restore the photo, or only rounding noise? Remember too
that a screen cuts every value above 255.

</div>

<div class="dl-world" data-world="pixel-art">

A sprite is a small picture made of squares. This cell draws one, a
little space invader, as filled squares at its points. Make it move:
walk, spin, squash when it lands, or flip to face the other way.
Draw each frame beside the last.

```python exec
id: make-it-yours-1--pixel-art
import matplotlib.pyplot as plt
import numpy as np

rows = ["..X...X..",
        "...X.X...",
        "..XXXXX..",
        ".XX.X.XX.",
        "XXXXXXXXX",
        "X.XXXXX.X",
        "X.X...X.X",
        "...X.X..."]
sprite = np.array([(x, -y) for y, row in enumerate(rows)
                   for x, square in enumerate(row) if square == "X"], dtype=float)

plt.figure(figsize=(3, 3))
plt.axis("off")
plt.scatter(sprite[:, 0], sprite[:, 1], marker="s", s=150)
plt.gca().set_aspect("equal")
```

A squash when it lands could be `[[1.2, 0], [0, 0.8]]`. Is its
determinant 1, and does that matter for a sprite?

</div>

<div class="dl-world" data-world="starships">

A ship docks by turning a little and moving closer each frame. One
matrix that turns by 15° and shrinks by 0.9 does both, and its powers
draw a spiral. Design your own manoeuvre, then fly it back out with the
inverse.

```python exec
id: make-it-yours-1--starships
import math

import matplotlib.pyplot as plt
import numpy as np

ship = np.array([(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)])
angle = math.radians(15)
step = 0.9 * np.array([[math.cos(angle), -math.sin(angle)],
                       [math.sin(angle), math.cos(angle)]])

plt.figure(figsize=(5, 5))
for k in range(0, 24, 3):
    frame = (ship + np.array([10, 0])) @ np.linalg.matrix_power(step, k).T
    plt.fill(frame[:, 0], frame[:, 1], alpha=0.6)
plt.gca().set_aspect("equal")
```

Each frame is the ship, moved out to $(10, 0)$ and then turned and
shrunk $k$ times. What is the determinant of `step`, and what does it
say happens to the ship's area each frame?

</div>

<div class="dl-world" data-world="space-scenes">

A moon goes round a planet, and the planet goes round a star. Each is
a turn, repeated. This cell draws the planet's path. Add the moon. Its
position is the planet's, plus its own small turn, going round faster.

```python exec
id: make-it-yours-1--space-scenes
import math

import matplotlib.pyplot as plt
import numpy as np


def turn_by(degrees):
    angle = math.radians(degrees)
    return np.array([[math.cos(angle), -math.sin(angle)],
                     [math.sin(angle), math.cos(angle)]])


planet = np.array([np.linalg.matrix_power(turn_by(3), k) @ np.array([5, 0]) for k in range(120)])

plt.figure(figsize=(5, 5))
plt.plot(planet[:, 0], planet[:, 1])
plt.plot([0], [0], "o", markersize=12)
plt.gca().set_aspect("equal")
```

The planet goes round once in 120 steps. If the moon goes round 12
times in that time, how many degrees does it turn each step?

</div>

## If you want more

- Put two of your matrices together into one with `@`, and check that
  it does the same as doing them one after the other.
- Find a matrix whose eighth power is the identity. What does your
  animation do after eight frames?
- Make a filter or a move with determinant 0 on purpose. What does it
  do to the picture, and what does `np.linalg.inv` say about it?
- Save your frames with `plt.savefig` and share them.

## Show somebody

Show what you made to somebody, or write a few lines for yourself:

- What does your matrix do, in words, and what is its determinant?
- Did the undo bring everything back exactly? If not, where did the
  difference come from?
- What surprised you, and can you now say why it happened?
