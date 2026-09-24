---
title: "Solving for x: linear and quadratic equations"
year: "2026-2027"
version: 2026.09.24.1
covers:
  when-do-two-plans-cost-the-same:
    covers: [MIT-1.9]
    touches: [MIT-1.7]
  a-tool-for-any-straight-line-equation:
    covers: [MIT-1.9]
    touches: [PDP-LO8]
  when-the-unknown-is-squared:
    covers: [MIT-1.9]
  factorising-by-inspection:
    covers: [MIT-1.9]
  the-quadratic-formula:
    covers: [MIT-1.9]
  how-many-answers-the-discriminant:
    covers: [MIT-1.9]
    touches: [PDP-LO8, PDP-LO10]
  when-the-square-root-says-no:
    touches: [MIT-1.10, PDP-LO9]
---

# Solving for x: linear and quadratic equations

A phone company has three plans. Plan A costs €8 a month, plus €2 for
each gigabyte of data. Plan B costs €20, however much you use. Plan C
costs €15, plus €1.20 a gigabyte. On
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
the graphs of plans A and B crossed at about 6 gigabytes. When do plans
A and C cost the same? A graph can only say "about". Can we find the
exact answer, and be sure of it?

On this page we:

- find where two plans cost the same, by a table and then by undoing
- write `solve_linear` for any equation of the form $ax + b = 0$
- solve an equation with a square in it by spotting two numbers
- say the quadratic formula in words, then in symbols, then in code
- count a quadratic's answers first, with the discriminant
- see `math.sqrt` refuse a negative number, and ask what that means

> **The space we're in.** The real numbers, $\mathbb{R}$: every point
> on the number line. A letter in an equation is a name for a number we
> do not know yet, and every answer is checked by putting it back in.
> One thing usually goes unsaid: an
> equation can have one answer, two, none, or every number as an
> answer. Your toolkit is loaded, with `evaluate` and `plot_rule` from
> the last two pages, and `close_enough` from
> [Does it work?](tutorial:does-it-work).

## Warm-up

