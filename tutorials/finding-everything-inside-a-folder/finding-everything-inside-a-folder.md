---
title: "Recursion: finding every file in a folder tree"
year: "2026-2027"
version: 2026.09.27.1
covers:
  a-structure-that-branches:
    covers: [CMPS-LO1]
  walking-it-with-recursion:
    covers: [CMPS-LO1]
  walking-it-without-recursion:
    covers: [CMPS-LO1]
  depth-first-and-breadth-first:
    covers: [CMPS-LO1]
worlds:
  mazes-and-dungeons: A dungeon whose rooms branch off one another, with a dragon somewhere inside.
  maps-and-networks: A river and the streams that flow into it. The names and lengths are made up.
  collections: A fossil museum, with halls, cabinets and fossils. The ages are rough.
  puzzles: The Tower of Hanoi, a puzzle of discs and three pegs.
---

# Recursion: finding every file in a folder tree

A grid has a fixed shape: a set number of rows and columns, and one value
where each row meets each column. A folder on a computer is different.
It holds files, and it holds other folders. Each of those can hold more
files and more folders, as many levels deep as anyone likes.

On this page we build that shape in Python. Then we count every file
inside it, in two different ways, and watch the order each way visits
the folders.

## A structure that branches

Here is one folder, written as a Python dictionary. It has three keys:
`"name"`, `"files"` and `"subfolders"`. The value for `"subfolders"` is a
list, and each item in that list is another folder, written the same
way. If you want a reminder of how dictionaries work, see
[Dictionaries: looking things up by name](tutorial:looking-things-up-by-name).

```python exec
id: a-structure-that-branches-1
photos = {
    "name": "photos",
    "files": ["beach.jpg", "party.jpg"],
    "subfolders": [
        {
            "name": "2025",
            "files": ["new_year.jpg"],
            "subfolders": [
                {"name": "summer", "files": ["swim.jpg"], "subfolders": []}
            ],
        },
        {
            "name": "2026",
            "files": [],
            "subfolders": [
                {"name": "trip", "files": ["day1.jpg", "day2.jpg"], "subfolders": []}
            ],
        },
    ],
}

print(photos["name"])
print(photos["files"])
print(photos["subfolders"][0]["name"])
```

![The photos folder holds two files and two subfolders, 2025 and 2026.
2025 holds one file and one subfolder, summer, which holds one file. 2026
holds no files and one subfolder, trip, which holds two
files.](photos-tree.svg)

This shape is called a *tree*. A tree is a structure where each value can
lead to several others, and if you follow it, you never return to
where you started.

- `photos` holds two files, and two subfolders: `"2025"` and `"2026"`.
- `"2025"` holds one file, and one subfolder, `"summer"`, which holds one
  file.
- `"2026"` holds no files of its own. It holds one subfolder, `"trip"`,
  which holds two files.

That makes three levels. But nothing in the dictionary says in advance
how many levels there will be. A grid in
[Matrices: adding, scaling and transposing a grid of
numbers](tutorial:grid-of-numbers) is different. Its number of rows and
columns is fixed as soon as it is made.

### Your turn

Look at `photos["subfolders"][1]["subfolders"][0]`.

1. Read the dictionary above. What is this folder's name, and how many
   files does it hold?
2. Check your answer with code.

```python exec
id: a-structure-that-branches-2
```

## Walking it with recursion

We want to count every file, at every level. So we need one function
that can handle any folder: one that holds only files, one that holds
only more folders, and anything in between.

How many files do you count in the picture above? Run the cell to check.

```python exec
id: walking-it-with-recursion-1
def count_files(folder):
    total = len(folder["files"])
    for sub in folder["subfolders"]:
        total += count_files(sub)
    return total

print(count_files(photos))
```

Look at the loop inside `count_files`. The function calls itself, once
for every subfolder. A function that calls itself is using *recursion*.
Each call answers a smaller version of the same question: how many files
does *this* folder contain?

Can you follow the calls on the picture, with your finger? Which folder
answers first?

<details class="dl-answer"><summary>What happens, call by call</summary>

1. `photos` has 2 files of its own. Then it asks each of its subfolders.
2. `"2025"` has 1 file. It asks its one subfolder, `"summer"`.
3. `"summer"` has 1 file and no subfolders. The loop has nothing to do,
   so it answers 1 straight away.
4. `"2025"` adds that up: 1 + 1 = 2.
5. `"2026"` has 0 files of its own. It asks its one subfolder, `"trip"`.
6. `"trip"` has 2 files and no subfolders, so it answers 2 straight away.
7. `"2026"` adds that up: 0 + 2 = 2.
8. `photos` adds everything up: 2 + 2 + 2 = 6.

