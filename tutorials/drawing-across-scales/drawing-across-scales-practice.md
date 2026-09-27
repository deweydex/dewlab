---
title: "Log scales: drawing things that differ by millions — Practice"
practice_for: drawing-across-scales
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Log scales: drawing things that differ by millions — Practice

Small problems on one idea. On a normal scale, equal gaps are equal
amounts. On a hops scale, or log scale, equal gaps are equal hops of
×10. A number sits at its hops: hops(10 → the number), or
$\log_{10}$ of the number. Try each problem before you open anything
under it. Choose numbers, shapes or letters in the box under the
title.

<img src="planets-hops.svg" alt="The eight planets on a line marked 10, 100, 1,000 and 10,000, labelled millions of km from the Sun. The four marks are equally spaced. Every planet has its own label. Mercury sits between 10 and 100. Venus, Earth, Mars and Jupiter sit between 100 and 1,000. Saturn, Uranus and Neptune sit between 1,000 and 10,000.">

## 1. Same or different?

```question
id: same-or-different-1
type: multiple-choice
answer: 1

On a hops scale, which two gaps have the same length: 1 to 10, 10 to
100, or 100 to 200?

- 1 to 10, and 10 to 100
  - Each is one hop of ×10.
- 10 to 100, and 100 to 200
  - Each is +90 or +100 in amount. But 100 to 200 is only one hop of
    ×2, which is less than one hop of ×10.
- All three
  - On a normal scale, 10 to 100 and 100 to 200 would be close in
    length. On a hops scale, count the ×10 hops in each.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each gap, divide the bigger number by the smaller one.
2. A gap of ×10 is one hop.
3. Which gaps multiply by the same amount?

**Think about:** a hops scale cares about multiplying, not adding.

**Try this next:** on a hops scale, is 100 to 200 the same length as
1,000 to 2,000?

</details>

## 2. Normal or hops?

```question
id: normal-or-hops-1
type: fill-in-the-blank

A line marked 0, 5, 10, 15, 20 is
{a normal scale|a hops scale}.

A line marked 1, 10, 100, 1,000 is
{a hops scale|a normal scale}.

A line marked 1, 2, 4, 8, 16, with equal gaps, is
{a hops scale, with hops of ×2|a normal scale}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the first two marks. What takes the first to the second?
2. Is it adding, or multiplying?
3. Check that the next marks follow the same change.

**Think about:** a normal scale adds the same amount at each mark. A
hops scale multiplies.

**Try this next:** a line marked 0.1, 1, 10, 100. Normal or hops?

</details>

## 3. Continue the marks

These are the marks on a hops scale, with equal gaps between them.

<div class="dl-world" data-world="numbers">

```question
id: continue-the-marks-1--numbers
type: fill-in-the-blank

1, 3, 9. The next mark is
{27|12|18}.

The mark one gap to the left of 1 is
{1/3|0|−3}.
```

</div>

<div class="dl-world" data-world="squiggles">

Here △ is a number bigger than 1.

```question
id: continue-the-marks-1--squiggles
type: fill-in-the-blank

1, △, △ × △. The next mark is
{△ × △ × △|△ × △ + △|3 × △}.

The mark one gap to the left of 1 is
{1/△|0|−△}.
```

</div>

<div class="dl-world" data-world="letters">

Here b is a number bigger than 1.

```question
id: continue-the-marks-1--letters
type: fill-in-the-blank

1, b, b². The next mark is
{b³|b² + b|3b}.

The mark one gap to the left of 1 is
{1/b|0|−b}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find what each mark is multiplied by to get the next one.
2. Multiply once more for the next mark.
3. To go one gap to the left, do the opposite: divide.

**Think about:** on a hops scale, going left divides, and dividing
never reaches 0.

**Try this next:** the mark two gaps to the left of 1.

</details>

## 4. Where on the line?

Here are two lines from 100 to 1,000. One is a normal scale. The other
is a hops scale. Where does 500 sit on each?

```question
id: where-on-the-line-1
type: fill-in-the-blank

On the normal scale, 500 is closer to
{100|1,000}.

On the hops scale, 500 is closer to
{1,000|100}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. On the normal scale, 500 − 100 is 400, and 1,000 − 500 is 500.
2. On the hops scale, 500 is 100 × 5, and 1,000 is 500 × 2.
3. Which is the bigger multiplying: the ×5 from 100, or the ×2 to
   1,000?

**Think about:** on a hops scale, the gap from 100 to 500 is ×5. The
gap from 500 to 1,000 is only ×2.

**Try this next:** on the hops scale, is 200 closer to 100 or to
1,000?

</details>

<details class="dl-answer"><summary>one way through it</summary>

