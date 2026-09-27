---
title: "Mixed problems: maths and programming, the whole course"
practice_across:
  - writing-your-own-functions
  - lists-and-sequences
  - putting-things-in-order
  - logic-and-truth
  - what-are-the-chances
  - making-sense-of-data
  - cracking-equations
  - parabolas
  - numbers-and-their-families
  - distance-and-pythagoras
  - the-unit-circle
  - solving-triangles
  - rates-of-change
year: "2026-2027"
version: 2026.09.27.1
worlds:
  fantasy-maps: A made-up kingdom, with its roads drawn on a grid.
  planets-and-moons: The Moon going round the Earth, with its orbit drawn as a circle.
  games-of-chance: Dice, cards and coins, and the games people play with them.
---

# Mixed problems: maths and programming, the whole course

These problems come from every series of the course, programming and
mathematics mixed together, and do not say which series each one comes
from. Choosing the idea is the first half of every problem.

```python exec
id: mixed-maths-and-programming-tools
import math
import random
```

## 1.

The median of a list is the middle value once the list is sorted. With
an even number of values, it is the average of the two middle ones. Can
you write `median(values)`?

```python exec
id: mixed-maths-and-programming-median
def median(values):
    """The middle value, or the average of the two middle values."""
    # Your code here.
```

```hint
Sort a copy of the list first. If `n` values are sorted, the middle
position is `n // 2`. For an even `n`, you need the value just before
it too.
```

```inputs
median([3, 1, 2])
median([4, 1, 3, 2])
median([7])
median([10, 2, 38, 23, 38, 23, 21])
```

```solution
title: with what you've met so far
def median(values):
    """The middle value, or the average of the two middle values."""
    ordered = sorted(values)
    n = len(ordered)
    middle = n // 2
    if n % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2
---
For [4, 1, 3, 2], the sorted list is [1, 2, 3, 4], and the two middle values are 2 and 3, so the median is 2.5.
```

```solution
title: a shorter way you'll meet later
import statistics


def median(values):
    """The middle value, or the average of the two middle values."""
    return statistics.median(values)
---
Python's own `statistics` module has a `median()` that does the same.
```

## 2.

Two dice are rolled. What is the chance that they add up to 7? The cell
rolls them 6,000 times.

```python exec
id: mixed-maths-and-programming-dice
random.seed(1)
sevens = 0
for _ in range(6000):
    if random.randint(1, 6) + random.randint(1, 6) == 7:
        sevens += 1
print(sevens / 6000)
```

```predict
type: number
tolerance: 0.02

About what share of the 6,000 rolls add up to 7?
```

Of the 36 ways two dice can land, 6 add up to 7: 1 and 6, 2 and 5, 3
and 4, and the same three the other way round. So the chance is
$6 \div 36 = 1 \div 6$, about 0.167. The simulation comes close, and
no other total has as many ways.

## 3.

The cell checks a rule of logic for every pair of `True` and `False`.

```python exec
id: mixed-maths-and-programming-de-morgan
holds = True
for a in [True, False]:
    for b in [True, False]:
        if (not (a and b)) != ((not a) or (not b)):
            holds = False
print(holds)
```

```predict
type: choice

Is "not (a and b)" always the same as "(not a) or (not b)"? What will
the cell print?

- True
- False
  - The "and" turned into "or", which looks like it should change the
    answer.
```

It prints `True`. "Not both" means the same as "at least one of them
is not". This is one of De Morgan's laws, and the other is its mirror:
"not (a or b)" is the same as "(not a) and (not b)". Four pairs are
all the cases there are, so the loop is a proof, not only a test.

## 4.

Solve $3x + 7 = 22$ by hand. Then check your answer in a cell by
putting it back.

```python exec
id: mixed-maths-and-programming-solve
```

<details class="dl-answer"><summary>one way through it</summary>

Take 7 from both sides: $3x = 15$. Divide both sides by 3: $x = 5$.
To check it, `3 * 5 + 7 == 22` gives `True`. Putting the answer back
into the equation is a check that needs no trust in the working.

</details>

## 5.

The cell tries $x$ from 0 to 6 in steps of 0.5, and prints the
smallest value of $2(x - 3)^2 + 1$ it finds.

```python exec
id: mixed-maths-and-programming-lowest
lowest = None
for i in range(13):
    x = i * 0.5
    y = 2 * (x - 3) ** 2 + 1
    if lowest is None or y < lowest:
        lowest = y
