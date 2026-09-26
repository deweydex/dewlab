---
title: "Mixed problems: algebra you can run"
practice_across:
  - rules-with-letters-in-them
  - drawing-a-rule
  - solving-for-x
  - when-there-is-no-real-answer
  - the-top-of-the-curve
  - several-unknowns-at-once
year: "2026-2027"
version: 2026.09.25.1
datasets: [planet-orbits]
---

# Mixed problems: algebra you can run

Each problem here draws on at least one page of Unit 7, and many draw on
two or more. None of them asks for more than those pages covered. This
time, nobody tells you which page a problem comes from. You choose the
tool yourself, and that is part of the problem.

Along the way, the problems build this unit's product in two parts: a
server chooser, which finds where two servers are equally fast and the
fastest server for a crowd, and a free-kick checker, which finds the top
of a ball's flight and whether it clears a wall. Every answer is checked
by putting it back into its rule, in code. Problems 4, 6, 8 and 9 build
the chooser, and 12, 13 and 15 the free-kick checker. Each builds on the
one before, so do those in order. Problem 11 is a detour to the
planets, with real data from NASA.

Your toolkit is loaded on this page: this unit's tools and every tool
from Units 1 to 6, such as `close_enough` and `largest`. Where a
problem asks you to predict, make the prediction before you run
anything. Schlomo and Schlomi, who are learning Python too, turn up in
a few problems with ideas of their own.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: mixed-run-scratch-1
# Try things here
```

**1. Predict.** What does each line print? Find each one by hand
first.

```python
print(evaluate([5, 0, -1], 3))
print(solve_linear(4, -10))
print(solve_quadratic(1, 0, -9))
print(vertex(1, -4, 1))
```

<details class="dl-answer"><summary>answer</summary>

`-4`, `2.5`, `[-3.0, 3.0]` and `(2.0, -3.0)`.

`[5, 0, -1]` is $5 - x^2$, lowest power first, and $5 - 9 = -4$.
$4x - 10 = 0$ gives $x = \frac{10}{4}$. $x^2 - 9 = 0$ has two roots,
smallest first. The vertex of $x^2 - 4x + 1$ is at
$x = -\frac{-4}{2} = 2$, where the rule is $4 - 8 + 1 = -3$.

</details>

**2. Make.** A phone is at 10% and charging. It gains 0.5% a minute.
(A steady rate is only a model. Real phones charge more slowly as they
fill.) How many minutes until it shows 40%? Write the equation, tidy it
into the shape $ax + b = 0$, solve it with `solve_linear`, and put the
answer back in.

<details class="dl-answer"><summary>answer</summary>

With $m$ minutes, the equation is $10 + 0.5m = 40$. Subtract 40 from
both sides: $0.5m - 30 = 0$, so $a = 0.5$ and $b = -30$.

```python
minutes = solve_linear(0.5, -30)
print(minutes)
print(evaluate([10, 0.5], minutes))
```

It prints `60.0`, and after 60 minutes the phone shows `40.0`. The rule
$10 + 0.5m$ is the list `[10, 0.5]`, so `evaluate` does the
substituting.

</details>

**3. Explain.** On a frosty night in Mullingar, a weather app models the
temperature $t$ hours after midnight as $0.1t^2 - 1.2t + 2$ degrees
Celsius, from midnight to noon. (A made-up model.) Schlomi says: "The
coldest moment is where the graph crosses zero." Run this cell. What do
the two answers mean, and when is the coldest moment?

```python
print(solve_quadratic(0.1, -1.2, 2))
print(vertex(0.1, -1.2, 2))
```

<details class="dl-answer"><summary>answer</summary>

The first line gives the roots, `[2.0, 10.0]`. The second gives the
vertex, $(6, -1.6)$, printed with a tiny float error in the last
digits.

A root is a time when the temperature is exactly 0 °C: 2 am and
10 am. The vertex is where the curve turns, as on
[The top of the curve](tutorial:the-top-of-the-curve#a-curve-that-turns).
Its $t^2$ term is positive, so the vertex is a minimum. The coldest
moment is 6 am, at −1.6 °C. Schlomi's idea is a natural one, since 0 °C
is where frost starts, but she has swapped the roots and the vertex.
The vertex is halfway between the roots, and 6 is halfway between 2 and 10.

</details>

## Core

The core problems build the server chooser. An app can run on three
kinds of server. Each answers a request in a fixed time, plus a time
for each thousand people using the app at once. The cluster spreads the
work over many machines, so the crowd makes no difference to it, but
every request passes through one extra machine first. (The times are
made up.)

| Server | Fixed time | For each thousand people |
|---|---|---|
| Small | 8 ms | 3 ms |
| Medium | 15 ms | 1.25 ms |
| Cluster | 30 ms | 0 ms |

Each server's time is a linear rule, so this cell keeps each one as a
list of coefficients, lowest power first, as on
[Rules with letters in them](tutorial:rules-with-letters-in-them#terms-coefficients-and-a-list).
Run it first.

```python exec
id: mixed-run-servers
servers = {
    "Small": [8, 3],
    "Medium": [15, 1.25],
    "Cluster": [30, 0],
}
print(evaluate(servers["Small"], 2))
```

It prints `14`. With two thousand people, the small server takes 14 ms.
Keep the chooser's functions in the scratch cell below as you write
them, so that later problems can use them.

```python exec
id: mixed-run-scratch-2
# Your server chooser, problem by problem
```

**4. Make.** The chooser's first job is a table. Write a loop that
prints each server's time at 0, 4, 8, 12 and 16 thousand people, one
row for each crowd. Which server would you choose for each crowd?

<details class="dl-answer"><summary>answer</summary>

```python
for thousands in [0, 4, 8, 12, 16]:
    row = [thousands]
    for name in servers:
        row.append(evaluate(servers[name], thousands))
    print(row)
