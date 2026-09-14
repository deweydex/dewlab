# refactor/ — courses and tutorials

A temporary folder. It holds the plan, the inventory and the scripts for one
change: a tutorial stops declaring where it lives, and placement moves into
`courses/`. When the change is done and `DECISIONS_LOG.md` records it, this
folder is deleted in the same pull request.

Read in this order:

1. `PLAN.md` — what is decided, the target shape, and the steps in order with
   what "done" means for each.
2. `TOUCHPOINTS.md` — every place in this repository that reads a tutorial's
   module or series today, grouped by the step that changes it.
3. `EDITOR.md` — what changes in `assets/editor.js` here and in the dewnote
   repository, file by file.
4. `DOCS.md` — the `pages/` folder (what changes and what does not), and
   every document that describes today's layout, file by file.
5. `migrate_tutorials.py` — the one-shot migration. Dry-run by default; it
   prints what it would do and writes nothing until `--apply`.
6. `apply_docs.py` — the document swap: every edit in `DOCS.md` §2 as an
   exact old-to-new replacement. `--check` (the default) proves each old
   passage is still in the tree; `--apply` makes the edits, right after the
   migration, in the same commit.
7. `storage_migration.js` — the browser-side key migration the runtime gains
   in step 3, kept here so it can be read on its own.

Nothing in this folder is imported by `build.py` or shipped in `site/`.
