---
title: "Surds and logs in the wild: A4 paper and the largest prime"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Surds and logs in the wild: A4 paper and the largest prime

This is the last page of this part of the module. It uses side and hops
on two real things: a sheet of paper, and a very big number.

Here are four sheets of paper, drawn to scale. Their names are A3, A4,
A5 and A6. Most countries use these sizes. A4 is the normal size for a
printer.

<img src="paper-sizes.svg" alt="Four sheets of paper drawn to scale, each in the top left corner of the one before. The biggest, A3, lies on its long side. A4 stands up in its corner and covers the left half of it. A5 lies on its long side in the corner of A4 and covers the top half of A4. A6 stands up in the corner of A5 and covers the left half of A5. Beside the sheets is a list of sizes: A3 is 297 × 420 mm, A4 is 210 × 297 mm, A5 is 148 × 210 mm, and A6 is 105 × 148 mm.">

```question
id: four-sheets-1
type: multiple-choice
answer: 1

How many A4 sheets cover one A3 sheet, with no gaps?

- 2
  - A4 covers the left half of A3. A second A4 would cover the right
    half.
- 4
  - Four sheets would each be a quarter of A3. That is the size of A5.
- 3
  - Look at the picture. A4 covers exactly half of A3.
```

## Folding in half

Fold an A4 sheet in half, so that the fold cuts its long side in two.
Each half is an A5 sheet.

```question
id: folding-in-half-1
type: fill-in-the-blank

A4 is 210 mm by 297 mm. Half of 297 is
{148.5|105|210}.

So each half is 210 mm by 148.5 mm. The list says A5 is 148 by
{210|297|105}
mm.
```

The sizes in the list are whole millimetres. A millimetre (mm) is about
the thickness of a bank card. The list drops the half, so 148.5 mm
becomes 148 mm.

## The same shape?

A5 looks like a small A4, lying on its side. Two sheets have the *same
shape* when one is the other made bigger or smaller, with nothing
stretched.

Here is a test for the same shape. Divide the long side by the short
side. If two sheets give the same answer, they have the same shape.

```python exec
id: the-same-shape-1
print("A3", 420 / 297)
print("A4", 297 / 210)
print("A5", 210 / 148)
```

```predict
type: choice

Before you run it: what will the three lines print?

- Three numbers close to each other
- Three very different numbers
  - A3 is much bigger than A5. But each line divides the two sides of
    one sheet.
- Three numbers close to 2
  - A3 is two A4s, so 2 can feel natural here.
```

All three start with 1.41. On every sheet, the long side is about 1.41
times the short side. Try A6 too: 148 / 105.

```question
id: the-same-shape-2
type: multiple-choice
answer: 1

Have you seen a number close to 1.414 before, on an earlier page?

- side(2)
  - side(2) is 1.41421…, from *Sides that never end: surds, the square
    root of 2*.
- side(4)
  - side(4) is 2, because 2 × 2 = 4.
- hops(10 → 100)
  - hops(10 → 100) is 2. Two hops of ×10 land on 100.
```

Why would paper have side(2) in it? The next four steps show why.

## A sheet we do not know

Take any sheet. Measure it with its own short side as the ruler. Then
the short side is 1, and the long side is a number we do not know yet.
Call it r. The letter r says how many short sides fit along the long
side.

```question
id: a-sheet-we-do-not-know-1
type: fill-in-the-blank

For A4, r is 297 ÷ 210, which is about
{1.414|297|210}.
```

Now fold the sheet in half, as before. The long side is cut in two. The short side does not change.

```question
id: a-sheet-we-do-not-know-2
type: fill-in-the-blank

The half sheet is 1 by
{r/2|2 × r|1/2}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try it with A4 first. Its sides are 210 and 297.
2. Folding cuts the 297 in two. The 210 stays.
3. Now do the same with 1 and r. Which one is cut in two?

**Think about:** folding in half halves one side only.

**Try this next:** what are the sides of the half sheet if you fold it
again?

</details>

## Which side is long now?

For A4, r is about 1.4. So r/2 is about 0.7.

```question
id: which-side-is-long-now-1
type: multiple-choice
answer: 1

