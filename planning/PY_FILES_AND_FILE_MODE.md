# Python files in dewmini: the percent format, file mode, and what stays markdown

A plan, in levels. Each level is useful on its own and none of them requires
the next, so this can stop at any point rather than being a thing that only
pays off when it is finished.

**Origin.** Josh, after rejecting the extract-to-function idea: students
write functions in cells comfortably; the step they find hard is *several
functions in a file, called from another file*. So the need is multiple
files, a file manager, and a way to look at a notebook as a `.py` — not a
refactoring tool.

Written to be read cold. Nothing here is implemented.

---

## 0. The decision that unlocks the rest

dewmini already exports `.py` and reads it back, with a home-grown marker:

```python
# dewmini export — 2026-08-31

# ---- cell 1 ----
marks = [72, 65, 88]

# ---- note ----
# Some prose from a text cell.
```

`downloadAsPython()` writes it, `parsePyCells()` reads it, both in
`compose/dewmini.js`. It works. It is also ours alone, and it answers Josh's
question — "are these `.py` files or `.py`-and-something files?" — with
"ours".

**Switch the marker to the percent format**, which Jupytext writes and VS
Code, Spyder and PyCharm all read:

```python
# %% [markdown]
# Some prose from a text cell.

# %%
marks = [72, 65, 88]
```

The mechanism is identical — a line-prefix marker, split on it, comment-strip
the markdown blocks. What changes is that the result is a convention with
readers outside this project. A student's file opens as cells in VS Code on
a college machine, unchanged, which is the entire argument for teaching the
file rather than only the notebook.

It also settles the naming question with no qualifier: **they are `.py`
files.** A percent-format file is valid Python — `python thing.py` runs it —
*and* is a notebook. The notebook view is a lens on a `.py`, not a rival
format, and no JSON is involved anywhere.

**Text goes in `#` comment lines, not triple-quoted strings.** A stray
`"""..."""` at module level is a real string object, and in first position it
silently becomes the module docstring. Comments cannot be mistaken for code
by a student or by Python.

**Cell metadata rides on the marker line** where it is needed:
`# %% id=first-run`. Jupytext already does this, so it stays readable
elsewhere.

---

## Level 0 — The marker swap

Small, self-contained, and worth doing whether or not anything below happens.

**What changes.** Four places, all in `compose/dewmini.js`:

| Site | Change |
|---|---|
| `downloadAsPython()` ~1181 | write `# %%` / `# %% [markdown]` |
| its comment ~1181 | describe the percent format and name Jupytext |
| `parsePyCells()` ~2071 | read the new markers |
| `markerRe` ~2085 | a pattern matching both old and new |

**Read both, write one.** Files students have already exported carry the old
markers, and a student who cannot reopen last term's work has been badly
served by a tidying exercise. `markerRe` accepts both spellings; the writer
only emits the new one. The old spelling can be dropped in a year, and the
comment should say that so it is a decision rather than an accident.

**A finding to act on first: the round trip is untested.** There is no test
anywhere over `downloadAsPython()` or `parsePyCells()` — not in
`tests/test_build.py` (they are JavaScript) and not in `tests/e2e/`. So
step one is a test that pins the *current* behaviour, before changing it. An
e2e test in `tests/e2e/test_dewmini_workbench.py` that builds a notebook,
exports it, re-imports it and compares is the shape; it also covers the
compatibility promise, since it can import a fixture in the old spelling.

**Authoring advice does not change.** Checked: `docs/WRITING_TUTORIALS.md`
never mentions the `.py` export. The marker is a dewmini import/export
concern and touches nothing an author writes. Josh's assumption was right.

**Also worth updating**: `DECISIONS_LOG.md` 7.x describes the old markers in
a historical entry — leave that, it is a record — and add a new entry for
the swap.

**Effort:** an afternoon, most of it the test that should have existed.

---

## Level 1 — One file can import another

The smallest thing that addresses the actual pedagogical gap.

Today nothing puts the workspace on `sys.path`, so no file can import
another. The workspace mounts at `/mnt/dewmini` (`compose/dewmini-fs.js`,
`MOUNT_POINT`). One insertion at boot makes every `.py` there importable.

**The wrinkle that must be designed in, not patched on.** Python caches
imported modules. After editing a file the student wrote — grades.py, say —
a second `import grades` gives the old version, and the student meets code
that is visibly right and behaves as though it is wrong: a worse mystery than
the one this solves.

Three options, and they are not equal:

