---
title: "Solving equations: linear, quadratic and simultaneous — Practice"
practice_for: cracking-equations
year: "2026-2027"
version: 2026.09.24.1
---

# Solving equations: linear, quadratic and simultaneous — Practice

The answers are hidden in folds under each problem. You can check every
root you find yourself: put it back into the equation, and see whether
you get zero. This is called *substituting* the root back in. So you can
find a wrong answer yourself, and fix it.

The factorising and quadratic problems are adapted from the Mathematics
repository's factoring worksheet.

## Linear equations

```python exec
id: linear-equations-1
def solve_linear(a, b):
    """Solve ax + b = 0."""
    if a == 0:
        return "no solution" if b else "every number"
    return -b / a


print(solve_linear(3, -12), solve_linear(0, 5), solve_linear(0, 0))
```

**1.** Solve each equation.

- (a) $3x - 12 = 0$
- (b) $5x + 20 = 0$
- (c) $7 - 2x = 0$
- (d) $\frac{x}{4} + 3 = 0$

<details class="dl-answer"><summary>answer</summary>

(a) 4. (b) −4. (c) 3.5. (d) −12.

</details>

**2.** Solve $3(x - 2) + 4 = 2(x + 5)$.

<details class="dl-answer"><summary>answer</summary>

$x = 12$.

1. Expand the brackets: $3x - 6 + 4 = 2x + 10$.
2. Tidy the left side: $3x - 2 = 2x + 10$.
3. Subtract $2x$ and add 2 on both sides: $x = 12$.

Check by substituting $x = 12$: the left side is $3(10) + 4 = 34$, and
the right side is $2(17) = 34$.

</details>

**3.** What happens with $2x + 3 = 2x + 5$? And with $2x + 3 = 2x + 3$?

<details class="dl-answer"><summary>answer</summary>

The first has no solution: subtracting $2x$ from both sides leaves
$3 = 5$, which is false. The second is true for every $x$.

In both cases, the $x$ terms cancel and we reach $0x = $ something. That
is why `solve_linear` has to check for `a == 0` before it divides. An
equation with no solutions and an equation with infinitely many look
the same until the last step.

</details>

## Quadratics by factorising

**4.** Factorise each quadratic.

- (a) $x^2 + 7x + 12$
- (b) $x^2 + 9x + 20$
- (c) $x^2 - 10x + 24$
- (d) $x^2 + 2x - 15$

<details class="dl-answer"><summary>answer</summary>

(a) $(x + 3)(x + 4)$. (b) $(x + 4)(x + 5)$. (c) $(x - 4)(x - 6)$. (d) $(x + 5)(x - 3)$.

Look for two numbers that multiply to give the constant and add to give
the middle coefficient. In (a), $3 \times 4 = 12$ and $3 + 4 = 7$. When
the constant is negative, as in (d), the two numbers have opposite
signs: $5 \times (-3) = -15$ and $5 + (-3) = 2$.

</details>

**5.** Factorise these. Each one follows a special pattern.

- (a) $x^2 - 49$
- (b) $x^2 - 100$
- (c) $x^2 + 6x + 9$
- (d) $x^2 - 14x + 49$
- (e) $4x^2 - 25$

<details class="dl-answer"><summary>answer</summary>

(a) $(x - 7)(x + 7)$. (b) $(x - 10)(x + 10)$. (c) $(x + 3)^2$. (d) $(x - 7)^2$. (e) $(2x - 5)(2x + 5)$.

(a), (b) and (e) are each a difference of two squares:
$x^2 - a^2 = (x - a)(x + a)$. (c) and (d) are each a *perfect square*:
$x^2 + 2ax + a^2 = (x + a)^2$. These two patterns are worth learning to
spot quickly. They appear often, and when you see them you do not need
to search for factor pairs.

</details>

**6.** Factorise $x^2 + 4$.

<details class="dl-answer"><summary>answer</summary>

It cannot be factorised using real numbers.

A difference of two squares factorises, but a *sum* of two squares does
not. Its discriminant is $0 - 16 = -16$, which is negative, so it has no
real roots. Using complex numbers it is $(x - 2i)(x + 2i)$. That is the
subject of the next page,
[Complex numbers: roots that are not real](tutorial:complex-roots).

</details>

**7.** Take out the common factor first, then factorise.

- (a) $2x^2 + 10x + 12$
- (b) $3x^2 - 27$
- (c) $5x^2 - 5x - 30$

<details class="dl-answer"><summary>answer</summary>

(a) $2(x + 2)(x + 3)$. (b) $3(x - 3)(x + 3)$. (c) $5(x - 3)(x + 2)$.

If you take out the common factor first, each of these becomes an easy
case. For example, $5x^2 - 5x - 30 = 5(x^2 - x - 6)$. If you try (c)
without doing this, you have to search for two numbers that multiply to
$5 \times (-30) = -150$. That is possible, but not pleasant.

</details>

**8.** Factorise $2x^2 + 7x + 3$. Here the leading coefficient (the
coefficient of $x^2$) is not 1.

