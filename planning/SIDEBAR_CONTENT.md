# A second sidebar: datasets, pedagogical notes, and images

Design note, not a spec ready to build from — three related asks bundled
together because they turned out to share one authoring question: *how
does content get from a markdown file into a sidebar without turning the
markdown into something else.* No code changes in this pass.

---

## 1. Three asks, and what already exists for each

**Datasets, kept in the repo, with attribution.** More built than it looks.
`data/` already exists (currently just `.gitkeep`), the build already
serves it to every page (`manifest.dataBase`, `build.py`), and
`tutorial_tools.load_csv(name)` already fetches a CSV from it and returns a
DataFrame — "datasets live once and are fetched at runtime — never
embedded or copied per tutorial," per its own docstring. **Nothing calls
it yet**: `grep -r load_csv tutorials/` finds nothing. So the actual gap is
not the mechanism, it is (a) real dataset files with a source anyone can
check, and (b) somewhere for attribution to live that survives the dataset
being used by more than one tutorial.

**Pedagogical notes / additional context.** Nothing exists for this today.
The closest relative is the hint/answer fold (`FOLD_CLASSES`,
`check_folds()`) — a `<details class="dl-hint">` block an author already
writes directly in markdown, which the build already scans for and
validates. A note is a different shape (never hidden behind a click the
way a hint is; meant to be seen, just not mid-paragraph) but the same
underlying trick — raw HTML inside markdown, checked at build time — is a
precedent worth reusing rather than reinventing.

**Images, inline and in a sidebar.** Already fully solved for the inline
half: ordinary `![alt](path)` markdown, alt-text required and checked
(`check_alt_text()`). Nothing exists for "also show this in a sidebar" —
but per §3 below, that turns out not to need its own mechanism if notes
already have one, since a note that contains an image is just markdown
content, and markdown content already renders an image correctly wherever
it is placed. No YouTube or other video embeds in this pass, matching what
was actually asked for.

## 2. Datasets: no new markdown syntax needed at all

This one does not need an authoring-mechanism decision, because a dataset
is not prose bound to a point in a tutorial's flow — it is a fact about a
file. Two small additions, neither touching the fence/cell machinery:

- **`data/ATTRIBUTION.yaml`** (or one `.yaml` per dataset, `data/<name>.yaml`
  beside `data/<name>.csv` — same beside-the-file pattern
  `<slug>.glossary.yaml` already established for tutorials): source, license,
  and a one-line description per file. One place attribution lives once,
  however many tutorials end up using that file.
- **A `datasets:` frontmatter list** on a tutorial (`datasets: [life-expectancy]`),
  the same shape `covers:`/`practice_for` already are — explicit and
  declarative, not scraped from cell code (grepping cells for
  `load_csv("...")` calls would work today, but breaks the moment a dataset
  name is built from a variable instead of a literal, and frontmatter never
  has that problem).

`build.py` cross-references the two — the same `fail()`-on-mismatch pattern
`practice_pairs()` already uses for `practice_for` — and a tutorial's
manifest carries its own datasets' attribution alongside whatever else it
already sends. What renders it is §4.

## 3. Notes: fence-tagged cell vs. HTML aside, compared

Two ways to write one, both real, both already have working relatives
in this codebase:

### (a) A new fence designator

```` ```note
id: why-order-matters
Multiplying grids in the wrong order gives a different, wrong answer —
this is *not* true of ordinary numbers, and it is the first place this
course asks you to unlearn a assumption from arithmetic.
``` ````

