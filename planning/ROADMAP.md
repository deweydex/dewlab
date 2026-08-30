# Roadmap

What to build next, in order, with the questions each piece leaves open.
This sits between two existing documents: `STATUS.md` records what is
already built, and the root `QUESTIONS.md` holds questions that need an
answer from a person. This one records what comes next and why it comes in
this order. When a phase ships, its section moves to `STATUS.md` in
summary; when one of its questions gets answered, the answer lands in
`QUESTIONS.md`'s Answered section and `DECISIONS_LOG.md`, same as any
other decision.

The ordering logic, in one line: fix the record first, then write the
content, then take only the platform work that multiplies content or
serves assessment.

Each open question below follows `QUESTIONS.md`'s shape where it can:
what is asked, what will be assumed if nobody answers, what changing it
later costs, and what it blocks. Most block nothing — that is stated
where it matters.

---

## Phase 1 — Put the record straight — **done**

Small pieces, mostly independent, all cheap. The point was to restore the
property the build already enforces for tutorials — that documentation
cannot quietly drift from what it describes — to the documentation
itself.

**What was done:**

1. **`dev/check_doc_links.py`**, run by CI, holds every document that
   describes the present to the present: a markdown link or a backticked
   path naming a file that is not in the repository fails the build.
   Records of what was decided *then* — `DECISIONS_LOG.md`,
   `QUESTIONS.md`, the superseded and retired planning docs — are exempt
   on purpose: an entry naming the reference panel's design doc by the
   name it had before it was renamed is not stale — that was its name when
   the entry was written, and rewriting it would make the record say
   something that was never true.
2. It found 99 references on its first run. All are now either fixed or
   deliberately exempt, and the fixes were real rather than cosmetic:
   attribution documented as the shape that shipped rather than the one
   the design rejected, a worksheet converter no longer named as a file
   that exists, `<series>.order.yaml` written as its real name.
3. `planning/README.md` indexes every planning document again — nine were
   missing, `REFERENCE_PANEL.md` among them, which `ARCHITECTURE.md`
   treats as a spec. `Educational Content guide for LLMs.md` is gone.
4. Stale facts corrected: `build.py`'s line count removed rather than
   updated, sympy described as opt-in because that is what the code does,
   the runtime's "not here yet" header dropped for three things that
   shipped years of entries ago, `image_input` and `run_query` added to
   the table of what a cell can call.
5. The build-language question is closed — see `QUESTIONS.md`.
6. Every tutorial is a folder. See below.

**The layout, answered.** A tutorial is now
`tutorials/<module>/<slug>/`, holding its markdown at `<slug>.md`, its
practice page, its glossary, its frozen past releases as `v<version>.md`,
and any pictures or recordings it uses. `DECISIONS_LOG.md` 7.90 has the
full account and `QUESTIONS.md` the reasoning. Three things came with it:
releasing adds a file instead of moving one, assets have somewhere to live
and a reference that resolves from every release, and a tutorial is one
thing to move or freeze rather than several files in two places. Nothing a
student receives changed — the built site was byte-identical afterwards.

**Still worth doing, and not done here:**

- The `*-explained.md` files `README.md` promises "one per code file" do
  not exist for `editor.js`, `tree.js` or `search.js`. Either write them
  or correct the promise.
- `tests/MANUAL_CHECKLIST.md` still says later sections are stubs for
  phases that have all shipped.
- The three empty module folders under `tutorials/` are still there.

## Phase 2 — Write the remaining tutorials

The bulk of the term's effort. Three of the five Computational Methods
strands are unwritten, and every planned platform feature is worth less
than these pages existing.

**The work:**

1. *Discrete Simulation & Monte Carlo Methods* — estimating π, queuing
   models, randomness (`CMPS-LO3`, `CMPS-LO6`, the randomness half of
   `CMPS-LO2`).
2. *Algorithmic Complexity & Systems Modeling* — complexity bounds,
   cache prediction, thermal simulation (`CMPS-LO5`, `CMPS-LO7`–`LO13`).
3. The remaining half of the link-graph strand: a real crawl or link
   graph beyond the worked three-page PageRank example.
4. Make at least one of these the first tutorial to use real data. The
   entire dataset apparatus — `data/`, `load_csv()`, the `datasets:`
   frontmatter, `check_datasets()`, the sidebar attribution — is built
   and used by nothing. `co2-emissions.csv` and `life-expectancy.csv`
   are sitting there licensed and cited.
5. Per tutorial as it ships, as already practised: an outline in
   `planning/outlines/`, the glossary skill, the cell-review skill, and
   `covers:` mapping checked against the curriculum map.

**Open questions:**

- **Which strand first?** *Assumed:* Monte Carlo — it builds on
  randomness the matrices series already touched, and it is the most
  immediately engaging material for a January-tired cohort. *Blocks:*
  nothing; the strands are independent.
