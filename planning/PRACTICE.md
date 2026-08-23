# Interactive Practice Sets & Runtime Student Cells Specification

Architecture specification for dedicated practice problem modules, reflection prompts, and dynamic student-created problem sharing.

---

## 1. Overview & Capabilities

A practice module is structured as a dedicated practice document paired with a tutorial, providing:
1. Formative problem solving with instant client-side verification (`check()`).
2. Reflective self-assessment prompts before and after problem sets.
3. Dynamic runtime problem creation and peer sharing.

## 2. Existing System Foundations

- **Interactive Widget Primitives**: `text_input`, `dropdown`, and `button` in `assets/tutorial_tools.py` provide interactive input surfaces.
- **Formative Answer Checking**: `check(actual, expected, tolerance)` provides immediate pass/fail feedback without grades or central data logging.
- **Local Persistence & Export**: `localStorage` saves student code by cell ID; JSON export/import enables offline backups and peer exchange.

## 3. Dynamic Runtime Cell Architecture

Standard dewlab tutorials mount static cells defined at build time in Markdown. Supporting student-authored practice problems requires dynamic runtime cell creation:

### Technical Requirements
- **Dynamic State Storage**: Storing dynamically created cells in local storage alongside build-time manifest cells.
- **Cell ID Namespacing**: Generating unique client-side IDs (`custom-<uuid>` or `custom-<timestamp>`) to prevent collisions with build manifests or imported peer datasets.
- **Version Immunity**: Dynamic student-created cells belong to no static release version; progress restoration preserves custom cells regardless of tutorial version changes.
- **Client Execution Security**: Imported peer problem files execute inside the Pyodide WebAssembly sandbox. While isolated from the host OS, code runs within the browser tab origin. Clear UI indications are presented when loading external peer code.

## 4. Practice Page Layout

Practice pages follow a three-tier structure:

1. **Pre-Practice Reflection**: Introductory self-assessment prompts (e.g. baseline confidence, expected challenge areas) without automated grading.
2. **Core Problems**: Progressive problem sequence spanning numeric evaluation, multi-step calculation, and function authoring, checked via `check()`.
3. **Post-Practice Reflection**: Summary prompts evaluating problem-solving strategy and unexpected conceptual insights.

## 5. Implementation Roadmap

1. ~~**Static Practice Page Prototyping**~~ — done. Thirty-two per-tutorial
   pages and four mixed sets; see `planning/EXERCISES.md`.
2. ~~**Build-Level Integration**~~ — done. `practice_for:` with bidirectional
   linking, and `practice_across:` for a set with no single owner. Both are
   validated at build time and covered by fourteen tests.
3. **Runtime Cell Engine**: Implement client-side dynamic cell insertion and CodeMirror editor mounting in `assets/tutorial-runtime.js`.
4. **Peer Problem Serialization**: Extend export/import tools to package student-authored problems into portable JSON snippets.

Steps 3 and 4 are the ones still open, and they are the two that need runtime
work rather than content. Nothing written so far depends on them: every page of
problems in the repository is static, which was the point of doing them in that
order.

One thing the static pages settled that this document assumed would need code:
**a practice page does not need `check()` under every question.** What it needs
is a few tools per section and the answer behind a fold. Sixty CodeMirror
instances on a page is a slow page, and a check under every question invites
running it instead of thinking about it.
