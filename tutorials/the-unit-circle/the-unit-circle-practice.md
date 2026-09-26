---
title: "The unit circle: sine, cosine and tangent — Practice"
practice_for: the-unit-circle
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: A lighthouse beam, turning. The numbers are made up.
  planets-and-moons: The International Space Station going round the Earth.
  fantasy-maps: A catapult's arm, swinging up. The numbers are made up.
---

# The unit circle: sine, cosine and tangent — Practice

You can keep the tutorial open beside you while you do these.
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

Remember that 180° is $\pi$. Every other angle is a fraction of that.

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

Why are radians worth the trouble? Take a circle of
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
$s = r\theta$ gives when $\theta = 2\pi$. So the circumference formula
is the arc length formula for a full turn.

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
length you pick, his answer differs from the modern figure by between
about 2% and about 15%. Even so, he found the size of the whole Earth,
in 240 BCE, from a stick, a well and one angle.

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

From Earth, the Sun and Moon look almost exactly the same size. This
makes a total solar eclipse possible. The Moon covers the Sun's disc
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
The cosine column is the same list backwards. This happens because 30°
and 60° use the same triangle, seen from its other corner.

</details>

**13.** The cell prints the across value at 120°, rounded to four
places.

```python exec
id: the-circle-itself-2
print(round(math.cos(math.radians(120)), 4))
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints $-0.5$. 120° is in the top-left quarter, where the across
value is negative. It is 60° short of a half turn, so it is the 60°
point reflected in the vertical axis, and the 60° point is
$\left(rac{1}{2}, rac{\sqrt{3}}{2}ight)$.

</details>

**14.** The tutorial's `walk` took 10,000 tiny steps. What happens with
far fewer? Here is `walk` again. Can you try a quarter turn with 10
steps, then 100, then 4? Where does the tip stop, and why is it short of
the top?

```python exec
id: the-circle-itself-3
def walk(distance_round, steps=10000):
    """Walk the tip from (1, 0), anticlockwise, this far round the circle."""
    x, y = 1.0, 0.0
    step = distance_round / steps
    for _ in range(steps):
        x, y = x - step * y, y + step * x
        size = math.sqrt(x ** 2 + y ** 2)
        x, y = x / size, y / size
    return x, y


print(walk(2 * math.pi / 4, steps=10))
```

<details class="dl-answer"><summary>why</summary>

With 10 steps the tip stops at about $(0.0127, 0.9999)$, a little short
of $(0, 1)$. With 100 steps it is at about $(0.0001, 1.0)$, and with 4
steps at about $(0.074, 0.997)$.

Each step goes in a straight line, at right angles to the hand, and then
the tip is pulled back to the circle. Pulling it back loses a little of
the turn. A straight step of length 0.157 turns the hand by only about
0.156. The smaller the steps, the less each one loses, so more steps
come closer to the top.

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

**17.** Why do we write $\frac{\sqrt{2}}{2}$ for $\cos 45^\circ$, and not
$0.7071$?

<details class="dl-answer"><summary>answer</summary>

Because $0.7071$ is a little too small. $\frac{\sqrt{2}}{2}$ squared is
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
the other side. So 89° and 91° are at the same height. This symmetry
makes the sine rule ambiguous. You will meet that in
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

Problems 21 and 22 go the other way. They give you the tangent or the
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
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines).

</details>

**21.** A ramp rises 1 m over a horizontal distance of 12 m. What angle
does it make with the ground?

<details class="dl-answer"><summary>answer</summary>

$\tan\theta = \frac{1}{12}$, so $\theta = \tan^{-1}\left(\frac{1}{12}\right) \approx 4.76^\circ$.

In Python: `math.degrees(math.atan(1 / 12))`.

Building rules for wheelchair ramps often ask for a slope of no more than
about 1 in 12. This problem uses that number.

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
touches the ground is exactly the distance the wheel covers. So
$s = r\theta$ appears in every problem about wheels, gears and belts.

</details>

**24.** A point starts at $(1, 0)$ on the unit circle. It moves
anticlockwise by $\frac{7\pi}{6}$ radians. Where does it stop, exactly?

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
the radius along the edge. The whole way round a circle is $2\pi$ radii,
because of how $\pi$ is defined. So a full turn is $2\pi$ radians.

It is a measurement of the circle. It is not a conversion factor that
somebody chose.

</details>

## Your world

**26.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

A lighthouse beam turns anticlockwise once every 10 seconds, and it
lights the sea up to 20 km away. At 0 seconds it points east. Where on
the chart is the far end of the beam after 3 seconds? Can you write
`beam_end(seconds)`?

```python exec
id: your-world-1--sea-and-sky
turn_seconds = 10
reach = 20    # km
```

```hint
What fraction of a turn is 3 seconds? The far end is on a circle of
radius 20 round the lighthouse.
```

```inputs
beam_end(3)
beam_end(2.5)
beam_end(10)
```

```solution
def beam_end(seconds):
    angle = seconds / turn_seconds * 2 * math.pi
    return reach * math.cos(angle), reach * math.sin(angle)