On the normal scale, 500 is 400 from 100 and 500 from 1,000, so it is
a little closer to 100. On the hops scale, 100 to 500 is ×5, and 500 to
1,000 is only ×2. So 500 is closer to 1,000. In Python,
`math.log10(500)` is about 2.70: much nearer to 3 hops than to 2.

</details>

## 5. Halfway on a hops line

This is a stretch. On a hops line, what number sits exactly halfway
between 10 and 100?

```question
id: halfway-on-a-hops-line-1
type: multiple-choice
answer: 2

Which number sits halfway between 10 and 100, on a hops line?

- 55
  - 55 is halfway on a normal line, because it is 45 more than 10 and
    45 less than 100.
- About 32
  - Half a hop of ×10 multiplies by halfway(10), about 3.16. And
    10 × 3.16 is about 32.
- 50
  - 50 is a round number near the middle of a normal line.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. From 10 to 100 is one hop of ×10.
2. Halfway is half a hop. Two half hops make one hop of ×10.
3. From *Halfway powers: fractional exponents, two half steps make
   one*: what number, done twice, multiplies by 10?

**Think about:** halfway(10) × halfway(10) is 10.

**Try this next:** what number sits halfway between 1 and 100 on a
hops line?

</details>

<details class="dl-answer"><summary>one way through it</summary>

Half a hop of ×10 is a multiplying that, done twice, gives ×10. That is
halfway(10), or $\sqrt{10}$, about 3.16. So the halfway number is
10 × 3.16, which is about 31.6. Python's `math.log10(31.6)` prints
about 1.5: one and a half hops.

</details>

## 6. Match three ways

<div class="dl-world" data-world="numbers">

```question
id: match-three-ways-1--numbers
type: multiple-choice
answer: 1

Which sentence says the same thing as hops(10 → 1,000,000) = 6?

- On a hops line, 1,000,000 sits 6 gaps to the right of 1
  - Each gap is one hop of ×10, and six hops land on 1,000,000.
- On a normal line, 1,000,000 sits 6 gaps to the right of 0
  - On a normal line, each gap is the same amount. 6 gaps would need
    each gap to be about 166,667.
- 1,000,000 ÷ 10 is 6
  - 1,000,000 ÷ 10 is 100,000. That is one hop back.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: match-three-ways-1--squiggles
type: multiple-choice
answer: 1

Which sentence says the same thing as hops(10 → $10^{\bigstar}$) = ★?

- On a hops line, $10^{\bigstar}$ sits ★ gaps to the right of 1
  - Each gap is one hop of ×10, and ★ hops land on $10^{\bigstar}$.
- On a hops line, $10^{\bigstar}$ sits 10 gaps to the right of 1
  - The 10 is the size of each hop. The exponent counts the hops.
- $10^{\bigstar}$ is 10 × ★
  - That adds ★ tens. A power multiplies tens.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: match-three-ways-1--letters
type: multiple-choice
answer: 1

Which sentence says the same thing as hops(10 → $10^{k}$) = k?

- On a hops line, $10^{k}$ sits k gaps to the right of 1
  - Each gap is one hop of ×10, and k hops land on $10^{k}$.
- On a hops line, $10^{k}$ sits 10 gaps to the right of 1
  - The 10 is the size of each hop. The exponent counts the hops.
- $10^{k}$ is 10k
  - 10k adds k tens. A power multiplies tens.
```

</div>

## 7. What went differently here?

Here is a worked problem, with one step that went differently.

> A hops line has the marks 0.01, 0.1, 1, 10 and 100. At its left end,
> one gap before 0.01, is the mark 0.

What went differently? What would the mark one gap before 0.01 be?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Going one gap to the left divides by 10.
2. What is 0.01 ÷ 10?
3. Is the answer 0? Can dividing by 10 ever give 0?

**Think about:** the halving pattern in *Graphs: a pattern as dots, a
line or a curve* came closer and closer to 0, and never reached it.

**Try this next:** how many gaps to the left of 1 is 0.000001?

</details>

<details class="dl-answer"><summary>one way through it</summary>

One gap before 0.01 is 0.01 ÷ 10, which is 0.001. The gap before that
is 0.0001. The marks get smaller and smaller, but no mark is ever 0. So
0 has no place on a hops line. The worked problem gave 0 a place, one
gap before 0.01.

</details>

## 8. Two paths, one answer

How many hops of ×10 go from 0.001 to 1,000?

- First path: count the gaps from 0.001 up to 1, then from 1 up to
  1,000.
- Second path: divide 1,000 by 0.001, and count the zeros.

```question
id: two-paths-one-answer-1
type: fill-in-the-blank

From 0.001 up to 1 is
{3|−3|1,000}
hops.

From 1 up to 1,000 is
{3|1,000|4}
hops.

