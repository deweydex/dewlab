---
title: "Graph search: the shortest way there — Practice"
practice_for: the-shortest-way-there
year: "2026-2027"
version: 2026.09.27.1
worlds:
  mazes-and-dungeons: A maze of corridors, with treasure at the far side.
  maps-and-networks: A railway between towns. The towns are made up.
  collections: The rooms of a museum, joined by doorways.
  puzzles: The water-jug puzzle, where every state of the jugs is a place on a map.
---

# Graph search: the shortest way there — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

```python exec
id: tools-1
streets = {
    "station": ["market", "bridge"],
    "market": ["station", "school", "library"],
    "bridge": ["station", "park"],
    "school": ["market", "library", "park"],
    "library": ["market", "school"],
    "park": ["bridge", "school", "harbour"],
    "harbour": ["park"],
}


def reached_from(graph, start):
    """For every place, the place the breadth-first walk reached it from."""
    came_from = {start: None}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in came_from:
                came_from[neighbour] = place
                to_visit.append(neighbour)
    return came_from


print(reached_from(streets, "station"))
```

## How far away

**1.** Can you write `distances(graph, start)`? It returns a dictionary
of every place that can be reached from `start`, with the fewest steps
it takes to get there.

```python exec
id: how-far-away-1
def distances(graph, start):
    """The fewest steps from start to every place it can reach."""
    # Your code here.
```

```hint
It is `reached_from` with a number in place of a place: the start is 0
steps away, and a place found from `place` is one step further than
`place`.
```

```inputs
distances(streets, "station")
distances(streets, "harbour")["library"]
distances({"alone": []}, "alone")
```

```solution
def distances(graph, start):
    """The fewest steps from start to every place it can reach."""
    steps = {start: 0}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in steps:
                steps[neighbour] = steps[place] + 1
                to_visit.append(neighbour)
    return steps
---
From the station: the market and the bridge are 1 step away, the
school, the library and the park 2, and the harbour 3. These are the
rings the breadth-first walk goes out in. From the harbour, the library
is 3 steps: park, school, library.
```

**2.** On a web page, a link goes one way: page `a` links to `b`, but
`b` need not link back. Here are three pages, each linking on to the
next.

```python exec
id: how-far-away-2
one_way = {"a": ["b"], "b": ["c"], "c": []}
print(len(reached_from(one_way, "a")), len(reached_from(one_way, "c")))
```

```predict
type: number

The first number is 3: from `a`, every page can be reached. What will
the second number be?
```

<details class="dl-answer"><summary>why</summary>

It is 1. Page `c` links nowhere, so from `c` only `c` itself can be
reached. A graph whose edges go one way is called *directed*. The
search is the same; only the lists change. The web is a directed graph,
which is why a page can be easy to reach but lead nowhere.

</details>

## Groups of places

**3.** Some maps fall into separate groups, with no way from one group
to another: islands, say, linked by ferries within each group but not
between them. Can you write `count_groups(graph)`?

```python exec
id: groups-of-places-1
islands = {
    "Big Isle": ["Middle Isle"],
    "Middle Isle": ["Big Isle", "Little Isle"],
    "Little Isle": ["Middle Isle"],
    "Far Rock": [],
    "North Isle": ["North Holm"],
    "North Holm": ["North Isle"],
}


def count_groups(graph):
    """How many separate groups of places the graph falls into."""
    # Your code here.
```

```hint
Go through every place. If it is not yet in any group you have found,
it starts a new group: count it, and add everything `reached_from` it
to the places already seen.
```

```inputs
count_groups(streets)
count_groups(islands)
count_groups({"a": ["b"], "b": ["a"], "c": []})
```

```solution
def count_groups(graph):
    """How many separate groups of places the graph falls into."""
    seen = set()
    groups = 0
    for place in graph:
        if place not in seen:
            groups += 1
            seen.update(reached_from(graph, place))
    return groups
---
The town is one group: every place can reach every other. The islands
are three: the three isles linked by ferry, Far Rock on its own, and
the two northern islands. `seen.update` adds every key of the
dictionary `reached_from` returns.
```

**4.** The page counted streets. Suppose some streets are much longer
than others. Does breadth-first still find the shortest walk?

<details class="dl-answer"><summary>answer</summary>

No. It finds the way with the fewest *streets*, and one long street can
be longer than three short ones. To find the shortest walk, the search
has to keep taking the nearest place found so far, by distance, not by
the order it was found in. That search is called *Dijkstra's
algorithm*, after Edsger Dijkstra, who found it in 1956. It is what
map apps start from.

</details>

## Your world

**5.** Can you write `places_within(graph, start, steps)`? It returns,
in sorted order, every place that is at most `steps` away from `start`.

<div class="dl-world" data-world="mazes-and-dungeons">

```python exec
id: your-world-1--mazes-and-dungeons
maze = ["S.#.....",
        ".##.###.",
        "....#...",
        ".##..##T",
        "...#...."]


def maze_graph(rows):
    """Every open square, as (row, column), with the open squares next to it."""
    graph = {}
    for r, row in enumerate(rows):
        for c, square in enumerate(row):
            if square == "#":
                continue
            graph[(r, c)] = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < len(rows) and 0 <= cc < len(row) and rows[rr][cc] != "#":
                    graph[(r, c)].append((rr, cc))
    return graph


maze_map = maze_graph(maze)


def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    # Your code here.
```

