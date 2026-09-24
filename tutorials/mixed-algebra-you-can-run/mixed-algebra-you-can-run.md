---
title: "Mixed problems: algebra you can run"
practice_across:
  - rules-with-letters-in-them
  - drawing-a-rule
  - solving-for-x
  - when-there-is-no-real-answer
  - the-top-of-the-curve
  - several-unknowns-at-once
year: "2026-2027"
version: 2026.09.24.1
---

# Mixed problems: algebra you can run

Each problem here draws on at least one page of Unit 7, and many draw on
two or more. None of them is harder than what those pages covered. The
new part is that nobody tells you which page a problem comes from.
Choosing the tool is part of the problem.

Along the way, the problems build this unit's product in two parts: a
phone-plan chooser, which finds where two plans cost the same and the
cheapest plan for your data, and a price finder for a small bakery.
Every answer is checked by putting it back into its rule, in code.
Problems 4, 6, 8 and 9 build the chooser, and 11, 12 and 14 the price
finder. Each builds on the one before, so do those in order.

Your toolkit is loaded on this page: `evaluate`, `plot_rule`,
`solve_linear`, `solve_quadratic`, `vertex` and `solve_simultaneous`
from this unit, and every tool from Units 1 to 6, such as
`close_enough` and `largest`. Each answer is hidden until you open it.
Where a problem asks you to predict, make the prediction before you run
anything. It is the most useful part.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: mixed-run-scratch-1
# Try things here
```

**1. Predict.** What does each line print? Work each one out by hand
first.

```python
print(evaluate([5, 0, -1], 3))
print(solve_linear(4, -10))
print(solve_quadratic(1, 0, -9))
print(vertex(1, -4, 1))
```

<details class="dl-answer"><summary>answer</summary>

`-4`, `2.5`, `[-3.0, 3.0]` and `(2.0, -3.0)`.

`[5, 0, -1]` is $5 - x^2$, lowest power first, and $5 - 9 = -4$.
$4x - 10 = 0$ gives $x = \frac{10}{4}$. $x^2 - 9 = 0$ has two roots,
smallest first. The vertex of $x^2 - 4x + 1$ is at
$x = -\frac{-4}{2} = 2$, where the rule is $4 - 8 + 1 = -3$.

</details>

**2. Make.** A bike-share scheme charges €10 a year, plus 50 cent a
ride. (The prices are made up.) You have €40 to spend this year. How
many rides is that? Write the equation, tidy it into the shape
$ax + b = 0$, solve it with `solve_linear`, and put the answer back in.

<details class="dl-answer"><summary>answer</summary>

With $r$ rides, the equation is $10 + 0.5r = 40$. Subtract 40 from both
sides: $0.5r - 30 = 0$, so $a = 0.5$ and $b = -30$.

```python
rides = solve_linear(0.5, -30)
print(rides)
print(evaluate([10, 0.5], rides))
```

It prints `60.0`, and 60 rides cost `40.0`. The rule $10 + 0.5r$ is the
list `[10, 0.5]`, so `evaluate` does the substituting.

</details>

**3. Explain.** On a frosty night in Mullingar, a weather app models the
temperature $t$ hours after midnight as $0.1t^2 - 1.2t + 2$ degrees
Celsius, from midnight to noon. (A made-up model.) A friend says: "The
coldest moment is where the graph crosses zero." Run this cell. What do
the two answers mean, and when is the coldest moment?

```python
print(solve_quadratic(0.1, -1.2, 2))
print(vertex(0.1, -1.2, 2))
```

<details class="dl-answer"><summary>answer</summary>

The first line gives the roots, `[2.0, 10.0]`. The second gives the
vertex, $(6, -1.6)$, printed with a tiny float error in the last
digits.

A root is a time when the temperature is exactly 0 °C: 2 am and
10 am. The vertex is where
the curve turns, as on
[The top of the curve](tutorial:the-top-of-the-curve#a-curve-that-turns).
Its $t^2$ term is positive, so the vertex is a minimum: the coldest
moment is 6 am, at −1.6 °C. The friend has mixed up the two. The mirror
joins them: 6 is halfway between 2 and 10.

</details>

## Core

The core problems build the phone-plan chooser. A phone company offers
three plans. Each costs a fixed amount a month, plus a price for each
gigabyte of data. (The prices are made up.)

| Plan | Each month | Each gigabyte |
|---|---|---|
| Basic | €8 | €3 |
| Flex | €15 | €1.25 |
| Unlimited | €30 | €0 |

Each plan's cost is a linear rule, so this cell keeps each one as a
list of coefficients, lowest power first, as on
[Rules with letters in them](tutorial:rules-with-letters-in-them#terms-coefficients-and-a-list).
Run it first.

```python exec
id: mixed-run-plans
plans = {
    "Basic": [8, 3],
    "Flex": [15, 1.25],
    "Unlimited": [30, 0],
}
print(evaluate(plans["Basic"], 2))
```

It prints `14`: two gigabytes on Basic cost €14. Keep the chooser's
functions in the scratch cell below as you write them, so that later
problems can use them.

```python exec
id: mixed-run-scratch-2
# Your phone-plan chooser, problem by problem
```

**4. Make.** The chooser's first job is a table. Write a loop that
prints what each plan costs at 0, 4, 8, 12 and 16 gigabytes a month,
one row for each amount. Which plan would you choose at each amount?

<details class="dl-answer"><summary>answer</summary>

```python
for gigabytes in [0, 4, 8, 12, 16]:
    row = [gigabytes]
    for name in plans:
        row.append(evaluate(plans[name], gigabytes))
    print(row)
