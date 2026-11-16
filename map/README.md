# The topic map's data

`map.html` draws every topic as a town on a map. This folder holds what it draws.

| File | What it is | Who writes it |
|---|---|---|
| `graph.json` | The map itself: continents, countries (regions), districts, topics with the pages that teach them and what they need first, landmarks, and the words that go with them. | A person. |
| `layout.json` | Where everything goes: each town's place, the land, the sea, the bridges. | `python3 dev/map_layout.py`. Do not edit it by hand. |

The build reads both files and the tutorials. A page's title, its section
headings and the courses it is on come from the tutorial, not from here, so a
renamed page cannot leave a wrong name on the map.

## The list under the map

`map.html` also writes every topic as a list, for a reader with no script, a
screen reader or a keyboard. It is also the part of the page below the picture,
so it is written to help a student choose a path. It has three ways in:

- **Follow a course.** One fold for each course, with the topics the course
  teaches in the order it teaches them. The order comes from the course file, not
  from `graph.json`.
- **Places to begin.** The topics that are taught and need nothing first, by country.
- **Browse by country.** Every country, with how many topics it has, what to begin
  with, which countries it uses topics from and which use its topics.

Each topic then names the pages that teach it, once each and in the order the
steps are written, with the sections it uses as parts. Steps with another role
(`closer-look`, `context`, `applies`) follow under their own label. A topic says
what it needs first, what it leads to (a list of more than four folds), and which
courses use it. A step that names a page twice is one entry, so list a page's
sections as separate steps without worrying about repeats.

## When the build refuses

The build stops, and names the problem, when:

- a topic or a landmark names a tutorial that does not exist;
- a topic needs something that is not a topic;
- a topic is in `graph.json` but not in `layout.json`.

It notes, and builds, when a topic names a section the tutorial no longer
has (the map links to the top of the page instead), and when `layout.json`
places a topic `graph.json` no longer has (it is ignored).

A topic with no place in the layout means the map changed and the layout did not. Run
`python3 dev/map_layout.py` and commit `layout.json`. It takes about ten
seconds and gives the same layout for the same graph. A change to the graph
settles the whole map again, so it can move towns that did not change. That is
accepted: the map may change. Check
`git diff --stat map/layout.json` before committing, and say in the pull
request that the map moved.

## Changing the map

**A tutorial is not on the map yet.** The build says so in a note. Add it as a
step of the topic it teaches, with the role `teaches`, or as a landmark.

**A step.** `{"tutorial": "<id>", "section": "<anchor or null>", "role": "teaches"}`.
The roles are `teaches`, `closer-look`, `context` and `applies`.

**A topic needs another.** Add its id to `needs`. A need means *you cannot
sensibly start this without that*, because every need closes a door
(`planning/topic-map/BRIEF.md` has the rule).

**A new topic, district or country.** Add it to `graph.json`, then run the
layout script. A country must be on exactly one continent. The first
continent of kind `start` is where the tower and the Prerequisite Plains
are, and the towns that need nothing first stand on the plains.

**Which countries share a continent** is not decided by hand. Run
`python3 planning/topic-map/continents.py map/graph.json` to see the matrix of
needs between countries and the groupings with the highest modularity.

`python3 planning/topic-map/validate.py graph map/graph.json` checks the
graph against the pages and the course outcomes (it needs
`python3 planning/topic-map/inventory.py` first).