- *Tell them.* A notice when an imported file has changed on disk, with a
  reload action. Honest, visible, and it teaches that modules are cached —
  which is a real thing to know.
- *Reload silently.* `importlib.reload` on any changed file before a cell
  runs. Frictionless and dishonest: it hides a behaviour they will meet
  everywhere else.
- *Restart.* Correct, and far too heavy for a one-line edit.

I would take the first. It is the only one where the student ends up knowing
something true.

**Effort:** small. The `sys.path` line is minutes; the change-detection and
notice is most of a day.

---

## Level 2 — File mode, and a file manager

**The mode is right, and my objection was wrong.** I argued against a
notebook/file mode on the grounds that beginners get lost in modes. Josh's
counter is better: an empty file is a blank page, and a blank page is
frightening in a way an empty cell is not. Cells lower the cost of starting,
which is most of why notebooks work for teaching at all.

So: a mode. The thing my objection was protecting is cheap to keep — make
the current lens **visible on the tab itself** rather than in a menu, so
nobody is ever in a state they cannot see. That costs nothing and keeps the
benefit.

**What Run means in each lens** has to be decided, because they differ:

- *Notebook lens*: run this cell. Unchanged.
- *File lens*: run the whole file, as `python thing.py` would — which is the
  point of the lens. The output goes to one output area for the file rather
  than to a cell.

That difference is not a wart; it is the lesson. A file runs top to bottom
every time, and that is exactly what a notebook does not do.

**Josh's explanatory-comment idea** — text at the top of the file the first
time someone makes the transition — is a good fit for the percent format,
because it is a markdown block like any other and the student can delete it.
Better than a dialogue, which they would dismiss unread.

**The file manager.** Two conventions collide. `DEWMINI_WORKBENCH.md` §2
already decided the right rail means "your own work" and the left means
"things you look up", which puts files right. Every IDE puts the tree left.

I would keep it right, on the grounds that tabs already carry navigation and
a tree only earns its place once there are folders or many files. But this is
a five-minute change either way and Josh should have the last word, since he
is the one who will watch students use it.

**What exists and what does not.** The filesystem layer is complete —
`listDir`, `readFile`, `writeFile`, `deleteFile`, `mkdir`, across all three
backends, with folders supported. The Files section in the Workbench rail is
a *storage inventory*: names, sizes, a delete button, upload, folder
picking. It has no notion of a file you open and edit.

So the work is not "build a file manager". It is: make a file in that list
openable, add new-file and rename, and let a tab hold a file rather than only
a notebook.

**The tab model is where the real design sits.** Today a tab is a notebook
(`{id, name, cells}`). It would need to be a tab over a *document*, which is
either a notebook or a file. That is the change with the widest blast radius
in this whole plan — storage, migration, every export path — and it is worth
sizing properly before starting rather than discovering mid-way.

**Effort:** the largest level here. Two to three weeks, most of it the tab
model rather than the visible UI.

---

## Level 3 — The big question: should tutorial sources become Python-first?

Josh asked for pros and cons rather than a verdict, so here is the case both
ways, then what I would do.

**What a tutorial source looks like today.** YAML frontmatter, then markdown
prose, with ` ```python exec ` fences that become runnable cells and plain
` ```python ` fences that are there to be read.

### The case for Python-first

One format across tutorials and dewmini. A tutorial source that is itself
runnable. Students able to open the source in any editor. Conceptual tidiness
— the thing that teaches Python is written in Python.

### The case against, with the corpus measured

**The ratio.** Across all 91 tutorial files: **6,076 lines of code against
17,306 lines of prose.** Nearly three quarters of the corpus is writing.
These are documents with code in them, not programs with commentary, and
turning 17,306 lines into `# ` comments would make the source materially
worse to write, review and diff for the majority of what it contains.

