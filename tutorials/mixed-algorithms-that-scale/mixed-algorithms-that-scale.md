---
title: "Mixed problems: algorithms that scale"
practice_across:
  - finding-things-fast
  - sorting-a-hand-of-cards
  - racing-the-sorts
  - a-function-that-calls-itself
  - doubling-and-halving
year: "2026-2027"
version: 2026.09.25.1
---

# Mixed problems: algorithms that scale

Each problem here draws on at least one page of Unit 6, and many draw on
two or more. None of them is harder than what those pages covered. This
time, nobody tells you which page a problem comes from. You choose the
tool yourself, and that is part of the problem.

Along the way, the problems build this unit's product: a phone-book
search that stays fast. You will look up the same name three ways, in
books of 10, 1,000 and 100,000 names, count the steps each way takes,
and write a sentence on why one way hardly slows down at all. Problems
5, 6, 9, 13, 16 and 17 are the product's parts, and they build on each
other, so do those in order.

Your toolkit is loaded on this page: `linear_search`, `binary_search`,
`selection_sort`, `insertion_sort`, `shell_sort`, `count_items` and
`halvings` from this unit, and every tool from Units 1 to 5, such as
`total`, `mean` and `largest`. Each answer is hidden until you open it,
and each one is only one way. Yours may be different and work too. Where a
problem asks you to predict, make the prediction before you run
anything. It is the most useful part.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: mixed-scale-scratch-1
# Try things here
```

**1. Predict.** What does each line print?

```python
print(binary_search([2, 5, 8, 13, 21], 13))
print(linear_search(["Cork", "Galway", "Athlone"], "Athlone"))
print(binary_search(["Cork", "Galway", "Athlone"], "Athlone"))
```

<details class="dl-answer"><summary>answer</summary>

`3`, `2` and `-1`.

13 is at index 3 of a sorted list, so binary search finds it. The
linear search reads from the front and finds Athlone at index 2. The
last line gives an untrue answer, with no error, because the list is
not sorted. The
binary search looks at Galway first. Athlone comes before Galway in the
alphabet, so it stops looking at Galway and every name after it, and
it never sees Athlone. Binary search keeps its promise only in the space of
sorted lists, as on
[Finding things fast](tutorial:finding-things-fast#only-in-a-sorted-list).

</details>

**2. Predict.** What do these three lines print?

```python
print(halvings(1000))
print(halvings(1000000))
print(halvings(1000000) + 1)
```

<details class="dl-answer"><summary>answer</summary>

`9`, `19` and `20`.

$\log_2 1000$ is about 9.97, and $\log_2 1000000$ is about 19.93, and
`halvings` rounds down. The last line is the most looks a binary search
can need among a million names. It makes one look for each halving,
and one at the name that is left, as on
[Doubling and halving](tutorial:doubling-and-halving#why-binary-search-is-so-quick).

</details>

**3. Predict.** A phone keeps its contacts in groups, and a group can
hold another group. What does this print?

```python
groups = [["Aoife", "Tomasz"], ["Priya", ["Kwame", "Liam"]], []]
print(count_items(groups))
```

<details class="dl-answer"><summary>answer</summary>

`5`.

`count_items` counts the names at any depth, and a list inside counts
only for what it holds. Aoife and Tomasz make 2. The second group has
Priya, and a group inside it with 2 more, which makes 3. The empty group
adds nothing. It is the folder count from
[A function that calls itself](tutorial:a-function-that-calls-itself#counting-every-file).

</details>

**4. Explain.** A music app shows your 2,000 songs sorted by title. It
jumps to a title the moment you type it. But "show every song by this
artist" can take longer. Why might that be?

<details class="dl-answer"><summary>answer</summary>

The songs are sorted by title, so a search by title can halve the list
again and again: binary search, about 11 looks for 2,000 songs. They
are not sorted by artist. For binary search, "this song's artist comes
before the one I want" says nothing about the songs to its left, so the
only safe move is to look at every song: a linear search, 2,000 looks.

A list sorted by title makes one kind of question quick.
Apps that need both usually keep a second list, sorted by artist, beside
the first.

</details>

## Core

This cell makes phone books of any size, with made-up names. You do not
need to read how it works. You only need to know what it does. `make_phone_book(size)`
returns a list of `size` different names, in no order, like contacts
in the order they were added. A number after each name keeps every entry
different, the way a real phone book adds an address. The same size
always gives the same book, so your counts will match the answers.

```python exec
id: mixed-scale-book
import random

