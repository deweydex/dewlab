# A per-tutorial cheat sheet, closed by default

A reader-facing sidebar of definitions, functions, and formulas — scoped so
that a tutorial's cheat sheet never shows something the reader hasn't met yet.

---

## 1. What this is, and the constraint that shapes everything below

A collapsible panel, closed by default, that a reader opens to see short
definitions of the terms, functions, and formulas relevant to the tutorial
they are on. The one requirement that matters more than the content itself:
**it must never show something the reader has not been taught yet.** A cheat
sheet that spoils next week's function names is worse than no cheat sheet.

That constraint means the content cannot be written once, globally — it has
to be assembled per tutorial, from whatever came before it. Two pieces follow
from that:

1. Something has to say what each tutorial *introduces* — not what a whole
   module covers (`covers:` in frontmatter already says that, coarsely, for
   `planning/curriculum/topics.yaml`'s broad topics), but the actual names:
   `len()`, "the mean", the quadratic formula.
2. Something has to say what order tutorials are met in, so "introduces" can
   be turned into "has introduced, up to and including this one."

(2) already exists: `order.yaml`'s `order:` list, the same one `nav_for()`
uses for previous/next navigation. (1) does not, and is most of this spec.

## 2. Scope: series order, not the topic dependency graph

`planning/curriculum/topics.yaml` and `DEPENDENCIES.md` model *reachability*
— what a student could jump to next, deliberately not a running order, so a
student can skip around and a teacher can slot in whatever fits a spare week.
That is the right model for the topic tree; it is the wrong model for "what
has this specific reader already seen," which needs an actual sequence.

`order.yaml` gives exactly that, but only within one series. Series within a
module have no defined order relative to each other by default
(`write_index` lists them `sorted()` by name — alphabetical, not curricular,
and that display order is unrelated to this one) — but a module may add
`tutorials/<module>/series.yaml` (`order:`, a list of series slugs) to say
what its own curricular order is, purely for cheat-sheet purposes.

**A cheat sheet draws from the current series, up to and including the
current tutorial's own position, plus every earlier series `series.yaml`
lists before this one** (`series_chain()`, `DECISIONS_LOG.md` 7.66) — never
from another module. `computational-methods/series.yaml` lists
`python-fundamentals` before `matrices`, so matrices' cheat sheet does
include what fundamentals introduced. A series left off the list — or a
module with no `series.yaml` at all — gets series-only accumulation, which
is what a series with no fixed curricular position needs:
`reflections-and-review`, in `mit-pdp-maths-prog-integration`, is revisited
whenever a reader wants rather than sitting at one point in the course
(that series' own `.order.yaml` says so), so it is never listed anywhere
and nothing about it changed when this shipped.

A **practice page** does not have its own coverage — `practice_for`/
`practice_across` name the tutorial(s) it tests instead of appearing in
`order.yaml`'s narrative position. Its cheat sheet is therefore not computed
from its own series position at all: it is the union of the named
tutorial(s)' own cumulative cheat sheets, unpacked through the same
`practice_for`/`practice_across` build.py already validates.

## 3. The glossary file: one per (module, slug), not per release

A new sibling file, `tutorials/<module>/<slug>.glossary.yaml` — beside the
`.md` (or beside the release folder, for a tutorial with several releases;
keyed the same way `assets/editor.js`'s `allTutorials()` already keys a
tutorial, by module+slug rather than by path, since what a tutorial teaches
does not change release to release the way its prose might).

```yaml
# tutorials/computational-methods/what-a-matrix-does-to-a-picture.glossary.yaml
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

`kind` is one of `concept | function | operator | formula | keyword` —
enough to group the panel without inventing a taxonomy nobody will maintain.
A missing glossary file is not an error: the tutorial's own contribution is
empty, and its cheat sheet is whatever came before it in the series. This is
what lets the feature ship before every tutorial has one, and why generating
them is deliberately its own batch of work rather than a blocker on the UI.

This shape is shown here so a reader knows what a `.glossary.yaml` actually
looks like — not as something to hand-write. `.claude/skills/
tutorial-glossary/SKILL.md` (§4) is the tool for writing or updating one:
run it on a tutorial, and it produces this file.

## 4. The skill: writing one tutorial's *new* terms, not the cumulative list

Not a cold read. `PEDAGOGICAL_STYLE_GUIDE.md` §4 already requires authors to
mark a term's first meaningful use in single-asterisk emphasis — "define
every technical term where it first appears, and mark it in italics" — and
`dev/curriculum_map.py` already relies on that same convention being real
(`EMPHASIS_RE`, `terms_of()`, `term_findings()`'s "introduced more than
once"/"used before it was introduced" checks, DECISIONS_LOG.md 5.11). That
is evidence of what an author considered a new word, not a list anyone
maintains by hand — and it means most of a tutorial's glossary candidates
already exist, mechanically extractable, before the skill reads a word of
prose.

The skill still needs judgment for two things emphasis alone will not catch:
a function or operator introduced mainly through a code cell rather than a
sentence (`@` for matrix multiplication is unlikely to appear as
`*@*` in prose), and confirming a candidate is genuinely new *for this
series* rather than one `term_findings()` would flag as repeated — emphasis
says "the author considered this new here," not "no earlier tutorial in
this series said it too."

Given one tutorial and the cumulative glossary of everything before it in
its series, the skill's job:

1. Run `dev/curriculum_map.py`'s extraction (or the equivalent read) to get
   this tutorial's own emphasised terms as a starting candidate list.
2. Read the tutorial's prose and cells for anything else it introduces as a
   tool the reader is now expected to reach for — a function, an operator,
   a named formula — whether or not it happened to be emphasised.
3. Drop anything already in the cumulative glossary it was handed, and
   anything `term_findings()` would flag as used earlier in the series than
   this tutorial.
4. Write `<slug>.glossary.yaml` with what remains. Short definitions,
   dewlab's own voice (`planning/PEDAGOGICAL_STYLE_GUIDE.md`), no invented
   forward references.
5. A practice page gets no glossary file at all — §2 already covers its
   content from what it practices.

Lives at `.claude/skills/tutorial-glossary/SKILL.md` (new directory; no
project skills exist yet). Run once per tutorial, in series order, each run
handed the accumulated output of every earlier run in that series — the
skill never has to re-derive "what came before," only receive it.

## 5. Build integration

`build.py`, per series, in `order.yaml` order:

1. Load each member's glossary file (if any).
2. Accumulate: `cumulative[i] = cumulative[i-1] + member[i].own_entries`.
3. For a practice page, look up its `practice_for`/`practice_across`
   target(s)' cumulative list instead of computing its own.
4. Pass the page's cumulative list into the page template as JSON — the
   same pattern `{{MANIFEST_JSON}}` already uses — so the runtime renders it
   without a second fetch.

## 6. The reader-facing panel

- **Toggle**: a small fixed-position button pinned to the page's top-left
  corner (independent of `.dl-masthead`'s flex row, which already has the
  wordmark on the left and Settings on the right — crowding either would
  cost one of them its space). Closed by default; state is not persisted
  across pages, same as Settings.
- **Panel**: anchored top-right, reusing `.dl-settings`'s own floating-card
  positioning (`position: fixed; right: 1rem; top: calc(chrome-height +
  ...)`, scrollable, same shadow/border/radius) rather than inventing a
  second panel language. Opening the cheat sheet closes Settings if it is
  open, and vice versa — both anchored to the same corner, so showing both
  at once would overlap.
- **Content**: entries grouped by `kind`, term + definition (+ example where
  present), in the order the series introduced them.
- **Empty state**: a tutorial with nothing accumulated yet (the first in its
  series, before any glossaries exist) hides the toggle entirely — same
  reasoning `dl-settings-section`s with nothing in them already use elsewhere
  in this codebase.
- **Mobile**: under the same `max-width: 34rem` phone breakpoint the rest
  of the page already collapses at, the panel becomes a bottom sheet
  (`top: auto; bottom: 0; left: 0; right: 0`) — the same treatment
  `.dl-settings` already has, rather than hiding outright. The toggle stays
  a small fixed corner button at this width; only the floating panel shape
  stopped working, and that is what changes.

## 7. What ships in what order

Roughly: schema + a couple of hand-written example glossaries to prove the
shape → build.py assembly + tests → the UI (toggle, panel, styling) wired to
real data → the skill itself → running the skill across every tutorial,
batched by series (this is most of the remaining work — dozens of tutorials,
each needing an actual read) → docs. Each stage is a PR of its own rather
than one large one, so a mistake in the schema is caught before forty files
commit to it.
