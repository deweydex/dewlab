# Outline — Solving Triangles

**Closes:** `MIT-4.8` (triangle area as ½ab sin C), `MIT-4.9` (practical
right-triangle trigonometry), `MIT-4.10` (the Sine Rule and the Cosine Rule).
**Goes after:** [Sine and Cosine Waves](./sine-and-cosine-waves.md).
**Builds on:** Lines and Distances (Pythagoras), The Unit Circle (the ratios).
**Size:** full.

## What it is

Given some of a triangle, find the rest. That is the whole tutorial, and it is
worth saying in one sentence because the three outcomes in it look like three
topics and are not: they are three cases of one question, in the order a person
would try them.

1. **Right-angled?** Pythagoras and the ratios. No new machinery.
2. **Not right-angled, and you know two sides and the angle between them, or
   three sides?** The Cosine Rule.
3. **Not right-angled, and you know a side and its opposite angle?** The Sine
   Rule.

The area formula falls out of the second: ½ab sin C is base times height, once
you notice that `b sin C` *is* the height.

## Where "How Tall Is That?" went

`MIT-4.9` was briefly its own proposal — a short tutorial about heights and
distances, ladders and roof pitches. Josh:

> I don't really think we need to worry about it. I don't think we need to deal
> with roof pitches and buildings, because we can deal with more appropriate to
> computer science types of questions there.

Both halves of that are right. The examples were the problem — a tutorial whose
motivating question is a roof is a tutorial for a different course — and once
the examples change, the material has no reason to be separate from the rules
it is the easy case of.

**So the practical work stays and its examples move to computing:**

- **Bearings and headings.** A drone flies 200 m on a bearing of 040°, then
  150 m on 110°. Where is it, and how far from home? This is two vectors and
  the Cosine Rule.
- **The angle between two vectors**, which is the Cosine Rule rearranged, and
  which they will meet again as similarity between two lists of numbers.
- **A robot arm** with two segments reaching for a point: the Cosine Rule tells
  you the joint angle, and there are two answers, both correct.
- **Distance to a point on a plot** at a known angle — the reverse of what they
  did in Lines and Distances.

None of those needs a building in it, and each is a question somebody in this
course might actually have.

## The naming and describing decisions

**Solve means find the missing parts**, and the word should be introduced
plainly, because "solving a triangle" sounds like a category error to anyone who
has only solved equations. One sentence, early.

**The rules are what you reach for when the right angle is missing.** Presented
that way they are a repair rather than two more formulae. Presented as free-
standing facts they are two more formulae. The order in the tutorial should be
the order a person actually tries things.

**The ambiguous case is a feature, not a footnote.** The Sine Rule can give two
valid triangles, and a student who meets that as a warning at the end will
remember it as a trap. Met as *the picture has two answers and here they both
are*, it is the most interesting thing in the tutorial — and it is the first
time in the series that a correct calculation gives two correct answers.

## The shape

### 1. When there is a right angle

- **Cell:** a right triangle drawn from three points, its sides measured with
  `distance` from Lines and Distances.
- **Cell:** the three ratios computed from the sides, checked against `math.sin`
  and friends applied to the angle.
- **Your turn:** a robot arm segment at a known angle — where does its tip land?
- **Point to make:** nothing here is new. It is the unit circle with the circle
  scaled up, which is why the ratios do not care how big the triangle is.

### 2. Area, and the height nobody drew

- **Cell:** base times height for a triangle where the height is obvious.
- **Cell:** the same triangle as ½ab sin C, agreeing.
- **Cell:** a triangle where the height is not obvious, done both ways.
- **Point to make:** `b sin C` is the height. The formula is not a new fact, it
  is the old one with the height worked out for you.

### 3. The Cosine Rule

- **Cell:** Pythagoras, and then the same triangle with the angle opened past
  90°. The two sides squared no longer add up — plot the gap against the angle.
- **Cell:** the gap is `2ab cos C`, which is the Cosine Rule.
- **Cell:** `solve_triangle` handling the two cases the rule covers.
- **Your turn:** the drone with two legs of its flight. How far from home?
- **Point to make:** the Cosine Rule is Pythagoras with a correction term, and
  the correction is zero at 90° — check that on screen.

### 4. The Sine Rule, and its two answers

- **Cell:** a side and its opposite angle, and the ratio that stays the same
  round the triangle.
- **Cell:** the ambiguous case, drawn. Both triangles plotted on one pair of
  axes, both correct.
- **Your turn:** given a case, decide whether it is ambiguous before computing.
- **Point to make:** a correct calculation with two correct answers is not a
  failure of the method. Deciding which one you meant is your job, not the
  formula's.

### 5. Putting it together

- **Cell:** a `solve` that takes whatever is known and picks the rule.
- **Your turn:** the angle between two vectors — three of them, and which pair
  is most alike?
- **Point to make:** that last question is what a recommendation system asks,
  and it is the Cosine Rule rearranged.

## What to reuse

`distance(p, q)` from Lines and Distances throughout. `unit_point` is not needed
here; the ratios come from `math` once the students have seen where they come
from.

## Open questions

- **How much of the drone problem to give.** Bearings are measured clockwise
  from north, which is not the convention the unit circle uses, and reconciling
  the two is either a good exercise or a distraction. It probably wants to be
  stated rather than discovered.
- **Whether the recommendation-system aside earns its place.** It is the best
  reason in the tutorial for caring about the angle between vectors, and it is
  also a whole other subject looked at through a keyhole.
