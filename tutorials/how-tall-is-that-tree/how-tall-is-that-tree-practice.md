---
title: "Solving triangles: how tall is that tree? — Practice"
practice_for: how-tall-is-that-tree
year: "2026-2027"
version: 2026.09.26.1
---

# Solving triangles: how tall is that tree? — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another way** means reach the same place by a second
route. The answers are folded away until you open them. Each is one
answer, and yours may be different and work too.

Your toolkit is loaded on this page, including `angle_between` from the
tutorial, `distance` from
[How far apart?](tutorial:how-far-apart) and `point_on_circle` from
[Going round in circles](tutorial:going-round-in-circles). `math` is
not loaded, so each cell starts with `import math`.

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
sine of 30° is 0.5. In a right-angled triangle with a 30° angle, the
side opposite it is half the hypotenuse.

</details>

**2. Predict.** What does `angle_between` give for each of these?

```python
print(round(angle_between((0, 5), (0, 0), (5, 0)), 1))
print(round(angle_between((1, 1), (0, 0), (2, 2)), 1))
```

<details class="dl-answer"><summary>answer</summary>

`90.0` and `0.0`.

From the corner $(0, 0)$, one point is due north and the other due east,
so they make a square corner. In the second line, $(1, 1)$ and $(2, 2)$ are in the
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
`math.atan` runs it backwards. The ladder's length does not matter. Any
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
# Your working for problems 5 to 13
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
y. Write `compass_bearing(start, end)`, which returns the bearing from
one point to another, from 0 up to 360 degrees. Test it with four points
due north, east, south and west of $(0, 0)$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find how far east and how far north `end` is from `start`.
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

**7. Fix.** Schlomo, who is learning Python too, checked the tree's
height from the tutorial: 20 m away, 35° up, eyes at 1.6 m. His cell
prints about 11.1, not 15.6. What is it doing with the 35, and what
needs to change?

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

Python gave no error, because 35 radians is a real angle. The number
was in a different space from the one Schlomo meant. He only saw the
problem because he checked against an answer he already knew.

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

**9. Fix.** Schlomi, who is learning Python too, wrote her own cosine
rule, with two tests. The first test passes and the second fails. What
is different about the second test, and what needs to change?

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
0 whether it is added or taken away. Schlomi started from the triangle
she knew best, the 3, 4, 5, and a test at a right angle alone can never
tell the two versions apart. For 60°, her version gives about 7.81, and the rule
gives $\sqrt{21} \approx 4.58$.

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

$d$ is about 25.95 m. Put it back in, and both sides give a height of
about 21.77 m above your eyes, and 23.4 m in all, the same as the sine
rule.

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
$180^\circ$ minus that, is yours to check. To test it, add up the
angles, and see if both choices stay under 180°.

</details>

**13. Make.** Light from the sky meets a glass window at 30° from the
normal. The glass has a refractive index of about 1.5, and air about
1.00. At what angle does the light travel inside the glass? It leaves
through the other side of the pane, which is parallel to the first.
Before you calculate it, at what angle does it come out into the room?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Snell's law: $1.00 \sin 30^\circ = 1.5 \sin\theta_2$.
2. Make $\sin\theta_2$ the subject, then use `math.asin` and
   `math.degrees`.
3. At the second side, the light meets the surface at the angle it had
   inside the glass, and goes from index 1.5 back to 1.00.

**Think about:** what does the second step undo?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
inside = math.degrees(math.asin(1.00 * math.sin(math.radians(30)) / 1.5))
print(round(inside, 2))
out_again = math.degrees(math.asin(1.5 * math.sin(math.radians(inside)) / 1.00))
print(round(out_again, 2))
```

Inside the glass the light travels at about 19.47° from the normal.
It comes out at 30° again. The second surface runs Snell's law
backwards, so the ray leaves parallel to how it came in, only moved a
little to one side. So a window does not bend the view behind it, but
a curved lens does.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: how-tall-practice-stretch
import math
# Your working for problems 14 to 18
```

**14. Make.** Write `height_from_two_angles(walked, first_angle,
second_angle, eye_height)`. It takes the two angles of elevation from
two spots, `walked` metres apart on a line towards something tall, and
returns its height, using the sine rule as the tutorial did. Test it
on the oak (15 m, 28°, 40°, 1.6 m gives about 23.4). Then use it on a
wind turbine: from a road the hub is 20° up, and 100 m closer it is 30°
up. These numbers are invented. How high is the hub?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The angle inside the triangle at the nearer spot is
   `180 - second_angle`.
