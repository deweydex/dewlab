---
title: "Number types, powers and logarithms"
year: "2026-2027"
version: 2026.09.24.1
covers:
  the-number-domains:
    covers: [MIT-2.1]
  powers-and-their-rules:
    covers: [MIT-1.1]
  logarithms-the-inverse-of-powers:
    covers: [MIT-1.1]
  practical-geometry-formulas-as-functions:
    covers: [MIT-1.2, MIT-1.3]
---

# Number types, powers and logarithms

This page starts a group of pages about algebra and functions. In this
group we take the classic tools of algebra, such as powers, formulas and
equations, and build each one as a program.

We start with the raw material: numbers themselves. Mathematicians sort
numbers into families. When we know which family a number belongs to, we
know which operations are safe to use on it, and what kind of answer to
expect.

On this page we:

- look again at the four number families, and write a function that
  sorts a number into them
- learn the rules for powers, and write our own `power()` function
- meet logarithms, which undo powers
- turn geometry formulas into Python functions

## The number domains

You met the four number families in
[Making decisions with if, elif and else](tutorial:making-decisions).
Here they are again. Each family contains the one before it and adds
something new.

**N** (natural numbers): 0, 1, 2, 3, ... These are the counting numbers.
If you add two natural numbers, the answer is always a natural number.
Subtraction does not always work: $3 - 5 = -2$, and $-2$ is not a
natural number. (Some books start the natural numbers at 1. In this
course, 0 counts as a natural number.)

**Z** (integers): ..., −2, −1, 0, 1, 2, ... Now subtraction always works.
The letter Z comes from *Zahlen*, the German word for numbers.

**Q** (rationals): a rational number is any number we can write as
$\frac{p}{q}$, where $p$ and $q$ are integers and $q \neq 0$. For
example, $0.25 = \frac{1}{4}$. Now division works too, with one
exception: we still cannot divide by zero.

**R** (reals): the real numbers are all the points on the number line.
They include *irrational* numbers. An irrational number is a real number
that we cannot write as a fraction of two integers, such as $\sqrt{2}$
and $\pi$. The irrationals fill in the gaps between the rationals.

Here is a word for what we have been describing. A family is *closed*
under an operation when that operation, used on two numbers from the
family, always gives an answer in the same family. So N is closed under
addition but not under subtraction, and Z is closed under subtraction.

| Family | Addition | Subtraction | Division (not by zero) |
|---|---|---|---|
| N | always works | not always | not always |
| Z | always works | always works | not always |
| Q | always works | always works | always works |
| R | always works | always works | always works |

Every natural number is an integer. Every integer is a rational number:
we can put it over 1, so $7 = \frac{7}{1}$. Every rational number is a
real number. The families sit one inside the next, like Russian dolls:
$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$.
The symbol $\subset$ means "is inside" (you met it as "is a subset of"
in [Sets: building them from sorted lists](tutorial:sets-as-sorted-lists)).

![Four rings, one inside the next. Naturals 0, 1, 2, 3 innermost; then
integers with −5 and −1; then rationals with 2/3 and 0.25; then reals with
root 2, pi and −1.5 outermost.](number-domains.svg)

In the picture, each number sits in the ring of the smallest family it
belongs to. To find all the families a number is in, find the number and
read outwards. For example, $-5$ is in the integers ring. So it is an
integer, a rational and a real. It is not a natural number, because it
is outside that ring.

### Your turn

How might you write a function `classify_number(n)`? It should take a
number and return a list of all the families it belongs to.

Here are some questions to think about first.

- How can you check whether a float is a whole number? The test
  `value == int(value)` works for most cases.
- How can you check whether a number is rational? A computer cannot
  store an irrational number exactly, so every number Python stores is
  rational. If we pass in something like `math.sqrt(2)`, we could still
  choose to call it "R" only.

To keep things manageable, we will use this rule. If a number has no
decimal part, it is an integer, and it may also be natural. If it has a
decimal part, it is rational, and so also real. We will not try to
detect irrational numbers.

**Pseudocode:**
```
IF the number equals its integer version:
    IF the number >= 0:
        RETURN ["N", "Z", "Q", "R"]
    ELSE:
        RETURN ["Z", "Q", "R"]
ELSE:
    RETURN ["Q", "R"]
```

1. Write `classify_number` in the first cell.
2. Test it in the second cell with 7, −3, 0, 0.5, −2.5 and 3.14159.

```python exec
id: your-turn-1
# Your classify_number function
```

```python exec
id: your-turn-2
# Test with: 7, -3, 0, 0.5, -2.5, 3.14159
```

## Powers and their rules

A power is a short way to write repeated multiplication. $a^n$ means
$n$ copies of $a$ multiplied together. The small raised number $n$ is
called the *exponent*, and $a$ is called the *base*. For example,
$2^3 = 2 \times 2 \times 2 = 8$.

Powers follow a few rules. They are worth knowing well, because we use
them all the time in algebra.

