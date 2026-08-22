# Curriculum map

**Generated — do not edit by hand.** `python3 dev/curriculum_map.py`
rebuilds it from three files, and CI fails if this one is out of date:

- `planning/curriculum/outcomes.yaml` — every learning outcome in the two
  QQI module descriptors.
- each tutorial's `covers:` frontmatter — which outcome each section
  teaches, and which it only uses.
- `planning/curriculum/out-of-scope.yaml` — what we have decided not to
  teach, so a decision stops looking like a gap.

Every link below goes to the section of the live site that does the work,
so this doubles as a way of finding where anything is taught.

## Where we stand

**41 of 65** outcomes are in place, once the 2 we have ruled out are set aside.

- 🟩 **40 taught** — a tutorial section teaches it.
- 🟦 **1 taught in part** — deliberately narrowed, and the narrowed version is written.
- 🟨 **4 used but not taught** — students meet it in passing without it ever being the subject. These are the quiet gaps: they look covered from a distance.
- 🟥 **20 not covered** — nothing in dewlab touches it.
- ⬜ **2 out of scope** — see `planning/curriculum/out-of-scope.yaml` for why.

### By strand

| Strand | 🟩 Taught | 🟦 Part, by choice | 🟨 Used only | 🟥 Not covered | ⬜ Out of scope |
|---|---:|---:|---:|---:|---:|
| **algebra** | 5 | 1 | 2 | 0 | 0 |
| **algorithms** | 9 | 0 | 0 | 0 | 0 |
| **calculus** | 0 | 0 | 0 | 3 | 0 |
| **functions** | 0 | 0 | 1 | 2 | 0 |
| **geometry** | 2 | 0 | 0 | 4 | 0 |
| **logic** | 0 | 0 | 1 | 1 | 0 |
| **number** | 2 | 0 | 0 | 0 | 0 |
| **probability** | 8 | 0 | 0 | 0 | 0 |
| **programming** | 7 | 0 | 0 | 4 | 0 |
| **sets** | 2 | 0 | 0 | 0 | 1 |
| **statistics** | 5 | 0 | 0 | 0 | 0 |
| **trigonometry** | 0 | 0 | 0 | 6 | 1 |

```mermaid
graph LR
  algebra["algebra<br/>6 of 8 in place"]
  algorithms["algorithms<br/>9 of 9 in place"]
  calculus["calculus<br/>0 of 3 in place"]
  functions["functions<br/>0 of 3 in place"]
  geometry["geometry<br/>2 of 6 in place"]
  logic["logic<br/>0 of 2 in place"]
  number["number<br/>2 of 2 in place"]
  probability["probability<br/>8 of 8 in place"]
  programming["programming<br/>7 of 11 in place"]
  sets["sets<br/>2 of 2 in place"]
  statistics["statistics<br/>5 of 5 in place"]
  trigonometry["trigonometry<br/>0 of 6 in place"]

  classDef full fill:#edf7f0,stroke:#1f6b3f,color:#1f6b3f;
  classDef part fill:#fdf6ec,stroke:#b5651d,color:#7a4310;
  classDef none fill:#fdf0ef,stroke:#9b2226,color:#9b2226;
  class algorithms,number,probability,sets,statistics full;
  class algebra,geometry,programming part;
  class calculus,functions,logic,trigonometry none;
```

## The series as it stands

Solid arrows are the reading order. A dashed arrow means the later
tutorial names the earlier one in its own text — evidence of a real
dependency rather than an intention, found by reading the tutorials
themselves. A tutorial with several dashed arrows into it is
load-bearing and expensive to move; one with none is cheap to move, and
possibly not pulling its weight where it is.

