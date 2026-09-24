---
title: "Circles that overlap: Venn diagrams"
year: "2026-2027"
version: 2026.09.24.1
covers:
  two-circles-in-a-box:
    covers: [MIT-2.3]
    touches: [MIT-2.2]
  counting-either-inclusion-exclusion:
    covers: [MIT-2.3]
    touches: [MIT-5.8]
  three-circles-eight-regions:
    covers: [MIT-2.3]
  yes-to-exactly-two:
    covers: [MIT-2.3]
    touches: [PDP-LO6]
  inclusion-exclusion-for-three-sets:
    covers: [MIT-2.3]
  filling-a-diagram-from-the-totals:
    covers: [MIT-2.3]
---

# Circles that overlap: Venn diagrams

A sports club wants to run a triathlon taster day: a short swim, a short
cycle and a short run. It asked its 20 members three questions. Do you
swim? Do you cycle? Do you run? The people most likely to sign up are the
ones who already do two of the three. How many people answered yes to
exactly two questions out of three?

On this page we:

- draw two sets as two circles in a box, and name every region
- count the people in either circle, without counting anyone twice
- draw three circles, and find all eight of their regions
- answer the club's question in two different ways, and check that they
  agree
- fill in a diagram from a survey's totals alone, when nobody gives us
  the names

> **The space we're in.** Sets of names, from
> [Collections without repeats](tutorial:collections-without-repeats):
> a set holds each value once, in no order, and Python works out unions,
> intersections and differences for us. Every set on this page sits
> inside one universal set, the people who were asked. That usually goes
> unsaid on a survey report, and it matters: "everyone who does not
> swim" means nothing until we say everyone out of whom. Every survey on
> this page is made up, so that the numbers stay small enough to check
> by eye.

## Warm-up

