---
title: "Rules with letters in them: expressions, equations and identities — Practice"
practice_for: rules-with-letters-in-them
year: "2026-2027"
version: 2026.09.26.1
---

# Rules with letters in them: expressions, equations and identities — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `evaluate` from the
tutorial and `close_enough` from
[Does it work?](tutorial:does-it-work#close-enough). The tutorial's
`expand_brackets` was a page cell, not a toolkit tool, so the stretch
section copies it in. Schlomo and Schlomi, who are learning Python too,
have ideas in a few of the problems.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: rules-with-practice-warm-up
# Try things here
```

**1. Predict.** What does this cell print?

```python
x = 4
print(2 * x ** 2, (2 * x) ** 2)
```

<details class="dl-answer"><summary>answer</summary>

It prints `32 64`.

In `2 * x ** 2`, the power comes first: $4^2 = 16$, then $2 \times 16 =
32$. In `(2 * x) ** 2`, the brackets come first: $2 \times 4 = 8$, then
$8^2 = 64$. In maths, $2x^2$ means the first one.

</details>

**2. Explain.** A weather sensor sends 3 readings every 4 seconds, so
in $y$ seconds it sends $\frac{3y}{4}$ readings. Which of these is an
expression, which an equation with one answer, and which an identity?
Say why for each.

- $\frac{3y}{4}$
- $\frac{3y}{4} = 6$
- $\frac{3(y + 4)}{4} = \frac{3y}{4} + 3$

<details class="dl-answer"><summary>answer</summary>

- $\frac{3y}{4}$ is an expression. It has no equals sign. It is a rule
  that gives a number of readings once $y$ has a value.
- $\frac{3y}{4} = 6$ is an equation with one answer. It asks "after how
  many seconds are there 6 readings?", and it is true only for $y = 8$.
- $\frac{3(y + 4)}{4} = \frac{3y}{4} + 3$ is an identity. Four more
  seconds always bring 3 more readings, whatever $y$ is. You can check
  it in a loop:

```python
for seconds in range(0, 21):
    assert close_enough(3 * (seconds + 4) / 4, 3 * seconds / 4 + 3)
print("True for every value tried.")
```

</details>

**3. Make.** Write the list of coefficients for $4x^3 - x + 9$. Then use
`evaluate` to find its value at $x = 2$, and check it with Python's own
arithmetic.

<details class="dl-answer"><summary>answer</summary>

```python
cubic_list = [9, -1, 0, 4]
print(evaluate(cubic_list, 2), 4 * 2 ** 3 - 2 + 9)
```

Both give 39. The list is lowest power first: 9, then $-1$ for the $x$
term, then 0, because there is no $x^2$ term, then 4 for $x^3$. The 0
keeps the 4 at index 3.

</details>

**4. Predict.** What does each line print?

```python
print(-3 ** 2)
print((-3) ** 2)
x = -3
print(x ** 2)
```

<details class="dl-answer"><summary>answer</summary>

They print `-9`, `9` and `9`.

In `-3 ** 2`, the power comes before the minus sign, so Python
calculates $-(3^2) = -9$. In the second line, the brackets make $-3$ one
number first. In the third, `x` already names the number $-3$, so
squaring it gives 9. That is one reason to substitute by naming the
value, as `evaluate` does, and not by pasting the digits in.

</details>

## Core

A cell for the core problems.

```python exec
id: rules-with-practice-core
# Your working for problems 5 to 11
```

**5. Make.** A backup program takes 30 seconds to start, and then 25
seconds for each gigabyte it copies. Write the time for $g$ gigabytes
as an expression, then as a list. Use `evaluate` to find the time for
12 GB.

<details class="dl-answer"><summary>answer</summary>

The time is $25g + 30$ seconds, which is the list `[30, 25]`.

```python
backup = [30, 25]
print(evaluate(backup, 12))
```

12 GB take 330 seconds, five and a half minutes. The constant, the time
to start, comes first in the list, because it is the $g^0$ term.

</details>

**6. Predict.** What do these two lines print?

```python
print(evaluate([1, 1, 1, 1], 2))
print(evaluate([1, 1, 1, 1], 10))
```

<details class="dl-answer"><summary>answer</summary>

They print `15` and `1111`.

The list is $1 + x + x^2 + x^3$. At $x = 2$ it is $1 + 2 + 4 + 8 = 15$.
At $x = 10$ it is $1 + 10 + 100 + 1000 = 1111$. The second one shows
something about place value. Read from the right, the digits of a
number are the coefficients of a polynomial, with 10 in place of $x$:
$1111 = 1 + 1 \times 10 + 1 \times 10^2 + 1 \times 10^3$.

</details>

**7. Make.** Simplify $3(2x + 1) - 2(x - 4)$ by hand. Then check your
answer by substitution, for every whole number from $-10$ to 10.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Multiply out the first bracket: $3 \times 2x$ and $3 \times 1$.
2. Multiply out the second bracket. The $-2$ multiplies both terms, so
   $-2 \times -4$ is $+8$.
3. Collect the $x$ terms, then the constants.

**Think about:** which step gives people the most trouble? Where
does the check catch it?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

$3(2x + 1) - 2(x - 4) = 6x + 3 - 2x + 8 = 4x + 11$.

```python
for x in range(-10, 11):
    assert 3 * (2 * x + 1) - 2 * (x - 4) == evaluate([11, 4], x)
```

Many people write $-2(x - 4) = -2x - 8$. The check shows the difference at once.
At $x = 0$ the two sides would be 11 and $-5$.

</details>

**8. Fix.** Schlomi, who is learning Python too, wrote her own version
of `evaluate`. $x^3 - 4x$ and $x^2 - 4$ are both 0 at $x = 2$. Her
function gives 0 for the first one, but 4 for the second. Can you find
the line that does not do what she meant, and change it?

```python exec
id: rules-with-practice-fix-evaluate
def value_of(coefficients, x):
    """Return the value of a polynomial at x. coefficients is lowest power first."""
    value = 0
    for power in range(1, len(coefficients)):
        value = value + coefficients[power] * x ** power
    return value
```

```inputs
value_of([0, -4, 0, 1], 2)    # x cubed take away 4x, at 2
value_of([-4, 0, 1], 2)       # x squared take away 4, at 2
```

```solution
def value_of(coefficients, x):
    """Return the value of a polynomial at x. coefficients is lowest power first."""
    value = 0
    for power in range(len(coefficients)):
        value = value + coefficients[power] * x ** power
    return value
---
The loop started at power 1, so it never added the constant term, at
index 0. Starting at 0 adds it.

The first polynomial gave 0 in both versions, because its constant term is 0.
The second one showed the gap. A polynomial with no constant could
never show it.
```

**9. Make.** A square icon is $x$ pixels on each side. A margin adds
4 pixels to its width and 6 to its height. Expand $(x + 4)(x + 6)$, the
area of the icon and its margin, with a grid of four pieces. Then check
your expansion by substitution.

<details class="dl-answer"><summary>answer</summary>

| times | $x$ | $6$ |
|---|---|---|
| $x$ | $x^2$ | $6x$ |
| $4$ | $4x$ | $24$ |

$(x + 4)(x + 6) = x^2 + 10x + 24$, which is the list `[24, 10, 1]`.

```python
for side in range(0, 101):
    assert evaluate([24, 10, 1], side) == (side + 4) * (side + 6)
```

For an icon 40 pixels wide, the area with the margin is
$1600 + 400 + 24 = 2024$ pixels.

</details>

**10. Another way.** Calculate $29 \times 31$ in your head. The tutorial's
last "Your turn" expanded $(x - 2)(x + 2)$. Use the same idea with
$(30 - 1)(30 + 1)$, then check with Python.

<details class="dl-answer"><summary>answer</summary>

$(x - 1)(x + 1) = x^2 - 1$, because the two strips, $-x$ and $+x$,
cancel each other. With $x = 30$:

$$29 \times 31 = (30 - 1)(30 + 1) = 900 - 1 = 899$$

```python
print(29 * 31, evaluate([-1, 0, 1], 30))
```

Both give 899. The same trick gives $48 \times 52 = 2500 - 4 = 2496$.
This mental arithmetic uses an identity.

</details>

**11. Explain.** The tutorial checked each piece of algebra by
substituting numbers, and said a proof by rules is what algebra is for
in the end. A textbook often starts the other way: it teaches the rules
for brackets and like terms, and practises them by hand, with no
numbers put in. Which way would you have wanted to learn it, and why?
There is no single answer.

<details class="dl-answer"><summary>answer</summary>

An answer might weigh a few things, and can choose either way.

- **Trust.** A check you run tells you at once whether two sides
  agree. A rule you apply works only if you apply it with care.
- **Certainty.** A proof by rules covers every number. A check covers
  the numbers you tried, unless you know a fact like "two quadratics
  that agree at three values are the same".
- **Speed.** With practice, rules are faster than typing a check,
  and exams usually ask for the rules.
- **Slips.** A check shows you where two sides differ. It does not
  show you why. Knowing the rules does.
- **You.** Some people need to see a rule work on numbers before they
  believe it. Others find the numbers slow.

Many people want both in the end. Rules do the work, and a check
catches the slips.

</details>

## Stretch

The tutorial's `expand_brackets`, copied in. Run this cell before the
stretch problems.

```python exec
id: rules-with-practice-stretch
def expand_brackets(first, second):
    """Return the coefficients of first times second, with the brackets multiplied out."""
    expanded = [0] * (len(first) + len(second) - 1)
    for i in range(len(first)):
        for j in range(len(second)):
            expanded[i + j] = expanded[i + j] + first[i] * second[j]
    return expanded
```

**12. Predict.** What do these lines print? Guess the last list before
you run it.

```python
power_of_bracket = [1]
for time in range(4):
    power_of_bracket = expand_brackets(power_of_bracket, [1, 1])
    print(power_of_bracket)
```

<details class="dl-answer"><summary>answer</summary>

```text
[1, 1]
[1, 2, 1]
[1, 3, 3, 1]
[1, 4, 6, 4, 1]
```

These are $(x + 1)$, $(x + 1)^2$, $(x + 1)^3$ and $(x + 1)^4$. Each row
is the row before, added to itself shifted one place. That is what
multiplying by $x + 1$ does. The numbers are the combinations from
[Orders and choices](tutorial:orders-and-choices): the coefficient of
$x^2$ in $(x + 1)^4$ is `combinations(4, 2)`, which is 6. Each $x^2$
term comes from choosing the $x$ in 2 of the 4 brackets.

```python
for chosen in range(5):
    print(chosen, combinations(4, chosen))
```

</details>

**13. Fix.** This version, `expand_quickly`, gives a different list
from the tutorial's `expand_brackets` for $(x + 3)(x + 5)$. Can you find the line that
causes it?

```python exec
id: rules-with-practice-fix-expand
def expand_quickly(first, second):
    """Return the coefficients of first times second, with the brackets multiplied out."""
    expanded = [0] * (len(first) + len(second) - 1)
    for i in range(len(first)):
        for j in range(len(second)):
            expanded[i + j] = first[i] * second[j]
    return expanded

print(expand_quickly([3, 1], [5, 1]))
```

```inputs
expand_quickly([3, 1], [5, 1])    # (x + 3)(x + 5)
```

```solution
def expand_quickly(first, second):
    """Return the coefficients of first times second, with the brackets multiplied out."""
    expanded = [0] * (len(first) + len(second) - 1)
    for i in range(len(first)):
        for j in range(len(second)):
            expanded[i + j] = expanded[i + j] + first[i] * second[j]
    return expanded
---
The first version prints `[15, 5, 1]`, not `[15, 8, 1]`. The line
inside the loops puts each product into its place, and so it replaces
what was there. Two pieces land at index 1, $3x$ and $5x$, and only the
last one is kept. Like terms need adding, so the line now adds each
product to what is already at `expanded[i + j]`.

For a bracket times a single number, no two pieces ever land in the
same place, so the two versions agree there and the difference stays
hidden.
```

**14. Another way.** $3x^2 + 5x - 2$ can be written with no powers at
all: $(3x + 5)x - 2$. Start with the highest coefficient. Multiply by
$x$, add the next coefficient, and repeat. Write
`evaluate_nested(coefficients, x)` that works this way, and check it
against `evaluate` for many values of $x$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The list is lowest power first, so loop over it backwards, with
   `range(len(coefficients) - 1, -1, -1)`: a range with a step of $-1$.
2. Start `value` at 0. Each time round, multiply `value` by `x`, then
   add the coefficient at that index.
3. Walk through `[-2, 5, 3]` at $x = 2$ by hand: 3, then 11, then 20.

**Think about:** how many multiplications does each way need for a
polynomial of degree 10?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def evaluate_nested(coefficients, x):
    """Return the value of a polynomial at x, with no powers: highest coefficient first."""
    value = 0
    for power in range(len(coefficients) - 1, -1, -1):
        value = value * x + coefficients[power]
    return value

for x in range(-10, 11):
    assert evaluate_nested([-2, 5, 3], x) == evaluate([-2, 5, 3], x)
    assert evaluate_nested([6, 11, 6, 1], x) == evaluate([6, 11, 6, 1], x)
print(evaluate_nested([-2, 5, 3], 2))
```

It prints 20, and every check passes. This is called Horner's method.
For degree 10 it makes 10 multiplications, where calculating every
power separately needs many more. Computers often evaluate polynomials
this way.

</details>

**15. Make.** The curves in many fonts use four points, not three: a
start, an end, and two points that pull. Their four weights are
$(1 - t)^3$, $3t(1 - t)^2$, $3t^2(1 - t)$ and $t^3$. Expand each one
with `expand_brackets`, then check that the four add up to 1 for every
$t$, as the three weights did on the tutorial.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $1 - t$ is the list `[1, -1]`, $3t$ is `[0, 3]` and $t$ is `[0, 1]`.
2. Each weight is three brackets, so call `expand_brackets` twice:
   expand two of them, then expand the answer with the third.
3. To add four lists of the same length, add them place by place.

**Think about:** where have you seen the numbers 1, 3, 3, 1 before?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
one_take_t = [1, -1]
start_weight = expand_brackets(expand_brackets(one_take_t, one_take_t), one_take_t)
first_pull = expand_brackets(expand_brackets([0, 3], one_take_t), one_take_t)
second_pull = expand_brackets(expand_brackets([0, 3], [0, 1]), one_take_t)
end_weight = expand_brackets(expand_brackets([0, 1], [0, 1]), [0, 1])
print(start_weight, first_pull, second_pull, end_weight)

added = []
for power in range(4):
    added.append(start_weight[power] + first_pull[power] + second_pull[power] + end_weight[power])
print(added)
```

The weights are `[1, -3, 3, -1]`, `[0, 3, -6, 3]`, `[0, 0, 3, -3]` and
`[0, 0, 0, 1]`, and they add up to `[1, 0, 0, 0]`, which is the number 1,
for every $t$. The 1, 3, 3, 1 in front of the weights are the row for
$(x + 1)^3$ from problem 12. In fact the four weights are the four
terms of $\big((1 - t) + t\big)^3$, and $(1 - t) + t$ is 1, so they
have to add up to $1^3 = 1$. PostScript fonts, and the letters on many
screens, are drawn with these four weights.

</details>

<aside class="dl-note" id="rules-with-practice-note-truetype">

**Three points or four.** Font files draw curves in two ways. Adobe's
PostScript Type 1 fonts, from the 1980s, use curves with four points,
as in this problem. Apple's TrueType fonts, first released in 1991, use
curves with three points, as on the tutorial page. A three-point curve
can always be written exactly as a four-point one. A four-point curve
often needs several three-point curves to copy it closely.

</aside>

**16. Explain.** Schlomo, who is also learning Python, checks the claim
$(x + 1)^3 = x^3 + 1$ at $x = 0$, and it is true. "So it is an
identity," he says. What
would you say back? Find every whole number from $-5$ to 5 where the
claim is true.

<details class="dl-answer"><summary>answer</summary>

One value that works does not make an identity. An identity must be
true for every value, and one value where it fails is enough to show it
is not one. Schlomo's check needs more values
beside it.

```python
for x in range(-5, 6):
    if (x + 1) ** 3 == x ** 3 + 1:
        print(x)
```

It prints `-1` and `0`. So the claim is an equation with two answers.
Expanding shows why: $(x + 1)^3 = x^3 + 3x^2 + 3x + 1$, and the middle
terms, $3x^2 + 3x = 3x(x + 1)$, are 0 only at $x = 0$ and $x = -1$.

</details>

**17. Another way.** The tutorial found each point of a curve by mixing
its three points with the weights $(1 - t)^2$, $2t(1 - t)$ and $t^2$.
Paul de Casteljau, an engineer at Citroën, found the same points by
mixing twice. Take the point a fraction $t$ of the way along each of the
two grey lines, join those two points with an orange line, and go a
fraction $t$ of the way along that. The cell below does this for the
letter bowl from
[The top of the curve](tutorial:the-top-of-the-curve#a-letter-that-sits-below-the-line),
and draws the curve as $t$ grows. Run it and watch. Then:

1. Move `pull` to `(260, -200)` and run it again. Before you do, guess:
   will the bowl dip about twice as far?
2. Show with algebra that mixing twice gives the same three weights.
   Mixing $p$ and $q$ gives $(1 - t)p + tq$.

```python exec
id: rules-with-practice-casteljau
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

start = (100, 112)
pull = (260, -108)       # move this point, then run the cell again
end = (460, 72)


def mix(p, q, t):
    """Return the point a fraction t of the way from p to q."""
    return ((1 - t) * p[0] + t * q[0], (1 - t) * p[1] + t * q[1])


figure, drawing = plt.subplots(figsize=(4, 2.8))
drawing.plot([start[0], pull[0], end[0]], [start[1], pull[1], end[1]], "o:", color="grey")
drawing.axhline(0, color="black", linewidth=1)
drawing.set_aspect("equal")
arm, = drawing.plot([], [], "o-", color="C1")
curve, = drawing.plot([], [], color="C0", linewidth=2)


def draw_frame(frame):
    t = frame / 20
    first = mix(start, pull, t)
    second = mix(pull, end, t)
    arm.set_data([first[0], second[0]], [first[1], second[1]])
    points = [mix(mix(start, pull, k / 20), mix(pull, end, k / 20), k / 20) for k in range(frame + 1)]
    curve.set_data([point[0] for point in points], [point[1] for point in points])
    drawing.set_title(f"t = {t:.2f}", fontsize=9)


FuncAnimation(figure, draw_frame, frames=21, interval=200)
```

<details class="dl-answer"><summary>answer</summary>

The orange line slides along the two grey lines, and its tip traces the
bowl, dipping below the baseline and rising again. With `pull` at
$(260, -200)$ the lowest height is about $-55$, where it was $-9$: six
times as deep, for a pull that moved less than twice as far. Near the
middle of the curve the pull point has about half the weight, so moving
it 92 units lower moves the bottom about 46 units lower, and the
bottom was only 9 below the line to begin with.

Here is the algebra for the heights. The across numbers work the same way.
Call the three heights $s$, $p$ and $e$. The first mix gives
$(1 - t)s + tp$, and the second gives $(1 - t)p + te$. Mixing those two:

$$(1 - t)\big((1 - t)s + tp\big) + t\big((1 - t)p + te\big)
= (1 - t)^2 s + 2t(1 - t)p + t^2 e$$

The middle point is met twice, once from each side, and that gives the
2 in $2t(1 - t)$. Here is one check in code, at eleven
values of $t$:

```python
for tenths in range(11):
    t = tenths / 10
    twice = mix(mix(start, pull, t), mix(pull, end, t), t)[1]
    weighted = (1 - t) ** 2 * start[1] + 2 * t * (1 - t) * pull[1] + t ** 2 * end[1]
    print(t, round(twice, 6), round(weighted, 6))
```

The two columns agree (a `-0.0` is a float a tiny bit below 0, and rounding
keeps its sign). Many drawing programs find a curve by mixing twice,
because it needs only the one small step, done again.

</details>
