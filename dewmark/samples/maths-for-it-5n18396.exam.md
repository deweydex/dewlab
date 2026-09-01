```exam
title: Maths for Information Technology - 5N18396
exam_code: maths-it-2026
version: 2026.09.01.1
total_marks: 120
time_allowed: 3 hours
student_details: [full name, student number]
instructions: |
  In Section A, answer any ten of the twelve questions; each is worth 4
  marks. In Section B, answer any four of the six questions; each is
  worth 20 marks. A calculator is permitted. Show all working: a
  correct final answer with no working shown may not receive full
  marks. The side panel holds a formula sheet and a guide to typing
  mathematical notation.
```

```reference
title: Typing mathematical notation
text: |
  Use whatever feels natural — the only thing that matters is being
  consistent within each answer.

  - **Powers.** `x^2`, `x**2`, and "x to the power 2" all mean the
    same thing.
  - **Fractions.** Write `a/b`. Use brackets for compound tops or
    bottoms: `(x+3)/(x-1)`.
  - **Square roots.** Write `sqrt(x)` or surd form like `4*sqrt(2)`.
  - **Derivatives.** `f'(x)`, `dy/dx`, or `d/dx` are all fine — say
    once at the top of each calculus answer which you are using.
  - **Degrees.** To convert degrees to radians, multiply by pi/180.
  - **Intervals.** `x < 2` or `(-inf, 2)` are both fine — pick one per
    answer and stick to it.
  - **Infinity.** Write `+inf` or `-inf` when describing what a
    function approaches.
```

```reference
title: Formula sheet - algebra and functions
text: |
  - Quadratic formula: `x = (-b ± sqrt(b² - 4ac)) / (2a)`
  - Completing the square:
    `ax² + bx + c = a(x + b/2a)² + c - b²/4a`
  - Inverse function: write y = f(x), rearrange to make x the subject,
    then swap x and y.
```

```reference
title: Formula sheet - differentiation
text: |
  - Power rule: `d/dx [x^n] = n x^(n-1)`
  - Sum rule: `(f + g)' = f' + g'`
  - Product rule: `(fg)' = f'g + fg'`
  - Quotient rule: `(f/g)' = (f'g - fg') / g²`
  - Chain rule: `d/dx [f(g(x))] = f'(g(x)) · g'(x)`
  - Trig derivatives: `d/dx [sin x] = cos x`, `d/dx [cos x] = -sin x`
  - Increasing where f'(x) > 0; decreasing where f'(x) < 0; turning
    point where f'(x) = 0.
```

```reference
title: Formula sheet - coordinate geometry
text: |
  - Midpoint: `M = ((x1 + x2)/2, (y1 + y2)/2)`
  - Distance: `|PQ| = sqrt((x2 - x1)² + (y2 - y1)²)`
  - Slope: `m = (y2 - y1) / (x2 - x1)`
  - Parallel lines have equal slopes.
  - Perpendicular lines: `m1 × m2 = -1`
  - Line through (x1, y1) with slope m: `y - y1 = m(x - x1)`
```

```reference
title: Formula sheet - counting and probability
text: |
  - Factorial: `n! = n × (n-1) × ··· × 2 × 1`
  - Arrangements (order matters): `P(n,r) = n! / (n-r)!`
  - Selections (order does not matter): `C(n,r) = n! / (r! (n-r)!)`
  - `0 ≤ P(A) ≤ 1` and `P(not A) = 1 - P(A)`
  - If A and B cannot both happen: `P(A or B) = P(A) + P(B)`
  - If A and B are independent: `P(A and B) = P(A) × P(B)`
  - Expected occurrences: `E = (number of tries) × P(event)`
```

```reference
title: Formula sheet - trigonometry
text: |
  Right-angled triangle:

  - `a² + b² = c²`
  - `sin θ = opposite / hypotenuse`, `cos θ = adjacent / hypotenuse`,
    `tan θ = opposite / adjacent`

  Any triangle:

  - Sine rule: `a / sin A = b / sin B = c / sin C`
  - Cosine rule: `c² = a² + b² - 2ab cos C`
  - Area: `Area = ½ ab sin C`

  Unit circle values:

  | Angle | sin | cos |
  | --- | --- | --- |
  | 0° | 0 | 1 |
  | 30° | 1/2 | sqrt(3)/2 |
  | 45° | sqrt(2)/2 | sqrt(2)/2 |
  | 60° | sqrt(3)/2 | 1/2 |
  | 90° | 1 | 0 |
  | 180° | 0 | -1 |
  | 270° | -1 | 0 |
