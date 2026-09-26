---
title: "Does it work? Testing, walkthroughs and naming — Practice"
practice_for: does-it-work
year: "2026-2027"
version: 2026.09.25.2
---

# Does it work? Testing, walkthroughs and naming — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another
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

It prints `True`, `False`, `True`, `True`.

`0.1 + 0.2` is off from 0.3 by far less than a billionth. 9.99 and 10
are 0.01 apart, which is more than the default tolerance, but less than
0.05. And two equal numbers are 0 apart, which is never more than any
tolerance.

</details>

**2. Make.** A video player shows how long a video is, in hours. Write three test
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

assert minutes_to_hours(90) == 1.5, "a 90-minute video is an hour and a half"
assert minutes_to_hours(0) == 0, "no minutes is no hours"
assert close_enough(minutes_to_hours(137) * 60, 137), "back to minutes again"
print("minutes_to_hours keeps its promise.")
```

It prints `minutes_to_hours keeps its promise.` The first test comes from
a fact, the second sits at the edge, and the third goes there and back.
Here is one answer. Yours may be different and work too.

</details>

**3. Explain.** Schlomo, who is learning Python too, says: "My function
ran, and there was no error, so it works." What would you say to him?
Give an example from this unit.

<details class="dl-answer"><summary>answer</summary>

Python only reports an error when it cannot make a move, such as
dividing by zero or using a name that points at nothing. It has no idea
what the function was meant to do. So a function can run with no error
and still break its promise. The tutorial's `to_celsius` ran, and said
water boils at about 194 °C. Only a test case, such as "32 °F should
give 0 °C", showed that it broke its promise. An error does mean that
something needs a look. But no error does not mean the promise is
kept.

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

**5. Predict.** A yeast colony in a lab weighs 100 mg, and grows by 10%
each hour. After how many hours is it 150 mg or more? Make a trace
table with the columns `hours` and `mass` before you run the cell.
(Round the mass to two decimal places in your table.)

```python
mass = 100
hours = 0
while mass < 150:
    mass = mass * 1.1
    hours = hours + 1
print(hours, round(mass, 2))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start the table with `hours` 0 and `mass` 100.
2. Each row: check `mass < 150`. If it is true, multiply the mass by
   1.1 and add 1 to `hours`.
3. Stop at the first row where the check is false.

**Think about:** why the loop runs once more after 146.41, even though
that is so close to 150.

</details>

<details class="dl-answer"><summary>answer</summary>

| `hours` | `mass` | `mass < 150`? |
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

**7. Fix.** Schlomi, who is learning Python too, writes a function for
a photo app that makes a picture 10% wider. The test fails. Run it. Which
one does not say what Schlomi meant: the code, the comment or the
docstring? Change it.

```python exec
id: does-it-practice-fix-wider
def wider(width):
    """Return a picture's width, in pixels, made 10% wider."""
    return width * 1.15    # make it 10% wider

assert close_enough(wider(100), 110), "100 pixels, 10% wider, is 110"
print("wider keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The app's rule is 10%, and the docstring and the comment both say 10%.
The code multiplies by 1.15, which adds 15%. So we change the
code:

```python
def wider(width):
    """Return a picture's width, in pixels, made 10% wider."""
    return width * 1.10
```

We can delete the comment, because it says what the code says. Notice the test uses
`close_enough`. `100 * 1.10` is `110.00000000000001`, so `==` would fail
even with 1.10 in the code. That is why Schlomi's test uses
`close_enough`.

</details>

**8. Make.** A GPS app shows distances in kilometres or in miles.
One mile is exactly 1.609344 km. Write `km_to_miles` and `miles_to_km`.
Test them with a fact (a marathon is 42.195 km, about 26.2 miles), and
with a loop that goes there and back for every whole number of km from 0
to 1,000.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

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
needs a wider tolerance, because 26.2 is itself rounded. The exact value
is about 26.219. The round trip uses the default tolerance, and `==`
would have failed on 41 km, among others.

</details>

<aside class="dl-note" id="does-it-practice-note-marathon">

**Why 42.195?** Early marathons had no fixed length. At the 1908
Olympic Games in London, the course ran from Windsor to the stadium at
White City: 26 miles and 385 yards, which is 42.195 km. In 1921 that
became the official length of a marathon.

</aside>

**9. Explain.** An image app has a function to double a picture's
width. It has a bug, but its test passes. Why does the test pass? Write
a better test.

```python
def double(width):
    """Return twice width."""
    return width * width

assert double(2) == 4
```

<details class="dl-answer"><summary>answer</summary>

For 2, doubling and squaring give the same answer: $2 + 2 = 4$ and
$2 \times 2 = 4$. So the test cannot tell doubling from squaring. A test
case is only useful if a likely bug would give a different answer.
`assert double(3) == 6` fails for this function, since
$3 \times 3 = 9$, and that catches the bug. Useful test values avoid 0, 1
and 2, where many different rules happen to agree.

</details>

**10. Make.** This function from a camera app works, but nobody can
tell what it does. Rename it and its inputs with words, add a docstring, and
test that your version gives the same answers as the old one for three
different sets of values.

```python
def calc(x, y, z):
    t = x * y
    return t * z / 8 / 1000000
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try `calc(4000, 3000, 24)`. What could 4000 and 3000 be in a camera?
2. `t` is `x` times `y`. What do you get when you multiply a picture's
   width by its height?
