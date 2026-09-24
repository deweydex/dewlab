---
title: "Getting closer: limits — Practice"
practice_for: getting-closer
year: "2026-2027"
version: 2026.09.24.1
---

# Getting closer: limits — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, with `plot_rule` from
[Drawing a rule](tutorial:drawing-a-rule) and `close_enough` from
[Does it work?](tutorial:does-it-work). `approach` belonged to the
tutorial page only, so the first cell below writes it again. Run that
cell first.

## Warm-up

```python exec
id: getting-closer-practice-warm-up
import math

def approach(rule, a, rows=10):
    """Print rule just left and just right of a, halving the step on each row."""
    step = 1
    for row in range(rows):
        print(step, rule(a - step), rule(a + step))
        step = step / 2

# Try things here
```

**1. Predict.** A ball is dropped from 2 metres. Each bounce takes it
back up to half the height of the one before. What do the heights head
for? Will any row print 0?

```python
height = 2.0
for bounce in range(8):
    print(bounce, height)
    height = height / 2
```

<details class="dl-answer"><summary>answer</summary>

The heights are 2.0, 1.0, 0.5, 0.25, and so on, down to 0.015625 after
7 bounces. No row prints 0: halving a number that is not 0 never gives
0. But the heights get as close to 0 as we like, so the limit of the
sequence is 0. (A real ball does stop, after a dozen or so bounces. The
rule "half the height every time" is a model, and it stops being true
when the bounces get very small.)

</details>

**2. Make.** The rule $\frac{x^2 - 9}{x - 3}$ has a hole at $x = 3$.
Use `approach` to find its limit there. Then find the same answer by
cancelling, as the tutorial did for $\frac{x^2 - 4}{x - 2}$.

<details class="dl-answer"><summary>answer</summary>

```python
def nine_hole(x):
    return (x ** 2 - 9) / (x - 3)

approach(nine_hole, 3, rows=6)
```

The left column climbs 5.0, 5.5, 5.75, 5.875, and the right column
falls 7.0, 6.5, 6.25, 6.125. Both head for 6. By algebra,
$x^2 - 9 = (x - 3)(x + 3)$, so away from 3 the rule is $x + 3$, and
$3 + 3 = 6$.

</details>

**3. Explain.** For each rule, say whether it has a *value* at the
point, and whether it has a *limit* there.

- $\frac{x^2 - 4}{x - 2}$ at $x = 2$
- the parking fee (€2 up to 1 hour, €5 for longer) at 1 hour
- $x + 2$ at $x = 2$

<details class="dl-answer"><summary>answer</summary>

- $\frac{x^2 - 4}{x - 2}$ at 2: no value, since $\frac{0}{0}$ has
  none, but a limit of 4.
- The parking fee at 1 hour: a value, €2, but no limit, because the
  left side heads for 2 and the right side for 5.
- $x + 2$ at 2: a value, 4, and a limit, 4, and they agree.

The first two show that a value and a limit are separate questions.
The third is the usual case, where there is no hole and no jump.

</details>

**4. Predict.** What do these two lines print?

```python
print(1 + 1e-16 == 1)
print(1 + 1e-15 == 1)
```

<details class="dl-answer"><summary>answer</summary>

