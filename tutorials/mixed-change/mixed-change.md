---
title: "Mixed problems: change"
practice_across:
  - getting-closer
  - how-fast-right-now
  - rules-for-change
  - solving-by-computing
year: "2026-2027"
version: 2026.09.25.1
datasets: [co2-emissions]
---

# Mixed problems: change

Each problem here draws on at least one page of Unit 9, and many draw on
two or more. None of them is harder than what those pages covered. This
time, nobody tells you which page a problem comes from. You choose the
tool yourself, and that is part of the problem.

Along the way, the problems build this unit's product: a best-moment
finder. Give it a rule, and it finds the rule's top or bottom and the
moment it changes fastest. Give it real data, Ireland's carbon dioxide
emissions since 1950, and it finds the year they peaked and the year
they rose fastest. Every answer is checked a second way. Problems 5,
7, 12, 14 and 16 are the finder's parts, and they build on each other,
so do those in order.

Your toolkit is loaded on this page: `derivative_at`, `bisect_root` and
`newton` from this unit, and every tool from Units 1 to 8, such as
`vertex`, `largest`, `slope` and `close_enough`. A cell that says
`slope = ...` hides that tool, so give your numbers other names. Where
a problem asks you to predict, make the prediction before you run
anything. It is the most useful part.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: mixed-change-scratch-1
import math
# Try things here
```

**1. Predict.** What does each line print?

```python
def cube(x):
    return x ** 3

def eight_gap(x):
    return x ** 3 - 8

print(round(derivative_at(cube, 2), 3))
print(round(newton(eight_gap, 3), 6))
print(round((1 + 1 / 1000) ** 1000, 3))
```

<details class="dl-answer"><summary>answer</summary>

`12.0`, `2.0` and `2.717`.

By the power rule from
[Rules for change](tutorial:rules-for-change#a-pattern-in-the-slopes-the-power-rule),
the slope of $x^3$ is $3x^2$, which is 12 at 2. `newton` looks for an
$x$ where $x^3 - 8$ is 0, and that is the cube root of 8, which is 2.
The last line is the bank that pays 1,000 times a year, on
[Getting closer](tutorial:getting-closer#a-limit-at-infinity), on its
way to $e \approx 2.718$.

</details>

**2. Predict.** Here is a table that closes in on 4 from both sides,
for the rule $\frac{\sqrt{x} - 2}{x - 4}$. At 4 itself, it is
$\frac{0}{0}$. What number do the columns head for? Then look at the
rule again. It is the slope of a chord of one curve. Which curve, and
which slope is the limit?

```python
import math

def root_chord(x):
    return (math.sqrt(x) - 2) / (x - 4)

step = 1
for row in range(10):
    print(step, root_chord(4 - step), root_chord(4 + step))
    step = step / 2
```

<details class="dl-answer"><summary>answer</summary>

Both columns head for 0.25, one from above and one from below.

Since $\sqrt{4} = 2$, the rule is $\frac{\sqrt{x} - \sqrt{4}}{x - 4}$:
rise over run, for the chord of $y = \sqrt{x}$ from 4 to $x$. So its
limit is the slope of $\sqrt{x}$ at 4, as on
[How fast, right now?](tutorial:how-fast-right-now#the-derivative-is-a-limit).
The power rule gives the same. The slope of $x^{1/2}$ is
$\frac{1}{2}x^{-1/2}$, and at 4 that is $\frac{1}{2} \times \frac{1}{2} = 0.25$.

</details>

**3. Predict.** A storage box shaped like a cube must hold 20 litres,
which is 20 cubic decimetres. Its side is the cube root of 20, between
2 and 3 decimetres. Bisection starts with `low` at 2 and `high` at 3.
How many halvings until the gap is no bigger than $10^{-6}$? Use
$2^{10} \approx 1000$. Then check by counting, with a counter inside a
copy of the bisection loop.

<details class="dl-answer"><summary>answer</summary>

Twenty. The gap starts at 1, and after $k$ halvings it is
$\frac{1}{2^k}$. We need $2^k \geq 10^6$, and $10^6$ is $1000^2$, so
about 20 halvings. $2^{20}$ is 1,048,576, just over a million.

```python
def box_gap(side):
    return side ** 3 - 20

