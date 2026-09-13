# Roadmap

What to build next, in order, with the questions each piece leaves open.
`STATUS.md` records what is already built; the root `QUESTIONS.md` holds
questions needing an answer from a person; this file records what comes
next and why. When a phase ships, its section here shrinks to a summary
and the detail moves to `STATUS.md`. When a question gets answered, the
answer lands in `QUESTIONS.md` and `DECISIONS_LOG.md`.

Ordering logic, in one line: fix the record first, then write the content,
then take only the platform work that multiplies content or serves
assessment.

Each open question below gives: what is asked, what will be assumed if
nobody answers, what changing it later costs, and what it blocks. Most
block nothing — stated where it matters.

---

## Phase 1 — Put the record straight — **done**

Restored the property the build already enforces for tutorials —
documentation can't quietly drift from what it describes — to the
documentation itself. `dev/check_doc_links.py`, run by CI, fails the build
on a dead link or path in any current-tense document (decision records are
exempt, since a past entry naming something by its old name was true when
written). It found 99 stale references on its first run; all are now fixed
or deliberately exempt. `planning/README.md` indexes every planning
document again. Every tutorial moved to its own folder
(`tutorials/<module>/<slug>/`), so a release adds a file instead of moving
one and a tutorial is one thing to move or freeze rather than several files
in two places — see `DECISIONS_LOG.md` 7.90. Nothing a student receives
changed; the built site was byte-identical afterwards.

**Still worth doing, not done here:**

- The `*-explained.md` files `README.md` promises "one per code file" do
  not exist for `editor.js`, `tree.js` or `search.js`. Either write them or
  correct the promise.
- `tests/MANUAL_CHECKLIST.md` still says later sections are stubs for
  phases that have all shipped.
- Of the three empty module folders under `tutorials/`, two
  (`mathematics-for-it`, `programming-design-principles`) are gone now that
  the integrated module covers them. `database-methods` is no longer
  empty either — it shipped as its own module (`DECISIONS_LOG.md` 7.147).

## Phase 2 — Write the remaining tutorials — **done**

All five Computational Methods strands are written. `CURRICULUM_MAP.md`
now reports 115 of 116 outcomes in place across all six accredited
modules, the one gap being `WA-LO12` in the since-added Web Authoring
module. `planning/STATUS.md` §2 has the per-outcome detail.

**Left undone, on purpose — not blocking, but real:**

1. A new *Text Generation* series (*A Chain Reads a Book*, *How Much It
   Remembers*, *Whose Voice Is This*, in `computational-methods`) is the
   first content to exercise the dataset apparatus end to end —
   `datasets:` frontmatter, `check_datasets()`, sidebar attribution, and a
   new `load_csv()` sibling, `load_text()`, across six bundled
   public-domain books. `load_csv()` itself, and
   `co2-emissions.csv`/`life-expectancy.csv` specifically, are still
   unclaimed by any tutorial — the apparatus is proven for text, not yet
   for tabular data.
2. The link-graph strand's crawl is still open. A first attempt at growing
   *Where Chains Lead*'s toy three-page PageRank example into a real crawl
   was designed and set aside as too advanced for where the curriculum
   currently sits; item 1's Markov-chain series was built instead. The toy
   PageRank example remains the only content on this topic.
3. The worksheet converter is still on hold — hand conversion hasn't become
   the bottleneck.

Whether either of the first two is worth doing now that every outcome is
covered, versus moving straight to Phase 3, is an open question of its own.

---

## Phase 3 — Highlights and margin notes

*(This slot held "Practice that regenerates" — seeded problem generators
with a "try another" control. Retired unbuilt, 2026-09-13, before any of
its open questions were settled — `DECISIONS_LOG.md` 7.155. The original
plan is still readable in git history at the commit that replaced this
section.)*

A reader marks a passage of prose, durably, with an optional note tied to
that specific passage — the persistent-highlighting idea Phase 5 raised
and set aside as needing real anchoring work. `HIGHLIGHTS_AND_NOTES.md`
has the full design: the anchoring scheme (quote-and-position, computed at
read time, no build.py change), the schema addition to the existing
saved-progress record, the selection toolbar, and a dozen-plus rollout
steps. Not started; that document is the plan.

## Phase 4 — retired

*(This slot held "The portfolio export" — a "Compile my work" button
producing a standalone document from a student's saved progress. Retired
unbuilt, 2026-09-13, in favour of Phase 3 above — `DECISIONS_LOG.md`
7.155. `HIGHLIGHTS_AND_NOTES.md` §11 explains why a highlight-with-a-note
makes a future portfolio export cheaper without building one now. The
original plan is still readable in git history at the commit that
replaced this section.)*

## Phase 5 — The reference grows up

The glossary machinery already knows what every tutorial teaches and where
every term is first used in italics. Three steps, each earning the next.

**The work:**

1. Highlight-to-search — **built**, `DECISIONS_LOG.md` 7.93. Select text on
   the page and, when the reference knows the term, a small button offers
   to open the panel filtered to it. No persistence, no new storage. It
   stays away for every selection that isn't a term, which is most of
   them.
2. "Where did I meet this?" — **built, but not as specified**,
   `DECISIONS_LOG.md` 7.94. Linking every later occurrence in the prose was
   built, measured, and withdrawn: ordinary English words are also
   glossary terms, and most matches for *shape* on one page were the
   everyday sense, not the matrix one. Each inherited reference entry now
   says "Introduced in *Title*" and links to the section instead — same
   question answered, no way to be wrong about a sense.
