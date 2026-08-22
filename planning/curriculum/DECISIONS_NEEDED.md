# Decisions needed before Phase 6

Six questions. Each blocks a specific piece of writing, each has a
recommendation, and each ends with the form of words that would settle it.

They are worth answering in the order given: 1 to 3 decide what two of the
outlines contain, 4 and 5 decide where things go, 6 is cheap and independent.

---

## First, a finding that changes all of them

I went looking in `everlearning` for material to reuse and found rather more
than expected. `PDP_MIT_2026_2027_Integrated/LearningOutcomes/MIT/` holds **seven
finished worksheets, 3,072 lines and 486 problems, every one with an answer
key** — and they cover almost exactly the gaps the curriculum map found:

| Worksheet | Lines | Problems | Covers |
|---|---:|---:|---|
| `MIT-3.2_3.4_Quadratic-Graphing-and-Completing-the-Square.md` | 564 | 68 | `MIT-3.2`, `MIT-3.4` |
| `MIT-3.3_Graphing-Sine-and-Cosine.md` | 572 | 82 | `MIT-3.3` |
| `MIT-3.6_Derivatives-Integrals-and-Inverse-Operations.md` | 512 | 82 | `MIT-3.6` |
| `MIT-3.7_Product-Quotient-Chain-Rule.md` | 367 | 74 | `MIT-3.7` |
| `MIT-4.1-4.3_Coordinate-Geometry.md` | 247 | 48 | `MIT-4.1`–`4.3` |
| `MIT-4.4_4.9_Right-Triangle-Trigonometry.md` | 386 | 62 | `MIT-4.4`, `MIT-4.9` |
| `MIT-4.5-4.7_Radians-and-the-Unit-Circle.md` | 424 | 70 | `MIT-4.5`–`4.7` |

So the real question underneath every decision below is not *"is this worth
writing?"* but **"is this worth converting, and what do we cut from it?"** — a
much cheaper question, and one where saying yes costs a fraction of what I
assumed when I wrote the outlines.

Two caveats. They are pen-and-paper worksheets: problems and answers, no
runnable code, so converting means adding the cells that justify dewlab as the
format rather than a PDF. And they were written to the descriptor rather than to
your scope decisions, so several contain material you have already ruled out —
which is what makes questions 1 to 3 answerable in terms of specific parts.

---

## 1. Right-triangle trigonometry — `MIT-4.4`, `MIT-4.9`

### The question

You ruled out "trigonometry beyond basic graphing and the sine/cosine rule".
Does that sentence also exclude Pythagoras and SOH-CAH-TOA, or are those the
foothold the two rules stand on?

I have read it both ways and cannot tell, so it is counted as a gap until you
say.

### What is at stake

`MIT-4.4_4.9_Right-Triangle-Trigonometry.md`: 386 lines, 62 problems, four
parts — the three ratios (20), finding missing sides (16), finding missing
angles (12), angles of elevation and depression (14). All four are within the
outcome as written.

The pedagogical argument is about the Sine and Cosine Rules, which you *have*
kept. Those rules are most naturally taught as **"what you reach for when the
triangle is not right-angled"** — which is a sentence that only means anything
to a student who has just done the right-angled case. Without it, the two rules
arrive as formulae to memorise, which is the thing the exclusions exist to
avoid.

Against that: students meet SOH-CAH-TOA at Junior Cycle. You may reasonably
judge it revision rather than teaching, and revision is not what these tutorials
are for.

### Options

- **(a) Keep both, in full.** Section 0 of Angles and Waves. Adds perhaps a
  third to that tutorial.
- **(b) Keep as a short recap, not an outcome.** Half a section, no exercises,
  purely to set up the two rules. `MIT-4.4` and `MIT-4.9` stay marked as gaps,
  honestly.
- **(c) Exclude both.** The two rules are taught cold.

### Recommendation

**(a).** Angles and Waves is the thinner of the two big tutorials, this material
already exists with an answer key, and the elevation-and-depression problems
(Part D) are the only genuinely applied trigonometry in the whole set — a ladder
against a wall, a surveyor and a hill. That is the part students remember.

### To settle it

> "Keep 4.4 and 4.9 in full / as a recap only / drop them."

---

## 2. Radians — `MIT-4.5`, `MIT-4.6`

### The question

Three parts, and they can be answered separately.

