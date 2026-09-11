# Bringing dewstack's courses into dewlab

Written 2026-09-10, at Josh's request, as the plan for retiring `dewstack`
as a separately-hosted site and making Database Methods (5N0783) and Web
Authoring (5N1910) dewlab modules instead. The two module folders this
work fills are not new: `tutorials/database-methods/` has sat empty since
the FOOP module shipped (`planning/ROADMAP.md`, "`database-methods` has
no outcomes written... stays, empty, until its tutorials are written"),
and the homepage already carries "Coming soon — see the earlier version
on dewstack" cards for both (`build.py`, the module-card list, ~line
2270). This document is what actually closes that gap.

## 1. What "merge" means here

Not a repository merge. `deweydex/dewstack` and `deweydex/dewlab` share no
code today, by a decision Josh made explicitly on 2026-09-06 and that
both repos' planning docs record (`DECISIONS_LOG.md` here, and
`planning/CELL_HINTS.md` §7 in dewstack): dewstack's `sql-cell.js` was
built by reading dewlab's `pyodide-engine.js` and reimplementing its
behaviour, not by importing it. "Port in shape, not code" is the standing
rule between the two repositories, and this merge extends it one more
time rather than breaking it: dewstack's content and design get rebuilt
inside dewlab's own conventions, and dewstack itself stops being the
place new work happens, the same way `sources/wadb/` and
`sources/playground/` inside dewstack itself are read from and never
edited once their replacements exist.

Two traps carry over from each repo's own CLAUDE.md and matter more here
than in ordinary work, because dewstack already has real students:

- **A dewstack slug is a contract.** `a-page-is-files`,
  `first-database`, and every other dewstack slug is the address a
  bookmark or a returning student uses. Ported tutorials keep their
  dewstack slugs as their dewlab slugs. A slug changes only where dewlab's
  own convention forces it (module folder renamed, e.g. `data` becoming
  `database-methods`), never by editorial preference.
- **A dewlab cell id is a contract the moment a class has seen it.**
  Every ported `python exec`/`sql exec` block gets a real, permanent
  `id:` on the header the first time it's written into dewlab, chosen
  with the same care as a new tutorial's own cells, because there is no
  second chance to rename it later without discarding saved work.

## 2. Scope: what actually moves, and what doesn't yet

dewstack's own ledger (`dewstack/planning/CONSOLIDATION_PLAN.md` §7) shows two
tracks finished to a "done" bar that already matches dewlab's own —
plain-language pass, glossary, `cell-code-review`, axe and 1200/390px
screenshots:

- **`data` module → dewlab's `database-methods`.** 12 pages:
  `a-table-is-a-list-of-rows`, `designing-a-table-before-you-build-it`,
  `loading-a-real-dataset`, `asking-questions-of-a-table`,
  `charting-a-querys-result`, `a-form-that-writes-a-row`,
  `changing-what-is-in-it`, `exporting-a-query-to-a-file`,
  `a-second-table-and-a-join`, `joining-two-real-tables`,
  `sql-practice`, `the-tentacular-plushies-quiz`.
- **`web` module → dewlab's `web-authoring`** (new folder; no
  reservation exists yet, so it's created fresh). 30 pages, Arc 1
  (concept pages: the box, selectors, flexbox, grid, and so on) and Arc 2
  (the `several-pages` series: navigation, forms, media queries, a-grid
  gallery, and the rest).

Two pieces are explicitly **not** in this pass:

- **`full-stack`** has one page on dewstack
  (`a-page-that-reads-from-a-database`) and dewlab has no full-stack
  concept at all yet. Combining SQL and web authoring needs both tracks
  live first. Left for a later phase (§7, Phase 4).
- **`getting-started` and `reference`** on dewstack teach a GitHub-Pages
  authoring workflow (a GitHub account, an editor, "the two loops",
  publishing) that is genuinely different content from dewlab's own
  Python-and-Pyodide `getting-started` module — not a duplicate to
  reconcile, but not obviously part of "Web Authoring and Databases"
  either. This is a real open question (§8), not decided by this plan,
  because it changes how big the ported curriculum is and touches
  dewlab's front page. Left out of the staging copy-in's first pass;
  added once Josh has ruled on it.

