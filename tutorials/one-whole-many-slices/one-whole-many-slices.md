---
title: "Fractions: one whole pizza, many slices"
year: "2026-2027"
version: 2026.09.26.1
---

# Fractions: one whole pizza, many slices

The first question looks very easy. It is not a trick. This page works
in small steps, and this is the first one.

<img src="one-pizza.svg" alt="A round pizza, not cut into slices.">

```question
id: one-pizza-1
type: fill-in-the-blank

The picture shows {one|two|half a} pizza.
```

## Cutting it again

Here is the same pizza three times. The first is cut into 2 equal
slices, the next into 4, and the last into 8.

<img src="cut-again.svg" alt="Three pizzas of the same size, side by side. The first is cut into 2 equal slices, the second into 4, the third into 8.">

```question
id: cutting-it-again-1
type: multiple-choice
answer: 3

The pizza on the right has more slices than the one on the left. Does
it have more pizza?

- Yes, more slices means more pizza
  - More pieces can feel like more. Look at the outside edge of each
    pizza: is any of them bigger?
- No, it has less pizza
  - Cutting does not take any pizza away. Each slice is smaller, but
    there are more of them.
- No, it has the same amount of pizza
  - The three circles are the same size. Only the cuts are different.
```

With more slices, each slice is smaller. The whole pizza stays the same
size. This is the most important idea on this page. We will use it
again.

## A name for one slice

Four friends share one pizza, cut into 4 equal slices. Each friend gets
one slice, shaded below.

<img src="one-of-four.svg" alt="A pizza cut into 4 equal slices. One slice is shaded.">

```question
id: a-name-for-one-slice-1
type: multiple-choice
answer: 2

Which sentence describes the shaded slice?

- It is 4 pizzas
  - There are 4 slices, but together they make only one pizza.
- It is 1 out of 4 equal slices of one pizza
  - One slice, out of the 4 the pizza was cut into.
- It is half the pizza
  - Half would be 2 of the 4 slices. Try shading 2 in your head.
```

We write one slice of a pizza cut into 4 like this:

$$\frac{1}{4}$$

We say "one quarter", or "one out of four". A number written like this
is called a *fraction*.

- The number on the **bottom** says how many equal slices the whole was
  cut into. Here, 4.
- The number on the **top** says how many of those slices we have. Here,
  1.

You will also see a fraction on one line, with a slash between the two
numbers: 1/4. That slash is half of this module's name.

## More than one slice

<img src="more-of-four.svg" alt="Four pizzas, each cut into 4 equal slices. The first has 1 slice shaded, the second 2, the third 3, and the fourth all 4.">

The bottom number stays 4 in every picture, because every pizza is cut
into 4. Only the top number changes.

```question
id: more-than-one-slice-1
type: fill-in-the-blank

Three shaded slices of a pizza cut into 4 is written {3/4|4/3|1/3}.
```

```question
id: more-than-one-slice-2
type: multiple-choice
answer: 2

The last pizza has all 4 of its 4 slices shaded. That is 4/4 of a
pizza. How much pizza is it?

- A quarter of a pizza
  - One quarter is one slice. This pizza has all four.
- One whole pizza
  - Every slice of the pizza is there, so it is the whole pizza.
- Four pizzas
  - There are four slices, and all four come from the same pizza.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the pizzas in the last picture. There is one.
2. Count its shaded slices. There are 4.
3. Count its slices that are not shaded. There are none.

**Think about:** if every slice is shaded, how much of the pizza is
missing?

**Try this next:** a pizza cut into 6 slices, all 6 shaded. How much
pizza is that?

</details>

{{include: setup/zen-calm-check.md}}

## Every slice

Here are four more pizzas. Each one is cut in a different way. In each
one, every slice is shaded.

<img src="every-slice.svg" alt="Four pizzas with every slice shaded. The first is cut into 3 slices, the second into 5, the third into 8, the fourth into 12.">

```question
id: every-slice-1
type: multiple-choice
answer: 4

Which of these is one whole pizza: 3/3, 5/5, 8/8 or 12/12?

- Only 3/3
  - 3/3 is one whole pizza. Look at the others: is any slice missing?
- Only 12/12
  - 12/12 has the most slices, but each slice is smaller.
- None of them
  - Each picture shows a full circle, with nothing missing.
- All of them
  - In each one, every slice of the pizza is there.
