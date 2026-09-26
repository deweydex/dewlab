---
title: "Make it: your own scene"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Make it: your own scene

This series drew a road of posts with one division, sent a ball round
in a circle, turned a cube with a matrix, and put a whole camera into
one 4×4 matrix. Every picture on those pages was somebody else's shape.
Now you build a scene of your own.

It starts small, with one shape of your own drawn through a camera. Then
three copies of it, placed with matrices. After that it can go as far
as you like: a turntable, a camera that flies, or a picture where the
near lines are drawn over the far ones.

## The tools

This cell holds the tools from the four pages of the series, gathered
in one place. Run it first. A shape is a pair, `(points, edges)`, as the
cube was: three rows of $x$, $y$ and $z$, and a list of which corners
to join.

```python exec
id: your-own-scene-tools
{{include: setup/graphics/scene.py}}
```

Here is what each tool does:

- `translation`, `rotation_x`, `rotation_y`, `rotation_z` and `scaling`
  make 4×4 matrices, as on the fourth page. The rotations take an angle
  in radians, so use `math.radians(30)` for 30°.
- `projection(fov)` is the camera's lens, with a field of view in
  degrees.
- `chain(a, b, c)` multiplies matrices into one. The last one acts
  first, as always.
- `place(shape, matrix)` makes a moved copy of a shape.
- `combine([shape1, shape2])` puts several shapes into one.
- `draw_wireframe(shape, camera)` draws a shape through a camera
  matrix. It leaves out any edge that reaches behind the camera, so it
  never divides by a depth of 0.

## A first step

Here is a pyramid: a square base on the ground and one point on top.
It has 5 corners and 8 edges. The camera matrix works from right to
left. It turns the pyramid 30° on the spot, tips it 20° towards you so
you look down on it, and moves it 7 units away and half a unit down.

```python exec
id: a-first-step-1
pyramid = (
    [[-1, 1, 1, -1, 0],     # x
     [0, 0, 0, 0, 2],       # y
     [-1, -1, 1, 1, 0]],    # z
    [(0, 1), (1, 2), (2, 3), (3, 0),
     (0, 4), (1, 4), (2, 4), (3, 4)],
)
camera = chain(projection(60), translation(0, -0.5, 7),
               rotation_x(math.radians(-20)), rotation_y(math.radians(30)))

plt.figure(figsize=(4, 4))
draw_wireframe(pyramid, camera)
```

Change one corner's numbers and run it again. Then change the shape
into something of your own: your initials, a house, a starship, a
lighthouse. Draw it on squared paper first, and number the corners.
The edges are easier to write once the corners have numbers.

## Make it yours

There are three steps. The first is enough on its own. Go as far as
the time you have allows.

1. **A wireframe of your own.** Your own points and edges, drawn
   through `camera`.
2. **A scene.** Three copies of your shape, each placed with its own
   translation and rotation, drawn through one camera. Choose a field
   of view that fits them all in.
3. **Something more.** A turntable that spins the scene, a camera that
   flies through it, or a picture where near edges are drawn darker and
   thicker than far ones.

Each world below has a shape to start from, if you want one.

<div class="dl-world" data-world="starships">

Here is a lighthouse. It is a tower that narrows as it rises, with a
lamp room on top and a pointed roof. It has 13 corners and 24 edges.

```python exec
id: make-it-yours-1--starships
lighthouse = (
    [[-1, 1, 1, -1, -0.6, 0.6, 0.6, -0.6, -0.7, 0.7, 0.7, -0.7, 0],
     [0, 0, 0, 0, 4, 4, 4, 4, 4.6, 4.6, 4.6, 4.6, 5.4],
     [-1, -1, 1, 1, -0.6, -0.6, 0.6, 0.6, -0.7, -0.7, 0.7, 0.7, 0]],
    [(0, 1), (1, 2), (2, 3), (3, 0),            # the base
     (4, 5), (5, 6), (6, 7), (7, 4),            # the top of the tower
     (0, 4), (1, 5), (2, 6), (3, 7),            # the tower's sides
     (8, 9), (9, 10), (10, 11), (11, 8),        # the lamp room
     (4, 8), (5, 9), (6, 10), (7, 11),
     (8, 12), (9, 12), (10, 12), (11, 12)],     # the roof
)
camera = chain(projection(60), translation(0, -2.5, 10))
plt.figure(figsize=(4, 4))
draw_wireframe(lighthouse, camera)
```

A harbour needs more than one light. Where would you put three of them
along a coast, and how would you turn each one?

</div>

<div class="dl-world" data-world="space-scenes">

Here is a small solar system, with a star and two planets on their
orbits. An orbit is a ring of 36 points, each joined to the next. A body is an
octahedron, 6 corners and 12 edges, like two pyramids base to base.

```python exec
id: make-it-yours-1--space-scenes
def orbit(radius, corners=36):
    xs = [radius * math.cos(2 * math.pi * k / corners) for k in range(corners)]
    zs = [radius * math.sin(2 * math.pi * k / corners) for k in range(corners)]
    edges = [(k, (k + 1) % corners) for k in range(corners)]
    return [xs, [0] * corners, zs], edges


def body(size):
    s = size
    points = [[s, -s, 0, 0, 0, 0], [0, 0, s, -s, 0, 0], [0, 0, 0, 0, s, -s]]
    edges = [(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5),
             (2, 4), (4, 3), (3, 5), (5, 2)]
    return points, edges


system = combine([
    body(0.8),
    orbit(3), place(body(0.3), translation(3, 0, 0)),
    orbit(5), place(body(0.4), chain(rotation_y(math.radians(120)), translation(5, 0, 0))),
])
camera = chain(projection(60), translation(0, 0, 14), rotation_x(math.radians(-25)))
plt.figure(figsize=(4, 4))
draw_wireframe(system, camera)
```

