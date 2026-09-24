---
title: "Sets: building them from sorted lists"
year: "2026-2027"
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

# Sets: building them from sorted lists

A *set* is a collection of different elements, where the order does not
matter and no element appears twice. In maths we write a set inside curly
brackets. So $\{3, 1, 4, 1, 5\}$ is the same set as $\{1, 3, 4, 5\}$. The
second 1 is a repeat, so it does not count, and the order of the elements
makes no difference.

Sets give us a language for three kinds of question:

- **membership**: is 7 in this set?
- **relationships**: what do these two sets have in common?
- **operations**: what do we get when we combine these two sets?

On this page we build all of this ourselves, using sorted lists to hold
the sets. Two earlier pages help us.
[Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order)
gives us sorted data, and the binary search from
[Searching a list: linear and binary search](tutorial:finding-things)
lets us find an element quickly.

On this page we:

- turn any list into a set, stored as a sorted list
- check whether an element is in a set
- combine two sets in four different ways, with one pattern
- learn the symbols mathematicians use for sets
- look at where sets are used in real programs

## Why sorted lists?

Python has its own `set` type. On this page we build our own sets
instead, as sorted lists with no repeats. There are two reasons.

First, it lets us practise algorithms we already know. Finding an
element in a sorted list is a binary search. Combining two sorted lists
uses a pattern called a merge, which we meet below. These patterns come
up again and again in programming.

Second, it shows that Python's `set` is not magic. Once you have built
the set operations yourself, you know what they do. Python's `set` gives
the same results. Inside, it uses a different and faster method, called
hashing, but the operations are the same ones we build here.

## Making a set

The first job is to take a list that might have repeats and might not be
sorted. From it, we make a sorted list with no repeats.

One way is to sort the list first. In a sorted list, any repeats sit
next to each other. So then we walk along the list and leave out each
item that is the same as the one before it.

### Your turn

Can you write a function `make_set(items)` that returns a sorted list
with no repeats? Here is the idea in pseudocode:

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

Then test it. The comments in the next cell say what each call should
give.

```python exec
id: your-turn-2
# Test cases
# make_set([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]) should give [1, 2, 3, 4, 5, 6, 9]
# make_set([1, 1, 1]) should give [1]
# make_set([]) should give []
# make_set([5, 3, 1]) should give [1, 3, 5]
```

## Membership testing

Is a particular element in the set? Our sets are sorted, so we can use
binary search to find out. Our binary search gives back the item's
position, or -1 when the item is missing. For a set, we want a plain yes or no:
`True` or `False`.

### Your turn

How might you write a function `is_member(s, item)`? It should return
`True` if `item` is in the set `s`, and `False` if it is not. The set is
sorted, so use the binary search method.

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

## Set operations: the merge pattern

There are three main ways to combine two sets:

- The *union* of two sets holds every element that is in either set, or
  in both.
- The *intersection* holds only the elements that are in both sets.
- The *difference* of a and b holds the elements that are in a but are
  not in b.

We can build all three with one pattern. It is the same pattern that
merge sort uses. We mentioned merge sort on the sorting page: it is a
faster sort that works by combining two sorted lists into one, again
and again. That combining step is called a *merge*.

Both of our sets are sorted. So we walk through the two of them at the
same time, with two pointers. A *pointer* here is an index variable, `i`
for set a and `j` for set b, that marks our place in each list. At each
step we compare the two current elements:

- If they are equal, the element goes in the union and in the
  intersection. Move both pointers on.
- If one is smaller, that element goes in the union, but not in the
  intersection. Move its pointer on.
- When one list runs out, the elements left in the other list go in the
  union.

We call this the *merge walk*. The picture shows it step by step.

![Five steps walking two sorted lists. Each step shows where both pointers
sit, the comparison that makes, and which pointer moves as a result. Then
what is left over in b, and the union they build.](merge-walk.svg)

The three rules above are the only three things that can happen at one
comparison. Each step is the same: look at where the two pointers are,
keep something, then move one pointer or both. Neither pointer ever goes
backwards.

How much work is that? Say set a has $n$ elements and set b has $m$.
Each step moves at least one pointer forward, so there are at most
$n + m$ steps. For two sets of 1,000 elements, that is at most 2,000
steps. Checking every element of a against every element of b would
take $n \times m$ steps, which is 1,000,000. So the merge walk is an
$O(n + m)$ algorithm.

Here is the merge walk written out for union. What do you expect it to
print for these two sets? Run it to check.

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

The *symmetric difference* of a and b holds the elements that are in a
or in b, but not in both.

1. Write `intersection(a, b)`: the elements that are in *both* a and b.
2. Write `difference(a, b)`: the elements that are in a but *not* in b.
3. Write `symmetric_difference(a, b)`: the elements that are in a or b,
   but *not* in both.
