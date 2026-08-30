# The visual authoring editor

A browser-based tool that lets a course maintainer reorder a series,
insert or create a tutorial, edit its Markdown and code, and publish a
new release — straight to GitHub, as a pull request, with no local
checkout or terminal needed.

---

## 1. The problem this solves

Ordering used to live in each tutorial's own `order:` frontmatter field,
which meant inserting or moving a tutorial meant editing several files
by hand.

The editor separates ordering from content entirely: a series' reading
order lives in its own file (`<series>.order.yaml`), and the editor
gives one interface for both editing content and managing releases.

## 2. Order files

```yaml
# tutorials/mit-pdp-maths-prog-integration/maths-and-programming.order.yaml
series: Maths and programming
order:
  - first-steps
  - storing-and-computing
  - making-decisions
```

- **One place to reorder.** Moving or inserting a tutorial is a
  one-line change to `<series>.order.yaml`, nothing else.
- **Checked at build time.** The build confirms every slug in
  `<series>.order.yaml` actually has a real tutorial behind it, and that no
  tutorial is quietly missing from the file and left off the reading
  path.

## 3. What the editor actually is (`assets/editor.js`, on a page `build.py`'s `write_editor_page()` writes)

A standalone page inside the built site (`editor.html`) that talks
directly to the GitHub REST API — nothing dewlab hosts sits between the
editor and GitHub.

### What it can do
- **Reorder a series** — drag-and-drop, or accessible keyboard controls,
  to reorder the cards in a series. Saving writes the updated
  `<series>.order.yaml` as a commit on a branch.
- **Insert or create a tutorial** — a card can be inserted anywhere in a
  series, or at the end. Giving it a title generates its slug, sets up
  its frontmatter, and creates a starting file with the standard
  sections, cells, and reflection blocks already in place.
- **Edit content and frontmatter** — Markdown prose, YAML frontmatter,
  and executable Python cells, all edited in place with syntax
  highlighting.
- **Preview structural problems** — rather than keeping a second
  renderer around that could quietly drift from what `build.py` does,
  the editor previews structural validity directly: cell counts,
  heading levels, syntax errors, an unclosed code fence, a duplicate
  cell id.

## 4. Authentication

The editor signs in to GitHub with a fine-grained personal access token,
scoped to `contents: write` on `deweydex/dewlab` alone.

- **Where the token lives**: in the browser's own `localStorage`. A
  "Forget token" control is always available, and the editor is never
  linked from anything a student sees.
- **How a change actually ships**: the editor commits to its own feature
  branch and opens a pull request — it never pushes straight to `main`.
  That's what keeps ordinary review and CI in the loop before anything
  reaches a student.

## 5. What's safe, what needs care, and what's blocked

Every operation is grouped by what it could do to a student's saved
progress.

### Safe — fully reversible
- **Reorder a series** — only touches `<series>.order.yaml`, never a tutorial's
  own content.
- **Insert or create a tutorial** — adds new files from the standard
  template.
- **Edit prose or a cell's code** — as long as the cell keeps its id.
- **Edit frontmatter** — `title`, `module`, `year`, `packages`.
- **Change status** — `draft`, `beta`, `live`, `archived`.
- **Release a new version** — freezes the current live content and
  publishes the working buffer as a new, dated release. The editor
  proposes doing this automatically whenever it notices a cell's
  structure or id has changed.

### Needs care — has real structural impact
- **Duplicate a tutorial** — clones it under a new slug and renames its
  cell ids, so the copy's saved progress can never collide with the
  original's.
- **Move a tutorial to a different series** — updates both series'
  order files and the tutorial's own `series:` field.

### Restricted, with a clear warning first
- **Rename a slug** — breaks any external link to the old address, and
  strands saved progress that was keyed to `(module, slug)` under the
  old name. The editor requires archiving the old slug rather than
  quietly renaming it.
- **Rename a cell id** — orphans a student's saved answer for that cell
  in any release that already shipped. The editor compares the working
  copy's cell ids against the original and warns explicitly before a
  commit goes through.
- **Delete a tutorial file outright** — not offered in the UI at all. A
  tutorial is retired by setting its status to `archived` instead.