```mermaid
graph TD
  T1["1. First Steps"]
  T2["2. Storing and Computing"]
  T3["3. Making Decisions"]
  T4["4. Repeating Yourself"]
  T5["5. Lists and Sequences"]
  T6["6. Finding Things"]
  T7["7. Putting Things in Order"]
  T8["8. Building Reusable Tools"]
  T9["9. Counting Carefully"]
  T10["10. What Are the Chances?"]
  T11["11. Making Sense of Data"]
  T12["12. Pictures Worth Numbers"]
  T13["13. Numbers and Their Families"]
  T14["14. Expressions Come Alive"]
  T15["15. Cracking Equations"]
  T16["16. Sets as Sorted Lists"]
  T17["17. Bringing It All Together"]
  T18["18. Looking Back Before Moving Forward"]

  T1 --> T2
  T2 --> T3
  T3 --> T4
  T4 --> T5
  T5 --> T6
  T6 --> T7
  T7 --> T8
  T8 --> T9
  T9 --> T10
  T10 --> T11
  T11 --> T12
  T12 --> T13
  T13 --> T14
  T14 --> T15
  T15 --> T16
  T16 --> T17
  T17 --> T18

  T9 -.->|builds on| T4
  T16 -.->|builds on| T6
  T16 -.->|builds on| T7
  T17 -.->|builds on| T1
  T17 -.->|builds on| T13
  T17 -.->|builds on| T14
  T17 -.->|builds on| T15
```

## What is missing, and where it would go

Dashed boxes are proposed. Placement is argued in
`planning/curriculum/proposed.yaml` and each has an outline in
`planning/outlines/`.

```mermaid
graph TD
  T1["1. First Steps"]
  T2["2. Storing and Computing"]
  T3["3. Making Decisions"]
  T4["4. Repeating Yourself"]
  T5["5. Lists and Sequences"]
  T6["6. Finding Things"]
  T7["7. Putting Things in Order"]
  T8["8. Building Reusable Tools"]
  T9["9. Counting Carefully"]
  T10["10. What Are the Chances?"]
  T11["11. Making Sense of Data"]
  T12["12. Pictures Worth Numbers"]
  T13["13. Numbers and Their Families"]
  T14["14. Expressions Come Alive"]
  T15["15. Cracking Equations"]
  T16["16. Sets as Sorted Lists"]
  T17["17. Bringing It All Together"]
  T18["18. Looking Back Before Moving Forward"]
  N0("Rearranging Formulae")
  N1("When There Is No Answer (And Then There Is)")
  N2("Drawing Functions")
  N3("Angles and Waves")
  N4("Approaching a Limit")
  N5("Rates of Change")
  N6("Logic and Truth")
  N7("How We Got Here")
  N8("When It Goes Wrong")
  N9("The Team Project")

  T1 --> T2
  T2 --> T3
  T3 --> T4
  T4 --> T5
  T5 --> T6
  T6 --> T7
  T7 --> T8
  T8 --> T9
  T9 --> T10
  T10 --> T11
  T11 --> T12
  T12 --> T13
  T13 --> T14
  T14 --> T15
  T15 --> T16
  T16 --> T17
  T17 --> T18

  T14 ==> N0
  T15 ==> N1
  T15 ==> N2
  N2 ==> N3
  N3 ==> N4
  N4 ==> N5
  T16 ==> N6
  T1 ==> N7
  T3 ==> N8
  T17 ==> N9

  classDef new fill:#fdf6ec,stroke:#b5651d,color:#7a4310,stroke-dasharray:4 3;
  class N0,N1,N2,N3,N4,N5,N6,N7,N8,N9 new;
```

