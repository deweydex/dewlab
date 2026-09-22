---
title: "Finding Things"
year: "2026-2027"
version: 2026.09.22.1
covers:
  functions-as-input-output-machines:
    covers: [MIT-6.2]
    touches: [MIT-3.1]
  scope-where-variables-live:
    covers: [PDP-LO8]
  linear-search-the-straightforward-approach:
    covers: [MIT-6.8, CMPS-LO5]
  binary-search-the-power-of-sorted-data:
    covers: [MIT-6.8, CMPS-LO5]
  divide-and-conquer:
    covers: [MIT-6.6]
  putting-it-together:
    covers: [CMPS-LO5]
---

# Finding Things

We can now keep data in lists, and write functions that work with them.
So here is the next question. We have a list, and we want one item in
it. How do we find it?

This is the *search problem*: the task of finding one item in a
collection. There are very different ways to solve it. Which way works
best depends on what we know about the data.

On this page we:

- look at what a function is, in mathematics and in Python
- see where a variable lives, inside or outside a function
- write two ways to search a list, and count how much work each one does

## Functions as Input-Output Machines

In mathematics, a function is a rule that gives *exactly one output* for
each input. For example, $f(x) = x^2$ takes 3 and gives 9. It takes -3
and also gives 9. The important property is this: the same input always
gives the same output.

Our Python functions can work the same way. Here is one:

```python
def square(n):
    return n ** 2
```

This code defines a rule that gives exactly one output for each input.
It is a mathematical function, written in code.

Not every Python function is a mathematical function. Some depend on
things outside the function. Others use random numbers. A *pure
function* is a function whose output depends only on its inputs. Pure
functions are the easiest to understand, to test and to trust, so they
are worth aiming for.

## Scope: Where Variables Live

A variable's *scope* is the part of the program where that variable
exists. A variable we create inside a function has *local scope*: it
exists only while that function is running.

Look at the last line of the next cell. It is a comment, so it does not
run. What do you think would happen if it did run?

```python exec
id: scope-where-variables-live-1
def calculate_area(radius):
    pi = 3.14159
    area = pi * radius ** 2
    return area

result = calculate_area(5)
print(result)

# What happens if this line runs? Delete the # at its start to find out.
# print(area)
```

Try it: delete the `#` at the start of the last line, and run the cell
again. Python stops with a `NameError`. The name `area` does not exist
outside the function.

Local scope helps us. Each function has its own workspace. A variable
inside one function cannot get mixed up with a variable in another
function, even when the two have the same name.

A variable we create outside any function has *global scope*: we can
read it from anywhere in the program. Even so, it is better to pass
values into a function as parameters than to rely on global variables.
Then the function does not depend on anything outside it, so we can
move it to another program and test it on its own.

### Your turn

Python lets a function return more than one value. We put a comma
between the values:

```python
def example():
    return 10, 20

a, b = example()   # a gets 10, b gets 20
```

1. In the first cell, write a function `circle_info(radius)` that
   returns *both* the area and the circumference of a circle. The cell
   starts with `import math`, so you can use `math.pi`.
2. In the second cell, test it with a radius you can check by hand.

```python exec
id: your-turn-1
# Your circle_info function
import math    # gives us math.pi for a more accurate value
```

```python exec
id: your-turn-2
# Test it
```

## Linear Search: The Straightforward Approach

*Linear search* is a way of searching that checks each element in turn,
from the start of the list. It stops when it finds the target, or when
it reaches the end of the list. It is how you would look for a friend's
name on a guest list that is in no order.

### Your turn

We want a function `linear_search(items, target)`. It returns the index
where it finds the target. If the target is not in the list, it returns
-1.

Here are the steps in pseudocode:

```
FOR each index i in the list:
    IF items[i] equals the target:
        RETURN i
RETURN -1 (target not found)
```

1. In the first cell, turn this pseudocode into Python.
2. In the second cell, test it three ways: with a name that is in the
   list, a name that is not in the list, and an empty list.

```python exec
id: your-turn-3
# Your linear_search function
```

```python exec
id: your-turn-4
# Test cases
names = ["Grace", "Ada", "Alan", "Margaret", "Linus", "Barbara"]

# Search for someone who is in the list
# Search for someone who is not in the list
# Search in an empty list
```

### How efficient is linear search?

If the list has 10 items, we might need up to 10 comparisons. If it has
1,000,000 items, we might need up to 1,000,000 comparisons. In the worst
case, the work grows in step with the size of the list.

Computer scientists write this as *O(n)*, said "order n". O(n) means
that the time grows in proportion to the size of the input, n. Twice as
many items means up to twice as many comparisons.

For a small list, that is fine. For a large list, it can be very slow.
Can we do better?

## Binary Search: The Power of Sorted Data

Think about looking up a word in a paper dictionary. You would not start
at page one and read every word. You would open it near the middle. Then
you would check whether your word comes before or after that page. With
one look, you have ruled out half of the dictionary. Then you do the
same thing again with the half that is left.

This is *binary search*. Binary search is a way of searching a sorted
list by checking the middle item and throwing away the half that cannot
hold the target. It works only when the data is *sorted*, which means
that it is in order, from smallest to largest. When the data is sorted,
binary search is very fast.

Here is how it works, step by step:

1. Keep track of the part of the list that is still possible. Two
   indexes mark its ends: `low` and `high`.
2. Look at the middle element, at index `mid`.
3. If the middle element is the target, we are done.
4. If the target is smaller, search the left half. To do this, set
   `high = mid - 1`.
