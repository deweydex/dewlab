---
title: "Derivative rules: power, sum, product and chain, found by experiment — Practice"
practice_for: derivative-rules
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: A weather balloon, filling up. The numbers are made up.
  planets-and-moons: How a planet's year grows with its distance from the Sun.
  fantasy-maps: A field, growing longer and wider. The numbers are made up.
---

# Derivative rules: power, sum, product and chain, found by experiment — Practice

Each answer is hidden in a fold under its question. For each question:

1. Differentiate by hand first.
2. Then check your answer with numbers, using the tools below.

The check shows whether your derivative matches the numbers.

## Tools

The cell below defines two helpers:

- `derivative_at(f, x)` computes the slope of `f` at `x` with numbers.
- `compare_slopes(f, df)` puts your hand-worked derivative `df` beside
  the numerical one, at four points.

The last line shows how to use `compare_slopes`, with $x^2$ and its derivative
$2x$. Where the two columns match, your derivative agrees with the slope
the numbers give.

```python exec
id: tools-1
def derivative_at(f, x, gap=1e-6):
    """The slope of f at x, computed numerically."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


def compare_slopes(f, df, points=(-2, -0.5, 1, 3)):
    """Compare a hand-computed derivative against the numerical one."""
    for x in points:
        print(f"  x = {x:>5}:  yours {df(x):>12.5f}   numerical {derivative_at(f, x):>12.5f}")


def differentiate_polynomial(coefficients):
    """Coefficients from the constant term upwards: [c, b, a] means a x^2 + b x + c."""
    return [i * coefficients[i] for i in range(1, len(coefficients))]


compare_slopes(lambda x: x ** 2, lambda x: 2 * x)
```

## The power rule

**1.** What is the derivative of each of these?

- (a) $x^5$
- (b) $x$
- (c) $x^{-2}$
- (d) $\sqrt{x}$, which is $x^{1/2}$

<details class="dl-answer"><summary>answer</summary>

(a) $5x^4$.

(b) $1$.

(c) $-2x^{-3}$.

(d) $\frac{1}{2}x^{-1/2}$, which is $\dfrac{1}{2\sqrt{x}}$.

The rule works the same way when the power is negative or a fraction:
bring the power down, and reduce it by one.

</details>

**2.** What is the derivative of a constant, such as $7$?

<details class="dl-answer"><summary>answer</summary>

Zero. A constant does not change, so its rate of change is zero.

The power rule agrees. $7$ is $7x^0$. If we bring the 0 down, we get
$0 \times 7x^{-1}$, which is 0.

</details>

**3.** Differentiate $3x^4 - 2x + 7$.

<details class="dl-answer"><summary>answer</summary>

$12x^3 - 2$.

Use the sum rule and go term by term: $3x^4$ gives $12x^3$, $-2x$ gives
$-2$, and the 7 gives 0.

</details>

**4.** Differentiate $x^3 - 6x^2 + 9x - 4$.

<details class="dl-answer"><summary>answer</summary>

$3x^2 - 12x + 9$.

</details>

## Turning points

**5.** Where are the turning points of $x^3 - 3x$?

<details class="dl-answer"><summary>answer</summary>

The derivative is $3x^2 - 3$. It is zero when $x^2 = 1$, so at $x = -1$
and $x = 1$.

The heights there are 2 and −2. The first is a local maximum, and the
second is a local minimum.

</details>

**6.** Find the turning point of $x^2 + 6x + 5$ in two ways: by
completing the square, and by the derivative.

<details class="dl-answer"><summary>answer</summary>

Completing the square gives $(x + 3)^2 - 4$, so the vertex is at
$(-3, -4)$.

The derivative is $2x + 6$. It is zero at $x = -3$, and the height there
is $9 - 18 + 5 = -4$.

Two different methods give one answer. When two methods agree, you can
trust the answer.

</details>

**7.** Find the turning points of $x^4 - 8x^2$.

<details class="dl-answer"><summary>answer</summary>

The derivative is $4x^3 - 16x = 4x(x^2 - 4)$. It is zero at $x = 0$,
$x = -2$ and $x = 2$.