```

```text
[0, 8, 15.0, 30]
[4, 20, 20.0, 30]
[8, 32, 25.0, 30]
[12, 44, 30.0, 30]
[16, 56, 35.0, 30]
```

Basic wins at 0 GB, Flex at 8 GB and Unlimited at 16 GB, with ties at
4 and 12 GB. The table shows the ties only because its rows land on
them.

</details>

**5. Predict.** Here are the three plans as a picture, drawn with
`plot_rule` from
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet).
How many times will two lines cross? Guess where, before you run it.

```python exec
id: mixed-run-plans-picture
import matplotlib.pyplot as plt

def basic(gigabytes):
    return evaluate(plans["Basic"], gigabytes)

def flex(gigabytes):
    return evaluate(plans["Flex"], gigabytes)

def unlimited(gigabytes):
    return evaluate(plans["Unlimited"], gigabytes)

plot_rule(basic, 0, 16)
plot_rule(flex, 0, 16)
plot_rule(unlimited, 0, 16)
plt.xlabel("gigabytes a month")
plt.ylabel("euro a month")
plt.legend()
```

<details class="dl-answer"><summary>answer</summary>

There are three crossings, one for each pair: Basic and Flex at 4 GB, Basic and
Unlimited at a little over 7 GB, and Flex and Unlimited at 12 GB.

Only two of them matter to a customer. The cheapest plan is the lowest
line: Basic up to 4 GB, Flex from 4 to 12 GB, and Unlimited after that.
Basic and Unlimited cross above the Flex line, where neither is
cheapest.

</details>

**6. Make.** Two plans cost the same where the difference of their
rules is 0. Write two functions:

- `subtract_polynomials(first, second)`, which gives back the list for
  `first` minus `second`, with like terms collected;
- `break_even(first, second)`, which gives back the gigabytes where two
  plans cost the same, using `solve_linear`, or `None` when there is no
  single answer.

Then find all three crossings exactly, and put each one back into both
plans.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `subtract_polynomials` has the shape of `add_polynomials` on
   [Rules with letters in them](tutorial:rules-with-letters-in-them#collecting-like-terms),
   with one `+` changed to `-`.
2. Basic minus Flex is $(8 + 3g) - (15 + 1.25g) = -7 + 1.75g$, the list
   `[-7, 1.75]`.
3. `solve_linear(a, b)` solves $ax + b = 0$. Which place in the list is
   $a$, and which is $b$?

**Think about:** what should `break_even` give back for two plans with
the same price per gigabyte?

**Try this next:** find where Basic and Flex meet with
`solve_simultaneous`, taking $g$ and the cost $y$ as the two unknowns:
$-3g + y = 8$ and $-1.25g + y = 15$.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def subtract_polynomials(first, second):
    """Return the coefficients of first - second, with like terms collected."""
    difference = [0] * max(len(first), len(second))
    for power in range(len(first)):
        difference[power] = difference[power] + first[power]
    for power in range(len(second)):
        difference[power] = difference[power] - second[power]
    return difference


def break_even(first, second):
    """Return the gigabytes where two plans [fee, per gigabyte] cost the same.

    Return None when there is no single answer.
    """
    difference = subtract_polynomials(first, second)
    return solve_linear(difference[1], difference[0])


for one, other in [("Basic", "Flex"), ("Basic", "Unlimited"), ("Flex", "Unlimited")]:
    gigabytes = break_even(plans[one], plans[other])
    first_cost = evaluate(plans[one], gigabytes)
    second_cost = evaluate(plans[other], gigabytes)
    assert close_enough(first_cost, second_cost), (one, other)
    print(one, other, round(gigabytes, 2), round(first_cost, 2))
```

