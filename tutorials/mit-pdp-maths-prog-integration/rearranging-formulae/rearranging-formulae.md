---
title: "Rearranging Formulae"
slug: rearranging-formulae
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
covers:
  the-same-formula-five-ways:
    covers: [MIT-1.7]
  the-moves:
    covers: [MIT-1.7]
  when-the-unknown-is-underneath:
    covers: [MIT-1.7]
  checking-yourself:
    covers: [MIT-1.7]
---

# Rearranging Formulae

**Maths for IT**

A formula is usually written with one particular letter on the left, and that letter is whichever one the person who first wrote it down happened to care about. `v = u + at` is written for somebody who wants the final speed. If you know the final speed and want the time, the formula is still true -- it is just facing the wrong way.

Turning it round is called **transposing** a formula, and it is one of those skills every other subject assumes you already have. Physics assumes it, electronics assumes it, statistics assumes it, and none of them teach it.

You have already been doing the hard half of it. In *Expressions Come Alive* you built expressions and evaluated them; here you take the same expression apart and rebuild it pointing a different way.

## The Same Formula, Five Ways

Here is a formula from mechanics: `v = u + a*t`. Final speed is starting speed plus acceleration times time.

There are four letters in it, so there are four questions you might be asking. Run this and read the four functions against each other.

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

Every one of those four is the same fact about the world. Writing the four functions *is* transposing the formula -- you have done the algebra already, in a language where you can check it.

That is worth saying plainly, because textbooks tend to present the original form as the real one and the rearrangements as derived. They are all equally real. `v = u + at` and `t = (v − u)/a` are the same sentence with a different word emphasised.

### Your turn

The area of a circle is `A = pi * r**2`. How would you write the function that goes the other way: given an area, what was the radius?

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

That last line is the whole test. Put a number in one direction, take it out the other, and see whether you get what you started with.

## The Moves

There is exactly one rule, and everything else is an application of it.

**Whatever you do to one side, do to the other.** The equals sign is a statement that two things are the same size; anything you do to both of them equally keeps that true.

In practice that means working backwards through the operations, undoing each one. To get `t` out of `v = u + at`:

1. `u` is being **added**, so subtract it from both sides: `v − u = at`
2. `a` is **multiplying** `t`, so divide both sides by it: `(v − u)/a = t`

Two steps, each one undoing the outermost thing in your way. Here is that on screen, with a check after each step.

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

Each line prints both sides. They agree at every step, which is what "doing the same thing to both sides" means made visible.

The order matters and it is the reverse of how you would evaluate. To work out `u + a*t` you would multiply first, then add. To undo it you subtract first, then divide. **Unwrapping goes outside in.**

### Your turn

Three formulae, each with something to make the subject.

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

## When the Unknown Is Underneath

Everything so far had the letter you wanted somewhere on top. The awkward case is when it is in a denominator, and the move that fixes it is the same rule applied to a fraction.

Two resistors in parallel:

`1/R = 1/a + 1/b`

You want `R`, and `R` is underneath. The trick is that you can find `1/R` easily -- so find that first, and then flip it.

```python exec
id: when-the-unknown-is-underneath-1
def parallel(a, b):
    one_over_r = 1 / a + 1 / b
    return 1 / one_over_r


print(parallel(10, 10))
print(parallel(100, 1))
```

Two things worth noticing in those answers.

Two equal resistors in parallel give exactly half of one of them. And a small one beside a large one gives *slightly less than the small one* -- the 1 dominates completely and the 100 barely matters.

Both of those are readable straight off the formula once it is the right way round, and neither is obvious from `1/R = 1/a + 1/b`. **That is what rearranging is for.** It is not tidying; it is putting the thing you want to understand where you can see it.

### The denominator that is not allowed

```python exec
id: when-the-unknown-is-underneath-2
print(parallel(10, 5))
print(parallel(10, 0))
```

The second one fails, and the algebra warned you before the code did: `1/b` with `b = 0` is not a number. A zero resistance is a wire, and a wire beside a resistor carries all the current -- there is no resistance left to speak of.

This is worth a habit. **When you divide by something, ask what happens when that something is zero**, because the formula is telling you about a real situation where something breaks.

### Your turn

The lens formula is `1/f = 1/u + 1/v`. How would you make `f` the subject? And `u`?

The second one is harder: you will need to get `1/u` on its own first, and then flip.

```python exec
id: your-turn-3
def focal_length(u, v):
    pass


def object_distance(f, v):
    pass


# print(focal_length(30, 15))
# print(object_distance(10, 15))
```

## Checking Yourself

Here is the part that makes this a programming tutorial rather than an algebra worksheet.

A rearrangement is correct if it agrees with the original for every input. You cannot try every input, but you can try a few hundred random ones, which in practice finds any mistake you are likely to make.

```python exec
id: checking-yourself-1
import random

def check(original, rearranged, tries=200):
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


print(check(lambda u, a, t: u + a * t,
            lambda v, u, a: (v - u) / a))

# And now a rearrangement with a mistake in it, to see the check work.
print(check(lambda u, a, t: u + a * t,
            lambda v, u, a: (v + u) / a))
```

The second one has a `+` where it should have a `−`, and the check finds it immediately.

The `1e-9` is there because these are floating-point numbers and two calculations that should agree exactly can differ in the last decimal place. You met that in *Storing and Computing*. Asking "are these equal?" of two floats is nearly always the wrong question; asking "are these closer together than I care about?" is the right one.

### Your turn

How might you write a check for one of the formulae you rearranged earlier? Then deliberately break your rearrangement and make sure the check catches it.

A test that has never failed has not been tested.

```python exec
id: your-turn-4
# Your check here.
```

## Reflection

One rule -- do the same thing to both sides -- applied outside in, undoing the operations in the reverse of the order you would carry them out.

Three things worth taking away.

**No arrangement of a formula is more correct than another.** The one it was written in tells you what the person writing it wanted to know, and nothing more.

**Rearranging is for seeing.** `R = 1/(1/a + 1/b)` tells you things that `1/R = 1/a + 1/b` hides, and the reason to do the work is to get to the version where the answer is visible.

**You can check.** Not by re-reading your algebra and hoping, but by putting numbers through both versions and comparing. That habit will outlast every formula in this tutorial.

In a few sentences, which of the rearrangements above did you find hardest, and what specifically made it harder than the others?

## Where to Read More

Khan Academy. *Rearrange Formulas to Isolate Specific Variables.*
<https://www.youtube.com/watch?v=eTSVTTg_QZ4>. The same one rule — do the
same thing to both sides — applied to a different set of formulae.
