---
title: "Polynomials: representing and combining them in Python — Practice"
practice_for: expressions-come-alive
year: "2026-2027"
version: 2026.09.26.1
worlds:
  rockets: Rockets, launches and the arcs they fly. The numbers are made up.
  electronics: Batteries, resistors and the power between them. The numbers are made up.
---

# Polynomials: representing and combining them in Python — Practice

The answers are hidden in folds under each problem. Try each expansion
by hand first. Then use the cell to check your answer. The cell is there
to settle a doubt, not to do the work for you.

The expansion problems are adapted from an earlier worksheet on
expanding brackets.

## Expanding

```python exec
id: expanding-1
def multiply_poly(a, b):
    """Multiply two polynomials given as coefficient lists, index = power."""
    result = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            result[i + j] += ca * cb
    return result


# (x + 3)(x + 2), with the constant first
print(multiply_poly([3, 1], [2, 1]))
```

**1.** Expand each one.

- (a) $(t + 2)(t + 5)$
- (b) $(p + 6)(p + 3)$
- (c) $(m + 4)(m + 7)$
- (d) $(k + 8)(k + 2)$

<details class="dl-answer"><summary>answer</summary>

(a) $t^2 + 7t + 10$. (b) $p^2 + 9p + 18$. (c) $m^2 + 11m + 28$. (d) $k^2 + 10k + 16$.

Look at the numbers. In every answer, the middle number is the sum of
the two constants, and the last number is their product. In (a),
$2 + 5 = 7$ and $2 \times 5 = 10$. This is not a coincidence. It makes
factorising possible. When you factorise, you go backwards from the
expanded form to the brackets. You will do that in
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).

</details>

**2.** Expand $(n + 5)(n + 5)$ and $(w + 3)(w + 3)$. Can you see a
general rule?

<details class="dl-answer"><summary>answer</summary>

They are $n^2 + 10n + 25$ and $w^2 + 6w + 9$.

The rule is $(x + a)^2 = x^2 + 2ax + a^2$. The middle coefficient is
twice the constant, because the $ax$ term appears twice: once from the
Outer product and once from the Inner product.

</details>

**3.** The tutorial found that $(a + b)^2$ is not $a^2 + b^2$. Is
$(a - b)^2$ the same as $a^2 - b^2$? Is $\sqrt{a + b}$ the same as
$\sqrt{a} + \sqrt{b}$? Try each with numbers before you decide.

<details class="dl-answer"><summary>answer</summary>

Neither is the same.

$(a - b)^2 = a^2 - 2ab + b^2$. With $a = 5$ and $b = 3$, $(5 - 3)^2 = 4$,
but $5^2 - 3^2 = 16$. The expression $a^2 - b^2$ is $(a - b)(a + b)$,
which is a different product.

Square roots do not split over a sum either:
$\sqrt{9 + 16} = \sqrt{25} = 5$, but $\sqrt{9} + \sqrt{16} = 7$.

A power or a root of a sum is not the sum of the powers or roots. A
power of a product does split: $(ab)^2 = a^2 b^2$.

</details>

**4.** Expand each one. Watch the minus signs.

- (a) $(x - 3)(x + 5)$
- (b) $(x - 4)(x - 6)$
- (c) $(x + 7)(x - 7)$
- (d) $(x - 5)^2$

<details class="dl-answer"><summary>answer</summary>

(a) $x^2 + 2x - 15$. (b) $x^2 - 10x + 24$. (c) $x^2 - 49$. (d) $x^2 - 10x + 25$.

(c) is called the *difference of two squares*: $(x + a)(x - a) = x^2 - a^2$.
The two middle terms, $-7x$ and $+7x$, cancel out. It is worth learning
to spot this pattern quickly, in both directions.

</details>

**5.** Expand each one. This time the $x$ terms have coefficients.

- (a) $(2x + 3)(x + 4)$
- (b) $(3x - 1)(2x + 5)$
- (c) $(5x + 2)^2$

<details class="dl-answer"><summary>answer</summary>

