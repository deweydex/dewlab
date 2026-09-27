---
title: "Counting hops: logarithms, how many times did we multiply?"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Counting hops: logarithms, how many times did we multiply?

Here is a line with the numbers 1, 10, 100 and 1,000 on it. Each curve
is a *hop*{.term}. A hop multiplies by 10. Look at the picture before you
answer.

<img src="hops-of-ten.svg" alt="A number line with stops at 1, 10, 100 and 1,000. Above the line, three arcs, each labelled ×10, hop from 1 to 10, from 10 to 100 and from 100 to 1,000.">

```question
id: hops-of-ten-1
type: multiple-choice
answer: 1

How many hops of ×10 go from 1 to 1,000?

- 3
  - There are three curves: 1 to 10, 10 to 100, and 100 to 1,000.
- 4
  - There are four stops on the line. The hops are the curves between
    the stops.
- 1,000
  - 1,000 is where the hops land. The question asks how many hops.
```

## Counting the zeros

Each hop of ×10 puts one more zero on the end of the number:

$$1 \xrightarrow{\times 10} 10 \xrightarrow{\times 10} 100 \xrightarrow{\times 10} 1000$$

So 1,000 has three zeros, and it takes three hops.

```question
id: counting-the-zeros-1
type: fill-in-the-blank

100,000 has
{5|4|6}
zeros.

So it takes
{5|4|100,000}
hops of ×10 to go from 1 to 100,000.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the zeros in 100,000 with your finger. The comma is not a
   zero.
2. Start at 1. Hop ×10, and write down where you land.
3. Hop again and again, and count the hops, until you land on 100,000.

**Think about:** what one hop of ×10 does to the end of a number.

**Try this next:** how many hops go from 1 to 10?

</details>

## A name for counting hops

Counting hops needs a name. We will write it like this:

$$\text{hops}(10 \to 1000) = 3$$

We read it as "hops of 10 to 1000 is 3". Start at 1, hop ×10 each
time, and count the hops until you land on 1000. That count is
hops(10 → 1000). The first number
says what each hop multiplies by. The arrow points at where we want to
land.

```question
id: a-name-for-counting-hops-1
type: fill-in-the-blank

hops(10 → 100) is
{2|10|100}.

hops(10 → 10,000) is
{4|5|1000}.

hops(10 → 10) is
{1|0|10}.
```

A power and hops are the same fact, seen from two sides. $10^3 = 1000$
says: three hops of ×10, where do we land? hops(10 → 1000) = 3 says: we
landed on 1000, so how many hops did we take?

## Hops of two

Now each hop multiplies by 2.

<img src="hops-of-two.svg" alt="A number line with stops at 1, 2, 4, 8 and 16. Above the line, four arcs, each labelled ×2, hop from each stop to the next.">

```question
id: hops-of-two-1
type: multiple-choice
answer: 1

What is hops(2 → 16)?

- 4
  - Four curves: 1 to 2, 2 to 4, 4 to 8, and 8 to 16.
- 8
  - 16 ÷ 2 is 8. That is one hop backwards from 16, not a count of
    the hops.
- 5
  - There are five stops on the line. The hops are the curves between
    them.
```

You have seen this line before, in
[Powers: the long way and the short way](tutorial:the-long-way). Each
fold of a sheet of paper doubles the pieces: 1, 2, 4, 8, 16. So the
number of folds is the number of hops of ×2. We will call it *folds*:

$$\text{folds}(16) = \text{hops}(2 \to 16) = 4$$

```question
id: hops-of-two-2
type: fill-in-the-blank

folds(32) is
{5|16|6}.

folds(64) is
{6|32|8}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start at 1, and double: 2, 4, 8, 16, …
2. Count each doubling as one fold.
3. Stop when you land on 32.

**Think about:** folds(32) is one more than folds(16). Why?

**Try this next:** folds(1024).

</details>

{{include: setup/zen-calm-check.md}}

## Hops of any size

A hop can multiply by any number. Choose numbers, shapes or letters in
the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: hops-of-any-size-1--numbers
type: fill-in-the-blank

1 → 3 → 9 → 27. So hops(3 → 27) is
{3|9|27}.

5³ is 125. So hops(5 → 125) is
{3|5|25}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: hops-of-any-size-1--squiggles
type: fill-in-the-blank

♡³ is ♡ × ♡ × ♡. So hops(♡ → ♡³) is
{3|♡|1}.

hops(★ → ★⁷) is
{7|★|14}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: hops-of-any-size-1--letters
type: fill-in-the-blank

b³ is b × b × b. So hops(b → b³) is
{3|b|1}.

hops(n → n⁷) is
{7|n|14}.
```

</div>

The heart could be any number at all, and the pattern stays the same.
That is all a letter in algebra means. hops counts the multiplying.
The exponent counts it too. So hops of a power is its exponent.

## A counting machine

Python can count hops for us. Python is a language for computers. This
program starts at 1. Then it multiplies by the base and counts, until
it reaches the target. The *base*{.term} is the number each hop multiplies
by, and the *target* is where we want to land.

```python exec
id: a-counting-machine-1
def hops(base, target):
    position = 1
    count = 0
    while position < target:
        position = position * base
        count = count + 1
    return count

