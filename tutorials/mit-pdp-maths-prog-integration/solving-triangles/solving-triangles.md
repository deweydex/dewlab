---
title: "Solving Triangles"
slug: solving-triangles
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: trigonometry-and-calculus
version: 2026.08.23.1
covers:
  when-there-is-a-right-angle:
    covers: [MIT-4.9]
  area-and-the-height-nobody-drew:
    covers: [MIT-4.8]
  the-cosine-rule:
    covers: [MIT-4.10]
  the-sine-rule-and-its-two-answers:
    covers: [MIT-4.10]
  putting-it-together:
    covers: [MIT-4.9, MIT-4.10]
---

# Solving Triangles

**Maths for IT**

Given some of a triangle, find the rest. That is the whole tutorial.

"Solving a triangle" is a strange phrase the first time you hear it, because until now solving has meant finding an unknown in an equation. Here it means filling in the missing measurements: you are told three things about a triangle and asked for the other three.

There are three cases and they come in the order a person would actually try them.

1. **Is there a right angle?** Then you need nothing new.
2. **No right angle, but you know two sides and the angle between them, or all three sides?** The Cosine Rule.
3. **No right angle, but you know a side and the angle opposite it?** The Sine Rule.

The area formula falls out of the second one on the way past.

## When There Is a Right Angle

The easy case, and it uses only what you already have: Pythagoras from *Lines and Distances*, and the ratios from *The Unit Circle*.

The unit circle had radius 1. A right-angled triangle is the same picture scaled up — which is why the ratios do not care how big the triangle is.

```python exec
id: when-there-is-a-right-angle-1
import math
import matplotlib.pyplot as plt

def right_triangle(adjacent, opposite):
    """Draw the right triangle with these two short sides, and label everything."""
    hypotenuse = math.sqrt(adjacent ** 2 + opposite ** 2)
    angle = math.degrees(math.atan2(opposite, adjacent))

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.plot([0, adjacent, adjacent, 0], [0, 0, opposite, 0], linewidth=2)
    ax.plot([adjacent - 0.3, adjacent - 0.3, adjacent],
            [0, 0.3, 0.3], color="grey", linewidth=1)
    ax.annotate(f"{adjacent}", (adjacent / 2, -0.35), ha="center")
    ax.annotate(f"{opposite}", (adjacent + 0.15, opposite / 2))
    ax.annotate(f"{hypotenuse:.3f}", (adjacent / 2 - 0.6, opposite / 2 + 0.2))
    ax.annotate(f"{angle:.1f} deg", (0.6, 0.18), fontsize=9)
    ax.set_aspect("equal")
    ax.axis("off")
    return hypotenuse, angle


h, a = right_triangle(4, 3)
print("hypotenuse:", h)
print("angle at the origin:", a, "degrees")
```

The three ratios have names, and they are the same three from the circle.

```python exec
id: when-there-is-a-right-angle-2
adjacent, opposite = 4, 3
hypotenuse = math.sqrt(adjacent ** 2 + opposite ** 2)
angle = math.atan2(opposite, adjacent)

print("opposite / hypotenuse =", opposite / hypotenuse,
      "   and sin of the angle =", math.sin(angle))
print("adjacent / hypotenuse =", adjacent / hypotenuse,
      "   and cos of the angle =", math.cos(angle))
print("opposite / adjacent   =", opposite / adjacent,
      "   and tan of the angle =", math.tan(angle))
```

They match, and the reason is the circle. Scale the unit circle up by the length of the hypotenuse and the coordinates scale with it, so the *ratios* stay exactly what they were.

The mnemonic is SOH-CAH-TOA — Sine is Opposite over Hypotenuse, Cosine is Adjacent over Hypotenuse, Tangent is Opposite over Adjacent. It is a memory aid rather than an idea, and the idea is that a triangle is a piece of a circle.

### Going backwards

If you know the ratio and want the angle, you need the inverse — the reflection idea from *Drawing Functions*.

```python exec
id: when-there-is-a-right-angle-3
print("The angle whose sine is 0.5:", math.degrees(math.asin(0.5)))
print("The angle whose tangent is 1:", math.degrees(math.atan(1)))
```

### Your turn

A robot arm segment is 40 cm long and is raised at 35 degrees from horizontal. How far out from its base does the tip reach, and how high is it?

```python exec
id: your-turn-1
# Your code here.
```

## Area, and the Height Nobody Drew

