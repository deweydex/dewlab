---
title: "Venn diagrams: drawing sets and their overlaps"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  book-characters: The people in six novels, chapter by chapter.
datasets: [dinosaur-finds, book-characters]
covers:
  two-circles-from-real-sets:
    covers: [MIT-2.3]
  the-regions-have-names-you-already-know:
    covers: [MIT-2.3]
  three-sets-which-is-where-it-earns-its-place:
    covers: [MIT-2.3]
  the-same-laws-in-a-different-notation:
    covers: [MIT-2.3]
---

# Venn diagrams: drawing sets and their overlaps

Roll two dice. There are 36 outcomes, from `(1, 1)` to `(6, 6)`. Two
events are sets of them: "a double", and "the dice add up to 8". This
cell collects both, and draws them as two circles.

```python exec
id: venn-two-events
import matplotlib.pyplot as plt

outcomes = set()
for first in range(1, 7):
    for second in range(1, 7):
        outcomes.add((first, second))

doubles = set()
eights = set()
for pair in outcomes:
    if pair[0] == pair[1]:
        doubles.add(pair)
    if pair[0] + pair[1] == 8:
        eights.add(pair)


def draw_two(left, right, left_name, right_name):
    """Draw two overlapping circles, with how many elements are in each part."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(plt.Circle((-0.5, 0), 1.3, fill=False, linewidth=2))
    ax.add_patch(plt.Circle((0.5, 0), 1.3, fill=False, linewidth=2))
    ax.text(-1.3, 0, str(len(left - right)), ha="center", fontsize=16)
    ax.text(0, 0, str(len(left & right)), ha="center", fontsize=16)
    ax.text(1.3, 0, str(len(right - left)), ha="center", fontsize=16)
    ax.text(-1.3, 1.5, left_name, ha="center")
    ax.text(1.3, 1.5, right_name, ha="center")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-1.8, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


draw_two(doubles, eights, "a double", "adds up to 8")
print(len(doubles), "doubles,", len(eights), "ways to make 8, and in both:", len(doubles & eights))
```

```predict
type: number

There are 6 doubles, and 5 ways to make 8. How many outcomes are in
both, where the circles overlap?
```

A *Venn diagram* is a picture of sets: each set is a circle, and the
circles overlap where the sets share elements. Every number in this one
came from a set operation. Nobody placed them by hand, so the picture
cannot disagree with the sets: change the sets, and the picture changes
with them.

With two sets you can often keep the picture in your head. The diagram
earns its place at three, and this page ends at the point where it stops
helping at all.

## Python's own sets

On [Sets: building them from sorted lists](tutorial:sets-as-sorted-lists)
we built every operation ourselves. From here on we use Python's own
`set`, which does the same jobs with shorter names:

| On the sets page | Python's `set` |
|---|---|
| `make_set(items)` | `set(items)` |
| `is_member(s, x)` | `x in s` |
| `union(a, b)` | `a \| b` |
| `intersection(a, b)` | `a & b` |
| `difference(a, b)` | `a - b` |
| `symmetric_difference(a, b)` | `a ^ b` |
| `is_subset(a, b)` | `a <= b` |

A Python set keeps no order, so `sorted()` is the way to print one
neatly. `s.add(x)` puts one element in.

## Two circles, from real sets

What do you think the diagram looks like for two events that cannot
happen together? And for one event that sits completely inside another?

```python exec
id: venn-no-overlap
# A double, and an odd total: a double always adds up to an even number.
odd_totals = set()
for pair in outcomes:
    if (pair[0] + pair[1]) % 2 == 1:
        odd_totals.add(pair)
draw_two(doubles, odd_totals, "a double", "an odd total")
```

```python exec
id: venn-inside
# Double sixes, and doubles.
draw_two({(6, 6)}, doubles, "double six", "a double")
```

The code did not change; the picture did. When the middle number is 0,
or one of the outer numbers is, that is not the drawing going wrong. It
is the diagram saying something true about the sets: a double and an odd
total never happen together, and every double six is a double.

## The regions have names you already know

Each part of the two-circle diagram matches an operation:

| Region | Operation | Python |
|---|---|---|
| Only in the left circle | difference | `doubles - eights` |
| The overlap | intersection | `doubles & eights` |
| Only in the right circle | difference the other way | `eights - doubles` |
| All three parts together | union | `doubles \| eights` |

```python exec
id: venn-regions
print("doubles - eights :", sorted(doubles - eights))
print("doubles & eights :", sorted(doubles & eights))
print("eights - doubles :", sorted(eights - doubles))
print("doubles | eights :", len(doubles | eights), "outcomes")
```

