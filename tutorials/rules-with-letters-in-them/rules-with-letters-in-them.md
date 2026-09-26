---
title: "Rules with letters in them: expressions, equations and identities"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-rule-a-question-and-a-promise:
    covers: [MIT-1.5]
    touches: [PDP-LO4]
  putting-a-number-in-for-the-letter:
    covers: [MIT-1.6]
    touches: [MIT-6.4]
  collecting-like-terms:
    covers: [MIT-1.6]
  expanding-brackets-is-a-loop:
    covers: [MIT-1.8, MIT-1.6]
---

# Rules with letters in them: expressions, equations and identities

Open a photo gallery on a website. The page has a header 30 pixels
tall, and under it rows of photos, each row 50 pixels tall. Your
browser window is 280 pixels tall. How many rows fit?

The sentence about the page is a rule. It works for any number of
rows. "How many rows fit?" is a question. It has one answer. Algebra writes both with the
same letters and the same equals sign. So how can you tell a rule from
a question?

On this page we:

- tell three kinds of sentence with letters in them apart: an
  expression, an equation and an identity
- put a number in for a letter, and add `evaluate` to the toolkit
- keep an expression like $3x^2 + 5x - 2$ as a list of numbers
- simplify an expression by collecting the parts that belong together
- multiply out brackets with a loop, and find the three weights that
  draw a curve on a screen

> **The space we're in.** We work with the real numbers, and one letter
> at a time, usually $x$. A letter stands for a number, so any move we may make with
> a number, we may make with the letter. Python has no letters of this
> kind. A Python name must have a value before we use it. So we check
> our algebra by giving the letter one value after another. We usually
> do not say it, but maths writes $3x$ for "3 times $x$", and Python
> needs `3 * x`.

## Warm-up

