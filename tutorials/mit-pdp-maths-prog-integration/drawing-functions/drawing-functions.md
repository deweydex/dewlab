---
title: "Drawing Functions"
slug: drawing-functions
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
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

# Drawing Functions

**Maths for IT**

You have written functions since *Building Reusable Tools*, and you have plotted data since *Pictures Worth Numbers*. Nobody has yet asked you to plot a *function* — and that is the habit almost everything after this depends on.

Trigonometry is a graph. A limit is a graph. A derivative is the slope of a graph. Once you can put a function on a pair of axes and read an answer off it, all three of those stop being abstract.

There is also something slightly odd about the series so far that this fixes. *Pictures Worth Numbers* taught you to plot data and never came back to it, and *Expressions Come Alive* built a polynomial evaluator that never got drawn. Those two have been waiting for each other.

## A Function Is a Machine

The word "function" has been doing two jobs and nobody has separated them.

In Python, a function is a piece of code with a name. In mathematics, a function is a rule that takes an input and gives back exactly one output. **They are the same idea**, and the mathematical definition is the stricter of the two.

"Exactly one output" is the part that matters. Given the same input, a function must give the same answer every time — otherwise it is not a function, it is just a thing that happens.

```python exec
id: a-function-is-a-machine-1
def double(x):
    return x * 2


def square(x):
    return x ** 2


for value in [-2, 0, 3, 3, 3]:
    print(f"double({value}) = {double(value):>4}    square({value}) = {square(value)}")
```

Notice the three 3s at the end. Same input, same output, three times. That sounds too obvious to mention until you meet something that does not do it:

```python exec
id: a-function-is-a-machine-2
import random

def roll(x):
    return random.randint(1, 6)


for _ in range(4):
    print("roll(1) =", roll(1))
```

`roll` is a perfectly good piece of Python and it is not a function in the mathematical sense. Feed it 1 four times and you get four different answers. **It has no graph** — you could not draw it, because there is no single height above `x = 1`.

The mathematical word for the set of inputs a function will accept is its **domain**, and for the set of outputs it can produce, its **range**.

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

A domain is not a technicality. It is the answer to "what am I allowed to put in?", and the error you get from putting in something else is the function telling you so.

## A Machine Has a Picture

Now the connection this tutorial exists for.

A function turns one number into another. Do that for a lot of numbers, keep the pairs, and plot them — and the machine has a shape.

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

Look at what `draw` does, because there is no magic in it. It makes a list of x values, calls your function on each one, and plots the pairs. **The list of (x, y) pairs and the curve are the same thing** — the curve is just what a very long list of pairs looks like from a distance.

That is worth saying because a graph can feel like a separate object that a function somehow has. It is not. It is the function's output, written down in a different medium.

### Your turn

What happens when you plot `f(x) = x**3 - 4*x`? Before you run it, how many times do you think it will cross the horizontal axis?

```python exec
id: your-turn-1
def cubic(x):
    return x ** 3 - 4 * x


# draw(cubic, label="x^3 - 4x")
```

## Straight Lines

The simplest interesting function is a straight line, and it has exactly two things you can change about it.

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

Two numbers, two completely separate effects. **`m` tilts the line and `c` slides it up and down**, and neither one interferes with the other.

`line` is doing something you have not seen before: it is a function that returns a function. `line(2, 0)` hands you back a new function that multiplies by 2. That pattern is useful whenever you want a family of similar functions, and you will use it repeatedly from here on.

The names are conventional rather than meaningful — `m` for the slope, `c` for where it crosses the vertical axis. Different countries use different letters for the same two things.

### Your turn

Which of these three lines are parallel? Make a prediction, then plot them to check.

```python exec
id: your-turn-2
# a: y = 3x + 1
# b: y = -3x + 1
# c: y = 3x - 4

# Your prediction as a comment, then plot all three on one pair of axes.
```

Slope, and what it means to say two lines are perpendicular, gets a tutorial of its own — [Lines and Distances](tutorial:lines-and-distances), which comes after this one. Here a line is just one more function to draw.

## Curves That Bend

A quadratic has an `x²` in it. That single change turns the straight line into a curve with a turning point.

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

A bigger `a` makes it narrower; a negative `a` turns it upside down. Same "one coefficient, one visible change" pattern as the line.

And a cubic bends twice.

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

