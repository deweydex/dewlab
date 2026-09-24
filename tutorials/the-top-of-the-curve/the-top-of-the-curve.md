---
title: "The top of the curve: maximum and minimum"
year: "2026-2027"
version: 2026.09.24.1
covers:
  a-price-too-low-a-price-too-high:
    covers: [MIT-3.4]
    touches: [MIT-6.4]
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

Aoife sells cupcakes at a Saturday market. If she charges too little,
she sells every cupcake and makes almost nothing on each. If she charges
too much, hardly anyone buys. Somewhere in between is the price that
makes her the most money. How can she find it?

On this page we:

- look for the best price in a table, and see what a table can miss
- draw the profit as a curve, and find its highest point
- see that the top sits halfway between the two roots
- rewrite a quadratic so that its top or bottom can be read straight off
- add `vertex` to the toolkit, and check it against a search of a fine
  list of prices

> **The space we're in.** Quadratics, $ax^2 + bx + c$, with $a$ not 0,
> over the real numbers. A price or a time is a real number here, but a
> model of a shop is only true for some prices, and we will say which.
> One thing usually goes unsaid: every answer on this page is checked by
> putting it back into the rule, in code. Your toolkit is loaded, with
> `evaluate`, `plot_rule` and `solve_quadratic` from earlier in this
> unit.

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
correct: 3

What does `solve_quadratic(1, -5, 6)` give back? It solves
$x^2 - 5x + 6 = 0$.

- `[5, 6]`
- `[-3, -2]`
- `[2.0, 3.0]`
- `[]`
```

## A price too low, a price too high

Aoife has kept notes from past markets. Her cupcakes cost her €1 each to
make. At a price of $p$ euro, she sells about $120 - 20p$ of them: 100 at
€1, 60 at €3, none at all at €6. The numbers are made up, but real
sellers see the same pattern: a higher price means fewer sales.

Her *profit* is the money she keeps: the profit on one cupcake, times
the number sold.

$$\text{profit} = (p - 1)(120 - 20p)$$

Expanding the brackets, as on
[Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop),
gives a quadratic:

$$\text{profit} = -20p^2 + 140p - 120$$

Let's write it with `evaluate`, and try every whole-euro price from €1
to €6. Before you run the cell, which price do you think wins?

```python exec
id: the-top-table-1
profit_rule = [-120, 140, -20]   # -120 + 140p - 20p², lowest power first

def profit(price):
    """Return Aoife's profit in euro for a day at this price."""
    return evaluate(profit_rule, price)

for price in range(1, 7):
    print(price, (price - 1) * (120 - 20 * price), profit(price))
```

The two columns agree, so the multiplied-out rule is the same rule. Now
look at the profits: 0, 80, 120, 120, 80, 0. There is no single winner.
€3 and €4 tie on €120.

A tie like that is a clue. The profit rises, and then falls, in a
pattern that is the same from both ends. So the best price is probably
between €3 and €4, where the table has no row. Let's look in steps of
50 cent.

```python exec
id: the-top-table-2
for step in range(0, 11):
    price = 1 + step / 2
    print(price, profit(price))
```

At €3.50 the profit is €125, more than either whole-euro price. A table
only shows the rows we ask for. The best answer can hide between them.

## A curve that turns

A picture shows every price at once. On
[Drawing a rule](tutorial:drawing-a-rule) we drew a rule with
`plot_rule`. What shape do you expect?

```python exec
id: the-top-curve-1
import matplotlib.pyplot as plt

