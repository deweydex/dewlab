---
title: "Several unknowns at once: simultaneous equations"
year: "2026-2027"
version: 2026.09.24.1
covers:
  two-facts-two-unknowns:
    covers: [MIT-1.12]
    touches: [MIT-6.6]
  two-lines-that-cross:
    covers: [MIT-1.12]
    touches: [MIT-3.2]
  elimination-one-unknown-at-a-time:
    covers: [MIT-1.12]
  one-formula-for-every-pair:
    covers: [MIT-1.12]
    touches: [PDP-LO8]
  when-there-is-no-single-answer:
    covers: [MIT-1.12]
  three-unknowns:
    covers: [MIT-1.12]
---

# Several unknowns at once: simultaneous equations

A GAA club ran a concert to raise money. Adult tickets cost €12 and
child tickets cost €5. At the end of the night the treasurer knows two
things: 230 tickets were sold, and the takings came to €2,060. Nobody
kept count of which kind was which. How many adults came, and how many
children?

On this page we:

- see that one fact about two unknowns has many answers, and two facts
  can pin down one
- draw each fact as a line, and find the answer where the lines cross
- solve by elimination, said in words and then in symbols
- turn elimination into a formula, and add `solve_simultaneous` to the
  toolkit
- see when two facts have no single answer, and draw why
- take the same idea to three unknowns

> **The space we're in.** Equations where each unknown is only
> multiplied by a number: no squares, no unknowns multiplied together.
> Each such equation in $x$ and $y$ draws a straight line on a flat
> plane. One thing usually goes unsaid: the answer must make every
> equation true at once, and we check that by substituting it back into
> each one. Your toolkit is loaded, with `plot_rule`, `solve_linear` and
> `vertex` from earlier in this unit.

## Warm-up

