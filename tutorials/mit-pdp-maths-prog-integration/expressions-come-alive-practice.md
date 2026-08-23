---
title: "Expressions Come Alive — Practice"
slug: expressions-come-alive-practice
practice_for: expressions-come-alive
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Expressions Come Alive — Practice

Answers are folded. Expand by hand first and use the cell to check — the point of the checking cell is to settle disputes, not to do the work.

The expansion problems are adapted from the FOIL worksheet in the Mathematics repository.

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

**1.** Expand each.

- (a) $(t + 2)(t + 5)$
- (b) $(p + 6)(p + 3)$
- (c) $(m + 4)(m + 7)$
- (d) $(k + 8)(k + 2)$

<details class="dl-answer"><summary>answer</summary>

(a) $t^2 + 7t + 10$. (b) $p^2 + 9p + 18$. (c) $m^2 + 11m + 28$. (d) $k^2 + 10k + 16$.

In every one, the middle number is the sum of the two constants and the last is their product. That is not a coincidence and it is what makes factorising possible.

</details>

**2.** Expand $(n + 5)(n + 5)$ and $(w + 3)(w + 3)$. What is the general rule?

<details class="dl-answer"><summary>answer</summary>

$n^2 + 10n + 25$ and $w^2 + 6w + 9$.

$(x + a)^2 = x^2 + 2ax + a^2$. The middle term is *twice* the constant, because it appears from both the outer and the inner product.

</details>

**3.** Is $(a + b)^2$ the same as $a^2 + b^2$?

<details class="dl-answer"><summary>answer</summary>

No, and this is the single most common mistake in algebra.

$(a + b)^2 = a^2 + 2ab + b^2$. Try it with numbers: $(3 + 4)^2 = 49$, while $3^2 + 4^2 = 25$. The missing 24 is the $2ab$.

Squaring does not distribute over addition. Neither does the square root: $\sqrt{9 + 16}$ is 5, not 7.

</details>

**4.** Expand with the negatives.

- (a) $(x - 3)(x + 5)$
- (b) $(x - 4)(x - 6)$
- (c) $(x + 7)(x - 7)$
- (d) $(x - 5)^2$

<details class="dl-answer"><summary>answer</summary>

(a) $x^2 + 2x - 15$. (b) $x^2 - 10x + 24$. (c) $x^2 - 49$. (d) $x^2 - 10x + 25$.

(c) is the difference of two squares — the middle terms cancel exactly, and it is worth recognising instantly in both directions.

</details>

**5.** Expand with coefficients.

- (a) $(2x + 3)(x + 4)$
- (b) $(3x - 1)(2x + 5)$
- (c) $(5x + 2)^2$

<details class="dl-answer"><summary>answer</summary>

(a) $2x^2 + 11x + 12$. (b) $6x^2 + 13x - 5$. (c) $25x^2 + 20x + 4$.

</details>

**6.** Expand $(x + 1)^2$, $(x + 1)^3$, $(x + 1)^4$. What are the coefficients?

<details class="dl-answer"><summary>answer</summary>

$x^2 + 2x + 1$, then $x^3 + 3x^2 + 3x + 1$, then $x^4 + 4x^3 + 6x^2 + 4x + 1$.

1 2 1, then 1 3 3 1, then 1 4 6 4 1 — Pascal's triangle. Each row is built by adding neighbouring pairs from the row above, and the same numbers count how many ways there are to choose k things from n, which is why *Counting Carefully* meets them again.

</details>

**7.** Expand $(x + 2)(x^2 + 3x + 1)$.

<details class="dl-answer"><summary>answer</summary>

$x^3 + 5x^2 + 7x + 2$.

FOIL only names the four products of two binomials. The actual rule is that every term multiplies every term — six products here — and that generalises where FOIL does not.

</details>

## Polynomials as Lists

**8.** Write these as coefficient lists, constant first.

- (a) $3x^2 + 5x - 2$
- (b) $2x^3 - 3x^2 + 1$
- (c) $7$
- (d) $x^5$

<details class="dl-answer"><summary>answer</summary>

(a) `[-2, 5, 3]`. (b) `[1, 0, -3, 2]`. (c) `[7]`. (d) `[0, 0, 0, 0, 0, 1]`.

The zeros in (b) and (d) are not padding — index i holds the coefficient of x^i, so a missing power is a zero coefficient and the position has to be kept.

</details>

**9.** Write `evaluate_poly(coeffs, x)`.

<details class="dl-answer"><summary>answer</summary>

```python
def evaluate_poly(coeffs, x):
    """The value of the polynomial at x."""
    total = 0
    for i, c in enumerate(coeffs):
        total = total + c * x ** i
    return total
```

`evaluate_poly([-2, 5, 3], 4)` is 66, and at x = 0 it is −2, which is a free test: a polynomial at zero is always its constant term.

</details>

**10.** How many multiplications does that do for a degree-10 polynomial? Can it be done in fewer?

