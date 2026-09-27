---
title: "Algebraic fractions: shapes and letters in fractions — Practice"
practice_for: fractions-with-holes
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Ordinary numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Algebraic fractions: shapes and letters in fractions — Practice

Small problems on one idea: a shape or a letter is a number we have not
chosen yet, so the pizza moves still work. Try each problem before you
open anything under it. There is no hurry, and no score. Choose
numbers, shapes or letters in the box under the title.

## 1. The same, or different?

<div class="dl-world" data-world="numbers">

```question
id: same-or-different-1--numbers
type: fill-in-the-blank

1/7 + 1/7 and 2/7 are {the same amount|different amounts}.

1/7 + 1/7 and 2/14 are {different amounts|the same amount}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: same-or-different-1--squiggles
type: fill-in-the-blank

1/♡ + 1/♡ and 2/♡ are {the same amount|different amounts}.

1/♡ + 1/♡ and 2/(♡ + ♡) are {different amounts|the same amount}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: same-or-different-1--letters
type: fill-in-the-blank

1/n + 1/n and 2/n are {the same amount|different amounts}.

1/n + 1/n and 2/(n + n) are {different amounts|the same amount}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Two slices of the same size: count them, and keep the bottom.
2. If there is a shape or a letter, choose a number for it. Try 7.
3. What is 2/14 in its shortest name? Is it the same as 2/7?

**Think about:** adding the bottoms would make the slices smaller.

**Try this next:** 1/♡ + 1/♡ + 1/♡.

</details>

## 2. Fill the gap

<div class="dl-world" data-world="numbers">

```question
id: fill-the-gap-1--numbers
type: fill-in-the-blank

3/10 + {4|10|7}/10 = 7/10.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: fill-the-gap-1--squiggles
type: fill-in-the-blank

3/△ + {4|△|7}/△ = 7/△.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: fill-the-gap-1--letters
type: fill-in-the-blank

3/b + {4|b|7}/b = 7/b.
```

</div>

## 3. Words, sum and answer

```question
id: words-sum-and-answer-1
type: multiple-choice
answer: 1

Which three go together?

- Half of 1/♡, and 1/2 × 1/♡, and 1/(2 × ♡)
  - "Of" means times. Then the tops multiply, and the bottoms multiply.
- Half of 1/♡, and 1/2 + 1/♡, and 2/(2 + ♡)
  - "Of" means times, not plus.
- Half of 1/♡, and 1/2 × 1/♡, and 2/♡
  - Half of a slice is smaller than the slice. 2/♡ is two slices.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Choose a number for the heart. Try 5.
2. Half of 1/5: picture a slice of a pizza cut into 5, then cut that
   slice in half.
3. How many of those small pieces would make the whole pizza?

**Think about:** cutting every slice in half doubles the number of
slices in the whole.

**Try this next:** what is a third of 1/△?

</details>

## 4. Cutting every slice again

<div class="dl-world" data-world="numbers">

```question
id: cutting-again-1--numbers
type: fill-in-the-blank

(7 × 11)/(9 × 11) is the same amount as {7/9|77/9|11}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: cutting-again-1--squiggles
type: fill-in-the-blank

(7 × ★)/(9 × ★) is the same amount as {7/9|(7 × ★)/9|★}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: cutting-again-1--letters
type: fill-in-the-blank

(7 × m)/(9 × m) is the same amount as {7/9|(7 × m)/9|m}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The top and the bottom are both multiplied by the same thing.
2. That is what cutting every slice again looks like.
3. What was the fraction before every slice was cut?

**Think about:** the answer does not depend on which number is in the
shape.

**Try this next:** (2 × ♡)/(2 × △).

</details>

## 5. Numbers in place of shapes

What is $\frac{1}{\heartsuit} + \frac{1}{\triangle}$ when the heart is
3 and the triangle is 4? Find it first with the page's answer,
$\frac{\triangle + \heartsuit}{\heartsuit \times \triangle}$. Then
check it in the cell. Change the numbers to check your own.

```python exec
id: plug-in-numbers-1
from fractions import Fraction

