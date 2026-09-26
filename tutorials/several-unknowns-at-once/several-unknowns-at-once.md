---
title: "Several unknowns at once: simultaneous equations"
year: "2026-2027"
version: 2026.09.26.1
covers:
  two-facts-two-unknowns:
    covers: [MIT-1.12]
    touches: [MIT-6.6]
  two-lines-that-cross:
    covers: [MIT-1.12]
    touches: [MIT-3.2]
  elimination-one-unknown-at-a-time:
    covers: [MIT-1.12]
  one-formula-for-every-pair:
    covers: [MIT-1.12]
    touches: [PDP-LO8]
  when-there-is-no-single-answer:
    covers: [MIT-1.12]
  three-unknowns:
    covers: [MIT-1.12]
---

# Several unknowns at once: simultaneous equations

A website's server keeps a log. Tonight's log says two things: it
answered 230 requests, and it sent 2,060 KB (kilobytes) of data. Each
request was for a small image, which is 12 KB, or for a page of text,
which is 5 KB. The log did not keep count of which kind was which. How
many images did it send, and how many pages of text?

Before you read on, take a guess. You have two facts and two things you
do not know. Is that enough to find them? It is exactly enough, and
this page shows why.

On this page we:

- see that one fact about two unknowns has many answers, and two facts
  can have just one
- draw each fact as a line, and find the answer where the lines cross
- solve by elimination, said in words and then in symbols
- turn elimination into a formula, and add `solve_simultaneous` to the
  toolkit
- see when two facts have no single answer, and draw why
- take the same idea to three unknowns

> **The space we're in.** Equations where each unknown is only
> multiplied by a number: no squares, no unknowns multiplied together.
> Each such equation in $x$ and $y$ draws a straight line on a flat
> plane. The answer must make every equation true at once, and we check that by substituting it back into
> each one. Your toolkit is loaded, with `plot_rule`, `solve_linear` and
> `vertex` from earlier in this unit.

## Warm-up

