---
title: "The unit circle: sine, cosine and tangent — Practice"
practice_for: the-unit-circle
year: "2026-2027"
version: 2026.08.23.1
---

# The unit circle: sine, cosine and tangent — Practice

You can keep the tutorial open beside you while you work through these.
Every answer is on this page, hidden. Click to see it, but try to write
something down first.

Each section starts with a checking cell. You do not need a new cell for
every problem. The one cell gives you the tools for that section, and you
can change it to test anything.

## Degrees and radians

```python exec
id: degrees-and-radians-1
import math

def to_radians(degrees):
    return degrees * math.pi / 180


def to_degrees(radians):
    return radians * 180 / math.pi


def as_fraction_of_pi(radians):
    """Show a radian value as a multiple of pi, which is how they are written."""
    ratio = radians / math.pi
    return f"{ratio:.6g} pi"


# Change these and run it as often as you like.
print(to_radians(90), "=", as_fraction_of_pi(to_radians(90)))
print(to_degrees(math.pi / 4), "degrees")
```

**1.** Convert each angle to radians, as a multiple of $\pi$: 90°, 180°,
45°, 60°, 30°, 270°, 360°.

<details class="dl-answer"><summary>answer</summary>

$\frac{\pi}{2}$, $\pi$, $\frac{\pi}{4}$, $\frac{\pi}{3}$, $\frac{\pi}{6}$,
$\frac{3\pi}{2}$, $2\pi$.

The pattern to remember: 180° is $\pi$, and every other angle is a
fraction of that.

</details>

**2.** Convert each angle to degrees: $\frac{\pi}{6}$, $\frac{3\pi}{4}$,
$\frac{5\pi}{3}$, $\frac{2\pi}{5}$.

<details class="dl-answer"><summary>answer</summary>

30°, 135°, 300°, 72°.

</details>

**3.** One radian is about how many degrees? Try to answer before you
compute it.

<details class="dl-answer"><summary>answer</summary>

About 57.3°. This is useful as a rough check. A radian is a little under
60 degrees. If a conversion gives you an answer very far from that scale,
you have probably multiplied where you should have divided.

</details>

**4.** A student writes `math.sin(30)`. They expect 0.5, but they get
−0.988. What went wrong? What should they have written?

<details class="dl-answer"><summary>answer</summary>

`math.sin` takes radians. The student asked for the sine of 30
*radians*. That is nearly five full turns round the circle, and it lands
near the bottom.

They wanted `math.sin(math.radians(30))`, or `math.sin(math.pi / 6)`.

</details>

**5.** Is $\sin 2$ positive or negative? The 2 is in radians. Can you
answer without computing it?

<details class="dl-answer"><summary>answer</summary>

Positive. Two radians is about 115°. That is in the top-left quarter of
the circle: past the top, but not yet down to the horizontal axis. So the
up value is still positive.

</details>

## Arc length, and what a radian is for

Why are radians worth the trouble? Here is the reason. Take a circle of
radius $r$, and walk along its edge through an angle of $\theta$
radians. The distance you walk is the *arc length*, $s$, and it is the
radius times the angle:

$$s = r\theta$$

There is no conversion factor anywhere. For example, on a circle of
radius 10 an angle of 2 radians gives an arc of $10 \times 2 = 20$.

```python exec
id: arc-length-and-what-a-radian-is-for-1
import math

def arc_length(radius, radians):
    return radius * radians


def angle_from_arc(radius, arc):
    return arc / radius


print(arc_length(10, math.pi))
print(angle_from_arc(10, 31.4159))
```

**6.** A circle has radius 10 cm. Find the arc length for a central angle
of $\frac{\pi}{2}$, of $\pi$, and of $2\pi$. What should the last one be?

<details class="dl-answer"><summary>answer</summary>

$5\pi \approx 15.71$ cm, $10\pi \approx 31.42$ cm, and
$20\pi \approx 62.83$ cm.

