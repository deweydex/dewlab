# Documentation and code-comments plan (follow-up)

## Context

`planning/DOCS_AND_COMMENTS_PASS.md` records the first pass at this —
pedagogical comments across the codebase, one `docs/<name>-explained.md`
per substantial module, `ARCHITECTURE.md`/`README.md` brought current, a
language pass over every planning document — closed out **Complete**,
with the standing rule (a change is not finished until the document
describing that behaviour describes the new one) living on in
`CONTRIBUTING.md`. That file stays as the historical record of how the
first pass was scoped; this one is where a follow-up lives, since a
standing rule only works while people actually follow it, and Josh
asked (2026-09-06, alongside the same ask for `deweydex/dewstack`,
which has never had this pass at all — see that repository's own new
`planning/DOCS_AND_COMMENTS_PLAN.md`) for exactly this kind of check
across both repositories.

## What this is, and isn't

Not a second full pass. `DOCS_AND_COMMENTS_PASS.md`'s own scope was
already deliberate about what it did and didn't cover — Phase D's
`dev/*.py` line, for instance, named four scripts, not the whole
folder, on purpose. This document is for two different things:

1. **Real drift since the first pass closed** — code that changed
   without its documentation catching up, which the standing rule was
   supposed to prevent and evidently didn't, every time.
2. **Gaps the first pass knowingly left out of scope**, now worth
   closing rather than leaving as a permanent exception.

## Found so far

- [x] **`dev/label_report.py`, `dev/report_patterns.py`** — built this
      session (Phase 8 of `DECISIONS_LOG.md`), never added to
      `docs/dev-scripts-explained.md`. Real drift: both scripts landed
      after the first pass closed, with no documentation update
      alongside them. Fixed 2026-09-06 — see that file's own new
      sections.
- [ ] **Six more `dev/*.py` scripts never covered by `dev-scripts-explained.md`
      at all** (`check_doc_links.py`, `apply_topic_edits.py`,
      `build_topic_editor.py`, `build_topic_game.py`,
      `draw_topic_graph.py`, `pair_results.py`) — a scoping gap from
      the first pass, not new drift; recorded honestly in that file's
      own "Not yet covered here" section rather than implied away.
- [ ] **A systematic audit is still owed, not yet done.** The finding
      above came from spot-checking one file while scoping this plan,
      not from reading every runtime file against its own explanation
      file. Before this checklist can honestly grow past what's listed
      here, someone needs to actually walk `assets/*.py`, `assets/*.js`,
      `compose/*.js`, and `build.py` against their matching
      `docs/*-explained.md` files, plus `ARCHITECTURE.md` and
      `DECISIONS_LOG.md` against what Phase 8 (the student feedback
      pathway: report doors, the cell report icon, the pattern-detection
      job) actually shipped, since that phase's own `DECISIONS_LOG.md`
      entries are the newest code in the repository and the first place
      drift would show up.
- [ ] **The tutorial-code side** — `.claude/skills/cell-code-review/SKILL.md`
      exists and is sound, but nothing in this repository tracks which
      tutorials have actually been run through it, the way
      `planning/PLAIN_LANGUAGE_PASS.md` tracks the prose pass. Worth
      deciding whether that's a real gap (some tutorials' cell code has
      never been reviewed this way) or whether the plain-language pass
      and this repository's overall newness make it moot — not yet
      checked.

## How this gets worked

Same triage as the standing rule already implies: read a file against
its explanation file (or against `ARCHITECTURE.md`, for something
smaller that never got its own), fix what's actually stale, and add
what's missing. A bug found on the way gets fixed inline if it's small
and local to the file being read; anything bigger gets flagged here or
spawned as its own task rather than expanding the documentation change
that found it.

## Ledger

| Area | Status |
|---|---|
| `dev/label_report.py` / `dev/report_patterns.py` docs | done, 2026-09-06 |
| The other six `dev/*.py` scripts | not started |
| Full audit: runtime files vs. their explanation files | not started |
| `ARCHITECTURE.md`/`DECISIONS_LOG.md` vs. Phase 8's actual code | not started |
| Tutorial cell-code-review coverage tracking | not decided whether needed |
