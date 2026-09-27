---
title: "Make it: a simulation of your own"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  living-systems: A forest that grows back after fires, as a grid of cells.
  queues-and-crowds: A café with two tills, and the question of how to queue for them.
  spread: A disease moving across a grid of towns.
  space-and-physics: Specks of dust, knocked about at random.
---

# Make it: a simulation of your own

This series turned chance into a tool: random numbers and seeds, darts
that measure an area, a model that corrects itself, a queue that times
every wait, and a ball stepped forward in time. Now you use them to
make a simulation of your own, in the world you choose. A simulation
here means a model with chance or time in it, run many times, that
answers a question you care about. And every model leaves something
out, so yours will name one thing it leaves out.

## A first step

In every world, the first step is the same. One run of a simulation,
under a stated seed, gives one answer. Many runs, with many seeds, show
how much the answer changes from run to run. Here is that skeleton,
with a placeholder for one run: ten coin flips.

```python exec
id: a-first-step-1
import random


def one_run(seed):
    """One run of the simulation, under a stated seed. Here: heads in ten flips."""
    random.seed(seed)
    return sum(1 for _ in range(10) if random.random() < 0.5)


results = [one_run(seed) for seed in range(100)]
print("average:", sum(results) / len(results))
print("lowest and highest:", min(results), max(results))
```

Your own `one_run` will do something bigger. Keep the seed, and keep
the loop over seeds. Then you can always run one result again, and you
always know how far your answer can move by luck alone.

## Make it yours

<div class="dl-world" data-world="living-systems">

A forest that grows back after fires. The forest is a grid of cells,
and each cell is empty, a tree, or on fire. Every step, the rules are
the same:

- A cell on fire burns out, and becomes empty.
- A tree next to a fire catches fire. Now and then, lightning sets a
  tree on fire anyway.
- An empty cell grows a new tree, now and then.

A grid of cells that all follow the same simple rules, looking only at
their neighbours, is called a *cellular automaton*.

Some questions your simulation could answer:

- How much of the forest is trees, on average, once it settles? Does it
  settle at all?
- How big are the fires? Are most fires small, with a few very large?
- What happens if trees grow faster, or lightning strikes more often?

```python exec
id: make-it-yours-1--living-systems
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

EMPTY, TREE, FIRE = 0, 1, 2
SIZE = 30            # the grid is SIZE by SIZE cells
GROW = 0.03          # the chance an empty cell grows a tree, each step
LIGHTNING = 0.0005   # the chance lightning sets a tree on fire, each step
random.seed(1)

forest = [[TREE if random.random() < 0.5 else EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def neighbour_on_fire(forest, row, col):
    """True when a cell above, below, left or right is on fire."""
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < SIZE and 0 <= c < SIZE and forest[r][c] == FIRE:
            return True
    return False


def step(forest):
    """The next state of every cell, by the three rules."""
    new = [[EMPTY] * SIZE for _ in range(SIZE)]
    for row in range(SIZE):
        for col in range(SIZE):
            cell = forest[row][col]
            if cell == TREE:
                if neighbour_on_fire(forest, row, col) or random.random() < LIGHTNING:
                    new[row][col] = FIRE
                else:
                    new[row][col] = TREE
            elif cell == EMPTY and random.random() < GROW:
                new[row][col] = TREE
    return new


tree_share = []
for _ in range(300):
    forest = step(forest)
    tree_share.append(sum(row.count(TREE) for row in forest) / SIZE ** 2)

fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
axes[0].imshow(forest, cmap=ListedColormap(["#e8dcc0", "#2e7d32", "#d84315"]), vmin=0, vmax=2)
axes[0].set_title("the forest after 300 steps")
axes[0].set_xticks([])
axes[0].set_yticks([])
axes[1].plot(tree_share)
axes[1].set_xlabel("step")
axes[1].set_ylabel("share of cells with a tree")
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

A café with two tills. Customers can wait in one shared queue, and go
to whichever till is free. Or each till can have its own queue, and a
customer picks one at random when they arrive. Which is quicker for the
customers? This starter builds both, from the queue in
[Simulating a queue: how busy is too busy?](tutorial:when-a-queue-never-clears),
with four chances of an arrival in each step.

Some questions your simulation could answer:

- How much longer is the average wait with a queue for each till, at
  different levels of busy?
- What if customers join the *shorter* queue, not a random one?
- What does the longest wait look like, for each way of queueing? Which
  one feels fairer to the customer?

```python exec
id: make-it-yours-1--queues-and-crowds
import random


def arrivals(arrival_prob, chances=4):
    """How many customers arrive this step: one check for each chance."""
    return sum(1 for _ in range(chances) if random.random() < arrival_prob)


def shared_queue(steps, arrival_prob, tills=2):
    """One queue; each till takes the next customer when it is free."""
    queue, waits = [], []
    for step in range(steps):
        for _ in range(arrivals(arrival_prob)):
            queue.append(step)
        for _ in range(min(len(queue), tills)):
            waits.append(step - queue.pop(0))
    return waits


