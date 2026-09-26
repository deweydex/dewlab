---
title: "Racing the sorts: counting steps — Practice"
practice_for: racing-the-sorts
year: "2026-2027"
version: 2026.09.25.1
---

# Racing the sorts: counting steps — Practice

Each answer is hidden until you open it, and each one is one way
through: yours may go another way. Where a problem asks you to predict,
the prediction is the exercise, so make one before you run anything.

Your toolkit is loaded on this page, so `shell_sort`, `selection_sort`,
`insertion_sort`, `binary_search` and `median` are ready to use. The
counting racers from the page are not in the toolkit, so the first cell
below holds them. Run it once before anything else.

## Warm-up

```python exec
id: racing-practice-tools
import random
import time

def random_list(size):
    """Give back a new list of size random whole numbers from 1 to 10,000."""
    numbers = []
    for count in range(size):
        numbers.append(random.randint(1, 10000))
    return numbers


def selection_count(values):
    """Selection sort a copy of values. Give back how many comparisons it made."""
    items = values.copy()
    comparisons = 0
    for place in range(len(items) - 1):
        smallest_at = place
        for i in range(place + 1, len(items)):
            comparisons = comparisons + 1
            if items[i] < items[smallest_at]:
                smallest_at = i
        items[place], items[smallest_at] = items[smallest_at], items[place]
    return comparisons


def insertion_count(values):
    """Insertion sort a copy of values. Give back how many comparisons it made."""
    items = values.copy()
    comparisons = 0
    for place in range(1, len(items)):
        item = items[place]
        i = place
        while i > 0 and items[i - 1] > item:
            comparisons = comparisons + 1
            items[i] = items[i - 1]
            i = i - 1
        if i > 0:
            comparisons = comparisons + 1
        items[i] = item
    return comparisons


def shell_count(values):
    """Shell sort a copy of values. Give back how many comparisons it made."""
    items = values.copy()
    comparisons = 0
    gap = len(items) // 2
    while gap > 0:
        for place in range(gap, len(items)):
            item = items[place]
            i = place
            while i >= gap and items[i - gap] > item:
                comparisons = comparisons + 1
                items[i] = items[i - gap]
                i = i - gap
            if i >= gap:
                comparisons = comparisons + 1
            items[i] = item
        gap = gap // 2
    return comparisons

print("The racers are ready.")
```

**1. Predict.** A teacher sorts 20 exam marks with selection sort. How
many comparisons does it make? Work it out before you check with
`selection_count(random_list(20))`.

<details class="dl-answer"><summary>answer</summary>

190. Selection sort always makes $\frac{n(n-1)}{2}$ comparisons, so for
20 marks it is $\frac{20 \times 19}{2} = 190$, whatever the marks are.

</details>

**2. Predict.** A bus timetable lists departure times that are already
in order: `[7, 8, 9, 10, 11, 12]`. How many comparisons does
`insertion_count` make on it?

<details class="dl-answer"><summary>answer</summary>

5. Each time from the second on looks once to its left, finds a smaller
time, and stays where it is. That is one comparison for each of the 5
times after the first. For a list already in order, insertion sort
makes $n - 1$ comparisons.

</details>

**3. Make.** Here are the highest temperatures of a made-up week in
Galway, in degrees: `[14, 17, 12, 15, 19, 13, 16]`. Sort them with
`shell_sort`, and check your answer against `sorted()`. Then check
that the original list did not change.

<details class="dl-answer"><summary>answer</summary>

```python
week = [14, 17, 12, 15, 19, 13, 16]
in_order = shell_sort(week)
print(in_order)                    # [12, 13, 14, 15, 16, 17, 19]
print(in_order == sorted(week))    # True
print(week)                        # [14, 17, 12, 15, 19, 13, 16]
```

`shell_sort` promises a new list and leaves the old one alone, so
`week` is as it was.

</details>

**4. Explain.** Why does selection sort make exactly the same number of
comparisons on every list of 1,000 values, sorted or not, while
insertion sort does not?

<details class="dl-answer"><summary>answer</summary>