3. Only after both have lived for a while: gentle retrieval prompts — the
   reference surfacing terms met some tutorials ago, phrased
   invitationally, never as a score.

**Open questions:**

- **How is a term matched in prose?** Exact string only, or inflected —
  does "matrices" link back to *matrix*? Assumed: exact match plus a
  hand-written `forms:` list in the glossary YAML where a term needs one,
  rather than a stemmer that will guess wrong in maths prose. Cost: small;
  the glossary format grows one optional field.
- **How much linking before prose gets noisy?** Assumed: first occurrence
  per section only, styled as quietly as the existing italics. Cost: a
  rendering rule, changeable freely.
- **Persistent highlighting: in or out?** Out, for now. Highlights need
  anchors that survive a version release; cell ids give that to code but
  prose has none, and an anchoring scheme (paragraph fingerprinting or
  similar) is real work. Once one exists, highlighting, margin notes, and
  reflection-answer boxes all become cheap — so the right question is "is a
  prose anchoring scheme worth building," asked once, not three separate
  feature questions. Blocks nothing in this phase.
- **What do retrieval prompts look like concretely?** Not designed here.
  Judge after step 2 ships whether the reference panel is the right home
  or whether it belongs on the contents page.

---

## Phase 6 — One workspace, and the edges — **done**

The edges audit is done — `planning/EDGES_AUDIT.md`, `DECISIONS_LOG.md`
7.95. The offline bundle boots and runs Python with every non-loopback
request blocked; two causes of sideways scrolling on a 375px phone were
found and fixed; a heading-order break on the contents page was corrected.
A real screen-reader pass still needs a person, and tap-target sizes are a
design decision rather than a patch — both named at the end of that
document.

Mini IDE has retired (`DECISIONS_LOG.md` 7.91) and dewmini has its own
downloadable, offline-capable copy (7.92). The parity checklist that
tracked those two gaps has been dropped rather than updated, since it
planned work that has happened; `MINI_IDE_AND_DEWMINI_NEXT.md`'s third
addendum keeps the one part of it that outlasts the plan.

Reviewing the Worker migration after it merged found six defects
(`DECISIONS_LOG.md` 7.97), the worst of them in the now-single shared
engine — with one engine serving every surface that runs Python, a change
to it is a change to all of them.

## Phase 6 — the original plan

`MINI_IDE_AND_DEWMINI_NEXT.md`'s addendum records the decision: dewmini
absorbs Mini IDE's capabilities and keeps its own smaller style; Mini IDE
retires at parity.

**The work:**

1. **Done.** A written parity checklist (files, uploads, SQLite, notebook
   import, Stop); dewmini gained each item in its own style
   (`DECISIONS_LOG.md` 7.87–7.89). The one item off that checklist — an
   offline, downloadable copy of the tool itself — landed separately once
   Mini IDE's retirement made it non-optional (`DECISIONS_LOG.md` 7.92),
   and surfaced a real bug in both offline bundles' core promise: neither
   could actually be opened by double-clicking, only served locally, until
   building dewmini's own bundle tested it.
2. **Done.** Mini IDE retired (`DECISIONS_LOG.md` 7.91); a later pass
   (`DECISIONS_LOG.md` 7.98) removed the app, its stylesheet, its offline
   download, and the redirect — nothing remains. dewmini and the tutorial
   pages already shared `tutorial-style.css`'s tokens and `.dl-*` classes
   before retirement, so there was no separate stylesheet-collapsing step.
3. The edges audit — done, above.

**Open questions:**

- **Does dewmini take the Worker engine?** Decided and done
  (`DECISIONS_LOG.md` 7.89): yes. The separable client became
  `assets/pyodide-engine.js`, shared rather than duplicated.
- **What happens to Mini IDE's URLs and downloaded bundles?** Decided and
  done, in two steps (`DECISIONS_LOG.md` 7.91, 7.98): the hosted page
  became a redirect at first; both the redirect and the offline download
  were then removed once dewmini's own offline bundle covered the need.
- **Offline proof: manual or CI?** Partly answered: a manual pass
  (`DECISIONS_LOG.md` 7.92) served both bundles with *serve.py* and ran a
  real interrupt-a-`while True`-loop Stop-button test against each, plus a
  `load_csv()` call against dewmini's own bundled `data/` — proof the
  *served* bundle works, not yet proof it works with the network fully
  off (both tests still reached a locally-vendored Pyodide over HTTP, not
  the bundle's own `assets/vendor/pyodide/`). Still assumed: a
  `MANUAL_CHECKLIST.md` entry per release for the fully-offline case; a CI
  job that serves a bundle with outbound network blocked if the manual
  check ever gets skipped.
- **What is the screen-reader baseline?** Assumed: VoiceOver/Safari and
  NVDA/Firefox, the pair a Dublin classroom is most likely to contain.
  Worth a minute of anyone's disagreement before it hardens into fact.

---

## What this file is not

Not a promise and not a schedule — phases ship independently and can be
stopped or reordered after any of them. The one hard dependency is that
Phase 5's term-linking wants Phase 2's glossaries written. And not a place
where questions get answered: when one is decided, the answer moves to
`QUESTIONS.md` and `DECISIONS_LOG.md`, and this file just says so.
