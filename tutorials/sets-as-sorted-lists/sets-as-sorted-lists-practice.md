---
title: "Sets: building them from sorted lists — Practice"
practice_for: sets-as-sorted-lists
year: "2026-2027"
version: 2026.08.23.1
---

# Sets: building them from sorted lists — Practice

Each answer is hidden until you open it. About half of these problems are
set arithmetic, to do on paper. The other half ask you to write the
merge walk in code. Try the paper ones first. The code is much easier to
write once you know what it should produce.

## Set arithmetic

This first cell uses Python's own `set` type, which the tutorial did not
use. Python writes a set in curly brackets, and it has an operator for
each operation: `|` for union, `&` for intersection, `-` for difference
and `^` for symmetric difference. We wrap each result in `sorted()`,
because Python's `set` does not keep its elements in order (problem 19
says why). You can use this cell to check your paper answers.

```python exec
id: set-arithmetic-1
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7}

print("union       ", sorted(A | B))
print("intersection", sorted(A & B))
print("difference  ", sorted(A - B))
print("symmetric   ", sorted(A ^ B))
```

**1.** With $A = \{1, 2, 3, 4, 5\}$ and $B = \{4, 5, 6, 7\}$, find each of these.

- (a) $A \cup B$
- (b) $A \cap B$
- (c) $A \setminus B$
- (d) $B \setminus A$

<details class="dl-answer"><summary>answer</summary>

(a) $\{1, 2, 3, 4, 5, 6, 7\}$. (b) $\{4, 5\}$. (c) $\{1, 2, 3\}$. (d) $\{6, 7\}$.

Look at (c) and (d). They are different. That is the point of this
problem. For union and intersection, the order of the two sets makes no
difference. For difference, it does.

</details>

**2.** The symmetric difference of $A$ and $B$ is written $A \triangle B$. It holds everything that is in exactly one of the two sets. Find $A \triangle B$.

<details class="dl-answer"><summary>answer</summary>

It is $\{1, 2, 3, 6, 7\}$.

There are two ways to describe it. It is $(A \setminus B) \cup (B \setminus A)$,
and it is also $(A \cup B) \setminus (A \cap B)$. The two descriptions
take different routes to the same set. Can you check that on the numbers
above?

</details>

**3.** How many elements are in $A \cup B$? Why is it not $|A| + |B|$?

<details class="dl-answer"><summary>answer</summary>

There are seven elements, not nine.

$|A \cup B| = |A| + |B| - |A \cap B|$, which is $5 + 4 - 2 = 7$. The two
shared elements, 4 and 5, were counted twice, so we take them away
once. This is the inclusion-exclusion principle.
[Venn diagrams: drawing sets and their overlaps](tutorial:venn-diagrams)
turns it into a picture.

</details>

**4.** Is each of these true or false? Say why.

- (a) $\{1, 2\} \subseteq \{1, 2, 3\}$
- (b) $\{1, 2\} \subseteq \{1, 2\}$
- (c) $\emptyset \subseteq \{1, 2\}$
- (d) $\{1, 2\} \in \{1, 2, 3\}$

<details class="dl-answer"><summary>answer</summary>

(a) True.

(b) True. Every set is a subset of itself.

(c) True. The empty set is a subset of every set. For it to fail, one of
its elements would have to be missing from $\{1, 2\}$, and it has no
elements.

(d) False.

(d) is the one to think about. $\in$ asks about membership: is this
thing one of the elements? $\subseteq$ asks about containment: are all of
these things among the elements? $\{1, 2\}$ is a set made of two of the
elements of $\{1, 2, 3\}$. It is not itself one of the three elements
1, 2 and 3.

</details>

**5.** How many subsets does a set of 4 elements have? How many does a set of $n$ elements have?

<details class="dl-answer"><summary>answer</summary>

A set of 4 elements has 16 subsets, and a set of $n$ elements has $2^n$.

