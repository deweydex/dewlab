---
title: "Sets as Sorted Lists — Practice"
slug: sets-as-sorted-lists-practice
practice_for: sets-as-sorted-lists
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Sets as Sorted Lists — Practice

Answers are folded. Half of these are set arithmetic to do on paper and half are the merge-walk to implement — do the paper ones first, because the code is much easier to write once you know what it should produce.

## Set Arithmetic

```python exec
id: set-arithmetic-1
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7}

print("union       ", sorted(A | B))
print("intersection", sorted(A & B))
print("difference  ", sorted(A - B))
print("symmetric   ", sorted(A ^ B))
```

**1.** With $A = \{1, 2, 3, 4, 5\}$ and $B = \{4, 5, 6, 7\}$, find each.

- (a) $A \cup B$
- (b) $A \cap B$
- (c) $A \setminus B$
- (d) $B \setminus A$

<details class="dl-answer"><summary>answer</summary>

(a) $\{1, 2, 3, 4, 5, 6, 7\}$. (b) $\{4, 5\}$. (c) $\{1, 2, 3\}$. (d) $\{6, 7\}$.

(c) and (d) being different is the point: difference is not symmetric, unlike union and intersection.

</details>

**2.** Find $A \triangle B$ — the symmetric difference, everything in exactly one of them.

<details class="dl-answer"><summary>answer</summary>

$\{1, 2, 3, 6, 7\}$.

It is $(A \setminus B) \cup (B \setminus A)$, and also $(A \cup B) \setminus (A \cap B)$. Those two descriptions produce the same set by different routes, which is worth checking on the numbers above.

</details>

**3.** How many elements are in $A \cup B$? Why is it not $|A| + |B|$?

<details class="dl-answer"><summary>answer</summary>

Seven, not nine.

$|A \cup B| = |A| + |B| - |A \cap B|$: 5 + 4 − 2. The two shared elements were counted twice and must be taken back once. This is inclusion–exclusion, and *Drawing Sets* makes it a picture.

</details>

**4.** True or false, and say why.

- (a) $\{1, 2\} \subset \{1, 2, 3\}$
- (b) $\{1, 2\} \subset \{1, 2\}$
- (c) $\emptyset \subset \{1, 2\}$
- (d) $\{1, 2\} \in \{1, 2, 3\}$

<details class="dl-answer"><summary>answer</summary>

(a) True. (b) True — a set is a subset of itself. (c) True — the empty set is a subset of everything, because there is no element of it to be missing. (d) False.

(d) is the one worth dwelling on. $\in$ asks about membership and $\subset$ about containment. $\{1, 2\}$ is not one of the three elements of $\{1, 2, 3\}$; it is a collection of two of them.

</details>

**5.** How many subsets does a set of 4 elements have? Of n elements?

<details class="dl-answer"><summary>answer</summary>

16, and $2^n$.

Each element is either in or out, independently — n binary choices. That includes the empty set and the whole set, both of which are genuine subsets.

This is why a set of 20 elements has over a million subsets, and why "just check all the subsets" stops being a plan very quickly.

</details>

**6.** Prove $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ with an example, then say what it corresponds to in ordinary algebra.

<details class="dl-answer"><summary>answer</summary>

With $A = \{1,2,3\}$, $B = \{2,4\}$, $C = \{3,5\}$: the left is $\{1,2,3\} \cap \{2,3,4,5\} = \{2,3\}$, and the right is $\{2\} \cup \{3\} = \{2,3\}$.

It is the distributive law, $a(b + c) = ab + ac$, with $\cap$ playing the part of multiplication and $\cup$ of addition.

The analogy is not perfect and the imperfection is interesting: in set theory, union also distributes over intersection. In arithmetic, $a + bc$ is not $(a+b)(a+c)$.

</details>

## Making Sets

**7.** Write `make_set(items)` returning a sorted list with duplicates removed.

<details class="dl-answer"><summary>answer</summary>

```python
def make_set(items):
    """A sorted list of the distinct values in items."""
    result = []
    for item in sorted(items):
        if not result or item != result[-1]:
            result.append(item)
    return result
```

`make_set([3, 1, 4, 1, 5])` gives `[1, 3, 4, 5]`.

Sorting first means duplicates are adjacent, so checking against the last one kept is enough. Without sorting you would have to search the whole result each time, which is n² instead of n log n.

</details>

**8.** Write `is_member(items, target)` for a sorted list, in fewer than n steps.

<details class="dl-answer"><summary>answer</summary>

Binary search — the same function as in *Finding Things*, returning a yes or no rather than a position.

```python
def is_member(items, target):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return True
        if target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return False
```

Being sorted is what earns this. It is the whole reason for representing a set as a *sorted* list rather than as any old list.

</details>

## The Merge Walk

```python exec
id: the-merge-walk-1
def union(a, b):
    """All elements of either, sorted, walking both lists once."""
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result + a[i:] + b[j:]


print(union([1, 3, 4, 5], [1, 2, 5, 7, 8]))
```

