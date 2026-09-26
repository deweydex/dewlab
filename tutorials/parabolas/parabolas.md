---
title: "Parabolas: completing the square"
year: "2026-2027"
version: 2026.09.26.1
covers:
  every-quadratic-is-the-same-curve:
    covers: [MIT-3.4]
  the-form-that-tells-you-where-the-bottom-is:
    covers: [MIT-3.4]
  doing-the-rearrangement:
    covers: [MIT-3.4]
  roots-from-the-same-form:
    covers: [MIT-3.4]
worlds:
  rockets: Rockets, launches and the arcs they fly. The numbers are made up.
  electronics: Batteries, resistors and the power between them. The numbers are made up.
  fantasy-maps: A made-up kingdom, its castle and its catapult. The numbers are made up.
---

# Parabolas: completing the square

A quadratic makes a curve with one turn in it. A *parabola* is the curve
that a quadratic makes.

In [Functions and their graphs](tutorial:drawing-functions) we drew
quadratics. In
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
we solved them with the formula. On this page we do a third thing with
a quadratic. We rewrite it in a form that shows where the curve turns,
so that we can read it straight from the expression.

This rewriting is called completing the square. Many people learn it as
a trick, without being told what it is for. Its purpose is the best
reason to learn it, so we start there.

## Every quadratic is the same curve

Here are three quadratics. How are the three curves different?

```python exec
id: every-quadratic-is-the-same-curve-1
import matplotlib.pyplot as plt

def draw(f, low=-6, high=6, steps=300, label=None, ax=None):
    """Plot any function of one number, from low to high."""
    xs = [low + (high - low) * i / steps for i in range(steps + 1)]
    if ax is None:
        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend()
    return ax


def quadratic(a, b, c):
    return lambda x: a * x ** 2 + b * x + c


ax = draw(quadratic(1, 0, 0), label="x^2")
draw(quadratic(1, -6, 5), label="x^2 - 6x + 5", ax=ax)
draw(quadratic(1, 4, 7), label="x^2 + 4x + 7", ax=ax)
ax.set_ylim(-6, 20)
ax.set_title("Three quadratics")
```

The three curves sit in different places. Now let's slide each one, so
that its lowest point sits at the origin, $(0, 0)$. What do you expect
to see?

```python exec
id: every-quadratic-is-the-same-curve-2
# Shift each one by hand so its turning point lands on (0, 0).
fig, ax2 = plt.subplots()
ax2.axhline(0, color="black", linewidth=0.8)
ax2.axvline(0, color="black", linewidth=0.8)
ax2.grid(alpha=0.3)
xs = [x / 30 for x in range(-150, 151)]
ax2.plot(xs, [x ** 2 for x in xs], linewidth=4, alpha=0.3, label="x^2")
ax2.plot(xs, [quadratic(1, -6, 5)(x + 3) + 4 for x in xs], "--", label="x^2 - 6x + 5, shifted")
ax2.plot(xs, [quadratic(1, 4, 7)(x - 2) - 3 for x in xs], ":", label="x^2 + 4x + 7, shifted")
ax2.legend()
ax2.set_title("All three, moved on top of each other")
```

The three curves land exactly on top of each other.

**They are one parabola.** Every quadratic with the same $a$ (the number
in front of $x^2$) is the same curve, slid sideways and up or down. A
different $a$ stretches the curve, or turns it upside down if $a$ is
negative. The shape underneath stays the same.

So a quadratic has only a few facts that matter:

- **where its turning point is**
- **how wide it is**, and which way it opens

Everything else follows from those.

## The form that tells you where the bottom is

The turning point of a parabola is called its *vertex*. It is the
lowest point when the parabola opens upwards, and the highest point
when it opens downwards.

Every quadratic can be written in this form:

$$a(x - h)^2 + k$$

