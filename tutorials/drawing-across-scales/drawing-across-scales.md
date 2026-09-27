---
title: "Log scales: drawing things that differ by millions"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Log scales: drawing things that differ by millions

Here are the eight planets, drawn on one line by how far each one is
from the Sun. The numbers under the line are millions of kilometres
(km). Look at the left end of the line before you answer.

<img src="planets-normal.svg" alt="A line from 0 to 5,000, marked every 1,000, labelled millions of km from the Sun. Eight dots sit on it. Four dots crowd together near 0 and share one label: Mercury, Venus, Earth, Mars. Jupiter, Saturn, Uranus and Neptune are spread along the rest of the line, with Neptune near 4,500.">

```question
id: planets-normal-1
type: fill-in-the-blank

Near 0,
{four|two|eight}
planets crowd together.

They share
{one|four|no}
label.
```

## Equal gaps, equal amounts

On this line, the gap from 0 to 1,000 is the same length as the gap
from 1,000 to 2,000. Each equal gap is 1,000 million km. The way
numbers are spread along a line is called its *scale*. On this *normal
scale*, equal gaps are equal amounts.

These are the distances from NASA, in millions of km:

| Planet | Mercury | Venus | Earth | Mars | Jupiter | Saturn | Uranus | Neptune |
|---|---|---|---|---|---|---|---|---|
| From the Sun | 57.9 | 108.2 | 149.6 | 228.0 | 778.5 | 1432.0 | 2867.0 | 4515.0 |

```question
id: equal-gaps-equal-amounts-1
type: multiple-choice
answer: 1

Why do Mercury, Venus, Earth and Mars crowd together?

- All four are closer than 250 million km, and one gap is 1,000
  - Mars, the furthest of the four, is at 228.0. The four fit in a
    quarter of the first gap.
- They are the smallest planets
  - The dots show distance, not size. Every dot is the same size.
- They are very close to each other in space
  - Mars is about four times as far from the Sun as Mercury. The line
    has no room to show that.
```

## A longer line?

Could a longer line help? Mercury and Venus are 50.3 million km apart,
because 108.2 − 57.9 = 50.3. We draw that gap 1 cm long, so the two
dots do not touch.

```question
id: a-longer-line-1
type: multiple-choice
answer: 2

With 1 cm for every 50.3 million km, about how far from the Sun is the
dot for Neptune?

- About 9 cm
  - 9 cm is about 450 million km. That is between Mars and Jupiter.
- About 90 cm
  - 4515 ÷ 50.3 is about 90. That is 90 cm, longer than most tables.
- About 4,515 cm
  - That would be 1 cm for every million km. Here, 1 cm is 50.3
    million km.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Each centimetre stands for 50.3 million km.
2. Neptune is 4515 million km from the Sun.
3. How many 50.3s fit into 4515? A guess near a round number is
   enough.

**Think about:** 50 × 90 is 4500.

**Try this next:** about how far from the Sun would the dot for Mars
be?

</details>

A line 90 cm long does not fit on a page. And the four planets nearest the Sun
would still be close together at one end.

## A line of hops

Here are the same eight planets on a different line.

<img src="planets-hops.svg" alt="The same eight planets on a line marked 10, 100, 1,000 and 10,000, labelled millions of km from the Sun. The four marks are equally spaced. Every planet has its own label. Mercury sits between 10 and 100. Venus, Earth, Mars and Jupiter sit between 100 and 1,000. Saturn, Uranus and Neptune sit between 1,000 and 10,000.">

```question
id: a-line-of-hops-1
type: fill-in-the-blank

The marks are 10, 100, 1,000 and 10,000.

From one mark to the next is one hop of
{×10|+10|+100}.

On this line, the planets are
{all spread out|crowded at the left|crowded at the right}.
```

## Equal gaps, equal hops

```question
id: equal-gaps-equal-hops-1
type: multiple-choice
answer: 1

The gap from 10 to 100 and the gap from 100 to 1,000 have the same
length. Why?

- Each gap is one hop of ×10
  - 10 × 10 is 100, and 100 × 10 is 1,000. Each gap is one hop.
- Each gap is 90 million km
  - 100 − 10 is 90. But 1,000 − 100 is 900, ten times as much.
- The line was drawn too short to show the difference
  - The gaps are the same length on purpose. On this line, a gap
    stands for a hop, not an amount.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What do you multiply 10 by to get 100?
