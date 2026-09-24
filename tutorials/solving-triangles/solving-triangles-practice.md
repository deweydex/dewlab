---
title: "Solving triangles: the sine rule and the cosine rule — Practice"
practice_for: solving-triangles
year: "2026-2027"
version: 2026.08.23.1
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

**5.** You stand 50 m from the bottom of a mast. Your eyes are 1.6 m
above the ground. From eye level, the top of the mast is 32° above the
horizontal. How tall is the mast?

<details class="dl-answer"><summary>answer</summary>

$50\tan 32^\circ \approx 31.24$ m above eye level. Add the 1.6 m, and the
mast is about 32.84 m tall.

The usual mistake here is to forget to add the eye height. A diagram is
exactly the thing that catches it.

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

The formula is half base times height, with the height worked out from
what you were given.

</details>

**8.** A triangular plot of land has sides of 30 m and 45 m, with 62°
between them. What is its area in hectares? (One hectare is
10,000 m².)

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{2} \times 30 \times 45 \times \sin 62^\circ \approx 596.0$ m²,
which is about 0.0596 hectares.

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
disappears, and $c^2 = a^2 + b^2$ is what is left.

The cosine rule is Pythagoras with a correction for an angle that is not
a right angle.

</details>

**13.** A drone flies 200 m on a bearing of 040°. Then it flies 150 m on
a bearing of 110°. How far is it from where it started?

<details class="dl-answer"><summary>answer</summary>

The turn is $110 - 40 = 70^\circ$, so the angle inside the triangle is
$180 - 70 = 110^\circ$.

Then $\sqrt{200^2 + 150^2 - 2 \times 200 \times 150 \times \cos 110^\circ} \approx 288.1$ m.

Going from the bearings to the inside angle is the hard part. A sketch
makes it quick.

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

**17.** A triangle has a side of 8, a side of 6, and an angle of 40°
opposite the 6. How many triangles fit that description?

<details class="dl-answer"><summary>answer</summary>

Two.

$\sin(\text{other angle}) = \frac{8\sin 40^\circ}{6} \approx 0.857$, so
the other angle is either 59° or 121°. Both have the same sine, and both
give a real triangle.

</details>

**18.** Why can this ambiguity not happen with the cosine rule?

<details class="dl-answer"><summary>answer</summary>

Cosine can tell an acute angle from an obtuse one, and sine cannot.
Cosine is positive for angles under 90° and negative for angles above
90°. So one cosine value points to exactly one angle between 0° and 180°.

Sine is positive for both kinds of angle, and it has the same value for
$\theta$ and $180 - \theta$.

</details>

**19.** A triangle has a side of 12, a side of 9, and an angle of 35°
opposite the 9. Is it ambiguous?

<details class="dl-answer"><summary>answer</summary>

Yes. $\sin(\text{other angle}) = \frac{12\sin 35^\circ}{9} \approx 0.765$,
which gives 49.9° or 130.1°. Both leave a positive third angle, 95.1° or
14.9°, so both are real triangles.

The case is ambiguous when two things are true. First, the side opposite
the known angle (here 9) is shorter than the other known side (here 12).
Second, it is still long enough to reach the third side: here it must be
longer than $12\sin 35^\circ \approx 6.88$. A sketch shows this better
than a rule.

</details>

## Putting it together

**20.** A surveyor stands at a point A and measures the angle up to the
top of a mast: 32°. She walks 50 m straight towards the mast and measures
again: 47°. How tall is the mast?

<details class="dl-answer"><summary>answer</summary>

Look at the triangle made by the two places she stood and the top of the
mast.

1. The angle at A is 32°.
2. The angle at the second place, inside the triangle, is
   $180 - 47 = 133^\circ$.
3. So the angle at the top is $180 - 32 - 133 = 15^\circ$.

Use the sine rule. The distance from the second place to the top is
$\frac{50 \times \sin 32^\circ}{\sin 15^\circ} \approx 102.4$ m.

Then the height is $102.4 \times \sin 47^\circ \approx 74.9$ m.

</details>

**21.** A triangle has sides 5, 6 and 7. Find all three angles, and check
that they add up to 180°.

<details class="dl-answer"><summary>answer</summary>

Opposite the 5: about 44.42°. Opposite the 6: about 57.12°. Opposite the
7: about 78.46°.

The sum is 180.00°. Finding all three angles and checking the sum is a
good habit. It catches a mistyped side straight away.

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
rule, `acos` stops with a `math domain error`. That is the arithmetic
saying the same thing, less helpfully.

</details>
