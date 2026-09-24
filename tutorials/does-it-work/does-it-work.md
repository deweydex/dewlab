---
title: "Does it work? Testing, walkthroughs and naming"
year: "2026-2027"
version: 2026.09.24.1
covers:
  code-that-runs-and-code-that-works:
    covers: [PDP-LO10]
  close-enough:
    covers: [PDP-LO10]
    touches: [MIT-1.4]
  a-walkthrough-by-hand:
    covers: [PDP-LO10]
  stepping-through-with-a-debugger:
    covers: [PDP-LO10]
  names-and-comments-a-stranger-can-read:
    covers: [PDP-LO11]
  your-toolkit-reviewed:
    covers: [PDP-LO10, PDP-LO11]
---

# Does it work? Testing, walkthroughs and naming

An American recipe says to bake a cake at 350 °F. A friend's cooking app
turns that into Celsius, and says 332 °C. Most home ovens do not even go
that high. The app did not crash, and it showed no error message. It
gave a wrong answer, calmly.

So how would anyone have known, before the cake burned? When you write a
function, how do you know it is right?

On this page we:

- test a function against answers we already know
- build `close_enough`, for testing with floats
- walk through a function by hand, with a table of names and values
- watch a debugger step through the same function, one line at a time
- read code for its names and comments, the way a stranger would
- run a test for every tool in your toolkit, all at once

> **The space we're in.** Python checks that code is written in valid
> Python, and then it runs it. It never checks that a function keeps its
> promise. A docstring says the promise, and nothing but a test checks
> it. That goes unsaid a lot: code that runs is not always code that
> works. Your toolkit is loaded, including the temperature and travel
> tools from
> [Running a formula backwards](tutorial:running-a-formula-backwards).

## Warm-up

Two questions from earlier pages. The first is from
[Running a formula backwards](tutorial:running-a-formula-backwards), and
the second from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).

```question
id: does-it-warm-up-1
type: fill-in-the-blank

To undo "multiply by 9/5, then add 32", the first step is to
{subtract 32|multiply by 5/9|divide by 32}.
```

```question
id: does-it-warm-up-2
type: multiple-choice
correct: 2

What happens when Python runs `assert 2 + 2 == 4`?

- It shows `True`.
- Nothing at all.
- It stops with an `AssertionError`.
```

## Code that runs and code that works

Here is the converter from the cooking app. Before you run it, read the
last line of the function. What do you think it will print for 350 °F?

```python exec
id: does-it-runs-1
def oven_celsius(fahrenheit):
    """Return an oven temperature in degrees Celsius, given it in degrees Fahrenheit."""
    return fahrenheit - 32 * 5 / 9

print(oven_celsius(350))
```

It prints about 332.2, with no error. Python did exactly what the line
says: it multiplied first, then subtracted. The code runs. It does not
work, because it breaks its promise.

A mistake in code that makes it break its promise is called a *bug*.
Python cannot find this kind of mistake for us, because Python does not
know what we meant. So we check. *Testing* is running code on inputs
where we already know what the promise says it should give, and
comparing. One input with its expected output is a *test case*.

Where do the expected answers come from? There are three good places.

1. **Facts from outside the code.** Water freezes at 32 °F, which is
   0 °C, and boils at 212 °F, which is 100 °C. We know these without
   the function.
2. **A second route.** A function and its inverse should undo each
   other. Going there and back should change nothing.
3. **The edges of the promise.** Mistakes often hide at the smallest
   and largest inputs the promise allows, and at zero and negative
   numbers.

On [Machines that take a number](tutorial:machines-that-take-a-number),
an `assert` could carry a message after a comma. Here are two test
cases with messages. The cell is meant to stop with an error, because
the function has a bug. Which test do you think fails first?

```python exec
id: does-it-runs-2
assert oven_celsius(32) == 0, "water freezes at 32 °F, which is 0 °C"
assert oven_celsius(212) == 100, "water boils at 212 °F, which is 100 °C"
print("oven_celsius keeps its promise.")
```

