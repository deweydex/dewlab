---
title: "Simulating a queue: how busy is too busy?"
year: "2026-2027"
version: 2026.09.26.1
covers:
  arrivals-you-cannot-predict-one-at-a-time:
    covers: [CMPS-LO6]
  timing-every-wait:
    covers: [CMPS-LO6]
  the-hockey-stick:
    covers: [CMPS-LO6]
    touches: [CMPS-LO3]
  past-full-a-queue-that-never-clears:
    covers: [CMPS-LO6]
  is-this-a-good-model-of-a-real-queue:
    touches: [CMPS-LO3]
worlds:
  living-systems: A cleaning station on a coral reef, where fish wait their turn with a cleaner wrasse.
  queues-and-crowds: The check-in desk at a spaceport, on the morning rush.
  spread: A clinic during an outbreak, where patients wait to see the doctor.
  space-and-physics: A meteor camera, whose pictures wait for the computer to check them.
---

# Simulating a queue: how busy is too busy?

Think of a check-in desk, a coffee counter, or a web server's list of
waiting requests. They all work the same way:

1. Things arrive at moments nobody can predict.
2. Something deals with them at a fixed rate.
3. A queue builds up in between.

The people in the queue care about one thing: how long they wait. On
this page we simulate a queue, time every wait, and measure how the
wait changes as the server gets busier. The answer surprised the
engineers who first measured it, and it still surprises the people who
plan shops, hospitals and computer systems.

## Arrivals you cannot predict, one at a time

We split time into steps. In each step, we check twice whether something
new has arrived, like flipping a coin twice. Then we count how many times
the answer was yes. So each step brings 0, 1 or 2 new arrivals.

The function below does this with a short form we have not used much
yet. `sum(1 for _ in range(2) if random.random() < arrival_prob)` works
like a list comprehension from
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids). It
makes a 1 for each of the two checks that gives yes, and `sum` adds
up the 1s.

```python exec
id: arrivals-you-cannot-predict-one-at-a-time-1
import random

random.seed(1)

def arrivals_this_step(arrival_prob):
    """0, 1, or 2 new arrivals, checked as two independent chances."""
    return sum(1 for _ in range(2) if random.random() < arrival_prob)

print([arrivals_this_step(0.3) for _ in range(10)])
```

`arrival_prob` is the chance that each of the two checks gives yes.
Over many steps, the average number of arrivals per step is
`2 * arrival_prob`. Keep that number in mind. It decides everything that
follows.

A queue needs one more thing: something that deals with what has
arrived. We call that the *server*. `service_capacity` is the most items
the server can clear in one step, however many are waiting.

## Timing every wait

To time the waits, the queue has to remember when each item arrived. So
our queue is a list of arrival steps, oldest first. When the server
takes an item from the front, that item's wait is the step now, minus
the step it arrived.

```python exec
id: timing-every-wait-1
def simulate_waits(steps, arrival_prob, service_capacity):
    """The wait of every item served, in steps, in the order they were served."""
    queue = []    # the step each waiting item arrived, oldest first
    waits = []
    for step in range(steps):
        for _ in range(arrivals_this_step(arrival_prob)):
            queue.append(step)
        for _ in range(min(len(queue), service_capacity)):
            waits.append(step - queue.pop(0))
    return waits


random.seed(1)
waits = simulate_waits(200, arrival_prob=0.3, service_capacity=1)
print(len(waits), "served")
print("average wait:", round(sum(waits) / len(waits), 2), "steps")
print("longest wait:", max(waits), "steps")
```

Change `arrival_prob` to `0.45` and run the cell again. What happens to
the average wait? And to the longest?

<details class="dl-answer"><summary>What each line does</summary>

1. `queue` holds the step at which each waiting item arrived. The
   oldest is at the front, at position 0.
2. For each arrival in this step, `queue.append(step)` adds its arrival
   step to the back.
3. `min(len(queue), service_capacity)` is how many the server takes: as
   many as it can, but never more than are waiting.
4. `queue.pop(0)` removes the item at the front, the one that has waited
   longest, and returns its arrival step.
5. `step - queue.pop(0)` is that item's wait. An item served in the step
   it arrived waited 0 steps.

</details>

With `arrival_prob=0.3`, most items do not wait at all. On average 0.6
items arrive each step, and the server can clear 1. So it is busy about
60% of the time, and idle the rest.

The share of its capacity that the server uses is called its
*utilisation*:

$$\text{utilisation} = \frac{\text{average arrivals per step}}{\text{service capacity}} = \frac{2 \times \text{arrival\_prob}}{\text{service\_capacity}}$$

## The hockey stick

At 60% busy, the average wait in a long run is about 0.4 steps. The
next server is 90% busy: one and a half times as busy. The cell runs it
for 20,000 steps and prints the average wait.

```python exec
id: the-hockey-stick-1
random.seed(1)
waits = simulate_waits(20000, arrival_prob=0.45, service_capacity=1)
print(round(sum(waits) / len(waits), 1))
```

```predict
type: number
tolerance: 0.5

What will the average wait be, in steps, to one decimal place?
```

About 2.3 steps. One and a half times as busy, and more than five times
the wait. What happens between those two? The next cell tries ten levels
of utilisation, from half busy to 98% busy, and plots the average wait
at each.

```python exec
id: the-hockey-stick-2
import matplotlib.pyplot as plt

busy_levels = [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.93, 0.95, 0.97, 0.98]
average_waits = []
for busy in busy_levels:
    random.seed(1)
    waits = simulate_waits(20000, arrival_prob=busy / 2, service_capacity=1)
    average_waits.append(sum(waits) / len(waits))
    print(f"{busy:.2f} busy: average wait {average_waits[-1]:.2f} steps")

plt.plot(busy_levels, average_waits, marker="o")
plt.xlabel("utilisation")
plt.ylabel("average wait (steps)")
```

From half busy to 80% busy, the average wait grows from about a quarter
of a step to about one step. From 90% to 98%, it grows from about 2 to
about 11. The curve lies nearly flat, then turns up sharply, like the
blade of a hockey stick. People who plan queues call it exactly that:
the *hockey stick*.

Why does it turn up so sharply? Think about the time the server is idle.
At half busy, it is idle one step in two, and a burst of arrivals is
soon cleared. At 98% busy, it is idle one step in fifty. A burst still
comes now and then, but there is almost no spare time to clear it in, so
it stays in the queue. Every time the idle share halves, the wait
roughly doubles: 10% idle gives about 2.3 steps, 5% gives about 4.6,
and 2% gives about 11.

For this model, a longer calculation than this page has room for gives
the average wait exactly: $\dfrac{u}{4(1 - u)}$ steps, where $u$ is the
utilisation. The $1 - u$ underneath is the idle share. As it shrinks
towards 0, the wait grows without limit. The simulated waits sit close
to the formula, and furthest from it at 97% and 98%. There, a run needs
to be very long before its average settles.

That is why a supermarket opens another till before every till is busy,
and why a web server that is 95% busy is thought of as nearly full.

## Past full: a queue that never clears

What happens at 100% busy, or more? At `arrival_prob=0.6`, on average
1.2 items arrive each step, and the server can clear 1.

```python exec
id: past-full-a-queue-that-never-clears-1
random.seed(1)
waits = simulate_waits(2000, arrival_prob=0.6, service_capacity=1)

plt.figure()
plt.plot(waits, linewidth=0.8)
plt.xlabel("item, in the order served")
plt.ylabel("wait (steps)")
print("wait of item 100: ", waits[99])
print("wait of item 1000:", waits[999])
print("wait of the last: ", waits[-1])
```

The 100th item waits 24 steps, the 1,000th waits 159, and the last
waits 331. Each item waits longer, on average, than the one before, and
the queue behind it keeps growing. A queue like this is called
*unstable*. It has no typical wait, because the longer it runs, the
longer the wait gets.

So there is one line that decides whether a queue ever clears:

- If the utilisation is *below* 1, the queue keeps coming back to empty,
  and its average wait settles. It is *stable*.
- If the utilisation is *1 or more*, the queue is unstable.

The hockey stick adds what that rule leaves out. A stable queue can
still have a very long wait, if it runs close to the line.

## Is this a good model of a real queue?

A model is a choice about what to keep and what to leave out. Our model
keeps one thing, the balance between arrivals and capacity, and it
leaves out a great deal. Here is one thing it leaves out: in our model,
arrivals come at most two in a step, and each one on its own. At a real
spaceport, a family of four arrives at the desk together.

The next cell changes only that. People now arrive in groups, and the
chance of a group is set so that the server is still 90% busy.

