---
name: triage-report
description: Work an issue opened through dewlab's own report doors (the footer's three-doors disclosure, or a cell's report icon) — decide what kind of thing it actually is, reproduce it, check for a duplicate, and either fix it, escalate it, or say why not. Use when asked to triage, work through, or clear the report inbox, when handed one such issue directly (including via an `@claude` mention), or when picking up an issue labelled `pattern`.
---

# Triaging a student report

An issue from the report doors (DECISIONS_LOG.md Phase 8) has a fixed shape:
`page` and `version` always filled in, `kind` one of the issue template's
three options, `cell`/`code`/`output`/`browser` filled in only if it came
from a cell's own report icon rather than the page footer, and whatever the
student actually typed under "What happened." This is the procedure for
turning that into either a merged fix, a redirected report, or a clear
reason nothing changes yet — never a silently closed issue.

## First: read before acting

1. **The issue itself, in full**, including which fields are empty. An
   empty `cell` field with a filled `code` field never happens from the
   real doors — if you see it, the report was filed by hand rather than
   through a door, and the checklist below still applies, just without a
   cell to reproduce against.
2. **The page it names, at the version it names** — `tutorials/<module>/<slug>/<slug>.md`
   for the current release, or `v<version>.md` beside it for an older one.
   A report against a frozen version is still real, but a fix belongs on
   the current release unless the report is specifically about the
   archiving itself.
3. **Open issues carrying the same page** (search issues for the page
   string). Two open issues naming the same page and the same cell are
   very likely the same thing — say so on the newer one and close it as a
   duplicate of the older, rather than fixing the same thing twice.

## Deciding the kind — the student's guess is a starting point, not a verdict

The three doors sort by what the student *thought* they had. Re-sort
before doing anything else:

- **"A question, an idea, or something else" reaching you as an issue**
  (it should have gone to Discussions, but a hand-filed report or an old
  link can still land here) — answer briefly if the answer is short, or
  say you're moving it, then convert the issue to a discussion. This is
  not fixing code; do not open a PR for it.
- **"It gives an error"** — reproduce first (below). Half the time this
  is a real bug in the shipped cell; the rest is a mistake in the
  student's own edit, which `code` makes obvious immediately, or a gap in
  what the tutorial explained, which is a `WRITING_TUTORIALS.md`-level fix
  to the prose around the cell rather than to the cell itself.
- **"The page is wrong, or I could not follow it"** — a factual mistake
  (wrong answer, a broken link, a stale reference) or a plain-language
  problem. These need different tools: a factual fix is usually one line;
  a "could not follow it" report means running `PEDAGOGICAL_STYLE_GUIDE.md`
  §4's nine checks over the passage before touching it, not guessing at a
  rewrite.

## Reproducing an error report

With `code` and `output` present, you very often do not need Pyodide at
all: read the traceback in `output` (it is the exact text
`tutorial_tools.py`'s `show_error()` wrote, trimmed to the student's own
line the same way it always is) and compare `code` against the cell's
starter code in the tutorial's markdown. Three outcomes:

1. **The starter code itself is broken** — a real bug. Fix it in the
   tutorial's markdown, keeping the cell's `id` exactly as it was (cell
   ids are a contract — `CLAUDE.md`). Run `python3 build.py` and open the
   built page to confirm the fixed cell actually runs clean.
2. **The student's edit introduced the error, and the tutorial gave them
   no reason to expect otherwise** — this is a prose gap, not a code bug.
   The fix is a sentence warning about the mistake shape, or a hint
   (`hint:` in the cell's header), not a change to the starter code.
3. **The student's edit introduced the error, and the tutorial already
   covers it** (a hint exists, or `first-steps.md`'s "When a cell does not
   do what you expect" already names this exact mistake) — nothing to
   fix. Say so on the issue, closing it once you have, rather than
   leaving it open with no comment.

If you cannot tell which of the three without actually running it, build
and open the page locally rather than guessing from the text alone.

## Fixing it

- One pull request per issue, mentioning the issue number, same as any
  other change to this repository (`docs/REPORTING_A_PROBLEM.md`'s own
  "If you want to fix it yourself" section describes the same convention
  from a contributor's side).
- `docs/WRITING_TUTORIALS.md` and `PEDAGOGICAL_STYLE_GUIDE.md` govern the
  fix exactly as they would any other tutorial edit — a report does not
  relax either.
- Never rename a cell's `id`, even if the new name would read better.
- Never touch `site/` — it is rebuilt, not edited.
- A prose fix gets the nine plain-language checks run over it before the
  PR opens, not after a reviewer asks.

## What escalates instead of getting fixed on the spot

**A mathematics or curriculum question** — whether an explanation is
*correct*, not just whether it is clear — is confirmed by Josh, not
decided by an agent working through the inbox. Say what you think the
issue is and propose a fix, but do not merge a change to what a tutorial
claims is mathematically true without that confirmation.

**Anything that touches more than the one page the report named** — a
pattern across several tutorials, a runtime change, a change to
`build.py` itself — is bigger than this issue. Comment what you found and
open a separate, properly scoped piece of work rather than quietly
expanding this PR to cover it.

**Nothing closes without a person having seen it.** A fix merged is not
the same as an issue closed — leave it open (or note it explicitly)
until whoever is running triage has actually looked, unless you are that
person and are looking right now.

## Working a `pattern` issue

A `pattern` issue (opened by the weekly job — see the workflow in
`.github/workflows/`) gathers several reports rather than describing one
directly. Read every issue it links before deciding anything: the job can
only count, so the read is where the actual diagnosis happens — whether
a later fix already addressed some of the gathered reports (check
timestamps against the fix's merge date), whether they share a root cause
or are coincidentally on the same page, and whether the right response is
a wording fix, a design change to the tutorial, or a runtime change. Say
which, on the pattern issue itself, before doing the work — this is
exactly the kind of decision that benefits from being visible rather than
inferred from a diff later.

## Two things never to do

Never mark a report resolved because it looks like a duplicate of
something already fixed — confirm the fix actually covers the reported
case first; a similar-looking report can be a new edge the earlier fix
missed. Never disable or narrow the report doors themselves
(`planning/feedback.yaml`) as a way of handling a flood of reports — that
is a decision for Josh, not a triage step.
