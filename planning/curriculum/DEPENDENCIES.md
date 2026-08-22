# Three ways of saying what comes first

Not a running order. You were explicit about that, and it changed what this
document is for:

> This is about giving students the opportunity to jump around, to find places
> where they struggle, and also allow teachers to understand, okay, I've gotta
> cover these things eventually, but maybe there's a nice opportunity in a week
> at the end of a quarter to fit something in.

So a dependency here answers **"can I start this now?"** — for a student picking
their next thing, and for a teacher with a spare week looking for something that
will land. Not "what does the class do in September".

That distinction decides everything below. A route wants few branches and one
clear line. A *reachability* map wants the opposite: as few edges as it can
honestly get away with, so that as much as possible is open at any moment.
**Every edge you add closes a door.**

Below are three trees built on three different rules for adding an edge, the
places they disagree, and which one I would ship.

---

## What is wrong with the tree we have

It was written topic by topic — "what does this one obviously need?" — which
produces edges that are individually reasonable and collectively arbitrary.

Your example is the clean demonstration. **Calculus needs quadratics**, and
nothing in the current data says so: limits point at graphing, graphing points
at functions and at multiplying out. The chain happens to work, but the fact
you actually care about — that a student should have met a parabola before
meeting a derivative — is nowhere.

The result is 14 roots and a longest path of 6, with stretches in the middle
where the ordering is invented rather than real.

---

## Tree A — Strictly impossible without

**Rule for an edge:** you literally cannot do the later topic without the
earlier. Not "would struggle". Cannot.

- **Shape:** shallow and wide. Around 20 roots, longest path 4.
- **Reads as:** almost everything is open almost always.
- **Good for:** a student jumping around; a teacher slotting something into a
  spare week.
- **Bad for:** telling anybody where to go next, because everything is
  available and nothing is recommended.

**What it drops from today's tree:** the derivative would no longer need
graphing (you can define it as a limit of a difference quotient without ever
drawing one), and searching and sorting would no longer need divide and conquer.

Both of those are true and both are worse teaching.

## Tree B — Would struggle without

**Rule for an edge:** a student who has not met the earlier topic will find the
later one harder than it needs to be — even where it is technically possible.

- **Shape:** deep and narrow. Around 8 roots, longest path 8 or 9.
- **Reads as:** a strong recommendation, close to a route.
- **Good for:** a student who wants to be told what to do next.
- **Bad for:** exactly what you asked for. It closes most doors, and a teacher
  looking for something that fits in one spare week will find almost nothing
  reachable.

**Your trigonometry example is the test.** Under B, SOH-CAH-TOA needs
coordinate graphing and probably functions. Under A it needs only Pythagoras.
You said it yourself: *"you can do some trigonometry without doing functions and
without doing coordinates, but I don't know how much."* B answers that question
one way and A the other, and neither is obviously right.

## Tree C — Five gateways

**Rule for an edge:** there are a small number of topics that genuinely unlock
large parts of the course. Everything else hangs off a gateway, and edges
between non-gateways are added only where the dependency is glaring.

The five, proposed:

| Gateway | Unlocks |
|---|---|
| **Expressions and equations** (`MIT-1.5`) | All of algebra, and every formula anywhere |
| **Functions and inverses** (`MIT-3.1`) | Graphing, calculus, and how a program is organised |
| **Graphing functions** (`MIT-3.2`) | Trigonometry as curves, limits, the derivative |
| **Lists and arrays** (`MIT-6.3`) | Every algorithm, and all of statistics |
| **The parts of a program** (`PDP-LO4`) | Everything anybody writes |

- **Shape:** two or three layers under each gateway. Longest path 5, measured.
- **Reads as:** "there are five things you want early; after that, range freely."
- **Good for:** all three of your uses at once. A student sees five landmarks
  rather than sixty-seven arrows. A teacher can check the five are covered and
  relax about the rest. Someone doing well can see which gateway opens the
  direction they want.
- **Bad for:** it is a simplification, and there will be pairs where the honest
  answer is an edge that C does not draw.

---

## Where they disagree, and where I am unsure

These are the ones worth your eye rather than mine.

| Question | A | B | C | Note |
|---|---|---|---|---|
| Does **SOH-CAH-TOA** need coordinate graphing? | No | Yes | No | Your open question. C says a right-angled triangle is a picture, not a graph. |
| Does **the derivative** need quadratics? | No | Yes | **Yes** | You raised this and I think you are right. A curve you have drawn is what makes a tangent mean anything. |
| Does **searching and sorting** need divide and conquer? | No | Yes | No | Binary search is the reason to care about divide and conquer, so this may be backwards in all three. |
| Does **statistics** need lists? | Yes | Yes | Yes | Nobody disagrees. |
| Does **truth tables** need sets? | No | Yes | No | They rhyme, and neither needs the other. B draws it, and I think B is wrong here. |
| Does **combinations** need factorials? | Yes | Yes | Yes | Agreed. |
| Does **complex roots** need number families? | Yes | Yes | Yes | Agreed. |
| Does **trigonometric graphing** need the unit circle? | Yes | Yes | Yes | Agreed. |
| Where does **matrices** attach? | — | — | — | Not in the data yet. See below. |

