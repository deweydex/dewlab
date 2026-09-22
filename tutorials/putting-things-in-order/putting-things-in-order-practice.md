---
title: "Putting Things in Order — Practice"
practice_for: putting-things-in-order
year: "2026-2027"
version: 2026.08.23.1
---

# Putting Things in Order — Practice

The answers are hidden in folds under each problem. Try tracing the
short ones by hand before you run anything. To *trace* a sort is to
follow it step by step on paper, writing down the list after each step.
If you have traced a sort once, you can find the mistakes in it. If you
have only run it, you usually cannot.

## Tracing

```python exec
id: tracing-1
def bubble_pass(items):
    """One pass of bubble sort, printing the list after each swap."""
    items = items.copy()
    for i in range(len(items) - 1):
        if items[i] > items[i + 1]:
            items[i], items[i + 1] = items[i + 1], items[i]
            print(items)
    return items


bubble_pass([5, 1, 4, 2, 8])
```

**1.** Trace one full pass of bubble sort over `[5, 1, 4, 2, 8]`. What is the list after the pass?

<details class="dl-answer"><summary>answer</summary>

`[1, 4, 2, 5, 8]`.

1. Compare 5 and 1: swap.
2. Compare 5 and 4: swap.
3. Compare 5 and 2: swap.
4. Compare 5 and 8: no swap.

The 5 moved all the way to its place in one pass. That movement is what
"bubbling" means. The largest value always reaches the end after the
first pass, so each pass after that can be one step shorter.

</details>

**2.** How many passes does bubble sort need on `[5, 1, 4, 2, 8]` before it is sorted?

<details class="dl-answer"><summary>answer</summary>

Two passes sort it. After the second pass, the list is `[1, 2, 4, 5, 8]`.

A plain bubble sort still does all four passes, because it never checks
whether the list is sorted. We can add a *flag*: a flag is a variable
that records whether something has happened, here "did this pass swap
anything?". With the flag, the sort stops as soon as a pass makes no
swaps. For a list that is already sorted, the work then grows like n,
and not like n².

</details>

**3.** Trace insertion sort over `[3, 1, 4, 1, 5]`. Write down the list after each item is placed.

<details class="dl-answer"><summary>answer</summary>

Start: `[3]`. A list of one item is always sorted.

Insert 1: `[1, 3]`. Insert 4: `[1, 3, 4]`. Insert 1: `[1, 1, 3, 4]`. Insert 5: `[1, 1, 3, 4, 5]`.

The second 1 landed *after* the first. Equal items keep the order they
started in. A sort that does this is *stable*, so insertion sort is
stable. Stability matters as soon as you sort the same data twice, by
two different things, such as by name and then by age.

</details>

**4.** Trace selection sort over `[64, 25, 12, 22, 11]`.

<details class="dl-answer"><summary>answer</summary>

1. The smallest is 11. Swap it into position 0: `[11, 25, 12, 22, 64]`.
2. The smallest of the rest is 12. Swap it into position 1: `[11, 12, 25, 22, 64]`.
3. The next smallest is 22: `[11, 12, 22, 25, 64]`.
4. The next is 25, which is already in place. The list is sorted.

There are four swaps at most, one for each position. Selection sort
makes the fewest swaps of the three sorts. That matters when a swap is
slow: for example, when each item is a large record, and not a small
number.

</details>

## Counting

```python exec
id: counting-1
def bubble_counted(items):
    items, comparisons, swaps = items.copy(), 0, 0
    n = len(items)
    for outer in range(n - 1):
        for i in range(n - 1 - outer):
            comparisons += 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swaps += 1
    return comparisons, swaps


for size in [10, 20, 40, 80]:
    reverse = list(range(size, 0, -1))
    ordered = list(range(1, size + 1))
    print(f"n={size:<4} reversed {bubble_counted(reverse)}   sorted {bubble_counted(ordered)}")
```

**5.** How many comparisons does bubble sort make on 10 items? On 20? What pattern do you see?

<details class="dl-answer"><summary>answer</summary>

45 and 190.

It is always n(n − 1)/2, whatever the data. The loops in the plain
version do not depend on what they find. When n doubles, the number of
comparisons goes up about four times. That is what n² growth looks like
up close.

