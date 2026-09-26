---
title: "Repeating steps with loops — Practice"
practice_for: repeating-yourself
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Repeating steps with loops — Practice

Problems on loops, and three from earlier pages. Before you write any loop,
ask three questions: what am I collecting as I go, what does it start at,
and what makes the loop stop? Try each problem before you open anything
under it.

## 1. What range gives

In this cell, `list()` shows all the numbers in a range at once.

```python exec
id: range-1
print(list(range(5, 5)))
```

```predict
type: text

What will it print?
```

Then say what these give, and try them: `range(5)`, `range(1, 5)`,
`range(0, 10, 3)`, `range(5, 0, -1)`.

<details class="dl-answer"><summary>answer</summary>

`range(5, 5)` gives nothing at all: `[]`. The others give 0 to 4, 1 to 4,
0, 3, 6, 9, and 5 down to 1. The stop value is never included. That is why
programmers write `range(1, n + 1)` for "1 to n": the `+ 1` is on purpose.

</details>

## 2. How many numbers

How many numbers does `range(1, 101)` give? And `range(0, 100)`?

<details class="dl-answer"><summary>answer</summary>

100 each. They cover different numbers, but there are the same number of
them: with a step of 1, the count is `stop - start`. Leaving out the stop
value is what makes that arithmetic so easy.

</details>

## 3. The odd numbers

Can you print the odd numbers from 1 to 99, all on one line? Then can you
do it a second way?

```python exec
id: the-odd-numbers-1

```

```solution
for n in range(1, 100, 2):
    print(n, end=" ")
print()
---
Or `for n in range(1, 100):` with `if n % 2 == 1:` inside. The first takes
fifty steps; the second takes ninety-nine, with a test at each. Both work,
and the first says what it means more directly.
```

## 4. One to a hundred

Can you add up the numbers from 1 to 100 with a loop?

```python exec
id: one-to-a-hundred-1
total = 0

print(total)
```

```inputs
total
```

```solution
total = 0
for i in range(1, 101):
    total = total + i
print(total)
---
5050. The story goes that the young Gauss saw it as fifty pairs, each
adding to 101, which gives the formula $\frac{n(n + 1)}{2}$. When a formula
like that exists, it is a free test of your loop.
```

## 5. Two sigmas

Can you work out $\sum_{i=1}^{10} i^2$, and then $\sum_{i=1}^{10} \frac{1}{i}$?

```python exec
id: two-sigmas-1
squares = 0
fractions = 0

print(squares, fractions)
```

```inputs
squares
fractions
```

```solution
title: with what you've met so far
squares = 0
fractions = 0
for i in range(1, 11):
    squares = squares + i ** 2
    fractions = fractions + 1 / i
print(squares, fractions)
---
385, and about 2.929. The second needs `1 / i`, not `1 // i`: with `//`,
every term after the first is zero, and the sum comes out as 1.
```

```solution
title: a shorter way you'll meet later
squares = sum(i ** 2 for i in range(1, 11))
fractions = sum(1 / i for i in range(1, 11))
print(squares, fractions)
---
`sum(i ** 2 for i in range(1, 11))` is an accumulator loop in one line: it
adds up `i ** 2` for each `i` in the range.
```

## 6. Ten factorial

Can you work out 10! with a loop? Why does the accumulator start at 1, and
not at 0?

```python exec
id: ten-factorial-1
product = 1

print(product)
```

```inputs
product
```

```solution
product = 1
for i in range(1, 11):
    product = product * i
print(product)
---
3,628,800. Starting at 0, it would be 0 forever, because zero times
anything is zero. Each accumulator starts at the value that changes
nothing: 0 for a sum, 1 for a product.
```

## 7. A sum that never settles

What is the sum $1 + \frac{1}{2} + \frac{1}{3} + \dots$ after 1,000 terms?
After 10,000? Does it settle at some value?

```python exec
id: a-sum-that-never-settles-1
total = 0
for i in range(1, 1001):
    total = total + 1 / i
print(total)
```

<details class="dl-answer"><summary>answer</summary>

About 7.485, and about 9.788. It never settles. The sum grows without
limit, but so slowly that it needs more than $10^{43}$ terms to reach 100.
So "the terms are getting smaller" is not enough to make a sum finite.
[Limits: getting closer without arriving](tutorial:approaching-a-limit)
comes back to this.

</details>

## 8. The largest

Can you find the largest number in `[3, 17, 4, 22, 8]` with a loop, without
`max()`? The square brackets make a *list*, which
[Lists: keeping many values in order](tutorial:lists-and-sequences) meets
properly. For now, `for n in numbers:` takes each number in turn, and
`numbers[0]` is the first one.

```python exec
id: the-largest-1
numbers = [3, 17, 4, 22, 8]

