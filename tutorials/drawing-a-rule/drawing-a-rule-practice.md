---
title: "Drawing a rule: graphs of functions — Practice"
practice_for: drawing-a-rule
year: "2026-2027"
version: 2026.09.25.1
---

# Drawing a rule: graphs of functions — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `plot_rule` from the
tutorial, `evaluate` from
[Rules with letters in them](tutorial:rules-with-letters-in-them), and
`close_enough`. Each call to `plot_rule` in one cell draws on the same
picture. The first cell below imports `matplotlib.pyplot` as `plt`, for
`plt.legend()` and the other drawing tools, and `math`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: drawing-a-practice-warm-up
import math
import matplotlib.pyplot as plt
# Try things here
```

**1. Predict.** The rule is $y = 2x + 1$. What are the coordinates of
its points at $x = 0$, 1 and 2? Then draw the rule from $-1$ to 3, and
find your three points on the line.

<details class="dl-answer"><summary>answer</summary>

$(0, 1)$, $(1, 3)$ and $(2, 5)$.

```python
def double_plus_one(x):
    """Return 2x + 1."""
    return 2 * x + 1

plot_rule(double_plus_one, -1, 3)
plt.plot([0, 1, 2], [1, 3, 5], "o")
```

The three dots sit on the line. Each step of 1 to the right goes 2 up,
and the line crosses the y-axis at 1, the $c$ of $y = mx + c$.

</details>

**2. Explain.** The graph of $y = x^2 - 4$ in the tutorial looks the
same on both sides of the y-axis, as if in a mirror. Why?

<details class="dl-answer"><summary>answer</summary>

A number and its negative have the same square: $(-3)^2 = 9 = 3^2$. So
$x$ and $-x$ always give the same $y$, and the point $(-x, y)$ is the
mirror of $(x, y)$ across the y-axis. The table in the tutorial showed
it too: 5 at $-3$ and at 3, $-3$ at $-1$ and at 1.

</details>

**3. Make.** Draw $y = 3 - x$ from $-2$ to 5. Read its root off the
graph, then check it by substituting.

<details class="dl-answer"><summary>answer</summary>

```python
def three_take_x(x):
    """Return 3 - x."""
    return 3 - x

plot_rule(three_take_x, -2, 5)
print(three_take_x(3))
```

The line slopes down, and meets the x-axis at $x = 3$. `three_take_x(3)`
is 0, so 3 is the root.

</details>

**4. Predict.** How many times will $y = x^2 + 1$ cross the x-axis?
Guess, then draw it from $-3$ to 3.

<details class="dl-answer"><summary>answer</summary>

None.

```python
def square_plus_one(x):
    """Return x squared, add 1."""
    return x ** 2 + 1

plot_rule(square_plus_one, -3, 3)
```

Every square is 0 or more, so $x^2 + 1$ is always 1 or more. The U sits
above the x-axis, and `plot_rule` draws no x-axis at all, because 0 is
not in view. The rule has no real roots.
[When there is no real answer](tutorial:when-there-is-no-real-answer)
builds a bigger space where it has two.

</details>

## Core

A cell for the core problems.

```python exec
id: drawing-a-practice-core
# Your working for problems 5 to 11
```

**5. Make.** On a weather app, $-40$ degrees is the one temperature
that is the same in Celsius and in Fahrenheit. Draw your toolkit's
`celsius_to_fahrenheit` and the rule $y = x$ on one picture, from $-60$
to 40, and find where they meet. Check by substituting.

<details class="dl-answer"><summary>answer</summary>

```python
def same_number(x):
    """Return x, unchanged."""
    return x

