# Contributing code to dewlab

Thanks for your interest in contributing to dewlap! This page is about what you need to know before recommending changes and additions to the site's own code — the
build, the runtime, and the editor, dewmini. It covers getting
set up, what to run before you open a pull request, and the one standing
requirement this repository has: that documentation and comments stay accurate
as the code changes.

If you are here for something else, one of these is a better door:

- Writing or editing a tutorial → [`docs/WRITING_TUTORIALS.md`](docs/WRITING_TUTORIALS.md)
- Reporting a bug or a mistake → [`docs/REPORTING_A_PROBLEM.md`](docs/REPORTING_A_PROBLEM.md)
- Understanding how the code fits together → [`ARCHITECTURE.md`](ARCHITECTURE.md)

---

## Getting set up

You need Python 3.12 or later. Node is only needed if you are changing a
vendored library, which is covered further down.

```sh
git clone https://github.com/deweydex/dewlab
cd dewlab
pip install -r requirements-build.txt
python3 build.py --clean
python3 -m http.server -d site 8000
```

That builds the whole site into `site/` and serves it at
`http://localhost:8000`. `site/` is never committed — it is regenerated on every
push, which is what keeps a published page from drifting from the markdown it
came from.

The downloadable single-file copies are the slow part of a build, so
`python3 build.py --no-standalone` skips them while you are iterating. Build
without that flag at least once before you open a pull request, since the
download path has its own failure modes.

---

## Running the tests

```sh
python3 -m pytest                      # everything
python3 -m pytest --ignore=tests/e2e   # the fast ones, no browser
```

The unit tests need nothing but Python. The end-to-end tests drive a real
browser against a real Python runtime, so they need a local copy of that runtime
first — `python3 dev/fetch_pyodide.py`, about 30 MB. Without it they skip with a
message rather than failing.

There is also [`tests/MANUAL_CHECKLIST.md`](tests/MANUAL_CHECKLIST.md) for the
things a browser test does not cover well.

---

## What runs in CI

Three workflows run on every push.

`tests` runs the unit suite, builds the site, and fails if
`planning/CURRICULUM_MAP.md` is out of date relative to the curriculum data and
the tutorials' own `covers:` frontmatter.

`standalone-bundle-is-current` rebuilds the vendored CodeMirror/KaTeX bundle
from `vendor-src/` and fails on any difference. The bundle is committed on
purpose, so that neither the build nor an author previewing locally needs a Node
toolchain — which also means it can go stale the moment anyone edits the
runtime. If you change a pinned version in `vendor-src/package.json`, rebuild
with `npm install && npm run build` inside `vendor-src/` and commit the result.

`publish` (`.github/workflows/deploy.yml`) builds the site and deploys it to
GitHub Pages on a push to `main`.

---

## Keep documentation and comments current

This is not cleanup for later. A change that adds a feature, or changes how one
works, is not finished until the documentation and comments describe the new
behaviour rather than the old one.

**Update the document that describes it.** If you change what a page does,
update the document a reader would reach for — `docs/FOR_STUDENTS.md`,
`docs/DEWMINI.md`. If you change how the code works, update
the matching `docs/<name>-explained.md`, and `README.md` or `ARCHITECTURE.md` if
they mention it.

**Comment every function you touch or add**, not only the ones with tricky
logic. A comment should say what the function does and, where it is not obvious,
why — written so that someone learning to program could follow it, not only
someone who already knows this codebase.

**Never leave a comment or document describing behaviour that no longer
exists.** A stale comment is worse than no comment, because it misleads the next
person to read it. If you are not sure whether a comment is still accurate,
check it against the code before you leave it alone.

### Explanation files

Every substantial code file has a matching file in `docs/` named
`<file>-explained.md` — `compose/dewmini.js` has `docs/dewmini-js-explained.md`,
and so on. These walk through how the file is put together: what its main pieces
are, how they call each other, and why it is organised the way it is. They are
for someone reading the code for the first time. They are not a changelog and
not an API reference; the inline comments already cover the details of any one
function.

If you add a file substantial enough to need its own inline comments, give it an
explanation file too. If you restructure an existing file, update its
explanation file to match — a walkthrough describing a structure the code no
longer has is worse than confusing.

### Who reads what

**Student-facing pages** (`docs/FOR_STUDENTS.md`,
`docs/DEWMINI.md`, the homepage, in-app help text): plain, friendly, welcoming
language, written for a teenage student. No jargon without explaining it, no
metaphor for its own sake. If you would not say it that way to a fifteen-year-old
sitting next to you, rewrite it.

**Contributor and maintainer documentation** (`README.md`, `ARCHITECTURE.md`,
`docs/WRITING_TUTORIALS.md`, `planning/*.md`): plain and direct in the same way,
but addressed to the reader who is there — a teacher deciding whether to build a
course in dewlab, or a developer changing the code. Do not rewrite these to
address a student; that is not who reads them, and it would make them harder to
use for the people who do.

**`DECISIONS_LOG.md`**: a record of engineering decisions, each dated and
numbered. Keep entries accurate and readable, but do not simplify away real
information for the sake of a friendlier tone. Its job is precision.

---

## Before you open a pull request

- Run `python3 -m pytest` (skip `tests/e2e` unless you are testing browser
  behaviour directly), `ruff check` on any Python you touched, and
  `python3 build.py` to confirm the site still builds.
- Read back the documentation and comments you touched as if you had never seen
  this codebase. If something needs reading twice to make sense, it needs
  another pass.
- Record a decision somebody could reasonably have made differently as a new
  numbered entry in [`DECISIONS_LOG.md`](DECISIONS_LOG.md), with what it would
  cost to change your mind later. [`QUESTIONS.md`](QUESTIONS.md) is where
  anything still waiting on a decision belongs.
- If you are unsure whether a change needs a new explanation file or an update to
  an existing one, write it. A missing explanation costs the next person more
  time than a redundant one.

---

## If this page is wrong

If something here does not match what you find in the code, the code is more
likely to be right and this page more likely to be stale — but say so anyway, so
it can be fixed. Open an issue, or fix it yourself and mention the mismatch in
your pull request.