2. What do you multiply 100 by to get 1,000?
3. Is it the same multiplying?

**Think about:** on the first line, equal gaps were equal amounts. What
are they on this one?

**Try this next:** the gap from 1,000 to 10,000 is the same length too.
How many million km is it?

</details>

Now we can name what we found. On a normal scale, equal gaps are equal
amounts. On a *hops scale*, equal gaps are equal hops of ×10.

You met hops in [Counting hops: logarithms, how many times did we
multiply?](tutorial:how-many-hops). hops(10 → 1000) counts the hops of
×10 from 1 to 1000. It is 3. The usual way to write it is
$\log_{10} 1000 = 3$, and *log* is short for *logarithm*. So the usual
name for a hops scale is a *log scale*, or a *logarithmic scale*. You
can keep saying hops scale, if it feels calmer.

On a hops scale, each dot sits at its hops. The dot for a number sits
at hops(10 → the number).

{{include: setup/zen-calm-check.md}}

## Where Earth sits

Earth is 149.6 million km from the Sun.

```question
id: where-earth-sits-1
type: fill-in-the-blank

149.6 is between the marks
{100 and 1,000|10 and 100|1,000 and 10,000}.

So hops(10 → 149.6) is between
{2 and 3|1 and 2|149 and 150}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the nearest mark below 149.6, and the nearest mark above it.
2. hops(10 → 100) is 2, because 100 is two hops of ×10 from 1.
3. How many hops is the nearest mark above?

**Think about:** a number between two marks has hops between the
marks' hops.

**Try this next:** hops(10 → 4515), for Neptune, is between which two
whole numbers?

</details>

## Powers of ten on a hops line

On a hops line, each mark is a power of ten. The number 1 is $10^0$,
at 0 hops. Choose numbers, shapes or letters in the box under the
title.

<div class="dl-world" data-world="numbers">

```question
id: powers-of-ten-on-a-hops-line-1--numbers
type: fill-in-the-blank

10⁵ sits
{5|10|50}
gaps to the right of 1.

10⁵ and 10⁶ are
{one gap apart|five gaps apart|ten gaps apart}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: powers-of-ten-on-a-hops-line-1--squiggles
type: fill-in-the-blank

$10^\bgroup \heartsuit\egroup$ sits
{♡|10|10 × ♡}
gaps to the right of 1.

$10^\bgroup \heartsuit\egroup$ and $10^\bgroup \heartsuit + 1\egroup$ are
{one gap apart|♡ gaps apart|ten gaps apart}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: powers-of-ten-on-a-hops-line-1--letters
type: fill-in-the-blank

$10^\bgroup n\egroup$ sits
{n|10|10n}
gaps to the right of 1.

$10^\bgroup n\egroup$ and $10^\bgroup n + 1\egroup$ are
{one gap apart|n gaps apart|ten gaps apart}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start at 1. Each gap to the right is one hop of ×10.
2. The exponent counts the hops of ×10 from 1.
3. One more in the exponent is one more hop.

**Think about:** hops(10 → $10^5$) is 5.

**Try this next:** $10^{-3}$ is $\frac{1}{1000}$. Where does it sit?
To the right of 1, or to the left?

</details>

The shape or letter can be many different numbers, and each power of
ten still sits at its exponent.

## A checking machine

Python can find hops for us. `import math` gets Python's box of maths
tools ready. `math.log10` is hops(10 → …): it counts the hops of ×10.

```python exec
id: a-checking-machine-1
import math

print(math.log10(149.6))
print(math.log10(4515.0))
```

```predict
type: number
tolerance: 0.5

Before you run it: about how many hops of ×10 go from 1 to 4515, for
Neptune? A guess with one decimal place is enough.
```

It prints `2.1749315935284423` for Earth. That is a little more than 2
hops. For Neptune it prints `3.6546577546495245`, between 3 and 4. On
the hops line, Neptune sits a little more than halfway from the 1,000
mark to the 10,000 mark. Try other planets: Mercury is 57.9, and
Jupiter is 778.5.

## Planets you can draw

This program draws the planets as dots. They go across in order from
the Sun, 1 to 8. Their distance goes up, as in [Graphs: a pattern as
dots, a line or a curve](tutorial:a-pattern-as-dots).

