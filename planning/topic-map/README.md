# The topic map: its tools

The map itself lives in `map/` (`map/README.md` says how to change it), the
layout script is `dev/map_layout.py`, and the page is `assets/map.js` and
`assets/map.css`. This folder holds the three scripts that check the map and
the rules it was drawn to.

| File | What it is |
|---|---|
| `BRIEF.md` | The rules the map follows: the levels, the size rule, needs, naming, ids, the file format. |
| `inventory.py` | Writes `generated/inventory.json` (every non-archived, non-practice page: headings, glossary concepts, courses, current claims, length, kind) and one file per area, all under `generated/`. Run it first; that folder is not committed. |
| `validate.py` | Checks the whole map (`graph <file>`) or one area's proposal (`proposal <file> <area>`): every page placed, needs resolve and form no cycle, every descriptor outcome served or culled, and an effort-by-depth table for the size rule. |
| `continents.py` | Prints the matrix of needs between regions and the groupings of regions with the highest modularity, which is where the map's continents come from. |

    python3 planning/topic-map/inventory.py
    python3 planning/topic-map/validate.py graph map/graph.json
