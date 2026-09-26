---
title: "Simulating a queue: stable and unstable queues"
year: "2026-2027"
version: 2026.09.22.1
covers:
  arrivals-you-cannot-predict-one-at-a-time:
    covers: [CMPS-LO6]
  a-queue-that-clears:
    covers: [CMPS-LO6]
  a-queue-that-never-clears:
    covers: [CMPS-LO6]
  predicting-it-before-running-it:
    covers: [CMPS-LO6]
---

# Simulating a queue: stable and unstable queues

Think of a print queue, a web server's list of waiting requests, or a
line of customers at a checkout. They all work the same way:

1. Things arrive at moments nobody can predict.
2. Something deals with them at a fixed rate.
3. A queue builds up in between.

This raises one question every time. Does the queue stay under control,
or does it grow forever? On this page we simulate a queue to find out.

## Arrivals You Cannot Predict, One at a Time

We split time into steps. In each step, we check twice whether something
new has arrived, like flipping a coin twice. Then we count how many times
the answer was yes. So each step brings 0, 1 or 2 new arrivals.

The function below does this with a short form we have not used much
yet. `sum(1 for _ in range(2) if random.random() < arrival_prob)` works
like a list comprehension from
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids). It
makes a 1 for each of the two checks that comes up yes, and `sum` adds
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

`arrival_prob` is the chance that each of the two checks comes up yes.
Over many steps, the average number of arrivals per step works out to
`2 * arrival_prob`. Keep that number in mind. It decides everything that
follows.

A queue needs one more thing: something that deals with what has
arrived. We call that the *server*.

```python exec
id: arrivals-you-cannot-predict-one-at-a-time-2
def simulate_queue(steps, arrival_prob, service_capacity):
    queue = 0
    history = []
    for _ in range(steps):
        queue += arrivals_this_step(arrival_prob)
        served = min(queue, service_capacity)
        queue -= served
        history.append(queue)
    return history
```

`service_capacity` is the most items the server can clear in one step,
however many are waiting. `min(queue, service_capacity)` picks the
smaller of the two numbers, so the server never clears more items than
are waiting.

Each step has two parts:

1. The new arrivals join the back of the queue.
2. The server clears as many as it can, up to its capacity.

### Your turn

Suppose `arrival_prob` is `0.5` and `service_capacity` is `2`.

1. What is the average number of arrivals per step?
2. How does it compare with what the server can clear?

```python exec
id: arrivals-you-cannot-predict-one-at-a-time-3
hint: Average arrivals per step is 2 * arrival_prob, from the paragraph above.
```

## A Queue That Clears

Here, `arrival_prob` is `0.3` and `service_capacity` is `1`. Before you
run the cell, work out the average number of arrivals per step. Is it
more or less than the server can clear?

```python exec
id: a-queue-that-clears-1
import matplotlib.pyplot as plt

random.seed(1)
stable = simulate_queue(200, arrival_prob=0.3, service_capacity=1)

plt.plot(stable)
plt.xlabel("step")
plt.ylabel("queue length")
print("longest the queue ever got:", max(stable))
print("queue length at the end:  ", stable[-1])
```

Average arrivals here are `2 * 0.3 = 0.6` per step. The server can clear
`1`. So on average, the server can clear more than arrives, and the queue
never grows for long. It rises after a run of bad luck. Then it drains
again, once arrivals fall back below what the server can handle.

A queue like this is called *stable*. A stable queue keeps coming back
to empty, and it has a typical length that it hovers around. A long run
of bad luck can still push it high, and nothing promises it will stay
below any particular length. But it always comes back down, and over a
long run its average length settles.

## A Queue That Never Clears

Now we change one number: `arrival_prob` goes from `0.3` to `0.6`. What
do you think the plot will look like?

```python exec
id: a-queue-that-never-clears-1
random.seed(1)
unstable = simulate_queue(200, arrival_prob=0.6, service_capacity=1)

plt.plot(unstable)
plt.xlabel("step")
plt.ylabel("queue length")
print("queue length at the end:", unstable[-1])
```

