---
title: "Solving triangles: the sine rule and the cosine rule"
year: "2026-2027"
version: 2026.09.25.1
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

# Solving triangles: the sine rule and the cosine rule

We know some of a triangle's sides and angles. Can we find the rest?
This whole page is about that question.

"Solving a triangle" may sound strange the first time you hear it. Until
now, solving has meant finding an unknown in an equation. *Solving a
triangle* means finding its missing measurements. A triangle has three
sides and three angles. You are told three of these six things, and you
find the other three.

There are three cases. They come in the order you would try them:

1. **Is there a right angle?** Then you need nothing new.
2. **There is no right angle, but you know two sides and the angle
   between them, or all three sides?** Use the cosine rule.
3. **There is no right angle, but you know a side and the angle opposite
   it?** Use the sine rule.

On the way, we also find a formula for a triangle's area. It uses the
same information as case 2: two sides and the angle between them.

## When there is a right angle

This is the easiest case. It uses only what you already have: Pythagoras
from [Straight lines: slope, midpoint and distance](tutorial:lines-and-distances),
and sine, cosine and tangent from
[The unit circle: sine, cosine and tangent](tutorial:the-unit-circle).

The unit circle had radius 1. A right-angled triangle is the same picture
made bigger: the hypotenuse is a radius of a bigger circle. That is why
the ratios do not depend on how big the triangle is.

The cell below draws a right-angled triangle from its two short sides.
It uses `math.atan2(opposite, adjacent)` to find the angle from those two
sides. We look at going from sides back to angles below, in "Going
backwards".

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

We name the sides from the point of view of the angle we are looking at.
The *opposite* side is the side across the triangle from that angle. The
*adjacent* side is the short side next to the angle. The hypotenuse is
the longest side, as before.

Three ratios of these sides have names. Are they the same three as on
the circle? Run the cell to compare.

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

They match because of the circle. Make the unit circle bigger, by
the length of the hypotenuse. The coordinates grow by the same amount, so
the *ratios* stay exactly what they were.

| Ratio | Name | In a formula |
|---|---|---|
| opposite ÷ hypotenuse | sine | $\sin\theta = \frac{\text{opposite}}{\text{hypotenuse}}$ |
| adjacent ÷ hypotenuse | cosine | $\cos\theta = \frac{\text{adjacent}}{\text{hypotenuse}}$ |
| opposite ÷ adjacent | tangent | $\tan\theta = \frac{\text{opposite}}{\text{adjacent}}$ |

For example, in the 3-4-5 triangle above, the angle at the origin has
opposite 3, adjacent 4 and hypotenuse 5, so its sine is
$\frac{3}{5} = 0.6$.

Many people remember the table with the memory aid SOH-CAH-TOA: Sine is
Opposite over Hypotenuse, Cosine is Adjacent over Hypotenuse, Tangent is
Opposite over Adjacent. It helps you remember. The idea behind it is
that a right-angled triangle is a piece of a circle.

### Going backwards

Suppose you know the ratio and want the angle. Then you need the
inverse, which we met in
[Functions and their graphs](tutorial:drawing-functions). The *inverse
sine*, written $\sin^{-1}$ or arcsin, takes a sine and returns an
angle. In Python it is `math.asin`. The inverse cosine and inverse
tangent are `math.acos` and `math.atan`. All three give their answer in
radians, so we use `math.degrees` to turn it into degrees.

What angle do you expect to have a sine of 0.5? Run the cell to check.

```python exec
id: when-there-is-a-right-angle-3
print("The angle whose sine is 0.5:", math.degrees(math.asin(0.5)))
print("The angle whose tangent is 1:", math.degrees(math.atan(1)))
```

The first answer prints as `30.000000000000004`. That tiny extra is a
rounding effect of decimals in Python. Read it as 30.

### Your turn

A robot arm segment is 40 cm long. It is raised at 35 degrees from the
horizontal.

1. How far out from its base does the tip reach?
2. How high is the tip?

```python exec
id: your-turn-1
# Your code here.
```

## Area, and the height nobody drew

The area of a triangle is half the base times the height. That is easy
when somebody has drawn the height in for you. Most of the time, nobody
has.

```python exec
id: area-and-the-height-nobody-drew-1
# A triangle where the height is obvious: base along the bottom, apex above it.
base, height = 6, 4
print("Half base times height:", 0.5 * base * height)
```

Now here is a triangle described the way triangles usually are: by **two
sides and the angle between them**. The dashed orange line is the height.
How could we find its length?

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

There it is. The height is $b\sin C$: the second side times the sine of
the angle between the two sides. This is SOH-CAH-TOA again, used on the
small right-angled triangle that the dashed line makes. In that small
triangle, $b$ is the hypotenuse and the height is the side opposite $C$.

So the area is half the base times the height:

$$\text{area} = \tfrac{1}{2}ab\sin C$$

