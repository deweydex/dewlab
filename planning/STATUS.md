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
  7.91).
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

### Mini IDE and dewmini (`assets/mini-ide.*`, `compose/dewmini.*`)
Two Python workspaces with no tutorial attached — see
`MINI_IDE_REDESIGN.md` for the full plan and `ARCHITECTURE.md` §4 for
how they're built.

- **Mini IDE**: rebuilt on the same Worker-based engine tutorial pages
  use (`assets/pyodide-engine.js`, a client of
  `assets/pyodide-worker.js`), giving it a genuine Stop button and real
  Jedi-backed autocomplete in place of the hardcoded stub it shipped
  with originally. A filesystem layer (`assets/mini-ide-fs.js`) mounts a
  real local folder (File System Access API), OPFS, or IDBFS — whichever
  the browser supports — behind one interface, so the file manager, SQL
  support (`sqlite3` against a mounted `.db` file), and file uploads all
  work the same way regardless of backend. `.ipynb`/`.py` import and a
  folder-based, offline-capable downloadable bundle
  (`write_mini_ide_bundle()` in `build.py`) round it out. A reopenable
  "?" Help panel next to Settings, and Shift+Enter to run a cell, match
  dewmini's own — both replaced a one-shot welcome banner that was gone
  for good the moment a reader had cells. Cells themselves match
  dewmini's look too now (a quiet coloured rail and icon-only actions
  rather than a bordered header full of labelled buttons), reorderable
  by dragging and insertable at any seam between cells — not just
  appended at the end — via the same hover-to-reveal dividers dewmini
  uses. Settings gained dewmini's own "Your notes" free-text box, an
  "Editor" section (code size, spacing, cursor, gutter, active line),
  and a file name field shared by every download and a Print/PDF
  button. Dark mode had its own bug: a local `.dl-btn` override hardcoded
  a fixed-dark navy for both toolbar and Settings buttons (invisible on a
  near-black background), and toolbar icons baked their fill color
  straight into the SVG data URI instead of using `currentColor` — both
  fixed, the icons now using the same `mask`/`background: currentColor`
  technique dewmini's own toolbar icons use. The toolbar was also trimmed
  down: Import and the `.py`/`.html`/`.ipynb` download buttons moved into
  Settings (which already had them), replaced by a "Load example" button
  that loads the same sample cells the notebook used to auto-seed on
  every load of an empty notebook — now a notebook you've cleared stays
  cleared. Settings itself is grouped into three collapsible sections
  (Workspace, Your work, Appearance) instead of one long scroll.
- **dewmini**: a smaller, quieter cousin — the same
  `tutorial_tools.py`, but Pyodide stays on the main thread always (no
  Worker, no Stop button), by design: dewmini is for something quick,
  and a project that outgrows that moves to Mini IDE.

### Documentation and code comments
Every substantial code file has detailed, teaching-oriented inline
comments and a matching `docs/<file>-explained.md` walking through its
structure — `CONTRIBUTING.md` makes keeping both current a standing
requirement for future changes, the same way the build already enforces
that links and folds can't go stale.

### Curriculum modules (`tutorials/`)
- **83 published tutorial and practice pages** — 41 tutorials, 38
  practice pages (one per tutorial, except the three that are already
  problems or reflection), and 4 mixed sets drawing on several tutorials
  at once. See `EXERCISES.md` for where the problems came from.
  - `computational-methods` (8 tutorials, 8 practice pages):
    `first-steps.md`, `working-with-tables.md`, and the `matrices`
    series — `grid-of-numbers.md`, `multiplying-grids.md`,
    `what-a-matrix-does-to-a-picture.md`, `undoing-it.md`,
    `solving-systems.md`, `where-chains-lead.md`.
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
All 67 learning outcomes across *Mathematics for IT (5N18396)* and
*Programming and Design Principles (5N2927)* are written, mapped, and
tested — no gaps in either descriptor.

---

## 2. What's still open

### Computational Methods (5N0554) curriculum
Full curriculum specification, mapping, and authoring for
*Computational Methods and Problem Solving 5N0554* (15 credits, 13
learning outcomes across 7 sections).

As of the run that closed the first strand: all 13 outcomes are
transcribed into `outcomes.yaml` under a new `CMPS` module, with the
descriptor's own "e.g." examples moved to `topics.yaml`'s `uses:` rather
than folded into what coverage is measured against (DECISIONS_LOG.md
7.55). The first target strand is written and released; the other four
are not.

1. **Linear Algebra & Matrix Operations** — **done.** Six tutorials —
   *A Grid of Numbers*, *Multiplying Grids*, *What a Matrix Does to a
   Picture*, *Undoing It*, *Solving Systems*, *Where Chains Lead* —
   under `tutorials/computational-methods/`, series `matrices`, each
   with a practice page. *Where Chains Lead* folds in Markov chains,
   word-level text generation, and a worked small-scale PageRank,
   closing what were planned as strands 1 and 2 (and part of 3) into one
   series — see `outlines/matrices.md`'s resolved open question and
   DECISIONS_LOG.md 7.56. `CMPS-LO4` is fully taught; `CMPS-LO1` and
   `CMPS-LO2` are touched but not taught, since only the
   data-structures half of LO1 and the randomness half of LO2 came up
   along the way.
2. **Markov Chains & Text Generation** — **folded into strand 1**, above,
   rather than written as its own strand.
3. **Link Graph Analysis & PageRank** — **partly done**, as the closing
   section of *Where Chains Lead* — a hand-checkable three-page example
   rather than a dedicated tutorial on crawling or a real link graph,
   which remains unwritten.
4. **Discrete Simulation & Monte Carlo Methods** — **half written.**
   Two of the four tutorials in `planning/outlines/monte-carlo.md` are
   released, as the `simulation` series under
   `tutorials/computational-methods/`: *Leaving It to Chance* (randomness,
   seeds and reproducibility) and *Counting Darts* (Monte Carlo estimation
   of $\pi$, and why more samples is not reliably better). `CMPS-LO3` and
   `CMPS-LO2` are both fully taught and green on the curriculum map.

   Still to write: *How Wrong Are We?* (the $1/\sqrt{n}$ law, and bootstrap
   resampling on `life-expectancy.csv` — the first use of a real dataset
   anywhere in dewlab, which needs `data/life-expectancy.yaml` written
   first) and *The Queue* (discrete-event simulation, and what happens to
   waiting time as utilisation approaches one). `CMPS-LO6` stays red until
   *The Queue* lands, and even then only half of it is reachable without
   the complexity strand — see the outline's own note.
5. **Algorithmic Complexity & Systems Modeling** — **not started.**
   Complexity bounds, cache prediction, thermal simulation —
   `CMPS-LO5`, `CMPS-LO7` through `CMPS-LO13`, all still red on the
   curriculum map.

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
