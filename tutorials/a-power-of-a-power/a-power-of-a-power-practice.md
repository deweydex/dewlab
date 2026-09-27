---
title: "A power of a power: stacks of stacks — Practice"
practice_for: a-power-of-a-power
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# A power of a power: stacks of stacks — Practice

Small problems on one idea. A power of a power is boxes of hearts:
(♡²)³ is 3 boxes of 2 hearts, so it is ♡⁶. Try each problem before you
open anything under it. Choose numbers, shapes or letters in the box
under the title.

## 1. Stacks of stacks

These come from the worksheet.

<div class="dl-world" data-world="numbers">

```question
id: stacks-of-stacks-1--numbers
type: fill-in-the-blank

(2²)³ is
{2⁶|2⁵|2⁸}.

(3⁵)² is
{3¹⁰|3⁷|3²⁵}.

(10¹⁰)⁴ is
{10⁴⁰|10¹⁴|10¹⁰⁰⁰⁰}.

(2¹⁰⁰)²⁰ is
{2²⁰⁰⁰|2¹²⁰|2²⁰⁰}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: stacks-of-stacks-1--squiggles
type: fill-in-the-blank

(♡²)³ is
{♡⁶|♡⁵|♡⁸}.

(△⁵)² is
{△¹⁰|△⁷|△²⁵}.

(□¹⁰)⁴ is
{□⁴⁰|□¹⁴|□¹⁰⁰⁰⁰}.

(★¹⁰⁰)²⁰ is
{★²⁰⁰⁰|★¹²⁰|★²⁰⁰}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: stacks-of-stacks-1--letters
type: fill-in-the-blank

(y²)³ is
{y⁶|y⁵|y⁸}.

(z⁵)² is
{z¹⁰|z⁷|z²⁵}.

(a¹⁰)⁴ is
{a⁴⁰|a¹⁴|a¹⁰⁰⁰⁰}.

(b¹⁰⁰)²⁰ is
{b²⁰⁰⁰|b¹²⁰|b²⁰⁰}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The exponent inside the brackets is the number in each box.
2. The exponent outside is the number of boxes.
3. Count them all: boxes times the number in each box.

**Think about:** 20 boxes of 100. Count in hundreds.

**Try this next:** (♡¹⁰⁰)¹⁰⁰.

</details>

## 2. Match three ways

A picture, some symbols and some words can show the same thing. Here is
the picture.

<img src="three-in-two-boxes.svg" alt="Two boxes side by side. Each box holds 3 hearts. Under the boxes, a label says: 2 boxes of 3 = 6.">

```question
id: match-three-ways-1
type: fill-in-the-blank

The picture shows
{(♡³)²|(♡²)³|♡³ × ♡²}.

In words, it is
{2 boxes of 3 hearts|3 boxes of 2 hearts|3 hearts and 2 hearts}.

As one power, it is
{♡⁶|♡⁵|♡⁹}.

(♡²)³ is a different picture, but it is
{the same amount|a different amount}.
```

## 3. Exponents you do not know

The worksheet has exponents we do not know.

<div class="dl-world" data-world="numbers">

Here are three powers of powers. Look at how they change.

$$\left(7^{10}\right)^2 \qquad \left(7^{11}\right)^2 \qquad \left(7^{12}\right)^2$$

```question
id: exponents-you-do-not-know-1--numbers
type: fill-in-the-blank

(7¹⁰)² is
{7²⁰|7¹²|7¹⁰⁰}.

(7¹¹)² is
{7²²|7¹³|7¹²¹}.

Each time the exponent inside goes up by 1, the answer's exponent goes
up by
{2|1|4}.
```

</div>

<div class="dl-world" data-world="squiggles">

$$\left(\heartsuit^{\triangle}\right)^2 \qquad \left(\triangle^3\right)^{\square} \qquad \left(\bigstar^{\heartsuit + 1}\right)^{\square}$$

```question
id: exponents-you-do-not-know-1--squiggles
type: fill-in-the-blank

The first one is
{♡^(2△)|♡^(△+2)|♡^(△²)}.

The second one is
{△^(3□)|△^(3+□)|△^(3^□)}.

The third one is
{★^(♡□+□)|★^(♡+1+□)|★^(♡□+1)}.
```

</div>

<div class="dl-world" data-world="letters">

$$\left(c^m\right)^2 \qquad \left(d^3\right)^n \qquad \left(n^{p+1}\right)^q$$

```question
id: exponents-you-do-not-know-1--letters
type: fill-in-the-blank

