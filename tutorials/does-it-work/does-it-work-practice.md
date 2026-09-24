---
title: "Does it work? Testing, walkthroughs and naming — Practice"
practice_for: does-it-work
year: "2026-2027"
version: 2026.09.24.1
---

# Does it work? Testing, walkthroughs and naming — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `close_enough`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: does-it-practice-warm-up
# Try things here
```

**1. Predict.** What does each line print?

```python
print(close_enough(0.1 + 0.2, 0.3))
print(close_enough(9.99, 10))
print(close_enough(9.99, 10, tolerance=0.05))
print(close_enough(2, 2))
```

<details class="dl-answer"><summary>answer</summary>

`True`, `False`, `True`, `True`.

`0.1 + 0.2` is off from 0.3 by far less than a billionth. 9.99 and 10
are 0.01 apart, which is more than the default tolerance, but less than
0.05. And two equal numbers are 0 apart, which is never more than any
tolerance.

</details>

**2. Make.** A cinema app shows film lengths in hours. Write three test
cases, with `assert`, for this function: one from a fact you know, one
at an edge, and one that uses a second route.

```python
def minutes_to_hours(minutes):
    """Return a length of time in hours, given it in minutes."""
    return minutes / 60
```

<details class="dl-answer"><summary>answer</summary>

One possible set:

```python
def minutes_to_hours(minutes):
    """Return a length of time in hours, given it in minutes."""
    return minutes / 60

assert minutes_to_hours(90) == 1.5, "a 90-minute film is an hour and a half"
assert minutes_to_hours(0) == 0, "no minutes is no hours"
assert close_enough(minutes_to_hours(137) * 60, 137), "back to minutes again"
print("minutes_to_hours keeps its promise.")
```

It prints `minutes_to_hours keeps its promise.` The first test comes from
a fact, the second sits at the edge, and the third goes there and back.
Yours may use other values and still be good tests.

</details>

**3. Explain.** A friend says: "My function ran, and there was no error,
so it works." What would you say to them? Give an example from this
unit.

<details class="dl-answer"><summary>answer</summary>

Python only reports an error when it cannot make a move, such as
dividing by zero or using a name that points at nothing. It has no idea
what the function was meant to do. So a function can run with no error
and still break its promise. The tutorial's `oven_celsius` ran, and said
350 °F was about 332 °C. Only a test case, such as "32 °F should give
0 °C", showed that it was wrong.

</details>

**4. Predict.** A fitness app adds up three days of steps. Make a trace
table with the columns `day_steps` and `steps`, one row for each time
round the loop, and use it to predict what the cell prints. Then run it.

```python
steps = 0
for day_steps in [4000, 6500, 3000]:
    steps = steps + day_steps
print(steps)
```

<details class="dl-answer"><summary>answer</summary>

| After loop number | `day_steps` | `steps` |
|---|---|---|
| (before the loop) | | 0 |
| 1 | 4000 | 4000 |
| 2 | 6500 | 10500 |
| 3 | 3000 | 13500 |

It prints `13500`. Each time round, `steps` grows by that day's steps.

</details>

## Core

A cell for the core problems.

```python exec
id: does-it-practice-core
# Your working for problems 5 to 12
```

**5. Predict.** €100 is saved at 10% interest a year. How many years
until it is €150 or more? Make a trace table with the columns `years`
and `balance` before you run the cell. (Round the balance to the cent in
your table.)

```python
balance = 100
years = 0
while balance < 150:
    balance = balance * 1.1
    years = years + 1
print(years, round(balance, 2))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start the table with `years` 0 and `balance` 100.
2. Each row: check `balance < 150`. If it is true, multiply the balance
   by 1.1 and add 1 to `years`.
3. Stop at the first row where the check is false.

**Think about:** why the loop runs once more after 146.41, even though
that is so close to 150.

</details>

<details class="dl-answer"><summary>answer</summary>

| `years` | `balance` | `balance < 150`? |
|---|---|---|
| 0 | 100.00 | True |
| 1 | 110.00 | True |
| 2 | 121.00 | True |
| 3 | 133.10 | True |
| 4 | 146.41 | True |
| 5 | 161.05 | False, so the loop stops |

