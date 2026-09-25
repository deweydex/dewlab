---
title: "When there is no real answer: complex numbers — Practice"
practice_for: when-there-is-no-real-answer
year: "2026-2027"
version: 2026.09.25.1
---

# When there is no real answer: complex numbers — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, with `evaluate`, `solve_quadratic`
and `close_enough`. `solve_quadratic_complex` was a cell on the
tutorial, not a toolkit tool, so the core section starts by writing it
again. `cmath` is not loaded: each cell that needs it starts with
`import cmath`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: no-real-practice-warm-up
import cmath
# Try things here
```

**1. Predict.** What does this line print?

```python
print(1j ** 2, (3j) ** 2, (1 + 2j).real, (1 + 2j).imag)
```

<details class="dl-answer"><summary>answer</summary>

`(-1+0j) (-9+0j) 1.0 2.0`.

$i^2 = -1$, and $(3i)^2 = 9i^2 = -9$. Python shows each as a complex
number with 0 as its imaginary part. The real part of $1 + 2i$ is 1 and
its imaginary part is 2, and Python gives both as floats.

</details>

**2. Predict.** What do these give? Guess before you run them.

```python
print(cmath.sqrt(-9))
print(cmath.sqrt(-2))
```

<details class="dl-answer"><summary>answer</summary>

`3j`, because $(3i)^2 = -9$. And `1.4142135623730951j`, which is
$\sqrt{2}\,i$: the square root of 2 from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#families-of-numbers),
turned a quarter turn. `math.sqrt` would refuse both.

</details>

**3. Explain.** Schlomi, who is learning Python too, says: "The square
root of −1 does not exist. My teacher told me so." Was she told
something false?

<details class="dl-answer"><summary>answer</summary>

No. Her teacher was working in the real numbers, $\mathbb{R}$, and in
$\mathbb{R}$ no number squares to make −1. That is true, and `math.sqrt`
agrees.

In the bigger space $\mathbb{C}$, there is such a number, $i$, and
there are two square roots of −1: $i$ and $-i$. Both statements are
true, each in its own space. It is the same as "you cannot take 5 from
3", which is true in $\mathbb{N}$ and not in $\mathbb{Z}$. One helpful
reply to Schlomi asks which space she means.

</details>

**4. Make.** Work out $(3 + 4i) + (1 - 2i)$ and $(3 + 4i)(1 - 2i)$ by
hand. Then check both in Python.

<details class="dl-answer"><summary>answer</summary>

Adding: $(3 + 1) + (4 - 2)i = 4 + 2i$.

Multiplying out the brackets:
$3 - 6i + 4i - 8i^2 = 3 - 2i + 8 = 11 - 2i$, because $-8i^2 = +8$.

```python
print((3 + 4j) + (1 - 2j))
print((3 + 4j) * (1 - 2j))
```

Python gives `(4+2j)` and `(11-2j)`.

</details>

## Core

The first cell writes `solve_quadratic_complex` again, as on the
tutorial. Run it first. Use the second cell for your working.

```python exec
id: no-real-practice-solver
import cmath


def solve_quadratic_complex(a, b, c):
    """Return both roots of a*x**2 + b*x + c = 0 as complex numbers.

    a must not be 0. When the discriminant is 0, the two roots are equal.
    """
    root = cmath.sqrt(b ** 2 - 4 * a * c)
    return [(-b - root) / (2 * a), (-b + root) / (2 * a)]
```

```python exec
id: no-real-practice-core
# Your working for problems 5 to 12
```

**5. Predict.** A game keeps the tip of a spaceship's nose at the point
$2 + i$, and turns the ship a quarter turn each time a key is pressed.
What will this print?

```python
nose = 2 + 1j
for press in range(4):
    print(nose)
    nose = nose * 1j
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Multiply out $(2 + i) \times i = 2i + i^2$.
2. Write $i^2$ as −1.
3. Do the same again to the answer.

</details>

<details class="dl-answer"><summary>answer</summary>

```text
(2+1j)
(-1+2j)
(-2-1j)
(1-2j)
```

$(2 + i)i = 2i + i^2 = -1 + 2i$. On the plane, the point $(2, 1)$ goes
to $(-1, 2)$, then $(-2, -1)$, then $(1, -2)$: a quarter turn against
the clock each time. One more press brings it back to $(2, 1)$.

</details>

