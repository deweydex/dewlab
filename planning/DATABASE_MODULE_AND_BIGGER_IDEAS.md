# A database module, and the bigger things Jupyter does badly

A companion to `planning/JUPYTER_FEATURES_NEXT.md`. That document covers five
small-to-medium features borrowed from Jupyter. This one covers the larger,
more speculative ground: where the notebook *form* fails, what a database
module specifically needs, and what dewlab could do that no notebook does.

Written to be read cold in a different session. Nothing here is
implemented, and nothing here is agreed — it is a set of arguments with the
groundwork checked, offered so the arguing can happen against something
concrete.

**Origin.** Josh, after PR #90 merged: *"are there bigger more elaborate
features that Jupyter also doesn't do well that maybe we could tackle?
What's missing for, for example, a database module that uses Python?"*

---

## 1. The argument this document rests on

A notebook models **values**. You run a cell, something comes back, you look
at it. The whole interface is built around that loop: a cell, its output
beneath it, a namespace of names bound to results.

A database is the opposite kind of thing. It is persistent, mutable, shared
state that outlives any cell and that no cell fully shows you. The value a
cell returns — a DataFrame of twenty rows — is a *photograph* of a corner of
it, taken at a moment, and the notebook then treats that photograph as
though it were the thing.

Jupyter never reconciled those two, and its usual answer is to hand you a
connection object and let the database stay invisible. You cannot see the
schema without querying `sqlite_master` by hand. You cannot see what an
`UPDATE` changed. You cannot undo it. The database is a black box that your
cells poke at.

**The compounding is what makes this urgent rather than merely untidy.** A
notebook already has one source of hidden state: cells run in the order you
pressed Run, not top to bottom, so a namespace can contain things whose
provenance is invisible. Add a database file and there is a second, worse
one — because it survives the restart that would have cleared the first. A
student's notebook works. Neither they nor you can say why. Restarting does
not help, because the `.db` on disk still carries whatever the deleted cell
did to it three sessions ago.

This is why the execution-counter and stale-marker features in
`JUPYTER_FEATURES_NEXT.md` change character here. For a Python notebook they
are good hygiene. For a database notebook they are close to a precondition:
without them, the two kinds of hidden state are indistinguishable from each
other and from an actual bug in the student's SQL.

**The opening.** Every gap above is a gap in the *incumbent*, not only in
dewlab. dewmini is small enough to try a different answer, and it has
already built the mechanism that answer needs — see §3.

---

## 2. Where dewlab actually stands

Checked against `main` at commit `e3229b6`, not recalled.

**The module exists as an empty folder.** `tutorials/database-methods/`
contains no tutorials. `planning/curriculum/outcomes.yaml` carries three
modules — MIT (5N18396), PDP (5N2927), CMPS (5N0554) — and no database
outcomes at all. `tutorials/modules.yaml` lists two modules in its display
order and does not mention it.

This is the good case. The tooling can be designed against the teaching
rather than retrofitted to it, and the outcomes can be written knowing what
the tool will be able to show.

**More SQL support exists than you would guess.**

| | Where |
|---|---|
| `sqlite3` in dewmini's package set | `compose/dewmini.js`, `DM_PACKAGES` (~line 30) |
| `run_query(conn_or_path, sql, params, max_rows, caption)` | `assets/tutorial_tools.py` ~1260 |
| A worked SQL notebook shipped with dewmini | `assets/examples/sql-owid.ipynb` |
| Three-tier persistent filesystem | `compose/dewmini-fs.js`; engine side `assets/pyodide-engine.js` ~900 |
| Namespace introspection crossing the worker boundary | `describe_globals()`, `assets/tutorial_tools.py` ~1366 |

`run_query` opens a short-lived connection if given a path, renders the
result as a table, and returns a DataFrame. The example notebook loads OWID
emissions data, pushes it into an in-memory SQLite database with
`df.to_sql`, and queries it — so the "same data, two languages" framing is
already written and tested.

**Persistence works, with a caveat worth knowing.** The filesystem picks one
of three backends: a real folder the student chose (File System Access API),
OPFS, or IDBFS as a last resort. IDBFS needs an explicit two-way sync —
`assets/pyodide-engine.js` ~644 notes that without calling it, changes exist
only in memory. **A database module leans on this far harder than anything
built so far**, because a `.db` is the first artefact where losing the file
means losing the work rather than losing a cached result. Whoever builds
this should treat "does a `.db` survive a reload on each of the three
backends" as a first-week check, not a late one, and add it to
`tests/MANUAL_CHECKLIST.md`.

