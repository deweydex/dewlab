---
title: "Rearranging formulae: changing the subject"
year: "2026-2027"
version: 2026.09.26.1
covers:
  the-same-formula-four-ways:
    covers: [MIT-1.7]
  the-moves:
    covers: [MIT-1.7]
  when-the-subject-is-behind-a-minus-sign:
    covers: [MIT-1.7]
  when-the-subject-appears-twice:
    covers: [MIT-1.7]
  when-the-unknown-is-underneath:
    covers: [MIT-1.7]
  checking-yourself:
    covers: [MIT-1.7]
worlds:
  rockets: Rockets, probes and the fuel they carry. The numbers are made up.
  electronics: Batteries, resistors and the voltages between them. The numbers are made up.
  music: Notes, strings and the beats between them.
  fantasy-maps: A made-up kingdom, and the journeys across it.
---

# Rearranging formulae: changing the subject

A formula usually has one letter on its own on the left. That letter is
called the *subject* of the formula. It is the quantity that the person
who first wrote the formula wanted to find.

For example, $v = u + at$ is written for somebody who wants the final
speed, $v$. But what if you know the final speed and want the time, $t$?
The formula is still true. It is only facing the wrong way for your
question.

*Transposing* a formula means rearranging it so that a different letter
is the subject. This is also called *changing the subject*. Physics,
electronics and statistics all expect you to be able to do it, and
usually none of them teach it.

You have already done half of the work. In
[Functions and their graphs](tutorial:drawing-functions) we undid a
function, step by step, in reverse order. Rearranging a formula is the
same idea, with letters: we take the formula apart, and build it again
so that it answers a different question.

## The same formula, four ways

Here is a formula from mechanics, the part of physics about motion:

$$v = u + at$$

In words: the final speed $v$ is the starting speed $u$, plus the
acceleration $a$ times the time $t$.

There are four letters in the formula. So there are four questions you
might ask, one for each letter. The cell below has one function for each
question. Read the four functions and compare them. The first line
finds a final speed. Can you predict what the other three lines
print, as they work backwards from that answer? Write your guess in a
comment first. Then run the cell.

```python exec
id: the-same-formula-five-ways-1
def final_speed(u, a, t):
    return u + a * t


def starting_speed(v, a, t):
    return v - a * t


def acceleration(v, u, t):
    return (v - u) / t


def time_taken(v, u, a):
    return (v - u) / a


# A car starting at 5 m/s, accelerating at 2 m/s^2, for 4 seconds.
v = final_speed(5, 2, 4)
print("Final speed:", v)

# And now working backwards from that answer.
print("Starting speed:", starting_speed(v, 2, 4))
print("Acceleration:", acceleration(v, 5, 4))
print("Time taken:", time_taken(v, 5, 2))
```

The final speed is 13 m/s. When we work backwards from 13, we get the
same starting speed 5, acceleration 2 and time 4 that we put in.

All four functions describe the same fact about the world. Together,
they are the formula transposed four ways, in a language where you can
check it.

Textbooks often show the first form as the "real" one, and the
rearrangements as copies made from it. In fact they are all equally
true. $v = u + at$ and $t = \frac{v - u}{a}$ say the same thing. They
only have a different letter as the subject.

### Your turn

The area of a circle is $A = \pi r^2$. How would you write the function
that goes the other way: given an area, what was the radius? The last
line of the cell is the test. Put a number through the formula one way,
then back through the other way. Do you get the number you started
with?

```python exec
id: your-turn-1
import math

def area(r):
    return math.pi * r ** 2


def radius(a):
    """The radius of a circle with area a."""
    # Your code here.


print(radius(area(3)))
```

```hint
The formula squares $r$, then multiplies by $\pi$. Which two steps undo
that, and in which order?
```

```inputs
guess: yes
radius(area(3))
radius(math.pi)
radius(100)
```

```solution
def radius(a):
    """The radius of a circle with area a."""
    return math.sqrt(a / math.pi)
---
Divide by $\pi$ first, because it was done last. Then take the square
root. `radius(area(3))` prints `3.0`, and `radius(100)` is about 5.64.
```

## The moves

There is one rule, and every step of a rearrangement uses it.

**Whatever you do to one side, do to the other.** The equals sign says
that two things are the same size. If you do the same thing to both of
them, they stay the same size.