The first question is from
[Collections without repeats](tutorial:collections-without-repeats), and
the second from
[Chances that combine](tutorial:chances-that-combine#when-both-can-happen).

```question
id: circles-warm-up-1
type: fill-in-the-blank

`{"rock", "jazz", "folk"} & {"jazz", "folk", "trad"}` keeps only the
values in both sets, so it has {2} values in it.
```

```question
id: circles-warm-up-2
type: multiple-choice
correct: 3

On one roll of a die, "even" has chance $\frac{3}{6}$ and "more than 4"
has chance $\frac{2}{6}$. The chance of "even or more than 4" is not
$\frac{5}{6}$. Why not?

- A die cannot be even and more than 4 at the same time.
- Chances are multiplied, not added.
- The 6 is in both events, so adding counts it twice.
```

## Two circles in a box

Here are the club's answers, as three sets. Each set holds the names of
the members who said yes to one question. The fourth set, `members`, is
everyone who was asked.

```python exec
id: circles-club-1
swimmers = {"Aoife", "Hassan", "Ben", "Isla", "Rory", "Priya", "Wei",
            "Ciara", "Eoin", "Maeve"}
cyclists = {"Aoife", "Hassan", "Ben", "Isla", "Rory", "Priya", "Wei",
            "Dmitri", "Kate", "Fatima", "Liam"}
runners = {"Aoife", "Hassan", "Ciara", "Dmitri", "Kate", "Grainne",
           "Sadhbh", "Tomas"}
members = swimmers | cyclists | runners | {"Jakub", "Niamh", "Oisin"}

print(len(members), "members")
print(len(swimmers), "swim,", len(cyclists), "cycle,", len(runners), "run")
```

Twenty members. 10 swim, 11 cycle and 8 run, and $10 + 11 + 8 = 29$,
which is more than 20. Some people must be in more than one set. A list
of names hides that. A picture shows it.

Let's start with two of the questions: swimming and cycling. Draw a box
for everyone who was asked. Inside it, draw one circle for the swimmers
and one for the cyclists, and let the circles overlap. Every member now
stands in exactly one of four places: only in the swim circle, in both
circles, only in the cycle circle, or outside both.

A *Venn diagram* is a picture of sets as circles inside a box, where
each circle holds one set, and where two circles overlap the sets share
members. It is named after John Venn, who drew them in 1880. The box is
the universal set, $U$, from
[Collections without repeats](tutorial:collections-without-repeats#everything-else-the-complement):
everything we are talking about at the moment, here the 20 members. The
four places are the diagram's *regions*.

Before you run the next cell, guess how many people are in each of the
four regions. The four numbers must add to 20.

The cell draws the diagram. It is the longest cell on this page, and you
do not need to follow every drawing line. What matters is where each
number comes from: every one is `len()` of a set, worked out from the
real sets.

```python exec
id: circles-draw-two
import matplotlib.pyplot as plt


def draw_two(left, right, everyone, left_name, right_name):
    """Draw two circles in a box, with how many are in each of the four regions."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(plt.Rectangle((-2.6, -1.7), 5.2, 3.8, fill=False))
    ax.add_patch(plt.Circle((-0.6, 0), 1.3, fill=False, linewidth=2, color="tab:blue"))
    ax.add_patch(plt.Circle((0.6, 0), 1.3, fill=False, linewidth=2, color="tab:orange"))
    ax.text(-1.2, 0, len(left - right), fontsize=16, ha="center", va="center")
    ax.text(0, 0, len(left & right), fontsize=16, ha="center", va="center")
    ax.text(1.2, 0, len(right - left), fontsize=16, ha="center", va="center")
    ax.text(2.2, -1.35, len(everyone - (left | right)), fontsize=16, ha="center")
    ax.text(-1.2, 1.5, left_name, ha="center")
    ax.text(1.2, 1.5, right_name, ha="center")
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-1.8, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")


draw_two(swimmers, cyclists, members, "swim", "cycle")
```

The diagram shows 3 people who swim and do not cycle, 7 who do both, 4
who cycle and do not swim, and 6, in the corner of the box, who do
neither. $3 + 7 + 4 + 6 = 20$, so everyone is somewhere, and nobody is
in two places.

Each region is a set of its own, and each one is a set operation you
already know. The circles are $S$ for swimmers and $C$ for cyclists.

| Region | In words | In symbols | In Python |
|---|---|---|---|
| left only | swim, and do not cycle | $S \setminus C$ | `swimmers - cyclists` |
| the overlap | swim and cycle | $S \cap C$ | `swimmers & cyclists` |
| right only | cycle, and do not swim | $C \setminus S$ | `cyclists - swimmers` |
| outside both | neither | $(S \cup C)'$ | `members - (swimmers \| cyclists)` |

The last row is a complement: everything in the box that is not in
either circle. On
[Collections without repeats](tutorial:collections-without-repeats#everything-else-the-complement)
the complement of $A$, written $A'$, was everything in the universal set
that is not in $A$. In Python it is the box minus the set:
`members - swimmers` is everyone in the club who does not swim.

In a diagram, the complement is the part of the box outside a circle,
so you can see where it lives. The complement of the swimmers is 10
people if the box is the club. If the box were everyone in Ireland, it
would be more than five million people. The same move gives a different
answer in a different space, so a Venn diagram always draws its box.

### Exactly one of the two

Who does exactly one of swimming and cycling, but not both? In the
diagram, that is the two outer parts of the circles together, without
the overlap. It is the symmetric difference from
[Collections without repeats](tutorial:collections-without-repeats#on-one-list-only-difference),
$S \triangle C$, which Python writes `^`:

```python exec
id: circles-exactly-one
print(swimmers ^ cyclists)
print((swimmers | cyclists) - (swimmers & cyclists))
```

Both lines give the same 7 names, perhaps in a different order, since a
set keeps no order. The picture shows why the two lines agree: the
union is all three parts inside the circles, and taking away the
overlap leaves the two outer parts. A name is in `swimmers ^ cyclists`
when exactly one of "swims" and "cycles" is true for them, the
exclusive or of
[True, false and every case](tutorial:true-false-and-every-case#exclusive-or-exactly-one).

### Your turn

1. Change the last line of the drawing cell to draw the cyclists and the
   runners. Before you run it, which region do you think will be the
   biggest?
2. Draw the swimmers and the runners too. Which region is the smallest?
3. In the cell below, print the complement of the runners: everyone in
   the club who does not run. How many names do you expect?

```python exec
id: circles-your-turn-1
# The complement of runners, inside the club
```

## Counting either: inclusion–exclusion

How many members swim or cycle, or both? Here is a first try. Before you
run it, look at the first line and guess whether it is right.

```python exec
id: circles-either-1
print(len(swimmers) + len(cyclists))
print(len(swimmers | cyclists))
```

Adding the two sizes gives 21, which is more than the 20 people in the
whole club. The union has 14. The picture says why. Adding the two
circles counts each circle once, and the 7 people in the overlap are in
both circles, so they were counted twice. To count them once, take the
overlap away once.

The cardinality of a set, $|A|$, is the number of its elements, as on
[Collections without repeats](tutorial:collections-without-repeats#two-playlists).
So $|S| = 10$, and $|S \cap C| = 7$. In words: the number in either set is the number in
the first, plus the number in the second, minus the number in both. In
symbols:

$$|A \cup B| = |A| + |B| - |A \cap B|$$

This is the *inclusion–exclusion principle*, for two sets. The name says
what it does: include each set, then exclude what was counted twice. For
the club it gives $10 + 11 - 7 = 14$.

It also counts the fourth region, outside both circles, without looking
at a single name: $20 - 14 = 6$.

A rule that holds for one club is not yet a rule for every pair of sets.
Let's test it on a thousand pairs. `random.sample(values, k)` picks `k`
different values from `values`, so each set below is a random group of
people, numbered from 1 to 30. Do you expect any pair to break the rule?

```python exec
id: circles-either-2
import random

people = range(1, 31)
broken = 0
for trial in range(1000):
    first = set(random.sample(people, random.randint(0, 30)))
    second = set(random.sample(people, random.randint(0, 30)))
    if len(first | second) != len(first) + len(second) - len(first & second):
        broken = broken + 1
print(broken, "pairs of sets broke the rule")
```

None of them. A thousand checks are not a proof. The picture is the
proof: whichever of the three regions a person stands in, the formula
counts them once. The checks tell us we wrote that idea down correctly.

You have met this rule before, in a different space. On
[Chances that combine](tutorial:chances-that-combine#when-both-can-happen)
it was $P(A \text{ or } B) = P(A) + P(B) - P(A \text{ and } B)$. Divide
every count in the formula by the size of the box, and you have the rule
for chances. When the two circles do not overlap at all, $|A \cap B| = 0$,
and the rule becomes plain adding, as the lunches on
[Counting every outfit](tutorial:counting-every-outfit#and-multiplies-or-adds)
did.

### Your turn

1. On paper, use the formula to find how many members cycle or run, or
   both. You need $|C| = 11$, $|R| = 8$, and $|C \cap R|$ from your
   diagram of cyclists and runners.
2. Check your answer with `len(cyclists | runners)` in the cell above.
3. How many members neither cycle nor run?

## Three circles, eight regions

Now all three questions. A third circle for the runners has to overlap
each of the other two, and it has to overlap the place where those two
already overlap. So the three circles sit in a triangle, and each one
crosses the other two.

How many regions are there now? Count them in your head before you run
the cell, and do not forget the outside.

```python exec
id: circles-draw-three
def draw_three(first, second, third, everyone, names):
    """Draw three circles in a box, with how many are in each of the eight regions."""
    fig, ax = plt.subplots(figsize=(6, 5.5))
    ax.add_patch(plt.Rectangle((-2.6, -2.4), 5.2, 4.9, fill=False))
    for x, y, colour in [(-0.65, 0.45, "tab:blue"), (0.65, 0.45, "tab:orange"), (0, -0.65, "tab:green")]:
        ax.add_patch(plt.Circle((x, y), 1.3, fill=False, linewidth=2, color=colour))
    places = [(-1.2, 0.8, first - second - third), (1.2, 0.8, second - first - third),
              (0, -1.3, third - first - second), (0, 1.0, (first & second) - third),
              (-0.75, -0.25, (first & third) - second), (0.75, -0.25, (second & third) - first),
              (0, 0.1, first & second & third), (2.2, -2.1, everyone - (first | second | third))]
    for x, y, region in places:
        ax.text(x, y, len(region), fontsize=15, ha="center", va="center")
    for x, y, name in [(-1.6, 2.0, names[0]), (1.6, 2.0, names[1]), (0, -2.2, names[2])]:
        ax.text(x, y, name, ha="center")
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.5, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")


draw_three(swimmers, cyclists, runners, members, ["swim", "cycle", "run"])
```

There are eight regions: seven inside the circles, and one outside all
three. Here they are, from the middle out. Write the swimmers, cyclists
and runners as $S$, $C$ and $R$.

| Region | Who stands there | In Python | Count |
|---|---|---|---|
| the middle | all three | `swimmers & cyclists & runners` | 2 |
| swim and cycle, not run | exactly two | `(swimmers & cyclists) - runners` | 5 |
| swim and run, not cycle | exactly two | `(swimmers & runners) - cyclists` | 1 |
| cycle and run, not swim | exactly two | `(cyclists & runners) - swimmers` | 2 |
| swim only | exactly one | `swimmers - cyclists - runners` | 2 |
| cycle only | exactly one | `cyclists - swimmers - runners` | 2 |
| run only | exactly one | `runners - swimmers - cyclists` | 3 |
| outside all three | none | `members - (swimmers \| cyclists \| runners)` | 3 |

The counts add to 20 again. Why eight? Each person answers three yes or
no questions, and each answer can go two ways. That is
$2 \times 2 \times 2 = 8$ ways to answer, and each way of answering is
one region. It is the same count as the eight rows of a truth table with
three inputs, on
[True, false and every case](tutorial:true-false-and-every-case#how-many-rows).
A Venn diagram of three sets is a truth table drawn as a picture.

```question
id: circles-regions-four
type: multiple-choice
correct: 3

A fourth question, "Do you row?", would need a fourth set. How many
regions would a diagram of four sets need?

- 9
- 12
- 16
- 32
```

Sixteen, because $2^4 = 16$. Four round circles cannot make all sixteen
regions, however you move them: some pairs of regions never appear. A
four-set diagram needs ovals or stranger shapes, and that is one reason
Venn diagrams usually stop at three.

### Your turn

1. Tomas runs, and does not swim or cycle. Which region is he in? Find
   his name with `print("Tomas" in runners - swimmers - cyclists)`.
2. Which region is Ciara in? Guess from the sets in the first cell, then
   test your guess the same way.
3. Move Ciara: add `"Ciara"` to `cyclists` in the first cell. Run that
   cell and the drawing again. Which two numbers changed?

```python exec
id: circles-your-turn-3
print("Tomas" in runners - swimmers - cyclists)
```

## Yes to exactly two

Now the club's question. The table has three rows marked "exactly two":
5, 1 and 2 people. So 8 members answered yes to exactly two questions.

That answer came from the regions. Here is a second route, which never
draws a circle. Go through the members one at a time, count the yes
answers each person gave, and keep the ones with exactly two. Before you
run it, which names do you expect?

```python exec
id: circles-exactly-two-1
two_yes = []
for name in sorted(members):
    yes_answers = 0
    for group in [swimmers, cyclists, runners]:
        if name in group:
            yes_answers = yes_answers + 1
    if yes_answers == 2:
        two_yes.append(name)

print(len(two_yes), two_yes)
```

`sorted(members)` gives the names as a list in alphabetical order, so
the loop visits them in the same order every time. The inner loop asks the three questions of
one person. The same eight names come out: the two routes agree.

Now the first route, written in Python. Each "exactly two" region is a
set, and the three regions share no one, so their union holds everyone
who said yes twice.

```python exec
id: circles-exactly-two-2
exactly_two = (((swimmers & cyclists) - runners)
               | ((swimmers & runners) - cyclists)
               | ((cyclists & runners) - swimmers))
print(len(exactly_two))
print(exactly_two == set(two_yes))
```

8, and `True`: the set of names from the regions is the same set as the
names from the loop. Two different methods, one answer. That is the
kind of check this course keeps coming back to.

The loop would work for four questions, or ten, with no change but the
list of groups. The regions give a picture of where everyone stands.

### Your turn

1. The club thinks people who do *at least* two are worth inviting too.
   Change the loop to keep anyone with 2 or more yes answers. How many
   now? Which region did the new names come from?
2. Change it again to find the people who said yes to none. Check your
   answer against the corner of the three-circle diagram.

## Inclusion–exclusion for three sets

How many members said yes to at least one question? The union has the
answer: `len(swimmers | cyclists | runners)`. But a survey report often
gives only the counts, not the names. Can the two-set formula grow to
three?

Start by adding the three circles: $10 + 11 + 8 = 29$. Everyone in an
overlap was counted more than once. So take away the three overlaps of
two circles. Then look at the middle. The table below follows one person
from each kind of region through the steps.

| A person who is in | Added with the circles | Taken away with the pairs | Counted so far |
|---|---|---|---|
| one circle | 1 time | 0 times | 1 |
| exactly two circles | 2 times | 1 time | 1 |
| all three circles | 3 times | 3 times | 0 |

The people in the middle are in every pair, so taking away the pairs
took them away three times. Now they are not counted at all. So we add
the middle back once. In words: add the three sets, take away the three
pairs, and add back the three-way overlap. In symbols:

$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

For the club, the pairs are 7, 3 and 4, and the middle is 2. What does
the formula give? Work it out, then run the cell.

```python exec
id: circles-three-formula-1
by_formula = (len(swimmers) + len(cyclists) + len(runners)
              - len(swimmers & cyclists) - len(swimmers & runners)
              - len(cyclists & runners)
              + len(swimmers & cyclists & runners))
print(by_formula, len(swimmers | cyclists | runners))
```

Both give 17: $29 - 14 + 2 = 17$. And again the space around the circles
comes for free: $20 - 17 = 3$ people said no to everything.

Here is the same random test as before, now with three sets. What do you
expect it to print?

```python exec
id: circles-three-formula-2
broken = 0
for trial in range(1000):
    first = set(random.sample(people, random.randint(0, 30)))
    second = set(random.sample(people, random.randint(0, 30)))
    third = set(random.sample(people, random.randint(0, 30)))
    union_size = len(first | second | third)
    formula = (len(first) + len(second) + len(third)
               - len(first & second) - len(first & third) - len(second & third)
               + len(first & second & third))
    if union_size != formula:
        broken = broken + 1
print(broken, "sets of three broke the rule")
```

Zero again.

## Filling a diagram from the totals

Real surveys rarely give names. A report gives totals, and the question
is what those totals say about the regions. Here is one. It is made up,
with numbers of the size a real one might give.

Sixty people at a Dublin bus stop were asked which of three services
they used last week: bus, Luas, DART.

- 34 used the bus, 25 used the Luas and 18 used the DART.
- 12 used the bus and the Luas, 8 used the bus and the DART, and 6 used
  the Luas and the DART.
- 3 used all three.

How many used exactly two? It is tempting to add $12 + 8 + 6 = 26$.
Before you read on, what is wrong with that?

The 12 who used the bus and the Luas include the 3 who used all three.
So does each of the other pairs. The trick is to fill the diagram from
the middle out, because the middle is the only region we are given on
its own.

1. **The middle:** 3.
2. **Each pair's region without the middle:** bus and Luas only is
   $12 - 3 = 9$. Bus and DART only is $8 - 3 = 5$. Luas and DART only is
   $6 - 3 = 3$.
3. **Each circle's region on its own:** take away everything else inside
   that circle. Bus only is $34 - 9 - 5 - 3 = 17$.
4. **Outside all three:** 60, minus everything inside the circles.

Each step uses only what the steps before it found. That is sequence,
our third question: the order is what makes the puzzle work. Here are
the four steps in Python. Before you run it, work out Luas only and DART
only on paper.

```python exec
id: circles-totals-1
asked = 60
bus, luas, dart = 34, 25, 18
bus_luas, bus_dart, luas_dart = 12, 8, 6
all_three = 3

bus_luas_only = bus_luas - all_three
bus_dart_only = bus_dart - all_three
luas_dart_only = luas_dart - all_three

bus_only = bus - bus_luas_only - bus_dart_only - all_three
luas_only = luas - bus_luas_only - luas_dart_only - all_three
dart_only = dart - bus_dart_only - luas_dart_only - all_three

inside = (all_three + bus_luas_only + bus_dart_only + luas_dart_only
          + bus_only + luas_only + dart_only)
print("only one:", bus_only, luas_only, dart_only)
print("exactly two:", bus_luas_only, bus_dart_only, luas_dart_only)
print("exactly two, together:", bus_luas_only + bus_dart_only + luas_dart_only)
print("at least one:", inside, " none:", asked - inside)
```

The line `bus, luas, dart = 34, 25, 18` names three values at once, in
order: the first name gets the first value. Then the answers: 17, 10 and
7 used only one service; 9, 5 and 3 used exactly two, which makes 17;
54 used at least one, and 6 used none of them.

There are two checks here. The first is the three-set formula:
$34 + 25 + 18 - 12 - 8 - 6 + 3 = 54$, the same as `inside`. The second
is the one that catches most mistakes in a filled diagram: every region
must be 0 or more. If a step gives −2 people, one of the totals was
wrong, or was copied wrongly. A count of people lives in the whole
numbers from 0 up, and a region outside that space is a message about
the data.

### Your turn

1. Look at step 2. Every pair lost the middle once, so "exactly two" is
   $12 + 8 + 6 - 3 \times 3$. Check that this gives 17.
2. Does the same shortcut work for the sports club? Its pairs are 7, 3
   and 4, and its middle is 2. Compare your answer with the 8 from the
   last section.
3. Change `luas_dart` in the cell to 1, and run it again. Which region
   breaks, and what does that tell you about the survey?

<details class="dl-why"><summary>Why this way?</summary>

This page began with names in sets, and drew each diagram from them.
Only at the end did it give totals and ask for the regions. Most
textbooks start the other way: a puzzle of totals, filled in from the
middle out, because that is the question an exam usually asks.

Starting from totals is good practice for that kind of question. It is
also closer to how survey results reach most people, as a report.

We began with names because a region is not a number to begin with. It
is a set of people, and its number comes from counting them. With the
names in hand, every count on the page could be checked against real
sets. The totals puzzle then became a question about sets you had
already seen, not a set of rules for filling in circles.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the universal set, $U$, and each circle's set; every region, which is a set with a name made from set operations, like `(swimmers & cyclists) - runners` |
| What is promised? | inclusion–exclusion promises the size of a union from the sizes of the sets and their overlaps; the loop and the regions promised the same eight names, and kept it |
| What happens when? | the overlaps are taken away after the circles are added, and the middle is added back last; a diagram from totals is filled from the middle out |
| What does this space let us do? | a complement means something only inside a box; three circles make eight regions, and four round circles cannot make sixteen; a region of −2 people says the data is wrong |

## What we have now

| Term | What it means |
|---|---|
| Venn diagram | sets drawn as circles in a box; overlapping circles share members |
| universal set, $U$ | everything we are talking about at the moment: the box |
| region | one part of the diagram; everyone in it gave the same yes and no answers |
| complement, symmetric difference | the box outside a circle; the two outer parts of two circles |
| inclusion–exclusion, two sets | $\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert - \lvert A \cap B \rvert$ |
| inclusion–exclusion, three sets | add the sets, take away the pairs, add back the middle |
| exactly two, from totals | the three pairs added, minus 3 times the middle |
| `random.sample(values, k)` | picks `k` different values from `values` |

The practice page is next, and after it the mixed problems for this
unit, where everything in Unit 5 meets in one report on real data.

For another route through the same ideas, the integrated course has
[Venn diagrams: drawing sets and their overlaps](tutorial:venn-diagrams).
