---
title: "The top of the curve: maximum and minimum"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-letter-that-sits-below-the-line:
    covers: [MIT-3.4]
    touches: [MIT-6.4, MIT-1.8]
  a-curve-that-turns:
    covers: [MIT-3.4]
    touches: [MIT-3.2]
  halfway-between-the-roots:
    covers: [MIT-3.4]
    touches: [MIT-1.9]
  completing-the-square:
    covers: [MIT-3.4]
  a-tool-for-the-top:
    covers: [MIT-3.4]
    touches: [PDP-LO8]
  checking-with-a-fine-comb:
    covers: [MIT-3.4]
    touches: [MIT-6.5]
---

# The top of the curve: maximum and minimum

Type the letters “x” and “o” next to each other, make them very
large, and look at the bottom of each. The x stands on the line. The o
does not: its bottom dips a little way below it. Pause here and guess
why a type designer would do that on purpose. I'll wait.

Here is the reason. A round shape touches the line at one point only,
so an o that sits exactly on the line looks as if it floats. Our eyes
are fooled, so the designer fools them back. To do that, you need to
know where the bottom of a curve is. This page is called "the top of
the curve", and it starts at the bottom of one. The maths is the same:
a curve that turns, and the one point where it turns.

On this page we:

- hunt for the lowest point of a letter's curve in a table
- draw the curve, and name the point where it turns
- see that the turning point sits halfway between the roots
- rewrite a quadratic so that its top or bottom can be read straight off
- add `vertex` to the toolkit, and check it with a fine comb

> **The space we're in.** Quadratics, $ax^2 + bx + c$, with $a$ not 0,
> over the real numbers. A letter's curve is only drawn for some inputs,
> and we will say which. One thing usually goes unsaid: every answer on
> this page is checked by putting it back into the rule, in code. Your
> toolkit is loaded, with `evaluate`, `plot_rule` and `solve_quadratic`
> from earlier in this unit.

## Warm-up

