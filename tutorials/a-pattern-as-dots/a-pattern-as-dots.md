---
title: "Graphs: a pattern as dots, a line or a curve"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Graphs: a pattern as dots, a line or a curve

Here are two lists of numbers, each drawn as a picture. The list is
written under its picture. Look at the two pictures before you answer.

<img src="two-patterns.svg" alt="Two plots side by side. Each has the numbers 1 to 5 along the bottom, and a scale from 0 to 32 going up the left side. The left plot, labelled 2, 4, 6, 8, 10, has five dots that climb in a straight line. The right plot, labelled 2, 4, 8, 16, 32, has five dots that start low and climb faster and faster, in a curve.">

```question
id: two-patterns-1
type: multiple-choice
answer: 1

In which picture are the dots in a straight line?

- The left picture, 2, 4, 6, 8, 10
  - A ruler laid along these dots would touch all five.
- The right picture, 2, 4, 8, 16, 32
  - These dots climb too. Compare the climb of the last two dots with
    the climb of the first two.
- Both pictures
  - Both lists climb. On the right, the last dots climb much faster
    than the first ones.
```

## A dot for each step

Each list follows a rule. We call a list like this a *pattern*. Each
number in it is one *step* of the pattern: the first step, the second
step, and so on. The number at a step is its *value*.

The picture gives each step a dot. The step number goes across: 1, 2,
3, 4, 5. The value goes up. This is the grid from *Coordinates: two
lines at right angles*: first across, then up.

```question
id: a-dot-for-each-step-1
type: fill-in-the-blank

In the left picture, the dot for step 3 is
{6|3|8}
up.

In the right picture, the dot for step 3 is
{8|6|3}
up.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the list under the left picture: 2, 4, 6, 8, 10.
2. Count along the list to the third number.
3. The third number is the value at step 3. It is how far up the dot
   is.

**Think about:** the step number tells you how far across. The value
tells you how far up.

**Try this next:** in the right picture, how far up is the dot for
step 5?

</details>

## The gaps on the left

The *gap* between two values is how much bigger the second one is. In
2, 4, 6, 8, 10, the first gap is 2, because 4 − 2 = 2. In the picture,
a gap is how far one dot climbs above the dot before it.

```question
id: the-gaps-on-the-left-1
type: fill-in-the-blank

6 − 4 is
{2|6|10}.

8 − 6 is
{2|8|14}.

10 − 8 is
{2|10|18}.

So the gaps in 2, 4, 6, 8, 10 are
{all the same|bigger and bigger|smaller and smaller}.
```

## The gaps on the right

Now the same question for 2, 4, 8, 16, 32.

```question
id: the-gaps-on-the-right-1
type: fill-in-the-blank

4 − 2 is
{2|4|6}.

8 − 4 is
{4|2|12}.

16 − 8 is
{8|2|24}.

32 − 16 is
{16|2|48}.

So the gaps in 2, 4, 8, 16, 32 are
{bigger and bigger|all the same|smaller and smaller}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take two numbers next to each other in the list, like 8 and 16.
2. Take the smaller one away from the bigger one.
3. Write the gap down, and move one step along the list.

**Think about:** the gaps on the left were 2, 2, 2, 2. How are these
gaps different?

**Try this next:** what are the gaps in 1, 3, 9, 27?

</details>

## Why a line, and why a curve?

On the left, the gaps are 2, 2, 2, 2. On the right, they are 2, 4, 8,
16. This is the main idea of the page. There is no hurry.

```question
id: why-a-line-1
type: multiple-choice
answer: 1

Why are the dots on the left in a straight line?

- Each dot climbs the same amount above the dot before it
  - Every gap is 2, and every step across is 1. So each dot is 1
    across and 2 up from the dot before it.
- All the numbers are even
  - 2, 4, 8, 16, 32 are all even too, and they make a curve.
- The numbers are small
  - Small numbers can make a curve too. 1, 2, 4, 8 is a curve.
```

