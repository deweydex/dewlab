> **Superseded in part.** `VERSIONS.md` is the current behaviour: a student is
> pinned to the release they started, and the old one stays reachable, rather
> than restoring into a changed page with an apology notice as described
> below. The cell-id matching below is unchanged, and is what makes that
> pinning possible.

# Versioning and Progress

## The problem

A student saves progress on Tutorial 3. A bug in one of its cells gets fixed and republished. The student comes back. What loads?

## Version metadata

Each tutorial's frontmatter carries a plain integer `version` field, incremented whenever executable-cell content changes — not for prose-only edits, which don't affect anything a student has already run or saved. The build script writes this into the generated page as a meta tag:

```html
<meta name="tutorial-version" content="2">
```

## What gets saved

The save format — student name, and an array of cells each carrying `task_id`, `student_code`, `output_html` and so on — gains one new top-level field: the `tutorial-version` the page was showing when the student saved.

## What happens on load

The loader reads the current page's version and compares it to the version recorded in the saved file.

If they match, restore proceeds with no friction — silent, cell by cell via `task_id`.

If they don't match, restore still happens, with a visible, non-blocking notice along the lines of "This progress was saved against an earlier version of this tutorial. Some cells may have changed." Matching still goes by `task_id`, not array position, so a cell being reordered or a new cell being inserted between versions doesn't corrupt the restore. Two edge cases follow: a saved cell whose `task_id` no longer exists gets dropped, noted in the restore summary; a current cell whose `task_id` wasn't in the saved file is left at its default starter content.

## Interactive widgets

One limitation is worth stating plainly rather than discovering: a widget cell restores its saved HTML, but the live Python object behind it does not come back until the cell is re-run. Worth a one-line note in the restore summary so it doesn't read as broken.

## Save transport

Tutorials are ungraded — self-paced practice, not tied to a mark — so losing progress is an inconvenience, not a lost grade. Autosave to `localStorage` is the primary mechanism: progress persists across a closed tab or browser restart on the same device, with no action required. A manual "export to JSON" option is a secondary path, for moving to another device or keeping an offline copy. An optional GitHub Gist-sync layer (a PAT-authenticated "Save" button calling the Gists API from browser JS) could sit on top of either path without changing the version-compare logic above — it would only change where the JSON blob lives between sessions.

A `check()` cell's pass/fail result is saved and restored the same way as any other cell's output — nothing new required in the save schema for it.