```hint
Find how far away every place is, as in problem 1, then keep the places
that are not too far, and sort them.
```

```inputs
len(places_within(maze_map, (0, 0), 3))
len(places_within(maze_map, (0, 0), 6))
len(maze_map)
```

```solution
def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    far = {start: 0}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in far:
                far[neighbour] = far[place] + 1
                to_visit.append(neighbour)
    return sorted(place for place, how_far in far.items() if how_far <= steps)
---
6 squares are within 3 steps of the start, and 13 within 6, of the maze's 28 open squares. A torch that lights 3 squares around you shows only a small part of the maze.
```

</div>

<div class="dl-world" data-world="maps-and-networks">

```python exec
id: your-world-1--maps-and-networks
rail = {
    "Northport": ["Ashford", "Kilbeg"],
    "Ashford": ["Northport", "Carrow"],
    "Kilbeg": ["Northport", "Dunmore"],
    "Carrow": ["Ashford", "Dunmore", "Fenmoor"],
    "Dunmore": ["Kilbeg", "Carrow", "Glenview"],
    "Fenmoor": ["Carrow", "Harbourtown"],
    "Glenview": ["Dunmore", "Ivybridge"],
    "Ivybridge": ["Glenview", "Harbourtown"],
    "Harbourtown": ["Fenmoor", "Ivybridge"],
}


def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    # Your code here.
```

```hint
Find how far away every place is, as in problem 1, then keep the places
that are not too far, and sort them.
```

```inputs
places_within(rail, "Carrow", 1)
places_within(rail, "Northport", 2)
places_within(rail, "Harbourtown", 0)
```

```solution
def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    far = {start: 0}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in far:
                far[neighbour] = far[place] + 1
                to_visit.append(neighbour)
    return sorted(place for place, how_far in far.items() if how_far <= steps)
---
One journey from Carrow reaches Ashford, Dunmore and Fenmoor, and Carrow itself is within 0. Two journeys from Northport reach four towns. A place is always within 0 steps of itself.
```

</div>

<div class="dl-world" data-world="collections">

```python exec
id: your-world-1--collections
floor = {
    "entrance": ["shop", "hall of minerals"],
    "shop": ["entrance", "café"],
    "hall of minerals": ["entrance", "hall of fossils", "map room"],
    "café": ["shop", "map room"],
    "map room": ["café", "hall of minerals", "star room"],
    "hall of fossils": ["hall of minerals", "dinosaur gallery"],
    "star room": ["map room", "dinosaur gallery"],
    "dinosaur gallery": ["hall of fossils", "star room"],
}


def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    # Your code here.
```

```hint
Find how far away every place is, as in problem 1, then keep the places
that are not too far, and sort them.
```

```inputs
places_within(floor, "map room", 1)
len(places_within(floor, "entrance", 2))
places_within(floor, "shop", 0)
```

```solution
def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    far = {start: 0}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in far:
                far[neighbour] = far[place] + 1
                to_visit.append(neighbour)
    return sorted(place for place, how_far in far.items() if how_far <= steps)
---
One doorway from the map room leads to the café, the hall of minerals and the star room. Within two doorways of the entrance are six of the eight rooms. A guard who can see two rooms away from the entrance cannot see the star room or the dinosaur gallery.
```

</div>

<div class="dl-world" data-world="puzzles">

```python exec
id: your-world-1--puzzles
def moves(state):
    """Every state one move away from (small, big), for jugs of 3 and 5 litres."""
    small, big = state
    pour_in = min(small, 5 - big)
    pour_out = min(big, 3 - small)
    after = {(3, big), (small, 5), (0, big), (small, 0),
             (small - pour_in, big + pour_in), (small + pour_out, big - pour_out)}
    after.discard(state)
    return sorted(after)


jugs = {}
to_build = [(0, 0)]
while to_build:
    state = to_build.pop()
    if state not in jugs:
        jugs[state] = moves(state)
        to_build.extend(jugs[state])


def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    # Your code here.
```

```hint
Find how far away every place is, as in problem 1, then keep the places
that are not too far, and sort them.
```

```inputs
places_within(jugs, (0, 0), 1)
len(places_within(jugs, (0, 0), 2))
len(places_within(jugs, (0, 0), 6))
```

```solution
def places_within(graph, start, steps):
    """Every place at most `steps` away from start, sorted."""
    far = {start: 0}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in far:
                far[neighbour] = far[place] + 1
                to_visit.append(neighbour)
    return sorted(place for place, how_far in far.items() if how_far <= steps)
---
One move from empty gives a full small jug or a full big one. Within two moves the jugs can be in 6 states, and within six moves in 14 of the 16. The last two take longer, and one of them is 4 litres with an empty small jug.
```

</div>

## From earlier

**6.** From [Recursion: finding every file in a folder
tree](tutorial:finding-everything-inside-a-folder). `pop(0)` takes from
the front of a list, and `pop()` from the back.

```python exec
id: from-earlier-1
line = ["a", "b", "c"]
line.pop(0)
line.pop()
print(" ".join(line))
```

```predict
type: choice

What will the cell print?

- b
- a
  - `pop(0)` takes the first item away.
- c
  - `pop()` takes the last item away.
```

<details class="dl-answer"><summary>why</summary>

It prints `b`. `pop(0)` removes `a` from the front, and `pop()` removes
`c` from the back. A list used with `pop(0)` and `append` is a queue:
first in, first out. Used with `pop()` and `append`, it is a stack:
last in, first out.

</details>