It prints `5 161.05`. 146.41 is still less than 150, so the loop runs
once more.

</details>

**6. Fix.** Here is someone's `close_enough`, with its tests. Run it,
read which test fails, and fix the function.

```python exec
id: does-it-practice-fix-close
def close_enough_again(a, b, tolerance=1e-9):
    """Return True when a and b differ by no more than tolerance."""
    return a - b <= tolerance

assert close_enough_again(0.1 + 0.2, 0.3), "very close"
assert not close_enough_again(5, 1), "far apart"
assert not close_enough_again(1, 5), "far apart, the other way round"
print("All tests pass.")
```

<details class="dl-answer"><summary>answer</summary>

The third test fails with `AssertionError: far apart, the other way
round`. `1 - 5` is −4, and −4 is smaller than any tolerance, so the
function says 1 and 5 are close. The distance between two numbers
needs `abs()`:

```python
def close_enough_again(a, b, tolerance=1e-9):
    """Return True when a and b differ by no more than tolerance."""
    return abs(a - b) <= tolerance
```

Now all three pass. Testing only `(5, 1)` would have missed this bug.

</details>

**7. Fix.** A restaurant adds a 10% tip to every bill. The test fails.
Run it, then decide: is the mistake in the code, the comment or the
docstring? Fix it.

```python exec
id: does-it-practice-fix-tip
def price_with_tip(bill):
    """Return the bill with a 10% tip added."""
    return bill * 1.15    # add the 10% tip

assert close_enough(price_with_tip(100), 110), "€100 plus 10% is €110"
print("price_with_tip keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The restaurant's rule is 10%, and the docstring and the comment both say
10%. The code multiplies by 1.15, which adds 15%. So the code is wrong:

```python
def price_with_tip(bill):
    """Return the bill with a 10% tip added."""
    return bill * 1.10
```

The comment can go: it says what the code says. Notice the test uses
`close_enough`. `100 * 1.10` is `110.00000000000001`, so `==` would fail
even with the right code.

</details>

**8. Make.** A running app shows distances in kilometres or in miles.
One mile is exactly 1.609344 km. Write `km_to_miles` and `miles_to_km`.
Test them with a fact (a marathon is 42.195 km, about 26.2 miles), and
with a loop that goes there and back for every whole number of km from 0
to 1,000.

<details class="dl-answer"><summary>answer</summary>

```python
def km_to_miles(km):
    """Return a distance in miles, given it in kilometres."""
    return km / 1.609344


def miles_to_km(miles):
    """Return a distance in kilometres, given it in miles. Undoes km_to_miles."""
    return miles * 1.609344


assert close_enough(km_to_miles(42.195), 26.2, tolerance=0.05), "a marathon is about 26.2 miles"
for km in range(0, 1001):
    assert close_enough(miles_to_km(km_to_miles(km)), km), km
print("The distance converter works both ways.")
```

It prints `The distance converter works both ways.` The marathon test
needs a wider tolerance, because 26.2 is itself rounded: the exact value
is about 26.219. The round trip uses the default tolerance, and `==`
would have failed on 41 km, among others.

</details>

**9. Explain.** A recipe app has a function to double the amounts. It has
a bug, but its test passes. Why does the test pass? Write a better test.

```python
def double(amount):
    """Return twice amount."""
    return amount * amount

assert double(2) == 4
```

<details class="dl-answer"><summary>answer</summary>

For 2, doubling and squaring give the same answer: $2 + 2 = 4$ and
$2 \times 2 = 4$. So the test cannot tell the right function from the
wrong one. A test case is only useful if a likely mistake would give a
different answer. `assert double(3) == 6` fails for this function, since
$3 \times 3 = 9$, and that catches the bug. Good test values avoid 0, 1
and 2, where many different rules happen to agree.

</details>

**10. Make.** This function from a concert ticket site works, but nobody
can tell what it does. Give it and its names words, add a docstring,
and test that your version gives the same answers as the old one for
three different sets of values.

```python
def calc(x, y, z):
    t = x * y
    return t - t * z / 100
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try `calc(40, 3, 10)`. What could 40, 3 and 10 be on a ticket site?
2. `t` is `x` times `y`. What is a ticket price times a number of
   tickets?
