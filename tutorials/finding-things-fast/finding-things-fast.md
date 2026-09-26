---
title: "Finding things fast: linear and binary search"
year: "2026-2027"
version: 2026.09.25.1
datasets: [exoplanets]
covers:
  one-contact-at-a-time:
    covers: [MIT-6.8]
    touches: [MIT-6.7]
  counting-the-looks:
    covers: [MIT-6.8]
  the-guessing-game:
    covers: [MIT-6.6]
  binary-search-halve-what-is-left:
    covers: [MIT-6.8, MIT-6.6]
  only-in-a-sorted-list:
    covers: [MIT-6.8]
  how-many-halvings:
    covers: [MIT-1.1]
  watching-the-steps-grow:
    covers: [MIT-6.8]
    touches: [MIT-1.1]
  two-tools-for-your-toolkit:
    touches: [MIT-6.8, PDP-LO8, PDP-LO10]
---

# Finding things fast: linear and binary search

Astronomers have found more than six thousand planets that go round
other stars. NASA keeps a list of them, and a computer can find any one
planet on that list in about a dozen looks. Your phone does the same
trick with its contacts: you type "Niamh", and her number is there
before you finish.

If everyone on Earth were on one list,
about 8 billion names, the same trick would find any one of them in 33
looks. How can so few looks be enough? And what does the list have to
be like for the trick to work?

On this page we:

- look for a name by checking one item after another: linear search
- count the looks with a counter inside the loop
- play a guessing game, and turn its trick into binary search
- search NASA's list of planets both ways
- find out which lists binary search works on, and which it does not
- meet logarithms again, as "how many halvings"
- plot the number of looks as the list grows
- add `linear_search` and `binary_search` to the toolkit

> **The space we're in.** We work with lists, with indexes that start
> at 0, as on [A row of numbers](tutorial:a-row-of-numbers). We usually
> do not say it, but a computer looks at one item of a list at a time, and
> "finding" means looking and comparing, again and again. It does not
> see the whole list at once, the way your eye takes in a short
> list of eight names. Whether the list is *in order* decides which
> moves are allowed, and this page asks that question again and
> again.

## Warm-up

Two questions from earlier pages. The first is from
[A row of numbers](tutorial:a-row-of-numbers#counting-from-0), and the
second from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times).

```question
id: finding-fast-warm-up-1
type: fill-in-the-blank

`days = ["Mon", "Tue", "Wed", "Thu", "Fri"]`. Then `days[2]` is
{"Wed"|"Tue"|"Thu"}, and the last index of `days` is {4}.
```

```question
id: finding-fast-warm-up-2
type: multiple-choice
answer: 3

$\log_2 32$ asks how many times we multiply by 2, starting from 1, to
reach 32. What is it?

- 2
  - This is 32 divided by 16, or the number of digits in 32.
- 4
  - 2 × 2 × 2 × 2 is 16, one doubling short.
- 5
  - Doubling from 1: 2, 4, 8, 16, 32 is five doublings.
- 16
  - This is 32 divided by 2, once.
```

## One contact at a time

Here are eight contacts, in the order they were added to a phone. The
phone has not put them in any order. How would you find Niamh? Most
people would read from the top until they reach her.

A *search* is a way of finding where a value,
the *target*, sits in a list. A *linear search* looks at each item in
turn, from the front, until it finds the target or runs out of items.
"Linear" means "in a line". It goes along the list one step at a time.

Before you run the cell, count: how many names will Python look at to
find Niamh?

```python exec
id: finding-fast-linear-1
contacts = ["Siobhán", "Tomasz", "Aoife", "Kwame", "Niamh", "Oisín", "Priya", "Liam"]


def find_contact(names, target):
    """Look at names from the front. Return target's index, or -1 if it is not there."""
    for i in range(len(names)):
        print("look at index", i, ":", names[i])
        if names[i] == target:
            return i
    return -1


print("Niamh is at index", find_contact(contacts, "Niamh"))
```

