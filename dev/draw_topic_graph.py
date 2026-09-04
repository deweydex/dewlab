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

The page does not draw all 117 arrows at once. A layered graph this wide is a
hairball when every edge is inked, and the question a reader actually has is
about one topic at a time: what does this need, and what needs it. So arrows
are drawn for the topic under the pointer, and a toggle inks the rest faintly
for anyone who wants the shape of the whole thing.
"""

from __future__ import annotations

import collections
import glob
import html
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "planning" / "curriculum" / "topics.yaml"
BLIND = ROOT / "planning" / "curriculum" / "review" / "blind"


def judgements() -> dict[str, dict]:
    runs: dict[str, dict] = collections.defaultdict(dict)
    for path in sorted(glob.glob(str(BLIND / "*.json"))):
        batch = json.loads(Path(path).read_text())
        for j in batch.get("judgements") or []:
            pair = j.get("pair") or []
            if len(pair) == 2:
                runs[batch["by"]][tuple(sorted(pair))] = (j["verdict"], j.get("first"))
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
    return {"edges": edges, "levels": levels, "dropped": dropped,
            "turned": turned, "added": arrows - existing, "existing": existing}


def layers(topics: dict, edges: set, levels: set) -> tuple[dict, dict]:
    """Which layer each unit sits on, with a level pair counting as one unit."""
    parent = {c: c for c in topics}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for x, y in levels:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    group = collections.defaultdict(list)
    for c in topics:
        group[find(c)].append(c)

    above = collections.defaultdict(set)
    for early, late in edges:
        if find(early) != find(late):
            above[find(late)].add(find(early))

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
        raise SystemExit(f"{len(group) - len(depth)} units sit in a loop and "
                         "cannot be layered; fix the loop first")
    return depth, group


BAND = ["needs nothing before it", "second", "third", "fourth", "fifth",
        "sixth", "seventh", "eighth"]


def page(topics: dict, g: dict, depth: dict, group: dict) -> str:
    unit_of = {c: u for u, members in group.items() for c in members}
    rows = collections.defaultdict(list)
    for unit, members in group.items():
        rows[depth[unit]].append(unit)
    for band in rows.values():
        band.sort(key=lambda u: topics[u]["name"])

    data = {
        "units": {u: [{"id": c, "name": topics[c]["name"]} for c in sorted(members)]
                  for u, members in group.items()},
        "edges": [[unit_of[a], unit_of[b]] for a, b in sorted(g["edges"])
                  if unit_of[a] != unit_of[b]],
    }

    bands = []
    for i in sorted(rows):
        chips = []
        for unit in rows[i]:
            members = sorted(group[unit])
            inner = '<span class="tie">&harr;</span>'.join(
                f'<b>{html.escape(topics[c]["name"])}</b>' for c in members)
            cls = "chip level" if len(members) > 1 else "chip"
            chips.append(f'<div class="{cls}" data-u="{html.escape(unit)}">{inner}</div>')
        label = BAND[i] if i < len(BAND) else f"layer {i + 1}"
        bands.append(
            f'<section class="band"><h2>{i + 1}. {label}'
            f'<span>{len(rows[i])}</span></h2><div class="chips">'
            + "".join(chips) + "</div></section>")

    counts = (f'{len(topics)} topics · {len(g["edges"])} arrows · '
              f'{len(g["levels"])} two-way pairs · {max(depth.values()) + 1} layers')
    return TEMPLATE.replace("__BANDS__", "".join(bands)) \
                   .replace("__DATA__", json.dumps(data)) \
                   .replace("__COUNTS__", counts) \
                   .replace("__WAS__", f'{len(g["existing"])} arrows before, '
                            f'{len(g["dropped"])} dropped, {len(g["added"])} added, '
                            f'{len(g["turned"])} turned round')


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The topic graph the judges built</title>
<style>
:root{--bg:#fdfcfa;--card:#fff;--ink:#1a1a1a;--muted:#5f6b7a;--navy:#1b2a4a;
 --brand:#d4692a;--rule:#e3ddd2;--panel:#f6f3ee;--up:#1b6b8f;--down:#b0541f;
 --serif:Georgia,"Iowan Old Style",serif;--sans:system-ui,-apple-system,"Segoe UI",sans-serif;
 --mono:ui-monospace,SFMono-Regular,Menlo,monospace}
@media (prefers-color-scheme:dark){:root{--bg:#14181f;--card:#1b2129;--ink:#e6e3dd;
 --muted:#98a2b3;--navy:#b9c8e6;--rule:#2a3140;--panel:#1b2129;--up:#7ec7e8;--down:#e8a06a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans)}
.wrap{max-width:78rem;margin:0 auto;padding:1.5rem 1rem 4rem}
h1{font-family:var(--serif);color:var(--navy);font-size:1.5rem;margin:0 0 .3rem}
.sub{font-family:var(--mono);font-size:.72rem;color:var(--muted);margin:0 0 .2rem}
.bar{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;margin:1rem 0;
 padding:.6rem;background:var(--panel);border:1px solid var(--rule);border-radius:8px}
.bar label{font-size:.78rem;color:var(--muted);display:flex;gap:.35rem;align-items:center}
.key{font-size:.72rem;color:var(--muted);display:flex;gap:.9rem;flex-wrap:wrap;margin-left:auto}
.key i{font-style:normal;display:inline-flex;gap:.3rem;align-items:center}
.sw{width:1.4rem;height:0;border-top:2px solid}
#stage{position:relative}
svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:visible}
.band{position:relative;z-index:1;margin:0 0 1.1rem}
.band h2{font-family:var(--mono);font-size:.66rem;letter-spacing:.09em;text-transform:uppercase;
 color:var(--brand);margin:0 0 .4rem;display:flex;gap:.5rem;align-items:baseline}
.band h2 span{color:var(--muted);font-size:.62rem}
.chips{display:flex;flex-wrap:wrap;gap:.35rem}
.chip{background:var(--card);border:1px solid var(--rule);border-radius:8px;
 padding:.4rem .55rem;font-size:.78rem;line-height:1.2;cursor:default;
 transition:border-color .12s,background .12s}
.chip b{font-weight:600;color:var(--navy)}
.chip.level{border-style:dashed;border-color:var(--brand);background:var(--panel)}
.tie{color:var(--brand);margin:0 .35rem;font-weight:700}
.chip.on{border-color:var(--brand);border-width:2px;background:var(--panel)}
.chip.up{border-color:var(--up)}
.chip.down{border-color:var(--down)}
.chip.dim{opacity:.32}
</style></head><body><div class="wrap">
<h1>The topic graph the judges built</h1>
<p class="sub">__COUNTS__</p>
<p class="sub">__WAS__</p>

<div class="bar">
  <label><input type="checkbox" id="all"> Ink every arrow at once</label>
  <span class="key">
    <i><span class="sw" style="border-color:var(--up)"></span> needs this first</i>
    <i><span class="sw" style="border-color:var(--down)"></span> needs the one you are on</i>
    <i><span class="sw" style="border-color:var(--brand);border-top-style:dashed"></span> a level, two ways</i>
  </span>
</div>

<div id="stage"><svg id="wires"></svg>__BANDS__</div>
</div>
<script>
const D = __DATA__;
const stage = document.getElementById("stage"), svg = document.getElementById("wires");
const chips = [...document.querySelectorAll(".chip")];
const byUnit = Object.fromEntries(chips.map(c => [c.dataset.u, c]));
const into = {}, outof = {};
D.edges.forEach(([a,b]) => { (outof[a] ||= []).push(b); (into[b] ||= []).push(a); });

/* A curve from the bottom of one chip to the top of another, in the stage's
   own coordinates so it survives a reflow at any width. */
function wire(a, b, colour, faint){
  const s = stage.getBoundingClientRect();
  const p = byUnit[a].getBoundingClientRect(), q = byUnit[b].getBoundingClientRect();
  const x1 = p.left - s.left + p.width/2, y1 = p.bottom - s.top;
  const x2 = q.left - s.left + q.width/2, y2 = q.top - s.top;
  const mid = (y1 + y2) / 2;
  const path = document.createElementNS("http://www.w3.org/2000/svg","path");
  path.setAttribute("d", `M${x1},${y1} C${x1},${mid} ${x2},${mid} ${x2},${y2}`);
  path.setAttribute("fill","none");
  path.setAttribute("stroke", colour);
  path.setAttribute("stroke-width", faint ? 1 : 1.8);
  path.setAttribute("opacity", faint ? .16 : .85);
  svg.appendChild(path);
}
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

function clear(){ svg.replaceChildren(); chips.forEach(c => c.className =
  c.className.replace(/ (on|up|down|dim)/g,"")); }

function focus(u){
  clear();
  const up = into[u] || [], down = outof[u] || [];
  chips.forEach(c => { if(c.dataset.u !== u && !up.includes(c.dataset.u)
    && !down.includes(c.dataset.u)) c.classList.add("dim"); });
  byUnit[u].classList.add("on");
  up.forEach(a => { byUnit[a].classList.add("up"); wire(a, u, css("--up")); });
  down.forEach(b => { byUnit[b].classList.add("down"); wire(u, b, css("--down")); });
}

function inkAll(){
  clear();
  D.edges.forEach(([a,b]) => wire(a, b, css("--muted"), true));
}

chips.forEach(c => {
  c.addEventListener("pointerenter", () => { if(!all.checked) focus(c.dataset.u); });
  c.addEventListener("click", () => focus(c.dataset.u));
});
stage.addEventListener("pointerleave", () => { if(all.checked) inkAll(); else clear(); });
const all = document.getElementById("all");
all.addEventListener("change", () => all.checked ? inkAll() : clear());
addEventListener("resize", () => { if(all.checked) inkAll(); else clear(); });
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
