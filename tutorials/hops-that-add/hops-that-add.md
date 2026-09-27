---
title: "Hops that add: logarithms of a product, and the slide rule"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Hops that add: logarithms of a product, and the slide rule

Here is a multiplication:

$$100 \times 1000 = 100{,}000$$

On an earlier page, we counted hops. hops(10 → 100) is 2. It takes
two hops of ×10 to go from 1 to 100. hops(10 → 1000) is 3.

```question
id: a-hundred-times-a-thousand-1
type: multiple-choice
answer: 1

What is hops(10 → 100,000)?

- 5
  - 100,000 has five zeros. Each hop of ×10 puts one zero on the end.
- 6
  - 2 × 3 is 6. The numbers multiply, so it can feel like the hops
    multiply too. Count the zeros of 100,000.
- 100,000
  - 100,000 is where the hops land. The question asks how many hops.
```

## Two hops, then three more

Here is 100 × 1000 as hops. Two hops of ×10 go from 1 to 100.
Multiplying by 1000 is three more hops of ×10.

$$1 \xrightarrow{\times 10} 10 \xrightarrow{\times 10} 100 \xrightarrow{\times 10} 1000 \xrightarrow{\times 10} 10{,}000 \xrightarrow{\times 10} 100{,}000$$

```question
id: two-hops-then-three-more-1
type: fill-in-the-blank

hops(10 → 100) + hops(10 → 1000) is
{2 + 3|2 × 3|100 + 1000}.

That is
{5|6|1100}
hops in total.
```

A *product* is the answer to a multiplication. Here, the product is
100,000. The hops for the product are the hops of each part, added.

## Hops of two

Now each hop multiplies by 2. hops(2 → 8) is 3, because
2 × 2 × 2 is 8. hops(2 → 4) is 2, because 2 × 2 is 4.

```question
id: hops-of-two-1
type: fill-in-the-blank

8 × 4 is
{32|12|16}.

hops(2 → 32) is
{5|6|16}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start at 1, and double: 2, 4, 8, 16, 32.
2. Count the doublings until you land on 32.
3. Now add hops(2 → 8) and hops(2 → 4). Do you get the same count?

**Think about:** multiplying by 8 is three hops of ×2. Multiplying by
4 is two more.

**Try this next:** is hops(2 → 16 × 2) the same as hops(2 → 16) +
hops(2 → 2)?

</details>

So hops(2 → 8) + hops(2 → 4) = hops(2 → 32). Three hops and two hops
make five hops.

## The same fact, seen before

On the page *Multiplying powers: joining two stacks*, we added
exponents: $2^3 \times 2^2 = 2^{3+2} = 2^5$. An exponent counts hops
too.

```question
id: the-same-fact-seen-before-1
type: multiple-choice
answer: 1

Which line says the same thing as
hops(2 → 8) + hops(2 → 4) = hops(2 → 32)?

- $2^3 \times 2^2 = 2^5$
  - Three hops of ×2, then two more, make five hops of ×2.
- $2^3 + 2^2 = 2^5$
  - 8 + 4 is 12, not 32. The hops add, but the numbers multiply.
- $3 \times 2 = 6$
  - That multiplies the hops. The hops add: 3 + 2 is 5.
```

Adding the exponents and adding the hops are one fact. It is written
in two ways.

## Your turn

Choose numbers, shapes or letters in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: your-turn-1--numbers
type: fill-in-the-blank

hops(10 → 1000) is 3, and hops(10 → 10,000) is 4. So
hops(10 → 1000 × 10,000) is
{7|12|10,000,000}.

9 × 27 is 243. So hops(3 → 243) is
{5|6|243}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: your-turn-1--squiggles
type: fill-in-the-blank

hops(♡ → ♡⁴ × ♡³) is
{7|12|♡⁷}.

hops(△ → △ × △⁵) is
{6|5|△⁶}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: your-turn-1--letters
type: fill-in-the-blank

hops(b → b⁴ × b³) is
{7|12|b⁷}.

hops(n → n × n⁵) is
{6|5|n⁶}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the hops for each part on its own.
2. A shape on its own, like △, is △¹: one hop.
3. Add the two counts.

**Think about:** 9 is two hops of ×3, and 27 is three hops of ×3.

**Try this next:** hops(♡ → ♡² × ♡² × ♡²).

</details>

The heart could be any number at all, and the pattern stays the same.
That is all a letter in algebra means.

## A counting machine

Python is a language for computers. Here is the counting machine from
an earlier page. It starts at 1, multiplies by the base, and counts,
until it reaches the target. The last two lines check that hops add.

```python exec
id: a-counting-machine-1
def hops(base, target):
    position = 1
    count = 0
    while position < target:
        position = position * base
        count = count + 1
    return count

print(hops(10, 100) + hops(10, 1000))
print(hops(10, 100 * 1000))
```

```predict
type: number

