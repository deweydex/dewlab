---
title: "When there is no real answer: complex numbers"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-question-with-no-answer-here:
    covers: [MIT-1.10]
  pythons-j:
    covers: [MIT-1.10]
  the-old-moves-in-the-new-space:
    covers: [MIT-1.10]
  numbers-on-a-plane:
    covers: [MIT-1.10]
  every-quadratic-has-roots-here:
    covers: [MIT-1.10]
    touches: [PDP-LO8]
  what-the-bigger-space-costs:
    touches: [MIT-1.10, PDP-LO9]
---

# When there is no real answer: complex numbers

Type `2j` into a Python cell, and Python does not complain. It shows
`2j` back. Now type `2j * 2j`, and Python gives `(-4+0j)`, which is −4.
So `2j` is a number that squares to make a negative. On the last page,
no real number could do that. Python has been keeping a number that
"does not exist" ready all along. What does it mean by `2j`, and why
does it keep one ready?

I think this is the strangest page in the unit. The new numbers look
like a trick at first. By the end, they turn a shape
on a screen, and every quadratic has its roots.

On this page we:

- see why $x^2 = -1$ has no answer on the number line
- build a bigger space where it has one, the same way $\mathbb{Z}$ was
  built from $\mathbb{N}$
- meet Python's complex numbers, `1j`, `2j` and `cmath.sqrt`
- draw complex numbers as points on a plane, and see that multiplying
  by `1j` is a quarter turn
- solve every quadratic, and check each root by putting it back
- find what the bigger space takes away

> **The space we're in.** This page starts in the real numbers,
> $\mathbb{R}$, and builds a bigger space around them, the complex
> numbers. Every real number is still there, and almost every move we
> could make before still works. The last section finds the one that
> does not. The name "imaginary", which we will meet, comes from
> history. It is not a
> sign that these numbers are less useful than the others. Your toolkit
> is loaded, with `evaluate`, `solve_quadratic` and `close_enough`.

## Warm-up

The first question is from
[Solving for x](tutorial:solving-for-x#how-many-answers-the-discriminant),
and the second from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#families-of-numbers).

```question
id: no-real-warm-up-1
type: fill-in-the-blank

$x^2 + 4 = 0$ has discriminant $0^2 - 4 \times 1 \times 4 = -16$, so it
has {no|one|two} real roots.
```

```question
id: no-real-warm-up-2
type: multiple-choice
answer: 2

$3 - 5$ has no answer in the natural numbers, $\mathbb{N}$. Which is the
smallest space where it has one?

- the natural numbers, $\mathbb{N}$
  - The answer is −2, and no natural number is below 0.
- the integers, $\mathbb{Z}$
  - The integers go below 0, and −2 is one of them.
- the rational numbers, $\mathbb{Q}$
  - −2 is rational too, but the integers already hold it, and they sit inside the rationals.
```

## A question with no answer here

Which number, multiplied by itself, makes −1? Let's look at some
squares first. Before you run the cell, will any square be negative?

```python exec
id: no-real-squares-1
for x in [-3, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 3]:
    print(x, x * x)
print(solve_quadratic(1, 0, 1))
```

Every square is 0 or more. A negative times a negative is positive, a
positive times a positive is positive, and 0 times 0 is 0. So
$x^2 = -1$, which is $x^2 + 1 = 0$, has no answer in $\mathbb{R}$, and
your `solve_quadratic` returns an empty list.

We have been here before. On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#families-of-numbers),
$3 - 5$ had no answer in $\mathbb{N}$. The answer was to build a
bigger space, $\mathbb{Z}$, with new
numbers in it, −1, −2 and so on, where $3 - 5$ has an answer. The old
numbers stayed, and adding and multiplying them worked as before.

In the 1500s, mathematicians in Italy made the same move again. They
gave a name to a number that does what no real number can. The
*imaginary unit*, written $i$, is a number with one promise:

$$i^2 = -1$$

That is the whole definition. Here we name the number we want first,
and then find what it lets us do.

<aside class="dl-note" id="no-real-note-history">

**A name meant as an insult.** Gerolamo Cardano met square roots of
negative numbers in his book *Ars Magna*, in 1545, and called them
useless. Rafael Bombelli, in his *Algebra* of 1572, wrote down the
rules for adding and multiplying them, and used them to find real
answers. In 1637 René Descartes called such numbers "imaginary", and
he did not mean it kindly. The name stayed. The numbers are now some
of the most useful in science.

</aside>

## Python's j

Python has this number built in. It writes $i$ as `j`, the letter
electrical engineers use, because in their work $i$ already means an
electric current. So `1j` is $i$, and `2j` is $2i$. What do you expect
each line to show?

```python exec
id: no-real-j-1
print(1j * 1j)
print(2j * 2j)
print(type(2j))
```

`1j * 1j` is `(-1+0j)`: −1, with 0 lots of $i$ added. `2j * 2j` is
−4, because $2i \times 2i = 4i^2 = -4$. And the type of `2j` is
`complex`.

A *complex number* is a number of the form $a + bi$, where $a$ and $b$
are real numbers. The number $a$ is its *real part*, and $b$ is its
*imaginary part*. The space of all complex numbers is written
$\mathbb{C}$. Python writes $3 + 2i$ as `3 + 2j`, and can show each
part:

```python exec
id: no-real-j-2
z = 3 + 2j
print(z.real, z.imag)
print(3 == 3 + 0j)
```

`z.real` is `3.0` and `z.imag` is `2.0`. The last line says that 3 and
$3 + 0i$ are the same number. Every real number is a complex number
whose imaginary part is 0, so $\mathbb{R}$ sits inside $\mathbb{C}$,
as $\mathbb{N}$ sits inside $\mathbb{Z}$:

$$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R} \subset \mathbb{C}$$

