# The topic map

The topic tree (*tree.html*, drawn from `planning/curriculum/topics.yaml`) is
to be replaced by a map with levels: subjects like countries, districts inside
them, topics as towns, and a topic's own pages as its streets. This document
says what the new map holds, how it was found, what Josh has to decide, and
how it gets built. The working folder is `planning/topic-map/`; its
`design.md` has the full technical and interaction design, and
`graph-final.json` the proposed map itself.

Status, 28 September 2026: **proposed, not decided.** Nothing the build reads
has changed. The prototype, built from `graph-final.json`, is the dewlab
Atlas (a private claude.ai page; ask for the link).

## Why the tree goes

The tree has two things to show, subject and prerequisite depth, and one axis
a scrolling page can use. It gave depth the vertical and made subject a
coloured stripe, so neighbours on the page share nothing but a depth count
("Organising data" sat between "Venn diagrams" and "The Sine Rule"). Rows
wrap five across, so its 143 arrows run through a grid as a hairball. And the
data under it had drifted:

- 81 of 274 pages claimed no topic. The Zen of Slashes and Surds and Full
  Stack did not appear at all, and there was no fractions topic anywhere.
- Topic size was wildly uneven: "Styling pages with CSS" took in 20 pages.
- A topic linked to the first tutorial claiming its *outcome*, so topics split
  from one outcome shared a link ("Standard deviation" went to the section on
  averages; "Solving quadratics" to the complex-numbers page).
- 139 of 142 nodes were "taught", so the legend distinguished nothing, and
  "How the tutorials relate" beneath it showed one series of forty.
- It knew nothing of where a learner had been.

## What the map holds

| | The old tree | The proposed map |
|---|---|---|
| Topics | 142, one per outcome or part of one | 185, found from what the pages teach |
| Pages placed | 193 of 274 (by `covers:` claims) | all 274 |
| Grouping | 6 columns in `strands.yaml`, unused by the tree | 11 regions, 41 districts |
| Ideas never named before | — | 56 topics with no old equivalent |
| Not ideas | mixed in as topics | 32 landmarks (projects, orientation, review); 9 outcomes culled to landmarks or teacher-only metadata |
| Planned, no page yet | 1 | 2 |

The regions and their districts (topics in brackets):

- **Number:** Number basics (3); Fractions (7); Powers (6); Roots and logarithms (7)
- **Logic and binary:** Numbers in a computer (4); Sets and logic (4)
- **Algebra and graphs:** Letters and expressions (3); Solving equations (5); Quadratics (4); Functions and their graphs (4); Grids and straight lines (4); Calculus (5)
- **Shape and space:** Measuring shapes (3); Triangles and trigonometry (5); Matrices and 3D pictures (5)
- **Chance and data:** Counting and chance (4); Chances that combine (4); Data, charts and averages (5); Simulations and models (5)
- **Machine learning:** Machines that write (3); Machines that learn (3)
- **Programming:** Starting with Python (4); Decisions and loops (4); Writing functions (4); Lists, grids and dictionaries (3); Algorithms (5); Objects and classes (5)
- **Making software:** Finding and fixing mistakes (3); Programs for people (5)
- **Databases:** Tables and queries (4); Linked tables (5); Data in and out (4)
- **Building web pages:** HTML: the parts of a page (6); CSS: how a page looks (6); Layout and screen sizes (7); Movement and interaction (6)
- **Websites and browsers:** Your tools: an editor and GitHub (5); Publishing and fixing a site (4); How a browser works (5); Pages everyone can use (4); Building a whole site (3)

The levels on screen follow the data: region names from far out, district
names at middle zoom, every town closer in, and a selected town's pages as
streets at the closest. A page that is not an idea is a landmark beside the
towns it draws on; a "closer look" page is a side street of the topic whose
misconception it tackles; a context page is a side street of its owner's
topic, unless it teaches an idea other topics need, in which case it is a
town (the cascade, how Git keeps history, how a browser fetches a page).

## How it was found

`BRIEF.md` in the working folder is the rule book the agents worked to. Its
centre is one sizing rule: **a topic is about the same amount of effort for
the learner arriving at it**, one to three sittings, where a sitting is about
one median page. Near the start a step as small as "adding fractions with
different denominators" is a whole topic, because that is where a beginner
sticks; deep in, "Matrices" can be one topic, because the learner arriving
there carries earlier ideas as chunks. Content grows with depth; effort stays
level. Around it sit the split, merge, step-not-topic and not-a-topic tests,
and the rule for prerequisites: a need means *you cannot sensibly start this
without that*, since every need closes a door.

