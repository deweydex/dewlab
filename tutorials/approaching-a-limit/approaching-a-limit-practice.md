---
title: "Limits: getting closer without arriving — Practice"
practice_for: approaching-a-limit
year: "2026-2027"
version: 2026.08.23.1
---

# Limits: getting closer without arriving — Practice

Each answer is hidden in a fold under its question. Try the question
first, then open the fold to check.

When a question asks you to find a limit, try two things:

1. Try it with numbers, from both sides.
2. Say what the algebra gives.

When the two agree, you can trust the answer.

## Tools

This cell defines `approach`, a helper that prints a function's values
as the input comes closer to a target. It then tries it on
$\dfrac{x^2 - 1}{x - 1}$ near 1, the example from the tutorial.

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

## Finding a limit

**1.** What is the limit of $\dfrac{x^2 - 4}{x - 2}$ as $x$ approaches 2?

<details class="dl-answer"><summary>answer</summary>

4.

The top factorizes as $(x - 2)(x + 2)$. So away from $x = 2$, the
function is the same as $x + 2$. At 2, that would be $2 + 2 = 4$.

The function itself has no value at 2. The bottom is zero there, so we
are not allowed to cancel. The limit says what the value *would* be, and
that is a different statement.

</details>

**2.** What is the limit of $\dfrac{x^2 - 9}{x - 3}$ as $x$ approaches 3?

<details class="dl-answer"><summary>answer</summary>

6.

Factorize in the same way: $\dfrac{(x - 3)(x + 3)}{x - 3}$ leaves
$x + 3$. At 3, that is $3 + 3 = 6$.

</details>

**3.** What is the limit of $\dfrac{x^3 - 1}{x - 1}$ as $x$ approaches 1?

<details class="dl-answer"><summary>answer</summary>

3.

$x^3 - 1$ factorizes as $(x - 1)(x^2 + x + 1)$. The $(x - 1)$ cancels,
leaving $x^2 + x + 1$. At $x = 1$ that is $1 + 1 + 1 = 3$.

</details>

**4.** What is the limit of $\dfrac{\sqrt{x} - 2}{x - 4}$ as $x$
approaches 4?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{1}{4}$.

Write the bottom as $(\sqrt{x} - 2)(\sqrt{x} + 2)$. The $(\sqrt{x} - 2)$
cancels, leaving $\dfrac{1}{\sqrt{x} + 2}$. At $x = 4$ that is
$\dfrac{1}{2 + 2} = \dfrac{1}{4}$.

It is worth checking with numbers too. The values head for 0.25 from
both sides.

</details>

**5.** Does $\dfrac{|x|}{x}$ have a limit as $x$ approaches 0?

<details class="dl-answer"><summary>answer</summary>

No.

From the right, it is 1, because a positive number divided by itself is
1. From the left, it is −1. The two sides disagree, so there is no
single value it is heading for.

This is the step function from the tutorial, written in different
notation.

</details>

## Limits that do not exist

**6.** What happens to $\dfrac{1}{x^2}$ as $x$ approaches 0? Is that a
limit?

<details class="dl-answer"><summary>answer</summary>

It grows without end from *both* sides, because squaring removes the
minus sign.

Strictly, there is no limit, because no number is being approached.
People often write "the limit is infinity". That is a short way of
saying "it grows without end". It does not claim that infinity is a
number.

</details>

**7.** How is $\dfrac{1}{x}$ different from $\dfrac{1}{x^2}$ near zero?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{1}{x}$ goes to positive infinity from the right and to negative
infinity from the left. $\dfrac{1}{x^2}$ goes to positive infinity from
both sides.

Neither one has a limit. But the second one at least does the same thing
on both sides.

</details>

**8.** What is the limit of $\dfrac{1}{x}$ as $x$ grows without end?

<details class="dl-answer"><summary>answer</summary>

0.

The values shrink towards zero and never reach it. This is the same kind
of statement as before: the value is approached, but never reached.

</details>

**9.** What is the limit of $\dfrac{3n + 5}{n + 2}$ as $n$ grows without
end?

<details class="dl-answer"><summary>answer</summary>

3.

Divide the top and the bottom by $n$:
$\dfrac{3 + \frac{5}{n}}{1 + \frac{2}{n}}$. As $n$ grows, both small
terms, $\frac{5}{n}$ and $\frac{2}{n}$, head for 0. That leaves
$\dfrac{3}{1} = 3$.

A useful rule of thumb: for large $n$, only the highest powers matter.
So the answer is the ratio of the numbers in front of the highest powers
(the leading coefficients).

</details>

