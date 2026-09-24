---
title: "The top of the curve: maximum and minimum — Practice"
practice_for: the-top-of-the-curve
year: "2026-2027"
version: 2026.09.24.1
---

# The top of the curve: maximum and minimum — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `vertex` from the
tutorial, `solve_quadratic` from
[Solving for x](tutorial:solving-for-x) and `evaluate` from
[Rules with letters in them](tutorial:rules-with-letters-in-them).

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: the-top-practice-warm-up
# Try things here
```

**1. Predict.** What does this line print? Is the point it gives a
maximum or a minimum?

```python
print(vertex(1, -4, 7))
```

<details class="dl-answer"><summary>answer</summary>

`(2.0, 3.0)`, and it is a minimum.

The $x$ of the vertex is $-\frac{b}{2a} = -\frac{-4}{2 \times 1} = 2$.
The height there is $2^2 - 4 \times 2 + 7 = 3$. The number in front of
$x^2$ is 1, which is positive, so the parabola opens upwards like a
valley, and the vertex is its lowest point.

</details>

**2. Predict.** One of these three rules has a maximum. Which one? Then
predict what `vertex` gives for it.

- $y = x^2 - 9$
- $y = 5 + 2x - x^2$
- $y = 0.5x^2 + 3x$

<details class="dl-answer"><summary>answer</summary>

$y = 5 + 2x - x^2$, because its $x^2$ has $-1$ in front of it. In the
order `vertex` wants, $a = -1$, $b = 2$ and $c = 5$:

```python
print(vertex(-1, 2, 5))
```

It prints `(1.0, 6.0)`. The highest the rule ever reaches is 6, at
$x = 1$.

</details>

**3. Make.** Complete the square for $x^2 + 10x$ by hand. What is its
vertex? Check with `vertex`.

<details class="dl-answer"><summary>answer</summary>

Half of 10 is 5, and $(x + 5)^2 = x^2 + 10x + 25$. That is 25 too much,
so we take 25 away:

$$x^2 + 10x = (x + 5)^2 - 25$$

The vertex is $(-5, -25)$. Watch the sign: $(x + 5)^2$ is 0 when $x$
is $-5$.

```python
print(vertex(1, 10, 0))
```

It prints `(-5.0, -25.0)`.

</details>

**4. Explain.** A friend says $x^2 - 2x + 5$ is never 0, for any real
$x$, without trying a single number. How could they know?

<details class="dl-answer"><summary>answer</summary>

Complete the square: $x^2 - 2x + 5 = (x - 1)^2 + 4$. A real square is
never negative, so $(x - 1)^2$ is 0 or more, and the whole rule is 4 or
more. It can never come down to 0. The discriminant from
[Solving for x](tutorial:solving-for-x#how-many-answers-the-discriminant)
says the same: $(-2)^2 - 4 \times 1 \times 5 = -16$, less than 0.

</details>

## Core

A cell for the core problems.

```python exec
id: the-top-practice-core
# Your working for problems 5 to 11
```

**5. Make.** Tomás has 40 m of fencing for a vegetable patch against a
garden wall. The wall is one long side, so the fence makes the other
three. If each short side is $w$ metres, the long side is $40 - 2w$
metres. What $w$ gives the biggest patch, and how big is it? Find it
with `vertex`, then check it with a fine comb.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The area is width times length: $w(40 - 2w)$.
2. Multiply out the bracket: $40w - 2w^2$. So $a = -2$, $b = 40$ and
   $c = 0$.
3. For the fine comb, try every $w$ from 0 to 20 in steps of 0.1, and
   keep the largest area.

**Think about:** why must $w$ be between 0 and 20?

**Try this next:** with the wall gone, the fence makes all four sides.
What shape gives the biggest patch then?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(vertex(-2, 40, 0))

widths = []
areas = []
for tenths in range(0, 201):
    widths.append(tenths / 10)
    areas.append(tenths / 10 * (40 - 2 * tenths / 10))
biggest = largest(areas)
print(widths[areas.index(biggest)], biggest)
```

Both give a width of 10 m and an area of 200 square metres. The long
side is then $40 - 20 = 20$ m. The width must be between 0 and 20,
because at 20 the long side is 0: that is the domain of the rule.

</details>

**6. Fix.** Here is someone's version of `vertex`. The first test
passes and the second fails. Run it, find the mistake, and fix it.

