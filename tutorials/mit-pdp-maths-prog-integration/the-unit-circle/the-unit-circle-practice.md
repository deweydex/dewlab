---
title: "The Unit Circle — Practice"
slug: the-unit-circle-practice
practice_for: the-unit-circle
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# The Unit Circle — Practice

Work through these with the tutorial open beside you if you want it. Every answer is on this page, folded — click to see it, and try not to click until you have written something down.

There is a checking cell at the top of each section. You do not need one problem per cell; you need one tool per section, and then you can test anything.

## Degrees and Radians

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

**1.** Convert to radians, as a multiple of π: 90°, 180°, 45°, 60°, 30°, 270°, 360°.

<details class="dl-answer"><summary>answer</summary>

π/2, π, π/4, π/3, π/6, 3π/2, 2π.

The pattern to hold on to is that 180° is π, and everything else is a fraction of that.

</details>

**2.** Convert to degrees: π/6, 3π/4, 5π/3, 2π/5.

<details class="dl-answer"><summary>answer</summary>

30°, 135°, 300°, 72°.

</details>

**3.** One radian is about how many degrees? Answer before computing it.

<details class="dl-answer"><summary>answer</summary>

About 57.3°. Worth remembering as a rough check: a radian is a bit under 60 degrees, so if a conversion gives you something wildly off that scale you have multiplied where you should have divided.

</details>

**4.** A student writes `math.sin(30)` expecting 0.5 and gets −0.988. What went wrong, and what should they have written?

<details class="dl-answer"><summary>answer</summary>

`math.sin` takes radians. They asked for the sine of 30 *radians*, which is nearly five full turns round the circle and lands somewhere near the bottom.

They wanted `math.sin(math.radians(30))`, or `math.sin(math.pi / 6)`.

</details>

**5.** Without computing: is `sin(2)` positive or negative? (The 2 is in radians.)

<details class="dl-answer"><summary>answer</summary>

Positive. Two radians is about 115°, which is in the top-left quarter of the circle — past the top but not yet down to the horizontal — so the up value is still positive.

</details>

## Arc Length, and What a Radian Is For

The reason radians are worth the trouble: for a circle of radius `r`, the distance along the edge through an angle of `θ` radians is simply `s = rθ`. No conversion factor anywhere.

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

**6.** A circle has radius 10 cm. Find the arc length for a central angle of π/2, of π, and of 2π. What should the last one be?

<details class="dl-answer"><summary>answer</summary>

5π ≈ 15.71 cm, 10π ≈ 31.42 cm, and 20π ≈ 62.83 cm.

The last one is the whole way round, so it should be the circumference — and `2πr` with `r = 10` is exactly what `s = rθ` gives when `θ = 2π`. The formula contains the circumference formula as its full-turn case.

</details>

**7.** The Earth's radius is about 6,371 km. If you travel along the surface through an angle of one radian, how far have you gone?

<details class="dl-answer"><summary>answer</summary>

6,371 km — the radius itself.

That is the definition of a radian, and it is worth seeing at this scale: one radian of the Earth is roughly the distance from Ireland to the middle of the Sahara.

</details>

**8.** Dublin is at latitude 53.3°N. How far is it from the equator, along the surface?

<details class="dl-answer"><summary>answer</summary>

53.3° is 0.9302 radians, so `s = 6371 × 0.9302 ≈ 5,926 km`.

</details>

**9.** Around 240 BCE, Eratosthenes noticed that at noon on the solstice the sun shone straight down a well in Syene, while 800 km north in Alexandria it cast a shadow at 7.2° from vertical. Use `s = rθ` to estimate the Earth's radius from those two numbers.

<details class="dl-answer"><summary>answer</summary>

7.2° is 0.1257 radians. Then `r = s/θ = 800 / 0.1257 ≈ 6,366 km`.

The modern figure is 6,371 km. He was within about 0.1%, in 240 BCE, using a stick and a well — which is one of the better arguments for taking a simple idea seriously.

</details>

**10.** The Moon's angular diameter — how wide it looks in the sky — is about 0.52°. It is about 384,400 km away. Estimate its actual diameter, treating the diameter as an arc.

<details class="dl-answer"><summary>answer</summary>

0.52° is 0.00908 radians, so `s = 384400 × 0.00908 ≈ 3,490 km`.

The actual figure is 3,474 km, so the estimate is within half a percent. The approximation involved — treating a straight diameter as a curved arc — barely matters at angles this small.

</details>

**11.** The Sun's angular diameter is about 0.53°, almost the same as the Moon's, and it is about 150 million km away. Estimate its diameter. What does the near-equality of those two angles let happen?

<details class="dl-answer"><summary>answer</summary>

0.53° is 0.00925 radians, so `s = 150,000,000 × 0.00925 ≈ 1.39 million km`. The Sun's actual diameter is about 1.392 million km.

The coincidence that the Sun and Moon look almost exactly the same size from Earth is what makes total solar eclipses possible — the Moon covers the Sun's disc almost exactly, which is why the corona becomes visible.

</details>

## The Circle Itself

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

**12.** Give the exact coordinates on the unit circle at 0°, 30°, 45°, 60° and 90°.

<details class="dl-answer"><summary>answer</summary>

| Angle | across (cos) | up (sin) |
|---|---|---|
| 0° | 1 | 0 |
| 30° | √3⁄2 | 1⁄2 |
| 45° | √2⁄2 | √2⁄2 |
| 60° | 1⁄2 | √3⁄2 |
| 90° | 0 | 1 |

