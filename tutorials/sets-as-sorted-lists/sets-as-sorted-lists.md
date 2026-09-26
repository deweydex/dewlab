---
title: "Sets: building them from sorted lists"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  exoplanets: Planets around other stars, and the ways they were found.
  book-characters: The people in six novels, chapter by chapter.
  games-of-chance: Dice, cards and coins, and the games people play with them.
datasets: [dinosaur-finds, exoplanets, book-characters]
covers:
  making-a-set:
    covers: [MIT-2.1]
  membership-testing:
    covers: [MIT-2.1]
  set-operations-the-merge-pattern:
    covers: [MIT-2.2]
  set-language-and-notation:
    covers: [MIT-2.1]
  sets-in-the-worlds:
    covers: [MIT-2.2]
---

# Sets: building them from sorted lists

Two teams dig in the same valley. Each team writes down every dinosaur
bone it finds, one line for each bone. (The notebooks are made up. The
dinosaurs are real.)

```python exec
id: sets-two-digs
dig_one = ["Allosaurus", "Stegosaurus", "Allosaurus", "Diplodocus", "Stegosaurus", "Allosaurus"]
dig_two = ["Diplodocus", "Camarasaurus", "Allosaurus", "Diplodocus"]

print(len(dig_one) + len(dig_two), "lines in the two notebooks")
print(len(set(dig_one + dig_two)), "different dinosaurs")
```

```predict
type: number

The notebooks have 10 lines between them. How many different dinosaurs
did the two teams find?
```

Python's `set()` removed every repeat in one step. A *set* is a
collection of different elements, where the order does not matter and no
element appears twice. In maths we write a set inside curly brackets, so
$\{3, 1, 4, 1, 5\}$ is the same set as $\{1, 3, 4, 5\}$.

On this page we build our own sets, so you can see what `set()` does.
Sets give us a language for three kinds of question:

- **membership**: is Diplodocus in this set?
- **relationships**: which dinosaurs did both teams find?
- **operations**: what do we get when we put two sets together?

The rest of this series uses that language.
[Venn diagrams](tutorial:venn-diagrams) draws sets as circles.
[Logic](tutorial:logic-and-truth) finds the same rules in true and false.
And in probability, an *event*, such as "the dice show a double", is a
set of outcomes.

## Why sorted lists?

Python has its own `set` type. We build ours as sorted lists with no
repeats, for two reasons.

First, it uses algorithms we already know. Finding an element in a sorted
list is the binary search from
[Searching a list](tutorial:finding-things). Combining two sorted lists
uses a pattern called a merge, which we meet below.

Second, once you have built the operations yourself, you know what they
do. Python's `set` gives the same results. Inside, it uses a different
and faster method, called hashing.

## Making a set

The first job is to take a list that might have repeats, and might not be
in order, and make a sorted list with no repeats.

One way is to sort the list first. In a sorted list, any repeats sit next
to each other. Then we walk along the list and skip each item that
is the same as the one before it.

```text
SORT the items
CREATE an empty result list
FOR each item in the sorted items:
    IF result is empty OR item is different from the last item in result:
        APPEND item to result
RETURN result
```

Can you write `make_set(items)` from that plan?

```python exec
id: sets-make-set
def make_set(items):
    """Return a sorted list of the different items, with no repeats."""
    # Your code here


print(make_set(dig_one))
```

```inputs
make_set([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
make_set([1, 1, 1])
make_set([])
make_set(dig_one + dig_two)
```

```hint
`sorted(items)` gives a new list in order. Look at each item in turn,
and keep it only when it is different from the last item you kept. What
should happen with the very first item, when nothing has been kept yet?
```

```solution
def make_set(items):
    """Return a sorted list of the different items, with no repeats."""
    result = []
    for item in sorted(items):
        if len(result) == 0 or item != result[-1]:
            result.append(item)
    return result


print(make_set(dig_one))
---
Sorting puts repeats next to each other, so one comparison with the last
item kept is enough. `len(result) == 0` has to come first, because on an
empty list `result[-1]` would stop with an IndexError. And `or` never looks
at its right side when the left side is already true.
```