The area of a triangle is half the base times the height. That is easy when somebody has drawn the height in for you, and most of the time nobody has.

```python exec
id: area-and-the-height-nobody-drew-1
# A triangle where the height is obvious: base along the bottom, apex above it.
base, height = 6, 4
print("Half base times height:", 0.5 * base * height)
```

Now a triangle described the way triangles usually are: **two sides and the angle between them**.

```python exec
id: area-and-the-height-nobody-drew-2
def draw_from_two_sides(a, b, angle_degrees):
    """Two sides meeting at a known angle, with the height drawn in."""
    angle = math.radians(angle_degrees)
    tip = (b * math.cos(angle), b * math.sin(angle))

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot([0, a, tip[0], 0], [0, 0, tip[1], 0], linewidth=2)
    ax.plot([tip[0], tip[0]], [0, tip[1]], "--", color="tab:orange", linewidth=2)
    ax.annotate(f"a = {a}", (a / 2, -0.4), ha="center")
    ax.annotate(f"b = {b}", (tip[0] / 2 - 0.5, tip[1] / 2))
    ax.annotate(f"height = b sin C = {tip[1]:.3f}",
                (tip[0] + 0.2, tip[1] / 2), color="tab:orange")
    ax.annotate(f"C = {angle_degrees} deg", (0.7, 0.25), fontsize=9)
    ax.set_aspect("equal")
    ax.axis("off")
    return tip[1]


height = draw_from_two_sides(7, 5, 50)
print("The height is:", height)
print("b sin C is:   ", 5 * math.sin(math.radians(50)))
```

There it is. **The height is `b sin C`** — the second side, times the sine of the angle between them. Which is just SOH-CAH-TOA applied to the little right triangle the dashed line makes.

So the area is:

```python exec
id: area-and-the-height-nobody-drew-3
def area(a, b, angle_degrees):
    return 0.5 * a * b * math.sin(math.radians(angle_degrees))


print(area(7, 5, 50))
print("and by base times height:", 0.5 * 7 * (5 * math.sin(math.radians(50))))

# The right-angled case, where the old formula obviously works too.
print()
print("a right angle:", area(6, 4, 90), "and half base times height:", 0.5 * 6 * 4)
```

**`½ab sin C` is not a new fact.** It is half base times height, with the height worked out for you from the information you were actually given.

### Your turn

A triangular plot of land has two sides of 30 m and 45 m with an angle of 62 degrees between them. What is its area?

```python exec
id: your-turn-2
# Your code here.
```

## The Cosine Rule

Now the case with no right angle at all.

Start from Pythagoras and watch it stop working.

```python exec
id: the-cosine-rule-1
def third_side(a, b, angle_degrees):
    """The side opposite the angle, measured by building the triangle."""
    angle = math.radians(angle_degrees)
    tip = (b * math.cos(angle), b * math.sin(angle))
    return math.sqrt((tip[0] - a) ** 2 + tip[1] ** 2)


a, b = 5, 4
print(" angle    actual c^2    a^2 + b^2    difference")
for angle in [30, 60, 90, 120, 150]:
    c = third_side(a, b, angle)
    print(f"  {angle:>4}     {c ** 2:>9.3f}     {a**2 + b**2:>8}"
          f"     {a**2 + b**2 - c**2:>10.3f}")
```

At 90 degrees the difference is zero — that is Pythagoras, and it only holds there.

Everywhere else there is a gap, and the gap is what the Cosine Rule is.

```python exec
id: the-cosine-rule-2
fig, ax = plt.subplots(figsize=(8, 4))
angles = list(range(1, 180))
gaps = [a ** 2 + b ** 2 - third_side(a, b, ang) ** 2 for ang in angles]
ax.plot(angles, gaps, linewidth=2, label="a^2 + b^2 - c^2")
ax.plot(angles, [2 * a * b * math.cos(math.radians(ang)) for ang in angles],
        "--", linewidth=2, label="2ab cos C")
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(90, color="tab:red", linestyle=":", label="90 degrees")
ax.grid(alpha=0.3)
ax.legend()
ax.set_xlabel("angle between the two sides, in degrees")
ax.set_title("The gap, and what it turns out to be")
```

The two curves are the same curve. So:

`c² = a² + b² − 2ab·cos C`

**The Cosine Rule is Pythagoras with a correction term**, and the correction is `2ab cos C`. At 90 degrees the cosine is zero, the correction vanishes, and you are left with Pythagoras exactly.