```python exec
id: is-this-a-good-model-of-a-real-queue-1
def simulate_group_waits(steps, group_prob, group_size, service_capacity):
    """Like simulate_waits, but people arrive in groups of group_size."""
    queue = []
    waits = []
    for step in range(steps):
        if random.random() < group_prob:
            for _ in range(group_size):
                queue.append(step)
        for _ in range(min(len(queue), service_capacity)):
            waits.append(step - queue.pop(0))
    return waits


for group_size in [2, 4, 8]:
    random.seed(1)
    waits = simulate_group_waits(20000, 0.9 / group_size, group_size, service_capacity=1)
    print(f"groups of {group_size}: average wait {sum(waits) / len(waits):.2f} steps")
```

Every one of these servers is 90% busy, like the one that gave 2.3
steps. With groups of 4, the average wait is about 17 steps; with groups
of 8, about 43. The average number of arrivals is the same. How they
come is different. So a model that gets the average right can still be
far out on the wait.

Here are some more things the model leaves out:

- Every item takes exactly one step to serve. A real barista is quicker
  with some orders than others.
- Nobody gives up. At a real clinic, some people see a long queue and go
  home.
- Arrivals do not depend on the time of day. A real café has a lunch
  rush.
- The server never stops. A real one takes breaks.

Choose two. Would each one make the real wait longer than the model
says, or shorter? A model is only as useful as the question it is used
for. This one is useful for "how does the wait change as the server gets
busier?" It is not useful for "exactly how long will I wait at the
spaceport on Monday?"

## Your world

Can you write `mean_wait(arrival_prob, service_capacity, seed)`? It
sets the seed, runs `simulate_waits` for 20,000 steps, and returns the
average wait.

<div class="dl-world" data-world="living-systems">

On a coral reef, fish queue at a cleaning station, where a small cleaner
wrasse eats the parasites off them. The wrasse cleans one fish a step,
and at the moment the fish arrive with `arrival_prob=0.4`. If more fish
come to the reef and `arrival_prob` rises to `0.48`, how much longer do
they wait?

```python exec
id: your-world-1--living-systems
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    # Your code here.
```

```hint
Call `random.seed(seed)` first, so the run can be repeated. Then
`simulate_waits(20000, arrival_prob, service_capacity)`, and the average
of the list it returns.
```

```inputs
round(mean_wait(0.4, 1), 2)
round(mean_wait(0.48, 1), 2)
round(mean_wait(0.48, 1, seed=2), 2)
```

```solution
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    random.seed(seed)
    waits = simulate_waits(20000, arrival_prob, service_capacity)
    return sum(waits) / len(waits)
---
At `arrival_prob=0.4` the wrasse is 80% busy, and a fish waits about 1
step. At `0.48` it is 96% busy, and a fish waits about 5.6 steps. The
fish arrive only a fifth more often, and they wait more than five times
as long. A second seed gives a slightly different number, because a
queue this close to full takes a long time to settle.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

At a spaceport, one check-in desk checks in one passenger a step. On the
morning rush, passengers arrive with `arrival_prob=0.47`. How long do
they wait? What if a second desk opens?

```python exec
id: your-world-1--queues-and-crowds
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    # Your code here.
```

```hint
Call `random.seed(seed)` first, so the run can be repeated. Then
`simulate_waits(20000, arrival_prob, service_capacity)`, and the average
of the list it returns.
```

```inputs
round(mean_wait(0.47, 1), 2)
round(mean_wait(0.47, 2), 2)
round(mean_wait(0.3, 1), 2)
```

```solution
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    random.seed(seed)
    waits = simulate_waits(20000, arrival_prob, service_capacity)
    return sum(waits) / len(waits)
---
One desk is 94% busy, and a passenger waits about 3.8 steps. With two
desks, the wait is 0. No real spaceport is like that, and the model says
why: at most two passengers arrive in a step, and two desks clear two.
A real rush brings a coach full of passengers at once, as the groups
above showed. Off the rush, at `arrival_prob=0.3`, one desk is enough:
about 0.4 steps.
```

</div>

<div class="dl-world" data-world="spread">

During an outbreak, patients arrive at a clinic with `arrival_prob=0.45`,
and one doctor sees one patient a step. At the peak of the outbreak,
`arrival_prob` rises to `0.49`. How long do patients wait, before and at
the peak?

```python exec
id: your-world-1--spread
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    # Your code here.
```

```hint
Call `random.seed(seed)` first, so the run can be repeated. Then
`simulate_waits(20000, arrival_prob, service_capacity)`, and the average
of the list it returns.
```

```inputs
round(mean_wait(0.45, 1), 2)
round(mean_wait(0.49, 1), 2)
round(mean_wait(0.49, 2), 2)
```

```solution
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    random.seed(seed)
    waits = simulate_waits(20000, arrival_prob, service_capacity)
    return sum(waits) / len(waits)
