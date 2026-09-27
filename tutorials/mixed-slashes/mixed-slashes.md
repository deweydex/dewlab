---
title: "Mixed problems: fractions"
practice_across:
  - one-whole-many-slices
  - same-amount-different-names
  - which-is-bigger
  - adding-slices
  - taking-slices-away
  - a-fraction-of-a-fraction
  - how-many-fit
  - fractions-with-holes
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Mixed problems: fractions

These problems use all the pages on fractions. They are mixed on
purpose. A problem does not say which page it comes from. It does not
say which move it needs, either. Choosing the move is part of the
problem. You can add, take away, multiply, divide, or give a fraction a
new name.

Try each problem before you open anything under it. There is no hurry,
and no score. Under most problems, "stuck? here are some steps" says
which page the idea comes from. Some problems come with numbers, shapes
or letters. Choose the way you like in the box under the title.

## A machine that checks

Python has a tool for fractions, called `Fraction`. The first line
below gets it ready. The next four lines add, take away, multiply and
divide the same two fractions. In Python, the times sign is `*`, and
the sign for dividing is `/`.

```python exec
id: a-machine-that-checks-1
from fractions import Fraction

print(Fraction(1, 2) + Fraction(1, 3))
print(Fraction(1, 2) - Fraction(1, 3))
print(Fraction(1, 2) * Fraction(1, 3))
print(Fraction(1, 2) / Fraction(1, 3))
```

You can change the numbers to check any problem on this page. Two of
the four lines print the same fraction. Try 1/3 and 1/4 in place of
1/2 and 1/3. Does it happen again?

## 1. Which move?

No working yet. Read each short story, and choose the move it needs. A
*recipe* is a list of what goes into a dish, and how much. Many recipes
measure milk in cups.

```question
id: which-move-1
type: fill-in-the-blank

You eat 1/4 of a pizza. Then you eat 1/3 of a pizza more. To find how
much you ate, we
{add|take away|multiply|divide}.

A recipe uses 3/4 of a cup of milk. You make half of the recipe. To
find the milk, we
{multiply|add|take away|divide}.

A bottle holds 2 litres. To find how many glasses of 1/4 litre it
fills, we
{divide|multiply|add|take away}.

There was 5/6 of a pizza on a plate. You ate 1/3 of a pizza. To find
what is on the plate now, we
{take away|divide|multiply|add}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The four stories use the ideas from *Adding fractions: putting
   slices together*, *Subtracting fractions: taking slices away*,
   *Multiplying fractions: a fraction of a fraction* and *Dividing
   fractions: how many fit?*
2. Ask what each story wants at the end. Is it more, less, a part of
   something, or a count?
3. More in total is adding. Less, after some is eaten, is taking away.
   Half of something is multiplying. A count of how many fit is
   dividing.

**Think about:** in the second story, is the milk more than 3/4 of a
cup, or less?

**Try this next:** write a story of your own for each of the four
moves.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Add, multiply, divide, and take away. If you want more, find each
amount too:

- $\frac{1}{4} + \frac{1}{3} = \frac{7}{12}$ of a pizza.
- Half of $\frac{3}{4}$ is $\frac{1}{2} \times \frac{3}{4} = \frac{3}{8}$
  of a cup.
- $2 \div \frac{1}{4} = 8$ glasses.
- $\frac{5}{6} - \frac{1}{3} = \frac{1}{2}$ of a pizza.

</details>

## 2. The same, or different?

<div class="dl-world" data-world="numbers">

```question
id: same-or-different-1--numbers
type: fill-in-the-blank

1/3 × 1/2 and 1/3 ÷ 2 are
{the same amount|different amounts}.

1/3 ÷ 1/2 and 1/3 × 2 are
{the same amount|different amounts}.

1/3 × 1/2 and 1/3 ÷ 1/2 are
{different amounts|the same amount}.

