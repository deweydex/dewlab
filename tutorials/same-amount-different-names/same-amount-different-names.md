---
title: "Equivalent fractions: the same amount, different names"
year: "2026-2027"
version: 2026.09.26.1
---

# Equivalent fractions: the same amount, different names

Here are three pizzas of the same size, cut in three different ways.
Some slices of each pizza are shaded. Look at the shaded part of each
pizza before you answer.

<img src="half-in-three-ways.svg" alt="Three pizzas of the same size. The first is cut into 2 slices with 1 shaded. The second is cut into 4 slices with 2 shaded. The third is cut into 8 slices with 4 shaded. In each, the right half of the pizza is shaded.">

```question
id: three-pizzas-1
type: multiple-choice
answer: 4

Which pizza has the most pizza shaded?

- The first: 1 of 2
  - Its one shaded slice is the biggest single slice. Look at how much
    of the circle it covers.
- The second: 2 of 4
- The third: 4 of 8
  - It has the most shaded slices, but each one is smaller.
- They all have the same amount shaded
  - In each picture, exactly the right half of the circle is shaded.
```

All three pizzas show the same amount: half a pizza. The slices are
different. So the names are different too: 1 of 2, 2 of 4, 4 of 8.

## A wall of fractions

Pizzas are round, so it is hard to compare their slices. Bars are
easier. Here, every bar is the same length: one whole. The second bar
is cut into halves. The third is cut into quarters. The last is cut into
eighths.

<img src="wall-of-halves.svg" alt="A fraction wall of four bars of the same length. The top bar is one whole. The next is cut into 2 halves, the next into 4 quarters, and the bottom into 8 eighths. The cuts line up: each half sits above 2 quarters, and each quarter above 2 eighths.">

```question
id: a-wall-of-fractions-1
type: fill-in-the-blank

Under one half, there are {2|4|1} quarters, and {4|2|8} eighths.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put your finger on the left half, in the second row.
2. Move your finger straight down to the quarters row. Count the
   quarters under the half.
3. Move down again, and count the eighths.

**Think about:** why the cuts in each row line up with the cuts above
them.

**Try this next:** how many eighths sit under one quarter?

</details>

## Shading the wall

Now the same wall, with half of each row shaded.

<img src="wall-shaded.svg" alt="The same fraction wall. In the halves row, 1 half is shaded. In the quarters row, 2 quarters are shaded. In the eighths row, 4 eighths are shaded. The shaded parts all end at the same place, the middle of the wall.">

All the shaded parts stop at the same place: the middle. So

$$\frac{1}{2} = \frac{2}{4} = \frac{4}{8}$$

Fractions that are the same amount are called *equivalent* fractions.
Equivalent means "equal in amount". The name changes. The amount stays
the same.

{{include: setup/zen-calm-check.md}}

## What happened to the numbers

Let's look at the numbers, from $\frac{1}{2}$ to $\frac{2}{4}$. We cut
every half into 2 smaller slices. This does two things at the same
time:

- The slices we have: 1 becomes 2.
- The slices in the whole: 2 becomes 4.

Both numbers were multiplied by 2. We did not add any pizza, and we did
not take any away. We only cut every slice again.

```question
id: what-happened-1
type: fill-in-the-blank

To go from 1/2 to 4/8, the top and the bottom were both multiplied by
{4|2|8}.
```

This works for any number of cuts. Cut every slice into $\heartsuit$
smaller slices. Then the top and the bottom are both multiplied by
$\heartsuit$:

$$\frac{1}{2} = \frac{1 \times \heartsuit}{2 \times \heartsuit}$$

The heart can be 2, or 10, or 1000. The amount of pizza stays the
same.

## Thirds

Here is another wall. This time the bars are cut into thirds, sixths
and twelfths. Two thirds of each bar is shaded.

<img src="wall-of-thirds.svg" alt="A fraction wall with a whole bar, then a bar cut into 3 thirds, then 6 sixths, then 12 twelfths. In the thirds row 2 thirds are shaded, in the sixths row 4 sixths, and in the twelfths row 8 twelfths. The shaded parts all end at the same place, two thirds of the way along.">

```question
id: thirds-1
type: fill-in-the-blank

Two thirds is the same amount as {4|3|5} sixths, and the same amount as
{8|6|4} twelfths.
```

## Going the other way

We can also go the other way, from small slices to big ones. Start
with $\frac{4}{8}$: 4 slices of a pizza cut into 8. Join the slices in
pairs. Now there are 2 slices of a pizza cut into 4.

$$\frac{4}{8} = \frac{2}{4} = \frac{1}{2}$$

This time, the top and the bottom were both *divided* by 2. Writing a
fraction with the smallest possible numbers is called *simplifying* it.
The amount stays the same. Only the name gets shorter.

```question
id: going-the-other-way-1
type: multiple-choice
answer: 3

What is the simplest name for 6/12?

- 6/12
  - That is the same amount, but it can be shorter.
- 3/6
  - That is the same amount, and shorter. Can you divide the top and
    the bottom again?
- 1/2
  - 6 is half of 12, so the amount is one half.
```

## A machine that checks

Python has a tool for fractions. It is called `Fraction`. It always
writes a fraction with its simplest name. So we can use it to check our
work.

```python exec
id: a-machine-that-checks-1
from fractions import Fraction

print(Fraction(4, 8))
```

```predict
type: choice

Before you run it: `Fraction(4, 8)` means four eighths. What will
Python print?

- 4/8
  - Python was given 4 and 8, so it could print them back.
- 1/2
- 0.5
  - 0.5 is also half, written as a decimal. Some tools print that.
```

Python printed 1/2. That is the simplest name for four eighths. The
first line, `from fractions import Fraction`, gets the tool ready. We
only need it once on this page.

Now try your own fractions. Change the two numbers and run it again.
Can you find a fraction that Python cannot make any simpler? What does
it print for `Fraction(12, 12)`?

```python exec
id: a-machine-that-checks-2
print(Fraction(6, 12))
print(Fraction(8, 12))
print(Fraction(2, 4) == Fraction(4, 8))
```

The last line asks Python a question: are these two fractions the same
amount? `True` means yes. `==` is how Python asks "is this equal to
that?"

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say the idea of this page in your own
words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

The same amount can have many names. Multiply the top and the bottom of
a fraction by the same number. This cuts every slice again, and gives a
new name for the same amount. Divide the top and the bottom by the same
number. This joins slices together, and gives a shorter name. Your way
of saying it may be clearer than ours.

</details>

## Make your own

Can you find five different names for three quarters? Can you find one
with a bottom number bigger than 100? And one with a shape in it: three
quarters, with every slice cut into $\heartsuit$ pieces?

## Looking back

On the first page, $\frac{3}{3}$ and $\frac{12}{12}$ were both one
whole pizza. How is that the same idea as this page?

A challenge: how many names does one third have, with a bottom number
of 30 or less? The program below looks at every fraction with a bottom
number up to 30. Can you change it, so that it prints only the fractions
that are the same amount as one third?

```python challenge
# Every name for one third, with a bottom number up to 30.
from fractions import Fraction

for bottom in range(1, 31):
    for top in range(0, bottom + 1):
        print(top, "/", bottom, "is", Fraction(top, bottom))
```

## Read more

The wall of bars on this page is called a *fraction wall*. Many
classrooms have one made of wood or card. Wikipedia's page on fractions
has a short section on
[equivalent fractions](https://en.wikipedia.org/wiki/Fraction#Equivalent_fractions).
