---
title: "Solving triangles: the sine rule and the cosine rule — Practice"
practice_for: solving-triangles
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: A boat, a harbour and a lighthouse. The numbers are made up.
  planets-and-moons: How Aristarchus measured the Sun against the Moon.
  fantasy-maps: A made-up kingdom's fields, measured by their sides. The numbers are made up.
---

# Solving triangles: the sine rule and the cosine rule — Practice

The answers are hidden under each problem. Before you compute anything,
draw the triangle. Most mistakes in this topic come from mixing up which
side is opposite which angle, and a sketch helps you see it.

## Tools

This cell gives you the functions from the tutorial. Run it once before
you start.

```python exec
id: tools-1
import math

def cosine_rule_side(a, b, angle_degrees):
    """Two sides and the angle between them, giving the third side."""
    return math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(angle_degrees)))


def cosine_rule_angle(a, b, c):
    """All three sides, giving the angle opposite c."""
    return math.degrees(math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))


def sine_rule_side(known_side, known_angle, wanted_angle):
    ratio = known_side / math.sin(math.radians(known_angle))
    return ratio * math.sin(math.radians(wanted_angle))


def area(a, b, angle_degrees):
    return 0.5 * a * b * math.sin(math.radians(angle_degrees))


print(cosine_rule_side(5, 4, 60))
print(cosine_rule_angle(3, 4, 5))
print(area(7, 5, 50))
```

## Right-angled triangles

**1.** A right-angled triangle has short sides 5 and 12. Find the
hypotenuse and the other two angles.

<details class="dl-answer"><summary>answer</summary>

The hypotenuse is 13, by Pythagoras: $\sqrt{25 + 144} = \sqrt{169} = 13$.

The angle opposite the 5 is
$\tan^{-1}\left(\frac{5}{12}\right) \approx 22.62^\circ$. The other angle
is $90 - 22.62 = 67.38^\circ$.

5-12-13 is one of the well-known whole-number right-angled triangles,
together with 3-4-5 and 8-15-17. They are worth recognizing.

</details>

**2.** A ladder 6 m long leans against a wall. It makes an angle of 70°
with the ground.

1. How far up the wall does it reach?
2. How far from the wall is its foot?

<details class="dl-answer"><summary>answer</summary>

Up: $6\sin 70^\circ \approx 5.64$ m. Out: $6\cos 70^\circ \approx 2.05$ m.

</details>

**3.** A robot arm segment is 40 cm long and is raised at 35° from the
horizontal. Where is its tip, compared with the joint?

<details class="dl-answer"><summary>answer</summary>

Out: $40\cos 35^\circ \approx 32.77$ cm. Up: $40\sin 35^\circ \approx 22.94$ cm.

This is the point at 35° on the unit circle, made 40 times bigger. The
ratios do not depend on how long the arm is.

</details>

**4.** A screen is 1920 pixels wide and 1080 pixels tall. What angle
does its diagonal make with the horizontal?

<details class="dl-answer"><summary>answer</summary>

$\tan^{-1}\left(\frac{1080}{1920}\right) \approx 29.36^\circ$.

The 16:9 ratio gives the same angle at any resolution. That is why
screens are described by a ratio, and not only by a size.

</details>

**5.** You stand 80 m from the bottom of a mast. Your eyes are 1.7 m
above the ground. From eye level, the top of the mast is 25° above the
horizontal. How tall is the mast?

<details class="dl-answer"><summary>answer</summary>

$80\tan 25^\circ \approx 37.30$ m above eye level. Add the 1.7 m, and
the mast is about 39.0 m tall.

A diagram helps you remember to add the height of your eyes.

</details>

## Area

**6.** Find the area of a triangle with sides 9 and 12 and an angle of
40° between them.

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{2} \times 9 \times 12 \times \sin 40^\circ \approx 34.7$ square
units.

</details>

**7.** Why is $\frac{1}{2}ab\sin C$ the same as half base times height?

