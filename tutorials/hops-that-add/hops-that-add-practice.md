---
title: "Hops that add: logarithms of a product, and the slide rule — Practice"
practice_for: hops-that-add
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Hops that add: logarithms of a product, and the slide rule — Practice

Small problems on one idea. The hops for a product are the hops of
each part, added: hops(10 → 100 × 1000) is hops(10 → 100) +
hops(10 → 1000). A slide rule uses this to multiply. Try each problem
before you open anything under it. Choose numbers, shapes or letters
in the box under the title.

<img src="two-rulers.svg" alt="Two rulers, one above the other, with their 1s at the same place. The top ruler is blue and the bottom one is yellow. Each is marked 1 to 10. The marks are not evenly spaced: the gap from 1 to 2 is the widest, and the gaps get smaller towards 10.">

## 1. Same or different?

```question
id: same-or-different-1
type: multiple-choice
answer: 1

Here are three counts. The first is hops(10 → 100 × 1000). The second
is hops(10 → 100) + hops(10 → 1000). The third is hops(10 → 100) ×
hops(10 → 1000). Which two are the same?

- The first and the second
  - 100 × 1000 is 100,000, which is 5 hops. And 2 + 3 is 5.
- The first and the third
  - 2 × 3 is 6. But 100,000 has 5 zeros, so it is 5 hops.
- The second and the third
  - 2 + 3 is 5, and 2 × 3 is 6.
```

## 2. Fill the gap

<div class="dl-world" data-world="numbers">

```question
id: fill-the-gap-1--numbers
type: fill-in-the-blank

hops(2 → 16) is 4, and hops(2 → 128) is 7. So 16 times
{8|112|3}
is 128.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: fill-the-gap-1--squiggles
type: fill-in-the-blank

hops($\heartsuit \to \heartsuit^4 \times \heartsuit^\square$) is 7. So □ is
{3|11|28}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: fill-the-gap-1--letters
type: fill-in-the-blank

hops($b \to b^4 \times b^k$) is 7. So $k$ is
{3|11|28}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The hops for the product are 7 in total.
2. The first part gives 4 of them.
3. How many hops must the second part give?

**Think about:** 4 + ? = 7.

**Try this next:** hops(2 → 32 × ?) is 8. What is the gap?

</details>

<details class="dl-answer"><summary>one way through it</summary>

4 + 3 is 7, so the second part is 3 hops. With numbers, 3 hops of ×2
land on 8, and 16 × 8 is 128. With a heart, □ is 3, because ♡⁴ × ♡³ is
♡⁷.

</details>

## 3. Continue the pattern

3 sits a little before the middle of the ruler. hops(10 → 3) is about
0.48.

| Number | 3 | 30 | 300 | 3000 |
|---|---|---|---|---|
| hops(10 → number) | about 0.48 | about 1.48 | ? | ? |

```question
id: continue-the-pattern-1
type: fill-in-the-blank

hops(10 → 300) is about
{2.48|48|0.48}.

hops(10 → 3000) is about
{3.48|4.48|1440}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 30 is 3 × 10. So hops(10 → 30) is hops(10 → 3) + hops(10 → 10).
2. 300 is 3 × 100. What is hops(10 → 100)?
3. Add it to hops(10 → 3).

**Think about:** each ×10 adds one whole hop.

**Try this next:** what is hops(10 → 3,000,000), about?

</details>

## 4. Match three ways

<div class="dl-world" data-world="numbers">

```question
id: match-three-ways-1--numbers
type: multiple-choice
answer: 1

Which of these says the same thing as hops(10 → 10² × 10⁴) = 6?

- $10^2 \times 10^4 = 10^6$
  - Two hops of ×10, then four more, make six hops.
- $10^2 \times 10^4 = 10^8$
  - 2 × 4 is 8. That multiplies the hops. Hops add.
- $10^2 + 10^4 = 10^6$
  - 100 + 10,000 is 10,100. The numbers multiply.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: match-three-ways-1--squiggles
type: multiple-choice
answer: 1

Which of these says the same thing as hops(♡ → ♡² × ♡⁴) = 6?

- $\heartsuit^2 \times \heartsuit^4 = \heartsuit^6$
  - Two hops of ×♡, then four more, make six hops.
- $\heartsuit^2 \times \heartsuit^4 = \heartsuit^8$
  - 2 × 4 is 8. That multiplies the hops. Hops add.
- $\heartsuit^2 + \heartsuit^4 = \heartsuit^6$
  - That adds the two powers. The powers multiply.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: match-three-ways-1--letters
type: multiple-choice
answer: 1

Which of these says the same thing as hops(b → b² × b⁴) = 6?

- $b^2 \times b^4 = b^6$
  - Two hops of ×b, then four more, make six hops.
- $b^2 \times b^4 = b^8$
  - 2 × 4 is 8. That multiplies the hops. Hops add.
- $b^2 + b^4 = b^6$
  - That adds the two powers. The powers multiply.
```