```python exec
id: the-top-practice-fix
def vertex_again(a, b, c):
    """Return the vertex of y = ax² + bx + c as a pair (x, y)."""
    x = -b / 2 * a
    y = a * x ** 2 + b * x + c
    return (x, y)

assert vertex_again(1, -6, 13) == (3, 4)
assert vertex_again(-20, 140, -120) == (3.5, 125), vertex_again(-20, 140, -120)
print("vertex_again keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The second test's message shows what the function gave back. Is the
   $x$ anywhere near 3.5?
2. Work out `-140 / 2 * -20` by hand, in the order Python does it.
3. Compare with the formula $-\frac{b}{2a}$. What is on the bottom?

**Think about:** why did the first test pass? What is special about its
$a$?

</details>

<details class="dl-answer"><summary>answer</summary>

The line `x = -b / 2 * a` divides by 2 and then *multiplies* by `a`,
because Python does `/` and `*` from left to right, as on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#which-comes-first).
The formula wants the whole of $2a$ on the bottom:

```python
x = -b / (2 * a)
```

The first test passed by luck: its $a$ is 1, and multiplying by 1 and
dividing by 1 give the same answer. A test with $a = 1$ cannot catch
this mistake, which is a good reason to test with other values too.

</details>

**7. Predict.** A band sells tickets for a gig. At $p$ euro a ticket,
about $800 - 30p$ people come, so the takings are $p(800 - 30p)$, which
is $-30p^2 + 800p$. The cell below searches whole-euro prices only.
Before you run it, what do you think it prints? Does it agree with
`vertex`?

```python
takings = []
for price in range(0, 27):
    takings.append(price * (800 - 30 * price))
best = largest(takings)
print(takings.index(best), best)
print(vertex(-30, 800, 0))
```

<details class="dl-answer"><summary>answer</summary>

The search prints `13 5330`, and `vertex` prints about
`(13.333333333333334, 5333.333333333334)`.

They disagree a little, and both are right. The vertex is at €13.33,
between two rows of the search, which only tried whole euros. €13
gives €5,330 and €14 gives €5,320, so €13 is the best whole-euro price.
At €13.33 the takings are only €3.33 more. For a real ticket price, the
whole-euro answer from the search may be the more useful one.

</details>

**8. Another way.** A sliotar's height, in metres, $t$ seconds after it
is struck, is $1.5 + 12t - 4.9t^2$. Find when it is highest in two
ways: with `vertex`, and from the two roots that `solve_quadratic`
gives.

<details class="dl-answer"><summary>answer</summary>

```python
print(vertex(-4.9, 12, 1.5))

roots = solve_quadratic(-4.9, 12, 1.5)
print(roots)
print((roots[0] + roots[1]) / 2)
```

`vertex` says about 1.22 seconds, at a height of about 8.85 m. The
roots are about −0.12 and 2.57 seconds, and halfway between them is
1.22 again. The mirror puts the vertex midway between the roots. The
negative root is a time before the sliotar was struck, but it still
does its job as the other end of the mirror.

</details>

**9. Make.** Complete the square for $2x^2 - 12x + 22$. Take the 2 out
of the $x$ terms first. Then check your vertex form against the first
form for several values of $x$, with a loop.

<details class="dl-answer"><summary>answer</summary>

Taking out the 2: $2x^2 - 12x + 22 = 2(x^2 - 6x) + 22$. Inside the
bracket, half of $-6$ is $-3$, and $x^2 - 6x = (x - 3)^2 - 9$. So

$$2\left((x - 3)^2 - 9\right) + 22 = 2(x - 3)^2 - 18 + 22 = 2(x - 3)^2 + 4$$

The vertex is $(3, 4)$, a minimum.

```python
for x in [-1, 0, 2.5, 3, 7]:
    print(x, 2 * x ** 2 - 12 * x + 22, 2 * (x - 3) ** 2 + 4)
