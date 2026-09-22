---
title: "Finding Things — Practice"
practice_for: finding-things
year: "2026-2027"
version: 2026.08.23.1
---

# Finding Things — Practice

The answers are hidden in folds under each problem. Several problems ask
you to count comparisons, and not to write code. Those are the ones to
try on paper first.

## Scope

```python exec
id: scope-1
count = 0

def bump():
    count = 10          # a new, local count
    return count


print(bump(), count)
```

**1.** What does the cell above print? Why is `count` still 0 afterwards?

<details class="dl-answer"><summary>answer</summary>

`10 0`.

The line `count = 10` inside the function created a *new* variable. That
variable exists only while the function is running. An assignment inside
a function never changes a variable outside it, unless you use the word
`global`. If you find you need `global`, that is usually a sign that the
function should return a value instead.

</details>

**2.** What does this print?

```python
def add_item(items):
    items.append("new")


things = ["a", "b"]
add_item(things)
print(things)
```

<details class="dl-answer"><summary>answer</summary>

`['a', 'b', 'new']`.

This looks like it goes against the previous question, but it does not.
The function did not *assign* anything to `items`. It changed the list
that `items` refers to, and that is the same list that `things` refers
to.

So there are two different actions. Giving a name a new value, with
`=`, stays local to the function. Changing a list in place, with
something like `append`, is seen everywhere that list is used.

A function that changes its arguments without saying so often surprises
people. So decide on purpose whether a function returns a new list or
changes the list it was given, and make its name say which.

</details>

**3.** What is a pure function? Which of these are pure?

- (a) `def double(x): return x * 2`
- (b) `def add_to_log(msg): log.append(msg)`
- (c) `def roll(): return random.randint(1, 6)`
- (d) `def area(r): return 3.14159 * r * r`

<details class="dl-answer"><summary>answer</summary>

A pure function is one that depends only on its arguments, and changes
nothing outside itself. The same input always gives the same output. It
has no *side effects*: a side effect is any change a function makes
outside itself, such as adding to a list elsewhere in the program.

(a) and (d) are pure. (b) changes something outside itself. (c) gives a
different answer each time.

Pure functions are easy to test and easy to think about. Their answers
can also be saved and reused, because the answer to the same question
never changes. Still, the goal is to know which kind you are writing.
The two functions here that are not pure are useful and needed too.

</details>

## Linear Search

**4.** Write `linear_search(items, target)`. It returns the index of the target, or −1 if the target is not there.

<details class="dl-answer"><summary>answer</summary>

```python
def linear_search(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1
```

The `return -1` has to be outside the loop. If it were inside the loop,
the function would return −1 after checking only the first item.

</details>

**5.** Why use −1 for "not found", and not 0?

<details class="dl-answer"><summary>answer</summary>

Because 0 is a real index. It means "found at the start". A "not found"
marker has to be a value that could never be a real answer. No search
ever reports "found here" at index −1, so −1 is safe.

Many Python programmers would return `None` instead. `None` has an
advantage: if you use it as an index by mistake, Python stops with an
error. An index of −1 used by mistake points at the last element, with
no error at all.

</details>

**6.** Linear search looks through a list of 100 items. How many comparisons does it make when the target is first? When it is last? When it is not there? On average?

<details class="dl-answer"><summary>answer</summary>

1, 100, 100, and about 50.

The average assumes that the target is in the list, and that it is
equally likely to be anywhere. Now suppose half of your searches are for
things that are not there. Then the average is much closer to 100. This
is why it is often worth building a quick way to answer "not here".

</details>

**7.** Can you find the *last* place a target appears, and not the first?

<details class="dl-answer"><summary>answer</summary>

```python
def last_index(items, target):
    for i in range(len(items) - 1, -1, -1):
        if items[i] == target:
            return i
    return -1
```

This searches backwards. It returns at the first match it finds, and
that is the last one in the list.

Another way is to search forwards and remember the most recent match.
But that way always looks at every item, even when the match is at the
end.

</details>

## Binary Search

```python exec
id: binary-search-1
def binary_search(items, target):
    low, high, steps = 0, len(items) - 1, 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if items[mid] == target:
            return mid, steps
        if target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, steps


data = list(range(0, 1000, 3))
print(binary_search(data, 750))
print(binary_search(data, 751))
```

**8.** Trace binary search for 31 in `[3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]`. Write down each `mid` it looks at.

<details class="dl-answer"><summary>answer</summary>

The indexes run from 0 to 14, so the first `mid` is 7. The item at index
7 is 31. It is found in one comparison.

That is the best case. It happens because 31 sits exactly in the middle.
Try 89 instead: mid 7 (31), then 11 (55), then 13 (72), then 14 (89).
That takes four comparisons.

</details>

**9.** What goes wrong if the list is not sorted?

<details class="dl-answer"><summary>answer</summary>

It can report "not found" for items that are in the list, and it gives
no warning. For example, in `[5, 1, 9, 3, 7]` it finds 9, but it says
that 1 is not there.

That is the dangerous kind of wrong. Binary search has a *precondition*:
a precondition is something that must be true before a function runs,
for its answer to be right. Here, the list must be sorted. The function
has no way to tell that this was broken, so it gives a confident answer
anyway.