The first question is from
[Solving for x](tutorial:solving-for-x), and the second from
[The top of the curve](tutorial:the-top-of-the-curve#a-curve-that-turns).

```question
id: several-unknowns-warm-up-1
type: fill-in-the-blank

`solve_linear(a, b)` gives the $x$ where $ax + b = 0$. So
`solve_linear(2, -10)` gives {5}.
```

```question
id: several-unknowns-warm-up-2
type: multiple-choice
answer: 1

The parabola $y = x^2 - 8x + 3$ has its vertex at $x = -\frac{b}{2a}$.
Where is that?

- $x = 4$
  - b is −8, so −b is 8, and 2a is 2: 8 ÷ 2 is 4.
- $x = -4$
  - This takes b as 8, leaving out its minus sign; b is −8, so −b is 8.
- $x = 8$
  - This is −b, before dividing by 2a.
- $x = 3$
  - 3 is the height of the curve at x = 0, not a place on the x-axis.
```

## Two facts, two unknowns

Let's name what we do not know. Call the number of image requests $a$
and the number of text requests $c$. The first fact, in symbols, is

$$a + c = 230$$

Is that enough to find $a$? Try some pairs: 200 images and 30 pages
of text, or 115 and 115. Each one makes 230. The cell counts every
pair of whole numbers that fits. How many do you expect?

```python exec
id: several-unknowns-facts-1
pairs = []
for images in range(0, 231):
    texts = 230 - images
    pairs.append((images, texts))

print(len(pairs), "pairs fit the first fact")
print(pairs[:3], "...", pairs[-2:])
```

There are 231 pairs, from no images to no text. One fact about two
unknowns leaves many answers. The second fact is the data: each image
sent 12 KB and each page of text 5 KB.

$$12a + 5c = 2060$$

Which of the 231 pairs fits this fact too? We can check them one at a
time, as a linear search does on
[Finding things fast](tutorial:finding-things-fast).

```python exec
id: several-unknowns-facts-2
for images, texts in pairs:
    if 12 * images + 5 * texts == 2060:
        print(images, "images and", texts, "pages of text")
```

Exactly one pair fits both: 130 images and 100 pages of text. Two
equations that must be true at the same time, for the same unknowns,
are called *simultaneous equations*. The pair that makes them all true
is their *solution*.

The search worked because the answers had to be whole numbers under
231. If the unknowns were measured amounts, such as sizes in megabytes,
there would be far too many cases to try. We need a method.

## Two lines that cross

On [Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
two servers were equally fast where their graphs crossed. Each fact
here can be written as a rule that gives $c$ from $a$:

- from the count, $c = 230 - a$;
- from the data, $5c = 2060 - 12a$, so $c = \frac{2060 - 12a}{5}$.

Each is a linear function, so each graph is a straight line. What do
you expect to see where they meet?

```python exec
id: several-unknowns-lines-1
import matplotlib.pyplot as plt

def texts_from_count(images):
    return 230 - images

def texts_from_data(images):
    return (2060 - 12 * images) / 5

plot_rule(texts_from_count, 0, 230)
plot_rule(texts_from_data, 0, 230)
plt.plot(130, 100, "o")
plt.xlabel("image requests")
plt.ylabel("text requests")
plt.legend()
```

Every point on the first line fits the count. Every point on the
second fits the data sent. Only one point is on both: the crossing, at
$(130, 100)$. To solve simultaneous equations in two unknowns, we find
where two lines cross.

## Elimination: one unknown at a time

The picture shows the answer. To get it exactly, we use the rule from
[Running a formula backwards](tutorial:running-a-formula-backwards#the-same-move-on-both-sides):
any move is allowed, if we do it to both sides. The plan, in words:

1. Change one equation so that $c$ has the same number in front of it
   in both.
2. Take one equation away from the other. The $c$ terms cancel, and
   only $a$ is left.
3. Solve for $a$.
4. Put $a$ back into either equation, and find $c$.

This method is called *elimination*, because step 2 eliminates one
unknown. In symbols, step 1 multiplies $a + c = 230$ by 5:

$$5a + 5c = 1150$$

Step 2 takes that away from $12a + 5c = 2060$:

$$7a = 910$$

Step 3 divides by 7, so $a = 130$. Step 4 puts 130 into $a + c = 230$,
so $c = 100$. The order matters. We cannot find $c$ in step 4 until
step 3 has found $a$.

Now the rule of this unit: substitute back, into both equations. Which
lines will print `True`?

```python exec
id: several-unknowns-elimination-1
images = 910 / 7
texts = 230 - images
print(images, texts)
print(images + texts == 230)
print(12 * images + 5 * texts == 2060)
```

Both are `True`. The equation we used in step 4 must fit, because we
built $c$ from it. The second check tells us more.

<aside class="dl-note" id="several-unknowns-note-nine-chapters">

**Two thousand years of elimination.** A Chinese book, *The Nine
Chapters on the Mathematical Art*, put together about two thousand
years ago, solves problems with several unknowns by laying their
numbers out on a counting board in columns and taking one column from
another. That is elimination, long before Europe had a name for it.

</aside>

### Your turn

In a game, a level hides coins worth 4 points and gems worth 6 points.
One player collected 45 of them and scored 222 points.

1. Name the two unknowns, and write the two facts as equations.
2. Eliminate one unknown, by hand, in the steps above.
3. Substitute your answer back into both equations in the cell below.

```python exec
id: several-unknowns-elimination-your-turn
# Your two unknowns, and the check in both equations
```

## One formula for every pair

Elimination is the same four steps every time, so we can do it once,
with letters, and get a formula. Write any two such equations as

$$a_1 x + b_1 y = c_1$$
$$a_2 x + b_2 y = c_2$$

The small numbers are part of the names: $a_1$ is "the $a$ of the first
equation". To eliminate $y$, multiply the first equation by $b_2$ and
the second by $b_1$, then take one from the other. The $y$ terms cancel
and leave

$$x = \frac{c_1 b_2 - c_2 b_1}{a_1 b_2 - a_2 b_1}$$

Eliminating $x$ the same way gives

$$y = \frac{a_1 c_2 - a_2 c_1}{a_1 b_2 - a_2 b_1}$$

This pair of formulas is called *Cramer's rule*. Both share the same
bottom, $a_1 b_2 - a_2 b_1$, which is called the *determinant*. In
words: write the four numbers in front of $x$ and $y$ in a square, with
$a_1$ and $b_1$ on top and $a_2$ and $b_2$ below. Multiply along one
diagonal, $a_1$ times $b_2$, then along the other, $a_2$ times $b_1$,
and take the second product from the first.

Here is that square for the two facts about the requests, where the
unknowns are $a$ and $c$.

<img src="the-determinant.svg" alt="The two equations a + c = 230 and 12a + 5c = 2060, and beside them a square of the four numbers in front of a and c. On top are 1 and 1, named a₁ and b₁. Below are 12 and 5, named a₂ and b₂. A solid arrow runs along one diagonal, from 1 to 5, and a dashed arrow runs along the other, from 12 to 1. Beside the square: one diagonal gives 1 × 5 = 5, the other gives 12 × 1 = 12, and the determinant is 5 − 12 = −7. It is not 0, so there is one answer: a = 130 and c = 100.">

A fraction with 0 on the bottom has no answer. So when the determinant
is 0, the formulas cannot give a single answer, and the next section
shows what that means. Here is the promise for your toolkit. It
returns `None`, Python's "nothing here", when there is no single answer.

```python exec
id: several-unknowns-toolkit
toolkit: yes
def solve_simultaneous(a1, b1, c1, a2, b2, c2):
    """Return the pair (x, y) where a1x + b1y = c1 and a2x + b2y = c2.

    Return None when there is no single answer: the determinant
    a1*b2 - a2*b1 is 0.
    """
    ...
```

```python toolkit-reference
for: several-unknowns-toolkit
def solve_simultaneous(a1, b1, c1, a2, b2, c2):
    """Return the pair (x, y) where a1x + b1y = c1 and a2x + b2y = c2.

    Return None when there is no single answer: the determinant
    a1*b2 - a2*b1 is 0.
    """
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None
    x = (c1 * b2 - c2 * b1) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    return (x, y)
```

```hint
after: 10 errors
title: some steps
1. Work out the determinant, `a1 * b2 - a2 * b1`, and give it a name.
2. If it is 0, return `None` straight away.
3. Otherwise work out `x` and `y` from the two formulas above, each
   divided by the determinant, and return the pair `(x, y)`.

**Think about:** why must the check for 0 come before the two
divisions, and not after?
```

How does your `solve_simultaneous` compare with a solution? The table
below runs the same calls on your function and on one way to write it,
side by side. The first row is the server log. The last row builds two
equations from an answer we choose, $(1.5, 4)$, and asks the tool to
find that answer again. Where a row is different, try that call on its
own.

```inputs
for: several-unknowns-toolkit
solve_simultaneous(1, 1, 230, 12, 5, 2060)                  # the server log
solve_simultaneous(1, 1, 10, 2, -1, 5)
solve_simultaneous(2, 4, 10, 1, 2, 5)                       # the determinant is 0
solve_simultaneous(3, -2, 3 * 1.5 - 2 * 4, 1, 5, 1.5 + 5 * 4)   # built from the answer (1.5, 4)
```

```solution
for: several-unknowns-toolkit
def solve_simultaneous(a1, b1, c1, a2, b2, c2):
    """Return the pair (x, y) where a1x + b1y = c1 and a2x + b2y = c2.

    Return None when there is no single answer: the determinant
    a1*b2 - a2*b1 is 0.
    """
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None
    x = (c1 * b2 - c2 * b1) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    return (x, y)
```

In the server log's row, the determinant is $1 \times 5 - 12 \times 1 = -7$,
the same 7 that elimination divided by, with its sign turned round.

<aside class="dl-note" id="several-unknowns-note-cramer">

**Cramer.** Gabriel Cramer, a Swiss mathematician, published the rule
in 1750, in a book about curves. He wanted to find the curve through a
set of points. The practice page asks the same question of a letter.

</aside>

## When there is no single answer

If you have not written `solve_simultaneous` yet, open the solution
under the table and copy it into the stub.

Two people read a backup log to find the size of one photo and one
song. The first reads that 3 photos and 2 songs made 80 MB. The second
reads that 6 photos and 4 songs made 150 MB. What does
`solve_simultaneous` make of that?

```python exec
id: several-unknowns-none-1
print(solve_simultaneous(3, 2, 80, 6, 4, 150))
print(3 * 4 - 6 * 2)
```

It returns `None`, because the determinant is 0. Let's draw the two
facts as rules that give a song's size from a photo's size. What will
the lines do?

```python exec
id: several-unknowns-none-2
def song_from_first_reading(photo):
    return (80 - 3 * photo) / 2

def song_from_second_reading(photo):
    return (150 - 6 * photo) / 4

plot_rule(song_from_first_reading, 0, 25)
plot_rule(song_from_second_reading, 0, 25)
plt.xlabel("MB in one photo")
plt.ylabel("MB in one song")
plt.legend()
```

The lines are *parallel*. They have the same steepness, and never meet.
No pair of sizes fits both facts. Six photos and four songs are twice
three and two, so they should make twice 80 MB, which is 160 MB. One of
the two readings is wrong, or the files were not all the same size.

If the second reading had said 160 MB, the two equations would be one
fact said twice, and the two lines would be the same line. Every point
on it fits, so there are endless answers and still no single one. The
determinant is 0 in both cases, and `None` covers both.

So two straight lines on a flat plane can meet in three ways: once,
never, or everywhere. The determinant tells us which kind we have
before we draw anything.

<img src="once-never-everywhere.svg" alt="Three small graphs side by side. Once: the two lines for the image and text requests cross at one point, (130, 100), and the determinant is −7. Never: the two readings of the backup log, 3 photos and 2 songs making 80 MB and 6 photos and 4 songs making 150 MB, give two parallel lines that never meet, and the determinant is 0. Everywhere: with 160 MB in place of 150 MB, the second line lies exactly on top of the first, the same line drawn twice, and the determinant is 0 again.">

```question
id: several-unknowns-none-3
type: multiple-choice
answer: 3

Which pair of equations has no single solution?

- $x + y = 4$ and $x - y = 2$
  - Adding the two gives 2x = 6, so x = 3 and y = 1.
- $2x + y = 7$ and $x + 2y = 8$
  - These two lines cross once, at x = 2 and y = 3.
- $x + 3y = 5$ and $2x + 6y = 9$
  - Doubling the first gives 2x + 6y = 10, and the second says 2x + 6y = 9: both cannot hold.
```

## Three unknowns

The backup log has three more lines. Each line is one upload, and gives
only its total size, not the size of a photo, a song or a short video
clip. (The sizes are invented, but real files are about this size.)

- 2 photos, 1 song and 1 clip made 12.5 MB;
- 1 photo, 2 songs and 1 clip made 11.5 MB;
- 1 photo, 1 song and 2 clips made 12.0 MB.

Three unknowns need three facts. Elimination works the same way, one
unknown at a time. Call the sizes $p$, $s$ and $v$. Take the second
upload from the first, and the clip cancels, leaving $p - s = 1$. Take
the third from twice the second, and it cancels again, leaving
$p + 3s = 11$. Now
there are two equations in two unknowns, and your toolkit can finish
the job. (This cell needs your `solve_simultaneous`.) What do you
expect?

```python exec
id: several-unknowns-three-1
photo, song = solve_simultaneous(1, -1, 12.5 - 11.5, 1, 3, 2 * 11.5 - 12.0)
clip = 12.5 - 2 * photo - song
print(photo, song, clip)

print(2 * photo + song + clip, photo + 2 * song + clip, photo + song + 2 * clip)
```

A photo is 3.5 MB, a song 2.5 MB and a clip 3.0 MB, and all three
uploads pass the check. The big job was made of smaller promises: two
eliminations, one call to `solve_simultaneous`, and one substitution.

Three facts for three unknowns can also find a curve from a picture.
The practice page finds the letter's bowl from
[The top of the curve](tutorial:the-top-of-the-curve#a-letter-that-sits-below-the-line)
from three of its pixels.

For more unknowns, the same idea is written with grids of numbers
called matrices, and numpy has a tool for it, `np.linalg.solve`. It
takes the numbers in front of the unknowns, one row for each equation,
and the totals.

```python exec
id: several-unknowns-three-2
import numpy as np

uploads = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
totals = [12.5, 11.5, 12.0]
print(np.linalg.solve(uploads, totals))
```

It finds the same three sizes. The Computational Methods course works with
these grids in depth, starting at
[Matrices: adding, scaling and transposing a grid of numbers](tutorial:grid-of-numbers).

<details class="dl-why"><summary>Why this way?</summary>

This page put Cramer's rule in the toolkit: one formula for the answer
to two equations. Most programs that solve equations do not use it.
They do elimination step by step on a grid of numbers, as
`np.linalg.solve` does.

Step-by-step elimination is the better method for many unknowns. It
works the same way for 3 or 300, and Cramer's rule becomes very slow as
the number of unknowns grows.

We used the formula because, for two unknowns, it shows the whole
method at once, and its bottom line, the determinant, says in one
number whether there is a single answer. The cost is that it only
works for two unknowns. For three, we had to eliminate by hand first.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | $a$ and $c$ for counts the log did not keep; $a_1$, $b_1$, $c_1$ for the numbers of the first equation; the determinant |
| What is promised? | the solution makes every equation true at once; `solve_simultaneous` promises that pair, or `None` |
| What happens when? | elimination first finds one unknown, and only then the other; three unknowns become two, and then one |
| What does this space let us do? | two straight lines on a flat plane cross once, never, or everywhere; a determinant of 0 means never or everywhere |

## What we have now

| Term or tool | What it means |
|---|---|
| simultaneous equations | equations that must all be true at once, for the same unknowns |
| solution | the values that make every equation true |
| elimination | combining equations so that one unknown cancels out |
| Cramer's rule | a formula for $x$ and $y$ from the six numbers of two equations |
| determinant | $a_1 b_2 - a_2 b_1$; when it is 0 there is no single answer |
| parallel lines | lines with the same steepness, which never meet |
| `solve_simultaneous(a1, b1, c1, a2, b2, c2)` | your toolkit tool: the pair $(x, y)$, or `None` |
| `np.linalg.solve(rows, totals)` | numpy's solver, for any number of unknowns |

For another route through the same ideas, the integrated course has
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations#simultaneous-equations).

## Where to read more

3Blue1Brown (2019). *Cramer's rule, explained geometrically: Chapter 12,
Essence of linear algebra.* <https://www.youtube.com/watch?v=jBsC34PxzoM>.
The formula this page finds for every pair of equations has a name,
Cramer's rule. Grant Sanderson shows why it works, with areas. About
twelve minutes.
