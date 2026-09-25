---
title: "Rearranging formulae: changing the subject"
year: "2026-2027"
version: 2026.09.25.1
covers:
  the-same-formula-four-ways:
    covers: [MIT-1.7]
  the-moves:
    covers: [MIT-1.7]
  when-the-unknown-is-underneath:
    covers: [MIT-1.7]
  checking-yourself:
    covers: [MIT-1.7]
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
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive)
we built expressions and evaluated them. Here we take an expression
apart, and build it again so that it answers a different question.

On this page we:

- see one formula written four ways, as four Python functions
- learn the one rule behind every rearrangement
- rearrange formulae where the letter we want is under a fraction line
- write code that checks a rearrangement for us

## The same formula, four ways

Here is a formula from mechanics, the part of physics about motion:

$$v = u + at$$

In words: the final speed $v$ is the starting speed $u$, plus the
acceleration $a$ times the time $t$.

There are four letters in the formula. So there are four questions you
might ask, one for each letter. The cell below has one function for each
question. Read the four functions and compare them. The first line
works out a final speed. Can you predict what the other three lines
print, as they work backwards from that answer? Run it to check.

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

The final speed is 13 m/s. Working backwards from 13, we get back the
starting speed 5, the acceleration 2 and the time 4 that we put in.

All four functions describe the same fact about the world. Writing the
four functions *is* transposing the formula. You have done the algebra
already, in a language where you can check it.

Textbooks often show the first form as the "real" one, and the
rearrangements as copies made from it. In fact they are all equally
true. $v = u + at$ and $t = \frac{v - u}{a}$ say the same thing, with a
different letter in the spotlight.

### Your turn

The area of a circle is $A = \pi r^2$. How would you write the function
that goes the other way: given an area, what was the radius?

1. Fill in `radius(a)` in the cell below.
2. Remove the `#` from the last line, and run the cell.

```python exec
id: your-turn-1
import math

def area(r):
    return math.pi * r ** 2


def radius(a):
    # Your code here.
    pass


# print(radius(area(3)))   # should come back as 3.0
```

That last line is the whole test. Put a number through the formula one
way, then back through the other way. Do you get the number you started
with?

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
and prints both sides after each step. What do you expect to see? Run
it to check.

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
and 8, then 4.0 and 4. That is what "doing the same thing to both sides"
looks like.

The order of the steps matters. It is the reverse of the order we use
to evaluate. To work out $u + at$, we multiply first, then add. To undo
it, we subtract first, then divide. **Undoing goes from the outside in.**

### Your turn

Here are three formulae. In each one, can you make the named letter the
subject?

1. Rearrange each formula on paper first.
2. Fill in the three functions in the cell.
3. Remove the `#` from the last three lines, and run the cell.

Two checks you can do in your head: water boils at 212 °F, which is
100 °C, and a trapezium with parallel sides 4 and 6 and area 30 has
height 6.

```python exec
id: your-turn-2
# 1. Simple interest: I = P * R * T / 100. Make P the subject.
def principal(interest, rate, time):
    pass


# 2. Celsius to Fahrenheit: F = C * 9/5 + 32. Make C the subject.
def celsius(fahrenheit):
    pass


# 3. The area of a trapezium: A = (a + b) * h / 2. Make h the subject.
def height(area, a, b):
    pass


# print(principal(50, 5, 2))
# print(celsius(212))
# print(height(30, 4, 6))
```

## When the unknown is underneath

So far, the letter we wanted was always on top, never in the bottom of
a fraction. The bottom of a fraction is called the *denominator*. When
the letter we want is in a denominator, it looks harder. But the same
rule still works.

Here is the formula for two resistors, $a$ and $b$, connected side by
side (in parallel). $R$ is their total resistance:

$$\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$$

We want $R$, and $R$ is in a denominator. Here is the trick: $\frac{1}{R}$
is easy to find, because it equals the right-hand side. So we find
$\frac{1}{R}$ first, and then flip it over:

$$R = \frac{1}{\frac{1}{a} + \frac{1}{b}}$$

