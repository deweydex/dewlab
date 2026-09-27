---
title: "Recursion: finding every file in a folder tree — Practice"
practice_for: finding-everything-inside-a-folder
year: "2026-2027"
version: 2026.09.27.1
worlds:
  mazes-and-dungeons: A dungeon whose rooms branch off one another, with a dragon somewhere inside.
  maps-and-networks: A river and the streams that flow into it. The names and lengths are made up.
  collections: A fossil museum, with halls, cabinets and fossils. The ages are rough.
  puzzles: The Tower of Hanoi, a puzzle of discs and three pegs.
---

# Recursion: finding every file in a folder tree — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

```python exec
id: tools-1
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


def count_files(folder):
    total = len(folder["files"])
    for sub in folder["subfolders"]:
        total += count_files(sub)
    return total


print(count_files(photos))
```

## The base case

**1.** An empty folder holds no files and no subfolders.

```python exec
id: the-base-case-1
print(count_files({"name": "empty", "files": [], "subfolders": []}))
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints `0`. The line `total = len(folder["files"])` sets `total` to
`0`, because `files` is empty. Then the loop runs zero times, because
there are no subfolders. This is the base case at work: a folder with
nothing inside answers at once, and `count_files` never calls itself.

</details>

**2.** Can you write `deepest_level(folder, level=0)`? It returns how
many levels down the deepest subfolder is. `photos` itself is at level
`0`.

```python exec
id: the-base-case-2
def deepest_level(folder, level=0):
    """How many levels down the deepest subfolder is."""
    # Your code here.
```

```hint
A folder with no subfolders is already at its own deepest level. A
folder with subfolders is as deep as the deepest of them, each asked
with `level + 1`. `max()` picks the largest of several values.
```

```inputs
deepest_level(photos)
deepest_level({"name": "empty", "files": [], "subfolders": []})
deepest_level({"name": "a", "files": [], "subfolders": [{"name": "b", "files": [], "subfolders": [{"name": "c", "files": [], "subfolders": [{"name": "d", "files": [], "subfolders": []}]}]}]})
```

```solution
def deepest_level(folder, level=0):
    """How many levels down the deepest subfolder is."""
    if not folder["subfolders"]:
        return level
    return max(deepest_level(sub, level + 1) for sub in folder["subfolders"])
---
`photos` is 2 deep: `"summer"` and `"trip"` are both on level 2. A
folder with no subfolders is level 0 on its own. A chain of four
folders, each inside the one before, is 3 deep.
```

## A different tree

**3.** Here is a second folder. This one is for work, not photos.

```python exec
id: a-different-tree-1
work = {
    "name": "work",
    "files": ["report.docx"],
    "subfolders": [
        {
            "name": "clients",
            "files": [],
            "subfolders": [
                {"name": "acme", "files": ["invoice.pdf", "contract.pdf"], "subfolders": []},
            ],
        },
        {"name": "archive", "files": ["old.docx", "older.docx", "oldest.docx"], "subfolders": []},
    ],
}
print(count_files(work))
```

```predict
type: number

Add up every file at every level by hand. What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints `6`: one file directly in `work`, two in `"acme"`, and three
in `"archive"`. `"clients"` holds no files of its own, only a
subfolder, so it adds nothing by itself.

</details>

## Levels and paths

**4.** Can you write `folders_at_level(folder, level)`? It returns the
names of the folders exactly `level` levels down, left to right.

```python exec
id: levels-and-paths-1
def folders_at_level(folder, level):
    """The names of the folders exactly this many levels down."""
    # Your code here.
```

```hint
Level 0 is the folder itself: `[folder["name"]]`. Any deeper level is
the same question, one level less, asked of each subfolder, with the
answers joined together.
```

```inputs
folders_at_level(photos, 1)
folders_at_level(photos, 2)
folders_at_level(photos, 3)
```

```solution
def folders_at_level(folder, level):
    """The names of the folders exactly this many levels down."""
    if level == 0:
        return [folder["name"]]
    names = []
    for sub in folder["subfolders"]:
        names += folders_at_level(sub, level - 1)
    return names
---
Level 1 is `2025` and `2026`, and level 2 is `summer` and `trip`. Level
3 is empty: the tree stops at level 2. Read level 0, then 1, then 2,
and you have the breadth-first order from the tutorial.
```

**5.** Can you write `find_file(folder, name)`? It returns the list of
folder names from `folder` down to the folder that holds the file
`name`, or `None` if no folder in the tree holds it.

```python exec
id: levels-and-paths-2
def find_file(folder, name):
    """Folder names from folder down to the one holding the file, or None."""
    # Your code here.
```

```hint
If the file is in this folder's own `"files"`, the path is just this
folder's name. Otherwise, ask each subfolder. The first one that
returns a path gives the answer: this folder's name, then that path.
```