The first question is from
[A row of numbers](tutorial:a-row-of-numbers#three-tools-for-your-toolkit),
and the second from
[Solving for x](tutorial:solving-for-x).

```question
id: the-top-warm-up-1
type: fill-in-the-blank

`scores = [4, 9, 2, 9, 6]`. Then `largest(scores)` is {9}, and
`scores.index(9)` is {1}.
```

```question
id: the-top-warm-up-2
type: multiple-choice
answer: 3

What does `solve_quadratic(1, -5, 6)` give back? It solves
$x^2 - 5x + 6 = 0$.

- `[5, 6]`
  - These are numbers from the equation, not the values of x that make it 0.
- `[-3, -2]`
  - These have the signs turned over: (x − 2)(x − 3) is 0 at 2 and 3.
- `[2.0, 3.0]`
  - (x − 2)(x − 3) is 0 at x = 2 and x = 3, given as floats, smallest first.
- `[]`
  - An empty list is for an equation with no real roots; this curve crosses the x-axis twice.
```

## A letter that sits below the line

A font stores each letter as points on a grid, measured in *font
units*. Our font is made up, but its numbers are the size a real
font's are: the top of a small x is at 500. The *baseline*, the line
the letters stand on, is at 0, and $y$ counts upwards, as on a graph.

Between the points, the font draws curves. A *quadratic Bézier curve*
needs three points: a start, an end, and a *control point*. The curve
starts at the first point, bends towards the control point, and ends
at the last. The control point pulls, but the curve never reaches it.

Here is the bottom of a bowl from our font. It starts at $(100, 112)$,
has its control point at $(260, -108)$, and ends at $(460, 72)$. A
number $t$ runs from 0 at the start to 1 at the end, and at each $t$
the curve's height is a mix of the three heights:

$$y = (1 - t)^2 \times 112 + 2t(1 - t) \times (-108) + t^2 \times 72$$

Expanding the brackets, as on
[Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop),
gives a quadratic in $t$:

$$y = 400t^2 - 440t + 112$$

The cell works out the height both ways, at every tenth from 0 to 1.
Before you run it, where do you think the curve is lowest?

```python exec
id: the-top-table-1
bowl_rule = [112, -440, 400]   # 112 - 440t + 400t², lowest power first

def bowl_height(t):
    """Return the height of the bowl's curve, in font units, at t from 0 to 1."""
    return evaluate(bowl_rule, t)

for tenths in range(0, 11):
    t = tenths / 10
    mixed = (1 - t) ** 2 * 112 + 2 * t * (1 - t) * -108 + t ** 2 * 72
    print(t, round(mixed, 2), round(bowl_height(t), 2))
```

The two columns agree, so the expanded rule is the same rule. The
heights fall below the baseline and come back up. (One row says
`-0.0`: that float is a hair below 0, and rounding keeps the minus
sign.) There is no single lowest row: at 0.5 and at 0.6 the height is
$-8$, a tie.

A tie like that is a clue. The heights fall and rise in a pattern that
is the same from both ends, so the lowest point is probably between 0.5
and 0.6, where the table has no row. Let's look in steps of 0.05.

```python exec
id: the-top-table-2
for twentieths in range(0, 21):
    t = twentieths / 20
    print(t, round(bowl_height(t), 2))
```

At 0.55 the height is $-9$, lower than any row of the first table. A
table only shows the rows we ask for, and the answer can hide between
them. The bowl dips 9 font units below the baseline: 1.8% of the x's
height of 500.

<aside class="dl-note" id="the-top-note-overshoot">

**Overshoot.** Type designers call this dip *overshoot*. Round letters
such as o, s and u go a little below the baseline, and a little above
the top of an x, so that they look the same size as flat letters. The
amount depends on the designer. About 1% to 3% of the letter's height
is usual for an o.

</aside>

## A curve that turns

A picture shows every $t$ at once. The cell draws the curve, its three
points, the baseline and the lowest point. What shape do you expect?

```python exec
id: the-top-curve-1
import matplotlib.pyplot as plt

xs = []
ys = []
for step in range(0, 101):
    t = step / 100
    xs.append((1 - t) ** 2 * 100 + 2 * t * (1 - t) * 260 + t ** 2 * 460)
    ys.append(bowl_height(t))

plt.plot(xs, ys, label="the bowl's curve")
plt.plot([100, 260, 460], [112, -108, 72], "o:", color="grey", label="its three points")
plt.axhline(0, color="black", linewidth=1, label="baseline")
plt.plot(xs[55], ys[55], "o", color="C3", label="lowest point")
plt.gca().set_aspect("equal")
plt.legend(loc="upper center")
```

The curve dips below the baseline and turns back up. The control
point, far below, only pulls it part of the way. The height against
$t$, drawn with `plot_rule`, has the same shape:

```python exec
id: the-top-curve-3
plot_rule(bowl_height, 0, 1)
plt.xlabel("t")
plt.ylabel("height in font units")
```

It is a parabola, like the goalkeeper's kick on
[Drawing a rule](tutorial:drawing-a-rule#curves-that-bend-parabolas-and-cubics).
A parabola has exactly one turning point, and that point is called the
*vertex*.

When $a$, the coefficient of $x^2$, is positive, the parabola opens
upwards, like a valley, and the vertex is its lowest point. The lowest
value a function reaches is its *minimum*. The bowl's $a$ is 400, so
its height has a minimum, $-9$.

When $a$ is negative, the parabola opens downwards, like a hill, and
the vertex is its highest point, the *maximum*. Every quadratic has one
or the other, never both.

Notice something else: the left and right halves of the parabola are
mirror images. A vertical line through the vertex, here $t = 0.55$, is
the parabola's *axis of symmetry*. That mirror is why 0.5 and 0.6 tied:
each is 0.05 from the axis.

<aside class="dl-note" id="the-top-note-bezier">

**Two car makers.** Bézier curves are named after Pierre Bézier, an
engineer at Renault, who used them in the 1960s to describe car bodies
to a machine. Paul de Casteljau found the same curves a few years
earlier at Citroën, but his work stayed a company secret. TrueType
fonts draw with the quadratic curves on this page; PostScript fonts use
cubic ones, with two control points.

</aside>

```question
id: the-top-curve-2
type: multiple-choice
answer: 2

The height of a sliotar, in metres, $t$ seconds after it is struck, is
$1.5 + 12t - 4.9t^2$. Does the height have a maximum or a minimum?

- a minimum, because 1.5 is positive
  - 1.5 is the height at the start, when t = 0; the t² part decides the shape.
- a maximum, because $-4.9$ is negative
  - A negative number with t² makes the curve open downward, so it has a highest point.
- neither, because $t$ is time
  - t is time, but the height still rises and then falls, so it has a highest point.
```

## Halfway between the roots

Where does the bowl cross the baseline? There, its height is 0, so
those $t$ are the roots of the quadratic. Your toolkit's
`solve_quadratic` finds them. What two values do you expect?

```python exec
id: the-top-roots-1
roots = solve_quadratic(400, -440, 112)
print(roots)
print((roots[0] + roots[1]) / 2)
```

The roots are 0.4 and 0.7. Between them, the letter is below the line.
The mirror puts the vertex halfway between them, at 0.55.

That is one way to find a vertex. But it needs two roots, and some
parabolas never meet the axis. On
[Solving for x](tutorial:solving-for-x#how-many-answers-the-discriminant),
the curve of $x^2 - 6x + 13$ never came down to the axis, and yet it
has a lowest point. We want a way that always works.

## Completing the square

Here is that quadratic with no real roots, $x^2 - 6x + 13$, written a
second way. Do the two columns agree?

```python exec
id: the-top-square-1
def as_given(x):
    return x ** 2 - 6 * x + 13

def as_square(x):
    return (x - 3) ** 2 + 4

for x in [-2, 0, 1, 3, 4.5, 10]:
    print(x, as_given(x), as_square(x))
```

Every row agrees, so the two forms are one rule. The second form is
the useful one. Here is why, in words:

1. A square is never negative, so $(x - 3)^2$ is 0 or more.
2. It is exactly 0 when $x = 3$, and more than 0 anywhere else.
3. So the smallest value of $(x - 3)^2 + 4$ is 4, and it happens at
   $x = 3$.

The vertex is $(3, 4)$, a minimum, and we read it from the rule without
drawing anything.

How do we get the second form from the first? On
[Rules with letters in them](tutorial:rules-with-letters-in-them#a-move-that-works-once),
$(x + n)^2 = x^2 + 2nx + n^2$ for any number $n$. So a bracket squared
makes an $x$ term with twice its number. We want $-6x$, so we halve
$-6$ and get $-3$: $(x - 3)^2 = x^2 - 6x + 9$. That is 4 short of
$x^2 - 6x + 13$, so we add 4:

$$x^2 - 6x + 13 = (x - 3)^2 + 4$$

Rewriting a quadratic as a square plus a number is called
*completing the square*. The result, $a(x - h)^2 + k$, is the
*vertex form*, and its vertex is $(h, k)$. Watch the sign of $h$:
$(x - 3)^2$ is 0 when $x$ is $+3$.

The same steps work on any quadratic. First take $a$ out of the
$x$ terms, then halve the number in front of $x$:

$$ax^2 + bx + c = a\left(x + \frac{b}{2a}\right)^2 + c - \frac{b^2}{4a}$$

So, for any quadratic, the vertex is at

$$x = -\frac{b}{2a}$$

and its height is the rule at that $x$. In words: the top or bottom is
at minus $b$, over two $a$.

For the bowl, $-\frac{-440}{2 \times 400} = 0.55$. The formula needs
no roots and no graph.

### Roots from the same form

Vertex form also gives the roots. The bowl's $a$ is 400 and its vertex
is $(0.55, -9)$, so its height is $400(t - 0.55)^2 - 9$. Setting that
to 0:

$$(t - 0.55)^2 = \frac{9}{400} = 0.0225$$

So $t - 0.55$ is $0.15$ or $-0.15$, and $t$ is 0.7 or 0.4, the roots we
found. The same steps, done with letters on $ax^2 + bx + c$, are where
the quadratic formula on
[Solving for x](tutorial:solving-for-x#the-quadratic-formula) comes
from. And if the number on the right is negative, as for
$(x - 3)^2 = -4$, there is no real root, because a real square is never
negative. In the bigger space of
[When there is no real answer](tutorial:when-there-is-no-real-answer),
there are two, $3 + 2i$ and $3 - 2i$.

### Your turn

1. Complete the square for $x^2 + 4x + 7$. What number do you halve?
2. What is the vertex? Is it a maximum or a minimum?
3. Check your vertex form in the cell below, by comparing both forms
   for several values of $x$, as the first cell of this section did.

```python exec
id: the-top-square-your-turn
# Compare x**2 + 4*x + 7 with your vertex form
```

## A tool for the top

Now the formula becomes a tool. Here is its promise; the body is yours
to write.

```python exec
id: the-top-toolkit
toolkit: yes
def vertex(a, b, c):
    """Return the vertex of the parabola y = ax² + bx + c as a pair (x, y).

    It is the highest point when a is negative, and the lowest when a
    is positive. a must not be 0.
    """
    ...
```

```python toolkit-reference
for: the-top-toolkit
def vertex(a, b, c):
    """Return the vertex of the parabola y = ax² + bx + c as a pair (x, y).

    It is the highest point when a is negative, and the lowest when a
    is positive. a must not be 0.
    """
    x = -b / (2 * a)
    y = a * x ** 2 + b * x + c
    return (x, y)
```

```hint
What does `print(vertex(1, -6, 13))` show? If it shows `None`, the
function has no `return` yet. It needs two lines before the `return`:
one for `x`, one for `y`.
```

```hint
after: 10 errors
title: some steps
1. Work out `x` as `-b / (2 * a)`. The brackets matter: without them,
   Python divides by 2 and then multiplies by `a`.
2. Work out `y` by putting that `x` into the rule `a * x ** 2 + b * x + c`.
3. Return the pair `(x, y)`.

**Think about:** why is `y` found by substituting `x` back, and not by
a second formula?
```

The tests check vertices we already know: the square, the bowl, and
the footballer's kick from
[Solving for x](tutorial:solving-for-x#the-quadratic-formula), whose
height was $1 + 14t - 4.9t^2$. The last test checks the mirror: one
step either side of the vertex, the rule gives the same value. Until
`vertex` is written, the first test stops with an error.

```python exec
id: the-top-toolkit-tests
assert vertex(1, -6, 13) == (3, 4)

bottom_t, bottom_height = vertex(400, -440, 112)
assert close_enough(bottom_t, 0.55)
assert close_enough(bottom_height, -9)

top_time, top_height = vertex(-4.9, 14, 1)
assert close_enough(top_time, 14 / 9.8)
assert close_enough(top_height, 11)

x, y = vertex(2, -3, -5)
assert close_enough(evaluate([-5, -3, 2], x - 1), evaluate([-5, -3, 2], x + 1))
print("vertex keeps its promise.")
print("The ball is highest after", round(top_time, 2), "s, at", round(top_height, 2), "m.")
```

The ball climbs for about 1.43 seconds and reaches 11 m, halfway
between the roots −0.07 and 2.93, as the mirror promises.

## Checking with a fine comb

The formula says 0.55. Is there really no lower point? Let's search.
The cell tries every $t$ from 0 to 1 in steps of a thousandth, works
out the height at each, and finds the lowest with your toolkit's
`smallest`. Before you run it, what do you expect it to print?

```python exec
id: the-top-comb-1
ts = []
heights = []
for thousandths in range(0, 1001):
    ts.append(thousandths / 1000)
    heights.append(bowl_height(thousandths / 1000))

lowest = smallest(heights)
print(len(ts), "values of t tried")
print(ts[heights.index(lowest)], round(lowest, 6))
print(vertex(400, -440, 112))
```

A thousand and one tries, and the search agrees with the formula: two
algorithms for one question, as the loop and Gauss's trick were on
[Machines that take a number](tutorial:machines-that-take-a-number#an-algorithm-is-a-function-too).
The search is slow and only sees the values it tries. We keep it
because it checks the formula with nothing but arithmetic.

What does the rule assume? The parabola goes on for ever, but the
letter only uses the piece from $t = 0$ to $t = 1$: that is the rule's
domain here. The vertex is inside it, so the answer stands. If a vertex
lands outside the domain, the lowest point of the piece is at one of
its ends. The picture and the table would show that; the formula alone
would not.

Could we find the curve from a photo of a letter, with no font file?
Three pixels on the curve would give three equations in three
unknowns, $a$, $b$ and $c$. That is the next page,
[Several unknowns at once](tutorial:several-unknowns-at-once#three-unknowns).

### Your turn

A ball thrown straight up is at a height of about $1.8 + 15t - 4.9t^2$
metres after $t$ seconds. (A model: it leaves out the air.)

1. Is there a maximum or a minimum? Say why before you run anything.
2. Use `vertex` to find when the ball is highest, and how high it gets.
3. Check with a fine comb: every hundredth of a second from 0 to 3.
4. When does it land? Which root from `solve_quadratic` is a real time?

```python exec
id: the-top-comb-your-turn
# The ball's highest point
```

<details class="dl-why"><summary>Why this way?</summary>

This page found the bottom of a curve with algebra: completing the
square, and the formula $x = -\frac{b}{2a}$ that comes from it. Many
courses find it with calculus instead: the slope of a curve is 0 at
its top or bottom, so they find where the slope is 0.

Calculus is the stronger tool. It finds the tops and bottoms of curves
that are not parabolas, where completing the square cannot help, such
as the cubic curves many fonts use.

We used algebra because it needs only one fact, that a square is never
negative, and that fact is enough to prove the answer. Calculus asks
for the idea of a slope at a single point, which is a large idea of
its own. Unit 9 comes back to this bowl with that idea.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | $t$ for how far along a curve we are; the vertex $(h, k)$; a quadratic named by its list of coefficients |
| What is promised? | `vertex(a, b, c)` promises the turning point; vertex form promises the same rule, written to show its top or bottom |
| What happens when? | the search tries every thousandth in order and keeps the smallest; completing the square halves $b$ first, then corrects the number at the end |
| What does this space let us do? | a real square is never negative, so the vertex is a true top or bottom; a letter's curve only uses $t$ from 0 to 1 |

## What we have now

| Term or tool | What it means |
|---|---|
| font units, baseline | the grid a font stores its letters on; the line the letters stand on, at 0 |
| quadratic Bézier curve | a curve from a start, a control point and an end; its height is a quadratic in $t$ |
| parabola | the graph of a quadratic, with one turning point |
| vertex | a parabola's turning point |
| maximum, minimum | the highest or lowest value a function reaches |
| axis of symmetry | the vertical line through the vertex; the parabola's mirror |
| completing the square | rewriting $ax^2 + bx + c$ as $a(x - h)^2 + k$ |
| vertex form | $a(x - h)^2 + k$, whose vertex is $(h, k)$ |
| $x = -\frac{b}{2a}$ | where the vertex of $ax^2 + bx + c$ is |
| `vertex(a, b, c)` | your toolkit tool: the turning point, as a pair $(x, y)$ |

For another route to the same curve, the integrated course has
[Parabolas: completing the square](tutorial:parabolas).

## Where to read more

Stand-up Maths (2016). *There is only One True Parabola.*
<https://www.youtube.com/watch?v=hoh4TmPzu1w>. Every parabola is the same
curve, made bigger or smaller and moved. Finding its top is finding where
it was moved to. Matt Parker shows why every parabola has the same shape.
About nine minutes.