**Packages are not a blocker.** Tutorials carry a narrower baseline
(`numpy`, `pandas`, `matplotlib` — `DEFAULT_PACKAGES` in
`assets/tutorial-runtime.js` ~37), but `packages:` in a tutorial's
frontmatter widens it (`docs/WRITING_TUTORIALS.md`), so a database tutorial
can request `sqlite3` without changing the baseline for every page.

**The maths module has already laid the conceptual groundwork**, which I did
not expect and which matters for sequencing. `planning/curriculum/topics.yaml`
already names the database application of five MIT topics:

- **MIT-2.2** (sets) — *"Database queries. A join is an intersection, a union
  is a union"*
- **MIT-2.5** (logic) — *"Search queries and database `WHERE` clauses, where
  the same rewrite can…"*
- **MIT-5.9** — *"Database schema design, which is this decision made
  permanent."*
- **MIT-6.3** (collections) — *"rows from a database, pixels in an…"*
- **MIT-6.8** (searching and sorting) — *"Understanding why a database index
  exists, and what it costs."*

Two consequences. The database module's `needs:` edges can point at real
existing topics rather than starting a disconnected island — which means the
beginner/intermediate/advanced facets from `DECISIONS_LOG.md` 7.101 will
band its terms correctly with no extra work, since those are derived from
prerequisite depth. And the module has an argument for existing beyond
vocational necessity: it is where several maths ideas stop being abstract.

---

## 3. The mechanism that makes most of this cheap

`describe_globals()` is the pattern to copy, and it is worth understanding
before reading the proposals.

It runs **in Python**, inside the worker, and returns a list of
`{name, type, summary, kind}` dictionaries — deliberately all strings, so
the result crosses `postMessage` as plain data with none of Pyodide's proxy
machinery involved. The JavaScript side renders it and knows nothing about
Python objects. It is unit-testable under CPython because it is ordinary
Python taking ordinary values.

Every database-inspection idea below is the same move pointed at SQLite
instead of at the namespace: a `describe_database(conn)` in
`assets/tutorial_tools.py` returning plain dictionaries, a renderer in
`compose/dewmini.js`, and a section in the Workbench rail beside Variables
(`compose/dewmini.html` ~356, `#dm-variables-section`).

That is why the schema browser is a couple of days rather than a couple of
weeks. The hard parts — the boundary, the panel, the refresh-after-run hook,
the tests — are built and shipped.

---

## 4. What SQLite gives you, verified

The bolder proposals depend on APIs that either exist or they do not. These
were run rather than assumed (CPython 3.11 / SQLite 3.45 in the authoring
sandbox; **re-confirm under Pyodide's Python 3.13 before relying on them**,
since that is the runtime that matters):

| Capability | Mechanism | Result |
|---|---|---|
| List tables | `select name from sqlite_master where type='table'` | works |
| Columns, types, PK, not-null | `pragma table_info(t)` | works |
| Foreign keys | `pragma foreign_key_list(t)` | works — returns table, from-column, to-column |
| Indexes | `pragma index_list(t)` | works |
| Undo a statement | `savepoint` / `rollback to` | works — deleted rows came back |
| Did this statement write? | `conn.set_authorizer(...)` | works — `SQLITE_SELECT`=21 and `SQLITE_READ`=20 for a read; `SQLITE_UPDATE`=23 appears for a write |
| How many rows changed | `conn.total_changes` | works |
| Query plan | `explain query plan …` | works — e.g. `SCAN book`, `SEARCH author USING INTEGER PRIMARY KEY` |
| Snapshot a database | `conn.backup(other)` | works, including memory-to-memory |
| Dump as SQL | `conn.iterdump()` | present |
| Trace executed SQL | `conn.set_trace_callback()` | present |

The authorizer is the interesting one. It is a hook SQLite calls *before*
executing each operation, with a code saying what kind of operation it is —
so a statement can be classified as reading or writing **before it runs**,
which is what a "this will change your data, are you sure" affordance needs.
It is also a real security mechanism (it can refuse), which means a
read-only mode for a demonstration database is available for free.

---

## 5. The database gaps, largest first

### 5.1 The database has no representation in the interface

**The proposal.** A Schema section in the Workbench rail: tables, their
columns with types, primary and foreign keys, indexes, and row counts.
Refreshed after any statement that wrote. Click a table to see a few rows.

**Why first.** It converts the database from something you interrogate blind
into something you can look at, and every other idea here is easier once the
schema is available as data. It is also the single clearest "we do this,
Jupyter does not" — in Jupyter you write `SELECT name FROM sqlite_master`
like it is 1998, or you install an extension.

