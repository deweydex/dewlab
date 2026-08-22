---
title: "Tutorial 15: Cracking Equations"
slug: tutorial-15-cracking-equations
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
order: 15
version: 1
covers:
  solving-linear-equations:
    touches: [MIT-1.7]
  the-quadratic-formula:
    touches: [MIT-1.10]
  factorisation:
    covers: [MIT-1.9]
  solving-inequalities:
    covers: [MIT-1.11]
  simultaneous-equations:
    covers: [MIT-1.12]
---

# Tutorial 15: Cracking Equations

**Programming Design Principles / Maths for IT**

We can now represent, evaluate, and manipulate polynomials. Today we learn to *solve* them: given an equation like $3x + 7 = 22$ or $x^2 - 4x + 3 = 0$, find the values of x that make it true.

We will also learn to factor quadratics -- decomposing them into simpler pieces -- and to solve systems of equations with two unknowns.

## Solving Linear Equations

A linear equation has the form $ax + b = 0$. The solution is straightforward:

$$x = -\frac{b}{a} \quad \text{(provided } a \neq 0 \text{)}$$

In our coefficient-list convention, a linear polynomial `[b, a]` represents $ax + b$. Setting it equal to zero and solving gives $x = -b/a$.

### Your turn

Write a function `solve_linear(coeffs)` that takes `[b, a]` and returns the solution. Think about edge cases: what if $a = 0$? That means there is no x term, so it is not really a linear equation. Your function should handle this gracefully.

```python exec
id: your-turn-1
# Your solve_linear function
```

```python exec
id: your-turn-2
# Test cases
# solve_linear([7, 3]) solves 3x + 7 = 0 -> x = -7/3
# solve_linear([-15, 5]) solves 5x - 15 = 0 -> x = 3
# solve_linear([4, 0]) -> no solution (or "not a linear equation")
```

## The Quadratic Formula

A quadratic equation $ax^2 + bx + c = 0$ has up to two solutions, given by:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

The expression under the square root, $b^2 - 4ac$, is called the *discriminant* and tells us how many real solutions exist:

- If the discriminant is positive: two distinct real roots
- If the discriminant is zero: one repeated root
- If the discriminant is negative: no real roots (the parabola does not cross the x-axis)

### Your turn

Write a function `solve_quadratic(coeffs)` that takes `[c, b, a]` (our convention) and returns the solutions. Handle all three cases of the discriminant.

**Pseudocode:**
```
EXTRACT c, b, a from coeffs
COMPUTE discriminant = b^2 - 4*a*c
IF discriminant > 0:
    COMPUTE root1 = (-b + sqrt(discriminant)) / (2*a)
    COMPUTE root2 = (-b - sqrt(discriminant)) / (2*a)
    RETURN (root1, root2)
ELIF discriminant == 0:
    COMPUTE root = -b / (2*a)
    RETURN (root,)
ELSE:
    RETURN () or a message indicating no real roots
```

```python exec
id: your-turn-3
import math

# Your solve_quadratic function
```

```python exec
id: your-turn-4
# Test cases
# solve_quadratic([3, -4, 1]) solves x^2 - 4x + 3 = 0 -> roots 1 and 3
# solve_quadratic([1, -2, 1]) solves x^2 - 2x + 1 = 0 -> repeated root 1
# solve_quadratic([5, 0, 1]) solves x^2 + 5 = 0 -> no real roots
# solve_quadratic([-9, 0, 1]) solves x^2 - 9 = 0 -> roots 3 and -3
```

### Verifying solutions

A satisfying check: if x is a root of the polynomial, then evaluating the polynomial at x should give zero (or very close to zero, allowing for floating-point imprecision).

```python exec
id: verifying-solutions-1
# Verification pattern
coeffs = [3, -4, 1]   # x^2 - 4x + 3
roots = solve_quadratic(coeffs)
print("Roots:", roots)
for root in roots:
    value = evaluate_poly(coeffs, root)
    print("  p(" + str(root) + ") =", value)
```

### Your turn

Write a function `verify_roots(coeffs, roots)` that checks whether each root really is a root by evaluating the polynomial at that point. Print PASS or FAIL for each (use a small tolerance like 0.0001 for floating-point comparison instead of exact equality).

```python exec
id: your-turn-5
# Your verify_roots function
```

```python exec
id: your-turn-6
# Test it on several quadratics
```

## Factorisation

If we know the roots $r_1$ and $r_2$ of a quadratic $ax^2 + bx + c$, we can write it in factored form:

$$a(x - r_1)(x - r_2)$$

For example, $x^2 - 4x + 3 = (x - 1)(x - 3)$.

This is the reverse of expanding (FOIL): instead of multiplying two binomials to get a quadratic, we decompose a quadratic into two binomials.

### Your turn

Write a function `factor_quadratic(coeffs)` that returns a string showing the factored form. If the quadratic has no real roots, return a message saying it cannot be factored over the reals.

Hint: use `solve_quadratic` to find the roots, then construct the string. Be careful with the leading coefficient $a$.

```python exec
id: your-turn-7
# Your factor_quadratic function
```

```python exec
id: your-turn-8
# Test cases
# factor_quadratic([3, -4, 1]) -> "(x - 1)(x - 3)" or similar
# factor_quadratic([-6, -1, 1]) -> "(x - 3)(x + 2)" or similar (roots are 3 and -2)
# factor_quadratic([5, 0, 1]) -> "Cannot be factored over the reals"
```

### Verification by expansion

We can verify a factorisation by multiplying the factors back together and checking that we get the original polynomial. This is where `multiply_poly` from Tutorial 14 pays off:

```python exec
id: verification-by-expansion-1
# If x^2 - 4x + 3 = (x - 1)(x - 3), then:
factor1 = [-1, 1]     # (x - 1) in our convention
factor2 = [-3, 1]     # (x - 3)
product = multiply_poly(factor1, factor2)
print("Product:", product)  # should be [3, -4, 1]
```

## Solving Inequalities

A linear inequality like $2x + 3 > 7$ defines a *set* of solutions rather than a single value. Solving it follows the same steps as an equation, but we need to remember: if we multiply or divide by a negative number, the inequality flips.

$$2x + 3 > 7 \implies 2x > 4 \implies x > 2$$

### Your turn

Write a function `solve_linear_inequality(a, b, c, operator)` that solves $ax + b$ [operator] $c$ where operator is one of ">", ">=", "<", "<=". Return a string describing the solution set.

Think about what happens when $a$ is negative (the inequality direction reverses).

```python exec
id: your-turn-9
# Your solve_linear_inequality function
```

```python exec
id: your-turn-10
# Test cases
# solve_linear_inequality(2, 3, 7, ">")  -> "x > 2.0"
# solve_linear_inequality(-3, 5, 2, "<") -> "x > 1.0" (inequality flips!)
# solve_linear_inequality(0, 5, 3, ">")  -> "True for all x" or "No solution"
```

## Simultaneous Equations

Sometimes we need to find values that satisfy two equations at once. The system:

$$x + y = 10$$
$$2x - y = 5$$

has the solution $x = 5, y = 5$.

The classic approach is *elimination*: multiply the equations so that one variable cancels when we add or subtract them. For the system $a_1 x + b_1 y = c_1$ and $a_2 x + b_2 y = c_2$:

$$x = \frac{c_1 b_2 - c_2 b_1}{a_1 b_2 - a_2 b_1}, \quad y = \frac{a_1 c_2 - a_2 c_1}{a_1 b_2 - a_2 b_1}$$

The denominator $a_1 b_2 - a_2 b_1$ is called the *determinant*. If it is zero, the system has no unique solution (the lines are parallel or identical).

### Your turn

Write a function `solve_simultaneous(eq1, eq2)` where each equation is represented as `[a, b, c]` meaning $ax + by = c$. Return the values of x and y, or indicate if no unique solution exists.

```python exec
id: your-turn-11
# Your solve_simultaneous function
```

```python exec
id: your-turn-12
# Test: solve the system x + y = 10, 2x - y = 5
# Should give x = 5, y = 5

# Test: 3x + 2y = 12, x - y = 1
# Should give x = 2, y = 3

# Test: 2x + 4y = 10, x + 2y = 5  (same line, infinite solutions)
```

## Reflection

We have built equation-solving machinery from scratch: linear equations, quadratic equations (with the discriminant determining the number of solutions), factorisation, inequalities, and simultaneous equations. Each solution method is a function that takes coefficients and returns results.

The power of this approach is that we can verify everything computationally. Find a root, then evaluate the polynomial at that root to confirm it is zero. Factor a quadratic, then multiply the factors to confirm we get the original. Solve a system, then substitute back to confirm both equations hold.

Next tutorial we will work with sets -- collections where membership and relationships matter -- which is the last major topic before Skills Demo 2B.

Which type of equation did you find most satisfying to solve programmatically?