**The 211 illustrative fences.** The corpus contains 646 executable cells
and **211 plain ` ```python ` blocks that exist to be read and must not
run.** `first-steps.md` teaches this distinction in prose: *"Not every piece
of code on a page is meant to be run."* In a Python-first file, code that
must not run either runs or becomes a comment, and both destroy a
distinction the tutorials explicitly teach.

**The authoring editor.** `assets/editor.js` is 1,235 lines of Milkdown/Crepe
built to edit markdown with live maths and code blocks. Python-first either
breaks it or forces a rewrite. That is the second-largest cost after the
prose, and it is a cost paid by the two people who write tutorials.

**The build pipeline is markdown-shaped throughout** — `extract_math`,
`extract_blocks`, `to_html`, `place_blocks` — and frontmatter has no natural
home in a `.py`.

**And 182 files to convert** (91 tutorials plus their practice pages), each
needing review, against a benefit nobody receives: students never see the
source. They see the built HTML page.

### What I would do instead

The dichotomy is false. The real need is not "tutorials written in Python" —
it is **a tutorial that can carry files**, so a lesson about importing can
ship the two files it is about.

Every tutorial is already a folder holding its markdown, its practice page,
its glossary and its assets. Add one convention:

```
tutorials/database-methods/joining-tables/
    joining-tables.md            ← unchanged, markdown-first
    joining-tables.glossary.yaml
    workspace/
        grades.py                ← shipped into the student's dewmini
        main.py
```

The tutorial stays a document. The lesson about files ships actual files.
`build.py` copies `workspace/` alongside the page and the page offers to open
them in dewmini. No conversion, no editor rewrite, no loss of the
read-versus-run distinction.

**Recommendation: keep tutorial sources markdown-first, and add carried
workspaces.** The percent format then earns its place exactly where it
belongs — in the files a *student* writes, which is where cross-tool
compatibility matters and where nobody is writing 17,000 lines of prose.

**Effort:** small in `build.py` — a copy step and a manifest entry — next to
weeks for the conversion it replaces.

---

## Level 4 — The sample flow

Josh's idea, and the thing that makes the levels above worth having: sample
notebooks that become sample files, ending somewhere real.

The database material is the right vehicle, because it has a natural reason
for more than one file: the queries belong apart from the reporting.
`assets/examples/sql-owid.ipynb` already exists and already loads OWID
emissions data into SQLite, so the starting point is written.

A progression worth designing against:

1. **One notebook.** The existing `sql-owid.ipynb`. Cells, one namespace.
2. **The same notebook, viewed as a file.** Nothing moves. The student sees
   that the thing they have been writing *was* a Python file all along.
3. **Two files.** The queries lift into a file of their own; the notebook imports
   them. This is the step Josh identified as the hard one, and it now has a
   tool that supports it.
4. **A program.** An entry-point file, run without the notebook at all.

Each step is a tutorial, each ships its `workspace/`, and the artefact at the
end is a small project rather than a page of cells.

**Effort:** content work, and it should follow the database module's outcomes
being written — see `DATABASE_MODULE_AND_BIGGER_IDEAS.md` §7, which says the
same thing about that module generally.

---

## Order, and why

| Level | Depends on | Effort | Useful alone |
|---|---|---|---|
| 0 — percent format | nothing | an afternoon | yes |
| 1 — import a workspace file | 0 in spirit, nothing technically | ~a day | yes |
| 2 — file mode and manager | 0, 1 | 2–3 weeks | yes |
| 3 — carried workspaces | nothing | small | yes |
| 4 — the sample flow | 1, 2, 3 | content | — |

Level 0 first because it is cheap, independent, and every later level writes
files in that format. Level 1 next because it is the smallest change that
touches the actual gap — a student can have two files and import one from
the other before any new UI exists.

Level 3 can happen any time and does not depend on the rest; it is worth
doing early because it settles the question of what tutorial sources are
before anyone is tempted to convert them.

Level 2 is the expensive one and the tab model is its real content. It should
not start until someone has written down what a tab holds.

---

## Open questions

- Files rail left or right. Recommendation above, but Josh watches students
  use it.
- Whether outputs survive the notebook→file lens. A `.py` has nowhere to put
  them: either they are kept out-of-band and re-attached, or switching drops
  them. Not obvious, and it should be decided before Level 2 rather than
  during.
- What a tab holds once it can hold a file, and how the existing
  `dewmini:notebooks:v1` storage migrates.
- Whether the old `# ---- cell N ----` spelling gets a removal date.
- Whether the carried workspace opens in dewmini automatically or on a
  press. Automatic is friendlier; on a press keeps the promise that nothing
  opens on a first visit (`DEWMINI_WORKBENCH.md` §1).

---

*Filenames a student would create are written without backticks on purpose:
`dev/check_doc_links.py` reads a backticked `*.py` as a claim that the file
exists in this repository, and these do not.*

*Written 2026-08-31 against `main` at `e3229b6`. Corpus figures measured, not
estimated: 91 tutorials, 646 executable cells, 211 illustrative blocks, 6,076
code lines, 17,306 prose lines.*