print(vertex(2, -12, 22))
```

The last two columns agree on every row, and `vertex` gives
`(3.0, 4.0)`.

</details>

**10. Explain.** A parabola has its vertex at $(2, -9)$, and the number
in front of its $x^2$ is positive. How many roots does it have? What if
that number were negative instead? Sketch both, or draw them with
`plot_rule` using $(x - 2)^2 - 9$ and $-(x - 2)^2 - 9$.

<details class="dl-answer"><summary>answer</summary>

With a positive number, the parabola opens upwards, and its lowest
point is 9 below the axis. It must cross the axis on the way down and
again on the way up: two roots. For $(x - 2)^2 - 9$ they are −1 and 5.

With a negative number, it opens downwards, and its *highest* point is
9 below the axis. It never reaches the axis: no roots.

So the vertex and the sign of $a$ together say how many roots there
are, without any formula. A vertex exactly on the axis gives one root.

</details>

**11. Explain.** The tutorial found Aoife's best price first with a
table, then with a graph, and only then with the formula
$x = -\frac{b}{2a}$. Another course might give the formula first and
then practise it on many examples. Which way would you have taught it,
and why?

<details class="dl-answer"><summary>answer</summary>

There is no one right answer. A good answer weighs things like these:

- The table and the graph show *why* there is a best price, and why
  €3 and €4 tie. A reader who forgets the formula can still find the
  answer that way.
- The table can miss the answer, as it did between €3 and €4. That
  miss is a reason to want a formula, and it is felt more strongly
  when the reader has seen it happen.
- Formula first is shorter, and it gets a reader to correct answers
  quickly, which some readers find encouraging.
- Formula first can leave a reader who gets a strange answer, such as a
  vertex outside the domain, with no picture to check it against.

Who is the page for, and what do they need most: speed, or a way to
check?

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: the-top-practice-stretch
# Your working for problems 12 to 14
```

**12. Make.** A coffee cart sells about $300 - 60p$ cups a day at $p$
euro a cup, and each cup costs it €0.80 to make. Write the profit as a
quadratic by multiplying out $(p - 0.8)(300 - 60p)$, check your
multiplying-out with `evaluate` at a few prices, then find the best
price.

<details class="dl-answer"><summary>answer</summary>

$(p - 0.8)(300 - 60p) = 300p - 60p^2 - 240 + 48p = -60p^2 + 348p - 240$.

```python
coffee_profit = [-240, 348, -60]
for price in [1, 2.5, 4]:
    print(price, round((price - 0.8) * (300 - 60 * price), 2), round(evaluate(coffee_profit, price), 2))

print(vertex(-60, 348, -240))
```

The two columns agree, so the multiplying-out is right. The best price
is €2.90, and the profit there is about €264.60 a day: 126 cups, each
making €2.10.

</details>

**13. Another way.** Here is a way to find the $x$ of any vertex without
roots and without completing the square. At $x = 0$, the rule
$ax^2 + bx + c$ gives $c$. Find the *other* $x$ where it gives $c$
again. Then use the mirror. Does your answer match $-\frac{b}{2a}$?
Check it on $x^2 - 6x + 13$, which has no real roots.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The rule gives $c$ when $ax^2 + bx + c = c$, that is when
   $ax^2 + bx = 0$.
2. Factorise: $x(ax + b) = 0$. So $x = 0$ or $ax + b = 0$.
3. `solve_linear(a, b)` gives the second one.
4. The mirror puts the vertex halfway between the two.

**Think about:** why does this work even when the parabola never
touches the axis?

</details>

<details class="dl-answer"><summary>answer</summary>

The rule gives $c$ at $x = 0$ and at $x = -\frac{b}{a}$. The mirror
puts the vertex halfway between: $\frac{0 + (-b/a)}{2} = -\frac{b}{2a}$,
the same formula.

```python
other = solve_linear(1, -6)
print(other, evaluate([13, -6, 1], 0), evaluate([13, -6, 1], other))
print((0 + other) / 2, vertex(1, -6, 13))
```

For $x^2 - 6x + 13$, the rule gives 13 at 0 and at 6, and halfway is 3,
the $x$ of the vertex $(3, 4)$. This works with no roots, because it
uses a height the curve always reaches, $c$, in place of the height 0.

</details>

**14. Make.** Here is a surprise that joins this page to
[What is typical?](tutorial:what-is-typical#the-standard-deviation).
Take the bus delays `[3, 7, 8, 12, 5]`. For any guess $m$, add up the
squared distances from each value to $m$. That total is a quadratic in
$m$:

$$5m^2 - 70m + 291$$

(The 5 is how many values there are, the 70 is twice their total, and
the 291 is the total of their squares.) Which $m$ makes it smallest?
Compare it with `mean`. Then divide the smallest total by 5, and
compare it with `std_dev` squared.

<details class="dl-answer"><summary>answer</summary>

```python
delays = [3, 7, 8, 12, 5]
best_guess, smallest_total = vertex(5, -70, 291)
print(best_guess, mean(delays))
print(smallest_total / 5, std_dev(delays) ** 2)
```

The vertex is at $m = 7$, which is the mean. The mean is the one guess
that makes the squared distances as small as they can be. The smallest
total is 46, and $46 \div 5 = 9.2$, which is the standard deviation
squared. So the standard deviation
is built from the bottom of this parabola.

</details>
