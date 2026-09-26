---
title: "Sorting a hand of cards: selection and insertion sort — Practice"
practice_for: sorting-a-hand-of-cards
year: "2026-2027"
version: 2026.09.25.1
datasets: [exoplanets]
---

# Sorting a hand of cards: selection and insertion sort — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find the one
line in some code that does not do what its writer meant, and change
it. **Explain** means answer in words. **Another way** means reach the
same place by a second route. The answers are folded away until you
open them. Each one is one answer. Yours may be different and work too.

Your toolkit is loaded on this page: `selection_sort` and
`insertion_sort` from the tutorial, `linear_search` and `binary_search`
from the page before, and `smallest`, `median` and the rest from
earlier pages.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: sorting-hand-practice-warm-up
file_sizes = [34, 7, 61, 12]
print(selection_sort(file_sizes))
```

**1. Predict.** Four files in a folder are 34, 7, 61 and 12 kilobytes
(KB). After the cell above has run, what does `file_sizes` hold? And
what does `insertion_sort(file_sizes)[0]` give? Say both before you
check.

<details class="dl-answer"><summary>answer</summary>

`file_sizes` still holds `[34, 7, 61, 12]`, in the old order. Both
toolkit sorts promise a new list, and leave the one they are given
alone. `insertion_sort(file_sizes)[0]` is 7. Index 0 of the sorted list
is the smallest value, the smallest file.

</details>

**2. Predict.** You are dealt 6 cards. How many comparisons will
selection sort make to put them in order? And how many will insertion
sort make if the 6 cards are already in order? Find both before
you run anything.

<details class="dl-answer"><summary>answer</summary>

Selection sort always makes $\frac{n(n-1)}{2}$ comparisons, which for
6 cards is $\frac{6 \times 5}{2} = 15$: 5, then 4, 3, 2 and 1.
Insertion sort on a hand already in order makes one comparison for
each card after the first, so 5.

```python
cards = 6
print(cards * (cards - 1) // 2)
print(total(range(1, cards)))
print(cards - 1)
```

The second line checks the formula with `total` from
[Doing it again](tutorial:doing-it-again): $1 + 2 + 3 + 4 + 5 = 15$.

</details>

**3. Make.** TRAPPIST-1 is a small, cool star about 40 light-years
away, with seven planets roughly the size of the Earth. Here is how
many days each planet takes to go once round the star, in no order.
Sort the list, and print the three shortest orbits: the three planets
nearest the star.

```python
trappist_days = [6.10, 1.51, 12.35, 2.42, 18.77, 4.05, 9.21]
```

<details class="dl-answer"><summary>answer</summary>

```python
trappist_days = [6.10, 1.51, 12.35, 2.42, 18.77, 4.05, 9.21]
in_order = insertion_sort(trappist_days)
print(in_order[:3])
```

This prints `[1.51, 2.42, 4.05]`. Ascending order puts the shortest
orbit first, and a slice from
[A row of numbers](tutorial:a-row-of-numbers#a-slice-of-the-week)
takes the first three. `selection_sort` gives the same list. A year on
the nearest planet lasts a day and a half of ours.

</details>

**4. Explain.** What is the difference between `sorted(scores)` and
`scores.sort()`? Give one reason to use each.

<details class="dl-answer"><summary>answer</summary>

`sorted(scores)` returns a new list in order, and leaves `scores`
as it was. `scores.sort()` sorts `scores` itself, in place, and
returns `None`.

Use `sorted()` when the old order still matters: a playlist in the
order a friend made it, or log entries in the order they happened.
Use `.sort()` when nobody needs the old order and the list is very
long, so that a second copy would waste memory.

</details>

## Core

**5. Fix.** Eight sensors on a weather buoy report their battery
levels, in percent. The one with the lowest battery gets a new one
first. Schlomo, who is learning Python too, sorts the levels and takes
the first. This cell stops with an error. Run it, read the last line of
the error, then find the line that does something other than Schlomo
meant.

```python exec
id: sorting-hand-practice-fix-battery
battery = [42, 37, 45, 29, 40, 88, 51, 33]
ranking = battery.sort()
print("The lowest battery is at", ranking[0], "percent")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last line of the error mentions `'NoneType'`. Which name holds
   `None`?
2. Print `ranking` on its own. Then print `battery`.
3. What does `.sort()` return, and what does it change?

**Think about:** which of Python's two sorts returns a list.

</details>

<details class="dl-answer"><summary>answer</summary>

The last line is `TypeError: 'NoneType' object is not subscriptable`.
The code used `[0]` on `None`. `battery.sort()` sorted `battery` in
place and returned `None`, so `ranking` is `None`. Schlomo's plan, sort
and take the first, works. Either use the new list that `sorted()`
returns, or sort in place and then use `battery`:

```python
battery = [42, 37, 45, 29, 40, 88, 51, 33]
ranking = sorted(battery)
print("The lowest battery is at", ranking[0], "percent")
```

It prints 29.

</details>

**6. Predict.** Sort each list of file names with `insertion_sort`.
What order do you expect for each one? Run it to check.

```python exec
id: sorting-hand-practice-words
print(insertion_sort(["readme.txt", "notes.md", "app.py", "makefile"]))
print(insertion_sort(["readme.txt", "Notes.md", "app.py", "Makefile"]))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first list is all small letters, so it sorts the way a
   dictionary does.
2. In the second list, two words start with a capital letter.
3. On [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
   every letter is stored as a number. Try `ord("M")` and `ord("a")`.

**Think about:** what `<` is really comparing when it compares two
letters.

</details>

<details class="dl-answer"><summary>answer</summary>

The first list comes out as `['app.py', 'makefile', 'notes.md', 'readme.txt']`.
The second comes out as `['Makefile', 'Notes.md', 'app.py', 'readme.txt']`,
with both capitals first. Python compares letters by the numbers that
store them, and every capital letter has a smaller number than every
small letter: `ord("M")` is 77, and `ord("a")` is 97.

The sort is doing what it promised. It is a different space: "code
number order", not "dictionary order". Some file browsers list files
this way, capitals first, for the same reason. To get dictionary order,
make every word lower case before you sort, with `word.lower()`.

</details>

**7. Make.** Which five known planets are nearest to us? The cell
below loads two lists from NASA's list of planets, as it was on 25
September 2026, in the same order: the names, and each planet's
distance from the Sun in light-years. A *light-year* is the distance
light travels in a year, about 9.5 million million kilometres.

There are over six thousand planets, which is a lot for our sorts. The
next page shows why. So first keep only the planets nearer than 20
light-years, as a list of pairs, `(distance, name)`. Then sort the
pairs with one of your tools, and print the first five. Python
compares two pairs by their first values, and uses the second values
only if the first are equal. So pairs sort by distance.

```python exec
id: sorting-hand-practice-near
df = await load_csv("exoplanets.csv")
names = df["name"].tolist()
light_years = df["distance_ly"].tolist()
print(len(names), names[0], light_years[0])
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with an empty list, `pairs = []`.
2. Loop by index. When `light_years[i] < 20`, append
   `(light_years[i], names[i])`.
3. Sort `pairs` with one of your tools, and take the slice `[:5]`.

**Think about:** why the pair puts the distance first and the name
second.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
pairs = []
for i in range(len(names)):
    if light_years[i] < 20:
        pairs.append((light_years[i], names[i]))

print(len(pairs), "planets nearer than 20 light-years")
nearest = insertion_sort(pairs)
print(nearest[:5])
```

60 planets are nearer than 20 light-years. The nearest five are
Proxima Cen b and d, 4.2 light-years away, and Barnard b, c and d, 6.0
light-years away. They go round Proxima Centauri, the nearest star to
the Sun, and Barnard's Star, the nearest star that is not part of a
group of stars. Where two
distances are equal, the names settle the order, which is why b comes
before d.

The pair puts the distance first because that is what we want to sort
by. With the name first, the pairs would sort in alphabetical order. A
few planets have no distance in the file, and `nan < 20` is False, so
the loop leaves them out.

</details>

**8. Fix.** Schlomi, who is learning Python too, writes a selection
sort for the lengths of songs, in seconds. Her first line, `items =
values`, is meant to make a list of her own to work on. The function
returns a sorted list, as it promises. But it breaks the other half
of its promise. Run it, find what happens to `song_lengths`, and
change the line that causes it.

```python exec
id: sorting-hand-practice-fix-copy
def sort_lengths(values):
    """Return a new list with values in ascending order. values is not changed."""
    items = values
    for place in range(len(items) - 1):
        smallest_at = place
        for i in range(place + 1, len(items)):
            if items[i] < items[smallest_at]:
                smallest_at = i
        items[place], items[smallest_at] = items[smallest_at], items[place]
    return items


song_lengths = [241, 187, 305, 199]
print(sort_lengths(song_lengths))
print(song_lengths)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Compare the two printed lines. Which one should still be in the old
   order?
2. After `items = values`, how many lists are there, and how many
   names?
3. What did the tutorial's sorts write on their first line?

**Think about:** the difference between a second name and a second
list, on
[A row of numbers](tutorial:a-row-of-numbers#two-names-for-one-list).

</details>

<details class="dl-answer"><summary>answer</summary>

Both lines print `[187, 199, 241, 305]`. `items = values` ties a second
name to the same list, so every swap changes `song_lengths` too, and
the playlist's own order is lost. Schlomi wanted a list of her own,
as the tutorial did. That needs `.copy()`:

```python
def sort_lengths(values):
    """Return a new list with values in ascending order. values is not changed."""
    items = values.copy()
    for place in range(len(items) - 1):
        smallest_at = place
        for i in range(place + 1, len(items)):
            if items[i] < items[smallest_at]:
                smallest_at = i
        items[place], items[smallest_at] = items[smallest_at], items[place]
    return items


song_lengths = [241, 187, 305, 199]
print(sort_lengths(song_lengths))
print(song_lengths)
```

Now the second line prints `[241, 187, 305, 199]`, in the playlist's
order.

</details>

**9. Another way.** Selection sort finds the smallest of what is left,
again and again. Your toolkit already has `smallest`, and
`linear_search` can find where a value is. Write a selection sort built
from those two tools. You will need one new move: `remaining.pop(i)`
takes the item at index `i` out of the list `remaining`. Test it on a
list of exam marks.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Make `remaining` a copy of the list, and `result` an empty list.
2. While `remaining` still has items in it, find its smallest value,
   and append that value to `result`.
3. Find where that value is in `remaining`, and remove it with
   `.pop()`.

**Think about:** what `while len(remaining) > 0:` checks, and why the
loop must end.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def selection_sort_from_tools(values):
    """Return a new list with values in ascending order, using smallest and linear_search."""
    remaining = values.copy()
    result = []
    while len(remaining) > 0:
        lowest = smallest(remaining)
        result.append(lowest)
        remaining.pop(linear_search(remaining, lowest))
    return result


marks = [68, 45, 91, 72, 45, 83]
print(selection_sort_from_tools(marks))
print(selection_sort_from_tools(marks) == selection_sort(marks))
```

It prints `[45, 45, 68, 72, 83, 91]` and `True`. It is the same idea.
Each round selects the smallest of the rest. It builds a second list
instead of swapping inside one, and it lets two tools you already trust
do the looking. It still makes about $\frac{n(n-1)}{2}$
comparisons, because `smallest` looks at every item that is left.

</details>

**10. Predict.** The tools cell below counts comparisons, as the
tutorial did. A leaderboard of 100 scores is already in order, and one
new score is added at the end. Guess how many comparisons each sort
makes to put the board back in order. Then run the cell.

```python exec
id: sorting-hand-practice-counts
def selection_comparisons(values):
    """Selection sort a copy of values. Return how many comparisons it made."""
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


def insertion_comparisons(values):
    """Insertion sort a copy of values. Return how many comparisons it made."""
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


board = list(range(10, 1010, 10))
board.append(505)
print(len(board))
print(selection_comparisons(board), insertion_comparisons(board))
```

<details class="dl-answer"><summary>answer</summary>

The board has 101 scores. Selection sort makes 5,050 comparisons, which
is $\frac{101 \times 100}{2}$. That is the same as for any list of 101, because
it always looks at everything that is left. Insertion sort makes 150.
Each of the first 100 scores, after the very first, looks once to its
left and stays. That is 99. The new score, 505, slides left past the
50 scores above it, and one more comparison finds 500: $99 + 51 = 150$.

When a list is nearly in order, insertion sort does very little work.
That is why it is often the sort used for adding a few new items to a
list that is already sorted.

</details>

## Stretch

Use this cell for any of the stretch problems.

```python exec
id: sorting-hand-practice-stretch
import random

chip_temps = [62, 71, 58, 66, 80, 55, 69]
print(insertion_sort(chip_temps))
```

**11. Another way.** A third sort, *bubble sort*, goes along the list
comparing each pair of neighbours, and swaps them if they are in the
wrong order. One trip along the list is a *pass*. After one pass, the
largest value has "bubbled" to the end. After $n - 1$ passes, the list
is sorted. Write `bubble_sort(values)`, with the same promise as your
two tools, and check it against `sorted()` on random lists.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from a copy of `values`.
2. An outer loop makes the passes: `for trip in range(len(items) - 1):`.
3. An inner loop goes along the neighbours:
   `for i in range(len(items) - 1):`, comparing `items[i]` with
   `items[i + 1]`.
4. If `items[i] > items[i + 1]`, swap them.

**Think about:** after the first pass, is it worth comparing the last
pair again?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def bubble_sort(values):
    """Return a new list with values in ascending order, by bubble sort.

    values itself is not changed.
    """
    items = values.copy()
    for trip in range(len(items) - 1):
        for i in range(len(items) - 1):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return items


print(bubble_sort(chip_temps))
for test_number in range(200):
    numbers = []
    for count in range(random.randint(0, 20)):
        numbers.append(random.randint(0, 100))
    assert bubble_sort(numbers) == sorted(numbers), numbers
print("bubble_sort agrees with sorted() every time.")
```

This version compares every pair on every pass, so it makes
$(n - 1)^2$ comparisons, even more than selection sort. After pass
number `trip`, the last `trip + 1` values are already in place, so the
inner loop can stop at `len(items) - 1 - trip`, which reduces it to
$\frac{n(n-1)}{2}$.

</details>

**12. Explain.** The tutorial taught selection and insertion sort
first, starting from the way people sort cards, and left bubble sort
for this page. Many courses start with bubble sort. Which would you
have taught first, and why?

<details class="dl-answer"><summary>answer</summary>

There is more than one answer worth giving. Here are some things an
answer might weigh:

- **What the reader already knows.** Selection and insertion sort
  match what hands already do with cards, so each line of code has a
  move to match. Hardly anyone sorts cards by bubble sort, so it has to be
  learned as a new idea.
- **How short the code is.** Bubble sort has two plain loops and one
  swap of neighbours, with no `while` loop and no index kept by name.
  For a reader new to nested loops, that is less to hold in mind at once.
- **What comes next.** Insertion sort is used in real programs for
  short or nearly sorted lists, and it is part of shell sort on the
  next page. Bubble sort is mostly met in courses and exams.
- **What you want the reader to count.** All three make about
  $\frac{n^2}{2}$ comparisons in the worst case, so any of them can
  show why a better sort is worth having.

A full answer picks one, says who it is for, and says what the choice
costs.

</details>

**13. Make.** A laptop measured the temperature of its processor
chip once a minute for seven minutes, in degrees Celsius: the list
`chip_temps` in the cell above. The median
is the middle value when the values stand in a line, in order. Find it
with one of your sorts and an index, and check it against `median`
from your toolkit.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Sort the list with your toolkit.
2. With 7 values, the middle one has 3 values on each side. What is its
   index?
3. For any odd length, the middle index is `len(values) // 2`.

**Think about:** what you would do with an even number of values, where
there are two middle values.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
in_order = insertion_sort(chip_temps)
middle_temp = in_order[len(in_order) // 2]
print(in_order)
print(middle_temp, median(chip_temps))
```

The sorted list is `[55, 58, 62, 66, 69, 71, 80]`, and index
`7 // 2 = 3` holds 66. `median` agrees. With an even number of values,
the median is the mean of the two middle ones, as on
[What is typical?](tutorial:what-is-typical). Finding a median starts
with sorting, which is one reason sorting matters so much.

</details>

**14. Make.** A phone holds 1,000 numbers in no order. Is it worth
sorting them first, so that every search can be a binary search? Use
`insertion_comparisons` from problem 10 to count the cost of sorting
1,000 random numbers. A linear search for a number that is there looks
at about 500 items on average, and a binary search at about 10. After
how many searches has sorting paid for itself?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Make a list of 1,000 random numbers, and count the comparisons
   `insertion_comparisons` makes on it.
2. Each binary search saves about $500 - 10 = 490$ looks.
3. Divide the cost of sorting by the saving per search.

**Think about:** why the answer changes each time you run it, but only
a little.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
phone_numbers = []
for count in range(1000):
    phone_numbers.append(random.randint(800000000, 899999999))

sorting_cost = insertion_comparisons(phone_numbers)
print(sorting_cost)
print(round(sorting_cost / 490))
```

Sorting costs about 250,000 comparisons, a different number each run,
because the numbers are random. That is about $\frac{1000^2}{4}$, half
of insertion sort's worst case. Divided by a saving of 490 looks per
search, sorting pays for itself after about 510 searches.

So for a phone book you search once, sorting is not worth it. For one
you search every day, it is. The next page,
[Racing the sorts](tutorial:racing-the-sorts), races a faster sort,
and a faster sort makes the answer smaller.

</details>
