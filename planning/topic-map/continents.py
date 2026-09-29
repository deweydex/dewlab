"""Find which countries belong on one continent, from the roads between them.

    python3 planning/topic-map/continents.py planning/topic-map/graph-final.json

Prints the matrix of needs between regions (row needs column) and the
groupings of regions with the highest modularity: how much more often roads
stay inside a group than they would by chance. Every way of splitting the
regions is tried, so it is slow past a dozen regions. Regions already on the
starting continent are left out; they are placed there by hand.
"""
import collections, itertools, json, sys

g = json.load(open(sys.argv[1]))
dist = {d["id"]: d["region"] for d in g["districts"]}
reg = {t["id"]: dist[t["district"]] for t in g["topics"]}
start = {r for c in g.get("continents") or [] if c.get("kind") == "start" for r in c["regions"]}
R = [r["id"] for r in g["regions"] if r["id"] not in start]
short = {r: "".join(w[0] for w in r.split("-")).upper()[:3] for r in R}

# arrows[a][b]: how many topics in a need a topic in b
arrows = collections.defaultdict(collections.Counter)
for t in g["topics"]:
    for n in t.get("needs") or []:
        if n in reg:
            arrows[reg[t["id"]]][reg[n]] += 1
shared = collections.Counter()
pages = collections.defaultdict(set)
for t in g["topics"]:
    for s in t.get("steps") or []:
        pages[s["tutorial"]].add(reg[t["id"]])
for rs in pages.values():
    for a, b in itertools.combinations(sorted(rs), 2):
        shared[frozenset((a, b))] += 1

print("Needs between regions: the row needs the column (needs inside a region on the diagonal)")
for r in R:
    print(f"  {short[r]:>4}  {r}")
print("      " + " ".join(f"{short[c]:>4}" for c in R))
for a in R:
    print(f"{short[a]:>5} " + " ".join(f"{arrows[a][b] or '.':>4}" for b in R))

# A tie counts needs both ways and half a tie for each page two regions share.
W = {a: {b: 0.0 for b in R} for a in R}
for a in R:
    for b in R:
        if a != b:
            W[a][b] = arrows[a][b] + arrows[b][a] + 0.5 * shared[frozenset((a, b))]
deg = {a: sum(W[a].values()) for a in R}
m2 = sum(deg.values())

def modularity(p):
    return sum(W[a][b] - deg[a] * deg[b] / m2 for c in p for a in c for b in c if a != b) / m2

def partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in partitions(rest):
        yield [[first]] + p
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]

size = collections.Counter(reg.values())
best = sorted(((modularity(p), p) for p in partitions(R)), key=lambda x: -x[0])[:6]
print()
print("Groupings with the highest modularity (topics in brackets):")
for q, p in best:
    groups = sorted(p, key=lambda c: -sum(size[r] for r in c))
    print(f"  Q={q:.3f}  " + "  |  ".join("+".join(short[r] for r in c) + f" ({sum(size[r] for r in c)})" for c in groups))
