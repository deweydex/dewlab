---
title: "Experiments with coin flips: chance in a list"
year: "2026-2027"
version: 2026.11.23.2
---

# Experiments with coin flips: chance in a list

Python can make random choices with the `random` module. A module is a file of ready-made functions, and `import` brings one in. On this page you flip coins and roll dice inside functions, keep the results in lists, and count what happened. The patterns come from the counts.

## 1. Random choices

**1.1** Run this cell three times. What changes, and what stays the same?

```python exec
id: random-choices-1
import random

print(random.randint(1, 6))
print(random.choice(["H", "T"]))
```

**1.2** Try `random.randint(1, 1)` and `random.randint(6, 1)`. One of them is not random at all. The other one fails. Read its error.

```python exec
id: random-choices-2
import random

print(random.randint(1, 1))
# your code here
```

**1.3** Put `random.seed(42)` on the line after the import and run the cell twice. What do you notice? Change 42 to another number.

```python exec
id: random-choices-3
import random

print(random.randint(1, 6), random.randint(1, 6), random.randint(1, 6))
```

## 2. One flip, then many

**2.1** Write `flip()`, which takes no arguments and returns `"H"` or `"T"`. Call it ten times in a loop.

```python exec
id: one-flip-then-many-1
import random

def flip():
    # your code here
    return "?"

for i in range(10):
    print(flip())
```

```solution
import random

def flip():
    return random.choice(["H", "T"])

for i in range(10):
    print(flip())
```

**2.2** Change the loop so the ten results print on one line. `print` has an `end` argument that can help.

**2.3** Write `flips(n)`, which returns a list of `n` coin flips.

```python exec
id: one-flip-then-many-2
import random

def flip():
    return random.choice(["H", "T"])

def flips(n):
    results = []
    # your loop here
    return results

print(flips(20))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Write a loop that runs `n` times.
2. Inside it, call `flip()` and add the result to `results` with `.append()`.
3. Return the list after the loop, not inside it. What happens if the `return` is indented into the loop?

</details>

```solution
import random

def flip():
    return random.choice(["H", "T"])

def flips(n):
    results = []
    for i in range(n):
        results.append(flip())
    return results

print(flips(20))
```

## 3. Counting what happened

**3.1** Write `count_heads(results)`, which counts the heads in a list with a loop and an `if`.

```python exec
id: counting-what-happened-1
def count_heads(results):
    heads = 0
    # your loop here
    return heads

print(count_heads(["H", "T", "H", "H", "T"]))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Loop over the list so that each result has a name, such as `result`.
2. Inside the loop, check whether `result` is `"H"`.
3. When it is, add 1 to `heads`.

</details>

```solution
def count_heads(results):
    heads = 0
    for result in results:
        if result == "H":
            heads = heads + 1
    return heads

print(count_heads(["H", "T", "H", "H", "T"]))
```

```inputs
count_heads(["H", "T", "H", "H", "T"])
count_heads(["T", "T"])     # no heads at all
count_heads([])             # no flips at all
```

**3.2** A list can count for you: `results.count("H")`. Check that it agrees with your function on a list of 50 flips.

```python exec
id: counting-what-happened-2
import random

results = [random.choice(["H", "T"]) for i in range(50)]
# your code here
```

**3.3** This cell flips `n` coins and prints the share that came up heads, for four sizes of `n`. Run it five or six times and watch the numbers. What happens to the share as `n` grows? What happens to how much it jumps around from run to run?

```python exec
id: counting-what-happened-3
import random

def fraction_heads(n):
    results = [random.choice(["H", "T"]) for i in range(n)]
    return results.count("H") / n

for n in [10, 100, 1000, 100000]:
    print(n, fraction_heads(n))
```

## 4. The longest streak

A streak is a run of the same result in a row, such as H, H, H, H.

**4.1** Before you write any code, guess the length of the longest streak in 100 flips. Write your guess down.