For each element there are two choices: it is in the subset, or it is
out. The choices do not depend on each other, so with $n$ elements there
are $2 \times 2 \times \dots \times 2 = 2^n$ ways to choose. This count
includes the empty set and the whole set. Both of them are subsets.

This is why a set of 20 elements has over a million subsets
($2^{20} = 1{,}048{,}576$). A plan to "check all the subsets" stops
working very quickly.

</details>

**6.** Check that $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ with an example. Then say which rule of ordinary algebra it matches.

<details class="dl-answer"><summary>answer</summary>

Take $A = \{1,2,3\}$, $B = \{2,4\}$ and $C = \{3,5\}$.

- The left side is $\{1,2,3\} \cap \{2,3,4,5\} = \{2,3\}$.
- The right side is $\{2\} \cup \{3\} = \{2,3\}$.

The two sides are equal. One example does not prove the rule for every
set, but the rule is true for all sets, and the example shows how it
works.

It matches the distributive law of algebra, $a(b + c) = ab + ac$. Here
$\cap$ plays the part of multiplication, and $\cup$ plays the part of
addition.

The match is not perfect, and the difference is interesting. For sets,
union also distributes over intersection:
$A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$. In arithmetic, the
matching rule fails: $a + bc$ is not equal to $(a+b)(a+c)$.

</details>

## Making sets

**7.** Write `make_set(items)`. It should return a sorted list with the repeats removed.

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

After the sort, any repeats sit next to each other. So it is enough to
compare each item with the last one we kept. Without a sort, we would
have to search the whole result for every item. That takes about $n^2$
steps, but a sort first takes about $n \log n$.

</details>

**8.** Write `is_member(items, target)` for a sorted list. Can it take fewer than $n$ steps?

<details class="dl-answer"><summary>answer</summary>

Yes, with binary search. It is the same function as in
[Searching a list: linear and binary search](tutorial:finding-things),
except that it returns yes or no (`True` or `False`) instead of a
position.

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

This only works because the list is sorted. That is the whole reason to
store a set as a *sorted* list, and not as a list in any order.

</details>

## The merge walk

Here is `union()` from the tutorial, written more compactly. It adds
whatever is left of each list with slices, `a[i:]` and `b[j:]`. The
other problems in this section build on it.

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

The outline is the same as `union()`, but each of the three cases does
something different. There is also no step at the end for leftovers.
When one list runs out, nothing left in the other list can be in both.

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

The leftover step is back, but only for `a`. Anything still left in `b`
when `a` runs out cannot be in the difference.

</details>

**11.** Write `symmetric_difference(a, b)` in two ways: first with the merge walk, then by combining functions you already have.

<details class="dl-answer"><summary>answer</summary>

By combining functions:

```python
def symmetric_difference(a, b):
    return union(difference(a, b), difference(b, a))
```

With the merge walk, it is the body of `union()`, except that the equal
case adds nothing to the result.

The combined version passes over the lists four times, and it is easy
to see that it is correct. The merge-walk version passes over them
once, but it takes a minute to check. Which one should you write? That
depends on whether the slower one is slow enough to matter. If it is
not, the easier one to read is the better choice.

</details>

**12.** Why is the merge walk faster than the most direct approach?

<details class="dl-answer"><summary>answer</summary>

The most direct approach takes each element of a and searches b for it.
That costs $n \times m$ steps, or $n \times \log m$ with binary search.

The merge walk costs $n + m$ steps, because each pointer only ever moves
forwards. For two sets of a thousand elements each, that is two thousand
steps instead of a million.

This only works because both lists are sorted. The merge walk depends
on sorted order, and so does binary search.

</details>

**13.** Write `is_subset(a, b)`. How does it relate to intersection?

<details class="dl-answer"><summary>answer</summary>

```python
def is_subset(a, b):
    return intersection(a, b) == a
```

If everything in a is also in b, then the intersection of a and b is all
of a.

