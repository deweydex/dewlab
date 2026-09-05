"""Draw the topic graph the blind judgements imply.

    python3 dev/draw_topic_graph.py out.html

Reads `planning/curriculum/topics.yaml` for the topics and the blind
judgements in `planning/curriculum/review/blind/` for what the graph should
be, then writes one self-contained page.

Three things decide what is drawn, and all three need two judges to agree:

  * an **arrow** — both judges said one topic comes first, and said the same
    one. An arrow they agree turns round replaces the one it reverses, rather
    than sitting beside it and inventing a loop.
  * a **level** — they pointed opposite ways, or either said "both". Two
    topics that need each other are drawn as one box with a two-way arrow
    inside it, and they layer as a single unit, because that is what being at
    one level means.
  * a **dropped arrow** — both called a pair unrelated where the graph has an
    arrow.

Where a judge stood alone the pair is left as it is. One judge is an opinion.

Then two things overrule that, in order. **`pairs/`** holds Josh's own
judgements, played blind in the game: his answer replaces whatever the agents
said about that pair, because he is the one who teaches from this. Then
**`decisions.yaml`**, what he settled deliberately with the agents' evidence
in front of him, which overrules even his own game answer. The conflicts
between those two are worth reading rather than resolving quietly, so `revise`
returns them.

The page does not draw all 117 arrows at once. A layered graph this wide is a
hairball when every edge is inked, and the question a reader actually has is
about one topic at a time: what does this need, and what needs it. So arrows
are drawn for the topic under the pointer, and a toggle inks the rest faintly
for anyone who wants the shape of the whole thing.
"""

from __future__ import annotations

import collections
import glob
import random
import itertools
import html
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "planning" / "curriculum" / "topics.yaml"
STRANDS = ROOT / "planning" / "curriculum" / "strands.yaml"
OUTCOMES = ROOT / "planning" / "curriculum" / "outcomes.yaml"
TUTORIALS = ROOT / "tutorials"
REVIEW = ROOT / "planning" / "curriculum" / "review"
BLIND = REVIEW / "blind"          # the two agents, judging without the graph
OWN = REVIEW / "pairs"            # Josh's own, played in the game
DECISIONS = REVIEW / "decisions.yaml"


# A split leaves every judgement and every decision naming a code that is gone.
# Each old code stands for the child that took over its arrows — the same child
# the parent's `needs` references were pointed at — so a judgement about the old
# topic still lands on the part of it that judgement was about. Where that is
# wrong the pair simply wants judging again, which the report will show as a
# pair nobody has an answer for.
GONE = {
    "MIT-6.3": "MIT-6.3a", "MIT-1.1": "MIT-1.1a", "MIT-6.8": "MIT-6.8a",
    "PDP-LO6": "PDP-LO6a", "MIT-1.10": "MIT-1.10a", "MIT-4.10": "MIT-4.10a",
    "MIT-5.12": "MIT-5.12a", "CMPS-LO1": "CMPS-LO1a", "MIT-5.8": "MIT-5.8a",
    "MIT-4.6": "MIT-4.6a", "CMPS-LO4": "CMPS-LO4a", "CMPS-LO2": "CMPS-LO2a",
    "MIT-2.1": "MIT-2.1a",
    # folded away rather than split: its material sits inside lists
    "MIT-6.5": "MIT-6.3a",
    # the same sentence twice, once from each module descriptor
    "CMPS-LO2a": "MIT-5.6",
    # the same lesson from two module descriptors, told once now
    "FOOP-LO2": "PDP-LO4", "FOOP-LO9": "PDP-LO7",
    "FOOP-LO10": "PDP-LO10",
}


def live(code: str) -> str:
    """The live code a dead one stands for, following a chain of them.

    A split can be followed by a merge — CMPS-LO2 became CMPS-LO2a, which
    was then folded into MIT-5.6 — so one lookup is not enough. Ten steps
    is far past any chain this file will ever hold, and stopping there
    means a mistake in GONE cannot hang the build.
    """
    for _ in range(10):
        nxt = GONE.get(code)
        if nxt is None:
            return code
        code = nxt
    raise SystemExit(f"GONE loops around {code}")


def owner_judgements() -> dict[tuple, tuple]:
    """Every pair Josh has judged himself, a newer file winning a repeat."""
    out: dict[tuple, tuple] = {}
    for path in sorted(glob.glob(str(OWN / "*.json"))):
        batch = json.loads(Path(path).read_text())
        for j in batch.get("judgements") or []:
            pair = j.get("pair") or []
            if len(pair) == 2:
                a, b = live(pair[0]), live(pair[1])
                if a == b:
                    continue          # both halves of a pair went into one child
                first = live(j["first"]) if j.get("first") else None
                out[tuple(sorted((a, b)))] = (j["verdict"], first)
    return out


def judgements() -> dict[str, dict]:
    runs: dict[str, dict] = collections.defaultdict(dict)
    for path in sorted(glob.glob(str(BLIND / "*.json"))):
        batch = json.loads(Path(path).read_text())
        for j in batch.get("judgements") or []:
            pair = j.get("pair") or []
            if len(pair) == 2:
                a, b = live(pair[0]), live(pair[1])
                if a == b:
                    continue
                first = live(j["first"]) if j.get("first") else None
                runs[batch["by"]][tuple(sorted((a, b)))] = (j["verdict"], first)
    return runs


