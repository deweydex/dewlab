---
title: "Designing and testing good functions — Practice"
practice_for: building-reusable-tools
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Designing and testing good functions — Practice

Problems on docstrings, edge cases and tests, and three from earlier
pages. Where a problem has a cell of tests under it, those tests are
yours. Add to them, and they run against your function and against a
solution. Try each problem before you open anything under it.

## 1. A docstring for f

Can you write a docstring for this function, and give it a better name?

```python
def f(a, b):
    return (a + b) / 2
```

<details class="dl-answer"><summary>one answer</summary>

```python
def midpoint(a, b):
    """Give back the number halfway between a and b."""
    return (a + b) / 2
```

Here the new name does more than the docstring. A good name can make a
docstring almost unnecessary, which is a success, and no reason to skip
the name.

</details>

## 2. What a docstring says

A docstring is for someone about to use the function. What three things
should it tell them?

<details class="dl-answer"><summary>answer</summary>

It should say what the function does, what it expects as input, and what
it returns, including what it does when the input is not what it expects. The last is
the part most often left out, and the part a reader most often needs.
"Raises ValueError for an empty list" can save somebody an hour.

</details>

## 3. A docstring that is not true

What is wrong with this function's docstring?

```python
def average(numbers):
    """Give back the mean of a list of numbers, or 0 if it is empty."""
    return sum(numbers) / len(numbers)
```

<details class="dl-answer"><summary>answer</summary>

On an empty list it stops with a `ZeroDivisionError`. The docstring
promises something the code does not do. A wrong docstring is worse than
none, because people trust it. Either add the check or change the
sentence. If you cannot decide which, you have found a question about what
the function is for.

</details>

## 4. The middle value

The *median* is the middle value of a list once it is sorted. With an even
number of values, it is the mean of the two in the middle. Can you write
`median(numbers)`, and add tests of your own?

```python exec
id: the-middle-value-1
def median(numbers):
    """Give back the middle value of a non-empty list of numbers."""
    return 0
```

```inputs
guess: yes
median([3, 1, 2])
median([4, 1, 3, 2])
median([7])
```

```python exec
id: the-middle-value-1-tests
tests: the-middle-value-1
assert median([5, 1, 9]) == 5
```

```hint
Sort a copy with `sorted()`. The middle index is `len(ordered) // 2`. When
the length is even, which two indexes are either side of the middle?
```

```solution
def median(numbers):
    """Give back the middle value of a non-empty list of numbers."""
    ordered = sorted(numbers)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2
---
`sorted()`, not `.sort()`, on purpose: asking for the median must not
change the order of the caller's list. `[4, 1, 3, 2]` gives 2.5.
```

## 5. What breaks them

Give an input that breaks each of these: `mean`, `median` from problem 4,
and Python's own `max`.

<details class="dl-answer"><summary>answer</summary>

An empty list breaks all three: `mean` divides by zero, `median` asks for
an element of an empty list, and `max([])` raises a `ValueError`. `mean`
also breaks on a list holding a string, and `max` does not:
`max(["b", "a"])` is `"b"`. So it is worth being clear which of your
assumptions is "numbers" and which is "not empty".

</details>

## 6. Three ways

A function can meet bad input by returning `None`, by raising an error, or
by returning a default value. When is each one right?

<details class="dl-answer"><summary>answer</summary>

**Raise** when the call itself was a mistake, and continuing would hide
it: `mean([])` almost always means a bug earlier in the program.

**Return `None`** when "no answer" is a normal result the caller should deal
with, such as a search for something that may not be there.

**Return a default** only when the default is right, and not because it
is easy. When `sum([])` gives 0, that is right. When `mean([])` gives 0,
that is wrong, and that wrong 0 appears in somebody's report.

</details>

## 7. The mean of True and False

```python exec
id: the-mean-of-true-and-false-1
answers = [True, True, False]
print(sum(answers) / len(answers))
```

```predict
type: number
tolerance: 0.01

