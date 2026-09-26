---
title: "Perspective projection: dividing by depth"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
  photos: Photographs, and the filters that change them.
covers:
  a-road-of-posts:
    covers: [CMPS-LO4]
  why-dividing-works:
    covers: [CMPS-LO4]
---

# Perspective projection: dividing by depth

Every picture on a screen is flat. Most of the things in a picture are
not. A game, a film's special effects and a 3D chart all start with
points that have a ***depth***, a distance in front of you. They all
end as pixels on a flat screen, and a pixel has no depth at all.
Somewhere in between, every point loses its third number.

This tutorial is about the rule that takes that number away. You might
expect something complicated. It is one division. By the end you will
have drawn a road of fence posts with that one division, and you will
have seen why it works. The next tutorial uses the same division to
move a camera and to make a ball go round in a circle.

Keep three things in mind as you go:

- Every cell on this page is yours to change. Change a number, run it
  again, and see what happens.
- A cell that gives an error has told you something about a line, not
  about you. One of the questions below is *meant* to go wrong.
- If a word is new, it is in bold the first time it appears, and the
  Reference panel, on the left, has all of them.

## A road of posts

Here are twelve fence posts, six on each side of a road. They are all
the same height, and they run away from you into the distance. Let's
run the cell before reading on.

```python exec
id: a-road-of-posts-1
import matplotlib.pyplot as plt

def project(x, y, z):
    return x / z, y / z

plt.figure(figsize=(5, 5))
for depth in [2, 3, 4, 6, 9, 14]:
    for side in [-1.5, 1.5]:
        foot_x, foot_y = project(side, -1, depth)
        top_x, top_y = project(side, 1, depth)
        plt.plot([foot_x, top_x], [foot_y, top_y], color="C0", linewidth=3)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.gca().set_aspect("equal")
```

Here is what each part of the cell does:

- `project(x, y, z)` takes three numbers and returns two. It is the
  whole rule, and it is two divisions.
- `depth` takes the values 2, 3, 4, 6, 9, 14: six posts on each side, each
  one further away than the last.
- `side` is $-1.5$ for the left-hand posts and $1.5$ for the right-hand
  ones.
- Each post is a line from its foot at $y = -1$ to its top at $y = 1$.

So every post is built the same way. The only thing that changes from
post to post is `depth`. Yet the far posts are drawn smaller. They are
drawn closer to the centre. Their bottoms sit higher up the picture,
the way the far end of a real road does. Nothing in the cell says
"make the far ones smaller". All `project` does is divide.

Each point going in has three numbers. $x$ is how far to the right.
$y$ is how far up. $z$, called `depth` in the cell, is how far in front
of you. What comes out has two numbers, because the picture is flat:

$$x' = \frac{x}{z}, \qquad y' = \frac{y}{z}$$

Read $x'$ as "the new $x$": where the point lands on the screen. Let's
do one by hand. The top of the nearest right-hand post is at
$(1.5, 1, 2)$. So:

$$x' = \frac{1.5}{2} = 0.75, \qquad y' = \frac{1}{2} = 0.5$$

Find that post in the picture: the tall one on the right, with its top
at $0.5$. Now the top of the furthest right-hand post, at
$(1.5, 1, 14)$: $x' = 1.5 / 14 \approx 0.11$ and $y' = 1 / 14 \approx 0.07$.
It is small, and close to the middle. The post is the same, but it is
seven times further away, so it is drawn seven times smaller.

### Your turn

What happens to the posts if you double every depth? What about a post
at depth 1, or at depth 0.5? And where would a post at depth 0 land?
Try that last one too. It gives an error on purpose.

```python exec
id: a-road-of-posts-2
hint: Copy the loop from the cell above and change the list of depths. Depth 0 is a division by zero, and Python says so.
```

## Why dividing works

Why divide, rather than subtract, or anything else? A side view answers
it. Imagine standing at the left edge of the next picture, looking to
the right along $z$. The screen is a sheet of glass standing one unit
in front of your eye. Light from a point behind the glass travels in a
straight line to your eye. You see the point at the place where that
line crosses the glass.