The run (`search.workflow.js`) had one agent search each of six areas from
the pages up and then from the learner down, one integrate the six into
regions, three critics review the result (size, needs, the learner's eye and
completeness), and one revise: 39 of the critics' 42 findings were applied.
Every stage had to pass `validate.py`, which checks that every page is
placed, needs resolve and form no cycle, and every descriptor outcome is
served or culled with a reason. The earlier plan of two blind searches per
area, so that agreement between them could count as evidence, was cut to one
to save tokens; the map therefore has no "found twice" signal.

One caveat on the size rule: most maths and programming topics have two to
four parallel routes, one per course, and the validator's effort table adds
them together. Counted on one route, effort runs from about 950 to 1,500
words a topic near the start to about 2,000 to 2,950 deep in, which is the
shape the rule asks for. Question 8 below would make that visible on the map.

## Decisions for Josh

Each has a recommendation; the evidence is in `graph-final.json` under
`questions`.

1. **Eleven regions.** Keep Logic and binary apart from Number, Machine
   learning apart from Chance and data, the web as two regions, and Making
   software as a small region of its own? *Recommended: eleven as drawn;
   at the widest zoom only region names show, so these are how a learner
   finds testing, binary or machine learning.*
2. **Ten web context pages as towns** (the cascade, Git's history, the four
   "How a browser…" pages, who reads a page, colour contrast, keyboards,
   where a form's answers go), plus how a computer stores a number.
   *Recommended: towns, since a learner looks for "the cascade" by name.*
3. **Truth tables before Venn diagrams?** Your pair answer says so; the
   integrated course teaches Venn first. *Recommended: no need either way.*
4. **The derivative needing expanded brackets?** Your game answer says so;
   the four derivative pages never expand. *Recommended: no need.*
5. **Kinds of data before averages?** `decisions.yaml` says so; both courses
   teach averages first. *Recommended: no need either way.*
6. **Combining chances:** two topics (and/or/not; conditional) or the three
   `decisions.yaml` settled? *Recommended: two.*
7. **Team programming** (PDP-LO12): a topic, or teacher-only metadata?
   *Recommended: a topic, "Building software as a team".*
8. **Tag each step with its courses,** so a town shows the learner's own
   route first and the size check counts one route? *Recommended: yes.*
9. **Gaps with no page:** decimals, percentages and ratio; multiplying
   negative numbers; kinds of triangle; information theory; COUNT and
   GROUP BY; HTML lists and tables; vectors and nearest neighbours.
   *Recommended: keep the two planned towns and write GROUP BY and
   multiplying negatives first; four later towns lean on the latter.*
10. **All the power rules at once:** a review landmark or a topic?
    *Recommended: landmark.*
11. **The library loans quiz** assumes the college timetable page but sits
    before it in Database Methods. *Recommended: move it after.*
12. **Polynomials need Python lists,** because both teaching pages keep a
    polynomial as a list from the first cell. That puts the rest of algebra
    behind a first Python course and the derivative at depth 10.
    *Recommended: keep it, and plan a paper page on like terms for the Zen
    module, which removes the need.*

## How it gets built

`design.md` in the working folder has the whole design; its main choices
are these.

- **The map owns placement.** Topics list their pages in order, the way the
  course files own reading order. Tutorials lose their `covers:` blocks and
  nothing else: no cell or tutorial id changes, so no saved work moves.
- **Its own folder.** Regions, districts, topics, landmarks, culled outcomes
  and a committed positions file, in a new top-level *map/* folder.
  `topics.yaml`, `strands.yaml` and `topic-groups.yaml` go in the last step.
- **Stable geography.** Positions are committed; a build places only new
  towns, near what they need, and never moves an old one.
- **One page.** *map.html* on the site's shell, with the full nested list of
  every town as its keyboard, screen-reader and no-script route; that list
  replaces "Browse by topic".
- **Progress that claims no more than it knows.** The map may say "you have
  run code here", never "done" or "you know this".
- **No bundle rebuild.** Nothing in the plan edits
  `assets/tutorial-runtime.js`.

The plan is eight PRs in order: the map's data and its checks; the geometry;
the page; progress; links from every tutorial and the course view; retiring
`covers:` and moving the Library's levels onto the new graph; the teacher's
coverage layer; and retargeting the topic editor and pair game before the old
files are deleted. `design.md` names each PR's tests and the documents it has
to update, lists the 23 decision-log entries it supersedes or amends, and
raises 13 further questions of its own.

Before the first PR: Josh's answers to the twelve questions above, and a pass
over `graph-final.json` for names and needs that read wrong to someone who
teaches from it. The Atlas's review layer marks the 25 towns the critics
created or reshaped, which is where to start.