2/6 and 1/3 are
{the same amount|different amounts}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: same-or-different-1--squiggles
type: fill-in-the-blank

1/♡ × 1/2 and 1/♡ ÷ 2 are
{the same amount|different amounts}.

1/♡ ÷ 1/2 and 1/♡ × 2 are
{the same amount|different amounts}.

1/♡ × 1/2 and 1/♡ ÷ 1/2 are
{different amounts|the same amount}.

2/(2 × ♡) and 1/♡ are
{the same amount|different amounts}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: same-or-different-1--letters
type: fill-in-the-blank

1/n × 1/2 and 1/n ÷ 2 are
{the same amount|different amounts}.

1/n ÷ 1/2 and 1/n × 2 are
{the same amount|different amounts}.

1/n × 1/2 and 1/n ÷ 1/2 are
{different amounts|the same amount}.

2/(2 × n) and 1/n are
{the same amount|different amounts}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. These use the ideas from *Multiplying fractions: a fraction of a
   fraction*, *Dividing fractions: how many fit?* and *Equivalent
   fractions: the same amount, different names*.
2. Sharing between 2 people gives each person half. So dividing by 2
   is the same as taking half.
3. Dividing by a fraction is multiplying by it turned over. What is
   1/2 turned over?

**Think about:** if there is a shape or a letter, choose a number for
it, like 5. Then find both amounts.

**Try this next:** are 1/3 ÷ 3 and 1/9 the same amount?

</details>

<details class="dl-answer"><summary>one way through it</summary>

With numbers: $\frac{1}{3} \times \frac{1}{2} = \frac{1}{6}$, and
$\frac{1}{3} \div 2 = \frac{1}{6}$ too. $\frac{1}{3} \div \frac{1}{2} =
\frac{1}{3} \times 2 = \frac{2}{3}$. So the third pair is
$\frac{1}{6}$ and $\frac{2}{3}$, which are different amounts. And
$\frac{2}{6}$ is $\frac{1}{3}$ with every slice cut in two.

</details>

## 3. Rice for more people

A recipe for 4 people uses 2/3 of a cup of rice. How much rice do you
need for 6 people? And how much for 2 people?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Dividing fractions: how many fit?* and
   *Multiplying fractions: a fraction of a fraction*.
2. Find the rice for one person first. The rice for 4 people is shared
   between 4.
3. Then multiply by the number of people.

**Think about:** 6 people need more than 4 people. So should the answer
be more than 2/3 of a cup, or less?

**Try this next:** how much rice for 10 people?

</details>

<details class="dl-answer"><summary>one way through it</summary>

One person needs $\frac{2}{3} \div 4 = \frac{2}{12} = \frac{1}{6}$ of a
cup. So 6 people need $6 \times \frac{1}{6} = 1$ cup, and 2 people need
$2 \times \frac{1}{6} = \frac{1}{3}$ of a cup.

There is a second path. 6 people is $\frac{6}{4} = \frac{3}{2}$ of the
recipe, and $\frac{3}{2} \times \frac{2}{3} = 1$. The two are partners,
so they make 1. And 2 people is half of the recipe:
$\frac{1}{2} \times \frac{2}{3} = \frac{1}{3}$.

</details>

## 4. Sharing what is left

3/4 of a pizza is left. Two friends share it, so each friend gets the
same amount. How much of a whole pizza does each friend get? Is that
more than a quarter of a pizza, or less?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Dividing fractions: how many fit?* and
   *Comparing fractions: which is bigger?*
2. Sharing between 2 is the same as taking half. Half of 3/4 is
   1/2 × 3/4.
3. Give a quarter a name in eighths. Then compare.

**Think about:** 3/4 is more than half a pizza. What is half of half a
pizza?

**Try this next:** 3/4 of a pizza, shared between 3 friends.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$\frac{3}{4} \div 2 = \frac{1}{2} \times \frac{3}{4} = \frac{3}{8}$ of
a pizza for each friend. A quarter is $\frac{2}{8}$. So each friend
gets more than a quarter, by one eighth.

