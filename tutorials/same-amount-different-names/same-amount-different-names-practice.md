---
title: "Equivalent fractions: the same amount, different names — Practice"
practice_for: same-amount-different-names
year: "2026-2027"
version: 2026.09.26.1
worlds:
  numbers: Ordinary numbers, like 3 and 12.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like n and k, which can stand for any number.
---

# Equivalent fractions: the same amount, different names — Practice

Small problems on one idea: the same amount can have many names. Try
each problem before you open anything under it. Some problems come with
numbers, shapes or letters. Choose the way you like in the box under
the title.

## 1. The same, or different?

```question
id: same-or-different-1
type: fill-in-the-blank

3/6 and 1/2 are {the same amount|different amounts}.

2/3 and 1/2 are {different amounts|the same amount}.

5/10 and 1/2 are {the same amount|different amounts}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Half of 6 is 3. So is 3/6 half of the pizza?
2. Half of 3 is one and a half. Is 2 slices out of 3 more than half, or
   less?
3. Half of 10 is 5.

**Think about:** a fraction is exactly one half when its top is half of
its bottom.

**Try this next:** is 7/14 the same amount as 1/2?

</details>

## 2. Fill the gap

<div class="dl-world" data-world="numbers">

```question
id: fill-the-gap-1--numbers
type: fill-in-the-blank

1/3 is the same amount as {3|1|9} ninths.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: fill-the-gap-1--squiggles
type: fill-in-the-blank

Cut every third into ♡ slices. Then 1/3 is the same amount as {♡|3|1}
slices out of 3 × ♡.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: fill-the-gap-1--letters
type: fill-in-the-blank

Cut every third into k slices. Then 1/3 is the same amount as {k|3|1}
slices out of 3k.
```

</div>

## 3. Cut every slice into three

Start with $\frac{2}{5}$. Cut every slice into 3 smaller slices.

```question
id: cut-into-three-1
type: multiple-choice
answer: 1

What is the new name for the same amount?

- 6/15
  - The slices we have: 2 becomes 6. The slices in the whole: 5
    becomes 15.
- 6/5
  - The slices we have were cut into 3, but so were all the others.
- 2/15
  - The whole pizza now has 15 slices, but we have more than 2 of them.
```

## 4. The shortest name

```question
id: the-shortest-name-1
type: fill-in-the-blank

The simplest name for 10/15 is {2/3|5/15|10/5}.

The simplest name for 9/12 is {3/4|3/12|9/4}.

The simplest name for 500/1000 is {1/2|50/100|5/10}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find a number that divides both the top and the bottom with nothing
   left over. For 10/15, try 5.
2. Divide both by it.
3. Look again. Is there another number that divides both?

**Think about:** when to stop. You stop when only 1 divides both.

**Try this next:** the simplest name for 24/36.

</details>

## 5. Check it with Python

You can check the problems on this page with `Fraction`. It always
prints the simplest name. Change the numbers and run it.

```python exec
id: check-it-with-python-1
from fractions import Fraction

print(Fraction(10, 15))
print(Fraction(9, 12) == Fraction(3, 4))
```

## 6. What went differently here?

Somebody wanted another name for $\frac{1}{2}$. They added 1 to the top
and 1 to the bottom, and wrote $\frac{2}{3}$. Is $\frac{2}{3}$ the same
amount as $\frac{1}{2}$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Picture a pizza cut into 3 slices, with 2 of them shaded.
2. Is more than half of it shaded, or less?
3. What would the top and the bottom need instead, to stay at one half?

**Think about:** adding 1 to the top and 1 to the bottom is different
from cutting every slice again.

**Try this next:** what happens to $\frac{1}{2}$ if you add 100 to the
top and 100 to the bottom?

</details>

<details class="dl-answer"><summary>one way through it</summary>

No. $\frac{2}{3}$ is more than half: two slices out of three. Adding
the same number to the top and the bottom changes the amount.
Multiplying both by the same number does not change it, because it only
cuts every slice again. Adding feels just as fair. That is why many
people try it.

</details>

## 7. Which is bigger?

Which is more pizza, $\frac{3}{4}$ or $\frac{5}{8}$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The two fractions have different slices: quarters and eighths.
2. Find another name for $\frac{3}{4}$ in eighths. Look back at the
   wall on the page if it helps.
3. Now both are counted in eighths. Which has more?

**Think about:** why it is easier to compare two fractions with the same
bottom number.

**Try this next:** which is bigger, $\frac{2}{3}$ or $\frac{7}{12}$?

</details>

<details class="dl-answer"><summary>one way through it</summary>

$\frac{3}{4}$ is the same amount as $\frac{6}{8}$. Six eighths is more
than five eighths, so $\frac{3}{4}$ is bigger, by one eighth.

</details>

## 8. Shapes that cancel

<div class="dl-world" data-world="numbers">

```question
id: shapes-that-cancel-1--numbers
type: fill-in-the-blank

(3 × 7) / (4 × 7) is the same amount as {3/4|21/4|7}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: shapes-that-cancel-1--squiggles
type: fill-in-the-blank

(3 × ♡) / (4 × ♡) is the same amount as {3/4|3/4 × ♡|♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: shapes-that-cancel-1--letters
type: fill-in-the-blank

(3 × k) / (4 × k) is the same amount as {3/4|3k/4|k}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The top and the bottom were both multiplied by the same thing.
2. That is what cutting every slice again looks like.
3. What was the fraction before every slice was cut?

**Think about:** it does not matter what number is hiding in the shape
or the letter.

**Try this next:** $(5 \times \triangle) / (8 \times \triangle)$.

</details>

## 9. From earlier: every slice

From *Fractions: one whole pizza, many slices*. A pizza is cut into 6 slices. How
many slices of $\frac{1}{6}$ make the whole pizza, and what is
$\frac{6}{6}$?

<details class="dl-answer"><summary>answer</summary>

Six of them, and $\frac{6}{6} = 1$, one whole pizza.

</details>

## 10. From earlier: folds and pieces

From *Before we start*. A sheet of paper is folded in half 4 times, then
unfolded flat. The creases divide it into equal pieces. How many
pieces, and what fraction of the sheet is each one?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Each fold doubles the number of layers, so it doubles the pieces too.
2. 1, 2, 4, …: keep doubling, four times.
3. If the sheet is in that many equal pieces, what is each piece called?

**Think about:** this is the pizza idea again, with paper.

**Try this next:** 5 folds.

</details>

<details class="dl-answer"><summary>answer</summary>

16 pieces, and each is $\frac{1}{16}$ of the sheet. All 16 together are
$\frac{16}{16}$, the whole sheet.

</details>

## 11. Five of your own

Can you find five names for $\frac{2}{5}$? Make one with a bottom number
bigger than 1000, and one with a shape in it. Then make a fraction that
*looks* like $\frac{2}{5}$ but is a different amount. How can you tell?
