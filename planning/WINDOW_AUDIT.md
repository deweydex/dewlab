# A pre-release check of what this project can't take back

A review of the storage schemas, slug scoping, cell-id conventions, and
version comparisons dewlab depends on — done once, before public cohorts
started saving real work, because these are the things that become hard
to change the moment a real student has saved something against them.

---

## Why this mattered

Once a student saves progress in their own browser, the shape of that
saved data becomes a promise. Changing a storage key, a cell id
convention, or how a saved record is structured after that point means
either writing a migration for every browser that already has old data
in it, or accepting that some students lose their work.

This review checked four of those promises across all 20 tutorials
published at the time (228 runnable cells) before launch. It found two
real scoping problems and fixed both.

---

## What was checked, and what was found

### 1. Tutorial slugs and storage scoping
- **The promise**: a URL path and a `localStorage` key both uniquely
  identify one tutorial.
- **What was actually true**: a slug is only unique *within* a module,
  not across the whole site — `first-steps` exists in both
  `computational-methods` and `mit-pdp-maths-prog-integration`. Storage
  keys originally used `dewlab:progress:<slug>` alone, so two modules'
  `first-steps` shared one key, and saving work in one silently
  overwrote the other.
- **Fixed by**: scoping every progress key to the `(module, slug)` pair
  instead — `dewlab:progress:<module>:<slug>` — with `module` now
  carried explicitly in every page's manifest.

### 2. Cell id conventions
- **The promise**: a cell's id (`task_id`) is what matches a student's
  saved code and output back to the right cell, between the tutorial's
  Markdown source and what's in local storage.
- **What was checked**: all 228 executable cells across the curriculum.
  - Every one uses lowercase letters, digits, and hyphens
    (`section-slug-n`) — no exceptions.
  - Lengths ranged from 5 to 48 characters, averaging 18.
  - 12 fairly generic ids (like `your-turn-1`) turn up in more than one
    tutorial — safe, since storage is already scoped per `(module,
    slug)` pair, so the same id in two different tutorials never
    collides.
- **Conclusion**: sound as-is. The authoring editor already warns an
  author if they change a cell id in a tutorial that's already live,
  which is the one way this contract could quietly break later.

### 3. The exported-save-file format
- **The promise**: an exported progress file is JSON shaped like
  `{tutorial-slug, tutorial-module, tutorial-version, saved_at,
  cells[]}`.
- **What was actually true**: importing a file used to write its
  contents straight into the current tutorial's storage key before
  checking whether the file's cells actually matched — so loading the
  wrong file could silently destroy real, unrelated saved work.
- **Fixed by**:
  - Every exported file now carries its own `tutorial-module` and
    `tutorial-slug`.
  - Its filename includes the module too (`<module>-<slug>-progress.json`),
    so two files aren't indistinguishable in a downloads folder.
  - The importer checks the module and slug match *before* writing
    anything, and refuses a mismatched file outright rather than
    touching storage at all.

### 4. Comparing version strings
- **The promise**: restoring saved work compares the version it was
  saved against with the tutorial's current version correctly.
- **What was checked**: the actual comparison
  (`String(record["tutorial-version"]) !== String(currentManifest.version)`)
  stringifies both sides first.
- **Conclusion**: works correctly with the dated version format
  (`YYYY.MM.DD.N`) this project actually uses.

---

## Summary

| What was checked | Result | How it's kept true |
|---|---|---|
| Slugs scoped per module | Fixed | `tests/test_tutorial_tools.py` |
| Cell id conventions | Already sound | A crawl of every tutorial's Markdown and code blocks |
| Import validation | Fixed | Tests that a mismatched file is rejected |
| Version comparison | Already sound | Tests on string equality during restore |
