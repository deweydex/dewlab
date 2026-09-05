# What's left to write (retired — see below)

This file tracked the twenty-six outcomes proposed after the survey
correction on 23 August. All twenty-six are now written and released — see
[`STATUS.md`](./STATUS.md) §1 for the tutorial list and
[`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md) for the outcome-by-outcome
accounting, both of which are the current sources of truth for what is
taught. Nothing below should be trusted over either.

## What is actually left

Nothing. `CURRICULUM_MAP.md`'s own generated summary is the honest
count: **91 of 91** outcomes are in place, across all four accredited
modules — *Mathematics for IT*, *Programming and Design Principles*,
*Fundamentals of Object Oriented Programming*, and *Computational
Methods and Problem Solving*. The twelve `CMPS-LO*` outcomes this file
used to list as missing were closed across five new tutorials (a
perceptron, a queue simulation, a coin-change strategy comparison, a
folder-tree recursion tutorial, and a debugging tutorial) plus small
additions to two existing ones — `planning/STATUS.md` §2 has the detail,
including a loose end that doesn't block the outcome count but is
worth knowing about: the link-graph strand's crawl is still just a
worked example, deliberately, in favour of a Markov-chain text-
generation series built instead. (The other loose end this line used
to name, no tutorial using real data, closed on 2026-09-05 — see
`STATUS.md` §2 and `ROADMAP.md`'s Phase 2.)

## Why this file stops here

Keeping a hand-written duplicate of a count that `CURRICULUM_MAP.md`
already generates from the outcome files, and that `STATUS.md` already
narrates, is exactly the drift this file itself fell into — it went stale
within days of the last big batch of writing landing, still listing
tutorials as outstanding that had already shipped. Rather than rewrite it
to match today's numbers, it now points at the two documents that cannot
go stale the same way: one is rebuilt by CI on every push, the other gets
updated in the same commits that do the writing.

The original twenty-six-outcome backlog, superseded rather than deleted,
is still readable in git history at the commit that retired this file.
