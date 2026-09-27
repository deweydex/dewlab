---
title: "Halfway powers: two half steps make one"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Ordinary numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Halfway powers: two half steps make one

Here is a line with the numbers 1, 2, 4, 8 and 16 on it. Each curve is
a *hop*. A hop multiplies. Above the line, two big hops each
multiply by 4. Below the line, there are smaller hops. Look at the
small hops before you answer.

<img src="halfway-hops.svg" alt="A number line with stops at 1, 2, 4, 8 and 16. Above the line, two big arcs labelled ×4 hop from 1 to 4 and from 4 to 16. Below the line, four smaller arcs labelled ×2 hop from 1 to 2, 2 to 4, 4 to 8 and 8 to 16.">

```question
id: halfway-hops-1
type: multiple-choice
answer: 1

Two small hops go from 1 to 4. What does each small hop do?

- It multiplies by 2
  - 1 × 2 is 2, and 2 × 2 is 4. The stop in the middle is 2.
- It multiplies by 3
  - 1 × 3 is 3. But the stop in the middle of the big hop is 2, not
    3.
- It adds 1.5
  - Adding 1.5 twice goes from 1 to 4. But then the middle stop would
    be 2.5.
```

## Two small hops make one big hop

Each small hop multiplies by 2. Two small hops multiply by 2, and then
by 2 again:

$$2 \times 2 = 4$$

So two small hops of ×2 make one big hop of ×4. Now look at the
second big hop, from 4 to 16.

```question
id: two-small-hops-1
type: fill-in-the-blank

The big hop from 4 to 16 multiplies by
{4|12|16}.

The first small hop under it goes from 4 to
{8|6|10}.
```

## Hops of three

Here is a new line. Each small hop multiplies by 3:

$$1 \xrightarrow{\times 3} 3 \xrightarrow{\times 3} 9$$

```question
id: hops-of-three-1
type: fill-in-the-blank

Two small hops of ×3 make one big hop of
{×9|×6|×3}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start at 1. One hop of ×3 lands on 3.
2. A second hop of ×3 lands on 3 × 3.
3. One big hop goes from 1 to the same place. What does it multiply
   by?

**Think about:** a hop multiplies. It does not add.

**Try this next:** two hops of ×5, starting at 1. Where do they land?

</details>

Two hops of ×3 make ×9, not ×6. With hops of ×2, we could not see
the difference, because 2 + 2 and 2 × 2 are both 4. With 3, the
difference shows.

## Going backwards

Now we start with a big hop, and look for the small one. One big hop
multiplies by 25. Two equal small hops land in the same place.

```question
id: going-backwards-1
type: multiple-choice
answer: 1

Which small hop, done twice, makes one big hop of ×25?

- ×5
  - 5 × 5 is 25.
- ×12.5
  - 12.5 is half of 25. But two hops multiply: 12.5 × 12.5 is 156.25.
- ×10
  - Two hops of ×10 go from 1 to 100.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Two equal small hops multiply by the same number twice.
2. So we need a number that, times itself, gives 25.
3. Try 2 × 2, then 3 × 3, then 4 × 4, and so on.

**Think about:** why half of 25 is much too big.

**Try this next:** which small hop, done twice, makes ×49?

</details>

## A question from a worksheet

A Grade 8 worksheet asks this question:

$$10^{1/2} \times 10^{1/2}$$

The exponent is a fraction. That can look scary. But we already have a
rule that can answer it.

The rule comes from the page *Multiplying powers: joining two stacks*.
When we multiply two powers of the same number, we add the exponents.
Here is an example:

$$10^2 \times 10^3 = 10^{2 + 3} = 10^5$$

Two tens, times three tens, is five tens in total. The rule does not
care what the exponents are. So let's use it on the worksheet's
question.

```question
id: a-question-from-a-worksheet-1
type: fill-in-the-blank

The two exponents are one half and one half. Added together, they make
{1|1/4|2/4}.

So the answer to the worksheet's question is 10¹, which is
{10|5|100}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the two exponents, the small raised numbers. Both are
   $\frac{1}{2}$.
2. Two halves of a pizza make one whole pizza. So
   $\frac{1}{2} + \frac{1}{2} = 1$.
3. The rule says to add the exponents. So the answer is $10^1$.

**Think about:** what $10^1$ means, the long way. It is one 10.

**Try this next:** what is $10^{1/2} \times 10^{1/2} \times 10^{1/2} \times 10^{1/2}$?

</details>

So $10^{1/2}$ is a number that, times itself, gives 10. It is a small
hop. Two of them make one big hop of ×10. The half in the exponent
means half of the multiplying.

```question
id: a-question-from-a-worksheet-2
type: multiple-choice
answer: 2