</div>

A third way to say it is the rule from *Multiplying powers: joining
two stacks*: when we multiply, we add the exponents.

## 5. Closer to 0, to a half, or to 1?

Look at the yellow ruler. The whole ruler is one hop of ×10.

```question
id: closer-to-1
type: fill-in-the-blank

hops(10 → 9) is closer to
{1|a half|0}.

hops(10 → 3) is closer to
{a half|0|1}.

hops(10 → 1.2) is closer to
{0|a half|1}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put your finger on 9 on the yellow ruler. Is it near the start, the
   middle or the far end?
2. Do the same for 3.
3. 1.2 is not marked. It is a little after 1.

**Think about:** the middle of the ruler is halfway(10), about 3.16.

**Try this next:** is hops(10 → 2) closer to 0, to a half, or to 1?

</details>

<details class="dl-answer"><summary>one way through it</summary>

9 sits near the far end, so hops(10 → 9) is close to 1. It is about
0.95. 3 sits a little before the middle, so hops(10 → 3) is close to a
half. It is about 0.48. 1.2 sits very near the start, so
hops(10 → 1.2) is close to 0. It is about 0.08.

</details>

## 6. Where on the ruler?

2 × 5 is 10. So hops(10 → 2) + hops(10 → 5) is hops(10 → 10), which
is one whole hop. hops(10 → 2) is about 0.3.

```question
id: where-on-the-ruler-1
type: multiple-choice
answer: 1

Where does 5 sit on the ruler?

- After the middle, about 0.7 of the way along
  - 0.3 + 0.7 is 1. The two hops together make one whole hop.
- In the middle, because 5 is half of 10
  - Half of 10 sits in the middle of a normal ruler. On this ruler,
    the middle is halfway(10), about 3.16.
- Before the middle
  - 5 is bigger than halfway(10), which sits in the middle.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The whole ruler is 1 hop.
2. 2 takes about 0.3 of it.
3. 5 must take the rest, so the two add to 1.

**Think about:** look at the picture. Is 5 before or after the middle?

**Try this next:** 4 × 2.5 is 10. hops(10 → 4) is about 0.6. Where
does 2.5 sit?

</details>

## 7. Reading the slide rule

In this picture, the blue ruler has slid along. Its 1 sits over the
yellow 2.

<img src="two-times-three.svg" alt="The two rulers again. The blue top ruler has slid to the right, so its 1 sits over the 2 on the yellow bottom ruler. Dashed lines mark two places. One is the blue 1 over the yellow 2, labelled 1 over 2. The other is the blue 3 over the yellow 6, labelled 3 over 6.">

```question
id: reading-the-slide-rule-1
type: fill-in-the-blank

The blue 4 sits over the yellow
{8|6|10}.

The yellow 10 is under the blue
{5|8|10}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The blue 1 sits over the yellow 2. So the slide multiplies by 2.
2. Each blue number sits over 2 times itself.
3. Which number, times 2, is 10?

**Think about:** the blue 6 would sit over 12. Is 12 on the yellow
ruler?

**Try this next:** slide the blue 1 over the yellow 3. What would sit
under the blue 3?

</details>

<details class="dl-answer"><summary>one way through it</summary>

The blue 4 sits over 2 × 4, which is 8. The yellow 10 is under the
blue 5, because 2 × 5 is 10. The blue 6 is past the end of the yellow
ruler, because 2 × 6 is 12, and the yellow ruler stops at 10.

</details>

## 8. What went differently here?

Here is a worked problem, with one step that went differently.

> hops(10 → 100 × 1000) is hops(10 → 100) × hops(10 → 1000). That is
> 2 × 3, which is 6.

What went differently? Check it by counting the zeros of 100 × 1000.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 100 × 1000 is 100,000. Count its zeros.
2. Each hop of ×10 puts one zero on the end.
3. So how many hops is it? Is that 2 × 3, or 2 + 3?

**Think about:** multiplying by 1000 after 100 is three more hops.

**Try this next:** hops(2 → 4 × 8), by hopping.

</details>

<details class="dl-answer"><summary>one way through it</summary>

100,000 has 5 zeros, so it is 5 hops. The worked problem multiplied the
two counts of hops. But the hops for a product are added: two hops to
100, then three more. 2 + 3 is 5.

</details>

## 9. Two paths, one answer

<div class="dl-world" data-world="numbers">

```question
id: two-paths-one-answer-1--numbers
type: fill-in-the-blank

Path 1: 4 × 8 × 16 is
{512|28|128}.

