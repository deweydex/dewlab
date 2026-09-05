---
title: "Cracking Equations — Practice"
slug: cracking-equations-practice
practice_for: cracking-equations
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
---

# Cracking Equations — Practice

Answers are folded. Every root you find can be checked by substituting it back, and there is no excuse for a wrong answer surviving on this page — put it back in and see whether you get zero.

The factorising and quadratic problems are adapted from the Mathematics repository's factoring worksheet.

## Linear Equations

```python exec
id: linear-equations-1
def solve_linear(a, b):
    """Solve ax + b = 0."""
    if a == 0:
        return "no unique solution" if b else "every number"
    return -b / a


print(solve_linear(3, -12), solve_linear(0, 5), solve_linear(0, 0))
```

**1.** Solve each.

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

Expand: $3x - 6 + 4 = 2x + 10$, so $3x - 2 = 2x + 10$, so $x = 12$.

Check by substituting: left is $3(10) + 4 = 34$, right is $2(17) = 34$.

</details>

**3.** What happens with $2x + 3 = 2x + 5$? And with $2x + 3 = 2x + 3$?

<details class="dl-answer"><summary>answer</summary>

The first has no solution — it reduces to $3 = 5$. The second is true for every x.

Both cases arrive as $0x = $ something, which is why `solve_linear` has to check for `a == 0` before dividing. An equation with no solutions and an equation with infinitely many look identical up to the last step.

</details>

## Quadratics by Factorising

**4.** Factorise.

- (a) $x^2 + 7x + 12$
- (b) $x^2 + 9x + 20$
- (c) $x^2 - 10x + 24$
- (d) $x^2 + 2x - 15$

<details class="dl-answer"><summary>answer</summary>

(a) $(x + 3)(x + 4)$. (b) $(x + 4)(x + 5)$. (c) $(x - 4)(x - 6)$. (d) $(x + 5)(x - 3)$.

Two numbers that multiply to the constant and add to the middle coefficient. When the constant is negative, as in (d), the two numbers have opposite signs.

</details>

**5.** Factorise the special patterns.

- (a) $x^2 - 49$
- (b) $x^2 - 100$
- (c) $x^2 + 6x + 9$
- (d) $x^2 - 14x + 49$
- (e) $4x^2 - 25$

<details class="dl-answer"><summary>answer</summary>

(a) $(x - 7)(x + 7)$. (b) $(x - 10)(x + 10)$. (c) $(x + 3)^2$. (d) $(x - 7)^2$. (e) $(2x - 5)(2x + 5)$.

The difference of two squares and the perfect square are worth recognising on sight, because they turn up constantly and they are the two cases where hunting for factor pairs is a waste of time.

</details>

**6.** Factorise $x^2 + 4$.

<details class="dl-answer"><summary>answer</summary>

It does not factorise over the real numbers.

A *sum* of squares has no real factorisation, unlike a difference. Over the complex numbers it is $(x - 2i)(x + 2i)$, which is what *When There Is No Answer* is about.

</details>

**7.** Take the common factor out first, then factorise.

- (a) $2x^2 + 10x + 12$
- (b) $3x^2 - 27$
- (c) $5x^2 - 5x - 30$

<details class="dl-answer"><summary>answer</summary>

(a) $2(x + 2)(x + 3)$. (b) $3(x - 3)(x + 3)$. (c) $5(x - 3)(x + 2)$.

Taking the common factor out first makes each of these an easy case. Attacking (c) directly means hunting for numbers multiplying to −150, which is possible and unpleasant.

</details>

**8.** Factorise $2x^2 + 7x + 3$, where the leading coefficient is not 1.

<details class="dl-answer"><summary>answer</summary>

$(2x + 1)(x + 3)$.

Find two numbers multiplying to $2 \times 3 = 6$ and adding to 7 — that is 6 and 1. Split the middle: $2x^2 + 6x + x + 3$, then group: $2x(x + 3) + 1(x + 3)$.

Or use the formula and work backwards from the roots, which is what a computer does and what you should do when the numbers are ugly.

</details>

## The Quadratic Formula

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

**9.** Solve with the formula, and check each root by substitution.

- (a) $x^2 - 5x + 6 = 0$
- (b) $2x^2 + 3x - 2 = 0$
- (c) $x^2 - 6x + 9 = 0$
- (d) $x^2 + x + 1 = 0$

<details class="dl-answer"><summary>answer</summary>

(a) 2 and 3. (b) 0.5 and −2. (c) 3, repeated. (d) no real roots.

For (d) the discriminant is $1 - 4 = -3$. The parabola sits entirely above the axis, which you can confirm by plotting it.

</details>

**10.** What does the discriminant tell you before you compute anything else?

<details class="dl-answer"><summary>answer</summary>

How many real roots there are: positive gives two, zero gives one repeated, negative gives none.

Geometrically it is asking whether the parabola crosses the axis, touches it, or misses it entirely. Computing it first also saves taking the square root of a negative number, which is the error the formula produces if you charge ahead.

</details>

**11.** Find the discriminant of each without solving: $x^2 - 4x + 4$, $x^2 - 4x + 3$, $x^2 - 4x + 5$.

<details class="dl-answer"><summary>answer</summary>

0, 4, and −4.

Same parabola shifted up by one each time: it touches the axis, then crosses it twice, then misses. Three cases from one number.

</details>

**12.** Write `verify_roots(a, b, c, roots)` that substitutes each root back and reports pass or fail.

<details class="dl-answer"><summary>answer</summary>

