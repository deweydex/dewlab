# Outline — The Zen of Slashes and Surds

**Status:** in progress. The pilot pages are written: `before-we-start`,
`one-whole-many-slices`, `same-amount-different-names` and `the-long-way`,
each with its practice page. The rest below is planned.
**Kind:** a module of its own (`courses/zen-of-slashes-and-surds.yaml`),
for readers who struggle with mathematics. It covers the primary and
secondary school ground that the other modules assume: fractions (the
slashes), powers, roots and logarithms (the surds, and their partners),
the first ideas of algebra, and seeing numbers as pictures and graphs.
**Closes:** nothing new on the outcome map. `MIT-1.1` (operations in N,
Z, Q, R; powers and logarithms) and `MIT-1.7` (rational algebraic
expressions) are marked covered already. This module is the ground under
those codes. No course descriptor asks for it; the readers do.
**Attaches to:** `numbers-and-their-families`, `doubling-and-halving`,
`rules-with-letters-in-them`, `running-a-formula-backwards`,
`rearranging-formulae`, `drawing-functions`. A reader who finishes this
module arrives at any of those already at ease with its first step.

## Who it is for

A reader who learned somewhere, early and firmly, that they are "not a
maths person". They can often do more than they think, but the moment a
page looks like mathematics their attention goes to the feeling, not the
page. Speed makes it worse. So do marks, and so does being shown a rule
before they have any reason to want one.

The rest of dewlab assumes a reader who is uncertain about a topic. This
module assumes a reader who is uncertain about themselves in the
subject. That changes the size of every step, how often the page stops,
and what it says when it does.

## What the module believes

These are stated to the reader on the first page, in plain words, and
returned to on every page. They extend the site's principles
(`PEDAGOGICAL_STYLE_GUIDE.md#how-learning-happens-here`); they do not
replace them.

**Fluency, not memory.** Nothing here is to be memorised. We practise a
thing until it feels ordinary, the way a road you walk every day stops
needing directions. A rule the reader can rebuild from a picture is worth
more than one they can recite, and the pages always offer the picture
again.

**A guess is the first step.** Every step starts with a guess, and a guess
that turns out different is the most useful kind
(`PEDAGOGICAL_STYLE_GUIDE.md#mistakes`). The `predict` block's "I'm not
sure yet" option is how a reader says so without shame, and it opens the
first hint straight away.

**Calm is the goal, and noticing comes first.** Curiosity and optimism
are how learning feels when it is going well. When they turn into
frustration, the reader has not failed; the step was too big. The module
teaches the reader to notice that change as a skill in its own right, and
every time it asks, it offers a route: go back one step to where it still
made sense, open the steps fold, or stop for today and come back to the
same page. Calm is what a reader practises alongside the mathematics,
and it is worth as much.

**Small steps up a mountain.** Understanding is at the top. Nobody is
asked to jump to it. Each page is a staircase of small steps, most of
them one question long, and a reader who is stuck is never more than one
step from the last place they were not stuck.

**The material checks itself.** In Montessori classrooms this is *control
of error*: the fraction pieces only fit the frame one way, so the child
sees a mistake without anyone pointing at it. dewlab already works like
this (`PEDAGOGICAL_STYLE_GUIDE.md#no-verdicts`). The picture, the cell's
output, or the page's answer behind a fold shows what happened, and nobody
says right or wrong.

### A departure from 7.229, decided in 7.254

`DECISIONS_LOG.md` 7.229 (25 September 2026) says the whole site names a
feeling *rarely*, and always with a route. This module names one more
often than that, because noticing frustration is part of what it teaches.
Every mention still carries a route, which keeps the part of 7.229 that
protects the reader. The difference is frequency and purpose: a fixed
"calm check" at the same places on every page (below), not a feeling
named in passing. `DECISIONS_LOG.md` 7.254 records the decision. The
words live once, in `setup/zen-calm-check.md`, and every page includes
them.

## Language: plainer than plain