```python exec
id: the-cosine-rule-3
def cosine_rule_side(a, b, angle_degrees):
    """Given two sides and the angle between them, find the third side."""
    angle = math.radians(angle_degrees)
    return math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(angle))


def cosine_rule_angle(a, b, c):
    """Given all three sides, find the angle opposite side c."""
    cos_c = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
    return math.degrees(math.acos(cos_c))


print("rule says:   ", cosine_rule_side(5, 4, 60))
print("measured:    ", third_side(5, 4, 60))
print()
print("and backwards:", cosine_rule_angle(5, 4, cosine_rule_side(5, 4, 60)))
```

The rule works in both directions: two sides and the angle between gives the third side, and three sides gives any angle.

### The drone

A drone flies 200 m on a bearing of 040 degrees, turns, and flies 150 m on a bearing of 110 degrees. How far is it from home?

Bearings are measured clockwise from north, which is not how the unit circle measures angles — so the first job is to work out the angle *inside* the triangle. Turning from 040 to 110 is a turn of 70 degrees, and the interior angle of the triangle is what is left of a straight line: 180 − 70 = 110 degrees.

```python exec
id: the-cosine-rule-4
first_leg, second_leg = 200, 150
turn = 110 - 40
interior = 180 - turn

print("The drone turned by", turn, "degrees.")
print("The angle inside the triangle is", interior, "degrees.")
print("Distance from home:", round(cosine_rule_side(first_leg, second_leg, interior), 1), "m")
```

### Your turn

Two vectors from the origin: one to `(4, 1)` and one to `(1, 4)`. What is the angle between them? The Cosine Rule will get you there.

You have all three sides already — two from `distance` and one between the two tips.

```python exec
id: your-turn-3
def distance(p, q):
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)


# Your code here.
```

That question — the angle between two lists of numbers — is one a recommendation system asks constantly. Two people's ratings are two vectors, and how similar their taste is comes out as the angle between them.

## The Sine Rule, and Its Two Answers

The Cosine Rule needs the angle *between* two known sides. When what you have instead is a side and the angle *opposite* it, there is a different relationship.

```python exec
id: the-sine-rule-and-its-two-answers-1
def build(a, b, angle_c_degrees):
    """Build a triangle from two sides and the angle between, and return
    all three sides and all three angles."""
    c = cosine_rule_side(a, b, angle_c_degrees)
    angle_a = cosine_rule_angle(b, c, a)
    angle_b = cosine_rule_angle(a, c, b)
    return (a, b, c), (angle_a, angle_b, angle_c_degrees)


sides, angles = build(5, 7, 55)
print("sides: ", [round(s, 3) for s in sides])
print("angles:", [round(x, 3) for x in angles], " sum:", round(sum(angles), 6))
print()
for side, angle in zip(sides, angles):
    print(f"side {side:>7.3f}  /  sin(angle) = {side / math.sin(math.radians(angle)):.6f}")
```

The same number, all three times.

That is the Sine Rule: **each side divided by the sine of the angle opposite it gives the same value**, for every side of the triangle.

```python exec
id: the-sine-rule-and-its-two-answers-2
def sine_rule_side(known_side, known_angle_degrees, wanted_angle_degrees):
    ratio = known_side / math.sin(math.radians(known_angle_degrees))
    return ratio * math.sin(math.radians(wanted_angle_degrees))


# A triangle with angles 40 and 75 (so the third is 65) and one side of 10
# opposite the 40.
print(sine_rule_side(10, 40, 75))
print(sine_rule_side(10, 40, 65))
```

### Two answers, both right

Here is the interesting part, and it is the first time in this course that a correct calculation gives you two correct answers.

Suppose you know a side of 8, another side of 6, and that the angle opposite the 6 is 40 degrees. Where is the third corner?

```python exec
id: the-sine-rule-and-its-two-answers-3
fig, ax = plt.subplots(figsize=(8, 4.5))

known_angle = 40
known_opposite = 6
other_side = 8

# The angle opposite the 8 comes from the sine rule — and asin has two answers.
ratio = known_opposite / math.sin(math.radians(known_angle))
sine_of_other = other_side / ratio
first = math.degrees(math.asin(sine_of_other))
second = 180 - first

print("The angle opposite the 8 could be", round(first, 2), "degrees")
print("                             or  ", round(second, 2), "degrees")
print()
print("Both have the same sine:", math.sin(math.radians(first)),
      math.sin(math.radians(second)))

for angle, style, name in [(first, "-", "acute"), (second, "--", "obtuse")]:
    third = 180 - known_angle - angle
    base = sine_rule_side(known_opposite, known_angle, third)
    tip = (other_side * math.cos(math.radians(known_angle)),
           other_side * math.sin(math.radians(known_angle)))
    ax.plot([0, base, tip[0], 0], [0, 0, tip[1], 0], style, linewidth=2,
            label=f"{name}: third angle {third:.1f} deg")

ax.set_aspect("equal")
ax.legend()
ax.axis("off")
ax.set_title("Two triangles, both fitting the same three facts")
```

