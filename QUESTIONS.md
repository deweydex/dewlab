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

### Is pre-run tooltip coverage (Jedi in Pyodide) worth its cost, or do the free extensions cover enough?

`planning/CELL_TOOLTIPS.md` surveys what is available for cell tooltips.
Two pieces close real gaps for free — widening `docFor` to also answer for
Python builtins, and a CodeMirror signature-help tooltip on typing `(`,
both reusing data already available from the live interpreter (`inspect`)
with no new dependency. A third piece, Jedi run inside Pyodide itself
(pure Python, already in Pyodide's own package index, and the same
combination JupyterLite's official Pyodide kernel uses in production),
would additionally cover hover/completion for a name **before** its
defining cell has run — but as a real new dependency downloaded on every
page with a cell, running alongside `docFor`'s live introspection rather
than replacing it.

**Assumed and built in the meantime:** nothing implemented yet — this was
a research task, not a build one. No cell today gets a tooltip it did not
already have before this question was raised.

**Cost to change later:** small either way. Building (a) and (b) first
does not foreclose adding Jedi later — they answer different questions
(live vs. static) and can coexist; nothing about building the free pieces
first would need undoing to add Jedi afterward.

**Blocks:** nothing — cells work exactly as before until this is answered
and acted on.

### Do pedagogical notes and datasets belong in the cheat sheet panel, or in a panel of their own?

`planning/SIDEBAR_CONTENT.md` designs a second sidebar's worth of content —
pedagogical notes authored as `<aside class="dl-note">` (reusing the
hint/answer fold's own already-proven pattern rather than a new fence tag),
and datasets with attribution (`data/ATTRIBUTION.yaml` plus a `datasets:`
frontmatter list; the runtime fetch mechanism, `load_csv()`, already
exists and is simply unused so far). It recommends surfacing both as new
sections inside the *existing* cheat-sheet panel — "or, better yet, in
the other side bar," as floated when this was raised — rather than a
third floating panel, since that reuses the toggle, the panel, and the
open/close wiring 7.64/7.65 already shipped.

**Assumed and built in the meantime:** nothing implemented — this was a
design task. No note, dataset, or panel section exists yet.

**Cost to change later:** small for the panel-vs-panel question (a CSS/JS
change to the container, not to how notes or datasets are authored or
extracted). Larger for the authoring-mechanism question (fence vs. HTML
aside) once tutorials have actually been written using one — same shape
as the YAML-vs-markdown glossary question above, cheaper the earlier it is
settled.

**Blocks:** nothing today — building §2's dataset pieces (frontmatter +
attribution file) does not require the notes question to be settled
first, since they are independent additions to the same panel either way.

---

## Answered

### Should a module's series carry an explicit reading order, and should the cheat sheet cross series within one module?

**Settled: series may cross within a module; never across modules.**

`tutorials/<module>/series.yaml` (`build.py`'s `module_series_order()`,
`series_chain()`, `check_series_order()`) optionally lists a module's
series in accumulation order — a series listed there inherits every
earlier listed series' own glossary too, not just its own. A series left
off the list (or a module with no file at all) keeps series-only
accumulation, which is what let `reflections-and-review` in
`mit-pdp-maths-prog-integration` stay exactly as it was: that series
already has its own documented reason for having no fixed position
("revisited whenever a reader wants," its own `.order.yaml`'s comment),
so it is deliberately never listed anywhere.
`tutorials/computational-methods/series.yaml` now lists
`python-fundamentals` before `matrices`, so a matrices tutorial's cheat
sheet carries fundamentals' vocabulary too.

Recorded as `DECISIONS_LOG.md` 7.66.

### Is a structured YAML glossary file the right format, or did "a markdown file" mean the glossary content itself?

**Settled: YAML, as already built** — the request's "markdown file" meant
the skill itself (`SKILL.md` is how a Claude Code skill is written), not a
requirement on the glossary's own output format. The one thing asked for
alongside confirming this: make sure writing a glossary is well documented
with the skill highlighted as the tool that makes it easy, so YAML's
structure is never something an author has to hand-write from a blank
page. `.claude/skills/tutorial-glossary/SKILL.md` is that documentation —
`planning/CHEAT_SHEETS.md` §3/§4, `README.md`, and `ARCHITECTURE.md` all
point to it by name as the way a glossary gets written, rather than
describing the YAML shape as something to fill in by hand.

### Does a mixed practice page's cheat sheet need curation, or is the raw union always right?

**Settled: fine as the raw union for now.** No change needed today.
Revisit with `.claude/skills/tutorial-glossary/SKILL.md` if a real
`practice_across` page's union ever looks too long in practice — the skill
can be pointed at a mixed page's actual accumulated list to judge whether
curation would visibly help, rather than deciding in the abstract.

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