Here $a$ is the same number that was in front of $x^2$, and the vertex
is at $(h, k)$. We call it the *vertex form*. For example,
$x^2 + 6x + 5$ is the same function as $(x + 3)^2 - 4$. In vertex form
that is $1(x - (-3))^2 + (-4)$, so $a = 1$, $h = -3$ and $k = -4$. Do
the two columns agree?

```python exec
id: the-form-that-tells-you-where-the-bottom-is-1
def standard(x):
    return x ** 2 + 6 * x + 5


def vertex_form(x):
    return (x + 3) ** 2 - 4


for value in [-6, -3, 0, 2, 7]:
    print(f"x = {value:>3}    standard: {standard(value):>4}    vertex form: {vertex_form(value):>4}")
```

The two columns are the same every time, because they are the same
function. Now we plot the vertex form, with its vertex marked.

```python exec
id: the-form-that-tells-you-where-the-bottom-is-2
ax = draw(vertex_form, low=-9, high=3, label="(x + 3)^2 - 4")
ax.set_ylim(-6, 20)
ax.plot([-3], [-4], "o", markersize=9)
```

```predict
type: choice

Before you run it: where will the marked lowest point of $(x + 3)^2 - 4$
be?

- At $(3, -4)$
  - The bracket has $+3$ in it, and the $-4$ is the height.
- At $(-3, -4)$
- At $(3, 4)$
  - The two numbers in the expression are 3 and 4.
```

The vertex is at $(-3, -4)$. The second number is the height, and it
keeps its sign. The first number flips. The bracket $(x + 3)^2$ is
zero at $x = -3$, and a square is never less than zero, so that is
where the curve is lowest. The vertex form hides the flip inside
$x - h$: with $h = -3$, $x - h$ is $x + 3$.

Why is this point the bottom of the curve? Because a square is never
negative. $(x + 3)^2$ is zero at $x = -3$ and positive everywhere else.
So $-4$ is the smallest value this function ever gives. When $a$ is
negative, the same reasoning makes $k$ the largest value instead.

That is the whole idea. Completing the square is worth doing because it
makes the vertex visible. It works because a squared number cannot be
negative.

## Doing the rearrangement

How do we get from $ax^2 + bx + c$ to $a(x - h)^2 + k$? Multiply out
the vertex form, and compare the two:

$$a(x - h)^2 + k = ax^2 - 2ahx + ah^2 + k$$

The $x^2$ terms match already. For the $x$ terms to match, $-2ah$ must
be $b$, so

$$h = -\frac{b}{2a}$$

For the numbers on their own to match, $ah^2 + k$ must be $c$, so

$$k = c - ah^2$$

So the whole method is: halve $b$, divide by $a$ and change the sign
to get $h$. Then take $ah^2$ away from $c$ to get $k$. The halving is
there because $(x - h)^2$ has $2h$ in the middle.

Let's check it on $x^2 + 6x + 5$, where $a = 1$. Then
$h = -\frac{6}{2} = -3$, and $k = 5 - 1 \times 9 = -4$. That is
$(x + 3)^2 - 4$, as before. The cell checks $(x + 3)^2$ against
$x^2 + 6x + 9$ for a few values of $x$.

```python exec
id: doing-the-rearrangement-1
h = -3
for x in [0, 1, 2, 5]:
    print(f"x = {x}:  (x + 3)^2 = {(x - h) ** 2}   and   x^2 + 6x + 9 = {x**2 + 6*x + 9}")
```

$(x + 3)^2$ is $x^2 + 6x + 9$. It has the right $x^2$ and the right
$6x$, but a 9 where we want a 5. So we subtract the 9 and add the 5,
and that is where $k = 5 - 9 = -4$ comes from.

### Your turn

Can you write `complete_the_square(a, b, c)`? It returns the three
numbers $a$, $h$ and $k$ of the vertex form, in that order.

```python exec
id: doing-the-rearrangement-2
def complete_the_square(a, b, c):
    """Rewrite ax^2 + bx + c as a(x - h)^2 + k, and return a, h and k."""
    # Your code here.
```