print(lowest)
```

```predict
type: number

What is the smallest value it finds?
```

1, at $x = 3$. In the form $a(x - h)^2 + k$, the vertex is at
$(h, k) = (3, 1)$. The squared part is never below 0, so the smallest
it can be is 0, at $x = 3$, and then $y$ is 1. The search only
confirms what the form already says.

## 6.

A ladder 5 metres long leans against a wall, at 60° to the ground. How
high up the wall does it reach? How far is its foot from the wall?

```python exec
id: mixed-maths-and-programming-ladder
```

<details class="dl-hint"><summary>hint</summary>

The ladder is the longest side of a right-angled triangle. The height
is opposite the 60° angle.

</details>

<details class="dl-answer"><summary>one way through it</summary>

The height is $5 \sin 60° \approx 4.33$ metres, and the foot is
$5 \cos 60° = 2.5$ metres from the wall. In Python,
`5 * math.sin(math.radians(60))` gives 4.330. Check with Pythagoras:
$4.33^2 + 2.5^2 \approx 25 = 5^2$.

</details>

## 7.

Can you write `slope(f, x, h)`? It returns the slope of the function
`f` at `x`, estimated as $\dfrac{f(x + h) - f(x)}{h}$.

```python exec
id: mixed-maths-and-programming-slope
def square(x):
    return x * x


def slope(f, x, h):
    """The slope of f at x, from a small step h."""
    # Your code here.
```

```hint
Call `f` twice: once at `x + h` and once at `x`.
```

```inputs
round(slope(square, 3, 0.1), 6)
round(slope(square, 3, 0.001), 6)
round(slope(math.sin, 0, 0.001), 6)
```

```solution
def slope(f, x, h):
    """The slope of f at x, from a small step h."""
    return (f(x + h) - f(x)) / h
---
The slope of x² at 3 is exactly 6. A step of 0.1 gives 6.1, and a step of 0.001 gives 6.001: the estimate is always too big by the step itself, so a smaller step is closer. The slope of sin at 0 is 1.
```

## 8.

Can you write `doublings_to_pass(target)`? It starts at 1, doubles
until the number is larger than `target`, and returns how many
doublings that took.

```python exec
id: mixed-maths-and-programming-doublings
def doublings_to_pass(target):
    """How many doublings, starting from 1, take the number past target."""
    # Your code here.
```

```hint
A `while` loop, with a count that goes up by 1 each time the number
doubles.
```

```inputs
doublings_to_pass(1)
doublings_to_pass(1000)
doublings_to_pass(1000000)
```

```solution
title: with what you've met so far
def doublings_to_pass(target):
    """How many doublings, starting from 1, take the number past target."""
    number = 1
    count = 0
    while number <= target:
        number = number * 2
        count += 1
    return count
---
10 doublings pass 1,000, since 2¹⁰ = 1,024, and 20 pass 1,000,000. The count is one more than the base-2 logarithm, rounded down: 1,000 times more takes only 10 more doublings.
```

```solution
title: a shorter way you'll meet later
def doublings_to_pass(target):
    """How many doublings, starting from 1, take the number past target."""
    return math.floor(math.log2(target)) + 1
```

## 9.

A classmate wrote `double(n)` so that it prints `n * 2`. Then
`double(3) + 1` gives an error. Why? What should `double` do instead?

<details class="dl-answer"><summary>answer</summary>

A function that prints shows a number on the screen, but it gives
nothing back: it returns `None`. So `double(3) + 1` asks Python to add
`None` and 1, which it cannot do. `double` should `return n * 2`. Then
the caller can print the result, add to it, or store it.

</details>

## In your world

<div class="dl-world" data-world="fantasy-maps">

The towns of a kingdom, as $(x, y)$ positions on a grid, in kilometres.
Can you write `distance(a, b)`? It returns the straight-line distance
between two positions.

```python exec
id: in-your-world-1--fantasy-maps
towns = {"Ashfall": (0, 0), "Brindle": (3, 4), "Corrow": (-5, 12), "Dunmere": (6, -8)}


