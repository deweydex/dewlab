# Bringing dewstack's courses into dewlab

Written 2026-09-10, at Josh's request, as the plan for retiring `dewstack`
as a separately-hosted site and making Database Methods (5N0783) and Web
Authoring (5N1910) dewlab modules instead. The two module folders this
work fills are not new: `tutorials/database-methods/` has sat empty since
the FOOP module shipped (`planning/ROADMAP.md`), and the homepage already
carries "Coming soon — see the earlier version on dewstack" cards for
both (`build.py`, the module-card list, ~line 2270). This document is
what actually closes that gap.

## 1. What "merge" means here

Not a repository merge. `deweydex/dewstack` and `deweydex/dewlab` share no
code, by a decision Josh made explicitly on 2026-09-06 and that both
repos' planning docs record (`DECISIONS_LOG.md` here, and
`planning/CELL_HINTS.md` §7 in dewstack): dewstack's `sql-cell.js` was
built by reading dewlab's `pyodide-engine.js` and reimplementing its
behaviour, not by importing it. "Port in shape, not code" is the standing
rule between the two repositories, and this merge extends it: dewstack's
content and design get rebuilt inside dewlab's own conventions, and
dewstack itself stops being the place new work happens, the same way
`sources/wadb/` and `sources/playground/` inside dewstack itself are read
from and never edited once their replacements exist.

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
  authoring workflow, genuinely different content from dewlab's own
  Python-and-Pyodide `getting-started` module. **Settled (§8): fold both
  in whole, copied across rather than rewritten from scratch, filed under
  the `web-authoring` module** (and, once it exists, `web-dev`) rather
  than merged into dewlab's own `getting-started`.

`javascript` is dewstack's own unwritten module — nothing to port.

## 3. The engine gap, honestly measured

**Data/SQL: smaller than it looks.** dewlab already runs real SQL: the
Worker-based `assets/pyodide-engine.js` and `assets/tutorial_tools.py`'s
`_run_sql_cell(conn, script, max_rows=20)` back dewmini's own SQL cell
type today (`tests/e2e/test_dewmini_workbench.py`). What's missing is a
*tutorial-page* surface for it: `build.py` has no SQL fence kind, and
`tutorial-runtime.js` has no rendering for one — extending an engine that
exists, not building one.

