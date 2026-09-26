---
title: "Mixed problems: algebra and functions"
practice_across:
  - numbers-and-their-families
  - expressions-come-alive
  - cracking-equations
  - rearranging-formulae
  - complex-roots
  - drawing-functions
  - parabolas
year: "2026-2027"
version: 2026.08.23.1
---

# Mixed problems: algebra and functions

Each problem here needs at least two of the algebra tutorials. Many of
them need a picture as well as a calculation. Nothing here is harder
than what those tutorials covered. The hard part is new: nobody tells
you which tool to use. Choosing the tool is part of the problem.

Each answer is hidden in a fold under its question. Some problems also
have a hint fold, to open first if you get stuck. When a problem can be
done both with algebra and with a graph, try it both ways. The second
way is your check.

## Tools

This cell defines two helpers:

- `draw(f)` plots a function. You can pass `low` and `high` to choose
  the range of $x$, and `label` to name the curve. To draw two curves on
  one set of axes, pass the axes from the first call as `ax`:
  `ax = draw(f)`, then `draw(g, ax=ax)`.
- `roots(a, b, c)` gives the real roots of $ax^2 + bx + c = 0$, using
  the quadratic formula.

The last two lines try them on $x^2 - 3x - 4$. Its roots are 4 and −1.

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

## Expand, factorise, solve

**1.** Take $(2x - 3)(x + 5)$.

1. Expand it.
2. Set the result equal to zero, and solve.
3. Check your roots by factorising back.

<details class="dl-answer"><summary>answer</summary>

Expanded, it is $2x^2 + 7x - 15$. The roots are 1.5 and −5.

Factorising back gives $2(x - 1.5)(x + 5)$, which multiplies out to the
original.

The leading 2 is the part people often drop. $(x - 1.5)(x + 5)$ on its
own is $x^2 + 3.5x - 7.5$. That is half of what we wanted.

</details>

**2.** For what value of $k$ does $x^2 + kx + 9$ have exactly one root?

<details class="dl-answer"><summary>answer</summary>

$k = 6$ or $k = -6$.

The discriminant, $k^2 - 36$, must be zero. There are two answers,
because the parabola can touch the axis on either side of the origin:
$(x + 3)^2$ touches at −3, and $(x - 3)^2$ touches at 3.

Plot both, and you will see the symmetry at once.

</details>

**3.** Find a quadratic whose roots are 2 and −7.

<details class="dl-answer"><summary>answer</summary>

$x^2 + 5x - 14$, or any multiple of it.

It comes from $(x - 2)(x + 7)$. There are infinitely many answers. For
example, $3x^2 + 15x - 42$ has the same roots. Multiplying a polynomial
by a number does not move the places where it crosses zero.

For $ax^2 + bx + c$, the sum of the roots is $-\dfrac{b}{a}$ and their
product is $\dfrac{c}{a}$. Here the sum is $2 + (-7) = -5$ and the
product is $-14$. That gives a quick way to build a quadratic, and an
even quicker way to check one.

</details>

**4.** A quadratic passes through $(0, 6)$ and has roots at 1 and 3.
What is it?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The roots tell you the shape. Start by writing a quadratic that has
   roots 1 and 3, in factorised form. Do not worry about its size yet.
2. Multiply that out, or leave it factorised. Either works for the next
   step.
3. Now use the third fact. What does "passes through $(0, 6)$" let you
   substitute?
4. Whatever number your factorised form gives at $x = 0$, you need it to
   be 6.

**Think about:** the two roots fixed the shape, and the one point fixed
the size. That is three facts for three coefficients. Count them, and
you can see that it had to work.

**Try this next:** find the quadratic with roots 1 and 3 that passes
through $(2, -4)$. What does the sign of the scale factor do to the
picture?

</details>

<details class="dl-answer"><summary>answer</summary>

$2x^2 - 8x + 6$.

Start from $a(x - 1)(x - 3)$, which is $a(x^2 - 4x + 3)$. At $x = 0$
that is $3a$. We need 6, so $a = 2$.

The two roots fix the shape, and one more point fixes the size. That is
three pieces of information for three coefficients, which is exactly
the right number.

</details>

## Rearranging

**5.** Make $r$ the subject of $V = \pi r^2 h$.

<details class="dl-answer"><summary>answer</summary>

$r = \sqrt{\dfrac{V}{\pi h}}$.

Take the positive root only, because a radius is a length. That rule
comes from the situation, and not from the algebra. The algebra will
not remind you of it.

</details>

