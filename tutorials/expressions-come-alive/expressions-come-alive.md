---
title: "Polynomials: representing and combining them in Python"
year: "2026-2027"
version: 2026.09.26.1
covers:
  expressions-versus-equations:
    covers: [MIT-1.5]
  representing-polynomials:
    covers: [MIT-1.6]
  evaluating-polynomials:
    covers: [MIT-1.6]
  displaying-polynomials:
    covers: [MIT-1.6]
  adding-polynomials:
    covers: [MIT-1.6]
  multiplying-polynomials:
    covers: [MIT-1.8]
  subtracting-and-scaling:
    covers: [MIT-1.6]
worlds:
  rockets: Rockets, launches and the arcs they fly. The numbers are made up.
  electronics: Batteries, resistors and the power between them. The numbers are made up.
---

# Polynomials: representing and combining them in Python

A model rocket is launched from a platform 2 m up, at 15 m/s. Its
height after $t$ seconds is about $2 + 15t - 4.9t^2$ metres. The cell
keeps the three numbers of that formula in a list, and uses them to
find the height each second.

```python exec
id: opening-1
rocket = [2, 15, -4.9]    # 2 + 15t - 4.9t^2, with the constant first

for t in [0, 1, 2, 3]:
    height = rocket[0] + rocket[1] * t + rocket[2] * t ** 2
    print(t, "s:", round(height, 1), "m")
```

```predict
type: choice

Is the rocket higher after 1 second or after 2 seconds?

- After 1 second
  - The $-4.9t^2$ pulls it down, and it grows fast.
- After 2 seconds
- The same height both times
  - A rocket going up and coming down could pass the same height twice.
```

The heights are 2, 12.1, 12.4 and 2.9 m. After 2 seconds the rocket is
a little higher than after 1, and after 3 it is nearly back down. Three
numbers in a list were enough to describe the whole flight.

On this page we store expressions like this one as lists of numbers.
Then we write functions that find their value, add them and multiply
them. The algebra turns into something we can run and test.

## Expressions versus equations

An *expression* is a piece of mathematics that has a value, such as
$3x + 7$, $x^2 - 4$ or $\frac{x+1}{x-1}$. An expression does not claim
anything. It gives a value once we choose a value for $x$. For example,
when $x = 5$, the expression $3x + 7$ has the value 22.

An *equation* is a statement that two expressions are equal, such as
$3x + 7 = 22$ or $x^2 - 4 = 0$. An equation makes a claim, and the claim
can be true or false, depending on $x$. The equation $3x + 7 = 22$ is
true when $x = 5$, and false for every other value of $x$.

| | Expression | Equation |
|---|---|---|
| Example | $3x + 7$ | $3x + 7 = 22$ |
| Has an equals sign? | no | yes |
| What we do with it | *evaluate* it: find its value | *solve* it: find the $x$ that makes it true |

### Three kinds of equals

On paper, $x = x + 1$ is an equation with no solution, because no
number is one more than itself. Here it is in Python.

```python exec
id: three-kinds-of-equals-1
x = 5
x = x + 1
print(x)
```

```predict
type: choice

What will it print?

- 6
- 5
  - $x = x + 1$ can never be true, so Python should leave $x$ alone.
- An error
  - An equation with no solution sounds like something Python should
    refuse.
- False
  - In maths, $x = x + 1$ is a false statement.
```

It prints 6. Python's `=` does not claim that two things are equal. And
`==` asks whether they are:

```python exec
id: three-kinds-of-equals-2
print(3 * x + 7 == 25)
```

That prints `True`, because $3 \times 6 + 7 = 25$. Here are the three
jobs an equals sign can do:

| Written | Where | Means |
|---|---|---|
| `x = x + 1` | Python | Find the value of the right side, then keep it under the name `x`. |
| `3 * x + 7 == 25` | Python | Are these two values equal? The answer is `True` or `False`. |
| $3x + 7 = 25$ | maths | A statement, true for some values of $x$. |

So Python's `=` is an instruction, not a claim. Python's `==` is a
question. The maths $=$ is a claim, and solving an equation means
finding when the claim is true. We solve equations in
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).
On this page we evaluate expressions.

## Representing polynomials

A *polynomial* is an expression made by adding up terms. A *term* is a
number multiplied by a whole-number power of $x$, such as $3x^2$ or
$5x$. The number in front of the power is the term's *coefficient*.

In $3x^2 + 5x - 2$ there are three terms:

