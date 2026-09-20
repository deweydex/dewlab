# Visual list

Where a diagram earns its place in dewlab, how those diagrams get made, and
how they stay legible in all four of the site's display modes.

---

## What earns a visual

Two jobs, and a visual should be doing at least one of them.

**Carrying a shape prose cannot carry.** Five tables pointing at each other, a
tree three levels deep, a recursion that asks the same question twice. A
reader can follow every sentence describing a structure and still not have the
structure, because assembling it was work the sentences left to them.

**Introducing notation a student will meet again.** Crow's-foot ER diagrams,
UML class boxes, state-transition graphs and flowcharts turn up in every
later textbook and tool a dewlab student will open. Meeting the notation here,
attached to a database they built themselves, is cheaper than meeting it cold
somewhere else. This argues for standard notation even where a friendlier
ad-hoc sketch would explain the immediate point just as well.

### What does not earn one

**A tutorial that already draws its own figure from data.** *Drawing Sets*,
*The Unit Circle*, *Solving Triangles*, *Pictures Worth Numbers*, *Sine and
Cosine Waves*, *Approaching a Limit*, *Rates of Change*, *Parabolas*, *Drawing
Functions*, *What a Matrix Does to a Picture*, *Counting Darts* and *Charting
a Query's Result* build their pictures in matplotlib from numbers the reader
can change. A static version is strictly worse: it cannot be poked. The same
holds for CSS tutorials whose live preview is the demonstration — *hover and
focus*, *transitions and transforms*, *media queries*.

**Decoration.** If the caption has to explain the picture, the picture is not
working. Every entry below names one thing a reader should be able to read off
the image without help. That sentence is also the image's `alt` text.

**Anything a teacher will want their own version of.** Site maps for a
student's own project, marking rubrics, worked layouts for the team project.
What belongs here is the notation itself, drawn on the course's own examples,
which a teacher can point at from whatever they use instead.

---

## How graphics get made

Graphics are code. A diagram that cannot be regenerated is a diagram nobody
will fix.

### One generator per module

`dev/graphics/<module>.py`, one file per course or series, holding every
figure that module needs. Each figure is a function returning an SVG; a
`--write` pass drops each one into its tutorial's own folder under the name
the markdown references. Fixing a diagram means fixing the function and
re-running, not opening an editor and hunting for the box that moved.

This also makes a module's visual language reviewable in one place. Five ER
diagrams drawn by five separate hands drift; five produced by one function
with different inputs cannot.

### Which tool draws what

| Tool | For | Why |
|---|---|---|
| **graphviz (`dot`)** | ER diagrams, state-transition graphs, trees, recursion trees, flowcharts | Automatic layout. Anything where boxes and arrows need arranging is a solved problem, and solving it by hand in matplotlib is how a week disappears. HTML-like labels give proper ER table boxes with `PK`/`FK` marks. |
| **matplotlib** | Number lines, nested sets, the box model, timelines, binary-search bars, the unit square and its determinant, probability trees with fixed geometry | Coordinates rather than layout. It is also the library the student-facing figures already use, so a generated figure and a live one look like relatives. |
| **matplotlib `mplot3d`** | Three planes meeting at a point, in *Solving Systems* | The one genuine 3D case in the material. |

Both are build-time only. Neither reaches a student's browser: the page's own
Python comes from Pyodide, and `requirements-build.txt` stays as it is. The
generator's dependencies belong in a separate file, installed by whoever is
regenerating a diagram, never by CI to build the site.

Adding a library is cheap here and should not be agonised over. A third one
earns its place the moment it draws something the two above draw badly.

---

## Colour: one normaliser, two producers

Every SVG in the repository passes through `dev/normalise_svg.py`, whether it
came from a generator or from a contributor's draw.io export. It maps literal
colours onto the tokens in `assets/tutorial-style.css`, which already solve
the problem the diagrams have.

`--dl-type-python`, `--dl-type-sql`, `--dl-type-html`, `--dl-type-css`,
`--dl-type-js` are chromatic **ink**: one hue that keeps its identity across
modes while changing tint to stay legible. SQL's teal is `#0d7a72` in light,
`#5eead4` in dark, `#0b635c` at high contrast.

