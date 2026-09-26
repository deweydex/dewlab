---
title: "Powers: the long way and the short way — Practice"
practice_for: the-long-way
year: "2026-2027"
version: 2026.09.26.1
worlds:
  numbers: Ordinary numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Powers: the long way and the short way — Practice

Small problems on one idea: a power is a number multiplied by itself,
written the short way. Try each problem before you open anything under
it. Choose numbers, shapes or letters in the box under the title.

## 1. The long way

<div class="dl-world" data-world="numbers">

```question
id: the-long-way-1--numbers
type: fill-in-the-blank

2⁶ the long way is {2 × 2 × 2 × 2 × 2 × 2|2 × 6|6 × 6}.

7³ the long way is {7 × 7 × 7|7 × 3|7 + 7 + 7}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: the-long-way-1--squiggles
type: fill-in-the-blank

△⁶ the long way is {△ × △ × △ × △ × △ × △|△ × 6|6 × 6}.

♡³ the long way is {♡ × ♡ × ♡|♡ × 3|♡ + ♡ + ♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: the-long-way-1--letters
type: fill-in-the-blank

g⁶ the long way is {g × g × g × g × g × g|g × 6|6 × 6}.

h³ the long way is {h × h × h|h × 3|h + h + h}.
```

</div>

## 2. The short way

<div class="dl-world" data-world="numbers">

```question
id: the-short-way-1--numbers
type: fill-in-the-blank

4 × 4 × 4 × 4 × 4 the short way is {4⁵|4 × 5|5⁴}.

9 × 9 the short way is {9²|9 × 2|2⁹}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: the-short-way-1--squiggles
type: fill-in-the-blank

★ × ★ × ★ × ★ × ★ the short way is {★⁵|5★|5^★}.

△ × △ the short way is {△²|2△|2^△}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: the-short-way-1--letters
type: fill-in-the-blank

k × k × k × k × k the short way is {k⁵|5k|5^k}.

m × m the short way is {m²|2m|2^m}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What is being multiplied? That is the base.
2. Count how many times it appears. That is the exponent.
3. Write the base, with the count small and raised beside it.

**Think about:** the count goes up high, not in front.

**Try this next:** how would you write a hundred of them multiplied
together?

</details>

## 3. How much is it?

Only numbers here, since these ask for an amount.

```question
id: how-much-is-it-1
type: fill-in-the-blank

2⁶ is {64|12|36}.

10⁴ is {10000|40|1000}.

3³ is {27|9|6}.

1⁵⁰ is {1|50|51}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the power the long way first.
2. Multiply two of the numbers. Then multiply that answer by the next
   one, and so on.
3. For $10^4$, count the zeros: each 10 adds one.

**Think about:** what multiplying 1 by itself does, however many times.

**Try this next:** $10^9$. How many zeros?

</details>

## 4. Check it with Python

Python writes a power with two stars. Change the numbers to check any
of the problems above.

```python exec
id: check-it-with-python-1
print(2 ** 6)
print(10 ** 4)
```

## 5. When the exponent is a shape too

This problem comes from a Maths for IT worksheet. What does a power
mean when we do not know its exponent?

<div class="dl-world" data-world="numbers">

Here is a power. Its base is 2, but we do not know its exponent yet.
How would you write it the long way?

</div>

<div class="dl-world" data-world="squiggles">

How would you write $\heartsuit^{\triangle}$ the long way?

</div>

<div class="dl-world" data-world="letters">

How would you write $f^m$ the long way?

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The base is multiplied by itself. That part does not change.
2. The exponent still counts how many times the base appears.
3. You cannot write every one, because you do not know how many there
   are. How could you show "and so on"?

**Think about:** what "…" means at the end of a list.

**Try this next:** how is the one with exponent "one more than
before" different?

</details>

<details class="dl-answer"><summary>one way through it</summary>

Write a few, then "…". Then say how many there are in total:

$$\heartsuit^{\triangle} = \underbrace{\heartsuit \times \heartsuit \times \cdots \times \heartsuit}_{\triangle \text{ hearts}}$$

