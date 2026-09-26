---
title: "Solving by computing: bisection and Newton's method — Practice"
practice_for: solving-by-computing
year: "2026-2027"
version: 2026.09.25.1
---

# Solving by computing: bisection and Newton's method — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `bisect_root` and
`newton` from the tutorial, `derivative_at` from
[How fast, right now?](tutorial:how-fast-right-now) and
`solve_quadratic` from [Solving for x](tutorial:solving-for-x).

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: solving-by-practice-warm-up
# Try things here
```

**1. Predict.** Bisection starts with a gap of 1 between `low` and
`high`. How many steps until the gap is smaller than 0.001? Use
$2^{10} \approx 1000$.

<details class="dl-answer"><summary>answer</summary>

It takes ten steps. After $k$ steps the gap is $\frac{1}{2^k}$, and
$2^{10} = 1024$, so after 10 steps the gap is $\frac{1}{1024}$, a
little under 0.001. After 9 steps it is $\frac{1}{512}$, which is
still bigger.

```python
import math
print(math.ceil(math.log2(1000)))
```

It prints `10`.

</details>

**2. Predict.** Newton's method is looking for $\sqrt{9}$, a root of
$x^2 - 9$, and starts at 4. What is its next guess? Find it by hand
with $g - \frac{f(g)}{f'(g)}$, using the slope $2x$.

<details class="dl-answer"><summary>answer</summary>

At 4, the rule gives $16 - 9 = 7$, and the slope is $2 \times 4 = 8$.
The next guess is $4 - \frac{7}{8} = 3.125$.

```python
def nine_gap(x):
    return x ** 2 - 9

print(newton(nine_gap, 4, steps=1))
```

It prints a number very close to `3.125`, because `newton` uses
`derivative_at`, an estimate of the slope.

</details>

**3. Make.** A small sensor for a weather station sits in a case shaped
like a cube, and the case must hold 50 cubic centimetres. How long is
each side? Use `newton`, and check with `50 ** (1 / 3)`.

<details class="dl-answer"><summary>answer</summary>

```python
def box_gap(side):
    return side ** 3 - 50

side = newton(box_gap, 4)
print(side, 50 ** (1 / 3), side ** 3)
```

Each side is about 3.684 cm. The two answers agree, and the side cubed
comes back to 50.

</details>

**4. Explain.** Schlomi, who is learning Python too, runs
`bisect_root(nine_gap, -5, 5)`, and it stops with a `ValueError`. She
says: "So $x^2 - 9$ has no root between $-5$ and 5." But it has two.
Where does her reading of the error stop working?

<details class="dl-answer"><summary>answer</summary>

At $-5$ and at 5 the rule gives 16, positive both times. There is no
sign change, so the promise of `bisect_root` cannot be kept, and it
says so. The curve goes down through zero at $-3$ and comes back up
through zero at 3, and the two crossings hide each other. A sign
change says "at least one root here". No sign change does not mean "no
root". Try `bisect_root(nine_gap, 0, 5)`: now there is a sign change,
and it finds 3.

This is one answer. Yours may use other words, or a picture, and say
the same thing.

</details>

## Core

A cell for the core problems.

```python exec
id: solving-by-practice-core
# Your working for problems 5 to 12
```

**5. Make.** On [Waves](tutorial:waves), each semitone on a piano
multiplies the frequency by the same number $r$, and 12 semitones make
an octave, which doubles it. So $r^{12} = 2$. Find $r$ with `newton`,
starting at 1, and check it against `2 ** (1 / 12)`.

<details class="dl-answer"><summary>answer</summary>

```python
def semitone_gap(ratio):
    return ratio ** 12 - 2

semitone = newton(semitone_gap, 1)
print(semitone, 2 ** (1 / 12))
print(440 * semitone)
```

Both give 1.0594630943592953. One semitone above A at 440 Hz is about
466.16 Hz.

</details>

**6. Fix.** Schlomo, who is learning Python too, wrote his own
bisection. It runs without an error, but the answer is far from
$\sqrt{2}$. Find the line that does not do what Schlomo meant, and
change it.

```python exec
id: solving-by-practice-fix
def two_gap(x):
    return x ** 2 - 2

low = 1
high = 2
while high - low > 1e-9:
    middle = (low + high) / 2
    if two_gap(low) * two_gap(middle) <= 0:
        low = middle
    else:
        high = middle
print((low + high) / 2)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Add a `print(low, high)` inside the loop, and look at the first few
   lines.
2. After the first step, is $\sqrt{2}$ still between `low` and `high`?
3. If the sign changes between `low` and `middle`, which half holds the
   root?

**Think about:** why did the loop still stop, if it lost the root?

</details>

<details class="dl-answer"><summary>answer</summary>

The two halves are swapped. When the sign changes between `low` and
`middle`, the root is in the left half, so `middle` must become the new
`high`:

```python
low = 1
high = 2
while high - low > 1e-9:
    middle = (low + high) / 2
    if two_gap(low) * two_gap(middle) <= 0:
        high = middle
    else:
        low = middle
print((low + high) / 2)
```

It prints `1.4142135619185865`. The broken version kept the half with
no root in it, and ended near 1.5. It still stopped,
because the gap halves at every step whichever half is kept. The loop
promises a small gap. Only the sign test promises the root is inside
it.

</details>

**7. Predict.** Bisection looks for $\sqrt{50}$ between 0 and 10, with a
tolerance of $10^{-6}$. How many steps will it take? Predict, then
count them with a counter inside the loop.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The gap starts at 10, and after $k$ steps it is $\frac{10}{2^k}$.
2. You want $\frac{10}{2^k} \leq 10^{-6}$, so $2^k \geq 10^7$.
3. $10^7$ is ten million. How many doublings is that?

</details>

<details class="dl-answer"><summary>answer</summary>

$2^{23}$ is about 8.4 million and $2^{24}$ is about 16.8 million, so
it takes 24 steps.

```python
low = 0
high = 10
steps_taken = 0
while high - low > 1e-6:
    middle = (low + high) / 2
    if (low ** 2 - 50) * (middle ** 2 - 50) <= 0:
        high = middle
    else:
        low = middle
    steps_taken = steps_taken + 1
print(steps_taken, (low + high) / 2)
```

It prints `24` and about 7.0710678. A wider start costs only a few more
steps. Ten times the width needs about 3.3 more halvings.

</details>

**8. Make.** A sliotar is struck from 1.5 m up. Its height after $t$
seconds is $1.5 + 12t - 4.9t^2$ metres. When does it land? Find it with
`bisect_root`, and check with `solve_quadratic`.

<details class="dl-answer"><summary>answer</summary>

At $t = 1$ the height is 8.6 m, and at $t = 5$ it is $-61$ m, below the
ground, so there is a sign change between 1 and 5.

```python
def sliotar_height(seconds):
    return 1.5 + 12 * seconds - 4.9 * seconds ** 2

print(bisect_root(sliotar_height, 1, 5))
print(solve_quadratic(-4.9, 12, 1.5))
```

It lands after about 2.57 seconds. `solve_quadratic` gives the same
root, and a second one, about $-0.12$, before the sliotar was struck.
Bisection only found the one inside the gap we gave it.

</details>