Why would Python keep these ready? Engineers use complex numbers to
describe things that swing back and forth: the current in the wires of
a house, a radio signal, a sound. We will not need that here. We need
them for one thing, which is to finish a job the last page left
unfinished.

## The old moves in the new space

To add two complex numbers, add the real parts, then add the imaginary
parts. To multiply them, expand the brackets as on
[Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop), and
wherever $i^2$ appears, write −1. That is the only new rule.

Let's try $(2 + 3i)(4 - i)$ by hand first:

$$(2 + 3i)(4 - i) = 8 - 2i + 12i - 3i^2 = 8 + 10i + 3 = 11 + 10i$$

The $-3i^2$ became $+3$, because $i^2 = -1$. Does Python agree?

```python exec
id: no-real-moves-1
print((2 + 3j) + (4 - 1j))
print((2 + 3j) * (4 - 1j))
```

`(6+2j)` and `(11+10j)`. Note that Python writes $-i$ as `- 1j`, with
the 1. On its own, `j` would be a name, not a number.

### Your turn

1. Find $(1 + i)^2$ by hand. Remember the rule for $i^2$.
2. Check it with `(1 + 1j) ** 2`.
3. Now guess $(1 + i)^4$. It is $(1 + i)^2$ squared. Check that too.

```python exec
id: no-real-moves-your-turn
# (1 + 1j) squared, and to the power 4
```

## Numbers on a plane

The real numbers fill a line. Where does $i$ go? It is not on the line,
because no point on the line squares to −1. So we give it a new
direction. A complex number $a + bi$ becomes the point $(a, b)$: $a$
across, and $b$ up. The real numbers are the line across, and the
numbers $i$, $2i$, $3i$ go straight up from 0. This picture is called
the *complex plane*.

Now look at what multiplying by $i$ does. Start at 1 and multiply by
$i$ again and again. Predict what it prints before you run the cell.

```python exec
id: no-real-plane-1
point = 1
for turn in range(5):
    print(point)
    point = point * 1j
```

`1`, then `1j`, then `(-1+0j)`, then `(-0-1j)`, which is $-i$, then
`(1-0j)`, which is 1 again. (A float can carry a sign on 0, and $-0$
equals 0.) On the plane, that is right, then up, then left, then down,
then back to the start. Each multiply by $i$ turns the
point a quarter turn about 0, against the clock.

So here is a picture for $i^2 = -1$. Multiplying by −1 is a half turn:
it sends 3 to −3, to the other side of 0. Two quarter turns make a half
turn. So the number that squares to −1 does a quarter turn.

Does it turn a whole shape? A game keeps the corners of a small ship as
complex numbers, and turns it by multiplying every corner by `1j`. What
do you expect to see?

