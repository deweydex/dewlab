---
title: "Mixed problems: trigonometry and geometry"
practice_across:
  - slope-and-lines
  - distance-and-pythagoras
  - the-unit-circle
  - sine-and-cosine-waves
  - solving-triangles
year: "2026-2027"
version: 2026.08.23.1
---

# Mixed problems: trigonometry and geometry

Coordinates, angles, triangles and waves are four views of the same
circle. These problems move between them, often without saying so.

Each answer is hidden in a fold under its question. Some problems also
have a hint fold, to open first if you get stuck. Draw the situation
before you calculate. In this topic more than any other, the picture
shows you the mistakes.

## Tools

This cell defines two helpers:

- `distance(p, q)` gives the straight-line distance between two points.
- `angle_between(p, q)` gives the direction of the line from `p` to `q`,
  in degrees, measured anticlockwise from east (the positive $x$
  direction).

The last line tries them. The distance from $(0, 0)$ to $(3, 4)$ is 5,
and the line from $(0, 0)$ to $(1, 1)$ points at 45°.

```python exec
id: tools-1
import math


def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    return math.hypot(x2 - x1, y2 - y1)


def angle_between(p, q):
    """The angle of the line from p to q, in degrees anticlockwise from east."""
    (x1, y1), (x2, y2) = p, q
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


print(distance((0, 0), (3, 4)), angle_between((0, 0), (1, 1)))
```

## Coordinates and angles

**1.** A point is at $(3, 4)$. How far is it from the origin, and at what
angle?

<details class="dl-answer"><summary>answer</summary>

5 units, at about 53.13°.

The distance comes from Pythagoras: $\sqrt{3^2 + 4^2} = \sqrt{25} = 5$.
The angle is $\arctan\left(\dfrac{4}{3}\right) \approx 53.13°$.

These two numbers, the distance $r$ and the angle $\theta$, are called
the *polar coordinates* of the point. Converting between $(x, y)$ and
$(r, \theta)$ uses the same arithmetic as converting between a right
triangle's sides and its angles. They are the same problem.

</details>

**2.** Convert $(r, \theta) = (10, 30°)$ back to $x$ and $y$.

<details class="dl-answer"><summary>answer</summary>

$(8.66, 5)$.

Use $x = r\cos\theta$ and $y = r\sin\theta$. Since
$\cos 30° = \dfrac{\sqrt{3}}{2}$ and $\sin 30° = \dfrac{1}{2}$, that
gives exactly $x = 5\sqrt{3} \approx 8.66$ and $y = 5$.

This is the unit circle, made 10 times bigger.

</details>

**3.** Why do we use `atan2(y, x)` instead of `atan(y/x)`?

<details class="dl-answer"><summary>answer</summary>

Because the division loses the quadrant.

$\dfrac{4}{3}$ and $\dfrac{-4}{-3}$ are the same number. So `atan`
cannot tell $(3, 4)$ from $(-3, -4)$. It returns 53.13° for both, but
$(-3, -4)$ is really at 233.13°.

`atan2` takes the two values separately, and keeps their signs. So it
returns the correct angle anywhere on the circle. It also works when
$x = 0$, where the division fails.

</details>

**4.** A robot at $(2, 3)$ must turn to face a target at $(7, 15)$. What
direction should it face, and how far away is the target?

<details class="dl-answer"><summary>answer</summary>

About 67.38°, and 13 units.

The gaps are 5 across and 12 up. That makes a 5-12-13 triangle, which is
worth knowing, like 3-4-5. The angle is
$\arctan\left(\dfrac{12}{5}\right) \approx 67.38°$.

</details>

## Triangles

**5.** A triangle has sides 7 and 9, with an angle of 40° between them.
Find the third side, and the other two angles.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw the triangle. You have two sides and the angle *between* them.
   The sine rule cannot start from that.
2. The cosine rule fits exactly this arrangement: two sides and the
   angle between them give you the third side.
3. Once you have all three sides, the sine rule will give you an angle.
4. Use it on the *shorter* of the two sides you started with. That
   matters. See "Think about" below.

**Think about:** the sine rule cannot tell an acute angle from the
obtuse angle that pairs with it, because both have the same sine. The
angle opposite the shorter side is always acute. So if you choose it,
there is no doubt, and you do not have to guess.

