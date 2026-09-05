---
title: "Rates of Change — Practice"
slug: rates-of-change-practice
practice_for: rates-of-change
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: trigonometry-and-calculus
version: 2026.08.23.1
---

# Rates of Change — Practice

Answers are folded. Differentiate by hand first, then check numerically — the check is what tells you whether the rule was applied correctly.

## Tools

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

## The Power Rule

**1.** Differentiate each.

- (a) `x⁵`
- (b) `x`
- (c) `x⁻²`
- (d) `√x`, which is `x^(1/2)`

<details class="dl-answer"><summary>answer</summary>

(a) `5x⁴`. (b) `1`. (c) `−2x⁻³`. (d) `½x^(−1/2)`, which is `1/(2√x)`.

The rule does not care whether the power is negative or fractional: bring it down, reduce it by one.

</details>

**2.** What is the derivative of a constant, say `7`?

<details class="dl-answer"><summary>answer</summary>

Zero. A constant does not change, so its rate of change is nothing.

By the power rule: `7` is `7x⁰`, and bringing the 0 down makes the whole thing vanish.

</details>

**3.** Differentiate `3x⁴ − 2x + 7`.

<details class="dl-answer"><summary>answer</summary>

`12x³ − 2`.

Term by term, using the sum rule, and the 7 disappears.

</details>

**4.** Differentiate `x³ − 6x² + 9x − 4`.

<details class="dl-answer"><summary>answer</summary>

`3x² − 12x + 9`.

</details>

## Turning Points

**5.** Where are the turning points of `x³ − 3x`?

<details class="dl-answer"><summary>answer</summary>

The derivative is `3x² − 3`, which is zero when `x² = 1`, so at x = −1 and x = 1.

The heights there are 2 and −2 — a local maximum and a local minimum.

</details>

**6.** Find the turning point of `x² + 6x + 5` two ways: by completing the square, and by the derivative.

<details class="dl-answer"><summary>answer</summary>

Completing the square gives `(x + 3)² − 4`, so the vertex is at `(−3, −4)`.

The derivative is `2x + 6`, which is zero at x = −3, and the height there is −4.

Two different methods, one answer — which is the sort of agreement that tells you both are right.

</details>

**7.** Find the turning points of `x⁴ − 8x² `.

<details class="dl-answer"><summary>answer</summary>

The derivative is `4x³ − 16x = 4x(x² − 4)`, zero at x = 0, −2 and 2.

Heights: 0 at the middle, and −16 at both of the outer ones. It is a W shape with two equal minima and a local maximum between them.

</details>

**8.** A curve has derivative zero at some point. Is that point necessarily a maximum or minimum?

<details class="dl-answer"><summary>answer</summary>

No. `x³` has derivative `3x²`, which is zero at x = 0 — and the curve carries straight on upwards through that point without turning.

It flattens for an instant and then continues. That is a point of inflection, and it is why "the derivative is zero" identifies *candidates* for turning points rather than turning points themselves.

</details>

## The Product Rule

**9.** Differentiate `(x + 1)(x² − 3)` two ways: by multiplying out first, and by the product rule.

<details class="dl-answer"><summary>answer</summary>

Multiplied out: `x³ + x² − 3x − 3`, whose derivative is `3x² + 2x − 3`.

By the rule: `1 × (x² − 3) + (x + 1) × 2x = x² − 3 + 2x² + 2x = 3x² + 2x − 3`.

Same. The rule is worth having for the cases you cannot multiply out.

</details>

**10.** Differentiate `x²(x + 5)`.

<details class="dl-answer"><summary>answer</summary>

`2x(x + 5) + x²(1) = 2x² + 10x + x² = 3x² + 10x`.

Check: multiplied out it is `x³ + 5x²`, whose derivative is `3x² + 10x`.

</details>

**11.** A student says the derivative of `x²·x³` is `2x · 3x² = 6x³`. What went wrong?

<details class="dl-answer"><summary>answer</summary>

They multiplied the derivatives, which is not the rule.

`x²·x³` is `x⁵`, whose derivative is `5x⁴`. The product rule gives `2x·x³ + x²·3x² = 2x⁴ + 3x⁴ = 5x⁴`, which agrees.

