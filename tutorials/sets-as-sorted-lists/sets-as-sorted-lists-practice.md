---
title: "Sets: building them from sorted lists — Practice"
practice_for: sets-as-sorted-lists
year: "2026-2027"
version: 2026.09.26.1
worlds:
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  exoplanets: Planets around other stars, and the ways they were found.
  book-characters: The people in six novels, chapter by chapter.
  games-of-chance: Dice, cards and coins, and the games people play with them.
datasets: [dinosaur-genera, exoplanets, book-characters]
---

# Sets: building them from sorted lists — Practice

Here are problems on sets, some on paper, some in code, and three from
earlier pages. Try each problem before you open anything under it.
Start with the paper ones. The code is much easier to write once you
know what it should produce.

## On paper

This cell uses Python's own `set` type, which the tutorial built its own
version of. Python writes a set in curly brackets, and has an operator
for each operation: `|` for union, `&` for intersection, `-` for
difference and `^` for symmetric difference. The cell sorts each result
with `sorted()`, because Python's `set` keeps no order (problem 14 says
why). Use it to check your paper answers.

```python exec
id: set-arithmetic-1
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7}

print("union       ", sorted(A | B))
print("intersection", sorted(A & B))
print("difference  ", sorted(A - B))
print("symmetric   ", sorted(A ^ B))
```

**1.** With $A = \{1, 2, 3, 4, 5\}$ and $B = \{4, 5, 6, 7\}$, can you find
each of these?

- (a) $A \cup B$
- (b) $A \cap B$
- (c) $A \setminus B$
- (d) $B \setminus A$

<details class="dl-answer"><summary>answer</summary>

(a) $\{1, 2, 3, 4, 5, 6, 7\}$. (b) $\{4, 5\}$. (c) $\{1, 2, 3\}$. (d) $\{6, 7\}$.

(c) and (d) are different. For union and intersection, the order of the
two sets makes no difference. For difference, it does.

</details>

**2.** The symmetric difference of $A$ and $B$ is written $A \triangle B$.
It holds everything in exactly one of the two sets. What is it here?

<details class="dl-answer"><summary>answer</summary>

$\{1, 2, 3, 6, 7\}$. It is $(A \setminus B) \cup (B \setminus A)$, and it
is also $(A \cup B) \setminus (A \cap B)$.
Can you check both on the numbers above?

</details>

**3.** How many elements are in $A \cup B$? Why is it not $|A| + |B|$?

<details class="dl-answer"><summary>answer</summary>

Seven, not nine. $|A \cup B| = |A| + |B| - |A \cap B|$, which is
$5 + 4 - 2 = 7$. The two shared elements, 4 and 5, were counted twice,
so we subtract them once. This is the inclusion-exclusion principle.
[Venn diagrams](tutorial:venn-diagrams) turns it into a picture.

</details>

**4.** Is each of these true or false?

```question
id: sets-true-or-false
type: fill-in-the-blank

- $\{1, 2\} \subseteq \{1, 2, 3\}$ is {true|false}.
- $\{1, 2\} \subseteq \{1, 2\}$ is {true|false}.
- $\emptyset \subseteq \{1, 2\}$ is {true|false}.
- $\{1, 2\} \in \{1, 2, 3\}$ is {false|true}.
```

<details class="dl-answer"><summary>why</summary>

The first three are true. Every set is a subset of itself, and the
empty set is a subset of every set. For it to fail, one of its elements
would have to be missing, and it has none.

The last one is false, and it is the one to think about. $\in$ asks
about membership: is this thing one of the elements? $\subseteq$ asks
about containment: are all of these things among the elements?
$\{1, 2\}$ is made of two elements of $\{1, 2, 3\}$. It is not itself
one of the three elements 1, 2 and 3.

</details>

**5.** How many subsets does a set of 4 elements have? How many does a
set of $n$ elements have?

<details class="dl-answer"><summary>answer</summary>

16, and $2^n$. For each element there are two choices: in the subset, or
out. The choices do not depend on each other, so there are
$2 \times 2 \times \dots \times 2 = 2^n$ ways to choose. The count
includes the empty set and the whole set. A set of 20 elements has over
a million subsets, so a plan to "check all the subsets" stops working
very quickly.

</details>

**6.** Can you check $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ with
an example? Which rule of ordinary algebra does it match?

<details class="dl-answer"><summary>answer</summary>

