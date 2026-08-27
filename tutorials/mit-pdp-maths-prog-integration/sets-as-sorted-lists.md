---
title: "Sets as Sorted Lists"
slug: sets-as-sorted-lists
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
covers:
  making-a-set:
    covers: [MIT-2.1]
  membership-testing:
    covers: [MIT-2.1]
  set-operations-the-merge-pattern:
    covers: [MIT-2.2]
  set-language-and-notation:
    covers: [MIT-2.1]
  sets-in-practice:
    covers: [MIT-2.2]
---

# Sets as Sorted Lists

**Programming Design Principles / Maths for IT**

A *set* is a collection of distinct elements where order does not matter and duplicates are not allowed. The set {3, 1, 4, 1, 5} is the same as {1, 3, 4, 5} -- the duplicate is removed and the order is irrelevant.

Sets give us a language for talking about membership ("is 7 in this set?"), relationships ("what do these two sets have in common?"), and operations ("combine these two sets"). Today we build all of this from scratch, using sorted lists as our underlying data structure.

This connects beautifully to our earlier work: the sort algorithms from *Putting Things in Order* prepare the data, and the binary search from *Finding Things* makes membership testing efficient.

## Why Sorted Lists?

Python has a built-in `set` type, but we are going to implement sets as sorted lists with no duplicates. There are two reasons for this.

First, it lets us practise the algorithms we have already learned. Finding an element in a sorted list is a binary search. Combining two sorted lists is a merge operation. These are fundamental patterns.

Second, it demystifies what the built-in `set` does. When you understand how set operations work at the algorithmic level, the built-in version is not magic -- it is just a faster implementation of the same ideas.

## Making a Set

The first operation: take a list that might contain duplicates and might not be sorted, and produce a clean sorted list with no duplicates.

One approach: sort the list, then walk through it removing consecutive duplicates.

### Your turn

Let's write a function `make_set(items)` that returns a sorted list with no duplicates.

**Pseudocode:**
```
SORT the items
CREATE empty result list
FOR each item in sorted items:
    IF result is empty OR item is different from the last element in result:
        APPEND item to result
RETURN result
```

```python exec
id: your-turn-1
# Your make_set function
```

```python exec
id: your-turn-2
# Test cases
# make_set([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]) should give [1, 2, 3, 4, 5, 6, 9]
# make_set([1, 1, 1]) should give [1]
# make_set([]) should give []
# make_set([5, 3, 1]) should give [1, 3, 5]
```

## Membership Testing

Is a particular element in the set? Since our sets are sorted, we can use binary search. But let's write a clean wrapper that returns True or False rather than an index:

### Your turn

How might you write a function `is_member(s, item)` that returns True if item is in the set s, False otherwise? Use the binary search approach since the set is sorted.

```python exec
id: your-turn-3
# Your is_member function
```

```python exec
id: your-turn-4
# Test it
s = make_set([3, 1, 4, 1, 5, 9, 2, 6])
print(is_member(s, 5))    # True
print(is_member(s, 7))    # False
print(is_member(s, 1))    # True
```

## Set Operations: The Merge Pattern

The core set operations -- union, intersection, and difference -- can all be implemented using a pattern similar to the merge step in merge sort. Since both input sets are sorted, we walk through them simultaneously with two pointers:

- If the current elements are equal, they go in both union and intersection. Advance both pointers.
- If one is smaller, it goes in the union (but not intersection). Advance that pointer.
- When one list runs out, any remaining elements from the other go in the union.

This is an efficient $O(n + m)$ algorithm, where $n$ and $m$ are the sizes of the two sets.

```python exec
id: set-operations-the-merge-pattern-1
# The merge-walk pattern, demonstrated for union
def union(a, b):
    """Return a sorted list of all elements that are in a or b (or both)."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            result.append(a[i])
            i = i + 1
        else:
            result.append(b[j])
            j = j + 1
    # Append any remaining elements
    while i < len(a):
        result.append(a[i])
        i = i + 1
    while j < len(b):
        result.append(b[j])
        j = j + 1
    return result

# Test
a = make_set([3, 1, 4, 1, 5])
b = make_set([5, 7, 2, 8, 1])
print("a:", a)
print("b:", b)
print("union:", union(a, b))
```

### Your turn

Using the same merge-walk pattern as a guide, how might you write the remaining set operations?

1. `intersection(a, b)` -- elements that are in *both* a and b
2. `difference(a, b)` -- elements that are in a but *not* in b
3. `symmetric_difference(a, b)` -- elements that are in a or b but *not* both