It takes five looks, and Niamh is at index 4. The loop runs by index,
as on [A row of numbers](tutorial:a-row-of-numbers#going-through-by-index).
When the names match, `return i` ends the whole function at once, so
the loop does not go on to Oisín.

What if the name is not there? Guess what this prints, and how many
looks it takes.

```python exec
id: finding-fast-linear-2
print("Zara is at index", find_contact(contacts, "Zara"))
```

It takes eight looks, one for every contact, and then the answer is
`-1`. The loop finished, so Python reached the last line, `return -1`.

Why −1? A search promises an index, and every real index is 0 or more.
So −1 cannot be mistaken for "found at the front", which 0 would mean.
Many languages use −1 for "not found" for that reason. But Python has
a trap here. On
[A row of numbers](tutorial:a-row-of-numbers#counting-from-the-end) we
saw that `contacts[-1]` is the last item, Liam. So a program that
forgets to check for −1 will quietly use Liam's number. In Python's
space, −1 is a real index. Always check the answer before you use it.

## Counting the looks

How long a search takes depends on how many times it looks. So let's
count. Here is the same search, with a counter in place of the
printing. The counter starts at 0 before the loop and goes up by 1
each time round, like a running total.

```python exec
id: finding-fast-count-1
def linear_looks(values, target):
    """Search values from the front for target. Return how many items were looked at."""
    looks = 0
    for i in range(len(values)):
        looks = looks + 1
        if values[i] == target:
            return looks
    return looks


print(linear_looks(contacts, "Siobhán"))
print(linear_looks(contacts, "Niamh"))
print(linear_looks(contacts, "Zara"))
```

Siobhán, at the front, takes one look. Niamh takes five. Zara, who is
not there, takes eight. The first is the *best case*, the fewest looks a
search can need. The last is the *worst case*, the most it can need.
For a linear search, the worst case is one look for every item: a
target at the very end, or not there at all.

With 8 contacts, 8 looks is nothing. With 2,000, it is 2,000. With a
million, it is a million. Double the list, and the worst case doubles too.

## The guessing game

Here is a game to play with someone. They think of a whole number from
1 to 100. You guess, and they say "higher", "lower" or "yes". How many
guesses do you need?

You could guess 1, then 2, then 3. That is a linear search, and it can
take 100 guesses. Most people find a better way. They start at 50. If they
say "higher", the number is from 51 to 100, and half the numbers are
gone with one guess. Guess 75, then 62 or 63, and so on. Each guess
removes half of what is left.

$$100 \to 50 \to 25 \to 12 \to 6 \to 3 \to 1$$

Each arrow is one guess that missed, and the numbers are how many are
still possible after it. After 6 missed guesses at most, only
one number is left, and the 7th guess is that number. That is seven
guesses, not 100.

This trick has a name. *Divide and conquer* is a way of solving a
problem by splitting it into smaller problems of the same kind, and
solving those: "find it in 1 to 100" becomes "find it in 51 to 100".

```question
id: finding-fast-game-1
type: multiple-choice
answer: 2

The guessing game works because "higher" or "lower" tells you which
half the number is in. What would change if your friend's numbers
were written on 100 cards, shuffled, and you guessed a card's position
instead?

- Nothing: guess the middle card, as before.
  - The middle card tells you nothing about where the others are, when they are shuffled.
- "Higher" and "lower" would say nothing about which half the card is in.
  - Shuffled cards have no order, so no answer rules out half of them.
- You would need exactly 100 guesses.
  - In the worst case you might need 100, but you would not always.
```

## Binary search: halve what is left

Now the same trick on the contacts. For it to work, the list must be
in order, so that "after the middle" means "later in the alphabet".
Python's `sorted()`, from
[What is typical?](tutorial:what-is-typical), returns a new list in
order. The next page,
[Sorting a hand of cards](tutorial:sorting-a-hand-of-cards), shows how
sorting works inside. For now we let Python do it.

Python compares two words with `<` letter by letter, the way a
dictionary does, so `"Aoife" < "Kwame"` is True.

A *binary search* finds a target in a sorted list by looking at the
middle item and removing the half the target cannot be in, again
and again. "Binary" means "in two". Each look splits what is left into
two halves. Here is the plan in pseudocode:

```text
SET low TO the first index, and high TO the last index
REPEAT while low is not past high:
    SET middle TO the index halfway between low and high
    IF the middle item is the target: give back middle
    IF the middle item comes before the target: SET low TO middle + 1
    OTHERWISE: SET high TO middle - 1
give back -1, because nothing is left to look at
```

`low` and `high` are the two ends of the part still worth looking at.
Before you run the cell, guess: how many looks will it need to find
Priya? Pause here and make the guess. I'll wait.

```python exec
id: finding-fast-binary-1
in_order = sorted(contacts)
print(in_order)


def binary_steps(sorted_values, target):
    """Binary search sorted_values for target, showing each look. Return its index, or -1."""
    low = 0
    high = len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        print("look at index", middle, ":", sorted_values[middle])
        if sorted_values[middle] == target:
            return middle
        if sorted_values[middle] < target:
            low = middle + 1     # the target comes later: keep the right half
        else:
            high = middle - 1    # the target comes earlier: keep the left half
    return -1


print("Priya is at index", binary_steps(in_order, "Priya"))
```

It takes two looks. The first look was at index 3, Niamh, halfway between 0 and
7. `(low + high) // 2` finds the middle, and `//` rounds down, as on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
Priya comes after Niamh, so the left half, Aoife to Niamh, was
skipped, and `low` became 4. The second look was halfway between 4 and 7,
at index 5, and that was Priya.

<img src="halving-the-contacts.svg" alt="The eight contacts in alphabetical order, Aoife to Tomasz, at indexes 0 to 7, drawn once for each look. Look 1: low is 0, high is 7, and the middle is index 3, Niamh. Niamh comes before Priya, so low becomes 4. Look 2: only indexes 4 to 7, Oisín to Tomasz, are still shaded. The middle is index 5, and that is Priya.">

Three names change at every look, and that is a lot to hold in your
head. If it feels like too much, take a pencil and write `low`, `high`
and `middle` as three columns, one row per look. The third step of the
Your turn below asks for exactly that.

<aside class="dl-note" id="finding-fast-note-overflow">

**A bug that hid for years.** In Java and C, a
whole number has a fixed size, and adding two very large ones can go
past the largest number the computer can hold. So `(low + high) / 2`
breaks once a list has more than about a billion items. Joshua Bloch
found this in the binary search in Java's own library, and wrote about
it in 2006. The same line is in Jon Bentley's well-known book
*Programming Pearls*, from 1986. Python's
whole numbers have no size limit, as on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#two-kinds-of-number-in-python),
so the line is safe here. The space we are in matters.

</aside>

### Your turn

1. Search for `"Aoife"`. Before you run it, which three names do you
   think it will look at?
2. Search for `"Zara"`, who is not there. How many looks does it take
   before it returns −1? Compare that with the 8 looks of the linear
   search.
3. Follow the values of `low` and `high` for the Zara search on paper,
   and find the moment `low` goes past `high`.

```python exec
id: finding-fast-binary-your-turn
print(binary_steps(in_order, "Aoife"))
```

Now a real list. NASA's Exoplanet Archive lists every *exoplanet*
known so far: a planet that goes round a star other than our Sun. The
file here is the list as it was on 25 September 2026. Each planet is
named after its star, with a small letter for the planet: Proxima Cen b
is the first planet found around Proxima Centauri, the star nearest to
the Sun.

The file lists the planets in no particular order. The cell sorts the
names, then searches for Proxima Cen b both ways. How many looks will
each search need? Guess before you run it.

```python exec
id: finding-fast-binary-2
df = await load_csv("exoplanets.csv")
planets = df["name"].tolist()
print(len(planets), "planets, on 25 September 2026")

planets_in_order = sorted(planets)
print("found at index", binary_steps(planets_in_order, "Proxima Cen b"))
print(linear_looks(planets, "Proxima Cen b"), "looks for a linear search")
```

There are 6,372 planets in this copy of the list. The binary search
took 11 looks, and the linear search took 4,915, because Proxima Cen b
happens to sit far down the file. I think that is surprising. The
binary search skipped thousands of planets it never needed to see.

<aside class="dl-note" id="finding-fast-note-planets">

**The first planets.** The oldest entries on the list were found in
1992, going round a dead star called a pulsar. The first planet found
around a star like the Sun was 51 Peg b, in 1995. Michel Mayor and
Didier Queloz, who found it, shared the Nobel Prize in Physics in 2019.
The list grows every week, so a copy fetched on another day holds more
planets.

</aside>

## Only in a sorted list

What if we forget to sort? Here is the binary search on the contacts as
they were added. Aoife is in the list, at index 2. What do you think
will happen?

```python exec
id: finding-fast-sorted-1
print(contacts)
print("Aoife is at index", binary_steps(contacts, "Aoife"))
```

It says −1, which means not there. There was no error message. It gave an answer
that is not true, calmly, like the oven converter on
[Does it work?](tutorial:does-it-work#code-that-runs-and-code-that-works).

Follow the looks. The first was Kwame. Aoife comes before Kwame in the
alphabet, so the search kept the left half: Siobhán, Tomasz and Aoife.
So far, Aoife is still in the part kept. The second look was Tomasz. Aoife comes before Tomasz
too, so the search skipped Tomasz and everything after him, and
Aoife went with them. In a sorted list, every name after Tomasz would
come later in the alphabet than Tomasz. In this list, that is not
true.

<img src="searching-unsorted-contacts.svg" alt="The contacts in the order they were added, Siobhán, Tomasz, Aoife, Kwame, Niamh, Oisín, Priya and Liam, drawn once for each look, with Aoife at index 2 in a dashed box. Look 1: the middle is index 3, Kwame. Aoife comes before Kwame, so high becomes 2, and indexes 0 to 2 are still shaded. Look 2: the middle is index 1, Tomasz. Aoife comes before Tomasz, so high becomes 0. Now only Siobhán is shaded, and Aoife is outside the shaded part. Look 3: the middle is index 0, Siobhán, and high becomes −1. Low is past high, so the search gives back −1.">

Binary search still keeps its promise, but only in one space: a
sorted list. There, "this item comes before the target" means "so does
everything to its left". In an unsorted list, one look says nothing
about the other items, and the only move that works is to look at all
of them.

That is why the promise belongs in the function's name and docstring:
`binary_search(sorted_values, target)`. It also tells us what a phone
does. Programs that hold many names usually keep them sorted, so that
they can halve, not read every name. Keeping a list sorted takes work
every time a name is added, and it is worth it when we search often.

```question
id: finding-fast-sorted-2
type: multiple-choice
answer: 3

Which of these lists is ready for a binary search?

- `[3, 9, 4, 12, 15]`
  - 12 comes after 4 but 9 before it: not in order.
- `["Cork", "Galway", "Athlone", "Dublin"]`
  - Athlone comes after Galway: not in alphabetical order.
- `[2, 5, 5, 8, 13, 21]`
  - Each number is at least as big as the one before it; a repeat is fine.
```

## How many halvings?

The guessing game took 7 guesses for 100 numbers. How many looks would
a binary search need for 1,000 names? We can count the halvings: keep
halving until one name is left, rounding down, as `//` does.

```python exec
id: finding-fast-halvings-1
import math

names_left = 1000
halving_count = 0
while names_left > 1:
    names_left = names_left // 2
    halving_count = halving_count + 1
    print(names_left)

print(halving_count, "halvings")
print(math.log2(1000))
```

Nine halvings take 1,000 down to 1: 500, 250, 125, 62, 31, 15, 7, 3, 1.
And `math.log2(1000)` is about 9.97.

On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times)
we met the logarithm as "how many times do I double to reach this
number?". Counting halvings asks the same question in
reverse. Doubling 1 about ten times reaches 1,000, so halving 1,000
about ten times reaches 1:

$$2^{10} = 1024 \quad \text{so} \quad \log_2 1000 \text{ is a little less than } 10$$

In words: the number of halvings that takes $n$ down to 1 is
$\log_2 n$, rounded down. A binary search makes one look for each
halving, and one more look at the last name left. So its worst case is
about $\log_2 n$ looks, one or two more at most.

| Names, $n$ | $\log_2 n$ | Worst case, linear | Worst case, binary |
|---|---|---|---|
| 1,000 | 9.97 | 1,000 | 10 |
| 1,000,000 | 19.9 | 1,000,000 | 20 |
| 8,000,000,000 | 32.9 | 8,000,000,000 | 33 |

The last row is everyone on Earth. With their names in order, 33 looks
would find anybody. This is the number from the top of the page, and I
think it is the most surprising number in this unit.

## Watching the steps grow

Let's check that table with our own counts, not with a formula. Here
is `binary_looks`, the binary search with a counter in place of the
printing. The cell then searches lists of 10, 100, 1,000, 10,000 and
100,000 items.

Only the length of the list changes the count, so we use quick lists
of even numbers in order, `range(0, 2 * size, 2)`. We search for
`2 * size`, which is bigger than every number in the list. That is the
worst case for both searches. Before you run it, guess the binary column.

```python exec
id: finding-fast-grow-1
def binary_looks(sorted_values, target):
    """Binary search sorted_values for target. Return how many items were looked at."""
    looks = 0
    low = 0
    high = len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        looks = looks + 1
        if sorted_values[middle] == target:
            return looks
        if sorted_values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return looks


sizes = [10, 100, 1000, 10000, 100000]
linear_counts = []
binary_counts = []
for size in sizes:
    numbers = list(range(0, 2 * size, 2))
    linear_counts.append(linear_looks(numbers, 2 * size))
    binary_counts.append(binary_looks(numbers, 2 * size))

print(linear_counts)
print(binary_counts)
```

The linear counts are 10, 100, 1,000, 10,000 and 100,000. They are the same as
the length every time. The binary counts are 4, 7, 10, 14 and 17, as
the table in the last section said. Each time the list gets 10 times
longer, the binary search needs only 3 or 4 more looks, because 10 is
between $2^3 = 8$ and $2^4 = 16$.

A picture makes the difference hard to miss. Guess the shape of each
line before you run it.

```python exec
id: finding-fast-grow-2
import matplotlib.pyplot as plt

plt.plot(sizes, linear_counts, marker="o", label="linear search")
plt.plot(sizes, binary_counts, marker="o", label="binary search")
plt.xlabel("items in the list")
plt.ylabel("looks, worst case")
plt.legend()
```

The linear line climbs straight up to 100,000. The binary line lies so
flat along the bottom that it looks like 0. It is not 0. It is 17,
which is too small to see on a scale that goes to 100,000.

The two lines have different shapes of growth. The linear count grows
*in proportion* to the list. Twice as many items need twice as many
looks. The binary count grows like the *logarithm* of the list. Twice
as many items need one more look. Programmers write these as $O(n)$ and
$O(\log n)$, said "order n" and "order log n". You will see those
names in books. On this course, we count.

### Your turn

1. Change `sizes` to `[1, 2, 4, 8, 16, 32, 64, 128]` and run both cells
   again. What happens to the binary count each time the size doubles?
2. Add 1,000,000 to the first list of sizes. Before you run it, how
   many looks do you expect in each column? (The linear search will
   take a second or two. It is making a million looks.)

## Two tools for your toolkit

Each search is a promise worth keeping. Here they are as stubs,
with their promises written. Both return an index, or −1 when the
target is not there.

1. For `linear_search`, start from `find_contact` at the top of the
   page, and delete the `print` line.
2. For `binary_search`, start from `binary_steps`, and delete the
   `print` line and the comment.

```python exec
id: finding-fast-toolkit
toolkit: yes
def linear_search(values, target):
    """Look through values from the front, and return the index of the
    first item equal to target, or -1 if no item is.

    values can be any list, in any order.
    """
    ...


def binary_search(sorted_values, target):
    """Return an index where target is in sorted_values, or -1 if it is
    not there, halving the part still to search at each look.

    sorted_values must be in order, smallest first. If target is there
    more than once, the index can be any one of them.
    """
    ...
```

```python toolkit-reference
for: finding-fast-toolkit
def linear_search(values, target):
    """Look through values from the front, and return the index of the
    first item equal to target, or -1 if no item is.

    values can be any list, in any order.
    """
    for i in range(len(values)):
        if values[i] == target:
            return i
    return -1


def binary_search(sorted_values, target):
    """Return an index where target is in sorted_values, or -1 if it is
    not there, halving the part still to search at each look.

    sorted_values must be in order, smallest first. If target is there
    more than once, the index can be any one of them.
    """
    low = 0
    high = len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        if sorted_values[middle] == target:
            return middle
        if sorted_values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1
```

The tests check the edges of each promise: the first item, the last
item, an empty list, and a target that is not there. The last test is
a long one. It searches for every item in lists of every length from 0
to 49, and for a number between each pair, which should never be
found. Until both tools are written, this cell stops with an error.

```python exec
id: finding-fast-toolkit-tests
assert linear_search(contacts, "Siobhán") == 0
assert linear_search(contacts, "Liam") == 7
assert linear_search(contacts, "Zara") == -1
assert linear_search([], "Zara") == -1
assert linear_search([4, 7, 4], 4) == 0          # the first one
assert binary_search(in_order, "Aoife") == 0
assert binary_search(in_order, "Tomasz") == 7
assert binary_search(in_order, "Zara") == -1
assert binary_search([], "Zara") == -1

for size in range(50):
    evens = list(range(0, 2 * size, 2))
    for i in range(size):
        assert binary_search(evens, evens[i]) == i
        assert binary_search(evens, evens[i] + 1) == -1
print("linear_search and binary_search keep their promises.")
```

```hint
Which test does the error point at? Try
`print(binary_search(in_order, "Aoife"))` on its own. `None` means the
function has no `return` yet.
```

```hint
after: 12 errors
title: some steps
1. Copy the body of `binary_steps`, from `low = 0` down to `return -1`,
   into `binary_search`.
2. Take out the line that starts with `print`.
3. Check that `return -1` sits outside the `while` loop, at the same
   level as `while`.

**Think about:** why must `return -1` wait until after the loop, and
not sit in an `else` inside it?
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too. Run the
tests to see what yours does.

```python
def linear_search(values, target):
    """Look through values from the front, and return the index of the
    first item equal to target, or -1 if no item is.

    values can be any list, in any order.
    """
    for i in range(len(values)):
        if values[i] == target:
            return i
    return -1


def binary_search(sorted_values, target):
    """Return an index where target is in sorted_values, or -1 if it is
    not there, halving the part still to search at each look.

    sorted_values must be in order, smallest first. If target is there
    more than once, the index can be any one of them.
    """
    low = 0
    high = len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        if sorted_values[middle] == target:
            return middle
        if sorted_values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1
```

</details>

Python has its own linear search. `contacts.index("Niamh")` gives 4,
and `"Niamh" in contacts` gives True. Both look through the list from
the front, one item at a time. `.index()` does not give −1 for a
missing item. It stops with a `ValueError`. That is a different promise
for the same search, and both are useful. You now know what both do
inside.

<details class="dl-why"><summary>Why this way?</summary>

This page measured each search by counting its looks. It never timed
one with a clock.

Timing is what a user feels, and it is what most programmers measure
first. It catches costs a count misses, such as a slow disk or a
list too big for memory. A later page in this unit times Python's own
sort for that reason.

We counted because a count stays the same on every computer, every
time you run it. A time changes with the machine, and with whatever
else the machine is doing, so two runs rarely agree. A count also
points at the cause. You can see that the binary search wins because
it looks fewer times, and you can see why it looks fewer times.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the target; `low`, `high` and `middle`, three indexes that mark the part still worth searching; −1, a value used as a name for "not found" |
| What is promised? | `linear_search` promises the first index of the target in any list; `binary_search` promises an index, but only for a sorted list |
| What happens when? | a linear search looks from the front, one item at a time; a binary search looks at the middle, then removes half, again and again |
| What does this space let us do? | in an unsorted list, only looking at everything works; in a sorted list, one look tells us about half the list; in Python, −1 is also a real index |

## What we have now

| Term or tool | What it means |
|---|---|
| search, target | finding where a value sits in a list; the value we are looking for |
| linear search | look at each item in turn, from the front |
| best case, worst case | the fewest looks a search can need; the most it can need |
| divide and conquer | split a problem into smaller problems of the same kind, and solve those |
| binary search | look at the middle of a sorted list, and remove the half the target cannot be in |
| `<` on words | compares letter by letter, the way a dictionary orders words |
| $\log_2 n$ as halvings | how many times $n$ can be halved before 1 is left: about the worst case of a binary search |
| in proportion, logarithmic | twice the items, twice the looks; twice the items, one more look |
| $O(n)$, $O(\log n)$ | how programmers write those two kinds of growth |
| `.index()`, `in` | Python's own linear searches on a list |
| exoplanet | a planet that goes round a star other than the Sun |
| `linear_search`, `binary_search` | your two new toolkit tools |

The practice page is next. After it,
[Sorting a hand of cards](tutorial:sorting-a-hand-of-cards) looks at
how a list gets into order in the first place, since binary search
needs one.

For another route through the same ideas, the integrated course has
[Searching a list: linear and binary search](tutorial:finding-things).

## Where to read more

Reducible (2020). *What Is Big O Notation?*
<https://www.youtube.com/watch?v=Q_1M2JaijjQ>. We counted how many looks
each search needs as the list grows. Big O notation is the name for that
way of counting. Reducible explains it with examples. About eighteen
minutes.
