# Documentation and code-comments pass

## Context

After the Mini IDE redesign (`planning/MINI_IDE_REDESIGN.md`), the project
owner asked for two things across the whole repository, not just this
redesign's own files: plain, jargon-light language in every document, and a
comment/documentation pass — every substantial code file gets one
`docs/<file>-explained.md` architecture walkthrough, and, at the time, a
comment on every function detailed enough to teach from. The standing rule
that followed — a change isn't finished until the document describing it
describes the new behaviour — lives in `CONTRIBUTING.md`.

**The comment-density standard has since been reversed.**
`CONTRIBUTING.md`'s comment policy now asks for comments only where the
*why* isn't obvious from the code itself — a constraint, a workaround, a
non-obvious ordering — kept to a line or two, with no banner comments,
section dividers, or walkthroughs of what the next ten lines do. A later
repo-wide pass stripped the long, teach-from comment blocks this document
describes adding. The `docs/<file>-explained.md` explanation-file
convention this pass introduced is still current — that's where a
walkthrough of a file's structure belongs now, not inline.

## Readers differ

`docs/MINI_IDE.md` and in-app help text are read by students.
`README.md`, `ARCHITECTURE.md`, `DECISIONS_LOG.md`, and `planning/*.md` are
read by maintainers and contributors — `README.md` says so directly. The
language pass applied everywhere as a *style* change (plain sentences, no
needless jargon, no metaphor for its own sake) while each document kept
addressing its actual reader, rather than rewriting maintainer docs to a
student's level.

## Scope (as decided)

- **Language pass** — every doc in the repo: full teen-friendly voice for
  student-facing content, plain jargon-light style for maintainer and
  contributor docs, each addressed to its actual reader.
- **Code comments** — every function, across the whole codebase. Superseded
  since — see the note under Context.
- **Explanation files** — one `docs/<name>-explained.md` per substantial
  module, in the directory convention `docs/MINI_IDE.md` already used.
- **Standing check** — `CONTRIBUTING.md`.

## Size

Roughly 18,700 lines across roughly 40 files — sequenced as phases rather
than attempted as one pass, the same shape as the Mini IDE redesign itself.

## What happened, by phase

**A — quick, high-visibility.** The homepage's mention of dewmini alongside
Mini IDE; `CONTRIBUTING.md` itself; a language pass and restructure on
`docs/MINI_IDE.md` (dropping developer-facing sections that don't belong in
a student-facing doc); the same pass on `docs/DEWMINI.md`, which landed
mid-effort via PR #71. `main`'s concurrent dewmini feature work (sqlite3,
Pillow, an `image_input` widget, doc-cell image attach — PR #69/#71) merged
cleanly and was covered by Phases C and D, not just what this effort
originally targeted.

**B — this redesign's own code.** `assets/mini-ide.js`, `mini-ide-engine.js`,
and `mini-ide-fs.js` — comments plus a matching `docs/<file>-explained.md`
each.

**C — the shared runtime this redesign builds on.** `assets/tutorial_tools.py`
(including `run_query` and `image_input`) and `assets/pyodide-worker.js` —
same treatment.

**D — the rest of the codebase.** `assets/tutorial-runtime.js`,
`compose/dewmini.js`, `build.py`, and four `dev/*.py` scripts
(`fetch_pyodide.py`, `from_notebook.py`, `generate_doc_snippets.py`,
`curriculum_map.py`) — same treatment.

**E — the whole-repo language pass.** `README.md` and `ARCHITECTURE.md`
were already plain and direct; both had a real staleness gap instead — the
directory map and cross-references hadn't caught up with Phases A–D, and
`ARCHITECTURE.md` was missing an entire section on Mini IDE's redesigned
engine and filesystem layer, added as §4 with what followed it renumbered.
All of `planning/*.md` (~25 files) were surveyed: most needed nothing.
`STATUS.md`, `planning/README.md`, `CURRICULUM_NOTES.md`, `VERSIONS.md`,
`WINDOW_AUDIT.md`, `EDITOR.md`, and the intros of `REFERENCE_PANEL.md` and
`PRACTICE.md` had drifted into a consulting-report register ("Implementation
Guarantee", "Technical Specification") and were rewritten to match the rest
of the repository, with every fact, number, and decision preserved.
`STATUS.md` and `planning/README.md` were also missing the Mini IDE redesign
and this documentation initiative; both are folded in now.
`planning/Educational Content guide for LLMs.md` referenced subdirectories
this repository doesn't have and read as an orphaned import from elsewhere;
left alone at the time, it has since been deleted for that reason (see
`planning/ROADMAP.md` Phase 1). `planning/curriculum/` and
`planning/outlines/` (data files and per-tutorial outlines) weren't surveyed
individually — out of scope for a repo-conventions language pass.
`DECISIONS_LOG.md` (2712 lines) was spot-checked and left unchanged: already
plain and direct, and rewriting a historical record for tone risks the
accuracy `CONTRIBUTING.md` asks it to keep.

## Status

Complete. Keeping documentation and comments current going forward is
`CONTRIBUTING.md`'s job, not this document's — this stays as the record of
how the original pass was scoped and sequenced. Its comment-density standard
no longer applies; see the note under Context.