**6.** Make $x$ the subject of $y = \dfrac{2x + 1}{x - 3}$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The unknown is on the bottom of a fraction, so the first move is to
   get it off the bottom. Multiply both sides by $x - 3$.
2. Expand, and look at where $x$ now appears. It appears twice.
3. Move every term that contains $x$ to one side, and everything else to
   the other side.
4. Now take $x$ out as a common factor on that side, and divide.

**Think about:** step 4 is only possible because you gathered the $x$
terms first. Whenever the unknown appears twice, gathering and then
factoring is the move to make.

**Try this next:** your answer is undefined at one value of $y$. Which
one? Then check that the original expression never produces that value.

</details>

<details class="dl-answer"><summary>answer</summary>

$x = \dfrac{3y + 1}{y - 2}$.

Multiply both sides by $x - 3$: $y(x - 3) = 2x + 1$. Expand:
$xy - 3y = 2x + 1$. Gather the $x$ terms: $xy - 2x = 3y + 1$. Factor:
$x(y - 2) = 3y + 1$. Then divide by $y - 2$.

The key move is to gather every $x$ on one side and factor it out. It is
the only move available when the unknown appears twice.

Notice that the result is undefined at $y = 2$. And the original never
produces 2: as $x$ grows, $\dfrac{2x + 1}{x - 3}$ gets closer and closer
to 2, but never reaches it. The rearranged formula carried that fact
across without being asked.

</details>

**7.** The compound interest formula is $A = P(1 + r)^n$. Here $P$ is the
amount you start with, $r$ is the yearly interest rate, and $A$ is the
amount after $n$ years.

1. Make $n$ the subject.
2. How long does €1,000 take to double at 5%?

<details class="dl-answer"><summary>answer</summary>

$n = \dfrac{\log(A/P)}{\log(1 + r)}$, and it takes about 14.2 years.

The unknown is in the power, so a logarithm is the only way to bring it
down. The base of the logarithm does not matter, as long as you use the
same base on the top and the bottom.

Doubling means $A/P = 2$, so $n = \dfrac{\log 2}{\log 1.05} \approx 14.2$.

The "rule of 72" is a quick estimate: divide 72 by the interest rate in
percent. It gives $72/5 \approx 14.4$. That is close enough to be
useful, and it comes from this same calculation.

</details>

**8.** Rearrange $\dfrac{1}{f} = \dfrac{1}{u} + \dfrac{1}{v}$ to make $v$
the subject. (This is the lens formula from physics.)

<details class="dl-answer"><summary>answer</summary>

$v = \dfrac{uf}{u - f}$.

First, $\dfrac{1}{v} = \dfrac{1}{f} - \dfrac{1}{u} = \dfrac{u - f}{uf}$.
Then turn both sides upside down.

Turning both sides upside down is safe here only because neither side
is zero. When $u = f$, the side $\dfrac{u - f}{uf}$ is zero, and the
lens forms no image. The algebra breaks down and the physics breaks
down at the same moment.

</details>

## Graphs

**9.** Sketch $y = x^2 - 4x + 3$ without plotting it.

1. Find its roots.
2. Find its vertex.
3. Find where it crosses the vertical axis.

<details class="dl-answer"><summary>answer</summary>

The roots are 1 and 3. The vertex is at $(2, -1)$. It crosses the
vertical axis at 3.

The vertex sits halfway between the roots, at
$x = -\dfrac{b}{2a} = \dfrac{4}{2} = 2$. There, $y = 4 - 8 + 3 = -1$.

Then plot it and check. Everything you predicted should be visible. If
the picture disagrees with you, the picture is right.

</details>

**10.** Where do $y = x^2 - 4$ and $y = 3x$ meet?

<details class="dl-answer"><summary>answer</summary>

At $(-1, -3)$ and $(4, 12)$.

Set them equal: $x^2 - 4 = 3x$, so $x^2 - 3x - 4 = 0$. That factorises
as $(x - 4)(x + 1) = 0$, so $x = 4$ or $x = -1$. Then $y = 3x$ gives
the $y$ values.

Every "where do these meet?" question is a "solve this equation"
question. The graph is how you check that you found all the answers.

</details>

**11.** For what values of $m$ does the line $y = mx + 1$ miss the
parabola $y = x^2$ completely?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. "Misses completely" means they never meet. Start by writing the
   equation for where they *do* meet.
2. Set them equal and bring everything to one side. You should have a
   quadratic in $x$.
