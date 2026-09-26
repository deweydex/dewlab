---
title: "Functions and their graphs — Practice"
practice_for: drawing-functions
year: "2026-2027"
version: 2026.08.23.1
---

# Functions and their graphs — Practice

Each answer is hidden until you open it.

Several questions ask you to predict before you plot. The prediction is
the exercise. Then the plot shows you what the curve really does. The cell
below has the `draw` helper you need.

## Tools

```python exec
id: tools-1
import matplotlib.pyplot as plt

def draw(f, low=-5, high=5, steps=300, label=None, ax=None):
    xs = [low + (high - low) * i / steps for i in range(steps + 1)]
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend(fontsize=8)
    return ax


draw(lambda x: x ** 2, label="x^2")
```

## Is it a function?

**1.** Which of these are functions in the mathematical sense?

- (a) `def f(x): return x * 3 + 1`
- (b) `def g(x): return random.randint(1, 6)`
- (c) A rule that takes a person and gives their date of birth
- (d) A rule that takes a date and gives the people born on it

<details class="dl-answer"><summary>answer</summary>

(a) and (c) are functions. Each input gives exactly one output, every
time.

(b) is not a function. The same input can give different answers.

(d) is not a function if the output must be one person, because many
people are born on the same date. It becomes a function if the output
is a *set* of people. The usual fix is to change what the output is
allowed to be.

</details>

**2.** What is the domain of each function?

- (a) $f(x) = \dfrac{1}{x - 3}$
- (b) $g(x) = \sqrt{x + 4}$
- (c) $h(x) = x^2$
- (d) $k(x) = \dfrac{1}{\sqrt{x}}$

<details class="dl-answer"><summary>answer</summary>

(a) Every number except 3.

(b) Every number from $-4$ upwards.

(c) Every number.

(d) Every number greater than 0. Zero is left out because
$\sqrt{0} = 0$, and we cannot divide by zero.

</details>

**3.** A function has domain "all real numbers" and range "every number
from 2 upwards". Sketch a function that fits.

<details class="dl-answer"><summary>answer</summary>

Any function with a lowest value of 2 and no highest value fits.
$x^2 + 2$ is one example. $|x| + 2$ is another.

</details>

## Lines

**4.** For each line, give the slope and the point where it crosses the
vertical axis. Then predict: which line is steepest?

- (a) $y = 3x - 2$
- (b) $y = -5x + 1$
- (c) $y = 0.5x + 4$

<details class="dl-answer"><summary>answer</summary>

(a) Slope 3, crosses at $-2$.

(b) Slope $-5$, crosses at 1.

(c) Slope 0.5, crosses at 4.

(b) is steepest. Steepness depends on the size of the slope, and the
sign does not matter. A slope of $-5$ is steeper than a slope of 3. It
goes down instead of up.

</details>

**5.** Which of these lines pass through the origin?

$y = 2x$, $\quad y = 2x + 1$, $\quad y = -7x$, $\quad y = 4$

<details class="dl-answer"><summary>answer</summary>

The first and the third. A line passes through the origin exactly when
its intercept is zero.

$y = 4$ is a flat line at height 4. It never reaches the origin.

</details>

**6.** Plot $y = 2x + 1$ and $y = -x + 7$ on one pair of axes.

1. Find the point where they cross on the plot.
2. Check your answer by solving the equation.

<details class="dl-answer"><summary>answer</summary>

They cross at $(2, 5)$.

By algebra: $2x + 1 = -x + 7$, so $3x = 6$ and $x = 2$. Then
$y = 2(2) + 1 = 5$.

The two methods agree, so we can trust the picture. That means we can
use it where the algebra is harder.

</details>

## Curves

**7.** Before you plot: how many times does each curve cross the
horizontal axis?

- (a) $y = x^2 - 4$
- (b) $y = x^2 + 4$
- (c) $y = x^3 - x$
- (d) $y = x^3$

<details class="dl-answer"><summary>answer</summary>

(a) Twice, at $-2$ and 2.

(b) Never. The curve sits completely above the axis.

(c) Three times, at $-1$, 0 and 1.

(d) Once, at 0.

</details>

**8.** What is the largest number of times a cubic can cross the axis?
What about a quartic, which has an $x^4$?

<details class="dl-answer"><summary>answer</summary>

Three for a cubic, and four for a quartic. In general, a polynomial of
degree $n$ crosses the axis at most $n$ times, because it has at most
$n$ real roots.

It can cross fewer times. $x^3$ crosses once, and $x^2 + 4$ does not
cross at all. But it never crosses more than $n$ times.

</details>

**9.** Plot $y = x^2$, $y = 3x^2$ and $y = 0.2x^2$ together. What does
the coefficient in front of $x^2$ do? What does it not do?

<details class="dl-answer"><summary>answer</summary>

It stretches the curve up and down. A bigger coefficient makes the
curve look narrower.

It does not move the curve. All three curves still have their lowest
point at the origin. All three still meet the axis at only one point,
0, where they touch it.

</details>

**10.** Plot $y = x^3$ and $y = -x^3$. Describe the difference in one
sentence.

<details class="dl-answer"><summary>answer</summary>

The second curve is the first one turned upside down. It is a
reflection in the horizontal axis.

$x^3$ climbs from bottom left to top right. $-x^3$ falls from top left
to bottom right.