There is a pattern here that holds generally: **the highest power tells you how many times the curve can turn.** A line (`x¹`) does not turn. A quadratic (`x²`) turns once. A cubic (`x³`) turns at most twice. It is a good rule of thumb for sketching something before you plot it.

Use your polynomial evaluator from *Expressions Come Alive* if you still have it — it does exactly what the functions above do, and it was written before you had anywhere to draw its output.

## Reading an Answer Off the Picture

Here is the habit everything after this depends on.

**Where a curve crosses the horizontal axis, the function is zero.** So solving `f(x) = 0` and finding where the curve crosses are the same question.

```python exec
id: reading-an-answer-off-the-picture-1
f = quadratic(1, -5, 6)
ax = draw(f, low=-1, high=6, label="x^2 - 5x + 6")
ax.set_ylim(-2, 8)
ax.set_title("Where does it cross?")
```

It crosses at 2 and at 3. Check that against the solver from *Cracking Equations* and you will get the same two numbers.

Two different methods, one answer. That is worth doing at least once for something you already know, because it is what tells you the picture can be trusted for something you do not.

The picture also answers questions the formula does not obviously answer:

```python exec
id: reading-an-answer-off-the-picture-2
ax = draw(quadratic(1, -5, 6), low=-1, high=6, label="x^2 - 5x + 6")
draw(line(1, -1), low=-1, high=6, label="x - 1", ax=ax)
ax.set_ylim(-3, 8)
ax.set_title("Where are these two equal?")
```

Two curves cross where the two functions are equal. Reading those two points off the graph solves `x² − 5x + 6 = x − 1` without doing any algebra at all — and it works just as well for equations that have no tidy algebraic method.

### Your turn

How might you find, from a picture, roughly where `x³ − 4x = 1`?

```python exec
id: your-turn-3
# Plot x^3 - 4x and the horizontal line y = 1 on one pair of axes,
# then read off the crossings.
```

## Undoing a Function

The last idea, and the one that needs the most care with the least mathematics.

An **inverse function** undoes what a function did. If `f` turns 3 into 6, its inverse turns 6 back into 3.

```python exec
id: undoing-a-function-1
def double(x):
    return x * 2


def halve(x):
    return x / 2


for value in [1, 5, -3, 0]:
    print(f"{value} -> double -> {double(value)} -> halve -> {halve(double(value))}")
```

Every one comes back to where it started. That round trip is what "inverse" means, and it is a test you can run rather than a definition to accept.

The picture of an inverse is a reflection. Swapping the inputs and outputs swaps the axes, so the graph flips across the diagonal line `y = x`.

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

Not every function has an inverse, and the reason is the "exactly one output" rule biting from the other end.

```python exec
id: undoing-a-function-3
def square(x):
    return x ** 2


print("square(3) =", square(3))
print("square(-3) =", square(-3))
```

Both 3 and −3 give 9. So what should the inverse of 9 be? There is no single right answer, and a function must give exactly one.

This is why `math.sqrt(9)` returns 3 and not −3: somebody made a decision to keep only the positive half, so that the square root could be a function at all. The plot above only goes from 0 upwards for the same reason.

**A function can only be undone if it never sends two different inputs to the same output.** Doubling can. Squaring cannot, unless you restrict what you will feed it.

### Your turn

Does `f(x) = x³` have an inverse over all the numbers? Answer by thinking about whether two different inputs can give the same output — then check with a plot.

```python exec
id: your-turn-4
# Your reasoning as a comment, then the plot.
```

## Reflection

A function is a rule with exactly one output per input, and that rule has a shape.

What to take from this.

**A graph is output, not decoration.** It is a long list of (x, y) pairs seen from a distance, and everything you can compute you can also draw.

**One coefficient, one visible change.** Lines have two numbers, quadratics have three, and each of them does a separate thing to the picture. That pattern comes back in every family of curves in the rest of the course.

**Crossing the axis is solving the equation.** Once you believe that, a picture becomes a way of answering questions, including questions with no tidy algebraic route.

**An inverse is a round trip, and not everything has one.** Whether a function can be undone is a question about whether two inputs ever collide.

In a few sentences, which did you find easier for `x² − 5x + 6 = 0` — the formula or the picture? What would change your answer?

## Where to Read More

Khan Academy. *Domain and Range of a Function.*
<https://www.youtube.com/watch?v=O0uUVH8dRiU>. The same two ideas this
page introduces through `reciprocal` and `square_root`, from a graph
instead of an error message.
