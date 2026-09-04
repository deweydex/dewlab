# The blind run

The judgements in `../pairs/` were made by judges who could read
`planning/curriculum/topics.yaml`, and that file carries the `needs:` lists.
They were auditing a graph while looking at it. The pair list they worked from
made it worse: it named the current prerequisite first in all 95 pairs, so a
judge who always picked the left-hand topic would have agreed with the graph
95 times out of 95.

This directory holds the control. The same 95 pairs, the same judges, the same
access to the tutorials, with two things changed:

- the topics file they read has no `needs:` in it at all
- each pair is listed in a random order, so the listing says nothing

Everything else is held constant, so a difference between the two runs is
down to the answer key rather than to having less evidence to go on.

`dev/pair_results.py` reads `../pairs/` and not this directory. The blind
judgements are evidence about the method, and mixing them into the same pile
would lose the comparison that makes them worth having.
