---
title: "Solving equations: linear, quadratic and simultaneous"
year: "2026-2027"
version: 2026.09.25.1
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

# Solving equations: linear, quadratic and simultaneous

In [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
we stored polynomials as lists, and evaluated, added and multiplied
them. In [Rearranging formulae: changing the subject](tutorial:rearranging-formulae)
we learned to move letters around a formula. Now we put the two together
and *solve* equations. To solve an equation means to find the values of
$x$ that make it true. For example, $3x + 7 = 22$ is true when $x = 5$.

A value of $x$ that makes an equation true is called a *solution* of the
equation. When the equation has the form "polynomial $= 0$", a solution
is also called a *root* of the polynomial. For example, $x = 1$ is a root
of $x^2 - 4x + 3$, because $1 - 4 + 3 = 0$.

On this page we:

- solve linear equations, like $3x + 7 = 22$
- solve quadratic equations, like $x^2 - 4x + 3 = 0$, with a formula
- factorise quadratics: split them into simpler pieces
- solve inequalities, like $2x + 3 > 7$
- solve two equations with two unknowns at the same time

## Solving linear equations

A *linear equation* is an equation where $x$ appears only to the power
1. We can always rearrange one into the form $ax + b = 0$. The rule is
to do the same thing to both sides, so that they stay equal. For
example, subtracting 22 from both sides of $3x + 7 = 22$ gives
$3x - 15 = 0$.

To solve $ax + b = 0$, we subtract $b$ from both sides, then divide by
$a$:

$$x = -\frac{b}{a} \quad \text{(as long as } a \neq 0 \text{)}$$

For $3x - 15 = 0$, that gives $x = -\frac{-15}{3} = 5$.

In code, a function takes the two numbers in the order they appear in
$ax + b$: first $a$, then $b$. So `solve_linear(3, -15)` is about
$3x - 15 = 0$. Every function on this page that takes coefficients
works the same way, starting with the number in front of the highest
power.

### Your turn

Can you write a function `solve_linear(a, b)` that returns the solution
of $ax + b = 0$?

1. Write the function in the first cell.
2. Think about $a = 0$. Then there is no $x$ term at all, so it is not
   really a linear equation. Make your function handle that case with a
   clear message, without crashing.
3. Test it in the second cell with the three cases in the comments.

```python exec
id: your-turn-1
# Your solve_linear function
```

```python exec
id: your-turn-2
# Test cases
# solve_linear(3, 7) solves 3x + 7 = 0 -> x = -7/3
# solve_linear(5, -15) solves 5x - 15 = 0 -> x = 3
# solve_linear(0, 4) -> no solution (or "not a linear equation")
```

## The quadratic formula

A *quadratic equation* has the form $ax^2 + bx + c = 0$, with
$a \neq 0$. It can have up to two solutions. The *quadratic formula*
gives them:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

The sign $\pm$ means "plus or minus". Using $+$ gives one solution, and
using $-$ gives the other.

Here is one worked example. For $x^2 - 4x + 3 = 0$, we have $a = 1$,
$b = -4$ and $c = 3$. Then $b^2 - 4ac = 16 - 12 = 4$, and
$\sqrt{4} = 2$. So

$$x = \frac{4 \pm 2}{2}, \quad\text{which gives } x = 3 \text{ or } x = 1.$$

The part under the square root, $b^2 - 4ac$, is called the
*discriminant*. The discriminant tells us how many real solutions there
are:

| Discriminant | Real roots | Example | $b^2 - 4ac$ |
|---|---|---|---|
| positive | two different roots | $x^2 - 4x + 3 = 0$ | $16 - 12 = 4$ |
| zero | one repeated root | $x^2 - 2x + 1 = 0$ | $4 - 4 = 0$ |
| negative | no real roots | $x^2 + 5 = 0$ | $0 - 20 = -20$ |

Why no real roots when it is negative? No real number squared gives a
negative number, so the square root of a negative number is not a real
number. The graph of a quadratic is a curve called a parabola. When
the discriminant is negative, the parabola does not cross the $x$-axis.
You will draw these curves in
[Functions and their graphs](tutorial:drawing-functions). And in
[Complex numbers: roots that are not real](tutorial:complex-roots),
the very next page, we find roots for these equations after all.

### Your turn

How might you write a function `solve_quadratic(a, b, c)`? It takes the
three numbers in the order they appear in $ax^2 + bx + c$, and returns
the solutions. It should handle all three cases of the discriminant.

**Pseudocode:**
```
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

1. Write `solve_quadratic` in the first cell.
2. Test it in the second cell with the four cases in the comments.

```python exec
id: your-turn-3
import math

# Your solve_quadratic function
```

```python exec
id: your-turn-4
# Test cases
# solve_quadratic(1, -4, 3) solves x^2 - 4x + 3 = 0 -> roots 1 and 3
# solve_quadratic(1, -2, 1) solves x^2 - 2x + 1 = 0 -> repeated root 1
# solve_quadratic(1, 0, 5) solves x^2 + 5 = 0 -> no real roots
# solve_quadratic(1, 0, -9) solves x^2 - 9 = 0 -> roots 3 and -3
```

### Verifying solutions

How can we be sure a root is right? If $x$ is a root of the polynomial,
then evaluating the polynomial at $x$ gives zero. With floats, it may
give a number very close to zero instead.

The cell below uses your `solve_quadratic`, so run it after you have
written that function. It puts each root back into $x^2 - 4x + 3$.
What values do you expect it to print?

```python exec
id: verifying-solutions-1
a, b, c = 1, -4, 3   # x^2 - 4x + 3
roots = solve_quadratic(a, b, c)
print("Roots:", roots)
for root in roots:
    value = a * root ** 2 + b * root + c
    print("  p(" + str(root) + ") =", value)
```

### Your turn

Can you write a function `verify_roots(a, b, c, roots)` that
substitutes each root back for you?

1. Evaluate the polynomial at each root.
2. Print each root beside the value it gives. How close to zero is close
   enough? A value like `2.2e-16` is zero, give or take rounding, so
   compare with a small tolerance, like 0.0001, rather than with an exact
   zero.
3. Test it on several quadratics in the second cell.

```python exec
id: your-turn-5
# Your verify_roots function
```

```python exec
id: your-turn-6
# Test it on several quadratics
```

## Factorisation

Suppose we know the roots $r_1$ and $r_2$ of a quadratic
$ax^2 + bx + c$. Then we can write the quadratic in *factorised form*:

$$a(x - r_1)(x - r_2)$$

For example, the roots of $x^2 - 4x + 3$ are 1 and 3, so
$x^2 - 4x + 3 = (x - 1)(x - 3)$. Here $a = 1$, so we do not need to
write it.

To *factorise* a quadratic is to write it in this form. A *binomial* is
a polynomial with two terms, such as $x - 1$. Factorising is the reverse
of expanding brackets with FOIL. When we expand, we multiply two
binomials to get a quadratic. When we factorise, we split a quadratic
into two binomials.

### Your turn

Can you write a function `factor_quadratic(a, b, c)` that returns a
string showing the factorised form?

1. Use `solve_quadratic` to find the roots.
2. Build the string from the roots. Be careful with the leading
   coefficient $a$: it goes in front.
3. If the quadratic has no real roots, the function should say so
   in plain words, and not guess at an answer.
4. Test it in the second cell with the three cases in the comments.

```python exec
id: your-turn-7
# Your factor_quadratic function
```

```python exec
id: your-turn-8
# Test cases
# factor_quadratic(1, -4, 3) -> "(x - 1)(x - 3)" or similar
# factor_quadratic(1, -1, -6) -> "(x - 3)(x + 2)" or similar (roots are 3 and -2)
# factor_quadratic(1, 0, 5) -> "Cannot be factorised over the reals"
```

### Verification by expansion

We can check a factorisation by multiplying the factors back together.
If we get the original polynomial, the factorisation is right. This is
where `multiply_poly` from
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
is useful again. The cell below brings it back.

`multiply_poly` works on lists, as it did on that page, with the
constant first, so that each number sits at the index of its power.
So $x - 1$ is `[-1, 1]` here. A list is a different thing from the
arguments of `solve_quadratic`: it holds a whole polynomial of any
length. What list do you expect the cell to print?

```python exec
id: verification-by-expansion-1
# multiply_poly, as written in "Polynomials: representing and combining them in Python"
def multiply_poly(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] += a[i] * b[j]
    return result


# If x^2 - 4x + 3 = (x - 1)(x - 3), then:
factor1 = [-1, 1]     # (x - 1) in our convention
factor2 = [-3, 1]     # (x - 3)
product = multiply_poly(factor1, factor2)
print("Product:", product)  # x^2 - 4x + 3, written constant first
```

## Solving inequalities

An *inequality* compares two expressions with $>$, $\geq$, $<$ or
$\leq$. A linear inequality like $2x + 3 > 7$ has a whole set of
solutions: every $x$ that makes it true.

We solve it with the same steps as an equation:

$$2x + 3 > 7 \implies 2x > 4 \implies x > 2$$

For example, $x = 3$ works: $2 \times 3 + 3 = 9$, and $9 > 7$.

There is one extra rule, and it trips up most people at first. **If we
multiply or divide both sides by a negative number, the inequality
flips.** For example, $-x > 3$ becomes $x < -3$ when we divide by $-1$.
Check with $x = -4$: $-(-4) = 4$, and $4 > 3$ is true.

### Your turn

How might you write a function `solve_linear_inequality(a, b, c, operator)`?

1. It should solve $ax + b$ [operator] $c$, where the operator is one of
   `">"`, `">="`, `"<"` or `"<="`.
2. It should return a string that describes the set of solutions.
3. Think about what happens when $a$ is negative: the direction of the
   inequality reverses.
4. Test it in the second cell with the three cases in the comments.

```python exec
id: your-turn-9
# Your solve_linear_inequality function
```

```python exec
id: your-turn-10
# Test cases
# solve_linear_inequality(2, 3, 7, ">")  -> "x > 2.0"
# solve_linear_inequality(-3, 5, 2, "<") -> "x > 1.0" (inequality flips!)
# solve_linear_inequality(0, 5, 3, ">")  -> "True for all x" (5 > 3 whatever x is)
# solve_linear_inequality(0, 5, 7, ">")  -> "No solution" (5 > 7 is never true)
```

## Simultaneous equations

Sometimes we need values that make two equations true at the same time.
Two equations like this are called *simultaneous equations*. Here is an
example:

$$x + y = 10$$
$$2x - y = 5$$

Its solution is $x = 5$, $y = 5$. Check: $5 + 5 = 10$, and
$2 \times 5 - 5 = 5$.

The classic method is *elimination*. We multiply the equations by
numbers chosen so that one unknown cancels out when we add or subtract
them. In the example, adding the two equations cancels $y$:
$3x = 15$, so $x = 5$. Then $y = 10 - 5 = 5$.

If we do elimination on the general system
$a_1 x + b_1 y = c_1$ and $a_2 x + b_2 y = c_2$, we get a formula for
each unknown:

$$x = \frac{c_1 b_2 - c_2 b_1}{a_1 b_2 - a_2 b_1}, \quad y = \frac{a_1 c_2 - a_2 c_1}{a_1 b_2 - a_2 b_1}$$

The bottom of both fractions, $a_1 b_2 - a_2 b_1$, is called the
*determinant*. If the determinant is zero, the system has no single
solution. Each equation's graph is a straight line, and the solution is
the point where the two lines cross. A zero determinant means the lines
are parallel (they never cross) or are the same line (they meet
everywhere).

### Your turn

Can you write a function `solve_simultaneous(eq1, eq2)`?

1. Each equation is a list `[a, b, c]`, which means $ax + by = c$.
2. The function returns the values of $x$ and $y$.
3. If there is no single solution, it says so in plain words.
4. Test it in the second cell with the three systems in the comments.

If you want to go further, try extending it to three equations with
three unknowns.

```python exec
id: your-turn-11
# Your solve_simultaneous function
```

```python exec
id: your-turn-12
# Test: solve the system x + y = 10, 2x - y = 5
# Should give x = 5, y = 5

# Test: 3x + 2y = 12, x - y = -1
# Should give x = 2, y = 3

# Test: 2x + 4y = 10, x + 2y = 5  (same line, infinite solutions)
```

## Reflection

We have built tools for solving equations from scratch: linear
equations, quadratic equations (where the discriminant tells us how many
solutions there are), factorisation, inequalities and simultaneous
equations. Each method is a function that takes coefficients and
returns results.

The strength of this approach is that we can check everything with
code:

- Find a root, then evaluate the polynomial at that root to confirm it
  gives zero.
- Factorise a quadratic, then multiply the factors to confirm we get the
  original.
- Solve a system, then put the values back in to confirm both equations
  hold.

Next, in
[Complex numbers: roots that are not real](tutorial:complex-roots), we
go back to the quadratics with a negative discriminant, and find their
roots in a new family of numbers.

Which type of equation did you find most satisfying to solve with code?

## Where to Read More

Khan Academy. *Quadratic Formula (Proof).*
<https://www.youtube.com/watch?v=mDmRYfma9C0>. Where the formula this page
turns into `solve_quadratic` comes from — completing the square,
step by step.