In practice, we work backwards through the operations, and undo them
one at a time. To make $t$ the subject of $v = u + at$:

1. $u$ is being **added**, so subtract $u$ from both sides:
   $v - u = at$.
2. $a$ is **multiplying** $t$, so divide both sides by $a$:
   $\frac{v - u}{a} = t$.

That takes two steps. Each step undoes the operation that is furthest
out, the last one done. The cell below does the same steps with numbers,
and prints both sides after each step. What do you expect to see?
Write your guess in a comment first. Then run the cell.

```python exec
id: the-moves-1
# We know these values, so we know the answer must come out as t = 4.
u, a, t = 5, 2, 4
v = u + a * t
print("Starting from  v =", v)

step_one = v - u
print("Subtract u:    v - u =", step_one, " and  a*t =", a * t)

step_two = step_one / a
print("Divide by a:   (v - u)/a =", step_two, " and  t =", t)
```

Each line prints both sides, and the two sides agree at every step: 8
and 8, then 4.0 and 4. The printout shows "doing the same thing to both
sides" with real numbers.

The order of the steps matters. It is the reverse of the order we use
to evaluate. To calculate $u + at$, we multiply first, then add. To undo
it, we subtract first, then divide. **We undo from the outside in.**

### The fraction bar

On paper, $t = \frac{v - u}{a}$ has a long line under $v - u$. Here is
that formula typed on one line, the way somebody might first type it
into Python, and then again with brackets. With $v = 13$, $u = 5$ and
$a = 2$, the answer should be 4.

```python exec
id: the-fraction-bar-1
v, u, a = 13, 5, 2
print(v - u / a)
```

```predict
type: number

What will it print?
```

It prints 10.5. With brackets, it prints 4.0:

```python exec
id: the-fraction-bar-2
print((v - u) / a)
```

Python divides before it subtracts, so `v - u / a` means $v - \frac{u}{a}$: it divides
only $u$ by $a$, and then takes that from $v$.

The fraction bar on paper does more than divide. It also groups
everything above it, and everything below it, as if they were in
brackets. The bar is an invisible bracket. When you type a formula on
one line, you have to write those brackets yourself:
$\frac{v - u}{a}$ becomes `(v - u) / a`. The
[closer look at the fraction line](tutorial:the-hidden-bracket) tests
this with a second formula.

### Your turn

Here are three formulae. In each one, can you make the named letter the
subject? Rearrange each on paper first, then write the three
functions. Two checks you can do in your head: water boils at 212 °F,
which is 100 °C, and a trapezium with parallel sides 4 and 6 and area 30
has height 6.

```python exec
id: your-turn-2
# 1. Simple interest: I = P * R * T / 100. Make P the subject.
def principal(interest, rate, time):
    """The amount invested, from the interest it earned."""


# 2. Celsius to Fahrenheit: F = C * 9/5 + 32. Make C the subject.
def celsius(fahrenheit):
    """The temperature in Celsius."""


# 3. The area of a trapezium: A = (a + b) * h / 2. Make h the subject.
def height(area, a, b):
    """The height of a trapezium with parallel sides a and b."""
```

```hint
For each formula, which operation was done last? Undo that one first.
Where does the formula need brackets once it is typed on one line?
```

```inputs
guess: yes
principal(50, 5, 2)
celsius(212)
celsius(32)
height(30, 4, 6)
```

```solution
def principal(interest, rate, time):
    """The amount invested, from the interest it earned."""
    return 100 * interest / (rate * time)


def celsius(fahrenheit):
    """The temperature in Celsius."""
    return (fahrenheit - 32) * 5 / 9


def height(area, a, b):
    """The height of a trapezium with parallel sides a and b."""
    return 2 * area / (a + b)
---
Each function needs brackets. Without them, `fahrenheit - 32 * 5 / 9`
would subtract 17.8, and `2 * area / a + b` would divide by $a$ alone.
Both are the fraction bar's invisible brackets, written in.
```

## When the subject is behind a minus sign

Sometimes the letter you want has a minus sign in front of it. Here is
a formula of that kind:

$$y = 10 - 3x$$

Make $x$ the subject. The $3x$ is being subtracted. So add $3x$ to both
sides, and the minus sign is gone:

$$y + 3x = 10$$

Now $3x$ is being added to $y$. Subtract $y$ from both sides, and then
divide by 3. Dividing a side by 3 divides every term on it, and the
[closer look at dividing](tutorial:dividing-every-term) shows why that
matters:

$$3x = 10 - y \qquad\text{so}\qquad x = \frac{10 - y}{3}$$

Check it with a number. At $x = 2$, $y = 10 - 6 = 4$. And
$\frac{10 - 4}{3} = 2$.

The first move is the only new one. Add the term with the minus sign to
both sides, so that it is positive. After that, the moves are the ones
you already know.

### Your turn

<div class="dl-world" data-world="rockets">

A probe is dropped from a tower 100 m up. After $t$ seconds its height
is $h = 100 - 4.9t^2$ metres. Can you make $t$ the subject, and write
`time_at_height(h)`? When is the probe 20 m up?

```python exec
id: behind-a-minus-sign-1--rockets
import math

def time_at_height(h):
    """How many seconds after the drop the probe is h metres up."""
```

```hint
The $4.9t^2$ is being subtracted from 100. What can you add to both
sides so that it is positive? Then which steps free $t$ from
$4.9t^2$?
```

```inputs
guess: yes
time_at_height(100)
time_at_height(20)
time_at_height(0)     # the ground
```

```solution
def time_at_height(h):
    """How many seconds after the drop the probe is h metres up."""
    return math.sqrt((100 - h) / 4.9)
---
Add $4.9t^2$ and subtract $h$: $4.9t^2 = 100 - h$. Divide by 4.9, and
take the square root. The probe is 20 m up after about 4.04 s, and hits
the ground after about 4.52 s. The negative square root is a time
before the drop, so it is not an answer here.
```

</div>

<div class="dl-world" data-world="electronics">

A battery makes $E$ volts, but it has a small resistance $r$ inside it.
When a current $I$ flows, the voltage you can measure at its ends is
$V = E - Ir$. A 12 V battery shows 11.2 V while 0.4 A flows. Can you
make $r$ the subject, and write `inside_resistance(E, V, I)`?

```python exec
id: behind-a-minus-sign-1--electronics
def inside_resistance(E, V, I):
    """The resistance inside a battery, from E, the measured V and the current I."""
```

```hint
The $Ir$ is being subtracted from $E$. What can you add to both sides so
that it is positive?
```

```inputs
guess: yes
inside_resistance(12, 11.2, 0.4)
inside_resistance(9, 8.1, 0.3)
inside_resistance(12, 12, 0.5)    # no voltage lost at all
```

```solution
def inside_resistance(E, V, I):
    """The resistance inside a battery, from E, the measured V and the current I."""
    return (E - V) / I
---
Add $Ir$, subtract $V$, and divide by $I$: $r = \frac{E - V}{I}$. The
12 V battery has about 2 ohms inside it. It prints
`2.0000000000000018`, which is 2 with a rounding error. If no voltage
is lost, $r$ is 0.
```

</div>

<div class="dl-world" data-world="music">

Two notes that are close in frequency make a slow wobble in the sound,
called *beats*. The number of beats each second is the difference
between the two frequencies: $b = f_1 - f_2$, when $f_1$ is the higher
one. A guitarist plays a string against a 440 Hz tuning fork and hears
3 beats a second. The string sounds flat, so it is the lower note. Can
you make $f_2$ the subject, and write `string_frequency(fork, beats)`?

```python exec
id: behind-a-minus-sign-1--music
def string_frequency(fork, beats):
    """The frequency of a flat string, from the fork's frequency and the beats."""
```

```hint
$f_2$ is being subtracted from $f_1$. What can you add to both sides so
that it is positive?
```

```inputs
guess: yes
string_frequency(440, 3)
string_frequency(440, 0)     # no beats at all
```

```solution
def string_frequency(fork, beats):
    """The frequency of a flat string, from the fork's frequency and the beats."""
    return fork - beats
---
Add $f_2$ and subtract $b$: $f_2 = f_1 - b$. The string is at 437 Hz.
When the beats stop, the two notes are the same, and the string is in
tune.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A messenger sets out to walk 30 km to the castle at 4 km/h. After $t$
hours, the distance left is $d = 30 - 4t$. Can you make $t$ the
subject, and write `hours_until(d)`? When are there 10 km left?

```python exec
id: behind-a-minus-sign-1--fantasy-maps
def hours_until(d):
    """How many hours until the messenger has d km left to walk."""
