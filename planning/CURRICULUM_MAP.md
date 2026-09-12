# Curriculum map

**Generated — do not edit by hand.** `python3 dev/curriculum_map.py`
rebuilds it from three files, and CI fails if this one is out of date:

- `planning/curriculum/outcomes.yaml` — every learning outcome in the
  QQI module descriptors.
- each tutorial's `covers:` frontmatter — which outcome each section
  teaches, and which it only uses.
- `planning/curriculum/out-of-scope.yaml` — what we have decided not to
  teach, so a decision stops looking like a gap.

Every link below goes to the section of the live site that does the work,
so this doubles as a way of finding where anything is taught.

## Where we stand

**115 of 116** outcomes are in place.

- 🟩 **113 taught** — a tutorial section teaches it.
- 🟦 **2 taught in part** — deliberately narrowed, and the narrowed version is written.
- 🟨 **0 used but not taught** — students meet it in passing without it ever being the subject. These are the quiet gaps: they look covered from a distance.
- 🟥 **1 not covered** — nothing in dewlab touches it.

**1 of the 1 outcomes still to write have no proposal**: `WA-LO12`. These are the ones nobody has decided how to teach yet.

### By strand

| Strand | 🟩 Taught | 🟦 Part, by choice | 🟨 Used only | 🟥 Not covered | ⬜ Out of scope |
|---|---:|---:|---:|---:|---:|
| **algebra** | 7 | 1 | 0 | 0 | 0 |
| **algorithms** | 9 | 0 | 0 | 0 | 0 |
| **calculus** | 2 | 1 | 0 | 0 | 0 |
| **complexity** | 2 | 0 | 0 | 0 | 0 |
| **css** | 1 | 0 | 0 | 0 | 0 |
| **data-entry** | 1 | 0 | 0 | 0 | 0 |
| **data-import** | 1 | 0 | 0 | 0 | 0 |
| **data-structures** | 1 | 0 | 0 | 0 | 0 |
| **database-concepts** | 2 | 0 | 0 | 0 | 0 |
| **design** | 2 | 0 | 0 | 0 | 0 |
| **design-principles** | 3 | 0 | 0 | 0 | 0 |
| **functions** | 3 | 0 | 0 | 0 | 0 |
| **geometry** | 6 | 0 | 0 | 0 | 0 |
| **html-tags** | 2 | 0 | 0 | 0 | 0 |
| **independence** | 1 | 0 | 0 | 0 | 0 |
| **linear-algebra** | 1 | 0 | 0 | 0 | 0 |
| **logic** | 2 | 0 | 0 | 0 | 0 |
| **modelling** | 2 | 0 | 0 | 0 | 0 |
| **number** | 2 | 0 | 0 | 0 | 0 |
| **oop** | 4 | 0 | 0 | 0 | 0 |
| **probability** | 10 | 0 | 0 | 0 | 0 |
| **problem-solving** | 3 | 0 | 0 | 0 | 0 |
| **process** | 2 | 0 | 0 | 0 | 0 |
| **programming** | 18 | 0 | 0 | 0 | 0 |
| **querying** | 3 | 0 | 0 | 0 | 0 |
| **reflection** | 2 | 0 | 0 | 0 | 0 |
| **reporting** | 1 | 0 | 0 | 0 | 0 |
| **sets** | 3 | 0 | 0 | 0 | 0 |
| **simulation** | 1 | 0 | 0 | 0 | 0 |
| **statistics** | 5 | 0 | 0 | 0 | 0 |
| **testing** | 1 | 0 | 0 | 0 | 0 |
| **tooling** | 2 | 0 | 0 | 1 | 0 |
| **trigonometry** | 7 | 0 | 0 | 0 | 0 |
| **web-history** | 1 | 0 | 0 | 0 | 0 |

```mermaid
graph LR
  algebra["algebra<br/>8 of 8 in place"]
  algorithms["algorithms<br/>9 of 9 in place"]
  calculus["calculus<br/>3 of 3 in place"]
  complexity["complexity<br/>2 of 2 in place"]
  css["css<br/>1 of 1 in place"]
  data_entry["data-entry<br/>1 of 1 in place"]
  data_import["data-import<br/>1 of 1 in place"]
  data_structures["data-structures<br/>1 of 1 in place"]
  database_concepts["database-concepts<br/>2 of 2 in place"]
  design["design<br/>2 of 2 in place"]
  design_principles["design-principles<br/>3 of 3 in place"]
  functions["functions<br/>3 of 3 in place"]
  geometry["geometry<br/>6 of 6 in place"]
  html_tags["html-tags<br/>2 of 2 in place"]
  independence["independence<br/>1 of 1 in place"]
  linear_algebra["linear-algebra<br/>1 of 1 in place"]
  logic["logic<br/>2 of 2 in place"]
  modelling["modelling<br/>2 of 2 in place"]
  number["number<br/>2 of 2 in place"]
  oop["oop<br/>4 of 4 in place"]
  probability["probability<br/>10 of 10 in place"]
  problem_solving["problem-solving<br/>3 of 3 in place"]
  process["process<br/>2 of 2 in place"]
  programming["programming<br/>18 of 18 in place"]
  querying["querying<br/>3 of 3 in place"]
  reflection["reflection<br/>2 of 2 in place"]
  reporting["reporting<br/>1 of 1 in place"]
  sets["sets<br/>3 of 3 in place"]
  simulation["simulation<br/>1 of 1 in place"]
  statistics["statistics<br/>5 of 5 in place"]
  testing["testing<br/>1 of 1 in place"]
  tooling["tooling<br/>2 of 3 in place"]
  trigonometry["trigonometry<br/>7 of 7 in place"]
  web_history["web-history<br/>1 of 1 in place"]

  classDef full fill:#edf7f0,stroke:#1f6b3f,color:#1f6b3f;
  classDef part fill:#fdf6ec,stroke:#b5651d,color:#7a4310;
  classDef none fill:#fdf0ef,stroke:#9b2226,color:#9b2226;
  class algebra,algorithms,calculus,complexity,css,data_entry,data_import,data_structures,database_concepts,design,design_principles,functions,geometry,html_tags,independence,linear_algebra,logic,modelling,number,oop,probability,problem_solving,process,programming,querying,reflection,reporting,sets,simulation,statistics,testing,trigonometry,web_history full;
  class tooling part;
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
  T3["3. How We Got Here"]
  T4["4. Making Decisions"]
  T5["5. When It Goes Wrong"]
  T6["6. Repeating Yourself"]
  T7["7. Lists and Sequences"]
  T8["8. Finding Things"]
  T9["9. Putting Things in Order"]
  T10["10. Building Reusable Tools"]
  T11["11. Counting Carefully"]
  T12["12. What Are the Chances?"]
  T13["13. Making Sense of Data"]
  T14["14. Pictures Worth Numbers"]
  T15["15. Sets as Sorted Lists"]
  T16["16. Logic and Truth"]
  T17["17. Drawing Sets"]
  T18["18. Numbers and Their Families"]
  T19["19. Expressions Come Alive"]
  T20["20. Rearranging Formulae"]
  T21["21. Cracking Equations"]
  T22["22. When There Is No Answer"]
  T23["23. Drawing Functions"]
  T24["24. Parabolas"]
  T25["25. Lines and Distances"]
  T26["26. The Unit Circle"]
  T27["27. Sine and Cosine Waves"]
  T28["28. Solving Triangles"]
  T29["29. Approaching a Limit"]
  T30["30. Rates of Change"]
  T31["31. Bringing It All Together"]

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
  T18 --> T19
  T19 --> T20
  T20 --> T21
  T21 --> T22
  T22 --> T23
  T23 --> T24
  T24 --> T25
  T25 --> T26
  T26 --> T27
  T27 --> T28
  T28 --> T29
  T29 --> T30
  T30 --> T31

  T11 -.->|builds on| T6
  T15 -.->|builds on| T8
  T15 -.->|builds on| T9
  T16 -.->|builds on| T4
  T17 -.->|builds on| T15
  T20 -.->|builds on| T2
  T21 -.->|builds on| T19
  T22 -.->|builds on| T18
  T23 -.->|builds on| T10
  T23 -.->|builds on| T14
  T23 -.->|builds on| T19
  T23 -.->|builds on| T21
  T24 -.->|builds on| T21
  T24 -.->|builds on| T22
  T25 -.->|builds on| T13
  T25 -.->|builds on| T14
  T25 -.->|builds on| T23
  T27 -.->|builds on| T23
  T27 -.->|builds on| T24
  T27 -.->|builds on| T25
  T28 -.->|builds on| T23
  T28 -.->|builds on| T25
  T28 -.->|builds on| T26
  T29 -.->|builds on| T2
  T30 -.->|builds on| T24
  T30 -.->|builds on| T25
  T31 -.->|builds on| T1
  T31 -.->|builds on| T15
  T31 -.->|builds on| T18
  T31 -.->|builds on| T19
  T31 -.->|builds on| T21
```

## What is missing, and where it would go

Dashed boxes are proposed. Placement is argued in
`planning/curriculum/proposed.yaml` and each has an outline in
`planning/outlines/`.

```mermaid
graph TD
  T1["1. First Steps"]
  T2["2. Storing and Computing"]
  T3["3. How We Got Here"]
  T4["4. Making Decisions"]
  T5["5. When It Goes Wrong"]
  T6["6. Repeating Yourself"]
  T7["7. Lists and Sequences"]
  T8["8. Finding Things"]
  T9["9. Putting Things in Order"]
  T10["10. Building Reusable Tools"]
  T11["11. Counting Carefully"]
  T12["12. What Are the Chances?"]
  T13["13. Making Sense of Data"]
  T14["14. Pictures Worth Numbers"]
  T15["15. Sets as Sorted Lists"]
  T16["16. Logic and Truth"]
  T17["17. Drawing Sets"]
  T18["18. Numbers and Their Families"]
  T19["19. Expressions Come Alive"]
  T20["20. Rearranging Formulae"]
  T21["21. Cracking Equations"]
  T22["22. When There Is No Answer"]
  T23["23. Drawing Functions"]
  T24["24. Parabolas"]
  T25["25. Lines and Distances"]
  T26["26. The Unit Circle"]
  T27["27. Sine and Cosine Waves"]
  T28["28. Solving Triangles"]
  T29["29. Approaching a Limit"]
  T30["30. Rates of Change"]
  T31["31. Bringing It All Together"]

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
  T18 --> T19
  T19 --> T20
  T20 --> T21
  T21 --> T22
  T22 --> T23
  T23 --> T24
  T24 --> T25
  T25 --> T26
  T26 --> T27
  T27 --> T28
  T28 --> T29
  T29 --> T30
  T30 --> T31


  classDef new fill:#fdf6ec,stroke:#b5651d,color:#7a4310,stroke-dasharray:4 3;
  class  new;
```

