---
title: "Machines that take a number: functions in maths and code — Practice"
practice_for: machines-that-take-a-number
year: "2026-2027"
version: 2026.09.25.2
---

# Machines that take a number: functions in maths and code — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another
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

**2. Make.** In a thunderstorm, the light of the flash reaches you at
once, and the sound comes later. Sound travels about 343 metres each
second in air at 20 °C. So if you count the seconds from the flash to
the thunder, the storm is 343 times that many metres away. Write the
rule in function notation, in kilometres, then as a Python function
`storm_km(seconds)`. How far away is a storm 3 seconds after the flash?

<details class="dl-answer"><summary>answer</summary>

In function notation, with $t$ for the seconds:
$d(t) = \frac{343t}{1000}$, because 1,000 metres make a kilometre.

```python
def storm_km(seconds):
    """Return how far away a storm is, in km, from the seconds between flash and thunder."""
    return 343 * seconds / 1000

print(storm_km(3))
```

This prints `1.029`. That is where the old rule "three seconds for
every kilometre" comes from. This is one way through. Your function may
have other names and do the same job.

</details>

**3. Explain.** In this code, what is the parameter, and what is the
argument?

```python
def colour_bytes(pixels):
    """Return how many bytes a picture needs, at 3 bytes for each pixel."""
    return pixels * 3

print(colour_bytes(4))
```

<details class="dl-answer"><summary>answer</summary>

The parameter is `pixels`: the name in the brackets of the `def` line.
The argument is `4`: the value put into that slot when the function is
called. The parameter is the slot, and the argument is what goes in it.
Call `colour_bytes(9)` and the parameter is still `pixels`, but the
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

Here is one answer. Yours may be different and work too.

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

**7. Fix.** Schlomo, who is learning Python too, has a phone at 20%
charge. It charges 1.5 percentage points every minute. He writes
`charge_after`, and then `minutes_for`, meant to be its inverse: how
many minutes it takes to reach a charge. His test fails. Run it, read
the error, and fix `minutes_for`.

```python exec
id: machines-practice-fix-charge
def charge_after(minutes):
    """Return the phone's charge, in percent, after charging for minutes."""
    return 20 + 1.5 * minutes


def minutes_for(percent):
    """Return how many minutes of charging it takes to reach percent."""
    return percent / 1.5 - 20


assert minutes_for(charge_after(40)) == 40
print("minutes_for undoes charge_after.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. List the steps of `charge_after`, in order: first multiply by 1.5,
   then add 20.
2. To undo them, undo the last step first.
3. What does `minutes_for(80)` give now? Forty minutes of charging
   reach 80%.

**Think about:** putting on socks and then shoes. Which one comes off
first?

**Try this next:** what does `minutes_for(110)` give? Why does that
answer mean nothing?

</details>

<details class="dl-answer"><summary>answer</summary>

Schlomo had the two steps that undo `charge_after`, but in the same
order as `charge_after` does them.
`charge_after` multiplies by 1.5 and then adds 20, so the inverse must
take away 20 first, and then divide by 1.5:

```python
def minutes_for(percent):
    """Return how many minutes of charging it takes to reach percent."""
    return (percent - 20) / 1.5
```

Now `minutes_for(80)` is `40.0`, and the test passes. The old version
gave $80 \div 1.5 - 20$, about 33.3. And `minutes_for(110)` gives 60
minutes for a charge no phone can reach: 110% is outside the range of
`charge_after`, so it is outside the domain of its inverse.

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

Here is one answer. Yours may be different and work too.

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

**10. Fix.** A photo app puts two pictures side by side, each scaled
to 125% of its width, and works out how wide the row is. It stops with
an error. Run it, read the last line of the error, and fix
`scaled_width`.

```python exec
id: machines-practice-fix-width
def scaled_width(width):
    """Return a picture's width, in pixels, scaled to 125%."""
    print(width * 1.25)


row = scaled_width(640) + scaled_width(1024)
print("The row is", row, "pixels wide")
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
`scaled_width` prints its answer, but gives back `None`, and Python
cannot add `None` to `None`. The docstring promised to return the
width, so keep that promise:

```python
def scaled_width(width):
    """Return a picture's width, in pixels, scaled to 125%."""
    return width * 1.25
```

Now the cell prints `The row is 2080.0 pixels wide`. The two numbers the
old version printed, 800.0 and 1280.0, were already the widths we
wanted. Only the handing back
was missing.

</details>

**11. Predict.** Your toolkit's `digit_at` has the parameters
`number`, `place` and `base`, in that order. A display wants the
digits of the year 2026. What does each line print? One of them stops
with an error.