The first test fails, and the last line of the traceback shows its
message. A test with a message says what the promise was, as well as
where it broke.

### Your turn

1. Fix `oven_celsius` in the first cell of this section. The formula is
   on the last page: subtract 32 first.
2. Run the first cell again, then run the tests. Do both pass now?
3. Add a third test: the one temperature where both scales agree is
   −40.

## Close enough

The last page found that going there and back with the temperature tools
gives back `0.9999999999999984` for 1 °C. The functions are right. The
float is very close to 1, but not equal to it, so `==` says `False`. The
last page rounded to 9 places before comparing. That works, but it hides
the question we are really asking: how far apart are these two numbers?

On [How likely is it?](tutorial:how-likely-is-it) we met `abs()`, which
gives the size of a number without its sign. So `abs(a - b)` is the
distance between `a` and `b`, whichever one is bigger. Two numbers are
close enough when that distance is no bigger than some small *tolerance*:
the largest difference we are willing to call "equal".

The default tolerance below is written `1e-9`. This is Python's way of
writing $1 \times 10^{-9}$, which is 0.000000001, one billionth. The `e`
means "times 10 to the power".

Here is the last tool of this unit's toolkit. Can you write its one line?

```python exec
id: does-it-toolkit
toolkit: yes
def close_enough(a, b, tolerance=1e-9):
    """Return True when a and b differ by no more than tolerance.

    tolerance is the largest difference that still counts as equal.
    The order of a and b does not matter.
    """
    ...
```

```python toolkit-reference
for: does-it-toolkit
def close_enough(a, b, tolerance=1e-9):
    """Return True when a and b differ by no more than tolerance.

    tolerance is the largest difference that still counts as equal.
    The order of a and b does not matter.
    """
    return abs(a - b) <= tolerance
```

A tool for testing needs tests of its own. Each test case below was
chosen for a reason. Look at the last two. Why test both orders? Until
your `close_enough` is written, this cell stops with an error.

```python exec
id: does-it-toolkit-tests
assert close_enough(0.1 + 0.2, 0.3), "the float is very close to 0.3"
assert not close_enough(1, 1.001), "0.001 is bigger than a billionth"
assert close_enough(1, 1.001, tolerance=0.01), "0.001 is smaller than 0.01"
assert not close_enough(5, 1), "5 and 1 are far apart"
assert not close_enough(1, 5), "1 and 5 are far apart, in either order"
print("close_enough keeps its promise.")
```

```hint
What is `1 - 5`? What is it without its sign? Which of those two do you
want to compare with the tolerance?
```

The last test is there because of a real, common bug. Without `abs()`,
`1 - 5` is −4, and −4 is smaller than any tolerance, so two numbers far
apart would count as "close". The test in one order would pass, and the
test in the other order catches it.

Now the tool can do real work. The next cell tests the temperature
tools on every whole number of degrees from −50 to 100. That is 151 test
cases, and nobody had to work out a single expected answer by hand. It
needs your `close_enough`. What do you expect it to print?

```python exec
id: does-it-close-1
count = 0
for celsius in range(-50, 101):
    there_and_back = fahrenheit_to_celsius(celsius_to_fahrenheit(celsius))
    assert close_enough(there_and_back, celsius), celsius
    count = count + 1
print(count, "round trips, all close enough.")
```

The message after the comma is `celsius` itself, so a failure would name
the temperature that went wrong.

## A walkthrough by hand

Tests tell us that something is wrong. They do not always tell us why.
Here is a function for a weather app. It finds the warmest temperature
in a list of readings, and it passes a test with summer readings. Before
you run it, what should it give for three January nights in Mullingar:
−3, −1 and −4 degrees? What will it give?