FIRST_NAMES = ["Aoife", "Ciarán", "Fatima", "Jack", "Kwame", "Lena", "Liam", "Mei",
               "Niamh", "Oisín", "Priya", "Rory", "Saoirse", "Tomasz", "Yusuf", "Zara"]
SURNAMES = ["Byrne", "Chen", "Doyle", "Kelly", "Kowalski", "Murphy",
            "Nowak", "O'Brien", "Okafor", "Ryan", "Silva", "Walsh"]


def make_phone_book(size):
    """Give back a list of size different made-up names, in no order.

    The same size always gives the same book.
    """
    maker = random.Random(size)    # a random maker that repeats itself for the same size
    book = []
    taken = set()
    while len(book) < size:
        name = maker.choice(SURNAMES) + ", " + maker.choice(FIRST_NAMES) + " " + str(maker.randint(1, 999))
        if name not in taken:
            taken.add(name)
            book.append(name)
    return book


print(make_phone_book(5))
```

A scratch cell for the core problems. Keep the product's functions in
it as you write them, so that later problems can use them.

```python exec
id: mixed-scale-scratch-2
# Your phone book search, problem by problem
```

**5. Make.** Binary search needs a sorted book, and on an unsorted
book it can give an untrue answer with no error. So the first part of the product is a check. Write
`is_in_order(values)`, which returns True when every value is less
than or equal to the one after it. Loop over the list by index. Test
it on `[]`, `[3]`, `[1, 2, 2, 5]` and `[2, 1]`, and then on a phone
book of 1,000 names before and after `sorted()`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over the indexes from 0 up to, but not including, the last
   one: `range(len(values) - 1)`.
2. Compare `values[i]` with `values[i + 1]`. If the first is bigger,
   the list is not in order, and you can `return False` at once.
3. If the loop ends without finding such a pair, `return True`.

**Think about:** why the loop stops one before the end. What would
`values[i + 1]` be on the last index?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def is_in_order(values):
    """Give back True when every value is less than or equal to the one after it."""
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            return False
    return True

assert is_in_order([])
assert is_in_order([3])
assert is_in_order([1, 2, 2, 5])
assert not is_in_order([2, 1])

book_1000 = make_phone_book(1000)
print(is_in_order(book_1000), is_in_order(sorted(book_1000)))
```

