---
title: "Graph search: the shortest way there"
year: "2026-2027"
version: 2026.09.27.1
covers:
  a-map-is-a-graph:
    covers: [CMPS-LO1]
  going-round-in-circles:
    covers: [CMPS-LO1]
  the-shortest-way:
    covers: [CMPS-LO1, CMPS-LO9]
  why-breadth-first:
    covers: [CMPS-LO9]
worlds:
  mazes-and-dungeons: A maze of corridors, with treasure at the far side.
  maps-and-networks: A railway between towns. The towns are made up.
  collections: The rooms of a museum, joined by doorways.
  puzzles: The water-jug puzzle, where every state of the jugs is a place on a map.
---

# Graph search: the shortest way there

A folder tree never loops back: each folder has one way in. A map is
different. From the station you can walk down one street and come back
by another. On this page we search a map for the shortest way from one
place to another. We use the breadth-first walk from
[Recursion: finding every file in a folder
tree](tutorial:finding-everything-inside-a-folder), with one addition
that loops need.

## A map is a graph

Here is a small town. Each place has a list of the places one street
away. A street works both ways, so each one appears in both lists.

```python exec
id: a-map-is-a-graph-1
import matplotlib.pyplot as plt

streets = {
    "station": ["market", "bridge"],
    "market": ["station", "school", "library"],
    "bridge": ["station", "park"],
    "school": ["market", "library", "park"],
    "library": ["market", "school"],
    "park": ["bridge", "school", "harbour"],
    "harbour": ["park"],
}

where = {"station": (0, 1), "market": (1, 2), "bridge": (1, 0), "library": (2, 3),
         "school": (2, 1.5), "park": (3, 0.5), "harbour": (4, 0.5)}
for place, neighbours in streets.items():
    for neighbour in neighbours:
        (x1, y1), (x2, y2) = where[place], where[neighbour]
        plt.plot([x1, x2], [y1, y2], color="grey")
for place, (x, y) in where.items():
    plt.plot(x, y, "o", markersize=10)
    plt.annotate(place, (x, y), textcoords="offset points", xytext=(0, 10), ha="center")
plt.axis("off")
```

