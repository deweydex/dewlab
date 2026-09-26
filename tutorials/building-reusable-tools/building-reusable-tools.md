---
title: "Designing and testing good functions"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  what-makes-a-good-function:
    covers: [PDP-LO8, PDP-LO11]
  testing-as-a-habit:
    covers: [PDP-LO10]
  functions-calling-functions:
    covers: [PDP-LO8]
  handling-edge-cases:
    covers: [PDP-LO7]
  variable-scope-revisited:
    covers: [PDP-LO8]
---

# Designing and testing good functions

Here is a function that calculates the average, the mean, of a list of
numbers. It works on the first list. What happens on the second?

```python exec
id: a-mean-that-works-1
def mean(numbers):
    return sum(numbers) / len(numbers)

print(mean([10, 20, 30]))
print(mean([]))
```

```predict
What will the last line do?

- Print 0
  - There are no numbers, so the average is nothing.
- Print None
  - A function gives back None when it has no answer.
- Stop with an error
  - An empty list has length 0, and it divides by 0.
```

It stops with a `ZeroDivisionError`. The function is right for every list
its author tried, and wrong for one they did not. This page shows how to
write functions that other people, and you next month, can rely on. We
say what a function promises, test that it keeps the promise, and decide
on purpose what it does with the inputs nobody thought of.

## What makes a good function?

A good function does one thing, and makes clear what it does. As you read
this one, ask what makes it easy to use.

```python exec
id: what-makes-a-good-function-1
def mean(numbers):
    """Give back the arithmetic mean of a list of numbers.

    numbers: a list of numbers, which must not be empty.
    Gives back: the mean, as a float.
    """
    total = 0
    for value in numbers:
        total = total + value
    return total / len(numbers)

print(mean([10, 20, 30]))
print(mean([1, 2, 3, 4, 5]))
```

The string in triple quotes under the `def` line is a *docstring*: a
description of the function, written at the top of it. It says what the
function does, what it needs, and what it returns. Together, those are
the function's *contract*: its promise. Give it this, and it gives you
that. Anyone can read the docstring, and use `mean()` without reading its
code. From here on, every function we write has one. One clear sentence is
often enough.

## Testing as a habit

A *test* gives a function an input whose answer we already know, and
checks that the function gives that answer. Python has a statement for
it. `assert` is followed by something that should be `True`. If it is,
nothing happens. If it is not, the program stops with an `AssertionError`.

```python exec
id: testing-as-a-habit-1
assert mean([10, 20, 30]) == 20
assert mean([42]) == 42
assert mean([-10, 10]) == 0
print("All three tests passed.")
```

Change one of the expected answers to something wrong, and run it again.
A test that passes is silent, and a test that fails says which line. Now
we do some detective work.

### Which one is right?

Four people wrote `mean`. One version is right. The other three are wrong,
each in its own way, and each gives the right answer for some lists. Can
your tests tell which one is right?

```python exec
id: testing-as-a-habit-2
def mean_a(numbers):
    total = 0
    for value in numbers:
        total = total + value
    return total / len(numbers)

def mean_b(numbers):
    total = 0
    for value in numbers[1:]:
        total = total + value
    return total / len(numbers)

def mean_c(numbers):
    total = 0
    for value in numbers:
        total = total + value
    return total // len(numbers)

def mean_d(numbers):
    total = 0
    for value in numbers:
        total = value
    return total / len(numbers)

def try_all(numbers, expected):
    versions = {"a": mean_a, "b": mean_b, "c": mean_c, "d": mean_d}
    for name, version in versions.items():
        answer = version(numbers)
        if answer == expected:
            print(name, "agrees")
        else:
            print(name, "gives", answer)

try_all([10, 20, 30], 20)
```

Add more calls to `try_all`, each with a list and the mean you know it
has. Which lists catch which versions? What is the smallest set of lists
that leaves only one version agreeing every time?

<details class="dl-answer"><summary>one way it goes</summary>

`[10, 20, 30]` catches b, which leaves out the first number, and d, which
keeps only the last. It does not catch c. Its mean is a whole number, so
`//` gives the same answer as `/`. A list with a mean that is not whole,
such as `[1, 2]`, catches c. So `[10, 20, 30]` and `[1, 2]` together leave
only a.