```hint
Which of $h$ and $k$ can you find first? The formula for $k$ uses $h$.
```

```inputs
guess: yes
complete_the_square(1, 6, 5)
complete_the_square(1, -4, 1)
complete_the_square(2, 12, 5)
complete_the_square(-1, 4, 0)     # a negative a: the curve opens downwards
```

```solution
def complete_the_square(a, b, c):
    """Rewrite ax^2 + bx + c as a(x - h)^2 + k, and return a, h and k."""
    h = -b / (2 * a)
    k = c - a * h ** 2
    return a, h, k
---
`complete_the_square(2, 12, 5)` returns `(2, -3.0, -13.0)`, so
$2x^2 + 12x + 5 = 2(x + 3)^2 - 13$. With $a = -1$, the vertex $(2, 4)$
is the highest point, not the lowest.
```

Do the two forms agree for every $x$? This cell tries 200 random values
of $x$ for each quadratic, using your function. Then it draws both
forms of one of them, on top of each other, with the vertex marked.

```python exec
id: doing-the-rearrangement-3
import random

def agree(a, b, c, tries=200):
    a, h, k = complete_the_square(a, b, c)
    for _ in range(tries):
        x = random.uniform(-50, 50)
        if abs((a * x ** 2 + b * x + c) - (a * (x - h) ** 2 + k)) > 1e-6:
            return False
    return True


print(all(agree(a, b, c) for a, b, c in [(1, 6, 5), (1, -4, 1), (2, 12, 5), (-1, 4, 0), (3, 0, 0)]))

a, h, k = complete_the_square(2, 12, 5)
ax = draw(quadratic(2, 12, 5), low=-7, high=1, label="2x^2 + 12x + 5")
ax.plot([h], [k], "o", markersize=9)
draw(lambda x: a * (x - h) ** 2 + k, low=-7, high=1, label="vertex form", ax=ax)
```

The two curves lie on top of each other, and the marked vertex sits on
the curve, at its lowest point. The algebra predicted the vertex, and
the picture shows it there.

### Your turn, on paper

Here are five quadratics. Can you complete the square on each by hand?
Write your answers as comments. Then check each with your
`complete_the_square`.

- $x^2 + 8x + 3$
- $x^2 - 2x + 6$
- $x^2 + 5x$
- $3x^2 - 12x + 7$
- $x^2 - 12x + 36$

Look at the last one before you start. What do you notice about it?

```python exec
id: your-turn-1
# Your answers as comments, then:
# print(complete_the_square(1, 8, 3))
```

<details class="dl-answer"><summary>answer</summary>

- $x^2 + 8x + 3 = (x + 4)^2 - 13$, vertex $(-4, -13)$.
- $x^2 - 2x + 6 = (x - 1)^2 + 5$, vertex $(1, 5)$.
- $x^2 + 5x = (x + 2.5)^2 - 6.25$, vertex $(-2.5, -6.25)$.
- $3x^2 - 12x + 7 = 3(x - 2)^2 - 5$, vertex $(2, -5)$. Here
  $h = \frac{12}{6} = 2$ and $k = 7 - 3 \times 4 = -5$.
- $x^2 - 12x + 36 = (x - 6)^2$, vertex $(6, 0)$. There is nothing left
  over, because 36 is already the square of half of 12. The vertex sits
  on the axis.

</details>

## Roots from the same form

The vertex form also gives us the roots. A root is a value of $x$ where
the function is zero. So we set the vertex form equal to zero and undo
it one step at a time, from the outside in:

$$
\begin{aligned}
a(x - h)^2 + k &= 0 \\
(x - h)^2 &= -\frac{k}{a} \\
x - h &= \pm\sqrt{-\frac{k}{a}} \\
x &= h \pm \sqrt{-\frac{k}{a}}
\end{aligned}
$$