| Proposed | Goes after | Closes | Size |
|---|---|---|---|
| **Rearranging Formulae** | after tutorial-14-expressions-come-alive | `MIT-1.7` | short |
| **When There Is No Answer (And Then There Is)** | after tutorial-15-cracking-equations | `MIT-1.10` | short |
| **Drawing Functions** | after tutorial-15-cracking-equations | `MIT-3.1`, `MIT-3.2`, `MIT-3.4`<br/>_if kept:_ `MIT-4.1`, `MIT-4.2`, `MIT-4.3` | full |
| **Angles and Waves** | after drawing-functions | `MIT-3.3`, `MIT-4.5`, `MIT-4.6`, `MIT-4.8`, `MIT-4.10`<br/>_if kept:_ `MIT-4.4`, `MIT-4.9` | full |
| **Approaching a Limit** | after angles-and-waves | `MIT-3.5` | short |
| **Rates of Change** | after approaching-a-limit | `MIT-3.6`, `MIT-3.7` | full |
| **Logic and Truth** | after tutorial-16-sets-as-sorted-lists | `MIT-2.4`, `MIT-2.5` | short |
| **How We Got Here** | after tutorial-01-first-steps | `PDP-LO1`, `PDP-LO3` | full |
| **When It Goes Wrong** | after tutorial-03-making-decisions | `PDP-LO9` | full |
| **The Team Project** | after tutorial-17-bringing-it-all-together | `PDP-LO12` | not-a-tutorial |

## Every outcome

### Maths for Information Technology 5N18396

#### 1. Basic Arithmetic and Algebra