```

```reference
title: Formula sheet - statistics
text: |
  - Mean: add up all values and divide by how many there are.
  - Mean from a frequency table:
    `mean = Σ(value × frequency) / total frequency`. For grouped data,
    use the midpoint of each group as the value.
  - Median: the middle value when all values are listed in order.
  - Mode: the value that appears most often.
  - Range: largest value minus smallest value.
```

```section
name: A
choose: 10
```

## Section A — Answer any ten of the twelve questions

Each question in this section is worth 4 marks.

### Question A1 — Sets

```question
name: a1
marks: 4
topic: sets
```

Two friends compare which apps they have installed on their phones.

- **Sam's phone:** Calculator, Camera, Clock, Maps, Music, Weather
- **Kai's phone:** Calendar, Camera, Clock, News, Photos, Weather

```answer
name: a1.both
type: short-written-answer
marks: 2
prompt: (a) Which apps do both Sam and Kai have?
model_answer: "Camera, Clock, Weather"
```

```answer
name: a1.union
type: short-written-answer
marks: 1
prompt: (b) List every app that appears on at least one of the two phones.
model_answer: |
  Calculator, Calendar, Camera, Clock, Maps, Music, News, Photos,
  Weather (9 apps in total)
```

```answer
name: a1.difference
type: short-written-answer
marks: 1
prompt: (c) How many apps does Sam have that Kai does not have?
model_answer: "3 (Sam has Calculator, Maps, and Music that Kai does not)"
```

### Question A2 — Functions

```question
name: a2
marks: 4
topic: functions
```

Let $f(x) = 2x + 3$.

```answer
name: a2.value
type: short-written-answer
marks: 1
prompt: (a) Find f(4).
model_answer: f(4) = 2(4) + 3 = 11
```

```answer
name: a2.inverse
type: short-written-answer
marks: 2
prompt: (b) Find the inverse of f. Show your working.
model_answer: |
  Let y = 2x + 3.
  Rearrange: y - 3 = 2x, so x = (y - 3)/2.
  Swap x and y: the inverse is (x - 3)/2.
```

```answer
name: a2.check
type: short-written-answer
marks: 1
prompt: >
  (c) Check your answer: substitute 9 into your inverse, then
  substitute the result into f, and show that you get 9 back.
model_answer: |
  Inverse of 9: (9 - 3)/2 = 3.
  f(3) = 2(3) + 3 = 9, as required.
```

### Question A3 — A quadratic function

```question
name: a3
marks: 4
topic: quadratics
```

Consider $f(x) = x^2 - 2x - 8$.

```answer
name: a3.factors
type: short-written-answer
marks: 2
prompt: (a) Write f(x) as a product of two brackets.
model_answer: f(x) = (x - 4)(x + 2)
```

```answer
name: a3.roots
type: short-written-answer
marks: 1
prompt: (b) State the two values of x where the graph crosses the x-axis.
model_answer: x = 4 and x = -2
```

Part (c): describe a rough sketch of the graph, marking the two
x-intercepts and the y-intercept.

```answer
name: a3.sketch
type: describe-a-sketch
marks: 1
shape:
  prompt: The parabola opens
  options: ["upward (a ∪ shape)", "downward (a ∩ shape)"]
  correct: 1
features:
  - label: "Crosses the x-axis at x = _ and x = _"
    boxes: 2
    expected: [4, -2]
  - label: "Crosses the y-axis at y = _"
    boxes: 1
    expected: [-8]
```

```marking
marks: 1
guidance:
  - the full mark needs the right opening direction and all three
    crossing values; either order of the x values is fine
```

### Question A4 — Simultaneous equations

```question
name: a4
marks: 4
topic: simultaneous equations
```

```answer
name: a4.working
type: long-written-answer
marks: 4
prompt: >
  Solve the following pair of equations and find the values of x and
  y. Show all steps, and state both values clearly at the end.
  3x + y = 10 and x + y = 4.
model_answer: |
  Subtract the second equation from the first:
  (3x + y) - (x + y) = 10 - 4
  2x = 6, so x = 3.
  Substitute back: 3 + y = 4, so y = 1.
  Answer: x = 3, y = 1.
```

```marking
marks: 4
guidance:
  - 2 marks for a correct elimination or substitution step
  - 1 mark for each correct value, with working that leads to it
