# Content and file architecture

## Markdown source format

Each tutorial is one Markdown file: YAML frontmatter, then prose
interleaved with tagged code fences.

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

`module` and `year` are free text, not drawn from a fixed list — a new
module is a new value here and a new subfolder under `tutorials/`.
`order` and `series` build the table of contents and prev/next links.
`version` holds the dated release identifier `VERSIONS.md` defines
(`2026.09.15.1`), not a plain integer — every release, current or
archived, carries its own. Other fields, like `dataset`, are added only
when a tutorial actually needs them.

## Cell types

A plain fenced code block renders as read-only illustrative code — no
cell, no Run button. A fence tagged `exec` becomes an executable cell,
with a stable id on its first line:

    ```python exec
    id: filter-example-1
    df[df["life_expectancy"] > 75]
    ```

That `id` is the key a student's saved answer is matched back to —
never the cell's position on the page.

A cell can call `check(actual, expected)` from `tutorial_tools.py` for
formative self-checking — a pass/fail indicator in the output area,
nothing scored or recorded. No separate fence tag: a check is just an
`exec` cell whose code happens to call `check()`.

An exec cell can carry an optional `hint:` field alongside `id:`:

    ```python exec
    id: filter-example-1
    hint: Try filtering on the life_expectancy column first
    df[df["life_expectancy"] > 75]
    ```

`hint` is plain author-written text behind a toggled "?" icon in the
cell's control bar. Not code, no effect on execution or the save
schema.

A tutorial with no `exec` cells — pure prose, or prose plus math with
nothing runnable — uses this same format; `exec` is what makes a cell
executable, and a tutorial simply doesn't need one. Math renders via
KaTeX wherever it appears, in the editor's live view and the built page
alike.

## Shared setup code

Boilerplate several tutorials need lives once in `/setup/` and is
pulled in with an include directive:

    ```python exec
    id: setup
    {{include: setup/load_life_expectancy.py}}
    ```

`build.py` expands this at build time. Each tutorial page is still its
own independent Pyodide instance with no kernel carried over from one
page to the next, so the expanded cell re-executes on every load.

## Shared data files

Datasets live once, in `/data/`, fetched at runtime by whichever
tutorial's setup cell needs them — never copied per tutorial.

## Cross-tutorial links

`[see Tutorial 2](tutorial:filtering-sorting#example-1)` resolves to a
real relative href at build time. A reference to a slug or anchor that
doesn't exist fails the build.

## Visual pattern

Every tutorial repeats the same shape: a prose block, then an
executable cell, then its output area directly beneath it.
