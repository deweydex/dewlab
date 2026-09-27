---
title: "Sides that never end: surds, the square root of 2 — Practice"
practice_for: sides-that-never-end
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Sides that never end: surds, the square root of 2 — Practice

These small problems are about sides that are not whole numbers, like
side(2). Its digits never stop and never repeat. Try each problem before
you open anything under it. Some problems come with numbers, shapes or
letters. Choose the way you like in the box under the title.

## 1. Where on the line?

Each of these sides is between two whole numbers. Picture a line with
the whole numbers on it.

```question
id: where-on-the-line-1
type: fill-in-the-blank

side(3) is between 1 and {2|3|4}.

side(5) is between 2 and {3|4|5}.

side(8) is between {2|3|4} and 3.

side(8) is closer to {3|2}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the first square numbers: 1, 4, 9, 16.
2. Find the two square numbers that each number sits between.
3. For side(8): is 8 closer to 4, or closer to 9?

**Think about:** the side of a number is between the sides of the two
square numbers around it.

**Try this next:** side(15) is between which two whole numbers? Which
one is it closer to?

</details>

## 2. Which sides are whole?

Of side(1), side(2), side(3), and so on up to side(20), how many are
whole numbers? Make a guess first. Then run the cell. It tries every
whole number for every area from 1 to 20.

```python exec
id: which-sides-are-whole-1
for area in range(1, 21):
    for side_length in range(1, area + 1):
        if side_length * side_length == area:
            print("side of", area, "is", side_length)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A side is whole when the area is a square number.
2. Write the square numbers up to 20.
3. How many did you write?

**Think about:** the other areas all have sides between two whole
numbers.

**Try this next:** how many from side(1) to side(100) are whole?

</details>

<details class="dl-answer"><summary>answer</summary>

Four: side(1) = 1, side(4) = 2, side(9) = 3 and side(16) = 4. The other
16 are not whole numbers. Their digits never stop.

</details>

## 3. Guess and check side(3)

side(3) is between 1 and 2. Use the cell to find it to two places after
the point. Try 1.7, then 1.73, then 1.74.

```python exec
id: guess-and-check-side-3-1
from decimal import Decimal

guess = Decimal("1.7")
print(guess * guess)
```

The first line gets the `Decimal` tool ready, which multiplies decimals
exactly.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Run the cell with 1.7. Is the answer more or less than 3?
2. Try 1.73. More or less than 3?
3. Try 1.74. More or less than 3?

**Think about:** when one guess is under 3 and the next is over 3,
side(3) is between them.

**Try this next:** find side(3) to three places.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$1.7 \times 1.7 = 2.89$, less than 3. $1.73 \times 1.73 = 2.9929$,
still less than 3. $1.74 \times 1.74 = 3.0276$, more than 3. So side(3)
is between 1.73 and 1.74. To more places, it is 1.7320508…, and its
digits never stop.

</details>

## 4. Fill the gap

A side times itself gives the area again.

<div class="dl-world" data-world="numbers">

```question
id: fill-the-gap-1--numbers
type: fill-in-the-blank

side(2) × side(2) = {2|4|1}

side(7) × side(7) = {7|49|14}
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: fill-the-gap-1--squiggles
type: fill-in-the-blank

side(♡) × side(♡) = {♡|♡ × ♡|2 × ♡}

side(△) × side(△) = {△|△ × △|2 × △}
```

</div>

<div class="dl-world" data-world="letters">

```question
id: fill-the-gap-1--letters
type: fill-in-the-blank

side(n) × side(n) = {n|n × n|2n}

side(k) × side(k) = {k|k × k|2k}
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. side(2) is the side of a square with area 2.
2. A square's area is its side times its side.
3. So what is side(2) × side(2)?

**Think about:** side(…) undoes a square. Squaring undoes side(…).

**Try this next:** side(10) × side(10).

</details>

## 5. The same, or different?

```question
id: the-same-or-different-1
type: fill-in-the-blank

side(8) and 2 × side(2) are {the same number|different numbers}.

side(8) and 4 are {different numbers|the same number}.

side(8) and side(2) + side(2) are {the same number|different numbers}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the big tilted square in the tutorial. Its side is two
   diagonals of a small square.
2. One diagonal is side(2).
3. For 4: what is 4 × 4? Is it 8?

**Think about:** 2 × side(2) and side(2) + side(2) are two ways to
write the same thing.

**Try this next:** is side(8) the same as side(4) + side(4)?

</details>

## 6. The side of 18

A grid 6 by 6 has a tilted square inside it, like the ones in the
tutorial. Its area is half of 36, which is 18. Each side of it crosses
3 small squares, corner to corner.

<div class="dl-world" data-world="numbers">

```question
id: the-side-of-18-1--numbers
type: fill-in-the-blank

side(18) = side(2 × 3 × 3) = {3|9|6} × side(2)

So side(18) is about {4.24|2.83|9}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: the-side-of-18-1--squiggles
type: fill-in-the-blank

side(2 × △ × △) = {△|△ × △|2 × △} × side(2)

side(2 × ★ × ★) = {★|★ × ★|2 × ★} × side(2)
```

</div>

<div class="dl-world" data-world="letters">

```question
id: the-side-of-18-1--letters
type: fill-in-the-blank

side(2 × m × m) = {m|m × m|2m} × side(2)

side(2 × p × p) = {p|p × p|2p} × side(2)
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Each side of the tilted square is 3 diagonals long.
2. One diagonal is side(2).
3. side(2) is about 1.414. What is 3 × 1.414?

**Think about:** the number that appears twice in the brackets comes
out once, in front.

**Try this next:** side(2 × 4 × 4), which is side(32).

</details>

## 7. Two paths to side(50)

$50 = 2 \times 5 \times 5$. Here are two ways to find side(50).

- Path one: side(50) = 5 × side(2).
- Path two: the machine below, with `area = 50`.

Do they give the same digits?

```python exec
id: two-paths-to-side-50-1
from decimal import Decimal