```

### Question A5 — Lines

```question
name: a5
marks: 4
topic: coordinate geometry
```

Two points $A(2, 1)$ and $B(5, 7)$ lie on the coordinate plane.

```answer
name: a5.slope
type: short-written-answer
marks: 1
prompt: (a) Find the slope of the line through A and B.
model_answer: slope = (7 - 1) / (5 - 2) = 6/3 = 2
```

```answer
name: a5.equation
type: short-written-answer
marks: 1
prompt: (b) Write the equation of the line through A and B.
model_answer: |
  y - 1 = 2(x - 2)
  y = 2x - 4 + 1
  y = 2x - 3
```

```answer
name: a5.perpendicular
type: short-written-answer
marks: 2
prompt: >
  (c) A second line passes through B and is perpendicular to AB. Find
  its equation.
model_answer: |
  Perpendicular slope = -1/2.
  y - 7 = -1/2 (x - 5)
  y = -x/2 + 5/2 + 7 = -x/2 + 19/2
```

### Question A6 — Distance and midpoint

```question
name: a6
marks: 4
topic: coordinate geometry
```

Points $P(2, -1)$ and $Q(-4, 3)$ are given.

```answer
name: a6.midpoint
type: short-written-answer
marks: 1
prompt: (a) Find the midpoint M of PQ.
model_answer: M = ((2 + -4)/2, (-1 + 3)/2) = (-1, 1)
```

```answer
name: a6.distance
type: short-written-answer
marks: 2
prompt: >
  (b) Find the distance from P to Q. Leave your answer in surd form if
  it does not simplify to a whole number.
model_answer: |
  |PQ| = sqrt((-4 - 2)² + (3 - (-1))²)
  = sqrt(36 + 16)
  = sqrt(52) = 2*sqrt(13)
```

```answer
name: a6.half
type: short-written-answer
marks: 1
prompt: (c) Find the distance from M to P. How does it compare to |PQ|?
model_answer: |
  |MP| = sqrt((-1 - 2)² + (1 - (-1))²) = sqrt(9 + 4) = sqrt(13),
  which is exactly half of |PQ| = 2*sqrt(13).
```

### Question A7 — Pythagorean triples

```question
name: a7
marks: 4
topic: pythagoras
```

A right-angled triangle whose three sides are all whole numbers is
called a *Pythagorean triple*. The 3-4-5 triangle is the simplest
example, since $3^2 + 4^2 = 9 + 16 = 25 = 5^2$.

```answer
name: a7.triples
type: long-written-answer
marks: 4
prompt: >
  Find two more right-angled triangles where every side is a whole
  number. For each one, write down the three lengths and show that the
  Pythagorean theorem holds. (2 marks each.)
model_answer: |
  Triple 1: 5, 12, 13. Check: 5² + 12² = 25 + 144 = 169 = 13².
  Triple 2: 8, 15, 17. Check: 8² + 15² = 64 + 225 = 289 = 17².
```

```marking
marks: 4
guidance:
  - 2 marks per triple - 1 for the three lengths, 1 for the check
  - a scaled copy of 3-4-5 (such as 6-8-10) earns its marks; the two
    triples must differ from each other by more than scale
```

### Question A8 — Trigonometric ratios

```question
name: a8
marks: 4
topic: trigonometry
```

In a right-angled triangle, the side opposite angle $θ$ has length 1
and the hypotenuse has length 2.

```answer
name: a8.ratios
type: short-written-answer
marks: 2
prompt: >
  (a) Write down sin θ and cos θ. Leave your answers in surd form
  where appropriate.
model_answer: sin θ = 1/2 and cos θ = sqrt(3)/2
```

```answer
name: a8.adjacent
type: short-written-answer
marks: 1
prompt: (b) Find the length of the third side, adjacent to θ.
model_answer: adjacent = sqrt(2² - 1²) = sqrt(3)
```

```answer
name: a8.tan
type: short-written-answer
marks: 1
prompt: (c) Use your answers to find tan θ.
model_answer: tan θ = (1/2) / (sqrt(3)/2) = 1/sqrt(3) = sqrt(3)/3
```

### Question A9 — Counting

```question
name: a9
marks: 4
topic: counting
```

```answer
name: a9.pins
type: short-written-answer
marks: 1
prompt: >
  (a) A 4-digit PIN uses the digits 0 to 9, and digits can be
  repeated. How many different PINs are there?
model_answer: 10^4 = 10,000 different PINs
```

```answer
name: a9.exact
type: short-written-answer
marks: 1
prompt: >
  (b) One PIN is chosen at random. What is the probability it is
  exactly "2580"?
model_answer: P = 1/10,000
```

```answer
name: a9.norepeat
type: short-written-answer
marks: 2
prompt: >
  (c) How many PINs are there where no digit is repeated? Show your
  reasoning.