The first question is from
[Machines that take a number](tutorial:machines-that-take-a-number#a-machine-with-one-slot),
and the second from
[A row of numbers](tutorial:a-row-of-numbers#counting-from-0).

```question
id: rules-with-warm-up-1
type: fill-in-the-blank

The temperature chip's rule is $f(x) = 100x - 50$. So $f(0.75)$ is {25}.
```

```question
id: rules-with-warm-up-2
type: fill-in-the-blank

`numbers = [7, 0, 2]`. Then `numbers[2]` is {2}, and `len(numbers)` is
{3}.
```

## A rule, a question and a promise

Let's write the gallery's rule with a letter. If $n$ is the number of
rows, the page's height in pixels is

$$50n + 30$$

On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#which-comes-first),
an expression was a piece of code that Python turns into one value.
In maths, an expression can have letters in it too. It is a rule made
of numbers, letters and operations, such as $50n + 30$ or $x^2 - 4$. It
has a value once each letter has a value. Here $n$ is a name for any
number we choose to put in, like the parameter of a function.

Now the question. "How many rows make exactly 280 pixels?" is written

$$50n + 30 = 280$$

An *equation* is a sentence that says two expressions are equal. It can
be true for some values of the letter and false for others. Here $n$ is
a name for a number we do not know yet. To *solve* an equation is to
find the values that make it true.

There is a third kind of sentence. Put two gallery pages one under the
other, each with its own header. Is doubling the whole rule the same as
doubling each part?

$$2(50n + 30) = 100n + 60$$

An *identity* is an equation that is true for every value of its
letters. Here $n$ is a name for every number at once. An identity is a
promise: whatever number you put in, the two sides agree.

The cell tries 1 to 8 rows, and asks the equation and the identity
of each. Pause here and guess which rows will say `True` in each
column. Then run it.

```python exec
id: rules-with-kinds-1
def page_height(rows):
    """Return the gallery page's height in pixels: a 30 px header and rows 50 px tall."""
    return 50 * rows + 30

for rows in range(1, 9):
    print(rows, page_height(rows),
          page_height(rows) == 280,
          2 * page_height(rows) == 100 * rows + 60)
```

The equation is true in one row only. Exactly 5 rows fit. The identity
is true in every row. Eight values do not prove it for every number,
but a single `False` would have been enough to show it is not an
identity.

In Python, `=` gives a name a value, and `==` asks whether two values
are equal. Maths uses one sign, $=$, for both jobs, and the reader has
to tell which is meant. I think Python helps us by keeping them
apart.

<aside class="dl-note" id="rules-with-note-equals">

**Two lines of the same length.** The sign $=$ was first printed in
1557, by the Welsh doctor Robert Recorde. He chose two lines of the
same length because, he wrote, no two things can be more equal.

</aside>

```question
id: rules-with-kinds-2
type: fill-in-the-blank

$3(x + 4) = 3x + 12$ is {an identity|an equation with one answer|an expression}.
$3x + 12 = 27$ is {an equation with one answer|an identity|an expression}.
$3x + 12$ on its own is {an expression|an identity|an equation with one answer}.
```

## Putting a number in for the letter

To *evaluate* an expression is to find its value for one value of
its letter. Putting the number in place of the letter is called
*substitution*.

The order of operations from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#which-comes-first)
still holds. In $3x^2$, the power comes first, then the multiply. What
will each line print when $x$ is $-2$?

```python exec
id: rules-with-evaluate-1
x = -2
print(3 * x ** 2 + 5 * x - 2)
print((3 * x) ** 2 + 5 * x - 2)
```

The first line is $3 \times 4 - 10 - 2 = 0$. The second squares $-6$,
and gives 24. The brackets moved the power to a new place in the
sequence of steps.

### Terms, coefficients and a list

The expression $3x^2 + 5x - 2$ is made of three parts added together. A
*term* is a number times a power of the letter, such as $3x^2$ or $5x$.
The number in front is the term's *coefficient*. The $-2$ has no letter.
It is the *constant term*, and we can think of it as $-2x^0$, because
$x^0 = 1$, as on
[Doubling and halving](tutorial:doubling-and-halving#grains-on-a-chessboard).

A *polynomial* is an expression made by adding terms like these, where
every power is a whole number, 0 or more. Its *degree* is its highest
power. A polynomial of degree 1, like $50n + 30$, is *linear*. Degree 2
is quadratic, and degree 3 is *cubic*.

A polynomial is its list of coefficients. We write the list lowest power
first, so that each coefficient's index is its power:

| Polynomial | List | Why |
|---|---|---|
| $3x^2 + 5x - 2$ | `[-2, 5, 3]` | $-2x^0$, $5x^1$, $3x^2$ |
| $50n + 30$ | `[30, 50]` | the constant first, then the $n$ term |
| $x^3 - 4x$ | `[0, -4, 0, 1]` | no constant and no $x^2$: each still needs its place, as 0 |

```question
id: rules-with-evaluate-2
type: multiple-choice
answer: 3

Which list is $2x^2 - 7$?

- `[2, -7]`
  - This leaves out the 0 for x, and puts the highest power first.
- `[2, 0, -7]`
  - Every power is there, but highest first; the list starts from the number on its own.
- `[-7, 0, 2]`
  - Lowest power first: −7 on its own, 0 lots of x, 2 lots of x².
- `[-7, 2]`
  - Lowest power first, but with no 0 for x the 2 sits in the x place, and means 2x.
```

### Your turn: a tool that evaluates

Here is the rule for evaluating, in words: multiply each coefficient by
$x$ to the power of its index, and add up the results. In symbols, with
$c_i$ for the coefficient at index $i$, it is the sigma from
[Doing it again](tutorial:doing-it-again#sigma-a-loop-written-by-mathematicians):

$$c_0 + c_1 x + c_2 x^2 + \dots + c_n x^n = \sum_{i=0}^{n} c_i x^i$$

Replace the `...` with a loop:

1. Start a running total at 0.
2. For each `power` in `range(len(coefficients))`, add
   `coefficients[power] * x ** power` to it.
3. After the loop, return the running total.

If the loop feels like hard work, open the hints under the cell, or
the answer under the tests, and come back to your own version later.

```python exec
id: rules-with-toolkit
toolkit: yes
def evaluate(coefficients, x):
    """Return the value of a polynomial when its letter is x.

    coefficients lists the number in front of each power, lowest power
    first: [-2, 5, 3] is 3x^2 + 5x - 2.
    """
    ...
```

```python toolkit-reference
for: rules-with-toolkit
def evaluate(coefficients, x):
    """Return the value of a polynomial when its letter is x.

    coefficients lists the number in front of each power, lowest power
    first: [-2, 5, 3] is 3x^2 + 5x - 2.
    """
    value = 0
    for power in range(len(coefficients)):
        value = value + coefficients[power] * x ** power
    return value
```

```hint
Try `print(evaluate([30, 50], 5))` on its own. Five rows of the gallery
make 280 pixels. What came back instead?
```

```hint
after: 10 errors
title: some steps
1. The first line under the docstring is `value = 0`.
2. The loop line is `for power in range(len(coefficients)):`.
3. Inside the loop, add `coefficients[power] * x ** power` to `value`.
4. The last line, back at the level of the loop, is `return value`.

**Think about:** why the list is written lowest power first. What would
the loop need to do if it were written highest power first?
```

The tests compare `evaluate` with Python's own arithmetic, for every
whole number from $-10$ to 10. Until `evaluate` is written, this cell
stops with an error, and so do the later cells on this page that use
it.

```python exec
id: rules-with-toolkit-tests
assert evaluate([30, 50], 5) == 280, "the gallery with 5 rows"
assert evaluate([-2, 5, 3], -2) == 0
assert evaluate([7], 100) == 7, "a constant has the same value for every x"
for x in range(-10, 11):
    assert evaluate([-2, 5, 3], x) == 3 * x ** 2 + 5 * x - 2
    assert evaluate([0, -4, 0, 1], x) == x ** 3 - 4 * x
assert close_enough(evaluate([-2, 5, 3], 0.1), 3 * 0.1 ** 2 + 5 * 0.1 - 2)
print("evaluate keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may use other names and still do the same job.

```python
def evaluate(coefficients, x):
    """Return the value of a polynomial when its letter is x.

    coefficients lists the number in front of each power, lowest power
    first: [-2, 5, 3] is 3x^2 + 5x - 2.
    """
    value = 0
    for power in range(len(coefficients)):
        value = value + coefficients[power] * x ** power
    return value
```

</details>

The last test uses `close_enough` from
[Does it work?](tutorial:does-it-work#close-enough). 0.1 is a float,
and two routes to a float can differ in the last digit.

## Collecting like terms

If you have not written `evaluate` yet, open the answer under the tests
and copy it into the stub.

A longer gallery page has two sections. The top one has 4 rows of
photos, each $x$ pixels tall, and a 30-pixel header. The bottom one has
3 rows and a 50-pixel footer. The page's height is

$$4x + 30 + 3x + 50$$

That is four terms, and it can be shorter. *Like terms* are terms with
the same power of the letter: $4x$ and $3x$ make $7x$, and the two
constants are like terms too. To *simplify* an expression is to write it with fewer parts
and the same value. *Collecting like terms*, adding their coefficients,
is one way:

$$4x + 30 + 3x + 50 = 7x + 80$$

$x^2$ and $x$ are not like terms, so $x^2 + x$ stays as it is.

In a list, like terms are already in the same place. The $x$ terms are
all at index 1. So collecting like terms is adding two lists place by
place, as on
[A row of numbers](tutorial:a-row-of-numbers#adding-and-multiplying-lists).
The lists may have different lengths, so the new list is as long as the
longer one. Before you run it, what list do you expect for the page?

```python exec
id: rules-with-collect-1
def add_polynomials(first, second):
    """Return the coefficients of first + second, with like terms collected."""
    collected = [0] * max(len(first), len(second))
    for power in range(len(first)):
        collected[power] = collected[power] + first[power]
    for power in range(len(second)):
        collected[power] = collected[power] + second[power]
    return collected

top_section = [30, 4]
bottom_section = [50, 3]
whole_page = add_polynomials(top_section, bottom_section)
print(whole_page)

for row_height in [50, 100, 120]:
    print(row_height, evaluate(whole_page, row_height),
          evaluate(top_section, row_height) + evaluate(bottom_section, row_height))
```

The list is `[80, 7]`, which is $7x + 80$. The last three lines check it
by substitution: for each row height, the short and the long expression
agree. Which rows make the page exactly 780 pixels tall? That is an
equation, $7x + 80 = 780$, and
[Solving for x](tutorial:solving-for-x) solves equations like it.

### Your turn

1. By hand, simplify $(4x^2 + 3x - 1) + (2x^2 - 3x + 6)$.
2. Check your answer with `add_polynomials([-1, 3, 4], [6, -3, 2])`.
   What happened to the $x$ term, and why does the list still have a
   place for it?
3. Check by substitution, for three values of $x$.

```python exec
id: rules-with-collect-your-turn
# Your checks here
```

## Expanding brackets is a loop

A square photo is $x$ pixels on each side. An app adds a strip 3 pixels
wide down its right side, and a caption bar 5 pixels tall along the
bottom. The new rectangle is $x + 3$ wide and $x + 5$ tall, so it
covers $(x + 3)(x + 5)$ pixels.

Picture the rectangle cut into four pieces: the photo, the strip, the
bar, and a small corner, 3 by 5. Each piece is one term of the first
bracket times one term of the second:

| times | $x$ | $5$ |
|---|---|---|
| $x$ | $x^2$ | $5x$ |
| $3$ | $3x$ | $15$ |

<img src="photo-with-bars.svg" alt="A rectangle x + 3 wide and x + 5 tall, cut into four pieces. At the top left is the photo, a square x by x, marked x². To its right is the strip, 3 wide and x tall, marked 3x. Below the photo is the bar, x wide and 5 tall, marked 5x. At the bottom right is the corner, 3 by 5, marked 15. Beside the rectangle: (x + 3)(x + 5) = x² + 3x + 5x + 15 = x² + 8x + 15.">

Adding the four pieces, and collecting the like terms $5x$ and $3x$,
gives the area:

$$(x + 3)(x + 5) = x^2 + 8x + 15$$

To *expand* brackets is to multiply every term in one bracket by every
term in the other, and then collect like terms.

Here is how that becomes code. A term at index $i$ times a term at index
$j$ gives a term at index $i + j$, because $x^i \times x^j = x^{i+j}$.
That is the law of powers from
[Doubling and halving](tutorial:doubling-and-halving#doublings-add-up).
So expanding is a loop inside a loop: every $i$ with every $j$. Predict
the list for $(x + 3)(x + 5)$ before you run the cell.

```python exec
id: rules-with-expand-1
def expand_brackets(first, second):
    """Return the coefficients of first times second, with the brackets multiplied out."""
    expanded = [0] * (len(first) + len(second) - 1)
    for i in range(len(first)):
        for j in range(len(second)):
            expanded[i + j] = expanded[i + j] + first[i] * second[j]
    return expanded

photo_with_bars = expand_brackets([3, 1], [5, 1])
print(photo_with_bars)
```

It prints `[15, 8, 1]`, which is $x^2 + 8x + 15$. Is the expansion an
identity? Let's substitute, and compare with Python multiplying the two
brackets itself:

```python exec
id: rules-with-expand-2
for side in range(-20, 21):
    assert evaluate(photo_with_bars, side) == (side + 3) * (side + 5)
print("The two sides agree for every whole number from -20 to 20.")
```

Two different quadratics can
agree at two values of $x$ at most. So if two quadratics agree at three
or more values, they are the same quadratic, and the 41 values we tried
are a proof. I find that surprising. Three checks cover every number
there is.

The loop can multiply three brackets too: expand two, then multiply
the answer by the third. How long will the list for
$(x + 1)(x + 2)(x + 3)$ be?

```python exec
id: rules-with-expand-3
cubic = expand_brackets(expand_brackets([1, 1], [2, 1]), [3, 1])
print(cubic)

for x in range(-10, 11):
    assert evaluate(cubic, x) == (x + 1) * (x + 2) * (x + 3)
print("Every value from -10 to 10 agrees.")
```

It is `[6, 11, 6, 1]`: the cubic $x^3 + 6x^2 + 11x + 6$. Three linear
brackets make a cubic, and two make a quadratic.

### Three weights for a curve

Fonts and drawing programs draw a smooth curve by mixing three
points: a start, an end, and a point in between that pulls the curve.
A number $t$ runs from 0 at the start to 1 at the end, and the three
points get three *weights*: $(1 - t)^2$, $2t(1 - t)$ and $t^2$. Each
weight is brackets multiplied together, so the loop can expand it.
What will each weight be at $t = 0$?

```python exec
id: rules-with-expand-weights-1
start_weight = expand_brackets([1, -1], [1, -1])      # (1 - t)(1 - t)
middle_weight = expand_brackets([0, 2], [1, -1])      # 2t times (1 - t)
end_weight = expand_brackets([0, 1], [0, 1])          # t times t
print(start_weight, middle_weight, end_weight)

for t in [0, 0.25, 0.5, 1]:
    print(t, evaluate(start_weight, t), evaluate(middle_weight, t), evaluate(end_weight, t))
```

At $t = 0$ all the weight is on the start, and at $t = 1$ all of it is
on the end. Halfway, the middle point gets half. Before you run the
next cell, what do the three weights add up to, as a polynomial?

```python exec
id: rules-with-expand-weights-2
all_three = add_polynomials(add_polynomials(start_weight, middle_weight), end_weight)
print(all_three)
```

It prints `[1, 0, 0]`, the number 1, with no $t$ at all. Three weights that rise
and fall add up to a flat 1, for every $t$. The mix works because of
that identity. The weights always share out one whole. On
[The top of the curve](tutorial:the-top-of-the-curve#a-letter-that-sits-below-the-line),
these three weights draw the bottom of a letter o.

<aside class="dl-note" id="rules-with-note-bernstein">

**Weights with a name.** These weights are called Bernstein
polynomials, after Sergei Bernstein, who used them in 1912 to show that
polynomials can come as close as you like to any unbroken curve.

</aside>

### A move that works once

Many people, in a hurry, write $(x + 3)^2 = x^2 + 9$. Is that an
identity? Let's substitute before we decide. Which rows do you expect to
say `True`?

```python exec
id: rules-with-expand-4
for x in range(-3, 4):
    print(x, (x + 3) ** 2, x ** 2 + 9, (x + 3) ** 2 == x ** 2 + 9)

print(expand_brackets([3, 1], [3, 1]))
```

It is true for $x = 0$ only. It is an equation with one answer, not an
identity. The expansion, `[9, 6, 1]`, shows what went missing:
$(x + 3)^2 = x^2 + 6x + 9$. For any number $a$, the same grid gives
$(x + a)^2 = x^2 + 2ax + a^2$. In the photo picture, $x^2 + 9$ keeps the
photo and the small corner, and forgets the strip and the bar, each
$3x$. The move works in the one case where they have no length: when
$x$ is 0.

<img src="the-square-forgotten.svg" alt="A square x + 3 on each side, cut into four pieces: the photo, x², at the top left; the strip, 3x, to its right; the bar, 3x, below the photo; and the corner, 9, at the bottom right. The strip and the bar are shaded and marked left out. Beside the square: (x + 3)² = x² + 3x + 3x + 9 = x² + 6x + 9, and x² + 9 keeps the photo and the corner, and leaves out the two 3x pieces.">

### Your turn

1. By hand, with a grid of four pieces, expand $(2x - 1)(x + 4)$.
2. Check it with `expand_brackets([-1, 2], [4, 1])`, and then by
   substitution for a few values of $x$.
3. Expand $(x - 2)(x + 2)$. What happened to the $x$ term? Look at the
   grid of four pieces to see why.

```python exec
id: rules-with-expand-your-turn
# Your expansions and checks here
```

<details class="dl-why"><summary>Why this way?</summary>

This page checked every piece of algebra by putting numbers in. A
second way is to prove each step from rules, such as "multiply each
term inside the bracket", and never try a number.

Proof by rules is what algebra is for, in the end. It covers every
number at once, and a list of checks never can, except in special cases
like the quadratics above.

We checked with numbers because a check is something you can run and
trust before you trust the rules, and it shows at once where two sides
differ. The cost is that a passing check shows a rule works only for the
numbers you tried.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a letter: any number, an unknown number, or every number at once; a polynomial, by its list of coefficients |
| What is promised? | an identity promises that its two sides agree for every value; `evaluate` promises the value of a polynomial at $x$; the three weights promise to add up to 1 |
| What happens when? | powers before multiplying; expand first, then collect like terms; in `expand_brackets`, every $i$ meets every $j$ |
| What does this space let us do? | any move we make with a number, we may make with a letter; Python needs a value for each name, so we check by substituting |

## What we have now

| Term or tool | What it means |
|---|---|
| expression | a rule of numbers, letters and operations; it has a value once each letter has one |
| equation, solving | two expressions said to be equal; solving finds the values that make it true |
| identity | an equation true for every value of its letters |
| evaluate, substitution | find an expression's value by putting a number in for its letter |
| term, coefficient, constant term | a number times a power of the letter; the number in front; the term with no letter |
| polynomial, degree | a sum of terms with whole-number powers; its highest power (1 linear, 2 quadratic, 3 cubic) |
| a polynomial as a list | coefficients lowest power first: `[-2, 5, 3]` is $3x^2 + 5x - 2$ |
| `evaluate(coefficients, x)` | your toolkit function: a polynomial's value at $x$ |
| like terms, collecting, simplifying | terms with the same power; add their coefficients; fewer parts, same value |
| expanding brackets | every term of one bracket times every term of the other, then collect |
| $(x + a)^2 = x^2 + 2ax + a^2$ | a squared bracket: two strips of $ax$ as well as the two squares |
| weights for a curve | $(1 - t)^2$, $2t(1 - t)$ and $t^2$, which add up to 1 for every $t$ |

For more, the page
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive),
from another course, builds tools that print, add, subtract and scale
polynomials kept as lists.

The practice page is next. On the next page,
[Drawing a rule](tutorial:drawing-a-rule), we draw $(x - 2)(x + 2)$ as a
picture.

## Where to read more

Ben Syversen (2026). *Why Did It Take 1,877 Years to Invent x²?*
<https://www.youtube.com/watch?v=uIQzkLTI2MU>. People wrote rules with
letters in them long before they had a short way to write powers. Ben
Syversen tells how the notation we use today came to be. About
twenty-seven minutes.
