---
title: "Racing the sorts: counting steps"
year: "2026-2027"
version: 2026.09.25.1
datasets: [exoplanets, life-expectancy]
covers:
  lists-to-race-on:
    covers: [MIT-6.8]
    touches: [MIT-5.6]
  ten-a-hundred-a-thousand:
    covers: [MIT-6.8]
  a-picture-of-the-race:
    covers: [MIT-6.8]
  a-list-that-is-nearly-in-order:
    covers: [MIT-6.8, PDP-LO2]
  shell-sort-long-jumps-first:
    covers: [MIT-6.8]
  a-tool-for-your-toolkit:
    covers: [MIT-6.8]
    touches: [PDP-LO10]
  the-fourth-racer-sorted:
    covers: [PDP-LO2]
    touches: [MIT-6.8]
  six-thousand-planets:
    covers: [MIT-6.8]
    touches: [PDP-LO2]
  which-sort-where:
    covers: [PDP-LO2]
---

# Racing the sorts: counting steps

NASA's list of planets around other stars has more than six thousand
entries. Say we want them in order of the length of their year: the
time each one takes to go round its star. On the last page we sorted a
hand of five cards. Which of our two sorts would you trust with six
thousand planets? And is there a faster one?

Here is the surprise. Before we run anything, a formula from the last
page can tell us how long we would wait. And on that list, the planet
with the shortest year and the one with the longest are about four
billion times apart.

On this page we:

- make random lists of 10, 100 and 1,000 numbers, and count the
  comparisons each sort makes
- plot the counts, and see the shape of the growth before we name it
- sort a real list that is nearly in order already
- build a third sort, Shell sort, which makes long jumps first
- time Python's own `sorted()` against all three
- sort six thousand real planets, and choose the racers we can wait for
- ask which sort to use where

> **The space we're in.** Lists of numbers, and the two sorts from
> [Sorting a hand of cards](tutorial:sorting-a-hand-of-cards), which
> your toolkit now holds. Random numbers come from the `random` module,
> as on [How likely is it?](tutorial:how-likely-is-it). One thing
> usually goes unsaid: every comparison of two numbers takes about the
> same time, whatever the numbers are. That is why counting comparisons
> tells us how the work grows, without a clock.

## Warm-up