Which number is closest to $10^{1/2}$?

- 5
  - 5 is half of 10. But 5 × 5 is 25, which is much more than 10.
- A little more than 3
  - 3 × 3 is 9, which is a little less than 10. So the number is a
    little more than 3.
- 100
  - 100 is 10 × 10. That is two big hops, not two small ones.
```

## A name for the small hop

The small hop needs a name. We will call it *halfway*.

halfway(♡) is the number that, done twice, gives ♡. Done twice means
multiplied by itself. So:

- halfway(4) = 2, because 2 × 2 = 4.
- halfway(9) = 3, because 3 × 3 = 9.
- halfway(16) = 4, because 4 × 4 = 16.

You may have read the page *Undoing a square: the side of a square*. It
found the side of a square of beads. A square of 9 beads has a side of
3. So side(9) is 3, and halfway(9) is 3 too. The side of a square
and the halfway hop are the same number. halfway(♡) is side(♡)
again.

```question
id: a-name-for-the-small-hop-1
type: fill-in-the-blank

halfway(36) is
{6|18|12}.

halfway(100) is
{10|50|20}.

halfway(49) is
{7|24.5|9}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. halfway(36) asks: which number, times itself, gives 36?
2. It is not half of 36. Half of 36 is 18, and 18 × 18 is much more
   than 36.
3. Try 5 × 5, then 6 × 6.

**Think about:** a square of 36 beads. How many beads are on one side?

**Try this next:** halfway(64).

</details>

{{include: setup/zen-calm-check.md}}

## Two halfway steps

Two halfway steps always make one whole step. The same is true
whatever number is in the brackets. Choose numbers, shapes or letters
in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: two-halfway-steps-1--numbers
type: fill-in-the-blank

halfway(36) × halfway(36) is
{36|18|72}.

halfway(5) × halfway(5) is
{5|2.5|25}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: two-halfway-steps-1--squiggles
type: fill-in-the-blank

halfway(♡) × halfway(♡) is
{♡|♡/2|♡²}.

halfway(△) × halfway(△) is
{△|2 × △|△²}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: two-halfway-steps-1--letters
type: fill-in-the-blank

halfway(n) × halfway(n) is
{n|n/2|n²}.

halfway(k) × halfway(k) is
{k|2k|k²}.
```

</div>

The heart could be any number at all, and the pattern stays the same.
That is all a letter in algebra means. Notice halfway(5) too. It is
not a whole number, but two of it still make 5.

## Thirds

A big hop can also be cut into three equal small hops. Here, three
hops of ×2 make one big hop of ×8:

$$1 \xrightarrow{\times 2} 2 \xrightarrow{\times 2} 4 \xrightarrow{\times 2} 8$$

The adding rule works here too. Three thirds make one whole:

$$8^{1/3} \times 8^{1/3} \times 8^{1/3} = 8^{1/3 + 1/3 + 1/3} = 8^1 = 8$$

So $8^{1/3}$ is the number that, done three times, gives 8. That is 2.
The page *Undoing a square: the side of a square* had a name for
this too: edge(8), the edge
of a cube of 8 beads. A cube of 8 beads is 2 beads wide, 2 high and 2
deep.

```question
id: thirds-1
type: multiple-choice
answer: 1

A cube of 27 beads has an edge of 3 beads. Which small hop, done
three times, makes one big hop of ×27?

- ×3
  - 3 × 3 × 3 is 27. It is edge(27).
- ×9
  - 27 ÷ 3 is 9. But three hops multiply: 9 × 9 × 9 is 729.
- ×5
  - 5 × 5 is 25, close to 27. But this needs three hops, not two.
```

## A checking machine

We can check each of these by multiplying. Python is a language for
computers. In Python, `*` means ×, and `==` asks "is this equal to
that?" Python answers `True` or `False`.

```python exec
id: a-checking-machine-1
print(3 * 3)
print(4 * 4 * 4 == 64)
print(5 * 5 == 20)
```

```predict
type: choice

Before you run it: what will the last line print?