def revise(topics: dict, runs: dict) -> dict:
    """The graph two judges agree on, out of the graph there is now."""
    names = sorted(runs)
    if len(names) != 2:
        raise SystemExit(f"expected two judges in {BLIND}, found {names}")
    a, b = (runs[n] for n in names)
    existing = {(n, c) for c, e in topics.items() for n in (e.get("needs") or [])}

    arrows, levels, dropped, turned = set(), set(), set(), set()
    for key in set(a) & set(b):
        (av, af), (bv, bf) = a[key], b[key]
        if "both" in (av, bv) or (av == bv == "needs" and af != bf):
            levels.add(key)
        elif av == bv == "needs" and af == bf:
            second = key[0] if key[1] == af else key[1]
            arrows.add((af, second))
            if (second, af) in existing:
                turned.add((second, af))
        elif av == bv == "unrelated":
            dropped |= {e for e in (key, key[::-1]) if e in existing}

    edges = (existing - dropped - turned) | arrows
    for pair in levels:
        edges -= {pair, pair[::-1]}

    own = owner_judgements()
    for key, (verdict, first) in own.items():
        edges -= {key, key[::-1]}
        levels.discard(key)
        if verdict == "needs" and first:
            edges.add((first, key[0] if key[1] == first else key[1]))
        elif verdict == "both":
            levels.add(key)

    decided = 0
    clashes = []
    for entry in (yaml.safe_load(DECISIONS.read_text()) or {}).get("decisions") or []:
        x, y = live(entry["pair"][0]), live(entry["pair"][1])
        if x == y:
            continue
        key = tuple(sorted((x, y)))
        settled = (entry["verdict"],
                   live(entry["first"]) if entry.get("first") else None)
        if key in own and own[key] != settled and not (
                own[key][0] == "both" and entry["verdict"] == "level"):
            clashes.append((key, own[key], settled))
        edges -= {(x, y), (y, x)}
        levels.discard((x, y))
        levels.discard((y, x))
        if entry["verdict"] == "needs":
            first = live(entry["first"])
            edges.add((first, y if first == x else x))
        elif entry["verdict"] == "level":
            levels.add(tuple(sorted((x, y))))
        decided += 1

    return {"edges": edges, "levels": levels, "dropped": dropped, "turned": turned,
            "added": arrows - existing, "existing": existing, "decided": decided,
            "own": own, "clashes": clashes}


def components(topics: dict, edges: set, levels: set) -> dict[str, list[str]]:
    """Every set of topics that can be reached from each other, as one unit.

A circle is A needs B needs C needs A, and it is a real thing a graph can
    contain: a region of the curriculum with no order inside it. It cannot be
    laid out in layers while its topics are drawn separately, so the whole
    region becomes one unit and the drawing says so.

    Levels are deliberately not part of this. A level is a two-way arrow
    between two topics, drawn as one; it is not a claim that everything either
    of them touches belongs in the same lesson.
    """
    # Only the one-way arrows decide the order. A level says two topics need
    # each other, which is a fact about those two and not a claim that
    # everything either of them touches is also one lesson. Feeding levels in
    # here fuses them transitively: twenty-five of them ran together into one
    # region of twenty-five topics with no order inside it, which is an
    # artefact of the merging rather than anything a judge said.
    ahead = collections.defaultdict(set)
    for early, late in edges:
        ahead[early].add(late)

    index, low, on, stack, order, out = {}, {}, set(), [], [], {}

    def strong(root):
        work = [(root, iter(ahead[root]))]
        index[root] = low[root] = len(index)
        stack.append(root); on.add(root)
        while work:
            node, kids = work[-1]
            for nxt in kids:
                if nxt not in index:
                    index[nxt] = low[nxt] = len(index)
                    stack.append(nxt); on.add(nxt)
                    work.append((nxt, iter(ahead[nxt])))
                    break
                if nxt in on:
                    low[node] = min(low[node], index[nxt])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[node])
                if low[node] == index[node]:
                    part = []
                    while True:
                        m = stack.pop(); on.discard(m); part.append(m)
                        if m == node:
                            break
                    order.append(part)

    for c in topics:
        if c not in index:
            strong(c)
    for part in order:
        out[min(part)] = sorted(part)
    return out


def layers(topics: dict, edges: set, levels: set) -> tuple[dict, dict]:
    """Which layer each unit sits on, a whole circular region counting as one."""
    group = components(topics, edges, levels)
    home = {c: u for u, members in group.items() for c in members}

    def find(x):
        return home[x]

    above = collections.defaultdict(set)
    for early, late in edges:
        if find(early) != find(late):
            above[find(late)].add(find(early))
    group = {u: m for u, m in group.items()}

    depth: dict[str, int] = {}
    for _ in range(len(group) + 1):
        moved = False
        for unit in group:
            if above[unit] <= set(depth):
                want = max((depth[p] + 1 for p in above[unit]), default=0)
                if depth.get(unit) != want:
                    depth[unit] = want
                    moved = True
        if not moved:
            break
    if len(depth) != len(group):
        # Naming the loop matters more than counting what it blocks: one
        # two-unit loop can strand a third of the graph behind it.
        stuck = set(group) - set(depth)
        found, path, on, seen = [], [], set(), set()

        def walk(node):
            path.append(node); on.add(node); seen.add(node)
            for nxt in (u for u in stuck if node in above[u]):
                if nxt in on:
                    found.append(path[path.index(nxt):] + [nxt])
                elif nxt not in seen:
                    walk(nxt)
            on.discard(node); path.pop()

        for unit in list(stuck):
            if unit not in seen:
                walk(unit)
        say = lambda u: " + ".join(topics[c]["name"] for c in sorted(group[u]))
        loops = "\n".join("  " + " -> ".join(say(u) for u in lp) for lp in found[:4])
        raise SystemExit(f"{len(stuck)} units cannot be layered, behind "
                         f"{len(found)} loop(s):\n{loops}")
    return depth, group


