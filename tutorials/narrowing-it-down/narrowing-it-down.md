---
title: "The Drake equation: narrowing it down, one fraction at a time"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# The Drake equation: narrowing it down, one fraction at a time

Here is a town of 1000 people. We invented the town, and its numbers
too. The top bar is everybody in the town. Each bar under
it keeps a part of the bar above it.

<img src="a-town.svg" alt="Four bars, one under another, each shorter than the one above. The top bar is labelled start, and its count is 1000. The second bar is labelled like tea, times 1/2, and its count is 500. The third bar is labelled have a bike, times 1/5, and its count is 100. The last bar is labelled can juggle, times 1/10, and its count is 10.">

```question
id: a-town-1
type: fill-in-the-blank

The town has
{1000|500|10}
people.

Of them,
{500|1000|100}
like tea.
```

## One bar at a time

The second bar is the people who like tea. The third bar keeps only
some of them: the tea drinkers who also have a bike. The last bar keeps
only the ones who can also juggle. To *juggle* is to throw three or
more balls in the air and catch them, again and again.

```question
id: one-bar-at-a-time-1
type: fill-in-the-blank

One fifth of the 500 tea drinkers have a bike. One fifth of 500 is
{100|5|495}.

One tenth of those 100 can juggle. One tenth of 100 is
{10|1|90}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. One fifth of something is one of 5 equal parts.
2. Put 500 people into 5 equal groups. How many are in one group?
3. Now put 100 people into 10 equal groups.

**Think about:** on [Multiplying fractions: a fraction of a
fraction](tutorial:a-fraction-of-a-fraction), *of* meant times. One
fifth of 500 is $\frac{1}{5} \times 500$.

**Try this next:** what is one half of 1000?

</details>

## The whole chain

Here is the town in one line. We start with 1000. Then we multiply by
each fraction, one after another:

$$1000 \times \frac{1}{2} \times \frac{1}{5} \times \frac{1}{10} = 10$$

```question
id: the-whole-chain-1
type: multiple-choice
answer: 1

The last bar is 10 people out of 1000. What fraction of the whole town
is that?

- 1/100
  - 10 out of 1000 is 1 out of 100. It is also 1/2 × 1/5 × 1/10.
- 1/17
  - 2 + 5 + 10 = 17. That adds the bottoms. Fractions of fractions
    multiply their bottoms.
- 1/10
  - 1/10 is the last fraction on its own. It keeps a tenth of the
    third bar, and the third bar is already much smaller than the town.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last bar has 10 people. The town has 1000.
2. How many groups of 10 fit in 1000?
3. Now multiply the three fractions: tops together, bottoms together.

**Think about:** two ways to find the same fraction. Do they agree?

**Try this next:** what fraction of the town likes tea and has a bike?

</details>

## A different order

Now ask the questions in a different order. First keep the jugglers,
then the ones with a bike, then the tea drinkers.

$$1000 \times \frac{1}{10} \times \frac{1}{5} \times \frac{1}{2}$$

```question
id: a-different-order-1
type: fill-in-the-blank

1000 × 1/10 is
{100|10|1010}.

Then 100 × 1/5 is
{20|500|5}.

Then 20 × 1/2 is
{10|40|2}.

Compared with the first order, the end is
{the same|bigger|smaller}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. One tenth of 1000: put 1000 into 10 equal groups.
2. One fifth of 100: put 100 into 5 equal groups.
3. One half of 20.

**Think about:** 3 × 4 and 4 × 3 are both 12.

**Try this next:** try the order 1/5, then 1/2, then 1/10.

</details>

The bars in the middle change with the order. The end does not. The
fractions are all multiplied together, and the order of multiplying
does not change the answer.

A start number, then fractions multiplied one after another, is called
a *chain* of fractions. Each fraction *narrows* the count. It keeps
only a part, and the count gets smaller.

## A town of any size

Choose numbers, shapes or letters in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: a-town-of-any-size-1--numbers
type: fill-in-the-blank

A town has 5000 people. The same three fractions keep
{50|500|5}
people at the end.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: a-town-of-any-size-1--squiggles
type: fill-in-the-blank

A town has ♡ people. The same three fractions keep
{♡/100|♡/17|100♡}
people at the end.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: a-town-of-any-size-1--letters
type: fill-in-the-blank

A town has n people. The same three fractions keep
{n/100|n/17|100n}
people at the end.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The three fractions together keep 1/100 of the town.
2. What is 1/100 of the start number?
3. With a shape or a letter, 1/100 of ♡ is ♡/100.

**Think about:** the town can have any number of people. The fraction
kept is always the same.

**Try this next:** a town of 20,000 people.

</details>

The heart can be any number, and the pattern still holds. That is all
a letter in algebra means.

## A checking machine

Python is a language for computers. The first line gets Python's
fraction tool, `Fraction`, ready. `Fraction(1, 2)` is one half. In
Python, the times sign is a star, `*`.

```python exec
id: a-checking-machine-1
from fractions import Fraction

