---
title: "Approaching a Limit"
slug: approaching-a-limit
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
covers:
  a-hole-in-a-line:
    covers: [MIT-3.5]
  getting-closer-without-arriving:
    covers: [MIT-3.5]
  when-there-is-no-limit:
    covers: [MIT-3.5]
  why-anybody-needs-this:
    covers: [MIT-3.5]
---

# Approaching a Limit

**Maths for IT**

A limit is the answer to a question of the form: *what would this be, if I could get there?*

That sounds evasive, and for two hundred years mathematicians were uneasy about it for exactly that reason. It turns out to be one of the most useful ideas in the subject, and it is the one thing standing between you and being able to talk about how fast something is changing at a single instant.

The good news is that computers make limits obvious in a way that paper does not. You can just try it, with numbers, and watch.

## A Hole in a Line

Here is a function that is completely ordinary except at one point.

```python exec
id: a-hole-in-a-line-1
def f(x):
    return (x ** 2 - 1) / (x - 1)


for value in [0, 0.5, 2, 3, 10]:
    print(f"f({value}) = {f(value)}")
```

Every answer is `x + 1`. And that makes sense: `x² − 1` factorises into `(x − 1)(x + 1)`, and the `(x − 1)` on top cancels the one underneath.

Except at one place.

```python exec
id: a-hole-in-a-line-2
print(f(1))
```

At `x = 1` the bottom is zero, so the cancelling is not allowed and the function has no value there at all. The domain of `f` is every number except 1.

```python exec
id: a-hole-in-a-line-3
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))
xs = [x / 100 for x in range(-100, 301) if abs(x / 100 - 1) > 0.005]
ax.plot(xs, [f(x) for x in xs], linewidth=2)
ax.plot([1], [2], "o", markerfacecolor="white", markeredgecolor="tab:blue",
        markersize=10, markeredgewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.grid(alpha=0.3)
ax.set_title("A straight line with one point missing")
```

A perfectly good line with a hole punched in it.

Now the question that limits answer. **The function has no value at 1. But if it did, what would it obviously have to be?**

## Getting Closer Without Arriving

You cannot ask for `f(1)`. You can ask for `f` of things very close to 1, from both sides, and watch.

```python exec
id: getting-closer-without-arriving-1
print("coming up from below")
for step in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
    x = 1 - step
    print(f"   f({x:<10}) = {f(x)}")

print()
print("coming down from above")
for step in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
    x = 1 + step
    print(f"   f({x:<10}) = {f(x)}")
```

From below the answers march up towards 2. From above they march down towards 2. Neither side ever *reaches* 2, because neither side ever reaches 1.

**The limit of `f(x)` as `x` approaches 1 is 2.** Written down, that is:

`lim(x→1) f(x) = 2`

And the sentence it stands for is: *you can get the output as close to 2 as you like, by getting the input close enough to 1.*

Notice what that sentence does not say. It does not say the function equals 2 at 1 — it does not, it has no value there. **A limit is a statement about the neighbourhood, not about the point.** That distinction is the whole idea, and it is why limits can talk about places a function cannot go.

### Both sides have to agree

```python exec
id: getting-closer-without-arriving-2
def step_function(x):
    return -1 if x < 0 else 1


print("from below:")
for step in [0.1, 0.01, 0.001]:
    print(f"   step_function({-step}) = {step_function(-step)}")

print("from above:")
for step in [0.1, 0.01, 0.001]:
    print(f"   step_function({step}) = {step_function(step)}")
```

Approaching zero from the left, the answers sit at −1. From the right, at 1. They do not agree, and there is no single number the function is heading for.

So **this limit does not exist** — not because the calculation is hard, but because the question has two different answers depending on which way you come at it.

### Your turn

What is the limit of `(x² − 4)/(x − 2)` as `x` approaches 2? Try values from both sides, then factorise the top and see whether the answer makes sense.

```python exec
id: your-turn-1
def g(x):
    return (x ** 2 - 4) / (x - 2)


# Your investigation here.
```

## When There Is No Limit

Not every hole is fillable. Sometimes getting closer makes things worse.

```python exec
id: when-there-is-no-limit-1
def h(x):
    return 1 / x


for step in [0.1, 0.01, 0.001, 0.0001]:
    print(f"h({step}) = {h(step):>12.1f}     h({-step}) = {h(-step):>12.1f}")
```

From the right it grows without bound; from the left it plunges without bound. There is no number it is approaching, in either direction.

```python exec
id: when-there-is-no-limit-2
fig, ax = plt.subplots(figsize=(7, 4))
left = [x / 100 for x in range(-300, -3)]
right = [x / 100 for x in range(3, 301)]
ax.plot(left, [1 / x for x in left], linewidth=2, color="tab:blue")
ax.plot(right, [1 / x for x in right], linewidth=2, color="tab:blue")
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="tab:red", linestyle=":", linewidth=1.5)
ax.set_ylim(-20, 20)
ax.grid(alpha=0.3)
ax.set_title("No limit at zero, in either direction")
```

You have met this shape twice already. It is the tangent function's behaviour at 90 degrees, and it is the vertical line that has no slope, and it is the same underlying fact each time: dividing by something that is shrinking to nothing.

### A limit that exists at infinity

The other useful direction is asking what happens as `x` gets very large rather than very close.

```python exec
id: when-there-is-no-limit-3
for x in [1, 10, 100, 1000, 100000, 10000000]:
    print(f"1/{x:<10} = {1 / x}")
```

