---
title: "How fast, right now? The derivative"
year: "2026-2027"
version: 2026.09.25.1
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

A hailstone about a centimetre across hits the ground at about 12
metres a second, a little over 40 km/h. But the moment it starts to
fall, it is barely moving. So here is a question that sounds simple:
how fast is it falling exactly 3 seconds after it starts? Not on
average. Right then.

Stop on that "right then" for a moment. Speed is distance divided by
time, and in a single instant the stone moves no distance, in no time.
So what can "its speed right now" even mean? Some weather radars
measure exactly that number. This page finds out what they measure.

On this page we:

- look at the hailstone's fall at every second, as a table and a curve
- find its average speed between two times, as the slope of a chord
- shrink the chord, and watch the average speeds settle
- name the number they settle on: the derivative
- add `derivative_at` to the toolkit, and see why its step is one
  millionth
- draw the tangent line, the straight line the curve looks like up close

> **The space we're in.** A rule that gives the distance fallen at any
> time, not only at whole seconds, in real numbers, with floats in the
> code. We can find the slope of a chord, from
> [Straight lines](tutorial:straight-lines), and a limit, from
> [Getting closer](tutorial:getting-closer). One thing usually goes
> unsaid: in a single instant, nothing moves at all. So "distance
> divided by time" at one instant is $\frac{0}{0}$, and this whole page
> is about that $\frac{0}{0}$.

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
answer: 3

Across the edge of a black square on a white screen, the brightness is
0 up to the edge and 255 after it. It has a value at the edge. Why does
it have no limit there?

- Because a brightness is not a real number.
  - A brightness from 0 to 255 is a real number; the trouble is at the edge, not in the numbers.
- Because the rule has a hole at the edge.
  - A hole is a missing value, and this rule has a value at the edge.
- Because the left side heads for 0 and the right side heads for 255.
  - A limit needs both sides to head for the same number, and these two head for 0 and 255.
```

## Distance at every second

A falling hailstone is pulled down by its weight and pushed up by the
air. That push is *air resistance*, and it grows as the stone goes
faster. In time the push is as big as the weight, and the stone stops
speeding up. The speed it settles at is its *terminal speed*.

Here is a rule for the distance, in metres, that the hailstone has
fallen after a number of seconds. It comes from the simplest model of
air resistance, where the push is proportional to the speed. Real air
pushes in a more complicated way, so this is a model. In it, the
terminal speed is 12 metres a second, and at the start the stone
speeds up by 10 metres a second every second, close to gravity alone.

The rule uses `math.exp(x)`, which is $e^x$: the number $e$ from
[Getting closer](tutorial:getting-closer#a-limit-at-infinity), to the
power $x$. You do not need to know why the rule has this shape. This
page is about what we can learn from a rule we cannot see inside.

```python exec
id: how-fast-distance-1
import math

def fall_distance(seconds):
    """Return how far the hailstone has fallen, in metres, this many seconds after it starts."""
    return 12 * (seconds - 1.2 * (1 - math.exp(-seconds / 1.2)))

for second in range(11):
    print(second, round(fall_distance(second), 2))
```

In the first second it falls 3.86 m. In the seventh, from 6 to 7
seconds, it falls 11.94 m. So it is speeding up. A picture shows how.
What shape do you expect?

```python exec
id: how-fast-distance-2
import matplotlib.pyplot as plt

plot_rule(fall_distance, 0, 10)
plt.xlabel("seconds after it starts to fall")
plt.ylabel("metres fallen")
```

The curve starts flat and gets steeper, and after about 5 seconds it is
close to a straight line. On a graph of distance against time, a steep
part means many metres in each second: steep is fast.

<aside class="dl-note" id="how-fast-note-hail">

**How fast does hail fall?** Measurements of real hailstones
(Heymsfield and colleagues, 2014) give about 12 metres a second for a
stone 1 cm across, and about 20 for one 2.5 cm across. Raindrops are
slower: even the largest fall at about 9 metres a second.

</aside>

## Average speed over a chord

How fast did it fall between 3 and 5 seconds? On
[Running a formula backwards](tutorial:running-a-formula-backwards#one-formula-three-questions),
average speed was distance divided by time. On
[Straight lines](tutorial:straight-lines#slope-between-any-two-points),
slope was rise over run. On this graph, the rise is metres and the run
is seconds. So will `speed` and `slope`, both from your toolkit, give
the same number? Guess, then run it.

```python exec
id: how-fast-chord-1
start = (3, fall_distance(3))
end = (5, fall_distance(5))

print(speed(end[1] - start[1], end[0] - start[0]))
print(slope(start, end))