town = 1000
like_tea = town * Fraction(1, 2)
have_a_bike = like_tea * Fraction(1, 5)
can_juggle = have_a_bike * Fraction(1, 10)
print(like_tea, have_a_bike, can_juggle)
```

```predict
type: number

Before you run it: what will the last number on the line be?
```

Python prints 500, 100 and 10, the counts in the picture. Now change
the town to 3000, and run it again. Then swap two of the fractions.
Which numbers change, and which one stays the same?

{{include: setup/zen-calm-check.md}}

## A chain for the whole galaxy

A *galaxy* is a huge group of stars. Ours is called the Milky Way, and
our Sun is one of its stars. In 1961, some scientists met at Green
Bank, in West Virginia, in the United States. It was the first meeting
about *SETI*. SETI means listening for signals from beings on other
worlds. The
astronomer Frank Drake wrote a chain for the meeting. It asks: how many
worlds in our galaxy are sending signals we could hear, now?

$$N = R_* \cdot f_p \cdot n_e \cdot f_l \cdot f_i \cdot f_c \cdot L$$

It is called the *Drake equation*. The dot, $\cdot$, is another way to
write times. Each letter is one step of the chain. The small letters
under each one are labels. Here are the steps, with Drake's guesses in
1961:

| Step | What it counts, or keeps | Drake's guesses |
|---|---|---|
| $R_*$ | new stars in our galaxy each year | 1 |
| $f_p$ | the fraction of stars with planets | 0.2 to 0.5 |
| $n_e$ | planets that could hold life, for each of those stars | 1 to 5 |
| $f_l$ | the fraction of those planets where life starts | 1 |
| $f_i$ | the fraction of those where life becomes clever | 1 |
| $f_c$ | the fraction of those that send signals into space | 0.1 to 0.2 |
| $L$ | how many years they keep sending | 1000 to 100,000,000 |

Some guesses are decimals. 0.2 is two tenths, which is $\frac{1}{5}$.
0.5 is $\frac{1}{2}$, and 0.1 is $\frac{1}{10}$. A guess of 1 keeps
everything.

The first step counts stars each year, and the last step counts years.
Multiplied together, they make a count. $N$ is that count: worlds
sending signals now.

```question
id: a-chain-for-the-whole-galaxy-1
type: multiple-choice
answer: 2

In the town, every fraction made the count smaller. Which steps of
Drake's chain can make the count bigger?

- None of them
  - The fractions all keep a part, or all of it. Look at the guesses
    for $n_e$ and for $L$.
- $n_e$ and $L$
  - Their guesses are bigger than 1. Multiplying by a number bigger
    than 1 makes the count bigger.
- $f_p$ and $f_c$
  - Their guesses are smaller than 1. They keep only a part.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look down the last column of the table.
2. Which guesses are smaller than 1? Which are 1? Which are bigger?
3. What does multiplying by 5 do to a number?

**Think about:** [Multiplying: a closer look at bigger and
smaller](tutorial:does-multiplying-make-it-bigger) asked when
multiplying makes a number bigger.

**Try this next:** what does multiplying by 1 do to a number?

</details>

## Drake's smallest guesses

Each guess is a range: a smallest value and a largest value. First we
take the smallest value of each, and multiply in small steps.

| Step | Multiply by | Count so far |
|---|---|---|
| $R_*$ | | 1 |
| $f_p$ | $\frac{1}{5}$ | $\frac{1}{5}$ |
| $n_e$ | 1 | $\frac{1}{5}$ |
| $f_l$ and $f_i$ | 1 and 1 | $\frac{1}{5}$ |
| $f_c$ | $\frac{1}{10}$ | ? |
| $L$ | 1000 | ? |