To find the smallest value in the rest of the list, selection sort must
look at every value in the rest. Nothing it has seen tells it where the
smallest is, so it cannot stop early. So round 1 always makes 999
comparisons, round 2 makes 998, and so on.

Insertion sort stops sliding a value as soon as it meets a smaller one.
How soon that happens depends on the order the list starts in. A list
in order stops every value at once; a list in reverse order slides
every value all the way.

</details>

## Core

```python exec
id: racing-practice-scratch-2
# Use this cell for the core problems
```

**5. Predict.** Your music app sorted 1,000 songs with selection sort in
499,500 comparisons. You add another 1,000 songs. About how many
comparisons for 2,000? Guess first, then work it out exactly with the
formula.

<details class="dl-answer"><summary>answer</summary>

About four times as many, since doubling $n$ multiplies $n^2$ by
$2^2 = 4$. Exactly:

$$\frac{2000 \times 1999}{2} = 1\,999\,000$$

```python
print(selection_count(random_list(2000)))    # 1999000
```

That is 4.002 times 499,500: quadratic growth.

</details>

**6. Make.** A game shows a leaderboard, and you want to test that a
list really is in order. Write `is_in_order(values)`, which gives back
`True` when every value is no bigger than the one after it. Use it to
check `shell_sort` on 100 random lists of 50 values. How many
comparisons does `is_in_order` make on a list of $n$ values?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over the indexes from 0 to `len(values) - 2`, so that `i + 1`
   is always a real index.
2. If `values[i] > values[i + 1]`, the list is out of order: give back
   `False` at once.
3. If the loop finishes, give back `True`.

**Think about:** what should an empty list give?

**Try this next:** is `is_in_order` quicker than sorting the list and
comparing?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def is_in_order(values):
    """Give back True when each value is no bigger than the next."""
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            return False
    return True

for test_number in range(100):
    assert is_in_order(shell_sort(random_list(50)))
print(is_in_order([3, 1, 2]), is_in_order([]))    # False True
```

At most $n - 1$ comparisons, one for each pair of neighbours. Checking
that a list is sorted is far cheaper than sorting it. An empty list
gives `True`, because it has no pair out of order.

</details>

**7. Fix.** Schlomi, who is learning Python too, wrote her own Shell
sort to put the sizes of eight photos in order, in kilobytes. Halving
the gap is dividing by 2, so she wrote `gap / 2`. That is a fair
reading of "halve". The cell is meant to fail. Read the last line of
the error, find the line that stops it, and change it.

```python exec
id: racing-practice-fix-gap
def shell_sort_draft(values):
    """Return a new sorted list, by Shell sort."""
    items = values.copy()
    gap = len(items) // 2
    while gap > 0:
        for place in range(gap, len(items)):
            item = items[place]
            i = place
            while i >= gap and items[i - gap] > item:
                items[i] = items[i - gap]
                i = i - gap
            items[i] = item
        gap = gap / 2
    return items

print(shell_sort_draft([1507, 1320, 1745, 1288, 1602, 1411, 1390, 1533]))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last line says `'float' object cannot be interpreted as an
   integer`. Which name holds a float?
2. The first pass, with a gap of 4, ran. What is `gap` for the second
   pass?