<details class="dl-answer"><summary>answer</summary>

Because $b\sin C$ *is* the height. Draw a line from the top corner
straight down to the base, at a right angle. It makes a right-angled
triangle with hypotenuse $b$ and angle $C$. So its vertical side, the
height, is $b\sin C$.

The formula is half base times height, with the height calculated from
what you were given.

</details>

**8.** The cell finds the area of two triangles, each with sides 8
and 10. The angle between the sides is 30° in one, and 150° in the
other.

```python exec
id: area-practice-1
print(area(8, 10, 30))
print(area(8, 10, 150))
```

```predict
type: number
tolerance: 0.01

The first line prints about 20. What will the second line print?
```

<details class="dl-answer"><summary>why</summary>

It prints about 20 too. $\sin 150^\circ = \sin 30^\circ$, because
sine has the same value for an angle and for 180° minus it. So the two
triangles, one pointed and one wide open, have the same height, and the
same area.

</details>

**9.** Two sides of a triangle are 8 and 10. Which angle between them
gives the largest area? What is that area?

<details class="dl-answer"><summary>answer</summary>

90°, which gives an area of 40.

The area is $\frac{1}{2} \times 8 \times 10 \times \sin C$. Sine is
largest at 90°, where it is 1. So the biggest triangle you can make from
two given sides is the right-angled one.

</details>

## The cosine rule

**10.** Two sides of 7 and 9 meet at 55°. Find the third side.

<details class="dl-answer"><summary>answer</summary>

$\sqrt{49 + 81 - 2 \times 7 \times 9 \times \cos 55^\circ} = \sqrt{130 - 72.28} \approx 7.60$.

</details>

**11.** A triangle has sides 6, 8 and 11. Find its largest angle.

<details class="dl-answer"><summary>answer</summary>

The largest angle is opposite the longest side, 11.

$$\cos C = \frac{36 + 64 - 121}{2 \times 6 \times 8} = \frac{-21}{96} = -0.21875$$

So the angle is about 102.6°.

The cosine is negative, so you know the angle is obtuse (more than 90°)
before you compute it. That is a useful check.

</details>

**12.** What does the cosine rule become when the angle is 90°?

<details class="dl-answer"><summary>answer</summary>

Pythagoras. $\cos 90^\circ = 0$, so the correction term $2ab\cos C$
disappears, and $c^2 = a^2 + b^2$ is left.

The cosine rule is Pythagoras with a correction for an angle that is not
a right angle.

</details>

**13.** A ship sails 8 km on a bearing of 060°. Then it turns and sails
5 km on a bearing of 150°. How far is it from where it started?

<details class="dl-hint"><summary>hint</summary>

Draw it. What is the turn, and what is the angle inside the triangle?

</details>

<details class="dl-answer"><summary>one way through it</summary>

The turn is $150 - 60 = 90^\circ$, so the angle inside the triangle is
$180 - 90 = 90^\circ$. A right angle means Pythagoras is enough:
$\sqrt{8^2 + 5^2} = \sqrt{89} \approx 9.43$ km. The cosine rule gives
the same, because $\cos 90^\circ = 0$.

</details>

**14.** Two vectors go from the origin to $(4, 1)$ and to $(1, 4)$. Find
the angle between them.

<details class="dl-answer"><summary>answer</summary>

Both vectors have length $\sqrt{17}$. The distance between the two tips
is $\sqrt{9 + 9} = \sqrt{18}$.

$$\cos\theta = \frac{17 + 17 - 18}{2 \times 17} = \frac{16}{34} \approx 0.4706$$

So $\theta \approx 61.9^\circ$.

A recommendation system does this calculation to decide how similar two
people's tastes are. Their ratings are two vectors, and the angle between
them measures how much they agree.

</details>

## The sine rule

**15.** A triangle has angles of 40° and 75°. The side opposite the 40°
is 10. Find the other two sides.

<details class="dl-answer"><summary>answer</summary>

The third angle is $180 - 40 - 75 = 65^\circ$.

