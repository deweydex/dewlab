---
title: "Putting Things in Order"
slug: putting-things-in-order
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.2
covers:
  bubble-sort-let-things-rise:
    covers: [MIT-6.8]
  insertion-sort-sort-like-you-sort-cards:
    covers: [MIT-6.8]
  selection-sort-find-the-smallest:
    covers: [MIT-6.8]
  comparing-our-sorts:
    covers: [MIT-6.8]
  optional-challenges:
    touches: [MIT-6.8]
---

# Putting Things in Order

**Programming Design Principles / Maths for IT**

Binary search is wonderful, but it needs sorted data. So how do we sort? This turns out to be one of the most studied problems in computer science -- not because sorting is hard to do, but because there are so many different ways to do it, and the differences in efficiency become dramatic as the data grows.

Today we implement three classic sorting algorithms. Each one reflects a different way of thinking about the problem, and each teaches us something about algorithm design.

## The Swap: A Small but Essential Tool

Before we sort anything, we need to know how to swap two elements in a list. In Python, this is elegant:

```python exec
id: the-swap-a-small-but-essential-tool-1
numbers = [10, 20, 30, 40, 50]
print("Before:", numbers)

# Swap elements at index 1 and index 3
numbers[1], numbers[3] = numbers[3], numbers[1]
print("After: ", numbers)
```

The line `a, b = b, a` works because Python evaluates the right side completely before assigning to the left side. In many other languages you would need a temporary variable:

```
temp = a
a = b
b = temp
```

Both approaches work. The Python one says the same thing in fewer moving parts.

## Bubble Sort: Let Things Rise

The idea behind bubble sort is simple: walk through the list comparing adjacent pairs. If they are in the wrong order, swap them. After one complete pass, the largest element will have "bubbled up" to the end. Repeat until the list is sorted.

Let's watch it happen step by step:

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
print("Notice: the largest element (90) is now at the end.")
```

One pass is not enough to fully sort the list. But after each pass, one more element is in its final position. So we need at most n-1 passes for a list of n elements.

### Your turn

Let's try `bubble_sort(items)`, returning the list in ascending order.

**Pseudocode:**
```
FOR each pass from 0 to length-2:
    FOR each index i from 0 to length-2-pass:
        IF items[i] > items[i+1]:
            SWAP them
RETURN items
```

Why can the inner loop stop earlier on each pass? The largest unsorted element reaches its final position at the end of every pass, so there is one fewer place worth looking each time.

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

Insertion sort works the way most people sort a hand of playing cards: pick up cards one at a time and insert each one into the correct position among the cards you have already sorted.

The algorithm maintains a sorted portion at the beginning of the list. It takes the next unsorted element and walks it backwards through the sorted portion until it finds the right spot.

### Your turn

How might `insertion_sort(items)` look?

**Pseudocode:**
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

The `key` variable holds the element we are currently inserting. We shift larger elements to the right until we find where the key belongs.

```python exec
id: your-turn-3
# Your insertion_sort function
```

```python exec
id: your-turn-4
# Test it with the same cases as bubble sort
```

## Selection Sort: Find the Smallest

Selection sort takes a different approach: find the smallest element in the unsorted portion and swap it into the next position of the sorted portion. Then find the next smallest, and so on.

It is like sorting a hand of cards by scanning for the lowest card, putting it first, then scanning the remaining cards for the next lowest, and so on.

### Your turn

And `selection_sort(items)` — the third of the three.

**Pseudocode:**
```
FOR each index i from 0 to length-2:
    SET min_index = i
    FOR each index j from i+1 to length-1:
        IF items[j] < items[min_index]:
            SET min_index = j
    SWAP items[i] and items[min_index]
RETURN items
```

```python exec
id: your-turn-5
# Your selection_sort function
```

```python exec
id: your-turn-6
# Test it
```

## Comparing Our Sorts

All three algorithms produce the same result -- a sorted list -- but they get there differently. Let's think about efficiency.

For each algorithm, the key question is: how many comparisons does it make? Let's add counting to find out:

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
    sorted_data, comps = bubble_sort_counted(test_data)
    print("Size " + str(size) + ": " + str(comps) + " comparisons")
```

Notice a pattern? When the size doubles, the number of comparisons roughly quadruples. This is because each of our three algorithms makes approximately $\frac{n(n-1)}{2}$ comparisons in the worst case, which grows proportionally to $n^2$.

For 10 items, that is about 45 comparisons -- instant. For 1,000 items, about 500,000 -- still fast. For 1,000,000 items, about 500,000,000,000 -- that is going to take a while.

Faster algorithms exist — merge sort and quicksort reach $O(n \log n)$ — and the three built today are still the ones worth building first. They are short enough to hold in your head at once, which is what makes the cost of an algorithm visible rather than asserted.

### Your turn

What happens if you add comparison counting to the insertion and selection sorts as well, and run all three over the same data? Do they always make the same number of comparisons, or does it depend on what they are given?

Random order, already sorted, and reverse sorted are the three cases worth trying. Which algorithm does best on data that is already in order, and can you say why before you run it?

```python exec
id: your-turn-7
# Your comparison experiments
```

## Optional Challenges

If you have time, here are two extensions worth exploring.

**Shell sort** is a clever improvement on insertion sort. Instead of comparing adjacent elements, it compares elements a fixed distance apart — the *gap* — and then reduces the gap gradually. When the gap reaches 1 it has become an ordinary insertion sort, but by then the list is nearly in order and insertion sort's best case takes over. It is a satisfying one to build.

**Recursive binary search**: In *Finding Things* we wrote binary search with a while loop. Can you rewrite it so the function calls itself with a smaller range instead? This is called *recursion*, and it is an elegant way to express divide-and-conquer algorithms.

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

We have now built three sorting algorithms from scratch, and we understand how to compare their efficiency by counting operations. Combined with the search algorithms from *Finding Things*, we have a solid toolkit for organising and finding data.

More importantly, we have practised the full cycle of algorithm development: understand the problem, write pseudocode, implement, test, and analyse. This cycle is the same whether the problem is sorting numbers or building a machine learning system.

You are now ready to build these tools fresh, from nothing but the ideas -- which is the only real way to find out whether the algorithms and the programming behind them have landed.

What was the most satisfying moment in these last two tutorials? What would you like to understand better?

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
