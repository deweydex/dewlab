---
title: "Counting hops: how many times did we multiply? — Practice"
practice_for: how-many-hops
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Ordinary numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Counting hops: how many times did we multiply? — Practice

Small problems on one idea. hops(10 → ♡) counts how many hops of ×10
go from 1 to ♡. Try each problem before you open anything under it.
Choose numbers, shapes or letters in the box under the title.

<img src="hops-of-ten.svg" alt="A number line with stops at 1, 10, 100 and 1,000. Above the line, three arcs, each labelled ×10, hop from 1 to 10, from 10 to 100 and from 100 to 1,000.">

## 1. Same or different?

```question
id: same-or-different-1
type: multiple-choice
answer: 2

Here are three counts for 1000: hops(10 → 1000), the number of zeros
in 1000, and the number of digits in 1000. Which two are the same?

- The zeros and the digits
  - 1000 has 3 zeros. It has 4 digits, because the 1 is a digit too.
- hops(10 → 1000) and the zeros
  - Each hop of ×10 puts one zero on the end. Three hops, three zeros.
- hops(10 → 1000) and the digits
  - Three hops land on 1000. But 1000 has 4 digits.
```

## 2. A million

```question
id: a-million-1
type: fill-in-the-blank

1,000,000 has
{6|7|3}
zeros.

So hops(10 → 1,000,000) is
{6|7|100,000}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the zeros in 1,000,000. The commas are not zeros.
2. Each hop of ×10 puts one zero on the end.
3. How many hops put that many zeros on the end of 1?

**Think about:** a million is $10^6$. What does the 6 count?

**Try this next:** hops(10 → a billion). A billion is 1,000,000,000.

</details>

## 3. Hops of three

<div class="dl-world" data-world="numbers">

```question
id: hops-of-three-1--numbers
type: fill-in-the-blank

1 → 3 → 9 → 27 → 81. So hops(3 → 81) is
{4|27|5}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: hops-of-three-1--squiggles
type: fill-in-the-blank

△⁴ is △ × △ × △ × △. So hops(△ → △⁴) is
{4|△|16}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: hops-of-three-1--letters
type: fill-in-the-blank

k⁴ is k × k × k × k. So hops(k → k⁴) is
{4|k|16}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start at 1.
2. Multiply by the base, and write down where you land.
3. Count the multiplying, until you land on the target.

**Think about:** 81 ÷ 3 is 27. Why is 27 not the number of hops?

**Try this next:** hops(3 → 243).

</details>

<details class="dl-answer"><summary>one way through it</summary>

1 × 3 is 3. 3 × 3 is 9. 9 × 3 is 27. 27 × 3 is 81. That is four
hops, so hops(3 → 81) is 4. It is the same fact as $3^4 = 81$.

</details>

## 4. Continue the pattern

<div class="dl-world" data-world="numbers">

hops(2 → 8) is 3. hops(2 → 4) is 2. hops(2 → 2) is 1.

```question
id: continue-the-pattern-1--numbers
type: fill-in-the-blank

The next one is hops(2 → 1), which is
{0|1|−1}.
```

</div>

<div class="dl-world" data-world="squiggles">

hops(♡ → ♡³) is 3. hops(♡ → ♡²) is 2. hops(♡ → ♡) is 1.

```question
id: continue-the-pattern-1--squiggles
type: fill-in-the-blank

The next one is hops(♡ → 1), which is
{0|1|♡}.
```

</div>

<div class="dl-world" data-world="letters">

hops(b → b³) is 3. hops(b → b²) is 2. hops(b → b) is 1.

```question
id: continue-the-pattern-1--letters
type: fill-in-the-blank

The next one is hops(b → 1), which is
{0|1|b}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Every count of hops starts at 1.
2. If the target is 1, where are we already?
3. How many hops do we need to take?

**Think about:** the numbers in the pattern go down by one each time.

**Try this next:** what could hops(2 → 1/2) be? This is a stretch.

</details>

## 5. Any shape

This one is for any number at all. The shape or letter can be any
number, and the count is the same.

<div class="dl-world" data-world="numbers">

```question
id: any-shape-1--numbers
type: fill-in-the-blank

7⁵ is 16,807. So hops(7 → 16,807) is
{5|7|35}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: any-shape-1--squiggles
type: fill-in-the-blank

