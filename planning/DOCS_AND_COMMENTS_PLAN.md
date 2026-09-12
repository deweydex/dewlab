# Documentation and code-comments plan (follow-up)

## Context

`planning/DOCS_AND_COMMENTS_PASS.md` records the first pass at this — one
`docs/<name>-explained.md` per substantial module, code comments, and a
language pass over every planning document — closed out **Complete**. Its
standing rule (a change isn't finished until the document describing it
describes the new behaviour) lives on in `CONTRIBUTING.md`. Its
comment-density standard does not: `CONTRIBUTING.md` now asks for a comment
only where the *why* isn't obvious from the code, kept to a line or two, and
a later repo-wide pass stripped the long teach-from comment blocks the first
pass added. What follows tracks documentation and explanation-file currency,
not comment density.

A standing rule only works while people actually follow it. Josh asked
(2026-09-06, alongside the same ask for `deweydex/dewstack`, which has never
had this pass at all — see that repository's own new
`planning/DOCS_AND_COMMENTS_PLAN.md`) for exactly this kind of check across
both repositories.

## What this is, and isn't

Not a second full pass. `DOCS_AND_COMMENTS_PASS.md`'s own scope was already
deliberate about what it did and didn't cover — Phase D's `dev/*.py` line,
for instance, named four scripts, not the whole folder, on purpose. This
document is for two different things: real drift since the first pass
closed (code that changed without its documentation catching up), and gaps
the first pass knowingly left out of scope.

## Found so far

- **`dev/label_report.py`, `dev/report_patterns.py`** — built after the
  first pass closed (Phase 8 of `DECISIONS_LOG.md`), never added to
  `docs/dev-scripts-explained.md`. Real drift. Fixed 2026-09-06 — see that
  file's own new sections.
- **Six more `dev/*.py` scripts never covered by `dev-scripts-explained.md`
  at all** (`check_doc_links.py`, `apply_topic_edits.py`,
  `build_topic_editor.py`, `build_topic_game.py`, `draw_topic_graph.py`,
  `pair_results.py`) — a scoping gap from the first pass, not new drift;
  recorded honestly in that file's own "Not yet covered here" section
  rather than implied away.
- **A systematic audit is still owed, not yet done.** The finding above
  came from spot-checking one file while scoping this plan, not from
  reading every runtime file against its own explanation file. Still
  needed: walk `assets/*.py`, `assets/*.js`, `compose/*.js`, and `build.py`
  against their matching `docs/*-explained.md` files, plus `ARCHITECTURE.md`
  and `DECISIONS_LOG.md` against what Phase 8 (the student feedback
  pathway: report doors, the cell report icon, the pattern-detection job)
  actually shipped, since that phase's `DECISIONS_LOG.md` entries are the
  newest code in the repository and the first place drift would show up.
- **The tutorial-code side isn't tracked.**
  `.claude/skills/cell-code-review/SKILL.md` exists and is sound, but
  nothing in this repository tracks which tutorials have actually been run
  through it, the way `planning/PLAIN_LANGUAGE_PASS.md` tracks the prose
  pass. Not yet decided whether that's a real gap or whether the
  plain-language pass and this repository's overall newness make it moot.

## How this gets worked

Read a file against its explanation file (or against `ARCHITECTURE.md`, for
something smaller that never got its own), fix what's actually stale, and
add what's missing. A bug found on the way gets fixed inline if it's small
and local to the file being read; anything bigger gets flagged here or
spawned as its own task rather than expanding the documentation change that
found it.

## Ledger

| Area | Status |
|---|---|
| `dev/label_report.py` / `dev/report_patterns.py` docs | done, 2026-09-06 |
| The other six `dev/*.py` scripts | not started |
| Full audit: runtime files vs. their explanation files | not started |
| `ARCHITECTURE.md`/`DECISIONS_LOG.md` vs. Phase 8's actual code | not started |
| Tutorial cell-code-review coverage tracking | not decided whether needed |