---
After 3 seconds the beam has turned 108 degrees, and its far end is at
about $(-6.18, 19.02)$: a little west of the lighthouse, and far to the
north. After 2.5 seconds, a quarter turn, it points due north.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

The International Space Station goes round the Earth about once every
92 minutes, about 6,780 km from the Earth's centre. How far along its
circle does it travel in 10 minutes? A walk round a circle of radius
$r$, through an angle of $\theta$ radians, is $r\theta$ long. Can you
write `travelled(minutes)`?

```python exec
id: your-world-1--planets-and-moons
orbit_minutes = 92
orbit_km = 6780
```

```hint
First find the angle, in radians, for 10 minutes. A full turn is
$2\pi$ radians.
```

```inputs
travelled(10)
travelled(92)
travelled(10) / (10 * 60)
```

```solution
def travelled(minutes):
    angle = minutes / orbit_minutes * 2 * math.pi
    return orbit_km * angle
---
In 10 minutes the station turns through about 0.68 radians and travels
about 4,630 km. The last line divides by the 600 seconds in 10 minutes:
the station moves about 7.7 km every second.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A catapult's arm is 4 m long, with its pivot 1.5 m above the ground. The
arm starts flat and swings up. At 70 degrees it lets the stone go. How
high is the stone then, and how far in front of the pivot? Can you
write `stone_at(degrees)`?

```python exec
id: your-world-1--fantasy-maps
arm = 4           # metres
pivot_height = 1.5
```

```hint
The end of the arm is on a circle of radius 4 round the pivot. The
height adds the pivot's own height.
```

```inputs
stone_at(70)
stone_at(0)
stone_at(90)
```

```solution
def stone_at(degrees):
    angle = math.radians(degrees)
    return arm * math.cos(angle), pivot_height + arm * math.sin(angle)
---
At 70 degrees the stone is about 1.37 m in front of the pivot and about
5.26 m above the ground.
```

</div>

## From earlier

**27.** From
[Distance and Pythagoras: how far apart two points are](tutorial:distance-and-pythagoras).
Is the point $(0.6, 0.8)$ on the unit circle? What about $(0.5, 0.5)$?

<details class="dl-answer"><summary>answer</summary>

A point is on the unit circle when its distance from $(0, 0)$ is 1.
$\sqrt{0.36 + 0.64} = 1$, so $(0.6, 0.8)$ is on it. It is the 3-4-5
triangle again, made smaller. $\sqrt{0.25 + 0.25} \approx 0.707$, so
$(0.5, 0.5)$ is inside the circle.

</details>

**28.** From [Complex numbers: roots that are not real](tutorial:complex-roots).
What will `(0.6 + 0.8j) * 1j` print? Where is that point on the unit
circle?

```python exec
id: from-earlier-1
print((0.6 + 0.8j) * 1j)
```

<details class="dl-answer"><summary>answer</summary>

It prints `(-0.8+0.6j)`, the point $(-0.8, 0.6)$. Multiplying by $i$ is
a quarter turn, so the point has moved a quarter of the way round the
circle, anticlockwise. It is still 1 from the centre.

</details>

## Where to read more

Stand-up Maths (2022). *What is wrong with this sine memorisation
pattern?* <https://www.youtube.com/watch?v=PDLQadz1KCc>. This video shows
a popular pattern for remembering the sines of the landmark angles. Check
it against your own values first. Then watch Matt Parker ask what is
wrong with it. It is about twelve minutes long.