4. Run the test cell to check all of them.

Use `union()` as your guide. What changes in the merge walk for each
operation? Which elements do we keep when `a[i] == b[j]`? Which do we
keep when `a[i] < b[j]`?

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

The four operations are connected to each other. We can use these
connections to test our functions. For any sets a and b:

- `symmetric_difference(a, b)` should equal `difference(union(a, b), intersection(a, b))`
- `union(a, b)` should equal `union(intersection(a, b), symmetric_difference(a, b))`
- `len(union(a, b))` should equal `len(a) + len(b) - len(intersection(a, b))`

Look at the last one. In words, it says: to count the elements in the
union, add the sizes of the two sets, then take away the elements they
share, because we counted those twice. In maths we write the size of a
set $A$ as $|A|$, so the rule is:

$$|A \cup B| = |A| + |B| - |A \cap B|$$

For example, take $A = \{1, 3, 4, 5\}$ and $B = \{1, 2, 5, 7, 8\}$. They
share 1 and 5, so the union has $4 + 5 - 2 = 7$ elements:
$\{1, 2, 3, 4, 5, 7, 8\}$.

This is the *inclusion-exclusion principle*. Does it look familiar? It
is the same idea as the general addition rule from
[Probability: simple, compound and conditional](tutorial:what-are-the-chances),
where we took away $P(A \text{ and } B)$ so that we did not count the
overlap twice.

The next cell checks the first and the last connection, on the sets a
and b from your test cell.

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

## Set language and notation

Mathematicians use a few special symbols for sets. The examples use
$A = \{1, 2, 3\}$ and $B = \{2, 3, 4\}$.

| Symbol | Read it as | Example |
|---|---|---|
| $\in$ | "is a member of" | $3 \in A$ |
| $\notin$ | "is not a member of" | $4 \notin A$ |
| $\cup$ | union | $A \cup B = \{1, 2, 3, 4\}$ |
| $\cap$ | intersection | $A \cap B = \{2, 3\}$ |
| $\setminus$ | difference | $A \setminus B = \{1\}$ |
| $\subseteq$ | "is a subset of" | $\{1, 3\} \subseteq A$ |
| $\emptyset$ | the empty set, $\{\}$ | $A \cap \{7, 8\} = \emptyset$ |

A set A is a *subset* of a set B when every element of A is also in B.
Every set is a subset of itself. Some books write $\subset$ for "is a
subset of". Other books keep $\subset$ for a subset that is smaller than
the whole set, so check which one your book means.

The *empty set* is the set with no elements at all. We write it
$\emptyset$ or $\{\}$.

### Your turn

1. Write `is_subset(a, b)`. It returns `True` if every element of a is
   also in b.
2. Write `is_equal(a, b)`. It returns `True` if the two sets contain
   exactly the same elements.
3. Run the test cell.

Then think about two questions. How does `is_subset` relate to
`intersection`? How does `is_equal` relate to `is_subset`?

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

## Sets in practice

Sets are more than abstract mathematics. Here are three places where
programs use them:

- **A search engine.** To find pages that match "python AND sorting",
  it takes the intersection of two sets: the pages that contain
  "python", and the pages that contain "sorting".
- **A social media app.** To suggest new friends, it might take the
  union of your friends' friend lists, then take away the people you
  already know.
- **A spell checker.** It checks whether each word is a member of the
  set of known words.

### Your turn

Can you think of one more practical use of sets?

1. Describe it in a sentence or two, as a comment.
2. Build a small example of it with your set functions.

```python exec
id: your-turn-11
# Your practical set example
```

## Reflection

We have built a complete set library ourselves. It can make a set, test
membership, and find the union, intersection, difference and symmetric
difference of two sets. It can also test for a subset and for equal
sets. Every one of these rests on sorted lists and the merge walk.

Each part connects to earlier work. Sorting prepares the data, binary
search makes membership fast, and the merge step from merge sort drives
all the set operations.

Next, [Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth)
looks at true and false statements, which follow rules much like these
set operations. After that,
[Venn diagrams: drawing sets and their overlaps](tutorial:venn-diagrams)
draws sets as pictures.

Which connection between sets and earlier material did you find most
satisfying?

## Where to Read More

Khan Academy. *Intersection and Union of Sets.*
<https://www.youtube.com/watch?v=jAfNg3ylZAI>. The same two operations
this page builds with a merge-walk, introduced from the mathematics side.

Python Software Foundation. *The Python Tutorial — Sets.*
<https://docs.python.org/3/tutorial/datastructures.html#sets>. The
built-in `set` this page deliberately avoids, for comparison once you have
built your own.
