# Curriculum notes

How the curriculum is organized, what its early coverage analysis
found, and the terminology rules that keep maths and programming from
talking past each other.

---

## 1. Where the curriculum data lives

| File | What's in it |
|---|---|
| [`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md) | Generated — every descriptor outcome, mapped to the tutorial that teaches it (or doesn't yet). |
| [`curriculum/outcomes.yaml`](./curriculum/outcomes.yaml) | Every learning outcome from the accredited module descriptors. |
| [`curriculum/out-of-scope.yaml`](./curriculum/out-of-scope.yaml) | What's been deliberately left out, and why — plus a record of anything that came back in. |
| [`curriculum/proposed.yaml`](./curriculum/proposed.yaml) | Tutorials that don't exist yet, and which outcomes they'd cover. |
| [`curriculum/DECISIONS_NEEDED.md`](./curriculum/DECISIONS_NEEDED.md) | Open questions about sequencing and scope, waiting on a decision. |
| [`outlines/`](./outlines/) | An outline for each proposed module. |

---

## 2. What the first coverage pass found

Looking at the 65 accredited learning outcomes early on showed a
lopsided picture — some strands fully covered, others essentially
untouched:

- **Fully covered**: Algorithms (9 of 9), Probability (8 of 8),
  Statistics (5 of 5), Number sets.
- **Not started**: Calculus (0 of 3), Trigonometry (0 of 6), Function
  graphing and analysis (0 of 3), Formal logic (0 of 2).
- **Partly covered**: Geometry (2 of 6), Core programming (7 of 11),
  Algebra (6 of 8).

### Quiet gaps — things used before they were taught

A few ideas kept turning up in code examples before any tutorial had
actually taught them:

1. **Truth tables (`MIT-2.4`)** — `and`/`or`/`not` showed up in early
   control-flow tutorials with no truth table or formal evaluation rule
   behind them. Fixed by scheduling *Logic and Truth*.
2. **Complex roots (`MIT-1.10`)** — solving a quadratic with a negative
   discriminant was handled by saying "no real solutions," with the
   imaginary unit $i$ never introduced. Fixed by scheduling *When There
   Is No Answer*.
3. **Inverse functions (`MIT-3.1`)** — function mappings were referenced
   without domain/range inversion ever being formally defined.
4. **Formula transposition (`MIT-1.7`)** — several science-flavoured
   exercises assumed a student could already rearrange an equation.
   Fixed by scheduling *Rearranging Formulae*.

---

## 3. Regrouping and sequencing

### *Numbers and Their Families*, reconsidered
Looking at this tutorial again showed it was actually three separate
ideas wearing one title:
- Number domains (`MIT-2.1`) — set theory, $\mathbb{N} \subset \mathbb{Z}
  \subset \mathbb{Q} \subset \mathbb{R}$.
- Exponents and logarithms (`MIT-1.1`) — algebra and inverse operations.
- Geometric formulas (`MIT-1.2`, `MIT-1.3`) — mensuration.

Splitting that apart changed where each piece sits:
- Number domains line up naturally with `int`/`float`, so they moved
  early.
- Exponents and logarithms now come before combinatorial counting,
  standard deviation, and polynomial calculus — all of which lean on
  them.
- Geometric formulas became a concrete application once function
  definition existed to hang them on.

### *Expressions Come Alive*
Stays narrowly focused on polynomial representation, evaluation, and
arithmetic (add, multiply, subtract) — the direct foundation for
*Cracking Equations* (algebraic solving) and *Rates of Change*
(polynomial calculus).

### Order lives in a file, not in the title
A tutorial's title never encodes its position ("Expressions Come Alive,"
not "Tutorial 14") — reading order comes from each series'
`<series>.order.yaml` file instead. That's what lets a new tutorial get
inserted anywhere in a series without renaming every file that comes
after it.

---

## 4. Terminology: keeping maths and programming from colliding

A handful of words mean genuinely different things in a maths context
and a programming one, and the curriculum sticks to one meaning per
word so a tutorial never has to disambiguate mid-sentence:

| Word | The rule | Why |
|---|---|---|
| **Index / Indices** | Only for a position in a list or sequence, or a summation bound. Use **power** or **exponent** for exponentiation. | Keeps `list[i]` from colliding with an algebraic power. |
| **Function** | Always say clearly whether you mean a Python callable (`def foo():`) or a mathematical mapping ($f: X \to Y$). | A function that returns nothing and a pure mapping aren't the same idea. |
| **Range** | Say clearly whether you mean Python's `range(start, stop)` or a statistical spread / a function's codomain. | One's an iteration tool, the other's a description of values. |
| **Set** | Distinguish Python's `set` collection from a mathematical set, and from a variable assignment (`=`). | Matters most in discrete maths and anything touching databases. |
| **Expression** | Distinguish a Python expression that actually evaluates from an algebraic symbolic expression. | Matters most once SymPy or any symbolic-computation content is involved. |
