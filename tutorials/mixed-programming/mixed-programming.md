---
title: "Mixed problems: programming"
practice_across:
  - first-steps
  - storing-and-computing
  - making-decisions
  - reading-an-error-message
  - repeating-yourself
  - writing-your-own-functions
  - lists-and-sequences
  - comprehensions-and-grids
  - looking-things-up-by-name
  - finding-things
  - putting-things-in-order
  - building-reusable-tools
  - when-it-goes-wrong
  - how-we-got-here
year: "2026-2027"
version: 2026.09.26.1
---

# Mixed problems: programming

Every problem here needs more than one page of the series, and none of
them says which. That is the point: seeing that a problem wants a loop
with a decision inside it, or a count followed by a sort, is a different
skill from being able to write either.

Most problems have more than one good answer. Where a problem hides a
decision, the solution says what it decided and why, rather than
pretending there was only one route. Try each problem before you open
anything under it.

## 1. Even, odd and zero

Can you write `parity_counts(numbers)`, which gives back a list of three
counts: how many are even, how many odd, and how many are zero?

```python exec
id: even-odd-and-zero-1
def parity_counts(numbers):
    return [0, 0, 0]
```

```inputs
guess: yes
parity_counts([1, 2, 3, 4])
parity_counts([0, 0, 5])
parity_counts([])
```

```solution
def parity_counts(numbers):
    """Give back [even, odd, zero]. Zero counts as even, and again as zero."""
    even = 0
    zero = 0
    for number in numbers:
        if number % 2 == 0:
            even = even + 1
        if number == 0:
            zero = zero + 1
    return [even, len(numbers) - even, zero]
---
The question hides a decision: is zero even, or a category of its own? It
is even, since it divides by 2 with nothing left over. Counting it twice,
as here, keeps "even" meaning even, and makes the three counts add up to
more than the length. Counting it only as zero does the opposite. Either
is fair, once the docstring says which.
```

## 2. Above the average

Can you write `above_average(marks)`, which gives back the marks above the
average, and an empty list for no marks?

```python exec
id: above-the-average-1
def above_average(marks):
    return []
```

```inputs
guess: yes
above_average([4, 8, 15, 16, 23, 42])
above_average([5, 5, 5])
above_average([])
```

```solution
def above_average(marks):
    """Give back the marks above the average. No marks gives []."""
    if len(marks) == 0:
        return []
    average = sum(marks) / len(marks)
    return [mark for mark in marks if mark > average]
---
Two passes, unavoidably: the average needs every mark before any can be
compared with it. An empty list gives `[]` rather than an error, because
"which marks are above average" has an answer for no marks, even though
"what is the average" does not.
```

## 3. The second largest

Can you write `second_largest(numbers)`? Decide first what `[5, 5, 3]`
should give: 5 or 3.

```python exec
id: the-second-largest-1
def second_largest(numbers):
    return None
```

```inputs
guess: yes
second_largest([3, 9, 4])
second_largest([5, 5, 3])
second_largest([7])
```

```hint
Build a list of the different values first, with each one once. Then sort
it, largest first. What should come back when there is only one value?
```

```solution
title: with what you've met so far
def second_largest(numbers):
    """The second-largest different value, or None if there is none."""
    different = []
    for number in numbers:
        if number not in different:
            different.append(number)
    different = sorted(different, reverse=True)
    if len(different) < 2:
        return None
    return different[1]
---
This reads "second largest" as the second-largest *different* value, so
`[5, 5, 3]` gives 3. Reading it the other way gives 5. Both are fair, and
they disagree, so the docstring has to say which.
```

```solution
title: a shorter way you'll meet later
def second_largest(numbers):
    """The second-largest different value, or None if there is none."""
    different = sorted(set(numbers), reverse=True)
    if len(different) < 2:
        return None
    return different[1]
---
`set()` keeps one of each value, with no order, which is why it is sorted
after.
```

## 4. FizzBuzz

Can you write `fizzbuzz(n)`, which gives back `"Fizz"` for a multiple of 3,
`"Buzz"` for a multiple of 5, `"FizzBuzz"` for a multiple of both, and the
number as a string otherwise?

```python exec
id: fizzbuzz-1
def fizzbuzz(n):
    return str(n)
```

```inputs
guess: yes
fizzbuzz(3)
fizzbuzz(5)
fizzbuzz(15)
fizzbuzz(7)
```

```solution
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return str(n)
---
The order is the whole problem. Test for 15 last, and 15 is caught first
by `n % 3 == 0`, and gives `Fizz`.
```