model_answer: |
  First digit: 10 choices; second: 9; third: 8; fourth: 7.
  10 × 9 × 8 × 7 = 5,040 PINs.
```

### Question A10 — Probability

```question
name: a10
marks: 4
topic: probability
```

The English alphabet has 26 letters. For this question, count 6 of
them as vowels (a, e, i, o, u, y) and the other 20 as consonants. A
letter is chosen at random.

```answer
name: a10.vowel
type: short-written-answer
marks: 1
prompt: (a) What is the probability the chosen letter is a vowel?
model_answer: P(vowel) = 6/26 = 3/13
```

```answer
name: a10.notvowel
type: short-written-answer
marks: 1
prompt: (b) What is the probability the chosen letter is not a vowel?
model_answer: P(not a vowel) = 20/26 = 10/13
```

```answer
name: a10.two
type: short-written-answer
marks: 2
prompt: >
  (c) Two letters are chosen one after the other, without
  replacement. What is the probability both are vowels? Show your
  working.
model_answer: |
  P(first is a vowel) = 6/26.
  P(second is a vowel, given the first was) = 5/25.
  P(both) = 6/26 × 5/25 = 30/650 = 3/65.
```

### Question A11 — Statistics

```question
name: a11
marks: 4
topic: statistics
```

A class of 20 students sat a short quiz. Their scores out of 5 are
recorded below.

| Score | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| Students | 2 | 4 | 8 | 4 | 2 |

```answer
name: a11.mode
type: short-written-answer
marks: 1
prompt: (a) What score appeared most often?
model_answer: The mode is 3, which appeared 8 times.
```

```answer
name: a11.mean
type: short-written-answer
marks: 2
prompt: (b) Calculate the mean score.
model_answer: |
  Mean = (1×2 + 2×4 + 3×8 + 4×4 + 5×2) / 20
  = (2 + 8 + 24 + 16 + 10) / 20
  = 60 / 20 = 3
```

```answer
name: a11.high
type: short-written-answer
marks: 1
prompt: >
  (c) A student is chosen at random. What is the probability their
  score is 4 or higher?
model_answer: P(score of 4 or higher) = (4 + 2)/20 = 6/20 = 3/10
```

### Question A12 — Limits

```question
name: a12
marks: 4
topic: limits
```

Consider the function $f(x) = 5 + 12/x$.

```answer
name: a12.values
type: short-written-answer
marks: 2
prompt: (a) Calculate f(1), f(10), f(100), and f(1000).
model_answer: |
  f(1) = 17, f(10) = 6.2, f(100) = 5.12, f(1000) = 5.012
```

```answer
name: a12.limit
type: short-written-answer
marks: 1
prompt: >
  (b) As x grows larger and larger without end, what single value does
  f(x) appear to be getting closer and closer to?
model_answer: |
  f(x) approaches 5: as x grows, the term 12/x shrinks towards 0,
  leaving 5.
```

```answer
name: a12.zero
type: short-written-answer
marks: 1
prompt: >
  (c) What happens to f(x) as x gets very close to 0 from above? Give
  a brief reason.
model_answer: |
  f(x) grows without bound (towards +inf), because 12/x becomes
  arbitrarily large as x approaches 0.
```

```section
name: B
choose: 4
```

## Section B — Answer any four of the six questions

Each question in this section is worth 20 marks.

### Question B1 — Quadratic functions and derivatives

```question
name: b1
marks: 20
topic: quadratics and calculus
```

Let $f(x) = x^2 - 4x + 3$.

```answer
name: b1.roots
type: long-written-answer
marks: 5
prompt: >
  (a) Find the two roots of f(x) = 0 and the y-intercept. Use the
  roots to find the x-coordinate of the vertex, then calculate the
  y-value there. State the coordinates of the vertex.
model_answer: |
  Factoring: (x - 1)(x - 3) = 0, so x = 1 and x = 3.
  y-intercept: f(0) = 3.
  Vertex x-coordinate: (1 + 3)/2 = 2.
  Vertex y-coordinate: f(2) = 4 - 8 + 3 = -1.
  Vertex: (2, -1).
```

```marking
marks: 5
guidance:
  - 2 marks for both roots with method shown, 1 for the y-intercept
  - 1 mark for the vertex x-coordinate from the roots, 1 for the
    vertex coordinates stated
```

Part (b): describe a sketch of the graph, giving the vertex, both
roots, and the y-intercept.

```answer
name: b1.sketch
type: describe-a-sketch
marks: 6
shape:
  prompt: The parabola opens
  options: ["upward (a ∪ shape)", "downward (a ∩ shape)"]
  correct: 1
