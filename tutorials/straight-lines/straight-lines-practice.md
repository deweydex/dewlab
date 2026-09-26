---
title: "Straight lines: slope and gradient — Practice"
practice_for: straight-lines
year: "2026-2027"
version: 2026.09.26.2
---

# Straight lines: slope and gradient — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another way** means reach the same place by a second
route. The answers are folded away until you open them. Each is one
answer, and yours may be different and work too.

Your toolkit is loaded on this page, including `slope` and
`line_through` from the tutorial, `close_enough` from
[Does it work?](tutorial:does-it-work) and `plot_rule` from
[Drawing a rule](tutorial:drawing-a-rule).

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: straight-practice-warm-up
# Try things here
```

**1. Predict.** What does each line print?

```python
print(slope((0, 0), (4, 1)))
print(slope((2, 5), (6, 5)))
print(slope((0, 3), (3, 0)))
```

<details class="dl-answer"><summary>answer</summary>

`0.25`, `0.0` and `-1.0`.

The first line rises 1 over a run of 4. The second has a rise of
$5 - 5 = 0$, so it is flat. The third falls 3 over a run of 3, so its
slope is $\frac{-3}{3} = -1$. It goes down as we read it from left to
right. Python shows each as a float, because `/` always gives a float.

</details>

**2. Make.** A road climbs 25 m while going 200 m along the ground.
What is its slope? Road signs often show a gradient as a percent, which
is the slope times 100. What percent is this hill, and what is it as
"1 in" something?

<details class="dl-answer"><summary>answer</summary>

```python
hill = 25 / 200
print(hill, hill * 100, 1 / hill)
```

The slope is 0.125, which is 12.5%, or 1 in 8. Every 8 metres along,
the road climbs 1 metre.

</details>

<aside class="dl-note" id="straight-practice-note-baldwin">

**The steepest street.** Guinness World Records lists Baldwin Street,
in Dunedin in New Zealand, as the steepest street in the world. In 2019
the title went to Ffordd Pen Llech, in Harlech in Wales. In 2020
Guinness measured both along the middle of the road, and Baldwin Street
won the title again: 34.8% against 28.6%.

</aside>

**3. Explain.** Ramp A rises 0.5 m over a run of 6 m. Ramp B rises
0.25 m over a run of 3 m. Which is steeper? Answer before you calculate
anything, then check.

<details class="dl-answer"><summary>answer</summary>

Neither. They are equally steep. Ramp B is ramp A cut in half, so both
the rise and the run are halved, and rise over run does not change.
Both slopes are $\frac{1}{12}$, a gradient of 1:12. Steepness is about
the rise for each metre along, not about the rise alone.

</details>

**4. Predict.** What does this print?

```python
print(line_through((0, 5), (2, 9)))
```

<details class="dl-answer"><summary>answer</summary>

`(2.0, 5.0)`.

The slope is $\frac{9 - 5}{2 - 0} = 2$. The first point has $x = 0$, so
it is where the line crosses the $y$ axis, and $c = 5$. The line is
$y = 2x + 5$.

</details>

## Core

A cell for the core problems.

```python exec
id: straight-practice-core
# Your working for problems 5 to 12
```

**5. Make.** A library door has one step, 0.25 m high, and room for a
ramp going up to 4 m along the path. The ramp table from the tutorial
says a going of up to 5 m may be at most 1:15. How long a run does a
1:15 ramp need for this step? Does it fit?

<details class="dl-answer"><summary>answer</summary>

```python
rise = 0.25
needed_run = rise * 15
print(needed_run, needed_run <= 4)
print(slope((0, 0), (needed_run, rise)), 1 / 15)
```

The run is $0.25 \times 15 = 3.75$ m, which fits in 4 m. This is the
slope formula run backwards: $\text{run} = \frac{\text{rise}}{\text{slope}}$,
and to divide by $\frac{1}{15}$, we multiply by 15. The last line
checks it with `slope`. Both numbers are about 0.0667.

</details>

**6. Fix.** Schlomo, who is learning Python too, wrote his own
`slope`. For a line at 45 degrees it gives 1. For a gentle ramp, from
$(0, 0)$ to $(10, 1)$, it gives 10, not 0.1. Can you find what to
change?

```python exec
id: straight-practice-fix-slope
def slope_again(p, q):
    """Return the slope of the straight line through the points p and q."""
    x1, y1 = p
    x2, y2 = q
    return (x2 - x1) / (y2 - y1)
