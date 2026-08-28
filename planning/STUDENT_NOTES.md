# Student notes: a place of their own, and encouraging a copy that outlives the browser

Design note. The plain version is built — DECISIONS_LOG.md 7.72: the
`notes` field, the textarea in Settings, the first-use hint line from §4's
smaller proposal. §4's second, larger proposal — a staleness marker on the
export button — is still open; see `OPEN_QUESTIONS.md`. Kept below for the
reasoning, not as an open task. Answers "does this make sense?" first, then
designs it against the mechanism the codebase already has for exactly this
kind of thing.

---

## 0. Not the same "notes" as `SIDEBAR_CONTENT.md`

Worth saying plainly, because the word is already spoken for: `planning/
SIDEBAR_CONTENT.md` designs **pedagogical notes** — short, author-written
asides (`<aside class="dl-note">`) that are part of a tutorial's own
content, the same for every reader, extending the cheat-sheet panel.

This is the opposite kind of thing: **a student's own free-text notes**,
written by that one reader, different for every reader, and not part of
the tutorial at all. Calling both "notes" in the same conversation invites
exactly the kind of confusion a reader of this doc a year from now would
have no way to untangle — so this document says **student notes**
throughout, and `SIDEBAR_CONTENT.md`'s stay **pedagogical notes**.

## 1. Does this make sense? Yes, and here is why

`planning/VERSIONING_AND_PROGRESS.md`'s "Save transport" section already
sets the philosophy this has to fit: autosave to `localStorage` is the
primary safety net, a manual "export to JSON" is the secondary path "for
moving to another device or keeping an offline copy," and — because
tutorials are ungraded practice — "losing progress here is an
inconvenience, not a lost grade." `tutorial-runtime.js` already builds
exactly that: `saveNow()`/`readSaved()` autosave every cell's code and
output to `dl-progress:<module>:<slug>`, and Settings already has a
working export/import pair (`initProgressSection()`) — download the saved
record as `<module>-<slug>-progress.json`, or load one back in, with a
mismatch check so an imported file from a different tutorial cannot
silently clobber the wrong one's work.

**Free-text notes fit this exact shape — student-owned, local by default,
already have a working export path to reuse.** The one real difference
worth naming, and the reason "encourage a download" deserves more than the
existing export button already quietly sitting in Settings: **cell code is
reproducible; a student's own sentence is not.** Losing an afternoon's
practice on `working-with-tables` costs nothing but time — the tutorial is
still there, and running it again reconstructs the same working code.
Losing the paragraph where a student worked out, in their own words, why
`x - 1` cancels does not have a "run it again" — that specific phrasing,
that specific way they got unstuck, is gone. The general "ungraded,
therefore low-stakes" reasoning in `VERSIONING_AND_PROGRESS.md` still holds
for the mechanism (local-only, no server, no account) — it does not follow
that notes deserve the same *quiet, easy-to-miss* export button cell code
gets, because what is actually lost on the two paths is not the same kind
of thing.

## 2. Where notes live: extend "Your work," not a new panel

Settings already has a section literally called this
(`#dl-settings-work`, `initProgressSection()`) — "the reader's work, the
download, and the reading texture," per the file's own top comment. A
student-notes textarea belongs there, immediately above the existing
export/import controls, for the same reuse-over-invention reason every
other piece of this project's UI history has favoured: no new panel, no
new toggle, no new open/close/mutual-exclusion wiring, and the export
button a student needs is now sitting directly under the thing they just
wrote instead of somewhere they have to go looking for.

**One existing assumption this breaks, in a good way.** `initProgressSection()`
currently removes the whole section on a page with zero cells — "a page
with no cells has nothing to save." That stops being true once notes
exist: a prose-and-mathematics tutorial has nothing *executable* to save,
but a reader can still want to write something down while reading it. The
section's guard becomes "nothing to save at all" (no cells **and** notes
disabled) rather than "no cells" — which, as a side effect, finally gives
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

No new save path, no new file format — the existing `dl-progress-export`
button already downloads this whole record, so notes ride along in the
same JSON the moment the field exists. Import already checks the file
belongs to this tutorial (`describeMismatch()`) before writing anything;
that check does not need to change to also protect notes, since it is
already keyed on the whole record, not per-field. `readSaved()`/
`restoreSaved()` gain the one-line counterpart on load: fill the textarea
from `record.notes` if present, same as a cell's `student_code` today.

