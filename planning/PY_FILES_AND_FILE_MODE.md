# Python files in dewmini: what to build, judged for authors and for readers

A plan, in levels. Each level is useful on its own, so the work can stop
anywhere rather than only paying off when it is finished.

**Origin.** Josh, after rejecting the extract-to-function idea: students write
functions in cells comfortably; the step they find hard is *several functions
in a file, called from another file*. So the need is multiple files, a file
manager, and a way to look at a notebook as a `.py`.

Written to be read cold. Nothing here is implemented.

---

## 0. A correction, because it changed the plan

The first draft of this document defended a migration path: read both the old
and new cell markers, keep the old spelling working, set a removal date a year
out, test the compatibility promise. The reasoning was *"a student who cannot
reopen last term's work has been badly served."*

**There is no last term.** dewlab has never been released. There are no saved
files, no exported notebooks, no students. Every line of that reasoning
defended people who do not exist, and the cost was real: a dual-read pattern,
a deprecation decision to record, an extra test, and a whole open question
about migrating storage.

This is the second time in this project I have imported a "don't break
existing users" instinct without checking whether there are users — the Mini
IDE redirect was the same error, and Josh had to say the same thing then. So
the process note, not just the fact:

> **Before writing compatibility code, ask who is harmed if this simply
> changes.** In a pre-release project the answer is usually nobody, and
> compatibility machinery is then pure cost: complexity with no beneficiary,
> defended by a habit rather than a reason.

It also changes the *question*. "How do we migrate from the current marker?"
is a small question. "What is the best format, starting today?" is the real
one, and it deserves harder scrutiny than a swap-in. Section 3 is that
scrutiny, and section 2 is a design option that compatibility thinking would
have hidden entirely.

---

## 1. The two audiences, which is how every choice below gets judged

Josh named them and they are the right lens.

**Authors** — the two people who will write tutorials. They meet these choices
in `tutorials/**/*.md` and in the authoring editor. What matters to them is
whether the source is pleasant to write, review and diff, and whether a
tutorial can express what it needs to teach.

**Readers** — students, meeting these choices inside dewmini. What matters to
them is whether what is on screen is legible, whether it transfers to tools
they will meet later, and whether it can be understood without being
explained.

Those two sometimes pull apart. Where they do, this document says so rather
than pretending a choice serves both.

---

## 2. What is a notebook, physically?

The question worth asking now that nothing constrains the answer.

**Today.** A notebook is JSON in `localStorage` under `dewmini:notebooks:v1`:
`{active, notebooks: [{id, name, cells}]}`, where each cell carries its content
*and its saved output*. Separately, a filesystem mounts at `/mnt/dewmini`
holding data files. Two stores, unrelated to each other.

**The option compatibility would have hidden: make a notebook a file.** A
notebook becomes a percent-format `.py` in the workspace filesystem. Tabs are
open files. `localStorage` keeps only which tabs are open.

What that buys, and it is a lot:

- The file manager and the tab strip stop being two lists of different things.
- "View as file" stops being a conversion. It is the file.
- Multiple files, and one file importing another, fall out rather than being
  built.
- A student's work is a folder of `.py` files they can hand to anyone.

What it costs, and this is not free:

- **Outputs have nowhere to live.** A `.py` cannot carry them. Either they
  move to a sidecar file, or switching to the file lens drops them.
- **The three filesystem backends differ in reliability.** IDBFS needs an
  explicit sync (`assets/pyodide-engine.js` ~644). Losing a notebook to a sync
  that did not fire would be far worse than any problem this solves.
- It only works once Python has booted, where `localStorage` is there
  immediately.

**A finding that bears on it.** `saveState()` writes every cell's output into
`localStorage` inside one JSON blob, and its `catch {}` swallows a quota
failure silently. `localStorage` is about 5 MB. A student with a few plots or
a wide table can quietly stop being saved, with nothing on screen to say so.
That is a live bug in shipped code whichever storage model wins, and it argues
for the filesystem holding the heavy parts.

**Recommendation: not yet, but decide deliberately.** The unified model is
better architecture and I would want it eventually. It should not be attempted
before the outputs question (§6) has an answer, because dropping a student's
outputs on a lens switch would make a worse tool than we have now. Level 2 is
written so that it does not foreclose this.

---

## 3. The marker, judged on legibility rather than compatibility

dewmini writes `# ---- cell 1 ----` and `# ---- note ----`
(`downloadAsPython()` and `parsePyCells()`, both in `compose/dewmini.js`).

