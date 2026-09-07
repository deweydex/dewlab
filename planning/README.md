# Planning and architecture

Design documents, decision records, and curriculum planning for dewlab —
mostly written before or during building something, kept afterward as
the record of why it works the way it does.

## Document index

### Writing tutorials
- **[`PEDAGOGICAL_STYLE_GUIDE.md`](./PEDAGOGICAL_STYLE_GUIDE.md)** — the
  teaching philosophy ("discover first, name afterwards"), what a good
  tutorial looks like, code-and-maths examples, and the author checklist.
- **[`EXERCISES.md`](./EXERCISES.md)** — how practice pages and
  fold-hidden answers work, and where worksheet conversion draws from
  ([`deweydex/Mathematics`](https://github.com/deweydex/Mathematics)).
- **[`PRACTICE.md`](./PRACTICE.md)** — cells a reader adds themselves,
  anywhere on a page, kept separate from the tutorial's own saved work.
  Built; this is the design behind it.

### Architecture
- **[`STATUS.md`](./STATUS.md)** — what's built, what's still open, and
  the trickier decisions behind the parts that are done.
- **[`ROADMAP.md`](./ROADMAP.md)** — what comes next, in phases, with
  the questions each phase leaves open and what will be assumed if
  nobody answers them.
- **[`DECISIONS.md`](./DECISIONS.md)** — the early choices (libraries,
  visual style, hosting, versioning, editor, maths) and why.
- **[`BUILD_PLAN.md`](./BUILD_PLAN.md)** — the staged plan this was
  actually built in, runtime first through curriculum last.
- **[`CONTENT_AND_FILE_ARCHITECTURE.md`](./CONTENT_AND_FILE_ARCHITECTURE.md)**
  — the tutorial Markdown format: executable code blocks, setup
  includes, dataset references.
- **[`VERSIONING_AND_PROGRESS.md`](./VERSIONING_AND_PROGRESS.md)** — how
  saved work is stored in the browser and restored across versions.
- **[`VERSIONS.md`](./VERSIONS.md)** — how a tutorial gets more than one
  release: dated versions, canonical URLs, frozen archives.
- **[`WINDOW_AUDIT.md`](./WINDOW_AUDIT.md)** — a pre-release check of
  every contract this project can't change its mind about later (URL
  slugs, cell ids, the saved-work schema, version format).
- **[`REPO_AND_EDITOR.md`](./REPO_AND_EDITOR.md)** — how the repository
  is laid out, how GitHub Actions deploys it, and the authoring editor's
  design.
- **[`EDITOR.md`](./EDITOR.md)** — the GitHub-integrated visual editor:
  what it does and how releases work through it.
- **[`MINI_IDE_AND_DEWMINI_NEXT.md`](./MINI_IDE_AND_DEWMINI_NEXT.md)** —
  a historical record from when dewlab had two Python workspaces: what
  was worth building on each, why merging them into one tool wasn't the
  answer, and (in its addenda) the decision that resolved the question
  the other way — dewmini absorbed everything and is the one workspace
  now.
- **[`MINI_IDE_REDESIGN.md`](./MINI_IDE_REDESIGN.md)** — the phased plan
  the earlier, since-absorbed workspace was rebuilt to: Worker engine,
  file manager, SQLite, notebook import, offline bundle. All phases
  shipped; the capabilities live on in dewmini.

### The reading surface
Each of these designs one part of what a reader sees, and each was
written before the thing it describes was built.

- **[`REFERENCE_PANEL.md`](./REFERENCE_PANEL.md)** — the per-tutorial
  reference, assembled from glossary files, and the rule it exists to
  keep: never show a reader a term they have not met.
- **[`SIDEBAR_CONTENT.md`](./SIDEBAR_CONTENT.md)** — datasets,
  author-written pedagogical notes, and what earns a panel of its own.
- **[`STUDENT_NOTES.md`](./STUDENT_NOTES.md)** — a reader's own free-text
  notes, and encouraging a copy that outlives the browser. Not the same
  "notes" as the pedagogical ones above; §0 says why.
- **[`PROGRESS_INDICATORS.md`](./PROGRESS_INDICATORS.md)** — completion
  badges on the contents page and a summary in Settings, both read from
  saved work that was already there.
- **[`CELL_CONTROLS.md`](./CELL_CONTROLS.md)** — where a cell's controls
  sit, and the Worker migration that made a real Stop button possible.
- **[`CELL_TOOLTIPS.md`](./CELL_TOOLTIPS.md)** — hover docs and signature
  help, including what Jedi in Pyodide costs and covers.
- **[`CELL_HINTS.md`](./CELL_HINTS.md)** — hints that appear after a
  cell has errored or run some number of times: what the page can
  already observe, the fold-and-attribute authoring surface, the
  questions Josh answered and how. Built (DECISIONS_LOG.md 7.135); its
  dewstack half lives beside it in that repository.
- **[`CELL_IDENTITY.md`](./CELL_IDENTITY.md)** — the settled design for
  execution counters and cell identity (the pill, the run line, what
  differs by cell type), not yet built. A working mockup of every cell
  type sits at [`mockups/cell-identity.html`](./mockups/cell-identity.html),
  and a plain-language explanation of the reasoning, written for a reader
  new to the project, at
  [`mockups/cell-identity-explained.html`](./mockups/cell-identity-explained.html).

### The edges
- **[`EDGES_AUDIT.md`](./EDGES_AUDIT.md)** — the phone, screen-reader and
  offline-bundle audit: what was claimed, what testing it found, and what
  still needs a person rather than a script.

### The documentation itself
- **[`DOCS_AND_COMMENTS_PASS.md`](./DOCS_AND_COMMENTS_PASS.md)** — the
  repo-wide pass that gave every substantial code file teaching-oriented
  comments and a matching `docs/<file>-explained.md`.

### Curriculum
- **[`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md)** — generated; every
  learning outcome, mapped to where (or whether) it's actually taught.
  Don't edit by hand — run `python3 dev/curriculum_map.py`.
- **[`CURRICULUM_NOTES.md`](./CURRICULUM_NOTES.md)** — notes on how the
  curriculum is structured and named.
- **[`WHAT_IS_LEFT_TO_WRITE.md`](./WHAT_IS_LEFT_TO_WRITE.md)** — retired:
  its own backlog is written. Points at `STATUS.md` and
  `CURRICULUM_MAP.md` for the current 5N0554 gap instead of duplicating
  it.
- **[`OPEN_QUESTIONS.md`](./OPEN_QUESTIONS.md)** — early architectural
  questions, the tradeoffs weighed, and how each was resolved.
- **[`curriculum/`](./curriculum/)** — the machine-readable outcome
  descriptors, scope limits, and topic dependency graph.
- **[`curriculum/review/contradictions.md`](./curriculum/review/contradictions.md)**
  — the pairs where a decision still disagrees with Josh's own game answer,
  and why the graph kept the decision.
- **[`curriculum/review/pair-results.md`](./curriculum/review/pair-results.md)**
  — generated; what the pair game's judgements say about the dependency
  graph. Run `python3 dev/pair_results.py` after new batches land in
  `curriculum/review/pairs/`.
- **[`outlines/`](./outlines/)** — an outline for each curriculum
  module.

## The principles behind it

1. **Computing and maths teach each other.** Code is a lab for building
   mathematical intuition; maths gives the code something real to model.
2. **Real Python, running locally, with nothing tracked.** Pyodide runs
   in the student's own browser tab — no server executes their code, no
   data leaves their machine.
3. **Scope is written down, not assumed.** What's covered and what's
   deliberately left out both live in machine-readable files
   (`outcomes.yaml`, `out-of-scope.yaml`, `proposed.yaml`), checked by
   CI so they can't quietly drift from the tutorials.
4. **A real decision gets a reason and a cost.** A choice that could
   reasonably have gone another way is written down in
   `DECISIONS_LOG.md`, with what it would cost to change later.
