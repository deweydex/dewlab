# Status

What's actually built, what's still open, and the trickier design
decisions behind the parts that are done. This is a factual record, kept
current as things change — not a pitch.

---

## 1. What's built

### Core runtime (`assets/`, `setup/`, `data/`)
- **Pyodide in the browser**: real Python, running client-side, with
  `numpy`, `pandas` and `matplotlib` available by default, and `sympy`
  and others on request via a tutorial's `packages:` frontmatter
  (`assets/tutorial-runtime.js`).
- **The tools bridge**: `show`, `show_table`, `check`, `text_input`,
  `dropdown`, `button`, and `load_csv`, all defined once in
  `assets/tutorial_tools.py`.
- **Trimmed tracebacks**: an error a student causes is trimmed down to
  their own line, not buried under dewlab's own plumbing.
- **Saved work**: a student's code and its last output persist in the
  browser, keyed to `(module, slug)` — no server, no tracking.
- **Saved work across versions**: a tutorial with more than one release
  restores a student's answers by matching cell id, so an edit that
  doesn't touch a cell's id never loses what was written there.

### The build (`build.py`, `dev/`)
- **Frontmatter and cell parsing**: `python exec` fences, `hint:`,
  `{{include: ...}}`.
- **Maths pulled out before Markdown sees it**, so `$a_i$` never comes
  back with the subscript read as emphasis.
- **Link validation**: a `tutorial:slug#anchor` link that doesn't
  resolve fails the build — never a dead link on a live page.
- **Multiple releases**: the newest live release serves the plain URL;
  every past release stays reachable, frozen, at its own dated address.
- **Downloadable copies**: a standalone single-file HTML per tutorial,
  and a zip per series, both in `site/download/`.

### UI and navigation (`assets/`, `shell.html`, `tree.html`, `editor.html`)
- **The reading surface**: serif prose, generous margins, and reader
  controls for theme, font, size, and line width.
- **Contents and navigation**: an auto-built table of contents (with
  repeated sub-headings filtered out), a sticky masthead, module order
  from `tutorials/modules.yaml`.
- **The topic tree**: a visual map of outcomes, their prerequisites, and
  which tutorial teaches each one, with pan/zoom (`assets/tree.js`).
- **Browse by topic** (`topics.html`): the tree's sibling for a different
  question — not "what does this need first," but "everything about
  trigonometry, gathered in one place, in whatever order suits me."
  Curated groupings live in `planning/curriculum/topic-groups.yaml`,
  separate from the tree's own `topics.yaml`; see `write_topics_page()`
  in `build.py` for how the two differ.
- **The authoring editor**: a browser-based tool that reads and writes
  tutorials through GitHub's API — series reordering, frontmatter
  editing, a warning before a cell-id change strands saved work,
  structural checks, and opening a pull request. Its prose surface is a
  Milkdown (Crepe preset) block editor, vendored the same way CodeMirror
  and KaTeX are — see `REPO_AND_EDITOR.md` and `ARCHITECTURE.md` §3.
- **Progress indicators**: a contents-page badge per tutorial, and a
  plain summary line in a tutorial's own Settings (`PROGRESS_INDICATORS.md`,
  DECISIONS_LOG.md 7.70).
- **Student notes**: a free-text field saved alongside a tutorial's
  cells, distinct from the author-written pedagogical notes described in
  `SIDEBAR_CONTENT.md` (`STUDENT_NOTES.md`, DECISIONS_LOG.md 7.72/7.75).
- **Highlight to look up**: selecting a word the reference knows offers
  a small button that opens the panel filtered to it; selecting anything
  else does nothing at all (`REFERENCE_PANEL.md` §6b, DECISIONS_LOG.md
  7.93).
- **Where a term came from**: an inherited reference entry says which
  tutorial introduced it and links to that section (`REFERENCE_PANEL.md`
  §6c, DECISIONS_LOG.md 7.94).