print(hops(10, 1000))
print(hops(2, 16))
print(hops(2, 1024))
```

```predict
type: number

Before you run it: what will the last line print? How many hops of ×2
go from 1 to 1024?
```

The first two lines print 3 and 4, as the pictures showed. The last
line prints 10, because $2^{10}$ is 1024. Ten hops of ×2 land on
1024. Change the numbers and run it again. Try
hops(3, 81).

## A hop that does not land

Where does 5000 sit on the line of ×10 hops?

$$1000 \xrightarrow{\times 10} 10000$$

5000 is after 1000, and before 10,000. No hop of ×10 lands on it.

```question
id: a-hop-that-does-not-land-1
type: multiple-choice
answer: 1

What can we say about hops(10 → 5000)?

- It is between 3 and 4
  - Three hops land on 1000. Four hops land on 10,000. 5000 is in
    between.
- It is 500
  - 5000 ÷ 10 is 500. That is one hop backwards, not a count of hops.
- It is exactly 4
  - Four hops land on 10,000. That is past 5000.
```

```python exec
id: a-hop-that-does-not-land-2
print(hops(10, 5000))
```

```predict
type: choice

Before you run it: what will the counting machine print for
hops(10, 5000)?

- 4
- 3
  - Three hops land on 1000. The machine is still below 5000 there.
- Something between 3 and 4
  - hops(10 → 5000) is between 3 and 4, so the machine could say so.
```

The machine prints 4. It counts whole hops, and it stops after it
passes 5000. It cannot land on 5000, so it hops past it to 10,000.

A stretch, if you want one: is hops(10 → 5000) nearer to 3, or nearer
to 4?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. From [Halfway powers: fractional exponents, two half steps make one](tutorial:halfway-steps),
   halfway(10) is about 3.16. So a half hop multiplies by about 3.16.
2. Three and a half hops land on 1000 × 3.16, which is about 3162.
3. Is 5000 before or after 3162?

**Think about:** what a half hop means, if two of them make one hop of
×10.

**Try this next:** is hops(10 → 2000) more or less than three and a
half?

</details>

## Counting digits

1000 has 4 digits, and hops(10 → 1000) is 3. The number of digits is
one more than the number of hops. Each hop adds a digit, and the 1 at
the start is a digit too.

For a number that does not land on a stop, it works almost the same.
5000 has 4 digits, and hops(10 → 5000) is between 3 and 4.

```question
id: counting-digits-1
type: fill-in-the-blank

12,345 has
{5|4|6}
digits.

So hops(10 → 12,345) is between
{4 and 5|5 and 6|3 and 4}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the digits of 12,345. The comma is not a digit.
2. Which stops is it between: 1000, 10,000 or 100,000?
3. How many hops land on each of those stops?

**Think about:** every number from 10,000 to 99,999 has 5 digits.

**Try this next:** how many digits does a number have if its hops
are between 8 and 9?

</details>

## The usual way to write it

The usual way to write hops(10 → 1000) is

$$\log_{10} 1000 = 3$$

We read it as "log to base 10 of 1000". *Log* is short for
*logarithm*. A logarithm counts hops. The small 10 is the base, the
number each hop multiplies by. It means exactly the same as
hops(10 → 1000). In the same way, folds(16) is $\log_2 16 = 4$.

Python has these too. The first line, `import math`, gets Python's
box of maths tools ready.

```python exec
id: the-usual-way-to-write-it-1
import math

print(math.log10(1000))
print(math.log2(16))
print(math.log10(5000))
```

It prints `3.0` and `4.0`. The `.0` means Python found them as
decimals. For 5000 it prints `3.6989700043360187`. That is between 3
and 4, and nearer to 4, as the hop line showed.

You can keep writing hops when it feels calmer. hops(10 → 1000) and
$\log_{10} 1000$ are two names for one number, 3.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say what hops(10 → ♡) means in your own
words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

hops(10 → ♡) counts how many times we multiply by 10, starting at 1,
to land on ♡. It is the exponent in $10^{?} = \heartsuit$. When ♡ is a
whole number, the number of digits in ♡ is close to
hops(10 → ♡) + 1. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five hops problems of your own? Try one with hops of ×10,
one with folds, and one with a shape, like hops(△ → △⁹). Try one that
does not land on a stop. Which one surprises you most?

## Looking back

Why does counting the zeros of 1000 give the same answer as counting
hops?

A challenge: the counting machine below always prints a whole number.
For 5000 it prints 4, because it hops past 5000. Can you change it, so
that it prints "between 3 and 4" when the last hop passes the target?

```python challenge
# Count hops of the base, starting at 1, until we reach the target.
def hops(base, target):
    position = 1
    count = 0
    while position < target:
        position = position * base
        count = count + 1
    return count

print(hops(10, 5000))
```

## Read more

The Simple English Wikipedia has a short page on
[logarithms](https://simple.wikipedia.org/wiki/Logarithm). It uses the
usual signs, and the ideas are the ones on this page. The longer
English page on the
[common logarithm](https://en.wikipedia.org/wiki/Common_logarithm)
says more about hops of 10, and their history.
