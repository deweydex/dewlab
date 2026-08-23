---
title: "Mixed Problems — Trigonometry and Geometry"
slug: mixed-trigonometry
practice_across:
  - lines-and-distances
  - the-unit-circle
  - sine-and-cosine-waves
  - solving-triangles
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Mixed Problems — Trigonometry and Geometry

Coordinates, angles, triangles and waves are four views of the same circle. These problems move between them, usually without saying so.

Answers are folded. Draw the situation before you calculate — in this topic more than any other, the picture is where the mistakes become visible.

## Tools

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

## Coordinates and Angles

**1.** A point sits at $(3, 4)$. How far is it from the origin, and at what angle?

<details class="dl-answer"><summary>answer</summary>

5 units, at about 53.13°.

The distance is Pythagoras. The angle is $\arctan(4/3)$.

These two numbers are the polar coordinates of the point, and converting between $(x, y)$ and $(r, \theta)$ is the same arithmetic as converting between a triangle's sides and its angles. They are the same problem.

</details>

**2.** Convert $(r, \theta) = (10, 30°)$ back to $x$ and $y$.

<details class="dl-answer"><summary>answer</summary>

$(8.66, 5)$.

$x = r\cos\theta$, $y = r\sin\theta$. With $\cos 30° = \frac{\sqrt3}{2}$ and $\sin 30° = \frac12$, that is $5\sqrt3$ and 5 exactly.

This is the unit circle scaled by 10 — which is what the unit circle is for.

</details>

**3.** Why is `atan2(y, x)` preferred to `atan(y/x)`?

<details class="dl-answer"><summary>answer</summary>

Because dividing loses the quadrant.

$\frac{4}{3}$ and $\frac{-4}{-3}$ are the same number, so `atan` cannot tell $(3, 4)$ from $(-3, -4)$ — it returns 53.13° for both, and one of them is at 233.13°.

`atan2` takes the two values separately and keeps the signs, so it returns the correct angle anywhere in the circle. It also survives $x = 0$, which the division does not.

</details>

**4.** A robot at $(2, 3)$ must face a target at $(7, 15)$. What heading, and how far?

<details class="dl-answer"><summary>answer</summary>

About 67.38°, and 13 units.

The gaps are 5 across and 12 up — a 5-12-13 triangle, which is worth recognising alongside 3-4-5.

</details>

## Triangles

**5.** A triangle has sides 7 and 9 with an angle of 40° between them. Find the third side and the remaining angles.

<details class="dl-answer"><summary>answer</summary>

Third side about 5.80; the other angles about 51.0° and 89.0°.

The cosine rule gives the side: $c^2 = 49 + 81 - 2(7)(9)\cos 40°$.

Then the sine rule gives an angle — but use it on the *shorter* remaining side. The sine rule cannot tell an acute angle from its obtuse partner, and taking the smaller side guarantees the acute one is right.

</details>

**6.** A triangle has sides 5, 12 and 13. Is it right-angled? What is its area?

<details class="dl-answer"><summary>answer</summary>

Yes: $25 + 144 = 169$. The area is 30.

For a right triangle the area is half the product of the two short sides. Heron's formula gives the same 30 without knowing it is right-angled, which is the point of Heron's formula.

</details>

**7.** Two sides of a triangle are 8 and 5, and the angle opposite the 5 is 30°. Find the third side.

<details class="dl-answer"><summary>answer</summary>

There are two answers: about 9.93 and about 3.93.

$\sin \theta = \frac{8 \sin 30°}{5} = 0.8$, so the angle opposite the 8 is either 53.13° or 126.87° — both have a sine of 0.8.

This is the ambiguous case, and it is genuinely ambiguous: two different triangles satisfy everything you were told. Drawing it shows why — swinging the 5 from the end of the 8 crosses the base twice.

The unit circle explains it in one line: sine is symmetric about 90°, so $\sin\theta$ never says which side of it you are on.

</details>

**8.** Find the area of a triangle with corners $(0,0)$, $(6,0)$ and $(2,5)$, three ways.

<details class="dl-answer"><summary>answer</summary>

15, every time.

Base times height over two: the base is 6 along the axis, the height is 5.

Heron: sides are 6, $\sqrt{29}$ and $\sqrt{41}$; $s \approx 8.89$, and the formula gives 15.

The coordinate formula: $\frac12|x_1(y_2-y_3) + x_2(y_3-y_1) + x_3(y_1-y_2)| = \frac12|0 + 6(5) + 2(0)| = 15$.

Three routes agreeing is the sort of check worth building the habit of.

</details>

## Waves

**9.** For $y = 3\sin(2x)$, give the amplitude, period and where it first crosses zero going upwards after $x = 0$.

<details class="dl-answer"><summary>answer</summary>

Amplitude 3, period $\pi$, and it crosses upwards at $x = 0$ itself and again at $\pi$.

The 3 stretches vertically; the 2 squashes horizontally, halving the period from $2\pi$ to $\pi$. The number inside does the opposite of what it looks like it should, which catches everybody once.

</details>

