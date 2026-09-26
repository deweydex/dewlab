---
title: "Solving triangles: the sine rule and the cosine rule"
year: "2026-2027"
version: 2026.09.26.1
covers:
  when-there-is-a-right-angle:
    covers: [MIT-4.9]
  heights-you-cannot-reach:
    covers: [MIT-4.9]
  area-and-the-height-nobody-drew:
    covers: [MIT-4.8]
  the-cosine-rule:
    covers: [MIT-4.10]
  the-sine-rule-and-its-two-answers:
    covers: [MIT-4.10]
  putting-it-together:
    covers: [MIT-4.9, MIT-4.10]
  triangles-in-your-world:
    covers: [MIT-4.9, MIT-4.10]
worlds:
  sea-and-sky: A lighthouse, seen through a sextant from a boat. The numbers are made up.
  planets-and-moons: Venus and Mercury, and how far each is from the Sun.
  fantasy-maps: Surveying a made-up kingdom with triangles. The numbers are made up.
---

# Solving triangles: the sine rule and the cosine rule

A lighthouse stands on flat ground. You cannot climb it, and you have no
tape long enough. You stand 50 m from its foot, and the top is 35
degrees above the horizontal. How tall is it?

We know some of a triangle's sides and angles. Can we find the rest?
This whole page is about that question. Until now, solving has meant
finding an unknown in an equation. *Solving a triangle* means finding
its missing measurements. A triangle has three sides and three angles.
You are told three of these six things, and you find the other three.

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
from [Distance and Pythagoras: how far apart two points are](tutorial:distance-and-pythagoras),
and sine, cosine and tangent from
[The unit circle: sine, cosine and tangent](tutorial:the-unit-circle).

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
the circle?

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

They match because of the circle. The hypotenuse is a radius, 5 long,
of a circle 5 times the size of the unit circle. Making the circle
bigger makes both coordinates bigger by the same amount, so the
*ratios* stay what they were on the unit circle.

What happens to the ratio if the whole triangle is ten times bigger,
with sides 40, 30 and 50?

```python exec
id: when-there-is-a-right-angle-3
print(3 / 5)      # opposite / hypotenuse, sides 4, 3 and 5
print(30 / 50)    # opposite / hypotenuse, sides 40, 30 and 50
```

```predict
type: choice

What will the second line print, beside the first line's 0.6?

- 6.0
  - Every side is ten times longer, so the ratio could be too.
- 0.6
- 0.06
  - Ten times bigger could mean ten times smaller for a ratio.
```

Both lines print 0.6. The angle is the same, so the ratios are the
same, however big the triangle is.

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
Opposite over Adjacent. It helps you remember the table. The idea behind
it is that a right-angled triangle is a piece of a circle.

### Going backwards

Suppose you know the ratio and want the angle. Then you need the
inverse, which we met in
[Functions and their graphs](tutorial:drawing-functions). The *inverse
sine*, written $\sin^{-1}$ or arcsin, takes a sine and returns an
angle. In Python it is `math.asin`. The inverse cosine and inverse
tangent are `math.acos` and `math.atan`. All three give their answer in
radians, so we use `math.degrees` to turn it into degrees.

What angle do you expect to have a sine of 0.5?

```python exec
id: when-there-is-a-right-angle-4
print("The angle whose sine is 0.5:", math.degrees(math.asin(0.5)))
print("The angle whose tangent is 1:", math.degrees(math.atan(1)))
```

The first answer prints as `30.000000000000004`. That tiny extra is a
rounding effect of decimals in Python. Read it as 30.

## Heights you cannot reach

Now we can answer the lighthouse. You, the foot of the lighthouse and
its top make a right-angled triangle. The 50 m along the ground is the
side adjacent to your 35 degrees. The height is the opposite side. Which
ratio uses the opposite and the adjacent sides? Tangent.

The angle up from the horizontal to something above you is its *angle
of elevation*. Your eyes are about 1.6 m above the ground, so the
triangle starts at eye level, and we add the 1.6 m at the end.

```python exec
id: heights-you-cannot-reach-1
distance_away = 50      # metres, along the ground
elevation = 35          # degrees, up from the horizontal
eyes = 1.6              # metres

height = distance_away * math.tan(math.radians(elevation)) + eyes
print("The lighthouse is about", round(height, 1), "m tall.")
```