</details>

A folder with no subfolders answers at once, using only
`len(folder["files"])`. It does not call `count_files` again. This case
is called the *base case*. The base case is the case a recursive
function can answer without calling itself.

Every branch of the tree ends in a folder with no subfolders, so every
chain of calls reaches a base case and stops. Without a base case, a
recursive function would call itself again and again, and never stop.

### Your turn

Write `deepest_level(folder, level=0)`. It returns how many levels down
the deepest subfolder is. `photos` itself is at level `0`, and `"trip"`
is at level `2`.

```python exec
id: walking-it-with-recursion-2
hint: A folder with no subfolders is already at its own deepest level. A folder with subfolders is one level deeper than the deepest of them.
```

## In what order?

`count_files` visits every folder once. In what order? This version
collects the names as it goes.

```python exec
id: in-what-order-1
def visit_order(folder):
    """The folders' names, in the order count_files visits them."""
    order = [folder["name"]]
    for sub in folder["subfolders"]:
        order += visit_order(sub)
    return order

print(" ".join(visit_order(photos)))
```

```predict
type: choice

What will the cell print?

- photos 2025 summer 2026 trip
- photos 2025 2026 summer trip
  - Every folder on one level is visited before the level below it.
- photos 2026 trip 2025 summer
  - The last subfolder is visited first.
```

The recursion goes as deep as it can down the first branch, all the way
to `"summer"`, before it returns for `"2026"`. It finishes one whole
branch before it starts the next.

## Walking it without recursion

We can do the same count without a function that calls itself. This
version uses a `while` loop, as in
[Repeating steps with loops](tutorial:repeating-yourself), and two list
methods you may not have met yet:

- `to_visit.pop()` removes the last item from the list `to_visit`, and
  returns it.
- `to_visit.extend(other_list)` adds every item from `other_list` to the
  end of `to_visit`.

`while to_visit:` continues as long as the list is not empty. Python
treats an empty list as false, and a list with anything in it as true.

```python exec
id: walking-it-without-recursion-1
def count_files_iterative(folder):
    """The number of files, and the order the folders were visited in."""
    total = 0
    order = []
    to_visit = [folder]
    while to_visit:
        current = to_visit.pop()
        order.append(current["name"])
        total += len(current["files"])
        to_visit.extend(current["subfolders"])
    return total, order

total, order = count_files_iterative(photos)
print(total)
print(" ".join(order))
```

```predict
type: choice

The first line is the total, 6. What will the second line say about the
order?

- photos 2026 trip 2025 summer
- photos 2025 summer 2026 trip
  - The same order as the recursion.
- photos 2025 2026 summer trip
  - Every folder on one level before the level below it.
```

`to_visit` holds every folder that is still waiting to be counted. It
starts with only `photos`. Each pass through the loop takes the folder
added most recently, counts its files, and adds its subfolders to the
end of the list. After `photos`, the list holds `"2025"` then `"2026"`,
so `pop()` takes `"2026"` first, and then its `"trip"`, before it comes
back to `"2025"`.

Nothing here calls itself. This version is *iterative*. It repeats a
loop, and it keeps its own list of what is left to do.

The recursive version needs a list like that too. Python keeps it for
us, and we do not see it. Python always keeps a list of the function
calls that have started but not yet finished, called the *call stack*.
In the recursive version, the call stack records which folders are
left.

## Depth-first and breadth-first

Both walks so far go as deep as they can down one branch before they
try the next. The recursion takes the branches left to right, and
`pop()` takes them right to left. A walk that finishes one branch before
it starts the next is called *depth-first*.

Now change one thing: `pop(0)` takes the *first* item in the list, the
one that has waited longest.

```python exec
id: depth-first-and-breadth-first-1
def visit_order_by_level(folder):
    order = []
    to_visit = [folder]
    while to_visit:
        current = to_visit.pop(0)
        order.append(current["name"])
        to_visit.extend(current["subfolders"])
    return order

print(" ".join(visit_order_by_level(photos)))
```

```predict
type: choice

What will the cell print?

- photos 2025 2026 summer trip
- photos 2025 summer 2026 trip
  - The same order as the recursion.
- photos 2026 trip 2025 summer
  - The same order as `pop()`.
```

With `pop(0)`, the folders leave the list in the order they joined it.
`photos` adds both of its subfolders before either of them adds its own,
so the walk visits every folder on level 1 before any folder on level 2.
A walk that goes level by level is called *breadth-first*.

