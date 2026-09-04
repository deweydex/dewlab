"""Apply the topic splits provisionally, so the shape can be looked at.

    python3 dev/apply_splits.py out.html

`decisions.yaml` records which topics are the wrong shape, and `topic_changes`
says what each should become. Nothing applies those: new topics need
descriptions, and their arrows need deciding. This script does it anyway, as a
sketch, so the shape of the graph after the splits can be seen before the work
of writing them properly is done.

Every split needs three things the recorded change does not always give:

  * the children, which the change does give;
  * how the children stand to each other, which it gives in prose for some
    and not at all for others;
  * where the old topic's own arrows go — into which child, and out of which.

The table below carries all three. Where it says `inferred`, that reading is
this script's and nobody has agreed it. Read those before trusting a shape.

The default, where nothing is said: the children form a chain in the order
listed, arrows into the old topic arrive at the first, and arrows out of it
leave from the last.
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import draw_topic_graph as G

# code -> (children, internal edges by index, index taking incoming arrows,
#          index emitting outgoing arrows, whether this reading was inferred)
SPLITS = {
    "MIT-2.1": (["Natural numbers", "Integers", "Rational numbers",
                 "Irrational numbers", "Computable numbers", "Real numbers",
                 "Complex numbers"],
                [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)], 0, 6,
                "inferred: the families nest, so they chain in that order"),
    "MIT-1.10": (["Solving quadratics", "Complex roots"], [(0,1)], 0, 1, ""),
    "MIT-1.1": (["Powers", "Logarithms"], [(0,1)], 0, 0,
                "inferred: a logarithm undoes a power, so powers come first, "
                "and it is powers that binary and the quadratics need"),
    "CMPS-LO1": (["Grids", "Trees", "Recursion"], [], 0, 2,
                 "inferred: left as siblings; no order was given"),
    "MIT-5.8": (["Combining with and", "Combining with or",
                 "Conditional probability"], [(0,2),(1,2)], 0, 2,
                "inferred: and/or are siblings, conditional follows both"),
    "CMPS-LO2": (["Probability", "Sampling", "Dependence",
                  "Pseudorandom numbers", "Information theory"],
                 [(0,1),(1,2),(2,3),(2,4)], 0, 3, ""),
    "CMPS-LO4": (["Matrices", "What matrices are used for"], [(0,1)], 0, 1, ""),
    "MIT-6.8": (["Searching", "Sorting"], [], 0, 1,
                "inferred: siblings, both levelled with divide and conquer"),
    "MIT-4.10": (["The Cosine Rule", "The Sine Rule", "The ambiguous case"],
                 [(1,2)], 0, 2,
                 "inferred: the Cosine Rule stands apart, the ambiguous case "
                 "follows the Sine Rule"),
    "PDP-LO6": (["Selection", "Iteration"], [], 0, 1,
                "they do not depend on each other, and lists depends on both"),
    "MIT-5.12": (["Centre", "Simple spread", "Standard deviation"],
                 [(0,1),(1,2)], 0, 2,
                 "inferred: chained by difficulty"),
    "MIT-4.6": (["Sine and cosine defined", "The identity",
                 "Tangent as slope"], [(0,1),(0,2)], 0, 0,
                "inferred: the definition is load-bearing and takes the arrows"),
    "MIT-6.3": (["Lists", "Arrays"], [(0,1)], 0, 0,
                "inferred: lists carry the arrows; arrays is the untaught half"),
}
FOLD = {"MIT-6.5": "MIT-6.3"}


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "split-graph.html")
    topics = yaml.safe_load(G.TOPICS.read_text())["topics"]
    g = G.revise(topics, G.judgements())
    edges, levels = set(g["edges"]), set(g["levels"])

    for old, new in FOLD.items():
        edges = {(new if a == old else a, new if b == old else b)
                 for a, b in edges}
        levels = {tuple(sorted((new if x == old else x, new if y == old else y)))
                  for x, y in levels}
        topics.pop(old, None)
    edges = {e for e in edges if e[0] != e[1]}
    levels = {l for l in levels if l[0] != l[1]}

    for code, (kids, inner, takes, gives, _note) in SPLITS.items():
        if code not in topics:
            continue
        ids = [f"{code}~{i}" for i in range(len(kids))]
        for i, name in zip(ids, kids):
            topics[i] = {"name": name, "needs": []}
        edges = {(ids[gives] if a == code else a,
                  ids[takes] if b == code else b) for a, b in edges}
        levels = {tuple(sorted((ids[gives] if x == code else x,
                                ids[gives] if y == code else y)))
                  for x, y in levels}
        edges |= {(ids[a], ids[b]) for a, b in inner}
        topics.pop(code)
    edges = {e for e in edges if e[0] != e[1] and e[0] in topics and e[1] in topics}
    levels = {l for l in levels if l[0] != l[1] and l[0] in topics and l[1] in topics}

    g = {**g, "edges": edges, "levels": levels, "decided": g["decided"]}
    depth, group = G.layers(topics, edges, levels)
    out.write_text(G.page(topics, g, depth, group))
    c = collections.Counter(depth.values())
    print(f"wrote {out}")
    print(f"{len(topics)} topics, {len(edges)} arrows, {len(levels)} two-way "
          f"pairs, {max(depth.values()) + 1} layers")
    print("widths", [c[i] for i in range(max(depth.values()) + 1)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