```python exec
id: does-it-walk-1
def warmest(readings):
    """Return the highest temperature in readings, a list of at least one number."""
    warmest_so_far = 0
    for reading in readings:
        if reading > warmest_so_far:
            warmest_so_far = reading
    return warmest_so_far

print(warmest([12, 15, 9]))
print(warmest([-3, -1, -4]))
```

The summer test gives 15, which is right. The January test gives 0, but
none of the nights was 0 degrees. The warmest was −1.

To find out why, let's be the computer. A *walkthrough*, or *trace*, is
running code by hand, one line at a time, writing down every name and
its value as it changes. The table we write it in is a *trace table*.
Each row is one step: the line about to run, and the value of each name
at that moment. Here is the trace for `warmest([-3, -1, -4])`.

| Step | Line about to run | `reading` | `warmest_so_far` |
|---|---|---|---|
| 1 | `warmest_so_far = 0` | | |
| 2 | `for reading in readings:` | | 0 |
| 3 | `if reading > warmest_so_far:` | −3 | 0 |
| 4 | `for reading in readings:` | −3 | 0 |
| 5 | `if reading > warmest_so_far:` | −1 | 0 |
| 6 | `for reading in readings:` | −1 | 0 |
| 7 | `if reading > warmest_so_far:` | −4 | 0 |
| 8 | `for reading in readings:` | −4 | 0 |
| 9 | `return warmest_so_far` | −4 | 0 |

At step 3, is −3 bigger than 0? No. At step 5, is −1 bigger than 0? No.
The `if` is never true, so `warmest_so_far` stays at 0 all the way down
its column. The column shows the bug: the starting value, 0, is bigger
than every reading.

Ask the fourth question. Starting at 0 is a guess from a different
space. For heights or prices, which are never below 0, it works. For
temperatures in Ireland in January, it does not. A better start is a
real reading: the first one, `readings[0]`. The docstring already
promises at least one reading, so there always is a first one.

A walkthrough also has a second meaning, in a team. A *structured
walkthrough* is a meeting where the person who wrote some code talks a
small group through it, line by line. The others follow along, ask
questions, and look for mistakes. Explaining code out loud to another
person finds bugs surprisingly often, sometimes before anyone has
asked a single question.

### Your turn

1. Make a trace table for `warmest([12, 15, 9])` on paper, with the same
   four columns. How many rows does it need?
2. In which rows does `warmest_so_far` change?
3. Fix `warmest` in the cell above so it starts from `readings[0]`, and
   run it again. Does the January test now give −1?

## Stepping through with a debugger

Writing a trace table by hand is slow, but it makes you look at every
line. A tool can write the same table for us.

A *debugger* is a tool that runs a program one line at a time, pausing
so you can see the value of every name. In an editor such as Thonny or
VS Code, you click beside a line to set a *breakpoint*: a line where the
program will pause. Then a "step" button runs one more line, and a
panel shows every name and its value. Stepping through a function this
way is called *step-through*.

The Python on this page has no debugger buttons. So here is a small one,
`step_through`, built from the same part of Python that real debuggers
use. You do not need to read how it works. What it does is enough:
before each line runs, it shows the line and every name the function can
see.

```python exec
id: does-it-debugger-1
import sys
import linecache


def step_through(function, *inputs):
    """Run function on inputs one line at a time, like a debugger.

    Before each line runs, show it with every name the function can see.
    At the end, show what the function gives back.
    """
    code = function.__code__

    def watch(frame, event, result):
        if frame.f_code is not code:
            return None
        if event == "line":
            line = linecache.getline(code.co_filename, frame.f_lineno).strip()
            names = "  ".join(f"{name}={value!r}" for name, value in frame.f_locals.items())
            print(f"{line:<32}| {names}")
        elif event == "return":
            print("gives back", repr(result))
        return watch

    sys.settrace(watch)
    try:
        function(*inputs)
    finally:
        sys.settrace(None)
```

