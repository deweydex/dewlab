---
title: "Designing and testing good functions — Practice"
practice_for: building-reusable-tools
year: "2026-2027"
version: 2026.08.23.1
---

# Designing and testing good functions — Practice

The answers are hidden in folds under each problem. Most problems ask
you to write a function, and then to say what it does with input it was
not designed for. That second part is the real exercise.

In the cell below, `mean.__doc__` gives back the docstring of `mean`.

## Docstrings and Contracts

```python exec
id: docstrings-and-contracts-1
def mean(numbers):
    """The arithmetic mean of a non-empty list of numbers."""
    return sum(numbers) / len(numbers)


print(mean([10, 20, 30]))
print(mean.__doc__)
```

**1.** Write a docstring for this function.

```python
def f(a, b):
    return (a + b) / 2
```

<details class="dl-answer"><summary>answer</summary>

```python
def midpoint(a, b):
    """The number halfway between a and b."""
    return (a + b) / 2
```

Here the new name does more than the docstring. Sometimes a good name
makes the docstring almost unnecessary. That is a success, and it is no
reason to skip the good name.

</details>

**2.** A docstring is for someone who is about to use the function. What three things should it tell them?

<details class="dl-answer"><summary>answer</summary>

1. What the function does.
2. What it expects as input.
3. What it gives back, including what it does when the input is not what
   it expects.

People often leave out that last part, and it is the part a reader most
often needs. The sentence "Returns None for an empty list" can save
someone an hour.

</details>

**3.** This function's docstring says something that is not true. What is wrong?

```python
def average(numbers):
    """Return the mean of a list of numbers, or 0 if the list is empty."""
    return sum(numbers) / len(numbers)
```

<details class="dl-answer"><summary>answer</summary>

On an empty list, it raises a `ZeroDivisionError`. The docstring
promises something the code does not do.

A wrong docstring is worse than no docstring, because people trust it.
Either add the check, or change the sentence. If you cannot decide
which, you have found a question about the design of the function, and
not only a problem with its description.

</details>

## Building on Other Functions

**4.** Write `data_range(numbers)`. It returns the difference between the largest and the smallest values.

<details class="dl-answer"><summary>answer</summary>

```python
def data_range(numbers):
    """The difference between the largest and smallest values.

    Returns None for an empty list. A single value gives 0.
    """
    if not numbers:
        return None
    return max(numbers) - min(numbers)
```

One element gives 0. That is the correct answer, and it needs no
special code: the largest and the smallest are the same value.

</details>

**5.** Write `describe(numbers)`. It prints a summary, using `mean`, `std_dev` and `data_range`.

<details class="dl-answer"><summary>answer</summary>

```python
def describe(numbers):
    """Print a short summary of a list of numbers."""
    if not numbers:
        print("no data")
        return
    print(f"n         {len(numbers)}")
    print(f"mean      {mean(numbers):.3f}")
    print(f"std dev   {std_dev(numbers):.3f}")
    print(f"range     {data_range(numbers)}")
```

The f-strings work as in
[Variables, data types and text](tutorial:storing-and-computing). Here `:.3f`
gives three decimal places.

On `[42, 38, 35, 47, 29, 41, 44, 33, 39, 48]`, it gives: mean 39.6,
standard deviation about 5.765, range 19.

Look at the `return` straight after "no data". It ends the function
early, so the rest of the function never has to think about the empty
list. Dealing with the awkward input first, and then leaving, is usually
neater than putting everything else inside an `if`.

</details>

**6.** `std_dev` calls `mean` twice. Why is that better than writing the averaging code inside `std_dev`?

<details class="dl-answer"><summary>answer</summary>

Because then there is only one piece of averaging code to get right,
to test and to fix.

The second call is the interesting one. The standard deviation is the
square root of the mean of the squared differences. So it uses *the same
operation twice*. That is easier to see when the operation has a name
than when it is two loops that happen to look alike.

</details>

**7.** Write `median(numbers)`. What does it do with a list that has an even number of items?

<details class="dl-answer"><summary>answer</summary>

```python
def median(numbers):
    """The middle value, or the mean of the two middle values."""
    if not numbers:
        return None
    ordered = sorted(numbers)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2
```

It uses `sorted`, and not `.sort()`, on purpose. Asking for the median
of a list must not change the order of the caller's list.

</details>

## Edge Cases

**8.** For each of these functions, give an input that breaks it: `mean`, `data_range`, `median`, `max`.

