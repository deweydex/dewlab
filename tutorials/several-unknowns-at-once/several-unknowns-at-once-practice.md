---
title: "Several unknowns at once: simultaneous equations — Practice"
practice_for: several-unknowns-at-once
year: "2026-2027"
version: 2026.09.24.1
---

# Several unknowns at once: simultaneous equations — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `solve_simultaneous`
from the tutorial, `solve_linear` from
[Solving for x](tutorial:solving-for-x) and `plot_rule` from
[Drawing a rule](tutorial:drawing-a-rule).

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: several-unknowns-practice-warm-up
# Try things here
```

**1. Predict.** Two numbers add up to 10, and the first is 4 more than
the second. So $x + y = 10$ and $x - y = 4$. What does this line print?

```python
print(solve_simultaneous(1, 1, 10, 1, -1, 4))
```

<details class="dl-answer"><summary>answer</summary>

`(7.0, 3.0)`. Check: $7 + 3 = 10$, and $7 - 3 = 4$.

Adding the two equations eliminates $y$ at once: $2x = 14$, so $x = 7$.
The determinant is $1 \times (-1) - 1 \times 1 = -2$, which is not 0,
so there is one answer.

</details>

**2. Predict.** What does this line print, and why?

```python
print(solve_simultaneous(2, 3, 5, 4, 6, 10))
```

<details class="dl-answer"><summary>answer</summary>

`None`. The determinant is $2 \times 6 - 4 \times 3 = 0$.

The second equation, $4x + 6y = 10$, is the first, $2x + 3y = 5$, with
everything doubled. It is the same fact said twice, so the two lines
are one line. Every point on it is an answer, which means there is no
single answer.

</details>

**3. Make.** Is $x = 4$, $y = -1$ the solution of $2x + y = 7$ and
$x - 3y = 7$? Check by substituting, in code.

<details class="dl-answer"><summary>answer</summary>

```python
x, y = 4, -1
print(2 * x + y == 7, x - 3 * y == 7)
```

Both print `True`: $8 - 1 = 7$ and $4 + 3 = 7$. So yes, it is the
solution. It must be the only one, because the determinant,
$2 \times (-3) - 1 \times 1 = -7$, is not 0.

</details>

**4. Explain.** A café sold 12 drinks, some tea and some coffee. That is
one fact, $t + c = 12$. How many answers does it have if the counts are
whole numbers? And if $t$ and $c$ could be any real numbers? What does a
second fact do?

<details class="dl-answer"><summary>answer</summary>

With whole numbers from 0 up, there are 13 answers: 0 teas and 12
coffees, 1 and 11, and so on up to 12 and 0. With any real numbers,
there are endless answers: every point on the line $c = 12 - t$.

A second fact that is not the same fact again draws a second line. Two
lines that are not parallel cross at exactly one point, and that point
is the one answer.

</details>

## Core

A cell for the core problems.

```python exec
id: several-unknowns-practice-core
# Your working for problems 5 to 11
```

**5. Make.** A breakfast bowl has 250 g of oats and yoghurt, and 29.5 g
of protein. Oats have about 13 g of protein in each 100 g, and this
yoghurt has 10 g in each 100 g. How many grams of each are in the bowl?
Write the two facts as equations, solve with `solve_simultaneous`, and
substitute back.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Name the unknowns: $x$ grams of oats and $y$ grams of yoghurt.
2. The weight: $x + y = 250$.
3. The protein: each gram of oats has 0.13 g, and each gram of yoghurt
   0.10 g. So $0.13x + 0.10y = 29.5$.
4. The six numbers, in the order `solve_simultaneous` wants, are
   `1, 1, 250, 0.13, 0.10, 29.5`.

**Think about:** the answers are floats. How should you check them?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
oats, yoghurt = solve_simultaneous(1, 1, 250, 0.13, 0.10, 29.5)
print(round(oats, 2), round(yoghurt, 2))
print(close_enough(oats + yoghurt, 250), close_enough(0.13 * oats + 0.10 * yoghurt, 29.5))
```

150 g of oats and 100 g of yoghurt, and both checks print `True`. The
numbers like 0.13 are floats, so the answer may come back a tiny way
from 150, and `close_enough` is the right test.

</details>

**6. Make.** Two bus fares and a train fare cost €8.30. One bus fare
and three train fares cost €12.40. (The fares are made up.) Find each
fare by elimination, by hand, in the four steps from the tutorial.
Then check with `solve_simultaneous`.