```predict
type: number

How many outcomes are a double *or* add up to 8? The last line prints it.
```

<details class="dl-answer"><summary>Why not 11?</summary>

6 doubles and 5 eights make 11, and `(4, 4)` is in both, so it was
counted twice. The union has 10: inclusion-exclusion, from the sets
page, $|A \cup B| = |A| + |B| - |A \cap B| = 6 + 5 - 1$. The diagram
shows it without the formula: add up the three numbers, and the middle
is only counted once.

</details>

### Your turn

The diagram leaves one part out: the outcomes in neither circle. Can you
set `exactly_one` to the outcomes in exactly one of the two events, and
`neither` to the outcomes in neither?

```python exec
id: venn-exactly-one-and-neither
exactly_one = set()
neither = set()

print(len(exactly_one), "in exactly one;", len(neither), "in neither")
```

```inputs
sorted(exactly_one)
len(neither)
```

```hint
Exactly one is everything in either circle except the middle. For
neither, start from every outcome, `outcomes`, and take away everything
in either circle.
```

```solution
exactly_one = doubles ^ eights
neither = outcomes - (doubles | eights)

print(len(exactly_one), "in exactly one;", len(neither), "in neither")
---
9 in exactly one, and 26 in neither. With the 1 in the middle, 9 + 1 + 26
is 36: every outcome is somewhere, once. `^` is *exclusive or*: in one or
the other, not both. The next page meets it again, as a fact about true
and false.
```

## Three sets, which is where it earns its place

Now three events: a double, a total of at least 8, and an even number on
the first die.

```python exec
id: venn-three-events
at_least_8 = set()
first_even = set()
for pair in outcomes:
    if pair[0] + pair[1] >= 8:
        at_least_8.add(pair)
    if pair[0] % 2 == 0:
        first_even.add(pair)


def draw_three(a, b, c, names):
    """Draw three overlapping circles, with how many elements are in each part."""
    fig, ax = plt.subplots(figsize=(6, 5.5))
    for (x, y) in [(-0.6, 0.35), (0.6, 0.35), (0, -0.7)]:
        ax.add_patch(plt.Circle((x, y), 1.2, fill=False, linewidth=2))
    regions = {
        (-1.25, 0.75): a - b - c,
        (1.25, 0.75): b - a - c,
        (0, -1.45): c - a - b,
        (0, 0.85): (a & b) - c,
        (-0.75, -0.4): (a & c) - b,
        (0.75, -0.4): (b & c) - a,
        (0, 0.0): a & b & c,
    }
    for (x, y), members in regions.items():
        ax.text(x, y, str(len(members)), ha="center", va="center", fontsize=15)
    for (x, y), name in zip([(-1.5, 1.75), (1.5, 1.75), (0, -2.2)], names):
        ax.text(x, y, name, ha="center", fontsize=11)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


draw_three(doubles, at_least_8, first_even, ["a double", "at least 8", "first die even"])
```

Now there are seven regions, one for each way of being in or out of each
circle. Try holding all seven in your head at once. Most people cannot,
and there is no reason they should.

Here is a question that is awkward in symbols and easy on the picture:
which outcomes are a double or at least 8, but have an odd first die?
Before you run the cell, which regions hold them?

```python exec
id: venn-double-or-high-but-odd
print(sorted((doubles | at_least_8) - first_even))
```

Find them on the diagram: the top two regions, the region between them,
and nothing in the bottom circle. That is 2 + 5 + 1 = 8 outcomes. Now
try to convince yourself of the same answer from the expression alone.
Which way was quicker?

Here are two expressions that look different. Do they give the same set?
The diagram can tell you before Python does.

```python exec
id: venn-two-expressions
first = (doubles & at_least_8) | (doubles & first_even)
second = doubles & (at_least_8 | first_even)
print(first == second)
```

```predict
Will it print True or False?

- True
  - Both are the doubles that are also in at least one of the other two circles.
- False
  - The first combines two overlaps, the second only one.
```

<details class="dl-answer"><summary>Why they match</summary>

`True`. Shade each one on the diagram: both are the parts of the doubles
circle that are also inside at least one of the other two. It is the
distributive law, $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$, with
$\cap$ playing multiplication and $\cup$ playing addition, as in
$a(b + c) = ab + ac$.

</details>

### Your turn

Choose a world at the top of the page. Each one has three sets of its
own, and a question the diagram can answer.

<div class="dl-world" data-world="games-of-chance">

Toss three coins. Each outcome is three letters, such as `"HHT"`. The
events: the first coin is heads, at least two are heads, and all three
are the same. Two regions will be empty: can you say why before you
draw it? Then set `answer` to the outcomes with at least two heads that
are not all the same.