plot_rule(fall_distance, 0, 6)
plt.plot([start[0], end[0]], [start[1], end[1]], marker="o")
```

Both give 11.52 metres a second. The straight line in the picture joins
two points of the curve. A straight line that joins two points of a
curve is a *chord*. The stone's average speed between 3 and 5 seconds
is the slope of the chord between them.

This works for any rule, not only distance. The slope of a chord is
the *average rate of change* of a rule between two inputs: how much the
output changes for each step of the input, on average over the chord.
Speed is the rate of change of distance.

But 11.52 is an average over two seconds, and the stone was speeding up
the whole time. It is not its speed at 3 seconds.

## Shrinking the chord

Let's keep one end of the chord at 3 seconds and bring the other end
closer, halving the step on each row, as
[Getting closer](tutorial:getting-closer#closer-from-both-sides) did.
The middle column is the chord from 3 to 3 + step. The last column is
the chord from 3 − step to 3, on the left. What will the columns do?

```python exec
id: how-fast-shrink-1
at = (3, fall_distance(3))
step = 1
for row in range(10):
    right = (3 + step, fall_distance(3 + step))
    left = (3 - step, fall_distance(3 - step))
    print(step, slope(at, right), slope(left, at))
    step = step / 2
```

The right-hand chords fall, 11.33, 11.19, 11.11, and the left-hand
chords climb, 10.46, 10.78, 10.90. After ten rows they are 11.0158 and
11.0142. Both columns head for the same number, a little over 11.01.

Now watch it happen. In this short animation, the left side shows the
stone at 3 seconds and at 3 + step. The right side shows the chord
between those two moments. Each frame makes the step shorter. Before
you run it: as the chord gets shorter, what happens to its direction?

```python exec
id: how-fast-shrink-2
from matplotlib.animation import FuncAnimation

figure, (column, graph) = plt.subplots(1, 2, figsize=(5, 2.5), gridspec_kw={"width_ratios": [1, 3]})
column.set_xlim(-1, 1)
column.set_ylim(60, 0)                     # 0 m at the top, falling downwards
column.set_xticks([])
column.set_ylabel("metres fallen")
column.plot([0], [fall_distance(3)], "o", color="grey")
stone_later, = column.plot([0], [0], "o", color="C0")

times = [t / 10 for t in range(0, 61)]
graph.plot(times, [fall_distance(t) for t in times], color="grey")
chord_line, = graph.plot([], [], color="C0")
ends, = graph.plot([], [], "o", color="C0")
graph.set_ylim(0, 60)
graph.set_xlabel("seconds")

def draw_frame(frame):
    step = 2.5 * 0.75 ** frame             # each frame, the step is a quarter shorter
    later = 3 + step
    chord_slope = slope((3, fall_distance(3)), (later, fall_distance(later)))
    stone_later.set_data([0], [fall_distance(later)])
    ends.set_data([3, later], [fall_distance(3), fall_distance(later)])
    chord_line.set_data([0, 6], [fall_distance(3) - 3 * chord_slope, fall_distance(3) + 3 * chord_slope])
    graph.set_title(f"step {step:.3f} s, slope {chord_slope:.3f}", fontsize=9)