def verticals(topics: dict, edges: set, levels: set) -> dict[str, str]:
    """Which column each topic belongs in, decided by the graph rather than by
    a label.

    Every topic starts in its own column and repeatedly joins whichever column
    most of its neighbours are in. Where that settles is a set of topics that
    mostly connect to each other — which is what a subject is, read off the
    arrows instead of off a syllabus heading.

    The result depends on the order topics are visited, so this runs it from
    twelve starting orders and keeps the one where fewest arrows cross a
    column. Fewest crossings is the thing worth having: a crossing is a topic
    reaching outside its own subject, and those are the interesting arrows
    precisely because they are rare.
    """
    near = collections.defaultdict(set)
    for a, b in list(edges) + [x for pair in levels for x in (pair, pair[::-1])]:
        near[a].add(b)
        near[b].add(a)

    def settle(seed: int) -> dict[str, str]:
        rng = random.Random(seed)
        label = {c: c for c in topics}
        for _ in range(60):
            order = sorted(topics)
            rng.shuffle(order)
            moved = False
            for code in order:
                if not near[code]:
                    continue
                count = collections.Counter(label[n] for n in near[code])
                # sorted() before max() so a tie breaks the same way every run
                best = max(sorted(count), key=lambda k: (count[k], k))
                if best != label[code]:
                    label[code] = best
                    moved = True
            if not moved:
                break
        return label

    best_labels, best_key = None, None
    for seed in range(12):
        label = settle(seed)
        crossing = sum(1 for a, b in edges if label[a] != label[b])
        key = (crossing, len(set(label.values())))
        if best_key is None or key < best_key:
            best_labels, best_key = label, key
    return best_labels


# One box on the map is one unit: a topic, or a whole circular region of the
# graph drawn as a single box because there is no order inside it.
NODE_W, NODE_H = 168, 56
GAP_X, GAP_Y = 18, 84
GUTTER = 54          # between one column and the next
PAD, HEAD = 36, 52   # HEAD is the strip the column names sit in
CHARS, LINES = 23, 3


def wrap(text: str) -> list[str]:
    """The lines of a box's label, cut short rather than spilling out of it."""
    out, line = [], ""
    for word in text.split():
        nxt = f"{line} {word}".strip()
        if len(nxt) > CHARS and line:
            out.append(line)
            line = word
        else:
            line = nxt
    out.append(line)
    if len(out) > LINES:
        out = out[:LINES]
        out[-1] = out[-1][:CHARS - 1] + "…"
    return out


def lessons() -> dict:
    """Which tutorial teaches each outcome, and where inside it.

    A tutorial's frontmatter claims outcomes section by section, so the first
    section claiming one is the place to send somebody who wants to learn it.
    Practice sits beside the tutorial under the same slug, which is a build
    convention rather than anything the frontmatter says, so the link is only
    offered where that file is really there.
    """
    found: dict[str, dict] = {}
    for path in sorted(TUTORIALS.rglob("*.md")):
        text = path.read_text()
        if not text.startswith("---"):
            continue
        meta = yaml.safe_load(text.split("---", 2)[1])
        if not isinstance(meta, dict) or "slug" not in meta:
            continue
        drill = path.parent / f"{meta['slug']}-practice.md"
        for anchor, claim in (meta.get("covers") or {}).items():
            for code in (claim or {}).get("covers") or []:
                found.setdefault(code, {
                    "title": meta.get("title") or meta["slug"],
                    "read": f"tutorials/{meta['module']}/{meta['slug']}.html#{anchor}",
                    "drill": (f"tutorials/{meta['module']}/{meta['slug']}-practice.html"
                              if drill.exists() else None),
                })
    return found


def current(topics: dict) -> dict:
    """The graph as it stands, by whichever route topics.yaml says.

    Until the graph has been authored in the editor, it is what the judges
    agreed on, what the decisions settled, and the wall in strands.yaml. Once
    it has been, the YAML is the graph and those three are how it got there:
    `authored: true` at the top of topics.yaml says which.

    Four kinds of link come back. `edges` and `levels` are what the map is
    drawn from. `helps` and `applied` only exist once authored, and the map
    draws them lighter because they do not decide the order.
    """
    doc = yaml.safe_load(TOPICS.read_text())
    if doc.get("authored"):
        g = {"edges": set(), "levels": set(), "helps": set(), "applied": set()}
        for code, entry in topics.items():
            for need in entry.get("needs") or []:
                g["edges"].add((need, code))
            for other in entry.get("interdependent") or []:
                g["levels"].add(tuple(sorted((code, other))))
            for other in entry.get("helps") or []:
                g["helps"].add((code, other))
            for other in entry.get("applied_in") or []:
                g["applied"].add((code, other))
        return g
    g = revise(topics, judgements())
    separate(g, bands(topics))
    g["helps"], g["applied"] = set(), set()
    return g