- **Cell tooltips**: hover docs and signature help that cover Python
  builtins, not just a student's own names, falling back to Jedi's
  static analysis for code that hasn't run yet — live always wins when
  both have an answer (`CELL_TOOLTIPS.md`, DECISIONS_LOG.md 7.76).
- **A genuine Stop button**: on the hosted site, Pyodide runs inside a
  Web Worker (`assets/pyodide-worker.js`), so a truly stuck loop can
  still be interrupted via a real `SharedArrayBuffer` — see
  `CELL_CONTROLS.md` §2 and DECISIONS_LOG.md 7.77. The offline
  standalone export keeps Pyodide on the main thread and has no Stop
  button, on purpose (`ARCHITECTURE.md` §4).
- **A reader's own cells**: on any page that already has cells, a reader
  can add their own — Python or a short text note — right below any cell
  on the page, not just at the bottom, and share one as a small file
  someone else can load in. Kept fully separate from the tutorial's own
  saved work and version system, so it survives a tutorial update
  untouched (`PRACTICE.md` §3-5).
- **Print/PDF and a Jupyter notebook**: alongside the existing "Download
  to keep," a tutorial page's Settings offers "Print — or save as PDF"
  and "Save as a Jupyter notebook" (a page's cells, real and a reader's
  own alike — not the reading itself, which Print and Download to keep
  already cover).

### dewmini (`compose/dewmini.*`)
The one Python workspace with no tutorial attached — see
`ARCHITECTURE.md` §4 for how it's built.

dewmini runs Python through
`assets/pyodide-engine.js`, a shared Worker-based engine (a client of
`assets/pyodide-worker.js`, the same runtime tutorial pages use) — a
genuine Stop button, and real Jedi-backed autocomplete and signature
help. `compose/dewmini-fs.js` mounts a real local folder (File System
Access API), its own named OPFS subdirectory, or IDBFS — whichever the
browser supports — behind one interface, so the Workbench's Files
section, SQL support (`sqlite3` against a mounted `.db` file), and file
uploads all work the same way regardless of backend. `.ipynb`/`.py`
import and export round it out, and dewmini has its own downloadable,
offline-capable copy (`write_dewmini_bundle()` in `build.py`). How it
came to be dewlab's one and only workspace is history, not status:
`DECISIONS_LOG.md` 7.87–7.98 and the addenda in
`planning/MINI_IDE_AND_DEWMINI_NEXT.md` hold that story.

Since `DECISIONS_LOG.md` 7.99 it is a workbench rather than a single
column: notebooks open in **tabs**, and two docked rails carry what a
tutorial page has no need of — a **Library** on the left (the
cross-tutorial reference built by `write_reference_index()`, a dataset
catalogue, and the help that used to be its own panel) and a
**Workbench** on the right (a live variable inspector reading
`tutorial_tools.describe_globals()`, notes, and files). Both are shut
until asked for, which is what keeps the five-second version of dewmini
intact; `planning/DEWMINI_WORKBENCH.md` is the design and its reasoning.

### Documentation and code comments
Every substantial code file has detailed, teaching-oriented inline
comments and a matching `docs/<file>-explained.md` walking through its
structure — `CONTRIBUTING.md` makes keeping both current a standing
requirement for future changes, the same way the build already enforces
that links and folds can't go stale.

