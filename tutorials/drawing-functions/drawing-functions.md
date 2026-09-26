---
title: "Functions and their graphs"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-function-is-a-machine:
    covers: [MIT-3.1]
  a-machine-has-a-picture:
    covers: [MIT-3.2]
  straight-lines:
    covers: [MIT-3.2]
  curves-that-bend:
    covers: [MIT-3.2]
  reading-an-answer-off-the-picture:
    covers: [MIT-3.2]
  undoing-a-function:
    covers: [MIT-3.1]
---

# Functions and their graphs

We have written functions since
[Writing your own functions](tutorial:writing-your-own-functions). We
have drawn charts of data since
[Charts: choosing the right chart for your data](tutorial:pictures-worth-numbers).
In [Complex numbers: roots that are not real](tutorial:complex-roots) we
drew three curves, to see why a quadratic can have no real roots.

On this page we put those two skills together, on purpose. We draw a
function, and we learn to read answers from the picture. Much of the
rest of the course depends on this habit. Trigonometry, limits and
derivatives all use graphs. Once you can draw a function and read an
answer from it, those topics become much less abstract.

In [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
we wrote a function that finds a polynomial's value. We never drew
its output. Now we can.

On this page we:

- see what makes something a function in mathematics
- draw any function as a curve
- see what each number in a line and in a quadratic does to the picture
- solve equations by reading where curves cross
- undo a function, and see when that is not possible

## A function is a machine

The word "function" has two meanings in this course, one in Python and
one in mathematics. How are they related?

In Python, a function is a piece of code with a name. In mathematics, a
function is a rule that takes an input and gives exactly one
output. These are the same idea, and the mathematical meaning is the
stricter of the two.

The important part is "exactly one output". A function must give the
same answer every time we give it the same input. If it does not, it is
not a function in the mathematical sense.

Look at the last three rows in the output. What do you notice?

```python exec
id: a-function-is-a-machine-1
def double(x):
    return x * 2


def square(x):
    return x ** 2


for value in [-2, 0, 3, 3, 3]:
    print(f"double({value}) = {double(value):>4}    square({value}) = {square(value)}")
```

The input 3 appears three times, and it gives the same output each time.
That may sound too obvious to mention. Now look at something that does
not behave that way. What do you think `roll(1)` will print each time?

```python exec
id: a-function-is-a-machine-2
import random

def roll(x):
    return random.randint(1, 6)


for _ in range(4):
    print("roll(1) =", roll(1))
```

`roll` is good Python code, but it is not a function in the mathematical
sense. We give it 1 each time, and the answers change. Run the cell
again and you will probably see a different list.

**`roll` has no graph.** A graph shows one height above each $x$. There
is no single height above $x = 1$ for `roll`, so we cannot draw it.

In [Writing your own functions](tutorial:writing-your-own-functions) we
met the domain of a function: the set of inputs it can accept. The
*range* of a function is the set of outputs it can give. This is a
different meaning from the range in
[Statistics: averages, spread and frequency](tutorial:making-sense-of-data),
where the range is the largest value minus the smallest.

Here are two functions with a limited domain. Each one has a line you
can uncomment to see what happens outside it.

```python exec
id: a-function-is-a-machine-3
import math

def reciprocal(x):
    return 1 / x


def square_root(x):
    return math.sqrt(x)


print(reciprocal(4))
print(square_root(9))

# Both of these are outside the domain of their function.
# Uncomment one at a time to see what that looks like.
# print(reciprocal(0))
# print(square_root(-1))
```

The domain answers the question "what am I allowed to put in?". It
matters. When we put in something outside the domain, Python gives an
error. The error tells us that the input is outside the domain.

## A machine has a picture

A function turns one number into another. Suppose we do that for many
numbers, keep each (input, output) pair, and plot the pairs. Then we
can see the function's shape.

```python exec
id: a-machine-has-a-picture-1
import matplotlib.pyplot as plt

def draw(f, low=-5, high=5, steps=200, label=None, ax=None):
    """Plot any single-argument function over a range.

    This one helper is used for the rest of this tutorial and several after it.
    """
    xs = [low + (high - low) * i / steps for i in range(steps + 1)]
    ys = [f(x) for x in xs]
    if ax is None:
        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
    ax.plot(xs, ys, label=label)
    if label:
        ax.legend()
    return ax


def square(x):
    return x ** 2


draw(square, label="x squared")
```

There is no magic inside `draw`. It does three things:

1. It makes a list of 201 $x$ values, spread evenly from `low` to `high`.
2. It calls your function on each one, to get the $y$ values.
3. It plots the $(x, y)$ pairs.

**The list of $(x, y)$ pairs and the curve are the same thing.** The
curve is a very long list of pairs, seen from far away.

This is worth saying, because a graph can feel like a separate object
that a function somehow owns. The *graph* of a function is its outputs,
drawn as points above its inputs.

### Your turn

Here is the function $f(x) = x^3 - 4x$.

1. Before you plot it, predict: how many times will the curve cross the
   horizontal axis?
2. Remove the `#` from the last line in the cell, and run it to check.

```python exec
id: your-turn-1
def cubic(x):
    return x ** 3 - 4 * x


# draw(cubic, label="x^3 - 4x")
```

## Straight lines

A straight line is the simplest interesting function. We write it as

$$y = mx + c$$

There are two numbers we can change, $m$ and $c$. The next two cells
change them one at a time. As you run them, what does $m$ do to the
line? What does $c$ do?

```python exec
id: straight-lines-1
def line(m, c):
    """Build a line function with slope m and intercept c."""
    def f(x):
        return m * x + c
    return f


ax = draw(line(1, 0), label="m=1, c=0")
draw(line(2, 0), label="m=2, c=0", ax=ax)
draw(line(0.5, 0), label="m=0.5, c=0", ax=ax)
draw(line(-1, 0), label="m=-1, c=0", ax=ax)
ax.set_title("Changing m, keeping c at 0")
```

```python exec
id: straight-lines-2
ax = draw(line(1, 0), label="m=1, c=0")
draw(line(1, 2), label="m=1, c=2", ax=ax)
draw(line(1, -3), label="m=1, c=-3", ax=ax)
ax.set_title("Changing c, keeping m at 1")
```

The two numbers have two separate effects:

| Number | Name | What it does to the line |
|---|---|---|
| $m$ | slope | tilts the line |
| $c$ | intercept | slides the line up or down |

Changing one does not change what the other does.

The *slope* $m$ tells us how steep the line is: for each step of 1 to the
right, the line goes up by $m$. The *intercept* $c$ is where the line
crosses the vertical axis. For example, $y = 2x + 1$ has slope 2 and
crosses the vertical axis at 1.

The letters are a habit, not a rule. Different countries use different
letters for these same two numbers. In the United States, for example,
the line is often written $y = mx + b$.

The function `line` does something new. It returns a function.
`line(2, 0)` returns a new function, and that new function multiplies
its input by 2. This pattern is useful whenever we
want a family of similar functions, and we use it again in the next
section.

### Your turn

Here are three lines:

- a: $y = 3x + 1$
- b: $y = -3x + 1$
- c: $y = 3x - 4$

1. Which of these lines are parallel? Write your prediction as a comment.
2. Plot all three on one pair of axes to check.

```python exec
id: your-turn-2
# a: y = 3x + 1
# b: y = -3x + 1
# c: y = 3x - 4

# Your prediction as a comment, then plot all three on one pair of axes.
```

Slope has a page of its own later, together with what it means for two
lines to be perpendicular:
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances).
Here, a line is one more function to draw.

