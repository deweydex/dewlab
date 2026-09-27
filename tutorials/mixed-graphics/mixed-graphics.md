---
title: "Mixed problems: computer graphics"
practice_across:
  - a-point-on-the-screen
  - a-ball-in-orbit
  - turning-a-cube
  - the-fourth-number
  - your-own-scene
year: "2026-2027"
version: 2026.09.27.1
worlds:
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Mixed problems: computer graphics

These problems move between the pages of the series on purpose, and do
not say which page each one comes from. Choosing the tool is part of
the problem. The first cell loads the tools from [Make it: a scene of
your own](tutorial:your-own-scene), with `project()` from the first
page.

```python exec
id: mixed-graphics-tools
{{include: setup/graphics/scene.py}}


def project(x, y, z):
    return x / z, y / z
```

## 1.

A star is at $(4, 2, 8)$, and the camera is at the origin. Where is it
drawn? Where would it be drawn at $(4, 2, 16)$, twice as far away?

```python exec
id: mixed-graphics-star
```

<details class="dl-hint"><summary>hint</summary>

Divide $x$ and $y$ by the depth, $z$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$4 \div 8 = 0.5$ and $2 \div 8 = 0.25$, so it is drawn at
$(0.5, 0.25)$. At depth 16 it is drawn at $(0.25, 0.125)$: twice as far
away, so half as far from the centre of the picture.
`project(4, 2, 8)` checks it.

</details>

## 2.

The camera steps back along the $z$ axis, and the point stays where it
is. The cell prints the point's screen $x$ for each place the camera
stands.

```python exec
id: mixed-graphics-stepping-back
def project_from(point, camera):
    x, y, z = point
    camera_x, camera_y, camera_z = camera
    depth = z - camera_z
    return (x - camera_x) / depth, (y - camera_y) / depth


for camera_z in [0, -2, -6]:
    print(camera_z, project_from((2, 1, 2), (0, 0, camera_z))[0])
```

```predict
type: number

The point is at $(2, 1, 2)$. What is its screen $x$ when the camera
stands at $z = -6$?
```

With the camera at $-6$, the point is $2 - (-6) = 8$ units ahead, so
its screen $x$ is $2 \div 8 = 0.25$. Stepping back from 2 units to 8
makes it four times smaller.

## 3.

This turn about the vertical axis should keep every shape as it is. At
45°, it squashes every shape onto a flat sheet: look at the new $x$ and
the new $z$ of these three corners. What is wrong with it? Can you
write `rotate_y(angle)`, a 3×3 matrix that turns without flattening?

```python exec
id: mixed-graphics-flattened
def rotate_y_broken(angle):
    c, s = math.cos(angle), math.sin(angle)
    return [[c, 0, s], [0, 1, 0], [s, 0, c]]


corners = [[1, 0, 1],    # x of each corner
           [0, 0, 1],    # y
           [0, 1, 2]]    # z
turned = multiply(rotate_y_broken(math.radians(45)), corners)
print("new x:", [round(v, 2) for v in turned[0]])
print("new z:", [round(v, 2) for v in turned[2]])


def rotate_y(angle):
    """A 3x3 turn about the vertical axis."""
    # Your code here.
```

```hint
Compare the two rows the cell prints. Then compare the broken matrix
with the rotation matrix on the cube page: one sign is missing.
```

```inputs
rotate_y(math.radians(90))
rotate_y(math.radians(45))
```

```solution
def rotate_y(angle):
    """A 3x3 turn about the vertical axis."""
    c, s = math.cos(angle), math.sin(angle)
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
---
The bottom-left sine needs a minus sign. Without it, the new x is c·x + s·z and the new z is s·x + c·z. At 45°, c and s are equal, so the new x and the new z are the same for every point: the two printed rows match, and every point lands on one flat sheet. With the minus sign, the matrix turns z towards x, as the cube page explains.
```

## 4.

To draw a scene with filled shapes, draw the farthest first, so that
nearer ones cover them. Can you write `far_to_near(points)`? `points`
is a list of $(x, y, z)$ tuples, and it returns them from the largest
depth to the smallest.

```python exec
id: mixed-graphics-far-to-near
def far_to_near(points):
    """The points from the farthest to the nearest."""
    # Your code here.
```