**Pedagogically** it does something subtler than convenience. A relational
schema *is* the model of the domain; that is the whole point of MIT-5.9's
"this decision made permanent". A student who can see the schema while
writing a query is being shown that the structure is a designed object with
consequences, rather than an incantation the tutorial gave them.

**Extent.** Medium-small, and mostly assembly. `describe_database(conn)` in
`assets/tutorial_tools.py` using the pragmas in §4, returning plain
dictionaries; a renderer beside `refreshVariables()` in `compose/dewmini.js`;
a section in `compose/dewmini.html` after `#dm-variables-section`.

**Two decisions it forces.** *Which* database — a student may have several
connections open, or none. A picker, or "the most recently used", or every
connection found in the namespace (which `describe_globals()` could report,
since a `sqlite3.Connection` is a namespace value like any other; that last
option is the most elegant and the least obvious). And *when* to refresh:
after every run is simplest, after every write is cheaper, and the
authorizer in §4 tells you which is which.

### 5.2 Nothing shows what a statement changed

**The proposal.** A statement that writes reports what it did. Minimum:
"3 rows changed". Better: which rows, before and after.

**Why.** `SELECT` is safe; `UPDATE` without a `WHERE` is a catastrophe; the
interface currently treats them identically — one renders a table, the other
renders nothing at all, which is *worse* than treating them identically,
because the destructive one produces the emptier screen.

The distinction between reading and writing is the first conceptual thing a
database course establishes, and the tool currently teaches against it.

**This is the clearest place to be better than Jupyter** rather than to
catch up with it. No notebook I know of shows a row-level diff of what a
statement did.

**Extent.** Three tiers, and they are separable — ship the first, decide
later about the rest.

1. *Row count.* Nearly free: `conn.total_changes` before and after, or
   `cursor.rowcount`. An afternoon.
2. *Classification.* Use the authorizer to say "this statement reads" or
   "this statement writes" **before** running it, and label the cell
   accordingly. Also an afternoon, and it is what makes tier 3 affordable
   because you only pay for the snapshot when a write is coming.
3. *Row-level diff.* Snapshot the affected table before a write (`backup()`,
   or `select *` for small tables), compare after, render added / removed /
   changed rows. Real work, and it needs a size ceiling — nobody wants a
   diff of a million-row table. Cap it, and say so in the output when the
   cap bites.

**The honest risk** is that tier 3 is where the effort concentrates and it
is only useful on small teaching databases. That may be fine: teaching
databases *are* small. But it should be a decision, and the cap should be
visible rather than silent.

### 5.3 There is no undo, and the current default forecloses transactions

**The finding.** `run_query`'s docstring is explicit: *"Every query commits,
including a `CREATE TABLE`/`INSERT`/`UPDATE` — the friendlier default for a
student who doesn't yet know sqlite3 needs an explicit `commit()`; reach for
sqlite3 directly for real transaction control."*

For a data-analysis tutorial that is the right call and I would not change
it there. For a database module it is wrong twice. Transactions, commit and
rollback are *core content*, not an advanced topic to be shielded from — and
auto-commit means a student experimenting with `DELETE` has no way back,
which makes the experiment too expensive to run and so removes the way
people actually learn what `DELETE` does.

**The proposal.** Wrap each student statement in a `SAVEPOINT`, and offer
"undo that statement". Verified working in §4: a `DELETE` of every row was
reversed by `ROLLBACK TO`.

**Why this is more than a convenience.** A forgiveness feature is what makes
a destructive operation safe enough to be worth trying, and trying is how
the concept lands. It has no notebook equivalent anywhere. It also stages
the teaching well: the student meets undo as a button, and later meets the
same idea as `ROLLBACK`, and finds it is the thing the button was doing all
along.

**Options, in increasing ambition.**

- *A `safe=` parameter on `run_query`* — smallest change, opt-in per call,
  and visible in the tutorial's source so a student can see the mechanism.
- *A savepoint around every statement, with an Undo button in the results* —
  best experience, but hides the mechanism, which cuts against teaching it.
- *An explicit transaction mode the module turns on* — most honest, most
  work, and the one that matches how the outcomes will probably be written.

I lean towards the first for the tutorials and the second for dewmini, with
the difference recorded rather than accidental. **This needs Josh's
decision and it should be made before the tutorials are written**, because
it changes what the prose can say.

### 5.4 Autocomplete stops at the Python boundary

Jedi completes Python names. Inside a SQL string, the editor sees a string —
so table and column names, the identifiers a student is most likely to
mistype and least likely to remember, get no help at all.

