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

## What it showed

Both judges ran the same 95 pairs twice, sighted and blind.

| | backs the existing arrow | unrelated | level |
|---|---|---|---|
| Ruth, sighted | 74/95 | 20 | 0 |
| Ruth, blind | 68/95 | 19 | 7 |
| Tom, sighted | 73/95 | 20 | 0 |
| Tom, blind | 66/95 | 18 | 9 |

**No judge reversed a single arrow.** Across 190 sighted judgements and 190
blind ones, not one pair that both runs ordered came out pointing the other
way. The directions in the graph are not an artefact of the judges having seen
them.

**Every level came from the blind run.** Sighted, across 190 judgements, the
answer "these two need each other" was used no times at all. Blind, it was used
sixteen. Thirteen of those are pairs the same judge had ordered when they could
see an arrow.

So the answer key does bias a judge, but only in one direction: an arrow on the
page stops them noticing that the two topics are mutual. It does not talk them
into the arrow's direction. That is worth knowing, because it says which half
of the first run can be trusted and which half has to be redone blind.

Six levels were found independently by both blind judges:

- What an algorithm is + Algorithms in the real world
- The parts of a program + The instructions a program is built from
- Selection and iteration + The instructions a program is built from
- The history of programming + Comparing languages
- Computer simulation + Modelling versus simulation
- Index and sigma notation + Iterating by index

Five of the six straddle a module boundary, where one descriptor restates
another descriptor's topic in its own words. That is the same thing both judges
flagged in prose when asked which topics needed rethinking.
