---
title: "Surds and logs in the wild: A4 paper and the largest prime — Practice"
practice_for: surds-and-logs-in-the-wild
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Surds and logs in the wild: A4 paper and the largest prime — Practice

Small problems on two ideas. A sheet that keeps its shape when you fold
it in half has a long side of side(2) short sides. And $2^n$ is about
n × 0.30103 hops of ×10, so its digits are the whole part of that, plus
one. Try each problem before you open anything under it. Choose
numbers, shapes or letters in the box under the title.

<img src="paper-sizes.svg" alt="Four sheets of paper drawn to scale, each in the top left corner of the one before. The biggest, A3, lies on its long side. A4 stands up in its corner and covers the left half of it. A5 lies on its long side in the corner of A4 and covers the top half of A4. A6 stands up in the corner of A5 and covers the left half of A5. Beside the sheets is a list of sizes: A3 is 297 × 420 mm, A4 is 210 × 297 mm, A5 is 148 × 210 mm, and A6 is 105 × 148 mm.">

## 1. Same or different?

```question
id: same-or-different-1
type: multiple-choice
answer: 2

Here are three sheets: A4 (210 × 297 mm), A6 (105 × 148 mm), and a
card 200 × 300 mm. Which two have the same shape?

- A4 and the card
  - The card's sides are close to A4's. But 300 ÷ 200 is 1.5, and
    297 ÷ 210 is about 1.414.
- A4 and A6
  - 297 ÷ 210 is about 1.414, and 148 ÷ 105 is about 1.41. Both are
    close to side(2).
- A6 and the card
  - The card is much bigger than A6. Try the shape test: long side
    divided by short side.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each sheet, divide the long side by the short side.
2. Write the three answers in a row.
3. Which two answers are close?

**Think about:** the size of a sheet does not matter for the shape
test. Only the two sides of one sheet are compared.

**Try this next:** is a square the same shape as A4?

</details>

## 2. Fill the gap

```question
id: fill-the-gap-1
type: fill-in-the-blank

A2 is 420 mm by 594 mm. Fold it in half, so that the fold cuts the long
side in two. Half of 594 is
{297|210|420}.

So the half sheet is 297 mm by 420 mm. That is the size of
{A3|A1|A4}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The fold cuts the long side, 594, in two.
2. The short side, 420, stays the same.
3. Look for 297 and 420 in the list beside the picture.

**Think about:** each fold makes the next size in the family.

**Try this next:** A1 is 594 mm by 841 mm. What is half of 841, to the
nearest millimetre?

</details>

## 3. Continue the pattern

On the page, the last digits of the powers of 2 went 2, 4, 8, 6, and
then again. Here are the powers of 3: 3, 9, 27, 81, 243, 729.

```question
id: continue-the-pattern-1
type: fill-in-the-blank

Their last digits are 3, 9, 7, 1, 3, 9. The next last digit is
{7|1|0}.

So a power of 3 ends in 0
{never|sometimes|always}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The next power is 729 × 3. You only need its last digit.
2. The last digit of 729 is 9. What is the last digit of 9 × 3?
3. Does the pattern 3, 9, 7, 1 ever reach 0?

**Think about:** 10 divides a number that ends in 0 exactly. So 2 and
5 divide it exactly too. A power of 3 is only 3s, multiplied together.

**Try this next:** does $3^{100} - 1$ have the same number of digits
as $3^{100}$?

</details>

## 4. Match three ways

<div class="dl-world" data-world="numbers">

```question
id: match-three-ways-1--numbers
type: multiple-choice
answer: 1

Which of these says the same thing as "side(2) × side(2) = 2"?

- $\sqrt{2} \times \sqrt{2} = 2$
  - √2 is the usual way to write side(2).
- $\sqrt{2} \times 2 = 2$
  - This multiplies side(2) by 2, not by itself.
- $2 \times 2 = 2$
  - 2 × 2 is 4. side(2) is not 2.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: match-three-ways-1--squiggles
type: multiple-choice
answer: 1

Which of these says the same thing as "side(♡) × side(♡) = ♡"?

- $\sqrt{\heartsuit} \times \sqrt{\heartsuit} = \heartsuit$
  - √♡ is the usual way to write side(♡).
