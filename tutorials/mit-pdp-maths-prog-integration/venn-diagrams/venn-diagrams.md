---
title: "Drawing Sets"
slug: venn-diagrams
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: data-chance-and-logic
version: 2026.08.23.1
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

# Drawing Sets

**Maths for IT**

Two overlapping circles with numbers in them. You have almost certainly seen one, and you may have been asked to fill one in at school.

This tutorial is short, and it is not really about the diagram. It is about the point at which a set expression stops fitting in your head, and about having something to reach for when that happens.

In *Sets as Sorted Lists* you built union, intersection and difference and used them on real data. Everything here is drawn from those. **No new operations, and nothing new to define** — a Venn diagram is a plot of things you already computed.

## Two Circles, from Real Sets

Here are two sets of students: the ones who own a bike, and the ones who own a car.

```python exec
id: two-circles-from-real-sets-1
import matplotlib.pyplot as plt

bike = {"Aoife", "Ben", "Cara", "Dara", "Eoin"}
car = {"Cara", "Dara", "Fiona", "Gearoid"}


def draw_two(left, right, left_name, right_name):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(plt.Circle((-0.5, 0), 1.3, fill=False, linewidth=2))
    ax.add_patch(plt.Circle((0.5, 0), 1.3, fill=False, linewidth=2))

    only_left = left - right
    only_right = right - left
    both = left & right

    ax.text(-1.3, 0, str(len(only_left)), ha="center", fontsize=16)
    ax.text(0, 0, str(len(both)), ha="center", fontsize=16)
    ax.text(1.3, 0, str(len(only_right)), ha="center", fontsize=16)
    ax.text(-1.3, 1.5, left_name, ha="center")
    ax.text(1.3, 1.5, right_name, ha="center")

    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-1.8, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


draw_two(bike, car, "bike", "car")
```

Three numbers, and every one of them came out of a set operation. Nothing was placed by hand.

That is the thing to hold onto. **The diagram is output.** It is drawn from the sets, so it cannot disagree with them, and if you change the data the picture changes with it.

```python exec
id: two-circles-from-real-sets-2
# Sets that do not overlap at all.
draw_two({"Aoife", "Ben"}, {"Cara", "Dara", "Eoin"}, "cyclists", "drivers")
```

```python exec
id: two-circles-from-real-sets-3
# One set entirely inside the other.
draw_two({"Aoife", "Ben", "Cara"}, {"Aoife", "Ben"}, "students", "first years")
```

The picture changed; the code did not. The middle number going to zero, or one of the outer ones going to zero, is the diagram telling you something true about the sets rather than the drawing being wrong.

## The Regions Have Names You Already Know

Three regions, three operations you wrote a fortnight ago.

| Region | Operation | Python |
|---|---|---|
| Only in the left circle | difference | `bike - car` |
| The overlap | intersection | `bike & car` |
| Only in the right circle | difference the other way | `car - bike` |
| All three together | union | `bike \| car` |

```python exec
id: the-regions-have-names-you-already-know-1
bike = {"Aoife", "Ben", "Cara", "Dara", "Eoin"}
car = {"Cara", "Dara", "Fiona", "Gearoid"}

print("bike - car :", sorted(bike - car))
print("bike & car :", sorted(bike & car))
print("car - bike :", sorted(car - bike))
print("bike | car :", sorted(bike | car))
```

Nothing new is being defined here. The diagram is giving the operations from *Sets as Sorted Lists* somewhere to sit.

### Your turn

Using the two sets above, how would you write the expression for each of these? Check what it gives.

- People who own exactly one of the two (a bike or a car, but not both).
- People who own neither, given that everybody in the class is `{"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona", "Gearoid", "Hannah"}`.

```python exec
id: your-turn-1
everyone = {"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona", "Gearoid", "Hannah"}

# exactly_one = ...
# neither = ...
```

The first of those is exclusive or, which you met in [Logic and Truth](tutorial:logic-and-truth) as a fact about true and false. Python spells it `^` for sets too, and for the same reason.

## Three Sets, Which Is Where It Earns Its Place

Two sets are easy to hold in your head. You can work out `bike − car` without drawing anything.

Three is where that stops.

