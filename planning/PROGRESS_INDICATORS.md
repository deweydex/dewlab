# Showing progress: the contents page, and inside a tutorial

Built as designed — `DECISIONS_LOG.md` 7.70. Two related but separate
features, both derived from data that already exists: how far a reader
has gotten in each tutorial, shown on the page that lists them all, and a
simple readout of where they are in the tutorial they have open.

---

## 1. What this is built on

Nothing new is saved to make this work. `tutorial-runtime.js`'s
`saveNow()` writes one record per tutorial to `localStorage`, keyed
`dl-progress:<module>:<slug>`, on every autosave — `cells:
[{task_id, student_code, output_html}, ...]`, one entry per cell that has
ever been run or edited. It's purely local; nothing here adds a fetch, a
server, or a new storage mechanism.

Every error a cell produces — a raised exception, a failed assertion — is
rendered through `tutorial_tools.py`'s stderr stream or its
`show_error()`, both of which write `class="dl-error"`
(`assets/tutorial_tools.py` lines 531/546/867). `saveNow()` captures that
once, as a plain boolean, alongside what it already saves:

```js
cells: cells.map((cell) => ({
  task_id: cell.id,
  student_code: cell.getCode(),
  output_html: cell.outputEl.innerHTML,
  errored: !!cell.outputEl.querySelector(".dl-error"),
})),
```

Three states per cell follow: **not started** (no record, or an empty
`output_html`), **done** (a record, `errored: false`), **errored** (a
record, `errored: true`) — grey, green, and red respectively, red
reserved specifically for errored rather than for "not started yet."

## 2. The contents page: a completion indicator per tutorial

Each tutorial in the site index is one `<li><a href="...">Title</a></li>`.
At build time, `render_index()` adds the cell count as a data attribute:

```html
<li><a href="first-steps.html" data-module="computational-methods"
       data-slug="first-steps" data-cells="6">First Steps</a></li>
```

A client-side script reads `dl-progress:<module>:<slug>` for every link
with a `data-cells` attribute, counts done/errored/not-started among the
cells that have a record, and renders a compact indicator next to the
title: a short "4/9" fraction, with a tiny inline segmented bar (one thin
block per cell, coloured per §1's three states) beside it. No fetch, no
per-tutorial page visited.

A tutorial with no saved record at all shows the plain title, not a "0/9"
that would read as a judgment on a page nobody has opened yet.

A Settings switch turns the indicator off entirely, back to plain titles
— the one opt-out this feature needs, since it's the only part that's
*ambient* (visible on every load, whether or not a reader wants a visible
tally). §3's in-tutorial summary doesn't need a second toggle: see §3.

## 3. Inside a tutorial: a line in Settings, not a bar

The summary lives as a new section in `#dl-settings`, alongside its
existing sections, rather than as fixed-position chrome on the page:

```
Progress
4 of 9 cells run · 1 with an error
```

It's recomputed the way `saveNow()`/`readSaved()` already work — reading
this page's own `dl-progress:` record, counting by state, and updating
after every save, the same moment the "Saved a moment ago" note already
updates.

No second toggle: this line is seen only by a reader who has already
opened Settings, so it's opt-in by where it lives, same as every other
Settings section.

## 4. What this does not do

- No per-cell coloured markers next to the cells themselves on the page —
  a third, more intrusive treatment on top of what a reader already sees
  when a cell has (or hasn't) been run.
- No cross-device or account-linked progress — exactly as local as the
  saved work itself (`localStorage`, this browser, this device).
- No change to what "saved" means or how autosave works — this reads the
  existing record, adding only the one `errored` boolean from §1.
