# The visual authoring editor

A browser-based tool (`editor.html`, `assets/editor.js`) that lets a
course maintainer reorder a series, insert or create a tutorial, edit
its Markdown and code, and publish a new release — straight to GitHub,
as a pull request, with no local checkout or terminal.

## Order files

A series' reading order lives in its own file, separate from any
tutorial's content:

```yaml
# tutorials/mit-pdp-maths-prog-integration/programming-foundations.order.yaml
series: Programming Foundations
order:
  - first-steps
  - storing-and-computing
  - making-decisions
```

Moving or inserting a tutorial is a one-line change here. The build
confirms every slug in an order file has a real tutorial behind it, and
that no tutorial is missing from it.

## What the editor does

Talks directly to the GitHub REST API — nothing dewlab hosts sits
between it and GitHub.

- **Reorder a series** — drag-and-drop or keyboard controls; saving
  writes the updated order file as a commit on a branch.
- **Insert or create a tutorial** — a title generates its slug, sets up
  frontmatter, and creates a starting file with standard sections,
  cells, and reflection blocks in place.
- **Edit content and frontmatter** — Markdown, YAML, and Python cells,
  with syntax highlighting.
- **Preview structural problems** directly — cell counts, heading
  levels, an unclosed fence, a duplicate cell id — rather than running a
  second renderer that could drift from what `build.py` does.

## Authentication

A fine-grained personal access token, scoped to `contents: write` on
`deweydex/dewlab` alone, held in the browser's own `localStorage` with
a "Forget token" control always available. The editor is never linked
from anything a student sees, and it commits to its own feature branch
and opens a pull request — never straight to `main`.

## What's safe, what needs care, what's blocked

### Safe — fully reversible
- Reorder a series.
- Insert or create a tutorial.
- Edit prose or a cell's code, keeping its id.
- Edit frontmatter (`title`, `module`, `year`, `packages`).
- Change status (`draft`, `beta`, `live`, `archived`).
- Release a new version — freezes the current live content and
  publishes the working buffer as a new, dated release. The editor
  proposes this automatically when it notices a cell's structure or id
  has changed.

### Needs care — real structural impact
- Duplicate a tutorial — clones it under a new slug and renames its
  cell ids, so the copy's saved progress can never collide with the
  original's.
- Move a tutorial to a different series — updates both series' order
  files and the tutorial's own `series:` field.

### Restricted, with a warning first
- Rename a slug — breaks any external link, and strands saved progress
  keyed to the old `(module, slug)`. The editor requires archiving the
  old slug rather than quietly renaming it.
- Rename a cell id — orphans a student's saved answer in any release
  that already shipped. The editor warns explicitly before committing.
- Delete a tutorial file — not offered. A tutorial is retired by
  setting its status to `archived`.