plot_rule(profit, 0, 7)
plt.plot(3.5, 125, "o")
plt.xlabel("price in euro")
plt.ylabel("profit in euro")
```

The curve rises, turns round at the dot, and comes back down. It is a
parabola, like the goalkeeper's kick on
[Drawing a rule](tutorial:drawing-a-rule#curves-that-bend-parabolas-and-cubics).
A parabola always has exactly one turning point, and that point is
called the *vertex*.

When $a$, the coefficient of $x^2$, is negative, the parabola opens
downwards, like a hill, and the vertex is its highest point. The
highest value a function reaches is its *maximum*. Aoife's $a$ is
$-20$, so her profit has a maximum, €125.

When $a$ is positive, the parabola opens upwards, like a valley, and
the vertex is its lowest point, the *minimum*. Every quadratic has one
or the other, never both.

Notice something else about the curve: its left and right halves are
mirror images. A vertical line through the vertex, here $p = 3.5$, is
the parabola's *axis of symmetry*. That mirror is why €3 and €4 tied:
each is 50 cent from the axis.

```question
id: the-top-curve-2
type: multiple-choice
correct: 2

The height of a sliotar, in metres, $t$ seconds after it is struck, is
$1.5 + 12t - 4.9t^2$. Does the height have a maximum or a minimum?

- a minimum, because 1.5 is positive
- a maximum, because $-4.9$ is negative
- neither, because $t$ is time
```

## Halfway between the roots

Where does Aoife make no profit at all? The curve meets the axis twice.
Those are the roots of the quadratic, which
[Solving for x](tutorial:solving-for-x) found with the quadratic
formula. Your toolkit's `solve_quadratic` takes $a$, $b$ and $c$. What
two prices do you expect?

```python exec
id: the-top-roots-1
roots = solve_quadratic(-20, 140, -120)
print(roots)
print((roots[0] + roots[1]) / 2)
```

The roots are €1, where she makes nothing on each cupcake, and €6, where
she sells none. The mirror puts the vertex halfway between them, at
€3.50.

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
makes an $x$ term with twice its number. We want $-6x$, so we halve $-6$ and get $-3$:
$(x - 3)^2 = x^2 - 6x + 9$. That is 4 short of $x^2 - 6x + 13$, so we
add 4:

$$x^2 - 6x + 13 = (x - 3)^2 + 4$$

Rewriting a quadratic as a square plus a number is called
*completing the square*. The result, $a(x - h)^2 + k$, is the
*vertex form*, and its vertex is $(h, k)$. Watch the sign of $h$: $(x - 3)^2$ is 0 when $x$ is
$+3$.

The same steps work on any quadratic. First take $a$ out of the
$x$ terms, then halve the number in front of $x$:

$$ax^2 + bx + c = a\left(x + \frac{b}{2a}\right)^2 + c - \frac{b^2}{4a}$$

So, for any quadratic, the vertex is at

$$x = -\frac{b}{2a}$$

and its height is the rule at that $x$. In words: the top or bottom is
at minus $b$, over two $a$.

For Aoife, $-\frac{140}{2 \times (-20)} = 3.5$. The formula needs no
roots and no graph.

### Roots from the same form

Vertex form also gives the roots. Aoife's $a$ is $-20$ and her vertex
is $(3.5, 125)$, so her profit is $-20(p - 3.5)^2 + 125$. Setting that
to 0:

$$(p - 3.5)^2 = \frac{125}{20} = 6.25$$

So $p - 3.5$ is $2.5$ or $-2.5$, and $p$ is 6 or 1, the roots we found.
[Solving for x](tutorial:solving-for-x#the-quadratic-formula) gave the
quadratic formula without saying where it came from. Doing these same
steps on $ax^2 + bx + c$ with letters is where it comes from. And if
the number on the right is negative, as it is for $(x - 3)^2 = -4$,
there is no real root: a real square is never negative. In the bigger
space of
[When there is no real answer](tutorial:when-there-is-no-real-answer),
it has two, $3 + 2i$ and $3 - 2i$.

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

The tests check the vertices we already know, and the footballer's
kick from
[Solving for x](tutorial:solving-for-x#the-quadratic-formula), whose
height was $1 + 14t - 4.9t^2$. The
last test checks the mirror: one step either side of the vertex, the
rule gives the same value. Until `vertex` is written, the first test
stops with an error.

```python exec
id: the-top-toolkit-tests
assert vertex(1, -6, 13) == (3, 4)
assert vertex(-20, 140, -120) == (3.5, 125)