A set compares its elements exactly. What happens when one team writes
its dinosaurs with a small letter?

```python exec
id: sets-capitals
print(make_set(["stegosaurus", "Allosaurus", "Stegosaurus", "Allosaurus"]))
```

```predict
How many elements will this set have?

- 2
  - A set has no repeats, and stegosaurus is Stegosaurus, however it is written.
- 3
  - To Python, a small s and a capital S are different letters.
- 4
  - Nothing here is an exact repeat.
```

<details class="dl-answer"><summary>What it shows</summary>

Three: `['Allosaurus', 'Stegosaurus', 'stegosaurus']`. A small `s` and a
capital `S` are different letters, so the two spellings are different
elements. The capitals also come first, because Python sorts every capital
letter before every small one. Real data often has this problem. The usual fix
is to make the text match before it goes into a set, with `.lower()` or
`.title()`.

</details>

## Membership testing

Is a particular element in the set? Our sets are sorted, so a binary
search can answer quickly. The binary search on
[Searching a list](tutorial:finding-things) returned a position, or -1
when the item was missing. For a set we want a plain `True` or `False`.

Can you write `is_member(s, item)`, with a binary search?

```python exec
id: sets-is-member
def is_member(s, item):
    """Return True if item is in the sorted set s, and False if it is not."""
    # Your code here


found = ["Allosaurus", "Camarasaurus", "Diplodocus", "Stegosaurus"]
print(is_member(found, "Diplodocus"))
print(is_member(found, "Tyrannosaurus"))
```

```inputs
is_member(found, "Diplodocus")
is_member(found, "Tyrannosaurus")
is_member([], "Allosaurus")
is_member([1, 3, 5, 7], 7)
is_member([1, 3, 5, 7], 0)
```

```hint
Keep two positions, `low` and `high`, the first and last places the item
could be. Look at the item in the middle. If it is smaller than the one
you want, everything to its left is smaller too, so the search can move
`low` past it. When `low` passes `high`, there is nowhere left to look.
```

```solution
def is_member(s, item):
    """Return True if item is in the sorted set s, and False if it is not."""
    low = 0
    high = len(s) - 1
    while low <= high:
        middle = (low + high) // 2
        if s[middle] == item:
            return True
        if s[middle] < item:
            low = middle + 1
        else:
            high = middle - 1
    return False


found = ["Allosaurus", "Camarasaurus", "Diplodocus", "Stegosaurus"]
print(is_member(found, "Diplodocus"))
print(is_member(found, "Tyrannosaurus"))
---
It is the search from Searching a list, returning `True` where that
returned a position, and `False` where it returned -1. It works on words
as well as numbers, because Python can put words in order too.
```

```question
id: sets-how-many-looks
type: multiple-choice
answer: 1

A set has 1,000 elements. At most, about how many elements does
`is_member` look at before it can say an item is not there?

- About 10
  - Each look halves what is left: 1,000, 500, 250, and so on, down to 1.
- About 500
  - A search from the front needs half the set, on average.
- 1,000
  - A search from the front needs every element, to be sure.
```

## Set operations: the merge pattern

There are three main ways to combine two sets:

- The *union* of two sets holds every element that is in either set, or
  in both.
- The *intersection* holds only the elements that are in both sets.
- The *difference* of a and b holds the elements that are in a but not
  in b.

We can build all three with one pattern, the one merge sort uses. Merge
sort is a faster sort that combines two sorted lists into one, again and
again, and that combining step is called a *merge*.

Both of our sets are sorted. So we walk along both lists at the same
time, with two pointers. A *pointer* here is an index, `i` for set a
and `j` for set b, that marks our place in each list. At each step we
compare the two current elements:

- If they are equal, the element goes in the union and in the
  intersection. Both pointers move forward.
