---
title: "Mixed problems: simulation"
practice_across:
  - leaving-it-to-chance
  - counting-darts
  - a-model-that-corrects-itself
  - when-a-queue-never-clears
  - stepping-forward-in-time
  - a-simulation-of-your-own
year: "2026-2027"
version: 2026.09.27.1
worlds:
  living-systems: A reef survey, counting the fish that swim past.
  queues-and-crowds: A café, and the customers who come in during an hour.
  spread: A rumour, passed on from person to person.
  space-and-physics: A speck of dust, knocked about at random.
---

# Mixed problems: simulation

These problems move between the pages of the series on purpose, and do
not say which page each one comes from. Choosing the tool is part of
the problem.

```python exec
id: mixed-simulation-tools
import math
import random
```

## 1.

In a queue, up to two items arrive each step, each with a chance of
0.4, and the server clears one item a step. What is the server's
utilisation? What is it if the server can clear two a step?

<details class="dl-hint"><summary>hint</summary>

On average, how many items arrive in a step? Divide that by how many
the server can clear.

</details>

<details class="dl-answer"><summary>one way through it</summary>

On average $2 \times 0.4 = 0.8$ items arrive each step. With a capacity
of 1, the utilisation is $0.8 \div 1 = 0.8$: busy 80% of the time. With
a capacity of 2, it is $0.8 \div 2 = 0.4$. At 80%, the queue is still
on the flat part of the hockey stick, but the steep part starts not
far past 90%.

</details>

## 2.

Two lists of dice rolls, from the same seed. The second has one extra
random number drawn before its rolls.

```python exec
id: mixed-simulation-one-extra
random.seed(4)
first = [random.randint(1, 6) for _ in range(5)]
random.seed(4)
random.random()
second = [random.randint(1, 6) for _ in range(5)]
print(first)
print(second)
print(first == second)
```

```predict
type: choice

Will the two lists be the same? What will the last line print?

- True
  - Both start from seed 4, so they seem bound to match.
- False
```

The seed fixes the whole sequence of random numbers, in order. The
extra `random.random()` uses up the first number of that sequence, so
every roll after it comes from one place further along. This is why a
function that draws random numbers should set its own seed, as
`estimate_pi()` does: then nothing that ran before it can change its
answer.

## 3.

Can you write `estimate_triangle(n, seed)`? It throws `n` darts at the
unit square and returns the share that land where $x + y < 1$. For each
dart, draw $x$ first and then $y$, each with `random.random()`. What
should the answer be close to?

```python exec
id: mixed-simulation-triangle
def estimate_triangle(n, seed):
    """The share of n random points in the unit square with x + y < 1."""
    # Your code here.
```

```hint
Set the seed first, inside the function. Then count the darts that
land inside, and divide by `n`.
```

```inputs
estimate_triangle(100, seed=0)
estimate_triangle(10000, seed=0)
```

```solution
def estimate_triangle(n, seed):
    """The share of n random points in the unit square with x + y < 1."""
    random.seed(seed)
    inside = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x + y < 1:
            inside += 1
    return inside / n
---
The line x + y = 1 cuts the square corner to corner, so the true answer is exactly 0.5. 100 darts give 0.43 and 10,000 give 0.5008: closer, but not exact, and that is not a bug.
```

## 4.

You and a classmate each throw 100 darts to estimate π. You get 3.20,
and your classmate gets 3.04. One of you must have a bug. True or
false? What would you do to get closer to π?

<details class="dl-answer"><summary>answer</summary>

False. Both are estimates from 100 darts, and 100 darts cannot pin π
down more closely than that: runs with different seeds spread out by
about 0.16 either side of π. Neither answer is a mistake. More darts
narrow the spread. Four times as many darts halve it, so 400 darts
spread by about 0.08, and 10,000 by about 0.016.

</details>

## 5.