```

## The idea of this page

Here is what the pictures show. Cut a pizza into any number of equal
slices. All of those slices together make the whole pizza.

$$\frac{3}{3} = 1 \qquad \frac{5}{5} = 1 \qquad \frac{8}{8} = 1 \qquad \frac{12}{12} = 1$$

Here is the same idea, starting from one slice. Cut a pizza into 5
slices. Each slice is $\frac{1}{5}$. Put 5 of them together, and you have
the whole pizza again.

$$\underbrace{\frac{1}{5} + \frac{1}{5} + \frac{1}{5} + \frac{1}{5} + \frac{1}{5}}_{5 \text{ slices}} = 1$$

The number of slices does not matter. So we can use a shape in place of
the number. A heart, $\heartsuit$, can be 3, or 12, or a million. It can
be any number, and

$$\frac{\heartsuit}{\heartsuit} = 1$$

That is the idea of this page. It is one of the most useful ideas in
maths. You will see it again with powers, and again with logarithms.

```question
id: the-idea-of-this-page-1
type: fill-in-the-blank

Seven slices, each one seventh of a pizza, make {1|7|1/7} whole pizza.
```

```question
id: the-idea-of-this-page-2
type: fill-in-the-blank

A pizza is cut into ♡ equal slices. Then ♡ of those slices make
{1|♡|1/♡} whole pizza.
```

## Very thin slices

<img src="very-thin.svg" alt="Three pizzas, each with one slice shaded. The first is not cut, so the whole pizza is shaded. The second is cut into 10 slices, the third into 24, and the one shaded slice gets thinner each time.">

More slices means thinner slices.

```question
id: very-thin-slices-1
type: multiple-choice
answer: 2

A pizza is cut into 1000 equal slices. Each slice is 1/1000 of the
pizza. How much pizza do all 1000 slices make?

- A very small amount
  - One slice is very small. There are a thousand of them, though.
- One whole pizza
  - 1000/1000 is every slice of one pizza.
- 1000 pizzas
  - All 1000 slices come from the same single pizza.
```

One slice of 1000 is almost nothing. It is too thin to hold. But
1000 of these thin slices still make a whole pizza.

{{include: setup/zen-calm-check.md}}

## A pizza you can change

The box below is a small Python program. It draws a pizza. You do not
need to understand the code. The two numbers at the top say how many
slices to cut, and how many slices to shade. Make a guess before you
press **Run**.

```python exec
id: a-pizza-you-can-change-1
import matplotlib.pyplot as plt

slices = 6
shaded = 6

colours = ["orange"] * shaded + ["none"] * (slices - shaded)
plt.pie([1] * slices, colors=colours,
        wedgeprops={"edgecolor": "grey", "linewidth": 2})
```

```predict
type: choice

Before you run it: with 6 slices and all 6 shaded, what will the
picture show?

- One whole pizza, all orange
- Six pizzas
  - Six slices can sound like six of something.
- Six orange dots
```

Now change the numbers and run it again. The first line, `import`,
gets the drawing tools ready. You do not need to change it.

- Can you make exactly half of the pizza orange? How many different
  ways can you find?
- What happens with `slices = 1` and `shaded = 1`?
- What happens with `slices = 100`?

<details class="dl-answer"><summary>What each line does</summary>

- `slices = 6` and `shaded = 6` keep the two numbers under names we can
  read.
- `colours = ...` makes a list of colours, one for each slice: "orange"
  for each shaded slice, and "none" for the rest.
- `plt.pie(...)` draws a circle cut into equal slices, and paints each
  slice with its colour from the list.

</details>

## Your rule, in your words

Before you read our version, say the idea of this page in your own
words. You can write it in the Notes panel or on paper, or say it
aloud.

<details class="dl-answer"><summary>one way to say it</summary>

Cut a whole into equal slices. All the slices together make the whole
again. So a fraction with the same number on the top and on the bottom
is exactly 1. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five fractions that look big or strange, but are exactly
one whole pizza? Here is one to start: $\frac{250}{250}$. Can you make
one with a heart in it? And one with a letter?

## Looking back

The pizza with 8 slices has more pieces than the pizza with 2. But it
has the same amount of pizza. Why? A friend says "more slices means more
pizza". What picture would you show your friend?

A challenge: draw two pizzas. Cut one into 4 slices and shade 2. Cut
the other into 8 slices. How many of the 8 slices must you shade, so
that both pizzas have the same amount shaded? The next page asks this
question too.

```python challenge
# Two pizzas. How many of the 8 slices match 2 of the 4?
import matplotlib.pyplot as plt

slices = 4
shaded = 2

colours = ["orange"] * shaded + ["none"] * (slices - shaded)
plt.pie([1] * slices, colors=colours,
        wedgeprops={"edgecolor": "grey", "linewidth": 2})
```

## Read more

Montessori classrooms teach this idea with *fraction insets*. These are
metal circles that fit into a frame. One circle is whole. The next is
cut into 2 pieces, the next into 3, and so on, up to 10. [Wikipedia's page on
fractions](https://en.wikipedia.org/wiki/Fraction) has the words and
signs people use for them around the world.
