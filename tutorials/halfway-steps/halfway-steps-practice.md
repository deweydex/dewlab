---
title: "Halfway powers: two half steps make one — Practice"
practice_for: halfway-steps
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Ordinary numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Halfway powers: two half steps make one — Practice

Small problems on one idea. halfway(♡) is the number that, multiplied
by itself, gives ♡. Many of these problems come from section 7 of a
Maths for IT worksheet. The worksheet writes them the usual way, with a
fraction as the exponent. Here, each one has its friendly name beside
it.

One rule helps with almost every problem. It comes from *Multiplying
powers: joining two stacks*. When we multiply two powers of the same
number, we add the exponents: $r^2 \times r^2 = r^{2+2} = r^4$.

Try each problem before you open anything under it. Choose numbers,
shapes or letters in the box under the title.

## 1. Same or different?

```question
id: same-or-different-1
type: multiple-choice
answer: 1

Three people found halfway(16). One wrote 4, one wrote 8, and one
wrote 2². Which answers are the same number?

- 4 and 2²
  - 2² is 2 × 2, which is 4. And 4 × 4 is 16.
- 4 and 8
  - 8 is half of 16. But 8 × 8 is 64, so 8 is a different number.
- All three
  - 2² and 4 are the same number. 8 is bigger than both.
```

## 2. Halfway of a power

<div class="dl-world" data-world="numbers">

```question
id: halfway-of-a-power-1--numbers
type: fill-in-the-blank

halfway(2⁴) is
{2²|2⁸|2}.

That is the number
{4|8|16}.

halfway(10⁶) is
{10³|10⁴|10¹²}.
```

<details class="dl-answer"><summary>one way through it</summary>

$2^2 \times 2^2 = 2^{2+2} = 2^4$. So halfway($2^4$) is $2^2$, which
is 4. In the same way, $10^3 \times 10^3 = 10^6$. So halfway of a
million is $10^3$, which is 1000.

</details>

</div>

<div class="dl-world" data-world="squiggles">

```question
id: halfway-of-a-power-1--squiggles
type: fill-in-the-blank

halfway(♡⁴) is
{♡²|♡⁸|2 × ♡}.

halfway(★¹⁶) is
{★⁸|★⁴|★³²}.
```

<details class="dl-answer"><summary>one way through it</summary>

$\heartsuit^2 \times \heartsuit^2 = \heartsuit^{2+2} = \heartsuit^4$.
So halfway($\heartsuit^4$) is $\heartsuit^2$. In the same way,
$\bigstar^8 \times \bigstar^8 = \bigstar^{16}$, so halfway($\bigstar^{16}$)
is $\bigstar^8$.

</details>

</div>

<div class="dl-world" data-world="letters">

The worksheet writes these as $(r^4)^{1/2}$ and $(u^{16})^{1/2}$.

```question
id: halfway-of-a-power-1--letters
type: fill-in-the-blank

halfway(r⁴) is
{r²|r⁸|2r}.

halfway(u¹⁶) is
{u⁸|u⁴|u³²}.
```

<details class="dl-answer"><summary>one way through it</summary>

$r^2 \times r^2 = r^{2+2} = r^4$. So halfway($r^4$) is $r^2$. In the
same way, $u^8 \times u^8 = u^{16}$, so halfway($u^{16}$) is $u^8$.

</details>

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. halfway asks: which number, multiplied by itself, gives this power?
2. Try a guess. Multiply it by itself, and add the two exponents.
3. Does the sum match the exponent in the question?

**Think about:** the exponent is cut into two equal parts.

**Try this next:** halfway of a power with exponent 10.

</details>

## 3. Continue the pattern

<div class="dl-world" data-world="numbers">

halfway($10^2$) is 10. halfway($10^4$) is 100. halfway($10^6$) is
1000.

```question
id: continue-the-pattern-1--numbers
type: fill-in-the-blank

The next one is halfway(10⁸), which is
{10⁴|10⁶|10¹⁶}.

That is the number
{10,000|100,000|1,000,000}.
```

</div>

