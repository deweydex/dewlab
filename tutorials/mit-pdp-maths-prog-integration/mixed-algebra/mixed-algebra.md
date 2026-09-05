---
title: "Mixed Problems — Algebra and Functions"
slug: mixed-algebra
practice_across:
  - numbers-and-their-families
  - expressions-come-alive
  - cracking-equations
  - rearranging-formulae
  - complex-roots
  - drawing-functions
  - parabolas
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
---

# Mixed Problems — Algebra and Functions

Each of these needs at least two of the algebra tutorials, and several want a picture as well as a calculation. Nothing here is harder than what those tutorials covered; what is harder is that nobody is telling you which one to use.

Answers are folded. Where a problem can be done algebraically and graphically, do it both ways — the second is the check.

## Tools

```python exec
id: tools-1
import math
import matplotlib.pyplot as plt


def draw(f, low=-6, high=6, steps=400, label=None, ax=None):
    xs = [low + (high - low) * i / steps for i in range(steps + 1)]
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend(fontsize=8)
    return ax


def roots(a, b, c):
    d = b * b - 4 * a * c
    if d < 0:
        return ()
    if d == 0:
        return (-b / (2 * a),)
    return ((-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a))


draw(lambda x: x ** 2 - 3 * x - 4, label="x^2 - 3x - 4")
print(roots(1, -3, -4))
```

## Expand, Factorise, Solve

**1.** Expand $(2x - 3)(x + 5)$, then solve the result equal to zero, then check the roots by factorising back.

<details class="dl-answer"><summary>answer</summary>

$2x^2 + 7x - 15$. Roots 1.5 and −5.

Factorising back gives $2(x - 1.5)(x + 5)$, which multiplies out to the original. The leading 2 is the part people drop: $(x - 1.5)(x + 5)$ alone is $x^2 + 3.5x - 7.5$, half of what was wanted.

</details>

**2.** For what value of $k$ does $x^2 + kx + 9$ have exactly one root?

<details class="dl-answer"><summary>answer</summary>

$k = 6$ or $k = -6$.

The discriminant $k^2 - 36$ must be zero. Two answers, because the parabola can touch the axis from either side of the origin: $(x+3)^2$ and $(x-3)^2$.

Plot both and the symmetry is immediate.

</details>

**3.** Find a quadratic whose roots are 2 and −7.

<details class="dl-answer"><summary>answer</summary>

$x^2 + 5x - 14$, or any multiple of it.

$(x - 2)(x + 7)$. There are infinitely many answers — $3x^2 + 15x - 42$ has the same roots — because scaling a polynomial does not move where it crosses zero.

The sum of the roots is $-b/a$ and their product is $c/a$, which is a quick way to build one and a quicker way to check one.

</details>

**4.** A quadratic passes through $(0, 6)$ and has roots at 1 and 3. Find it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Knowing the roots tells you the shape. Start by writing the quadratic that has roots 1 and 3, in factorised form, without worrying about the scale.
2. Multiply that out, or leave it factorised — either works for the next step.
3. Now use the third fact. What does "passes through $(0, 6)$" let you substitute?
4. Whatever number your factorised form gives at $x = 0$, you need it to be 6.

**Think about:** two roots fixed the shape and one point fixed the size. Three facts, three coefficients — count them and see that it had to work.

**Try this next:** find the quadratic with roots 1 and 3 passing through $(2, -4)$. What does the sign of the scale factor do to the picture?

</details>

<details class="dl-answer"><summary>answer</summary>

$2x^2 - 8x + 6$.

Start from $a(x-1)(x-3)$, which is $a(x^2 - 4x + 3)$. At $x = 0$ that is $3a$, and we need 6, so $a = 2$.

Two roots fix the shape; one more point fixes the scale. Three pieces of information for three coefficients, which is exactly the right count.

</details>

## Rearranging

**5.** Make $r$ the subject of $V = \pi r^2 h$.

<details class="dl-answer"><summary>answer</summary>

$r = \sqrt{\dfrac{V}{\pi h}}$.

Positive root only, because a radius is a length. That restriction comes from the situation rather than from the algebra, and the algebra will not remind you.

</details>

**6.** Make $x$ the subject of $y = \dfrac{2x + 1}{x - 3}$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The unknown is on the bottom of a fraction, so the first move is always to get it off there. Multiply both sides by $x - 3$.
2. Expand, and look at where $x$ now appears. There are two of them.
3. Get every term containing $x$ onto one side and everything else onto the other.
4. Now factor $x$ out of that side, and divide.

**Think about:** step 4 is only possible because you gathered first. Whenever the unknown appears twice, gathering and factoring is the move.

**Try this next:** your answer is undefined at one value of $y$. Work out which, then check that the original expression never produces that value.

</details>

<details class="dl-answer"><summary>answer</summary>

$x = \dfrac{3y + 1}{y - 2}$.