low = 2
high = 3
halvings_done = 0
while high - low > 1e-6:
    middle = (low + high) / 2
    if box_gap(low) * box_gap(middle) <= 0:
        high = middle
    else:
        low = middle
    halvings_done = halvings_done + 1

print(halvings_done, (low + high) / 2)
print(bisect_root(box_gap, 2, 3, tolerance=1e-6))
```

Twenty halvings, and a side of about 2.714 dm, or 27.1 cm. The loop is
the one inside
[`bisect_root`](tutorial:solving-by-computing#a-tool-that-halves), with
a counter added.

</details>

**4. Explain.** A weather radar says a hailstone is falling at 11 metres
a second. Schlomo, who is learning Python too, says: "In a single
instant the stone moves 0 metres, and 0 metres in 0 seconds is not a
speed. So the radar is showing something that does not exist." Where does
Schlomo's idea work, where does it stop working, and what does the
radar show?

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Schlomo's first step works. Distance divided by time, at one instant, is
$\frac{0}{0}$, which has no value. But a rule can have a limit where it
has no value, as $\frac{x^2 - 4}{x - 2}$ did at 2 on
[Getting closer](tutorial:getting-closer#a-rule-with-a-hole-in-it). The
average speeds over one second, half a second, a hundredth of a second,
head for one number. That limit is the derivative of the distance, as
on [How fast, right now?](tutorial:how-fast-right-now#the-derivative-is-a-limit),
and it is what the radar shows.

</details>

## Core

A scratch cell for the core problems. Keep the finder's functions in it
as you write them, so that later problems can use them.

```python exec
id: mixed-change-scratch-2
import math
# Your best-moment finder, problem by problem
```

**5. Make.** On
[The top of the curve](tutorial:the-top-of-the-curve#a-letter-that-sits-below-the-line),
the bottom of a letter's bowl had the height $400t^2 - 440t + 112$ font
units, for $t$ from 0 to 1.

The first part of the finder is `best_point(rule, low, high)`. At a top
or a bottom the slope is 0, so `best_point` finds a root of the rule's
slope with `bisect_root`, and returns $(x, \text{rule}(x))$. Use
it to find how far the bowl dips below the baseline, and check it with
`vertex`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Inside `best_point`, write a small function `slope_here(x)` that
   returns `derivative_at(rule, x)`.
2. `bisect_root(slope_here, low, high)` finds where that slope is 0.
3. Return the $x$ it found, and the rule at that $x$.

**Think about:** `slope_here` uses `rule`, which is not one of its own
inputs. Why can it see it?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def best_point(rule, low, high):
    """Return (x, rule(x)) where the slope of rule is 0, for x between low and high.

    The slope must be positive at one end and negative at the other.
    It is a top when the slope goes from positive to negative, and a
    bottom when it goes from negative to positive.
    """
    def slope_here(x):
        return derivative_at(rule, x)
    x = bisect_root(slope_here, low, high)
    return (x, rule(x))

def bowl_height(t):
    """Return the height of the letter's bowl, in font units, at t from 0 to 1."""
    return 400 * t ** 2 - 440 * t + 112

print(best_point(bowl_height, 0, 1))
print(vertex(400, -440, 112))
```