## Curves that bend

A quadratic has an $x^2$ in it. That one change turns the straight line
into a curve with a turning point.

What does the number $a$ in $ax^2$ do? Run the cell and compare the four
curves.

```python exec
id: curves-that-bend-1
def quadratic(a, b, c):
    def f(x):
        return a * x ** 2 + b * x + c
    return f


ax = draw(quadratic(1, 0, 0), label="x^2")
draw(quadratic(2, 0, 0), label="2x^2", ax=ax)
draw(quadratic(0.3, 0, 0), label="0.3x^2", ax=ax)
draw(quadratic(-1, 0, 0), label="-x^2", ax=ax)
ax.set_ylim(-10, 10)
ax.set_title("What the a in ax^2 does")
```

A bigger $a$ makes the curve narrower. A negative $a$ turns it upside
down. So far, this is the same pattern we saw with the line: one number,
one visible change.

Does $b$ behave the same way? Before you run the next cell, guess. Will
changing $b$ slide the curve left and right, move it up and down, or do
something else? The cell draws $x^2 + bx$ nine times, once for every
whole number $b$ from $-4$ to $4$.

```python exec
id: curves-that-bend-3
ax = None
for b in range(-4, 5):
    ax = draw(quadratic(1, b, 0), ax=ax)
ax.set_ylim(-6, 10)
ax.set_title("x^2 + bx, for b from -4 to 4")

# Remove the # from the next line when you have a guess.
# draw(quadratic(-1, 0, 0), ax=ax, label="-x^2")
```