The height is 0 at the middle point, and −16 at both outer points. The
curve is a W shape, with two equal minimums and a local maximum between
them.

</details>

**8.** A curve has derivative zero at some point. Must that point be a
maximum or a minimum?

<details class="dl-answer"><summary>answer</summary>

No. $x^3$ has derivative $3x^2$, which is zero at $x = 0$. But the curve
keeps going upwards through that point, without turning.

It is flat for an instant, and then it continues. A point like that is
called a point of inflection. This is why "the derivative is zero" gives
you *candidates* for turning points. You still need to check each one.

</details>

## The product rule

**9.** Differentiate $(x + 1)(x^2 - 3)$ in two ways: by expanding the
brackets first, and by the product rule.

<details class="dl-answer"><summary>answer</summary>

Expanded, it is $x^3 + x^2 - 3x - 3$. Its derivative is
$3x^2 + 2x - 3$.

By the product rule:

$$1 \times (x^2 - 3) + (x + 1) \times 2x = x^2 - 3 + 2x^2 + 2x = 3x^2 + 2x - 3$$

The two answers are the same. The rule is useful for the cases that you
cannot expand.

</details>

**10.** Differentiate $x^2(x + 5)$.

<details class="dl-answer"><summary>answer</summary>

$$2x(x + 5) + x^2(1) = 2x^2 + 10x + x^2 = 3x^2 + 10x$$

To check: expanded, it is $x^3 + 5x^2$, and its derivative is
$3x^2 + 10x$.

</details>

**11.** $x \cdot x$ is $x^2$. The slope of $x$ is 1 everywhere, and
$1 \times 1 = 1$. The cell asks `derivative_at` for the slope of
$x \cdot x$ at 5.

```python exec
id: the-product-rule-1
print(derivative_at(lambda x: x * x, 5))
```

