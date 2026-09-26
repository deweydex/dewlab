---
title: "Machines that take a number: functions in maths and code"
year: "2026-2027"
version: 2026.09.25.2
covers:
  a-machine-with-one-slot:
    covers: [MIT-3.1]
    touches: [PDP-LO8]
  what-goes-in-and-what-comes-out:
    covers: [MIT-3.1]
    touches: [PDP-LO9]
  an-algorithm-is-a-function-too:
    covers: [MIT-6.2]
    touches: [PDP-LO6]
  functions-that-give-back-and-procedures-that-do:
    covers: [PDP-LO8]
  running-it-backwards-the-inverse:
    covers: [MIT-3.1]
  machines-in-a-row-composition:
    covers: [MIT-3.1, PDP-LO8]
---

# Machines that take a number: functions in maths and code

A weather station, a phone and a 3D printer all know the temperature.
But the small chip that senses it knows nothing about degrees. It gives
out a voltage, and a rule turns that voltage into a temperature. The
rule takes one number in and gives one number out. That is a function.

Here is the question for this page. Give the rule a voltage the chip
could never make, and it answers −350 °C. That is colder than anything
in the universe can be. What went wrong, and whose job was it to stop
it?

On this page we:

- write one rule as a function in maths and in Python, and see that the
  two are the same idea
- ask which inputs a function accepts, and which outputs it can give
- see an algorithm as a function on a set of inputs
- tell a function that gives back a value from one that only does
  something
- run a function backwards, with its inverse
- join two functions into one, and add `compose` to the toolkit