**2a.** Radians, or degrees only? Graphing sine and cosine needs an x-axis and
that axis is conventionally in radians. But `math.sin` takes radians whatever we
teach, so degrees-only means every cell carries a conversion the students do not
understand.

**2b.** If radians: the whole of `MIT-4.5`/`4.6`, or the minimum the graphs
need? The worksheet's Part C includes a **special-angles table in surd form** —
that is `MIT-4.7`, which you have already excluded. So Part C either gets cut or
gets rewritten in decimals.

**2c.** The same worksheet ends with the **Pythagorean identity**
(sin²θ + cos²θ = 1). Your exclusion says "identities... are not". Does that catch
this one? It is arguably not an identity to manipulate but the observation that
the unit circle has radius 1 — which is the definition the whole tutorial is
built on, and one line of code can demonstrate it.

### What is at stake

`MIT-4.5-4.7_Radians-and-the-Unit-Circle.md`: 424 lines, 70 problems. Part A
degrees and radians (20), Part B arc length (12), Part C the unit circle (24,
including the surd table), plus the identity.

### Recommendation

**2a: radians, taught properly.** The conversion problem does not go away, it
just moves somewhere the students cannot see it — and "a radian is how far you
have walked round the circle" is a genuinely good idea that takes one cell.

**2b: Parts A and B in full, Part C rewritten in decimals.** The unit circle
matters; memorising √3/2 does not, and you have already said so.

**2c: keep it, as one cell, not as a topic.** Walk a point round the circle,
square the two coordinates, add them, get 1 every time. That is the unit circle
proving something about itself, and it is thirty seconds.

### To settle it

> "2a: radians / degrees only. 2b: Parts A and B, C in decimals / something
> else. 2c: keep the identity as a cell / drop it."

---

## 3. Coordinate geometry — `MIT-4.1`, `MIT-4.2`, `MIT-4.3`

### The question

You did not mention it either way. Does it come into Drawing Functions, or is it
out?

### What is at stake

`MIT-4.1-4.3_Coordinate-Geometry.md`: 247 lines, 48 problems — the smallest of
the seven worksheets, and **half of it is already redundant**:

- Part A, coordinate basics (10 problems) — new, and needed.
- Part B, vectors (12) — **not in either descriptor**. Cut.
- Part C, slope and linear equations (14) — new, and needed.
- Part D, systems of linear equations (12) — **already taught** in Tutorial 15's
  Simultaneous Equations section. Cut.

So the actual new material is 24 problems, and it lands in a tutorial that is
being written anyway. Drawing Functions has a Straight Lines section whether or
not you keep these outcomes; keeping them means that section computes slope and
midpoint rather than only drawing.

This is also the one part of Section 4 the *programming* half of the course uses
directly — distance between two points turns up in every graphics or
game-flavoured exercise the students are likely to meet.

### Options

- **(a) Fold into Drawing Functions' Straight Lines section.** Three outcomes for
  roughly half a section.
- **(b) Its own short tutorial.** Cleaner mapping, one more thing in the series.
- **(c) Out of scope.** Three outcomes stay red.

### Recommendation

**(a).** It is the cheapest three outcomes on the entire list and it makes a
section that already exists do more work. The cost is that Drawing Functions
grows, which question 4 addresses.

### To settle it

> "Fold 4.1–4.3 into Drawing Functions / give them their own tutorial / leave
> them out."

---

## 4. Tutorial 15, and how big Drawing Functions gets

### The question

Two parts, and they interact.

**4a.** Tutorial 15's quadratic section currently stops at *"if the discriminant
is negative: no real roots"* — the pseudocode literally says
`RETURN () or a message indicating no real roots`. Two of the outlines want to
change that:

- `complex-roots.md` proposes a **new short tutorial** picking up where 15 stops.
- The completing-the-square section of `drawing-functions.md` takes material
  that arguably belongs in 15 too.

Do we **revise Tutorial 15** to include both, or **leave it and build outward**?

**4b.** Drawing Functions as outlined has six sections and would grow further if
you keep coordinate geometry (question 3). Is it **one tutorial or two** —
straight lines and curves, then solving and inverses?

### What is at stake

Revising 15 means editing a tutorial students may already have downloaded, which
is exactly the case the version-and-progress design exists to handle: bump
`version`, and a student's saved work is compared against it and flagged rather
than silently mismatched. So it is safe. It is not free, though — the
downloadable copy changes, and anyone holding the old file has an old file.