| Term | Coefficient | Power of $x$ |
|---|---|---|
| $3x^2$ | 3 | $x^2$ |
| $5x$ | 5 | $x^1$ |
| $-2$ | $-2$ | $x^0$ |

The last term, $-2$, has no $x$ in it. It is called the *constant term*.
We can still think of it as $-2 \times x^0$, because $x^0 = 1$ (you saw
this in [Number types, powers and logarithms](tutorial:numbers-and-their-families)).

The *degree* of a polynomial is the highest power of $x$ in it. So
$3x^2 + 5x - 2$ has degree 2. Some degrees have their own names: degree
0 is a constant, degree 1 is *linear*, degree 2 is *quadratic*, and
degree 3 is *cubic*.

So a polynomial is a list of coefficients, one for each power of $x$.
We can store it as a Python list. We will use this rule: the item at
index $i$ is the coefficient of $x^i$. So:

$$3x^2 + 5x - 2 \quad\leftrightarrow\quad [-2, 5, 3]$$

- The constant term, $-2$ (the coefficient of $x^0$), is at index 0.
- The coefficient of $x^1$, which is 5, is at index 1.
- The coefficient of $x^2$, which is 3, is at index 2.

This rule is easy to remember, because the index matches the exponent.
It does mean the list is in the opposite order to the way we usually
write the polynomial. The rocket's list in the opening cell used the
same rule. Look at the cubic in the cell below before you run it. Can
you see why its list has a 0 in it?

```python exec
id: representing-polynomials-1
constant_5 = [5]              # just the number 5
linear = [3, 2]               # 2x + 3
quadratic = [-2, 5, 3]        # 3x^2 + 5x - 2
cubic = [1, 0, -3, 2]         # 2x^3 - 3x^2 + 1

print("Constant:", constant_5)
print("Linear:", linear)
print("Quadratic:", quadratic)
print("Cubic:", cubic)
```

The cubic $2x^3 - 3x^2 + 1$ has no $x$ term. Its coefficient of $x^1$ is
0, and the list must still keep a place for it.

## Evaluating polynomials

To *evaluate* a polynomial means to find its value for one chosen value
of $x$. For $3x^2 + 5x - 2$ at $x = 4$:

$$3(16) + 5(4) - 2 = 48 + 20 - 2 = 66$$

With our list, the steps are: for each index $i$, multiply the
coefficient by $x^i$, and then add up all the results. In sigma
notation, which you met in
[Repeating steps with loops](tutorial:repeating-yourself), that is:

$$p(x) = \sum_{i=0}^{n} c_i \cdot x^i$$

Here $c_i$ is the coefficient at index $i$, and $n$ is the degree. A sum
like this turns straight into a loop.

### Your turn

Can you write a function `evaluate_poly(coeffs, x)`? It takes a list of
coefficients and a value of $x$, and returns the polynomial's value at
that $x$. The opening cell did the same job for one list of three
numbers. Yours should work for a list of any length.

<div class="dl-world" data-world="rockets">

Test it on the rocket, and on $3x^2 + 5x - 2$.

```python exec
id: your-turn-1--rockets
rocket = [2, 15, -4.9]


def evaluate_poly(coeffs, x):
    """The value at x of the polynomial whose coefficients are in coeffs."""
    # Your code here.
```

```hint
What did the opening cell do with `rocket[0]`, `rocket[1]` and
`rocket[2]`? How could a loop do the same for every index?
```

```inputs
guess: yes
evaluate_poly(rocket, 0)
evaluate_poly(rocket, 2)
evaluate_poly([-2, 5, 3], 4)
evaluate_poly([-2, 5, 3], 0)    # only the constant term is left
evaluate_poly([1], 999)         # a constant polynomial
```

```solution
def evaluate_poly(coeffs, x):
    """The value at x of the polynomial whose coefficients are in coeffs."""
    total = 0
    for i, c in enumerate(coeffs):
        total = total + c * x ** i
    return total
---
`evaluate_poly(rocket, 2)` prints `12.399999999999999`, which is 12.4
with a rounding error. At $x = 0$ every term but the constant is 0, so
a polynomial at 0 is always its constant term. That makes an easy test.
```

</div>

<div class="dl-world" data-world="electronics">

A power supply gives 12 volts, but it has a resistance of 2 ohms
inside it. When a current of $I$ amps flows, the power it delivers, in
watts, is $12I - 2I^2$. Test your function on that, and on
$3x^2 + 5x - 2$.

