---
title: "Solving by computing: bisection and Newton's method"
year: "2026-2027"
version: 2026.09.24.1
covers:
  squeezing-a-root-between-two-guesses:
    covers: [MIT-6.6]
    touches: [MIT-3.2]
  bisection-binary-search-on-a-number-line:
    covers: [MIT-6.6]
    touches: [MIT-1.1, PDP-LO6]
  a-tool-that-halves:
    covers: [MIT-6.6]
    touches: [PDP-LO8, PDP-LO10]
  following-the-tangent-down-newtons-method:
    covers: [MIT-3.6]
    touches: [MIT-4.2]
  a-tool-that-follows-tangents:
    covers: [MIT-3.6, MIT-6.6]
    touches: [PDP-LO8, PDP-LO10]
  when-the-tangent-is-flat:
    covers: [MIT-3.6]
    touches: [PDP-LO9]
---

# Solving by computing: bisection and Newton's method

Fold a sheet of A4 paper in half, and the half has the same shape as
the whole sheet. That only works because the long side is $\sqrt{2}$
times the short side. It is 210 mm across, and $210 \times \sqrt{2}$,
about 297 mm, down. Your calculator says $\sqrt{2}$ is 1.4142135623730951.
But a calculator can only add, take away, multiply and divide, and no
amount of adding gives a number whose digits never end. So where do
those digits come from? Most people trust the square-root button
without asking. This page shows what is
inside it.

<aside class="dl-note" id="solving-by-note-a4">

**Why A4 is that shape.** The international standard for paper sizes,
ISO 216, starts from A0, a sheet with an area of one square metre and
sides in the ratio $1 : \sqrt{2}$. Fold it in half and you get A1, the
same shape. Fold again for A2, and so on down to A4.

</aside>

On this page we:

- trap $\sqrt{2}$ between two guesses, using a sign change
- halve the gap between the guesses again and again, which is binary
  search on a number line, and add `bisect_root` to the toolkit
- follow a tangent down to zero, which is Newton's method, and add
  `newton` to the toolkit
- race the two methods, and count their steps
- watch Newton's method fail on a flat tangent, and ask why