<details class="dl-answer"><summary>answer</summary>

Call the bus fare $b$ and the train fare $t$:

$$2b + t = 8.30$$
$$b + 3t = 12.40$$

Step 1: multiply the second equation by 2, so $b$ has 2 in front of it
in both: $2b + 6t = 24.80$. Step 2: take the first equation away from
it: $5t = 16.50$. Step 3: $t = 3.30$. Step 4: put it back into the
first equation: $2b + 3.30 = 8.30$, so $2b = 5$ and $b = 2.50$.

```python
fares = solve_simultaneous(2, 1, 8.30, 1, 3, 12.40)
print(fares)
print(round(fares[0], 2), round(fares[1], 2))
```

A bus fare is €2.50 and a train fare €3.30. The first line may show a
float a tiny way off, such as `2.5000000000000004`; rounding to cent
shows the fares.

</details>

**7. Fix.** Here is someone's version of `solve_simultaneous`. The
first test passes, and the second stops with an error. Run it, read the
error, and fix the function.

```python exec
id: several-unknowns-practice-fix
def solve_pair(a1, b1, c1, a2, b2, c2):
    """Return (x, y) where a1x + b1y = c1 and a2x + b2y = c2, or None if there is no single answer."""
    determinant = a1 * b2 - a2 * b1
    x = (c1 * b2 - c2 * b1) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    if determinant == 0:
        return None
    return (x, y)

assert solve_pair(1, 1, 230, 12, 5, 2060) == (130, 100)
assert solve_pair(3, 2, 80, 6, 4, 150) is None
print("solve_pair keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line of the error. Which operation failed?
2. Which line of `solve_pair` does that operation, and what is
   `determinant` when it runs?
3. The check for 0 is there. When does Python reach it?

**Think about:** what happens when, in this function? Which line must
come first?

</details>

<details class="dl-answer"><summary>answer</summary>

The error is `ZeroDivisionError: division by zero`, on the line that
works out `x`. For the fans' T-shirts the determinant is 0, and the
function divides by it before it checks. The check is right, and it
comes too late. Move it up, straight after the determinant:

```python
def solve_pair(a1, b1, c1, a2, b2, c2):
    """Return (x, y) where a1x + b1y = c1 and a2x + b2y = c2, or None if there is no single answer."""
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None
    x = (c1 * b2 - c2 * b1) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    return (x, y)

assert solve_pair(1, 1, 230, 12, 5, 2060) == (130, 100)
assert solve_pair(3, 2, 80, 6, 4, 150) is None
print("solve_pair keeps its promise.")
```

Now both tests pass. The same lines, in a different order, keep the
promise: that is sequence.

</details>

**8. Predict.** Before you run this, what will the picture show, and
what will the last line print?

```python
import matplotlib.pyplot as plt

def first_line(x):
    return 2 * x + 1

def second_line(x):
    return 2 * x - 3

plot_rule(first_line, -3, 3)
plot_rule(second_line, -3, 3)
plt.legend()
print(solve_simultaneous(-2, 1, 1, -2, 1, -3))
```

<details class="dl-answer"><summary>answer</summary>

Two parallel lines, 4 apart, and `None`.

Both lines climb 2 for every 1 across, so they have the same
steepness, and they never meet. To use `solve_simultaneous`, each rule
$y = 2x + 1$ was moved into the shape $a x + b y = c$: $-2x + y = 1$,
and $-2x + y = -3$. The determinant is
$(-2) \times 1 - (-2) \times 1 = 0$.

</details>

**9. Another way.** Solve the concert question from the tutorial by
*substitution* instead of elimination. From $a + c = 230$, write
$a = 230 - c$, and put that in place of $a$ in $12a + 5c = 2060$. That
leaves one equation in $c$. Tidy it into the shape $mc + k = 0$ and
finish with `solve_linear`.

<details class="dl-answer"><summary>answer</summary>

$12(230 - c) + 5c = 2060$, so $2760 - 12c + 5c = 2060$, which is
$2760 - 7c = 2060$. Taking 2060 from both sides gives $-7c + 700 = 0$.

```python
children = solve_linear(-7, 700)
adults = 230 - children
print(adults, children)
print(adults + children == 230, 12 * adults + 5 * children == 2060)
```

130 adults and 100 children, as before, and both checks print `True`.
Substitution turns two unknowns into one, and the toolkit already had a
tool for one.

</details>

**10. Explain.** In elimination, we multiplied $a + c = 230$ by 5 to get
$5a + 5c = 1150$. Why does that not change the answer? Would its line on
a graph change?

<details class="dl-answer"><summary>answer</summary>

Any pair that makes $a + c = 230$ true also makes $5a + 5c = 1150$ true,
because both sides were multiplied by the same number. It works the
other way too: dividing both sides by 5 brings the first equation back.
So the two equations are true for exactly the same pairs. They are the
same fact, written two ways, and they draw the same line.

Multiplying both sides by 0 would be different: $0 = 0$ is true for
every pair, so that move throws the fact away.

</details>

**11. Make.** On [Solving for x](tutorial:solving-for-x) one phone plan
cost €20 a month, and another cost €8 plus 6 cent a minute. Write the
two plans as simultaneous equations in $m$ (minutes) and $y$ (the cost
in euro), and solve them with `solve_simultaneous`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first plan: $y = 20$. With no $m$ in it, that is $0m + 1y = 20$.
2. The second plan: $y = 8 + 0.06m$. Move the $m$ term to the left:
   $-0.06m + 1y = 8$.
3. The six numbers are `0, 1, 20, -0.06, 1, 8`.

**Think about:** what does the answer's second number, $y$, mean?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
minutes, cost = solve_simultaneous(0, 1, 20, -0.06, 1, 8)
print(round(minutes, 6), cost)
print(close_enough(8 + 0.06 * minutes, 20))
```