Before you run it: the first line adds two counts of hops. What will
the last line print?
```

Both lines print 5. Now change the numbers and run it again. Try
`hops(2, 8) + hops(2, 4)` and `hops(2, 8 * 4)`. Do the two lines still
agree?

{{include: setup/zen-calm-check.md}}

## A ruler of hops

Here are two rulers, one above the other. The top one is blue, and the
bottom one is yellow. Each is marked from 1 to 10. They are not normal
rulers.

<img src="two-rulers.svg" alt="Two rulers, one above the other, with their 1s at the same place. The top ruler is blue and the bottom one is yellow. Each is marked 1 to 10. The marks are not evenly spaced: the gap from 1 to 2 is the widest, and the gaps get smaller towards 10.">

On these rulers, the whole length from 1 to 10 is one hop of ×10. A
number sits at its hops of 10 from 1. For a number between 1 and 10,
that is a fraction of a hop.

```question
id: a-ruler-of-hops-1
type: fill-in-the-blank

hops(10 → 1) is
{0|1|10}.

hops(10 → 10) is
{1|10|0}.
```

So 1 sits at the start of the ruler, and 10 sits at the far end, one
whole hop along.

## Not evenly spaced

```question
id: not-evenly-spaced-1
type: multiple-choice
answer: 1

Look at the yellow ruler. Which gap is wider, 1 to 2 or 9 to 10?

- 1 to 2
  - 1 to 2 multiplies by 2. 9 to 10 multiplies by only a little more
    than 1.
- They are the same
  - On a normal ruler, each gap is 1. On this ruler, the gaps are not
    the same. Look at the picture.
- 9 to 10
  - 9 and 10 are big numbers. But the gap between them is small in the
    picture.
```

On this ruler, a gap shows how much we multiply, not how much we add.
From 1 to 2 multiplies by 2. From 9 to 10 multiplies by 10/9, a little
more than 1.

## The middle of the ruler

```question
id: the-middle-of-the-ruler-1
type: multiple-choice
answer: 1

Which number sits in the middle of the ruler, half a hop from 1?

- About 3.16, which is halfway(10)
  - Two half hops make one whole hop of ×10, and 3.16 × 3.16 is about
    10.
- 5
  - 5 is half of 10. But two hops of ×5 go from 1 to 25, past 10.
- 5.5
  - 5.5 is halfway from 1 to 10 when we add. This ruler multiplies.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The page *Halfway powers: fractional exponents, two half steps make
   one* had halfway(10). It is the number that, done twice, gives 10.
2. 3 × 3 is 9, a little less than 10. So halfway(10) is a little more
   than 3.
3. Look at the picture. Which mark is close to the middle?

**Think about:** half a hop, done twice, is one whole hop.

**Try this next:** which number sits a quarter of the way along?

</details>

## Sliding the rulers

Now the blue ruler slides to the right. Its 1 sits over the 2 on the
yellow ruler.

<img src="two-times-three.svg" alt="The two rulers again. The blue top ruler has slid to the right, so its 1 sits over the 2 on the yellow bottom ruler. Dashed lines mark two places. One is the blue 1 over the yellow 2, labelled 1 over 2. The other is the blue 3 over the yellow 6, labelled 3 over 6.">

```question
id: sliding-the-rulers-1
type: fill-in-the-blank

The blue 3 sits over the yellow
{6|5|9}.
```

Here is why. Start at the yellow 1. The slide moves the blue ruler
hops(10 → 2) along. Then the blue 3 is hops(10 → 3) further. So the
blue 3 is hops(10 → 2) + hops(10 → 3) from the yellow 1. Hops add, so
that is hops(10 → 2 × 3), which is hops(10 → 6).

```question
id: sliding-the-rulers-2
type: multiple-choice
answer: 1

Sliding one ruler along the other adds two distances. What does that
do to the two numbers?

- It multiplies them
  - 2 × 3 is 6, and the blue 3 sits over the yellow 6.
- It adds them
  - 2 + 3 is 5. Look at the picture: the blue 3 sits over 6, not 5.
- It takes one away from the other
  - 3 − 2 is 1. The blue 3 is far from the yellow 1.
```

## Two times four

Here is the same slide again. The blue 1 still sits over the yellow 2.

<img src="two-times-four.svg" alt="The two rulers again. The blue top ruler has slid to the right, so its 1 sits over the 2 on the yellow bottom ruler. Dashed lines mark two places. One is the blue 1 over the yellow 2, labelled 1 over 2. The other is the blue 4 over the yellow 8, labelled 4 over 8.">

```question
id: two-times-four-1
type: multiple-choice
answer: 1

What does this picture find?

- 2 × 4 = 8
  - The blue 1 sits over 2, and the blue 4 sits over 8.
- 2 + 4 = 6
  - The rulers add distances, not numbers. The blue 4 sits over 8.
- 4 − 2 = 2
  - 2 is where the blue 1 sits. Look where the blue 4 sits.
```