> **The space we're in.** Most functions on this page take one number
> and give one number back. We work in the real numbers, $\mathbb{R}$,
> where no number squares to make a negative one. Python gives us `def`
> and `return`, which we met on
> [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
> One thing usually goes unsaid: Python never checks that a function
> keeps its promise. The docstring says the promise, and tests check it.

## Warm-up

Two questions from earlier pages. The first is from
[Doing it again](tutorial:doing-it-again), and the second from
[Orders and choices](tutorial:orders-and-choices).

```question
id: machines-warm-up-1
type: fill-in-the-blank

We start with `total = 0`. Then the loop `for day in range(7):` adds 3
to `total` each time round. When the loop ends, `total` is {21}.
```

```question
id: machines-warm-up-2
type: multiple-choice
answer: 3

Your toolkit's `factorial` promises the number of orders of `n`
different things. What does `factorial(4)` give back?

- 4
  - 4 is how many things there are, not how many orders they can go in.
- 10
  - This is 4 + 3 + 2 + 1: adding, where factorial multiplies.
- 24
  - 4 × 3 × 2 × 1: four choices for the first place, three for the next, and so on.
- 16
  - This is 4 × 4, which lets one thing appear twice in the same order.
```

## A machine with one slot

Picture a machine with a slot and a tray. You put a number in the
slot, the machine follows its rule, and a number drops into the tray.
The same number in always gives the same number out.

A common temperature chip, the TMP36, gives out 0.5 volts at 0 °C, and
0.01 volts more for every degree warmer. (A *volt* measures the push
behind an electric current.) So
to get the temperature, multiply the voltage by 100, then take away 50.

Maths writes that rule like this:

$$f(x) = 100x - 50$$

We read $f(x)$ as "f of x". The letter $f$ is the function's name, $x$
stands for the input, and the right-hand side is the rule. So $f(0.75)$
means "put 0.75 in the slot": $f(0.75) = 100 \times 0.75 - 50 = 25$.
Writing a function this way is called *function notation*.

Python writes the same rule with `def`. Before you run the cell, what
will each line show?

```python exec
id: machines-slot-1
def sensor_celsius(volts):
    """Return the temperature in °C that a TMP36 chip reads as volts."""
    return 100 * volts - 50

print(sensor_celsius(0.75))
print(sensor_celsius(0.5))
```

The cell shows `25.0` and `0.0`: a warm room, and freezing. Put the two
versions side by side, and every part of one has a partner in the
other:

| | Maths | Python |
|---|---|---|
| the function's name | $f$ | `sensor_celsius` |
| the input's name | $x$ | `volts` |
| the rule | $100x - 50$ | `100 * volts - 50` |
| using it on 0.75 | $f(0.75)$ | `sensor_celsius(0.75)` |

They are one idea, written two ways. In maths, a function is a rule that gives exactly
one output for each input. A Python function that takes a number and
returns a number keeps the same promise.

Two words help us talk about the slot. On
[Recipes are algorithms](tutorial:recipes-are-algorithms) we met the
parameter: the name in the brackets of the `def` line, here `volts`.
The value we put in when we call the function, here `0.75`, is the
*argument*. The parameter is the slot, and the argument is what goes
into it.

### Your turn

Another chip, the LM35, gives out 0 volts at 0 °C, and 0.01 volts more
for every degree.

1. Change the rule in the cell below to the LM35's.
2. Before you run it, work out what 0.25 volts means for this chip.
3. Add a line that prints `lm35_celsius(0)`. Why is it different from
   the TMP36 at 0 volts?

```python exec
id: machines-slot-your-turn
def lm35_celsius(volts):
    """Return the temperature in °C that an LM35 chip reads as volts."""
    return 100 * volts - 50   # change this to the LM35's rule

print(lm35_celsius(0.25))
```

## What goes in and what comes out

Can we put any number in the slot? Python will run
`sensor_celsius(-3)` without a word of complaint, and give back
`-350`. The chip never gives out −3 volts, and nothing can be −350 °C.
Python followed the rule. The rule did not know which numbers it was
meant for.

<aside class="dl-note" id="machines-note-absolute-zero">

**The coldest there is.** Nothing can be colder than −273.15 °C, called
*absolute zero*. Scientists measure from there with the kelvin scale,
where absolute zero is 0 K. So −350 °C is not a very cold day. It is a
temperature that does not exist.

</aside>

The *domain* of a function is the set of inputs it accepts. The *range*
is the set of outputs it can give. The TMP36 works from −40 °C to
125 °C, so for our rule:

- the domain is every voltage from 0.1 to 1.75 volts;
- the range is every temperature from −40 °C to 125 °C.

Some functions in Python do check their domain. Here is one. The
*square root* of a number is the number that, multiplied by itself,
makes it. The square root of 16 is 4, because $4 \times 4 = 16$. We
write it $\sqrt{16}$, and Python keeps it in the `math` module as
`math.sqrt`.

What do you think each line will do? The last line is meant to stop
with an error.

```python exec
id: machines-domain-1
import math

print(math.sqrt(16))
print(math.sqrt(2))
print(math.sqrt(-4))
```

The first two lines show `4.0` and `1.4142135623730951`. Now read the
last line of the error, as we did on
[When Python says no](tutorial:when-python-says-no):

`ValueError: math domain error`

Python uses the mathematician's own word. A *ValueError* means the value
was the right kind of thing, a number, but outside what the function
accepts. That is different from a `TypeError`, which means the wrong
kind of thing altogether.

So is asking for $\sqrt{-4}$ a foolish move? No. It has no answer in
$\mathbb{R}$, because every real number, multiplied by itself, gives 0
or more. Unit 7 builds a bigger space where $-4$ does have a square
root. The move is fine; it needs a different space.

Our own function can say its domain too. The docstring says it in
words, and an `assert` at the top checks it, with `between` from your
toolkit. After the comma, an `assert` can carry a message, which Python
shows if the check fails. The last line of this cell is meant to stop
with an error.

```python exec
id: machines-domain-2
def sensor_celsius(volts):
    """Return the temperature in °C that a TMP36 chip reads as volts.

    volts must be from 0.1 to 1.75, the voltages the chip can give.
    """
    assert between(volts, 0.1, 1.75), "a TMP36 gives 0.1 to 1.75 volts"
    return 100 * volts - 50

print(sensor_celsius(0.75))
print(sensor_celsius(-3))
```

This time the last line of the error is
`AssertionError: a TMP36 gives 0.1 to 1.75 volts`. So the answer to the
question at the top is: the function's job, once its promise names its
domain. The message helps whoever calls the function next, and that is
often you, a few weeks later.

```question
id: machines-range-round
type: multiple-choice
answer: 2

`round(x)` accepts any real number $x$ and rounds it to the nearest
whole number. What is its range?

- every real number
  - This is the domain, what may go in; what comes out is always whole.
- the whole numbers, the integers
  - Whatever goes in, a whole number comes out, and every whole number can come out.
- the numbers from 0 to 9
  - These are the digits; `round(123.4)` gives 123, which is outside 0 to 9.
```

## An algorithm is a function too

On [Doing it again](tutorial:doing-it-again) we added up
$1 + 2 + \dots + n$ in two ways. A loop added the numbers one at a time.
Gauss's trick paired the ends, and gave

$$1 + 2 + \dots + n = \frac{n(n + 1)}{2}$$

Let's write both ways as functions, and look at them as machines. Will
they agree for 100?

```python exec
id: machines-algorithm-1
def sum_by_loop(n):
    """Return 1 + 2 + ... + n, adding one number at a time.

    n is a whole number, 0 or more.
    """
    running_total = 0
    for number in range(1, n + 1):
        running_total = running_total + number
    return running_total


def sum_by_formula(n):
    """Return 1 + 2 + ... + n, using n(n + 1) / 2.

    n is a whole number, 0 or more.
    """
    # n(n + 1) is always even, so // loses nothing and keeps an int.
    return n * (n + 1) // 2


print(sum_by_loop(100), sum_by_formula(100))
```

Both give 5050. Inside, one makes a hundred additions, and the other
one multiplication and one division. But from the outside, as machines, the two cannot be told
apart: the same input always gives the same output.

This is how mathematicians think of an algorithm. An algorithm, the list
of clear steps we met on
[Four questions for any puzzle](tutorial:four-questions), is a function
on a domain of inputs: for each input it is built for, it gives one
output. The function says what comes out. The algorithm says how we get
there. Two algorithms can be one function.

Let's check that on a lot of the domain at once. How long do you expect
it to take?

```python exec
id: machines-algorithm-2
for n in range(0, 1001):
    assert sum_by_loop(n) == sum_by_formula(n)
print("They agree for every n from 0 to 1000.")
```

Every check passed. Now let's try an input from outside the domain. "Add up the whole numbers from 1 to −5" does
not mean anything. What will each function do with it?

```python exec
id: machines-algorithm-3
print(sum_by_loop(-5), sum_by_formula(-5))
```

The loop gives `0`, because `range(1, -4)` is empty. The formula gives
`10`. Outside the domain the two machines disagree, and neither answer
means anything, because the question has no answer. That is why the domain
belongs in the promise: both promised the same thing, for whole numbers
from 0 up, and both kept it.

## Functions that give back, and procedures that do

Not every function hands back a value. Some do a job instead: they
print a line, draw a picture or save a file. Here is one. What will the
last line show?

```python exec
id: machines-procedure-1
def show_reading(volts):
    """Print a sensor reading: the voltage, and the temperature it means."""
    print("Sensor voltage:", volts)
    print("Temperature in °C:", sensor_celsius(volts))


result = show_reading(0.75)
print("show_reading gave back:", result)
```

The reading appears, and then `show_reading gave back: None`. *None* is
Python's value for "nothing here". A function with no `return` line
gives back `None` when it finishes.

A *procedure* is a function that does a job, such as printing, instead
of giving back a value. Python writes both with `def`. Some older
languages, such as Pascal, use two different words for them. The
difference matters when we build with them. `sensor_celsius(0.75) + 2`
is a number we can use. `show_reading(0.75) + 2` asks Python to add
`None` and 2, and stops with a `TypeError`.

Look at how `show_reading` gets its temperature. It does not work it
out again: it calls `sensor_celsius`. Splitting a program into small
functions, each with one job, is called *modularisation*. Swap the
TMP36 for another chip, change `sensor_celsius`, and every reading is
right at once.

A call can also name its arguments. `sensor_celsius(volts=0.75)` puts
0.75 into the slot called `volts`. This is a *keyword argument*, and it
helps most when a function has several slots. Your toolkit's `digit_at`
has three. Say a display is to show 5050, the sum from 1 to 100. Before
you run this, which digit will each line give?

```python exec
id: machines-procedure-2
print(digit_at(sum_by_loop(100), 3))
print(digit_at(sum_by_loop(100), place=1, base=2))
```

The first line gives 5, the digit in the thousands place. The second
gives 1: in binary, 5050 is `1001110111010`, and its bit in place 1 is
1. Look at the order of events. Python works out `sum_by_loop(100)`
first, and gets 5050. Only then does that number go into `digit_at`.
The inside of the brackets happens before the outside, as it did with
`print(1920 * 1080)` on the first page of this course.

## Running it backwards: the inverse

The display says 25 °C. What voltage did the chip give out?

The rule did two things, in order: multiply by 100, then take away 50.
To go backwards, undo each step in the opposite order. First add 50,
then divide by 100:

$$f^{-1}(y) = \frac{y + 50}{100}$$

We read $f^{-1}$ as "f inverse". The *inverse* of a function is a
function that undoes it: if $f$ takes $x$ to $y$, then $f^{-1}$ takes
$y$ back to $x$. The −1 here is a name, not a power.

What will these three lines show? The second and third put one machine's
output into the other's slot.

```python exec
id: machines-inverse-1
def volts_for(celsius):
    """Return the voltage a TMP36 gives out at this temperature in °C."""
    return (celsius + 50) / 100

print(volts_for(25))
print(volts_for(sensor_celsius(1.25)))
print(sensor_celsius(volts_for(-10)))
```

The answers are `0.75`, `1.25` and `-10.0`. Going forward and then back
lands where we started, whichever way round we go. Notice that the
domain of `volts_for` is the range of `sensor_celsius`. −60 °C is not in
that range, and `volts_for(-60)` gives −0.1 volts, which the chip can
never give. A later page in this unit,
[Running a formula backwards](tutorial:running-a-formula-backwards),
undoes formulas in general, one step at a time.

Does every function have an inverse? Try squaring. What will each line
show?

```python exec
id: machines-inverse-2
import math

def square(x):
    """Return x multiplied by itself."""
    return x * x

print(square(3), square(-3))
print(math.sqrt(square(3)), math.sqrt(square(-3)))
```

Both 3 and −3 square to 9. So if the tray shows 9, which number went in?
There is no way to know, and an inverse must give one answer. The square
root chooses 3, which undoes the square for 3 but not for −3.

A function has an inverse only when each output comes from exactly one
input. Such a function is called *one-to-one*. Squaring on all of
$\mathbb{R}$ is not one-to-one. But on a smaller space, the numbers from
0 up, it is, and there $\sqrt{x}$ is its inverse. A move that fails in
one space can work in another. This time the space that works is
smaller.

```question
id: machines-inverse-round
type: multiple-choice
answer: 3

Does `round` have an inverse?

- Yes: add 0.5 to the answer.
  - Adding 0.5 to 2 gives 2.5, but 2.4 and 1.6 both went in to give that 2.
- Yes: `round` is its own inverse.
  - `round(round(2.4))` is 2, not 2.4: rounding again does not bring back what went in.
- No: `round(2.4)` and `round(1.6)` both give 2, so 2 cannot say which went in.
  - An inverse has to say which input gave each output, and 2 came from more than one.
```

## Machines in a row: composition

A small computer board, such as an Arduino, cannot read a voltage
directly. It turns the voltage into a whole number from 0 to 1023: 10
bits, so $2^{10} = 1024$ possible readings. Each step up is
$\frac{5}{1024}$ of a volt. So a reading goes through two machines:
first reading to volts, then volts to °C.

Earlier on this page, `digit_at(sum_by_loop(100), 3)` sent the output
of one machine straight into the slot of the next. Joining two
functions this way is called *composition*. Maths writes "g after f"
as

$$(g \circ f)(x) = g(f(x))$$

The small circle is read "after", and it is a reminder that $f$ runs
first, even though it is written second. What temperature is a reading
of 154? And what happens if the two machines swap places?

```python exec
id: machines-compose-1
def reading_volts(reading):
    """Return the voltage for a board's reading, a whole number from 0 to 1023."""
    return reading * 5 / 1024

print(sensor_celsius(reading_volts(154)))
print(reading_volts(sensor_celsius(0.75)))
```

The first line gives about 25.2 °C. Now look at the second. Python ran
the machines the other way round without a word, and gave about 0.12.
That number means nothing: it treats a temperature as a board's
reading. The same two machines, in a different order, do a different
job, or no job at all. That is sequence, the third of our four
questions: what happens when?

### Your turn: a tool that joins machines

Your toolkit already takes functions as inputs: `truth_table` was given
a rule. `compose` goes one step further. It takes two functions and
gives back a new function. Here is its promise:
`compose(outer, inner)` is a function that, given `x`, returns
`outer(inner(x))`.

Replace the `...` with three lines:

1. Inside `compose`, start a new function with `def both(x):`, pushed
   in one level.
2. Inside `both`, pushed in one more level, return `outer(inner(x))`.
3. Back at the level of `def both`, write `return both`, with no
   brackets after `both`. The brackets would call it; without them, we
   hand over the function itself.

```python exec
id: machines-toolkit
toolkit: yes
def compose(outer, inner):
    """Return a new function that runs inner on its input, then outer on the result.

    compose(outer, inner)(x) gives the same answer as outer(inner(x)).
    """
    ...
```

```python toolkit-reference
for: machines-toolkit
def compose(outer, inner):
    """Return a new function that runs inner on its input, then outer on the result.

    compose(outer, inner)(x) gives the same answer as outer(inner(x)).
    """
    def both(x):
        return outer(inner(x))
    return both
```

```hint
What does `compose(sensor_celsius, square)` give back at the moment?
Try `print(compose(sensor_celsius, square))` on its own. A function you can call is
shown as `<function ...>`.
```

```hint
after: 10 errors
title: some steps
1. The first line under the docstring is `def both(x):`, pushed in as
   far as the docstring.
2. The line under that is pushed in one level further, and starts with
   `return`.
3. The last line is back at the level of `def both(x):`, and gives
   back `both`.

**Think about:** why `return both` and not `return both(x)`? Which one
hands back a machine, and which one hands back a number?
```

Now the tests. Until `compose` is written, the first test stops with an
error. That is the test doing its job. What do you notice about the
third test?

```python exec
id: machines-toolkit-tests
reading_celsius = compose(sensor_celsius, reading_volts)
assert reading_celsius(154) == sensor_celsius(reading_volts(154))
assert compose(sensor_celsius, volts_for)(25) == 25
assert compose(volts_for, sensor_celsius)(0.75) == 0.75
assert compose(math.sqrt, square)(-3) == 3
print("compose keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

Here is one way through. Yours may use other names inside and do the
same job.

```python
def compose(outer, inner):
    """Return a new function that runs inner on its input, then outer on the result.

    compose(outer, inner)(x) gives the same answer as outer(inner(x)).
    """
    def both(x):
        return outer(inner(x))
    return both
```

</details>

The third test joins `sensor_celsius` to its own inverse, and 0.75
comes straight back out. That is one way to say what an inverse is:
$f^{-1}(f(x)) = x$ for every $x$ in the domain. The last test is the
square root failing to undo squaring: −3 went in, and 3 came out.

One thing may seem strange. `both` is made inside `compose`, and still
knows `outer` and `inner` after `compose` has finished. If that is hard
to picture, it is fine to take it on trust for now: a later page in this
unit, [What a function can see](tutorial:what-a-function-can-see),
explains how.

### Your turn

1. Use `reading_celsius` from the tests on the readings 102, 205 and
   300. Before you run it, which one is close to freezing?
2. Use `compose` to make `lm35_reading_celsius`, for a board with the
   LM35 chip from the first Your turn. What does a reading of 51 give?

```python exec
id: machines-compose-your-turn
# Your readings, and the other order
```

<details class="dl-why"><summary>Why this way?</summary>

This page showed a function as a machine with a slot and a tray.
Mathematicians define a function another way: as a set of pairs, each
input paired with exactly one output, with no machine in sight.

The set of pairs is the definition a university course would use. It
covers functions no machine could ever run, and it makes proofs exact.

We used the machine because it answers "what is promised?" with a
picture you can keep in your head. It also fits Python, where `def` does
build something you put values into. The picture has a cost. It hides
the fact that a function is only its pairs, and that fact is why two
different machines, the loop and Gauss's formula, could be one
function.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a function ($f$, `sensor_celsius`), its input ($x$, `volts`), and the value put in, the argument |
| What is promised? | one output for each input in the domain; an inverse promises to undo; `compose` promises a new function |
| What happens when? | the inside of the brackets first; in $g(f(x))$, $f$ runs first; the order of two machines can change the answer |
| What does this space let us do? | the domain says which inputs are allowed; $\sqrt{-4}$ needs a bigger space; squaring has an inverse only on a smaller one |

## What we have now

| Term | What it means |
|---|---|
| $f(x)$ | function notation: the function $f$, used on the input $x$ |
| argument | the value put into a parameter when a function is called |
| domain, range | the inputs a function accepts; the outputs it can give |
| `math.sqrt(x)` | the square root of $x$: the number that, times itself, makes $x$ |
| `ValueError` | the right kind of value, but outside what the function accepts |
| `assert condition, "message"` | a check that shows a message when it fails |
| algorithm as a function | for each input in its domain, one output; two algorithms can be one function |
| procedure, `None` | a function that does a job and gives back nothing; Python's value for nothing |
| modularisation | splitting a program into small functions, each with one job |
| keyword argument | naming the slot in a call: `sensor_celsius(volts=0.75)` |
| inverse, $f^{-1}$ | the function that undoes $f$ |
| one-to-one | each output comes from exactly one input; only these have inverses |
| composition, $g \circ f$ | $g(f(x))$: the output of $f$ goes into $g$ |
| `compose(outer, inner)` | your toolkit function that joins two machines into one |

## Where to read more

CrashCourse (2017). *Programming Basics: Statements & Functions: Crash
Course Computer Science #12.*
<https://www.youtube.com/watch?v=l26oaHV7D40>. Functions in code, built up
for a small game: a name, what goes in, and the value that comes back.
About eleven minutes.
