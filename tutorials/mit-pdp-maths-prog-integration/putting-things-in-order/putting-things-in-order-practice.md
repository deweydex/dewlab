---
title: "Putting Things in Order — Practice"
slug: putting-things-in-order-practice
practice_for: putting-things-in-order
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Putting Things in Order — Practice

Answers are folded. Trace the short ones by hand before running anything — a sort you have traced once is a sort you can debug, and one you have only run is not.

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

**1.** Trace one full pass of bubble sort over `[5, 1, 4, 2, 8]`. What is the list afterwards?

<details class="dl-answer"><summary>answer</summary>

`[1, 4, 2, 5, 8]`.

Compare 5 and 1 — swap. Compare 5 and 4 — swap. Compare 5 and 2 — swap. Compare 5 and 8 — leave.

The 5 travelled all the way to its place in one pass, which is what "bubbling" describes. The largest value always reaches the end after the first pass, which is why each subsequent pass can be one shorter.

</details>

**2.** How many passes does bubble sort need on `[5, 1, 4, 2, 8]` before it is sorted?

<details class="dl-answer"><summary>answer</summary>

Two passes get it sorted: after the second, `[1, 2, 4, 5, 8]`.

A plain bubble sort still does all four passes, because it does not check. Adding a "did I swap anything this pass" flag lets it stop as soon as a pass makes no swaps, which turns already-sorted input from n² work into n.

</details>

**3.** Trace insertion sort over `[3, 1, 4, 1, 5]`, writing the list after each item is placed.

<details class="dl-answer"><summary>answer</summary>

Start: `[3]` is trivially sorted.

Insert 1: `[1, 3]`. Insert 4: `[1, 3, 4]`. Insert 1: `[1, 1, 3, 4]`. Insert 5: `[1, 1, 3, 4, 5]`.

The second 1 landed *after* the first. That is what makes insertion sort stable — equal items keep their original order — and stability matters as soon as you sort the same data twice by different keys.

</details>

**4.** Trace selection sort over `[64, 25, 12, 22, 11]`.

<details class="dl-answer"><summary>answer</summary>

Find the smallest (11), swap with position 0: `[11, 25, 12, 22, 64]`.

Smallest of the rest (12), swap with position 1: `[11, 12, 25, 22, 64]`.

Then (22): `[11, 12, 22, 25, 64]`. Then (25): already there. Done.

Four swaps at most, one per position. Selection sort makes the fewest swaps of the three, which matters when a swap is expensive — moving large records rather than numbers, say.

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

**5.** How many comparisons does bubble sort make on 10 items? On 20? What is the pattern?

<details class="dl-answer"><summary>answer</summary>

45 and 190.

It is always n(n − 1)/2, regardless of the data — the plain version's loops do not depend on what it finds. Doubling n roughly quadruples the comparisons, which is what n² growth looks like from close up.

</details>

**6.** Bubble sort on already-sorted data makes the same number of comparisons as on reversed data. Why, and how would you fix it?

<details class="dl-answer"><summary>answer</summary>

Because the loops are fixed in advance; only the swaps depend on the data. On sorted input it makes 45 comparisons and 0 swaps.

The fix is to notice the zero:

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

Now sorted input costs one pass — 9 comparisons — instead of 45. On nearly-sorted data, which is extremely common in practice, this is a large win for four lines.

</details>

**7.** Which of the three sorts does best on already-sorted data, and which does worst?

<details class="dl-answer"><summary>answer</summary>

Insertion sort does best: each item is already in place, so it does n − 1 comparisons and no movement. That is linear, and it is why insertion sort is used as the finishing step inside industrial sorting algorithms.

Selection sort does worst in the sense that it cannot benefit at all — it scans the whole remaining list to find the minimum every time, whatever the order. It is n² on every input, best case and worst.

Bubble sort with the early-exit flag matches insertion sort; without it, it matches selection sort.

</details>

**8.** For a million items, roughly how many comparisons does an n² sort make? At ten million comparisons a second, how long is that?

<details class="dl-answer"><summary>answer</summary>

About 500,000,000,000 — five hundred billion.

At ten million a second that is 50,000 seconds, or about fourteen hours. An n log n sort on the same data does about twenty million comparisons: two seconds.

This is the clearest case in the course for why the growth rate matters more than the constant factor. No amount of writing the inner loop cleverly closes a gap of that size.