3. The last line takes away `z` per cent of `t`.

**Think about:** which names would let a stranger guess what the
function does without running it?

</details>

<details class="dl-answer"><summary>answer</summary>

`x` is a ticket price, `y` is how many tickets, and `z` is a discount in
per cent.

```python
def calc(x, y, z):
    t = x * y
    return t - t * z / 100


def price_after_discount(ticket_price, tickets, discount_percent):
    """Return the cost of tickets at ticket_price each, with discount_percent taken off."""
    full_price = ticket_price * tickets
    return full_price - full_price * discount_percent / 100


for values in [(40, 3, 10), (25.5, 2, 0), (60, 10, 15)]:
    assert price_after_discount(*values) == calc(*values)
print("The two versions agree.")
print(price_after_discount(40, 3, 10))
```

It prints `The two versions agree.`, then `108.0`. Three tickets at €40,
with 10% off, cost €108. Writing `*values` hands the three numbers in a
row to the function as its three inputs, the same way `*row` did on
[Untangling a condition](tutorial:untangling-a-condition).

</details>

**11. Another way.** Python has its own tool for this job,
`math.isclose(a, b)`. Run both tools on the pairs below. On which pairs
do they disagree? The first number in the third pair is the distance to
the Moon, in metres.

```python
import math

pairs = [(0.1 + 0.2, 0.3), (1, 1.001), (384400000.0, 384400000.1), (0.000000001, 0.000000002)]
for a, b in pairs:
    print(a, b, close_enough(a, b), math.isclose(a, b))
```

<details class="dl-answer"><summary>answer</summary>

```text
0.30000000000000004 0.3 True True
1 1.001 False False
384400000.0 384400000.1 False True
1e-09 2e-09 True False
```

They agree on the first two pairs and disagree on the last two.
`close_enough` asks whether two numbers are within a fixed distance, a
billionth. `math.isclose` asks whether they are within a billionth *of
their size*. For the Moon, 0.1 m out of 384 million metres is tiny
compared with the size, so `math.isclose` says True. For two numbers
that are both about a billionth, one is double the other, so
`math.isclose` says False. Each tool is right in its own space: a fixed
tolerance suits numbers of an everyday size, like temperatures and
prices.

</details>

**12. Fix.** A weather app counts the days with any rain at all. Five
days in Galway had 0, 2.5, 0, 4.1 and 0.2 mm of rain, so the answer
should be 3. Make a trace table to find the bug, then fix it.

```python exec
id: does-it-practice-fix-rain
def rainy_days(rainfall):
    """Return how many days in rainfall had more than 0 mm of rain."""
    for amount in rainfall:
        count = 0
        if amount > 0:
            count = count + 1
    return count

print(rainy_days([0, 2.5, 0, 4.1, 0.2]))
assert rainy_days([0, 2.5, 0, 4.1, 0.2]) == 3, "three days had rain"
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Make a table with the columns `amount` and `count`.
2. Write a row each time a line changes `count`.
3. Look at what happens to `count` at the start of each time round the
   loop.

**Think about:** which lines should run once, and which should run once
for every day?

</details>

<details class="dl-answer"><summary>answer</summary>

The cell prints `1`, and then the test fails.

| `amount` | `count` after `count = 0` | `count` after the `if` |
|---|---|---|
| 0 | 0 | 0 |
| 2.5 | 0 | 1 |
| 0 | 0 | 0 |
| 4.1 | 0 | 1 |
| 0.2 | 0 | 1 |

`count = 0` is inside the loop, so the count starts again at 0 every
day. Only the last day is counted. The start belongs before the loop,
where it runs once:

```python
def rainy_days(rainfall):
    """Return how many days in rainfall had more than 0 mm of rain."""
    count = 0
    for amount in rainfall:
        if amount > 0:
            count = count + 1
    return count