(a) $2x^2 + 11x + 12$. (b) $6x^2 + 13x - 5$. (c) $25x^2 + 20x + 4$.

</details>

**6.** Expand $(x + 2)(x^2 + 3x + 1)$.

<details class="dl-answer"><summary>answer</summary>

It is $x^3 + 5x^2 + 7x + 2$.

A *binomial* is a polynomial with two terms, such as $x + 2$. FOIL only
names the four products you get from two binomials. The real rule is
that every term multiplies every term. Here that gives six products,
since $2 \times 3 = 6$. That rule works for any polynomials, where FOIL
does not.

</details>

## Polynomials as lists

**7.** Write each one as a coefficient list, with the constant first.

- (a) $3x^2 + 5x - 2$
- (b) $2x^3 - 3x^2 + 1$
- (c) $7$
- (d) $x^5$

<details class="dl-answer"><summary>answer</summary>

(a) `[-2, 5, 3]`. (b) `[1, 0, -3, 2]`. (c) `[7]`. (d) `[0, 0, 0, 0, 0, 1]`.

Index $i$ holds the coefficient of $x^i$. So a missing power has a
coefficient of zero, and in (b) and (d) its place must stay in the list.
Those zeros say "no term with this power".

</details>

**8.** Here is `evaluate_poly` from the tutorial, and a polynomial to
evaluate at $x = -1$.

```python exec
id: evaluate-at-minus-one
def evaluate_poly(coeffs, x):
    """The value at x of the polynomial whose coefficients are in coeffs."""
    total = 0
    for i, c in enumerate(coeffs):
        total = total + c * x ** i
    return total


print(evaluate_poly([1, 2, 3, 4], -1))
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>answer</summary>

It prints $-2$.

The polynomial is $4x^3 + 3x^2 + 2x + 1$. At $x = -1$, an odd power is
$-1$ and an even power is $+1$. So the value is $-4 + 3 - 2 + 1 = -2$.
At $x = -1$, the value of a polynomial is the coefficients added with
alternating signs.

</details>

**9.** How many multiplications does that function do for a polynomial
of degree 10? Can it be done with fewer?

<details class="dl-answer"><summary>answer</summary>

It does about 55 for the powers alone. By hand, each `x ** i` takes
$i$ multiplications, and $0 + 1 + 2 + \ldots + 10 = 55$.

A method called Horner's method needs only one multiplication for each
coefficient, 11 in all:

```python
def evaluate_poly(coeffs, x):
    total = 0
    for c in reversed(coeffs):
        total = total * x + c
    return total
```

It works by nesting the brackets: $3x^2 + 5x - 2 = ((3)x + 5)x - 2$.
Each step is one multiplication and one addition, and there are no
powers anywhere. It is also more accurate with floats, which is why
libraries for numerical work use it.

</details>

**10.** Here is a shorter `add_poly`. It gives the right answer for the
first call. What goes wrong with the second? What would happen if the
two lists in the second call were the other way round? Can you fix it?

```python exec
id: add-with-a-short-loop
def add_poly(a, b):
    """The sum of two polynomials, as a new coefficient list."""
    result = []
    for i in range(len(a)):
        result.append(a[i] + b[i])
    return result


print(add_poly([-2, 5, 3], [7, -3, 1]))
print(add_poly([3, 2], [-2, 5, 3]))
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too. The second
call prints `[1, 7]`. It should be `[1, 7, 3]`, which is
$3x^2 + 7x + 1$. The loop only goes as far as the end of `a`, so the
$3x^2$ is lost without any error. The other way round, `b` is the
shorter list, and `b[2]` raises an `IndexError`.

```python
def add_poly(a, b):
    """The sum of two polynomials, as a new coefficient list."""
    length = max(len(a), len(b))
    a = a + [0] * (length - len(a))
    b = b + [0] * (length - len(b))
    result = []
    for i in range(length):
        result.append(a[i] + b[i])
    return result
```

Padding both lists with zeros to the same length makes the loop safe.
A bug that gives a wrong answer with no error is harder to find than
one that stops the program.

</details>