For $(x + 3)^2 - 4$, $h = -3$ and $-\frac{k}{a} = 4$, so
$x = -3 \pm 2$. That gives $x = -1$ and $x = -5$.

The $\pm$ is there because both $2^2$ and $(-2)^2$ are 4. That step is
why a quadratic can have two roots.

The next cell finds roots in two ways: by completing the square, and by
the formula. Do you expect the two methods to agree?

```python exec
id: roots-from-the-same-form-1
import math

def roots_by_completing(a, b, c):
    a, h, k = complete_the_square(a, b, c)
    if -k / a < 0:
        return "No real roots."
    root = math.sqrt(-k / a)
    return (h + root, h - root)


def roots_by_formula(a, b, c):
    d = b ** 2 - 4 * a * c
    if d < 0:
        return "No real roots."
    return ((-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a))


for a, b, c in [(1, 6, 5), (1, -4, 1), (2, 12, 5), (1, 2, 7)]:
    print(f"a = {a}, b = {b}, c = {c}")
    print("   completing the square:", roots_by_completing(a, b, c))
    print("   the formula:          ", roots_by_formula(a, b, c))
```

Both methods give the same answers.

Why? **The quadratic formula is completing the square, done once with
letters.** Put $h = -\frac{b}{2a}$ and $k = c - ah^2$ into
$h \pm \sqrt{-\frac{k}{a}}$, and tidy it up. What comes out is

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

If you have seen a formula built, you can build it again when you
forget it.

## When there is nothing to find

Where is the vertex of $x^2 + 2x + 7$? Does the curve reach the
horizontal axis?

```python exec
id: when-there-is-nothing-to-find-1
ax = draw(quadratic(1, 2, 7), low=-7, high=5, label="x^2 + 2x + 7")
ax.set_ylim(-2, 30)
a, h, k = complete_the_square(1, 2, 7)
ax.plot([h], [k], "o", markersize=9)
```

The vertex is at $(-1, 6)$, above the axis, and the curve opens
upwards. So the curve never comes down to zero, and there are no real
roots.

We can see this from the vertex form, $(x + 1)^2 + 6$, without
calculating anything. The square $(x + 1)^2$ is never negative, so the
whole expression is always at least 6. In the roots formula above,
$-\frac{k}{a} = -6$, and a negative number has no real square root.

The formula tells us the same thing with a negative discriminant. The
vertex form says it in a way we can picture. The next page,
[Complex numbers: roots that are not real](tutorial:complex-roots),
shows where those roots have gone. They exist, but not on this line.

## The vertex in your world

<div class="dl-world" data-world="rockets">

The rocket's height is $-4.9t^2 + 15t + 2$ metres after $t$ seconds.
Its vertex is the top of its flight. Can you use `complete_the_square`
to find when the rocket is highest and how high it goes? Keep them as
`h` and `k`. Then use the roots to find when it lands, and keep that as
`landing`.

```python exec
id: the-vertex-in-your-world-1--rockets
rocket = (-4.9, 15, 2)    # a, b and c
```

```hint
Which of $h$ and $k$ is a time, and which is a height? A root is a time
when the height is zero. Which of the two roots makes sense here?
```

```inputs
h    # the time of the highest point
k    # the highest point
landing
```

```solution
import math


def complete_the_square(a, b, c):
    h = -b / (2 * a)
    return a, h, c - a * h ** 2


a, h, k = complete_the_square(*rocket)
root = math.sqrt(-k / a)
print("highest at", h, "s, at", k, "m")
print("roots:", h - root, h + root)
landing = h + root
---
`complete_the_square` is your function from earlier on the page.
`*rocket` hands it the three numbers one by one. The rocket is highest
at about 1.53 s, at about 13.48 m. The roots are about $-0.13$ s and
3.19 s, and it lands at 3.19 s. The negative root is a time before the
launch, which is not part of this flight.
```

</div>

<div class="dl-world" data-world="electronics">

