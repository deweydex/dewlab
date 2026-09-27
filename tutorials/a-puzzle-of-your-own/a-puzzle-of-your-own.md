---
title: "Make it: a maze or puzzle of your own"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  mazes-and-dungeons: A dungeon with a locked door, and a key somewhere else.
  maps-and-networks: A network of computers, and the one that would cut it in two.
  collections: A word list, and a word puzzle from 1879.
  puzzles: A farmer, a wolf, a goat and a cabbage, and one small boat.
---

# Make it: a maze or puzzle of your own

This series searched a list, sorted one, walked a folder tree, found
the shortest way across a map, and made change three ways. Now you
design a maze or a puzzle of your own, and the computer solves it. The
idea that makes this possible comes from [Graph search: the shortest
way there](tutorial:the-shortest-way-there). If you can list the
positions of a puzzle, and the moves from each one, then the puzzle is
a map. Breadth-first search finds the fewest moves to the goal.

## A first step

A *state* is everything you need to know about a puzzle at one moment.
In this first puzzle, the state is one number. You start at 1, and
each move either adds 1 or doubles the number. The goal is 10.

```python exec
id: a-first-step-1
def solve(start, moves, is_goal):
    """A shortest list of states from start to a goal, and how many states were found."""
    came_from = {start: None}
    to_visit = [start]
    while to_visit:
        state = to_visit.pop(0)
        if is_goal(state):
            way = [state]
            while came_from[way[-1]] is not None:
                way.append(came_from[way[-1]])
            way.reverse()
            return way, len(came_from)
        for next_state in moves(state):
            if next_state not in came_from:
                came_from[next_state] = state
                to_visit.append(next_state)
    return None, len(came_from)


def add_one_or_double(number):
    return [number + 1, number * 2]


def is_ten(number):
    return number == 10


way, found = solve(1, add_one_or_double, is_ten)
print("states found:", found)
print("the way:", way)
print("moves:", len(way) - 1)
```

```predict
type: number

How many moves does the shortest way from 1 to 10 take?
```

Four: 1, 2, 4, 5, 10. The search found 15 states before it reached 10.

`solve` is the breadth-first search from the graph search page, with
two changes. First, it does not need the whole map before it starts.
`moves` and `is_goal` are functions, given to `solve` like any other
value, and `solve` calls them when it needs them. It calls
`moves(state)` to find the neighbours of a state only when the search
reaches that state. This puzzle needs that, because its map has no
end: from any number, you can always add 1 again. A map written out
first, as a dictionary, could never be finished. Second, `solve` stops
as soon as it takes a goal from the list, and returns the way there.

Every puzzle on this page uses the same `solve`. What changes is what a
state is, which moves are allowed, and what counts as the goal.

## Make it yours

<div class="dl-world" data-world="mazes-and-dungeons">

A dungeon with a locked door. `S` is the start and `T` is the
treasure. `K` is a key, and `D` is a door that opens only for somebody
who holds the key. The treasure is behind the door.

Now the square you stand on is not enough to say where you are in the
puzzle. The state is the square *and* whether you hold the key. So one
square can be two different states: with the key, and without it.

Some questions your puzzle could answer:

- How many steps does the shortest way take? How many of them are
  spent fetching the key?
- If you add a second key and a second door, how many states do you
  expect the search to find? Say a number first, then run it.
- Can you design a small dungeon with a very long shortest way?

