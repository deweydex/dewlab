# Outline — The Matrices Strand

**Series:** `computational-methods` (not `maths-for-it`).
**Closes:** nothing in the MIT descriptor. That is the point — this is the first
strand that is deliberately *beyond* the module, and the reason the second
series exists.
**Attaches to:** lists and arrays (`MIT-6.3`) and coordinate graphing
(`MIT-3.2`). Nothing else in the map depends on it.

## Why this, and why here

You asked for computational-methods material that does not appear in Maths for
IT, and for matrices specifically:

> having a student think through the basic operations of matrices and code them
> up themselves and also see how those different types of mappings skew space
> and all sorts of other nice plotting things there.

Checking the descriptor against `everlearning` confirms the gap is real. The MIT
outcomes touch matrices exactly once, sideways: `MIT-1.12` (simultaneous
equations in two and three unknowns), where `everlearning`'s own inventory notes
that the three-unknown case *"currently only [exists] via the matrix-method
worksheet"*. Matrices are the tool that case is already reaching for and never
gets given.

`everlearning` also already has the pen-and-paper half written, and marks it as
outside the syllabus in its own inventory:

| Worksheet | Covers | Marked |
|---|---|---|
| `worksheet_07a_matrix_operations.md` | operations, determinants, inverses | beyond MIT syllabus |
| `worksheet_07b_linear_systems.md` | Gaussian elimination, 3 unknowns, RREF | — (the `MIT-1.12` overflow) |
| `worksheet_07c_eigenvalues_eigenvectors.md` | eigenvalues, eigenvectors, PCA | beyond MIT syllabus |
| `worksheet_07d_markov_chains.md` | transition matrices, steady state | beyond MIT syllabus |

So the strand is not new authorship from nothing. It is the interactive half of
material that exists on paper, plus the thing paper cannot do — showing a
mapping act on a picture and watching the picture move.

## Where it attaches, and why only there

Two edges, both of them mild:

- **Lists and arrays (`MIT-6.3`).** A matrix is a list of lists before it is
  anything else. A student who has indexed a list can index a grid.
- **Graphing functions (`MIT-3.2`).** A mapping that skews space is only
  legible to someone who can already draw a shape on axes.

Nothing downstream in the existing map needs matrices, which means the whole
strand hangs off the side of the tree and can be taken in a spare week or
skipped entirely — the flexibility case, working as intended.

## The shape — five small tutorials

Following the split-into-single-topics principle. Each is one sitting.

### 1. A Grid of Numbers

A matrix as a list of lists, and the operations that are just bookkeeping.

- **Cell:** build a 2×2 and a 2×3 by hand as nested lists; print them so the
  rows line up. (A `show(m)` that pads columns — small, and used all strand.)
- **Cell:** `add(a, b)` and `scale(k, m)`, written by the student.
- **Cell:** the shape rule. `add` on mismatched shapes should raise something
  the student wrote, not an `IndexError` from the middle of a loop.
- **Your turn:** transpose. It is four lines and it is the first operation with
  no arithmetic in it at all.

### 2. Multiplying Grids

The one operation nobody guesses, done slowly.

- **Cell:** the dot product of two lists, on its own, first.
- **Cell:** `multiply(a, b)` built from it — one dot product per output cell.
- **Point to make:** why the inner dimensions must match, discovered by trying
  a pair that does not and reading the student's own error.
- **Cell:** show `A @ B` and `B @ A` differ. Order matters, demonstrated rather
  than announced.
- **Your turn:** the identity matrix. Find the one that leaves things alone.

### 3. What a Matrix Does to a Picture

The tutorial the strand exists for.

- **Cell:** a unit square as four points; plot it.
- **Cell:** apply a 2×2 to each corner with the student's own `multiply`, and
  plot before and after on the same axes.
- **Cell:** a small gallery, one change at a time — stretch, squash, rotate,
  shear, reflect. The student predicts the picture before running.
- **Point to make:** the columns of the matrix are where `(1,0)` and `(0,1)`
  land. Once seen, every matrix in the gallery can be read off by eye.
