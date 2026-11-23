---
title: "Experiments with coin flips: chance in a list"
year: "2026-2027"
version: 2026.11.23.3
---

# Experiments with coin flips: chance in a list

Python can make random choices for us. On this page we flip coins and roll dice inside functions, keep the results in lists, and count what happened. The patterns come from the counts.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Random choices

Python's random choices live in a module called `random`. A module is a file of ready-made functions, and the line `import random` brings it in so that we can use them. Two of its functions are useful here: `random.randint(1, 6)` picks a whole number from 1 to 6, like a die, and `random.choice(["H", "T"])` picks one item from a list.

```python exec
id: random-choices-1
import random

print(random.randint(1, 6))
print(random.choice(["H", "T"]))
```

**1.1** Run the cell three times. What changes from run to run, and what stays the same?

<!-- answer -->

**1.2** What do you expect from `random.randint(1, 1)`? What about `random.randint(6, 1)`? Try both, and read any error.

```python exec
id: random-choices-2
print(random.randint(1, 1))
```

<!-- answer -->

**1.3** The cell below sets a seed before rolling. Run it twice. What do you notice? Then change 42 to another number and run it twice more.

```python exec
id: random-choices-3
random.seed(42)
print(random.randint(1, 6), random.randint(1, 6), random.randint(1, 6))
```

<!-- answer -->

## 2. One flip, then many

**2.1** Write a function `flip()` that hands back `"H"` or `"T"` at random. It needs no arguments, so its brackets stay empty.

```python exec
id: one-flip-then-many-1
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

**2.2** The cell below prints ten flips. How could you make them print on one line? `print` has an argument called `end` that decides what comes after each print.

```python exec
id: one-flip-then-many-2
for i in range(10):
    print(flip())
```

**2.3** Write `flips(n)`, which hands back a list of `n` coin flips.

```python exec
id: one-flip-then-many-3
def flips(n):
    results = []
    # your loop here
    return results

print(flips(20))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Write a loop that runs `n` times.
2. Inside the loop, call `flip()` and add its result to `results` with `.append()`.
3. Put the `return` after the loop, not inside it. What happens if it is indented into the loop?

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

**3.1** Write `count_heads(results)`, which counts the heads in a list of flips using a loop and an `if`.

```python exec
id: counting-what-happened-1
def count_heads(results):
    heads = 0
    # your loop here
    return heads

print(count_heads(["H", "T", "H", "H", "T"]))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Loop over the list so that each flip has a name, such as `result`.
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

**3.2** Lists can count for themselves: `results.count("H")` counts the heads in `results`. Does it agree with your function on 50 flips?

```python exec
id: counting-what-happened-2
results = flips(50)
print(count_heads(results), results.count("H"))
```

**3.3** The cell below flips `n` coins and prints the share that came up heads, for four sizes of `n`. Run it five or six times and watch the numbers. What happens to the share as `n` grows? What happens to how much it jumps around from run to run?

```python exec
id: counting-what-happened-3
def fraction_heads(n):
    return flips(n).count("H") / n

for n in [10, 100, 1000, 100000]:
    print(n, fraction_heads(n))
```

<!-- answer -->

## 4. The longest streak

A streak is a run of the same result in a row, such as H, H, H, H.

**4.1** Before writing any code, guess the length of the longest streak in 100 flips.

<!-- answer -->

**4.2** Write `longest_streak(results)`, which hands back the length of the longest streak in a list. `longest_streak(["H", "T", "T", "T", "H"])` should give 3.

```python exec
id: the-longest-streak-1
def longest_streak(results):
    longest = 0
    current = 0
    # your loop here
    return longest

print(longest_streak(["H", "T", "T", "T", "H"]))
print(longest_streak(["H", "H", "H"]))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Walk through the list by position, with `for i in range(len(results))`.
2. Compare each flip with the one before it, `results[i - 1]`. The first flip has nothing before it, so it needs its own case.
3. When a flip matches the one before, the current streak grows by 1. When it does not, a new streak starts. How long is a new streak?
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
print(longest_streak(["H", "H", "H"]))
```

**4.3** The cell below finds the longest streak in 100 fresh flips, ten times over. How close was your guess? Was it too high or too low?

```python exec
id: the-longest-streak-2
for trial in range(10):
    print(longest_streak(flips(100)))
```

<!-- answer -->

## 5. Two dice

**5.1** The cell below rolls two dice 10000 times and counts each total from 2 to 12. The list `counts` has a slot for each total, and `counts[total] += 1` adds one to the right slot. Run it a few times. Which totals turn up most, and which least?

```python exec
id: two-dice-1
def roll_two():
    return random.randint(1, 6) + random.randint(1, 6)

counts = [0] * 13
for i in range(10000):
    counts[roll_two()] += 1
for total in range(2, 13):
    print(total, counts[total])
```

<!-- answer -->

**5.2** On paper, list every way two dice can make a total of 2, then 3, then 7. Does a 3 on the first die and a 4 on the second count as a different way from a 4 and a 3?

<!-- answer -->

**5.3** Write code that goes through every way two dice can land and counts how many ways make each total from 2 to 12. How do those numbers compare with the counts from 5.1?

```python exec
id: two-dice-2
ways = [0] * 13
# your loops here
for total in range(2, 13):
    print(total, ways[total])
```

<details class="dl-hint"><summary>smaller steps</summary>

1. A loop for the first die, `for first in range(1, 7):`, with a second loop inside it for the second die, visits every way the two dice can land. How many ways is that?
2. Inside both loops, add 1 to `ways[first + second]`.
3. Multiply each number of ways by 10000 and divide by 36. How close is that to the counts?

</details>

```solution
ways = [0] * 13
for first in range(1, 7):
    for second in range(1, 7):
        ways[first + second] += 1
for total in range(2, 13):
    print(total, ways[total], round(ways[total] * 10000 / 36))
```

**5.4** Look at the list of ways, from 2 up to 12. Have you seen a pattern like it on the number patterns page? What do the gaps between neighbours look like?

<!-- answer -->

## 6. Questions to think about

This section has no answers to check. The questions are for testing in code and talking over with someone.

**6.1** Somebody writes down 100 "random" coin flips by hand, and a computer makes another 100. Could you tell which list is which? What would you count?

<!-- answer -->

**6.2** How many flips does it take before the share of heads stops moving much? What would "stops moving much" mean in numbers?

<!-- answer -->

**6.3** What would the counts look like for three dice? Which totals are possible, and which would you expect to be most common?

<!-- answer -->

<details class="dl-hint"><summary>ways in</summary>

1. For 6.1, write 100 flips by hand yourself as a list, then compare `longest_streak` on your list and on a real one.
2. For 6.2, run `fraction_heads` many times for one size of `n`, and look at the smallest and largest answers.
3. For 6.3, add a third loop inside the two from 5.3.

</details>

```python exec
id: questions-to-think-about-1
# your experiments here
```