```python exec
id: your-turn-1--electronics
supply = [0, 12, -2]    # 12I - 2I^2


def evaluate_poly(coeffs, x):
    """The value at x of the polynomial whose coefficients are in coeffs."""
    # Your code here.
```

```hint
Why is the first number in `supply` a 0? Which power of $I$ does each
number go with?
```

```inputs
guess: yes
evaluate_poly(supply, 1)
evaluate_poly(supply, 3)
evaluate_poly(supply, 6)
evaluate_poly([-2, 5, 3], 4)
evaluate_poly([1], 999)         # a constant polynomial
```

```solution
def evaluate_poly(coeffs, x):
    """The value at x of the polynomial whose coefficients are in coeffs."""
    total = 0
    for i, c in enumerate(coeffs):
        total = total + c * x ** i
    return total
---
The supply delivers 10 W at 1 A and 18 W at 3 A, but 0 W at 6 A. At
6 A all 12 volts are used up inside the supply, and nothing is left for
whatever it powers.
[Parabolas: completing the square](tutorial:parabolas) finds the best
current.
```

</div>

## Displaying polynomials

A list like `[-2, 5, 3]` is good for computing, but it is hard for a
person to read. Can we write a function that turns it into a string like
`"3x^2 + 5x - 2"`?

This is trickier than it looks. Here are the cases to handle:

- A coefficient of zero: skip that term.
- The constant term: it has no "x" part.
- The $x^1$ term: show it as "x", not "x^1".
- A coefficient of 1 or −1: show "x^2", not "1x^2".
- Plus and minus signs: the first term should not start with "+".

### Your turn

How might you write a function `poly_to_string(coeffs)` that returns a
readable string? Start with a simple version that works for basic cases,
such as `[-2, 5, 3]`. Then improve it, one case from the list above at a
time. Many special cases make formatting tricky, so expect to improve
your function more than once.

```python exec
id: your-turn-3
def poly_to_string(coeffs):
    """A readable form of a polynomial, highest power first."""
    # Your code here.
```

```hint
Which power should come first in the string? Can you make a loop over
the indexes, from the highest down to 0?
```

```inputs
poly_to_string([-2, 5, 3])
poly_to_string([0, 0, 1])       # x^2
poly_to_string([7])
poly_to_string([0, 1])          # x
poly_to_string([1, 0, -3, 2])   # a zero in the middle
poly_to_string([0, -1])         # a first term with a minus sign
```

```solution
def poly_to_string(coeffs):
    """A readable form of a polynomial, highest power first."""
    parts = []
    for power in range(len(coeffs) - 1, -1, -1):
        c = coeffs[power]
        if c == 0:
            continue
        if power == 0:
            piece = str(abs(c))
        else:
            variable = "x" if power == 1 else f"x^{power}"
            piece = variable if abs(c) == 1 else f"{abs(c)}{variable}"
        sign = "-" if c < 0 else "+"
        parts.append((sign, piece))
    if not parts:
        return "0"
    first_sign, first = parts[0]
    text = ("-" if first_sign == "-" else "") + first
    for sign, piece in parts[1:]:
        text = text + f" {sign} {piece}"
    return text
---
Each term is kept as a sign and a piece, so the first term can be
treated differently from the rest. A list of all zeros prints as `0`.
```

## Adding polynomials

To add two polynomials, we add the coefficients of the same power of
$x$:

$$(3x^2 + 5x - 2) + (x^2 - 3x + 7) = 4x^2 + 2x + 5$$

In list form, we add the items at the same index:
`[-2, 5, 3]` and `[7, -3, 1]` give `[5, 2, 4]`.

Sometimes the two polynomials have different degrees, so their lists
have different lengths. In that case, we treat the shorter list as if it
had zeros in the missing places. For example, $2x + 3$ is `[3, 2]`, and
we treat it as `[3, 2, 0]`.

### Your turn

Can you write a function `add_poly(a, b)`? It should return a new list
for the sum, and it should work when the lists have different lengths.

```python exec
id: your-turn-5
def add_poly(a, b):
    """The sum of two polynomials, as a new coefficient list."""
    # Your code here.
```

```hint
How long should the answer be? What should you add at an index that
one of the lists does not reach?
```

```inputs
guess: yes
add_poly([-2, 5, 3], [7, -3, 1])
add_poly([3, 2], [-2, 5, 3])    # different lengths
add_poly([1, 1], [-1, -1])      # everything cancels
```

