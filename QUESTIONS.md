# Questions for Josh

Where the scheduled build sessions put decisions they cannot make alone, and
where the answers come back.

Sessions run unattended every six hours and work through
`planning/BUILD_PLAN.md`. They have git and no GitHub API, so this file — not
an issue, not a PR thread — is the running list. Three times a day a short
session reads it and notifies Josh only if something is unanswered. Silence
means nothing is waiting on him.

## For a session writing a question

Never stop to wait for an answer. Add the question here, record the assumption
you shipped in the meantime, and carry on with everything the question does not
block. Then commit and push, so the next reader sees it.

Add entries under **Open**, newest last, numbered in sequence. Each one says, in
prose: what is being asked, concretely enough to answer without opening the
repo; what you assumed and shipped meanwhile, so that "that's fine" costs Josh
nothing; what changing it later would cost, in the manner of `DECISIONS_LOG.md`;
and what it blocks, if anything. A question only its author can understand is a
note, not a question.

## For a session reading an answer

Answered questions come before new work. Act on the answer, record the outcome
in `DECISIONS_LOG.md` as a numbered entry, move the question down to
**Answered** with what you did, and push.

## For Josh

Answer wherever suits — in this file directly, or by telling whichever session
you are talking to, which will write it down here. An answer of one line is a
complete answer.

---

## Open

**1 — How should `build.py` render math?**

DECISIONS.md settles KaTeX, rendered at build time rather than in the student's
browser, and names markdown-it-texmath as the toolchain. That toolchain is
JavaScript and `build.py` is Python. `assets/vendor/` carries KaTeX's stylesheet
but no KaTeX JavaScript, so there is no client-side fallback to lean on either —
whatever produces the markup has to run during the build.

Three ways out, in rough order of how much they cost. Shell out to Node from
`build.py`, using the KaTeX already pinned in `vendor-src/` — keeps the settled
toolchain exactly, at the price of Node becoming a build dependency for CI and
for any author previewing locally. Add KaTeX's JavaScript to the vendor bundle
and render in the browser after all — cheapest to build, but it reverses the
"no client-side LaTeX parsing cost for students" reasoning in DECISIONS.md.
Or find a Python LaTeX-to-HTML renderer that targets KaTeX's markup, which I
have not surveyed and would want to before recommending.

Shipped meanwhile: nothing. Phase 1's brief does not include math, so the
converter passes `$…$` through untouched as literal text. No tutorial written so
far contains any, and none should until this is settled, because a tutorial
written against the wrong mechanism has to be rewritten rather than rebuilt.

Cost to change: low now, higher later. Whichever way this goes, it is a change
to `build.py`'s rendering path and to `vendor-src/`, not to the cell or link
handling.

Blocks: any Mathematics for IT content, which is a quarter of the year-one
modules. Nothing in Phases 2 or 3.

**2 — Are the two sample tutorials meant to stay?**

Phase 1 needed one hand-written tutorial to test the converter end to end, so
`tutorials/computational-methods/first-steps.md` and `working-with-tables.md`
exist and build. They are written as real student-facing material rather than
as lorem ipsum, because a fixture that does not look like the real thing does
not test the real thing — but the teaching is a guess, and pedagogy is your
department, not mine.

Shipped meanwhile: both, as ordinary tutorials in the real tree.

Cost to change: none. Delete them, rewrite them, or keep them; the converter
does not care and no test depends on their content.

Blocks: nothing.

## Answered

*Nothing yet.*
