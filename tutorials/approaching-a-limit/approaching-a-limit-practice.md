---
title: "Limits: getting closer without arriving — Practice"
practice_for: approaching-a-limit
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: A tank of fresh water, filling with seawater. The numbers are made up.
  planets-and-moons: The Earth's pull on a spacecraft, further and further away.
  fantasy-maps: A messenger who walks half of what is left each hour. The numbers are made up.
---

# Limits: getting closer without arriving — Practice

Each answer is hidden in a fold under its question. Try the question
first, then open the fold to check.

When a question asks you to find a limit, try two things:

1. Try it with numbers, from both sides.
2. Say what the algebra gives.

When the two agree, you can trust the answer.

## Tools

This cell defines `approach`, a helper that prints a function's values
as the input comes closer to a target. It then tries it on
$\dfrac{x^2 - 1}{x - 1}$ near 1, the example from the tutorial.

```python exec
id: tools-1
def approach(f, target, from_below=True):
    """Print f at values marching towards `target`."""
    for step in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
        x = target - step if from_below else target + step
        try:
            print(f"   f({x:<12}) = {f(x)}")
        except ZeroDivisionError:
            print(f"   f({x:<12}) = undefined")


f = lambda x: (x ** 2 - 1) / (x - 1)
print("from below:")
approach(f, 1)
print("from above:")
approach(f, 1, from_below=False)
```

## Finding a limit

**1.** The cell tries $\dfrac{x^2 - 25}{x - 5}$ just above 5.

```python exec
id: finding-a-limit-1
def g(x):
    return (x ** 2 - 25) / (x - 5)


print(g(5.001))
```

```predict
type: number
tolerance: 0.01

What will it print, roughly?
```

<details class="dl-answer"><summary>why</summary>

It prints about 10.001. The top factorises as $(x - 5)(x + 5)$, so away
from 5 the function is the same as $x + 5$, and $5.001 + 5 = 10.001$.
The limit as $x$ approaches 5 is 10, although the function has no value
at 5.

</details>

**2.** What is the limit of $\dfrac{x^2 - 9}{x - 3}$ as $x$ approaches 3?

<details class="dl-answer"><summary>answer</summary>

6.

Factorise in the same way: $\dfrac{(x - 3)(x + 3)}{x - 3}$ leaves
$x + 3$. At 3, that is $3 + 3 = 6$.

</details>

**3.** What is the limit of $\dfrac{x^3 - 1}{x - 1}$ as $x$ approaches 1?

<details class="dl-answer"><summary>answer</summary>

3.

$x^3 - 1$ factorises as $(x - 1)(x^2 + x + 1)$. The $(x - 1)$ cancels,
leaving $x^2 + x + 1$. At $x = 1$ that is $1 + 1 + 1 = 3$.

</details>

**4.** What is the limit of $\dfrac{\sqrt{x} - 2}{x - 4}$ as $x$
approaches 4?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{1}{4}$.

Write the bottom as $(\sqrt{x} - 2)(\sqrt{x} + 2)$. The $(\sqrt{x} - 2)$
cancels, leaving $\dfrac{1}{\sqrt{x} + 2}$. At $x = 4$ that is
$\dfrac{1}{2 + 2} = \dfrac{1}{4}$.

It is worth checking with numbers too. The values move towards 0.25 from
both sides.

</details>

**5.** Does $\dfrac{|x|}{x}$ have a limit as $x$ approaches 0?

<details class="dl-answer"><summary>answer</summary>

No.

From the right, it is 1, because a positive number divided by itself is
1. From the left, it is −1. The two sides disagree, so there is no
single value it is moving towards.

This is the step function from the tutorial, written in different
notation.

</details>

## Limits that do not exist

**6.** What happens to $\dfrac{1}{x^2}$ as $x$ approaches 0? Is that a
limit?

<details class="dl-answer"><summary>answer</summary>

It grows without end from *both* sides, because squaring removes the
minus sign.

Strictly, there is no limit, because no number is being approached.
People often write "the limit is infinity". That is a short way of
saying "it grows without end". It does not claim that infinity is a
number.

</details>

**7.** How is $\dfrac{1}{x}$ different from $\dfrac{1}{x^2}$ near zero?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{1}{x}$ goes to positive infinity from the right and to negative
infinity from the left. $\dfrac{1}{x^2}$ goes to positive infinity from
both sides.

Neither one has a limit. But the second one at least does the same thing
on both sides.

</details>

**8.** What is the limit of $\dfrac{1}{x}$ as $x$ grows without end?

<details class="dl-answer"><summary>answer</summary>

0.

The values shrink towards zero and never reach it. This is the same kind
of statement as before: the value is approached, but never reached.

</details>