```python exec
id: planets-you-can-draw-1
import matplotlib.pyplot as plt

planets = [1, 2, 3, 4, 5, 6, 7, 8]
distances = [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0]

plt.plot(planets, distances, "o")
plt.xlabel("planet, counting from the Sun")
plt.ylabel("millions of km from the Sun")
# plt.yscale("log")
```

```predict
type: choice

Before you run it: where will the first four dots be?

- Close together, near the bottom
- Evenly spaced up the side
  - Each planet is further than the last. Look at how much further,
    in the table.
- Near the top
  - The up scale must reach Neptune, at 4515. The first four are all
    under 250.
```

The first line, `import`, gets Python's drawing tools ready. The last
line starts with `#`, so Python skips it for now.

Now delete the `#` at the start of the last line, and run it again.
`plt.yscale("log")` makes the up scale a hops scale, so each equal gap
going up is one hop of ×10. The marks up the side are $10^2$, which is
100, and $10^3$, which is 1,000. Can you see every planet now?

## From a virus to the whole universe

Neptune is about 78 times as far from the Sun as Mercury. Some
things differ by far more. Here are five sizes, each in metres. Each comes from a source you
can check.

| Thing | Size in metres | Source |
|---|---|---|
| A virus, across | $10^{-7}$ (100 nanometres) | Wikipedia, "Virus": many are 20 to 300 nanometres |
| You, tall | between 1 and 2 | your own height |
| The Earth, across | $1.2756 \times 10^{7}$ (12,756 km) | NASA Planetary Fact Sheet |
| From the Earth to the Sun | $1.496 \times 10^{11}$ (149.6 million km) | NASA Planetary Fact Sheet |
| The observable universe, across | $8.8 \times 10^{26}$ | Wikipedia, "Observable universe" |

A *nanometre* is a billionth of a metre. The *observable universe* is
all the space we can see from the Earth, in every direction.

```question
id: from-a-virus-to-the-universe-1
type: multiple-choice
answer: 3

On a normal scale, we draw the virus 1 millimetre wide. How long
must the line be, to reach the size of the universe?

- About a kilometre
  - A kilometre is a million millimetres. That is only $10^6$ viruses
    side by side.
- About as long as the Earth is wide
  - The Earth is about $10^{14}$ viruses wide. The universe is much,
    much bigger than the Earth.
- About 10,000 times longer than the universe itself
  - The universe is about $8.8 \times 10^{33}$ viruses wide. At 1 mm
    each, that is 10,000 universes.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The universe is $8.8 \times 10^{26}$ metres. The virus is $10^{-7}$
   metres.
2. The number of viruses across the universe is the first number
   divided by the second.
3. Dividing by $10^{-7}$ is multiplying by $10^{7}$, from *Negative
   powers: more on the bottom*.

**Think about:** each virus becomes 1 millimetre. How many
millimetres are in a metre?

**Try this next:** on a normal scale with the universe 1 metre long,
could you see the Earth?

</details>

A normal scale cannot hold a virus and the universe at once. A hops
scale can.

```question
id: from-a-virus-to-the-universe-2
type: fill-in-the-blank

From $10^\bgroup -7\egroup$ metres up to 1 metre is
{7|−7|0}
hops of ×10.

From 1 metre up to $10^\bgroup 27\egroup$ metres is
{27|26|28}
hops.

So from the virus to the universe is about
{34|20|189}
hops.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $10^{-7}$ is $\frac{1}{10^7}$. Seven hops of ×10 take it back up to
   1.
2. From 1, each hop of ×10 adds one zero. $10^{27}$ has 27 zeros.
3. Add the two counts of hops.

**Think about:** the universe is $8.8 \times 10^{26}$ metres, which is
very close to $10^{27}$.

**Try this next:** how many hops from the virus to the Earth, about?

</details>

The universe is a little less than $10^{27}$ metres, so the count is a
little less than 34. Python gives 33.94, with `math.log10`. With 1 cm for each hop, the
whole hops ruler is about 34 cm long. That is a little longer than a
30 cm school ruler.

## Sizes you can draw

This program draws the five sizes on a hops scale. In Python,
`10 ** -7` means $10^{-7}$. Put your own height in metres in place of
1.7.

