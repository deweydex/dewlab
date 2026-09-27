---
title: "Simulating a queue: how busy is too busy? — Practice"
practice_for: when-a-queue-never-clears
year: "2026-2027"
version: 2026.09.27.1
worlds:
  living-systems: A cleaning station on a coral reef, where fish wait their turn with the cleaner wrasse.
  queues-and-crowds: The check-in desks at a spaceport, on the morning rush.
  spread: A clinic during an outbreak, where patients wait to see a doctor.
  space-and-physics: A meteor camera, whose pictures wait for the computers to check them.
---

# Simulating a queue: how busy is too busy? — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

Run this cell first. It holds the tutorial's two functions, with one
more setting: `chances`, the number of checks for an arrival in each
step. The tutorial always used 2.

```python exec
id: tools-1
import random


def arrivals_this_step(arrival_prob, chances=2):
    """How many arrive this step: one check for each chance."""
    return sum(1 for _ in range(chances) if random.random() < arrival_prob)


def simulate_waits(steps, arrival_prob, service_capacity, chances=2):
    """The wait of every item served, in steps, in the order they were served."""
    queue = []
    waits = []
    for step in range(steps):
        for _ in range(arrivals_this_step(arrival_prob, chances)):
            queue.append(step)
        for _ in range(min(len(queue), service_capacity)):
            waits.append(step - queue.pop(0))
    return waits


print("ready")
```

## Busy and waiting

**1.** Can you write `utilisation(arrival_prob, service_capacity,
chances=2)`? It returns the average arrivals per step, divided by the
service capacity.

```python exec
id: busy-and-waiting-1
def utilisation(arrival_prob, service_capacity, chances=2):
    """The share of the server's capacity that the arrivals use, on average."""
    # Your code here.
```

```hint
Each chance adds `arrival_prob` to the average number of arrivals, so
the average is `chances * arrival_prob`.
```

```inputs
utilisation(0.4, 1)
utilisation(0.47, 2)
round(utilisation(0.3, 1, chances=8), 2)
```

```solution
def utilisation(arrival_prob, service_capacity, chances=2):
    """The share of the server's capacity that the arrivals use, on average."""
    return chances * arrival_prob / service_capacity
---
0.8 is stable, and well back from the hockey stick. 0.47 is a server
busy less than half the time. 2.4 is more than twice what the server
can clear: that queue never clears, however long it runs.
```

**2.** Requests arrive at a web server at random, 45 a second on
average. The server can deal with 50 a second. During a sudden busy
period, the average rises to 55 a second. What is the utilisation
before, and during? What happens to the wait in each?

<details class="dl-answer"><summary>answer</summary>

Before, the utilisation is 45 / 50 = 0.9. The queue is stable, but it
is on the steep part of the hockey stick: a small rise in requests
would make the wait much longer.

During the busy period, it is 55 / 50 = 1.1. The queue never clears,
and every request waits longer than the one before, for as long as the
busy period lasts. In the end the server's room for waiting requests
fills up, and it starts to turn requests away. This is how a service
that was fine yesterday can fail during a busy period today.

</details>

**3.** The tutorial gave the average wait for its model as
$\dfrac{u}{4(1 - u)}$ steps. This cell runs a server that is 75% busy.

```python exec
id: busy-and-waiting-2
random.seed(1)
waits = simulate_waits(20000, arrival_prob=0.375, service_capacity=1)
print(round(sum(waits) / len(waits), 2))
```

```predict
type: number
tolerance: 0.15

Use the formula first. What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

The formula gives $\dfrac{0.75}{4 \times 0.25} = 0.75$ steps, and the
run gives 0.77. A long run of a queue this far from full settles close
to the formula.

</details>

## The same average, different arrivals

**4.** Each of these four servers is 90% busy. The only difference is
how the arrivals come: 1, 2, 4 or 8 chances each step, each chance
smaller so that the average stays the same. Will the four average waits
be the same? Decide, then run the cell.

```python exec
id: the-same-average-1
for chances in [1, 2, 4, 8]:
    random.seed(1)
    waits = simulate_waits(20000, 0.9 / chances, 1, chances)
    print(f"{chances} chances: average wait {sum(waits) / len(waits):.2f} steps")
```

<details class="dl-answer"><summary>answer</summary>

No: 0.00, 2.27, 3.23 and 3.88 steps. With one chance a step, no more
than one item can arrive in a step, and the server always clears it, so
nobody ever waits. With more chances, several items can arrive in the
same step, and a burst like that has to wait. More chances means bigger
bursts, and longer waits. With 50 chances, the average wait is about
4.1 steps.

So the utilisation alone does not decide the wait. How the arrivals
bunch together decides it too, as the groups in the tutorial showed.

</details>

## Your world

**5.** With several servers, how many do you need? Can you write
`servers_needed(arrival_prob, chances, limit)`? It returns the fewest
servers whose average wait, over 20,000 steps with `random.seed(1)`, is
under `limit`.

<div class="dl-world" data-world="living-systems">

A reef's cleaning station has several cleaner wrasse, each cleaning one
fish a step. Fish arrive with 10 chances a step, each with
`arrival_prob=0.39`. How many wrasse keep the average wait under 1 step?

```python exec
id: your-world-1--living-systems
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    # Your code here.
```

```hint
Start with one server and add one at a time. Skip any number of servers
that is not more than the average arrivals, `chances * arrival_prob`:
that queue never clears, and a long run of it is slow. For the rest,
set `random.seed(1)`, run `simulate_waits`, and compare the average
wait with `limit`.
```

```inputs
servers_needed(0.39, 10, 1)
servers_needed(0.39, 10, 5)
servers_needed(0.3, 2, 1)
```

```solution
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    capacity = 1
    while True:
        if chances * arrival_prob < capacity:
            random.seed(1)
            waits = simulate_waits(20000, arrival_prob, capacity, chances)
            if sum(waits) / len(waits) < limit:
                return capacity
        capacity += 1
