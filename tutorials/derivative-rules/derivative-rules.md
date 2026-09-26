---
title: "Derivative rules: power, sum, product and chain, found by experiment"
year: "2026-2027"
version: 2026.09.26.1
covers:
  a-pattern-in-the-slopes:
    covers: [MIT-3.7]
  adding-things-together:
    covers: [MIT-3.7]
  multiplying-things-together:
    covers: [MIT-3.7]
  one-function-inside-another:
    covers: [MIT-3.7]
  rules-in-your-world:
    covers: [MIT-3.7]
  going-further-running-it-backwards:
    covers: [MIT-3.6]
worlds:
  sea-and-sky: An oil spill, spreading in a circle. The numbers are made up.
  planets-and-moons: Sunlight on a spacecraft moving away from the Sun. The numbers are made up.
  fantasy-maps: A growing town, and the tax it pays. The numbers are made up.
---

# Derivative rules: power, sum, product and chain, found by experiment

In [Derivatives: the rate of change of a curve](tutorial:rates-of-change)
we found every slope from a limit, with `derivative_at`. Here it is
again, with a table of slopes for $x$, $x^2$, $x^3$ and $x^4$ at three
places. Can you find a pattern in each row?

```python exec
id: a-pattern-in-the-slopes-1
def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


print("  function        slope at 2      slope at 3      slope at 5")
for name, f in [("x", lambda x: x),
                ("x^2", lambda x: x ** 2),
                ("x^3", lambda x: x ** 3),
                ("x^4", lambda x: x ** 4)]:
    row = [f"{derivative_at(f, x):>13.4f}" for x in (2, 3, 5)]
    print(f"  {name:<12} {''.join(row)}")
```

Computing a limit every time would be tiring. On this page we look for
patterns in the answers, and each pattern becomes a rule. We find every
rule the same way: compute the slopes with numbers, look, guess, and
check the guess.

## A pattern in the slopes

Compare each row with powers of the $x$ values. For example, the slope
of $x^3$ at 3 is 27, which is $3 \times 3^2$. The slope of $x^4$ at 2 is
32, which is $4 \times 2^3$. The pattern is:

| Function | Its derivative |
|---|---|
| $x$ | $1$ everywhere |
| $x^2$ | $2x$ |
| $x^3$ | $3x^2$ |
| $x^4$ | $4x^3$ |

> **The power rule:** the derivative of $x^n$ is $n x^{n-1}$.

In words: bring the power down to the front, and reduce the power by
one. For example, the derivative of $x^7$ is $7x^6$.

A guess from four rows is only a guess. The next cell checks the rule
against the numbers for powers the table did not have, at $x = 2.5$.

```python exec
id: a-pattern-in-the-slopes-2
def power_rule(n):
    """The derivative of x^n, as a function."""
    return lambda x: n * x ** (n - 1)


for n in [1, 2, 5, 7, 0.5, -1]:
    numeric = derivative_at(lambda x: x ** n, 2.5)
    by_rule = power_rule(n)(2.5)
    print(f"x^{n}:  numerically {numeric:>12.5f}   by the rule {by_rule:>12.5f}")
```

The rule holds for a power of a half, $\sqrt{x}$, and for a power of
$-1$, $\frac{1}{x}$, too. A number on its own, such as 5, never
changes, so its slope is 0.

## Adding things together

What is the slope of $x^3 + x^2$? Here $f$ is $x^3$ and $g$ is $x^2$.
Before you run the cell, can you guess how the third slope relates to
the first two? Write your guess in a comment first. Then run the cell.

```python exec
id: adding-things-together-1
f = lambda x: x ** 3
g = lambda x: x ** 2
both = lambda x: f(x) + g(x)

for x in [1, 2, 4]:
    print(f"at x = {x}:  slope of f is {derivative_at(f, x):>8.4f},"
          f"  of g is {derivative_at(g, x):>8.4f},"
          f"  of f+g is {derivative_at(both, x):>8.4f}")
```

> **The sum rule:** the derivative of $f + g$ is the derivative of $f$
> plus the derivative of $g$.

A polynomial is a sum of powers, so we can differentiate it one term at
a time. For example, the derivative of $x^2 + 6x + 5$ is $2x + 6 + 0$,
which is $2x + 6$.

