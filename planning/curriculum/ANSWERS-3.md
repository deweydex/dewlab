# Josh's answers, round three

Recorded as given, so the next session starts from the decision rather than
from the question. Nothing here is built yet.

## 1. The editor edits content too — **both**

> Both!

So the editor is not only reorder/insert/create. It also edits a tutorial's
prose and its cells. `planning/EDITOR.md` currently says the opposite —
*"it is not a markdown editor"* — and that section is now wrong and needs
rewriting rather than working around.

What that changes about the plan:

- Cell editing means editing the `id:` line too, and **an id is what a
  student's saved work is keyed on**. Renaming one silently discards their
  work in that cell. The editor has to know that, and say so.
- A content editor wants a preview. The build is Python; the editor is a
  browser page. Either it ships a rough preview that can disagree with the
  real build, or it commits and waits for the site to republish.
- The token-in-`localStorage` design was sized for occasional structural
  edits. Content editing means it is open far more often.

Those three are the design work of the editor, and none of them was in the
plan when the plan said "not a markdown editor".

## 2. Searching and sorting split; divide and conquer sits in both

> I think both searching and sorting can be in the same module as divide and
> conquer, maybe we can split sorting and searching into two different
> tutorials and divide and conquer can be present in both?

So the edge direction I shipped (7.7) is beside the point — divide and conquer
is not before *or* after, it is **inside both**. Which means:

- The single "Searching and sorting" topic becomes **two**.
- Divide and conquer is taught in both, discovered twice: once as binary search
  halving a sorted list, once as merge sort halving an unsorted one.
- The existing tutorials `finding-things` and `putting-things-in-order` are
  already that split. The *topics* have not caught up with the tutorials.

## 3 & 4. Pythagoras is a gateway; trigonometry needs triangles and coordinates

> I think pythagoras can certainly be a good gateway... I think SOH-CAH-TOA
> needs categorization of different triangles (scalene, isosceles, equilateral)
> and coordinates so we can have the unit circle

Two changes to the tree:

- **Pythagoras becomes the sixth gateway.** The measurement already said so
  (it unlocks 7, more than graphing's 5); I argued against it and Josh went
  with the measurement.
- **SOH-CAH-TOA gains two prerequisites**: naming triangles by their sides,
  and coordinate geometry. The second is the one I had left out, on the
  grounds that a right-angled triangle is a picture rather than a graph —
  but the unit circle *is* a graph, and it is where the trigonometry goes.

Is there a topic for classifying triangles? If `topics.yaml` has none, one
needs adding rather than the edge being quietly dropped.

Also asked for, and separate from the edges:

> let's make sure that the paths make sense and that the colors make sense
> (and are mentioned somewhere as a description)

The strand colours currently appear on every node and are explained nowhere
except the detail panel, which you only see after choosing something. The tree
page needs a key.

## 5. Matrices: no eigenvectors, yes Markov, five to seven tutorials

> I think we dont need eigenvectors but markov would be great

`planning/outlines/matrices.md` drops the eigenvector bonus and promotes Markov
chains from bonus to a tutorial. `everlearning/OtherCourses/Markov-Chains-and-Text-Generation`
is a whole small course already, and `worksheet_07d_markov_chains.md` is the
paper half.

**No longer blocked.** The descriptor was not in `everlearning` — only MIT and
PDP are — so Josh supplied it. It is now in the repository at
`planning/curriculum/descriptors/ComputationalMethodsandProblemSolving5N0554.pdf`,
which is the first module descriptor dewlab holds as a source document rather
than as `outcomes.yaml` entries somebody typed up.

**Computational Methods and Problem Solving 5N0554**, Dublin and Dún Laoghaire
ETB. 150 hours, 15 credits, thirteen learning outcomes across seven sections.

It says more than "matrices are in scope", and some of it is a surprise:

| Section | What it names |
|---|---|
| 1. Discrete computational structures | arrays, lists, **matrices**, trees — used for ASCII art, computer graphics, **Gaussian elimination**, decision matrices, classical sorting/searching/filtering. Functions and **recurrence relations**. Iterative versus recursive. |
| 2. Discrete probability | distributions (Gaussian), sample mean and variance, expectation, dependent vs independent events, **random numbers in computing**, and why randomness matters to PKI |
| 3. Modelling and simulation | computational and numerical methods, **Monte Carlo** |
| 4. **Linear algebra and applications** | arrays and matrices in graphics and games, **Google PageRank**, sequence alignment, nearest neighbour |
| 5. Algorithms and complexity | best, expected and worst case |
| 6. Applications of discrete probability | average-case analysis, failure prediction, branch prediction, network packet loss |
| 7. Modelling and simulation | abstraction; server-room temperature, robot control, autonomous vehicles, traffic flow |
| 8–13 | problem definition and solution design, heuristics, symptom versus root cause, iterative model creation and validation, personal attributes, reflection |

Three things this settles:

1. **Markov chains are not a bonus, they are the syllabus.** LO4 names Google
   PageRank explicitly, and PageRank *is* a Markov chain — the stationary
   distribution of a transition matrix. Josh's instinct that "markov would be
   great" lands exactly on a named outcome.
2. **Dropping eigenvectors is fine, but PageRank is an eigenvector problem** in
   disguise. It can be taught as repeated multiplication converging, which is
   tutorial 2 of the strand doing something a student cares about, with no
   eigenvector vocabulary anywhere.
3. **Matrices are a fraction of it.** Monte Carlo, randomness and PKI,
   complexity analysis, recurrence relations, and modelling are all in here and
   none is matrices. Five to seven tutorials on matrices is comfortable, but the
   series needs several more strands beyond them — which answers the matrices
   outline's open question about whether five tutorials is too much of the
   series. It is not.

**Still to do:** the outcomes need transcribing into `outcomes.yaml` in the
shape MIT and PDP use, so coverage can be tracked the same way. Not done here.

## 6. The map is MIT and PDP only

> lets just have the map be about maths for it and PDP. So we dont need to deal
> with matrices in the map at all.

This settles the open question at the end of `DEPENDENCIES.md` about where
matrices attach: **nowhere, because they are not on the map.** The map is the
two module descriptors and nothing else. The computational-methods series is
extra material that stands outside it.

That also means the matrices outline's "open question" about whether the strand
assumes the maths series is now a teaching note rather than a data question —
there is no edge to draw either way.

## Order of work agreed

Scheduled for a fresh session: the editor first, and these tree changes
alongside it.