```

```text
[0, 8, 15.0, 30]
[4, 20, 20.0, 30]
[8, 32, 25.0, 30]
[12, 44, 30.0, 30]
[16, 56, 35.0, 30]
```

Small wins with no crowd, Medium at 8 thousand and the cluster at 16
thousand, with ties at 4 and 12 thousand. The table shows the ties only
because its rows land on them.

</details>

**5. Predict.** Here are the three servers as a picture, drawn with
`plot_rule` from
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet).
How many times will two lines cross? Guess where, before you run it.

```python exec
id: mixed-run-servers-picture
import matplotlib.pyplot as plt

def small(thousands):
    return evaluate(servers["Small"], thousands)

def medium(thousands):
    return evaluate(servers["Medium"], thousands)

def cluster(thousands):
    return evaluate(servers["Cluster"], thousands)

plot_rule(small, 0, 16)
plot_rule(medium, 0, 16)
plot_rule(cluster, 0, 16)
plt.xlabel("thousands of people using the app")
plt.ylabel("ms to answer")
plt.legend()
```

<details class="dl-answer"><summary>answer</summary>

There are three crossings, one for each pair: Small and Medium at 4
thousand, Small and Cluster at a little over 7 thousand, and Medium and
Cluster at 12 thousand.

Only two of them matter to someone choosing. The fastest server is the
lowest line: Small up to 4 thousand, Medium from 4 to 12 thousand, and
the cluster after that. Small and Cluster cross above the Medium line,
where neither is fastest.

</details>

**6. Make.** Two servers are equally fast where the difference of their
rules is 0. Write two functions:

- `subtract_polynomials(first, second)`, which returns the list for
  `first` minus `second`, with like terms collected;
- `same_speed(first, second)`, which returns the crowd, in
  thousands, where two servers are equally fast, using `solve_linear`,
  or `None` when there is no single answer.

Then find all three crossings exactly, and put each one back into both
servers' rules.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `subtract_polynomials` has the shape of `add_polynomials` on
   [Rules with letters in them](tutorial:rules-with-letters-in-them#collecting-like-terms),
   with one `+` changed to `-`.
2. Small minus Medium is $(8 + 3g) - (15 + 1.25g) = -7 + 1.75g$, the
   list `[-7, 1.75]`.
3. `solve_linear(a, b)` solves $ax + b = 0$. Which place in the list is
   $a$, and which is $b$?

**Think about:** what should `same_speed` return for two servers
with the same time for each thousand people?

**Try this next:** find where Small and Medium meet with
`solve_simultaneous`, taking $g$ and the time $y$ as the two unknowns:
$-3g + y = 8$ and $-1.25g + y = 15$.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def subtract_polynomials(first, second):
    """Return the coefficients of first - second, with like terms collected."""
    difference = [0] * max(len(first), len(second))
    for power in range(len(first)):
        difference[power] = difference[power] + first[power]
    for power in range(len(second)):
        difference[power] = difference[power] - second[power]
    return difference


def same_speed(first, second):
    """Return the crowd, in thousands, where two servers [fixed, per thousand] are equally fast.

    Return None when there is no single answer.
    """
    difference = subtract_polynomials(first, second)
    return solve_linear(difference[1], difference[0])


for one, other in [("Small", "Medium"), ("Small", "Cluster"), ("Medium", "Cluster")]:
    thousands = same_speed(servers[one], servers[other])
    first_time = evaluate(servers[one], thousands)
    second_time = evaluate(servers[other], thousands)
    assert close_enough(first_time, second_time), (one, other)
    print(one, other, round(thousands, 2), round(first_time, 2))
```