The last one is the whole way round, so it should be the circumference.
The circumference is $2\pi r$, and with $r = 10$ that is exactly what
$s = r\theta$ gives when $\theta = 2\pi$. So the arc length formula
contains the circumference formula: it is the full-turn case.

</details>

**7.** The Earth's radius is about 6,371 km. Suppose you travel along the
surface through an angle of one radian. How far have you gone?

<details class="dl-answer"><summary>answer</summary>

6,371 km, the radius itself.

That is the definition of a radian, and it is interesting to see it at
this size. One radian of the Earth is a little further than the distance
from Dublin to Chicago, which is about 5,900 km.

</details>

**8.** Dublin is at latitude 53.3°N. How far is it from the equator,
along the surface?

<details class="dl-answer"><summary>answer</summary>

53.3° is 0.9302 radians, so $s = 6371 \times 0.9302 \approx 5926$ km.

</details>

**9.** Around 240 BCE, a Greek scholar called Eratosthenes noticed
something at noon on the longest day of the year. In the town of Syene,
the sun shone straight down a well. In Alexandria, 800 km to the north,
the sun cast a shadow at 7.2° from vertical. How can you use $s = r\theta$
to estimate the Earth's radius from those two numbers?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

The 800 km is the arc, $s$, and the 7.2° is the angle, $\theta$. Convert
the angle to radians first, then rearrange: $r = \frac{s}{\theta}$.

</details>

<details class="dl-answer"><summary>answer</summary>

7.2° is 0.1257 radians. Then
$r = \frac{s}{\theta} = \frac{800}{0.1257} \approx 6366$ km.

The modern figure is 6,371 km, so this answer is within about 0.1%.
Be careful with that 0.1%, though. It depends on the 800 km, and the
800 km is ours. Eratosthenes gave the distance as 5,000 stadia, a
Greek unit of length, and nobody knows exactly how long his stadion
was. Depending on which
length you pick, his answer was somewhere between about 2% and about
15% out. Even so, he found the size of the whole Earth, in 240 BCE,
from a stick, a well and one angle. That is a good reason to take a
simple idea seriously.

</details>

**10.** The Moon's *angular diameter* is how wide it looks in the sky,
measured as an angle. It is about 0.52°. The Moon is about 384,400 km
away. Estimate its real diameter, treating the diameter as an arc.

<details class="dl-answer"><summary>answer</summary>

0.52° is 0.00908 radians, so $s = 384400 \times 0.00908 \approx 3490$ km.

The real figure is 3,474 km, so the estimate is within half a percent.
We treated a straight diameter as a curved arc, but at an angle this
small the difference is tiny.

</details>

**11.** The Sun's angular diameter is about 0.53°, almost the same as the
Moon's. The Sun is about 150 million km away.

1. Estimate the Sun's diameter.
2. The two angles are almost equal. What does that make possible?

<details class="dl-answer"><summary>answer</summary>

0.53° is 0.00925 radians, so
$s = 150{,}000{,}000 \times 0.00925 \approx 1.39$ million km. The Sun's
real diameter is about 1.392 million km.

From Earth, the Sun and Moon look almost exactly the same size. That is
what makes a total solar eclipse possible. The Moon covers the Sun's disc
almost exactly, and so the corona, the Sun's faint outer glow, becomes
visible.

</details>

## The circle itself

```python exec
id: the-circle-itself-1
import math

def unit_point(degrees):
    angle = math.radians(degrees)
    return (math.cos(angle), math.sin(angle))


for d in [0, 30, 45, 60, 90]:
    x, y = unit_point(d)
    print(f"{d:>4} degrees:  across {x:>8.5f}   up {y:>8.5f}")
```

**12.** Give the exact coordinates on the unit circle at 0°, 30°, 45°,
60° and 90°.

<details class="dl-answer"><summary>answer</summary>

| Angle | across ($\cos$) | up ($\sin$) |
|---|---|---|
| 0° | $1$ | $0$ |
| 30° | $\frac{\sqrt{3}}{2}$ | $\frac{1}{2}$ |
| 45° | $\frac{\sqrt{2}}{2}$ | $\frac{\sqrt{2}}{2}$ |
| 60° | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ |
| 90° | $0$ | $1$ |