### Curriculum modules (`tutorials/`)
- **113 published tutorial and practice pages** across three modules —
  see `EXERCISES.md` for where the problems came from.
  - `computational-methods` (15 tutorials, 15 practice pages): `first-steps.md`,
    `working-with-tables.md`; the `matrices` series —
    `grid-of-numbers.md`, `multiplying-grids.md`,
    `what-a-matrix-does-to-a-picture.md`, `undoing-it.md`,
    `solving-systems.md`, `where-chains-lead.md`; the `simulation`
    series — `leaving-it-to-chance.md`, `counting-darts.md`,
    `a-model-that-corrects-itself.md` (a from-scratch perceptron),
    `when-a-queue-never-clears.md`; the `algorithms` series —
    `three-ways-to-make-change.md` (brute force, memoization, a greedy
    heuristic), `finding-everything-inside-a-folder.md` (trees,
    recursion vs. iteration); and the `problem-solving` series —
    `finding-where-it-went-wrong.md` (problem definition, symptom vs.
    root cause, the personal attributes behind debugging).
  - `fundamentals-of-oop` (9 tutorials, 7 practice pages, 1 mixed
    practice-across page): the `programming-with-objects` series —
    `the-moves-you-already-know.md`, `objects-and-classes.md`,
    `the-tools-around-your-code.md`, `one-class-many-methods.md`,
    `one-parent-many-children.md`, `testing-what-a-class-does.md`,
    `documenting-a-class.md`, `a-front-end-for-a-class.md`, and
    `mixed-programming-with-objects.md` (the practice-across page).
  - `mit-pdp-maths-prog-integration` (67 tutorial and practice files):
    - *Foundations & Programming Spine*: `first-steps.md`,
      `storing-and-computing.md`, `making-decisions.md`,
      `repeating-yourself.md`, `lists-and-sequences.md`,
      `finding-things.md`, `putting-things-in-order.md`,
      `building-reusable-tools.md`, `how-we-got-here.md`,
      `when-it-goes-wrong.md`, `the-team-project.md`.
    - *Discrete Math & Statistics*: `counting-carefully.md`,
      `what-are-the-chances.md`, `making-sense-of-data.md`,
      `pictures-worth-numbers.md`, `numbers-and-their-families.md`,
      `sets-as-sorted-lists.md`, `logic-and-truth.md`,
      `venn-diagrams.md`.
    - *Algebra, Functions & Calculus*: `expressions-come-alive.md`,
      `cracking-equations.md`, `rearranging-formulae.md`,
      `complex-roots.md`, `drawing-functions.md`, `parabolas.md`,
      `approaching-a-limit.md`, `rates-of-change.md`.
    - *Geometry & Trigonometry*: `lines-and-distances.md`,
      `the-unit-circle.md`, `sine-and-cosine-waves.md`,
      `solving-triangles.md`.
    - *Synthesis & Review*: `bringing-it-all-together.md`,
      `critique-and-reflection.md`.
    - *Interactive Practice Companions*: one `<slug>-practice.md` beside
      every tutorial above except `bringing-it-all-together`,
      `critique-and-reflection`, and `the-team-project`.
    - *Mixed Problem Sets*: `mixed-programming.md`, `mixed-algebra.md`,
      `mixed-trigonometry.md`, `mixed-data.md`.

### Curriculum coverage (`CURRICULUM_MAP.md`)
**All 91 learning outcomes across all four accredited modules are
written, mapped, and tested** — *Mathematics for IT (5N18396)*,
*Programming and Design Principles (5N2927)*, *Fundamentals of Object
Oriented Programming (5N0541)*, and *Computational Methods and Problem
Solving (5N0554)*. No gaps in any descriptor. `CURRICULUM_MAP.md` is
regenerated from the tutorials themselves and is the source of truth;
this file only narrates it.

---

## 2. What's still open

### Computational Methods (5N0554) curriculum — **all 13 outcomes now taught**
Every outcome in *Computational Methods and Problem Solving 5N0554*
now has a tutorial section teaching it, per `CURRICULUM_MAP.md`. What
actually closed each one, strand by strand:

1. **Linear Algebra & Matrix Operations** — six tutorials (*A Grid of
   Numbers* through *Where Chains Lead*), series `matrices`. `CMPS-LO4`
   fully taught; `CMPS-LO1` and `CMPS-LO2`'s data-structures/randomness
   halves surfaced here first but weren't the whole outcome yet.