def bands(topics: dict) -> dict:
    """Which column each topic is drawn in.

    The column comes from `strands.yaml`, which is a drawing decision and not
    a claim about what depends on what. Columns branch, rejoin and reach into
    each other, and the arrows that cross between them are the point.
    """
    spec = yaml.safe_load(STRANDS.read_text())
    outcomes = {o["code"]: o
                for o in yaml.safe_load(OUTCOMES.read_text())["outcomes"]}
    over = spec.get("topics") or {}

    band = {}
    for code, entry in topics.items():
        if code in over:
            band[code] = over[code]["column"]
            continue
        claimed = entry.get("outcome") or code
        first = claimed if isinstance(claimed, str) else claimed[0]
        fine = (outcomes.get(first) or {}).get("strand")
        band[code] = spec["from_strand"].get(fine)
    astray = sorted(c for c, b in band.items() if not b)
    if astray:
        raise SystemExit(f"no column for {', '.join(astray)} — add them to "
                         f"{STRANDS.name}")
    return band


def separate(g: dict, band: dict) -> tuple[int, int]:
    """Drop the arrows a wall in `strands.yaml` forbids, and the levels that
    straddle it.

    A wall says one column's topics never come before another's. Where two
    module descriptors cover the same ground in their own order, the graph
    ends up asserting both directions between them, and no single pair can be
    argued out of it. The wall settles the whole boundary at once, and the
    file that declares it says why.
    """
    spec = yaml.safe_load(STRANDS.read_text())
    walls = spec.get("no_arrow_from") or {}
    if not walls:
        return 0, 0
    barred = {(a, b) for a, kids in walls.items() for b in kids}
    arrows = {e for e in g["edges"] if (band[e[0]], band[e[1]]) in barred}
    pairs = {p for p in g["levels"]
             if (band[p[0]], band[p[1]]) in barred
             or (band[p[1]], band[p[0]]) in barred}
    g["edges"] -= arrows
    g["levels"] -= pairs
    return len(arrows), len(pairs)


def column_order(topics: dict, edges: set, band: dict) -> list:
    """What order the columns go in, left to right.

    Worked out rather than chosen: every one of the seven hundred and twenty
    arrangements is tried, and the one kept is whichever puts the fewest
    column widths between the two ends of an arrow. Related columns end up
    beside each other because the arrows say they are.
    """
    spec = yaml.safe_load(STRANDS.read_text())
    ids = [c["id"] for c in spec["columns"]]
    home = {c["id"]: i for i, c in enumerate(spec["columns"])}

    def cost(order: tuple) -> tuple:
        where = {c: i for i, c in enumerate(order)}
        far = sum(abs(where[band[a]] - where[band[b]]) for a, b in edges)
        return (far, tuple(home[c] for c in order))

    best = min(itertools.permutations(ids), key=cost)
    return [next(c for c in spec["columns"] if c["id"] == i) for i in best]