```text
Basic Flex 4.0 20.0
Basic Unlimited 7.33 30.0
Flex Unlimited 12.0 30.0
```

Every crossing passes the check. The list is lowest power first, so the
number in front of $g$ is `difference[1]`. Basic meets Unlimited at
$7\frac{1}{3}$ GB, a float, so the check uses `close_enough`.

The simultaneous route from the hint is one line:

```python
print(solve_simultaneous(-3, 1, 8, -1.25, 1, 15))
```

It gives `(4.0, 20.0)`: the same 4 GB, and the cost there too. Taking one of its facts from the other cancels
$y$ and leaves $-1.75g = -7$, the same equation `break_even` solves.

</details>

**7. Fix.** Someone's first `break_even` gives an answer, but the check
after it fails. Run it, and read the message. Find the mistake, and fix
it.

```python exec
id: mixed-run-fix-order
def break_even_first_try(first, second):
    """Return the gigabytes where two plans [fee, per gigabyte] cost the same."""
    difference = [first[0] - second[0], first[1] - second[1]]
    return solve_linear(difference[0], difference[1])


gigabytes = break_even_first_try([8, 3], [15, 1.25])
print(gigabytes)
assert close_enough(evaluate([8, 3], gigabytes), evaluate([15, 1.25], gigabytes)), "the plans should cost the same here"
print("Basic and Flex cost the same at", gigabytes, "GB.")
```

<details class="dl-answer"><summary>answer</summary>

It prints `0.25`, and then stops with
`AssertionError: the plans should cost the same here`. At 0.25 GB,
Basic costs €8.75 and Flex about €15.31.

The difference is `[-7, 1.75]`, which is $-7 + 1.75g$. The call passes
$-7$ as $a$ and $1.75$ as $b$, so it solves $-7g + 1.75 = 0$, a
different equation. The fix swaps them:

```python
def break_even_first_try(first, second):
    """Return the gigabytes where two plans [fee, per gigabyte] cost the same."""
    difference = [first[0] - second[0], first[1] - second[1]]
    return solve_linear(difference[1], difference[0])
```

Now it prints `4.0`, and the check passes. A coefficient list puts the
constant first, and $ax + b$ puts it last. Without the substitution
check, 0.25 GB would have looked like a believable answer.

</details>

**8. Make.** The chooser's main tool. Write
`cheapest_plan(plans, gigabytes)`, which gives back the name of the
cheapest plan for that much data. Test it at 2, 8 and 20 GB, and print
what the winning plan costs each time.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep two names: the best plan so far, and its cost. Start both at
   `None`.
2. Loop over the names in `plans`, and work out each plan's cost with
   `evaluate`.
3. If there is no best plan yet, or this plan costs less, it becomes the
   best plan.

**Think about:** at exactly 4 GB, Basic and Flex tie. Which one will
your function give back, and why?

**Try this next:** give back the name and the cost together, as a pair.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def cheapest_plan(plans, gigabytes):
    """Return the name of the plan that costs least for this many gigabytes."""
    best_name = None
    best_cost = None
    for name in plans:
        cost = evaluate(plans[name], gigabytes)
        if best_cost is None or cost < best_cost:
            best_name = name
            best_cost = cost
    return best_name


assert cheapest_plan(plans, 2) == "Basic"
assert cheapest_plan(plans, 8) == "Flex"
assert cheapest_plan(plans, 20) == "Unlimited"
for gigabytes in [2, 8, 20]:
    name = cheapest_plan(plans, gigabytes)
    print(gigabytes, name, evaluate(plans[name], gigabytes))
```

```text
2 Basic 14
8 Flex 25.0
20 Unlimited 30
```

At exactly 4 GB it gives back Basic: a plan that only ties is not
`<`, so it does not replace the plan found first. Either is a right
answer there.

</details>

**9. Make.** Your old phone plan had a monthly fee and a price per
gigabyte, and you have lost the leaflet. In March you used 3 GB and
paid €17.50. In April you used 7 GB and paid €27.50. Find the fee and the price per gigabyte with
`solve_simultaneous`, and check both bills. Then add the old plan to
`plans` as `"Old"`. Is it ever the cheapest?

<details class="dl-answer"><summary>answer</summary>

Call the fee $f$ and the price per gigabyte $p$. The bills are two
facts: $f + 3p = 17.50$ and $f + 7p = 27.50$.

```python
fee, per_gigabyte = solve_simultaneous(1, 3, 17.50, 1, 7, 27.50)
print(fee, per_gigabyte)
print(fee + 3 * per_gigabyte, fee + 7 * per_gigabyte)