The first one is
{c^(2m)|c^(m+2)|c^(m²)}.

The second one is
{d^(3n)|d^(3+n)|d^(3ⁿ)}.

The third one is
{n^(pq+q)|n^(p+1+q)|n^(pq+1)}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Choose a number for the unknown exponent, like 4.
2. Find the power of a power with that number: boxes times the number
   in each box.
3. Now choose 5. What changed in the answer?

**Think about:** in the third one, each box holds $p + 1$. There are
$q$ boxes, so the count is $(p + 1) \times q$.

**Try this next:** $\left(\heartsuit^{\triangle}\right)^{\triangle}$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Multiply the two exponents. $\left(c^m\right)^2 = c^{2m}$, since 2
boxes of $m$ is $2m$. $\left(d^3\right)^n = d^{3n}$, since $n$ boxes of
3 is $3n$. For the third, $q$ boxes of $p + 1$ is $(p + 1) \times q$,
which is $pq + q$. So $\left(n^{p+1}\right)^q = n^{pq+q}$.

</details>

## 4. Joining, then stacking

These use two rules. Joining two stacks adds the exponents. Stacks of
stacks multiply them.

<div class="dl-world" data-world="numbers">

$$\left(2^2 \cdot 2^3\right)^2 \qquad \left(3^2 \cdot 3^4\right)^3 \qquad \left(10^{10}\right)^{10} \cdot \left(10^2\right)^2$$

```question
id: joining-then-stacking-1--numbers
type: fill-in-the-blank

The first one is
{2¹⁰|2⁷|2¹²}.

The second one is
{3¹⁸|3⁹|3²⁴}.

The third one is
{10¹⁰⁴|10¹⁰⁰|10²⁴}.
```

</div>

<div class="dl-world" data-world="squiggles">

$$\left(\heartsuit^2 \cdot \heartsuit^3\right)^2 \qquad \left(\triangle^{\square} \cdot \triangle^{\bigstar}\right)^{\heartsuit} \qquad \left(\bigstar^{10}\right)^{10} \cdot \left(\bigstar^2\right)^2$$

```question
id: joining-then-stacking-1--squiggles
type: fill-in-the-blank

The first one is
{♡¹⁰|♡⁷|♡¹²}.

The second one is
{△^((□+★)♡)|△^(□★♡)|△^(□+★+♡)}.

The third one is
{★¹⁰⁴|★¹⁰⁰|★²⁴}.
```

</div>

<div class="dl-world" data-world="letters">

$$\left(e^2 \cdot e^3\right)^2 \qquad \left(f^m \cdot f^n\right)^p \qquad \left(g^{10}\right)^{10} \cdot \left(g^2\right)^2$$

```question
id: joining-then-stacking-1--letters
type: fill-in-the-blank

The first one is
{e¹⁰|e⁷|e¹²}.

The second one is
{f^((m+n)p)|f^(mnp)|f^(m+n+p)}.

The third one is
{g¹⁰⁴|g¹⁰⁰|g²⁴}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start inside the brackets. Two powers multiplied together join into
   one stack: add their exponents.
2. Now there is one box, with an exponent outside. Multiply.
3. For the third one, find each power of a power first. Then join the
   two stacks.

**Think about:** which rule belongs to each step.

**Try this next:** $\left(\heartsuit \cdot \heartsuit^4\right)^3$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

With letters:

- $e^2 \cdot e^3 = e^5$, and $\left(e^5\right)^2 = e^{10}$.
- $f^m \cdot f^n = f^{m+n}$, and $p$ boxes of that is $f^{(m+n)p}$.
- $\left(g^{10}\right)^{10} = g^{100}$ and $\left(g^2\right)^2 = g^4$.
  Joined, they make $g^{104}$.

With numbers, the first one is $2^{10}$, which is 1024.

</details>

## 5. Two kinds in one box

When a box holds two kinds, the exponent outside reaches both.

<div class="dl-world" data-world="numbers">

$$\left(\left(2^2 \cdot 3^3\right)^2\right)^2 \qquad \left(2^4 \cdot 5^3\right)^2$$

```question
id: two-kinds-in-one-box-1--numbers
type: fill-in-the-blank

The first one is
{2⁸ · 3¹²|2⁸ · 3³|2⁴ · 3⁶}.

The second one is
{2⁸ · 5⁶|2⁸ · 5³|2⁶ · 5⁵}.
```

</div>

<div class="dl-world" data-world="squiggles">

$$\left(\left(\heartsuit^2 \triangle^3\right)^2\right)^2 \qquad \left(\heartsuit^{\square} \triangle^{\bigstar}\right)^2$$

```question
id: two-kinds-in-one-box-1--squiggles
type: fill-in-the-blank

