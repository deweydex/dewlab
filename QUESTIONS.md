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

*Nothing waiting.*
