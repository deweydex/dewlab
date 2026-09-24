---
title: "Measuring rooms and tins: area, perimeter and volume — Practice"
practice_for: measuring-rooms-and-tins
year: "2026-2027"
version: 2026.09.24.1
---

# Measuring rooms and tins: area, perimeter and volume — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, so every shape tool from the
tutorial is here: `rectangle_perimeter`, `rectangle_area`,
`triangle_area`, `circle_circumference`, `circle_area`, the four volumes
and the four surface areas. So are `compose`, `total` and `simulate`
from earlier pages. The cell below imports `math` for the whole page.
Run it first.

```python exec
id: measuring-practice-start
import math

print(rectangle_area(4, 3.5), circle_area(1))
```

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: measuring-practice-warm-up
# Try things here
```

**1. Predict.** A picture frame is 5 cm by 2 cm, and a small square tile
is 3 cm on each side. What does each line print?

```python
print(rectangle_perimeter(5, 2))
print(rectangle_area(5, 2))
print(rectangle_area(3, 3))
```

<details class="dl-answer"><summary>answer</summary>

`14`, `10` and `9`.

Round the frame: $5 + 2 + 5 + 2 = 14$ cm. The frame covers
$5 \times 2 = 10$ cm². The tile is a square, so its area is $3^2 = 9$ cm².
The first answer is a length, in cm, and the other two are areas, in cm².

</details>

**2. Make.** A full-size GAA pitch can be up to 145 m long and 90 m
wide. How far is it round the pitch? How much grass does it cover? Use
your toolkit.

<details class="dl-answer"><summary>answer</summary>

```python
print(rectangle_perimeter(145, 90), "m round the edge")
print(rectangle_area(145, 90), "m² of grass")
```

This prints `470 m round the edge` and `13050 m² of grass`. That is
more than 1.3 hectares: a hectare is 10,000 m².

</details>

**3. Explain.** A friend measures a square room, 4 m on each side. "Its
area is 16 and its perimeter is 16," they say, "so the area and the
perimeter are the same." What would you say to them?

<details class="dl-answer"><summary>answer</summary>

The two 16s are in different spaces. The perimeter is 16 metres, a
length. The area is 16 square metres, a count of squares. They only
look equal because the numbers happen to match.

Change the units and the match goes away. In centimetres, the room is
400 cm on each side: its perimeter is 1,600 cm, and its area is
160,000 cm². A length and an area cannot be the same, in the same way
that 16 minutes and 16 euro cannot.

</details>

**4. Predict.** A vinyl record is 30 cm across. Roughly how long is its
edge, all the way round? Guess first, then use `circle_circumference`.
Be careful: which number does the function want?

<details class="dl-answer"><summary>answer</summary>

```python
print(circle_circumference(15))
```

About 94.2 cm. The function wants the radius, which is half of 30 cm.
A quick check: the edge is a bit more than 3 times the distance across,
and $3 \times 30 = 90$.

</details>

## Core

A cell for your core answers.

```python exec
id: measuring-practice-core
# Try things here
```

**5. Make.** A garden shed has a flat roof, 3 m by 2 m. In a year,
Dublin gets about 750 mm of rain. If all the rain on the roof ran into a
barrel, how many litres would it collect? Picture the year's rain as a
layer of water on the roof, 0.75 m deep. One cubic metre is 1,000
litres.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The layer of water is a cuboid. What are its length, width and
   height, in metres?
2. `cuboid_volume` gives cubic metres.
3. Multiply by 1,000 for litres.

**Think about:** why 750 mm must become 0.75 m before you multiply.

**Try this next:** many places in the west of Ireland get more than
1,200 mm a year. How much would the same shed collect there?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
rain_m3 = cuboid_volume(3, 2, 0.75)
print(rain_m3 * 1000, "litres")
```

This prints `4500.0 litres`. Every length must be in the same unit,
metres, before we multiply. Otherwise the answer mixes metres and
millimetres, and means nothing.

</details>

**6. Fix.** A pizza menu gives each size as a diameter. This function is
meant to give a pizza's area from its diameter, but the test fails. Run
it, then find and fix the mistake.

