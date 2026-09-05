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
import html
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "planning" / "curriculum" / "topics.yaml"
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
}


def live(code: str) -> str:
    return GONE.get(code, code)


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
PAD = 36
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


def place(depth: dict, group: dict, edges: set) -> tuple[dict, int, int]:
    """Where every box sits, and how big the map is.

    The layer fixes the row, so that part is not a choice. Which order the
    boxes sit in along a row is free, and the order chosen here is the one that
    puts each box near the boxes it connects to. Short arrows that cross each
    other rarely are the only thing being optimised.

    Left to right inside a row carries no meaning. Those topics have no order
    between them, which is what sharing a row says.
    """
    unit_of = {c: u for u, members in group.items() for c in members}
    rows = collections.defaultdict(list)
    for unit, level in depth.items():
        rows[level].append(unit)
    for level in rows:
        rows[level].sort()

    up = collections.defaultdict(list)
    down = collections.defaultdict(list)
    for early, late in sorted(edges):
        a, b = unit_of[early], unit_of[late]
        if a != b:
            down[a].append(b)
            up[b].append(a)

    def spread(row: list[str]) -> dict[str, float]:
        if len(row) == 1:
            return {row[0]: 0.5}
        return {u: i / (len(row) - 1) for i, u in enumerate(row)}

    # Sweep down the rows then back up, each time re-ordering a row by where
    # its neighbours in the row before sit. Ten passes is well past the point
    # where the ordering stops changing for a graph this size.
    for sweep in range(10):
        pos = {}
        for row in rows.values():
            pos.update(spread(row))
        levels_in_order = sorted(rows) if sweep % 2 == 0 else sorted(rows, reverse=True)
        side = up if sweep % 2 == 0 else down
        for level in levels_in_order:
            row = rows[level]
            here = spread(row)

            def anchor(unit: str) -> tuple[float, str]:
                near = [pos[n] for n in side[unit] if n in pos]
                return (sum(near) / len(near) if near else here[unit], unit)

            row.sort(key=anchor)
            pos.update(spread(row))

    widest = max(len(row) for row in rows.values())
    width = PAD * 2 + widest * NODE_W + (widest - 1) * GAP_X
    height = PAD * 2 + (max(rows) + 1) * NODE_H + max(rows) * GAP_Y

    at = {}
    for level, row in rows.items():
        span = len(row) * NODE_W + (len(row) - 1) * GAP_X
        left = (width - span) / 2
        for i, unit in enumerate(row):
            at[unit] = (left + i * (NODE_W + GAP_X), PAD + level * (NODE_H + GAP_Y))
    return at, int(width), int(height)


def page(topics: dict, g: dict, depth: dict, group: dict) -> str:
    """One page: the map as a drawn graph, plus a search box and a card.

    The map is drawn as boxes in rows with the arrows between them, because
    that is the shape of the thing: what has to come first sits above what
    needs it. It opens scaled to fit whatever screen it is on, so a phone gets
    the shape first and the detail on a tap.
    """
    unit_of = {c: u for u, members in group.items() for c in members}
    at, width, height = place(depth, group, g["edges"])

    name = {u: " + ".join(topics[c]["name"] for c in sorted(members))
            for u, members in group.items()}

    up = collections.defaultdict(set)
    down = collections.defaultdict(set)
    for early, late in g["edges"]:
        a, b = unit_of[early], unit_of[late]
        if a != b:
            down[a].add(b)
            up[b].add(a)

    wires = []
    for a in sorted(down):
        for b in sorted(down[a]):
            x1, y1 = at[a][0] + NODE_W / 2, at[a][1] + NODE_H
            x2, y2 = at[b][0] + NODE_W / 2, at[b][1]
            bend = max(24, (y2 - y1) / 2)
            wires.append(
                f'<path class="wire" data-a="{a}" data-b="{b}" '
                f'd="M{x1:.0f} {y1:.0f} C{x1:.0f} {y1 + bend:.0f} '
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
            f'<g class="node{many}" data-u="{unit}" transform="translate({x:.0f},{y})">'
            f'<rect width="{NODE_W}" height="{NODE_H}" rx="9"/>'
            f'<text>{text}</text></g>')

    facts = {
        u: {"n": name[u], "c": sorted(group[u]), "r": depth[u],
            "u": sorted(up[u]), "d": sorted(down[u])}
        for u in at
    }
    roots = sorted((u for u in at if not up[u]), key=lambda u: name[u].lower())

    return (TEMPLATE
            .replace("__W__", str(width))
            .replace("__H__", str(height))
            .replace("__WIRES__", "\n".join(wires))
            .replace("__PAIRS__", "\n".join(pairs))
            .replace("__BOXES__", "\n".join(boxes))
            .replace("__FACTS__", json.dumps(facts, sort_keys=True))
            .replace("__ROOTS__", json.dumps(roots))
            .replace("__ROWS__", str(max(depth.values()) + 1))
            .replace("__COUNT__", str(len(topics)))
            .replace("__ARROWS__", str(len(g["edges"]))))


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The topic map</title>
<style>
:root{
  --ink:#1b1b1f; --dim:#6b6b76; --line:#d6d6de; --paper:#fbfbfd;
  --box:#fff; --mark:#1b5cff; --soft:#eef2ff; --two:#b8860b;
}
@media (prefers-color-scheme: dark){
  :root{ --ink:#e9e9ef; --dim:#9a9aa6; --line:#3a3a44; --paper:#141418;
         --box:#1e1e25; --mark:#7aa2ff; --soft:#22283a; --two:#e0b552; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
     font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;
     display:flex;flex-direction:column;height:100dvh}
header{padding:.6rem .8rem;border-bottom:1px solid var(--line);background:var(--paper)}
h1{margin:0 0 .35rem;font-size:1rem;font-weight:600}
h1 span{font-weight:400;color:var(--dim)}
.bar{display:flex;gap:.4rem;align-items:center}
input[type=search]{flex:1;min-width:0;padding:.5rem .6rem;font:inherit;
  border:1px solid var(--line);border-radius:8px;background:var(--box);color:inherit}
button{font:inherit;padding:.45rem .6rem;border:1px solid var(--line);
  border-radius:8px;background:var(--box);color:inherit;cursor:pointer}
button:disabled{opacity:.45;cursor:default}
#stage{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;
  touch-action:pan-x pan-y;display:grid;place-content:start center;padding:.5rem}
