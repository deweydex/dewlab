---
title: "Algebraic fractions: shapes and letters in fractions"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Algebraic fractions: shapes and letters in fractions

Here is a sum with a heart in it. On earlier pages, a heart could be
any number: 3, or 12, or a million.

$$\frac{1}{\heartsuit} + \frac{1}{\heartsuit}$$

```question
id: two-hearts-1
type: multiple-choice
answer: 1

A pizza is cut into ♡ equal slices. We take one slice, and then one
more. What is 1/♡ + 1/♡?

- 2/♡
  - Two slices, and each slice is 1/♡ of the pizza.
- 2/(♡ + ♡)
  - This adds the tops and adds the bottoms. The slices are still the
    same size.
- 1/♡
  - That is one slice. We took two.
```

## Check it with a number

We do not know what number the heart is. But we can choose one, and
check. Let the heart be 5.

```question
id: check-with-a-number-1
type: fill-in-the-blank

When ♡ is 5, the sum 1/♡ + 1/♡ is 1/5 + 1/5, which is {2/5|2/10|1/5}.
```

When the heart is 5, the answer $\frac{2}{\heartsuit}$ becomes
$\frac{2}{5}$ too.
Choose another number for the heart, and it still works. The slices are
all the same size, so we count them, and the bottom stays the same.

## The same slices, three ways

Choose numbers, shapes or letters in the box under the title. The
pattern is the same in each.

<div class="dl-world" data-world="numbers">

```question
id: the-same-slices-1--numbers
type: fill-in-the-blank

3/7 + 2/7 is {5/7|5/14|6/7}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: the-same-slices-1--squiggles
type: fill-in-the-blank

3/♡ + 2/♡ is {5/♡|5/(♡ + ♡)|6/♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: the-same-slices-1--letters
type: fill-in-the-blank

3/n + 2/n is {5/n|5/(n + n)|6/n}.
```

</div>

## Cutting every slice again

On *Equivalent fractions: the same amount, different names*, we cut
every slice into smaller slices. The top and the bottom were both
multiplied by the same number, and the amount stayed the same.

$$\frac{3 \times \heartsuit}{4 \times \heartsuit}$$

```question
id: cutting-every-slice-1
type: multiple-choice
answer: 1

What is the same amount as (3 × ♡)/(4 × ♡)?

- 3/4
  - Every slice of 3/4 was cut into ♡ smaller slices. The amount did
    not change.
- 3/4 × ♡
  - The heart is on the top and on the bottom. It does not make the
    amount bigger.
- ♡
  - The 3 and the 4 are still there.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Choose a number for the heart. Try 2.
2. The fraction becomes (3 × 2)/(4 × 2), which is 6/8.
3. What is the shortest name for 6/8?

**Think about:** the heart could be any number, and the answer does
not depend on it.

**Try this next:** what is (5 × △)/(8 × △)?

</details>

<div class="dl-world" data-world="numbers">

```question
id: cutting-every-slice-2--numbers
type: fill-in-the-blank

(5 × 9)/(8 × 9) is the same amount as {5/8|45/8|9}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: cutting-every-slice-2--squiggles
type: fill-in-the-blank

(5 × △)/(8 × △) is the same amount as {5/8|5/8 × △|△}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: cutting-every-slice-2--letters
type: fill-in-the-blank

(5 × k)/(8 × k) is the same amount as {5/8|(5 × k)/8|k}.
```

</div>

{{include: setup/zen-calm-check.md}}

## A fraction and its partner

On [Dividing fractions: how many fit?](tutorial:how-many-fit), a
fraction turned over was its partner. The two multiplied to make 1.
Here is the same move with shapes:

$$\frac{\triangle}{\heartsuit} \times \frac{\heartsuit}{\triangle}$$

```question
id: a-fraction-and-its-partner-1
type: fill-in-the-blank

The tops multiply to make △ × ♡.

The bottoms multiply to make {♡ × △|♡ + △|△ × △}.

So the answer is {1|△/♡|♡ × △}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Multiply the tops: △ × ♡.
2. Multiply the bottoms: ♡ × △.
3. 2 × 3 and 3 × 2 are the same number. Are △ × ♡ and ♡ × △ the same?

**Think about:** a fraction with the same top and bottom, from the
first pizza page.

**Try this next:** what is ★/□ × □/★?

</details>

## Different slices

This one has more steps. What is this sum?

$$\frac{1}{\heartsuit} + \frac{1}{\triangle}$$

The slices are different sizes. To add them, we cut both pizzas into
slices of the same size. Cut every $\frac{1}{\heartsuit}$ slice into
$\triangle$ smaller slices. Cut every $\frac{1}{\triangle}$ slice into
$\heartsuit$ smaller slices. Now both pizzas have $\heartsuit \times
\triangle$ slices.

