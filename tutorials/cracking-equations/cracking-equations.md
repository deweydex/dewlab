---
title: "Solving equations: linear, quadratic and simultaneous"
year: "2026-2027"
version: 2026.09.26.1
covers:
  solving-linear-equations:
    touches: [MIT-1.7]
  the-quadratic-formula:
    touches: [MIT-1.10]
  factorisation:
    covers: [MIT-1.9]
  solving-inequalities:
    covers: [MIT-1.11]
  simultaneous-equations:
    covers: [MIT-1.12]
worlds:
  music: A band, its gigs and its tickets. The numbers are made up.
  electronics: Bulbs, batteries and the cost of running them.
  rockets: Rockets, launches and when two of them meet. The numbers are made up.
  fantasy-maps: A made-up kingdom, and the routes across it.
---

# Solving equations: linear, quadratic and simultaneous

In [Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
we stored polynomials as lists, and evaluated, added and multiplied
them. In [Functions and their graphs](tutorial:drawing-functions) we
read answers from the places where curves cross. In
[Rearranging formulae: changing the subject](tutorial:rearranging-formulae)
we moved letters around a formula. Now we put these together and
*solve* equations. To solve an equation means to find the values of $x$
that make it true. For example, $3x + 7 = 22$ is true when $x = 5$.

A value of $x$ that makes an equation true is called a *solution* of the
equation. When the equation has the form "polynomial $= 0$", a solution
is a root of the polynomial, as in
[Functions and their graphs](tutorial:drawing-functions): a value of $x$
where it is zero. For example, $x = 1$ is a root of $x^2 - 4x + 3$,
because $1 - 4 + 3 = 0$.

## Solving linear equations

A *linear equation* is an equation where $x$ appears only to the power
1. The rule for solving one is the rule from rearranging. Do the same
thing to both sides, so that they stay equal. Here is
$5x - 4 = 2x + 11$, one step at a time.

1. Subtract $2x$ from both sides, so that $x$ is only on the left:
   $3x - 4 = 11$.
2. Add 4 to both sides: $3x = 15$.
3. Divide both sides by 3: $x = 5$.

This way of working is called *balancing*, because each step keeps the
two sides equal, like the two pans of a balance. The cell checks the
answer by putting $x = 5$ into both sides of the starting equation.

```python exec
id: solving-linear-equations-1
x = 5
print(5 * x - 4, 2 * x + 11)
```

Both sides give 21, so $x = 5$ makes the equation true.

### Your turn, on paper

Can you solve each of these by balancing? Write your steps as comments
in the cell. Then check each answer by putting it into both sides, as
the cell does for the first one.

- $5x - 4 = 2x + 11$ (done above)
- $2(x + 3) = 14$
- $\frac{x}{3} - 2 = 1$
- $7 - 2x = 3x - 8$

```python exec
id: your-turn-on-paper-1
# 2(x + 3) = 14
# ...

x = 5    # change this to your answer for each equation
print(5 * x - 4, 2 * x + 11)
```

```hint
after: 2 unchanged runs
For $2(x + 3) = 14$, what was done to $x$ last? The bracket was
multiplied by 2, so dividing both sides by 2 is a good first step. For
$7 - 2x = 3x - 8$, which side would you like the $x$ terms on, so that
the number in front of $x$ is positive?
```

<details class="dl-answer"><summary>answer</summary>

- $2(x + 3) = 14$: divide by 2, $x + 3 = 7$, so $x = 4$.
- $\frac{x}{3} - 2 = 1$: add 2, $\frac{x}{3} = 3$, then multiply by 3,
  $x = 9$.
- $7 - 2x = 3x - 8$: add $2x$ to both sides, $7 = 5x - 8$. Add 8,
  $15 = 5x$, so $x = 3$.

Check the last one: $7 - 6 = 1$ and $9 - 8 = 1$.

</details>

### Your turn

Any linear equation can be balanced into the form $ax + b = 0$. Then we
subtract $b$ from both sides and divide by $a$:

$$x = -\frac{b}{a} \quad \text{(as long as } a \neq 0 \text{)}$$

Can you write `solve_linear(a, b)`, which returns the solution of
$ax + b = 0$? The numbers go in the order they appear in $ax + b$:
first $a$, then $b$. Every function on this page that takes
coefficients as separate numbers works the same way, starting with the
number in front of the highest power. The lists that `multiply_poly`
uses, later on the page, are the other way round, with the constant
first.

When $a = 0$, there is no $x$ term at all. Then $b = 0$ is either true
for every $x$ (when $b$ is 0) or for none. How will your function say
which?

```python exec
id: your-turn-1
def solve_linear(a, b):
    """The solution of ax + b = 0, or a sentence saying why there is not one."""
    # Your code here.
```

```hint
What should happen before the division, so that it never divides by
zero?
```

```inputs
guess: yes
solve_linear(3, -15)
solve_linear(3, 7)
solve_linear(0, 4)     # 0x + 4 = 0
solve_linear(0, 0)     # 0x + 0 = 0
```

```solution
def solve_linear(a, b):
    """The solution of ax + b = 0, or a sentence saying why there is not one."""
    if a == 0:
        if b == 0:
            return "Every x is a solution."
        return "No x is a solution."
    return -b / a
---
`solve_linear(3, 7)` is about $-2.33$, which is $-\frac{7}{3}$. With
$a = 0$ the equation says $b = 0$, and $x$ has no part in it. So it is
true for every $x$, or for none.
```

## The quadratic formula

A *quadratic equation* has the form $ax^2 + bx + c = 0$, with
$a \neq 0$. It can have up to two solutions. The *quadratic formula*
gives them:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

The sign $\pm$ means "plus or minus". Using $+$ gives one solution, and
using $-$ gives the other.

Here is one worked example. For $x^2 - 4x + 3 = 0$, we have $a = 1$,
$b = -4$ and $c = 3$. Then $b^2 - 4ac = 16 - 12 = 4$, and
$\sqrt{4} = 2$. So

$$x = \frac{4 \pm 2}{2}, \quad\text{which gives } x = 3 \text{ or } x = 1.$$

The part under the square root, $b^2 - 4ac$, is called the
*discriminant*. The discriminant tells us how many real solutions there
are:

| Discriminant | Real roots | Example | $b^2 - 4ac$ |
|---|---|---|---|
| positive | two different roots | $x^2 - 4x + 3 = 0$ | $16 - 12 = 4$ |
| zero | one repeated root | $x^2 - 2x + 1 = 0$ | $4 - 4 = 0$ |
| negative | no real roots | $x^2 + 5 = 0$ | $0 - 20 = -20$ |

Why no real roots when it is negative? No real number squared gives a
negative number, so the square root of a negative number is not a real
number. On a graph, as in
[Functions and their graphs](tutorial:drawing-functions), a negative
discriminant means the curve does not cross the horizontal axis. In
[Complex numbers: roots that are not real](tutorial:complex-roots) we
find roots for these equations after all.

### Your turn

Can you write `solve_quadratic(a, b, c)`? It takes the three numbers in
the order they appear in $ax^2 + bx + c$, and returns the real
solutions as a tuple: two roots, one root, or none.

```python exec
id: your-turn-3
import math

def solve_quadratic(a, b, c):
    """The real roots of ax^2 + bx + c = 0, as a tuple."""
    # Your code here.
```

```hint
Which number decides how many roots there are? Can you find it first,
and keep it under a name?
```

```hint
after: 3 errors
title: the steps, in words
    SET discriminant = b^2 - 4*a*c
    IF discriminant > 0:
        RETURN ((-b + sqrt(discriminant)) / (2*a), (-b - sqrt(discriminant)) / (2*a))
    IF discriminant == 0:
        RETURN (-b / (2*a),)
    RETURN ()
```

```inputs
guess: yes
solve_quadratic(1, -4, 3)     # x^2 - 4x + 3 = 0
solve_quadratic(1, -2, 1)     # x^2 - 2x + 1 = 0
solve_quadratic(1, 0, 5)      # x^2 + 5 = 0
solve_quadratic(1, 0, -9)     # x^2 - 9 = 0
solve_quadratic(2, 3, -2)     # 2x^2 + 3x - 2 = 0
```

```solution
def solve_quadratic(a, b, c):
    """The real roots of ax^2 + bx + c = 0, as a tuple."""
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        root = math.sqrt(discriminant)
        return ((-b + root) / (2 * a), (-b - root) / (2 * a))
    if discriminant == 0:
        return (-b / (2 * a),)
    return ()
---
A tuple of one needs its comma: `(-b / (2 * a),)`. An empty tuple
means there are no real roots.
```

### Checking a root

How can we be sure a root is right? If $x$ is a root of the polynomial,
then evaluating the polynomial at $x$ gives zero. With floats, it may
give a number very close to zero instead.

The cell below uses your `solve_quadratic`, so run it after you have
written that function. It puts each root back into $x^2 - 4x + 3$.
What values do you expect it to print?

```python exec
id: verifying-solutions-1
a, b, c = 1, -4, 3   # x^2 - 4x + 3
roots = solve_quadratic(a, b, c)
print("Roots:", roots)
for root in roots:
    value = a * root ** 2 + b * root + c
    print("  p(" + str(root) + ") =", value)
```

### Your turn

Can you write `verify_roots(a, b, c, roots)`, which substitutes each
root back for you and returns `True` if every one gives zero? A value
like `2.2e-16` is zero, apart from rounding, so compare with a small
tolerance, like 0.0001, and not with an exact zero.

```python exec
id: your-turn-5
def verify_roots(a, b, c, roots):
    """True if every root makes ax^2 + bx + c zero, apart from rounding."""
    # Your code here.
```

```inputs
guess: yes
verify_roots(1, -4, 3, (1, 3))
verify_roots(1, -4, 3, (1, 2))           # 2 is not a root
verify_roots(3, -7, 2, (2, 1 / 3))       # 1/3 is stored as 0.333...
verify_roots(1, 0, 5, ())                # no roots to check
```

```solution
def verify_roots(a, b, c, roots):
    """True if every root makes ax^2 + bx + c zero, apart from rounding."""
    for root in roots:
        value = a * root ** 2 + b * root + c
        if abs(value) > 0.0001:
            return False
    return True
---
For $3x^2 - 7x + 2$, the root $\frac{1}{3}$ gives a value of about
$2.2 \times 10^{-16}$, not exactly 0, so an exact test would reject it.
With no roots to check, the function returns `True`, because none of
them failed.
```

## Factorisation

Suppose we know the roots $r_1$ and $r_2$ of a quadratic
$ax^2 + bx + c$. Then we can write the quadratic in *factorised form*:

$$a(x - r_1)(x - r_2)$$

For example, the roots of $x^2 - 4x + 3$ are 1 and 3, so
$x^2 - 4x + 3 = (x - 1)(x - 3)$. Here $a = 1$, so we do not need to
write it.

To *factorise* a quadratic is to write it in this form. A *binomial* is
a polynomial with two terms, such as $x - 1$. Factorising is the reverse
of expanding brackets. When we expand, we multiply two binomials to get
a quadratic. When we factorise, we split a quadratic into two binomials.

### Your turn

Can you write `factor_quadratic(a, b, c)`, which returns a string
showing the factorised form? Use `solve_quadratic` to find the roots,
and put the leading coefficient $a$ in front when it is not 1. If the
quadratic has no real roots, the function should say so in plain words,
and not guess.

```python exec
id: your-turn-7
def factor_quadratic(a, b, c):
    """The factorised form of ax^2 + bx + c, as a string."""
    # Your code here.
```

```hint
A root of 3 gives the bracket $(x - 3)$, and a root of $-2$ gives
$(x + 2)$. How can your code choose between `-` and `+`?
```

```inputs
factor_quadratic(1, -4, 3)
factor_quadratic(1, -1, -6)     # roots 3 and -2
factor_quadratic(2, -2, -12)    # a is not 1
factor_quadratic(1, -2, 1)      # one repeated root
factor_quadratic(1, 0, 5)       # no real roots
```

```solution
def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        root = math.sqrt(discriminant)
        return ((-b + root) / (2 * a), (-b - root) / (2 * a))
    if discriminant == 0:
        return (-b / (2 * a),)
    return ()


def bracket(root):
    """(x - root), with the sign turned round for a negative root."""
    if root < 0:
        return f"(x + {-root:g})"
    return f"(x - {root:g})"


def factor_quadratic(a, b, c):
    """The factorised form of ax^2 + bx + c, as a string."""
    roots = solve_quadratic(a, b, c)
    if not roots:
        return "It cannot be factorised with real numbers."
    front = "" if a == 1 else f"{a:g}"
    if len(roots) == 1:
        return f"{front}{bracket(roots[0])}^2"
    return front + bracket(roots[0]) + bracket(roots[1])
---
`solve_quadratic` is the one from earlier on the page. `bracket` does
the sign work: a root of $-2$ becomes `(x + 2)`, not `(x - -2)`.
```

### Checking by expanding

We can check a factorisation by multiplying the factors back together.
If we get the original polynomial, the factorisation is right.
`multiply_poly` from
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
is useful again here, and the cell below brings it back.

`multiply_poly` works on lists, as it did on that page, with the
constant first, so that each number sits at the index of its power.
So $x - 1$ is `[-1, 1]` here. What list do you expect the cell to print?

```python exec
id: verification-by-expansion-1
def multiply_poly(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] = result[i + j] + a[i] * b[j]
    return result


factor1 = [-1, 1]     # (x - 1)
factor2 = [-3, 1]     # (x - 3)
print(multiply_poly(factor1, factor2))
```

It prints `[3, -4, 1]`, which is $x^2 - 4x + 3$ with the constant
first. Expanding the factors gives the original polynomial, so the two
forms are the same.

## Solving inequalities

An *inequality* compares two expressions with $>$, $\geq$, $<$ or
$\leq$. A linear inequality like $2x + 3 > 7$ has a whole set of
solutions: every $x$ that makes it true.

We solve it with the same steps as an equation:

$$2x + 3 > 7 \implies 2x > 4 \implies x > 2$$

For example, $x = 3$ works: $2 \times 3 + 3 = 9$, and $9 > 7$.

There is one extra rule, and most people forget it at first. **If we
multiply or divide both sides by a negative number, the inequality
flips.** For example, $-x > 3$ becomes $x < -3$ when we divide by $-1$.
Check with $x = -4$: $-(-4) = 4$, and $4 > 3$ is true.

### Your turn

Can you write `solve_linear_inequality(a, b, c, sign)`? It solves
$ax + b$ [sign] $c$, where the sign is one of `">"`, `">="`, `"<"` or
`"<="`, and returns a string that describes the solutions. What
happens when $a$ is negative? And when $a$ is 0?

```python exec
id: your-turn-9
def solve_linear_inequality(a, b, c, sign):
    """The solutions of ax + b [sign] c, described in a string."""
    # Your code here.
```

```hint
Balance it first: $ax > c - b$. Which step comes next, and when does
that step flip the sign?
```

```inputs
solve_linear_inequality(2, 3, 7, ">")
solve_linear_inequality(-3, 5, 2, "<")     # dividing by -3 flips it
solve_linear_inequality(0, 5, 3, ">")      # 5 > 3, whatever x is
solve_linear_inequality(0, 5, 7, ">")      # 5 > 7 is never true
```

```solution
def solve_linear_inequality(a, b, c, sign):
    """The solutions of ax + b [sign] c, described in a string."""
    if a == 0:
        holds = {">": b > c, ">=": b >= c, "<": b < c, "<=": b <= c}[sign]
        return "Every x is a solution." if holds else "No x is a solution."
    boundary = (c - b) / a
    if a < 0:
        sign = {">": "<", ">=": "<=", "<": ">", "<=": ">="}[sign]
    return f"x {sign} {boundary:g}"
---
The dictionary in the last `if` reverses each sign. With $a = 0$
there is no $x$ left, so the inequality compares $b$ with $c$, and it
is true for every $x$ or for none. $0x + 5 > 3$ is true for every $x$.
```

## Simultaneous equations

Sometimes two things must be true at the same time. Each one is an
equation, and together they are called *simultaneous equations*. They
often come from two straight lines. The place where the lines cross is
the one point that is on both. Here is one from the world you chose.

<div class="dl-world" data-world="music">

A band sells tickets at €12 each. The gig costs €300 to put on, plus €2
for every ticket sold. With $n$ tickets sold,

$$\text{income} = 12n \qquad \text{cost} = 300 + 2n$$

The band *breaks even* where the income and the cost are equal. Below
that number of tickets, it loses money. Above it, it makes money. The
cell draws both lines.

```python exec
id: simultaneous-equations-1--music
import matplotlib.pyplot as plt

tickets = [0, 60]
fig, ax = plt.subplots()
ax.plot(tickets, [12 * n for n in tickets], label="income = 12n")
ax.plot(tickets, [300 + 2 * n for n in tickets], label="cost = 300 + 2n")
ax.set_xlabel("tickets sold")
ax.set_ylabel("euro")
ax.grid(alpha=0.3)
ax.legend()
```

The lines cross at about 30 tickets and €360. To find the point
exactly, call the amount of money $y$. Both lines must give the same
$y$, so we have two equations:

$$12n - y = 0 \qquad 2n - y = -300$$

Subtract the second from the first, and $y$ disappears: $10n = 300$, so
$n = 30$. Then $y = 12 \times 30 = 360$. The band breaks even at 30
tickets, with €360 in and €360 out.

</div>

<div class="dl-world" data-world="electronics">

A halogen bulb costs €2 and uses 35 watts. An LED bulb costs €8 and
uses 5 watts. Electricity costs about €0.35 for a kilowatt-hour, the
energy of 1000 watts for an hour. After $h$ hours of light, the total
cost of each bulb is

$$\text{halogen} = 2 + 0.01225h \qquad \text{LED} = 8 + 0.00175h$$

The LED starts €6 dearer, but it costs less to run. It *breaks even*
where the two costs are equal. After that, it is the cheaper bulb. The
cell draws both lines.

```python exec
id: simultaneous-equations-1--electronics
import matplotlib.pyplot as plt

hours = [0, 1500]
fig, ax = plt.subplots()
ax.plot(hours, [2 + 0.01225 * h for h in hours], label="halogen")
ax.plot(hours, [8 + 0.00175 * h for h in hours], label="LED")
ax.set_xlabel("hours of light")
ax.set_ylabel("total cost (euro)")
ax.grid(alpha=0.3)
ax.legend()
```

The lines cross somewhere near 570 hours and €9. To find the point
exactly, call the cost $y$. Both lines must give the same $y$, so we
have two equations:

$$0.01225h - y = -2 \qquad 0.00175h - y = -8$$

Subtract the second from the first, and $y$ disappears:
$0.0105h = 6$, so $h \approx 571.4$. Then $y = 2 + 0.01225 \times
571.4 = 9$. After about 571 hours, both bulbs have cost €9, and from
then on the LED is cheaper.

</div>

<div class="dl-world" data-world="rockets">

Rocket A is launched and climbs at a steady 50 m/s. Rocket B is
launched 3 seconds later and climbs at 80 m/s. $t$ seconds after the
first launch, their heights are

$$h_A = 50t \qquad h_B = 80(t - 3) = 80t - 240$$

B is faster, so at some moment it catches A. The cell draws both lines
from the moment B is launched.

```python exec
id: simultaneous-equations-1--rockets
import matplotlib.pyplot as plt

times = [3, 12]
fig, ax = plt.subplots()
ax.plot(times, [50 * t for t in times], label="rocket A")
ax.plot(times, [80 * t - 240 for t in times], label="rocket B")
ax.set_xlabel("seconds after A's launch")
ax.set_ylabel("height (m)")
ax.grid(alpha=0.3)
ax.legend()
```

The lines cross at about 8 seconds and 400 m. To find the point
exactly, call the height $h$. Both rockets are at the same $h$ when they
meet, so we have two equations:

$$50t - h = 0 \qquad 80t - h = 240$$

Subtract the first from the second, and $h$ disappears: $30t = 240$, so
$t = 8$. Then $h = 50 \times 8 = 400$. B catches A 8 seconds after the
first launch, 400 m up.

</div>

<div class="dl-world" data-world="fantasy-maps">

To reach a village $d$ km away, a messenger can walk straight across
the moor at 5 km/h. Or they can walk half an hour to the road, and ride
the rest at 20 km/h. The times, in hours, are

$$\text{moor} = 0.2d \qquad \text{road} = 0.5 + 0.05d$$

For a near village, the moor is quicker. For a far one, the road is.
The two routes *break even* where the times are equal. The cell draws
both lines.

```python exec
id: simultaneous-equations-1--fantasy-maps
import matplotlib.pyplot as plt

distances = [0, 8]
fig, ax = plt.subplots()
ax.plot(distances, [0.2 * d for d in distances], label="across the moor")
ax.plot(distances, [0.5 + 0.05 * d for d in distances], label="by the road")
ax.set_xlabel("distance to the village (km)")
ax.set_ylabel("time (hours)")
ax.grid(alpha=0.3)
ax.legend()
```

The lines cross at about 3.3 km and 0.67 hours. To find the point
exactly, call the time $y$. Both routes take the same $y$ there, so we
have two equations:

$$0.2d - y = 0 \qquad 0.05d - y = -0.5$$

Subtract the second from the first, and $y$ disappears: $0.15d = 0.5$,
so $d \approx 3.33$. Then $y = 0.2 \times 3.33 \approx 0.67$ hours,
about 40 minutes. For a village nearer than 3.3 km, cross the moor.
For one further away, take the road.

</div>

The method in each case is called *elimination*. We add or subtract the
equations so that one unknown cancels out, solve for the other, and
then put that value back to find the first. When the numbers in front
of the unknown do not match, we multiply first. For example, with

$$3x + 2y = 12 \qquad x - y = -1$$

multiply the second by 2, to get $2x - 2y = -2$. Adding that to the
first cancels $y$: $5x = 10$, so $x = 2$. Then $2 - y = -1$, so
$y = 3$.

Each equation's graph is a straight line, so there are three things
that can happen. The lines cross once, and there is one solution. The
lines are parallel, and there is none. Or the two equations are the
same line, and every point on it is a solution.

<details class="dl-answer"><summary>where the formula in some textbooks comes from</summary>

Some books give a formula for two equations $a_1 x + b_1 y = c_1$ and
$a_2 x + b_2 y = c_2$. It is elimination, done once with letters.
Multiply the first equation by $b_2$ and the second by $b_1$. Both $y$
terms are now $b_1 b_2 y$, so subtracting removes them:

$$(a_1 b_2 - a_2 b_1) x = c_1 b_2 - c_2 b_1$$

So $x = \dfrac{c_1 b_2 - c_2 b_1}{a_1 b_2 - a_2 b_1}$. The number on
the bottom, $a_1 b_2 - a_2 b_1$, is called the *determinant*. When it
is zero, the two lines have the same slope. They are parallel, or they
are the same line, and there is no single solution.

</details>

### Your turn

Can you write `solve_simultaneous(eq1, eq2)` by elimination? Each
equation is a list `[a, b, c]`, which means $ax + by = c$. The function
returns $x$ and $y$, or says in plain words that there is no single
solution.

```python exec
id: your-turn-11
def solve_simultaneous(eq1, eq2):
    """x and y that make both equations true. Each is [a, b, c] for ax + by = c."""
    # Your code here.
```

```hint
To cancel $y$, what can you multiply each equation by, so that both $y$
terms are the same? Then subtract one from the other.
```

```hint
after: 3 errors
title: the steps, in words
    MULTIPLY eq1 by b2 and eq2 by b1, so both y terms are b1*b2*y
    SUBTRACT: (a1*b2 - a2*b1) x = c1*b2 - c2*b1
    IF a1*b2 - a2*b1 is 0: RETURN "no single solution"
    DIVIDE to find x
    PUT x back into an equation that has a y term, to find y
```

```inputs
solve_simultaneous([1, 1, 10], [2, -1, 5])
solve_simultaneous([3, 2, 12], [1, -1, -1])
solve_simultaneous([2, 4, 10], [1, 2, 5])       # the same line, twice
solve_simultaneous([12, -1, 0], [2, -1, -300])  # the band
solve_simultaneous([50, -1, 0], [80, -1, 240])  # the rockets
solve_simultaneous([0, 1, 3], [1, 1, 5])        # no x in the first
```

```solution
def solve_simultaneous(eq1, eq2):
    """x and y that make both equations true. Each is [a, b, c] for ax + by = c."""
    a1, b1, c1 = eq1
    a2, b2, c2 = eq2
    # Multiplying eq1 by b2 and eq2 by b1 makes the y terms match.
    x_coefficient = a1 * b2 - a2 * b1
    if x_coefficient == 0:
        return "No single solution: the lines are parallel, or the same line."
    x = (c1 * b2 - c2 * b1) / x_coefficient
    if b1 != 0:
        y = (c1 - a1 * x) / b1
    else:
        y = (c2 - a2 * x) / b2
    return x, y
---
The last `if` puts $x$ back into whichever equation has a $y$ in it.
For `[0, 1, 3]`, the first equation is $y = 3$, so $x$ comes from
$x + 3 = 5$. `solve_simultaneous([2, 4, 10], [1, 2, 5])` says there is
no single solution, because the second equation is the first one,
halved.
```

## Looking back

We have found solutions in three ways on this page: by balancing, by a
formula, and by reading where two lines cross. For the break-even point
in your world, the picture came first and the algebra second. What did
the picture tell you that the algebra did not, and what did the algebra
add?

A challenge: can you extend `solve_simultaneous` to three equations in
three unknowns? Eliminate one unknown from two different pairs of
equations, and you are left with two equations in two unknowns, which
your function already solves.

```python challenge
# Three equations, three unknowns: x + y + z = 6, 2x - y + z = 3, x + 2y - z = 2.
equations = [
    [1, 1, 1, 6],
    [2, -1, 1, 3],
    [1, 2, -1, 2],
]
```

Next, [Parabolas: completing the square](tutorial:parabolas) rewrites a
quadratic so that its turning point shows.

## Where to read more

Khan Academy. *Quadratic Formula (Proof).*
<https://www.youtube.com/watch?v=mDmRYfma9C0>. This video shows where the
formula in `solve_quadratic` comes from. It completes the square, step
by step, as the next page does.