- If one is smaller, that element goes in the union, but not in the
  intersection. Its pointer moves forward.
- When one list ends, the rest of the other goes in the union.

We call this the *merge walk*. The picture shows it step by step.

![Five steps walking two sorted lists. Each step shows where both pointers
sit, the comparison that makes, and which pointer moves as a result. Then
what is left over in b, and the union they build.](merge-walk.svg)

Neither pointer ever goes backwards. So if set a has $n$ elements and set
b has $m$, there are at most $n + m$ steps. For two sets of 1,000
elements, that is at most 2,000 steps. Checking every element of a
against every element of b would take $n \times m$ steps, which is
1,000,000. The merge walk is an $O(n + m)$ algorithm.

Here is the merge walk written out for union.

```python exec
id: sets-union
def union(a, b):
    """Return a sorted list of the elements in a or b, or both."""
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
    # One list has run out. Everything left in the other one goes in.
    while i < len(a):
        result.append(a[i])
        i = i + 1
    while j < len(b):
        result.append(b[j])
        j = j + 1
    return result


a = [1, 3, 4, 5]
b = [1, 2, 5, 7, 8]
print("a:", a)
print("b:", b)
print("union:", union(a, b))
```

```predict
What will the last line print?

- union: [1, 2, 3, 4, 5, 7, 8]
  - Every element of either set, once each, in order.
- union: [1, 3, 4, 5, 1, 2, 5, 7, 8]
  - The two sets, one after the other.
- union: [1, 5]
  - The elements the two sets share.
```

Try changing the equal case so that it appends `a[i]` twice. What happens
to the union, and why?

<details class="dl-answer"><summary>What each part does</summary>

- The first `while` runs as long as both pointers are still inside their
  lists. Each time round it compares one element from each.
- The three cases are the three bullets above: equal, a's smaller, b's
  smaller. Each appends one element and moves at least one pointer.
- When one list ends, the last two loops copy what is left of the
  other. Only one of them does anything, because the list that ended has
  nothing left.

</details>

### Your turn

Using `union()` as your guide, can you write the other three? For each,
ask two questions: which elements do we keep when `a[i] == b[j]`, and
which when one is smaller?

The *symmetric difference* of a and b holds the elements that are in a or
in b, but not in both. The tasks use the two digs, as sets:

```python exec
id: sets-the-digs-as-sets
first_dig = ["Allosaurus", "Diplodocus", "Stegosaurus"]
second_dig = ["Allosaurus", "Camarasaurus", "Diplodocus"]
```

```python exec
id: sets-intersection
def intersection(a, b):
    """Return a sorted list of the elements in both a and b."""
    # Your code here


print(intersection(first_dig, second_dig))
```

```inputs
intersection([1, 3, 4, 5], [1, 2, 5, 7, 8])
intersection([1, 2, 3], [4, 5, 6])
intersection([], [1, 2])
intersection(first_dig, second_dig)
```

```hint
Only the equal case keeps anything. When one element is smaller, it
cannot be in both, so its pointer moves forward and nothing is kept.
When one list ends, is anything left that could be in both?
```

```solution
def intersection(a, b):
    """Return a sorted list of the elements in both a and b."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            i = i + 1
        else:
            j = j + 1
    return result


print(intersection(first_dig, second_dig))
---
It is the same walk as `union()`. Only the equal case appends, and
nothing is copied at the end. Once one list ends, nothing left in the
other can be in both.
```

```python exec
id: sets-difference
def difference(a, b):
    """Return a sorted list of the elements in a that are not in b."""
    # Your code here


print(difference(first_dig, second_dig))
```

```inputs
difference([1, 3, 4, 5], [1, 2, 5, 7, 8])
difference([1, 2, 5, 7, 8], [1, 3, 4, 5])
difference([1, 2, 3], [])
difference(first_dig, second_dig)
```

```hint
An element of a goes in when it is smaller than the current element of b,
because b has gone past it without finding it. What should happen to the
rest of a when b ends?
```