It works the other way down, too. From the top of a cliff 60 m high, a
boat is 12 degrees below the horizontal. This is the *angle of
depression*. The boat, the foot of the cliff and the top of the cliff
make a right-angled triangle, and the 12 degrees is at the top. How far
out is the boat?

```python exec
id: heights-you-cannot-reach-2
cliff = 60          # metres
depression = 12     # degrees, down from the horizontal

print("The boat is about", round(cliff / math.tan(math.radians(depression))), "m out.")
```

The angle at the boat, looking up at the cliff top, is also 12 degrees,
because the horizontal at the top and the sea are parallel. So the cliff
is the side opposite the boat's angle, and the distance out is the
adjacent side.

### Your turn

A house is 8 m wide. Its roof has two sloping sides, each at 35 degrees
to the flat, meeting at the top in the middle. How long is each sloping
side, from the wall to the top? How high is the top above the walls?
Can you write `roof(width, pitch)`, which returns both, for any width
and angle in degrees?

```python exec
id: heights-you-cannot-reach-3
def roof(width, pitch):
    """The length of one sloping side, and the height of the top above the walls."""
    # Your code here.
```

```hint
Draw it. Each half of the roof is a right-angled triangle. Which side of
that triangle do you know, and which ratio joins it to each side you
want?
```

```inputs
roof(8, 35)
roof(8, 45)
roof(10, 20)
```

```solution
def roof(width, pitch):
    """The length of one sloping side, and the height of the top above the walls."""
    half = width / 2
    angle = math.radians(pitch)
    return half / math.cos(angle), half * math.tan(angle)
---
Each half is a right-angled triangle with an adjacent side of half the
width, 4 m. Each sloping side is about 4.88 m long, and the top is about
2.80 m above the walls. At 45 degrees the height is the same as the half
width, 4 m, because $\tan 45^\circ = 1$.
```

## Area, and the height nobody drew

The area of a triangle is half the base times the height. That is easy
when somebody has drawn the height in for you. Most of the time, nobody
has.

Here is a triangle described the way triangles usually are: by **two
sides and the angle between them**. The dashed orange line is the height.
How could we find its length?

```python exec
id: area-and-the-height-nobody-drew-1
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

The height is $b\sin C$: the second side times the sine of the angle
between the two sides. This is SOH-CAH-TOA again, used on the small
right-angled triangle that the dashed line makes. In that small
triangle, $b$ is the hypotenuse and the height is the side opposite $C$.

So the area is half the base times the height:

$$\text{area} = \tfrac{1}{2}ab\sin C$$

For the triangle above, that is
$\frac{1}{2} \times 7 \times 5 \times \sin 50^\circ \approx 13.41$.

```python exec
id: area-and-the-height-nobody-drew-2
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

### Your turn

A plot of land is a triangle. Two of its sides are 30 m and 45 m, with
an angle of 62 degrees between them. What is its area? Which angle
between those two sides would give the biggest area?

```python exec
id: your-turn-2
# Your code here.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

`area(30, 45, 62)` is about 596 square metres. The biggest area comes
at 90 degrees, 675 square metres, because $\sin 90^\circ = 1$ is the
biggest a sine can be.

</details>

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

A vector here is an arrow from the origin to a point. Three people each
give two films a score out of 5, and each person's two scores make a
vector: Aoife gives $(5, 1)$, Ben gives $(4, 2)$, and Chidi gives
$(1, 5)$. The smaller the angle between two vectors, the more alike
the two people's tastes. Which two people are most alike?

Can you write `angle_between(u, v)` with the cosine rule? You already
have all three sides of the triangle. Two sides are the lengths of the
vectors, which `distance` gives you. The third side is the distance
between the two tips.

```python exec
id: your-turn-3
def distance(p, q):
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)


aoife, ben, chidi = (5, 1), (4, 2), (1, 5)


def angle_between(u, v):
    """The angle, in degrees, between the arrows from the origin to u and v."""
    # Your code here.
```

```hint
The triangle has corners at the origin, at `u` and at `v`. Which side is
opposite the angle you want?
```

```inputs
angle_between(aoife, ben)
angle_between(aoife, chidi)
angle_between(ben, chidi)
```

```solution
def angle_between(u, v):
    """The angle, in degrees, between the arrows from the origin to u and v."""
    origin = (0, 0)
    return cosine_rule_angle(distance(origin, u), distance(origin, v), distance(u, v))