Which side of the half sheet is the long side now?

- 1
  - r/2 is about 0.7, and 1 is more than 0.7.
- r/2
  - r was the long side before the fold. But the fold cut it in two.
- r
  - No side of the half sheet is r long. The fold cut r in two.
```

So the shape test for the half sheet divides 1 by r/2:

$$1 \div \frac{r}{2} = \frac{2}{r}$$

Dividing by a fraction is the same as multiplying by the fraction
turned over. We met this in *Dividing fractions: how many fit?*

## The same shape again

A5 is the same shape as A4. So the half sheet gives the same answer to
the shape test as the whole sheet:

$$r = \frac{2}{r}$$

Now multiply both sides by r. The r on the bottom cancels.

```question
id: the-same-shape-again-1
type: fill-in-the-blank

r × r =
{2|1|4}.

So r is
{side(2)|2|side(4)}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. On the left, r × r is r × r.
2. On the right, (2/r) × r. The r on the top and the r on the bottom
   make r/r, which is 1.
3. So what is left on the right?

**Think about:** side(2) is the number that, times itself, makes 2.

**Try this next:** what if folding a sheet in three gave the same
shape? What would r × r be then?

</details>

So a sheet that keeps its shape when you fold it in half has a long
side of side(2) short sides. That is why A-series paper has side(2) in
it.

The usual way to write side(2) is $\sqrt{2}$. Python finds it as
`2 ** 0.5`. Here it is beside A4.

```python exec
id: the-same-shape-again-2
print(297 / 210)
print(2 ** 0.5)
```

The two numbers agree as far as 1.4142. After that they differ,
because the sizes are rounded to whole millimetres.

## One square metre

The biggest sheet in the family is A0. It is 841 mm by 1189 mm. A
square metre is a square 1000 mm by 1000 mm, so it is 1,000,000 square
millimetres.

```question
id: one-square-metre-1
type: fill-in-the-blank

841 × 1189 is 999,949. So A0 is
{very close to|much less than|much more than}
one square metre.
```

A0 folded in half is A1. A1 folded in half is A2, then A3, then A4.

```question
id: one-square-metre-2
type: fill-in-the-blank

From A0 to A4 is
{4|16|2}
folds.

So one A0 sheet makes
{16|8|4}
A4 sheets.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the folds on your fingers: A0 to A1, A1 to A2, A2 to A3, A3
   to A4.
2. Each fold doubles the number of pieces: 1, 2, 4, …
3. This is the folded paper from *Powers: the long way and the short
   way*.

**Think about:** folds(16) from *Counting hops: logarithms, how many
times did we multiply?*

**Try this next:** how many A6 sheets does one A0 sheet make?

</details>

So an A4 sheet is one sixteenth of a square metre.

{{include: setup/zen-calm-check.md}}

## A very big prime

A *prime number* is a whole number bigger than 1 that only 1 and
itself divide exactly. 2, 3, 5, 7 and 11 are prime. 9 is not prime,
because 3 × 3 = 9.

On 12 October 2024, Luke Durant found the largest prime number known
today, through GIMPS, a project where many computers search for primes
together. Here is the number:

$$2^{136\,279\,841} - 1$$

It is 136,279,841 twos multiplied together, and then 1 less.
Nobody can count its digits by hand. But hops can.

```question
id: a-very-big-prime-1
type: multiple-choice
answer: 2

Make a guess. How many digits do you think it has?

- About 136 million
  - 136,279,841 is the exponent. It counts the hops of ×2, not the
    digits.
- About 41 million
  - Each hop of ×2 adds less than one digit. So there are fewer digits
    than hops.
- About 136 thousand
  - That is 136,279,841 with the last three digits dropped. Is there a
    reason to drop them?
