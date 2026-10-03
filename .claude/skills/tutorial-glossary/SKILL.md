---
name: tutorial-glossary
description: Generate or update a dewlab tutorial's <slug>.glossary.yaml — the terms, functions, operators, and formulas that specific tutorial introduces, for the reader-facing reference (planning/REFERENCE_PANEL.md). Use when asked to write, regenerate, or check a glossary file for one or more tutorials in tutorials/, or after editing a tutorial's content in a way that could add or remove what it introduces.
---

# Writing one tutorial's glossary

A glossary file lists what this tutorial introduces for the first time in its series: terms, functions, operators, formulas. It is not `covers:` (curriculum outcomes), and it is not everything the reader now knows; build.py assembles that cumulative reference from the series' glossary files in course-file order. The design and its reasons are in `planning/REFERENCE_PANEL.md`.

## Before you start

1. Read the tutorial, `tutorials/<id>/<id>.md`, not a `v<version>.md` release file. There is one glossary per tutorial however many releases it has.
2. Read its course file, `courses/<course>.yaml`, for the series order, and gather the union of every earlier member's `<slug>.glossary.yaml`. Run in series order and carry the list forward; redoing one tutorial mid-series, gather it fresh.
3. If the frontmatter sets `practice_for:` or `practice_across:`, **stop**: a practice page gets no glossary file, and build.py resolves its reference from the tutorials it names. A `context_for:` page gets a file only for terms it defines that its tutorials do not, checked against that union.

## Find candidates

You need both sources.

- **Emphasis.** Authors mark a term's first use as `*term*` (`docs/WRITING_TUTORIALS.md#marking-a-term`). `dev/curriculum_map.py` extracts these (`terms_of()`, `EMPHASIS_RE`, `STRESS_WORDS`); import it or run it and read its vocabulary section, rather than finding them by eye. A `*term*{.term}` is a later use and is not introduced here.
- **Your own read of the cells and prose**, for functions, operators, keywords and named formulas the reader is now expected to use but nobody emphasised. A tutorial that teaches `len()` counts; one that uses it in passing does not.

## Decide what is new

- Already in the cumulative glossary, a stress word, an ordinary word, or a bibliography title: drop it.
- Emphasised here, but `term_findings()` shows an earlier use: decide whether this tutorial re-teaches it (keep it, note why) or the emphasis is a mistake. Report a mistake to whoever asked; do not edit the tutorial's prose as a side effect.
- Used here only as a black box and explained by a later tutorial: leave it out. A reference that shows a reader something they have not been taught is worse than none. When unsure, leave it for the later tutorial.

## Write the entries

`tutorials/<id>/<id>.glossary.yaml`:

```yaml
entries:
  - term: "transformation matrix"
    kind: concept
    definition: >
      A transformation matrix is a grid of numbers that describes one
      specific reshaping of space. Multiplying it against a point moves
      that point somewhere new.
  - term: "@"
    kind: operator
    definition: "Multiplies two matrices. Use * instead to multiply elementwise."
    example: "rotated = M @ point"
```

- `term`: as a reader would look it up. Lowercase unless a symbol or identifier (`@`, `len()`).
- `kind`: one of `concept | function | operator | formula | keyword`. When two apply, take the more concrete (a named formula is `formula`).
- `definition`: one to three sentences in the style guide's voice, with its plain-language rules (`PEDAGOGICAL_STYLE_GUIDE.md#plain-language`). It jogs the memory of something already met; it is not the tutorial's explanation again. The rules a glossary breaks most:
  - Write a sentence, not a noun phrase: *A matrix is a grid of numbers.* The exception is `function` and `operator` entries, which lead with the verb: *Displays whatever is inside its parentheses.*
  - One idea per sentence, about twenty words.
  - Say what a thing is before what it is not.
  - A metaphor may follow a plain statement. It never replaces one.
- `example`: optional. Use it when a short fragment says more than another sentence (an operator, a call shape). Skip it for a pure concept.
- `python`: for anything that names a Python object, the exact dotted name or a list of them, owner included:

  ```yaml
  - term: "append()"
    python: list.append
  - term: "math.sin(), math.cos()"
    python: [math.sin, math.cos]
  - term: "elif"
    python: elif
  - term: "show()"
    python: tutorial_tools.show
  ```

  Give one to every Python function, method, keyword and built-in exception, third-party ones included. Omit it for non-Python things (CSS, SQL), operators, and special methods such as `__str__`.

Then run `python3.13 dev/glossary_python.py`. It checks that each name exists and that the `example` fits the real signature, and it writes the signatures the reference shows. Do not write signatures yourself. CI runs it with `--check` on 3.13, so another Python version fails there.

A tutorial that introduces nothing gets `entries: []`, not a missing file. The empty list records that it was checked.
