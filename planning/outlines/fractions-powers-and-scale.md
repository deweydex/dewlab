# Outline — The Fractions, Powers and Scale Series

**Status:** proposed, not yet written. No tutorial below exists.
**Kind:** a review series. It is the mathematics most of the other series
assume a reader already has: fraction arithmetic, reciprocals, powers
(positive, negative, fractional), logarithms, scientific notation, and
drawing things on a scale that fits them.
**Closes:** nothing new on the outcome map. `MIT-1.1` (operations in N, Z,
Q, R; powers and logarithms) and `MIT-1.7` (rational algebraic expressions)
are both marked covered already. What this series fills is the layer under
those codes, where the survey below found the gaps.
**Attaches to:** `numbers-and-their-families` and `doubling-and-halving`
(powers and logarithms), `running-a-formula-backwards` and
`rearranging-formulae` (fractions with letters in them), `drawing-functions`
and `pictures-worth-numbers` (charts), `how-a-computer-stores-a-number`
(e-notation).

## Why this exists

Every one of these skills is touched somewhere, and none is taught slowly
anywhere. A survey of the site (2026-09) found:

| Skill | Where it lives now |
|---|---|
| Adding, subtracting, multiplying and dividing fractions | Only on `numbers-and-their-families-practice` (with `Fraction`). No tutorial teaches it. |
| Reciprocals | One row of the powers table in `numbers-and-their-families`, as the meaning of `a**-n`. |
| Fractions with letters | The last section of `running-a-formula-backwards`, and `rearranging-formulae` §3. |
| Negative exponents | `numbers-and-their-families`, as a rule in a table. |
| Fractional exponents and roots as powers | One practice question (`16**(1/2)`, `8**(2/3)`). Not taught. |
| Logarithms | `numbers-and-their-families` and `doubling-and-halving` (as "how many halvings"). |
| Scientific notation | "Reading e-16" in `how-a-computer-stores-a-number`, which no course lists. |
| Orders of magnitude, estimation | Nowhere. |
| Log scales on a chart | One `set_xscale("log")` in `approaching-a-limit`, and `pictures-worth-numbers-practice`. |

A reader who arrives unsure of fractions meets them first as a rule in a
table, at speed, inside a page about something else. That works for a
reader who needs reminding. It does not work for a reader who never had the
idea, and the course descriptors assume both kinds.

The series also has material waiting for it. The fraction worksheets in
`deweydex/everlearning` (`Maths Stuff/Worksheets/worksheet_01*.md`,
especially 1B, *Fractions in the Wild*) and the Grade 8 sequence
*An introduction to Scientific Notation and Scale* (`Maths Stuff/Grade 8
Scientific Notation/`, four sheets) were written for this ground, and the
Grade 8 sequence was building towards the Drake equation. Its fourth sheet
ends: "This will help us tomorrow when we look at the Drake Equation." The
fifth sheet is not in the repository. This series is, in part, that fifth
sheet.

## The spine: equations that multiply fractions together

The Drake equation (1961) is a chain of fractions:

$$N = R_* \cdot f_p \cdot n_e \cdot f_l \cdot f_i \cdot f_c \cdot L$$

Stars born per year, times the fraction with planets, times the number of
habitable planets per system, times the fraction where life starts, where
it becomes intelligent, where it builds a radio, times how long it keeps
transmitting. Each factor narrows the count down. It is the best example we
have of *multiplying by a fraction makes a number smaller*, and of why the
order of multiplication does not matter.

Its descendants each teach something different, which is why the series
can return to it rather than using it once:

| Equation | What it changes | What it teaches here |
|---|---|---|
| **Drake** (1961) | the original | multiplying fractions; each factor narrows |
| **Seager** (2013): $N = N_* F_Q F_{HZ} F_O F_L F_S$ | counts planets with detectable biosignature gases in a real survey, not civilisations | the same shape, but every factor is something a telescope could measure; answer is small (Seager's own estimate was a handful) |
| **Frank & Sullivan** (2016), the "archaeological form": $A = N_{ast} \cdot f_{bt}$ | asks whether any other technological species has *ever* arisen, and drops $L$ | a reciprocal. Set $A = 1$ and solve: $f_{bt} = 1 / N_{ast}$. For the Milky Way, $N_{ast} \approx 6 \times 10^{10}$, so $f_{bt} \approx 1.7 \times 10^{-11}$, "one in 60 billion". For the observable universe, $2.5 \times 10^{-22}$. Their "pessimism line" |
| **Sandberg, Drexler & Ord** (2018), *Dissolving the Fermi paradox* | replaces each factor's single value with a range spanning orders of magnitude, and samples | logarithms and log scales. Each range is log-uniform (e.g. $f_i$ from $10^{-3}$ to $1$). The median result is below one; the mean is far larger. Roughly even odds we are alone in the galaxy (check the paper's own figures before quoting) |
| **Westby & Conselice** (2020), the "Astrobiological Copernican limit" | assumes intelligence takes about 5 billion years wherever it arises | a confident-looking answer (at least 36 communicating civilisations, nearest perhaps 17,000 light-years) built from stated assumptions; good for "which factor did they fix, and why" |
| **Backus** (2010), *Why I don't have a girlfriend* | applies the chain to meeting a partner in London | the same arithmetic on a human scale; ends at 26 people in the UK, a 1 in 285,000 chance on a night out. Teacher's call: the "attractive" factor makes it awkward in some rooms, and the same page can be rebuilt as "how many people in Dublin could be your study partner" |

Sources: Frank & Sullivan, *Astrobiology* 16(5), 2016 (arXiv:1510.08837;
the galaxy and universe figures are its Table 1). Sandberg, Drexler & Ord,
arXiv:1806.02404. Westby & Conselice, *ApJ* 896:58, 2020
(arXiv:2004.03968). Seager's equation: her 2013 proposal, written up as
"The search for habitable planets with biosignature gases framed by a
'Biosignature Drake Equation'" (*Int. J. Astrobiology*, 2018). Backus:
University of Warwick, 2010.

## Worlds

The series offers the usual worlds (`PEDAGOGICAL_STYLE_GUIDE.md#choice-of-world`).
Planets carries the Drake spine. The others each have their own chain of
fractions and their own scale:

- **Planets.** Drake and its descendants; Kepler's third law with NASA's
  planetary fact sheet; light-minutes, AU, Voyager.
- **The sea floor.** Of every ship ever built, the fraction that sank, the
  fraction in water shallow enough to reach, the fraction found. Pressure
  doubling with depth; a sunlight fraction that halves every few metres.
- **Pixel art.** Megapixels and bytes; a compression ratio (worksheet 1B,
  Q10) as a fraction; 8-bit colour as $2^8$ and 24-bit as $2^{24}$.
- **Ciphers.** Egyptian fractions (the Rhind papyrus writes $2/5$ as
  $1/3 + 1/15$); key spaces as powers ($26!$, $2^{128}$) and their
  logarithms as "how many digits".
- **Games.** Drop rates as "one in how many"; expected tries as $1/p$
  (worksheet 1B, Q25); experience curves that grow by a power.

## The shape — eight tutorials, a closer look, a making task, a mixed set

Each tutorial is one sitting. The order is fractions, then powers, then the
two that need both (logarithms and log scales). A reader who is only
unsure of powers can start at 5.

### 1. Multiplying fractions: narrowing it down

*Id:* `narrowing-it-down`. *World:* planets.

Opens with a cell that multiplies seven numbers and prints an answer, the
Drake equation with Drake's own 1961 values, before anything is named. The
reader is asked to guess which factor matters most, in writing, and then to
change one factor at a time and see. The finding comes before the word:
every factor below one made the answer smaller, and the order the reader
changed them in did not matter. Then name it: multiplying fractions, tops
together and bottoms together, and `fractions.Fraction` to check by hand
work exactly.

Then the Seager equation: same shape, but every factor is one a telescope
could measure. The reader fills in a completed version with one factor
missing.

Your turn, in the reader's world: a chain of their own, three factors long.

### 2. Adding fractions: parts of different wholes

*Id:* `parts-of-different-wholes`. *World:* ciphers (Egyptian fractions).

Opens with the Rhind papyrus writing $2/5$ as $1/3 + 1/15$, and a cell
that checks it with `Fraction`. Why would anyone write a fraction as a sum
of unit fractions? The reader tries to find one for $3/7$, by hand, before
seeing the greedy method as a loop. Adding is where a common denominator
earns its place: the reader meets it as the thing the loop had to do.