As `x` grows, `1/x` heads for 0 and never gets there. That is a limit too — the limit as `x` approaches infinity is 0.

```python exec
id: when-there-is-no-limit-4
# A more interesting one: what does this settle on?
def ratio(n):
    return (3 * n + 5) / (n + 2)


for n in [1, 10, 100, 1000, 100000]:
    print(f"n = {n:<8} -> {ratio(n)}")
```

It settles on 3. Which you could have guessed: for large `n` the `+5` and the `+2` stop mattering, and what is left is `3n/n`.

## Why Anybody Needs This

Now the reason this tutorial exists, which is a question you cannot ask without it.

**How fast is something changing at one instant?**

Speed is distance over time — but that needs two moments to work with. "Distance travelled in no time at all, divided by no time at all" is `0/0`, which is not a number.

Here is a ball dropped from a height. Distance fallen after `t` seconds is about `4.9t²` metres.

```python exec
id: why-anybody-needs-this-1
def fallen(t):
    return 4.9 * t ** 2


print("After 1 second:", fallen(1), "m")
print("After 2 seconds:", fallen(2), "m")
print()
print("Average speed over that second:", fallen(2) - fallen(1), "m/s")
```

That is the average over a whole second, and the ball was speeding up the whole time, so it is not the speed at any particular moment.

Make the interval smaller.

```python exec
id: why-anybody-needs-this-2
def average_speed(t, gap):
    return (fallen(t + gap) - fallen(t)) / gap


print("Speed at t = 1, measured over shorter and shorter intervals:")
for gap in [1, 0.5, 0.1, 0.01, 0.001, 0.0001, 0.00001]:
    print(f"   gap of {gap:<9} : {average_speed(1, gap)}")
```

The numbers are heading for 9.8, and they never arrive — you cannot set the gap to zero, because that is `0/0`.

**But the limit exists, and it is 9.8 m/s.** That is the speed at the instant `t = 1`, and it is a real answer to a question that had no arithmetic.

```python exec
id: why-anybody-needs-this-3
fig, ax = plt.subplots(figsize=(7, 4))
gaps = [1 / (1.6 ** k) for k in range(22)]
ax.plot(gaps, [average_speed(1, g) for g in gaps], "o-", markersize=4)
ax.axhline(9.8, color="tab:red", linestyle="--", label="9.8")
ax.set_xscale("log")
ax.invert_xaxis()
ax.set_xlabel("size of the gap (getting smaller to the right)")
ax.set_ylabel("average speed over that gap")
ax.grid(alpha=0.3)
ax.legend()
ax.set_title("Closing in on the speed at one instant")
```

### Your turn

What speed is the ball travelling at three seconds in? Try the same approach at `t = 3`.

Then try `t = 0` — does the answer make sense for a ball that has just been let go?

```python exec
id: your-turn-2
# Your code here.
```

## A Warning About Trying It With Numbers

Everything above worked by computing values and looking. That is an excellent way to *see* a limit, and it is not a proof — and floating-point arithmetic will eventually lie to you.

```python exec
id: a-warning-about-trying-it-with-numbers-1
def f(x):
    return (x ** 2 - 1) / (x - 1)


for step in [1e-10, 1e-13, 1e-15, 1e-16]:
    x = 1 + step
    try:
        print(f"f(1 + {step:<8}) = {f(x)}")
    except ZeroDivisionError:
        print(f"f(1 + {step:<8}) = the arithmetic gave up")
```

The first three are fine. The fourth stops being arithmetic at all.

`1 + 1e-16` is **not a different number from 1** in double-precision floating point — there is no room left to record the difference. So `x - 1` on the bottom is exactly zero, and the division fails.

Notice what did *not* happen. The answers did not drift or degrade gracefully; they were exactly right and then the calculation died. That is characteristic: floating point usually fails suddenly rather than gradually, at whichever step first asks it to represent a difference smaller than it can hold.

**The mathematics is fine and the arithmetic ran out.** The limit is still 2 — nothing about the function changed at `1e-16`. What changed is that the computer stopped being able to tell `1 + 1e-16` from `1`.

You met the same floor in *Storing and Computing*, where two floats that should have been equal were not.

So use the numbers to see what the answer is, and use algebra to know it. In the very first example, cancelling `(x − 1)` tells you the answer is `x + 1` and therefore 2 — with no approximation anywhere.

## Reflection

A limit is what a function is heading towards, whether or not it ever gets there.

**It is a statement about the neighbourhood, not the point.** The function need not have a value where you are asking, and often the interesting cases are exactly the ones where it does not.

**Both sides have to agree**, or there is no limit.

**Some limits do not exist**, and running away to infinity is the usual reason.

**The point of all this is the next tutorial.** "How fast is it changing right now?" is `0/0` if you ask it directly, and a limit is the thing that makes it answerable.

**Numbers show you the answer; algebra proves it.** And past about fifteen decimal places, the numbers stop showing you anything at all.

In a few sentences and in your own words, what is the difference between "f(1) = 2" and "the limit of f as x approaches 1 is 2"?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2017). *Essence of Calculus, Chapter 7:
Limits, L'Hôpital's Rule, and Epsilon Delta Definitions.*
<https://www.youtube.com/watch?v=kfF40MiS7zA>. The formal definition
behind the "getting closer without arriving" this page does by trying
numbers.