A ball is dropped from rest, from a height in metres, with gravity
$-9.8$. Can you write `fall_time(height, step)`? It steps forward in
time as on the Liberty Hall page: move the height with the velocity the
ball has now, then change the velocity, then add `step` to the time.
It stops when the height is 0 or less, and returns the time.

```python exec
id: mixed-simulation-fall
def fall_time(height, step):
    """Seconds until the ball reaches the ground, stepped forward by `step`."""
    # Your code here.
```

```hint
Start with `velocity = 0` and `time = 0`, and loop `while height > 0:`.
Inside the loop, the order of the three lines matters.
```

```inputs
round(fall_time(60, 1), 3)
round(fall_time(60, 0.1), 3)
round(fall_time(60, 0.01), 3)
round(math.sqrt(60 / 4.9), 3)
```

```solution
def fall_time(height, step):
    """Seconds until the ball reaches the ground, stepped forward by `step`."""
    velocity = 0
    time = 0
    while height > 0:
        height = height + velocity * step
        velocity = velocity + -9.8 * step
        time = time + step
    return time
---
The formula gives 3.499 seconds. A step of 1 second gives 5, a step of 0.1 gives 3.6, and a step of 0.01 gives 3.51. Each step pretends the velocity stays the same for the whole step, and a smaller step pretends for less time.
```

## 6.

Past full, a queue never clears. Here up to two items arrive each step,
each with a chance of 0.6, and the server clears one a step. The cell
prints how many are waiting after 1,000 steps.

```python exec
id: mixed-simulation-past-full
random.seed(2)
waiting = 0
for step in range(1000):
    waiting += sum(1 for _ in range(2) if random.random() < 0.6)
    waiting -= min(waiting, 1)
print(waiting)
```

```predict
type: number
tolerance: 60

About how many items will be waiting after 1,000 steps?
```

On average 1.2 items arrive each step and 1 leaves, so the queue grows
by about 0.2 a step: about 200 after 1,000 steps. A utilisation of 1.2
does not mean a long wait. It means the wait grows without end.

## 7.

This perceptron should learn to tell a plus from a cross. It never
improves: in every epoch, it gets exactly one of the two right. Which
line is wrong? Print `weights` at the end, to see where they are
heading.

```python exec
id: mixed-simulation-wrong-way
PLUS = [0, 1, 0, 1, 1, 1, 0, 1, 0]
CROSS = [1, 0, 1, 0, 1, 0, 1, 0, 1]
examples = [(PLUS, 1), (CROSS, 0)]


def predict(weights, bias, pixels):
    total = sum(w * p for w, p in zip(weights, pixels)) + bias
    return 1 if total > 0 else 0


weights = [0.0] * 9
bias = 0.0
for epoch in range(6):
    correct = 0
    for pixels, label in examples:
        guess = predict(weights, bias, pixels)
        error = guess - label
        if error != 0:
            for i in range(9):
                weights[i] += 0.5 * error * pixels[i]
            bias += 0.5 * error
        else:
            correct += 1
    print(epoch + 1, correct, "of 2 right")
```

<details class="dl-answer"><summary>answer</summary>

`error = guess - label` has the sign the wrong way round. It should be
`label - guess`. For a missed plus, the label is 1 and the guess is 0,
so the error must be +1, to push the lit pixels' weights up. With the
sign turned round, every correction pushes the weights further the
wrong way: after six epochs, every weight on a pixel of the plus is
−3. The model calls everything a cross, and it gets the cross right
only by accident. Change that one line, and it gets both right from
the second epoch on.

</details>

## In your world

A simulation run once gives one answer. Many runs, with many seeds,
show how far the answer can move by chance alone. Can you write
`summary(one_run, seeds)`? It calls `one_run(seed)` for every seed,
and returns a tuple: the average of the results, rounded to 2 places,
the lowest, and the highest.

<div class="dl-world" data-world="living-systems">

A diver counts the fish that swim past in 20 sightings. Each sighting
is a parrotfish with a chance of 0.3.

