---
title: "The rules of powers: everything at once"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# The rules of powers: everything at once

Here is a line of maths. It looks scary. It has two stacks joined, a
power of a power and a division, all in one.

$$\frac{\heartsuit^3 \times \heartsuit^4}{\left(\heartsuit^2\right)^3}$$

Before any rule, we count hearts.

```question
id: count-the-hearts-1
type: fill-in-the-blank

The top is ♡³ × ♡⁴. Written the long way, it has
{7|12|3}
hearts.

The bottom is (♡²)³: 3 boxes, with 2 hearts in each. It has
{6|5|8}
hearts.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write ♡³ as ♡ × ♡ × ♡, and ♡⁴ as four hearts. Count them all.
2. Draw 3 boxes. Put ♡ × ♡ in each box.
3. Count every heart in the boxes.

**Think about:** the top is two stacks side by side. The bottom is
boxes of hearts.

**Try this next:** how many hearts are in (♡³)²?

</details>

## Cross out the pairs

Now the fraction is 7 hearts over 6 hearts:

$$\frac{\heartsuit \times \heartsuit \times \heartsuit \times \heartsuit \times \heartsuit \times \heartsuit \times \heartsuit}{\heartsuit \times \heartsuit \times \heartsuit \times \heartsuit \times \heartsuit \times \heartsuit}$$

Each heart on the bottom crosses out one heart on the top. Each pair is
♡/♡, which is 1.

```question
id: cross-out-the-pairs-1
type: multiple-choice
answer: 1

After we cross out every pair, what is left?

- ♡
  - 6 pairs cross out. One heart on the top has no partner.
- 1
  - That would need the same number of hearts on the top and on the
    bottom. The top has one more.
- 1/♡
  - That would need one more heart on the bottom. Here the top has
    more.
- ♡¹³
  - 7 + 6 = 13. The hearts on the bottom cross out hearts on the top.
    They do not join them.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put your finger on the first heart on the top, and the first heart
   on the bottom. That is one pair.
2. Keep pairing, one on the top with one on the bottom.
3. When the bottom has no hearts left, look at the top.

**Think about:** which side has more hearts.

**Try this next:** what is ♡⁸/♡⁶?

</details>

So the scary line is only ♡. We did it the long way: write every heart,
then cross out the pairs. The long way is slow, and it always works.

## The same, with the rules

The last five pages each found a rule. The rules are a shorter path to
the same place. This line needs three of them, one at a time.

```question
id: the-same-with-the-rules-1
type: fill-in-the-blank

The top, ♡³ × ♡⁴, joins two stacks. We
{add|multiply|subtract}
the exponents, and get ♡⁷.

The bottom, (♡²)³, is a power of a power. We
{multiply|add|subtract}
the exponents, and get ♡⁶.

Then ♡⁷/♡⁶ crosses out pairs. We
{subtract|add|multiply}
the exponents, and get ♡¹, which is ♡.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Two stacks side by side join into one row. We count all their hearts.
2. Boxes of hearts: the number of boxes, times the hearts in each box.
3. Each heart on the bottom takes one heart away from the top.

**Think about:** the long way gave ♡ too. The two paths must agree.

**Try this next:** (♡² × ♡⁵)/(♡³)² with the rules.

</details>

Many problems look like this one. They mix many powers, and in the end
they are one short thing. We call them *looks scary, is
simple*.

## Five rules from five pages

Here are the five rules in one place. Each one came from counting
hearts, on its own page.

| The page | An example | What we do with the exponents |
|---|---|---|
| [Multiplying powers: joining two stacks](tutorial:joining-two-stacks) | $\heartsuit^3 \times \heartsuit^4 = \heartsuit^7$ | add them |
| [Dividing powers: crossing out pairs](tutorial:sharing-out) | $\heartsuit^5 / \heartsuit^2 = \heartsuit^3$ | subtract the bottom from the top |
| [The zero power: when everything cancels](tutorial:when-everything-cancels) | $\heartsuit^4 / \heartsuit^4 = \heartsuit^0 = 1$ | subtract, and get 0 |
| [Negative powers: more on the bottom](tutorial:more-on-the-bottom) | $\heartsuit^2 / \heartsuit^5 = \heartsuit^{-3} = \frac{1}{\heartsuit^3}$ | subtract, and get a negative |
| [A power of a power: stacks of stacks](tutorial:a-power-of-a-power) | $\left(\heartsuit^2\right)^3 = \heartsuit^6$ | multiply them |

```question
id: five-rules-1
type: fill-in-the-blank