print(largest)
```

```inputs
largest
```

```solution
numbers = [3, 17, 4, 22, 8]
largest = numbers[0]
for n in numbers:
    if n > largest:
        largest = n
print(largest)
---
22. The detail to remember is starting at `numbers[0]`, not at 0. Starting
at 0, a list of negative numbers would report 0 as its largest, and 0 is
not in the list.
```

## 9. A loop that never ends

What will this do, and why?

```python
n = 10
while n > 0:
    print(n)
```

<details class="dl-answer"><summary>answer</summary>

It prints 10 forever. Nothing inside the loop changes `n`, so the condition
never becomes `False`. Every `while` loop needs something inside it that
moves it towards stopping, and when a loop never stops, that is the first
thing to look for.

</details>

## 10. Halving

```python exec
id: halving-1
x = 100
count = 0
while x >= 1:
    x = x / 2
    count = count + 1
print(count)
```

```predict
type: number

How many times does it halve 100 before the value drops below 1?
```

<details class="dl-answer"><summary>why</summary>

Seven: 50, 25, 12.5, 6.25, 3.125, 1.5625 and 0.78125. With `x // 2`
instead, it stops at 0, and the loop still ends.

</details>

## 11. While or for

When should you use `while`, and when `for`?

<details class="dl-answer"><summary>one good answer</summary>

`for` is for a known count: every letter of a message, or every number in
a range. `while` is for a condition: until the guess matches, or until the
answer stops changing. Each is awkward doing the other's job: a `while`
loop counting to ten needs its own counter, and a `for` loop that has to
stop early needs a way out.

</details>

## 12. Past a million

Can you find the smallest power of 2 above 1,000,000?

```python exec
id: past-a-million-1
power = 1

print(power)
```

```inputs
power
```

```solution
power = 1
while power <= 1_000_000:
    power = power * 2
print(power)
---
1,048,576, which is $2^{20}$. Python lets you write `1_000_000` with
underscores, to make big numbers easier to read. This is why a "megabyte"
is sometimes 1,048,576 bytes, not a million.
```

## 13. A triangle, and a triangle the other way

Can you print a triangle five rows tall: one `#` on the first row, and five
on the last? Then the same triangle lined up on the right, so the right
edge is straight?

```python exec
id: a-triangle-1

```

```solution
for row in range(1, 6):
    print("#" * row)
for row in range(1, 6):
    print(" " * (5 - row) + "#" * row)
---
No inner loop is needed, because `*` repeats a string. For the second
triangle the spaces are the whole trick. How do you know it is `5 - row`,
not `5 - row - 1`? Try the first and last rows, not the middle ones:
off-by-one slips live at the edges.
```

## 14. Three or seven

How many numbers from 1 to 100 can be divided by 3 *or* by 7?

```python exec
id: three-or-seven-1
count = 0

print(count)
```

```inputs
count
```

```solution
title: with what you've met so far
count = 0
for i in range(1, 101):
    if i % 3 == 0 or i % 7 == 0:
        count = count + 1
print(count)
---
43. There are 33 multiples of 3 and 14 of 7, and 33 + 14 is 47, not 43:
the four multiples of 21 were counted twice. Taking them away once is
called inclusion–exclusion, and
[Venn diagrams: drawing sets and their overlaps](tutorial:venn-diagrams)
turns it into a picture.
```

```solution
title: a shorter way you'll meet later
count = sum(1 for i in range(1, 101) if i % 3 == 0 or i % 7 == 0)
print(count)
---
This adds 1 for every `i` that passes the test, so it counts them.
```

## 15. Backwards

<div class="dl-world" data-world="secret-messages">

Some of the simplest codes just write a message backwards. Can you turn
`"RETTO"` round, with a loop?

```python exec
id: backwards-1--secret-messages
message = "RETTO"
backwards = ""

print(backwards)
```

```inputs
backwards
```

```hint
An accumulator can add to the front as well as the end. What does
`letter + backwards` do, where `backwards + letter` would add to the end?
```

```solution
message = "RETTO"
backwards = ""
for letter in message:
    backwards = letter + backwards
print(backwards)
---
Each new letter goes in front of the ones before it, so the last letter
ends up first: `OTTER`.
```

