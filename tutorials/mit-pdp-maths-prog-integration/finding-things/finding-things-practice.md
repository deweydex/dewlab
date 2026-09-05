---
title: "Finding Things — Practice"
slug: finding-things-practice
practice_for: finding-things
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Finding Things — Practice

Answers are folded. Several of these are about counting comparisons rather than writing code, and those are the ones worth doing on paper first.

## Scope

```python exec
id: scope-1
count = 0

def bump():
    count = 10          # a new, local count
    return count


print(bump(), count)
```

**1.** What does the cell above print, and why is `count` still 0 afterwards?

<details class="dl-answer"><summary>answer</summary>

`10 0`.

The assignment inside the function created a *new* variable that exists only while the function is running. Assigning inside a function never reaches out and changes a variable outside it, unless you say `global` — and needing `global` is usually a sign the function should return a value instead.

</details>

**2.** What does this print?

```python
def add_item(items):
    items.append("new")


things = ["a", "b"]
add_item(things)
print(things)
```

<details class="dl-answer"><summary>answer</summary>

`['a', 'b', 'new']`.

This looks like it contradicts the previous question, and it does not. The function did not *assign* to `items`; it changed the list `items` refers to, which is the same list `things` refers to. Rebinding a name is local; changing an object is not.

Functions that quietly modify their arguments are a common source of surprise. It is worth deciding deliberately whether a function returns a new list or edits the one it was given, and saying so in its name.

</details>

**3.** What is a pure function, and which of these are pure?

- (a) `def double(x): return x * 2`
- (b) `def add_to_log(msg): log.append(msg)`
- (c) `def roll(): return random.randint(1, 6)`
- (d) `def area(r): return 3.14159 * r * r`

<details class="dl-answer"><summary>answer</summary>

A pure function depends only on its arguments and changes nothing outside itself. Same input, same output, no side effects.

(a) and (d) are pure. (b) changes something outside. (c) gives a different answer each time.

Pure functions are the ones you can test easily, reason about safely, and cache. Both of the impure ones here are useful and necessary — the point is knowing which kind you are writing.

</details>

## Linear Search

**4.** Write `linear_search(items, target)` returning the index or −1.

<details class="dl-answer"><summary>answer</summary>

```python
def linear_search(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1
```

The `return -1` has to be outside the loop. Inside, it would return −1 after checking only the first item.

</details>

**5.** Why −1 rather than 0 for "not found"?

<details class="dl-answer"><summary>answer</summary>

Because 0 is a real index — it means "found at the start". A not-found marker has to be something that could never be a genuine answer, and no list has an item at index −1 in the "found here" sense.

Returning `None` is the more Pythonic choice, and it has the advantage that using it by accident fails loudly rather than pointing at the last element.

</details>

**6.** How many comparisons does linear search make on a list of 100 items when the target is first? Last? Absent? On average?

<details class="dl-answer"><summary>answer</summary>

1, 100, 100, and about 50.

The average assumes the target is present and equally likely to be anywhere. If half your searches are for things that are absent, the average is much closer to 100 — which is why a cache that answers "not here" quickly is often the thing worth building.

</details>

**7.** Find the *last* occurrence of a target rather than the first.

<details class="dl-answer"><summary>answer</summary>

```python
def last_index(items, target):
    for i in range(len(items) - 1, -1, -1):
        if items[i] == target:
            return i
    return -1
```

Searching backwards returns on the first match found, which is the last one in the list. The alternative — searching forwards and remembering the most recent match — always looks at every item, even when the match is at the end.

</details>

## Binary Search

```python exec
id: binary-search-1
def binary_search(items, target):
    low, high, steps = 0, len(items) - 1, 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if items[mid] == target:
            return mid, steps
        if target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, steps


data = list(range(0, 1000, 3))
print(binary_search(data, 750))
print(binary_search(data, 751))
```

**8.** Trace binary search for 31 in `[3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]`. Write down each `mid` it looks at.

<details class="dl-answer"><summary>answer</summary>

Indices 0–14, so mid is 7 — which is 31. Found in one comparison.

That is the best case, and it happens because 31 sits exactly in the middle. Try 89 instead: mid 7 (31), then 11 (55), then 13 (72), then 14 (89). Four comparisons.

</details>

**9.** What goes wrong if the list is not sorted?

<details class="dl-answer"><summary>answer</summary>

It reports "not found" for things that are in the list, and it does so without complaint.

That is the dangerous kind of wrong. The function has no way to tell that its precondition was broken, so it returns a confident answer. Whoever calls it is responsible for the list being sorted, and if that is not obvious from the code it belongs in the function's name or its docstring.