For (★⁴)⁵, we
{multiply|add|subtract}
the exponents.

For ★⁴ × ★⁵, we
{add|multiply|subtract}
the exponents.

For ★⁹/★⁴, we
{subtract|add|multiply}
the exponents.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Brackets with an exponent outside are boxes of stars.
2. A × between two stacks joins them into one row.
3. A line for dividing means crossing out pairs.

**Think about:** what the sign between the two powers is: ×, a
division line, or brackets.

**Try this next:** which rule does (★⁴)⁵ × ★ need, after the first
one?

</details>

## Two paths, one answer

Here is a second scary one:

$$\left(\frac{\triangle^5}{\triangle^5}\right)^{100}$$

We can start inside the brackets. Or we can use a rule first. Here are
both paths.

```question
id: two-paths-one-answer-1
type: fill-in-the-blank

First path, the inside first. △⁵/△⁵ is
{1|0|△}.

So the whole thing is 1¹⁰⁰, which is
{1|100|0}.

Second path, a rule first. △⁵/△⁵ is △ to the power
{0|1|10}.

Then (△⁰)¹⁰⁰ is △ to the power 0 × 100, which is △⁰, which is
{1|0|△}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A fraction with the same top and bottom is 1, like 4/4 of a pizza.
2. 1¹⁰⁰ is 1 × 1 × 1 × … a hundred times.
3. For the second path, subtract the exponents: 5 − 5.

**Think about:** a power of a power multiplies the exponents. What is
0 times anything?

**Try this next:** (♡⁶/♡⁶)¹⁰⁰⁰, in both ways.

</details>

Both paths give 1. The hundred made it look scary. It did not change
anything.

{{include: setup/zen-calm-check.md}}

## Now with letters

Letters work the same way. Here is one:

$$\frac{\left(b^4\right)^2}{b^3 \times b^5}$$

```question
id: now-with-letters-1
type: fill-in-the-blank

The top, (b⁴)², is
{b⁸|b⁶|b¹⁶}.

The bottom, b³ × b⁵, is
{b⁸|b¹⁵|b²}.

So the whole thing is
{1|b|0}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The top is 2 boxes of 4. How many b's in total?
2. The bottom joins a stack of 3 and a stack of 5.
3. Compare the top and the bottom.

**Think about:** the top and the bottom are built in different ways.
Only their totals need to match.

**Try this next:** (c³)²/(c² × c⁴).

</details>

Like the heart, the letter b can be any number, and the pattern still
holds.

## Now with numbers

Here is the first scary line again, with 2 in place of the heart:

$$\frac{2^3 \times 2^4}{\left(2^2\right)^3}$$

The rules say it is $2^1$, which is 2. Python can check this. It is a
language for computers. In Python, `**` means a power, `*` means
times, and `/` means divide. Python finds what is in brackets first,
then the powers, then the times and divide, from left to right.

```python exec
id: now-with-numbers-1
print(2 ** 3 * 2 ** 4 / (2 ** 2) ** 3)
print(3 ** 3 * 3 ** 4 / (3 ** 2) ** 3)
print(10 ** 3 * 10 ** 4 / (10 ** 2) ** 3)
```

```predict
type: number

Before you run it: what number will the first line print?
```

The first line prints 2.0. Python writes the answer to a `/` division
with a decimal point, and 2.0 is the same number as 2. The second line
has 3 in place of 2, and prints 3.0. The last has 10, and prints 10.0.
Each time, the answer is the base. The squiggles said so: the answer
was ♡, whatever number the heart is.

## When you forget a rule

Somebody could not remember the rule for (♡³)². Is it ♡⁵, or ♡⁶? The
long way is there for exactly this.

```question
id: when-you-forget-a-rule-1
type: fill-in-the-blank

(♡³)² the long way is ♡³ × ♡³. That is
{♡ × ♡ × ♡ × ♡ × ♡ × ♡|♡ × ♡ × ♡ × ♡ × ♡|♡³ + ♡³}.

So (♡³)² is
{♡⁶|♡⁵|♡⁹}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The exponent 2 outside the brackets says: two boxes.
2. Each box is ♡³: three hearts.
3. Write both boxes out, and count every heart.

**Think about:** a number can check it too. (2³)² is 8 × 8.

**Try this next:** is (2³)² the same as 2⁵ or 2⁶? 2⁵ is 32 and 2⁶ is
64.

</details>

Nobody needs to remember the rules. When you forget one, write the
powers the long way and count. Or choose a small number, like 2, and
check. Both are safe paths back to the rule.

## Your turn

Choose numbers, shapes or letters in the box under the title.

<div class="dl-world" data-world="squiggles">

```question
id: your-turn-1--squiggles
type: fill-in-the-blank