1,000 ÷ 0.001 is 1,000,000, which has
{6|3|9}
zeros.
```

<details class="dl-answer"><summary>one way through it</summary>

0.001, 0.01, 0.1, 1 is 3 hops. 1, 10, 100, 1,000 is 3 more hops. That
makes 6. And 1,000 ÷ 0.001 is 1,000,000, with 6 zeros. Both paths give
6 hops.

</details>

## 9. Looks scary, is simple

<div class="dl-world" data-world="numbers">

```question
id: looks-scary-is-simple-1--numbers
type: fill-in-the-blank

From $10^\bgroup -12\egroup$ up to $10^\bgroup 12\egroup$ is
{24|0|12}
hops of ×10.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: looks-scary-is-simple-1--squiggles
type: fill-in-the-blank

From $10^\bgroup -\heartsuit\egroup$ up to $10^\bgroup \heartsuit\egroup$ is
{2 × ♡|0|♡}
hops of ×10.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: looks-scary-is-simple-1--letters
type: fill-in-the-blank

From $10^\bgroup -n\egroup$ up to $10^\bgroup n\egroup$ is
{2n|0|n}
hops of ×10.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Where is 1 on the hops line? It is at 0 hops.
2. How many hops from the small number up to 1?
3. How many hops from 1 up to the big number? Add the two.

**Think about:** a negative exponent sits to the left of 1, as many
gaps as the exponent says.

**Try this next:** from $10^{-7}$, a virus, up to $10^{27}$, about the
size of the universe.

</details>

## 10. Voyager, in Earths

Voyager 1 is a *space probe*: a machine sent into space, with no
people on board. On 18 November 2026, NASA says it will be
25.902 billion km from the Earth. The Earth is 12,756 km across. How
many Earths, side by side, would reach Voyager 1? And how many hops of
×10 is that?

The cell finds both. `import math` gets Python's maths tools ready.

```python exec
id: voyager-in-earths-1
import math

earths = 25902000000 / 12756
print(earths)
print(math.log10(earths))
```

```predict
type: choice

Before you run it: about how many hops of ×10 is it from one Earth
width to Voyager 1?

- Between 6 and 7
- Between 2 and 3
  - Two or three hops would be a few hundred Earths. Voyager 1 is much
    further than that.
- Between 20 and 30
  - From a virus to the whole universe is about 34 hops. Voyager 1 is
    far, but not that far.
```

<details class="dl-answer"><summary>one way through it</summary>

The first line prints about 2,030,574: about two million Earths. The
second prints about 6.31. So Voyager 1 is between 6 and 7 hops of ×10
from one Earth width.

</details>

## 11. From earlier: doubling on a hops scale

From *Graphs: a pattern as dots, a line or a curve*. The doubling
pattern 2, 4, 8, 16, … makes a curve on a normal scale. What shape
does it make when the up scale is a hops scale?

```python exec
id: doubling-on-a-hops-scale-1
import matplotlib.pyplot as plt

steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
doubling = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

plt.plot(steps, doubling, "o")
plt.yscale("log")
```

The first line, `import`, gets Python's drawing tools ready.
`plt.yscale("log")` makes the up scale a hops scale.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Each step of the doubling pattern multiplies by 2.
2. On a hops scale, equal multiplying makes equal gaps.
3. So how far does each dot climb above the one before?

**Think about:** on the page before, equal climbs made a straight line.

**Try this next:** what shape does the adding pattern 2, 4, 6, 8, 10
make on a hops scale?

</details>

<details class="dl-answer"><summary>one way through it</summary>

The dots make a straight line. Each step multiplies by 2, so each dot
climbs the same amount on a hops scale: hops(10 → 2), about 0.3 of a
hop of ×10. A pattern that multiplies becomes a straight line on a
hops scale.

</details>

## 12. From earlier: to the left of 1

From *Negative powers: more on the bottom*. What is $10^{-3}$ as a
fraction? Where does it sit on a hops line?

<details class="dl-answer"><summary>answer</summary>

$10^{-3} = \frac{1}{10^3} = \frac{1}{1000}$, which is 0.001. It sits 3
gaps to the left of 1.

</details>

## 13. From earlier: counting digits

From *Counting hops: logarithms, how many times did we multiply?*.
Neptune is 4515 million km from the Sun. How many digits does 4515
have? So hops(10 → 4515) is between which two whole numbers?

<details class="dl-answer"><summary>answer</summary>

4515 has 4 digits, so hops(10 → 4515) is between 3 and 4. It is about
3.65. On the planets' hops line, Neptune sits between the 1,000 mark
and the 10,000 mark.

</details>

## 14. Five of your own

Can you make five hops problems of your own? Here are some ideas:

- two things of very different sizes, from a real source
- a number that sits halfway between two marks
- a number to the left of 1
- a pattern that makes a straight line on a hops scale
- a scale with hops of ×2

Which one would be hardest to draw on a normal scale?
