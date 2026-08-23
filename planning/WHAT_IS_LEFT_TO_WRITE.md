# What is left to write

What exists, what the curriculum map says is still to be written, and whether
anybody has decided how to teach it.

**Read the map, not this file, for numbers.** `planning/CURRICULUM_MAP.md` is
generated from the outcomes, the tutorials' own `covers:` frontmatter and
`out-of-scope.yaml`, and it now reports the one figure this document exists to
give: how many outstanding outcomes have no proposal. This file is the prose
around that figure, and it will go stale before the map does.

## The first version of this was wrong, twice

Worth saying at the top, because both mistakes are the kind that recur.

The first pass counted coverage with a script written for the purpose instead of
reading the map that already exists, and got two different answers wrong in the
same direction:

- **It counted "used" as "taught".** Four outcomes are named in a tutorial's
  `covers:` under `touches:` rather than `covers:` — students meet them in
  passing and nothing teaches them. The map has always drawn that distinction and
  calls them the quiet gaps. The script did not, so it reported them as done.
- **It ignored `out-of-scope.yaml` entirely**, and so reported two settled
  decisions as gaps: Venn diagrams and trigonometric ratios in surd form. That
  file exists precisely so a decision stops looking like a gap, and the first
  survey of what was missing walked straight past it.

Both errors are now caught by the map itself rather than by whoever reads it
next. The map reports the unplanned count in its own summary, and
`tests/test_curriculum_map.py` fails if a proposal claims an outcome that is
already taught.

---

## What exists

Twenty tutorials: seventeen in Maths and Programming, one in Reflections and
Review, two in the Computational Methods series.

## What is left, and who has thought about it

Sixty-seven outcomes, none ruled out, forty-one in place. **Twenty-six still
need writing** — twenty-two nothing touches, and four the students meet in
passing without anything teaching them.

**Every one of the twenty-six now has a proposal.** That was not true on the
morning of 23 August, when five had neither a tutorial nor a plan, and it is the
one thing in this document worth checking again later. The map prints the number.

Where the outstanding work sits:

- **Functions and calculus**, all seven outcomes. Drawing Functions, Parabolas,
  Approaching a Limit, Rates of Change.
- **Geometry and trigonometry**, all ten. Lines and Distances, The Unit Circle,
  Sine and Cosine Waves, Solving Triangles.
- **Logic and sets**, three. Logic and Truth, Drawing Sets.
- **Algebra**, two used-but-not-taught. Rearranging Formulae, When There Is No
  Answer.
- **Programming and Design Principles**, four. Two everlearning conversions and
  the team project.

Nothing on the mathematics side past algebra has been written. That is not a
surprise: the seventeen tutorials that exist are the programming spine with
mathematics threaded through it, and the mathematics that is threaded is
arithmetic, algebra, counting, probability and statistics. The half of the
descriptor that needs pictures has none of them yet.

## What was decided on 23 August, later the same day

Everything below the next heading was written before these, and the counts in it
were superseded within hours. **Twenty-six outcomes now need writing, not
twenty-five**, because `MIT-4.7` came back into scope — and nothing is out of
scope at all any more.

Three things changed the shape of the plan:

**Trigonometry became three tutorials.** *Angles and Waves* carried five
outcomes and gave the unit circle a fifth of itself. It is now The Unit Circle,
Sine and Cosine Waves, and Solving Triangles. *Parabolas* came out of *Drawing
Functions* for the same reason.

**`MIT-4.7` came back**, and it is the reason The Unit Circle exists as its own
tutorial. Ruled out, the exact values were three numbers to memorise; on the
circle they are the places the angles land, and Pythagoras produces them in a
line.

**The re-cut went too far and was pulled back.** Four proposals were split to one
outcome each and three of them were put back the same day. Josh: *"I'd rather
they not be too short — they still need to motivate, introduce and explain
content, and give students a chance to work through things. So let's not
overcorrect before making things."* The floor is the teaching, not the outcome
count. See DECISIONS_LOG 7.42.

**And a new thread.** The practice problems for most of this already exist in
`deweydex/Mathematics` — twenty-seven worksheets with answer keys, mapping almost
one-to-one onto the proposals. `planning/EXERCISES.md` is the plan.

## What was decided earlier on 23 August