</details>

## 5. Glasses of juice

A bottle holds 3/2 litres of juice. That is one and a half litres. A
glass holds 1/4 of a litre. How many glasses can you fill?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Dividing fractions: how many fit?* and
   *Equivalent fractions: the same amount, different names*.
2. The question asks how many quarters fit in 3/2.
3. Give 3/2 a name in quarters. Cut every half into 2.

**Think about:** a glass is less than a litre. So will the answer be
more than 3/2, or less?

**Try this next:** the same bottle, and glasses of 3/8 of a litre.

</details>

<details class="dl-answer"><summary>one way through it</summary>

6 glasses. Three halves are the same amount as six quarters, so six
quarter-litre glasses fit. With the rule:
$\frac{3}{2} \div \frac{1}{4} = \frac{3}{2} \times 4 = \frac{12}{2} = 6$.

</details>

## 6. Grass in the shade

Three quarters of a garden is grass. Two fifths of the grass is in the
*shade*, where the sun does not reach. What fraction of the whole
garden is grass in the shade?

Then, what fraction of the garden is grass in the sun? Can you find the
second answer in two ways?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Multiplying fractions: a fraction of a
   fraction* and *Subtracting fractions: taking slices away*.
2. "Two fifths of the grass" is a fraction of a fraction. Draw a
   square. Cut it into 4 columns for the quarters, and into 5 rows for
   the fifths.
3. For the sun, one path takes the shade away from all the grass.
   Another path asks what fraction of the grass is not in the shade.

**Think about:** the grass in the shade and the grass in the sun
together make all the grass.

**Try this next:** add your two answers. Do you get 3/4?

</details>

<details class="dl-answer"><summary>one way through it</summary>

In the shade: $\frac{2}{5} \times \frac{3}{4} = \frac{6}{20} =
\frac{3}{10}$ of the garden.

In the sun, path one: $\frac{3}{4} - \frac{3}{10} = \frac{15}{20} -
\frac{6}{20} = \frac{9}{20}$.

In the sun, path two: $\frac{3}{5}$ of the grass is not in the shade,
and $\frac{3}{5} \times \frac{3}{4} = \frac{9}{20}$.

The two paths meet at $\frac{9}{20}$ of the garden.

</details>

## 7. What went differently here?

Somebody wrote this:

$$\frac{2}{5} + \frac{1}{3} = \frac{3}{8}$$

Before you add anything, compare $\frac{3}{8}$ with $\frac{2}{5}$. Which
is bigger? What does that tell you about the sum?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Comparing fractions: which is bigger?* and
   *Adding fractions: putting slices together*.
2. Give 3/8 and 2/5 names with the same bottom number. 40 works for
   both.
3. Adding 1/3 of a pizza to 2/5 should give more than 2/5.

**Think about:** which part of the sum went differently, the tops or
the bottoms?

**Try this next:** find 2/5 + 1/3 in fifteenths.

</details>

<details class="dl-answer"><summary>one answer</summary>

$\frac{3}{8}$ is $\frac{15}{40}$, and $\frac{2}{5}$ is $\frac{16}{40}$.
So $\frac{3}{8}$ is less than $\frac{2}{5}$. But the sum started with
$\frac{2}{5}$ and added more pizza. So the answer must be more than
$\frac{2}{5}$.

The tops were added, and the bottoms were added too. Fifths and thirds
are different sizes, so first cut both into fifteenths:
$\frac{6}{15} + \frac{5}{15} = \frac{11}{15}$. Here is one answer.
Yours may be different and work too.

</details>

## 8. What went differently here?

Somebody found $\frac{2}{5} \times \frac{3}{4}$ in three steps.

1. The bottoms are different, so give both fractions the same bottom:
   $\frac{8}{20} \times \frac{15}{20}$.