```hint
Find the point with the largest z, put it first, and repeat with what
is left. Or look at `sorted()` with a `key=`.
```

```inputs
far_to_near([(0, 0, 3), (1, 1, 9), (2, 0, 5)])
far_to_near([(5, 5, 1)])
far_to_near([(0, 1, 2), (0, 2, 4), (0, 3, 8), (0, 4, 6)])
```

```solution
title: with what you've met so far
def far_to_near(points):
    """The points from the farthest to the nearest."""
    remaining = list(points)
    ordered = []
    while remaining:
        farthest = remaining[0]
        for point in remaining:
            if point[2] > farthest[2]:
                farthest = point
        ordered.append(farthest)
        remaining.remove(farthest)
    return ordered
---
Drawing far to near is the painter's algorithm, from the scene page. A painter paints the far hills first and the near trees last.
```

```solution
title: a shorter way you'll meet later
def far_to_near(points):
    """The points from the farthest to the nearest."""
    return sorted(points, key=lambda point: point[2], reverse=True)
---
`key=` says what to sort by, here the third number of each point, and `reverse=True` puts the largest first.
```

## 5.

A move five units away, and a quarter turn. Does the order matter?

```python exec
id: mixed-graphics-order
move = translation(0, 0, 5)
turn = rotation_y(math.radians(90))
point = [[1], [0], [0], [1]]
turn_first = multiply(chain(move, turn), point)
move_first = multiply(chain(turn, move), point)
print([round(row[0], 3) for row in turn_first])
print([round(row[0], 3) for row in move_first])
print(turn_first == move_first)
```

```predict
type: choice

Will the two orders put the point in the same place? What will the last
line print?

- True
  - A move and a turn feel as though they should add up, whatever the
    order.
- False
```

The last matrix in `chain()` acts first. Turned first, the point swings
from $(1, 0, 0)$ to $(0, 0, -1)$, and then moves out to $(0, 0, 4)$.
Moved first, it goes to $(1, 0, 5)$, and then the turn swings it about
the origin, to $(5, 0, -1)$. Matrix multiplication is not like
ordinary multiplication: the order changes the answer.

## 6.

A camera has $f = 2$. What is its field of view? Is it wider or
narrower than 60°?

```python exec
id: mixed-graphics-field-of-view
```

<details class="dl-hint"><summary>hint</summary>

$f = 1 \div \tan(\text{fov} \div 2)$. Work backwards: what is
$\tan(\text{fov} \div 2)$, and which angle has that tangent?
`math.atan()` finds it, in radians.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$\tan(\text{fov} \div 2) = 1 \div 2 = 0.5$, and
`math.degrees(math.atan(0.5))` is about 26.57°, so the field of view is
about 53.13°. That is narrower than 60°, whose $f$ is about 1.73. A
larger $f$ is a narrower view, like a zoom lens.

</details>

## 7.

Somebody says: "A 3×3 matrix can move the cube five units away, if you
choose its nine numbers carefully." Can it? Try it on one corner,
$(0, 0, 0)$.

```python exec
id: mixed-graphics-origin
```

<details class="dl-answer"><summary>answer</summary>

No. Every 3×3 matrix times $(0, 0, 0)$ gives $(0, 0, 0)$, because every
number in the answer is a sum of numbers times 0. So a 3×3 matrix can
never move the origin, and a move five units away must move it. The
fourth number, the 1 in homogeneous coordinates, is what lets a matrix
add a fixed amount.

</details>

## 8.

After the projection matrix and the divide by $w$, a point's depth is a
number from −1 at the near plane to 1 at the far plane. Can you write
`screen_depth(depth, near, far)`? It returns that number, for a point
straight ahead at `depth`.

```python exec
id: mixed-graphics-screen-depth
def screen_depth(depth, near, far):
    """The depth after projection and the divide by w, from -1 to 1."""
    # Your code here.
```

```hint
Multiply `projection(60, near, far)` by the point `[[0], [0], [depth],
[1]]`, and divide the third number of the result by the fourth. The
field of view does not change the depth, so any angle will do.
```

```inputs
round(screen_depth(1, 1, 20), 6)
round(screen_depth(20, 1, 20), 6)
round(screen_depth(2, 1, 20), 3)
round(screen_depth(10, 1, 20), 3)
```