> **The space we're in.** Real numbers, kept as floats, and rules
> whose graphs have no gaps. We cannot solve $x^2 = 2$ by writing down
> the answer, because its digits never end, as
> [How a computer stores a number](tutorial:how-a-computer-stores-a-number#the-square-root-of-2)
> showed. So we change the question. "What is the answer?" becomes
> "Which float is close enough?". Every method on this page gives a sequence of guesses, like the sequences
> on [Getting closer](tutorial:getting-closer), and stops when a guess
> is good enough, not when it is exact.

## Warm-up

The first question is from
[Finding things fast](tutorial:finding-things-fast#the-guessing-game),
and the second from
[Rules for change](tutorial:rules-for-change#a-pattern-in-the-slopes-the-power-rule).

```question
id: solving-by-warm-up-1
type: fill-in-the-blank

In the guessing game, a friend thinks of a whole number from 1 to 100
and says "higher" or "lower". Guessing the middle each time, you never
need more than {7} guesses.
```

```question
id: solving-by-warm-up-2
type: multiple-choice
answer: 2

What is the slope of $y = x^2 - 2$ at $x = 3$?

- 7
  - 7 is the height of the curve at x = 3, not its slope.
- 6
  - The slope of x² is 2x, and the −2 moves the curve down without changing its slope: 2 × 3.
- 9
  - 9 is 3², the height of x² at 3.
- 4
  - This takes the 2 off the slope, but moving a curve down leaves its slope as it was.
```

## Squeezing a root between two guesses

To find $\sqrt{2}$, we look for the number whose square is 2. Said
another way, we look for a root of the rule $x^2 - 2$. A root is an $x$
where the rule gives 0, as on
[Drawing a rule](tutorial:drawing-a-rule#a-tool-that-draws-any-rule).

Let's try a few guesses. Before you run the cell, which two whole
numbers do you think $\sqrt{2}$ sits between?

```python exec
id: solving-by-squeeze-1
def square_gap(x):
    """Return how far x squared is from 2. It is 0 when x is the square root of 2."""
    return x ** 2 - 2

for guess in [0, 1, 1.4, 1.5, 2]:
    print(guess, square_gap(guess))

plot_rule(square_gap, 0, 2)
```

At 1 the rule gives $-1$, below zero. At 2 it gives 2, above zero. The
graph has no gaps, so to get from below zero to above zero it must
cross zero somewhere between 1 and 2. That crossing is $\sqrt{2}$.

This is the idea of the whole page. A *sign change* is a pair of
inputs where a rule gives a negative value at one and a positive value
at the other. If a rule has a sign change and its graph has no gap,
there is a root between the two inputs. The guesses 1.4 and 1.5 also
give a sign change, so the root is between them too. Each new pair of
guesses squeezes it into a smaller space.

## Bisection: binary search on a number line

How should we choose the next guess? On
[Finding things fast](tutorial:finding-things-fast#binary-search-halve-what-is-left),
binary search looked at the middle of a sorted list, and ignored the
half where the target could not be. We can do the same on a number
line.

Start with `low` at 1 and `high` at 2. Look at the middle. If the sign
changes between `low` and the middle, the root is in the left half, so
the middle becomes the new `high`. If not, the root is in the right
half, so the middle becomes the new `low`. This method is called
*bisection*, which means "cutting in two".

To test for a sign change, we multiply the two values. A negative times
a positive is negative, and two values with the same sign make a
positive. So `square_gap(low) * square_gap(middle) <= 0` means the
root is in the left half. (The `=` catches a middle that is exactly the
root.)

How close do you think 8 halvings will get? Guess, then run it.

```python exec
id: solving-by-bisect-1
low = 1
high = 2
for step in range(1, 9):
    middle = (low + high) / 2
    if square_gap(low) * square_gap(middle) <= 0:
        high = middle
    else:
        low = middle
    print(step, low, high, "gap:", high - low)
```

Read it as a sequence. The gap between `low` and `high` halves at every
step: 0.5, 0.25, 0.125, and after 8 steps it is 0.00390625. The root is
always inside. After 8 steps we know that $\sqrt{2}$ is between 1.4140625
and 1.41796875, so its first two decimal places are 1.41.

Bisection is divide and conquer, as the guessing game was. Each step
turns the problem into the same problem, half the size.

How many steps until the gap is below a billionth, $10^{-9}$? The gap
starts at 1, and after $k$ steps it is $\frac{1}{2^k}$. So we want the
first $k$ with $2^k \geq 10^9$. On
[Doubling and halving](tutorial:doubling-and-halving#halving-down-to-1),
that was a logarithm: $k = \log_2 10^9$, rounded up. Predict it with
$2^{10} \approx 1000$ before you run the cell.

```python exec
id: solving-by-bisect-2
import math

print(math.log2(10 ** 9))
print(math.ceil(math.log2(10 ** 9)))
print(halvings(10 ** 9) + 1)
```

It takes thirty steps. $10^9$ is $1000^3$, and each thousand is about 10
halvings. Every step gives us about one more correct binary digit.

### Your turn

1. In the cell below, write a rule `three_gap` for $x^2 - 3$. Which
   `low` and `high` give a sign change?
2. Copy the bisection loop into the cell, using `three_gap`. What are
   the first two decimal places of $\sqrt{3}$?
3. How many steps would a gap of 1 need to get below 0.001?

```python exec
id: solving-by-bisect-your-turn
# Your square root of 3
```

## A tool that halves

The loop becomes a tool. Its promise has a condition: the rule must
have a sign change between `low` and `high`. You write the body. It is
the last cell with `square_gap` changed to `rule`, and
the `for` loop changed to a `while` loop that stops when the gap is no
bigger than `tolerance`.

```python exec
id: solving-by-toolkit-bisect
toolkit: yes
def bisect_root(rule, low, high, tolerance=1e-9):
    """Return an x between low and high where rule(x) is 0, to within tolerance.

    rule(low) and rule(high) must have opposite signs (or one of them is 0),
    and the graph of rule must have no gap between them. Each step halves
    the gap between low and high, and keeps the half with the sign change.
    Raises ValueError when there is no sign change.
    """
    ...
```

```python toolkit-reference
for: solving-by-toolkit-bisect
def bisect_root(rule, low, high, tolerance=1e-9):
    """Return an x between low and high where rule(x) is 0, to within tolerance.

    rule(low) and rule(high) must have opposite signs (or one of them is 0),
    and the graph of rule must have no gap between them. Each step halves
    the gap between low and high, and keeps the half with the sign change.
    Raises ValueError when there is no sign change.
    """
    if rule(low) * rule(high) > 0:
        raise ValueError("rule(low) and rule(high) have the same sign")
    while high - low > tolerance:
        middle = (low + high) / 2
        if rule(low) * rule(middle) <= 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2
```

```hint
What does `print(bisect_root(square_gap, 1, 2))` show? If it shows
`None`, the function has no `return` yet. What should it give back once
the gap between `low` and `high` is small enough?
```

```hint
after: 10 errors
title: some steps
1. If `rule(low) * rule(high)` is more than 0, raise a `ValueError`.
2. While `high - low` is bigger than `tolerance`, find the middle.
3. Keep the half with the sign change, as the last cell did.
4. After the loop, return the middle of `low` and `high`.

**Think about:** why does the loop need no counter, when the last cell
had one?
```

The tests check $\sqrt{2}$ against `math.sqrt`, a root that
[Solving for x](tutorial:solving-for-x#the-quadratic-formula) could
find with a formula, and a root that sits exactly on `low`. Until
`bisect_root` is written, the first test stops with a `TypeError`.

```python exec
id: solving-by-toolkit-bisect-tests
def quadratic_rule(x):
    return x ** 2 - 5 * x + 6

def line_rule(x):
    return 2 * x - 6

assert close_enough(bisect_root(square_gap, 1, 2), math.sqrt(2))
assert close_enough(bisect_root(quadratic_rule, 2.5, 10), solve_quadratic(1, -5, 6)[1])
assert close_enough(bisect_root(line_rule, 3, 8), 3), "a root at low"
assert close_enough(bisect_root(square_gap, 1, 2, tolerance=0.01), math.sqrt(2), tolerance=0.01)
print("bisect_root keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

```python
def bisect_root(rule, low, high, tolerance=1e-9):
    """Return an x between low and high where rule(x) is 0, to within tolerance.

    rule(low) and rule(high) must have opposite signs (or one of them is 0),
    and the graph of rule must have no gap between them. Each step halves
    the gap between low and high, and keeps the half with the sign change.
    Raises ValueError when there is no sign change.
    """
    if rule(low) * rule(high) > 0:
        raise ValueError("rule(low) and rule(high) have the same sign")
    while high - low > tolerance:
        middle = (low + high) / 2
        if rule(low) * rule(middle) <= 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2
```

</details>

### Where bisection can be fooled

The promise said "no gap". On
[Drawing a rule](tutorial:drawing-a-rule#rules-with-gaps-and-rules-that-race),
$\frac{1}{x}$ had a gap at 0: negative on the left, positive on the
right, and never 0. If you have not written `bisect_root` yet, open the
answer under the tests and copy it into the stub. What do you think it
will say about $\frac{1}{x}$ between $-1$ and 2?

```python exec
id: solving-by-fooled-1
def one_over(x):
    return 1 / x

fake_root = bisect_root(one_over, -1, 2)
print(fake_root, one_over(fake_root))
```

It returns a number very close to 0, and $\frac{1}{x}$ there is
billions, nowhere near 0. The sign changed, but across a gap, not a
crossing. Bisection kept its promise to halve and keep the sign change.
The rule broke the condition the promise depended on. So before you
trust a root, put it back in the rule, as Unit 7 did every time.

## Following the tangent down: Newton's method

Bisection is sure, but slow. It takes about 30 steps for 9 decimal
places. It only uses the sign of the rule, never its size or its
shape. Can a guess use more?

On
[How fast, right now?](tutorial:how-fast-right-now#the-tangent-line),
the tangent line was the straight line that touches a curve at one
point, with the curve's slope there. Close to that point, the curve and its tangent are
nearly the same. And a straight line is a rule we can solve.

So here is a plan. Start with a guess. Draw the tangent at the guess.
Follow the tangent down to where it meets zero. That point is the next
guess. The cell draws it for the guess 1. Before you run it, where do
you expect the tangent to meet the axis?

```python exec
id: solving-by-newton-1
import matplotlib.pyplot as plt

guess = 1
height = square_gap(guess)
tangent_slope = derivative_at(square_gap, guess)
next_guess = guess - height / tangent_slope
print("slope", round(tangent_slope, 6), " next guess", round(next_guess, 6))

plot_rule(square_gap, 0.5, 2)
plt.plot([guess, next_guess], [height, 0], "--o")
```

The tangent at 1 has slope 2, and it meets zero at 1.5. From 1, the
next guess is 1.5, much closer to 1.414 than 1 was.

Where does the formula come from? The tangent starts at height
$f(g)$ above the guess $g$, and drops by $f'(g)$ for every step
across. To drop the whole height, it must go $\frac{f(g)}{f'(g)}$
across, as rise over run on
[Straight lines](tutorial:straight-lines#how-steep-is-a-ramp) said. In
words: from the guess, go back by the height divided by the slope.

$$\text{next guess} = g - \frac{f(g)}{f'(g)}$$

*Newton's method* uses that step again and again. Here are six
steps from the guess 1. Watch the last column. How fast do you think
it will shrink?

```python exec
id: solving-by-newton-2
guess = 1
for step in range(1, 7):
    guess = guess - square_gap(guess) / derivative_at(square_gap, guess)
    print(step, guess, "error:", guess - math.sqrt(2))
```

The errors go 0.09, 0.002, 0.000002, 0.0000000000016, and then 0.
After four steps the guess matches $\sqrt{2}$ to 11 decimal places, and after
five it is the float `math.sqrt` gives. The sixth step moves it by one
float's width, about $2 \times 10^{-16}$. The number of correct digits
roughly doubles at every step, once the guess is close. I find that
astonishing every time. Bisection adds one binary digit a step, and
this doubles the digits it already had.

For $x^2 - 2$, the slope is $2x$, as
[Rules for change](tutorial:rules-for-change#a-pattern-in-the-slopes-the-power-rule)
showed, and the step becomes "the average of $g$ and $\frac{2}{g}$".
That form is nearly 2,000 years old. Heron of Alexandria described it
as a way to find square roots.

<aside class="dl-note" id="solving-by-note-raphson">

**Newton and Raphson.** Isaac Newton described a version of this
method in 1669, working on one equation at a time. Joseph Raphson
published a simpler, general form in 1690, so it is often called the
Newton–Raphson method.

</aside>

## A tool that follows tangents

The six-step loop becomes your second tool. Its promise has a
condition too. Newton's method needs a start close enough to a root,
where the curve is not flat.

```python exec
id: solving-by-toolkit-newton
toolkit: yes
def newton(rule, start, steps=20):
    """Return a guess at a root of rule, found by Newton's method.

    From start, each step follows the tangent to where it meets 0:
    guess - rule(guess) / derivative_at(rule, guess). It takes this
    step steps times. It works best when start is near a root, and it
    fails when a tangent on the way is flat.
    """
    ...
```

```python toolkit-reference
for: solving-by-toolkit-newton
def newton(rule, start, steps=20):
    """Return a guess at a root of rule, found by Newton's method.

    From start, each step follows the tangent to where it meets 0:
    guess - rule(guess) / derivative_at(rule, guess). It takes this
    step steps times. It works best when start is near a root, and it
    fails when a tangent on the way is flat.
    """
    guess = start
    for step in range(steps):
        guess = guess - rule(guess) / derivative_at(rule, guess)
    return guess
```

```hint
after: 8 errors
title: some steps
1. Give the name `guess` to `start`.
2. Loop `steps` times. Each time, work out the next guess from the
   formula, and give it the name `guess`.
3. After the loop, return `guess`.

**Think about:** the loop runs 20 times even when the guess stopped
changing after 5. Does that do any harm?
```

A water tank shaped like a cube must hold 10 cubic metres. How long is
each side? The side $s$ must make $s^3 = 10$, a cube root, and the
tests find it both ways. Until `newton` is written, the first test
stops with a `TypeError`.

```python exec
id: solving-by-toolkit-newton-tests
def tank_gap(side):
    """Return how far a cube with this side, in metres, is from holding 10 cubic metres."""
    return side ** 3 - 10

assert close_enough(newton(square_gap, 1), math.sqrt(2))
assert close_enough(newton(quadratic_rule, 5), 3)
tank_side = newton(tank_gap, 2)
assert close_enough(tank_side, bisect_root(tank_gap, 2, 3))
assert close_enough(tank_side ** 3, 10)
print("newton keeps its promise. The tank's side is", round(tank_side, 3), "m.")
```

<details class="dl-answer"><summary>answer</summary>

```python
def newton(rule, start, steps=20):
    """Return a guess at a root of rule, found by Newton's method.

    From start, each step follows the tangent to where it meets 0:
    guess - rule(guess) / derivative_at(rule, guess). It takes this
    step steps times. It works best when start is near a root, and it
    fails when a tangent on the way is flat.
    """
    guess = start
    for step in range(steps):
        guess = guess - rule(guess) / derivative_at(rule, guess)
    return guess
```

</details>

The tank's side is about 2.154 m. The tests
checked Newton against bisection, and then put the answer back in.

### A race

Bisection needed 30 steps for 9 decimal places. Newton's method needed
4 or 5. Each Newton step does more work, because it calculates a slope,
and `derivative_at` calculates the rule twice. So a fair count is how
many times each method calculates the rule: about 30 for bisection, and
about 15 for Newton. Newton still wins, and the gap grows with every
extra digit we ask for.

## When the tangent is flat

What if the first guess for $\sqrt{2}$ is 0? The cell is meant to stop
with an error. If you have not written `newton` yet, open the answer
under its tests and copy it into the stub. Before you run it, look at
the graph of $x^2 - 2$ at 0. What is its tangent there?

```python exec
id: solving-by-flat-1
print(newton(square_gap, 0))
```

The last line reads `ZeroDivisionError: float division by zero`. At 0
the parabola is at its lowest point, its vertex, as on
[The top of the curve](tutorial:the-top-of-the-curve#a-curve-that-turns).
The tangent there is flat, with slope 0. A flat line never meets zero,
so "follow the tangent down" has nowhere to go.

Newton's method needs a space where the slope is not 0, and 0 is outside that space. Start a little to the
side, at 0.01, and the tangent is nearly flat. What do you expect?

```python exec
id: solving-by-flat-2
guess = 0.01
for step in range(1, 12):
    guess = guess - square_gap(guess) / derivative_at(square_gap, guess)
    print(step, guess)
```

The first step sends the guess to 100. Then it walks back,
roughly halving each time, and only speeds up near the root. It gets
there in the end, after 11 steps, not 5.

So each method lives in its own space:

| | Bisection | Newton's method |
|---|---|---|
| needs | a sign change, and no gap | a start near a root, and no flat tangent |
| each step | halves the gap | follows the tangent to zero |
| uses | the sign of the rule | the value and the slope of the rule |
| steps for $10^{-9}$ | about 30 | about 5, when it works |
| when it fails | on a gap, and it does not say so | on a flat tangent, sometimes with an error |

Many real solvers use both. Bisection keeps the root trapped, and
Newton's method takes over once a guess is close, where it is fast.

### Your turn

1. Find $\sqrt{10}$ with `newton`, starting at 3. Check it with
   `math.sqrt`.
2. Find it again with `bisect_root`. Which two whole numbers make a
   good `low` and `high`?
3. Try `newton(square_gap, -1)`. Which root does it find? Why did the
   tangent lead there?

```python exec
id: solving-by-flat-your-turn
# Your square root of 10, two ways
```

<details class="dl-why"><summary>Why this way?</summary>

This page taught bisection first, and Newton's method second, and it
counted steps for both.

Many courses teach only Newton's method, as a formula to use on an
exam question, and it is the one worth knowing if you only learn one.
It is fast, it uses the slope from the last two pages, and many
calculators and libraries use it to find roots.

We started with bisection because it is binary search again, and it
never loses the root. With both on the page, you can see what speed
costs: Newton's method is fast, and it needs a good start.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | `low` and `high`, the two ends of the trap; a guess $g$, and the next guess |
| What is promised? | `bisect_root` promises a root when there is a sign change and no gap; `newton` promises a root when the start is close and no tangent is flat |
| What happens when? | each method makes a sequence of guesses; bisection halves the gap each step, and Newton's digits roughly double each step |
| What does this space let us do? | floats let us stop at "close enough"; a rule with a gap can fool bisection, and a flat tangent stops Newton's method |

## What we have now

| Term or tool | What it means |
|---|---|
| sign change | a rule negative at one input and positive at another |
| bisection | halving the gap around a sign change, again and again |
| $2^k \geq \frac{1}{\text{tolerance}}$ | how many bisection steps are needed, when the gap starts at 1 |
| `bisect_root(rule, low, high, tolerance=1e-9)` | your toolkit tool: a root found by bisection |
| Newton's method, $g - \frac{f(g)}{f'(g)}$ | follow the tangent at the guess down to zero, and repeat |
| `newton(rule, start, steps=20)` | your toolkit tool: a root found by Newton's method |
| a flat tangent | where Newton's method has nowhere to go |

The practice page is next. Then
[Putting the derivative to work](tutorial:putting-the-derivative-to-work)
lets you choose a project that uses everything in this unit, before the
mixed problems.

## Where to read more

3Blue1Brown (2021). *Newton's fractal (which Newton knew nothing about).*
<https://www.youtube.com/watch?v=-RdOwhmqP5s>. What happens when Newton's
method starts from every point on a plane? Grant Sanderson colours each
start by the root it reaches, and finds a fractal. About twenty-six
minutes, and the second half is harder.