2. Multiply the tops: $8 \times 15 = 120$.
3. Keep the bottom, 20. The answer is $\frac{120}{20}$, which is 6.

Two fractions smaller than 1 gave 6. Which step changed the amount?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Multiplying fractions: a fraction of a
   fraction* and *Adding fractions: putting slices together*.
2. Is 8/20 the same amount as 2/5? Is 15/20 the same amount as 3/4?
3. For a fraction of a fraction, what happens to the bottoms?

**Think about:** which move keeps the bottom number the same, and why
it does.

**Try this next:** find 2/5 × 3/4 without step 1.

</details>

<details class="dl-answer"><summary>one answer</summary>

Step 1 gives new names for the same amounts, so it changes nothing.
Step 3 changed the amount. Keeping the bottom is the move for adding:
slices of the same size keep their size. For a fraction of a fraction,
the bottoms multiply too.

$$\frac{8}{20} \times \frac{15}{20} = \frac{120}{400} = \frac{3}{10}$$

Without step 1, it is shorter: $\frac{2}{5} \times \frac{3}{4} =
\frac{6}{20} = \frac{3}{10}$. Here is one answer. Yours may be
different and work too.

</details>

## 9. What went differently here?

Somebody wanted to know how many halves fit in three quarters. They
wrote this:

$$\frac{3}{4} \div \frac{1}{2} = \frac{3}{4} \times \frac{1}{2} = \frac{3}{8}$$

Picture three quarters of a pizza. Does one whole half fit in it? What
does that say about $\frac{3}{8}$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Dividing fractions: how many fit?* and
   *Multiplying fractions: a fraction of a fraction*.
2. One half is 2/4. Take 2 quarters away from 3 quarters. What is left?
3. What part of a half is that last quarter?

**Think about:** when the ÷ became a ×, what else needed to change?

**Try this next:** how many halves fit in 5/4?

</details>

<details class="dl-answer"><summary>one answer</summary>

One half fits in three quarters, and a quarter is left. A quarter
is half of a half. So one and a half halves fit: $\frac{3}{2}$. The
answer $\frac{3}{8}$ is less than 1, but at least one whole half fits.

The ÷ became a ×, but $\frac{1}{2}$ was not turned over. So the line
found half of $\frac{3}{4}$, which is a different question. Turned
over, it is $\frac{3}{4} \times \frac{2}{1} = \frac{6}{4} =
\frac{3}{2}$. Here is one answer. Yours may be different and work too.

</details>

{{include: setup/zen-calm-check.md}}

## 10. One pair, four moves

Here are $\frac{1}{2}$ and $\frac{1}{10}$, with each of the four moves.
Do not find them exactly yet. Picture each one first.

```question
id: one-pair-four-moves-1
type: fill-in-the-blank

1/2 + 1/10 is
{closest to 1/2|closest to 0|closest to 1|much more than 1}.

1/2 − 1/10 is
{closest to 1/2|closest to 0|closest to 1|much more than 1}.

1/2 × 1/10 is
{closest to 0|closest to 1/2|closest to 1|much more than 1}.

1/2 ÷ 1/10 is
{much more than 1|closest to 0|closest to 1/2|closest to 1}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the four moves from the pages on adding, taking away,
   multiplying and dividing fractions. It uses the landmarks from
   *Comparing fractions: which is bigger?* too.
2. 1/10 is a thin slice. Adding it or taking it away changes one half
   only a little.
3. 1/2 × 1/10 is a tenth of a half. 1/2 ÷ 1/10 asks how many tenths fit
   in a half.

**Think about:** which two moves change one half a little, and which
two change it a lot.

**Try this next:** the same four moves with 1/2 and 1/100.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$\frac{1}{2} + \frac{1}{10} = \frac{3}{5}$ and $\frac{1}{2} -
\frac{1}{10} = \frac{2}{5}$. Both are one tenth from one half.
$\frac{1}{2} \times \frac{1}{10} = \frac{1}{20}$, which is very close
to 0. $\frac{1}{2} \div \frac{1}{10} = 5$: five tenths fit in a half.
The machine at the top of the page can check all four.

</details>

## 11. Three ways to make 1

<div class="dl-world" data-world="numbers">

```question
id: three-ways-to-make-1-1--numbers
type: fill-in-the-blank