```solution
def difference(a, b):
    """Return a sorted list of the elements in a that are not in b."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            result.append(a[i])
            i = i + 1
        else:
            j = j + 1
    while i < len(a):
        result.append(a[i])
        i = i + 1
    return result


print(difference(first_dig, second_dig))
---
The loop at the end copies again, but only for a. Anything left in b when
a ends is not in a, so it cannot be in a's difference. The first two
inputs give different answers, because for difference the order of the
two sets matters.
```

```python exec
id: sets-symmetric-difference
def symmetric_difference(a, b):
    """Return a sorted list of the elements in exactly one of a and b."""
    # Your code here


print(symmetric_difference(first_dig, second_dig))
```

```inputs
symmetric_difference([1, 3, 4, 5], [1, 2, 5, 7, 8])
symmetric_difference([1, 2], [1, 2])
symmetric_difference(first_dig, second_dig)
```

```hint
Two ways work. It is the union's walk, except that the equal case keeps
nothing. Or it is built from functions you already have: what is in a
and not b, together with what is in b and not a.
```

```solution
def symmetric_difference(a, b):
    """Return a sorted list of the elements in exactly one of a and b."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            result.append(a[i])
            i = i + 1
        else:
            result.append(b[j])
            j = j + 1
    return result + a[i:] + b[j:]


print(symmetric_difference(first_dig, second_dig))
---
It is the union's walk, and the equal case keeps nothing. The last line
copies what is left of both lists at once. Only one of `a[i:]` and
`b[j:]` has anything in it. The other way is one line,
`union(difference(a, b), difference(b, a))`. It is easier to check, and
it walks the lists three times.
```

The four functions are connected, and the connections make good tests.
For any sets a and b:

- `symmetric_difference(a, b)` equals `difference(union(a, b), intersection(a, b))`
- `len(union(a, b))` equals `len(a) + len(b) - len(intersection(a, b))`

Look at the second one. To count the elements in the union, add the sizes
of the two sets, then subtract the elements they share, because they
were counted twice. In maths we write the size of a set $A$ as $|A|$:

$$|A \cup B| = |A| + |B| - |A \cap B|$$

This is the *inclusion-exclusion principle*. It appears again in
probability, where the chance of "A or B" subtracts the chance of both,
for the same reason.

```python exec
id: sets-check-the-connections
a = make_set([3, 1, 4, 1, 5, 9, 2, 6])
b = make_set([5, 7, 2, 8, 1, 8])
print(symmetric_difference(a, b) == difference(union(a, b), intersection(a, b)))
print(len(a), "+", len(b), "-", len(intersection(a, b)), "=", len(union(a, b)))
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
subset of", and others keep $\subset$ for a subset smaller than the whole
set, so check which one your book means. The *empty set* has no elements
at all.

Can you write `is_subset(a, b)`, using a function you already have?

```python exec
id: sets-is-subset
def is_subset(a, b):
    """Return True if every element of a is also in b."""
    # Your code here


print(is_subset(["Allosaurus"], second_dig))
print(is_subset(first_dig, second_dig))
```

```inputs
is_subset([1, 3], [1, 2, 3, 4])
is_subset([1, 5], [1, 2, 3, 4])
is_subset([], [1, 2])
is_subset([1, 2], [1, 2])
```

```hint
If every element of a is also in b, what is the intersection of a and b?
```

```solution
def is_subset(a, b):
    """Return True if every element of a is also in b."""
    return intersection(a, b) == a