## 5. Threes and fives

How many whole numbers below 1,000 can be divided by 3 or by 5? Can you
set `count` and `total`?

```python exec
id: threes-and-fives-1
count = 0
total = 0

print(count, total)
```

```inputs
count
total
```

```solution
count = 0
total = 0
for number in range(1, 1000):
    if number % 3 == 0 or number % 5 == 0:
        count = count + 1
        total = total + number
print(count, total)
---
466 numbers, adding up to 233,168. There is a way with no loop: the
multiples of 3 add up to 3 × (1 + 2 + … + 333), the multiples of 5 to
5 × (1 + … + 199), and the multiples of 15 have been counted twice, so
they come off once. Add both, take away the overlap: the same idea as the
union of two sets.
```

## 6. Two discounts

A shop takes 10% off orders over €50, and a further €5 off with a loyalty
card. Can you write `to_pay(total, loyalty)`?

```python exec
id: two-discounts-1
def to_pay(total, loyalty):
    return total
```

```inputs
guess: yes
to_pay(60, False)
to_pay(60, True)
to_pay(50, True)
to_pay(3, True)
```

```solution
def to_pay(total, loyalty):
    """The price after 10% off over €50, then €5 off with a loyalty card.

    Exactly €50 is not over €50. The price never goes below 0.
    """
    if total > 50:
        total = total * 0.9
    if loyalty:
        total = max(0, total - 5)
    return round(total, 2)
---
Three decisions the question did not make. Is €50 "over 50"? Taken as no.
Does the €5 come off before or after the 10%? After, which costs the
customer more. Can the price go below zero? No. Real specifications are
like this, and a docstring is what turns a guess into a decision somebody
can correct.
```

## 7. The longest word, however it is written

Can you write `longest_word(sentence)`, which gives back the longest word
in capitals, with any punctuation left off?

```python exec
id: the-longest-word-however-it-is-written-1
def longest_word(sentence):
    return ""
```

```inputs
guess: yes
longest_word("Meet me, at the bridge!")
longest_word("a bb cc")
longest_word("... !!")
```

```hint
`.upper()` puts the sentence in capitals, and `.split()` cuts it into
words. In a word in capitals, `character.isupper()` is `True` for the
letters, and `False` for punctuation.
```

```solution
def longest_word(sentence):
    """The longest word, in capitals, without punctuation. Ties go to the first."""
    best = ""
    for word in sentence.upper().split():
        letters = ""
        for character in word:
            if character.isupper():
                letters = letters + character
        if len(letters) > len(best):
            best = letters
    return best
---
BRIDGE. A loop, a decision inside it, a string built up, and a best so
far: four pages in one function. A "word" that is only punctuation cleans
to nothing, so it never wins.
```

## 8. The three commonest words

Can you set `top` to the three most common words in this sentence, most
common first?

```python exec
id: the-three-commonest-words-1
sentence = "the cat sat on the mat and the dog sat on the cat"
top = []

print(top)
```

```inputs
top
```

```hint
Count the words into a dictionary. Then sort its keys with a `key=`
function that gives each word's count, largest first, and take a slice.
```

```solution
sentence = "the cat sat on the mat and the dog sat on the cat"
counts = {}
for word in sentence.split():
    counts[word] = counts.get(word, 0) + 1

def how_often(word):
    return counts[word]

top = sorted(counts, key=how_often, reverse=True)[:3]
print(top)
---
`['the', 'cat', 'sat']`. cat, sat and on are all used twice. The sort is
stable, so they stay in the order they were first counted, and on misses
out. A different tie rule would give a different third word.
```

## 9. Anagrams

Two words are *anagrams* if they use the same letters, as LISTEN and SILENT
do. Can you write `same_letters(a, b)`?

```python exec
id: anagrams-1
def same_letters(a, b):
    return False
```

```inputs
guess: yes
same_letters("LISTEN", "SILENT")
same_letters("LOOP", "POLO")
same_letters("LOOP", "PLOP")
```

```solution
title: with what you've met so far
def count_letters(word):
    counts = {}
    for letter in word:
        counts[letter] = counts.get(letter, 0) + 1
    return counts

def same_letters(a, b):
    return count_letters(a) == count_letters(b)
---
Two dictionaries are equal when they have the same keys with the same
values, whatever order the pairs were added in.
```

```solution
title: another way
def same_letters(a, b):
    return sorted(a) == sorted(b)
---
Sorting both puts the same letters in the same order, if they are the same
letters.
```

## 10. Ten thousand lookups

