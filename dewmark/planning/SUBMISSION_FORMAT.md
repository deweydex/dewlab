# The submission format

What leaves the student's machine, what the teacher collects, and what the
workbench reads. Designed so that a folder of these files is a complete,
self-explaining record of a sitting — openable by a human with no tooling,
parseable by the workbench with no server, and still legible in ten years.

## 1. The zip

One file per student:

```text
dewmark_<exam_id>_<student_id>_<surname>-<firstname>.zip
  submission.json     the machine-readable record (§2)
  snapshot.html       a human-readable, inert copy of the paper as answered (§3)
```

The name carries exam, id, and student so a directory listing is already a
roster (the experiments' `exam_submission_<timestamp>.json` is the
counterexample). Name components are sanitised to `[a-z0-9-]`; the
authoritative identity lives inside `submission.json`, the filename is a
convenience. The zip is store-only (no compression) written by a small
first-party zip writer — local file headers, central directory, CRC-32 —
roughly sixty lines of JS, no dependency, and trivially unpackable
everywhere.

The autosave file (EXAM_RUNNER §4) is `submission.json` alone, same schema,
saved continuously; finishing packages it with the snapshot. One format for
saving, restoring, and submitting — a restore reads a submission and a
submission is the last save.

## 2. `submission.json`

```json
{
  "dewmark_submission": 1,
  "exam": {"exam_id": "mit-5n18396-2026-summer",
            "version": "2026.05.01.1",
            "title": "...", "module": "5N18396", "variant": "student"},
  "student": {"name": "Agnes Nitt", "student_id": "S12345"},
  "timing": {"started_at": "2026-05-14T09:31:04Z",
              "finished_at": "2026-05-14T11:22:40Z",
              "saved_at": "2026-05-14T11:22:40Z"},
  "answers": {
    "a1.a": {"type": "text", "value": "A ∪ B = {1, 2, 3, 5, 8}"},
    "a3.roots": {"type": "numeric", "values": {"r1": "4", "r2": "-2"}},
    "b1.shape": {"type": "mcq", "selected": 2},
    "b2.t": {"type": "table", "cells": {"r0c1": "16", "r0c2": "11"}},
    "b1.sketch": {"type": "sketch", "shape": "upward (∪)",
                   "features": {"root1": ["1", "0"], "vertex": ["2", "-1"]}},
    "t2.a": {"type": "code",
              "code": "df = pd.read_sql(...)\nshow(df)",
              "last_run": "2026-05-14T10:14:02Z",
              "run_matches_code": true,
              "outputs": [
                {"kind": "stdout", "text": "..."},
                {"kind": "table", "columns": ["name", "programme"],
                 "rows": [["...", "..."]]},
                {"kind": "image", "mime": "image/png", "b64": "..."},
                {"kind": "error", "text": ""}
              ]}
  },
  "attempted": {"A": ["a1", "a2", "a3", "a5", "..."], "B": ["b1", "b2", "b4", "b6"]},
  "events": [{"t": "2026-05-14T09:31:04Z", "e": "start"},
              {"t": "2026-05-14T10:14:02Z", "e": "run", "id": "t2.a"},
              {"t": "2026-05-14T11:22:40Z", "e": "finish"}]
}
```

Rules the schema exists to enforce:

- **Everything keyed by answer id.** No positional data anywhere
  (LESSONS: "Answers keyed by position").
- **No HTML.** Text is text, tables are columns and rows, figures are
  typed base64 images with a declared mime, errors are text. The
  workbench renders from structure and never injects submission content
  as markup (LESSONS: "Output persisted as scraped innerHTML"). A reader
  encountering an unknown `kind` shows a labelled placeholder, not
  nothing.
- **Absent means unanswered.** An empty-string answer is preserved as the
  student left it; a missing id means the field was never touched. The
  workbench treats both as unanswered but displays them differently.
- **`run_matches_code`** records whether the stored outputs came from the
  code as submitted — false when the student edited after the last run —
  so a marker knows whether to trust the printed output.
- **Events are minimal and honest**: lifecycle and runs only, no
  keystrokes, no focus tracking. They serve recovery and timestamping, and
  the format documentation states their full extent.

`dewmark_submission: 1` versions the schema; readers refuse unknown major
versions with a message naming both versions.

## 3. `snapshot.html`

A single inert HTML file: the paper with the student's answers rendered
into it — prose, filled fields as static text, code with its recorded
outputs, figures inline. No JavaScript at all; print CSS embedded, so
opening it in any browser and printing gives the paper-trail PDF whenever
one is wanted. This replaces the experiments' "remember to press Print
before you leave" step as the safety copy: the record exists whether or
not anyone printed. The workbench never parses the snapshot (it reads
`submission.json`); the snapshot exists for humans — the student's own
copy, an external examiner's quick look, a dispute years later.

Because it renders student text, the snapshot generator escapes
everything and renders figures only from validated `data:image/...`
URIs.

## 4. The marking pack

Not part of the submission, but specified here because it is the other
file the workbench loads. The composer emits, per exam,
`dewmark_<exam_id>_marking_pack.json`: the full canonical model *plus*
model answers and rubrics keyed by answer id, plus the choose-N rules.
It is the marking scheme in machine-readable form, it never leaves the
teacher's machine, and its exam id and version are checked against every
submission the workbench opens. The assessor HTML variant (the readable
model-answer paper) is generated from the same data for humans who want
the MIT-style key on paper.

## 5. Collection

dewmark does not run the collection channel; Moodle (or a shared folder,
or email at worst) does. The format's contribution is that the collected
artefacts need no unpacking discipline: the teacher selects all zips,
downloads them into one folder, and points the workbench at it. Duplicate
submissions from one student (a re-upload after the ten-more-minutes
amendment) are resolved by the workbench — newest `saved_at` wins, both
retained, the choice logged and reversible (GRADING_WORKBENCH §2).