print(is_subset(["Allosaurus"], second_dig))
print(is_subset(first_dig, second_dig))
---
When a is a subset of b, the intersection is all of a. The empty set is a
subset of every set, because its intersection with anything is empty,
which is itself. A merge walk of its own could stop at the first element
of a that b does not have. The one-line version says what a subset is.
```

Two sets are *equal* when each is a subset of the other. For our sorted
sets that is the same as `a == b`. Python's own sets keep no order, and
`==` on them checks the same thing.

## Sets in the worlds

Now the functions answer questions about real data. Choose a world at
the top of the page. Each one asks its own question, with the functions
you have written.

<div class="dl-world" data-world="dinosaurs">

The file `dinosaur-finds.csv` has one row for each dinosaur fossil find
in the Paleobiology Database, with the country it was found in. The
Jurassic ran from 201.4 to 145 million years ago, and the Cretaceous from
145 to 66. Which countries have fossils from both?

```python exec
id: sets-in-the-worlds--dinosaurs
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)

jurassic = finds[(finds.oldest_mya <= 201.4) & (finds.youngest_mya >= 145)]
cretaceous = finds[(finds.oldest_mya <= 145) & (finds.youngest_mya >= 66)]
jurassic_countries = make_set(jurassic["country_code"].tolist())
cretaceous_countries = make_set(cretaceous["country_code"].tolist())
print(len(jurassic_countries), "countries with Jurassic finds")
print(len(cretaceous_countries), "with Cretaceous finds")

# Which countries have both? Which have only Jurassic finds?
```

```solution
{{include: setup/sets/functions.py}}

finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)

jurassic = finds[(finds.oldest_mya <= 201.4) & (finds.youngest_mya >= 145)]
cretaceous = finds[(finds.oldest_mya <= 145) & (finds.youngest_mya >= 66)]
jurassic_countries = make_set(jurassic["country_code"].tolist())
cretaceous_countries = make_set(cretaceous["country_code"].tolist())

both = intersection(jurassic_countries, cretaceous_countries)
print(len(both), "countries have both")
print(difference(jurassic_countries, cretaceous_countries))
---
With the copy saved on {{snapshot: dinosaur-finds}}, 23 countries have
both. Seven have only Jurassic finds: CH, KG, LS, NA, PL, VE and ZW,
which are Switzerland, Kyrgyzstan, Lesotho, Namibia, Poland, Venezuela
and Zimbabwe. A find counts for a period only when the whole age of its
rock is inside it. `keep_default_na=False` is there for Namibia. Its code
is NA, which pandas otherwise reads as a missing value, and Namibia would
quietly vanish from the set. These are the countries where people have
dug and published, which is not the same as where dinosaurs lived.
```

</div>

<div class="dl-world" data-world="exoplanets">

The file `exoplanets.csv` has one row for each planet found around
another star, with the year it was announced and the method that found
it. Is every method used before 2000 still in use? Which methods are new
since 2020?

```python exec
id: sets-in-the-worlds--exoplanets
planets = await load_csv("exoplanets.csv")

early = make_set(planets[planets.discovered < 2000]["method"].tolist())
recent = make_set(planets[planets.discovered >= 2020]["method"].tolist())
print(early)
print(len(recent), "methods since 2020")

# Is early a subset of recent? Which methods are only in recent?
```

```solution
{{include: setup/sets/functions.py}}

planets = await load_csv("exoplanets.csv")

early = make_set(planets[planets.discovered < 2000]["method"].tolist())
recent = make_set(planets[planets.discovered >= 2020]["method"].tolist())
print(is_subset(early, recent))
print(difference(recent, early))
---
Before 2000 there were only two methods, Pulsar Timing and Radial
Velocity, and both are still in use, so `early` is a subset of `recent`.
Seven are new since then, Transit among them, which has found most of
the planets known today. A subset question with a yes answer is worth
checking both ways: `is_subset(recent, early)` is `False`.
```

</div>

<div class="dl-world" data-world="book-characters">

The file `book-characters.csv` counts how often each main character is
named in each chapter of six novels. *Pride and Prejudice* has 61
chapters. Is everyone named in the first chapter named again in the last?

```python exec
id: sets-in-the-worlds--book-characters
characters = await load_csv("book-characters.csv")
pride = characters[(characters.book == "pride-and-prejudice") & (characters.mentions > 0)]