**9. Another way.** Newton's method for $\sqrt{2}$ can use the exact
slope, $2x$, from
[Rules for change](tutorial:rules-for-change#a-pattern-in-the-slopes-the-power-rule),
in place of `derivative_at`. Write the loop that way, for 6 steps from
1. Then write the step as "the average of $g$ and $\frac{2}{g}$". Do
all three agree?

<details class="dl-answer"><summary>answer</summary>

$g - \frac{g^2 - 2}{2g} = g - \frac{g}{2} + \frac{1}{g} = \frac{1}{2}\left(g + \frac{2}{g}\right)$,
the average of $g$ and $\frac{2}{g}$.

```python
def two_gap(x):
    return x ** 2 - 2

exact = 1
average = 1
for step in range(6):
    exact = exact - (exact ** 2 - 2) / (2 * exact)
    average = (average + 2 / average) / 2
print(exact, average, newton(two_gap, 1))
```

All three give 1.414213562373095. The exact
slope saves two calls of the rule at every step.

</details>

**10. Explain.** Run Newton's method on $x^3 - 2x + 2$, starting at 0,
and print each guess. What happens? Why?

```python
def stuck_rule(x):
    return x ** 3 - 2 * x + 2

guess = 0
for step in range(6):
    print(step, guess)
    guess = guess - stuck_rule(guess) / derivative_at(stuck_rule, guess)
```

<details class="dl-answer"><summary>answer</summary>

The guesses go 0, 1, 0, 1, 0, 1 (to within a tiny float error), for
ever. At 0 the rule gives 2 and the slope is $-2$, so the tangent
leads to $0 - \frac{2}{-2} = 1$. At 1 the rule gives 1 and the slope is
1, so the tangent leads to $1 - 1 = 0$. Each tangent points back at
the other guess.

No error appears, and `newton` would return a number, about 0, after
20 steps. So put an answer back into the rule to check it.
`stuck_rule(0)` is 2, not 0. The real root is near $-1.77$. A start
at $-2$ finds it.

</details>

**11. Make.** Ireland's population was 4,761,865 at the 2016 census and
5,149,139 at the 2022 census. If it grew by the same rate $r$ each
year, then $(1 + r)^6 = \frac{5149139}{4761865}$. Find $r$ with
`bisect_root`, between 0 and 0.1, and say it as a percentage.

<details class="dl-answer"><summary>answer</summary>

```python
def growth_gap(rate):
    return (1 + rate) ** 6 - 5149139 / 4761865

rate = bisect_root(growth_gap, 0, 0.1)
print(rate, round(rate * 100, 2))
print(4761865 * (1 + rate) ** 6)
```

The rate is about 0.0131, or 1.31% a year. Put it back in, and you get
5,149,139 again, to within a small fraction of a person.

</details>

**12. Another way.** On
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
server A answered in $8 + 2x$ ms with $x$ thousand people using an
app, and server B in 20 ms. Find where they are equally fast with
`bisect_root`, by looking for a root of the difference between them.
Compare with `solve_linear`.

<details class="dl-answer"><summary>answer</summary>

The servers are equally fast where server A minus server B is 0:
$2x - 12 = 0$.

```python
def server_difference(thousands):
    return (8 + 2 * thousands) - 20

print(bisect_root(server_difference, 0, 10))
print(solve_linear(2, -12))
```

Both give 6 thousand people (bisection to within a billionth). Any "where are
two rules equal?" question becomes a root question this way.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: solving-by-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** Where will Mars be in its orbit next month?
Astronomers answer that with Kepler's equation,
$E - e\sin E = M$. Here $M$ is how far round Mars would be if it
moved at a steady speed, $e$ says how far its orbit is from a circle,
and $E$ is an angle that fixes where Mars really is. All three are in
radians, and for Mars $e$ is about 0.0934. Nobody has found a formula
for $E$. Find $E$ when $M = 1$ with `bisect_root`, then check it with
`newton`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write a rule of $E$ that returns $E - 0.0934 \sin E - 1$. It is
   0 at the answer.
2. Try it at 0 and at 2. Is there a sign change?
3. Give those two as `low` and `high`.

**Think about:** $e$ is small, so $E$ is close to $M$. Why?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import math

def kepler_gap(angle):
    return angle - 0.0934 * math.sin(angle) - 1

print(kepler_gap(0), kepler_gap(2))
print(bisect_root(kepler_gap, 0, 2))
print(newton(kepler_gap, 1))
```

The rule is $-1$ at 0 and about 0.92 at 2, so there is a sign change.
Both methods give $E \approx 1.0825$ radians. Mars is a little ahead of
where a steady speed would put it. $E$ is close to $M$ because the
$e \sin E$ part is never bigger than 0.0934. Mars's orbit is nearly a
circle. Programs that track planets and satellites solve this
equation again and again, often with Newton's method.

</details>

**14. Make.** On
[Rules for change](tutorial:rules-for-change#back-to-the-top-of-the-curve),
a box made from card 30 cm across had the volume $x(30 - 2x)^2$, and
its slope was $(30 - 2x)(30 - 6x)$. The biggest box is where the slope
is 0. Find it with `newton` from 3, and with `bisect_root` between 0
and 10. Then try `newton` from 12. What changes?

<details class="dl-answer"><summary>answer</summary>

```python
def box_slope(cut):
    return (30 - 2 * cut) * (30 - 6 * cut)

print(newton(box_slope, 3))
print(bisect_root(box_slope, 0, 10))
print(newton(box_slope, 12))
```

From 3, Newton's method finds 5, and bisection agrees, at 5 cm from each
corner. From 12, Newton's method finds 15, the other place where the
slope is 0. That one is the box with no base, a bottom of the volume
curve, not its top. A root of the slope is a place where the curve is
flat. It is still your job to ask whether it is a top or a bottom.

</details>

**15. Explain.** Some computer chips divide by using Newton's method.
To find $\frac{1}{3}$, they look for the root of $\frac{1}{x} - 3$, and
the Newton step for that rule simplifies to $2g - 3g^2$, which needs no
division at all. Try it from 0.3, and then from 1. What happens, and
why?

```python
guess = 0.3
for step in range(5):
    guess = 2 * guess - 3 * guess ** 2
    print(guess)
```

<details class="dl-answer"><summary>answer</summary>

From 0.3 the guesses go about 0.33, 0.3333, 0.33333333, and then
0.3333333333333333. The correct digits double every step.

From 1 they go $-1$, $-5$, $-85$, $-21845$, running away. The graph of
$\frac{1}{x} - 3$ has a gap at 0. From 1, the tangent is gentle, and
when we follow it down to zero, we cross to the far side of the gap, where
the curve never comes back to zero. A start between 0 and
$\frac{2}{3}$ stays on the right side. So a chip that divides this way
needs a first guess close enough, which it gets from a small table.

</details>

<aside class="dl-note" id="solving-by-practice-note-quake">

**A famous line in a game.** The game Quake III Arena, from 1999,
needed $\frac{1}{\sqrt{x}}$ many times a second, for its lighting. Its
code makes a rough first guess with a strange number, `0x5f3759df`,
and then takes one Newton step, which needs no division. One step
brings the answer within about 0.2% of the true value.

</aside>

## Where to read more

Stand-up Maths (2018). *How to find a square root.*
<https://www.youtube.com/watch?v=Bwt5EZEb1Ns>. Matt Parker finds a square
root by hand, the way people did before calculators. Which of this page's
two methods is his closest to? About six minutes.