plot_rule(celsius_to_fahrenheit, -60, 40)
plot_rule(same_number, -60, 40)
plt.legend()
print(celsius_to_fahrenheit(-40))
```

The lines meet at $(-40, -40)$, and `celsius_to_fahrenheit(-40)` is
`-40.0`. Where the graph of a rule meets $y = x$, the rule gives back
the number it was given.

</details>

**6. Fix.** Schlomo, who is learning Python too, wants to draw an arch,
$y = 4 - x^2$. He remembers that some calculators and spreadsheets
write a power with `^`, so he tries it. His cell stops with an error.
Read the error, then change the rule.

```python exec
id: drawing-a-practice-fix-arch
def arch(x):
    """Return 4 take away x squared."""
    return 4 - x ^ 2

plot_rule(arch, -3, 3)
```

<details class="dl-answer"><summary>answer</summary>

The last line of the error is
`TypeError: unsupported operand type(s) for ^: 'float' and 'int'`.
In Python, `^` is not a power. It is XOR, from
[Bits that flip](tutorial:bits-that-flip), and it works only on whole
numbers, so the float `-3.0` makes it stop. The power is `**`:

```python
def arch(x):
    """Return 4 take away x squared."""
    return 4 - x ** 2

plot_rule(arch, -3, 3)
```

Now it draws an upside-down U, with its top at $(0, 4)$ and roots at
$-2$ and 2. Schlomo's memory was sound: spreadsheets do write powers
with `^`. Python keeps that sign for XOR. With whole numbers only,
`4 - x ^ 2` would have run and given other numbers with no error at
all, which is harder to notice.

</details>

**7. Make.** A basketball leaves a player's hands 2 m above the floor.
In a simple model, its height after $t$ seconds is $2 + 8t - 5t^2$
metres. If nobody catches it, when does it hit the floor? Draw the rule,
read the answer to one decimal place, then check by substituting.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write `basketball_height(seconds)`, which gives back the rule.
2. Draw it from 0 to 2 seconds. Where does it meet the x-axis?
3. Substitute your reading, and the numbers either side of it. Which
   side of 0 is each?

**Think about:** a reading from a graph is only as fine as the picture.
How could you get the second decimal place?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def basketball_height(seconds):
    """Return the height in metres of the basketball, seconds after it is thrown."""
    return 2 + 8 * seconds - 5 * seconds ** 2

plot_rule(basketball_height, 0, 2)
print(basketball_height(1.8), basketball_height(1.9))
```

The graph meets the x-axis at about 1.8 seconds. The height at 1.8 is
about 0.2 m, and at 1.9 it is below 0, so the ball lands between the
two, closer to 1.8. Drawing again from 1.8 to 1.85 gives about 1.82.

</details>

**8. Predict.** Two ways to back up the photos on a phone. Method A
takes 4 minutes to start, then 1.5 minutes for each gigabyte. Method B
takes 6 minutes to start, then 1.2 minutes for each gigabyte. (The
times are made up.) Which is faster for a small backup, and which for a
large one? Guess about where they take the same time, then draw both
from 0 to 15 GB and check.

<details class="dl-answer"><summary>answer</summary>

```python
def method_a(gigabytes):
    """Return method A's backup time in minutes for this many gigabytes."""
    return 4 + 1.5 * gigabytes

def method_b(gigabytes):
    """Return method B's backup time in minutes for this many gigabytes."""
    return 6 + 1.2 * gigabytes

plot_rule(method_a, 0, 15)
plot_rule(method_b, 0, 15)
plt.legend()
print(method_a(20 / 3), method_b(20 / 3))
```

Method A starts lower, and method B climbs more slowly, so A is faster
for small backups and B for large ones. The lines meet at about 6.7 GB,
where each takes 14 minutes. The exact crossing is $6\frac{2}{3}$ GB,
and both times print as `14.0`.

</details>

**9. Another way.** Find the roots of $y = x^2 - 4$ with no picture. Go
along $x$ from $-3$ to 3 in steps of 0.01, and print every place where
the value changes from negative to positive, or back.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start a name, `before`, at the value when $x$ is $-3$.
2. Make each next $x$ as `step / 100`, for `step` in
   `range(-299, 301)`. After each check, the new value becomes
   `before`.
3. When `before` and the new value have different signs, or the new
   value is 0, print $x$.

