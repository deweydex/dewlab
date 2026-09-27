---
title: "Mixed problems: algorithms"
practice_across:
  - finding-things
  - putting-things-in-order
  - finding-everything-inside-a-folder
  - the-shortest-way-there
  - three-ways-to-make-change
  - a-puzzle-of-your-own
year: "2026-2027"
version: 2026.09.27.1
worlds:
  mazes-and-dungeons: A maze of corridors, and the dead ends in it.
  maps-and-networks: A railway between towns. The towns are made up.
  collections: A museum drawer of fossils, and their ages.
  puzzles: Sudoku, and the rule every row must keep.
---

# Mixed problems: algorithms

These problems move between the pages of the series on purpose, and do
not say which page each one comes from. Choosing the tool is part of
the problem.

## 1.

A list of 1,000 names is in alphabetical order. What is the largest
number of names binary search could need to look at, to find one or to
be sure it is not there? And a linear search?

<details class="dl-hint"><summary>hint</summary>

Each look at the middle halves what is left. How many halvings take
1,000 down to 1?

</details>

<details class="dl-answer"><summary>one way through it</summary>

Binary search needs at most 10: 1,000, then at most 500, 250, 125, 62,
31, 15, 7, 3, 1. Another way to see it: $2^{10} = 1024$, which is more
than 1,000. A linear search could need all 1,000, if the name is last
or missing. For 1,000,000 names, binary search needs 20 and linear
search up to 1,000,000.

</details>

## 2.

This bubble sort counts its comparisons. It always makes every pass,
even when the list is already in order.

```python exec
id: mixed-algorithms-comparisons
def bubble_sort_counted(items):
    items = items[:]
    comparisons = 0
    for pass_number in range(len(items) - 1):
        for i in range(len(items) - 1 - pass_number):
            comparisons = comparisons + 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return comparisons


print(bubble_sort_counted(list(range(10, 0, -1))))
print(bubble_sort_counted(list(range(20, 0, -1))))
```

```predict
type: number

For 10 items in reverse order, it makes 45 comparisons. How many for
20 items?
```

190. The count is $n(n-1) \div 2$: $20 \times 19 \div 2 = 190$. Twice
the items make about four times the comparisons, which is what
$O(n^2)$ means.

## 3.

This function walks a tree of folders, and prints each folder's name as
it arrives.

```python exec
id: mixed-algorithms-walk-order
music = {
    "name": "music",
    "subfolders": [
        {"name": "rock", "subfolders": [{"name": "live", "subfolders": []}]},
        {"name": "jazz", "subfolders": []},
    ],
}


def walk(folder):
    print(folder["name"], end=" ")
    for sub in folder["subfolders"]:
        walk(sub)


walk(music)
print()
```

```predict
type: choice

In what order will it print the folders?

- music rock jazz live
  - It visits every folder on one level before the next level.
- music rock live jazz
- live rock jazz music
  - It prints each folder after the folders inside it.
```

`walk(music)` prints "music", then calls `walk` on "rock", which prints
"rock" and calls `walk` on "live" before it returns. Only then does the
loop in `walk(music)` move on to "jazz". It finishes one branch before
it starts the next: depth-first.

## 4.

A currency is safe for greedy change when greedy always uses the fewest
coins. Can you write `greedy_is_safe(coins, limit)`? It returns `True`
if `greedy(amount, coins)` equals `fewest(amount, coins)` for every
amount from 1 to `limit`, and `False` otherwise.

```python exec
id: mixed-algorithms-greedy-safe
def fewest(amount, coins, cache=None):
    """The fewest coins that make amount exactly, or None."""
    if cache is None:
        cache = {}
    if amount == 0:
        return 0
    if amount in cache:
        return cache[amount]
    best = None
    for coin in coins:
        if coin <= amount:
            rest = fewest(amount - coin, coins, cache)
            if rest is not None and (best is None or rest + 1 < best):
                best = rest + 1
    cache[amount] = best
    return best


def greedy(amount, coins):
    """Coins taken largest first, or None if that leaves a remainder."""
    remaining = amount
    count = 0
    for coin in sorted(coins, reverse=True):
        while remaining >= coin:
            remaining -= coin
            count += 1
    return count if remaining == 0 else None


def greedy_is_safe(coins, limit):
    """True if greedy uses the fewest coins for every amount from 1 to limit."""
    # Your code here.
```

