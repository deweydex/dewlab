---
title: "Solving for x: linear and quadratic equations"
year: "2026-2027"
version: 2026.09.25.1
covers:
  when-are-two-servers-equally-fast:
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

On
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
three servers raced to answer an app's requests. Server A takes 8 ms,
plus 2 ms for every thousand people using the app. Server B takes
20 ms, however many people there are. Server C takes 15 ms, plus 1.2 ms
for every thousand. The graphs of A and B crossed at about 6 thousand
people, and A and C somewhere near 9. A graph can only say "about".
Can we find the exact crowd where A and C are equally fast, and be sure
of it?

And a second question, with a ball in it: a footballer volleys a ball
upwards. When does it land? This one has a square in it, and a square
changes everything.

On this page we:

- find where two servers are equally fast, by a table and then by
  undoing
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

A temperature chip's rule multiplies the volts by 100, then subtracts 50.
To undo it, we first {add 50|divide by 100|subtract 50}.
```

```question
id: solving-warm-up-2
type: multiple-choice
answer: 3

The list `[6, 5, 1]` stands for $6 + 5x + x^2$, lowest power first.
What does `evaluate([6, 5, 1], 2)` give?

- 13
  - This counts x only once; the 1 belongs to x², so it gives 1 × 2 × 2.
- 16
  - 6 + 5 × 2 leaves out the x² part: 1 × 2² adds 4 more.
- 20
  - 6 + 5 × 2 + 1 × 2²: 6 + 10 + 4.
- 32
  - The three parts are 6, 5 × 2 and 1 × 2²; this total is more than all three together.
```

## When are two servers equally fast?

Let's start with servers A and B. Call the number of people, in
thousands, $g$. Here $g$ is a name for a number we do not know yet. On
[Rules with letters in them](tutorial:rules-with-letters-in-them#a-rule-a-question-and-a-promise),
an equation was a question, and solving it meant finding the values
that make it true. "When are A and B equally fast?" is this equation:

$$8 + 2g = 20$$

On [Running a formula backwards](tutorial:running-a-formula-backwards#the-same-move-on-both-sides)
we kept a formula true by doing the same move to both sides. The same
rule works here. First, subtract 8 from both sides: $2g = 12$. Then
divide both sides by 2: $g = 6$. The graph's "about 6" is exactly 6.

<aside class="dl-note" id="solving-note-al-jabr">

**Where "algebra" comes from.** Around the year 820, in Baghdad,
Muhammad ibn Musa al-Khwarizmi wrote a book on solving equations. Its
title has the word *al-jabr*, "restoring": moving a term that is taken
away on one side over to the other, where it is added. That word became
*algebra*, and his own name became *algorithm*.

</aside>

Now servers A and C. A table first. Before you run it, guess where the
two meet.

```python exec
id: solving-servers-1
for thousands in range(0, 13):
    server_a = 8 + 2 * thousands
    server_c = 15 + 1.2 * thousands
    print(thousands, server_a, round(server_c, 2))
```

At 8 thousand people, server A is faster. At 9, server C is. The two
meet somewhere between, and the table cannot say where. So let's write
the equation:

$$8 + 2g = 15 + 1.2g$$

This time $g$ is on both sides. The same rule still works, one move at
a time:

1. Subtract $1.2g$ from both sides: $8 + 0.8g = 15$.
2. Subtract 8 from both sides: $0.8g = 7$.
3. Divide both sides by 0.8: $g = 8.75$.

The rule of this unit is that every answer is checked. We put it back
into both sides and see if they agree. What do you expect?

```python exec
id: solving-servers-2
thousands = 7 / 0.8
print(thousands)
print(8 + 2 * thousands, 15 + 1.2 * thousands)
```

`8.75`, and both servers take 25.5 ms there. Below 8,750 people server
A is faster, and above it server C is. Each side of this equation has
degree 1, so it is a *linear equation*: the unknown is only multiplied
by a number and added to. Each side, drawn as on the last page, is a
straight line, and the answer is where the two lines cross.

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

# the servers, the gallery page from Rules with letters in them, and more
for a, b in [(0.8, -7), (2, -12), (7, -700), (0.6, -30), (3, 7), (-2.5, 4)]:
    x = solve_linear(a, b)
    assert close_enough(evaluate([b, a], x), 0), (a, b, x)
print("solve_linear keeps its promise.")
```

```hint
What does `print(solve_linear(2, 6))` show? If it shows `None`, the
last line of the function is not written yet. It starts with `return`.
```

### Your turn

Two phones are charging. Phone A is at 20% and gains 1.5% a minute.
Phone B is at 50% and gains 0.9% a minute. (A steady rate is a model:
real phones charge more slowly as they fill.)