def queue_per_till(steps, arrival_prob, tills=2):
    """A queue for each till; each customer picks one at random."""
    queues = [[] for _ in range(tills)]
    waits = []
    for step in range(steps):
        for _ in range(arrivals(arrival_prob)):
            random.choice(queues).append(step)
        for queue in queues:
            if queue:
                waits.append(step - queue.pop(0))
    return waits


for arrival_prob in [0.4, 0.45]:
    random.seed(1)
    shared = shared_queue(20000, arrival_prob)
    random.seed(1)
    separate = queue_per_till(20000, arrival_prob)
    print(f"{2 * arrival_prob:.0%} busy: shared {sum(shared) / len(shared):.2f} steps, "
          f"a queue each {sum(separate) / len(separate):.2f} steps")
```

</div>

<div class="dl-world" data-world="spread">

A disease moving across a grid of towns. It starts in the town in the
middle. Each step, every sick town can pass it to each town beside it,
with a chance `CATCH`. A town stays sick for `SICK_FOR` steps, then
recovers, and cannot catch it again.

Some questions your simulation could answer:

- What share of the towns is ever sick? How does that change with
  `CATCH`? Is there a value where it changes suddenly?
- When is the most towns sick at once, and how many?
- What happens if some towns, chosen at random, are protected at the
  start and can never catch it?

```python exec
id: make-it-yours-1--spread
import random
import matplotlib.pyplot as plt

SIZE = 30        # the grid is SIZE by SIZE towns
CATCH = 0.3      # the chance a sick town passes it to a town beside it, each step
SICK_FOR = 3     # how many steps a town stays sick


def one_outbreak(seed):
    """Sick towns after each step, and how many towns were ever sick."""
    random.seed(seed)
    days_left = {(SIZE // 2, SIZE // 2): SICK_FOR}    # each sick town: steps of illness left
    recovered = set()
    sick_counts = []
    while days_left:
        new_cases = set()
        for row, col in days_left:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                town = (row + dr, col + dc)
                if (0 <= town[0] < SIZE and 0 <= town[1] < SIZE
                        and town not in days_left and town not in recovered
                        and random.random() < CATCH):
                    new_cases.add(town)
        for town in list(days_left):
            days_left[town] -= 1
            if days_left[town] == 0:
                del days_left[town]
                recovered.add(town)
        for town in new_cases:
            days_left[town] = SICK_FOR
        sick_counts.append(len(days_left))
    return sick_counts, len(recovered)


sick_counts, ever_sick = one_outbreak(seed=1)
print(f"{ever_sick} of {SIZE * SIZE} towns were ever sick, over {len(sick_counts)} steps")
plt.plot(sick_counts)
plt.xlabel("step")
plt.ylabel("towns sick at once")
```

</div>

<div class="dl-world" data-world="space-and-physics">

Specks of dust in still air, knocked about by molecules too small to
see. Each step, each speck moves one step up, down, left or right, at
random. This starter follows 200 specks for 400 steps, and plots their
average distance from where they started.

Some questions your simulation could answer:

- How far does a speck get, on average, after 100 steps? After 400? How
  close is that to the square root of the number of steps, the dashed
  line?
- Put the specks in a box. How long until the first one reaches a wall?
- What if a gentle breeze makes one direction a little more likely?

```python exec
id: make-it-yours-1--space-and-physics
import math
import random
import matplotlib.pyplot as plt

SPECKS = 200
STEPS = 400
random.seed(1)

average_distance = [0.0] * STEPS
for _ in range(SPECKS):
    x, y = 0, 0
    for step in range(STEPS):
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        x, y = x + dx, y + dy
        average_distance[step] += math.sqrt(x * x + y * y) / SPECKS

plt.plot(range(1, STEPS + 1), average_distance, label="average distance")
plt.plot(range(1, STEPS + 1), [math.sqrt(n) for n in range(1, STEPS + 1)],
         linestyle="--", label="square root of the steps")
plt.xlabel("steps")
plt.ylabel("distance from the start")
plt.legend()
```

</div>

## One thing it leaves out

Every model leaves things out: that is what makes it a model and not
the world. The queue page left out people who arrive in groups, and the
wait at 90% busy went from about 2 steps to 17 when they came back in.

Name one thing your simulation leaves out. Then say, before you test
it, whether putting it back would make your answer bigger or smaller.
If you can, put it back in, and see whether you were right.

## If you want more

- Can your simulation run many seeds, and report the spread of its
  answer as well as the average?
- Can it draw a picture of one run, so that somebody else can see what
  happens step by step?
- Can you name every number in it at the top, like a lab bench, so
  that somebody else can change them?

## Show somebody

Show your simulation to somebody, or write a few lines for yourself:

- What question does your simulation answer, and which page of this
  series did each part come from?
- Which result surprised you?
- What does your simulation leave out, and what did you think putting
  it back would do?
- If somebody gave you another hour, what would you add?
