# Outline — Angles and Waves

**Closes:** `MIT-3.3` (define and graph the trigonometric functions), `MIT-4.5`
(degree and radian measure), `MIT-4.6` (sin, cos, tan and the unit circle),
`MIT-4.8` (triangle area), `MIT-4.10` (Sine and Cosine Rules).
**Goes after:** [Lines and Distances](./lines-and-distances.md), which the unit
circle needs — a point on a circle of radius one is a coordinate-geometry
object, and the distance formula is what makes the identity true.
**Followed by:** *How Tall Is That?*, the short tutorial that takes `MIT-4.9`.
This outline used to carry `MIT-4.4` and `MIT-4.9` conditionally; Pythagoras is
in Lines and Distances now and practical right-triangle work has its own short
tutorial, so this one keeps its five outcomes and its smallness.
**Builds on:** Drawing Functions, Lines and Distances.

## What this is not

All of trigonometry that survives the scope decisions, and nothing else. No
identities, no trigonometric equations, no compound angle formulae, no surd
form. Two things are worth having: what the sine and cosine curves look like and
what you can do to them, and how to solve a triangle that is not right-angled.

That is a deliberately small tutorial for a large-looking topic, and the
smallness is the point — see `planning/curriculum/out-of-scope.yaml`.

## The shape

### 1. Going round in circles

The unit circle, and where sine and cosine actually come from.

- **Cell:** walk a point around the unit circle, printing its x and y at each
  step. The two columns *are* cosine and sine, before either word is used.
- **Cell:** plot those two columns against the angle. The curves appear out of
  the table the student just made.
- **Point to make:** sine and cosine are not new functions to memorise; they are
  the coordinates of a point going round a circle.

### 2. Two ways to measure an angle

Radians, kept to exactly what the graphs need.

- **Cell:** `math.sin` takes radians, and a student who feeds it degrees gets
  nonsense. Show the nonsense first, then fix it.
- **Cell:** a `to_radians` the student writes, checked against `math.radians`.
- **Point to make:** a radian is how far you have walked round the circle. That
  is why `2π` gets you back where you started.

### 3. What you can do to a wave

Amplitude, period, phase and vertical shift, each varied one at a time.

- **Cell:** `plot_wave(amplitude, period, phase, shift)` written once and called
  repeatedly, exactly as `plot_line` was in Drawing Functions.
- **Your turn:** given a picture of a wave, work out the four numbers. Then
  check by plotting.
- **Point to make:** this is the same "one coefficient, one visible change"
  pattern as the quadratics, which the students have already met.

### 4. Triangles that are not right-angled

The Sine Rule, the Cosine Rule, and the area formula.

- **Cell:** a `solve_triangle` that takes what is known and returns what is not.
- **Cell:** area as ½·a·b·sin C, checked against the base-times-height answer
  for a triangle where both work.
- **Your turn:** a surveying problem and a navigation problem — two distances
  and the angle between them, find the third side.
- **Point to make:** the rules are what you reach for when SOH-CAH-TOA runs out.
  Which is the argument for keeping right-triangle trigonometry as the way in.

## Open questions

- Do Pythagoras and SOH-CAH-TOA (`MIT-4.4`, `MIT-4.9`) come in as section 0?
  They are the students' existing foothold, and the Sine and Cosine Rules make
  more sense as "what to do when the triangle is not right-angled" than as free-
  standing formulae. Listed as undecided in `out-of-scope.yaml`.
- Is degrees-only viable? It would drop `MIT-4.5` entirely, at the cost of every
  library function needing a conversion the students do not understand.
