---
title: "Rules with letters in them: expressions, equations and identities"
year: "2026-2027"
version: 2026.09.24.1
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

A pancake recipe says: use 50 g of flour for each person, and 30 g
more, because the first pancake always goes wrong. You have 280 g of
flour. How many people can you feed?

The first sentence is a rule: it works for any number of people. The
second is a question: it has one answer. Algebra writes both with the
same letters. So what is the difference between a rule and a question?

On this page we:

- tell three kinds of sentence with letters in them apart: an
  expression, an equation and an identity
- put a number in for a letter, and add `evaluate` to the toolkit
- keep an expression like $3x^2 + 5x - 2$ as a list of numbers
- simplify an expression by collecting the parts that belong together
- multiply out brackets with a loop, into quadratics and cubics, and
  check every answer by putting numbers back in

> **The space we're in.** The real numbers, and one letter at a time,
> usually $x$. A letter stands for a number, so any move we may make with
> a number, we may make with the letter. Python has no letters of this
> kind: a Python name must have a value before we use it. So we check
> our algebra by giving the letter one value after another. One thing
> usually goes unsaid: maths writes $3x$ for "3 times $x$", and Python
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

Let's write the recipe's rule with a letter. If $p$ is the number of
people, the flour in grams is

$$50p + 30$$

On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#which-comes-first),
an expression was a piece of code that Python works out to one value.
In maths, an expression can have letters in it too: it is a rule made
of numbers, letters and operations, such as $50p + 30$ or $x^2 - 4$. It
has a value once each letter has a value. Here $p$ is a name for any
number we choose to put in, like the parameter of a function.

Now the question. "Which $p$ needs exactly 280 g?" is written

$$50p + 30 = 280$$

An *equation* is a sentence that says two expressions are equal. It can
be true for some values of the letter and false for others. Here $p$ is
a name for a number we do not know yet. To *solve* an equation is to
find the values that make it true.

There is a third kind of sentence. Say you double the recipe for two
tables. Is doubling the whole rule the same as doubling each part?

$$2(50p + 30) = 100p + 60$$

An *identity* is an equation that is true for every value of its
letters. Here $p$ is a name for every number at once. An identity is a
promise: whatever number you put in, the two sides agree.

The cell tries 1 to 8 people. For each row, it prints the flour, then
asks the equation, then asks the identity. Which rows do you expect to
say `True` in each column? Run it to check.

```python exec
id: rules-with-kinds-1
def flour_needed(people):
    """Return the grams of flour the pancake recipe needs for this many people."""
    return 50 * people + 30

for people in range(1, 9):
    print(people, flour_needed(people),
          flour_needed(people) == 280,
          2 * flour_needed(people) == 100 * people + 60)
```

The equation is true in one row only: 5 people. The identity is true in
every row. Checking 8 values does not prove the identity for every
number, but it tells us a lot. A single `False` would have been enough
to show that it is not an identity.

Look at the two kinds of equals sign in the cell. In Python, `=` gives a
name a value, and `==` asks whether two values are equal. Maths uses one
sign, $=$, for both jobs, and the reader has to tell which one is meant.

```question
id: rules-with-kinds-2
type: fill-in-the-blank

$3(x + 4) = 3x + 12$ is {an identity|an equation with one answer|an expression}.
$3x + 12 = 27$ is {an equation with one answer|an identity|an expression}.
$3x + 12$ on its own is {an expression|an identity|an equation with one answer}.
```

## Putting a number in for the letter

To *evaluate* an expression is to work out its value for one value of
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
and gives 24. The brackets moved the power to a different place in the
sequence of steps, and the answer changed.

### Terms, coefficients and a list