A ruler like this is called a *slide rule*. In 1620, Edmund Gunter of
Oxford made a ruler marked in this way. Around 1622, William Oughtred
of Cambridge put two of them together. That was the first slide rule.
It came a few years after John Napier published a book on numbers
like hops.

Engineers and scientists used slide rules for about 350 years. Buzz
Aldrin's slide rule flew with him to the Moon, on Apollo 11. Around
1974, pocket calculators became cheap, and people stopped using slide
rules for most work.

```question
id: two-times-four-2
type: fill-in-the-blank

From 1622 to 1974 is
{about 350|about 35|about 3500}
years.
```

## A stretch: sliding back

This step goes a little further. Sliding forwards adds two distances.
Sliding back takes one distance away. Look at the last picture again,
and read it the other way.

To find 8 ÷ 4, put the blue 4 over the yellow 8. That is where it
already is.

```question
id: a-stretch-sliding-back-1
type: fill-in-the-blank

The blue 1 sits over the yellow
{2|4|12}.

So 8 ÷ 4 is
{2|4|12}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The blue 4 is hops(10 → 4) from the blue 1.
2. The yellow 8 is hops(10 → 8) from the yellow 1.
3. So the blue 1 sits hops(10 → 8) − hops(10 → 4) from the yellow 1.
   Which yellow number is there?

**Think about:** multiplying adds hops. What does dividing do to hops?

**Try this next:** how would you find 6 ÷ 3 on the slide rule in the
picture before?

</details>

## The usual way to write it

Here is the idea of this page with the friendly name:

$$\text{hops}(10 \to 2 \times 3) = \text{hops}(10 \to 2) + \text{hops}(10 \to 3)$$

On the page *Counting hops: logarithms, how many times did we
multiply?*, hops(10 → 1000) had a usual way to write it:
$\log_{10} 1000$. We read it as "log to base 10 of 1000". *Log* is
short for *logarithm*. A logarithm counts hops. So the idea of this
page is

$$\log_{10}(2 \times 3) = \log_{10} 2 + \log_{10} 3$$

When the base is clear, people often leave the small 10 off. For any
two numbers $a$ and $b$:

$$\log(a \times b) = \log a + \log b$$

In words: the logarithm of a product is the logarithm of each part,
added. It means exactly the same as "hops for a product is the hops of
each part, added".

Python can find hops that are a fraction of a hop. The first line,
`import math`, gets Python's box of maths tools ready. `math.log10(2)`
is hops(10 → 2).

```python exec
id: the-usual-way-to-write-it-1
import math

print(math.log10(2) + math.log10(3))
print(math.log10(6))
print(math.log10(2) + math.log10(4))
print(math.log10(8))
```

```predict
type: choice

Before you run it: will the first two lines print the same number?

- Yes, the same number
- No, different numbers
  - Neither 2 nor 3 lands on a stop of ×10, so it can feel like the
    rule might not hold for them.
```

The first two lines both print `0.7781512503836436`. The last two both
print `0.9030899869919435`. So the blue 3 sits about 0.78 of the way
along the yellow ruler, over the 6.

You can keep writing hops when it feels calmer. hops(10 → 6) and
$\log_{10} 6$ are two names for one number.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say the idea of this page in your own
words. Why does a slide rule multiply, when it only adds two distances?
Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

Multiplying two numbers adds their hops: hops(10 → 2 × 3) is
hops(10 → 2) + hops(10 → 3). On a slide rule, each number sits at its
hops of 10 from 1. So sliding one ruler along the other adds two
numbers' hops, and the answer is under the second number. Your way of
saying it may be clearer than ours.

</details>

## Make your own

Can you make five problems of your own like these? Try one with hops
of ×10, and one with hops of ×2. Try one with a shape, like
hops(△ → △³ × △⁶). Try one that the slide rule in the pictures could
show, like 2 × 5. Which one surprises you most?

## Looking back

On the slide rule, the gap from 1 to 2 is wider than the gap from 9 to
10. Why is that?

A challenge: the counting machine below counts only whole hops. It
says hops(10, 20) is 2, and hops(10, 50) is 2. That adds to 4. But
20 × 50 is 1000, and hops(10, 1000) is 3. Can you see why the two
answers are different? Can you change the machine, so that it says
"between 1 and 2" for hops(10, 20)?

```python challenge
# The counting machine counts whole hops, and passes a target it cannot land on.
def hops(base, target):
    position = 1
    count = 0
    while position < target:
        position = position * base
        count = count + 1
    return count

print(hops(10, 20) + hops(10, 50))
print(hops(10, 20 * 50))
```

## Read more

The page before this one on hops is
[Counting hops: logarithms, how many times did we multiply?](tutorial:how-many-hops).
The Simple English Wikipedia page on the
[slide rule](https://simple.wikipedia.org/wiki/Slide_rule) shows real
slide rules, and how they multiply and divide. The longer English page
on the [slide rule](https://en.wikipedia.org/wiki/Slide_rule) tells its
history, from Gunter and Oughtred to the calculators that replaced it.
