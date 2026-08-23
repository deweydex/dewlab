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

*Nothing waiting.*

---

## Answered

### Coordinate geometry has no tutorial and no outline, and something already depends on it

**Settled: its own tutorial, and the describing comes first.**

Josh: *"for coordinate geometry, I think we just need to figure out ways of
describing that. And, yes, I think that's a very important thing to discuss."*

So `MIT-4.1` to `4.4` become [Lines and Distances](planning/outlines/lines-and-distances.md),
sitting between Drawing Functions and Angles and Waves rather than folded into
either. Pythagoras is one of the six gateways in the topic tree, and a gateway
that exists only as somebody else's third subsection is not a gateway.

The outline is mostly about how to describe the material, because that is what
was asked for: what to call it, which of the three descriptions of a line comes
first and why the general form arrives last, whether slope is named as
rise-over-run or as a rate of change, and why distance should come before
Pythagoras rather than after.

`MIT-4.9` went with it as far as needing a home, and got a separate short
tutorial after Angles and Waves — it needs the ratios, which arrive there.

### Where do Venn diagrams go?

**Settled: a small tutorial of its own, linked rather than merged.**

Josh: *"we can make a little separate tutorial about Venn diagrams. That's
totally fine. If you wanna connect it to DeMorgan's and also connect it to
sets-as-sorted-lists, that's fine. But again, those can be connections. We don't
need to do combinations here."*

Neither of the two options I offered, and the better answer. Both of mine folded
it into an existing tutorial; this keeps three whole things and links them.

It also reverses an entry in `out-of-scope.yaml`, which had ruled Venn diagrams
out as a pen-and-paper convention adding notation rather than understanding. The
reversal answers that rather than overruling it: what comes back is the picture
drawn by matplotlib from real sets — output rather than convention — and the
point at which three sets stop fitting in a person's head. The outline is
[Drawing Sets](planning/outlines/venn-diagrams.md).

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
