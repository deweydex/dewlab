# Student notes: a place of their own, and encouraging a copy that outlives the browser

Built — DECISIONS_LOG.md 7.72 (the `notes` field, the textarea in Settings,
the first-use hint line) and 7.75 (§4's staleness marker on the export
button, opt-out in Settings). Kept below as the design record, not an open
task.

---

## 0. Not the same "notes" as `SIDEBAR_CONTENT.md`

`planning/SIDEBAR_CONTENT.md` designs **pedagogical notes** — short,
author-written asides (`<aside class="dl-note">`) that are part of a
tutorial's own content, the same for every reader, extending the
reference panel.

This is the opposite: **a student's own free-text notes**, written by
that one reader, different for every reader, and not part of the
tutorial at all. To keep the two from colliding, this document says
**student notes** throughout, and `SIDEBAR_CONTENT.md`'s stay
**pedagogical notes**.

## 1. Does this make sense? Yes, and here is why

`planning/VERSIONING_AND_PROGRESS.md`'s "Save transport" section sets the
philosophy this has to fit: autosave to `localStorage` is the primary
safety net, and a manual "export to JSON" is the secondary path, since
tutorials are ungraded practice and losing progress is an inconvenience,
not a lost grade. `tutorial-runtime.js` already builds exactly that:
`saveNow()`/`readSaved()` autosave every cell's code and output to
`dl-progress:<module>:<slug>`, and Settings already has a working
export/import pair (`initProgressSection()`), with a mismatch check so an
imported file from a different tutorial can't silently clobber the wrong
one's work.

Free-text notes fit this exact shape: student-owned, local by default,
with a working export path to reuse already. The one real difference:
**cell code is reproducible; a student's own sentence is not.** Losing an
afternoon's practice on `working-with-tables` costs nothing but time — the
tutorial is still there, and running it again reconstructs the same
working code. Losing the paragraph where a student worked out, in their
own words, why `x - 1` cancels has no "run it again" — that specific
phrasing is gone for good. The mechanism (local-only, no server, no
account) stays right for notes too, but because what's lost on the two
paths isn't the same kind of thing, notes deserve more than the quiet,
easy-to-miss export button cell code gets — see §4.

## 2. Where notes live: extend "Your work," not a new panel

Settings already has a section for exactly this (`#dl-settings-work`,
`initProgressSection()`) — "the reader's work, the download, and the
reading texture," per the file's own top comment. A student-notes
textarea belongs there, immediately above the existing export/import
controls: no new panel, no new toggle, no new open/close/mutual-exclusion
wiring, and the export button sits directly under what the student just
wrote.

This breaks one existing assumption, in a good way. `initProgressSection()`
currently removes the whole section on a page with zero cells, on the
reasoning that a page with no cells has nothing to save. That stops being
true once notes exist: a prose-and-mathematics tutorial has nothing
*executable* to save, but a reader can still want to write something down
while reading it. The section's guard becomes "nothing to save at all"
(no cells **and** notes disabled) rather than "no cells" — which gives
every tutorial, not just ones with code, a place for a student's own
material.

## 3. Storage and export: the same record, one more field

`saveNow()`'s record gains `notes: string` alongside `cells`:

```json
{
  "tutorial-slug": "working-with-tables",
  "tutorial-module": "computational-methods",
  "tutorial-version": "2026.08.23.1",
  "saved_at": "2026-08-28T09:00:00.000Z",
  "notes": "the ISO date sort trick only works because...",
  "cells": [ ... ]
}
```

No new save path, no new file format: the existing `dl-progress-export`
button already downloads this whole record, so notes ride along in the
same JSON the moment the field exists. Import already checks the file
belongs to this tutorial (`describeMismatch()`) before writing anything;
that check doesn't need to change, since it's keyed on the whole record,
not per-field. `readSaved()`/`restoreSaved()` gain the one-line
counterpart on load: fill the textarea from `record.notes` if present,
same as a cell's `student_code` today.

## 4. Actually encouraging the download — without nagging

The existing export button works but is passive — almost nobody will find
it without being told it exists. Two small changes, both consistent with
this project's "a notice, never a block" instinct (`VERSIONING_AND_PROGRESS.md`'s
own phrase, for the version-mismatch case):

- **A one-line hint the first time the notes field is used on a given
  tutorial** — a small line of text under the textarea: *"Notes are saved
  in this browser only. Download a copy to keep them anywhere else."*
  Dismissible once read, or simply always present in small type.
- **A gentle staleness signal, not an interruption.** Once a meaningful
  amount of new note text has accumulated since the last export (a rough
  heuristic on character count or elapsed session, tracked the same
  lightweight way `rememberVersion()` already tracks other per-tutorial
  state), the export button in Settings gains a small marker — the same
  visual language `.dl-status-error` already uses for "something here
  wants your attention" — rather than a banner competing with the reading
  for space. Never blocks typing, never appears mid-sentence, and
  disappears the moment the student exports.

Both are proposals, not requirements. The one firm recommendation is
"never a block": a save mechanism that makes itself annoying is what
would make a student turn it off rather than use it.

## 5. Scope: per-tutorial notes first, not one course-wide notebook

Two shapes:

- **Per-tutorial** (this design): one notes field per `dl-progress:
  <module>:<slug>` record, exactly where the cell work already lives.
  Ships with zero new infrastructure — the record, the export button, the
  mismatch check all already exist and already work this way.
- **One running notebook across the whole course**: a single `dl-notes`
  record, not tied to any one tutorial, editable from anywhere. Closer to
  how a student actually thinks, since "things I'm still confused about"
  rarely respects a tutorial boundary — but needs real new plumbing: its
  own export/import pair (a single global JSON, not per-tutorial), and
  somewhere to see and edit it that isn't tied to one tutorial's page —
  the contents page, most likely, which currently has no save-related UI
  of its own at all.

**Recommendation: ship per-tutorial first.** It costs nothing beyond the
field itself, is immediately useful (a note next to the material it is
about, found again by opening that tutorial), and doesn't foreclose a
course-wide notebook later — that would sit beside this one, not replace
it, the same way mixed-practice pages sit beside single-tutorial ones.
Worth revisiting only if per-tutorial notes turn out to feel too
fragmented in practice, judged after this ships rather than guessed at
now.

## 6. What this does not do

- No rich text, no markdown rendering in the notes field — a plain
  `<textarea>`, matching the plain-text simplicity of `student_code` and
  keeping the save format a single string rather than a second markup
  pipeline to maintain.
- No sync between devices beyond the existing manual export/import, same
  as cell progress today. `VERSIONING_AND_PROGRESS.md` floats an optional
  Gist-sync layer as a possible future path for saved work in general;
  notes would ride along with that unchanged, since it operates on the
  same JSON record.
- Not the standalone single-file tutorial download (`standalone.bundle.js`,
  "download this tutorial to work offline") — that downloads the
  *tutorial*, not a student's *work on* it, so "save offline" here should
  not be read as pointing at that button instead of the progress-export
  one this design extends.

## 7. Rollout sketch

Roughly: `notes` field in `saveNow()`/`readSaved()`/`restoreSaved()`, the
`initProgressSection()` guard update, tests (a unit test round-tripping
notes through export/import, an e2e test typing into the field and
confirming it survives a reload) → the textarea and hint text in
`shell.html`/`tutorial-style.css` → the staleness-marker UX, once the
plain version has shipped and it's clear whether it's still needed →
docs.
