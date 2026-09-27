---
title: "Mixed problems: objects, with everything before them"
practice_across:
  - objects-and-classes
  - keeping-details-inside-an-object
  - one-class-many-methods
  - one-parent-many-children
  - objects-inside-objects
  - testing-what-a-class-does
year: "2026-2027"
version: 2026.09.27.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
---

# Mixed problems: objects, with everything before them

These problems put objects together with the programming that came
before them: lists, dictionaries, sorting, searching and recursion.
None of them says which idea it needs. [Mixed problems: programming
with objects](tutorial:mixed-programming-with-objects) stays inside
this course; this set reaches back further.

## 1.

Two names, one object. What does the last line print?

```python exec
id: mixed-objects-and-more-two-names
class Crate:
    def __init__(self, label, weight):
        self.label = label
        self.weight = weight


first = Crate("tools", 12)
second = first
second.weight = second.weight + 5
print(first.weight)
```

```predict
type: number

What will the cell print?
```

17. `second = first` does not copy the crate. It gives the same crate a
second name, just as `b = a` gives a list a second name. So changing
`second.weight` changes the one crate that both names point at.

## 2.

Two crates, made the same way. Are they equal?

```python exec
id: mixed-objects-and-more-equal
a = Crate("tools", 12)
b = Crate("tools", 12)
print(a.label == b.label and a.weight == b.weight)
print(a == b)
```

```predict
type: choice

What will the last line print?

- True
  - Every attribute matches, so they seem equal.
- False
```

`False`. Unless a class says otherwise, `==` asks whether two names
point at the same object, and `a` and `b` are two objects. A class can
say what equal means for it, with a method called `__eq__`. Without
one, compare the attributes you care about, as the first line does.

## 3.

Can you write `heaviest_first(crates)`? It returns the crates in order
from the heaviest to the lightest.

```python exec
id: mixed-objects-and-more-heaviest
crates = [Crate("rope", 4), Crate("tools", 12), Crate("food", 9), Crate("lamp", 2)]


def heaviest_first(crates):
    """The crates from the heaviest to the lightest."""
    # Your code here.
```

```hint
Any sort from the sorting page works, comparing `.weight`. Or use
`sorted()` with a `key=`.
```

```inputs
[crate.label for crate in heaviest_first(crates)]
[crate.label for crate in heaviest_first([Crate("one", 1)])]
```

```solution
title: with what you've met so far
def heaviest_first(crates):
    """The crates from the heaviest to the lightest."""
    items = list(crates)
    for i in range(1, len(items)):
        j = i
        while j > 0 and items[j - 1].weight < items[j].weight:
            items[j - 1], items[j] = items[j], items[j - 1]
            j -= 1
    return items
---
Insertion sort works on objects as it did on numbers. Only the comparison changes: `.weight` of each crate, not the crate itself.
```

```solution
title: a shorter way you'll meet later
def heaviest_first(crates):
    """The crates from the heaviest to the lightest."""
    return sorted(crates, key=lambda crate: crate.weight, reverse=True)
---
Without `key=`, `sorted()` would have to compare two crates, and Python does not know how, so it gives a `TypeError`.
```

## 4.

Can you write `by_label(crates)`? It returns a dictionary, with each
crate's label as the key and the crate itself as the value.

```python exec
id: mixed-objects-and-more-by-label
def by_label(crates):
    """A dictionary from each crate's label to the crate."""
    # Your code here.
```

```hint
Start with an empty dictionary, and add one entry for each crate.
```

```inputs
by_label(crates)["food"].weight
sorted(by_label(crates))
len(by_label(crates + [Crate("rope", 7)]))
```

```solution
def by_label(crates):
    """A dictionary from each crate's label to the crate."""
    found = {}
    for crate in crates:
        found[crate.label] = crate
    return found
---
Looking up a crate by its label now takes one step, however many crates there are, instead of a search through the list. Two crates with the same label share one key, so the later one replaces the earlier: five crates go in, and four come out. Is that what you want? If not, what would you store instead?
```

## 5.

Can you write `count_by_kind(things)`? Each thing has a `.kind`, such
as `"tool"` or `"food"`. It returns a dictionary from each kind to how
many things have it.

```python exec
id: mixed-objects-and-more-count
class Thing:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind


things = [Thing("rope", "tool"), Thing("bread", "food"), Thing("lamp", "tool"),
          Thing("apple", "food"), Thing("map", "paper"), Thing("saw", "tool")]


def count_by_kind(things):
    """A dictionary from each kind to how many things have it."""
    # Your code here.
```

```hint
`.get(kind, 0) + 1` adds one to a count that might not exist yet.
```

```inputs
count_by_kind(things)
count_by_kind([])
```

