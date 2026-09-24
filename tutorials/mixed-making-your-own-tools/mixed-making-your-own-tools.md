---
title: "Mixed problems: making your own tools"
practice_across:
  - machines-that-take-a-number
  - measuring-rooms-and-tins
  - running-a-formula-backwards
  - does-it-work
  - what-a-function-can-see
year: "2026-2027"
version: 2026.09.24.1
---

# Mixed problems: making your own tools

Each problem here draws on at least one page of Unit 4, and many draw on
two or more. None of them is harder than what those pages covered. The
new part is that nobody tells you which page a problem comes from.
Choosing the tool is part of the problem.

Along the way, the problems build this unit's product: a unit
converter, where every conversion is tested both ways. Going there and
back should bring you home. Problems 5, 6, 10, 15 and 16 are the
converter's main parts, and they build on each other, so do those in
order.

Your toolkit is loaded on this page: `compose`, the area and volume
functions, the temperature and travel functions and `close_enough` from
this unit, and every tool from Units 1 to 3. Each answer is hidden until
you open it. Where a problem asks you to predict, make the prediction
before you run anything. It is the most useful part.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: mixed-tools-scratch-1
# Try things here
```

**1. Predict.** An oven dial shows Fahrenheit. What does this line show?
Work it out by hand first.

```python
print(compose(celsius_to_fahrenheit, fahrenheit_to_celsius)(212))
```

<details class="dl-answer"><summary>answer</summary>

`212.0`.

`compose(outer, inner)` runs `inner` first. So 212 °F goes into
`fahrenheit_to_celsius`, and comes out as 100 °C, the boiling point of
water. Then `celsius_to_fahrenheit` turns 100 back into 212. A function
composed with its inverse gives back what it was given, as on
[Running a formula backwards](tutorial:running-a-formula-backwards#the-promise-run-backwards).
It is a float, `212.0`, because `/` always gives a float.

</details>

**2. Predict.** A game moves a player to the next level. What does the
last line show?

```python
level = 1

def next_level(level):
    return level + 1

next_level(level)
print(level)
```

<details class="dl-answer"><summary>answer</summary>

`1`.

The call works out 2, and gives it back, but nothing keeps it. The
parameter `level` lives in the call's own space, and the page's `level`
never changes. On
[What a function can see](tutorial:what-a-function-can-see#values-in-by-position-and-by-name)
that was the `add_tip` table. To move up a level, the page has to say
so: `level = next_level(level)`.

</details>

**3. Explain.** `celsius_to_fahrenheit(-10)` is a sensible question: it
is a cold night in January. What about a distance converter,
`km_to_miles(-10)`? What is the domain of each converter, and why are
they different?

<details class="dl-answer"><summary>answer</summary>

A temperature can be below zero on either scale, so the domain of
`celsius_to_fahrenheit` is every temperature down to absolute zero,
about −273 °C. A distance is never negative, so the domain of
`km_to_miles` is every number from 0 up.

Python will work out `-10 / 1.609344` without a word, and give a negative
answer. The rule does not know what it is for. That is the lesson from
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out):
the domain belongs in the docstring, and an `assert` can check it.

</details>

**4. Make.** A bedroom wall is 4 m wide and 2.5 m high. One litre of
paint covers 10 square metres, and the wall needs two coats. Use
`rectangle_area` to work out how many litres of paint to buy.

<details class="dl-answer"><summary>answer</summary>

```python
wall = rectangle_area(4, 2.5)
coats = 2
litres = wall * coats / 10
print(wall, litres)
```

The wall is 10.0 square metres. Two coats cover 20 square metres, so
the room needs 2.0 litres of paint. The formula from
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins) did the
first step; the rest is one line of arithmetic.

</details>

## Core

A scratch cell for the core problems. Keep the converter's functions in
it as you write them, so that later problems can use them.

```python exec
id: mixed-tools-scratch-2
# Your converter, problem by problem
```

**5. Make.** On 20 January 2005, Ireland's speed limit signs changed
from miles per hour to kilometres per hour. One mile is exactly
1.609344 km. Write `miles_to_km(miles)` and `km_to_miles(km)`, each
with a docstring. Test them with values you know: 1 mile is 1.609344 km,
and 0 is 0 in both. Then find what the old 60 mph limit is in km/h.

<details class="dl-answer"><summary>answer</summary>

```python
KM_PER_MILE = 1.609344