plans["Old"] = [fee, per_gigabyte]
for gigabytes in [0, 2, 4, 6, 10, 20]:
    print(gigabytes, cheapest_plan(plans, gigabytes))
```

The old plan was €10 a month plus €2.50 a gigabyte, and both bills
check out: `17.5 27.5`. By elimination: 4 GB more cost €10 more, so a
gigabyte costs €2.50.

The old plan never wins. It beats Basic above 4 GB and Flex below 4 GB,
and at 4 GB all three cost €20: their lines cross at one point,
$(4, 20)$.

</details>

**10. Explain.** The company adds Flex Plus: €20 a month and €1.25 a
gigabyte, with free calls abroad. What does
`break_even(plans["Flex"], [20, 1.25])` give back? What would its line
look like beside Flex on a graph, and what does that mean for someone
choosing between them?

<details class="dl-answer"><summary>answer</summary>

It gives back `None`. The difference is `[-5, 0]`, which is $-5 + 0g$,
and no $g$ makes $-5 = 0$.

The two lines have the same steepness, so they are parallel and never
cross, like the two fans' facts on
[Several unknowns at once](tutorial:several-unknowns-at-once#when-there-is-no-single-answer).
Flex Plus always costs €5 more than Flex, so the data never changes the
choice. The question is whether free calls abroad are worth €5 a month
to you. The algebra puts a price on that question. It cannot answer it.

</details>

## Stretch

The stretch problems build the price finder. A small bakery sells
sourdough loaves, and each loaf costs €1.40 to make. At a price of $p$
euro, it sells about $260 - 40p$ loaves a day. (A made-up model: a
higher price means fewer sales.) The profit is the profit on one loaf,
times the number sold:

$$\text{profit} = (p - 1.4)(260 - 40p)$$

Here is a scratch cell for the stretch problems.

```python exec
id: mixed-run-scratch-3
# Your price finder, problem by problem
```

**11. Make.** Multiply out the brackets with a loop, as
`expand_brackets` did on
[Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop).
Write it again here, from memory if you can, and get the profit as a
list of coefficients. Then check the list against the brackets, at
every price from €1.40 to €6.50 in steps of 10 cent.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $p - 1.4$ is the list `[-1.4, 1]`, and $260 - 40p$ is `[260, -40]`.
2. The expanded list's length is `len(first) + len(second) - 1`.
3. A term at index `i` times a term at index `j` goes to index `i + j`.

**Think about:** why does the check need `close_enough`, and not `==`?

**Try this next:** find the list for a loaf that costs €2 to make.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def expand_brackets(first, second):
    """Return the coefficients of first times second, with the brackets multiplied out."""
    expanded = [0] * (len(first) + len(second) - 1)
    for i in range(len(first)):
        for j in range(len(second)):
            expanded[i + j] = expanded[i + j] + first[i] * second[j]
    return expanded


profit_rule = expand_brackets([-1.4, 1], [260, -40])
print(profit_rule)

for cents in range(140, 651, 10):
    price = cents / 100
    assert close_enough(evaluate(profit_rule, price), (price - 1.4) * (260 - 40 * price))
print("The expanded rule agrees with the brackets.")
```

The list is `[-364.0, 316.0, -40]`, so the profit is
$-40p^2 + 316p - 364$. By hand, the grid of four pieces gives
$260p - 40p^2 - 364 + 56p$, and the two $p$ terms collect to $316p$.
The check passes at all 52 prices. It needs `close_enough` because 1.4
is a float, and two routes to a float can differ in the last digit.

</details>