```predict
type: number
tolerance: 0.01

What will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints about 10, not 1. Multiplying the two slopes is not the rule.
The product rule gives $1 \cdot x + x \cdot 1 = 2x$, which is 10 at 5,
and the power rule gives $2x$ for $x^2$ too.

</details>

## The chain rule

**12.** Differentiate $(3x + 2)^5$.

<details class="dl-answer"><summary>answer</summary>

$$5(3x + 2)^4 \times 3 = 15(3x + 2)^4$$

First, differentiate the outside and leave the inside alone. Then
multiply by the derivative of the inside, which is 3.

</details>

**13.** Differentiate $(x^2 + 1)^3$.

<details class="dl-answer"><summary>answer</summary>

$$3(x^2 + 1)^2 \times 2x = 6x(x^2 + 1)^2$$

</details>

**14.** Differentiate $\sqrt{4x + 1}$.

<details class="dl-answer"><summary>answer</summary>

Write it as $(4x + 1)^{1/2}$. Then:

$$\frac{1}{2}(4x + 1)^{-1/2} \times 4 = \frac{2}{\sqrt{4x + 1}}$$

</details>

**15.** Can you explain the chain rule in terms of rates, with no
algebra?

<details class="dl-answer"><summary>answer</summary>

Suppose $u$ changes three times as fast as $x$, and $y$ changes twice as
fast as $u$. Then $y$ changes six times as fast as $x$.

Rates multiply along a chain. That is the whole idea, and it gives the
rule its name.

</details>

## Rates in the world

**16.** A tank holds $V(t) = 100 - 2t^2$ litres after $t$ minutes. How
fast is it emptying at $t = 3$?

<details class="dl-answer"><summary>answer</summary>

$V'(t) = -4t$. So at $t = 3$, the rate is $-4 \times 3 = -12$ litres per
minute. The tank is emptying at 12 litres a minute.

The minus sign tells you that the volume is going down.

</details>

**17.** For that tank, when is it empty? How fast is it emptying at that
moment?

<details class="dl-answer"><summary>answer</summary>

It is empty when $100 - 2t^2 = 0$. So $t^2 = 50$, and
$t \approx 7.07$ minutes.

At that moment the rate is $-4 \times 7.07 \approx -28.3$ litres per
minute. It empties faster and faster the whole time, because of the
squared term.

</details>

**18.** A company's revenue from selling $n$ items is
$R(n) = 50n - 0.1n^2$ euro. They are already selling 100 items. About
how much extra revenue does one more item bring?

<details class="dl-answer"><summary>answer</summary>

$R'(n) = 50 - 0.2n$. So at $n = 100$, it is $50 - 20 = 30$: about €30.

(The exact extra revenue from the 101st item is
$R(101) - R(100)$, which is €29.90. The derivative gives a very close estimate.)

Economists call this marginal revenue. It is the derivative under a
different name.

Notice that it falls as $n$ rises. At $n = 250$, $R'(n) = 0$. One more
item adds almost nothing. After that, each extra sale makes the
total revenue go down.

</details>

**19.** A population is $P(t) = 500 + 40t + t^2$ after $t$ years. What is
its growth rate at $t = 0$, and at $t = 10$?

<details class="dl-answer"><summary>answer</summary>

$P'(t) = 40 + 2t$. So the growth rate is 40 per year at the start, and
$40 + 20 = 60$ per year after ten years.

The growth is getting faster, because of the $t^2$ term.

</details>

**20.** Distance is measured in metres, and time in seconds. What are the
units of the derivative of distance? And what are the units of the
derivative of *that*?

<details class="dl-answer"><summary>answer</summary>

Metres per second, which is speed. Then metres per second per second,
which is acceleration.

The calculation itself gives the units. A derivative divides a
change in the output by a change in the input, so its units are output
units per input unit. Units are a useful check that you have
differentiated the thing you meant to.

</details>

## One longer one

**21.** We make an open box from a square sheet, 20 cm by 20 cm. We cut a
square of side $x$ from each corner, then fold up the sides.

1. Write the volume as a function of $x$.
2. What range of $x$ makes sense?
3. Find the $x$ that gives the largest volume.
4. What is that volume?

<details class="dl-answer"><summary>answer</summary>

1. The base is a square with side $20 - 2x$, and the height is $x$. So
   $V(x) = x(20 - 2x)^2$.

2. Between 0 and 10. At 0 there is no height. At 10 there is no base
   left.

3. Expand the brackets: $V(x) = 4x^3 - 80x^2 + 400x$. So
   $V'(x) = 12x^2 - 160x + 400$. Set that to zero, and divide by 4:
   $3x^2 - 40x + 100 = 0$. The quadratic formula gives
   $$x = \frac{40 \pm \sqrt{1600 - 1200}}{6} = \frac{40 \pm 20}{6},$$
   so $x = 10$ or $x = \dfrac{10}{3}$.
   $x = 10$ is the end of the range, where there is no box. So the
   answer is $x = \dfrac{10}{3} \approx 3.33$ cm.

4. $V\left(\dfrac{10}{3}\right) = \dfrac{10}{3}\left(20 - \dfrac{20}{3}\right)^2 = \dfrac{16000}{27} \approx 592.6$ cm³.

Two things are worth noticing here. First, the derivative gave two
candidates, and one of them did not make sense for the box. Second, this is the
usual shape of an optimisation problem, a problem that asks for the
best (largest or smallest) value:

1. Write the quantity as a function.
2. Differentiate it.
3. Set the derivative to zero and solve.
4. Think about which answer makes sense.

</details>

## More rules

**22.** The power rule says the slope of $\frac{1}{x} = x^{-1}$ is
$-x^{-2}$. The cell checks it at 2.

```python exec
id: more-rules-1
print(derivative_at(lambda x: 1 / x, 2))
```

```predict
type: number
tolerance: 0.001

What will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints about $-0.25$. $-x^{-2}$ at 2 is $-\frac{1}{4}$. The slope is
negative because $\frac{1}{x}$ gets smaller as $x$ grows.

</details>

**23.** The tutorial's `integrate_polynomial` runs the power rule
backwards. Which polynomial has the derivative $3 + 6x^2$? Find it by
hand, then check it with `differentiate_polynomial`. How many answers
are there?