Look at where each curve turns. The turning points are not scattered.
They seem to sit on a curve of their own, an upside-down one. Which
curve could it be? When you have a guess, remove the `#` from the last
line of the cell and run it again.

Every turning point lies on $y = -x^2$. That is a strange result, isn't
it? Changing $b$ does not do one separate thing. It slides the curve
sideways and down at the same time, and the turning point travels along
a parabola of its own. The next page,
[Parabolas: completing the square](tutorial:parabolas), shows where that
path comes from.

A cubic has an $x^3$ in it, and it can bend twice. Look at the two
cubics below. Which one turns, and which one does not?

```python exec
id: curves-that-bend-2
def cubic(a, b, c, d):
    def f(x):
        return a * x ** 3 + b * x ** 2 + c * x + d
    return f


ax = draw(cubic(1, 0, 0, 0), low=-3, high=3, label="x^3")
draw(cubic(1, 0, -4, 0), low=-3, high=3, label="x^3 - 4x", ax=ax)
ax.set_title("Cubics")
```

The curve $x^3 - 4x$ turns twice. The curve $x^3$ is flat for a moment
at 0, but it keeps going up, so it never turns.

There is a general pattern here. **The number of turns is at most one
less than the highest power.**

| Function | Highest power | Turns at most |
|---|---|---|
| line | $x^1$ | 0 |
| quadratic | $x^2$ | 1 |
| cubic | $x^3$ | 2 |

This is a useful rule for sketching a curve before you plot it.

If you still have your polynomial evaluator from
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive),
try drawing with it. It does the same job as the functions above. We
wrote it before we had any way to draw its output.

## Reading an answer off the picture

Here is the habit that much of the rest of the course depends on.

**Where a curve crosses the horizontal axis, the function is zero.** So
two questions are the same question:

- What values of $x$ solve $f(x) = 0$?
- Where does the curve cross the horizontal axis?

Where does this curve cross? Run the cell and read the answer from the
picture.

```python exec
id: reading-an-answer-off-the-picture-1
f = quadratic(1, -5, 6)
ax = draw(f, low=-1, high=6, label="x^2 - 5x + 6")
ax.set_ylim(-2, 8)
ax.set_title("Where does it cross?")
```

The curve crosses at 2 and at 3. The solver from
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
gives the same two numbers.

The two methods give the same answer. It is worth doing this once
for a question where we already know the answer. Then we can trust the
picture for questions where we do not.

The picture can also answer questions that are harder to answer with a
formula. Where do these two curves meet?

```python exec
id: reading-an-answer-off-the-picture-2
ax = draw(quadratic(1, -5, 6), low=-1, high=6, label="x^2 - 5x + 6")
draw(line(1, -1), low=-1, high=6, label="x - 1", ax=ax)
ax.set_ylim(-3, 8)
ax.set_title("Where are these two equal?")
```

Two curves cross where the two functions are equal. The two crossing
points solve

$$x^2 - 5x + 6 = x - 1$$

without any algebra. From the picture, the crossings are near
$x = 1.6$ and $x = 4.4$. The exact answers are $3 - \sqrt{2}$ and
$3 + \sqrt{2}$, about 1.59 and 4.41.

This method works equally well for equations that have no neat
algebraic method.

### Your turn

Where is $x^3 - 4x = 1$? We can find the answer, roughly, from a
picture.