```question
id: drakes-smallest-guesses-1
type: fill-in-the-blank

1/5 × 1/10 is
{1/50|1/15|2/10}.

Then 1/50 × 1000 is
{20|50|1000}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Multiply the tops: 1 × 1. Multiply the bottoms: 5 × 10.
2. 1/50 × 1000 asks: what is one fiftieth of 1000?
3. Put 1000 into 50 equal groups. How many are in each group?

**Think about:** 50 × 20 is 1000.

**Try this next:** what is 1/50 × 100?

</details>

So Drake's smallest guesses give $N = 20$: twenty worlds in our galaxy,
sending signals now.

## Drake's largest guesses

Now we take the largest value of each guess.

| Step | Multiply by | Count so far |
|---|---|---|
| $R_*$ | | 1 |
| $f_p$ | $\frac{1}{2}$ | $\frac{1}{2}$ |
| $n_e$ | 5 | ? |
| $f_l$ and $f_i$ | 1 and 1 | ? |
| $f_c$ | $\frac{1}{5}$ | ? |
| $L$ | 100,000,000 | ? |

```question
id: drakes-largest-guesses-1
type: fill-in-the-blank

1/2 × 5 is
{5/2|1/10|5}.

5/2 × 1 × 1 is still 5/2. Then 5/2 × 1/5 is
{1/2|5/10|25/2}.

Then 1/2 × 100,000,000 is
{50,000,000|100,000,000|200,000,000}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 5 is 5/1. Multiply the tops, then the bottoms: 1/2 × 5/1.
2. For 5/2 × 1/5, multiply the tops and the bottoms again. The answer
   is 5/10. What is its shortest name?
3. Half of 100 million.

**Think about:** multiplying by 5 and then by 1/5 lands where you
started.

**Try this next:** what is 1/2 × 1000?

</details>

## How far apart?

The smallest guesses gave 20 worlds. The largest gave 50,000,000:
fifty million worlds.

```question
id: how-far-apart-1
type: multiple-choice
answer: 1

How many times bigger is 50,000,000 than 20?

- 2,500,000
  - 20 × 2,500,000 = 50,000,000.
- 49,999,980
  - That is 50,000,000 − 20. It says how much bigger, by taking away.
    The question asks how many times.
- 1000
  - 20 × 1000 is 20,000. That is much less than 50,000,000.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. "How many times bigger" is a division: 50,000,000 ÷ 20.
2. First divide by 10: 5,000,000.
3. Then divide by 2.

**Think about:** which step of the chain had the widest guesses?

**Try this next:** 100,000,000 is how many times 1000?

</details>

The two answers are two and a half million times apart. Most of that
comes from $L$. Its guesses go from 1000 to 100,000,000, and the second
is 100,000 times the first. Nobody in 1961 knew how long a world keeps
sending signals. Nobody knows now. The chain shows which guess makes
the two answers so far apart.

## Your own guesses

Here is Drake's chain as a cell, with his smallest guesses. The names
say what each step is. Change any guess and run it again.

```python exec
id: your-own-guesses-1
from fractions import Fraction

new_stars_each_year = 1
with_planets = Fraction(1, 5)
planets_for_life = 1
life_starts = 1
life_gets_clever = 1
sends_signals = Fraction(1, 10)
years_sending = 1000
print(new_stars_each_year * with_planets * planets_for_life * life_starts
      * life_gets_clever * sends_signals * years_sending)
```

```predict
type: number

Before you run it: what will the cell print?
```

It prints 20, as we found by hand. Now try your own guesses. Can you
find guesses that make the answer exactly 1: our world alone, and no
other?

## A different question

In 2016, two scientists, Adam Frank and Woody Sullivan, asked a
different question. Drake asked how many worlds are sending signals
*now*. They asked: has any other world *ever* made machines like ours,
at any time in the history of the galaxy?

Their chain has no $L$, because they count every world that ever did
it, for a long time or a short one. They call the count $A$. Their
chain has two steps:

$$A = N_{ast} \cdot f_{bt}$$

- $N_{ast}$ is the number of planets in the *habitable zone* of their
  star: not too hot, and not too cold, so water can be a liquid.
- $f_{bt}$ is the fraction of those planets where a kind of life ever
  builds machines like ours.

For $N_{ast}$ they multiply the stars in the galaxy by two fractions,
$f_p \approx 1$ and $n_e \approx 0.2$. The sign $\approx$ means
*about*. So for every five stars, there is about one planet in a
habitable zone.
For the Milky Way, their count is

$$N_{ast} = 6 \times 10^{10}$$

$10^{10}$ is 10 multiplied by itself 10 times: a 1 with ten zeros
after it. [Powers: the long way and the short
way](tutorial:the-long-way) has more about powers like this one.

```question
id: a-different-question-1
type: fill-in-the-blank

10¹⁰ is
{10,000,000,000|100|1,000,000,000}.

