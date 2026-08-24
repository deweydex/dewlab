---
title: "Expressions Come Alive"
slug: expressions-come-alive
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
covers:
  expressions-versus-equations:
    covers: [MIT-1.5]
  representing-polynomials:
    covers: [MIT-1.6]
  evaluating-polynomials:
    covers: [MIT-1.6]
  displaying-polynomials:
    covers: [MIT-1.6]
  adding-polynomials:
    covers: [MIT-1.6]
  multiplying-polynomials:
    covers: [MIT-1.8]
  subtracting-and-scaling:
    covers: [MIT-1.6]
---

# Expressions Come Alive

**Programming Design Principles / Maths for IT**

Today we take on one of the most satisfying challenges in these tutorials: representing algebraic expressions as data structures and computing with them. A polynomial like $3x^2 + 5x - 2$ will become a list of numbers that our functions can evaluate, add, and multiply. The algebra becomes tangible.

## Expressions versus Equations

An important distinction first. An *expression* is a mathematical phrase that has a value: $3x + 7$, $x^2 - 4$, $\frac{x+1}{x-1}$. It does not assert anything -- it just computes something for a given value of x.

An *equation* is a statement that two expressions are equal: $3x + 7 = 22$, $x^2 - 4 = 0$. An equation asserts something and can be true or false depending on x.

We *evaluate* expressions. We *solve* equations. Today is about evaluation; solving comes in *Cracking Equations*.

## Representing Polynomials

A polynomial like $3x^2 + 5x - 2$ has a simple structure: it is a sum of terms, each being a coefficient multiplied by a power of x. We can represent it as a list of coefficients, where the position in the list indicates the power.

We will use the convention that index $i$ holds the coefficient of $x^i$. So:

$$3x^2 + 5x - 2 \quad\leftrightarrow\quad [-2, 5, 3]$$

The constant term ($-2$, coefficient of $x^0$) is at index 0, the coefficient of $x^1$ (which is 5) is at index 1, and the coefficient of $x^2$ (which is 3) is at index 2.

This convention is natural because the index matches the exponent.

```python exec
id: representing-polynomials-1
# Some polynomials as lists
constant_5 = [5]               # just the number 5
linear = [3, 2]                # 2x + 3
quadratic = [-2, 5, 3]        # 3x^2 + 5x - 2
cubic = [1, 0, -3, 2]         # 2x^3 - 3x^2 + 1

print("Constant:", constant_5)
print("Linear:", linear)
print("Quadratic:", quadratic)
print("Cubic:", cubic)
```

## Evaluating Polynomials

To evaluate $3x^2 + 5x - 2$ at $x = 4$, we compute: $3(16) + 5(4) - 2 = 48 + 20 - 2 = 66$.

In terms of our list: for each index $i$, multiply the coefficient by $x^i$ and add them all up.

$$p(x) = \sum_{i=0}^{n} c_i \cdot x^i$$

This is a direct application of sigma notation -- and it maps perfectly to a loop.

### Your turn

Write a function `evaluate_poly(coeffs, x)` that takes a list of coefficients and a value of x, and returns the polynomial's value at that point.

**Pseudocode:**
```
SET result = 0
FOR each index i from 0 to length-1:
    ADD coeffs[i] * x^i to result
RETURN result
```

```python exec
id: your-turn-1
# Your evaluate_poly function
```

```python exec
id: your-turn-2
# Test cases
# evaluate_poly([-2, 5, 3], 0) should be -2 (just the constant term)
# evaluate_poly([-2, 5, 3], 1) should be 6 (= -2 + 5 + 3)
# evaluate_poly([-2, 5, 3], 4) should be 66 (= -2 + 20 + 48)
# evaluate_poly([1], 999) should be 1 (constant polynomial)
```

## Displaying Polynomials

A list like `[-2, 5, 3]` is fine for computation but not great for reading. Let's write a function that produces a human-readable string like `"3x^2 + 5x - 2"`.

This is trickier than it looks. We need to handle:
- Zero coefficients (skip them)
- The constant term (no "x" part)
- The linear term ($x^1$ should display as just "x", not "x^1")
- Coefficient of 1 or -1 (display as "x^2" not "1x^2")
- Positive and negative signs (the first term should not start with "+")

### Your turn

Write a function `poly_to_string(coeffs)` that returns a human-readable string. Start with a simple version that works for basic cases, then refine it to handle the edge cases above.

Do not worry about making it perfect on the first try -- string formatting with many special cases is genuinely tricky. Get the basic version working first, then improve.

```python exec
id: your-turn-3
# Your poly_to_string function
# Start simple, then refine
```

```python exec
id: your-turn-4
# Test with various polynomials
# poly_to_string([-2, 5, 3]) should produce something like "3x^2 + 5x - 2"
# poly_to_string([0, 0, 1]) should produce something like "x^2"
# poly_to_string([7]) should produce "7"
# poly_to_string([0, 1]) should produce "x"
```

## Adding Polynomials