Both triangles genuinely have a side of 8, a side of 6, and a 40-degree angle opposite the 6. Neither is wrong.

The cause is that **sine gives the same value for an angle and for 180 minus that angle** — which you can see on the wave from the last tutorial, where every height between 0 and 1 is reached twice on the way up and over.

```python exec
id: the-sine-rule-and-its-two-answers-4
for angle in [30, 150, 50, 130]:
    print(f"sin({angle:>4}) = {math.sin(math.radians(angle)):.6f}")
```

**A correct calculation with two correct answers is not a failure of the method.** Deciding which one you meant is your job, and it usually comes from something you know about the situation that the three numbers did not capture.

This does not happen with the Cosine Rule, because cosine is negative for obtuse angles and positive for acute ones — so it can tell them apart and sine cannot.

### Your turn

Given a side of 12, a side of 9, and an angle of 35 degrees opposite the 9: is this case ambiguous? Work it out before computing.

```python exec
id: your-turn-4
# Your reasoning as a comment, then the calculation.
```

## Putting It Together

One function that picks the right rule for what you were given.

```python exec
id: putting-it-together-1
def solve(a=None, b=None, c=None, A=None, B=None, C=None):
    """Fill in what is missing, from whatever three things are known.

    Sides a, b, c. Angles A, B, C in degrees, each opposite its own letter.
    """
    if a and b and C:                      # two sides and the angle between
        c = cosine_rule_side(a, b, C)
        A = cosine_rule_angle(b, c, a)
        B = 180 - A - C
    elif a and b and c:                    # all three sides
        A = cosine_rule_angle(b, c, a)
        B = cosine_rule_angle(a, c, b)
        C = 180 - A - B
    elif a and A and B:                    # a side, its angle, one more angle
        C = 180 - A - B
        b = sine_rule_side(a, A, B)
        c = sine_rule_side(a, A, C)
    else:
        return "Not enough, or not a combination this handles."
    return {"a": round(a, 3), "b": round(b, 3), "c": round(c, 3),
            "A": round(A, 2), "B": round(B, 2), "C": round(C, 2)}


print(solve(a=5, b=7, C=55))
print(solve(a=3, b=4, c=5))
print(solve(a=10, A=40, B=75))
```

The middle one should have a 90 in it, and it does — a 3-4-5 triangle is right-angled, which the Cosine Rule works out without being told.

### Your turn

A surveyor stands at point A and measures the angle to a mast as 32 degrees. She walks 50 m directly towards it and measures again: 47 degrees. How tall is the mast?

Try drawing it first — there is a triangle in there with one side of 50 and two angles you can work out.

```python exec
id: your-turn-5
# Your code here.
```

## Reflection

Given some of a triangle, find the rest — and which tool you reach for depends on which parts you were given.

**A right angle needs nothing new.** Pythagoras and the three ratios, which are the unit circle scaled up.

**`½ab sin C` is half base times height**, with `b sin C` being the height that nobody drew in.

**The Cosine Rule is Pythagoras with a correction**, and the correction is zero at 90 degrees. That is why it looks like Pythagoras with something extra bolted on: it is.

**The Sine Rule can give two answers**, because sine cannot tell an angle from 180 minus that angle. Both triangles are real. Choosing between them is not arithmetic.

In a few sentences, of the three situations at the top of this tutorial, which do you think you would meet most often, and in what?

## Where to Read More

Khan Academy. *Proof of the Law of Cosines.*
<https://www.youtube.com/watch?v=pGaDcOMdw48>. Where `c² = a² + b² − 2ab
cos C` actually comes from — the same correction-to-Pythagoras idea this
page arrives at by comparing gaps.

Khan Academy. *Proof: Law of Sines.*
<https://www.youtube.com/watch?v=APNkWrD-U1k>. Why every side divided by
the sine of its opposite angle gives the same number, derived rather than
just checked.