5. If the target is larger, search the right half. To do this, set
   `low = mid + 1`.
6. Repeat from step 2, until we find the target or nothing is left to
   search.

![Four passes over a fifteen-item sorted list, searching for 3. The live
range shrinks from fifteen cells to seven, then three, then one, with low,
mid and high marked under it each time.](range-collapsing.svg)

Count the shaded cells in each row, from top to bottom. How many are
left each time?

There are fifteen, then seven, then three, then one. This halving is the
reason binary search is fast. It is also where the mistakes happen. The
`mid - 1` and `mid + 1` are what make the range smaller each time. If
either one is wrong, the range can stop shrinking, and the loop never
ends.

### Your turn

Here is the pseudocode, with three gaps marked `???`:

```
SET low = 0
SET high = length of list - 1
WHILE low <= high:
    SET mid = (low + high) // 2
    IF items[mid] equals target:
        ???
    ELIF target < items[mid]:
        ???
    ELSE:
        ???
RETURN -1
```

1. What goes in each of the three gaps?
2. In the first cell, write a `binary_search` function from the
   pseudocode.
3. In the second cell, run the four tests listed there. Remember that
   the list must be sorted.

```python exec
id: your-turn-5
# Your binary_search function
```

```python exec
id: your-turn-6
# Test cases -- remember the list must be sorted!
sorted_numbers = [3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]

# Search for 31 (should find it)
# Search for 20 (should not find it)
# Search for 3 (first element)
# Search for 89 (last element)
```

### How efficient is binary search?

Each step cuts the part left to search in half. Say we start with
1,000,000 items:

| After | Items left to search |
|---|---|
| 1 step | 500,000 |
| 2 steps | 250,000 |
| 10 steps | about 1,000 |
| 20 steps | about 1 |

So binary search on a million items needs at most about 20 comparisons.
Linear search might need a million. That is the difference between
$O(\log n)$ and $O(n)$. *O(log n)* means that the time grows with the
number of times we can halve n before we reach 1. That number grows very
slowly as n gets bigger.

There is a cost. The data must be sorted first, and sorting takes time.
So binary search pays off when we search the same data many times. That
happens very often.

## Divide and Conquer

Binary search is our first example of *divide and conquer*. Divide and
conquer is a way to solve a problem in three steps:

1. Split the problem into smaller pieces.
2. Solve the smaller pieces.
3. Combine the answers.

It is one of the most useful ideas in the design of algorithms, and it
shows up in many places:

- Looking up a contact on your phone (the list is sorted by name).
- Finding a page in a book (the pages are numbered in order).
- A doctor finding out what illness someone has (each test rules out
  about half of the possible causes).

### Your turn

Here is a small puzzle. I am thinking of a whole number between 1 and
100. You can ask questions of the form "Is it greater than X?", and I
will always answer truthfully.

What is the largest number of questions you could need, to be sure of
finding my number? How did you work it out?

## Putting It Together

Let's write a small program that compares linear search and binary
search. It searches for the same target in the same list, both ways, and
counts the comparisons each one makes.

The list holds the numbers 0, 3, 6, 9, and so on, up to 999. The target
is 750. Before you run the cell, guess: how many comparisons will linear
search need? And binary search?

```python exec
id: putting-it-together-1
def linear_search_counted(items, target):
    comparisons = 0
    for i in range(len(items)):
        comparisons = comparisons + 1
        if items[i] == target:
            return i, comparisons
    return -1, comparisons

def binary_search_counted(sorted_items, target):
    comparisons = 0
    low = 0
    high = len(sorted_items) - 1
    while low <= high:
        comparisons = comparisons + 1
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid, comparisons
        elif target < sorted_items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons

# Let's test with a larger sorted list
data = list(range(0, 1000, 3))   # [0, 3, 6, 9, ..., 999]
target = 750

linear_index, linear_comparisons = linear_search_counted(data, target)
binary_index, binary_comparisons = binary_search_counted(data, target)

print("List size:", len(data))
print("Linear search: found at index " + str(linear_index) + ", " + str(linear_comparisons) + " comparisons")
print("Binary search: found at index " + str(binary_index) + ", " + str(binary_comparisons) + " comparisons")
```

### Your turn

Change the target and the size of the list, and run the searches again.
Try these cases:

1. The target is the very first element.
2. The target is the very last element.
3. The target is not in the list at all.

Which search does better in each case? Were you surprised by any of
them?

```python exec
id: your-turn-7
# Your experiments here
```

## Reflection

On this page we looked more closely at functions: pure functions as
mathematical functions, scope, and returning more than one value. We
also wrote two important search algorithms.

The main lesson is this: *the way we organise data changes how fast we
can work with it*. When data is sorted, we can use binary search. For a
large collection, binary search is much faster than linear search.

Next, we look at the other side of this: how do we sort data in the
first place? That is the subject of
[Putting Things in Order](tutorial:putting-things-in-order).

What surprised you most about the difference between linear search and
binary search?

## Where to Read More

Mike Pound (Computerphile) (2023). *Binary Search Algorithm.*
<https://www.youtube.com/watch?v=hDn8iOc30Tk>. The same halve-and-repeat
idea this page builds, explained with a different worked example.

Computerphile (2013). *Getting Sorted & Big O Notation.*
<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. Where the $O(\log n)$ and
$O(n)$ this page mentions come from, and how the same notation applies to
sorting as well as searching.