heart = 3
triangle = 4
print(Fraction(1, heart) + Fraction(1, triangle))
print(Fraction(triangle + heart, heart * triangle))
```

<details class="dl-answer"><summary>one way through it</summary>

$\frac{4 + 3}{3 \times 4} = \frac{7}{12}$. Both lines of the cell print
7/12.

</details>

## 6. What went differently here?

Somebody added two fractions like this:

$$\frac{1}{\heartsuit} + \frac{1}{\triangle} = \frac{2}{\heartsuit + \triangle}$$

Choose 2 for the heart and 3 for the triangle. Do the two sides of the
= sign give the same amount?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Before the = sign, the sum becomes 1/2 + 1/3.
2. After the = sign, it becomes 2/(2 + 3).
3. Find both. The cell in problem 5 can help with the first one.

**Think about:** what adding the bottoms does to the size of the
slices.

**Try this next:** try 1 for the heart and 1 for the triangle. Do the
two sides agree now?

</details>

<details class="dl-answer"><summary>one way through it</summary>

No. Before the = sign, $\frac{1}{2} + \frac{1}{3} = \frac{5}{6}$.
After it, $\frac{2}{2 + 3} = \frac{2}{5}$. The tops and the bottoms were added, but
the slices were different sizes. First cut both pizzas into
$\heartsuit \times \triangle$ slices:

$$\frac{1}{\heartsuit} + \frac{1}{\triangle} = \frac{\triangle + \heartsuit}{\heartsuit \times \triangle}$$

With 2 and 3, that gives $\frac{5}{6}$.

</details>

## 7. Two paths, one answer

Here is $\frac{2 \times \heartsuit}{6 \times \heartsuit}$, two ways.

- Path one: the heart is on the top and the bottom. Divide the top and
  the bottom by the heart first. Then find the shortest name.
- Path two: choose 10 for the heart. Find the fraction, then its
  shortest name.

Do the two paths meet?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Path one: without the heart, the fraction is 2/6.
2. Path two: with 10, the fraction is 20/60.
3. Give each its shortest name.

**Think about:** why the choice of 10 does not change the answer.

**Try this next:** choose 1000 for the heart.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Path one: $\frac{2}{6} = \frac{1}{3}$. Path two: $\frac{20}{60} =
\frac{1}{3}$. Both give $\frac{1}{3}$. Any number for the heart gives
$\frac{1}{3}$ too.

</details>

## 8. Looks scary, is simple

<div class="dl-world" data-world="numbers">

```question
id: looks-scary-1--numbers
type: fill-in-the-blank

(13 × 17 × 19)/(19 × 13 × 17) is {1|0|13/19}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: looks-scary-1--squiggles
type: fill-in-the-blank

(★ × △ × ♡)/(♡ × ★ × △) is {1|0|★/♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: looks-scary-1--letters
type: fill-in-the-blank

(p × q × r)/(r × p × q) is {1|0|p/r}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. List what is multiplied on the top.
2. List what is multiplied on the bottom.
3. Is anything on one list missing from the other?

**Think about:** 2 × 3 × 5 and 5 × 2 × 3 are the same number.

**Try this next:** △/♡ × ♡/★ × ★/△.

</details>

## 9. Close to 0, a half, or 1?

Picture a very big number: a million. Where does each fraction land?

<div class="dl-world" data-world="numbers">

```question
id: close-to-1--numbers
type: fill-in-the-blank

1/1000000 is closest to {0|1/2|1}.

1000000/1000001 is closest to {1|1/2|0}.

1000000/2000000 is exactly {1/2|0|1}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: close-to-1--squiggles
type: fill-in-the-blank

When ♡ is a million, 1/♡ is closest to {0|1/2|1}.

When ♡ is a million, ♡/(♡ + 1) is closest to {1|1/2|0}.

When ♡ is a million, ♡/(2 × ♡) is exactly {1/2|0|1}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: close-to-1--letters
type: fill-in-the-blank

When n is a million, 1/n is closest to {0|1/2|1}.

When n is a million, n/(n + 1) is closest to {1|1/2|0}.

When n is a million, n/(2 × n) is exactly {1/2|0|1}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. One slice of a million is very thin.
2. A million slices out of a million and one is every slice but one.
3. The last one: the bottom is twice the top.

**Think about:** "one slice missing" is almost the whole pizza.

**Try this next:** when ♡ is a million, where is (♡ − 1)/♡?

</details>

## 10. A stretch: two different slices

This one goes past the page. What is this sum?

$$\frac{1}{\heartsuit} + \frac{1}{2 \times \heartsuit}$$

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The second slice is half the size of the first.
2. Cut every slice of the first pizza into 2. Then 1/♡ is 2 small
   slices out of 2 × ♡.
3. Now both are counted in slices of 1/(2 × ♡). Add them.

**Think about:** you do not always need to multiply the two bottoms.
Here one bottom already fits the other.

**Try this next:** 1/♡ + 1/(3 × ♡).

</details>

<details class="dl-answer"><summary>one way through it</summary>

$$\frac{1}{\heartsuit} + \frac{1}{2 \times \heartsuit} = \frac{2}{2 \times \heartsuit} + \frac{1}{2 \times \heartsuit} = \frac{3}{2 \times \heartsuit}$$

Check with 5 for the heart: $\frac{1}{5} + \frac{1}{10} = \frac{3}{10}$,
and $\frac{3}{2 \times 5} = \frac{3}{10}$ too.

</details>

## 11. From earlier: how many fit?

From *Dividing fractions: how many fit?*. How many thirds fit in 3
pizzas? Write it as a division.

<details class="dl-answer"><summary>answer</summary>

$3 \div \frac{1}{3} = 9$. Each pizza holds 3 thirds, and there are 3
pizzas.

</details>

## 12. From earlier: a fraction of a fraction

From *Multiplying fractions: a fraction of a fraction*. What is two
thirds of three quarters? Draw the square if it helps.

<details class="dl-answer"><summary>answer</summary>

$\frac{2}{3} \times \frac{3}{4} = \frac{6}{12} = \frac{1}{2}$.

</details>

## 13. Five of your own

Can you make five problems of your own, with shapes or letters in them?
Make each one a little stranger. Here are some ideas:

- a sum of slices of the same size
- a fraction times its partner
- a sum of two fractions with different shapes on the bottom
- a tangle of shapes that is exactly 1

Choose numbers for the shapes, and check each problem with `Fraction`.
Which of your problems looks scariest, and is simplest?