**6. Make.** Solve $x^2 + 2x + 10 = 0$. First work out the discriminant,
and say how many real roots there are. Then find the complex roots with
`solve_quadratic_complex`, and put each one back with `evaluate`.

<details class="dl-answer"><summary>answer</summary>

The discriminant is $2^2 - 4 \times 1 \times 10 = -36$, so there are no
real roots.

```python
print(solve_quadratic(1, 2, 10))
for x in solve_quadratic_complex(1, 2, 10):
    print(x, evaluate([10, 2, 1], x))
```

`solve_quadratic` gives `[]`. The complex roots are $-1 - 3i$ and
$-1 + 3i$, and each gives 0 when put back. The square root of −36 is
$6i$, so the formula gives $\frac{-2 \pm 6i}{2} = -1 \pm 3i$.

</details>

**7. Fix.** This cell should turn a triangle a quarter turn. It stops
with an error. Read the last line of the error, then fix it.

```python exec
id: no-real-practice-fix-j
triangle = [0, 2, 1 + 1j]
turned = []
for corner in triangle:
    turned.append(corner * j)
print(turned)
```

<details class="dl-answer"><summary>answer</summary>

The last line is `NameError: name 'j' is not defined`. On its own, `j`
is a name, like `x` or `total`, and nothing has that name. The number
$i$ is written `1j`, with the 1:

```python
    turned.append(corner * 1j)
```

Now it prints `[0j, 2j, (-1+1j)]`. The corner at 0 stays where it is,
because 0 is the centre of the turn.

</details>

**8. Explain.** On the tutorial, the two roots of $x^2 - 2x + 5 = 0$
were $1 - 2i$ and $1 + 2i$: conjugates. For a quadratic whose $a$, $b$
and $c$ are real numbers, why do complex roots always come as a pair
like this? Look at the quadratic formula.

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

In $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$, the only part that can
make an $i$ is the square root of a negative discriminant. Everything
else, $-b$ and $2a$, is real. So both roots have the same real part,
$-\frac{b}{2a}$. The $\pm$ adds the imaginary part once and takes it
away once, so the imaginary parts are opposites. On the plane, the two
roots are mirror images across the line of real numbers.

</details>

**9. Another way.** A quarter turn against the clock sends the point
$(x, y)$ to $(-y, x)$. You can see it on squared paper: turn the page,
and "across" becomes "up". Check that this rule and multiplying by
`1j` agree, for the points $(3, 2)$, $(-1, 4)$ and $(0, -5)$.

<details class="dl-answer"><summary>answer</summary>

```python
for x, y in [(3, 2), (-1, 4), (0, -5)]:
    by_rule = complex(-y, x)
    by_multiplying = complex(x, y) * 1j
    print(by_rule, by_multiplying, by_rule == by_multiplying)
```

All three lines end in `True`. `complex(x, y)` makes the number
$x + yi$. The rule and the multiplication agree because
$(x + yi) \times i = xi + yi^2 = -y + xi$. So the geometry and the
algebra are two ways of saying one thing.

</details>

**10. Predict.** This cell is meant to fail. Which error do you expect,
and why? Then run it.

```python
print(sorted([3, 1j, 2]))
```

<details class="dl-answer"><summary>answer</summary>

`TypeError: '<' not supported between instances of 'complex' and
'int'`. To sort, Python compares values with `<`, and complex numbers
have no `<`. There is no order for points on a plane that keeps the
rules of $\mathbb{R}$. That is why the toolkit's `solve_quadratic`
promises real roots, smallest first: only in $\mathbb{R}$ does
"smallest first" mean anything.

</details>

**11. Fix.** Schlomo, who is also learning Python, puts the roots of
$2x^2 + 3x + 5 = 0$ back in to check them. His check fails, although
the roots are true roots. Find the line in the check that makes it
fail.

```python exec
id: no-real-practice-fix-zero
for x in solve_quadratic_complex(2, 3, 5):
    left_side = evaluate([5, 3, 2], x)
    print(x, left_side)
    assert left_side == 0, "not a root"
print("Both roots check out.")
```

<details class="dl-answer"><summary>answer</summary>

The left side comes back as `(4.440892098500626e-16+0j)`, not exactly
0. The roots are floats, and each step rounds a tiny amount, as on
[Does it work?](tutorial:does-it-work). `==` asks for exactly 0, so the
check fails. Use `close_enough`:

```python
    assert close_enough(left_side, 0), "not a root"
```