**Switch to the percent format** — `# %%` and `# %% [markdown]` — which
Jupytext writes and VS Code, Spyder and PyCharm all read.

Compatibility was never the strong argument for it. Here is the case under the
two audiences.

**For readers.** The cost first, because I skipped past it in the first draft
while thinking about migration: `# %%` means nothing to a beginner, where
`# ---- cell 1 ----` explains itself. That is a real loss.

Two things answer it. Inside dewmini the student never sees `# %%` — the file
lens renders the markers as cell dividers, exactly as VS Code does, so the
cryptic string surfaces only in a plain text editor. And Josh's own idea
covers that case: a short explanatory markdown block at the top of a file the
first time someone makes the transition, which the percent format carries
natively and the student can delete.

The gain is that the file opens as cells in VS Code on a college machine with
no conversion step. That is the whole argument for teaching the file rather
than only the notebook, and it is worth more than a self-describing marker
that works nowhere else.

**For authors.** No effect at all. Checked rather than assumed:
`docs/WRITING_TUTORIALS.md` never mentions the `.py` export. Tutorial sources
are markdown and stay markdown (§4). Josh's assumption here was right.

**Text goes in `#` comment lines, not triple-quoted strings.** A stray
triple-quoted block at module level is a real string object, and in first
position it silently becomes the module docstring. A comment cannot be
mistaken for code by a student or by Python.

**What the swap involves**, with the compatibility scaffolding gone: change
the writer, change the reader's pattern, update two comments. That is the
whole change.

**One thing to do first.** There is no test anywhere over `downloadAsPython()`
or `parsePyCells()` — not in `tests/test_build.py` (they are JavaScript) and
not in `tests/e2e/`. The round trip is unprotected today. Write the test, then
change the format.

---

## 4. Should tutorial sources become Python-first?

The pre-release framing sharpens this too. The question is not "is converting
worth it" — sunk cost is a weak argument and I do not want to lean on it. The
question is: **starting today, which would we choose?**

The answer is still markdown, and it is a stronger answer for being derived
that way.

**What the corpus is.** Measured across all 91 tutorials: **6,076 lines of
code against 17,306 lines of prose**, a ratio of 1:2.8. And 646 executable
cells against **211 plain code blocks that exist to be read and must not
run**.

**For authors.** Nearly three quarters of what they write is prose. A
Python-first source turns 17,306 lines of writing into `#` comments: worse to
write, worse to review, worse to diff, for the majority of the artefact. The
authoring editor (`assets/editor.js`, 1,235 lines of Milkdown/Crepe) edits
markdown with live maths and code blocks; Python-first breaks it or forces a
rewrite, and the two authors pay that.

**For readers.** They never see the source — they read the built page. So the
only reader-facing consequence is what becomes *teachable*, and there
Python-first actively loses something. `first-steps.md` teaches the
distinction between code to run and code to read, in prose. In a Python-first
file, code that must not run either runs or becomes a comment. Both destroy a
distinction the tutorials teach on purpose, and 211 blocks depend on it.

**The one real pull the other way** is that a tutorial about writing Python
files would itself be written in a different format from the files it teaches.
That is a genuine oddity, and the next section dissolves it.

### What is actually needed

Not tutorials written in Python — **a tutorial that can carry files.** Every
tutorial is already a folder holding its markdown, its practice page and its
glossary. Add one convention:

```
tutorials/database-methods/joining-tables/
    joining-tables.md            <- markdown, unchanged
    joining-tables.glossary.yaml
    workspace/                   <- shipped into the student's dewmini
```

The tutorial stays a document. The lesson about files ships real files, in the
percent format, which the student opens in dewmini and edits. Authors keep
markdown; readers get the thing being taught. Small in `build.py`: a copy step
and a manifest entry.

---

## 5. The levels

| Level | What | Effort | Useful alone |
|---|---|---|---|
| 0 | Percent-format markers | half a day | yes |
| 1 | One file imports another | ~a day | yes |
| 2 | File lens and a file manager | 1-2 weeks | yes |
| 3 | Tutorials carry a workspace | small | yes |
| 4 | The sample flow | content | - |

### Level 0 — the markers

Writer, reader pattern, two comments, and one new test that should have
existed anyway. No dual-read, no deprecation window, nothing to migrate.

