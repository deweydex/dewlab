---
title: "Counting Darts"
slug: counting-darts
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.08.30.1
covers:
  a-question-you-can-answer-by-throwing-things:
    covers: [CMPS-LO3]
  one-dart-at-a-time:
    covers: [CMPS-LO3]
  watching-it-settle:
    covers: [CMPS-LO3]
  more-is-not-reliably-better:
    covers: [CMPS-LO3, CMPS-LO13]
---

# Counting Darts

The last tutorial ended with a machine that produces unpredictable numbers on
demand. This one spends them on something that looks, at first, like an
absurd way to do mathematics: working out the value of π by throwing darts at
a wall and counting where they land.

It is absurd, and it works, and the reason it works is the foundation of an
entire family of methods that get used on problems where nothing else does.

## A Question You Can Answer by Throwing Things

Picture a square, one unit on each side, with a quarter-circle drawn inside
it from corner to corner.

The square's area is $1 \times 1 = 1$. The quarter-circle's area is a quarter
of a full circle of radius 1, which is $\pi/4$. So if you scattered points
across that square completely at random, the *fraction* landing inside the
curve should be:

$$\frac{\text{quarter-circle area}}{\text{square area}} = \frac{\pi/4}{1} = \frac{\pi}{4}$$

Which rearranges to something useful. Multiply the fraction that lands inside
by 4, and you have an estimate of π — obtained without measuring a circle,
without a formula for its area, and without knowing π in the first place.

The only thing needed is a way to tell whether a point is inside the curve.
A point $(x, y)$ is inside a circle of radius 1 centred on the origin exactly
when $x^2 + y^2 \le 1$ — which is Pythagoras, doing the only work anyone asks
of it here.

```python exec
id: a-question-you-can-answer-by-throwing-things-1
def inside_circle(x, y):
    """True when the point lies within the quarter-circle of radius 1."""
    return x * x + y * y <= 1

print(inside_circle(0.2, 0.3))   # near the corner the curve encloses
print(inside_circle(0.9, 0.9))   # out past the curve
```

### Your turn

Where does the point $(0.6, 0.8)$ fall? Work it out on paper first — $0.6^2 +
0.8^2$ is a calculation worth doing by hand — then check.

```python exec
id: a-question-you-can-answer-by-throwing-things-2
hint: 0.36 + 0.64. The answer is exactly on the boundary, which is why this particular point is worth asking about.
```

## One Dart at a Time

Now the throwing. Each dart is a pair of random numbers between 0 and 1 —
which is precisely what `random.random()` hands over, so a dart costs two
calls and nothing else.

```python exec
id: one-dart-at-a-time-1
import random

def estimate_pi(n, seed=0):
    """Throw n darts at the unit square; return 4 x the fraction inside.

    Seeds itself, so every call is repeatable and independent of whatever
    ran before it — the habit from the last tutorial, doing real work here.
    """
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if inside_circle(x, y):
            hits += 1
    return 4 * hits / n

print(estimate_pi(100))
```

3.04, from a hundred darts and no mathematics beyond a square root that never
even got taken.

It is also wrong in the second decimal place, which is worth sitting with
rather than hurrying past. The method has not made an error. There is no bug
to find. A hundred darts genuinely does not contain enough information to
pin π down further than that, and no amount of care in the code would change
it.

### Your turn

What happens with more darts? Try 1,000, then 10,000, and see how close each
gets.

```python exec
id: one-dart-at-a-time-2
hint: The function already takes n as its argument, so this is three calls. Printing the difference from math.pi alongside each estimate makes the comparison easier to read than the estimates alone.
```

## Watching It Settle

Printing three numbers tells you the answer improves. It does not show you
*how* it improves, and the shape of that improvement is the real subject.

So rather than throwing a batch and reporting one number, this version keeps
a running estimate — recording, after every single dart, what π would be
estimated as if you stopped right there.

```python exec
id: watching-it-settle-1
import random
import matplotlib.pyplot as plt

random.seed(0)

hits = 0
running = []
for throw in range(1, 5001):
    x, y = random.random(), random.random()
    if inside_circle(x, y):
        hits += 1
    running.append(4 * hits / throw)

plt.plot(running, linewidth=0.8)
plt.axhline(3.14159, color="grey", linestyle="--", label="π")
plt.ylim(2.6, 3.6)
plt.xlabel("darts thrown")
plt.ylabel("estimate")
plt.legend()
```

That picture is the tutorial. Three things in it are worth naming.

The estimate is **wild at the start** — with ten darts, one dart either way
moves it by 0.4 — and settles as the count grows, because each new dart is a
smaller fraction of the total and can shift the average less.

It **never stops moving**. There is no point where it arrives at π and stays.
It wanders around the answer, and it will still be wandering at a million
darts, just in a narrower band.

