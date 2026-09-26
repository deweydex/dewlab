---
title: "Venn diagrams: drawing sets and their overlaps — Practice"
practice_for: venn-diagrams
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  book-characters: The people in six novels, chapter by chapter.
datasets: [dinosaur-finds, book-characters]
---

# Venn diagrams: drawing sets and their overlaps — Practice

Problems on two and three sets, and three from earlier pages. When a
question is about three sets, sketch the diagram first, then work out the
answer: helping you think is what the diagram is for.

## Tools

This cell sets up a class of nine students, `everyone`, and three sets:
who knows Python, who knows SQL, and who knows JavaScript. Run it before
the problems, and use it to check your answers.

```python exec
id: tools-1
everyone = {"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona", "Gearoid", "Hannah", "Iarla"}
python = {"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona"}
sql = {"Cara", "Dara", "Eoin", "Gearoid", "Hannah"}
javascript = {"Dara", "Eoin", "Fiona", "Hannah", "Iarla"}


def complement(s):
    return everyone - s


print("python & sql :", sorted(python & sql))
```

## Two sets

```question
id: venn-two-sets-who
type: fill-in-the-blank

- Python but not SQL is the {difference|intersection|union|symmetric difference}, `python - sql`.
- Exactly one of Python and SQL is the {symmetric difference|difference|intersection|union}, `python ^ sql`.
- Neither Python nor SQL is everything outside the {union|intersection|difference|symmetric difference}.
```

<details class="dl-answer"><summary>who they are</summary>

Aoife, Ben and Fiona know Python but not SQL. Aoife, Ben, Fiona, Gearoid
and Hannah know exactly one: the symmetric difference, XOR for sets.
Only Iarla knows neither.

</details>

**1.** How many regions does a two-circle diagram have, if you count the
outside?

<details class="dl-answer"><summary>answer</summary>

Four: only in the left circle, only in the right, in both, and in
neither. The outside region is easy to forget, and it is often the one a
question asks about.

</details>

**2.** In a class of 30, 18 students take Maths and 15 take Physics. 7
take both. How many take neither?

<details class="dl-answer"><summary>answer</summary>

$18 + 15 - 7 = 26$ take at least one, so $30 - 26 = 4$ take neither.
Taking away the 7 is the key step: adding 18 and 15 counts those seven
students twice.

</details>

## Three sets

**3.** How many regions does a three-circle diagram have, if you count
the outside?

<details class="dl-answer"><summary>answer</summary>

Eight. For each of the three sets, a person is in it or out of it:
$2 \times 2 \times 2 = 8$ combinations.

</details>

**4.** Who knows Python or SQL, but not JavaScript? And who knows all
three?

<details class="dl-answer"><summary>answer</summary>

`(python | sql) - javascript` gives Aoife, Ben, Cara and Gearoid.
`python & sql & javascript` gives Dara and Eoin.

</details>

**5.** Can you write `exactly_two(a, b, c)`, which gives the elements in
exactly two of the three sets? Sketch which regions it means first.

```python exec
id: venn-exactly-two
def exactly_two(a, b, c):
    """Return the set of elements that are in exactly two of a, b and c."""
    # Your code here


print(sorted(exactly_two(python, sql, javascript)))
```

```inputs
sorted(exactly_two(python, sql, javascript))
sorted(exactly_two({1, 2}, {2, 3}, {3, 1}))
sorted(exactly_two({1}, {1}, {1}))
```

```hint
Three regions, one for each pair: in a and b but not c, in a and c but
not b, in b and c but not a. Join them with `|`.
```

```solution
def exactly_two(a, b, c):
    """Return the set of elements that are in exactly two of a, b and c."""
    return ((a & b) - c) | ((a & c) - b) | ((b & c) - a)


print(sorted(exactly_two(python, sql, javascript)))
---
Cara, Fiona and Hannah. The three pair-overlaps each lose the middle,
since the middle is in all three, not two. Another route counts:
an element is in exactly two when `(x in a) + (x in b) + (x in c)` is 2,
since `True` counts as 1.
```

**6.** In a survey of 100 people, 60 use email, 45 use messaging and 40
use the phone. 30 use email and messaging, 20 email and the phone, and 15
messaging and the phone. 10 use all three. How many use at least one?

<details class="dl-answer"><summary>answer</summary>

$60 + 45 + 40 - 30 - 20 - 15 + 10 = 90$. Add the single sets, take away
the pairs, then add the triple back. The ten who use all three were added
three times, once for each single set, then taken away three times, once
for each pair, which leaves them counted zero times, so they go back in
once.

</details>

**7.** Three sets from a world, and a diagram that says something about
it.

<div class="dl-world" data-world="games-of-chance">

Two dice: the total is even, the total is at least 10, and a double. How
many outcomes are in exactly two of the three events, and why are none
of them a double with an odd total?

```python exec
id: venn-world--games-of-chance
rolls = {(a, b) for a in range(1, 7) for b in range(1, 7)}
even = {r for r in rolls if (r[0] + r[1]) % 2 == 0}
high = {r for r in rolls if r[0] + r[1] >= 10}
double = {r for r in rolls if r[0] == r[1]}
```

```solution
rolls = {(a, b) for a in range(1, 7) for b in range(1, 7)}
even = {r for r in rolls if (r[0] + r[1]) % 2 == 0}
high = {r for r in rolls if r[0] + r[1] >= 10}
double = {r for r in rolls if r[0] == r[1]}
two = ((even & high) - double) | ((even & double) - high) | ((high & double) - even)
print(len(two), sorted(two))
---
Six: the four low doubles, which are even and not high, and (4, 6) and
(6, 4), which are even and high and not doubles. A double always has an
even total, so the double circle sits wholly inside the even one, and
the parts of it outside the even circle are empty. `{r for r in rolls
if ...}` is a *set comprehension*: a list comprehension in curly
brackets, which builds a set.
```