```

```hint
The $4t$ is being subtracted from 30. What can you add to both sides so
that it is positive?
```

```inputs
guess: yes
hours_until(10)
hours_until(30)    # at the start
hours_until(0)     # at the castle
```

```solution
def hours_until(d):
    """How many hours until the messenger has d km left to walk."""
    return (30 - d) / 4
---
Add $4t$, subtract $d$, and divide by 4: $t = \frac{30 - d}{4}$. There
are 10 km left after 5 hours, and the messenger reaches the castle after
7.5 hours.
```

</div>

## When the subject appears twice

Here is a formula with $x$ in two places:

$$a = \frac{x + 3}{x}$$

The moves so far free one copy of $x$, but the other copy is still
there. The way through is to gather both copies on one side, and then
take $x$ out as a common factor.

1. Multiply both sides by $x$: $ax = x + 3$.
2. Take $x$ from both sides, so both copies are on the left:
   $ax - x = 3$.
3. Take out $x$ as a common factor: $x(a - 1) = 3$.
4. Divide by $a - 1$: $x = \frac{3}{a - 1}$.

Check it with a number. At $x = 1$, $a = \frac{4}{1} = 4$. And
$\frac{3}{4 - 1} = 1$.

Step 3 is the new move. $ax - x$ is $x$ lots of $a$, minus $x$ lots of
1, so it is $x$ lots of $a - 1$. That turns two copies of $x$ into one,
and then the usual moves work.

### Your turn

<div class="dl-world" data-world="rockets">

A rocket's *fuel fraction* is the share of its launch mass that is
fuel: $\phi = \frac{f}{m + f}$, where $f$ is the fuel and $m$ is the
rocket without fuel. A rocket stage is 25 tonnes when empty, and its
engineers want a fuel fraction of 0.9. How much fuel must it carry?
Can you make $f$ the subject, and write `fuel_needed(m, phi)`?

```python exec
id: appears-twice-1--rockets
def fuel_needed(m, phi):
    """The fuel a rocket of empty mass m needs, for a fuel fraction phi."""
```

```hint
Multiply both sides by $m + f$ first. Where is $f$ now? Gather both
copies on one side, then take $f$ out as a common factor.
```

```inputs
guess: yes
fuel_needed(25, 0.9)
fuel_needed(25, 0.5)
fuel_needed(25, 0)
```

```solution
def fuel_needed(m, phi):
    """The fuel a rocket of empty mass m needs, for a fuel fraction phi."""
    return phi * m / (1 - phi)
---
$\phi(m + f) = f$, so $\phi m = f - \phi f = f(1 - \phi)$, and
$f = \frac{\phi m}{1 - \phi}$. The stage needs 225 tonnes of fuel,
nine times its empty mass. Python prints `225.00000000000006`, which is
225 with a rounding error. At a fuel fraction of 0.5, the fuel and the
rocket weigh the same. A fraction of 1 would need infinite fuel: the
bottom is zero.
```

</div>

<div class="dl-world" data-world="electronics">

Two resistors in a line make a *voltage divider*. With $V_\text{in}$
across both, the voltage across the second one is

$$V_\text{out} = \frac{V_\text{in} R_2}{R_1 + R_2}$$

From 12 V, with $R_1 = 1000$ ohms, a sensor needs 3 V. Can you make
$R_2$ the subject, and write `second_resistor(v_in, v_out, r1)`?

```python exec
id: appears-twice-1--electronics
def second_resistor(v_in, v_out, r1):
    """The resistor R2 that gives v_out from v_in, with r1 above it."""
```

```hint
Multiply both sides by $R_1 + R_2$ first. Where is $R_2$ now? Gather
both copies on one side, then take $R_2$ out as a common factor.
```

```inputs
guess: yes
second_resistor(12, 3, 1000)
second_resistor(12, 6, 1000)     # half the voltage
second_resistor(12, 12, 1000)    # all of it
```

```solution
def second_resistor(v_in, v_out, r1):
    """The resistor R2 that gives v_out from v_in, with r1 above it."""
    return v_out * r1 / (v_in - v_out)