```python exec
id: three-sets-which-is-where-it-earns-its-place-1
import matplotlib.pyplot as plt

python = {"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona"}
sql = {"Cara", "Dara", "Eoin", "Gearoid", "Hannah"}
javascript = {"Dara", "Eoin", "Fiona", "Hannah", "Iarla"}


def draw_three(a, b, c, names):
    fig, ax = plt.subplots(figsize=(6, 5.5))
    centres = [(-0.6, 0.35), (0.6, 0.35), (0, -0.7)]
    for (x, y) in centres:
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


draw_three(python, sql, javascript, ["Python", "SQL", "JavaScript"])
```

Seven regions now, and each one is a different combination of in and out. Try holding all seven in your head at once -- most people cannot, and there is no reason they should.

Here is a question that is genuinely awkward in symbols and easy on the picture: **who knows Python or SQL, but not JavaScript?**

```python exec
id: three-sets-which-is-where-it-earns-its-place-2
print(sorted((python | sql) - javascript))
```

Find those people on the diagram above. They are the two top regions and the one between them, and not the bottom circle. Now try to convince yourself of the same answer from the expression alone.

### Your turn

Two expressions that look different. Are they the same set? Predict from the picture first, then check.

```python exec
id: your-turn-2
first = (python & sql) | (python & javascript)
second = python & (sql | javascript)

# Your prediction as a comment, then:
# print(first == second)
```

## The Same Laws, in a Different Notation

In *Logic and Truth* you proved De Morgan's Laws by looping over four rows. Here they are again, shaded.

```python exec
id: the-same-laws-in-a-different-notation-1
everyone = set(range(1, 13))
a = {1, 2, 3, 4, 5, 6}
b = {5, 6, 7, 8, 9}

def complement(s):
    return everyone - s


print("not (A or B):        ", sorted(complement(a | b)))
print("(not A) and (not B): ", sorted(complement(a) & complement(b)))
print()
print("not (A and B):       ", sorted(complement(a & b)))
print("(not A) or (not B):  ", sorted(complement(a) | complement(b)))
```

Identical, both times.

*Logic and Truth* proved this by checking four rows. That proof is complete -- there really are only four cases. This one is a different kind of thing: you can *see* that the region outside both circles is the same region as the overlap of the two outsides, and once you have seen it you do not need to check.

**Neither proof is better.** They are the same claim in two notations, which is exactly why the pairing is worth having. If the truth table version did not land, this one might, and they are not two facts to learn.

## Where the Picture Stops Helping

One more thing, and it is the most interesting item in the tutorial.

Three circles give seven regions, which is every combination of in and out for three sets. Four sets would need fifteen. **Four circles cannot do it.**

```python exec
id: where-the-picture-stops-helping-1
from itertools import combinations

for n in (2, 3, 4, 5):
    print(f"{n} sets need {2 ** n - 1} regions")
```

That is not a limitation of the drawing code. It is a fact about circles in a plane: no arrangement of four of them produces all fifteen regions. Diagrams for four sets exist, but they use ellipses or stranger shapes and stop being readable, which rather defeats the purpose.

Meanwhile the set operations keep working perfectly for four sets, or forty.

**Every representation runs out somewhere, and knowing where is part of knowing it.** A picture that helps enormously at three and not at all at four is still a good tool — you just have to know which of those you are holding.

## Reflection

The diagram is not a notation to learn. It is a plot of set operations you already had, and its job is to take over at the point where the expressions stop fitting in your head.

Three things.

**It is drawn from the data**, so it cannot lie about the data. Change the sets and the picture changes.

**Two sets rarely need it; three often do.** That is the size at which it earns its place.

**It runs out at four.** Not because the drawing is bad, but because of a fact about circles — and the operations carry on regardless.

In a few sentences, think of three overlapping groups you belong to. Which regions of that diagram have people in them, and which are empty?

## Where to Read More

Khan Academy. *Visualising Set Operations Using Venn Diagrams.*
<https://www.youtube.com/watch?v=c6TY6fVUlDQ>. The same two-circle
pictures this page draws from real data, drawn by hand instead.

Khan Academy. *Properties of Set Operations Using Venn Diagrams.*
<https://www.youtube.com/watch?v=lWjmbch870g>. De Morgan's Laws shaded on
a diagram, which is exactly where this page ends up.
