# What is left to write

A survey, not a plan: what exists, what the curriculum map says is still
uncovered, and which of those gaps nobody has proposed a tutorial for.

Counted from the repository on 23 August 2026 — `tutorials/`,
`planning/curriculum/outcomes.yaml`, and `planning/curriculum/proposed.yaml`.
It will go stale, and the way to refresh it is to re-run the counts rather than
to trust the numbers below.

---

## What exists

| Series | Module | Tutorials |
|---|---|---|
| Maths and programming | MIT + PDP integrated | 17 |
| Reflections and review | MIT + PDP integrated | 1 |
| Python fundamentals | Computational Methods 5N0554 | 2 |

Twenty tutorials, of which eighteen are the integrated series that the
curriculum map measures.

## What the map says is missing

Sixty-seven outcomes across the two mapped descriptors. **Forty-one are taught;
twenty-six are not.**

Twenty-two of the twenty-six are Maths for IT, and they are not scattered — they
are two whole sections of the descriptor:

- **Section 3, Functions and Calculus** — all seven outcomes. Functions and
  inverses, graphing, completing the square, limits, the derivative, the rules
  of differentiation.
- **Section 4, Geometry and Trigonometry** — all ten outcomes. Coordinate
  geometry, Pythagoras, radians, the unit circle, surds, triangle area, the
  Sine and Cosine Rules.

Plus five singles: transposing formulae (1.7), quadratics with complex roots
(1.10), Venn diagrams (2.3), truth tables (2.4) and De Morgan (2.5).

The four Programming and Design Principles gaps are the history of programming
(LO1), telling languages apart (LO3), reading compiler messages (LO9) and the
team project (LO12).

**Nothing on the maths side of the course past algebra has been written yet.**
That is the headline, and it is not a surprise — the eighteen tutorials that
exist are the programming spine with maths threaded through it, and the maths
that is threaded is arithmetic, algebra, counting, probability and statistics.
The half of the descriptor that needs pictures has none.

## What is already proposed

`planning/curriculum/proposed.yaml` holds ten proposals, each with an outline in
`planning/outlines/`. Between them they close **nineteen of the twenty-six**.

| Proposal | Closes | Size |
|---|---|---|
| Rearranging Formulae | MIT-1.7 | short |
| When There Is No Answer | MIT-1.10 | short |
| Drawing Functions | MIT-3.1, 3.2, 3.4 | full |
| Angles and Waves | MIT-3.3, 4.5, 4.6, 4.8, 4.10 | full |
| Approaching a Limit | MIT-3.5 | short |
| Rates of Change | MIT-3.6, 3.7 | full |
| Logic and Truth | MIT-2.4, 2.5 | short |
| How We Got Here | PDP-LO1, LO3 | full, converted from everlearning |
| When It Goes Wrong | PDP-LO9 | full, converted from everlearning |
| The Team Project | PDP-LO12 | not a tutorial |

Four full tutorials, three short ones, two conversions and one thing that is
not a tutorial at all. That is the written-down plan, and it is a good one.

## What nothing covers: seven outcomes

These have no tutorial and no proposal. **Build all ten proposals and the map
still shows seven gaps.**

| Outcome | |
|---|---|
| MIT-4.1 | Linear equations in the form ax + by + c = 0 |
| MIT-4.2 | Slope; parallel and perpendicular lines |
| MIT-4.3 | Midpoint and length of a line segment |
| MIT-4.4 | The Pythagorean theorem |
| MIT-4.7 | Trigonometric ratios in surd form |
| MIT-4.9 | Practical right-triangle trigonometry |
| MIT-2.3 | Venn diagrams for two and three sets |

### The first four are one missing tutorial

MIT-4.1 to 4.4 is coordinate geometry, and it is a coherent subject rather than
four loose ends: a line as an equation, what its slope means, the distance
between two points, and Pythagoras — which is the same theorem as the distance
formula, written the other way round.