```solution
def add_poly(a, b):
    """The sum of two polynomials, as a new coefficient list."""
    length = max(len(a), len(b))
    result = []
    for i in range(length):
        left = a[i] if i < len(a) else 0
        right = b[i] if i < len(b) else 0
        result.append(left + right)
    return result
---
A missing coefficient counts as 0, because a polynomial of lower degree
has zero coefficients for the higher powers. `add_poly([1, 1], [-1, -1])`
returns `[0, 0]`, which is the polynomial 0.
```

## Multiplying polynomials

It takes more steps to multiply polynomials. To multiply $(2x + 3)(x + 4)$,
we multiply each term of the first polynomial by every term of the
second, and then add the results. This is called *expanding the
brackets*. For two terms times two terms, many people use the *FOIL
method*: multiply the First terms, then the Outer, then the Inner, then
the Last.

$$(2x + 3)(x + 4) = 2x^2 + 8x + 3x + 12 = 2x^2 + 11x + 12$$

### Your turn, on paper

Before any code, can you expand these two by hand? Write your answers
as comments in the cell, highest power first. The code later on the page
will check them.

- $(x + 3)(x - 2)$
- $(2x - 1)^2$, which is $(2x - 1)(2x - 1)$

```python exec
id: your-turn-on-paper-1
# (x + 3)(x - 2) =
# (2x - 1)^2 =
```

```hint
after: 2 unchanged runs
Every term in the first bracket meets every term in the second. For
$(x + 3)(x - 2)$ that is four products: $x \times x$, $x \times (-2)$,
$3 \times x$ and $3 \times (-2)$. Which two of them have an $x$ in them
and nothing more?
```

<details class="dl-answer"><summary>answer</summary>

$(x + 3)(x - 2) = x^2 - 2x + 3x - 6 = x^2 + x - 6$.

$(2x - 1)^2 = 4x^2 - 2x - 2x + 1 = 4x^2 - 4x + 1$.

</details>

### Turning expanding into code

Here is the idea that turns expanding into code. When we multiply a
term $a_i x^i$ by a term $b_j x^j$, we get $a_i \cdot b_j \cdot x^{i+j}$.
The coefficients multiply and the powers add. For example,
$2x \times 4 = 2x^1 \times 4x^0 = 8x^1$.

So in the answer, the coefficient of $x^k$ is the sum of all the
products $a_i \cdot b_j$ where $i + j = k$.

Can you write a function `multiply_poly(a, b)` that returns a new list
for the product? Then check your two answers from paper with it.

```python exec
id: your-turn-7
def multiply_poly(a, b):
    """The product of two polynomials, as a new coefficient list."""
    # Your code here.
```

```hint
How long is the answer? Multiplying a degree 1 polynomial by a degree 1
polynomial gives degree 2. How many coefficients does a degree 2
polynomial have?
```

```hint
after: 3 errors
title: the steps, in words
    SET result_length = length(a) + length(b) - 1
    CREATE a result list of that length, filled with zeros
    FOR each index i in a:
        FOR each index j in b:
            ADD a[i] * b[j] to result[i + j]
    RETURN result
```

```inputs
guess: yes
multiply_poly([3, 2], [4, 1])      # (2x + 3)(x + 4)
multiply_poly([3, 1], [-2, 1])     # (x + 3)(x - 2)
multiply_poly([-1, 2], [-1, 2])    # (2x - 1)^2
multiply_poly([1, 1], [1, 1])      # (x + 1)^2
```

```solution
def multiply_poly(a, b):
    """The product of two polynomials, as a new coefficient list."""
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] = result[i + j] + a[i] * b[j]
    return result
---
The line `result[i + j] = ...` is where the powers add. The list
representation was chosen so that index $i$ times index $j$ lands at
index $i + j$.
```

### Squaring a sum

Here is a quick question about squaring, with a cell that tests it for
four values of $x$. The middle column is $(x + 3)^2$ and the last is
$x^2 + 9$.

```python exec
id: squaring-a-sum-1
for x in [0, 1, 2, 10]:
    print(x, (x + 3) ** 2, x ** 2 + 9)
```

```predict
type: choice

Before you run it: when are $(x + 3)^2$ and $x^2 + 9$ equal?

- For every $x$
  - Squaring each part of the sum looks like the way to square the
    whole sum.
- For one value of $x$ only
- Never
  - The brackets change the order of the work, so the answers should
    always differ.
```

