---
title: "Machines that take a number: functions in maths and code — Practice"
practice_for: machines-that-take-a-number
year: "2026-2027"
version: 2026.09.24.1
---

# Machines that take a number: functions in maths and code — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, `compose` included. Every other
function a problem needs is written out in the problem.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: machines-practice-warm-up
# Try things here
```

**1. Predict.** A drummer's app turns a speed in beats per minute into
the time between two beats, in seconds. What does each line print?

```python
def seconds_per_beat(bpm):
    """Return the seconds between two beats, at bpm beats per minute."""
    return 60 / bpm

print(seconds_per_beat(120))
print(seconds_per_beat(60))
print(seconds_per_beat(90))
```

<details class="dl-answer"><summary>answer</summary>

`0.5`, `1.0` and `0.6666666666666666`.

A minute is 60 seconds. At 120 beats a minute, each beat gets half a
second. At 60 it gets a whole second. At 90 the answer is $\frac{2}{3}$
of a second, which a float can only hold as a long decimal. And `/`
always gives a float, which is why the second line shows `1.0` and not
`1`.

</details>

**2. Make.** A common rule of thumb says that a person's highest safe
heart rate, in beats per minute, is 220 minus their age. Write the rule
in function notation, then as a Python function `max_heart_rate(age)`.
What does it give for an age of 40?

<details class="dl-answer"><summary>answer</summary>

In function notation, with $a$ for the age: $h(a) = 220 - a$.

```python
def max_heart_rate(age):
    """Return a rough highest safe heart rate, in beats per minute."""
    return 220 - age

print(max_heart_rate(40))
```

This prints `180`. It is only a rough rule: a doctor or a fitness test
gives a better number for one person.

</details>

**3. Explain.** In this code, what is the parameter, and what is the
argument?

```python
def pizza_slices(people):
    """Return how many slices to order, at 3 slices each."""
    return people * 3

print(pizza_slices(4))
```

<details class="dl-answer"><summary>answer</summary>

The parameter is `people`: the name in the brackets of the `def` line.
The argument is `4`: the value put into that slot when the function is
called. The parameter is the slot, and the argument is what goes in it.
Call `pizza_slices(9)` and the parameter is still `people`, but the
argument is now 9.

</details>

**4. Predict.** What does this cell print? There are two lines.

```python
def greet(name):
    """Print a greeting for name."""
    print("Hello,", name)

answer = greet("Aoife")
print(answer)
```

<details class="dl-answer"><summary>answer</summary>

```text
Hello, Aoife
None
```

`greet` is a procedure. It does a job, printing, and it has no `return`
line. So when it finishes, it gives back `None`, and that is what the
name `answer` points at.

</details>

## Core

A cell for your core answers.

```python exec
id: machines-practice-core
# Try things here
```

**5. Make.** A weather station counts the days in a year with some rain.
Write `rain_percent(rainy_days)`, which gives those days as a percentage
of 365. Its domain is the whole numbers from 0 to 365. Use `between`
from your toolkit in an `assert` with a message, so that 400 days stops
with a clear error. Try it with 230 days, then with 400.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The percentage is the rainy days divided by 365, times 100.
2. `between(rainy_days, 0, 365)` is True for every day count in the
   domain.
3. An `assert` can carry a message after a comma:
   `assert condition, "message"`.

**Think about:** which line has to come first, the `assert` or the
`return`? What happens to lines after a `return`?

**Try this next:** round the answer to one decimal place.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def rain_percent(rainy_days):
    """Return rainy_days as a percentage of a 365-day year.

    rainy_days is a whole number from 0 to 365.
    """
    assert between(rainy_days, 0, 365), "a year has 0 to 365 days"
    return rainy_days / 365 * 100

print(rain_percent(230))
print(rain_percent(400))
```

The first line prints `63.013698630136986`. The second stops with
`AssertionError: a year has 0 to 365 days`. The `assert` must come
before the `return`, because nothing after a `return` runs.

</details>

**6. Predict.** In a game, a power-up doubles your score, and a bonus
adds 10 points. What does each line print?

```python
def double(score):
    """Return the score, doubled."""
    return score * 2

def add_bonus(score):
    """Return the score, with 10 bonus points."""
    return score + 10

print(compose(double, add_bonus)(5))
print(compose(add_bonus, double)(5))
```

<details class="dl-answer"><summary>answer</summary>

`30`, then `20`.

`compose(double, add_bonus)` runs `add_bonus` first, because it is the
inner function: 5 becomes 15, then doubles to 30. The other order
doubles first, to 10, and then adds the bonus, to 20. A player would
want the bonus before the power-up.

</details>

**7. Fix.** A city bike costs €3 to unlock, then €0.25 for each minute.
`minutes_for` is meant to be the inverse of `bike_cost`, but the test
fails. Run it, read the error, and fix `minutes_for`.