1. Plot $x^3 - 4x$ and the flat line $y = 1$ on one pair of axes.
2. Find the $x$ values where they cross on the plot.

```python exec
id: your-turn-3
# Plot x^3 - 4x and the horizontal line y = 1 on one pair of axes,
# then read off the crossings.
```

## Undoing a function

This is the last idea on the page. It needs the least mathematics, but
the most care.

In [Writing your own functions](tutorial:writing-your-own-functions) we
met the inverse of a function. An inverse function undoes what a
function did. If $f$ turns 3 into 6, its inverse turns 6 back into 3.

What do you expect at the end of each line below?

```python exec
id: undoing-a-function-1
def double(x):
    return x * 2


def halve(x):
    return x / 2


for value in [1, 5, -3, 0]:
    print(f"{value} -> double -> {double(value)} -> halve -> {halve(double(value))}")
```

Every value ends where it started. This round trip is what "inverse"
means. It is also a test we can run for ourselves.

The picture of an inverse is a mirror image. The inverse swaps inputs
and outputs, so it swaps the two axes. The graph flips across the
diagonal line $y = x$.

The next cell uses `lambda x: x ** 2`. A `lambda` is a short way to
write a small function without giving it a name. Here it means the same
as our `square` function.

```python exec
id: undoing-a-function-2
import math

ax = draw(lambda x: x ** 2, low=0, high=4, label="x squared")
draw(math.sqrt, low=0, high=4, label="square root", ax=ax)
draw(lambda x: x, low=0, high=4, label="y = x", ax=ax)
ax.set_ylim(0, 4)
ax.set_aspect("equal")
ax.set_title("A function and its inverse, mirrored in y = x")
```

### When you cannot undo it

Not every function has an inverse. The reason is the "exactly one
output" rule again.

```python exec
id: undoing-a-function-3
def square(x):
    return x ** 2


print("square(3) =", square(3))
print("square(-3) =", square(-3))
```

Both 3 and $-3$ give 9. So what should the inverse give for 9? There is
no single right answer, and a function must give exactly one.

This is why `math.sqrt(9)` gives 3, and not $-3$. Mathematicians agreed
to keep only the positive answer, so that the square root can be a
function. For the same reason, the plot above starts at 0.

**A function can be undone only if it never sends two different inputs
to the same output.** Doubling can be undone. Squaring cannot, unless we
limit the inputs, for example to numbers that are 0 or more.

### Your turn

Does $f(x) = x^3$ have an inverse over all the numbers?

1. Think about it first: can two different inputs give the same output?
   Write your reasoning as a comment.
2. Check with a plot.

```python exec
id: your-turn-4
# Your reasoning as a comment, then the plot.
```

## Reflection

A function is a rule with exactly one output for each input, and that
rule has a shape.

Here are four ideas to take with you.

**A graph is the function's output, drawn.** It is a long list of
$(x, y)$ pairs seen from far away. Anything we can compute, we can also
draw.

**Some numbers make one visible change, and some do not.** The two
numbers in a line each do one job. In a quadratic, $a$ changes the width.
But $b$ moves the turning point sideways and down at once, along the
curve $y = -x^2$. Only the picture showed us that.

**The points where a curve crosses the axis solve the equation.** Once
we trust that, a
picture becomes a way to answer questions, including questions with no
neat algebraic method.

**An inverse is a round trip, and not every function has one.** A
function can be undone only if no two inputs give the same output.

For $x^2 - 5x + 6 = 0$, which did you find easier: the formula or the
picture? What would change your answer? Write a few sentences.

## Where to read more

Khan Academy. *Domain and Range of a Function.*
<https://www.youtube.com/watch?v=O0uUVH8dRiU>. This video explains the
two ideas this page shows with `reciprocal` and `square_root`. It uses a
graph instead of an error message.

SimonDev (2022). *An In-Depth look at Lerp, Smoothstep, and Shaping
Functions.* <https://www.youtube.com/watch?v=YJB1QnEmlTs>. Game developers
use small functions to shape movement: a straight line from one value to
another, or a curve that starts slowly and ends slowly. SimonDev draws
each one as a graph. It is about eight minutes long.
