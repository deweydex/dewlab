# Tutorial versions

How a tutorial gets more than one release: dated versions, archive
retention, and how saved progress survives a student moving between
them.

---

## 1. What versioning has to do

Tutorials change over academic terms, and the versioning system exists
to satisfy three things at once:

1. **A student's saved work has to survive a revision.** Updating a
   tutorial must never disrupt a session already in progress or
   invalidate answers a student already saved.
2. **A past release has to stay reachable.** A cohort that worked
   through an earlier version can still get back to exactly the page
   they used, at a permanent URL.
3. **A new tutorial or release can be staged before it's live.** An
   author can write and preview a `draft` or `beta` tutorial without it
   replacing the default route students actually land on.

A **version** is a formal, published release — not every commit. A
typo fix or a prose clarification happens in place, no version bump
needed; a structural change (different exercises, a rewritten section)
gets a new, timestamped release instead.

---

## 2. Version identifiers and lifecycle states

### Format
A version is a human-readable release timestamp: `YYYY.MM.DD.N` (e.g.
`2026.09.15.1`) — year, month, day, and which release of that day it
was.

- **Identity and URLs**: used in versioned URLs
  (`<slug>/v2026.09.15.1.html`) and in the page's own manifest.
- **Sorting**: parsed as four separate integers, so `2026.08.20.10`
  correctly sorts after `2026.08.20.9` — sorting the raw string would
  get that wrong.
- **Shown to a reader**: rendered as an ordinary date ("15 September
  2026") anywhere a student picks between releases.

### Status

| Status | Built as a page? | In the reading order? | What it means |
|---|---|---|---|
| `draft` | No | No | Work in progress — visible only in a local build or the authoring editor. |
| `beta` | Yes | No | Reachable by direct URL, for testing or preview — never the default route. |
| `live` | Yes | Yes | The active, canonical release — the one a plain URL serves. |
| `archived` | Yes | No | Retired — still built, at its old URL, so past students' saved work still has somewhere to land — but out of the reading order. |

---

## 3. Where the files live

A tutorial is either a single Markdown file (while it only has one
release) or a folder (once a second release is published):

```
tutorials/mit-pdp-maths-prog-integration/
  first-steps.md                  # single-version tutorial (the normal case)
  cracking-equations/             # a tutorial with more than one release
    cracking-equations.md         # the current, working release
    v2026.06.02.1.md              # a frozen past release
    v2026.09.15.1.md              # a frozen past release
```

- **The plain URL** (`tutorials/<module>/<slug>.html`) always serves the
  newest `live` release.
- **Past releases** build to `tutorials/<module>/<slug>/v<version>.html`.
- **Search engines** are pointed at the canonical page: every archived
  release carries `<link rel="canonical" href=".../<slug>.html">` back
  to the current one.
- **Downloadable copies**: only the current `live` release gets a
  standalone offline HTML file or a place in a series' zip — an offline
  copy of a superseded release isn't worth the size.

---

## 4. How saved work survives a version change

### Matching a student's answers back up
A student's cells are saved by `task_id`, never by version string. When
a tutorial page loads:

1. Saved progress is read from `localStorage`, under the scoped key
   `dewlab:progress:<module>:<slug>`.
2. Each saved cell is matched against the cells actually on the current
   page, by id.
3. An answer whose cell id isn't on this release just stays saved —
   nothing is lost — and reappears the moment the student is on a
   release that has that cell again.

### What the version picker tells a student
Switching versions through the UI compares the cell-id sets of both
releases and gives an honest, exact count, not a vague warning:

> **15 September 2026** — 6 of your 8 answers carry over. 2 cells
> aren't in that version (they're still saved, and come back if you
> return to a version that has them).

### Which release a student actually lands on
- **A first-time visitor** gets the newest `live` release, at the plain
  URL.
- **A returning student** is kept on the release they were already
  working in — the runtime remembers, and doesn't move them without
  asking.
- **Settings** lets a reader choose which of those two behaviours they
  want going forward: stay on the version they left off in, or always
  jump to the newest.

---

## 5. How a release actually happens (`assets/editor.js`)

1. The editor keeps two copies in memory: `state.original` (what was
   fetched) and the working buffer (what's being edited).
2. Releasing freezes `state.original` as a new file named for its own
   old version (`v<previous-version>.md`), and publishes the working
   buffer under today's date as the new current version.
3. Before that, the editor compares cell ids between the working buffer
   and the original, and prompts the author to release a new version if
   any were added, removed, or renamed — the signal that this edit is
   structural, not just a wording fix.

---

## 6. Linking to a topic, not just a tutorial

Beyond a plain `tutorial:<slug>#<anchor>` link, a tutorial can link to a
learning outcome directly:

```markdown
As introduced in [Linear Functions](topic:MIT-3.2) ...
```

- `build.py` resolves `MIT-X.Y` to whichever tutorial currently teaches
  that outcome (`taught_where()`).
- If an outcome is removed or archived with nothing left to take its
  place, the build fails rather than shipping a link that points at
  nothing.