`javascript` is dewstack's own unwritten module — nothing to port.

## 3. The engine gap, honestly measured

**Data/SQL: smaller than it looks.** dewlab already runs real SQL: the
Worker-based `assets/pyodide-engine.js` and `assets/tutorial_tools.py`'s
`_run_sql_cell(conn, script, max_rows=20)` back dewmini's own SQL cell
type today (`tests/e2e/test_dewmini_workbench.py`). What's missing is a
*tutorial-page* surface for it: `build.py` has no SQL fence kind (only
`python exec` exists there), and `tutorial-runtime.js` has no rendering
for one. This is extending an engine that exists, not building one.

**Revised, against §8's own original assumption:** dewstack's `sql
cell=<name>[ persist]` and separate `sql-check db=<name> task=<name>`
fences (`dewstack/build.py` `SQL_BLOCK`/`SQL_CHECK_BLOCK`) turned out, on
reading them closely while building this, to be a different *grammar*,
not just a different spelling — a per-cell named database (several
databases can coexist on one page), a `persist` flag controlling
`localStorage`, and a check that runs a hand-written `check_*` Python
function named by `task=`, with no code of its own. dewlab's own cell
model is a single shared `_page_globals` namespace (one `db`, the same
one every cell, matching what `_run_sql_cell()` and dewmini already
assume), `id:`/`hint:`/`expect:` header lines identical to every
`python exec` cell, and a generic `check()` that already compares
DataFrames via `_compare()` — no per-task function needed. Copying
dewstack's grammar verbatim would mean two incompatible fence dialects
inside one file format, which is a worse outcome than dewstack's own
two-repository compromise ever had to solve for, now that there is only
one repository. **The fence is `sql exec`, not `sql cell=`**, reusing
`parse_cell()`'s existing header-line grammar unchanged — the SQL text
simply takes the place `python exec`'s Python code takes, and the editor
holds real SQL, not a wrapped Python call (see §3's engine section for
how that wrapping happens at runtime instead). This is the one place
this document's original assumption changed after actually reading the
other repository's code closely enough to implement against it — worth
flagging precisely because it reverses something written down earlier as
settled.

