---
title: "Tutorial 17: Bringing It All Together"
slug: tutorial-17-bringing-it-all-together
module: mit-pdp-maths-prog-integration
year: "2026-2027"
series: maths-and-programming
order: 17
version: 1
---

# Tutorial 17: Bringing It All Together

**Programming Design Principles / Maths for IT**

This is the last tutorial before Skills Demo 2B. Rather than introducing new material, today we practise combining the tools we have built across the last four tutorials into something cohesive. We will work through a few problems that require multiple tools, and we will think about how all these mathematical concepts connect to each other and to programming.

## The Toolkit So Far

Over Tutorials 13-16, we built:

**From Tutorial 13:** `classify_number`, `power`, `log_base`, geometry functions

**From Tutorial 14:** `evaluate_poly`, `poly_to_string`, `add_poly`, `multiply_poly`, `subtract_poly`, `scale_poly`

**From Tutorial 15:** `solve_linear`, `solve_quadratic`, `factor_quadratic`, `solve_linear_inequality`, `solve_simultaneous`

**From Tutorial 16:** `make_set`, `is_member`, `union`, `intersection`, `difference`, `symmetric_difference`, `is_subset`, `is_equal`

Let's start by collecting our key functions. Copy them into the cell below (or rewrite them -- sometimes rewriting from memory is the best test of understanding):

```python exec
id: the-toolkit-so-far-1
# Collect your key functions here
# You may want to import math at the top

import math

# Polynomial functions

# Equation solving functions

# Set functions
```

## Problem 1: The Polynomial Workshop

Given two polynomials, produce a complete analysis: display them, add them, multiply them, find the roots of each (if they are linear or quadratic), and verify the roots by evaluation.

Write a function `analyse_polynomials(p, q)` that does all of this:

```python exec
id: problem-1-the-polynomial-workshop-1
# Your analyse_polynomials function
```

```python exec
id: problem-1-the-polynomial-workshop-2
# Test with:
# p = [3, -4, 1]    (x^2 - 4x + 3)
# q = [-6, -1, 1]   (x^2 - x - 6)
```

## Problem 2: Where Do They Meet?

Two polynomials $p(x)$ and $q(x)$ intersect where $p(x) = q(x)$, which means $p(x) - q(x) = 0$.

Write a function `find_intersections(p, q)` that finds where two polynomials (up to quadratic) intersect. Use `subtract_poly` to get the difference, then solve the resulting equation.

```python exec
id: problem-2-where-do-they-meet-1
# Your find_intersections function
```

```python exec
id: problem-2-where-do-they-meet-2
# Test: where do x^2 and 2x + 3 intersect?
# p = [0, 0, 1]   (x^2)
# q = [3, 2]       (2x + 3)
# p - q = [-3, -2, 1] (x^2 - 2x - 3)
# Roots should be x = 3 and x = -1
```

## Problem 3: Sets of Solutions

Different quadratic equations have different solution sets. Let's explore the relationship between the solutions of several equations using our set tools.

Given a list of quadratic polynomials, find the set of all real roots across all of them, and determine which roots are shared between which equations.

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

## Problem 4: Building and Verifying

Here is a challenge that ties everything together. Start with the roots you want: say, $x = 2$ and $x = -5$. Build a quadratic that has those roots by multiplying the factors $(x - 2)(x + 5)$. Then solve the quadratic to verify you get the original roots back. Finally, display the polynomial, its factored form, and its roots.

Write a function `roundtrip(root1, root2)` that demonstrates this full cycle.

```python exec
id: problem-4-building-and-verifying-1
# Your roundtrip function
```

```python exec
id: problem-4-building-and-verifying-2
# Test with several pairs of roots
# roundtrip(2, -5)
# roundtrip(0, 7)
# roundtrip(3, 3)     # repeated root
```

## Problem 5: Self-Assessment

For each of the following tasks, rate your confidence on a scale of 1 (not confident) to 5 (very confident). Then pick one task you rated low and spend some time working on it.

1. Representing a polynomial as a list of coefficients
2. Evaluating a polynomial at a given value of x
3. Adding and multiplying polynomials
4. Using the quadratic formula to find roots
5. Checking your work by evaluating the polynomial at its roots
6. Creating a set from a list (removing duplicates, sorting)
7. Finding the intersection and union of two sets
8. Solving a system of two linear equations

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

## Looking Ahead to Skills Demo 2B

Skills Demo 2B will ask you to build an algebra engine: polynomial representation and operations, equation solving, and set operations. You will be working from fresh -- not copying from these tutorials -- but the ideas and patterns are the same.

The key is not to memorise code but to understand the ideas well enough to reconstruct them. If you understand that polynomial multiplication works by combining every term in the first with every term in the second, you can write the nested loop. If you understand that set intersection keeps elements that appear in both sorted lists, you can write the merge-walk. Understanding beats memorisation every time.

Take a few minutes to write down the three most important ideas from Tutorials 13-16 -- the ones you would want to remember even if you forgot everything else:

```python exec
id: looking-ahead-to-skills-demo-2b-1
# Your three most important ideas
# 1. 
# 2. 
# 3. 
```

## Reflection

We have come a long way: from "Hello, world!" in Tutorial 1 to polynomial algebra, equation solving, and set theory in Tutorial 16. Each piece builds on the ones before it, and the mathematical ideas and programming concepts are woven together throughout.

The final reflection: what has changed about how you think about mathematics since we started? And what has changed about how you think about programming?