---
3.9 fish arrive a step on average, so 4 wrasse would be stable, at 98% busy. But a fish would wait about 2 steps. 5 wrasse bring the wait under 1, to about 0.1. To keep it under 5 steps, 4 are enough. The tutorial's single server, at `arrival_prob=0.3`, needs no help.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

The spaceport's departure hall has several check-in desks. Passengers
arrive with 8 chances a step, each with `arrival_prob=0.475`. How many
desks keep the average wait under 1 step?

```python exec
id: your-world-1--queues-and-crowds
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    # Your code here.
```

```hint
Start with one server and add one at a time. Skip any number of servers
that is not more than the average arrivals, `chances * arrival_prob`:
that queue never clears, and a long run of it is slow. For the rest,
set `random.seed(1)`, run `simulate_waits`, and compare the average
wait with `limit`.
```

```inputs
servers_needed(0.475, 8, 1)
servers_needed(0.475, 8, 5)
servers_needed(0.3, 2, 1)
```

```solution
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    capacity = 1
    while True:
        if chances * arrival_prob < capacity:
            random.seed(1)
            waits = simulate_waits(20000, arrival_prob, capacity, chances)
            if sum(waits) / len(waits) < limit:
                return capacity
        capacity += 1
---
3.8 passengers arrive a step on average, so 4 desks would be stable, at 95% busy. But a passenger would wait about 1.1 steps. 5 desks bring the wait down to about 0.06. To keep it under 5 steps, 4 are enough. The tutorial's single server, at `arrival_prob=0.3`, needs no help.
```

</div>

<div class="dl-world" data-world="spread">

During an outbreak, a clinic has several doctors, each seeing one
patient a step. Patients arrive with 6 chances a step, each with
`arrival_prob=0.49`. How many doctors keep the average wait under 2
steps?

```python exec
id: your-world-1--spread
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    # Your code here.
```

```hint
Start with one server and add one at a time. Skip any number of servers
that is not more than the average arrivals, `chances * arrival_prob`:
that queue never clears, and a long run of it is slow. For the rest,
set `random.seed(1)`, run `simulate_waits`, and compare the average
wait with `limit`.
```

```inputs
servers_needed(0.49, 6, 2)
servers_needed(0.49, 6, 5)
servers_needed(0.3, 2, 1)
```

```solution
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    capacity = 1
    while True:
        if chances * arrival_prob < capacity:
            random.seed(1)
            waits = simulate_waits(20000, arrival_prob, capacity, chances)
            if sum(waits) / len(waits) < limit:
                return capacity
        capacity += 1
---
2.94 patients arrive a step on average, so 3 doctors would be stable, at 98% busy. But a patient would wait about 4 steps. 4 doctors bring the wait down to under a tenth of a step. To keep it under 5 steps, 3 are enough. The tutorial's single server, at `arrival_prob=0.3`, needs no help.
```

</div>

<div class="dl-world" data-world="space-and-physics">

On the night of a meteor shower, several computers check the camera's
pictures, one picture a step each. Pictures arrive with 5 chances a
step, each with `arrival_prob=0.58`. How many computers keep the average
wait under 1 step?

```python exec
id: your-world-1--space-and-physics
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    # Your code here.
```

```hint
Start with one server and add one at a time. Skip any number of servers
that is not more than the average arrivals, `chances * arrival_prob`:
that queue never clears, and a long run of it is slow. For the rest,
set `random.seed(1)`, run `simulate_waits`, and compare the average
wait with `limit`.
```

```inputs
servers_needed(0.58, 5, 1)
servers_needed(0.58, 5, 5)
servers_needed(0.3, 2, 1)
```

```solution
def servers_needed(arrival_prob, chances, limit):
    """The fewest servers whose average wait, seed 1, 20,000 steps, is under limit."""
    capacity = 1
    while True:
        if chances * arrival_prob < capacity:
            random.seed(1)
            waits = simulate_waits(20000, arrival_prob, capacity, chances)
            if sum(waits) / len(waits) < limit:
                return capacity
        capacity += 1
---
2.9 pictures arrive a step on average, so 3 computers would be stable, at 97% busy. But a picture would wait about 2.2 steps. 4 computers bring the wait down to 0.03. To keep it under 5 steps, 3 are enough. The tutorial's single server, at `arrival_prob=0.3`, needs no help.
```

</div>


## From earlier

**6.** From [Comprehensions, grids and
aliasing](tutorial:comprehensions-and-grids). `arrivals_this_step`
counts with `sum(1 for ... if ...)`.

```python exec
id: from-earlier-1
print(sum(1 for x in [0.1, 0.5, 0.9] if x < 0.6))
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints 2. The comprehension makes a 1 for each value below 0.6:
there are two of them, 0.1 and 0.5. `sum` adds the 1s. In
`arrivals_this_step`, each value is a new `random.random()`, and each
one below `arrival_prob` is an arrival.

</details>

**7.** From [Random numbers: pseudo-random numbers and
seeds](tutorial:leaving-it-to-chance). The tutorial's hockey-stick cell
calls `random.seed(1)` again before every level of utilisation, not
once before the loop. Why might that be a good idea?

<details class="dl-answer"><summary>answer</summary>

Each level then starts from the same random numbers. The difference
between two levels comes from the utilisation, not from one level
happening to get a luckier run than the next. It also means each point
on the curve can be run again on its own, and gives the same number.
Seeded once before the loop, the curve would still show the hockey
stick, but each point would depend on every level that ran before it.

</details>
