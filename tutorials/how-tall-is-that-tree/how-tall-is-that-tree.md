---
title: "Solving triangles: how tall is that tree?"
year: "2026-2027"
version: 2026.09.26.1
covers:
  naming-the-sides-from-one-angle:
    covers: [MIT-4.9]
  how-tall-is-that-tree:
    covers: [MIT-4.9]
  going-backwards-from-sides-to-an-angle:
    covers: [MIT-4.9]
    touches: [MIT-3.1, MIT-1.7]
  area-from-two-sides-and-the-angle-between:
    covers: [MIT-4.8]
  the-cosine-rule:
    covers: [MIT-4.10]
  a-tool-for-the-angle-at-a-corner:
    covers: [MIT-4.10]
    touches: [PDP-LO8, PDP-LO10]
  the-sine-rule-when-you-cannot-reach-the-tree:
    covers: [MIT-4.10]
---

# Solving triangles: how tall is that tree?

There is a tall beech tree in the park. You cannot climb it, and no tape
measure reaches the top. But you can walk to it, and you can look up at
it. Is that enough to find its height? Guess before you read on.

It is. A distance and an angle make a triangle, and a triangle with
enough known parts can tell us the rest. Later on this page, the same
moves explain how light is trapped inside a glass cable.

On this page we:

- name the three sides of a right-angled triangle from one of its angles
- find the tree's height from a distance and an angle
- go backwards, from two sides to an angle, and find a bearing on a map
- follow a ray of light into water, with Snell's law
- find a triangle's area from two sides and the angle between them
- solve triangles with no right angle, with the cosine rule and the sine
  rule
- add `angle_between` to the toolkit