<details class="dl-answer"><summary>answer</summary>

An empty list breaks all four, unless the function checks for it. The
`mean` in the cell above divides by zero. `max([])` raises a
`ValueError`. A `data_range` or `median` with no check fails too:
`data_range` because it calls `max` and `min`, and `median` because it
asks for an item from an empty list. The versions in problems 4 and 7
check first, and return `None`.

`mean` also breaks on a list that holds a string. `max` does not:
`max(["b", "a"])` works fine. So be clear about which of your
assumptions is "numbers" and which is "not empty".

</details>

**9.** Here are three ways to handle bad input: return `None`, raise an exception, or return a default value. When is each one right?

<details class="dl-answer"><summary>answer</summary>

**Raise an exception** when the call itself was a mistake, and carrying
on would hide it. `mean([])` almost always means there is a bug
somewhere earlier in the program, so raising an error points at the real
problem.

**Return `None`** when "no answer" is a fair result that the caller
should deal with. Searching for something that might not be there is an
example.

**Return a default** only when the default is correct, and not only
because it is easy. `sum([])` giving 0 is right. `mean([])` giving 0 is
wrong, and that wrong 0 will end up in a report.

</details>

**10.** Add input checking to `mean`, so that it refuses a list that holds anything that is not a number.

<details class="dl-answer"><summary>answer</summary>

```python
def mean(numbers):
    """The arithmetic mean of a non-empty list of numbers."""
    if not numbers:
        raise ValueError("mean of an empty list is undefined")
    for value in numbers:
        if not isinstance(value, (int, float)):
            raise TypeError(f"not a number: {value!r}")
    return sum(numbers) / len(numbers)
```

`isinstance(value, (int, float))` asks whether `value` is an `int` or a
`float`. In the f-string, `!r` shows the value the way Python writes it,
with quotes around a string.

Is the check worth it? Without it, a string in the list still raises a
`TypeError`, from `sum`. The difference is that this error names the
value that caused it. That is usually the whole benefit of a check: it
says which item caused the error.

</details>

**11.** What does `mean([True, True, False])` give? Should it?

<details class="dl-answer"><summary>answer</summary>

0.666…, because in Python `True` counts as 1 and `False` counts as 0.

`isinstance(True, int)` is `True`, so the check in the previous answer
lets `True` and `False` through. Is that a bug? It depends on what you
meant. The mean of a list of yes-or-no answers is the fraction that
said yes, and that is often the number you wanted.

</details>

## Testing

```python exec
id: testing-1
def test_mean():
    assert mean([10, 20, 30]) == 20
    assert mean([5]) == 5
    assert abs(mean([1, 2]) - 1.5) < 1e-9
    print("mean: all tests passed")


test_mean()
```

The cell below uses `assert`. An `assert` line checks that something is
true. If it is not true, Python stops with an `AssertionError`.

**12.** Write three tests for `data_range`: an ordinary one, an edge case, and one that should fail loudly.

<details class="dl-answer"><summary>answer</summary>

```python
assert data_range([1, 5, 3]) == 4          # ordinary
assert data_range([7]) == 0                # edge: one item
assert data_range([]) is None              # edge: empty
```

A test that "should fail loudly" checks that an error really happens.
Here `try` runs `mean([])`. The `except` part runs if a `ValueError` is
raised. The `else` part runs if no error is raised:

```python
try:
    mean([])
except ValueError:
    print("raised as expected")
else:
    print("did NOT raise — the check is missing")
```

Testing that something fails is as important as testing that it
works. It is also the half that most people skip.

</details>

**13.** Why is `assert mean([0.1, 0.2]) == 0.15` a bad test?

<details class="dl-answer"><summary>answer</summary>

Because the test fails, even though the function is fine.

`(0.1 + 0.2) / 2` is 0.15000000000000002. A computer cannot store most
decimals exactly. So a test that checks two floats for exact equality is
testing how the computer stores numbers, and not your code. Instead,
check that the difference is very small, as `testing-1` does with
`abs(...) < 1e-9`.

</details>

**14.** You write a test and it passes immediately. What should you check?

<details class="dl-answer"><summary>answer</summary>

Check that it would fail if the code were wrong.

Break the function on purpose. For example, return the wrong thing, or
turn a `<` into a `>`. Then make sure the test complains. A test that
passes on broken code tests nothing, and there are many such tests in
the world.

</details>