</div>

<div class="dl-world" data-world="pixel-art">

A row of pixels, written `#` for lit and `.` for dark, can be mirrored left
to right. Can you mirror `"##..#."` with a loop?

```python exec
id: backwards-1--pixel-art
row = "##..#."
mirrored = ""

print(mirrored)
```

```inputs
mirrored
```

```hint
An accumulator can add to the front as well as the end. What does
`pixel + mirrored` do, where `mirrored + pixel` would add to the end?
```

```solution
row = "##..#."
mirrored = ""
for pixel in row:
    mirrored = pixel + mirrored
print(mirrored)
---
Each new pixel goes in front of the ones before it, so the row comes out
mirrored: `.#..##`. Do it to every row of a picture, and the picture faces
the other way.
```

</div>

## 16. Five hundred primes

A prime is a whole number above 1 that only 1 and itself divide. Can you
add up the first 500 primes?

```python exec
id: five-hundred-primes-1
total = 0
found = 0
n = 1

print(total)
```

```inputs
total
```

```hint
The outer loop is a `while`, because nobody knows in advance which number
is the 500th prime. Inside it, a second loop tries each divisor `d` from 2
upwards. Do you need to try divisors bigger than the square root of `n`?
```

```solution
total = 0
found = 0
n = 1
while found < 500:
    n = n + 1
    is_prime = True
    d = 2
    while d * d <= n:
        if n % d == 0:
            is_prime = False
        d = d + 1
    if is_prime:
        total = total + n
        found = found + 1
print(total)
---
824,693. A factor bigger than the square root of `n` always has a partner
smaller than it, so there is nothing new to find above the square root.
That is why the test is `d * d <= n`, and it is what makes the program fast
enough to finish.
```

## 17. Adding the digits

Can you add up the digits of 9,876,543, without turning the number into
text?

```python exec
id: adding-the-digits-1
n = 9876543
total = 0

print(total)
```

```inputs
total
```

```hint
What does `n % 10` give? What does `n // 10` do to `n`?
```

```solution
n = 9876543
total = 0
while n > 0:
    total = total + n % 10
    n = n // 10
print(total)
---
42. `% 10` takes the last digit, and `// 10` removes it. That pair walks
through the digits of any number.
```

## 18. Up and down to one

The Collatz rule says: if a number is even, halve it; if it is odd,
multiply it by three and add one. Starting from 27, how many steps does it
take to reach 1, and how high does it climb on the way?

```python exec
id: up-and-down-to-one-1
n = 27
steps = 0
highest = 27

print(steps, highest)
```

```inputs
steps
highest
```

```solution
n = 27
steps = 0
highest = 27
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    steps = steps + 1
    if n > highest:
        highest = n
print(steps, highest)
---
111 steps, and it climbs as high as 9,232. Nobody has proved that this rule
reaches 1 for every starting number, and nobody has found one that does
not. So this loop is known to stop for every number anyone has tried, but
not known to stop in general, which is an unusual thing for a program this
short.
```

## 19. From earlier: a remainder

From *Algorithms, pseudocode and your first Python*. A film is 200 minutes
long. How many whole hours is that, and how many minutes left over?

<details class="dl-answer"><summary>answer</summary>

`200 // 60` is 3 hours, and `200 % 60` is 20 minutes. `//` counts the whole
ones, and `%` gives what is left.

</details>

## 20. From earlier: one letter back

From *Variables, data types and text*. A Caesar shift of 10 turned a letter
into K. Which letter was it?

```python exec
id: from-earlier-one-letter-back-1
letter = "K"
shift = 10

```

```solution
letter = "K"
shift = 10
position = ord(letter) - ord("A")
moved = (position - shift) % 26
print(chr(moved + ord("A")))
---
A. Moving back is the same shift with a minus, and `% 26` brings a number
below 0 back round to the end of the alphabet.
```

## 21. From earlier: the order of the questions

From *Making decisions with if, elif and else*. This gives every
brightness from 64 up the same character. Why?

```python
if brightness >= 64:
    pixel = "-"
elif brightness >= 128:
    pixel = "+"
elif brightness >= 192:
    pixel = "#"
```

<details class="dl-answer"><summary>answer</summary>

Python runs the first path whose condition is `True`, and skips the rest.
Every brightness of 128 or 192 is also 64 or more, so the first path
catches them all. With `>=`, the biggest threshold goes first.

</details>
