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


def page(topics: dict, g: dict, depth: dict, group: dict) -> str:
    """One page: a search box, the columns, and the arrows for whatever you
    point at.

    Two things it deliberately does not do. It does not ink all 387 arrows at
    once, because a graph this size drawn in full is a grey wash nobody can
    read a single path out of. And it does not lay the columns out by subject
    heading: the columns come from `verticals()`, so a column is a set of
    topics that mostly need each other, and the arrows that leave one are rare
    enough to be worth marking.
    """
    unit_of = {c: u for u, members in group.items() for c in members}
    column = verticals(topics, g["edges"], g["levels"])

    # A column is named after whichever of its topics the others most depend
    # on, so the heading is a real topic rather than a label somebody invented.
    pull = collections.Counter()
    for a, b in g["edges"]:
        if column[a] == column[b]:
            pull[a] += 1
    order = collections.Counter(column.values())
    names = {}
    for col in order:
        members = [c for c in topics if column[c] == col]
        names[col] = topics[max(members, key=lambda c: (pull[c], c))]["name"]

    # Depth two ways. Global keeps every column on the same rows, so a crossing
    # arrow always points downwards. Local packs each column tight from its own
    # first topic, which is shorter to read and lets a crossing point upwards.
    local: dict[str, int] = {}
    for col in order:
        members = [c for c in topics if column[c] == col]
        inside = {(a, b) for a, b in g["edges"]
                  if column[a] == col and column[b] == col}
        above = collections.defaultdict(set)
        for a, b in inside:
            if unit_of[a] != unit_of[b]:
                above[b].add(a)
        for _ in range(len(members) + 1):
            for c in sorted(members, key=lambda c: depth[unit_of[c]]):
                want = max((local.get(p, 0) + 1 for p in above[c]), default=0)
                local[c] = max(local.get(c, 0), want)

    data = {
        "topics": {
            c: {
                "name": topics[c]["name"],
                "plain": " ".join(str(topics[c].get("plain", "")).split()),
                "col": column[c],
                "deep": depth[unit_of[c]],
                "near": local[c],
            }
            for c in sorted(topics)
        },
        "columns": [
            {"key": col, "name": names[col], "size": order[col]}
            for col in sorted(order, key=lambda k: (-order[k], names[k]))
        ],
        "edges": sorted([a, b] for a, b in g["edges"]),
        "levels": sorted([a, b] for a, b in g["levels"]),
    }

    crossing = sum(1 for a, b in g["edges"] if column[a] != column[b])
    counts = (f'{len(topics)} topics in {len(order)} columns · '
              f'{len(g["edges"])} arrows, {crossing} of them crossing a column · '
              f'{len(g["levels"])} two-way pairs')
    return (TEMPLATE.replace("__DATA__", json.dumps(data))
                    .replace("__COUNTS__", counts))


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The topic map</title>
<style>
:root{--bg:#fdfcfa;--card:#fff;--ink:#1a1a1a;--muted:#5f6b7a;--navy:#1b2a4a;
 --brand:#d4692a;--rule:#e3ddd2;--panel:#f6f3ee;--up:#1b6b8f;--down:#b0541f;
 --serif:Georgia,"Iowan Old Style",serif;
 --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
 --mono:ui-monospace,SFMono-Regular,Menlo,monospace}
@media (prefers-color-scheme:dark){:root{--bg:#14181f;--card:#1b2129;--ink:#e6e3dd;
 --muted:#98a2b3;--navy:#b9c8e6;--rule:#2a3140;--panel:#1b2129;--up:#7ec7e8;--down:#e8a06a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans)}
header{position:sticky;top:0;z-index:3;background:var(--bg);
 border-bottom:1px solid var(--rule);padding:.75rem 1rem}
h1{font-family:var(--serif);color:var(--navy);font-size:1.2rem;margin:0 0 .15rem}
.sub{font-family:var(--mono);font-size:.68rem;color:var(--muted);margin:0}
.tools{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;margin-top:.6rem}
#q{flex:1 1 16rem;min-width:12rem;padding:.5rem .7rem;font:inherit;font-size:.9rem;
 border:1px solid var(--rule);border-radius:8px;background:var(--card);color:var(--ink)}
#q:focus{outline:2px solid var(--brand);outline-offset:1px}
label{font-size:.76rem;color:var(--muted);display:flex;gap:.3rem;align-items:center}
.key{font-size:.7rem;color:var(--muted);display:flex;gap:.8rem;flex-wrap:wrap}
.key i{font-style:normal;display:inline-flex;gap:.3rem;align-items:center}
.sw{width:1.3rem;height:0;border-top:2px solid}
#hits{font-family:var(--mono);font-size:.68rem;color:var(--brand)}

#stage{position:relative;overflow-x:auto;padding:1rem}
svg{position:absolute;inset:0;pointer-events:none;z-index:0;overflow:visible}
#cols{position:relative;z-index:1;display:flex;gap:1.1rem;align-items:flex-start;
 min-width:max-content}