Nobody has caught the version that passes everything yet, but that does
not prove it is right.
Each test is a question, and a good set asks different questions: a
middle case, an edge, a case where two ways of being wrong would give
different answers.

</details>

## Functions calling functions

Small, tested functions can be built into bigger ones. The *standard
deviation* measures how spread out numbers are round their mean. For every
value in a list:

1. Find the mean.
2. For each value, take its difference from the mean, and square it.
3. Find the mean of those squares.
4. Take the square root.

How many times does this function call `mean()`?

```python exec
id: functions-calling-functions-1
def std_dev(numbers):
    """Give back the standard deviation of a non-empty list of numbers."""
    average = mean(numbers)
    squares = []
    for value in numbers:
        squares.append((value - average) ** 2)
    return mean(squares) ** 0.5

print(std_dev([10, 20, 30]))
```

It calls `mean()` twice, once for the numbers and once for the squared
differences. The averaging code is written once, in `mean()`. If a bug
appears in `mean()`, one fix there fixes `std_dev()` too, and each
function can be tested on its own. This is the main idea of modular
design.

### Your turn

The *range* of a list, in statistics, is the difference between its
largest and smallest values. It has nothing to do with Python's `range()`.
Can you write `data_range(numbers)`, with a docstring, using `max()` and
`min()`? Then write your own tests for it, in the second cell: an ordinary
list, one where every value is the same, and one with negative numbers.

```python exec
id: your-turn-1
def data_range(numbers):
    """Give back the difference between the largest and smallest values."""
    return 0
```

```inputs
guess: yes
data_range([3, 9, 4])
data_range([-5, 5])
data_range([7])
```

```python exec
id: your-turn-1-tests
tests: your-turn-1
assert data_range([1, 5, 3]) == 4
```

```hint
`max(numbers)` is the largest value, and `min(numbers)` the smallest.
What is one taken from the other?
```

```solution
def data_range(numbers):
    """Give back the difference between the largest and smallest values."""
    return max(numbers) - min(numbers)
---
Your tests run against your function and against this one. A test that
fails on this one too is a question about the test: was the expected
answer right? With one value, the range is 0. With no values, `max()`
stops with a `ValueError`, which the next section is about.
```

## Handling edge cases

An empty list is an *edge case*: an unusual input, at the edge of what a
function expects, that it has to handle on purpose. There are three
things a function can do with one. Here is the one that looks helpful.

```python exec
id: handling-edge-cases-1
def mean(numbers):
    if len(numbers) == 0:
        print("Cannot take the mean of nothing")
    else:
        return sum(numbers) / len(numbers)

result = mean([])
print(result + 1)
```

```predict
What happens?

- It prints the message, and stops.
  - The message tells the person what went wrong.
- It prints the message, then stops with an error.
  - The function still gives back something, and it is None.
- It prints the message, then 1.
  - With nothing to add, the mean counts as 0.
```

It prints the message, and then stops with a `TypeError`, a line later,
somewhere else. `print` is for the person watching. The program that
called `mean` never sees the message. It gets `None`, as
[Writing your own functions](tutorial:writing-your-own-functions) showed a
function without a `return` always does. So the error appears far from
its cause.

The two better ways both tell the caller.

```python exec
id: handling-edge-cases-2
def mean_or_none(numbers):
    """Give back the mean, or None for an empty list."""
    if len(numbers) == 0:
        return None
    return sum(numbers) / len(numbers)

def mean(numbers):
    """Give back the mean of a list of numbers, which must not be empty."""
    if len(numbers) == 0:
        raise ValueError("mean() needs at least one number")
    return sum(numbers) / len(numbers)

print(mean_or_none([]))
print(mean([]))
```

`return None` gives the caller a value that means "no answer", which they
can check for with `if result is None`. `raise` stops the function with an
error of its own, naming the problem, at the place it happened. Which
should you choose? If an empty list is normal, and the caller can do
something sensible with no answer, return `None`. If it is a mistake,
raise an error. A mistake that stops the program at once is much easier to find than one
that travels.

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you write `most_common(text)`, which returns the capital letter
that appears most often in `text`, and raises a `ValueError` when `text`
has no capital letters at all? Then write your own tests for it.

```python exec
id: your-turn-2--secret-messages
def most_common(text):
    """Give back the most common capital letter in text.

    Raises ValueError if text has no capital letters.
    """
    return ""
```