Parsed exactly where `exec` already is (`extract_blocks()`'s `"exec" in
info` branch), as a third fence kind alongside "cell" and "illustrative
code." Reads naturally next to a `python exec` fence an author has already
written five of on the same page — one more fence tag to learn, in a
vocabulary that already has fence tags.

*Cost: real code change — `extract_blocks()` needs a third branch,
`Tutorial` needs a `notes: list[Note]` field, and a new dataclass. Not
large (the `exec`-vs-illustrative dispatch this extends is already exactly
this shape), but not zero either.*

### (b) An HTML aside, same trick as the hint/answer fold

```html
<aside class="dl-note" id="why-order-matters">

Multiplying grids in the wrong order gives a different, wrong answer —
this is *not* true of ordinary numbers, and it is the first place this
course asks you to unlearn an assumption from arithmetic.

</aside>
```

(The blank lines after `<aside ...>` and before `</aside>` matter — that is
what makes most markdown converters still process the inside as markdown
rather than treating it as opaque HTML, the same reason the existing
hint/answer folds are written the same way.) Extracted the same way
`check_folds()` already scans `body_html` for `<details>` tags with a known
class — a new `check`/`extract` pass over `<aside class="dl-note">`, not a
change to fence parsing at all.

*Cost: smaller — no `FENCE_RE`/`extract_blocks()` changes, because this
never goes near the fence machinery. A body-scan function in the same
family as `check_alt_text()`/`check_folds()`, plus the same small
`Tutorial.notes` field (a) also needs.*

### Comparison

| | (a) fence | (b) HTML aside |
|---|---|---|
| New concept for an author | A new fence tag | None — same trick as hint/answer, already known |
| Build-time change | New branch in the fence dispatcher | New scan function, same shape as two that already exist |
| Reads as "markdown" | Yes, fence syntax is markdown-native | Less so — raw HTML, though the folds already set this precedent |
| Risk of colliding with `exec`/illustrative fences | None — a third tag | None — different mechanism entirely |

Both are cheap. (b) is cheaper and, more importantly, is not a new pattern
— it is the same pattern the fold feature already proved works, already
documented, already has a build-time check to model the new one on. That
is the stronger argument than the small code-size difference: one fewer
kind of thing for the next person reading `build.py` to learn.

**Recommendation: (b), the HTML aside**, for that reason — reuse over
invention, matching how this codebase has generally chosen to grow (the
cheat sheet panel reusing `.dl-settings`'s CSS rather than inventing a
second panel language is the same instinct, one PR ago).

## 4. Where notes (and datasets) surface

The user's own phrasing floated this directly: pedagogical notes "or,
better yet, in the other side bar" — i.e. not necessarily a *third* panel.
Two real options:

- **A third panel**, its own toggle, mirroring `.dl-cheatsheet`/`.dl-settings`.
  Consistent with how the cheat sheet was built, but a third fixed-position
  toggle competing for the same top-left corner the cheat sheet's toggle
  already claimed — needs its own spot (stacking two small buttons is fine
  visually; three floating panels all mutually closing each other is more
  moving parts than either alone).
- **A second section inside the existing cheat-sheet panel** — "This
  tutorial's cheat sheet" (what 7.64/7.65 already ships, cumulative across
  the series) plus a "Notes" section and a "Datasets used here" section
  (both **not** cumulative — a note is tied to this specific tutorial, not
  something every later tutorial keeps carrying, the way a glossary term
  does). Same toggle, same panel, no new open/close/mutual-exclusion wiring
  at all — `renderCheatSheet()` already groups by kind; grouping by
  section is the same idea one level up.

**Recommendation: extend the existing panel**, for the same reuse-over-
invention reason as §3, and because it directly answers what was asked
for ("in the other side bar") rather than substituting a design the
request explicitly considered and set aside. The one thing this costs is
conceptual: the panel stops being *only* "what has this reader been
taught" and starts being "everything about this tutorial worth having to
hand" — worth naming clearly in the UI (a heading per section) so a reader
does not read a note as if it were a taught, examinable term.

## 5. What this does not decide

- Exact wording/heading for the panel once it holds more than a cumulative
  glossary (still called "Cheat sheet"? Something broader?) — a naming
  question, not an architecture one, and cheap to change later either way.
- Whether every tutorial needs a note, or whether most will have none —
  same "a missing file/field means empty, not an error" shape the cheat
  sheet already established, so this costs nothing to leave unanswered:
  an empty `notes:`/no `<aside>` tags is simply nothing added to the panel.
- The `.glossary.yaml`-writing skill's counterpart for notes and datasets —
  out of scope here on purpose. Notes are authorial judgment about what
  deserves a call-out, not "what did this tutorial teach," which is a much
  worse fit for a mechanical extraction skill than the glossary was.

## 6. Rollout sketch, if this goes ahead

Roughly: `data/ATTRIBUTION.yaml` schema + one real dataset file, proving the
shape → `datasets:` frontmatter + build.py cross-reference + first tutorial
actually calling `load_csv` → the `<aside class="dl-note">` scan +
`Tutorial.notes` + tests, same shape as `check_folds()` → the panel's new
sections in `tutorial-runtime.js`/CSS → docs. Each a PR of its own, same
reasoning `CHEAT_SHEETS.md` §7 gave for staging that feature the same way.