What will it print?
```

<details class="dl-answer"><summary>why</summary>

The answer is about 0.667. In Python, `True` counts as 1 and `False` as 0,
so the sum is 2. Is that a bug? It depends on what you meant. The mean of a
list of
yes-or-no answers is the fraction that said yes, which is often the
number you wanted.

</details>

## 8. A test that fails a good function

```python exec
id: a-test-that-fails-a-good-function-1
def mean(numbers):
    return sum(numbers) / len(numbers)

assert mean([0.1, 0.2]) == 0.15
print("passed")
```

```predict
What will it do?

- Print passed
  - The mean of 0.1 and 0.2 is 0.15.
- Stop with an AssertionError
  - A float is often not stored exactly.
```

<details class="dl-answer"><summary>why</summary>

It stops with an `AssertionError`, though the function is fine.
`(0.1 + 0.2) / 2` is `0.15000000000000002`: most decimals cannot be
stored exactly. A test that checks two floats for exact equality tests
how the computer stores numbers, not your code. Check that they are close
instead: `assert abs(mean([0.1, 0.2]) - 0.15) < 1e-9`.

</details>

## 9. A test that passes at once

You write a test, and it passes the first time. What should you check?

<details class="dl-answer"><summary>answer</summary>

Check that it would fail if the code were wrong. Break the function on
purpose:
return the wrong thing, or turn a `<` into a `>`. Then make sure the test
complains. A test that passes on broken code tests nothing, and the
bug hunt on the tutorial page had three versions ready to show it.

</details>

## 10. A test that checks for an error

How can a test check that `mean([])` raises a `ValueError`, when an error
stops the program?

<details class="dl-answer"><summary>answer</summary>

It can use `try`, which is new here. The `try` part runs the call. The `except`
part runs only if that kind of error is raised. The `else` part runs only
if nothing was raised.

```python
try:
    mean([])
except ValueError:
    print("raised, as the docstring promises")
else:
    print("did not raise: the check is missing")
```

A test that checks for a failure is as important as a test that checks
that it works. Most people skip the first kind.

</details>

## 11. Reads the same both ways

<div class="dl-world" data-world="secret-messages">

A *palindrome* reads the same forwards and backwards, like NOON. Can you
write `is_palindrome(text)`, which ignores spaces and capital letters, so
that `"Never odd or even"` counts? Add tests of your own.

```python exec
id: reads-the-same-both-ways-1--secret-messages
def is_palindrome(text):
    """Give back True if text reads the same both ways, ignoring spaces and case."""
    return False
```

```inputs
guess: yes
is_palindrome("Never odd or even")
is_palindrome("MEET ME")
is_palindrome("")
```

```python exec
id: reads-the-same-both-ways-1-tests--secret-messages
tests: reads-the-same-both-ways-1--secret-messages
assert is_palindrome("NOON")
```

```hint
First build a string of the letters only, all in capitals. Then compare
it with itself backwards: a loop can build the backwards copy, or
`[::-1]` can.
```

```solution
def is_palindrome(text):
    """Give back True if text reads the same both ways, ignoring spaces and case."""
    letters = ""
    for character in text.upper():
        if character != " ":
            letters = letters + character
    return letters == letters[::-1]
---
An empty string reads the same both ways, so it counts. Is that what you
wanted? Your tests are the place to say so.
```

</div>

<div class="dl-world" data-world="pixel-art">

A row of pixels is *symmetric* if it looks the same mirrored. Can you
write `is_symmetric(picture)`, which gives `True` when every row of a
picture is symmetric? Add tests of your own.

```python exec
id: reads-the-same-both-ways-1--pixel-art
def is_symmetric(picture):
    """Give back True if every row of picture reads the same both ways."""
    return False
```

```inputs
guess: yes
is_symmetric([[0, 255, 0], [255, 0, 255]])
is_symmetric([[1, 2], [2, 2]])
is_symmetric([])
```

```python exec
id: reads-the-same-both-ways-1-tests--pixel-art
tests: reads-the-same-both-ways-1--pixel-art
assert is_symmetric([[1, 0, 1]])
```

```hint
Check the rows one at a time. `row[::-1]` is the row backwards. As soon as
one row is not symmetric, the answer is `False`.
```

```solution
def is_symmetric(picture):
    """Give back True if every row of picture reads the same both ways."""
    for row in picture:
        if row != row[::-1]:
            return False
    return True
