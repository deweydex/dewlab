---
name: tutorial-glossary
description: Generate or update a dewlab tutorial's <slug>.glossary.yaml — the terms, functions, operators, and formulas that specific tutorial introduces, for the reader-facing cheat sheet (planning/CHEAT_SHEETS.md). Use when asked to write, regenerate, or check a glossary file for one or more tutorials in tutorials/, or after editing a tutorial's content in a way that could add or remove what it introduces.
---

# Writing one tutorial's glossary

A glossary file says what **this specific tutorial** introduces — not what
it covers overall (`covers:` in its frontmatter already names broad
curriculum outcomes), not everything a reader now knows (that is the
*cumulative* cheat sheet build.py assembles from every glossary file in a
series, in `order.yaml` order) — only the terms, functions, operators, and
formulas that show up here for the first time in this tutorial's series.

Read `planning/CHEAT_SHEETS.md` first if you have not already; it has the
full design and the reasoning behind every rule below. This file is the
step-by-step for running that design on one tutorial.

## What you need before you start

1. **The tutorial itself** — `tutorials/<module>/<slug>.md`, or
   `tutorials/<module>/<slug>/<slug>.md` if it has releases (read the
   `.md` file directly under the tutorial's own name, not a `vX.md`
   release file — coverage does not change release to release the way
   prose might, so there is one glossary per tutorial regardless of how
   many releases it has).
2. **Its series' `order.yaml`**, to find what comes immediately before it.
3. **The cumulative glossary of everything before it in that series** — the
   union of every earlier member's own `<slug>.glossary.yaml`. If you are
   running this tutorial-by-tutorial in series order (the normal case),
   you will already have built this up from the runs before it. If asked
   to redo one tutorial in the middle of a series, gather every earlier
   member's glossary file fresh rather than trusting a stale list.
4. If the tutorial's `frontmatter` sets `practice_for:` or
   `practice_across:` — **stop**. A practice page gets no glossary file of
   its own; its cheat sheet is the union of the tutorial(s) it names, which
   build.py resolves automatically. Do not write one.

## Finding candidates

Two sources, and you need both — neither alone is reliable.

**Emphasis, mechanically.** `PEDAGOGICAL_STYLE_GUIDE.md` requires authors to
mark a term's first meaningful use in single-asterisk emphasis:
`*transformation matrix*`. `dev/curriculum_map.py`'s `EMPHASIS_RE`/
`terms_of()`/`prose_of()` already extract these correctly — code fences,
inline code, and the standing subtitle are already stripped, and a fixed
`STRESS_WORDS` list already filters out ordinary emphasis ("*not* the
same") that is not a term. Run that extraction (import it, or run
`python3 dev/curriculum_map.py` and read its vocabulary section) to get
this tutorial's own emphasised terms as your starting list. Do not
re-implement this extraction by eye — it exists, it is tested, use it.

**Your own read, for what emphasis misses.** A function or operator
introduced mainly through a code cell rarely gets written as `*@*` in
prose. Read the tutorial's cells and any surrounding prose for a function,
operator, keyword, or named formula the reader is now expected to reach
for, whether or not the author happened to emphasise it. This is where
judgment matters: using `len()` in passing, inside an example about
something else, is not the same as a tutorial that actually teaches what
`len()` does.

## Deciding what is genuinely new

For each candidate from either source:

- **Already in the cumulative glossary you were handed?** Drop it. It was
  introduced earlier in this series; this tutorial using it again is not a
  second introduction.
- **Emphasised here, but `dev/curriculum_map.py`'s `term_findings()` shows
  it used in an earlier tutorial in this series?** That is the "used
  before it was introduced" case the map already flags — read both
  places and decide whether this tutorial is re-teaching it (keep it, note
  why) or whether the emphasis here is a mistake in the tutorial itself
  worth a separate note to whoever asked you to run this (do not silently
  "fix" the tutorial's prose as a side effect of writing a glossary).
- **A stress word, an ordinary English word doing ordinary work, a
  bibliography title?** Not a term. `curriculum_map.py`'s own
  `STRESS_WORDS`/`BIBLIOGRAPHY_RE` already filter the mechanical pass; use
  the same judgment for anything your own read turned up that emphasis
  did not.
- **Something a *later* tutorial in this series actually explains, used
  here only as a black box (a function called but not taught)?** Leave it
  out. This is the one mistake that matters most — a cheat sheet that
  shows a reader something they have not been taught yet is worse than no
  cheat sheet at all (`planning/CHEAT_SHEETS.md` §1). When genuinely
  unsure whether a term belongs to this tutorial or a later one, leave it
  for the later one; it costs nothing to pick it up there, and showing it
  early cannot be undone by a reader who already saw it.

## Writing the entries

`tutorials/<module>/<slug>.glossary.yaml`:

```yaml
entries:
  - term: "transformation matrix"
    kind: concept
    definition: >
      A grid of numbers that describes a specific reshaping of space —
      multiplying it against a point moves that point to a new one.
  - term: "@"
    kind: operator
    definition: "Matrix multiplication, as opposed to * (elementwise)."
    example: "rotated = M @ point"
```

- `term` — as a reader would look it up. Lowercase unless it is a symbol or
  an actual identifier (`@`, `len()`, not `Len()`).
- `kind` — one of `concept | function | operator | formula | keyword`.
  Pick the one a reader would expect it filed under; when two apply, pick
  the more concrete one (a named formula is `formula`, not `concept`, even
  though it is also a concept).
- `definition` — one to three sentences, dewlab's own voice
  (`PEDAGOGICAL_STYLE_GUIDE.md` §4: plain, warm, no condescension, no
  emoji). This is a cheat sheet entry, not the tutorial's own explanation
  restated — shorter, and written to jog a reader's memory of something
  they already met, not to teach it fresh.
- `example` — optional. Include it when a short code fragment says more
  than another sentence would (an operator, a function's call shape); skip
  it for a pure concept.
- A tutorial that introduces nothing new gets `entries: []`, not a missing
  file — a missing file and an empty list mean the same thing to build.py,
  but an explicit empty list says this tutorial was actually checked,
  which matters if you are running this over the whole curriculum and
  want to know what has and has not been done yet.

## When you are done with one tutorial

Add its own entries to the cumulative list before moving to the next
tutorial in series order — the next run needs the updated cumulative list,
not the one you started with. If you were asked to run this across a whole
series or module, work in `order.yaml` order for exactly this reason; doing
them out of order means re-gathering the cumulative list by hand each time
rather than carrying it forward.