The 12 V supply from
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
delivers $-2I^2 + 12I$ watts at a current of $I$ amps. Its vertex is
the most power it can deliver. Can you use `complete_the_square` to
find the best current and the most power, as `h` and `k`? Then find the
resistance that draws that current, as `resistance`. The voltage it
gets is $12 - 2I$, and the resistance is voltage divided by current.

```python exec
id: the-vertex-in-your-world-1--electronics
supply = (-2, 12, 0)    # a, b and c
```

```hint
Which of $h$ and $k$ is a current, and which is a power? Once you have
the current, what voltage is left for the resistor?
```

```inputs
h    # the best current
k    # the most power
resistance
```

```solution
def complete_the_square(a, b, c):
    h = -b / (2 * a)
    return a, h, c - a * h ** 2


a, h, k = complete_the_square(*supply)
voltage = 12 - 2 * h
resistance = voltage / h
print("best current:", h, "A, giving", k, "W")
print("resistance:", resistance, "ohms")
---
`complete_the_square` is your function from earlier on the page. The
most power is 18 W, at 3 A. The resistor then gets 6 V, so it is
$\frac{6}{3} = 2$ ohms, the same as the resistance inside the supply.
This is true for any supply: it delivers the most power to a resistor
that matches its own inside resistance.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A catapult on the castle wall throws a stone. When the stone is $x$
metres out from the wall, its height is $-0.02x^2 + 0.8x + 6$ metres.
Can you use `complete_the_square` to find how far out the stone is at
its highest, and how high it goes, as `h` and `k`? Then use the roots to
find where it lands, as `landing`.

```python exec
id: the-vertex-in-your-world-1--fantasy-maps
stone = (-0.02, 0.8, 6)    # a, b and c
```

```hint
Which of $h$ and $k$ is a distance out from the wall, and which is a
height? Which of the two roots is in front of the wall?
```

```inputs
h    # how far out the highest point is
k    # the highest point
landing
```

```solution
import math


def complete_the_square(a, b, c):
    h = -b / (2 * a)
    return a, h, c - a * h ** 2


a, h, k = complete_the_square(*stone)
root = math.sqrt(-k / a)
print("highest", h, "m out, at", k, "m")
print("roots:", h - root, h + root)
landing = h + root
---
`complete_the_square` is your function from earlier on the page. The
stone is highest 20 m out, at 14 m. The roots are about $-6.5$ m and
46.5 m. The stone lands about 46.5 m from the wall. The negative root
is behind the wall, where the stone never was.
```

</div>

## Looking back

There is one curve, moved around, and the vertex form says where it has
been moved to. Think about $x^2 - 6x + 5$ and $(x - 3)^2 - 4$. Which
of the two would you prefer to be given to find the vertex, and which
to find where the curve crosses the vertical axis? Why?

A challenge: can you draw the vertex of $x^2 + bx$ for every whole
number $b$ from $-4$ to 4? In
[Functions and their graphs](tutorial:drawing-functions) those vertices
seemed to lie on $y = -x^2$. With `complete_the_square`, can you show
why?

```python challenge
import matplotlib.pyplot as plt

def complete_the_square(a, b, c):
    h = -b / (2 * a)
    return a, h, c - a * h ** 2


fig, ax = plt.subplots()
for b in range(-4, 5):
    a, h, k = complete_the_square(1, b, 0)
    ax.plot([h], [k], "o")
```

## Where to read more

Khan Academy. *Example 3: Completing the Square.*
<https://www.youtube.com/watch?v=TV5kDqiJ1Os>. It shows the same
halve-square-subtract steps as this page, on a different quadratic.

Stand-up Maths (2016). *There is only One True Parabola.*
<https://www.youtube.com/watch?v=hoh4TmPzu1w>. Every parabola is the same
curve, made bigger or smaller and moved. Matt Parker shows why. Completing
the square finds how much it was moved. About nine minutes.