So the code that calls the function is responsible for sorting the
list. If that is not clear from the code, say it in the function's name,
or in the note that describes the function.

</details>

**10.** Why write `mid = (low + high) // 2`, and not `(low + high) / 2`?

<details class="dl-answer"><summary>answer</summary>

An index must be a whole number. `/` always gives a float, and
`items[3.5]` raises a `TypeError`.

There is a famous problem with this line in some other languages. In
those languages, whole numbers have a fixed size, and `low + high` can
become too big to store when the list is very large. The fix is
`low + (high - low) // 2`. That bug sat unnoticed in the standard Java
library for nine years. Python's whole numbers can grow as large as they
need to, so this does not happen in Python.

</details>

**11.** What is the largest number of comparisons binary search needs on 1,000 items? On 1,000,000?

<details class="dl-answer"><summary>answer</summary>

10 and 20.

Each step halves the range. So the count is the number of times you can
halve n before you reach 1. This is log₂n, rounded up. 2¹⁰ is 1,024, and
2²⁰ is 1,048,576.

Multiplying the data by a thousand adds only ten comparisons. That is
what logarithmic growth means. It is why binary search stays fast, however
big the data gets.

</details>

**12.** I am thinking of a whole number from 1 to 100. You may ask "Is it greater than X?". How many questions do you need to be sure of finding it?

<details class="dl-answer"><summary>answer</summary>

Seven.

Each question halves the range: 100 → 50 → 25 → 13 → 7 → 4 → 2 → 1. Six
questions can only be sure of finding one number out of 64, and 100 is
more than 64.

The general rule is that n yes-or-no questions can tell apart 2ⁿ
possibilities. This is the same fact as the cost of binary search. It is
also the reason a 7-bit code has 128 values.

</details>

**13.** Binary search needs sorted data, and sorting takes longer than one linear search. When is sorting worth it?

<details class="dl-answer"><summary>answer</summary>

When you search the same data more than a few times.

Sorting costs about n log n, once. Each linear search costs n. Each
binary search costs log n. So sorting pays for itself after about log n
searches. For a million items, that is after about twenty searches.

Every lookup table, index or dictionary you have used has already made
this trade for you.

If the data changes all the time and you search it only rarely, linear
search wins.

</details>

## Putting It Together

**14.** Change binary search so that, when the target is not there, it returns the place where the target *would* go.

<details class="dl-answer"><summary>answer</summary>

```python
def insertion_point(items, target):
    low, high = 0, len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low
```

When the loop ends, `low` is the index where the target belongs. Python's
`bisect.bisect_left` does the same thing. This is how we keep a list
sorted as new items arrive: search for the right position, then insert
the item there.

Notice that two boundaries changed. `high` starts at `len(items)`, not at
`len(items) - 1`. The loop test is `<`, not `<=`. Binary search breaks
easily if either choice is wrong. That is why it is worth writing it out
carefully, and not changing a version you half remember.

</details>

**15.** Use a list of 334 items. Count the comparisons each search makes when the target is at the start, in the middle, at the end, and not there.

<details class="dl-answer"><summary>answer</summary>

With `data = list(range(0, 1000, 3))`, which has 334 items:

| Target | Linear | Binary |
|---|---:|---:|
| 0 (first) | 1 | 8 |
| 498 (exact middle) | 167 | 1 |
| 999 (last) | 334 | 9 |
| 751 (not there) | 334 | 8 |

Binary search is *worse* than linear search when the target is first:
eight comparisons against one. That matters. If a few items are asked
for again and again, moving them to the front of the list beats any
clever method. Real systems use this idea to store popular answers
where they are quick to reach.

Notice also that a missing target costs binary search nearly its worst
case. It has to shrink the range to nothing before it can say no. Linear
search pays its full worst case for every missing target, every time.

</details>

**16.** Write a function that finds *all* the indexes where a target appears.

<details class="dl-answer"><summary>answer</summary>

```python
def all_indices(items, target):
    return [i for i, item in enumerate(items) if item == target]
```

This has to be a linear search, even on sorted data, because it cannot
stop early: it does not know how many matches there are.

On sorted data, there is another way. Binary search for the first match
and for the last match, and take everything between them. That is worth
doing only when the list is large and there are few matches.

</details>

**17.** Search a list of names for a name that is not there. Can you make the function report the closest match, and not only fail?

<details class="dl-answer"><summary>answer</summary>

```python
def closest(names, target):
    best, best_score = None, -1
    for name in names:
        score = sum(1 for a, b in zip(name.lower(), target.lower()) if a == b)
        if score > best_score:
            best, best_score = name, score
    return best
```

This counts the letters that match in the same positions. That is a
rough measure, but it is enough to catch a typing mistake in the first
few letters.

Real spell-checkers use *edit distance*. Edit distance is the number of
single-letter insertions, deletions and replacements it takes to turn one word
into another. It gives a much better answer, and it needs a much longer
function.

The lesson here is the decision, more than the measure: "not found" is
often not the most useful thing a search can say.

</details>
