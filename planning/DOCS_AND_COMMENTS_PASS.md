# Documentation and Code-Comments Pass

## Context

After the Mini IDE redesign (`planning/MINI_IDE_REDESIGN.md`), the project
owner asked for two related, ongoing things:

1. **Accessible language everywhere.** Plain, friendly, metaphor-free
   writing suitable for a teenage student, across the repo's
   documentation — not just the student-facing pages.
2. **Pedagogical code comments.** Every function across the codebase
   gets a comment explaining what it does and why, detailed enough to
   teach from — not the codebase's existing minimal, why-only comment
   style. One explanation file per module/file elaborates on structure
   beyond what fits as inline comments.

They also asked that this become a standing check going forward — new
code and doc changes should keep both current, not just this one pass.
That's `CONTRIBUTING.md` at the repo root.

## One clarification worth recording

Not every document in the repo has the same *reader*. `docs/MINI_IDE.md`
and the in-app help text are read by students. `README.md`, `ARCHITECTURE.md`,
`DECISIONS_LOG.md`, and `planning/*.md` are read by teachers and
maintainers deciding whether to build a course in dewlab, or a
contributor changing the code — `README.md` says so explicitly ("If you
are deciding whether to write your next set of materials in dewlab...").
Rewriting those to *address* a 14-year-old would break what they're for:
`DECISIONS_LOG.md` in particular is a historical record of engineering
decisions, not a tutorial.

So the language pass applies everywhere as a **style** change — plain
sentences, no needless jargon, no metaphor for its own sake — while each
document keeps addressing its actual reader. Flagging this here so it's
a visible decision, not a silent reinterpretation of "the whole repo."

## Scope (as decided)

- **Language pass**: every doc in the repo — student-facing content in
  full teen-friendly voice; maintainer/contributor docs in plain,
  jargon-light style while staying addressed to their actual reader (see
  above).
- **Code comments**: every function, across the whole codebase, not just
  this redesign's own files.
- **Explanation files**: one per module — `docs/<name>-explained.md` or
  similar, in the same directory convention as `docs/MINI_IDE.md`.
- **Standing check**: `CONTRIBUTING.md` at the repo root.

## Size

~18,700 lines across roughly 40 files. Not achievable as one pass — this
tracks it as a sequenced effort, same shape as the Mini IDE redesign.

## Sequencing

**Phase A — quick, high-visibility**
- [x] Homepage: mention dewmini alongside Mini IDE (`build.py`'s
      `write_index()`)
- [x] `CONTRIBUTING.md` — the standing check
- [x] `docs/MINI_IDE.md` — language pass, and restructured to drop
      developer-facing sections that don't belong in a student-facing doc
- [x] `docs/DEWMINI.md` — same pass; this file didn't exist when this plan
      was first written (it landed via PR #71, merged into `main` around
      the same time as this redesign) — same audience as
      `docs/MINI_IDE.md`, same treatment

Note: `main` also picked up dewmini's own feature work (sqlite3, Pillow,
an `image_input` widget in `tutorial_tools.py`, doc-cell image attach —
PR #69/#71) while this session was running. It merged cleanly with no
conflicts; `tutorial_tools.py`'s pedagogical-comment pass (Phase C) and
`compose/dewmini.js`'s (Phase D) both accounted for that code, not just
what this session originally wrote.

**Phase B — this redesign's own code (freshest, most relevant)**
- [x] `assets/mini-ide.js` (1751 lines) — pedagogical comments +
      `docs/mini-ide-js-explained.md`
- [x] `assets/mini-ide-engine.js` (570 lines) — pedagogical comments +
      `docs/mini-ide-engine-explained.md`
- [x] `assets/mini-ide-fs.js` (281 lines) — pedagogical comments +
      `docs/mini-ide-fs-explained.md`

**Phase C — the shared runtime this redesign builds on**
- [x] `assets/tutorial_tools.py` (1025 lines, incl. `run_query` and
      `image_input`) — pedagogical comments + `docs/tutorial-tools-explained.md`
- [x] `assets/pyodide-worker.js` (348 lines) — pedagogical comments +
      `docs/pyodide-worker-explained.md`

**Phase D — the rest of the codebase**
- [x] `assets/tutorial-runtime.js` (1967 lines) — pedagogical comments +
      `docs/tutorial-runtime-explained.md`
- [x] `compose/dewmini.js` (1214 lines) — pedagogical comments +
      `docs/dewmini-js-explained.md`
- [x] `build.py` (2893 lines) — pedagogical comments +
      `docs/build-explained.md`
- [x] `dev/*.py` (fetch_pyodide.py, from_notebook.py,
      generate_doc_snippets.py, curriculum_map.py) — pedagogical comments
      + `docs/dev-scripts-explained.md`

**Phase E — the "whole repo" language pass**
- [x] `README.md` — already in plain, direct language; fixed a real
      staleness gap instead (the directory map and cross-references
      hadn't caught up with everything Phases A-D added)
- [x] `ARCHITECTURE.md` — same finding: already plain and direct, but
      missing an entire section on Mini IDE's redesigned engine and
      filesystem layer. Added §4, renumbered what followed it.
- [x] `planning/*.md` — surveyed all ~25 files. Most were already in the
      same plain, direct voice as the rest of the repo and needed
      nothing. A distinct subset (`STATUS.md`, this file's own
      `README.md`, `CURRICULUM_NOTES.md`, `VERSIONS.md`, `WINDOW_AUDIT.md`,
      `EDITOR.md`, plus the intros of `REFERENCE_PANEL.md` and
      `PRACTICE.md`)
      had drifted into a noticeably different, consulting-report register
      ("Implementation Guarantee", "Technical Specification",
      "Fundamental Requirements") — rewritten to match, with every fact,
      number, and decision preserved. `STATUS.md` and `planning/README.md`
      were also missing the Mini IDE redesign and this whole docs
      initiative; both are folded in now.
      `planning/Educational Content guide for LLMs.md` was left alone at
      the time: it referenced subdirectories (`by_content_type/`, etc.)
      that don't exist in this repo, so it read as an orphaned import from
      elsewhere, not a document this repo's conventions actually govern.
      It has since been deleted for exactly that reason — see
      `planning/ROADMAP.md` Phase 1.
      `planning/curriculum/` and `planning/outlines/` (data files and
      per-tutorial outlines) weren't surveyed individually — out of scope
      for a repo-conventions language pass.
- [x] `DECISIONS_LOG.md` (2712 lines) — spot-checked, left unchanged. It
      was already in the same plain, direct voice as everywhere else;
      rewriting a historical record for tone risks the accuracy
      CONTRIBUTING.md asks it to keep.

## Status

Complete. Every phase above is checked off. Going forward, keeping this
current is `CONTRIBUTING.md`'s job, not this file's — this document stays
as the record of how the initial pass was scoped and sequenced.
