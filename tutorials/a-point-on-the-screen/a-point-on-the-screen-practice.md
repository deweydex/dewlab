---
title: "Perspective projection: dividing by depth — Practice"
practice_for: a-point-on-the-screen
year: "2026-2027"
version: 2026.09.22.1
---

# Perspective projection: dividing by depth — Practice

Work each one out by hand first, then run it. The arithmetic is one
division, so the practice is in deciding what to divide by what.

## Dividing by Depth

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
depth? What did the divide throw away?

**Try this next:** the same screen point, at depth 3.

</details>

<details class="dl-answer"><summary>answer</summary>

$(2, 1, 10)$: $0.2 \times 10 = 2$ and $0.1 \times 10 = 1$. Without the
depth there is no answer at all. Every point along the line of sight
through $(0.2, 0.1)$ lands on the same pixel, which is exactly what the
divide throws away. At depth 3 the same screen point is $(0.6, 0.3, 3)$.

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
problem 1. Moving the glass further away draws everything twice as big,
which is what a zoom lens does.

</details>