**Try this next:** find the third angle by subtracting from 180°
instead, and check that it agrees. Which method would you trust if the
numbers were measured, not given?

</details>

<details class="dl-answer"><summary>answer</summary>

The third side is about 5.79. The other angles are about 51.0° and
89.0°.

The cosine rule gives the side:
$c^2 = 49 + 81 - 2(7)(9)\cos 40° \approx 33.48$, so $c \approx 5.79$.

Then the sine rule gives an angle. Use it on the *shorter* of the two
remaining sides, the 7. The sine rule cannot tell an acute angle from
the obtuse angle with the same sine. The angle opposite the shorter side
must be acute, so the acute answer is the right one.

</details>

**6.** A triangle has sides 5, 12 and 13. Is it right-angled? What is its
area?

<details class="dl-answer"><summary>answer</summary>

Yes, because $5^2 + 12^2 = 25 + 144 = 169 = 13^2$. The area is 30.

For a right triangle, the area is half the product of the two short
sides: $\dfrac{5 \times 12}{2} = 30$.

*Heron's formula* gives the area of any triangle from its three sides
alone. First find $s$, half the perimeter. Then the area is
$\sqrt{s(s - a)(s - b)(s - c)}$. Here $s = \dfrac{5 + 12 + 13}{2} = 15$,
and the area is $\sqrt{15 \times 10 \times 3 \times 2} = \sqrt{900} = 30$.
It gives the same 30 without knowing that the triangle is right-angled.

</details>

**7.** Two sides of a triangle are 8 and 5. The angle opposite the 5 is
30°. Find the third side.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. You have two sides and an angle that is *not* between them. Sketch
   it: draw the 8, mark the 30° at one end, and swing the 5 from the
   other end.
2. The sine rule gives you the angle opposite the 8. Find its sine
   first, before you take an inverse.
3. Now stop. Your calculator gives one angle. Is there another angle
   between 0° and 180° with the same sine?
4. Each of those two angles gives a different third angle, and so a
   different third side.

**Think about:** the picture shows this directly. When you swing the 5,
it crosses the base line in two places. This is why this arrangement is
called the ambiguous case.

**Try this next:** change the 5 to a 3, and try again. What happens?
What does the picture look like now?

</details>

<details class="dl-answer"><summary>answer</summary>

There are two answers: about 9.93 and about 3.93.

$\sin \theta = \dfrac{8 \sin 30°}{5} = \dfrac{8 \times 0.5}{5} = 0.8$. So
the angle opposite the 8 is either 53.13° or 126.87°. Both have a sine
of 0.8.

This is the ambiguous case. Two different triangles fit everything you
were told. A drawing shows why. When you swing the 5 from the end of the
8, it crosses the base line twice.

The unit circle explains it in one line. Sine is symmetric about 90°,
so $\sin\theta$ never tells you which side of 90° you are on.

</details>

**8.** Find the area of the triangle with corners $(0, 0)$, $(6, 0)$ and
$(2, 5)$, in three different ways.

<details class="dl-answer"><summary>answer</summary>

15, every time.

**Base times height, over two.** The base is 6, along the $x$-axis. The
height is 5. So the area is $\dfrac{6 \times 5}{2} = 15$.

**Heron's formula** (see question 6). The sides are 6, $\sqrt{29}$ and
$\sqrt{41}$, so $s \approx 8.89$. The formula gives 15.

**The coordinate formula.**
$\frac{1}{2}|x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)| = \frac{1}{2}|0 + 6(5) + 2(0)| = 15$.

When three routes agree, you can trust the answer. It is a good habit to
check like this.

</details>

## Waves

**9.** For $y = 3\sin(2x)$, what is the amplitude? What is the period?
Where does it first cross zero going upwards, from $x = 0$ on?

<details class="dl-answer"><summary>answer</summary>

The amplitude is 3 and the period is $\pi$. It crosses zero going
upwards at $x = 0$ itself, and again at $x = \pi$.

The 3 stretches the wave upwards and downwards. The 2 squashes it from
side to side, and halves the period from $2\pi$ to $\pi$. The number
inside does the opposite of what it looks like it should do. Almost
everybody makes this mistake at least once.

</details>

**10.** Sketch $y = \sin x$ and $y = \cos x$ together. How far apart are
they?

<details class="dl-answer"><summary>answer</summary>