def place(depth: dict, group: dict, edges: set, band: dict,
          order: list) -> tuple[dict, dict, int, int]:
    """Where every box sits, how wide each column is, and how big the map is.

    The row is the layer, so that part is not a choice, and the column is the
    subject. What is left free is the order of the boxes within one column on
    one row, and the order chosen is the one that puts each box near the boxes
    it connects to.

    Left to right carries no meaning inside a column. Those topics have no
    order between them, which is what sharing a row says.
    """
    unit_of = {c: u for u, members in group.items() for c in members}
    col_of = {u: band[min(members)] for u, members in group.items()}

    cells = collections.defaultdict(list)
    for unit, level in depth.items():
        cells[(level, col_of[unit])].append(unit)
    for key in cells:
        cells[key].sort()

    up = collections.defaultdict(list)
    down = collections.defaultdict(list)
    for early, late in sorted(edges):
        a, b = unit_of[early], unit_of[late]
        if a != b:
            down[a].append(b)
            up[b].append(a)

    seen = sorted({l for l, _ in cells})
    wide = {c["id"]: max((len(cells.get((lv, c["id"])) or ()) for lv in seen),
                         default=0) or 1
            for c in order}
    left, run = {}, PAD
    for c in order:
        left[c["id"]] = run
        run += wide[c["id"]] * NODE_W + (wide[c["id"]] - 1) * GAP_X + GUTTER
    width = int(run - GUTTER + PAD)
    rows = max(l for l, _ in cells) + 1
    height = int(HEAD + PAD + rows * NODE_H + (rows - 1) * GAP_Y)

    def spread(key) -> dict[str, float]:
        row, col = cells[key], key[1]
        span = len(row) * NODE_W + (len(row) - 1) * GAP_X
        start = left[col] + (wide[col] * NODE_W + (wide[col] - 1) * GAP_X - span) / 2
        return {u: start + i * (NODE_W + GAP_X) for i, u in enumerate(row)}

    # Sweep down the rows then back up, each time re-ordering each cell by
    # where its neighbours in the row before sit. Ten passes is well past the
    # point where the ordering stops changing for a graph this size.
    for sweep in range(10):
        at_x = {}
        for key in list(cells):
            at_x.update(spread(key))
        levels = sorted({l for l, _ in cells}, reverse=sweep % 2)
        side = up if sweep % 2 == 0 else down
        for level in levels:
            for c in order:
                key = (level, c["id"])
                if len(cells[key]) < 2:
                    continue
                here = spread(key)

                def anchor(unit: str) -> tuple[float, str]:
                    near = [at_x[n] for n in side[unit] if n in at_x]
                    return (sum(near) / len(near) if near else here[unit], unit)

                cells[key].sort(key=anchor)
                at_x.update(spread(key))

    at = {}
    for key, row in cells.items():
        if not row:
            continue
        xs = spread(key)
        for unit in row:
            at[unit] = (xs[unit], HEAD + key[0] * (NODE_H + GAP_Y))
    spans = {c["id"]: (left[c["id"]] - GAP_X / 2,
                       wide[c["id"]] * NODE_W + (wide[c["id"]] - 1) * GAP_X + GAP_X)
             for c in order}
    return at, spans, width, height


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def page(topics: dict, g: dict, depth: dict, group: dict) -> str:
    """The map page: a search box, a close-up of one topic, and the whole map.

    Two views over one graph. The close-up centres on a topic, with what it
    needs to its left and what it opens to its right, a few steps each way —
    the answer to "I am here" and "I am stuck on this". The whole map is the
    same graph drawn in its six columns, for standing back.

    Neither view is radial. A prerequisite graph's content is direction, and a
    ring around a centre says only "connected": left and right say which way.
    """
    unit_of = {c: u for u, members in group.items() for c in members}
    band = bands(topics)
    order = column_order(topics, g["edges"], band)
    at, spans, width, height = place(depth, group, g["edges"], band, order)
    col_of = {u: band[min(members)] for u, members in group.items()}
    teach = lessons()

    name = {u: " + ".join(topics[c]["name"] for c in sorted(members))
            for u, members in group.items()}

    up = collections.defaultdict(set)
    down = collections.defaultdict(set)
    for early, late in g["edges"]:
        a, b = unit_of[early], unit_of[late]
        if a != b:
            down[a].add(b)
            up[b].add(a)

    stripes = []
    for i, c in enumerate(order):
        x, w = spans[c["id"]]
        stripes.append(
            f'<g class="band{" alt" if i % 2 else ""}" data-c="{c["id"]}">'
            f'<rect x="{x:.0f}" y="0" width="{w:.0f}" height="{height}"/>'
            f'<text x="{x + w / 2:.0f}" y="30">{esc(c["name"])}</text></g>')

    wires, crossings = [], 0
    for a in sorted(down):
        for b in sorted(down[a]):
            x1, y1 = at[a][0] + NODE_W / 2, at[a][1] + NODE_H
            x2, y2 = at[b][0] + NODE_W / 2, at[b][1]
            bend = max(24, (y2 - y1) / 2)
            over = col_of[a] != col_of[b]
            crossings += over
            wires.append(
                f'<path class="wire{" over" if over else ""}" data-a="{a}" '
                f'data-b="{b}" d="M{x1:.0f} {y1:.0f} C{x1:.0f} {y1 + bend:.0f} '
                f'{x2:.0f} {y2 - bend:.0f} {x2:.0f} {y2:.0f}"/>')

    pairs = []
    for a, b in sorted(g["levels"]):
        ua, ub = unit_of[a], unit_of[b]
        if ua == ub:
            continue
        x1, y1 = at[ua][0] + NODE_W / 2, at[ua][1] + NODE_H / 2
        x2, y2 = at[ub][0] + NODE_W / 2, at[ub][1] + NODE_H / 2
        pairs.append(f'<path class="pair" data-a="{ua}" data-b="{ub}" '
                     f'd="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}"/>')

    boxes = []
    for unit in sorted(at, key=lambda u: (depth[u], at[u][0])):
        x, y = at[unit]
        lines = wrap(name[unit])
        top = NODE_H / 2 - (len(lines) - 1) * 6.5
        text = "".join(
            f'<tspan x="{NODE_W / 2:.0f}" y="{top + i * 13:.1f}">{esc(line)}</tspan>'
            for i, line in enumerate(lines))
        many = " many" if len(group[unit]) > 1 else ""
        boxes.append(
            f'<g class="node{many}" data-u="{unit}" data-c="{col_of[unit]}" '
            f'data-m="{module_of(unit)}" '
            f'transform="translate({x:.0f},{y:.0f})">'
            f'<rect width="{NODE_W}" height="{NODE_H}" rx="9"/>'
            f'<text>{text}</text></g>')

    facts = {}
    for unit, members in group.items():
        lead = min(members)
        entry = topics[lead]
        claimed = entry.get("outcome") or lead
        outcomes = [claimed] if isinstance(claimed, str) else list(claimed)
        lesson = next((teach[o] for o in outcomes if o in teach), None)
        facts[unit] = {
            "n": name[unit], "c": col_of[unit], "m": module_of(unit),
            "r": depth[unit], "u": sorted(up[unit]), "d": sorted(down[unit]),
            "p": " ".join((entry.get("plain") or "").split()),
            "w": [" ".join(u.split()) for u in (entry.get("uses") or [])],
            "L": lesson,
        }

    chips = "".join(
        f'<button class="chip col" data-c="{c["id"]}" aria-pressed="true">'
        f'{esc(c["name"])}</button>' for c in order)
    seen_modules = sorted({module_of(u) for u in group})
    modules = "".join(
        f'<button class="chip mod" data-m="{m}" aria-pressed="true">'
        f'{esc(MODULES.get(m, m))}</button>' for m in seen_modules)

    return (TEMPLATE
            .replace("__W__", str(width))
            .replace("__H__", str(height))
            .replace("__BANDS__", "\n".join(stripes))
            .replace("__WIRES__", "\n".join(wires))
            .replace("__PAIRS__", "\n".join(pairs))
            .replace("__BOXES__", "\n".join(boxes))
            .replace("__CHIPS__", chips)
            .replace("__MODULES__", modules)
            .replace("__FACTS__", json.dumps(facts, sort_keys=True))
            .replace("__ROWS__", str(max(depth.values()) + 1))
            .replace("__COUNT__", str(len(topics)))
            .replace("__CROSS__", str(crossings))
            .replace("__ARROWS__", str(len(g["edges"]))))