The second planet was moved out 5 units and then turned 120° about the
star, so it sits a third of the way round its orbit. Which matrices would a
moon need, and in which order?

</div>

<div class="dl-world" data-world="pixel-art">

The F from the matrices series, given a depth. The front F and the
back F are the same 10 corners, 1 unit apart, and 10 more edges join
them. That makes 20 corners and 30 edges.

```python exec
id: make-it-yours-1--pixel-art
outline = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]


def extrude(outline, depth=1):
    """A flat outline made solid: a front copy, a back copy, and edges between."""
    n = len(outline)
    xs = [x for x, y in outline] * 2
    ys = [y for x, y in outline] * 2
    zs = [0] * n + [depth] * n
    edges = [(k, (k + 1) % n) for k in range(n)]
    edges = edges + [(n + k, n + (k + 1) % n) for k in range(n)]
    edges = edges + [(k, n + k) for k in range(n)]
    return [xs, ys, zs], edges


letter_f = extrude(outline)
camera = chain(projection(60), translation(-1.5, -2.5, 10), rotation_y(math.radians(30)))
plt.figure(figsize=(4, 4))
draw_wireframe(letter_f, camera)
```

Your initials are outlines too. Can you write the outline of each
letter, extrude it, and place the letters side by side?

</div>

### A scene of three copies

`place` makes a moved copy, and `combine` puts the copies into one
shape. This cell places three pyramids along a line, each turned a
little more than the last:

```python exec
id: a-scene-of-three-copies-1
copies = []
for number, x in enumerate([-3, 0, 3]):
    turn = rotation_y(math.radians(30 * number))
    copies.append(place(pyramid, chain(translation(x, 0, 0), turn)))
scene = combine(copies)

camera = chain(projection(60), translation(0, -1.5, 10))
plt.figure(figsize=(4, 4))
draw_wireframe(scene, camera)
```

Each copy is turned first, about its own centre, and then moved along
the line. Swap the order inside `chain`, and each one swings round the
middle instead. Try a field of view of 30, and then 100. Which fits the
scene best?

### Something more

<details class="dl-hint"><summary>A turntable</summary>

Turn the whole scene a little more in each frame. The turn goes last
in `chain`, so it acts first, while the scene is still centred on the
origin:

```python
from matplotlib.animation import FuncAnimation

figure = plt.figure(figsize=(4, 4))


def draw_step(step):
    plt.cla()
    spin = rotation_y(2 * math.pi * step / 36)
    draw_wireframe(scene, chain(projection(60), translation(0, -1.5, 10), spin))


FuncAnimation(figure, draw_step, frames=36, interval=80)
```

`plt.cla()` clears the picture before each frame is drawn.

</details>

<details class="dl-hint"><summary>A camera that flies</summary>

A camera at `(x, y, z)` sees the world moved by `translation(-x, -y,
-z)`. To fly forwards, start the camera far back and bring it closer in
each frame. When it passes a shape, `draw_wireframe` leaves out the
edges behind it:

```python
figure = plt.figure(figsize=(4, 4))


def draw_step(step):
    plt.cla()
    z = -14 + step * 0.4
    draw_wireframe(scene, chain(projection(70), translation(0, -1, -z)))


FuncAnimation(figure, draw_step, frames=40, interval=80)
```

Can you make the camera turn as it flies? A turn of the camera is the
opposite turn of the world, placed just after the projection.

</details>

<details class="dl-hint"><summary>Near lines in front</summary>

A painter paints the far hills first and the near trees last, so the
trees cover the hills. Drawing works the same way. Find each edge's
depth, the average $w$ of its two ends, sort the edges from far to
near, and draw the near ones darker and thicker:

```python
def draw_by_depth(shape, camera, near=0.1):
    points, edges = shape
    xs, ys, zs, ws = multiply(camera, with_ones(points))
    visible = [(start, end) for start, end in edges if ws[start] >= near and ws[end] >= near]
    visible.sort(key=lambda edge: -(ws[edge[0]] + ws[edge[1]]) / 2)
    nearest = min(ws[start] for start, end in visible)
    for start, end in visible:
        depth = (ws[start] + ws[end]) / 2
        strength = nearest / depth
        plt.plot([xs[start] / ws[start], xs[end] / ws[end]],
                 [ys[start] / ws[start], ys[end] / ws[end]],
                 color=(0, 0, 0, strength), linewidth=3 * strength)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect("equal")


plt.figure(figsize=(4, 4))
draw_by_depth(scene, camera)
```

Drawing far to near is the *painter's algorithm*. With lines it only
changes which line is on top where two cross. With filled faces, it
decides what hides what.

</details>

```python exec
id: something-more-1
```

## On your own, or in a group

**On your own**, make one shape of your own, place three copies of it,
and choose a camera. Then pick one thing from "Something more".

**In a group**, each person makes one shape. Agree first on what one
unit is, a metre say, and where the ground is, $y = 0$, so that the
shapes fit together. Then one person puts them into one scene with
`combine`, and one camera looks at it all. `combine` adds the number of
corners already in the scene to every edge of the next shape, so the
edges still join the right corners.

## Looking back

Show your scene to somebody, or write a few lines for yourself:

- Which step took you longest: the corners, the edges, or placing the
  copies? Why do you think that was?
- When you swapped the order of a turn and a move, what did you expect,
  and what happened?
- Where in your scene does the picture look least like the real thing?
  What would it take to fix it?
- If you worked in a group, what did you have to agree on before the
  shapes fitted together?
