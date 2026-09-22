---
title: "Repeating Yourself — Practice"
practice_for: repeating-yourself
year: "2026-2027"
version: 2026.08.23.1
---

# Repeating Yourself — Practice

The answers are hidden until you open them. Before you write any loop
on this page, ask yourself three questions:

1. What am I accumulating?
2. What does it start at?
3. What makes the loop stop?

## Range

In this cell, `list()` shows all the numbers in a range at once.

```python exec
id: range-1
print(list(range(5)))
print(list(range(1, 6)))
print(list(range(0, 20, 5)))
print(list(range(10, 0, -2)))
```

**1.** What numbers does each one give?

- (a) `range(5)`
- (b) `range(1, 5)`
- (c) `range(0, 10, 3)`
- (d) `range(5, 0, -1)`
- (e) `range(5, 5)`

<details class="dl-answer"><summary>answer</summary>

(a) 0, 1, 2, 3, 4. (b) 1, 2, 3, 4. (c) 0, 3, 6, 9. (d) 5, 4, 3, 2, 1.
(e) nothing at all.

The stop value is never included. That is why programmers write
`range(1, n + 1)` for "1 to n". The `+ 1` is not a mistake that somebody
left in.

</details>

**2.** How many numbers does `range(1, 101)` give? And `range(0, 100)`?

<details class="dl-answer"><summary>answer</summary>

100 each.

They cover different numbers, but there are the same number of them.
With a step of 1, the count is always `stop - start`. (With a bigger
step, divide by the step and round up.) Leaving out the stop value is
what makes this arithmetic so easy.

</details>

**3.** Write a loop that prints the odd numbers from 1 to 99. Can you
then write it a second way?

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

The first way takes fifty steps. The second takes ninety-nine, with a
test at each one. Both are correct, but the first says what it means
more directly.

</details>

## Accumulators

**4.** Work out the sum of the numbers from 1 to 100.

<details class="dl-answer"><summary>answer</summary>

```python
total = 0
for i in range(1, 101):
    total = total + i
print(total)
```

The answer is 5050. The story is that Gauss saw it as fifty pairs, each
adding up to 101. That gives the formula `n(n + 1)/2`. Check that the
loop and the formula agree. When a formula like this exists, it gives
you a free test of your loop.

</details>

**5.** Work out $\sum_{i=1}^{10} i^2$, then $\sum_{i=1}^{10} \frac{1}{i}$.

<details class="dl-answer"><summary>answer</summary>

385, and about 2.9290.

```python
print(sum(i ** 2 for i in range(1, 11)))
print(sum(1 / i for i in range(1, 11)))
```

`sum(i ** 2 for i in range(1, 11))` is a short way to write an
accumulator loop. It adds up `i ** 2` for each `i` in the range.

If you write the second one as a loop, it needs `1 / i`, and not
`1 // i`. With `//`, every term after the first is zero, and the answer
comes out as 1.

</details>

**6.** Work out 10! with a loop. Why does the accumulator start at 1, and
not at 0?

<details class="dl-answer"><summary>answer</summary>

3,628,800.

```python
product = 1
for i in range(1, 11):
    product = product * i
```

If it started at 0, the answer would be 0 forever, because zero times
anything is zero. Each accumulator has to start at the value that
changes nothing: 0 for a sum, and 1 for a product. Mathematicians call
these values identity elements. Here, the reason they matter is
completely practical.

</details>

**7.** What is the sum of the harmonic series after 1,000 terms? After
10,000? Does it settle at some value?

<details class="dl-answer"><summary>answer</summary>

About 7.485, and about 9.788.

It never settles. The harmonic series grows without limit, but so slowly
that it needs more than 10^43 terms to reach 100. This shows that "the
terms are getting smaller" is not enough to make a sum finite.
[Approaching a Limit](tutorial:approaching-a-limit) comes back to this
point.

</details>

**8.** Find the largest number in `[3, 17, 4, 22, 8]` with a loop,
without using `max()`.

<details class="dl-answer"><summary>answer</summary>

```python
numbers = [3, 17, 4, 22, 8]
largest = numbers[0]
for n in numbers:
    if n > largest:
        largest = n
print(largest)
```

The answer is 22. The detail to remember is starting at `numbers[0]`,
the first item, and not at 0. If you start at zero, a list of negative
numbers reports its largest value as 0, which is not in the list.

</details>

## While Loops

**9.** What is wrong with this?

```python
n = 10
while n > 0:
    print(n)
```

<details class="dl-answer"><summary>answer</summary>

Nothing changes `n`. So the condition never becomes False, and the loop
prints 10 forever.

Every `while` loop needs something inside it that moves it towards the
stopping condition. When a loop never stops, that is the first thing to
look for.

</details>

**10.** Write a loop that halves a number until it drops below 1, and
prints each value.

<details class="dl-answer"><summary>answer</summary>

```python
x = 100
while x >= 1:
    print(x)
    x = x / 2
```

It stops after seven halvings. If you write `x = x // 2` instead, it
also stops, but at 0 and not at 0.78. Whole-number division on the way
down reaches 0 in the end. Here, for once, that means the loop stops,
and does not run forever.

</details>

**11.** When should you use `while`, and when `for`?

<details class="dl-answer"><summary>answer</summary>

Use `while` when you do not know in advance how many times to repeat.

`for` is for a known count: every item of a list, or every number in a
range. `while` is for a condition: until the user types "quit", until
the guess is right, or until the answer stops changing. Each one is
awkward when it does the other one's job. A `for` loop acting as a
`while` needs a `break` to get out early, and a `while` loop counting to
ten needs its own counter.