```python exec
id: make-it-yours-1--mazes-and-dungeons
dungeon = ["S...#..#.T",
           ".##.#..#..",
           ".#.....D..",
           ".#.#######",
           "K........."]


def where(letter):
    """The (row, column) of a letter in the dungeon."""
    for r, row in enumerate(dungeon):
        if letter in row:
            return (r, row.index(letter))


def dungeon_moves(state):
    """Every state one step away. A state is (row, column, has_key)."""
    r, c, has_key = state
    next_states = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        rr, cc = r + dr, c + dc
        if not (0 <= rr < len(dungeon) and 0 <= cc < len(dungeon[0])):
            continue
        square = dungeon[rr][cc]
        if square == "#" or (square == "D" and not has_key):
            continue
        next_states.append((rr, cc, has_key or square == "K"))
    return next_states


treasure = where("T")


def at_treasure(state):
    return (state[0], state[1]) == treasure


start_row, start_col = where("S")
way, found = solve((start_row, start_col, False), dungeon_moves, at_treasure)
print("states found:", found)
print("steps:", len(way) - 1)
print("steps to the key:", [state[2] for state in way].index(True))

picture = [list(row) for row in dungeon]
for r, c, has_key in way:
    if picture[r][c] == ".":
        picture[r][c] = "*"
for row in picture:
    print("".join(row))
```

</div>

<div class="dl-world" data-world="maps-and-networks">

A network of computers in a college. Each wire joins two computers,
and a message can travel along a wire in either direction. One step
along a wire is called a *hop*. The puzzle is to find which computer,
if it broke, would cut the network in two.

To answer it, the cell breaks each computer in turn, and searches from
one of the others. The goal is never reached, so the search finds
every computer it can, and then stops. If it finds fewer than all of
them, some computers can no longer reach each other.

Some questions your puzzle could answer:

- Which computers would cut the network in two? Can you add one wire,
  so that no single broken computer can do that?
- Which two computers are furthest apart, in hops?
- What would a network of your own look like: the rooms of a house,
  the stops on a bus route, the computers in your home?

```python exec
id: make-it-yours-1--maps-and-networks
wires = [("front-desk", "library"), ("front-desk", "office"),
         ("library", "office"), ("library", "lab-1"), ("office", "lab-1"),
         ("lab-1", "server-room"), ("server-room", "lab-2"),
         ("server-room", "studio"), ("lab-2", "studio"),
         ("studio", "workshop"), ("lab-2", "workshop"),
         ("workshop", "canteen")]

network = {}
for a, b in wires:
    if a not in network:
        network[a] = []
    if b not in network:
        network[b] = []
    network[a].append(b)
    network[b].append(a)


def hops(computer):
    return network[computer]


def is_canteen(computer):
    return computer == "canteen"


way, found = solve("front-desk", hops, is_canteen)
print("front desk to canteen:", way)
print("hops:", len(way) - 1)


def never(computer):
    """A goal that is never reached, so the search finds everything it can."""
    return False


for broken in network:
    def hops_without(computer):
        return [other for other in network[computer] if other != broken]

    others = [computer for computer in network if computer != broken]
    way, reached = solve(others[0], hops_without, never)
    if reached < len(others):
        print("if", broken, "breaks,", others[0], "can no longer reach",
              len(others) - reached, "of the others")
```

</div>

<div class="dl-world" data-world="collections">

In 1879, Lewis Carroll, who wrote *Alice's Adventures in Wonderland*,
published a word puzzle he called Doublets. You turn one word into
another, one letter at a time, and every step must be a real word. His
first example turned HEAD into TAIL. Here the collection is a small
word list. Two words are neighbours when they differ in exactly one
letter.

Some questions your puzzle could answer:

- Can the search get from `head` to `warm`? If not, which one word,
  added to the list, would join them?
- Which word in the list is furthest from `head`?
- Can you make a word list of your own, with five-letter words, or
  words in another language you know?

```python exec
id: make-it-yours-1--collections
words = """head heal heat heap hear held help hell hall hail tail tall
tell teal seal sell sale sail mail meal melt belt bell ball bale bold
cold cord card ward warm word wore were tale tile till toll""".split()


def one_letter_apart(a, b):
    """True when two words of the same length differ in exactly one place."""
    differences = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            differences = differences + 1
    return differences == 1


def next_words(word):
    return [other for other in words if one_letter_apart(word, other)]


def is_tail(word):
    return word == "tail"


way, found = solve("head", next_words, is_tail)
print("words found:", found)
print("the chain:", ", ".join(way))
print("steps:", len(way) - 1)
```