In 2/3 + ? = 1, the gap is
{1/3|2/3|3/2}.

In 2/3 × ? = 1, the gap is
{3/2|1/3|2/3}.

In 2/3 ÷ ? = 1, the gap is
{2/3|3/2|1/3}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: three-ways-to-make-1-1--squiggles
type: fill-in-the-blank

In △/♡ + ? = 1, the gap is
{(♡ − △)/♡|△/♡|♡/△}.

In △/♡ × ? = 1, the gap is
{♡/△|△/♡|(♡ − △)/♡}.

In △/♡ ÷ ? = 1, the gap is
{△/♡|♡/△|1}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: three-ways-to-make-1-1--letters
type: fill-in-the-blank

In k/n + ? = 1, the gap is
{(n − k)/n|k/n|n/k}.

In k/n × ? = 1, the gap is
{n/k|k/n|(n − k)/n}.

In k/n ÷ ? = 1, the gap is
{k/n|n/k|1}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Fractions: one whole pizza, many slices*,
   *Adding fractions: putting slices together* and *Dividing fractions:
   how many fit?*
2. For +, count the slices that are missing from the whole pizza.
3. For ×, find the partner: the fraction turned over. For ÷, ask what
   fits exactly once.

**Think about:** three moves, three different gaps, and the same
answer, 1.

**Try this next:** fill the three gaps for 3/8.

</details>

## 12. Four moves, one slice

<div class="dl-world" data-world="numbers">

```question
id: four-moves-one-slice-1--numbers
type: fill-in-the-blank

1/5 + 1/5 is
{2/5|1/25|1|2/10}.

1/5 × 1/5 is
{1/25|2/5|1|1/10}.

1/5 ÷ 1/5 is
{1|1/25|2/5|0}.

1/5 − 1/5 is
{0|1|1/25|1/5}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: four-moves-one-slice-1--squiggles
type: fill-in-the-blank

1/♡ + 1/♡ is
{2/♡|1/(♡ × ♡)|1|2/(♡ + ♡)}.

1/♡ × 1/♡ is
{1/(♡ × ♡)|2/♡|1|1/(♡ + ♡)}.

1/♡ ÷ 1/♡ is
{1|1/(♡ × ♡)|2/♡|0}.

1/♡ − 1/♡ is
{0|1|1/(♡ × ♡)|1/♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: four-moves-one-slice-1--letters
type: fill-in-the-blank

1/n + 1/n is
{2/n|1/(n × n)|1|2/(n + n)}.

1/n × 1/n is
{1/(n × n)|2/n|1|1/(n + n)}.

1/n ÷ 1/n is
{1|1/(n × n)|2/n|0}.

1/n − 1/n is
{0|1|1/(n × n)|1/n}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Algebraic fractions: shapes and letters in
   fractions*, and the pages on adding, taking away, multiplying and
   dividing fractions.
2. Adding: two slices of the same size. Taking away: one slice, then
   the same slice gone.
3. Multiplying: a fifth of a fifth. Picture a square cut into 5 columns
   and 5 rows. Dividing: how many of these slices fit in one of them?

**Think about:** one slice, four moves, and four different answers.

**Try this next:** 1/5 + 1/5 + 1/5 + 1/5 + 1/5.

</details>

## 13. Looks scary, is simple

<div class="dl-world" data-world="numbers">

```question
id: looks-scary-1--numbers
type: fill-in-the-blank

(17/19 × 19/17) + (17/19 − 17/19) is
{1|0|17/19|2}.

