---
title: "Lines and Distances — Practice"
slug: lines-and-distances-practice
practice_for: lines-and-distances
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Lines and Distances — Practice

Answers are folded. Write something down before you unfold.

## Tools

```python exec
id: tools-1
import math

def slope(p, q):
    (x1, y1), (x2, y2) = p, q
    return (y2 - y1) / (x2 - x1)


def midpoint(p, q):
    (x1, y1), (x2, y2) = p, q
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


print(slope((0, 0), (3, 6)))
print(midpoint((1, 2), (7, 6)))
print(distance((0, 0), (3, 4)))
```

## Slope

**1.** Find the slope of the line through each pair.

- (a) `(0, 0)` and `(4, 8)`
- (b) `(2, 5)` and `(6, 1)`
- (c) `(-3, -2)` and `(1, 6)`
- (d) `(4, 7)` and `(9, 7)`

<details class="dl-answer"><summary>answer</summary>

(a) 2. (b) −1. (c) 2. (d) 0.

The last one is horizontal — y does not change at all when x does, so the rate of change is nothing.

</details>

**2.** What is the slope of the line through `(3, 1)` and `(3, 9)`?

<details class="dl-answer"><summary>answer</summary>

There is none. Both points have x = 3, so the run is zero and the division fails.

"How much does y change when x goes up by one" has no answer, because x never goes up on this line. This is the case `y = mx + c` cannot describe, and it is why `ax + by + c = 0` exists.

</details>

**3.** A line passes through `(1, 4)`, `(3, 10)` and `(6, k)`. Find `k`.

<details class="dl-answer"><summary>answer</summary>

The slope from the first two points is (10 − 4)/(3 − 1) = 3. Straight means the slope is the same everywhere, so from `(1, 4)` to `(6, k)` it must also be 3: `(k − 4)/(6 − 1) = 3`, so `k = 19`.

</details>

**4.** A mobile plan charges €12 a month plus 6 cent a minute. Write it as `y = mx + c`, and say what each of the two numbers means.

<details class="dl-answer"><summary>answer</summary>

`y = 0.06x + 12`, where x is minutes and y is euro.

The 0.06 is the rate — what one more minute costs. The 12 is what you pay for zero minutes, which is the standing charge.

</details>

**5.** Two points on a line are `(10, 250)` and `(30, 610)`, where x is items produced and y is total cost in euro. What is the cost per item, and what is the fixed cost?

<details class="dl-answer"><summary>answer</summary>

Slope = (610 − 250)/(30 − 10) = 18, so €18 per item.

Working back to x = 0: 250 − 10 × 18 = 70, so €70 fixed.

</details>

## Parallel and Perpendicular

**6.** Which of these are parallel, and which perpendicular?

- (a) `y = 3x + 1`
- (b) `y = 3x − 7`
- (c) `y = -x/3 + 2`
- (d) `y = x/3`

<details class="dl-answer"><summary>answer</summary>

(a) and (b) are parallel — the same slope of 3.

(c) is perpendicular to both (a) and (b): 3 × (−1/3) = −1.

(d) is none of the above. A slope of 1/3 is not −1/3, and it is easy to miss the sign.

</details>

**7.** Find the line through `(2, 3)` perpendicular to `y = 4x − 1`.

<details class="dl-answer"><summary>answer</summary>

The perpendicular slope is −1/4. Through `(2, 3)`: `3 = −1/4 × 2 + c`, so `c = 3.5`.

`y = −0.25x + 3.5`.

</details>

**8.** A triangle has corners at `(0, 0)`, `(4, 0)` and `(4, 3)`. Is it right-angled? Show it two ways.

<details class="dl-answer"><summary>answer</summary>

Yes, at `(4, 0)`.

By slopes: the side from `(0,0)` to `(4,0)` has slope 0 and the side from `(4,0)` to `(4,3)` is vertical, so they meet at a right angle.

By Pythagoras: the sides are 4, 3 and 5, and 16 + 9 = 25.

</details>

**9.** Why does the perpendicular rule multiply to −1 rather than to some other number?

<details class="dl-answer"><summary>answer</summary>

Turning a right triangle a quarter turn swaps its rise and its run, and makes one of them negative. So a slope of `rise/run` becomes `run/(−rise)`, or `(−run)/rise`.

Multiply those together and the rise and run cancel completely, leaving −1. It is the swapping that makes everything cancel, and the negation is all that survives.

</details>

## The General Form

**10.** Write each in the form `ax + by + c = 0`.

- (a) `y = 2x + 5`
- (b) `y = -3x`
- (c) the vertical line through `(7, 0)`
- (d) the horizontal line through `(0, -4)`

<details class="dl-answer"><summary>answer</summary>

(a) `2x − y + 5 = 0`. (b) `3x + y = 0`. (c) `x − 7 = 0`. (d) `y + 4 = 0`.

Only (c) could not have been written as `y = mx + c`.

</details>

**11.** Convert `3x + 4y − 12 = 0` into slope-intercept form, and find where it crosses each axis.