```python exec
id: venn-your-world--games-of-chance
tosses = set()
for a in "HT":
    for b in "HT":
        for c in "HT":
            tosses.add(a + b + c)

first_heads = set()
two_heads = set()
all_same = set()
for toss in tosses:
    if toss[0] == "H":
        first_heads.add(toss)
    if toss.count("H") >= 2:
        two_heads.add(toss)
    if toss[0] == toss[1] == toss[2]:
        all_same.add(toss)

draw_three(first_heads, two_heads, all_same, ["first is heads", "two or more heads", "all the same"])
answer = set()
```

```inputs
sorted(answer)
```

```solution
tosses = set()
for a in "HT":
    for b in "HT":
        for c in "HT":
            tosses.add(a + b + c)

first_heads = set()
two_heads = set()
all_same = set()
for toss in tosses:
    if toss[0] == "H":
        first_heads.add(toss)
    if toss.count("H") >= 2:
        two_heads.add(toss)
    if toss[0] == toss[1] == toss[2]:
        all_same.add(toss)

answer = two_heads - all_same
print(sorted(answer))
---
`['HHT', 'HTH', 'THH']`. The two empty regions are "first is heads and
all the same, but not two heads", and "two heads and all the same, but
the first is tails". Both are impossible: all the same with a head first
is HHH, which has three heads, and all the same with two heads is HHH
again. An empty region is the diagram saying so. TTH and THT are in no
circle at all.
```

</div>

<div class="dl-world" data-world="dinosaurs">

The Triassic ran from 251.9 to 201.4 million years ago, the Jurassic
from 201.4 to 145, and the Cretaceous from 145 to 66. For each period,
this cell collects the countries with a dinosaur find from it, and draws
the three. Can you set `answer` to the countries with Triassic or
Jurassic finds, and none from the Cretaceous?

```python exec
id: venn-your-world--dinosaurs
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)


def countries(oldest, youngest):
    """The countries with a find whose rock is wholly inside this span of time."""
    inside = finds[(finds.oldest_mya <= oldest) & (finds.youngest_mya >= youngest)]
    return set(inside["country_code"])


triassic = countries(251.9, 201.4)
jurassic = countries(201.4, 145)
cretaceous = countries(145, 66)
draw_three(triassic, jurassic, cretaceous, ["Triassic", "Jurassic", "Cretaceous"])
answer = set()
```

```inputs
sorted(answer)
```

```solution
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)


def countries(oldest, youngest):
    """The countries with a find whose rock is wholly inside this span of time."""
    inside = finds[(finds.oldest_mya <= oldest) & (finds.youngest_mya >= youngest)]
    return set(inside["country_code"])


triassic = countries(251.9, 201.4)
jurassic = countries(201.4, 145)
cretaceous = countries(145, 66)
answer = (triassic | jurassic) - cretaceous
print(sorted(answer))
---
With the copy saved on {{snapshot: dinosaur-finds}}, ten codes, from CH
(Switzerland) to ZW (Zimbabwe). One of them is not a country: O2 is the
North Sea, where a *Plateosaurus* bone came up in a rock core drilled far
beneath the sea floor. Nine countries have finds from all three periods,
and 29 from the Cretaceous only, partly because more rock of that age is
at the surface, where people can find it.
```

</div>

<div class="dl-world" data-world="book-characters">

A set can hold chapter numbers. This cell collects the chapters of *Pride
and Prejudice* that name Lydia, Mr Bingley and Wickham, and draws the
three. Can you set `answer` to the chapters that name Wickham or Lydia,
but not Mr Bingley?

```python exec
id: venn-your-world--book-characters
characters = await load_csv("book-characters.csv")
pride = characters[(characters.book == "pride-and-prejudice") & (characters.mentions > 0)]


def chapters_naming(name):
    """The chapters of Pride and Prejudice that name this character."""
    return set(pride[pride.character == name]["chapter"])


lydia = chapters_naming("Lydia")
bingley = chapters_naming("Mr Bingley")
wickham = chapters_naming("Wickham")
draw_three(lydia, bingley, wickham, ["Lydia", "Mr Bingley", "Wickham"])
answer = set()
```

```inputs
sorted(answer)
```