`close_enough` works on complex numbers, because `abs` of a complex
number is its distance from 0 on the plane.

</details>

**12. Make.** Write a loop that checks `solve_quadratic` and
`solve_quadratic_complex` agree on quadratics that have real roots.
Try $x^2 - 5x + 6$, $2x^2 - 7x + 3$ and $x^2 - 6x + 9$. What do you
notice about the one with a repeated root?

<details class="dl-answer"><summary>answer</summary>

```python
for a, b, c in [(1, -5, 6), (2, -7, 3), (1, -6, 9)]:
    print(solve_quadratic(a, b, c), solve_quadratic_complex(a, b, c))
```

```text
[2.0, 3.0] [(2+0j), (3+0j)]
[0.5, 3.0] [(0.5+0j), (3+0j)]
[3.0] [(3+0j), (3+0j)]
```

The roots agree, with `+0j` on the complex ones. For $x^2 - 6x + 9$,
`solve_quadratic` gives one root and `solve_quadratic_complex` gives
the same root twice. Both are fair: the one root is where the curve
touches the axis, and counting it twice is how "every quadratic has two
roots" stays true in $\mathbb{C}$.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: no-real-practice-stretch
import cmath
import matplotlib.pyplot as plt
# Your working for problems 13 to 15
```

**13. Make.** An artist wants eight dots in a ring, evenly spaced, like
the points of a compass. A quarter turn is multiplying by $i$. Which
number, multiplied twice, makes a quarter turn? Find it with
`cmath.sqrt(1j)`, then multiply 1 by it again and again to make the
eight dots, and draw them.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Call the number `eighth = cmath.sqrt(1j)`, and check that
   `eighth * eighth` is very close to `1j`.
2. Start at `dot = 1`, and loop 8 times, keeping `dot.real` and
   `dot.imag` in two lists before multiplying `dot` by `eighth`.
3. Draw the lists with `plt.scatter`.

**Think about:** what `abs(eighth)` is, and why it matters that it is 1.

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
eighth = cmath.sqrt(1j)
print(eighth, eighth * eighth, abs(eighth))

across = []
up = []
dot = 1
for step in range(8):
    across.append(dot.real)
    up.append(dot.imag)
    dot = dot * eighth
plt.scatter(across, up)
plt.gca().set_aspect("equal")
```

`eighth` is about $0.707 + 0.707i$, an eighth of a turn, the point
halfway between 1 and $i$. Squared, it gives very nearly `1j`. Its
distance from 0, `abs(eighth)`, is 1, so each multiply turns a dot
without moving it nearer to 0 or further away. The eight dots sit on a
circle of radius 1, like a compass. A later unit comes back to points
on a circle, with sine and cosine.

</details>

**14. Another way.** On the tutorial, $x^2 + 1 = 0$ had roots $i$ and
$-i$, found with the formula. Find them a second way, with the picture:
$x^2 = -1$ asks for a number that, done twice, is a half turn. Which
turns, done twice, make a half turn? Check your answer in Python.

<details class="dl-answer"><summary>answer</summary>

A quarter turn against the clock, done twice, is a half turn: that is
multiplying by $i$. A quarter turn with the clock, done twice, is also
a half turn, the other way round: that is multiplying by $-i$. So the
two roots are $i$ and $-i$.

```python
print(1j * 1j, -1j * -1j)
```

Both give `(-1+0j)`, which matches the formula's roots.

</details>

**15. Explain.** The tutorial gave $i$ a picture: a point on a plane,
and a quarter turn when we multiply by it. Many courses give only the
rule, $i^2 = -1$, and practise the algebra of $a + bi$ with no picture.
Which way would you have wanted to learn it, and why? There is no
single answer.

<details class="dl-answer"><summary>answer</summary>

An answer might weigh a few things, and can land on either side.

- **What each one explains.** The picture gives $i^2 = -1$ a reason:
  two quarter turns make a half turn. The rule on its own asks you to
  accept it.
- **What each one costs.** The rule is shorter, and it is all that
  solving a quadratic needs. The picture adds geometry that the
  quadratics did not use.
- **What comes next.** Exam questions on complex numbers are mostly
  the algebra. Turning and signals, in games and engineering, use the
  picture.
- **The word "imaginary".** A picture may make the numbers feel less
  like a trick. For some people, a clean rule does that better.
- **You.** Some people trust an idea once they can see it. Others trust
  it once they can calculate with it.

It is also fair to want both, in one order or the other.

</details>