A quarter turn: $\cos x = \sin\left(x + \dfrac{\pi}{2}\right)$.

They are the same wave, started at a different point. The unit circle
shows this. Cosine is the across value, and sine is the up value, of the
same turning point.

</details>

**11.** The depth of water at a harbour is roughly
$h = 3 + 2\sin\left(\dfrac{2\pi t}{12.4}\right)$ metres, with $t$ in
hours.

1. What is the depth at high water?
2. What is the depth at low water?
3. How long is it from one high water to the next?

<details class="dl-answer"><summary>answer</summary>

High water is 5 m, low water is 1 m, and there are 12.4 hours between
high waters.

The 3 is the middle level, and the 2 is the amplitude. So the depth
goes from $3 - 2 = 1$ up to $3 + 2 = 5$. The period is
$\dfrac{2\pi}{2\pi/12.4} = 12.4$ hours.

The period is 12.4 hours, not 12. That is why high tide comes about 50
minutes later each day. The tide follows the moon, and the moon is not
on a 24-hour cycle.

</details>

**12.** A boat needs at least 4 m of water. Using the tide above, for how
long in each cycle can it enter the harbour?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Use the tide formula to write the inequality that the question asks
   about.
2. Rearrange it until the sine is on its own on one side.
3. Now you need the angles whose sine is at least that value. On the
   unit circle, which arc is that?
4. That arc is a fraction of a full turn. The same fraction of the
   period is your answer.

**Think about:** you never needed to find an actual clock time. The
answer was a fraction of the cycle. So it is the same for any
harbour with this middle level and amplitude.

**Try this next:** try a boat that needs 4.5 m, and then one that needs
5.5 m. At what depth does the answer become zero? Why does that make
sense?

</details>

<details class="dl-answer"><summary>answer</summary>

About 4.13 hours in each cycle.

Solve $3 + 2\sin\left(\dfrac{2\pi t}{12.4}\right) \ge 4$. Subtract 3 and
divide by 2: the sine must be at least 0.5. That is true when the angle
is between 30° and 150°. That is 120°, a third of a full turn.

A third of 12.4 hours is about 4.13 hours. The answer came from the unit
circle, and not from any calculation about boats. That is the useful
part.

</details>

**13.** Check that $\sin^2\theta + \cos^2\theta = 1$ for several angles.
Why must it be true?

<details class="dl-answer"><summary>answer</summary>

```python
for d in [0, 17, 45, 90, 137, 250, 359]:
    a = math.radians(d)
    print(d, round(math.sin(a) ** 2 + math.cos(a) ** 2, 12))
```

Every line prints 1.0.

It is Pythagoras on the unit circle. The point is at distance 1 from
the centre. Its two coordinates are the two short sides of a right
triangle whose longest side is 1.

Every trigonometric identity is a fact about that circle, written in a
different notation. This is the one the rest are built from.

</details>

## Longer ones

**14.** Three phone masts are at $(0, 0)$, $(10, 0)$ and $(4, 8)$, in
kilometres. A phone is 6 km from the first mast and 7 km from the
second. Where might it be? Does the third mast tell you which?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. You have two distances from two known points. Write each one as an
   equation. The set of points at a fixed distance from a point is a
   circle.
2. Subtract one circle's equation from the other. The $x^2$ and $y^2$
   terms cancel, and what is left is a straight line.
3. That line goes through the points where the two circles cross.
   Substitute back into either circle to find those two points.
4. Now use the third mast. Compute the distance from each possible
   point to $(4, 8)$.

**Think about:** two measurements always leave two possible points, and
more accuracy does not fix that. The third measurement tells you which
side you are on. It is not about precision.

**Try this next:** what if the third mast were at $(4, 0)$ instead, on
the line between the other two? Would it still tell you which?

</details>

<details class="dl-answer"><summary>answer</summary>

There are two possible positions: about $(4.35, 4.13)$ and
$(4.35, -4.13)$.

The circles are $x^2 + y^2 = 36$ and $(x - 10)^2 + y^2 = 49$.
Subtracting gives $20x - 100 = -13$, so $x = 4.35$. Then
$y^2 = 36 - 4.35^2 \approx 17.08$, so $y \approx \pm 4.13$.

Two circles cross at two points, so two distances are never enough. The
third mast picks one. The phone is 3.88 km from $(4, 8)$ if it is above
the axis, and 12.14 km if it is below. Those are very different
measurements.