```text
Small Medium 4.0 20.0
Small Cluster 7.33 30.0
Medium Cluster 12.0 30.0
```

Every crossing passes the check. The list is lowest power first, so the
number in front of $g$ is `difference[1]`. Small meets Cluster at
$7\frac{1}{3}$ thousand, a float, so the check uses `close_enough`.

The simultaneous route from the hint,
`solve_simultaneous(-3, 1, 8, -1.25, 1, 15)`, gives `(4.0, 20.0)`: the
same 4 thousand, and the time there too.

</details>

**7. Fix.** Schlomo wrote his own first `same_speed`. It gives an
answer, but the check after it fails. Run it, and read the message.
Find the line that makes the check fail, and change it.

```python exec
id: mixed-run-fix-order
def same_speed_first_try(first, second):
    """Return the crowd, in thousands, where two servers [fixed, per thousand] are equally fast."""
    difference = [first[0] - second[0], first[1] - second[1]]
    return solve_linear(difference[0], difference[1])


thousands = same_speed_first_try([8, 3], [15, 1.25])
print(thousands)
assert close_enough(evaluate([8, 3], thousands), evaluate([15, 1.25], thousands)), "the servers should be equally fast here"
print("Small and Medium are equally fast at", thousands, "thousand people.")
```

<details class="dl-answer"><summary>answer</summary>

It prints `0.25`, and then stops with
`AssertionError: the servers should be equally fast here`. At 0.25
thousand people, Small takes 8.75 ms and Medium about 15.31.

The difference is `[-7, 1.75]`, which is $-7 + 1.75g$. The call passes
$-7$ as $a$ and $1.75$ as $b$, so it solves $-7g + 1.75 = 0$, a
different equation. Swapping them fixes it:

```python
def same_speed_first_try(first, second):
    """Return the crowd, in thousands, where two servers [fixed, per thousand] are equally fast."""
    difference = [first[0] - second[0], first[1] - second[1]]
    return solve_linear(difference[1], difference[0])
```

Now it prints `4.0`, and the check passes. A coefficient list puts the
constant first, and $ax + b$ puts it last, so almost everyone
makes this swap once. Schlomo's check caught it.

</details>

**8. Make.** The chooser's main tool. Write
`fastest_server(servers, thousands)`, which returns the name of the
fastest server for that crowd. Test it at 2, 8 and 20 thousand, and
print the winning server's time each time.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep two names: the fastest server so far, and its time. Start both
   at `None`.
2. Loop over the names in `servers`, and find each server's time
   with `evaluate`.
3. If there is no fastest server yet, or this one is quicker, it becomes
   the fastest.

**Think about:** at exactly 4 thousand, Small and Medium tie. Which one
will your function return, and why?

**Try this next:** return the name and the time together, as a
pair.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def fastest_server(servers, thousands):
    """Return the name of the server that answers fastest with this many thousand people."""
    best_name = None
    best_time = None
    for name in servers:
        time = evaluate(servers[name], thousands)
        if best_time is None or time < best_time:
            best_name = name
            best_time = time
    return best_name


assert fastest_server(servers, 2) == "Small"
assert fastest_server(servers, 8) == "Medium"
assert fastest_server(servers, 20) == "Cluster"
for thousands in [2, 8, 20]:
    name = fastest_server(servers, thousands)
    print(thousands, name, evaluate(servers[name], thousands))
```

```text
2 Small 14
8 Medium 25.0
20 Cluster 30
```

At exactly 4 thousand it returns Small. A server that only ties is
not `<`, so it does not replace the one found first. Either would do
there.

</details>

**9. Make.** You also have an old server, and nobody wrote down its
numbers. You measure it twice. With 3 thousand people it took 17.5 ms.
With 7 thousand, it took 27.5 ms. Find its fixed time and its time for each
thousand with `solve_simultaneous`, and check both measurements. Then
add it to `servers` as `"Old"`. Is it ever the fastest?

<details class="dl-answer"><summary>answer</summary>

Call the fixed time $f$ and the time for each thousand $p$. The two
measurements are two facts: $f + 3p = 17.5$ and $f + 7p = 27.5$.

```python
fixed, per_thousand = solve_simultaneous(1, 3, 17.5, 1, 7, 27.5)
print(fixed, per_thousand)
print(fixed + 3 * per_thousand, fixed + 7 * per_thousand)