**Think about:** `plot_rule` works out a table like this and draws it.
What do you get from the table that the picture did not give you?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
before = evaluate([-4, 0, 1], -3)
for step in range(-299, 301):
    x = step / 100
    now = evaluate([-4, 0, 1], x)
    if now == 0 or (before < 0) != (now < 0):
        print(x, now)
    before = now
```

It prints `-2.0 0.0`, then `-1.99`, then `2.0 0.0`. The roots are $-2$
and 2. The line at $-1.99$ is where the value first goes below 0, one
step after the root. A table like this gives numbers you can print; a
picture gives the shape at a glance. Here the search found each root
exactly, because $-2$ and 2 are on the table's steps.

</details>

**10. Explain.** The graph of $y = \frac{1}{x}$ creeps towards the
x-axis and never reaches it. Schlomi, who is learning Python too, is
not so sure. "Take $x$ big enough and it does reach 0. Python says so."
She runs `print(1 / 10 ** 400)`, and it prints `0.0`. Which should we
believe, the graph or Python? Why?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What number, times $x$, makes 1? Could that number be 0?
2. Try `print(1 / 10 ** 300)` and `print(1 / 10 ** 330)`.
3. Which space is each answer in: the real numbers, or Python's floats?

</details>

<details class="dl-answer"><summary>answer</summary>

Both, each in its own space. In the real numbers, $\frac{1}{x}$ is
the number that, times $x$, makes 1. If it were 0, then 0 times $x$
would be 1, but 0 times any number is 0. So $\frac{1}{x}$ can be as
small as you like, when $x$ is large, but never 0: the equation
$\frac{1}{x} = 0$ has no answer in $\mathbb{R}$.

Schlomi's `0.0` is true of floats. A float cannot hold a number much
smaller than about $10^{-308}$ in the usual way, and nothing below
about $5 \times 10^{-324}$ at all, so $10^{-400}$ is rounded to 0.0.
`1 / 10 ** 300` still prints `1e-300`. Her experiment found the edge of
Python's number space, which the graph, drawn in $\mathbb{R}$, does not
have.

</details>

**11. Make.** A shared drive of 60 GB is split equally among the people
who use it. Draw the rule $\frac{60}{x}$ from 1 to 10 as a curve. On the
same picture, draw dots at the whole numbers 1 to 10 only. Which picture
tells the truth about sharing a drive among people, and why?

<details class="dl-answer"><summary>answer</summary>

```python
def each_share(people):
    """Return each person's share in GB when 60 GB is shared by people."""
    return 60 / people

plot_rule(each_share, 1, 10)
dots_x = []
dots_y = []
for people in range(1, 11):
    dots_x.append(people)
    dots_y.append(each_share(people))
plt.plot(dots_x, dots_y, "o")
```

The dots tell the truth. People come in whole numbers, so the domain
of this rule is 1, 2, 3 and so on. The curve has a value at 2.5 people,
24 GB, which means nothing. A curve says "every value in between makes
sense". For a speed, a temperature, or a time, it does. For a
count of people, it does not.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: drawing-a-practice-stretch
# Your working for problems 12 to 16
```

**12. Predict.** Which is bigger at $x = 10$: $x^3$ or $2^x$? Guess,
then draw both from 0 to 12, and find where they meet.

<details class="dl-answer"><summary>answer</summary>

```python
def cubed(x):
    """Return x cubed."""
    return x ** 3

def two_to_the(x):
    """Return 2 to the power x."""
    return 2 ** x

plot_rule(cubed, 0, 12)
plot_rule(two_to_the, 0, 12)
plt.legend()
print(cubed(10), two_to_the(10))
```

$2^{10}$ is 1,024 and $10^3$ is 1,000, so $2^x$ is barely ahead. The
graphs meet twice, at about 1.4 and about 9.9. Between those, $x^3$ is
ahead. After 9.9, $2^x$ pulls away and never looks back. Every power
of $x$, however high, is overtaken by $2^x$ in the end.