<details class="dl-answer"><summary>answer</summary>

About 55, because `x ** i` costs i multiplications and those add up.

Horner's method does it in 10:

```python
def evaluate_poly(coeffs, x):
    total = 0
    for c in reversed(coeffs):
        total = total * x + c
    return total
```

It works by nesting: $3x^2 + 5x - 2 = ((3)x + 5)x - 2$. Each step is one multiply and one add, and there is no power operation anywhere. It is also more accurate in floating point, which is why numerical libraries use it.

</details>

**11.** Write `add_poly(a, b)`, handling lists of different lengths.

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

The different lengths are the whole problem, and treating a missing coefficient as 0 is exactly right — a polynomial of lower degree *does* have zero coefficients up there.

</details>

**12.** Write `multiply_poly(a, b)`. What is the degree of the result?

<details class="dl-answer"><summary>answer</summary>

```python
def multiply_poly(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            result[i + j] += ca * cb
    return result
```

The degree is the sum of the two degrees, so the list length is `len(a) + len(b) - 1`.

`result[i + j]` is the line worth staring at: multiplying $x^i$ by $x^j$ gives $x^{i+j}$, so the exponents add and the indices add with them. The list representation was chosen so that this would be true.

</details>

**13.** Write `poly_to_string(coeffs)` producing something a person would write.

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

Six edge cases in one function: zero coefficients, the constant term, x¹, coefficients of 1 and −1, the leading sign, and the zero polynomial. Testing it is more work than writing it, which is a fair description of most formatting code.

</details>

## Verification

**14.** How can you check that your `multiply_poly` is right, without checking by hand?

<details class="dl-answer"><summary>answer</summary>

Evaluate. If $c = a \times b$ as polynomials, then $c(x) = a(x) \times b(x)$ for *every* x.

```python
for x in [-3, -1, 0, 0.5, 2, 7]:
    assert abs(evaluate_poly(product, x)
               - evaluate_poly(a, x) * evaluate_poly(b, x)) < 1e-9
```

Two polynomials of degree n that agree at n + 1 points are the same polynomial, so a handful of test values is not a spot check — it is a proof, as long as you use enough of them.

</details>

**15.** `[1, 2, 1]` times `[1, 1]` should be `[1, 3, 3, 1]`. Verify by evaluating both at x = 10.

<details class="dl-answer"><summary>answer</summary>

$(1 + 2 \cdot 10 + 100) = 121$ and $(1 + 10) = 11$; $121 \times 11 = 1331$.

The product at 10 is $1 + 30 + 300 + 1000 = 1331$. They agree.

Evaluating at 10 has a pleasant side effect: the coefficients appear as the digits, as long as none of them reaches 10. $11^2 = 121$ and $11^3 = 1331$ are Pascal's triangle in disguise, and $11^5 = 161051$ is where the carrying starts and the disguise fails.

</details>

## Applications

**16.** A rectangle is $(x + 3)$ by $(x + 5)$. Write its area, and its perimeter.

<details class="dl-answer"><summary>answer</summary>

Area $x^2 + 8x + 15$, perimeter $4x + 16$.

Area multiplies and grows quadratically; perimeter adds and grows linearly. That difference is why doubling a room's dimensions doubles the skirting board and quadruples the carpet.

</details>

**17.** A square lawn of side $x$ has a 2 m path around the outside. Write the path's area.

<details class="dl-answer"><summary>answer</summary>

$(x + 4)^2 - x^2 = 8x + 16$.

The path is 4 m wider than the lawn, not 2 — the border is on both sides. Getting that wrong is the point of the problem, and the linear answer is a small surprise: the path's area does not grow quadratically with the lawn.

</details>

**18.** €1000 grows at 5% a year. Write the amount after n years as a polynomial in the growth factor, and find the amount after 3 years.

<details class="dl-answer"><summary>answer</summary>

$1000(1 + r)^n$ with $r = 0.05$, so $1000 \times 1.05^3 = 1157.63$.

Expanding $(1 + r)^3 = 1 + 3r + 3r^2 + r^3$ gives 1000 + 150 + 7.50 + 0.125. The first two terms are the simple-interest answer; everything after is interest on interest, and for small r the later terms shrink fast. That is why $(1 + r)^n \approx 1 + nr$ is a decent approximation for one year and a bad one for thirty.

</details>

**19.** Expand $(x + y)^2$, $(x - y)^2$ and $(x + y)(x - y)$, and say what each is useful for.

<details class="dl-answer"><summary>answer</summary>

$x^2 + 2xy + y^2$, $x^2 - 2xy + y^2$, and $x^2 - y^2$.

The third is the useful one for mental arithmetic: $37 \times 43$ is $(40 - 3)(40 + 3) = 1600 - 9 = 1591$.

The first two are the ones that turn up when you square a distance or a difference from a mean, which is exactly what the standard deviation does.

</details>