```python exec
id: machines-practice-fix-bike
def bike_cost(minutes):
    """Return the cost in euro of a bike ride of minutes minutes."""
    return 3 + 0.25 * minutes


def minutes_for(cost):
    """Return how many minutes a ride was, if it cost cost euro."""
    return cost / 0.25 - 3


assert minutes_for(bike_cost(20)) == 20
print("minutes_for undoes bike_cost.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. List the steps of `bike_cost`, in order: first multiply by 0.25, then
   add 3.
2. To undo them, undo the last step first.
3. What does `minutes_for(8)` give now? A 20-minute ride costs €8.

**Think about:** putting on socks and then shoes. Which one comes off
first?

**Try this next:** add a test that goes the other way:
`bike_cost(minutes_for(8)) == 8`.

</details>

<details class="dl-answer"><summary>answer</summary>

The steps are undone in the wrong order. `bike_cost` multiplies by 0.25
and then adds 3, so the inverse must take away 3 first, and then divide
by 0.25:

```python
def minutes_for(cost):
    """Return how many minutes a ride was, if it cost cost euro."""
    return (cost - 3) / 0.25
```

Now `minutes_for(8)` is `20.0`, and the test passes. The old version
gave $8 \div 0.25 - 3 = 29$.

</details>

**8. Explain.** Squaring has no inverse on all of $\mathbb{R}$. Cubing,
$x^3 = x \times x \times x$, does. Why the difference? Try a few numbers
in the cell first, negative ones too.

<details class="dl-answer"><summary>answer</summary>

Squaring sends 3 and −3 to the same output, 9, so the output cannot say
which one went in. Squaring is not one-to-one.

Cubing keeps the sign: $3^3 = 27$ and $(-3)^3 = -27$. Every real number
has exactly one cube, and every output comes from exactly one input, so
cubing is one-to-one. Its inverse is the cube root: $\sqrt[3]{27} = 3$
and $\sqrt[3]{-27} = -3$.

```python
for x in [-3, -2, 2, 3]:
    print(x, x ** 3, x ** 2)
```

The middle column is different on every line. The last column is not.

</details>

**9. Another way.** How many even numbers are there from 1 to $n$? One
algorithm counts them with a loop and `%`. Another says the answer is
`n // 2`. Write the loop version as `evens_by_loop(n)`, and check that
the two algorithms are the same function for every $n$ from 0 to 200.

<details class="dl-answer"><summary>answer</summary>

```python
def evens_by_loop(n):
    """Return how many even numbers there are from 1 to n."""
    count = 0
    for number in range(1, n + 1):
        if number % 2 == 0:
            count = count + 1
    return count


for n in range(0, 201):
    assert evens_by_loop(n) == n // 2
print("Two algorithms, one function.")
```

It prints `Two algorithms, one function.` The loop looks at every
number. `n // 2` counts the whole pairs in $n$, and every pair has one
even number in it.

</details>

**10. Fix.** A shop's app adds 23% VAT to two prices and adds them up.
It stops with an error. Run it, read the last line of the error, and
fix `vat_price`.

```python exec
id: machines-practice-fix-vat
def vat_price(price):
    """Return the price with 23% VAT added."""
    print(price * 1.23)


basket = vat_price(10) + vat_price(20)
print("Total:", basket)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last line of the error names two kinds of value. Which one is
   `NoneType`?
2. What does a function give back when it has no `return` line?
3. The docstring says "Return". Does the function do that?

**Think about:** the difference between showing a number and handing it
back.

</details>

<details class="dl-answer"><summary>answer</summary>

The error is
`TypeError: unsupported operand type(s) for +: 'NoneType' and 'NoneType'`.
`vat_price` prints its answer, but gives back `None`, and Python cannot
add `None` to `None`. The docstring promised to return the price, so
keep that promise:

```python
def vat_price(price):
    """Return the price with 23% VAT added."""
    return price * 1.23
```

Now the cell prints `Total: 36.900000000000006`. The long tail is float
rounding, which we met on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros);
`round(basket, 2)` shows `36.9`. The two numbers the old version printed
were right. Only the handing back was missing.

</details>

**11. Predict.** Your toolkit's `split_bill` has the parameters
`total`, `people` and `tip_percent`, in that order. What does each line
print? One of them stops with an error.

```python
print(split_bill(people=2, total=30))
print(split_bill(30, 2, tip_percent=20))
print(split_bill(2, 30))
print(split_bill(total=30, 2))
```

<details class="dl-answer"><summary>answer</summary>

Python reads the whole cell before it runs any of it, and the last line
is not allowed. So nothing prints at all: the cell stops with
`SyntaxError: positional argument follows keyword argument`.

Take the last line out, and the others print `15.0`, `18.0` and `0.07`.
With keyword arguments, the order in the call does not matter, because
each value names its slot. Without them, the order is everything:
`split_bill(2, 30)` shares a €2 bill between 30 people. Once one
argument is named, every argument after it must be named too.

</details>

## Stretch

**12. Make.** A lighting app keeps each colour level as a number from 0
to 1. A web page wants it as a byte, from 0 to 255, written in hex, as
on [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
Write `to_byte(level)`, which gives `round(level * 255)`. Then use
`compose` and your toolkit's `to_hex` to make `hex_for`, which goes
straight from a level to hex. Try it on 1, 0.5 and 0. Is every answer
ready to go into a colour like `#RRGGBB`?