features:
  - label: "Root 1 at ( _ , 0 ) and root 2 at ( _ , 0 )"
    boxes: 2
    expected: [1, 3]
  - label: "Crosses the y-axis at ( 0 , _ )"
    boxes: 1
    expected: [3]
  - label: "Vertex at ( _ , _ )"
    boxes: 2
    expected: [2, -1]
```

```marking
marks: 6
guidance:
  - 1 mark for the opening direction, 1 for each root, 1 for the
    y-intercept, 2 for the vertex
```

```answer
name: b1.derivative
type: long-written-answer
marks: 5
prompt: >
  (c) Differentiate f. Use the derivative to state the value of x at
  which f has its minimum, the minimum value of f, and the intervals
  where f is decreasing and where it is increasing.
model_answer: |
  f'(x) = 2x - 4.
  Setting f'(x) = 0: 2x - 4 = 0, so x = 2.
  Minimum value: f(2) = -1.
  Decreasing on (-inf, 2), where f'(x) < 0.
  Increasing on (2, +inf), where f'(x) > 0.
```

```marking
marks: 5
guidance:
  - 1 mark for the derivative, 1 for solving it equal to zero, 1 for
    the minimum value, 1 for each interval
```

```answer
name: b1.shift
type: long-written-answer
marks: 4
prompt: >
  (d) Now consider g(x) = f(x + 1). Substitute (x + 1) into your
  expression for f and simplify g(x) fully. Then describe in one
  sentence how the graph of g is related to the graph of f.
model_answer: |
  g(x) = (x + 1)² - 4(x + 1) + 3
  = x² + 2x + 1 - 4x - 4 + 3
  = x² - 2x
  The graph of g is the graph of f shifted 1 unit to the left.
```

```marking
marks: 4
guidance:
  - 2 marks for a correct substitution and expansion, 1 for the fully
    simplified form, 1 for the sentence about the shift
```

### Question B2 — Cubic functions

```question
name: b2
marks: 20
topic: cubics
```

Let $g(x) = x^3 - 12x$.

Part (a): complete the table of values.

```answer
name: b2.table
type: complete-the-table
marks: 3
columns: [x, -2, -1, 0, 1, 2]
rows:
  - ["g(x)", "?", "?", "?", "?", "?"]
expected:
  - ["g(x)", 16, 11, 0, -11, -16]
```

```marking
marks: 3
guidance:
  - 3 marks for all five cells, 2 for at least three, 1 for at least
    one
```

Part (b): using your table, describe a sketch of the graph, marking
approximately where it crosses the x-axis.

```answer
name: b2.sketch
type: describe-a-sketch
marks: 4
shape:
  prompt: The overall shape of the curve is
  options:
    - "rising overall, with two turning points"
    - "rising overall, with no turning points"
    - "falling overall, with two turning points"
    - "falling overall, with no turning points"
  correct: 1
features:
  - label: "Highest local point near x = _ , where g(x) = _"
    boxes: 2
    expected: [-2, 16]
  - label: "Lowest local point near x = _ , where g(x) = _"
    boxes: 2
    expected: [2, -16]
  - label: "Crosses the x-axis at x = _ , x = _ , and x = _"
    boxes: 3
    expected: [0, "about -3.46", "about 3.46"]
```

```marking
marks: 4
guidance:
  - 1 mark for the shape, 1 for each local extreme, 1 for the three
    crossings; accept ±2*sqrt(3) or anything close to ±3.5 for the
    outer crossings, in any order
```

```answer
name: b2.derivative
type: short-written-answer
marks: 2
prompt: (c) Differentiate g.
model_answer: g'(x) = 3x² - 12, by the power rule on each term.
```

```answer
name: b2.turning
type: long-written-answer
marks: 4
prompt: >
  (d) Set your derivative equal to zero and solve to find the
  x-coordinates of both turning points. Then calculate the y-value at
  each one.
model_answer: |
  3x² - 12 = 0, so x² = 4 and x = ±2.
  g(-2) = -8 + 24 = 16, giving the turning point (-2, 16).
  g(2) = 8 - 24 = -16, giving the turning point (2, -16).
```

```marking
marks: 4
guidance:
  - 2 marks for solving the derivative equal to zero, 1 for each
    turning point's coordinates
```

```answer
name: b2.classify
type: long-written-answer
marks: 4
prompt: >
  (e) For each turning point, explain whether it is a local maximum or
  a local minimum. Then state the intervals over which g is increasing
  and over which g is decreasing.