<details class="dl-answer"><summary>one way through it</summary>

Each power goes up by one and is divided by its new power: $3$ comes
from $3x$, and $6x^2$ comes from $2x^3$. So $3x + 2x^3$ works, and
`differentiate_polynomial([0, 3, 0, 2])` returns `[3, 0, 6]`. Any
number added on the end works too, such as $3x + 2x^3 + 7$, because a
number on its own has a slope of 0. So there are infinitely many
answers.

</details>

## Your world

**24.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

A weather balloon is filled with gas. Its radius is $0.1t$ metres, $t$
minutes after filling starts, and its volume is
$\frac{4}{3}\pi r^3$. How fast is the volume growing after 20
minutes, when the radius is 2 m? Can you write `volume_rate(t)` from the
rules?

```python exec
id: your-world-1--sea-and-sky
import math


def volume(t):
    return 4 / 3 * math.pi * (0.1 * t) ** 3
```

```hint
The radius is inside the volume. The slope of $\frac{4}{3}\pi r^3$ is
$4\pi r^2$, by the power rule. What is the slope of $0.1t$?
```

```inputs
round(volume_rate(20), 3)
round(derivative_at(volume, 20), 3)
```

```solution
def volume_rate(t):
    radius = 0.1 * t
    return 4 * math.pi * radius ** 2 * 0.1
---
By the chain rule, the rate is $4\pi r^2 \times 0.1$. At a radius of
2 m, that is about 5.03 cubic metres a minute.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

Kepler found that a planet's year, in Earth years, is $a^{1.5}$, where
$a$ is its distance from the Sun in AU. How fast does the year grow with
distance, at 4 AU? Can you write `year_rate(a)` with the power rule?

```python exec
id: your-world-1--planets-and-moons
def year(a):
    return a ** 1.5
```

```hint
The power rule works for a power of 1.5: bring it down, and take 1 away.
```

```inputs
round(year_rate(4), 3)
round(year_rate(1), 3)
round(derivative_at(year, 4), 3)
```

```solution
def year_rate(a):
    return 1.5 * a ** 0.5
---
The slope is $1.5a^{0.5}$. At 4 AU, a planet's year grows by about 3
Earth years for each extra AU. At 1 AU, it grows by 1.5 years for each
AU. Further out, the years grow faster.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A field's length is $4t$ metres and its width is $10 + t$ metres, $t$
years after the farmer starts clearing it. How fast is its area growing
after 5 years? Can you write `area_rate(t)` from the rules?

```python exec
id: your-world-1--fantasy-maps
def area(t):
    return 4 * t * (10 + t)
```

```hint
The area is the length times the width. Which rule is for a product?
```

```inputs
round(area_rate(5), 3)
round(derivative_at(area, 5), 3)
```

```solution
def area_rate(t):
    length, width = 4 * t, 10 + t
    return 4 * width + length * 1
---
By the product rule, the rate is $4(10 + t) + 4t$. After 5 years that
is $60 + 20 = 80$ square metres a year.
```

</div>

## From earlier

**25.** From
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive).
The rocket's height was `[2, 15, -4.9]`, which means
$2 + 15t - 4.9t^2$. What does `differentiate_polynomial` give for it,
and what does that list mean? How fast is the rocket going after 1
second?

<details class="dl-answer"><summary>answer</summary>

It gives `[15, -9.8]`, which means $15 - 9.8t$: the rocket's speed.
After 1 second it is going up at $15 - 9.8 = 5.2$ m/s. The $-9.8$ is how
fast gravity takes the speed away, every second.

</details>

**26.** From [Number types, powers and logarithms](tutorial:numbers-and-their-families).
$\sqrt{x}$ is $x^{1/2}$. What does the power rule give for its slope?
What is the slope at 4?

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{2}x^{-1/2}$, which is $\frac{1}{2\sqrt{x}}$. At 4 that is
$\frac{1}{4} = 0.25$, and `derivative_at(lambda x: x ** 0.5, 4)` agrees.

</details>
