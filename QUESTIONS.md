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

---

## Answered

### What is the right layout for a tutorial and the files that belong to it?

**Settled and built: every tutorial is a folder, from the moment it is
created — `DECISIONS_LOG.md` 7.90.**

A tutorial was a lone markdown file that grew a folder only on its second
release, and its practice page and glossary stayed behind at module level
when it did. Four tutorials already had their files split across two
directory levels, and every new release added another.

A tutorial is now `tutorials/<module>/<slug>/`, holding its markdown at
`<slug>.md`, its practice page, its glossary, any frozen past releases as
`v<version>.md`, and any pictures or recordings it uses. A tutorial with
one release and nothing else is a folder with a single file in it, which is
the normal case rather than an awkward one: nothing has to be rearranged
later to make room for a tutorial's own material.

Three things follow from it, and each was worth having on its own:

- **Versioning stops moving files.** `<slug>.md` is always the current
  release and `v<version>.md` is always a past one, so releasing adds a
  file and renames nothing. The authoring editor used to produce two
  different shapes depending on whether a tutorial had been released
  before; now there is one.
- **Assets have somewhere to live.** A file in the folder is copied to the
  site beside the tutorial, and a plain `src="picture.png"` resolves from
  the current release and every frozen one — which a hand-written path
  could not do, since the two are served from different depths. A
  reference to a file that is not there fails the build, as a dead
  `tutorial:` link already does.
- **A tutorial is one thing to move, freeze or delete.** It was several
  files in two places.

Nothing a student receives changed: page URLs and saved-work storage keys
are built from frontmatter, never from source paths, and the built site
came out byte-identical to the one before the migration.

### Is the build being rewritten in JavaScript?

**Settled: no, and the question is closed by events rather than by
argument.** `DECISIONS_LOG.md` 1.10 left this open deliberately, to be
decided "before the editor is built, and not by accident before then." The
editor has since been built, and needed none of it: `assets/editor.js`
reads and writes markdown through GitHub's API and never runs the build at
all. The one thing a JavaScript build would have added — a preview inside
the browser-based editor — the editor does without, by rendering prose
live in Milkdown and leaving the structural checks to `problems()`, which
reproduces the build's own rules client-side.

The cost of revisiting rises with everything built on the current script,
which is the reason the question had a deadline. Reopening it now would
need a reason the editor did not supply.

### Is moving Pyodide into a Web Worker worth it, to give a runaway cell a real Stop button?

**Settled and built: yes — DECISIONS_LOG.md 7.77.** Pyodide now runs off
the main thread on the hosted site (`assets/pyodide-worker.js`), with
`pyodide.setInterruptBuffer()` against a real `SharedArrayBuffer`, and
`coi-serviceworker` vendored to add the `Cross-Origin-Opener-Policy`/
`Cross-Origin-Embedder-Policy` headers GitHub Pages will not set directly.
Every place `tutorial-runtime.js` used to talk to Pyodide directly now has
a Worker-side counterpart behind a postMessage RPC, exactly as this
question anticipated. The offline standalone export keeps the old
main-thread path — it has no Stop button to justify the cost, and a
`file://` page cannot use a module Worker anyway.

### Should a module's series carry an explicit reading order, and should the reference panel cross series within one module?

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
`planning/REFERENCE_PANEL.md` §3/§4, `docs/WRITING_TUTORIALS.md`, and
`ARCHITECTURE.md` all
point to it by name as the way a glossary gets written, rather than
describing the YAML shape as something to fill in by hand.

### Does a mixed practice page's reference panel need curation, or is the raw union always right?

**Settled: fine as the raw union for now.** No change needed today.
Revisit with `.claude/skills/tutorial-glossary/SKILL.md` if a real
`practice_across` page's union ever looks too long in practice — the skill
can be pointed at a mixed page's actual accumulated list to judge whether
curation would visibly help, rather than deciding in the abstract.

### What should the reference panel become on a phone?

**Settled: a bottom sheet, mirroring `.dl-settings`' own existing mobile
treatment**, rather than hiding the panel outright. The toggle stays a
small fixed corner button at phone width; only the floating panel's shape
changes — `top: auto; bottom: 0; left: 0; right: 0`, the same rule
`.dl-settings` already had. `tests/e2e/test_reference.py`'s `TestMobile`
covers both: the toggle stays visible, and opening it produces a sheet
actually anchored to the bottom edge (asserted via `getComputedStyle`,
not just visually).

### Do pedagogical notes and datasets belong in the reference panel, or in a panel of their own? And is a second, left-anchored panel worth having?

**Settled and built: notes and datasets extend the existing reference
panel, as `planning/SIDEBAR_CONTENT.md` §4 recommended** — no third panel
for them. `DECISIONS_LOG.md` 7.74. Neither is cumulative across a series
the way the glossary is; both ride on the same manifest `glossary` already
uses, each with its own heading inside the panel so a reader does not
mistake a note for an examinable, taught term.

**The second, left-anchored panel is settled and built, but scaled down
from §4b's original sketch: series navigation only, not a duplicate of
the existing "Contents" table of contents.** `DECISIONS_LOG.md` 7.73. An
external PR (#65) moved the reference panel itself from right-anchored
to left-anchored while this was being designed, which took "left" off the
table as free space for a spatially separate panel — the series nav panel
instead shares that same anchor, stacked below the reference panel's
toggle, and joined the Settings/reference mutual-exclusion group as a third
member. The per-page table of contents (`render_toc()`) was left where it
already was — inline, at the top of the page — rather than duplicated
into this panel: it already answers "where am I on this page," and
duplicating it here would only add a second place to keep in sync for no
reader benefit.

### What should the contents page and a tutorial's own page show about a reader's progress?

**Settled and built**, per `planning/PROGRESS_INDICATORS.md` and
`DECISIONS_LOG.md` 7.70: a per-tutorial completion badge on the contents
page (`data-cells` at build time, a client-side read of the existing
saved-progress `localStorage` record, no new save format beyond one
`errored` boolean `saveNow()` now captures), plus a plain summary line
folded into the existing Settings panel on a tutorial's own page rather
than a new persistent bar. Grey/green, red reserved for a cell whose last
run actually errored. Only the contents-page badge has a Settings toggle
— the in-tutorial summary lives inside a panel a reader already chose to
open, so it needs no toggle of its own.

### Should the export nudge get more insistent than a first-use hint line?

**Settled and built**, per `planning/STUDENT_NOTES.md` §4's second, larger
proposal and `DECISIONS_LOG.md` 7.75: a small marker on the export button
once notes have grown by a rough threshold since the last export, rendered
as a coloured dot rather than a banner, cleared by an export, an import,
or "Start again." The baseline it compares against is not a new field on
the saved-progress record — that would conflate "as of the last autosave"
with "as of the last export" — but a small piece of per-tutorial state of
its own, tracked the same way `rememberVersion()` already tracks a
version pin. A Settings toggle turns it off entirely, the same shape the
progress badges toggle above already has.

### Is pre-run tooltip coverage (Jedi in Pyodide) worth its cost, or do the free extensions cover enough?

**Settled and built: all three — DECISIONS_LOG.md 7.76.** `planning/
CELL_TOOLTIPS.md`'s (a) and (b) shipped as planned (builtins in `docFor`,
signature help on typing `(`), and (c) — Jedi — shipped alongside them
rather than waiting, once prototyping it directly against dewlab's real
pinned Pyodide showed a genuine yes: `.help()`/`.get_signatures()` resolve
a function defined but never run, from source text alone, in low tens of
milliseconds warm. Live answers still win whenever the interpreter already
knows a name; Jedi only fills the gap live cannot reach.

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