```python exec
id: why-dividing-works-1
eye = (0, 0)
point = (4, 2)  # four units ahead, two units up
screen_z = 1

plt.figure(figsize=(6, 3))
plt.plot([eye[0], point[0]], [eye[1], point[1]], color="C1", label="line of sight")
plt.axvline(screen_z, color="grey", linestyle="--", label="the glass")
plt.plot(*point, "o", color="C0", label="the point")
plt.plot(*eye, "o", color="black", label="your eye")
plt.plot(screen_z, point[1] / point[0], "o", color="C3", label="where it appears")
plt.xlabel("z (ahead)")
plt.ylabel("y (up)")
plt.legend()
```

The line of sight crosses the glass at $y = 0.5$. And $0.5$ is $2 / 4$:
the point's height divided by its depth. That is not a coincidence.
Here is why, in three small steps:

1. Two triangles share this picture. A big one runs from your eye out
   to the point: base $4$, height $2$. A small one runs from your eye
   out to the glass: base $1$, height $y'$.
2. They are the same shape. One is a bigger copy of the other. Two
   triangles like that are called ***similar triangles***, and in
   similar triangles the matching sides are in the same ratio.
3. So the small triangle's height divided by its base equals the big
   triangle's height divided by its base:

$$\frac{y'}{1} = \frac{y}{z} = \frac{2}{4}$$

Look at the same scene from above instead of from the side, and the
same picture gives $x'$. This is the whole rule. Its name is the
***perspective divide***. Perspective is the word for the way far
things look smaller, and this divide causes it. Painters
found this in the early 1400s, and every picture since then
that looks "right" uses it, whether the painter knew the
arithmetic or not.

When we turn a point that has a depth into a point on a flat screen,
we are ***projecting*** it. The word comes from a projector, which
throws a picture onto a screen. This division is the projection that
every camera does, whether it is a real camera or a few lines of code.

One thing in the picture was a choice: the glass stands one unit away.
Stand it two units away and everything on it is drawn twice as big.
That is what a zoom lens does. We return to that in [Field of
view](tutorial:the-fourth-number#field-of-view), in the fourth tutorial
of this series.

```question
id: why-dividing-works-2
type: multiple-choice
answer: 2

A post 2 units tall stands at depth 8. How tall is it on the screen?

- 2 units
  - This keeps the post's own height, as if depth made no difference on the screen.
- 0.25 units
  - Height divided by depth: 2 divided by 8.
- 4 units
  - This divides the depth by the height, the other way round.
```

<details class="dl-answer"><summary>the same in NumPy</summary>

[NumPy](tutorial:matrices-in-numpy) divides a whole column of numbers at
once. Put every post end in one array, one row each, and one line
projects them all:

```python
import numpy as np

ends = np.array([[side, height, depth] for depth in [2, 3, 4, 6, 9, 14]
                 for side in [-1.5, 1.5] for height in [-1, 1]])
screen = ends[:, :2] / ends[:, 2:3]
print(screen[:4])
```

`ends[:, :2]` is the first two columns, $x$ and $y$, and `ends[:, 2:3]`
is the depth column. Dividing one by the other divides each row by its
own depth. The first four rows are the two nearest posts, at
$(\pm 0.75, \pm 0.5)$.

</details>

## Your world

The same division, in the world you chose.

<div class="dl-world" data-world="starships">

A starship is 100 metres long. You hold a model of it, 1 metre long,
0.6 metres from your eye. The real ship flies straight away from you.
How far away is it when it looks exactly as long as the model?

```python exec
id: point-your-world--starships
def drawn_length(length, depth):
    return length / depth


print(drawn_length(1, 0.6))
```

```hint
The model is drawn `drawn_length(1, 0.6)` long. Try the ship at depths
of 10, 20, 30 and so on, and look for the same number. Or solve
$100 / d = 1 / 0.6$ for $d$.
```

```solution
def drawn_length(length, depth):
    return length / depth


print(drawn_length(1, 0.6))
for depth in range(10, 101, 10):
    print(depth, round(drawn_length(100, depth), 3))
---
The model is drawn about 1.667 long, and so is the ship at 60 metres:
$100 / 60 = 1 / 0.6$. The ship is 100 times longer, so it has to be 100
times further away, $100 \times 0.6 = 60$ metres. A film uses this with
models, and the camera cannot tell the difference.
```

</div>

<div class="dl-world" data-world="space-scenes">

The Moon is 1,737 km in radius and about 384,400 km away. The Sun is
696,000 km in radius and about 149,600,000 km away. Which one looks
bigger in the sky?

```python exec
id: point-your-world--space-scenes
moon_radius, moon_distance = 1737, 384400
sun_radius, sun_distance = 696000, 149600000
```

```predict
Which looks bigger from the Earth?

- The Sun, by a lot
  - The Sun is 400 times wider than the Moon.
- About the same
  - The Sun is also much further away.
- The Moon, by a lot
  - The Moon is much closer.
```

```hint
The drawn size is the real size divided by the depth, as for the posts.
```

```solution
moon_radius, moon_distance = 1737, 384400
sun_radius, sun_distance = 696000, 149600000
print(round(moon_radius / moon_distance, 5))
print(round(sun_radius / sun_distance, 5))
---
They are 0.00452 and 0.00465, only about 3% apart. The Sun is about 400
times wider than the Moon, and about 400 times further away, so the
division cancels it out. The Moon's distance changes by about a tenth
over a month. So in an eclipse the Moon sometimes covers the Sun
completely, and sometimes leaves a thin ring of it showing.
```

</div>

<div class="dl-world" data-world="photos">

A photo hangs on a wall to your right, and the wall runs away from
you. The photo is 1 unit tall, from $y = -0.5$ to $y = 0.5$. Its near
edge is at depth 2 and its far edge at depth 4, both at $x = 1.5$. What
shape is it on the screen?

```python exec
id: point-your-world--photos
import matplotlib.pyplot as plt


def project(x, y, z):
    return x / z, y / z


corners = [(1.5, -0.5, 2), (1.5, 0.5, 2), (1.5, 0.5, 4), (1.5, -0.5, 4)]
```

```predict
What shape does the photo make on the screen?

- A rectangle, as on the wall
  - The photo is a rectangle.
- A shape with a short far edge
  - The far edge is twice as far away.
- A shape with a short near edge
  - The near edge is closer to the middle of the picture.
```

```hint
Project each corner, then draw the four screen points with `plt.fill`,
as in the first cell of the page.
```

```solution
import matplotlib.pyplot as plt


def project(x, y, z):
    return x / z, y / z


corners = [(1.5, -0.5, 2), (1.5, 0.5, 2), (1.5, 0.5, 4), (1.5, -0.5, 4)]
screen = [project(x, y, z) for x, y, z in corners]
print(screen)
plt.figure(figsize=(4, 4))
plt.fill([p[0] for p in screen], [p[1] for p in screen], alpha=0.5)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.gca().set_aspect("equal")
---
The near edge runs from $-0.25$ to $0.25$, and the far edge from
$-0.125$ to $0.125$, half as tall. The photo is drawn as a shape that
narrows away from you. That is also why a photo of a tall building,
taken from the ground, seems to lean back. Its top is further away, so
it is drawn smaller.
```

</div>

## Reflection

One division gives a flat picture depth. Where did the division
come from, when you saw the side view with the glass in it? Was it what
you expected, or had you assumed something more complicated was
happening inside a game?

So far the eye has stayed in one place, and nothing has moved. [3D
animation: a camera and a ball in orbit](tutorial:a-ball-in-orbit)
moves the camera, and then sends a ball round in a circle, with
the same division doing all the work.

## Where to read more

O'Flaherty-Chan, G. (2026). *Divide by depth for instant 3D.*
<https://gabrieloc.com/2026/09/15/perspective.html>. This series grew
from this blog post. It has the same divide, a camera you can move, and
the same ball in orbit, in a few dozen lines of code. It ends at the
projection matrix the fourth tutorial builds.

Scratchapixel. *Computing the Pixel Coordinates of a 3D Point.*
<https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/>.
This lesson draws the same similar-triangles picture carefully. Then it
shows the extra steps that turn a point on the glass into a pixel on a real
screen.

CrashCourse (2017). *3D Graphics: Crash Course Computer Science #27.*
<https://www.youtube.com/watch?v=TEAtmCYYKZA>. This video shows how a 3D
scene becomes a flat picture: projecting points onto the screen, colouring the triangles,
and deciding which ones are in front. Twelve minutes.
