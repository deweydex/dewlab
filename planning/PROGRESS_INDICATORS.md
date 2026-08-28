# Showing progress: the contents page, and inside a tutorial

Design note, not yet built. Two related but separate features, both derived
from data that already exists: how far a reader has gotten in each
tutorial, shown on the page that lists them all, and a simple readout of
where they are in the tutorial they have open.

---

## 1. What already exists to build this on

Nothing new to save. `tutorial-runtime.js`'s `saveNow()` already writes one
record per tutorial to `localStorage`, keyed `dl-progress:<module>:<slug>`,
on every autosave — `cells: [{task_id, student_code, output_html}, ...]`,
one entry per cell that has ever been run or edited. All of it is already
purely local; nothing here adds a fetch, a server, or a new storage
mechanism.

**What "done" and "errored" mean is already visible in that data, just not
extracted.** Every error a cell produces — a raised exception, a failed
assertion — is rendered through `tutorial_tools.py`'s stderr stream or its
`show_error()`, and both write `class="dl-error"` (`assets/tutorial_tools.py`
lines 531/546/867). So `output_html` already says, textually, whether a
cell's last run failed. Rather than re-deriving that by string-searching
saved HTML wherever it is needed, `saveNow()` should capture it once, as a
plain boolean, alongside what it already saves:

```js
cells: cells.map((cell) => ({
  task_id: cell.id,
  student_code: cell.getCode(),
  output_html: cell.outputEl.innerHTML,
  errored: !!cell.outputEl.querySelector(".dl-error"),   // new
})),
```

That gives every consumer — the index page, an in-page summary, anything
later — one clean question to ask instead of parsing HTML: for this cell,
is there a saved record, and if so, is `errored` true?

Three states per cell follow directly: **not started** (no record, or an
empty `output_html`), **done** (a record, `errored: false`), **errored** (a
record, `errored: true`). Confirmed as the recommended reading: grey for
not started, green for done, red reserved specifically for errored — not
for "not started yet," which is not a failure and should not look like one.

## 2. The contents page: a completion indicator per tutorial

The page every reader returns to, to pick up where they left off
(`write_index()`/`render_index()`, the site root). Each tutorial is one
`<li><a href="...">Title</a></li>`; a reader currently has no way to tell,
from that list, which ones they have already started or finished without
opening each in turn.

**Build time:** `render_index()` already has `len(member.cells)` for free —
add it to the link as a data attribute, no new computation:

```html
<li><a href="first-steps.html" data-module="computational-methods"
       data-slug="first-steps" data-cells="6">First Steps</a></li>
```

**Client side:** a small script on the index page reads
`dl-progress:<module>:<slug>` for every link with a `data-cells` attribute,
counts done/errored/not-started among the cells that have a record,
compares against `data-cells`, and renders a compact indicator next to the
title — clean and minimal means small: a short "4/9" fraction is enough on
its own; a tiny inline segmented bar (one thin block per cell, colored per
§1's three states) is a nice-to-have beside it, not a requirement. No fetch,
no per-tutorial page visited — everything needed is already in
`localStorage` and the page's own markup.

**A tutorial with no saved record at all** shows nothing extra — the
existing bare title — rather than a "0/9" that reads as a judgment on a
page nobody has opened yet.

**Toggle:** a Settings switch, off means the contents page reverts to plain
titles with no indicator at all. This is the one piece of this design that
needs an opt-out, because it is the only part that is *ambient* — visible
every time the contents page loads, whether or not a reader wants a
visible tally of what they have and have not finished. (§3's in-tutorial
summary does not need a second toggle of its own — see §3.)

## 3. Inside a tutorial: no dedicated bar

The original framing floated a persistent bar (bottom of the screen, or the
right edge, filling as you progress) — reconsidered in favour of something
smaller: **fold a plain summary into the Settings panel**, the surface that
already exists for exactly this kind of "how is this page configured /
how am I doing" information, rather than adding new fixed-position chrome
competing with the cheat sheet's own toggle for a screen edge.

A new section in `#dl-settings`, alongside its existing sections:

```
Progress
4 of 9 cells run · 1 with an error
```

Recomputed the same way `saveNow()`/`readSaved()` already work — read this
page's own `dl-progress:` record, count by state, update the text after
every save (the same moment the "Saved a moment ago" note already updates,
so this is not new plumbing, just one more thing that redraws at a point
the runtime already redraws something).

**No second toggle needed for this one.** Unlike the contents page's
indicator, this line is only ever seen by a reader who has already opened
Settings — it is opt-in by where it lives, the same way every other
Settings section already is. Adding a toggle to hide something inside a
panel a reader chose to open would be a toggle nobody needs.

## 4. What this does not do

- No per-cell colored markers next to the cells themselves on the page —
  that would be a third, more intrusive treatment layered on top of what a
  reader already sees when a cell has (or has not) been run; out of scope
  unless §2/§3 turn out not to be enough on their own.
- No cross-device or account-linked progress — this is exactly as local as
  the saved work itself already is (`localStorage`, this browser, this
  device), and showing a percentage anywhere does not change that.
- No change to what "saved" means or how autosave works — this reads the
  existing record; it does not write anything new to it beyond the one
  `errored` boolean in §1.

## 5. Rollout sketch

Roughly: `errored` capture in `saveNow()`, read-side helpers for the three
states (`tutorial-runtime.js`) → the contents-page indicator (build-time
`data-cells` attribute, client-side render, Settings toggle) → the
in-tutorial Settings section → tests (a unit test on the build-time
attribute, e2e tests seeding `localStorage` directly the way
`tests/e2e/test_cheat_sheet.py` seeds fixture content, to check all three
states render distinctly) → docs. Each a PR of its own, same reasoning
`CHEAT_SHEETS.md` §7 and `SIDEBAR_CONTENT.md` §6 gave for staging those
features the same way.