```question
id: why-a-curve-1
type: fill-in-the-blank

On the right, each dot climbs
{more than|the same as|less than}
the dot before it.

So the dots bend, and make
{a curve|a straight line}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put a finger on the first dot on the right.
2. Move to the next dot. How far did your finger climb?
3. Do the same for each dot. Is each climb the same as the last one?

**Think about:** a straight line climbs the same amount for each step
across. What happens to the line when the climbs grow?

**Try this next:** what shape would 10, 20, 30, 40 make?

</details>

Now we can name what we found. 2, 4, 6, 8, 10 *adds* 2 at each step.
2, 4, 8, 16, 32 *multiplies* by 2 at each step.

- Adding the same amount at each step makes equal gaps. The dots make
  a straight line.
- Multiplying by the same amount at each step makes bigger and bigger
  gaps. The dots make a curve.

A picture with a dot for each pair of numbers is called a *graph*. The
two pictures at the top of this page are graphs.

{{include: setup/zen-calm-check.md}}

## The folded paper

You have met 2, 4, 8, 16, 32 before, in [Powers: the long way and the
short way](tutorial:the-long-way). Each fold of a sheet of paper
doubles the pieces. One fold makes 2 pieces, two folds make 4, and five
folds make $2^5 = 32$. So the step number is the number of folds.

```question
id: the-folded-paper-1
type: fill-in-the-blank

After 6 folds, there are
{64|34|36}
pieces.

The gap from 32 to that number is
{32|2|6}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. After 5 folds, there are 32 pieces.
2. One more fold doubles the pieces.
3. Then find the gap: take 32 away from the new number.

**Think about:** each fold doubles the pieces. What does it do to the
gap?

**Try this next:** after 7 folds, how many pieces are there? What is
the gap from 6 folds?

</details>

Look at the gaps again: 2, 4, 8, 16, 32. They are the doubling pattern
itself. The gaps double too. So each dot climbs twice as far as the one
before, and the curve gets *steeper*: it climbs more for each step
across.

## Shapes and letters

Choose numbers, shapes or letters in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: shapes-and-letters-1--numbers
type: fill-in-the-blank

In 5, 8, 11, 14, each step adds
{3|5|8}.

So its dots make
{a straight line|a curve}.

In 3, 9, 27, 81, each step multiplies by
{3|6|9}.

So its dots make
{a curve|a straight line}.
```

</div>

<div class="dl-world" data-world="squiggles">

Here ♡ and △ are both numbers bigger than 1.

```question
id: shapes-and-letters-1--squiggles
type: fill-in-the-blank

In ♡, ♡ + △, ♡ + △ + △, ♡ + △ + △ + △, each step adds
{△|♡|♡ + △}.

So its dots make
{a straight line|a curve}.

In ♡, ♡ × △, ♡ × △ × △, ♡ × △ × △ × △, each step multiplies by
{△|♡|2}.

So its dots make
{a curve|a straight line}.
```

</div>

<div class="dl-world" data-world="letters">

Here a and r are both numbers bigger than 1. We write ar for a × r.

```question
id: shapes-and-letters-1--letters
type: fill-in-the-blank

In a, a + d, a + 2d, a + 3d, each step adds
{d|a|a + d}.

So its dots make
{a straight line|a curve}.

In a, ar, ar², ar³, each step multiplies by
{r|a|2}.

So its dots make
{a curve|a straight line}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take the first two steps. What changed from the first to the
   second?
2. Is that change an adding, or a multiplying?
3. Check the next two steps. Is it the same change?

**Think about:** adding the same amount makes equal gaps. Multiplying
makes bigger and bigger gaps.

**Try this next:** does 1, 10, 100, 1000 make a line or a curve?

</details>

The ♡ and the △ can be many different numbers, and the shape of the
dots stays the same. That is all a letter in algebra means.

## Dots you can change

The box below is a small Python program. Python is a language for
computers. The program draws a graph of a pattern. You do not need to
understand all of it. The two lists near the top are the steps and
their values. Make a guess before you press **Run**.

```python exec
id: dots-you-can-change-1
import matplotlib.pyplot as plt

steps = [1, 2, 3, 4, 5]
values = [3, 6, 9, 12, 15]

plt.plot(steps, values, "o")
plt.xlabel("step")
plt.ylabel("value")
```

```predict
type: choice

Before you run it: the values are 3, 6, 9, 12, 15. What shape will the
five dots make?

- A straight line
- A curve that gets steeper
  - The values grow, and growing can feel like a curve. Look at the
    gaps.
- No clear shape at all
  - Each value follows a rule, so each dot follows the rule too.
```

The first line, `import`, gets Python's drawing tools ready.
`plt.plot(steps, values, "o")` puts a dot, "o", at each step and its
value. The last two lines write a name on each side of the graph.

Now change the values and run it again. Keep five numbers in the list.

- What happens with `values = [3, 6, 12, 24, 48]`?
- What happens with `values = [5, 5, 5, 5, 5]`? What does each step
  add?
