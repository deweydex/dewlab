# Outline — The Matrices Strand

**Module:** `computational-methods` (not `mit-pdp-maths-prog-integration`),
**series:** `matrices` — alongside `python-fundamentals`, already in that
module.
**Closes:** nothing in the MIT descriptor, which is why this outline was
written before 5N0554 existed as data. It now closes `CMPS-LO4` in full, and
touches `CMPS-LO1` and `CMPS-LO2` — see DECISIONS_LOG 7.56.
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

Markov chains, structured as a dedicated practical tutorial.

A transition matrix multiplied by itself repeatedly demonstrates repeated matrix
multiplication converging to a stationary distribution. Upstream materials
in `everlearning/OtherCourses/Markov-Chains-and-Text-Generation` and
`deweydex/Mathematics/worksheet_07d_markov_chains.md` provide established foundations.

- **Cell:** a weather matrix, three states, one step at a time.
- **Cell:** the same matrix raised to a power, watching the rows converge.
- **Cell:** text generation from a transition matrix built out of a real
  paragraph — demonstrating computational linear algebra applications.
- **Point to make:** convergence to stationary state without requiring
  abstract eigenvector formalism.

**PageRank** represents the same computation over a web link graph, included
here or as a companion module.

## Dropped from Scope

- **Formal Eigenvector Theory**: PageRank and steady-state distributions are taught
  empirically via iterative matrix powers rather than formal characteristic
  polynomials and eigenspaces, keeping focus on algorithmic linear algebra.

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
- ~~Which application carries tutorial 6.~~ **Settled: it rides along.**
  *Where Chains Lead* is weather, then convergence, then word-level text
  generation, then a hand-checkable three-page PageRank example, in that
  order — four sections, not a fifth tutorial's worth. PageRank as a
  dedicated tutorial over a real, larger link graph remains open; what is
  closed here is small enough that a worked example inside the Markov
  tutorial was the honest size for it, rather than manufacturing a seventh
  tutorial to hold three cells.
