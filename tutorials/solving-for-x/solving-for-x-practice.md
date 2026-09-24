---
title: "Solving for x: linear and quadratic equations — Practice"
practice_for: solving-for-x
year: "2026-2027"
version: 2026.09.24.1
---

# Solving for x: linear and quadratic equations — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `solve_linear` and
`solve_quadratic` from the tutorial, and `evaluate`, `plot_rule` and
`close_enough` from earlier pages. As on the tutorial, every answer
gets checked by putting it back in.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: solving-practice-warm-up
# Try things here
```

**1. Predict.** What does each line print?

```python
print(solve_linear(4, -10))
print(solve_linear(0, 3))
print(solve_quadratic(1, -5, 6))
```

<details class="dl-answer"><summary>answer</summary>

`2.5`, then `None`, then `[2.0, 3.0]`.

$4x - 10 = 0$ gives $x = \frac{10}{4} = 2.5$. $0x + 3 = 0$ has no
answer at all, so `solve_linear` keeps its promise and gives back
`None`. And $x^2 - 5x + 6 = (x - 2)(x - 3)$, so the roots are 2 and 3,
smallest first. They are floats, because the formula divides.

</details>

**2. Make.** A band hires a hall for €500. The venue pays the band €300,
plus €4 for every ticket sold. How many tickets must be sold for the
band to cover the hall? Write the equation, tidy it into the shape
$ax + b = 0$, solve it with `solve_linear`, and substitute the answer
back.

<details class="dl-answer"><summary>answer</summary>

$300 + 4t = 500$. Subtract 500 from both sides: $4t - 200 = 0$, so
$a = 4$ and $b = -200$.

```python
tickets = solve_linear(4, -200)
print(tickets)
print(300 + 4 * tickets)
```

It prints `50.0` and `500.0`: 50 tickets pay for the hall.

</details>

**3. Predict.** Without running anything, work out the discriminant of
each quadratic, and say how many real roots it has. Then check with
`solve_quadratic`.

- $x^2 + 2x + 1$
- $x^2 + x + 1$
- $x^2 - 9$

<details class="dl-answer"><summary>answer</summary>

| Quadratic | $b^2 - 4ac$ | Real roots |
|---|---|---|
| $x^2 + 2x + 1$ | $4 - 4 = 0$ | one, −1 |
| $x^2 + x + 1$ | $1 - 4 = -3$ | none |
| $x^2 - 9$ | $0 + 36 = 36$ | two, −3 and 3 |

```python
print(solve_quadratic(1, 2, 1))
print(solve_quadratic(1, 1, 1))
print(solve_quadratic(1, 0, -9))
```

It prints `[-1.0]`, `[]` and `[-3.0, 3.0]`. For $x^2 - 9$ there is no
$x$ term, so $b$ is 0.

</details>

**4. Explain.** A square rug covers 9 square metres. A friend writes
$x^2 = 9$ and says "so $x = 3$". Is that the whole answer to the
equation? Is it the whole answer to the question about the rug?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work out $3^2$, then $(-3)^2$.
2. Ask what $x$ stands for in the question.

**Think about:** which space the equation lives in, and which space the
rug lives in.

</details>

<details class="dl-answer"><summary>answer</summary>

The equation has two roots, 3 and −3, because $(-3)^2 = 9$ as well.
`solve_quadratic(1, 0, -9)` gives both. So "$x = 3$" is not the whole
answer to the equation.

It is the whole answer to the question. The side of a rug is a length,
and a length lives in the numbers from 0 up. There, −3 is not
allowed, and 3 is the only answer. Your friend was right about the
rug, and left out a root of the equation.

</details>

## Core

A cell for the core problems.

```python exec
id: solving-practice-core
# Your working for problems 5 to 12
```

**5. Make.** Two car hire companies charge for one day. Company A
charges €30, plus 10 cent a kilometre. Company B charges €20, plus 25
cent a kilometre. At what distance do they cost the same? Which is
cheaper for a 50 km trip to the coast?

<details class="dl-answer"><summary>answer</summary>

$30 + 0.10d = 20 + 0.25d$. Subtract $20 + 0.25d$ from both sides:
$-0.15d + 10 = 0$.

```python
distance = solve_linear(-0.15, 10)
print(distance)
print(30 + 0.10 * distance, 20 + 0.25 * distance)
print(30 + 0.10 * 50, 20 + 0.25 * 50)
```

The two companies cost the same at about 66.7 km, where each costs
about €36.67. For 50 km, A costs €35 and B costs €32.50, so B is
cheaper. B's day rate is lower, so B wins for short trips and A for
long ones.

</details>

**6. Fix.** It is 50 °F in New York. This cell tries to find that
temperature in Celsius by solving $\frac{9}{5}C + 32 = 50$ with
`solve_linear`. The check fails. Find the mistake.

```python exec
id: solving-practice-fix-weather
# 9/5 * C + 32 = 50, tidied into a*C + b = 0
a = 9 / 5
b = 50 - 32
celsius = solve_linear(a, b)
print(celsius)
assert close_enough(celsius_to_fahrenheit(celsius), 50)
print("It is", celsius, "degrees Celsius.")
```

<details class="dl-answer"><summary>answer</summary>

It prints `-10.0`, and the check fails: −10 °C is 14 °F. To tidy
$\frac{9}{5}C + 32 = 50$ into the shape $aC + b = 0$, we subtract 50
from both sides. That leaves $\frac{9}{5}C + 32 - 50 = 0$, so $b$ is
$32 - 50 = -18$, not $50 - 32$:

```python
b = 32 - 50
```

Now `celsius` is `10.0`, and the check passes. The mistake is a very
common one: moving a number across the equals sign and forgetting that
it changes sign. The check caught it, which is what it is for.

</details>

**7. Make.** Factorise $x^2 - 2x - 15$ by inspection, in your head: which
two numbers add to −2 and multiply to −15? Then check the roots with
`evaluate` and with `solve_quadratic`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. List pairs that multiply to 15: 1 and 15, 3 and 5.
2. One number of the pair must be negative, because the product is −15.
3. Which way round gives a sum of −2?

**Try this next:** $x^2 + x - 20$.

</details>

<details class="dl-answer"><summary>answer</summary>

3 and −5: $3 \times (-5) = -15$ and $3 + (-5) = -2$. So
$x^2 - 2x - 15 = (x + 3)(x - 5)$, and the roots are −3 and 5.

```python
print(evaluate([-15, -2, 1], -3), evaluate([-15, -2, 1], 5))
print(solve_quadratic(1, -2, -15))
```

Both give 0, and `solve_quadratic` gives `[-3.0, 5.0]`. For the next
one, $x^2 + x - 20 = (x + 5)(x - 4)$.

</details>

**8. Predict.** This is the tutorial's search loop, for a new pair of
targets. What will it print, and which quadratic is it factorising?

```python
target_sum = -7
target_product = 12

