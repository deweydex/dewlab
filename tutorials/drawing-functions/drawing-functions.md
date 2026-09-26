---
title: "Functions and their graphs"
year: "2026-2027"
version: 2026.09.26.1
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
worlds:
  rockets: Rockets, launches and the arcs they fly. The numbers are made up.
  electronics: Batteries, resistors and the power between them. The numbers are made up.
  music: Notes, octaves and the frequencies that make them.
  fantasy-maps: A made-up kingdom, with its roads drawn on a grid.
---

# Functions and their graphs

In [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
we wrote `evaluate_poly`, which finds a polynomial's value at any $x$.
We never drew what it gives. The cell below does that for the rocket
from that page, whose height after $t$ seconds is $2 + 15t - 4.9t^2$
metres.

```python exec
id: opening-1
import matplotlib.pyplot as plt


def evaluate_poly(coeffs, x):
    total = 0
    for i, c in enumerate(coeffs):
        total = total + c * x ** i
    return total


rocket = [2, 15, -4.9]
times = [i / 10 for i in range(33)]      # 0, 0.1, 0.2, ... 3.2 seconds
heights = [evaluate_poly(rocket, t) for t in times]

fig, ax = plt.subplots()
ax.plot(times, heights)
ax.set_xlabel("time (s)")
ax.set_ylabel("height (m)")
ax.grid(alpha=0.3)
```

```predict
type: choice

Before you run it: what shape will the line make?

- A straight line going up
  - The rocket is launched upwards, and a straight line is the
    simplest picture of that.
- A hill: up, then down
- A curve that keeps getting steeper
  - A rocket speeds up as it goes.
```

The heights make a hill. The rocket climbs, slows, stops near 1.5
seconds and falls. Four numbers on the last page (2, 12.1, 12.4 and
2.9) gave only a rough idea of that shape. The picture shows all of it
at once.

On this page we draw functions, and we learn to read answers from the
picture. Much of the rest of the course uses this habit. Trigonometry,
limits and derivatives all use graphs, and they are much less abstract
once you can draw a function and read an answer from it.

## A function is a machine

The word "function" has two meanings in this course, one in Python and
one in mathematics. How are they related?

In Python, a function is a piece of code with a name. In mathematics, a
function is a rule that takes an input and gives exactly one output.
These are the same idea, and the mathematical meaning is the stricter
of the two.

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

The domain answers the question "what am I allowed to put in?". When we
put in something outside the domain, Python stops with an error, and
the error tells us that the input is outside the domain.

## A machine has a picture

A function turns one number into another. Suppose we do that for many
numbers, keep each (input, output) pair, and plot the pairs. Then we
can see the function's shape. The opening cell did this for one
polynomial. Here is a helper that does it for any function of one
number.

```python exec
id: a-machine-has-a-picture-1
def draw(f, low=-5, high=5, steps=200, label=None, ax=None):
    """Plot any function of one number, from low to high."""
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


draw(square, label="x squared")
```

There is no magic inside `draw`. It does three things:

1. It makes a list of 201 $x$ values, spread evenly from `low` to `high`.
2. It calls your function on each one, to get the $y$ values.
3. It plots the $(x, y)$ pairs.

**The list of $(x, y)$ pairs and the curve are the same thing.** The
curve is a very long list of pairs, seen from far away. The *graph* of
a function is its outputs, drawn as points above its inputs.

To draw two curves on one pair of axes, keep the axes that the first
call returns, and pass them to the second: `ax = draw(f)`, then
`draw(g, ax=ax)`.

### Your turn

Here is the function $f(x) = x^3 - 4x$. Before you plot it, how many
times do you think the curve crosses the horizontal axis? Then remove
the `#` from the last line, and run the cell to check.

```python exec
id: your-turn-1
def cubic(x):
    return x ** 3 - 4 * x


# draw(cubic, label="x^3 - 4x")
```

## Straight lines

A straight line is the simplest interesting function. We write it as

$$y = mx + c$$

There are two numbers we can change, $m$ and $c$. A straight line needs
only two points, so a function that draws one does not need 201 of
them.

### Your turn

Can you write `plot_line(m, c, ax)`? It draws $y = mx + c$ on the axes
`ax`, from $x = -5$ to $x = 5$, with a label such as `"y = 2x + 1"`, and
then calls `ax.legend()` so the labels show. The cell makes the axes and
calls your function three times.

```python exec
id: your-turn-2
def plot_line(m, c, ax):
    """Draw y = mx + c on the axes ax, from x = -5 to x = 5."""
    # Your code here.


fig, ax = plt.subplots()
ax.grid(alpha=0.3)
plot_line(1, 0, ax)
plot_line(2, 0, ax)
plot_line(1, 3, ax)
```

```hint
Which two $x$ values are the ends of the line? What is $y$ at each of
them? `ax.plot` takes a list of the $x$ values and a list of the $y$
values.
```

```solution
def plot_line(m, c, ax):
    """Draw y = mx + c on the axes ax, from x = -5 to x = 5."""
    xs = [-5, 5]
    ys = [m * x + c for x in xs]
    ax.plot(xs, ys, label=f"y = {m}x + {c}")
    ax.legend()


fig, ax = plt.subplots()
ax.grid(alpha=0.3)
plot_line(1, 0, ax)
plot_line(2, 0, ax)
plot_line(1, 3, ax)
---
Two points are enough. `ax.plot` joins them with a straight line.
```

Now use your `plot_line` to see what each number does. The first
cell changes $m$ and keeps $c$ at 0. The second changes $c$ and keeps
$m$ at 1. What does $m$ do to the line? What does $c$ do?

```python exec
id: straight-lines-1
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
for m in [1, 2, 0.5, -1]:
    plot_line(m, 0, ax)
ax.set_title("Changing m, keeping c at 0")
```

```python exec
id: straight-lines-2
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
for c in [0, 2, -3]:
    plot_line(1, c, ax)
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

### Lines in your world

<div class="dl-world" data-world="rockets">

A rocket's upward speed after $t$ seconds is its launch speed minus
$9.8t$ m/s on Earth, and minus $3.7t$ on Mars, where gravity is weaker.
Here are three rockets:

- a: launched at 10 m/s on Earth, $v = -9.8t + 10$
- b: launched at 20 m/s on Earth, $v = -9.8t + 20$
- c: launched at 20 m/s on Mars, $v = -3.7t + 20$

Which of these lines are parallel? Write your guess as a comment, then
plot all three with `plot_line`.

```python exec
id: lines-in-your-world-1--rockets
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
```

```solution
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
plot_line(-9.8, 10, ax)
plot_line(-9.8, 20, ax)
plot_line(-3.7, 20, ax)
---
a and b are parallel, because both have slope $-9.8$: the same gravity
slows both rockets at the same rate. c starts where b does, at 20 m/s,
but its line is less steep, because Mars slows it more gently.
`plot_line` draws from $-5$ to 5, and the left half, before the
launch, has no meaning for a rocket.
```

</div>

<div class="dl-world" data-world="electronics">

For a resistor, the voltage across it is the current times the
resistance: $V = IR$. This is *Ohm's law*. Plotted with the current
along the bottom, each resistor is a line through the origin. Here are
three:

- a 2 ohm resistor, $V = 2I$
- a 4 ohm resistor, $V = 4I$
- a 0.5 ohm resistor, $V = 0.5I$

Which line will be steepest? What does the slope of each line tell you?
Write your guess as a comment, then plot all three with `plot_line`.

```python exec
id: lines-in-your-world-1--electronics
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
```

```solution
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
plot_line(2, 0, ax)
plot_line(4, 0, ax)
plot_line(0.5, 0, ax)
---
The 4 ohm line is steepest. The slope is the resistance. For every extra
amp, the voltage goes up by that many volts. The intercept is 0 for all
three, because no current flows when there is no voltage.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The kingdom's map has a grid, with each square 1 km wide. Three roads
are straight lines on it:

- the King's Road, $y = 0.5x + 2$
- the Mill Road, $y = 0.5x - 1$
- the Tower Road, $y = -2x + 8$

Which roads are parallel, so that they never meet? Write your guess as
a comment, then plot all three with `plot_line`.

```python exec
id: lines-in-your-world-1--fantasy-maps
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
ax.set_aspect("equal")
```

```solution
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
ax.set_aspect("equal")
plot_line(0.5, 2, ax)
plot_line(0.5, -1, ax)
plot_line(-2, 8, ax)
---
The King's Road and the Mill Road are parallel. Both have slope 0.5,
and they stay 3 km apart up the vertical axis. The Tower Road crosses
both at a right angle. $0.5 \times (-2) = -1$, and
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances)
shows why that makes two lines perpendicular.
```

</div>

## Curves that bend

A quadratic has an $x^2$ in it. That one change turns the straight line
into a curve with a turning point. Let's move the simplest one, $y = x^2$,
one change at a time.

```python exec
id: curves-that-bend-1
ax = draw(lambda x: x ** 2, label="x^2")
ax.set_ylim(-2, 15)
draw(lambda x: x ** 2 + 3, label="x^2 + 3", ax=ax)
```

```predict
type: choice

Where will the curve for $x^2 + 3$ be, compared with $x^2$?

- 3 higher
- 3 lower
  - Adding 3 to the formula could be undone by moving down.
- 3 to the right
  - A bigger number sounds like further along.
```

Adding 3 to the output lifts every point by 3, so the whole curve moves
3 up. Now the same change, but inside the square.

```python exec
id: curves-that-bend-2
ax = draw(lambda x: x ** 2, label="x^2")
ax.set_ylim(-2, 15)
draw(lambda x: (x - 2) ** 2, label="(x - 2)^2", ax=ax)
```

```predict
type: choice

Where will the curve for $(x - 2)^2$ be, compared with $x^2$?

- 2 to the right
- 2 to the left
  - A minus sign usually means moving to the left, or down.
- 2 lower
  - A minus 2 sounds like the curve should drop.
```

$(x - 2)^2$ is 2 to the right. Its lowest point is where the bracket is
zero, and that is at $x = 2$. At $x = 5$ it gives what $x^2$ gave at
$x = 3$, so every value arrives 2 later. So a change inside the bracket moves
the curve the opposite way to its sign. Moving a whole curve without
changing its shape is called a *translation*.

What does the number $a$ in $ax^2$ do? The next cell builds each curve
with a function `quadratic(a, b, c)`, which returns the function
$ax^2 + bx + c$. It is a function that returns a function, so that one
line can make a whole family of curves.

```python exec
id: curves-that-bend-3
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
down. So far, each number does one visible thing: $c$ moves the curve up
and down, and $a$ stretches it.

Does $b$ behave the same way? Before you run the next cell, guess. Will
changing $b$ slide the curve left and right, move it up and down, or do
something else? The cell draws $x^2 + bx$ nine times, once for every
whole number $b$ from $-4$ to $4$.

```python exec
id: curves-that-bend-4
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
a parabola of its own.
[Parabolas: completing the square](tutorial:parabolas) shows where that
path comes from.

A cubic has an $x^3$ in it, and it can bend twice. Look at the two
cubics below. Which one turns, and which one does not?

```python exec
id: curves-that-bend-5
ax = draw(lambda x: x ** 3, low=-3, high=3, label="x^3")
draw(lambda x: x ** 3 - 4 * x, low=-3, high=3, label="x^3 - 4x", ax=ax)
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

The curve crosses at 2 and at 3. We can check both by putting them back
in: $2^2 - 5 \times 2 + 6 = 0$ and $3^2 - 5 \times 3 + 6 = 0$. In
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
a formula finds the same two numbers.

The picture can also answer questions that are harder to answer with a
formula. Where do these two curves meet?

```python exec
id: reading-an-answer-off-the-picture-2
ax = draw(quadratic(1, -5, 6), low=-1, high=6, label="x^2 - 5x + 6")
draw(lambda x: x - 1, low=-1, high=6, label="x - 1", ax=ax)
ax.set_ylim(-3, 8)
ax.set_title("Where are these two equal?")
```

Two curves cross where the two functions are equal. The two crossing
points solve

$$x^2 - 5x + 6 = x - 1$$

without any algebra. From the picture, the crossings are near
$x = 1.6$ and $x = 4.4$. The exact answers are $3 - \sqrt{2}$ and
$3 + \sqrt{2}$, about 1.59 and 4.41.

This method works just as well for equations that have no neat
algebraic method.

### Your turn

<div class="dl-world" data-world="rockets">

When is the rocket from the opening cell 10 m up? It passes that height
twice, once going up and once coming down. Can you plot the rocket's
height and the flat line at 10 m on one pair of axes, and read the two
times from the picture?

```python exec
id: your-turn-3--rockets
def height(t):
    return 2 + 15 * t - 4.9 * t ** 2
```

```hint
The height is a function of $t$, so `draw(height, low=0, high=3.2)`
draws it. What function of $t$ gives 10 every time?
```

```solution
ax = draw(height, low=0, high=3.2, label="height")
draw(lambda t: 10, low=0, high=3.2, label="10 m", ax=ax)
---
The curves cross near $t = 0.7$ and $t = 2.4$. Put in more exactly,
the times are about 0.69 s and 2.37 s. The rocket is above 10 m for
about 1.7 seconds.
```

</div>

<div class="dl-world" data-world="electronics">

The 12 volt supply from the last page delivers $12I - 2I^2$ watts when
a current of $I$ amps flows. At which currents does it deliver exactly
10 watts? Can you plot the power and the flat line at 10 W on one pair
of axes, and read the currents from the picture?

```python exec
id: your-turn-3--electronics
def power(current):
    return 12 * current - 2 * current ** 2
```

```hint
Draw the power from 0 to 6 amps. What function gives 10 every time?
```

```solution
ax = draw(power, low=0, high=6, label="power")
draw(lambda current: 10, low=0, high=6, label="10 W", ax=ax)
---
The curves cross at 1 A and at 5 A. Check both: $12 - 2 = 10$ and
$60 - 50 = 10$. At 1 A the supply delivers 10 W and wastes 2 W as heat
inside it. At 5 A it also delivers 10 W, but wastes 50 W.
```

</div>

<div class="dl-world" data-world="music">

A note $n$ semitones above the orchestra's A has the frequency
$440 \times 2^{n/12}$ Hz. A whistle sounds at 1000 Hz. How many
semitones above the A is it? Can you plot the frequency for $n$ from
0 to 24, and the flat line at 1000 Hz, and read $n$ from the picture?

```python exec
id: your-turn-3--music
def frequency(n):
    return 440 * 2 ** (n / 12)
```

```hint
`draw(frequency, low=0, high=24)` draws the curve. What function of
$n$ gives 1000 every time?
```

```solution
ax = draw(frequency, low=0, high=24, label="frequency")
draw(lambda n: 1000, low=0, high=24, label="1000 Hz", ax=ax)
---
The curves cross a little past $n = 14$. The exact answer is about
14.2 semitones, which is $12 \log_2 \frac{1000}{440}$ from
[Number types, powers and logarithms](tutorial:numbers-and-their-families).
The curve bends upwards, because each semitone multiplies the
frequency, so it adds more hertz than the semitone before.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The King's Road is $y = 0.5x + 2$ and the River Road is $y = -x + 5$.
A tollhouse stands where they cross. Can you plot both roads on one
pair of axes, and read where the tollhouse is?

```python exec
id: your-turn-3--fantasy-maps
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
ax.set_aspect("equal")
```

```hint
Your `plot_line` draws each road. Which two numbers does each road
give it?
```

```solution
fig, ax = plt.subplots()
ax.grid(alpha=0.3)
ax.set_aspect("equal")
plot_line(0.5, 2, ax)
plot_line(-1, 5, ax)
---
The roads cross at $(2, 3)$. Check it in both: $0.5 \times 2 + 2 = 3$
and $-2 + 5 = 3$. The tollhouse is 2 km east and 3 km north of the
middle of the map.
```

</div>

## Undoing a function

This is the last idea on the page. It needs the least mathematics, but
the most care.

In [Writing your own functions](tutorial:writing-your-own-functions) we
met the inverse of a function. An inverse function undoes what a
function did. If $f$ turns 3 into 6, its inverse turns 6 back into 3.

What do you expect at the end of each line below?

```python exec
id: undoing-a-function-1
def halve(x):
    return x / 2


for value in [1, 5, -3, 0]:
    print(f"{value} -> double -> {double(value)} -> halve -> {halve(double(value))}")
```

Every value ends where it started. This round trip is also a test we can
run for ourselves.

The picture of an inverse is a mirror image. The inverse swaps inputs
and outputs, so it swaps the two axes. The graph flips across the
diagonal line $y = x$.

In [Number types, powers and logarithms](tutorial:numbers-and-their-families)
a logarithm was a power read backwards. So $\log_2 x$ is the inverse of
$2^x$: $2^3 = 8$ and $\log_2 8 = 3$. Here are the two, with the line
$y = x$ between them.

```python exec
id: undoing-a-function-2
ax = draw(lambda x: 2 ** x, low=-3, high=3, label="2^x")
draw(math.log2, low=0.125, high=8, label="log2 x", ax=ax)
draw(lambda x: x, low=-3, high=8, label="y = x", ax=ax)
ax.set_xlim(-3, 8)
ax.set_ylim(-3, 8)
ax.set_aspect("equal")
ax.set_title("A power and its inverse, mirrored in y = x")
```

The point $(3, 8)$ is on the curve $2^x$, and $(8, 3)$ is on the curve
$\log_2 x$. Every point on one has its mirror image on the other. The
logarithm is only drawn for $x$ above 0, because $2^x$ is never 0 or
negative, so the logarithm has nothing to undo there.

### When you cannot undo it

Not every function has an inverse. The reason is the "exactly one
output" rule again.

```python exec
id: undoing-a-function-3
print("square(3) =", square(3))
print("square(-3) =", square(-3))
```

Both 3 and $-3$ give 9. So what should the inverse give for 9? There is
no single answer, and a function must give exactly one.

This is why `math.sqrt(9)` gives 3, and not $-3$. Mathematicians agreed
to keep only the positive answer, so that the square root can be a
function.

**A function can be undone only if it never sends two different inputs
to the same output.** Doubling can be undone. Squaring cannot, unless we
limit the inputs, for example to numbers that are 0 or more.

### Undoing in your world

<div class="dl-world" data-world="rockets">

Can the rocket's height be undone? Given a height, is there one time
when the rocket was there? Can you find two different times with the
same height, using `height` from your turn above?

```python exec
id: undoing-in-your-world-1--rockets
def height(t):
    return 2 + 15 * t - 4.9 * t ** 2
```

```hint
The rocket is highest at $t = 15 / 9.8$ seconds. What is its height
half a second before that, and half a second after?
```

```solution
top = 15 / 9.8          # the time of the highest point
print(height(top - 0.5), height(top + 0.5))
---
Both print about 12.25. The rocket passes 12.25 m going up, at about
1.03 s, and again coming down, at about 2.03 s. Any height below the
top is reached twice, so "when was it this high?" has two answers, and
the height has no inverse. Every quadratic is like this, for the same
reason as squaring.
```

</div>

<div class="dl-world" data-world="electronics">

A resistor of 2 ohms turns $2I^2$ watts into heat when a current of
$I$ amps flows. Current can flow either way through a resistor, so $I$
can be negative. If a resistor is making 18 W of heat, can you tell
what the current is? Try `heat(3)` and `heat(-3)`.

```python exec
id: undoing-in-your-world-1--electronics
def heat(current):
    return 2 * current ** 2
```

```solution
print(heat(3), heat(-3))
---
Both give 18. 3 amps one way and 3 amps the other way make the same
heat, so the heat cannot tell you which way the current flows. Like
squaring, this function has no inverse unless we only allow currents
of 0 or more.
```

</div>

<div class="dl-world" data-world="music">

`frequency(n)` turns semitones into hertz. Can you write
`semitones(hz)`, its inverse, and check it with a round trip?

```python exec
id: undoing-in-your-world-1--music
def frequency(n):
    return 440 * 2 ** (n / 12)
```

```hint
$\text{hz} = 440 \times 2^{n/12}$. Which two steps undo this, and in
which order?
```

```solution
def semitones(hz):
    return 12 * math.log2(hz / 440)


for n in [-12, 0, 7, 12]:
    print(n, frequency(n), semitones(frequency(n)))
---
Divide by 440, take $\log_2$, and multiply by 12: the steps of
`frequency`, undone in reverse order. The round trip brings every $n$
back, apart from rounding. This inverse exists because a higher note
always has a higher frequency, so no two notes share one.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The map is drawn at 1 : 50,000, so `to_ground(cm)` turns a map
distance in centimetres into a real distance in kilometres. Can you
write `to_map(km)`, its inverse, and check it with a round trip?

```python exec
id: undoing-in-your-world-1--fantasy-maps
def to_ground(cm):
    return cm * 50_000 / 100_000
```

```solution
def to_map(km):
    return km * 100_000 / 50_000


for cm in [1, 7.2, 20]:
    print(cm, to_ground(cm), to_map(to_ground(cm)))
---
1 cm on the map is 0.5 km on the ground, so `to_map` doubles a
distance in km to give centimetres. The round trip brings every map
distance back.
```

</div>

## Looking back

For $x^2 - 5x + 6 = 0$ you can check a root by putting it back in, or
read it from the picture. The picture showed both roots at once. When
would you trust the picture less than the arithmetic?

A challenge: can you draw $2^x$, $x^2$ and $x$ on one pair of axes,
from 0 to 5? Where does $2^x$ overtake $x^2$, and does it stay ahead?
Try a wider range before you decide.

```python challenge
import matplotlib.pyplot as plt

xs = [i / 10 for i in range(51)]
fig, ax = plt.subplots()
ax.plot(xs, [2 ** x for x in xs], label="2^x")
ax.plot(xs, [x ** 2 for x in xs], label="x^2")
ax.legend()
```

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