def distance(a, b):
    """The straight-line distance between two (x, y) positions."""
    # Your code here.
```

```hint
Find how far apart the two positions are across and up. Then use
Pythagoras.
```

```inputs
distance(towns["Ashfall"], towns["Brindle"])
distance(towns["Ashfall"], towns["Corrow"])
distance(towns["Brindle"], towns["Dunmere"])
```

```solution
def distance(a, b):
    """The straight-line distance between two (x, y) positions."""
    across = b[0] - a[0]
    up = b[1] - a[1]
    return math.sqrt(across ** 2 + up ** 2)
---
Ashfall to Brindle is 5 km, and Ashfall to Corrow 13 km: both whole numbers, from the 3, 4, 5 and 5, 12, 13 triangles. Brindle to Dunmere is the square root of 153, about 12.37 km.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

A moon goes round its planet in a circle. It starts at angle 0, and
takes `period` hours to go all the way round. Can you write
`moon_position(radius, period, hours)`? It returns the moon's
$(x, y)$ position after `hours`, each rounded to 1 decimal place.

```python exec
id: in-your-world-1--planets-and-moons
def moon_position(radius, period, hours):
    """The (x, y) position after `hours`, on a circle of `radius`."""
    # Your code here.
```

```hint
After `hours`, the moon has turned through `2 * math.pi * hours /
period` radians. The unit circle gives the point at that angle; the
radius stretches it.
```

```inputs
moon_position(10, 24, 0)
moon_position(10, 24, 6)
moon_position(10, 24, 12)
moon_position(384, 655, 100)
```

```solution
def moon_position(radius, period, hours):
    """The (x, y) position after `hours`, on a circle of `radius`."""
    angle = 2 * math.pi * hours / period
    return (round(radius * math.cos(angle), 1), round(radius * math.sin(angle), 1))
---
After a quarter of the period, the moon is at (0, 10), a quarter turn round, and after half, at (-10, 0). The Moon is about 384,000 km from the Earth, so a radius of 384 counts in thousands of km. It goes round in about 655 hours, so 100 hours take it about 55° round.
```

</div>

<div class="dl-world" data-world="games-of-chance">

A game pays out different amounts with different chances. Its
*expected value* is what it pays on average, per game, over many
games. Can you write `expected_value(outcomes)`? `outcomes` is a list
of `(chance, payout)` pairs, and it returns the sum of each chance
times its payout.

```python exec
id: in-your-world-1--games-of-chance
die_game = [(1 / 6, 6), (5 / 6, -1)]
coin_game = [(0.5, 2), (0.5, -2)]


def expected_value(outcomes):
    """The average payout per game: the sum of chance times payout."""
    # Your code here.
```

```hint
Start a total at 0, and add `chance * payout` for each pair.
```

```inputs
round(expected_value(die_game), 4)
expected_value(coin_game)
round(expected_value([(0.25, 10), (0.75, -4)]), 4)
```

```solution
title: with what you've met so far
def expected_value(outcomes):
    """The average payout per game: the sum of chance times payout."""
    total = 0
    for chance, payout in outcomes:
        total = total + chance * payout
    return total
---
The die game wins €6 on a six and loses €1 otherwise: on average it pays about €0.17 a game. The coin game is fair: 0 on average. The third game pays €10 a quarter of the time and loses €4 otherwise, so on average it loses €0.50 a game. The die game wins only one time in six, yet pays on average. How often a game wins does not decide what it pays.
```

```solution
title: a shorter way you'll meet later
def expected_value(outcomes):
    """The average payout per game: the sum of chance times payout."""
    return sum(chance * payout for chance, payout in outcomes)
```

</div>