model_answer: |
  At x = -2 the derivative changes from positive to negative, so
  (-2, 16) is a local maximum.
  At x = 2 the derivative changes from negative to positive, so
  (2, -16) is a local minimum.
  Increasing on (-inf, -2) and (2, +inf); decreasing on (-2, 2).
```

```marking
marks: 4
guidance:
  - 1 mark for each classification with a reason, 1 for each of the
    increasing and decreasing statements
```

```answer
name: b2.ends
type: short-written-answer
marks: 2
prompt: >
  (f) As x grows to be a very large positive number, what happens to
  g(x)? What about when x becomes a very large negative number?
model_answer: |
  As x goes to +inf, g(x) goes to +inf; as x goes to -inf, g(x) goes
  to -inf. The x³ term dominates, and its coefficient is positive.
```

```answer
name: b2.atzero
type: short-written-answer
marks: 1
prompt: >
  (g) Calculate the value of your derivative at x = 0. In one
  sentence, explain what this value tells you about the shape of the
  curve there.
model_answer: |
  g'(0) = -12. At x = 0 the curve has a slope of -12, so it is
  descending steeply.
```

### Question B3 — Differentiation

```question
name: b3
marks: 20
topic: calculus
```

Part (a): find the derivative of each function below, stating which
rule you use in each case.

```answer
name: b3.power
type: short-written-answer
marks: 3
prompt: "(a)(i) h(x) = 3x⁴ - 2x³ + 5x - 7"
model_answer: |
  Power rule on each term: h'(x) = 12x³ - 6x² + 5.
```

```answer
name: b3.expand
type: short-written-answer
marks: 4
prompt: >
  (a)(ii) k(x) = (x - 2)(x² + 3). Expand first, then differentiate.
model_answer: |
  Expanded: k(x) = x³ - 2x² + 3x - 6.
  Power rule: k'(x) = 3x² - 4x + 3.
```

```answer
name: b3.chain
type: short-written-answer
marks: 3
prompt: "(a)(iii) m(x) = (3x + 2)⁴"
model_answer: |
  Chain rule, with u = 3x + 2 and m = u⁴:
  m'(x) = 4(3x + 2)³ × 3 = 12(3x + 2)³.
```

Part (b): a drone rises straight up from the ground. Its height in
metres at time $t$ seconds is $h(t) = 24t - 4t^2$, for $t ≥ 0$.

```answer
name: b3.velocity
type: short-written-answer
marks: 3
prompt: >
  (b)(i) Differentiate h. In one sentence, describe what the
  derivative represents in this situation.
model_answer: |
  h'(t) = 24 - 8t. This is the drone's velocity: the rate of change
  of height with time, in metres per second.
```

```answer
name: b3.peaktime
type: short-written-answer
marks: 2
prompt: (b)(ii) At what time t does the drone reach its maximum height?
model_answer: Setting h'(t) = 0 gives 24 - 8t = 0, so t = 3 seconds.
```

```answer
name: b3.peak
type: short-written-answer
marks: 2
prompt: (b)(iii) What is that maximum height?
model_answer: h(3) = 24(3) - 4(9) = 72 - 36 = 36 metres.
```

```answer
name: b3.landing
type: short-written-answer
marks: 3
prompt: >
  (b)(iv) After reaching its peak, the drone falls back to the
  ground. At what time t does it land? Ignore t = 0, the launch time.
model_answer: |
  Setting h(t) = 0: 24t - 4t² = 0, so 4t(6 - t) = 0.
  t = 0 is the launch, so the drone lands at t = 6 seconds.
```

### Question B4 — Probability and statistics

```question
name: b4
marks: 20
topic: probability and statistics
```

Part (a) is about long sequences of coin flips, and what turns out to
be surprising about them.

```answer
name: b4.single
type: short-written-answer
marks: 1
prompt: (a)(i) What is the probability of getting heads on a single flip?
model_answer: P(heads) = 1/2
```

```answer
name: b4.three
type: short-written-answer
marks: 2
prompt: >
  (a)(ii) What is the probability of getting heads three times in a
  row? Show your reasoning.
model_answer: |
  The flips are independent, so
  P(three heads in a row) = 1/2 × 1/2 × 1/2 = 1/8.
```

```answer
name: b4.eight
type: short-written-answer
marks: 1
prompt: >
  (a)(iii) What is the probability of getting heads eight times in a
  row?
