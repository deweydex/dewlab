# Curriculum Scope & Architecture Resolutions

Formal resolution record for the seven core curriculum decisions formulated in `DECISIONS_NEEDED.md`.

---

## 1–3. Trigonometry, Radians, Coordinate Geometry — **In Scope in Full**

Right-triangle trigonometry (`MIT-4.4`, `MIT-4.9`), radians and the unit circle (`MIT-4.5`, `MIT-4.6`), and coordinate geometry (`MIT-4.1`–`4.3`) are incorporated in full.

**Pedagogical Principle**: Tutorial length and module count are unconstrained; comprehensive conceptual coverage and clear modular isolation are prioritized over compressed composite tutorials.

## 4. Complex Roots — **Dedicated Module & Non-Real Solutions**

Tutorial 15 maintains its focused treatment of quadratic real roots, linking directly to a dedicated unit on complex numbers and the imaginary unit $i$ (*When There Is No Answer*, `MIT-1.10`).

## 5. Sequence & Numbering — **Decouple Numbering from Files, Implement Editor**

Numbered titles and filenames were eliminated across the curriculum:
- Filenames and titles are decoupled from fixed ordinal positions, preventing cascading renames upon insertion.
- The visual authoring editor (`planning/EDITOR.md`) manages sequence order directly via series order files (`<series>.order.yaml`).

## 6. Calculus — **Two Focused Tutorials and Application Synthesis**

- *Approaching a Limit* (computational limits, secant slopes).
- *Rates of Change* (power rule differentiation, polynomial integration, constant of integration).
- Specialized algebraic manipulations (quotient rule, integration by parts) are excluded in favor of computational applications.

## 7. Modular Scope Decomposition

Tutorials are decomposed into focused, single-concept units with explicit cross-references (e.g. splitting polynomial representation, quadratic algebra, and polynomial graphing into dedicated modules).

---

## 8. Practice Problems Specification

Architecture for practice problem sets paired with each tutorial, featuring collapsible in-line solutions and section-level verification helpers (`planning/EXERCISES.md`, `planning/PRACTICE.md`).