.col{display:flex;flex-direction:column;gap:.3rem;width:11.5rem}
.col h2{font-family:var(--mono);font-size:.6rem;letter-spacing:.08em;
 text-transform:uppercase;color:var(--brand);margin:0 0 .2rem;
 position:sticky;top:0;background:var(--bg);padding:.15rem 0}
.col h2 span{color:var(--muted)}
.band{min-height:.1rem;display:flex;flex-direction:column;gap:.25rem}
.chip{background:var(--card);border:1px solid var(--rule);border-radius:7px;
 padding:.35rem .45rem;font-size:.73rem;line-height:1.2;color:var(--navy);
 cursor:pointer;transition:border-color .1s,opacity .1s}
.chip.lv{border-style:dashed;border-color:var(--brand)}
.chip.on{border-color:var(--brand);border-width:2px;background:var(--panel);font-weight:600}
.chip.up{border-color:var(--up)}
.chip.down{border-color:var(--down)}
.chip.dim{opacity:.25}
.chip.hit{background:var(--brand);color:#fff;border-color:var(--brand)}
#detail{position:sticky;bottom:0;z-index:3;background:var(--panel);
 border-top:1px solid var(--rule);padding:.6rem 1rem;font-size:.8rem;min-height:2.6rem}
#detail b{color:var(--navy)}
#detail .p{color:var(--muted);font-size:.76rem}
</style></head><body>

<header>
  <h1>The topic map</h1>
  <p class="sub">__COUNTS__</p>
  <div class="tools">
    <input id="q" type="search" placeholder="Find a topic…" autocomplete="off">
    <span id="hits"></span>
    <label><input type="checkbox" id="tight"> Pack each column</label>
    <label><input type="checkbox" id="all"> Ink every arrow</label>
    <span class="key">
      <i><span class="sw" style="border-color:var(--up)"></span>needs this</i>
      <i><span class="sw" style="border-color:var(--down)"></span>needs the one you are on</i>
      <i><span class="sw" style="border-color:var(--brand);border-top-style:dashed"></span>crosses a column</i>
    </span>
  </div>
</header>

<div id="stage"><svg id="wires"></svg><div id="cols"></div></div>
<div id="detail">Point at a topic to see what it needs.</div>

<script>
const D = __DATA__;
const T = D.topics;
const into = {}, outof = {}, level = {};
D.edges.forEach(([a,b]) => { (outof[a] ||= []).push(b); (into[b] ||= []).push(a); });
D.levels.forEach(([a,b]) => { (level[a] ||= []).push(b); (level[b] ||= []).push(a); });

const cols = document.getElementById("cols");
const svg = document.getElementById("wires");
const stage = document.getElementById("stage");
const chip = {};

function draw(){
  const tight = document.getElementById("tight").checked;
  const key = tight ? "near" : "deep";
  cols.replaceChildren();
  for(const col of D.columns){
    const box = document.createElement("div");
    box.className = "col";
    box.innerHTML = "<h2>" + col.name + " <span>" + col.size + "</span></h2>";
    const rows = {};
    for(const [code, t] of Object.entries(T)){
      if(t.col !== col.key) continue;
      (rows[t[key]] ||= []).push(code);
    }
    const deepest = Math.max(...Object.values(T).map(t => t[key]));
    for(let r = 0; r <= deepest; r++){
      const band = document.createElement("div");
      band.className = "band";
      /* In the aligned mode every column carries every row, empty or not, so
         a topic on row 7 sits level with every other row-7 topic and a
         crossing arrow can only point downwards. */
      if(!tight) band.style.minHeight = "1.9rem";
      for(const code of (rows[r] || []).sort((x,y) => T[x].name.localeCompare(T[y].name))){
        const el = document.createElement("div");
        el.className = "chip" + (level[code] ? " lv" : "");
        el.textContent = T[code].name;
        el.dataset.code = code;
        band.appendChild(el);
        chip[code] = el;
      }
      box.appendChild(band);
    }
    cols.appendChild(box);
  }
  bind();
  if(document.getElementById("all").checked) inkAll(); else clear();
}