In [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
we kept a polynomial as a list of its coefficients, from the constant
term upwards: `[5, 6, 1]` means $5 + 6x + x^2$. The power rule and the
sum rule together turn one list into another. The number at position
$i$ belongs to $x^i$, so its derivative is $i$ times the number, one
place lower.

```python exec
id: adding-things-together-2
def differentiate_polynomial(coefficients):
    """Coefficients from the constant term upwards: [c, b, a] means a x^2 + b x + c."""
    return [i * coefficients[i] for i in range(1, len(coefficients))]


def evaluate(coefficients, x):
    total = 0
    for i in range(len(coefficients)):
        total += coefficients[i] * x ** i
    return total


poly = [5, 6, 1]           # 5 + 6x + x^2
slope_poly = differentiate_polynomial(poly)
print("the polynomial:", poly)
print("its derivative:", slope_poly)

for x in [-5, -3, 0, 2]:
    print(f"  at x = {x:>3}:  by rule {evaluate(slope_poly, x):>8.4f}"
          f"   numerically {derivative_at(lambda v: evaluate(poly, v), x):>8.4f}")
```

The derivative is `[6, 2]`, which means $6 + 2x$: the $2x + 6$ we found
by hand.

### Your turn, on paper

Can you differentiate $5x^3 + 4x^2 - x + 2$ by hand? Then check your
answer at $x = 2$ with `derivative_at`, and with
`differentiate_polynomial`.

```python exec
id: adding-things-together-3
# Your answer, then two checks.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

The derivative is $15x^2 + 8x - 1$. At $x = 2$ that is
$60 + 16 - 1 = 75$. `derivative_at(lambda x: 5 * x ** 3 + 4 * x ** 2 - x + 2, 2)`
prints about 75, and `differentiate_polynomial([2, -1, 4, 5])` returns
`[-1, 8, 15]`.

</details>

## Multiplying things together

Adding split neatly into its parts. Does multiplying work the same way? Here $f$
is $x^2$ and $g$ is $x^3$, at $x = 2$.

```python exec
id: multiplying-things-together-1
f = lambda x: x ** 2
g = lambda x: x ** 3
product = lambda x: f(x) * g(x)

x = 2
print("slope of f:      ", derivative_at(f, x))
print("slope of g:      ", derivative_at(g, x))
print("those multiplied:", derivative_at(f, x) * derivative_at(g, x))
print("slope of f*g:    ", derivative_at(product, x))
```

```predict
type: choice

Will the last two lines match?

- Yes, both will be about 48
  - Adding split into its parts, so multiplying should split too.
- No, they will be different
```

They do not match, and they are not close: 48 against 80. Multiplying
the two derivatives does not give the derivative of the product.

So what does? Here are three guesses, each tried against the numbers at
three places. $f'$ is the slope of $f$, which is $2x$, and $g'$ is the
slope of $g$, which is $3x^2$.

```python exec
id: multiplying-things-together-2
df = lambda x: 2 * x          # the slope of f
dg = lambda x: 3 * x ** 2     # the slope of g

guesses = {
    "f' g'":        lambda x: df(x) * dg(x),
    "f' g + f g'":  lambda x: df(x) * g(x) + f(x) * dg(x),
    "f' g":         lambda x: df(x) * g(x),
}

for x in [1, 2, 3]:
    print(f"x = {x}:  the slope is {derivative_at(product, x):>8.2f}")
    for name, guess in guesses.items():
        print(f"      {name:<12} gives {guess(x):>8.2f}")
```

Only one guess matches at every place.

> **The product rule:** the derivative of $f \cdot g$ is
> $f' \cdot g + f \cdot g'$.

In words: differentiate the first and leave the second alone. Then
differentiate the second and leave the first alone. Add the two results.

We can check this another way. $x^2 \cdot x^3$ is $x^5$, and by the
power rule its derivative is $5x^4$. The product rule gives:

$$2x \cdot x^3 + x^2 \cdot 3x^2 = 2x^4 + 3x^4 = 5x^4$$

At $x = 2$, $5x^4 = 5 \times 16 = 80$, the same 80 as above.

### Your turn, on paper

Can you differentiate $(2x - 1)(x^2 + 4)$ with the product rule? Then
multiply the brackets out and differentiate the polynomial. Do the two
agree? Check at $x = 2$ with `derivative_at`.

```python exec
id: multiplying-things-together-3
# Your two answers, then a check.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

By the product rule: $2(x^2 + 4) + (2x - 1) \cdot 2x = 6x^2 - 2x + 8$.

Multiplied out: $(2x - 1)(x^2 + 4) = 2x^3 - x^2 + 8x - 4$, and its
derivative is $6x^2 - 2x + 8$. The two agree. At $x = 2$ both give 28,
and so does `derivative_at(lambda x: (2 * x - 1) * (x ** 2 + 4), 2)`.

</details>

## One function inside another

What happens when one function is inside another? Here the inner
function is $2x + 1$, and the outer function cubes whatever it is given.
So the whole thing is $(2x + 1)^3$. The cell finds three slopes: the
inner one, the outer one at the value the inner one gives, and the
whole.

```python exec
id: one-function-inside-another-1
inner = lambda x: 2 * x + 1
outer = lambda u: u ** 3
nested = lambda x: outer(inner(x))

x = 1.5
print("slope of the inner:  ", derivative_at(inner, x))
print("slope of the outer at inner(x):", derivative_at(outer, inner(x)))
print("those multiplied:    ",
      derivative_at(inner, x) * derivative_at(outer, inner(x)))
print("slope of the whole:  ", derivative_at(nested, x))
```

```predict
type: choice

After the product rule, will the last two lines agree this time?

- Yes
- No
  - Multiplying two slopes gave the wrong answer for a product, so it
    should give the wrong answer here too.
```

Those last two agree: both are 96. Here multiplying the slopes does
work.

> **The chain rule:** the derivative of $f(g(x))$ is
> $f'(g(x)) \cdot g'(x)$.

In words: first, differentiate the outside function, and leave the
inside alone. Then multiply by the derivative of the inside.

The idea behind it is that rates multiply. Suppose $u$ changes three
times as fast as $x$, and $y$ changes twice as fast as $u$. Then $y$
changes $3 \times 2 = 6$ times as fast as $x$. Rates multiply along a
chain, and that gives the rule its name. A product is not a chain: $f$
and $g$ are side by side, and neither is inside the other.

### Your turn, on paper

How might you differentiate $(2x - 5)^4$ with the chain rule? Name the
inside and the outside function first. Then check your answer at
$x = 3$ with `derivative_at`.

```python exec
id: one-function-inside-another-2
# Your answer, then the check.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

The inside is $2x - 5$, with slope 2. The outside is $u^4$, with slope
$4u^3$. So the derivative is $4(2x - 5)^3 \times 2 = 8(2x - 5)^3$. At
$x = 3$ that is $8 \times 1^3 = 8$, and `derivative_at` agrees.

</details>

## Rules in your world

<div class="dl-world" data-world="sea-and-sky">

Oil from a damaged ship spreads in a circle. Its radius is $2t$ metres,
$t$ minutes after the leak starts, so its area is $\pi(2t)^2$. How fast
is the area growing after 25 minutes, when the radius is 50 m? Can you
write `area_rate(t)` from the rules, and check it with `derivative_at`?

```python exec
id: rules-in-your-world-1--sea-and-sky
import math


def area(t):
    return math.pi * (2 * t) ** 2
```

```hint
The area is $\pi r^2$, with $r = 2t$ inside it. Which rule is for one
function inside another?
```

```inputs
round(area_rate(25), 2)
round(derivative_at(area, 25), 2)
```

```solution
def area_rate(t):
    radius = 2 * t
    return 2 * math.pi * radius * 2    # the slope of pi r^2, times the slope of 2t
---
By the chain rule, the slope of $\pi r^2$ is $2\pi r$, and the radius
grows at 2 m a minute, so the area grows at $2\pi r \times 2$. At 50 m
that is about 628 square metres a minute. The same spill grows faster
and faster, because a longer edge moves outwards each minute.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

At 1 AU from the Sun, sunlight brings 1361 watts to each square metre.
The brightness is $\dfrac{1361}{d^2}$ at $d$ AU. A spacecraft is at
$d = 1 + 0.01t$, $t$ days after it passes the Earth's distance. How fast
is its sunlight falling at $t = 0$? Can you write `light_rate(t)` from
the rules, and check it with `derivative_at`?

```python exec
id: rules-in-your-world-1--planets-and-moons
def light(t):
    return 1361 / (1 + 0.01 * t) ** 2
```

```hint
$\dfrac{1361}{d^2}$ is $1361 d^{-2}$, and the power rule works for $-2$.
$d$ is itself a function of $t$.
```

```inputs
round(light_rate(0), 2)
round(derivative_at(light, 0), 2)
round(light_rate(100), 2)
```

```solution
def light_rate(t):
    d = 1 + 0.01 * t
    return 1361 * -2 * d ** -3 * 0.01    # the slope of 1361 d^-2, times the slope of d
---
By the power rule, the slope of $1361 d^{-2}$ is $-2722 d^{-3}$, and
$d$ grows by 0.01 AU a day, so the chain rule gives about $-27.2$ watts
per square metre each day at $t = 0$. After 100 days, at 2 AU, it falls
only about $-3.4$ each day: the light is already a quarter as bright.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A town grows by 50 people a year, from 1000. Each person pays a tax
that grows too: $2 + 0.1t$ gold pieces a year, $t$ years from now. So
the town pays $(1000 + 50t)(2 + 0.1t)$ gold a year. How fast is that
growing after 10 years? Can you write `tax_rate(t)` from the rules, and
check it with `derivative_at`?

```python exec
id: rules-in-your-world-1--fantasy-maps
def tax(t):
    return (1000 + 50 * t) * (2 + 0.1 * t)
```

```hint
The tax is one thing times another. Which rule is for a product? What
are the slopes of the two parts?
```

```inputs
round(tax_rate(10), 2)
round(derivative_at(tax, 10), 2)
```

```solution
def tax_rate(t):
    people, each = 1000 + 50 * t, 2 + 0.1 * t
    return 50 * each + people * 0.1    # the product rule
---
By the product rule, the rate is $50(2 + 0.1t) + (1000 + 50t) \times 0.1$.
After 10 years that is $150 + 150 = 300$ gold a year, every year. Half
of the growth comes from more people, and half from each paying more.
```

</div>

## Going further: running it backwards

Differentiating goes from a total to its rate of change. Can we go the
other way, from a rate back to the total? Going backwards is called
*integration*. For a polynomial, we can undo the power rule: $x^n$ came
from $\frac{x^{n+1}}{n + 1}$. So each number moves one place up, and is
divided by its new position.

```python exec
id: going-further-running-it-backwards-1
def integrate_polynomial(coefficients):
    """The polynomial whose derivative is this one, with 0 as its constant."""
    return [0] + [coefficients[i] / (i + 1) for i in range(len(coefficients))]


rate = [6, 2]                          # 6 + 2x
total = integrate_polynomial(rate)
print("back to:", total)
print("and forward again:", differentiate_polynomial(total))
print("the original:", differentiate_polynomial([5, 6, 1]))
```

The round trip gives `[6, 2]` back, but `integrate_polynomial` returns
`[0, 6.0, 1.0]`, not the `[5, 6, 1]` we started from. The 5 is lost,
because a number on its own has a slope of 0. Any constant would give
the same derivative, so integration cannot know which one it was. That
unknown number is called the *constant of integration*.

What does integration mean in the world? The falling ball's speed is
$9.8t$. Integrating it gives $4.9t^2$, the distance fallen: going from
a speed back to a distance. Can you check that with
`integrate_polynomial([0, 9.8])`?

## Looking back

Every rule on this page was found the same way: compute slopes with
numbers, see a pattern, guess a rule, and check the guess against more
numbers. Powers bring the power down. Sums split into their parts.
Products do not: they need $f'g + fg'$. For one function inside
another, the rates multiply.

The quotient rule, for one function divided by another, is not on this
page. You can manage without it. Write the division as a product with a
power of $-1$, and use the product rule and the chain rule.

Which of the four rules surprised you most? Why?

A challenge: in
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
you wrote `multiply_poly`. Can you use it with `differentiate_polynomial`
to check the product rule for any two polynomials, as lists?

```python challenge
def differentiate_polynomial(coefficients):
    return [i * coefficients[i] for i in range(1, len(coefficients))]


def multiply_poly(a, b):
    """The product of two polynomials, as lists from the constant term up."""
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] += a[i] * b[j]
    return result


f = [-1, 2]       # 2x - 1
g = [4, 0, 1]     # x^2 + 4
# Your code here: is the derivative of f*g the same as f' g + f g'?
```

[The slope of a wave](tutorial:the-slope-of-a-wave) uses these rules
on sine and cosine.

## Where to read more

3Blue1Brown (2017). *Visualizing the chain rule and product rule:
Chapter 4, Essence of calculus.* <https://www.youtube.com/watch?v=YG15m2VwSjA>.
Grant Sanderson draws the product rule as the area of a rectangle whose
sides grow, and the chain rule as rates passed along a line of machines.

3Blue1Brown (2017). *Integration and the fundamental theorem of
calculus: Chapter 8, Essence of calculus.*
<https://www.youtube.com/watch?v=rfG8ce4nNh0>. This video explains why
running a derivative backwards finds an area, which this page only
touched.