---
$V_\text{out}(R_1 + R_2) = V_\text{in} R_2$, so
$V_\text{out} R_1 = R_2(V_\text{in} - V_\text{out})$, and
$R_2 = \frac{V_\text{out} R_1}{V_\text{in} - V_\text{out}}$. For 3 V,
$R_2$ is about 333 ohms. For half the voltage, $R_2$ equals $R_1$. For
all 12 V, the bottom is zero. No resistor can do it, and Python raises
a `ZeroDivisionError`.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A messenger walks to the next town at 4 km/h and rides back on a horse
at $s$ km/h. The average speed for the whole journey is

$$A = \frac{8s}{4 + s}$$

The king wants an average of 5 km/h. How fast must the horse go? Can
you make $s$ the subject, and write `horse_speed(A)`?

```python exec
id: appears-twice-1--fantasy-maps
def horse_speed(A):
    """How fast the horse must go for an average speed of A km/h."""
```

```hint
Multiply both sides by $4 + s$ first. Where is $s$ now? Gather both
copies on one side, then take $s$ out as a common factor.
```

```inputs
guess: yes
horse_speed(5)
horse_speed(4)     # the same speed both ways
horse_speed(8)
```

```solution
def horse_speed(A):
    """How fast the horse must go for an average speed of A km/h."""
    return 4 * A / (8 - A)
---
$A(4 + s) = 8s$, so $4A = 8s - As = s(8 - A)$, and
$s = \frac{4A}{8 - A}$. For 5 km/h the horse must go at about
6.67 km/h. An average of 8 km/h is impossible, however fast the horse:
the walk alone takes as long as the whole journey would at 8 km/h.
Python raises a `ZeroDivisionError`.
```

</div>

## When the unknown is underneath

The bottom of a fraction is called the *denominator*. In the last
section, the letter we wanted was on the top and on the bottom. Here it
is only on the bottom. That looks harder, but the same rule still
works.

Here is the formula for two resistors, $a$ and $b$, connected side by
side (in parallel). $R$ is their total resistance:

$$\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$$

We want $R$, and $R$ is in a denominator. But $\frac{1}{R}$ is easy to
find, because it equals the right-hand side. So we find
$\frac{1}{R}$ first, and then flip it over:

$$R = \frac{1}{\frac{1}{a} + \frac{1}{b}}$$

For example, with $a = 10$ and $b = 10$:
$\frac{1}{10} + \frac{1}{10} = \frac{2}{10}$, and flipping it gives
$R = \frac{10}{2} = 5$.

What do you think `parallel(100, 1)` will give: more than 1, or less
than 1? Write your guess in a comment first. Then run the cell.

```python exec
id: when-the-unknown-is-underneath-1
def parallel(a, b):
    one_over_r = 1 / a + 1 / b
    return 1 / one_over_r


print(parallel(10, 10))
print(parallel(100, 1))
```

There are two things to notice in those answers.

- Two equal resistors in parallel give exactly half the resistance of
  one of them: 10 and 10 give 5.
- A small resistor beside a large one gives a little *less than the
  small one*: 100 and 1 give about 0.99. The 1 controls the answer, and
  the 100 hardly matters.

Both facts are easy to read from the formula once $R$ is the subject.
Neither one is easy to see in $\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$.

### The denominator that is not allowed

What do you think happens when one resistance is 0? Write your guess in
a comment first. Then run the cell.

```python exec
id: when-the-unknown-is-underneath-2
print(parallel(10, 5))
print(parallel(10, 0))
```

The first line works. The second one fails with an error. The algebra
warned us before the code did. $\frac{1}{b}$ with $b = 0$ is not a
number. In real life, a resistance of zero is a plain wire. A wire
beside a resistor carries all the current, so there is no resistance
left to measure.

This is a good habit to build. **When you divide by something, ask what
happens when that something is zero.** A division by zero in a formula
often points to a real situation where something breaks. The task in
your world in the last section had one.

### Your turn

The lens formula is $\frac{1}{f} = \frac{1}{u} + \frac{1}{v}$. How
would you make $f$ the subject, in `focal_length(u, v)`? And $u$, in
`object_distance(f, v)`? The second one is harder. First get
$\frac{1}{u}$ on its own, and then flip it.