hops(♡ → ♡⁵) is
{5|♡|5 × ♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: any-shape-1--letters
type: fill-in-the-blank

hops(n → n⁵) is
{5|n|5n}.
```

</div>

<details class="dl-answer"><summary>one way through it</summary>

$\heartsuit^5$ is five hearts multiplied: five hops of $\times\heartsuit$
from 1. So hops($\heartsuit \to \heartsuit^5$) is 5, whatever the heart
is. With numbers, $7^5 = 16807$, so hops(7 → 16,807) is 5 too.

</details>

## 6. Counting digits

The number of digits is one more than the hops of ×10, when a number
lands on a stop. For other numbers, it is close.

```question
id: counting-digits-1
type: fill-in-the-blank

5000 has
{4|3|5}
digits.

999,999 has
{6|5|7}
digits.

So hops(10 → 999,999) is between
{5 and 6|6 and 7|4 and 5}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the digits. The commas are not digits.
2. 999,999 is one less than 1,000,000. How many hops land on
   1,000,000?
3. So 999,999 comes a little before that stop. Which stop is before
   it?

**Think about:** 999,999 is very close to a stop, but it does not
land on it.

**Try this next:** how many digits does 10 × 999,999 have?

</details>

## 7. What is between?

These hops do not land on a stop. Which two whole numbers is each one
between?

```question
id: what-is-between-1
type: fill-in-the-blank

hops(10 → 50) is between
{1 and 2|4 and 5|5 and 50}.

hops(2 → 20) is between
{4 and 5|10 and 11|2 and 3}.

hops(10 → 5000) is between
{3 and 4|4 and 5|500 and 5000}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the stops: for ×2, they are 1, 2, 4, 8, 16, 32, …
2. Find the two stops the target sits between.
3. Count the hops to each of those two stops.

**Think about:** 20 is after 16 and before 32.

**Try this next:** hops(2 → 100).

</details>

## 8. Match three ways

<div class="dl-world" data-world="numbers">

```question
id: match-three-ways-1--numbers
type: multiple-choice
answer: 1

Which of these says the same thing as hops(2 → 32) = 5?

- $2^5 = 32$
  - Five hops of ×2, starting at 1, land on 32.
- $32 \div 2 = 16$
  - That is one hop backwards from 32.
- $5 \times 2 = 10$
  - That adds five 2s. Hops multiply.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: match-three-ways-1--squiggles
type: multiple-choice
answer: 1

Which of these says the same thing as hops(♡ → ♡³) = 3?

- $\heartsuit \times \heartsuit \times \heartsuit = \heartsuit^3$
  - Three hops of ×♡, starting at 1, land on $\heartsuit^3$.
- $\heartsuit + \heartsuit + \heartsuit = 3 \times \heartsuit$
  - That adds three hearts. Hops multiply.
- $\heartsuit^3 \div \heartsuit = \heartsuit^2$
  - That is one hop backwards from $\heartsuit^3$.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: match-three-ways-1--letters
type: multiple-choice
answer: 1

Which of these says the same thing as hops(b → b³) = 3?

- $b \times b \times b = b^3$
  - Three hops of ×b, starting at 1, land on $b^3$.
- $b + b + b = 3b$
  - That adds three bs. Hops multiply.
- $b^3 \div b = b^2$
  - That is one hop backwards from $b^3$.
```

</div>

A third way to say it is the folded paper from *Powers: the long way
and the short way*. folds(32) is 5: five folds make 32 pieces.

## 9. What went differently here?

Here is a worked problem, with one step that went differently.

> hops(2 → 16). 16 ÷ 2 is 8. So hops(2 → 16) is 8.

What went differently? Check it by hopping: where do 8 hops of ×2
land, starting at 1?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start at 1, and double 8 times. Write each number down.
2. Where do you land? Is it 16?
3. Now count the hops that land on 16.

**Think about:** what "16 ÷ 2" finds. Is it a count, or a place on the
line?

**Try this next:** hops(2 → 64), by hopping.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Eight hops of ×2 land on 256, not 16. The worked problem divided once,
and found the stop before 16. That is 8. But hops counts the hops from
1: 1, 2, 4, 8, 16. That is 4 hops, so hops(2 → 16) is 4.

</details>

## 10. A counting machine

Here is the counting machine from the page. It starts at 1, multiplies
by the base, and counts until it reaches the target. Use it to check
any problem above.

```python exec
id: a-counting-machine-1
def hops(base, target):
    position = 1
    count = 0
    while position < target:
        position = position * base
        count = count + 1
    return count

print(hops(3, 81))
print(hops(10, 1000000))
```

It prints 4 and 6. Remember that it counts whole hops. For a target
that is not on a stop, it hops past it, and prints the next whole
number.

## 11. A stretch: a very big number

From *Powers: the long way and the short way*: $2^{100}$ is a very big
number. How many digits does it have? Here is a first step. $2^{10}$
is 1024, which is close to 1000.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $2^{10}$ is about $10^3$. Ten hops of ×2 are about three hops of
   ×10.
2. $2^{100}$ is ten copies of $2^{10}$, multiplied together.
3. So how many hops of ×10 is it, about? And how many digits?

**Think about:** each hop of ×10 adds one digit.

**Try this next:** about how many digits does $2^{20}$ have?

</details>

Python can count the digits for you. `str` turns a number into text,
and `len` counts the characters in the text.

```python exec
id: a-stretch-a-very-big-number-1
print(len(str(2 ** 100)))
```

<details class="dl-answer"><summary>one way through it</summary>

$2^{100}$ is $(2^{10})^{10}$, which is about $1000^{10}$. That is about
$10^{30}$, so hops(10 → $2^{100}$) is about 30. The number of digits
is one more: 31. The cell prints 31.

</details>

## 12. From earlier: the golden beads

From *Powers: the long way and the short way*. The golden bead cube is
$10^3 = 1000$ beads. What is hops(10 → 1000)? And what does the
exponent 3 count on the cube?

<details class="dl-answer"><summary>answer</summary>

hops(10 → 1000) is 3. On the cube, the 3 counts the directions: 10
wide, 10 high and 10 deep. Each direction is one hop of ×10.

</details>

## 13. From earlier: halfway hops

From *Halfway powers: two half steps make one*. halfway(10,000) is
100, because 100 × 100 is 10,000. What is hops(10 → 10,000)? And what
is hops(10 → 100)? What do you notice?

<details class="dl-answer"><summary>answer</summary>

hops(10 → 10,000) is 4, and hops(10 → 100) is 2. Taking halfway cut
the hops in half: 4 hops became 2.

</details>

## 14. Five of your own

Can you make five hops problems of your own? Here are some ideas:

- hops of ×10 to a very big number
- folds of a number of pieces
- a hop that does not land on a stop
- a shape, like hops(△ → △¹²)
- hops of a number to itself

Which one was the hardest to make?