Then the pattern sums from worksheet 1A (Part B): $1 + 1/2 + 1/4 + \dots$
and $\frac{1}{1\cdot2} + \frac{1}{2\cdot3} + \dots$, run in a loop, with a
prediction of where each total is heading. Points forward to
`getting-closer` without teaching limits.

Last section, with letters: $1/m + 1/n$, and the parallel-resistance or
lens formula (worksheet 1A, Q40). Links to `running-a-formula-backwards`
rather than repeating it.

### 3. Reciprocals and dividing: one in how many?

*Id:* `one-in-how-many`. *World:* planets, then games.

Opens with Frank and Sullivan's question: how rare would a technological
species have to be for us to be the only one ever? The reader has the
number of habitable-zone planets in the galaxy ($6 \times 10^{10}$) and
sets the count to one. The answer is a reciprocal, and "one in 60 billion"
is how a person says it.

Then dividing by a fraction as multiplying by its reciprocal, found by
running both in a cell and noticing they agree, then asked why. Expected
tries as $1/p$ (a 1 in 6 chance takes 6 tries on average) in the games
world. What $1/0$ does in Python, and why the algebra warned about it.

### 4. When the bottom gets small: fractions in the wild

*Id:* `when-the-bottom-gets-small`. *World:* planets (relativity), then
the reader's choice.

