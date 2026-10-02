# The topic map's data

`map.html` draws every topic as a town on a map. This folder holds what it draws.

| File | What it is | Who writes it |
|---|---|---|
| `graph.json` | The map itself: continents, countries (regions), districts, topics with the pages that teach them and what they need first, landmarks, and the words that go with them. | A person. |
| `layout.json` | Where everything goes: each town's place, the land, the sea, the bridges. | `python3 dev/map_layout.py`. Do not edit it by hand. |

The build reads both files and the tutorials. A page's title, its section
headings and the courses it is on come from the tutorial, not from here, so a
renamed page cannot leave a wrong name on the map.

## When the build refuses

The build stops, and names the problem, when:

- a topic or a landmark names a tutorial that does not exist;
- a topic names a section that the tutorial does not have;
- a topic needs something that is not a topic;
- a topic is in `graph.json` but not in `layout.json`, or the other way round.

The last one means the map changed and the layout did not. Run
`python3 dev/map_layout.py` and commit `layout.json`. It takes about ten
seconds and gives the same layout for the same graph. A change to the graph
settles the whole map again, so it can move towns that did not change. Check
`git diff --stat map/layout.json` before committing. Keeping old towns still
while a new one is placed is planned (`planning/topic-map/design.md`, 2.4) and
not built.

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

The reasoning behind all of this is in `planning/TOPIC_MAP.md` and
`planning/topic-map/design.md`, and the decision is `DECISIONS_LOG.md` 7.293.
