# Versioning and Progress

## The problem

A student saves progress on Tutorial 3. A bug in one of its cells gets fixed and republished. The student comes back. What loads?

## Version metadata

Each tutorial's frontmatter carries a plain integer `version` field, incremented whenever executable-cell content changes — not for prose-only edits, which don't affect anything a student has already run or saved. The build script writes this into the generated page as a meta tag:

```html
<meta name="tutorial-version" content="2">
```

## What gets saved

The save format — student name, an array of cells with `task_id`, `student_code`, `output_html`, and so on, following the exam tool's original design — gains one new top-level field: the `tutorial-version` the page was showing when the student saved.

## What happens on load

The loader reads the current page's version and compares it to the version recorded in the saved file.

If they match, restore proceeds with no friction — silent, cell by cell via `task_id`.

If they don't match, restore still happens, but with a visible, non-blocking notice along the lines of "This progress was saved against an earlier version of this tutorial. Some cells may have changed." The matching logic doesn't change: it still goes by `task_id`, not array position, which is what lets it tolerate a cell being reordered or a new cell being inserted between versions without corrupting the restore. Two edge cases fall out of that: a saved cell whose `task_id` no longer exists in the current version gets dropped, noted in the restore summary rather than silently discarded; a current cell whose `task_id` wasn't in the saved file is left at its default starter content.

## Interactive widgets

A known limitation from the exam tool's load-JSON design carries over: widget cells restore their HTML snapshot but need a re-run to reinstantiate the live Python-side object behind them. Worth a one-line note in the restore summary so it doesn't read as broken.

## Save transport

Tutorials are confirmed ungraded — self-paced practice, not tied to a mark — which changes what this needs to protect against. Autosave to `localStorage` is the primary mechanism: progress persists across a closed tab or browser restart on the same device with no explicit action required. A manual "export to JSON" option stays available as a secondary path, for moving to another device or keeping an offline copy, but it's no longer the primary safety net the way it was in the exam tool's design — losing progress here is an inconvenience, not a lost grade. An optional GitHub Gist-sync layer (a PAT-authenticated "Save" button calling the Gists API directly from browser JS) can still sit on top of either path without changing any of the version-compare logic above — it only changes where the JSON blob lives between sessions.

A `check()` cell's pass/fail result is saved and restored the same way as any other cell's output — nothing new required in the save schema for it.