Leaving it means Tutorial 15 permanently contains a sentence that is not true,
with the correction three tutorials later.

### Recommendation

**4a: leave Tutorial 15 alone and write the short tutorial.** Not because
revising is risky but because *"you were told there was no answer, and there
is"* is a better lesson than never having been told. The cliff edge is
pedagogically useful, and the new tutorial also completes Tutorial 13's tour of
the number domains, which a revision to 15 would not. Completing the square
stays in Drawing Functions, where its payoff — the vertex — is a fact about the
graph.

**4b: two tutorials.** Drawing Functions is carrying `MIT-3.1`, `3.2`, `3.4` and
possibly `4.1`–`4.3`: five to six outcomes and 116 problems' worth of source
material. That is two sittings by any measure, and the natural seam is between
drawing a function and reading answers off it.

### To settle it

> "4a: leave 15 as it is and write the new tutorial / revise 15 instead.
> 4b: split Drawing Functions in two / keep it as one."

---

## 5. Numbering and placement

### The question

The proposals do not sit neatly on the end. Two want to go near the **front**
(How We Got Here after Tutorial 1; When It Goes Wrong after Tutorial 3) and the
maths cluster wants to go after Tutorial 15.

Three parts:

**5a.** Do the two PDP conversions go where they teach best (early), or on the
end where they cost nothing?

**5b.** If anything is inserted, what happens to the numbering?

**5c.** Is this the moment to stop numbering tutorials in their titles
altogether?

### What is at stake — measured

I counted. Inserting a tutorial before the end costs:

- **50 prose references by number** across the tutorials — "your functions from
  Tutorial 11", "the evaluator from Tutorial 14". Every one after the insertion
  point is wrong.
- **17 titles and 17 slugs** carrying their number.
- **17 published URLs**, and any downloaded file a student is holding, since the
  filename is the slug.
- Only **three** cross-links use the `tutorial:slug` syntax the build validates
  — so the build would catch almost none of this. The rest is prose, and prose
  is invisible to the checker.

That last point is the one that matters. Renumbering is not a rename; it is a
50-place edit that nothing verifies.

Note that `order:` in the frontmatter is what actually sequences the series —
the number in the title is decoration the build never reads. So placement and
numbering are **separable decisions**, which is what makes 5c possible.

### Options for 5b

- **(a) Renumber everything.** Correct, and 50 prose edits with no safety net.
- **(b) Insert without renumbering** — "Tutorial 3a". Ugly, honest, cheap.
- **(c) Append everything.** Free, and puts error-reading at tutorial 20 when
  students need it at 3.

### Recommendation

**5c: drop the numbers from the titles, and then 5a becomes free.**

The numbers are doing less work than they look. Navigation is previous/next, the
contents page is ordered, and `order:` sequences the series regardless. What the
numbers actually buy is the ability to write "Tutorial 11" in prose — and those
50 references would read better as *"the statistics functions you wrote"*
anyway, which is what a student remembers. The tutorial they remember is
"Cracking Equations", not "15".

That is a one-off edit of comparable size to a single renumbering, and it is the
last one ever needed: after it, a tutorial can be inserted anywhere by setting
`order:`, and nothing else changes.

If that is too much upheaval, **(c), append everything** — and accept that
When It Goes Wrong arrives late.

### To settle it

> "5c: drop the numbers / keep them. If keeping: 5a and 5b — insert and
> renumber / insert as 3a / append everything."

---

## 6. What the calculus tutorial actually contains

### The question

Cheap and independent of the rest. Your exclusion of the chain and quotient
rules cuts deeply into one of the two calculus worksheets, and I want to check
the cut is where you meant it.

`MIT-3.7_Product-Quotient-Chain-Rule.md`, 74 problems:

| Part | Problems | In or out |
|---|---:|---|
| A — Product rule | 12 | **In** |
| B — Integration by parts | 10 | Out (beyond polynomials) |
| C — Quotient rule | 10 | Out (your exclusion) |
| D — Chain rule | 16 | Out (your exclusion) |
| E — Substitution | 16 | Out (reverses the chain rule) |
| F — Combining everything | 10 | Out (combines the excluded) |