- **Do long-running simulations need a tutorial convention of their
  own?** Thermal models and queue simulations run longer than any
  existing cell; the Stop button exists, but nothing in the tutorial
  format says "this cell takes ten seconds, that is normal." *Assumed:*
  a sentence of prose suffices until proven otherwise. *Cost:* a
  convention added later touches only new tutorials.
- **Does the worksheet converter revive?** It was never written. The
  unconverted worksheets
  (Bayes, distributions, the matrices set) cover material these strands
  will teach. *Assumed:* still on hold; convert by hand as before, and
  revisit only if hand conversion is the bottleneck in practice.

---

## Phase 3 — Practice that regenerates

One authored problem template becomes as much practice as a student
wants. The architecture makes this unusually cheap: the generator and
the checker are both Python, running in the Pyodide the student already
has. Nothing leaves the browser and there is no answer key to leak.

**The work:**

1. A cell convention for seeded problems: the fence carries generator
   code that produces the problem text and numbers from a seed, plus a
   `check()` that computes the expected answer from the same seed.
2. A "try another like this" control on such cells, re-seeding and
   regenerating in place.
3. Retrofit two or three existing practice pages to prove the shape
   before any new page is written with it.

**Open questions:**

- **Where does the seed live, and what does a reopened page show?**
  *Assumed:* the seed is stored in the saved-progress record, so a
  student who closes the tab returns to the same problem they left, and
  "try another" writes a new seed. *Cost to change:* high once shipped —
  this touches the saved-work schema, which `WINDOW_AUDIT.md` treats as
  a frozen contract. This is the question to settle most carefully, and
  first.
- **Does a regenerated problem replace the old attempt or accumulate?**
  *Assumed:* replace — the record stays one-cell-one-slot, matching the
  existing schema, and a student who wants to keep an attempt exports
  it. Accumulating attempts is a schema change (same warning as above).
- **How is the generator authored?** In the fence itself, hidden from
  the reader, or as a sidecar file? *Assumed:* in the fence, marked by a
  new tag on the existing `python exec` convention, since the build
  already parses fence info strings and a sidecar adds a file per
  problem. *Cost:* moderate — the editor's `restoreExecTag()` and the
  build's fence parsing both learn one more tag.
- **Is `check()` enough as it stands?** It compares a value; a generated
  problem may want tolerance, multiple accepted forms, or a worked
  solution behind a fold. *Assumed:* start with what `check()` does and
  let real problems argue for extensions one at a time.

---

## Phase 4 — The portfolio export

QQI Level 5 assessment leans on collections of work. A student's dewlab
record — code, outputs, notes, their own added cells — already is one,
trapped in `localStorage`. One button turns the no-tracking stance into
an asset: the student owns the evidence and chooses to hand it over.
Nothing is scored; everything is theirs.

**The work:**

1. "Compile my work": a standalone HTML document assembling the
   tutorial's exercises with the student's answers, notes, reader-added
   cells, and dates, built from the standalone-export machinery and the
   saved-progress record, both of which exist.
2. A student-facing paragraph in `docs/FOR_STUDENTS.md` explaining what
   it is for.

**Open questions:**

- **Per tutorial, per series, or per module?** *Assumed:* per series,
  with per-tutorial as the degenerate case — a series is the natural
  unit of evidence for one topic. *Cost:* small; the assembly loop just
  reads more records.
- **Do reflection sections gain an answer box?** Reflections are
  currently open questions in prose with nowhere to write — the notes
  field is per-tutorial, not per-question. A portfolio that shows the
  reflections unanswered undersells exactly the part where the learning
  lands. *Assumed:* not in the first version; the per-tutorial notes
  field appears in the export beside the reflection section. This is
  the question most worth answering properly rather than by default,
  because an answer box changes the tutorial format itself.
- **What would an assessor need to trust it?** Dates and version ids
  are in the record already; whether QQI verification wants anything
  more (a declaration of own work, a tutor countersignature line) is a
  question for a colleague or external examiner, not for this
  repository. *Blocks:* nothing — build the export, then ask with the
  artifact in hand.
- **Where does the button live?** *Assumed:* Settings, under "Your
  work," beside the existing export. *Cost:* nil.

---

## Phase 5 — The reference grows up

The glossary machinery already knows what every tutorial teaches and
where every term is first used in italics. Three steps, each earning the
next.

**The work:**

1. Highlight-to-search: select text on the page, filter the reference
   panel to it. No persistence, no new storage — selection in,
   `filterReferenceContent()` out.
2. Build-time term links: every later occurrence of a taught term links
   quietly back to its introduction, so "where did I meet this?" is
   answerable from anywhere. For returners after a break, re-finding is
   the need.
3. Only after both have lived for a while: gentle retrieval prompts —
   the reference surfacing terms met some tutorials ago, phrased
   invitationally, never as a score.

**Open questions:**