Multiply up: $y(x - 3) = 2x + 1$, so $xy - 3y = 2x + 1$, so $x(y - 2) = 3y + 1$.

Gathering every x on one side and factoring it out is the move, and it is the only one available when the unknown appears twice.

Notice the result is undefined at $y = 2$ — and the original never produces 2, because $\frac{2x+1}{x-3}$ approaches 2 without reaching it. The rearrangement carried that fact across without being asked.

</details>

**7.** The compound interest formula is $A = P(1 + r)^n$. Make $n$ the subject, and find how long €1,000 takes to double at 5%.

<details class="dl-answer"><summary>answer</summary>

$n = \dfrac{\log(A/P)}{\log(1 + r)}$, and about 14.2 years.

The unknown is in the exponent, so a logarithm is the only way down. Which base does not matter, as long as both are the same.

The rule of 72 says 72/5 ≈ 14.4, which is close enough to be useful and comes from exactly this calculation.

</details>

**8.** Rearrange $\frac{1}{f} = \frac{1}{u} + \frac{1}{v}$ to make $v$ the subject.

<details class="dl-answer"><summary>answer</summary>

$v = \dfrac{uf}{u - f}$.

$\frac{1}{v} = \frac{1}{f} - \frac{1}{u} = \frac{u - f}{uf}$, then invert both sides.

Inverting is safe here only because neither side is zero — and $u = f$ makes it zero, which is the case where the lens has no image to form. The algebra breaking down and the physics breaking down are the same event.

</details>

## Graphs

**9.** Sketch $y = x^2 - 4x + 3$ without plotting: find its roots, its vertex, and where it crosses the vertical axis.

<details class="dl-answer"><summary>answer</summary>

Roots 1 and 3; vertex at $(2, -1)$; crosses the vertical axis at 3.

The vertex sits halfway between the roots, at $x = -b/2a = 2$, and $y$ there is $4 - 8 + 3 = -1$.

Then plot it and check. Everything you predicted should be visible, and if the picture disagrees the picture is right.

</details>

**10.** Where do $y = x^2 - 4$ and $y = 3x$ meet?

<details class="dl-answer"><summary>answer</summary>

At $(-1, -3)$ and $(4, 12)$.

$x^2 - 3x - 4 = 0$, factorising as $(x-4)(x+1)$.

Every "where do these meet" question is a "solve this equation" question, and the graph is how you check you got them all.

</details>

**11.** For what values of $m$ does the line $y = mx + 1$ miss the parabola $y = x^2$ entirely?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. "Misses entirely" means they never meet. Start by writing the equation for where they *do* meet.
2. Set them equal and bring everything to one side. You should have a quadratic in $x$.
3. A quadratic has no real solutions exactly when one particular quantity is negative. Which?
4. Work out that quantity in terms of $m$, and ask for what values of $m$ it is negative.

**Think about:** you should find there are none. Before trusting the algebra, sketch the parabola and a line through $(0, 1)$ and see whether the picture agrees.

**Try this next:** change the line to $y = mx - 1$ and redo it. Now there is a range of $m$ that misses. Why does the sign of the intercept change everything?

</details>

<details class="dl-answer"><summary>answer</summary>

There are none.

Setting them equal gives $x^2 - mx - 1 = 0$, whose discriminant is $m^2 + 4$ — positive for every real m. The line always crosses twice.

The +1 is why. A line through $(0, 1)$ starts *inside* the parabola, and there is no way out that does not cross the sides. Change the intercept to −1 and the answer becomes a range of m, which is worth working out.

</details>

**12.** Plot $y = x^2$, $y = x^3$ and $y = 2^x$ on one pair of axes from 0 to 10. Which is largest where?

<details class="dl-answer"><summary>answer</summary>

$x^3$ leads from about 1.4 to about 9.9. $2^x$ is ahead below that, falls behind, and overtakes everything permanently just before 10.

At $x = 10$: 100, 1000, and 1024. At $x = 20$: 400, 8000, and 1,048,576.

The exponential losing for nine units and then winning by a factor of a thousand is the whole reason "asymptotically faster" is worth saying. Any finite piece of the graph can mislead you about which grows faster.

</details>

## Complex Roots

**13.** Solve $x^2 + 4x + 13 = 0$.

<details class="dl-answer"><summary>answer</summary>

$x = -2 \pm 3i$.

The discriminant is $16 - 52 = -36$, and $\sqrt{-36} = 6i$.

The two roots are conjugates — same real part, opposite imaginary parts — which is always true when the coefficients are real. Plotting the parabola shows it floating entirely above the axis, its lowest point at $(-2, 9)$.

</details>

**14.** A quadratic has roots $3 + 2i$ and $3 - 2i$. Find it.

<details class="dl-answer"><summary>answer</summary>

$x^2 - 6x + 13$.

Sum of roots 6, product $9 + 4 = 13$. The imaginary parts cancel in the sum and multiply into a real number in the product, which is why a real quadratic can have complex roots at all.

