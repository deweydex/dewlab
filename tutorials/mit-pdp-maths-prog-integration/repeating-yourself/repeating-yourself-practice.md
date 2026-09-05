---
title: "Repeating Yourself — Practice"
slug: repeating-yourself-practice
practice_for: repeating-yourself
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Repeating Yourself — Practice

Answers are folded. For every loop here, ask the same three questions before you write it: what am I accumulating, what does it start at, and what makes it stop.

## Range

```python exec
id: range-1
print(list(range(5)))
print(list(range(1, 6)))
print(list(range(0, 20, 5)))
print(list(range(10, 0, -2)))
```

**1.** What does each produce?

- (a) `range(5)`
- (b) `range(1, 5)`
- (c) `range(0, 10, 3)`
- (d) `range(5, 0, -1)`
- (e) `range(5, 5)`

<details class="dl-answer"><summary>answer</summary>

(a) 0, 1, 2, 3, 4. (b) 1, 2, 3, 4. (c) 0, 3, 6, 9. (d) 5, 4, 3, 2, 1. (e) nothing at all.

The end is never included. That is why `range(1, n + 1)` is the idiom for "1 to n" and why the `+ 1` is not a mistake somebody left in.

</details>

**2.** How many numbers does `range(1, 101)` produce? And `range(0, 100)`?

<details class="dl-answer"><summary>answer</summary>

100 each.

They cover different numbers and there are the same quantity of them. Counting the elements of a range is `(stop - start)` divided by the step, and this is the one place where excluding the end makes the arithmetic simple.

</details>

**3.** Write a loop that prints the odd numbers from 1 to 99. Then write it a second way.

<details class="dl-answer"><summary>answer</summary>

```python
for n in range(1, 100, 2):
    print(n, end=" ")
```

Or by filtering:

```python
for n in range(1, 100):
    if n % 2 == 1:
        print(n, end=" ")
```

The first does fifty steps, the second ninety-nine and a test each time. Both are correct; the first says what it means more directly.

</details>

## Accumulators

**4.** Compute the sum of the numbers from 1 to 100.

<details class="dl-answer"><summary>answer</summary>

```python
total = 0
for i in range(1, 101):
    total = total + i
print(total)
```

5050. Gauss is said to have seen it as fifty pairs each adding to 101, which is the formula `n(n + 1)/2`. Check that the loop and the formula agree — when a closed form exists, it is a free test of the loop.

</details>

**5.** Compute $\sum_{i=1}^{10} i^2$, then $\sum_{i=1}^{10} \frac{1}{i}$.

<details class="dl-answer"><summary>answer</summary>

385, and about 2.9290.

```python
print(sum(i ** 2 for i in range(1, 11)))
print(sum(1 / i for i in range(1, 11)))
```

Written as a loop, the second one needs `1 / i` rather than `1 // i`, or every term after the first is zero and the answer is 1.

</details>

**6.** Compute 10! with a loop. Why does the accumulator start at 1 rather than 0?

<details class="dl-answer"><summary>answer</summary>

3,628,800.

```python
product = 1
for i in range(1, 11):
    product = product * i
```

Starting at 0 would give 0 forever, because zero times anything is zero. Each accumulator has to start at the value that changes nothing: 0 for a sum, 1 for a product. Mathematicians call those identity elements, and the reason they matter here is entirely practical.

</details>

**7.** What is the sum of the harmonic series after 1,000 terms? After 10,000? Does it settle anywhere?

<details class="dl-answer"><summary>answer</summary>

About 7.485 and about 9.788.

It never settles. The harmonic series grows without bound, but so slowly that it takes over 10^43 terms to reach 100. This is one of the better demonstrations that "the terms are getting smaller" is not enough to make a sum finite — a point *Approaching a Limit* comes back to.

</details>

**8.** Find the largest number in `[3, 17, 4, 22, 8]` with a loop, without using `max()`.

<details class="dl-answer"><summary>answer</summary>

```python
numbers = [3, 17, 4, 22, 8]
largest = numbers[0]
for n in numbers:
    if n > largest:
        largest = n
print(largest)
```

22. Starting at `numbers[0]` rather than 0 is the detail worth keeping: start at zero and a list of negative numbers reports its maximum as 0, which is not in the list.

</details>

## While Loops

**9.** What is wrong with this?

```python
n = 10
while n > 0:
    print(n)
```

<details class="dl-answer"><summary>answer</summary>

Nothing changes `n`, so the condition never becomes false and it prints 10 forever.

Every `while` needs something inside it that moves towards the stopping condition. When one hangs, that is the first thing to look for.

</details>

**10.** Write a loop that halves a number until it drops below 1, printing each value.

<details class="dl-answer"><summary>answer</summary>

```python
x = 100
while x >= 1:
    print(x)
    x = x / 2
```

It stops after seven halvings. If you write `x = x // 2` instead it also stops, and at zero rather than at 0.78 — integer division on the way down eventually gets stuck at 0, which for once is a stop rather than a hang.

</details>

