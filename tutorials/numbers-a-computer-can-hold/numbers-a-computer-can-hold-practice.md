---
title: "Numbers a computer can hold — Practice"
practice_for: numbers-a-computer-can-hold
year: "2026-2027"
version: 2026.09.26.1
---

# Numbers a computer can hold — Practice

Each problem says what kind it is: **Predict**, **Make**, **Fix**,
**Explain** or **Another way**. With numbers, it is tempting to run the
cell first and guess afterwards. Try it the other way round. Write your
guess down, then run. You learn most from the surprises, and a guess
that misses gives you one.

Your `digit_at` from the tutorial page is loaded here. If you have not
written it yet, the page uses a reference version, so every problem
works.

## Warm-up

**1. Predict.** A folder on a computer holds 17 files, and you move
them into smaller folders of 5. What does each line show, and what does
each answer mean for the files?

```python exec
id: numbers-practice-predict-1
print(17 // 5)
print(17 % 5)
print(17 / 5)
```

<details class="dl-answer"><summary>answer</summary>

```text
3
2
3.4
```

`17 // 5` is 3, so there are enough files for 3 full folders. `17 % 5`
is 2, so two files are left over. `17 / 5` is 3.4, which is a true answer in
the rational numbers, but nobody can fill 0.4 of a folder. For this
question, `//` and `%` live in the right space, and `/` does not.

</details>

**2. Explain.** What is the smallest family of numbers, $\mathbb{N}$,
$\mathbb{Z}$, $\mathbb{Q}$ or $\mathbb{R}$, that each of these belongs to?

- (a) 12 pixels in a row
- (b) a temperature of −4 °C in Mullingar in January
- (c) a phone battery three quarters full, 0.75
- (d) $\pi$, the number that turns a circle's width into its distance round

<details class="dl-answer"><summary>answer</summary>

(a) $\mathbb{N}$, a counting number.

(b) $\mathbb{Z}$, because it is a whole number below zero.

(c) $\mathbb{Q}$, because it is the fraction $\frac{3}{4}$.

(d) $\mathbb{R}$, because $\pi$ is not a fraction of two whole numbers.

The families sit inside each other, so 12 is also in $\mathbb{Z}$,
$\mathbb{Q}$ and $\mathbb{R}$. The question asked for the smallest.

</details>

**3. Predict.** What does each line show?

```python exec
id: numbers-practice-predict-2
print(2 + 3 * 4)
print((2 + 3) * 4)
```

<details class="dl-answer"><summary>answer</summary>

`14`, then `20`.

In the first line, the multiply happens before the add: $3 \times 4 =
12$, then $2 + 12 = 14$. In the second, the brackets go first:
$2 + 3 = 5$, then $5 \times 4 = 20$.

</details>

**4. Make.** A phone sends a 50 KB (kilobyte) photo over a network in
packets of 6 KB each. Write two lines that show how many full packets it sends,
and how many KB are left over for one last, smaller packet.

```python exec
id: numbers-practice-make-1
# Your two lines here
```

<details class="dl-answer"><summary>answer</summary>

```python
print(50 // 6)
print(50 % 6)
```

8 full packets, with 2 KB left over. Check: $8 \times 6 + 2 = 50$. That
check always works. The whole part times the divisor, plus the
remainder, gives the number you started with.

</details>

## Core

**5. Predict.** What does each line show? Look carefully at the third.

```python exec
id: numbers-practice-predict-3
print(type(10 / 5))
print(10 // 4)
print(10.0 // 4)
```

<details class="dl-answer"><summary>answer</summary>

```text
<class 'float'>
2
2.0
```

`/` always gives a float, even when the division is exact, so `10 / 5` is
`2.0`, a float. `10 // 4` keeps the whole part, 2, and since both
numbers were ints, the answer is an int. In the third line, `10.0` is a
float, so the answer is a float too: `2.0`. Floor division keeps the
kind of number it was given.

</details>