**12. Make.** Find the best price with `vertex`, and the profit there.
Then check it with a fine comb, as on
[The top of the curve](tutorial:the-top-of-the-curve#checking-with-a-fine-comb):
try every price from €1.40 to €6.50, one cent apart, and find the
largest profit.

<details class="dl-answer"><summary>answer</summary>

```python
best_price, best_profit = vertex(-40, 316, -364)
print(best_price, round(best_profit, 2))

prices = []
profits = []
for cents in range(140, 651):
    prices.append(cents / 100)
    profits.append(evaluate(profit_rule, cents / 100))

top = largest(profits)
print(prices[profits.index(top)], round(top, 2))
```

Both lines give €3.95 and a profit of €260.10 a day. The vertex is at
$p = -\frac{316}{2 \times (-40)} = 3.95$, and the $p^2$ term is
negative, so it is a maximum. The comb tried 511 prices, and none beats
it.

</details>

**13. Another way.** Find the best price with `solve_quadratic` and no
vertex formula. Where is the profit 0? What does each of those prices
mean for the bakery?

<details class="dl-answer"><summary>answer</summary>

```python
roots = solve_quadratic(-40, 316, -364)
print(roots)
print((roots[0] + roots[1]) / 2)
```

The roots are €1.40, where a loaf sells for what it costs to make, and
€6.50, where the bakery sells none. Each is where one bracket of
$(p - 1.4)(260 - 40p)$ is 0. The parabola's mirror puts its top halfway
between them, at €3.95, as on
[The top of the curve](tutorial:the-top-of-the-curve#halfway-between-the-roots).

</details>

**14. Predict.** Which prices make at least €200 a day? Which price
makes €300? Each target gives an equation: the profit, minus the target,
equals 0. Before you run the cell, say how many real roots each has.
Then compare the real part of the complex roots with problem 12.

```python
import cmath

def solve_quadratic_complex(a, b, c):
    """Return both roots of a*x**2 + b*x + c = 0 as complex numbers."""
    root = cmath.sqrt(b ** 2 - 4 * a * c)
    return [(-b - root) / (2 * a), (-b + root) / (2 * a)]

print(solve_quadratic(-40, 316, -364 - 200))
print(solve_quadratic(-40, 316, -364 - 300))
print(solve_quadratic_complex(-40, 316, -364 - 300))
```

<details class="dl-answer"><summary>answer</summary>

€200 has two real roots, about €2.72 and €5.18, and any price between
them makes at least €200. Put each root back in, and the profit is €200:

```python
for price in solve_quadratic(-40, 316, -564):
    print(round(price, 2), round(evaluate(profit_rule, price), 2))
```

€300 has none, and `solve_quadratic` gives back `[]`. The most the
bakery can make is €260.10, so no real price reaches €300. The
discriminant agrees: $316^2 - 4 \times (-40) \times (-664) = -6384$.

The complex roots are about $3.95 + 0.999i$ and $3.95 - 0.999i$.
Their real part is 3.95, the best price, and that is no accident. The
formula is $-\frac{b}{2a}$, plus or minus a square root over $2a$, and
$-\frac{b}{2a}$ is the vertex. When the discriminant is negative, only
the plus-or-minus part turns imaginary.

A price is a real amount of money, so the owner's question lives in
$\mathbb{R}$, and the honest answer is "no price reaches €300". The
complex roots are true roots in $\mathbb{C}$, as on
[When there is no real answer](tutorial:when-there-is-no-real-answer#every-quadratic-has-roots-here),
but nobody can charge them.

</details>

**15. Fix.** Someone tries the fine comb with prices one cent apart,
and the cell stops with an error. Read its last line, find the mistake,
and fix it.

```python exec
id: mixed-run-fix-comb
best_so_far = 0
for price in range(1.40, 6.50, 0.01):
    profit_here = (price - 1.4) * (260 - 40 * price)
    if profit_here > best_so_far:
        best_so_far = profit_here
        best_price_so_far = price
print(best_price_so_far, best_so_far)
```

<details class="dl-answer"><summary>answer</summary>

The error is `TypeError: 'float' object cannot be interpreted as an
integer`. `range` works in the space of whole numbers: its start, stop
and step must all be ints. The fix counts in whole cents, and turns each
count into euro inside the loop. The stop is 651, because `range` stops
before its last number:

```python
best_so_far = 0
for cents in range(140, 651):
    price = cents / 100
    profit_here = (price - 1.4) * (260 - 40 * price)
    if profit_here > best_so_far:
        best_so_far = profit_here
        best_price_so_far = price
print(best_price_so_far, round(best_so_far, 2))
```

It prints `3.95 260.1`, the answer from problem 12. Counting in cents
also avoids adding 0.01 again and again, which would build up a small
float error at every step.

</details>

**16. Explain.** Every answer on this page was checked by putting it
back into the rule it came from, and every check passed. Does that mean
the bakery should charge €3.95? What does a substitution check prove,
and what can it not prove?

<details class="dl-answer"><summary>answer</summary>

A substitution check proves that an answer fits its rule, so the
algebra and the code made no mistake. It caught the swapped argument in
problem 7 at once.

It cannot prove that the rule fits the world. The bakery's rule is a
guess. If customers really buy $300 - 60p$ loaves, every check still
passes, and €3.95 is the wrong price. The step from the world to the
rule needs other evidence, such as the bakery's own sales at a few
prices, like Aoife's notes on
[The top of the curve](tutorial:the-top-of-the-curve#a-price-too-low-a-price-too-high).

The phone plans are different: their rules come from the price list,
so they are exact. A good answer names both steps: the answer fits the
rule, and here is why we trust the rule.

</details>
