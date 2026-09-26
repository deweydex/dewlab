---
title: "The top of the curve: maximum and minimum — Practice"
practice_for: the-top-of-the-curve
year: "2026-2027"
version: 2026.09.25.1
---

# The top of the curve: maximum and minimum — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means answer in words. **Another
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

**4. Explain.** Schlomi, who is learning Python too, says
$x^2 - 2x + 5$ is never 0, for any real $x$. She has not tried a single
number. How could she know?

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Complete the square. $x^2 - 2x + 5 = (x - 1)^2 + 4$. A real square is
never negative, so $(x - 1)^2$ is 0 or more, and the whole rule is 4 or
more. It can never come down to 0. The discriminant from
[Solving for x](tutorial:solving-for-x#how-many-answers-the-discriminant)
says the same: $(-2)^2 - 4 \times 1 \times 5 = -16$, less than 0.

</details>

## Core

A cell for the core problems.

```python exec
id: the-top-practice-core
# Your working for problems 5 to 12
```

**5. Make.** In a building game, you have 40 blocks of fence to make a
rectangular pen against the edge of the map. The edge is one long
side, so the fence makes the other three. If each short side is $w$
blocks, the long side is $40 - 2w$ blocks. What $w$ gives the biggest
pen, and how many squares of ground does it hold? Find it with
`vertex`, then check it with a search in small steps.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The area is width times length: $w(40 - 2w)$.
2. Multiply out the bracket: $40w - 2w^2$. So $a = -2$, $b = 40$ and
   $c = 0$.
3. For the search, try every $w$ from 0 to 20 in steps of 0.1, and
   keep the largest area.

**Think about:** why must $w$ be between 0 and 20?

**Try this next:** away from the edge, the fence makes all four sides.
What shape gives the biggest pen then?

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

Both give a width of 10 blocks and 200 squares of ground. The long
side is then $40 - 20 = 20$ blocks. The width must be between 0 and 20,
because at 20 the long side is 0. So 0 to 20 is the domain of the rule. A
game needs whole blocks, and here the best width is whole already.

</details>

**6. Fix.** Schlomo, who is also learning Python, wrote his own
`vertex`. The first test passes and the second fails. Run it, find the
line that does not do what Schlomo meant, and change it.

```python exec
id: the-top-practice-fix
def vertex_again(a, b, c):
    """Return the vertex of y = ax² + bx + c as a pair (x, y)."""
    x = -b / 2 * a
    y = a * x ** 2 + b * x + c
    return (x, y)

assert vertex_again(1, -6, 13) == (3, 4)
assert close_enough(vertex_again(400, -440, 112)[0], 0.55), vertex_again(400, -440, 112)
print("vertex_again keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The second test's message shows what the function returned. Is the
   $x$ anywhere near 0.55?
2. Calculate `440 / 2 * 400` by hand, in the order Python does it.
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

Schlomo's $x$ for the bowl was 88,000, far off the letter. The first
test passed by luck. Its $a$ is 1, and multiplying by 1 and dividing by
1 give the same answer. A test with $a = 1$ cannot tell the two lines
apart, which is a reason to test with other values too.

</details>

**7. Predict.** A game draws a thrown ball 10 times a second. The
ball's height after $t$ seconds is $1 + 14t - 4.9t^2$ metres, so frame
number $f$ shows it at $t = f / 10$. The cell finds the frame where
the ball is drawn highest. Before you run it, what do you think it
prints? Does it agree with `vertex`?

```python
heights = []
for frame in range(0, 30):
    t = frame / 10
    heights.append(1 + 14 * t - 4.9 * t ** 2)
top = largest(heights)
print(heights.index(top), top)
print(vertex(-4.9, 14, 1))
```

<details class="dl-answer"><summary>answer</summary>

The search prints frame `14`, at a height of about 10.996 m, and
`vertex` prints about `(1.4286, 11.0)`.

They differ a little, and each gives what it measures. The true top is at 1.4286
seconds, between frame 14 and frame 15, and the game never draws that
moment. So the highest ball a player sees is 4 mm lower than the real
top. For a game, that is close enough. For a program that must know the true
top, such as one that checks whether the ball clears a bar, should
use the formula.

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
marks the other end of the mirror.

</details>

**9. Make.** Complete the square for $2x^2 - 12x + 22$. Take the 2 out
of the $x$ terms first. Then check your vertex form against the first
form for several values of $x$, with a loop.

<details class="dl-answer"><summary>answer</summary>

First take out the 2: $2x^2 - 12x + 22 = 2(x^2 - 6x) + 22$. Inside the
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
again on the way up, so it has two roots. For $(x - 2)^2 - 9$ they are −1 and 5.

With a negative number, it opens downwards, and its *highest* point is
9 below the axis. It never reaches the axis, so it has no roots.

So the vertex and the sign of $a$ together say how many roots there
are, without any formula. A vertex exactly on the axis gives one root.

</details>

**11. Explain.** The tutorial found the bottom of the letter's bowl
first with a table, then with a graph, and only then with the formula
$x = -\frac{b}{2a}$. Another course might give the formula first and
then practise it on many examples. Which way would you have taught it,
and why?

<details class="dl-answer"><summary>answer</summary>

This question has more than one answer. Here is one, which weighs
things like these:

- The table and the graph show *why* there is a lowest point, and why
  0.5 and 0.6 tie. A reader who forgets the formula can still find the
  answer that way.
- The table can miss the answer, as it did between 0.5 and 0.6. That
  miss is a reason to want a formula, and a reader feels it more after
  seeing it happen.
- Formula first is shorter, and it gets a reader to an answer
  quickly, which some readers find encouraging.
- Formula first can leave a reader who gets a strange answer, such as a
  vertex outside the domain, with no picture to check it against.

Who is the page for, and what do they need most: speed, or a way to
check? Your answer may weigh things this list leaves out.

</details>

**12. Explain.** Schlomo has an idea for the letter's bowl on the
tutorial page. "The control point is at $(260, -108)$, and it is the
lowest of the three points. So the bowl's lowest point is 108 units
below the baseline, at $x = 260$. No formula needed." Where does
Schlomo's idea work, and where does it stop working?

<details class="dl-answer"><summary>answer</summary>

The bowl does not go down to $-108$, but part of his idea works. The curve never reaches
its control point. The control point only pulls it. The bowl's lowest
point is only 9 units below the baseline, at $t = 0.55$, where $x$ is
about 288. You can see it in the tutorial's picture: the dotted lines
go down to $-108$, and the curve stays far above them.

This part of his idea works. The curve always stays inside the
triangle its three points make. So the bowl cannot go below the
control point's height, $-108$. Schlomo found this limit, but not the
bottom itself. Here is one way to check:

```python
print(vertex(400, -440, 112))
```

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: the-top-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** The bottom of an "s" in the same font is another
quadratic Bézier curve. Its three heights, in font units, are 40 at the
start, $-70$ at the control point and 60 at the end. Multiply out
$(1 - t)^2 \times 40 + 2t(1 - t) \times (-70) + t^2 \times 60$ to get
$at^2 + bt + c$, check your multiplying-out with `evaluate` at a few
values of $t$, then find how far the "s" dips below the baseline.

<details class="dl-answer"><summary>answer</summary>

$(1 - t)^2 \times 40 = 40 - 80t + 40t^2$, and
$2t(1 - t) \times (-70) = -140t + 140t^2$, and the last part is $60t^2$.
Collecting: $240t^2 - 220t + 40$.

```python
s_bottom = [40, -220, 240]
for t in [0, 0.25, 0.5, 1]:
    mixed = (1 - t) ** 2 * 40 + 2 * t * (1 - t) * -70 + t ** 2 * 60
    print(t, round(mixed, 6), round(evaluate(s_bottom, t), 6))

print(vertex(240, -220, 40))
```

The two columns agree, so the multiplied-out rule is the same rule. The vertex is
at $t \approx 0.458$, and the "s" dips about 10.4 units below the
baseline: a little more than the bowl's 9. The vertex is inside 0 to 1,
so it is on the letter.

</details>

**14. Another way.** Here is a way to find the $x$ of any vertex without
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

**15. Make.** Here is a surprise that joins this page to
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