2. **Discrete Simulation & Monte Carlo Methods** — *Leaving It to
   Chance* and *Counting Darts* (estimating $\pi$, why more samples
   isn't reliably better — now with an added section distinguishing
   *accuracy* from *precision*, closing `CMPS-LO13`); *A Model That
   Corrects Itself* (a from-scratch perceptron, closing `CMPS-LO7` and
   `CMPS-LO11`); *When a Queue Never Clears* (queueing stability,
   closing `CMPS-LO6`). Series `simulation`.
3. **Algorithms** (new series) — *Three Ways to Make Change* (brute
   force vs. memoization vs. a greedy heuristic, closing `CMPS-LO9`,
   and tagging `finding-things.md`/`putting-things-in-order.md`'s
   existing search/sort complexity coverage as `CMPS-LO5`, already
   taught there in substance); *Finding Everything Inside a Folder*
   (trees, recursion vs. iteration, closing `CMPS-LO1`).
4. **Problem Solving** (new series) — *Finding Where It Went Wrong*
   (one buggy pipeline carrying problem definition/testing `CMPS-LO8`,
   symptom-vs-root-cause `CMPS-LO10`, and the personal attributes
   behind debugging `CMPS-LO12`).

**Loose ends the outcome closure didn't resolve, worth knowing about
even though nothing blocks on them:**
- **Half-closed: a real dataset is finally in use.** The new *Text
  Generation* series (`computational-methods`; *A Chain Reads a Book*,
  *How Much It Remembers*, *Whose Voice Is This*) genuinely exercises
  `data/`, the `datasets:` frontmatter, `check_datasets()`, and sidebar
  attribution, via a new sibling to `load_csv()` — `load_text()` —
  across six bundled public-domain books. `load_csv()` itself, and
  `co2-emissions.csv`/`life-expectancy.csv` specifically, are still
  unclaimed — the apparatus is proven, but not yet for tabular data.
  ROADMAP.md's Phase 2 has the fuller account.
- **The link-graph strand's crawl is still just the worked three-page
  PageRank example** inside *Where Chains Lead*, deliberately: a first
  design for a real crawl was set aside as too advanced for now, and
  the Markov-chain series above was built in its place, extending the
  same tutorial's other worked example instead. `CMPS-LO4` doesn't
  need the crawl, but it's still a gap in ambition rather than in
  coverage.
- **`CMPS-LO2` and `CMPS-LO1`'s topics.yaml sub-parts** (grids, trees,
  recursion) are each taught in the tutorial that introduces that
  specific representation, not gathered into one dedicated "data
  structures" tutorial — worth a look if a QQI verification visit ever
  wants to see them side by side.

### Automated worksheet-to-practice converter (unwritten)
On hold, and possibly not needed. The worksheets whose material is
taught have already been converted by hand; the ones that remain
(`07a`–`08b`, matrices, Markov chains, Bayes, distributions) cover
material no tutorial teaches yet, and six of those carry their answer
keys only as PDFs. There's nothing for the converter to convert until
that material is written.

### CI/CD deployment
**Done.** `.github/workflows/deploy.yml` builds and publishes the
148-page site to GitHub Pages on every push to `main`. Two more
workflows guard it: `tests` runs the unit suite, and
`standalone-bundle-is-current` fails if the vendored bundle has drifted
from `vendor-src/`.

---

## 3. Trickier decisions, briefly

**Saved work has to survive a live cohort.** A student working through a
multi-month course must never lose their progress or see a broken
indicator. Storage keys are scoped exactly to
`dewlab:progress:<module>:<slug>`, cell ids are treated as immutable
once published, and the authoring editor actively warns before a change
that would rename one.

**Two students, two versions, no interference.** A cohort working in an
earlier release (say `2026.08.20.1`) should have a stable, undisturbed
experience for the rest of their term, even as new releases ship. The
plain unversioned URL always serves the newest release; a returning
student is automatically kept on the release they were already working
in, with an honest count of how many of their answers carry over.

**Sharing code between students has to be safe on a shared machine.**
Pyodide runs entirely inside the browser tab's WebAssembly sandbox, with
no access to the local filesystem or operating system — so a student
running code someone else wrote can't do anything to the machine it's
running on.