Here is a copy of the first `warmest`, with its bug, so that you can
compare the debugger's steps with the trace table above. How many lines
do you expect before "gives back"?

```python exec
id: does-it-debugger-2
def warmest_first_try(readings):
    """Return the highest temperature in readings, a list of at least one number."""
    warmest_so_far = 0
    for reading in readings:
        if reading > warmest_so_far:
            warmest_so_far = reading
    return warmest_so_far

step_through(warmest_first_try, [-3, -1, -4])
```

Nine lines, then `gives back 0`. They are the nine rows of the trace
table, in the same order, with the same values. The debugger also shows
`readings` on every line, because the function can see that name too.

Here is the same function with the fix from the last section: it starts
from the first reading, `readings[0]`. Before you run it, in which steps
will `warmest_so_far` change?

```python exec
id: does-it-debugger-3
def warmest_second_try(readings):
    """Return the highest temperature in readings, a list of at least one number."""
    warmest_so_far = readings[0]
    for reading in readings:
        if reading > warmest_so_far:
            warmest_so_far = reading
    return warmest_so_far

step_through(warmest_second_try, [-3, -1, -4])
```

It starts at −3, the first reading, and changes once, when −1 arrives.
It gives back −1.

A trace by hand and a debugger show the same thing. The hand trace makes
you predict each value before you see it, which is where you learn. The
debugger is faster, and it cannot make a mistake copying a value. Most
programmers use both.

### Your turn

1. Step through `warmest_second_try` with the summer readings,
   `[12, 15, 9]`. Do the steps match your trace table from the last
   section?
2. Step through `celsius_to_fahrenheit` with 20. How many lines does it
   run? A debugger steps a whole line at a time, so what can it not show
   you about the order of `*`, `/` and `+` inside that line?

## Names and comments a stranger can read

A test checks that code works. It does not check that anyone else can
read it. Here is a function that works. What do you think it does?

```python exec
id: does-it-names-1
def f(a, b):
    c = a * b / 100
    return a + c  # add c to a

print(f(84, 10))
print(f(50, 23))
```

It is hard to say. It adds a percentage to an amount, and that could be
a tip, or VAT, or a price rise. The comment, "add c to a", says only
what the code already says. Here is the same function with new names, a
docstring, and no comment. Which version would you rather find in your
toolkit in six months?

```python exec
id: does-it-names-2
def add_percent(amount, percent):
    """Return amount with percent per cent added, as for a tip or VAT."""
    extra = amount * percent / 100
    return amount + extra

for amount, percent in [(84, 10), (50, 23), (19.99, 0)]:
    assert add_percent(amount, percent) == f(amount, percent)
print("The two versions agree.")
```

The tests show that renaming changed nothing for Python. Python does not
read names. People do.

A team usually writes down how its code should look, so that everyone's
code reads the same way. A *coding standard* is a set of agreed rules
for how code is written: names, comments, indentation and layout.
Python's own standard is called PEP 8. Here are the parts that matter
most so far.

- **Names are words that say what a value is.** `total_minutes`, not
  `tm` or `x`. A function is named for what it gives back or what it
  does: `add_percent`, `travel_time`. Python names are written in small
  letters, with underscores between words, like `warmest_so_far`.
- **A comment says why, not what.** The code already says what it does.
  A comment earns its place when it says something the code cannot: a
  reason, or a warning. In `warmest`, a useful comment would be
  `# start from a real reading, since a temperature can be below 0`.
- **Indentation is four spaces for each level.** Python needs the
  indentation to be the same through a block, or it stops with an
  `IndentationError`, which we met on
  [When Python says no](tutorial:when-python-says-no). PEP 8 says to
  use four spaces.

There is one more rule, and it matters most when code changes. A comment
that no longer matches the code is worse than no comment at all, because
a reader will believe it.