---
The angle is opposite the side between the two tips. Aoife and Ben are
about 15 degrees apart, Aoife and Chidi about 67, and Ben and Chidi
about 52. Aoife and Ben are most alike.
```

Recommendation systems often ask this question with long lists of
numbers: two people's ratings of hundreds of films are two vectors, and
the angle between them shows how similar their tastes are.

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
for i in range(3):
    ratio = sides[i] / math.sin(math.radians(angles[i]))
    print(f"side {sides[i]:>7.3f}  /  sin(angle) = {ratio:.6f}")
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

You have seen two correct answers before, with quadratic equations. Now
it happens with a triangle: one correct calculation gives two correct
triangles.

Suppose you know a side of 8, another side of 6, and that the angle
opposite the 6 is 40 degrees. Put the corner with the 40 degrees at the
origin, and the side of 8 going up from it at 40 degrees. The side of 6
hangs from the top of the 8, and it must reach the flat line along the
bottom. Watch it swing. Where can it reach the line?

```python exec
id: the-sine-rule-and-its-two-answers-3
from matplotlib.animation import FuncAnimation

top = (8 * math.cos(math.radians(40)), 8 * math.sin(math.radians(40)))
swings = [math.radians(-170 + 160 * k / 23) for k in range(24)]

figure, stage = plt.subplots(figsize=(5, 2.8))
stage.plot([-1, 12], [0, 0], color="black", linewidth=1)
stage.plot([0, top[0]], [0, top[1]], linewidth=2, color="tab:blue")
rim = [math.radians(-180 + k) for k in range(181)]
stage.plot([top[0] + 6 * math.cos(t) for t in rim],
           [top[1] + 6 * math.sin(t) for t in rim], ":", color="grey")
reach = math.sqrt(6 ** 2 - top[1] ** 2)
for x in [top[0] - reach, top[0] + reach]:
    stage.plot([x], [0], "o", color="tab:red")
stage.set_aspect("equal")
stage.axis("off")
side, = stage.plot([], [], linewidth=2, color="tab:orange")


def draw_step(k):
    t = swings[k]
    side.set_data([top[0], top[0] + 6 * math.cos(t)],
                  [top[1], top[1] + 6 * math.sin(t)])


FuncAnimation(figure, draw_step, frames=24, interval=150)
```

The orange side is 6 long. As it swings, its end draws the grey dotted
curve, and that curve crosses the flat line twice, at the two red dots.
Each red dot is a place for the third corner. So two triangles fit the
same three facts.

What if the swinging side were a different length? Move the slider.
How short can it be and still reach the line? For which lengths does
only one triangle fit?

```python exec
id: the-sine-rule-and-its-two-answers-6
length = slider("length of the swinging side", 4.0, 9.0, step=0.1, value=6.0)
side_length = length.value

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot([-4, 16], [0, 0], color="black", linewidth=1)
ax.plot([0, top[0]], [0, top[1]], linewidth=2, color="tab:blue")
rim = [math.radians(k) for k in range(361)]
ax.plot([top[0] + side_length * math.cos(t) for t in rim],
        [top[1] + side_length * math.sin(t) for t in rim], ":", color="grey")

corners = []
if side_length >= top[1]:
    reach = math.sqrt(side_length ** 2 - top[1] ** 2)
    corners = sorted({x for x in [top[0] - reach, top[0] + reach] if x > 0})
for x in corners:
    ax.plot([0, x, top[0]], [0, 0, top[1]], color="tab:orange")
    ax.plot([x], [0], "o", color="tab:red")
ax.set_xlim(-4, 16)
ax.set_ylim(-4, 15)
ax.set_aspect("equal")
ax.axis("off")
print(len(corners), "triangles")
```

The sine rule finds both. It gives the angle opposite the 8, from its
sine. `math.asin` returns one angle, and 180 minus that angle has the
same sine, so that is a second answer.

```python exec
id: the-sine-rule-and-its-two-answers-4
fig, ax = plt.subplots(figsize=(8, 4.5))

