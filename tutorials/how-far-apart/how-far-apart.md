---
title: "How far apart? Distance, midpoint and Pythagoras"
year: "2026-2027"
version: 2026.09.26.1
covers:
  straight-across-and-straight-up:
    covers: [MIT-4.3]
    touches: [MIT-4.4]
  squares-on-the-sides-pythagoras:
    covers: [MIT-4.4]
    touches: [MIT-1.2, PDP-LO10]
  the-distance-between-two-points:
    covers: [MIT-4.3, MIT-4.4]
    touches: [PDP-LO8, PDP-LO10]
  halfway-the-midpoint:
    covers: [MIT-4.3]
    touches: [MIT-4.2, PDP-LO10]
  did-the-ball-hit-the-player:
    covers: [MIT-4.3]
    touches: [PDP-LO6, MIT-6.2]
---

# How far apart? Distance, midpoint and Pythagoras

In a 2D game, a ball flies across the screen towards a player. Sixty
times a second, the game has to answer one question: did the ball hit
the player? The game knows where the centre of each one is, and how big
each one is. What else does it need to know?

Pause and guess before you read on. The answer is one number, and
people have known the rule that finds it for about 3,800 years.

On this page we:

- measure a distance straight across, then straight up, then on a slant
- see why Pythagoras' theorem is true, by moving the pieces of a picture
- find the distance between any two points, and add `distance` to the
  toolkit
- find the point halfway between two points, and add `midpoint`
- decide whether two circles in a game touch, and watch a fast ball
  slip through

> **The space we're in.** The same flat plane as on
> [Straight lines](tutorial:straight-lines), with the same unit across
> and up. Here the unit is the pixel, one dot of the screen. One thing
> usually goes unsaid: "how far" means in a straight line, as a bird
> flies. A person walking along streets, or a ball bouncing off walls,
> goes further.

## Warm-up