`True`, then `False`. The gap between neighbouring floats near 1 is
about $2.2 \times 10^{-16}$, as on
[How a computer stores a number](tutorial:how-a-computer-stores-a-number#reading-e-16).
$10^{-16}$ is less than half that gap, so $1 + 10^{-16}$ is kept as 1.
$10^{-15}$ is bigger than the gap, so $1 + 10^{-15}$ lands on a
different float. This is why the bank's table broke at $10^{16}$
payments.

</details>

## Core

A cell for the core problems.

```python exec
id: getting-closer-practice-core
# Your working for problems 5 to 11
```

**5. Make.** A sound engineer's formula for a wave has
$\frac{1 - \cos x}{x^2}$ in it, with $x$ in radians. At $x = 0$ it is
$\frac{0}{0}$. Write it as a function, and use `approach` to find its
limit at 0.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write `def cos_rule(x):` and give back `(1 - math.cos(x)) / x ** 2`.
2. Call `approach(cos_rule, 0)`.
3. Read the columns: what number do they head for?

**Think about:** why are the two columns the same?

**Try this next:** what happens with `approach(cos_rule, 0, rows=40)`?
Problem 13 has the reason.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def cos_rule(x):
    return (1 - math.cos(x)) / x ** 2

approach(cos_rule, 0)
```

The values go 0.4597, 0.4897, 0.4974, 0.4993, and after ten rows
0.49999984. The limit is 0.5, or $\frac{1}{2}$. The two columns are the
same because $\cos(-x) = \cos x$ and $(-x)^2 = x^2$: the rule gives
the same value on each side.

</details>

**6. Fix.** Here is someone's version of `approach`. Run it. The table
never gets any closer to 6. Find the one mistake.

```python exec
id: getting-closer-practice-fix
def approach_again(rule, a, rows=6):
    """Print rule just left and just right of a, halving the step on each row."""
    step = 1
    for row in range(rows):
        print(step, rule(a - step), rule(a + step))
    step = step / 2

def nine_hole(x):
    return (x ** 2 - 9) / (x - 3)

approach_again(nine_hole, 3)
```

<details class="dl-answer"><summary>answer</summary>

Every row prints `1 5.0 7.0`. The line `step = step / 2` is not
indented under the `for`, so it runs once, after the loop has finished.
The step is 1 on every row. The fix is to indent it:

```python
    for row in range(rows):
        print(step, rule(a - step), rule(a + step))
        step = step / 2
```

The order of the lines was right. Their place was not: indentation
says which lines are inside the loop, and so which lines happen again.

</details>

**7. Make.** A small café pays €300 a week for its coffee machine,
however many cups it makes, and €0.50 for the beans and milk in each
cup. So the average cost of a cup, when it makes $n$ cups, is
$\frac{300 + 0.5n}{n}$. What happens to the average cost as $n$
grows? Try 10, 100, 1,000, 10,000 and 1,000,000 cups, and give the
limit at infinity.

<details class="dl-answer"><summary>answer</summary>

```python
for cups in [10, 100, 1000, 10000, 1000000]:
    print(cups, (300 + 0.5 * cups) / cups)
```

€30.50, €3.50, €0.80, €0.53, €0.5003. The limit at infinity is €0.50.
The rule is $\frac{300}{n} + 0.5$, and $\frac{300}{n}$ heads for 0
as $n$ grows, like $\frac{1}{x}$ did. The cost of the machine gets
shared among more and more cups, but each cup always needs its own
beans and milk.

</details>

**8. Another way.** Find $\lim_{x \to 2} \frac{x^2 + x - 6}{x - 2}$
two ways: with a table, and by writing the top as two brackets.

<details class="dl-answer"><summary>answer</summary>

```python
def six_hole(x):
    return (x ** 2 + x - 6) / (x - 2)

approach(six_hole, 2, rows=6)
```

The columns head for 5 from both sides: 4.0, 4.5, 4.75, and 6.0, 5.5,
5.25. By algebra, $x^2 + x - 6 = (x - 2)(x + 3)$: the two numbers
multiply to $-6$ and add to 1. Away from 2, the rule is $x + 3$, and
$2 + 3 = 5$. The two routes agree. The algebra gives the exact answer;
the table checks that the algebra has no slip in it.

</details>

**9. Make.** A patient takes 100 mg of a medicine each morning. By the
next morning, the body has removed half of what was there. So each
morning, the amount is half of yesterday's, plus 100. Start from 0,
and print the amount after each of the first 10 doses. What limit does
the sequence head for? (These numbers are made up, and are not advice
about any real medicine.)

<details class="dl-answer"><summary>answer</summary>

```python
level = 0
for dose in range(1, 11):
    level = level / 2 + 100
    print(dose, level)
```

100, 150, 175, 187.5, and after 10 doses 199.8046875. The limit is
200 mg. Check it: if the level were exactly 200, then half of it plus
100 is 200 again, so it would stay there. The gap to 200 halves each
day, like the walk to the door.

</details>

**10. Predict.** Python's `round` rounds a number to the nearest whole
number. What happens near 2.5? Predict both columns, and
`round(2.5)`, before you run it.

```python
approach(round, 2.5, rows=5)
print(round(2.5), round(3.5))
```

<details class="dl-answer"><summary>answer</summary>

The first row is `1 2 4`, since 1.5 rounds to 2 and 3.5 to 4. After
that, the left column is always 2 and the right column always 3. So the
one-sided limits are 2 from the left and 3 from the right, and `round`
has no limit at 2.5.

The last line prints `2 4`, which surprises most people. Exactly
halfway, Python rounds to the even neighbour, so 2.5 goes down to 2
and 3.5 goes up to 4. This is called banker's rounding. The value at
2.5 is a rule someone chose, and the limit would not tell you which.

</details>

**11. Another way.** On
[Doubling and halving](tutorial:doubling-and-halving#how-long-to-double),
savings grew by 4% a year. If the bank paid $\frac{4}{n}$% $n$ times a
year, a euro would end the year at $(1 + \frac{0.04}{n})^n$. Find the
limit with a table. Then compare it with `math.e ** 0.04`.

<details class="dl-answer"><summary>answer</summary>

```python
for times in [1, 12, 365, 1000000]:
    print(times, (1 + 0.04 / times) ** times)
print(math.e ** 0.04)
```

1.04, then 1.040742, 1.040808, and 1.0408108 at a million. The last
line is 1.0408108 as well. So paying 4% all the time gives
$e^{0.04}$, a little over 4.08% in a year. The same limit that made $e$
from 100% makes $e^{0.04}$ from 4%. That is why $e$ turns up wherever
growth happens all the time.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: getting-closer-practice-stretch
# Your working for problems 12 to 15
```

**12. Explain.** Here is a table for $\sin\left(\frac{\pi}{x}\right)$
near 0. Every value is tiny, so it looks like the limit is 0. Then the
second loop tries a few other points near 0. What went wrong, and does
the rule have a limit at 0?

```python
def sine_of_pi_over_x(x):
    return math.sin(math.pi / x)

approach(sine_of_pi_over_x, 0, rows=6)
for x in [0.3, 0.03, 0.003, 0.0003]:
    print(x, sine_of_pi_over_x(x))
```

<details class="dl-answer"><summary>answer</summary>

`approach` only tries steps of 1, $\frac{1}{2}$, $\frac{1}{4}$, and so
on. At $x = \frac{1}{2^k}$, the rule is $\sin(2^k \pi)$, and the sine
of a whole number of half turns is 0. So every row is 0, apart from
float noise like `1e-16`. The table only looked at points where the
rule happens to be 0.

At 0.3, 0.03, 0.003 and 0.0003 the rule is about $-0.866$. Close to 0,
$\frac{\pi}{x}$ is huge and changes very fast, so the sine swings
between $-1$ and 1 over and over, however close we get. The values
never settle, so there is no limit. A table is evidence, not proof,
and a table that only looks at special points can be fooled.

</details>

**13. Predict.** The tutorial's bank broke at $n = 10^{16}$. Here is
the same rule at powers of 2. Predict each line, and say why powers of
2 last longer than powers of 10.

```python
for k in [20, 40, 52, 53]:
    n = 2 ** k
    print(k, (1 + 1 / n) ** n)
```

<details class="dl-answer"><summary>answer</summary>

2.7182805, 2.71828182845781, then 2.718281828459045, which is `math.e`
to every digit Python shows, and then 1.0.

A float is a binary fraction, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#why-01-02-is-not-03).
$\frac{1}{2^{52}}$ is a binary fraction with a single 1 in it, so
$1 + \frac{1}{2^{52}}$ is kept exactly, with no rounding at all. But
$\frac{1}{10^{15}}$ has no exact binary form, so it is rounded, and
the power makes the rounding error large. At $2^{53}$, the step is
half the gap between floats near 1, and $1 + \frac{1}{2^{53}}$ is kept
as 1.

The same thing happens in problem 5 with `rows=40`: from row 28 on,
$\cos x$ is so close to 1 that it is kept as exactly 1, and the rule
gives 0.0.

</details>

**14. Make.** A made-up income tax takes 20% of the first €40,000 of
income, and 40% of every euro above that. Write `tax(income)` and
`rate(income)`, where `rate` is the percentage taken from the next
euro. Use `approach` on both at €40,000. Which one has a limit there?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Up to €40,000, the tax is `0.2 * income`.
2. Above it, the tax is 8,000 for the first €40,000, plus
   `0.4 * (income - 40000)`.
3. `rate` gives back 0.2 up to €40,000 and 0.4 above.

**Think about:** when someone earns one euro more than €40,000, how
much more tax do they pay?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def tax(income):
    if income <= 40000:
        return 0.2 * income
    return 8000 + 0.4 * (income - 40000)

def rate(income):
    if income <= 40000:
        return 0.2
    return 0.4

approach(tax, 40000, rows=4)
approach(rate, 40000, rows=4)
```

The tax heads for €8,000 from both sides, 7,999.80 and 8,000.40 on the
first row, and closer after. So the tax has a limit at €40,000, and it
is the value there: there is no jump in what people pay. The rate jumps
from 0.2 to 0.4, so it has two different one-sided limits and no limit.
This is why earning a little more never leaves you with less money in
this system: only the euros above the line are taxed at the higher
rate.

</details>

**15. Make.** The rule $x^x$ has no value at $x = 0$ in Python's
floats, and for negative $x$ it gives complex numbers, as on
[When there is no real answer](tutorial:when-there-is-no-real-answer).
Try `(-0.5) ** (-0.5)` to see one. So only the right-hand side makes
sense here. Write `approach_from_right(rule, a, rows=10)`, which prints
only the right column, and use it to find the one-sided limit of $x^x$
as $x \to 0^+$.

<details class="dl-answer"><summary>answer</summary>

```python
def approach_from_right(rule, a, rows=10):
    """Print rule just right of a, halving the step on each row."""
    step = 1
    for row in range(rows):
        print(step, rule(a + step))
        step = step / 2

def x_to_the_x(x):
    return x ** x

print((-0.5) ** (-0.5))
approach_from_right(x_to_the_x, 0)
print(x_to_the_x(1e-6))
```

`(-0.5) ** (-0.5)` gives a complex number, about $-1.414i$. From the
right, the values are 1, 0.707, 0.707, 0.771, 0.841, and then they
climb: 0.988 after ten rows, and 0.99999 at $x = 10^{-6}$. So
$\lim_{x \to 0^+} x^x = 1$. The values first go down and then come
back up. A limit only cares where they end up, not the path they take.

</details>
