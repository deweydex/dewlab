# The topic map

The topic tree (*tree.html*, drawn from `planning/curriculum/topics.yaml`) is
to be replaced by a map with levels: continents of subjects that share many
roads, subjects like countries on them, districts inside those, topics as
towns, and a topic's own pages as its streets. This document
says what the new map holds, how it was found, what Josh has to decide, and
how it gets built. The working folder is `planning/topic-map/`; its
`design.md` has the full technical and interaction design, and
`graph-final.json` the proposed map itself.

Status, 28 September 2026: **proposed, with Josh's answers to its twelve
questions applied** (see [Josh's decisions](#joshs-decisions)), and laid out
as continents (see [How the land is laid out](#how-the-land-is-laid-out)). Nothing the
build reads has changed, except that the library loans quiz moved in Database
Methods (decision 11). The prototype, built from `graph-final.json`, is the dewlab
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
| Topics | 142, one per outcome or part of one | 189, found from what the pages teach |
| Pages placed | 193 of 274 (by `covers:` claims) | all 274 |
| Grouping | 6 columns in `strands.yaml`, unused by the tree | 12 regions and 41 districts, on three continents, a starting island and two small islands |
| Ideas never named before | — | 60 topics with no old equivalent |
| Not ideas | mixed in as topics | 32 landmarks (projects, orientation, review); 9 outcomes culled to landmarks or teacher-only metadata |
| Planned, no page yet | 1 | 7, one for every gap |

The continents, their regions and the regions' districts (topics in
brackets; a district's count includes any of its towns on the plains):

- **The Island of First Steps** (where to start): the Tower of Unknowing; the
  Prerequisite Plains, where the 12 towns that need nothing first stand,
  whatever their country; and
  - **Your tools:** Your tools: an editor and GitHub (5)
- **The Old Country** (mathematics):
  - **Number:** Number basics (5); Fractions (7); Powers (6); Roots and logarithms (7)
  - **Algebra and graphs:** Letters and expressions (3); Solving equations (5); Quadratics (4); Functions and their graphs (4); Grids and straight lines (4); Calculus (5)
  - **Shape and space:** Measuring shapes (4); Triangles and trigonometry (5); Matrices and 3D pictures (6)
- **The New World** (programming and data):
  - **Programming:** Starting with Python (4); Decisions and loops (4); Writing functions (4); Lists, grids and dictionaries (3); Algorithms (5); Objects and classes (5)
  - **Making software:** Finding and fixing mistakes (3); Programs for people (4)
  - **Chance and data:** Counting and chance (4); Chances that combine (4); Data, charts and averages (5); Simulations and models (5)
  - **Machine learning:** Machines that write (3); Machines that learn (3)
- **The Wide Web** (the web and databases):
  - **Building web pages:** HTML: the parts of a page (7); CSS: how a page looks (6); Layout and screen sizes (7); Movement and interaction (6)
  - **Websites and browsers:** Publishing and fixing a site (4); How a browser works (5); Pages everyone can use (4); Building a whole site (3)
  - **Databases:** Tables and queries (4); Linked tables (5); Data in and out (4)
- **The Isles of Yes and No**, two small islands:
  - **Logic and binary:** Numbers in a computer (4); Sets and logic (4)

The levels on screen follow the data: continent names from far out, then
region names, district names at middle zoom, every town closer in, and a
selected town's pages as streets at the closest. A page that is not an idea is a landmark beside the
towns it draws on; a "closer look" page is a side street of the topic whose
misconception it tackles; a context page is a side street of its owner's
topic, unless it teaches an idea other topics need, in which case it is a
town (the cascade, how Git keeps history, how a browser fetches a page).

<a id="how-the-land-is-laid-out"></a>
### How the land is laid out

**Which countries share a continent comes from the roads between them.**
`planning/topic-map/continents.py` counts the needs between every pair of
regions and tries every way of splitting the regions into groups, ranking the
splits by modularity: how much more often a need stays inside its group than
it would by chance. Three groups come out on their own, with no number of
continents asked for:

| Continent | Regions | Topics | What ties it |
|---|---|---|---|
| The Old Country | Number, Algebra and graphs, Shape and space | 65 | Shape needs algebra 8 times, algebra needs number 5 times. |
| The New World | Programming, Making software, Chance and data, Machine learning | 56 | Making software needs programming 11 times, chance and data 7, machine learning 4. |
| The Wide Web | Building web pages, Websites and browsers, Databases | 55 | Websites need web pages 17 times; nothing on it needs anything on the other continents. |

The best split (modularity 0.553) puts Logic and binary with the New World;
the next best (0.550) puts it with the Old Country. It sits between the two,
needing number once and programming twice, so it is neither: it became the
Isles of Yes and No, two small islands in the sea between them, one for each of
its districts. Maths and programming are the only two continents with roads
between them (11, most of them shape and algebra needing Python). The Wide
Web has none: it joins the rest of Comath only through the starting island.

**The starting island is the one continent placed by hand.** It holds the
tower, the Prerequisite Plains and the Tool Market, a twelfth country made
from the district "Your tools: an editor and GitHub", which used to be part of
Websites and browsers. A country cannot cross the sea, and the editor and the
GitHub account are the first things a web learner picks up, so the tools
stand beside the tower. One of its towns, *How Git keeps history*, needs a
town on the Wide Web, so one road leaves the island and comes back.

**The map is drawn from the outside in** (`layout.py`). First the continents
go round the island, each a disc of its size, a sea apart, drawn towards the
island and towards the continents they share roads with. Then each
continent's countries get a home on it, and each country's districts a home
in it, turned to face what they have roads to: Python City faces the island,
because the plains' first lines of Python lead there. Only then do the towns
settle. Every town pushes the others away, harder across a border and hardest
across the sea. A prerequisite pulls like a spring. Each town is drawn to the
middle of its county and its country, and depth is a gentle pull away from the
tower, so that usually the further a town is from the tower, the more it
needs. Each country is split into counties (its districts) with dotted
borders, and each continent has one family of hues, which its countries
share. An earlier layout put every country round one island and fixed each
town's distance from the middle by its depth, which turned a long chain of
prerequisites into a spike.

**A road between two continents crosses the sea on a bridge.** There is one
bridge for each pair of continents with roads between them, placed where it
keeps those roads shortest, and every road across that sea is drawn through
it, so roads gather at a bridge as they do on a real map. Six bridges carry
43 roads: the island to the Old Country (14), to the Wide Web (12), to the
New World (3) and to the Isles (1), the Old Country to the New World (11),
and the New World to the Isles (2). Two continents without a bridge of their
own are joined by way of the island.

### The map's voice

The map introduces itself as **Comath, the land of maths and computing**:
countries, towns, roads and landmarks, with the Tower of Unknowing in the
middle where every traveller starts, and the Prerequisite Plains around it
(the towns that need nothing first). Each region has a whimsical name with its
real name beside it, "Python City (Programming)", and so does each continent,
"The Old Country (Mathematics)". The tower keeps the orientation pages. The fantasy is in the framing, and it follows the style guide's rule
that a metaphor comes after the plain statement, never instead of it
(`PEDAGOGICAL_STYLE_GUIDE.md#plain-language`). So the page first says what the
map is in plain words, and only then uses the land's voice. Each region has a
plain `blurb` and, after it, one line of `lore` in `graph-final.json` ("Chance
and data: probability, statistics, charts and simulations. *Nothing in this
country is certain, but some things are very likely.*"). The words stay
common ones, with no archaic ones like "realm" or "yonder", because a reader
may be working in a second language. Town names stay plain, because decision
1 relies on a learner finding "binary" or "testing" by name.

Every name was checked against its neighbours. The Isles of Yes and No are two
islands. The Triangle Mountains border the Valley of the Missing X and are
drawn with small peaks, and the Forest of Learning Machines with trees. Browser
Harbour is on the Wide Web's coast, where the bridge from the island lands.
Python City, "the biggest city in the land", takes the island's bridge to the
New World. The lore agrees across levels: the Counting Kingdom is the oldest
country and stands in the Old Country; Machine learning is the youngest
country and stands in the New World, where "nothing is more than a hundred
years old".

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

<a id="joshs-decisions"></a>
## Josh's decisions

Answered 28 September 2026. The questions, with their evidence and the
options offered, stay in `graph-final.json` under `questions`, each now with
its `answer`. Ten follow the recommendation; decisions 7 and 9 do not, and
changed the map.

1. **Regions:** eleven, as drawn. (Later twelve: laying the map out as
   continents gave the tools district a country of its own on the starting
   island. See [How the land is laid out](#how-the-land-is-laid-out).)
2. **Web context pages:** towns of their own.
3. **Truth tables and Venn diagrams:** no need either way.
4. **The derivative and expanded brackets:** no need.
5. **Kinds of data and averages:** no need either way.
6. **Combining chances:** two topics, and/or/not together and conditional
   probability apart.
7. **Team programming** (PDP-LO12): teacher-only metadata. Its town is off the
   map; the team briefs stay as landmarks beside planning, testing and readable
   code.
8. **Courses on steps:** yes. Each step carries its courses, so a town shows a
   learner their own route first and the size check counts one route. The
   design builds this into the map's data.
9. **Gaps:** a planned town for every one. Five were added beside the two
   already there: decimals, percentages and ratio; multiplying negative
   numbers; kinds of triangle; lists and tables in HTML; comparing rows of
   numbers (which brings CMPS-LO4d back from the culled list). No existing
   town needs a planned one, because directions would then send a learner
   through a page that does not exist. Inverse functions, complex numbers and
   inequalities lean on multiplying negatives; those needs are added when its
   page is written.
10. **All the power rules at once:** a review landmark.
11. **The library loans quiz:** moved to the end of "A database with several
    tables" in `courses/database-methods.yaml`, after the college timetable it
    assumes.
12. **Polynomials and Python lists:** the need stays, and a paper page on terms
    and like terms is planned for the Zen module, which will remove it.

Pages this sets to write, in order: multiplying negative numbers and COUNT
with GROUP BY first, then the paper page on like terms, then the other
planned towns.

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

Before the first PR: a pass over `graph-final.json` for names and needs that
read wrong to someone who teaches from it. The Atlas's review layer marks the 25 towns the critics
created or reshaped, which is where to start.