**6. Fix.** Schlomo, who is learning Python too, has a temperature
sensor that read 12, 15 and 18 °C. He wants the average, which is 15.
His cell shows 33.0 instead. Find the part that does not do what he
meant, and change it.

```python exec
id: numbers-practice-fix-1
print(12 + 15 + 18 / 3)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which happens first in this line, the adding or the dividing?
2. So which number is being divided by 3?
3. How can you make the adding happen first?

**Think about:** how would you write this average on paper, with a line
for the division?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print((12 + 15 + 18) / 3)
```

Division comes before addition, so Schlomo's line calculated
$18 \div 3 = 6$ first, then $12 + 15 + 6 = 33$. Brackets make the adding
happen first: $45 \div 3 = 15.0$.

On paper, he would have written $\frac{12 + 15 + 18}{3}$, and the long
line does the job of the brackets. Python has no long line, so we write
the brackets ourselves. His way of writing it came from paper, where it
works.

</details>

**7. Fix.** A video lasts 135 minutes. This cell should show it in
hours and minutes: 2 hours and 15 minutes. Run it and see what it shows
instead, then fix it.

```python exec
id: numbers-practice-fix-2
minutes = 135
print(minutes / 60, "hours and", minutes % 60, "minutes")
```

<details class="dl-answer"><summary>answer</summary>

It shows `2.25 hours and 15 minutes`. The 2.25 hours already includes
the 15 minutes (a quarter of an hour), so the time is counted twice.

```python
minutes = 135
print(minutes // 60, "hours and", minutes % 60, "minutes")
```

This shows `2 hours and 15 minutes`. `//` gives the whole hours, and `%`
gives the minutes left over. `digit_at(135, 1, 60)` and
`digit_at(135, 0, 60)` give the same two numbers, because hours and
minutes are base 60 too.

</details>

**8. Another way.** Schlomi, who is also learning Python, says: "You
can't take 5 away from 3." Schlomo says you can, and the answer is −2.
Find a space where Schlomi's idea works, and a space where Schlomo's
does.
Give a real situation for each.

<details class="dl-answer"><summary>answer</summary>

Schlomi's idea works in $\mathbb{N}$. If a phone has 3 GB (gigabytes) of free space, it
cannot store a 5 GB video. There is no such thing as −2 GB of free
space.

Schlomo's works in $\mathbb{Z}$. If it is 3 °C and the temperature
drops by 5 degrees, it is −2 °C.

They are answering in two different spaces. Here is one pair of
situations. Yours may be different and work too.

</details>

**9. Make.** A message on a phone app is shared in rounds. In the
first round, one person sends it to 2 people. In each round after that,
the number who get it doubles. In the 2022 census, Ireland's population
was 5,149,139. Use `math.log2` to find about how many rounds of
doubling it takes for one round to reach that many people.

```python exec
id: numbers-practice-make-2
import math

# Your line here
```

<details class="dl-answer"><summary>answer</summary>

```python
import math

print(math.log2(5149139))
```

It shows about 22.3. So 22 doublings are not quite enough, and 23 are
more than enough. Check with powers: $2^{22} = 4{,}194{,}304$, which is
less than the population, and $2^{23} = 8{,}388{,}608$, which is more.

A very big number needs surprisingly few doublings. That is why a
message can reach a whole country in a day.

</details>

<aside class="dl-note" id="numbers-practice-note-census">

**Five million again.** The 2022 census counted more than five million
people. The last census to count that many in the same area was in
1851. After 1851 the number fell for more than a hundred years. It was
lowest in 1961, at 2,818,341.

</aside>

**10. Explain.** Predict what this cell shows, then run it. Why is the
answer what it is, and why might it matter in a program that handles
money?

```python exec
id: numbers-practice-explain-1
print(0.1 + 0.2 == 0.3)
```

<details class="dl-answer"><summary>answer</summary>

It shows `False`.