svg{display:block}
.node rect{fill:var(--box);stroke:var(--line);stroke-width:1.2}
.node.many rect{stroke-dasharray:5 3}
.node text{font-size:12px;fill:var(--ink);text-anchor:middle;
  dominant-baseline:middle;pointer-events:none}
.node{cursor:pointer}
.wire{fill:none;stroke:var(--line);stroke-width:1.2}
.pair{fill:none;stroke:var(--two);stroke-width:1.4;stroke-dasharray:3 4;opacity:.7}
svg.picked .node rect{opacity:.25}
svg.picked .wire{opacity:.12}
svg.picked .pair{opacity:.12}
svg.picked .node.on rect{opacity:1;stroke:var(--mark);stroke-width:2;fill:var(--soft)}
svg.picked .node.here rect{opacity:1;stroke:var(--mark);stroke-width:3;fill:var(--soft)}
svg.picked .node.on text,svg.picked .node.here text{opacity:1}
svg.picked .node rect:not(.x){}
svg.picked .wire.on{opacity:1;stroke:var(--mark);stroke-width:1.8}
.node.found rect{stroke:var(--two);stroke-width:2.4}
#card{border-top:1px solid var(--line);background:var(--paper);
  padding:.6rem .8rem;max-height:42dvh;overflow:auto}
#card[hidden]{display:none}
#card h2{margin:0 0 .1rem;font-size:1rem}
#card p{margin:.15rem 0 .5rem;color:var(--dim);font-size:.85rem}
#card h3{margin:.6rem 0 .25rem;font-size:.8rem;text-transform:uppercase;
  letter-spacing:.04em;color:var(--dim)}
#card ul{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:.3rem}
#card li button{padding:.3rem .5rem;font-size:.85rem}
.none{color:var(--dim);font-size:.85rem;margin:0}
.key{display:flex;flex-wrap:wrap;align-items:center;gap:.15rem .9rem;
  margin:.45rem 0 0;font-size:.78rem;color:var(--dim)}
.key b{font-weight:400;display:flex;align-items:center;gap:.3rem}
.key path{fill:none;stroke-width:1.6}
.key .one{stroke:var(--dim)}
.key .two{stroke:var(--two);stroke-dasharray:3 4}
</style></head><body>
<header>
  <h1>The topic map <span>__COUNT__ topics · __ARROWS__ arrows · __ROWS__ rows</span></h1>
  <div class="bar">
    <input type="search" id="find" placeholder="Search a topic" autocomplete="off">
    <button id="out" title="Smaller">−</button>
    <button id="in" title="Bigger">+</button>
    <button id="fit">Fit</button>
  </div>
  <p class="key">
    <b><svg width="26" height="11" aria-hidden="true"><path class="one"
      d="M1 1 C10 1 16 10 25 10"/></svg> one comes before the other</b>
    <b><svg width="26" height="11" aria-hidden="true"><path class="two"
      d="M1 6 L25 6"/></svg> neither comes first</b>
    <b>Left to right means nothing.</b>
  </p>