**11.** When should you use `while` rather than `for`?

<details class="dl-answer"><summary>answer</summary>

When you do not know how many times in advance.

`for` is for a known count — every item of a list, every number in a range. `while` is for a condition — until the user types "quit", until the guess is right, until the answer stops changing. Written the other way round, both are awkward: a `for` loop faking a `while` needs a `break`, and a `while` counting to ten needs its own counter.

</details>

**12.** Write a loop that finds the smallest power of 2 above 1,000,000.

<details class="dl-answer"><summary>answer</summary>

```python
power = 1
while power <= 1_000_000:
    power = power * 2
print(power)
```

1048576, which is 2^20. This is why a "megabyte" is sometimes 1,048,576 bytes rather than a million.

</details>

## Nested Loops

**13.** Print a 10 by 10 multiplication table with the columns lined up.

<details class="dl-answer"><summary>answer</summary>

```python
for row in range(1, 11):
    for col in range(1, 11):
        print(str(row * col).rjust(5), end="")
    print()
```

The `print()` on its own after the inner loop is what ends the row. Leaving it out prints a hundred numbers on one line, which is the classic first attempt.

</details>

**14.** How many multiplications does that table perform? What if it were 100 by 100?

<details class="dl-answer"><summary>answer</summary>

100, and 10,000.

Two nested loops of n steps each do n² operations. That squaring is what makes the difference between a fast and a slow algorithm later, in *Putting Things in Order* — and it is why a sort that compares every pair struggles on a large list.

</details>

**15.** Print a triangle of stars, five rows tall: one star on the first row, five on the last.

<details class="dl-answer"><summary>answer</summary>

```python
for row in range(1, 6):
    print("*" * row)
```

No inner loop needed, because `*` repeats a string. Written with an inner loop it also works, and this version says the intention in one line.

</details>

**16.** Print the same triangle right-aligned, so the left edge slopes and the right edge is straight.

<details class="dl-answer"><summary>answer</summary>

```python
for row in range(1, 6):
    print(" " * (5 - row) + "*" * row)
```

The spaces are the whole trick, and getting `5 - row` rather than `5 - row - 1` right is a matter of trying it on the first and last rows rather than on the middle ones. Edges are where off-by-one errors live.

</details>

## Loops With Conditions

**17.** Count the numbers from 1 to 100 divisible by both 3 and 7. Then by 3 or 7.

<details class="dl-answer"><summary>answer</summary>

Four (21, 42, 63, 84), and forty-three.

```python
print(sum(1 for i in range(1, 101) if i % 3 == 0 and i % 7 == 0))
print(sum(1 for i in range(1, 101) if i % 3 == 0 or i % 7 == 0))
```

Note that 33 + 14 is 47, not 43. The four multiples of 21 were counted twice, and subtracting them once is inclusion–exclusion, which *Drawing Sets* makes a picture of.

</details>

**18.** Print all numbers from 1 to 50 that are perfect squares or perfect cubes.

<details class="dl-answer"><summary>answer</summary>

1, 4, 8, 9, 16, 25, 27, 36, 49.

```python
squares = {i * i for i in range(1, 8)}
cubes = {i ** 3 for i in range(1, 4)}
print(sorted(squares | cubes))
```

Generating them is more reliable than testing them. Testing with `n ** 0.5 == int(n ** 0.5)` works for small numbers and starts lying at large ones, because the square root is a float and floats are approximate.

1 is both a square and a cube, and appears once.

</details>

**19.** Sum the first 500 prime numbers.

<details class="dl-answer"><summary>answer</summary>

824,693.

```python
def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 1
    return True


total, found, n = 0, 0, 1
while found < 500:
    n = n + 1
    if is_prime(n):
        total = total + n
        found = found + 1
print(total)
```

Two things worth noticing. The outer loop is a `while` because you do not know in advance which number the 500th prime is. And `d * d <= n` rather than `d <= n` is what makes it fast enough to finish — a factor larger than the square root always has a partner smaller than it, so there is nothing above there to find.

</details>

**20.** Compute the sum of the digits of 9,876,543.

<details class="dl-answer"><summary>answer</summary>

42.

```python
n, total = 9876543, 0
while n > 0:
    total = total + n % 10
    n = n // 10
print(total)
```

`% 10` takes the last digit and `// 10` removes it. That pair walks through the digits of any number without turning it into text, and it is the same shift-and-take pattern as reading a number in another base.

</details>

**21.** The Collatz rule: if a number is even, halve it; if odd, triple it and add one. Starting from 27, how many steps does it take to reach 1?

<details class="dl-answer"><summary>answer</summary>

111 steps, having climbed as high as 9,232 on the way.

```python
n, steps, highest = 27, 0, 27
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps, highest = steps + 1, max(highest, n)
print(steps, highest)
```

Nobody has proved that this reaches 1 for every starting number, and nobody has found one that does not. So this is a `while` loop that is known to stop for every value anyone has tried and not known to stop in general — which is a genuinely unusual thing for a five-line program to be.

</details>
