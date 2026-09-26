---
title: "Circles that overlap: Venn diagrams"
year: "2026-2027"
version: 2026.09.25.1
covers:
  two-circles-in-a-box:
    covers: [MIT-2.3]
    touches: [MIT-2.2]
  counting-either-inclusion-exclusion:
    covers: [MIT-2.3]
    touches: [MIT-5.8]
  three-circles-eight-regions:
    covers: [MIT-2.3]
  exactly-two-of-the-three:
    covers: [MIT-2.3]
    touches: [PDP-LO6]
  inclusion-exclusion-for-three-sets:
    covers: [MIT-2.3]
  filling-a-diagram-from-the-totals:
    covers: [MIT-2.3]
---

# Circles that overlap: Venn diagrams

A college's IT team checks 20 laptops for three things that keep a
laptop safe. Are its *updates* installed: the new versions of its
software that close known security holes? Does it run *antivirus*
software, a program that looks for harmful programs? Is its work
*backed up*, with a copy kept somewhere else? This week the team has
time to fix the laptops that are one step away from all three. How
many laptops have exactly two of the three?

Three yes-or-no questions, twenty laptops. It sounds like a job for a
pencil. It turns out to be a job for three circles, and the circles
turn out to be a truth table in disguise.

On this page we:

- draw two sets as two circles in a box, and name every region
- count the laptops in either circle, without counting any twice
- draw three circles, and find all eight of their regions
- answer the team's question in two different ways, and check that
  they agree
- fill in a diagram from a report's totals alone, when nobody gives us
  the names

> **The space we're in.** Sets of names, from
> [Collections without repeats](tutorial:collections-without-repeats):
> a set holds each value once, in no order, and Python works out unions,
> intersections and differences for us. Every set on this page sits
> inside one universal set, here the laptops that were checked. That
> usually goes unsaid in a report, and it matters: "every laptop without
> backups" means nothing until we say every laptop out of which. Every
> check on this page is made up, so that the numbers stay small enough
> to check by eye.

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
answer: 3

On one roll of a die, "even" has chance $\frac{3}{6}$ and "more than 4"
has chance $\frac{2}{6}$. The chance of "even or more than 4" is not
$\frac{5}{6}$. Why not?

- A die cannot be even and more than 4 at the same time.
  - A 6 is both even and more than 4, so the two can happen together.
- Chances are multiplied, not added.
  - Multiplying is for both happening; 'or' needs adding, with care for the overlap.
- The 6 is in both events, so adding counts it twice.
  - 6 is even and more than 4, so it sits in both events and is counted twice.
```

## Two circles in a box

Here are the team's findings, as three sets. Each laptop is named after
the person who uses it. Each set holds the laptops that passed one
check. The fourth set, `laptops`, is every laptop that was checked.

```python exec
id: circles-laptops-1
updated = {"Aoife", "Hassan", "Ben", "Isla", "Rory", "Priya", "Wei",
           "Ciara", "Eoin", "Maeve"}
antivirus = {"Aoife", "Hassan", "Ben", "Isla", "Rory", "Priya", "Wei",
             "Dmitri", "Kate", "Fatima", "Liam"}
backed_up = {"Aoife", "Hassan", "Ciara", "Dmitri", "Kate", "Grainne",
             "Sadhbh", "Tomas"}
laptops = updated | antivirus | backed_up | {"Jakub", "Niamh", "Oisin"}

print(len(laptops), "laptops")
print(len(updated), "updated,", len(antivirus), "with antivirus,", len(backed_up), "backed up")
```

Twenty laptops. 10 are updated, 11 have antivirus and 8 are backed up,
and $10 + 11 + 8 = 29$, which is more than 20. Some laptops must be in
more than one set. A list of names hides that. A picture shows it.

Let's start with two of the checks: updates and antivirus. Draw a box
for every laptop that was checked. Inside it, draw one circle for the
updated laptops and one for those with antivirus, and let the circles
overlap. Every laptop now stands in exactly one of four places: only in
the updates circle, in both circles, only in the antivirus circle, or
outside both.

A *Venn diagram* is a picture of sets as circles inside a box, where
each circle holds one set, and where two circles overlap the sets share
members. It is named after John Venn, an English mathematician who
drew them in 1880. The box is
the universal set, $U$, from
[Collections without repeats](tutorial:collections-without-repeats#everything-else-the-complement):
everything we are talking about at the moment, here the 20 laptops. The
four places are the diagram's *regions*.

<aside class="dl-note" id="circles-note-venn">

**Venn in glass.** John Venn taught at Gonville and Caius College, in
Cambridge. The college remembers him with a stained-glass window in its
dining hall: three coloured circles, overlapping, in the shape of his
diagram.

</aside>

Before you run the next cell, guess how many laptops are in each of the
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


draw_two(updated, antivirus, laptops, "updates", "antivirus")
```