And it **approaches from no particular direction**. The estimate is not
climbing towards π or falling towards it; it crosses the line repeatedly, and
whether it happens to be above or below when you stop is luck.

### Your turn

What does the same plot look like with a different seed? Change `random.seed(0)`
to another number and run it again — then say what stays the same between the
two pictures and what does not.

```python exec
id: watching-it-settle-2
hint: Look at the shape of the settling rather than the particular wiggles. The wiggles are different every time; something about them is not.
```

## More Is Not Reliably Better

Here is the result that makes this method honest, and it comes out of a
table rather than an argument.

```python exec
id: more-is-not-reliably-better-1
import math

for n in [100, 1000, 10000, 100000]:
    estimate = estimate_pi(n)
    print(f"n = {n:>6}   estimate = {estimate:.5f}   off by {abs(estimate - math.pi):.5f}")
```

Read the last column downward. A hundred darts is off by about 0.10. A
thousand darts is off by about 0.014 — a real improvement. Ten thousand gets
to 0.006.

And a hundred thousand darts is off by 0.0069, which is *worse than ten
thousand*.

That is not a mistake in the code and it is not a bad seed. Ten times the
work bought a slightly worse answer on this particular run, and that is a
completely ordinary thing for this method to do. Run it with another seed and
the numbers will differ; the pattern of a stubbornly slow, unreliable
improvement will not.

```python exec
id: more-is-not-reliably-better-3
for seed in [0, 1, 2, 3]:
    estimate = estimate_pi(100000, seed=seed)
    print(f"seed = {seed}   estimate = {estimate:.5f}")
```

Four runs, all one hundred thousand darts, produce four different second
decimal places. This shows two separate questions worth asking about any
model's numbers. *Accuracy* is how close an estimate is to the true
answer — the "off by" column above. *Precision* is how much of an
estimate stays the same if the whole thing is run again.

A hundred thousand darts here is reasonably accurate, off by well under a
hundredth. It is not especially precise, since a fresh run can produce a
different second decimal place entirely. Knowing which one is missing
decides what fixing it actually needs: more darts, a better method, or a
clearer sense of how far the number can be trusted.

The underlying rule, which the next tutorial takes apart properly, is that
the typical error shrinks in proportion to $1/\sqrt{n}$. Squeezing one more
decimal place out of the answer means about **a hundred times** the darts.
Two more decimal places means ten thousand times. This is why nobody computes
π this way — there are far better methods — and why it is still the first
example everyone is shown: the arithmetic is trivial, so the behaviour is
what you notice.

### Your turn

If a hundred thousand darts gets you to roughly two correct decimal places,
roughly how many would you need for four? Work it out from the rule above
before running anything, and then decide whether running it is a good use of
your afternoon.

```python exec
id: more-is-not-reliably-better-2
hint: Two more decimal places means the error has to fall by a factor of 100. If error goes as 1/sqrt(n), what does n have to do?
```

## Reflection

The method in this tutorial has no formula for π in it anywhere. It does not
know what π is. It counts a proportion, and π falls out of the geometry of
the question being asked.

That is the move worth carrying forward, because it generalises far past
circles. Any quantity that can be written as "the fraction of cases where
something is true" can be estimated by generating cases and counting — and
plenty of real questions have that shape while having no formula at all. What
fraction of delivery routes finish before 5pm? How often does this design
fail under load? Those are not solvable on paper, and they are exactly as
easy to throw darts at as a quarter-circle is.

Was the wandering estimate uncomfortable to look at? Most of the mathematics
you have met so far produces an answer that is simply correct, and a method
whose answer is *approximately* right, by an amount you can only describe
statistically, asks for a different kind of trust. That discomfort is the
right instinct — it is what the next tutorial is for.

## Where to Read More

Metropolis, N. and Ulam, S. (1949). *The Monte Carlo Method.* Journal of the
American Statistical Association, 44(247), 335–341.
<https://doi.org/10.1080/01621459.1949.10483310>. The paper that named the
method, written while it was being used on problems nobody could solve any
other way. Short, and much more readable than its date suggests.

Downey, A. B. (2014). *Think Stats* (2nd ed.). O'Reilly.
<https://greenteapress.com/thinkstats2/>. Chapter 9 works through simulation
as a way of answering statistical questions without formulas, which is this
tutorial's argument applied to real data.

Robert, C. P. and Casella, G. (2004). *Monte Carlo Statistical Methods*
(2nd ed.). Springer. The standard graduate reference, well past this course's
level — listed because Chapter 1's opening pages make the same argument this
tutorial does, that the method earns its place on problems where no formula
is available, and it is worth seeing that stated by the people who use it in
earnest.
