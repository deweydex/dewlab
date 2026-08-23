# Outline — Sine and Cosine Waves

**Closes:** `MIT-3.3` (define and graph the trigonometric functions).
**Goes after:** [The Unit Circle](./the-unit-circle.md).
**Followed by:** [Solving Triangles](./solving-triangles.md).
**Builds on:** Drawing Functions (a function has a picture), The Unit Circle
(what sine and cosine are).
**Size:** short, and not thin — one idea with a lot to do in it.

## Why it is separate from the circle

The circle is where sine and cosine are *defined*; this is where they *move*.
Those are two different activities and each wants room: the first is a careful
argument about coordinates, the second is experiment — change a number, look at
what happened, change it back.

Put together they were a fifth of *Angles and Waves*, which carried five
outcomes and gave none of them enough space. Apart, the circle gets its
argument and this gets its playground.

One outcome, and a tutorial rather than a section, because the work here is
practice rather than exposition. A student who has read about amplitude and not
changed one has not learned anything.

## The one thing dewlab can do that paper cannot

Unrolling. A point goes round the circle on the left while the curve draws
itself on the right, and the height of the point *is* the height of the curve.
On paper that is two pictures and a sentence asking the reader to imagine the
connection. Here it is one animation and the connection is the thing you see.

This is the tutorial's centre and everything else arranges itself around it.

## The shape

### 1. Unrolling the circle

- **Cell:** `unit_point(angle)` from the last tutorial, called for a long
  sequence of angles, with the y values plotted against the angle.
- **Cell:** the same again with x. Two curves out of one walk.
- **Point to make:** nothing new has been defined. This is the table from the
  last tutorial with the angle along the bottom instead of in a column.

### 2. Why it repeats

- **Cell:** carry on past 2π and watch the curve come round again.
- **Cell:** negative angles, going the other way.
- **Your turn:** without plotting, say what `sin(10π)` is and why. Then check.
- **Point to make:** periodicity is not a property the curve happens to have.
  It is what going round in a circle looks like when you draw it flat.

### 3. The four numbers

Amplitude, period, phase and vertical shift, one at a time.

- **Cell:** `wave(amplitude, period, phase, shift)` written once and called
  repeatedly on one pair of axes, changing exactly one argument each time.
- **Cell:** all four at once, and the same picture rebuilt from the four
  numbers alone.
- **Your turn:** four pictures of waves; find the numbers for each. Then plot
  yours over the original and see whether it lands.
- **Point to make:** this is the same "one coefficient, one visible change"
  pattern as the quadratics in Parabolas. The students have done this before
  with a different curve.

### 4. Where a wave comes from

The section that says why anyone would want this, and the one most likely to be
cut for time — which would be the wrong cut.

- **Cell:** a sound sample plotted, and the same sample rebuilt from two sine
  waves added together.
- **Cell:** a year of daylight hours for Dublin, with a sine wave fitted over
  it by hand — adjust the four numbers until it sits on the data.
- **Point to make:** a wave is what anything that goes round and comes back
  looks like when you plot it against time. Daylight, tides, a spinning motor,
  a sound.

### 5. Tangent, briefly

- **Cell:** tan plotted over the same range, with its asymptotes.
- **Point to make:** it is not a wave. It is a slope, and slopes go to infinity
  when a line stands up — which the students met when they tried to plot
  `x = 3` in Lines and Distances.

## What to reuse

`unit_point(angle)` from The Unit Circle, and the plotting helper from Drawing
Functions. `wave(...)` is written here and used again in Solving Triangles for
nothing much, so it does not need to be careful about its interface.

## Open questions

- **The daylight data.** Real numbers for Dublin would be better than invented
  ones and mean a file in `data/`. Worth it if the fit is the payoff of the
  tutorial, which I think it is.
- **Whether fitting by hand is too loose.** Adjusting four numbers until a curve
  sits on data is the honest version of what regression does later, but a
  student who cannot get it to fit will feel it as a failure rather than as an
  experiment. It may want a "good enough" line drawn on the plot.