```

```inputs
slope_again((0, 0), (1, 1))     # a line at 45 degrees
slope_again((0, 0), (10, 1))    # a gentle ramp
```

```solution
def slope_again(p, q):
    """Return the slope of the straight line through the points p and q."""
    x1, y1 = p
    x2, y2 = q
    return (y2 - y1) / (x2 - x1)
---
Schlomo's function divides the run by the rise. That is the slope
formula upside down.

The line at 45 degrees gave 1 even so, because it has the same rise
and run, and $\frac{1}{1}$ upside down is still 1. A 45-degree line
is a natural first check, but it cannot show a swap like this. A line
where the rise and the run differ shows it.
```

**7. Another way.** Water freezes at 0 °C, which is 32 °F, and boils at
100 °C, which is 212 °F. Those are two points, $(0, 32)$ and
$(100, 212)$. Use `line_through` to find the rule for turning Celsius
into Fahrenheit. Then check it against your toolkit's
`celsius_to_fahrenheit`, from
[Running a formula backwards](tutorial:running-a-formula-backwards).

<details class="dl-answer"><summary>answer</summary>

```python
m, c = line_through((0, 32), (100, 212))
print(m, c)
for celsius in [-40, 0, 37, 100]:
    print(celsius, m * celsius + c, celsius_to_fahrenheit(celsius))
```

The line is $F = 1.8C + 32$, with slope 1.8, crossing at 32. The two columns
agree for every temperature, with at most a tiny float difference. So
the conversion is a straight line, and two points were enough to find
all of it. At −40 the two scales agree. There, the line crosses
$y = x$.

</details>

**8. Predict.** A game's level editor has three corridors, drawn as
lines on its map:

- corridor A: $y = 2x + 1$
- corridor B: $y = 2x - 3$
- corridor C: $y = -0.5x + 4$

Which pairs are parallel, and which are perpendicular? Decide, then run
this.

```python
corridor_slopes = {"A": 2, "B": 2, "C": -0.5}
for first, second in [("A", "B"), ("A", "C"), ("B", "C")]:
    product_of_slopes = corridor_slopes[first] * corridor_slopes[second]
    print(first, second, corridor_slopes[first] == corridor_slopes[second], product_of_slopes)
```

<details class="dl-answer"><summary>answer</summary>

```text
A B True 4
A C False -1.0
B C False -1.0
```

A and B have the same slope, so they are parallel. They never meet. C
is perpendicular to both, because $2 \times -0.5 = -1$. A line that is
perpendicular to one of two parallel lines is perpendicular to the
other too.

</details>

**9. Make.** Air usually gets colder as you climb. On a day when it is
15 °C at sea level, a standard model of the air says it will be about
2 °C at 2,000 m up. Treat that as a straight line. Find its slope, and
use it to estimate the temperature at the top of Carrauntoohil,
Ireland's highest mountain, at 1,039 m.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The two points are (height, temperature): $(0, 15)$ and
   $(2000, 2)$.
2. `line_through` gives you `m` and `c`.
3. Put 1,039 in for $x$ in $y = mx + c$.

**Think about:** what does a negative slope mean for a climber?

**Try this next:** at what height would the line reach 0 °C?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
m, c = line_through((0, 15), (2000, 2))
print(m, c)
print(round(m * 1039 + c, 1))
print(round(m * 1000, 1), "degrees for every 1,000 m")
```

