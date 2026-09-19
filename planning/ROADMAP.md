# Roadmap

What's still ahead, and the questions each piece leaves open.
`STATUS.md` covers what's already built; the root `QUESTIONS.md` holds
questions needing a person's answer; this file is neither — once a
piece ships, it moves to `STATUS.md` and drops out of here entirely.

---

## Documentation debt

- `editor.js`, `tree.js`, and `search.js` have no matching
  `docs/<file>-explained.md`, though `CONTRIBUTING.md` promises one per
  substantial code file.

## The reference's term-linking, beyond first occurrence

Only the first occurrence of a term per section links back to where it
was introduced (built). Linking every later occurrence was tried,
measured, and withdrawn — too many false hits from ordinary English
words that are also glossary terms (*shape*, for one).

**Open:**

- **Exact string match, or inflected?** Does "matrices" link back to
  *matrix*? Leaning toward exact match plus a hand-written `forms:`
  list in the glossary YAML where a term needs one, over a stemmer that
  guesses wrong in maths prose.
- **What do retrieval prompts look like** — the reference surfacing
  terms met some tutorials ago, phrased invitationally, never as a
  score? Not designed. Judge once the above has settled whether the
  reference panel is the right home for this at all.

## Content gaps, not blocking anything

- **The link-graph strand's crawl is a toy** — *Where Chains Lead*'s
  three-page PageRank example, not a real crawl. Set aside as too
  advanced for where the curriculum sits now.
- **The worksheet-to-practice converter is unwritten**, on hold, and
  possibly not needed — the worksheets whose material is taught are
  already converted by hand.