model_answer: P(eight heads in a row) = (1/2)^8 = 1/256
```

```answer
name: b4.runs
type: long-written-answer
marks: 4
prompt: >
  (a)(iv) Suppose you flip a coin 1000 times. At each position from
  flip 1 through to flip 993, you can ask whether the next 8 flips
  all come up heads — 993 possible starting positions for a run of 8
  heads. Using your answer to part (iii), estimate the expected
  number of such runs in 1000 flips, rounded to one decimal place.
  Does the answer surprise you?
model_answer: |
  Expected runs = 993 × 1/256 = 993/256, which is about 3.9.
  Surprisingly many: in only 1000 flips you should expect about four
  runs of eight consecutive heads.
```

```marking
marks: 4
guidance:
  - 2 marks for multiplying the positions by the probability, 1 for
    the rounded value, 1 for a sentence engaging with the surprise
```

Part (b): the bar chart below shows how many times each of the
letters A through E appeared in a short message.

![A bar chart. The vertical axis counts appearances, from 0 to 9 with
a gridline every 2. Five bars: A reaches 5, B reaches 8, C reaches 3,
D reaches 7, and E reaches 2.](pictures/letter-frequency-chart.svg)

```answer
name: b4.most
type: short-written-answer
marks: 1
prompt: >
  (b)(i) Which letter appeared most often, and how many times did it
  appear?
model_answer: B appeared most often, 8 times.
```

```answer
name: b4.total
type: short-written-answer
marks: 1
prompt: (b)(ii) How many letters are there in the message altogether?
model_answer: 5 + 8 + 3 + 7 + 2 = 25 letters.
```

```answer
name: b4.pc
type: short-written-answer
marks: 3
prompt: >
  (b)(iii) If one letter is chosen at random from the message, what
  is the probability it is the letter C?
model_answer: P(C) = 3/25, since 3 of the 25 letters are C.
```

```answer
name: b4.notc
type: short-written-answer
marks: 1
prompt: (b)(iv) What is the probability the chosen letter is not C?
model_answer: P(not C) = 1 - 3/25 = 22/25
```

```answer
name: b4.meanfreq
type: short-written-answer
marks: 3
prompt: (b)(v) Find the mean frequency across the five letters A to E.
model_answer: Mean = (5 + 8 + 3 + 7 + 2) / 5 = 25/5 = 5.
```

```answer
name: b4.order
type: short-written-answer
marks: 3
prompt: >
  (b)(vi) List the five letters in order from least likely to most
  likely to be chosen at random.
model_answer: |
  E (2/25), then C (3/25), then A (5/25), then D (7/25), then
  B (8/25).
```

### Question B5 — Triangle trigonometry

```question
name: b5
marks: 20
topic: trigonometry
```

In triangle ABC: angle $C = 40°$, side $a = BC = 7$ cm, and side
$b = AC = 10$ cm.

![A triangle with vertex C at the bottom left, vertex A at the bottom
right, and vertex B at the top. Side a runs from C up to B, side b
from B down to A, and side c along the bottom from C to A. An arc
marks the angle at vertex C.](pictures/triangle-abc.svg)

Part (i): fill in the values you know from the question, and — once
you have worked them out in the later parts — the three unknowns.

```answer
name: b5.known
type: complete-the-table
marks: 3
columns: [quantity, value]
rows:
  - ["angle C", "?"]
  - ["side a = BC", "?"]
  - ["side b = AC", "?"]
  - ["side c = AB", "?"]
  - ["angle A", "?"]
  - ["angle B", "?"]
expected:
  - ["angle C", "40°"]
  - ["side a = BC", "7 cm"]
  - ["side b = AC", "10 cm"]
  - ["side c = AB", "about 6.46 cm"]
  - ["angle A", "about 44.1°"]
  - ["angle B", "about 95.9°"]
```

```marking
marks: 3
guidance:
  - 1 mark for the three given values, 2 for the three computed ones
    consistent with the student's later working
```

```answer
name: b5.cosine
type: long-written-answer
marks: 6
prompt: >
  (ii) Using the cosine rule, find the length of side c = AB. Round
  to 2 decimal places.
model_answer: |
  c² = a² + b² - 2ab cos(C)
  c² = 49 + 100 - 2(7)(10)cos(40°)
  c² = 149 - 140 × 0.7660 = 149 - 107.24 = 41.76
  c = sqrt(41.76), about 6.46 cm.
```

```marking
marks: 6
guidance:
  - 2 marks for the rule with the right values in place, 2 for the
    arithmetic, 2 for the square root and rounding
