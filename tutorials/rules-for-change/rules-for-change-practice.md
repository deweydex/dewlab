---
title: "Rules for change: the sum, product, quotient and chain rules — Practice"
practice_for: rules-for-change
year: "2026-2027"
version: 2026.09.25.1
---

# Rules for change: the sum, product, quotient and chain rules — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `derivative_at` from
[How fast, right now?](tutorial:how-fast-right-now), `compose` from
[Machines that take a number](tutorial:machines-that-take-a-number)
and `close_enough` from [Does it work?](tutorial:does-it-work). Run the
first cell before any other: it gives you `slopes_agree` and the list
of `points` from the tutorial.

## Warm-up

```python exec
id: rules-for-practice-warm-up
def slopes_agree(rule, slope_rule, points):
    """Return True when slope_rule(x) and derivative_at(rule, x) agree at every x in points.

    derivative_at is an estimate, so agree means within 0.000001, as in its own tests.
    Prints the first x where they disagree.
    """
    for x in points:
        if not close_enough(derivative_at(rule, x), slope_rule(x), tolerance=1e-6):
            print("they disagree at", x)
            return False
    return True

points = []
for step in range(-30, 31):
    points.append(step / 10)
print("slopes_agree is ready.")
```

**1. Predict.** By the power rule, what is the slope of $x^5$ at
$x = 2$? Then check with `derivative_at`.

<details class="dl-answer"><summary>answer</summary>

The power rule gives $5x^4$, and at 2 that is $5 \times 16 = 80$.

```python
def fifth_power(x):
    return x ** 5

print(derivative_at(fifth_power, 2))
```

It prints a number a tiny way from 80, such as `80.00000000230045`:
the chord's estimate, off in the ninth decimal place.

</details>

**2. Make.** Write the slope rule of $4x^3 - 2x + 7$ by hand, using the
power rule and the sum rule. Check it with `slopes_agree`.

<details class="dl-answer"><summary>answer</summary>

$4x^3$ has slope $12x^2$, $-2x$ has slope $-2$, and 7 has slope 0. So
the slope rule is $12x^2 - 2$.

```python
def polynomial(x):
    return 4 * x ** 3 - 2 * x + 7

def polynomial_slope(x):
    return 12 * x ** 2 - 2

print(slopes_agree(polynomial, polynomial_slope, points))
```

It prints `True`.

</details>

**3. Predict.** A drone rises so that its height after $t$ seconds is
$3t + 0.5t^2$ metres. How fast is it climbing after 4 seconds, in
metres per second?

<details class="dl-answer"><summary>answer</summary>

By the sum rule, the slope is $3 + t$. After 4 seconds it climbs at 7
metres a second.

```python
def drone_height(seconds):
    return 3 * seconds + 0.5 * seconds ** 2

print(round(derivative_at(drone_height, 4), 6))
```

It prints `7.0`.

</details>

**4. Explain.** On
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
phone plan B cost €20 a month, however many gigabytes you used. Why is
the slope of plan B 0? What does that slope mean for a customer?

<details class="dl-answer"><summary>answer</summary>

Plan B's graph is a flat line: the cost does not change as the
gigabytes change. A slope says how much the output changes for each
step of the input, and here it changes by nothing. For a customer, each
extra gigabyte costs €0 more. Plan A's slope is 2: each extra gigabyte
costs €2 more.

</details>

## Core

A cell for the core problems.

```python exec
id: rules-for-practice-core
# Your working for problems 5 to 12
```

**5. Make.** A picture on a phone screen grows as you spread two
fingers. After $t$ tenths of a second, it is $4 + 0.2t$ cm wide and
$3 + 0.1t$ cm high. Use the product rule to find how fast its area is
growing after 10 tenths of a second. Check with `derivative_at`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The area is width times height.
2. The width's slope is 0.2, and the height's slope is 0.1.
3. The product rule: width times the height's slope, plus height times
   the width's slope.

