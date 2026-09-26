---
title: "Simulating a queue: stable and unstable queues — Practice"
practice_for: when-a-queue-never-clears
year: "2026-2027"
version: 2026.09.22.1
---

# Simulating a queue: stable and unstable queues — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what the code will do before you run it. Try to answer
before you check. A wrong guess teaches you more than a lucky right one,
once you see why it was wrong.

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

## Predicting before simulating

**1.** A queue has `arrival_prob=0.4` and `service_capacity=1`.

1. Without running anything, is it stable or unstable?
2. Check with a 300-step run.

```python exec
id: predicting-before-simulating-1
hint: Average arrivals per step is 2 * arrival_prob. Compare that to service_capacity.
```

<details class="dl-answer"><summary>answer</summary>

It is stable. Average arrivals are `2 * 0.4 = 0.8`, which is below the
service capacity of `1`. A 300-step run agrees. The queue wanders, but it
stays small. On most runs it never gets longer than about five, and it
rarely reaches ten.

</details>

**2.** Requests arrive at a web server at random, 45 a second on average.
The server can deal with 50 a second. During a sudden busy period, the
average rises to 55 a second, and the server's capacity stays the same.
Which of these two situations is stable, in the tutorial's meaning of the
word?

<details class="dl-answer"><summary>answer</summary>

Only the first one is stable.

- `45 < 50`. Average arrivals stay below capacity, so the queue of waiting
  requests stays under control, even through a bad few seconds.
- `55 > 50`. Average arrivals are above capacity, so the queue keeps
  growing for as long as the busy period lasts.

The server has limited room to hold waiting requests. In the end, that
room is full. Then requests start to be dropped, or to take so
long that they fail. This is why a service that was fine yesterday can
fail during a busy period today. The average arrival rate crossed the
one number that decides everything.

</details>

## Changing the shape of arrivals

**3.** Rewrite `arrivals_this_step` so that it checks *three* separate
chances each step, instead of two. What is the new formula for average
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

Average arrivals per step are now `3 * arrival_prob`. The stability rule
stays the same: compare average arrivals with the service capacity. Only
the formula for the average has changed.

</details>

**4.** Use three chances per step (`arrivals_this_step_v2`) and
`service_capacity=1`. Is `arrival_prob=0.3` stable? Try it for 500 steps.
Look at how long the queue gets during the run, not only its final
value.

```python exec
id: changing-the-shape-of-arrivals-2
hint: Average arrivals = 3 * 0.3. Compare that with 1. How close are the two numbers?
```

<details class="dl-answer"><summary>answer</summary>

It is stable, but only barely. Average arrivals are `3 * 0.3 = 0.9`, a
little below the service capacity of `1`. The rule still calls it stable,
and over a long run it is stable. The queue does not grow forever.

But a queue this close to the boundary swings much wider than the queue
in question 1, which was safely stable. It often gets to ten or more, and
sometimes to 13 or more, before it gets shorter again.

</details>

## Reading the rule

**5.** Two runs with exactly the same settings give different queue
lengths at every step. So how can one comparison, `arrival_prob *
(number of chances)` against `service_capacity`, speak for every possible
run? Answer in your own words.

<details class="dl-answer"><summary>answer</summary>

The comparison is about the long-run *average*. It is not about any one
set of arrivals. Two runs with the same settings do differ from moment to
moment, in the same way as two dart-throwing runs in
[Monte Carlo simulation: estimating π with random darts](tutorial:counting-darts).

But the settings are always on the same side of the line. Average
arrivals are either below capacity, or not. That alone decides whether
the server clears the queue over a long enough run, or the queue grows
forever. The rule predicts the *shape* that every run will take in the end. It does not
predict the exact path any one run takes to get there.

</details>