| Proposed | Goes after | Closes | Size |
|---|---|---|---|

## Every outcome

### Maths for Information Technology 5N18396

#### 1. Basic Arithmetic and Algebra

| Outcome | | Where |
|---|---|---|
| `MIT-1.1` Operations in N, Z, Q, R; powers (the syllabus says indices) and logarithms | 🟩 | [Making Decisions — Classifying Numbers: A Mathematical Application](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-decisions.html#classifying-numbers-a-mathematical-application)<br/>[Numbers and Their Families — Powers and Their Rules](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/numbers-and-their-families.html#powers-and-their-rules)<br/>[Numbers and Their Families — Logarithms: The Inverse of Powers](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/numbers-and-their-families.html#logarithms-the-inverse-of-powers) |
| `MIT-1.2` Area and perimeter: square, rectangle, triangle, circle | 🟩 | [Numbers and Their Families — Practical Geometry: Formulas as Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/numbers-and-their-families.html#practical-geometry-formulas-as-functions) |
| `MIT-1.3` Volume and surface area: cube, cylinder, cone, sphere | 🟩 | [Numbers and Their Families — Practical Geometry: Formulas as Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/numbers-and-their-families.html#practical-geometry-formulas-as-functions) |
| `MIT-1.4` Binary and hexadecimal arithmetic and conversion | 🟩 | [Storing and Computing — Number Systems: How Computers Count](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/storing-and-computing.html#number-systems-how-computers-count)<br/>_used in:_ [How We Got Here — The Only Language the Machine Understands](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#the-only-language-the-machine-understands)<br/>_used in:_ [How We Got Here — Assembly, and Why Hexadecimal Exists](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#assembly-and-why-hexadecimal-exists) |
| `MIT-1.5` Distinguish an expression from an equation | 🟦 | [Expressions Come Alive — Expressions versus Equations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/expressions-come-alive.html#expressions-versus-equations)<br/>**Narrowed:** not the formal expression-versus-equation distinction as an assessed item |
| `MIT-1.6` Evaluate, expand and simplify expressions | 🟩 | [Expressions Come Alive — Representing Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/expressions-come-alive.html#representing-polynomials)<br/>[Expressions Come Alive — Evaluating Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/expressions-come-alive.html#evaluating-polynomials)<br/>[Expressions Come Alive — Displaying Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/expressions-come-alive.html#displaying-polynomials)<br/>[Expressions Come Alive — Adding Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/expressions-come-alive.html#adding-polynomials)<br/>[Expressions Come Alive — Subtracting and Scaling](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/expressions-come-alive.html#subtracting-and-scaling)<br/>_used in:_ [Bringing It All Together — Problem 1: The Polynomial Workshop](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/bringing-it-all-together.html#problem-1-the-polynomial-workshop) |
| `MIT-1.7` Transpose formulae; operate on rational algebraic expressions | 🟩 | [Rearranging Formulae — The Same Formula, Five Ways](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rearranging-formulae.html#the-same-formula-five-ways)<br/>[Rearranging Formulae — The Moves](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rearranging-formulae.html#the-moves)<br/>[Rearranging Formulae — When the Unknown Is Underneath](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rearranging-formulae.html#when-the-unknown-is-underneath)<br/>[Rearranging Formulae — Checking Yourself](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rearranging-formulae.html#checking-yourself)<br/>_used in:_ [Cracking Equations — Solving Linear Equations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/cracking-equations.html#solving-linear-equations) |
| `MIT-1.8` Multiply linear expressions into quadratics and cubics | 🟩 | [Expressions Come Alive — Multiplying Polynomials](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/expressions-come-alive.html#multiplying-polynomials)<br/>_used in:_ [Bringing It All Together — Problem 1: The Polynomial Workshop](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/bringing-it-all-together.html#problem-1-the-polynomial-workshop) |
| `MIT-1.9` Factor quadratics by inspection and solve them | 🟩 | [Cracking Equations — Factorisation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/cracking-equations.html#factorisation) |
| `MIT-1.10` Solve quadratics, including complex roots | 🟩 | [When There Is No Answer — The Cliff Edge](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/complex-roots.html#the-cliff-edge)<br/>[When There Is No Answer — Inventing a Number](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/complex-roots.html#inventing-a-number)<br/>[When There Is No Answer — Roots That Are Not Real](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/complex-roots.html#roots-that-are-not-real)<br/>[When There Is No Answer — They Come in Pairs](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/complex-roots.html#they-come-in-pairs)<br/>_used in:_ [Cracking Equations — The Quadratic Formula](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/cracking-equations.html#the-quadratic-formula) |
| `MIT-1.11` Solve linear inequalities | 🟩 | [Cracking Equations — Solving Inequalities](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/cracking-equations.html#solving-inequalities) |
| `MIT-1.12` Simultaneous equations in two and three unknowns | 🟩 | [Cracking Equations — Simultaneous Equations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/cracking-equations.html#simultaneous-equations)<br/>_used in:_ [Solving Systems — Three Unknowns, Row by Row](https://deweydex.github.io/dewlab/tutorials/computational-methods/solving-systems.html#three-unknowns-row-by-row)<br/>_used in:_ [Bringing It All Together — Problem 2: Where Do They Meet?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/bringing-it-all-together.html#problem-2-where-do-they-meet) |

#### 2. Set Theory and Boolean Logic

| Outcome | | Where |
|---|---|---|
| `MIT-2.1` Set language: N, Z, Q, R, C, the empty set; finite, infinite, cardinality | 🟩 | [Numbers and Their Families — The Number Domains](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/numbers-and-their-families.html#the-number-domains)<br/>[Sets as Sorted Lists — Making a Set](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sets-as-sorted-lists.html#making-a-set)<br/>[Sets as Sorted Lists — Membership Testing](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sets-as-sorted-lists.html#membership-testing)<br/>[Sets as Sorted Lists — Set Language and Notation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sets-as-sorted-lists.html#set-language-and-notation)<br/>_used in:_ [When There Is No Answer — Inventing a Number](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/complex-roots.html#inventing-a-number) |
| `MIT-2.2` Set operations: union, intersection, complement, symmetric difference, Cartesian product, power set | 🟩 | [Sets as Sorted Lists — Set Operations: The Merge Pattern](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sets-as-sorted-lists.html#set-operations-the-merge-pattern)<br/>[Sets as Sorted Lists — Sets in Practice](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sets-as-sorted-lists.html#sets-in-practice)<br/>_used in:_ [Bringing It All Together — Problem 3: Sets of Solutions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/bringing-it-all-together.html#problem-3-sets-of-solutions) |
| `MIT-2.3` Venn diagrams for two and three sets | 🟩 | [Drawing Sets — Two Circles, from Real Sets](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/venn-diagrams.html#two-circles-from-real-sets)<br/>[Drawing Sets — The Regions Have Names You Already Know](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/venn-diagrams.html#the-regions-have-names-you-already-know)<br/>[Drawing Sets — Three Sets, Which Is Where It Earns Its Place](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/venn-diagrams.html#three-sets-which-is-where-it-earns-its-place)<br/>[Drawing Sets — The Same Laws, in a Different Notation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/venn-diagrams.html#the-same-laws-in-a-different-notation) |
| `MIT-2.4` Truth tables: AND, NOT, OR, XOR | 🟩 | [Logic and Truth — Every Possible Case](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/logic-and-truth.html#every-possible-case)<br/>[Logic and Truth — Exclusive Or](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/logic-and-truth.html#exclusive-or)<br/>_used in:_ [Making Decisions — Boolean Operators: Combining Conditions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-decisions.html#boolean-operators-combining-conditions) |
| `MIT-2.5` De Morgan's Laws | 🟩 | [Logic and Truth — De Morgan's Laws](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/logic-and-truth.html#de-morgans-laws)<br/>[Logic and Truth — Where You Have Already Used This](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/logic-and-truth.html#where-you-have-already-used-this)<br/>[Logic and Truth — The Same Shapes, on Sets](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/logic-and-truth.html#the-same-shapes-on-sets) |

#### 3. Functions and Calculus

| Outcome | | Where |
|---|---|---|
| `MIT-3.1` The function and inverse function concept | 🟩 | [Drawing Functions — A Function Is a Machine](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/drawing-functions.html#a-function-is-a-machine)<br/>[Drawing Functions — Undoing a Function](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/drawing-functions.html#undoing-a-function)<br/>_used in:_ [Finding Things — Functions as Input-Output Machines](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#functions-as-input-output-machines) |
| `MIT-3.2` Graph linear, quadratic and cubic functions; solve from a graph | 🟩 | [Drawing Functions — A Machine Has a Picture](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/drawing-functions.html#a-machine-has-a-picture)<br/>[Drawing Functions — Straight Lines](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/drawing-functions.html#straight-lines)<br/>[Drawing Functions — Curves That Bend](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/drawing-functions.html#curves-that-bend)<br/>[Drawing Functions — Reading an Answer Off the Picture](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/drawing-functions.html#reading-an-answer-off-the-picture)<br/>_used in:_ [What a Matrix Does to a Picture — Where Do the Corners Go?](https://deweydex.github.io/dewlab/tutorials/computational-methods/what-a-matrix-does-to-a-picture.html#where-do-the-corners-go) |
| `MIT-3.3` Define and graph the trigonometric functions | 🟩 | [Sine and Cosine Waves — Unrolling the Circle](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sine-and-cosine-waves.html#unrolling-the-circle)<br/>[Sine and Cosine Waves — Why It Repeats](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sine-and-cosine-waves.html#why-it-repeats)<br/>[Sine and Cosine Waves — The Four Numbers](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sine-and-cosine-waves.html#the-four-numbers)<br/>[Sine and Cosine Waves — Where a Wave Comes From](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/sine-and-cosine-waves.html#where-a-wave-comes-from) |
| `MIT-3.4` Complete the square to find roots and vertex | 🟩 | [Parabolas — Every Quadratic Is the Same Curve](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/parabolas.html#every-quadratic-is-the-same-curve)<br/>[Parabolas — The Form That Tells You Where the Bottom Is](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/parabolas.html#the-form-that-tells-you-where-the-bottom-is)<br/>[Parabolas — Doing the Rearrangement](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/parabolas.html#doing-the-rearrangement)<br/>[Parabolas — Roots from the Same Form](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/parabolas.html#roots-from-the-same-form) |
| `MIT-3.5` The limit of a function | 🟩 | [Approaching a Limit — A Hole in a Line](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/approaching-a-limit.html#a-hole-in-a-line)<br/>[Approaching a Limit — Getting Closer Without Arriving](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/approaching-a-limit.html#getting-closer-without-arriving)<br/>[Approaching a Limit — When There Is No Limit](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/approaching-a-limit.html#when-there-is-no-limit)<br/>[Approaching a Limit — Why Anybody Needs This](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/approaching-a-limit.html#why-anybody-needs-this) |
| `MIT-3.6` The derivative as a limit, a tangent slope, a rate of change | 🟩 | [Rates of Change — The Slope of Something That Is Not Straight](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rates-of-change.html#the-slope-of-something-that-is-not-straight)<br/>[Rates of Change — Three Descriptions of One Number](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rates-of-change.html#three-descriptions-of-one-number)<br/>[Rates of Change — The Derivative as a Function](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rates-of-change.html#the-derivative-as-a-function) |
| `MIT-3.7` Sum, product, quotient and chain rules | 🟦 | [Rates of Change — Rules Instead of Limits](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rates-of-change.html#rules-instead-of-limits)<br/>[Rates of Change — The Chain Rule](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/rates-of-change.html#the-chain-rule)<br/>**Narrowed:** not the quotient rule, and integration by parts |

#### 4. Geometry and Trigonometry

| Outcome | | Where |
|---|---|---|
| `MIT-4.1` Linear equations in the form ax + by + c = 0 | 🟩 | [Lines and Distances — A Line You Have Already Written](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lines-and-distances.html#a-line-you-have-already-written)<br/>[Lines and Distances — The Line That Breaks the Formula](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lines-and-distances.html#the-line-that-breaks-the-formula) |
| `MIT-4.2` Slope; parallel and perpendicular lines | 🟩 | [Lines and Distances — Slope, as How Fast Something Changes](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lines-and-distances.html#slope-as-how-fast-something-changes)<br/>[Lines and Distances — Parallel and Perpendicular](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lines-and-distances.html#parallel-and-perpendicular) |
| `MIT-4.3` Midpoint and length of a line segment | 🟩 | [Lines and Distances — Midpoint, Which Needs No Theory](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lines-and-distances.html#midpoint-which-needs-no-theory)<br/>[Lines and Distances — How Far Apart, and the Theorem That Answers It](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lines-and-distances.html#how-far-apart-and-the-theorem-that-answers-it) |
| `MIT-4.4` The Pythagorean theorem | 🟩 | [Lines and Distances — How Far Apart, and the Theorem That Answers It](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lines-and-distances.html#how-far-apart-and-the-theorem-that-answers-it) |
| `MIT-4.5` Degree and radian measure | 🟩 | [The Unit Circle — Measuring the Walk](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-unit-circle.html#measuring-the-walk) |
| `MIT-4.6` sin, cos, tan and the unit circle: amplitude, phase, period | 🟩 | [The Unit Circle — Going Round in Circles](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-unit-circle.html#going-round-in-circles)<br/>[The Unit Circle — The Names for Those Two Columns](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-unit-circle.html#the-names-for-those-two-columns)<br/>[The Unit Circle — Tangent, Which Is a Slope](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-unit-circle.html#tangent-which-is-a-slope) |
| `MIT-4.7` Trigonometric ratios in surd form | 🟩 | [The Unit Circle — The Landmark Points](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-unit-circle.html#the-landmark-points) |
| `MIT-4.8` Triangle area as one half a b sin theta | 🟩 | [Solving Triangles — Area, and the Height Nobody Drew](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/solving-triangles.html#area-and-the-height-nobody-drew) |
| `MIT-4.9` Practical right-triangle trigonometry | 🟩 | [Solving Triangles — When There Is a Right Angle](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/solving-triangles.html#when-there-is-a-right-angle)<br/>[Solving Triangles — Putting It Together](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/solving-triangles.html#putting-it-together) |
| `MIT-4.10` The Sine Rule and the Cosine Rule | 🟩 | [Solving Triangles — The Cosine Rule](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/solving-triangles.html#the-cosine-rule)<br/>[Solving Triangles — The Sine Rule, and Its Two Answers](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/solving-triangles.html#the-sine-rule-and-its-two-answers)<br/>[Solving Triangles — Putting It Together](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/solving-triangles.html#putting-it-together) |

#### 5. Probability and Statistics

| Outcome | | Where |
|---|---|---|
| `MIT-5.1` List the outcomes of an experiment | 🟩 | [What Are the Chances? — Basic Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/what-are-the-chances.html#basic-probability) |
| `MIT-5.2` The fundamental principle of counting | 🟩 | [Counting Carefully — A Practical Application: Password Strength](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/counting-carefully.html#a-practical-application-password-strength) |
| `MIT-5.3` Arrangements of n objects (n factorial) | 🟩 | [Counting Carefully — Factorials: The Foundation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/counting-carefully.html#factorials-the-foundation) |
| `MIT-5.4` Permutations P(n, r) | 🟩 | [Counting Carefully — Permutations: Order Matters](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/counting-carefully.html#permutations-order-matters) |
| `MIT-5.5` Combinations C(n, r) | 🟩 | [Counting Carefully — Combinations: Order Does Not Matter](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/counting-carefully.html#combinations-order-does-not-matter) |
| `MIT-5.6` Probability as a scale from 0 to 1 | 🟩 | [What Are the Chances? — Basic Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/what-are-the-chances.html#basic-probability) |
| `MIT-5.7` Probability from equally likely outcomes | 🟩 | [What Are the Chances? — Basic Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/what-are-the-chances.html#basic-probability)<br/>_used in:_ [What Are the Chances? — Simulation: Testing Probability with Code](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/what-are-the-chances.html#simulation-testing-probability-with-code) |
| `MIT-5.8` Compound probability: independent and mutually exclusive events | 🟩 | [What Are the Chances? — Compound Events](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/what-are-the-chances.html#compound-events)<br/>[What Are the Chances? — Conditional Probability](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/what-are-the-chances.html#conditional-probability) |
| `MIT-5.9` Data types: nominal, ordinal, discrete, continuous | 🟩 | [Making Sense of Data — Data Types](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-sense-of-data.html#data-types) |
| `MIT-5.10` Effectiveness of displays: pie, histogram, stem-and-leaf | 🟩 | [Making Sense of Data — Visualisation with matplotlib](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-sense-of-data.html#visualisation-with-matplotlib)<br/>[Pictures Worth Numbers — Why Visualise?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/pictures-worth-numbers.html#why-visualise)<br/>[Pictures Worth Numbers — Choosing the Right Chart](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/pictures-worth-numbers.html#choosing-the-right-chart)<br/>[Pictures Worth Numbers — Good Practices for Visualisation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/pictures-worth-numbers.html#good-practices-for-visualisation) |
| `MIT-5.11` Frequency tables and histograms | 🟩 | [Making Sense of Data — Frequency Distributions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-sense-of-data.html#frequency-distributions) |
| `MIT-5.12` Mean, median, mode, range, standard deviation | 🟩 | [Making Sense of Data — Measures of Central Tendency](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-sense-of-data.html#measures-of-central-tendency)<br/>[Making Sense of Data — Measures of Spread](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-sense-of-data.html#measures-of-spread)<br/>[Pictures Worth Numbers — Combining Statistics and Visualisation](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/pictures-worth-numbers.html#combining-statistics-and-visualisation) |
| `MIT-5.13` Merits and limitations of the averages with skewed data | 🟩 | [Making Sense of Data — A note on limitations](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-sense-of-data.html#a-note-on-limitations) |

#### 6. Algorithms and Computations

| Outcome | | Where |
|---|---|---|
| `MIT-6.1` The concept of an algorithm | 🟩 | [First Steps — What is an Algorithm?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/first-steps.html#what-is-an-algorithm) |
| `MIT-6.2` An algorithm as a function on a domain of inputs | 🟩 | [Finding Things — Functions as Input-Output Machines](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#functions-as-input-output-machines)<br/>[Lists and Sequences — Mathematical Sequences as Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#mathematical-sequences-as-functions) |
| `MIT-6.3` Manipulate lists and arrays, including addition and multiplication | 🟩 | [Lists and Sequences — Lists: Ordered Collections](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#lists-ordered-collections)<br/>[Lists and Sequences — Building Lists with Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#building-lists-with-loops)<br/>[Lists and Sequences — The Dot Product: Lists Meet Arithmetic](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#the-dot-product-lists-meet-arithmetic)<br/>_used in:_ [A Grid of Numbers — Nine Numbers That Draw a Picture](https://deweydex.github.io/dewlab/tutorials/computational-methods/grid-of-numbers.html#nine-numbers-that-draw-a-picture) |
| `MIT-6.4` Index, sigma and pi notation | 🟩 | [Repeating Yourself — Sigma Notation: Mathematics Meets Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/repeating-yourself.html#sigma-notation-mathematics-meets-loops) |
| `MIT-6.5` Lists and arrays applied to simple problems | 🟩 | [Lists and Sequences — Looping Over Lists](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#looping-over-lists) |
| `MIT-6.6` Divide and conquer | 🟩 | [Finding Things — Divide and Conquer](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#divide-and-conquer) |
| `MIT-6.7` Iterate over a one-dimensional array by index | 🟩 | [Lists and Sequences — Building Lists with Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#building-lists-with-loops)<br/>[Lists and Sequences — Looping Over Lists](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#looping-over-lists)<br/>[Repeating Yourself — For Loops: When You Know How Many Times](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/repeating-yourself.html#for-loops-when-you-know-how-many-times)<br/>[Repeating Yourself — Building Up Gradually: Counting with Conditions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/repeating-yourself.html#building-up-gradually-counting-with-conditions) |
| `MIT-6.8` Recursion; linear and binary search; bubble, insertion, selection and shell sort | 🟩 | [Finding Things — Linear Search: The Straightforward Approach](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#linear-search-the-straightforward-approach)<br/>[Finding Things — Binary Search: The Power of Sorted Data](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#binary-search-the-power-of-sorted-data)<br/>[Putting Things in Order — Bubble Sort: Let Things Rise](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/putting-things-in-order.html#bubble-sort-let-things-rise)<br/>[Putting Things in Order — Insertion Sort: Sort Like You Sort Cards](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/putting-things-in-order.html#insertion-sort-sort-like-you-sort-cards)<br/>[Putting Things in Order — Selection Sort: Find the Smallest](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/putting-things-in-order.html#selection-sort-find-the-smallest)<br/>[Putting Things in Order — Comparing Our Sorts](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/putting-things-in-order.html#comparing-our-sorts)<br/>_used in:_ [Putting Things in Order — Optional Challenges](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/putting-things-in-order.html#optional-challenges) |

### Programming and Design Principles 5N2927

| Outcome | | Where |
|---|---|---|
| `PDP-LO1` The history of computer programming | 🟩 | [How We Got Here — Before There Were Computers](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#before-there-were-computers)<br/>[How We Got Here — The Only Language the Machine Understands](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#the-only-language-the-machine-understands)<br/>[How We Got Here — Assembly, and Why Hexadecimal Exists](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#assembly-and-why-hexadecimal-exists)<br/>[How We Got Here — Languages People Can Read](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#languages-people-can-read) |
| `PDP-LO2` Algorithms and their real-world application | 🟩 | [First Steps — What is an Algorithm?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/first-steps.html#what-is-an-algorithm) |
| `PDP-LO3` Differentiate programming languages by their characteristics | 🟩 | [How We Got Here — Languages People Can Read](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#languages-people-can-read)<br/>[How We Got Here — The Same Problem, Four Ways](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/how-we-got-here.html#the-same-problem-four-ways) |
| `PDP-LO4` Procedural syntax: storage, expressions, statements, input and output, keywords, operators | 🟩 | [First Steps — A Few More Things Python Can Do](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/first-steps.html#a-few-more-things-python-can-do)<br/>[Storing and Computing — Variables: Giving Names to Things](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/storing-and-computing.html#variables-giving-names-to-things)<br/>[Storing and Computing — Data Types: Different Kinds of Information](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/storing-and-computing.html#data-types-different-kinds-of-information)<br/>[Storing and Computing — Type Conversion](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/storing-and-computing.html#type-conversion) |
| `PDP-LO5` The sequential nature of problem solving | 🟩 | [First Steps — Pseudocode: Planning Before Coding](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/first-steps.html#pseudocode-planning-before-coding) |
| `PDP-LO6` Structured design: pseudocode, storage, selection and iteration | 🟩 | [First Steps — Pseudocode: Planning Before Coding](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/first-steps.html#pseudocode-planning-before-coding)<br/>[Making Decisions — Comparisons: True or False?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-decisions.html#comparisons-true-or-false)<br/>[Making Decisions — If Statements: Choosing a Path](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-decisions.html#if-statements-choosing-a-path)<br/>[Making Decisions — If-Else: Two Paths](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-decisions.html#if-else-two-paths)<br/>[Making Decisions — Elif: Multiple Paths](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-decisions.html#elif-multiple-paths)<br/>[Making Decisions — Boolean Operators: Combining Conditions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/making-decisions.html#boolean-operators-combining-conditions)<br/>[Repeating Yourself — While Loops: Repeat Until Done](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/repeating-yourself.html#while-loops-repeat-until-done)<br/>[Repeating Yourself — For Loops: When You Know How Many Times](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/repeating-yourself.html#for-loops-when-you-know-how-many-times)<br/>[Repeating Yourself — Nested Loops](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/repeating-yourself.html#nested-loops) |
| `PDP-LO7` Develop documented programs for familiar and unfamiliar problems | 🟩 | [Building Reusable Tools — Handling Edge Cases](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/building-reusable-tools.html#handling-edge-cases)<br/>[Storing and Computing — Putting It Together: A Small Program](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/storing-and-computing.html#putting-it-together-a-small-program) |
| `PDP-LO8` Modularisation: functions, procedures, scope, parameter passing | 🟩 | [Building Reusable Tools — What Makes a Good Function?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/building-reusable-tools.html#what-makes-a-good-function)<br/>[Building Reusable Tools — Functions Calling Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/building-reusable-tools.html#functions-calling-functions)<br/>[Building Reusable Tools — Variable Scope Revisited](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/building-reusable-tools.html#variable-scope-revisited)<br/>[Finding Things — Scope: Where Variables Live](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#scope-where-variables-live)<br/>[Lists and Sequences — Functions: Reusable Algorithms](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/lists-and-sequences.html#functions-reusable-algorithms)<br/>[Pictures Worth Numbers — Writing Reusable Plotting Functions](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/pictures-worth-numbers.html#writing-reusable-plotting-functions) |
| `PDP-LO9` Interpret compiler and linker messages and react appropriately | 🟩 | [When It Goes Wrong — Three Kinds of Wrong](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/when-it-goes-wrong.html#three-kinds-of-wrong)<br/>[When It Goes Wrong — Errors Python Catches Before It Starts](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/when-it-goes-wrong.html#errors-python-catches-before-it-starts)<br/>[When It Goes Wrong — Errors That Happen While It Runs](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/when-it-goes-wrong.html#errors-that-happen-while-it-runs)<br/>[When It Goes Wrong — Reading a Traceback](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/when-it-goes-wrong.html#reading-a-traceback)<br/>[When It Goes Wrong — The Dangerous Kind](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/when-it-goes-wrong.html#the-dangerous-kind) |
| `PDP-LO10` The testing process: structured walkthroughs and debugging tools | 🟩 | [Bringing It All Together — Problem 4: Building and Verifying](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/bringing-it-all-together.html#problem-4-building-and-verifying)<br/>[Building Reusable Tools — Testing as a Habit](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/building-reusable-tools.html#testing-as-a-habit) |
| `PDP-LO11` Coding standards: comments, indentation, variable naming | 🟩 | [Building Reusable Tools — What Makes a Good Function?](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/building-reusable-tools.html#what-makes-a-good-function)<br/>[Looking Back Before Moving Forward — Part 1: Reading Your Own Code](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/critique-and-reflection.html#part-1-reading-your-own-code)<br/>[Looking Back Before Moving Forward — Part 2: Reading Someone Else's Code](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/critique-and-reflection.html#part-2-reading-someone-elses-code)<br/>[Storing and Computing — Variables: Giving Names to Things](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/storing-and-computing.html#variables-giving-names-to-things) |
| `PDP-LO12` Team programming: design, develop, release and review over time, in teams of three to five | 🟩 | [The Team Project — What You Are Being Asked to Do](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-team-project.html#what-you-are-being-asked-to-do)<br/>[The Team Project — Three Releases, Not One Deadline](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-team-project.html#three-releases-not-one-deadline)<br/>[The Team Project — Working on One Thing at Once](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-team-project.html#working-on-one-thing-at-once)<br/>[The Team Project — Reviewing Each Other's Work](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/the-team-project.html#reviewing-each-others-work) |

### Computational Methods and Problem Solving 5N0554

| Outcome | | Where |
|---|---|---|
| `CMPS-LO1` Data structures and representations — arrays, lists, matrices, trees — and the difference between iterative and recursive algorithms | 🟩 | [A Chain Reads a Book — Too Many Words for a Grid](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-chain-reads-a-book.html#too-many-words-for-a-grid)<br/>[Finding Everything Inside a Folder — A Structure That Branches](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-everything-inside-a-folder.html#a-structure-that-branches)<br/>[Finding Everything Inside a Folder — Walking It With Recursion](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-everything-inside-a-folder.html#walking-it-with-recursion)<br/>[Finding Everything Inside a Folder — Walking It Without Recursion](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-everything-inside-a-folder.html#walking-it-without-recursion)<br/>_used in:_ [A Chain Reads a Book — Loading a Real Book](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-chain-reads-a-book.html#loading-a-real-book)<br/>_used in:_ [A Grid of Numbers — Nine Numbers That Draw a Picture](https://deweydex.github.io/dewlab/tutorials/computational-methods/grid-of-numbers.html#nine-numbers-that-draw-a-picture)<br/>_used in:_ [How Much It Remembers — Comparing What Each One Writes](https://deweydex.github.io/dewlab/tutorials/computational-methods/how-much-it-remembers.html#comparing-what-each-one-writes)<br/>_used in:_ [Where Chains Lead — Words That Follow Words](https://deweydex.github.io/dewlab/tutorials/computational-methods/where-chains-lead.html#words-that-follow-words)<br/>_used in:_ [Whose Voice Is This — Cleaning Two Different Books](https://deweydex.github.io/dewlab/tutorials/computational-methods/whose-voice-is-this.html#cleaning-two-different-books) |
| `CMPS-LO2` Elementary probability and information theory: distributions, sample statistics, dependent and independent events, conditional probability, and randomness in computing | 🟩 | [Leaving It to Chance — Asking the Machine for a Number](https://deweydex.github.io/dewlab/tutorials/computational-methods/leaving-it-to-chance.html#asking-the-machine-for-a-number)<br/>[Leaving It to Chance — The Same Numbers Twice](https://deweydex.github.io/dewlab/tutorials/computational-methods/leaving-it-to-chance.html#the-same-numbers-twice)<br/>[Leaving It to Chance — What Random Is Good Enough For](https://deweydex.github.io/dewlab/tutorials/computational-methods/leaving-it-to-chance.html#what-random-is-good-enough-for)<br/>[Leaving It to Chance — Choosing From a List](https://deweydex.github.io/dewlab/tutorials/computational-methods/leaving-it-to-chance.html#choosing-from-a-list)<br/>_used in:_ [Where Chains Lead — A Weather Machine](https://deweydex.github.io/dewlab/tutorials/computational-methods/where-chains-lead.html#a-weather-machine)<br/>_used in:_ [Whose Voice Is This — Investigating the Difference](https://deweydex.github.io/dewlab/tutorials/computational-methods/whose-voice-is-this.html#investigating-the-difference) |
| `CMPS-LO3` Basic computational and numerical methods for computer simulation | 🟩 | [Counting Darts — A Question You Can Answer by Throwing Things](https://deweydex.github.io/dewlab/tutorials/computational-methods/counting-darts.html#a-question-you-can-answer-by-throwing-things)<br/>[Counting Darts — One Dart at a Time](https://deweydex.github.io/dewlab/tutorials/computational-methods/counting-darts.html#one-dart-at-a-time)<br/>[Counting Darts — Watching It Settle](https://deweydex.github.io/dewlab/tutorials/computational-methods/counting-darts.html#watching-it-settle)<br/>[Counting Darts — More Is Not Reliably Better](https://deweydex.github.io/dewlab/tutorials/computational-methods/counting-darts.html#more-is-not-reliably-better)<br/>_used in:_ [Leaving It to Chance — What Random Is Good Enough For](https://deweydex.github.io/dewlab/tutorials/computational-methods/leaving-it-to-chance.html#what-random-is-good-enough-for) |
| `CMPS-LO4` Apply array and matrix representations to real-world computational problems | 🟩 | [A Chain Reads a Book — A Dictionary of Dictionaries](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-chain-reads-a-book.html#a-dictionary-of-dictionaries)<br/>[How Much It Remembers — Keying On More Than One Word](https://deweydex.github.io/dewlab/tutorials/computational-methods/how-much-it-remembers.html#keying-on-more-than-one-word)<br/>[Solving Systems — Three Unknowns, Row by Row](https://deweydex.github.io/dewlab/tutorials/computational-methods/solving-systems.html#three-unknowns-row-by-row)<br/>[Solving Systems — Reading Off the Answer](https://deweydex.github.io/dewlab/tutorials/computational-methods/solving-systems.html#reading-off-the-answer)<br/>[Solving Systems — Checking Your Work](https://deweydex.github.io/dewlab/tutorials/computational-methods/solving-systems.html#checking-your-work)<br/>[Undoing It — Undoing a Transformation](https://deweydex.github.io/dewlab/tutorials/computational-methods/undoing-it.html#undoing-a-transformation)<br/>[Undoing It — Which Ones Can Be Undone](https://deweydex.github.io/dewlab/tutorials/computational-methods/undoing-it.html#which-ones-can-be-undone)<br/>[What a Matrix Does to a Picture — Where Do the Corners Go?](https://deweydex.github.io/dewlab/tutorials/computational-methods/what-a-matrix-does-to-a-picture.html#where-do-the-corners-go)<br/>[What a Matrix Does to a Picture — A Small Gallery](https://deweydex.github.io/dewlab/tutorials/computational-methods/what-a-matrix-does-to-a-picture.html#a-small-gallery)<br/>[What a Matrix Does to a Picture — Guess the Matrix](https://deweydex.github.io/dewlab/tutorials/computational-methods/what-a-matrix-does-to-a-picture.html#guess-the-matrix)<br/>[Where Chains Lead — A Weather Machine](https://deweydex.github.io/dewlab/tutorials/computational-methods/where-chains-lead.html#a-weather-machine)<br/>[Where Chains Lead — Watching It Settle](https://deweydex.github.io/dewlab/tutorials/computational-methods/where-chains-lead.html#watching-it-settle)<br/>[Where Chains Lead — Words That Follow Words](https://deweydex.github.io/dewlab/tutorials/computational-methods/where-chains-lead.html#words-that-follow-words)<br/>[Where Chains Lead — Ranking a Small Web](https://deweydex.github.io/dewlab/tutorials/computational-methods/where-chains-lead.html#ranking-a-small-web)<br/>[Whose Voice Is This — Two Writers, Two Chains](https://deweydex.github.io/dewlab/tutorials/computational-methods/whose-voice-is-this.html#two-writers-two-chains)<br/>_used in:_ [A Grid of Numbers — Two Grids, Added Together](https://deweydex.github.io/dewlab/tutorials/computational-methods/grid-of-numbers.html#two-grids-added-together)<br/>_used in:_ [A Grid of Numbers — Scaling and the Shape Rule](https://deweydex.github.io/dewlab/tutorials/computational-methods/grid-of-numbers.html#scaling-and-the-shape-rule)<br/>_used in:_ [A Grid of Numbers — Turning It Sideways: the Transpose](https://deweydex.github.io/dewlab/tutorials/computational-methods/grid-of-numbers.html#turning-it-sideways-the-transpose)<br/>_used in:_ [Multiplying Grids — The Dot Product, First](https://deweydex.github.io/dewlab/tutorials/computational-methods/multiplying-grids.html#the-dot-product-first)<br/>_used in:_ [Multiplying Grids — Multiplying Two Grids](https://deweydex.github.io/dewlab/tutorials/computational-methods/multiplying-grids.html#multiplying-two-grids)<br/>_used in:_ [Multiplying Grids — Order Matters](https://deweydex.github.io/dewlab/tutorials/computational-methods/multiplying-grids.html#order-matters)<br/>_used in:_ [Multiplying Grids — The Matrix That Does Nothing](https://deweydex.github.io/dewlab/tutorials/computational-methods/multiplying-grids.html#the-matrix-that-does-nothing)<br/>_used in:_ [Solving Systems — A System You Can Already Solve](https://deweydex.github.io/dewlab/tutorials/computational-methods/solving-systems.html#a-system-you-can-already-solve)<br/>_used in:_ [Undoing It — Measuring the Square](https://deweydex.github.io/dewlab/tutorials/computational-methods/undoing-it.html#measuring-the-square)<br/>_used in:_ [Undoing It — When the Square Collapses](https://deweydex.github.io/dewlab/tutorials/computational-methods/undoing-it.html#when-the-square-collapses) |
| `CMPS-LO5` Assess an algorithm or computational approach for speed, efficiency, and best/expected/worst-case behaviour | 🟩 | [Finding Things — Linear Search: The Straightforward Approach](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#linear-search-the-straightforward-approach)<br/>[Finding Things — Binary Search: The Power of Sorted Data](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#binary-search-the-power-of-sorted-data)<br/>[Finding Things — Putting It Together](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/finding-things.html#putting-it-together)<br/>[Putting Things in Order — Comparing Our Sorts](https://deweydex.github.io/dewlab/tutorials/mit-pdp-maths-prog-integration/putting-things-in-order.html#comparing-our-sorts)<br/>_used in:_ [Three Ways to Make Change — Remembering What We Already Worked Out](https://deweydex.github.io/dewlab/tutorials/computational-methods/three-ways-to-make-change.html#remembering-what-we-already-worked-out)<br/>_used in:_ [Three Ways to Make Change — The Greedy Shortcut](https://deweydex.github.io/dewlab/tutorials/computational-methods/three-ways-to-make-change.html#the-greedy-shortcut) |
| `CMPS-LO6` Apply probability and information theory to computational approaches to real-world problems | 🟩 | [When a Queue Never Clears — Arrivals You Cannot Predict, One at a Time](https://deweydex.github.io/dewlab/tutorials/computational-methods/when-a-queue-never-clears.html#arrivals-you-cannot-predict-one-at-a-time)<br/>[When a Queue Never Clears — A Queue That Clears](https://deweydex.github.io/dewlab/tutorials/computational-methods/when-a-queue-never-clears.html#a-queue-that-clears)<br/>[When a Queue Never Clears — A Queue That Never Clears](https://deweydex.github.io/dewlab/tutorials/computational-methods/when-a-queue-never-clears.html#a-queue-that-never-clears)<br/>[When a Queue Never Clears — Predicting It Before Running It](https://deweydex.github.io/dewlab/tutorials/computational-methods/when-a-queue-never-clears.html#predicting-it-before-running-it) |
| `CMPS-LO7` Differentiate modelling from simulation, and the abstraction that lets a machine address a real-world problem | 🟩 | [A Model That Corrects Itself — A Model That Starts Out Wrong](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-model-that-corrects-itself.html#a-model-that-starts-out-wrong)<br/>[A Model That Corrects Itself — Running It Again and Again](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-model-that-corrects-itself.html#running-it-again-and-again)<br/>[A Model That Corrects Itself — What the Model Actually Learned](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-model-that-corrects-itself.html#what-the-model-actually-learned) |
| `CMPS-LO8` Identify approaches to problem definition, solution design, testing and evaluation | 🟩 | [Finding Where It Went Wrong — Deciding What Done Means](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-where-it-went-wrong.html#deciding-what-done-means)<br/>[Finding Where It Went Wrong — Building the Pipeline](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-where-it-went-wrong.html#building-the-pipeline) |
| `CMPS-LO9` Strengths, weaknesses and areas of application of contemporary problem definition and analysis techniques | 🟩 | [Three Ways to Make Change — Trying Every Combination](https://deweydex.github.io/dewlab/tutorials/computational-methods/three-ways-to-make-change.html#trying-every-combination)<br/>[Three Ways to Make Change — Remembering What We Already Worked Out](https://deweydex.github.io/dewlab/tutorials/computational-methods/three-ways-to-make-change.html#remembering-what-we-already-worked-out)<br/>[Three Ways to Make Change — The Greedy Shortcut](https://deweydex.github.io/dewlab/tutorials/computational-methods/three-ways-to-make-change.html#the-greedy-shortcut)<br/>[Three Ways to Make Change — Choosing a Strategy](https://deweydex.github.io/dewlab/tutorials/computational-methods/three-ways-to-make-change.html#choosing-a-strategy) |
| `CMPS-LO10` Distinguish pragmatic problem-solving (treating the symptom) from semantic analysis (finding the root cause) | 🟩 | [Finding Where It Went Wrong — The Symptom Is Not the Cause](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-where-it-went-wrong.html#the-symptom-is-not-the-cause)<br/>_used in:_ [Finding Where It Went Wrong — Building the Pipeline](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-where-it-went-wrong.html#building-the-pipeline) |
| `CMPS-LO11` An iterative process of model creation and validation against the real-world situation being modelled | 🟩 | [A Model That Corrects Itself — Checking It Against Patterns It Has Never Seen](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-model-that-corrects-itself.html#checking-it-against-patterns-it-has-never-seen)<br/>_used in:_ [A Model That Corrects Itself — Running It Again and Again](https://deweydex.github.io/dewlab/tutorials/computational-methods/a-model-that-corrects-itself.html#running-it-again-and-again) |
| `CMPS-LO12` The role of personal attributes — initiative, a methodical approach, logical reasoning, persistence, lateral thinking — in preventing and resolving problems | 🟩 | [Finding Where It Went Wrong — What Finding It Actually Took](https://deweydex.github.io/dewlab/tutorials/computational-methods/finding-where-it-went-wrong.html#what-finding-it-actually-took) |
| `CMPS-LO13` Reflect on the impact of numerical and logical thinking in the real world: accuracy, precision, and decisions made from computational models and simulations | 🟩 | [Counting Darts — More Is Not Reliably Better](https://deweydex.github.io/dewlab/tutorials/computational-methods/counting-darts.html#more-is-not-reliably-better) |

### Fundamentals of Object Oriented Programming 5N0541

| Outcome | | Where |
|---|---|---|
| `FOOP-LO1` Data types used in object oriented programs | 🟩 | [Objects and Classes — One Thing, Many Parts](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/objects-and-classes.html#one-thing-many-parts) |
| `FOOP-LO2` The fundamental set of instructions in a program, and using them to design and construct programs that solve problems | 🟩 | [The Moves You Already Know — The Handful of Moves](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/the-moves-you-already-know.html#the-handful-of-moves)<br/>[The Moves You Already Know — The Same Moves, Inside a Class](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/the-moves-you-already-know.html#the-same-moves-inside-a-class)<br/>[The Moves You Already Know — One Method, Several Moves](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/the-moves-you-already-know.html#one-method-several-moves) |
| `FOOP-LO3` Basic object oriented constructs: classes, objects, methods, fields, encapsulation, abstraction, inheritance | 🟩 | [Objects and Classes — One Thing, Many Parts](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/objects-and-classes.html#one-thing-many-parts)<br/>[Objects and Classes — Keeping Details to Itself](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/objects-and-classes.html#keeping-details-to-itself)<br/>[Objects and Classes — Building on What Already Exists](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/objects-and-classes.html#building-on-what-already-exists) |
| `FOOP-LO4` Design and construct modular, reusable code blocks | 🟩 | [One Class, Many Methods — From Loose Functions to One Class](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/one-class-many-methods.html#from-loose-functions-to-one-class)<br/>[One Class, Many Methods — Giving It More to Do](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/one-class-many-methods.html#giving-it-more-to-do) |
| `FOOP-LO5` Work within a modern integrated development environment | 🟩 | [The Tools Around Your Code — An Environment You Are Already In](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/the-tools-around-your-code.html#an-environment-you-are-already-in)<br/>[The Tools Around Your Code — Errors Worth Reading](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/the-tools-around-your-code.html#errors-worth-reading)<br/>[The Tools Around Your Code — What the Editor Already Knows](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/the-tools-around-your-code.html#what-the-editor-already-knows)<br/>[The Tools Around Your Code — Where a Bigger Project Lives](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/the-tools-around-your-code.html#where-a-bigger-project-lives) |
| `FOOP-LO6` Construct larger programs from smaller ones | 🟩 | [One Parent, Many Children — Another Kind of Account](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/one-parent-many-children.html#another-kind-of-account)<br/>[One Parent, Many Children — Many Kinds, One Loop](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/one-parent-many-children.html#many-kinds-one-loop) |
| `FOOP-LO7` Model real-world objects to build object oriented programs that model real-world activities | 🟩 | [One Parent, Many Children — Many Kinds, One Loop](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/one-parent-many-children.html#many-kinds-one-loop)<br/>[One Parent, Many Children — A Bank Holds Its Accounts](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/one-parent-many-children.html#a-bank-holds-its-accounts) |
| `FOOP-LO8` Ways to organise and structure data | 🟩 | [One Class, Many Methods — Data That Belongs Together](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/one-class-many-methods.html#data-that-belongs-together) |
| `FOOP-LO9` Document program code properly | 🟩 | [Documenting a Class — A Class Docstring](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/documenting-a-class.html#a-class-docstring)<br/>[Documenting a Class — Documenting Each Method](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/documenting-a-class.html#documenting-each-method)<br/>[Documenting a Class — Keeping Documentation Honest](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/documenting-a-class.html#keeping-documentation-honest) |
| `FOOP-LO10` Debug and test programs | 🟩 | [Testing What a Class Does — A Bug That Hides in Another Class](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/testing-what-a-class-does.html#a-bug-that-hides-in-another-class)<br/>[Testing What a Class Does — Writing a Test for One Method](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/testing-what-a-class-does.html#writing-a-test-for-one-method)<br/>[Testing What a Class Does — A Few Tests, Run Together](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/testing-what-a-class-does.html#a-few-tests-run-together) |
| `FOOP-LO11` Deploy a program to the end user via a front end | 🟩 | [A Front End for a Class — A Program Only Its Author Can Use](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/a-front-end-for-a-class.html#a-program-only-its-author-can-use)<br/>[A Front End for a Class — A Menu Loop](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/a-front-end-for-a-class.html#a-menu-loop)<br/>[A Front End for a Class — Leaving the Loop Cleanly](https://deweydex.github.io/dewlab/tutorials/fundamentals-of-oop/a-front-end-for-a-class.html#leaving-the-loop-cleanly) |

### Database Methods 5N0783

| Outcome | | Where |
|---|---|---|
| `DBM-LO1` Typical uses for databases, in everyday life and in business decision-making | 🟩 | [A Table Is a List of Rows — Where databases already show up](https://deweydex.github.io/dewlab/tutorials/database-methods/a-table-is-a-list-of-rows.html#where-databases-already-show-up) |
| `DBM-LO2` Essential database concepts: tables, rows, columns, statements, queries | 🟩 | [A Table Is a List of Rows — Three instructions, one script](https://deweydex.github.io/dewlab/tutorials/database-methods/a-table-is-a-list-of-rows.html#three-instructions-one-script)<br/>[Designing a Table Before You Build It — Naming a column and its type](https://deweydex.github.io/dewlab/tutorials/database-methods/designing-a-table-before-you-build-it.html#naming-a-column-and-its-type)<br/>_used in:_ [The Library Loans Quiz — Task 1: authors and books](https://deweydex.github.io/dewlab/tutorials/database-methods/the-library-loans-quiz.html#task-1-authors-and-books)<br/>_used in:_ [The Library Loans Quiz — Task 3: members and loans](https://deweydex.github.io/dewlab/tutorials/database-methods/the-library-loans-quiz.html#task-3-members-and-loans) |
| `DBM-LO3` Explain what a query does, and read and write one in SQL (the descriptor's own list — design view, datasheet view, pivot table, pivot chart — names a GUI tool's views; dewlab teaches the query language directly instead) | 🟩 | [Asking Questions of a Table — Naming columns](https://deweydex.github.io/dewlab/tutorials/database-methods/asking-questions-of-a-table.html#naming-columns)<br/>_used in:_ [SQL Practice — Exercise 1: naming columns](https://deweydex.github.io/dewlab/tutorials/database-methods/sql-practice.html#exercise-1-naming-columns) |
| `DBM-LO4` Open an existing table and carry out routine operations on it: reading, adding, editing, deleting, sorting and filtering rows | 🟩 | [Updating and Deleting Rows — UPDATE: changing a value](https://deweydex.github.io/dewlab/tutorials/database-methods/changing-what-is-in-it.html#update-changing-a-value)<br/>[Updating and Deleting Rows — DELETE: removing a row](https://deweydex.github.io/dewlab/tutorials/database-methods/changing-what-is-in-it.html#delete-removing-a-row)<br/>_used in:_ [SQL Practice — Exercise 3: INSERT](https://deweydex.github.io/dewlab/tutorials/database-methods/sql-practice.html#exercise-3-insert)<br/>_used in:_ [The Tentacular Plushies Quiz — Task 3: add products](https://deweydex.github.io/dewlab/tutorials/database-methods/the-tentacular-plushies-quiz.html#task-3-add-products) |
| `DBM-LO5` Retrieve chosen data from one or more tables by writing a query, saved as the reader's own work for reuse | 🟩 | [A College Timetable — Finding a clash](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#finding-a-clash)<br/>[A Second Table and a Join — JOIN: querying across both tables](https://deweydex.github.io/dewlab/tutorials/database-methods/a-second-table-and-a-join.html#join-querying-across-both-tables)<br/>[Asking Questions of a Table — WHERE: keeping only some rows](https://deweydex.github.io/dewlab/tutorials/database-methods/asking-questions-of-a-table.html#where-keeping-only-some-rows)<br/>[Joining Two Real Tables — The join that loses a row](https://deweydex.github.io/dewlab/tutorials/database-methods/joining-two-real-tables.html#the-join-that-loses-a-row)<br/>_used in:_ [A College Timetable — Asking it real questions](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#asking-it-real-questions)<br/>_used in:_ [A College Timetable — The same idea, for a teacher](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#the-same-idea-for-a-teacher)<br/>_used in:_ [Asking Questions of a Table — ORDER BY: choosing an order](https://deweydex.github.io/dewlab/tutorials/database-methods/asking-questions-of-a-table.html#order-by-choosing-an-order)<br/>_used in:_ [Charting a Query's Result — From SELECT to DataFrame](https://deweydex.github.io/dewlab/tutorials/database-methods/charting-a-querys-result.html#from-select-to-dataframe)<br/>_used in:_ [Loading a Real Dataset — Querying it as SQL](https://deweydex.github.io/dewlab/tutorials/database-methods/loading-a-real-dataset.html#querying-it-as-sql)<br/>_used in:_ [SQL Practice — Exercise 2: WHERE](https://deweydex.github.io/dewlab/tutorials/database-methods/sql-practice.html#exercise-2-where)<br/>_used in:_ [SQL Practice — Exercise 4: ORDER BY](https://deweydex.github.io/dewlab/tutorials/database-methods/sql-practice.html#exercise-4-order-by)<br/>_used in:_ [SQL Practice — Exercise 5: COUNT](https://deweydex.github.io/dewlab/tutorials/database-methods/sql-practice.html#exercise-5-count)<br/>_used in:_ [The Library Loans Quiz — Task 6: two questions for your database](https://deweydex.github.io/dewlab/tutorials/database-methods/the-library-loans-quiz.html#task-6-two-questions-for-your-database)<br/>_used in:_ [The Tentacular Plushies Quiz — Task 5: query the data](https://deweydex.github.io/dewlab/tutorials/database-methods/the-tentacular-plushies-quiz.html#task-5-query-the-data) |
| `DBM-LO6` Write the query a data-entry submission would run against a table (the descriptor's own form is a GUI data-entry screen; dewlab covers the query side here and the HTML side in Web Authoring) | 🟩 | [A Form That Writes a Row — The row a submission would add](https://deweydex.github.io/dewlab/tutorials/database-methods/a-form-that-writes-a-row.html#the-row-a-submission-would-add) |
| `DBM-LO7` Present selected information from a database in a format suitable for sharing or printing (the descriptor's own GUI report builder; dewlab teaches a CSV export and a chart instead) | 🟩 | [Exporting a Query to a File — Saving it as a file](https://deweydex.github.io/dewlab/tutorials/database-methods/exporting-a-query-to-a-file.html#saving-it-as-a-file)<br/>_used in:_ [Charting a Query's Result — One line per country](https://deweydex.github.io/dewlab/tutorials/database-methods/charting-a-querys-result.html#one-line-per-country) |
| `DBM-LO8` Import external data, such as a CSV file, into a table | 🟩 | [Loading a Real Dataset — Fetching a CSV from a Python cell](https://deweydex.github.io/dewlab/tutorials/database-methods/loading-a-real-dataset.html#fetching-a-csv-from-a-python-cell) |
| `DBM-LO9` Design a database to a brief: tables, primary keys, and the relationships between tables | 🟩 | [A College Timetable — Five tables for one timetable](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#five-tables-for-one-timetable)<br/>[Designing a Table Before You Build It — What goes in which table](https://deweydex.github.io/dewlab/tutorials/database-methods/designing-a-table-before-you-build-it.html#what-goes-in-which-table)<br/>[Designing a Table Before You Build It — One row can point at many](https://deweydex.github.io/dewlab/tutorials/database-methods/designing-a-table-before-you-build-it.html#one-row-can-point-at-many)<br/>[The Library Loans Quiz — Task 2: a book can have more than one author](https://deweydex.github.io/dewlab/tutorials/database-methods/the-library-loans-quiz.html#task-2-a-book-can-have-more-than-one-author)<br/>_used in:_ [A College Timetable — Finding a clash](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#finding-a-clash)<br/>_used in:_ [A Second Table and a Join — JOIN: querying across both tables](https://deweydex.github.io/dewlab/tutorials/database-methods/a-second-table-and-a-join.html#join-querying-across-both-tables)<br/>_used in:_ [Joining Two Real Tables — A second table, written by hand](https://deweydex.github.io/dewlab/tutorials/database-methods/joining-two-real-tables.html#a-second-table-written-by-hand) |
| `DBM-LO10` Build a database to a brief: create its tables, load or enter data, and write the queries it needs | 🟩 | [A College Timetable — Building it](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#building-it)<br/>[The Library Loans Quiz — Task 4: add authors, books, and authorships](https://deweydex.github.io/dewlab/tutorials/database-methods/the-library-loans-quiz.html#task-4-add-authors-books-and-authorships)<br/>[The Tentacular Plushies Quiz — Task 1: a products table](https://deweydex.github.io/dewlab/tutorials/database-methods/the-tentacular-plushies-quiz.html#task-1-a-products-table)<br/>[The Tentacular Plushies Quiz — Task 2: a transactions table](https://deweydex.github.io/dewlab/tutorials/database-methods/the-tentacular-plushies-quiz.html#task-2-a-transactions-table)<br/>_used in:_ [A College Timetable — Your turn](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#your-turn)<br/>_used in:_ [The Library Loans Quiz — Task 5: add members and loans](https://deweydex.github.io/dewlab/tutorials/database-methods/the-library-loans-quiz.html#task-5-add-members-and-loans) |
| `DBM-LO11` Use hints, error messages and self-checks to work through an unfamiliar database problem | 🟩 | [The Library Loans Quiz — Task 2: a book can have more than one author](https://deweydex.github.io/dewlab/tutorials/database-methods/the-library-loans-quiz.html#task-2-a-book-can-have-more-than-one-author)<br/>[The Tentacular Plushies Quiz — Task 1: a products table](https://deweydex.github.io/dewlab/tutorials/database-methods/the-tentacular-plushies-quiz.html#task-1-a-products-table)<br/>_used in:_ [A College Timetable — Your turn](https://deweydex.github.io/dewlab/tutorials/database-methods/a-college-timetable.html#your-turn) |

### Web Authoring 5N1910

| Outcome | | Where |
|---|---|---|
| `WA-LO1` The development of HTML and CSS, through the versions of each standard | 🟩 | [Conclusions and Next Steps — How HTML and CSS got here](https://deweydex.github.io/dewlab/tutorials/web-authoring/conclusions-and-next-steps.html#how-html-and-css-got-here) |
| `WA-LO2` The use, purpose and attributes of a range of HTML tags, and how browsers render them | 🟩 | [A page is files — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-page-is-files.html#why-this-happens)<br/>[Headings, paragraphs and emphasis — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/headings-and-emphasis.html#why-this-happens)<br/>[Images, paths and alt text — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/images-and-alt-text.html#why-this-happens)<br/>[Navigation — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/navigation.html#why-this-happens)<br/>[Sections, and the tags that mean something — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/sections-that-mean-something.html#why-this-happens)<br/>[The skeleton: head and body — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-skeleton.html#why-this-happens)<br/>[Three kinds of link — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/three-kinds-of-link.html#why-this-happens)<br/>_used in:_ [A form — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-form.html#why-this-happens)<br/>_used in:_ [A rule, and where it lives — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-rule-and-where-it-lives.html#why-this-happens)<br/>_used in:_ [Images and file size — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/images-and-file-size.html#your-turn)<br/>_used in:_ [Keyframe animation and the checkbox hack — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/keyframes-and-the-checkbox-hack.html#why-this-happens)<br/>_used in:_ [Keyframe animation and the checkbox hack — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/keyframes-and-the-checkbox-hack.html#your-turn)<br/>_used in:_ [Several pages, one navigation — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/pages-and-navigation.html#why-this-happens)<br/>_used in:_ [Quick reference — HTML](https://deweydex.github.io/dewlab/tutorials/web-authoring/quick-reference.html#html) |
| `WA-LO3` Explore available HTML and CSS editors and development tools (the descriptor's own contrast is a WYSIWYG editor against a text editor; dewlab explores its own in-browser site editor against a plain-text editor instead) | 🟩 | [An editor — VS Code, the usual choice](https://deweydex.github.io/dewlab/tutorials/web-authoring/an-editor.html#vs-code-the-usual-choice)<br/>[An editor — No installing anything: GitHub's own editor](https://deweydex.github.io/dewlab/tutorials/web-authoring/an-editor.html#no-installing-anything-githubs-own-editor)<br/>_used in:_ [Your copy of the starter — Three ways to open it](https://deweydex.github.io/dewlab/tutorials/web-authoring/your-copy-of-the-starter.html#three-ways-to-open-it) |
| `WA-LO4` The principles of good website design: target audience, site objectives, navigation, structure, interface and access speed | 🟩 | [Images and file size — Choosing a format](https://deweydex.github.io/dewlab/tutorials/web-authoring/images-and-file-size.html#choosing-a-format)<br/>[Images and file size — Keeping file size down](https://deweydex.github.io/dewlab/tutorials/web-authoring/images-and-file-size.html#keeping-file-size-down)<br/>[Planning a site — Two site maps](https://deweydex.github.io/dewlab/tutorials/web-authoring/planning-a-site.html#two-site-maps)<br/>[Planning a site — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/planning-a-site.html#why-this-happens)<br/>_used in:_ [Images and file size — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/images-and-file-size.html#your-turn)<br/>_used in:_ [Several pages, one navigation — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/pages-and-navigation.html#why-this-happens)<br/>_used in:_ [Planning a site — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/planning-a-site.html#your-turn)<br/>_used in:_ [Project ideas — Making any of them easy to read](https://deweydex.github.io/dewlab/tutorials/web-authoring/project-ideas.html#making-any-of-them-easy-to-read) |
| `WA-LO5` Investigate available web authoring tools, including desktop publishing programs and website management systems (the descriptor's own examples — Dreamweaver, Photoshop, Joomla, WordPress — are commercial GUI tools; dewlab discusses GitHub Pages, WordPress and two modern single-page builders against the hand-written HTML and CSS this course actually teaches) | 🟩 | [Conclusions and Next Steps — Other ways to build a website](https://deweydex.github.io/dewlab/tutorials/web-authoring/conclusions-and-next-steps.html#other-ways-to-build-a-website)<br/>_used in:_ [Conclusions and Next Steps — Give it a try](https://deweydex.github.io/dewlab/tutorials/web-authoring/conclusions-and-next-steps.html#give-it-a-try) |
| `WA-LO6` Keep evidence of a web authoring project: its own research, requirements, and an evaluation of the finished site | 🟩 | [Documenting what you built — What readme.md is for](https://deweydex.github.io/dewlab/tutorials/web-authoring/documenting-what-you-built.html#what-readmemd-is-for)<br/>_used in:_ [Documenting what you built — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/documenting-what-you-built.html#your-turn) |
| `WA-LO7` Plan a design and user interface for a specified website, documenting each stage of the process (the descriptor's own outcome also has the learner selecting an authoring tool; dewlab's own tool is a given, not a choice) | 🟩 | [Planning a site — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/planning-a-site.html#why-this-happens)<br/>_used in:_ [Planning a site — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/planning-a-site.html#your-turn) |
| `WA-LO8` Use HTML tags to build a standards-conformant page or site to a given design | 🟩 | [A page is files — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-page-is-files.html#your-turn)<br/>_used in:_ [A form — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-form.html#your-turn)<br/>_used in:_ [Headings, paragraphs and emphasis — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/headings-and-emphasis.html#your-turn)<br/>_used in:_ [Images, paths and alt text — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/images-and-alt-text.html#your-turn)<br/>_used in:_ [Images and file size — An images folder](https://deweydex.github.io/dewlab/tutorials/web-authoring/images-and-file-size.html#an-images-folder)<br/>_used in:_ [Navigation — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/navigation.html#your-turn)<br/>_used in:_ [Several pages, one navigation — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/pages-and-navigation.html#your-turn)<br/>_used in:_ [Project ideas — After you fork the starter](https://deweydex.github.io/dewlab/tutorials/web-authoring/project-ideas.html#after-you-fork-the-starter)<br/>_used in:_ [Sections, and the tags that mean something — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/sections-that-mean-something.html#your-turn)<br/>_used in:_ [The skeleton: head and body — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-skeleton.html#your-turn)<br/>_used in:_ [Three kinds of link — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/three-kinds-of-link.html#your-turn) |
| `WA-LO9` Use CSS to style a standards-conformant page or site to a given design | 🟩 | [A rule, and where it lives — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-rule-and-where-it-lives.html#why-this-happens)<br/>[CSS variables and BEM names — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/css-variables-and-bem.html#why-this-happens)<br/>[Flexbox first steps — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/flexbox-first-steps.html#why-this-happens)<br/>[Flexible images — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/flexible-images.html#why-this-happens)<br/>[States: hover and focus — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/hover-and-focus.html#why-this-happens)<br/>[Keyframe animation and the checkbox hack — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/keyframes-and-the-checkbox-hack.html#why-this-happens)<br/>[Media queries — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/media-queries.html#why-this-happens)<br/>[Named grid areas — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/named-grid-areas.html#why-this-happens)<br/>[Position, and the sticky header — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/position-and-the-sticky-header.html#why-this-happens)<br/>[Position, and the sticky header — And the footer](https://deweydex.github.io/dewlab/tutorials/web-authoring/position-and-the-sticky-header.html#and-the-footer)<br/>[Selectors and classes — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/selectors-and-classes.html#why-this-happens)<br/>[Text and units — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/text-and-units.html#why-this-happens)<br/>[The box — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-box.html#why-this-happens)<br/>[The container: width and centring — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-container.html#why-this-happens)<br/>[Transitions and transforms — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/transitions-and-transforms.html#why-this-happens)<br/>[Variables and colour — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/variables-and-colour.html#why-this-happens)<br/>_used in:_ [A form — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-form.html#why-this-happens)<br/>_used in:_ [A grid gallery — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-grid-gallery.html#why-this-happens)<br/>_used in:_ [A grid gallery — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-grid-gallery.html#your-turn)<br/>_used in:_ [Cards in a row — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/cards-in-a-row.html#why-this-happens)<br/>_used in:_ [Cards in a row — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/cards-in-a-row.html#your-turn)<br/>_used in:_ [CSS variables and BEM names — Naming with BEM](https://deweydex.github.io/dewlab/tutorials/web-authoring/css-variables-and-bem.html#naming-with-bem)<br/>_used in:_ [CSS variables and BEM names — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/css-variables-and-bem.html#your-turn)<br/>_used in:_ [Flexbox first steps — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/flexbox-first-steps.html#your-turn)<br/>_used in:_ [Flexible images — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/flexible-images.html#your-turn)<br/>_used in:_ [States: hover and focus — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/hover-and-focus.html#your-turn)<br/>_used in:_ [Keyframe animation and the checkbox hack — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/keyframes-and-the-checkbox-hack.html#your-turn)<br/>_used in:_ [Media queries — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/media-queries.html#your-turn)<br/>_used in:_ [Named grid areas — Other properties from the same lesson](https://deweydex.github.io/dewlab/tutorials/web-authoring/named-grid-areas.html#other-properties-from-the-same-lesson)<br/>_used in:_ [Named grid areas — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/named-grid-areas.html#your-turn)<br/>_used in:_ [A navigation that works on a phone — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/navigation-on-a-phone.html#why-this-happens)<br/>_used in:_ [A navigation that works on a phone — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/navigation-on-a-phone.html#your-turn)<br/>_used in:_ [Position, and the sticky header — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/position-and-the-sticky-header.html#your-turn)<br/>_used in:_ [Project ideas — After Flexbox and Grid](https://deweydex.github.io/dewlab/tutorials/web-authoring/project-ideas.html#after-flexbox-and-grid)<br/>_used in:_ [Quick reference — CSS](https://deweydex.github.io/dewlab/tutorials/web-authoring/quick-reference.html#css)<br/>_used in:_ [Selectors and classes — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/selectors-and-classes.html#your-turn)<br/>_used in:_ [Text and units — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/text-and-units.html#your-turn)<br/>_used in:_ [The box — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-box.html#your-turn)<br/>_used in:_ [The container: width and centring — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-container.html#your-turn)<br/>_used in:_ [Transitions and transforms — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/transitions-and-transforms.html#your-turn)<br/>_used in:_ [Variables and colour — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/variables-and-colour.html#your-turn) |
| `WA-LO10` Test a website's functioning and fix any issues found (the descriptor's own outcome also names cross-browser testing; dewlab teaches diagnosis with a single browser's own developer tools instead) | 🟩 | [The browser inspector — Elements: the page's actual structure](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-inspector.html#elements-the-pages-actual-structure)<br/>[The browser inspector — Console: where errors show up](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-inspector.html#console-where-errors-show-up)<br/>[Troubleshooting — A page or a style doesn't look right](https://deweydex.github.io/dewlab/tutorials/web-authoring/troubleshooting.html#a-page-or-a-style-doesnt-look-right)<br/>[Troubleshooting — My code has a mistake I can't find](https://deweydex.github.io/dewlab/tutorials/web-authoring/troubleshooting.html#my-code-has-a-mistake-i-cant-find)<br/>_used in:_ [A form — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-form.html#your-turn)<br/>_used in:_ [A navigation that works on a phone — Why this happens](https://deweydex.github.io/dewlab/tutorials/web-authoring/navigation-on-a-phone.html#why-this-happens)<br/>_used in:_ [A navigation that works on a phone — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/navigation-on-a-phone.html#your-turn)<br/>_used in:_ [The browser inspector — Opening it](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-inspector.html#opening-it) |
| `WA-LO11` Recommend how a website should be upgraded, maintained and tested in future | 🟩 | [Documenting what you built — What maintenance.md is for](https://deweydex.github.io/dewlab/tutorials/web-authoring/documenting-what-you-built.html#what-maintenancemd-is-for)<br/>_used in:_ [Documenting what you built — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/documenting-what-you-built.html#your-turn) |
| `WA-LO12` Use HTML and CSS code generators and judge how well they work (dewlab teaches HTML and CSS by hand instead of a generator — not yet covered by anything in dewlab) | 🟥 | — |
| `WA-LO13` Work independently to design, build and publish webpages, without needing an ISP's own hosting (dewlab's own equivalent of the descriptor's own phrase is GitHub Pages, free and independent of any commercial host) | 🟩 | [Publish it — Turning it on](https://deweydex.github.io/dewlab/tutorials/web-authoring/publish-it.html#turning-it-on)<br/>[Publish it — Keeping it up to date](https://deweydex.github.io/dewlab/tutorials/web-authoring/publish-it.html#keeping-it-up-to-date)<br/>_used in:_ [A GitHub account — What GitHub actually does](https://deweydex.github.io/dewlab/tutorials/web-authoring/a-github-account.html#what-github-actually-does)<br/>_used in:_ [An editor — No installing anything: GitHub's own editor](https://deweydex.github.io/dewlab/tutorials/web-authoring/an-editor.html#no-installing-anything-githubs-own-editor)<br/>_used in:_ [How the pieces fit — From a change to a published page](https://deweydex.github.io/dewlab/tutorials/web-authoring/how-the-pieces-fit.html#from-a-change-to-a-published-page)<br/>_used in:_ [Publish it — Why the address looks the way it does](https://deweydex.github.io/dewlab/tutorials/web-authoring/publish-it.html#why-the-address-looks-the-way-it-does)<br/>_used in:_ [The two loops — The local loop: save and refresh](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-two-loops.html#the-local-loop-save-and-refresh)<br/>_used in:_ [The two loops — The GitHub loop: commit, push, and wait](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-two-loops.html#the-github-loop-commit-push-and-wait)<br/>_used in:_ [The two loops — Telling the two apart](https://deweydex.github.io/dewlab/tutorials/web-authoring/the-two-loops.html#telling-the-two-apart) |
| `WA-LO14` Apply the principles of good website design when building a real page or site | 🟩 | [Project ideas — Making any of them easy to read](https://deweydex.github.io/dewlab/tutorials/web-authoring/project-ideas.html#making-any-of-them-easy-to-read)<br/>_used in:_ [Documenting what you built — Your turn](https://deweydex.github.io/dewlab/tutorials/web-authoring/documenting-what-you-built.html#your-turn) |

## Vocabulary

The tutorials mark a term being introduced by putting it in italics the first time it means something particular. **107 terms** are marked that way, and asking two questions of them is free.

### Introduced more than once

The same word presented as new in two places. Either it is being introduced twice, or the two places mean different things by it — nothing here can tell which, and a person reading both decides. `index` was the second kind and cost a rewrite.

| Term | Introduced in tutorials |
|---|---|
| *building reusable tools* | 5, 23 |
| *cracking equations* | 19, 22, 23, 24, 31 |
| *drawing functions* | 24, 25, 27, 28 |
| *expressions come alive* | 20, 21, 23, 31 |
| *finding things* | 9, 15 |
| *index* | 6, 7, 18 |
| *lines and distances* | 26, 27, 28, 30 |
| *making sense of data* | 14, 25 |
| *numbers and their families* | 22, 31 |
| *parabolas* | 27, 30 |
| *pictures worth numbers* | 23, 25 |
| *see* | 17, 29 |
| *set* | 15, 21 |
| *sets as sorted lists* | 16, 17, 31 |
| *solve* | 19, 21 |
| *storing and computing* | 3, 20, 29 |
| *zahlen* | 2, 18 |

### Used before it was introduced

A word appearing in an earlier tutorial than the one that stops to explain it. Some are ordinary English doing ordinary work and can be ignored; the rest are places a student met a term as though they already knew it.

| Term | First appears in | Introduced in |
|---|---:|---:|
| *argument* | 5 | 7 |
| *before* | 1 | 3 |
| *between* | 2 | 28 |
| *counting carefully* | 11 | 12 |
| *design* | 8 | 10 |
| *drawing functions* | 23 | 24 |
| *equation* | 15 | 19 |
| *expression* | 1 | 19 |
| *expressions come alive* | 19 | 20 |
| *finding things* | 8 | 9 |
| *first steps* | 1 | 31 |
| *function* | 2 | 23 |
| *functions* | 2 | 7 |
| *how* | 2 | 3 |
| *independent* | 10 | 12 |
| *inside* | 4 | 28 |
| *lines and distances* | 23 | 26 |
| *local* | 8 | 30 |
| *logic and truth* | 16 | 17 |
| *making decisions* | 4 | 16 |
| *making sense of data* | 13 | 14 |
| *numbers and their families* | 18 | 22 |
| *opposite* | 22 | 28 |
| *parabolas* | 24 | 27 |
| *parameters* | 7 | 10 |
| *pictures worth numbers* | 14 | 23 |
| *power* | 2 | 18 |
| *putting things in order* | 9 | 15 |
| *reaches* | 5 | 29 |
| *repeating yourself* | 6 | 11 |
| *repetition* | 4 | 11 |
| *representation* | 2 | 19 |
| *return values* | 7 | 10 |
| *see* | 1 | 17 |
| *set* | 1 | 15 |
| *sets as sorted lists* | 15 | 16 |
| *solve* | 7 | 19 |
| *storing and computing* | 2 | 3 |
| *the unit circle* | 25 | 28 |
| *tools* | 3 | 10 |
| *what* | 1 | 3 |
| *wrong* | 1 | 26 |

## Scope questions, settled

Kept rather than deleted: a decision is worth as much as the question it answered, and the next person to wonder will wonder the same thing.

- **MIT-4.4, MIT-4.9 — Pythagoras and right-triangle trigonometry** — In scope in full.
- **MIT-4.5, MIT-4.6 — radians and the unit circle** — In scope in full.
- **MIT-4.1, MIT-4.2, MIT-4.3 — coordinate geometry** — In scope in full.
- **Expansion scope** — Modularity and comprehensive coverage are prioritized; additional focused tutorials are preferred over congested composite units.