1. Write the equation for "the two show the same charge", with $m$ for
   the minutes.
2. Tidy it into the shape $am + b = 0$. What are $a$ and $b$?
3. Solve it with `solve_linear`, and substitute the answer back.

```python exec
id: solving-linear-your-turn
# The phones: solve, then substitute back
```

## When the unknown is squared

A game keeps its small pictures, its *sprites*, side by side in one
image called a sprite sheet. One sprite sheet holds 40 tiles in a
rectangle, with 3 more columns than rows. How many rows are there?

Call the number of rows $w$. Then there are $w + 3$ columns, and the
number of tiles is rows times columns:

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

Let's try a table first. How many rows do you expect?

```python exec
id: solving-sprites-1
for rows in range(0, 9):
    print(rows, rows * (rows + 3))
```

5 rows give exactly 40 tiles. The table worked because the answer is a
whole number. Here is a way that does not need luck.

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

Two roots. Which one answers the question? A count of rows is never
negative. The equation lives in all of $\mathbb{R}$, and the sprite
sheet lives in the whole numbers from 0 up. So it has 5 rows and 8
columns. We check both roots anyway. What do you expect?

```python exec
id: solving-inspection-2
sprite_sheet = [-40, 3, 1]
print(evaluate(sprite_sheet, 5), evaluate(sprite_sheet, -8))
```

Both give 0, so both are roots. Only one of them is a sprite sheet.

### Your turn

1. Factorise $x^2 + 7x + 12$ by inspection, in your head. Which two
   numbers add to 7 and multiply to 12?
2. Change `target_sum` and `target_product` in the cell above to check.
3. Now try $x^2 - x - 6$. What are its two roots? Substitute both back
   with `evaluate`.

## The quadratic formula

Inspection works well when the roots are whole numbers. Often they are
not. Back to the footballer. The ball leaves the boot 1 m above the
grass, rising at 14 metres a second. Gravity slows it by 9.8 metres a
second, every second. Leaving out the air, its height after $t$
seconds is

$$1 + 14t - 4.9t^2$$

metres. (The 4.9 is half of 9.8.) When does it land? It lands when its
height is 0:

$$-4.9t^2 + 14t + 1 = 0$$

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

Where the formula comes from is on
[The top of the curve](tutorial:the-top-of-the-curve#completing-the-square).
Here we check it instead. Here are the four steps for the ball, one
line each. Before you run it, guess: is the ball in the air for more
than 3 seconds, or less? I'll wait.

```python exec
id: solving-formula-1
import math

a, b, c = -4.9, 14, 1
under_the_root = b ** 2 - 4 * a * c
root = math.sqrt(under_the_root)
print((-b + root) / (2 * a))
print((-b - root) / (2 * a))
```

The two roots are about −0.07 and 2.93. The ball lands a little before
3 seconds. What is the other root? It is a time 0.07 seconds *before*
the kick. The rule's curve, run backwards, would have left the grass
then; the real ball was still on the boot. So, as with the sprite
sheet, the equation has two answers and the question has one. Let's
put the landing time back into the rule:

```python exec
id: solving-formula-2
landing = (-b - root) / (2 * a)
print(landing, 1 + 14 * landing - 4.9 * landing ** 2)
```

`0.0`: at 2.93 seconds the ball is back on the grass.

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
assert solve_quadratic(1, 3, -40) == [-8, 5], "the sprite sheet"
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
the ball's cell again, for $x^2 + 1 = 0$. This cell is meant to stop
with an error. Before you run it, which line do you think will stop it?

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
$\mathbb{R}$ there is none, so `solve_quadratic` keeps its promise by
giving back `[]`.

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
arrives here as a fact from outside. Two pages on,
[The top of the curve](tutorial:the-top-of-the-curve#completing-the-square)
builds it.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a letter, $g$, $w$ or $x$, for a number we do not know yet; $a$, $b$ and $c$ for the numbers in an equation; roots |
| What is promised? | `solve_linear` gives the one answer, or `None`; `solve_quadratic` gives every real root, smallest first; every answer is checked by substituting it back |
| What happens when? | the same move on both sides, one step at a time; the discriminant is worked out before any square root is taken |
| What does this space let us do? | in $\mathbb{R}$, $x^2 = -1$ has no answer and `math.sqrt` refuses; a count of rows lives in the whole numbers, and a landing time comes after the kick, so one root may not fit the question |

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

## Where to read more

Welch Labs (2015). *Imaginary Numbers Are Real [Part 3: Cardan's
Problem].* <https://www.youtube.com/watch?v=N9QOLrfcKNc>. The quadratic
formula has an older cousin for cubic equations. This short video tells
how people found it, and the strange square roots it needed. Five minutes.