# The four QQI modules, shortened to fit a chip. "Groundwork" is ours: a PRE-
# topic is prior knowledge no descriptor asked for.
MODULES = {
    "MIT": "Maths for IT", "PDP": "Programming and Design",
    "CMPS": "Computational Methods", "FOOP": "Object Oriented",
    "PRE": "Groundwork",
}


def module_of(unit: str) -> str:
    return unit.split("-")[0]


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The topic map</title>
<style>
:root{
  --ink:#1b1b1f; --dim:#6b6b76; --line:#d6d6de; --paper:#fbfbfd;
  --box:#fff; --mark:#1b5cff; --soft:#eef2ff; --two:#b8860b;
  --tint:#f1f1f6; --cross:#c2703a; --panel:#fff;
}
@media (prefers-color-scheme: dark){
  :root{ --ink:#e9e9ef; --dim:#9a9aa6; --line:#3a3a44; --paper:#141418;
         --box:#1e1e25; --mark:#7aa2ff; --soft:#22283a; --two:#e0b552;
         --tint:#1a1a20; --cross:#e08a52; --panel:#1a1a20; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;
  display:flex;flex-direction:column;height:100dvh;overflow:hidden}
header{padding:.55rem .8rem;border-bottom:1px solid var(--line);flex:none}
.bar{display:flex;gap:.4rem;align-items:center}
h1{margin:0 .5rem 0 0;font-size:.95rem;font-weight:600;white-space:nowrap}
input[type=search]{flex:1;min-width:0;padding:.5rem .6rem;font:inherit;
  border:1px solid var(--line);border-radius:8px;background:var(--box);color:inherit}
button{font:inherit;padding:.45rem .6rem;border:1px solid var(--line);
  border-radius:8px;background:var(--box);color:inherit;cursor:pointer}
button[aria-pressed=true]{background:var(--soft);border-color:var(--mark);color:var(--mark)}
.rows{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.4rem;align-items:center}
.rows small{color:var(--dim);font-size:.75rem;margin-right:.1rem}
.chip{padding:.25rem .5rem;font-size:.78rem;border-radius:999px}
.chip[aria-pressed=false]{opacity:.45}
main{flex:1;display:flex;min-height:0}
#stage{flex:1;min-width:0;position:relative;overflow:auto;
  -webkit-overflow-scrolling:touch;touch-action:pan-x pan-y}
aside{width:320px;flex:none;border-left:1px solid var(--line);
  background:var(--panel);overflow:auto;padding:.9rem}
#sift{display:none}
@media (max-width:820px){
  main{flex-direction:column}
  aside{width:auto;border-left:0;border-top:1px solid var(--line);
        max-height:40dvh;padding:.7rem}
  h1{display:none}
  /* the chips are a third of a phone screen, so they fold away */
  #sift{display:block}
  #filters{display:none}
  #filters.open{display:flex}
}
/* the close-up */
#near{display:none;padding:1rem .6rem;min-height:100%;position:relative}
#near.on{display:flex;gap:0;align-items:stretch;min-height:100%}
#near .step{flex:1;min-width:150px;max-width:230px;display:flex;
  flex-direction:column;padding:0 .5rem;position:relative;z-index:1}
#near .stack{flex:1;display:flex;flex-direction:column;gap:.4rem;
  justify-content:center}
#near h2{margin:0 0 .3rem;font-size:.7rem;text-transform:uppercase;
  letter-spacing:.05em;color:var(--dim);font-weight:600;text-align:center}
.card{display:block;width:100%;text-align:left;padding:.45rem .55rem;
  font-size:.83rem;line-height:1.25;border-radius:9px;border:1px solid var(--line);
  background:var(--box)}
.card.here{border-color:var(--mark);border-width:2px;background:var(--soft);
  font-weight:600;font-size:.92rem;padding:.6rem}
.card.off{opacity:.3}
.card em{display:block;font-style:normal;font-size:.68rem;color:var(--dim);
  margin-top:.15rem}
.more{font-size:.75rem;color:var(--dim);padding:.3rem}
#threads{position:absolute;inset:0;pointer-events:none;z-index:0}
#threads path{fill:none;stroke:var(--line);stroke-width:1.4}
#threads path.over{stroke:var(--cross)}
.empty{color:var(--dim);font-size:.78rem;text-align:center;padding:.4rem}
/* the whole map */
#all{display:none;place-content:start center;padding:.5rem}
#all.on{display:grid}
svg#map{display:block}
.band rect{fill:none}
.band.alt rect{fill:var(--tint)}
.band text{font-size:17px;fill:var(--dim);text-anchor:middle;font-weight:600}
.node rect{fill:var(--box);stroke:var(--line);stroke-width:1.2}
.node.many rect{stroke-dasharray:5 3}
.node text{font-size:12px;fill:var(--ink);text-anchor:middle;
  dominant-baseline:middle;pointer-events:none}
.node{cursor:pointer}
.node.off{opacity:.12}
.node.found rect{stroke:var(--two);stroke-width:2.4}
.wire{fill:none;stroke:var(--line);stroke-width:1.2}
.wire.over{stroke:var(--cross);opacity:.55}
.pair{fill:none;stroke:var(--two);stroke-width:1.4;stroke-dasharray:3 4;opacity:.7}
/* the panel */
aside h2{margin:0 0 .15rem;font-size:1.05rem}
aside .where{color:var(--dim);font-size:.78rem;margin:0 0 .6rem}
aside p{margin:0 0 .7rem}
aside .go{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:.8rem}
aside .go a{text-decoration:none;padding:.45rem .7rem;border-radius:8px;
  border:1px solid var(--mark);color:var(--mark);font-size:.85rem}
