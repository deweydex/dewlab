# Repository and Editor

## Repo layout

```
/tutorials/
    computational-methods/     one subfolder per module
    mathematics-for-it/
    programming-design-principles/
    database-methods/
/setup/                    shared setup snippets, pulled in via {{include:}}
/data/                     shared CSV datasets
/assets/
    tutorial-style.css
    tutorial-runtime.js
    tutorial_tools.py
build.py
.github/workflows/deploy.yml
```

Subfolders under `/tutorials/` are one per module, named by the same slug that goes in a tutorial's `module` frontmatter field (see CONTENT_AND_FILE_ARCHITECTURE.md). A new module is a new folder — nothing in `build.py` needs to know the set of modules in advance. The four above are the confirmed year-one set; a `foundations-oop-lv5` folder will likely join as a pilot for a colleague's module.

Generated HTML doesn't live in the repo as committed files — it's a build artifact, produced fresh on every push and deployed straight to Pages. That avoids the failure mode where a tutorial's markdown gets edited, the rebuild is forgotten, and source and output ship out of sync.

## Deployment

A GitHub Actions workflow triggered on push to main: checks out the repo, runs `build.py`, and deploys the result to GitHub Pages via the standard Pages deploy action. The workflow becomes edit markdown, commit, push — build and deploy happen without a manual step to remember. Worth noting this differs slightly from how Web Authoring students use Pages, where they push already-built static files directly; here the repo holds source, and Pages serves something Actions built from it.

## The editor, v1

A local GUI built on Milkdown (Crepe preset) — the same live, borderless block-editing pattern already in use in Josh's other markdown-authoring projects — not a CLI-only workflow. Two people will be authoring tutorials, both comfortable with git, and both prefer working visually: open a folder, see the tutorials already there, create a new one, add and reorder cells, rather than hand-editing YAML frontmatter and fenced code blocks directly in a text editor.

The GUI operates on the same markdown files CONTENT_AND_FILE_ARCHITECTURE.md specifies — a front end onto `/tutorials/`, not a separate storage format. Concretely: a folder view listing existing tutorials grouped by module subfolder, and a per-file editor where prose and math render live as you type (Crepe's native behavior — no separate preview pane needed for that half), with `exec` cells as distinct blocks you can add, reorder, or delete, each one a CodeMirror instance with syntax highlighting. Frontmatter (title, slug, module, year, series, order, version) is exposed as form fields rather than raw YAML. Saving writes plain markdown back to disk, so a file edited through the GUI and one edited by hand afterward stay interchangeable — nothing about the underlying format is GUI-specific.

`build.py` is unaffected. It's still the script from BUILD_PLAN.md Phase 1 that converts `/tutorials/` markdown into the hosted HTML series, and it's still what runs inside the GitHub Actions workflow on push. The GUI sits in front of authoring; the build step behind it is unchanged.

The one thing Crepe's live rendering doesn't reach is a cell's actual Python output. Previewing that still means running `build.py` and opening the result in a browser tab, rather than a live Pyodide pane inside the editor. That richer version is deliberately deferred until it's clear the build-then-open loop is too slow to work with day to day.
