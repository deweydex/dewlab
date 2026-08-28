# Curriculum Writing Backlog & Coverage Roadmap

This file tracked the twenty-six outcomes proposed after the survey
correction on 23 August. All twenty-six are now written and released — see
[`STATUS.md`](./STATUS.md) §1 for the tutorial list and
[`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md) for the outcome-by-outcome
accounting, both of which are the current sources of truth for what is
taught. Nothing below should be trusted over either.

## What is actually left

`CURRICULUM_MAP.md`'s own generated summary is the honest count: **68 of
80** outcomes are in place, and the twelve still missing are all in the
`CMPS` module — *Computational Methods and Problem Solving 5N0554* — with
no proposal written for any of them yet:

`CMPS-LO1`, `CMPS-LO2`, `CMPS-LO3`, `CMPS-LO5`, `CMPS-LO6`, `CMPS-LO7`,
`CMPS-LO8`, `CMPS-LO9`, `CMPS-LO10`, `CMPS-LO11`, `CMPS-LO12`, `CMPS-LO13`.

`STATUS.md` §2, Phase 7, carries this in prose: the first target strand
(linear algebra) is written; the second and third folded into it. The
fourth — discrete simulation and Monte Carlo methods — and the fifth —
algorithmic complexity and systems modelling — are not started, and
between them cover the twelve outcomes above.

Practice pages for those strands, once written, are tracked in
[`EXERCISES.md`](./EXERCISES.md) §4 rather than here.

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