known_angle = 40
known_opposite = 6
other_side = 8

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
    ax.plot([0, base, top[0], 0], [0, 0, top[1], 0], style, linewidth=2,
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
id: the-sine-rule-and-its-two-answers-5
for angle in [30, 150, 50, 130]:
    print(f"sin({angle:>4}) = {math.sin(math.radians(angle)):.6f}")
```

This is called the *ambiguous case*. One correct calculation gives two
correct answers. It is part of the method, not a mistake. You decide
which triangle you meant. The answer usually comes from something you
know about the real situation, which the three numbers did not include.

The cosine rule does not have this problem. Cosine is negative for obtuse
angles (between 90° and 180°) and positive for acute ones (less than
90°). So cosine can tell them apart, and sine cannot.

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
        return []    # side a is too short to reach
    first = math.degrees(math.asin(sine_of_B))
    triangles = []
    for B in sorted({first, 180 - first}):   # a set, so 90 is not counted twice
        C = 180 - A - B
        if C > 0:
            triangles.append(tidy(a, b, sine_rule_side(a, A, C), A, B, C))
    return triangles


print(side_side_angle(6, 8, 40))
```

Here is a new case. A side of 9 is opposite an angle of 35 degrees, and
another side is 12. How many triangles fit?

```python exec
id: putting-it-together-2
found = side_side_angle(9, 12, 35)
print(found)
print(len(found), "triangles")
```

```predict
type: number

How many triangles will `side_side_angle` find?
```

Now we write one function that picks the right rule for what you were
given.

```python exec
id: putting-it-together-3
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
two from the ambiguous case. The function returns both, and does not
choose. The three numbers cannot choose either. You have to choose.

### Your turn

A surveyor stands at a point and measures the angle up to the top of a
mast: 32 degrees. She walks 50 m straight towards the mast and measures
again: 47 degrees. How tall is the mast? Can you write
`mast_height(first, second, walked)` for any two angles and any walk?

```python exec
id: putting-it-together-4
def mast_height(first, second, walked):
    """The height of a mast, from two angles of elevation and the walk between."""
    # Your code here.
```

```hint
Draw it first. There is a triangle with one side of 50 m: the two
places the surveyor stood, and the top of the mast. What are its angles?
```

```hint
after: 3 errors
title: The steps

1. The angle at the first place is 32 degrees.
2. The angle at the second place, inside that triangle, is
   $180 - 47 = 133$ degrees.
3. So the angle at the top of the mast is $180 - 32 - 133 = 15$
   degrees, which is $47 - 32$.
4. The sine rule gives the side from the second place to the top.
5. That side is the hypotenuse of a right-angled triangle, and the
   height is opposite the 47 degrees.
```

```inputs
mast_height(32, 47, 50)
mast_height(30, 60, 100)
```

```solution
def mast_height(first, second, walked):
    """The height of a mast, from two angles of elevation and the walk between."""
    at_top = second - first
    nearer = sine_rule_side(walked, at_top, first)
    return nearer * math.sin(math.radians(second))
---
The angle at the top of the mast is $47 - 32 = 15$ degrees. The side
opposite it is the 50 m walk, so the sine rule gives the side from the
second place to the top: about 102.4 m. The height is that times
$\sin 47^\circ$, about 74.9 m. With 30 and 60 degrees and a walk of
100 m, the mast is about 86.6 m tall.
```

## Triangles in your world

<div class="dl-world" data-world="sea-and-sky">

A sextant measures the angle between two things, very exactly. Sailors
used it to find how far they were from a lighthouse whose height they
knew. A lighthouse's light is 40 m above the sea. From a boat, the
light is 2.5 degrees above the sea. How far is the boat from the
lighthouse? Can you write `distance_off(height, angle)`?

```python exec
id: triangles-in-your-world-1--sea-and-sky
light_height = 40    # metres above the sea
```

```hint
The sea, the lighthouse and your line of sight make a right-angled
triangle. Which side do you know, and which do you want?
```

```inputs
distance_off(40, 2.5)
distance_off(40, 1)
distance_off(40, 45)
```

```solution
def distance_off(height, angle):
    return height / math.tan(math.radians(angle))
---
The boat is about 916 m from the lighthouse. A smaller angle means a
bigger distance: at 1 degree it is about 2.3 km. At 45 degrees the
distance is the height, 40 m.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

Venus is closer to the Sun than the Earth is, so from the Earth it never
seems far from the Sun in the sky. The biggest angle between them, seen
from the Earth, is about 46.3 degrees. At that moment, our line of sight
just touches Venus's orbit, so the angle at Venus, between the Sun and
the Earth, is a right angle. The Earth is 1 AU from the Sun. How far
from the Sun is Venus? Can you write `orbit_radius(biggest_angle)`, in
AU? Mercury's biggest angle is about 22.8 degrees.

```python exec
id: triangles-in-your-world-1--planets-and-moons
earth_to_sun = 1    # AU
```

```hint
Draw the Sun, the Earth and Venus, with the right angle at Venus. Which
side is the hypotenuse? Which side is opposite the angle at the Earth?
```

```inputs
orbit_radius(46.3)
orbit_radius(22.8)
```

```solution
def orbit_radius(biggest_angle):
    return earth_to_sun * math.sin(math.radians(biggest_angle))
---
Venus is about 0.72 AU from the Sun, and Mercury about 0.39 AU. The
Earth-Sun line is the hypotenuse, and the Sun-Venus line is opposite
the angle at the Earth. Copernicus used this triangle in the 1500s,
long before anybody could measure these distances directly.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The kingdom's surveyors map it with triangles. Two towers stand 5 km
apart, on a *baseline* they measured carefully. From the first tower, a
far mountain top is 62 degrees from the baseline. From the second, it
is 71 degrees. How far is the mountain from each tower? Can you write
`survey(baseline, first_angle, second_angle)`?

```python exec
id: triangles-in-your-world-1--fantasy-maps
baseline = 5    # km between the towers
```

```hint
What is the third angle, at the mountain? Which side is opposite it?
```

```inputs
survey(5, 62, 71)
survey(5, 60, 60)
```

```solution
def survey(baseline, first_angle, second_angle):
    at_mountain = 180 - first_angle - second_angle
    from_first = sine_rule_side(baseline, at_mountain, second_angle)
    from_second = sine_rule_side(baseline, at_mountain, first_angle)
    return from_first, from_second
---
The angle at the mountain is 47 degrees, and the baseline is opposite
it. The sine rule gives about 6.46 km from the first tower and about
6.04 km from the second. With 60 and 60 degrees, the triangle is
equilateral, and both are 5 km. Real maps were made this way, one
triangle next to another, from a single measured baseline.
```

</div>

## Going further: a robot arm

A robot arm has two parts: an upper arm 3 long and a forearm 2 long,
joined at an elbow. Its shoulder is at the origin. How does it reach the
point $(4, 1)$?

The shoulder, the elbow and the point make a triangle, and we know all
three sides: 3, 2, and the distance to the point. So the cosine rule
gives the angle at the shoulder. The elbow can bend either way, so
there are two ways to reach the point: elbow up and elbow down.

```python exec
id: going-further-a-robot-arm-1
upper, forearm = 3, 2
target = (4, 1)
reach = math.sqrt(target[0] ** 2 + target[1] ** 2)

pointing = math.degrees(math.atan2(target[1], target[0]))
at_shoulder = cosine_rule_angle(upper, reach, forearm)

fig, ax = plt.subplots(figsize=(5, 4))
for shoulder, name in [(pointing + at_shoulder, "elbow up"),
                       (pointing - at_shoulder, "elbow down")]:
    elbow = (upper * math.cos(math.radians(shoulder)),
             upper * math.sin(math.radians(shoulder)))
    ax.plot([0, elbow[0], target[0]], [0, elbow[1], target[1]], "o-", label=name)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.legend()
print("upper arm at", round(pointing + at_shoulder, 1), "or",
      round(pointing - at_shoulder, 1), "degrees")
```

Try other targets. Which points can the arm not reach at all, and what
does `cosine_rule_angle` do there? Where are the only points it can reach
in just one way?

## Looking back

We know some of a triangle, and we find the rest. A right angle needs
only the three ratios. Two sides and the angle between them, or three
sides, need the cosine rule. A side and the angle opposite it need the
sine rule, and it can give two answers.

Look back at the three cases at the top of this page. Which one do you
think you would meet most often, and where?

A challenge: `solve` handles four combinations. Can you add a fifth: two
angles and the side between them? A surveyor's baseline and two angles
is this case.

```python challenge
import math


def sine_rule_side(known_side, known_angle_degrees, wanted_angle_degrees):
    ratio = known_side / math.sin(math.radians(known_angle_degrees))
    return ratio * math.sin(math.radians(wanted_angle_degrees))


def two_angles_and_side_between(A, B, c):
    """The triangle with angles A and B, and the side c between them."""
    # Your code here.


print(two_angles_and_side_between(62, 71, 5))
```

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