The slope is −0.0065. The air loses 0.0065 °C for every metre up, or
6.5 °C for every 1,000 m. At the top of Carrauntoohil the line gives
about 8.2 °C. Real air does not follow the line exactly, and wind
makes it feel colder, so a walker still packs a warm layer.

</details>

**10. Explain.** Why can $ax + by + c = 0$ write the wall $x = 2$, when
$y = mx + c$ cannot? What does $b = 0$ mean for a line?

<details class="dl-answer"><summary>answer</summary>

$y = mx + c$ is a rule for finding $y$ from $x$, so it gives one $y$
for each $x$. A wall has many $y$ values at the one $x$, so no such
rule can describe it. The general form only asks whether a point makes
$ax + by + c$ equal 0. It does not need to find $y$, so it has room for
the wall: $1x + 0y - 2 = 0$.

When $b = 0$, the $y$ disappears from the line's equation, and only $x$
decides whether a point is on the line. So $b = 0$ means a vertical
line. The slope, $-\frac{a}{b}$, cannot be found then, because it
would divide by 0.

</details>

**11. Make.** Write `slope_from_general(a, b)`, which returns the slope
of the line $ax + by + c = 0$. Use it on $3x - 6y + 12 = 0$, and check
by finding two points on that line and using `slope`.

<details class="dl-answer"><summary>answer</summary>

```python
def slope_from_general(a, b):
    """Return the slope of the line ax + by + c = 0. b must not be 0."""
    return -a / b

print(slope_from_general(3, -6))
# Two points: when x = 0, -6y + 12 = 0, so y = 2. When x = 4, 12 - 6y + 12 = 0, so y = 4.
print(slope((0, 2), (4, 4)))
```

Both give 0.5. Move everything except $by$ to the right, and you get
$by = -ax - c$, so $y = -\frac{a}{b}x - \frac{c}{b}$, and the slope is
$-\frac{a}{b} = -\frac{3}{-6} = 0.5$.

</details>

**12. Fix.** Schlomi, who is learning Python too, wrote her own
`line_through`. For server A, from $(0, 8)$ to $(10, 28)$, her line
goes through both points. For the line through $(2, 3)$ and $(6, 11)$,
it misses them. What is different about the second line, and what
needs to change?

```python exec
id: straight-practice-fix-line
def line_through_again(p, q):
    """Return (m, c) for the line y = mx + c through the points p and q."""
    m = slope(p, q)
    x1, y1 = p
    c = y1 + m * x1
    return (m, c)
```

```inputs
line_through_again((0, 8), (10, 28))    # server A
line_through_again((2, 3), (6, 11))     # a second line
```

```solution
def line_through_again(p, q):
    """Return (m, c) for the line y = mx + c through the points p and q."""
    m = slope(p, q)
    x1, y1 = p
    c = y1 - m * x1
    return (m, c)
---
In $y_1 = m x_1 + c$, when $m x_1$ moves to the other side, it is taken
away. So $c = y_1 - m x_1$. Schlomi's code adds it.

Server A's line came out as it should, because its first point has
$x_1 = 0$. So $m x_1$ is 0, and it makes no difference whether we add
it or take it away. Server A was a natural first check for Schlomi,
since it is the line she knew best. If she had put both points back
into the line, as the tutorial did, she would have seen the mistake at
once.
```

## Stretch

A cell for the stretch problems.

```python exec
id: straight-practice-stretch
# Your working for problems 13 to 15
```

**13. Make.** A drawing program lets you draw a line, then click a
point to draw a second line at a right angle to it. Write
`perpendicular_through(m, point)`, which returns the `(m, c)` of the line
through `point` that is perpendicular to a line of slope `m`. Test it
by drawing both lines with `plot_rule`, with `plt.axis("equal")`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The new slope is $-\frac{1}{m}$.
2. The point is on the new line, so $c = y - (\text{new slope}) \times x$,
   as in `line_through`.
3. Return the pair.