```hint
Loop over every amount from 1 to `limit`. As soon as greedy and fewest
disagree, you can return `False`.
```

```inputs
greedy_is_safe([1, 2, 5, 10, 20, 50], 100)
greedy_is_safe([1, 3, 4], 10)
greedy_is_safe([1, 7, 10], 20)
greedy_is_safe([1, 7, 10], 13)
```

```solution
title: with what you've met so far
def greedy_is_safe(coins, limit):
    """True if greedy uses the fewest coins for every amount from 1 to limit."""
    for amount in range(1, limit + 1):
        if greedy(amount, coins) != fewest(amount, coins):
            return False
    return True
---
The euro coins, up to 50c, are safe up to 100. With [1, 3, 4], greedy fails at 6. With [1, 7, 10], it fails at 14, so it is safe up to 13 and not up to 20.
```

```solution
title: a shorter way you'll meet later
def greedy_is_safe(coins, limit):
    """True if greedy uses the fewest coins for every amount from 1 to limit."""
    return all(greedy(amount, coins) == fewest(amount, coins) for amount in range(1, limit + 1))
```

## 5.

This search is meant to list every place that can be reached from a
start. On a map with a loop, it never finishes. Can you write
`reachable(graph, start)`, which finishes, and returns the places in
alphabetical order?

```python
def reachable_broken(graph, start):
    found = []
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        found.append(place)
        to_visit.extend(graph[place])
    return sorted(found)
```

```python exec
id: mixed-algorithms-reachable
lanes = {
    "gate": ["well", "barn"],
    "well": ["gate", "barn"],
    "barn": ["gate", "well", "mill"],
    "mill": ["barn"],
    "pond": ["reeds"],
    "reeds": ["pond"],
}


def reachable(graph, start):
    """Every place reachable from start, in alphabetical order."""
    # Your code here.
```

```hint
Keep a record of every place already found, and add a neighbour to
`to_visit` only if it has not been found before.
```

```inputs
reachable(lanes, "gate")
reachable(lanes, "pond")
reachable(lanes, "mill")
```

```solution
def reachable(graph, start):
    """Every place reachable from start, in alphabetical order."""
    found = {start}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in found:
                found.add(neighbour)
                to_visit.append(neighbour)
    return sorted(found)
---
The broken version adds every neighbour, every time. The gate leads to the well, the well leads back to the gate, and the gate goes back on the list, again and again. The set `found` stops any place joining the list twice. The pond and the reeds form a second group that the gate can never reach.
```

## 6.

Which tool from this series would you reach for?

1. A sorted list of 1,000,000 postcodes: is one particular postcode in it?
2. The fewest stamps that make a postage cost exactly, from stamps of
   odd values.
3. The fewest changes of train from one station to another.
4. The total size of every file on a USB stick, in every folder.

<details class="dl-answer"><summary>answer</summary>

1. Binary search, because the list is sorted: at most 20 looks.
2. Brute force with a cache. Greedy is quick, but with odd values it
   can use more stamps than it needs.
3. Breadth-first search, with each station as a place. It finds the
   fewest steps first.
4. A walk through the folder tree, with recursion or with a list of
   folders still to visit.

</details>

## In your world

<div class="dl-world" data-world="mazes-and-dungeons">

A dead end is an open square with exactly one open square next to it,
above, below, left or right. Can you write `dead_ends(maze)`? It
returns how many dead ends the maze has.

```python exec
id: in-your-world-1--mazes-and-dungeons
maze = ["S.#.....",
        ".##.###.",
        "....#...",
        ".##..##T",
        "...#...."]


def dead_ends(maze):
    """How many open squares have exactly one open neighbour."""
    # Your code here.
```

```hint
For each square that is not `#`, count the neighbours inside the maze
that are not `#`. Remember to check the row and column are in range.
```

```inputs
dead_ends(maze)
dead_ends(["...", ".#.", "..."])
dead_ends([".#.", ".#.", "..."])
```

```solution
def dead_ends(maze):
    """How many open squares have exactly one open neighbour."""
    count = 0
    for r, row in enumerate(maze):
        for c, square in enumerate(row):
            if square == "#":
                continue
            open_next = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < len(maze) and 0 <= cc < len(row) and maze[rr][cc] != "#":
                    open_next += 1
            if open_next == 1:
                count += 1
    return count