<div class="dl-world" data-world="squiggles">

halfway($\heartsuit^2$) is $\heartsuit$. halfway($\heartsuit^4$) is
$\heartsuit^2$. halfway($\heartsuit^6$) is $\heartsuit^3$.

```question
id: continue-the-pattern-1--squiggles
type: multiple-choice
answer: 1

What is halfway($\heartsuit^{2 \times \triangle}$)?

- $\heartsuit^{\triangle}$
  - Two of them make $\heartsuit^{\triangle + \triangle}$, which is
    $\heartsuit^{2 \times \triangle}$.
- $\heartsuit^{2}$
  - Two of them make $\heartsuit^4$. That is only the same when
    $\triangle$ is 2.
- $\heartsuit^{4 \times \triangle}$
  - That doubles the exponent. Halfway cuts it in half.
```

</div>

<div class="dl-world" data-world="letters">

halfway($w^2$) is $w$. halfway($w^4$) is $w^2$. halfway($w^6$) is
$w^3$. The worksheet asks for $(w^{2n})^{1/2}$.

```question
id: continue-the-pattern-1--letters
type: multiple-choice
answer: 1

What is halfway($w^{2n}$)?

- $w^{n}$
  - Two of them make $w^{n + n}$, which is $w^{2n}$.
- $w^{2}$
  - Two of them make $w^4$. That is only the same when $n$ is 2.
- $w^{4n}$
  - That doubles the exponent. Halfway cuts it in half.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the exponents in the pattern: 2, 4, 6. Then look at the
   exponents of the answers: 1, 2, 3.
2. Each answer's exponent is half of the question's.
3. What is half of "2 times something"?

**Think about:** the pattern does not care which number is in the
exponent.

**Try this next:** halfway of a power with exponent 200.

</details>

## 4. An odd exponent

Some exponents do not split into two equal whole numbers. 9 is one of
them. This one looks scary, but the rule still works.

<div class="dl-world" data-world="numbers">

$2^9$ is 512. 22 × 22 is 484, and 23 × 23 is 529.

```question
id: an-odd-exponent-1--numbers
type: fill-in-the-blank

halfway(512) is between
{22 and 23|16 and 17|256 and 257}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: an-odd-exponent-1--squiggles
type: multiple-choice
answer: 1

What is halfway($\heartsuit^9$)?

- $\heartsuit^{9/2}$, which is $\heartsuit^{4.5}$
  - 4.5 + 4.5 is 9.
- $\heartsuit^3$
  - Three of these make $\heartsuit^9$. That is edge($\heartsuit^9$),
    not halfway.
- $\heartsuit^7$
  - 9 − 2 is 7. But two of these make $\heartsuit^{14}$.
```

```question
id: an-odd-exponent-2--squiggles
type: multiple-choice
answer: 1

And what is halfway($\heartsuit^{\triangle}$), for any number $\triangle$?

- $\heartsuit^{\triangle/2}$
  - Half of $\triangle$, added to half of $\triangle$, is $\triangle$.
- $\heartsuit^{\triangle - 2}$
  - That takes 2 away from the exponent. Halfway cuts it in half.
- $\heartsuit^{2 \times \triangle}$
  - That doubles the exponent. Halfway cuts it in half.
```

</div>

<div class="dl-world" data-world="letters">

The worksheet writes these as $(s^9)^{1/2}$ and $(v^m)^{1/2}$.

```question
id: an-odd-exponent-1--letters
type: multiple-choice
answer: 1

What is halfway($s^9$)?

- $s^{9/2}$, which is $s^{4.5}$
  - 4.5 + 4.5 is 9.
- $s^3$
  - Three of these make $s^9$. That is edge($s^9$), not halfway.
- $s^7$
  - 9 − 2 is 7. But two of these make $s^{14}$.
```

```question
id: an-odd-exponent-2--letters
type: multiple-choice
answer: 1

And what is halfway($v^m$), for any number $m$?

- $v^{m/2}$
  - Half of $m$, added to half of $m$, is $m$.
- $v^{m - 2}$
  - That takes 2 away from the exponent. Halfway cuts it in half.
