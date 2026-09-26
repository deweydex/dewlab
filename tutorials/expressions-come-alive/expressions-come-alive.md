---
title: "Polynomials: representing and combining them in Python"
year: "2026-2027"
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

# Polynomials: representing and combining them in Python

Can a computer do algebra? On this page we find out. We take an
expression like $3x^2 + 5x - 2$ and store it as a list of numbers. Then
we write functions that work out its value, add two of them together,
and multiply them. The algebra turns into something we can hold, run and
test.

On this page we:

- see how an expression is different from an equation
- store a polynomial as a list of numbers
- work out a polynomial's value, and print it in a readable way
- add, multiply, subtract and scale polynomials, and test our work

## Expressions versus equations

An *expression* is a piece of mathematics that has a value, such as
$3x + 7$, $x^2 - 4$ or $\frac{x+1}{x-1}$. An expression does not claim
anything. It gives a value once we choose a value for $x$. For example,
when $x = 5$, the expression $3x + 7$ has the value 22.

An *equation* is a statement that two expressions are equal, such as
$3x + 7 = 22$ or $x^2 - 4 = 0$. An equation makes a claim, and the claim
can be true or false, depending on $x$. The equation $3x + 7 = 22$ is
true when $x = 5$, and false for every other value of $x$.

| | Expression | Equation |
|---|---|---|
| Example | $3x + 7$ | $3x + 7 = 22$ |
| Has an equals sign? | no | yes |
| What we do with it | *evaluate* it: work out its value | *solve* it: find the $x$ that makes it true |

This page is about evaluating. Solving comes in
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).

## Representing polynomials

A *polynomial* is an expression made by adding up terms. A *term* is a
number multiplied by a whole-number power of $x$, such as $3x^2$ or
$5x$. The number in front of the power is the term's *coefficient*.

In $3x^2 + 5x - 2$ there are three terms:

| Term | Coefficient | Power of $x$ |
|---|---|---|
| $3x^2$ | 3 | $x^2$ |
| $5x$ | 5 | $x^1$ |
| $-2$ | $-2$ | $x^0$ |

The last term, $-2$, has no $x$ in it. It is called the *constant term*.
We can still think of it as $-2 \times x^0$, because $x^0 = 1$ (you saw
this in [Number types, powers and logarithms](tutorial:numbers-and-their-families)).

The *degree* of a polynomial is the highest power of $x$ in it. So
$3x^2 + 5x - 2$ has degree 2. Some degrees have their own names: degree
0 is a constant, degree 1 is *linear*, degree 2 is *quadratic*, and
degree 3 is *cubic*.

So a polynomial is really a list of coefficients, one for each power of
$x$. We can store it as a Python list. We will use this rule: the item
at index $i$ is the coefficient of $x^i$. So:

$$3x^2 + 5x - 2 \quad\leftrightarrow\quad [-2, 5, 3]$$

- The constant term, $-2$ (the coefficient of $x^0$), is at index 0.
- The coefficient of $x^1$, which is 5, is at index 1.
- The coefficient of $x^2$, which is 3, is at index 2.

This rule is easy to remember, because the index matches the exponent.
It does mean the list is in the opposite order to the way we usually
write the polynomial. Look at the cubic in the cell below before you run
it. Can you see why its list has a 0 in it?

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

The cubic $2x^3 - 3x^2 + 1$ has no $x$ term. Its coefficient of $x^1$ is
0, and the list must still keep a place for it.

## Evaluating polynomials

To *evaluate* a polynomial means to work out its value for one chosen
value of $x$. For $3x^2 + 5x - 2$ at $x = 4$:

$$3(16) + 5(4) - 2 = 48 + 20 - 2 = 66$$

With our list, the steps are: for each index $i$, multiply the
coefficient by $x^i$, and then add up all the results. In sigma
notation, which you met in
[Repeating steps with loops](tutorial:repeating-yourself), that is:

$$p(x) = \sum_{i=0}^{n} c_i \cdot x^i$$

Here $c_i$ is the coefficient at index $i$, and $n$ is the degree. A sum
like this turns straight into a loop.

### Your turn

How would you write a function `evaluate_poly(coeffs, x)`? It takes a
list of coefficients and a value of $x$, and returns the polynomial's
value at that $x$.

**Pseudocode:**
```
SET result = 0
FOR each index i from 0 to length-1:
    ADD coeffs[i] * x^i to result
RETURN result
```

1. Write `evaluate_poly` in the first cell.
2. Test it in the second cell with the four cases in the comments.

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

## Displaying polynomials

A list like `[-2, 5, 3]` is good for computing, but it is hard for a
person to read. Can we write a function that turns it into a string like
`"3x^2 + 5x - 2"`?

This is trickier than it looks. Here are the cases to handle:

- A coefficient of zero: skip that term.
- The constant term: it has no "x" part.
- The $x^1$ term: show it as "x", not "x^1".
- A coefficient of 1 or −1: show "x^2", not "1x^2".
- Plus and minus signs: the first term should not start with "+".

### Your turn

How might you write a function `poly_to_string(coeffs)` that returns a
readable string?

1. Start with a simple version that works for basic cases.
2. Then improve it, one case from the list above at a time.

Many special cases make string formatting tricky, so do not expect it to
be perfect on the first try. Get the simple version working first.

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

## Adding polynomials

To add two polynomials, we add the coefficients of the same power of
$x$:

$$(3x^2 + 5x - 2) + (x^2 - 3x + 7) = 4x^2 + 2x + 5$$

In list form, we add the items at the same index:
`[-2, 5, 3]` and `[7, -3, 1]` give `[5, 2, 4]`.

Sometimes the two polynomials have different degrees, so their lists
have different lengths. In that case, we treat the shorter list as if it
had zeros in the missing places. For example, $2x + 3$ is `[3, 2]`, and
we treat it as `[3, 2, 0]`.

