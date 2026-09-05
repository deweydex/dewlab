---
title: "When a Queue Never Clears"
slug: when-a-queue-never-clears
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.09.05.1
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

# When a Queue Never Clears

A print queue, a web server's list of waiting requests, a line of
customers at a till: every one of them is the same shape. Things arrive
at unpredictable moments, something processes them at a fixed rate, and
a queue builds up in between. This tutorial asks the question that shape
always raises: does the queue stay under control, or does it grow
forever?

## Arrivals You Cannot Predict, One at a Time

An arrival is a coin flip repeated. Each time step, check twice whether
something new has shown up, and count how many times the answer was yes.

```python exec
id: arrivals-you-cannot-predict-one-at-a-time-1
import random

random.seed(1)

def arrivals_this_step(arrival_prob):
    """0, 1, or 2 new arrivals, checked as two independent chances."""
    return sum(1 for _ in range(2) if random.random() < arrival_prob)

print([arrivals_this_step(0.3) for _ in range(10)])
```

`arrival_prob` sets how likely each of the two chances is to land. Over
many steps, the average number of arrivals per step works out to `2 *
arrival_prob` — a number worth keeping in mind, since it decides
everything that follows.

A queue needs one more thing: something processing what has arrived.

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

`service_capacity` is how many waiting items get cleared each step,
however many are waiting. Each step: new arrivals join the back of the
queue, then the server clears as many as it can, up to its capacity.

### Your turn

If `arrival_prob` is `0.5` and `service_capacity` is `2`, what is the
average number of arrivals per step, and how does it compare to what the
server can clear?

```python exec
id: arrivals-you-cannot-predict-one-at-a-time-3
hint: Average arrivals per step is 2 * arrival_prob, from the paragraph above.
```

## A Queue That Clears

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

Average arrivals here are `2 * 0.3 = 0.6` per step, against a service
capacity of `1`. The server can clear more than what shows up, on
average, so the queue never grows for long. It rises after a run of bad
luck, then drains again once arrivals fall back below what the server
can handle. A queue with this property is *stable*: however bad its
luck, it never grows forever.

## A Queue That Never Clears

Change one number.

```python exec
id: a-queue-that-never-clears-1
random.seed(1)
unstable = simulate_queue(200, arrival_prob=0.6, service_capacity=1)

plt.plot(unstable)
plt.xlabel("step")
plt.ylabel("queue length")
print("queue length at the end:", unstable[-1])
```

Average arrivals are now `2 * 0.6 = 1.2` per step, against the same
service capacity of `1`. The server is behind by `0.2` items every step,
on average — never by much, on any one step, but never caught up either.
The queue does not wander back down the way the first one did. It
climbs. That is what makes a queue *unstable*: not that it grows fast,
but that nothing about it ever turns around.

### Your turn

Run `simulate_queue` for 2,000 steps instead of 200, with the same
`arrival_prob=0.6` and `service_capacity=1`. Does the queue length look
like it is settling toward some value, or still climbing?

```python exec
id: a-queue-that-never-clears-2
hint: Print the queue length at a few points along the way -- step 200, step 1000, step 2000 -- rather than only the very last value.
```

## Predicting It Before Running It

Both simulations above could have been called before either one ran.
Compare `2 * arrival_prob` to `service_capacity`. Below it, the queue
stays bounded. At or above it, the queue grows without limit, whatever
the actual numbers happen to look like on any one run.

```python exec
id: predicting-it-before-running-it-1
def predict_stable(arrival_prob, service_capacity):
    average_arrivals = 2 * arrival_prob
    return average_arrivals < service_capacity

for arrival_prob in [0.2, 0.3, 0.45, 0.5, 0.6, 0.8]:
    stable = predict_stable(arrival_prob, service_capacity=1)
    print(f"arrival_prob={arrival_prob}: predicted {'stable' if stable else 'unstable'}")
```

This is the real value of the two simulations above, not the plots on
their own. A plot tells you what happened on one run, seeded one
particular way. The comparison here tells you what will happen on every
run, before spending any computer time finding out. It is the same kind
of prediction an engineer makes before adding a fourth checkout to a
shop, or before deciding whether a server needs a second worker process.

Simulation still matters here, alongside that prediction, not instead of
it. The rule says *whether* a queue is stable. It says nothing about how
large the queue gets before it drains on a run that is stable but
unlucky. It also says nothing about how long an unstable queue takes to
become a real problem. Those numbers only come from running it.

### Your turn

The demo above already called `arrival_prob=0.5` "unstable" — average
arrivals of exactly `1` never fall strictly below a service capacity of
`1`, so the rule's `<` never fires. Run `simulate_queue` at this setting
for 1,000 steps and watch the queue length over the whole run, not just
the final value. Does it behave like the clearly stable run, the clearly
unstable one, or something in between?

```python exec
id: predicting-it-before-running-it-2
hint: Try two different seeds and compare. The clearly stable run stayed small and settled; the clearly unstable one climbed steadily. Look for which of those two shapes this one is closer to.
```

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