For the triangle above, that is
$\frac{1}{2} \times 7 \times 5 \times \sin 50^\circ \approx 13.41$.

```python exec
id: area-and-the-height-nobody-drew-3
def area(a, b, angle_degrees):
    return 0.5 * a * b * math.sin(math.radians(angle_degrees))


print(area(7, 5, 50))
print("and by base times height:", 0.5 * 7 * (5 * math.sin(math.radians(50))))

# The right-angled case, where the old formula works too.
print()
print("a right angle:", area(6, 4, 90), "and half base times height:", 0.5 * 6 * 4)
```

The formula $\frac{1}{2}ab\sin C$ is half the base times the height.
The height is calculated for you from the information you were given.
It is not a new fact.

### Your turn

A plot of land is a triangle. Two of its sides are 30 m and 45 m, with
an angle of 62 degrees between them. What is its area?

```python exec
id: your-turn-2
# Your code here.
```

## The cosine rule

Now we look at the case with no right angle at all.

We start from Pythagoras, $c^2 = a^2 + b^2$, and watch it stop working.
The next cell builds triangles with sides 5 and 4 and different angles
between them. It measures the third side, $c$, and compares $c^2$ with
$a^2 + b^2$. At which angle do you think the difference will be zero?

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

At 90 degrees the difference is zero. That is Pythagoras, and it only
holds for a right angle.

At every other angle there is a gap. What is the gap? The next cell draws
it, next to a guess: $2ab\cos C$.

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

The two curves are the same curve. So the gap is $2ab\cos C$, and:

$$c^2 = a^2 + b^2 - 2ab\cos C$$

This is the *cosine rule*. It is Pythagoras with a correction, and the
correction is $2ab\cos C$. At 90 degrees the cosine is zero, so
the correction disappears, and Pythagoras is left exactly.

For example, with $a = 5$, $b = 4$ and $C = 60^\circ$:
$c^2 = 25 + 16 - 2 \times 5 \times 4 \times 0.5 = 21$, so
$c = \sqrt{21} \approx 4.583$.

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

The rule works in both directions:

- two sides and the angle between them give the third side
- three sides give any angle

### The drone

A drone flies 200 m on a bearing of 040 degrees. Then it turns and flies
150 m on a bearing of 110 degrees. How far is it from home?

A *bearing* is an angle measured clockwise from north. The unit circle
measures angles in a different way, so the first job is to find the angle
*inside* the triangle:

1. Turning from 040 to 110 is a turn of 70 degrees.
2. The drone's path would be a straight line, 180 degrees, if it did not
   turn.
3. So the angle inside the triangle is what is left of the straight
   line: $180 - 70 = 110$ degrees.

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

A vector here is an arrow from the origin to a point. Take two vectors:
one to $(4, 1)$ and one to $(1, 4)$. What is the angle between them? The
cosine rule can find it.

You already have all three sides of the triangle. Two sides are the
lengths of the vectors, which `distance` gives you. The third side is the
distance between the two tips.

```python exec
id: your-turn-3
def distance(p, q):
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)


# Your code here.
```

Recommendation systems often ask for the angle between two lists of
numbers. Two people's ratings are two vectors. The angle between them
shows how similar their taste is.

## The sine rule, and its two answers

The cosine rule needs the angle *between* two known sides. Sometimes you
know a side and the angle *opposite* it instead. Then a different
relationship helps.

The next cell builds a triangle and then divides each side by the sine of
the angle opposite it. What do you notice?

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

We get the same number, all three times.

This is the *sine rule*. In any triangle, each side divided by the sine
of the angle opposite it gives the same value.

$$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}$$

Here a small letter is a side, and the capital letter is the angle
opposite it. For example, if a side of 10 is opposite an angle of 40°,
the ratio is $\frac{10}{\sin 40^\circ} \approx 15.557$. A side opposite
75° is then $15.557 \times \sin 75^\circ \approx 15.03$.

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

Here is something new. You have seen two correct answers before, with
quadratic equations. Now it happens with a triangle: one correct
calculation gives two correct triangles.

Suppose you know a side of 8, another side of 6, and that the angle
opposite the 6 is 40 degrees. Where is the third corner?

```python exec
id: the-sine-rule-and-its-two-answers-3
fig, ax = plt.subplots(figsize=(8, 4.5))

known_angle = 40
known_opposite = 6
other_side = 8

# The angle opposite the 8 comes from the sine rule. asin gives one angle,
# and 180 minus that angle has the same sine, so it is a second answer.
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

Both triangles have a side of 8, a side of 6, and a 40-degree angle
opposite the 6. Both of them are real triangles.

Why does this happen? Sine gives the same value for an angle and for 180
minus that angle. You can see this on the wave from
[Sine and cosine waves: amplitude, period and shift](tutorial:sine-and-cosine-waves):
on the way up and over the top, the wave reaches every height between 0
and 1 twice.

```python exec
id: the-sine-rule-and-its-two-answers-4
for angle in [30, 150, 50, 130]:
    print(f"sin({angle:>4}) = {math.sin(math.radians(angle)):.6f}")