**Think about:** what are the units of the answer?

</details>

<details class="dl-answer"><summary>answer</summary>

After 10 tenths, the width is 6 cm and the height is 4 cm. The product
rule gives $6 \times 0.1 + 4 \times 0.2 = 0.6 + 0.8 = 1.4$ square cm
for each tenth of a second.

```python
def picture_width(tenths):
    return 4 + 0.2 * tenths

def picture_height(tenths):
    return 3 + 0.1 * tenths

def picture_area(tenths):
    return picture_width(tenths) * picture_height(tenths)

def picture_area_slope(tenths):
    return picture_width(tenths) * 0.1 + picture_height(tenths) * 0.2

print(round(picture_area_slope(10), 6), round(derivative_at(picture_area, 10), 6))
print(slopes_agree(picture_area, picture_area_slope, list(range(0, 31))))
```

Both give 1.4, and the check agrees at every time from 0 to 30.

</details>

**6. Fix.** Here is someone's slope rule for $\frac{x}{x^2 + 1}$, made
with the quotient rule. The check says no. Find the one mistake, and
fix it.

```python exec
id: rules-for-practice-fix
def ratio(x):
    return x / (x ** 2 + 1)

def ratio_slope(x):
    top = x
    bottom = x ** 2 + 1
    top_slope = 1
    bottom_slope = 2 * x
    return (top * bottom_slope - bottom * top_slope) / bottom ** 2

print(slopes_agree(ratio, ratio_slope, points))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Say the quotient rule in words: the bottom times the slope of the
   top, minus ...
2. Now read the `return` line in words. Which part comes first?
3. At which $x$ did the check disagree? Compare the two slopes there.

**Think about:** why does swapping the two parts change only the sign?

</details>

<details class="dl-answer"><summary>answer</summary>

The two parts of the top line are the wrong way round. The quotient
rule is the bottom times the slope of the top, minus the top times the
slope of the bottom:

```python
def ratio_slope(x):
    top = x
    bottom = x ** 2 + 1
    top_slope = 1
    bottom_slope = 2 * x
    return (bottom * top_slope - top * bottom_slope) / bottom ** 2

print(slopes_agree(ratio, ratio_slope, points))
```

It prints `True`. The mistake gave the right size of slope with the
wrong sign, so a graph of it would go downhill wherever the curve goes
uphill. The order matters because of the minus sign, and
$a - b = -(b - a)$.

</details>

**7. Predict.** Schlomi, who is learning Python too, says the slope of
$(3x + 2)^2$ is $2(3x + 2)$, so at $x = 1$ it is 10. She used the power
rule, which is a sensible start. What do you think `derivative_at` will
say?

```python
def bracket_squared(x):
    return (3 * x + 2) ** 2

print(round(derivative_at(bracket_squared, 1), 6))
```

<details class="dl-answer"><summary>answer</summary>

It prints `30.0`. Schlomi used the power rule on the outside, and
forgot the chain rule's last step: times the slope of the inside, which
is 3. So the slope is $2(3x + 2) \times 3 = 6(3x + 2)$, and at 1 that
is 30.

</details>

**8. Another way.** Find the slope of $(3x + 2)^2$ a second way:
multiply out the bracket first, as on
[Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop),
then use the power rule and the sum rule. Do the two ways agree?

<details class="dl-answer"><summary>answer</summary>

$(3x + 2)^2 = 9x^2 + 12x + 4$, and its slope is $18x + 12$. The chain
rule gave $6(3x + 2) = 18x + 12$. They are the same rule.

```python
def expanded_slope(x):
    return 18 * x + 12

def chain_slope(x):
    return 6 * (3 * x + 2)