2. The angle at the top is what is left of 180°.
3. By the sine rule, the line of sight from the nearer spot is
   `walked * sin(first_angle) / sin(angle at the top)`.
4. SOH from the nearer spot gives the height above your eyes.

**Think about:** what happens if `second_angle` is not bigger than
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
$180 - 20 - (180 - 30) = 30 - 20 = 10°$. That is the difference between
the two angles. If the two angles are the same, that angle is 0, its sine is 0,
and Python stops with a `ZeroDivisionError`. The two lines of sight
never meet, and there is no triangle.

</details>

**15. Make.** In a football game on a screen, a player at `player` is
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

**16. Another way.** The three phone masts from the tutorial stand at
$(0, 0)$, $(3.0, 0)$ and `point_on_circle(2.5, 70)`, in kilometres.
Find the area of their triangle two ways from the corners alone: with
`angle_between`, `distance` and $\frac{1}{2}ab\sin C$, and with
`triangle_area(base, height)`, where the height is the top corner's y.
Do both give about 3.52 square kilometres?

<details class="dl-answer"><summary>answer</summary>

```python
first_mast = (0, 0)
second_mast = (3.0, 0)
third_mast = point_on_circle(2.5, 70)

side_a = distance(first_mast, second_mast)
side_b = distance(first_mast, third_mast)
angle_c = angle_between(second_mast, first_mast, third_mast)
print(round(0.5 * side_a * side_b * math.sin(math.radians(angle_c)), 2))
print(round(triangle_area(3.0, third_mast[1]), 2))
```

Both print 3.52. The base lies along the x-axis, so the height is the
top corner's y. The first route never needed the height at all.

</details>

**17. Explain.** The tutorial found the tree's height from an angle
and the tangent. There is an older way, with no angles at all. On a
sunny day, stand a 1 m stick upright and measure its shadow, then
measure the tree's shadow. The stick and the tree make two triangles of
the same shape, so the tree is as many times taller than the stick as
its shadow is longer. If you were teaching a friend to measure a tree,
which way would you start with, and why?

<details class="dl-answer"><summary>answer</summary>

There is no single answer. An answer might weigh a few things:

- **What it needs.** Shadows need sun, a tape and a stick, and no
  sines or tangents. Angles need a way to measure an angle, but work
  on a cloudy day, and across a river with the sine rule.
- **What it leads to.** The shadow method is two triangles of the same
  shape, and stops there. Angles lead to the sine and cosine rules,
  for triangles with no right angle at all.
- **Your friend.** Someone meeting triangles for the first time may
  trust a shadow they can see. Someone who needs bearings for a map, or
  angles for a game, will need the tangent at some point.

It helps to say who the friend is and what they will use it for, and
to choose from that.

</details>

**18. Make.** An optical fibre has a core of glass with a refractive
index of about 1.47, inside a layer of glass, the cladding, of about
1.46. (These are typical values, rounded.) Find the critical angle
where the core meets the cladding. Next, suppose light travels down the fibre
at 5° to its middle line, and meets the side. The side runs along the
middle line, so the normal is at a right angle to it. Does the light
stay in? And at 10°?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. At the critical angle, the light would leave at 90°, where the sine
   is 1. So $1.47 \sin\theta_c = 1.46 \times 1$.
2. A ray at 5° to the middle line meets the side at $90 - 5 = 85$
   degrees from the normal.
3. The light stays in when that angle is bigger than the critical
   angle.

**Think about:** why does the cladding's index have to be lower than
the core's?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
critical = math.degrees(math.asin(1.46 / 1.47))
print(round(critical, 1))
for angle_to_middle in [5, 10]:
    from_normal = 90 - angle_to_middle
    print(angle_to_middle, from_normal, from_normal > critical)
```

The critical angle is about 83.3°. A ray at 5° to the middle line meets
the side at 85° from the normal, past the critical angle, so it
reflects and stays in. A ray at 10° meets the side at 80°, and some of
it escapes. So a fibre only carries light that travels almost straight
along it, within about 6.7° of its middle line. If the cladding's
index were higher than the core's, there would be no critical angle at
all, because $\sin\theta_c$ would have to be more than 1.

</details>

<aside class="dl-note" id="how-tall-practice-note-kao">

**A Nobel Prize for pure glass.** In 1966, Charles Kao and George
Hockham showed that light could travel through a glass fibre for
kilometres, if the glass were pure enough. The fibres of the 1960s
could carry light only about 20 metres. The first fibre pure enough
was made in 1970, and Kao was given the Nobel Prize in Physics in 2009.

</aside>