def miles_to_km(miles):
    """Give back a distance in km, given it in miles. miles must be 0 or more."""
    return miles * KM_PER_MILE


def km_to_miles(km):
    """Give back a distance in miles, given it in km. This undoes miles_to_km."""
    return km / KM_PER_MILE


assert miles_to_km(1) == 1.609344
assert km_to_miles(1.609344) == 1
assert miles_to_km(0) == 0 and km_to_miles(0) == 0
print(miles_to_km(60))
```

60 mph is about 96.6 km/h. On national roads the new signs rounded it
to 100 km/h. On regional and local roads the new limit was 80 km/h.

`KM_PER_MILE` is a global name, and both functions read it. That is not
a hidden input in the sense of the tutorial, because it never changes:
the capital letters are how Python programmers say "this name is fixed".
The rule has one number in it, and it is written once.

</details>

**6. Make.** Here is the tool that makes the converter trustworthy.
Write `works_both_ways(there, back, values)`. It should give back
`True` when, for every value in `values`, `back(there(value))` is
`close_enough` to the value, and `False` otherwise. Use `compose`. Try
it on your two distance functions with the values 0, 1, 26.2 and 100,
and on the two temperature functions.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `round_trip = compose(back, there)` is one function that goes there
   and back.
2. Loop over `values`. As soon as one value does not come home, give
   back `False`.
3. Only after the loop has finished, give back `True`.

**Think about:** why must `return True` be outside the loop?

**Try this next:** find two functions that are not inverses, and check
that `works_both_ways` says `False`.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def works_both_ways(there, back, values):
    """Give back True when back undoes there for every value in values."""
    round_trip = compose(back, there)
    for value in values:
        if not close_enough(round_trip(value), value):
            return False
    return True


print(works_both_ways(miles_to_km, km_to_miles, [0, 1, 26.2, 100]))
print(works_both_ways(celsius_to_fahrenheit, fahrenheit_to_celsius, [-40, 0, 37, 100]))
print(works_both_ways(miles_to_km, miles_to_km, [0, 1]))
```

The first two lines show `True`. The last shows `False`: going from
miles to km twice does not bring 1 home. (It passes at 0, which is a
reason to test more than one value.)

