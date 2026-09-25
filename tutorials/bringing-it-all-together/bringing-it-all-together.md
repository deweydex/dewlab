---
title: "Review problems: polynomials, equations and sets"
year: "2026-2027"
version: 2026.09.25.1
covers:
  problem-1-the-polynomial-workshop:
    touches: [MIT-1.6, MIT-1.8]
  problem-2-where-do-they-meet:
    touches: [MIT-1.12]
  problem-3-sets-of-solutions:
    touches: [MIT-2.2]
  problem-4-building-and-verifying:
    covers: [PDP-LO10]
---

# Review problems: polynomials, equations and sets

This page has no new material. Instead, we combine tools that we built
in three earlier tutorials:

- [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
- [Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
- [Sets: building them from sorted lists](tutorial:sets-as-sorted-lists)

Each problem below needs more than one of those tools. As we work, we
also look at how the maths ideas connect to each other, and to
programming.

## The toolkit so far

The problems below use these functions. You wrote each of them in a
"Your turn" cell on one of those pages.

| Tutorial | Functions the problems use |
|---|---|
| [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive) | `evaluate_poly`, `poly_to_string`, `add_poly`, `subtract_poly`, `multiply_poly` |
| [Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations) | `solve_linear`, `solve_quadratic` |
| [Sets: building them from sorted lists](tutorial:sets-as-sorted-lists) | `make_set`, `union`, `intersection` |

Your own versions are on other pages, and some of them may not be
finished. So the four cells below hold working versions of all of
them. Run all four before you start.

If you would rather, delete the body of any function and write it again
from memory. Writing a function again from memory is often the best
test of whether you understand it.

Two ways of writing numbers meet on this page. A polynomial is a list
with the constant first, as on the polynomials page, so `[3, -4, 1]` is
$x^2 - 4x + 3$. The solvers take the numbers in the order they appear in
the equation, starting with $a$, as on the equations page. So to solve
`p = [3, -4, 1]`, the call is `solve_quadratic(1, -4, 3)`, which is
`solve_quadratic(p[2], p[1], p[0])`.

```python exec
id: the-toolkit-so-far-1
# Polynomials: a list of coefficients, constant first.
def trim(coeffs):
    """Drop zeros from the high end, so the last number is the leading one."""
    coeffs = list(coeffs)
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs


def evaluate_poly(coeffs, x):
    total = 0
    for power, coefficient in enumerate(coeffs):
        total = total + coefficient * x ** power
    return total


def add_poly(p, q):
    length = max(len(p), len(q))
    p = p + [0] * (length - len(p))
    q = q + [0] * (length - len(q))
    return trim([p[i] + q[i] for i in range(length)])


def subtract_poly(p, q):
    return add_poly(p, [-coefficient for coefficient in q])


def multiply_poly(p, q):
    result = [0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            result[i + j] += p[i] * q[j]
    return trim(result)


print(subtract_poly([0, 0, 1], [3, 2]))
print(multiply_poly([-1, 1], [-3, 1]))
```

```python exec
id: the-toolkit-so-far-2
def poly_to_string(coeffs):
    """[3, -4, 1] becomes "x^2 - 4x + 3"."""
    text = ""
    for power in range(len(coeffs) - 1, -1, -1):
        coefficient = coeffs[power]
        if coefficient == 0:
            continue
        sign = " - " if coefficient < 0 else " + "
        size = f"{abs(coefficient):g}"
        if power == 0:
            term = size
        else:
            if size == "1":
                size = ""
            term = size + ("x" if power == 1 else f"x^{power}")
        text = text + sign + term
    if text == "":
        return "0"
    if text.startswith(" - "):
        return "-" + text[3:]
    return text[3:]


print(poly_to_string([3, -4, 1]))
print(poly_to_string([-10, 3, 1]))
print(poly_to_string([0, -1]))
```

```python exec
id: the-toolkit-so-far-3
import math


def solve_linear(a, b):
    """The solution of ax + b = 0, or None if there is not exactly one."""
    if a == 0:
        return None
    return -b / a


def solve_quadratic(a, b, c):
    """The real roots of ax^2 + bx + c = 0, as a list, smallest first."""
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return []
    if discriminant == 0:
        return [-b / (2 * a)]
    root = math.sqrt(discriminant)
    return sorted([(-b - root) / (2 * a), (-b + root) / (2 * a)])


print(solve_linear(2, 3))
print(solve_quadratic(1, -4, 3))
```

```python exec
id: the-toolkit-so-far-4
# Sets: sorted lists with no repeats.
def make_set(items):
    result = []
    for item in sorted(items):
        if not result or item != result[-1]:
            result.append(item)
    return result


def union(a, b):
    return make_set(a + b)


def intersection(a, b):
    result = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i, j = i + 1, j + 1
        elif a[i] < b[j]:
            i = i + 1
        else:
            j = j + 1
    return result


print(union([1, 3], [2, 3]), intersection([1, 3], [2, 3]))
```

## Problem 1: The polynomial workshop

Suppose you are given two polynomials. How might you write a complete
analysis of them? Write a function `analyse_polynomials(p, q)` that does
these things:

1. Display both polynomials.
2. Add them, and display the result.
3. Multiply them, and display the result.
4. Find the roots of each one, if it is linear or quadratic.
5. Check each root by evaluating the polynomial there. The answer
   should be 0.

```python exec
id: problem-1-the-polynomial-workshop-1
# Your analyse_polynomials function
```

Test it with the two polynomials in the comments below.

```python exec
id: problem-1-the-polynomial-workshop-2
# Test with:
# p = [3, -4, 1]    (x^2 - 4x + 3)
# q = [-6, -1, 1]   (x^2 - x - 6)
```

## Problem 2: Where do they meet?

Two polynomials $p(x)$ and $q(x)$ intersect where their graphs meet,
which is where $p(x) = q(x)$. That is the same as $p(x) - q(x) = 0$.

For example, $x^2$ and $2x + 3$ meet where $x^2 - 2x - 3 = 0$. That
factorises as $(x - 3)(x + 1) = 0$, so they meet at $x = 3$ and
$x = -1$. Check: at $x = 3$, both give 9.

How might you write a function `find_intersections(p, q)` that finds
where two polynomials meet? Keep to polynomials that are at most
quadratic.

1. Use `subtract_poly` to find $p - q$.
2. Solve $p - q = 0$ with the right solver for its degree.

```python exec
id: problem-2-where-do-they-meet-1
# Your find_intersections function
```

Test it with the example above.

```python exec
id: problem-2-where-do-they-meet-2
# Test: where do x^2 and 2x + 3 intersect?
# p = [0, 0, 1]   (x^2)
# q = [3, 2]       (2x + 3)
# p - q = [-3, -2, 1] (x^2 - 2x - 3)
# Roots should be x = 3 and x = -1
```

## Problem 3: Sets of solutions

Different quadratic equations have different sets of solutions. We can
use our set tools to compare them.

Here is a list of four quadratics. Can you answer these questions with
your code?

1. What are the real roots of each equation?
2. Which roots are shared by *all* the equations? (Use the
   intersection.)
3. Which roots appear in *any* of the equations? (Use the union.)
4. Which root appears in the most equations?

```python exec
id: problem-3-sets-of-solutions-1
# Find and compare solution sets
equations = [
    [3, -4, 1],    # x^2 - 4x + 3 = 0 (roots: 1, 3)
    [-6, -1, 1],   # x^2 - x - 6 = 0 (roots: 3, -2)
    [2, -3, 1],    # x^2 - 3x + 2 = 0 (roots: 1, 2)
    [-3, -2, 1],   # x^2 - 2x - 3 = 0 (roots: 3, -1)
]

# For each equation, find its roots
# Collect all roots into sets
# Find the intersection (roots common to all)
# Find the union (all roots that appear anywhere)
# Which root appears in the most equations?
```

## Problem 4: Building and verifying

This problem ties everything together. We start from the roots we
want, and work backwards to the equation.

Say we want the roots $x = 2$ and $x = -5$. Which quadratic has those
roots? Multiplying the factors $(x - 2)(x + 5)$ gives
$x^2 + 3x - 10$. Then solving $x^2 + 3x - 10 = 0$ should give 2 and −5
back again.

Let's write a function `roundtrip(root1, root2)` that does this full
cycle:

1. Build the quadratic by multiplying the two factors.
2. Solve the quadratic.
3. Check that you get the original roots back.
4. Display the polynomial, its factorised form, and its roots.

```python exec
id: problem-4-building-and-verifying-1
# Your roundtrip function
```

Then test it with several pairs of roots. The last pair is a
repeated root: the same root twice. What do you expect to happen
there?

```python exec
id: problem-4-building-and-verifying-2
# Test with several pairs of roots
# roundtrip(2, -5)
# roundtrip(0, 7)
# roundtrip(3, 3)     # repeated root
```

## Problem 5: Self-assessment

How confident do you feel about each of these tasks? Rate each one on a
scale from 1 (not confident) to 5 (very confident).

1. Representing a polynomial as a list of coefficients
2. Evaluating a polynomial at a given value of $x$
3. Adding and multiplying polynomials
4. Using the quadratic formula to find roots
5. Checking your work by evaluating the polynomial at its roots
6. Creating a set from a list (removing duplicates, sorting)
7. Finding the intersection and union of two sets
8. Solving a system of two linear equations

Then pick one task that you rated low, and spend some time working on
it.

```python exec
id: problem-5-self-assessment-1
# Your confidence ratings and notes
# 1. Polynomial representation: 
# 2. Evaluation: 
# 3. Add/multiply: 
# 4. Quadratic formula: 
# 5. Verification: 
# 6. Set creation: 
# 7. Set operations: 
# 8. Simultaneous equations: 

# Which one did you spend extra time on? What did you do?
```

## Building it yourself

The real test of this material is to build a small algebra engine from
nothing. That means polynomials and their operations, equation solving,
and set operations, all written fresh, without copying from the
tutorials. The ideas and patterns are the same. Only the typing is new.

The aim is to understand the ideas well enough to rebuild the code, and
not to memorise it. Here are two examples:

- If you understand that multiplying polynomials combines every term of
  the first with every term of the second, you can write the nested
  loop.
- If you understand that a set intersection keeps the elements that
  appear in both sorted lists, you can write the merge.

In the long run, understanding usually does far more for you than
memorising.

What are the three most important ideas from the four tutorials above?
Choose the ones you would want to remember even if you forgot
everything else. Take a few minutes to write them down:

```python exec
id: looking-ahead-to-skills-demo-2b-1
# Your three most important ideas
# 1. 
# 2. 
# 3. 
```

## Reflection

We have come a long way. We started with "Hello, world!" in
[Algorithms, pseudocode and your first Python](tutorial:first-steps).
We have reached polynomial algebra, equation solving, and set theory in
[Sets: building them from sorted lists](tutorial:sets-as-sorted-lists),
and on to limits and derivatives in
[Derivatives: the rate of change of a curve](tutorial:rates-of-change).
Each piece builds on the ones before it, and the maths ideas and the
programming ideas are woven together all the way through.

Here is a final question to reflect on. What has changed about how you
think about mathematics since we started? And what has changed about
how you think about programming?

## Where to Read More

Pastötter, B. and Bäuml, K.-H. T. (2014). *Retrieval Practice Enhances New
Learning: The Forward Effect of Testing.* Frontiers in Psychology, 5, 286.
<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3983480/>. Why rebuilding a
function from memory, as this page asks you to, teaches more than copying
it out again.