With letters it is the same: $f^m$ is $m$ copies of $f$ multiplied
together. With one more in the exponent, there is one more copy:
$f^{m+1} = f^m \times f$.

</details>

## 6. A fraction for a base

<div class="dl-world" data-world="numbers">

```question
id: a-fraction-for-a-base-1--numbers
type: fill-in-the-blank

(1/3)² is {1/9|2/3|1/6}.

(2/3)² is {4/9|4/6|2/9}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: a-fraction-for-a-base-1--squiggles
type: fill-in-the-blank

(1/♡)² is {1/♡²|2/♡|1/(2 × ♡)}.

(△/2)³ is {△³/8|3△/2|△³/2}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: a-fraction-for-a-base-1--letters
type: fill-in-the-blank

(1/j)⁴ is {1/j⁴|4/j|1/(4j)}.

(h/2)³ is {h³/8|3h/2|h³/2}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the power the long way: the fraction, times itself, as many
   times as the exponent says.
2. Multiplying fractions: the tops multiply together, and the bottoms
   multiply together. The folded paper did this: half of a half is a
   quarter.
3. Write the top and the bottom as powers.

**Think about:** the power reaches the top *and* the bottom.

**Try this next:** $\left(\frac{1}{10}\right)^3$.

</details>

## 7. Growing and shrinking

What happens to $\left(\frac{1}{2}\right)^n$ as $n$ gets bigger: 1, 2,
3, 10, 100? And what happens to $2^n$? Guess first, then use the cell.

```python exec
id: growing-and-shrinking-1
for exponent in [1, 2, 3, 10, 100]:
    print(exponent, 2 ** exponent, (1 / 2) ** exponent)
```

<details class="dl-answer"><summary>one way to see it</summary>

$2^n$ grows faster and faster: $2^{100}$ has 31 digits. $(1/2)^n$ gets
smaller and smaller, but never gets to zero: $(1/2)^{100}$ is about
$0.0000000000000000000000000000008$. A number bigger than 1 grows when
we multiply it by itself. A number between 0 and 1 gets smaller. Python
prints the very small number as `7.888609052210118e-31`. This is
Python's short way to write a very small number. A later page is about
it.

</details>

## 8. Two ways round

$2^3$ is 8 and $3^2$ is 9. Is there a pair of different whole numbers
where swapping the base and the exponent gives the *same* answer?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try the small ones: 2 and 3, 2 and 4, 2 and 5.
2. Find each power both ways round, or use the cell in problem 4.
3. Stop when you find a pair that matches.

**Think about:** how rare you think such a pair is.

**Try this next:** is there a second pair?

</details>

<details class="dl-answer"><summary>answer</summary>

$2^4 = 16$ and $4^2 = 16$. It is the only pair of different whole
numbers that works, which mathematicians proved a long time ago.

</details>

## 9. Beads beyond the cube

From the golden beads: the cube is $10^3 = 1000$ beads. How many beads
is $10^5$? If you built it from cubes, how many cubes would you need?

<details class="dl-answer"><summary>answer</summary>

$10^5 = 100000$ beads. That is 100 cubes of 1000. Put the cubes in a
square, ten by ten. It looks like the hundred-square, made of cubes.

</details>

## 10. From earlier: sixteen pieces

From *Fractions: one whole pizza, many slices*. After 4 folds, a sheet
is in 16 equal pieces, each $\frac{1}{16}$ of the sheet. How much of the
sheet do all 16 pieces make?

<details class="dl-answer"><summary>answer</summary>

The whole sheet: $\frac{16}{16} = 1$.

</details>

## 11. From earlier: another name

From *Equivalent fractions: the same amount, different names*. What is
the simplest name for $\frac{8}{16}$?

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{2}$: divide the top and the bottom by 8.

</details>

## 12. Five wild ones of your own

This page comes from a worksheet. Each part of that worksheet ends like
this: make five problems of your own, as strange as you like. Here are
some ideas:

- a very big exponent
- a fraction or a decimal as the base
- a shape as the exponent
- an exponent of 1

Which of your problems surprises you most?