- $v^{2m}$
  - That doubles the exponent. Halfway cuts it in half.
```

</div>

<details class="dl-answer"><summary>one way through it</summary>

Half of 9 is 4.5. Two of $s^{4.5}$ make $s^{4.5 + 4.5} = s^9$. So
halfway($s^9$) is $s^{4.5}$. We can also split it as
$s^4 \times$ halfway($s$), because $4 + \frac{1}{2}$ is 4.5.

With numbers: halfway(512) is $2^4 \times$ halfway(2), which is
16 × 1.414…, or about 22.6.

</details>

## 5. Three half steps

This one is from the worksheet too: $t^{3/2}$. The bottom of the
fraction, 2, says each step is a half step. The top, 3, says we take
three of them. So

$$t^{3/2} = \text{halfway}(t) \times \text{halfway}(t) \times \text{halfway}(t)$$

<div class="dl-world" data-world="numbers">

```question
id: three-half-steps-1--numbers
type: fill-in-the-blank

halfway(4) is 2. So three half steps of 4 are 2 × 2 × 2, which is
{8|6|12}.

halfway(9) is 3. So three half steps of 9 are
{27|13.5|18}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: three-half-steps-1--squiggles
type: multiple-choice
answer: 1

Two half steps make one whole step. What are three half steps of ♡?

- ♡ × halfway(♡)
  - The first two half steps make ♡. One half step is left.
- 3 × ♡ ÷ 2
  - That is one and a half hearts, added. Half steps multiply.
- ♡³ ÷ 2
  - That multiplies three whole hearts. These steps are halves.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: three-half-steps-1--letters
type: multiple-choice
answer: 1

Two half steps make one whole step. What is $t^{3/2}$?

- $t \times$ halfway($t$)
  - The first two half steps make $t$. One half step is left.
- $3t \div 2$
  - That is one and a half of $t$, added. Half steps multiply.
- $t^3 \div 2$
  - That multiplies three whole $t$s. These steps are halves.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the three half steps in a row.
2. Put a bracket round the first two. What do two half steps make?
3. What is left over?

**Think about:** the numbers world, where $4^{3/2}$ is 8. And 8 is
$4 \times 2$.

**Try this next:** five half steps of 4.

</details>

## 6. Thirds

A third step, done three times, makes one whole step. It is the edge of
a cube, edge(♡).

<div class="dl-world" data-world="numbers">

```question
id: thirds-1--numbers
type: fill-in-the-blank

2⁹ is 512. edge(512) is 2³, which is
{8|64|3}.

edge(10⁶) is
{10²|10³|10¹⁸}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: thirds-1--squiggles
type: fill-in-the-blank

edge(♡⁹) is
{♡³|♡⁶|♡²⁷}.

edge(★²⁷) is
{★⁹|★²⁴|★⁸¹}.
```

</div>

<div class="dl-world" data-world="letters">

The worksheet writes these as $(x^9)^{1/3}$ and $(y^{27})^{1/3}$.

```question
id: thirds-1--letters
type: fill-in-the-blank

edge(x⁹) is
{x³|x⁶|x²⁷}.

edge(y²⁷) is
{y⁹|y²⁴|y⁸¹}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. edge asks: which number, multiplied three times, gives this power?
2. So the exponent is cut into three equal parts.
3. What is 9 split into three equal parts?

**Think about:** a cube is the same in all three directions.

**Try this next:** edge of a power with exponent 30.

</details>

## 7. Quarters, and tenths

The worksheet asks for $(z^{12})^{1/4}$. The bottom, 4, says we need
four equal steps that make $z^{12}$.

<div class="dl-world" data-world="numbers">

```question
id: quarters-and-tenths-1--numbers
type: fill-in-the-blank

2¹² is 4096. Four equal steps make 4096 when each step is
{2³, which is 8|2⁸, which is 256|2⁴⁸}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: quarters-and-tenths-1--squiggles
type: fill-in-the-blank

Four equal steps make ♡¹² when each step is
{♡³|♡⁸|♡⁴⁸}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: quarters-and-tenths-1--letters
type: fill-in-the-blank