## From the Everlearning Problem Bank

**15.** Write `convert_temperature(celsius)`. It returns both the Fahrenheit and the Kelvin temperature.

<details class="dl-answer"><summary>answer</summary>

```python
def convert_temperature(celsius):
    """Return (fahrenheit, kelvin) for a temperature in Celsius."""
    return celsius * 9 / 5 + 32, celsius + 273.15
```

A Python function gives back more than one value by returning a
*tuple*. A tuple is a fixed group of values, with commas between them.
The caller unpacks it: `f, k = convert_temperature(20)`.

Check it against a value you know: 100 °C should give 212 °F and
373.15 K.

</details>

**16.** Write `remove_character(text, position)`. It removes the character at a given index.

<details class="dl-answer"><summary>answer</summary>

```python
def remove_character(text, position):
    """Return text with the character at `position` removed."""
    return text[:position] + text[position + 1:]
```

It uses slicing, and does not delete, because a string cannot be
changed in place.

A position past the end returns the string unchanged, with no error. A
slice never goes out of range: it stops at the ends. A negative position
is stranger still: try `remove_character("abc", -1)`. If either result
is wrong for your purpose, you have to write the check yourself.

</details>

**17.** Write `swap_first_last(text)`. It swaps the first and last characters of a string.

<details class="dl-answer"><summary>answer</summary>

```python
def swap_first_last(text):
    """Return text with its first and last characters exchanged."""
    if len(text) < 2:
        return text
    return text[-1] + text[1:-1] + text[0]
```

The `if` at the start does real work. Without it, a one-character
string comes back doubled, because `text[-1]` and `text[0]` are the same
character, and `text[1:-1]` is empty. An empty string would raise an
`IndexError`.

</details>

**18.** Write `is_palindrome(text)`. A palindrome reads the same forwards and backwards. Your function ignores capital letters and punctuation.

<details class="dl-answer"><summary>answer</summary>

```python
def is_palindrome(text):
    """True if text reads the same both ways, ignoring case and punctuation."""
    letters = [c.lower() for c in text if c.isalnum()]
    return letters == letters[::-1]
```

`"A man, a plan, a canal: Panama"` gives `True`.

`c.isalnum()` is `True` for letters and digits, so the list keeps only
those.

It is much easier to build the cleaned list first and then compare. The
other way walks two positions inwards from the ends, skipping
punctuation as it goes, and it is easy to get wrong. The first way is
also the version you can still read in a month.

</details>

**19.** Write `longest_word(sentence)`.

<details class="dl-answer"><summary>answer</summary>

```python
def longest_word(sentence):
    """The longest word in a sentence, or None if there are no words."""
    words = sentence.split()
    if not words:
        return None
    longest = words[0]
    for word in words:
        if len(word) > len(longest):
            longest = word
    return longest
```

If two words tie, the first one wins, because the test is `>` and not
`>=`. Is that right? The problem does not say. Either way, it is worth a
line in the docstring.

</details>

## Putting It Together

**20.** Build a small statistics toolkit: `mean`, `median`, `mode`, `data_range`, `std_dev`, and a `summary` that uses them all. Give each function a docstring and at least two tests.

<details class="dl-answer"><summary>answer</summary>

The shape matters more than the details. The *mode* is the most common
value in a list.

```python
def mode(numbers):
    """The most common value. Ties are broken by first appearance."""
    if not numbers:
        return None
    return max(numbers, key=numbers.count)


def summary(numbers):
    """Print mean, median, mode, range and standard deviation."""
    for name, value in [
        ("mean", mean(numbers)),
        ("median", median(numbers)),
        ("mode", mode(numbers)),
        ("range", data_range(numbers)),
        ("std dev", std_dev(numbers)),
    ]:
        print(f"{name:<10}{value}")
```

There are five small functions, each one testable on its own, and a
sixth that puts them together. In `summary`, `{name:<10}` pads each name
with spaces to ten characters, so the values line up.

Make every one of them handle the empty list in the same way. A toolkit
whose pieces disagree about edge cases is harder to use than one that is
always strict, or always forgiving. Right now they do not agree: `mode`
returns `None`, but the `mean` from the cell above divides by zero, and
so does `std_dev`, which calls it.

`mode` is the one worth arguing about. A list with two values that are
equally common has two modes. Returning only one of them, without
saying so, is a decision. At the least, say so in the docstring. The
more accurate version returns a list of all the modes.

</details>
