---
title: "3D animation: a camera and a ball in orbit — Practice"
practice_for: a-ball-in-orbit
year: "2026-2027"
version: 2026.09.26.1
worlds:
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
---

# 3D animation: a camera and a ball in orbit — Practice

Solve each one by hand first, then run it. Every problem is still
one division. The practice is to decide what to subtract first, and
what to divide by.

## Moving the camera

```python exec
id: camera-setup-1
def project(x, y, z):
    return x / z, y / z


def project_from(point, camera):
    x, y, z = point
    camera_x, camera_y, camera_z = camera
    depth = z - camera_z
    return (x - camera_x) / depth, (y - camera_y) / depth
```

**1.** The point $(1, 1, 2)$ is seen by a camera at $(0, 0, -2)$. Where
does it appear? And where does the same point appear to a camera at
$(1, 0, 0)$?

<details class="dl-answer"><summary>answer</summary>

From $(0, 0, -2)$ the point is four units ahead, so it appears at
$(1/4, 1/4) = (0.25, 0.25)$.

From $(1, 0, 0)$ the point is directly ahead in $x$, since
$1 - 1 = 0$, and two units away, so it appears at $(0, 0.5)$. That is on
the centre line, half a unit up.

```python
print(project_from((1, 1, 2), camera=(0, 0, -2)))
print(project_from((1, 1, 2), camera=(1, 0, 0)))
```

</details>

## The orbit

```python exec
id: orbit-1
import math


def ball_position(angle, radius=2, centre_depth=5, height=-0.8):
    return radius * math.cos(angle), height, centre_depth + radius * math.sin(angle)


for turn in [0, 0.25, 0.5, 0.75]:
    x, y, z = ball_position(turn * 2 * math.pi)
    print(f"{turn} of a turn: depth {z:.1f}")
```

**2.** With a hoop of radius 2 centred five units ahead, at what point
of the turn is the ball drawn largest? How many times larger is it
there than at its smallest?

<details class="dl-answer"><summary>answer</summary>

Largest at three quarters of a turn, where the depth is $5 - 2 = 3$,
and smallest at a quarter turn, where it is $5 + 2 = 7$. The drawn
radius is the real radius divided by the depth, so the ratio is
$7 / 3$, about $2.33$. The ball at the front is a little more than
twice the size of the ball at the back.

</details>

**3.** A ball of real radius $0.3$ is drawn with a radius of $0.1$ on
the screen. How far away is it? And the scatter plot in the tutorial
used `600 / z ** 2` for a dot's size. What depth makes that size 24?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Drawn radius equals real radius divided by depth, so depth equals
   real radius divided by drawn radius.
2. For the second part, $600 / z^2 = 24$ means $z^2 = 600 / 24$.
3. Take the square root.

**Think about:** why the scatter size has $z$ squared in it, when the
drawn radius only has $z$.

**Try this next:** what size does the same formula give at depth 10?

</details>

<details class="dl-answer"><summary>answer</summary>

Depth $3$, since $0.3 / 0.1 = 3$.

$z^2 = 600 / 24 = 25$, so $z = 5$. The size is an area, and an area
grows with the square of the radius, so it shrinks with the square of
the depth. At depth 10 the size is $600 / 100 = 6$.

</details>

## Frames

**4.** An animation is made with `FuncAnimation(figure, draw_step,
frames=50, interval=40)`. How many frames does it show each second, and
how long does one loop take?

<details class="dl-answer"><summary>answer</summary>

`interval=40` is 40 thousandths of a second between frames, so there are
$1000 / 40 = 25$ frames a second, one more than a cinema film. 50 frames
at 25 a second take 2 seconds, so the loop starts again every 2
seconds.

</details>

**5.** Put the hoop at eye level, with `height=0`, and plot the 60
positions again.

```python exec
id: orbit-eye-level
import matplotlib.pyplot as plt

screen_xs, screen_ys = [], []
for step in range(60):
    x, y, z = ball_position(step * 2 * math.pi / 60, height=0)
    screen_x, screen_y = project(x, y, z)
    screen_xs.append(screen_x)
    screen_ys.append(screen_y)

plt.figure(figsize=(6, 3))
plt.scatter(screen_xs, screen_ys)
plt.xlim(-0.6, 0.6)
plt.ylim(-0.35, 0.35)
plt.gca().set_aspect("equal")
```

```predict
What shape will the 60 dots make?

- An oval, like before
  - It is the same circle.
- A straight line
  - The eye is level with the hoop.
- A circle
  - Nothing is below eye level now.
```

<details class="dl-answer"><summary>answer</summary>

A straight line along the middle of the picture. Every position has
$y = 0$, and 0 divided by any depth is 0, so every dot is drawn at
$y' = 0$. You are looking at the hoop exactly edge on, as you would at
a coin held level with your eye.