Four equal steps make z¹² when each step is
{z³|z⁸|z⁴⁸}.
```

</div>

Now a worked problem, with one step that went differently. It is
$(a^{100})^{1/10}$ from the worksheet:

> Ten equal steps make $a^{100}$. 100 − 10 is 90. So each step is
> $a^{90}$.

What went differently here? Check it by multiplying: what do ten steps
of $a^{90}$ make?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Ten steps of $a^{90}$: add 90 to itself ten times.
2. Is that 100?
3. Which sum would give 100 with ten equal parts?

**Think about:** what the bottom of the fraction counts.

**Try this next:** $(a^{100})^{1/4}$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Ten steps of $a^{90}$ make $a^{900}$, not $a^{100}$. The worked problem
took 10 away from 100. But ten equal steps need 100 split into ten
equal parts: $100 \div 10 = 10$. So each step is $a^{10}$, and ten of
them make $a^{10 \times 10} = a^{100}$.

</details>

## 8. Two letters at once

This looks scary. But each letter is its own small problem.

<div class="dl-world" data-world="numbers">

```question
id: two-letters-at-once-1--numbers
type: fill-in-the-blank

halfway(2⁶ × 3⁶) is
{2³ × 3³|2³ × 3⁶|2¹² × 3¹²}.

That is the number
{216|46656|36}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: two-letters-at-once-1--squiggles
type: fill-in-the-blank

halfway(♡⁶△⁶) is
{♡³△³|♡³△⁶|♡¹²△¹²}.

halfway(♡¹²△⁴) is
{♡⁶△²|♡⁶△⁴|♡⁸△⁰}.

Four equal steps make ♡⁸△¹² when each step is
{♡²△³|♡⁴△⁶|♡⁴△⁸}.
```

</div>

<div class="dl-world" data-world="letters">

The worksheet writes these as $(b^6c^6)^{1/2}$, $(d^{12}e^4)^{1/2}$
and $(f^8g^{12})^{1/4}$.

```question
id: two-letters-at-once-1--letters
type: fill-in-the-blank

halfway(b⁶c⁶) is
{b³c³|b³c⁶|b¹²c¹²}.

halfway(d¹²e⁴) is
{d⁶e²|d⁶e⁴|d⁸e⁰}.

Four equal steps make f⁸g¹² when each step is
{f²g³|f⁴g⁶|f⁴g⁸}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at one letter at a time. Cover the other with your finger.
2. For halfway, cut that letter's exponent in half.
3. Then do the same for the other letter.

**Think about:** multiply your answer by itself. Each letter's
exponents add on their own.

**Try this next:** halfway of $p^{10}q^{20}$.

</details>

We can check with numbers. Put a number in for each letter, and ask
Python if the two sides are equal. Here, `**` means a power, and `==`
asks "is this equal to that?"

```python exec
id: two-letters-at-once-2
# Put numbers in for the letters. Any numbers work here.
b = 2
c = 3
print(b ** 3 * c ** 3)
print((b ** 3 * c ** 3) * (b ** 3 * c ** 3) == b ** 6 * c ** 6)
```

It prints 216, and then `True`. Change `b` and `c`, and run it again.
Can you check halfway(d¹²e⁴) in the same way?

## 9. Two paths, one answer

The worksheet asks for $((h^2)^6)^{1/2}$. That is halfway of
$(h^2)^6$. There are two paths to the answer.

- **Path 1.** $(h^2)^6$ is six copies of $h^2$, multiplied. That is
  $h^{12}$. Then find halfway($h^{12}$).
- **Path 2.** Put the six copies of $h^2$ into two equal groups. Each
  group is three copies of $h^2$. One group is halfway.

```question
id: two-paths-one-answer-1
type: fill-in-the-blank

Path 1 gives
{h⁶|h³|h¹²}.

Path 2 gives
{h⁶|h³|h¹²}.
```

<details class="dl-answer"><summary>one way through it</summary>

Path 1: $h^{12}$, and halfway($h^{12}$) is $h^6$.

