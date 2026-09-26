---
title: "Perspective projection: dividing by depth — Practice"
practice_for: a-point-on-the-screen
year: "2026-2027"
version: 2026.09.26.1
---

# Perspective projection: dividing by depth — Practice

Solve each one by hand first, then run it. The arithmetic is one
division, so the practice is to decide what to divide by what.

## Dividing by depth

```python exec
id: dividing-1
def project(x, y, z):
    return x / z, y / z


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
depth? What did the divide lose?

**Try this next:** the same screen point, at depth 3.

</details>

<details class="dl-answer"><summary>answer</summary>

$(2, 1, 10)$: $0.2 \times 10 = 2$ and $0.1 \times 10 = 1$. Without the
depth there is no answer at all. Every point along the line of sight
through $(0.2, 0.1)$ lands on the same pixel, which is exactly what the
divide loses. At depth 3 the same screen point is $(0.6, 0.3, 3)$.

</details>

**4.** In the tutorial the glass stood one unit in front of your eye.
Suppose it stands two units away instead. Where does the point
$(3, 1.5, 6)$ from problem 1 appear now?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw the side view again: your eye, the glass, and the point.
2. The small triangle now has a base of 2, not 1.
3. The two triangles are still similar, so
   $\frac{y'}{2} = \frac{y}{z}$.

**Think about:** what happens to every point on the screen when the
glass moves from 1 to 2?

</details>

<details class="dl-answer"><summary>answer</summary>

$(1, 0.5)$. With the glass at distance 2, the similar triangles give
$y' / 2 = y / z$, so $y' = 2 \times 1.5 / 6 = 0.5$. In the same way
$x' = 2 \times 3 / 6 = 1$. Both numbers are twice what they were in
problem 1. When the glass moves twice as far away, everything is drawn twice
as big, which is what a zoom lens does.

</details>

## Very near

**5.** A post from $y = -1$ to $y = 1$ stands at depth 0.5, closer than
the glass. Where are its ends on the screen?

```python exec
id: very-near-1
print(project(0, -1, 0.5), project(0, 1, 0.5))
```

```predict
Where do the post's ends land?

- Between -1 and 1, like the other posts
  - Every post so far fitted on the screen.
- Beyond -1 and 1, off the edge of a screen that runs from -1 to 1
  - Dividing by a number smaller than 1 makes it bigger.
- At 0
  - It is very close to the eye.
```

<details class="dl-answer"><summary>answer</summary>

At $-2$ and $2$. Dividing by 0.5 doubles a number, so the post is drawn
twice its real height, and its ends are off the edge of a screen that
runs from $-1$ to $1$. The closer a thing comes, the bigger it is drawn,
without any limit, until the depth reaches 0.

</details>

## From earlier

**6.** From *Reading an error message*. What does `project(1, 1, 0)` do,
and which line does the traceback point to?

<details class="dl-answer"><summary>answer</summary>

It raises `ZeroDivisionError: division by zero`, and the traceback's
last lines point to `return x / z, y / z`, the line inside `project`
that divides. The line that called it, `project(1, 1, 0)`, is above it
in the traceback. The mistake is in the call, a depth of 0, but Python
reports it where the division failed.

</details>