**10.** Sketch $y = \sin x$ and $y = \cos x$ together. How far apart are they?

<details class="dl-answer"><summary>answer</summary>

A quarter turn: $\cos x = \sin(x + \frac{\pi}{2})$.

They are the same wave started at a different point — which is what the unit circle says, since cosine is the across value and sine the up value of the same rotating point.

</details>

**11.** The tide at a harbour is roughly $h = 3 + 2\sin\left(\frac{2\pi t}{12.4}\right)$ metres, with $t$ in hours. Find the high and low water depths and the time between successive high waters.

<details class="dl-answer"><summary>answer</summary>

High 5 m, low 1 m, and 12.4 hours between highs.

The 3 is the mean level, the 2 is the amplitude, and the period is $\frac{2\pi}{2\pi/12.4}$.

12.4 hours rather than 12 is why high tide drifts about 50 minutes later each day: the tide follows the moon, and the moon is not on a 24-hour cycle.

</details>

**12.** A boat needs 4 m of water. Using the tide above, for how long each cycle can it enter?

<details class="dl-answer"><summary>answer</summary>

About 4.13 hours per cycle.

Solve $3 + 2\sin(\frac{2\pi t}{12.4}) \ge 4$, so $\sin(\cdot) \ge 0.5$, so the angle is between 30° and 150° — a third of a full turn.

A third of 12.4 is 4.13. The answer came from the unit circle rather than from any calculation about boats, which is the useful part.

</details>

**13.** Show that $\sin^2\theta + \cos^2\theta = 1$ for several angles, and say why it must be true.

<details class="dl-answer"><summary>answer</summary>

```python
for d in [0, 17, 45, 90, 137, 250, 359]:
    a = math.radians(d)
    print(d, round(math.sin(a) ** 2 + math.cos(a) ** 2, 12))
```

All 1.0.

It is Pythagoras on the unit circle. The point is at distance 1 from the centre, and its two coordinates are the two short sides of a right triangle with hypotenuse 1.

Every trigonometric identity is a fact about that circle written in a different notation, and this is the one the rest are built from.

</details>

## Longer Ones

**14.** Three phone masts are at $(0,0)$, $(10,0)$ and $(4,8)$, in kilometres. A phone is 6 km from the first and 7 km from the second. Where might it be, and does the third mast settle it?

<details class="dl-answer"><summary>answer</summary>

Two possible positions: about $(4.35, 4.13)$ and $(4.35, -4.13)$.

Two circles cross at two points, so two distances are never enough. The third mast picks one: the phone is 3.88 km from $(4, 8)$ if it is above the axis and 12.14 km if below, and those are very different measurements.

This is trilateration, and it is how satellite positioning works. Three satellites give a position on the surface; a fourth is needed because the receiver's clock is also unknown.

</details>

**15.** A ladder 6 m long leans against a wall at 70° to the ground. How high does it reach, and how far out is its foot? If the foot slips out 0.5 m, what angle is it at then?

<details class="dl-answer"><summary>answer</summary>

It reaches 5.64 m up, with its foot 2.05 m out.

After slipping to 2.55 m out, the angle is $\arccos(2.55/6) \approx 64.8°$ and it now reaches 5.43 m.

Half a metre of slip costs five degrees and twenty centimetres of height. The relationship is not linear, and it gets much worse as the angle drops — which is the argument for the 4-to-1 rule about ladders.

</details>

**16.** A wheel of radius 0.35 m turns at 60 revolutions per minute. How fast is a point on the rim moving, and how far does the wheel travel in a minute?

<details class="dl-answer"><summary>answer</summary>

About 2.20 m/s, and about 132 m per minute.

One revolution is $2\pi$ radians, so 60 rpm is $2\pi$ radians per second. Then $v = r\omega = 0.35 \times 2\pi \approx 2.199$ m/s.

Rolling without slipping means the rim speed and the ground speed are the same, which is the whole reason $s = r\theta$ is useful for anything mechanical.

</details>

**17.** Two points on a circle of radius 5 are 6 apart in a straight line. What is the angle between them at the centre, and how far apart are they along the arc?

<details class="dl-answer"><summary>answer</summary>

About 1.287 radians (73.7°), and about 6.44 along the arc.

The chord, the radius and the radius form an isosceles triangle. Half of it is a right triangle with hypotenuse 5 and opposite side 3, so half the angle is $\arcsin(0.6) \approx 0.6435$.

The arc is $r\theta = 5 \times 1.287$. It is longer than the chord, as it must be — the straight line is the short way.

</details>

**18.** Write a function that takes three points and returns the three interior angles of the triangle they form. Test it on an equilateral one.

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

For $(0,0)$, $(1,0)$ and $(0.5, \sqrt{3}/2)$ it gives 60, 60, 60 — to within floating-point noise.

The cosine rule rearranged is the right tool, because it works from three sides and never runs into the ambiguous case. `acos` returns a value between 0 and 180°, which is exactly the range an interior angle can occupy — so the ambiguity that plagues the sine rule cannot arise here.

Checking that the three sum to 180 is a free test, and it is worth asserting rather than eyeballing.

</details>