For example, with $a = 10$ and $b = 10$:
$\frac{1}{10} + \frac{1}{10} = \frac{2}{10}$, and flipping it gives
$R = \frac{10}{2} = 5$.

What do you think `parallel(100, 1)` will give: more than 1, or less
than 1? Run the cell to check.

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
**That is what rearranging is for.** It puts the thing you want to
understand where you can see it. It is more than tidying up.

### The denominator that is not allowed

What do you think happens when one resistance is 0? Run the cell to
find out.

```python exec
id: when-the-unknown-is-underneath-2
print(parallel(10, 5))
print(parallel(10, 0))
```

The first line works. The second one fails with an error. The algebra
warned us before the code did: $\frac{1}{b}$ with $b = 0$ is not a
number. In real life, a resistance of zero is a plain wire. A wire
beside a resistor carries all the current, so there is no resistance
left to measure.

This is a good habit to build. **When you divide by something, ask what
happens when that something is zero.** A division by zero in a formula
often points to a real situation where something breaks.

### Your turn

The lens formula is $\frac{1}{f} = \frac{1}{u} + \frac{1}{v}$.

1. How would you make $f$ the subject? Write `focal_length(u, v)`.
2. How would you make $u$ the subject? Write `object_distance(f, v)`.
3. Remove the `#` from the last two lines, and run the cell.

The second one is harder. First get $\frac{1}{u}$ on its own, and then
flip it.

```python exec
id: your-turn-3
def focal_length(u, v):
    pass


def object_distance(f, v):
    pass


# print(focal_length(30, 15))
# print(object_distance(10, 15))
```

## Checking yourself

Here is where programming helps with the algebra.

A rearrangement is correct if it agrees with the original formula for
every input. We cannot try every input. But we can try a few hundred
random ones, and in practice that finds almost any mistake you are
likely to make.

The cell below uses `lambda`, which we have not used before. A `lambda`
is a short way to write a small function on one line, without giving it
a name. For example, `lambda u, a, t: u + a * t` is a function that
takes `u`, `a` and `t`, and returns `u + a * t`.

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
            lambda v, u, a: (v + u) / a))
```

The second rearrangement has a `+` where it should have a `-`, and the
check finds it on the first try.

Why is the `1e-9` there? `1e-9` means $10^{-9}$, or 0.000000001. In
[Variables, data types and text](tutorial:storing-and-computing) we saw
that floats cannot store every number exactly. So two calculations that
should agree exactly can differ in the last decimal place. With floats,
"are these exactly equal?" is nearly always the wrong question. The
right question is: "are these closer together than I care about?"

### Your turn

How might you write a check for one of the formulae you rearranged
earlier?

1. Write a check for one formula, in the style of the cell above.
2. Run it, and make sure it agrees.
3. Now break your rearrangement on purpose. Does the check catch it?

A test that has never failed has not really been tested.

```python exec
id: your-turn-4
# Your check here.
```

## Reflection

Everything on this page used one rule: do the same thing to both sides.
We applied it from the outside in, undoing the operations in the reverse
of the order we would do them.

Here are three things worth remembering.

**No arrangement of a formula is more correct than another.** The form
a formula was written in only tells you what its writer wanted to know.

**Rearranging is for seeing.** $R = \frac{1}{\frac{1}{a} + \frac{1}{b}}$
shows things that $\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$ hides. We do
the work to reach the form where the answer is easy to see.

**You can check.** Put numbers through both versions and compare them.
That is better than reading your algebra again and hoping. You will use
this habit long after you have forgotten the formulas on this page.

Next, in
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations),
we use the same rule to find the value of an unknown.

In a few sentences: which of the rearrangements above did you find
hardest? What exactly made it harder than the others?

## Where to Read More

Khan Academy. *Rearrange Formulas to Isolate Specific Variables.*
<https://www.youtube.com/watch?v=eTSVTTg_QZ4>. The same one rule — do the
same thing to both sides — applied to a different set of formulae.