for p in range(-12, 13):
    for q in range(-12, 13):
        if p + q == target_sum and p * q == target_product:
            print(p, q)
```

<details class="dl-answer"><summary>answer</summary>

```text
-4 -3
-3 -4
```

The pair is −4 and −3, found in both orders. The quadratic is
$x^2 - 7x + 12 = (x - 3)(x - 4)$, with roots 3 and 4. The two numbers
in the brackets are negative, and the roots are positive: each root
makes its own bracket 0.

</details>

**9. Make.** A five-a-side pitch is a rectangle, 20 m longer than it is
wide, and covers 800 square metres. Write the equation, solve it with
`solve_quadratic`, and say which root is the width. How long is the
pitch?

<details class="dl-answer"><summary>answer</summary>

$w(w + 20) = 800$, which is $w^2 + 20w - 800 = 0$.

```python
print(solve_quadratic(1, 20, -800))
print(20 * (20 + 20))
```

The roots are −40 and 20. A width cannot be negative, so the pitch is
20 m wide and 40 m long, and $20 \times 40 = 800$. By inspection, the
pair is 40 and −20: $(w + 40)(w - 20) = 0$.

</details>

**10. Fix.** Here is someone's quadratic solver, with two tests that
substitute the roots back. The first test passes and the second fails.
Find the mistake.

```python exec
id: solving-practice-fix-roots
import math


def roots_of(a, b, c):
    """Return the real roots of a*x**2 + b*x + c = 0, smallest first."""
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return []
    root = math.sqrt(discriminant)
    return sorted([(-b - root) / 2 * a, (-b + root) / 2 * a])


for x in roots_of(1, -5, 6):
    assert close_enough(evaluate([6, -5, 1], x), 0), x
for x in roots_of(2, -7, 3):
    assert close_enough(evaluate([3, -7, 2], x), 0), x
