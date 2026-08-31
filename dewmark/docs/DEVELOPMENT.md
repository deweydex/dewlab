# dewmark development notes

This document is for people working on dewmark's own code. It explains
how the folder is organised, how to run everything, and — most
importantly — where the current draft falls short of the design
documents, so nobody mistakes a draft behaviour for a decision.

## dewmark stands alone

dewmark lives inside the dewlab repository but deliberately shares no
code, styles, or build machinery with it. Everything dewmark needs is
under `dewmark/`, its pages repeat the colour palette rather than
importing it, and its tests run on their own. The intent is that the
folder could be lifted into its own repository without breaking
anything. The one thing shared with dewlab is its working habits:
plain-spoken documents, why-comments in code, and tests beside every
program.

## Layout

```text
dewmark/
  build_exam.py        the exam builder: exam file in, finished pages out
  assets/
    exam-page.css      styles inlined into every built exam page
    exam-page.js       behaviour inlined into every built exam page
  workbench/
    index.html         the marking workbench, one self-contained page
  samples/             openly shareable exam files and their pictures
  tests/               the builder's automated tests
  dev/                 hand-run scripts, including the browser smoke test
  docs/                this file, and the guide for teachers
  planning/            the design documents (start with the README above)
```

## Running things

```sh
pip install -r dewmark/requirements.txt

# build the sample exam
python dewmark/build_exam.py dewmark/samples/sample-mixed-paper.exam.md \
    --output /tmp/dewmark-sample

# the builder's tests
python -m pytest dewmark/tests -q

# the browser smoke test (needs Playwright and a Chromium; see the file)
python dewmark/dev/smoke_pages.py
```

The smoke test builds the sample exam, sits part of it in a headless
browser (answers several question types, finishes, downloads the
submission, reloads and restores), then loads the marking workbench,
marks with all three marking methods, and checks the exports. It is the
closest thing to a rehearsal that runs without a person.

## Where the draft falls short of the design

Each of these is a deliberate simplification in the current code, not a
decision against the design documents. The documents remain the target.

- **Mathematics is not typeset.** Text between dollar signs renders in
  italics. The design calls for proper typesetting at build time.
- **Python code questions are refused by the builder** with a message
  naming the roadmap. Everything about them — the in-page runner, the
  recorded outputs — is still to build.
- **The essay writing view is simplified.** The word count and the
  planning box work; the full-width distraction-free layout the design
  describes is not built.
- **Marking is mouse-and-keyboard, not keyboard-first.** The
  digits-then-Enter flow, and the reusable feedback phrases, are not
  wired yet.
- **"Answer any N" counting cannot yet be overridden.** The workbench
  counts the best N automatically; the marking record already has a
  field for a marker's override, but there is no control for it.
- **The readable copy is produced from the live page.** The design
  prefers a copy generated independently of the page's state; the
  current approach is tested to contain no scripts, but it is the
  weaker construction.
- **Submission zips are read back only in dewmark's own form** (entries
  stored without compression). A zip re-packed by other software is
  reported, not read.
- **Question prose cannot contain lines of three backticks**, because
  the parser treats every such line as a settings block. This will
  matter when Python questions arrive and is noted in the parser.
- **Two markers, one folder, is unhandled.** The marking record is a
  single file with no merging; the last save wins.
- **The accessibility baseline is only partly met.** Answer spaces have
  labels and the pages work by keyboard, but no full audit against
  planning/APPEARANCE_AND_READABILITY.md has been run.

## Conventions

Python and JavaScript code carries comments that explain why, not what.
Every check the builder performs has a test in `tests/` that proves it
fires, and a change that adds a check adds its test in the same commit.
The saved-data formats — the exam file, the answers file, the marking
scheme, the marking record — all carry `format_version: 1`; any change
to what they contain must raise the version and keep the old one
readable, because real submissions must stay readable for years. None
of the formats is frozen yet; the roadmap freezes them before any real
sitting.