```python
print(digit_at(place=1, number=2026))
print(digit_at(2026, 1, base=2))
print(digit_at(1, 2026))
print(digit_at(number=2026, 1))
```

<details class="dl-answer"><summary>answer</summary>

Python reads the whole cell before it runs any of it, and the last line
is not allowed. So nothing prints at all: the cell stops with
`SyntaxError: positional argument follows keyword argument`.

Take the last line out, and the others print `2`, `1` and `0`. With
keyword arguments, the order in the call does not matter, because each
value names its slot. Without them, the order is everything:
`digit_at(1, 2026)` asks for the digit in place 2026 of the number 1,
which is 0. Once one argument is named, every argument after it must be
named too.

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

Here is one answer. Yours may be different and work too.

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

**13. Make.** In a small network, every computer has its own cable to
every other computer. On [Orders and choices](tutorial:orders-and-choices)
we counted pairs like these with `combinations(computers, 2)`. Now go
backwards: if there are 45 cables, how many computers are there? Write
`computers_for(cables)`, with a `while` loop that tries 2 computers,
then 3, and so on, until `combinations(computers, 2)` reaches `cables`.
Try it on 45. What should it do with 50?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with `computers = 2`.
2. While `combinations(computers, 2)` is less than `cables`, add 1 to
   `computers`.
3. When the loop ends, `combinations(computers, 2)` is `cables` or more.
   Which of the two tells you the answer was in the range?

**Think about:** is `combinations(computers, 2)` one-to-one, for 2 or
more computers? What does that say about the inverse?

**Try this next:** list the numbers of cables that are possible for 2
to 10 computers. Those are the range, and the domain of
`computers_for`.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def computers_for(cables):
    """Return how many computers a network has, if every pair has a cable.

    cables must be a number that some network can have: 1, 3, 6, 10, ...
    """
    computers = 2
    while combinations(computers, 2) < cables:
        computers = computers + 1
    assert combinations(computers, 2) == cables, "no network has that many cables"
    return computers

print(computers_for(45))
print(computers_for(50))
```

The first line prints `10`, because $C(10, 2) = 45$. The second stops
with `AssertionError: no network has that many cables`. Nine computers
need 36 cables and ten need 45, so 50 is not in the range of the cable
function, and not in the domain of its inverse.

Each extra computer adds more cables, never the same number, so the
cable function is one-to-one for 2 or more computers. That is why it has
an inverse at all. It is also why real networks rarely wire every pair:
100 computers would need 4,950 cables.

</details>

**14. Another way.** A clock shows the hours 0 to 11. The function
`later(hour)` gives the time 4 hours on: `(hour + 4) % 12`. Schlomi,
who is learning Python too, says its inverse is "take away 4", and
tries it on 2 o'clock: $2 - 4$ is $-2$. Where does her idea work, and where does it stop
working? Find the space where "take away 4" undoes `later`, and check the inverse with `compose` for every hour.

<details class="dl-answer"><summary>answer</summary>

Schlomi's move is the one that undoes `later`. She tried it on the
number line, not on the clock. On a clock, the
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

**15. Explain.** A file manager turns a size in bytes into kilobytes,
kilobytes into megabytes, and megabytes into a rounded, readable
number. (Here a kilobyte is 1,000 bytes, and a megabyte is 1,000
kilobytes.) Here are three machines joined in two different groupings.
Predict, run, then say why the two answers agree. Would they still agree
if you swapped the order of two of the machines?

```python exec
id: machines-practice-grouping
def to_kilobytes(size_bytes):
    """Return a size in bytes as kilobytes."""
    return size_bytes / 1000


def to_megabytes(size_kilobytes):
    """Return a size in kilobytes as megabytes."""
    return size_kilobytes / 1000


def to_one_place(megabytes):
    """Return a size in megabytes rounded to one decimal place."""
    return round(megabytes, 1)


first_way = compose(to_one_place, compose(to_megabytes, to_kilobytes))
second_way = compose(compose(to_one_place, to_megabytes), to_kilobytes)
photo = 3456789   # the size of one photo, in bytes
print(first_way(photo), second_way(photo))
```

<details class="dl-answer"><summary>answer</summary>

Both print `3.5`. In both groupings, the machines run in the same order:
`to_kilobytes`, then `to_megabytes`, then `to_one_place`. Grouping only
decides which two are joined first, and that does not change what
happens to the number. Maths says composition is associative:
$f \circ (g \circ h) = (f \circ g) \circ h$.

Swapping the order is different. Round first, in bytes, and then
divide, and the answer is no longer rounded to one place:
`to_megabytes(to_kilobytes(to_one_place(photo)))` gives `3.456789`.
Grouping does not matter; order does.

</details>