`--dl-highlight-bg`, `--dl-highlight-green`, `--dl-highlight-blue`,
`--dl-highlight-pink` are chromatic **fills**: soft tints in light, deep muted
equivalents in dark. They were chosen as highlights behind body text, which is
a harsher test than a diagram fill, so "not jarring, not too bright" comes for
free.

| Source colour | Becomes | Why |
|---|---|---|
| Black, near-black ink | `currentColor` | Follows `--dl-fg`, so theme and high contrast work without the diagram knowing about either |
| White masking fill | `var(--dl-bg)` | Stays opaque against the page in every mode |
| Mid grey | `var(--dl-muted)` text, `var(--dl-rule)` lines | The two greys the site already distinguishes |
| A chromatic fill | nearest `--dl-highlight-*` by hue | Keeps the hue's identity, inherits the tuned light and dark versions |
| A chromatic stroke or label | nearest `--dl-type-*` by hue | Legible as a line and as text in all four modes |
| Anything unrecognised | reported, build fails | See below |

### Three things the normaliser has to do beyond swapping colours

**Set `fill="currentColor"` on the root.** A producer omits the `fill`
attribute wherever the colour is the SVG default of black, so there is nothing
to rewrite and the text stays black — invisible on a dark background, while a
colour-mapping report says every colour was mapped. `fill` is an inherited
presentation attribute, so one attribute on the root catches every descendant
at once. Anything that genuinely wants no fill says `fill="none"` already.

**Strip colour declarations out of inline `style` attributes.** A style
property beats a presentation attribute, so rewriting `fill="…"` achieves
nothing while `style="fill: …"` survives beside it.

**Strip draw.io's `<style>` block and its `light-dark()` values.** A current
draw.io export is already theme-aware, but against the wrong signal: it writes
`light-dark(rgb(0,0,0), rgb(255,255,255))` and `var(--ge-adaptive-bg)`, both
resolving against `color-scheme`, which follows the operating system. dewlab's
own `data-theme` is set in the settings panel and is allowed to disagree with
the OS, and `data-contrast="high"` is invisible to `light-dark()` entirely. So
the export's theming is removed rather than worked with, and the root is given
`color-scheme: normal` so nothing re-enters through it.

### It fails the build

A missing `alt` already stops the build rather than logging a warning, because
a warning in a CI log is a warning nobody reads (`DECISIONS_LOG.md` 1.4). The
same applies here with more force: the contributor who breaks a diagram is in
light mode, so the failure is invisible to exactly the person who caused it.

The check runs over committed SVGs and needs no graphviz, so CI stays cheap.
It should be paired with a rendered check in the existing e2e suite: load a
page in each of the four modes and assert every `<text>` in an SVG clears 4.5:1
against the background. Source-level checking alone reported "every colour
mapped" on a diagram whose text was invisible.

**Not a regenerate-and-diff check.** `standalone-bundle-is-current` rebuilds
the vendor bundle and fails on any difference, which works because the bundler
is pinned and deterministic. Graphviz embeds its version in its output and
shifts layout between releases, so the same check here would fail on an
unrelated upgrade. Check the committed SVG, not the ability to reproduce it
byte for byte.

---

## Regenerating, and frozen releases

`copy_tutorial_assets()` writes the same asset bytes to the same path for
every version of a tutorial, current and frozen alike. A frozen release
therefore shows whatever the image file currently holds. So:

**Fixing a diagram — a colour, a typo, a crossed line — regenerates in place.**
The frozen release wanted that fix too.

**Changing what a diagram says needs a new filename.** The frozen `.md` keeps
its own `![](old-name.svg)`, the old file stays in the folder, and the current
release points at the new one. This needs no build change, only the naming
discipline, and it matches how `v<version>.md` already works.

---

## Drawn for the reader, or drawn by the reader

A diagram handed to a reader teaches the notation. A diagram the reader
produces tests whether the structure is in their head. Both are worth having,
in that order — so the later a tutorial sits in a sequence, the weaker the
case for drawing its diagram for it.