```python exec
id: measuring-practice-fix-pizza
def pizza_area(diameter):
    """Return the area in cm² of a round pizza, given its diameter in cm."""
    return circle_area(diameter)


assert round(pizza_area(40)) == 1257
print("pizza_area keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Print `pizza_area(40)` on its own. Is it too big or too small?
2. By how many times?
3. Read the docstring of `circle_area` with `help(circle_area)`. Which
   measurement does it want?

**Think about:** why the answer is four times too big, not twice.

</details>

<details class="dl-answer"><summary>answer</summary>

`circle_area` wants the radius, and it was given the diameter. The
radius is half the diameter:

```python
def pizza_area(diameter):
    """Return the area in cm² of a round pizza, given its diameter in cm."""
    return circle_area(diameter / 2)
```

Now the test passes. The wrong version gave 5,027 cm², four times too
much. Doubling the radius doubles it twice, because the radius is
squared.

</details>

**7. Another way.** The tutorial found a cylinder's surface area as two
circles plus a label. Peel the label off and it is a rectangle. Find
the surface area of a tin with radius 4 cm and height 10 cm in two ways:
once with `cylinder_surface_area`, and once by adding two circles to a
rectangle, using `circle_area`, `circle_circumference` and
`rectangle_area`. Do they agree?

<details class="dl-answer"><summary>answer</summary>

```python
first_way = cylinder_surface_area(4, 10)
label = rectangle_area(circle_circumference(4), 10)
second_way = 2 * circle_area(4) + label
print(first_way, second_way)
```

Both are `351.85837720205683` cm². The label's length is the
circumference, because it went once round the tin.

</details>

**8. Predict.** A dice maker doubles the size of a cube, from 2 cm on
each side to 4 cm. How many times more plastic does it need inside? How
many times more paint to cover it? Guess both, then check with
`cuboid_volume` and `cube_surface_area`.

<details class="dl-answer"><summary>answer</summary>

```python
print(cuboid_volume(4, 4, 4) / cuboid_volume(2, 2, 2))
print(cube_surface_area(4) / cube_surface_area(2))
```

This prints `8.0` and `4.0`. The volume goes up 8 times, $2^3$, because
it is length times length times length. The surface area goes up 4
times, $2^2$, because it is length times length. Double every length of
any solid, and its volume is 8 times bigger, but its outside only 4
times.

</details>

**9. Make.** A recipe asks for a round cake tin, 20 cm across. You only
have a square tin, 18 cm on each side. Both are 7 cm deep. Which holds
more cake mix, and by how much?

<details class="dl-answer"><summary>answer</summary>

```python
round_tin = cylinder_volume(10, 7)
square_tin = cuboid_volume(18, 18, 7)
print(round(round_tin), round(square_tin), round(square_tin - round_tin))
```

This prints `2199 2268 69`. The square tin holds about 69 cm³ more, a
little over 3%. So the recipe fits the square tin, and the cake may
need a few minutes less, because it is slightly thinner.

</details>

**10. Explain.** A school trip has 53 students, and a minibus seats 16.
Three programmers work out how many minibuses to book:

```python
print(round(53 / 16))
print(53 // 16)
print(math.ceil(53 / 16))
```

They get 3, 3 and 4. Which is right, and why are the other two wrong
here?

<details class="dl-answer"><summary>answer</summary>

`math.ceil` is right: 4 minibuses. $53 \div 16 = 3.3125$, so three
minibuses carry 48 students, and 5 would be left at the school.

`round` goes to the nearest whole number, which is 3. `//` keeps only
the whole part, which is also 3. Both would be right for a different
question, such as "how many minibuses can we fill completely?". Here
minibuses come whole, and everyone must travel, so any part of a
minibus means one more minibus. That is rounding up.

</details>

**11. Fix.** Someone wrote their own function for the volume of a ball.
The test uses Archimedes' rule from the tutorial: a sphere fills two
thirds of the cylinder that fits round it. The test fails. Run it, then
find and fix the mistake.

```python exec
id: measuring-practice-fix-ball
def ball_volume(radius):
    """Return the volume of a ball of this radius."""
    return 4 / 3 * math.pi * radius ** 2


fits_round = cylinder_volume(3, 6)   # radius 3, height 6: the ball fits exactly inside
assert round(ball_volume(3), 6) == round(2 / 3 * fits_round, 6)
print("ball_volume keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The formula is $V = \frac{4}{3}\pi r^3$. Compare it with the code,
   one piece at a time.
2. What unit would `radius ** 2` give, if the radius is in cm?
3. Is a volume in cm² or cm³?

**Think about:** how checking the units finds this mistake before any
test runs.

</details>

<details class="dl-answer"><summary>answer</summary>

The radius is squared, but a volume needs it cubed:

```python
def ball_volume(radius):
    """Return the volume of a ball of this radius."""
    return 4 / 3 * math.pi * radius ** 3
```

Now the test passes. The wrong version gave about 37.7 cm³ in place of
113.1 cm³. A units check finds it too: $r^2$ is an area, and no number
times an area is a volume.

</details>

## Stretch

**12. Make.** A tablet capsule is a cylinder with half a sphere on each
end. Its radius is 0.3 cm, and the cylinder part is 1.2 cm long. How
much medicine can it hold? Say how you put it together from your
toolkit.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Picture the capsule in three pieces: two half-spheres and a cylinder.
2. Two half-spheres of the same radius make one whole sphere.
3. Add the two volumes.

**Think about:** how you would find the plastic needed to make the
capsule's outside.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
capsule = cylinder_volume(0.3, 1.2) + sphere_volume(0.3)
print(round(capsule, 3), "cm³")
```

This prints `0.452 cm³`, a little under half a millilitre. The two
half-spheres make one sphere, so the capsule is one cylinder and one
sphere, added together.

</details>

**13. Make.** A pizza shop sells three sizes: 25 cm for €9, 30 cm for
€12 and 40 cm for €16. Which gives the most pizza for each euro? Write a
loop over the three sizes, as on
[Doing it again](tutorial:doing-it-again), and print the price of one
square centimetre of each, in cent.

<details class="dl-answer"><summary>answer</summary>

```python
menu = [(25, 9), (30, 12), (40, 16)]
for diameter, price in menu:
    area = circle_area(diameter / 2)
    print(diameter, "cm:", round(price * 100 / area, 2), "cent per cm²")
```

This prints `1.83`, `1.7` and `1.27` cent per cm². The large pizza
costs most, but it is the best value by far. The price goes up with the
diameter, but the area goes up with the diameter squared.

</details>

**14. Another way.** Here is a way to find $\pi$ with chance, using
`simulate` from [How likely is it?](tutorial:how-likely-is-it). Picture
a square 1 unit on each side, with a quarter circle of radius 1 drawn
from one corner. Drop a point anywhere in the square, at random. The
chance that it lands inside the quarter circle is the quarter circle's
area divided by the square's: $\frac{\pi}{4}$. Write a trial that drops
one point and says whether it landed inside, simulate it many times,
and multiply by 4.

```python exec
id: measuring-practice-random-pi
import random

# Your trial, and the estimate of pi
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `random.random()` gives a number from 0 to 1. Use it twice, for `x`
   and `y`.
2. The point is inside the quarter circle when its distance from the
   corner is less than 1. That is when $x^2 + y^2 < 1$.
3. `simulate(inside, 100000)` gives the fraction of points inside.

**Think about:** how many runs you need before the first two decimal
places stop changing.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import random

def inside():
    """Drop one random point in the unit square; True if it lands in the quarter circle."""
    x = random.random()
    y = random.random()
    return x ** 2 + y ** 2 < 1

print(4 * simulate(inside, 100000))
print(math.pi)
```

The first line prints a number close to 3.14, such as 3.1418. Yours
will be a little different on every run, because the points are random.
With more runs it usually comes closer to `math.pi`, but slowly: to get
one more correct digit, you need about 100 times as many points. The
string and the dinner plate from the tutorial were one route to $\pi$.
This is another.

</details>

**15. Make.** A traffic cone is 45 cm tall, and its base has a radius of
15 cm. Its orange plastic covers only the sloping side. The base is
open. How much orange plastic is there, in cm²? Use
`cone_surface_area`, and think about which part to leave out.

<details class="dl-answer"><summary>answer</summary>

```python
sloping_side = cone_surface_area(15, 45) - circle_area(15)
print(round(sloping_side), "cm²")
```

This prints `2235 cm²`. `cone_surface_area` gives the base circle and
the sloping side together, so we take the circle away. Another route is
the formula for the side alone, $\pi r l$, with
$l = \sqrt{15^2 + 45^2}$: it gives the same 2,235 cm².

</details>
