---
title: "How fast, right now? The derivative — Practice"
practice_for: how-fast-right-now
year: "2026-2027"
version: 2026.09.25.1
datasets: [co2-emissions]
---

# How fast, right now? The derivative — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `derivative_at` from the
tutorial, `slope` and `line_through` from
[Straight lines](tutorial:straight-lines), `speed` from
[Running a formula backwards](tutorial:running-a-formula-backwards),
`plot_rule` and `close_enough`. The first cell below brings back the
falling hailstone and two small rules. Run it first.

## Warm-up

```python exec
id: how-fast-practice-warm-up
import math
import matplotlib.pyplot as plt

def fall_distance(seconds):
    """Return how far the hailstone has fallen, in metres, this many seconds after it starts."""
    return 12 * (seconds - 1.2 * (1 - math.exp(-seconds / 1.2)))

def squared(x):
    return x ** 2

def straight_line(x):
    return 1.5 * x + 4

# Try things here
```

**1. Predict.** What does this print? It is the slope of a chord of the
curve $y = x^2$.

```python
print(slope((1, squared(1)), (3, squared(3))))
```

<details class="dl-answer"><summary>answer</summary>

`4.0`. The chord joins $(1, 1)$ and $(3, 9)$. Its rise is $9 - 1 = 8$
and its run is $3 - 1 = 2$, so its slope is 4. That is the average rate
of change of $x^2$ between 1 and 3.

</details>

**2. Make.** A GPS logger rides on a coach that leaves Dublin at 10:00.
The log says that at 10:30 the coach has gone 40 km, and at 11:30 it
has gone 125 km. (The log is made up.) What was its average speed
between 10:30 and 11:30, in km/h? Find it with `speed`, and again as
the slope of a chord with time in hours.

<details class="dl-answer"><summary>answer</summary>

```python
print(speed(125 - 40, 1.0))
print(slope((0.5, 40), (1.5, 125)))
```

Both give 85 km/h. The chord runs from half an hour after 10:00 to an
hour and a half after, so the run is 1 hour and the rise is 85 km.

</details>

**3. Explain.** Schlomo, who is learning Python too, wants the exact
slope, not a close one. So he tries `derivative_at(straight_line, 2,
step=0)`. It stops with an error. Why? What does the derivative do
instead of taking a step of 0?

<details class="dl-answer"><summary>answer</summary>

With a step of 0, the chord runs from 2 to 2: a single point. Its rise
is 0 and its run is 0, so the slope is $\frac{0}{0}$, and Python raises
a `ZeroDivisionError`. The derivative never takes a step of 0. It is
the limit of the chord slopes as the step gets close to 0, the number
they head for. `derivative_at` cannot take a limit, so it takes one
small step, $10^{-6}$, and gives a number very close to the limit.

That is one good way to say it. Yours may use other words, or a
picture, and be as good.

</details>

**4. Predict.** What do these print? The first rule is the straight
line from the warm-up cell, and the second is a phone plan that costs
€20 whatever you use, as on
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet).

```python
def plan_b(gigabytes):
    return 20

print(derivative_at(straight_line, 100))
print(derivative_at(plan_b, 5))
```

<details class="dl-answer"><summary>answer</summary>

About 1.5, printed as 1.499999996212864, and exactly 0.0.

A straight line has the same slope everywhere, so its derivative is
its slope at every point: the line climbs 1.5 for each step of 1. The
tiny difference from 1.5 is float rounding. A flat rule never changes,
so its rate of change is 0: one more gigabyte costs nothing more.

</details>

## Core

A cell for the core problems.

```python exec
id: how-fast-practice-core
# Your working for problems 5 to 12
```

**5. Make.** A cup of tea is poured at 90 °C into a room at 20 °C. A
model for its temperature, after some minutes, is
$20 + 70e^{-t/10}$. This shape is Newton's law of cooling, a real law
of physics: the hotter the tea is than the room, the faster it cools.
(The 10 is made up; a real cup depends on the cup.)
Write it as a function and find its rate of change at 0 minutes and at
10 minutes. What does the sign of the answer mean?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write `def tea(minutes):` giving back
   `20 + 70 * math.exp(-minutes / 10)`.
2. Call `derivative_at(tea, 0)` and `derivative_at(tea, 10)`.
3. The answers are in °C per minute.

**Think about:** what would a rate of change of 0 mean for the tea?

**Try this next:** at what time is the tea cooling at 1 °C a minute?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def tea(minutes):
    return 20 + 70 * math.exp(-minutes / 10)