- $\sqrt{\heartsuit} \times \heartsuit = \heartsuit$
  - This multiplies side(♡) by ♡, not by itself.
- $\heartsuit \times \heartsuit = \heartsuit$
  - ♡ × ♡ is ♡², a bigger square. side(♡) is its side.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: match-three-ways-1--letters
type: multiple-choice
answer: 1

Which of these says the same thing as "side(b) × side(b) = b"?

- $\sqrt{b} \times \sqrt{b} = b$
  - √b is the usual way to write side(b).
- $\sqrt{b} \times b = b$
  - This multiplies side(b) by b, not by itself.
- $b \times b = b$
  - b × b is b², a bigger square. side(b) is its side.
```

</div>

A third way to say it is a square. A square with side(2) as its side
has an area of 2.

## 5. Closer to 0, a half, or 1?

```question
id: closer-to-1
type: fill-in-the-blank

An A4 sheet is about 1/16 of a square metre. 1/16 is closer to
{0|a half|1}.

9 is almost 10. So hops(10 → 9) is closer to
{1|a half|0}.

3 × 3 is 9, which is almost 10. So two hops of ×3 are almost one hop of
×10. hops(10 → 3) is closer to
{a half|0|1}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For 1/16, think of a pizza cut into 16 slices. One slice is small.
2. For hops(10 → 9), one whole hop of ×10 lands on 10. 9 is nearly
   there.
3. For hops(10 → 3), two hops of ×3 land near 10. So one hop of ×3 is
   about what part of a hop of ×10?

**Think about:** from 1 to 3, and from 3 to 9, are two equal hops.

**Try this next:** is hops(10 → 2) closer to 0, a half, or 1?

</details>

## 6. Where on the line?

Here is the line of ×10 hops: 1, 10, 100, 1000, … Each stop is a power
of ten. $2^{100}$ has 31 digits.

```question
id: where-on-the-line-1
type: fill-in-the-blank

The smallest number with 31 digits is 1 followed by 30 zeros. That is
{10³⁰|10³¹|10¹⁰⁰}.

So $2^{100}$ lands between $10^{30}$ and
{10³¹|10³²|10¹⁰⁰}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 100 has 3 digits, and it is $10^2$. 1000 has 4 digits, and it is
   $10^3$.
2. So a 1 with 30 zeros is 10 to what power?
3. Every number with 31 digits is at least that, and less than the
   next stop.

**Think about:** the number of digits is one more than the power of
the stop before it.

**Try this next:** between which two powers of ten does $2^{20}$
land?

</details>

## 7. Looks scary, is simple

<div class="dl-world" data-world="numbers">

```question
id: looks-scary-1--numbers
type: fill-in-the-blank

$10^6$ is 1,000,000. It has
{7|6|10}
digits.

$10^{1000}$ has
{1001|1000|10}
digits.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: looks-scary-1--squiggles
type: fill-in-the-blank

$10^6$ is 1,000,000. It has
{7|6|10}
digits.

$10^{\heartsuit}$ has
{♡ + 1|♡|10}
digits.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: looks-scary-1--letters
type: fill-in-the-blank

$10^6$ is 1,000,000. It has
{7|6|10}
digits.

$10^{n}$ has
{n + 1|n|10}
digits.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the zeros of 1,000,000. Then count the 1.
2. Each hop of ×10 adds one zero.
3. So how many zeros does the power have, and how many digits?

**Think about:** hops(10 → $10^6$) is 6. Here the hops land exactly on
a stop.

**Try this next:** how many digits does $10^{\heartsuit} - 1$ have?
It is a row of 9s.

</details>

## 8. What went differently here?

Here is a worked problem, with one step that went differently.

> $2^{20}$ is 20 × 0.30103 = 6.0206 hops of ×10. So $2^{20}$ has 6
> digits.

$2^{20}$ is 1,048,576. What went differently?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the digits of 1,048,576.
2. How many digits does $10^6$, 1,000,000, have?
3. $2^{20}$ is a little past $10^6$. What must we add to the whole
   part of the hops?

**Think about:** 1000 is three hops of ×10, and it has four digits.