Two questions from earlier pages. The first is from
[Sorting a hand of cards](tutorial:sorting-a-hand-of-cards#counting-the-comparisons),
and the second from
[How likely is it?](tutorial:how-likely-is-it#letting-python-toss-the-coin).

```question
id: racing-warm-up-1
type: fill-in-the-blank

Selection sort on a hand of 6 cards compares $5 + 4 + 3 + 2 + 1$ pairs,
which is {15} comparisons.
```

```question
id: racing-warm-up-2
type: multiple-choice
correct: 3

Which numbers can `random.randint(1, 10)` give?

- 1 to 9
- 0 to 10
- 1 to 10, both ends included
```

## Lists to race on

A race needs a fair track, so let's start with lists of random
numbers, which suit no sort in particular. What will this print?

```python exec
id: racing-lists-1
import random

def random_list(size):
    """Give back a new list of size random whole numbers from 1 to 10,000."""
    numbers = []
    for count in range(size):
        numbers.append(random.randint(1, 10000))
    return numbers

print(random_list(10))
```

Ten numbers, and a different ten each time you run it.

Next, the racers. Your toolkit's `selection_sort` and `insertion_sort`
give back a sorted list, but they do not count. So here they are again,
line for line, with a counter added, as on the last page. Each gives
back the number of comparisons it made.

```python exec
id: racing-lists-2
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
```

```python exec
id: racing-lists-3
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
            comparisons = comparisons + 1    # the one that found a smaller item
        items[i] = item
    return comparisons
```

## Ten, a hundred, a thousand

Now the race. The cell makes one random list of each size, and gives
the same list to both sorts, so that each race is fair. Selection sort
makes $\frac{n(n-1)}{2}$ comparisons on $n$ values, whatever their
order. So you can work out its column before you run the cell. What do
you guess for insertion sort?

```python exec
id: racing-ten-1
for size in [10, 100, 1000]:
    numbers = random_list(size)
    print(size, selection_count(numbers), insertion_count(numbers))
```

Selection sort makes 45, 4,950 and 499,500 comparisons, the same every
time you run the cell. Insertion sort's counts change from run to run,
because the lists are random, but they stay close to 25, 2,500 and
250,000.

Insertion sort makes about half as many comparisons as selection sort.
On a random list, each new value slides about half way along the
sorted part before it finds its place. Selection sort always looks at
all of the rest.

Now look down each column. The list gets 10 times longer, and the
count gets about 100 times bigger. Why 100? Each of the $n$ values is
compared with a share of the other $n$ values, so the count grows like
$n \times n$, or $n^2$. Ten times the values means $10^2 = 100$ times
the comparisons.

```question
id: racing-ten-2
type: multiple-choice
correct: 3

A list of 1,000 random values takes insertion sort about 250,000
comparisons. About how many would a list of 2,000 take?

- 500,000
- 250,002
- 1,000,000
```

## A picture of the race

A table with three rows hides the shape. Let's count at ten sizes, from
100 to 1,000, and draw the counts. This cell makes about three million
comparisons, so give it a few seconds. Before you run it, guess the
shape of each line: straight, like linear search on
[Finding things fast](tutorial:finding-things-fast#watching-the-steps-grow),
or something else?

```python exec
id: racing-picture-1
import matplotlib.pyplot as plt

sizes = list(range(100, 1001, 100))
selection_counts = []
insertion_counts = []
for size in sizes:
    numbers = random_list(size)
    selection_counts.append(selection_count(numbers))
    insertion_counts.append(insertion_count(numbers))

plt.plot(sizes, selection_counts, marker="o", label="selection sort")
plt.plot(sizes, insertion_counts, marker="o", label="insertion sort")
plt.xlabel("values in the list")
plt.ylabel("comparisons")
plt.legend()
```

Both lines curve upwards, steeper as they go. Each 100 new values add
more comparisons than the 100 before, because each new value has more
values to be compared with.

Growth like this, where the count grows with the square of the size, is
called *quadratic* growth. In the notation from Finding things fast,
programmers write it $O(n^2)$. For 1,000 values it is fine: a computer
makes half a million comparisons in well under a second. For a million
values, it is about half a million million comparisons, and that takes
hours.

## A list that is nearly in order

Random lists are a fair track. But real lists are often not random.
Here is one from
[A row of numbers](tutorial:a-row-of-numbers#a-real-list-ireland-since-1950):
life expectancy in Ireland, in years, for every year from 1950 to 2016.
The cell takes the `life_expectancy` column for Ireland as a list.

It mostly goes up, year after year, with a few small dips. So the list
is nearly in order already. Before you run the cell, which sort do you
think this suits?

```python exec
id: racing-nearly-1
df = await load_csv("life-expectancy.csv")
ireland = df[df.country == "Ireland"]["life_expectancy"].tolist()

print(len(ireland), "years")
print(ireland[:6])
print("selection sort:", selection_count(ireland))
print("insertion sort:", insertion_count(ireland))
```

There are 67 years. Selection sort makes 2,211 comparisons, which is
$\frac{67 \times 66}{2}$: it cannot tell that the list is nearly
sorted. Insertion sort makes only 86. Each value only needs to slide
back a step or two, past a dip, and most values do not move at all.

Lists like this are common: a leaderboard sorted yesterday, with three
new scores at the end, is nearly in order too.

## Shell sort: long jumps first

Insertion sort is slow on a random list because a value moves only one
place for each comparison. A small value near the end has a long way
to walk.

In 1959, Donald Shell found a way round this. First, sort values that
are far apart. Take every 4th value, say, and insertion sort only those.
A small value can then jump 4 places with one comparison. Then do the
same for every 2nd value, and at last for every value, with an ordinary
insertion sort. By the last pass, the list is nearly in order, and the
last section showed what insertion sort does with a list like that.

The distance between the values sorted together is the *gap*. *Shell
sort* is insertion sort done again and again, first with a large gap
and then with smaller ones, ending with a gap of 1. Here, the gap
starts at half the length of the list, and halves each pass.

Here is Shell sort on a hand of 8 cards in reverse order, the worst
case for insertion sort. Before you run it, what will the hand look
like after the gap-4 pass?

```python exec
id: racing-shell-1
def shell_steps(values):
    """Shell sort a copy of values, showing the list after each gap."""
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
        print("gap", gap, ":", items)
        gap = gap // 2
    return items

print(shell_steps([13, 12, 9, 8, 7, 5, 3, 1]))
```

If the inner `while` loop is hard to follow, compare it line by line
with `insertion_steps` on the last page: inside the gap loop, each step
of 1 has become a step of `gap`. Or run the cell and read the printed lines first, then
come back to the code.

With a gap of 4, the pairs 4 places apart are sorted: 13 and 7, 12
and 5, 9 and 3, 8 and 1. Every small card jumped 4 places towards the
front in one move. With a gap of 2, each card jumps 2 places. The last
pass, with a gap of 1, only has to swap neighbours.

```question
id: racing-shell-2
type: fill-in-the-blank

For a list of 1,000 values, the gaps start at 1000 // 2 = 500, and
halve: 500, 250, 125, 62, 31, 15, 7, 3 and {1}.
```

## A tool for your toolkit

Shell sort goes in your toolkit beside the other two, with the same
kind of promise. Here it is as a stub. Start from `shell_steps` above:
keep everything except the `print` line.

```python exec
id: racing-toolkit
toolkit: yes
def shell_sort(values):
    """Return a new list with the items of values in ascending order,
    found by Shell sort. values itself is not changed.

    The gap between the items compared starts at half the length and
    halves each pass, ending with an ordinary insertion sort.
    The items must be comparable with <, like numbers or words.
    """
    ...
```

```python toolkit-reference
for: racing-toolkit
def shell_sort(values):
    """Return a new list with the items of values in ascending order,
    found by Shell sort. values itself is not changed.

    The gap between the items compared starts at half the length and
    halves each pass, ending with an ordinary insertion sort.
    The items must be comparable with <, like numbers or words.
    """
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
        gap = gap // 2
    return items
```

The tests are the ones the last page used for your other two sorts,
with one more: all three sorts must agree on the same random list.
Until `shell_sort` is written, this cell stops with an error.

```python exec
id: racing-toolkit-tests
hand = [13, 12, 9, 8, 7, 5, 3, 1]
assert shell_sort(hand) == [1, 3, 5, 7, 8, 9, 12, 13]
assert hand == [13, 12, 9, 8, 7, 5, 3, 1], "the original must not change"
assert shell_sort([]) == []
assert shell_sort([5]) == [5]
assert shell_sort([4, 1, 4, 1]) == [1, 1, 4, 4]
assert shell_sort(["Oisín", "Aoife", "Kwame"]) == ["Aoife", "Kwame", "Oisín"]
for test_number in range(200):
    numbers = random_list(random.randint(0, 50))
    assert shell_sort(numbers) == sorted(numbers), numbers
numbers = random_list(1000)
assert shell_sort(numbers) == insertion_sort(numbers) == selection_sort(numbers)
print("shell_sort keeps its promise.")
```

```hint
Which test does the error point at? Try `print(shell_sort([3, 1, 2]))`
on its own. `None` means the function has no `return` yet.
```

```hint
after: 12 errors
title: some steps
1. Copy the body of `shell_steps`, from `items = values.copy()` down to
   `return items`, into `shell_sort`, under the docstring.
2. Take out the line that starts with `print`.
3. Check that `gap = gap // 2` sits inside the `while gap > 0:` loop,
   but outside the `for` loop.

**Think about:** what would happen if `gap = gap // 2` were left out?
```

<details class="dl-answer"><summary>answer</summary>

Here is one way to write it. Yours may differ and still keep the
promise: the tests are the judge.

```python
def shell_sort(values):
    """Return a new list with the items of values in ascending order,
    found by Shell sort. values itself is not changed.

    The gap between the items compared starts at half the length and
    halves each pass, ending with an ordinary insertion sort.
    The items must be comparable with <, like numbers or words.
    """
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
        gap = gap // 2
    return items
```

</details>

If you have not written `shell_sort` yet, open the answer above and
copy it into the stub. The rest of the page uses it.

Now Shell sort joins the race. Here is its counter, with the same two
counting lines as `insertion_count`. Guess its count for 1,000 random
values: nearer 250,000, or nearer 1,000?

```python exec
id: racing-toolkit-count
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

numbers = random_list(1000)
print(selection_count(numbers), insertion_count(numbers), shell_count(numbers))
print("Ireland:", shell_count(ireland))
```

On 1,000 random values, Shell sort makes about 15,000 comparisons,
where insertion sort made about 250,000. That is about 16 times fewer,
and the difference grows as the lists get longer.

On Ireland's nearly sorted list, though, Shell sort makes 356
comparisons, and insertion sort made 86. The long jumps are work that
a nearly sorted list did not need. No sort wins every race.

## The fourth racer: sorted()

Python's own `sorted()` is the last racer. It is not our code, so we
cannot put a counter inside it. We time it with a clock instead.

`time.perf_counter()` gives the time, in seconds, on a clock inside
the computer. Read it before a job and again after it, and the
difference is how long the job took. The cell below times all four
sorts on the same 1,000 random values, and shows each time in
milliseconds, thousandths of a second. Which do you think wins, and by
how much?

```python exec
id: racing-sorted-1
import time

numbers = random_list(1000)
for racer in [selection_sort, insertion_sort, shell_sort, sorted]:
    start = time.perf_counter()
    racer(numbers)
    seconds = time.perf_counter() - start
    print(racer.__name__, round(seconds * 1000, 2), "ms")
```

Your times will differ from anyone else's, and from run to run.
(`racer.__name__` is the name each function was given when it was
made.) Two things usually hold, though.

First, `sorted()` is far ahead of all three: often more than ten times
faster than Shell sort, and more than a hundred times faster than
selection sort.

Second, and this may surprise you, insertion sort is not twice as fast
as selection sort, although it made half as many comparisons. It is
often a little slower. Each time insertion sort compares, it also moves
a value one place, and moving takes time too. Selection sort moves a
value only once per round. A count only counts what we chose to count.

Here is the honest reason `sorted()` wins. It uses a cleverer method,
called Timsort, which needs about 8,600 comparisons for 1,000 random
numbers. And it is written in the language C, so it runs as the
computer's own instructions, not as lines of Python read one at a time.

<aside class="dl-note" id="racing-note-timsort">

**Tim's sort.** Timsort is named after Tim Peters, who wrote it for
Python in 2002. It worked so well on real data that Java adopted it
too, for sorting lists of objects.

</aside>

That is not a reason to stop writing sorts of your own. Timsort is
built from the ideas on these pages: inside it, short pieces of the
list are sorted by insertion sort, because insertion sort is quick on
short lists and nearly sorted ones.

## Six thousand planets

Now the list from the top of the page. The file holds NASA's list of
planets as it was on 25 September 2026. For each planet, `orbit_days`
is the length of its year: how many of our days it takes to go once
round its star. A few planets have no value for this, and `.dropna()`
leaves those out. It keeps only the rows that have a number.

Before you run anything, use the formula. How many comparisons would
selection sort make on this list?

```python exec
id: racing-planets-1
df = await load_csv("exoplanets.csv")
planet_days = df["orbit_days"].dropna().tolist()
size = len(planet_days)
print(size, "planets with a known year")
print(size * (size - 1) // 2, "comparisons for selection sort")
```

There are 6,019 planets with a known year, and selection sort would
make 18,111,171 comparisons; insertion sort, about nine million. Each
could keep you waiting a long time. The formula told us the cost
before we paid it, so we race only the two we can wait for. Guess
Shell sort's count first: nearer nine million, or a hundred thousand?

```python exec
id: racing-planets-2
print(shell_count(planet_days), "comparisons for Shell sort")

start = time.perf_counter()
planets_in_order = sorted(planet_days)
print(round((time.perf_counter() - start) * 1000, 2), "ms for sorted()")

print("shortest year:", planets_in_order[0], "days")
print("longest year:", planets_in_order[-1], "days")
```

Shell sort makes 148,266 comparisons, about sixty times fewer than
insertion sort would. `sorted()` takes a few milliseconds.

And look at the two ends. The shortest year is 0.090706 days, about 2
hours and 11 minutes: a planet called PSR J1719-1438 b, which goes
round a dead star in about the time a long film lasts. The longest is
402,000,000 days, which is about 1.1 million of our years. That planet,
COCONUTS-2 b, is so far from its star that in the 300,000 years or so
since the first people of our kind lived, it has gone less than a
third of the way round. The two years are more than four billion times
apart, and one sort puts them at the two ends of the same list.

## Which sort, where?

An algorithm is chosen for the job it is doing, not only for its
speed on one track. Here is what the races found.

| Sort | Comparisons, $n$ random values | Where it fits |
|---|---|---|
| selection sort | $\frac{n(n-1)}{2}$, always | where moving a value is costly: it makes at most $n - 1$ swaps |
| insertion sort | about $\frac{n^2}{4}$; about $n$ if nearly in order | short lists, and lists that are nearly in order |
| Shell sort | far fewer than $n^2$ | small devices, where the code must be short and there is little memory to spare |
| `sorted()` | about 8,600 for 1,000 values | almost everywhere else in Python |

```question
id: racing-where-1
type: multiple-choice
correct: 2

A catalogue keeps 6,000 planets in order of their distance. Each week,
five new planets are added at the end. Which sort of ours does the
least work on the new list?

- selection sort, because it always does the same work
- insertion sort, because the list is nearly in order
- Shell sort, because it is fastest on random lists
```

### Your turn

1. Race all three of our sorts on a list that is already in order:
   `list(range(1000))`. Before you run it, predict each count.
2. Now race them on the same list in reverse order,
   `list(range(1000, 0, -1))`. Which sort is hurt most?
3. Add a line that times `sorted()` on `ireland`.

```python exec
id: racing-where-your-turn
in_order = list(range(1000))
print(selection_count(in_order), insertion_count(in_order), shell_count(in_order))
```

<details class="dl-why"><summary>Why this way?</summary>

This page measured the growth of each sort on random lists, and met
real lists, Ireland's and the planets', only after that. Racing on real
data from the start, the lists a program meets at work, was the other
choice.

Real data is the honest test of a program in use. It is often nearly
in order, as Ireland's list was, and a sort that looks slow on random
lists can win there. Benchmarks used in industry are usually built
from real data for this reason.

We started with random lists because they favour no sort, and because
a random list of any size is one line away. They showed the shape of
the growth at 10, 100 and 1,000 values. But the Ireland race showed
what that choice hides: the track decides the winner. When someone tells you one method
is faster, ask what it was raced on.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the racers, as functions we can pass to a loop; `comparisons`, a counter inside each sort; the gap |
| What is promised? | all three sorts promise the same sorted list, and the tests check that they agree; `time.perf_counter()` promises a clock reading |
| What happens when? | Shell sort sorts far-apart values first, then nearer ones; the order a list starts in changes insertion sort's work |
| What does this space let us do? | a random list favours no sort; a nearly sorted list favours insertion sort; C runs faster than Python lines |

## What we have now

| Term or tool | What it means |
|---|---|
| quadratic growth, $O(n^2)$ | the count grows with the square of the size: 10 times the values, 100 times the work |
| gap | the distance between the values Shell sort compares |
| Shell sort | insertion sort with a large gap first, then smaller gaps, ending with a gap of 1 |
| `shell_sort(values)` | your new toolkit tool: a new sorted list, found by Shell sort |
| `.dropna()` | keeps only the values in a column that are there, and leaves out the empty cells |
| `time.perf_counter()` | a clock reading, in seconds; the difference of two readings is how long a job took |
| Timsort | the method inside Python's `sorted()` |
| choosing an algorithm | pick the one that fits the job: the list's length, its starting order, and what is costly |

The practice page is next. After it,
[A function that calls itself](tutorial:a-function-that-calls-itself)
counts every file in a folder, however deep the folders go.

For another route through the same sorts, with Shell sort as an
optional challenge, the integrated course has
[Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order).