```python exec
id: sizes-you-can-draw-1
import matplotlib.pyplot as plt

names = ["virus", "you", "Earth", "Earth to Sun", "universe"]
metres = [10 ** -7, 1.7, 1.2756 * 10 ** 7, 1.496 * 10 ** 11, 8.8 * 10 ** 26]

plt.plot(names, metres, "o")
plt.yscale("log")
plt.ylabel("metres")
```

```predict
type: choice

Before you run it: which climb from one dot to the next will be the
biggest?

- From "Earth to Sun" up to the universe
- From the virus up to you
  - A virus and a person feel very far apart. Count the hops: about 7.
- From you up to the Earth
  - The Earth is huge next to you. Count the hops: about 7.
```

The biggest climb is from the Earth–Sun distance to the universe:
nearly 16 hops. And here is a surprise. From a virus up to you is
about 7 hops. From you up to the Earth is about 7 hops too. On a hops
scale, you are about halfway between a virus and the whole Earth.

Put a `#` in front of `plt.yscale("log")` and run it again. On the
normal scale, can you see any dot but the universe?

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say in your own words how a hops scale
is different from a normal scale. Write it in the Notes panel or on
paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

On a normal scale, equal gaps are equal amounts: +1,000 each time, for
example. On a hops scale, equal gaps are equal hops of ×10: 10, 100,
1,000. A number sits at its hops, hops(10 → the number), which is also
written $\log_{10}$ of the number. So a hops scale can hold very small
and very big things on one short line. Your way of saying it may be
clearer than ours.

</details>

## Make your own

Can you make a hops ruler of five things of your own? Choose things of
very different sizes: an ant, a bus, a mountain, the Moon. Find each
size in a real source, and write the source down. How many hops
is your ruler, from the smallest thing to the biggest?

## Looking back

On a normal scale, two dots at 100 and 200 are as far apart as dots at
1,000 and 1,100. On a hops scale, which pair is further apart? Why?

A challenge: the program below has the planets' distances and the
time each one takes to travel once around the Sun, in Earth days. The times
are from NASA's Planetary Fact Sheet. `plt.xscale("log")` makes the
across scale a hops scale. `plt.yscale("log")` does the same for the
up scale. Can you find a straight line? How many hops up does it climb
for each hop across?

```python challenge
# Each planet's distance from the Sun (millions of km) and its year (days).
import matplotlib.pyplot as plt

distances = [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0]
days = [88.0, 224.7, 365.2, 687.0, 4331, 10747, 30589, 59800]

plt.plot(distances, days, "o")
plt.xscale("log")
plt.yscale("log")
```

<details class="dl-answer"><summary>one way through it</summary>

With both scales set to hops, the eight dots make a straight line.
From Mercury to Neptune, the distance climbs 1.89 hops, and the time
climbs 2.83 hops. 2.83 ÷ 1.89 is about 1.5, which is 3/2. So for every
2 hops across, the line climbs 3 hops up.

So if a planet is 4 times as far from the Sun as another, its year is
$4^{3/2} = 8$ times as long. This is the kind of power from *Stretching the halfway steps: fractional
exponents, the top and the bottom*. Jupiter is 778.5 ÷ 149.6, about
5.2 times as far from the Sun as Earth. In Python,
`(778.5 / 149.6) ** (3/2)` prints about 11.87. Jupiter's year is 4331
days, which is 11.86 Earth years.

Johannes Kepler found this pattern and published it in 1619. It is
called *Kepler's third law*.

</details>

## Read more

NASA's [Planetary Fact
Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/) has the
distances, the sizes and the years of every planet. The Simple English
Wikipedia has a short page on the [logarithmic
scale](https://simple.wikipedia.org/wiki/Logarithmic_scale). The
sizes on this page come from NASA and from Wikipedia's pages on the
[virus](https://en.wikipedia.org/wiki/Virus) and the [observable
universe](https://en.wikipedia.org/wiki/Observable_universe).
Wikipedia's page on [Kepler's
laws](https://en.wikipedia.org/wiki/Kepler%27s_laws_of_planetary_motion)
has the planets on a hops graph like yours.

*Powers of Ten* is a short film from 1977 by Charles and Ray Eames. It
starts on the Earth, and moves away one hop of ×10 at a time, to the
whole universe. Then it comes back, one hop at a time, to a single
atom.
[Wikipedia](https://en.wikipedia.org/wiki/Powers_of_Ten_%28film_series%29)
describes it.