**Two I am genuinely unsure about:**

1. **Divide and conquer versus binary search.** Every tree above had divide and
   conquer come first, because that is how it is usually taught. But a student
   meets binary search first and *then* has a reason to name the idea — the same
   discover-then-name principle you applied to the chain rule. **I have turned
   this edge around in what shipped**: searching and sorting is now a root, and
   divide and conquer hangs off it. If you disagree, it is one line in
   `topics.yaml` (`MIT-6.6`) and I will put it back.

2. **Whether graphing is one gateway or two.** Drawing a function and reading
   answers off it are different skills. C treats them as one gateway; splitting
   them would add a layer but might be more honest.

---

## Matrices, which are not here yet

You asked for computational-methods tutorials on material not in Maths for IT,
starting with matrices — the operations coded by hand, and what different
mappings do to space.

That is a separate strand with its own internal order, and it attaches to the
rest at exactly two points: **lists and arrays** (a matrix is a list of lists
before it is anything else) and **coordinate geometry** (a mapping skews a plane
you already know how to draw). Both are gateways or near them under C, which is
mild evidence that C is carving in the right places.

Sketched separately in `planning/outlines/matrices.md`.

---

## What C actually measures, once built

Estimates above; these are counted from `topics.yaml` as shipped.

| | Old tree | Tree C |
|---|---|---|
| Topics | 67 | 67 |
| Edges | 63 | 64 |
| Roots (open from a standing start) | 14 | **15** |
| Longest path | 6 | **5** |

Tier sizes, where tier 0 is "needs nothing":

| Tier | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Topics | 15 | 23 | 15 | 7 | 6 | 1 |

**Not the result I expected, and worth saying so.** I assumed C would cut edges
and it added one. What actually changed is where the edges point: the longest
path dropped from 6 to 5 and one more topic became open from a standing start,
because the edges C removes are the deep ones in the middle of chains and the
edges it adds are shallow ones onto gateways. Fewer arrows was never the goal —
less *depth* was, and that is what moved.

**One thing the measurement disagrees with.** Ranking every topic by how much it
transitively unlocks does not quite produce the five gateways I proposed:

| Unlocks | Topic |
|---|---|
| 18 | Expressions and equations (`MIT-1.5`) — gateway |
| 8 | The parts of a program (`PDP-LO4`) — gateway |
| 8 | Lists and arrays (`MIT-6.3`) — gateway |
| 8 | Functions and inverses (`MIT-3.1`) — gateway |
| **7** | **Pythagoras (`MIT-4.4`) — not a gateway** |
| **7** | **Expanding and simplifying (`MIT-1.6`) — not a gateway** |
| 5 | Graphing functions (`MIT-3.2`) — gateway |

Graphing is the weakest of the five by this measure, and Pythagoras outranks it.
I have left the five as proposed, because Pythagoras unlocks one strand
(trigonometry) whereas graphing unlocks three that do not otherwise touch
(trigonometry, calculus, and reading answers off a picture) — breadth matters
more than count for a landmark. But it is a judgement, not a measurement, and
you may want Pythagoras named as a sixth.

---

## What I would ship

**Tree C**, and it is what shipped. It is the only one of the three that serves
the thing you actually described — a student finding where to go next, and a teacher finding what fits
— rather than a sequence dressed up as a map. A is honest and useless; B is
useful and closes the doors you wanted open.

With **the derivative needing quadratics** added, because you are right and all
three trees were poorer without it.

I will implement C, keep A and B recorded here, and leave the disagreements
above visible on the map rather than silently resolved — an edge somebody
disagrees with is more useful when it is labelled as one.


---

## What the map does with this

The tree page now **reads downwards**: nothing in the top row needs anything, and
no arrow ever points upwards. Each tier is a labelled stripe — "start anywhere
here", then "one layer down" and so on — so the depth means something without
anybody having to decode a tier number.

Subject stopped being an axis. The first attempt gave each of the twelve
subjects its own column and measured 5854px wide against 756px tall, which is a
horizontal tree in a hat. Subject is now a sort within a tier plus a colour on
each node, and the tree is 1058 × 1768 — tall, and it fits a phone.

Choosing a topic now also answers **"where can I go next?"**, which is the
question you actually posed. The panel lists what a topic opens up as well as
what it needs, so a student who already knows something can see what that buys
them. Both lists are clickable.