| Rule | In words | Example |
|---|---|---|
| $a^m \times a^n = a^{m+n}$ | Multiplying powers of the same base: add the exponents. | $2^2 \times 2^3 = 2^5 = 32$ |
| $(a^m)^n = a^{m \times n}$ | A power of a power: multiply the exponents. | $(2^2)^3 = 2^6 = 64$ |
| $a^0 = 1$ for any $a \neq 0$ | Any base (except 0) to the power 0 is 1. | $5^0 = 1$ |
| $a^{-n} = \frac{1}{a^n}$ | A negative exponent means one over the positive power (the *reciprocal*). | $2^{-3} = \frac{1}{8}$ |
| $a^1 = a$ | Any number to the power 1 is itself. | $7^1 = 7$ |

We can test these rules with Python. The cell below uses $a = 3$. On each
line, it prints the left side of a rule and then the right side. If a
rule is true, what should you see on each line? Run it to check.

```python exec
id: powers-and-their-rules-1
# Verifying the rules of powers
a = 3

print("a^2 * a^3 =", a**2 * a**3, "  a^5 =", a**5)
print("(a^2)^3  =", (a**2)**3, "  a^6 =", a**6)
print("a^0      =", a**0)
print("a^(-2)   =", a**(-2), "  1/a^2 =", 1/a**2)
```

The two numbers on each line match: 243 and 243, then 729 and 729. Also
$3^0$ is 1, and $3^{-2}$ and $\frac{1}{3^2}$ are both $0.111\ldots$

A note on names: the syllabus, and any exam paper you sit, calls powers
*indices*, and calls the rules above the *laws of indices*. Indices and
powers are the same thing, so it is good to recognise the word. This
course says *power* and *exponent*, because the word *index* already
means something else here: the position of an item in a list.

### Your turn

Can we build `power(base, exponent)` ourselves, without Python's `**`
operator? There are three cases to think about:

- A positive exponent means multiplying by the base again and again.
- An exponent of zero gives 1.
- A negative exponent gives one over the positive power.

**Pseudocode:**
```
IF exponent is 0:
    RETURN 1
IF exponent is negative:
    RETURN 1 / power(base, -exponent)
SET result = 1
FOR i from 1 to exponent:
    MULTIPLY result by base
RETURN result
```

1. Write `power` in the first cell.
2. In the second cell, compare your function with Python's `**`
   operator. The comments list three results to check.

```python exec
id: your-turn-3
# Your power function
```

```python exec
id: your-turn-4
# Test: compare your function to Python's ** operator
# power(2, 10) should be 1024
# power(3, 0) should be 1
# power(2, -3) should be 0.125
```

## Logarithms: the inverse of powers

A *logarithm* is a power read backwards. It answers the question: "what
power of $a$ gives $x$?"

$$\text{If } a^n = x, \text{ then } \log_a(x) = n.$$

Here $a$ is the base again. For example, $2^{10} = 1024$, so
$\log_2(1024) = 10$. In words: we need ten 2s multiplied together to
make 1024.

Logarithms matter a lot in computing. In
[Searching a list: linear and binary search](tutorial:finding-things)
we saw that binary search needs about $\log_2(n)$ steps to search $n$
items. That count is a logarithm: it is how many times we can halve $n$
before we reach 1.

Python's `math` module has logarithm functions. `math.log2(x)` gives the
base-2 logarithm, and `math.log10(x)` gives the base-10 logarithm. What
do you think the first two lines print? Run the cell to check.

```python exec
id: logarithms-the-inverse-of-powers-1
import math

print("log2(1024) =", math.log2(1024))
print("log10(1000) =", math.log10(1000))
print("log2(1000000) =", round(math.log2(1000000), 2), "(binary search steps for 1M items)")
```

The first two give 10.0 and 3.0, because $2^{10} = 1024$ and
$10^3 = 1000$. The third gives 19.93: binary search on a million items
needs about 20 steps.

### Your turn

What happens if you take a number and keep dividing it by the base?
Count how many divisions you can do while the result stays at 1 or
more. That count is the whole-number part of $\log_{base}(x)$. For
example, $1024 \div 2$ ten times gives exactly 1, and one more division
would drop below 1, so the count is 10.

The whole-number part is all we need when we count the steps an
algorithm takes. So this idea is enough to build `log_base(x, base)`.

1. Write `log_base` in the first cell.
2. Test it in the second cell with the three examples in the comments.

```python exec
id: your-turn-5
# Your log_base function
```

```python exec
id: your-turn-6
# Test: log_base(1024, 2) should be 10
#        log_base(1000, 10) should be 3
#        log_base(100, 3) should be 4 (3^4 = 81, 3^5 = 243)
```

## Practical geometry: formulas as functions

A formula for area, perimeter, volume or surface area is a function. It
takes measurements as input and returns a value. For example, the area
of a circle takes a radius $r$ and returns $\pi r^2$. For $r = 5$ that
is $\pi \times 25$, about 78.54. Let's build a small geometry toolkit.