Path 2: one group is $h^2 \times h^2 \times h^2 = h^{2+2+2} = h^6$.

The two paths land in the same place, $h^6$.

</details>

## 10. What does the bottom mean?

An exploration. We have met exponents with 2, 3, 4 and 10 on the
bottom. What does the bottom of a fraction in an exponent tell us? And
what could $\heartsuit^{1/100}$ be?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $\heartsuit^{1/2}$ is halfway($\heartsuit$). How many of them make
   $\heartsuit$?
2. $\heartsuit^{1/3}$ is edge($\heartsuit$). How many of them make
   $\heartsuit$?
3. Now $\heartsuit^{1/4}$. How many?

**Think about:** a pizza cut into 4 slices. How many slices make the
whole pizza?

**Try this next:** what could $\heartsuit^{1/1}$ be?

</details>

<details class="dl-answer"><summary>one answer</summary>

The bottom counts equal steps. $\heartsuit^{1/4}$ is one step out of
4, and 4 of those steps make $\heartsuit$. So $\heartsuit^{1/100}$ is
a very small step, and 100 of them make $\heartsuit$. It is the pizza
idea again: 100 slices of $\frac{1}{100}$ make one whole. Here is one
answer. Yours may be different and work too.

</details>

## 11. Halfway of a half

An exploration. The usual way writes these as $(1/2)^{1/2}$ and
$2^{1/2}$. Guess first, then check.

```question
id: halfway-of-a-half-1
type: fill-in-the-blank

halfway(2) is between
{1 and 2|0 and 1|2 and 3}.

halfway(1/2) is between
{a half and 1|0 and a half|1 and 2}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. halfway(2): 1 × 1 is 1, and 2 × 2 is 4. Where does 2 sit?
2. halfway(1/2): try a half. $\frac{1}{2} \times \frac{1}{2}$ is
   $\frac{1}{4}$. Is that too small or too big?
3. So is halfway(1/2) bigger or smaller than a half?

**Think about:** multiplying a number smaller than 1 by itself makes
it smaller. The folded paper did this.

**Try this next:** what is halfway(1/4)?

</details>

Python can check. `**` means a power, and `0.5` is one half.

```python exec
id: halfway-of-a-half-2
print(2 ** 0.5)
print(0.5 ** 0.5)
```

<details class="dl-answer"><summary>one way to see it</summary>

halfway(2) is about 1.414. It is between 1 and 2. halfway(1/2) is
about 0.707. It is *bigger* than a half. For a number between 0 and 1,
halfway is bigger than the number: halfway(1/4) is 1/2.

There is one more surprise. 1.414 × 0.707 is about 1. So halfway(2)
and halfway(1/2) multiply to make 1, the way 2 and $\frac{1}{2}$ do.

</details>

## 12. From earlier: halfway through the folds

From *Powers: the long way and the short way*. After 4 folds, a sheet
of paper is in 16 pieces. After 2 folds, how many pieces are there?
What is halfway(16)?

<details class="dl-answer"><summary>answer</summary>

After 2 folds there are 4 pieces, and halfway(16) is 4. Two folds are
halfway to four folds. Two more folds multiply the 4 pieces by 4 again,
and make 16.

</details>

## 13. From earlier: another name for a half

From *Equivalent fractions: the same amount, different names*. What is
the simplest name for $\frac{2}{4}$? What does that tell you about
$\heartsuit^{2/4}$?

<details class="dl-answer"><summary>answer</summary>

$\frac{2}{4}$ is $\frac{1}{2}$. So $\heartsuit^{2/4}$ is
$\heartsuit^{1/2}$, which is halfway($\heartsuit$). Two quarter steps
make one half step.

</details>

## 14. Five of your own

Each part of the worksheet ends like this: make five problems of your
own, as strange as you like. Here are some ideas:

- halfway of a power with a very big exponent
- a fraction with 5 on the bottom
- two letters at once, with a quarter step
- a problem whose answer is 1
- a problem with an odd exponent

Which of your problems looks the most scary, but is simple inside?
