---
title: "How far apart? Distance, midpoint and Pythagoras — Practice"
practice_for: how-far-apart
year: "2026-2027"
version: 2026.09.26.1
---

# How far apart? Distance, midpoint and Pythagoras — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another way** means reach the same place by a second
route. The answers are folded away until you open them. Each is one
answer, and yours may be different and work too.

Your toolkit is loaded on this page, including `distance` and
`midpoint` from the tutorial and `slope` from
[Straight lines](tutorial:straight-lines). `math` is not loaded. Each
cell that needs it starts with `import math`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: how-far-practice-warm-up
import math
# Try things here
```

**1. Predict.** What does each line print?

```python
print(distance((1, 1), (4, 5)))
print(midpoint((0, 0), (8, 2)))
print(distance((-2, 0), (3, 0)))
```

<details class="dl-answer"><summary>answer</summary>

`5.0`, `(4.0, 1.0)` and `5.0`.

From $(1, 1)$ to $(4, 5)$ is 3 across and 4 up, the 3, 4, 5 triangle
again. The midpoint of $(0, 0)$ and $(8, 2)$ is halfway in each
direction. From $-2$ to 3 on one row is 5. If we square the difference and then
take the square root, we get its size, with no sign.

</details>

**2. Make.** A football pitch in a big stadium is often 105 m long and
68 m wide. How far is it from one corner flag to the opposite corner
flag, in a straight line?

<details class="dl-answer"><summary>answer</summary>

```python
print(distance((0, 0), (105, 68)))
```

About 125.1 m. The two sides of the pitch meet at a right angle at
every corner, so the diagonal is the hypotenuse:
$\sqrt{105^2 + 68^2} = \sqrt{15649}$.

</details>

**3. Explain.** A carpenter checks that the corner of a new room is
square like this. She marks a point 3 m along one wall and a point 4 m
along the other, and measures between the marks. If it is exactly 5 m,
she knows the corner is a right angle. Why does this work? What would a
measurement of 4.8 m tell her?

<details class="dl-answer"><summary>answer</summary>

Pythagoras says that a right angle makes $3^2 + 4^2 = 5^2$. The
carpenter uses it the other way round. If the sides are 3, 4 and 5, the
corner must be a right angle. That rule is true too,
though the tutorial did not prove it.

A measurement of 4.8 m is less than 5, so the walls lean in towards
each other, and the corner is smaller than a right angle. More than 5 m
would mean the corner is too wide. A wall is not a grid on a page, but
the maths is the same.

</details>

**4. Predict.** A circle has its centre at $(0, 0)$ and a radius of 5.
Is the point $(3, 4)$ inside it, outside it, or on its edge? What does
this print?

```python
print(distance((0, 0), (3, 4)) <= 5)
print(distance((0, 0), (3, 4.1)) <= 5)
```

<details class="dl-answer"><summary>answer</summary>

`True` and then `False`.

$(3, 4)$ is exactly 5 from the centre, so it is on the edge, and `<=`
counts the edge as in. $(3, 4.1)$ is about 5.08 from the centre, just
outside.

</details>

## Core

A cell for the core problems.

```python exec
id: how-far-practice-core
import math
# Your working for problems 5 to 12
```

**5. Make.** A television is sold as "55 inch". That is the length of
its diagonal. Its screen has the shape 16:9: 16 units wide for every 9
units high. How wide and how high is the screen, in inches and in
centimetres? (1 inch is 2.54 cm.)

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A 16 by 9 screen has a diagonal of `distance((0, 0), (16, 9))`.
2. The real screen is that shape, made bigger. How many times bigger,
   to make the diagonal 55?
3. Multiply 16 and 9 by that number.

**Think about:** why must the width, the height and the diagonal all
grow by the same amount?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
small_diagonal = distance((0, 0), (16, 9))
times_bigger = 55 / small_diagonal
width = 16 * times_bigger
height = 9 * times_bigger
print(round(small_diagonal, 2), round(times_bigger, 3))
print(round(width, 1), round(height, 1), "inches")
print(round(width * 2.54, 1), round(height * 2.54, 1), "cm")
print(distance((0, 0), (width, height)))
```

A 16 by 9 screen has a diagonal of about 18.36, so the real screen is
about 2.996 times bigger. It is about 47.9 inches wide and 27.0 inches
high, or about 121.8 cm by 68.5 cm. The last line puts the answer back
in to check it. The diagonal comes out as `55.0`.

</details>

**6. Fix.** Schlomo, who is learning Python too, wrote his own
`distance`. Run it, see which test fails, and change it so both pass.