**9.** What is the limit of $\dfrac{3n + 5}{n + 2}$ as $n$ grows without
end?

<details class="dl-answer"><summary>answer</summary>

3.

Divide the top and the bottom by $n$:
$\dfrac{3 + \frac{5}{n}}{1 + \frac{2}{n}}$. As $n$ grows, both small
terms, $\frac{5}{n}$ and $\frac{2}{n}$, move towards 0. That leaves
$\dfrac{3}{1} = 3$.

For large $n$, only the highest powers matter. This is a useful rule.
So the answer is the ratio of the numbers in front of the highest powers
(the leading coefficients).

</details>

**10.** What is the limit of $\dfrac{2n^2 + n}{5n^2 - 3}$ as $n$ grows
without end?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{2}{5}$.

The reasoning is the same. The $n^2$ terms are much bigger than
everything else, so everything else hardly matters. That leaves
$\dfrac{2n^2}{5n^2} = \dfrac{2}{5}$.

</details>

## Why limits matter

**11.** A toy car's distance is $2t^3$ metres after $t$ seconds. What
is its speed at $t = 2$? Can you find it with the algebra, as well as
with numbers?

<details class="dl-hint"><summary>hint</summary>

The average speed from $t = 2$ to $t = 2 + h$ is
$\dfrac{2(2 + h)^3 - 16}{h}$. Expand $(2 + h)^3$ first.

</details>

<details class="dl-answer"><summary>one way through it</summary>

$(2 + h)^3 = 8 + 12h + 6h^2 + h^3$, so the top is
$16 + 24h + 12h^2 + 2h^3 - 16 = 24h + 12h^2 + 2h^3$. Divide by $h$ to get
$24 + 12h + 2h^2$. As $h$ shrinks, that moves towards **24 m/s**.

With numbers, a gap of `1e-7` gives about 24.0000012.

</details>

**12.** What happens if the gap is negative, so the second moment is
*before* the first? Here is the ball's average speed at $t = 3$, over a
gap of $-0.001$.

```python exec
id: why-limits-matter-1
def fallen(t):
    return 4.9 * t ** 2


gap = -0.001
print((fallen(3 + gap) - fallen(3)) / gap)
```

<details class="dl-answer"><summary>answer</summary>

It prints about 29.3951, just below 29.4. A negative gap measures the
speed over the moment just before $t = 3$, when the ball was a little
slower. Positive gaps come down towards 29.4 from above, and negative
gaps come up towards it from below. Both sides agree, so the limit is
29.4.

</details>

**13.** Why can we not set the gap to zero and compute the answer
directly?

<details class="dl-answer"><summary>answer</summary>

Because that gives $\dfrac{0}{0}$: a distance of zero, travelled in no
time, divided by no time.

$\dfrac{0}{0}$ is not a number, and it is not a short way of writing
one. It tells us that the question needs a different method. The limit
is that method.

</details>

## Where numbers stop helping

**14.** The cell adds a tiny number to 1, then subtracts the 1 again.

```python exec
id: where-numbers-stop-helping-1
print((1 + 1e-16) - 1)
print((1 + 1e-15) - 1)
```

```predict
type: number

The first line prints 0.0. What will the second line print?
```

<details class="dl-answer"><summary>why</summary>

It prints `1.1102230246251565e-15`, not `1e-15`. A float keeps about 16
significant digits. `1 + 1e-15` has room for the tiny part, but only
roughly, so taking the 1 away leaves a number near $10^{-15}$ that is
not exactly it. `1 + 1e-16` has no room at all, and the tiny part is
lost. That lost part is why the tutorial's speed went silently to 0.0.

</details>

**15.** So what should we use numbers for, and what should we use algebra
for?

<details class="dl-answer"><summary>answer</summary>

We use numbers to *see* what the answer is. A column of values moving
towards 2 is convincing, and quick to produce.

We use algebra to *know* it. Cancelling $(x - 1)$ proves that the answer
is exactly 2, with no approximation anywhere and no rounding error.

Neither one can replace the other. If you only use numbers, they will
mislead you in the end.

</details>

## One longer one

**16.** A regular polygon with $n$ equal sides fits inside a circle of
radius 1, with its corners on the circle. Its perimeter is
$2n \sin\left(\dfrac{\pi}{n}\right)$.

1. Compute the perimeter for $n$ = 3, 6, 12, 100 and 10000.
2. What is it approaching, and why?
3. What does that tell you about $\pi$?

<details class="dl-answer"><summary>answer</summary>

1. About 5.196, 6.000, 6.212, 6.282 and 6.28319.

2. It approaches $2\pi \approx 6.28319$, the circumference of the
   circle. As $n$ grows, the polygon gets closer to the circle, so its
   perimeter gets closer to the circle's circumference.

