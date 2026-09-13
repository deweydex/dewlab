# Highlights and margin notes

A reader marks a passage of prose and, optionally, writes a short note
against it. Both persist the way a cell's code already does: local to the
browser, in the same saved-progress record, exported the same way.

Replaces `ROADMAP.md` Phases 3 and 4 (practice regeneration, portfolio
export) — abandoned unbuilt in favour of this, `DECISIONS_LOG.md` 7.155.

---

## 1. Two things that already exist, and why this is neither

- **Highlight to look up** (`REFERENCE_PANEL.md` §6b) — selecting a word
  the glossary knows offers a button that opens the reference filtered to
  it. Nothing is stored; the selection is gone the moment the panel opens.
  Stays exactly as it is; this feature adds two buttons beside it, not a
  replacement for it.
- **Student notes** (`STUDENT_NOTES.md`) — one free-text box per tutorial,
  in Settings, for anything a reader wants to write down. Stays too. It
  answers "what do I think about this tutorial"; a highlight's note
  answers "why did this one sentence matter" — different questions, and
  merging them would trade a working, shipped field for a bigger schema
  change with no clear gain. §10 below says more.

What is actually new: **marking a specific passage, durably, with an
optional note tied to that passage rather than to the page.**

## 2. The obstacle this project already named and set aside

`ROADMAP.md` Phase 5 raised persistent highlighting and put it out of
scope: "highlights need anchors that survive a version release; cell ids
give that to code but prose has none, and an anchoring scheme (paragraph
fingerprinting or similar) is real work." That is still true, and it is
the one piece of this whole feature that is a genuine design problem
rather than a wiring exercise. §3 answers it.

## 3. Anchoring: quote-and-position, not a new build-time id

Two shapes were on the table:

- **Paragraph ids from `build.py`**, the same way a cell gets a `task_id`
  from its fence. Rejected: it makes prose a schema `WINDOW_AUDIT.md`
  would need to freeze, the same weight that made Phase 3's "where does
  the seed live" question expensive. A highlight is not that important —
  losing one gracefully costs a reader a sentence, not a session's work.
- **Quote-and-position, computed at read time, no build step involved.**
  Recommended, and what follows describes it.

When a highlight is made, record three things about the live DOM, not
about the source Markdown:

1. **`block_index`** — this passage's ordinal position among `#dl-body`'s
   direct prose blocks (`p`, `li`, `td`, `blockquote`, …), counted the same
   way on every load since it is just walking rendered HTML in reading
   order. No id, no build.py change.
2. **`quote`** — the selected text itself, verbatim.
3. **`prefix`/`suffix`** — a short slice (~24 characters) of the text
   immediately before and after the selection, for the rare case where
   `quote` appears more than once in the same block.

Restoring a highlight: look at `block_index` first. If that block still
contains `quote` (checked against `prefix`/`suffix` when `quote` is not
unique in it), reattach there — silent, the common case, unchanged
prose. If it doesn't — the tutorial was edited — search a small window of
nearby blocks (say ±5) for the same `quote`/`prefix`/`suffix` before
giving up, since most edits move a passage a little rather than rewrite
it. If nothing matches, drop the highlight and say so in the restore
summary, exactly the sentence `VERSIONING_AND_PROGRESS.md` already writes
for a cell whose `task_id` disappeared: a reader who marked something
deserves to be told it's gone, not to silently lose it.

This is the same "a notice, never a block" posture the version-mismatch
design already commits to. Nothing here is guaranteed permanent; every
part of it degrades to "tell the reader plainly" rather than "guess" or
"corrupt."

*Cost to change: the anchoring algorithm is the one piece of this
feature worth prototyping and testing in isolation before any UI is
built on it — see the rollout sketch, §11.*

## 4. What gets saved

The existing per-tutorial record (`dl-progress:<module>:<slug>`) gains one
more array, alongside `cells`, `notes`, and `siteEditors`:

```json
{
  "highlights": [
    {
      "id": "h-3f2a",
      "block_index": 7,
      "quote": "the pivot only works because the matrix is square",
      "prefix": "…and this is where ",
      "suffix": " — try it on a 2×3 one",
      "note": "this is the bit I kept forgetting",
      "created_at": "2026-09-13T10:02:00.000Z"
    }
  ]
}
```