A direct merge walk would be faster. It can stop as soon as it finds an
element of a that is not in b, and it does not need to build a new list.
But the one-line version says what a subset *is*, and that has value
too.

</details>

**14.** Write `is_equal(a, b)`. How does it relate to `is_subset`?

<details class="dl-answer"><summary>answer</summary>

For our sorted sets, `is_equal(a, b)` is `a == b`.

By definition, two sets are equal when each one is a subset of the other:
`is_subset(a, b) and is_subset(b, a)`. This version still works when the
sets are not stored in sorted order. Mathematics defines equal sets this
way too.

</details>

## Sets in practice

The answers in this section use Python's own `set` type again, with the
same operators as the first cell. Problems 16 and 17 also build sets with
a comprehension in curly brackets. It works like a list comprehension,
but it makes a set.

**15.** Two students each take a list of modules. Find the modules both of them take, the ones only the first student takes, and the total number of different modules.

<details class="dl-answer"><summary>answer</summary>

```python
ann = {"maths", "programming", "databases", "networks"}
ben = {"programming", "databases", "web", "security"}

print(sorted(ann & ben))       # both
print(sorted(ann - ben))       # only Ann
print(len(ann | ben))          # distinct in total
```

This prints `['databases', 'programming']`, then `['maths', 'networks']`,
then 6.

</details>

**16.** You have two lists of email addresses. Find the addresses that appear in both, ignoring upper and lower case.

<details class="dl-answer"><summary>answer</summary>

```python
common = {e.lower() for e in first} & {e.lower() for e in second}
```

The main job is to make the addresses match before we compare them, here
by changing them all to lower case.

There is a detail worth knowing before you remove repeats from anybody's
mailing list. The part after the @ is not case-sensitive. The official
standard says the part before the @ can be case-sensitive, but almost no
email provider treats it that way. So lower case is right in
practice, even though the standard does not promise it.

</details>

**17.** Find the words that appear in one document but not in another.

<details class="dl-answer"><summary>answer</summary>

```python
def words(text):
    return {w.strip(".,!?;:'\"").lower() for w in text.split() if w.strip(".,!?;:'\"")}


only_in_first = words(one) - words(two)
```

It matters more than it looks to remove the punctuation before we compare.
Without it, `cat` and `cat.` count as different words, and the answer
fills up with noise.

</details>

**18.** A set has 3 elements. List all its subsets, and check that there are 8.

<details class="dl-answer"><summary>answer</summary>

For $\{a, b, c\}$ the subsets are $\emptyset$, $\{a\}$, $\{b\}$, $\{c\}$, $\{a,b\}$, $\{a,c\}$, $\{b,c\}$ and $\{a,b,c\}$.

In code, we can produce all of them by counting in binary from 0 to 7:

```python
items = ["a", "b", "c"]
for pattern in range(2 ** len(items)):
    print([items[i] for i in range(len(items)) if pattern >> i & 1])
```

Each subset matches one binary number. Bit `i` of the number says
whether item `i` is in the subset. In the code, `pattern >> i & 1` reads
bit `i` of `pattern`. It gives 1 if the bit is on and 0 if it is off.
Because subsets match binary numbers, the count is exactly $2^n$. It is also a useful trick whenever you need to list every
possible choice.

</details>

**19.** Why does Python's own `set` not keep its elements in order?

<details class="dl-answer"><summary>answer</summary>

Python's `set` is a *hash table*, and not a sorted list. A hash table
calculates a number, called a hash, from each element, and uses it to
decide where the element is stored. The hash has nothing to do with the
order of the elements.

There is a trade here. Python's `set` tests membership in about the same
time however large the set is, on average. A sorted list takes about
$\log n$ steps. The `set` loses order. You cannot ask a `set`
for its smallest element without looking at all of it.

When we build sets from sorted lists, as the tutorial does, we make the
opposite trade. Neither choice is right for every problem.

</details>