- **How is a term matched in prose?** Exact string only, or inflected —
  does "matrices" link back to *matrix*? *Assumed:* exact match plus a
  hand-written `forms:` list in the glossary YAML where a term needs
  one, rather than a stemmer that will guess wrong in maths prose.
  *Cost:* small; the glossary format grows one optional field.
- **How much linking before prose gets noisy?** *Assumed:* first
  occurrence per section only, styled as quietly as the existing
  italics. *Cost:* a rendering rule, changeable freely.
- **Persistent highlighting: in or out?** Out, for now, and worth
  recording why: highlights need anchors that survive a version
  release, cell ids give that to code but prose has none, and an
  anchoring scheme (paragraph fingerprinting or similar) is real work.
  The moment one exists, highlighting, margin notes, and
  reflection-answer boxes all become cheap — so the right question is
  "is a prose anchoring scheme worth building," asked once, not three
  separate feature questions. *Blocks:* nothing in this phase.
- **What do retrieval prompts look like concretely?** Deliberately not
  designed here. Judge after step 2 ships whether the reference panel
  is the right home or whether it belongs on the contents page.

---

## Phase 6 — One workspace, and the edges

The addendum in `MINI_IDE_AND_DEWMINI_NEXT.md` records the decision:
dewmini absorbs Mini IDE's capabilities and keeps its own smaller style;
Mini IDE retires at parity. Until then, three hand-maintained page
chromes and three stylesheets carry one visual system — so no polish on
Mini IDE between now and convergence.

**The work:**

1. **Done.** A written parity checklist (files, uploads, SQLite,
   notebook import, Stop), then dewmini gained each item in its own
   style (`DECISIONS_LOG.md` 7.87–7.89). The one item left off that
   original checklist — an offline, downloadable copy of the tool
   itself, not just a student's own notebook — landed separately once
   Mini IDE's retirement made it stop being optional
   (`DECISIONS_LOG.md` 7.92), and surfaced a real bug in *both* offline
   bundles' core promise along the way: neither could actually be
   opened by double-clicking, only served locally, something nothing
   had tested until building dewmini's own bundle did.
2. **Done.** Mini IDE retired (`DECISIONS_LOG.md` 7.91) — its hosted
   URL redirects to dewmini; its app survives, unlinked, only as the
   source for a still-offered offline download. Collapsing toward one
   stylesheet for the shared chrome did not turn out to be part of
   this step: dewmini and the tutorial pages already shared
   `tutorial-style.css`'s own tokens and `.dl-*` classes before
   retirement, and Mini IDE's own stylesheet (`assets/mini-ide-style.css`)
   only needs to keep working for its offline-only copy now, not to
   converge with anything live — nothing forces that collapse to
   happen at all unless a real reason to touch that file shows up.
3. The edges audit, which is the equity work: the site on a phone
   end-to-end, a screen-reader pass, and a proof that the offline
   bundle boots with the network off on a fresh machine — currently
   asserted, not tested.

**Open questions:**

- **Does dewmini take the Worker engine?** *Decided, and done*
  (`DECISIONS_LOG.md` 7.89): yes — the identity worth keeping was the
  smaller surface, not the older plumbing. The separable client became
  `assets/pyodide-engine.js`, shared rather than duplicated, exactly as
  this entry's *cost to change* anticipated.
- **What happens to Mini IDE's URLs and downloaded bundles?**
  *Decided, and done* (`DECISIONS_LOG.md` 7.91): the hosted page is now
  a short redirect-with-explanation; the offline download keeps working
  as a self-contained artifact, produced from a renamed copy of the
  original app kept for exactly that purpose.
- **Offline proof: manual or CI?** *Partly answered:* a manual pass
  (`DECISIONS_LOG.md` 7.92) served both bundles with *serve.py* and ran
  a real interrupt-a-`while True`-loop Stop-button test against each,
  plus a `load_csv()` call against dewmini's own bundled `data/` — real
  proof the *served* bundle works, not yet proof it works with the
  network fully off (both tests still reached a locally-vendored Pyodide
  over HTTP, not the bundle's own `assets/vendor/pyodide/`, which
  neither test environment had populated). *Still assumed:* a
  `MANUAL_CHECKLIST.md` entry per release for the fully-offline case
  specifically; a CI job that serves a bundle with outbound network
  blocked if the manual check ever gets skipped.
- **What is the screen-reader baseline?** Which reader and browser
  pairs count as "tested"? *Assumed:* VoiceOver/Safari and NVDA/Firefox,
  as the pair a Dublin classroom is most likely to contain. Worth a
  minute of anyone's disagreement before it hardens into fact.

---

## What this file is not

Not a promise and not a schedule — phases ship independently and can be
stopped or reordered after any of them. The one hard dependency is that
Phase 5's term-linking wants Phase 2's glossaries written. And not a
place where questions get answered: when one is decided, the answer
moves to `QUESTIONS.md` and `DECISIONS_LOG.md`, and this file just says
so.
