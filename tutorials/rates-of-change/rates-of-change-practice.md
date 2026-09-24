---
title: "Derivatives: the rate of change of a curve — Practice"
practice_for: rates-of-change
year: "2026-2027"
version: 2026.08.23.1
---

# Derivatives: the rate of change of a curve — Practice

Each answer is hidden in a fold under its question. For each question:

1. Differentiate by hand first.
2. Then check your answer with numbers, using the tools below.

The check tells you whether you applied the rule correctly.

## Tools

The cell below defines two helpers:

- `derivative_at(f, x)` computes the slope of `f` at `x` with numbers.
- `check(f, df)` compares your hand-worked derivative `df` with the
  numerical one, at four points.

The last line shows how to use `check`, with $x^2$ and its derivative
$2x$. If the two columns match, your derivative is right.

```python exec
id: tools-1
def derivative_at(f, x, gap=1e-6):
    """The slope of f at x, computed numerically."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


def check(f, df, points=(-2, -0.5, 1, 3)):
    """Compare a hand-computed derivative against the numerical one."""
    for x in points:
        print(f"  x = {x:>5}:  yours {df(x):>12.5f}   numerical {derivative_at(f, x):>12.5f}")


check(lambda x: x ** 2, lambda x: 2 * x)
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

The power rule agrees. $7$ is $7x^0$. Bringing the 0 down gives
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

Two different methods give one answer. That kind of agreement tells you
that both are right.

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

**9.** Differentiate $(x + 1)(x^2 - 3)$ in two ways: by multiplying out
first, and by the product rule.

<details class="dl-answer"><summary>answer</summary>

Multiplied out, it is $x^3 + x^2 - 3x - 3$. Its derivative is
$3x^2 + 2x - 3$.

By the product rule:

$$1 \times (x^2 - 3) + (x + 1) \times 2x = x^2 - 3 + 2x^2 + 2x = 3x^2 + 2x - 3$$

The two answers are the same. The rule is useful for the cases that you
cannot multiply out.

</details>

**10.** Differentiate $x^2(x + 5)$.

<details class="dl-answer"><summary>answer</summary>

$$2x(x + 5) + x^2(1) = 2x^2 + 10x + x^2 = 3x^2 + 10x$$

To check: multiplied out, it is $x^3 + 5x^2$, and its derivative is
$3x^2 + 10x$.

</details>

**11.** A student says that the derivative of $x^2 \cdot x^3$ is
$2x \cdot 3x^2 = 6x^3$. What went wrong?

<details class="dl-answer"><summary>answer</summary>

They multiplied the derivatives, and that is not the rule.

$x^2 \cdot x^3$ is $x^5$, and its derivative is $5x^4$. The product rule
gives $2x \cdot x^3 + x^2 \cdot 3x^2 = 2x^4 + 3x^4 = 5x^4$, which
agrees.

$6x^3$ does not even have the right power. That is a quick way to spot
the mistake.

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

Rates multiply along a chain. That is the whole idea, and it is where
the rule gets its name.

</details>

## Rates in the world

**16.** A tank holds $V(t) = 100 - 2t^2$ litres after $t$ minutes. How
fast is it emptying at $t = 3$?

<details class="dl-answer"><summary>answer</summary>

$V'(t) = -4t$. So at $t = 3$, the rate is $-4 \times 3 = -12$ litres per
minute. The tank is emptying at 12 litres a minute.

The minus sign carries information: it tells you the volume is going
down.

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

Notice that it falls as $n$ rises. At $n = 250$, $R'(n) = 0$: one more
item brings in almost nothing. After that, each extra sale makes the
total revenue go down.

</details>

**19.** A population is $P(t) = 500 + 40t + t^2$ after $t$ years. What is
its growth rate at $t = 0$, and at $t = 10$?

<details class="dl-answer"><summary>answer</summary>

$P'(t) = 40 + 2t$. So the growth rate is 40 per year at the start, and
$40 + 20 = 60$ per year after ten years.

The growth is speeding up, and the $t^2$ term is the cause.

</details>

**20.** Distance is measured in metres, and time in seconds. What are the
units of the derivative of distance? And what are the units of the
derivative of *that*?

<details class="dl-answer"><summary>answer</summary>

Metres per second, which is speed. Then metres per second per second,
which is acceleration.

The units come out of the calculation itself. A derivative divides a
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

3. Multiply out: $V(x) = 4x^3 - 80x^2 + 400x$. So
   $V'(x) = 12x^2 - 160x + 400$. Set that to zero, and divide by 4:
   $3x^2 - 40x + 100 = 0$. The quadratic formula gives
   $$x = \frac{40 \pm \sqrt{1600 - 1200}}{6} = \frac{40 \pm 20}{6},$$
   so $x = 10$ or $x = \dfrac{10}{3}$.
   $x = 10$ is the end of the range, where there is no box. So the
   answer is $x = \dfrac{10}{3} \approx 3.33$ cm.

4. $V\left(\dfrac{10}{3}\right) = \dfrac{10}{3}\left(20 - \dfrac{20}{3}\right)^2 = \dfrac{16000}{27} \approx 592.6$ cm³.

Two things are worth noticing here. First, the derivative gave two
candidates, and the situation ruled one of them out. Second, this is the
usual shape of an optimization problem, a problem that asks for the
best (largest or smallest) value:

1. Write the quantity as a function.
2. Differentiate it.
3. Set the derivative to zero and solve.
4. Think about which answer makes sense.

</details>