The two columns agree only at $x = 0$. Expand the bracket and you can
see why: $(x + 3)^2 = x^2 + 6x + 9$. The $6x$ is missing from $x^2 + 9$,
and $6x$ is zero only when $x$ is zero. In general,
$(a + b)^2 = a^2 + 2ab + b^2$, and the $2ab$ in the middle is easy to
forget.

## Checking by evaluating

How can we be sure that `multiply_poly` is right? Here is one way. If
$(2x + 3)(x + 4) = 2x^2 + 11x + 12$, then both sides must give the same
value for every $x$. So we can pick a value, such as $x = 5$, and
evaluate both sides.

This cell uses your `evaluate_poly` and `multiply_poly`, so run it after
you have written both. Do you expect the last line to say `True`? Run it
to check.

```python exec
id: a-verification-trick-1
a = [3, 2]     # 2x + 3
b = [4, 1]     # x + 4
product = multiply_poly(a, b)

x = 5
left_side = evaluate_poly(a, x) * evaluate_poly(b, x)
right_side = evaluate_poly(product, x)
print("(2*5+3) * (5+4) =", left_side)
print("2*25 + 11*5 + 12 =", right_side)
print("Match:", left_side == right_side)
```

Both sides give 117.

Look at the two kinds of equation on this page. $3x + 7 = 22$ is true
for one value of $x$. $(2x + 3)(x + 4) = 2x^2 + 11x + 12$ is true for
every value of $x$. An equation that is true for every value of $x$ is
called an *identity*. Every correct expansion is an identity, and
$(x + 3)^2 = x^2 + 9$ is not one.

So we can test an expansion by evaluating both sides at several values
of $x$. If a product of two polynomials of degree 1 agrees with your
expansion at three values of $x$, the expansion is right. In general,
two polynomials of degree at most $n$ that agree at $n + 1$ values of
$x$ are the same polynomial.

### Your turn

Can you write a function `test_multiply(a, b)` that does this check for
you? It evaluates both sides at $x$ = 0, 1, 2, −1 and 10, prints both
sides for each $x$, and returns `True` if they agree every time.

```python exec
id: your-turn-9
def test_multiply(a, b):
    """Check multiply_poly(a, b) by evaluating both sides at five values of x."""
    # Your code here.
```

```hint
Which two functions does the cell above use? What does it compare?
```

```inputs
test_multiply([3, 2], [4, 1])
test_multiply([1, 1], [1, 1])
test_multiply([-1, 2], [-1, 2])
```

```solution
def evaluate_poly(coeffs, x):
    total = 0
    for i, c in enumerate(coeffs):
        total = total + c * x ** i
    return total


def multiply_poly(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] = result[i + j] + a[i] * b[j]
    return result


def test_multiply(a, b):
    """Check multiply_poly(a, b) by evaluating both sides at five values of x."""
    product = multiply_poly(a, b)
    agree = True
    for x in [0, 1, 2, -1, 10]:
        left = evaluate_poly(a, x) * evaluate_poly(b, x)
        right = evaluate_poly(product, x)
        print(x, left, right)
        if left != right:
            agree = False
    return agree
---
The first two functions are the ones from earlier on the page. Only
`test_multiply` is new. If you break `multiply_poly` on purpose, for
example by writing `result[i]` in place of `result[i + j]`, does
`test_multiply` catch it?
```

## Expanding in your world

<div class="dl-world" data-world="rockets">

The rocket's upward speed after $t$ seconds is $15 - 9.8t$ m/s. The
energy of its movement depends on the square of its speed,
$(15 - 9.8t)^2$. Can you expand that square by hand, and write the
answer as a list? Then check it by evaluating both at a few times.

```python exec
id: expanding-in-your-world-1--rockets
speed = [15, -9.8]    # 15 - 9.8t
```

```hint
$(15 - 9.8t)^2$ is $(15 - 9.8t)(15 - 9.8t)$. Squaring a sum gives three
terms, not two. What is the middle one?
```

```inputs
squared
```

```solution
squared = [15 * 15, 2 * 15 * -9.8, 9.8 * 9.8]
print(squared)
for t in [0, 1, 2]:
    by_list = squared[0] + squared[1] * t + squared[2] * t ** 2
    print(t, (15 - 9.8 * t) ** 2, by_list)
---
$(15 - 9.8t)^2 = 225 - 294t + 96.04t^2$. The middle term is
$2 \times 15 \times (-9.8) = -294$. The list prints `96.04000000000002`
for the last coefficient, which is a rounding error. The two columns
agree at every $t$, apart from rounding. The speed is zero at about
1.53 s, the top of the flight, so the square is smallest there.
```