Take $A = \{1,2,3\}$, $B = \{2,4\}$ and $C = \{3,5\}$. The left side is
$\{1,2,3\} \cap \{2,3,4,5\} = \{2,3\}$. The right side is
$\{2\} \cup \{3\} = \{2,3\}$. One example does not prove the rule, and
the rule is true for all sets.

It matches the distributive law, $a(b + c) = ab + ac$, with $\cap$ as
multiplication and $\cup$ as addition. The match is not perfect. For
sets, union also distributes over intersection,
$A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$, and in arithmetic
$a + bc$ is not $(a+b)(a+c)$.

</details>

## In code

This cell holds the tutorial's functions, so the problems below can use
them. Run it first.

```python exec
id: sets-practice-functions
{{include: setup/sets/functions.py}}

print(union([1, 3, 4, 5], [1, 2, 5, 7, 8]))
```

**7.** Sometimes only the count matters. Can you write `count_shared(a,
b)`, which gives the number of elements in both sets, with a merge walk
that never builds a list?

```python exec
id: sets-count-shared
def count_shared(a, b):
    """Return how many elements the sorted sets a and b have in common."""
    # Your code here


print(count_shared([1, 3, 4, 5], [1, 2, 5, 7, 8]))
```

```inputs
count_shared([1, 3, 4, 5], [1, 2, 5, 7, 8])
count_shared([1, 2, 3], [4, 5, 6])
count_shared([], [1, 2])
count_shared([1, 2, 3], [1, 2, 3])
```

```hint
Use the walk from `intersection()`, with a counter where it appended.
```

```solution
def count_shared(a, b):
    """Return how many elements the sorted sets a and b have in common."""
    count = 0
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            count = count + 1
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            i = i + 1
        else:
            j = j + 1
    return count


print(count_shared([1, 3, 4, 5], [1, 2, 5, 7, 8]))
---
The walk takes the same steps as `intersection()`. It only saves the
memory the list would have used, which matters once the sets are large.
With it, inclusion-exclusion needs no union at all:
`len(a) + len(b) - count_shared(a, b)` is the size of the union.
```

**8.** The tutorial's `is_subset` builds the whole intersection before it
answers. Can you write one that stops at the first element of `a` it
cannot find in `b`?

```python exec
id: sets-subset-early-stop
def is_subset_fast(a, b):
    """Return True if every element of the sorted set a is in the sorted set b."""
    # Your code here


print(is_subset_fast([2, 5], [1, 2, 3, 4, 5]))
print(is_subset_fast([0, 2, 5], [1, 2, 3, 4, 5]))
```

```inputs
is_subset_fast([2, 5], [1, 2, 3, 4, 5])
is_subset_fast([0, 2, 5], [1, 2, 3, 4, 5])
is_subset_fast([], [1, 2])
is_subset_fast([1, 2], [])
is_subset_fast([5, 6], [1, 2, 3, 4, 5])
```

```hint
Walk both lists. If `a[i]` is smaller than `b[j]`, then b has already gone
past where `a[i]` would be, so `a[i]` is not in b. What does it mean when
b ends while a still has elements left?
```

```solution
def is_subset_fast(a, b):
    """Return True if every element of the sorted set a is in the sorted set b."""
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            return False
        else:
            j = j + 1
    return i == len(a)


print(is_subset_fast([2, 5], [1, 2, 3, 4, 5]))
print(is_subset_fast([0, 2, 5], [1, 2, 3, 4, 5]))
---
`[0, 2, 5]` stops at the very first step. 0 is smaller than 1, so b has
no 0. Look at the last line. When b ends, a is a subset only if every one
of its elements was found, that is, if `i` reached the end of a.
```

**9.** A world question, with the tutorial's functions.

<div class="dl-world" data-world="dinosaurs">

In the 1870s, Othniel Marsh and Edward Drinker Cope raced each other to
name new dinosaurs, in what became known as the Bone Wars.
`dinosaur-genera.csv` records who named each genus, and the geological
age of its oldest fossils. In which ages did both men name dinosaurs?

```python exec
id: sets-bone-wars--dinosaurs
genera = await load_csv("dinosaur-genera.csv")
marsh = genera[genera.named_by.str.match(r"Marsh \d{4}$", na=False)]
cope = genera[genera.named_by.str.match(r"Cope \d{4}$", na=False)]
print(len(marsh), "genera named by Marsh,", len(cope), "by Cope")

marsh_ages = make_set(marsh["first_stage"].dropna().tolist())
cope_ages = make_set(cope["first_stage"].dropna().tolist())
```