---
An empty picture has no row that breaks the rule, so it gives `True`.
That is how "every" works in mathematics too, and it is still worth a
test, so that nobody changes it by accident.
```

</div>

## 12. The longest word

`sentence.split()` gives a list of the words in a sentence, cut wherever
there are spaces. Can you write `longest_word(sentence)`, and decide what
it gives for a sentence with no words?

```python exec
id: the-longest-word-1
def longest_word(sentence):
    """Give back the longest word in sentence."""
    return ""
```

```inputs
guess: yes
longest_word("the quick brown fox")
longest_word("a bb cc")
longest_word("")
```

```python exec
id: the-longest-word-1-tests
tests: the-longest-word-1
assert longest_word("hi there") == "there"
```

```solution
def longest_word(sentence):
    """Give back the longest word in sentence.

    The first one wins a tie. An empty sentence gives an empty string.
    """
    best = ""
    for word in sentence.split():
        if len(word) > len(best):
            best = word
    return best
---
"quick", not "brown": both have five letters, and `>` keeps the first.
The docstring now says so, and says what an empty sentence gives.
```

## 13. The most frequent

The *mode* is the value that appears most often. Can you write
`mode(numbers)`, say in its docstring what happens with a tie, and test
it?

```python exec
id: the-most-frequent-1
def mode(numbers):
    """Give back the most common value in a non-empty list."""
    return 0
```

```inputs
guess: yes
mode([3, 7, 3, 9, 7, 3, 1])
mode([5])
mode([2, 1, 1, 2])
```

```python exec
id: the-most-frequent-1-tests
tests: the-most-frequent-1
assert mode([4, 4, 1]) == 4
```

```solution
def mode(numbers):
    """Give back the most common value in a non-empty list.

    With a tie, the value that appears first in the list wins.
    """
    counts = {}
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1
    best = numbers[0]
    for number, count in counts.items():
        if count > counts[best]:
            best = number
    return best
---
`[2, 1, 1, 2]` gives 2, because 2 comes first. A tie rule nobody wrote
down is a rule nobody can test.
```

## 14. From earlier: sorting a string

From *Sorting a list: bubble, insertion and selection sort*.

```python exec
id: from-earlier-sorting-a-string-1
print(sorted("CAB"))
```

```predict
What will it print?

- ABC
  - `sorted()` puts the letters of a string in order.
- ['A', 'B', 'C']
  - `sorted()` always gives back a list.
- An error
  - Only a list can be sorted.
```

<details class="dl-answer"><summary>why</summary>

The answer is `['A', 'B', 'C']`. `sorted()` takes anything a loop can use,
and always returns a list. `"".join(sorted("CAB"))` makes it a string
again.

</details>

## 15. From earlier: minus one as an index

From *Searching a list: linear and binary search*.

```python exec
id: from-earlier-minus-one-as-an-index-1
def linear_search(items, target):
    for index in range(len(items)):
        if items[index] == target:
            return index
    return -1

names = ["OTTER", "HERON"]
print(names[linear_search(names, "FOX")])
```

```predict
What will it print?

- HERON
  - -1 is a real index: the last element.
- An error
  - FOX is not there, so there is nothing to print.
- -1
  - The search gives -1 for "not there".
```

<details class="dl-answer"><summary>why</summary>

The answer is `HERON`, with no error. The search said "not there" with
−1, and the caller used it as an index, which picks the last element. A
caller must check for −1 before using the answer. If the search raised
an error in place of returning −1, nobody could forget the check.

</details>

## 16. From earlier: a key that is not there

From *Dictionaries: looking things up by name*.

```python exec
id: from-earlier-a-key-that-is-not-there-1
counts = {"E": 9}
print(counts.get("Z"))
```

```predict
What will it print?

- 0
  - A missing count is zero.
- None
  - `.get()` with no default gives None.
- An error
  - Z is not a key.
```

<details class="dl-answer"><summary>why</summary>

The answer is `None`. `.get()` never raises a `KeyError`. With no
default, it returns `None`. `counts.get("Z", 0)` gives 0.

</details>
