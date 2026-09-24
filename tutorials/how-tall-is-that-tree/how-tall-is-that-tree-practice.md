---
title: "Solving triangles: how tall is that tree? — Practice"
practice_for: how-tall-is-that-tree
year: "2026-2027"
version: 2026.09.24.1
---

# Solving triangles: how tall is that tree? — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `angle_between` from the
tutorial, `distance` from
[How far apart?](tutorial:how-far-apart) and `point_on_circle` from
[Going round in circles](tutorial:going-round-in-circles). `math` is
not: each cell starts with `import math`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: how-tall-practice-warm-up
import math
# Try things here
```

**1. Predict.** What does this line print?

```python
print(round(math.degrees(math.atan(1)), 1), round(math.sin(math.radians(30)), 2))
```

<details class="dl-answer"><summary>answer</summary>

`45.0 0.5`.

A tangent of 1 means the opposite and adjacent sides are the same
length, so the triangle is half of a square, and its angle is 45°. The
sine of 30° is 0.5: in a right-angled triangle with a 30° angle, the
side opposite it is half the hypotenuse.

</details>

**2. Predict.** What does `angle_between` give for each of these?

```python
print(round(angle_between((0, 5), (0, 0), (5, 0)), 1))
print(round(angle_between((1, 1), (0, 0), (2, 2)), 1))
```

<details class="dl-answer"><summary>answer</summary>

`90.0` and `0.0`.

From the corner $(0, 0)$, one point is due north and the other due east:
a square corner. In the second line, $(1, 1)$ and $(2, 2)$ are in the
same direction from $(0, 0)$, so the two lines lie on top of each other
and the angle between them is 0°.

</details>

**3. Make.** On the practice page for
[How far apart?](tutorial:how-far-apart), a ladder followed the "1 in
4" rule: for every 4 m of height, its foot is 1 m out from the wall.
What angle does such a ladder make with the ground?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. From the angle at the foot of the ladder, the wall is the opposite
   side and the ground is the adjacent side.
2. Which of SOH, CAH and TOA uses opposite and adjacent?
3. Go backwards from the ratio to the angle, and turn radians into
   degrees.

**Think about:** does it matter how long the ladder is?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(math.degrees(math.atan(4 / 1)))
```

About 76°. The tangent is opposite over adjacent, $\frac{4}{1}$, and
`math.atan` runs it backwards. The ladder's length does not matter: any
ladder at 4 up for 1 out has the same shape, and the same angle.

</details>

**4. Explain.** A ramp rises from the path to a door. From the angle at
the bottom of the ramp, the rise is the opposite side. From the angle at
the top, between the ramp and the door's wall, which side is opposite?
Why can one side have two names?

<details class="dl-answer"><summary>answer</summary>

From the top, the opposite side is the flat run along the ground, and the
rise is now the adjacent side. The names opposite and adjacent are not
fixed to the sides. They say where a side is from the angle we are
looking at. Only the hypotenuse keeps its name, because it is always
across from the right angle.

</details>

## Core

A cell for the core problems.

```python exec
id: how-tall-practice-core
import math
# Your working for problems 5 to 12
```

**5. Make.** You fly a kite on Dollymount Strand. All 50 m of its string
is let out, the string is straight, and it makes 40° with level ground.
Your hand is 1 m above the sand. How high is the kite?

<details class="dl-answer"><summary>answer</summary>

```python
string = 50
kite_height = string * math.sin(math.radians(40)) + 1
print(round(kite_height, 1))
```

About 33.1 m. The string is the hypotenuse and the height above your
hand is the opposite side, so SOH gives
$\text{opposite} = \text{hypotenuse} \times \sin 40^\circ$. Then add the
1 m to your hand.

</details>

**6. Make.** Orienteering maps have a grid with east as x and north as
y. Write `compass_bearing(start, end)`, which gives back the bearing from
one point to another, from 0 up to 360 degrees. Test it with four points
due north, east, south and west of $(0, 0)$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work out how far east and how far north `end` is from `start`.
2. `math.atan2` takes two sides and keeps their signs. For a bearing,
   give it east first, then north.
3. Turn radians into degrees, and use `% 360` to move a negative answer
   round to the compass.

**Think about:** what should the bearing be for a point due west?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def compass_bearing(start, end):
    """Return the bearing from start to end in degrees, from 0 up to 360."""
    east = end[0] - start[0]
    north = end[1] - start[1]
    return math.degrees(math.atan2(east, north)) % 360

assert compass_bearing((0, 0), (0, 5)) == 0
assert compass_bearing((0, 0), (5, 0)) == 90
assert compass_bearing((0, 0), (0, -5)) == 180
assert compass_bearing((0, 0), (-5, 0)) == 270
print(compass_bearing((2, 1), (5, 5)))
```

The four tests pass, and a control point 3 km east and 4 km north of you
is on a bearing of about 36.9°. Without `% 360`, the point due west
gives −90.

</details>

**7. Fix.** This cell is meant to find the tree's height from the
tutorial: 20 m away, 35° up, eyes at 1.6 m. It prints about 11.1, not
15.6. Find the mistake.

```python exec
id: how-tall-practice-fix-radians
import math

