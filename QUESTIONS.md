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

### Should a module's series carry an explicit reading order, and should the cheat sheet cross series within one module?

A tutorial's cheat sheet (`planning/CHEAT_SHEETS.md`) draws from everything
earlier in its own series (`order.yaml`), because that is the only ordering
the build actually has. Series within a module have no defined order —
`write_index()` lists them alphabetically — even though, e.g.,
`computational-methods`' Matrices series plausibly comes after its Python
fundamentals series for a student working through the module in the obvious
way.

**Assumed and built in the meantime:** scope stays inside one series. A
matrices tutorial's cheat sheet will not include anything Python
fundamentals introduced, even if a reader met it first.

**Cost to change later:** small if it happens before many glossaries exist —
one field (`order.yaml` gaining a module-level series sequence, or an
explicit `after: python-fundamentals` on a series) and a build.py change to
walk it. Larger once dozens of glossary files exist and some entries turn
out to already be covered by an earlier series — those would need pruning,
not just the assembly logic changing.

**Blocks:** nothing today. It only produces a cheat sheet that is narrower
than it could correctly be, never one that shows something too early.

### Is a structured YAML glossary file the right format, or did "a markdown file" mean the glossary content itself?

The request described the glossary as something a skill produces "as a
markdown file." `planning/CHEAT_SHEETS.md` §3 instead specifies YAML
(`<slug>.glossary.yaml`, `term`/`kind`/`definition`/`example` fields) — read
as "the *skill* is written as a markdown file," which is simply how a
Claude Code skill (`SKILL.md`) works, rather than as a requirement on the
glossary's own output format.

**Assumed and built in the meantime:** YAML output, because build.py needs
to parse it structurally (group by `kind`, walk it in `order.yaml` order)
and a freeform markdown glossary would need its own parser to do the same
job less reliably.

**Cost to change later:** moderate — every already-generated `.glossary.yaml`
would need converting (mechanical, scriptable) or the build's parser would
need to grow a second input format. Cheaper the earlier it happens, same as
the schema question in §7 of the spec.

**Blocks:** nothing yet — no glossary files exist before the schema PR
lands, so there is nothing to convert if the answer is "markdown after all."

### What should the cheat sheet become on a phone, later?

`planning/CHEAT_SHEETS.md` §6 hides the toggle entirely under the existing
34rem phone breakpoint, matching the request's own "we wouldn't have this
option [on mobile], but maybe we can do that later." What "later" should
look like is not decided: a bottom sheet like `.dl-settings` already becomes
on a phone, a plain link to a standalone per-tutorial glossary page, or
something else.

**Assumed and built in the meantime:** nothing on mobile, matching the
request exactly.

**Cost to change later:** small — the panel's content and the data feeding
it are unaffected either way; only its container needs a phone-specific
layout, and `.dl-settings`'s own mobile CSS is a template already sitting in
the codebase.

**Blocks:** nothing — a phone reader today sees the page exactly as before
this feature existed.

### Does a mixed practice page's cheat sheet need curation, or is the raw union always right?

`practice_across` lets one practice page test several tutorials at once
(`build.py`'s `practice_pairs()`/`mixed_practice()`). §2 of the spec unions
every named tutorial's cumulative cheat sheet for such a page. If a mixed
practice page spans much of a series, that union could be long enough that
"a cheat sheet" stops being the right word for it.

**Assumed and built in the meantime:** the raw union, uncapped — simplest
to build, and never wrong in the sense that matters (nothing forward-looking
ever appears), only potentially long.

**Cost to change later:** small — a length cap or a "most relevant" ranking
is a filter applied after the union is already computed, not a change to how
the union itself is built.

**Blocks:** nothing — no `practice_across` page currently spans enough of a
series for this to have been checked against a real, long example.

---

## Answered

### Coordinate geometry has no tutorial and no outline, and something already depends on it

**Settled: its own tutorial, and the describing comes first.**

Outcomes `MIT-4.1` to `4.4` form [Lines and Distances](planning/outlines/lines-and-distances.md),
sitting between Drawing Functions and Angles and Waves rather than folded into
either. Pythagoras is one of the six gateways in the topic tree, and a gateway
requires a dedicated tutorial rather than an embedded subsection.

The outline focuses on pedagogical descriptions: naming conventions, ordering
linear representations ($y = mx + c$ before general form $ax + by + c = 0$),
framing slope as rise-over-run and rate of change, and sequencing distance
alongside the Pythagorean theorem.

`MIT-4.9` (angle of elevation and depression) is sequenced as a separate short
unit after Angles and Waves to build directly on trigonometric ratios.

### Where do Venn diagrams go?

**Settled: a small tutorial of its own, linked rather than merged.**

Venn diagrams (`MIT-2.3`) are structured as a dedicated modular tutorial
([Drawing Sets](planning/outlines/venn-diagrams.md)), connected via cross-links
to *Logic and Truth* and *Sets as Sorted Lists*.

This keeps three self-contained modules linked cleanly. Matplotlib draws
the diagrams directly from set operations in code, framing the diagram as
computed visual output rather than manual notation.

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