print(slopes_agree(bracket_squared, expanded_slope, points))
print(slopes_agree(bracket_squared, chain_slope, points))
```

Both print `True`. Multiplying out works for a square. For
$(3x + 2)^{20}$ it would be a long job, and the chain rule is one line.

</details>

**9. Make.** A weather balloon is being filled. Its radius, in metres,
is $1 + 0.1t$ after $t$ seconds. Use `compose` and your toolkit's
`sphere_volume` to write its volume as a rule of time. How fast is the
volume growing after 10 seconds? Work it out with the chain rule, then
check.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The volume is $\frac{4}{3}\pi r^3$, and by the power rule its slope,
   per metre of radius, is $4\pi r^2$.
2. The radius grows by 0.1 m each second.
3. The chain rule multiplies them, with $r$ worked out at the time you
   want.

**Think about:** the rate you found has units. What are they?

</details>

<details class="dl-answer"><summary>answer</summary>

After 10 seconds the radius is 2 m. The chain rule gives
$4\pi \times 2^2 \times 0.1 = 1.6\pi$, about 5.03 cubic metres a
second.

```python
import math

def balloon_radius(seconds):
    return 1 + 0.1 * seconds

balloon_volume = compose(sphere_volume, balloon_radius)

def balloon_volume_slope(seconds):
    return 4 * math.pi * balloon_radius(seconds) ** 2 * 0.1

print(balloon_volume_slope(10), derivative_at(balloon_volume, 10))
print(slopes_agree(balloon_volume, balloon_volume_slope, list(range(0, 31))))
```

Both give about 5.0265, and the check agrees at every second from 0 to
30.

</details>

**10. Explain.** Schlomo, who is learning Python too, says: "The slope
of $x \times x$ should be the slope of $x$ times the slope of $x$, which
is $1 \times 1 = 1$." But $x \times x$ is $x^2$, whose slope is $2x$.
Where does Schlomo's move go wrong? Is there a space where multiplying
slopes is right?

<details class="dl-answer"><summary>answer</summary>

$x \times x$ is a product, and the product rule gives
$x \times 1 + x \times 1 = 2x$, which matches the power rule.
Multiplying the slopes ignores the two strips of the growing rectangle:
when both sides grow, each side's growth is multiplied by the *other*
side's length.

Multiplying slopes is right for a rule inside a rule. There, the
chain rule multiplies the outside slope by the inside slope, because
the inside rule's output is the outside rule's input.

That is one good way to say it. Yours may use other words, or a
picture, and be as good.

</details>

**11. Make.** On
[The top of the curve](tutorial:the-top-of-the-curve#checking-with-a-fine-comb),
a ball thrown straight up was at a height of about $1.8 + 15t - 4.9t^2$
metres after $t$ seconds. Find when it is highest by setting the slope
to 0. Check your answer with `vertex`.

<details class="dl-answer"><summary>answer</summary>

The slope is $15 - 9.8t$. It is 0 when $9.8t = 15$, so $t$ is about
1.53 seconds.

```python
print(solve_linear(-9.8, 15))
print(vertex(-4.9, 15, 1.8))
```

Both say about 1.53 seconds, and `vertex` says the ball is about
13.28 m up then. At the top the ball stops rising for an instant: its
speed, the slope of its height, is 0.

</details>

**12. Explain.** The tutorial found the power rule from a table of
slopes, and then checked each rule against `derivative_at` at 61
points. Many courses prove each rule from limits first, and then
practise using it. Which way would you have taught it, and why?

<details class="dl-answer"><summary>answer</summary>

There is no one right answer. A good answer weighs things like these:

- A table lets a reader find the pattern for themselves, before being
  told it. A found rule is often easier to remember.
- A check at 61 points catches almost every mistake, but it is not a
  proof. A rule could agree at those points and fail somewhere else.
- A proof from limits shows *why* each rule holds, and a reader who
  follows it can rebuild a rule they have forgotten.
- Proofs from limits need a lot of algebra, and a reader who
  struggles with it may lose sight of what the rule is for.

Who is the page for, and what do they need first: a rule they trust
and can use, or a rule they can prove?

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: rules-for-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** A box with no lid is made from a square of card 30 cm
across, by cutting a square of side $x$ cm from each corner. Its volume
is $x(30 - 2x)^2$, and its slope, by the product and chain rules, is
$(30 - 2x)(30 - 6x)$. Multiply out the slope, find where it is 0 with
`solve_quadratic`, and decide which answer gives the biggest box.
Check with a fine comb over $x$ from 0 to 15.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $(30 - 2x)(30 - 6x) = 900 - 180x - 60x + 12x^2$.
2. So `solve_quadratic(12, -240, 900)` gives the $x$ values where the
   slope is 0.
3. Work out the volume at each. Which makes sense for a box?

**Think about:** what does the box look like at $x = 15$?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def box_volume(cut):
    return cut * (30 - 2 * cut) ** 2

def box_slope(cut):
    return (30 - 2 * cut) * (30 - 6 * cut)

cuts = []
volumes = []
for step in range(0, 1501):
    cuts.append(step / 100)
    volumes.append(box_volume(step / 100))

print(slopes_agree(box_volume, box_slope, cuts))
flat_points = solve_quadratic(12, -240, 900)
print(flat_points)
for cut in flat_points:
    print(cut, box_volume(cut))
print(cuts[volumes.index(largest(volumes))], largest(volumes))
```