**9.** Write `intersection(a, b)` with the same pattern.

<details class="dl-answer"><summary>answer</summary>

```python
def intersection(a, b):
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return result
```

Identical skeleton, three different bodies. And no leftover step at the end — when one list runs out there is nothing left that could be in both.

</details>

**10.** Write `difference(a, b)`.

<details class="dl-answer"><summary>answer</summary>

```python
def difference(a, b):
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1; j += 1
        elif a[i] < b[j]:
            result.append(a[i]); i += 1
        else:
            j += 1
    return result + a[i:]
```

The leftover step is back, and only for `a`. Anything remaining in `b` when `a` runs out cannot be in the difference.

</details>

**11.** Write `symmetric_difference(a, b)` two ways: with the merge walk, and by combining functions you already have.

<details class="dl-answer"><summary>answer</summary>

By combination:

```python
def symmetric_difference(a, b):
    return union(difference(a, b), difference(b, a))
```

By merge walk, it is the union body with the equal case appending nothing.

The combined version walks the lists four times and is obviously correct. The merge version walks them once and takes a minute to verify. Which one to write depends entirely on whether anything is measurably slow, and the honest default is the readable one.

</details>

**12.** Why is the merge walk faster than the obvious approach?

<details class="dl-answer"><summary>answer</summary>

The obvious approach — for each element of a, search b — costs n × m, or n × log m with binary search.

The merge walk costs n + m, because each pointer only ever moves forwards. For two sets of a thousand elements each that is two thousand steps rather than a million.

This only works because both lists are sorted. Sortedness is the resource being spent here, and it is the same resource binary search spends.

</details>

**13.** Write `is_subset(a, b)`. How does it relate to intersection?

<details class="dl-answer"><summary>answer</summary>

```python
def is_subset(a, b):
    return intersection(a, b) == a
```

If everything in a is also in b, then their intersection is all of a.

A direct merge walk is faster — it can stop the moment it finds an element of a that is not in b, without building anything. But the one-liner says what a subset *is*, and that is worth something.

</details>

**14.** Write `is_equal(a, b)`, and relate it to `is_subset`.

<details class="dl-answer"><summary>answer</summary>

For sorted sets it is just `a == b`.

Definitionally, two sets are equal when each is a subset of the other: `is_subset(a, b) and is_subset(b, a)`. That is the version that still works when the representation is not sorted, and it is how the equality is actually defined in mathematics.

</details>

## Sets in Practice

**15.** Two students' module lists are given. Find the modules both take, the ones only the first takes, and the total distinct modules.

<details class="dl-answer"><summary>answer</summary>

```python
ann = {"maths", "programming", "databases", "networks"}
ben = {"programming", "databases", "web", "security"}

print(sorted(ann & ben))       # both
print(sorted(ann - ben))       # only Ann
print(len(ann | ben))          # distinct in total
```

`['databases', 'programming']`, `['maths', 'networks']`, and 6.

</details>

**16.** Given two lists of email addresses, find the ones that appear in both, ignoring case.

<details class="dl-answer"><summary>answer</summary>

```python
common = {e.lower() for e in first} & {e.lower() for e in second}
```

Normalising before comparing is the whole job. Email addresses are case-insensitive in their domain part and technically case-sensitive before the @, which almost no provider honours — so lowercasing is right in practice and wrong in the standard, and that is worth knowing before you deduplicate anybody's mailing list.

</details>

**17.** Find the words that appear in one document and not another.

<details class="dl-answer"><summary>answer</summary>

```python
def words(text):
    return {w.strip(".,!?;:'\"").lower() for w in text.split() if w.strip(".,!?;:'\"")}


only_in_first = words(one) - words(two)
```

Stripping punctuation before comparing matters more than it looks: without it, `cat` and `cat.` are different words and the answer fills up with noise.

</details>

**18.** A set has 3 elements. List all its subsets, and check there are 8.

<details class="dl-answer"><summary>answer</summary>

For $\{a, b, c\}$: $\emptyset$, $\{a\}$, $\{b\}$, $\{c\}$, $\{a,b\}$, $\{a,c\}$, $\{b,c\}$, $\{a,b,c\}$.

In code, counting in binary gives them in order:

```python
items = ["a", "b", "c"]
for pattern in range(2 ** len(items)):
    print([items[i] for i in range(len(items)) if pattern >> i & 1])
```

Each subset is a binary number: bit i says whether item i is in. That correspondence is why the count is exactly $2^n$, and it is a genuinely useful trick when you need to enumerate possibilities.

</details>

**19.** Why does Python's built-in `set` not keep its elements in order?

<details class="dl-answer"><summary>answer</summary>

Because it is a hash table, not a sorted list. Elements land in positions determined by their hash values, which have nothing to do with their order.

The trade is worth understanding: Python's set tests membership in constant time regardless of size, where a sorted list takes log n. What it gives up is ordering — you cannot ask a `set` for its smallest element without looking at all of it.

Building sets out of sorted lists, as this tutorial does, is the opposite trade. Neither is the right answer in general.

</details>