The diagram shows 3 laptops that are updated and have no antivirus, 7
that have both, 4 with antivirus and no updates, and 6, in the corner
of the box, with neither. $3 + 7 + 4 + 6 = 20$, so every laptop is
somewhere, and none is in two places.

Each region is a set of its own, and each one is a set operation you
already know. The circles are $U_p$ for updated and $A$ for antivirus.
(We cannot call the updated laptops $U$: that letter already names the
box.)

| Region | In words | In symbols | In Python |
|---|---|---|---|
| left only | updated, no antivirus | $U_p \setminus A$ | `updated - antivirus` |
| the overlap | updated and antivirus | $U_p \cap A$ | `updated & antivirus` |
| right only | antivirus, not updated | $A \setminus U_p$ | `antivirus - updated` |
| outside both | neither | $(U_p \cup A)'$ | `laptops - (updated \| antivirus)` |

The last row is a complement: everything in the box that is not in
either circle. On
[Collections without repeats](tutorial:collections-without-repeats#everything-else-the-complement)
the complement of $A$, written $A'$, was everything in the universal set
that is not in $A$. In Python it is the box minus the set:
`laptops - updated` is every laptop that still needs its updates.

In a diagram, the complement is the part of the box outside a circle,
so you can see where it lives. The complement of the updated laptops is
10 laptops if the box is this room. If the box were every laptop in
Ireland, it would be millions. The same move gives a different answer
in a different space, so a Venn diagram always draws its box.

### Exactly one of the two

Which laptops have exactly one of updates and antivirus, but not both?
In the
diagram, that is the two outer parts of the circles together, without
the overlap. It is the symmetric difference from
[Collections without repeats](tutorial:collections-without-repeats#on-one-list-only-difference),
$S \triangle C$, which Python writes `^`:

```python exec
id: circles-exactly-one
print(updated ^ antivirus)
print((updated | antivirus) - (updated & antivirus))
```

Both lines give the same 7 names, perhaps in a different order, since a
set keeps no order. The picture shows why the two lines agree: the
union is all three parts inside the circles, and taking away the
overlap leaves the two outer parts. A name is in `updated ^ antivirus`
when exactly one of "updated" and "has antivirus" is true for it, the
exclusive or of
[True, false and every case](tutorial:true-false-and-every-case#exclusive-or-exactly-one).

### Your turn

1. Change the last line of the drawing cell to draw antivirus and
   backups. Before you run it, which region do you think will be the
   biggest?
2. Draw updates and backups too. Which region is the smallest?
3. In the cell below, print the complement of `backed_up`: every laptop
   whose work is not backed up. How many names do you expect?

```python exec
id: circles-your-turn-1
# The complement of backed_up, inside the box of laptops
```

## Counting either: inclusion-exclusion

How many laptops are updated or have antivirus, or both? Here is a
first try. Before you
run it, look at the first line and guess whether it answers that
question.

```python exec
id: circles-either-1
print(len(updated) + len(antivirus))
print(len(updated | antivirus))
```

Adding the two sizes gives 21, which is more than the 20 laptops in the
whole room. The union has 14. The picture says why. Adding the two
circles counts each circle once, and the 7 laptops in the overlap are
in both circles, so they were counted twice. To count them once, take the
overlap away once.

The cardinality of a set, $|A|$, is the number of its elements, as on
[Collections without repeats](tutorial:collections-without-repeats#two-playlists).
So $|U_p| = 10$, and $|U_p \cap A| = 7$. In words: the number in either set is the number in
the first, plus the number in the second, minus the number in both. In
symbols:

$$|A \cup B| = |A| + |B| - |A \cap B|$$

This is the *inclusion–exclusion principle*, for two sets. The name says
what it does: include each set, then exclude what was counted twice. For
the laptops it gives $10 + 11 - 7 = 14$.

It also counts the fourth region, outside both circles, without looking
at a single name: $20 - 14 = 6$.

A rule that holds for one room of laptops is not yet a rule for every
pair of sets. Let's test it on a thousand pairs. `random.sample(values,
k)` picks `k` different values from `values`, so each set below is a
random group of things, numbered from 1 to 30. Do you expect any pair to break the rule?

```python exec
id: circles-either-2
import random

things = range(1, 31)
broken = 0
for trial in range(1000):
    first = set(random.sample(things, random.randint(0, 30)))
    second = set(random.sample(things, random.randint(0, 30)))
    if len(first | second) != len(first) + len(second) - len(first & second):
        broken = broken + 1
print(broken, "pairs of sets broke the rule")
```

None of them. A thousand checks are not a proof. The picture is the
proof: whichever of the three regions a laptop stands in, the formula
counts it once. The checks tell us the code says the same as that idea.

You have met this rule before, in a different space. On
[Chances that combine](tutorial:chances-that-combine#when-both-can-happen)
it was $P(A \text{ or } B) = P(A) + P(B) - P(A \text{ and } B)$. Divide
every count in the formula by the size of the box, and you have the rule
for chances. When the two circles do not overlap at all, $|A \cap B| = 0$,
and the rule becomes plain adding, as the lunches on
[Counting every outfit](tutorial:counting-every-outfit#and-multiplies-or-adds)
did.

### Your turn

1. On paper, use the formula to find how many laptops have antivirus or
   backups, or both. Write $B$ for the backed-up laptops. You need
   $|A| = 11$, $|B| = 8$, and $|A \cap B|$
   from your diagram of antivirus and backups.
2. Check your answer with `len(antivirus | backed_up)` in the cell above.
3. How many laptops have neither?

## Three circles, eight regions

Now all three checks. A third circle for the backups has to overlap
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


draw_three(updated, antivirus, backed_up, laptops, ["updates", "antivirus", "backups"])
```

There are eight regions: seven inside the circles, and one outside all
three. Here they are, from the middle out.

| Region | Which laptops | In Python | Count |
|---|---|---|---|
| the middle | all three | `updated & antivirus & backed_up` | 2 |
| updates and antivirus, no backup | exactly two | `(updated & antivirus) - backed_up` | 5 |
| updates and backup, no antivirus | exactly two | `(updated & backed_up) - antivirus` | 1 |
| antivirus and backup, not updated | exactly two | `(antivirus & backed_up) - updated` | 2 |
| updates only | exactly one | `updated - antivirus - backed_up` | 2 |
| antivirus only | exactly one | `antivirus - updated - backed_up` | 2 |
| backup only | exactly one | `backed_up - updated - antivirus` | 3 |
| outside all three | none | `laptops - (updated \| antivirus \| backed_up)` | 3 |

The counts add to 20 again. Why eight? Each laptop gets three yes or no
answers, and each answer can go two ways. That is
$2 \times 2 \times 2 = 8$ ways to answer, and each way of answering is
one region. It is the same count as the eight rows of a truth table with
three inputs, on
[True, false and every case](tutorial:true-false-and-every-case#how-many-rows).
A Venn diagram of three sets is a truth table drawn as a picture. I
think that is the nicest surprise on this page: two tools from two
different units turn out to be one idea.

```question
id: circles-regions-four
type: multiple-choice
answer: 3

A fourth check, "Is the disk encrypted?", would need a fourth set. How many
regions would a diagram of four sets need?

- 9
  - This is three circles' 8 regions, plus one.
- 12
  - This adds 4 more regions to 8, rather than doubling.
- 16
  - Each new set splits every region in two: 2 × 2 × 2 × 2.
- 32
  - This doubles once more than there are sets.
```

Sixteen, because $2^4 = 16$. Four round circles cannot make all sixteen
regions, however you move them: some pairs of regions never appear. A
four-set diagram needs ovals or stranger shapes, and that is one reason
Venn diagrams usually stop at three.

### Your turn

1. Tomas's laptop is backed up, and has no updates and no antivirus.
   Which region is it in? Check with
   `print("Tomas" in backed_up - updated - antivirus)`.
2. Which region is Ciara's laptop in? Guess from the sets in the first
   cell, then test your guess the same way.
3. Fix Ciara's laptop: add `"Ciara"` to `antivirus` in the first cell.
   Run that cell and the drawing again. Which two numbers changed?

```python exec
id: circles-your-turn-3
print("Tomas" in backed_up - updated - antivirus)
```

## Exactly two of the three

Now the team's question. The table has three rows marked "exactly two":
5, 1 and 2 laptops. So 8 laptops are one fix away from all three.

That answer came from the regions. Here is a second route, which never
draws a circle. Go through the laptops one at a time, count the checks
each one passed, and keep the ones with exactly two. Before you run it,
which names do you expect?

```python exec
id: circles-exactly-two-1
two_yes = []
for name in sorted(laptops):
    yes_answers = 0
    for group in [updated, antivirus, backed_up]:
        if name in group:
            yes_answers = yes_answers + 1
    if yes_answers == 2:
        two_yes.append(name)

print(len(two_yes), two_yes)
```

`sorted(laptops)` gives the names as a list in alphabetical order, so
the loop visits them in the same order every time. The inner loop asks
the three questions of one laptop. The same eight names come out: the
two routes agree.

Now the first route, written in Python. Each "exactly two" region is a
set, and the three regions share no one, so their union holds everyone
who said yes twice.

```python exec
id: circles-exactly-two-2
exactly_two = (((updated & antivirus) - backed_up)
               | ((updated & backed_up) - antivirus)
               | ((antivirus & backed_up) - updated))
print(len(exactly_two))
print(exactly_two == set(two_yes))
```

8, and `True`: the set of names from the regions is the same set as the
names from the loop. Two different methods, one answer. That is the
kind of check this course keeps coming back to.

The loop would work for four checks, or ten, with no change but the
list of groups. The regions give a picture of where every laptop
stands.

### Your turn

1. The team wants a list of every laptop with *at least* two. Change the
   loop to keep any laptop with 2 or more yes answers. How many now?
   Which region did the new names come from?
2. Change it again to find the laptops with none of the three: the most
   urgent ones. Check your answer against the corner of the
   three-circle diagram.

## Inclusion-exclusion for three sets

How many laptops passed at least one check? The union has the answer:
`len(updated | antivirus | backed_up)`. But a report often gives only
the counts, not the names. Can the two-set formula grow to
three?

Start by adding the three circles: $10 + 11 + 8 = 29$. Everyone in an
overlap was counted more than once. So take away the three overlaps of
two circles. Then look at the middle. The table below follows one laptop
from each kind of region through the steps.

| A laptop that is in | Added with the circles | Taken away with the pairs | Counted so far |
|---|---|---|---|
| one circle | 1 time | 0 times | 1 |
| exactly two circles | 2 times | 1 time | 1 |
| all three circles | 3 times | 3 times | 0 |

The laptops in the middle are in every pair, so taking away the pairs
took them away three times. Now they are not counted at all. So we add
the middle back once. In words: add the three sets, take away the three
pairs, and add back the three-way overlap. In symbols:

$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

For the laptops, the pairs are 7, 3 and 4, and the middle is 2. What
does the formula give? Work it out, then run the cell.

```python exec
id: circles-three-formula-1
by_formula = (len(updated) + len(antivirus) + len(backed_up)
              - len(updated & antivirus) - len(updated & backed_up)
              - len(antivirus & backed_up)
              + len(updated & antivirus & backed_up))
print(by_formula, len(updated | antivirus | backed_up))
```

Both give 17: $29 - 14 + 2 = 17$. And again the space around the circles
comes for free: $20 - 17 = 3$ laptops failed every check.

Here is the same random test as before, now with three sets. What do you
expect it to print?

```python exec
id: circles-three-formula-2
broken = 0
for trial in range(1000):
    first = set(random.sample(things, random.randint(0, 30)))
    second = set(random.sample(things, random.randint(0, 30)))
    third = set(random.sample(things, random.randint(0, 30)))
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

Real reports rarely give names. They give totals, and the question is
what those totals say about the regions. Here is one, for the 60
laptops in a whole college building. It is made up, with numbers of the
size a real one might give.

- 34 are updated, 25 have antivirus and 18 are backed up.
- 12 have updates and antivirus, 8 have updates and backups, and 6 have
  antivirus and backups.
- 3 have all three.

How many have exactly two? It is tempting to add $12 + 8 + 6 = 26$.
Before you read on, what is the catch?

The 12 with updates and antivirus include the 3 that have all three.
So does each of the other pairs. The trick is to fill the diagram from
the middle out, because the middle is the only region we are given on
its own.

1. **The middle:** 3.
2. **Each pair's region without the middle:** updates and antivirus
   only is $12 - 3 = 9$. Updates and backups only is $8 - 3 = 5$.
   Antivirus and backups only is $6 - 3 = 3$.
3. **Each circle's region on its own:** take away everything else inside
   that circle. Updates only is $34 - 9 - 5 - 3 = 17$.
4. **Outside all three:** 60, minus everything inside the circles.

Each step uses only what the steps before it found. That is sequence,
our third question: the order is what makes the puzzle work. Here are
the four steps in Python. Before you run it, work out antivirus only
and backups only on paper.

```python exec
id: circles-totals-1
checked = 60
updates, antivirus_total, backups = 34, 25, 18
updates_antivirus, updates_backups, antivirus_backups = 12, 8, 6
all_three = 3

updates_antivirus_only = updates_antivirus - all_three
updates_backups_only = updates_backups - all_three
antivirus_backups_only = antivirus_backups - all_three

updates_only = updates - updates_antivirus_only - updates_backups_only - all_three
antivirus_only = antivirus_total - updates_antivirus_only - antivirus_backups_only - all_three
backups_only = backups - updates_backups_only - antivirus_backups_only - all_three

pairs_only = updates_antivirus_only + updates_backups_only + antivirus_backups_only
inside = all_three + pairs_only + updates_only + antivirus_only + backups_only
print("only one:", updates_only, antivirus_only, backups_only)
print("exactly two:", updates_antivirus_only, updates_backups_only, antivirus_backups_only)
print("exactly two, together:", pairs_only)
print("at least one:", inside, " none:", checked - inside)
```

The line `updates, antivirus_total, backups = 34, 25, 18` names three
values at once, in order: the first name gets the first value. (The
name `antivirus` is already the set from the first cell, so the total
gets a name of its own.) Then the answers: 17, 10 and 7 laptops have
only one; 9, 5 and 3 have exactly two, which makes 17; 54 have at least
one, and 6 have none of them.

There are two checks here. The first is the three-set formula:
$34 + 25 + 18 - 12 - 8 - 6 + 3 = 54$, the same as `inside`. The second
is the one that catches most miscounts in a filled diagram: every region
must be 0 or more. If a step gives −2 laptops, one of the totals was
miscounted, or copied down with a slip. A count of laptops lives in the
whole numbers from 0 up, and a region outside that space is a message
about the data.

### Your turn

1. Look at step 2. Every pair lost the middle once, so "exactly two" is
   $12 + 8 + 6 - 3 \times 3$. Check that this gives 17.
2. Does the same shortcut work for the 20 laptops? Their pairs are 7, 3
   and 4, and their middle is 2. Compare your answer with the 8 from
   the last section.
3. Change `antivirus_backups` in the cell to 1, and run it again. Which
   region breaks, and what does that tell you about the report?

<details class="dl-why"><summary>Why this way?</summary>

This page began with laptops' names in sets, and drew each diagram
from them.
Only at the end did it give totals and ask for the regions. Most
textbooks start the other way: a puzzle of totals, filled in from the
middle out, because that is the question an exam usually asks.

Starting from totals is good practice for that question, and it is how
survey and audit results reach most people.

We began with names because a region is not a number to begin with. It
is a set of laptops, and its number comes from counting them. With the
names in hand, every count on the page could be checked against real
sets. The totals puzzle then became a question about sets you had
already seen, not a set of rules for filling in circles.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the universal set, $U$, and each circle's set; every region, which is a set with a name made from set operations, like `(updated & antivirus) - backed_up` |
| What is promised? | inclusion–exclusion promises the size of a union from the sizes of the sets and their overlaps; the loop and the regions promised the same eight names, and kept it |
| What happens when? | the overlaps are taken away after the circles are added, and the middle is added back last; a diagram from totals is filled from the middle out |
| What does this space let us do? | a complement means something only inside a box; three circles make eight regions, and four round circles cannot make sixteen; a region of −2 laptops says the data has a slip in it |

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

## Where to read more

Patrick J (2017). *The Principle of Inclusion Exclusion: Basic Example.*
<https://www.youtube.com/watch?v=Xd2ZGvMqXsc>. One worked example of
counting "either" by adding the two circles and taking away the overlap.
About seven minutes.