<details class="dl-answer"><summary>answer</summary>

$(2x + 1)(x + 3)$.

1. Find two numbers that multiply to $2 \times 3 = 6$ and add to 7.
   They are 6 and 1.
2. Split the middle term using them: $2x^2 + 6x + x + 3$.
3. Group the terms in pairs: $2x(x + 3) + 1(x + 3)$.
4. Take out the common bracket: $(2x + 1)(x + 3)$.

Another way is to use the quadratic formula and work backwards from the
roots. A computer does this, and it is the better choice when
the numbers are awkward.

</details>

## The quadratic formula

```python exec
id: the-quadratic-formula-1
import math


def solve_quadratic(a, b, c):
    """Real roots of ax^2 + bx + c = 0."""
    d = b * b - 4 * a * c
    if d > 0:
        root = math.sqrt(d)
        return ((-b + root) / (2 * a), (-b - root) / (2 * a))
    if d == 0:
        return (-b / (2 * a),)
    return ()


for coeffs in [(1, -4, 3), (1, -2, 1), (1, 0, 5), (1, 0, -9)]:
    print(coeffs, "->", solve_quadratic(*coeffs))
```

**9.** Solve each equation with the formula. Then check each root by
substituting it back.

- (a) $x^2 - 5x + 6 = 0$
- (b) $2x^2 + 3x - 2 = 0$
- (c) $x^2 - 6x + 9 = 0$
- (d) $x^2 + x + 1 = 0$

<details class="dl-answer"><summary>answer</summary>

(a) 2 and 3. (b) 0.5 and −2. (c) 3, repeated. (d) no real roots.

For (d) the discriminant is $1 - 4 = -3$, which is negative. The
parabola $y = x^2 + x + 1$ sits completely above the $x$-axis. You can
confirm this by plotting it.

</details>

**10.** What does the discriminant tell you, before you calculate anything
else?

<details class="dl-answer"><summary>answer</summary>

It tells you how many real roots there are. Positive gives two, zero
gives one repeated root, and negative gives none.

On the graph, it tells you whether the parabola crosses the $x$-axis,
touches it, or misses it completely. If you find it first, you also avoid
taking the square root of a negative number. The formula gives that
error if you continue without checking.

</details>

**11.** Find the discriminant of each one, without solving:
$x^2 - 4x + 4$, $x^2 - 4x + 3$, $x^2 - 4x + 5$.

<details class="dl-answer"><summary>answer</summary>

0, 4 and −4.

Look at the constants: 4, 3, 5. The three parabolas are the same shape,
moved up or down. The first touches the $x$-axis, the second crosses it
twice, and the third misses it. The discriminant alone separates the
three cases.

</details>

**12.** Can you write `verify_roots(a, b, c, roots)`? It should
substitute each root back and show what each one gives.

<details class="dl-answer"><summary>answer</summary>

```python
def verify_roots(a, b, c, roots, tolerance=1e-9):
    """Check each root by substitution."""
    for r in roots:
        value = a * r * r + b * r + c
        near = "zero, within the tolerance" if abs(value) < tolerance else "not zero"
        print(f"  x = {r:<20} gives {value:<25} {near}")
```

You need the tolerance. Many quadratics give exact roots: $x^2 - 4x + 3$
gives 3.0 and 1.0, and both substitute to exactly zero. But
$3x^2 - 7x + 2$ gives a root of 0.3333333333333333, which substitutes to
`2.2e-16`. An exact test for zero would say that 0.3333333333333333 is
not a root, when it is one, apart from rounding.

The interesting case is $x^2 - 200000x + 1$, from the next problem. Its
small root substitutes to about `1.1e-6`. That is far too large to be
normal rounding error. Here the tolerance shows something useful. It
tells you that the root itself is not accurate.

</details>

**13.** Solve $x^2 - 200000x + 1 = 0$ with the formula. Then check both
roots.

<details class="dl-answer"><summary>answer</summary>

The roots are about 199999.999995 and 0.000005. The formula loses
accuracy on the small one.

To get the small root, `(-b - sqrt(d)) / (2a)` subtracts two numbers
that are almost equal, and nearly all the useful digits cancel out. The
standard fix has two steps. First, find the large root, which has no
such subtraction. Then get the small root from a fact about quadratics:
the two roots multiply to give $\frac{c}{a}$.

```python
big = (-b - math.sqrt(d)) / (2 * a) if b > 0 else (-b + math.sqrt(d)) / (2 * a)
small = c / (a * big)
```

The formula is exact as mathematics. Computer arithmetic is not exact,
so the result can lose accuracy.

</details>

## Inequalities

**14.** Solve each inequality.

- (a) $3x - 6 > 0$
- (b) $-2x + 4 \ge 0$
- (c) $5 - x < 2$

<details class="dl-answer"><summary>answer</summary>

(a) $x > 2$. (b) $x \le 2$. (c) $x > 3$.