</details>

**6.** Bubble sort makes the same number of comparisons on sorted data as on reversed data. Why? How would you fix it?

<details class="dl-answer"><summary>answer</summary>

The number of times each loop runs is fixed before the sort starts.
Only the swaps depend on the data. On 10 sorted items, it makes 45
comparisons and 0 swaps.

The fix is to notice when a pass makes no swaps:

```python
for outer in range(n - 1):
    swapped = False
    for i in range(n - 1 - outer):
        if items[i] > items[i + 1]:
            items[i], items[i + 1] = items[i + 1], items[i]
            swapped = True
    if not swapped:
        break
```

Now 10 sorted items cost one pass: 9 comparisons, not 45. Real data is
very often nearly sorted already. On that kind of data, these four extra
lines save a lot of work.

</details>

**7.** Which of the three sorts does best on data that is already sorted? Which does worst?

<details class="dl-answer"><summary>answer</summary>

Insertion sort does best. Each item is already in place, so it makes
n − 1 comparisons and moves nothing. That work grows like n. This is why
the fast sorting algorithms used in real software often use insertion
sort for the small pieces of the job, or as their last step.

Selection sort does worst, because it gains nothing from sorted data.
Every time, it looks through the whole rest of the list to find the
smallest item, whatever the order. It does n² work on every input, in
the best case and the worst.

Bubble sort with the early-stop flag matches insertion sort. Without the
flag, it matches selection sort.

</details>

**8.** For a million items, about how many comparisons does an n² sort make? At ten million comparisons a second, how long does that take?

<details class="dl-answer"><summary>answer</summary>

About 500,000,000,000, or five hundred billion.

At ten million a second, that is 50,000 seconds, or about fourteen
hours. An n log n sort on the same data makes about twenty million
comparisons. That takes two seconds.

This is the clearest example in the course of why the way the work
grows matters more than how fast each step is. However cleverly you
write the inner loop, you cannot close a gap that size.

</details>

## Writing Them

**9.** Can you write selection sort from nothing?

<details class="dl-answer"><summary>answer</summary>

```python
def selection_sort(items):
    items = items.copy()
    for i in range(len(items)):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j] < items[smallest]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items
```

Notice that it keeps the *index* of the smallest item, and not its
value. If it kept only the value, it could not do the swap, because it
would no longer know where that value came from.

</details>

**10.** Can you write insertion sort from nothing?

<details class="dl-answer"><summary>answer</summary>

```python
def insertion_sort(items):
    items = items.copy()
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]
            j = j - 1
        items[j + 1] = current
    return items
```

The `j >= 0` in the `while` condition is a guard. It stops the loop
from walking off the front of the list.

Put the guard first. Python checks the two sides of an `and` from left
to right, and stops as soon as one is false. If you swap the two sides,
then when `j` reaches −1, Python first reads `items[-1]`, the last
element, before the guard is checked. In Python the sort still gives the
right answer, because the guard then fails. But the code has read an
element it never meant to read, and in many other languages that is a
crash.

</details>

**11.** Why does each of these functions start with `items = items.copy()`?

<details class="dl-answer"><summary>answer</summary>

So that the function returns a sorted list, and leaves the caller's
list as it was.

Without the copy, `sorted_data = my_sort(data)` would also sort `data`.
Nobody wants that surprise. Python itself offers both ways. `sorted(x)`
returns a new list. `x.sort()` changes the list `x` itself. The two
names make the difference clear in the line where you use them.

</details>

**12.** Sort a list of names by length. Where two names have the same length, sort them alphabetically.

<details class="dl-answer"><summary>answer</summary>

```python
names = ["Ada", "Grace", "Alan", "Bob", "Margaret"]
print(sorted(names, key=lambda name: (len(name), name)))
```

`['Ada', 'Bob', 'Alan', 'Grace', 'Margaret']`.

`key=` tells `sorted` what to sort by. `lambda name: (len(name), name)`
is a small function with no name. For each name, it gives a pair of
values: the length, then the name itself. A pair like this is a *tuple*,
a fixed group of values in round brackets.

Sorting by a tuple sorts by its first value. It uses the second value
only to break ties.

