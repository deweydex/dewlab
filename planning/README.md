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

### The reading surface
- **[`REFERENCE_PANEL.md`](./REFERENCE_PANEL.md)** — the per-tutorial
  reference, assembled from glossary files, and the rule it exists to
  keep: never show a reader a term they have not met.
- **[`DOT_DOCK.md`](./DOT_DOCK.md)** — exploring the masthead's orange dot
  as a replacement for the Panels disclosure, up to six panels fanning
  into three zones. Design note; nothing here is built.

### Curriculum
- **[`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md)** — generated; every
  learning outcome, mapped to where (or whether) it's actually taught.
  Don't edit by hand — run `python3 dev/curriculum_map.py`.
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
