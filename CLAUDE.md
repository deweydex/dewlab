# dewlab

Markdown in, a static site out. `README.md` has the full picture,
`ARCHITECTURE.md` has the map, `DECISIONS_LOG.md` has the reasoning. This
file is only what you need before touching anything.

## Running things

```bash
pip install -r requirements-build.txt   # first time only
python3 build.py --clean                # writes site/ from scratch
python3 -m pytest                       # unit + browser tests
```

`site/` is gitignored and rebuilt every time. Never edit it. If you change
anything under `vendor-src/`, or `assets/tutorial-runtime.js` (bundled
directly into `assets/vendor/standalone.bundle.js`), rebuild
`assets/vendor/` with `npm ci && npm run build` in `vendor-src/` and commit
the result, or CI fails.

## Before you write a word a student will read

Student-facing means the contents page, the topic tree, a glossary
definition, a tutorial or practice page, and any string in `build.py` that
ends up on a page — not code comments, not planning documents, not this
file. Read `planning/PEDAGOGICAL_STYLE_GUIDE.md` before writing any of it.
It is short; if you read one part, read `#voice`.

## Where the rest lives

| Doing | Read |
|---|---|
| Writing or editing a tutorial | `docs/WRITING_TUTORIALS.md`, then the style guide |
| Writing a glossary file | `.claude/skills/tutorial-glossary/SKILL.md` |
| Reviewing a tutorial's cell code | `.claude/skills/cell-code-review/SKILL.md` |
| Working an issue from the report doors | `.claude/skills/triage-report/SKILL.md` |
| Changing the build or the runtime | `CONTRIBUTING.md`, then `ARCHITECTURE.md` |
| Wondering why something works the way it does | `DECISIONS_LOG.md` |
| Anything else | `README.md` |

`CONTRIBUTING.md` has the rule that matters most when you touch code: a
change isn't finished until the document describing that behaviour
describes the new one. A stale comment is worse than no comment.

## Two traps

**Cell ids are a contract, and so is a tutorial's id.** Once a tutorial has
been in front of a class, a cell id is the key somebody's saved work lives
under, and the tutorial's id — its folder name — is the other half of that
key. Renaming either throws that work away. A cell in a world variant ends
in its world (`your-turn-1--planets`), so the world is part of its id too.

**Editing `assets/tutorial-runtime.js` without rebuilding the vendor
bundle looks harmless until CI catches it.** `standalone-bundle-is-current`
rebuilds `assets/vendor/standalone.bundle.js` from scratch and fails on
any difference from the committed copy — the one CI check a plain "the
tests passed" locally won't have run, since it needs Node, not just
Python.