</details>

**13. Make.** Draw the cubic $y = (x + 1)(x - 1)(x - 3)$. First expand
it by hand, or with the tutorial's grid, into a list for `evaluate`.
Before you draw it, say where its roots will be. Then check them by
substituting.

<details class="dl-answer"><summary>answer</summary>

$(x + 1)(x - 1) = x^2 - 1$, and $(x^2 - 1)(x - 3) = x^3 - 3x^2 - x + 3$,
which is the list `[3, -1, -3, 1]`. The roots are where a bracket is 0:
$-1$, 1 and 3.

```python
def three_roots(x):
    """Return (x + 1)(x - 1)(x - 3), expanded."""
    return evaluate([3, -1, -3, 1], x)

plot_rule(three_roots, -2, 4)
print(three_roots(-1), three_roots(1), three_roots(3))
```

It prints `0 0 0`, and the graph crosses the x-axis three times, as a
cubic can.

</details>

**14. Another way.** When is $2^x = 10$? Draw $2^x$ and the flat line
$y = 10$ from 0 to 5, and read where they meet. Then find the same
answer another way, with a function from
[Doubling and halving](tutorial:doubling-and-halving#doublings-add-up).

<details class="dl-answer"><summary>answer</summary>

```python
def ten(x):
    """Return 10, whatever x is."""
    return 10

plot_rule(two_to_the, 0, 5)
plot_rule(ten, 0, 5)
print(math.log2(10))
```

The graphs meet at about $x = 3.3$. `math.log2(10)` is about 3.32: the
logarithm answers "how many doublings make 10?", which is the same
question. Reading off the graph and using the inverse function are two
routes to one answer.

</details>

**15. Fix.** This cell should draw server A's time from the tutorial.
It stops with a `TypeError`. Find the line that causes it.

```python exec
id: drawing-a-practice-fix-return
def server_time(thousands):
    """Return server A's time to answer in ms: 8, plus 2 for each thousand people."""
    8 + 2 * thousands

plot_rule(server_time, 0, 10)
```

<details class="dl-answer"><summary>answer</summary>

The last line of the error is
`TypeError: '<' not supported between instances of 'NoneType' and 'NoneType'`.
The function works out `8 + 2 * thousands` and then throws it away,
because there is no `return`. So it gives back `None` for every
point, and `plot_rule` stops when it asks for the smallest of its
values to decide where the x-axis goes: `None` cannot be compared with
`None`.

```python
def server_time(thousands):
    """Return server A's time to answer in ms: 8, plus 2 for each thousand people."""
    return 8 + 2 * thousands

plot_rule(server_time, 0, 10)
```

The error was raised inside `plot_rule`, but the missing `return` was
in `server_time`. The traceback lists both. The line at the bottom says
what happened, and the lines above say where it came from.

</details>

**16. Explain.** Run this cell. The tutorial said `plot_rule` works out
401 points so that it does not miss a dip. Does this graph cross zero?
Then substitute 3.002. What happened, and how could you have found out?

```python exec
id: drawing-a-practice-narrow
def narrow_dip(x):
    """Return (x - 3.001)(x - 3.003)."""
    return (x - 3.001) * (x - 3.003)

plot_rule(narrow_dip, 0, 7)
```

<details class="dl-answer"><summary>answer</summary>

The graph seems to touch 0 and stay above it. Every one of the 401
points is above 0: the smallest is about 0.00006. But the rule has two
roots, 3.001 and 3.003, and between them it dips below 0:

```python
print(narrow_dip(3.002))
plot_rule(narrow_dip, 3, 3.004)
```

`narrow_dip(3.002)` is about $-0.000001$. The points of the graph are
0.0175 apart, and the whole dip is only 0.002 wide, so no point landed
in it. More points would help for this rule, but some other rule will
always have a narrower dip. Zooming in near where a graph comes close
to 0 is one way to find out. Algebra is another: the brackets show the
two roots with no picture at all.

</details>