(□⁶ × □²)/(□³)² is
{□²|□⁵|□}.

(★²)⁵/★¹⁰ is
{1|★|★⁻³}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: your-turn-1--letters
type: fill-in-the-blank

(x⁶ × x²)/(x³)² is
{x²|x⁵|x}.

(y²)⁵/y¹⁰ is
{1|y|y⁻³}.
```

</div>

<div class="dl-world" data-world="numbers">

```question
id: your-turn-1--numbers
type: fill-in-the-blank

(10⁶ × 10²)/(10³)² is
{100|100,000|10}.

(5²)⁵/5¹⁰ is
{1|5|0}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the top as one power. Then find the bottom as one power.
2. Now it is one power over one power. Subtract the exponents.
3. If you forget a rule, write it the long way.

**Think about:** in the second one, the top is boxes and the bottom is
one stack.

**Try this next:** (□⁴ × □⁴)/(□²)⁴.

</details>

## More on the bottom

This one leaves more on the bottom:

$$\frac{\left(\heartsuit^2\right)^3}{\heartsuit^4 \times \heartsuit^5}$$

```question
id: more-on-the-bottom-1
type: fill-in-the-blank

The top is
{♡⁶|♡⁵|♡⁸}.

The bottom is
{♡⁹|♡²⁰|♡¹}.

So the whole thing is ♡ to the power
{−3|3|15}.

That is the same as
{1/♡³|−♡³|♡³}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The top is 3 boxes of 2. The bottom joins 4 and 5.
2. Cross out the pairs. Which side has hearts left?
3. 6 − 9 is below zero. A negative power means one over the power.

**Think about:** three hearts are left on the bottom, under a 1.

**Try this next:** with 2 in place of the heart, the answer is 1/2³.
What fraction is that?

</details>

With 2 in place of the heart, this is $\frac{2^6}{2^9} = \frac{64}{512}$,
which is $\frac{1}{8}$. That is $\frac{1}{2^3}$.

## Two kinds at once

This step is a stretch. Here there are hearts and triangles:

$$\frac{\left(\heartsuit^3 \triangle^2\right)^2}{\heartsuit^5 \triangle^4}$$

```question
id: two-kinds-at-once-1
type: fill-in-the-blank

The top is two boxes of ♡³△². In total, it has ♡ to the power
{6|5|9}
and △ to the power
{4|2|3}.

After crossing out, the hearts leave
{♡|1|♡¹¹}.

The triangles leave
{1|△|△⁸}.

So the whole thing is
{♡|♡△|1}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the two boxes: ♡³△² × ♡³△².
2. Count the hearts, and then the triangles.
3. Hearts cross out with hearts, and triangles with triangles.

**Think about:** each kind of tile has its own pairs.

**Try this next:** (♡△²)³/(♡³△⁶).

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say in your own words how you find a
scary line of powers. Which rule comes first? What do you do when you
forget one? Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

Make the top one power, and the bottom one power. Joining stacks adds
the exponents. Boxes of stacks multiply them. Then one power over
another subtracts them. If the answer is 0, it is 1. If it is
negative, the hearts are on the bottom. The order can change, and the
answer stays the same. When you forget a rule, write it the long way,
or check with a small number. Your way of saying it may be clearer than
ours.

</details>

## Make your own

Can you make five scary lines of your own, each one simple in the end?
Try one that comes to 1, one that comes to ♡, and one with more on the
bottom. Try one with a very big exponent, and one with two kinds of
tile. Check each one with a number in Python.

## Looking back

On this page, the same line could be found in more than one order. Why
do the different paths always land in the same place?

A challenge: the program below checks the first scary line with many
numbers for the heart. Can you change it to check your own scary line?
What happens when the base is 0? Guess first, then add 0 to the list.

```python challenge
# Is (b³ × b⁴)/(b²)³ always b? Try many numbers for b.
for base in [2, 3, 5, 10]:
    print(base, base ** 3 * base ** 4 / (base ** 2) ** 3)
```

## Read more

Maths is Fun has a page on the [laws of
exponents](https://www.mathsisfun.com/algebra/exponent-laws.html). It
has every rule on this page, each written the long way first.
Wikipedia's page on
[exponentiation](https://en.wikipedia.org/wiki/Exponentiation#Identities_and_properties)
lists the rules for powers in a short table.