distance_to_trunk = 20
angle_up = 35
tree_height = distance_to_trunk * math.tan(angle_up) + 1.6
print(round(tree_height, 1))
```

<details class="dl-answer"><summary>answer</summary>

`math.tan` works in radians, and it was given 35 degrees. As an angle in
radians, 35 is more than five whole turns round the circle, and its
tangent is about 0.47, where the tangent of 35° is about 0.70. The fix:

```python
tree_height = distance_to_trunk * math.tan(math.radians(angle_up)) + 1.6
```

Python gave no error, because 35 radians is a real angle. It was the
wrong space for the number, and only a check against an answer we knew
caught it.

</details>

**8. Make.** A dinghy's sail is a triangle. Two of its edges are 3.2 m
and 2.5 m, and the angle between them is 80°. How many square metres of
cloth is the sail?

<details class="dl-answer"><summary>answer</summary>

```python
print(round(0.5 * 3.2 * 2.5 * math.sin(math.radians(80)), 2))
```

About 3.94 square metres, from
$\text{area} = \frac{1}{2}ab\sin C$. With a right angle, it would be
$\frac{1}{2} \times 3.2 \times 2.5 = 4$ square metres, a little more,
because $\sin 90^\circ = 1$ is the biggest a sine can be.

</details>

**9. Fix.** Here is someone's cosine rule, with two tests. The first
test passes and the second fails. Find the mistake.

```python exec
id: how-tall-practice-fix-cosine
import math

def third_side(a, b, angle_c):
    """Return the side across from angle_c (in degrees), where sides a and b meet."""
    return math.sqrt(a ** 2 + b ** 2 + 2 * a * b * math.cos(math.radians(angle_c)))

