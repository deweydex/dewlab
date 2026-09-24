---
title: "Polynomials: representing and combining them in Python — Practice"
practice_for: expressions-come-alive
year: "2026-2027"
version: 2026.08.23.1
---

# Polynomials: representing and combining them in Python — Practice

The answers are hidden in folds under each problem. Try each expansion
by hand first. Then use the cell to check your answer. The cell is there
to settle a doubt, not to do the work for you.

The expansion problems are adapted from the FOIL worksheet in the
Mathematics repository.

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
$2 + 5 = 7$ and $2 \times 5 = 10$. This is not a coincidence. It is what
makes factorising possible: going backwards from the expanded form to
the brackets. You will do that in
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).

</details>

**2.** Expand $(n + 5)(n + 5)$ and $(w + 3)(w + 3)$. Can you see a
general rule?

<details class="dl-answer"><summary>answer</summary>

$n^2 + 10n + 25$ and $w^2 + 6w + 9$.

The rule is $(x + a)^2 = x^2 + 2ax + a^2$. The middle coefficient is
twice the constant, because the $ax$ term appears twice: once from the
Outer product and once from the Inner product.

</details>

**3.** Is $(a + b)^2$ the same as $a^2 + b^2$?

<details class="dl-answer"><summary>answer</summary>

No. This is the most common mistake in algebra, so do not worry if you
thought yes.

$(a + b)^2 = a^2 + 2ab + b^2$. Try it with numbers: $(3 + 4)^2 = 49$,
but $3^2 + 4^2 = 25$. The missing 24 is the $2ab$ term:
$2 \times 3 \times 4 = 24$.

We cannot square each part of a sum separately. The same is true for
square roots: $\sqrt{9 + 16} = \sqrt{25} = 5$, not $3 + 4 = 7$.

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

**6.** Expand $(x + 1)^2$, $(x + 1)^3$ and $(x + 1)^4$. What do you notice
about the coefficients?

<details class="dl-answer"><summary>answer</summary>

$x^2 + 2x + 1$, then $x^3 + 3x^2 + 3x + 1$, then $x^4 + 4x^3 + 6x^2 + 4x + 1$.

The coefficients are 1 2 1, then 1 3 3 1, then 1 4 6 4 1. These are the
rows of Pascal's triangle. Each row is built by adding pairs of
neighbours from the row above: in 1 3 3 1, $1 + 3 = 4$, $3 + 3 = 6$ and
$3 + 1 = 4$ give the 4 6 4 of the next row. The same numbers count how
many ways there are to choose $k$ things from $n$. You met them there in
[Counting: factorials, permutations and combinations](tutorial:counting-carefully).

</details>

**7.** Expand $(x + 2)(x^2 + 3x + 1)$.

<details class="dl-answer"><summary>answer</summary>

$x^3 + 5x^2 + 7x + 2$.

A *binomial* is a polynomial with two terms, such as $x + 2$. FOIL only
names the four products you get from two binomials. The real rule is
that every term multiplies every term. Here that gives six products,
since $2 \times 3 = 6$. That rule works for any polynomials, where FOIL
does not.

</details>

## Polynomials as lists

**8.** Write each one as a coefficient list, with the constant first.

- (a) $3x^2 + 5x - 2$
- (b) $2x^3 - 3x^2 + 1$
- (c) $7$
- (d) $x^5$

<details class="dl-answer"><summary>answer</summary>

(a) `[-2, 5, 3]`. (b) `[1, 0, -3, 2]`. (c) `[7]`. (d) `[0, 0, 0, 0, 0, 1]`.

Index $i$ holds the coefficient of $x^i$. So a missing power has a
coefficient of zero, and in (b) and (d) its place must stay in the list.
Those zeros carry meaning: they say "no term with this power".

</details>

**9.** Can you write `evaluate_poly(coeffs, x)`?

<details class="dl-answer"><summary>answer</summary>

```python
def evaluate_poly(coeffs, x):
    """The value of the polynomial at x."""
    total = 0
    for i, c in enumerate(coeffs):
        total = total + c * x ** i
    return total
```

`evaluate_poly([-2, 5, 3], 4)` is 66. At $x = 0$ it is −2. That gives
you an easy test: at zero, a polynomial always equals its constant term.

</details>

**10.** How many multiplications does that function do for a polynomial
of degree 10? Can it be done with fewer?

<details class="dl-answer"><summary>answer</summary>

About 55 for the powers alone. Working out `x ** i` by hand takes $i$
multiplications, and $0 + 1 + 2 + \ldots + 10 = 55$.

A method called Horner's method does it with 10:

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

**11.** Can you write `add_poly(a, b)` so that it works for lists of
different lengths?

<details class="dl-answer"><summary>answer</summary>

```python
def add_poly(a, b):
    """Add two polynomials given as coefficient lists."""
    length = max(len(a), len(b))
    result = []
    for i in range(length):
        left = a[i] if i < len(a) else 0
        right = b[i] if i < len(b) else 0
        result.append(left + right)
    return result
```