```

Now it gives 3. This is a sequence bug: the right lines, with one of
them in the wrong place.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: does-it-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** The unit converter this unit is building has many pairs
of functions that should undo each other. Write
`works_both_ways(forwards, backwards, values)`, which gives back `True`
when `backwards(forwards(value))` is close enough to `value` for every
value in `values`, and `False` otherwise. Test it on the temperature
tools, on the travel tools, and on a pair that does not undo each other.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over `values`.
2. For each one, go there and back, and compare with `close_enough`.
3. If any value fails, give back `False` straight away. If the loop
   finishes, give back `True`.

**Think about:** `travel_time` and `distance_travelled` take two inputs.
How could you make a one-input function from each, for a fixed speed?

**Try this next:** make `works_both_ways` say which value failed.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def works_both_ways(forwards, backwards, values):
    """Return True when backwards undoes forwards, within close_enough, for every value."""
    for value in values:
        if not close_enough(backwards(forwards(value)), value):
            return False
    return True


def km_at_80(hours):
    """Return the km covered in hours at 80 km/h."""
    return distance_travelled(80, hours)


def hours_at_80(km):
    """Return the hours to cover km at 80 km/h."""
    return travel_time(km, 80)


temperatures = range(-50, 101)
print(works_both_ways(celsius_to_fahrenheit, fahrenheit_to_celsius, temperatures))
print(works_both_ways(km_at_80, hours_at_80, [0.5, 1, 2.75, 10]))
print(works_both_ways(celsius_to_fahrenheit, celsius_to_fahrenheit, temperatures))
```

This prints `True`, `True`, `False`. Converting to Fahrenheit twice does
not bring a temperature back, and the tool catches it.

</details>

**14. Explain.** `close_enough` uses a tolerance of a billionth. Two
lab results are 0.000000001 grams and 0.000000002 grams, and
`close_enough` says they are equal. A GPS says two points are
384,400,000.0 and 384,400,000.1 metres from a satellite, and
`close_enough` says they are not equal. Is `close_enough` wrong? When
would you change its tolerance?

<details class="dl-answer"><summary>answer</summary>

`close_enough` keeps its promise both times: the first pair differs by
less than a billionth, and the second by 0.1, which is more. The
trouble is the tolerance, not the function. A billionth is far too big
for numbers that are themselves about a billionth, since one lab result
is double the other. It is far too small for distances to a satellite,
where 0.1 m hardly matters. The tolerance should fit the size of the
numbers and how exact they need to be. For grams in a lab, try
`tolerance=1e-15`. For a GPS distance, 0.5 m might be close enough.
Problem 11 shows `math.isclose`, which scales its tolerance to the size
of the numbers.

</details>

**15. Fix.** A bus company charges nothing for children under 5, €1 for
ages 5 to 17, and €2 for anyone 18 or over. Write test cases at every
edge of that promise, run them, and fix the bug they find.

```python exec
id: does-it-practice-fix-fare
def fare(age):
    """Return the bus fare in euro: free under 5, €1 from 5 to 17, €2 from 18."""
    if age < 5:
        return 0
    elif age < 17:
        return 1
    else:
        return 2

# Your test cases here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The promise changes at 5 and at 18. Those are the edges.
2. Test the age just before each edge, and the edge itself: 4, 5, 17 and
   18.
3. Which one gives the wrong fare?

**Think about:** "5 to 17" includes 17. Which sign includes it?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
assert fare(4) == 0, "4 is under 5"
assert fare(5) == 1, "5 is the first child fare"
assert fare(17) == 1, "17 is the last child fare"
assert fare(18) == 2, "18 is the first adult fare"
print("fare keeps its promise.")
```

The test for 17 fails: `17 < 17` is False, so a 17-year-old pays the
adult fare. Either of these fixes it:

```python
def fare(age):
    """Return the bus fare in euro: free under 5, €1 from 5 to 17, €2 from 18."""
    if age < 5:
        return 0
    elif age < 18:
        return 1
    else:
        return 2
```

or `elif between(age, 5, 17):`, with the toolkit's `between`. A test in
the middle, like age 10, would never have found this bug. Bugs like this
one live at the edges, so the edges are where tests go.

</details>