**Try this next:** how many digits does $2^{40}$ have?

</details>

<details class="dl-answer"><summary>one way through it</summary>

1,048,576 has 7 digits. The worked problem took the whole part of the
hops, 6, and stopped there. It needs one more: the digits are the whole
part of the hops, plus one. So 6 + 1 = 7.

</details>

## 9. Two paths, one answer

How many A4 sheets make one A0 sheet? Here are two paths.

- **Folds.** A0 to A4 is 4 folds. Each fold doubles the pieces.
- **Areas.** A0 is 841 × 1189 = 999,949 square millimetres. A4 is
  210 × 297 = 62,370 square millimetres.

```question
id: two-paths-1
type: fill-in-the-blank

Four folds make $2^4$ =
{16|8|4}
pieces.

999,949 ÷ 62,370 is about
{16.03|4.01|160.3}.
```

Why is the second path not exactly 16?

<details class="dl-answer"><summary>one way through it</summary>

$2^4 = 16$, so the first path gives 16. The second gives about 16.03.
The sizes are whole millimetres, so the areas are a little off. The
folds do not depend on the millimetres, so they give exactly 16. Here
is one answer. Yours may be different and work too.

</details>

## 10. A stretch: cutting into more pieces

On the page, a sheet folded in half kept its shape when r × r = 2. What
if we cut the long side into more equal pieces?

<div class="dl-world" data-world="numbers">

```question
id: a-stretch-folding-1--numbers
type: fill-in-the-blank

Cut the long side into 3 equal pieces. The small sheet keeps the shape
when r = 3/r. Then r × r =
{3|9|6}.

So r is
{side(3)|3|side(9)}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: a-stretch-folding-1--squiggles
type: fill-in-the-blank

Cut the long side into ♡ equal pieces. The small sheet keeps the shape
when r = ♡/r. Then r × r =
{♡|♡ × ♡|2 × ♡}.

So r is
{side(♡)|♡|side(♡ × ♡)}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: a-stretch-folding-1--letters
type: fill-in-the-blank

Cut the long side into k equal pieces. The small sheet keeps the shape
when r = k/r. Then r × r =
{k|k²|2k}.

So r is
{side(k)|k|side(k²)}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. On the page, halving gave r = 2/r.
2. Multiply both sides by r. The r on the bottom cancels.
3. Now use 3, or your shape, in place of the 2.

**Think about:** the 2 in side(2) came from cutting into 2 pieces.

**Try this next:** side(3) is about 1.732. Would a sheet of that shape
look long and thin, or nearly square?

</details>

## 11. A stretch: the powers of 3

Each hop of ×3 is about 0.47712 hops of ×10. So $3^{100}$ is about
100 × 0.47712 = 47.712 hops of ×10. How many digits does it have?
Make your guess first. Then run the cell to check.

```python exec
id: a-stretch-the-powers-of-3-1
print(len(str(3 ** 100)))
```

<details class="dl-answer"><summary>one way through it</summary>

The whole part of 47.712 is 47. The digits are one more, so 48. The
cell prints 48.

</details>

## 12. From earlier: one whole sheet

From *Fractions: one whole pizza, many slices*. An A4 sheet is 1/16 of
an A0 sheet. Put 16 A4 sheets together. How much of A0 do they make?

<details class="dl-answer"><summary>answer</summary>

16/16 of A0, which is one whole A0 sheet. It is the pizza idea again:
all the slices together make the whole.

</details>

## 13. From earlier: side(8)

From *Sides that never end: surds, the square root of 2*.
side(8) = 2 × side(2). side(2) is about 1.414. What is side(8), about?
And what is side(8) × side(8)?

<details class="dl-answer"><summary>answer</summary>

side(8) is about 2 × 1.414 = 2.828. side(8) × side(8) is 8, because
side(8) is the side of a square of area 8.

</details>

## 14. Five of your own

Can you make five problems of your own? Here are some ideas:

- the shape test for a sheet you have at home
- how many A6 sheets make one A2 sheet
- the digits of $2^{\triangle}$, for a number △ you choose
- the last digits of the powers of 7
- a sheet cut into 4 pieces that keeps its shape

Which one was the hardest to make?