servers["Old"] = [fixed, per_thousand]
for thousands in [0, 2, 4, 6, 10, 20]:
    print(thousands, fastest_server(servers, thousands))
```

The old server takes 10 ms, plus 2.5 ms for each thousand, and both
measurements pass the check: `17.5 27.5`. By elimination, 4 thousand more
people add 10 ms, so each thousand adds 2.5 ms.

The old server is never the fastest. It beats Small above 4 thousand
and Medium below 4 thousand, and at 4 thousand all three take 20 ms.
Their lines cross at one point, $(4, 20)$.

</details>

**10. Explain.** The company adds Medium Plus: 20 ms and 1.25 ms for
each thousand, because it keeps a second copy of every change. What
does `same_speed(servers["Medium"], [20, 1.25])` return? What would
its line look like beside Medium's on a graph, and what does that mean
for someone choosing between them?

<details class="dl-answer"><summary>answer</summary>

It returns `None`. The difference is `[-5, 0]`, which is $-5 + 0g$,
and no $g$ makes $-5 = 0$.

The two lines have the same steepness, so they are parallel and never
cross, like the two backup readings on
[Several unknowns at once](tutorial:several-unknowns-at-once#when-there-is-no-single-answer).
Medium Plus is always 5 ms slower than Medium, so the crowd never
changes the choice. The question is whether a second copy of every
change is worth 5 ms to you. The algebra puts a number on that
question. It cannot answer it.

</details>

**11. Make.** A detour to the planets. In 1619 Johannes Kepler
published a rule for them: measure a planet's year $T$ in Earth years,
and its distance $a$ from the Sun in Earth distances, and then

$$T^2 = a^3$$

(The Earth's distance from the Sun, about 149.6 million km, is called
an astronomical unit, AU.) The cell loads NASA's numbers for the
eight planets and turns them into Earth years and AU. Run it, then:

1. For each planet, print $T^2$ and $a^3$ side by side. How close are
   they?
2. Draw Kepler's rule, $T = a^{1.5}$, with `plot_rule` from 0 to 32,
   and the eight planets as dots on the same picture.
3. How far out would a planet with a year of 2 Earth years be? Solve
   $a^3 = 4$ by undoing, and put your answer back in.
4. Ceres, a dwarf planet found in 1801, goes round the Sun in 4.6
   years. Where does the rule put it? NASA gives 2.768 AU.

```python exec
id: mixed-run-planets
planets = await load_csv("planet-orbits.csv")
names = planets["planet"].tolist()
distances = [km / 149.6 for km in planets["distance_million_km"].tolist()]
years = [days / 365.2 for days in planets["orbit_days"].tolist()]
for name, distance, year in zip(names, distances, years):
    print(name, round(distance, 3), "AU,", round(year, 3), "years")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over `zip(names, distances, years)` and print `year ** 2` and
   `distance ** 3`.
2. Write `def kepler(distance):` returning `distance ** 1.5`, and
   draw it. Then `plt.plot(distances, years, "o")`.
3. Undoing a cube is a cube root: `4 ** (1 / 3)`, as on
   [Running a formula backwards](tutorial:running-a-formula-backwards).
4. For Ceres, $a^3 = 4.6^2$.

**Think about:** Uranus was found in 1781 and Neptune in 1846. Kepler
died in 1630. What does it say that his rule fits them?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
for name, distance, year in zip(names, distances, years):
    print(name, round(year ** 2, 2), round(distance ** 3, 2))

def kepler(distance):
    """Return a planet's year, in Earth years, from its distance in AU, by Kepler's rule."""
    return distance ** 1.5

plot_rule(kepler, 0, 32)
plt.plot(distances, years, "o")
plt.xlabel("distance from the Sun, AU")
plt.ylabel("year, Earth years")

two_year_distance = 4 ** (1 / 3)
print(two_year_distance, round(two_year_distance * 149.6), "million km")
print(close_enough(two_year_distance ** 3, 4))