The arithmetic here is the easy part. The more useful habit is writing
clean functions: parameter names that say what they mean, and a
docstring that says what goes in and what comes back. That habit turns a
formula you typed once into a tool you can still use months later.

### Your turn

Here are nine functions to write, in five groups. Give each one a
docstring.

1. `circle_area(radius)` and `circle_circumference(radius)`
2. `rectangle_area(length, width)` and `rectangle_perimeter(length, width)`
3. `triangle_area(base, height)`
4. `cylinder_volume(radius, height)` and `cylinder_surface_area(radius, height)`
5. `sphere_volume(radius)` and `sphere_surface_area(radius)`

Use `math.pi` for $\pi$. Here are the formulas you need:

| Shape | Formula |
|---|---|
| Circle | area $\pi r^2$, circumference $2\pi r$ |
| Rectangle | area $l \times w$, perimeter $2(l + w)$ |
| Triangle | area $\frac{1}{2} \times b \times h$ |
| Cylinder | volume $\pi r^2 h$, surface area $2\pi r^2 + 2\pi r h$ |
| Sphere | volume $\frac{4}{3}\pi r^3$, surface area $4\pi r^2$ |

Write your functions in the first cell. Then test each one in the second
cell, with values you can check by hand.

```python exec
id: your-turn-7
import math

# Your geometry functions
```

```python exec
id: your-turn-8
# Test each one with values you can verify
# Circle with radius 5: area should be about 78.54
# Rectangle 4x6: area 24, perimeter 20
```

## Putting it together: a number explorer

Now we can combine our tools into a small program. It takes a number and
prints what it can work out about it.

The program uses `classify_number` from earlier on this page. If you
have not written that function yet, the cell tells you so, and the rest
still runs. That is worth noticing: a function that reports what is
missing is much easier to work with than one that stops with an error.

What do you think it will say about 49? Run it to check.

```python exec
id: putting-it-together-a-number-explorer-1
import math

def explore_number(n):
    """Print what we can work out about a number."""
    print("Number:", n)
    if "classify_number" in globals():
        print("Domains:", classify_number(n))
    else:
        print("Domains: (write classify_number above and run this again)")
    
    if n > 0:
        print("log2:", round(math.log2(n), 4))
        print("log10:", round(math.log10(n), 4))
        print("sqrt:", round(math.sqrt(n), 4))
    
    print("n^2:", n ** 2)
    print("n^3:", n ** 3)
    
    if n == int(n) and n >= 0:
        n_int = int(n)
        # Check if it's a perfect square
        root = int(math.sqrt(n_int))
        if root * root == n_int:
            print("Perfect square! sqrt =", root)
        # Check if it's prime (simple check)
        if n_int > 1:
            is_prime = True
            for i in range(2, int(math.sqrt(n_int)) + 1):
                if n_int % i == 0:
                    is_prime = False
                    break
            print("Prime:", is_prime)
    print()

# Try it
explore_number(49)
explore_number(17)
explore_number(-3.5)
```

### Your turn

What else could `explore_number` tell us? Here are a few ideas:

- whether the number is a perfect cube
- whether it appears in the Fibonacci sequence
- what its prime factors are, when it is a positive whole number

One extension is plenty. The interesting part is deciding what belongs
in a function like this, and what does not.

```python exec
id: your-turn-9
# Your extended explore_number
```

## Reflection

On this page we worked with the basic objects of mathematics: number
families, powers, logarithms and geometry formulas. None of them is
complicated on its own. Together they are the base for everything that
follows.

The main idea underneath all of this is that every formula is already a
function: it takes inputs and produces an output. When we write it as
code, we make that clear, and we can test it.

Next, in
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive),
we start working with expressions and polynomials.

What connections do you see between logarithms and the step counts for
searching and sorting in
[Searching a list: linear and binary search](tutorial:finding-things)
and [Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order)?

## Where to Read More

3Blue1Brown (2017). *Logarithm fundamentals* (Essence of Calculus supplement).
<https://www.youtube.com/watch?v=cEvgcoyZvB4>. Why a logarithm is an exponent
read backwards, shown rather than stated.

Veritasium (2021). *The Discovery That Transformed Pi*.
<https://www.youtube.com/watch?v=gMlf1ELvRzc>. Not about pi's irrationality
directly, but the best available demonstration that a number can be perfectly
well defined and impossible to write down.

Stewart, I. (2008). *Taming the Infinite: The Story of Mathematics.* Quercus.
Chapters 2 and 3 on how the number families were built one at a time, each to
solve a problem the previous one could not.

Python Software Foundation. *Floating Point Arithmetic: Issues and Limitations.*
<https://docs.python.org/3/tutorial/floatingpoint.html>. The authoritative short
answer to why `0.1 + 0.2` is not `0.3`, and worth reading once properly.

Khan Academy. *Exponents, radicals, and scientific notation.*
<https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:rational-exponents-radicals>.
Practice on the index laws, if the ones here went past too quickly.