- **Your turn:** given a picture of a transformed square, write the matrix.
  Check by running it.

### 4. Undoing It

Determinant and inverse, arrived at from the pictures rather than the formula.

- **Cell:** measure the area of the transformed square from tutorial 3. Compare
  with `ad - bc`. The determinant is discovered as the area factor before it is
  named. (Discover-then-name, as with the chain rule.)
- **Cell:** a matrix with determinant zero, and its picture — the square
  collapsing to a line. Why nothing can be undone from there.
- **Cell:** the 2×2 inverse; apply it to the transformed square and watch the
  original come back.
- **Your turn:** which of these five matrices can be undone? Answer from the
  determinant, then confirm with the picture.

### 5. Solving Systems

`MIT-1.12`'s three-unknown case, finally with the right tool.

- **Cell:** three equations as a grid plus a right-hand side.
- **Cell:** Gaussian elimination, one row operation at a time, printing the grid
  after each. The algorithm is visible as a sequence of pictures of numbers.
- **Cell:** the same system through the inverse from tutorial 4, agreeing.
- **Point to make:** the two-unknown elimination they did by hand earlier was
  this, on a smaller grid.

## Tutorial 6 — Where it settles

Markov chains, promoted from a bonus to a tutorial. Josh: *"I think we dont need
eigenvectors but markov would be great."*

A transition matrix multiplied by itself repeatedly is tutorial 2 doing
something a student can care about, and it ends somewhere: the distribution
stops moving. `everlearning`'s `OtherCourses/Markov-Chains-and-Text-Generation`
is a whole small course already and `worksheet_07d_markov_chains.md` is the
paper half, so this is largely a conversion.

- **Cell:** a weather matrix, three states, one step at a time.
- **Cell:** the same matrix raised to a power, watching the rows converge.
- **Cell:** text generation from a transition matrix built out of a real
  paragraph — the payoff, and the reason this is worth a tutorial rather than a
  footnote.
- **Point to make:** the thing it settles on does not depend on where it
  started. That is the whole idea, and it needs no eigenvector vocabulary
  anywhere — which is why dropping eigenvalues costs nothing.

**PageRank** is the same computation on a graph of links, and it belongs here or
as a seventh tutorial depending on how long tutorial 6 runs. The 5N0554
descriptor names it under linear algebra and applications, as *one suggestion
among several* — graphics, games, sequence alignment and nearest neighbour sit
beside it. It is here because it is worth teaching, not because it is required.

## Dropped, and why

- **Eigenvectors.** They fall out of tutorial 3's gallery nicely, and
  `worksheet_07c` has the paper half, so this was a real candidate. Josh's call,
  and a defensible one: PageRank is an eigenvector problem in disguise and
  teaches perfectly well as repeated multiplication converging. The vocabulary
  buys nothing at this level.

## Bonus, if the strand earns it

- **Rasterization** — `OtherCourses/Computer-Graphics-Algorithms` has Bresenham
  and midpoint-circle notebooks. Different topic, same "coordinates become
  pixels" instinct, and convertible with `dev/from_notebook.py`.

## What to reuse

`show(m)` from tutorial 1 and `multiply(a, b)` from tutorial 2 carry the whole
strand. No NumPy anywhere until the last section of the last tutorial, where
`numpy` appears once to say *this is what you just built, and it is why the
library exists*.

## Open questions, and two that closed

- ~~Does this strand assume the maths series, or stand alone?~~ **Not a data
  question any more.** The curriculum map is MIT and PDP only, so there is no
  edge to draw either way and nothing in the build depends on the answer. It
  stays a teaching note: the strand leans on lists and on graphing, and a
  student who has not met those will feel it.
- ~~Is five tutorials too large a fraction of the series?~~ **No.** 5N0554 is a
  150-hour module with thirteen outcomes across seven sections, of which
  matrices are one. Five to seven matrix tutorials is proportionate — what would
  be out of proportion is the six other strands having nothing.
- Still open: **which application carries tutorial 6.** Markov is settled;
  whether PageRank rides along inside it or becomes a seventh tutorial depends
  on how long the text-generation section runs once it is written.
