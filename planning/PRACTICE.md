# Practice pages and student-created problems

What a practice page is, what it's built on, and how the
runtime-created-cell feature works.

---

## 1. What this covers

A practice module is a practice document paired with a tutorial. It
gives a student three things:
1. Real problems, checked instantly, client-side (`check()`).
2. A reflection prompt before and after the problem set.
3. The ability to create their own cell at runtime and share it with
   someone else — see §5.

## 2. What already exists to build this on

- **The widget bridge** — `text_input`, `dropdown`, and `button` in
  `assets/tutorial_tools.py` are the interactive controls a problem can
  use.
- **`check()`** — pass/not-yet feedback, instantly, with nothing scored
  or logged anywhere.
- **Saved work and export** — `localStorage` already saves a student's
  code by cell id, and JSON export/import already gives a way to back up
  or hand off work.

## 3. What a runtime cell needed (now built — see §5)

An ordinary dewlab cell is static — defined once, at build time, in the
tutorial's own Markdown. Letting a student create their *own* cell means
cells that don't exist until runtime, which needs four things:

- **Somewhere to store them.** Its own, separate `localStorage` key
  (`dewlab:custom-cells:<module>:<slug>`), kept apart from the
  tutorial's own saved-work record — so version-matching logic never
  has to account for custom cells at all.
- **Ids that can't collide.** `custom-<timestamp>-<random>`, so it can
  never clash with a real manifest cell (a tutorial author would never
  write an id starting with `custom-`) or with a cell someone else
  shares (a fresh id is always minted on import, never trusted from the
  file).
- **No tie to a version.** True by construction: a custom cell was
  never part of the versioned record, so there's nothing for a version
  comparison to notice.
- **A clear line around trust.** A cell loaded from a shared file is
  never auto-run. Settings says plainly, before anything runs, that a
  loaded cell behaves like any other code on the page, and running
  still needs the reader's own explicit click, the same as every cell
  on the site already requires.

## 4. What a practice page looks like

Three parts, in order:

1. **Before the problems** — a short reflection prompt (how confident do
   you feel, what looks hardest), never graded.
2. **The problems themselves** — a sequence that moves from a plain
   calculation through a multi-step one to writing a function, each
   checked with `check()`.
3. **After the problems** — a prompt asking what worked, and what
   turned out to be surprising.

## 5. What's done, and what's still just a plan

1. ~~**Static practice pages**~~ — done. Thirty-two per-tutorial pages
   and four mixed sets; see `EXERCISES.md`.
2. ~~**Wired into the build**~~ — done. `practice_for:` links a page back
   to its tutorial both ways; `practice_across:` covers a set with no
   single owner. Both are checked at build time and covered by fourteen
   tests.
3. ~~**A runtime cell engine**~~ — done. A reader can add their own cell
   at runtime, on any page that already has cells of its own — see
   `docs/tutorial-runtime-explained.md`'s "Custom cells" section for how
   it's built and, especially, how it stays deliberately separate from
   the tutorial's own saved-work and version system.
4. ~~**Sharing a problem with someone else**~~ — done. Each custom cell
   has its own "share" button (downloads it as a small JSON file) and
   Settings has a matching "Load a shared cell" — file-based, the same
   trust model the existing progress export/import already uses. A
   loaded cell is never auto-run.

Everything above is built. Not attempted, deliberately: a structured
problem-authoring UI (a title, an expected answer, a rating or discovery
system for shared cells) — a custom cell is plain Python, and a reader's
own `check(...)` call inside it already serves as their verification
test. That would be a larger, separate feature, not a gap in the above.

**A practice page doesn't need `check()` under every question.** It
needs a few tools per section and the answer behind a fold. Sixty
CodeMirror instances on one page makes for a slow page, and a check
under every question invites running it instead of thinking about the
answer.
