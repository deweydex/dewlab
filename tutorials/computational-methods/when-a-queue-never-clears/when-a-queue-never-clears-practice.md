---
title: "When a Queue Never Clears — Practice"
slug: when-a-queue-never-clears-practice
practice_for: when-a-queue-never-clears
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.09.05.1
---

# When a Queue Never Clears — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

```python exec
id: setup-1
import random

def arrivals_this_step(arrival_prob):
    return sum(1 for _ in range(2) if random.random() < arrival_prob)

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

## Predicting Before Simulating

**1.** Without running anything: is a queue with `arrival_prob=0.4` and
`service_capacity=1` stable or unstable? Then check with a 300-step run.

```python exec
id: predicting-before-simulating-1
hint: Average arrivals per step is 2 * arrival_prob. Compare that to service_capacity.
```

<details class="dl-answer"><summary>answer</summary>

Stable. Average arrivals are `2 * 0.4 = 0.8`, below the service capacity
of `1`. A 300-step run backs this up: the queue wanders but stays small,
never climbing far past single digits.

</details>

**2.** A web server handles requests arriving at random, averaging 45 a
second, and can process 50 a second. During a traffic spike, the average
arrival rate rises to 55 a second, capacity unchanged. Which of these two
situations is stable, in this tutorial's sense of the word?

<details class="dl-answer"><summary>answer</summary>

Only the first. `45 < 50`: average arrivals stay below capacity, so the
queue of waiting requests stays bounded, even through a bad few seconds.
`55 > 50`: average arrivals rise above capacity, so the queue grows
without limit for as long as that spike lasts. Whatever buffer the
server has fills up eventually, and requests start getting dropped or
timing out. This is the real reason a service that was fine yesterday
fails during a spike today: the average arrival rate crossed the one
number that decides everything.

</details>

## Changing the Shape of Arrivals

**3.** Try rewriting `arrivals_this_step` to check *three* independent
chances each step instead of two. What is the new formula for average
arrivals per step, in terms of `arrival_prob`?

```python exec
id: changing-the-shape-of-arrivals-1
hint: Each independent chance contributes arrival_prob to the average on its own. Three chances means three chances to contribute.
```

<details class="dl-answer"><summary>answer</summary>

```python
def arrivals_this_step_v2(arrival_prob):
    return sum(1 for _ in range(3) if random.random() < arrival_prob)
```

Average arrivals per step is now `3 * arrival_prob`, not `2 *
arrival_prob`. The stability rule does not change in spirit: compare
average arrivals to service capacity. Only the formula for working out
what the average actually is has changed.

</details>

**4.** With three chances per step (`arrivals_this_step_v2`) and
`service_capacity=1`, is `arrival_prob=0.3` stable? Try it for 500 steps
and look at how large the queue gets, not just its final value.

```python exec
id: changing-the-shape-of-arrivals-2
hint: Average arrivals = 3 * 0.3. Compare that to 1 — and notice how close the two numbers are.
```

<details class="dl-answer"><summary>answer</summary>

Stable, but only just. Average arrivals are `3 * 0.3 = 0.9`, a hair
below the service capacity of `1`. The rule still calls it stable, and
over a long run it is: the queue never runs away for good. But a queue
this close to its own boundary swings much wider than the confidently
stable case in question 1. It reaches into the teens rather than
staying in single digits, before eventually draining back down.

</details>

## Reading the Rule

**5.** In your own words: why does one comparison, `arrival_prob *
(number of chances)` against `service_capacity`, get to speak for every
possible run, when two runs at the identical settings produce different
queue lengths at every step?

<details class="dl-answer"><summary>answer</summary>

The comparison is about the long-run *average*, not about any particular
sequence of arrivals. Two runs at the same settings really do differ
moment to moment, exactly as two dart-throwing runs in `counting-darts`
differed. What does not differ between them is which side of the
average-arrivals-versus-capacity line the settings sit on. That alone
decides whether the server catches up over a long enough run, or falls
permanently behind. The rule predicts the *shape* every run will
eventually take, not the specific path any one run takes to get there.

</details>
