# Outline — The Unit Circle

**Closes:** `MIT-4.5` (degree and radian measure), `MIT-4.6` (sin, cos, tan and
the unit circle), `MIT-4.7` (trigonometric ratios in surd form).
**Goes after:** [Lines and Distances](./lines-and-distances.md).
**Followed by:** [Sine and Cosine Waves](./sine-and-cosine-waves.md), then
[Solving Triangles](./solving-triangles.md).
**Builds on:** Lines and Distances — a point on a circle of radius one is a
coordinate-geometry object, and the distance formula is what makes the identity
true.
**Size:** full.

## Why the circle is the tutorial rather than a step on the way to one

This was a section of *Angles and Waves*, which carried five outcomes and gave
the circle about a fifth of itself. Josh asked for the exact values in surd form
to have a tutorial, and for the circle to be worth introducing on its own:

> The trigonometric ratios in surd form, I think, is great — especially that
> deserves its own tutorial, and talking about the unit circle would be a great
> way to do that. Maybe introducing the unit circle as a separate entity would
> be helpful.

That is right, and it turns out to settle a scope decision as well. `MIT-4.7`
was ruled out on the grounds that exact values are a hand-calculation skill —
three numbers to memorise from two triangles nobody draws. **On the circle they
are not values to memorise, they are places.** √2⁄2 is where the 45° line
crosses; it is √2⁄2 *because* the point is as far across as it is up and the
distance to it is 1. Pythagoras gives it in one line, and the students have just
had Pythagoras.

So all three outcomes here are one drawing seen three ways:

| Outcome | What it is, on this circle |
|---|---|
| `MIT-4.5` radians | how far you have walked round it |
| `MIT-4.6` sin, cos, tan | the coordinates of where you are standing |
| `MIT-4.7` surd values | the coordinates at the angles a person can picture |

Taught apart, each is a convention to accept. Taught here, each is a fact about
a picture the student drew.

## The naming and describing decisions

**Coordinates before names.** Walk a point round the circle and print its x and
y before either word is used. When "cosine" arrives it is a name for a column
the student already has, rather than a function to be trusted.

**Radians as distance walked, not as a conversion factor.** The usual
introduction is `π/180`, which makes a radian a unit you convert *to*. The
better description is that a radian is arc length: walk a distance equal to the
radius and you have turned one radian, which is why the whole way round is 2π
of them. The conversion follows from that and is worth deriving once rather than
being handed over.

The way in is the failure. `math.sin(90)` returns 0.894, which is wrong and
looks plausible — show that first, and radians become the answer to a problem
rather than a preliminary.

**Tangent last, and as a slope.** sin and cos are coordinates; tan is y over x,
which is the slope of the line from the origin. That connects it to Lines and
Distances rather than making it a third thing to memorise, and it explains the
asymptote: a vertical line has no slope, which the students met when they tried
to plot `x = 3`.

**Surds as exactness rather than as notation.** The point of √2⁄2 is not that it
is a tidier way of writing 0.7071. It is that 0.7071 is *wrong* — it is a
rounding — and there are places where that matters. Say so once, with a cell
that squares both and shows only one of them gives exactly 0.5.

## The shape

### 1. Going round in circles

- **Cell:** walk a point round a circle of radius one, printing x and y at each
  step. Two columns, no vocabulary.
- **Cell:** plot the point at several angles, joined to the origin.
- **Point to make:** every one of these points is distance 1 from the centre —
  which is the distance formula from the last tutorial, and it is the only rule
  this whole tutorial rests on.

### 2. The names for those two columns

- **Cell:** the same table with the columns labelled cosine and sine, checked
  against `math.cos` and `math.sin`.
- **Cell:** x² + y² = 1 for every row. The identity, discovered rather than
  stated.
- **Your turn:** predict the sign of each coordinate in each quadrant, then
  check.

### 3. Measuring the walk

- **Cell:** `math.sin(90)`, which returns 0.894 and is not what anyone wanted.
- **Cell:** the arc length of a slice of the circle, and the angle that makes it
  exactly 1. That angle is one radian.
- **Cell:** a `to_radians` the student writes, checked against `math.radians`.
- **Point to make:** 2π is not a magic number. It is the distance round a circle
  of radius one, so it is how many radians there are in a full turn.

### 4. The landmark points

Where `MIT-4.7` lives.

- **Cell:** the 45° point. It is as far across as it is up, and the distance to
  it is 1, so x = y and x² + x² = 1. Solve it on screen: x = √2⁄2.
- **Cell:** the 30° and 60° points from the same argument, using the half of an
  equilateral triangle.
- **Cell:** square the exact value and square the decimal. One gives 0.5 and one
  gives 0.49999999999999994.
- **Your turn:** fill in the whole table of exact values for the four quadrants
  from the first quadrant and the signs.
- **Point to make:** these are not values to remember. They are the answers to
  "where does that line cross?", and the argument that produces them is
  Pythagoras, which you already have.

### 5. Tangent, which is a slope

- **Cell:** y/x for the points on the circle, plotted against angle, beside the
  line from the origin whose slope it is.
- **Cell:** what happens at 90°, and why the plot goes to infinity.
- **Point to make:** the asymptote is the vertical line that has no slope —
  the same one that would not fit `y = mx + c`.

## What to reuse

`distance(p, q)` from Lines and Distances, unchanged, to show that every point
on the circle really is 1 away. The plotting helper from Drawing Functions.

`unit_point(angle)` is written here and used by both tutorials that follow.

## Open questions

- **Is degrees-only viable?** It would drop `MIT-4.5` and cost a conversion at
  every library call that the students would not understand. Recorded here
  because it is the one place radians could have been avoided, and they are not
  being avoided.
- **How much of the exact-value table to ask for.** The first quadrant is three
  points and an argument; the other three are signs. Asking for all sixteen
  entries risks turning a tutorial about a picture into a drill.