**4.2** Write `longest_streak(results)`. `longest_streak(["H", "T", "T", "T", "H"])` should give 3.

```python exec
id: the-longest-streak-1
def longest_streak(results):
    longest = 0
    current = 0
    # your loop here
    return longest

print(longest_streak(["H", "T", "T", "T", "H"]))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Walk through the list by position, with `for i in range(len(results))`.
2. Compare each result with the one before it, `results[i - 1]`. The first result has nothing before it, so treat it on its own.
3. When a result matches the one before, the current streak grows by 1. When it does not, a new streak starts. How long is a new streak?
4. After each step, if the current streak is longer than `longest`, update `longest`.

</details>

```solution
def longest_streak(results):
    longest = 0
    current = 0
    for i in range(len(results)):
        if i > 0 and results[i] == results[i - 1]:
            current = current + 1
        else:
            current = 1
        if current > longest:
            longest = current
    return longest

print(longest_streak(["H", "T", "T", "T", "H"]))
```

```inputs
longest_streak(["H", "T", "T", "T", "H"])
longest_streak(["H", "H", "H"])      # one long streak
longest_streak(["H"])                # a single flip
longest_streak([])                   # no flips
```

**4.3** Run `longest_streak` on 100 fresh flips ten times. How close was your guess? Was it too high or too low?

```python exec
id: the-longest-streak-2
import random

# paste your longest_streak function here
for trial in range(10):
    results = [random.choice(["H", "T"]) for i in range(100)]
    # print the longest streak here
```

## 5. Two dice

**5.1** This cell rolls two dice 10000 times and counts each total from 2 to 12. Run it a few times. Which totals turn up most, and which least?

```python exec
id: two-dice-1
import random

def roll_two():
    return random.randint(1, 6) + random.randint(1, 6)

counts = [0] * 13
for i in range(10000):
    counts[roll_two()] += 1
for total in range(2, 13):
    print(total, counts[total])
```

**5.2** Explain the counts. Write code that lists every way two dice can land and counts how many ways make each total from 2 to 12. Compare those numbers with the counts above.

```python exec
id: two-dice-2
ways = [0] * 13
# your loops here
for total in range(2, 13):
    print(total, ways[total])
```

<details class="dl-hint"><summary>smaller steps</summary>

1. On paper, list every way to make 2, then every way to make 3, then every way to make 7. Count each list. Does 3 + 4 count as a different way from 4 + 3?
2. A loop for the first die, `for first in range(1, 7):`, with a second loop for the second die inside it, visits every way the two dice can land. How many ways is that?
3. Inside both loops, add 1 to `ways[first + second]`.
4. Multiply each number of ways by 10000 and divide by 36. How close is that to your counts?

</details>

```solution
ways = [0] * 13
for first in range(1, 7):
    for second in range(1, 7):
        ways[first + second] += 1
for total in range(2, 13):
    print(total, ways[total], round(ways[total] * 10000 / 36))
```

**5.3** Look at the list of ways, from 2 up to 12. Have you seen a pattern like it on the number patterns page? What do the gaps between neighbours look like?

## 6. Questions to think about

This section has no answers to check. The questions are for testing in code and talking over with someone.

**6.1** Somebody writes down 100 "random" coin flips by hand, and a computer makes another 100. Could you tell which list is which? What would you count?

**6.2** How many flips do you need before the share of heads stops moving much? What would "stops moving much" mean in numbers?

**6.3** What would the counts look like for three dice? Which totals are possible, and which do you expect to be most common?

<details class="dl-hint"><summary>ways in</summary>

1. For 6.1, try writing 100 flips by hand yourself, then run `longest_streak` on your list and on a real one.
2. For 6.2, run `fraction_heads` many times for one size of `n`, and look at the smallest and largest answers.
3. For 6.3, add a third loop inside the two from 5.2.

</details>

```python exec
id: questions-to-think-about-1
import random

# your experiments here
```