```python exec
id: how-far-practice-fix-distance
def distance_again(p, q):
    """Return the straight-line distance between the points p and q."""
    x1, y1 = p
    x2, y2 = q
    return (x2 - x1) ** 2 + (y2 - y1) ** 2

assert distance_again((0, 0), (0, 1)) == 1, "one step up"
assert distance_again((0, 0), (3, 4)) == 5, "the 3, 4, 5 triangle"
print("distance_again keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The second test fails. `distance_again((0, 0), (3, 4))` gives 25. The
function stops at $c^2$ and never takes the square root. The fix:

```python
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
```

with `import math` at the top of the cell. The first test passed
because $1^2 = 1$ and $\sqrt{1} = 1$. For a distance of 1, it makes no
difference whether we take the square root. Schlomo chose the smallest test he could think
of, and it happened to be that one length.

</details>

**7. Another way.** In the tutorial's first picture of Pythagoras, the
tilted square has corners at $(3, 0)$, $(7, 3)$, $(4, 7)$ and
$(0, 4)$. Find its area a second way: measure one side with
`distance`, and square it. Then check that all four sides are the same
length.

<details class="dl-answer"><summary>answer</summary>

```python
tilted = [(3, 0), (7, 3), (4, 7), (0, 4)]
side = distance(tilted[0], tilted[1])
print(side, side ** 2)
for position in range(4):
    print(distance(tilted[position], tilted[(position + 1) % 4]))
```

Each side is 5.0, so the area is 25, the same as the white space the
tutorial found by taking four triangles away from the frame. The
`% 4` makes the last corner join back to the first, as `%` gave the
remainder on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).

</details>

**8. Make.** Ladder safety guidance uses a "1 in 4" rule: the foot of a
ladder should be 1 m out from the wall for every 4 m of height it
reaches. A ladder must reach a gutter 6 m up. How far out from the wall
does its foot go, and how long must the ladder be?

<details class="dl-answer"><summary>answer</summary>

```python
height = 6
out_from_wall = height / 4
print(out_from_wall, distance((0, 0), (out_from_wall, height)))
```

The foot goes 1.5 m out, and the ladder must be at least about 6.18 m
long. The wall and the ground meet at a right angle, so the ladder is
the hypotenuse. In practice it should also reach about 1 m above the
gutter, so a person has something to hold.

</details>

**9. Predict.** A delivery drone flies from its base to a drop point,
but stops at a charging pad on the way. The map is in kilometres. What
do these two lines print? Which is bigger?

```python
base, charger, drop_point = (0, 0), (6, 8), (12, 0)
print(distance(base, drop_point))
print(distance(base, charger) + distance(charger, drop_point))
```

<details class="dl-answer"><summary>answer</summary>

`12.0` and `20.0`.

The trip by the charger is two 6, 8, 10 triangles, 10 km each. A trip
that stops somewhere off the straight line is always longer than the
straight line. It can only be as short when the charger is on the line
itself.

</details>

**10. Explain.** On the tutorial's first row, $(9, 5)$ to $(2, 5)$, we
needed `abs()` to turn $-7$ into 7. Why does `distance` never need
`abs()`, even when a difference is negative?

<details class="dl-answer"><summary>answer</summary>

`distance` squares each difference before it adds them. A negative
number times itself is positive: $(-7)^2 = 49$, the same as $7^2$. So
the sign is gone before the square root, and `math.sqrt` returns the
positive root. If you square a number and then take the square root,
you get its size: `math.sqrt((-7) ** 2)` is `7.0`.

</details>

**11. Make.** A campus map is marked in metres. The library's Wi-Fi
router is at $(100, 40)$ and the sports hall's is at $(340, 220)$. A
relay antenna goes halfway between them, to pass the signal along.
Where is it, and how far is it from each router?

<details class="dl-answer"><summary>answer</summary>

```python
library_router = (100, 40)
hall_router = (340, 220)
relay = midpoint(library_router, hall_router)
print(relay, distance(relay, library_router), distance(relay, hall_router))
```

The relay goes at $(220, 130)$, 150 m from each router. The routers
are 240 m across and 180 m up from each other, which is the 3, 4, 5
triangle made 60 times bigger, so they are 300 m apart.

</details>

**12. Fix.** This version of `midpoint` passes its first test and fails
its second. What does it do with the second pair of points, and what
needs to change?

```python exec
id: how-far-practice-fix-midpoint
def midpoint_again(p, q):
    """Return the point halfway between the points p and q."""
    x1, y1 = p
    x2, y2 = q
    return (x1 + x2 / 2, y1 + y2 / 2)

