# `dev/*.py`, explained

The `dev/` folder holds standalone scripts a maintainer runs by hand (or
CI runs automatically) — none of them are part of the actual website
build. Each one is small enough to read on its own; this document is a
short map of what each does and why it exists, plus a couple of patterns
worth understanding once rather than four times.

---

## `dev/fetch_pyodide.py`

Downloads a **trimmed** copy of Pyodide — the core runtime plus only the
package wheels a given set of packages actually needs — into
`dev/pyodide/`. "Trimmed" matters: the full Pyodide distribution is
around 400 MB; this cuts that down to the roughly 32 MB the site's
baseline packages (`numpy`, `pandas`, `matplotlib`, `jedi`) actually need,
by reading Pyodide's own dependency lockfile and following it.

Read `resolve()` first if you haven't seen a breadth-first graph walk
before — it's a clean, small example: start with the packages asked for,
and keep pulling in whatever *those* depend on until nothing new is
left to add.

Three different things end up depending on this script: the end-to-end
tests (so they don't need a live CDN), the self-hosted-Pyodide escape
hatch for a school network that blocks the CDN, and `build.py`'s dewmini
bundle (with a wider package list, to make the downloadable Notebook work
completely offline).

## `dev/generate_doc_snippets.py`

Generates `assets/editor-doc-snippets.js` — real Python docstrings,
captured once and committed, for the small set of names the *authoring*
editor (where a maintainer writes tutorials, not where a student runs
code) might show a hover tooltip for. The reason this needs its own
script at all: the authoring editor never boots a real Pyodide (see
`ARCHITECTURE.md`), so unlike a student's cell — which can just ask a
live interpreter — there's no live Python here to ask.

The fix this script takes is to ask a *real* Pyodide, once, in a
disposable headless browser tab, and save the answer. `_collect()` is
worth reading slowly if the idea of code calling into other code across
languages is new: it's Python, calling `page.evaluate()` with a string of
real JavaScript, which itself contains a triple-backtick string of real
Python passed to `pyodide.runPython(...)` — three languages, nested.

## `dev/from_notebook.py`

Converts Jupyter notebooks into dewlab tutorial Markdown files — used
when content originates somewhere else (a course called "everlearning" is
mentioned in the script's own comments) and needs to become a real
dewlab tutorial. `convert()` is the heart of it: walk a notebook's cells
in document order, turn a Markdown cell into prose and a code cell into
an `exec` fence, and skip or flag anything this script genuinely can't
translate on its own (an IPython magic, a shell escape, a notebook
attachment) rather than guessing.

Read the module's own top docstring first — it's explicit about what this
script *won't* do (invent frontmatter it can't know, like which module
and series a converted tutorial belongs to) as much as what it will.

## `dev/curriculum_map.py`

Generates `planning/CURRICULUM_MAP.md` — a report showing exactly which
of the two QQI module descriptors' learning outcomes are actually taught,
where, and what's still missing. This is the most data-heavy of the four
scripts, but its shape is simple once you see it: `load_outcomes()` and
`load_tutorials()` read the source data, `coverage()`/`status_of()` work
out where each thing stands, and a series of small `*_table`/`*_graph`
functions each build one section of the final Markdown document, which
`render()` assembles in order.

The distinction the whole script cares about, stated plainly in its own
top docstring, is between **covering** an outcome (a section genuinely
teaches it) and **touching** it (a section merely uses it in passing) —
counting the second as the first would make the curriculum look more
complete than it actually is.

`--check` mode (what CI runs) doesn't write anything; it regenerates the
map in memory and fails if that doesn't match what's committed — the
same "generated file can't silently drift" idea CONTRIBUTING.md asks of
this whole repository's documentation, enforced automatically for this
one file.

---

## `dev/glossary_python.py`

Checks every glossary entry that names something in Python (a `python:`
field: `list.append`, `math.sin`, `elif`) against Python itself, and
writes `assets/python-signatures.json`, the signatures the reference
shows beside those entries. Three steps: `resolve()` turns a dotted name
into the real object (or a keyword), `example_problems()` binds each call
in the entry's example against that object's signature without running
anything, and `display()` formats the signature as Python gives it, type
hints and a method's `self` left out.

`--check` writes nothing and fails on a missing name, an example Python
would reject, or a stale signatures file. Signatures depend on the Python
version, so the file is written with the one Pyodide runs (3.13), and a
CI job on that version runs the check; under another version it checks
names and examples and says it skipped the signatures.

---

## `dev/label_report.py`

Called once, right after a report issue opens
(`.github/workflows/label-report.yml`), to apply the two labels the
issue form itself cannot: `.github/ISSUE_TEMPLATE/report.yml` can put a
fixed `source: page` on every report, but not a label whose *value*
depends on what the student actually typed — which page, which kind.
`parse_fields()` reads the issue body back out (GitHub renders every
form field as `### <label>\n\n<value>`, in field order — the one regex
at the top of the file, `FIELD_RE`, is built to read that shape
regardless of which fields a given report filled in), `kind_label()`
turns the free-text "what kind of thing is this?" answer into one of
three fixed labels, and `ensure_label()` creates a label the first time
anything needs it rather than requiring a maintainer to set one up by
hand in GitHub's settings first.

No `kind:` label exists for "a question, an idea, or something else" on
purpose — see the file's own docstring for why, and `DECISIONS_LOG.md`
8.4 for the fuller reasoning.

## `dev/report_patterns.py`

Runs weekly (`.github/workflows/report-patterns.yml`), reading every
open report issue and asking one question: does any single page, or any
single cell on a page, have enough open reports recently to be worth a
person looking at as a group rather than one at a time? `gather()`
groups issues by page (and, within a page, by cell, when the report
came from a cell's own report icon and so carries one), `worth_a_pattern()`
applies the threshold (three reports on a page, or two naming the same
cell, within the last fortnight), and `pattern_body()` writes the
issue text a human triager reads.

Idempotent by design: a hidden `<!-- pattern-key: <page> -->` marker in
the issue body is how a second run finds the pattern issue it already
opened for a page, rather than opening a duplicate — the body is
replaced wholesale each run, so an issue nobody has looked at yet still
reflects the current count, not the count from whenever it was first
opened. `.claude/skills/triage-report/SKILL.md`'s own "Working a
pattern issue" section is what a person (or an agent) actually does
with the result.

`parse_fields()` is deliberately the same regex as
`label_report.py`'s own, copied rather than imported from a shared
module — each script is meant to be readable and runnable on its own.
`tests/test_report_patterns.py`'s `test_label_report_uses_the_same_parser`
exists to catch the day the two copies quietly diverge, which is the
real risk that duplication carries.

## `dev/check_video_links.py`

Runs weekly (`.github/workflows/video-links.yml`) and asks YouTube about
every video linked from a page students read: every tutorial and
practice page, frozen releases included, and the site's own pages.
`links_by_video()` finds the links, whichever of YouTube's address forms
they use, `check()` sends each video's ID to YouTube's oEmbed endpoint
(the small request a site makes before embedding a video, which needs
no key), and `classify()` reads the answer: 200 is there, 400 or 404 is
gone, 401 or 403 is private or has embedding turned off. A timeout or a
5xx is retried, and never counts as gone, because a bad day on YouTube's
side is not a dead link.

It keeps one `video-link` issue the way `report_patterns.py` keeps its
`pattern` issues: a hidden `<!-- video-links -->` marker finds it again,
each run rewrites it with the current list, and it closes itself with a
comment once every video answers normally. A video that plays on
YouTube but has embedding turned off answers 401 for ever, so it goes
in `EMBEDDING_OFF` once someone has opened it and checked. Run by hand
without `--issue`, it prints the same report and exits 1 if anything
has gone. `tests/test_video_links.py` covers everything but the network.

---

## `dev/datasets.py`, `dev/daylight.py`, `dev/book_counts.py`

The datasets in `data/` (#324). `datasets.py` fetches the source of every
dataset with a `recipe:`, shapes it with the runtime's own
`tutorial_tools.shape_live()`, and says how far the snapshot has drifted,
row by row; `--refresh <name>` saves the source as the snapshot and moves
its `snapshot:` date to today. For a `live: true` dataset it also checks
the `Access-Control-Allow-Origin` header a browser needs. `daylight.py`
and `book_counts.py` make the two datasets whose sources are not files:
sunrise and sunset from NASA/JPL Horizons, and chapters and character
names counted from the novels in `data/`. See `docs/WRITING_TUTORIALS.md`
("Datasets") for when to run which.

---

## Not yet covered here

Six more scripts live in `dev/` — `check_doc_links.py`,
`apply_topic_edits.py`, `build_topic_editor.py`, `build_topic_game.py`,
`draw_topic_graph.py`, `pair_results.py` — that this file has never
covered. Not new drift; a gap that was already there, recorded honestly
rather than implied away by this file's title.

---

## A pattern shared by most of these: a script is a `main()`, guarded

Every one of these files ends with the same shape:

```python
def main() -> int:      # or -> None
    ...

if __name__ == "__main__":
    raise SystemExit(main())
```

`if __name__ == "__main__":` is a standard Python idiom: the code inside
it only runs when the file is executed directly (`python3
dev/whatever.py`), not when it's imported by something else (a test
file, say). Wrapping the real work in a `main()` function rather than
writing it directly at the bottom of the file is what makes that
possible — `main()` itself could still be imported and called from a test
without triggering `SystemExit`, since only the `if __name__ ==
"__main__":` line does that.
