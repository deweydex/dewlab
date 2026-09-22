---
title: "A Point on the Screen — Practice"
practice_for: a-point-on-the-screen
year: "2026-2027"
version: 2026.09.21.1
---

# A Point on the Screen — Practice

Work each one out by hand first, then run it. The arithmetic is one
division, so the practice is in deciding what to divide by what.

## Dividing by Depth

```python exec
id: dividing-1
def project(x, y, z):
    return x / z, y / z


def project_from(point, camera):
    x, y, z = point
    camera_x, camera_y, camera_z = camera
    depth = z - camera_z
    return (x - camera_x) / depth, (y - camera_y) / depth


print(project(3, 1.5, 6))
```

**1.** A point sits at $(3, 1.5, 6)$: three to the right, one and a half
up, six ahead. Where does it appear on the screen?

<details class="dl-answer"><summary>answer</summary>

$(0.5, 0.25)$. Both numbers are divided by the depth, $6$: $3 / 6 = 0.5$
and $1.5 / 6 = 0.25$. The cell above prints exactly that.

</details>

**2.** Two posts have the same height, from $y = -1$ to $y = 1$. One
stands at depth 4, the other at depth 12. How tall is each one on the
screen, and how many times taller is the nearer one?

<details class="dl-answer"><summary>answer</summary>

The near post runs from $-1/4$ to $1/4$, so it is $0.5$ tall on the
screen. The far post runs from $-1/12$ to $1/12$, so it is about
$0.167$ tall. The near one is three times taller, because it is three
times closer. Drawn height goes down in exact proportion as depth goes
up.

</details>

**3.** A point appears on the screen at $(0.2, 0.1)$, and you happen to
know it is at depth 10. Where is it in the world?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The screen position is the world position divided by the depth.
2. So the world position is the screen position multiplied by the depth.
3. Multiply both screen numbers by 10.

**Think about:** could you have answered this without being told the
depth? What did the divide throw away?

**Try this next:** the same screen point, at depth 3.

</details>

<details class="dl-answer"><summary>answer</summary>

$(2, 1, 10)$: $0.2 \times 10 = 2$ and $0.1 \times 10 = 1$. Without the
depth there is no answer at all. Every point along the line of sight
through $(0.2, 0.1)$ lands on the same pixel, which is exactly what the
divide throws away. At depth 3 the same screen point is $(0.6, 0.3, 3)$.

</details>

## Moving the Camera

**4.** The point $(1, 1, 2)$ is seen by a camera at $(0, 0, -2)$. Where
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

**5.** With a hoop of radius 2 centred five units ahead, at what point
of the turn is the ball drawn largest? How many times larger is it
there than at its smallest?

<details class="dl-answer"><summary>answer</summary>

Largest at three quarters of a turn, where the depth is $5 - 2 = 3$,
and smallest at a quarter turn, where it is $5 + 2 = 7$. The drawn
radius is the real radius divided by the depth, so the ratio is
$7 / 3$, about $2.33$: the ball at the front is a little more than
twice the size of the ball at the back.

</details>

**6.** A ball of real radius $0.3$ is drawn with a radius of $0.1$ on
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