The different lengths are the hard part. Treating a missing coefficient
as 0 is exactly right, because a polynomial of lower degree does have
zero coefficients for the higher powers.

</details>

**12.** Can you write `multiply_poly(a, b)`? What is the degree of the result?

<details class="dl-answer"><summary>answer</summary>

```python
def multiply_poly(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            result[i + j] += ca * cb
    return result
```

The degree of the result is the sum of the two degrees. So the list
length is `len(a) + len(b) - 1`.

The line worth looking at closely is `result[i + j]`. Multiplying $x^i$
by $x^j$ gives $x^{i+j}$, so the exponents add, and the indexes add with
them. We chose the list representation so that this would be true.

</details>

**13.** Can you write `poly_to_string(coeffs)` so that it gives the form a
person would write?

<details class="dl-answer"><summary>answer</summary>

```python
def poly_to_string(coeffs):
    """A readable form of a polynomial coefficient list."""
    parts = []
    for power in range(len(coeffs) - 1, -1, -1):
        c = coeffs[power]
        if c == 0:
            continue
        if power == 0:
            piece = str(abs(c))
        else:
            variable = "x" if power == 1 else f"x^{power}"
            piece = variable if abs(c) == 1 else f"{abs(c)}{variable}"
        sign = "-" if c < 0 else "+"
        parts.append((sign, piece))
    if not parts:
        return "0"
    first_sign, first = parts[0]
    out = ("-" if first_sign == "-" else "") + first
    for sign, piece in parts[1:]:
        out += f" {sign} {piece}"
    return out
```

`[-2, 5, 3]` gives `3x^2 + 5x - 2`.

This one function handles six special cases:

1. zero coefficients
2. the constant term
3. the $x^1$ term
4. coefficients of 1 and −1
5. the sign of the first term
6. the zero polynomial, which prints as `0`

Testing it is more work than writing it. That is true of most
formatting code.

</details>

## Verification

**14.** How can you check that your `multiply_poly` is right, without
working it out by hand?

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

**15.** `[1, 2, 1]` times `[1, 1]` should be `[1, 3, 3, 1]`. Can you
check this by evaluating both sides at $x = 10$?

<details class="dl-answer"><summary>answer</summary>

The left side: $1 + 2 \cdot 10 + 100 = 121$ and $1 + 10 = 11$, and
$121 \times 11 = 1331$.

The right side: $1 + 30 + 300 + 1000 = 1331$. They agree.

Evaluating at 10 has a nice side effect. The coefficients appear as the
digits of the answer, as long as none of them is 10 or more. So
$11^2 = 121$ and $11^3 = 1331$ are rows of Pascal's triangle in
disguise. At $11^5 = 161051$ the pattern breaks, because the
coefficients 10 carry into the next digit.

</details>

## Applications

**16.** A rectangle measures $(x + 3)$ by $(x + 5)$. What are its area
and its perimeter?

<details class="dl-answer"><summary>answer</summary>

The area is $x^2 + 8x + 15$, and the perimeter is $4x + 16$.

The area comes from multiplying, so it is quadratic. The perimeter comes
from adding, so it is linear. That is why, if you double the length and
width of a room, the length of its walls doubles, but you need four
times as much carpet.

</details>

**17.** A square lawn has sides of length $x$. A path 2 m wide runs
around the outside. What is the area of the path?

<details class="dl-answer"><summary>answer</summary>

$(x + 4)^2 - x^2 = 8x + 16$.

The lawn and path together are $x + 4$ wide, not $x + 2$, because the
path is on both sides. Most people get this wrong the first time, and
that is the point of the problem. The answer is a small surprise too: it
is linear, so the path's area does not grow quadratically with the
lawn.

</details>

**18.** €1000 grows at 5% a year. Can you write the amount after $n$
years as a polynomial in the growth factor? What is the amount after 3
years?

<details class="dl-answer"><summary>answer</summary>

The amount is $1000(1 + r)^n$ with $r = 0.05$. After 3 years it is
$1000 \times 1.05^3 = 1157.63$ (to the nearest cent).

Expanding $(1 + r)^3 = 1 + 3r + 3r^2 + r^3$ and multiplying by 1000
gives $1000 + 150 + 7.50 + 0.125$. The first two terms are the
simple-interest answer. Everything after them is interest on interest.
For a small $r$, those later terms shrink fast. That is why
$(1 + r)^n \approx 1 + nr$ is a good approximation over a year or two,
and a bad one over thirty years.

</details>

**19.** Expand $(x + y)^2$, $(x - y)^2$ and $(x + y)(x - y)$. What is
each one useful for?

<details class="dl-answer"><summary>answer</summary>

$x^2 + 2xy + y^2$, $x^2 - 2xy + y^2$, and $x^2 - y^2$.

The third is useful for mental arithmetic:
$37 \times 43 = (40 - 3)(40 + 3) = 1600 - 9 = 1591$.

The first two turn up whenever you square a distance, or a difference
from a mean. The standard deviation does exactly that.

</details>
