---
name: triage-report
description: Work an issue opened through dewlab's own report doors (the footer's three-doors disclosure, or a cell's report icon) — decide what kind of thing it actually is, reproduce it, check for a duplicate, and either fix it, escalate it, or say why not. Use when asked to triage, work through, or clear the report inbox, when handed one such issue directly (including via an `@claude` mention), or when picking up an issue labelled `pattern`.
---

# Triaging a student report

An issue from the report doors (DECISIONS_LOG.md Phase 8) has a fixed shape: `page` and `version` always filled in; `kind` one of the issue template's three options; `cell`, `code`, `output` and `browser` only when it came from a cell's report icon; and whatever the student typed under "What happened." Every report ends as a fix, a redirect, or a stated reason nothing changes yet. Never close one silently.

## Read first

1. The issue in full, noting which fields are empty. A filled `code` with an empty `cell` means it was filed by hand, so there is no cell to reproduce against.
2. The page at the version named: `tutorials/<id>/<id>.md` for the current release, `v<version>.md` beside it for an older one. A report against a frozen version is real, but the fix goes on the current release unless the report is about the archiving.
3. Open issues naming the same page. The same page and cell is very likely the same problem: say so on the newer issue and point it at the older one.

## Decide the kind

The student's choice of door is a guess. Re-sort before acting.

- **A question, an idea, or something else.** It belongs in Discussions. Answer briefly if the answer is short, or say you are moving it, then convert it. No PR.
- **It gives an error.** Reproduce first (below).
- **The page is wrong, or I could not follow it.** A factual mistake is usually one line. For "could not follow", run the checks in `PEDAGOGICAL_STYLE_GUIDE.md#plain-language` over the passage before touching it.

## Reproduce an error

With `code` and `output` present you rarely need Pyodide. `output` is the traceback `_format_exception()` produced and `render_error()` showed, trimmed to the student's own line. Compare `code` with the cell's starter code in the tutorial's markdown:

1. **The starter code is broken.** Fix it in the markdown, keeping the cell's `id` exactly as it was. Run `python3 build.py` and open the built page to confirm the cell runs clean.
2. **The student's edit caused it, and the tutorial gave no warning.** This is a prose gap. Add a sentence about the mistake or a `hint:` in the cell header. Leave the starter code alone.
3. **The student's edit caused it, and the tutorial already covers it** (a hint exists, or a note in `_ERROR_HINTS` in `tutorial_tools.py` names this mistake). Nothing to fix. Say so on the issue.

If you cannot tell which without running it, build and open the page locally rather than guessing from the text.

## Fix it

One pull request per issue, naming the issue number. `docs/WRITING_TUTORIALS.md` and the style guide apply in full; a report relaxes neither. Run the plain-language checks on any prose fix before the PR opens. Never rename a cell `id`.

## Escalate instead

- **A mathematics or curriculum question**, meaning whether an explanation is correct and not just clear, is confirmed by Josh. Say what you think is wrong and propose the fix, but do not merge a change to what a tutorial claims is true.
- **Anything beyond the page the report named**: a pattern across tutorials, a runtime change, a change to `build.py`. Comment what you found and open separate, scoped work instead of widening this PR.
- **Closing.** Nothing closes until a person has seen it, unless you are that person and are looking right now. A merged fix is not a closed issue.

## A `pattern` issue

The weekly job (`.github/workflows/report-patterns.yml`) opens one to gather several reports. It can only count, so the diagnosis is yours. Read every issue it links and decide whether a later fix already covered some of them (compare timestamps with the fix's merge date), whether they share a root cause, and whether the response is a wording fix, a tutorial redesign, or a runtime change. Say which on the pattern issue before doing the work.

## Two things never to do

Do not mark a report resolved as a duplicate of something already fixed until you have confirmed the fix covers the reported case; a similar report can be a new edge. Do not disable or narrow the report doors (`planning/feedback.yaml`) to handle a flood of reports. That decision is Josh's.
