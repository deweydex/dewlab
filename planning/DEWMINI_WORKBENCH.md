# dewmini as a workbench: two rails, tabs, and tools for looking at your own work

Written in response to a direct instruction: tabs, sidebars on both sides
carrying file imports and "variable inspectors and other pedagogical
tools", a fuller reference with search and category navigation on the
left, data import from somewhere like Our World in Data, and a right-hand
side simplified away from settings and towards notes and pedagogy.
Widgets — the one real capability gap — were explicitly deferred.

This document is the design and the record of what was built to it.

---

## 1. The tension worth naming first

Every planning document dewmini has says the same thing: it is the small
one. `MINI_IDE_AND_DEWMINI_NEXT.md` §3's entire finding was "nothing that
makes it bigger", and the retirement addendum insisted the goal was
gaining the other workspace's *capability*, not its *weight*.

What is asked for here is more surface: two rails, tabs, a reference, an
inspector. Taken naively, that is the cockpit those documents warned
against — and it would be the second time this repository talked itself
into one.

It is also the right call, and the documents themselves say why: this is
a decision only the person the tool is for gets to make, and the reason
the smallness rule existed was that dewmini had a larger sibling to be
small *against*. That sibling is gone. dewmini is now the only place a
student writes Python outside a tutorial, and the only place a project
can grow. A tool with no alternative cannot also refuse to grow.

So the rule the smallness discipline becomes, rather than the rule it
was:

> **Quiet by default, everything one press away.**

Nothing new opens on a first visit. The notebook keeps the middle of the
screen and its full width until a reader asks for something else. Someone
who came to check `6 * 7` sees a heading, a toolbar, and a cell — exactly
what they see today. Someone building a project opens both rails and has
a workbench. The capability is additive; the weight is opt-in.

Every decision below is checked against that sentence.

---

## 2. What goes where, and why

Three panels across two edges, replacing today's two-on-one-edge.

**Left — Library (`#dm-library`). Things you bring in.**
Reference, data, and help: everything that is *lookup*. A student opens
the left rail with a question about the world outside their notebook —
what does `enumerate` do, what data can I get, what does Shift+Enter do.

**Right — Workbench (`#dm-workbench`). Things about your own work.**
Notes, variables, files. A student opens the right rail with a question
about the notebook in front of them — what have I got, where did my
`.db` file go, what was I thinking last time.

**Right — Settings (`#dl-settings`). Configuration, demoted.**
Still there, still docked right, but no longer the headline. Notes and
Files *move out of it* into the Workbench, which is the substance of the
instruction to make the right-hand side "more into notes and other
pedagogical ideas": the right rail's identity is now your work, and
settings is the thing you occasionally go and change.

The pairing follows the tutorial pages exactly, mirrored: the two
right-docked panels are mutually exclusive because they occupy the same
edge; the left one is independent, so a reader can have the reference
open beside their variables. That is not a new mechanism — the shared
stylesheet has carried `data-dl-panel-left`/`data-dl-panel-right` and
independent width variables since `DECISIONS_LOG.md` 7.83. dewmini had
been overriding it with a single-panel simplification (7.84, correct at
the time, since both its panels docked right). Removing that override is
most of the two-rail work.

Help stops being its own panel and becomes a Library section, on
`SIDEBAR_CONTENT.md` §4's own reasoning: extend a panel rather than add
one, because panels that mutually close each other are more moving parts
than they are worth. Three toggles, not four.

---

## 3. Tabs

`cells` — a module-level array — becomes one notebook among several.
Storage moves from `dewmini:cells:v1` (a bare array) to
`dewmini:notebooks:v1` (`{active, notebooks: [{id, name, cells}]}`), with
a one-way migration that folds any existing saved array into a first
notebook called "Notebook". Nobody loses work; that migration is tested.

Each notebook carries its own name, which is also its export filename —
so "Keep a copy" downloads the tab you are looking at, named what the tab
is called, rather than one global filename for everything.

**One Python session, shared by every tab — deliberately.** Real Jupyter
gives each notebook its own kernel; dewmini has one interpreter, and
giving each tab its own namespace would mean threading a namespace
identifier through every engine call and across the worker boundary — a
change to the shared engine, which `DECISIONS_LOG.md` 7.97 established is
a change to every surface that runs Python. That is a poor trade for an
overnight change made without the person it is for available to weigh it.

The honest alternative is to make the sharing *visible* rather than
surprising, which the Workbench does for free: the Variables section
shows one namespace, and says in plain words that every tab shares it. A
student who defines `data` in one tab and finds it in another has been
told, and can see why. Recorded here as a real decision with a real
alternative, not an oversight — if it turns out to confuse people, the
per-tab namespace is the fix and this paragraph is the brief for it.

---

## 4. The reference, and the constraint it deliberately drops

