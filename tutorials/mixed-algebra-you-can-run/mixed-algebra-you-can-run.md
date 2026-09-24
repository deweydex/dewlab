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

Along the way, the problems build this unit's product in two parts. The
first is a phone-plan chooser: it finds where two plans cost the same,
and the cheapest plan for the data you use. The second is a price finder
for a small bakery: the price that makes the most profit. The rule of
this unit holds for both. Every answer is checked by putting it back
into the rule it came from, in code. Problems 5, 7, 9 and 10 build the
chooser, and problems 13, 14 and 16 build the price finder. Each part
builds on the one before, so do those in order.

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

- `[5, 0, -1]` is $5 - x^2$, lowest power first. At 3 it is
  $5 - 9 = -4$.
- `solve_linear(4, -10)` solves $4x - 10 = 0$. Add 10 to both sides, then
  divide by 4: $x = 2.5$.
- $x^2 - 9 = 0$ has two roots, $-3$ and 3, smallest first. They are
  floats because the formula divides.
- The vertex of $x^2 - 4x + 1$ is at $x = -\frac{-4}{2 \times 1} = 2$,
  and the rule there is $4 - 8 + 1 = -3$. The $x^2$ term is positive, so
  it is a minimum.

</details>

**2. Make.** A bike-share scheme charges €10 a year, plus 50 cent a
ride. (The prices are made up.) You have €40 to spend this year. How
many rides is that? Write the equation, tidy it into the shape
$ax + b = 0$, solve it with `solve_linear`, and put the answer back in.

<details class="dl-answer"><summary>answer</summary>

With $r$ rides, the year costs $10 + 0.5r$, so the equation is
$10 + 0.5r = 40$. Subtract 40 from both sides: $0.5r - 30 = 0$. So
$a = 0.5$ and $b = -30$.

```python
rides = solve_linear(0.5, -30)
print(rides)
print(evaluate([10, 0.5], rides))
```

It prints `60.0`, and the year's cost at 60 rides is `40.0`. The rule
$10 + 0.5r$ is the list `[10, 0.5]`, so `evaluate` does the
substituting.

</details>

**3. Explain.** On a frosty night in Mullingar, a weather app models the
temperature $t$ hours after midnight as $0.1t^2 - 1.2t + 2$ degrees
Celsius, from midnight to noon. (A made-up model.) A friend says: "The
coldest moment is where the graph crosses zero." Run this cell. What do
the two answers mean, and which one is the coldest moment?

```python
print(solve_quadratic(0.1, -1.2, 2))
print(vertex(0.1, -1.2, 2))
```

<details class="dl-answer"><summary>answer</summary>

The first line gives the roots, `[2.0, 10.0]`. The second gives the
vertex, $(6, -1.6)$, printed with a tiny float error in the last
digits.

A root is a time when the temperature is exactly 0 °C: at about 2 am it
drops below freezing, and at about 10 am it climbs back above. The
vertex is the turning point of the curve. Its $t^2$ term is positive, so
it is a minimum: the coldest moment is 6 am, at −1.6 °C.