```python
def verify_roots(a, b, c, roots, tolerance=1e-9):
    """Check each root by substitution."""
    for r in roots:
        value = a * r * r + b * r + c
        verdict = "PASS" if abs(value) < tolerance else "FAIL"
        print(f"  x = {r:<20} gives {value:<25} {verdict}")
```

The tolerance is not optional. Plenty of quadratics come out exactly — $x^2 - 4x + 3$ gives 3.0 and 1.0, and both substitute to a clean zero — but $3x^2 - 7x + 2$ gives a root of 0.3333333333333333, which substitutes to `2.2e-16`. An exact comparison marks that correct answer wrong.

The interesting case is $x^2 - 200000x + 1$ from the next problem, where the small root substitutes to about `1.1e-6`. That is far too large to be rounding noise, and the tolerance is doing its real job there: telling you the root is not accurate, rather than telling you the arithmetic is.

</details>

**13.** Solve $x^2 - 200000x + 1 = 0$ with the formula, then check both roots.

<details class="dl-answer"><summary>answer</summary>

The roots are about 199999.999995 and 0.000005, and the small one is where the formula loses accuracy.

`(-b - sqrt(d)) / (2a)` subtracts two nearly equal numbers, and nearly all the significant digits cancel. The standard fix is to compute the large root that way and get the small one from the fact that the roots multiply to $c/a$:

```python
big = (-b - math.sqrt(d)) / (2 * a) if b > 0 else (-b + math.sqrt(d)) / (2 * a)
small = c / (a * big)
```

The formula is exactly right as mathematics and imperfect as arithmetic, which is a distinction worth keeping.

</details>

## Inequalities

**14.** Solve each.

- (a) $3x - 6 > 0$
- (b) $-2x + 4 \ge 0$
- (c) $5 - x < 2$

<details class="dl-answer"><summary>answer</summary>

(a) $x > 2$. (b) $x \le 2$. (c) $x > 3$.

In (b) and (c), dividing or multiplying by a negative number *flips* the inequality. That is the one rule in this topic that has to be remembered rather than derived, and it is where nearly all the marks are lost.

</details>

**15.** Solve $x^2 - 5x + 6 > 0$.

<details class="dl-answer"><summary>answer</summary>

$x < 2$ or $x > 3$.

The roots are 2 and 3, and the parabola opens upwards, so it is above the axis outside the roots and below them between. Sketching it is faster and more reliable than any rule about signs.

Note the answer is two separate ranges. An inequality involving a quadratic often has a disconnected solution set, which a linear one never does.

</details>

**16.** Solve $x^2 < 9$.

<details class="dl-answer"><summary>answer</summary>

$-3 < x < 3$.

Not $x < 3$. Squaring loses the sign, so both roots matter — and $(-4)^2 = 16$, which is not less than 9.

</details>

## Simultaneous Equations

**17.** Solve.

$$2x + y = 11$$
$$x - y = 1$$

<details class="dl-answer"><summary>answer</summary>

$x = 4$, $y = 3$.

Adding the two equations eliminates y directly: $3x = 12$.

Check both: $8 + 3 = 11$ and $4 - 3 = 1$. Checking *both* is the point — a value satisfying one equation and not the other is the usual failure.

</details>

**18.** Solve.

$$4x + 3y = 18$$
$$2x - y = 4$$

<details class="dl-answer"><summary>answer</summary>

$x = 3$, $y = 2$.

From the second equation, $y = 2x - 4$. Substituting into the first: $4x + 6x - 12 = 18$, so $10x = 30$.

Check both: $12 + 6 = 18$ and $6 - 2 = 4$. Checking *both* is the point — a pair that satisfies one equation and not the other is the usual failure, and it looks exactly like a right answer until you substitute.

</details>

**19.** What does it mean, geometrically, when two simultaneous linear equations have no solution?

<details class="dl-answer"><summary>answer</summary>

The two lines are parallel and distinct — same slope, different intercept, so they never meet.

Infinitely many solutions means they are the same line drawn twice. One solution means they cross once. Those are the only three possibilities for two straight lines, which is why a pair of linear equations can never have exactly two solutions.

</details>

**20.** Where do $y = x^2$ and $y = x + 6$ meet?

<details class="dl-answer"><summary>answer</summary>

At $(-2, 4)$ and $(3, 9)$.

Setting them equal gives $x^2 - x - 6 = 0$, which factorises as $(x - 3)(x + 2)$.

A line and a parabola meet at two points, one point, or none — and which of those it is, is the discriminant again.

</details>

## Putting It Together

**21.** A rectangular garden has a perimeter of 34 m and an area of 60 m². Find its dimensions.

<details class="dl-answer"><summary>answer</summary>

12 m by 5 m.

The perimeter gives $l + w = 17$ and the area gives $lw = 60$. Substituting $w = 17 - l$ turns the second into $l^2 - 17l + 60 = 0$, which factorises as $(l - 12)(l - 5)$.

Check both conditions: $2(12 + 5) = 34$ and $12 \times 5 = 60$.

10 by 7 is the answer people reach for, because 34 and 60 both look like they suggest it. Its perimeter is right and its area is 70. One condition satisfied is not a solution.

</details>

**22.** A ball is thrown up at 20 m/s. Its height after t seconds is $h = 20t - 4.9t^2$. When is it at 15 m?

<details class="dl-answer"><summary>answer</summary>

At about 0.99 s on the way up and about 3.09 s on the way down.

$4.9t^2 - 20t + 15 = 0$, discriminant $400 - 294 = 106$, roots $(20 \pm \sqrt{106})/9.8$.

Two answers, both physically real. A quadratic from a physical problem usually has one root you want and one you have to think about — and here you want them both.

</details>