```solution
genera = await load_csv("dinosaur-genera.csv")
marsh = genera[genera.named_by.str.match(r"Marsh \d{4}$", na=False)]
cope = genera[genera.named_by.str.match(r"Cope \d{4}$", na=False)]

marsh_ages = make_set(marsh["first_stage"].dropna().tolist())
cope_ages = make_set(cope["first_stage"].dropna().tolist())
print(intersection(marsh_ages, cope_ages))
---
With the copy saved on {{snapshot: dinosaur-genera}}, the answer is
Albian, Campanian, Kimmeridgian and Oxfordian. The Kimmeridgian and
Oxfordian are the ages of the Morrison Formation in the American West,
where both men's teams dug, sometimes within sight of each other.
`str.match` with `\d{4}$` keeps only genera named by one man alone, in
one year. A genus named "Marsh and Cope 1880" would need a different
question.
```

</div>

<div class="dl-world" data-world="exoplanets">

Some ways of finding planets only work on stars close to us, and some
only on stars far away. Which methods have found planets within 50
light-years but none beyond 1,000, and which the other way round?

```python exec
id: sets-near-and-far--exoplanets
planets = await load_csv("exoplanets.csv")
near = make_set(planets[planets.distance_ly < 50]["method"].tolist())
far = make_set(planets[planets.distance_ly > 1000]["method"].tolist())
print(near)
print(far)
```

```solution
planets = await load_csv("exoplanets.csv")
near = make_set(planets[planets.distance_ly < 50]["method"].tolist())
far = make_set(planets[planets.distance_ly > 1000]["method"].tolist())
print(difference(near, far))
print(difference(far, near))
---
Astrometry and Imaging appear only in `near`. Both need to see the
star, or the planet, clearly. A photograph of a planet is only possible
for a nearby one. Five methods appear only in `far`, Microlensing among
them. It needs a distant star to sit exactly behind a nearer one, so it works best a long way off.
The two differences are different sets, because order matters for
difference.
```

</div>

<div class="dl-world" data-world="book-characters">

*Frankenstein* opens with four letters from Robert Walton, an explorer,
before Victor Frankenstein tells his story in chapters. Who is named in
the letters, and is everyone named there named again later?

```python exec
id: sets-the-letters--book-characters
characters = await load_csv("book-characters.csv")
named = characters[(characters.book == "frankenstein") & (characters.mentions > 0)]
in_letters = make_set(named[named.chapter <= 4]["character"].tolist())
later = make_set(named[named.chapter > 4]["character"].tolist())
print(later)
```

```solution
characters = await load_csv("book-characters.csv")
named = characters[(characters.book == "frankenstein") & (characters.mentions > 0)]
in_letters = make_set(named[named.chapter <= 4]["character"].tolist())
later = make_set(named[named.chapter > 4]["character"].tolist())
print(in_letters)
print(is_subset(in_letters, later))
---
Only Walton is named in the letters, and he is named again later, so the
answer is `True`. Victor is in the letters, and is never named there.
Walton calls him "the stranger", eight times. So he is not in the set of
names.
```

</div>

<div class="dl-world" data-world="games-of-chance">

A deck has 52 cards: 13 ranks in each of four suits. With each card as a
pair, `(rank, suit)`, the hearts are one set and the picture cards (jack,
queen, king) another. How many cards are hearts or picture cards?

```python exec
id: sets-hearts-and-pictures--games-of-chance
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["clubs", "diamonds", "hearts", "spades"]
deck = []
for suit in suits:
    for rank in ranks:
        deck.append((rank, suit))

hearts = []
pictures = []
for card in deck:
    if card[1] == "hearts":
        hearts.append(card)
    if card[0] in ["J", "Q", "K"]:
        pictures.append(card)
hearts = make_set(hearts)
pictures = make_set(pictures)
```

```solution
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["clubs", "diamonds", "hearts", "spades"]
deck = []
for suit in suits:
    for rank in ranks:
        deck.append((rank, suit))

hearts = []
pictures = []
for card in deck:
    if card[1] == "hearts":
        hearts.append(card)
    if card[0] in ["J", "Q", "K"]:
        pictures.append(card)
hearts = make_set(hearts)
pictures = make_set(pictures)
print(len(union(hearts, pictures)))
print(len(hearts) + len(pictures) - len(intersection(hearts, pictures)))
---
22 both ways: 13 hearts and 12 picture cards, minus the 3 that are both.
The sorted order of the pairs looks odd, with "10" before "2", because
the ranks are text, compared letter by letter. The set operations do not
mind, as long as both sets are sorted the same way.
```

