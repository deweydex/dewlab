---
title: "Finding bugs in bigger programs"
year: "2026-2027"
version: 2026.10.10.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  errors-from-lists-and-dictionaries:
    covers: [PDP-LO9]
  tracebacks-through-several-functions:
    covers: [PDP-LO9]
  the-dangerous-kind:
    covers: [PDP-LO9]
  debugging-habits:
    covers: [PDP-LO9]
    touches: [PDP-LO10]
---

# Finding bugs in bigger programs

This function is meant to count how often each item appears in a list. It
runs with no error. What does it print?

```python exec
id: a-count-that-forgets-1
def count_items(items):
    for item in items:
        counts = {}
        counts[item] = counts.get(item, 0) + 1
    return counts

print(count_items(["fig", "plum", "fig", "fig", "plum", "pear"]))
```

```predict
What will it print?

- {'fig': 3, 'plum': 2, 'pear': 1}
  - Each item is counted as the loop goes. There is
    [a closer look at this](tutorial:a-total-that-starts-again).
- {'pear': 1}
  - `counts = {}` runs every time round, so each item starts again.
- An error
  - `counts` is made inside the loop, so `return` cannot see it.
```

It prints `{'pear': 1}`. `counts = {}` is inside the *loop*{.term}, so every time
round, the *dictionary*{.term} is deleted and started again, and only the last
item survives. One line is indented one step too far, and nothing
complains.

[Reading an error message](tutorial:reading-an-error-message) met the three
kinds of wrong in *programs*{.term} of a few lines. Since then, programs have grown:
loops, lists, dictionaries, and functions that call functions. Bigger
programs bring new errors, longer *tracebacks*{.term}, and *logical errors*{.term} that hide
much better. Most cells on this page are meant to fail, or to give a wrong
answer. The exercise is to see why.

## Errors from lists and dictionaries

A list and a dictionary each give a new way to ask for something that is
not there.

| Error | What it means |
|---|---|
| `IndexError` | You asked for a position the list does not have. |
| `KeyError` | You asked for a *key*{.term} the dictionary does not have. The message shows the key you asked for. |
| `AttributeError` | You asked a value for something it does not have, such as a method. Often the value is not the type you thought. |
| `TypeError: '...' object is not callable` | You put brackets after something that is not a function. Often a name you gave a value was already the name of a function. |

### Your turn

Before you run each cell, decide which error it will raise, and write it in
the *comment*{.term}. Then run it, and read the last line.

```python exec
id: errors-from-lists-and-dictionaries-1
names = ["Ana", "Ben", "Cian"]
print(names[len(names)])
# I think it raises:
```

```python exec
id: errors-from-lists-and-dictionaries-2
ages = {"Ana": 31, "Ben": 27}
print(ages["ana"])
# I think it raises:
```

```python exec
id: errors-from-lists-and-dictionaries-3
basket = ["fig", "plum"]
basket.add("pear")
# I think it raises:
```

```python exec
id: errors-from-lists-and-dictionaries-4
scores = [30, 90, 250]
max = 0
for value in scores:
    if value > max:
        max = value
print(max(scores))
# I think it raises:
```

<details class="dl-answer"><summary>answer</summary>

It raises an `IndexError`. Three names have positions 0, 1 and 2, and
`len(names)` is 3. The last position is always one less than the length.
This slip is common enough to have a name, an *off-by-one error*.

It raises a `KeyError: 'ana'`, because the dictionary has `"Ana"`, with a
capital A. The message shows the key you asked for, so compare it, letter
by letter, with the keys there are.

It raises an `AttributeError`: `'list' object has no attribute 'add'`. A list grows
with `append`.

It raises a `TypeError: 'int' object is not callable`. The loop works, but
`max = 0` gave the name `max` to a number, so `max` is no longer Python's
function. Any name can be reused this way, which is a good reason never to
call a *variable*{.term} `max`, `sum`, `list` or `str`.

</details>

## Tracebacks through several functions

When the error happens inside a function called by another function,
Python shows the whole chain, one step for each call.

```python exec
id: reading-a-traceback-1
def add_tax(price, rate):
    return price * (1 + rate)


def basket_total(prices, rate):
    total = 0
    for price in prices:
        total = total + add_tax(price, rate)
    return total


print(basket_total([10, 20], 0.5))
print(basket_total([10, 20], "0.5"))
```

