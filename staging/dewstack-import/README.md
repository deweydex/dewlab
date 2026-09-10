# dewstack import staging

A verbatim, unedited copy-in from `deweydex/dewstack`, taken at commit
`892e8780d7ca797a5c2cdfeb9205d3052d4f7c86` (2026-09-08, "Turn the student
report doors off"). Not built, not linked, not live — `build.py` only
globs `tutorials/`, not `staging/`, so nothing here reaches `site/`.

See `planning/DEWSTACK_MERGE.md` for what this is for and the phased plan
that reads from it. In short: this folder is the source material for
porting dewstack's `data` and `web` tracks into dewlab's own
`tutorials/database-methods/` and `tutorials/web-authoring/`, and the
engine files (`assets/site-editor.js`, `assets/sql-cell.js`,
`assets/sql_tools.py`, `assets/python_tools.py`, `assets/workspace.js`)
that back them, rebuilt against dewlab's own conventions rather than
copied.

**Nothing in this folder gets edited in place.** The actual port happens
by reading from here and writing into dewlab's real `tutorials/` and
`assets/` trees. Once a module's port is done and has run in front of a
class, delete that module's slice of this folder; delete the whole
folder once nothing in it is still being read from. dewstack's own copy
of this content is untouched by any of this and stays up in its own
repository throughout.

## What's here

- `tutorials/data/` — 12 pages, the source for `database-methods`.
- `tutorials/web/` — 30 pages, the source for `web-authoring`.
- `tutorials/full-stack/` — the one page dewstack has so far; reference
  only, not scheduled for porting yet (`planning/DEWSTACK_MERGE.md` §2).
- `tutorials/modules.yaml` — dewstack's own module ordering, for
  reference when deciding dewlab's `database-methods`/`web-authoring`
  ordering.
- `assets/` — the five engine source files these two tracks run on.
- `planning/CONSOLIDATION_PLAN.md`, `planning/NEXT_STEPS.md` — dewstack's
  own migration ledger and rationale, for the "why" behind what's already
  considered done on the dewstack side.
