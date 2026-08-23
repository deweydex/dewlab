# Curriculum Design Decisions — Synthesis & Architecture

Formal architectural specifications covering the authoring editor capabilities, dependency graph gateways, and syllabus mapping for Computational Methods.

---

## 1. Authoring Editor Capabilities

The browser-based authoring editor (`planning/EDITOR.md`) provides dual capabilities:
1. **Series Structure Management**: Reordering, inserting, and creating tutorials with automated `order.yaml` branch commits.
2. **Content & Cell Editing**: In-place editing of Markdown prose, frontmatter metadata, and executable Python code cells.

### Structural Integrity Safeguards
- **Cell ID Mutation Warnings**: The editor actively inspects working versus baseline cell IDs and alerts authors before committing ID changes that would orphan student progress.
- **Structural Linting**: Previews document structure, unclosed fences, and unique cell ID validation prior to GitHub PR submission.

---

## 2. Dependency Graph Architecture & Gateways

1. **Searching & Sorting Partition**: Divide-and-conquer is demonstrated across two independent contexts: binary search over ordered sequences (*Finding Things*) and merge sort over arbitrary sequences (*Putting Things in Order*).
2. **Pythagoras as Gateway Node**: Pythagoras unlocks seven downstream topics in the topic dependency tree, requiring coordinate geometry as a prerequisite for trigonometric unit circle derivation.
3. **Graph Legend & Visualization Key**: The interactive topic tree provides explicit color-coded legends for curriculum strands.

---

## 3. Computational Methods (5N0554) Syllabus Integration

The syllabus for *Computational Methods and Problem Solving 5N0554* (Dublin and Dún Laoghaire ETB, 15 credits, 13 learning outcomes) outlines the following core strands:

| Section | Core Syllabus Concepts |
|---|---|
| 1. Discrete Computational Structures | Arrays, lists, matrices, recurrence relations, iterative vs. recursive algorithms. |
| 2. Discrete Probability | Distributions, expectation, random numbers in computing, cryptographic entropy. |
| 3. Modelling and Simulation | Numerical computation, Monte Carlo methods. |
| 4. Linear Algebra & Applications | Matrix operations in computer graphics, Markov chains, PageRank, nearest-neighbor classification. |
| 5. Algorithms & Complexity | Best, average, and worst-case algorithmic complexity. |
| 6. Applied Probability | Reliability engineering, failure prediction, network traffic modeling. |
| 7. Systems Modelling | Server room thermal dynamics, robotic feedback control, traffic simulation. |
