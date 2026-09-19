# Status

What's actually built and what's still open. Kept current as things
change — not a pitch, not a history.

---

## 1. What's built

### Core runtime
- Real Python in the browser via Pyodide — `numpy`, `pandas`,
  `matplotlib` by default, more on request via a tutorial's `packages:`
  frontmatter.
- The tools bridge: `show`, `show_table`, `check`, `text_input`,
  `dropdown`, `button`, `load_csv`, `load_text`, `run_query` — all in
  `assets/tutorial_tools.py`.
- Trimmed tracebacks: an error a student causes is trimmed to their own
  line.
- Saved work, keyed to `(module, slug)`, restored across releases by
  matching cell id.

### The build
- Frontmatter and cell parsing: `python exec` fences, `hint:`,
  `{{include: ...}}`.
- Maths pulled out before Markdown sees it.
- Link validation: a `tutorial:slug#anchor` that doesn't resolve fails
  the build.
- Multiple dated releases, each frozen and reachable at its own URL.
- Downloadable copies: a standalone HTML file per tutorial, a zip per
  series.

### UI and navigation
- The reading surface, contents and navigation, the topic tree,
  browse-by-topic.
- The authoring editor: reorders series, edits frontmatter and content,
  warns before a cell-id change strands saved work, opens a pull
  request.
- Progress indicators, student notes, cell tooltips (live introspection
  falling back to Jedi's static analysis), a real Stop button on the
  hosted site (Worker-based; the offline export has none, on purpose).
- Highlight to look up a term; an inherited reference entry says which
  tutorial introduced it.
- Highlights and margin notes: a reader marks a passage of prose,
  durably, with an optional note — anchored by quote-and-position,
  computed at read time, surviving a version release the same way a
  cell's saved answer does.
- A reader's own cells, separate from the tutorial's saved work and
  version system.
- Print/PDF and a Jupyter notebook export.

### dewmini
The one Python workspace with no tutorial attached, its own downloadable
offline copy. A workbench: notebooks open in tabs, a Library rail (the
cross-tutorial reference, a dataset catalogue) and a Workbench rail (a
live variable inspector, notes, files), both closed until asked for.
Runs through the same Worker-based engine as tutorial pages, so it gets
the same real Stop button and Jedi-backed autocomplete.

### Curriculum
113 published tutorial and practice pages across `computational-methods`,
`fundamentals-of-oop`, and `mit-pdp-maths-prog-integration` — the exact
list lives in `CURRICULUM_MAP.md`, generated from the tutorials
themselves; this file doesn't repeat it. `database-methods` and
`web-authoring` are ported from `deweydex/dewstack` and built;
`full-stack` is built with its one reference tutorial. `database-methods`
is live; `web-authoring` and `full-stack` wait on running in front of a
class before going on the homepage, not on engineering.

115 of 116 learning outcomes across all six accredited modules are
written, mapped, and tested. One gap remains, `WA-LO12`, with no
proposal yet.

---

## 2. What's still open

- **Three `*-explained.md` files are missing**: `editor.js`, `tree.js`,
  `search.js` have none, though `CONTRIBUTING.md` promises one per
  substantial code file.
- **The worksheet-to-practice converter is unwritten**, on hold, and
  possibly not needed — the worksheets whose material is taught are
  already converted by hand; the rest cover material no tutorial teaches
  yet.
- **The link-graph strand's crawl is a toy.** *Where Chains Lead*'s
  three-page PageRank example was deliberately not grown into a real
  crawl — set aside as too advanced for where the curriculum sits now.
- **Retrieval prompts** (the reference surfacing terms met some
  tutorials ago) aren't designed yet. Judge after the reference's other
  work has settled whether it's the right home.

---

## 3. Constraints that shape everything above

**Saved work has to survive a live cohort.** Storage keys are scoped
exactly to `dewlab:progress:<module>:<slug>`, cell ids are immutable
once published, and the authoring editor warns before a change that
would rename one.

**Two students, two versions, no interference.** The plain unversioned
URL always serves the newest release; a returning student is kept on
the release they were already working in, with an honest count of how
many answers carry over.

**Sharing code has to be safe on a shared machine.** Pyodide runs
entirely inside the browser tab's WebAssembly sandbox — no filesystem
or OS access — so code a student didn't write can't touch the machine
it runs on.
