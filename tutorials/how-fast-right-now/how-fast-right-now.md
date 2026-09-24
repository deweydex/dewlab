---
title: "How fast, right now? The derivative"
year: "2026-2027"
version: 2026.09.24.1
covers:
  distance-at-every-second:
    covers: [MIT-3.6]
    touches: [MIT-3.2]
  average-speed-over-a-chord:
    covers: [MIT-3.6]
    touches: [MIT-4.2, MIT-1.7]
  shrinking-the-chord:
    covers: [MIT-3.6]
    touches: [MIT-3.5, PDP-LO6]
  the-derivative-is-a-limit:
    covers: [MIT-3.6]
    touches: [MIT-3.5]
  a-tool-for-the-slope-at-a-point:
    covers: [MIT-3.6]
    touches: [PDP-LO8, PDP-LO10]
  why-the-step-cannot-be-0-or-too-small:
    covers: [MIT-3.6]
    touches: [MIT-1.4, PDP-LO9]
  the-tangent-line:
    covers: [MIT-3.6]
    touches: [MIT-4.1]
---

# How fast, right now? The derivative

A sprinter runs 100 metres in about 9.53 seconds. That is an average of
about 10.5 metres every second. But she was not running at 10.5 metres a
second the whole way: at the gun she was standing still. How fast was
she going exactly 3 seconds into the race? A car's speedometer answers
a question like this at every moment. What is it measuring?

On this page we:

- look at the sprinter's distance at every second, as a table and a
  curve
- find her average speed between two times, as the slope of a chord
- shrink the chord, and watch the average speeds settle
- name the number they settle on: the derivative
- add `derivative_at` to the toolkit, and see why its step is one
  millionth
- draw the tangent line, the straight line the curve looks like up close

> **The space we're in.** A rule that gives the sprinter's distance at
> any time, not only at whole seconds, in real numbers, with floats in
> the code. We can find the slope of a chord, from
> [Straight lines](tutorial:straight-lines), and a limit, from
> [Getting closer](tutorial:getting-closer). One thing usually goes
> unsaid: in a single instant, nobody moves at all. So "distance divided
> by time" at one instant is $\frac{0}{0}$, and this whole page is about
> that $\frac{0}{0}$.

## Warm-up