### Your turn

Can you write a function `add_poly(a, b)`? It should return a new list
for the sum, and it should work when the lists have different lengths.

**Pseudocode:**
```
SET length to the longer of the two lists
CREATE result list of that length, filled with zeros
FOR each index i in result:
    IF i < length of a: ADD a[i] to result[i]
    IF i < length of b: ADD b[i] to result[i]
RETURN result
```

1. Write `add_poly` in the first cell.
2. Test it with the example in the comment.
3. Test it again with two polynomials of different lengths.

```python exec
id: your-turn-5
# Your add_poly function
```

```python exec
id: your-turn-6
# Test: [-2, 5, 3] + [7, -3, 1] should give [5, 2, 4]
# Also test with different-length polynomials
```

## Multiplying polynomials

Multiplying polynomials takes more steps. To multiply $(2x + 3)(x + 4)$,
we multiply each term of the first polynomial by every term of the
second, and then add the results. This is called *expanding the
brackets*. For two terms times two terms, many people use the *FOIL
method*: multiply the First terms, then the Outer, then the Inner, then
the Last.

$$(2x + 3)(x + 4) = 2x^2 + 8x + 3x + 12 = 2x^2 + 11x + 12$$

Here is the idea that turns this into code. When we multiply a term
$a_i x^i$ by a term $b_j x^j$, we get $a_i \cdot b_j \cdot x^{i+j}$: the
coefficients multiply and the powers add. For example,
$2x \times 4 = 2x^1 \times 4x^0 = 8x^1$.

So in the answer, the coefficient of $x^k$ is the sum of all the
products $a_i \cdot b_j$ where $i + j = k$.

### Your turn

How might you write a function `multiply_poly(a, b)` that returns a new
list for the product?

**Pseudocode:**
```
SET result_length = length(a) + length(b) - 1
CREATE result list of that length, filled with zeros
FOR each index i in a:
    FOR each index j in b:
        ADD a[i] * b[j] to result[i + j]
RETURN result
```

1. Write `multiply_poly` in the first cell.
2. Test it with the two examples in the comments.

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

How can we be sure that `multiply_poly` is right? Here is one way. If
$(2x + 3)(x + 4) = 2x^2 + 11x + 12$, then both sides must give the same
value for every $x$. So we can pick a value, such as $x = 5$, and
evaluate both sides.

This cell uses your `evaluate_poly` and `multiply_poly`, so run it after
you have written both. Do you expect the last line to say `True`? Run it
to check.

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

Both sides give 117. This is a strong way to test code: use a
mathematical fact that must hold, and check that your code agrees with
it. Suppose `evaluate_poly(multiply_poly(a, b), x)` equals
`evaluate_poly(a, x) * evaluate_poly(b, x)` for several values of $x$.
Then your multiplication is almost certainly correct.

### Your turn

Can you write a function `test_multiply(a, b)` that does this check for
you?

1. Evaluate both sides at $x$ = 0, 1, 2, −1 and 10.
2. Print both sides for each value of $x$. Where, if anywhere, do they
   differ?
3. Try it on several pairs of polynomials in the second cell.

```python exec
id: your-turn-9
# Your test_multiply function
```

```python exec
id: your-turn-10
# Test it on several polynomial pairs
```

## Subtracting and scaling

Two more operations finish our set. One is subtracting two polynomials.
The other is *scaling*: multiplying every coefficient by the same
number. For example, $2 \times (3x^2 + 5x - 2) = 6x^2 + 10x - 4$, so
scaling `[-2, 5, 3]` by 2 gives `[-4, 10, 6]`.

### Your turn

1. Write `subtract_poly(a, b)`. How is it related to `add_poly`?
2. Write `scale_poly(coeffs, scalar)`. Could `subtract_poly` use it?
3. Test both in the second cell.

If you want to go further, try a `poly_derivative(coeffs)` function too.
Differentiating a polynomial follows its own short rule about
coefficients and exponents. You will meet that rule properly in
[Derivatives: the rate of change of a curve](tutorial:rates-of-change).

```python exec
id: your-turn-11
# Your subtract_poly and scale_poly functions
```

```python exec
id: your-turn-12
# Test them
```

## Reflection

We have built the core of a small algebra system for polynomials. It can
store a polynomial, evaluate it, display it, and add, subtract, multiply
and scale polynomials. Each function is small and testable, and each one
builds on the others.

The deeper lesson is about *representation*: the way we choose to store
something as data. We chose to store polynomials as lists, and that
turned abstract algebra into work with lists. Adding became adding list
items. Multiplying became a loop inside a loop. The algebra did not
change. Our way of looking at it did.

Next, in
[Rearranging formulae: changing the subject](tutorial:rearranging-formulae),
we move from evaluating a formula to rearranging it. After that, in
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations),
we solve equations and factorise polynomials.

What was the trickiest part of this page for you: the formatting in
`poly_to_string`, or the loops in `multiply_poly`?

## Where to Read More

Khan Academy. *Adding and Subtracting Polynomials.*
<https://www.youtube.com/watch?v=ZGl2ExHwdak>. The same coefficient-by-
coefficient operation this page builds as `add_poly`, worked by hand
first.

Khan Academy. *Multiplying Polynomials Example.*
<https://www.youtube.com/watch?v=yJzLYa-_Y1k>. The FOIL method this page
turns into a nested loop over coefficients.

Stand-up Maths (2023). *Beware the Runge Spikes!*
<https://www.youtube.com/watch?v=F_43oTnTXiw>. Draw a polynomial through a
few points and it behaves. Add more points and it can swing wildly between
them. Matt Parker shows why. About seventeen minutes.