```

```answer
name: b5.sine
type: long-written-answer
marks: 6
prompt: >
  (iii) Using the sine rule, find angle A. Round to 1 decimal place.
model_answer: |
  sin(A)/a = sin(C)/c
  sin(A) = 7 × sin(40°) / 6.46 = 7 × 0.6428 / 6.46, about 0.6962.
  A = arcsin(0.6962), about 44.1°.
```

```marking
marks: 6
guidance:
  - 2 marks for the rule with the right values in place, 2 for
    isolating sin(A), 2 for the inverse sine and rounding
```

```answer
name: b5.angleb
type: short-written-answer
marks: 2
prompt: (iv) Find angle B.
model_answer: B = 180° - 40° - 44.1° = 95.9°, since angles sum to 180°.
```

```answer
name: b5.area
type: short-written-answer
marks: 3
prompt: >
  (v) Calculate the area of triangle ABC, using the half-ab-sin-C
  formula from the formula sheet.
model_answer: |
  Area = 1/2 × 7 × 10 × sin(40°) = 35 × 0.6428, about 22.5 cm².
```

### Question B6 — Similar triangles

```question
name: b6
marks: 20
topic: similar triangles
```

Two right-angled triangles are given. In each triangle, the two
shorter sides are equal in length. The longest side of the small
triangle is 8 cm, and the longest side of the large triangle is
24 cm.

![Two right-angled triangles side by side. Each has a small square
marking the right angle at its bottom-left corner, and a single tick
mark on each of its two shorter sides showing they are equal. The
small triangle's longest side is labelled 8 cm; the large triangle's
longest side is labelled 24 cm.](pictures/similar-triangles.svg)

```answer
name: b6.similar
type: long-written-answer
marks: 4
prompt: >
  (a) The two triangles shown are described as similar. Explain in
  your own words what it means for two triangles to be similar.
  Then, looking only at what is already marked on the diagrams,
  identify the features that are the same in both triangles and
  explain briefly why this is enough to confirm that they are
  similar to each other.
model_answer: |
  Two triangles are similar when they have exactly the same set of
  angles — the same shape — but not necessarily the same size; their
  corresponding sides are proportional rather than equal.
  Both diagrams show a right angle, and tick marks showing the two
  shorter sides equal. A right-angled triangle with two equal legs
  must split the remaining 90° equally, so both triangles have the
  angle pattern 90°, 45°, 45°, which confirms they are similar.
```

```marking
marks: 4
guidance:
  - 2 marks for a correct account of similarity in the student's own
    words, 2 for reading the right angle and tick marks off the
    diagrams and drawing the conclusion
```

```answer
name: b6.angles
type: long-written-answer
marks: 4
prompt: >
  (b) Using the fact that the angles of any triangle sum to 180°,
  find the size of each unknown angle in the small triangle. Explain
  your reasoning in full.
model_answer: |
  One angle is 90°, so the other two sum to 90°. The two shorter
  sides are equal, so the angles opposite them are equal too. Each is
  therefore 90°/2 = 45°. The angles are 45°, 45°, and 90°.
```

```answer
name: b6.sides
type: long-written-answer
marks: 4
prompt: >
  (c) Find the length of each shorter side of the small triangle.
  Leave your answer in surd form.
model_answer: |
  Let s be the length of each shorter side.
  By Pythagoras: s² + s² = 8², so 2s² = 64 and s² = 32.
  s = sqrt(32) = 4*sqrt(2) cm.
```

```answer
name: b6.scale
type: long-written-answer
marks: 4
prompt: >
  (d) Write down all three side lengths of the large triangle, and
  state the scale factor from the small triangle to the large one.
model_answer: |
  Scale factor = 24/8 = 3.
  Each leg of the large triangle is 4*sqrt(2) × 3 = 12*sqrt(2) cm.
  The three sides are 12*sqrt(2) cm, 12*sqrt(2) cm, and 24 cm.
```

```answer
name: b6.areas
type: long-written-answer
marks: 4
prompt: >
  (e) Calculate the area of each triangle, showing your working. By
  what factor is the area of the large triangle greater than the
  area of the small one?
model_answer: |
  Small: 1/2 × 4*sqrt(2) × 4*sqrt(2) = 1/2 × 32 = 16 cm².
  Large: 1/2 × 12*sqrt(2) × 12*sqrt(2) = 1/2 × 288 = 144 cm².
  Ratio = 144/16 = 9 — the square of the scale factor, 3² = 9.
```

```marking
marks: 4
guidance:
  - 1 mark for each area with working, 1 for the ratio, 1 for
    connecting it to the square of the scale factor
```