## 4. Actually encouraging the download — without nagging

The existing export button is correct but passive: it works, and almost
nobody will find it without being told it exists. Two changes, both
small, both consistent with this project's established "a notice, never a
block" instinct (`VERSIONING_AND_PROGRESS.md`'s own phrase, for the
version-mismatch case):

- **A one-line hint the first time the notes field is used on a given
  tutorial** — not a popup, not a dialog that has to be dismissed, just a
  small line of text under the textarea: *"Notes are saved in this
  browser only. Download a copy to keep them anywhere else."* Dismissible
  once read, the same way a first-time hint anywhere else on the web
  usually works, or simply always present in small type — cheap either
  way, and a design detail rather than an architecture one.
- **A gentle staleness signal, not an interruption.** After a meaningful
  amount of new note text has accumulated since the last export (a rough
  heuristic — say, the notes have grown by some number of characters, or
  it has been a session since the last `dl-progress-export` click, tracked
  the same lightweight way `rememberVersion()` already tracks a small
  piece of per-tutorial state) the export button in Settings gains a
  small marker — a dot, a colour change, the same visual language
  `.dl-status-error` already uses for "something here wants your
  attention" — rather than a banner competing with the reading itself for
  space. Never blocks typing, never appears mid-sentence, and disappears
  the moment the student exports.

Both are proposals, not requirements — the one firm recommendation is the
"never a block" part, because a save mechanism that makes itself annoying
is the one thing that would make a student turn it off rather than use it.

## 5. Scope: per-tutorial notes first, not one course-wide notebook

Two shapes were worth weighing:

- **Per-tutorial** (this design): one notes field per `dl-progress:
  <module>:<slug>` record, exactly where the cell work already lives.
  Ships with zero new infrastructure — the record, the export button, the
  mismatch check all already exist and already work this way.
- **One running notebook across the whole course**: a single `dl-notes`
  record, not tied to any one tutorial, editable from anywhere. Arguably
  closer to how a student actually thinks — "things I'm still confused
  about" rarely respects a tutorial boundary — but needs real new
  plumbing this project does not have yet: its own export/import pair (a
  single global JSON, not per-tutorial), and somewhere to see and edit it
  that is not tied to being on one specific tutorial's page — the
  contents page, most likely, which currently has no save-related UI of
  its own at all.

**Recommendation: ship per-tutorial first.** It is the version that costs
nothing beyond the field itself, it is immediately useful (a note next to
the material it is about, found again by opening that tutorial), and it
does not foreclose a course-wide notebook later — that would be an
additive feature sitting beside this one, not a replacement, the same way
the mixed-practice pages sit beside single-tutorial ones without
replacing them. Worth revisiting only if per-tutorial notes turn out to
feel too fragmented in practice — a real possibility, not a foregone
conclusion, and one better judged after this ships than guessed at now.

## 6. What this does not do

- No rich text, no markdown rendering in the notes field — a plain
  `<textarea>`, matching the plain-text simplicity of `student_code` and
  keeping the save format a single string rather than a second markup
  pipeline to maintain.
- No sync between devices beyond the existing manual export/import — same
  as cell progress today; `VERSIONING_AND_PROGRESS.md` already floats an
  optional Gist-sync layer as a possible future path for saved work in
  general, and notes would ride along with that unchanged if it is ever
  built, since it operates on the same JSON record.
- Not the standalone single-file tutorial download (`standalone.bundle.js`,
  "download this tutorial to work offline") — a different existing
  feature, downloading the *tutorial*, not a student's *work on* it. Worth
  naming only so "save offline" is not misread as pointing at that button
  instead of the progress-export one this design extends.

## 7. Rollout sketch

Roughly: `notes` field in `saveNow()`/`readSaved()`/`restoreSaved()`, the
`initProgressSection()` guard update, tests (a unit test round-tripping
notes through export/import, an e2e test typing into the field and
confirming it survives a reload) → the textarea and hint text in
`shell.html`/`tutorial-style.css` → the staleness-marker UX, once the
plain version has shipped and it is clear whether it is still needed →
docs. Same staged-PR reasoning every other design in this planning
directory has given for its own rollout.