Many readers of this module read English as a second language, and
many had trouble with reading at school as well as with maths. So the
module goes further than `PEDAGOGICAL_STYLE_GUIDE.md#plain-language`:

- **Short sentences, one idea each.** Most are under fifteen words. A
  sentence with "and", "but" and "so" in it is usually two or three.
- **Common words.** *Normal*, not *ordinary*; *scary*, not *frightening*;
  *in total*, not *altogether*; *aloud*, not *out loud*.
- **Every hard word explained where it appears**, the maths ones and the
  others: *frustrated* comes with "annoyed, tired or stuck", *Zen* with
  "a calm mind", *Python* with "a language for computers".
- **No idioms and no phrasal verbs**, even easy-looking ones: *keep in
  mind*, *saves ink*, *gives it away*, *pick up*, *work out*.
- **Lists instead of long sentences** when a sentence has three or more
  parts, as in "here are some ideas" at the end of a practice page.
- **One gap per line** in a fill-in-the-blank question, with a blank line
  between sentences, so each gap reads as its own small step.

## How the ideas are shown

### Concrete, then pictures, then symbols

Each idea arrives first as something to handle, then as a picture, then
as symbols. This order comes from Bruner's enactive, iconic and symbolic
stages, and from the concrete-pictorial-abstract sequence that Singapore
mathematics built on them. Montessori materials are the model for the
concrete end, rebuilt as pictures and as cells a reader can change:

| Material | What it becomes here |
|---|---|
| Fraction circles (the Montessori fraction insets): one whole cut into 2, 3, … 10 equal pieces | **A pizza cut into *n* slices.** One whole, *n* slices of $1/n$ each; eat all *n* and you have eaten 1. A cell `draw_pizza(slices=8, shaded=3)` the reader can change. |
| Fraction strips: bars of the same length cut into halves, thirds, quarters | **A fraction wall.** Same length, different cuts, so $2/4$ and $1/2$ are seen to be the same size before they are called equal. |
| The golden beads: a unit, a ten-bar, a hundred-square, a thousand-cube | **Powers of ten as shapes.** A bead, a line, a square, a cube: $10^0$, $10^1$, $10^2$, $10^3$. The exponent counts the directions it spreads in, and what comes after the cube is the first real question. |
| Folding paper in half, again and again | **Powers of two, and halves of halves.** Each fold doubles the layers and halves the area, so $2^n$ and $(1/2)^n$ are one experiment seen from two sides. |
| A balance with the same weight on each side | **An equation.** Whatever we do to one side we do to the other, and it stays level. |

Pictures are SVG files in each tutorial's folder, drawn by a small script
in `dev/` so the whole module has one style. Each carries real alt text
(the build refuses an image without it; see
`docs/WRITING_TUTORIALS.md`, *Images*), and each must read in both the
light and the dark theme.

### Squiggles, letters, numbers: the same shape three ways

A reader who panics at $a^m \cdot a^n$ can often see the same pattern
without trouble when it is made of shapes:

$$\heartsuit^{\triangle} \cdot \heartsuit^{\square} = \heartsuit^{\triangle + \square}$$

The squiggles say: *it does not matter what is in the holes, look at the
shape.* Letters say the same thing in the form every later page uses, and
numbers make it something to check. The module offers all three for the
same problems, and the reader chooses.

The site already has the mechanism for that choice: **worlds**
(`docs/WRITING_TUTORIALS.md#worlds`). A page offers `squiggles`, `letters`
and `numbers`, and every task and practice problem has a variant in each.
A reader can switch at any step, and the switch is remembered. Worlds were
designed for contexts (planets, the sea floor), so using them for
notation is a new use, and the ids of a variant's cells gain the world
(`--squiggles`), as the contract requires. KaTeX already draws the shapes
this needs (`\heartsuit`, `\triangle`, `\square`, `\bigstar`,
`\diamond`, `\clubsuit`), so no new machinery is needed. Squiggles stay in
prose and questions; Python cannot use them as names, and the pages do not
pretend it can.