In (b) and (c), we divide or multiply by a negative number, and that
*flips* the inequality. In (c): $5 - x < 2$ gives $-x < -3$, and
multiplying by $-1$ gives $x > 3$. This is the one rule in this topic
that you need to remember. Most lost marks come from it.

</details>

**15.** Solve $x^2 - 5x + 6 > 0$.

<details class="dl-answer"><summary>answer</summary>

$x < 2$ or $x > 3$.

The roots are 2 and 3, and the parabola opens upwards (the $x^2$ term is
positive). So the curve is above the $x$-axis outside the roots, and
below it between them. A quick sketch is faster and more reliable than
any rule about signs.

Notice that the answer is two separate ranges. The solution set of a
quadratic inequality is often in two pieces. A linear inequality's
solution set never is.

</details>

**16.** Solve $x^2 < 9$.

<details class="dl-answer"><summary>answer</summary>

$-3 < x < 3$.

The answer is not $x < 3$. Squaring loses the sign, so both roots, $-3$
and 3, matter. For example, $-4 < 3$, but $(-4)^2 = 16$, which is not
less than 9.

</details>

## Simultaneous equations

**17.** Solve these simultaneous equations.

$$2x + y = 11$$
$$x - y = 1$$

<details class="dl-answer"><summary>answer</summary>

$x = 4$, $y = 3$.

Adding the two equations eliminates $y$ straight away: $3x = 12$, so
$x = 4$. Then $4 - y = 1$, so $y = 3$.

Check both equations: $8 + 3 = 11$ and $4 - 3 = 1$. It matters that you
check *both*. The usual mistake is a pair of values that makes one
equation true and not the other. It looks exactly like a solution until
you substitute.

</details>

**18.** Solve these simultaneous equations.

$$4x + 3y = 18$$
$$2x - y = 4$$

<details class="dl-answer"><summary>answer</summary>

$x = 3$, $y = 2$.

This time we use substitution: we rearrange one equation, and put it
into the other.

1. From the second equation, $y = 2x - 4$.
2. Substitute that into the first: $4x + 3(2x - 4) = 18$, so
   $4x + 6x - 12 = 18$, so $10x = 30$ and $x = 3$.
3. Then $y = 2(3) - 4 = 2$.

Check both equations: $12 + 6 = 18$ and $6 - 2 = 4$.

</details>

**19.** Each linear equation in $x$ and $y$ has a straight line as its
graph. What does it mean for those lines when two simultaneous linear
equations have no solution?

<details class="dl-answer"><summary>answer</summary>

The two lines are parallel and different. They have the same steepness
(the same slope) but cross the $y$-axis at different places, so they
never meet.

| Solutions | The two lines |
|---|---|
| exactly one | cross at one point |
| none | are parallel, and never meet |
| infinitely many | are the same line, drawn twice |

These are the only three possibilities for two straight lines. That is
why a pair of linear equations can never have exactly two solutions.

</details>

**20.** Where do $y = x^2$ and $y = x + 6$ meet?

<details class="dl-answer"><summary>answer</summary>

At $(-2, 4)$ and $(3, 9)$.

Where they meet, both have the same $y$. So set them equal:
$x^2 = x + 6$, which gives $x^2 - x - 6 = 0$. This factorises as
$(x - 3)(x + 2)$, so $x = 3$ or $x = -2$. Then $y = x^2$ gives 9 and 4.

A line and a parabola meet at two points, at one point, or not at all.
The discriminant of this equation tells you which.

</details>

## Putting it together

**21.** A rectangular garden has a perimeter of 34 m and an area of
60 m². How long and how wide is it?

<details class="dl-answer"><summary>answer</summary>

12 m by 5 m.

1. The perimeter gives $2(l + w) = 34$, so $l + w = 17$.
2. The area gives $lw = 60$.
3. Substitute $w = 17 - l$ into the second: $l(17 - l) = 60$, which
   rearranges to $l^2 - 17l + 60 = 0$.
4. This factorises as $(l - 12)(l - 5)$, so $l = 12$ or $l = 5$. The
   other side is then 5 or 12.

Check both conditions: $2(12 + 5) = 34$ and $12 \times 5 = 60$.

Many people first try 10 by 7, because 34 and 60 both seem to point to
it. Its perimeter is 34, but its area is 70. A pair of values that
meets only one condition is not a solution.

</details>

**22.** A ball is thrown straight up at 20 m/s. Its height after $t$
seconds is $h = 20t - 4.9t^2$. When is it at a height of 15 m?

<details class="dl-answer"><summary>answer</summary>

At about 0.99 s on the way up and about 3.09 s on the way down.

Set $h = 15$, so $15 = 20t - 4.9t^2$. Then add $4.9t^2$ to both sides
and take $20t$ from both sides: $4.9t^2 - 20t + 15 = 0$.
The discriminant is $400 - 294 = 106$, so the roots are
$t = \frac{20 \pm \sqrt{106}}{9.8}$.

There are two answers, and both make sense. Often a quadratic from a
real problem has one root you want and one you must think about. Here
you want them both. The ball passes 15 m once going up and once coming
down.

</details>