**11.** Before you run it: how long will the list be, and what is in it?

```python exec
id: product-length
def multiply_poly(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] = result[i + j] + a[i] * b[j]
    return result


print(multiply_poly([1, 0, 0, 1], [1, 1]))
```

<details class="dl-answer"><summary>answer</summary>

It prints `[1, 1, 0, 1, 1]`, a list of 5.

The polynomials are $x^3 + 1$ and $x + 1$, of degree 3 and 1. The
product has degree $3 + 1 = 4$, so it has 5 coefficients:
$(x^3 + 1)(x + 1) = x^4 + x^3 + x + 1$. There is no $x^2$ term, so a 0
keeps its place.

</details>

**12.** Which of these are identities, true for every $x$? Which are
equations, true only for some $x$? Can you decide by expanding, and
then check by evaluating both sides at a few values?

- (a) $(x + 1)^2 = x^2 + 2x + 1$
- (b) $2x + 3 = 11$
- (c) $x(x + 2) = x^2 + 2x$
- (d) $(x - 1)(x + 1) = x^2 + 1$

```python exec
id: identity-or-equation
for x in [-2, 0, 1, 4]:
    print(x, (x - 1) * (x + 1), x ** 2 + 1)
```

<details class="dl-answer"><summary>answer</summary>

(a) and (c) are identities. (b) is an equation, true only for $x = 4$.

(d) looks like an identity, but it is not one, and it is not true for
any $x$. The left side expands to $x^2 - 1$, which is always 2 less
than $x^2 + 1$. The cell shows the gap of 2 at every $x$. An equation
can be true for many values, one value, or none.

</details>

## Verification

**13.** How can you check that your `multiply_poly` gives the product,
without calculating it by hand?

<details class="dl-answer"><summary>answer</summary>

Evaluate both sides. If $c = a \times b$ as polynomials, then
$c(x) = a(x) \times b(x)$ for every value of $x$.

```python
for x in [-3, -1, 0, 0.5, 2, 7]:
    assert abs(evaluate_poly(product, x)
               - evaluate_poly(a, x) * evaluate_poly(b, x)) < 1e-9
```

Two polynomials of degree at most $n$ that agree at $n + 1$ points are
the same polynomial. So a few test values are more than a spot check.
If you use enough of them, they are a proof.

</details>

**14.** `[1, 2, 1]` times `[1, 1]` should be `[1, 3, 3, 1]`. Can you
check this by evaluating both sides at $x = 10$?

<details class="dl-answer"><summary>answer</summary>

The left side: $1 + 2 \cdot 10 + 100 = 121$ and $1 + 10 = 11$, and
$121 \times 11 = 1331$.

The right side: $1 + 30 + 300 + 1000 = 1331$. They agree.

Evaluating at 10 has a nice side effect. The coefficients appear as the
digits of the answer, as long as none of them is 10 or more. So
$11^2 = 121$ and $11^3 = 1331$ are rows of Pascal's triangle, written as
numbers. At $11^5 = 161051$ the pattern breaks, because the
coefficients 10 carry into the next digit.

</details>

## Your world

**15.** A problem from the world you chose.

<div class="dl-world" data-world="rockets">

A second rocket is launched from 1 m up at 20 m/s, so its height is
$1 + 20t - 4.9t^2$. How much higher is it than the first rocket,
$2 + 15t - 4.9t^2$, after $t$ seconds? Subtract the two polynomials.
What kind of polynomial is the gap?

```python exec
id: your-world--rockets
first = [2, 15, -4.9]
second = [1, 20, -4.9]
```

<details class="dl-answer"><summary>answer</summary>

The gap is $-1 + 5t$, a straight line.

```python
gap = []
for i in range(3):
    gap.append(second[i] - first[i])
print(gap)
```

It prints `[-1, 5, 0.0]`. The $-4.9t^2$ terms cancel, because gravity
pulls on both rockets in
the same way. So the gap grows by 5 m every second, the difference
between their launch speeds. At $t = 0$ the second rocket is 1 m lower.
At $t = 0.2$ they are level, and after that the second is higher.