The tutorial pages' Reference panel is assembled per page under one hard
rule (`REFERENCE_PANEL.md` §1): never show a reader something they have
not been taught yet. A reference that spoils next week's function names
is worse than no reference.

dewmini's reference **drops that rule**, and this needs to be a stated
decision rather than an accident of reuse. The rule exists to protect a
reader's position in a sequence. A student in an open workspace has no
position in a sequence — that is what the workspace *is*. Someone who
opens dewmini to try an idea is already off the rails the curriculum
lays, and a reference that hid two-thirds of itself on the grounds that
they had not reached tutorial 31 yet would be actively unhelpful.

So dewmini gets the union: every term from every tutorial's glossary,
deduplicated on `(term, kind)`, 251 entries across 43 files today,
grouped by the five kinds the glossary schema already defines — concept,
function, operator, formula, keyword — with search across both terms and
definitions, and each entry saying which tutorial introduced it and
linking there. Category navigation and search are what make 251 entries
navigable rather than a wall.

Generated at build time into `assets/reference-index.json` by
`write_reference_index()`, from the same `own_glossary()` the tutorial
pages use. One source of truth: a glossary edit reaches both surfaces, and
neither can drift from the other.

---

## 5. Variables, and why an inspector is a teaching tool

The gap this closes is small to describe and large in practice: a student
runs a cell, something happens, and the only evidence is whatever they
remembered to print. Variables that exist but were never printed are
invisible. "Did that actually work?" has no answer short of typing the
name and running again.

The Workbench's Variables section lists what is actually in the session:
name, type, and a one-line summary — a DataFrame's shape, a list's
length, a number's value — refreshed after every run. It separates a
student's own data from the functions and modules that share the
namespace, so what they made is at the top and the furniture is tucked
below.

The introspection is Python (`describe_globals()` in
`tutorial_tools.py`), not JavaScript, for three reasons: it is where
`_page_globals` lives; it returns only strings, so nothing crosses the
worker boundary as a proxy; and it is unit-testable under plain CPython,
which the JavaScript half is not.

---

## 6. Data, and one thing this environment could not verify

The catalogue (`compose/data-catalogue.json`) lists datasets with their
real source, licence and description, and inserts working starter code
into the notebook when picked. It covers the three datasets already in
`data/`, and a curated set of Our World in Data releases.

**The remote half carries a caveat, stated rather than hidden.** A
browser will only fetch a file from another site if that site permits it
(the CORS rule). Our World in Data's CSV endpoints are widely used from
browsers and are expected to permit it — but *this* was built in a
sandbox whose network policy blocks `ourworldindata.org` outright, so the
fetch could not be tried even once. Twice now this repository has shipped
a claim about something it never tested (`DECISIONS_LOG.md` 7.92: two
offline bundles that could not actually be opened), so the claim is not
being made a third time.

What was built instead assumes nothing: `load_csv()` now accepts a full
URL as well as a local name, and when a remote fetch fails it raises an
error that *explains* — that the other site has to allow it, and that the
reliable route is to download the file and add it through the Workbench's
Files section. That failure path is itself a lesson about how the web
works, rather than a dead end. `tests/MANUAL_CHECKLIST.md` carries the
one check nobody here could run: open dewmini on a real network, pick a
remote dataset, and see which way it goes.

---

## 7. Smaller things, from the same review

- **Undo for a destructive import.** Picking an `.ipynb` replaced the
  whole notebook with no confirmation and no way back, and because saving
  is immediate, the previous work was gone. Imports now land in a *new
  tab* rather than over your work — which tabs make possible, and which
  is better than the confirmation dialog that was the alternative.
- **Shift+Enter runs and advances**, matching every notebook tool a
  student will meet later; Ctrl/Cmd+Enter runs in place.
- **Find and replace** in the editor, which CodeMirror has always
  supported and dewmini had never wired up.

---

## 8. Deliberately not done

- **Widgets off the main thread** — the real capability gap, deferred by
  instruction. `text_input`, `dropdown`, `button` and `image_input` still
  raise on the hosted page.
- **A namespace per tab** — §3.
- **`micropip` package installation** — the next ceiling a self-directed
  project hits, and untouched here.
- **Notebooks saved into the mounted filesystem** — they remain in
  browser storage. Tabs make this more attractive, not less; it is the
  obvious next step.

---

## 9. What was verified, and how

Not asserted — run, in this order:

1. `pytest` — unit tests, including the storage migration and
   `describe_globals()` over every type it claims to summarise.
2. `python3 build.py --clean` — a real build, with the reference index
   emitted and checked.
3. **A real browser.** `tests/e2e/` drives Chromium against a
   self-hosted Pyodide. New tests there cover tabs, the variable
   inspector against live Python, and the rails opening together. This
   is the part the decision log keeps saying was missing.
