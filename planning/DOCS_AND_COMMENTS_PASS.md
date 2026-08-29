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
- [ ] `CONTRIBUTING.md` — the standing check
- [ ] `docs/MINI_IDE.md` — language pass (already written for this
      redesign; needs a friendlier pass, not a rewrite)
- [ ] `docs/DEWMINI.md` — same pass; this file didn't exist when this plan
      was first written (it landed via PR #71, merged into `main` around
      the same time as this redesign) — same audience as
      `docs/MINI_IDE.md`, same treatment

Note: `main` also picked up dewmini's own feature work (sqlite3, Pillow,
an `image_input` widget in `tutorial_tools.py`, doc-cell image attach —
PR #69/#71) while this session was running. It merged cleanly with no
conflicts; `tutorial_tools.py`'s pedagogical-comment pass (Phase C) and
`compose/dewmini.js`'s (Phase D) both need to account for that code now,
not just what this session originally wrote.

**Phase B — this redesign's own code (freshest, most relevant)**
- [ ] `assets/mini-ide.js` (1751 lines) — pedagogical comments +
      `docs/mini-ide-js-explained.md`
- [ ] `assets/mini-ide-engine.js` (570 lines) — pedagogical comments +
      `docs/mini-ide-engine-explained.md`
- [ ] `assets/mini-ide-fs.js` (281 lines) — pedagogical comments +
      `docs/mini-ide-fs-explained.md`

**Phase C — the shared runtime this redesign builds on**
- [ ] `assets/tutorial_tools.py` (1025 lines, incl. `run_query`) —
      pedagogical comments + `docs/tutorial-tools-explained.md`
- [ ] `assets/pyodide-worker.js` (348 lines) — pedagogical comments +
      `docs/pyodide-worker-explained.md`

**Phase D — the rest of the codebase**
- [ ] `assets/tutorial-runtime.js` (1967 lines) — pedagogical comments +
      `docs/tutorial-runtime-explained.md`
- [ ] `compose/dewmini.js` (1214 lines) — pedagogical comments +
      `docs/dewmini-js-explained.md`
- [ ] `build.py` (2891 lines) — pedagogical comments +
      `docs/build-explained.md`
- [ ] `dev/*.py` (fetch_pyodide.py, from_notebook.py,
      generate_doc_snippets.py, curriculum_map.py) — pedagogical comments
      + `docs/dev-scripts-explained.md`

**Phase E — the "whole repo" language pass**
- [ ] `README.md` (648 lines)
- [ ] `ARCHITECTURE.md` (423 lines)
- [ ] `planning/*.md` (roughly 20 files, mostly short) — including
      `planning/PEDAGOGICAL_STYLE_GUIDE.md`, which already governs
      *tutorial content's* voice and is the natural place to check this
      pass against for consistency
- [ ] `DECISIONS_LOG.md` (2664 lines) — a careful, low-priority pass; a
      historical record, not something to simplify at the cost of
      accuracy

## Status

- [x] Phase A.1 — homepage dewmini mention
- [ ] Phase A.2 — CONTRIBUTING.md
- [ ] Phase A.3 — docs/MINI_IDE.md language pass
- [ ] Phase B — Mini IDE's own JS files
- [ ] Phase C — shared runtime (tutorial_tools.py, pyodide-worker.js)
- [ ] Phase D — rest of the codebase
- [ ] Phase E — whole-repo language pass
