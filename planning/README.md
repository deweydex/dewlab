# dewlab — Planning Packet

Prep material for the next build session. Five documents, each answering one question. Read DECISIONS.md first — everything else expands on entries in that log.

## Contents

- **DECISIONS.md** — every settled decision (libraries, style, hosting, versioning, editor, math rendering) with the reasoning behind it, plus a short list of things assumed rather than settled.
- **BUILD_PLAN.md** — the build in dependency order, five phases, ending in a pilot before converting the full series.
- **CONTENT_AND_FILE_ARCHITECTURE.md** — the markdown source format, the cell/layout pattern, and how a tutorial references data, shared setup code, or another tutorial.
- **VERSIONING_AND_PROGRESS.md** — what happens to a student's saved progress when a tutorial gets edited after they've started it.
- **REPO_AND_EDITOR.md** — the GitHub repo layout, the Pages deploy setup, and what the editor is for v1.

## Where this started

An earlier exam tool (hvit_exam.html) proved out the hard problems conceptually — Pyodide loading, CodeMirror cells, save/load JSON — but that file, and its widget-bridge module, no longer exist. This packet rebuilds that functionality from the specification the exam tool left behind, rather than porting working code, and changes two structural things given dewlab's own constraints (no sqlite, hosted rather than double-clicked, a series rather than one file): assets move from fully inlined to shared-and-hosted, and saved state gets a version number so it survives edits.

## Scope, confirmed

Not tied to any single course. Two authors, both comfortable with git. Year-one modules: Computational Methods, Mathematics for IT, Programming and Design Principles, Database Methods, plus a pilot in a colleague's Foundations of Object-Oriented Programming LV5. `module` and `year` are editable frontmatter fields rather than a fixed list, so a new module later is a new value and a new folder, not an architecture change. OPEN_QUESTIONS.md tracks what's still unresolved — aesthetics chief among what's left.