You have a sorted list of a million numbers, and 10,000 numbers to look up
in it. How would you do it, and how much faster is that than the obvious
way?

<details class="dl-answer"><summary>answer</summary>

Binary search each one: about 10,000 × 20 = 200,000 comparisons. Linear
search each one: about 10,000 × 500,000 = five billion, twenty-five
thousand times slower. If the list were not sorted, sorting it first would
cost about twenty million comparisons, and 10,000 lookups would still
repay it many times over.

</details>

## 11. A pair that adds up

Can you write `pair_summing_to(numbers, target)`, which gives back two
numbers from the list that add up to `target`, or `None`?

```python exec
id: a-pair-that-adds-up-1
def pair_summing_to(numbers, target):
    return None
```

```inputs
guess: yes
pair_summing_to([2, 7, 11, 15], 9)
pair_summing_to([3, 5, 8], 100)
pair_summing_to([], 5)
```

```solution
title: with what you've met so far
def pair_summing_to(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [numbers[i], numbers[j]]
    return None
---
Every pair, one loop inside another: for n numbers, about n²/2 pairs.
```

```solution
title: a faster way
def pair_summing_to(numbers, target):
    seen = {}
    for number in numbers:
        if target - number in seen:
            return [target - number, number]
        seen[number] = True
    return None
---
One pass. For each number, it asks whether the number that would complete
it has been seen already, which is a dictionary lookup, not a search. The
arithmetic is the same: the question changed.
```

## 12. By surname

Can you set `by_surname` to these names sorted by the last word of each?

```python exec
id: by-surname-1
names = ["Ada Lovelace", "Alan Turing", "Grace Hopper", "Karen Sparck Jones"]
by_surname = []

print(by_surname)
```

```inputs
by_surname
```

```solution
names = ["Ada Lovelace", "Alan Turing", "Grace Hopper", "Karen Sparck Jones"]

def surname(name):
    return name.split()[-1]

by_surname = sorted(names, key=surname)
print(by_surname)
---
Hopper, Jones, Lovelace, Turing. Taking the last word is a guess about
names: it is wrong for Sparck Jones, whose surname is two words, for names
written family name first, and for anybody with one name. It works for
most of this list. "Surname" is not something every name in the world has.
```

## 13. Merging two sorted lists

Can you write `merge(a, b)`, which gives back one sorted list from two
sorted lists, without sorting the result?

```python exec
id: merging-two-sorted-lists-1
def merge(a, b):
    return []
```

```inputs
guess: yes
merge([1, 4, 9], [2, 3, 10])
merge([], [5])
merge([2, 2], [2])
```

```hint
Keep an index into each list. Each time round, take the smaller of the two
front elements, and move that list's index on. When one list runs out,
the rest of the other goes on the end.
```

```solution
def merge(a, b):
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i = i + 1
        else:
            result.append(b[j])
            j = j + 1
    return result + a[i:] + b[j:]
---
This is the heart of *merge sort*: split a list until every piece has one
element, then merge the pieces back up, which takes about n log n steps
instead of n². `<=`, not `<`, keeps it stable: equal elements keep the
order they came in.
```

## 14. Where the None came from

This program stops. Which line failed, and which line is responsible?

```python exec
id: where-the-none-came-from-1
def average(values):
    print(sum(values) / len(values))


def report(name, values):
    return name + ": " + str(round(average(values), 1))


print(report("row 1", [30, 90, 250]))
```

<details class="dl-answer"><summary>answer</summary>

It prints 123.33… and then stops with a `TypeError`, in `report`: `round`
cannot round `None`. The line responsible is the `print` inside
`average`, which should be a `return`. `average` shows its answer and then
gives back `None`, so the number never reaches `report`.

</details>

## 15. A list that will not empty

```python exec
id: a-list-that-will-not-empty-1
def start_again(items):
    items = []

row = [1, 2, 3]
start_again(row)
print(row)
```

```predict
What will it print?

- []
  - The function emptied the list.
- [1, 2, 3]
  - `items = []` gave the name `items` a new list, inside the function.
```

<details class="dl-answer"><summary>why</summary>

`[1, 2, 3]`. `items = []` gives the local name a new, empty list, and
leaves the caller's list alone. Changing a list in place, as `append()`
does, would have been seen by the caller. Giving a name a new value never
is. Two pages, scope and two names for one list, meet in two lines.

</details>

## 16. Any base

Can you write `to_base(n, base)`, which writes a whole number in any base
from 2 to 16, with the digits `0123456789ABCDEF`?