</div>

<div class="dl-world" data-world="electronics">

Where does $12I - 2I^2$ come from? The 2 ohms inside the supply use up
$2I$ volts, so the voltage left for the circuit is $12 - 2I$. Power is
voltage times current, so the power is $(12 - 2I) \times I$. Can you
expand that by hand, and write it as a list? Is it the same as
`supply`?

```python exec
id: expanding-in-your-world-1--electronics
supply = [0, 12, -2]
```

```hint
$I$ on its own is the list `[0, 1]`. What does multiplying by it do to
each power in $12 - 2I$?
```

```inputs
expanded
expanded == supply
```

```solution
expanded = [0, 12, -2]
for current in [1, 3, 6]:
    by_list = expanded[1] * current + expanded[2] * current ** 2
    print(current, (12 - 2 * current) * current, by_list)
---
$(12 - 2I) \times I = 12I - 2I^2$, which is `[0, 12, -2]`, the same as
`supply`. Multiplying by $I$ moves every coefficient up one power, so a
0 appears at the front for the missing constant term.
```

</div>

## Subtracting and scaling

Two more operations finish our set. One subtracts two polynomials. The
other is *scaling*, which multiplies every coefficient by the same
number. For example, $2 \times (3x^2 + 5x - 2) = 6x^2 + 10x - 4$, so
`[-2, 5, 3]` scaled by 2 gives `[-4, 10, 6]`.

### Your turn

Can you write `scale_poly(coeffs, scalar)` and `subtract_poly(a, b)`?
Subtracting $b$ is the same as adding $b$ scaled by $-1$. Could
`subtract_poly` use the other two functions?

```python exec
id: your-turn-11
def scale_poly(coeffs, scalar):
    """Every coefficient multiplied by scalar, as a new list."""
    # Your code here.


def subtract_poly(a, b):
    """a minus b, as a new coefficient list."""
    # Your code here.
```

```inputs
guess: yes
scale_poly([-2, 5, 3], 2)
subtract_poly([-2, 5, 3], [7, -3, 1])
subtract_poly([3, 2], [3, 2])      # a polynomial minus itself
```

```solution
def add_poly(a, b):
    length = max(len(a), len(b))
    result = []
    for i in range(length):
        left = a[i] if i < len(a) else 0
        right = b[i] if i < len(b) else 0
        result.append(left + right)
    return result


def scale_poly(coeffs, scalar):
    """Every coefficient multiplied by scalar, as a new list."""
    return [scalar * c for c in coeffs]


def subtract_poly(a, b):
    """a minus b, as a new coefficient list."""
    return add_poly(a, scale_poly(b, -1))
---
`add_poly` is the one from earlier on the page. `subtract_poly` is one
line, because adding and scaling already do the work.
```

## Looking back

We chose to store a polynomial as a list, with index $i$ holding the
coefficient of $x^i$. Which of the functions on this page would have
been harder to write if the list had been in the other order, highest
power first? Why?

A challenge: the *derivative* of a polynomial follows a short rule.
Each term $c x^i$ becomes $i c x^{i-1}$. So $3x^2 + 5x - 2$ becomes
$6x + 5$. Can you write `poly_derivative(coeffs)`? You will meet what
the derivative means in
[Derivatives: the rate of change of a curve](tutorial:rates-of-change).

```python challenge
# The derivative of a polynomial: each c * x^i becomes i * c * x^(i - 1).
def poly_derivative(coeffs):
    ...


print(poly_derivative([-2, 5, 3]))    # 6x + 5 is [5, 6]
```

## Where to read more

Khan Academy. *Adding and Subtracting Polynomials.*
<https://www.youtube.com/watch?v=ZGl2ExHwdak>. It shows the same
coefficient-by-coefficient operation this page builds as `add_poly`,
worked by hand.

Khan Academy. *Multiplying Polynomials Example.*
<https://www.youtube.com/watch?v=yJzLYa-_Y1k>. It shows the FOIL method,
which this page turns into a loop inside a loop.

Stand-up Maths (2023). *Beware the Runge Spikes!*
<https://www.youtube.com/watch?v=F_43oTnTXiw>. Draw a polynomial through a
few points and it behaves. Add more points and it can swing wildly between
them. Matt Parker shows why. The video is about seventeen minutes long.