Look for a pattern in the sine column:
$\frac{\sqrt{0}}{2}, \frac{\sqrt{1}}{2}, \frac{\sqrt{2}}{2}, \frac{\sqrt{3}}{2}, \frac{\sqrt{4}}{2}$.
The cosine column is the same list backwards. That is the same triangle,
seen from its other corner.

</details>

**13.** In which quarter of the circle is the across value negative and
the up value positive?

<details class="dl-answer"><summary>answer</summary>

The second quarter: top left, between 90° and 180°. There you are above
the horizontal axis, so up is positive. You are also to the left of the
vertical axis, so across is negative.

</details>

**14.** Give the exact coordinates at 120°, 135° and 150°.

<details class="dl-answer"><summary>answer</summary>

120°: $\left(-\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$.
135°: $\left(-\frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2}\right)$.
150°: $\left(-\frac{\sqrt{3}}{2}, \frac{1}{2}\right)$.

Each one is a mirror image of a first-quarter point: the point at 180°
minus the angle, with the across value made negative. So 120° mirrors
60°, 135° mirrors 45°, and 150° mirrors 30°.

</details>

**15.** Show that $\sin^2\theta + \cos^2\theta = 1$ at 30°, without a
calculator.

<details class="dl-answer"><summary>answer</summary>

$\sin 30^\circ = \frac{1}{2}$, so $\sin^2 30^\circ = \frac{1}{4}$.
$\cos 30^\circ = \frac{\sqrt{3}}{2}$, so $\cos^2 30^\circ = \frac{3}{4}$.
And $\frac{1}{4} + \frac{3}{4} = 1$.

This is Pythagoras. The point is at distance 1 from the centre, so its
two coordinates, squared, add up to 1.

</details>

**16.** We know that $\cos\theta = \frac{4}{5}$, and $\theta$ is in the
first quarter. Find $\sin\theta$ exactly.

<details class="dl-answer"><summary>answer</summary>

$\sin^2\theta = 1 - \left(\frac{4}{5}\right)^2 = 1 - \frac{16}{25} = \frac{9}{25}$,
so $\sin\theta = \frac{3}{5}$.

The answer is positive, because in the first quarter both coordinates are
positive. This is the 3-4-5 triangle, made smaller to fit inside the unit
circle.

</details>

**17.** Why is $0.7071$ not a good enough answer for $\cos 45^\circ$?

<details class="dl-answer"><summary>answer</summary>

Because it is wrong, by a small amount. $\frac{\sqrt{2}}{2}$ squared is
exactly $0.5$, but $0.7071$ squared is $0.49999041$.

For most purposes that does not matter. It does matter when the small
error is squared, or multiplied by something large, or added up over many
steps. And the exact form costs nothing to write.

</details>

**18.** Which is bigger, $\sin 89^\circ$ or $\sin 91^\circ$? Answer from
the circle before you compute it.

<details class="dl-answer"><summary>answer</summary>

They are equal.

The up value is highest at 90°, and it comes back down in the same way on
the other side. So 89° and 91° are at the same height. This symmetry is
what makes the sine rule ambiguous. You will meet that in
[Solving triangles: the sine rule and the cosine rule](tutorial:solving-triangles).

</details>

## Tangent

```python exec
id: tangent-1
import math

def tan_from_coordinates(degrees):
    x, y = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return y / x


for d in [0, 30, 45, 60, 80]:
    print(f"tan({d:>3}) = {tan_from_coordinates(d):>10.5f}"
          f"    math.tan gives {math.tan(math.radians(d)):>10.5f}")
```

Problems 21 and 22 go the other way: they give you the tangent or the
sine, and ask for the angle. The function that does this is called an
inverse. The inverse tangent is written $\tan^{-1}$ or arctan, and in
Python it is `math.atan`. The inverse sine is $\sin^{-1}$ or arcsin, and
in Python it is `math.asin`. Both give their answer in radians, so use
`math.degrees` to turn it into degrees. For example,
`math.degrees(math.atan(1))` gives 45.0.

