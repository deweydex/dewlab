# Do the 18 root topics really need nothing?

A first pass over every topic in `topics.yaml` that declares no prerequisite.
Three Haiku agents, six topics each, each given all 92 topics as the pool it
could draw a prerequisite from.

**Nothing here has been applied.** Every row is a proposal to accept or reject.

## What it found

| Topic | Verdict | Proposed prerequisite | Confidence |
|---|---|---|---|
| MIT-4.4 Pythagoras | missing | PRE-1 Kinds of triangle | high |
| MIT-5.6 Probability as a scale | missing | MIT-5.1 Listing outcomes | high |
| FOOP-LO5 Working in a development environment | missing | PDP-LO4 The parts of a program | high |
| FOOP-LO5 Working in a development environment | missing | PDP-LO10 Testing and debugging | high |
| CMPS-LO12 Personal attributes in problem-solving | not a topic | — | — |
| MIT-1.1 Powers and logarithms | root, unconfirmed | — | — |
| MIT-1.2 Area and perimeter | root, unconfirmed | — | — |
| MIT-1.4 Binary and hexadecimal | root, confirmed by hand | — | — |
| MIT-1.5 Expressions and equations | root, unconfirmed | — | — |
| MIT-2.1 Number families | root, unconfirmed | — | — |
| MIT-2.4 Truth tables | root, unconfirmed | — | — |
| MIT-4.5 Degrees and radians | root | — | — |
| PRE-1 Kinds of triangle | root | — | — |
| MIT-5.1 Listing outcomes | root | — | — |
| MIT-5.9 Kinds of data | root | — | — |
| MIT-6.1 What an algorithm is | root | — | — |
| MIT-6.3 Lists and arrays | root | — | — |
| PDP-LO1 The history of programming | root | — | — |
| PDP-LO4 The parts of a program | root | — | — |

So 18 roots become about 14, not 5. The instinct that 18 was too many is right;
the scale of the error is smaller than it looks.

## The four proposed edges, and why

**MIT-4.4 needs PRE-1.** The Pythagoras tutorial says "right-angled triangle"
throughout and its practice page asks whether a triangle is isosceles. Neither
is answerable without the naming topic. PRE-1 exists in the file for no other
purpose, and is currently wired to right-triangle trigonometry instead. This
one looks like a wiring error rather than a judgement call.

**MIT-5.6 needs MIT-5.1.** A probability is a count of favourable outcomes over
a count of all of them. The scale from zero to one means nothing until a
student can list what could happen.

**FOOP-LO5 needs PDP-LO4 and PDP-LO10.** You cannot see why autocomplete helps
until you know what code looks like, and the topic's own description says a
debugger is for "following a program step by step when reading it is not
enough", which is debugging.

## CMPS-LO12 should come off the map

Its own description says none of it is a technique you can be taught. It has no
prerequisites and nothing depends on it, so it sits alone on the tree. It is a
real learning outcome and belongs in `outcomes.yaml`; it is not a node with
arrows.

## What this pass taught us about running the next one

Depth of investigation predicted whether an agent found anything.

| Batch | Tool calls | Real edges found |
|---|---|---|
| Two | 26 | 2 |
| One | 4 | 0 |
| Three | 2 | 1 |

The batch that read the actual tutorials found real edges. The batch that read
only `topics.yaml` returned "genuine root" for all six. Reading the tutorial has
to be required, not optional, because whether an edge exists depends on how the
topic is taught.

That is the sharper finding here. Binary and hexadecimal needs powers of two as
mathematics, and does not as dewlab teaches it: the tutorial converts by
repeated doubling and never mentions a power. `topics.yaml` says its `needs`
are "about the mathematics rather than about the order we happen to teach in".
Those two rules disagree on this topic, and the rule needs settling before a
larger audit runs, because it decides which answer is correct.

The example problems were the weakest output everywhere. One offered a 3D
renderer optimising shading by triangle symmetry as an example of naming
triangles. Examples want their own pass, with a tighter prompt, checked against
the tutorials rather than invented.

## Alternative names worth keeping

- MIT-1.4 → How computers count: binary and hexadecimal number bases
- MIT-1.1 → Exponents, and finding powers with logarithms
- MIT-6.1 → Step-by-step instructions that need no judgement
- MIT-6.3 → Storing many pieces of data under one name
- PDP-LO1 → Where programming languages came from
- PDP-LO4 → The basic building blocks of any program
- FOOP-LO5 → Using an editor, running code, and debugging