assert close_enough(third_side(3, 4, 90), 5), "a right angle"
assert close_enough(third_side(5, 4, 60), math.sqrt(21)), "a 60 degree corner"
print("third_side keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The correction must be taken away: $c^2 = a^2 + b^2 - 2ab\cos C$. The
line should be

```python
    return math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(angle_c)))
```

The first test passed because $\cos 90^\circ = 0$, so the correction is
0 whether it is added or taken away. A test at a right angle alone could
never have found this mistake. For 60°, the wrong version gives about
7.81, and the right one gives $\sqrt{21} \approx 4.58$.

</details>

**10. Another way.** In the tutorial, the oak across the river was 28°
up from spot A and 40° up from spot B, 15 m closer. The sine rule gave
about 23.4 m. Find it again with tangents alone. Call the unknown
distance from B to the trunk $d$. Then the height above your eyes is
$d\tan 40^\circ$, and it is also $(d + 15)\tan 28^\circ$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The two heights are the same, so
   $d\tan 40^\circ = (d + 15)\tan 28^\circ$.
2. Move everything to one side:
   $d(\tan 40^\circ - \tan 28^\circ) - 15\tan 28^\circ = 0$.
3. That is $ad + b = 0$, a linear equation. Your toolkit's
   `solve_linear(a, b)` from
   [Solving for x](tutorial:solving-for-x) solves it.

**Think about:** how do you check the $d$ you found?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
tan_40 = math.tan(math.radians(40))
tan_28 = math.tan(math.radians(28))

d = solve_linear(tan_40 - tan_28, -15 * tan_28)
print(round(d, 2))
print(round(d * tan_40, 2), round((d + 15) * tan_28, 2))
print(round(d * tan_40 + 1.6, 1))
```

$d$ is about 25.95 m. Substituting it back, both sides give a height of
about 21.77 m above your eyes, and 23.4 m in all, the same as the sine
rule. Two routes, one tree.

</details>

**11. Predict.** Before you run it, what are the three angles of this
triangle, roughly, and what is their sum?

```python
corners = [(0, 0), (4, 0), (0, 3)]
at_0 = angle_between(corners[1], corners[0], corners[2])
at_1 = angle_between(corners[0], corners[1], corners[2])
at_2 = angle_between(corners[0], corners[2], corners[1])
print(round(at_0, 2), round(at_1, 2), round(at_2, 2), round(at_0 + at_1 + at_2, 2))
```

<details class="dl-answer"><summary>answer</summary>

`90.0 36.87 53.13 180.0`.

The corner at $(0, 0)$ is a square corner. At $(4, 0)$, the opposite
side is 3 and the adjacent side is 4, so the angle is
`math.degrees(math.atan(3 / 4))`, about 36.87°. The last angle is what is
left of 180°. On a flat plane it always is.

</details>

**12. Explain.** `math.asin(0.5)`, turned into degrees, gives 30°.
But $\sin 150^\circ$ is 0.5 too. Why can the sine rule sometimes fit two
different triangles to the same measurements, and why does `math.asin`
give only one of them?

<details class="dl-answer"><summary>answer</summary>

On the circle, the points at 30° and at 150° are at the same height,
one on each side of the y-axis, so they have the same sine. When the
sine rule gives you a sine and you go back to an angle, both 30° and
150° fit. If the other angles still leave room, there are two triangles.

`math.asin` is a function, and a function gives one answer for each
input. So it always picks the angle from −90° to 90°. The other answer,
$180^\circ$ minus that, is yours to check. A good test: add up the
angles, and see if both choices stay under 180°.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: how-tall-practice-stretch
import math
# Your working for problems 13 to 16
```

**13. Make.** Write `height_from_two_angles(walked, first_angle,
second_angle, eye_height)`. It takes the two angles of elevation from
two spots, `walked` metres apart on a line towards something tall, and
gives back its height, using the sine rule as the tutorial did. Test it
on the oak (15 m, 28°, 40°, 1.6 m gives about 23.4). Then use it on a
wind turbine: from a road the hub is 20° up, and 100 m closer it is 30°
up. These numbers are made up. How high is the hub?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The angle inside the triangle at the nearer spot is
   `180 - second_angle`.
2. The angle at the top is what is left of 180°.
3. By the sine rule, the line of sight from the nearer spot is
   `walked * sin(first_angle) / sin(angle at the top)`.
4. SOH from the nearer spot gives the height above your eyes.

**Think about:** what goes wrong if `second_angle` is not bigger than
`first_angle`?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def height_from_two_angles(walked, first_angle, second_angle, eye_height):
    """Return the height of something tall, from its angles of elevation at two spots.

    The spots are walked metres apart, in a line towards it, and
    second_angle (the nearer spot) must be bigger than first_angle.
    """
    angle_at_top = second_angle - first_angle
    sight_line = (walked * math.sin(math.radians(first_angle))
                  / math.sin(math.radians(angle_at_top)))
    return sight_line * math.sin(math.radians(second_angle)) + eye_height

assert close_enough(height_from_two_angles(15, 28, 40, 1.6), 23.3715, tolerance=0.001)
print(round(height_from_two_angles(100, 20, 30, 1.6), 1))
```

The hub is about 100 m up. The angle at the top is
$180 - 20 - (180 - 30) = 30 - 20 = 10°$: the difference between the two
angles. If the two angles are the same, that angle is 0, its sine is 0,
and Python stops with a `ZeroDivisionError`. The two lines of sight
never meet, and there is no triangle.

</details>

**14. Make.** In a football game on a screen, a player at `player` is
facing towards the point `facing`. The player can see the ball if the
angle between where they face and where the ball is, measured at the
player, is 60° or less. Write `can_see(player, facing, ball)`, and test
it with a player at $(0, 0)$ facing $(10, 0)$, and a ball at $(5, 2)$,
at $(0, 5)$ and at $(-5, 0)$.

<details class="dl-answer"><summary>answer</summary>

```python
def can_see(player, facing, ball):
    """Return True when the ball is within 60 degrees of where the player faces."""
    return angle_between(facing, player, ball) <= 60

print(can_see((0, 0), (10, 0), (5, 2)))
print(can_see((0, 0), (10, 0), (0, 5)))
print(can_see((0, 0), (10, 0), (-5, 0)))
```

`True`, `False`, `False`. The first ball is about 22° off to the side,
the second is at 90° and the third is right behind, at 180°. The corner
is the player, so `player` goes in the middle of `angle_between`.

</details>

**15. Another way.** The allotment from the tutorial has corners at
$(0, 0)$, $(30, 0)$ and `point_on_circle(25, 70)`. Find its area two
ways from the corners alone: with `angle_between`, `distance` and
$\frac{1}{2}ab\sin C$, and with `triangle_area(base, height)`, where the
height is the top corner's y. Do both give about 352.4?

<details class="dl-answer"><summary>answer</summary>

```python
gate = (0, 0)
far_corner = (30, 0)
top_corner = point_on_circle(25, 70)

side_a = distance(gate, far_corner)
side_b = distance(gate, top_corner)
angle_c = angle_between(far_corner, gate, top_corner)
print(round(0.5 * side_a * side_b * math.sin(math.radians(angle_c)), 1))
print(round(triangle_area(30, top_corner[1]), 1))
```

Both print 352.4. The base lies along the x-axis, so the height is the
top corner's y. The first route never needed the height at all.

</details>

**16. Explain.** The tutorial found the tree's height from an angle
and the tangent. There is an older way, with no angles at all. On a
sunny day, stand a 1 m stick upright and measure its shadow, then
measure the tree's shadow. The stick and the tree make two triangles of
the same shape, so the tree is as many times taller than the stick as
its shadow is longer. If you were teaching a friend to measure a tree,
which way would you start with, and why?

<details class="dl-answer"><summary>answer</summary>

There is no one right answer. A good answer weighs a few things:

- **What it needs.** Shadows need sun, a tape and a stick, and no
  sines or tangents. Angles need a way to measure an angle, but work
  on a cloudy day, and across a river with the sine rule.
- **What it leads to.** The shadow method is two triangles of the same
  shape, and stops there. Angles lead on to the sine and cosine rules,
  for triangles with no right angle at all.
- **Your friend.** Someone meeting triangles for the first time may
  trust a shadow they can see. Someone who needs bearings for a map, or
  angles for a game, needs the tangent sooner or later.

A strong answer says who the friend is and what they will use it for,
and chooses from that.

</details>