The first call works. The second prints several lines of traceback, and
they come in a deliberate order.

**Read it from the bottom.** The last line names the error. Above it, the
steps run from the outermost call down to the innermost, so the place the
error happened is nearest the bottom. Your program started at the top,
and it broke at the bottom. `in <module>` is the main part
of the program, and `in basket_total` and `in add_tax` mean a line inside
that function.

The error is in `add_tax`, on the arithmetic. But is the fault in
`add_tax`? It adds a rate to 1, which works for a number. The problem is
the rate it was given, `"0.5"`, which is a string. It came from the line at
the top. In a real program, it would come from `input()`, which always gives a
string. The bottom says *what* happened, and the lines above say *how* it
came to happen.

<div class="dl-drawn dl-traceback">
<p class="dl-tb-edge">The program started here, at the top.</p>
<div class="dl-tb-body">
<div class="dl-tb-row"><code>Traceback (most recent call last):</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell reading-a-traceback-1&gt;", line 13, in &lt;module&gt;</code></div>
<div class="dl-tb-row dl-tb-cause"><code>    print(basket_total([10, 20], "0.5"))</code><span class="dl-tb-note">the line that is responsible</span></div>
<div class="dl-tb-row dl-tb-cause"><code>          ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell reading-a-traceback-1&gt;", line 8, in basket_total</code></div>
<div class="dl-tb-row"><code>    total = total + add_tax(price, rate)</code></div>
<div class="dl-tb-row"><code>                    ~~~~~~~^^^^^^^^^^^^^</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell reading-a-traceback-1&gt;", line 2, in add_tax</code></div>
<div class="dl-tb-row dl-tb-failed"><code>    return price * (1 + rate)</code><span class="dl-tb-note">the line that failed</span></div>
<div class="dl-tb-row dl-tb-failed"><code>                    ~~^~~~~~</code></div>
<div class="dl-tb-row dl-tb-error"><code>TypeError: unsupported operand type(s) for +: 'int' and 'str'</code></div>
</div>
<p class="dl-tb-edge">The program broke here, at the bottom. Read that last line first.</p>
</div>

### Your turn

Run the cell, and read the traceback. Which line failed? Which line is
responsible? Write both in the comments at the end.

```python exec
id: tracebacks-through-several-functions-1
def average(marks):
    return sum(marks) / len(marks)


def best_group(groups):
    best = 0
    for index in range(len(groups)):
        if average(groups[index]) > average(groups[best]):
            best = index
    return best


print(best_group([[10, 20], [80, 90], [60, 60]]))
print(best_group([[10, 20], [], [60, 60]]))

# The line that failed:
# The line that is responsible:
```

<details class="dl-answer"><summary>answer</summary>

The line that failed is `return sum(marks) / len(marks)`, in `average`,
with a `ZeroDivisionError`. The line responsible is the last `print`,
because its groups include an empty list. Should `average` refuse an
empty list with a clear `ValueError`, as
[Designing and testing good functions](tutorial:building-reusable-tools)
did for `mean`? Or should the groups never have had one? That is a
question about the whole program, not one line.

</details>

## The dangerous kind

Logical errors hide better in bigger programs: inside a function, a loop,
or a condition written weeks ago. Here are three kinds that appear once
programs work with lists and functions. What does this one print?

```python exec
id: the-dangerous-kind-1
def has_vowel(word):
    for letter in word:
        if letter in "AEIOU":
            return True
        else:
            return False

print(has_vowel("EGG"), has_vowel("SKY"), has_vowel("TREE"))
```

```predict
What will it print?

- True False True
  - EGG and TREE have vowels, and SKY has none.
- True False False
  - The function gives its answer after looking at one letter.
```

It prints `True False False`. `return` ends the function at once, so the
`else` stops the search after the first letter. T is not a vowel, and TREE is
never looked at again. The `return False` belongs after the loop, once
every letter has been checked. It passes a *test*{.term} on `"EGG"` and on
`"SKY"`, which is why it survives.

The second kind changes something the caller did not expect to change.

