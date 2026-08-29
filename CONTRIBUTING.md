# Contributing to dewlab

Thanks for wanting to help. This page covers two things every change to
this repository should do: keep the documentation accurate, and keep the
code readable by someone who is still learning to program. Everything
else about contributing — how tutorials are structured, how the build
works, how to run tests — is in [`README.md`](README.md) and
[`ARCHITECTURE.md`](ARCHITECTURE.md).

---

## 1. Keep documentation and comments current

This is not optional cleanup for later. A change that adds a feature, or
changes how one works, is not finished until the documentation and
comments describe the new behavior — not the old one.

### When you change code

- **Update the doc that describes it.** If you change what a page does,
  update the page in `docs/` that a student would read (e.g.
  `docs/MINI_IDE.md`, `docs/DEWMINI.md`). If you change how the code
  itself works, update the matching `docs/<name>-explained.md` file (see
  below) and `README.md`/`ARCHITECTURE.md` if they mention it.
- **Comment every function you touch or add**, not just the ones with
  tricky logic. A comment should say what the function does and, where
  it isn't obvious, why — written so someone learning to program could
  follow it, not just someone who already knows this codebase.
- **Never leave a comment or doc describing behavior that no longer
  exists.** A stale comment is worse than no comment — it actively
  misleads the next person to read it. If you're not sure whether a
  comment is still accurate, check it against the code before you leave
  it alone.

### Explanation files

Every substantial code file has a matching file in `docs/` named
`<file>-explained.md` — for example, `assets/mini-ide.js` has
`docs/mini-ide-js-explained.md`. These walk through how the file is put
together: what its main pieces are, how they call each other, and why
it's organized the way it is. They're for someone reading the code for
the first time, not a changelog and not API reference — the inline
comments already cover the details of any one function.

If you add a new file that's substantial enough to need its own inline
comments, give it its own explanation file too. If you restructure an
existing file significantly, update its explanation file to match — a
walkthrough that describes a structure the code no longer has is
actively confusing, not just outdated.

### Where this applies

- **Student-facing pages** (`docs/MINI_IDE.md`, `docs/DEWMINI.md`, the
  homepage, in-app help text): plain, friendly, welcoming language,
  written for a teenage student — no jargon without explaining it, no
  metaphor for its own sake. If you wouldn't say it that way to a
  fifteen-year-old sitting next to you, rewrite it.
- **Contributor and maintainer documentation** (`README.md`,
  `ARCHITECTURE.md`, `planning/*.md`): plain and direct, the same as
  above, but still addressed to the reader who actually reads it — a
  teacher deciding whether to build a course in dewlab, or a developer
  changing the code. Don't rewrite these to address a student; that's
  not who reads them, and doing so would make them harder to use for the
  people who do.
- **`DECISIONS_LOG.md`**: a historical record of engineering decisions,
  each dated and numbered. Keep entries accurate and readable, but don't
  simplify away real information for the sake of a friendlier tone — its
  job is precision, not welcome.

---

## 2. Before you open a pull request

- Run the repo's own checks locally — `python3 -m pytest` (skip
  `tests/e2e` unless you're testing browser behavior directly),
  `ruff check` on any Python you touched, and `python3 build.py` to
  confirm the site still builds.
- Read back the documentation and comments you touched as if you'd never
  seen this codebase before. If something needs re-reading twice to make
  sense, it needs another pass.
- If you're not sure whether a change needs a new explanation file or an
  update to an existing one, err on the side of writing it — a missing
  explanation costs the next person more time than a redundant one.

---

## Questions

If something in this file doesn't match what you find in the code, the
code is more likely to be right and this file more likely to be stale —
but say so anyway, so it can be fixed. Open an issue, or fix it yourself
and mention the mismatch in your pull request.