`note` is an empty string for a highlight with no note attached — a plain
highlight and a highlight-with-a-note are the same record shape, not two
features. `id` is a short client-generated token (a highlight has no
natural key the way a cell's `task_id` does), used for editing and
deletion without re-matching text.

No new save path: `saveNow()`/`readSaved()`/`restoreSaved()` learn one
more field, exactly the shape `notes` was added in (`STUDENT_NOTES.md`
§3). The existing export button, the mismatch check, and the version
banner all keep working unchanged, since none of them read fields by name
beyond what they already check.

## 5. Making a highlight: extending the selection toolbar that already exists

`initReferenceLookup()` already listens for `selectionchange` inside
`#dl-body`, excludes `.dl-editor`/`.dl-output` (a cell's own code and
output are not "prose" for this purpose either), and positions one button
against the selection's bounding rectangle. That becomes a small toolbar
of up to three buttons instead of one:

- **Look up "term"** — unchanged, shown only when the selection matches a
  glossary term, exactly as today.
- **Highlight** — shown for any non-trivial selection inside prose
  (reusing the existing length/viewport checks, dropping the
  glossary-match gate that only applies to Look up).
- **Add a note** — same gate as Highlight. Creates the highlight and opens
  the note editor (§7) in one action, rather than making a reader
  highlight first and separately hunt for how to attach a note.

Clicking Highlight wraps the current `Range` in `<mark class="dl-highlight">`
and calls `saveNow()`'s scheduler, the same autosave path a keystroke in a
cell already uses.

## 6. Wrapping a selection that isn't one text node

A selection rarely sits inside a single text node — it can span a `<code>`
span, an emphasis run, or a sentence break. `Range.surroundContents()`
throws in exactly that case (a partially-selected element it can't safely
wrap). The standard workaround: walk the range's text nodes individually
and wrap each one's selected portion in its own `<mark>`, rather than one
`<mark>` around the whole range. Several `<mark>` elements sharing one
highlight id is normal, not a bug — `.dl-highlight[data-highlight-id="h-3f2a"]`
selects all of them for styling, editing, and removal alike.

## 7. Editing or removing a highlight

Clicking anywhere on a `<mark class="dl-highlight">` opens a small
popover, anchored the same way the Look up button already anchors itself
to a rectangle: the note text in a small textarea (empty if there isn't
one) plus **Save**, and a separate **Remove highlight** control. Removing
strips the `<mark>` wrapper (restoring the plain text node — never
deletes the prose itself) and drops the record from the saved array.

Keyboard reachability matters here the way it already does for the
reference panel's own Escape handling: the popover is a real focusable
element, not a hover-only tooltip, since a highlight a reader wants to
edit or remove has to be reachable without a mouse.

## 8. Where highlights are reviewed: a new list in Settings, "Your work"

The existing "Your work" section (`#dl-settings-work`) already holds the
free-text notes field and the export/import controls
(`STUDENT_NOTES.md` §2). A new subsection, **Highlights**, sits between
them: one row per highlight — the quoted text (truncated), the note
underneath it if there is one, a **Jump to it** link that scrolls the
tutorial to the block and briefly flashes the `<mark>`, and a delete
control mirroring §7's popover.

Empty state: no rows, section hidden — the same reasoning
`initProgressSection()` already applies to the whole "Your work" section
on a page with nothing to save (§2 of `STUDENT_NOTES.md` describes the
existing guard this joins).

## 9. Visual design

- **One highlight colour in v1**, not a palette of categories. Matches the
  plain-textarea choice `STUDENT_NOTES.md` §6 made for the free-text
  field: ship the plain version, let real use argue for more later rather
  than guessing at a taxonomy nobody asked for.
- **Contrast in both themes.** `tutorial-style.css` already carries the
  reader's theme as CSS custom properties; the highlight background is
  defined from those tokens (a translucent tint of the accent colour, most
  likely), not a hardcoded yellow, and is checked against body text the
  same way `test_link_contrast.py` already checks links — this feature
  should extend that test rather than skip it.
- **Narrow screens.** The toolbar and the edit popover both need testing
  at the 375px width fixed for cell headers in PR #203 — the exact bug
  class (a header that doesn't wrap and overflows the viewport) is equally
  possible here, and should be caught before shipping rather than found
  from a screenshot afterward.

## 10. Relationship to the free-text notes field — kept, not merged

Both stay, doing different jobs: the free-text field is one running
thought about the whole tutorial; a highlight's note is anchored to the
one sentence it's about. A reader who wants both keeps using the field
for "what I think" and highlights for "what mattered, and where." Folding
them into one mechanism (say, making the free-text field a special
"whole-page" highlight) was considered and set aside — it would touch a
shipped, working field for a conceptual tidiness that no reader asked
for, exactly the kind of unforced schema change this project avoids
elsewhere.

## 11. What this reopens, cheaply, for later — without building it now

Phase 4's abandoned portfolio-export design worried about reflections
having "nowhere to write" a specific answer, beyond one page-wide notes
field. A highlight-with-a-note is exactly that anchor, built for a
different reason. If a portfolio export is ever revisited, it would have
real per-passage material to assemble instead of one undifferentiated
paragraph — worth noting in `DECISIONS_LOG.md` when it ships, not worth
designing now against a feature that isn't being built.

## 12. What this does not do

- No highlight categories or colours beyond one, in v1 (§9).
- No rich text in a highlight's note — a plain `<textarea>`, same as the
  free-text field.
- No sharing, no comments, no multi-reader visibility — this is one
  reader's own local marks, same privacy stance as everything else saved
  in `localStorage`.
- No cross-device sync beyond the existing manual export/import.
- Not a replacement for `STUDENT_NOTES.md`'s field, and not the portfolio
  export — §10 and §11.

## 13. Tests

- **Unit**: the record round-trips `highlights` through export/import
  the way `STUDENT_NOTES.md`'s rollout sketch tested `notes`; the
  restore-time matching algorithm (§3) gets its own test for the three
  outcomes — same block, moved-but-findable block, and genuinely gone —
  since that logic has no build-time equivalent to lean on.
- **e2e**: select text → Highlight appears → reload → still there;
  Add a note → note visible in the Settings list; delete → gone from both
  the page and the list; narrow-screen toolbar stays inside the viewport
  (extending `test_narrow_screen.py`'s existing pattern); highlight
  contrast in both themes (extending `test_link_contrast.py`).

## 14. Rollout sketch

Each numbered piece below is small enough to be its own PR, in roughly
this order — a mistake in the anchoring algorithm (2) is worth catching
before any UI is built to depend on it (5 onward):

1. Retire `ROADMAP.md` Phases 3 and 4; add this document; log the
   decision (`DECISIONS_LOG.md` 7.155) — this PR.
2. The anchoring algorithm on its own: block-index counting, quote
   matching with the ±5 fallback window, and its unit tests — no UI yet.
3. Schema: `highlights` in `saveNow()`/`readSaved()`/`restoreSaved()`,
   with the restore-summary line for a dropped highlight; a round-trip
   unit test.
4. Wrap/unwrap a `Range` in `<mark class="dl-highlight">`, handling the
   multi-text-node case (§6), as a standalone function exercised by its
   own test before anything calls it from the UI.
5. The selection toolbar: extend `initReferenceLookup()`'s listener into
   the shared three-button toolbar (§5); Highlight button wired to (3)
   and (4).
6. The edit/remove popover on an existing `<mark>` (§7).
7. "Add a note" as the one-step combination of highlighting and opening
   the note editor.
8. The Highlights list in Settings → "Your work" (§8), including its
   empty-state guard.
9. Visual design pass: theme tokens for the highlight colour, the
   contrast test extension (§9).
10. Narrow-screen pass at 375px for the toolbar and the popover, tested
    from the start rather than discovered later (§9, §13).
11. e2e coverage for the full loop: highlight → note → reload → edit →
    delete → export (§13).
12. `docs/FOR_STUDENTS.md` gets a short paragraph — plain-language pass
    required (`CLAUDE.md`'s nine checks) — and `planning/PLAIN_LANGUAGE_PASS.md`
    is updated once it ships.
13. `planning/STATUS.md` gains the built-feature entry, in the same list
    as student notes and highlight-to-look-up, once the above is done.