Wherever the squiggle version exists, the page says out loud what is
happening: *the heart could be any number at all, and the pattern still
holds. That is all a letter in algebra means.* That sentence is half of
what `rules-with-letters-in-them` spends a page on, arrived at sideways.

### Mostly no Python, and Python where it helps

A page whose only interactive content is `question` blocks never loads
Python (`docs/WRITING_TUTORIALS.md#questions`), so it opens quickly and
asks nothing technical of the reader. Most steps in this module are
questions: a multiple choice, or a sentence with a gap that is a dropdown
(`{2/4|3/4|4/4}`). Python arrives in two roles only: as a material the
reader can change (`draw_pizza`, a fraction wall, a bead picture), and as
a checking machine (`Fraction(3, 4) + Fraction(1, 4)`), the control of
error made runnable. The module never teaches Python for its own sake.

## The shape of a page: a staircase

A page teaches one idea in eight to fifteen small steps. A step is one
picture or one line of mathematics, and one question about it. Between
steps the page does not explain much; it moves one thing at a time and
asks again.

- **Steps come in threes:** one the reader can almost read off the
  picture, one that needs the idea, one that stretches it. The third is
  where a reader who is ready finds more (`PEDAGOGICAL_STYLE_GUIDE.md#low-floor-high-ceiling`).