Opposite the 75°: $\frac{10 \times \sin 75^\circ}{\sin 40^\circ} \approx 15.03$.

Opposite the 65°: $\frac{10 \times \sin 65^\circ}{\sin 40^\circ} \approx 14.10$.

</details>

**16.** When do you use the sine rule, and when the cosine rule?

<details class="dl-answer"><summary>answer</summary>

Use the sine rule when you have a side and the angle *opposite* it, plus
one more thing.

The cosine rule needs the angle *between* two known sides, or all three
sides. If what you have does not fit that, the sine rule is the other
tool.

</details>

**17.** A side of 10 is opposite an angle of 40°, and another side is 8.

```python exec
id: sine-rule-practice-1
def side_side_angle(a, b, A):
    """Every triangle with sides a and b, and the angle A opposite a."""
    sine_of_B = round(b * math.sin(math.radians(A)) / a, 9)
    if sine_of_B > 1:
        return []
    first = math.degrees(math.asin(sine_of_B))
    return [B for B in sorted({first, 180 - first}) if 180 - A - B > 0]


found = side_side_angle(10, 8, 40)
print(found)
print(len(found), "triangles")
```

```predict
type: number

How many triangles fit?
```

<details class="dl-answer"><summary>why</summary>

Only one. The sine rule gives the angle opposite the 8 as about 30.9°
or 149.1°. With 149.1°, the three angles would be more than 180°, so
that triangle cannot exist. Here the side opposite the known angle, 10,
is longer than the other side, 8, and then there is only ever one
triangle.

</details>

**18.** The sine rule can give two triangles. Why can that not happen
with the cosine rule?

<details class="dl-answer"><summary>answer</summary>

Cosine can tell an acute angle from an obtuse one, and sine cannot.
Cosine is positive for angles under 90° and negative for angles above
90°. So one cosine value points to exactly one angle between 0° and 180°.

Sine is positive for both kinds of angle, and it has the same value for
$\theta$ and $180 - \theta$.

</details>

**19.** A robot arm has an upper arm 3 long and a forearm 2 long. Which
points can its hand reach? Which points can it reach in only one way?

<details class="dl-answer"><summary>answer</summary>

The shoulder, the elbow and the hand make a triangle with sides 3 and
2. The third side, from the shoulder to the hand, must be shorter than
$3 + 2 = 5$ and longer than $3 - 2 = 1$. So the hand can reach every
point between 1 and 5 from the shoulder: a ring.

At exactly 5 the arm is straight, and at exactly 1 it is folded back on
itself. Both are one way only. Everywhere between, the elbow can bend
up or down, which gives two ways.

</details>

## Putting it together

**20.** From the top of a lighthouse 45 m high, a boat is 8° below the
horizontal. How far is the boat from the foot of the lighthouse?

<details class="dl-answer"><summary>answer</summary>

The angle at the boat, looking up, is also 8°. The height is opposite
it, and the distance is adjacent to it:
$\frac{45}{\tan 8^\circ} \approx 320$ m.

</details>

**21.** A triangle has sides 5, 6 and 7. Find all three angles, and check
that they add up to 180°.

<details class="dl-answer"><summary>answer</summary>

Opposite the 5: about 44.42°. Opposite the 6: about 57.12°. Opposite the
7: about 78.46°.

The sum is 180.00°. It is a good habit to find all three angles and
check the sum. It catches a mistyped side straight away.

</details>

**22.** Write a function that takes three side lengths and says whether
they can form a triangle at all.

<details class="dl-answer"><summary>answer</summary>

Each side must be shorter than the other two added together. If it is
not, the two short sides cannot reach across the long one.

```python
def possible(a, b, c):
    return a + b > c and b + c > a and a + c > b
```

`possible(1, 2, 10)` is `False`. If you give those sides to the cosine
rule, `acos` stops with a `math domain error`. The error means the same
thing, but it explains it less clearly.

</details>

## Your world

**23.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