print("roots_of keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Print `roots_of(2, -7, 3)`. The roots should be 0.5 and 3.
2. Work out `12 / 2 * 2` in your head, the way Python does: left to
   right.

**Think about:** why the first test could not find this mistake.

</details>

<details class="dl-answer"><summary>answer</summary>

`/ 2 * a` divides by 2, then multiplies by $a$. The formula divides by
$2a$, so the bottom needs brackets:

```python
    return sorted([(-b - root) / (2 * a), (-b + root) / (2 * a)])
```

With the mistake, `roots_of(2, -7, 3)` gives `[2.0, 12.0]`. The first
test passed because there $a$ is 1, and dividing by 2 then multiplying
by 1 is the same as dividing by 2. A test with $a = 1$ alone would never
have found this. It is the order of operations from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#which-comes-first).

</details>

**11. Explain.** For $x^2 + 4 = 0$, the toolkit's `solve_quadratic`
gives back `[]`, an empty list. It could have stopped with an error
instead. Why is an empty list a better way to keep its promise? Think
about a loop like `for x in solve_quadratic(a, b, c):`.

<details class="dl-answer"><summary>answer</summary>

The promise is "a list of the real roots". When there are none, an
empty list keeps that promise exactly: it says "no real roots" in the
same shape as "two roots" or "one root".

Code that uses the tool does not need a special case. A loop over an
empty list runs 0 times and moves on, so a check like the tutorial's
works for every quadratic. An error would stop the whole program, even
though "no real roots" is a true answer, not a mistake. An error is the
right choice when the input itself is wrong, such as $a = 0$, which the
docstring rules out.

</details>

**12. Another way.** Solve $x^2 - 6x + 8 = 0$ three ways: by inspection,
with `solve_quadratic`, and by drawing it with `plot_rule` and reading
where it crosses the x-axis. Do all three agree?

<details class="dl-answer"><summary>answer</summary>

By inspection: −2 and −4 add to −6 and multiply to 8, so
$x^2 - 6x + 8 = (x - 2)(x - 4)$, with roots 2 and 4.

```python
def six_eight(x):
    return x ** 2 - 6 * x + 8

print(solve_quadratic(1, -6, 8))
plot_rule(six_eight, 0, 6)
```

`solve_quadratic` gives `[2.0, 4.0]`, and the graph crosses the x-axis
at 2 and 4. The picture shows the roots at a glance. Inspection is
quick when the roots are whole numbers. The formula always works.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: solving-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** €1,000 is saved for two years at a rate $r$ a year, with
compound growth as on
[Doubling and halving](tutorial:doubling-and-halving#how-long-to-double).
After two years there is €1,102.50. So $1000(1 + r)^2 = 1102.5$. Find
$r$ as a percentage.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Expand $(1 + r)^2$ into $1 + 2r + r^2$, then multiply by 1000.
2. Subtract 1102.5 from both sides, so the right side is 0.
3. Read off $a$, $b$ and $c$, and use `solve_quadratic`.

**Think about:** which root is a rate a bank would offer.

</details>

<details class="dl-answer"><summary>answer</summary>

$1000 + 2000r + 1000r^2 - 1102.5 = 0$, which is
$1000r^2 + 2000r - 102.5 = 0$.

```python
rates = solve_quadratic(1000, 2000, -102.5)
print(rates)
print(1000 * (1 + rates[1]) ** 2)
```

The roots are about −2.05 and 0.05. A rate of −205% would mean the bank
takes more than you saved, so the rate is 0.05, which is 5%. Putting it
back gives about €1,102.50. Another way: $(1 + r)^2 = 1.1025$, so
$1 + r = \sqrt{1.1025} = 1.05$.

</details>

**14. Another way.** Here is a fact about any quadratic
$ax^2 + bx + c$ with two roots: the roots add to $-\frac{b}{a}$, and
multiply to $\frac{c}{a}$. Check it with `solve_quadratic` on
$x^2 - 7x + 12$ and $2x^2 - 7x + 3$. Then use it: one root of
$x^2 - 10x + 21 = 0$ is 3. What is the other, with no formula?

<details class="dl-answer"><summary>answer</summary>

```python
for a, b, c in [(1, -7, 12), (2, -7, 3)]:
    first, second = solve_quadratic(a, b, c)
    print(first + second, -b / a, first * second, c / a)
```

For $x^2 - 7x + 12$, the roots 3 and 4 add to 7 and multiply to 12. For
$2x^2 - 7x + 3$, the roots 0.5 and 3 add to 3.5 and multiply to 1.5.
Both match.

For $x^2 - 10x + 21$ the roots add to 10, so the other root is
$10 - 3 = 7$. Check: $3 \times 7 = 21$. This is factorising by
inspection, seen from the roots' side: when $a$ is 1, the two numbers
you look for are the roots with their signs turned round.

</details>

**15. Explain.** Try `solve_linear` on $2(x + 3) = 2x + 6$, and then on
$2(x + 3) = 2x + 7$. Tidy each into the shape $ax + b = 0$ first. Both
give `None`. Do they mean the same thing?

<details class="dl-answer"><summary>answer</summary>

Expanding $2(x + 3)$ gives $2x + 6$. Take away the right side:

- $2(x + 3) = 2x + 6$ becomes $0x + 0 = 0$, so `solve_linear(0, 0)`.
- $2(x + 3) = 2x + 7$ becomes $0x - 1 = 0$, so `solve_linear(0, -1)`.

Both give `None`, and for different reasons. The first is true for
every $x$: it is an identity, as on
[Rules with letters in them](tutorial:rules-with-letters-in-them). The
second is true for no $x$ at all. `None` promises only "no single
answer". A tool that needed to tell the two apart would have to look at
$b$ as well.

</details>
