---
title: "Finding Things"
slug: finding-things
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
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

**Programming Design Principles / Maths for IT**

We can now store collections of data in lists and write functions to work with them. A natural next question: given a collection, how do we find a specific item in it? This is the *search problem*, and it turns out there are very different approaches depending on what we know about the data.

We will also deepen our understanding of functions today, looking at how they communicate with each other and how to think about what a function *is* from a mathematical perspective.

## Functions as Input-Output Machines

In mathematics, a function is a rule that assigns *exactly one output* to each input. $f(x) = x^2$ takes 3 and gives 9, takes -3 and also gives 9. The key property: the same input always gives the same output.

Our Python functions work the same way. When we write:

```python
def square(n):
    return n ** 2
```

we are defining a rule that maps each input to exactly one output. This is a genuine mathematical function implemented in code.

Not every Python function is a mathematical function (some depend on external state, or use randomness), but the ones that are -- where the output depends only on the inputs -- are the easiest to understand, test, and trust. We call these *pure functions*, and they are worth striving for.

## Scope: Where Variables Live

When we define a variable inside a function, it only exists while that function is running. This is called *local scope*:

```python exec
id: scope-where-variables-live-1
def calculate_area(radius):
    pi = 3.14159
    area = pi * radius ** 2
    return area

result = calculate_area(5)
print(result)

# This would cause an error if uncommented:
# print(area)    # 'area' does not exist outside the function
```

This is actually a feature, not a limitation. It means functions are self-contained -- you do not need to worry about a variable inside one function accidentally interfering with a variable in another. Each function has its own workspace.

Variables defined outside any function have *global scope* -- they can be read from anywhere. But it is good practice to pass values into functions as parameters rather than relying on global variables. This makes your functions portable and testable.

### Your turn

Let's write a function `circle_info(radius)` that returns *both* the area and circumference of a circle. Python lets you return multiple values by separating them with a comma:

```python
def example():
    return 10, 20

a, b = example()   # a gets 10, b gets 20
```

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

Given a list and a target value, linear search checks each element one by one until it finds the target or runs out of list. It is the approach you would use to find a friend's name in an unsorted guest list.

### Your turn

Let's write a function `linear_search(items, target)` that returns the index where the target was found, or -1 if the target is not in the list.

**Pseudocode:**
```
FOR each index i in the list:
    IF items[i] equals the target:
        RETURN i
RETURN -1 (target not found)
```

Translate this to Python:

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

If the list has 10 items, we might need up to 10 comparisons. If it has 1,000,000 items, we might need up to 1,000,000 comparisons. The worst case grows directly with the size of the list. Computer scientists describe this as O(n) -- "order n" -- meaning the time grows proportionally to the input size.

For a small list, this is fine. For a large one, it can be painfully slow. Can we do better?

## Binary Search: The Power of Sorted Data

Imagine looking up a word in a dictionary. You would not start at page one and read every entry. You would open it roughly in the middle, see if your word comes before or after that point, and immediately eliminate half the dictionary. Then you would repeat with the remaining half.

This is *binary search*, and it only works when the data is *sorted*. But when the data is sorted, it is spectacularly fast.

The idea: maintain a search range defined by `low` and `high` indices. Look at the middle element. If it matches the target, we are done. If the target is smaller, search the left half (set `high = mid - 1`). If larger, search the right half (set `low = mid + 1`). Repeat until found or the range is empty.

### Your turn

**Pseudocode** (fill in the details):
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

Now implement it:

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

Each step halves the search space. Starting with 1,000,000 items:
- After 1 step: 500,000 remaining
- After 2 steps: 250,000
- After 10 steps: ~1,000
- After 20 steps: ~1

So binary search on a million items needs at most about 20 comparisons. Linear search might need a million. That is the difference between $O(\log n)$ and $O(n)$.

The catch: the data must be sorted first. Sorting takes time, so binary search only wins when we search the same data many times (which is actually very common).

## Divide and Conquer

Binary search is our first example of *divide and conquer*: split the problem into smaller pieces, solve the smaller pieces, and combine. This is one of the most powerful ideas in algorithm design.

The pattern appears everywhere:
- Looking up a contact on your phone (the list is sorted alphabetically)
- Finding a page in a book (pages are numbered in order)
- A doctor diagnosing an illness (running tests that rule out half the possibilities)

### Your turn

Here is a small puzzle. I am thinking of a number between 1 and 100. You can ask questions of the form "is it greater than X?" and I will answer truthfully. What is the maximum number of questions you need to guarantee finding the number?

What's your reasoning?

## Putting It Together

Let's write a small program that demonstrates the difference between linear and binary search. We will search for the same target in the same list using both methods, and count how many comparisons each one makes.

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

index_lin, comps_lin = linear_search_counted(data, target)
index_bin, comps_bin = binary_search_counted(data, target)

print("List size:", len(data))
print("Linear search: found at index " + str(index_lin) + ", " + str(comps_lin) + " comparisons")
print("Binary search: found at index " + str(index_bin) + ", " + str(comps_bin) + " comparisons")
```

### Your turn

Try different targets and list sizes. What happens when the target is the very first element? The very last? Not in the list at all? Which search method handles each case better?

```python exec
id: your-turn-7
# Your experiments here
```

## Reflection

Today we explored functions more deeply (scope, return values, pure functions as mathematical functions), and we implemented two fundamental search algorithms. The key takeaway is that *how we organise data affects how efficiently we can work with it*. Sorted data enables binary search, which is dramatically faster than linear search for large collections.

Next time, we will tackle the other side of this coin: how do we sort data in the first place?

What surprised you most about the difference between linear and binary search?

## Where to Read More

Mike Pound (Computerphile) (2023). *Binary Search Algorithm.*
<https://www.youtube.com/watch?v=hDn8iOc30Tk>. The same halve-and-repeat
idea this page builds, explained with a different worked example.

Computerphile (2013). *Getting Sorted & Big O Notation.*
<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. Where the $O(\log n)$ and
$O(n)$ this page mentions come from, and how the same notation applies to
sorting as well as searching.