---
The maze has 3 dead ends. A ring of corridors, like the second maze, has none: every square has two ways out.
```

</div>

<div class="dl-world" data-world="maps-and-networks">

Which town has the most lines out of it? Can you write
`busiest(graph)`? It returns the town with the most neighbours.

```python exec
id: in-your-world-1--maps-and-networks
rail = {
    "Northport": ["Ashford", "Kilbeg"],
    "Ashford": ["Northport", "Carrow", "Glenview", "Dunmore"],
    "Kilbeg": ["Northport", "Glenview"],
    "Carrow": ["Ashford", "Fenmoor"],
    "Glenview": ["Kilbeg", "Ashford", "Harbourtown"],
    "Dunmore": ["Ashford"],
    "Fenmoor": ["Carrow", "Harbourtown"],
    "Harbourtown": ["Fenmoor", "Glenview"],
}


def busiest(graph):
    """The place with the most neighbours."""
    # Your code here.
```

```hint
Keep the best town so far, and replace it whenever a town has more
neighbours.
```

```inputs
busiest(rail)
busiest({"a": ["b"], "b": ["a", "c"], "c": ["b"]})
```

```solution
title: with what you've met so far
def busiest(graph):
    """The place with the most neighbours."""
    best = None
    for place in graph:
        if best is None or len(graph[place]) > len(graph[best]):
            best = place
    return best
---
Ashford, with four lines. If Ashford closed, could every other town still reach Harbourtown? A copy of `rail` without Ashford, and `reachable()` from problem 5, can tell you.
```

```solution
title: a shorter way you'll meet later
def busiest(graph):
    """The place with the most neighbours."""
    return max(graph, key=lambda place: len(graph[place]))
```

</div>

<div class="dl-world" data-world="collections">

A drawer of fossils, with their ages in millions of years. Can you
write `oldest_first(fossils)`? It returns the fossils in order from the
oldest to the youngest.

```python exec
id: in-your-world-1--collections
fossils = [("ammonite", 200), ("trilobite", 500), ("mammoth tooth", 1),
           ("fern", 300), ("shark tooth", 20)]


def oldest_first(fossils):
    """The (name, age) pairs from the oldest to the youngest."""
    # Your code here.
```

```hint
Any sort from the sorting page will do, comparing the ages, `[1]`, not
the names. Or use `sorted()` with a `key=`.
```

```inputs
oldest_first(fossils)
oldest_first([("coral", 400)])
```

```solution
title: with what you've met so far
def oldest_first(fossils):
    """The (name, age) pairs from the oldest to the youngest."""
    items = list(fossils)
    for i in range(1, len(items)):
        j = i
        while j > 0 and items[j - 1][1] < items[j][1]:
            items[j - 1], items[j] = items[j], items[j - 1]
            j -= 1
    return items
---
Insertion sort, with the comparison turned round so that older comes first. The trilobite, at 500 million years, leads, and the mammoth tooth, at 1 million, is last.
```

```solution
title: a shorter way you'll meet later
def oldest_first(fossils):
    """The (name, age) pairs from the oldest to the youngest."""
    return sorted(fossils, key=lambda fossil: fossil[1], reverse=True)
```

</div>

<div class="dl-world" data-world="puzzles">

In Sudoku, every row must hold each of the numbers 1 to 9 exactly once.
Can you write `row_ok(row)`? It returns `True` if the row keeps that
rule.

```python exec
id: in-your-world-1--puzzles
def row_ok(row):
    """True if the row holds each of 1 to 9 exactly once."""
    # Your code here.
```

```hint
Sort a copy of the row. What should a good row look like, once it is
sorted?
```

```inputs
row_ok([5, 3, 4, 6, 7, 8, 9, 1, 2])
row_ok([5, 3, 4, 6, 7, 8, 9, 1, 1])
row_ok([1, 2, 3, 4, 5, 6, 7, 8])
row_ok([9, 8, 7, 6, 5, 4, 3, 2, 1])
```

```solution
def row_ok(row):
    """True if the row holds each of 1 to 9 exactly once."""
    return sorted(row) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
---
Sorting turns "each number once, in any order" into "exactly 1 to 9, in order", which one comparison can check. A row with a repeated number, or a missing one, cannot sort into that list.
```

</div>