So the friend has mixed up two different points. Crossing zero is where
the value is 0, as on
[Drawing a rule](tutorial:drawing-a-rule#a-tool-that-draws-any-rule).
The coldest moment is where the curve turns, as on
[The top of the curve](tutorial:the-top-of-the-curve#a-curve-that-turns).
The mirror joins them: 6 is halfway between 2 and 10.

</details>

**4. Predict.** A music festival sold 5,000 tickets: day tickets at €60
and weekend tickets at €90. It took €360,000. Before you run the line
below, guess: were more than half of the tickets day tickets? Then run
it, and put the answer back into both facts.

```python
print(solve_simultaneous(1, 1, 5000, 60, 90, 360000))
```

<details class="dl-answer"><summary>answer</summary>

`(3000.0, 2000.0)`: 3,000 day tickets and 2,000 weekend tickets, so yes,
more than half.

A quick way to guess: if all 5,000 were day tickets, the takings would
be €300,000. Each weekend ticket adds €30 more, and €60,000 more is
2,000 weekend tickets. Now the check, in both facts:

```python
day, weekend = solve_simultaneous(1, 1, 5000, 60, 90, 360000)
print(day + weekend, 60 * day + 90 * weekend)
```

It prints `5000.0 360000.0`. Checking both facts matters: one fact on
its own has thousands of answers, as on
[Several unknowns at once](tutorial:several-unknowns-at-once#two-facts-two-unknowns).

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

Each plan's cost is a linear rule, so each is a list of coefficients,
lowest power first, as on
[Rules with letters in them](tutorial:rules-with-letters-in-them#terms-coefficients-and-a-list).
Unlimited keeps its 0 in place, so every list has two numbers. This cell
keeps the three plans in a dictionary, keyed by name. Run it first.

```python exec
id: mixed-run-plans
plans = {
    "Basic": [8, 3],
    "Flex": [15, 1.25],
    "Unlimited": [30, 0],
}
print(evaluate(plans["Basic"], 2))
```

It prints `14`: two gigabytes on Basic cost €14. A scratch cell for the
core problems. Keep the chooser's functions in it as you write them, so
that later problems can use them.

```python exec
id: mixed-run-scratch-2
# Your phone-plan chooser, problem by problem
```

**5. Make.** The chooser's first job is a table. Write a loop that
prints what each plan costs at 0, 4, 8, 12 and 16 gigabytes a month, one
row for each amount. From the table, which plan would you choose at each
amount?

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

Basic is cheapest at 0 GB. At 4 GB, Basic and Flex tie on €20. At 8 GB
Flex wins, at 12 GB Flex and Unlimited tie on €30, and at 16 GB
Unlimited wins. The table shows two ties, but only because we chose
rows that land on them. With other rows, a table can only say "somewhere
between".

</details>

**6. Predict.** Now a picture of all three plans, drawn with
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

Three crossings, one for each pair of plans: Basic and Flex at 4 GB,
Basic and Unlimited at a bit more than 7 GB, and Flex and Unlimited at
12 GB.

Only two of them matter to a customer. The cheapest plan at each amount
is the lowest line there. Basic is lowest up to 4 GB, Flex from 4 to 12
GB, and Unlimited after 12 GB. The Basic and Unlimited crossing happens
above the Flex line, where neither of them is the cheapest.

The picture says "a bit more than 7". The next problem finds each
crossing exactly.

</details>

**7. Make.** Two plans cost the same where the difference of their
rules is 0. Write two functions:

- `subtract_polynomials(first, second)`, which gives back the list for
  `first` minus `second`, with like terms collected;
- `break_even(first, second)`, which gives back the gigabytes where two
  linear plans cost the same, using `solve_linear`, or `None` when there
  is no single answer.

Then find all three crossings, and put each one back into both plans.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `subtract_polynomials` has the shape of `add_polynomials` on
   [Rules with letters in them](tutorial:rules-with-letters-in-them#collecting-like-terms),
   with one `+` changed to `-`.
2. The difference of Basic and Flex is $(8 + 3g) - (15 + 1.25g)$, which
   is $-7 + 1.75g$, the list `[-7, 1.75]`.
3. `solve_linear(a, b)` wants $ax + b = 0$. Which place in the list is
   $a$, and which is $b$?

**Think about:** what should `break_even` give back for two plans with
the same price per gigabyte?

**Try this next:** add a fourth plan, and find where it meets each of
the other three.

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
number in front of $g$ is `difference[1]`, and the constant is
`difference[0]`. The Basic and Unlimited crossing is at $7\frac{1}{3}$
GB: $8 + 3g = 30$ gives $3g = 22$. `round` keeps the print short, and
`close_enough` does the checking, because $7\frac{1}{3}$ is a float
with a tiny error.

</details>

**8. Fix.** Someone's first `break_even` gives an answer, but the check
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
Basic costs €8.75 and Flex costs about €15.31.

The difference is `[-7, 1.75]`, lowest power first: $-7 + 1.75g$. The
call `solve_linear(difference[0], difference[1])` passes $-7$ as $a$ and
$1.75$ as $b$, so it solves $-7g + 1.75 = 0$, a different equation.
The fix swaps them:

```python
def break_even_first_try(first, second):
    """Return the gigabytes where two plans [fee, per gigabyte] cost the same."""
    difference = [first[0] - second[0], first[1] - second[1]]
    return solve_linear(difference[1], difference[0])
```

Now it prints `4.0`, and the check passes. Two conventions met here:
coefficient lists put the constant first, and $ax + b$ puts it last.
The substitution check caught the mix-up at once. Without it, 0.25 GB
would have looked like a believable answer.

</details>

**9. Make.** The chooser's main tool. Write
`cheapest_plan(plans, gigabytes)`, which gives back the name of the
cheapest plan for that much data. Test it at 2, 8 and 20 GB, and print
what the winning plan costs each time.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep two names: the best plan so far, and its cost. Start with no
   plan and a cost of `None`.
2. Loop over the names in `plans`. Work out each plan's cost with
   `evaluate`.
3. If there is no best plan yet, or this plan costs less, it becomes the
   best plan.

**Think about:** at exactly 4 GB, Basic and Flex tie. Which one will your
function give back, and why?

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

At exactly 4 GB it gives back Basic. The test is `cost < best_cost`, so
a plan that only ties does not replace the plan found first, and Basic
comes first in the dictionary. A tie is a real answer here: either plan
is cheapest.

</details>

**10. Make.** Your old phone plan had a fixed monthly fee and a price
per gigabyte, but you have lost the leaflet. You still have two bills.
In March you used 3 GB and paid €17.50. In April you used 7 GB and paid
€27.50. Find the fee and the price per gigabyte with
`solve_simultaneous`, and check both bills. Then add the old plan to
`plans` as `"Old"`. Is it ever the cheapest?

<details class="dl-answer"><summary>answer</summary>

Call the fee $f$ and the price per gigabyte $p$. The two bills are two
facts:

$$f + 3p = 17.50$$
$$f + 7p = 27.50$$

```python
fee, per_gigabyte = solve_simultaneous(1, 3, 17.50, 1, 7, 27.50)
print(fee, per_gigabyte)
print(fee + 3 * per_gigabyte, fee + 7 * per_gigabyte)

plans["Old"] = [fee, per_gigabyte]
for gigabytes in [0, 2, 4, 6, 10, 20]:
    print(gigabytes, cheapest_plan(plans, gigabytes))
```

The old plan was €10 a month plus €2.50 a gigabyte, and both bills
check out: `17.5 27.5`. Taking one bill from the other shows why:
4 GB more cost €10 more, so each gigabyte costs €2.50.

The old plan never wins. It is cheaper than Basic above 4 GB, and
cheaper than Flex below 4 GB, and at 4 GB all three cost €20. Draw it
with the others, and the three lines cross at one point, $(4, 20)$. So
there is no amount of data where the old plan beats both. Unless you
like it for another reason, switching costs you nothing.

</details>

**11. Explain.** The company adds a fifth plan, Flex Plus: €20 a month
and €1.25 a gigabyte, with free calls abroad. What does
`break_even(plans["Flex"], [20, 1.25])` give back? What would its line
look like beside Flex on a graph, and what does that mean for someone
choosing between the two?

<details class="dl-answer"><summary>answer</summary>

It gives back `None`. The difference is `[-5, 0]`, which is $-5 + 0g$,
and `solve_linear(0, -5)` has no single answer: no $g$ makes
$-5 = 0$.

The two lines have the same steepness, so they are parallel, and they
never cross. Flex Plus always costs €5 a month more than Flex, however
much data you use. That is the same case as the two fans on
[Several unknowns at once](tutorial:several-unknowns-at-once#when-there-is-no-single-answer),
where the determinant was 0.

So there is no amount of data where the choice changes. The question
for the customer is a different one: are free calls abroad worth €5 a
month to you? The algebra can say the price of that question. It cannot
answer it.

</details>

**12. Another way.** Find where Basic and Flex cost the same a second
way, with `solve_simultaneous`. Call the gigabytes $g$ and the monthly
cost $y$, so each plan is one fact about $g$ and $y$. Do the two ways
agree?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Basic says $y = 8 + 3g$. Move the $g$ term across: $-3g + y = 8$.
2. Do the same for Flex.
3. In `solve_simultaneous(a1, b1, c1, a2, b2, c2)`, the unknowns are
   in the order $g$, then $y$.

**Think about:** what does the second number of the answer mean?

**Try this next:** do the same for Flex and Unlimited.

</details>

<details class="dl-answer"><summary>answer</summary>

Basic is $-3g + y = 8$, and Flex is $-1.25g + y = 15$.

```python
print(solve_simultaneous(-3, 1, 8, -1.25, 1, 15))
print(break_even(plans["Basic"], plans["Flex"]))
```

The first line gives `(4.0, 20.0)`: 4 GB, at €20. The second gives
`4.0`. They agree, and the simultaneous route gives the cost as well.

The two routes are one idea. `break_even` took one rule from the other
to get one equation in one unknown. Elimination on
[Several unknowns at once](tutorial:several-unknowns-at-once#elimination-one-unknown-at-a-time)
does the same: taking one fact from the other cancels $y$, and leaves
$-1.75g = -7$.

</details>

## Stretch

The stretch problems build the price finder. A small bakery sells
sourdough loaves. Each loaf costs €1.40 to make. At a price of $p$ euro,
it sells about $260 - 40p$ loaves a day. (A made-up model, with the
shape real sellers see: a higher price means fewer sales.) The profit is
the profit on one loaf, times the number sold:

$$\text{profit} = (p - 1.4)(260 - 40p)$$

A scratch cell for the stretch problems.

```python exec
id: mixed-run-scratch-3
# Your price finder, problem by problem
```

**13. Make.** Multiply out the brackets with a loop, as
`expand_brackets` did on
[Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop).
Write it again here, from memory if you can, and use it to get the
profit as a list of coefficients. Then check the list against the
brackets, by substituting every price from €1.40 to €6.50 in steps of 10
cent.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $p - 1.4$ is the list `[-1.4, 1]`, and $260 - 40p$ is `[260, -40]`.
2. The expanded list has room for every power: its length is
   `len(first) + len(second) - 1`.
3. A term at index `i` times a term at index `j` goes to index `i + j`.

**Think about:** why does the check need `close_enough`, and not `==`?

**Try this next:** what happens to the list if each loaf costs €2 to
make?

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

The list is `[-364.0, 316.0, -40]`: the profit is
$-40p^2 + 316p - 364$. By hand, the grid of four pieces gives
$260p - 40p^2 - 364 + 56p$, and collecting the two $p$ terms gives
$316p$. The check passes at all 52 prices. It uses `close_enough`
because 1.4 is a float, and the two routes can differ in the last digit.

</details>

**14. Make.** Find the best price with `vertex`, and the profit there.
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

Both lines give a price of €3.95 and a profit of €260.10 a day. The
vertex is at $p = -\frac{316}{2 \times (-40)} = 3.95$. The $p^2$ term is
negative, so the parabola opens downwards, and the vertex is a maximum.
The comb tried 511 prices, and none beats it. At €3.95 the bakery sells
$260 - 158 = 102$ loaves, and makes €2.55 on each.

</details>

**15. Another way.** Find the best price a third way, with
`solve_quadratic` and no vertex formula. Where is the profit 0? What
does each of those prices mean for the bakery?

<details class="dl-answer"><summary>answer</summary>

```python
roots = solve_quadratic(-40, 316, -364)
print(roots)
print((roots[0] + roots[1]) / 2)
```

The roots are €1.40 and €6.50, and halfway between them is €3.95. At
€1.40 each loaf sells for what it costs to make, so the bakery makes
nothing on each one. At €6.50 it sells no loaves at all: $260 - 40
\times 6.5 = 0$. A parabola is a mirror image of itself, so its top is
halfway between the two roots, as on
[The top of the curve](tutorial:the-top-of-the-curve#halfway-between-the-roots).
The roots could be read straight off the brackets too, since each
bracket is 0 at one of them.

</details>

**16. Predict.** The owner asks two more questions. Which prices give a
profit of at least €200 a day? And which price gives €300 a day? Each
target makes a quadratic equation: profit minus the target equals 0.
Before you run the cell, say how many real roots each one will have.
Then look at the complex roots of the second, and compare their real
part with your answer to problem 14.

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

€200 has two real roots, about €2.72 and €5.18. Any price between them
makes at least €200 a day. Put each root back in, and the profit is
€200:

```python
for price in solve_quadratic(-40, 316, -564):
    print(round(price, 2), round(evaluate(profit_rule, price), 2))
```

€300 has none: `solve_quadratic` gives back `[]`. The most the bakery
can make is €260.10, from problem 14, so no real price reaches €300. The
discriminant says the same: $316^2 - 4 \times (-40) \times (-664)$ is
$-6384$.

The complex roots are about $3.95 + 0.999i$ and $3.95 - 0.999i$, a
pair of conjugates. Their real part is 3.95, the best price. That is no accident. The formula is
$-\frac{b}{2a}$, plus or minus a square root over $2a$, and
$-\frac{b}{2a}$ is the vertex. When the discriminant is negative, the
plus-or-minus part is imaginary, and the real part is left pointing at
the top of the curve.

So which space answers the owner? A price is a real amount of money, so
the question lives in $\mathbb{R}$, and the honest answer is "no price
reaches €300". The complex roots are true roots in $\mathbb{C}$, as on
[When there is no real answer](tutorial:when-there-is-no-real-answer#every-quadratic-has-roots-here).
They are not prices anyone can charge.

</details>

**17. Fix.** Someone tries the fine comb with prices one cent apart.
The cell stops before it prints anything. Read the last line of the
error, find the mistake, and fix it.

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
integer`. `range` counts in whole numbers only: its start, stop and
step must all be ints. Nothing is wrong with the idea, only with the
space `range` works in.

The fix counts in whole cents, and turns each count into euro inside
the loop. The stop is 651, because `range` stops before its last
number:

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

It prints `3.95 260.1`, the answer from problem 14. Counting in cents
has a second benefit: `cents / 100` gives each price once, fresh. Adding
0.01 again and again would build up a small float error with each step.

</details>

**18. Explain.** Every answer on this page was checked by putting it
back into the rule it came from. The chooser and the price finder pass
every check. Does that mean the bakery should charge €3.95? What does a
substitution check prove, and what can it not prove?

<details class="dl-answer"><summary>answer</summary>

A substitution check proves that the answer fits the rule. If $3.95$ goes
into $-40p^2 + 316p - 364$ and the vertex is right, the algebra and the
code made no mistake. It catches a swapped argument, as in problem 8, or
a lost term, at once.

It cannot prove that the rule fits the world. The bakery's rule came
from a guess: about $260 - 40p$ loaves a day. If customers really buy
$300 - 60p$, every check still passes, and €3.95 is still the wrong
price. The check is about the second step, from rule to answer. The
first step, from the world to the rule, needs other evidence: the
bakery's own sales at a few prices, as Aoife's notes were on
[The top of the curve](tutorial:the-top-of-the-curve#a-price-too-low-a-price-too-high).

The same holds for the phone plans, with one difference. Their rules
come from the company's price list, so the rule is exact, and the
checks say nearly everything. A good answer names both steps: the
answer fits the rule, and here is why we trust the rule.

</details>