---
Before the peak the doctor is 90% busy, and a patient waits about 2.3
steps. At the peak the doctor is 98% busy, and a patient waits about
11.3 steps. Patients arrive less than a tenth more often, and wait five
times as long. A second doctor brings the wait to 0 in this model,
though a real outbreak would bring patients in bursts.
```

</div>

<div class="dl-world" data-world="space-and-physics">

A camera watches the night sky for meteors, and a computer checks each
picture, one picture a step. On an ordinary night, pictures arrive with
`arrival_prob=0.3`. On the night of a meteor shower, `arrival_prob`
rises to `0.49`. How long does a picture wait to be checked?

```python exec
id: your-world-1--space-and-physics
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    # Your code here.
```

```hint
Call `random.seed(seed)` first, so the run can be repeated. Then
`simulate_waits(20000, arrival_prob, service_capacity)`, and the average
of the list it returns.
```

```inputs
round(mean_wait(0.3, 1), 2)
round(mean_wait(0.49, 1), 2)
round(mean_wait(0.49, 1, seed=2), 2)
```

```solution
def mean_wait(arrival_prob, service_capacity, seed=1):
    """The average wait over 20,000 steps, under a stated seed."""
    random.seed(seed)
    waits = simulate_waits(20000, arrival_prob, service_capacity)
    return sum(waits) / len(waits)
---
On an ordinary night the computer is 60% busy, and a picture waits
about 0.4 steps. On the night of the shower it is 98% busy, and a
picture waits about 11.3 steps. A second seed gives about 10.3: a queue
this close to full takes a long time to settle, so one run tells you
less.
```

</div>

## Lab bench

Every number this simulation uses is named at the top of the next cell.
Change them, run it, and see what happens.

```python exec
id: lab-bench-1
STEPS = 5000             # how long the run lasts
ARRIVAL_PROB = 0.45      # the chance of an arrival, at each of the two checks
SERVICE_CAPACITY = 1     # the most the server clears in one step
SEED = 1                 # change it for another run

random.seed(SEED)
waits = simulate_waits(STEPS, ARRIVAL_PROB, SERVICE_CAPACITY)
print(f"utilisation:  {2 * ARRIVAL_PROB / SERVICE_CAPACITY:.2f}")
print(f"served:       {len(waits)}")
print(f"average wait: {sum(waits) / len(waits):.2f} steps")
print(f"longest wait: {max(waits)} steps")

plt.figure()
plt.plot(waits, linewidth=0.6)
plt.xlabel("item, in the order served")
plt.ylabel("wait (steps)")
```

Choose one of these questions, or ask one of your own:

1. How far apart are the average waits from five different seeds, at
   the same settings? Does a longer run bring them closer together?
2. At what utilisation does the longest wait first pass 20 steps?
3. Set `SERVICE_CAPACITY = 2` and `ARRIVAL_PROB = 0.9`. The server is
   90% busy, but nobody waits. Why? What does that tell you about the
   model?
4. The utilisation is exactly 1 when `ARRIVAL_PROB = 0.5`. Is that
   queue stable? Run it for 1,000 steps, then 10,000, and compare.

## Where to read more

Kendall, D. G. (1953). *Stochastic Processes Occurring in the Theory of
Queues and their Analysis by the Method of the Imbedded Markov Chain.*
The Annals of Mathematical Statistics, 24(3), 338–354. This paper
started queueing theory as its own field of mathematics. It is much more
formal than this tutorial's simple step-by-step count, but it asks
the same questions.

Harchol-Balter, M. (2013). *Performance Modeling and Design of Computer
Systems: Queueing Theory in Action*. Cambridge University Press. This
textbook is about computing, not queueing theory for its own sake. Its
early chapters explain why a server near full capacity makes everyone
wait, for the print-queue and request-queue examples this tutorial
opened with.

engineerguy (2010). *Why the other line is likely to move faster.*
<https://www.youtube.com/watch?v=F5Ri_HhziI0>. Bill Hammack explains
queueing theory, which started with telephone calls in Copenhagen, and how
a shop can arrange its lines so that people wait less. The video is four
minutes long.