- False
- True
  - 5 × 4 is 20. But this line multiplies 5 by 5.
- 25
  - 5 × 5 is 25. But this line asks a question about it.
```

The first line prints 9, so halfway(9) is 3. The second prints
`True`, so edge(64) is 4. The last line prints `False`, because
5 × 5 is 25, not 20. Change the numbers and run it again. Can you
check halfway(81)?

## Finding halfway by trying

What about halfway(10)? We can find it by trying: 1 × 1, then 2 × 2,
then 3 × 3, and so on. We stop when we reach 10 or pass it. This
program tries for us.

```python exec
id: finding-halfway-by-trying-1
def halfway(number):
    guess = 0
    while guess * guess < number:
        guess = guess + 1
    if guess * guess == number:
        return guess
    # We passed the number without landing on it.
    return "between " + str(guess - 1) + " and " + str(guess)

print(halfway(16))
print(halfway(10))
```

```predict
type: choice

Before you run it: what will it print for halfway(10)?

- 5
  - 5 is half of 10. But halfway is not "half of". 5 × 5 is 25.
- between 3 and 4
- 3
  - 3 × 3 is 9, very close to 10. But it does not land on 10.
```

3 × 3 is 9, a little less than 10. 4 × 4 is 16, which is more than
10. So halfway(10) is between 3 and 4. No whole number works. Try
halfway(2) and halfway(50) too. Which numbers have a whole number for
their halfway?

## The usual way to write it

The usual way to write halfway(♡) is $\heartsuit^{1/2}$. You met
this sign in the worksheet's question. The two mean exactly the same
thing:

$$\text{halfway}(9) = 9^{1/2} = 3$$

The edge of a cube has a usual way too: edge(8) is $8^{1/3}$.

The page *Undoing a square: the side of a square* had one more
sign: $\sqrt{9}$. It is
called the *square root* of 9, and it is side(9). So halfway(9),
side(9), $9^{1/2}$ and $\sqrt{9}$ are four names for one number, 3.
You can keep writing halfway when it feels calmer.

In Python, `**` means a power. So Python writes $9^{1/2}$ as
`9 ** 0.5`, because 0.5 is one half as a decimal. It writes $8^{1/3}$
as `8 ** (1/3)`. The brackets make Python find 1/3 first.

```python exec
id: the-usual-way-to-write-it-1
print(9 ** 0.5)
print(8 ** (1/3))
print(64 ** (1/3))
print(10 ** 0.5 * 10 ** 0.5)
```

The first two lines print `3.0` and `2.0`. The `.0` means Python found
the answer as a decimal. Look at the last two lines. edge(64) is 4,
but Python prints `3.9999999999999996`. And the worksheet's question
is 10, but Python prints `10.000000000000002`.

The computer rounds. Python writes 1/3 as `0.3333333333333333`, and
stops there. So its answer is a tiny bit different from 4. This is why
this page found halfway by trying whole numbers. Whole numbers do not
round.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say what halfway(♡) means in your own
words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

halfway(♡) is the number that, multiplied by itself, gives ♡. It is a
small hop. Two of them make one big hop of ×♡. It is the side of a
square of ♡ beads. We can also write it $\heartsuit^{1/2}$, because
two halves add to one whole. Your way of saying it may be clearer than
ours.

</details>

## Make your own

Can you make five halfway problems of your own? Try one with a whole
number answer, like halfway(81). Try one with no whole number answer,
like halfway(20). Try one with a shape, and one with thirds, like
edge(125). Which one surprises you most?

## Looking back

halfway(16) is 4, not 8. Why does halfway not mean "half of"?

A challenge: the program below finds halfway by trying. Can you make
an edge function in the same way, that tries whole numbers for a cube?
Check it with edge(27), edge(1000) and edge(30).

```python challenge
# halfway(number), found by trying whole numbers.
def halfway(number):
    guess = 0
    while guess * guess < number:
        guess = guess + 1
    if guess * guess == number:
        return guess
    return "between " + str(guess - 1) + " and " + str(guess)

print(halfway(49))
```

## Read more

The Simple English Wikipedia has a short page on the
[square root](https://simple.wikipedia.org/wiki/Square_root). The
longer English page on exponentiation has a section on
[fractions as exponents](https://en.wikipedia.org/wiki/Exponentiation#Rational_exponents).
Both use the usual signs. The ideas are the ones on this page.