Adding two polynomials means adding corresponding coefficients:

$$(3x^2 + 5x - 2) + (x^2 - 3x + 7) = 4x^2 + 2x + 5$$

In list form: `[-2, 5, 3] + [7, -3, 1] = [5, 2, 4]`

When the polynomials have different degrees (different list lengths), the shorter one effectively has zeros in the higher positions.

### Your turn

Write a function `add_poly(a, b)` that returns a new list representing the sum. Handle different-length lists gracefully.

**Pseudocode:**
```
SET length to the longer of the two lists
CREATE result list of that length, filled with zeros
FOR each index i in result:
    IF i < length of a: ADD a[i] to result[i]
    IF i < length of b: ADD b[i] to result[i]
RETURN result
```

```python exec
id: your-turn-5
# Your add_poly function
```

```python exec
id: your-turn-6
# Test: [-2, 5, 3] + [7, -3, 1] should give [5, 2, 4]
# Also test with different-length polynomials
```

## Multiplying Polynomials

Multiplying polynomials is more involved. When we multiply $(2x + 3)(x + 4)$, we use the FOIL method (or more generally, distribute each term of the first polynomial across every term of the second):

$$(2x + 3)(x + 4) = 2x^2 + 8x + 3x + 12 = 2x^2 + 11x + 12$$

The key insight: when we multiply $c_i x^i$ by $c_j x^j$, the result is $c_i \cdot c_j \cdot x^{i+j}$. So the coefficient at position $k$ in the result is the sum of all products $a_i \cdot b_j$ where $i + j = k$.

### Your turn

Write a function `multiply_poly(a, b)` that returns a new list representing the product.

**Pseudocode:**
```
SET result_length = length(a) + length(b) - 1
CREATE result list of that length, filled with zeros
FOR each index i in a:
    FOR each index j in b:
        ADD a[i] * b[j] to result[i + j]
RETURN result
```

```python exec
id: your-turn-7
# Your multiply_poly function
```

```python exec
id: your-turn-8
# Test: multiply_poly([3, 2], [4, 1]) should give [12, 11, 2]
# That's (2x + 3)(x + 4) = 2x^2 + 11x + 12
# In our convention: [12, 11, 2]

# Also verify: multiply_poly([1, 1], [1, 1]) should give [1, 2, 1]
# That's (x + 1)(x + 1) = x^2 + 2x + 1
```

### A verification trick

We can verify polynomial multiplication by evaluating both sides at a specific value of x. If $(2x + 3)(x + 4) = 2x^2 + 11x + 12$, then both sides should give the same value for any x:

```python exec
id: a-verification-trick-1
# Verification by evaluation
a = [3, 2]     # 2x + 3
b = [4, 1]     # x + 4
product = multiply_poly(a, b)

x = 5
left_side = evaluate_poly(a, x) * evaluate_poly(b, x)
right_side = evaluate_poly(product, x)
print("(2*5+3) * (5+4) =", left_side)
print("2*25 + 11*5 + 12 =", right_side)
print("Match:", left_side == right_side)
```

This is a powerful testing technique: use a known mathematical property to verify your code. If `evaluate_poly(multiply_poly(a, b), x)` equals `evaluate_poly(a, x) * evaluate_poly(b, x)` for several values of x, your multiplication is almost certainly correct.

### Your turn

Write a function `test_multiply(a, b)` that automatically verifies the multiplication by checking the evaluation at x = 0, 1, 2, -1, and 10. Print PASS or FAIL for each.

```python exec
id: your-turn-9
# Your test_multiply function
```

```python exec
id: your-turn-10
# Test it on several polynomial pairs
```

## Subtracting and Scaling

Two more operations before we finish: subtracting polynomials and multiplying by a constant (scaling).

### Your turn

Write `subtract_poly(a, b)` and `scale_poly(coeffs, scalar)`. Think about how each relates to what you have already built.

```python exec
id: your-turn-11
# Your subtract_poly and scale_poly functions
```

```python exec
id: your-turn-12
# Test them
```

## Reflection

We have built the core of a polynomial algebra system: representation, evaluation, display, addition, subtraction, multiplication, and scaling. Each function is small, testable, and builds on the others.

The deeper lesson is about *representation*. By choosing to represent polynomials as lists, we turned abstract algebra into concrete data manipulation. Addition became adding list elements. Multiplication became a nested loop. The algebra did not change -- our perspective on it did.

Next time we will use this machinery to solve equations and factor polynomials.

What was the trickiest part of this tutorial? The `poly_to_string` formatting, or the `multiply_poly` algorithm?

## Where to Read More

Khan Academy. *Adding and Subtracting Polynomials.*
<https://www.youtube.com/watch?v=ZGl2ExHwdak>. The same coefficient-by-
coefficient operation this page builds as `add_poly`, worked by hand
first.

Khan Academy. *Multiplying Polynomials Example.*
<https://www.youtube.com/watch?v=yJzLYa-_Y1k>. The FOIL method this page
turns into a nested loop over coefficients.