**Coordinate geometry became a tutorial of its own.** `MIT-4.1` to `4.4` were
settled as in scope in full on 22 August and nothing was written to carry them;
`drawing-functions.md` had them as a conditional extra, written back when Section
4 was mostly out of scope. They are now
[Lines and Distances](./outlines/lines-and-distances.md), which sits between
Drawing Functions and the trigonometry.

Two reasons it is not a section of Drawing Functions. Pythagoras is one of the
six gateways in the topic tree, unlocking seven downstream topics — a gateway
that exists only as somebody else's third subsection is not a gateway. And Angles
and Waves already assumes this material: the unit circle is a coordinate-geometry
object, so without this tutorial it would have to teach coordinates in passing on
its way to trigonometry.

The outline is mostly about **how to describe the material** rather than what to
include, because that was the part Josh asked to work out first: what to call it,
which of the three descriptions of a line comes first and why the general form
arrives last, whether slope is named as rise-over-run or as a rate of change, and
why the distance formula should come before Pythagoras rather than after.

~~**`MIT-4.9` became a short tutorial called *How Tall Is That?*.**~~ Superseded
the same day. It is a section of Solving Triangles now — the easy case the Sine
and Cosine Rules are the repair for. Josh: *"I don't really think we need to
worry about it… we can deal with more appropriate to computer science types of
questions there."* Once the examples stopped being ladders and roofs, the
material had no reason to sit apart from the rules it is a special case of.

**Venn diagrams came back into scope** as [Drawing Sets](./outlines/venn-diagrams.md),
a short tutorial of its own. It had been ruled out on the grounds that the
diagram is a pen-and-paper convention adding notation rather than understanding.
Josh reversed that and asked for it separate, linked to Logic and Truth and to
Sets as Sorted Lists rather than folded into either — *"those can be connections.
We don't need to do combinations here."*

The reversal answers the original objection rather than overruling it. What comes
back is not the notation but the picture drawn by matplotlib from real sets:
output rather than convention, and the point at which three sets stop fitting in
a person's head.

**`MIT-4.7` stayed out of scope** — for about four hours. Trigonometric ratios in
surd form. The first version of this survey called it a gap; it was a decision
with a reason. Then Josh reversed the decision, and it is now the reason The Unit
Circle is a tutorial rather than a section. Both of those are recorded above.

## Computational Methods 5N0554 is not measured

Two tutorials against a 150-hour, 15-credit module with thirteen outcomes.

Those thirteen are not in `outcomes.yaml`, so the map does not measure this module
and none of the numbers above include it. That follows from Josh's decision that
the map is Maths for IT and Programming and Design Principles only, and it has a
side effect worth naming: *there is no count of what this module is missing, so
it cannot appear in a survey like this one.*

What is known about its shape, from `planning/curriculum/ANSWERS-3.md`:

- **The matrices strand** — six tutorials outlined in
  [The Matrices Strand](./outlines/matrices.md), ending in Markov chains rather
  than eigenvectors.
- **Six other strands the descriptor names** and nothing outlines: discrete
  probability and randomness, modelling and simulation, algorithms and
  complexity, applications of probability, problem definition and solution
  design, and reflection.
- Every worked example the descriptor names is a suggestion rather than a
  requirement. Cover the topics; choose the route.

One strand outlined, six not, and no measurement either way.

---

## If I had to order it

1. **The two everlearning conversions** — How We Got Here and When It Goes Wrong.
   Conversions rather than new writing, so they are the cheapest real progress
   available, and they close three PDP outcomes.
2. **Drawing Functions**, **Lines and Distances**, **The Unit Circle**. The
   spine everything else in Sections 3 and 4 hangs off, in the only order that
   works — each one is assumed by the next.
3. The short ones — Rearranging Formulae, When There Is No Answer, Parabolas,
   Drawing Sets, Logic and Truth — which can be written in any order and slotted
   in.
4. **Approaching a Limit** and **Rates of Change**, which need Drawing Functions
   and nothing else.
5. **Sine and Cosine Waves** and **Solving Triangles**, after The Unit Circle.
6. **The first practice set**, by hand, against whichever tutorial lands first.
   `planning/EXERCISES.md` says why one by hand comes before a converter.

The matrices strand and the rest of 5N0554 are a separate body of work, not the
next thing.