```python exec
id: no-real-plane-2
import matplotlib.pyplot as plt

def draw(points, label):
    """Draw complex numbers joined up: across by the real part, up by the imaginary part."""
    across = []
    up = []
    for point in points:
        across.append(point.real)
        up.append(point.imag)
    plt.plot(across, up, marker="o", label=label)

ship = [1 + 1j, 3 + 1j, 1 + 2j, 1 + 1j]
for turns in range(4):
    draw(ship, "turned " + str(turns) + " times")
    turned = []
    for corner in ship:
        turned.append(corner * 1j)
    ship = turned

plt.axhline(0, color="grey")
plt.axvline(0, color="grey")
plt.gca().set_aspect("equal")
plt.legend()
```

The ship points right, then up, then left, then down. Its size and
shape stay the same. One multiply by `1j` turns every point at once.

### Your turn

1. Multiply `3 + 2j` by `1j`. Which point do you get? Is it a quarter
   turn of the point $(3, 2)$?
2. In the ship cell, change `1j` to `-1`. Before you run it, what should
   happen to the ship?
3. Now try `2j`. What does multiplying by 2 add to the turn?

## Every quadratic has roots here

Back to the job the last page left unfinished. `math.sqrt` refuses a
negative number, because it works in $\mathbb{R}$. Python has a second
module, `cmath`, with the same functions for $\mathbb{C}$. What do you
think `cmath.sqrt(-4)` gives?

```python exec
id: no-real-roots-1
import cmath

print(cmath.sqrt(-4))
print(cmath.sqrt(9))
```

`2j`, because $(2i)^2 = -4$. And `(3+0j)`: a real answer, written as a
complex number.

Now the quadratic formula works for every quadratic. Here it is with
`cmath.sqrt`, in a cell of this page. It is not a replacement for your
toolkit's `solve_quadratic`, which keeps its promise of real roots.
Compare the two. What is missing here?

```python exec
id: no-real-roots-2
def solve_quadratic_complex(a, b, c):
    """Return both roots of a*x**2 + b*x + c = 0 as complex numbers.

    a must not be 0. When the discriminant is 0, the two roots are equal.
    """
    root = cmath.sqrt(b ** 2 - 4 * a * c)
    return [(-b - root) / (2 * a), (-b + root) / (2 * a)]

print(solve_quadratic_complex(1, 0, 1))
print(solve_quadratic_complex(1, -2, 5))
print(solve_quadratic_complex(1, 3, -40))
```

There is no `if`. Nothing can fail now, so there is no case to leave
out. $x^2 + 1 = 0$ has roots $-i$ and $i$. $x^2 - 2x + 5 = 0$ has roots
$1 - 2i$ and $1 + 2i$. And the sprite sheet from the last page still
has its roots, −8 and 5, now written with `+0j`.

Look at the two roots of $x^2 - 2x + 5$. They have the same real part,
and imaginary parts that are opposites. Two such numbers are called
*conjugates*. The $\pm$ in the formula causes this. The square root of
the discriminant is added once and taken away once. On the plane, the two
roots are mirror images across the line of real numbers.

Are these truly roots? The rule of this unit is to check, by putting
each one back. Your toolkit's `evaluate` works for complex numbers too,
because it only adds and multiplies. What do you expect?

```python exec
id: no-real-roots-3
for a, b, c in [(1, 0, 1), (1, -2, 5), (2, 3, 5), (1, -6, 9)]:
    for x in solve_quadratic_complex(a, b, c):
        print(x, evaluate([c, b, a], x))
        assert close_enough(evaluate([c, b, a], x), 0)
print("Every root checks out.")
```

Every value comes back as 0, or as something like
`(4.440892098500626e-16+0j)`. That is $4.4 \times 10^{-16}$, a float's
rounding, very close to 0, as on
[Does it work?](tutorial:does-it-work). `close_enough` works here too,
because `abs` of a complex number is its distance from 0 on the plane.

In $\mathbb{C}$, every quadratic has two roots, counting a repeated
root twice.

### Your turn

1. Before you run anything, what is the discriminant of
   $x^2 + 6x + 13$? Is it negative?
2. Find the roots with `solve_quadratic_complex`. Are they conjugates?
3. Put each root back with `evaluate`.