```

This is called the *ambiguous case*. One correct calculation gives two
correct answers. It is part of the method, not a mistake. You decide
which triangle you meant. The answer usually comes from
something you know about the real situation, which the three numbers did
not include.

The cosine rule does not have this problem. Cosine is negative for obtuse
angles (between 90° and 180°) and positive for acute ones (less than
90°). So cosine can tell them apart, and sine cannot.

### Your turn

You know a side of 12, a side of 9, and an angle of 35 degrees opposite
the 9. Is this case ambiguous?

1. Think it through first, and write your reasoning as a comment.
2. Then do the calculation, and check both possible angles.

```python exec
id: your-turn-4
# Your reasoning as a comment, then the calculation.
```

## Putting it together

First, two helpers. `tidy` rounds a finished triangle so that it is
easy to read. `side_side_angle` handles the ambiguous case. It returns
every triangle that fits, which may be none, one or two.

```python exec
id: putting-it-together-1
def tidy(a, b, c, A, B, C):
    return {"a": round(a, 3), "b": round(b, 3), "c": round(c, 3),
            "A": round(A, 2), "B": round(B, 2), "C": round(C, 2)}


def side_side_angle(a, b, A):
    """Every triangle with sides a and b, and the angle A opposite a."""
    # Rounded, because floats are not exact: sin(30) is not quite 0.5.
    sine_of_B = round(b * math.sin(math.radians(A)) / a, 9)
    if sine_of_B > 1:
        return "No triangle fits: side a is too short to reach."
    first = math.degrees(math.asin(sine_of_B))
    triangles = []
    for B in sorted({first, 180 - first}):   # a set, so 90 is not counted twice
        C = 180 - A - B
        if C > 0:
            triangles.append(tidy(a, b, sine_rule_side(a, A, C), A, B, C))
    return triangles


print(side_side_angle(6, 8, 40))
```

Now we write one function that picks the right rule for what you were
given.

```python exec
id: putting-it-together-2
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
    elif a and b and A:                    # two sides, and the angle opposite one
        return side_side_angle(a, b, A)
    else:
        return "Not enough, or not a combination this handles."
    return tidy(a, b, c, A, B, C)


print(solve(a=5, b=7, C=55))
print(solve(a=3, b=4, c=5))
print(solve(a=10, A=40, B=75))
print(solve(a=6, b=8, A=40))
```

Look at the second result. A 3-4-5 triangle is right-angled, so there
should be a 90 in it. Is there? The cosine rule found the right angle
without being told.

Now look at the last one. It is a list, with two triangles in it: the
two from the ambiguous case, with a side of 6, a side of 8, and 40
degrees opposite the 6. The function returns both, and does not choose.
The three numbers cannot choose either. You have to choose.

### Your turn

A surveyor stands at a point and measures the angle up to the top of a
mast: 32 degrees. She walks 50 m straight towards the mast and measures
again: 47 degrees. How tall is the mast?

It helps to draw it first. There is a triangle in the drawing with one
side of 50 m and two angles you can find.

```python exec
id: your-turn-5
# Your code here.
```

## Reflection

We know some of a triangle and we find the rest. Which tool we use
depends on which parts we were given.

**A right angle needs nothing new.** We use Pythagoras and the three
ratios, and the ratios are the unit circle made bigger.

**$\frac{1}{2}ab\sin C$ is half base times height.** $b\sin C$ is the
height that nobody drew in.

**The cosine rule is Pythagoras with a correction.** The correction is
zero at 90 degrees.

**The sine rule can give two answers**, because sine gives the same value
for an angle and for 180 minus that angle. Both triangles are real.
Arithmetic cannot choose between them.

Look back at the three cases at the top of this page. Which one do you
think you would meet most often, and where? Write a few sentences.

## Where to read more

Khan Academy. *Proof of the Law of Cosines.*
<https://www.youtube.com/watch?v=pGaDcOMdw48>. This video proves where
`c² = a² + b² − 2ab cos C` comes from. This page found the same
correction to Pythagoras by comparing gaps.

Khan Academy. *Proof: Law of Sines.*
<https://www.youtube.com/watch?v=APNkWrD-U1k>. This video proves that
every side divided by the sine of its opposite angle gives the same
number. This page only checked it.

Ellie Sleightholm (2026). *Where Trigonometry Really Comes From.*
<https://www.youtube.com/watch?v=bkvyu5mxVdY>. This video explains why
the ratio of two sides stays the same for every triangle with the same
angles, and how that becomes sine and cosine. It is about twelve minutes
long.