</div>

## Sets in practice

These use Python's own `set`, with the same operators as the first cell.

**10.** Two students each take a list of modules. Which modules do both
take, which only the first, and how many different modules are there in
all?

```python exec
id: sets-two-timetables
ann = {"maths", "programming", "databases", "networks"}
ben = {"programming", "databases", "web", "security"}
```

```solution
ann = {"maths", "programming", "databases", "networks"}
ben = {"programming", "databases", "web", "security"}
print(sorted(ann & ben))
print(sorted(ann - ben))
print(len(ann | ben))
---
`['databases', 'programming']`, then `['maths', 'networks']`, then 6.
```

**11.** Two mailing lists share some people, written with capitals in
different places. Can you find the addresses on both, ignoring upper and
lower case?

```python exec
id: sets-two-mailing-lists
first = ["Ada@example.org", "grace@example.org", "Alan@Example.org"]
second = ["ada@example.org", "linus@example.org", "alan@example.org"]
common = set()
print(sorted(common))
```

```inputs
sorted(common)
```

```hint
Make every address lower case before it goes into a set. `.lower()` does
that for one string. A loop, or a set comprehension, does it for a list.
```

```solution
first = ["Ada@example.org", "grace@example.org", "Alan@Example.org"]
second = ["ada@example.org", "linus@example.org", "alan@example.org"]
common = {e.lower() for e in first} & {e.lower() for e in second}
print(sorted(common))
---
`['ada@example.org', 'alan@example.org']`. The main job is to make the
addresses match before comparing them. The part after the @ is never
case-sensitive. The standard lets the part before it be case-sensitive,
and almost no email provider treats it that way. So lower case works in
practice.
```

**12.** A set has 3 elements. Can you list all its subsets, and check that
there are 8?

<details class="dl-answer"><summary>answer</summary>

For $\{a, b, c\}$: $\emptyset$, $\{a\}$, $\{b\}$, $\{c\}$, $\{a,b\}$,
$\{a,c\}$, $\{b,c\}$ and $\{a,b,c\}$. In code, count in binary from 0 to
7. Bit `i` of the number says whether item `i` is in the subset.

```python
items = ["a", "b", "c"]
for pattern in range(2 ** len(items)):
    print([items[i] for i in range(len(items)) if pattern >> i & 1])
```

Each subset matches one binary number, which is why there are exactly
$2^n$.

</details>

## From earlier

**13.** From *Searching a list*. `binary_search` looks for 7 in
`[1, 3, 7, 7, 7, 9]`. The list has three 7s. Which position does it
find?

```python exec
id: sets-from-earlier-repeats
def binary_search(items, target):
    low = 0
    high = len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


print(binary_search([1, 3, 7, 7, 7, 9], 7))
```

```predict
type: number

Which position will it print?
```

<details class="dl-answer"><summary>why</summary>

2. The first middle, `(0 + 5) // 2`, is already a 7, so the search stops
there. With repeats, binary search finds *a* match, not the first one.
That is one more reason a set keeps no repeats. "Is it there?" has one
answer, and "where is it?" would have three.

</details>

**14.** From *Looking things up by name*. Why does Python's own `set` not
keep its elements in order, when a dictionary's keys do stay in the order
they were added?

<details class="dl-answer"><summary>answer</summary>

Both are *hash tables*. A hash table calculates a number, a hash, from each
element, and uses it to decide where the element is stored. The hash has
nothing to do with order. A dictionary also keeps a separate record of the
order keys arrived in, since Python 3.7, and a set does not. Neither
keeps *sorted* order. A hash table answers "is it there?" in about the
same time however large it is, and a sorted list takes about $\log n$
steps. But only the sorted list can give you its smallest element
without looking at all of it.

</details>

**15.** From *Sorting a list*. `make_set` sorts first. On a list of
10,000 items, about how many comparisons would a slow sort, such as
selection sort, make, against Python's `sorted()`?

<details class="dl-answer"><summary>answer</summary>

Selection sort makes $\frac{n(n-1)}{2}$, which is about 50 million for
10,000 items. `sorted()` makes roughly $n \log_2 n$, about 130,000. The
set operations after the sort are cheap. The sort decides how fast
`make_set` is.

</details>
