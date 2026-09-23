---
title: "3D animation: a camera and a ball in orbit — Practice"
practice_for: a-ball-in-orbit
year: "2026-2027"
version: 2026.09.22.1
---

# 3D animation: a camera and a ball in orbit — Practice

Work each one out by hand first, then run it. Every problem is still
one division. The practice is in deciding what to subtract first, and
what to divide by.

## Moving the Camera

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
$1 - 1 = 0$, and two units away, so it appears at $(0, 0.5)$: on the
centre line, half a unit up.

```python
print(project_from((1, 1, 2), camera=(0, 0, -2)))
print(project_from((1, 1, 2), camera=(1, 0, 0)))
```

</details>

## The Orbit

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
$7 / 3$, about $2.33$: the ball at the front is a little more than
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