`6x³` is not even the right power, which is a quick way to spot the error.

</details>

## The Chain Rule

**12.** Differentiate `(3x + 2)⁵`.

<details class="dl-answer"><summary>answer</summary>

`5(3x + 2)⁴ × 3 = 15(3x + 2)⁴`.

Outside first, leaving the inside alone; then multiply by the derivative of the inside.

</details>

**13.** Differentiate `(x² + 1)³`.

<details class="dl-answer"><summary>answer</summary>

`3(x² + 1)² × 2x = 6x(x² + 1)²`.

</details>

**14.** Differentiate `√(4x + 1)`.

<details class="dl-answer"><summary>answer</summary>

`½(4x + 1)^(−1/2) × 4 = 2/√(4x + 1)`.

</details>

**15.** Explain the chain rule in terms of rates, without any algebra.

<details class="dl-answer"><summary>answer</summary>

If `u` changes three times as fast as `x`, and `y` changes twice as fast as `u`, then `y` changes six times as fast as `x`.

Rates multiply along a chain. That is the whole idea, and it is why the rule has the name it does.

</details>

## Rates in the World

**16.** A tank holds `V(t) = 100 − 2t²` litres after t minutes. How fast is it emptying at t = 3?

<details class="dl-answer"><summary>answer</summary>

`V′(t) = −4t`, so at t = 3 it is −12 litres per minute — emptying at 12 litres a minute.

The negative sign is information: the volume is decreasing.

</details>

**17.** For that tank, when is it empty, and how fast is it going at that moment?

<details class="dl-answer"><summary>answer</summary>

Empty when `100 − 2t² = 0`, so `t² = 50` and t ≈ 7.07 minutes.

At that moment the rate is `−4 × 7.07 ≈ −28.3` litres per minute. It is emptying faster and faster the whole time, which is what a squared term does.

</details>

**18.** A company's revenue from selling n items is `R(n) = 50n − 0.1n²`. What is the extra revenue from selling one more item when they are already selling 100?

<details class="dl-answer"><summary>answer</summary>

`R′(n) = 50 − 0.2n`, so at n = 100 it is €30.

Economists call this marginal revenue, and it is the derivative under a different name. Notice it falls as n rises — the 201st item brings in nothing at all, and after that more sales lose money.

</details>

**19.** A population grows as `P(t) = 500 + 40t + t²` after t years. What is its growth rate at t = 0 and at t = 10?

<details class="dl-answer"><summary>answer</summary>

`P′(t) = 40 + 2t`, so 40 per year at the start and 60 per year after ten.

The growth is accelerating, which the `t²` term is responsible for.

</details>

**20.** Distance is in metres and time in seconds. What are the units of the derivative? And of the derivative of *that*?

<details class="dl-answer"><summary>answer</summary>

Metres per second, which is speed. And then metres per second per second, which is acceleration.

The units come out of the calculation itself — a derivative is a division of the output units by the input units — and they are a useful check that you have differentiated the thing you meant to.

</details>

## One Longer One

**21.** A box is made from a 20 cm by 20 cm sheet by cutting a square of side `x` from each corner and folding up the sides.

- (a) Write the volume as a function of x.
- (b) What range of x makes sense?
- (c) Find the x that gives the largest volume.
- (d) What is that volume?

<details class="dl-answer"><summary>answer</summary>

(a) The base is `(20 − 2x)` square and the height is `x`, so `V(x) = x(20 − 2x)²`.

(b) Between 0 and 10. At 0 there is no height; at 10 there is no base left.

(c) `V(x) = 4x³ − 80x² + 400x`, so `V′(x) = 12x² − 160x + 400`. Setting that to zero: `3x² − 40x + 100 = 0`, giving `x = (40 ± √(1600 − 1200))/6 = (40 ± 20)/6`, so x = 10 or x = 10/3.

x = 10 is the useless end of the range, so the answer is **x = 10/3 ≈ 3.33 cm**.

(d) `V(10/3) = (10/3)(20 − 20/3)² ≈ 592.6 cm³`.

Two things worth noticing: the derivative gave two candidates and the situation ruled one out, and this is the standard shape of an optimisation problem — write the quantity, differentiate, set to zero, and then think about which answer is real.

</details>