There is a pattern in the sine column worth noticing: √0⁄2, √1⁄2, √2⁄2, √3⁄2, √4⁄2. The cosine column is the same list backwards, which is the same triangle seen from its other corner.

</details>

**13.** In which quarter of the circle is the across value negative and the up value positive?

<details class="dl-answer"><summary>answer</summary>

The second — top left, between 90° and 180°. You are above the horizontal axis, so up is positive, and to the left of the vertical one, so across is negative.

</details>

**14.** Give the exact coordinates at 120°, 135° and 150°.

<details class="dl-answer"><summary>answer</summary>

120°: (−1⁄2, √3⁄2). 135°: (−√2⁄2, √2⁄2). 150°: (−√3⁄2, 1⁄2).

Each is the mirror of the first-quarter value at 180 minus the angle, with the across value made negative. 120° mirrors 60°, 135° mirrors 45°, 150° mirrors 30°.

</details>

**15.** Show that `sin²θ + cos²θ = 1` at 30°, without a calculator.

<details class="dl-answer"><summary>answer</summary>

sin 30° = 1⁄2, so sin² = 1⁄4. cos 30° = √3⁄2, so cos² = 3⁄4. And 1⁄4 + 3⁄4 = 1.

Which is Pythagoras: the point is 1 from the centre, so its two coordinates squared add to 1.

</details>

**16.** Given that `cos θ = 4/5` and θ is in the first quarter, find `sin θ` exactly.

<details class="dl-answer"><summary>answer</summary>

sin²θ = 1 − (4/5)² = 1 − 16/25 = 9/25, so sin θ = 3/5.

Positive, because the first quarter has both coordinates positive. This is the 3-4-5 triangle, scaled to fit inside the unit circle.

</details>

**17.** Why is `0.7071` not a satisfactory answer for cos 45°?

<details class="dl-answer"><summary>answer</summary>

Because it is wrong, by a small amount. `√2⁄2` squared is exactly 0.5; `0.7071` squared is 0.49999041.

For most purposes that does not matter. It matters when the small error is squared, or multiplied by something large, or accumulated over many steps — and the exact form costs nothing to write.

</details>

**18.** Which is bigger, `sin 89°` or `sin 91°`? Answer from the circle before computing.

<details class="dl-answer"><summary>answer</summary>

They are equal.

The up value peaks at 90° and comes back down symmetrically, so 89° and 91° are the same height. That symmetry is exactly what makes the Sine Rule ambiguous — see *Solving Triangles*.

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

**19.** Find the exact value of tan 45°, tan 30° and tan 60°.

<details class="dl-answer"><summary>answer</summary>

tan 45° = 1, because the across and up values are equal there.

tan 30° = (1⁄2) ÷ (√3⁄2) = 1/√3 = √3⁄3.

tan 60° = (√3⁄2) ÷ (1⁄2) = √3.

The last two are reciprocals of each other, for the same reason 30° and 60° swap their coordinates.

</details>

**20.** What is tan 90°, and why?

<details class="dl-answer"><summary>answer</summary>

It has no value. At 90° the point is at (0, 1), so the across value is zero, and tangent is up divided by across.

Geometrically: tangent is the slope of the line from the origin to the point, and at 90° that line is vertical. A vertical line has no slope — the same fact that `y = mx + c` could not express in *Lines and Distances*.

</details>

**21.** A ramp rises 1 m over a horizontal distance of 12 m. What angle does it make with the ground?

<details class="dl-answer"><summary>answer</summary>

tan θ = 1/12, so θ = arctan(1/12) ≈ 4.76°.

For reference, building regulations for wheelchair ramps typically ask for no more than about 1 in 12 — which is where that number came from.

</details>

**22.** Light entering glass bends, and how much depends on the refractive index. If a beam hits at 30° from the vertical and the glass has an index of 1.5, the bend angle satisfies `sin(30°) = 1.5 × sin(θ)`. Find θ.

<details class="dl-answer"><summary>answer</summary>

sin θ = sin(30°)/1.5 = 0.5/1.5 = 0.3333, so θ ≈ 19.47°.

The beam bends towards the vertical on entering a denser medium. This is Snell's Law, and it is the reason a straw looks bent in a glass of water.

</details>

## Putting It Together

**23.** A wheel of radius 35 cm turns through 4 radians. How far has a point on its rim travelled, and how far has the wheel rolled along the ground?

<details class="dl-answer"><summary>answer</summary>

Both are 140 cm — `s = rθ = 35 × 4`.

They are the same because rolling without slipping means the arc that touches the ground is exactly the distance covered. That equality is why `s = rθ` shows up in every problem about wheels, gears and belts.

</details>

**24.** A point starts at (1, 0) on the unit circle and moves anticlockwise by 7π/6 radians. Where does it end up, exactly?

<details class="dl-answer"><summary>answer</summary>

7π/6 is 210°, which is in the third quarter — both coordinates negative. It is 30° past the horizontal, so the coordinates are the 30° pair with both signs flipped: (−√3⁄2, −1⁄2).

</details>

**25.** Explain, in one or two sentences and without any formulae, why a full turn is 2π radians.

<details class="dl-answer"><summary>answer</summary>

A radian is the angle you turn through when you walk a distance equal to the radius along the edge. The whole way round a circle is 2π radii — that is what π means. So a full turn is 2π radians.

It is not a conversion factor anybody chose. It is a measurement of the circle.

</details>
