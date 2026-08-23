# Open questions

Every project accumulates decisions that one person should not make alone, and
most of them get made anyway — quietly, by whoever happened to be writing the
code that afternoon. This file exists to catch those before they happen by
default.

It is for questions about dewlab itself: how it should behave, what it should
be built out of, what a student should see. Questions about a *particular*
tutorial belong with that tutorial.

## How to raise one

Write the question here and keep working. That order matters. A question that
stops the work costs a day; a question that is written down, shipped with a
stated assumption, and answered later costs almost nothing — and an assumption
someone can read is much easier to overturn than one buried in a commit.

Each question should say four things:

- **What is being asked**, concretely enough that someone can answer it without
  opening the repository.
- **What was assumed and built in the meantime**, so that "that's fine" is a
  complete answer and costs the person answering nothing.
- **What changing it later would cost** — the same accounting `DECISIONS_LOG.md`
  uses, because a cheap decision and an expensive one deserve different amounts
  of anyone's attention.
- **What it blocks**, if anything. Most questions block less than they appear
  to, and saying so plainly stops a small question holding up a large piece of
  work.

A question only its author can understand is a note, not a question.

## How answers land

Answer in this file, or in conversation with whoever is building. Either way
the answer ends up in three places, and that repetition is deliberate:

1. Here, with the question moved down to **Answered**, so the reasoning stays
   attached to the question that prompted it.
2. In `DECISIONS_LOG.md` as a numbered entry, so the decision is findable from
   the code that depends on it.
3. In the code or the documents themselves, which is the only place it actually
   takes effect.

A one-line answer is a complete answer.

---

## Open

### Coordinate geometry has no tutorial and no outline, and something already depends on it

**What is being asked.** Four Maths for IT outcomes — MIT-4.1 to 4.4, a line as
an equation, slope, midpoint and distance, and Pythagoras — have no tutorial and
appear in none of the ten proposals. Should coordinate geometry become the
eleventh proposal, with an outline written next?

The reason it is worth a question rather than a shrug: `angles-and-waves` is the
proposal that carries the unit circle, and you said in `ANSWERS-3.md` that
SOH-CAH-TOA needs "coordinates so we can have the unit circle". So a proposal
that exists is already building on a tutorial that does not.

**What was assumed and built in the meantime.** Nothing yet. The survey in
`planning/WHAT_IS_LEFT_TO_WRITE.md` names it as the first thing to write and
places it before Angles and Waves rather than after.

**What changing it later would cost.** Nothing structural — it is a proposal and
an outline, both of which are text. What it would cost is discovering it while
writing Angles and Waves and having to stop.

**What it blocks.** Angles and Waves, and therefore most of Section 4.

### Where do Venn diagrams go?

**What is being asked.** MIT-2.3, two and three set Venn diagrams, has no home.
`sets-as-sorted-lists` teaches sets and does not draw them; the proposed
`logic-and-truth` covers truth tables and De Morgan and does not draw them
either. Three options:

1. A section inside `logic-and-truth`. De Morgan's Laws are the natural pairing,
   because the picture is the proof — but it turns a short tutorial into a full
   one.
2. A section added to `sets-as-sorted-lists`, which exists already and already
   has the vocabulary. Cheapest, and it puts the picture where the sets are.
3. Its own short tutorial. Hard to justify for one outcome.

**What was assumed and built in the meantime.** Nothing. My preference is 2, on
the grounds that it costs one section in a tutorial that is already written.

**What changing it later would cost.** Small either way. Moving a section
between two tutorials is moving prose and two cells.

**What it blocks.** Nothing. It is the last uncovered outcome once the rest is
planned, and it can be decided when `logic-and-truth` is written.

---

## Answered

### How should mathematics be rendered?

**Settled: in the browser, from spans the build marks, using KaTeX.**

Mathematics matters here — most of the maths tutorials use notation, and a
maths tutorial that cannot show a fraction is not a maths tutorial. The
question was where the LaTeX gets turned into readable mathematics: during the
build, or in the student's browser.

Rendering during the build produces a static page and costs the student
nothing. But the tools that do it are JavaScript, and reaching them from a
Python build script means every build — and every author previewing locally —
needs a Node toolchain installed. The committed vendor bundle exists precisely
so that nobody needs one.

Rendering in the browser costs a 266 KB download, on the pages that have
mathematics and no others. Weighed against making every author install Node,
that is the cheaper side, and the decision was taken that way.

The build still does the hard half. It finds the mathematics and lifts it out of
the source before the markdown converter runs — without that, `$a_i + b_j$`
comes back with its subscripts turned into italics — and leaves the LaTeX in a
marked span. That span is both what KaTeX renders and what a reader sees if
JavaScript never loads, which is a far better failure than an empty gap.

Recorded as `DECISIONS_LOG.md` 1.8.

*Also asked at the time: could the Python runtime render it instead? It could,
but a prose-and-mathematics tutorial currently never starts that runtime at
all. Loading a Python interpreter to render `$x^2$` would cost several times
what KaTeX costs.*

### Should ordinary code blocks be syntax highlighted?

**Settled: yes, using the same highlighter as the live cells.**

Only editable cells were highlighted; illustrative code came out as flat text.
For a beginner that is a worse gap than it sounds — the two kinds of code look
different for a reason that has nothing to do with what they *are*.

A build-time highlighter would have worked, but it means a second colour scheme
to keep in step with the one the texture panel already switches between, and
two schemes drift. Illustrative blocks now get the same read-only editor
component, from the same theme, so one theme change repaints everything at once.

Recorded as `DECISIONS_LOG.md` 1.9.

### Where is this hosted, and does the build have to be JavaScript?

**Settled: GitHub Pages, built automatically on push. The build stays Python
for now.**

Pages plus an automated build is free, needs no server to maintain, and makes
publishing identical to committing — which is the property worth protecting,
because a build step someone has to remember is a build step that gets
forgotten.

A local preview is wanted, and there was a reasonable case that this forces the
build script into JavaScript. It does not, on its own: building and serving
locally is already a preview on any machine with Python installed. What Python
cannot give is a preview *inside* a browser-based editor, or on a machine with
no Python at all.

Whether that is worth rewriting the build is a real question, and it is left
open deliberately rather than answered early — the cost rises with everything
built on top of the current script, so it should be decided before the editor
is built, and not by accident before then.

Recorded as `DECISIONS_LOG.md` 1.10.