```inputs
find_file(photos, "swim.jpg")
find_file(photos, "beach.jpg")
find_file(photos, "cat.jpg")
```

```solution
def find_file(folder, name):
    """Folder names from folder down to the one holding the file, or None."""
    if name in folder["files"]:
        return [folder["name"]]
    for sub in folder["subfolders"]:
        path = find_file(sub, name)
        if path is not None:
            return [folder["name"]] + path
    return None
---
`swim.jpg` is in `photos`, then `2025`, then `summer`. `beach.jpg` is in
`photos` itself, so the path is one folder long. A file that is not
there gives `None`, because no branch returns a path.
```

## Your world

**6.** A problem from the world you chose.

<div class="dl-world" data-world="mazes-and-dungeons">

Can you write `count_rooms(room)`, which counts this room and every room
beyond it?

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


def count_rooms(room):
    """This room, and every room beyond it."""
    # Your code here.
```

```hint
Start at 1, for this room. Then add what each room beyond it counts.
```

```inputs
count_rooms(dungeon)
count_rooms(dungeon["rooms"][1])
count_rooms({"name": "cupboard", "rooms": []})
```

```solution
def count_rooms(room):
    """This room, and every room beyond it."""
    total = 1
    for next_room in room["rooms"]:
        total += count_rooms(next_room)
    return total
---
Seven rooms in all. The chapel's branch has two: the chapel and the
crypt. A room that leads nowhere is the base case, and counts 1.
```

</div>

<div class="dl-world" data-world="maps-and-networks">

Can you write `count_streams(river)`, which counts every stream that
flows into this river, at every level, but not the river itself?

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


def count_streams(river):
    """Every stream that flows into this river, at every level."""
    # Your code here.
```

```hint
Each stream that flows straight in counts 1, plus every stream that
flows into *it*.
```

```inputs
count_streams(river)
count_streams(river["tributaries"][1])
count_streams({"name": "Moss Rill", "km": 4, "tributaries": []})
```

```solution
def count_streams(river):
    """Every stream that flows into this river, at every level."""
    total = 0
    for stream in river["tributaries"]:
        total += 1 + count_streams(stream)
    return total
---
Six streams feed the Great River. Two feed Slow Water: Bog Burn, and
Moss Rill, which flows into Bog Burn. Moss Rill has none.
```

</div>

<div class="dl-world" data-world="collections">

Can you write `all_fossils(room)`, which lists every fossil's name in
this room and inside it, depth-first: a room's own fossils first, then
each inner room's in turn?

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


def all_fossils(room):
    """Every fossil's name in this room and inside it, depth-first."""
    # Your code here.
```

```hint
Start with this room's own fossil names, then add what each inner room
returns, in order.
```

```inputs
all_fossils(museum)
all_fossils(museum["rooms"][0])
len(all_fossils(museum))
```

```solution
def all_fossils(room):
    """Every fossil's name in this room and inside it, depth-first."""
    names = [name for name, age in room["fossils"]]
    for inner in room["rooms"]:
        names += all_fossils(inner)
    return names
---
Six fossils, sea hall first: the trilobite, the ammonite and the
brachiopod, then the dinosaur hall's three. The sea hall and its cabinet
hold three between them.
```

</div>

<div class="dl-world" data-world="puzzles">

To count the moves in the Tower of Hanoi, you do not need the list of
moves. Can you write `hanoi_count(n)`, which counts them with the same
recursion: the moves for `n - 1` discs, one move for the largest, and
the moves for `n - 1` again?

```python exec
id: your-world-1--puzzles
def hanoi_count(n):
    """How many moves carry n discs from one peg to another."""
    # Your code here.
```

```hint
No discs take no moves. Otherwise, `2 * hanoi_count(n - 1) + 1`.
```

```inputs
hanoi_count(1)
hanoi_count(3)
hanoi_count(20)
```

```solution
def hanoi_count(n):
    """How many moves carry n discs from one peg to another."""
    if n == 0:
        return 0
    return 2 * hanoi_count(n - 1) + 1
---
1, 7 and 1,048,575: $2^n - 1$ each time. Twenty discs would take more
than twelve days at a move a second.
```

</div>

## From earlier

**7.** From [Dictionaries: looking things up by
name](tutorial:looking-things-up-by-name). A tree is dictionaries and
lists inside one another, and each `[...]` looks one level in.

```python exec
id: from-earlier-1
print(photos["subfolders"][0]["subfolders"][0]["files"][0])
```

```predict
type: choice

What will the cell print?

- swim.jpg
- new_year.jpg
  - The first subfolder of `photos` is `2025`.
- summer
  - The last `[0]` is inside `"files"`.
```

<details class="dl-answer"><summary>why</summary>

It prints `swim.jpg`. `photos["subfolders"][0]` is `2025`, its
`["subfolders"][0]` is `summer`, and `summer`'s `["files"][0]` is its
first file.

</details>
