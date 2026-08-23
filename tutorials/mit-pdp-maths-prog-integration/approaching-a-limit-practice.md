---
title: "Approaching a Limit — Practice"
slug: approaching-a-limit-practice
practice_for: approaching-a-limit
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Approaching a Limit — Practice

Answers are folded. Where a question asks you to find a limit, try it with numbers *and* say what the algebra gives — the two together are what makes the answer trustworthy.

## Tools

```python exec
id: tools-1
def approach(f, target, from_below=True):
    """Print f at values marching towards `target`."""
    for step in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
        x = target - step if from_below else target + step
        try:
            print(f"   f({x:<12}) = {f(x)}")
        except ZeroDivisionError:
            print(f"   f({x:<12}) = undefined")


f = lambda x: (x ** 2 - 1) / (x - 1)
print("from below:")
approach(f, 1)
print("from above:")
approach(f, 1, from_below=False)
```

## Finding a Limit

**1.** Find the limit of `(x² − 4)/(x − 2)` as x approaches 2.

<details class="dl-answer"><summary>answer</summary>

4.

The top factorises as `(x − 2)(x + 2)`, so away from x = 2 the function is just `x + 2` — and at 2 that would be 4.

The function itself has no value at 2: the bottom is zero there and the cancelling is not allowed. The limit says what it would be, and that is a different statement.

</details>

**2.** Find the limit of `(x² − 9)/(x − 3)` as x approaches 3.

<details class="dl-answer"><summary>answer</summary>

6, by the same factorising: `(x − 3)(x + 3)` over `(x − 3)` leaves `x + 3`.

</details>

**3.** Find the limit of `(x³ − 1)/(x − 1)` as x approaches 1.

<details class="dl-answer"><summary>answer</summary>

3.

`x³ − 1` factorises as `(x − 1)(x² + x + 1)`, and at x = 1 that second bracket is 1 + 1 + 1 = 3.

</details>

**4.** Find the limit of `(√x − 2)/(x − 4)` as x approaches 4.

<details class="dl-answer"><summary>answer</summary>

1/4.

Write the bottom as `(√x − 2)(√x + 2)`. The `(√x − 2)` cancels, leaving `1/(√x + 2)`, which at x = 4 is 1/4.

Numerically it heads for 0.25 from both sides, which is worth checking.

</details>

**5.** Does `|x|/x` have a limit as x approaches 0?

<details class="dl-answer"><summary>answer</summary>

No.

From the right it is 1 (a positive number over itself); from the left it is −1. The two sides disagree, so there is no single value it is heading for.

This is the step function from the tutorial, wearing different notation.

</details>

## Limits That Do Not Exist

**6.** What happens to `1/x²` as x approaches 0? Is that a limit?

<details class="dl-answer"><summary>answer</summary>

It grows without bound from *both* sides, because squaring removes the sign.

Strictly there is no limit — no number is being approached. It is common to write "the limit is infinity", which is shorthand for "it grows without bound", not a claim that infinity is a value.

</details>

**7.** How does `1/x` differ from `1/x²` near zero?

<details class="dl-answer"><summary>answer</summary>

`1/x` goes to positive infinity from the right and negative infinity from the left. `1/x²` goes to positive infinity from both.

Neither has a limit, but the second at least does the same thing on both sides.

</details>

**8.** Find the limit of `1/x` as x grows without bound.

<details class="dl-answer"><summary>answer</summary>

0.

The values shrink towards zero and never reach it, which is the same kind of statement as before — approached, not attained.

</details>

**9.** Find the limit of `(3n + 5)/(n + 2)` as n grows without bound.

<details class="dl-answer"><summary>answer</summary>

3.

Divide top and bottom by n: `(3 + 5/n)/(1 + 2/n)`. Both of the small terms head for 0, leaving 3/1.

The rule of thumb: for large n only the highest powers matter, so the answer is the ratio of the leading coefficients.

</details>

**10.** Find the limit of `(2n² + n)/(5n² − 3)` as n grows without bound.

<details class="dl-answer"><summary>answer</summary>

2/5.

Same reasoning — the `n²` terms dominate and everything else becomes negligible.

</details>

## Why Any of This Matters

**11.** A ball falls `4.9t²` metres in t seconds. Find its speed at t = 3, by shrinking the interval.

<details class="dl-answer"><summary>answer</summary>

The average speed from 3 to 3 + h is `(4.9(3+h)² − 4.9(9))/h`, which simplifies to `29.4 + 4.9h`. As h shrinks, that heads for **29.4 m/s**.

Which is `9.8 × 3` — the speed after t seconds of falling is `9.8t`.

</details>

**12.** What is the ball's speed at t = 0, and does the answer make sense?

<details class="dl-answer"><summary>answer</summary>

Zero, which is right: at the instant it is released it has not started moving.

Its *acceleration* is not zero — it is 9.8 m/s² throughout — which is why the speed does not stay at zero.

</details>

**13.** Why can you not just set the gap to zero and compute the answer directly?

<details class="dl-answer"><summary>answer</summary>

Because that gives `0/0`. The distance travelled in no time is zero, divided by no time.

`0/0` is not a number and not a shorthand for one — it is the arithmetic saying the question needs a different method. The limit is that method.

</details>

## Where Numbers Stop Helping

**14.** Compute `(x² − 1)/(x − 1)` at x = 1 + 1e-16. What happens, and why?

<details class="dl-answer"><summary>answer</summary>

You get something unhelpful — often 0, sometimes an error.

`1 + 1e-16` is not a different number from 1 in double-precision floating point, so the subtraction on the bottom gives exactly zero.

The mathematics is fine; the arithmetic ran out. The same thing that made two supposedly equal floats differ in *Storing and Computing*.

</details>

**15.** Given that, what should you use numbers for and what should you use algebra for?

<details class="dl-answer"><summary>answer</summary>

Numbers to *see* what the answer is — a column marching towards 2 is convincing and immediate.

Algebra to *know* it. Cancelling `(x − 1)` proves the answer is exactly 2, with no approximation anywhere and no floating-point floor.

Neither is a substitute for the other, and using the numbers alone will eventually mislead you.

</details>

## One Longer One

**16.** The perimeter of a regular n-sided polygon inscribed in a circle of radius 1 is `2n sin(π/n)`.

- (a) Compute it for n = 3, 6, 12, 100, 10000.
- (b) What is it approaching, and why?
- (c) What does that tell you about π?

<details class="dl-answer"><summary>answer</summary>

(a) About 5.196, 6.000, 6.211, 6.282, 6.28319.

(b) It approaches `2π ≈ 6.28319`, the circumference of the circle. As n grows the polygon gets closer to the circle, so its perimeter gets closer to the circle's.

(c) It gives you a way to compute π: take the perimeter of a many-sided polygon and halve it. This is essentially Archimedes' method from around 250 BCE, and it is a limit argument two thousand years before limits were defined.

```python
import math
for n in [3, 6, 12, 100, 10000]:
    print(n, 2 * n * math.sin(math.pi / n))
```

The circularity is worth noticing — using `math.pi` to compute π proves nothing. Archimedes worked the side lengths out geometrically instead, by repeatedly bisecting.

</details>

**17.** In your own words: what is the difference between "f(2) = 4" and "the limit of f as x approaches 2 is 4"?

<details class="dl-answer"><summary>answer</summary>

The first is a statement about the function *at* 2. The second is a statement about its behaviour *near* 2, and it does not require the function to have a value there at all.

The interesting cases are precisely the ones where the first is untrue and the second is — which is every derivative you will ever compute.

</details>