- **Every step has a steps fold** (`dl-hint`, "stuck? here are some
  steps"), and the steps inside are smaller again. The fold never ends at
  the answer; it ends with a smaller question the reader can answer.
- **A calm check** comes twice on a page, after the middle step and
  before the last, always in the same words so it becomes a habit and not
  a surprise. A sketch of the wording:

  > Stop for a moment. Is this still interesting, or has it started to
  > feel like a fight? If it feels like a fight, the step was too big, and
  > that is useful to know. Three ways on: return to the last step that
  > made sense, open the steps under this question, or stop here for today.
  > The page will keep your place.

- **The rule comes last, in the reader's own words.** The discovery
  worksheet ends each section by asking the reader to write their
  "discovered rule" in words. Every page here ends the same way, with a text `predict` block
  or a sentence to finish, and only then shows the page's own version.
- **Then invent some.** Each page closes with "make up five of your own",
  from the same worksheets. A reader who can make a problem that
  simplifies to 1 understands what makes things cancel.

### An example staircase: the first page

*Cutting a pizza: one whole, many slices.* Squiggles are not needed here;
the page is all picture.

1. A pizza in one piece. How many pizzas? (One.)
2. The same pizza cut into 2 equal slices. How many slices? How many
   pizzas, still?
3. Cut into 4. Into 8. Did the amount of pizza change? (A choice: more,
   less, the same.)
4. One slice out of 4 is shaded. We write it $\frac{1}{4}$: the bottom
   says how many slices the whole was cut into, the top says how many we
   have. (The first name, given after three steps of looking.)
5. Shade 2 of the 4. Shade 3. Shade all 4: how much pizza is that?
6. $\frac{4}{4}$ is one whole pizza. What about $\frac{8}{8}$? $\frac{3}{3}$?
   (A dropdown: less than one, one, more than one.)
7. **The idea of the page:** if a pizza is cut into $n$ slices, $n$ of
   those slices is the whole pizza. Shown with a picture for $n = 5$ and
   $n = 12$, then with a heart: $\heartsuit$ slices of size
   $\frac{1}{\heartsuit}$ make 1.
8. Calm check.
9. The cell: `draw_pizza(slices=6, shaded=6)`. Change the numbers. Can you
   make a picture of exactly half? How many ways?
10. Stretch: a pizza cut into 1 slice. Into 100. Into 1000: what does one
    slice look like now?
11. Your rule, in words. Then five of your own.

The same "*n* pieces of $1/n$ make one" returns as the heart of the
reciprocals page, the zero-power page ($\heartsuit^{\triangle} /
\heartsuit^{\triangle} = 1$) and the negative-power page. The module
comes back to it on purpose.

## Practice: a lot of it, and all kinds

Every tutorial has a practice page, and in this module the practice page
is longer than the tutorial. The exploratory worksheets set the pattern:
ten to fourteen small problems that change one thing at a time, then an
exploration, then "invent five". Each problem has its steps fold and its
answer fold (`docs/WRITING_TUTORIALS.md#answers-and-hints`), and each has
a variant in each notation world.

Kinds of problem to mix, beyond "simplify this":

- **Same or different?** Three pictures or expressions; which show the
  same amount? ($\frac{2}{4}$, $\frac{1}{2}$, $\frac{3}{6}$.)
- **Continue the pattern.** $\heartsuit^1, \heartsuit^2, \heartsuit^3, \dots$
  written the long way; what comes next, and what came before the first?
  (The zero and negative powers arrive this way.)
- **Fill the gap.** $\frac{1}{3} + ? = 1$; $\heartsuit^{?} \cdot
  \heartsuit^{2} = \heartsuit^{7}$. Gaps are dropdowns where the reader is
  new, typing boxes later.
- **Match three ways.** A picture, the symbols, and a sentence in words;
  which go together?
- **Closer to 0, to a half, or to 1?** Estimation before calculation, for
  number sense.
- **Where does it go on the line?** Placing fractions on a number line.
- **Spot what happened.** A worked problem by the module's recurring
  character, who makes the mistakes and takes the blame
  (`PEDAGOGICAL_STYLE_GUIDE.md#plain-and-alive`). Which step changed the
  amount? The reader finds it without anyone being wrong but the
  character.
- **Two paths, one answer.** From worksheet 8, question 5: simplify
  $(z^{12})^{1/6}$ two ways and see they agree.
- **Looks scary, is simple.** From the mixed challenge: a tangle that
  simplifies to one letter, or to 1.
- **Invent five.** Always last.
- **Three from before.** Every practice page carries two or three problems
  from earlier pages (`PEDAGOGICAL_STYLE_GUIDE.md#nothing-taught-once`), so fluency is built by
  meeting things again, not by remembering them.

A **practice machine** is optional and worth piloting: one cell per
practice page whose function makes a new problem of the page's kind each
time it runs, in the reader's chosen notation, with its steps. It gives a
reader who wants more an endless supply, which is what fluency needs and
what a printed sheet cannot give.

## The strands

Five strands, each a staircase of short pages. The first four end at a
"view from the top" page that shows why the climb was worth it. The pages
are listed in order. Ids of pages not yet written are proposals.

### Strand 0. Before we start

- **Before we start: how this module works** (`before-we-start`,
  written). No mathematics.
  The beliefs above, in the reader's words: fluency, guesses, calm,
  noticing, small steps. One guess on the page, about something harmless,
  so the reader has made a guess before any mathematics appears. The calm
  check is introduced here, so it is familiar when it comes.

### Strand A. Parts of a whole (fractions)

1. **Cutting a pizza: one whole, many slices** (`one-whole-many-slices`,
   written). The staircase above.
2. **The same amount, different names** (`same-amount-different-names`,
   written).
   The fraction wall: $\frac{1}{2} = \frac{2}{4} = \frac{3}{6}$, seen
   before it is said. Multiplying top and bottom by the same number cuts
   every slice again without changing the pizza.
3. **Which is bigger?** (`which-is-bigger`). Comparing, the number line,
   and the three landmarks 0, $\frac{1}{2}$ and 1.
4. **Adding slices** (`adding-slices`). Same-size slices first, then
   different sizes: to add a half and a third, cut both pizzas into
   sixths. The common denominator arrives as the thing the picture needed.
5. **Taking slices away** (`taking-slices-away`).
6. **A fraction of a fraction** (`a-fraction-of-a-fraction`).
   Multiplying: half of a half, shown by cutting the pizza one way and then
   the other. Why multiplying by a fraction smaller than one makes a
   number smaller (the closer look below).
7. **How many fit? Turning a fraction over** (`how-many-fit`). Dividing
   as "how many quarters fit in 3?", then the reciprocal as the partner
   that makes 1, which is the first page's idea again.
8. **Fractions with holes in them** (`fractions-with-holes`). The same
   moves with squiggles and letters: $\frac{1}{\heartsuit} +
   \frac{1}{\heartsuit}$, $\frac{\triangle}{\heartsuit} \cdot
   \frac{\heartsuit}{\triangle}$. Points forward to
   `running-a-formula-backwards`.
9. **View from the top: narrowing it down** (`narrowing-it-down`). The
   Drake equation as a chain of fractions, each factor narrowing the
   count. Then Frank and Sullivan's "one in 60 billion" as a reciprocal.
   See *The views from the top*, below.

**Closer look:** *does multiplying always make a number bigger?*
(`does-multiplying-make-it-bigger`), after page 6.

### Strand B. Repeated multiplication (powers)

The order of the *Exponent Rules – Discovery Worksheet* (Maths for IT,
Autumn 2025), each section split into two or three smaller pages, each
starting with squiggles and pictures before letters.

1. **The long way** (`the-long-way`, written). A power written out as
   repeated multiplication: $\heartsuit^3 = \heartsuit \cdot \heartsuit
   \cdot \heartsuit$. Paper folding and the golden beads.
2. **Joining two stacks** (`joining-two-stacks`). Multiplying with the
   same base: write both the long way, count the hearts. The rule is the
   reader's to say.
3. **Sharing out** (`sharing-out`). Dividing with the same base: write
   both the long way, cancel in pairs.
4. **When everything cancels** (`when-everything-cancels`). The zero
   power, as $\frac{\heartsuit^{\triangle}}{\heartsuit^{\triangle}}$. It is
   the pizza page again: all the slices make 1.
5. **More on the bottom** (`more-on-the-bottom`). Negative powers, from
   dividing when the bottom has more. Reciprocals return.
6. **A power of a power** (`a-power-of-a-power`). Stacks of stacks.
7. **Everything at once** (`everything-at-once`). The worksheet's mixed
   simplification challenge, with the "looks scary, is simple" problems
   and invent-five. Its fractional-power sections wait for strand C.
8. **View from the top: from a virus to Voyager** (`powers-of-ten`).
    Powers of ten and scientific notation, from the Grade 8 sequence.
    See below.

### Strand C. Undoing a power (surds and logarithms)

Surds and logarithms are where many readers stop. Both are the same
move, undoing a power: a root asks which number was multiplied, a
logarithm asks how many times. So this strand does what the whole
module does, more slowly. **Each idea gets a friendly name and a picture
first, and its usual sign last**, only after the reader has used the
friendly one enough to want something shorter.

| Usual sign | Friendly name first | The picture behind it |
|---|---|---|
| $\sqrt{49}$ | **side(49)**: the side of a square of 49 beads | the bead squares: 1, 4, 9, 16, … |
| $\sqrt[3]{27}$ | **edge(27)**: the edge of a cube of 27 beads | the bead cubes |
| $49^{1/2}$ | **halfway(49)**: half of the multiplying | $\heartsuit^{1/2} \cdot \heartsuit^{1/2} = \heartsuit$, from strand B's rule |
| $\log_{10} 1000$ | **hops(10 → 1000)**: how many ×10 hops from 1 to 1000 | a row of hops, $1 \to 10 \to 100 \to 1000$ |
| $\log_2 16$ | **folds(16)**: how many folds make 16 pieces | the folded paper from strand B |

The friendly names are written in plain text and in Python the same way
(`side(49)`, `hops(10, 1000)`), so a reader can check one in a cell. The
reveal is always a short section headed "The usual way to write it",
which shows the sign, says it means exactly the friendly name, and says
the reader can keep using whichever feels calmer.

1. **The side of a square** (`the-side-of-a-square`). Bead squares, and
   side(n). Which squares have a whole side? Then edge(n) for the bead
   cubes. The usual way to write it: $\sqrt{\;}$ and $\sqrt[3]{\;}$.
2. **Sides that never end** (`sides-that-never-end`). side(2), the
   diagonal of a one-by-one square: no whole number, and no fraction
   either. A cell runs it to twenty places and it does not stop. Then
   side(8) as two side(2)s, from a picture of a square of area 8 made of
   four squares of area 2. The usual way to write it, and the word
   *surd* last of all.
3. **Halfway steps** (`halfway-steps`). halfway(♡) is the power that,
   done twice, gives ♡. It is side(♡) again. The usual way to write it:
   $\heartsuit^{1/2}$, then $\heartsuit^{1/3}$ as edge.
4. **Stretching the halfway steps** (`stretching-the-halfway-steps`).
   $\heartsuit^{2/3}$: what the top and the bottom of the fraction each
   do. The worksheet's sections 7 and 8.
5. **How many hops?** (`how-many-hops`). hops(10 → 1000), folds(16),
   and counting the digits of a number as nearly the same question. The
   usual way to write it: $\log$, last.
6. **Hops that add** (`hops-that-add`). hops for a product is the hops
   of each part added together, seen on two rulers laid side by side: a
   slide rule, the material engineers used for three hundred years.
7. **View from the top: surds and logs in the wild**
   (`surds-and-logs-in-the-wild`). A sheet of A4 folded in half keeps its
   shape because its sides are in the ratio side(2)
   ($297/210 \approx 1.4143$). And the largest known prime,
   $2^{136279841} - 1$ (found in October 2024), has 41,024,320 digits:
   hops, not counting, tells us so.

### Strand D. Seeing it (pictures and graphs)

1. **The number line** (`the-number-line`). Whole numbers, fractions and
   negatives in one line, and the space between them.
2. **Two lines at right angles** (`two-lines-at-right-angles`). The grid,
   and a point as two numbers.
3. **A pattern as dots** (`a-pattern-as-dots`). Plot $1, 2, 3, \dots$
   against $2, 4, 6, \dots$ and then against $2, 4, 8, \dots$. One makes a
   line and one makes a curve. Why?
4. **View from the top: drawing things that differ by millions**
   (`drawing-across-scales`). Log scales: the planets on an ordinary axis
   and then on a log axis, and a scale strip from a virus to the
   observable universe.

### Strand E. The balance (first algebra)

Short, because the Dewey Track already teaches this
(`rules-with-letters-in-them`, `running-a-formula-backwards`). Two or
three pages that make those pages' first step small enough.

1. **A box with something in it** (`a-box-with-something-in-it`).
   $\square + 3 = 7$, then $x + 3 = 7$: a letter is a box.
2. **Keeping it level** (`keeping-it-level`). The balance: do the same to
   both sides. Undoing, one step at a time.

### Mixed sets

One per strand, and one across the module. They are made mostly of the
practice kinds above, in the reader's chosen notation.

## The views from the top

The last page of strands A to D is a reward, not a test. It uses the
strand's mathematics on something with wonder in it, and it is where the
material from the earlier version of this outline now lives.

**Strand A: narrowing it down.** The Drake equation (1961) is a chain of
fractions:

$$N = R_* \cdot f_p \cdot n_e \cdot f_l \cdot f_i \cdot f_c \cdot L$$

Each factor narrows the count. Its descendants each teach something:

| Equation | What it changes | What it shows here |
|---|---|---|
| **Seager** (2013): $N = N_* F_Q F_{HZ} F_O F_L F_S$ | counts planets with gases life could have made, that a telescope could detect | the same shape, with factors that can be measured |
| **Frank & Sullivan** (2016): $A = N_{ast} \cdot f_{bt}$ | asks whether anyone has *ever* arisen, and drops $L$ | a reciprocal: set $A = 1$, and $f_{bt} = 1 / N_{ast}$. For the Milky Way, $N_{ast} \approx 6 \times 10^{10}$, so "one in 60 billion" ($1.7 \times 10^{-11}$) |
| **Sandberg, Drexler & Ord** (2018) | gives each factor a range many powers of ten wide, and samples it | why the median and the mean can disagree hugely; for strand D's view |
| **Westby & Conselice** (2020) | assumes intelligence takes about 5 billion years wherever it arises | "at least 36" civilisations: which assumption fixed that number? |
| **Backus** (2010) | the same chain for finding a partner in London | a human-scale version; teacher's call, as its "attractive" factor makes it awkward in some rooms, and it can be rebuilt as a study-partner chain |

Worksheet 1B (*Fractions in the Wild*, `deweydex/everlearning`,
`Maths Stuff/Worksheets/worksheet_01b_fractions_wild.md`) supplies a
second view for strand A, or a page between A and B: the Lorentz factor
$\gamma = 1/\sqrt{1 - v^2/c^2}$ and what happens as the bottom gets small.
Its note to students ("These are just fractions") is this module's
stance.

**Strand B: from a virus to Voyager.** The Grade 8 sequence, *An
introduction to Scientific Notation and Scale* (`Maths Stuff/Grade 8
Scientific Notation/`, four sheets): the Earth's volume and mass, how many
viruses fit on a full stop, caesium atoms in a tennis ball, a container
ship's cargo, light-minutes and the AU. The fourth sheet ends "This will
help us tomorrow when we look at the Drake Equation"; the fifth is not in
the repository, and strand A's view is its natural partner. Voyager 1 is
no longer at the sheet's 117 AU: it reaches one light-day from Earth
(about $2.59 \times 10^{10}$ km) on 18 November 2026. NASA's "Where are
Voyager 1 and 2 now?" page has the live figure.

**Strand C: surds and logs in the wild.** Described with the strand
above.

**Strand D: drawing across scales.** Kepler's third law with NASA's
planetary data on log–log axes is a straight line with slope $3/2$, which
is strand C's stretched halfway steps seen as a picture. Sandberg, Drexler and
Ord's ten thousand Drake equations make a histogram that can only be
read on a log axis.

Sources: Frank & Sullivan, *Astrobiology* 16(5), 2016 (arXiv:1510.08837,
Table 1). Sandberg, Drexler & Ord, arXiv:1806.02404. Westby & Conselice,
*ApJ* 896:58, 2020 (arXiv:2004.03968). Seager, "The search for habitable
planets with biosignature gases framed by a 'Biosignature Drake
Equation'", *Int. J. Astrobiology*, 2018. Backus, University of Warwick,
2010. Check every figure against its paper before a page quotes it.

## What this module deliberately does not do

- **No timers, no scores, no streaks.** Nothing that measures speed.
  Fluency is ease, and ease is not speed.
- **No rule before its picture.** A rule shown first is something to
  memorise, which is what this module is not for.
- **No Python for its own sake.** It is a material and a checking machine.
- **No teaching of limits, or of algebra beyond the balance.** Those
  pages exist already and are linked.
- **No pretending the difficulty is not there.** A step that is hard is
  made smaller, not called easy.

## Before writing

- **A pilot first.** Strand 0, pages A1 and A2 and page B1, with their
  practice pages, are written, so a class meets both slashes and powers.
  What the pilot should answer: are the steps small enough, does the calm
  check help or annoy, and do readers use the notation switch.
- **The recurring character.** The style guide allows one who makes the
  mistakes. This module needs one before the "spot what happened"
  problems can be written.
- **The picture script** is `dev/graphics/zen.py`. Its SVGs are drawn
  in the site's theme colours, so they read in light, dark and high
  contrast.
- **The ids.** Settle them before the first page ships: once a page has
  been in front of a class, its id is the key a reader's saved work lives
  under.
- **The source worksheets.** `worksheet_01a` and `01b`, the four Grade 8
  sheets, and the *Exponent Rules – Discovery Worksheet* (Maths for IT,
  Autumn 2025). The discovery worksheet is not yet in `everlearning`;
  add it there so the next writer can find it.