```python exec
id: no-real-roots-your-turn
# x**2 + 6x + 13: find the roots, then put them back
```

## What the bigger space costs

Each bigger space so far let us do more. This one also takes something
away. In $\mathbb{R}$ we can always ask which of two numbers is bigger:
the one further right on the line. Can we ask that of $i$ and 2? This
cell is meant to stop with an error. Which line stops it?

```python exec
id: no-real-costs-1
print(abs(1j), abs(2))
print(1j < 2)
```

The first line prints `1.0 2`: the distances from 0. The second stops
with `TypeError: '<' not supported between instances of 'complex' and
'int'`. Nothing was mistyped. The message says that `<` is a move this
space does not have. Points on a plane have no one order, left to
right, that keeps the rules of $\mathbb{R}$. Is $i$ bigger than 0, or
smaller? Either answer breaks a rule. In $\mathbb{R}$, a number above
0 or below 0 always squares to more than 0, and $i^2$ is −1. So
mathematicians give neither answer.

So your toolkit's `solve_quadratic` promised real roots, smallest
first. "Smallest first" means nothing in $\mathbb{C}$.

So which space should we work in? It depends on the question. A
sprite sheet's rows must be real, and the order matters. So
$\mathbb{R}$ is the space for it, and "no real roots" is the answer it
needs. A question about a turning shape, or a signal that swings, is
better asked in $\mathbb{C}$. You can always ask "which space are we
in?" Here, the space decides the answer.

<details class="dl-why"><summary>Why this way?</summary>

This page gave $i$ a picture: a point above 0 on a plane, and a quarter
turn when we multiply by it. Many courses define $i$ by its rule,
$i^2 = -1$, and then practise the algebra of $a + bi$, with no picture
at all.

The rule on its own is shorter, and it is all that solving a quadratic
needs. Exam questions on complex numbers are mostly that algebra.

We drew the plane because a rule with no picture can feel like a trick,
and "imaginary" already sounds like one. The quarter turn gives
$i^2 = -1$ a reason. The cost is a section that the quadratics did not
need, and some geometry that waits until a later unit to be used again.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | $i$, a number named for its promise $i^2 = -1$, written `1j` in Python; the real and imaginary parts of $a + bi$; $\mathbb{C}$ |
| What is promised? | $i^2 = -1$, and every old rule of adding and multiplying; `solve_quadratic_complex` promises two roots for every quadratic |
| What happens when? | multiplying by `1j` again and again turns a point a quarter turn each time, and four turns bring it back |
| What does this space let us do? | $\mathbb{C}$ lets every quadratic have roots, and `cmath.sqrt` takes the root of a negative; it has no `<`, so no "smallest first" |

## What we have now

| Term or tool | What it means |
|---|---|
| imaginary unit, $i$ | a number with $i^2 = -1$; Python writes it `1j` |
| complex number, $a + bi$ | a real part $a$ and an imaginary part $b$; `z.real`, `z.imag` |
| $\mathbb{C}$ | the complex numbers, a space that holds $\mathbb{R}$ |
| multiplying complex numbers | multiply out the brackets, then write −1 for $i^2$ |
| complex plane | $a + bi$ drawn as the point $(a, b)$ |
| multiplying by $i$ | a quarter turn about 0, against the clock |
| `cmath.sqrt(x)` | a square root that accepts negative numbers, and gives a complex answer |
| conjugates | $a + bi$ and $a - bi$: the two complex roots of a quadratic with real numbers in it |
| no order in $\mathbb{C}$ | `<` and "smallest first" have no meaning for complex numbers |

## Where to read more

Electrical engineers use complex numbers every day. The current in the
wires of a house swings back and forth, 50 times a second in Ireland,
and they write it as a complex number, whose turn on the plane says
where in its swing the current is.
In [Waves](tutorial:waves), in the next unit, a swing becomes a sine
wave.

For another route through these numbers, the integrated course has
[Complex numbers: roots that are not real](tutorial:complex-roots).

Up and Atom (2019). *Imaginary Numbers Are Just Regular Numbers.*
<https://www.youtube.com/watch?v=sZrOxm5Gszk>. Negative numbers once
seemed impossible too. Jade Tan-Holmes shows that multiplying by i is a
quarter turn, which is why these numbers live on a plane. Nine minutes.