**Delete while you are there.** `migrateLegacyCells()` and `LEGACY_CELLS_KEY`
(`compose/dewmini.js` ~118-131) fold pre-tabs saved work into a first
notebook. There is no pre-tabs saved work and there never will be. The
function, the key, and `test_work_saved_before_tabs_is_migrated` in
`tests/e2e/test_dewmini_workbench.py` all defend a case that cannot occur.
Removing them leaves a smaller codebase with no lost capability.

### Level 1 — one file imports another

The smallest change that touches the actual gap. The workspace mounts at
`/mnt/dewmini` and nothing puts it on `sys.path`; one insertion at boot makes
every `.py` there importable.

**The wrinkle to design in, not patch on.** Python caches imported modules, so
after editing a file a second `import` gives the old version: code that is
visibly right, behaving as though it is wrong. Of the three answers — notice
the student and offer a reload, reload silently, or restart — take the first.
It is the only one where the reader ends up knowing something true, and module
caching is a real thing to know.

### Level 2 — the file lens and the file manager

**The mode is right and my objection was wrong.** I argued against a
notebook/file mode because beginners get lost in modes. Josh's counter is
better: an empty file is a blank page, and a blank page is frightening in a
way an empty cell is not. Lowering the cost of starting is most of why
notebooks work for teaching at all.

The thing my objection was protecting is cheap to keep: show the current lens
**on the tab**, so nobody is in a state they cannot see.

**Run means different things in each lens**, and that difference is the lesson
rather than a wart. Notebook lens: run this cell. File lens: run the whole
file, top to bottom, as `python thing.py` would.

**The file manager.** `DEWMINI_WORKBENCH.md` §2 already decided the right rail
means "your own work" and the left means "things you look up", which puts
files right; every IDE puts the tree left. I would keep it right — tabs
already carry navigation, and a tree earns its place only with folders or many
files — but it is a small change either way and Josh watches students use it.

**What exists.** The filesystem layer is complete: `listDir`, `readFile`,
`writeFile`, `deleteFile`, `mkdir`, across all three backends, folders
included. The Files section in the Workbench rail is a *storage inventory* —
names, sizes, delete, upload — with no notion of a file you open. So the work
is: make a listed file openable, add new-file and rename, and let a tab hold a
file as well as a notebook.

**Design it so §2 stays open.** Whatever a tab holds should be a *document*
with a backing store behind an interface, rather than `localStorage` JSON
assumed throughout. Then moving notebooks onto the filesystem later is a
change in one place instead of everywhere.

### Level 3 — tutorials carry a workspace

`build.py` copies a tutorial's `workspace/` folder alongside the built page,
and the page offers to open those files in dewmini. Independent of everything
above, and worth doing early because it settles what tutorial sources are
before anyone is tempted to convert them.

### Level 4 — the sample flow

Josh's progression, and the thing that makes the rest worth having. The
database material is the right vehicle because it has a real reason for more
than one file — the queries belong apart from the reporting — and
`assets/examples/sql-owid.ipynb` already loads OWID emissions data into
SQLite, so the starting point is written.

1. **One notebook.** Cells, one namespace.
2. **The same notebook in the file lens.** Nothing moves. The student sees
   that what they have been writing *was* a Python file all along.
3. **Two files.** The queries lift into a file of their own; the notebook
   imports them. This is the step Josh identified as the hard one.
4. **A program.** An entry-point file, run without the notebook at all.

Each step is a tutorial and ships its own `workspace/`. Content work, and it
should follow the database module's outcomes being written.

---

## 6. Open questions

Shorter than the first draft, because three of them were about migrating from
a past that does not exist.

- **Where do outputs live?** A `.py` cannot carry them. A sidecar file, or
  dropped on a lens switch? This gates §2 and wants answering before Level 2,
  not during.
- **Do notebooks become files?** §2. Better architecture; needs the outputs
  answer first.
- **Files rail left or right?** Recommendation above; Josh's call.
- **Does a carried workspace open automatically or on a press?** Automatic is
  friendlier; on a press keeps the promise that nothing opens on a first visit
  (`DEWMINI_WORKBENCH.md` §1).
- **The silent quota failure in `saveState()`** is a real bug today, found
  while writing §2. Worth fixing on its own, whatever else happens.

---

*Corpus figures measured, not estimated: 91 tutorials, 646 executable cells,
211 illustrative blocks, 6,076 code lines, 17,306 prose lines.*

*Filenames a student would create are written without backticks on purpose:
`dev/check_doc_links.py` reads a backticked `*.py` as a claim that the file
exists in this repository, and these do not.*

*Written 2026-08-31 against `main` at `e3229b6`.*