3. The last line divides by 8 and then by a million. How many bits are
   in a byte?

**Think about:** which names would let a stranger guess what the
function does without running it?

</details>

<details class="dl-answer"><summary>answer</summary>

`x` and `y` are a photo's width and height in pixels, and `z` is how
many bits each pixel uses. The answer is the photo's size in megabytes.

```python
def calc(x, y, z):
    t = x * y
    return t * z / 8 / 1000000


def photo_megabytes(width, height, bits_per_pixel):
    """Return the size in MB of a photo, width by height pixels, before any squeezing."""
    pixels = width * height
    return pixels * bits_per_pixel / 8 / 1000000


for values in [(4000, 3000, 24), (1920, 1080, 24), (640, 480, 8)]:
    assert photo_megabytes(*values) == calc(*values)
print("The two versions agree.")
print(photo_megabytes(4000, 3000, 24))
```

It prints `The two versions agree.`, then `36.0`. A 12-megapixel photo
at 24 bits a pixel is 36 MB before it is squeezed. The `*values`
passes the three numbers in a row to the function as its three inputs,
the same way `*row` did on
[Untangling a condition](tutorial:untangling-a-condition). Here is one
answer. Yours may be different and work too.

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
`math.isclose` says False. Each tool suits its own space. A fixed
tolerance suits numbers of an everyday size, like temperatures and
distances in a room.

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

Now it gives 3. The order of the lines matters here. Every line is
needed, but one of them ran inside the loop when it belongs before it.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: does-it-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** The unit converter this unit is building has many pairs
of functions that should undo each other. Write
`works_both_ways(forwards, backwards, values)`, which returns `True`
when `backwards(forwards(value))` is close enough to `value` for every
value in `values`, and `False` otherwise. Test it on the temperature
tools, on the travel tools, and on a pair that does not undo each other.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over `values`.
2. For each one, go there and back, and compare with `close_enough`.
3. If any value fails, return `False` straight away. If the loop
   finishes, return `True`.

**Think about:** `travel_time` and `distance_travelled` take two inputs.
How could you make a one-input function from each, for a fixed speed?

**Try this next:** make `works_both_ways` say which value failed.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

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

This prints `True`, `True`, `False`. If you convert to Fahrenheit twice,
you do not get the first temperature back, and the tool catches it.

</details>

**14. Explain.** `close_enough` uses a tolerance of a billionth. Two
lab results are 0.000000001 grams and 0.000000002 grams, and
`close_enough` says they are equal. A GPS says two points are
20,200,000.0 and 20,200,000.1 metres from a satellite, and
`close_enough` says they are not equal. Is `close_enough` breaking its
promise? When
would you change its tolerance?

<details class="dl-answer"><summary>answer</summary>

`close_enough` keeps its promise both times. The first pair differs by
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

**15. Fix.** A phone shows its battery icon in red below 20%, in amber
from 20% to 49%, and in green from 50% up. Write test cases at every
edge of that promise, run them, and fix the bug they find.

```python exec
id: does-it-practice-fix-battery
def battery_colour(percent):
    """Return the battery icon's colour: red under 20, amber from 20 to 49, green from 50."""
    if percent < 20:
        return "red"
    elif percent < 49:
        return "amber"
    else:
        return "green"

# Your test cases here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The promise changes at 20 and at 50. Those are the edges.
2. Test the value right before each edge, and the edge itself: 19, 20,
   49 and 50.
3. Which one gives a colour the promise does not?

**Think about:** "20 to 49" includes 49. Which sign includes it?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
assert battery_colour(19) == "red", "19 is under 20"
assert battery_colour(20) == "amber", "20 is the first amber"
assert battery_colour(49) == "amber", "49 is the last amber"
assert battery_colour(50) == "green", "50 is the first green"
print("battery_colour keeps its promise.")
```

The test for 49 fails: `49 < 49` is False, so 49% shows green. Either of
these fixes it:

```python
def battery_colour(percent):
    """Return the battery icon's colour: red under 20, amber from 20 to 49, green from 50."""
    if percent < 20:
        return "red"
    elif percent < 50:
        return "amber"
    else:
        return "green"
```

or `elif between(percent, 20, 49):`, with the toolkit's `between`. A
test in the middle, like 35, would never have found this bug. Bugs like
this one are often at the edges, so put your tests there.

</details>

**16. Explain.** The tutorial page had you write a trace table by hand
before it showed you `step_through`. Some teachers would show the debugger
first, and skip the hand trace. For a short function you have never seen
before, which would you do first, and why? Is there a function where you
would skip the hand trace altogether?

<details class="dl-answer"><summary>answer</summary>

There is more than one good answer. Here are some things to weigh.

- **By hand first.** You have to predict each value before you see it,
  and a prediction that misses shows you exactly where your picture of
  the code and Python's differ. But it is slow, and a value copied
  by hand can come out different from the one Python holds.
- **Debugger first.** It is fast, and it copies every value exactly.
  But the values appear before you have thought about them, so it
  is possible to watch without learning much.

A loop that runs 1,000 times is one place to skip the hand trace. Nobody
can write 1,000 rows. A function you already trust, like `total`, is
another. One answer might say: trace a short, new function by hand,
and use the debugger for long runs, or to check a hand trace.

</details>