The first one is
{♡⁸△¹²|♡⁸△³|♡⁴△⁶}.

The second one is
{♡^(2□) △^(2★)|♡^(2□) △^★|♡^(□+2) △^(★+2)}.
```

</div>

<div class="dl-world" data-world="letters">

$$\left(\left(i^2 j^3\right)^2\right)^2 \qquad \left(k^m r^n\right)^2$$

```question
id: two-kinds-in-one-box-1--letters
type: fill-in-the-blank

The first one is
{i⁸j¹²|i⁸j³|i⁴j⁶}.

The second one is
{k^(2m) r^(2n)|k^(2m) rⁿ|k^(m+2) r^(n+2)}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the inside box the long way, once.
2. The exponent outside says how many of those boxes there are.
3. Count each kind on its own.

**Think about:** in the first one, there are boxes inside boxes. Start
with the inside brackets.

**Try this next:** $\left(\heartsuit \triangle\right)^5$.

</details>

## 6. Boxes inside boxes

From the worksheet. Find the inside brackets first. Then find the next
brackets, one at a time.

<div class="dl-world" data-world="numbers">

$$\left(\left(2^2\right)^3\right)^4 \qquad \left(\left(10^4\right)^2 \left(10^3\right)^2\right)^2$$

```question
id: boxes-inside-boxes-1--numbers
type: fill-in-the-blank

The first one is
{2²⁴|2⁹|2¹⁴}.

The second one is
{10²⁸|10¹⁴|10⁴⁸}.
```

</div>

<div class="dl-world" data-world="squiggles">

$$\left(\left(\heartsuit^2\right)^3\right)^4 \qquad \left(\left(\triangle^4\right)^2 \left(\triangle^3\right)^2\right)^2$$

```question
id: boxes-inside-boxes-1--squiggles
type: fill-in-the-blank

The first one is
{♡²⁴|♡⁹|♡¹⁴}.

The second one is
{△²⁸|△¹⁴|△⁴⁸}.
```

</div>

<div class="dl-world" data-world="letters">

$$\left(\left(h^2\right)^3\right)^4 \qquad \left(\left(m^4\right)^2 \left(m^3\right)^2\right)^2$$