`close_enough` is there because a round trip through floats can land a
tiny distance from home, as `fahrenheit_to_celsius` showed on
[Running a formula backwards](tutorial:running-a-formula-backwards#the-promise-run-backwards).

</details>

**7. Fix.** An airline allows a 23 kg suitcase, and a passenger from
the United States wants it in pounds. One pound is exactly 0.45359237
kg. This cell tests the two weight functions both ways, and stops with
an `AssertionError`. Find the mistake, and fix it.

```python exec
id: mixed-tools-fix-weight
KG_PER_POUND = 0.45359237


def kg_to_pounds(kg):
    """Give back a weight in pounds, given it in kg."""
    return kg / KG_PER_POUND


def pounds_to_kg(pounds):
    """Give back a weight in kg, given it in pounds."""
    return pounds / KG_PER_POUND


for weight in [0, 1, 23, 100]:
    assert close_enough(pounds_to_kg(kg_to_pounds(weight)), weight)
print("The weight functions work both ways.")
print(kg_to_pounds(23))
```

<details class="dl-answer"><summary>answer</summary>

`pounds_to_kg` divides, when it should multiply. The test passes at 0
and fails at 1. A walkthrough of 1 kg shows why: `kg_to_pounds(1)` is
about 2.2 pounds, and `pounds_to_kg` then divides 2.2 by 0.45 again,
giving about 4.9 kg, not 1.

```python
def pounds_to_kg(pounds):
    """Give back a weight in kg, given it in pounds."""
    return pounds * KG_PER_POUND
```

Now the test passes, and the suitcase limit is about 50.7 pounds.

</details>

**8. Explain.** A friend writes `miles_to_km` with 1.6 in place of
1.609344, and `km_to_miles` with 1.6 too. Will `works_both_ways` catch
the mistake? What kind of test would?

<details class="dl-answer"><summary>answer</summary>

`works_both_ways` will say `True`. Multiplying by 1.6 and dividing by
1.6 undo each other perfectly, so every value comes home. The two
functions are wrong in the same way, and a round trip cannot see a
mistake that the way back undoes.

A test with a known value catches it: `miles_to_km(1)` should be
1.609344, and the friend's version gives 1.6. So a converter needs both
kinds of test from
[Running a formula backwards](tutorial:running-a-formula-backwards#the-promise-run-backwards):
known values, to check the factor is right, and round trips, to check
the two directions agree. Neither kind is enough alone.

</details>

**9. Predict.** Someone keeps the factor on the page, and later uses
the same name for another unit. What does the last line show, and what
should it show?

```python
factor = 1.609344

def miles_to_km_from_page(miles):
    return miles * factor

factor = 0.45359237
print(miles_to_km_from_page(10))
```

<details class="dl-answer"><summary>answer</summary>

It shows about `4.536`, and it should show about `16.09`.

The function reads `factor` each time it runs, and by then the page's
`factor` points at the pound factor. That is the hidden input from
[What a function can see](tutorial:what-a-function-can-see#what-a-function-can-see-from-outside).
No error appears: the answer is wrong, quietly. A test with a known
value, like `miles_to_km_from_page(1) == 1.609344`, would catch it, if
it ran after the name was reused.

</details>

**10. Make.** Every converter so far has the same shape: multiply by a
factor, or divide by it. Write `scaler(factor)`, which gives back a
function that multiplies its input by `factor`. Then use it to make
`litres_to_gallons` and `gallons_to_litres`. One UK gallon is exactly
4.54609 litres. Check them with `works_both_ways`, and find the price of
a gallon of fuel at €1.80 a litre.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `scaler` has the shape of `rate_converter` on
   [What a function can see](tutorial:what-a-function-can-see#a-function-made-inside-a-function).
2. Going the other way is multiplying by `1 / factor`.
3. A price per litre is a different question from a number of litres.
   How many litres are in a gallon?

**Think about:** where does each of your two new functions find its
`factor`?

**Try this next:** use `scaler` to rewrite `miles_to_km` and
`km_to_miles` in two lines.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def scaler(factor):
    """Give back a function that multiplies its input by factor."""
    def scale(value):
        return value * factor
    return scale


LITRES_PER_GALLON = 4.54609
gallons_to_litres = scaler(LITRES_PER_GALLON)
litres_to_gallons = scaler(1 / LITRES_PER_GALLON)

print(works_both_ways(litres_to_gallons, gallons_to_litres, [0, 1, 50, 1000]))
print(round(1.80 * gallons_to_litres(1), 2))
```

The first line shows `True`. A gallon holds about 4.55 litres, so at
€1.80 a litre it costs €8.18.

`gallons_to_litres` and `litres_to_gallons` are two closures. Each was
made in its own call to `scaler`, and each keeps its own `factor`.

</details>

**11. Another way.** In Ireland, people often give their weight in
stone. One stone is 14 pounds. Write `pounds_to_stone`, and use
`compose` with your fixed `kg_to_pounds` from problem 7 to make
`kg_to_stone`. Then find a second route: one stone is exactly 6.35029318
kg. Check that the two routes agree for 70 kg.

<details class="dl-answer"><summary>answer</summary>

```python
def pounds_to_stone(pounds):
    """Give back a weight in stone, given it in pounds."""
    return pounds / 14


kg_to_stone = compose(pounds_to_stone, kg_to_pounds)

def kg_to_stone_directly(kg):
    """Give back a weight in stone, given it in kg, in one step."""
    return kg / 6.35029318


print(kg_to_stone(70), kg_to_stone_directly(70))
print(close_enough(kg_to_stone(70), kg_to_stone_directly(70)))
```

Both routes give about 11.02 stone, and `close_enough` says `True`. The
second route's number is $14 \times 0.45359237$, the two steps of the
first route multiplied together. Composing two scalings is one scaling,
by the product of their factors.

</details>

**12. Explain.** A metronome is set in beats per minute. A drummer wants
to know how many seconds each beat lasts. At 120 beats per minute, each
beat is $60 \div 120 = 0.5$ seconds. So `seconds_per_beat(bpm)` gives
back `60 / bpm`. What is its inverse, the function that turns seconds
per beat back into beats per minute? What is surprising about it?

<details class="dl-answer"><summary>answer</summary>

Rearrange $s = \frac{60}{b}$ to make $b$ the subject. Multiply both
sides by $b$, then divide both sides by $s$: $b = \frac{60}{s}$.

That is the same rule. The function is its own inverse:

```python
def seconds_per_beat(bpm):
    """Give back how long one beat lasts, in seconds, at bpm beats per minute."""
    return 60 / bpm

print(seconds_per_beat(120), seconds_per_beat(0.5))
print(works_both_ways(seconds_per_beat, seconds_per_beat, [40, 60, 120, 200]))
```

The first line shows `0.5 120.0`. One machine takes 120 to 0.5, and the
same machine takes 0.5 back to 120. The domain leaves out 0, as the
`travel_time` formula did: a metronome at 0 beats per minute never
ticks.

</details>

**13. Make.** A saucepan is a cylinder, 10 cm in radius and 12 cm deep.
Use `cylinder_volume` to find how many litres it holds. (A litre is 1000
cubic centimetres.) A recipe from the United States asks for 4 cups of
stock, and a US cup is about 0.24 litres. Does it fit?

<details class="dl-answer"><summary>answer</summary>

```python
pot_cm3 = cylinder_volume(10, 12)
pot_litres = pot_cm3 / 1000
stock_litres = 4 * 0.24
print(round(pot_litres, 2), stock_litres, stock_litres < pot_litres)
```

The pot holds about 3.77 litres, and the stock is 0.96 litres, so it
fits with plenty of room for the vegetables. The volume is
$\pi r^2 h = \pi \times 10^2 \times 12$, about 3770 cm³.

</details>

## Stretch

A scratch cell for the stretch problems. Your converter from the core
problems needs to be in it, or in the core scratch cell above, run
first.

```python exec
id: mixed-tools-scratch-3
# Try things here
```

**14. Another way.** A runner logs a week of training in miles: 3.1,
5, 6.2 and 13.1. Find the week's total in km two ways. First, add the
miles with `total`, then convert. Second, convert each run, then add.
Do the two ways agree? Now try the same two ways on three days of
temperatures, 10, 12 and 15 °C, converted to Fahrenheit. What happens,
and why?

<details class="dl-answer"><summary>answer</summary>

```python
runs = [3.1, 5, 6.2, 13.1]
first = miles_to_km(total(runs))

runs_in_km = []
for run in runs:
    runs_in_km.append(miles_to_km(run))
second = total(runs_in_km)

print(first, second, close_enough(first, second))
```

Both ways give about 44.1 km, and `close_enough` says `True`.

```python
days = [10, 12, 15]
days_in_f = []
for day in days:
    days_in_f.append(celsius_to_fahrenheit(day))

print(celsius_to_fahrenheit(total(days)))
print(total(days_in_f))
```

These do not agree: 98.6 and 162.6. Converting each day adds 32 three
times, and converting the total adds it once. A total of temperatures
is not a temperature anyone would feel, either.

So "add, then convert" is a move that works in one space and not the
other. It works for a converter that only multiplies, like miles to
km. It fails for a converter that also adds, like Celsius to
Fahrenheit.

</details>

**15. Make.** Now the converter itself. Write
`convert(value, from_unit, to_unit)`. It should know six units:
`"km"`, `"miles"`, `"kg"`, `"pounds"`, `"C"` and `"F"`, and convert
between each unit and its partner, in both directions. For any other
pair, it should stop with an `assert` message that names the pair. Use
the functions you have already written.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Use `if` and `elif`, one branch for each of the six directions.
2. Each branch gives back one of your converter functions, called on
   `value`.
3. After the last `elif`, an `assert False, "..."` stops with your
   message.

**Think about:** `convert` has three parameters, and `from_unit` and
`to_unit` are strings. What would happen if someone called it with the
units in the wrong order?

**Try this next:** add `"litres"` and `"gallons"`.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def convert(value, from_unit, to_unit):
    """Give back value, measured in from_unit, in to_unit instead.

    Knows km and miles, kg and pounds, and C and F.
    """
    if from_unit == "km" and to_unit == "miles":
        return km_to_miles(value)
    elif from_unit == "miles" and to_unit == "km":
        return miles_to_km(value)
    elif from_unit == "kg" and to_unit == "pounds":
        return kg_to_pounds(value)
    elif from_unit == "pounds" and to_unit == "kg":
        return pounds_to_kg(value)
    elif from_unit == "C" and to_unit == "F":
        return celsius_to_fahrenheit(value)
    elif from_unit == "F" and to_unit == "C":
        return fahrenheit_to_celsius(value)
    assert False, "convert does not know " + from_unit + " to " + to_unit


print(convert(26.2, "miles", "km"))
print(convert(23, "kg", "pounds"))
print(convert(-40, "C", "F"))
convert(5, "km", "kg")
```

The first three lines show a marathon in km, about 42.2, the suitcase
limit, about 50.7 pounds, and −40.0, where the two temperature scales
meet. The last line stops with
`AssertionError: convert does not know km to kg`, which is the promise
naming its own domain: a distance cannot become a weight.

If someone swaps the units, `convert(42.2, "km", "miles")` still works:
the strings are matched by what they say, so the order of the branches
does not matter here. Swapping `value` with a unit is another matter,
and gives a `TypeError`. Keyword arguments, like
`convert(value=10, from_unit="km", to_unit="miles")`, make each value's
job plain in the call itself.

</details>

**16. Make.** The last step: test every pair in `convert` both ways,
with `works_both_ways`. The trouble is that `works_both_ways` wants
functions of one input, and `convert` has three. Write
`converter_for(from_unit, to_unit)`, which gives back a one-input
function, and use it to check all three pairs.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Inside `converter_for`, define a function of one input, `value`, that
   calls `convert(value, from_unit, to_unit)`.
2. Give that function back, without brackets.
3. For each pair, `there` is `converter_for(a, b)` and `back` is
   `converter_for(b, a)`.

**Think about:** which space does the inner function find `from_unit`
and `to_unit` in?

**Try this next:** add litres and gallons to `convert`, and their pair
to the test. How many lines did the test need to grow by?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def converter_for(from_unit, to_unit):
    """Give back a function of one value that converts it from from_unit to to_unit."""
    def one_way(value):
        return convert(value, from_unit, to_unit)
    return one_way


test_values = [0, 1, 23, 100, 1000]
for pair in [("km", "miles"), ("kg", "pounds"), ("C", "F")]:
    there = converter_for(pair[0], pair[1])
    back = converter_for(pair[1], pair[0])
    assert works_both_ways(there, back, test_values), pair
    assert works_both_ways(back, there, test_values), pair
print("Every conversion works both ways.")
```

It prints `Every conversion works both ways.` Each pair is tested
twice, starting from each end, so there are six round trips over five
values each.

`one_way` is a closure. It finds `from_unit` and `to_unit` in the space
of the call to `converter_for` that made it, and that is what lets a
three-input tool become a one-input tool that `compose` can use. That
is the whole unit in one function: a promise (`convert`), its inverse,
a composition, a test, and a function that remembers what it can see.

</details>

**17. Fix.** Someone's first version of `works_both_ways` says `True` for
two functions that do not undo each other: doubling, and
dividing by 3. Find the mistake. Why did the value 0 hide it?

```python exec
id: mixed-tools-fix-both-ways
def works_both_ways_first_try(there, back, values):
    """Give back True when back undoes there for every value in values."""
    round_trip = compose(back, there)
    for value in values:
        if close_enough(round_trip(value), value):
            return True
        else:
            return False


def double(x):
    return 2 * x


def third(x):
    return x / 3


print(works_both_ways_first_try(double, third, [0, 1, 2, 3]))    # should be False
```

<details class="dl-answer"><summary>answer</summary>

Both `return` lines are inside the loop, so the function gives back an
answer after the first value, and never looks at the rest. The first
value is 0, and $0 \times 2 \div 3$ is 0, so 0 comes home, and the answer
is `True`.

A walkthrough shows it: the loop starts with `value` pointing at 0,
the `if` is True, `return True` runs, and the call's space is thrown
away with 1, 2 and 3 never checked. The fix is the shape from problem 6:

```python
def works_both_ways_fixed(there, back, values):
    round_trip = compose(back, there)
    for value in values:
        if not close_enough(round_trip(value), value):
            return False
    return True

print(works_both_ways_fixed(double, third, [0, 1, 2, 3]))    # False
```

A function can say `False` as soon as one value fails, but it can only
say `True` after it has checked them all. And 0 is a weak test value
for any converter that only multiplies, because every factor takes 0
to 0.

</details>
