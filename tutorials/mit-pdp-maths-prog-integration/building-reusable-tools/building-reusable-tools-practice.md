---
title: "Building Reusable Tools — Practice"
slug: building-reusable-tools-practice
practice_for: building-reusable-tools
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Building Reusable Tools — Practice

Answers are folded. Most of these ask you to write a function and then say what it does with input it was not designed for. That second half is the exercise.

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

The rename does more than the docstring here. When a good name makes the docstring redundant, that is a success rather than a reason to skip the name.

</details>

**2.** What three things should a docstring tell someone who is about to use the function?

<details class="dl-answer"><summary>answer</summary>

What it does, what it expects, and what it gives back — including what it does when the expectation is not met.

That last part is the one people leave out, and it is the one a reader most often needs. "Returns None for an empty list" is a sentence that saves an hour.

</details>

**3.** This function has a docstring that lies. What is wrong?

```python
def average(numbers):
    """Return the mean of a list of numbers, or 0 if the list is empty."""
    return sum(numbers) / len(numbers)
```

<details class="dl-answer"><summary>answer</summary>

It raises `ZeroDivisionError` on an empty list. The docstring promises something the code does not do.

A wrong docstring is worse than none, because it is trusted. Either add the check or change the sentence — and if you cannot decide which, that is a design question you have just discovered rather than a documentation problem.

</details>

## Building on Other Functions

**4.** Write `data_range(numbers)`, returning the difference between the largest and smallest.

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

One element gives 0, which is correct rather than a special case — the largest and smallest are the same value.

</details>

**5.** Write `describe(numbers)` that prints a summary using `mean`, `std_dev` and `data_range`.

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

On `[42, 38, 35, 47, 29, 41, 44, 33, 39, 48]`: mean 39.6, standard deviation about 5.765, range 19.

The early `return` after printing "no data" is what keeps the rest of the function from having to handle the empty case again. Dealing with the awkward input first and leaving is usually tidier than wrapping everything in an `if`.

</details>

**6.** `std_dev` calls `mean` twice. Why is that better than computing the average inline?

<details class="dl-answer"><summary>answer</summary>

Because there is one averaging routine to be right, to test, and to fix.

The second call is the interesting one: the standard deviation is the mean of the squared differences, square-rooted. Seeing that it is *the same operation applied twice* is easier when it has a name than when it is two loops that happen to look alike.

</details>

**7.** Write `median(numbers)`. What does it do with an even-length list?

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

`sorted` rather than `.sort()` matters: the caller's list must not be reordered by asking for its median.

</details>

## Edge Cases

**8.** For each function, name an input that breaks it: `mean`, `data_range`, `median`, `max`.

<details class="dl-answer"><summary>answer</summary>

All four break on an empty list — division by zero for `mean`, and "arg is an empty sequence" for the others.

`mean` also breaks on a list containing a string, and `max` does not: `max(["b", "a"])` is perfectly happy. Knowing which of your assumptions is "numbers" and which is "non-empty" is worth being explicit about.

</details>

**9.** Three ways to handle bad input: return `None`, raise an exception, or return a default. When is each right?

<details class="dl-answer"><summary>answer</summary>

Raise when the call was a mistake and continuing would hide it. `mean([])` is almost always a bug upstream, so raising points at the real problem.

Return `None` when "no answer" is a legitimate outcome the caller should handle — searching for something that might not be there.

Return a default only when the default is genuinely correct, not merely convenient. `sum([])` being 0 is right; `mean([])` being 0 is a lie that will end up in a report.

</details>

**10.** Add input checking to `mean` so it refuses a list containing anything that is not a number.

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

Worth asking whether it is worth it. Without the check, a string in the list raises a `TypeError` from `sum` anyway — the difference is that this one names the offending value. That is usually the whole benefit of a check: not catching the error, but saying which item caused it.

</details>

**11.** What does `mean([True, True, False])` give, and should it?

<details class="dl-answer"><summary>answer</summary>

0.666…, because in Python `True` is 1 and `False` is 0.

`isinstance(True, int)` is `True`, so the check in the previous answer lets booleans through. Whether that is a bug depends on what you meant: the mean of a list of yes/no answers is the proportion that said yes, which is often exactly the number you wanted.

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