3. A quadratic has no real solutions exactly when one particular
   quantity is negative. Which quantity?
4. Work out that quantity in terms of $m$. For what values of $m$ is it
   negative?

**Think about:** you should find that there are none. Before you trust
the algebra, sketch the parabola and a line through $(0, 1)$. Does the
picture agree?

**Try this next:** change the line to $y = mx - 1$ and do it again. Now
there is a range of $m$ that misses. Why does the sign of the
intercept change everything?

</details>

<details class="dl-answer"><summary>answer</summary>

There are none.

Setting them equal gives $x^2 - mx - 1 = 0$. Its discriminant is
$m^2 + 4$, which is positive for every real $m$. So the line always
crosses the parabola twice.

The $+1$ is the reason. A line through $(0, 1)$ starts *inside* the
parabola, and it cannot get out without crossing the sides. Change the
intercept to −1, and the answer becomes a range of $m$. That range is
worth working out.

</details>

**12.** Plot $y = x^2$, $y = x^3$ and $y = 2^x$ on one set of axes, from 0
to 10. Which one is largest, and where?

<details class="dl-answer"><summary>answer</summary>

$2^x$ is largest at first, up to about $x = 1.4$. Then $x^3$ is largest,
from about 1.4 to about 9.9. Just before 10, $2^x$ overtakes everything,
and it stays ahead for good.

At $x = 10$ the values are 100, 1000 and 1024. At $x = 20$ they are 400,
8000 and 1,048,576.

The exponential loses for nine units, and then wins by a factor of more
than a hundred. This is why people say that $2^x$ grows "asymptotically
faster": for large enough $x$, it is always ahead. Any finite piece of
the graph can mislead you about which one grows faster.

</details>

## Complex roots

**13.** Solve $x^2 + 4x + 13 = 0$.

<details class="dl-answer"><summary>answer</summary>

$x = -2 \pm 3i$.

The discriminant is $16 - 52 = -36$, and $\sqrt{-36} = 6i$. So
$x = \dfrac{-4 \pm 6i}{2} = -2 \pm 3i$.

The two roots are conjugates: they have the same real part, and
opposite imaginary parts. That is always true when the coefficients are
real.

If you plot the parabola, you will see it sits completely above the
axis. Its lowest point is at $(-2, 9)$.

</details>

**14.** A quadratic has roots $3 + 2i$ and $3 - 2i$. What is it?

<details class="dl-answer"><summary>answer</summary>

$x^2 - 6x + 13$.

The sum of the roots is 6. Their product is
$(3 + 2i)(3 - 2i) = 9 - 4i^2 = 9 + 4 = 13$.

In the sum, the imaginary parts cancel. In the product, they multiply
to give a real number. That is how a quadratic with real coefficients
can have complex roots at all.

</details>

**15.** Check that $3 + 2i$ satisfies the quadratic you just found, by
substituting it in.

<details class="dl-answer"><summary>answer</summary>

First, $(3 + 2i)^2 = 9 + 12i + 4i^2 = 5 + 12i$. Then:

$$5 + 12i - 6(3 + 2i) + 13 = 5 + 12i - 18 - 12i + 13 = 0$$

```python
z = complex(3, 2)
print(z ** 2 - 6 * z + 13)
```

Python prints `0j`, which is zero.

Notice the $4i^2$ becoming $-4$. That one substitution is the whole
difference between complex arithmetic and ordinary algebra.

</details>

## Longer ones

**16.** A farmer builds a rectangular pen against a wall, so only three
sides need a fence. There is 60 m of fence. What size of pen gives the
largest area?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw it. Three sides have a fence, and one side is the wall. Which
   two of the three fenced sides are equal?
2. Call the two equal sides $x$. If the total fence is 60 m, how long is
   the third side?
3. Write the area as the product of those two lengths. It is a quadratic
   in $x$.
4. A quadratic's highest point is at $x = -\dfrac{b}{2a}$. You do not
   need calculus for this one.

**Think about:** with no wall, the best rectangle for a fixed perimeter
is a square. The wall changes the answer. Why?

**Try this next:** what if the wall is only 20 m long, so the side along
it can be at most 20 m? Where is the best pen now?

</details>

<details class="dl-answer"><summary>answer</summary>

30 m along the wall and 15 m out from it. That gives an area of
450 m².

If the two sides out from the wall are $x$, the side along the wall is
$60 - 2x$. So the area is $A = x(60 - 2x) = -2x^2 + 60x$.

