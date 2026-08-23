# Outline — Drawing Sets

**Closes:** `MIT-2.3` (Venn diagrams for two and three sets).
**Goes after:** Tutorial 16, Sets as Sorted Lists.
**Sits beside:** Logic and Truth, which proves the same laws in a different
notation.
**Builds on:** Tutorial 16 (set operations), Tutorial 12 (plotting).
**Size:** short.

## Scope Rationale & Computational Framing

Venn diagrams were initially excluded from the curriculum when considered as manual pen-and-paper notation.

Restructuring Venn diagrams as a computational visualization module resolves this objection: Matplotlib plots diagram regions directly from real Python set operations, framing the diagram as computed output rather than manual drawing notation.

## Modular Isolation vs Composite Merging

Rather than folding Venn diagrams into *Logic and Truth* or *Sets as Sorted Lists*, keeping *Drawing Sets* as a dedicated, focused module provides clear modular boundaries:
- *Sets as Sorted Lists* focuses on algorithmic data structures (sorted lists, membership, operations from scratch).
- *Logic and Truth* focuses on Boolean truth tables and formal proofs.
- *Drawing Sets* focuses on visual set verification and Venn region plotting in Python.

This adheres to the core architecture pattern: **explicit connections between focused modules rather than overloaded composite tutorials**.

## The shape

### 1. Two circles, from real sets

- **Cell:** two Python sets from Tutorial 16 — say the students who own a bike
  and the students who own a car — and a plot of two overlapping circles with the
  counts written in the three regions.
- **Cell:** the same drawing function called with sets that do not overlap, and
  with one set inside another. The picture changes; the code does not.
- **Point to make:** the diagram is output. It is drawn from the sets, so it
  cannot disagree with them.

### 2. The regions have names you already know

- **Cell:** each region labelled with the operation that produces it —
  intersection in the middle, the two differences either side, union as all
  three together.
- **Your turn:** given a picture with counts in it, write the expression for each
  region.
- **Point to make:** nothing new is being defined. Tutorial 16's operations are
  being given somewhere to sit.

### 3. Three sets, which is where it earns its place

- **Cell:** three circles, seven regions, counts in each.
- **Cell:** an expression a student would struggle to reason about in symbols —
  `(A ∪ B) − C` — highlighted on the diagram.
- **Your turn:** two expressions that look different. Are they the same set?
  Answer from the picture, then check with Python.
- **Point to make:** two sets are easy to hold in your head and three are not.
  This is the size at which the picture starts doing work you cannot do without
  it.

### 4. The same laws, in a different notation

The link to Logic and Truth, made once and briefly.

- **Cell:** the complement of a union, and the intersection of the complements,
  shaded on the same diagram. Identical regions.
- **Point to make:** this is De Morgan again. Logic and Truth proves it by
  checking four rows; here it is proved by looking. Neither proof is better —
  they are the same claim in two notations, which is what makes the pairing worth
  the link.

### 5. Where the picture stops helping

- **Cell:** four sets. The three-circle drawing does not extend — four circles
  cannot make all fifteen regions, which is a real fact about the plane and not a
  limitation of the code.
- **Point to make:** every representation runs out. Knowing where is part of
  knowing the representation, and the set operations keep working long after the
  picture gives up.

## What to reuse

Tutorial 16's set functions, unchanged. The drawing helper is written here and
used nowhere else, which is a fair description of how much machinery this
tutorial needs.

## Open questions

- **The title.** "Drawing Sets" rather than "Venn Diagrams", on the same
  reasoning as "Lines and Distances": it says what a student will do rather than
  naming a convention. But "Venn diagram" is the phrase an examiner will use, so
  it has to appear early and be findable.
- **Section 5.** The four-set impossibility is the most interesting thing in the
  tutorial and the least examinable. Keep it as a closing aside rather than a
  section if the tutorial runs long.