```

We will find the answer in small steps. Start small.

## Ten hops of two

On *Counting hops: logarithms, how many times did we multiply?*, the
number of digits was close to hops(10 → the number) + 1.

$2^{10}$ is 1024. That is ten hops of ×2. Three hops of ×10 land on
1000.

```question
id: ten-hops-of-two-1
type: fill-in-the-blank

1024 is very close to 1000. So ten hops of ×2 are about
{3|10|30}
hops of ×10.

So one hop of ×2 is about
{0.3|3|10}
hops of ×10.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Ten hops of ×2 land near 1000.
2. How many hops of ×10 land on 1000?
3. Divide the hops of ×10 by the ten hops of ×2.

**Think about:** a hop of ×2 is a smaller hop than a hop of ×10.

**Try this next:** about how many hops of ×10 are twenty hops of ×2?

</details>

More exactly, hops(10 → 2) is about 0.30103. So each hop of ×2 moves
us about 0.30103 of a hop of ×10.

Here is a second way to see it. hops(2 → 10) is between 3 and 4,
because $2^3 = 8$ and $2^4 = 16$. It is about 3.32. And 1 ÷ 3.32 is
about 0.301.

## Counting the digits

$2^{100}$ is 100 hops of ×2. That is about 100 × 0.30103 = 30.103 hops
of ×10. So it should have 31 digits.

Python can count them. `str` turns a number into text, and `len`
counts the characters in the text.

```python exec
id: counting-the-digits-1
print(len(str(2 ** 10)))
print(len(str(2 ** 20)))
print(len(str(2 ** 100)))
```

```predict
type: number

Before you run it: what will the last line print? How many digits does
2 ** 100 have?
```

The cell prints 4, 7 and 31. Here they are beside the hops:

| Number | Hops of ×10, about | Digits |
|---|---|---|
| $2^{10}$ | 10 × 0.30103 = 3.0103 | 4 |
| $2^{20}$ | 20 × 0.30103 = 6.0206 | 7 |
| $2^{100}$ | 100 × 0.30103 = 30.103 | 31 |

Each time, the digits are the whole part of the hops, plus one. The
*whole part* is the number before the point.

## Any number of hops

Choose numbers, shapes or letters in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: any-number-of-hops-1--numbers
type: fill-in-the-blank

$2^{200}$ is about
{60.206|200|20}
hops of ×10.

So $2^{200}$ has
{61|60|201}
digits.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: any-number-of-hops-1--squiggles
type: fill-in-the-blank

$2^{\heartsuit}$ is ♡ hops of ×2. That is about
{♡ × 0.30103|♡ + 0.30103|♡ ÷ 0.30103}
hops of ×10.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: any-number-of-hops-1--letters
type: fill-in-the-blank

$2^{n}$ is n hops of ×2. That is about
{n × 0.30103|n + 0.30103|n ÷ 0.30103}
hops of ×10.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Each hop of ×2 is about 0.30103 of a hop of ×10.
2. Count the hops of ×2. It is the exponent.
3. Multiply the two numbers.

**Think about:** the heart could be any number at all, and the pattern
still holds. That is all a letter in algebra means.

**Try this next:** about how many digits does $2^{1000}$ have?

</details>

## The prime's digits

Now the big one. $2^{136\,279\,841}$ is 136,279,841 hops of ×2. Here
it is with 0.30103, and with Python's own value of hops(10 → 2).

The usual way to write hops(10 → 2) is $\log_{10} 2$. Python finds it
as `math.log10(2)`. The first line, `import math`, gets Python's box of
maths tools ready.

```python exec
id: the-primes-digits-1
import math

print(136279841 * 0.30103)
print(math.log10(2))
print(136279841 * math.log10(2))
```

```predict
type: choice

Before you run it: will the first and the last lines have the same
whole part?

- Yes, the same whole part
  - 0.30103 is very close to hops(10 → 2), so the answers should be
    close.
- No, they will differ by a little
  - 0.30103 is rounded. The tiny difference is multiplied by 136
    million.
- No, they will be very different
  - The two hops numbers are almost the same. Can a tiny difference
    make a big one?
```

