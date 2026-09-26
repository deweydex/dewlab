---
title: "Venn diagrams: drawing sets and their overlaps"
year: "2026-2027"
version: 2026.09.25.1
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

You have probably seen two overlapping circles with numbers in them.
You may even have filled one in at school. A *Venn diagram* is a picture
of sets: each set is a circle, and the circles overlap where the sets
share elements.

This page is short, and the diagram itself is not the main point. The
main point is that at some size, a set expression no longer fits in
your head. When that happens, a picture helps.

In [Sets: building them from sorted lists](tutorial:sets-as-sorted-lists)
we built union, intersection and difference ourselves. In
[Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth)
we met Python's own `set` type, with `|` for union, `&` for intersection
and `-` for difference. Everything on this page is drawn from those
operations. A Venn diagram is a plot of things you can already compute.
There are no new operations here.

On this page we:

- draw a two-circle diagram from real sets
- match each region of the diagram to an operation we know
- move to three sets, where the picture starts to help
- see De Morgan's laws again, on the diagram
- find the point where circles stop working

## Two circles, from real sets

Here are two sets of students: the ones who own a bike, and the ones who
own a car. The function `draw_two()` counts how many students are in
each region, and then draws the circles.

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

There are three numbers, and every one of them came from a set
operation. Nobody placed them by hand.

Remember this idea. The diagram is output. It is drawn from
the sets, so it cannot disagree with them. If you change the data, the
picture changes with it.

What do you think the diagram will look like for two sets with no
students in common? What about one set that sits completely inside the
other? Run the next two cells to check.

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

The picture changed, but the code did not. Sometimes the middle number
goes to zero, or one of the outer numbers does. The drawing has not gone
wrong. The diagram tells you something true about the sets.

## The regions have names you already know

Each region of the diagram matches an operation from the sets page:

| Region | Operation | Python |
|---|---|---|
| Only in the left circle | difference | `bike - car` |
| The overlap | intersection | `bike & car` |
| Only in the right circle | difference the other way | `car - bike` |
| All three regions together | union | `bike \| car` |

Can you predict who is in each region, from the two sets above? Run the
cell to check.

```python exec
id: the-regions-have-names-you-already-know-1
bike = {"Aoife", "Ben", "Cara", "Dara", "Eoin"}
car = {"Cara", "Dara", "Fiona", "Gearoid"}

print("bike - car :", sorted(bike - car))
print("bike & car :", sorted(bike & car))
print("car - bike :", sorted(car - bike))
print("bike | car :", sorted(bike | car))
```

We have not defined anything new here. The diagram gives each operation
from the sets page a place on the picture.

### Your turn

Use the two sets above. How would you write an expression for each of
these groups?

1. The people who own exactly one of the two: a bike or a car, but not
   both.
2. The people who own neither. For this one you need the whole class,
   which is `{"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona", "Gearoid", "Hannah"}`.
   The cell stores it as `everyone`.
3. Run each expression, and check that the result matches the diagram.

```python exec
id: your-turn-1
everyone = {"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona", "Gearoid", "Hannah"}

# exactly_one = ...
# neither = ...
```

The first group is exclusive or. You met it in
[Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth)
as a fact about true and false. Python writes it `^` for sets too, for
the same reason.

## Three sets, which is where it earns its place

With two sets, you can keep the picture in your head. You can find
`bike - car` without drawing anything.

With three sets, that stops working. Here are three sets of students:
the ones who know Python, the ones who know SQL, and the ones who know
JavaScript.

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

Now there are seven regions. Each one is a different combination of in
or out for each circle. Try to hold all seven in your head at once. Most people cannot, and there is no reason they should.

Here is a question that is awkward in symbols but easy on the picture:
who knows Python or SQL, but not JavaScript? Before you run the cell,
which regions of the diagram do you think hold those people?

```python exec
id: three-sets-which-is-where-it-earns-its-place-2
print(sorted((python | sql) - javascript))
```

Find those four people on the diagram. They are in the two top regions,
and in the region between those two, and nowhere in the bottom circle.
Now try to convince yourself of the same answer from the expression
alone. Which way was easier?

### Your turn

Here are two expressions that look different. Do they give the same set?

1. Look at the diagram, and predict the answer. Write your prediction as
   a comment.
2. Remove the `#` from the `print` line, and run the cell to check.

```python exec
id: your-turn-2
first = (python & sql) | (python & javascript)
second = python & (sql | javascript)

# Your prediction as a comment, then:
# print(first == second)
```

## The same laws, in a different notation

In [Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth)
we proved De Morgan's laws by looping over four rows. Here they are
again, on sets. As you read the output, picture the two-circle diagram:
which region does each line describe?

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

The two lines in each pair are the same.

The logic page proved this by checking four rows. That proof is
complete, because there are only four cases. The diagram gives a
different kind of proof. You can *see* that the region outside both
circles is the same region as the overlap of the two outsides. Once you
have seen it, you do not need to check.

Neither proof is better than the other. They are the same claim in two
notations, and that is why it helps to have both. If the truth table
version did not make sense to you, this one might. And they are one
fact, not two facts to learn.

## Where the picture stops helping

There is one more thing, and it is the most interesting idea on the
page.

Three circles give seven regions. That is every combination of in and
out for three sets, apart from "in none of them", which is the space
outside all the circles. In general, $n$ sets need $2^n - 1$ regions
inside the circles. For three sets that is $2^3 - 1 = 7$. How many
regions do you expect four sets to need? Run the cell to check.

```python exec
id: where-the-picture-stops-helping-1
for n in (2, 3, 4, 5):
    print(f"{n} sets need {2 ** n - 1} regions")
```

Four sets need fifteen regions, and four circles cannot make them. This
is a fact about circles on a flat page. It is not a weakness of the
drawing code. No arrangement of four circles produces all fifteen
regions. Diagrams for four sets do exist, but they use ovals or stranger
shapes, and they get much harder to read. Then they no longer help.

Meanwhile, the set operations keep working perfectly, for four sets or
for forty.

Every way of showing an idea stops working at some point. A Venn diagram
helps a lot with three sets and not at all with four, and it is still a
good tool. You need to know which of the two cases you are in.

## Reflection

A Venn diagram is a plot of set operations you already had. It is not a
new notation to learn. It helps at the point where the expressions no
longer fit in your head.

Here are three things to remember:

- **It is drawn from the data**, so it cannot lie about the data. Change
  the sets, and the picture changes.
- **Two sets rarely need it, and three often do.** Three sets is the
  size where it becomes useful.
- **It stops working at four**, because of a fact about circles, not
  because the drawing is bad. The set operations continue to work.

Think of three overlapping groups that you belong to. In a few
sentences, say which regions of their diagram have people in them, and
which are empty.

## Where to read more

Khan Academy. *Visualising Set Operations Using Venn Diagrams.*
<https://www.youtube.com/watch?v=c6TY6fVUlDQ>. It shows the same
two-circle pictures this page draws from real data, but drawn by hand.

Khan Academy. *Properties of Set Operations Using Venn Diagrams.*
<https://www.youtube.com/watch?v=lWjmbch870g>. It shades De Morgan's laws
on a diagram, as this page does near its end.

Up and Atom (2019). *Russell's Paradox: A Ripple in the Foundations of
Mathematics.* <https://www.youtube.com/watch?v=xauCQpnbNAM>. Think of a
set of all sets that do not contain themselves. Does it contain itself?
Jade Tan-Holmes tells how this question shook mathematics. The video is
about fourteen minutes long.