Once §5.1 has the schema as data, the completion source exists. The work is
in CodeMirror: recognising that the cursor is inside a SQL string (or a SQL
cell, per §5.6), and offering schema identifiers there.

Outside paid extensions, Jupyter does not do this either. Medium effort,
high daily value, and it is the kind of thing that quietly reduces the
number of errors a class produces per hour.

### 5.5 Relationships are invisible

Foreign keys are the conceptual core of a relational database and they exist
only as text inside a `CREATE TABLE`. `pragma foreign_key_list` gives them
up readily (§4), and an ER diagram drawn from them is cheap once the schema
browser exists.

Adjacent and worth pairing: `EXPLAIN QUERY PLAN` rendered as a small
annotated tree rather than raw tuples. The raw output of the join in §4 is
`SCAN book` and `SEARCH author USING INTEGER PRIMARY KEY (rowid=?)` — which
is *exactly* the difference between a full scan and an indexed lookup, and
therefore exactly MIT-6.8's *"why a database index exists, and what it
costs"*, sitting there in machine-readable form. Add an index, re-run, watch
`SCAN` become `SEARCH`. That is a complete lesson in one interaction and
there is no way to teach it as well with prose.

**A caution.** Both of these are drawing features, and drawing features
absorb time. The ER diagram is worth it because relationships are the
subject; the query plan tree is worth it because the before/after is the
lesson. Neither should be attempted before §5.1, since both consume its
output.

### 5.6 A SQL cell type

**The proposal.** A third cell type beside Python and text: a cell whose
content is SQL, syntax-highlighted, run against a chosen connection,
rendering a result table.

**Why it is not a magic.** `JUPYTER_FEATURES_NEXT.md` §7 argues against
`%%sql` on the grounds that it teaches invisible non-Python syntax that
breaks the moment a student writes a real `.py` file. A cell *type* escapes
that objection: it is visibly a different kind of cell, it does not pretend
to be Python, and the boundary between the languages stays legible rather
than smeared. CodeMirror has a SQL mode already.

**Why I am still unsure.** It changes the notebook's data model — `CELL_TYPES`
(`compose/dewmini.js` ~40) is currently a closed pair, and every path that
touches cells would need to learn the third: storage and migration, the
`.ipynb` export (which has no native SQL cell — it would have to become a
code cell, losing information), the standalone HTML export, the PDF export,
the import scanner. That is the same class of "touches every surface"
change as `DECISIONS_LOG.md` 7.97, and those have a history here of costing
more than the estimate.

**The cheaper alternative worth considering first:** keep SQL in Python
strings, but detect a string being passed to `run_query` and highlight it as
SQL in the editor. Most of the readability, none of the data-model change.
It is less honest about the boundary, which is the trade.

### 5.7 Reproducible seeding — the one I would not skip

**The problem.** A `.db` file is hidden state that survives everything. A
student's database works because of a statement they ran in week three from
a cell they have since deleted. Restart Python and it is still there;
restart the browser and it is still there. Jupyter has no answer to this at
all — its "Restart and run all" clears the kernel and leaves the files.

**The proposal.** Make "rebuild this database from nothing, deterministically"
a first-class action: a seed script (SQL or Python) that drops and rebuilds,
runnable in one press. `conn.iterdump()` (§4) can generate the starting
point from a database that already exists, which makes it easy for a teacher
to produce one from a database they built by hand.

**Why it matters more than it sounds.** It is the database analogue of
restart-and-run-all, and it is the thing that makes a tutorial *reliable* —
if every student's database can be returned to a known state, an exercise
can assume one. Without it, every database tutorial is one stray `UPDATE`
away from being unfollowable, and the student cannot tell whether they are
confused or their data is wrong.

It is also the honest teaching of a real professional practice: migrations
and fixtures exist for this reason.

**Extent.** Small-to-medium, and it composes with the data catalogue that
already exists (`compose/data-catalogue.json`) — a seeded teaching database
is a catalogue entry like any dataset.

---

## 6. Bigger things beyond databases

### 6.1 The path from notebook to program

**The largest gap in dewmini, and it has nothing to do with SQL.**

Every student on PDP and CMPS eventually has to stop writing cells and write
a `.py` file with functions in it. This is the single most common complaint
about teaching with notebooks: the notebook is a good place to try things
and a bad place to build anything, and the transition is unsupported, so
students either never make it or make it painfully somewhere else.

dewmini has the pieces: a filesystem, a file tree, `.py` import, and export.
What it lacks is the idea of a **project** — several files, one importable
by a cell, and a route from a working notebook into that shape.