It prints `False True`. An empty list and a list of one value count as
in order, since no pair is in the wrong order. Equal neighbours are
allowed, which is why the test uses `>` and not `>=`. This loop by
index is the one from
[A row of numbers](tutorial:a-row-of-numbers#going-through-by-index).

</details>

**6. Make.** The first way to look a name up is linear search. Write
`linear_looks(book, name)`, which searches from the front and returns
how many names it looked at. Then, for books of 10, 1,000 and
100,000 names, count the looks for two names: the last name in the
book, and `"Zhang, Anna 1"`, who is not in any book.

<details class="dl-answer"><summary>answer</summary>

```python
def linear_looks(book, name):
    """Search book from the front for name. Give back how many names were looked at."""
    looks = 0
    for i in range(len(book)):
        looks = looks + 1
        if book[i] == name:
            return looks
    return looks

for size in [10, 1000, 100000]:
    book = make_phone_book(size)
    print(size, linear_looks(book, book[-1]), linear_looks(book, "Zhang, Anna 1"))
```

It prints `10 10 10`, `1000 1000 1000` and `100000 100000 100000`. A
name at the end, or a name that is not there, costs one look for every
name in the book. That is linear search's worst case, from
[Finding things fast](tutorial:finding-things-fast#counting-the-looks).
The 100,000 book takes a moment to make and to search.

</details>

**7. Fix.** Schlomo, who is learning Python too, wrote this binary
search. He made one change to the toolkit's version. `high` starts at
`len(sorted_values)`, since that is how many names there are. It finds
names in the middle of the book, but one search stops with an error.
Run it, read the last line of the error, and change the line that
causes it.

```python exec
id: mixed-scale-fix-high
def binary_search_again(sorted_values, target):
    """Give back an index where target is in sorted_values, or -1 if it is not there."""
    low = 0
    high = len(sorted_values)
    while low <= high:
        middle = (low + high) // 2
        if sorted_values[middle] == target:
            return middle
        if sorted_values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1

small_book = sorted(make_phone_book(10))
print(binary_search_again(small_book, small_book[4]))
print(binary_search_again(small_book, "Aaron, Adam 1"))
print(binary_search_again(small_book, "Zhang, Anna 1"))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The error is an `IndexError`. Which index is the last real one in a
   list of 10 names?
2. `"Zhang, Anna 1"` comes after every name. Follow `low` and `high` on
   paper: `low` keeps moving up. Where does `middle` end up?
3. Compare the first two lines of the function with `binary_search` on
   [Finding things fast](tutorial:finding-things-fast#two-tools-for-your-toolkit).

**Think about:** why did the search for `"Aaron, Adam 1"`, which comes
before every name, not fail?

</details>

<details class="dl-answer"><summary>answer</summary>

The first two searches print `4` and `-1`. The third stops with
`IndexError: list index out of range`. `high` starts at 10, one past the
last index, which is 9. A search for a name after every other name
keeps moving `low` up, until `middle` is 10, and there is no index 10.
Schlomo counted the names. The search needs the last index, which is
one less. That is the first line of the toolkit's version:

```python
    high = len(sorted_values) - 1
```

The search for Aaron never failed because it moves `high` down, away
from index 10. A search only in the middle of the book would never
have found this. Test at the edges of the promise, as on
[Does it work?](tutorial:does-it-work#code-that-runs-and-code-that-works).

</details>

**8. Predict.** Binary search needs a sorted book. How many comparisons
would the toolkit's `selection_sort` make to sort a book of 100,000
names? Use the formula from
[Sorting a hand of cards](tutorial:sorting-a-hand-of-cards#counting-the-comparisons),
and calculate it in one line of Python. Should we use it?

<details class="dl-answer"><summary>answer</summary>

```python
size = 100000
print(size * (size - 1) // 2)
```

4,999,950,000: about five billion comparisons. Selection sort makes
$\frac{n(n-1)}{2}$ comparisons on $n$ values, whatever their order. In
the browser's Python that would take hours. Python's `sorted()`, which
won the race on
[Racing the sorts](tutorial:racing-the-sorts#the-fourth-racer-sorted),
sorts 100,000 names in a fraction of a second, so the product uses
`sorted()` for the big book. It still helps to know what a sort costs.

</details>

**9. Make.** The second way is binary search. Write
`binary_looks(sorted_book, name)`, which returns how many names a
binary search looked at. For sorted books of 10, 1,000 and 100,000
names, count the looks for `"Zhang, Anna 1"`, and print
`halvings(size) + 1` beside each count.

<details class="dl-answer"><summary>answer</summary>

```python
def binary_looks(sorted_book, name):
    """Binary search sorted_book for name. Give back how many names were looked at."""
    low = 0
    high = len(sorted_book) - 1
    looks = 0
    while low <= high:
        middle = (low + high) // 2
        looks = looks + 1
        if sorted_book[middle] == name:
            return looks
        if sorted_book[middle] < name:
            low = middle + 1
        else:
            high = middle - 1
    return looks

for size in [10, 1000, 100000]:
    sorted_book = sorted(make_phone_book(size))
    assert is_in_order(sorted_book)
    print(size, binary_looks(sorted_book, "Zhang, Anna 1"), halvings(size) + 1)
```

It prints `10 4 4`, `1000 10 10` and `100000 17 17`. From 10 names to
100,000 names, ten thousand times as many, the looks go from 4 to only
17. The `assert` uses your check from problem 5, so a book that was
somehow not sorted would stop the cell rather than give a count that
means nothing.

</details>

**10. Another way.** On average, how many looks does a linear search
need to find a name that *is* in a book of 1,000 names? Find it two
ways: by searching for every name in the book and taking the `mean` of
the looks, and with the formula for $1 + 2 + \dots + n$ from
[Doing it again](tutorial:doing-it-again#sigma-a-loop-written-by-mathematicians).

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The name at index 0 takes 1 look, the name at index 1 takes 2, and
   the last name takes 1,000.
2. So the looks, over every name, are $1, 2, \dots, 1000$.
3. The average is their sum, divided by how many there are.

**Think about:** why the answer is about half the book, and not the
whole book.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
book_1000 = make_phone_book(1000)
every_count = []
for name in book_1000:
    every_count.append(linear_looks(book_1000, name))
print(mean(every_count))

n = 1000
print(n * (n + 1) / 2 / n)
```

Both give 500.5. The looks are 1, 2, 3 and so on up to 1,000, and their
sum is $\frac{n(n+1)}{2}$. Dividing by $n$ leaves $\frac{n + 1}{2}$. So
a linear search reads about half the book on average, which still grows
in proportion to the book. Twice the names means twice the looks. The loop
makes half a million looks in all, so it takes a moment.

</details>

**11. Explain.** Sorting a book costs work, and a linear search needs no
sorting. When is it worth sorting first? Think about two cases: you
search a book of 100,000 names once, and a phone searches its contacts
hundreds of times a day.

<details class="dl-answer"><summary>answer</summary>

For one search, it is not worth sorting first. A linear search costs at
most 100,000 looks. Even Python's `sorted()` needs far more comparisons
than that to sort 100,000 names, well over a million, and then the
binary search is 17 looks on top.

For many searches, it is worth it many times over. You sort once,
and every search after it costs 17 looks in place of up to 100,000.
After a few dozen searches, the sorted book is ahead, and it stays
ahead. A phone also keeps its contacts sorted as it goes. A new contact
added to a sorted list leaves it nearly in order, and insertion sort
does well on a list like that, as on
[Racing the sorts](tutorial:racing-the-sorts#which-sort-where).

The choice depends on the job, not only on which algorithm is fastest
in a race.

</details>

**12. Predict.** A company's list of customers doubles every year. It
starts with 1,000 names. After 10 years, how many names are there? How
many looks can a linear search need then, and how many can a binary
search need? Predict first, then check with `halvings`.

<details class="dl-answer"><summary>answer</summary>

```python
customers = 1000 * 2 ** 10
print(customers, halvings(customers) + 1)
```

1,024,000 names. A linear search can need 1,024,000 looks, a thousand
times more than at the start. A binary search can need 20, up from 10.
Each doubling of the list adds one halving, so ten doublings add ten
looks. The list grows exponentially, but the search grows steadily, one look
a year. These are the rumour and the phone book from
[Doubling and halving](tutorial:doubling-and-halving#why-binary-search-is-so-quick),
side by side.

</details>

## Stretch

A scratch cell for the stretch problems.

```python exec
id: mixed-scale-scratch-3
# Your working for problems 13 to 17
```

**13. Make.** The third way to look a name up is a set, from
[Collections without repeats](tutorial:collections-without-repeats#is-it-in-the-set).
A set does not look through its names one by one. It calculates where a
name would be from a short code made from the name, called a hash, so
it usually needs about one step whatever its size. We cannot count
those steps, since the code is not ours, so time all three ways instead,
as `sorted()` was timed on Racing the sorts.

Make a book of 100,000 names, a sorted copy, and a set of the same
names. Write three small functions, `by_linear(name)`, `by_binary(name)`
and `by_set(name)`, using `linear_search`, `binary_search` and `in`.
Then time each one, in milliseconds per lookup, on the last ten names of
the unsorted book.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `big_book = make_phone_book(100000)`, then `big_sorted = sorted(big_book)`
   and `big_set = set(big_book)`.
2. Each small function takes a name and returns one search's result:
   for example, `return name in big_set`.
3. Write `milliseconds_per_lookup(look_up, names)`, which reads
   `time.perf_counter()`, runs `look_up` on every name, reads the clock
   again, and divides the time by `len(names)`.
4. Binary search and the set are so fast that ten lookups may take
   less time than the clock can show. Give them `last_ten * 1000`, the
   ten names repeated a thousand times.

**Think about:** why the ten names at the end of the unsorted book are
the worst case for the linear search, but not for the other two.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import time

big_book = make_phone_book(100000)
big_sorted = sorted(big_book)
big_set = set(big_book)

def by_linear(name):
    """Look name up by linear search in the book as it was made."""
    return linear_search(big_book, name)

def by_binary(name):
    """Look name up by binary search in the sorted book."""
    return binary_search(big_sorted, name)

def by_set(name):
    """Look name up in the set of names."""
    return name in big_set

def milliseconds_per_lookup(look_up, names):
    """Run look_up on every name in names. Give back the average time in milliseconds."""
    start = time.perf_counter()
    for name in names:
        look_up(name)
    return (time.perf_counter() - start) * 1000 / len(names)

last_ten = big_book[-10:]
print("linear", milliseconds_per_lookup(by_linear, last_ten))
print("binary", milliseconds_per_lookup(by_binary, last_ten * 1000))
print("set   ", milliseconds_per_lookup(by_set, last_ten * 1000))
```

Your times will be different from anyone else's, and a little different
each run. The order is the same: the linear search takes several
milliseconds for each lookup, the binary search takes less than a
thousandth of that, and the set is faster again. The binary search is
our own Python, 17 looks at most. The set, like `sorted()`, runs as
the computer's own instructions, and it does not use halving at all.

</details>

<aside class="dl-note" id="mixed-algorithms-note-luhn">

**Buckets in 1953.** Early in 1953, Hans Peter Luhn, an engineer at
IBM, wrote a memo about putting records into "buckets", each chosen by
a number made from the record, so that a search could go straight to
the right bucket. It is one of the first descriptions of hashing. Luhn
also designed the check digit at the end of most bank card numbers,
which catches any single mistyped digit.

</aside>

**14. Another way.** Binary search has the shape of a promise that uses
itself, from
[A function that calls itself](tutorial:a-function-that-calls-itself#a-promise-that-uses-itself):
to search a part of the book, look at its middle, then search a part
half the size. Write `binary_looks_by_calls(sorted_book, name, low, high)`
with no loop, which returns the number of looks. Check that it agrees
with your `binary_looks` from problem 9 for every name in a sorted book
of 1,000, and for `"Zhang, Anna 1"`.

<details class="dl-answer"><summary>answer</summary>

```python
def binary_looks_by_calls(sorted_book, name, low, high):
    """Binary search sorted_book[low], ..., sorted_book[high] for name.
    Give back how many names were looked at.
    """
    if low > high:
        return 0                          # the base case: nothing left to look at
    middle = (low + high) // 2
    if sorted_book[middle] == name:
        return 1
    if sorted_book[middle] < name:
        return 1 + binary_looks_by_calls(sorted_book, name, middle + 1, high)
    return 1 + binary_looks_by_calls(sorted_book, name, low, middle - 1)

sorted_1000 = sorted(make_phone_book(1000))
last = len(sorted_1000) - 1
for name in sorted_1000 + ["Zhang, Anna 1"]:
    assert binary_looks_by_calls(sorted_1000, name, 0, last) == binary_looks(sorted_1000, name), name
print("The two versions agree.")
```

It prints `The two versions agree.` Each call makes one look, and hands
the rest to a call on half the part. The base case is an empty part,
where `low` has passed `high`, and it costs no looks. The calls go only
about 10 deep for 1,000 names, and 17 deep for 100,000, far from
Python's limit, because each one halves the problem.

</details>

**15. Fix.** Schlomi, who is learning Python too, wrote binary search
as a recursion, as on
[A function that calls itself](tutorial:a-function-that-calls-itself#a-promise-that-uses-itself).
It finds every name that is in the book, but a search for a missing
name stops with an error. Run it, read the last line of the error, and
add what is missing.

```python exec
id: mixed-scale-fix-base
def search_by_calls(sorted_book, name, low, high):
    """Give back an index where name is in sorted_book[low], ..., sorted_book[high], or -1."""
    middle = (low + high) // 2
    if sorted_book[middle] == name:
        return middle
    if sorted_book[middle] < name:
        return search_by_calls(sorted_book, name, middle + 1, high)
    return search_by_calls(sorted_book, name, low, middle - 1)

tiny_book = sorted(make_phone_book(10))
print(search_by_calls(tiny_book, tiny_book[7], 0, 9))
print(search_by_calls(tiny_book, "Kelly, Mei 500", 0, 9))
```

<details class="dl-answer"><summary>answer</summary>

The first search prints `7`. The second stops with
`RecursionError: maximum recursion depth exceeded`. The function has no
base case for a part with nothing left in it. Once `low` passes `high`,
it continues calling itself on empty parts, for ever, until Python stops
it, as on
[A function that calls itself](tutorial:a-function-that-calls-itself#where-the-promise-stops-the-base-case).
Schlomi's recursive cases do what she meant. It needs a base case at the top:

```python
    if low > high:
        return -1
```

With it, the missing name gives `-1`. The loop version has the same
check, as `while low <= high`. The loop's condition and the base case
are the same check, written two ways.

</details>

**16. Make.** Now put the product together. For books of 10, 1,000 and
100,000 names, find the worst case of each way: linear looks and binary
looks for `"Zhang, Anna 1"`, and 1 for the set, which the answer to
problem 13 explains. Print a table, one row for each size. Then plot the
linear and binary looks against the size of the book.

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

book_sizes = [10, 1000, 100000]
linear_worst = []
binary_worst = []
print("names", "linear", "binary", "set (about)")
for size in book_sizes:
    book = make_phone_book(size)
    sorted_book = sorted(book)
    linear_worst.append(linear_looks(book, "Zhang, Anna 1"))
    binary_worst.append(binary_looks(sorted_book, "Zhang, Anna 1"))
    print(size, linear_worst[-1], binary_worst[-1], 1)

plt.plot(book_sizes, linear_worst, marker="o", label="linear search")
plt.plot(book_sizes, binary_worst, marker="o", label="binary search")
plt.xlabel("names in the book")
plt.ylabel("looks, worst case")
plt.legend()
```

| Names | Linear | Binary | Set (about) |
|---|---|---|---|
| 10 | 10 | 4 | 1 |
| 1,000 | 1,000 | 10 | 1 |
| 100,000 | 100,000 | 17 | 1 |

The linear line climbs to 100,000. The binary line lies along the
bottom, at 17 or less. Our code does not count the set's 1. It is
what the set's design promises, most of the time, and the times in
problem 13 agree with it.

</details>

**17. Explain.** The last part of the product is the sentence on why.
In two or three sentences, say why binary search on the sorted book
stays fast as the book grows, using $2^k = n$ and $k = \log_2 n$. Say
what it needs to work.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may say it differently.

"Each look removes half of the names that are left, so the most
looks a binary search can need is the number of halvings that take $n$
names down to one, plus one: $k = \log_2 n$, rounded down, plus one.
Because $2^k = n$, doubling the book adds only one look, so 100,000
names need at most 17 looks where a linear search can need 100,000.
It only works if the book is sorted, so the book must be sorted once
and kept in order."

This answer names the halving, links it to $\log_2 n$, and says what
the space must be: a sorted book. The set is faster again, but by a
different trick, a hash, which a later course explains.

</details>