A map like this is called a *graph*. The places are its *nodes*, and
the streets that join them are its *edges*. A folder tree is a graph
too, one with no loops. The web is a graph: pages are the nodes, and
links are the edges.
[Markov chains: where repeated steps
settle](tutorial:where-chains-lead#ranking-a-small-web) walked a small
web at random, to rank its pages. Here we walk a graph in order, to
find a way through it.

## Going round in circles

Here is the breadth-first walk from the folder page, with `pop(0)`,
started at the station. A folder's subfolders are now a place's
neighbours. The cell stops it after 12 visits.

```python exec
id: going-round-in-circles-1
order = []
to_visit = ["station"]
while to_visit and len(order) < 12:
    place = to_visit.pop(0)
    order.append(place)
    to_visit.extend(streets[place])
print(order)
```

The station comes back, and the market, and the bridge. The market
leads back to the station, which leads to the market again. On a map
with loops, this walk never ends: it goes round in circles. A folder
tree could never do that, because nothing leads back up.

The fix is to remember every place we have already found, in a set,
and never add one twice.

```python exec
id: going-round-in-circles-2
def visit_order(graph, start):
    """Every place, breadth-first from start, each one once."""
    order = []
    visited = {start}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        order.append(place)
        for neighbour in graph[place]:
            if neighbour not in visited:
                visited.add(neighbour)
                to_visit.append(neighbour)
    return order

print(" ".join(visit_order(streets, "station")))
```

```predict
type: choice

What will the cell print? Look at the map first.

- station market bridge school library park harbour
- station market school library park harbour bridge
  - It follows one street as far as it goes, then comes back.
- station bridge park harbour market school library
  - It goes straight towards the harbour.
```

Each place goes into `visited` as soon as it is found, and so it joins
`to_visit` only once. The walk goes out in rings: first the station,
then every place one street away, then every place two streets away.

## The shortest way

To find a *way* to a place, not only the place, the walk needs to
remember one more thing: for each place, the place it was reached from.
Then, once the walk has reached the target, we can follow those back to
the start.

```python exec
id: the-shortest-way-1
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


came_from = reached_from(streets, "station")
print(came_from)
```

`came_from` is a dictionary, so it does two jobs at once. Its keys are
the places already found, so it replaces `visited`. Its values say
where each one was found from. The station's value is `None`: it is the
start.

Follow the harbour back: the harbour was reached from the park, the
park from the bridge, and the bridge from the station. So the way from
the station to the harbour is station, bridge, park, harbour: three
streets.

<details class="dl-answer"><summary>Walking back, in code</summary>

```python
way = ["harbour"]
while came_from[way[-1]] is not None:
    way.append(came_from[way[-1]])
way.reverse()
print(way)
```

`way[-1]` is the last place added. The loop keeps adding the place it
was reached from, until it reaches the start, whose value is `None`.
Then `reverse()` turns the list round, so it runs from the start.

</details>

## Why breadth-first?

Breadth-first finds every place one street away before any place two
streets away. So the first time it reaches a place, it has reached it
by the fewest streets possible. The way it finds is always a shortest
way.

Depth-first does not promise that. Here is the same walk with `pop()`
in place of `pop(0)`, and the way it finds to the library.

```python exec
id: why-breadth-first-1
def reached_from_depth_first(graph, start):
    came_from = {start: None}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop()
        for neighbour in graph[place]:
            if neighbour not in came_from:
                came_from[neighbour] = place
                to_visit.append(neighbour)
    return came_from


for walk in [reached_from, reached_from_depth_first]:
    came_from = walk(streets, "station")
    way = ["library"]
    while came_from[way[-1]] is not None:
        way.append(came_from[way[-1]])
    print(walk.__name__, list(reversed(way)))
```

Breadth-first finds station, market, library: two streets. Depth-first
goes down the bridge's branch first, round by the park and the school,
and reaches the library by four streets. It found *a* way, but not the
shortest. One argument, `pop()` or `pop(0)`, again makes all the
difference.

## Your world

Can you write `shortest_way(graph, start, target)`? It returns the
list of places on a shortest way from `start` to `target`, or `None` if
there is no way there.

<div class="dl-world" data-world="mazes-and-dungeons">

A maze of corridors: `#` is a wall and `.` is a corridor. You start at `S`, in the top-left corner, and the treasure is at `T`. The cell turns the maze into a graph: every corridor square is a place, and its neighbours are the corridor squares above, below, left and right.

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


def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    # Your code here.
```

```hint
Build `came_from` with the breadth-first walk from this page. If the
target is not in it, there is no way there. Otherwise, walk back from
the target to the start, and turn the list round.
```

```inputs
len(shortest_way(maze_map, (0, 0), (3, 7))) - 1
shortest_way(maze_map, (0, 0), (3, 7))[:4]
shortest_way(maze_map, (0, 0), (0, 7))
```

```solution
def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    came_from = {start: None}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in came_from:
                came_from[neighbour] = place
                to_visit.append(neighbour)
    if target not in came_from:
        return None
    way = [target]
    while came_from[way[-1]] is not None:
        way.append(came_from[way[-1]])
    way.reverse()
    return way
---
The treasure is 12 steps away: down the left side, along the middle row, and round the bottom. The way to the top-right corner, `(0, 7)`, is 11 steps, up through the gap at column 3. The graph turned a picture into places and neighbours, and the same search did the rest.
```

</div>

<div class="dl-world" data-world="maps-and-networks">

A railway joins nine towns. Which route from Northport to Harbourtown passes through the fewest stations?

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


def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    # Your code here.
```

```hint
Build `came_from` with the breadth-first walk from this page. If the
target is not in it, there is no way there. Otherwise, walk back from
the target to the start, and turn the list round.
```

```inputs
shortest_way(rail, "Northport", "Harbourtown")
shortest_way(rail, "Kilbeg", "Fenmoor")
shortest_way(rail, "Northport", "Atlantis")
```

```solution
def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    came_from = {start: None}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in came_from:
                came_from[neighbour] = place
                to_visit.append(neighbour)
    if target not in came_from:
        return None
    way = [target]
    while came_from[way[-1]] is not None:
        way.append(came_from[way[-1]])
    way.reverse()
    return way
---
Northport, Ashford, Carrow, Fenmoor, Harbourtown: four journeys. The other way, by Kilbeg and Glenview, takes five. From Kilbeg to Fenmoor, the route through Dunmore and Carrow is shorter than going back through Northport. A town that is not on the railway gives `None`.
```

</div>

<div class="dl-world" data-world="collections">

A museum's rooms are joined by doorways, and some rooms have more than one way in. What is the shortest walk from the entrance to the dinosaur gallery?

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


def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    # Your code here.
```

```hint
Build `came_from` with the breadth-first walk from this page. If the
target is not in it, there is no way there. Otherwise, walk back from
the target to the start, and turn the list round.
```

```inputs
shortest_way(floor, "entrance", "dinosaur gallery")
shortest_way(floor, "entrance", "star room")
shortest_way(floor, "entrance", "attic")
```

```solution
def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    came_from = {start: None}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in came_from:
                came_from[neighbour] = place
                to_visit.append(neighbour)
    if target not in came_from:
        return None
    way = [target]
    while came_from[way[-1]] is not None:
        way.append(came_from[way[-1]])
    way.reverse()
    return way
---
Through the hall of minerals and the hall of fossils: three doorways. The walk round by the map room and the star room takes four. To reach the star room, the hall of minerals is the quicker way in, not the shop and the café. A room that is not on the plan gives `None`.
```

</div>

<div class="dl-world" data-world="puzzles">

You have a 3-litre jug and a 5-litre jug, and a tap. You can fill a jug, empty it, or pour one into the other until one is empty or the other is full. How do you measure exactly 4 litres? Every state of the two jugs, `(small, big)`, is a place, and each move leads to a neighbouring state. The cell builds that graph.

```python exec
id: your-world-1--puzzles
def moves(state):
    """Every state one move away from (small, big), for jugs of 3 and 5 litres."""
    small, big = state
    pour_in = min(small, 5 - big)     # pour the small jug into the big one
    pour_out = min(big, 3 - small)    # pour the big jug into the small one
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


def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    # Your code here.
```

```hint
Build `came_from` with the breadth-first walk from this page. If the
target is not in it, there is no way there. Otherwise, walk back from
the target to the start, and turn the list round.
```

```inputs
shortest_way(jugs, (0, 0), (3, 4))
len(jugs)
len(shortest_way(jugs, (0, 0), (0, 4))) - 1
```

```solution
def shortest_way(graph, start, target):
    """A shortest list of places from start to target, or None."""
    came_from = {start: None}
    to_visit = [start]
    while to_visit:
        place = to_visit.pop(0)
        for neighbour in graph[place]:
            if neighbour not in came_from:
                came_from[neighbour] = place
                to_visit.append(neighbour)
    if target not in came_from:
        return None
    way = [target]
    while came_from[way[-1]] is not None:
        way.append(came_from[way[-1]])
    way.reverse()
    return way
---
Six moves: fill the big jug, pour it into the small one, empty the small one, pour again, fill the big jug, and top up the small one. That leaves 4 litres in the big jug. There are 16 states the jugs can reach, and a search over them finds the answer that puzzles people for minutes. To have 4 litres and an empty small jug takes one move more.
```

</div>
## Looking back

A tree has one way to each folder. A graph can have many ways to each
place, and loops that lead back. Two small changes turned the folder
walk into a map search: a record of every place already found, so that
the walk never goes round in circles, and a note of where each place
was found from, so that the way can be followed back. Breadth-first
then finds the shortest way, because it reaches every place in the
order of how far away it is.

Every map app, every game character that walks round a wall, and every
network that sends a message by the fewest hops starts from this idea.
Most of them add distances to the edges, since a long road is not the
same as a short one. What would have to change here, if some streets
were longer than others?

## Where to read more

Sedgewick, R. and Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
Chapter 4.1 builds breadth-first search on a graph, with the same
`came_from` idea, which it calls `edgeTo`. It goes much further than
this page, into maps whose roads have lengths.

Reducible (2020). *Breadth First Search (BFS): Visualized and Explained.*
<https://www.youtube.com/watch?v=xlVX7dXLS64>. It walks through
breadth-first search in pictures, with examples, and then writes the
code. Watch it after the section on why breadth-first finds
the shortest way.

Reducible (2020). *Depth First Search (DFS) Explained: Algorithm,
Examples, and Code.* <https://www.youtube.com/watch?v=PMMc4VsIacU>. This
is the other walk from this page, the one that goes as deep as it can
first. It has a recursive version and a loop version, as [Recursion:
finding every file in a folder
tree](tutorial:finding-everything-inside-a-folder) does.