</details>

## Writing Them

**9.** Write selection sort from scratch.

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

Note it tracks the *index* of the smallest, not the value. Tracking the value means you cannot swap it back, because you no longer know where it came from.

</details>

**10.** Write insertion sort from scratch.

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

The `j >= 0` in the while condition is the guard that stops it walking off the front of the list. It has to come first: reverse the two halves of the `and` and the list is indexed at −1 before the check happens, which quietly reads the last element instead of failing.

</details>

**11.** Why does each of these start with `items = items.copy()`?

<details class="dl-answer"><summary>answer</summary>

So the function returns a sorted list and leaves the caller's list alone.

Without the copy, calling `sorted_data = my_sort(data)` would also sort `data`, which is a surprise nobody wants. Python's own library offers both: `sorted(x)` returns a new list, `x.sort()` changes it in place — and the naming makes the difference visible at the call site.

</details>

**12.** Sort a list of names by length, then alphabetically among equal lengths.

<details class="dl-answer"><summary>answer</summary>

```python
names = ["Ada", "Grace", "Alan", "Bob", "Margaret"]
print(sorted(names, key=lambda name: (len(name), name)))
```

`['Ada', 'Bob', 'Alan', 'Grace', 'Margaret']`.

Sorting by a tuple sorts by the first element, then uses the second only to break ties. The other route is to sort twice — alphabetically first, then by length — and that only works because Python's sort is stable, preserving the earlier order among equals.

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

Two things every recursive function needs, both present here: a case that returns without recursing (`low > high`, and finding it), and a call that is strictly closer to that case. Miss either and it runs until Python stops it.

The default `high=None` rather than `high=len(items) - 1` is deliberate — a default argument is evaluated once when the function is defined, so it could not refer to `items` anyway.

</details>

**14.** Write a recursive factorial, and say where it stops.

<details class="dl-answer"><summary>answer</summary>

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

It stops at 1. Using `n == 1` instead of `n <= 1` works for positive input and recurses forever on 0 or on a negative number, which is the sort of thing that only shows up in production.

Python's default recursion limit is about 1,000, so `factorial(5000)` raises rather than answering. The loop version has no such limit.

</details>

**15.** Implement shell sort — insertion sort with a gap that shrinks to 1.

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

It is insertion sort with every `1` replaced by `gap`. The large gaps move far-out-of-place items most of the way home cheaply; by the time the gap is 1, the list is nearly sorted and insertion sort's best case takes over.

Its actual performance depends on the sequence of gaps, and finding good ones is a genuinely open problem — one of the few places in a first course where the honest answer is that nobody knows the best method.

</details>

## Thinking About It

**16.** Is there a sorting algorithm that can beat n log n comparisons in general?

<details class="dl-answer"><summary>answer</summary>

Not by comparing items, no — and this is proved rather than merely unobserved.

Each comparison answers one yes-or-no question, so n comparisons can distinguish at most 2ⁿ arrangements. A list of n items has n! possible orders, and you need log₂(n!) questions to tell them apart, which works out to about n log n. Any comparison-based sort must make at least that many.

Sorts that beat it exist and do not compare: counting sort and radix sort use the values themselves as positions. They are faster and they only work when you know something about the data, such as that it is whole numbers in a known range.

</details>

**17.** You have a list of a million already-sorted items, and one new item to add. What is the cheapest way to keep it sorted?

<details class="dl-answer"><summary>answer</summary>

Binary search for the position, then insert there. About 20 comparisons.

Re-sorting the whole list would be twenty million. Appending and sorting is what most people write first, and on a loop that adds items one at a time it is the difference between instant and hopeless.

Inserting into the middle of a Python list still shifts everything after it, so this is fast in comparisons and linear in memory movement. When that becomes the bottleneck, the answer is a different data structure.

</details>

**18.** Two students hand in sorts that produce correct output. One does 45 comparisons on ten items, the other 90. Is the second one wrong?

<details class="dl-answer"><summary>answer</summary>

No — it is correct and slower, which are different judgements.

Worth asking before optimising: is ten items the real size? If it is, the difference is microseconds and readability wins. If ten was the test and the real input is ten million, the difference is the whole assignment.

Correctness first, then measure, then improve the part the measurement pointed at. Guessing which part is slow is famously unreliable, including among people who have been doing it for years.

</details>