The first question is from
[Straight lines](tutorial:straight-lines#slope-between-any-two-points),
and the second from
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins#triangles-half-a-rectangle).

```question
id: how-far-warm-up-1
type: fill-in-the-blank

`slope((1, 2), (3, 8))` gives {3}: a rise of 6 over a run of 2.
```

```question
id: how-far-warm-up-2
type: multiple-choice
answer: 1

A triangle has a square corner. The two sides that meet at that corner
are 3 m and 4 m long. What is its area?

- 6 m²
  - Half of 3 × 4: the triangle is half of a 3 m by 4 m rectangle.
- 7 m²
  - This adds the two sides, 3 + 4, which gives a length, not an area.
- 12 m²
  - This is the whole 3 m by 4 m rectangle, and the triangle is half of it.
- 5 m²
  - 5 m is the third side, the long one across from the square corner.
```

## Straight across and straight up

Start with two points on the same row, $(2, 5)$ and $(9, 5)$. Only $x$
changes, so the distance between them is $9 - 2 = 7$. From right to
left the difference is $2 - 9 = -7$, but a distance has no direction, so
we keep its size with `abs()`, from
[How likely is it?](tutorial:how-likely-is-it). The same works for two
points in one column.

Now the game. The player's centre is at $(100, 50)$ and the ball's
centre is at $(130, 90)$. From the player to the ball is 30 pixels
across and 40 pixels up. Going across and then up is 70 pixels. The
straight line from one centre to the other is shorter than that. How
long is it? Make a guess before
you run the cell, which draws the three lines.

```python exec
id: how-far-across-1
import matplotlib.pyplot as plt

player = (100, 50)
ball = (130, 90)
corner = (130, 50)
plt.plot([player[0], corner[0]], [player[1], corner[1]], color="orange", label="across: 30")
plt.plot([corner[0], ball[0]], [corner[1], ball[1]], color="green", label="up: 40")
plt.plot([player[0], ball[0]], [player[1], ball[1]], marker="o", label="straight: ?")
plt.axis("equal")
plt.legend()
```

The three lines make a triangle with a square corner where across meets
up. A square corner is a *right angle*, 90 degrees, and a triangle with
one is a *right-angled triangle*. Its longest side, the one opposite the
right angle, is the *hypotenuse*. The straight line we want is the
hypotenuse.

## Squares on the sides: Pythagoras

You used a rule for this on
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins#wrapping-it-surface-area),
to find the slant of a cone, and that page promised the reason later.
Here it is, as a picture.

Take a right-angled triangle with short sides $a$ and $b$, and
hypotenuse $c$. Make four copies of it, and a square frame with sides
$a + b$. There are two ways to lay the four triangles in the frame:

1. **One in each corner**, turned so that their long sides make a tilted
   square in the middle. The space left over is one square, with side
   $c$.
2. **In two pairs**, each pair making an $a$ by $b$ rectangle, in two
   opposite corners. The space left over is two squares, one with side
   $a$ and one with side $b$.

The cell draws both, with $a = 3$ and $b = 4$. Before you run it, can
you say why the white space in the two pictures must have the same
area?

```python exec
id: how-far-squares-1
first_way = [[(0, 0), (3, 0), (0, 4)], [(3, 0), (7, 0), (7, 3)],
             [(7, 3), (7, 7), (4, 7)], [(4, 7), (0, 7), (0, 4)]]
second_way = [[(4, 0), (7, 0), (7, 4)], [(4, 0), (4, 4), (7, 4)],
              [(0, 4), (4, 4), (4, 7)], [(0, 4), (0, 7), (4, 7)]]

figure, (left, right) = plt.subplots(1, 2, figsize=(8, 4))
for panel, triangles in [(left, first_way), (right, second_way)]:
    panel.plot([0, 7, 7, 0, 0], [0, 0, 7, 7, 0], color="black")
    for corners in triangles:
        panel.add_patch(plt.Polygon(corners, facecolor="lightblue", edgecolor="black"))
    panel.set_aspect("equal")
    panel.axis("off")
```

`plt.Polygon` makes a flat shape from a list of corners, and
`add_patch` puts it on the drawing.

The frame is the same, and so are the four triangles. So whatever is
left over must have the same area in both pictures. On the left it is
$c^2$. On the right it is $a^2 + b^2$. So:

$$c^2 = a^2 + b^2$$

In words: in a right-angled triangle, the square on the hypotenuse is
equal to the two other squares added together. This is *Pythagoras'
theorem*. Nothing in the argument needed $a = 3$ and $b = 4$: it works
for any right-angled triangle. A reason that holds for every case,
like this one, is a *proof*.

Let's check it with numbers. The white space is the frame's area
minus four triangles. `triangle_area` is from your toolkit. Will the two
columns agree for every pair?

```python exec
id: how-far-squares-2
for a, b in [(3, 4), (5, 12), (1, 1), (2.5, 7)]:
    left_over = (a + b) ** 2 - 4 * triangle_area(a, b)
    print(a, b, left_over, a ** 2 + b ** 2)
```

They agree every time, including $a = b = 1$, where the hypotenuse is
$\sqrt{2}$, a number that is not a fraction.

Does the rule hold for every triangle, or only right-angled ones? A
triangle with sides 4, 5 and 6 has no right angle. $4^2 + 5^2 = 41$,
while $6^2 = 36$. The theorem is a promise about right-angled triangles
only, and the square corner is what made the pieces fit in the picture.

## The distance between two points

Now back to the ball. The across and up are the two short sides, so
the straight distance is the square root of $30^2 + 40^2$.

For any two points $(x_1, y_1)$ and $(x_2, y_2)$, the across is
$x_2 - x_1$ and the up is $y_2 - y_1$. So the distance between them is:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

This is the *distance formula*: Pythagoras' theorem, written with
points. A difference may be negative, but its square never is, so the
order of the points does not matter. That is your first tool for this
page.

```python exec
id: how-far-toolkit-distance
toolkit: yes
import math

def distance(p, q):
    """Return the straight-line distance between the points p and q.

    p and q are (x, y) pairs. distance((0, 0), (3, 4)) is 5.0.
    """
    ...
```

```python toolkit-reference
for: how-far-toolkit-distance
import math

def distance(p, q):
    """Return the straight-line distance between the points p and q.

    p and q are (x, y) pairs. distance((0, 0), (3, 4)) is 5.0.
    """
    x1, y1 = p
    x2, y2 = q
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
```

Python has its own version, `math.dist`, which does the same job. The
tests use it as a second opinion. Until your `distance` has its
`return` line, the first test stops with an `AssertionError`. Before
you run them: what is the distance from the player to the ball?

```python exec
id: how-far-toolkit-distance-tests
import math

assert distance((0, 0), (3, 4)) == 5, "the 3, 4, 5 triangle"
assert distance((3, 4), (0, 0)) == 5, "either order"
assert distance((2, 5), (9, 5)) == 7, "on one row"
assert distance((6, 6), (6, 6)) == 0, "a point is 0 from itself"
for p, q in [((1, 2), (5, 4)), ((-3, 7), (2, -1.5)), (player, ball)]:
    assert close_enough(distance(p, q), math.dist(p, q)), (p, q)
print("distance keeps its promise. Player to ball:", distance(player, ball))
```

```hint
Try `print(distance((0, 0), (3, 4)))` on its own. What came back? The
formula has three steps: two differences, their squares added, then a
square root.
```

The ball is 50 pixels from the player, not 70. And one more check,
from [Straight lines](tutorial:straight-lines#the-rule-for-a-ramp): the
hall's new ramp runs 4.5 m along and rises 0.3 m. How long is its
sloping surface? `distance((0, 0), (4.5, 0.3))` gives about 4.51 m,
only 1 cm longer than the run. A gentle slope is almost as long as the
ground under it.

<aside class="dl-note" id="how-far-note-plimpton">

**Older than Pythagoras.** A clay tablet from Babylon, now called
Plimpton 322, was written about 3,800 years ago. It lists two sides
each of fifteen right-angled triangles whose sides are all whole
numbers, such as 119 and 169, whose third side is 120. Pythagoras lived
more than a thousand years later. The theorem carries his name, but people knew
the rule long before him.

</aside>

## Halfway: the midpoint

In a two-player game, the camera has to keep both players on the
screen. One way is to point it at the spot halfway between them. The
players stand at $(2, 1)$ and $(10, 7)$, in metres of the game's world.
Where does the camera point?

Halfway across is the mean of the two $x$ values, and halfway up is the
mean of the two $y$ values, as `mean` on
[What is typical?](tutorial:what-is-typical#share-it-out-equally-the-mean)
shares a total out equally. The *midpoint* of two points is:

$$\left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right)$$

Before you write it, work this one out in your head: where does the
camera point?

```python exec
id: how-far-toolkit-midpoint
toolkit: yes
def midpoint(p, q):
    """Return the point halfway between the points p and q, as an (x, y) pair.

    midpoint((2, 1), (10, 7)) is (6.0, 4.0).
    """
    ...
```

```python toolkit-reference
for: how-far-toolkit-midpoint
def midpoint(p, q):
    """Return the point halfway between the points p and q, as an (x, y) pair.

    midpoint((2, 1), (10, 7)) is (6.0, 4.0).
    """
    x1, y1 = p
    x2, y2 = q
    return ((x1 + x2) / 2, (y1 + y2) / 2)
```

How do we know the point is really halfway? Two things must be true.
It must be the same distance from both ends, half the whole way. And it
must be on the line between them, so the slope from the start to the
midpoint must be the slope of the whole line. The tests check both,
with `slope` from the last page. Until `midpoint` is written, the first
test stops with `AssertionError: None`.

```python exec
id: how-far-toolkit-midpoint-tests
first_player = (2, 1)
second_player = (10, 7)
camera = midpoint(first_player, second_player)
assert camera == (6, 4), camera
assert close_enough(distance(first_player, camera), distance(camera, second_player)), "same from both ends"
assert close_enough(distance(first_player, camera), distance(first_player, second_player) / 2), "half the way"
assert close_enough(slope(first_player, camera), slope(first_player, second_player)), "on the line"
print("midpoint keeps its promise. The camera points at", camera, distance(first_player, camera), "m from each player.")
```

The camera points at $(6, 4)$, 5 m from each player. The two players
are a 6, 8, 10 triangle apart: the 3, 4, 5 triangle made twice as big.
As they move, the game works the midpoint out again every frame.

### Your turn

1. Find the distance from $(-2, 3)$ to $(4, -5)$ on paper first, then
   with `distance`.
2. Find the midpoint of the same two points. Is it the same distance
   from both?
3. A delivery drone flies from $(0, 0)$ to $(9, 12)$ in a straight
   line. A van must follow streets, across and then up. How much
   further does the van go?

## Did the ball hit the player?

Now the game's question. Picture the ball and the player as two
circles. Draw the straight line between their centres. Along that
line, the ball's edge is its radius from its centre, and the player's
edge is the player's radius from theirs. If the centres are further
apart than the two radii added together, there is a gap between the
edges. If not, the circles touch or overlap.

$$\text{touching when} \quad d \le r_1 + r_2$$

Here $d$ is the distance between the centres. The ball has a radius
of 10 pixels and the player 25. They are 50 apart now, and
$10 + 25 = 35$. So not yet.

Each frame, the ball moves 3 pixels left and 4 down, straight at the
player. In which frame do they first touch? Guess, then run it. The
cell uses your `distance`, so write that first.

```python exec
id: how-far-hit-1
def circles_touch(centre_a, radius_a, centre_b, radius_b):
    """Return True when two circles touch or overlap."""
    return distance(centre_a, centre_b) <= radius_a + radius_b

ball_radius = 10
player_radius = 25
for frame in range(6):
    ball_now = (130 - 3 * frame, 90 - 4 * frame)
    gap = distance(ball_now, player)
    print(frame, ball_now, gap, circles_touch(ball_now, ball_radius, player, player_radius))
```

The ball moves 5 pixels closer each frame, since each step is a 3, 4,
5 triangle of its own. In frame 3 the centres are exactly 35 apart,
and the edges just touch. We wrote `<=`, so touching counts as a hit.
A game that wrote `<` would let the ball graze the player. Which is
fairer is a choice about the game, not about the maths.

Here is frame 3 as a picture. `plt.Circle` makes a circle from a centre
and a radius, and `add_patch` puts it on the drawing.

```python exec
id: how-far-hit-2
frame_3 = (121, 78)
figure, axes = plt.subplots()
axes.add_patch(plt.Circle(player, player_radius, color="lightblue"))
axes.add_patch(plt.Circle(frame_3, ball_radius, color="orange"))
axes.plot([player[0], frame_3[0]], [player[1], frame_3[1]], color="black", marker=".")
axes.set_xlim(60, 150)
axes.set_ylim(10, 110)
axes.set_aspect("equal")
```

The two circles meet at one point, on the line between the centres.
Without `set_aspect("equal")`, the circles would be drawn as ovals, the
same stretching that hid the right angle on the last page.

### Watching it frame by frame

The game only looks at the ball once a frame. This animation shows
what it sees: the ball turns red in every frame where `circles_touch`
says it touches the player. After you have watched it, change `step` on
the first line to 90, as if the ball were kicked much harder. Before
you run it again, guess: in which frame does it turn red?

```python exec
id: how-far-hit-3
from matplotlib.animation import FuncAnimation

step = 5     # pixels the ball moves each frame: change it, then run the cell again

figure, axes = plt.subplots(figsize=(3.2, 3.2))
axes.add_patch(plt.Circle(player, player_radius, color="lightblue"))
ball_shape = plt.Circle(ball, ball_radius, color="orange")
axes.add_patch(ball_shape)
axes.set_xlim(40, 160)
axes.set_ylim(-20, 120)
axes.set_aspect("equal")


def draw_frame(frame):
    # Each frame, the ball moves step pixels along the 3, 4, 5 direction.
    ball_now = (130 - 0.6 * step * frame, 90 - 0.8 * step * frame)
    ball_shape.center = ball_now
    if circles_touch(ball_now, ball_radius, player, player_radius):
        ball_shape.set_color("red")
    else:
        ball_shape.set_color("orange")


FuncAnimation(figure, draw_frame, frames=int(110 / step) + 1, interval=200)
```

At 5 pixels a frame, the ball turns red from frame 3 and stays red
while it overlaps the player. At 90 pixels a frame, it never turns red.
In frame 0 it is 50 pixels from the player's centre, and in frame 1 it
is already 40 pixels past it, on the other side. Both are more than 35,
so the game sees no hit, although the ball went straight through. I
think this is the strangest result on the page. Game makers call it
*tunnelling*, and the practice page asks how a game can stop it. The
animation loops; run the cell again to watch it from the start.

### Your turn

1. Make the ball smaller, with a radius of 5. In which frame does it
   touch the player now?
2. A second player stands at $(160, 40)$ with a radius of 20. Is the
   ball, where it starts, touching that player?
3. Change the move to 6 left and 8 down each frame. Which frame is the
   first hit? Is there a frame where the ball is exactly touching?

<details class="dl-why"><summary>Why this way?</summary>

This page proved Pythagoras' theorem by moving four triangles around a
frame, before any code used it.

The usual alternative is to state the theorem, check it on a few
triangles, and use it. That is quicker, and most people who use the
theorem at work have never seen a proof. A second alternative is the
algebra proof, which multiplies out $(a + b)^2$. It needs no picture,
and it uses the brackets of Unit 7.

We chose the picture because a check with numbers only says the rule
worked for the triangles we tried, and a proof says why it works for
all of them. The cost is time, and a picture proof asks you to trust
that the middle shape really is a square.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the hypotenuse $c$ and the short sides $a$ and $b$; a centre and a radius for each circle; a point as an $(x, y)$ pair |
| What is promised? | Pythagoras promises $c^2 = a^2 + b^2$ for every right-angled triangle; `distance` and `midpoint` promise what their docstrings say, checked with `math.dist` and `slope` |
| What happens when? | differences first, then squares, then the square root; each frame, the ball moves and then the game checks for a hit |
| What does this space let us do? | a flat plane with the same unit both ways, where the pieces of the picture fit; a distance as a bird flies, not along streets |

## What we have now

| Term or tool | What it means |
|---|---|
| right angle, right-angled triangle | a square corner of 90 degrees; a triangle with one |
| hypotenuse | the longest side of a right-angled triangle, opposite the right angle |
| Pythagoras' theorem, $c^2 = a^2 + b^2$ | the square on the hypotenuse equals the other two squares added |
| proof | a reason that holds for every case, not only the ones tried |
| distance formula | $d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$ |
| `math.dist(p, q)` | Python's own straight-line distance between two points |
| midpoint | the point halfway between two points: the mean of the $x$ values and of the $y$ values |
| circles touch | when the distance between centres is at most the two radii added |
| tunnelling | a fast object passing through another between two frames, with no hit seen |
| `plt.Polygon`, `plt.Circle`, `add_patch` | draw a shape from its corners, or a circle from its centre and radius |
| `distance(p, q)` | your toolkit tool: how far apart two points are |
| `midpoint(p, q)` | your toolkit tool: the point halfway between two points |

The practice page is next.

## Where to read more

The dewlab page
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances#how-far-apart-and-the-theorem-that-answers-it)
reaches the same theorem from a different direction.