FuncAnimation(figure, draw_frame, frames=24, interval=250)
```

As the second stone moves up towards the first, the two ends of the
chord close in. The blue line through them is drawn long, so you can
see its direction: it turns a little less on each frame, and settles.
The slope above the graph falls to about 11.02. The animation loops;
run the cell again to watch it from the start.

## The derivative is a limit

In words: the stone's speed at 3 seconds is the limit of its average
speeds over shorter and shorter times that start at 3 seconds.

In symbols, maths names the step $h$. For a rule $f$ and a point $a$,
the chord from $a$ to $a + h$ has slope
$\frac{f(a + h) - f(a)}{h}$. Its limit, as $h$ gets close to 0, is the
*derivative* of $f$ at $a$, written $f'(a)$ and said "f prime of a":

$$f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h}$$

At $h = 0$ exactly, the fraction is $\frac{0}{0}$: a hole, like the
one on the last page. The derivative is the limit at that hole: the
slope of the curve at a single point. That is what "its speed right
now" means. I think it is a lovely answer to a question that looked
impossible.

Speed at one instant is an *instantaneous rate of change*: the rate of
change at a single moment, not averaged over a stretch of time. Every
derivative is one. The hailstone's speed at 3 seconds, a little over
11.01 metres a second, is the derivative of its distance at 3. You will
also see the derivative written $\frac{dy}{dx}$.

A weather radar that measures fall speed does not divide a distance by
a time. It sends out radio waves. A wave that bounces off a moving
hailstone comes back with its frequency changed a little, by an amount
that depends on how fast the stone moves along the beam. This is the
*Doppler effect*. A radar pointing straight up reads the fall speed
from its echo, over a tiny moment: the derivative, measured.

<aside class="dl-note" id="how-fast-note-doppler">

**Christian Doppler.** The effect is named after the Austrian
physicist Christian Doppler, who described it in 1842. You hear it
when an ambulance passes: its siren sounds higher as it comes towards
you and lower as it goes away.

</aside>

## A tool for the slope at a point

Look back at the table. The right-hand chords were too high, and the
left-hand ones too low. A chord from $a - h$ to $a + h$, centred on the
point, sits between the two. Here is the centred chord beside the
right-hand one, for two steps. Which do you expect to settle faster?

```python exec
id: how-fast-centred-1
for step in [0.1, 0.01]:
    right = (fall_distance(3 + step) - fall_distance(3)) / step
    centred = (fall_distance(3 + step) - fall_distance(3 - step)) / (2 * step)
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
slope everywhere, as on
[Straight lines](tutorial:straight-lines#a-line-as-a-rule-y-mx-c). The
kicked ball on
[Drawing a rule](tutorial:drawing-a-rule#curves-that-bend-parabolas-and-cubics)
is at its top after 2 seconds, where for a moment it is going neither
up nor down. Until `derivative_at` is written, the first test stops
with a `TypeError`, because `...` gives back `None`.

```python exec
id: how-fast-toolkit-tests
def straight_line(x):
    return 1.5 * x + 4

def ball_height(seconds):
    return 20 * seconds - 5 * seconds ** 2

def squared(x):
    return x ** 2

assert close_enough(derivative_at(straight_line, 7), 1.5, tolerance=1e-6), "a line's slope"
assert close_enough(derivative_at(squared, 3), 6, tolerance=1e-6)
assert close_enough(derivative_at(ball_height, 2), 0, tolerance=1e-6), "the top"
assert 11.0142 < derivative_at(fall_distance, 3) < 11.0158, "between the chords"
print("derivative_at keeps its promise:", derivative_at(fall_distance, 3))
```

```hint
Try `print(derivative_at(squared, 3))` on its own. What came back?
Which two values of the rule does the centred chord subtract, and what
does it divide by?
```

<details class="dl-answer"><summary>answer</summary>

Here is one way through. One line does it: the rise of the centred chord
over its run, which is two steps long.

```python
def derivative_at(rule, x, step=1e-6):
    """Return the slope of rule at x: the slope of a very short chord centred on x.

    The chord runs from x - step to x + step, so step must not be 0.
    For the rule x squared, derivative_at at 3 is about 6.
    """
    return (rule(x + step) - rule(x - step)) / (2 * step)
```

</details>

The hailstone's speed at 3 seconds is 11.01498 metres a second. The
tests use a tolerance of $10^{-6}$, not the usual $10^{-9}$: the next
section says why.

## Why the step cannot be 0, or too small

If you have not written `derivative_at` yet, open the answer under the
tests and copy it into the stub.

Why not take a step of 0, and get the exact slope? This cell is meant
to stop with an error.

```python exec
id: how-fast-step-1
print(derivative_at(fall_distance, 3, step=0))
```

`ZeroDivisionError: float division by zero`. A chord of length 0 is a
single point, with a rise of 0 over a run of 0. That is the hole again,
and a computer cannot take a limit. It can only take a small step.

So why not a very small step, like $10^{-15}$? The model comes with a
speed rule of its own, $12(1 - e^{-t/1.2})$ metres a second. Let's take
it as the true slope, and measure how far out each step is. Where do
you expect the error to be smallest?

```python exec
id: how-fast-step-2
true_speed = 12 * (1 - math.exp(-3 / 1.2))
for power in range(1, 16):
    step = 10 ** -power
    error = derivative_at(fall_distance, 3, step) - true_speed
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
m = derivative_at(fall_distance, 3)
c = fall_distance(3) - m * 3

def tangent_at_3(seconds):
    return m * seconds + c

plot_rule(fall_distance, 0, 6)
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
plot_rule(fall_distance, 2.9, 3.1)
plot_rule(tangent_at_3, 2.9, 3.1)
plt.legend()
```

Close up, the curve and its tangent line look like one line. A smooth
curve, looked at closely enough, is nearly straight, and the derivative
is the slope of that nearly-straight piece.

### Your turn

1. Find the hailstone's speed at 1 second, and at 8 seconds. When is
   it speeding up fastest?
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
| air resistance, terminal speed | the push of the air on a falling thing; the speed where that push balances its weight |
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

3Blue1Brown (2017). *The paradox of the derivative: Chapter 2, Essence of
calculus.* <https://www.youtube.com/watch?v=9vKqVkMQHKk>. What can "speed
at one moment" mean, when speed needs two moments to measure? Grant
Sanderson answers with a step that shrinks, the idea this page uses. About
seventeen minutes.