assert midpoint_again((0, 0), (4, 4)) == (2, 2), "from the origin"
assert midpoint_again((2, 1), (10, 7)) == (6, 4), "the two players"
print("midpoint_again keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The second test fails. It gives `(7.0, 4.5)`. Division comes before
addition, as on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#which-comes-first),
so `x1 + x2 / 2` halves only `x2`. Brackets make Python add
first:

```python
    return ((x1 + x2) / 2, (y1 + y2) / 2)
```

The first test passed because its first point is $(0, 0)$. It makes no
difference whether 0 is added before or after the halving. Tests that start at
the origin miss many slips like this one.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: how-far-practice-stretch
import math
import random
# Your working for problems 13 to 16
```

**13. Make.** In the game, the right-hand wall of the screen is the
vertical line $x = 300$. A ball of radius 10 starts with its centre at
$(200, 150)$ and moves 12 pixels right each frame. The distance from
the ball's centre to the wall is `abs(300 - x)`. In which frame does
the ball first touch the wall? By how much does it overlap then?

<details class="dl-answer"><summary>answer</summary>

```python
ball_radius = 10
for frame in range(12):
    x = 200 + 12 * frame
    gap = abs(300 - x)
    if gap <= ball_radius:
        print("frame", frame, "centre at x =", x, "overlap", ball_radius - gap)
        break
```

In frame 8, the centre is at $x = 296$, only 4 pixels from the wall.
So the ball overlaps it by 6 pixels. In frame 7 the centre was at 284, 16
pixels away. A real game would push the ball back out and turn it
round. The distance to a wall that goes straight up is only the
across part, because the shortest way from a point to that wall is
flat, at a right angle to it.

</details>

**14. Another way.** Games check for hits many thousands of times a
second, and a square root is slow next to a multiplication. So games
often compare squares instead: two circles touch when
$(x_2 - x_1)^2 + (y_2 - y_1)^2 \le (r_1 + r_2)^2$. Write
`touch_without_root` like that, and check that it agrees with a version
that uses `distance`, on 10,000 random pairs of circles.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the version with `distance` first, as in the tutorial.
2. Write the new version with no `math.sqrt` in it.
3. In a loop, make random centres and radii with `random.randint`, and
   `assert` the two versions agree.

**Think about:** why is it safe to square both sides? Would it be safe
if one side could be negative?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def touch_with_root(centre_a, radius_a, centre_b, radius_b):
    """Return True when two circles touch or overlap."""
    return distance(centre_a, centre_b) <= radius_a + radius_b

def touch_without_root(centre_a, radius_a, centre_b, radius_b):
    """Return True when two circles touch or overlap, with no square root."""
    x1, y1 = centre_a
    x2, y2 = centre_b
    return (x2 - x1) ** 2 + (y2 - y1) ** 2 <= (radius_a + radius_b) ** 2

hits = 0
for trial in range(10000):
    centre_a = (random.randint(0, 200), random.randint(0, 200))
    centre_b = (random.randint(0, 200), random.randint(0, 200))
    radius_a = random.randint(1, 50)
    radius_b = random.randint(1, 50)
    same = touch_with_root(centre_a, radius_a, centre_b, radius_b)
    assert same == touch_without_root(centre_a, radius_a, centre_b, radius_b)
    if same:
        hits = hits + 1
print("They agree every time.", hits, "of the pairs touched.")
```

They agree on every pair. The number of hits changes from run to run,
since the circles are random. We can square both sides here because
both sides are 0 or more. For numbers that are not negative, the bigger
one always has the bigger square. That would not be true if a side
could be negative, since $-6 < 5$ but $36 > 25$.

</details>

**15. Explain.** Schlomi, who is learning Python too, is making a game.
Her players can shoot very fast, and she tests a ball fired straight
through the middle of another player. The ball has a radius of 10, the
player 25, and the player's centre is at $(0, 0)$. Run this. What did
the game miss, and how could it stop missing it? The tutorial's last
animation showed the same thing.

```python
for frame in range(3):
    ball_now = (-60 + 100 * frame, 0)
    print(frame, ball_now, distance(ball_now, (0, 0)) <= 10 + 25)
```

<details class="dl-answer"><summary>answer</summary>

It prints `False` three times. In frame 0 the ball is 60 pixels away,
too far to touch. In frame 1 it is 40 pixels away on the other side,
still too far. Between the two frames it passed right through the
player, but the game only checks where the ball is at each frame, not
where it went in between. This is tunnelling. In frame 2 the ball has
gone. Schlomi's test found the case her checker misses.

One fix is to move a fast ball in smaller steps, and check after each
one. Another is to check the whole straight path between the two
frames. Here, the path from $(-60, 0)$ to $(40, 0)$ passes through
$(0, 0)$, so it must hit. The first is simple and costs time. The
second is exact and needs more maths. These are two ways, and yours
may be a third.

</details>

**16. Explain.** The tutorial proved Pythagoras' theorem with a
picture of four triangles in a frame, before any code used it. Many
courses only state the theorem, check it on a few triangles, and then
use it. Which way would you have wanted, and why? There is no
single answer.

<details class="dl-answer"><summary>answer</summary>

An answer might weigh a few things, and can choose either way.

- **Time.** Stating and checking is quicker, and leaves more time to
  use the theorem.
- **What a check can say.** A check on a few triangles says the rule
  worked for those. A proof says why it must work for every
  right-angled triangle.
- **What you remember.** Some people remember a picture long after the
  formula has gone, and can rebuild the formula from it.
- **Trust in pictures.** A picture proof asks you to trust that the
  middle shape really is a square. Problem 7 checked it with
  `distance`, but that is a check, not a proof.
- **You.** Some people want the reason before they will use a rule.
  Others are happy to use it first and ask why later.

You might also want a proof for a rule this important, and only a
check for smaller ones.

</details>

<aside class="dl-note" id="how-far-practice-note-garfield">

**A president's proof.** In 1876, James Garfield, then a member of the
US Congress, published a proof of Pythagoras' theorem of his own. It
uses a trapezium made of three right-angled triangles. Five years
later he became the 20th President of the United States.

</aside>