</header>
<div id="stage">
<svg id="map" viewBox="0 0 __W__ __H__" width="__W__" height="__H__">
<g id="pairs">__PAIRS__</g>
<g id="wires">__WIRES__</g>
<g id="boxes">__BOXES__</g>
</svg>
</div>
<div id="card" hidden></div>
<script>
const FACTS = __FACTS__;
const ROOTS = __ROOTS__;
const map = document.getElementById("map");
const stage = document.getElementById("stage");
const card = document.getElementById("card");
const W = __W__, H = __H__;
let scale = 1;

function apply(){
  map.setAttribute("width", Math.round(W * scale));
  map.setAttribute("height", Math.round(H * scale));
}
function fit(){
  scale = Math.min(1.6, (stage.clientWidth - 4) / W);
  apply();
}
document.getElementById("fit").addEventListener("click", () => { fit(); });
document.getElementById("in").addEventListener("click", () => { scale *= 1.35; apply(); });
document.getElementById("out").addEventListener("click", () => { scale /= 1.35; apply(); });

function reach(start, key){
  const seen = new Set(), queue = [start];
  while(queue.length){
    const at = queue.pop();
    for(const next of FACTS[at][key]){
      if(!seen.has(next)){ seen.add(next); queue.push(next); }
    }
  }
  return seen;
}

function box(unit){ return map.querySelector('.node[data-u="' + CSS.escape(unit) + '"]'); }

function pick(unit){
  map.classList.add("picked");
  for(const n of map.querySelectorAll(".node")) n.classList.remove("on","here");
  for(const w of map.querySelectorAll(".wire")) w.classList.remove("on");
  const before = reach(unit, "u"), after = reach(unit, "d");
  const lit = new Set([...before, ...after, unit]);
  for(const u of lit) box(u).classList.add("on");
  box(unit).classList.add("here");
  for(const w of map.querySelectorAll(".wire")){
    if(lit.has(w.dataset.a) && lit.has(w.dataset.b)) w.classList.add("on");
  }
  show(unit, before.size, after.size);
  const r = box(unit).getBoundingClientRect(), s = stage.getBoundingClientRect();
  stage.scrollBy({left: r.left - s.left - s.width/2, top: r.top - s.top - s.height/2,
                  behavior: "smooth"});
}

function clear(){
  map.classList.remove("picked");
  for(const n of map.querySelectorAll(".node")) n.classList.remove("on","here");
  for(const w of map.querySelectorAll(".wire")) w.classList.remove("on");
  card.hidden = true;
}

function list(title, units){
  if(!units.length) return "<h3>" + title + "</h3><p class=none>Nothing.</p>";
  const items = units.map(u =>
    '<li><button data-go="' + u + '">' + FACTS[u].n + "</button></li>").join("");
  return "<h3>" + title + "</h3><ul>" + items + "</ul>";
}

function show(unit, before, after){
  const f = FACTS[unit];
  const row = "Row " + (f.r + 1) + ". " + before + " behind it, " + after + " ahead of it.";
  card.innerHTML = "<h2>" + f.n + "</h2><p>" + row + "</p>"
    + list("Needs first", f.u) + list("Opens up", f.d);
  card.hidden = false;
}

map.addEventListener("click", e => {
  const node = e.target.closest(".node");
  if(node) pick(node.dataset.u); else clear();
});
card.addEventListener("click", e => {
  const go = e.target.closest("[data-go]");
  if(go) pick(go.dataset.go);
});

const find = document.getElementById("find");
find.addEventListener("input", () => {
  const q = find.value.trim().toLowerCase();
  let first = null;
  for(const n of map.querySelectorAll(".node")){
    const hit = q.length > 1 && FACTS[n.dataset.u].n.toLowerCase().includes(q);
    n.classList.toggle("found", hit);
    if(hit && !first) first = n;
  }
  if(first){
    const r = first.getBoundingClientRect(), s = stage.getBoundingClientRect();
    stage.scrollBy({left: r.left - s.left - s.width/2,
                    top: r.top - s.top - s.height/2, behavior: "smooth"});
  }
});

addEventListener("resize", () => {});
fit();
</script></body></html>
"""


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "topic-graph.html")
    topics = yaml.safe_load(TOPICS.read_text())["topics"]
    g = revise(topics, judgements())
    depth, group = layers(topics, g["edges"], g["levels"])
    out.write_text(page(topics, g, depth, group))
    print(f"wrote {out} — {len(topics)} topics, {len(g['edges'])} arrows, "
          f"{len(g['levels'])} two-way pairs, {max(depth.values()) + 1} layers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
