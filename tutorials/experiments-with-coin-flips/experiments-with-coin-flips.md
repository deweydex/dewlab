---
title: "Experiments with coin flips: chance in a list"
year: "2026-2027"
version: 2026.11.23.1
---

# Experiments with coin flips: chance in a list

Python can make random choices with the `random` module. A module is a file of ready-made functions, and `import` brings one in. On this page you flip coins and roll dice inside functions, keep the results in lists, and count what happened.

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

**3.3** Write `fraction_heads(n)`, which flips `n` coins and returns the share that came up heads, as a number between 0 and 1. Run it for 10, 100, 1000 and 100000 flips, a few times each. What happens to the answer as `n` grows? What happens to how much it jumps around?

```python exec
id: counting-what-happened-3
import random

def fraction_heads(n):
    # your code here
    return 0

for n in [10, 100, 1000, 100000]:
    print(n, fraction_heads(n))
```

```solution
import random

def fraction_heads(n):
    heads = 0
    for i in range(n):
        if random.choice(["H", "T"]) == "H":
            heads = heads + 1
    return heads / n

for n in [10, 100, 1000, 100000]:
    print(n, fraction_heads(n))
```

## 4. The longest streak

A streak is a run of the same result in a row, such as H, H, H, H.

**4.1** Before you write any code, guess the length of the longest streak in 100 flips. Write your guess down.

**4.2** Write `longest_streak(results)`. Walk through the list with two counters: the length of the current streak and the longest one so far. `longest_streak(["H", "T", "T", "T", "H"])` should give 3.

```python exec
id: the-longest-streak-1
def longest_streak(results):
    longest = 0
    current = 0
    # your loop here
    return longest

print(longest_streak(["H", "T", "T", "T", "H"]))
```

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

**5.1** Write `roll_two()`, which returns the total of two dice.

```python exec
id: two-dice-1
import random

def roll_two():
    # your code here
    return 0

print(roll_two())
```

```solution
import random

def roll_two():
    return random.randint(1, 6) + random.randint(1, 6)

print(roll_two())
```

**5.2** Roll 10000 times and count each total from 2 to 12. The list `[0] * 13` gives a slot for every total from 0 to 12, and `counts[total] += 1` adds one to the right slot. Which total turns up most often?

```python exec
id: two-dice-2
import random

def roll_two():
    return random.randint(1, 6) + random.randint(1, 6)

counts = [0] * 13
# your loop here
for total in range(2, 13):
    print(total, counts[total])
```

```solution
import random

def roll_two():
    return random.randint(1, 6) + random.randint(1, 6)

counts = [0] * 13
for i in range(10000):
    counts[roll_two()] += 1
for total in range(2, 13):
    print(total, counts[total])
```

**5.3** On paper, list every way two dice can make 7, and every way they can make 2. Does that explain your counts?

## 6. An unfair coin

**6.1** `random.random()` gives a decimal between 0 and 1. Write `unfair_flip(p)`, which returns `"H"` with probability `p`. Check with 10000 flips that `unfair_flip(0.7)` lands heads about 70% of the time.

```python exec
id: an-unfair-coin-1
import random

def unfair_flip(p):
    # your code here
    return "H"

results = [unfair_flip(0.7) for i in range(10000)]
print(results.count("H") / 10000)
```

```solution
import random

def unfair_flip(p):
    if random.random() < p:
        return "H"
    return "T"

results = [unfair_flip(0.7) for i in range(10000)]
print(results.count("H") / 10000)
```