ceres = (4.6 ** 2) ** (1 / 3)
print(round(ceres, 3))
```

The two columns agree for every planet to within about 2.5%: Jupiter's
are 140.64 and 140.92, and Neptune, the furthest off, has 26,813 and
27,490. (Part of Neptune's gap is in the data: NASA counts its year
from one spring equinox to the next, 389 days short of a full turn
against the stars.)

A planet with a 2-year orbit would be about 1.587 AU out, about 237
million km, a little beyond Mars at 1.524. The rule puts Ceres at 2.766
AU, and NASA measures 2.768. I think this is the most surprising
number on the page. Kepler had six planets and no idea why the rule
held. It still holds for two planets and a dwarf planet found after his
death.

</details>

## Stretch

The stretch problems build the free-kick checker. A footballer chips a
free kick over the wall of defenders. Leaving out the air and the spin,
the ball's height in metres, $x$ metres along the ground from where it
is kicked, is

$$\text{height} = 0.025x(26 - x)$$

(This model has made-up numbers. A real ball slows in the air.) Here is a
scratch cell for the stretch problems.

```python exec
id: mixed-run-scratch-3
# Your free-kick checker, problem by problem
```

**12. Make.** Multiply out the brackets with a loop, as
`expand_brackets` did on
[Rules with letters in them](tutorial:rules-with-letters-in-them#expanding-brackets-is-a-loop).
Write it again here, from memory if you can, and get the height as a
list of coefficients. Then check the list against the brackets, every
half metre from 0 to 26 m.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $0.025x$ is the list `[0, 0.025]`, and $26 - x$ is `[26, -1]`.
2. The expanded list's length is `len(first) + len(second) - 1`.
3. A term at index `i` times a term at index `j` goes to index `i + j`.

**Think about:** why does the check need `close_enough`, and not `==`?

**Try this next:** find the list for a kick that lands 30 m away,
$0.025x(30 - x)$.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def expand_brackets(first, second):
    """Return the coefficients of first times second, with the brackets multiplied out."""
    expanded = [0] * (len(first) + len(second) - 1)
    for i in range(len(first)):
        for j in range(len(second)):
            expanded[i + j] = expanded[i + j] + first[i] * second[j]
    return expanded


height_rule = expand_brackets([0, 0.025], [26, -1])
print(height_rule)

for halves in range(0, 53):
    x = halves / 2
    assert close_enough(evaluate(height_rule, x), 0.025 * x * (26 - x))
print("The expanded rule agrees with the brackets.")
```

The list is `[0, 0.65, -0.025]`, so the height is
$-0.025x^2 + 0.65x$, and the check passes at all 53 points. It needs
`close_enough` because 0.025 is a float, and two routes to a float can
differ in the last digit.

</details>