```solution
def screen_depth(depth, near, far):
    """The depth after projection and the divide by w, from -1 to 1."""
    x, y, z, w = [row[0] for row in multiply(projection(60, near, far), [[0], [0], [depth], [1]])]
    return z / w
---
The near plane gives −1 and the far plane 1. Depth 2, only one step past the near plane, is already at 0.053, past the middle, and depth 10 is at 0.895. Most of the range from −1 to 1 goes to the nearest few units, where a small difference in depth matters most for what hides what.
```

## In your world

Can you write `width_on_screen(points)`? `points` is a list of
$(x, y, z)$ tuples. It projects each one with `project()`, and returns
the distance from the leftmost drawn point to the rightmost.

<div class="dl-world" data-world="starships">

The corners of a starship's hull, 10 units ahead, and the same ship 20
units ahead.

```python exec
id: in-your-world-1--starships
hull = [(-2, 0, 10), (2, 0, 10), (-1, 1, 12), (1, 1, 12), (0, 0, 8)]
far_hull = [(x, y, z + 10) for x, y, z in hull]


def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    # Your code here.
```

```hint
Project each point and keep its screen x. Then take the largest minus
the smallest.
```

```inputs
round(width_on_screen(hull), 4)
round(width_on_screen(far_hull), 4)
```

```solution
title: with what you've met so far
def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    xs = []
    for x, y, z in points:
        screen_x, screen_y = project(x, y, z)
        xs.append(screen_x)
    return max(xs) - min(xs)
---
The hull is 0.4 wide on the screen at 10 units, and 0.2 at 20. Its widest corners are at depth 10, and twice the depth makes them half as wide.
```

```solution
title: a shorter way you'll meet later
def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    xs = [project(x, y, z)[0] for x, y, z in points]
    return max(xs) - min(xs)
```

</div>

<div class="dl-world" data-world="space-scenes">

Four moons in a ring about a planet 10 units ahead, and the same ring
with the planet 5 units ahead.

```python exec
id: in-your-world-1--space-scenes
ring = [(3, 0, 10), (0, 0, 13), (-3, 0, 10), (0, 0, 7)]
near_ring = [(x, y, z - 5) for x, y, z in ring]


def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    # Your code here.
```

```hint
Project each point and keep its screen x. Then take the largest minus
the smallest.
```

```inputs
round(width_on_screen(ring), 4)
round(width_on_screen(near_ring), 4)
```

```solution
title: with what you've met so far
def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    xs = []
    for x, y, z in points:
        screen_x, screen_y = project(x, y, z)
        xs.append(screen_x)
    return max(xs) - min(xs)
---
The ring is 0.6 wide at 10 units, and 1.2 at 5. The two side moons set the width, and halving their depth doubles it.
```

```solution
title: a shorter way you'll meet later
def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    xs = [project(x, y, z)[0] for x, y, z in points]
    return max(xs) - min(xs)
```

</div>

<div class="dl-world" data-world="pixel-art">

The four corners of a flat sprite, 4 units ahead, and the same sprite
tilted so that its right edge is twice as far away.

```python exec
id: in-your-world-1--pixel-art
sprite = [(-1, -1, 4), (1, -1, 4), (1, 1, 4), (-1, 1, 4)]
tilted = [(-1, -1, 4), (1, -1, 8), (1, 1, 8), (-1, 1, 4)]


def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    # Your code here.
```

```hint
Project each point and keep its screen x. Then take the largest minus
the smallest.
```

```inputs
round(width_on_screen(sprite), 4)
round(width_on_screen(tilted), 4)
```

```solution
title: with what you've met so far
def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    xs = []
    for x, y, z in points:
        screen_x, screen_y = project(x, y, z)
        xs.append(screen_x)
    return max(xs) - min(xs)
---
The sprite is 0.5 wide face on, and 0.375 tilted. Only the right edge moved away, so only its half of the width shrank, from 0.25 to 0.125.
```

```solution
title: a shorter way you'll meet later
def width_on_screen(points):
    """The distance from the leftmost projected point to the rightmost."""
    xs = [project(x, y, z)[0] for x, y, z in points]
    return max(xs) - min(xs)
```

</div>