The lowest point is at $t = 0.55$, 9 font units below the baseline.
`best_point` is a billionth away, since `bisect_root` stops when its
gap is that small. The slope is 0 at the bottom, as on
[Rules for change](tutorial:rules-for-change#back-to-the-top-of-the-curve).

`slope_here` can see `rule` because it is made inside `best_point`, as
on
[What a function can see](tutorial:what-a-function-can-see#a-function-made-inside-a-function).

</details>

**6. Fix.** Schlomi, who is learning Python too, wrote a first
`best_point`. On the bowl it stops with a `ValueError`: "rule(low) and
rule(high) have the same sign". But the bowl's slope does change sign
between 0 and 1. Find the line that does not do what Schlomi meant.

```python exec
id: mixed-change-fix-best
def first_best_point(rule, low, high):
    """Return (x, rule(x)) where the slope of rule is 0."""
    x = bisect_root(rule, low, high)
    return (x, rule(x))

def bowl_height(t):
    return 400 * t ** 2 - 440 * t + 112

print(first_best_point(bowl_height, 0, 1))
```

<details class="dl-answer"><summary>answer</summary>

It looks for a root of the rule, not of its slope. A root of the
height is a $t$ where the letter crosses the baseline. At 0 and at 1
the height is 112 and 72, both above the line, so `bisect_root` finds
no sign change and says so. The error message was telling the truth
about a different rule from the one Schlomi meant. The fix is to hand `bisect_root` the slope:

```python
def first_best_point(rule, low, high):
    """Return (x, rule(x)) where the slope of rule is 0."""
    def slope_here(x):
        return derivative_at(rule, x)
    x = bisect_root(slope_here, low, high)
    return (x, rule(x))
```

Then it gives $t = 0.55$ and a height of $-9$.

</details>

**7. Make.** A courier drives a 240 km run. The driver is paid €18 an
hour, so at $v$ km/h the wages for the trip are
$\frac{240 \times 18}{v} = \frac{4320}{v}$ euro. A faster drive burns more fuel. Say the fuel for
the trip costs $0.0036v^2$ euro. (A made-up model.) The cost of the
trip is the two added.

Find the cheapest speed between 40 and 120 km/h with `best_point`. Then
check it with a fine comb, as on
[The top of the curve](tutorial:the-top-of-the-curve#checking-with-a-fine-comb):
every speed from 40 to 120 in steps of 0.01 km/h, and the smallest
cost among them.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def trip_cost(speed_kmh):
    """Return the cost in euro of the 240 km run at this speed: wages plus fuel."""
    return 4320 / speed_kmh + 0.0036 * speed_kmh ** 2

print(best_point(trip_cost, 40, 120))

speeds = []
costs = []
for hundredths in range(4000, 12001):
    speeds.append(hundredths / 100)
    costs.append(trip_cost(hundredths / 100))
cheapest = smallest(costs)
print(speeds[costs.index(cheapest)], cheapest)
```

About 84.34 km/h, for a trip that costs about €76.83, and the comb of
8,001 speeds agrees. `best_point` found a bottom this time, not a top,
and it did not need to know which. Either way the slope is 0 there.
The name `speed_kmh` leaves your toolkit's `speed` alone.

</details>

**8. Another way.** Find the courier's cheapest speed with no search.
Write the slope of the cost with the power and sum rules
($\frac{4320}{v}$ is $4320v^{-1}$), set it to 0, and rearrange to get
$v^3$ on its own. Check your answer with `newton`.

<details class="dl-answer"><summary>answer</summary>

By the power rule, the slope of $4320v^{-1}$ is $-4320v^{-2}$, and the
slope of $0.0036v^2$ is $0.0072v$. So the slope of the cost is

$$-\frac{4320}{v^2} + 0.0072v$$

Set it to 0, and multiply both sides by $v^2$. This gives
$0.0072v^3 = 4320$, so $v^3 = 600000$, and $v$ is the cube root of
600,000.

```python
def cube_gap(v):
    return v ** 3 - 600000

print(600000 ** (1 / 3))
print(newton(cube_gap, 80))
print(best_point(trip_cost, 40, 120)[0])
```

All three give 84.343. The algebra also says why. At the best speed,
the slopes of the wages and the fuel cancel.

</details>

**9. Predict.** The number $e$ from
[Getting closer](tutorial:getting-closer#a-limit-at-infinity) has a
famous property. What do you expect the two columns to show? Guess,
then run it.

```python
for x in [-1, 0, 1, 2, 3]:
    print(x, round(derivative_at(math.exp, x), 6), round(math.exp(x), 6))
```

<details class="dl-answer"><summary>answer</summary>

The two columns are the same. The slope of $e^x$ is $e^x$ itself. At every point, the
curve climbs as fast as it is high.

By the chain rule, the slope of $e^{kx}$ is $e^{kx} \times k$. For
example, the slope of $e^{-t/2}$ is $-\frac{1}{2}e^{-t/2}$. The next
problem needs that.

</details>

**10. Make.** After a tablet is swallowed, the amount of medicine in
the blood rises, peaks and falls. A model for one medicine, in mg
per litre, $t$ hours after the dose, is $30te^{-t/2}$. (The numbers are
made up.) When is the amount highest, and how high is it? Find it with
`best_point`. Then check it with the product rule and the chain rule:
write the slope by hand, and find where it is 0.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The rule is a product: $30t$ times $e^{-t/2}$.
2. The slope of $30t$ is 30. The slope of $e^{-t/2}$ is
   $-\frac{1}{2}e^{-t/2}$, from problem 9.
3. By the product rule, the slope is the first times the slope of the second, plus the
   second times the slope of the first.
4. $e^{-t/2}$ is never 0, so take it out as a common factor.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def in_blood(hours):
    """Return the medicine in the blood, in mg per litre, this many hours after the dose."""
    return 30 * hours * math.exp(-hours / 2)

peak_time, peak_amount = best_point(in_blood, 0, 8)
print(peak_time, peak_amount)
print(60 / math.e)
```

The peak is after 2 hours, at about 22.07 mg per litre.

By the product rule, the slope is

$$30t \times \left(-\tfrac{1}{2}e^{-t/2}\right) + e^{-t/2} \times 30 = 30e^{-t/2}\left(1 - \tfrac{t}{2}\right)$$

$e^{-t/2}$ is never 0, so the slope is 0 only when $1 - \frac{t}{2} = 0$,
at $t = 2$. The peak is $30 \times 2 \times e^{-1} = \frac{60}{e}$, the
last line of the cell.

</details>

**11. Explain.** A nurse wants the highest amount in the first hour
only, and calls `best_point(in_blood, 0, 1)`. It stops with a
`ValueError`. Why? And what is the highest amount in the first hour?

<details class="dl-answer"><summary>answer</summary>

In the first hour, the amount is still rising, so the slope is
positive at both ends. With no sign change, `bisect_root` raises a
`ValueError`, as its
[promise](tutorial:solving-by-computing#a-tool-that-halves) says.

In that window there is no flat tangent, so `best_point` has nothing
to find. The highest amount is at the edge, at 1 hour.
`in_blood(1)` is about 18.2 mg per litre. The end of
[The top of the curve](tutorial:the-top-of-the-curve#checking-with-a-fine-comb)
gave the same warning. When the turning point is outside the domain,
the best answer is at an edge.

</details>

**12. Make.** A song goes viral. A model for its total streams, in
millions, $t$ days after it is released, is

$$\frac{2}{1 + e^{-(t - 20)/3}}$$

The total climbs slowly, then fast, then flattens near 2 million.
(The model is made up.) On which day are the streams arriving fastest,
and how many a day is that?

This is the finder's second part. It finds the moment a rule changes fastest.
Write `stream_rate(day)`, the slope of the total with `derivative_at`.
Then comb every tenth of a day from 0 to 40 for the largest rate. Draw
the total and its rate on two pictures.

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

def total_streams(day):
    """Return the song's total streams, in millions, this many days after release."""
    return 2 / (1 + math.exp(-(day - 20) / 3))

def stream_rate(day):
    """Return how fast the streams are arriving, in millions a day."""
    return derivative_at(total_streams, day)

days = []
rates = []
for tenths in range(0, 401):
    days.append(tenths / 10)
    rates.append(stream_rate(tenths / 10))
fastest = largest(rates)
print(days[rates.index(fastest)], fastest)

plot_rule(total_streams, 0, 40)
plt.figure()
plot_rule(stream_rate, 0, 40)
```

The streams arrive fastest on day 20, at about 167,000 a day. The
second picture is a hill with its top at day 20. The total grows
fastest where its rate is highest.

</details>

## Stretch

A scratch cell for the stretch problems. Run your finder's cell
first.

```python exec
id: mixed-change-scratch-3
import math
# Your working for problems 13 to 17
```

**13. Another way.** The fastest moment is the top of the rate's hill,
so `best_point(stream_rate, 5, 35)` should find it too. Try it. It says
about 19.996, not 20. Why is it a little off? Find the day a third way, with a slope of the rate whose
step is $10^{-3}$, and `bisect_root`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `best_point` takes a slope of `stream_rate`, and `stream_rate` is
   itself a slope. How many small steps are inside each other?
2. Read
   [Why the step cannot be 0, or too small](tutorial:how-fast-right-now#why-the-step-cannot-be-0-or-too-small)
   again. What happens to a tiny error when it is divided by a tiny
   step?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(best_point(stream_rate, 5, 35))

def rate_slope(day):
    return derivative_at(stream_rate, day, step=1e-3)

print(bisect_root(rate_slope, 5, 35))
```

`best_point` takes a chord of a chord. `stream_rate` already carries a
tiny float error. `best_point` subtracts two nearly equal rates and
divides by $2 \times 10^{-6}$ again, which makes that error large. Near
the top, the true slope of the rate is very small, so the error moves
the sign change by 0.004 of a day. With a step of $10^{-3}$ for the
outer chord, the error stays small, and `bisect_root` finds
20.000000.

</details>

**14. Make.** Now real data. Ireland's carbon dioxide emissions, in
millions of tonnes a year, are in `co2-emissions.csv`, as on
[Doubling and halving](tutorial:doubling-and-halving#doubling-in-real-data).
There is no rule for `derivative_at`, only one number a year. But a
centred chord needs only the year before and the year after.

1. Load Ireland's years and emissions as two lists.
2. Find the peak year with `largest`.
3. For every year that has a year on each side, find the slope of the
   centred chord from the year before to the year after.
4. A top is a year where the slope before it was positive and its own
   slope is 0 or less. List the years where that happens.

<details class="dl-answer"><summary>answer</summary>

```python
df = await load_csv("co2-emissions.csv")
ireland = df[df.country == "Ireland"]
years = ireland["year"].tolist()
emissions = ireland["co2"].tolist()

peak = largest(emissions)
print("peak:", years[emissions.index(peak)], peak)

middle_years = []
chord_slopes = []
for i in range(1, len(years) - 1):
    middle_years.append(years[i])
    chord_slopes.append(slope((years[i - 1], emissions[i - 1]), (years[i + 1], emissions[i + 1])))

tops = []
for i in range(1, len(chord_slopes)):
    if chord_slopes[i - 1] > 0 and chord_slopes[i] <= 0:
        tops.append(middle_years[i])
print("tops:", tops)
```

The peak is 2005, at 48.2 million tonnes. But the slopes find eight
tops: 1956, 1974, 1980, 1988, 2002, 2006, 2017 and 2022. Real data goes
up and down a little every year, with the weather and the economy, and
a chord two years long sees every bump.

</details>

**15. Predict.** Now make each chord longer: from 5 years before to 5
years after. How many tops do you expect this time? Change the cell
from problem 14, then run it.

<details class="dl-answer"><summary>answer</summary>

Give the reach a name, and use it in the loop that makes the chords:

```python
reach = 5
middle_years = []
chord_slopes = []
for i in range(reach, len(years) - reach):
    middle_years.append(years[i])
    chord_slopes.append(slope((years[i - reach], emissions[i - reach]), (years[i + reach], emissions[i + reach])))

tops = []
for i in range(1, len(chord_slopes)):
    if chord_slopes[i - 1] > 0 and chord_slopes[i] <= 0:
        tops.append(middle_years[i])
print("tops:", tops)
```

One top: 2004, one year from the peak `largest` found. A ten-year
chord smooths the bumps, and only the long rise and fall is left.

This is the step-size question from
[How fast, right now?](tutorial:how-fast-right-now#why-the-step-cannot-be-0-or-too-small)
in a new space. There, a step too short was lost in the float errors.
Here, a chord too short is lost in the bumps, and a chord too long
blurs the answer. The reach is a choice, and a report should say which
it used.

</details>

**16. Make.** Put the data half of the finder together. Write
`data_rates(years, values, reach)`, which returns two lists: the
middle years, and the slope of the centred chord at each. Then use it
with a reach of 5 to report three things about Ireland's emissions:
the peak year, found two ways; the year with the fastest rise; and the
year with the fastest fall. Draw the rates against the years, with a
line at 0.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
import matplotlib.pyplot as plt

def data_rates(years, values, reach):
    """Return (middle_years, rates): the slope of the centred chord at each middle year.

    Each chord runs from reach years before to reach years after, so the
    first and last reach years have no rate.
    """
    middle_years = []
    rates = []
    for i in range(reach, len(years) - reach):
        middle_years.append(years[i])
        rates.append(slope((years[i - reach], values[i - reach]), (years[i + reach], values[i + reach])))
    return (middle_years, rates)

middle_years, co2_rates = data_rates(years, emissions, 5)

print("peak, by largest:", years[emissions.index(largest(emissions))])
for i in range(1, len(co2_rates)):
    if co2_rates[i - 1] > 0 and co2_rates[i] <= 0:
        print("peak, by the rates:", middle_years[i])

fastest_rise = largest(co2_rates)
fastest_fall = smallest(co2_rates)
print("fastest rise:", middle_years[co2_rates.index(fastest_rise)], round(fastest_rise, 2))
print("fastest fall:", middle_years[co2_rates.index(fastest_fall)], round(fastest_fall, 2))

plt.plot(middle_years, co2_rates, marker="o")
plt.axhline(0, color="grey", linewidth=1)
plt.xlabel("middle year of a 10-year chord")
plt.ylabel("change in million tonnes a year")
```

The peak is 2005 by `largest`, and 2004 by the rates. The fastest rise
is centred on 1996. From 1991 to 2001, emissions grew by about 1.39
million tonnes a year. The fastest fall is centred on 2006. From 2001
to 2011, they fell by about 0.96 million tonnes a year, most of it
after 2008.

That is the finder. For a rule, it finds a slope of 0. For data, it
finds a peak two ways.

</details>

**17. Fix.** Schlomo wants a more exact bottom for the letter's bowl,
so he gives `derivative_at` a much smaller step. He thinks a
smaller step is closer to the limit. But the finder now
says the bowl is lowest at about $t = 0.514$, and the height there is
higher than at 0.55. Find the line that does not do what Schlomo meant.
Which page warned about it?

```python exec
id: mixed-change-fix-step
def bowl_height(t):
    return 400 * t ** 2 - 440 * t + 112

def exact_slope(t):
    return derivative_at(bowl_height, t, step=1e-15)

lowest_t = bisect_root(exact_slope, 0, 1)
print(lowest_t, bowl_height(lowest_t), bowl_height(0.55))
for t in [0.2, 0.5, 0.6]:
    print(t, exact_slope(t), 800 * t - 440)
```

<details class="dl-answer"><summary>answer</summary>

The step of $10^{-15}$ is too small. The two heights the chord
subtracts are nearly equal, and each is a float a tiny way off, so the
"slope" is mostly float error: $-28.4$ at 0.5 beside the true
$-40$, and $14.2$ at 0.6 beside the true 40. With slopes that far off,
the sign change lands somewhere else. The fix is to leave the step
at its default:

```python
def exact_slope(t):
    return derivative_at(bowl_height, t)
```

Then the root is 0.55 again.
[How fast, right now?](tutorial:how-fast-right-now#why-the-step-cannot-be-0-or-too-small)
warned that a step of $10^{-15}$ loses the answer, and
[Getting closer](tutorial:getting-closer#when-the-floats-run-out)
showed why. In the floats, a very small step gives a worse answer,
not a better one. Before you trust a best point, put it
back in the rule, as the cell's first `print` did.

</details>