**Think about:** which slope `m` makes this function fail, and what
kind of line would the answer be?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

def perpendicular_through(m, point):
    """Return (m, c) of the line through point at a right angle to a line of slope m.

    m must not be 0: the line at a right angle to a flat line is vertical.
    """
    new_slope = -1 / m
    x, y = point
    return (new_slope, y - new_slope * x)

new_m, new_c = perpendicular_through(0.5, (2, 2))
print(new_m, new_c, close_enough(0.5 * new_m, -1))

def first_line(x):
    return 0.5 * x + 1

def second_line(x):
    return new_m * x + new_c

plt.axis("equal")
plot_rule(first_line, -1, 5)
plot_rule(second_line, -1, 5)
```

The new line is $y = -2x + 6$, and it goes through $(2, 2)$, which is
on the first line. The picture shows a square corner. With `m = 0` the
function stops with a `ZeroDivisionError`. The line at a right angle
to a flat line is a wall, which has no slope.

</details>

**14. Another way.** The rule $m_1 m_2 = -1$ fails for a flat line and
a wall, because the wall has no slope. In the general form, two lines
$a_1 x + b_1 y + c_1 = 0$ and $a_2 x + b_2 y + c_2 = 0$ are
perpendicular when $a_1 a_2 + b_1 b_2 = 0$. Check this rule on the
floor $y = 0$ and the wall $x = 2$, and on the tutorial's lines
$y = 0.5x + 1$ and $y = -2x + 6$.

<details class="dl-answer"><summary>answer</summary>

```python
def perpendicular_general(a1, b1, a2, b2):
    """Return True when a1x + b1y + c1 = 0 and a2x + b2y + c2 = 0 meet at a right angle."""
    return close_enough(a1 * a2 + b1 * b2, 0)

print(perpendicular_general(0, 1, 1, 0))       # the floor 0x + 1y + 0 = 0 and the wall 1x + 0y - 2 = 0
print(perpendicular_general(0.5, -1, -2, -1))  # 0.5x - y + 1 = 0 and -2x - y + 6 = 0
print(perpendicular_general(2, -1, 2, -1))     # two parallel lines
```

`True`, `True`, `False`. For the floor and the wall,
$0 \times 1 + 1 \times 0 = 0$. For the tutorial's lines,
$0.5 \times -2 + (-1) \times (-1) = -1 + 1 = 0$. The general form gives
one rule that covers every pair of lines, walls included. The slope
rule is the same rule, divided through by $b_1 b_2$. So it breaks when
a $b$ is 0.

</details>

**15. Make.** A phone's GPS app records a hill climb, as (distance
along the road in km, height in m) pairs. These numbers are invented:

```python
climb = [(0, 20), (1.0, 60), (1.5, 110), (2.5, 150), (3.0, 240)]
```

Find the slope of each section, and the steepest one as a percent. Be
careful: what space are the two numbers in each pair measured in?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over the positions `0` to `len(climb) - 2`, and take each point
   with the next one.
2. Turn the distance into metres first, so that across and up use the
   same unit.
3. Keep the slopes in a list, and use `largest` from your toolkit.

**Think about:** what would the steepest slope be if you forgot to
turn km into m? Would anyone cycle up it?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
climb = [(0, 20), (1.0, 60), (1.5, 110), (2.5, 150), (3.0, 240)]
section_slopes = []
for position in range(len(climb) - 1):
    km_start, height_start = climb[position]
    km_end, height_end = climb[position + 1]
    section_slopes.append(slope((km_start * 1000, height_start), (km_end * 1000, height_end)))
print(section_slopes)
print(largest(section_slopes) * 100, "percent")
```

The slopes are 0.04, 0.1, 0.04 and 0.18, so the last section is the
steepest, at 18%. That is very steep for a road. Without the change to
metres, the last slope would come out as 180, which would mean
climbing 180 m for every metre along. The slope only means something
when across and up share a unit.

</details>