3. It gives us a way to compute $\pi$. Take the perimeter of a polygon
   with many sides and halve it. This is close to Archimedes' method from
   around 250 BCE. It is a limit argument, made two thousand years
   before limits were defined.

```python
import math
for n in [3, 6, 12, 100, 10000]:
    print(n, 2 * n * math.sin(math.pi / n))
```

Notice a problem here. This code uses `math.pi` to compute $\pi$, so it
proves nothing. Archimedes found the side
lengths with geometry instead, by cutting angles in half again and
again.

</details>

**17.** Can you write a Python function whose limit at 3 is 5, but whose
value at 3 is 7?

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def odd_one(x):
    if x == 3:
        return 7
    return x + 2
```

Near 3, from both sides, the values move towards 5, so the limit is 5.
At 3 itself the function says 7. The limit does not depend on what
happens at the point, only near it.

</details>

## Your world

**18.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

A tank of fresh water is slowly filled with seawater. After $t$
minutes, its water holds $\dfrac{35t}{t + 20}$ grams of salt in each
litre. What does the saltiness settle on as $t$ grows? Can you see it
with numbers, and then say why from the formula?

```python exec
id: your-world-1--sea-and-sky
def salt(t):
    return 35 * t / (t + 20)


for t in [1, 10, 100, 1000, 100000]:
    print(t, salt(t))
```

<details class="dl-answer"><summary>answer</summary>

It settles on 35 grams a litre, about the saltiness of the sea. When
$t$ is very large, the $+ 20$ is tiny next to $t$, so the formula is
close to $\dfrac{35t}{t} = 35$. It never quite reaches 35, since the
bottom is always a little bigger than $t$.

</details>

</div>

<div class="dl-world" data-world="planets-and-moons">

The Earth pulls on a spacecraft $h$ km above its surface with a
strength of $\dfrac{9.8}{(1 + h / 6371)^2}$ metres per second every
second. 6371 km is the Earth's radius. What does the pull settle on as
$h$ grows? Is there a height where it is exactly 0?

```python exec
id: your-world-1--planets-and-moons
def pull(h):
    return 9.8 / (1 + h / 6371) ** 2


for h in [0, 400, 36000, 384400, 10 ** 9]:
    print(h, pull(h))
```

<details class="dl-answer"><summary>answer</summary>

The pull moves towards 0 as $h$ grows, and never gets there: the limit
at infinity is 0. At 400 km, where the space station flies, it is still
about 8.7, nearly nine tenths of the pull on the ground. The astronauts
float because they are falling round the Earth, not because the pull
has gone.

</details>

</div>

<div class="dl-world" data-world="fantasy-maps">

A messenger sets out for a castle 10 km away. Each hour, the messenger
walks half of the distance that is left. How far has the messenger gone
after $n$ hours? Can you write `gone(n)` with a loop, and find the
limit as $n$ grows?

```python exec
id: your-world-1--fantasy-maps
# Your code here.
```

```hint
Keep the distance left. Each hour, the messenger walks half of it, so
what is left is halved.
```

```inputs
gone(1)
gone(3)
round(gone(50), 6)
```

```solution
def gone(n):
    left = 10
    for _ in range(n):
        left = left / 2
    return 10 - left
---
After 1 hour the messenger has gone 5 km, after 3 hours 8.75 km, and
after 50 hours so close to 10 km that the difference is too small to
see. The limit is 10 km. The messenger never quite arrives.
```

</div>

## From earlier

**19.** From [Number types, powers and logarithms](tutorial:numbers-and-their-families).
What does $\left(1 + \frac{1}{n}\right)^n$ settle on as $n$ grows? Try
$n$ = 1, 10, 100, 10,000 and 1,000,000.

<details class="dl-answer"><summary>answer</summary>

It settles on about 2.71828. That number is called $e$, and Python has
it as `math.e`. It is the limit at infinity of this expression. It
appears wherever something grows in proportion to its own size, such as
money with interest added more and more often.

</details>

**20.** From [The unit circle: sine, cosine and tangent](tutorial:the-unit-circle).
What is the limit of $\dfrac{\sin x}{x}$ as $x$ approaches 0, with $x$
in radians? What if $x$ is in degrees?

```python exec
id: from-earlier-1
import math

for x in [0.1, 0.01, 0.001]:
    print(x, math.sin(x) / x, math.sin(math.radians(x)) / x)
```

<details class="dl-answer"><summary>answer</summary>

In radians the limit is 1: for a tiny angle, the up value and the
distance walked round the circle are almost the same. In degrees it is
about 0.01745, which is $\frac{\pi}{180}$. Radians are the unit that
makes this limit 1, and that is one reason calculus uses them.

</details>