top_time, top_height = vertex(-4.9, 14, 1)
assert close_enough(top_time, 14 / 9.8)
assert close_enough(top_height, 11)

x, y = vertex(2, -3, -5)
assert close_enough(evaluate([-5, -3, 2], x - 1), evaluate([-5, -3, 2], x + 1))
print("vertex keeps its promise.")
print("The ball is highest after", round(top_time, 2), "s, at", round(top_height, 2), "m.")
```

The ball climbs for about 1.43 seconds and reaches 11 m. That is
halfway between the two roots Solving for x found, −0.07 and 2.93, as
the mirror promises.

## Checking with a fine comb

The formula says €3.50. Is there really no better price? Let's search.
The cell builds a list of every price from €1 to €6 in steps of one
cent, works out the profit at each, and finds the largest with your
toolkit's `largest`. Before you run it, what do you expect it to print?

```python exec
id: the-top-comb-1
prices = []
profits = []
for cents in range(100, 601):
    prices.append(cents / 100)
    profits.append(profit(cents / 100))

best_profit = largest(profits)
best_price = prices[profits.index(best_profit)]
print(len(prices), "prices tried")
print(best_price, best_profit)
print(vertex(-20, 140, -120))
```

Five hundred and one prices, and the search agrees with the formula.
The search and the formula are two algorithms for one question, as the
loop and Gauss's trick were on
[Machines that take a number](tutorial:machines-that-take-a-number#an-algorithm-is-a-function-too).
The search is slow, and it only sees the prices it tries. The formula
is one line. We keep the search because it checks the formula with
nothing but arithmetic.

What does the model assume? It says Aoife sells $120 - 20p$ cupcakes.
At €7 that is $-20$ cupcakes, which means nothing, and `profit(7)` is
$-120$. So the rule only makes sense from €1 to €6: that is its domain.
The vertex is inside it, so the answer stands. If a vertex ever lands
outside the prices that make sense, the best answer is at the edge of
the domain instead. The picture and the table would show that; the
formula alone would not.

### Your turn

A car's fuel use, in litres per 100 km, at a speed of $v$ km/h, is
about $0.001v^2 - 0.14v + 9.9$. (A made-up model, with the shape of a
real car's.)

1. Is there a maximum or a minimum? Say why before you run anything.
2. Use `vertex` to find the most economical speed, and the fuel use
   there.
3. Check your answer with a fine comb: every speed from 30 to 130 km/h.
4. How much more fuel does the car use at 120 km/h?

```python exec
id: the-top-comb-your-turn
# The car's most economical speed
```

<details class="dl-why"><summary>Why this way?</summary>

This page found the top of a curve with algebra: completing the square,
and the formula $x = -\frac{b}{2a}$ that comes from it. Many courses
find it with calculus instead: the slope of a curve is 0 at its top,
so they find where the slope is 0.

Calculus is the stronger tool. It finds the tops and bottoms of curves
that are not parabolas, where completing the square cannot help.

We used algebra because it needs only one fact, that a square is never
negative, and that fact is enough to prove the answer. Calculus asks
for the idea of a slope at a single point, which is a large idea of
its own. Unit 9 comes back to this curve with that idea.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | $p$ for a price; the vertex $(h, k)$; a quadratic named by its list of coefficients |
| What is promised? | `vertex(a, b, c)` promises the turning point; vertex form promises the same rule, written to show its top or bottom |
| What happens when? | the search tries every cent in order and keeps the largest; completing the square halves $b$ first, then corrects the number at the end |
| What does this space let us do? | a real square is never negative, so the vertex is a true top or bottom; a model of a shop only holds between €1 and €6 |

## What we have now

| Term or tool | What it means |
|---|---|
| profit | the money kept: income minus cost |
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
