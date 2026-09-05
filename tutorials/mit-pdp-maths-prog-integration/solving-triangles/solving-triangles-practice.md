---
title: "Solving Triangles — Practice"
slug: solving-triangles-practice
practice_for: solving-triangles
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: trigonometry-and-calculus
version: 2026.08.23.1
---

# Solving Triangles — Practice

Answers are folded. Draw the triangle before you compute anything — most of the mistakes in this topic are about which side is opposite which angle.

## Tools

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

## Right-Angled Triangles

**1.** A right triangle has short sides 5 and 12. Find the hypotenuse and both other angles.

<details class="dl-answer"><summary>answer</summary>

Hypotenuse 13, by Pythagoras.

The angle opposite the 5 is arctan(5/12) ≈ 22.62°, and the other is 90 − 22.62 = 67.38°.

5-12-13 is one of the standard whole-number triangles, along with 3-4-5 and 8-15-17. Worth recognising.

</details>

**2.** A ladder 6 m long leans against a wall at 70° to the ground. How far up does it reach, and how far out is its foot?

<details class="dl-answer"><summary>answer</summary>

Up: 6 sin 70° ≈ 5.64 m. Out: 6 cos 70° ≈ 2.05 m.

</details>

**3.** A robot arm segment 40 cm long is raised at 35° from horizontal. Where is its tip, relative to the joint?

<details class="dl-answer"><summary>answer</summary>

Out: 40 cos 35° ≈ 32.77 cm. Up: 40 sin 35° ≈ 22.94 cm.

Which is `unit_point(35)` scaled by 40 — the ratios do not care how long the arm is.

</details>

**4.** A screen is 1920 pixels wide and 1080 tall. What angle does its diagonal make with the horizontal?

<details class="dl-answer"><summary>answer</summary>

arctan(1080/1920) ≈ 29.36°.

The 16:9 ratio gives the same angle at any resolution, which is the point of specifying a ratio rather than a size.

</details>

**5.** You are 50 m from the base of a mast and the top is at 32° above horizontal, measured from eye level 1.6 m up. How tall is the mast?

<details class="dl-answer"><summary>answer</summary>

50 tan 32° ≈ 31.25 m above eye level, plus the 1.6 m: about 32.85 m.

Forgetting to add the eye height is the classic error here, and it is exactly the sort of thing a diagram catches.

</details>

## Area

**6.** Find the area of a triangle with sides 9 and 12 and an angle of 40° between them.

<details class="dl-answer"><summary>answer</summary>

½ × 9 × 12 × sin 40° ≈ 34.7 square units.

</details>

**7.** Why is `½ab sin C` the same as half base times height?

<details class="dl-answer"><summary>answer</summary>

Because `b sin C` *is* the height. Drop a perpendicular from the far corner to the base: it makes a right triangle with hypotenuse `b` and angle `C`, so its vertical side is `b sin C`.

The formula is half base times height, with the height worked out from what you were given.

</details>

**8.** A triangular plot has sides of 30 m and 45 m with 62° between them. What is its area in hectares?

<details class="dl-answer"><summary>answer</summary>

½ × 30 × 45 × sin 62° ≈ 595.9 m², which is about 0.0596 hectares.

</details>

**9.** Two sides of a triangle are 8 and 10. What angle between them gives the largest area, and what is it?

<details class="dl-answer"><summary>answer</summary>

90°, giving 40.

The area is `½ × 8 × 10 × sin C`, and sine is largest at 90°, where it is 1. So the biggest triangle you can make from two given sides is the right-angled one.

</details>

## The Cosine Rule

**10.** Two sides of 7 and 9 meet at 55°. Find the third side.

<details class="dl-answer"><summary>answer</summary>

√(49 + 81 − 2×7×9×cos 55°) = √(130 − 72.28) ≈ 7.60.

</details>

**11.** A triangle has sides 6, 8 and 11. Find its largest angle.

<details class="dl-answer"><summary>answer</summary>

The largest angle is opposite the longest side. cos = (36 + 64 − 121)/(2×6×8) = −21/96 = −0.21875, so the angle is about 102.6°.

The negative cosine tells you it is obtuse before you compute the angle at all — which is a useful check.

</details>

**12.** What does the Cosine Rule become when the angle is 90°?

<details class="dl-answer"><summary>answer</summary>

Pythagoras. cos 90° = 0, so the correction term `2ab cos C` vanishes and `c² = a² + b²` is what is left.

