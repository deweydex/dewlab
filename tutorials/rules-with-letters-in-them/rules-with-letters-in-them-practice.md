---
title: "Rules with letters in them: expressions, equations and identities — Practice"
practice_for: rules-with-letters-in-them
year: "2026-2027"
version: 2026.09.24.1
---

# Rules with letters in them: expressions, equations and identities — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `evaluate` from the
tutorial and `close_enough` from
[Does it work?](tutorial:does-it-work#close-enough). The tutorial's
`expand_brackets` was a page cell, not a toolkit tool, so the stretch
section copies it in.

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

`32 64`.

In `2 * x ** 2`, the power comes first: $4^2 = 16$, then $2 \times 16 =
32$. In `(2 * x) ** 2`, the brackets come first: $2 \times 4 = 8$, then
$8^2 = 64$. In maths, $2x^2$ means the first one.

</details>

**2. Explain.** A pancake recipe has 3 eggs for every 4 people, so $y$
people need $\frac{3y}{4}$ eggs. Which of these is an expression, which
an equation with one answer, and which an identity? Say why for each.

- $\frac{3y}{4}$
- $\frac{3y}{4} = 6$
- $\frac{3(y + 4)}{4} = \frac{3y}{4} + 3$

<details class="dl-answer"><summary>answer</summary>

- $\frac{3y}{4}$ is an expression. It has no equals sign. It is a rule
  that gives a number of eggs once $y$ has a value.
- $\frac{3y}{4} = 6$ is an equation with one answer. It asks "how many
  people use 6 eggs?", and it is true only for $y = 8$.
- $\frac{3(y + 4)}{4} = \frac{3y}{4} + 3$ is an identity. Four more
  people always need 3 more eggs, whatever $y$ is. You can check it in
  a loop:

```python
for people in range(0, 21):
    assert close_enough(3 * (people + 4) / 4, 3 * people / 4 + 3)
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

`-9`, `9` and `9`.

In `-3 ** 2`, the power comes before the minus sign, so Python works
out $-(3^2) = -9$. In the second line, the brackets make $-3$ one
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

**5. Make.** A gym charges €30 to join, and then €25 a month. Write the
cost after $m$ months as an expression, then as a list. Use `evaluate`
to find the cost of one year.

<details class="dl-answer"><summary>answer</summary>

The cost is $25m + 30$, which is the list `[30, 25]`.

```python
gym = [30, 25]
print(evaluate(gym, 12))
```

One year costs €330. The constant, the joining fee, comes first in the
list, because it is the $m^0$ term.

</details>

**6. Predict.** What do these two lines print?

```python
print(evaluate([1, 1, 1, 1], 2))
print(evaluate([1, 1, 1, 1], 10))
```

<details class="dl-answer"><summary>answer</summary>

`15` and `1111`.

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

**Think about:** which step is the one most people get wrong? Where
does the check catch it?

</details>

<details class="dl-answer"><summary>answer</summary>

$3(2x + 1) - 2(x - 4) = 6x + 3 - 2x + 8 = 4x + 11$.

```python
for x in range(-10, 11):
    assert 3 * (2 * x + 1) - 2 * (x - 4) == evaluate([11, 4], x)
print("4x + 11 checks out.")
```

A common slip is $-2(x - 4) = -2x - 8$. The check finds it at once:
at $x = 0$ the two sides would be 11 and $-5$.

</details>

**8. Fix.** Here is someone's version of `evaluate`, with two tests.
Run it, see which test fails, and fix the function.

```python exec
id: rules-with-practice-fix-evaluate
def value_of(coefficients, x):
    """Return the value of a polynomial at x. coefficients is lowest power first."""
    value = 0
    for power in range(1, len(coefficients)):
        value = value + coefficients[power] * x ** power
    return value

assert value_of([0, -4, 0, 1], 2) == 0, "x cubed take away 4x, at 2"
assert value_of([-4, 0, 1], 2) == 0, "x squared take away 4, at 2"
print("value_of keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The second test fails: `value_of([-4, 0, 1], 2)` gives 4, not 0. The
loop starts at power 1, so it never adds the constant term, at index 0.
The fix is to start at 0:

```python
def value_of(coefficients, x):
    """Return the value of a polynomial at x. coefficients is lowest power first."""
    value = 0
    for power in range(len(coefficients)):
        value = value + coefficients[power] * x ** power
    return value

assert value_of([0, -4, 0, 1], 2) == 0
assert value_of([-4, 0, 1], 2) == 0
print("value_of keeps its promise.")
```

The first test passed with the bug, because its constant term is 0.
A test on a polynomial with no constant could never find this mistake.

</details>

**9. Make.** A square painting is $x$ cm on each side. Its frame adds
4 cm to the width and 6 cm to the height. Expand $(x + 4)(x + 6)$, the
area of the painting and frame, with a grid of four pieces. Then check
your answer by substitution.

<details class="dl-answer"><summary>answer</summary>

| times | $x$ | $6$ |
|---|---|---|
| $x$ | $x^2$ | $6x$ |
| $4$ | $4x$ | $24$ |

$(x + 4)(x + 6) = x^2 + 10x + 24$, which is the list `[24, 10, 1]`.

```python
for side in range(0, 101):
    assert evaluate([24, 10, 1], side) == (side + 4) * (side + 6)
print("x^2 + 10x + 24 checks out.")
```

For a painting 40 cm wide, the area with the frame is
$1600 + 400 + 24 = 2024$ square centimetres.

</details>

**10. Another way.** Work out $29 \times 31$ in your head. The tutorial's
last "Your turn" expanded $(x - 2)(x + 2)$. Use the same idea with
$(30 - 1)(30 + 1)$, then check with Python.

<details class="dl-answer"><summary>answer</summary>

$(x - 1)(x + 1) = x^2 - 1$, because the two strips, $-x$ and $+x$,
cancel out. With $x = 30$:

$$29 \times 31 = (30 - 1)(30 + 1) = 900 - 1 = 899$$

```python
print(29 * 31, evaluate([-1, 0, 1], 30))
```

Both give 899. The same trick gives $48 \times 52 = 2500 - 4 = 2496$.
Mental arithmetic like this is an identity at work.

</details>

**11. Explain.** The tutorial checked each piece of algebra by
substituting numbers, and said a proof by rules is what algebra is for
in the end. A textbook often starts the other way: it teaches the rules
for brackets and like terms, and practises them by hand, with no
numbers put in. Which way would you have wanted to learn it, and why?
There is no one right answer.

<details class="dl-answer"><summary>answer</summary>

A good answer weighs a few things, and can land on either side.

- **Trust.** A check you run tells you at once whether a step was
  right. A rule you apply tells you only if you applied it well.
- **Certainty.** A proof by rules covers every number. A check covers
  the numbers you tried, unless you know a fact like "two quadratics
  that agree at three values are the same".
- **Speed.** With practice, rules are faster than typing a check,
  and exams usually ask for the rules.
- **Mistakes.** A check shows you where a mistake is. It does not show
  you why it happened. Knowing the rules does.
- **You.** Some people need to see a rule work on numbers before they
  believe it. Others find the numbers slow.

Many people end up wanting both: rules to do the work, and a check to
catch the slips.

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
is the row before, added to itself shifted one place: that is what
multiplying by $x + 1$ does. The numbers are the combinations from
[Orders and choices](tutorial:orders-and-choices): the coefficient of
$x^2$ in $(x + 1)^4$ is `combinations(4, 2)`, which is 6. Each $x^2$
term comes from choosing the $x$ in 2 of the 4 brackets.

```python
for chosen in range(5):
    print(chosen, combinations(4, chosen))
```

</details>

**13. Fix.** This version of `expand_brackets` gives the wrong list for
$(x + 3)(x + 5)$. Find the mistake.

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
assert expand_quickly([3, 1], [5, 1]) == [15, 8, 1]
```

<details class="dl-answer"><summary>answer</summary>

It prints `[15, 5, 1]`, and the test fails. The line inside the loops
puts each product into its place, and so it replaces what was there.
Two pieces land at index 1, $3x$ and $5x$, and only the last one is
kept. Like terms must be added:

```python
            expanded[i + j] = expanded[i + j] + first[i] * second[j]
```

Now it gives `[15, 8, 1]`. The mistake is invisible for a bracket times
a single number, where no two pieces ever land in the same place.

</details>

**14. Another way.** $3x^2 + 5x - 2$ can be written with no powers at
all: $(3x + 5)x - 2$. Start with the highest coefficient. Multiply by
$x$, add the next coefficient, and repeat. Write
`evaluate_nested(coefficients, x)` that works this way, and check it
against `evaluate` for many values of $x$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The list is lowest power first, so go through it backwards, with
   `range(len(coefficients) - 1, -1, -1)`: a range with a step of $-1$.
2. Start `value` at 0. Each time round, multiply `value` by `x`, then
   add the coefficient at that index.
3. Walk through `[-2, 5, 3]` at $x = 2$ by hand: 3, then 11, then 20.

**Think about:** how many multiplications does each way need for a
polynomial of degree 10?

</details>

<details class="dl-answer"><summary>answer</summary>

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
For degree 10 it makes 10 multiplications, where working out every
power separately makes many more. Computers often evaluate polynomials
this way.

</details>

**15. Make.** €1,000 is saved at a rate $r$ a year (0.04 means 4%). After
two years it is $1000(1 + r)^2$. Expand this into a polynomial in $r$
with `expand_brackets`, then multiply every coefficient by 1000. Check
your answer at $r = 0.04$.

<details class="dl-answer"><summary>answer</summary>

```python
squared_bracket = expand_brackets([1, 1], [1, 1])
savings = []
for coefficient in squared_bracket:
    savings.append(1000 * coefficient)
print(savings)

print(evaluate(savings, 0.04), 1000 * 1.04 ** 2)
print(close_enough(evaluate(savings, 0.04), 1000 * 1.04 ** 2))
```

The list is `[1000, 2000, 1000]`: $1000 + 2000r + 1000r^2$. At 4%, both
give €1,081.60 (the float may show a few more digits). The $2000r$ is
the interest of both years on the €1,000. The $1000r^2$ is the
interest earned on the first year's interest: €1.60. That small term is
compound growth, from
[Doubling and halving](tutorial:doubling-and-halving#how-long-to-double).

</details>

**16. Explain.** A friend checks the claim $(x + 1)^3 = x^3 + 1$ at
$x = 0$, and it is true. "So it is an identity," they say. What would
you say back? Find every whole number from $-5$ to 5 where the claim
is true.

<details class="dl-answer"><summary>answer</summary>

One value that works does not make an identity. An identity must be
true for every value, and one value where it fails is enough to show it
is not one.

```python
for x in range(-5, 6):
    if (x + 1) ** 3 == x ** 3 + 1:
        print(x)
```

It prints `-1` and `0`. So the claim is an equation with two answers.
Expanding shows why: $(x + 1)^3 = x^3 + 3x^2 + 3x + 1$, and the middle
terms, $3x^2 + 3x = 3x(x + 1)$, are 0 only at $x = 0$ and $x = -1$.

</details>