**Interactive here means generated from the student's own work, not a form.**
`text_input`, `dropdown`, `button` and `image_input` raise `RuntimeError` on a
published page: Pyodide runs in a Worker, and a widget needs to attach a
listener to a live element on the main thread (`DECISIONS_LOG.md` 7.77). They
work only in a downloaded copy, and nothing published uses them.

What works published is better anyway. A Python cell reads `PRAGMA table_info`
and `PRAGMA foreign_key_list` off the student's own database and draws the ER
diagram their `CREATE TABLE` statements actually describe — not the one they
meant. A missing arrow is a missing foreign key, seen as a gap rather than
reported as a message. The schema stays the single source of truth, `check()`
still gives the pass, and the picture is theirs.

**This needs foreign keys declared.** `PRAGMA foreign_key_list` reports only
what was written. With enforcement off, a table created with
`FOREIGN KEY (product_id) REFERENCES products(id)` reports the relationship in
full; `dinosaur_id INTEGER`, the module's current style, reports nothing. Only
*The Tentacular Plushies Quiz* declares it today. It is the standard form every
other course and tool expects, and SQLite records it without enforcing it, so
no existing cell changes behaviour.

*A Second Table and a Join* stays bare — its point is the shared value, not the
syntax that declares it. `REFERENCES` arrives in *Designing a Table Before You
Build It*, where the design vocabulary already lives and "which column points
at another table" is already the third question, and is declared from there on.

---

## The database module, page by page

| Page | Visual | Kind |
|---|---|---|
| [A Table Is a List of Rows](../tutorials/a-table-is-a-list-of-rows/a-table-is-a-list-of-rows.md) | The existing grid diagram, normalised, and given real `alt` text | Drawn (exists) |
| [A Second Table and a Join](../tutorials/a-second-table-and-a-join/a-second-table-and-a-join.md) | One foreign key with the actual values in it, the duplication on the correct side | Drawn |
| [Designing a Table](../tutorials/designing-a-table-before-you-build-it/designing-a-table-before-you-build-it.md) | Crow's-foot ER diagram of products and sales; the notation introduced | Drawn |
| [Designing a Table](../tutorials/designing-a-table-before-you-build-it/designing-a-table-before-you-build-it.md) — "your turn" | Nothing. It asks for paper and should keep asking for paper | Neither |
| [Joining Two Real Tables](../tutorials/joining-two-real-tables/joining-two-real-tables.md) | Inner versus left join as row matching | Drawn |
| [The Tentacular Plushies Quiz](../tutorials/the-tentacular-plushies-quiz/the-tentacular-plushies-quiz.md) | ER diagram generated from the student's own schema | Student-produced |
| [The Library Loans Quiz](../tutorials/the-library-loans-quiz/the-library-loans-quiz.md) | The same, and the junction table is the point of it | Student-produced |
| [A College Timetable](../tutorials/a-college-timetable/a-college-timetable.md) | Five-table ER diagram, generated; plus a drawn overlap timeline | Both |

The plushies quiz introduces the generated diagram, because it already
declares `FOREIGN KEY … REFERENCES` and already reads `PRAGMA table_info` for
its own checks. No new syntax has to be taught to make it work.

The timetable is the one page wanting both. The five-table diagram is
generated, because getting four arrows into `sessions` right is the task. The
overlap timeline is drawn, because it illustrates a rule about two intervals
and there is nothing in the reader's database to generate it from.

One drawing function takes a connection and returns a figure; every page after
the first calls it in two lines. That function is the real build cost of this
half of the plan, and the thing to get right before it is copied five times.

---

## Tier one

The drawn diagrams to make first. The database entries above say which pages
get a generated diagram instead; the two lists read together.

### Databases

**[A Second Table and a Join](../tutorials/a-second-table-and-a-join/a-second-table-and-a-join.md) — one foreign key, with real values in it.**
Two small row lists holding the actual data from the cells above, and a line
from `sightings.dinosaur_id = 1` to `dinosaurs.id = 1`, drawn twice because
two sighting rows point at the same dinosaur. The claim "that shared value is
what connects one table's row to the other's" is one sentence doing a lot of
work. Showing the same value in two places, with the duplication on the
correct side, is what makes the next page's argument about misspellings land.