| Outcome | | Where |
|---|---|---|
| `MIT-1.1` Operations in N, Z, Q, R; powers (the syllabus says indices) and logarithms | 🟩 | [Tutorial 3: Making Decisions — Classifying Numbers: A Mathematical Application](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-03-making-decisions.html#classifying-numbers-a-mathematical-application)<br/>[Tutorial 13: Numbers and Their Families — Powers and Their Rules](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-13-numbers-and-their-families.html#powers-and-their-rules)<br/>[Tutorial 13: Numbers and Their Families — Logarithms: The Inverse of Powers](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-13-numbers-and-their-families.html#logarithms-the-inverse-of-powers) |
| `MIT-1.2` Area and perimeter: square, rectangle, triangle, circle | 🟩 | [Tutorial 13: Numbers and Their Families — Practical Geometry: Formulas as Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-13-numbers-and-their-families.html#practical-geometry-formulas-as-functions) |
| `MIT-1.3` Volume and surface area: cube, cylinder, cone, sphere | 🟩 | [Tutorial 13: Numbers and Their Families — Practical Geometry: Formulas as Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-13-numbers-and-their-families.html#practical-geometry-formulas-as-functions) |
| `MIT-1.4` Binary and hexadecimal arithmetic and conversion | 🟩 | [Tutorial 2: Storing and Computing — Number Systems: How Computers Count](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-02-storing-and-computing.html#number-systems-how-computers-count) |
| `MIT-1.5` Distinguish an expression from an equation | 🟦 | [Tutorial 14: Expressions Come Alive — Expressions versus Equations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-14-expressions-come-alive.html#expressions-versus-equations)<br/>**Narrowed:** not the formal expression-versus-equation distinction as an assessed item |
| `MIT-1.6` Evaluate, expand and simplify expressions | 🟩 | [Tutorial 14: Expressions Come Alive — Representing Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-14-expressions-come-alive.html#representing-polynomials)<br/>[Tutorial 14: Expressions Come Alive — Evaluating Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-14-expressions-come-alive.html#evaluating-polynomials)<br/>[Tutorial 14: Expressions Come Alive — Displaying Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-14-expressions-come-alive.html#displaying-polynomials)<br/>[Tutorial 14: Expressions Come Alive — Adding Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-14-expressions-come-alive.html#adding-polynomials)<br/>[Tutorial 14: Expressions Come Alive — Subtracting and Scaling](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-14-expressions-come-alive.html#subtracting-and-scaling)<br/>_used in:_ [Tutorial 17: Bringing It All Together — Problem 1: The Polynomial Workshop](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-17-bringing-it-all-together.html#problem-1-the-polynomial-workshop) |
| `MIT-1.7` Transpose formulae; operate on rational algebraic expressions | 🟨 | _used in:_ [Tutorial 15: Cracking Equations — Solving Linear Equations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-15-cracking-equations.html#solving-linear-equations) |
| `MIT-1.8` Multiply linear expressions into quadratics and cubics | 🟩 | [Tutorial 14: Expressions Come Alive — Multiplying Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-14-expressions-come-alive.html#multiplying-polynomials)<br/>_used in:_ [Tutorial 17: Bringing It All Together — Problem 1: The Polynomial Workshop](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-17-bringing-it-all-together.html#problem-1-the-polynomial-workshop) |
| `MIT-1.9` Factor quadratics by inspection and solve them | 🟩 | [Tutorial 15: Cracking Equations — Factorisation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-15-cracking-equations.html#factorisation) |
| `MIT-1.10` Solve quadratics, including complex roots | 🟨 | _used in:_ [Tutorial 15: Cracking Equations — The Quadratic Formula](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-15-cracking-equations.html#the-quadratic-formula) |
| `MIT-1.11` Solve linear inequalities | 🟩 | [Tutorial 15: Cracking Equations — Solving Inequalities](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-15-cracking-equations.html#solving-inequalities) |
| `MIT-1.12` Simultaneous equations in two and three unknowns | 🟩 | [Tutorial 15: Cracking Equations — Simultaneous Equations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-15-cracking-equations.html#simultaneous-equations)<br/>_used in:_ [Tutorial 17: Bringing It All Together — Problem 2: Where Do They Meet?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-17-bringing-it-all-together.html#problem-2-where-do-they-meet) |

#### 2. Set Theory and Boolean Logic

| Outcome | | Where |
|---|---|---|
| `MIT-2.1` Set language: N, Z, Q, R, C, the empty set; finite, infinite, cardinality | 🟩 | [Tutorial 13: Numbers and Their Families — The Number Domains](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-13-numbers-and-their-families.html#the-number-domains)<br/>[Tutorial 16: Sets as Sorted Lists — Making a Set](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-16-sets-as-sorted-lists.html#making-a-set)<br/>[Tutorial 16: Sets as Sorted Lists — Membership Testing](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-16-sets-as-sorted-lists.html#membership-testing)<br/>[Tutorial 16: Sets as Sorted Lists — Set Language and Notation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-16-sets-as-sorted-lists.html#set-language-and-notation) |
| `MIT-2.2` Set operations: union, intersection, complement, symmetric difference, Cartesian product, power set | 🟩 | [Tutorial 16: Sets as Sorted Lists — Set Operations: The Merge Pattern](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-16-sets-as-sorted-lists.html#set-operations-the-merge-pattern)<br/>[Tutorial 16: Sets as Sorted Lists — Sets in Practice](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-16-sets-as-sorted-lists.html#sets-in-practice)<br/>_used in:_ [Tutorial 17: Bringing It All Together — Problem 3: Sets of Solutions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-17-bringing-it-all-together.html#problem-3-sets-of-solutions) |
| `MIT-2.3` Venn diagrams for two and three sets | ⬜ | **Out of scope** — Venn diagrams. The set operations themselves are taught in Tutorial 16 and that is the part the students use. The diagram is a pen-and-paper convention that adds notation without adding understanding here. |
| `MIT-2.4` Truth tables: AND, NOT, OR, XOR | 🟨 | _used in:_ [Tutorial 3: Making Decisions — Boolean Operators: Combining Conditions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-03-making-decisions.html#boolean-operators-combining-conditions) |
| `MIT-2.5` De Morgan's Laws | 🟥 | — |

#### 3. Functions and Calculus

| Outcome | | Where |
|---|---|---|
| `MIT-3.1` The function and inverse function concept | 🟨 | _used in:_ [Tutorial 6: Finding Things — Functions as Input-Output Machines](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-06-finding-things.html#functions-as-input-output-machines) |
| `MIT-3.2` Graph linear, quadratic and cubic functions; solve from a graph | 🟥 | — |
| `MIT-3.3` Define and graph the trigonometric functions | 🟥 | — |
| `MIT-3.4` Complete the square to find roots and vertex | 🟥 | — |
| `MIT-3.5` The limit of a function | 🟥 | — |
| `MIT-3.6` The derivative as a limit, a tangent slope, a rate of change | 🟥 | — |
| `MIT-3.7` Sum, product, quotient and chain rules | 🟥 | **Not written. When it is:** the sum rule and the product rule only, not the chain rule and the quotient rule |

#### 4. Geometry and Trigonometry

| Outcome | | Where |
|---|---|---|
| `MIT-4.1` Linear equations in the form ax + by + c = 0 | 🟥 | — |
| `MIT-4.2` Slope; parallel and perpendicular lines | 🟥 | — |
| `MIT-4.3` Midpoint and length of a line segment | 🟥 | — |
| `MIT-4.4` The Pythagorean theorem | 🟥 | — |
| `MIT-4.5` Degree and radian measure | 🟥 | — |
| `MIT-4.6` sin, cos, tan and the unit circle: amplitude, phase, period | 🟥 | — |
| `MIT-4.7` Trigonometric ratios in surd form | ⬜ | **Out of scope** — Trigonometric ratios in surd form. Exact values from the special triangles are a hand-calculation skill; the trigonometry we want is the graphing and the two rules, both of which work in decimals. |
| `MIT-4.8` Triangle area as one half a b sin theta | 🟥 | — |
| `MIT-4.9` Practical right-triangle trigonometry | 🟥 | — |
| `MIT-4.10` The Sine Rule and the Cosine Rule | 🟥 | — |

#### 5. Probability and Statistics

| Outcome | | Where |
|---|---|---|
| `MIT-5.1` List the outcomes of an experiment | 🟩 | [Tutorial 10: What Are the Chances? — Basic Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-10-what-are-the-chances.html#basic-probability) |
| `MIT-5.2` The fundamental principle of counting | 🟩 | [Tutorial 9: Counting Carefully — A Practical Application: Password Strength](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-09-counting-carefully.html#a-practical-application-password-strength) |
| `MIT-5.3` Arrangements of n objects (n factorial) | 🟩 | [Tutorial 9: Counting Carefully — Factorials: The Foundation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-09-counting-carefully.html#factorials-the-foundation) |
| `MIT-5.4` Permutations P(n, r) | 🟩 | [Tutorial 9: Counting Carefully — Permutations: Order Matters](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-09-counting-carefully.html#permutations-order-matters) |
| `MIT-5.5` Combinations C(n, r) | 🟩 | [Tutorial 9: Counting Carefully — Combinations: Order Does Not Matter](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-09-counting-carefully.html#combinations-order-does-not-matter) |
| `MIT-5.6` Probability as a scale from 0 to 1 | 🟩 | [Tutorial 10: What Are the Chances? — Basic Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-10-what-are-the-chances.html#basic-probability) |
| `MIT-5.7` Probability from equally likely outcomes | 🟩 | [Tutorial 10: What Are the Chances? — Basic Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-10-what-are-the-chances.html#basic-probability)<br/>_used in:_ [Tutorial 10: What Are the Chances? — Simulation: Testing Probability with Code](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-10-what-are-the-chances.html#simulation-testing-probability-with-code) |
| `MIT-5.8` Compound probability: independent and mutually exclusive events | 🟩 | [Tutorial 10: What Are the Chances? — Compound Events](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-10-what-are-the-chances.html#compound-events)<br/>[Tutorial 10: What Are the Chances? — Conditional Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-10-what-are-the-chances.html#conditional-probability) |
| `MIT-5.9` Data types: nominal, ordinal, discrete, continuous | 🟩 | [Tutorial 11: Making Sense of Data — Data Types](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-11-making-sense-of-data.html#data-types) |
| `MIT-5.10` Effectiveness of displays: pie, histogram, stem-and-leaf | 🟩 | [Tutorial 11: Making Sense of Data — Visualisation with matplotlib](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-11-making-sense-of-data.html#visualisation-with-matplotlib)<br/>[Tutorial 12: Pictures Worth Numbers — Why Visualise?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-12-pictures-worth-numbers.html#why-visualise)<br/>[Tutorial 12: Pictures Worth Numbers — Choosing the Right Chart](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-12-pictures-worth-numbers.html#choosing-the-right-chart)<br/>[Tutorial 12: Pictures Worth Numbers — Good Practices for Visualisation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-12-pictures-worth-numbers.html#good-practices-for-visualisation) |
| `MIT-5.11` Frequency tables and histograms | 🟩 | [Tutorial 11: Making Sense of Data — Frequency Distributions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-11-making-sense-of-data.html#frequency-distributions) |
| `MIT-5.12` Mean, median, mode, range, standard deviation | 🟩 | [Tutorial 11: Making Sense of Data — Measures of Central Tendency](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-11-making-sense-of-data.html#measures-of-central-tendency)<br/>[Tutorial 11: Making Sense of Data — Measures of Spread](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-11-making-sense-of-data.html#measures-of-spread)<br/>[Tutorial 12: Pictures Worth Numbers — Combining Statistics and Visualisation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-12-pictures-worth-numbers.html#combining-statistics-and-visualisation) |
| `MIT-5.13` Merits and limitations of the averages with skewed data | 🟩 | [Tutorial 11: Making Sense of Data — A note on limitations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-11-making-sense-of-data.html#a-note-on-limitations) |

#### 6. Algorithms and Computations

| Outcome | | Where |
|---|---|---|
| `MIT-6.1` The concept of an algorithm | 🟩 | [Tutorial 1: First Steps — What is an Algorithm?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-01-first-steps.html#what-is-an-algorithm) |
| `MIT-6.2` An algorithm as a function on a domain of inputs | 🟩 | [Tutorial 5: Lists and Sequences — Mathematical Sequences as Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#mathematical-sequences-as-functions)<br/>[Tutorial 6: Finding Things — Functions as Input-Output Machines](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-06-finding-things.html#functions-as-input-output-machines) |
| `MIT-6.3` Manipulate lists and arrays, including addition and multiplication | 🟩 | [Tutorial 5: Lists and Sequences — Lists: Ordered Collections](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#lists-ordered-collections)<br/>[Tutorial 5: Lists and Sequences — Building Lists with Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#building-lists-with-loops)<br/>[Tutorial 5: Lists and Sequences — The Dot Product: Lists Meet Arithmetic](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#the-dot-product-lists-meet-arithmetic) |
| `MIT-6.4` Index, sigma and pi notation | 🟩 | [Tutorial 4: Repeating Yourself — Sigma Notation: Mathematics Meets Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-04-repeating-yourself.html#sigma-notation-mathematics-meets-loops) |
| `MIT-6.5` Lists and arrays applied to simple problems | 🟩 | [Tutorial 5: Lists and Sequences — Looping Over Lists](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#looping-over-lists) |
| `MIT-6.6` Divide and conquer | 🟩 | [Tutorial 6: Finding Things — Divide and Conquer](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-06-finding-things.html#divide-and-conquer) |
| `MIT-6.7` Iterate over a one-dimensional array by index | 🟩 | [Tutorial 4: Repeating Yourself — For Loops: When You Know How Many Times](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-04-repeating-yourself.html#for-loops-when-you-know-how-many-times)<br/>[Tutorial 4: Repeating Yourself — Building Up Gradually: Counting with Conditions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-04-repeating-yourself.html#building-up-gradually-counting-with-conditions)<br/>[Tutorial 5: Lists and Sequences — Building Lists with Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#building-lists-with-loops)<br/>[Tutorial 5: Lists and Sequences — Looping Over Lists](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#looping-over-lists) |
| `MIT-6.8` Recursion; linear and binary search; bubble, insertion, selection and shell sort | 🟩 | [Tutorial 6: Finding Things — Linear Search: The Straightforward Approach](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-06-finding-things.html#linear-search-the-straightforward-approach)<br/>[Tutorial 6: Finding Things — Binary Search: The Power of Sorted Data](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-06-finding-things.html#binary-search-the-power-of-sorted-data)<br/>[Tutorial 7: Putting Things in Order — Bubble Sort: Let Things Rise](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-07-putting-things-in-order.html#bubble-sort-let-things-rise)<br/>[Tutorial 7: Putting Things in Order — Insertion Sort: Sort Like You Sort Cards](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-07-putting-things-in-order.html#insertion-sort-sort-like-you-sort-cards)<br/>[Tutorial 7: Putting Things in Order — Selection Sort: Find the Smallest](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-07-putting-things-in-order.html#selection-sort-find-the-smallest)<br/>[Tutorial 7: Putting Things in Order — Comparing Our Sorts](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-07-putting-things-in-order.html#comparing-our-sorts)<br/>_used in:_ [Tutorial 7: Putting Things in Order — Optional Challenges](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-07-putting-things-in-order.html#optional-challenges) |

### Programming and Design Principles 5N2927

| Outcome | | Where |
|---|---|---|
| `PDP-LO1` The history of computer programming | 🟥 | — |
| `PDP-LO2` Algorithms and their real-world application | 🟩 | [Tutorial 1: First Steps — What is an Algorithm?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-01-first-steps.html#what-is-an-algorithm) |
| `PDP-LO3` Differentiate programming languages by their characteristics | 🟥 | — |
| `PDP-LO4` Procedural syntax: storage, expressions, statements, input and output, keywords, operators | 🟩 | [Tutorial 1: First Steps — A Few More Things Python Can Do](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-01-first-steps.html#a-few-more-things-python-can-do)<br/>[Tutorial 2: Storing and Computing — Variables: Giving Names to Things](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-02-storing-and-computing.html#variables-giving-names-to-things)<br/>[Tutorial 2: Storing and Computing — Data Types: Different Kinds of Information](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-02-storing-and-computing.html#data-types-different-kinds-of-information)<br/>[Tutorial 2: Storing and Computing — Type Conversion](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-02-storing-and-computing.html#type-conversion) |
| `PDP-LO5` The sequential nature of problem solving | 🟩 | [Tutorial 1: First Steps — Pseudocode: Planning Before Coding](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-01-first-steps.html#pseudocode-planning-before-coding) |
| `PDP-LO6` Structured design: pseudocode, storage, selection and iteration | 🟩 | [Tutorial 1: First Steps — Pseudocode: Planning Before Coding](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-01-first-steps.html#pseudocode-planning-before-coding)<br/>[Tutorial 3: Making Decisions — Comparisons: True or False?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-03-making-decisions.html#comparisons-true-or-false)<br/>[Tutorial 3: Making Decisions — If Statements: Choosing a Path](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-03-making-decisions.html#if-statements-choosing-a-path)<br/>[Tutorial 3: Making Decisions — If-Else: Two Paths](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-03-making-decisions.html#if-else-two-paths)<br/>[Tutorial 3: Making Decisions — Elif: Multiple Paths](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-03-making-decisions.html#elif-multiple-paths)<br/>[Tutorial 3: Making Decisions — Boolean Operators: Combining Conditions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-03-making-decisions.html#boolean-operators-combining-conditions)<br/>[Tutorial 4: Repeating Yourself — While Loops: Repeat Until Done](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-04-repeating-yourself.html#while-loops-repeat-until-done)<br/>[Tutorial 4: Repeating Yourself — For Loops: When You Know How Many Times](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-04-repeating-yourself.html#for-loops-when-you-know-how-many-times)<br/>[Tutorial 4: Repeating Yourself — Nested Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-04-repeating-yourself.html#nested-loops) |
| `PDP-LO7` Develop documented programs for familiar and unfamiliar problems | 🟩 | [Tutorial 2: Storing and Computing — Putting It Together: A Small Program](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-02-storing-and-computing.html#putting-it-together-a-small-program)<br/>[Tutorial 8: Building Reusable Tools — Handling Edge Cases](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-08-building-reusable-tools.html#handling-edge-cases) |
| `PDP-LO8` Modularisation: functions, procedures, scope, parameter passing | 🟩 | [Tutorial 5: Lists and Sequences — Functions: Reusable Algorithms](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-05-lists-and-sequences.html#functions-reusable-algorithms)<br/>[Tutorial 6: Finding Things — Scope: Where Variables Live](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-06-finding-things.html#scope-where-variables-live)<br/>[Tutorial 8: Building Reusable Tools — What Makes a Good Function?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-08-building-reusable-tools.html#what-makes-a-good-function)<br/>[Tutorial 8: Building Reusable Tools — Functions Calling Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-08-building-reusable-tools.html#functions-calling-functions)<br/>[Tutorial 8: Building Reusable Tools — Variable Scope Revisited](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-08-building-reusable-tools.html#variable-scope-revisited)<br/>[Tutorial 12: Pictures Worth Numbers — Writing Reusable Plotting Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-12-pictures-worth-numbers.html#writing-reusable-plotting-functions) |
| `PDP-LO9` Interpret compiler and linker messages and react appropriately | 🟥 | — |
| `PDP-LO10` The testing process: structured walkthroughs and debugging tools | 🟩 | [Tutorial 8: Building Reusable Tools — Testing as a Habit](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-08-building-reusable-tools.html#testing-as-a-habit)<br/>[Tutorial 17: Bringing It All Together — Problem 4: Building and Verifying](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-17-bringing-it-all-together.html#problem-4-building-and-verifying) |
| `PDP-LO11` Coding standards: comments, indentation, variable naming | 🟩 | [Tutorial 2: Storing and Computing — Variables: Giving Names to Things](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-02-storing-and-computing.html#variables-giving-names-to-things)<br/>[Tutorial 8: Building Reusable Tools — What Makes a Good Function?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-08-building-reusable-tools.html#what-makes-a-good-function)<br/>[Interlude: Looking Back Before Moving Forward — Part 1: Reading Your Own Code](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-interlude-critique-and-reflection.html#part-1-reading-your-own-code)<br/>[Interlude: Looking Back Before Moving Forward — Part 2: Reading Someone Else's Code](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/tutorial-interlude-critique-and-reflection.html#part-2-reading-someone-elses-code) |
| `PDP-LO12` Team programming: design, develop, release and review over time, in teams of three to five | 🟥 | — |

## Scope questions still open

Counted as gaps until they are settled, which is the safer default.

- **MIT-4.4, MIT-4.9 — Pythagoras and practical right-triangle trigonometry** — "Trigonometry beyond graphing and the Sine and Cosine Rules" could be read as excluding SOH-CAH-TOA as well. It is the usual way in to the subject and the students will have met it before, so it may be worth keeping as the bridge into the two rules rather than dropping.
- **MIT-4.5, MIT-4.6 — radians and the unit circle** — Graphing sine and cosine needs an x-axis, and radians are what that axis is normally in. Keep radians as the minimum needed for the graphs, or teach the graphs in degrees and drop radians entirely?
- **MIT-4.1, MIT-4.2, MIT-4.3 — coordinate geometry** — Not mentioned either way. Slope and midpoint are cheap to teach, sit naturally beside graphing straight lines in the polynomial tutorial, and are the one part of Section 4 that the programming half of the course can use directly. Keep?