That is a parabola opening downwards. Its peak is at
$x = -\dfrac{b}{2a} = -\dfrac{60}{2 \times (-2)} = 15$. Then the side
along the wall is $60 - 30 = 30$, and the area is $15 \times 30 = 450$.

Compare a square pen against the wall, 20 m by 20 m. Its three fenced
sides also use 60 m of fence, and it encloses 400 m². So the best pen is
50 m² bigger than the square one. With a wall, the best shape is no
longer a square, and that is the interesting part.

</details>

**17.** A ball is thrown upwards at 15 m/s from a ledge 2 m high. Its
height after $t$ seconds is $h = 2 + 15t - 4.9t^2$ metres.

1. When does it land?
2. How high does it get?
3. When is it above 10 m?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. There are three questions, and each one solves for something
   different. Take them one at a time.
2. "Lands" means the height is back to zero. That is a quadratic to
   solve. It has two roots, and one of them is in the past.
3. The peak of a downward parabola is at $t = -\dfrac{b}{2a}$. Find the
   time first, then substitute it to find the height.
4. "Above 10 m" means $h > 10$. Bring the 10 across, and solve the
   quadratic you get.

**Think about:** for the last part, the parabola opens downwards. So the
times above 10 m are *between* the two roots, and not outside them. A
sketch settles which.

**Try this next:** how long is the ball above 12 m? Above 14 m? At what
height does the answer become "never"?

</details>

<details class="dl-answer"><summary>answer</summary>

It lands at about 3.19 s. It reaches its peak of about 13.48 m at about
1.53 s. It is above 10 m from about 0.69 s to about 2.37 s.

**Landing:** solve $-4.9t^2 + 15t + 2 = 0$ and take the positive root,
about 3.19.

**Peak:** $t = -\dfrac{b}{2a} = \dfrac{15}{9.8} \approx 1.531$. The
height there is about 13.48 m.

**Above 10 m:** $2 + 15t - 4.9t^2 > 10$ becomes
$-4.9t^2 + 15t - 8 > 0$. The roots of $-4.9t^2 + 15t - 8 = 0$ are
about 0.69 and 2.37. The ball is above 10 m *between* those times,
because the parabola opens downwards. Getting that direction right is
the important part.

</details>

**18.** €500 is invested at 4% interest, compounded every year.

1. Write the balance after $n$ years as a function.
2. Plot it next to the straight line for the same money at 4% simple
   interest. (Simple interest pays 4% of the original €500 every year,
   so it adds €20 a year.)
3. In which year does the gap between them first go over €100?

<details class="dl-answer"><summary>answer</summary>

Compound: $500 \times 1.04^n$. Simple: $500(1 + 0.04n)$.

The gap first goes over €100 in year 15. At $n = 15$ it is €100.47. (At
$n = 14$ it is €85.84.)

For the first few years, the two are nearly the same. That is why simple
interest is a good estimate over a short time, and a bad one over a
working life. The gap keeps growing, with no limit. By year 50 it is
over €2,000.

</details>

**19.** Which of these can you solve exactly by hand? Which ones need a
picture or a numerical method?

- (a) $x^2 - 5x + 6 = 0$
- (b) $x^3 - 2x - 1 = 0$
- (c) $2^x = 10$
- (d) $x + \sin x = 1$
- (e) $x^5 - x - 1 = 0$

<details class="dl-answer"><summary>answer</summary>

(a) It factorises: $(x - 2)(x - 3) = 0$, so the roots are 2 and 3.

(b) It factorises, with some effort. $x = -1$ is a root, so $(x + 1)$ is
a factor, and the cubic is $(x + 1)(x^2 - x - 1)$. The other two roots
come from $x^2 - x - 1 = 0$. They are the golden ratio,
$\dfrac{1 + \sqrt{5}}{2}$, and its conjugate, $\dfrac{1 - \sqrt{5}}{2}$.

(c) Use a logarithm: $x = \log_2 10 \approx 3.32$.

(d) There is no exact form. The answer is about 0.511. You can find it
by plotting, or by *bisection*: halving an interval that contains the
answer, again and again. That is the same idea as binary search in
[Searching a list: linear and binary search](tutorial:finding-things).

(e) There is no exact form, and this can be proved. The answer is about
1.1673.

That last fact is worth knowing. Quadratics have a formula. Cubics and
quartics (degree four) also have formulas, but very long ones. From
degree five, there is no general formula using roots such as
$\sqrt{\ }$. In 1824, Abel proved that no such formula exists, so the
reason is not that nobody has looked hard enough.

</details>