<details class="dl-answer"><summary>answer</summary>

`4y = −3x + 12`, so `y = −0.75x + 3`.

It crosses the vertical axis at 3 (set x = 0) and the horizontal axis at 4 (set y = 0).

</details>

**12.** What does `ax + by + c = 0` become when `b = 0`? And when `a = 0`?

<details class="dl-answer"><summary>answer</summary>

`b = 0` gives `ax + c = 0`, so `x = −c/a` — a vertical line, which is the case the other forms cannot manage.

`a = 0` gives `by + c = 0`, so `y = −c/b` — a horizontal line, which they can.

Both zero would give `c = 0`, which is either every point or none, and is not a line.

</details>

## Midpoint and Distance

**13.** Find the midpoint of `(2, 8)` and `(6, 2)`; of `(-3, 4)` and `(5, -2)`.

<details class="dl-answer"><summary>answer</summary>

(4, 5) and (1, 1).

</details>

**14.** The midpoint of a segment is `(3, 1)` and one end is `(7, 4)`. Where is the other end?

<details class="dl-answer"><summary>answer</summary>

`(-1, -2)`.

The midpoint is the average, so the other end is the midpoint moved by the same amount again: `(3 − 4, 1 − 3)`.

</details>

**15.** Find the distance between each pair.

- (a) `(0, 0)` and `(3, 4)`
- (b) `(1, 2)` and `(4, 6)`
- (c) `(-2, 3)` and `(4, -1)`
- (d) `(5, 5)` and `(5, 12)`

<details class="dl-answer"><summary>answer</summary>

(a) 5. (b) 5. (c) √52 ≈ 7.211. (d) 7.

The last one needed no square root — the points are on a vertical line, so the distance is the difference in the y values.

</details>

**16.** A triangle has corners `(0, 0)`, `(6, 0)` and `(3, 4)`. Is it isosceles?

<details class="dl-answer"><summary>answer</summary>

Yes. The base is 6, and both sloping sides are √(9 + 16) = 5.

</details>

**17.** Two servers in a data centre are at grid positions `(12, 30)` and `(45, 74)`, in metres. A cable runs directly between them. How long does it need to be?

<details class="dl-answer"><summary>answer</summary>

√(33² + 44²) = √(1089 + 1936) = √3025 = 55 m.

That is a 3-4-5 triangle scaled by 11 — worth noticing, because those turn up constantly and spotting one saves a calculation.

</details>

**18.** Show that `(1, 2)`, `(4, 6)` and `(8, 3)` form a right-angled triangle, and say which corner has the right angle.

<details class="dl-answer"><summary>answer</summary>

The three side lengths are 5, 5 and √50. Since 25 + 25 = 50, Pythagoras holds and the right angle is at `(4, 6)` — the corner opposite the longest side.

It is also isosceles, which the two equal sides give away.

</details>

**19.** Why is the distance formula the same thing as Pythagoras?

<details class="dl-answer"><summary>answer</summary>

Draw the horizontal gap and the vertical gap between two points. They meet at a right angle, and the direct distance is the third side of that triangle.

So `distance² = across² + up²` is literally `c² = a² + b²`, with the two short sides being the two gaps. Neither is a special case of the other — they are one statement.

</details>

## Putting It Together

**20.** A drone is at `(0, 0)` and two landing pads are at `(30, 40)` and `(-20, 45)`. Which is closer, and by how much?

<details class="dl-answer"><summary>answer</summary>

The first is at distance 50; the second at √(400 + 2025) = √2425 ≈ 49.24.

The second is closer, by about 0.76 — which is close enough that guessing from the picture would have been unreliable.

</details>

**21.** Find the point on the horizontal axis that is the same distance from `(0, 4)` and `(6, 2)`.

<details class="dl-answer"><summary>answer</summary>

Call it `(x, 0)`. Then `x² + 16 = (x − 6)² + 4`, which gives `x² + 16 = x² − 12x + 40`, so `12x = 24` and `x = 2`.

The point is `(2, 0)`, and it is 2√5 from each.

</details>

**22.** A circle has centre `(3, 1)` and passes through `(7, 4)`. What is its radius, and is `(0, 5)` inside or outside it?

<details class="dl-answer"><summary>answer</summary>

The radius is the distance from centre to the known point: √(16 + 9) = 5.

`(0, 5)` is √(9 + 16) = 5 from the centre — exactly on the circle, neither inside nor out.

</details>

**23.** Write a function that takes three points and says whether they lie on one straight line.

<details class="dl-answer"><summary>answer</summary>

Compare the slopes between the first pair and the second pair; if they are equal, the three are collinear.

```python
def collinear(p, q, r):
    return abs(slope(p, q) - slope(q, r)) < 1e-9
```

The tolerance matters — comparing floats for exact equality will report perfectly straight triples as bent. And it fails if any pair is vertical, which is worth guarding: comparing `(y2−y1)(x3−x2)` with `(y3−y2)(x2−x1)` avoids dividing at all.

</details>
