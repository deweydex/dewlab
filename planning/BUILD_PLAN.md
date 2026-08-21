# Build Plan

Five phases, each depending on the one before it. Nothing in a later phase should require reopening an earlier one.

## Phase 0 — Foundations

Stand up the repo skeleton described in REPO_AND_EDITOR.md, including the per-module subfolder structure under `/tutorials/`. Build the shell HTML template every generated tutorial will use, referencing the shared `/assets/` CSS and JS rather than inlining them. Confirm `pyodide.loadPackage(['numpy', 'pandas', 'matplotlib'])` loads cleanly against that shell with no micropip step involved, and that a plain `exec` cell running numpy/pandas/matplotlib code renders its output beneath it correctly — worth checking against whatever Pyodide version this ends up targeting, since package availability shifts between releases. Build tutorial_tools.py's DOM-bridge widget functions (text_input, dropdown, button, show, show_table, check) against the specification in DECISIONS.md after that core execution path is confirmed, not before — the widget bridge is a bonus layer, not a precondition for the plain execution path working.

## Phase 1 — Build script v1

Write the markdown-to-HTML converter: parse frontmatter and body, convert exec-tagged fences into cell objects, expand include directives into their referenced setup code, resolve cross-tutorial links to relative hrefs and warn on anything that doesn't resolve, then render the result into the shell template. Test this against one hand-written sample tutorial, start to finish, before touching real content.

## Phase 2 — Save, load, and versioning

Build the save/load JSON logic in tutorial_tools' runtime against the schema in VERSIONING_AND_PROGRESS.md. Add the version metadata and the compare-on-load logic from that same document. Test the mismatch path deliberately — bump a tutorial's version number on purpose and confirm the restore still works and the notice appears, rather than only testing the happy path where nothing has changed.

## Phase 3 — Navigation shell

Build the series-level table of contents page and the prev/next header shared across every generated tutorial.

## Phase 4 — Hosting

Write the GitHub Actions workflow that runs the build script on push to main and deploys to Pages. Confirm the relative data-file fetches work against the live Pages URL, not just a local server — path resolution is one of the more common places hosted-vs-local behavior diverges.

## Phase 5 — Pilot

Convert two or three real tutorials end to end before converting the whole series. Get them in front of students, or at minimum dry-run them on a machine that isn't the development machine, before committing to converting everything that already exists as a static tutorial.