The first question is from
[Solving for x](tutorial:solving-for-x), and the second from
[The top of the curve](tutorial:the-top-of-the-curve#a-curve-that-turns).

```question
id: several-unknowns-warm-up-1
type: fill-in-the-blank

`solve_linear(a, b)` gives the $x$ where $ax + b = 0$. So
`solve_linear(2, -10)` gives {5}.
```

```question
id: several-unknowns-warm-up-2
type: multiple-choice
correct: 1

The parabola $y = x^2 - 8x + 3$ has its vertex at $x = -\frac{b}{2a}$.
Where is that?

- $x = 4$
- $x = -4$
- $x = 8$
- $x = 3$
```

## Two facts, two unknowns

Let's name what we do not know. Call the number of adults $a$ and the
number of children $c$. The first fact, in symbols, is

$$a + c = 230$$

Is that enough to find $a$? Try some pairs: 200 adults and 30
children, or 115 and 115. Each one makes 230. The cell counts every
pair of whole numbers that fits. How many do you expect?

```python exec
id: several-unknowns-facts-1
pairs = []
for adults in range(0, 231):
    children = 230 - adults
    pairs.append((adults, children))

print(len(pairs), "pairs fit the first fact")
print(pairs[:3], "...", pairs[-2:])
```

There are 231 pairs, from no adults to no children. One fact about two
unknowns leaves many answers. The second fact is the money: each adult
paid €12 and each child €5.

$$12a + 5c = 2060$$

Which of the 231 pairs fits this fact too? We can check them one at a
time, as a linear search does on
[Finding things fast](tutorial:finding-things-fast).

```python exec
id: several-unknowns-facts-2
for adults, children in pairs:
    if 12 * adults + 5 * children == 2060:
        print(adults, "adults and", children, "children")
```

Exactly one pair fits both: 130 adults and 100 children. Two equations
that must be true at the same time, for the same unknowns, are called
*simultaneous equations*. The pair that makes them all true is their
*solution*.

The search worked because the answers had to be whole numbers under
231. If the unknowns were prices, with cents, or measured amounts, there
would be far too many cases to try. We need a method.

## Two lines that cross

On [Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
two phone plans met where their graphs crossed. Each fact here can be
written as a rule that gives $c$ from $a$:

- from the tickets, $c = 230 - a$;
- from the money, $5c = 2060 - 12a$, so $c = \frac{2060 - 12a}{5}$.

Each is a linear function, so each graph is a straight line. What do
you expect to see where they meet?

```python exec
id: several-unknowns-lines-1
import matplotlib.pyplot as plt

def children_from_tickets(adults):
    return 230 - adults

def children_from_money(adults):
    return (2060 - 12 * adults) / 5

plot_rule(children_from_tickets, 0, 230)
plot_rule(children_from_money, 0, 230)
plt.plot(130, 100, "o")
plt.xlabel("adults")
plt.ylabel("children")
plt.legend()
```

Every point on the first line fits the ticket count. Every point on the
second fits the takings. Only one point is on both: the crossing, at
$(130, 100)$. Solving simultaneous equations in two unknowns is finding
where two lines cross.

## Elimination: one unknown at a time

The picture shows the answer. To get it exactly, we use the rule from
[Running a formula backwards](tutorial:running-a-formula-backwards#the-same-move-on-both-sides):
any move is allowed, if we do it to both sides. The plan, in words:

1. Change one equation so that $c$ has the same number in front of it
   in both.
2. Take one equation away from the other. The $c$ terms cancel, and
   only $a$ is left.
3. Solve for $a$.
4. Put $a$ back into either equation, and find $c$.

This method is called *elimination*, because step 2 eliminates one
unknown. In symbols, step 1 multiplies $a + c = 230$ by 5:

$$5a + 5c = 1150$$

Step 2 takes that away from $12a + 5c = 2060$:

$$7a = 910$$

Step 3 divides by 7, so $a = 130$. Step 4 puts 130 into $a + c = 230$,
so $c = 100$. The order matters: we cannot find $c$ in step 4 until
step 3 has found $a$.

Now the rule of this unit: substitute back, into both equations. Which
lines will print `True`?

```python exec
id: several-unknowns-elimination-1
adults = 910 / 7
children = 230 - adults
print(adults, children)
print(adults + children == 230)
print(12 * adults + 5 * children == 2060)
```

Both are `True`. Checking only the equation we used in step 4 would
prove little, since we built $c$ from it. The second check is the one
that counts.

### Your turn

A juice bar sells small smoothies for €4 and large ones for €6. One
morning it sold 45 smoothies and took €222.

1. Name the two unknowns, and write the two facts as equations.
2. Eliminate one unknown, by hand, in the steps above.
3. Substitute your answer back into both equations in the cell below.

```python exec
id: several-unknowns-elimination-your-turn
# Your two unknowns, and the check in both equations
```

## One formula for every pair

Elimination is the same four steps every time, so we can do it once,
with letters, and get a formula. Write any two such equations as

$$a_1 x + b_1 y = c_1$$
$$a_2 x + b_2 y = c_2$$

The small numbers are part of the names: $a_1$ is "the $a$ of the first
equation". To eliminate $y$, multiply the first equation by $b_2$ and
the second by $b_1$, then take one from the other. The $y$ terms cancel
and leave

$$x = \frac{c_1 b_2 - c_2 b_1}{a_1 b_2 - a_2 b_1}$$

Eliminating $x$ the same way gives

$$y = \frac{a_1 c_2 - a_2 c_1}{a_1 b_2 - a_2 b_1}$$

This pair of formulas is called *Cramer's rule*. Both share the same
bottom, $a_1 b_2 - a_2 b_1$, which is called the *determinant*. In
words: write the four numbers in front of $x$ and $y$ in a square, with
$a_1$ and $b_1$ on top and $a_2$ and $b_2$ below. Multiply along one
diagonal, $a_1$ times $b_2$, then along the other, $a_2$ times $b_1$,
and take the second product from the first.

A fraction with 0 on the bottom has no answer. So when the determinant
is 0, the formulas cannot give a single answer, and the next section
shows what that means. Here is the promise for your toolkit. It gives
back `None`, Python's "nothing here", when there is no single answer.

```python exec
id: several-unknowns-toolkit
toolkit: yes
def solve_simultaneous(a1, b1, c1, a2, b2, c2):
    """Return the pair (x, y) where a1x + b1y = c1 and a2x + b2y = c2.

    Return None when there is no single answer: the determinant
    a1*b2 - a2*b1 is 0.
    """
    ...
```

```python toolkit-reference
for: several-unknowns-toolkit
def solve_simultaneous(a1, b1, c1, a2, b2, c2):
    """Return the pair (x, y) where a1x + b1y = c1 and a2x + b2y = c2.

    Return None when there is no single answer: the determinant
    a1*b2 - a2*b1 is 0.
    """
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None
    x = (c1 * b2 - c2 * b1) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    return (x, y)
```

```hint
after: 10 errors
title: some steps
1. Work out the determinant, `a1 * b2 - a2 * b1`, and give it a name.
2. If it is 0, return `None` straight away.
3. Otherwise work out `x` and `y` from the two formulas above, each
   divided by the determinant, and return the pair `(x, y)`.

**Think about:** why must the check for 0 come before the two
divisions, and not after?
```

The tests start with the concert. The last one makes up two equations
from an answer we choose, and checks that the tool finds that answer
again. Until your function is written, the first test stops with an
error.

```python exec
id: several-unknowns-toolkit-tests
assert solve_simultaneous(1, 1, 230, 12, 5, 2060) == (130, 100)
assert solve_simultaneous(1, 1, 10, 2, -1, 5) == (5, 5)
assert solve_simultaneous(2, 4, 10, 1, 2, 5) is None

x, y = solve_simultaneous(3, -2, 3 * 1.5 - 2 * 4, 1, 5, 1.5 + 5 * 4)
assert close_enough(x, 1.5) and close_enough(y, 4)
print("solve_simultaneous keeps its promise.")
```

In the concert test, the determinant is $1 \times 5 - 12 \times 1 = -7$,
the same 7 that elimination divided by, with its sign turned round.

## When there is no single answer

Two fans are counting their spending at a concert. The first says three
T-shirts and two posters cost €80. The second says six T-shirts and
four posters cost €150. What does `solve_simultaneous` make of that?

```python exec
id: several-unknowns-none-1
print(solve_simultaneous(3, 2, 80, 6, 4, 150))
print(3 * 4 - 6 * 2)
```

It gives back `None`, because the determinant is 0. Let's draw the two
facts as rules that give the poster price from the T-shirt price. What
will the lines do?

```python exec
id: several-unknowns-none-2
def poster_from_first_fan(shirt):
    return (80 - 3 * shirt) / 2

def poster_from_second_fan(shirt):
    return (150 - 6 * shirt) / 4

plot_rule(poster_from_first_fan, 0, 25)
plot_rule(poster_from_second_fan, 0, 25)
plt.xlabel("T-shirt price")
plt.ylabel("poster price")
plt.legend()
```

The lines are *parallel*: they have the same steepness, and never meet.
No pair of prices fits both facts. Six T-shirts and four posters are
twice three and two, so they should cost twice €80, which is €160. One
of the fans has it wrong, or had a discount.

If the second fan had said €160, the two equations would be one fact
said twice, and the two lines would be the same line. Every point on it
fits, so there are endless answers and still no single one. The
determinant is 0 in both cases, and `None` covers both.

So two straight lines on a flat plane can meet in three ways: once,
never, or everywhere. That is what this space allows, and the
determinant tells us which kind we have before we draw anything.

```question
id: several-unknowns-none-3
type: multiple-choice
correct: 3

Which pair of equations has no single solution?

- $x + y = 4$ and $x - y = 2$
- $2x + y = 7$ and $x + 2y = 8$
- $x + 3y = 5$ and $2x + 6y = 9$
```

## Three unknowns

A café's three orders are on the till receipts, but the prices of a
coffee, a scone and a juice are not:

- 2 coffees, 1 scone and 1 juice cost €12.50;
- 1 coffee, 2 scones and 1 juice cost €11.50;
- 1 coffee, 1 scone and 2 juices cost €12.00.

Three unknowns need three facts. Elimination works the same way, one
unknown at a time. Taking the second order from the first eliminates
the juice: $c - s = 1$. Taking the third from twice the second
eliminates it again: $c + 3s = 11$. Now there are two equations in two
unknowns, and your toolkit can finish the job. (This cell needs your
`solve_simultaneous`.) What do you expect?

```python exec
id: several-unknowns-three-1
coffee, scone = solve_simultaneous(1, -1, 12.50 - 11.50, 1, 3, 2 * 11.50 - 12.00)
juice = 12.50 - 2 * coffee - scone
print(coffee, scone, juice)

print(2 * coffee + scone + juice, coffee + 2 * scone + juice, coffee + scone + 2 * juice)
```

A coffee is €3.50, a scone €2.50 and a juice €3.00, and all three
orders check out. The big job was made of smaller promises: two
eliminations, one call to `solve_simultaneous`, and one substitution.

For more unknowns, the same idea is written with grids of numbers
called matrices, and numpy has a tool for it, `np.linalg.solve`. It
takes the numbers in front of the unknowns, one row for each equation,
and the totals.

```python exec
id: several-unknowns-three-2
import numpy as np

orders = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
totals = [12.50, 11.50, 12.00]
print(np.linalg.solve(orders, totals))
```

The same three prices. The Computational Methods course works with
these grids in depth, starting at
[Matrices: adding, scaling and transposing a grid of numbers](tutorial:grid-of-numbers).

<details class="dl-why"><summary>Why this way?</summary>

This page put Cramer's rule in the toolkit: one formula for the answer
to two equations. Most programs that solve equations do not use it.
They do elimination step by step on a grid of numbers, as
`np.linalg.solve` does.

Step-by-step elimination is the better method for many unknowns. It
works the same way for 3 or 300, and Cramer's rule becomes very slow as
the number of unknowns grows.

We used the formula because, for two unknowns, it shows the whole
method at once, and its bottom line, the determinant, says in one
number whether there is a single answer. The cost is that it does not
grow: for three unknowns we had to eliminate by hand first.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | $a$ and $c$ for counts nobody kept; $a_1$, $b_1$, $c_1$ for the numbers of the first equation; the determinant |
| What is promised? | the solution makes every equation true at once; `solve_simultaneous` promises that pair, or `None` |
| What happens when? | elimination first finds one unknown, and only then the other; three unknowns become two, and then one |
| What does this space let us do? | two straight lines on a flat plane cross once, never, or everywhere; a determinant of 0 means never or everywhere |

## What we have now

| Term or tool | What it means |
|---|---|
| simultaneous equations | equations that must all be true at once, for the same unknowns |
| solution | the values that make every equation true |
| elimination | combining equations so that one unknown cancels out |
| Cramer's rule | a formula for $x$ and $y$ from the six numbers of two equations |
| determinant | $a_1 b_2 - a_2 b_1$; when it is 0 there is no single answer |
| parallel lines | lines with the same steepness, which never meet |
| `solve_simultaneous(a1, b1, c1, a2, b2, c2)` | your toolkit tool: the pair $(x, y)$, or `None` |
| `np.linalg.solve(rows, totals)` | numpy's solver, for any number of unknowns |

For another route through the same ideas, the integrated course has
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations#simultaneous-equations).