**13. Make.** Find the top of the flight with `vertex`: how far along,
and how high? Then check it with a fine comb, as on
[The top of the curve](tutorial:the-top-of-the-curve#checking-with-a-fine-comb):
try every centimetre from 0 to 26 m, and find the greatest height.

<details class="dl-answer"><summary>answer</summary>

```python
top_x, top_height = vertex(-0.025, 0.65, 0)
print(top_x, round(top_height, 4))

places = []
heights = []
for centimetres in range(0, 2601):
    places.append(centimetres / 100)
    heights.append(evaluate(height_rule, centimetres / 100))

highest = largest(heights)
print(places[heights.index(highest)], round(highest, 4))
```

Both give 13 m along and a height of 4.225 m. The vertex is at
$x = -\frac{0.65}{2 \times (-0.025)} = 13$, and the $x^2$ term is
negative, so it is a maximum. The comb tried 2,601 places, and none is
higher.

</details>

**14. Another way.** Find where the top is with `solve_quadratic` and
no vertex formula. Where is the height 0? What does each of those
places mean for the kick?

<details class="dl-answer"><summary>answer</summary>

```python
roots = solve_quadratic(-0.025, 0.65, 0)
print(roots)
print((roots[0] + roots[1]) / 2)
```

The roots are 0 m, where the ball is kicked, and 26 m, where it lands.
(Python prints the first as `-0.0`: a float 0 that keeps a minus sign
from the division.)
Each is where one bracket of $0.025x(26 - x)$ is 0. The parabola's
two sides are mirror images, so its top is halfway between the roots, at 13 m, as on
[The top of the curve](tutorial:the-top-of-the-curve#halfway-between-the-roots).

</details>

**15. Predict.** The wall of defenders stands 9.15 m from the ball, as
the rules of football say, and a jumping defender reaches about 2.2 m.
Where along its flight is the ball above 2.2 m? Can it ever reach 5 m?
Each target gives an equation: the height, minus the target, equals 0.
Before you run the cell, say how many real roots each has. Then compare
the real part of the complex roots with problem 13.

```python
import cmath

def solve_quadratic_complex(a, b, c):
    """Return both roots of a*x**2 + b*x + c = 0 as complex numbers."""
    root = cmath.sqrt(b ** 2 - 4 * a * c)
    return [(-b - root) / (2 * a), (-b + root) / (2 * a)]

print(solve_quadratic(-0.025, 0.65, -2.2))
print(solve_quadratic(-0.025, 0.65, -5))
print(solve_quadratic_complex(-0.025, 0.65, -5))
```

<details class="dl-answer"><summary>answer</summary>

2.2 m has two real roots, 4 m and 22 m, and the ball is above 2.2 m
everywhere between them. The wall, at 9.15 m, is between, so the ball
clears it. Put each root back in, and the height is 2.2:

```python
for x in solve_quadratic(-0.025, 0.65, -2.2):
    print(round(x, 6), round(evaluate(height_rule, x), 6))
```

5 m has none, and `solve_quadratic` returns `[]`. The ball's highest
point is 4.225 m, so it never reaches 5 m. The discriminant agrees:
$0.65^2 - 4 \times (-0.025) \times (-5) = -0.0775$.

The complex roots are about $13 + 5.57i$ and $13 - 5.57i$. Their real
part is 13, the place of the top. The formula
is $-\frac{b}{2a}$, plus or minus a square root over $2a$, and
$-\frac{b}{2a}$ is the vertex. When the discriminant is negative, only
the plus-or-minus part becomes imaginary.

A place on a pitch is a real distance, so the question is about
$\mathbb{R}$, and the answer is "never". The complex roots are
true roots in $\mathbb{C}$, as on
[When there is no real answer](tutorial:when-there-is-no-real-answer#every-quadratic-has-roots-here),
but nobody can stand at them.

</details>

**16. Fix.** Schlomi tries the fine comb one centimetre at a time, and
her cell stops with an error. Read its last line, find the line that
causes it, and change it.

```python exec
id: mixed-run-fix-comb
highest_so_far = 0
for x in range(0, 26, 0.01):
    height_here = 0.025 * x * (26 - x)
    if height_here > highest_so_far:
        highest_so_far = height_here
        place_so_far = x
print(place_so_far, highest_so_far)
```

<details class="dl-answer"><summary>answer</summary>

The error is `TypeError: 'float' object cannot be interpreted as an
integer`. `range` works in the space of whole numbers. Its start, stop
and step must all be ints. Schlomi's idea, one centimetre at a time,
works. The loop needs to count in whole centimetres, and turn each
count into metres inside the loop. The stop is 2601, because `range` stops
before its last number:

```python
highest_so_far = 0
for centimetres in range(0, 2601):
    x = centimetres / 100
    height_here = 0.025 * x * (26 - x)
    if height_here > highest_so_far:
        highest_so_far = height_here
        place_so_far = x
print(place_so_far, round(highest_so_far, 4))
```

It prints `13.0 4.225`, the answer from problem 13. Counting in
whole centimetres also avoids adding 0.01 again and again, which would
add a small float error at every step.

</details>

**17. Explain.** Every answer on this page was checked by putting it
back into the rule it came from, and every check passed. Does that mean
a real ball, kicked the same way, clears the wall? What does a
substitution check prove, and what can it not prove?

<details class="dl-answer"><summary>answer</summary>

A substitution check proves that an answer fits its rule, so the
algebra and the code agree with each other. It caught the swapped
argument in problem 7 at once.

It cannot prove that the rule fits the world. The ball's rule is a
model. It leaves out the air and the spin. A real ball slows in the
air, so its flight is shorter and lower than the model's. Every check
on this page would still pass, and the real ball might still hit the
wall. The step from the world to the rule needs other evidence, such as
a video of real kicks.

The planets are different. Kepler's rule was checked against
measurements of every planet, and then of Ceres. So was the letter's
bowl on
[The top of the curve](tutorial:the-top-of-the-curve#a-letter-that-sits-below-the-line),
in its own way. Its rule came from the font's own points, so the
bottom that `vertex` found is the real bottom of the letter. An answer
that names both steps says two things: the answer fits the rule, and
here is why we trust the rule.

</details>
