---
title: "Sorting a list: bubble, insertion and selection sort"
year: "2026-2027"
version: 2026.09.22.1
covers:
  bubble-sort-let-things-rise:
    covers: [MIT-6.8]
  insertion-sort-sort-like-you-sort-cards:
    covers: [MIT-6.8]
  selection-sort-find-the-smallest:
    covers: [MIT-6.8]
  comparing-our-sorts:
    covers: [MIT-6.8, CMPS-LO5]
  optional-challenges:
    touches: [MIT-6.8]
---

# Sorting a list: bubble, insertion and selection sort

In [Searching a list: linear and binary search](tutorial:finding-things) we saw that binary search is
very fast, but it needs sorted data. So how do we sort a list?

Sorting is one of the most studied problems in computer science. It is
not hard to sort a list. What makes sorting interesting is that there are
many ways to do it, and as the data grows, some ways become far slower
than others.

On this page we:

- learn how to swap two elements in a list
- build three classic sorting algorithms: bubble sort, insertion sort
  and selection sort
- count the work each one does, and see how that work grows

Each algorithm thinks about the problem in a different way, and each one
teaches us something about how to design algorithms.

## The Swap: A Small but Essential Tool

Before we sort anything, we need a way to *swap* two elements in a list.
To swap two elements is to exchange their positions. Python can do this
in one line:

```python exec
id: the-swap-a-small-but-essential-tool-1
numbers = [10, 20, 30, 40, 50]
print("Before:", numbers)

# Swap elements at index 1 and index 3
numbers[1], numbers[3] = numbers[3], numbers[1]
print("After: ", numbers)
```

A line like `a, b = b, a` works because Python first works out the whole
right side. Only then does it assign the values to the left side.

Many other languages need a temporary variable to do the same thing:

```
temp = a
a = b
b = temp
```

Both ways work. The Python way says the same thing with fewer parts.

## Bubble Sort: Let Things Rise

*Bubble sort* is a sorting algorithm that walks through the list and
compares each pair of neighbours. If a pair is in the wrong order, it
swaps them. After one full pass, the largest element has "bubbled up" to
the end. Then it repeats, until the list is sorted.

Let's watch one pass, step by step. In this list, the largest number,
90, is already at the end. Look at 64, the next largest, which starts at
the front. Where do you think 64 will be after one pass? Run the cell to
check.

```python exec
id: bubble-sort-let-things-rise-1
# A single pass of bubble sort, with commentary
data = [64, 34, 25, 12, 22, 11, 90]
print("Start:", data)

for i in range(len(data) - 1):
    if data[i] > data[i + 1]:
        data[i], data[i + 1] = data[i + 1], data[i]
        print("  Swapped index " + str(i) + " and " + str(i + 1) + ":", data)
    else:
        print("  No swap at index " + str(i) + ":", data)

print("After one pass:", data)
```

The 64 moves one place to the right at every swap, until it meets 90. A
pass always carries the largest element it meets along with it. So after
one pass, the largest element is at the end. Here that was 90, which
started there.

One pass is not enough to sort the whole list. But after each pass, one
more element is in its final place. So a list of n elements needs at most
n − 1 passes.

That claim is worth watching, and not only believing. Here is the same
sort again, all the way to the end. A bar, `|`, marks the part that has
settled into place.

```python exec
id: bubble-sort-let-things-rise-2
data = [64, 34, 25, 12, 22, 11, 90]
comparisons = 0

print("Start:            ", data, "|", [])

for pass_number in range(len(data) - 1):
    # Everything past this point settled on an earlier pass, so there is
    # no reason to look at it again. That is why each pass is shorter.
    still_to_check = len(data) - pass_number
    swaps = 0

    for i in range(still_to_check - 1):
        comparisons = comparisons + 1
        if data[i] > data[i + 1]:
            data[i], data[i + 1] = data[i + 1], data[i]
            swaps = swaps + 1

    moving = data[:still_to_check - 1]
    settled = data[still_to_check - 1:]
    print("After pass", pass_number + 1, ":", moving, "|", settled,
          "  compared:", still_to_check - 1, " swapped:", swaps)

print("Comparisons in total:", comparisons)
```

Here are three things to look for:

1. The bar moves one place to the left on every pass. That is the claim
   above.
2. The number of comparisons drops by one on every pass, for the same
   reason.
3. The last pass swaps nothing. The list was already sorted before that
   pass ran, but bubble sort had no way to know.

What happens with a list of your own? Change `data` and run the cell
again. Try a list that is already sorted, and a list in reverse order.

### Your turn

Here is the pseudocode for a function `bubble_sort(items)`. It returns
the list in *ascending order*, which means from smallest to largest.

```
FOR each pass from 0 to length-2:
    FOR each index i from 0 to length-2-pass:
        IF items[i] > items[i+1]:
            SWAP them
RETURN items
```

Why can the inner loop stop earlier on each pass? At the end of every
pass, the largest element that is not yet in place reaches its final
position. So each time, there is one fewer place worth looking.

1. In the first cell, write `bubble_sort(items)` from the pseudocode.
2. In the second cell, test it. The comment there lists some good test
   cases.

```python exec
id: your-turn-1
# Your bubble_sort function
```

```python exec
id: your-turn-2
# Worth testing on: already sorted, reverse sorted, all the same value,
# a single element, and an empty list. The last two are where sorts break.
```

## Insertion Sort: Sort Like You Sort Cards

*Insertion sort* is a sorting algorithm that works the way most people
sort a hand of playing cards. You pick up the cards one at a time. You
put each new card into its correct place among the cards you have
already sorted.

In a list, insertion sort keeps a sorted part at the start of the list.
It takes the next element that is not yet sorted. Then it walks that
element backwards through the sorted part, until it finds the right
place.

### Your turn

How might `insertion_sort(items)` look? Here is the pseudocode:

```
FOR each index i from 1 to length-1:
    SET key = items[i]
    SET j = i - 1
    WHILE j >= 0 AND items[j] > key:
        MOVE items[j] one position to the right
        DECREASE j by 1
    PLACE key at position j+1
RETURN items
```

The variable `key` holds the element we are inserting right now. We move
each larger element one place to the right, until we find where `key`
belongs.

1. In the first cell, write `insertion_sort(items)`.
2. In the second cell, test it with the same cases you used for bubble
   sort.

```python exec
id: your-turn-3
# Your insertion_sort function
```

```python exec
id: your-turn-4
# Test it with the same cases as bubble sort
```

## Selection Sort: Find the Smallest

*Selection sort* is a sorting algorithm that finds the smallest element
in the part of the list that is not yet sorted. It swaps that element
into the next place in the sorted part. Then it finds the next smallest,
and so on.

With a hand of cards, this is like looking through all the cards for the
lowest one, and putting it first. Then you look through the rest for the
next lowest, and so on.

### Your turn

Here is the pseudocode for `selection_sort(items)`, the third of our
three sorts:

```
FOR each index i from 0 to length-2:
    SET min_index = i
    FOR each index j from i+1 to length-1:
        IF items[j] < items[min_index]:
            SET min_index = j
    SWAP items[i] and items[min_index]
RETURN items
```

1. In the first cell, write `selection_sort(items)`.
2. In the second cell, test it.

```python exec
id: your-turn-5
# Your selection_sort function
```

```python exec
id: your-turn-6
# Test it
```

## Comparing Our Sorts

All three algorithms give the same result, a sorted list. But they get
there in different ways. So which one does less work?

A good measure is the number of comparisons each one makes. The next
cell adds a counter to bubble sort. It runs the sort on lists of 10, 50,
100 and 200 items, each in reverse order, which is the worst case. What
do you think happens to the count when the size doubles?

```python exec
id: comparing-our-sorts-1
def bubble_sort_counted(items):
    items = items.copy()
    comparisons = 0
    n = len(items)
    for pass_num in range(n - 1):
        for i in range(n - 1 - pass_num):
            comparisons = comparisons + 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return items, comparisons

# Test with different sized lists
for size in [10, 50, 100, 200]:
    test_data = list(range(size, 0, -1))   # worst case: reverse sorted
    sorted_data, comparison_count = bubble_sort_counted(test_data)
    print("Size " + str(size) + ": " + str(comparison_count) + " comparisons")
```

