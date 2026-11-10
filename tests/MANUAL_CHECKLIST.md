# Manual checklist

What the automated tests cannot reach. The unit tests cover the build and the
Python tools, and the browser tests drive one headless Chromium on the build
machine. Neither says anything about a student's own laptop, a school
network, a phone in a hand, or a screen reader.

So nothing here repeats a test. Running a cell, a traceback, saved work
coming back, a version change, a broken link stopping the build: those are
in `tests/`, and [`docs/tests-explained.md`](../docs/tests-explained.md) says
where. Run the sections that apply to what you changed, and all of it before
a release.

## Setup

```sh
pip install -r requirements-dev.txt
python3 build.py --clean
python3 -m http.server -d site 8000
```

Then open a built tutorial, for example
`http://localhost:8000/tutorials/first-steps.html`.
For the checks that need a real network or a real device, use the live site.

## Real machines and real networks

- [ ] **A school machine, on the school network.** Does Python load at all?
      Nothing else can answer it. If the CDN is blocked, the fix is
      `dev/fetch_pyodide.py`, which fetches a copy the site can serve itself.
- [ ] Time the first load on a school machine and on a home connection:
      roughly how long before the Run buttons enable?
- [ ] A second page load is markedly faster than the first.
- [ ] Safari and Firefox, not only Chrome: a page loads, a cell runs, Stop
      stops a `while True: pass`.
- [ ] On the live site, a page that loads a dataset shows its table, and a
      tutorial in a course folder finds its styles and scripts.

## Eyes and hands

- [ ] Every theme and every typeface in Settings is readable at the smallest
      and the largest text size, including the colours inside a code cell and
      a table in an output.
- [ ] A chart is legible at the page's own width, not clipped or blurred.
- [ ] Keyboard only, no mouse: you can reach every cell, run it, leave it
      again (Escape, then Tab), and open and close each panel.

## Before a release

### The offline bundle actually boots offline

The one check nothing in CI can do, because CI never builds the bundle with
a vendored Pyodide in it — and the one most likely to break silently, since
a bundle that quietly falls back to the CDN looks perfect on a machine with
a connection.

```sh
python3 dev/fetch_pyodide.py --out assets/vendor/pyodide \
    --packages numpy pandas matplotlib sqlite3 Pillow jedi pyodide-http
python3 build.py --clean
python3 -m http.server -d site/download/notebook 8200
```

Then, on a machine with the network off (or with everything but
`127.0.0.1` blocked), open `http://127.0.0.1:8200/` and:

- [ ] the page loads with no failed requests
- [ ] adding a Python cell and running `print(6 * 7)` prints `42`
- [ ] the Stop button interrupts a `while True: pass`
- [ ] a cell running `print("Hi " + input("Name? "))` shows a box after
      `Name? `; typing `Ada` and pressing Enter prints `Name? Ada` and
      `Hi Ada` (`assets/input-wait.js`)
- [ ] a text cell with `Solve $x^2 = 4$.` renders as real maths, with no
      failed request for `katex.bundle.js`, `katex.min.css`, or a font
      (the offline copy carries all three so a
      classroom with no network at all can still render maths, not just
      one with a slow one)

Last verified: 2026-08-30 — loaded and ran Python 3.13.2 with every
non-loopback request aborted, zero blocked requests recorded. The maths
line above was added after that verification and has not itself been
checked against a real offline bundle yet.

### A remote dataset actually loads

The one check the sandbox this was built in could not run at all: its
network policy blocks `ourworldindata.org`, so whether a browser is
allowed to fetch those CSVs was never observed, only expected.
Everything else about the Data catalogue —
the cards, the code it writes, the local datasets — is covered by
`tests/e2e/test_dewmini_workbench.py`; this is the half that needs a
real network.

On a machine with an ordinary connection, open the Notebook, open the
**Library** rail, and in **Data** pick one of the entries marked *from
the web*. Run the cell it adds.

- [ ] the table renders, or
- [ ] it fails with the CORS explanation from `load_csv()` — naming the
      other site's permission and pointing at Files — rather than a bare
      network error

Either outcome is a pass for the *code*; the second means the catalogue's
remote entries should be reconsidered, since a student should not be
offered a dataset that reliably fails.

Last verified: never.

### A phone

At 375px wide, on a tutorial and a practice page:

- [ ] nothing scrolls sideways (`tests/e2e/test_page_smoke.py` covers the
      known causes; this is for anything new)
- [ ] the launcher at the foot of the screen opens every panel, and each
      one closes again
- [ ] a cell's code is readable and editable without pinching

### A screen reader

Not covered by anything automated: a structural check (heading order,
landmark roles, alt text) can pass while the page is still confusing read
aloud, so this needs an actual screen reader, not a linter.

- [ ] a tutorial page reads in a sensible order from the top
- [ ] opening the Reference panel announces itself
- [ ] running a cell announces that output arrived