A boat leaves the harbour and sails 6 km on a bearing of 070°. A
lighthouse is 4 km from the harbour, on a bearing of 130°. How far is
the boat from the lighthouse? Can you write
`apart(first_km, first_bearing, second_km, second_bearing)`, for any two
places given from the same starting point?

```python exec
id: your-world-1--sea-and-sky
# Your code here.
```

```hint
Both places are measured from the harbour. What is the angle between
the two bearings, at the harbour?
```

```inputs
apart(6, 70, 4, 130)
apart(3, 0, 4, 90)
```

```solution
def apart(first_km, first_bearing, second_km, second_bearing):
    between = abs(second_bearing - first_bearing)
    return cosine_rule_side(first_km, second_km, between)
---
The angle at the harbour is 60°, so the distance is
$\sqrt{36 + 16 - 48\cos 60^\circ} = \sqrt{28} \approx 5.29$ km. Due
north and due east, 3 km and 4 km, are 5 km apart.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

About 2,300 years ago, Aristarchus of Samos saw that when the Moon is
exactly half lit, the angle at the Moon, between the Earth and the Sun,
is a right angle. He measured the angle at the Earth, between the Moon
and the Sun, as 87°. Then the Sun is $\frac{1}{\cos 87^\circ}$ times
as far away as the Moon. Can you write `how_many_times(angle)`? The
angle is really about 89.85°. What does that change?

```python exec
id: your-world-1--planets-and-moons
# Your code here.
```

```hint
Draw the Earth, the Moon and the Sun, with the right angle at the Moon.
The Earth-Sun line is the hypotenuse. Which side is adjacent to the
angle at the Earth?
```

```inputs
how_many_times(87)
how_many_times(89.85)
```

```solution
def how_many_times(angle):
    return 1 / math.cos(math.radians(angle))
---
With 87°, the Sun is about 19 times as far as the Moon. With 89.85°,
it is about 382 times. Near 90°, a tiny change in the angle makes a
huge change in the answer, because the cosine is close to 0. The method
was right, and the angle was too hard to measure by eye.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A triangular field in the kingdom has sides of 250 m, 310 m and 400 m.
Nobody measured its angles. What is its area? Can you write
`field_area(a, b, c)` for any three sides?

```python exec
id: your-world-1--fantasy-maps
# Your code here.
```

```hint
The area formula needs two sides and the angle between them. Which rule
finds an angle from three sides?
```

```inputs
field_area(250, 310, 400)
field_area(300, 400, 500)
```

```solution
def field_area(a, b, c):
    angle = cosine_rule_angle(a, b, c)
    return area(a, b, angle)
---
The angle opposite the 400 m side is about 90.5°, so the field is
about 38,700 m², nearly 4 hectares. The 300-400-500 field is a 3-4-5
triangle made 100 times bigger, with an area of 60,000 m².
```

</div>

## From earlier

**24.** From
[Distance and Pythagoras: how far apart two points are](tutorial:distance-and-pythagoras).
A triangle has corners at $(1, 1)$, $(7, 1)$ and $(4, 5)$. What are its
three angles?

<details class="dl-answer"><summary>one way through it</summary>

The sides are 6, 5 and 5, from the distance formula. The angle opposite
the 6 is `cosine_rule_angle(5, 5, 6)`, about 73.74°. The other two are
equal, because the triangle is isosceles: about 53.13° each. The three
add up to 180°.

</details>

**25.** From
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines).
The lines $y = x$ and $y = -x$ have slopes 1 and $-1$, which multiply to
$-1$. Arrows along them go to $(1, 1)$ and $(1, -1)$. What angle does
the cosine rule give between the arrows?

<details class="dl-answer"><summary>answer</summary>

Both arrows have length $\sqrt{2}$, and the tips are 2 apart.
`cosine_rule_angle(math.sqrt(2), math.sqrt(2), 2)` prints a number very
close to 90. The slope rule and the cosine rule agree: the lines are
perpendicular.

</details>