hops(2 → 512) is
{9|24|256}.

Path 2: hops(2 → 4) + hops(2 → 8) + hops(2 → 16) is 2 + 3 + 4, which is
{9|24|28}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: two-paths-one-answer-1--squiggles
type: fill-in-the-blank

Path 1: ♡² × ♡³ × ♡⁴ is
{♡⁹|♡²⁴|3♡⁹}.

hops(♡ → ♡⁹) is
{9|24|♡}.

Path 2: 2 + 3 + 4 is
{9|24|28}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: two-paths-one-answer-1--letters
type: fill-in-the-blank

Path 1: b² × b³ × b⁴ is
{b⁹|b²⁴|3b⁹}.

hops(b → b⁹) is
{9|24|b}.

Path 2: 2 + 3 + 4 is
{9|24|28}.
```

</div>

Python can check the numbers. This is the counting machine from the
page. It starts at 1, multiplies by the base, and counts until it
reaches the target.

```python exec
id: two-paths-one-answer-2
def hops(base, target):
    position = 1
    count = 0
    while position < target:
        position = position * base
        count = count + 1
    return count

print(hops(2, 4 * 8 * 16))
print(hops(2, 4) + hops(2, 8) + hops(2, 16))
```

<details class="dl-answer"><summary>one way through it</summary>

Path 1 multiplies first: 4 × 8 × 16 is 512, and nine hops of ×2 land
on 512. Path 2 counts each part first: 2 + 3 + 4 is 9. The two paths
land in the same place. The cell prints 9 twice.

</details>

## 10. A stretch: sliding back

Multiplying adds hops. Dividing takes hops away.

```question
id: a-stretch-sliding-back-1
type: fill-in-the-blank

hops(10 → 1000 ÷ 10) is 3 − 1, which is
{2|4|100}.

hops(2 → 32 ÷ 4) is 5 − 2, which is
{3|7|8}.
```

On the slide rule, dividing slides back. To find 8 ÷ 2, put the blue 2
over the yellow 8. Where is the blue 1 now?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The blue 2 is hops(10 → 2) from the blue 1.
2. So the blue 1 sits hops(10 → 2) back from the yellow 8.
3. Which yellow number, times 2, is 8?

**Think about:** 8 ÷ 2 asks which number, times 2, makes 8.

**Try this next:** how would you find 9 ÷ 3 on the slide rule?

</details>

<details class="dl-answer"><summary>one way through it</summary>

The blue 1 sits over the yellow 4. The blue 2 is hops(10 → 2) from the
blue 1, so the blue 1 is hops(10 → 8) − hops(10 → 2) from the yellow 1.
That is hops(10 → 4). And 8 ÷ 2 is 4.

</details>

## 11. Looks scary, is simple

Neither 4 nor 25 lands on a stop of ×10. hops(10 → 4) is about 0.6,
and hops(10 → 25) is about 1.4.

```question
id: looks-scary-is-simple-1
type: fill-in-the-blank

4 × 25 is
{100|29|425}.

So hops(10 → 4) + hops(10 → 25) is exactly
{2|1|3}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. You do not need either count on its own.
2. Multiply the two numbers first.
3. How many hops of ×10 land on that product?

**Think about:** 0.6 + 1.4 is 2. The two counts fit together.

**Try this next:** hops(10 → 2) + hops(10 → 50).

</details>

## 12. From earlier: folds

From *Counting hops: logarithms, how many times did we multiply?*.
folds(32) counts how many folds of a sheet of paper make 32 pieces.
What is folds(32)? 32 is 4 × 8. Is folds(4) + folds(8) the same?

<details class="dl-answer"><summary>answer</summary>

folds(32) is 5, because 2 × 2 × 2 × 2 × 2 is 32. folds(4) is 2 and
folds(8) is 3. 2 + 3 is 5, so they are the same. Folds are hops of ×2,
so they add too.

</details>

## 13. From earlier: halfway

From *Halfway powers: fractional exponents, two half steps make one*.
What is halfway(100)? What are hops(10 → 100) and
hops(10 → halfway(100))?

<details class="dl-answer"><summary>answer</summary>

halfway(100) is 10, because 10 × 10 is 100. hops(10 → 100) is 2, and
hops(10 → 10) is 1. 100 is 10 × 10, so its hops are 1 + 1. Halfway
cuts the hops in half.

</details>

## 14. Five of your own

Can you make five problems of your own, as strange as you like? Here
are some ideas:

- hops of ×10 for a product of three numbers
- two numbers that do not land on a stop, but whose product does
- a shape, like hops(△ → △⁵ × △⁷)
- a multiplication the slide rule in the pictures could show
- a division, by sliding back

Which of your problems was the hardest to make?