```question
id: does-it-names-3
type: multiple-choice
correct: 3

A line in a shopping app is `total = total * 0.9`. Which comment is the
most useful?

- `# multiply total by 0.9`
- `# change the total`
- `# members get 10% off`
```

## Your toolkit, reviewed

Your toolkit now has functions from every page of this course. A set of
tests kept together, so that they can all be run at once, is a *test
suite*. Here is one for your toolkit, with a few test cases for each
tool. Some of its tests use `close_enough`, so write that first. What
do you expect it to print?

```python exec
id: does-it-review-1
def test_toolkit():
    """Run a few test cases for each toolkit function, and say how many passed."""
    tests = [
        split_bill(84, 4, 10) == 23.1,
        to_binary(5) == "101",
        to_hex(255) == "FF",
        between(18, 18, 65),
        not between(17, 18, 65),
        parity_bit([1, 0, 1, 1]) == 1,
        total([3.20, 0, 3.50]) == 6.7,
        factorial(5) == 120,
        compose(fahrenheit_to_celsius, celsius_to_fahrenheit)(20) == 20,
        close_enough(circle_area(1), 3.141592653589793),
        distance_travelled(80, 3) == 240,
        close_enough(travel_time(208, 80), 2.6),
        close_enough(0.1 + 0.2, 0.3),
    ]
    for number, passed in enumerate(tests, start=1):
        assert passed, "test " + str(number) + " failed"
    return len(tests)

print(test_toolkit(), "tests passed.")
```

Each test case is a `True` or a `False`, and the list keeps them in
order. `enumerate()` counts along the list as it goes, so that a failed
test can name its own number.

A test suite is worth the most when it is run again after every change.
A change to one function can quietly break a promise somewhere else,
and a suite that ran green yesterday will say so today.

### Your turn

Your toolkit cells are your own code, so this review is yours to do.
Open one or two of the earlier pages, and look at your toolkit cells as
a stranger would.

1. Does every function have a docstring that says its promise?
2. Is every name a word that says what it holds?
3. Is every comment about why, and does it still match the code?
4. Add one test case of your own to `test_toolkit` above, for the edge
   of some promise, such as `split_bill` with one person, or
   `to_binary(0)`. Run it again.

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | names that say what they hold, like `warmest_so_far`; renaming changes nothing for Python and everything for a reader |
| What is promised? | a docstring states the promise, and a test case checks it; `close_enough` promises "equal, within a tolerance" |
| What happens when? | a trace table and a debugger show each line in the order it runs, with each name's value at that moment |
| What does this space let us do? | Python runs any valid code, right or wrong; floats need "close enough", not `==`; a start of 0 belongs to a space with no negative numbers |

## What we have now

| Term | What it means |
|---|---|
| bug | a mistake that makes code break its promise |
| testing, test case | running code where we know the right answer; one input with its expected output |
| three sources of test cases | facts from outside, a second route, the edges of the promise |
| tolerance, `1e-9` | the largest difference still counted as equal; $1 \times 10^{-9}$ |
| `close_enough(a, b, tolerance=1e-9)` | your toolkit's test for floats |
| walkthrough, trace, trace table | running code by hand, writing down each name's value at each step |
| structured walkthrough | a meeting where the writer talks others through their code, line by line |
| debugger, breakpoint, step-through | a tool that pauses on a line and runs one line at a time, showing every name |
| coding standard, PEP 8 | agreed rules for names, comments and indentation; Python's own standard |
| test suite | tests kept together and run all at once, after every change |

## Where to read more

The dewlab page
[Debugging a wrong answer: from symptom to cause](tutorial:finding-where-it-went-wrong)
follows a harder bug from the wrong answer back to its cause.

PEP 8, Python's style guide, is at
[peps.python.org/pep-0008](https://peps.python.org/pep-0008/). Its
sections on naming and comments are the ones to read first.

Thonny, at [thonny.org](https://thonny.org), is a free Python editor
made for learners. Its debugger steps through code and shows every name,
the way `step_through` does here.