</details>

**10.** Why `mid = (low + high) // 2` rather than `(low + high) / 2`?

<details class="dl-answer"><summary>answer</summary>

An index must be a whole number. `/` gives a float, and `items[3.5]` is a `TypeError`.

There is a famous variant of this line: in languages with fixed-size integers, `low + high` can overflow on a very large list, and the fix is `low + (high - low) // 2`. That bug sat undetected in the standard Java library for nine years.

</details>

**11.** What is the maximum number of comparisons binary search needs on 1,000 items? On 1,000,000?

<details class="dl-answer"><summary>answer</summary>

10 and 20.

Each step halves the range, so the count is how many times you can halve n before reaching 1 — which is log₂n rounded up. 2¹⁰ is 1,024 and 2²⁰ is 1,048,576.

Multiplying the data by a thousand adds ten comparisons. That is what logarithmic growth means, and it is why binary search does not care how big your data is.

</details>

**12.** I am thinking of a number from 1 to 100 and you may ask "is it greater than X?". How many questions guarantee finding it?

<details class="dl-answer"><summary>answer</summary>

Seven.

Each question halves the range: 100 → 50 → 25 → 13 → 7 → 4 → 2 → 1. Six questions only guarantee narrowing 64 possibilities, and 100 is more than 64.

The general rule is that n yes-or-no questions can distinguish 2ⁿ possibilities, which is the same statement as binary search's cost and also the reason a 7-bit code has 128 values.

</details>

**13.** Binary search needs sorted data, and sorting takes longer than a single linear search. When is it worth it?

<details class="dl-answer"><summary>answer</summary>

When you search the same data more than a handful of times.

Sorting costs roughly n log n once. Each linear search costs n; each binary search costs log n. So sorting pays for itself after about log n searches — for a million items, after about twenty. Any lookup table, index or dictionary you have ever used is this trade-off already made for you.

If the data changes constantly and you search it rarely, linear search wins.

</details>

## Putting It Together

**14.** Modify binary search to return where the target *would* go if it is absent.

<details class="dl-answer"><summary>answer</summary>

```python
def insertion_point(items, target):
    low, high = 0, len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low
```

When the loop ends, `low` is the index where the target belongs. This is what `bisect.bisect_left` does, and it is the basis of keeping a list sorted as items arrive — search for the position, insert there.

Note the boundaries changed: `high` starts at `len(items)`, not `len(items) - 1`, and the loop is `<` rather than `<=`. Binary search is unusually sensitive to those two choices, which is why it is worth writing out rather than adapting from memory.

</details>

**15.** Count comparisons for both searches over a list of 334 items, for a target at the start, in the middle, at the end, and absent.

<details class="dl-answer"><summary>answer</summary>

Using `data = list(range(0, 1000, 3))`, which has 334 items:

| Target | Linear | Binary |
|---|---:|---:|
| 0 (first) | 1 | 8 |
| 498 (dead centre) | 167 | 1 |
| 999 (last) | 334 | 9 |
| 751 (absent) | 334 | 8 |

Binary search is *worse* than linear when the target is first — eight comparisons against one — and that is not a small point. If a few items are asked for constantly, moving them to the front beats any amount of cleverness, and that idea is a real cache design rather than a curiosity.

Note also that an absent target costs binary search nearly its worst case, because it has to narrow the range to nothing before it can say no. Linear search pays its full worst case for every absent target, every time.

</details>

**16.** Write a function that finds *all* the indices where a target appears.

<details class="dl-answer"><summary>answer</summary>

```python
def all_indices(items, target):
    return [i for i, item in enumerate(items) if item == target]
```

This has to be linear even on sorted data, because you cannot stop early — you do not know how many there are. On sorted data you could binary search for the first and last and take everything between, which is worth doing only when the list is large and the matches are few.

</details>

**17.** Search a list of names for one that is not there, and make the function report the closest match instead of failing.

<details class="dl-answer"><summary>answer</summary>

```python
def closest(names, target):
    best, best_score = None, -1
    for name in names:
        score = sum(1 for a, b in zip(name.lower(), target.lower()) if a == b)
        if score > best_score:
            best, best_score = name, score
    return best
```

Counting matching characters in matching positions is a crude measure, and it is enough to catch a typo in the first few letters. Real spell-checkers use edit distance, which asks how many insertions, deletions and substitutions separate two words — a considerably better answer and a considerably longer function.

The point of the exercise is the decision, not the metric: "not found" is often not the most useful thing a search can say.

</details>