```solution
characters = await load_csv("book-characters.csv")
pride = characters[(characters.book == "pride-and-prejudice") & (characters.mentions > 0)]


def chapters_naming(name):
    """The chapters of Pride and Prejudice that name this character."""
    return set(pride[pride.character == name]["chapter"])


lydia = chapters_naming("Lydia")
bingley = chapters_naming("Mr Bingley")
wickham = chapters_naming("Wickham")
answer = (wickham | lydia) - bingley
print(sorted(answer))
---
Fifteen chapters, from 14 to 52, and most of them late in the book, when
Lydia runs away with Wickham and Mr Bingley is away from Netherfield. Five
chapters name none of the three: 19, 22, 28, 30 and 31, which are Mr
Collins's proposal, Charlotte's engagement, and Elizabeth's visit to
Hunsford.
```

</div>

## The same laws, in a different notation

Every outcome is either in a set or not. The set of everything *not* in
a set is its *complement*: here, every outcome of the two dice that is
not in it. De Morgan's laws say how "not" meets "or" and "and". Picture
the two-circle diagram as you read each pair: which region does each
line describe?

```python exec
id: venn-de-morgan
def complement(s):
    """Every outcome of two dice that is not in s."""
    return outcomes - s


print(len(complement(doubles | eights)), "are not (a double or an 8)")
print(len(complement(doubles) & complement(eights)), "are (not a double) and (not an 8)")
print()
print(len(complement(doubles & eights)), "are not (a double and an 8)")
print(len(complement(doubles) | complement(eights)), "are (not a double) or (not an 8)")
```

The two lines in each pair are the same: 26, the region outside both
circles, and 35, everything but the middle. On the diagram you can *see*
that the region outside both circles is the overlap of the two outsides.
The next page, [Logic](tutorial:logic-and-truth), proves the same laws a
different way, by checking every row of a truth table. They are one fact
in two notations, and whichever makes sense to you first can explain the
other.

## Where the picture stops helping

Three circles give seven regions: every combination of in and out for
three sets, apart from "in none of them", which is the space outside. In
general, $n$ sets need $2^n - 1$ regions inside the circles. How many do
you expect four sets to need?

```python exec
id: venn-how-many-regions
for n in (2, 3, 4, 5):
    print(n, "sets need", 2 ** n - 1, "regions")
```

Four sets need fifteen regions, and four circles cannot make them. This
is a fact about circles on a flat page, not a weakness of the drawing
code: no arrangement of four circles makes all fifteen. Diagrams for four
sets do exist, with ovals or stranger shapes, and they are much harder to
read, which defeats the purpose.

The set operations keep working for four sets, or forty. Every way of
showing an idea stops working somewhere, and part of knowing a tool is
knowing where.

## Looking back

Four sets need fifteen regions, and circles cannot draw them. If a
question needed four sets, how would you show somebody the answer
without a diagram?

A challenge: draw the Venn diagram for three events from a game you
know. The starter draws one for a deck of cards; change the events, or
the game.

```python challenge
import matplotlib.pyplot as plt


def draw_three(a, b, c, names):
    fig, ax = plt.subplots(figsize=(6, 5.5))
    for (x, y) in [(-0.6, 0.35), (0.6, 0.35), (0, -0.7)]:
        ax.add_patch(plt.Circle((x, y), 1.2, fill=False, linewidth=2))
    regions = {
        (-1.25, 0.75): a - b - c, (1.25, 0.75): b - a - c, (0, -1.45): c - a - b,
        (0, 0.85): (a & b) - c, (-0.75, -0.4): (a & c) - b, (0.75, -0.4): (b & c) - a,
        (0, 0.0): a & b & c,
    }
    for (x, y), members in regions.items():
        ax.text(x, y, str(len(members)), ha="center", va="center", fontsize=15)
    for (x, y), name in zip([(-1.5, 1.75), (1.5, 1.75), (0, -2.2)], names):
        ax.text(x, y, name, ha="center", fontsize=11)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = set()
for suit in ["clubs", "diamonds", "hearts", "spades"]:
    for rank in ranks:
        deck.add((rank, suit))

hearts = {card for card in deck if card[1] == "hearts"}
pictures = {card for card in deck if card[0] in ["J", "Q", "K"]}
red = {card for card in deck if card[1] in ["hearts", "diamonds"]}
draw_three(hearts, pictures, red, ["hearts", "picture cards", "red"])
```

The next page, [Logic: truth tables, XOR and De Morgan's
laws](tutorial:logic-and-truth), finds the same rules in true and false.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Khan Academy. *Visualising Set Operations Using Venn Diagrams.*
<https://www.youtube.com/watch?v=c6TY6fVUlDQ>. The same two-circle
pictures this page draws from real data, drawn by hand instead.

Khan Academy. *Properties of Set Operations Using Venn Diagrams.*
<https://www.youtube.com/watch?v=lWjmbch870g>. De Morgan's laws shaded on
a diagram, which is where this page ends up.