**19.** Find the exact values of $\tan 45^\circ$, $\tan 30^\circ$ and
$\tan 60^\circ$.

<details class="dl-answer"><summary>answer</summary>

$\tan 45^\circ = 1$, because the across and up values are equal there.

$\tan 30^\circ = \frac{1}{2} \div \frac{\sqrt{3}}{2} = \frac{1}{\sqrt{3}} = \frac{\sqrt{3}}{3}$.

$\tan 60^\circ = \frac{\sqrt{3}}{2} \div \frac{1}{2} = \sqrt{3}$.

The last two are reciprocals of each other: each is 1 divided by the
other. That happens for the same reason that 30° and 60° swap their
coordinates.

</details>

**20.** What is $\tan 90^\circ$, and why?

<details class="dl-answer"><summary>answer</summary>

It has no value. At 90° the point is at $(0, 1)$, so the across value is
zero, and tangent is up divided by across.

We can also see it in the picture. Tangent is the slope of the line from
the origin to the point, and at 90° that line is vertical. A vertical line
has no slope. It is the same fact that $y = mx + c$ could not express in
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances).

</details>

**21.** A ramp rises 1 m over a horizontal distance of 12 m. What angle
does it make with the ground?

<details class="dl-answer"><summary>answer</summary>

$\tan\theta = \frac{1}{12}$, so $\theta = \tan^{-1}\left(\frac{1}{12}\right) \approx 4.76^\circ$.

In Python: `math.degrees(math.atan(1 / 12))`.

Building rules for wheelchair ramps often ask for a slope of no more than
about 1 in 12. That is where this number came from.

</details>

**22.** Light bends when it goes into glass. How much it bends depends on
the glass's *refractive index*. Suppose a beam hits the glass at 30° from
the vertical, and the glass has an index of 1.5. Then the new angle
$\theta$ satisfies $\sin 30^\circ = 1.5 \times \sin\theta$. Find
$\theta$.

<details class="dl-answer"><summary>answer</summary>

$\sin\theta = \frac{\sin 30^\circ}{1.5} = \frac{0.5}{1.5} = 0.3333$, so
$\theta = \sin^{-1}(0.3333) \approx 19.47^\circ$.

In Python: `math.degrees(math.asin(0.5 / 1.5))`.

The beam bends towards the vertical when it goes into a denser material.
This is called Snell's Law, and it is the reason a straw looks bent in a
glass of water.

</details>

## Putting it together

**23.** A wheel of radius 35 cm turns through 4 radians.

1. How far has a point on its rim travelled?
2. How far has the wheel rolled along the ground?

<details class="dl-answer"><summary>answer</summary>

Both are 140 cm: $s = r\theta = 35 \times 4 = 140$.

They are the same because the wheel rolls without slipping. The arc that
touches the ground is exactly the distance the wheel covers. That is why
$s = r\theta$ shows up in every problem about wheels, gears and belts.

</details>

**24.** A point starts at $(1, 0)$ on the unit circle. It moves
anticlockwise by $\frac{7\pi}{6}$ radians. Where does it end up, exactly?

<details class="dl-answer"><summary>answer</summary>

$\frac{7\pi}{6}$ is 210°. That is in the third quarter, where both
coordinates are negative. It is 30° past the horizontal axis, so the
coordinates are the 30° pair with both signs changed:
$\left(-\frac{\sqrt{3}}{2}, -\frac{1}{2}\right)$.

</details>

**25.** Why is a full turn $2\pi$ radians? Explain in one or two
sentences, without any formulae.

<details class="dl-answer"><summary>answer</summary>

A radian is the angle you turn through when you walk a distance equal to
the radius along the edge. The whole way round a circle is $2\pi$ radii;
that is what $\pi$ means. So a full turn is $2\pi$ radians.

It is a measurement of the circle. It is not a conversion factor that
somebody chose.

</details>