```question
id: different-slices-1
type: fill-in-the-blank

1/♡ is now {△|♡|1} slices out of ♡ × △.

1/△ is now {♡|△|1} slices out of ♡ × △.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try it with numbers first. Let ♡ be 2 and △ be 3.
2. 1/2 is one slice of 2. Cut every slice into 3. How many small
   slices is the one slice now, out of 6?
3. 1/3 is one slice of 3. Cut every slice into 2. How many small
   slices is it now, out of 6?

**Think about:** when you cut every slice into △ pieces, one slice
becomes △ pieces.

**Try this next:** the same for 1/4 and 1/5. How many slices are in
the whole now?

</details>

Now the slices are the same size, so we can add them:

$$\frac{1}{\heartsuit} + \frac{1}{\triangle} = \frac{\triangle}{\heartsuit \times \triangle} + \frac{\heartsuit}{\heartsuit \times \triangle}$$

```question
id: different-slices-2
type: multiple-choice
answer: 1

What is 1/♡ + 1/△?

- (△ + ♡)/(♡ × △)
  - △ slices and ♡ slices, all the same size, out of ♡ × △.
- 2/(♡ + △)
  - This adds the tops and adds the bottoms. The slices were different
    sizes.
- 2/(♡ × △)
  - The small slices are the same size now. But there are more than
    two of them.
```

## Numbers for both shapes

We can check the answer with numbers. Let the heart be 2 and the
triangle be 3. Then the sum is $\frac{1}{2} + \frac{1}{3}$, and the
answer is

$$\frac{3 + 2}{2 \times 3} = \frac{5}{6}$$

Python can check this. Python cannot use a ♡ as a name, so the cell
writes the words `heart` and `triangle` instead. The first line gets the
`Fraction` tool ready.

```python exec
id: plug-in-numbers-1
from fractions import Fraction

heart = 2
triangle = 3
print(Fraction(1, heart) + Fraction(1, triangle))
print(Fraction(triangle + heart, heart * triangle))
```

```predict
type: choice

Before you run it: what will the two lines print?

- 5/6, and 5/6 again
  - The two lines are the same sum, written in two ways.
- 2/5, and then 5/6
  - The first line could seem to add the tops and add the bottoms.
- 5/6, and then 6/5
  - The second line could seem to be upside down.
```

Both lines print 5/6. Now change `heart` and `triangle` to any numbers
you like, and run it again. Do the two lines ever disagree? What
happens if the heart is 0? If the answer surprises you, read the end
of *Dividing fractions: how many fit?* again.

<div class="dl-world" data-world="numbers">

```question
id: plug-in-numbers-2--numbers
type: fill-in-the-blank

1/4 + 1/5 is {9/20|2/9|2/20}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: plug-in-numbers-2--squiggles
type: fill-in-the-blank

1/□ + 1/★ is {(★ + □)/(□ × ★)|2/(□ + ★)|2/(□ × ★)}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: plug-in-numbers-2--letters
type: fill-in-the-blank

1/x + 1/y is {(y + x)/(x × y)|2/(x + y)|2/(x × y)}.
```

</div>

## Letters

Many books use letters where this page uses shapes. A letter works in
the same way as a heart. Here is the sum again, with $a$ for the heart
and $b$ for the triangle:

$$\frac{1}{a} + \frac{1}{b} = \frac{b + a}{a \times b}$$

In books, $a \times b$ is often written $ab$, with no sign between. A
fraction with a letter or a shape in it is called an *algebraic
fraction*. *Algebra* is the part of maths that uses letters for
numbers.

A shape or a letter is only a number we have not chosen yet. So every
move from the pizza pages still works: adding slices of the same size,
cutting every slice again, multiplying, and turning over.

The page [Running a formula backwards: rearranging and
inverses](tutorial:running-a-formula-backwards#fractions-with-letters-in-them)
has a section on fractions with letters. It uses these moves on a
question about a drone, a small flying machine.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say the idea of this page in your own
words. Why do the pizza moves still work with a shape? Write it in the
Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A shape or a letter in a fraction stands for a number we have not
chosen yet. Whatever number it is, the fraction is still slices of a
pizza. So we add, cut, multiply and turn over in the same way as with
numbers. To check, choose a number for each shape, and find the answer
both ways. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five problems of your own with shapes or letters in them?
Choose numbers for the shapes, and check each one with `Fraction`. Here
are some ideas:

- a sum of slices of the same size
- a fraction where the same shape is on the top and the bottom
- a fraction times its partner
- a sum of two fractions with different shapes on the bottom
- one that looks scary, but is exactly 1

## Looking back

On *Fractions: one whole pizza, many slices*, we wrote
$\frac{\heartsuit}{\heartsuit} = 1$. Where did that idea appear again
on this page?

A challenge: does $\frac{\triangle + \heartsuit}{\heartsuit \times
\triangle}$ always match $\frac{1}{\heartsuit} + \frac{1}{\triangle}$?
The program below checks five pairs of numbers. Can you make it check a
hundred? Can you find a pair where the two do not match?

```python challenge
# Does (triangle + heart) / (heart * triangle) always match
# 1/heart + 1/triangle? Check many pairs of numbers.
from fractions import Fraction

for heart in range(1, 6):
    triangle = heart + 1
    added = Fraction(1, heart) + Fraction(1, triangle)
    formula = Fraction(triangle + heart, heart * triangle)
    print(heart, triangle, added, formula, added == formula)
```

## Read more

Wikipedia's page on [algebraic
fractions](https://en.wikipedia.org/wiki/Algebraic_fraction) shows
more of them. It uses more letters than this page, but the moves are
the same.
