# The topic map: working folder

Where the topic tree's replacement is being planned: a map with levels
(continent, region, district, topic, step) and a topic list rebuilt from what the pages
teach. Nothing here is read by the build yet.

| File | What it is |
|---|---|
| `BRIEF.md` | The rules every search agent works to: the levels, the size rule, needs, naming, ids, the file format. |
| `inventory.py` | Writes `generated/inventory.json` (every non-archived, non-practice page: headings, glossary concepts, courses, current claims, length, kind) and one file per search area, all under `generated/`. Run it first; that folder is not committed. |
| `validate.py` | Checks a proposal (`proposal <file> <area>`) or the whole map (`graph <file>`): every page placed, needs resolve and form no cycle, every descriptor outcome served or culled, and an effort-by-depth table for the size rule. |
| `search.workflow.js` | The multi-agent run: one proposer per search area, an integrator, three critics, a reviser. Writes its proposals and the integrated and revised map into this folder. (A heavier version, with two blind proposers and a reconciler per area, is in this file's history.) |
| `continents.py` | Prints the matrix of needs between regions and the groupings of regions with the highest modularity, which is where the continents in `graph-final.json` come from. |
| `layout.py`, `assemble.py`, `atlas.template.html` | Lay a graph out as continents round a starting island, with bridges between them, and build the clickable Atlas prototype from it: `python3 layout.py graph-final.json map.json`, then `python3 assemble.py atlas.template.html map.json "" atlas.html`. |

To run the search from a fresh checkout:

    python3 planning/topic-map/inventory.py
    # then run search.workflow.js with Claude Code's Workflow tool

Status, 28 September 2026: the search is finished. `graph-final.json` is the
proposed map (189 topics, 41 districts, 12 regions on five landmasses, every
page placed), after integration, three critics, a revision and Josh's answers
to its twelve questions; `graph.json` is the map before the critics. `planning/TOPIC_MAP.md`
sets out what it holds, those decisions, and the build plan from `design.md`. To rerun only the
stages after the search, pass the workflow `{from: 'integrate'}`.