(17/19 ÷ 17/19) × 3/4 is
{3/4|0|1}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: looks-scary-1--squiggles
type: fill-in-the-blank

(♡/△ × △/♡) + (♡/△ − ♡/△) is
{1|0|♡/△|2}.

(♡/△ ÷ ♡/△) × 3/4 is
{3/4|0|1}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: looks-scary-1--letters
type: fill-in-the-blank

(p/q × q/p) + (p/q − p/q) is
{1|0|p/q|2}.

(p/q ÷ p/q) × 3/4 is
{3/4|0|1}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Dividing fractions: how many fit?*,
   *Subtracting fractions: taking slices away* and *Fractions: one
   whole pizza, many slices*.
2. Find each bracket first. Do not multiply the big numbers.
3. A fraction times its partner is 1. A fraction divided by itself is 1.
   A fraction take away itself leaves nothing.

**Think about:** none of the answers depends on the numbers inside the
brackets.

**Try this next:** (♡/△ + ♡/△) ÷ ♡/△.

</details>

## 14. Walking for six days

Every day you walk 1/2 of a kilometre to the shop. Then you walk 1/3 of
a kilometre more to the bus. A kilometre (km) is 1000 metres. How far
do you walk in 6 days? Can you find it in two ways?

- **One day first.** Find how far you walk in one day. Then find 6
  days.
- **One walk at a time.** Find 6 days of walking to the shop, and 6
  days of walking to the bus. Then add.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Adding fractions: putting slices together*
   and *Multiplying fractions: a fraction of a fraction*.
2. For one day, the slices are halves and thirds. Sixths work for both.
3. For the second path, what is 6 × 1/2? What is 6 × 1/3?

**Think about:** which path had the easier numbers.

**Try this next:** how far do you walk in 12 days?

</details>

<details class="dl-answer"><summary>one way through it</summary>

One day first: $\frac{1}{2} + \frac{1}{3} = \frac{3}{6} + \frac{2}{6} =
\frac{5}{6}$ km. Then $6 \times \frac{5}{6} = \frac{30}{6} = 5$ km.

One walk at a time: $6 \times \frac{1}{2} = 3$ km to the shop, and
$6 \times \frac{1}{3} = 2$ km to the bus. That is $3 + 2 = 5$ km.

The two paths meet at 5 km.

</details>

## 15. Check it with numbers

<div class="dl-world" data-world="numbers">

Somebody wrote a quick way to take one slice from another:

$$\frac{1}{4} - \frac{1}{5} = \frac{5 - 4}{4 \times 5}$$

Do the two sides give the same amount? Does the same way work for
other numbers?

</div>

<div class="dl-world" data-world="squiggles">

Somebody wrote a rule for taking one slice from another:

$$\frac{1}{\heartsuit} - \frac{1}{\triangle} = \frac{\triangle - \heartsuit}{\heartsuit \times \triangle}$$

Choose numbers for the heart and the triangle. Do the two sides give
the same amount?

</div>

<div class="dl-world" data-world="letters">

Somebody wrote a rule for taking one slice from another:

$$\frac{1}{a} - \frac{1}{b} = \frac{b - a}{a \times b}$$

Choose numbers for $a$ and $b$. Do the two sides give the same amount?

</div>

The cell checks both sides. Python cannot use a ♡ as a name, so the
cell writes the words `heart` and `triangle`. The first line gets the
`Fraction` tool ready. Change the two numbers, and run it again.