What changes in the merge-walk logic for each operation? Which elements do we keep when `a[i] == b[j]`? When `a[i] < b[j]`?

```python exec
id: your-turn-5
# Your intersection function
```

```python exec
id: your-turn-6
# Your difference function
```

```python exec
id: your-turn-7
# Your symmetric_difference function
```

```python exec
id: your-turn-8
# Test all operations
a = make_set([3, 1, 4, 1, 5, 9, 2, 6])
b = make_set([5, 7, 2, 8, 1, 8])
print("a:", a)
print("b:", b)
print("union:", union(a, b))
print("intersection:", intersection(a, b))
print("difference (a-b):", difference(a, b))
print("difference (b-a):", difference(b, a))
print("symmetric_difference:", symmetric_difference(a, b))
```

### Verification

There is a beautiful relationship between these operations that we can use for testing. For any sets a and b:

- `symmetric_difference(a, b)` should equal `difference(union(a, b), intersection(a, b))`
- `union(a, b)` should equal `union(intersection(a, b), symmetric_difference(a, b))`
- `len(union(a, b))` should equal `len(a) + len(b) - len(intersection(a, b))`

The last one is the set version of the inclusion-exclusion principle we saw in probability!

```python exec
id: verification-1
# Verify the relationships
print("sym_diff:", symmetric_difference(a, b))
print("union - intersection:", difference(union(a, b), intersection(a, b)))
print("Match:", symmetric_difference(a, b) == difference(union(a, b), intersection(a, b)))

print()
print("|a| + |b| - |a & b| =", len(a) + len(b) - len(intersection(a, b)))
print("|a | b| =", len(union(a, b)))
print("Match:", len(a) + len(b) - len(intersection(a, b)) == len(union(a, b)))
```

## Set Language and Notation

Mathematicians use specific notation and terminology for sets:

- $\in$ means "is a member of": $3 \in \{1, 2, 3\}$
- $\notin$ means "is not a member of": $4 \notin \{1, 2, 3\}$
- $\cup$ means union: $A \cup B$
- $\cap$ means intersection: $A \cap B$
- $\setminus$ means difference: $A \setminus B$
- $\subset$ means "is a subset of": every element of A is also in B
- $\emptyset$ means the empty set: $\{\}$

### Your turn

Let's write two more functions:

1. `is_subset(a, b)` -- returns True if every element of a is also in b
2. `is_equal(a, b)` -- returns True if the two sets contain exactly the same elements

How does `is_subset` relate to `intersection`? And how does `is_equal` relate to `is_subset`?

```python exec
id: your-turn-9
# Your is_subset and is_equal functions
```

```python exec
id: your-turn-10
# Test them
print(is_subset([1, 3], [1, 2, 3, 4]))    # True
print(is_subset([1, 5], [1, 2, 3, 4]))    # False
print(is_equal([1, 2, 3], [3, 1, 2]))     # True (after make_set)
```

## Sets in Practice

Sets are not just abstract mathematics. Here are a few practical applications:

A search engine finding pages that match "python AND sorting": it computes the intersection of the set of pages containing "python" and the set containing "sorting."

A social media app suggesting friends: it might look at the union of your friends' friend lists, minus people you already know.

A spell checker: it checks whether each word is a member of the set of known words.

### Your turn

What's one more practical application of sets you can think of? Describe it briefly, then implement a small example using your set functions.

```python exec
id: your-turn-11
# Your practical set example
```

## Reflection

We have implemented a complete set library from scratch: construction, membership testing, union, intersection, difference, symmetric difference, subset testing, and equality. Every operation is built on the foundation of sorted lists and the merge-walk pattern.

The connection to earlier work is satisfying: our sorting algorithms prepare the data, our binary search makes membership efficient, and the merge pattern from sorting theory drives all the set operations. Everything builds on everything else.

You are now ready to combine polynomial algebra, equation solving, and set operations into a single coherent toolkit of your own.

What was the most elegant connection you noticed between sets and earlier material?

## Where to Read More

Khan Academy. *Intersection and Union of Sets.*
<https://www.youtube.com/watch?v=jAfNg3ylZAI>. The same two operations
this page builds with a merge-walk, introduced from the mathematics side.

Python Software Foundation. *The Python Tutorial — Sets.*
<https://docs.python.org/3/tutorial/datastructures.html#sets>. The
built-in `set` this page deliberately avoids, for comparison once you have
built your own.