> **The space we're in.** A flat plane, with points as `(x, y)` tuples.
> We say angles in degrees, and Python's `math` works in radians, as on
> [Going round in circles](tutorial:going-round-in-circles). On a flat
> plane, a triangle's three angles add up to 180°. On
> [a ball](tutorial:going-round-in-circles#triangles-on-a-ball) they
> do not. One thing usually goes unsaid: a person measured every angle
> and distance here, so every answer is only as good as the measuring.

## Warm-up

The first question is from
[How far apart?](tutorial:how-far-apart), and the second from
[Going round in circles](tutorial:going-round-in-circles).

```question
id: how-tall-warm-up-1
type: fill-in-the-blank

A right-angled triangle has short sides of 6 m and 8 m. Its longest
side, the hypotenuse, is {10} m.
```

```question
id: how-tall-warm-up-2
type: multiple-choice
answer: 3

A point goes round a circle of radius 1, starting at $(1, 0)$. After it
has turned through an angle $\theta$, where is it?

- $(\theta, 1)$
  - This uses the angle as a distance; the point stays on a circle of radius 1.
- $(\sin\theta, \cos\theta)$
  - Sine and cosine the other way round: at θ = 0 this gives (0, 1), not the start, (1, 0).
- $(\cos\theta, \sin\theta)$
  - Across is cos θ and up is sin θ, and at θ = 0 it is (1, 0), where the point starts.
- $(1, \tan\theta)$
  - This is where the angle's line meets the upright line x = 1, outside the circle.
```

## Naming the sides from one angle

Stand 20 m from the tree and look up at the top. Three lines make a
triangle: a level line from your eyes to the trunk, the trunk above
that line, and your line of sight. The trunk meets the level line at a
right angle.

On [Going round in circles](tutorial:going-round-in-circles), a point
turned round a circle, and its x and y came from the cosine and the
sine. A right-angled triangle is a piece of that picture: your line of
sight is a radius, and the tree is the point's height. The cell draws
it with `point_on_circle` from your toolkit.

```python exec
id: how-tall-sides-1
import math
import matplotlib.pyplot as plt

sight_line = 10          # any length works: the shape is what matters
angle_up = 35            # degrees, from the ground up to the top
top = point_on_circle(sight_line, angle_up)

circle_x = []
circle_y = []
for degrees in range(0, 91):
    x, y = point_on_circle(sight_line, degrees)
    circle_x.append(x)
    circle_y.append(y)

plt.plot(circle_x, circle_y, color="lightgrey")
plt.plot([0, top[0], top[0], 0], [0, 0, top[1], 0], marker="o")
plt.text(top[0] / 2, -0.8, "adjacent", ha="center")
plt.text(top[0] + 0.2, top[1] / 2, "opposite")
plt.text(top[0] / 2 - 0.5, top[1] / 2 + 0.5, "hypotenuse", ha="right")
plt.text(1.2, 0.2, "35°")
plt.gca().set_aspect("equal")
print(top)
```

The top corner sits on the circle. We name the sides from the 35° angle
at your eye:

- the hypotenuse, from
  [How far apart?](tutorial:how-far-apart#squares-on-the-sides-pythagoras),
  is the longest side, across from the right angle: your line of sight;
- the *opposite* side is the side across the triangle from the angle:
  the tree;
- the *adjacent* side is the short side that touches the angle: the
  level line.

From the treetop, the names would swap.

The adjacent side is the point's x, the hypotenuse times the cosine. The
opposite side is its y, the hypotenuse times the sine. And the
[tangent](tutorial:going-round-in-circles#a-third-name-tangent) was
rise over run: in the triangle, opposite over adjacent.

Will the three ratios match `math.sin`, `math.cos` and `math.tan`?

```python exec
id: how-tall-sides-2
adjacent = top[0]
opposite = top[1]
hypotenuse = sight_line
angle = math.radians(angle_up)

print(opposite / hypotenuse, math.sin(angle))
print(adjacent / hypotenuse, math.cos(angle))
print(opposite / adjacent, math.tan(angle))
```

They match, perhaps apart from the last digit. Change `sight_line` to 3
or 500, and the ratios stay the same: the shape decides them, not the
size. People remember them with one made-up word, SOH-CAH-TOA:

| Letters | In words | In symbols |
|---|---|---|
| SOH | sine is opposite over hypotenuse | $\sin\theta = \frac{\text{opp}}{\text{hyp}}$ |
| CAH | cosine is adjacent over hypotenuse | $\cos\theta = \frac{\text{adj}}{\text{hyp}}$ |
| TOA | tangent is opposite over adjacent | $\tan\theta = \frac{\text{opp}}{\text{adj}}$ |

## How tall is that tree?

You stand 20 m from the trunk. A phone app that measures angles says the
top of the tree is 35° above level, and your eyes are about 1.6 m above
the ground. Guess the tree's height before you run anything.

We know the adjacent side, 20 m, and want the opposite side, the tree
above your eyes. TOA holds both. In words: the height above your eyes is
the distance times the tangent of the angle.

$$\text{height} = 20 \times \tan 35^\circ + 1.6$$

```python exec
id: how-tall-tree-1
distance_to_trunk = 20
angle_up = 35
eye_height = 1.6

above_eyes = distance_to_trunk * math.tan(math.radians(angle_up))
print(round(above_eyes, 2), round(above_eyes + eye_height, 2))
```

The tree is about 15.6 m tall. The angle you look up at is called the
*angle of elevation*: the angle between level ground and your line of
sight to something above you.

How close is that? A phone held by hand can be off by 2° or so. Here
is the same sum for 33° and for 37°:

```python exec
id: how-tall-tree-2
for measured in [33, 35, 37]:
    height = distance_to_trunk * math.tan(math.radians(measured)) + eye_height
    print(measured, "degrees gives", round(height, 1), "m")
```

The answer moves from 14.6 m to 16.7 m. The maths is exact, and the
measuring is not, so "about 15 or 16 metres" is the honest answer.

### Your turn

1. A friend stands further back, 32 m from the trunk, and measures 25°.
   Why is their angle smaller than yours?
2. Work out the height from their measurement. Is it the same tree,
   roughly?

```python exec
id: how-tall-tree-your-turn
# Your friend's measurement
```

## Going backwards: from sides to an angle

The Spire on O'Connell Street in Dublin is 120 m tall. Standing 100 m
from its base, how far up do you tilt your head?

Now we know the tangent, $\frac{120}{100} = 1.2$, and want the angle.
That is the tangent run backwards: its inverse, as on
[Machines that take a number](tutorial:machines-that-take-a-number#running-it-backwards-the-inverse).
Python calls it `math.atan`. The inverses of sine and cosine are
`math.asin` and `math.acos`. All three answer in radians, and
`math.degrees` turns that into degrees. More or less than 45°?

```python exec
id: how-tall-back-1
print(math.degrees(math.atan(120 / 100)))
print(math.degrees(math.atan(1 / 10)))
```

About 50°: more than 45°, because the Spire is taller than you are far
from it. The second line is the hall's ramp from
[Straight lines](tutorial:straight-lines#how-steep-is-a-ramp), a slope
of 1:10. Its angle is under 6°, and still too steep for a ramp that
long.

### Bearings

A walker in the Wicklow mountains has a map with a grid in kilometres.
The car park is at $(0, 0)$, and the summit is 3 km east and 4 km north,
at $(3, 4)$. Which way should she face?

A *bearing* is a direction given as an angle, measured clockwise from
north, from 0° up to 360°. North is 0°, east is 90°, south is 180° and
west is 270°.

The tangent of the angle from north is east over north, $\frac{3}{4}$.
But a summit to the south-west, at $(-3, -4)$, gives $\frac{-3}{-4}$,
the same fraction: the division threw away the signs.
`math.atan2(y, x)` takes the two sides separately and keeps their
signs, so it works in any direction. Maths measures angles from east,
anticlockwise: `atan2(north, east)`. A bearing is measured from north,
clockwise. Swapping the two inputs, `atan2(east, north)`, makes both
changes at once. Predict each bearing, then run it.

```python exec
id: how-tall-back-2
def bearing(start, end):
    """Return the bearing from start to end, in degrees from 0 up to 360.

    start and end are (x, y) points, with x to the east and y to the north.
    """
    east = end[0] - start[0]
    north = end[1] - start[1]
    return math.degrees(math.atan2(east, north)) % 360


car_park = (0, 0)
for summit in [(3, 4), (-3, -4), (4, 0), (-2, 2)]:
    print(summit, round(bearing(car_park, summit), 1))
```

The first summit is on a bearing of 36.9°, and the second on 216.9°,
exactly 180° more: the opposite direction. `atan2` gives angles from
−180° to 180°, and `% 360` moves the negative ones round to the 0° to
360° of a compass. With `distance` from your toolkit, a map gives a
walker both things: how far, and which way.

### Light that bends: Snell's law

Put a straw in a glass of water, and it looks broken at the surface:
light changes direction as it passes from water into air. This bending
is called *refraction*.

Each clear material has a *refractive index*, $n$: how many times more
slowly light travels in it than in empty space. Air is about 1.00,
water about 1.33, and glass about 1.5. The angles are measured from the
*normal*, a line at right angles to the surface. *Snell's law* says

$$n_1 \sin\theta_1 = n_2 \sin\theta_2$$

In words: the index times the sine of the angle is the same on both
sides of the surface. Sunlight meets a pond at 40° from the normal. At
what angle does it go on in the water? Make $\sin\theta_2$ the subject,
then `math.asin` goes back to the angle, as `math.atan` did for the
Spire. More than 40°, or less?

```python exec
id: how-tall-snell-1
def refracted_angle(angle_in, n_from, n_to):
    """Return the angle from the normal, in degrees, after light crosses into a new material.

    Gives back None when no light gets through: total internal reflection.
    """
    sine_out = n_from * math.sin(math.radians(angle_in)) / n_to
    if sine_out > 1:
        return None
    return math.degrees(math.asin(sine_out))

print(refracted_angle(40, 1.00, 1.33))   # air into water
print(refracted_angle(40, 1.33, 1.00))   # water up into air
print(refracted_angle(60, 1.33, 1.00))
```

Going into the water, the ray bends towards the normal, to 28.9°. From
water up into air, it bends away from it, to 58.7°. And at 60° there is
no answer: the sine would have to be 1.15, and no angle has a sine
above 1. The light cannot get out, and all of it reflects back into the
water. This is *total internal reflection*, and the angle where it
starts is the *critical angle*. For water into air it is
`math.degrees(math.asin(1 / 1.33))`, about 48.8°.

The cell draws a lamp at the bottom of a pool, shining up at the
surface at `angle_in` from the normal. Run it at 40, then at 48, then
at 50. What do you expect to see at 50?

```python exec
id: how-tall-snell-2
angle_in = 40        # degrees from the normal: change it, then run again

angle_out = refracted_angle(angle_in, 1.33, 1.00)
plt.figure(figsize=(4, 3))
plt.axhspan(-1.2, 0, color="lightblue")                   # the water
plt.plot([0, 0], [-1.2, 1.2], "--", color="grey")         # the normal
plt.text(0.5, -1.0, "water")
plt.text(0.5, 1.0, "air")
lamp = point_on_circle(1, 270 - angle_in)
plt.plot([lamp[0], 0], [lamp[1], 0], color="orange", linewidth=2)
if angle_out is None:
    back_down = point_on_circle(1, 270 + angle_in)
    plt.plot([0, back_down[0]], [0, back_down[1]], color="orange", linewidth=2)
    plt.title("all of it reflects")
else:
    into_air = point_on_circle(1, 90 - angle_out)
    plt.plot([0, into_air[0]], [0, into_air[1]], color="orange", linewidth=2)
    plt.title("out at " + str(round(angle_out, 1)) + " degrees")
plt.gca().set_aspect("equal")
plt.axis("off")
```

At 48° the ray leaves almost flat along the surface, at 81.3°. Two
degrees more, and the surface becomes a mirror. I think that sudden
change is the most surprising thing on this page.

An *optical fibre* is a thread of glass about as thin as a hair, inside
a layer of glass whose index is a little lower. Light sent along it
meets the side past the critical angle, so none gets out, even round
gentle bends. Most of the data that travels between countries goes
this way, as flashes of light in cables under the sea.

<aside class="dl-note" id="how-tall-note-snell">

**Older than Snell.** Willebrord Snellius, a Dutch mathematician, found
the law in 1621 but never published it. In 984, the Persian scholar Ibn
Sahl had already written it down, in a book on burning mirrors and
lenses. René Descartes published it in 1637, and in France it is
called the Snell-Descartes law.

</aside>

## Area, from two sides and the angle between

Three phone masts stand at the corners of a triangle. A phone inside
it can be located from all three, a way of finding a position called
*triangulation*. Two sides of the triangle are 3.0 km and 2.5 km, and
the angle between them is 70°. How much ground lies inside?

On [Measuring rooms and tins](tutorial:measuring-rooms-and-tins), a
triangle's area was half the base times the height. Nobody measured the
height here. Picture the 3.0 km side along the bottom. The height is the
line straight down from the top corner, the opposite side of a small
right-angled triangle whose hypotenuse is the 2.5 km side. By SOH, the
height is $2.5 \times \sin 70^\circ$.

In words: the area is half of one side, times the other side, times the
sine of the angle between them. With sides $a$ and $b$ and the angle $C$
between them:

$$\text{area} = \tfrac{1}{2}ab\sin C$$

Will it agree with your toolkit's `triangle_area(base, height)`?

```python exec
id: how-tall-area-1
side_a = 3.0     # km
side_b = 2.5     # km
angle_c = 70

height = side_b * math.sin(math.radians(angle_c))
print(triangle_area(side_a, height))
print(0.5 * side_a * side_b * math.sin(math.radians(angle_c)))
```

Both give about 3.52 square kilometres. It is the old formula, with the
height worked out from what we measured.

## The cosine rule

Most triangles have no right angle. From where you stand by a lake, one
end of it is 300 m away and the other end is 250 m away, and the angle
between the two directions is 70°. How long is the lake?

For a right angle,
[Pythagoras](tutorial:how-far-apart#squares-on-the-sides-pythagoras)
says $c^2 = a^2 + b^2$. Other angles need a correction, which uses the
cosine. In words: the third side squared is the other two squared and
added, minus twice their product times the cosine of the angle between
them.

$$c^2 = a^2 + b^2 - 2ab\cos C$$

This is the *cosine rule*. At 90°, $\cos C = 0$, so the correction is 0
and Pythagoras is left. The cell checks the rule by putting the lake on
a map: you at $(0, 0)$, one end due east, the other on a circle of
radius 250 at 70°. Will the two numbers agree?

```python exec
id: how-tall-cosine-1
you = (0, 0)
near_end = (300, 0)
far_end = point_on_circle(250, 70)

by_rule = math.sqrt(300 ** 2 + 250 ** 2 - 2 * 300 * 250 * math.cos(math.radians(70)))
print(by_rule)
print(distance(near_end, far_end))
```

Both say the lake is about 318 m long. The rule also runs backwards.
With all three sides known, we can make $\cos C$ the subject, as on
[Running a formula backwards](tutorial:running-a-formula-backwards):

$$\cos C = \frac{a^2 + b^2 - c^2}{2ab}$$

and then `math.acos` gives the angle.

## A tool for the angle at a corner

Games and maps often know three points and want the angle at the middle
one. Is the player facing the ball? Here is a toolkit function for
that, with the cosine rule run backwards inside it. The body is yours:

1. Use `distance` to find the two sides that meet at `q`, and the side
   across from `q`.
2. Work out $\cos C$ from the backwards rule.
3. Keep that cosine between −1 and 1 with `max(-1, min(1, cos_q))`. The
   reason is below.
4. Return the angle, in degrees, with `math.acos` and `math.degrees`.

```python exec
id: how-tall-toolkit
toolkit: yes
import math


def angle_between(p, q, r):
    """Return the angle at corner q, in degrees, between the line to p and the line to r.

    p, q and r are (x, y) points, and neither p nor r is the same point as q.
    The answer is from 0 to 180. angle_between((1, 0), (0, 0), (0, 1)) is 90.
    """
    ...
```

```python toolkit-reference
for: how-tall-toolkit
import math


def angle_between(p, q, r):
    """Return the angle at corner q, in degrees, between the line to p and the line to r.

    p, q and r are (x, y) points, and neither p nor r is the same point as q.
    The answer is from 0 to 180. angle_between((1, 0), (0, 0), (0, 1)) is 90.
    """
    side_to_p = distance(q, p)
    side_to_r = distance(q, r)
    across = distance(p, r)
    cos_q = (side_to_p ** 2 + side_to_r ** 2 - across ** 2) / (2 * side_to_p * side_to_r)
    # Rounding can push a cosine a hair past 1 or -1, where acos has no answer.
    cos_q = max(-1, min(1, cos_q))
    return math.degrees(math.acos(cos_q))
```

Run the toolkit cell, then the tests. Until `angle_between` is written,
the first test stops with a `TypeError`, because `...` gives back `None`.

```python exec
id: how-tall-toolkit-tests
assert close_enough(angle_between((1, 0), (0, 0), (0, 1)), 90), "a square corner"
assert close_enough(angle_between((4, 0), (0, 0), (4, 3)), math.degrees(math.atan(3 / 4)))
assert close_enough(angle_between(near_end, you, far_end), 70), "the lake"
assert close_enough(angle_between((-1, 0), (0, 0), (1, 0)), 180), "a straight line"
assert close_enough(angle_between((0.1, 0.1), (0.2, 0.1), (0.4, 0.1)), 180), "a straight line, with rounding"

corners = [(0, 0), (7, 1), (2, 5)]
angle_sum = (angle_between(corners[2], corners[0], corners[1])
             + angle_between(corners[0], corners[1], corners[2])
             + angle_between(corners[1], corners[2], corners[0]))
assert close_enough(angle_sum, 180), "the angles of a flat triangle"
print("angle_between keeps its promise.")
```

```hint
Try `print(angle_between((1, 0), (0, 0), (0, 1)))` on its own. What came
back? If it is `None`, which line should give the answer back?
```

```hint
after: 10 errors
title: some steps
1. `side_to_p = distance(q, p)` and `side_to_r = distance(q, r)` are the
   two sides that meet at `q`.
2. `across = distance(p, r)` is the side opposite `q`.
3. `cos_q` is the two sides squared and added, minus `across` squared,
   all divided by twice the two sides multiplied.
4. Keep it in range, then `return math.degrees(math.acos(cos_q))`.

**Think about:** why is `across` the side that is taken away?
```

The fifth test is why step 3 is there. Three points on a straight line
make an angle of 180°, whose cosine is −1. But 0.1 and 0.2 are not exact
in binary, so the sum comes out a tiny bit below −1, such as
−1.0000000000000002. That is outside the domain of `math.acos`, which
stops with `ValueError: math domain error`. The `max` and `min` line
moves it back to −1. The last test is about the space we are in: the
angles of a flat triangle add up to 180°.

## The sine rule: when you cannot reach the tree

Now an oak stands across a river, and you cannot measure the distance
to its trunk. What can you measure? Two angles, and how far you walk
between them.

From a spot A, the top of the tree is 28° up. You walk 15 m straight
towards the tree, to a spot B, and the top is now 40° up. A, B and the
treetop T make a triangle with no right angle. At A, its angle is 28°.
At B, the 40° is outside the triangle, so the angle inside is
$180 - 40 = 140°$. At T is what is left: $180 - 28 - 140 = 12°$.

We know one side, AB = 15 m, and the angle across from it, 12° at T.
When a side and its opposite angle are both known, the *sine rule* helps.
In words: each side divided by the sine of the angle opposite it gives
the same number, all the way round the triangle.

$$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}$$

The side from B up to the treetop is opposite the 28° angle at A. So
$\frac{BT}{\sin 28^\circ} = \frac{15}{\sin 12^\circ}$. Once we know BT,
SOH from spot B gives the height. Guess the height first.

```python exec
id: how-tall-sine-1
walked = 15
angle_at_a = 28
angle_at_b = 180 - 40
angle_at_top = 180 - angle_at_a - angle_at_b

b_to_top = walked * math.sin(math.radians(angle_at_a)) / math.sin(math.radians(angle_at_top))
tree_height = b_to_top * math.sin(math.radians(40)) + eye_height
print(angle_at_top, round(b_to_top, 2), round(tree_height, 1))
```

The line of sight from B is about 33.9 m, and the oak is about 23.4 m
tall. Nobody crossed the river.

Does the sine rule hold here? The cell puts the triangle on a map and
measures every angle with your `angle_between`, so write that first.

```python exec
id: how-tall-sine-2
spot_b = (0, 0)
spot_a = (-walked, 0)
treetop = point_on_circle(b_to_top, 40)

at_a = angle_between(spot_b, spot_a, treetop)
at_b = angle_between(spot_a, spot_b, treetop)
at_t = angle_between(spot_a, treetop, spot_b)
print(round(at_a, 6), round(at_b, 6), round(at_t, 6))

print(distance(spot_b, treetop) / math.sin(math.radians(at_a)))
print(distance(spot_a, treetop) / math.sin(math.radians(at_b)))
print(distance(spot_a, spot_b) / math.sin(math.radians(at_t)))
```

The angles are 28°, 140° and 12°, and each side divided by the sine
across from it gives the same number. So which rule, when? With a right
angle, SOH-CAH-TOA. With two sides and the angle between them, or all
three sides, the cosine rule. With a side and the angle across from it,
the sine rule. For further reading, there is
[Solving triangles: the sine rule and the cosine rule](tutorial:solving-triangles)
in the integrated course.

<details class="dl-why"><summary>Why this way?</summary>

This page built `angle_between` from three distances and the cosine rule
run backwards. It needed a line to keep a cosine inside −1 to 1.

A game programmer would more often use `math.atan2` twice, once for
each direction from `q`, and take the difference. That route never
leaves the domain of a function, and it can say which way the angle
turns, which a game needs to steer a player.

We chose the cosine rule because the page had just taught it, and a tool
built from its own rule is a check on that rule. The cost is a tool
that never says which side an angle is on.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a triangle's sides, named from one angle: opposite, adjacent, hypotenuse |
| What is promised? | SOH-CAH-TOA for a right angle; the cosine and sine rules for any triangle; `angle_between` promises the angle at a corner |
| What happens when? | at the river, the angles first, then the sine rule, then SOH; a cosine is put back in range before `acos` |
| What does this space let us do? | a flat triangle's angles make 180°, and a triangle on a ball need not; `atan2` keeps the signs a division throws away; no angle has a sine above 1, so past the critical angle light stays in |

## What we have now

| Term or tool | What it means |
|---|---|
| opposite, adjacent | from one angle: the side across from it; the short side touching it |
| SOH-CAH-TOA | $\sin = \frac{\text{opp}}{\text{hyp}}$, $\cos = \frac{\text{adj}}{\text{hyp}}$, $\tan = \frac{\text{opp}}{\text{adj}}$ |
| tangent in a triangle | opposite over adjacent: rise over run |
| angle of elevation | the angle up from level ground to something above you |
| `math.asin`, `math.acos`, `math.atan` | the inverses: from a ratio back to an angle, in radians |
| refraction, refractive index $n$ | light bending as it crosses into a new material; how many times more slowly light travels in it |
| Snell's law | $n_1 \sin\theta_1 = n_2 \sin\theta_2$, with angles from the normal |
| total internal reflection, critical angle | past the critical angle, no light gets out and all of it reflects |
| `math.atan2(y, x)` | the angle from two sides, keeping their signs |
| bearing | a direction, clockwise from north, 0° up to 360° |
| $\text{area} = \frac{1}{2}ab\sin C$ | a triangle's area from two sides and the angle between them |
| cosine rule | $c^2 = a^2 + b^2 - 2ab\cos C$: Pythagoras with a correction |
| sine rule | $\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}$ |
| `angle_between(p, q, r)` | your toolkit tool: the angle at corner `q`, in degrees |

The practice page is next, and after it the mixed problems for this
unit, where a small game checks whether a ball hits a wall.