```python exec
id: the-dangerous-kind-2
def median(numbers):
    numbers.sort()
    return numbers[len(numbers) // 2]

readings = [30, 10, 20]
print(median(readings))
print(readings)
```

The median it gives back is the one we want, but the caller's list has
been sorted as a side effect. There are two names for one list, as in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).
If the order of `readings` mattered, the time they were taken, say, it is
now lost, and nothing said so. `sorted(numbers)` would have left it alone.

The third kind changes a list while a loop uses it. `.remove(value)`
takes the first *element*{.term} equal to `value` out of a list. This is meant to
take every 0 out of a list.

```python exec
id: the-dangerous-kind-3
scores = [0, 0, 7, 0]
for value in scores:
    if value == 0:
        scores.remove(value)
print(scores)
```

It prints `[7, 0]`. One 0 survives. Each removal moves the rest of the
list one place left, under the loop, so the loop skips the element that
moved into the gap. A new list is safer:
`[value for value in scores if value != 0]`.

**This is why we check answers we already know.** Each of these gives a
believable answer. Only an answer you can check for yourself, on a case
chosen to catch it, shows that it is wrong.

### Your turn

Each task has a cell with a bug in it, and a second cell for your tests. A
test is an `assert` line. It does nothing when its two sides are equal, and
it stops with an `AssertionError` when they are not.

<div class="dl-world" data-world="secret-messages">

This function is meant to reverse a key, so that a code letter looks up
its plain letter. It runs, and it is wrong. Can you find the bug, and fix
it? Then add a test that would have caught it.

```python exec
id: your-turn-1--secret-messages
def reverse_key(key):
    """Give back key turned round: each value becomes a key."""
    reverse = {}
    for letter, code in key.items():
        reverse[letter] = code
    return reverse
```

```inputs
guess: yes
reverse_key({"A": "Q", "B": "W"})
reverse_key({"C": "E"})
reverse_key({})
```

```hint
after: 3 runs
Add `print(reverse_key({"C": "E"}))` under the function. What did you
expect it to print, and what did it print? Which line of the loop builds
the new pair?
```

```python exec
id: your-turn-1-tests--secret-messages
tests: your-turn-1--secret-messages
assert reverse_key({"C": "E"}) == {"E": "C"}
```

```solution
def reverse_key(key):
    """Give back key turned round: each value becomes a key."""
    reverse = {}
    for letter, code in key.items():
        reverse[code] = letter
    return reverse
---
The buggy version copied the key as it was. On an empty key, both versions
give `{}`, so a test on `{}` alone passes the bug. A test needs at least
one pair, and a pair where the two letters differ.
```

</div>

<div class="dl-world" data-world="pixel-art">

This function is meant to count the lit pixels in a row. It runs, and it
is wrong. Can you find the bug, and fix it? Then add a test that would
have caught it.

```python exec
id: your-turn-1--pixel-art
def lit_count(row):
    """Give back how many pixels in row are "#"."""
    count = 0
    for index in range(1, len(row)):
        if row[index] == "#":
            count = count + 1
    return count
```

```inputs
guess: yes
lit_count("#.#")
lit_count(".##")
lit_count("")
```

```hint
after: 3 runs
Add `print(lit_count("#.#"))` under the function. How many `#` does the
row have, and what did it print? Which positions does
`range(1, len(row))` give you?
```

```python exec
id: your-turn-1-tests--pixel-art
tests: your-turn-1--pixel-art
assert lit_count("###") == 3
```

```solution
def lit_count(row):
    """Give back how many pixels in row are "#"."""
    count = 0
    for pixel in row:
        if pixel == "#":
            count = count + 1
    return count
---
`range(1, len(row))` starts at index 1, so the first pixel is never
looked at. `".##"` gives the right answer with the bug, because its first
pixel is dark: a test needs a row that starts lit.
```

</div>

## Debugging habits

A mistake in a program is often called a *bug*. When we find bugs and fix
them, we call it *debugging*. When a program gives a wrong answer and no error,
where do we start? Two habits help more than any others.

**The first habit: print the values in the middle.** This is meant to give
the average length of the words in a sentence. The words in
`"play is at noon"` have 4, 2, 2 and 4 letters, so the average is 3. What
does it print?

```python exec
id: debugging-habits-1
def average_word_length(sentence):
    letters = 0
    for character in sentence:
        letters = letters + 1
    words = len(sentence.split())
    return letters / words