The first question is from
[Running a formula backwards](tutorial:running-a-formula-backwards#undoing-in-reverse-order),
and the second from
[Rules with letters in them](tutorial:rules-with-letters-in-them#putting-a-number-in-for-the-letter).

```question
id: solving-warm-up-1
type: fill-in-the-blank

A taxi meter multiplies the distance by 1.5, then adds 4. To undo it,
we first {subtract 4|divide by 1.5|add 4}.
```

```question
id: solving-warm-up-2
type: multiple-choice
correct: 3

The list `[6, 5, 1]` stands for $6 + 5x + x^2$, lowest power first.
What does `evaluate([6, 5, 1], 2)` give?

- 13
- 16
- 20
- 32
```

## When do two plans cost the same?

Let's start with plans A and B. Call the number of gigabytes $g$. Here
$g$ is a name for a number we do not know yet. On
[Rules with letters in them](tutorial:rules-with-letters-in-them#a-rule-a-question-and-a-promise),
an equation was a question, and solving it meant finding the values
that make it true. "When do A and B cost the same?" is this equation:

$$8 + 2g = 20$$

On [Running a formula backwards](tutorial:running-a-formula-backwards#the-same-move-on-both-sides)
we kept a formula true by doing the same move to both sides. The same
rule works here. First, subtract 8 from both sides: $2g = 12$. Then
divide both sides by 2: $g = 6$. The graph's "about 6" is exactly 6.

Now plans A and C. A table first. Before you run it, guess where the
two plans meet.

```python exec
id: solving-plans-1
for gigabytes in range(0, 13):
    plan_a = 8 + 2 * gigabytes
    plan_c = 15 + 1.2 * gigabytes
    print(gigabytes, plan_a, round(plan_c, 2))
```

At 8 gigabytes, plan A is cheaper. At 9, plan C is. The two plans meet
somewhere between, and the table cannot say where. So let's write the
equation:

$$8 + 2g = 15 + 1.2g$$

This time $g$ is on both sides. The same rule still works, one move at
a time:

1. Subtract $1.2g$ from both sides: $8 + 0.8g = 15$.
2. Subtract 8 from both sides: $0.8g = 7$.
3. Divide both sides by 0.8: $g = 8.75$.

The rule of this unit is that every answer is checked. We put it back
into both sides and see if they agree. What do you expect?

```python exec
id: solving-plans-2
gigabytes = 7 / 0.8
print(gigabytes)
print(8 + 2 * gigabytes, 15 + 1.2 * gigabytes)
```

`8.75`, and both plans cost €25.50 there. Below 8.75 gigabytes plan A
is cheaper, and above it plan C is. Each side of this equation has
degree 1, so it is a *linear equation*: the unknown is only multiplied
by a number and added to. Its graph, as on the last page, is a straight
line.

## A tool for any straight-line equation

Every linear equation can be tidied into one shape. Subtract 15 from
both sides of $8 + 0.8g = 15$, and it becomes

$$0.8g - 7 = 0$$

That is the shape $ax + b = 0$, with $a = 0.8$ and $b = -7$. In maths
the letters $a$ and $b$ are the usual names for these two numbers, so
our code uses them too.

Now solve $ax + b = 0$ once, for every $a$ and $b$. In words: first
subtract $b$ from both sides, then divide both sides by $a$.

$$x = -\frac{b}{a}$$

There is one space to watch. If $a$ is 0, the equation says $0x + b = 0$.
When $b$ is 5, no $x$ works, because $0x$ is always 0. When $b$ is 0,
every $x$ works. Either way there is no single answer, and dividing by
$a$ would stop with a `ZeroDivisionError`. So the promise says what to
give back instead: `None`, Python's value for "nothing here".

Can you write the body? It needs an `if` for the case where `a` is 0,
then one line for every other case.

```python exec
id: solving-toolkit-linear
toolkit: yes
def solve_linear(a, b):
    """Return the x where a*x + b = 0.

    When a is 0 there is no single answer, so return None.
    """
    ...
```

```python toolkit-reference
for: solving-toolkit-linear
def solve_linear(a, b):
    """Return the x where a*x + b = 0.

    When a is 0 there is no single answer, so return None.
    """
    if a == 0:
        return None
    return -b / a
```

The tests check three known answers. Then the loop checks each answer
the way this unit always will: it substitutes the answer back. The rule
$ax + b$ is a polynomial with two coefficients, so `evaluate([b, a], x)`
works it out. Until your `solve_linear` is written, this cell stops
with an error.

```python exec
id: solving-toolkit-linear-tests
assert solve_linear(0.8, -7) == 8.75
assert solve_linear(2, 6) == -3
assert solve_linear(0, 5) is None

for a, b in [(0.8, -7), (2, -12), (5, -35), (3, 7), (-2.5, 4)]:
    x = solve_linear(a, b)
    assert close_enough(evaluate([b, a], x), 0), (a, b, x)
print("solve_linear keeps its promise.")
```

```hint
What does `print(solve_linear(2, 6))` show? If it shows `None`, the
last line of the function is not written yet. It starts with `return`.
```

### Your turn

A swimming pool charges €7 a visit. A membership costs €35 a month,
plus €2 a visit.

1. Write the equation for "the two cost the same", with $v$ for the
   number of visits in a month.
2. Tidy it into the shape $av + b = 0$. What are $a$ and $b$?
3. Solve it with `solve_linear`, and substitute the answer back.

```python exec
id: solving-linear-your-turn
# The pool: solve, then substitute back
```

## When the unknown is squared

An allotment plot is a rectangle, 3 m longer than it is wide, and it
covers 40 square metres. How wide is it?

Call the width $w$. Then the length is $w + 3$, and the area is width
times length:

$$w(w + 3) = 40$$

Can the same moves as before solve it? Multiply out the bracket and
subtract 40:

$$w^2 + 3w - 40 = 0$$

Now $w$ appears twice, once squared, and no single move gets it alone.
An equation of the shape $ax^2 + bx + c = 0$, where $a$ is not 0, is a
*quadratic equation*: its left side is a quadratic, of degree 2. The
numbers that make it true are its roots. As on
[Drawing a rule](tutorial:drawing-a-rule#a-tool-that-draws-any-rule),
a root is a place where the graph meets the x-axis.

Let's try a table first. What width do you expect?

```python exec
id: solving-allotment-1
for width in range(0, 9):
    print(width, width * (width + 3))
```

A width of 5 m gives exactly 40. The table worked because the answer is
a whole number. Here is a way that does not need luck.

## Factorising by inspection

On [Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop)
we expanded brackets. Two brackets like $(x + p)(x + q)$ expand to

$$x^2 + (p + q)x + pq$$

So if we can find two numbers $p$ and $q$ that add to make 3 and
multiply to make $-40$, then $w^2 + 3w - 40$ is $(w + p)(w + q)$.
Writing an expression as brackets multiplied together is called
*factorising*. It is expanding, run backwards. Finding the two numbers
by looking and thinking is *factorising by inspection*.

Can you find the pair in your head? Then the cell tries every pair of
whole numbers from −40 to 40, and prints the ones that work.

```python exec
id: solving-inspection-1
target_sum = 3
target_product = -40

for p in range(-40, 41):
    for q in range(-40, 41):
        if p + q == target_sum and p * q == target_product:
            print(p, q)
```

The pair is −5 and 8, found twice, once in each order. So

$$w^2 + 3w - 40 = (w - 5)(w + 8) = 0$$

Now one fact does the rest. If two numbers multiply to make 0, then one
of them must be 0. So either $w - 5 = 0$, which gives $w = 5$, or
$w + 8 = 0$, which gives $w = -8$.

Two roots. Which one answers the question? A width is a length, and a
length is never negative. The equation lives in all of $\mathbb{R}$,
and the allotment lives in the numbers from 0 up. So it is 5 m wide
and 8 m long. We check both roots anyway. What do you expect?

```python exec
id: solving-inspection-2
allotment = [-40, 3, 1]
print(evaluate(allotment, 5), evaluate(allotment, -8))
```

Both give 0, so both are roots. Only one of them is an allotment.

### Your turn

1. Factorise $x^2 + 7x + 12$ by inspection, in your head. Which two
   numbers add to 7 and multiply to 12?
2. Change `target_sum` and `target_product` in the cell above to check.
3. Now try $x^2 - x - 6$. What are its two roots? Substitute both back
   with `evaluate`.

## The quadratic formula

Inspection works well when the roots are whole numbers. Often they are
not. A photo 20 cm wide and 30 cm tall goes in a frame with a border of
the same width, $x$ cm, all the way round. The framed picture must
cover 1,000 square centimetres. How wide is the border?

The framed picture is $20 + 2x$ wide and $30 + 2x$ tall, so

$$(20 + 2x)(30 + 2x) = 1000$$

Expanding the brackets and subtracting 1,000 gives

$$4x^2 + 100x - 400 = 0$$

No pair of whole numbers factorises that. We need a method that always
works.

The *quadratic formula* gives the roots of $ax^2 + bx + c = 0$. Here it
is in words first:

1. Square $b$, and take away four times $a$ times $c$.
2. Take the square root of that.
3. Add it to $-b$ for one root, and take it away from $-b$ for the other.
4. Divide each by two times $a$.

And in symbols, where $\pm$ means "plus for one root, minus for the
other":

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

The fold near the end of this page says where the formula comes from.
Here we check it instead. Here are the four steps for the frame, one
line each. Before you run it, guess: is the border more or
less than 5 cm?

```python exec
id: solving-formula-1
import math

a, b, c = 4, 100, -400
under_the_root = b ** 2 - 4 * a * c
root = math.sqrt(under_the_root)
print((-b + root) / (2 * a))
print((-b - root) / (2 * a))
```

The two roots are about 3.51 and −28.51. The border is about 3.5 cm
wide. A border of −28.5 cm means nothing, so, as with the allotment,
the equation has two answers and the question has one. Let's check the
border in the frame:

```python exec
id: solving-formula-2
border = (-b + root) / (2 * a)
print((20 + 2 * border) * (30 + 2 * border))
```

`1000.0`: the framed picture covers 1,000 square centimetres.

## How many answers? The discriminant

The part under the square root, $b^2 - 4ac$, is called the
*discriminant*. It tells us how many roots there are before we look for
them. Here are three quadratics that differ only in their last number.
Predict the discriminant of each, and how many roots it has.

```python exec
id: solving-discriminant-1
for c in [5, 9, 13]:
    print("x² - 6x +", c, "has discriminant", (-6) ** 2 - 4 * 1 * c)
```

The discriminants are 16, 0 and −16. Each has a meaning:

| Discriminant | Roots | Why |
|---|---|---|
| more than 0 | two | the root is added once and taken away once |
| exactly 0 | one | adding 0 and taking away 0 agree |
| less than 0 | none on the number line | no real number squares to a negative |

A picture says the same. What do you expect to see?

```python exec
id: solving-discriminant-2
import matplotlib.pyplot as plt

def two_roots(x):
    return x ** 2 - 6 * x + 5

def one_root(x):
    return x ** 2 - 6 * x + 9

def no_roots(x):
    return x ** 2 - 6 * x + 13

plot_rule(two_roots, 0, 6)
plot_rule(one_root, 0, 6)
plot_rule(no_roots, 0, 6)
plt.legend()
```

The first curve crosses the axis twice, at 1 and 5. The second touches
it once, at 3. The third never comes down to it.

Now the formula can go in your toolkit. `solve_quadratic` promises a
list of the real roots, smallest first: two, one, or none. Here are the
steps for the body:

1. Work out the discriminant.
2. If it is less than 0, return an empty list, `[]`.
3. If it is 0, return a list holding the one root, $-\frac{b}{2a}$.
4. Otherwise, work out both roots with `math.sqrt`, and return them in
   a list, smallest first. `sorted` from
   [What is typical?](tutorial:what-is-typical) puts them in order.

```python exec
id: solving-toolkit-quadratic
toolkit: yes
import math


def solve_quadratic(a, b, c):
    """Return a list of the real x where a*x**2 + b*x + c = 0, smallest first.

    The list holds 2, 1 or 0 roots. a must not be 0.
    """
    ...
```

```python toolkit-reference
for: solving-toolkit-quadratic
import math


def solve_quadratic(a, b, c):
    """Return a list of the real x where a*x**2 + b*x + c = 0, smallest first.

    The list holds 2, 1 or 0 roots. a must not be 0.
    """
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return []
    if discriminant == 0:
        return [-b / (2 * a)]
    root = math.sqrt(discriminant)
    return sorted([(-b - root) / (2 * a), (-b + root) / (2 * a)])
```

The tests check the three kinds of answer, then substitute every root
back in. Until `solve_quadratic` is written, this cell stops with an
error.

```python exec
id: solving-toolkit-quadratic-tests
assert solve_quadratic(1, 3, -40) == [-8, 5], "the allotment"
assert solve_quadratic(1, -6, 9) == [3]
assert solve_quadratic(1, -6, 13) == []

for a, b, c in [(1, 3, -40), (-4.9, 14, 1), (2, -7, 3), (1, -4, 1), (1, -6, 9)]:
    for x in solve_quadratic(a, b, c):
        assert close_enough(evaluate([c, b, a], x), 0), (a, b, c, x)
print("solve_quadratic keeps its promise.")
```

```hint
Try `print(solve_quadratic(1, 3, -40))` on its own. Is it a list? Are
the two roots in order, smallest first?
```

```hint
after: 10 errors
title: some steps
1. The first line of the body is `discriminant = b ** 2 - 4 * a * c`.
2. Then `if discriminant < 0:` and, pushed in, `return []`.
3. Then the same for `== 0`, returning `[-b / (2 * a)]`.
4. Last, `root = math.sqrt(discriminant)`, and return both roots
   inside `sorted([...])`.

**Think about:** when $a$ is negative, as in the test
$-4.9x^2 + 14x + 1$, which of
$-b + \sqrt{\ }$ and $-b - \sqrt{\ }$ gives the smaller root?
```

### Your turn

1. Before you run anything, work out the discriminant of
   $2x^2 - 7x + 3$. How many roots will it have?
2. Check with `solve_quadratic(2, -7, 3)`.
3. Can you factorise it? Its roots give a hint: $(2x - 1)(x - 3)$.
   Multiply it out to check.

## When the square root says no

What if `solve_quadratic` did not check the discriminant first? Here is
the frame's cell again, for $x^2 + 1 = 0$. This cell is meant to stop with an error. Before you run
it, which line do you think will stop it?

```python exec
id: solving-no-root-1
a, b, c = 1, 0, 1
under_the_root = b ** 2 - 4 * a * c
print(under_the_root)
root = math.sqrt(under_the_root)
```

It prints `-4`, and then stops at the last line with
`ValueError: math domain error`. We met this message on
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out):
the value is a number, but outside what `math.sqrt` accepts.

$x^2 + 1 = 0$ asks for a number that squares to make −1. In
$\mathbb{R}$ there is none, so `solve_quadratic` is right to give back
`[]`.

But is asking the question a foolish move? On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#families-of-numbers),
$3 - 5$ had no answer in $\mathbb{N}$, and it had one in a bigger
space, $\mathbb{Z}$. So the question to ask is this: which space would
$x^2 = -1$ have an answer in? The next page builds it.

<details class="dl-why"><summary>Why this way?</summary>

This page gave the quadratic formula without deriving it. It said the
formula in words, then checked every root it gave by putting the root
back into the equation.

The usual route is to derive the formula by completing the square:
rewriting $ax^2 + bx + c$ so that $x$ appears only once, inside a
square, and then undoing. That route shows where every part of the
formula comes from, and it is the route most textbooks take.

We checked instead of deriving because a check is something a reader
can run, on any equation, and trust. The cost is that the formula
arrives as a fact from outside, and a reader who forgets it cannot
rebuild it.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a letter, $g$, $w$ or $x$, for a number we do not know yet; $a$, $b$ and $c$ for the numbers in an equation; roots |
| What is promised? | `solve_linear` gives the one answer, or `None`; `solve_quadratic` gives every real root, smallest first; every answer is checked by substituting it back |
| What happens when? | the same move on both sides, one step at a time; the discriminant is worked out before any square root is taken |
| What does this space let us do? | in $\mathbb{R}$, $x^2 = -1$ has no answer and `math.sqrt` refuses; a width lives in the numbers from 0 up, so one root may not fit the question |

## What we have now

| Term or tool | What it means |
|---|---|
| linear equation | the unknown is only multiplied by a number and added to; $ax + b = 0$ has the one answer $x = -\frac{b}{a}$ when $a$ is not 0 |
| quadratic equation, root | $ax^2 + bx + c = 0$ with $a$ not 0; a number that makes it true |
| factorising by inspection | finding two numbers that add to $b$ and multiply to $c$, so that $x^2 + bx + c = (x + p)(x + q)$ |
| if two numbers multiply to 0 | one of them is 0 |
| quadratic formula | $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ |
| discriminant | $b^2 - 4ac$: more than 0 gives two roots, 0 gives one, less than 0 gives none in $\mathbb{R}$ |
| `solve_linear(a, b)` | your toolkit tool for $ax + b = 0$ |
| `solve_quadratic(a, b, c)` | your toolkit tool: the real roots, as a list, smallest first |

For another route through these equations, the integrated course has
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).
