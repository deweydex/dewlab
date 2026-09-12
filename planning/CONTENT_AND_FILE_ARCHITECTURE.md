# Content and File Architecture

## Markdown source format

Each tutorial is one markdown file with YAML frontmatter and a body of ordinary prose interleaved with tagged code fences.

Frontmatter example:

```yaml
---
title: "Loops and Accumulation"
slug: loops-accumulation
module: computational-methods
year: "2026-2027"
series: python-fundamentals
order: 3
version: 1
---
```

`version` is the field VERSIONING_AND_PROGRESS.md compares against saved student progress. `order` and `series` are what the navigation shell (Build Plan, Phase 3) uses to build the table of contents and prev/next links. `module` and `year` are free text/slug fields, not drawn from any fixed list: a tutorial declares which module and year it belongs to, and that's what organizes the `/tutorials/` folder (see REPO_AND_EDITOR.md) and any per-module filtering in the navigation shell. `year` is an academic-year string like `2026-2027`, not a plain integer, since the program is scoped one year at a time. The build script doesn't enumerate or validate against a known set of modules — a new module is just a new value in this field and a new subfolder. Other fields, like `dataset`, are illustrative rather than fixed: a data-focused tutorial adds it, a tutorial with no data doesn't.

## Cell types

Ordinary fenced code blocks render as read-only illustrative code, exactly as markdown normally handles them — no cell, no Run button. A fence tagged `exec` becomes an executable cell, with a stable id on its first line:

    ```python exec
    id: filter-example-1
    df[df["life_expectancy"] > 75]
    ```

That `id` is what the version-compare logic in VERSIONING_AND_PROGRESS.md matches against, rather than the cell's position on the page.

Some cells give students a self-check against a correct answer, using a `check(actual, expected)` function from tutorial_tools.py — the same kind of tutorial-facing function as `show` or `show_table`, called from within the cell's own code, rendering a pass/fail indicator in the output area. This is formative feedback only: nothing is scored or recorded, and it's unrelated to any grade. No new fence tag or cell type is needed — a check is just an `exec` cell whose code happens to call `check()`.

An exec cell can also carry an optional `hint:` field in its header, alongside `id:`:

    ```python exec
    id: filter-example-1
    hint: Try filtering on the life_expectancy column first
    df[df["life_expectancy"] > 75]
    ```

`hint` is plain author-written text, shown via a small "?" icon in the cell's control bar — click it to open, click again to close (a toggle rather than a hover popover; see DECISIONS_LOG.md 7.67). Not code, not evaluated, no effect on execution or the save schema. Omit it and the cell just has no hint.

A tutorial with no `exec` cells at all — pure prose, or prose plus math notation with no runnable code — is a fully valid file in this same format, not a special case. It uses the same frontmatter, the same shell template, the same navigation as any other tutorial; the `exec` tag is what makes a cell executable, and a tutorial simply doesn't need one. Math notation renders via KaTeX, in both the GUI editor's live view and the built page (see DECISIONS.md), and doesn't change anything else about the frontmatter or cell structure.

## Shared setup code

Boilerplate several tutorials need — loading the same dataset into a DataFrame, for instance — lives once in a `/setup/` folder and gets pulled in with an include directive:

    ```python exec
    id: setup
    {{include: setup/load_life_expectancy.py}}
    ```

The build script expands this at build time, so the source stays free of duplicated boilerplate. The include mechanism de-duplicates the source, not the runtime: each tutorial page is still its own independent Pyodide instance with no kernel carried over from one tutorial to the next, so the expanded setup cell re-executes on every page load.

## Shared data files

Datasets live once, in `/data/`, and are fetched at runtime by whichever tutorial's setup cell needs them — never embedded or copied per tutorial. Everything is hosted on the same GitHub Pages origin, so a relative fetch (`pyodide.http.pyfetch('../data/life-expectancy.csv')`, written into Pyodide's virtual filesystem, then read with `pd.read_csv`) works without CORS complications — hosting rather than double-clicking a file makes this possible.

## Cross-tutorial links

A recognized link syntax in the markdown — `[see Tutorial 2](tutorial:filtering-sorting#example-1)` — gets resolved by the build script into a real relative href pointing at the generated page and anchor. The build script also acts as a link checker: a reference to a slug or anchor that doesn't exist among the tutorials it just built fails the build, rather than shipping a dead link.

## Visual pattern

Every tutorial follows the same repeating shape: a prose block explaining a concept, followed by an executable cell with its output area directly beneath it. That consistency is what makes the tool read as one coherent thing rather than a folder of one-off pages that happen to share a colour scheme.