aside .go a.solid{background:var(--mark);color:#fff}
aside .none{color:var(--dim);font-size:.82rem}
aside h3{margin:.9rem 0 .3rem;font-size:.72rem;text-transform:uppercase;
  letter-spacing:.05em;color:var(--dim)}
aside ul{margin:0;padding-left:1.1rem}
aside li{margin-bottom:.4rem;font-size:.85rem}
.hits{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.4rem}
.hits:empty{display:none}
.hits button{padding:.25rem .55rem;font-size:.8rem;border-radius:999px}
</style></head><body>
<header>
  <div class="bar">
    <h1>The topic map</h1>
    <input type="search" id="find" placeholder="Search a topic you are on, or one you find hard" autocomplete="off">
    <button id="sift" aria-pressed="false">Filters</button>
    <button id="wide" aria-pressed="false">Whole map</button>
  </div>
  <div class="hits" id="hits"></div>
  <div class="rows" id="filters">
    <small>Subjects</small>__CHIPS__
    <small>Modules</small>__MODULES__
    <small>How far</small>
    <button class="chip step" data-n="1">1 step</button>
    <button class="chip step" data-n="2">2 steps</button>
    <button class="chip step" data-n="3">3 steps</button>
  </div>
</header>
<main>
  <div id="stage">
    <div id="near"><svg id="threads"></svg></div>
    <div id="all">
      <svg id="map" viewBox="0 0 __W__ __H__" width="__W__" height="__H__">
      <g id="bands">__BANDS__</g>
      <g id="pairs">__PAIRS__</g>
      <g id="wires">__WIRES__</g>
      <g id="boxes">__BOXES__</g>
      </svg>
    </div>
  </div>
  <aside id="panel"></aside>
</main>
<script>
const FACTS = __FACTS__;
const stage = document.getElementById("stage");
const near = document.getElementById("near");
const all = document.getElementById("all");
const map = document.getElementById("map");
const panel = document.getElementById("panel");
const threads = document.getElementById("threads");
const CAP = 12;
let here = null, steps = null, opened = new Set();
const hidden = {c: new Set(), m: new Set()};

const START = "<h2>Where are you?</h2>"
  + "<p>Search for a topic you are working on, or one you are finding hard. "
  + "The map then shows what comes before it and what it leads to.</p>"
  + "<p>Select any box to move the map to it. Where a tutorial teaches the "
  + "topic, its link appears here.</p>"
  + "<p class=none>The chips above hide a column or a module, which makes the "
  + "map smaller while you look for something.</p>";

function shown(u){ const f = FACTS[u]; return !hidden.c.has(f.c) && !hidden.m.has(f.m); }
function fit(){ return innerWidth < 900 ? 2 : 3; }
function reach(u, key, n){
  const rings = [];
  let front = new Set([u]), seen = new Set([u]);
  for(let i = 0; i < n; i++){
    const next = new Set();
    for(const c of front) for(const x of FACTS[c][key]) if(!seen.has(x)){ next.add(x); seen.add(x); }
    if(!next.size) break;
    rings.push([...next].sort((a, b) => FACTS[a].n.localeCompare(FACTS[b].n)));
    front = next;
  }
  return rings;
}

function cardHtml(u, cls){
  const f = FACTS[u];
  const note = f.L ? "" : "<em>no tutorial yet</em>";
  return '<button class="card ' + cls + (shown(u) ? "" : " off") + '" data-u="'
    + u + '">' + f.n + note + "</button>";
}

function column(title, list, key){
  const open = opened.has(key);
  const take = open ? list : list.slice(0, CAP);
  const rest = list.length - take.length;
  return '<div class="step">' + "<h2>" + title + '</h2><div class="stack">'
    + (list.length ? take.map(u => cardHtml(u, "")).join("")
                   : '<p class="empty">Nothing.</p>')
    + (rest > 0 ? '<button class="more" data-open="' + key + '">and '
        + rest + " more</button>" : "") + "</div></div>";
}

function drawNear(){
  if(!here) return;
  const n = steps || fit();
  const back = reach(here, "u", n), fwd = reach(here, "d", n);
  const say = i => i === 1 ? "Comes first" : i + " steps before";
  const sayF = i => i === 1 ? "Comes next" : i + " steps on";
  let html = "";
  for(let i = back.length; i >= 1; i--) html += column(say(i), back[i-1], "b" + i);
  html += '<div class="step"><h2>You are here</h2><div class="stack">'
        + cardHtml(here, "here") + "</div></div>";
  for(let i = 1; i <= fwd.length; i++) html += column(sayF(i), fwd[i-1], "f" + i);
  near.innerHTML = '<svg id="threads"></svg>' + html;
  wireUp();
  show(here);
  // After the frame, because the columns have no width until they are laid
  // out, and a phone shows two of seven — opening anywhere but on the topic
  // itself is opening in the wrong place.
  requestAnimationFrame(() => {
    const you = near.querySelector(".card.here");
    if(you) you.scrollIntoView({inline: "center", block: "nearest"});
  });
}

function wireUp(){
  const svg = document.getElementById("threads");
  const box = near.getBoundingClientRect();
  svg.setAttribute("viewBox", "0 0 " + box.width + " " + box.height);
  svg.setAttribute("width", box.width);
  svg.setAttribute("height", box.height);
  const spot = {};
  for(const el of near.querySelectorAll(".card")){
    const r = el.getBoundingClientRect();
    spot[el.dataset.u] = {l: r.left - box.left, r: r.right - box.left,
                          y: r.top - box.top + r.height / 2};
  }
  let d = "";
  for(const a in spot) for(const b of FACTS[a].d){
    if(!spot[b] || spot[b].l <= spot[a].r - 4) continue;
    const over = FACTS[a].c !== FACTS[b].c;
    const mid = (spot[a].r + spot[b].l) / 2;
    d += '<path class="' + (over ? "over" : "") + '" d="M' + spot[a].r + " "
      + spot[a].y + " C" + mid + " " + spot[a].y + " " + mid + " " + spot[b].y
      + " " + spot[b].l + " " + spot[b].y + '"/>';
  }
  svg.innerHTML = d;
}

function show(u){
  const f = FACTS[u];
  let html = "<h2>" + f.n + "</h2><p class=where>" + f.c.replace(/-/g, " ")
    + " · row " + (f.r + 1) + "</p>";
  if(f.p) html += "<p>" + f.p + "</p>";
  if(f.L){
    html += '<div class="go"><a class="solid" href="' + f.L.read + '">Read it</a>'
      + (f.L.drill ? '<a href="' + f.L.drill + '">Practice</a>' : "") + "</div>"
      + '<p class="none">In <b>' + f.L.title + "</b>.</p>";
  } else {
    html += '<p class="none">No tutorial teaches this one yet.</p>';
  }
  if(f.w && f.w.length){
    html += "<h3>Where it turns up</h3><ul>"
      + f.w.map(x => "<li>" + x + "</li>").join("") + "</ul>";
  }
  panel.innerHTML = html;
}

function centre(u){
  here = u;
  opened.clear();
  if(all.classList.contains("on")) wideOff();
  near.classList.add("on");
  drawNear();
}

function wideOn(){
  near.classList.remove("on"); all.classList.add("on");
  document.getElementById("wide").setAttribute("aria-pressed", "true");
  const w = stage.clientWidth - 12, h = stage.clientHeight - 12;
  const s = Math.min(1.6, w / __W__);
  map.setAttribute("width", Math.round(__W__ * s));
  map.setAttribute("height", Math.round(__H__ * s));
}
function wideOff(){
  all.classList.remove("on");
  document.getElementById("wide").setAttribute("aria-pressed", "false");
  if(here) near.classList.add("on");
}
document.getElementById("sift").addEventListener("click", e => {
  const open = document.getElementById("filters").classList.toggle("open");
  e.currentTarget.setAttribute("aria-pressed", String(open));
});
document.getElementById("wide").addEventListener("click", () => {
  all.classList.contains("on") ? wideOff() : wideOn();
});

near.addEventListener("click", e => {
  const more = e.target.closest("[data-open]");
  if(more){ opened.add(more.dataset.open); drawNear(); return; }
  const c = e.target.closest(".card");
  if(c) centre(c.dataset.u);
});
map.addEventListener("click", e => {
  const n = e.target.closest(".node");
  if(n) centre(n.dataset.u);
});

document.getElementById("filters").addEventListener("click", e => {
  const chip = e.target.closest(".chip");
  if(!chip) return;
  if(chip.classList.contains("step")){
    steps = Number(chip.dataset.n);
    for(const s of document.querySelectorAll(".chip.step"))
      s.setAttribute("aria-pressed", String(s === chip));
    drawNear();
    return;
  }
  const key = chip.classList.contains("col") ? "c" : "m";
  const id = key === "c" ? chip.dataset.c : chip.dataset.m;
  const on = chip.getAttribute("aria-pressed") === "true";
  chip.setAttribute("aria-pressed", String(!on));
  on ? hidden[key].add(id) : hidden[key].delete(id);
  for(const n of map.querySelectorAll(".node")) n.classList.toggle("off", !shown(n.dataset.u));
  if(here) drawNear();
});

const find = document.getElementById("find");
const hits = document.getElementById("hits");
function matches(){
  const q = find.value.trim().toLowerCase();
  if(q.length < 2) return [];
  return Object.keys(FACTS).filter(u => shown(u)
    && FACTS[u].n.toLowerCase().includes(q))
    .sort((a, b) => FACTS[a].n.length - FACTS[b].n.length).slice(0, 8);
}
find.addEventListener("input", () => {
  const found = matches();
  hits.innerHTML = found.map(u => '<button data-u="' + u + '">'
    + FACTS[u].n + "</button>").join("");
  for(const n of map.querySelectorAll(".node"))
    n.classList.toggle("found", found.includes(n.dataset.u));
});
find.addEventListener("keydown", e => {
  if(e.key !== "Enter") return;
  const found = matches();
  if(found.length) centre(found[0]);
});
hits.addEventListener("click", e => {
  const b = e.target.closest("button");
  if(b) centre(b.dataset.u);
});

addEventListener("resize", () => {
  if(all.classList.contains("on")) wideOn(); else if(here) drawNear();
});
panel.innerHTML = START;
wideOn();
</script></body></html>
"""


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "topic-graph.html")
    topics = yaml.safe_load(TOPICS.read_text())["topics"]
    g = current(topics)
    depth, group = layers(topics, g["edges"], g["levels"])
    out.write_text(page(topics, g, depth, group))
    print(f"wrote {out} — {len(topics)} topics, {len(g['edges'])} arrows, "
          f"{len(g['levels'])} two-way pairs, {max(depth.values()) + 1} layers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