Do you see a pattern? When the size doubles, the number of comparisons
goes up about four times. In the worst case, each of our three
algorithms makes about $\frac{n(n-1)}{2}$ comparisons. That number grows
in proportion to $n^2$, and we write this as $O(n^2)$.

| Items | Comparisons, about | Time |
|---|---|---|
| 10 | 45 | instant |
| 1,000 | 500,000 | still fast |
| 1,000,000 | 500,000,000,000 | a long wait |

Faster algorithms exist. Merge sort reaches $O(n \log n)$, and quicksort
usually does too. Even so, the three sorts on this page are the best
ones to build first. Each one is short enough to hold in your head all
at once. That lets you see the cost of an algorithm for yourself, and
not only be told about it.

### Your turn

1. Add comparison counting to your insertion sort and your selection
   sort, too.
2. Run all three sorts over the same data. Try three kinds of data:
   random order, already sorted, and reverse order.

Do the three sorts always make the same number of comparisons? Or does
it depend on the data they get? Which one do you think does best on data
that is already in order? Can you say why, before you run it?

```python exec
id: your-turn-7
# Your comparison experiments
```

## Optional Challenges

If you have time, here are two more things to explore.

**Shell sort** is a clever improvement on insertion sort. Insertion sort
compares elements that sit next to each other. Shell sort compares
elements a fixed distance apart. This distance is called the *gap*.
Shell sort makes the gap smaller, step by step. When the gap reaches 1,
shell sort has become an ordinary insertion sort. But by then the list
is nearly in order, and insertion sort is at its fastest on a list that
is nearly in order. It is a satisfying one to build.

**Recursive binary search.** In [Searching a list: linear and binary search](tutorial:finding-things)
we wrote binary search with a `while` loop. Can you rewrite it so that
the function calls itself, each time with a smaller range? A function
that calls itself is using *recursion*. Recursion is a neat way to write
divide-and-conquer algorithms. Here is one way to write it:

```
def binary_search_recursive(items, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if items[mid] == target:
        return mid
    elif target < items[mid]:
        return binary_search_recursive(items, target, low, mid - 1)
    else:
        return binary_search_recursive(items, target, mid + 1, high)
```

```python exec
id: optional-challenges-1
# Optional: shell sort implementation
```

```python exec
id: optional-challenges-2
# Optional: try the recursive binary search and compare it to your iterative version
```

## Reflection

We have now built three sorting algorithms from nothing. We also know how
to compare how fast they are, by counting the steps they take. Together
with the search algorithms from [Searching a list: linear and binary search](tutorial:finding-things),
we now have a good set of tools for putting data in order and finding
things in it.

We also went through the full cycle of building an algorithm:

1. Understand the problem.
2. Write pseudocode.
3. Write the code.
4. Test it.
5. Measure how much work it does.

This cycle is the same whether the problem is sorting numbers or
building a machine learning system.

You are now ready to build these tools again, from nothing but the
ideas. That is the only real way to find out whether the algorithms, and
the programming behind them, have stuck.

What was the most satisfying moment in these last two tutorials? What
would you like to understand better?

## Where to Read More

Timo Bingmann (2013). *15 Sorting Algorithms in 6 Minutes.*
<https://www.youtube.com/watch?v=kPRA0W1kECg>. Sorting made audible and visible
at once. The difference between the $n^2$ sorts and the $n \log n$ ones is
obvious here in a way no table of numbers manages.

Sebastian Lague (2016). *Coding Adventure: Sorting Algorithms.*
<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. Built from nothing, at a pace
that assumes you are following along rather than watching.

Computerphile (2016). *Getting Sorted & Big O Notation.*
<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. Why the growth rate matters more
than the constant factor, which is the whole argument of the comparison section.

Cormen, T. H., Leiserson, C. E., Rivest, R. L. and Stein, C. (2022).
*Introduction to Algorithms* (4th ed.). MIT Press. Chapter 2 covers insertion
sort and the analysis properly. Heavier than this course needs, and the standard
reference if you go further.

Python Software Foundation. *Sorting Techniques.*
<https://docs.python.org/3/howto/sorting.html>. How `sorted` and `key` actually
work, including why Python's sort is stable and when that matters.