```python exec
id: check-it-with-numbers-1
from fractions import Fraction

heart = 2
triangle = 3
print(Fraction(1, heart) - Fraction(1, triangle))
print(Fraction(triangle - heart, heart * triangle))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Algebraic fractions: shapes and letters in
   fractions* and *Subtracting fractions: taking slices away*.
2. With 2 and 3, the side before the = sign is 1/2 − 1/3. Cut both
   into sixths.
3. The side after the = sign is (3 − 2)/(2 × 3). Compare the two.

**Think about:** why cutting both pizzas into ♡ × △ slices makes the
rule work.

**Try this next:** write a rule of the same kind for 1/♡ + 1/△.

</details>

<details class="dl-answer"><summary>one way through it</summary>

With 2 and 3, both lines print 1/6. With 4 and 5, both sides are
$\frac{1}{20}$. The rule holds for every pair, except where a bottom
is 0. Cut both pizzas into $\heartsuit \times \triangle$ slices. Then
$\frac{1}{\heartsuit}$ is $\triangle$ small slices, and
$\frac{1}{\triangle}$ is $\heartsuit$ small slices. Take $\heartsuit$
slices away from $\triangle$ slices.

Try 3 for the heart and 2 for the triangle. Both lines print -1/6. We
take away more than we have, so the answer is below 0.

</details>

## 16. A stretch: water in a bottle

A water bottle is 3/4 full. You drink 2/3 of the water in it. How full
is the bottle now?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Multiplying fractions: a fraction of a
   fraction* and *Subtracting fractions: taking slices away*.
2. "2/3 of the water in it" is a fraction of a fraction: 2/3 of 3/4.
   How much of a full bottle did you drink?
3. Take that away from 3/4.

**Think about:** 2/3 of the water in the bottle is not 2/3 of a full
bottle.

**Try this next:** the bottle is 3/4 full, and you drink 2/3 of a full
bottle. How full is it now?

</details>

<details class="dl-answer"><summary>one way through it</summary>

You drank $\frac{2}{3} \times \frac{3}{4} = \frac{6}{12} = \frac{1}{2}$
of a full bottle. So the bottle is now $\frac{3}{4} - \frac{1}{2} =
\frac{3}{4} - \frac{2}{4} = \frac{1}{4}$ full.

A second path: you left $\frac{1}{3}$ of the water. And
$\frac{1}{3} \times \frac{3}{4} = \frac{3}{12} = \frac{1}{4}$. The two
paths meet. The bottle is a quarter full.

</details>

## 17. Slices to order

A pizza shop cuts every pizza into 6 equal slices, and it sells single
slices. You want 1/2 of a pizza. One friend wants 1/3 of a pizza.
Another friend wants 2/3 of a pizza. How many slices do you order in
total? How much pizza is that?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This uses the ideas from *Equivalent fractions: the same amount,
   different names*, *Adding fractions: putting slices together* and
   *Dividing fractions: how many fit?*
2. Give each fraction a name in sixths. The top of each new name is a
   number of slices.
3. Add the slices.

**Think about:** counting slices of the same size is what a common
denominator lets us do.

**Try this next:** another shop cuts every pizza into 8 slices. Can it
sell you exactly 1/3 of a pizza?

</details>

<details class="dl-answer"><summary>one way through it</summary>

In sixths, $\frac{1}{2} = \frac{3}{6}$, $\frac{1}{3} = \frac{2}{6}$ and
$\frac{2}{3} = \frac{4}{6}$. That is $3 + 2 + 4 = 9$ slices. Nine sixths
is $\frac{9}{6} = \frac{3}{2}$: one and a half pizzas.

Each count is a division too. $\frac{1}{2} \div \frac{1}{6} = 3$: three
slices of one sixth fit in a half.

</details>

{{include: setup/zen-calm-check.md}}

## 18. Five of your own

Can you make five fraction problems of your own, one for each move?
Make at least two of them stories, where the move is not named. Here
are some ideas:

- a recipe for more people, or for fewer
- something shared between friends
- how many small glasses fill a big bottle
- a part of a part, like the grass in the shade
- a problem that needs two moves, one after the other

Give one of your stories to somebody. Which move do they choose?

## Read more

Wikipedia's page on fractions has a section on [arithmetic with
fractions](https://en.wikipedia.org/wiki/Fraction#Arithmetic_with_fractions).
It shows adding, taking away, multiplying and dividing, one after
another.