dewstack's own `sql cell=<name>[ persist]` and `sql-check db=<name>
task=<name>` fences (`dewstack/build.py` `SQL_BLOCK`/`SQL_CHECK_BLOCK`)
are a different *grammar*, not just a different spelling: a per-cell
named database, a `persist` flag controlling `localStorage`, and a check
that runs a hand-written `check_*` function named by `task=`. dewlab's
own cell model is a single shared `_page_globals` namespace (one `db`,
matching what `_run_sql_cell()` and dewmini already assume),
`id:`/`hint:`/`expect:` header lines identical to every `python exec`
cell, and a generic `check()` that already compares DataFrames via
`_compare()`. Copying dewstack's grammar verbatim would mean two
incompatible fence dialects inside one file format. **The fence is
`sql exec`, not `sql cell=`**, reusing `parse_cell()`'s existing
header-line grammar unchanged — the SQL text takes the place `python
exec`'s Python code takes, and the editor holds real SQL rather than a
wrapped Python call.

**Web authoring** turned out to differ in both directions from the
original assumption. dewlab already has almost all of the live-preview
mechanics — just not on a tutorial page. dewmini's Site tab
(`compose/dewmini.js`, `openSiteFile()`/`renderSiteView()`) is exactly
this pattern: a sandboxed `srcdoc`
iframe (`sandbox="allow-scripts"`, no same-origin), an HTML/CSS live
rebuild with JS on a Run click, a console relayed from inside the frame
with four plain-language error mappings (`SITE_FRIENDLY`), a
single-document-in-flight coalescing flush with a watchdog.
`dewstack/assets/site-editor.js` was ported from it in shape on
2026-09-04 (`CONSOLIDATION_PLAN` §13), and dewstack's own later addition —
the console and the Run-vs-live split for JS — was ported back into
dewmini on 2026-09-06. The relay to reuse for
the tutorial-page component is the one already living in
`dewmini.js:1349-1379` — not `compose/js-cell-engine.js` (dewmini's
separate JS-cell type, a different feature) and not a third independent
copy.

The genuine, forced gap: dewmini's `renderSiteView()` is a singleton over
module-level state — it can show one site at a time. A tutorial page
needs several independently live editors on one page (dewstack's own
`position-and-the-sticky-header.md` ships two), and identity has to come
from the fence itself rather than a mounted filesystem path. dewstack
solved both with a per-instance `mount(el, opts)` and an `editors`
registry (`site-editor.js`) — itself already ported in shape from
dewmini once, so dewlab's tutorial-page version is built the same way, a
second application of the same rule rather than a new one.

But dewstack's fence spelling still can't be copied, for the same reason
as SQL: `site=name` puts the site's identity in the fence's own info
string, and dewlab's Crepe-based authoring editor keeps only the *first
word* of a fence's info string on a round trip (`ARCHITECTURE.md` §3,
"The authoring editor"); every other exec fence survives this by
recovering its tag from an `id:` header line written *inside* the fence
(`assets/editor.js`'s `restoreExecTag()`). A `site=name` fence has
nothing inside it to recover from — every `html site=hero` block edited
through dewlab's own authoring page would silently come back as inert,
illustrative HTML the moment an author saved.

**The fence, decided:** an `id:`-bearing header, same grammar every other
exec-family fence already uses, with an explicit grouping key rather than
name-in-the-info-string:

    ```html site
    id: hero-markup
    site: hero
    <button>Hover me</button>
    ```

    ```css site
    id: hero-style
    site: hero
    .btn { ... }
    ```

Consecutive fences sharing a `site:` value group into one editor, the
same adjacency rule dewstack's own `site=` enforces (`build.py`'s
consecutive-run walk), so the source still reads as the student's whole
site at a glance. Panes stay optional (most of dewstack's own 27 web
pages are HTML+CSS only); `renderSiteView()`'s always-three-panes habit
doesn't carry over. `js site` fences get a Run button and console;
`html site`/`css site` stay live.

**Engine shape:** a new, instantiable version of dewmini's Site view —
`mount(container, {html, css, js})` returning `{run, destroy}` — built in
`assets/tutorial-runtime.js`, sharing the relay/friendly-map/document-assembly
code already sitting in `dewmini.js` rather than copying it a third time
(within one repository that means actually extracting it to a shared file
both `compose/dewmini.js` and `tutorial-runtime.js` import — "port in
shape" is the rule for the boundary between the two *repositories*, not
within one). One bug fixed in the same pass: dewmini's document assembly
(`buildSiteDocument()`) was missing `<base href="about:srcdoc">`, which
dewstack's copy has — without it, a relative link inside a dewmini site
preview navigates the dewmini page itself instead of the frame.

**dewmini web, by contrast, is the easy side of this.** Measured against
dewmini's *existing* Site tab and its own multi-notebook store
(`dewmini:notebooks:v1`, already shaped like dewstack's
`dewstack:workspace:v1`), what's missing is small and additive: freeing a
site's display name from its filename, "load files in" from the local
machine, "download these files" out, the preview-width slider. No new
identity model, no instancing refactor.

## 4. dewmini and dewmini web

`planning/MINI_IDE_AND_DEWMINI_NEXT.md` already answered a version of
this question for a narrower case: Mini IDE and dewmini were two Python
notebooks solving the same problem for two audiences, and the eventual
answer was not "keep both" but "one absorbs the other," because keeping
two tools with overlapping purpose meant every shared fix landing twice
and drifting.

That reasoning doesn't transfer here: dewmini and a Web Authoring
workspace don't share a purpose. One is a Python-and-SQL notebook; the
other is a multi-file site (HTML, CSS, JS) with a live preview — a
different interaction shape, not a lighter or heavier version of the same
one. Forcing site-authoring into dewmini's cell-by-cell notebook UI would
cost real usability for no shared benefit.

**Recommendation: two products.**

- **dewmini** stays exactly what it is — the Python-and-SQL notebook —
  and gains nothing from this merge except, eventually, the `sql cell=`
  tutorial-page fence reusing the same `_run_sql_cell()` it already
  calls.
- **dewmini web** (named by Josh, 2026-09-11: "we can always change it
  later") is a new, standalone site-authoring workspace, built to the
  shape of dewstack's `dewstack/assets/workspace.js` (multi-file
  HTML/CSS/JS, a file concept, no notebook cells) rather than dewstack's
  in-tutorial `site-editor.js` — the same relationship dewmini has to
  tutorial Python cells.

What carries over from the dewmini precedent is its other half: share the
engine underneath even when the products stay separate. `dewmini web`'s
JS execution reuses `compose/js-cell-engine.js`; if it ever offers a SQL
pane (dewstack's `dewstack/assets/workspace.js` doesn't appear to have
one — worth confirming before promising it), that reuses
`pyodide-engine.js`/`tutorial_tools.py` too, the same as dewmini and the
new tutorial-page SQL cells.

This is a product-shape call, not an engineering one, and it is Josh's to
confirm — see §8. Nothing in the staging phase or the data-track work
depends on the answer.

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
`tutorials/web-authoring/` folder, and new `assets/` files — never edited
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
2. **Data engine + module — done.** A `sql exec` fence in `build.py` and
   `tutorial-runtime.js`, calling the existing `_run_sql_cell()`; the 12
   pages ported into `tutorials/database-methods/` through §6's
   checklist, preserving dewstack's slugs, with the QQI outcome
   descriptors 5N0783 needs added to `planning/curriculum/outcomes.yaml`;
   the homepage card flipped and live. See the ledger (§9).
3. **Web engine, `dewmini web`, and all 42 web-authoring pages — done.**
   The engine half: `html site`/`css site`/`js site` fence kinds, and
   `assets/site-relay.js` as the shared live-preview engine underneath a
   tutorial's own site editor, dewmini's Site tab, and `dewmini web` too.
   `dewmini web` itself — the standalone workspace, shaped like
   dewstack's `workspace.js` — is built: several named sites, HTML/CSS/JS
   panes, a live preview, load-files-in and download-files-out, linked
   from the homepage. §8 q1 is answered: it exists, so the tutorial pages
   can honestly promise the same "open this in the workspace" hand-off
   dewstack's own pages offer. `getting-started`/`reference` are done —
   twelve pages folded in whole under `web-authoring` (§8 q2), the
   `welcome` and `shelf` series, with the platform-specific facts they
   named (dewlab's own repository and a real dewlab PR in place of
   dewstack's, the actual uniform save/reset model in place of dewstack's
   "Your table" special case) corrected rather than carried over unread.
   The 30 lesson pages are done too, the `first-site` and
   `several-pages` series — porting live content into the engine found a
   real gap: the preview-width slider dewstack's own site editor has and
   the engine's port never grew, plus a side-by-side editor/preview split
   too narrow to demonstrate a realistic media-query breakpoint. Both
   fixed.

   QQI 5N1910 mapping — done, once Josh supplied the actual descriptor.
   All fourteen outcomes are in `outcomes.yaml` and `topics.yaml`; 40 of
   the 42 pages carry `covers:`/`touches:` frontmatter (`faq` and
   `issues-and-pull-requests` genuinely teach nothing on the list). Ten
   of the fourteen codes land on real content; WA-LO1 (HTML/CSS version
   history), WA-LO5 (desktop publishing/CMS tools) and WA-LO12 (code
   generators) have no dewlab equivalent, the same honest shape as
   DBM-LO1. `topic-groups.yaml`'s reachability groups stay in place
   alongside the outcome map, not instead of it — the two answer
   different questions (§9 of this file, `topics.yaml`'s own header
   comment). Flipping the homepage card still waits on the module
   running in front of a class, the same rule that held
   database-methods' card — it stays "Coming soon" until then.
4. **Full-stack — done.** `html app`/`css app`/`js app`, a new cell kind
   beside the site editor rather than a third site-pane language, since a
   site editor's sandboxed iframe exists specifically to stop a reader's
   script reaching anything else on the page, and this needed exactly
   that channel — the page's own shared `db`. `DECISIONS_LOG.md` 7.148
   has the design: the `_query_rows()`/`queryRows()` bridge across the
   Worker boundary, why it is a separate cell kind, and two
   authoring-editor round-trip gaps (site fences and app fences both)
   closed together in the same pass. One page ported from dewstack's
   staged reference, in shape rather than copied — dewlab's single
   shared connection drops the per-cell database name dewstack's
   `dlQuery(name, sql, params)` needed and this does not. No QQI mapping;
   none exists for this module, the same honest gap `covers:` leaves open
   elsewhere rather than inventing one.
5. **Cutover.** Both dewlab homepage cards point at real pages instead of
   dewstack. dewstack's own front page (`dewstack/tutorials/front.md`)
   gets a note pointing the other way — "the current version of this
   course is on dewlab." `staging/dewstack-import/` is deleted once
   nothing in it is still being read from. dewstack's repository and
   history are not deleted or archived by this plan; that stays a
   separate decision for whenever Josh judges the replacement has been in
   front of enough classes.

## 8. Questions that are Josh's, not this plan's, to settle

1. **`dewminiweb`'s scope and name — settled 2026-09-11, and built the
   same day.** Named **"dewmini web"** (working name, Josh: "we can
   always change it later"). A separate product from dewmini, shaped like
   dewstack's `workspace.js` rather than its in-tutorial `site-editor.js`
   — the same relationship dewmini has to tutorial Python cells. It
   shipped ahead of the web-authoring tutorial pages, resolving the
   sequencing question in the way §3's SQL lesson predicted: the engine —
   and now the standalone workspace built on it — exists before any
   tutorial page promises a hand-off into it.
2. **`getting-started`/`reference` from dewstack — settled 2026-09-11,
   and built the same day.** Folded in whole rather than left linked to
   dewstack or rewritten from scratch — Josh: "I think we can literally
   copy paste there." Filed under the `web-authoring` module (and, once
   it exists, `web-dev`), not merged into dewlab's own `getting-started`,
   which teaches a different thing (Python/Pyodide, not a GitHub-Pages
   authoring workflow). "Copy paste" still meant dewlab's own conventions
   applied on the way in — the plain-language pass, dewlab's own
   frontmatter shape — the same "port in shape, not code" rule §2 already
   applies, and "in shape" turned out to include the platform-specific
   facts these pages named about themselves, not only their prose
   register. No `covers:` frontmatter after all: nothing here teaches a
   QQI 5N1910 outcome, so `topic-groups.yaml` carries the reachability
   these pages need instead.
3. **Fence-kind spelling — resolved for SQL, and now resolved for web
   too, 2026-09-11.** §3 has the full comparison for both: `sql exec`
   over `sql cell=`/`sql check=`, and the `id:`/`site:`-header grammar
   over `site=name`, in each case because dewstack's spelling assumed a
   cell-identity model dewlab's authoring editor can't round-trip.
   dewmini's existing Site tab code is reused for the relay/console/preview
   layer, refactored to be instantiable per editor rather than the
   singleton it is today.
4. **dewstack's eventual fate.** Out of scope for this plan, noted so it
   isn't forgotten: once both modules are live and have run in front of a
   class, does dewstack's repository stay up as a read-only archive
   indefinitely, or does something happen to it? Not a question this
   document answers.

## 9. Ledger

| Module | Staged | Engine built | Ported | Live |
|---|---|---|---|---|
| `database-methods` (5N0783) | done | done, merged to `main` (`sql exec`) | done — 12 tutorials, QQI mapping | done — merged to `main` |
| `web-authoring` (5N1910) | done | done, merged to `main` (`html site`/`css site`/`js site`, `assets/site-relay.js`; `dewmini web` standalone workspace; preview-width slider + stacked site-editor layout) | done — all 42 pages (`getting-started`/`reference`, `first-site`, `several-pages`); QQI 5N1910 mapping done too | not yet — homepage card stays "Coming soon" until the module has run in front of a class |
| `full-stack` | done (reference only) | done — `html app`/`css app`/`js app`, `_query_rows()`/`queryRows()` Worker bridge (`DECISIONS_LOG.md` 7.148) | done — 1 of 1 staged page (`a-page-that-reads-from-a-database`), no QQI mapping (none exists for this module) | not yet — no homepage card until the module has run in front of a class |

Update this table as each phase in §7 completes.