</div>

<div class="dl-world" data-world="dinosaurs">

Three countries, and the dinosaur genera found in each: the United
States, China and Argentina. Which genera are found in more than one?
Draw the diagram in your head before you run the answer: is any circle
on its own?

```python exec
id: venn-world--dinosaurs
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)


def genera_in(code):
    """The genera found in one country: the first word of each find's name."""
    names = finds[finds.country_code == code]["name"]
    return {name.split()[0] for name in names}


us = genera_in("US")
china = genera_in("CN")
argentina = genera_in("AR")
print(len(us), len(china), len(argentina))
```

```solution
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)


def genera_in(code):
    """The genera found in one country: the first word of each find's name."""
    names = finds[finds.country_code == code]["name"]
    return {name.split()[0] for name in names}


us = genera_in("US")
china = genera_in("CN")
argentina = genera_in("AR")
print(sorted(us & china))
print(us & argentina, china & argentina)
---
Eight genera are found in both the United States and China, with the
copy saved on {{snapshot: dinosaur-finds}}. Argentina shares none with
either: its circle stands alone. Through much of the age of dinosaurs,
South America was part of a southern continent, Gondwana, which was
separating from the northern lands, and that is likely part of the
reason. A diagram with one circle apart is the start of that story, not
the end of it.
```

</div>

<div class="dl-world" data-world="book-characters">

In *Pride and Prejudice*, Mr Collins marries Charlotte, and works for
Lady Catherine. Which chapters name Mr Collins and Charlotte, but not
Lady Catherine? And which name Lady Catherine alone?

```python exec
id: venn-world--book-characters
characters = await load_csv("book-characters.csv")
pride = characters[(characters.book == "pride-and-prejudice") & (characters.mentions > 0)]
collins = set(pride[pride.character == "Mr Collins"]["chapter"])
charlotte = set(pride[pride.character == "Charlotte"]["chapter"])
catherine = set(pride[pride.character == "Lady Catherine"]["chapter"])
```

```solution
characters = await load_csv("book-characters.csv")
pride = characters[(characters.book == "pride-and-prejudice") & (characters.mentions > 0)]
collins = set(pride[pride.character == "Mr Collins"]["chapter"])
charlotte = set(pride[pride.character == "Charlotte"]["chapter"])
catherine = set(pride[pride.character == "Lady Catherine"]["chapter"])
print(sorted((collins & charlotte) - catherine))
print(sorted(catherine - collins - charlotte))
---
Chapters 20, 24 and 25 name Mr Collins and Charlotte without Lady
Catherine, and 58 and 61 name her alone, both near the end of the book,
after her visit to Longbourn. Fifteen chapters name all three, which
says how tied together the three of them are.
```

</div>

## De Morgan on sets

**8.** Is the complement of $A \cup B$ the same as the intersection of
the two complements? And the complement of $A \cap B$, the same as the
union of the complements?

<details class="dl-answer"><summary>answer</summary>

Yes, both. Being outside both circles is being outside the first and
outside the second. Being outside the overlap is missing at least one of
the circles: outside the first or outside the second. Shade each pair on
a diagram, and they cover the same region.

</details>

## Where it runs out

**9.** What still works well at four sets, when four circles cannot draw
them?

<details class="dl-answer"><summary>answer</summary>

The set operations: `A & B & C & D` is no harder to compute than
`A & B`, and inclusion-exclusion works for any number of sets. Every way
of showing an idea stops working somewhere, and part of knowing a tool
is knowing where.

</details>

## One longer one

**10.** A support team sorts its tickets by category. There are 120
hardware tickets, 95 software and 60 network. 30 are both hardware and
software, 25 hardware and network, and 20 software and network. 10 are in
all three. There are 250 tickets in total.

- (a) How many are in at least one category?
- (b) How many are in none?
- (c) How many are hardware only?

<details class="dl-answer"><summary>answer</summary>

(a) $120 + 95 + 60 - 30 - 25 - 20 + 10 = 210$.

(b) $250 - 210 = 40$.

(c) Start with the 120 hardware tickets. Take away those also software
(30) and those also network (25). That takes away the ten in all three
twice, so add ten back: $120 - 30 - 25 + 10 = 75$. Without a diagram, it
is very hard to notice the all-three region went twice; with one, it is
easy to see.

</details>

## From earlier

**11.** From *Sets*. On that page, `is_subset(a, b)` checked that every
element of a is in b. Python writes it `a <= b`. With `double` as every
double on two dice and `even` as every even total, what do these print?

```python exec
id: venn-from-earlier-subset
rolls = {(a, b) for a in range(1, 7) for b in range(1, 7)}
double = {r for r in rolls if r[0] == r[1]}
even = {r for r in rolls if (r[0] + r[1]) % 2 == 0}
print(double <= even, even <= double)
```

```predict
What will it print?

- True False
  - Every double is even, and most even totals are not doubles.
- True True
  - They are the same kind of roll.
- False False
  - Neither set fits inside the other.
```

**12.** From *Sets*. With inclusion-exclusion, how many cards in a deck
are hearts or aces?

<details class="dl-answer"><summary>answer</summary>

$13 + 4 - 1 = 16$: 13 hearts, 4 aces, and the ace of hearts is both.

</details>

**13.** From *Making decisions*. The numbers for which `x > 2 and x < 8`
is true form a set. Is it the intersection or the union of the numbers
more than 2 and the numbers less than 8?

<details class="dl-answer"><summary>answer</summary>

The intersection: `and` asks for both, the overlap of the two sets. With
`or`, every number would be in at least one of them, so the union would
be every number there is.

</details>