</details>

**15.** Verify that $(3 + 2i)$ satisfies the quadratic you just found, by substituting it in.

<details class="dl-answer"><summary>answer</summary>

$(3+2i)^2 = 9 + 12i + 4i^2 = 5 + 12i$. Then $5 + 12i - 6(3 + 2i) + 13 = 5 + 12i - 18 - 12i + 13 = 0$.

```python
z = complex(3, 2)
print(z ** 2 - 6 * z + 13)
```

Python prints `0j`, which is zero. Note the $4i^2$ becoming $-4$ — that single substitution is the entire difference between complex arithmetic and ordinary algebra.

</details>

## Longer Ones

**16.** A rectangular pen is built against a wall, so only three sides need fencing. With 60 m of fence, what dimensions give the largest area?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw it. Three sides are fenced and one is the wall — decide which of the three are equal.
2. Call the two equal sides $x$. If the total fence is 60, how long is the third side?
3. Write the area as a product of those two expressions. It is a quadratic in $x$.
4. A quadratic's highest point sits at $x = -b/2a$. You do not need calculus for this one.

**Think about:** without the wall, the best rectangle for a fixed perimeter is a square. The wall changes the answer. Why?

**Try this next:** what if the wall is only 20 m long, so the side along it cannot exceed 20? Where is the best pen now?

</details>

<details class="dl-answer"><summary>answer</summary>

30 m along the wall and 15 m out, giving 450 m².

If the sides out from the wall are $x$, the side along it is $60 - 2x$, so the area is $A = x(60 - 2x) = -2x^2 + 60x$. That is a parabola opening downwards, with its peak at $x = -b/2a = 15$.

A square pen — 20 by 20 — would use 60 m of fence on all four sides and enclose 400 m². The wall is worth 50 m² here, and the optimal shape is no longer a square, which is the interesting part.

</details>

**17.** A ball is thrown from a 2 m ledge at 15 m/s upwards. Its height is $h = 2 + 15t - 4.9t^2$. When does it land, how high does it get, and when is it above 10 m?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Three questions, three different things to solve for. Take them separately.
2. "Lands" means the height is back to zero. That is a quadratic to solve, and it has two roots — one of which is in the past.
3. The peak of a downward parabola is at $t = -b/2a$. Find the time first, then substitute for the height.
4. "Above 10 m" means $h > 10$, so bring the 10 across and solve the quadratic you get.

**Think about:** for the last part the parabola opens downwards, so the region above 10 m is *between* the two roots, not outside them. Sketching it settles which.

**Try this next:** how long is the ball above 12 m? Above 14 m? At what height does the answer become "never"?

</details>

<details class="dl-answer"><summary>answer</summary>

It lands at about 3.19 s, peaks at about 13.48 m at 1.53 s, and is above 10 m between about 0.69 s and 2.37 s.

Landing: solve $-4.9t^2 + 15t + 2 = 0$ and take the positive root.

Peak: $t = -b/2a = 15/9.8 \approx 1.531$, and $h$ there is about 13.48.

Above 10 m: solve $-4.9t^2 + 15t - 8 = 0$, giving 0.69 and 2.37 — and the ball is above 10 m *between* those, because the parabola opens downwards. That direction is the part worth getting right.

</details>

**18.** €500 is invested at 4% compounded annually. Write the balance as a function, plot it against a straight line for the same money at 4% simple interest, and say when the gap first exceeds €100.

<details class="dl-answer"><summary>answer</summary>

Compound: $500 \times 1.04^n$. Simple: $500(1 + 0.04n)$.

The gap first exceeds €100 in year 15 — at n = 15 it is €100.47.

For the first few years the two are nearly identical, which is why simple interest is a decent approximation over short periods and a bad one over a career. The gap grows without limit; by year 50 it is over €2,000.

</details>

**19.** Which of these can be solved exactly by hand, and which need a picture or a numerical method?

- (a) $x^2 - 5x + 6 = 0$
- (b) $x^3 - 2x - 1 = 0$
- (c) $2^x = 10$
- (d) $x + \sin x = 1$
- (e) $x^5 - x - 1 = 0$

<details class="dl-answer"><summary>answer</summary>

(a) Factorises: 2 and 3.

(b) Factorises, with effort: $x = -1$ is a root, so it divides into $(x+1)(x^2 - x - 1)$, and the rest is the golden ratio and its conjugate.

(c) A logarithm: $x = \log_2 10 \approx 3.32$.

(d) No exact form. About 0.511, found by plotting or by bisection.

(e) No exact form, and provably so — no formula in radicals exists for the general fifth-degree equation. About 1.1673.

That last fact is worth knowing. Quadratics have a formula, cubics and quartics have horrible ones, and from degree five there is none — not because nobody has found it, but because Abel proved in 1824 that there is not one to find.

</details>