function wire(a, b, colour, faint, dashed){
  const s = stage.getBoundingClientRect();
  const p = chip[a].getBoundingClientRect(), q = chip[b].getBoundingClientRect();
  const x1 = p.left - s.left + stage.scrollLeft + p.width/2, y1 = p.bottom - s.top;
  const x2 = q.left - s.left + stage.scrollLeft + q.width/2, y2 = q.top - s.top;
  const mid = (y1 + y2) / 2;
  const path = document.createElementNS("http://www.w3.org/2000/svg","path");
  path.setAttribute("d", `M${x1},${y1} C${x1},${mid} ${x2},${mid} ${x2},${y2}`);
  path.setAttribute("fill","none");
  path.setAttribute("stroke", colour);
  path.setAttribute("stroke-width", faint ? 1 : 1.8);
  path.setAttribute("opacity", faint ? .14 : .85);
  if(dashed) path.setAttribute("stroke-dasharray","4 3");
  svg.appendChild(path);
}
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const crosses = (a,b) => T[a].col !== T[b].col;

function clear(){
  svg.replaceChildren();
  Object.values(chip).forEach(c => c.className =
    c.className.replace(/ (on|up|down|dim)/g,""));
}

function focus(code){
  clear();
  const up = into[code] || [], down = outof[code] || [], lv = level[code] || [];
  const near = new Set([code, ...up, ...down, ...lv]);
  Object.values(chip).forEach(c => { if(!near.has(c.dataset.code)) c.classList.add("dim"); });
  chip[code].classList.add("on");
  up.forEach(a => { chip[a].classList.add("up");
    wire(a, code, crosses(a,code) ? css("--brand") : css("--up"), false, crosses(a,code)); });
  down.forEach(b => { chip[b].classList.add("down");
    wire(code, b, crosses(code,b) ? css("--brand") : css("--down"), false, crosses(code,b)); });
  lv.forEach(x => { chip[x].classList.add("on");
    wire(code, x, css("--brand"), false, true); wire(x, code, css("--brand"), false, true); });

  const t = T[code];
  const say = list => list.length ? list.map(c => T[c].name).join(", ") : "nothing";
  document.getElementById("detail").innerHTML =
    "<b>" + t.name + "</b> \\u00b7 needs " + say(up) + " \\u00b7 needed by " + say(down)
    + (lv.length ? " \\u00b7 at one level with " + say(lv) : "")
    + "<div class='p'>" + t.plain + "</div>";
}

function inkAll(){
  clear();
  D.edges.forEach(([a,b]) => wire(a, b, crosses(a,b) ? css("--brand") : css("--muted"),
                                 true, crosses(a,b)));
}

function bind(){
  Object.values(chip).forEach(el => {
    el.addEventListener("pointerenter", () => { if(!all.checked) focus(el.dataset.code); });
    el.addEventListener("click", () => focus(el.dataset.code));
  });
}

const q = document.getElementById("q");
q.addEventListener("input", () => {
  const term = q.value.trim().toLowerCase();
  let n = 0, first = null;
  Object.entries(chip).forEach(([code, el]) => {
    const hit = term && (T[code].name.toLowerCase().includes(term)
                      || T[code].plain.toLowerCase().includes(term));
    el.classList.toggle("hit", !!hit);
    if(hit){ n++; first ||= code; }
  });
  document.getElementById("hits").textContent = term ? n + " found" : "";
  /* Bring the first match into view without moving anything else: the map
     stays where it was, so a search never costs you your place. */
  if(first) chip[first].scrollIntoView({block:"center", inline:"center", behavior:"smooth"});
});
q.addEventListener("keydown", e => {
  if(e.key !== "Enter") return;
  const hit = Object.entries(chip).find(([,el]) => el.classList.contains("hit"));
  if(hit) focus(hit[0]);
});

const all = document.getElementById("all");
all.addEventListener("change", () => all.checked ? inkAll() : clear());
document.getElementById("tight").addEventListener("change", draw);
stage.addEventListener("pointerleave", () => { if(all.checked) inkAll(); else clear(); });
addEventListener("resize", () => { if(all.checked) inkAll(); else clear(); });
draw();
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
