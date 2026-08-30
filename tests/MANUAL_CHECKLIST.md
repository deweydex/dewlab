# Manual checklist

What the automated tests can't reach. The unit tests cover the pure logic and
the e2e test drives one headless Chromium on the build machine; neither says
anything about how this behaves on a student's actual laptop, on a school
network, or under a screen reader.

Every section below is live — the build phases this was originally written
against are all shipped (`planning/BUILD_PLAN.md`). Run what applies to what
you changed, and run "Before a release" in full before publishing one.

## Setup

```sh
pip install -r requirements-build.txt
python3 dev/fetch_pyodide.py        # once, ~32 MB, for the e2e tests
python3 build.py --clean
python3 -m http.server -d site 8000
```

Then open a built tutorial, for example
`http://localhost:8000/tutorials/computational-methods/first-steps.html`.

Note that this serves the tutorials as a reader would meet them, which is the
point of checking by hand: everything below is about what actually happens on a
machine that is not the one this was built on.

## Phase 0 — foundations

### On the development machine

- [ ] The page renders before Python has finished loading — prose is readable,
      cells are visible, the Run buttons are visibly disabled rather than
      looking broken.
- [ ] The status bar says what it is doing (starting Python, loading packages)
      and disappears when ready.
- [ ] Every cell runs, and its output lands beneath that cell and no other.
- [ ] The matplotlib figure is legible at the page's own width, not clipped or
      pixelated.
- [ ] A deliberately broken cell shows a traceback pointing at the line you
      broke.
- [ ] Ctrl-Enter (Cmd-Enter on a Mac) runs the focused cell.
- [ ] "reset" restores the author's starter code and clears the output.
- [ ] Tab indents inside a cell; Escape then Tab moves focus out of it.

### Texture panel

- [ ] All three themes look right, including the syntax colours in a code cell
      and the tables in an output area.
- [ ] All three fonts are readable at the smallest and largest text size.
- [ ] Choices survive a reload, and survive navigating to another tutorial.
- [ ] With the browser set to dark and the panel set to auto, the page is dark.

### Hardware and environment — the part that needs real machines

- [ ] **A school machine, on the school network.** Does Pyodide load at all?
      This is OPEN_QUESTIONS.md 32 and nothing else can answer it. If the CDN
      is blocked, the fix is `dev/fetch_pyodide.py` plus decision 0.17 in
      DECISIONS_LOG.md.
- [ ] Time the first load on a school machine and on a home connection. Roughly
      how long before the Run buttons enable?
- [ ] A second page load — the browser cache should make it markedly faster.
- [ ] **A phone.** Does the layout hold? Can a cell be edited at all? (Not a
      supported use, but worth knowing what happens.)
- [ ] Safari and Firefox, not just Chrome.
- [ ] Keyboard only, no mouse: can you reach every cell, run it, and open the
      texture panel?
- [ ] A screen reader on the status bar and on a check() verdict.

## Phase 1 — build script

- [ ] A tutorial with no `exec` cells at all builds and opens, and never loads
      Pyodide.
- [ ] A broken cross-tutorial link fails the build loudly rather than shipping.

## Phase 2 — save, load, versioning

- [ ] Bump a tutorial's `version` by hand, reload with saved progress present,
      and confirm the notice appears and the restore still works.
- [ ] Delete a cell whose id is in the saved file; confirm it is reported in the
      restore summary rather than silently dropped.
- [ ] Close the browser entirely, reopen, confirm autosaved work is still there.

## Phase 4 — hosting

- [ ] Data-file fetches work against the live Pages URL, not just localhost.
- [ ] Assets resolve from a tutorial nested in a module subfolder, not only from
      the site root.

---

## Before a release

### The offline bundle actually boots offline

The one check nothing in CI can do, because CI never builds the bundle with
a vendored Pyodide in it — and the one most likely to break silently, since
a bundle that quietly falls back to the CDN looks perfect on a machine with
a connection.

```sh
python3 dev/fetch_pyodide.py --out assets/vendor/pyodide \
    --packages numpy pandas matplotlib sqlite3 Pillow jedi
python3 build.py --clean
python3 -m http.server -d site/download/dewmini 8200
```

Then, on a machine with the network off (or with everything but
`127.0.0.1` blocked), open `http://127.0.0.1:8200/` and:

- [ ] the page loads with no failed requests
- [ ] adding a Python cell and running `print(6 * 7)` prints `42`
- [ ] the Stop button interrupts a `while True: pass`

Last verified: 2026-08-30 — loaded and ran Python 3.13.2 with every
non-loopback request aborted, zero blocked requests recorded.
`planning/EDGES_AUDIT.md` §1.

### A phone

At 375px wide, on a tutorial and a practice page:

- [ ] nothing scrolls sideways (`tests/e2e/test_narrow_screen.py` covers the
      two known causes; this is for anything new)
- [ ] the Reference, Series and Settings panels open as bottom sheets
- [ ] a cell's code is readable and editable without pinching

### A screen reader

Not covered by anything automated — `planning/EDGES_AUDIT.md` §3 explains
what the structural checks do and do not tell you.

- [ ] a tutorial page reads in a sensible order from the top
- [ ] opening the Reference panel announces itself
- [ ] running a cell announces that output arrived