```python exec
id: your-turn-3
def focal_length(u, v):
    """The focal length of a lens, from the two distances u and v."""


def object_distance(f, v):
    """The distance u, from the focal length f and the distance v."""
```

```hint
In `focal_length`, the right-hand side is already $\frac{1}{f}$. In
`object_distance`, what do you subtract from $\frac{1}{f}$ to leave
$\frac{1}{u}$?
```

```inputs
guess: yes
focal_length(30, 15)
object_distance(10, 15)
object_distance(10, 10)    # v the same as f
```

```solution
def focal_length(u, v):
    """The focal length of a lens, from the two distances u and v."""
    return 1 / (1 / u + 1 / v)


def object_distance(f, v):
    """The distance u, from the focal length f and the distance v."""
    return 1 / (1 / f - 1 / v)
---
`focal_length(30, 15)` is 10.0. `object_distance(10, 15)` prints
`29.999999999999993`, which is 30 with a rounding error. When $v = f$,
$\frac{1}{f} - \frac{1}{v}$ is zero, and there is no answer.
```

## Checking yourself

Programming can help with the algebra here.

A rearrangement is correct if it agrees with the original formula for
every input. We cannot try every input. But we can try a few hundred
random ones, and in practice that finds almost any mistake you are
likely to make.

The cell below uses `lambda`, which you met in
[Functions and their graphs](tutorial:drawing-functions): a short way
to write a small function on one line, without giving it a name. For
example, `lambda u, a, t: u + a * t` is a function that takes `u`, `a`
and `t`, and returns `u + a * t`.

The cell checks two rearrangements of $v = u + at$. The second one has a
mistake in it. Can you spot it before you run the cell?

```python exec
id: checking-yourself-1
import random

def do_they_agree(original, rearranged, tries=200):
    """Feed random numbers to both and see whether they ever disagree."""
    for _ in range(tries):
        u = random.uniform(1, 100)
        a = random.uniform(1, 100)
        t = random.uniform(1, 100)
        v = original(u, a, t)
        recovered = rearranged(v, u, a)
        if abs(recovered - t) > 1e-9:
            return f"They disagree: expected {t}, got {recovered}"
    return f"Agreed on all {tries} tries."


print(do_they_agree(lambda u, a, t: u + a * t,
            lambda v, u, a: (v - u) / a))

# And now a rearrangement with a mistake in it, to see the check work.
print(do_they_agree(lambda u, a, t: u + a * t,
            lambda v, u, a: v - u / a))
```

The second rearrangement is the one from the fraction bar: `v - u / a`,
with the invisible brackets left out. The check finds it on the first
try.

Why is the `1e-9` there? `1e-9` means $10^{-9}$, or 0.000000001. In
[Variables, data types and text](tutorial:storing-and-computing) we saw
that floats cannot store every number exactly. So two calculations that
should agree exactly can differ in the last decimal place. So with
floats, we do not ask "are these exactly equal?" We ask "are these
closer together than I care about?"

### Your turn

How might you write a check for one of the formulae you rearranged
earlier? Write it in the style of the cell above, and run it. Then
break your rearrangement on purpose. Does the check catch it? If a
check never fails, you do not know that it can catch a mistake.

```python exec
id: your-turn-4
# Your check here.
```

## Looking back

Two moves on this page were new: adding a term with a minus sign to
both sides, and gathering two copies of the subject before taking it
out as a factor. Which formula on this page would you give to somebody
to show them why the second move is needed?

A challenge: can you write a checker that works for any formula, not
only $v = u + at$? It would take the original formula, the
rearrangement, and the names of the letters. The version in the
practice page's tools cell is one way.

```python challenge
import random

# The original: v = u + a*t. The rearrangement to check: t = (v - u) / a.
def original(u, a, t):
    return u + a * t


def rearranged(v, u, a):
    return (v - u) / a


for _ in range(5):
    u, a, t = (random.uniform(1, 10) for _ in range(3))
    print(t, rearranged(original(u, a, t), u, a))
```

## Where to read more

Khan Academy. *Rearrange Formulas to Isolate Specific Variables.*
<https://www.youtube.com/watch?v=eTSVTTg_QZ4>. This video uses the same
rule, do the same thing to both sides, on a different set of formulae.