The slope is 0 at $x = 5$ and $x = 15$. At 15 the base has no width
and the volume is 0: that is a bottom of the curve, not a top. At 5 the
volume is 2,000 cubic cm, and the fine comb agrees. The biggest box has
5 cm cut from each corner.

</details>

**14. Another way.** Use `derivative_at` to make a table of the slope
of `math.sin` at a few angles in radians, beside `math.cos` at the same
angles. What do you notice? Then use the chain rule to find the slope
of your toolkit's `wave(2, 3, t)`, as a rule of time $t$, and check it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try the angles 0, 0.5, 1, 2 and 3.
2. `wave(2, 3, t)` is $2\sin(2\pi \times 3 \times t)$. The inside rule
   is $6\pi t$, with slope $6\pi$.
3. The outside rule is $2\sin(u)$. Your table says what its slope is.

**Think about:** where is the wave when its slope is largest?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import math

for angle in [0, 0.5, 1, 2, 3]:
    print(angle, round(derivative_at(math.sin, angle), 6), round(math.cos(angle), 6))

def note(time):
    return wave(2, 3, time)

def note_slope(time):
    return 2 * math.cos(6 * math.pi * time) * 6 * math.pi

times = []
for step in range(0, 101):
    times.append(step / 100)
print(slopes_agree(note, note_slope, times))
```

The two columns agree: the slope of $\sin x$ is $\cos x$. By the chain
rule, the slope of $2\sin(6\pi t)$ is $2\cos(6\pi t) \times 6\pi$, and
the check agrees. The slope is largest when the wave crosses 0, and 0
at the top and bottom of each wave.

</details>

**15. Make.** A second video service rents a bigger server for €900 a
month, and each film costs €0.25 in data. With the quotient rule, find
the slope of the average cost per film after $n$ films. After how many
films is the average falling by less than a tenth of a cent, €0.001,
per extra film?

<details class="dl-answer"><summary>answer</summary>

The top is $900 + 0.25n$, with slope 0.25, and the bottom is $n$, with
slope 1. The quotient rule gives
$\frac{0.25n - (900 + 0.25n)}{n^2} = -\frac{900}{n^2}$.

It falls by less than 0.001 when $\frac{900}{n^2} < 0.001$, that is
when $n^2 > 900{,}000$, so $n > 948.7$. From the 949th film on.

```python
def film_average(films):
    return (900 + 0.25 * films) / films

def film_average_slope(films):
    return -900 / films ** 2

print(slopes_agree(film_average, film_average_slope, list(range(100, 3001, 50))))
print(film_average_slope(948), film_average_slope(949))
```

The check agrees, and the slope is about $-0.001001$ at 948 films and
$-0.000999$ at 949.

</details>