first = make_set(pride[pride.chapter == 1]["character"].tolist())
last = make_set(pride[pride.chapter == 61]["character"].tolist())
print(first)
print(last)

# Is first a subset of last? Who is in the last chapter and not the first?
```

```solution
{{include: setup/sets/functions.py}}

characters = await load_csv("book-characters.csv")
pride = characters[(characters.book == "pride-and-prejudice") & (characters.mentions > 0)]

first = make_set(pride[pride.chapter == 1]["character"].tolist())
last = make_set(pride[pride.chapter == 61]["character"].tolist())
print(is_subset(first, last))
print(difference(last, first))
---
Yes. All five people named in chapter 1 are named again in chapter 61.
The last chapter adds Darcy, Lady Catherine, Miss Bingley, Mrs Bennet and
Wickham. Mrs Bennet is the surprise. She speaks in most of chapter 1, and
is never named in it, only "his wife" and "his lady". The data counts
names, not people, and so does any set built from it.
```

</div>

<div class="dl-world" data-world="games-of-chance">

Roll two dice. Each outcome is a pair, the first die and the second, so
`(4, 3)` and `(3, 4)` are different outcomes. An event, such as "a
double", is a set of outcomes. Python can sort pairs, so `make_set` works
on them too. Which outcomes are a double *and* add up to 8? How many are
a double *or* add up to 8?

```python exec
id: sets-in-the-worlds--games-of-chance
outcomes = []
for first in range(1, 7):
    for second in range(1, 7):
        outcomes.append((first, second))

doubles = []
eights = []
for pair in outcomes:
    if pair[0] == pair[1]:
        doubles.append(pair)
    if pair[0] + pair[1] == 8:
        eights.append(pair)
doubles = make_set(doubles)
eights = make_set(eights)
print(len(outcomes), "outcomes;", len(doubles), "doubles;", len(eights), "add up to 8")

# The outcomes in both? How many in either?
```

```solution
{{include: setup/sets/functions.py}}

outcomes = []
for first in range(1, 7):
    for second in range(1, 7):
        outcomes.append((first, second))

doubles = []
eights = []
for pair in outcomes:
    if pair[0] == pair[1]:
        doubles.append(pair)
    if pair[0] + pair[1] == 8:
        eights.append(pair)
doubles = make_set(doubles)
eights = make_set(eights)
print(intersection(doubles, eights))
print(len(union(doubles, eights)))
---
Only `(4, 4)` is in both. The union has 10 outcomes, and
inclusion-exclusion says so without listing them: 6 doubles, plus 5 ways
to make 8, minus the 1 counted twice. Out of 36 equally likely outcomes,
that is a chance of 10 in 36.
[What are the chances?](tutorial:what-are-the-chances) continues from there.
```

</div>

## Looking back

Every set on this page was kept sorted. Which of the operations would
still give the right answer on lists that were not sorted, and which
would quietly give a wrong one?

A challenge: Python's own `set` does all of this with `|`, `&` and `-`.
How much faster is it? Time `set()` against your `make_set` on a list of
100,000 random numbers.

```python challenge
import random
import time

numbers = []
for count in range(100000):
    numbers.append(random.randint(1, 50000))

start = time.perf_counter()
python_set = set(numbers)
print(len(python_set), "different numbers, in", round(time.perf_counter() - start, 4), "seconds")

# Paste your make_set here, and time it on the same list.
```

The next page, [Venn diagrams](tutorial:venn-diagrams), draws these sets
as circles, and counts what is in each part.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Khan Academy. *Intersection and Union of Sets.*
<https://www.youtube.com/watch?v=jAfNg3ylZAI>. The same two operations
this page builds with a merge walk, introduced from the mathematics side.

Python Software Foundation. *The Python Tutorial — Sets.*
<https://docs.python.org/3/tutorial/datastructures.html#sets>. The
built-in `set` this page builds its own version of, for comparison once
you have built yours.