```inputs
guess: yes
most_common("BANANA")
most_common("MEET ME")
most_common("no capitals")
```

```python exec
id: your-turn-2-tests--secret-messages
tests: your-turn-2--secret-messages
assert most_common("AAB") == "A"
```

```hint
Count the capitals into a dictionary, as
[Dictionaries: looking things up by name](tutorial:looking-things-up-by-name)
did. If the dictionary is still empty after the loop, there were none:
raise. If not, keep the letter with the biggest count.
```

```solution
def most_common(text):
    """Give back the most common capital letter in text.

    Raises ValueError if text has no capital letters.
    """
    counts = {}
    for character in text:
        if character.isupper():
            counts[character] = counts.get(character, 0) + 1
    if len(counts) == 0:
        raise ValueError("most_common() needs at least one capital letter")
    best = ""
    for letter, count in counts.items():
        if count > counts.get(best, 0):
            best = letter
    return best
---
The docstring says what happens at the edge, so a caller knows to expect
it. What does it give for `"ABAB"`, where two letters tie? Is that written
down anywhere? It could be.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you write `average_brightness(row)`, which returns the mean
brightness of a row of pixels, and raises a `ValueError` for a row with no
pixels? Then write your own tests for it.

```python exec
id: your-turn-2--pixel-art
def average_brightness(row):
    """Give back the mean brightness of a row of pixels.

    Raises ValueError if the row is empty.
    """
    return 0
```

```inputs
guess: yes
average_brightness([0, 255])
average_brightness([90])
average_brightness([])
```

```python exec
id: your-turn-2-tests--pixel-art
tests: your-turn-2--pixel-art
assert average_brightness([100, 200]) == 150
```

```hint
Check for the empty row first, and raise. After that, the row has at
least one pixel, and dividing by its length is safe.
```

```solution
def average_brightness(row):
    """Give back the mean brightness of a row of pixels.

    Raises ValueError if the row is empty.
    """
    if len(row) == 0:
        raise ValueError("average_brightness() needs at least one pixel")
    total = 0
    for value in row:
        total = total + value
    return total / len(row)
---
`[0, 255]` gives 127.5, which is not a whole brightness. Should it round?
The docstring says "the mean", so it does not. A caller who wants a pixel
value can round it.
```

</div>

## Variable scope revisited

Our functions now call other functions, so it is worth checking scope,
from [Writing your own functions](tutorial:writing-your-own-functions).
Each function has its own workspace, and the variables made inside it
disappear when it finishes.

```python exec
id: variable-scope-revisited-1
def with_border(width):
    edge = "#" * width
    middle = "#" + "." * (width - 2) + "#"
    return edge + "\n" + middle + "\n" + edge

print(with_border(6))

# What happens if this line runs? Delete the # at its start to find out.
# print(edge)
```

It gives a `NameError`, because `edge` exists only inside `with_border`.
That is a help, not a nuisance. Many functions can each have a variable
called `total` or `edge`, and none of them clashes with another.
Information goes in through parameters, and leaves through `return`.

## Looking back

A test that passes tells you less than a test that fails. Why? What would
make you trust a function you did not write?

Here is a challenge. Test your bubble sort from
[Sorting a list](tutorial:putting-things-in-order) on a hundred lists
nobody chose. Make each list at random, sort it, and check the answer
against Python's own `sorted()`. What is the smallest list that catches a
broken sort?

```python challenge
import random

def bubble_sort(items):
    for pass_number in range(len(items) - 1):
        for i in range(len(items) - 1 - pass_number):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return items

for trial in range(100):
    items = [random.randint(0, 9) for _ in range(random.randint(0, 8))]
    assert bubble_sort(items[:]) == sorted(items), items
print("100 random lists, all sorted the same way as sorted().")
```

The next page, [Finding bugs in bigger programs](tutorial:when-it-goes-wrong),
uses these habits when something does go wrong in a program of several
functions.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Schafer, C. (2017). *Python Tutorial: Unit Testing Your Code with the
unittest Module*. <https://www.youtube.com/watch?v=6tNS--WetLI>. This page
tests with `assert`. That is the first step, and this video is the second.

Python Software Foundation. *The Python Tutorial*, section 4.9, "More on
Defining Functions".
<https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions>.
This is the official reference for docstrings, default values, and everything else
a function definition can do.