This is worksheet 1B made runnable. Its note to students ("You don't need
to understand what these formulas do in their original context... Keep
calm. These are just fractions.") is the page's stance. The Lorentz factor
opens it:

$$\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$$

The reader predicts what happens to $\gamma$ as $v$ approaches $c$, then
runs a table of speeds, then plots it. The bottom goes to zero, so the
whole thing grows without limit. Time dilation and relativistic energy are
the same fraction pattern. Then a short tour, one cell each, of fractions
whose behaviour matters more than their meaning: the sigmoid, learning-rate
decay, precision and recall, the F1 score as a harmonic mean, and the
Bayes medical-test result where a rare disease keeps the answer small.

The risk is length. Worksheet 1B has 28 questions; the page takes four or
five and leaves the rest to its practice page.

### 5. Powers of ten: from a virus to Voyager

*Id:* `powers-of-ten`. *World:* planets, then the reader's choice.

Grade 8 sheets 1 to 4, compressed into one page. The reader discovers
$10^a \cdot 10^b = 10^{a+b}$ and $(10^a)^b = 10^{ab}$ by running cases,
then meets the sheet's key question: what goes in the gap in
$10^a \cdot 10^{?} = 10^0 = 1$? Negative exponents come out of that, with
the sheet's own warning before the reveal. Then scientific notation, and
Python's `1.5e11` and `f"{x:.2e}"`.

The problems are the sheets' problems, and they are the reason the page
exists: the Earth's volume and mass from its radius and density; how many
20 nm viruses fit on a full stop; how many caesium atoms make a tennis
ball; how long the Sun's light takes to arrive; how far Voyager 1 is. Two
updates are needed. Voyager 1 is no longer 117 AU away; it is near 170 AU
in 2026 and reaches one light-day from Earth (about $2.59 \times 10^{10}$
km) on 18 November 2026, which is a better hook than any number on the
sheet. NASA's "Where are Voyager 1 and 2 now?" page has the live figure. The comic panels on the sheets cannot be reused.

### 6. Fractional exponents: halfway between powers

*Id:* `halfway-between-powers`. *World:* planets.

Sheet 1, question 1(e) is the opening, unchanged: what is
$10^{1/2} \cdot 10^{1/2}$? The rule the reader found on page 5 says
$10^1$, so $10^{1/2}$ has to be the square root of 10. The reader checks
with `10**0.5`. Then $x^{1/3}$, $x^{2/3}$ and negative fractional powers.

Then the planets: Kepler's third law with NASA's fact-sheet data. A
planet's year, in Earth years, is its distance from the Sun, in AU, to the
power $3/2$. The reader computes it for all eight planets and compares
with the real figures. Half-life as $(1/2)^{t/T}$ and $(1 + 1/n)^n$
approaching $e$ (worksheet 1B, Part E) as the reader's-choice tasks.

### 7. Logarithms: counting the zeros

*Id:* `counting-the-zeros`. *World:* planets.

$\log_{10}$ first as "how many zeros", the order of magnitude, before it
is anything else. Then the property that makes it useful: the logarithm
of a product is the sum of the logarithms. The Drake equation, taken to
logarithms, becomes a sum of exponents, and the reader can see which
factor moves the answer by how many powers of ten.

Then Sandberg, Drexler and Ord. Each factor becomes a range several powers
of ten wide, sampled evenly *in its logarithm*. The reader runs ten
thousand Drake equations, and the median and the mean disagree by orders
of magnitude. Which one answers "are we alone?" This half reuses the
Monte Carlo loop from `counting-darts`, and should link to it rather than
teach it again.

Overlap: `numbers-and-their-families` defines logarithms as the inverse of
powers, and `doubling-and-halving` teaches $\log_2$. This page must link
to both. It is the slower route to the same place, not a second version of
it.

### 8. Log scales: drawing things that differ by millions

*Id:* `drawing-across-scales`. *World:* planets, then the reader's choice.

Opens with a bar chart of the planets' distances on an ordinary axis:
Mercury, Venus, Earth and Mars crowd together in one corner. The reader
switches to `set_yscale("log")` and the picture opens out. Then log–log:
Kepler's periods against distances fall on a straight line, and its slope
is the $3/2$ from page 6. Then the Monte Carlo results from page 7 as a
histogram, useless on a linear axis and readable on a log one. The page
ends with a scale strip from a virus to the observable universe, each tick
a power of ten.

The chart conventions come from `docs/` and the dataviz practice already
on the site; the page teaches the reading of a log axis, and what zero does
to one.

### Closer look: does multiplying always make a number bigger?

*Id:* `does-multiplying-make-it-bigger`.

The misconception a Drake chain collides with. Both ideas predict an
answer for $40 \times 0.5$ and $40 \times 1.5$; only one matches. Then why
the idea is so natural to hold: every multiplication a reader met before
fractions made a number bigger. Place it after tutorial 1.

### Making task: your own Drake equation

*Id:* `your-own-drake-equation`.

The reader writes a Drake-style estimate for something nobody has counted,
in their world: wrecks on the sea floor that could still be found, players
who will ever reach the top rank, how many 128-bit keys could be tried
before the Sun burns out. It needs a chain of fractions (1–3), numbers in
scientific notation (5), a range for each factor sampled on a log scale
(7), and a chart that can show the spread (8). Judged by reflection
questions only: which factor are you least sure of, and how much would the
answer move if you were wrong about it by a factor of ten?

### Mixed set

*Id:* `mixed-fractions-powers-and-scale`. Draws on all eight, plus two or
three problems from `numbers-and-their-families` and
`running-a-formula-backwards` (`PEDAGOGICAL_STYLE_GUIDE.md#nothing-taught-once`).
Worksheets 1A and 1B supply most of it.

## Where it goes

Not decided. Two options, and they are not exclusive:

- **In `mit-pdp-maths-prog-integration`**, as a series before *Algebra and
  Functions*. Then `numbers-and-their-families` becomes the fast recap for
  a reader who did not need this series, and its powers table can point
  back here.
- **In `dewey-track`**, between *Instructions for a machine* and *Making
  your own tools*, where `running-a-formula-backwards` first needs
  fractions.

Either way the tutorials should exist once and be listed by whichever
courses want them, the way `running-a-formula-backwards` is shared now.

## What this series deliberately does not do

- **No new algebra pages.** Fractions with letters, transposition and
  expanding brackets are taught in `running-a-formula-backwards`,
  `rearranging-formulae` and `rules-with-letters-in-them`. Pages 2 and 3
  end by linking there.
- **No claim that any Drake result is right.** Every estimate in the
  series is presented with the assumption it depends on. The point of the
  descendants is that the same arithmetic gives answers from "alone" to
  "dozens", and the arithmetic is not where the disagreement lives.
- **No teaching of limits.** Pages 2 and 4 approach them and stop, and
  link to `getting-closer`.
- **No `numpy` before page 7**, and there only for sampling.

## Before writing

- Read the everlearning sources above; they are the first draft of most
  cells and nearly every practice problem.
- Check every figure quoted from a paper against the paper, and date the
  ones that move (Voyager's distance, exoplanet counts).
- The ids above are proposals. Once a page has been in front of a class
  its id is the key a reader's saved work lives under, so settle them
  before the first page ships.