```question
id: boxes-inside-boxes-1--letters
type: fill-in-the-blank

The first one is
{h²⁴|h⁹|h¹⁴}.

The second one is
{m²⁸|m¹⁴|m⁴⁸}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. In the first one, find the inside power of a power: $\left(h^2\right)^3$.
2. That answer is one box. Now there are 4 of those boxes.
3. In the second one, find the two inside powers first. Join them into
   one stack. Then use the last exponent.

**Think about:** each new bracket multiplies again.

**Try this next:** the worksheet asks about very deep boxes. What is
$\left(\left(\left(v^2\right)^3\right)^4\right)^5$?

</details>

<details class="dl-answer"><summary>one way through it</summary>

- $\left(h^2\right)^3 = h^6$, and $\left(h^6\right)^4 = h^{24}$. That is
  $2 \times 3 \times 4$.
- $\left(m^4\right)^2 = m^8$ and $\left(m^3\right)^2 = m^6$. Joined,
  they make $m^{14}$. Then $\left(m^{14}\right)^2 = m^{28}$.

One more box around the first one, with exponent 5, makes $2 \times 3
\times 4 \times 5 = 120$.

</details>

## 7. A negative base

From the worksheet: what is $\left(\left(-2\right)^2\right)^3$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The base is −2. Find $(-2)^2$ first: $-2 \times -2$.
2. Now find that number to the power 3.
3. Or count: 3 boxes of 2 is a power of 6.

**Think about:** a negative times a negative is positive.

**Try this next:** $\left(\left(-2\right)^3\right)^1$. Is it positive
or negative?

</details>

<details class="dl-answer"><summary>one way through it</summary>

$(-2)^2 = 4$, and $4^3 = 64$. By counting, it is $(-2)^6$, which is
also 64. Six negatives multiplied together make a positive number.

</details>

You can check it here. Keep the brackets round −2. Without them,
Python finds `2 ** 2` first, and puts the minus sign in front
afterwards.

```python exec
id: a-negative-base-1
print(((-2) ** 2) ** 3)
print((-2) ** 6)
print(-2 ** 2)
```

## 8. A fraction for a base

From the worksheet: what is $\left(\left(\frac{1}{2}\right)^3\right)^4$?
Think of the folded paper.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. There are 4 boxes, with 3 in each box. Multiply the exponents.
2. So it is $\left(\frac{1}{2}\right)$ to the power 12.
3. That is the paper folded 12 times. How many pieces is that?

**Think about:** $2^{10}$ is 1024. Two more folds double it twice.

**Try this next:** $\left(\left(\frac{1}{10}\right)^2\right)^3$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$$\left(\left(\frac{1}{2}\right)^3\right)^4 = \left(\frac{1}{2}\right)^{12} = \frac{1}{4096}$$

Folded 12 times, the paper is in 4096 pieces. Each piece is
$\frac{1}{4096}$ of the sheet.

</details>

## 9. Two paths, one answer

From the worksheet: $\left(u^2 \cdot u^5\right)^2$. Can you find it in
two different ways?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. First path: join the two stacks inside the brackets. Then use the
   exponent outside.
2. Second path: the box is $u^2 \cdot u^5$. Write the box twice, and
   join all four stacks.
3. Compare the two answers.

**Think about:** why the two paths must agree.

**Try this next:** $\left(\heartsuit \cdot \heartsuit^3\right)^3$, in
two ways.

</details>

<details class="dl-answer"><summary>one way through it</summary>

First path: $u^2 \cdot u^5 = u^7$, and $\left(u^7\right)^2 = u^{14}$.

Second path: $\left(u^2 \cdot u^5\right) \cdot \left(u^2 \cdot
u^5\right) = u^{2 + 5 + 2 + 5} = u^{14}$.

Both paths give $u^{14}$. They are two ways to count the same hearts.

</details>

## 10. What went differently here?

Somebody found $\left(2^3\right)^2$ like this. "The exponents are 3 and
2. $3 + 2 = 5$. So the answer is $2^5$, which is 32." Is
$\left(2^3\right)^2$ the same amount as 32?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find $2^3$ first.
2. Square that number: multiply it by itself.
3. Compare your answer with 32.

**Think about:** how many boxes, and how many in each box.

**Try this next:** when is adding the exponents the thing to do?

</details>

<details class="dl-answer"><summary>one way through it</summary>

No. $2^3 = 8$, and $8^2 = 64$. That is $2^6$: 2 boxes of 3 twos.
Adding the exponents is the rule for joining two stacks, like $2^3
\times 2^2$. The two rules look alike, so many people mix them. Here is
one answer. Yours may be different and work too.

</details>

## 11. From earlier: a negative power in a box

From *Negative powers: more on the bottom*. This one is a stretch. What
is $\left(2^{-1}\right)^3$? Find it in two ways.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $2^{-1}$ is one over $2^1$. What fraction is that?
2. First way: multiply that fraction by itself 3 times.
3. Second way: multiply the exponents, −1 and 3.

**Think about:** $-1 \times 3$ is −3.

**Try this next:** $\left(10^{-2}\right)^3$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$2^{-1} = \frac{1}{2}$, and $\left(\frac{1}{2}\right)^3 = \frac{1}{8}$.
Multiplying the exponents gives $2^{-3} = \frac{1}{2^3} =
\frac{1}{8}$. Both ways give $\frac{1}{8}$.

</details>

## 12. From earlier: a million

From *Powers: the long way and the short way*. How many zeros does
$10^6$ have? Now write $10^6$ as a power of a power, in two different
ways.

<details class="dl-answer"><summary>one way through it</summary>

$10^6$ is 1,000,000: six zeros. It is $\left(10^2\right)^3$, three
hundreds multiplied together. It is also $\left(10^3\right)^2$, a thousand
multiplied by a thousand.

</details>

## 13. From earlier: a simpler name

From *Equivalent fractions: the same amount, different names*. What is
the simplest name for $\frac{16}{64}$?

<details class="dl-answer"><summary>one way through it</summary>

Divide the top and the bottom by 16: $\frac{16}{64} = \frac{1}{4}$.
With powers, 16 is $2^4$ and 64 is $\left(2^3\right)^2 = 2^6$. So the
fraction is $2^{4-6} = 2^{-2} = \frac{1}{4}$.

</details>

## 14. Five of your own

The worksheet ends each part like this: make five problems of your
own. Can you make five problems that all come to $\heartsuit^{24}$?
Here are some ideas:

- boxes inside boxes inside boxes
- a letter in one of the exponents
- two kinds in one box
- a power of a power joined to another stack

Which of your five looks least like $\heartsuit^{24}$?