print(derivative_at(tea, 0))
print(derivative_at(tea, 10))
```

About $-7.0$ °C a minute at the start, and about $-2.58$ °C a minute
after 10 minutes. The minus sign means the temperature is falling: the
tea is cooling. It cools fastest when it is hottest, and more slowly as
it gets close to the room's 20 °C.

</details>

**6. Fix.** Schlomi, who is learning Python too, wrote her own
`derivative_at`. Run the cell, see which test fails, and fix the one
mistake.

```python exec
id: how-fast-practice-fix
def derivative_again(rule, x, step=1e-6):
    """Return the slope of rule at x: the slope of a very short chord centred on x."""
    return (rule(x + step) - rule(x - step)) / step

assert close_enough(derivative_again(straight_line, 0), 1.5, tolerance=1e-6), "a line"
print("derivative_again keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The test fails, because `derivative_again(straight_line, 0)` gives about 3, twice
the right answer. The chord runs from `x - step` to `x + step`, so its
run is two steps, not one. The fix is to divide by `2 * step`:

```python
    return (rule(x + step) - rule(x - step)) / (2 * step)
```

A test on a straight line catches this, because the right answer, the
line's slope, is known exactly.

</details>

**7. Predict.** The tutorial said a big step bends away from the curve.
What do you expect from these two lines, with steps of 1 and 0.5?

```python
print(derivative_at(squared, 3, step=1))
print(derivative_at(squared, 3, step=0.5))
```

<details class="dl-answer"><summary>answer</summary>

Both print `6.0`, the exact slope, even with a long chord. For $x^2$,
the centred chord from $3 - h$ to $3 + h$ has slope

$$\frac{(3 + h)^2 - (3 - h)^2}{2h} = \frac{12h}{2h} = 6$$

for every $h$. The $h^2$ parts cancel. So for a parabola, the error of
a long centred chord is 0. For a curve like the hailstone's, the errors
on the two sides only mostly cancel, and a short step is still needed.

</details>

**8. Another way.** The ball's height is $20t - 5t^2$ metres. Find its
speed at $t = 1$ with `derivative_at`. Then find it with algebra: work
out $\frac{f(1 + h) - f(1)}{h}$ with letters, and let $h$ get close to
0.

<details class="dl-answer"><summary>answer</summary>

```python
def ball_height(seconds):
    return 20 * seconds - 5 * seconds ** 2

print(derivative_at(ball_height, 1))
```

About 10 metres a second. With algebra, $f(1) = 15$, and

$$f(1 + h) = 20 + 20h - 5(1 + 2h + h^2) = 15 + 10h - 5h^2$$

so $\frac{f(1 + h) - f(1)}{h} = \frac{10h - 5h^2}{h} = 10 - 5h$. As
$h$ gets close to 0, this gets close to 10. The algebra gives the exact
limit. The tool gives a number very close to it, and checks the
algebra.

</details>

**9. Make.** Ireland's carbon dioxide emissions, in millions of tonnes
a year, are in `co2-emissions.csv`, as on
[Doubling and halving](tutorial:doubling-and-halving#doubling-in-real-data).
Find the average rate of change from 1990 to 2000, and from 2010 to
2020, in millions of tonnes per year.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Load the file and keep Ireland's rows, as on Doubling and halving.
2. Make a dictionary from each year to its emissions:
   `dict(zip(years, emissions))`.
3. Each average rate of change is the slope of a chord:
   `slope((1990, co2[1990]), (2000, co2[2000]))`.

**Think about:** what would a rate of change of 0 mean here?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
df = await load_csv("co2-emissions.csv")
ireland = df[df.country == "Ireland"]
co2 = dict(zip(ireland["year"].tolist(), ireland["co2"].tolist()))

print(slope((1990, co2[1990]), (2000, co2[2000])))
print(slope((2010, co2[2010]), (2020, co2[2020])))
```

From 1990 to 2000, emissions rose by about 1.23 million tonnes a year,
from 32.9 to 45.3. From 2010 to 2020, they fell by about 0.67 million
tonnes a year, from 41.8 to 35.1. Real data has no rule to put into
`derivative_at`, so a chord between two measurements is the rate of
change we can find.

</details>

**10. Make.** Use the tangent line to the tea's curve at 10 minutes to
estimate its temperature at 12 minutes. Then compare with the rule
itself.

<details class="dl-answer"><summary>answer</summary>

```python
m = derivative_at(tea, 10)
c = tea(10) - m * 10
print(m * 12 + c)
print(tea(12))
```

The tangent line gives about 40.6 °C, and the rule gives about
41.1 °C. Two minutes on, the tangent line is still close, but a little
low: the curve bends up away from it, because the tea cools more slowly
as time goes on. A tangent line is a good guess close to its point, and
a worse one further away.

</details>

**11. Predict.** On [Waves](tutorial:waves), a sound was a sine wave.
What is the slope of $\sin x$ at $x = 0$, and at the top of the wave,
$x = \frac{\pi}{2}$? Predict, then run it.

```python
print(derivative_at(math.sin, 0))
print(derivative_at(math.sin, math.pi / 2))
```

<details class="dl-answer"><summary>answer</summary>

About 1, and exactly 0.0. At 0, the sine wave rises through the axis
with slope 1, the same slope as the line $y = x$. At
$\frac{\pi}{2}$, the wave is at its top, and for a moment it goes
neither up nor down, like the ball at its highest point. `math.sin`
is a rule like any other, so `derivative_at` takes it with no `def`.

</details>

**12. Explain.** This course met the derivative as the limit of chord
slopes, and gave you a tool before any rules. Many courses give the
rules first, such as "the derivative of $x^n$ is $n x^{n-1}$", and
practise them by hand. If you were teaching a friend, which way would
you choose, and why?

<details class="dl-answer"><summary>answer</summary>

There is no single right answer. A good answer weighs a few things:

- **Speed and exams.** Rules first gets to exact answers quickly, and
  exams usually ask for them.
- **Meaning.** Chords first shows what a derivative is, a slope and a
  rate of change, so a rule has something to be a shortcut for.
- **Checking.** A tool like `derivative_at` can check a rule, and a
  rule can check the tool. Either order can use both.
- **Who the friend is.** Someone who needs a result for next week's
  test may want the rules. Someone who has always been told maths is
  rules to follow may need to see where the rules come from.

Whichever you choose, say what it costs. That is the question the
tutorial's "Why this way?" fold asks of itself.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: how-fast-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** The hailstone's terminal speed in this model is 12
metres a second. At what time, to the nearest hundredth of a second,
does it first reach 11.9 metres a second? Search with a loop, as the
fine comb did on
[The top of the curve](tutorial:the-top-of-the-curve#checking-with-a-fine-comb).

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start `time_now` at 0.
2. While `derivative_at(fall_distance, time_now)` is less than 11.9,
   add 0.01 to `time_now`.
3. Round the time as you go, so that float errors do not pile up.

**Think about:** could it ever reach 12 metres a second?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
time_now = 0
while derivative_at(fall_distance, time_now) < 11.9:
    time_now = round(time_now + 0.01, 2)
print(time_now)
```

5.75 seconds. The model's speed rule is $12(1 - e^{-t/1.2})$, which
gets closer and closer to 12 and never reaches it: the terminal speed is
the limit of the speed at infinity. That is what "terminal" means in
this model. (The exact answer is
$1.2 \ln 120 \approx 5.745$ seconds, where $\ln$ is a logarithm with
base $e$. The search rounds it to 5.75.)

</details>

**14. Predict.** `derivative_at` uses a step of $10^{-6}$. The slope of
$x^2$ at $x$ is $2x$. What do these print, next to the right answers?

```python
for x in [1e8, 1e10, 1e11]:
    print(x, derivative_at(squared, x), 2 * x)
```

<details class="dl-answer"><summary>answer</summary>

At $10^8$ the answer is right, $2 \times 10^8$. At $10^{10}$ it is
about $3.28 \times 10^{10}$, when it should be $2 \times 10^{10}$. At
$10^{11}$ it is 0.0.

Near $10^{11}$, the gap between neighbouring floats is about $10^{-5}$,
bigger than the step. So $10^{11} + 10^{-6}$ is kept as $10^{11}$, the
chord has no length, and the rise is 0. This is why the tutorial said
$10^{-6}$ suits rules whose values are of ordinary size. One fix is a
step that grows with $x$: `derivative_at(squared, 1e11, step=1e5)`
gives $2 \times 10^{11}$, to within a float's rounding.

</details>

**15. Make.** A derivative at every point is a new rule: the
hailstone's speed at every time. Write `fall_speed(seconds)`, which
gives back `derivative_at(fall_distance, seconds)`, and draw it from 0
to 10 with `plot_rule`. Where is the curve steepest, and what does
that mean?

<details class="dl-answer"><summary>answer</summary>

```python
def fall_speed(seconds):
    return derivative_at(fall_distance, seconds)

plot_rule(fall_speed, 0, 10)
plt.xlabel("seconds after it starts to fall")
plt.ylabel("metres a second")
for second in [0, 1, 3, 6, 10]:
    print(second, round(fall_speed(second), 2))
```

The speed starts at 0, is 6.78 after 1 second and 11.01 after 3, and
levels off near 12: 11.92 at 6 seconds and 12.0 at 10. The speed curve
is steepest at the start, where the speed changes fastest. The slope of
the speed curve is itself a rate of change, of speed, which is called
acceleration: the stone speeds up most in the first second, and hardly
at all once the air's push nearly balances its weight. A rule made
from the derivative at every point is called the derivative function,
and [Rules for change](tutorial:rules-for-change) finds such rules
without a chord at all.

</details>
