# Contracts this project can't break

Once a student saves progress in their own browser, the shape of that
saved data is a promise. Breaking any of these means writing a
migration for every browser already holding old data, or accepting
that some students lose work.

- **Storage keys are scoped to `(module, slug)`, never `slug` alone.**
  A slug is only unique within its own module — `first-steps` exists in
  both `computational-methods` and `mit-pdp-maths-prog-integration`.
- **A cell id is lowercase letters, digits, and hyphens**
  (`section-slug-n`), unique within its own tutorial, not globally. The
  authoring editor warns before a cell-id change ships on an already-live
  tutorial — the one way this could quietly break.
- **An exported progress file carries its own `tutorial-module` and
  `tutorial-slug`**, and the importer refuses a mismatched file before
  writing anything to storage.
- **Version comparison stringifies both sides first** — safe with the
  dated release format (`YYYY.MM.DD.N`) `VERSIONS.md` defines.