It is also a **prerequisite that is already assumed**. Josh said so in
`planning/curriculum/ANSWERS-3.md`: SOH-CAH-TOA needs "coordinates so we can
have the unit circle", and Pythagoras is one of the six gateways in the topic
tree. So `angles-and-waves` — the proposal that carries the unit circle — is
building on a tutorial that does not exist and is not proposed.

This is the clearest thing the survey turned up. **The next outline to write is
coordinate geometry**, and it sits before Angles and Waves rather than after it.

It is also the most natural home for **MIT-4.9**, practical right-triangle
trigonometry: heights and distances from an angle and a side, which is
Pythagoras and the ratios put to work. Whether it belongs there or in Angles and
Waves is a judgement about pacing rather than about the maths.

### MIT-4.7 is a sentence, not a tutorial

Trigonometric ratios in surd form — the exact values at 30, 45 and 60 degrees.
It belongs inside Angles and Waves as a section, and the outline should say so
rather than leaving it to be noticed later. One line in `covers:`.

### MIT-2.3 is Venn diagrams, and it has no home at all

`sets-as-sorted-lists` teaches sets and does not draw them; `logic-and-truth`
proposes truth tables and De Morgan and does not draw them either. Two and three
set Venn diagrams are a drawing exercise, and matplotlib can do them.

Three options, and I would take the second:

1. A section inside `logic-and-truth`, which turns a short tutorial into a full
   one. De Morgan's Laws are the natural pairing — the picture is the proof.
2. A section added to `sets-as-sorted-lists`, which already exists and already
   has the vocabulary. Cheapest, and it puts the picture where the sets are.
3. Its own short tutorial. Hard to justify for one outcome.

## Computational Methods 5N0554: not measured at all

Two tutorials against a 150-hour, 15-credit module with thirteen outcomes.

The thirteen outcomes are **not in `outcomes.yaml`**, so the curriculum map does
not measure this module and the numbers above do not include it. That is a
deliberate decision — Josh asked for the map to be MIT and PDP only — but it has
a side effect worth naming: *there is no count of what this module is missing,
so it cannot appear in a survey like this one.*

Transcribing the thirteen outcomes is still on the list. Doing it would let this
module be counted without putting it on the map, if `outcomes.yaml` grows a way
to say "tracked but not mapped". Whether that is worth the machinery is a real
question and not one to answer here.

What is known about the shape of it, from `planning/curriculum/ANSWERS-3.md`:

- **The matrices strand** — five tutorials outlined in
  `planning/outlines/matrices.md`, ending in Markov chains and PageRank rather
  than eigenvectors. That outline still needs the eigenvector bonus dropped and
  Markov promoted, which was agreed and not yet applied to the file.
- **Six other strands named by the descriptor** and not outlined at all: discrete
  probability and randomness, modelling and simulation, algorithms and
  complexity, applications of probability, problem definition and solution
  design, and reflection.
- Every worked example the descriptor names is **a suggestion rather than a
  requirement**. Cover the topics; choose the route.

So the honest summary for this module is: one strand outlined, six not, and no
measurement either way.

---

## If I had to order it

1. **Coordinate geometry** — write the outline. It closes four outcomes, it is
   already assumed by a proposal, and it is the only gap that is a whole missing
   tutorial rather than a section in somebody else's.
2. **Fold MIT-4.7 into Angles and Waves and MIT-2.3 into one of the two set
   tutorials.** Both are edits to outlines that already exist, and both stop a
   gap being discovered at the end.
3. **The two everlearning conversions** — How We Got Here and When It Goes
   Wrong. They are conversions rather than new writing, so they are the cheapest
   real progress available, and they close three PDP outcomes.
4. **Drawing Functions**, then **Angles and Waves**. The two full maths
   tutorials everything else in Section 3 and 4 hangs off.
5. Everything else in the proposals table, in the order it already declares.

The matrices strand and the rest of 5N0554 are a separate body of work, not the
next thing.