</details>

**6.** Move the hoop further away, with `centre_depth=10`. How many
times larger is the ball drawn at the front than at the back now? It
was about 2.33 times at depth 5.

<details class="dl-answer"><summary>answer</summary>

1.5 times. The front of the hoop is at depth $10 - 2 = 8$ and the back
at $10 + 2 = 12$, and $12 / 8 = 1.5$. The further away the hoop is, the
less the front and the back differ, and the flatter the orbit looks.
The cube on the next page does the same when it is pushed out to depth
20.

</details>

## The near plane

**7.** On a hoop of radius 6, centred 5 units ahead, how many of the 60
positions are nearer than 0.1, where a renderer would clip them?

```python exec
id: orbit-near-plane
```

```hint
Loop over the 60 steps as in the tutorial, call
`ball_position(..., radius=6)`, and count the depths below 0.1.
```

```solution
import math


def ball_position(angle, radius=2, centre_depth=5, height=-0.8):
    return radius * math.cos(angle), height, centre_depth + radius * math.sin(angle)


clipped = 0
for step in range(60):
    x, y, z = ball_position(step * 2 * math.pi / 60, radius=6)
    if z < 0.1:
        clipped = clipped + 1
print(clipped, "of 60")
---
It prints `11 of 60`. The depth $5 + 6\sin\theta$ is below 0.1 when
$\sin\theta$ is below about $-0.82$, which happens between about 235°
and 305°. That is about a fifth of the orbit, the part that passes
behind the camera.
```

## Your world

**8.** An orbit in the world you chose.

<div class="dl-world" data-world="starships">

A shuttle circles a space station on a hoop of radius 3. The station is
8 units ahead, and the hoop is 1.5 units below eye level. How many times
larger is the shuttle drawn at the front of its circle than at the
back? Draw its path to check.

```python exec
id: orbit-world--starships
```

```hint
The front is at depth $8 - 3$ and the back at $8 + 3$. `ball_position`
takes `radius`, `centre_depth` and `height`.
```

```solution
import math

import matplotlib.pyplot as plt


def ball_position(angle, radius=2, centre_depth=5, height=-0.8):
    return radius * math.cos(angle), height, centre_depth + radius * math.sin(angle)


xs, ys = [], []
for step in range(60):
    x, y, z = ball_position(step * 2 * math.pi / 60, radius=3, centre_depth=8, height=-1.5)
    xs.append(x / z)
    ys.append(y / z)
print((8 + 3) / (8 - 3))
plt.figure(figsize=(6, 3))
plt.scatter(xs, ys)
plt.gca().set_aspect("equal")
---
It is 2.2 times. The front is at depth 5 and the back at depth 11. The path
is an oval, lower and wider at the front.
```

</div>

<div class="dl-world" data-world="space-scenes">

A comet's orbit is a stretched circle, an ellipse. Its position is
$x = 4\cos\theta$, $y = -1$ and $z = 6 + 1.5\sin\theta$. Can you draw
its path, and find where on the screen the comet is drawn largest?

```python exec
id: orbit-world--space-scenes
```

```hint
Write a `comet_position(angle)` like `ball_position`, with 4 across and
1.5 in depth.
```

```solution
import math

import matplotlib.pyplot as plt


def comet_position(angle):
    return 4 * math.cos(angle), -1, 6 + 1.5 * math.sin(angle)


xs, ys, depths = [], [], []
for step in range(60):
    x, y, z = comet_position(step * 2 * math.pi / 60)
    xs.append(x / z)
    ys.append(y / z)
    depths.append(z)
plt.figure(figsize=(6, 3))
plt.scatter(xs, ys, s=[600 / z ** 2 for z in depths])
plt.gca().set_aspect("equal")
print(min(depths))
---
It is drawn largest at the front, at depth 4.5, three quarters of the
way round. The path is a wide, flat oval, because the ellipse is much
longer across than it is deep.
```

</div>

## From earlier

**9.** From *what a matrix does to a picture*. `ball_position` puts the
ball at $(r\cos\theta, r\sin\theta)$ across and in depth, before the
centre depth is added. Which 2×2 matrix sends $(r, 0)$ there?

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta
\end{bmatrix}$, the turn by $\theta$. Its first column is
$(\cos\theta, \sin\theta)$, so it sends $(r, 0)$ to
$(r\cos\theta, r\sin\theta)$. The next page calls it the rotation
matrix.

</details>

**10.** From *Repeating steps with loops*. The flip-book in the tutorial
draws 10 frames round one turn. How many degrees are there between one
frame and the next, and how many radians?

<details class="dl-answer"><summary>answer</summary>

36°, since $360 / 10 = 36$. In radians it is $2\pi / 10 \approx 0.628$,
which is what `index * 2 * math.pi / 10` adds each time round the loop.

</details>