```python exec
id: in-your-world-1--living-systems
def one_run(seed):
    """How many of 20 sightings are parrotfish."""
    random.seed(seed)
    return sum(1 for _ in range(20) if random.random() < 0.3)


def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    # Your code here.
```

```hint
Make a list of `one_run(seed)` for every seed. Then use `sum()`,
`len()`, `min()` and `max()` on that list.
```

```inputs
summary(one_run, range(100))
summary(one_run, range(10))
```

```solution
def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    results = [one_run(seed) for seed in seeds]
    return (round(sum(results) / len(results), 2), min(results), max(results))
---
Over 100 surveys, the diver sees 6.03 parrotfish on average, close to 20 × 0.3 = 6. But one survey sees as few as 2 and another as many as 11. A single survey could easily mislead you about how common parrotfish are.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

A café door, over 60 minutes. In each minute, a customer comes in with
a chance of 0.2.

```python exec
id: in-your-world-1--queues-and-crowds
def one_run(seed):
    """How many customers come in during an hour."""
    random.seed(seed)
    return sum(1 for _ in range(60) if random.random() < 0.2)


def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    # Your code here.
```

```hint
Make a list of `one_run(seed)` for every seed. Then use `sum()`,
`len()`, `min()` and `max()` on that list.
```

```inputs
summary(one_run, range(100))
summary(one_run, range(10))
```

```solution
def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    results = [one_run(seed) for seed in seeds]
    return (round(sum(results) / len(results), 2), min(results), max(results))
---
Over 100 hours, 12.38 customers on average, close to 60 × 0.2 = 12. But the quietest hour has 6 and the busiest 20. A café that plans for the average hour will be short-staffed in its busy ones.
```

</div>

<div class="dl-world" data-world="spread">

A rumour starts with one person. Each day, each person who knows it
tells one new person, with a chance of 0.5. How many know it after 6
days?

```python exec
id: in-your-world-1--spread
def one_run(seed):
    """How many people know the rumour after 6 days."""
    random.seed(seed)
    knowing = 1
    for day in range(6):
        knowing += sum(1 for _ in range(knowing) if random.random() < 0.5)
    return knowing


def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    # Your code here.
```

```hint
Make a list of `one_run(seed)` for every seed. Then use `sum()`,
`len()`, `min()` and `max()` on that list.
```

```inputs
summary(one_run, range(100))
summary(one_run, range(10))
```

```solution
def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    results = [one_run(seed) for seed in seeds]
    return (round(sum(results) / len(results), 2), min(results), max(results))
---
Over 100 runs, 12.0 people on average, close to 1.5 multiplied by itself six times, about 11.4. But the spread is huge: in one run nobody else ever hears it, and in another 31 people do. A rumour's first few days decide most of what happens later, and those few days are the most random part.
```

</div>

<div class="dl-world" data-world="space-and-physics">

A speck of dust takes 100 steps, each one unit up, down, left or right,
chosen at random. How far from its start does it end?

```python exec
id: in-your-world-1--space-and-physics
def one_run(seed):
    """The distance from the start after 100 random steps."""
    random.seed(seed)
    x, y = 0, 0
    for _ in range(100):
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        x, y = x + dx, y + dy
    return round(math.sqrt(x * x + y * y), 2)


def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    # Your code here.
```

```hint
Make a list of `one_run(seed)` for every seed. Then use `sum()`,
`len()`, `min()` and `max()` on that list.
```

```inputs
summary(one_run, range(100))
summary(one_run, range(10))
```

```solution
def summary(one_run, seeds):
    """(average rounded to 2 places, lowest, highest) over one run per seed."""
    results = [one_run(seed) for seed in seeds]
    return (round(sum(results) / len(results), 2), min(results), max(results))
---
Over 100 specks, 9.66 units on average, near the square root of the 100 steps, 10. But one speck ends back where it started, 0 units away, and another 23.19 units away.
```

</div>