The Cosine Rule is Pythagoras with a correction for the angle not being right.

</details>

**13.** A drone flies 200 m on a bearing of 040°, then 150 m on a bearing of 110°. How far is it from where it started?

<details class="dl-answer"><summary>answer</summary>

The turn is 110 − 40 = 70°, so the interior angle of the triangle is 180 − 70 = 110°.

Then `√(200² + 150² − 2×200×150×cos 110°)` ≈ 287.4 m.

Getting from the bearings to the interior angle is the whole difficulty, and a sketch settles it in seconds.

</details>

**14.** Two vectors go from the origin to `(4, 1)` and `(1, 4)`. Find the angle between them.

<details class="dl-answer"><summary>answer</summary>

Both have length √17. The distance between the two tips is √(9 + 9) = √18.

cos θ = (17 + 17 − 18)/(2 × 17) = 16/34 ≈ 0.4706, so θ ≈ 61.9°.

This is the calculation a recommendation system does to decide how similar two people's tastes are: their ratings are two vectors, and the angle between them measures the agreement.

</details>

## The Sine Rule

**15.** A triangle has angles 40° and 75°, and the side opposite the 40° is 10. Find the other two sides.

<details class="dl-answer"><summary>answer</summary>

The third angle is 65°.

Opposite the 75°: 10 × sin 75° / sin 40° ≈ 15.03.
Opposite the 65°: 10 × sin 65° / sin 40° ≈ 14.10.

</details>

**16.** When do you use the Sine Rule rather than the Cosine Rule?

<details class="dl-answer"><summary>answer</summary>

When you have a side and the angle *opposite* it, plus one more thing.

The Cosine Rule needs the angle *between* two known sides, or all three sides. If what you have does not fit that, the Sine Rule is the other tool.

</details>

**17.** A triangle has a side of 8, a side of 6, and an angle of 40° opposite the 6. How many triangles fit that description?

<details class="dl-answer"><summary>answer</summary>

Two.

sin(other angle) = 8 sin 40° / 6 ≈ 0.857, so the other angle is either 59° or 121° — both have the same sine, and both give a valid triangle.

</details>

**18.** Why can this ambiguity not happen with the Cosine Rule?

<details class="dl-answer"><summary>answer</summary>

Because cosine tells acute from obtuse and sine does not. Cosine is positive for angles under 90° and negative above, so a cosine value picks out exactly one angle between 0 and 180.

Sine is positive for both, and equal for θ and 180 − θ.

</details>

**19.** A triangle has a side of 12, a side of 9, and an angle of 35° opposite the 9. Is it ambiguous?

<details class="dl-answer"><summary>answer</summary>

Yes. sin(other) = 12 sin 35° / 9 ≈ 0.765, giving 49.9° or 130.1°. Both leave a positive third angle (95.1° or 14.9°), so both are real triangles.

The case is ambiguous when the known side opposite the known angle is shorter than the other known side, and long enough to reach — which is worth checking with a sketch rather than a rule.

</details>

## Putting It Together

**20.** A surveyor at point A measures the angle to the top of a mast as 32°. She walks 50 m directly towards it and measures again: 47°. How tall is the mast?

<details class="dl-answer"><summary>answer</summary>

In the triangle made by the two viewing points and the top: the angle at A is 32°, the angle at the second point (measured inside the triangle) is 180 − 47 = 133°, so the angle at the top is 15°.

Sine Rule: the distance from the second point to the top is 50 × sin 32° / sin 15° ≈ 102.4 m.

Then the height is 102.4 × sin 47° ≈ 74.9 m.

</details>

**21.** A triangle has sides 5, 6 and 7. Find all three angles and check they add to 180°.

<details class="dl-answer"><summary>answer</summary>

Opposite the 5: about 44.42°. Opposite the 6: about 57.12°. Opposite the 7: about 78.46°.

Sum: 180.00°. Doing all three and checking the sum is a good habit — it catches a mis-typed side immediately.

</details>

**22.** Write a function that takes three side lengths and says whether they can form a triangle at all.

<details class="dl-answer"><summary>answer</summary>

Each side must be shorter than the sum of the other two — otherwise the two short ones cannot reach across the long one.

```python
def possible(a, b, c):
    return a + b > c and b + c > a and a + c > b
```

`possible(1, 2, 10)` is False, and if you feed those to the Cosine Rule you get a `math domain error` from `acos` — which is the arithmetic saying the same thing less helpfully.

</details>
