# Practice pages and student-created problems

What a practice page is, what it's built on, and the one part of this
plan — runtime-created cells and peer-shared problems — that's still
just a plan.

---

## 1. What this covers

A practice module is a practice document paired with a tutorial. It
gives a student three things:
1. Real problems, checked instantly, client-side (`check()`).
2. A reflection prompt before and after the problem set.
3. (Not built yet) the ability to create their own problem at runtime
   and share it with someone else.

## 2. What already exists to build this on

- **The widget bridge** — `text_input`, `dropdown`, and `button` in
  `assets/tutorial_tools.py` are the interactive controls a problem can
  use.
- **`check()`** — pass/not-yet feedback, instantly, with nothing scored
  or logged anywhere.
- **Saved work and export** — `localStorage` already saves a student's
  code by cell id, and JSON export/import already gives a way to back up
  or hand off work.

## 3. What a runtime cell would need

An ordinary dewlab cell is static — defined once, at build time, in the
tutorial's own Markdown. Letting a student create their *own* problem
means cells that don't exist until runtime, and that's a different
thing to build:

- **Somewhere to store them.** A dynamically created cell needs to live
  in local storage alongside the cells the build-time manifest already
  knows about.
- **Ids that can't collide.** A cell created this way needs its own id
  scheme (`custom-<uuid>` or `custom-<timestamp>`) so it can never clash
  with a real manifest cell or with a problem someone else shares.
- **No tie to a version.** A student-created cell doesn't belong to any
  tutorial release — it has to survive a version change untouched,
  since there's no version it was ever "written for."
- **A clear line around trust.** A problem a student imports from a
  peer still runs inside Pyodide's WebAssembly sandbox — isolated from
  the operating system, but still running within the browser tab's own
  origin. The page has to say plainly when it's about to run someone
  else's code.

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
3. **A runtime cell engine** — not built. Would mean dynamic cell
   insertion and mounting a CodeMirror editor for it, in
   `assets/tutorial-runtime.js`.
4. **Sharing a problem with someone else** — not built. Would extend the
   export/import tools to package a student-authored problem as a
   portable JSON snippet.

Steps 3 and 4 are the two still open, and they're the two that actually
need runtime code rather than more content. Nothing written so far
depends on them — every practice page in the repository today is
static, which was the point of building them in that order.

One thing the static pages settled, that this document originally
assumed would need code to solve: **a practice page doesn't need
`check()` under every question.** What it needs is a few tools per
section and the answer behind a fold. Sixty CodeMirror instances on one
page makes for a slow page, and a check under every single question
invites running it instead of actually thinking about the answer.