Average arrivals are now `2 * 0.6 = 1.2` per step. The server can still
clear only `1`. So on average, the server falls behind by `0.2` items
every step. That is never much on any one step, but the server never
catches up either.

This queue does not drain back down the way the first one did. It goes
down a little now and then, but over the whole run it climbs.

A queue like this is called *unstable*. An unstable queue has no
typical length. It does not have to grow fast. But the longer you run
it, the longer its average length gets. It never settles.

### Your turn

1. Run `simulate_queue` for 2,000 steps instead of 200, with the same
   `arrival_prob=0.6` and `service_capacity=1`.
2. Is the queue length settling towards some value, or still climbing?

```python exec
id: a-queue-that-never-clears-2
hint: Print the queue length at a few points along the way, such as step 200, step 1000 and step 2000. The last value alone does not show the shape.
```

## Predicting It Before Running It

We could have predicted both results before running either simulation.
Compare `2 * arrival_prob` with `service_capacity`:

- If average arrivals are *below* the capacity, the queue is stable. It
  keeps coming back to empty, and its average length settles.
- If average arrivals are *at or above* the capacity, the queue is
  unstable. On any one run, the numbers may look different, but over a
  long run its average length keeps growing.

Before you run the next cell, which of these settings do you expect to be
stable?

```python exec
id: predicting-it-before-running-it-1
def predict_stable(arrival_prob, service_capacity):
    average_arrivals = 2 * arrival_prob
    return average_arrivals < service_capacity

for arrival_prob in [0.2, 0.3, 0.45, 0.5, 0.6, 0.8]:
    stable = predict_stable(arrival_prob, service_capacity=1)
    print(f"arrival_prob={arrival_prob}: predicted {'stable' if stable else 'unstable'}")
```

This rule is the real result of the two simulations above. The plots
only tell us what happened on one run, with one seed. The rule tells us
how the queue behaves in the long run, whatever the seed, before we
spend any computer time finding out. It does not tell us what any one
run will look like. An engineer makes the same kind of prediction before adding a
fourth checkout to a shop, or before deciding whether a web server needs
a second worker.

We still need simulation, alongside the rule. The rule says *whether* a
queue is stable. It says nothing about some other questions:

- How long does a stable queue get on an unlucky run, before it drains?
- How long does an unstable queue take to become a real problem?

Only running the simulation answers those.

### Your turn

Look at `arrival_prob=0.5` in the cell above. The rule called it
"unstable". Average arrivals are exactly `1`, which is not *below* a
capacity of `1`. So the rule's `<` gives `False`.

1. Run `simulate_queue` at this setting for 1,000 steps.
2. Watch the queue length over the whole run, not only the final value.
3. Does it behave like the stable run, the unstable run, or something in
   between?

```python exec
id: predicting-it-before-running-it-2
hint: Try two different seeds and compare them. The stable run stayed small and settled. The unstable run climbed steadily. Which of those two shapes is this one closer to?
```

Most runs look like something in between. The queue does not climb
steadily, like the unstable run. It often drains back to empty. But it
has no level that it settles around either. Some runs wander well above
ten before they come back down, and a longer run can wander further
still. Its average length keeps growing the longer it runs. It has no
typical length, and that is why the rule counts this setting as
unstable.

## Where to Read More

Kendall, D. G. (1953). *Stochastic Processes Occurring in the Theory of
Queues and their Analysis by the Method of the Imbedded Markov Chain.*
The Annals of Mathematical Statistics, 24(3), 338–354. The paper that
started queueing theory as its own field of mathematics, considerably
more formal than this tutorial's simple step-by-step count, but asking
exactly the same stability question.

Harchol-Balter, M. (2013). *Performance Modeling and Design of Computer
Systems: Queueing Theory in Action*. Cambridge University Press. A
textbook aimed squarely at computing rather than at queueing theory for
its own sake — written for exactly the print-queue, request-queue,
packet-queue examples this tutorial opened with.

engineerguy (2010). *Why the other line is likely to move faster.*
<https://www.youtube.com/watch?v=F5Ri_HhziI0>. Bill Hammack explains
queueing theory, which started with telephone calls in Copenhagen, and how
a shop can arrange its lines so that people wait less. Four minutes.