**[Designing a Table Before You Build It](../tutorials/designing-a-table-before-you-build-it/designing-a-table-before-you-build-it.md) — a crow's-foot ER diagram of products and sales.**
The tutorial is entirely about a decision made on paper before any SQL is
written, and there is no picture of what that paper looks like. Two entities,
one-to-many marked with crow's feet, `PK` on `products.id`, `FK` on
`sales.product_id`. A reader should be able to read off it that one product
row connects to many sales rows and not the reverse. This is where the
notation is introduced, so it wants a sentence naming it and saying they will
see it again.

**[Joining Two Real Tables](../tutorials/joining-two-real-tables/joining-two-real-tables.md) — inner versus left join, as row matching. Not a Venn diagram.**
The overlapping-circles picture of join types is everywhere online and is a
poor model: it implies joins are set operations on rows, which mispredicts
what happens when a key repeats on one side, and it hides which table's rows
survive. Draw two columns of labelled rows with match lines, then the same
pair twice — once under `JOIN`, where the unmatched `United States` row has no
line and is gone; once under `LEFT JOIN`, where it survives carrying an empty
`region`. That empty cell is what the section is about, and the Venn picture
cannot show it at all.

**[A College Timetable](../tutorials/a-college-timetable/a-college-timetable.md#finding-a-clash) — an overlap timeline.**
Three bars on a shared time axis: A at 10:00–12:00, B at 11:00–13:00
overlapping it, and C at 11:00–13:00 sitting back to back with a 09:00–11:00
session. The rule `s1.start < s2.end AND s2.start < s1.end` is a statement
about two intervals, and the tutorial already walks it through on paper
because it knows the rule is hard to see. The picture makes the back-to-back
case — the one that stops a full day being reported as one long clash —
obvious rather than argued.

### Mathematics and computational methods

**[Where Chains Lead](../tutorials/where-chains-lead/where-chains-lead.md#a-weather-machine) — the two-state transition diagram.**
Two nodes, sunny and rainy, four labelled arrows carrying 0.7, 0.3, 0.4 and
0.6, both self-loops included. The tutorial has no figures at all, and the
labelled graph is the standard picture of a Markov chain. More than the
exposure: the matrix `P` and the graph are the same object written two ways,
and putting them side by side is the insight. A reader should be able to trace
the row-sums-to-one fact off the picture, as the arrows leaving each node.

**[Three Ways to Make Change](../tutorials/three-ways-to-make-change/three-ways-to-make-change.md#remembering-what-we-already-worked-out) — a recursion tree with the repeat marked.**
The argument for memoisation is made in prose about a shape: reaching 6 via 3
then 3 asks "fewest tokens for 3", and reaching it via 4 then 1 then 1 asks
the same question again. Drawing the tree from 6 down with the two identical
subtrees circled turns a paragraph the reader has to trust into something they
can count.

**[Multiplying Grids](../tutorials/multiplying-grids/multiplying-grids.md#multiplying-two-grids) — row by column into one cell.**
The rule arrives as $c_{ij} = \sum_k a_{ik} b_{kj}$, which is precise and hard
to read cold. One 2×3 and one 3×2, with row 2 of $A$ and column 1 of $B$
picked out, an arrow to the single result cell they produce, and the three
products written underneath. Why the shapes have to agree, and why the
transpose is the convenient way at the columns, both follow from that picture.

**[Numbers and Their Families](../tutorials/numbers-and-their-families/numbers-and-their-families.md#the-number-domains) — nested number sets.**
$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$ as
nested regions, with example values placed in the right ring rather than
listed: $3$ innermost, $-5$ in $\mathbb{Z}$ only, $\tfrac{2}{3}$ in
$\mathbb{Q}$ only, $\sqrt{2}$ and $\pi$ in the outer ring alone. A reader
should be able to answer "which families does $-5$ belong to" by pointing,
which is what `classify_number` is being asked to compute.

**[Finding Everything Inside a Folder](../tutorials/finding-everything-inside-a-folder/finding-everything-inside-a-folder.md#a-structure-that-branches) — the `photos` tree.**
The tutorial describes a three-level structure one node at a time, because a
nested dictionary literal does not read as a shape. The same picture then
serves twice more: the recursive walk descends it, and the iterative walk
pushes and pops on it.

**[A Model That Corrects Itself](../tutorials/a-model-that-corrects-itself/a-model-that-corrects-itself.md#a-model-that-starts-out-wrong) — the perceptron.**
Nine inputs, one weight on each edge, a summing node, the bias arriving into
it, the threshold, one binary output. It also does immediate local work: the
"your turn" sets `weights[1]` to 1.0 by hand and asks which pattern flips and
why that pixel. With the nine edges drawn and the 3×3 grid positions labelled,
that is answerable by looking.

### Object-oriented programming

**[One Parent, Many Children](../tutorials/one-parent-many-children/one-parent-many-children.md) — a UML class diagram.**
`BankAccount` above, `SavingsAccount` and `CheckingAccount` beneath it with
hollow-triangle inheritance arrows, and `Bank` holding accounts as a different
relationship entirely. It carries content the code makes you scroll to see:
that `withdraw` appears in both the parent and `CheckingAccount`, which is
what overriding is, and that `Bank` relates to accounts a completely different
way from how the subclasses do.

### Web authoring

**[The box](../tutorials/the-box/the-box.md#why-this-happens) — the box model.**
Content, padding, border and margin as four labelled nested rectangles. The
live preview shows what changing padding does and never puts the four names on
the picture. Padding tinted with the box's background, margin left
transparent, since that distinction is the one the prose makes.

**[The two loops](../tutorials/the-two-loops/the-two-loops.md) — two cycles, side by side.**
Left: edit, save, refresh, back to edit. Right: edit, add, commit, push, wait
for Pages, refresh, back to edit. Drawn as cycles rather than as two lists,
because the habit the page teaches is diagnostic — *which loop am I in* — and
that is a question about position in a cycle. The wait step wants marking as
the only one the reader does not control.

---

## Tier two

Real value, lower ratio, and several are harder to draw well than tier one.
Worth starting once the generators and the normaliser have stopped moving.

**[A page that reads from a database](../tutorials/a-page-that-reads-from-a-database/a-page-that-reads-from-a-database.md)** — the request path: page, its own script, the query, the table, rows back, rows into the DOM. The sentence carrying this tutorial is "what its script is allowed to reach"; showing the reach as an arrow crossing a boundary is what makes full-stack concrete.

**[When It Goes Wrong](../tutorials/when-it-goes-wrong/when-it-goes-wrong.md#reading-a-traceback)** — an annotated traceback: top marked "where the program started", bottom "where it broke", and separate marks on the line that *failed* and the line that is *responsible*. The section makes a subtle distinction — `average` is not wrong, the empty list handed to it is — and annotation is the natural medium for it.

**[Flexbox first steps](../tutorials/flexbox-first-steps/flexbox-first-steps.md#why-this-happens)** — main axis and cross axis. The preview shows wrapping; the vocabulary that makes every later flexbox property comprehensible is not visible in it.

**[Planning a site](../tutorials/planning-a-site/planning-a-site.md#two-site-maps)** — the good site map drawn as a map, and one rough wireframe. A tutorial about planning visually whose two site maps are both prose blockquotes. Keep it deliberately rough, so it reads as something a student could draw in two minutes.

**[Finding Things](../tutorials/finding-things/finding-things.md#binary-search-the-power-of-sorted-data)** — the search range collapsing: four or five rows of the same sorted list, live range shaded and shrinking, `low`, `mid` and `high` marked. The halving is the whole efficiency claim, and the picture also debugs the off-by-one the pseudocode invites.

**[Sets as Sorted Lists](../tutorials/sets-as-sorted-lists/sets-as-sorted-lists.md#set-operations-the-merge-pattern)** — the two-pointer walk, three or four steps, each showing which pointer advanced and what was appended. Three of the reader's own functions are variations on this shape.

**[What Are the Chances?](../tutorials/what-are-the-chances/what-are-the-chances.md#compound-events)** — a probability tree for two draws without replacement, $\tfrac{4}{52}$ then $\tfrac{3}{51}$ on the branches; and a two-way table for aces against hearts showing the one cell subtracted in the general addition rule. That overlap cell is what students double-count.

**[Counting Carefully](../tutorials/counting-carefully/counting-carefully.md#combinations-order-does-not-matter)** — permutations and combinations off one tree: pick three from four, then the same picture with the orderings of each set grouped. The $r!$ you divide by becomes the size of a group.

**[Repeating Yourself](../tutorials/repeating-yourself/repeating-yourself.md#sigma-notation-mathematics-meets-loops)** — sigma notation and a `for` loop mapped part to part: index variable, lower bound, upper bound, body, accumulator, with lines between corresponding pieces.

**[Logic and Truth](../tutorials/logic-and-truth/logic-and-truth.md#de-morgans-laws)** — De Morgan's laws twice: two shaded set pictures that come out identical, and two gate arrangements that do. The claim is about two pictures landing on the same region, which is why *Drawing Sets* drawing its own from data does not cover it.

**[How We Got Here](../tutorials/how-we-got-here/how-we-got-here.md#the-only-language-the-machine-understands)** — the abstraction stack: hardware, machine code, assembly, a language people read, each band carrying what it hides. The tutorial walks up this ladder historically; the vertical picture makes "higher level" a spatial fact rather than a phrase.

**[When a Queue Never Clears](../tutorials/when-a-queue-never-clears/when-a-queue-never-clears.md)** — arrivals, queue, server, departures, with rates on the arrows. The plots already show behaviour; the block diagram names the parts.

**[Undoing It](../tutorials/undoing-it/undoing-it.md#measuring-the-square)** — the unit square and its image, the determinant as the area of the parallelogram, and a collapsed case where the area is zero. The argument for why a zero determinant means no inverse is geometric and currently unillustrated.

**[Solving Systems](../tutorials/solving-systems/solving-systems.md#three-unknowns-row-by-row)** — three planes meeting at a point, and the two degenerate cases. The one place 3D is the honest picture rather than a flourish.

**[Named grid areas](../tutorials/named-grid-areas/named-grid-areas.md)** — the grid with line numbers and named areas overlaid on one picture. Grid is the CSS layout topic where the preview genuinely does not reveal the coordinate system.

---

## Pages that introduce the notation

Two, not four.

**ER notation, in Database Methods.** Crow's foot, `PK` and `FK`, one-to-many
and many-to-many, on the products-and-sales example. It sits with or just
before *Designing a Table Before You Build It*, the first page where design
vocabulary arrives and the first asking a reader to plan on paper. Everything
after it points back rather than re-explaining, and the student-generated
diagrams later have a notation to be read against.

**Graphs and trees, in Computational Methods.** Nodes and edges; directed
versus undirected; a weight on an edge; a self-loop; a tree as the special
case with no way back. One page serves five tutorials — *Where Chains Lead*,
*Finding Everything Inside a Folder*, *Three Ways to Make Change*, *A Chain
Reads a Book* and *When a Queue Never Clears*. It belongs at the end of the
Matrices series, immediately before *Where Chains Lead*, since that is where
the transition matrix arrives and the whole point is that the matrix and the
graph are the same object written twice.

**Not matrices.** The notation the matrix tutorials use is ordinary
mathematical notation they already introduce in place. What is missing is two
specific pictures — row-by-column in *Multiplying Grids*, the unit square in
*Undoing It* — both already listed.

**Not sets.** *Drawing Sets* already is the set notation page: it builds two-
and three-circle diagrams from real sets, names every region, and says where
the picture stops helping at four sets. What it lacks is small and belongs
inside it — a panel putting $\cup$, $\cap$, $\setminus$, $\subset$, $\in$ and
complement against the shaded region each one names.

---

## Where the files go

A diagram lives in its own tutorial's folder and is referenced by plain name,
with no path:

```markdown
![One product row connects to many sales rows; each sales row names exactly one product.](products-sales-erd.svg)
```

A reference to a file the folder does not hold stops the build, and so does a
missing `alt`. Most of these diagrams carry the content of a section, so
`alt=""` is wrong on nearly all of them. The alt text is the one thing the
entry above says a reader should be able to read off the picture — not a
description of the drawing.