3. Which kind of division, from
   [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
   always gives a whole number?

**Think about:** why did the first pass work?

**Try this next:** what would `gap` be after `2 / 2`, `1 / 2`, and so
on? Would the loop ever end?

</details>

<details class="dl-answer"><summary>answer</summary>

`gap = gap / 2` makes `gap` a float: 4 becomes 2.0. `range(2.0, 8)`
cannot count from a float, so the second pass stops with a
`TypeError`. Schlomi's halving needs to stay in the whole numbers,
which is floor division:

```python
        gap = gap // 2
```

Now it prints `[1288, 1320, 1390, 1411, 1507, 1533, 1602, 1745]`. With
`/`, the gap would also never reach 0: 1, 0.5, 0.25 and on, so the
`while` loop would never end even if `range` allowed it.

</details>

**8. Fix.** Schlomo, who is learning Python too, times `shell_sort` on
1,000 values. He reads the clock before the sort and after it, and
subtracts one from the other. His cell prints a time below zero. Which
line needs to change?

```python exec
id: racing-practice-fix-timer
numbers = random_list(1000)
start = time.perf_counter()
shell_sort(numbers)
seconds = start - time.perf_counter()
print(round(seconds * 1000, 2), "ms")
```

<details class="dl-answer"><summary>answer</summary>

The two readings are the plan Schlomo needs. The subtraction runs the
other way round from what he meant. The clock reading after the sort
is the bigger number, so the time taken is the later reading minus the
earlier one:

```python
seconds = time.perf_counter() - start
```

Order matters in a subtraction, as it does in the steps of a program.

</details>

**9. Predict.** A playlist of 100 songs is sorted Z to A, and you want
it A to Z. How many comparisons will insertion sort make? And
selection sort?

<details class="dl-answer"><summary>answer</summary>

Both make 4,950. A list in reverse order is insertion sort's worst
case: every song slides all the way to the front, so it compares with
every song before it, $1 + 2 + \dots + 99 = \frac{99 \times 100}{2} =
4950$. Selection sort makes 4,950 on every list of 100.

```python
backwards = list(range(100, 0, -1))
print(insertion_count(backwards), selection_count(backwards))    # 4950 4950
```

</details>

**10. Another way.** Here are seven response times of a website, in
milliseconds: `[210, 190, 3400, 180, 230, 1850, 200]`. Find the median
by sorting them with `shell_sort` and taking the middle one. Then check
with your toolkit's `median` from
[What is typical?](tutorial:what-is-typical).

<details class="dl-answer"><summary>answer</summary>

```python
response_ms = [210, 190, 3400, 180, 230, 1850, 200]
in_order = shell_sort(response_ms)
print(in_order)                        # [180, 190, 200, 210, 230, 1850, 3400]
print(in_order[len(in_order) // 2])    # 210
print(median(response_ms))             # 210
```

Both give 210 ms. With 7 values, the middle one is at index 3. A median
needs the values in order, so every median starts with a sort.

</details>

**11. Make.** A game's leaderboard holds 1,000 scores in order. Five new
scores arrive and are put at the end. Make that list with
`sorted(random_list(1000)) + random_list(5)`, and race all three of
our sorts on it. Which wins?

<details class="dl-answer"><summary>answer</summary>

```python
board = sorted(random_list(1000)) + random_list(5)
print(selection_count(board), insertion_count(board), shell_count(board))
```

One run gave 504,510 for selection sort, 3,680 for insertion sort and
9,335 for Shell sort. Your numbers will differ a little, but insertion
sort wins. The first 1,000 values are already in order, so each costs
one comparison; only the five new ones slide, each part of the way.
Shell sort's long jumps are work this list did not need.

</details>

**12. Explain.** This course had you write three sorts of your own, and
only then showed you that Python's `sorted()` beats all of them. Another
course might start from `sorted()`, and use it from the first day. Which
way would you have taught sorting, and why?

<details class="dl-answer"><summary>answer</summary>

There is more than one answer worth giving. Here are some things an
answer might weigh.

- What each way lets a reader do soon. Starting from `sorted()` gets
  real work done on day one, which is how most programmers work.
- What each way shows. Writing a sort shows what a comparison is, why
  the starting order matters, and why the work grows as it does. With
  only `sorted()`, those stay hidden inside it.
- What the reader will need later. Someone who will choose between
  methods, or explain why a program is slow, needs the inside view.
  Someone who needs a sorted list once may not.
- The cost in time and patience. Three sorts take hours that could go
  elsewhere.

It also helps to say who the course is for, since the choice changes
with the reader.

</details>

## Stretch

```python exec
id: racing-practice-scratch-3
# Use this cell for the stretch problems
```

**13. Another way.** Shell sort's gaps do not have to halve. In 1973,
Donald Knuth suggested the gaps 1, 4, 13, 40, 121, 364, and so on, where
each gap is 3 times the one before, plus 1. Write a counting Shell sort
that uses these gaps, largest first, and race it against `shell_count`
on the same 1,000 random values.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Build the list of gaps first: start with `[1]`, and append
   `3 * gaps[-1] + 1` while that is smaller than the length of the list.
2. Go through the gaps from largest to smallest. `reversed(gaps)` does
   that.
3. The inside of each pass is the same as in `shell_count`.

**Think about:** what must the last gap always be, and why?

**Try this next:** try both on 10,000 values.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def knuth_count(values):
    """Shell sort a copy of values with gaps 1, 4, 13, 40, ...; give back the comparisons."""
    items = values.copy()
    comparisons = 0
    gaps = [1]
    while 3 * gaps[-1] + 1 < len(items):
        gaps.append(3 * gaps[-1] + 1)
    for gap in reversed(gaps):
        for place in range(gap, len(items)):
            item = items[place]
            i = place
            while i >= gap and items[i - gap] > item:
                comparisons = comparisons + 1
                items[i] = items[i - gap]
                i = i - gap
            if i >= gap:
                comparisons = comparisons + 1
            items[i] = item
    return comparisons

numbers = random_list(1000)
print(knuth_count(numbers), shell_count(numbers))
```

For 1,000 values the gaps are 364, 121, 40, 13, 4 and 1. Three runs
gave about 13,600 to 14,200 for Knuth's gaps against about 14,800 to
15,400 for halving: a little better. The last gap must be 1, so that
the last pass is an ordinary insertion sort and the list ends fully in
order.

</details>

**14. Make.** Add Shell sort to the picture from the page. Count all
three sorts on random lists of 100, 200, and so on up to 1,000 values,
and plot the three lines. What shape is the Shell sort line?

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

sizes = list(range(100, 1001, 100))
counts = {"selection sort": [], "insertion sort": [], "Shell sort": []}
for size in sizes:
    numbers = random_list(size)
    counts["selection sort"].append(selection_count(numbers))
    counts["insertion sort"].append(insertion_count(numbers))
    counts["Shell sort"].append(shell_count(numbers))

for name in counts:
    plt.plot(sizes, counts[name], marker="o", label=name)
plt.xlabel("values in the list")
plt.ylabel("comparisons")
plt.legend()
```

The Shell sort line lies close to the bottom, reaching about 15,000 at
1,000 values while selection sort reaches 499,500. It still bends
upwards a little, so it grows faster than a straight line, but much
more slowly than the other two. The dictionary here is the kind from
[Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts).

</details>

**15. Predict.** When the list doubles in length, selection sort's
count goes up about 4 times. What do you think happens to Shell sort's
count? Guess, then count it for 1,000, 2,000 and 4,000 random values.

<details class="dl-answer"><summary>answer</summary>

```python
for size in [1000, 2000, 4000]:
    print(size, shell_count(random_list(size)))
```

One run gave about 14,500, 36,000 and 85,000. Each doubling multiplies
the count by about 2.4. That is more than 2, the growth of a straight
line, and less than 4, the quadratic growth of selection sort. Shell
sort sits between the two.

</details>

**16. Make.** A travel app keeps a list of Irish counties in the order
they were added. Sort them with `shell_sort`, then find Kerry with
`binary_search`. How many comparisons did the sort make?

```python
counties = ["Wexford", "Carlow", "Kerry", "Donegal", "Galway", "Mayo",
            "Cork", "Louth", "Clare", "Sligo", "Offaly", "Dublin"]
```

<details class="dl-answer"><summary>answer</summary>

```python
in_order = shell_sort(counties)
print(in_order)
print(binary_search(in_order, "Kerry"))    # 6
print(shell_count(counties))               # 37
```

The sorted list starts Carlow, Clare, Cork, Donegal, Dublin, Galway,
and Kerry is at index 6. The sort made 37 comparisons. Words compare
letter by letter, so every sort here works on them without a change.
Sorting once and then searching many times is how a phone keeps its
contacts quick to find.

</details>

## Where to read more

Stand-up Maths (2022). *Someone improved my code by 40,832,277,770%.*
<https://www.youtube.com/watch?v=c33AZBnRHks>. Matt Parker wrote a program
that took about a month to run. Viewers made the same job run in a tiny
fraction of a second, by choosing better ways to do it. About twenty-nine
minutes.