</details>

## Reading answers off the picture

**11.** Plot $y = x^2 - 3x - 4$ and read its roots from the plot. Then check them
with the quadratic formula.

<details class="dl-answer"><summary>answer</summary>

The curve crosses at $-1$ and 4.

With the formula: the discriminant is $9 + 16 = 25$, so the roots are
$\dfrac{3 \pm 5}{2}$, which gives 4 and $-1$.

</details>

**12.** Solve $x^3 - 2x = 1$ from a picture, to one decimal place.

<details class="dl-answer"><summary>answer</summary>

Plot $y = x^3 - 2x$ and the flat line $y = 1$. Read the crossings from the plot:
about $-1.0$, $-0.6$ and 1.6.

More exactly, the answers are $-1$, $-0.618$ and 1.618. The last two are
$\dfrac{1 \pm \sqrt{5}}{2}$, which are linked to the golden ratio.
To find them with algebra, you first have to spot that $-1$ is a root.
The picture needs no trick, so it is often the easier way.

</details>

**13.** Where do $y = x^2$ and $y = x + 2$ cross? Read it from the
picture, then check.

<details class="dl-answer"><summary>answer</summary>

At $(-1, 1)$ and $(2, 4)$.

To check, set them equal: $x^2 = x + 2$, so $x^2 - x - 2 = 0$. This
factorises as $(x - 2)(x + 1) = 0$, so $x = 2$ or $x = -1$.

</details>

**14.** A ball is thrown upwards. Its height in metres after $t$ seconds
is $h = 20t - 4.9t^2$. Plot it, then answer:

1. When does the ball land?
2. How high does it go?

<details class="dl-answer"><summary>answer</summary>

1. It lands when the height comes back to zero, at about $t = 4.08$
   seconds. To see this with algebra, set $20t - 4.9t^2 = 0$. That gives
   $t(20 - 4.9t) = 0$, so $t = 0$ or $t = 20/4.9$.
2. The highest point is halfway between the two roots, at
   $t \approx 2.04$. There the height is about 20.4 m.

The curve is symmetric about its peak. That is why the peak is halfway
between the roots.

</details>

## Inverses

**15.** What is the inverse of each function?

- (a) $f(x) = x + 7$
- (b) $f(x) = 5x$
- (c) $f(x) = 3x - 2$
- (d) $f(x) = x^3$

<details class="dl-answer"><summary>answer</summary>

(a) $x - 7$

(b) $\dfrac{x}{5}$

(c) $\dfrac{x + 2}{3}$

(d) The cube root, $\sqrt[3]{x}$, which is $x^{1/3}$.

Each inverse undoes the steps in reverse order. We did the same in
[Rearranging formulae: changing the subject](tutorial:rearranging-formulae).

A warning for (d) in Python: `x ** (1/3)` works for positive `x`, but
for a negative `x` it gives a complex number. Try `(-8) ** (1/3)` to
see.

</details>

**16.** Check one of your answers with a round trip: send several values
through the function and then through its inverse.

<details class="dl-answer"><summary>answer</summary>

```python
f = lambda x: 3 * x - 2
g = lambda x: (x + 2) / 3
print(all(abs(g(f(x)) - x) < 1e-9 for x in [-10, 0, 1.5, 7, 100]))
```

This prints `True`. Check the other direction too. `f(g(x))` should
also give `x` again.

</details>

**17.** Why does $x^2$ have no inverse over all the numbers, when $x^3$
does?

<details class="dl-answer"><summary>answer</summary>

Both 3 and $-3$ square to 9. So the inverse of 9 has two possible
answers, and a function may give only one.

Cubing never sends two numbers to the same place. The sign stays: the
cube of a negative number is negative. No two different numbers have the
same cube, so the cube root is a function for every number.

The usual fix for squaring is to limit the domain to numbers that are 0
or more. `math.sqrt` does this. It gives only the positive root.

</details>

**18.** Plot $y = 2x + 1$, its inverse, and $y = x$ on one pair of axes.
What do you notice?

<details class="dl-answer"><summary>answer</summary>

The inverse is $\dfrac{x - 1}{2}$. The two lines are mirror images in
the line $y = x$.

Swapping the inputs and outputs swaps the axes. So the graph of an
inverse is the graph of the function, reflected across the diagonal.

</details>

## One longer problem

**19.** A shop's profit, in euro, from selling $n$ items is
$P(n) = -0.5n^2 + 30n - 200$.

1. Plot it for $n$ from 0 to 60.
2. How many items must the shop sell to break even (no profit and no
   loss)?
3. How many items give the most profit, and how much is that profit?
4. What happens after about 52 items? Does that make sense?

<details class="dl-answer"><summary>answer</summary>

2. The shop breaks even where the curve crosses zero: at about
   $n = 7.6$ and $n = 52.4$. Items are whole, so the shop needs to sell
   8 to start making a profit.
3. The peak is halfway between the roots, at $n = 30$. There the profit
   is €250.
4. After 52 items, the model says the profit goes below zero and keeps
   falling. That is a feature of the model, not of the shop. A quadratic
   falls forever, but a real business would not keep making items at a
   loss.

**A model works over the range of data it was built from. Outside that
range, it may not.** Think about this before you use any model past its
data.

</details>