The expression $3x^2 + 5x - 2$ is made of three parts added together. A
*term* is a number times a power of the letter, such as $3x^2$ or $5x$.
The number in front is the term's *coefficient*. The $-2$ has no letter.
It is the *constant term*, and we can think of it as $-2x^0$, because
$x^0 = 1$, as on
[Doubling and halving](tutorial:doubling-and-halving#grains-on-a-chessboard).

A *polynomial* is an expression made by adding terms like these, where
every power is a whole number, 0 or more. Its *degree* is its highest
power. A polynomial of degree 1, like $50p + 30$, is *linear*. Degree 2
is quadratic, the word
[Racing the sorts](tutorial:racing-the-sorts) used for growth like
$n^2$. Degree 3 is *cubic*.

A polynomial is its list of coefficients. We write the list lowest power
first, so that each coefficient's index is its power:

| Polynomial | List | Why |
|---|---|---|
| $3x^2 + 5x - 2$ | `[-2, 5, 3]` | $-2x^0$, $5x^1$, $3x^2$ |
| $50p + 30$ | `[30, 50]` | the constant first, then the $p$ term |
| $x^3 - 4x$ | `[0, -4, 0, 1]` | no constant and no $x^2$: each still needs its place, as 0 |

```question
id: rules-with-evaluate-2
type: multiple-choice
correct: 3

Which list is $2x^2 - 7$?

- `[2, -7]`
- `[2, 0, -7]`
- `[-7, 0, 2]`
- `[-7, 2]`
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
3. After the loop, give back the running total.

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
Try `print(evaluate([30, 50], 5))` on its own. The recipe for 5 people
needs 280 g. What came back instead?
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
assert evaluate([30, 50], 5) == 280, "flour for 5 people"
assert evaluate([-2, 5, 3], -2) == 0
assert evaluate([7], 100) == 7, "a constant has the same value for every x"
for x in range(-10, 11):
    assert evaluate([-2, 5, 3], x) == 3 * x ** 2 + 5 * x - 2
    assert evaluate([0, -4, 0, 1], x) == x ** 3 - 4 * x
assert close_enough(evaluate([-2, 5, 3], 0.1), 3 * 0.1 ** 2 + 5 * 0.1 - 2)
print("evaluate keeps its promise.")
```

The last test uses `close_enough` from
[Does it work?](tutorial:does-it-work#close-enough), because 0.1 is a
float, and two routes to the same float answer can differ in the last
digit.

## Collecting like terms

A band plays two nights and is paid $x$ euro for each ticket. On Friday
it sells 120 tickets and pays €300 for the hall. On Saturday it sells 80
tickets and pays €200. Its takings for the weekend are

$$120x - 300 + 80x - 200$$

That is four terms, and it can be shorter. *Like terms* are terms with
the same power of the letter. $120x$ and $80x$ are like terms: 120 lots
of $x$ and 80 more lots of $x$ make 200 lots. The two constants are like
terms too. To *simplify* an expression is to write it with fewer parts
and the same value. *Collecting like terms*, adding their coefficients,
is one way:

$$120x - 300 + 80x - 200 = 200x - 500$$

$x^2$ and $x$ are not like terms, so $x^2 + x$ stays as it is.

In a list, like terms are already in the same place: the $x$ terms are
all at index 1. So collecting like terms is adding two lists place by
place, as on
[A row of numbers](tutorial:a-row-of-numbers#adding-and-multiplying-lists).
The lists may have different lengths, so the new list is as long as the
longer one. Before you run it, what list do you expect for the weekend?

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

friday = [-300, 120]
saturday = [-200, 80]
weekend = add_polynomials(friday, saturday)
print(weekend)

for ticket_price in [5, 10, 12.5]:
    print(ticket_price, evaluate(weekend, ticket_price),
          evaluate(friday, ticket_price) + evaluate(saturday, ticket_price))
```

The list is `[-500, 200]`, which is $200x - 500$. The last three lines
check it by substitution. At each ticket price, the short expression and
the long one give the same takings. When is the weekend's total exactly
zero? That is an equation, $200x - 500 = 0$, and
[Solving for x](tutorial:solving-for-x) is where we solve equations like
it.

### Your turn

1. By hand, simplify $(4x^2 + 3x - 1) + (2x^2 - 3x + 6)$.
2. Check your answer with `add_polynomials([-1, 3, 4], [6, -3, 2])`.
   What happened to the $x$ term, and why does the list still have a
   place for it?
3. Check again by substitution: compare `evaluate` on your answer with
   the two original expressions added, for three values of $x$.

```python exec
id: rules-with-collect-your-turn
# Your checks here
```

## Expanding brackets is a loop

A square patio is $x$ metres on each side. The owner makes it 3 m longer
one way and 5 m longer the other way. The new area is $(x + 3)(x + 5)$
square metres.

Picture the new rectangle cut into four pieces: the old square, a strip
$x$ by 5, a strip 3 by $x$, and a small corner, 3 by 5. Each piece is
one term of the first bracket times one term of the second:

| times | $x$ | $5$ |
|---|---|---|
| $x$ | $x^2$ | $5x$ |
| $3$ | $3x$ | $15$ |

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

patio = expand_brackets([3, 1], [5, 1])
print(patio)
```

It prints `[15, 8, 1]`, which is $x^2 + 8x + 15$. Is the expansion an
identity? Let's substitute, and compare with Python multiplying the two
brackets itself:

```python exec
id: rules-with-expand-2
for side in range(-20, 21):
    assert evaluate(patio, side) == (side + 3) * (side + 5)
print("The two sides agree for every whole number from -20 to 20.")
```

Here the check says more than it seems to. Two different quadratics can
agree at two values of $x$ at most. So if two quadratics agree at three
or more values, they are the same quadratic. The 41 values we tried are
a proof.

A loop that multiplies two brackets can multiply three: expand two of
them, then multiply the answer by the third. How long will the list for
$(x + 1)(x + 2)(x + 3)$ be?

```python exec
id: rules-with-expand-3
cubic = expand_brackets(expand_brackets([1, 1], [2, 1]), [3, 1])
print(cubic)

for x in range(-10, 11):
    assert evaluate(cubic, x) == (x + 1) * (x + 2) * (x + 3)
print("It checks out.")
```

It is `[6, 11, 6, 1]`: the cubic $x^3 + 6x^2 + 11x + 6$. Three linear
brackets make a cubic, and two make a quadratic.

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

It is true for $x = 0$ only, so it is an equation with one answer, and
not an identity. The expansion, `[9, 6, 1]`, shows what went missing:
$(x + 3)^2 = x^2 + 6x + 9$. For any number $a$, the same grid gives
$(x + a)^2 = x^2 + 2ax + a^2$. In the patio picture, $x^2 + 9$ keeps the
big square and the small corner, and forgets the two strips, each $3x$.
The move is right in the one case where the strips have no width: when
$x$ is 0.

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

This page checked every piece of algebra by putting numbers in: the
pancake identity, the band's takings, the patio's area. A second way is
to prove each step from rules, such as "multiply each term inside the
bracket", and never try a number.

Proof by rules is what algebra is for, in the end. It covers every
number at once, and a list of checks never can, except in special cases
like the quadratics above.

We checked with numbers because a check is something you can run and
trust, even before you trust the rules. It also finds a mistake at once.
The cost is that a passing check can feel like more than it is: it
shows a rule works for the numbers you tried.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a letter, which names any number (an expression), an unknown number (an equation) or every number at once (an identity); a polynomial, named by its list of coefficients |
| What is promised? | an identity promises that its two sides agree for every value; `evaluate` promises the value of a polynomial at $x$ |
| What happens when? | powers before multiplying; expand first, then collect like terms; in `expand_brackets`, every $i$ meets every $j$ |
| What does this space let us do? | any move we may make with a number, we may make with a letter; Python needs a value for each name, so we check by substituting |

## What we have now

| Term or tool | What it means |
|---|---|
| expression | a rule of numbers, letters and operations; it has a value once each letter has one |
| equation, solving | a sentence saying two expressions are equal; solving finds the values that make it true |
| identity | an equation true for every value of its letters |
| evaluate, substitution | work out an expression's value by putting a number in place of its letter |
| term, coefficient, constant term | a number times a power of the letter; the number in front; the term with no letter |
| polynomial, degree | a sum of terms with whole-number powers; its highest power |
| linear, quadratic, cubic | degree 1, 2 and 3 |
| a polynomial as a list | coefficients lowest power first: `[-2, 5, 3]` is $3x^2 + 5x - 2$ |
| `evaluate(coefficients, x)` | your toolkit function: a polynomial's value at $x$ |
| like terms, collecting, simplifying | terms with the same power; add their coefficients; fewer parts, same value |
| expanding brackets | multiply every term of one bracket by every term of the other, then collect |
| $(x + a)^2 = x^2 + 2ax + a^2$ | a squared bracket: the big square, two strips of $ax$, and the small corner |

For more, the page
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive),
from another course, builds tools that print, add, subtract and scale
polynomials kept as lists.

The practice page is next. On the next page,
[Drawing a rule](tutorial:drawing-a-rule), we draw $(x - 2)(x + 2)$ as a
picture.