**12.** Write three tests for `data_range`: one ordinary, one edge case, one that should fail loudly.

<details class="dl-answer"><summary>answer</summary>

```python
assert data_range([1, 5, 3]) == 4          # ordinary
assert data_range([7]) == 0                # edge: one item
assert data_range([]) is None              # edge: empty
```

A test that "should fail loudly" is one where you assert the error happens:

```python
try:
    mean([])
except ValueError:
    print("raised as expected")
else:
    print("did NOT raise — the check is missing")
```

Testing that something fails is as important as testing that it works, and it is the half most people skip.

</details>

**13.** Why is `assert mean([0.1, 0.2]) == 0.15` a bad test?

<details class="dl-answer"><summary>answer</summary>

Because it fails, and the function is fine.

`(0.1 + 0.2) / 2` is 0.15000000000000002. Any test comparing floats for exact equality is testing the arithmetic hardware rather than your code. Compare with a tolerance.

</details>

**14.** You write a test and it passes immediately. What should you check?

<details class="dl-answer"><summary>answer</summary>

That it would fail if the code were wrong.

Break the function on purpose — return the wrong thing, flip a comparison — and make sure the test complains. A test that passes against broken code is decorative, and there are more of those in the world than anyone would like.

</details>

## From the Everlearning Problem Bank

**15.** Write `convert_temperature(celsius)` returning both Fahrenheit and Kelvin.

<details class="dl-answer"><summary>answer</summary>

```python
def convert_temperature(celsius):
    """Return (fahrenheit, kelvin) for a temperature in Celsius."""
    return celsius * 9 / 5 + 32, celsius + 273.15
```

Returning a tuple is how a Python function gives back more than one thing. The caller unpacks it: `f, k = convert_temperature(20)`.

Worth checking against a value you know: 100 °C should give 212 °F and 373.15 K.

</details>

**16.** Write `remove_character(text, position)` that removes the character at a given index.

<details class="dl-answer"><summary>answer</summary>

```python
def remove_character(text, position):
    """Return text with the character at `position` removed."""
    return text[:position] + text[position + 1:]
```

Slicing rather than deleting, because strings cannot be changed in place.

An out-of-range position does not fail — it returns the string unchanged, because slices clamp. If that is wrong for your purpose, the check has to be explicit.

</details>

**17.** Write `swap_first_last(text)`.

<details class="dl-answer"><summary>answer</summary>

```python
def swap_first_last(text):
    """Return text with its first and last characters exchanged."""
    if len(text) < 2:
        return text
    return text[-1] + text[1:-1] + text[0]
```

The guard is doing real work. Without it, a one-character string comes back doubled, because `text[-1]` and `text[0]` are the same character and `text[1:-1]` is empty.

</details>

**18.** Write `is_palindrome(text)` that ignores case and punctuation.

<details class="dl-answer"><summary>answer</summary>

```python
def is_palindrome(text):
    """True if text reads the same both ways, ignoring case and punctuation."""
    letters = [c.lower() for c in text if c.isalnum()]
    return letters == letters[::-1]
```

`"A man, a plan, a canal: Panama"` gives `True`.

Building the cleaned list first and then comparing is much easier to get right than walking two pointers inwards while skipping punctuation — and it is the version you can still read in a month.

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

Ties go to the first, because the comparison is strict. Whether that is right is a question the specification did not answer, and it is worth a line of docstring either way.

</details>

## Putting It Together

**20.** Build a small statistics toolkit: `mean`, `median`, `mode`, `data_range`, `std_dev`, and a `summary` that uses them all. Give each a docstring and at least two tests.

<details class="dl-answer"><summary>answer</summary>

The shape matters more than the details:

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

Six small functions, each testable alone, and one that arranges them. Every one of them handles the empty list the same way, which is not an accident — a toolkit whose pieces disagree about edge cases is harder to use than one that is uniformly strict or uniformly forgiving.

`mode` is the one worth arguing about. A list with two equally common values has two modes, and returning one of them silently is a decision. Saying so in the docstring is the minimum; returning a list of them is the honest version.

</details>