The whole difference between the two is one argument: `pop()` or
`pop(0)`. They visit the same folders and count the same files. The
order never changes the total. But when the question is "which is
nearest?", the order matters, and the next page uses breadth-first to
find the shortest way through a map.

## A real folder tree

Python's own `os.walk` walks a real folder tree, on a disk. The next
cell builds `photos` as real folders and files, in a temporary folder,
and walks it. In a browser tab, the disk is a pretend one that Python
keeps in memory, and it disappears when you close the page.

```python exec
id: a-real-folder-tree-1
import os
import tempfile

root = os.path.join(tempfile.mkdtemp(), "photos")


def make_on_disk(folder, where):
    """Make this folder, its files and its subfolders, at the path where."""
    os.makedirs(where)
    for name in folder["files"]:
        open(os.path.join(where, name), "w").close()
    for sub in folder["subfolders"]:
        make_on_disk(sub, os.path.join(where, sub["name"]))


make_on_disk(photos, root)
for here, subfolders, files in os.walk(root):
    subfolders.sort()
    print(os.path.relpath(here, os.path.dirname(root)), sorted(files))
```

`os.walk` gives each folder's path, its subfolders and its files, in
turn. Which order does it use: depth-first or breadth-first? And why
does `make_on_disk` call itself?

## Your world

Each world has its own tree, or its own recursion. The function you
write calls itself, and has a base case that does not.

<div class="dl-world" data-world="mazes-and-dungeons">

A dungeon's rooms branch off one another, like folders: each room leads
on to a few more, and no passage loops back. Can you write
`path_to(room, target)`? It returns the list of room names from `room`
down to the room called `target`, or `None` if that room is not in this
part of the dungeon.

```python exec
id: your-world-1--mazes-and-dungeons
dungeon = {
    "name": "entrance",
    "rooms": [
        {
            "name": "guard room",
            "rooms": [
                {"name": "armoury", "rooms": []},
                {"name": "cellar", "rooms": [{"name": "dragon's lair", "rooms": []}]},
            ],
        },
        {"name": "chapel", "rooms": [{"name": "crypt", "rooms": []}]},
    ],
}


def path_to(room, target):
    """Room names from this room down to target, or None if target is not below it."""
    # Your code here.
```

```hint
If this room is the target, the path is just `[room["name"]]`: that is
the base case. Otherwise, ask each room it leads to. The first one that
returns a path gives the answer: this room's name, then that path.
```

```inputs
path_to(dungeon, "dragon's lair")
path_to(dungeon, "crypt")
path_to(dungeon, "kitchen")
```

```solution
def path_to(room, target):
    """Room names from this room down to target, or None if target is not below it."""
    if room["name"] == target:
        return [room["name"]]
    for next_room in room["rooms"]:
        path = path_to(next_room, target)
        if path is not None:
            return [room["name"]] + path
    return None
---
The dragon is at the end of entrance, guard room, cellar. The search is
depth-first: it tries the whole of the guard room's branch before the
chapel. A room that is not there gives `None`, because no branch
returns a path. The next page's dungeon has passages that loop back,
and a search there needs one more thing.
```

</div>

<div class="dl-world" data-world="maps-and-networks">

A river is a tree too: streams flow into bigger streams, which flow into
the river. Can you write `total_length(river)`? It returns the length in
km of the river and every stream that flows into it, at every level.

```python exec
id: your-world-1--maps-and-networks
river = {
    "name": "Great River", "km": 120, "tributaries": [
        {"name": "Swift Water", "km": 45, "tributaries": [
            {"name": "Hill Brook", "km": 12, "tributaries": []},
            {"name": "Mill Stream", "km": 8, "tributaries": []},
        ]},
        {"name": "Slow Water", "km": 60, "tributaries": [
            {"name": "Bog Burn", "km": 15, "tributaries": [
                {"name": "Moss Rill", "km": 4, "tributaries": []},
            ]},
        ]},
    ],
}


def total_length(river):
    """The length of this river and every stream that flows into it."""
    # Your code here.
```

```hint
It is `count_files`, with `river["km"]` in place of the number of files,
and `"tributaries"` in place of `"subfolders"`.
```

```inputs
total_length(river)
total_length(river["tributaries"][1])
total_length({"name": "Moss Rill", "km": 4, "tributaries": []})
```

```solution
def total_length(river):
    """The length of this river and every stream that flows into it."""
    total = river["km"]
    for stream in river["tributaries"]:
        total += total_length(stream)
    return total
---
264 km of water in all: 120 in the Great River, and 144 in the streams
that feed it. Slow Water and everything that flows into it make 79 km.
A stream with nothing flowing into it is the base case: its own length.
```