So 6 × 10¹⁰ is
{60,000,000,000|6,000,000,000|600}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 10¹ is 10, with one zero. 10² is 100, with two zeros.
2. 10¹⁰ has ten zeros after the 1. Count them as you write.
3. Six of those is a 6 with ten zeros after it.

**Think about:** each ×10 puts one more zero on the end.

**Try this next:** how many zeros does 10⁶, a million, have?

</details>

60,000,000,000 is 60 billion. A *billion* is a thousand million.

## One in 60 billion

We know one world made machines like ours: our own. So $A$ is at least
1. Frank and Sullivan asked: how small must $f_{bt}$ be, for $A$ to be
only 1? Then

$$6 \times 10^{10} \times f_{bt} = 1$$

On [Dividing fractions: how many fit?](tutorial:how-many-fit), a number
times its partner, the *reciprocal*, made 1. $\frac{1}{4} \times 4 = 1$.

```question
id: one-in-60-billion-1
type: multiple-choice
answer: 1

Which number, times 60,000,000,000, makes 1?

- 1/60,000,000,000
  - The reciprocal of 60 billion. A number times its reciprocal is 1.
- 60,000,000,000
  - That is the number itself. 60 billion times 60 billion is far
    more than 1.
- 1/60
  - 60 billion × 1/60 is one billion. The bottom needs to be 60
    billion.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start smaller. What times 4 is 1?
2. What times 60 is 1?
3. Now use 60 billion in place of 60.

**Think about:** a whole cut into 60 billion slices. How many slices
make the whole again?

**Try this next:** what times 1000 is 1?

</details>

So $f_{bt} = \frac{1}{60{,}000{,}000{,}000}$: one in 60 billion. Here
is what it means. Suppose life builds machines on one habitable-zone
planet in 60 billion. Then the Milky Way has made about one such world in
its whole history, and that one is ours. Suppose the fraction is
bigger. Then, Frank and Sullivan say, another world has likely done it
too, at some time in our galaxy's history.

## The way the paper writes it

Frank and Sullivan write one in 60 billion as $1.7 \times 10^{-11}$.
Python can show where that comes from. In Python, `60_000_000_000` is
60 billion. The low lines, `_`, between the digits help us read it.

```python exec
id: the-way-the-paper-writes-it-1
print(1 / 60_000_000_000)
```

Python prints `1.6666666666666667e-11`. The `e-11` means "times
$10^{-11}$". On [Negative powers: more on the
bottom](tutorial:more-on-the-bottom), $10^{-11}$ is one over $10^{11}$.
The paper rounds 1.666… to 1.7.

```question
id: the-way-the-paper-writes-it-2
type: fill-in-the-blank

1.7 × 10⁻¹¹ is
{a very small fraction|a very big number|a negative number}.
```

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say in your own words what a chain of
fractions does, and what the order of the fractions changes. Write it
in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A chain starts with a count and multiplies it by one fraction after
another. Each fraction keeps a part of the count, so the count gets
smaller. The order changes the bars in the middle, but not the end. A
number bigger than 1 in the chain makes the count bigger. When the end
must be exactly 1, the last step is the reciprocal of everything
before it. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five chains of your own? Start with a count, and narrow it
with fractions. Here are some ideas:

- the people in your class, or your street
- a chain whose end is exactly 1
- a chain with a number bigger than 1 in it
- a chain with a heart as the start number
- your own guesses for Drake's chain

Check each one with `Fraction`, or with bars on paper.

## Looking back

In the town, every step made the count smaller. In Drake's chain, two
steps can make it bigger. What must be true of a step, for it to make
the count bigger?

A challenge: the program below narrows the town one step at a time,
and prints each bar. Can you make a chain for your own school, or your
own street? Can you find a chain of three fractions that narrows 1000
down to exactly 1?

```python challenge
# A chain of fractions, one step at a time.
from fractions import Fraction

count = 1000
for kept in [Fraction(1, 2), Fraction(1, 5), Fraction(1, 10)]:
    count = count * kept
    print(count)
```

## Read more

Wikipedia's page on the [Drake
equation](https://en.wikipedia.org/wiki/Drake_equation) has Drake's
1961 guesses, and many later ones. The Simple English Wikipedia has a
[shorter page](https://simple.wikipedia.org/wiki/Drake_equation). Frank
and Sullivan's paper is [on arXiv](https://arxiv.org/abs/1510.08837).
Its Table 1 has the Milky Way's 60 billion planets, and the same count
for the whole Universe.