- Can you make a straight line that climbs faster than the first one?

## Ten steps

Here are both patterns again, now with ten steps each. The program
draws them on the same graph, with one up scale for both.

```python exec
id: ten-steps-1
import matplotlib.pyplot as plt

steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
adding = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
doubling = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

plt.plot(steps, adding, "o", label="adding 2")
plt.plot(steps, doubling, "o", label="doubling")
plt.legend()
```

```predict
type: choice

Before you run it: where will the ten dots for adding 2 be?

- Almost flat, along the bottom
- Above the doubling dots
  - The adding pattern starts level with the doubling one. Which one
    reaches the bigger number at step 10?
- About half as high as the doubling dots
  - At step 10, adding reaches 20, and doubling reaches 1024.
```

`label` gives each list a name. `plt.legend()` shows the names in a
small box, with the colour of each list's dots.

The doubling pattern reaches 1024, so the up scale goes past 1000. On
that scale, 20 is very close to 0. The adding dots still make a
straight line. It is a very flat one. After ten steps, adding 2 has
reached 20, and doubling has reached $2^{10} = 1024$.

## A pattern that goes down

This one goes a step past the page. Here is a pattern that halves at
each step:

$$32,\ 16,\ 8,\ 4,\ 2,\ 1,\ \tfrac{1}{2}$$

Each dot is lower than the one before. So now each gap is a *drop*:
how much smaller the next value is.

```question
id: a-pattern-that-goes-down-1
type: fill-in-the-blank

The drops are 16, 8, 4, 2, 1 and
{1/2|1|0}.

Each drop is
{smaller than the last|the same as the last|bigger than the last}.

The next value after 1/2 is
{1/4|0|−1/2}.
```

```question
id: a-pattern-that-goes-down-2
type: multiple-choice
answer: 2

If the pattern keeps halving, do the dots ever reach 0?

- Yes, at the next step
  - The next value is half of 1/2, which is 1/4. That is small, but it
    is not 0.
- No, they come closer and closer to 0
  - Half of something is never nothing. Each value is small, but it is
    still more than 0.
- Yes, after many steps
  - After ten halvings of 1, the value is 1/1024. It is very small, but
    it is still more than 0.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take 1/2, and halve it. Then halve that.
2. Is any of the answers 0?
3. Think of the folded paper. Each fold makes the pieces smaller.

**Think about:** can half of a piece of paper ever be no paper at all?

**Try this next:** is the pattern 32, 28, 24, 20 a line or a curve?
Does it reach 0?

</details>

The drops get smaller at each step, so this curve flattens as it comes
down. It comes closer and closer to 0, and never reaches it. In
*Powers: the long way and the short way*, the pieces of folded paper
did the same.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say in your own words why one pattern
makes a straight line and the other makes a curve. Write it in the
Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

Draw a dot for each step: the step number across, the value up. The
gap between two values is how far a dot climbs above the one before.
When each step adds the same amount, every gap is the same, so the dots
make a straight line. When each step multiplies by the same amount,
the gaps grow, so the dots make a curve that gets steeper. Your way of
saying it may be clearer than ours.

</details>

## Make your own

Can you make five patterns of your own, and say what each graph looks
like before you draw it? Try one that adds, one that multiplies, and
one that goes down. Try one that adds 0. Then draw them in the box
above, and check.

## Looking back

A friend says: "A pattern that grows always makes a straight line."
What pattern would you show them? What would you say about its gaps?

A challenge: the program below draws the halving pattern. Can you draw
a pattern that goes down in a straight line on the same graph? What
happens to the straight line when it passes 0? *The number line: whole
numbers, fractions and negatives* has the numbers below 0.

```python challenge
# A pattern that halves at each step, drawn as dots.
import matplotlib.pyplot as plt

steps = [1, 2, 3, 4, 5, 6, 7]
halving = [32, 16, 8, 4, 2, 1, 1/2]

plt.plot(steps, halving, "o", label="halving")
plt.legend()
```

## Read more

A pattern that adds the same amount is often called an *arithmetic
sequence*. A pattern that multiplies by the same amount is a
*geometric sequence*. Maths is Fun has a short page on
[sequences](https://www.mathsisfun.com/algebra/sequences-series.html)
with both kinds. Growing by multiplying, like the doubling curve, is called
*exponential growth*. The Simple English Wikipedia has a page on
[exponential growth](https://simple.wikipedia.org/wiki/Exponential_growth).