```solution
def count_by_kind(things):
    """A dictionary from each kind to how many things have it."""
    counts = {}
    for thing in things:
        counts[thing.kind] = counts.get(thing.kind, 0) + 1
    return counts
---
This is the same pattern as counting the words that follow a word in a chain: a dictionary of counts, one `.get()` at a time. Only the thing being counted has changed.
```

## 6.

A dictionary or a class? For each, say which, and why.

1. The price of each item in a shop, looked up by its name.
2. A bank account that must never go below zero.
3. The number of times each word appears in a book.
4. A character in a game who can take damage, heal, and be down.

<details class="dl-answer"><summary>answer</summary>

1. A dictionary: names to prices. Nothing needs guarding.
2. A class: the rule "never below zero" belongs inside it, in a method
   that refuses, so no other code can break it.
3. A dictionary: words to counts.
4. A class: it has rules (health from 0 to the maximum) and actions
   that must keep them.

A dictionary is enough when the data has no rules. When it has rules
that must always hold, a class can keep them in one place.

</details>

## In your world

Some objects hold other objects of the same kind, which may hold more
again. Can you write `count_inside(thing)`? It returns how many objects
are inside `thing` at every level: the ones it holds, the ones they
hold, and so on.

<div class="dl-world" data-world="game">

A backpack holds items and bags, and a bag can hold more bags.

```python exec
id: in-your-world-1--game
class Bag:
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents    # a list of names and other bags


backpack = Bag("backpack", [
    "rope",
    Bag("pouch", ["coin", "coin", Bag("tiny purse", ["gem"])]),
    "lamp",
    Bag("food bag", ["bread", "apple"]),
])


def count_inside(thing):
    """How many things are inside, at every level."""
    # Your code here.
```

```hint
Count each thing in `contents`. If it is a `Bag`
(`isinstance(item, Bag)`), add what is inside it too, by calling
`count_inside` on it.
```

```inputs
count_inside(backpack)
count_inside(Bag("empty", []))
count_inside(Bag("one", [Bag("inner", ["key"])]))
```

```solution
def count_inside(thing):
    """How many things are inside, at every level."""
    total = 0
    for item in thing.contents:
        total += 1
        if isinstance(item, Bag):
            total += count_inside(item)
    return total
---
10 things: 4 in the backpack itself, and 6 inside its bags. The function calls itself for each bag inside, just as the folder walk did for each subfolder, and a bag with nothing inside is its base case.
```

</div>

<div class="dl-world" data-world="ocean">

A submarine has compartments, and a compartment can hold smaller
compartments and the equipment inside them.

```python exec
id: in-your-world-1--ocean
class Compartment:
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents    # a list of names and other compartments


submarine = Compartment("submarine", [
    Compartment("control room", ["sonar", "periscope"]),
    Compartment("lab", ["microscope", Compartment("sample store", ["jar", "jar", "jar"])]),
    "engine",
])


def count_inside(thing):
    """How many things are inside, at every level."""
    # Your code here.
```

```hint
Count each thing in `contents`. If it is a `Compartment`
(`isinstance(item, Compartment)`), add what is inside it too, by
calling `count_inside` on it.
```

```inputs
count_inside(submarine)
count_inside(Compartment("empty", []))
count_inside(Compartment("one", [Compartment("inner", ["valve"])]))
```

```solution
def count_inside(thing):
    """How many things are inside, at every level."""
    total = 0
    for item in thing.contents:
        total += 1
        if isinstance(item, Compartment):
            total += count_inside(item)
    return total
---
10 things: 3 in the submarine itself, and 7 inside its compartments. The function calls itself for each compartment inside, just as the folder walk did for each subfolder, and a compartment with nothing inside is its base case.
```

</div>

<div class="dl-world" data-world="solar-system">

A star has planets, a planet has moons, and a probe can orbit a moon.

```python exec
id: in-your-world-1--solar-system
class Body:
    def __init__(self, name, orbiters):
        self.name = name
        self.contents = orbiters    # the bodies that go round this one


sun = Body("Sun", [
    Body("Mercury", []),
    Body("Earth", [Body("Moon", [Body("probe", [])])]),
    Body("Mars", [Body("Phobos", []), Body("Deimos", [])]),
])


def count_inside(thing):
    """How many bodies go round this one, at every level."""
    # Your code here.
```

```hint
Count each body in `contents`, and add what goes round it, by calling
`count_inside` on it.
```

```inputs
count_inside(sun)
count_inside(Body("lonely", []))
count_inside(sun.contents[1])
```

```solution
def count_inside(thing):
    """How many bodies go round this one, at every level."""
    total = 0
    for body in thing.contents:
        total += 1 + count_inside(body)
    return total
---
7 bodies: 3 planets, 3 moons and 1 probe. Every item here is a body, so there is no need to check what kind it is: each one is counted, and so is everything that goes round it. A body with nothing going round it is the base case.
```

</div>
