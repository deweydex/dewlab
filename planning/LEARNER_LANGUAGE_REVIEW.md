# Learner language review

## Purpose

This review aims to make dewlab clearer for adults reading at about B1
English level. Invitations need specific things to try. Reassurance
needs a useful route to help. Learners can pause, use a hint, read an
answer, or return to an earlier explanation.

The [pedagogical style guide](PEDAGOGICAL_STYLE_GUIDE.md) remains the
writing guide. This review applies it through questions a learner may
have. B1 is the intended audience, not a rating established by a score.

## Questions for each page

| Learner's question | What the page needs |
|---|---|
| Why might I want to learn this? | A concrete purpose or example. |
| Where can I begin? | A starting point, with any setup or earlier knowledge explained. |
| What does this mean? | Common words, connected sentences, and technical terms explained where they appear. |
| What could I try? | A specific invitation with enough information to act. |
| What might happen? | An expected result and a way to notice changes. |
| What can help if I get stuck? | A hint, worked answer, earlier explanation, or person to ask. |
| Can I pause or choose another way? | Space to return, repeat, read an answer, or take a break. |
| What happens to my work? | Accurate saving, reset, sharing, and assessment information. |

Common words and explicit steps support reading without removing the
technical ideas. Short button labels can stay direct. Activities explain
what a learner could try and what they might notice. Adding "you can"
to every sentence is not the aim.

## First batch, 2026-09-05

Prepared as one coordinated commit for upstream review, following the
same approach as dewstack's entry-page review. The saving and reporting
explanations need to agree across these pages. This is not a claim that
all tutorials or documentation have been reviewed.

| Surface | Difficulty found | Change |
|---|---|---|
| Contents page in `build.py` | Commands, abstract explanations, and broad reassurance. | A starting route, specific experiments, choices about practice, and practical help. |
| About page in `build.py` | Broad saving claims and a promise to merge proposed changes. | Clear learning routes, accurate sharing and saving explanations, and proposals described as reviewable. |
| `README.md` | Technical density, absolute privacy claims, and stale content counts. | A teacher/contributor overview with plain explanations and links to maintained status and coverage records. |
| `docs/FOR_STUDENTS.md` | Feature detail before first-use help; reset and download options were unclear. | First-use guidance, learner choices, and separate explanations for saved work, added cells, and published downloads. |
| `docs/FAQ.md` | Commands and promises about saved work, ability, and privacy. | Direct answers, flexible routes, and qualified explanations of storage and sharing. |
| `docs/REPORTING_A_PROBLEM.md` | Reporting felt conditional on diagnosis; reset was presented as proof of fault. | Optional checks, concrete report examples, and an explanation of when code is sent to GitHub. |
| First Steps in maths and programming | Dense opening, broad claims, and references to text cells that did not exist. | A simpler opening, expected first result, notes guidance, and a choice about making predictions. The rest of this tutorial still needs a full prose pass. |
| Shared Settings text in `assets/shell.html` and download text in `build.py` | Saving and download promises did not distinguish the controls. | Accurate descriptions at the point where learners choose a control. |
| Contributor audience guidance | It described a teenage audience, conflicting with the adult-learning guide. | Adult B1 readers, with the same invitational goals. |

## Behaviour checked before writing

The explanations were checked against `assets/tutorial-runtime.js`,
`assets/shell.html`, and `build.py`:

- Tutorial-cell edits, notes, and results are stored in browser storage.
  Large results can be omitted when storage is full. Saving can fail.
- Export a copy reads the saved tutorial-cell record and notes. It does
  not include added cells. If saving fails, copying text elsewhere is a
  clearer recovery route than promising that export has captured it.
- Added cells have separate storage and Share files. The notebook export
  includes all current cell code and text, without results or the reading.
- A cell's reset restores its starter code and clears its output. It does
  not restart Python. Start again clears tutorial-cell edits and notes,
  after confirmation, and leaves added cells in place.
- Saved results do not recreate values in a new Python session.
- Download to keep links to the published reading and starter code. It
  is separate from saved-work exports.
- Cell report links include current code, output, and browser information.
  Opening the form sends those details to GitHub in the URL. Submitting
  posts the report. Long code and output can be shortened.

No executable cell code, cell identifiers, tutorial frontmatter, or
runtime behaviour changed. The build and shell edits change text and
links only. The code walkthrough notes where this text lives.

## Further batches

1. Finish First Steps and review the other introductory tutorials in
   teaching order, including activities, hints, and answers.
2. Continue through later tutorials and practice pages in small batches.
3. Review glossary definitions, the topic tree, and remaining generated
   interface text. The earlier language record lists known issues.
4. Review the dewmini guide and its interface together, with attention to
   its different saving and file controls.
5. Review author, teacher, and contributor documentation for clear
   prerequisites and procedures, while keeping necessary technical detail.
6. Invite learners to use the drafts. Useful questions include "Where
   would you begin?" and "What could you do if this did not work?"

For each batch, record the current passage, possible learner difficulty,
proposed wording, and factual checks. Sentence measurements flag passages
to read again; they do not establish understanding or English level.

## Validation

- Full `python3 build.py --clean` build: 263 pages, including downloadable
  copies. The existing missing-vendored-Pyodide notice means the dewmini
  bundle loads Python from the CDN on first use.
- Unit suite: 487 passed, 1 skipped. The runtime end-to-end suite was not
  run; this change preserves executable cell code and runtime behaviour.
- Document-link check: 71 documents, no stale references.
- Curriculum map, topic game, topic editor, and pair-report checks pass.
  The vocabulary map was regenerated because it also reads tutorial prose.
- First Steps code blocks, cell identifiers, and frontmatter match the
  base commit exactly. Its existing introduction test now checks the
  introductory region and starting link rather than requiring a command.
- Sentence review of the main guides: average lengths around 11 words.
  The rendered contents introduction and About page were also read and
  measured. The remaining First Steps prose is not marked as reviewed.
- Ruff on the changed Python files: no new findings compared with the
  base commit. Existing findings remain: 13 in the build and 7 in its
  tests. Explicit parentheses around the edited introduction's adjacent
  string literals remove 9 existing findings without changing values.
- Chromium at 1200 and 390 pixels: contents, About, and First Steps have
  no horizontal overflow, one main landmark, and one h1. Screenshots were
  captured at both widths. Settings opens from the keyboard and Escape
  closes it and returns focus to the button.
- Axe-core 4.10.3 and keyboard checks were compared with an unchanged
  archive of main in the same environment. The contents page has no axe
  violations. About has an existing duplicate-landmark finding. First
  Steps has the same existing editor-label and contrast findings at both
  widths, with the same affected-element counts. Navigation labels and
  moving focus into Settings also remain follow-up work. These browser
  checks do not claim an accessibility pass for the whole site.
- `git diff --check`: no whitespace errors.

The checks used temporary dependencies, fonts, and browser files outside
the repository. No project dependencies changed. Comprehension with
learners remains a review step.

## Accessibility follow-up found during this review

The unchanged base and the review branch show the same issues. A separate
interface review can address them together:

- Give code editors accessible names, including read-only code examples.
- Improve contrast for editor text, cell controls, and related links.
- Name repeated navigation landmarks so they can be distinguished.
- Decide and implement the focus behaviour when Settings opens.

The language commit leaves those controls and styles unchanged. The
baseline comparison keeps these known issues visible without treating
them as regressions caused by the new prose.