The search finds a chain of five steps. Carroll's own chain was head,
heal, teal, tell, tall, tail: also five steps, but a different chain.
There can be more than one shortest way. Breadth-first search gives the
first one it reaches, and which one that is depends on the order of the
word list.

</div>

<div class="dl-world" data-world="puzzles">

A farmer must take a wolf, a goat and a cabbage across a river. The
boat holds the farmer and one more. If the farmer is not there, the
wolf eats the goat, and the goat eats the cabbage. This puzzle is more
than 1,000 years old.

A state says which bank each of the four is on: `0` for the near bank,
and `1` for the far bank. A move is the farmer crossing, alone or with
one passenger from the same bank. A move is allowed only if nobody is
eaten afterwards.

Some questions your puzzle could answer:

- What if the boat holds the farmer and two more? Is the puzzle still
  a puzzle?
- With four on the bank there are 16 possible states. How many would
  there be with a fifth passenger, and how many does the search find?
- Can you invent new rules, or a new danger, and still find a way
  across?

```python exec
id: make-it-yours-1--puzzles
names = ["farmer", "wolf", "goat", "cabbage"]


def nobody_eaten(state):
    farmer, wolf, goat, cabbage = state
    if wolf == goat and farmer != goat:
        return False
    if goat == cabbage and farmer != goat:
        return False
    return True


def crossings(state):
    """Every state one crossing away: the farmer alone, or with one passenger."""
    next_states = []
    for i in range(len(state)):
        if state[i] != state[0]:
            continue
        new = list(state)
        new[0] = 1 - state[0]
        new[i] = 1 - state[i]
        new = tuple(new)
        if nobody_eaten(new):
            next_states.append(new)
    return next_states


def all_across(state):
    return state == (1, 1, 1, 1)


way, found = solve((0, 0, 0, 0), crossings, all_across)
print("states found:", found)
print("crossings:", len(way) - 1)
for state in way:
    near = [name for name, side in zip(names, state) if side == 0]
    far = [name for name, side in zip(names, state) if side == 1]
    print("near:", near, "far:", far)
```

The loop in `crossings` starts at `i = 0`, the farmer. For that one,
both lines set `new[0]`, to the same value, so the farmer crosses
alone.

</div>

## How big is your puzzle?

Every search on this page prints how many states it found. That count
is the work the search did.

A state with more parts can have many more states. In the dungeon,
every square can be reached with the key or without it, so one key can
double the number of states. A second key can double it again, and ten
keys can multiply it by 1,024. On the river, each of the four can be on
either bank: 2 × 2 × 2 × 2 = 16 possible states. A fifth passenger
makes 32. This is the same *exponential* growth as brute force on
[Making change](tutorial:three-ways-to-make-change#how-the-work-grows):
each thing you add multiplies the work.

Before you make your puzzle bigger, say how many states you expect the
search to find. Then run it, and compare.

## If you want more

- Can you make a puzzle with no way to the goal? What does `solve`
  return, and how many states does it find before it stops?
- Change `pop(0)` to `pop()` in `solve`. Does it still find a way? Is
  the way still a shortest one?
- In the first step, the fewest moves from 1 to 100 is 8. Can you find
  them by working backwards from 100, halving when you can and taking
  away 1 when you cannot? Does that always give the fewest moves?

## Show somebody

Show your puzzle to somebody, or write a few lines for yourself:

- What is your puzzle, and what is a state in it?
- How many moves does the shortest way take, and how many states did
  the search find?
- Which page of this series did each part of your code come from?
- If somebody gave you another hour, what would you add?

## Where to read more

Carroll, L. (1879). *Doublets: A Word-Puzzle*. Macmillan. Carroll first
published the puzzle in the magazine *Vanity Fair* in March 1879, and
this short book followed later that year. He called the two words at
the ends "a Doublet", the words between them "Links", and the whole
list "a Chain".