</details>

</div>

<div class="dl-world" data-world="electronics">

The 12 V supply from the tutorial makes $12I$ watts. Its own 2 ohms
turn $2I^2$ watts into heat. The power left for the circuit is the
first minus the second. Can you write both as lists and subtract them?
Is the answer the list `[0, 12, -2]`?

```python exec
id: your-world--electronics
made = [0, 12]
heat = [0, 0, 2]
```

<details class="dl-answer"><summary>answer</summary>

Yes. $12I - 2I^2$ is `[0, 12, -2]`.

```python
made = made + [0]      # 12I becomes [0, 12, 0], the same length as heat
left = []
for i in range(3):
    left.append(made[i] - heat[i])
print(left)
```

At 3 A the supply makes 36 W and turns 18 W into heat, so 18 W reach
the circuit. At 6 A it makes 72 W and all 72 W become heat.

</details>

</div>

## Applications

**16.** A rectangle measures $(x + 3)$ by $(x + 5)$. What are its area
and its perimeter?

<details class="dl-answer"><summary>answer</summary>

The area is $x^2 + 8x + 15$, and the perimeter is $4x + 16$.

We multiply to get the area, so it is quadratic. We add to get the
perimeter, so it is linear. That is why, if you double the length and
width of a room, the length of its walls doubles, but you need four
times as much carpet.

</details>

**17.** A square lawn has sides of length $x$. A path 2 m wide runs
around the outside. What is the area of the path?

<details class="dl-answer"><summary>answer</summary>

The area of the path is $(x + 4)^2 - x^2 = 8x + 16$.

The lawn and path together are $x + 4$ wide, not $x + 2$, because the
path is on both sides. Most people use $x + 2$ the first time, and that
is the point of the problem. The answer is a small surprise too. It is
linear, so the path's area does not grow quadratically with the
lawn.

</details>

**18.** Expand $(x + y)^2$, $(x - y)^2$ and $(x + y)(x - y)$. What is
each one useful for?

<details class="dl-answer"><summary>answer</summary>

They are $x^2 + 2xy + y^2$, $x^2 - 2xy + y^2$ and $x^2 - y^2$.

The third is useful for mental arithmetic:
$37 \times 43 = (40 - 3)(40 + 3) = 1600 - 9 = 1591$.

The first two appear whenever you square a distance, or a difference
from a mean. The standard deviation does exactly that.

</details>

## From earlier

**19.** Expand $(x + 1)^2$, $(x + 1)^3$ and $(x + 1)^4$. What do you notice
about the coefficients?

<details class="dl-answer"><summary>answer</summary>

They are $x^2 + 2x + 1$, then $x^3 + 3x^2 + 3x + 1$, then $x^4 + 4x^3 + 6x^2 + 4x + 1$.

The coefficients are 1 2 1, then 1 3 3 1, then 1 4 6 4 1. These are the
rows of Pascal's triangle. Each row is built by adding pairs of
neighbours from the row above: in 1 3 3 1, $1 + 3 = 4$, $3 + 3 = 6$ and
$3 + 1 = 4$ give the 4 6 4 of the next row. The same numbers count how
many ways there are to choose $k$ things from $n$. You met them there in
[Counting: factorials, permutations and combinations](tutorial:counting-carefully).

</details>

**20.** €1000 grows at 5% a year. Can you write the amount after $n$
years as a polynomial in the growth factor? What is the amount after 3
years?

<details class="dl-answer"><summary>answer</summary>

The amount is $1000(1 + r)^n$ with $r = 0.05$. After 3 years it is
$1000 \times 1.05^3 = 1157.63$ (to the nearest cent).

When we expand $(1 + r)^3 = 1 + 3r + 3r^2 + r^3$ and multiply by 1000,
we get $1000 + 150 + 7.50 + 0.125$. The first two terms are the
simple-interest answer. Everything after them is interest on interest.
For a small $r$, those later terms shrink fast. That is why
$(1 + r)^n \approx 1 + nr$ is a good approximation over a year or two,
and a bad one over thirty years.

</details>