Concretely, three things, in order of ambition:

1. *Import your own module.* A `.py` file in the workspace becomes
   importable from a cell. Mostly a `sys.path` question, and much of the
   filesystem work is done.
2. *Extract to a function.* Take a cell, or a selection, and lift it into a
   named function in a file — with the notebook then calling it. This is a
   refactoring tool, and it teaches the move rather than merely permitting
   it.
3. *Run the project.* A `main.py` that runs without the notebook at all, so
   the student sees the thing they built work as a program.

For two of the three current modules this outranks everything in §5.

### 6.2 Provenance, bounded carefully

The execution counters in `JUPYTER_FEATURES_NEXT.md` §1 record *when* each
cell last ran. The natural extension is a record of the order things
happened — which would let a student see, and a teacher discuss, the actual
history of a session rather than its final state.

**This must be bounded before it is built.** dewlab has refused tracking,
accounts and anything assessment-shaped, repeatedly and on principle. A
provenance record that lives on the student's own machine, is visible to
them, is theirs to delete, and is never transmitted anywhere is compatible
with that. One that quietly accumulates a history a teacher can request is
not. The distinction is easy to state and easy to erode, so it belongs in
`DECISIONS_LOG.md` before any code exists.

### 6.3 Accessibility as a place to be better

Jupyter is poor for screen-reader users; this is well documented and long
standing. `tests/MANUAL_CHECKLIST.md` currently lists dewlab's own
screen-reader checks as never run, and `planning/EDGES_AUDIT.md` §3 explains
what the automated structural checks do and do not tell you.

For an FE cohort this is not a nicety. It is also the rare case where the
work is mostly *checking* rather than building, since the structure is
largely right — and where being better than the incumbent is achievable
rather than aspirational.

### 6.4 Two smaller ones, recorded so they are not lost

**Output that is not a dead HTML table.** Every result — DataFrame or query
— renders as static HTML. Sortable columns and a row count would cost little
and would make exploring a result an activity rather than a squint. The
argument against: it invites building a spreadsheet, and the point is to
teach people to express the sort in code.

**A beginner-legible debugger.** Jupyter's is poor and beginners use `print`
instead, which is not the worst outcome. But stepping through a loop and
watching a variable change is how the idea of iteration lands for a lot of
people, and the variable inspector is already most of the display half.
Large, speculative, and probably after everything else here.

---

## 7. Sequencing, and what would change it

If the database module is the next thing written, the order I would argue
for is: schema browser (5.1), then reproducible seeding (5.7), then the
transaction decision (5.3), then row-count reporting as the first tier of
5.2. That gets a module's worth of tooling for something like two to three
weeks of work, and each piece is useful before the next exists.

**What would change it.** If the module's outcomes lean on transactions
early, 5.3 moves first, because its decision constrains how every tutorial's
prose is written and is expensive to reverse afterwards. If they lean on
schema design, 5.5's ER diagram climbs. If they lean on query performance,
5.5's plan tree does.

**So the first task is not a feature.** It is writing the module's outcomes
into `planning/curriculum/outcomes.yaml` and its topics into `topics.yaml`,
wired by `needs:` onto the MIT topics listed in §2. That is a day's careful
work, it makes the sequencing question answerable instead of speculative,
and it is the thing that turns this document from a list of nice ideas into
a plan.

If the *next* thing written is not the database module, then §6.1 — the path
from notebook to program — is the strongest item in this document, and I
would rather build that than any three things in §5.

---

## 8. Open questions this document does not settle

- What the database module's learning outcomes are. Everything else waits on
  this.
- Whether `run_query` keeps auto-commit for tutorials while dewmini gets
  savepoints, or whether both change together. (§5.3)
- Whether a `.db` survives a reload on all three filesystem backends. Needs
  testing on a real machine; belongs in `tests/MANUAL_CHECKLIST.md`. (§2)
- Whether the SQL cell type is worth a change to the notebook data model, or
  whether SQL-highlighting inside strings is enough. (§5.6)
- The size ceiling for a row-level diff, and what it says when it is hit.
  (§5.2)
- Whether the schema browser picks a connection, or reports every one it
  finds in the namespace. (§5.1)
- Whether the §4 SQLite capabilities all hold under Pyodide's Python 3.13.
  They were verified under CPython 3.11 here.

---

*Written 2026-08-31 against `main` at `e3229b6`. Companion to
`planning/JUPYTER_FEATURES_NEXT.md`. Nothing in it is implemented.*