</div>

<div class="dl-world" data-world="collections">

A fossil museum has halls, and cabinets inside the halls, and each
holds fossils, with their rough age in millions of years. Can you write
`oldest(room)`? It returns `(age, name)` for the oldest fossil in this
room or any room inside it, or `None` if there are no fossils there at
all.

```python exec
id: your-world-1--collections
museum = {
    "name": "museum", "fossils": [], "rooms": [
        {"name": "sea hall", "fossils": [("trilobite", 500), ("ammonite", 200)], "rooms": [
            {"name": "shell cabinet", "fossils": [("brachiopod", 450)], "rooms": []},
        ]},
        {"name": "dinosaur hall", "fossils": [("Tyrannosaurus", 66)], "rooms": [
            {"name": "bird cabinet", "fossils": [("Archaeopteryx", 150)], "rooms": []},
            {"name": "ice age room", "fossils": [("woolly mammoth", 0.01)], "rooms": []},
        ]},
    ],
}


def oldest(room):
    """(age, name) of the oldest fossil in this room or inside it, or None."""
    # Your code here.
```

```hint
Start with `best = None`. Check this room's own fossils, then ask each
room inside it, and keep whichever is older. A room with no fossils
anywhere inside it gives `None`.
```

```inputs
oldest(museum)
oldest(museum["rooms"][1])
oldest({"name": "empty", "fossils": [], "rooms": []})
```

```solution
def oldest(room):
    """(age, name) of the oldest fossil in this room or inside it, or None."""
    best = None
    for name, age in room["fossils"]:
        if best is None or age > best[0]:
            best = (age, name)
    for inner in room["rooms"]:
        found = oldest(inner)
        if found is not None and (best is None or found[0] > best[0]):
            best = found
    return best
---
The trilobite, about 500 million years old, is the oldest in the
museum. In the dinosaur hall and its cabinets it is Archaeopteryx, about
150. The museum's own entrance has no fossils, so its answer comes
entirely from the rooms inside it.
```

</div>

<div class="dl-world" data-world="puzzles">

The Tower of Hanoi has three pegs, A, B and C, and a pile of discs on
A, largest at the bottom. The task is to move the whole pile to C, one
disc at a time, never putting a larger disc on a smaller one. The trick
is recursion: to move `n` discs, move the top `n - 1` out of the way to
the spare peg, move the largest disc, then move the `n - 1` back on top
of it. Can you write `hanoi(n, source, target, spare)`, which returns the
list of moves as `(from, to)` pairs?

```python exec
id: your-world-1--puzzles
def hanoi(n, source, target, spare):
    """The moves that carry n discs from source to target, as (from, to) pairs."""
    # Your code here.
```

```hint
Moving 0 discs takes no moves: that is the base case. Otherwise, the
moves are: `hanoi(n - 1, source, spare, target)`, then
`(source, target)`, then `hanoi(n - 1, spare, target, source)`.
```

```inputs
hanoi(1, "A", "C", "B")
hanoi(2, "A", "C", "B")
len(hanoi(10, "A", "C", "B"))
```

```solution
def hanoi(n, source, target, spare):
    """The moves that carry n discs from source to target, as (from, to) pairs."""
    if n == 0:
        return []
    return (hanoi(n - 1, source, spare, target)
            + [(source, target)]
            + hanoi(n - 1, spare, target, source))
---
One disc takes one move, two take three, and ten take 1,023. Each extra
disc doubles the moves and adds one, so $n$ discs take $2^n - 1$. A
legend tells of a temple where priests move 64 golden discs: at one
move a second, $2^{64} - 1$ moves would take far longer than the age of
the universe.
```

</div>

## Where to read more

Sedgewick, R. and Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
Chapter 4 covers graphs, and the depth-first and breadth-first traversal
strategies this page builds by hand for a tree. It goes much deeper than
this course needs, but it is worth knowing it is there.

Python Software Foundation. *os.walk().*
<https://docs.python.org/3/library/os.html#os.walk>. This is the standard
library function that walks a real folder tree on disk. It is the same
shape this page built by hand with a plain dictionary.

Reducible (2020). *Depth First Search (DFS) Explained: Algorithm,
Examples, and Code.* <https://www.youtube.com/watch?v=PMMc4VsIacU>.
When we walk a folder tree, we do one kind of depth-first search. It goes
as deep as it can, then returns and tries the next branch. Reducible shows
it on other shapes too, with a recursive version and a loop version, as
this page does. The video is about twenty-one minutes long.