`0.1 + 0.2` is `0.30000000000000004` as a float. Python cannot store 0.1
or 0.2 exactly, only very close to them, and the tiny differences appear
in the sum. `==` asks whether two values are exactly equal, and these
two are not quite equal.

So a program should not test floats with `==` before rounding them.
Try `print(round(0.1 + 0.2, 2) == 0.3)`. It shows `True`. Programs that
handle money often count in whole cents instead, since ints are exact.
A later page in this unit explains why 0.1 cannot be stored exactly.

</details>

**11. Make.** A microwave timer has 754 seconds left. Use `digit_at`
to find the minutes and the seconds it shows. Then find the four digits
its display lights, from left to right.

```python exec
id: numbers-practice-make-3
# Your lines here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The seconds are the digit in place 0, in base 60.
2. The minutes are the digit in place 1, in base 60.
3. Each of those is a number from 0 to 59. Its tens digit is place 1,
   and its ones digit is place 0, in base 10.

**Think about:** why the base-10 calls need no third number.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
minutes = digit_at(754, 1, 60)
seconds = digit_at(754, 0, 60)
print(minutes, seconds)
print(digit_at(minutes, 1), digit_at(minutes, 0), digit_at(seconds, 1), digit_at(seconds, 0))
```

This shows `12 34`, then `1 2 3 4`, so the timer reads 12:34. Check:
$12 \times 60 + 34 = 754$. The base-10 calls have no third number,
so `base` takes its default value, 10.

</details>

**12. Make.** On a piano, one A is 110 Hz and a higher A is 1760 Hz.
(Hz, hertz, counts how many times a sound wave shakes the air each
second.) Each octave up doubles the frequency. Use `math.log2` to find
how many octaves apart the two notes are.

```python exec
id: numbers-practice-make-4
import math

# Your line here
```

<details class="dl-answer"><summary>answer</summary>

```python
import math

print(math.log2(1760 / 110))
```

It shows `4.0`, so they are 4 octaves apart. First, $1760 \div 110 = 16$,
so the higher note shakes the air 16 times as fast. Then
$\log_2 16 = 4$, because $2^4 = 16$. Check by doubling: 110, 220, 440,
880, 1760. That is four doublings.

</details>

## Stretch

**13. Another way.** The tutorial found $\log_2 128$ with `math.log2`.
Find $\log_2 1024$ another way, without any logarithm and without a
computer. Start from 1024 and keep halving.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Halve 1024. Write the answer down.
2. Halve that. Keep going.
3. Stop when you reach 1.
4. Count how many halvings you did.

**Think about:** why does counting halvings down to 1 give the same
answer as counting doublings up from 1?

**Try this next:** how many halvings from 1,000,000 to get below 1? What
does `math.log2(1000000)` say?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1. That is 10 halvings, so
$\log_2 1024 = 10$.

Halving down to 1 undoes doubling up from 1, one step at a time. So the
number of halvings is the number of doublings, which is the logarithm.
This idea also explains why halving a sorted list is such a fast way
to search it. A later unit uses it.

For the "try this next", `math.log2(1000000)` is about 19.9, so 20
halvings take a million below 1.

</details>

**14. Fix.** Schlomi wants the tens digit of a number. Her idea is to
take the last digit, then divide it by 10. For 2026 her function gives
0, but the tens digit is 2. Can you find the mistake in the idea, and fix
it?

```python exec
id: numbers-practice-fix-3
def tens_digit(number):
    """Give the tens digit of a whole number."""
    return number % 10 // 10
```

```inputs
tens_digit(2026)
tens_digit(57)
```

```solution
def tens_digit(number):
    """Give the tens digit of a whole number."""
    return number // 10 % 10
---
`2026 % 10` is 6, and `6 // 10` is 0. Any last digit is less than 10,
so her function gives 0 every time. The first step loses the tens
digit.

The steps need the other order. First drop the last digit, then keep
the new last digit.