The first question is from
[Straight lines](tutorial:straight-lines#slope-between-any-two-points),
and the second from
[Getting closer](tutorial:getting-closer#when-the-two-sides-disagree).

```question
id: how-fast-warm-up-1
type: fill-in-the-blank

A line goes through $(1, 3)$ and $(3, 7)$. Its slope,
`slope((1, 3), (3, 7))`, is {2}.
```

```question
id: how-fast-warm-up-2
type: multiple-choice
correct: 3

The parking fee is €2 up to 1 hour and €5 for longer. It has a value
at 1 hour. Why does it have no limit there?

- Because a fee is not a real number.
- Because the rule has a hole at 1 hour.
- Because the left side heads for 2 and the right side heads for 5.
```

## Distance at every second

Here is a rule for the sprinter's distance, in metres, after a number
of seconds. It comes from a model of sprinting, in which a runner's
speed climbs quickly at first and then levels off near a top speed,
here 12 metres a second. The numbers are made up, but they are close
to a world-class 100 m.

The rule uses `math.exp(x)`, which is $e^x$: the number $e$ from
[Getting closer](tutorial:getting-closer#a-limit-at-infinity), to the
power $x$. You do not need to know why the rule has this shape. This
page is about what we can learn from a rule we cannot see inside.

```python exec
id: how-fast-distance-1
import math

def sprint_distance(seconds):
    """Return the sprinter's distance in metres, this many seconds after the gun."""
    return 12 * (seconds - 1.2 * (1 - math.exp(-seconds / 1.2)))

for second in range(11):
    print(second, round(sprint_distance(second), 2))
```

After 1 second she has run 3.86 m, after 3 seconds 22.78 m, and after
10 seconds 105.6 m. In the first second she covers 3.86 m. In the
seventh, from 6 to 7 seconds, she covers 11.94 m. So she is speeding
up. A picture shows how. What shape do you expect?

```python exec
id: how-fast-distance-2
import matplotlib.pyplot as plt

plot_rule(sprint_distance, 0, 10)
plt.xlabel("seconds after the gun")
plt.ylabel("metres run")
```

The curve starts flat and gets steeper, and after about 5 seconds it is
close to a straight line. On a graph of distance against time, a steep
part means many metres in each second: steep is fast.

## Average speed over a chord

How fast did she go between 3 and 5 seconds? On
[Running a formula backwards](tutorial:running-a-formula-backwards#one-formula-three-questions),
average speed was distance divided by time. On
[Straight lines](tutorial:straight-lines#slope-between-any-two-points),
slope was rise over run. On this graph, the rise is metres and the run
is seconds. So will `speed` and `slope`, both from your toolkit, give
the same number? Guess, then run it.

```python exec
id: how-fast-chord-1
start = (3, sprint_distance(3))
end = (5, sprint_distance(5))

print(speed(end[1] - start[1], end[0] - start[0]))
print(slope(start, end))

plot_rule(sprint_distance, 0, 6)
plt.plot([start[0], end[0]], [start[1], end[1]], marker="o")
```

Both give 11.52 metres a second. The straight line in the picture joins
two points of the curve. A straight line that joins two points of a
curve is a *chord*. Her average speed between 3 and 5 seconds is the
slope of the chord between them.

This works for any rule, not only distance. The slope of a chord is
the *average rate of change* of a rule between two inputs: how much the
output changes for each step of the input, on average over the chord.
Speed is the rate of change of distance.

But 11.52 is an average over two seconds, and she was speeding up the
whole time. It is not her speed at 3 seconds.

## Shrinking the chord

Let's keep one end of the chord at 3 seconds and bring the other end
closer, halving the step on each row, as
[Getting closer](tutorial:getting-closer#closer-from-both-sides) did.
The middle column is the chord from 3 to 3 + step. The last column is
the chord from 3 − step to 3, on the left. What will the columns do?

```python exec
id: how-fast-shrink-1
at = (3, sprint_distance(3))
step = 1
for row in range(10):
    right = (3 + step, sprint_distance(3 + step))
    left = (3 - step, sprint_distance(3 - step))
    print(step, slope(at, right), slope(left, at))
    step = step / 2
```

The right-hand chords fall, 11.33, 11.19, 11.11, and the left-hand
chords climb, 10.46, 10.78, 10.90. After ten rows they are 11.0158 and
11.0142. Both columns head for the same number, a little over 11.01.

Here are three of those chords on one picture. Before you run it,
think: as a chord gets shorter, what happens to its direction?

```python exec
id: how-fast-shrink-2
plot_rule(sprint_distance, 1, 5)
for step in [2, 1, 0.5]:
    plt.plot([3, 3 + step], [sprint_distance(3), sprint_distance(3 + step)], marker="o")
```

Each shorter chord is a little less steep than the one before, and the
turning gets smaller each time. The chords are settling on one
direction.

## The derivative is a limit

In words: her speed at 3 seconds is the limit of her average speeds
over shorter and shorter times that start at 3 seconds.

In symbols, maths names the step $h$. For a rule $f$ and a point $a$,
the chord from $a$ to $a + h$ has slope
$\frac{f(a + h) - f(a)}{h}$. Its limit, as $h$ gets close to 0, is the
*derivative* of $f$ at $a$, written $f'(a)$ and said "f prime of a":

$$f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h}$$

At $h = 0$ exactly, the fraction is $\frac{0}{0}$: a hole, like the
one on the last page. The derivative is the limit at that hole. It is
the slope of the curve at a single point.

Speed at one instant is an *instantaneous rate of change*: the rate of
change at a single moment, not averaged over a stretch of time. Every
derivative is one. So the sprinter's speed at 3 seconds, a little over
11.01 metres a second, is the derivative of her distance at 3. That is
what a speedometer shows. You will also meet the derivative written as
$\frac{dy}{dx}$, "the change in $y$ for a tiny change in $x$".

## A tool for the slope at a point

Look back at the table. The right-hand chords were too high, and the
left-hand ones too low. A chord from $a - h$ to $a + h$, centred on the
point, sits between the two. Here is the centred chord beside the
right-hand one, for two steps. Which do you expect to settle faster?

```python exec
id: how-fast-centred-1
for step in [0.1, 0.01]:
    right = (sprint_distance(3 + step) - sprint_distance(3)) / step
    centred = (sprint_distance(3 + step) - sprint_distance(3 - step)) / (2 * step)
    print(step, right, centred)
```

With a step of 0.1, the centred chord already gives 11.0138, closer
than the right-hand chord at a step of 0.01. The error on one side
mostly cancels the error on the other. In symbols, the centred chord
is

$$\frac{f(a + h) - f(a - h)}{2h}$$

and it has the same limit, the derivative. Now it becomes a tool. Here
is its promise; the body is yours to write.

```python exec
id: how-fast-toolkit
toolkit: yes
def derivative_at(rule, x, step=1e-6):
    """Return the slope of rule at x: the slope of a very short chord centred on x.

    The chord runs from x - step to x + step, so step must not be 0.
    For the rule x squared, derivative_at at 3 is about 6.
    """
    ...
```

```python toolkit-reference
for: how-fast-toolkit
def derivative_at(rule, x, step=1e-6):
    """Return the slope of rule at x: the slope of a very short chord centred on x.

    The chord runs from x - step to x + step, so step must not be 0.
    For the rule x squared, derivative_at at 3 is about 6.
    """
    return (rule(x + step) - rule(x - step)) / (2 * step)
```

The tests use slopes we already know. A straight line has the same
slope everywhere, like the taxi on
[Straight lines](tutorial:straight-lines#a-line-as-a-rule-y-mx-c). The
kicked ball on
[Drawing a rule](tutorial:drawing-a-rule#curves-that-bend-parabolas-and-cubics)
is at its top after 2 seconds, where for a moment it is going neither
up nor down. Until `derivative_at` is written, the first test stops
with a `TypeError`, because `...` gives back `None`.

```python exec
id: how-fast-toolkit-tests
def taxi(x):
    return 1.5 * x + 4

def ball_height(seconds):
    return 20 * seconds - 5 * seconds ** 2

def squared(x):
    return x ** 2

assert close_enough(derivative_at(taxi, 7), 1.5, tolerance=1e-6), "a line's slope"
assert close_enough(derivative_at(squared, 3), 6, tolerance=1e-6)
assert close_enough(derivative_at(ball_height, 2), 0, tolerance=1e-6), "the top"
assert 11.0142 < derivative_at(sprint_distance, 3) < 11.0158, "between the chords"
print("derivative_at keeps its promise:", derivative_at(sprint_distance, 3))
```

```hint
Try `print(derivative_at(squared, 3))` on its own. What came back?
Which two values of the rule does the centred chord subtract, and what
does it divide by?
```

<details class="dl-answer"><summary>answer</summary>

One line does it: the rise of the centred chord over its run, which is
two steps long.

```python
def derivative_at(rule, x, step=1e-6):
    """Return the slope of rule at x: the slope of a very short chord centred on x.

    The chord runs from x - step to x + step, so step must not be 0.
    For the rule x squared, derivative_at at 3 is about 6.
    """
    return (rule(x + step) - rule(x - step)) / (2 * step)
```

</details>

The sprinter's speed at 3 seconds is 11.01498 metres a second. The
tests use a tolerance of $10^{-6}$, not the usual $10^{-9}$: the next
section says why.

## Why the step cannot be 0, or too small

If you have not written `derivative_at` yet, open the answer under the
tests and copy it into the stub.

Why not take a step of 0, and get the exact slope? This cell is meant
to stop with an error.

```python exec
id: how-fast-step-1
print(derivative_at(sprint_distance, 3, step=0))
```

`ZeroDivisionError: float division by zero`. A chord of length 0 is a
single point, with a rise of 0 over a run of 0. That is the hole again,
and a computer cannot take a limit. It can only take a small step.

So why not a very small step, like $10^{-15}$? The model comes with a
speed rule of its own, $12(1 - e^{-t/1.2})$ metres a second. Let's take
it as the right answer, and measure how far out each step is. Where do
you expect the error to be smallest?

```python exec
id: how-fast-step-2
true_speed = 12 * (1 - math.exp(-3 / 1.2))
for power in range(1, 16):
    step = 10 ** -power
    error = derivative_at(sprint_distance, 3, step) - true_speed
    print(step, error)
```

The error shrinks, and then grows again. There are two kinds of error
here.

1. A long chord bends away from the curve. Each time the step gets 10
   times shorter, this error gets about 100 times smaller: $10^{-3}$ at
   a step of 0.1, $10^{-9}$ at $10^{-4}$.
2. A short chord subtracts two distances that are nearly the same.
   Each distance is a float, a tiny way off, as on
   [How a computer stores a number](tutorial:how-a-computer-stores-a-number#when-rounding-errors-add-up).
   Subtracting leaves only that tiny error, and dividing by a tiny
   $2h$ makes it large.

The first error falls as the step shrinks, and the second one rises.
They balance somewhere near $10^{-5}$ or $10^{-6}$. At $10^{-6}$ the
error is less than a billionth of a metre a second. At $10^{-15}$ the
answer is off by about 0.36, over 3%, which is
[Getting closer](tutorial:getting-closer#when-the-floats-run-out)
again: the floats have run out. So `derivative_at` uses $10^{-6}$ by
default. It is a good step for rules whose values are of ordinary
size, and a chord, not a limit, so its answer is close, not exact.

## The tangent line

The derivative is a slope, so it gives a straight line through the
point: the line through $(3, f(3))$ with slope $f'(3)$. As on
[Straight lines](tutorial:straight-lines#a-line-as-a-rule-y-mx-c),
$c = y_1 - m x_1$. What will this line look like beside the curve?

```python exec
id: how-fast-tangent-1
m = derivative_at(sprint_distance, 3)
c = sprint_distance(3) - m * 3

def tangent_at_3(seconds):
    return m * seconds + c

plot_rule(sprint_distance, 0, 6)
plot_rule(tangent_at_3, 0, 6)
plt.legend()
```

The straight line touches the curve at 3 seconds and runs along it,
with the curve bending away on each side. A straight line that touches
a curve at one point, with the same slope as the curve there, is the
*tangent line* at that point. The word is the same as the tangent,
$\tan\theta$, on
[Going round in circles](tutorial:going-round-in-circles#a-third-name-tangent),
but it names a different thing, like two people called Seán.

Now zoom in. The last page opened by asking what happens to a value as
you zoom in on it. Guess before you run it.

```python exec
id: how-fast-tangent-2
plot_rule(sprint_distance, 2.9, 3.1)
plot_rule(tangent_at_3, 2.9, 3.1)
plt.legend()
```

Close up, the curve and its tangent line look like one line. A smooth
curve, looked at closely enough, is nearly straight, and the derivative
is the slope of that nearly-straight piece.

### Your turn

1. Find the sprinter's speed at 1 second, and at 8 seconds. When is
   she speeding up fastest?
2. Draw the tangent line at 1 second, the way the cell above drew it at
   3.
3. The ball from the tests: find `derivative_at(ball_height, t)` for
   $t$ = 0, 1, 2, 3 and 4. What does a negative answer mean for the
   ball?

```python exec
id: how-fast-tangent-your-turn
# Your speeds, and your tangent line
```

<details class="dl-why"><summary>Why this way?</summary>

This page found a derivative as a number, from the slopes of shorter
and shorter chords, and gave you a tool that works it out for any
rule.

Most courses teach the rules for derivatives early: for $x^n$, the
derivative is $n x^{n-1}$, and so on. Then they practise using the
rules by hand. That route gives exact answers, quickly, with a pen, and
it is what exams usually ask for.

We started with chords because a derivative is a limit before it is a
rule, and a table of chords shows what the rules are shortcuts for.
The cost is that `derivative_at` is only close, never exact, and you
have waited a page for the rules.
[Rules for change](tutorial:rules-for-change) finds them, and checks
each one against your tool.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a chord and its slope; the step $h$; the derivative $f'(a)$; the tangent line, a new use of an old word |
| What is promised? | `derivative_at(rule, x)` promises the slope of a very short centred chord, close to the derivative |
| What happens when? | the chord shrinks one halving at a time, and its slopes settle; the error of the tool falls, then rises, as the step shrinks |
| What does this space let us do? | in the maths, the step shrinks to a limit; in floats, a step of 0 is a `ZeroDivisionError` and a step of $10^{-15}$ loses the answer |

## What we have now

| Term or tool | What it means |
|---|---|
| chord | a straight line that joins two points of a curve |
| average rate of change | the slope of a chord: how much the output changes for each step of the input, on average |
| derivative, $f'(a)$ | the limit of the chord slopes $\frac{f(a + h) - f(a)}{h}$ as $h$ gets close to 0: the slope of the curve at $a$ |
| instantaneous rate of change | the rate of change at a single moment; speed is the one for distance |
| centred chord, $\frac{f(a + h) - f(a - h)}{2h}$ | a chord centred on the point, which settles faster than a one-sided chord |
| `derivative_at(rule, x, step=1e-6)` | your toolkit tool: the slope of `rule` at `x`, from a centred chord |
| step size | too big bends away from the curve; too small loses the answer in the floats; $10^{-6}$ is a good middle |
| tangent line | the straight line that touches a curve at a point, with the same slope as the curve there |
| `math.exp(x)` | $e$ to the power $x$ |

The practice page is next. Then
[Rules for change](tutorial:rules-for-change) finds shortcuts for the
derivative, and checks each one with `derivative_at`.

## Where to read more

The dewlab page
[Derivatives: the rate of change of a curve](tutorial:rates-of-change),
from another course, meets the derivative as a slope and a speed, and
goes on to the rules.
