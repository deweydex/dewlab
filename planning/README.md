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
  what's still worth building on each of dewlab's two Python workspaces,
  and why merging them into one tool isn't the answer.

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