The first line is about 41,024,320.5, and the last is about
41,024,319.9. They
differ by about 0.6. 0.30103 is rounded, and Python's value is
0.30102999566… The tiny difference, multiplied by 136 million,
becomes big enough to change the whole part.

So we use Python's value. `int` keeps the whole part of a number.

```python exec
id: the-primes-digits-2
print(int(136279841 * math.log10(2)) + 1)
```

It prints 41024320. So $2^{136\,279\,841}$ has 41,024,320 digits.

## One less

The prime is $2^{136\,279\,841} - 1$. Does taking 1 away change the
number of digits?

1000 − 1 is 999, which has one digit fewer. But 1024 − 1 is 1023, with
the same number of digits. A number loses a digit only when it is 1
followed by zeros.

```question
id: one-less-1
type: fill-in-the-blank

The powers of 2 are 2, 4, 8, 16, 32, 64, 128, 256. Their last digits
are 2, 4, 8, 6, 2, 4, 8, 6. The next last digit is
{2|0|6}.

So a power of 2 ends in 0
{never|sometimes|always}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The next power is 256 × 2 = 512. What is its last digit?
2. Only the last digit decides the next last digit. 6 × 2 is 12, which
   ends in 2.
3. Does the pattern 2, 4, 8, 6 ever reach 0?

**Think about:** which number times 2 ends in 0? Is it in the pattern?

**Try this next:** what are the last digits of the powers of 3?

</details>

A power of 2 never ends in 0, so it is never 1 followed by zeros.
Taking 1 away does not change its number of digits. The largest known
prime has 41,024,320 digits, as Wikipedia says. We found it with hops,
without writing a single digit.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say the two ideas of this page in your
own words. Why does A4 keep its shape when you fold it? How do you
count the digits of $2^n$? Write it in the Notes panel or on paper, or
say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A sheet keeps its shape when you fold it in half only if its long side
is side(2) times its short side, because then r = 2/r, so r × r = 2.
Each hop of ×2 is about 0.30103 hops of ×10. So $2^n$ is about
n × 0.30103 hops of ×10, and its digits are the whole part of that,
plus one. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five problems of your own, and find each answer? Here are
some ideas:

- the shape test for A1 (594 × 841 mm) or A2 (420 × 594 mm)
- how many A5 sheets one A0 sheet makes
- the digits of $2^{50}$, with hops, then with `len(str(2 ** 50))`
- the digits of $10^{\heartsuit}$, for a shape of your choice
- a power of 5: does it ever end in 0?

Which one surprised you most?

## Looking back

On this page, side(2) came from folding paper, and hops counted digits
that nobody could write. Which one surprised you more, and why?

A challenge: hops can also find the first digits of a big number. The
program below takes the part of the hops after the point, and turns it
into a number. For the prime it prints 8.8169… Wikipedia shows the
first digits of the prime: 881694… Can you change it to find the first
digits of $2^{100}$? Check them with `print(2 ** 100)`.

```python challenge
# The first digits of 2 ** 136279841, found with hops.
import math

hops_of_ten = 136279841 * math.log10(2)
after_the_point = hops_of_ten - int(hops_of_ten)
print(10 ** after_the_point)
```

## Read more

Wikipedia's page on [paper sizes](https://en.wikipedia.org/wiki/Paper_size)
has the whole A-series, and the reason for side(2), with the usual
signs. Its page on the [largest known prime
number](https://en.wikipedia.org/wiki/Largest_known_prime_number) shows
the first and last digits of the prime. GIMPS told the world about it
in a [short news page](https://www.mersenne.org/primes/?press=M136279841).
The pages this one builds on are [Sides that never end: surds, the
square root of 2](tutorial:sides-that-never-end) and [Counting hops:
logarithms, how many times did we multiply?](tutorial:how-many-hops).