This method is called *trilateration*, and satellite positioning (GPS)
works this way. Three satellites give a position on the Earth's
surface. A fourth is needed, because the receiver's clock is also
unknown.

</details>

**15.** A ladder 6 m long leans against a wall, at 70° to the ground.

1. How high up the wall does it reach?
2. How far from the wall is its foot?
3. If the foot slips 0.5 m further out, what angle is the ladder at
   then?

<details class="dl-answer"><summary>answer</summary>

It reaches $6 \sin 70° \approx 5.64$ m up the wall. Its foot is
$6 \cos 70° \approx 2.05$ m out.

After slipping, the foot is 2.55 m out. The angle is
$\arccos\left(\dfrac{2.55}{6}\right) \approx 64.8°$, and the ladder now
reaches 5.43 m.

Half a metre of slip costs five degrees, and twenty centimetres of
height. The relationship is not a straight line, and each extra slip
costs more height as the angle drops. That is the reason for the
4-to-1 rule for ladders: 1 m out from the wall for every 4 m up, which
is an angle of about 76°.

</details>

**16.** A wheel of radius 0.35 m turns at 60 revolutions per minute.
How fast is a point on the rim moving? How far does the wheel roll in a
minute?

<details class="dl-answer"><summary>answer</summary>

About 2.20 m/s, and about 132 m in a minute.

One revolution is $2\pi$ radians. So 60 revolutions per minute is one
revolution per second, which is $2\pi$ radians per second. This is the
*angular speed*, written $\omega$ (the Greek letter omega): the angle
turned per second.

A radian is the angle where the arc equals the radius. So an angle of
$\theta$ radians gives an arc of length $s = r\theta$. In one second
the rim moves $v = r\omega = 0.35 \times 2\pi \approx 2.199$ m. In a
minute, that is $2.199 \times 60 \approx 132$ m.

When the wheel rolls without slipping, the rim speed and the ground
speed are the same. That is why $s = r\theta$ is so useful for anything
mechanical.

</details>

**17.** Two points on a circle of radius 5 are 6 apart in a straight
line. What is the angle between them at the centre? How far apart are
they along the arc?

<details class="dl-answer"><summary>answer</summary>

About 1.287 radians (73.7°), and about 6.44 along the arc.

The straight line between the points (the chord) and the two radii form
an isosceles triangle. Cut it in half, and you get a right triangle
with longest side 5 and opposite side 3. So half the angle is
$\arcsin(0.6) \approx 0.6435$, and the whole angle is about 1.287.

The arc is $r\theta = 5 \times 1.287 \approx 6.44$. It is longer than
the chord, as it must be: the straight line is the shortest way.

</details>

**18.** Write a function that takes three points and returns the three
inside angles of the triangle they make. Test it on an equilateral
triangle.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. You have three points. Start by turning them into three side
   lengths.
2. To get an angle from three sides, rearrange the cosine rule so that
   the cosine is on its own.
3. Be careful about which side is opposite which angle. For the angle
   at `p`, the opposite side is the one joining `q` and `r`.
4. `math.acos` returns radians, so convert to degrees.

**Think about:** the cosine rule works from three sides, and it never
meets the ambiguous case. `acos` only returns angles between 0° and
180°, and that is exactly the range an inside angle can have.

**Try this next:** use `assert` to check that your three angles add up
to 180°. Then try three points in a straight line, and see what the
function does.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def angles(p, q, r):
    """The three interior angles in degrees, in the order of the points given."""
    a, b, c = distance(q, r), distance(p, r), distance(p, q)
    return tuple(
        math.degrees(math.acos((y * y + z * z - x * x) / (2 * y * z)))
        for x, y, z in [(a, b, c), (b, a, c), (c, a, b)]
    )
```

For $(0, 0)$, $(1, 0)$ and $\left(0.5, \dfrac{\sqrt{3}}{2}\right)$, it
gives 60, 60 and 60, apart from tiny floating-point errors.

The rearranged cosine rule is the right tool, because it works from
three sides and never runs into the ambiguous case. `acos` returns a
value between 0° and 180°, and that is exactly the range an inside angle
can have. So the doubt that troubles the sine rule cannot happen here.

The three angles must add up to 180°, so you get an extra test with no
extra work. Use an `assert` for it, instead of checking by eye.

</details>
