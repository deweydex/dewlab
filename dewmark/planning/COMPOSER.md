# The composer

The teacher-side authoring surface: source in, exam variants out. It grows
in three phases, and the first is not a page at all.

## Phase 1 — the builder

`dewmark/build_exam.py`, a command-line compiler in the build.py mould:
Python, no dependencies beyond the repo's build requirements, one file
until it earns splitting, a `docs/build-exam-explained.md` beside it, and
a unit-test suite that grows with every parsing rule (the `tests/`
precedent for build.py is the model — most of SOURCE_FORMAT's *build
error* promises become test cases here).

```sh
python dewmark/build_exam.py path/to/exam.md --out dist/
```

emits, per exam:

```text
dist/
  mit-2026-summer.student.html        the paper (scaffolds per variant flag)
  mit-2026-summer.backup.html         no-Python variant, when the exam has code
  mit-2026-summer.assessor.html       readable model-answer key
  dewmark_mit-2026-summer_marking_pack.json
```

Flags: `--variant` to build a subset, `--practice` to keep scaffolds and
relabel the header, `--check` to validate without writing (the CI mode).
The builder is where every invariant lives: marks arithmetic, id
uniqueness, embedded-file completeness, the no-model-content-in-student-
variants assertion, KaTeX build-time rendering, determinism (same input,
byte-identical output — diffs of regenerated papers must be reviewable).

Phase 1 authoring is therefore any text editor plus the builder in a
terminal — which is also exactly the loop an LLM translation runs
(SOURCE_FORMAT §10). This is deliberate: the format and compiler must be
good enough to author with before a UI papers over them.

## Phase 2 — preview

`--serve` (or a watcher): rebuild on save, open the student variant
locally, hot-reload. Sitting the paper yourself is the only real proof a
question reads well at the answer box; the preview makes that loop
seconds long. The preview banner states variant and version so a teacher
never mistakes an assessor build for a student one (the MIT assessor
banner, done properly — and hidden in print).

## Phase 3 — the composer page

A static page (`dewmark/composer/`), hosted with the tools or run
locally, for teachers who will not run a terminal — which is most
teachers, and eventually this project's test of whether dewmark travels
beyond its author. Scope, in order:

1. **Load, validate, preview, package.** Open or paste source; run the
   same validation the builder runs (the parsing core must be reusable
   from the page — an argument for compiling it to run in Pyodide, so
   the page and the CLI share one implementation rather than a JS port
   that drifts; DM-11); preview any variant in an iframe; attach data
   files; download the variant set and marking pack.
2. **Structured editing.** A question list with drag-reorder, per-part
   forms for the fielded data (ids, marks, types, rubrics), a text
   editor for prose. The dewlab authoring editor and the FAQ app are the
   in-family precedents (Milkdown for prose is available in
   `assets/vendor/`), but an exam is more form than essay, so
   form-first with a prose editor per block is the working assumption —
   held loosely until phase 1 authoring has taught us where the friction
   is.
3. **A question bank.** Import questions from other dewmark sources by
   id; `compose/practice-bank.json` and the everlearning skills-demo
   material are the seed corpus. Bank-aware authoring (reuse a question,
   vary its numbers via the Python builder) is where the format's
   LLM-translation groundwork compounds: old papers become bank entries
   once, then recombine.

The composer never touches a server and never holds the only copy of
anything: its working state autosaves to localStorage, but the source
file on the teacher's disk remains the truth, and Save always means
"write the file back" (File System Access) or "download it".

## What the composer does not decide

Where exam sources live (a private repo, a local folder — DM-1), and
whether the composer gains the editor.js-style GitHub PAT integration for
teachers who do keep sources in a repo. Both wait on real usage; the
builder works on files and does not care.
