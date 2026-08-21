# dewlab

Interactive Python tutorials for programming and maths FE modules. A tutorial
is a markdown file; the build turns it into a page where prose, live code cells
and their output alternate, and the Python runs in the student's own browser
via Pyodide — nothing to install, nothing submitted anywhere.

Status: **Phase 0 complete.** The execution path works end to end. `build.py`
(Phase 1) does not exist yet, so there are no real tutorials in `tutorials/`.

## Layout

```text
tutorials/            one subfolder per module, matching the `module` frontmatter slug
  computational-methods/
  mathematics-for-it/
  programming-design-principles/
  database-methods/
setup/                shared setup snippets, pulled in with {{include: ...}}
data/                 shared CSV datasets, fetched at runtime
assets/
  shell.html          the template every generated page is rendered into
  tutorial-style.css  the house style and the texture panel's variables
  tutorial-runtime.js boots Pyodide, mounts the editors, runs a cell
  tutorial_tools.py   what a student's cell code sees
  vendor/             CodeMirror and KaTeX, built from vendor-src/
vendor-src/           pinned dependencies and the esbuild script for assets/vendor/
dev/                  Phase 0 scaffolding, replaced by build.py
tests/                unit tests, e2e tests, and the manual checklist
```

Generated HTML is not committed. It is a build artifact, produced on push and
deployed straight to Pages, so markdown source and published output cannot
drift apart.

## Running it now

```sh
python3 dev/make_harness.py
python3 -m http.server -d dev/harness 8000
```

Then open `http://localhost:8000`. The harness page is a fixed set of cells
chosen to exercise every branch of the output renderer — printed text, a last
expression, a DataFrame, a figure, a traceback, and each widget. It is a test
fixture, not a preview tool; `build.py` replaces it in Phase 1.

## Tests

```sh
python3 -m pytest tests/test_tutorial_tools.py    # fast, no browser
python3 dev/fetch_pyodide.py                      # once, ~30 MB
python3 -m pytest tests/e2e                       # real Chromium, real Pyodide
```

The fast tests cover the pure logic — `check`'s comparison rules, output
markup, escaping, traceback trimming — by importing `tutorial_tools` under
CPython with a recording stub in place of the DOM. The e2e test drives the
golden path in a browser, because that is the only thing that can say the
execution path really works. `tests/MANUAL_CHECKLIST.md` covers what neither
can reach: school machines, school networks, other browsers, assistive tech.

## Rebuilding assets/vendor/

Only needed when a pin in `vendor-src/package.json` changes.

```sh
cd vendor-src && npm install && npm run build
```

## Where the decisions live

- `planning/DECISIONS.md` and the rest of the planning packet — the settled
  decisions, and the source of truth.
- `DECISIONS_LOG.md` — everything decided during the build that the packet
  does not settle, with the reasoning and the cost of changing it.