**10.** What is the limit of $\dfrac{2n^2 + n}{5n^2 - 3}$ as $n$ grows
without end?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{2}{5}$.

The reasoning is the same. The $n^2$ terms are much bigger than
everything else, so everything else stops mattering. What is left is
$\dfrac{2n^2}{5n^2} = \dfrac{2}{5}$.

</details>

## Why limits matter

**11.** A ball falls $4.9t^2$ metres in $t$ seconds. What is its speed at
$t = 3$? Find it by making the time interval smaller and smaller.

<details class="dl-answer"><summary>answer</summary>

The average speed from $t = 3$ to $t = 3 + h$ is

$$\frac{4.9(3 + h)^2 - 4.9 \times 9}{h}.$$

Expand the top: $4.9(9 + 6h + h^2) - 44.1 = 29.4h + 4.9h^2$. Divide by
$h$ to get $29.4 + 4.9h$.

As $h$ shrinks, that heads for **29.4 m/s**.

That is $9.8 \times 3$. The speed after $t$ seconds of falling is
$9.8t$.

</details>

**12.** What is the ball's speed at $t = 0$? Does the answer make sense?

<details class="dl-answer"><summary>answer</summary>

Zero. That is right: at the instant the ball is let go, it has not
started moving.

Its *acceleration*, how fast its speed is changing, is not zero. It is
9.8 m/s² the whole time. That is why the speed does not stay at zero.

</details>

**13.** Why can we not set the gap to zero and compute the answer
directly?

<details class="dl-answer"><summary>answer</summary>

Because that gives $\dfrac{0}{0}$: a distance of zero, travelled in no
time, divided by no time.

$\dfrac{0}{0}$ is not a number, and it is not a short way of writing
one. It is the arithmetic telling us that the question needs a different
method. The limit is that method.

</details>

## Where numbers stop helping

**14.** Compute $\dfrac{x^2 - 1}{x - 1}$ in Python at `x = 1 + 1e-16`.
What happens, and why?

<details class="dl-answer"><summary>answer</summary>

Python stops with a `ZeroDivisionError`. (Some other tools, such as
NumPy, give `nan`, "not a number", instead. Either way, the answer is
no help.)

In double-precision floating point, `1 + 1e-16` is the same number as
`1`. So the subtraction on the bottom gives exactly zero.

The mathematics is fine; the arithmetic ran out. This is the same limit
that makes `0.1 + 0.2 == 0.3` come out `False`, on the practice page for
[Variables, data types and text](tutorial:storing-and-computing).

</details>

**15.** So what should we use numbers for, and what should we use algebra
for?

<details class="dl-answer"><summary>answer</summary>

We use numbers to *see* what the answer is. A column of values moving
towards 2 is convincing, and quick to produce.

We use algebra to *know* it. Cancelling $(x - 1)$ proves that the answer
is exactly 2, with no approximation anywhere and no floating-point
floor.

Neither one can replace the other. Using the numbers alone will
eventually mislead you.

</details>

## One longer one

**16.** A regular polygon with $n$ equal sides fits inside a circle of
radius 1, with its corners on the circle. Its perimeter is
$2n \sin\left(\dfrac{\pi}{n}\right)$.

1. Compute the perimeter for $n$ = 3, 6, 12, 100 and 10000.
2. What is it approaching, and why?
3. What does that tell you about $\pi$?

<details class="dl-answer"><summary>answer</summary>

1. About 5.196, 6.000, 6.212, 6.282 and 6.28319.

2. It approaches $2\pi \approx 6.28319$, the circumference of the
   circle. As $n$ grows, the polygon gets closer to the circle, so its
   perimeter gets closer to the circle's circumference.

3. It gives us a way to compute $\pi$: take the perimeter of a polygon
   with many sides and halve it. This is close to Archimedes' method from
   around 250 BCE. It is a limit argument, made two thousand years
   before limits were defined.

```python
import math
for n in [3, 6, 12, 100, 10000]:
    print(n, 2 * n * math.sin(math.pi / n))
```

Notice the circle in the reasoning here: this code uses `math.pi` to
compute $\pi$, so it proves nothing. Archimedes worked out the side
lengths with geometry instead, by cutting angles in half again and
again.

</details>

**17.** In your own words: what is the difference between "$f(2) = 4$"
and "the limit of $f(x)$ as $x$ approaches 2 is 4"?

<details class="dl-answer"><summary>answer</summary>

The first is a statement about the function *at* 2. The second is a
statement about what it does *near* 2. The second does not need the
function to have a value at 2 at all.

The interesting cases are exactly the ones where the first statement is
false and the second is true. Every derivative you will ever compute is
one of those cases.

</details>