area = 50

side = Decimal(0)
step = Decimal(1)
for places in range(0, 21):
    while (side + step) * (side + step) <= area:
        side = side + step
    print(round(side, places))
    step = step / 10
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Run this cell. Read the last line.
2. For path one, find 5 × 1.41421356237309504880. Add this line at the
   end of the cell: `print(5 * Decimal("1.41421356237309504880"))`.
3. Compare the two last lines.

**Think about:** a tilted square in a grid 10 by 10 has area 50.

**Try this next:** find side(32) both ways.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Both paths give 7.07106781186547524400. Path one: 5 × side(2) is
5 × 1.41421356237309504880 = 7.07106781186547524400. Path two: the
machine finds the same 20 places.

</details>

## 8. What went differently here?

Somebody found $1.4 \times 1.4 = 1.96$. They wrote: "So side(2) = 1.4."
What happened?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. side(2) is the number that, times itself, makes exactly 2.
2. Is 1.96 exactly 2?
3. Is 1.4 a little too big, or a little too small?

**Think about:** "very close" and "exactly" are different.

**Try this next:** what does 1.41 × 1.41 give?

</details>

<details class="dl-answer"><summary>one way through it</summary>

1.96 is close to 2, but it is not 2. So 1.4 is a little less than
side(2). Many people stop here, because
1.96 looks so close. Adding digits brings the guess closer: 1.41, then
1.414. No guess with digits that stop is ever exactly side(2). Here is
one answer. Yours may be different and work too.

</details>

## 9. From earlier: the simplest name

From *Equivalent fractions: the same amount, different names*. 1.4 is
the same as $\frac{14}{10}$. What is the simplest name for
$\frac{14}{10}$?

<details class="dl-answer"><summary>answer</summary>

$\frac{7}{5}$: divide the top and the bottom by 2. Problem 10 uses it.

</details>

## 10. A stretch: a fraction for side(2)?

$\frac{7}{5} \times \frac{7}{5} = \frac{49}{25}$, a little less than 2.
Can you find a fraction that, times itself, is exactly 2? The cell
below checks a fraction. The first line gets the `Fraction` tool ready.
Try $\frac{17}{12}$, $\frac{41}{29}$ and $\frac{99}{70}$.

```python exec
id: a-fraction-for-side-2-1
from fractions import Fraction

guess = Fraction(7, 5)
print(guess * guess)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Run the cell with 7/5. Look at the top and the bottom of the answer.
2. For exactly 2, the top would be exactly twice the bottom. Is 49
   twice 25?
3. Try the other fractions. Compare each top with twice its bottom.

**Think about:** how close the top gets to twice the bottom, each time.

**Try this next:** try $\frac{577}{408}$.

</details>

<details class="dl-answer"><summary>answer</summary>

No fraction works. The tutorial said so: people proved long ago that no
fraction can ever equal side(2). The fractions here get very close.
$\frac{577}{408} \times \frac{577}{408} = \frac{332929}{166464}$. Twice
166464 is 332928, so the top is only 1 more than twice the bottom. For
each fraction here, the top is 1 more or 1 less than twice the bottom.
None is ever exactly twice.

</details>

## 11. Looks scary, is simple

<div class="dl-world" data-world="numbers">

What is side(2 × 100 × 100)? Use side(2) = 1.41421356….

</div>

<div class="dl-world" data-world="squiggles">

What is side(2 × ♡ × ♡ × ♡ × ♡)?

</div>

<div class="dl-world" data-world="letters">

What is side(2 × k × k × k × k)?

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put the four in pairs: two of them make one group, and two make
   another.
2. So the brackets hold 2 times a group, times the same group again.
3. The group appears twice, so it comes out once, in front.

**Think about:** side(2 × ♡ × ♡) = ♡ × side(2).

**Try this next:** side(2 × 10 × 10 × 10 × 10).

</details>

<details class="dl-answer"><summary>one way through it</summary>

side(2 × 100 × 100) = 100 × side(2) = 141.421356…. The digits are the
digits of side(2), with the point moved two places. The machine in
problem 7, with `area = 20000`, finds the same digits. With shapes,
side(2 × ♡ × ♡ × ♡ × ♡) = ♡ × ♡ × side(2). With letters, it is
k × k × side(2).

</details>

## 12. From earlier: square numbers

From *Undoing a square: square roots, the side of a square*.

```question
id: from-earlier-square-numbers-1
type: fill-in-the-blank

side(144) = {12|72|14}

edge(125) = {5|25|41}
```

## 13. The usual way to write it

The tutorial showed the sign: $\sqrt{2}$ means side(2), and
$\sqrt{8} = 2\sqrt{2}$. A number like $\sqrt{2}$, whose digits never
end and never repeat, is a *surd*.

```question
id: the-usual-way-to-write-it-1
type: fill-in-the-blank

√18 = {3√2|9√2|6√2}

√50 = {5√2|25√2|10√2}

Of √9, √10 and √16, the surd is {√10|√9|√16}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write each one with side(…): √18 is side(18).
2. Use what you found in problems 6 and 7.
3. For the surd: which of 9, 10 and 16 is not a square number?

**Think about:** you can always write side(…) first, then the sign.

**Try this next:** √32.

</details>

## 14. Five of your own

Can you make five problems of your own, and find each answer? Here are
some ideas:

- the side of a tilted square in a grid 20 by 20
- side(2 × ♡ × ♡) with a big number for the heart
- side(3) or side(7), to 10 places, with the machine
- a fraction that, times itself, is very close to 3

Which of your problems looks scary, but is simple?