**Web authoring: a genuine gap.** dewlab has no sandboxed-iframe,
live-HTML/CSS-run-on-demand-JS pattern anywhere in a tutorial page today.
dewstack's `dewstack/assets/site-editor.js` (18.8K) is the design to port: HTML
and CSS panes rebuild the preview live; the JS pane runs on a Run click;
errors relay from the iframe's console with a line number and a
plain-language second line (`SITE_FRIENDLY` mapped errors, per
`DECISIONS_LOG.md`'s account of the original build). This needs new
`build.py` fence kinds (`site=`, `html app=`/`css app=`/`js app=`,
matching dewstack's spelling for the same reason as above) and a new
runtime file — working name assets/site-runtime.js, not yet created —
built against dewlab's manifest/report-doors conventions rather than
dewstack's.

The JS execution piece of this should not be built twice. dewlab already
has a sandboxed JS runner for JS cells in dewmini
(`compose/js-cell-engine.js`, `<iframe sandbox="allow-scripts">`, no
Worker). The web-authoring engine's JS pane should share that file or a
lightly generalised version of it, rather than dewstack's separate JS
console-relay code being reimplemented a third time.

## 4. dewmini and dewminiweb

dewlab already decided a version of this question once, for a narrower
case, in `planning/MINI_IDE_AND_DEWMINI_NEXT.md`: Mini IDE and dewmini
were two Python notebooks solving the same problem for two audiences, and
the eventual answer was not "keep both" but "one absorbs the other,"
because keeping two tools with overlapping purpose meant every shared fix
landing twice and drifting (the output-rendering bug that hit only one of
them is the example the document leads with).

That reasoning doesn't transfer here, because the situation is different
in the one way that mattered: dewmini and a Web Authoring workspace don't
share a purpose. One is a Python-and-SQL notebook; the other is a
multi-file site (HTML, CSS, JS) with a live preview — a different
interaction shape, not a lighter or heavier version of the same one.
Forcing site-authoring into dewmini's cell-by-cell notebook UI would cost
real usability for no shared benefit; keeping them as two products is the
version of §4's own test ("does this serve a genuinely different use
case") that comes out the other way this time.

**Recommendation: two products.**

- **dewmini** stays exactly what it is — the Python-and-SQL notebook —
  and gains nothing from this merge except, eventually, the `sql cell=`
  tutorial-page fence reusing the same `_run_sql_cell()` it already
  calls.
- **dewminiweb** (working name, per Josh's own suggestion) is a new,
  standalone site-authoring workspace, built to the shape of dewstack's
  `dewstack/assets/workspace.js` (multi-file HTML/CSS/JS, a file concept,
  no notebook cells) rather than dewstack's in-tutorial `site-editor.js` —
  the same relationship dewmini has to tutorial Python cells.

What does carry over from the dewmini precedent is its other half: share
the engine underneath even when the products stay separate.
`dewminiweb`'s JS execution reuses `compose/js-cell-engine.js`; if it
ever offers a SQL pane (dewstack's `dewstack/assets/workspace.js` doesn't
appear to have one — worth confirming before promising it), that reuses
`pyodide-engine.js`/`tutorial_tools.py` too, the same as dewmini and the
new tutorial-page SQL cells will.

This is a product-shape call, not an engineering one, and it is Josh's
to confirm before `dewminiweb` gets built — see §8. Nothing in the
staging phase or the data-track work depends on the answer.

## 5. Staging: what it is, and what it deliberately isn't

`staging/dewstack-import/` at the dewlab repo root — not under
`tutorials/`, so `build.py`'s glob never touches it and nothing it
contains is live, linked, or built.

It holds a **verbatim, unedited copy-in**, taken from a named dewstack
commit, of:

- `dewstack/tutorials/data/` and `dewstack/tutorials/web/` in full
  (markdown, glossary files, `.order.yaml`s, images).
- `dewstack/tutorials/full-stack/` (the one page, for later reference).
- The relevant slice of `dewstack/tutorials/modules.yaml` (the
  `data`/`web` ordering and notes).
- The five engine source files: `dewstack/assets/site-editor.js`,
  `dewstack/assets/sql-cell.js`, `dewstack/assets/sql_tools.py`,
  `dewstack/assets/python_tools.py`, `dewstack/assets/workspace.js`.
- `dewstack/planning/CONSOLIDATION_PLAN.md` and
  `dewstack/planning/NEXT_STEPS.md`, for the ledger and rationale behind
  what's already "done."

A short `staging/dewstack-import/README.md` records the exact commit
hash it was taken from and what it's for, so nobody mistakes it for a
live copy or tries to build from it directly.

What it isn't: a place to edit. Every file in it gets read from while the
real port happens directly in `tutorials/database-methods/`, a new
tutorials/web-authoring/ folder, and new `assets/` files — never edited
in place inside staging, and never the thing a pull request ships. Once a
module's port is done and running in front of a class, its slice of
staging is deleted. dewstack's own copy stays untouched in its own
repository throughout — this plan never asks dewstack to delete
anything, matching its own "nothing moves by deletion" rule.

## 6. What "done" means for a ported page

The same bar dewstack already used, since it's dewlab's own bar too:

1. Content through `planning/PEDAGOGICAL_STYLE_GUIDE.md` §4's plain
   language checks (the two repos already share this guide by
   reference — dewstack's own CLAUDE.md points back here for it), even
   where the dewstack original already passed dewstack's copy of the same
   check, because the guide has moved since some of that content was
   written.
2. A glossary file, run through the `tutorial-glossary` skill.
3. A `cell-code-review` pass on every exec cell.
4. Real cell ids, chosen fresh, not copied from any internal dewstack
   naming.
5. An accessibility and 1200px/390px screenshot check.
6. A row in this document's own ledger (§9) recording it.

## 7. Phased rollout

1. **Staging copy-in.** Populate `staging/dewstack-import/` as described
   in §5. No `build.py` changes, no tutorial changes, nothing
   student-visible. Reversible by deleting a folder.
2. **Data engine + module.** **Engine done** (DECISIONS_LOG.md 7.140): a
   `sql exec` fence in `build.py` and `tutorial-runtime.js`, calling the
   existing `_run_sql_cell()`, verified end to end in a real browser
   against a real Pyodide with no tutorial content using it yet. Still to
   do: port the 12 pages into `tutorials/database-methods/` through §6's
   checklist, preserving dewstack's slugs; add the QQI outcome
   descriptors 5N0783 needs to `planning/curriculum/outcomes.yaml`
   (currently absent — `planning/ROADMAP.md` already flags this gap);
   flip the homepage card once the module has run in front of a class.
3. **Web engine + module.** Resolve the dewmini/dewminiweb question
   (§8). Build the site-authoring fence kinds and a new site-runtime.js
   for tutorial pages; build `dewminiweb` if confirmed. Port the 30 web
   pages into a new tutorials/web-authoring/ folder the same way. Flip
   its homepage card.
4. **Full-stack, later.** Combine dewstack's one page with whatever
   dewlab's own full-stack concept becomes, once both tracks are live.
   Not scheduled yet.
5. **Cutover.** Both dewlab homepage cards point at real pages instead of
   dewstack. dewstack's own front page (`dewstack/tutorials/front.md`)
   gets a note pointing the other way — "the current version of this
   course is on dewlab" — in the same spirit as its `notes.web` line about
   WADB_Tutorials today. `staging/dewstack-import/` is deleted once
   nothing in it is still being read from. dewstack's repository and
   history are not deleted or archived by this plan; that stays a
   separate decision for whenever Josh judges the replacement has been in
   front of enough classes.

## 8. Questions that are Josh's, not this plan's, to settle

1. **`dewminiweb`'s scope and name.** Confirmed direction: a separate
   product from dewmini, shaped like dewstack's `workspace.js`. Not yet
   confirmed: the actual name (working name only), and whether it ships
   in the same pass as the web-authoring tutorial pages or trails them.
2. **`getting-started`/`reference` from dewstack.** Fold into the ported
   modules as prerequisite pages, leave linked to the still-live dewstack
   pages indefinitely (dewstack's own `notes.web` line already does this
   for WADB_Tutorials), or write new dewlab-native equivalents. Affects
   scope and the front page, not just these two modules.
3. **Fence-kind spelling — resolved for SQL, still open for web.** §3
   now settles the SQL side: `sql exec`, dewlab's own `id:`/`hint:`
   grammar, one shared `db`, generic `check()` — not dewstack's `sql
   cell=`/`sql check=`, once reading that grammar closely showed it was a
   different cell-identity model, not just different words. The web
   fences (`site=`, `html app=`/`css app=`/`js app=`) haven't been read
   as closely yet — worth checking whether the same thing is true of
   them before assuming their spelling carries over unchanged, rather
   than repeating this document's own first mistake on the SQL side.
4. **dewstack's eventual fate.** Out of scope for this plan, noted so it
   isn't forgotten: once both modules are live and have run in front of a
   class, does dewstack's repository stay up as a read-only archive
   indefinitely, or does something happen to it? Not a question this
   document answers.

## 9. Ledger

| Module | Staged | Engine built | Ported | Live |
|---|---|---|---|---|
| `database-methods` (5N0783) | done | done, merged to `main` (`sql exec`, DECISIONS_LOG.md 7.140, PR #172) | done — 12 tutorials, QQI mapping, verified in a real browser (DECISIONS_LOG.md 7.141) | pending PR review |
| `web-authoring` (5N1910) | done | not yet | not yet | not yet |
| `full-stack` | done (reference only) | — | — | — |

Update this table as each phase in §7 completes.