200 minutes, at a cost of €20. That is the answer `solve_linear` found
on that page, and the crossing of the two lines. Here the second number
is the cost where the plans meet, which the one-unknown version did not
give us.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: several-unknowns-practice-stretch
import numpy as np
# Your working for problems 12 to 14
```

**12. Make.** In rugby union, a try is worth 5 points, a conversion 2
and a penalty 3. A team scored 35 points from 10 scores, and converted
every try but one. How many tries, conversions and penalties did it
score? Eliminate one unknown by hand, then let `solve_simultaneous`
finish.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Name them $t$, $c$ and $p$. The three facts are $t + c + p = 10$,
   $5t + 2c + 3p = 35$ and $c = t - 1$.
2. Put $t - 1$ in place of $c$ in the first two facts. Collect like
   terms.
3. You now have two equations in $t$ and $p$.

**Think about:** the third fact was already in the shape "$c$ equals
something". Which method, substitution or elimination, suits it?

</details>

<details class="dl-answer"><summary>answer</summary>

Putting $c = t - 1$ into the first fact: $t + t - 1 + p = 10$, so
$2t + p = 11$. Into the second: $5t + 2t - 2 + 3p = 35$, so
$7t + 3p = 37$.

```python
tries, penalties = solve_simultaneous(2, 1, 11, 7, 3, 37)
conversions = tries - 1
print(tries, conversions, penalties)
print(tries + conversions + penalties, 5 * tries + 2 * conversions + 3 * penalties)
```

4 tries, 3 conversions and 3 penalties: 10 scores and 35 points.

</details>

**13. Another way.** Check your rugby answer with `np.linalg.solve`.
Write each fact with all three unknowns in it, in the same order, $t$,
$c$, $p$, using 0 where an unknown is missing.

<details class="dl-answer"><summary>answer</summary>

The third fact, $c = t - 1$, becomes $t - c + 0p = 1$.

```python
rows = [[1, 1, 1], [5, 2, 3], [1, -1, 0]]
totals = [10, 35, 1]
print(np.linalg.solve(rows, totals))
```

It prints `[4. 3. 3.]`, the same answer.

</details>

**14. Predict.** These two lines are *nearly* parallel. The only
difference between the two calls is the very last number, which moves
by 0.0001. How far do you think the answer moves?

```python
print(solve_simultaneous(1, 1, 2, 1, 1.0001, 2.0001))
print(solve_simultaneous(1, 1, 2, 1, 1.0001, 2.0002))
```

<details class="dl-answer"><summary>answer</summary>

The first gives very nearly $(1, 1)$, and the second gives $(0, 2)$.
The first answer's last digits are a little off, because 1.0001 is a
float. A change of 0.0001 in one fact moved the answer by a whole 1 in
each unknown.

The determinant is $1 \times 1.0001 - 1 \times 1 = 0.0001$, very close
to 0. Dividing by a very small number makes every small change huge.
Two lines that are nearly parallel cross at a point that is very
sensitive: tilt one line a little and the crossing slides a long way.
So when the determinant is close to 0, an answer built from measured
numbers deserves less trust.

</details>