</details>

**12.** Write a loop that finds the smallest power of 2 above 1,000,000.

<details class="dl-answer"><summary>answer</summary>

```python
power = 1
while power <= 1_000_000:
    power = power * 2
print(power)
```

The answer is 1048576, which is 2^20. (Python lets you write
`1_000_000` with underscores, to make big numbers easier to read.) This
is why a "megabyte" is sometimes 1,048,576 bytes, and not a million.

</details>

## Nested Loops

**13.** Print a 10 by 10 multiplication table, with the columns lined
up.

<details class="dl-answer"><summary>answer</summary>

```python
for row in range(1, 11):
    for col in range(1, 11):
        print(str(row * col).rjust(5), end="")
    print()
```

The `print()` on its own, after the inner loop, is what ends each row.
If you leave it out, all hundred numbers print on one line. That is the
classic first attempt.

</details>

**14.** How many multiplications does that table do? What if it were 100
by 100?

<details class="dl-answer"><summary>answer</summary>

100, and 10,000.

Two nested loops of n steps each do n² steps. That squaring is what
separates a fast algorithm from a slow one later, in
[Putting Things in Order](tutorial:putting-things-in-order). It is also
why a sort that compares every pair of items struggles on a large list.

</details>

**15.** Print a triangle of stars, five rows tall: one star on the first
row, and five on the last.

<details class="dl-answer"><summary>answer</summary>

```python
for row in range(1, 6):
    print("*" * row)
```

You do not need an inner loop, because `*` repeats a string. A version
with an inner loop also works, but this version says what it means in
one line.

</details>

**16.** Print the same triangle lined up on the right, so that the left
edge slopes and the right edge is straight.

<details class="dl-answer"><summary>answer</summary>

```python
for row in range(1, 6):
    print(" " * (5 - row) + "*" * row)
```

The spaces are the whole trick. How do you know it is `5 - row` and not
`5 - row - 1`? Try it on the first and last rows, not the middle ones.
Off-by-one errors live at the edges.

</details>

## Loops With Conditions

**17.** Count the numbers from 1 to 100 that can be divided by both 3
and 7. Then count those that can be divided by 3 or 7.

<details class="dl-answer"><summary>answer</summary>

Four (21, 42, 63, 84), and forty-three.

```python
print(sum(1 for i in range(1, 101) if i % 3 == 0 and i % 7 == 0))
print(sum(1 for i in range(1, 101) if i % 3 == 0 or i % 7 == 0))
```

Each line adds 1 for every `i` that passes the test, so it counts them.

Notice that 33 + 14 is 47, not 43. The four multiples of 21 were counted
twice. Taking them away once is called inclusion–exclusion, and
[Drawing Sets](tutorial:venn-diagrams) turns it into a picture.

</details>

**18.** Print all the numbers from 1 to 50 that are perfect squares or
perfect cubes.

<details class="dl-answer"><summary>answer</summary>

1, 4, 8, 9, 16, 25, 27, 36, 49.

```python
squares = {i * i for i in range(1, 8)}
cubes = {i ** 3 for i in range(1, 4)}
print(sorted(squares | cubes))
```

The curly brackets make a set, which is a collection with no repeats.
`|` joins two sets together, and `sorted()` puts the result in order.

Making the squares and cubes is more reliable than testing for them. A
test like `n ** 0.5 == int(n ** 0.5)` works for small numbers, but gives
wrong answers for large ones. The square root is a float, and floats are
approximate.

1 is both a square and a cube, and it appears once.

</details>

**19.** Add up the first 500 prime numbers.

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

This answer uses `def` to make a function, `is_prime`, and `return` to
give back its answer. We meet these in
[Lists and Sequences](tutorial:lists-and-sequences). The line
`total, found, n = 0, 0, 1` sets three variables at once.

There are two things to notice here:

- The outer loop is a `while`, because you do not know in advance which
  number the 500th prime is.
- A factor larger than the square root of `n` always has a partner
  factor smaller than it. So there is nothing new to find above the
  square root. That is why the test is `d * d <= n`, and not `d <= n`,
  and it is what makes the program fast enough to finish.

</details>

**20.** Work out the sum of the digits of 9,876,543.

<details class="dl-answer"><summary>answer</summary>

42.

```python
n, total = 9876543, 0
while n > 0:
    total = total + n % 10
    n = n // 10
print(total)
```

`% 10` takes the last digit, and `// 10` removes it. That pair walks
through the digits of any number without turning it into text. It is
the same shift-and-take pattern as reading a number in another base.

</details>

**21.** The Collatz rule says: if a number is even, halve it; if it is
odd, multiply it by three and add one. Starting from 27, how many steps
does it take to reach 1?

<details class="dl-answer"><summary>answer</summary>

111 steps. On the way, it climbs as high as 9,232.

```python
n, steps, highest = 27, 0, 27
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps, highest = steps + 1, max(highest, n)
print(steps, highest)
```

Two short forms appear here. `n // 2 if n % 2 == 0 else 3 * n + 1`
gives `n // 2` when `n` is even, and `3 * n + 1` when it is odd.
`max(highest, n)` gives the larger of the two values.

Nobody has proved that this rule reaches 1 for every starting number.
Nobody has found a number that does not reach 1, either. So this
`while` loop is known to stop for every value anyone has tried, but not
known to stop in general. That is an unusual thing for a five-line
program to be.

</details>