print(average_word_length("play is at noon"))
```

It prints 3.75. Somewhere a number is wrong, but which? Make the program
tell you. Add a labelled `print` for each value in the middle, just before
the `return`:

```python exec
id: debugging-habits-2
def average_word_length(sentence):
    letters = 0
    for character in sentence:
        letters = letters + 1
    words = len(sentence.split())
    print("letters:", letters, "words:", words)
    return letters / words

print(average_word_length("play is at noon"))
```

`words` is 4, and there are four words. `letters` is 15, and there are
only 12 letters. The loop counted the three spaces too. A label on each `print`
matters, because a column of bare numbers is hard to read. When the bug is
fixed, take the extra `print` out again.

**The second habit: test the small pieces.** A long function can go wrong
in many places. Short functions, each tested on its own with `assert`, can
each go wrong in only one, and a failing test points straight at it.

### Your turn

This program turns marks into grades, with three functions. It runs, and
prints the wrong thing. The first group of marks should print `DCA`, and
the second `ABD`.

1. Can you test `grade` on its own, with `90`, `65`, `50` and `5`?
2. Can you test `grades_for` on its own, with `[10, 50, 90]`?
3. Which function has the bug? Can you fix it?

Put your tests in the cell under the program.

```python exec
id: your-turn-2
def grade(mark):
    if mark >= 80:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 40:
        return "C"
    return "D"


def grades_for(marks):
    line = ""
    for mark in marks:
        line = line + grade(mark)
        return line


def report(groups):
    for marks in groups:
        print(grades_for(marks))


report([[10, 50, 90], [95, 65, 5]])
```

```inputs
guess: yes
grade(65)
grades_for([10, 50, 90])
grades_for([])
```

```python exec
id: your-turn-2-tests
tests: your-turn-2
assert grade(90) == "A"
```

```hint
after: 3 runs
`grade` gives the grade you expect for all four marks. What does
`grades_for` give back, and after how many marks? Look at how far its
`return` is indented.
```

```solution
def grade(mark):
    if mark >= 80:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 40:
        return "C"
    return "D"


def grades_for(marks):
    line = ""
    for mark in marks:
        line = line + grade(mark)
    return line


def report(groups):
    for marks in groups:
        print(grades_for(marks))


report([[10, 50, 90], [95, 65, 5]])
---
The `return` was inside the loop, so `grades_for` gave back its line after
one mark. With an empty list, the loop never ran, so the buggy version
gave back `None`. Moved out one step, the `return` runs once the loop has
finished.
```

## Looking back

Which of this page's bugs would a test have caught first, and which would
only a person reading the output notice? What does that say about the
tests worth writing?

Here is a challenge. This program has three bugs, and it runs. The comment says
what it is meant to do. Can you find all three, and write a test that
catches each one?

```python challenge
# top_group gives back the first group with the most passes (marks of 40 or more).
def pass_count(marks):
    count = 0
    for index in range(len(marks) - 1):
        if marks[index] >= 40:
            count = count + 1
    return count

def top_group(groups):
    best = groups[0]
    for marks in groups:
        if pass_count(marks) >= pass_count(best):
            best = marks
        return best

groups = [[50, 20, 70, 10], [90, 80, 60, 40], [55, 45, 30, 20], [55, 45, 60, 70]]
print(top_group(groups))
```

The next page, [How programming languages came to be](tutorial:how-we-got-here),
leaves our own programs for a while. It looks at the people who made
programming possible, and at what the machine underneath is doing.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Evans, J. (2022). *The Pocket Guide to Debugging*. Wizard Zines.
<https://wizardzines.com/zines/debugging-guide/>. It is short and
illustrated. It is full of the habits on this page, and many more, from
someone who debugs for a living.

Schafer, C. (2015). *Python Tutorial: Using Try/Except Blocks for Error
Handling*. <https://www.youtube.com/watch?v=NIWwJbo-9_8>. It shows how to
handle, on purpose, the errors this page teaches you to read, instead of
rewriting the line that raised them.