```python exec
id: any-base-1
def to_base(n, base):
    digits = "0123456789ABCDEF"
    return ""
```

```inputs
guess: yes
to_base(42, 2)
to_base(255, 16)
to_base(42, 8)
to_base(0, 2)
```

```hint
It is `to_binary` with `base` in place of 2. `n % base` is the last digit,
and `digits[n % base]` writes it.
```

```solution
def to_base(n, base):
    digits = "0123456789ABCDEF"
    if n == 0:
        return "0"
    text = ""
    while n > 0:
        text = digits[n % base] + text
        n = n // base
    return text
---
`101010`, `FF` and `52`. One function covers binary, hex and every base
between: the base is a parameter, not a new program.
```

## 17. A week of steps

Can you write `report(steps)`, which gives back a dictionary with the day
of the most steps and of the fewest, counting from day 1, how many days
were above the average, and the longest run of days above it in a row?

```python exec
id: a-week-of-steps-1
def report(steps):
    return {}

week = [4200, 8100, 9000, 3000, 7600, 8800, 9100, 2000]
print(report(week))
```

```inputs
guess: yes
report(week)
report([5000])
```

```hint
The run needs two numbers as the loop goes: the current run, and the best
so far. When a day is above the average, the current run grows. When it is
not, it goes back to 0. Compare it with the best every time round.
```

```solution
def report(steps):
    average = sum(steps) / len(steps)
    run = 0
    longest = 0
    above = 0
    for day in steps:
        if day > average:
            run = run + 1
            above = above + 1
        else:
            run = 0
        longest = max(longest, run)
    return {
        "most": steps.index(max(steps)) + 1,
        "fewest": steps.index(min(steps)) + 1,
        "above average": above,
        "longest run": longest,
    }

week = [4200, 8100, 9000, 3000, 7600, 8800, 9100, 2000]
print(report(week))
---
Day 7 has the most and day 8 the fewest; five days are above the average
of 6,475; the longest run is three. The current run and the best so far is
the pattern worth taking away: the same lines find the longest run of
anything.
```

## 18. Sorted, and the same things

Can you write `is_sorted(items)`, and `same_items(a, b)`, which says
whether two lists hold the same elements in any order?

```python exec
id: sorted-and-the-same-things-1
def is_sorted(items):
    return False

def same_items(a, b):
    return False
```

```inputs
guess: yes
is_sorted([1, 2, 2, 5])
is_sorted([3, 1])
is_sorted([])
same_items([3, 1, 2], [1, 2, 3])
same_items([1, 1], [1])
```

```solution
title: with what you've met so far
def is_sorted(items):
    for i in range(len(items) - 1):
        if items[i] > items[i + 1]:
            return False
    return True

def same_items(a, b):
    return sorted(a) == sorted(b)
---
These two together are how to test a sort. Its answer must be sorted *and*
hold what went in. `is_sorted` alone accepts a sort that gives back `[]`
every time, and `same_items` alone accepts one that does nothing.
```

```solution
title: a shorter way you'll meet later
def is_sorted(items):
    return all(items[i] <= items[i + 1] for i in range(len(items) - 1))

def same_items(a, b):
    return sorted(a) == sorted(b)
---
`all()` is `True` when every value it is given is true.
```

## 19. The missing number

A list holds every whole number from 1 to `n` except one. Can you write
`missing(numbers, n)`, doing as little work as you can?

```python exec
id: the-missing-number-1
def missing(numbers, n):
    return 0
```

```inputs
guess: yes
missing([1, 2, 4, 5], 5)
missing([2, 3], 3)
missing([], 1)
```

```hint
You know what the list *should* add up to: 1 + 2 + … + n is n(n + 1)/2,
from [Repeating steps with loops](tutorial:repeating-yourself). What is
the difference between that and what it does add up to?
```

```solution
def missing(numbers, n):
    return n * (n + 1) // 2 - sum(numbers)
---
One pass, no sorting. Sorting and looking for the gap works too, and so
does checking each number from 1 to n. The sum uses something you *know*
about the data, not only what you can see in it, and that is usually where
the good answer is.
```

## 20. Somebody else's function

You are handed somebody else's function. It works. What would you check
before you use it in your own code?

<details class="dl-answer"><summary>answer</summary>

What it does with nothing: an empty list, a zero, an empty string. Whether
it changes what it is given, or only reads it. Whether it gives the same
answer every time. And what it does with input it was not designed for: a
negative where a count was expected, text where a number was. None of this
is about whether it is right on the cases it was written for. It is about
the edges, where code you did not write meets data you did not expect.

</details>