This is about *what happens when*. Here is another way that
works: `number % 100 // 10` keeps the last two digits first, 26, then
drops the ones, leaving 2. Schlomi had the two moves she needed. Only
their order had to change.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find `tens_digit(2026)` by hand. What is `2026 % 10`?
2. What is that number `// 10`?
3. Which of `%` and `//` should happen first, to remove the ones
   digit?

**Think about:** which of the four questions is this about?

</details>

**15. Predict.** You know `7 // 2` is 3. What do you think `-7 // 2` is?
Make a guess, then run the cell.

```python exec
id: numbers-practice-predict-4
print(-7 // 2)
print(-7 % 2)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Calculate $-7 \div 2$ exactly. You get −3.5.
2. Draw a number line, and mark −3.5 on it.
3. `//` is floor division. Floor means "the next whole number down".
   Which whole number comes next below −3.5 on your line?

**Think about:** is "down" the same as "towards zero" for a negative
number?

</details>

<details class="dl-answer"><summary>answer</summary>

`-4`, then `1`.

$-7 \div 2 = -3.5$. Floor division rounds down, to the whole number
below, and on the number line the whole number below −3.5 is −4, not
−3. For positive numbers, rounding down and removing the decimal
part give the same answer. For negative numbers they do not.

The remainder follows from that. Python keeps the rule from problem 4:
$-4 \times 2 + 1 = -7$. So the remainder is 1.

Most people guess −3, and that is what some other programming
languages give, because they round towards zero. Python
chose "down" instead.

</details>

**16. Make.** A photo 1920 pixels wide is shrunk to fit a screen 1280
pixels wide. Write a function `scale(position, from_width, to_width)`
that returns where a pixel's column moves to. Give it a docstring, and
test it with at least two `assert` lines.

```python exec
id: numbers-practice-make-5
def scale(position, from_width, to_width):
    """Your promise here."""
    ...
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What fraction of the way across the photo is `position`?
2. Where is that same fraction of the way across the new width?
3. Write that as one expression after `return`.
4. Test it with numbers you can check in your head: halfway across 1920
   is 960, and halfway across 1280 is 640.

**Think about:** does your function work for any two widths, or only
these?

**Try this next:** what does your function give for column 1, from a
width of 3 to a width of 2? Is that a column a screen can have?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def scale(position, from_width, to_width):
    """Return where column position moves to, when an image
    from_width pixels wide is scaled to to_width pixels wide."""
    return position / from_width * to_width

assert scale(960, 1920, 1280) == 640
assert scale(100, 400, 200) == 50
```

First we divide by the old width, to find how far across the pixel is.
960 is half of 1920. Then we multiply by the new width: half of 1280 is
640. The promise is about any two widths, so it works for any image.

For the "try this next", `scale(1, 3, 2)` gives 0.6666666666666666.
There is no column 0.67. A real program would round it, or use `//`,
to land on a whole pixel.

</details>

**17. Explain.** The tutorial page met logarithms as a question, "how
many times do I multiply?". Another course might teach the rules first,
such as $\log_2(a \times b) = \log_2 a + \log_2 b$. For someone meeting
logarithms for the first time, which would you start with, the question
or the rules? Say why, and say what a learner who met only your choice
would be missing.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. It looks at a few things.

- **The question first** gives the idea something to be about. A learner
  knows what a logarithm is for before they learn its rules. For now,
  they miss a way to work with logarithms on paper, which exams often
  ask for.
- **The rules first** are quick to use, and they are what a calculator
  and many exam questions need. A learner can miss what the rules mean,
  and then the rules are hard to rebuild if they are forgotten.

The question can even explain a rule. Multiplying 8 by 4 means doubling 3
times and then 2 more times, 5 doublings in all:

```python
import math

print(math.log2(8 * 4))
print(math.log2(8) + math.log2(4))
```

Both lines show `5.0`. So one answer might start with the question,
and let the rules arrive as facts about it. Someone who chose the rules
first, with reasons about exams, has another.

</details>
