---
title: "Homogeneous coordinates and the projection matrix — Practice"
practice_for: the-fourth-number
year: "2026-2027"
version: 2026.09.21.1
---

# Homogeneous coordinates and the projection matrix — Practice

Keep track of $w$. In every problem here, ask what the fourth number
is before and after the multiplication, because the trick happens
there.

## Moving by multiplying

```python exec
id: moving-1
{{include: setup/cube.py}}
```

```python exec
id: moving-2
def with_ones(points):
    return points + [[1] * len(points[0])]


def translation(dx, dy, dz):
    return [[1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]]


def divide_by_w(points):
    xs, ys, zs, ws = points
    return [[x / w for x, w in zip(xs, ws)], [y / w for y, w in zip(ys, ws)]]


print(multiply(translation(2, 0, 0), [[1], [1], [1], [1]]))
```

**1.** What does `translation(2, 0, 0)` do to the point $(1, 1, 1, 1)$?
Do the top row of the multiplication by hand.

<details class="dl-answer"><summary>answer</summary>

$(3, 1, 1, 1)$. The top row is $1 \cdot 1 + 0 \cdot 1 + 0 \cdot 1 + 2 \cdot 1 = 3$.
The $2$ came in on the point's fourth number, and the other three rows
pass their own coordinate through unchanged, the last one keeping the
$1$ ready for the next matrix.

</details>

**2.** Multiply `translation(1, 2, 3)` by `translation(4, 5, 6)`. What
matrix do you get, and does the order matter for this pair?

<details class="dl-answer"><summary>answer</summary>

`translation(5, 7, 9)`, in either order. Two moves, one after the other,
make one move by the sum, and addition gives the same answer in either
order.
Translations are one of the few kinds of matrix where the order does
not matter.

```python
print(multiply(translation(1, 2, 3), translation(4, 5, 6)))
print(multiply(translation(4, 5, 6), translation(1, 2, 3)))
```

</details>

**3.** What is the inverse of `translation(1, 2, 3)`? Write it down
without any formula, and check that the product of the two is the
identity.

<details class="dl-answer"><summary>answer</summary>

`translation(-1, -2, -3)`. To undo a move, move back the same
amount. The product is the 4×4 identity matrix.

```python
print(multiply(translation(1, 2, 3), translation(-1, -2, -3)))
```

</details>

## Dividing by w

**4.** Push the point $(2, 1, 4, 1)$ through `simple_projection`, the
matrix whose last row is $0, 0, 1, 0$. What comes out, and what is the
point after dividing by $w$?

<details class="dl-answer"><summary>answer</summary>

$(2, 1, 4, 4)$. The last row copies $z$ into $w$, and nothing else
changes. A division by $w = 4$ gives $(0.5, 0.25)$ on the screen, with
the third and fourth numbers both becoming $1$. That is the same
$(2 / 4, 1 / 4)$ the plain perspective divide would give.

```python
simple_projection = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0]]
print(multiply(simple_projection, [[2], [1], [4], [1]]))
print(divide_by_w(multiply(simple_projection, [[2], [1], [4], [1]])))
```

</details>

## Field of view

```python exec
id: field-of-view-1
def projection(fov_degrees, near, far):
    f = 1 / math.tan(math.radians(fov_degrees) / 2)
    depth_scale = (far + near) / (far - near)
    depth_shift = -2 * far * near / (far - near)
    return [[f, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, depth_scale, depth_shift],
            [0, 0, 1, 0]]


print(round(1 / math.tan(math.radians(45) / 2), 3))
```

**5.** With a field of view of $45°$, where on the screen does the point
$(1, 0, 5)$ land? Compare it with the plain divide, which puts it at
$x = 0.2$.

<details class="dl-answer"><summary>answer</summary>

At $x \approx 0.483$. $f = 1 / \tan(22.5°) \approx 2.414$, and the
screen $x$ is $f \cdot x / z = 2.414 \times 1 / 5 \approx 0.483$. A
$45°$ lens is a narrow one, so everything is drawn about two and a half
times further from the centre than the plain divide puts it.

```python
point = multiply(projection(45, near=1, far=20), [[1], [0], [5], [1]])
print(divide_by_w(point))
```

</details>

**6.** With `near=1` and `far=10`, what converted depth does the middle
of the range, depth $5.5$, come out as? And which depth comes out as
exactly $0$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The third row gives $z' = \text{scale} \cdot z + \text{shift}$, then
   divide by $w = z$.
2. With near 1 and far 10, scale is $11 / 9$ and shift is $-20 / 9$.
3. For the second part, set $\text{scale} \cdot z + \text{shift} = 0$
   and solve for $z$.

**Think about:** why the depth that maps to $0$ is so much nearer than
the middle of the range.

**Try this next:** the same two questions with `near=0.1`.

</details>

<details class="dl-answer"><summary>answer</summary>

Depth $5.5$ comes out as about $0.818$, not $0$. Most of the range
between $-1$ and $1$ has already been used by the time the depth
reaches the middle.

The depth that maps to $0$ is $z = 20 / 11 \approx 1.818$, because
$\frac{11}{9} z - \frac{20}{9} = 0$ there. Half the depth range is
already used less than one unit past the near plane. The conversion
is a divide by $z$, like everything else in this series, so it is
steep near the camera and flat far away.

```python
camera = projection(60, near=1, far=10)
for depth in [1.818, 5.5]:
    x, y, z, w = [row[0] for row in multiply(camera, [[0], [0], [depth], [1]])]
    print(depth, "->", round(z / w, 3))
```

</details>