```python exec
id: machines-practice-colour
# Your to_byte and hex_for
```

<details class="dl-answer"><summary>answer</summary>

```python
def to_byte(level):
    """Return a colour level from 0 to 1 as a byte from 0 to 255."""
    return round(level * 255)


hex_for = compose(to_hex, to_byte)

print(hex_for(1))
print(hex_for(0.5))
print(hex_for(0))
```

This prints `FF`, `80` and `0`. The last one is not ready: a colour
needs two hex digits for each byte, so 0 must be written `00`. `to_hex`
keeps its own promise, which says nothing about two digits. The fix
belongs in a third machine that adds a 0 in front of a one-digit
answer, composed after the other two.

</details>

**13. Make.** At a meeting, every person shakes hands once with every
other person. On [Orders and choices](tutorial:orders-and-choices) we
counted these with `combinations(people, 2)`. Now go backwards: if
there were 45 handshakes, how many people were there? Write
`people_for(handshakes)`, with a `while` loop that tries 2 people, then
3, and so on, until `combinations(people, 2)` reaches `handshakes`. Try
it on 45. What should it do with 50?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with `people = 2`.
2. While `combinations(people, 2)` is less than `handshakes`, add 1 to
   `people`.
3. When the loop ends, `combinations(people, 2)` is `handshakes` or more.
   Which of the two tells you the answer was in the range?

**Think about:** is `combinations(people, 2)` one-to-one, for 2 or more
people? What does that say about the inverse?

**Try this next:** list the numbers of handshakes that are possible for
2 to 10 people. Those are the range, and the domain of `people_for`.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def people_for(handshakes):
    """Return how many people shook hands, if there were handshakes in total.

    handshakes must be a number that some group can make: 1, 3, 6, 10, ...
    """
    people = 2
    while combinations(people, 2) < handshakes:
        people = people + 1
    assert combinations(people, 2) == handshakes, "no group makes that many handshakes"
    return people

print(people_for(45))
print(people_for(50))
```

The first line prints `10`, because $C(10, 2) = 45$. The second stops
with `AssertionError: no group makes that many handshakes`. Nine people
make 36 handshakes and ten make 45, so 50 is not in the range of the
handshake function, and not in the domain of its inverse.

Each extra person makes more handshakes, never the same number, so the
handshake function is one-to-one for 2 or more people. That is why it
has an inverse at all.

</details>

**14. Another way.** A clock shows the hours 0 to 11. The function
`later(hour)` gives the time 4 hours on: `(hour + 4) % 12`. A student
says its inverse is "take away 4", and tries it on 2 o'clock: $2 - 4$ is
$-2$. Is the student wrong? Find the space where "take away 4" is right,
and check the inverse with `compose` for every hour.

<details class="dl-answer"><summary>answer</summary>

The student has the right move, in the wrong space. On a clock, the
numbers go round, so "take away 4" also has to go round. Python's `%`
does that for us, even with a negative number:

```python
def later(hour):
    """Return the hour on a 12-hour clock, 4 hours after hour."""
    return (hour + 4) % 12


def earlier(hour):
    """Return the hour on a 12-hour clock, 4 hours before hour."""
    return (hour - 4) % 12


there_and_back = compose(earlier, later)
for hour in range(12):
    assert there_and_back(hour) == hour
print(earlier(2))
```

It prints `10`, and every test passes. In the integers, $2 - 4 = -2$.
On the clock, $2 - 4$ is 10 o'clock, and "take away 4" is the inverse
of "add 4" there, as it was in the integers. The move was never
foolish.

</details>

**15. Explain.** A running app turns a time in seconds into minutes,
minutes into hours, and hours into a rounded, readable number. Here are
three machines joined in two different groupings. Predict, run, then
say why the two answers agree. Would they still agree if you swapped
the order of two of the machines?

```python exec
id: machines-practice-grouping
def to_minutes(seconds):
    """Return seconds as minutes."""
    return seconds / 60


def to_hours(minutes):
    """Return minutes as hours."""
    return minutes / 60


def to_one_place(hours):
    """Return hours rounded to one decimal place."""
    return round(hours, 1)


first_way = compose(to_one_place, compose(to_hours, to_minutes))
second_way = compose(compose(to_one_place, to_hours), to_minutes)
marathon = 3 * 60 * 60 + 25 * 60   # 3 hours 25 minutes, in seconds
print(first_way(marathon), second_way(marathon))
```

<details class="dl-answer"><summary>answer</summary>

Both print `3.4`. In both groupings, the machines run in the same order:
`to_minutes`, then `to_hours`, then `to_one_place`. Grouping only
decides which two are joined first, and that does not change what
happens to the number. Maths says composition is associative:
$f \circ (g \circ h) = (f \circ g) \circ h$.

Swapping the order is different. Round first, in seconds, and then
divide, and the answer is no longer rounded to one place:
`to_hours(to_minutes(to_one_place(marathon)))` gives
`3.4166666666666665`. Grouping does not matter; order does.

</details>