**62 of 74 problems fall away.** Twelve survive.

The other worksheet fares very differently.
`MIT-3.6_Derivatives-Integrals-and-Inverse-Operations.md`, 82 problems, is
**entirely within scope** — power rule both directions, the constant of
integration, constants and sums, polynomials complete, intuition, and a
Fundamental Theorem preview. Not one part needs cutting. It is a near-exact match
for the Rates of Change outline.

### What this means

Rates of Change is really the 3.6 worksheet plus twelve problems. That is
a *good* outcome — it is the best-matched source material of the seven — but it
does mean `MIT-3.7` ends up marked "taught in part" on the strength of the
product rule alone.

### Recommendation

**Accept it, and say so in the tutorial.** One honest sentence — *"there are two
more rules, for functions inside functions and for one function divided by
another; you will meet them if you go further"* — costs nothing and stops a
student who has seen the chain rule elsewhere thinking they have missed
something.

The alternative is keeping the chain rule (Part D, 16 problems), which is the
one exclusion I would gently push back on: it is the rule that makes the others
useful, and it is the only one of the three that turns up in the machine-learning
material in the other repositories.

### To settle it

> "Product rule only, with a note / add the chain rule back in."

---

## 7. Splitting Tutorial 13, and where the foundations sit

Added after the first six, from your read of 13 and 14. `CURRICULUM_NOTES.md`
has the full working; this is the decision.

### The question

**7a.** Tutorial 13 holds three unrelated topics — number domains (set theory),
powers and logarithms (algebra), and area and volume formulas (mensuration).
Split it into three and place each where it is needed?

**7b.** Tutorial 14 is not a mishmash — it is polynomials, done properly, in one
arc. Split it anyway, or leave it as one and possibly move it?

### What is at stake

Tutorial 2, at *Data Types*, already tells students that `int` corresponds to ℤ
and `float` approximates ℝ. Tutorial 13 then teaches ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ properly,
with a `classify_number` exercise, **eleven tutorials later**. The shallow
version arrives first and the real one arrives long after anybody needs it.

More broadly, MIT Section 1 is the *basic arithmetic and algebra*, and dewlab
teaches it at positions 13 to 15 — after counting and probability (9, 10) and
statistics (11, 12) have already leaned on powers, roots and factorials. That
ordering came from the source notebooks' numbering rather than from a decision
anybody made.

### Recommendation

**7a: yes, three ways.**

| Piece | Where it should go | Why |
|---|---|---|
| Number domains | Into Tutorial 2, or immediately after | Same idea as `int` versus `float`, which Tutorial 2 is already half-teaching |
| Powers and logarithms | Before Tutorial 9, expanded to a full tutorial | Powers and roots are what counting, standard deviation and polynomials all assume |
| Practical geometry | After functions are introduced (5 or 8) | "A formula is a function" is the best first use of a function there is |

**7b: leave 14 as one.** It is the most coherent tutorial in the series. It
follows the powers tutorial naturally and still precedes 15, so whether it
moves depends on whether powers moves — not on anything about 14.

### The catch

Every one of these moves renumbers everything after it, and doing this *as well
as* inserting the new maths tutorials means two renumberings — 50 unchecked
prose references each time (question 5). This is the clearest case yet for
dropping the numbers: the reordering is worth doing on its own merits, and the
numbering is the only thing making it expensive.

### To settle it

> "7a: split 13 three ways as proposed / differently / leave it.
> 7b: leave 14 as one / split it too."

---

## Summary

| # | Question | Recommendation |
|---|---|---|
| 1 | Right-triangle trig | Keep in full, as section 0 of Angles and Waves |
| 2 | Radians | Radians; Parts A and B whole, C in decimals; keep the identity as one cell |
| 3 | Coordinate geometry | Fold into Drawing Functions |
| 4 | Tutorial 15 / tutorial size | Leave 15, write the short tutorial; split Drawing Functions in two |
| 5 | Numbering | Drop the numbers from titles, then place freely |
| 6 | Calculus scope | Product rule only, with an honest note — but consider keeping the chain rule |
| 7 | Tutorial 13 and the ordering | Split 13 three ways, each placed where it is needed; leave 14 as one |

Answering 1, 2, 3 and 6 unblocks all the writing. 4, 5 and 7 can follow later
without stalling anything — though 7 sharpens the case for 5.