The other way is to sort twice: first alphabetically, then by length.
That works only because Python's sort is stable, so it keeps the
alphabetical order among names of equal length.

</details>

## Recursion

**13.** Rewrite binary search so that it calls itself instead of looping.

<details class="dl-answer"><summary>answer</summary>

```python
def binary_search(items, target, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if items[mid] == target:
        return mid
    if target < items[mid]:
        return binary_search(items, target, low, mid - 1)
    return binary_search(items, target, mid + 1, high)
```

Every recursive function needs two things, and both are here:

1. A case that returns without calling itself again. Here there are two:
   `low > high`, and finding the target.
2. A call that always moves closer to that case. Here the range gets
   smaller with each call.

Leave out either one, and the function keeps calling itself until Python
stops it.

The default `high=None` is on purpose; `high=len(items) - 1` would not
work. Python works out a default value once, when the function is
defined. At that moment there is no `items` to measure.

</details>

**14.** Write a recursive factorial function. Where does it stop?

<details class="dl-answer"><summary>answer</summary>

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

It stops at 1. What if you wrote `n == 1` in place of `n <= 1`? That
works for positive numbers. But on 0 or a negative number, the function
calls itself forever, until Python stops it. A mistake like this often
shows up only after real users start giving the program real data.

Python's default recursion limit is about 1,000 calls. So
`factorial(5000)` raises a `RecursionError`, and gives no answer. The
loop version has no such limit.

</details>

**15.** Write shell sort. It is insertion sort with a gap that shrinks to 1.

<details class="dl-answer"><summary>answer</summary>

```python
def shell_sort(items):
    items = items.copy()
    gap = len(items) // 2
    while gap > 0:
        for i in range(gap, len(items)):
            current, j = items[i], i
            while j >= gap and items[j - gap] > current:
                items[j] = items[j - gap]
                j = j - gap
            items[j] = current
        gap = gap // 2
    return items
```

It is insertion sort with every `1` changed to `gap`. The large gaps
move items that are far from their place most of the way there, with
little work. By the time the gap is 1, the list is nearly sorted, and
insertion sort is fast on a list that is nearly sorted.

How fast shell sort is depends on the list of gaps it uses. Finding the
best list of gaps is still an open problem. This is one of the few
places in a first course where nobody yet knows the best method.

</details>

## Thinking About It

**16.** Can any sorting algorithm beat n log n comparisons in general?

<details class="dl-answer"><summary>answer</summary>

Not a sort that works by comparing items. This has been proved; it is
not only that nobody has found one yet.

Each comparison answers one yes-or-no question. So k comparisons can
tell apart at most 2ᵏ different orders. A list of n items can be in n!
different orders. To tell them all apart, a sort needs log₂(n!)
questions, and that works out to about n log n. So every sort that works
by comparing must make at least that many comparisons.

Some sorts do beat it, because they do not compare. Counting sort and
radix sort use the values themselves as positions. They are faster, but
they work only when you know something about the data: for example,
that it is whole numbers in a known range.

</details>

**17.** You have a sorted list of a million items, and one new item to add. What is the cheapest way to keep the list sorted?

<details class="dl-answer"><summary>answer</summary>

Use binary search to find the position, then insert the item there.
That takes about 20 comparisons.

Sorting the whole list again, with an n log n sort, would take about
twenty million. Most people first write "add it to the end, then sort".
In a loop that adds items one at a time, that is the difference between
instant and hopeless.

There is still a cost. Inserting into the middle of a Python list moves
every item after it along by one place. So this way needs few
comparisons, but the moving grows like n. When that moving becomes the
slowest part, the answer is a different way of storing the data.

</details>

**18.** Two students hand in sorts that both give correct output. One makes 45 comparisons on ten items, and the other makes 90. Is the second one wrong?

<details class="dl-answer"><summary>answer</summary>

No. It is correct, and it is slower. Those are two different
judgements.

Before you make it faster, ask: is ten items the real size? If it is,
the difference is a few millionths of a second, and code that is easy to
read matters more. If ten was only the test, and the real input is ten
million items, the difference is the whole assignment.

So, in order:

1. Make it correct.
2. Measure it.
3. Improve the part the measurement points to.

People are bad at guessing which part of a program is slow, even people
who have written programs for years.

</details>
