// The topic map. build.py puts the map's data in a block in the page
// (#dewlab-map) and an empty frame (#dl-tmap); this draws the land in the
// frame and runs it. The picture is for a reader with a pointer or a touch
// screen. Everything in it is also in the list under it, which needs no script.

const NS = "http://www.w3.org/2000/svg";
const SHADES = [0, 3.5, -3, 2, -4.5, 1.5, -1.5];
const ROLE = { teaches: "", "closer-look": "a closer look", context: "background", applies: "put to work" };
const TOWER_SVG = '<svg viewBox="0 0 18 22" aria-hidden="true"><path d="M1 21V9h2V3h3v3h2V3h2v3h2V3h3v6h2v12z" fill="currentColor" stroke="var(--dl-bg)" stroke-width="1.2" stroke-linejoin="round"/><path d="M7.5 21v-4.5a1.5 1.5 0 0 1 3 0V21z" fill="var(--dl-bg)"/></svg>';
const TERRAIN = {
  mountains: [120, 100, "M14 70L34 38L54 70M62 96L78 70L94 96"],
  forest: [100, 100, "M16 40a10 10 0 1 0 20 0a10 10 0 1 0 -20 0M26 50V60M64 80a8 8 0 1 0 16 0a8 8 0 1 0 -16 0M72 88V96"],
};
const PHONE = 760; // a frame narrower than this puts its panel in a sheet along the bottom

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const svgEl = (tag, attrs, parent) => {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
};
const div = (cls, parent, tag = "div") => {
  const n = document.createElement(tag);
  n.className = cls;
  if (parent) parent.appendChild(n);
  return n;
};

// The outlines come from the layout as straight pieces between a few points.
// Cutting each corner twice (Chaikin's way: a new point a quarter of the way
// along each piece from each end) rounds them into coasts and borders, and
// costs a quarter of the bytes that sending the rounded outline would.
function smooth(d) {
  return d.split("Z").filter((sub) => sub.trim()).map((sub) => {
    const n = sub.match(/-?\d+(?:\.\d+)?/g).map(Number);
    let pts = [];
    for (let i = 0; i < n.length; i += 2) pts.push([n[i], n[i + 1]]);
    for (let round = 0; round < 2; round++) {
      const out = [];
      for (let k = 0; k < pts.length - 1; k++) {
        const [x1, y1] = pts[k], [x2, y2] = pts[k + 1];
        out.push([0.75 * x1 + 0.25 * x2, 0.75 * y1 + 0.25 * y2], [0.25 * x1 + 0.75 * x2, 0.25 * y1 + 0.75 * y2]);
      }
      out.push(out[0]);
      pts = out;
    }
    return "M" + pts.map(([x, y]) => `${x.toFixed(0)} ${y.toFixed(0)}`).join("L") + "Z";
  }).join("");
}

function stopsWords(tier) {
  if (tier === 0) return "needs nothing first";
  return `${tier} stop${tier === 1 ? "" : "s"} on the longest road to it`;
}

function start(root, data) {
  const towns = data.towns;
  const byCode = new Map(towns.map((t) => [t.code, t]));
  const regionById = new Map(data.regions.map((r) => [r.id, r]));
  const districtById = new Map(data.districts.map((d) => [d.id, d]));
  const continents = data.continents;
  const contById = new Map(continents.map((c) => [c.id, c]));
  const startLand = (continents.find((c) => c.kind === "start") || {}).id;
  const tower = data.tower || {};
  const plainsName = (tower.plains || {}).name || "The Prerequisite Plains";
  for (const r of data.regions) r.full = r.fancy ? `${r.fancy} (${r.name})` : r.name;
  for (const c of continents) c.full = c.fancy ? `${c.fancy} (${c.name})` : c.name;
  data.coast = smooth(data.coast);
  data.plains.land = smooth(data.plains.land);
  for (const r of data.regions) r.land = smooth(r.land);
  for (const d of data.districts) if (d.land) d.land = smooth(d.land);

  const landColour = (r, shade) => `hsl(${r.hue} var(--map-land-s) calc(var(--map-land-l) + ${SHADES[(shade || 0) % SHADES.length]}%))`;
  const contColour = (c) => (c.kind === "start" ? "var(--map-plains)" : `hsl(${c.hue} var(--map-land-s) var(--map-land-l))`);

  const landmarksAt = new Map(towns.map((t) => [t.code, []]));
  for (const lm of data.landmarks) for (const a of lm.at) landmarksAt.get(a).push(lm);
  const children = new Map(towns.map((t) => [t.code, []]));
  for (const t of towns) for (const n of t.needs) children.get(n).push(t.code);

  // ---------- the frame
  root.innerHTML = `
    <div class="dl-tmap-stage"><svg class="dl-tmap-svg" aria-hidden="true"><g></g></svg><svg class="dl-tmap-leaders" aria-hidden="true"></svg><div class="dl-tmap-overlay"></div></div>
    <div class="dl-tmap-top dl-tmap-card">
      <label for="dl-tmap-q" class="dl-sr-only">Find a topic</label>
      <input id="dl-tmap-q" type="search" placeholder="Find a topic, like logarithms" autocomplete="off">
      <ul class="dl-tmap-results" role="listbox" aria-label="Topics that match"></ul>
    </div>
    <div class="dl-tmap-controls">
      <div class="dl-tmap-zoom">
        <button type="button" data-zoom="out" aria-label="Zoom out">−</button>
        <button type="button" data-zoom="fit">whole map</button>
        <button type="button" data-zoom="in" aria-label="Zoom in">+</button>
        <button type="button" class="dl-tmap-layers-toggle" aria-expanded="false">layers</button>
      </div>
      <div class="dl-tmap-layers dl-tmap-card">
        <h3>Layers</h3>
        <label><input type="checkbox" data-roads checked> Roads between towns</label>
        <div><label for="dl-tmap-course">A course as a road</label><select id="dl-tmap-course"><option value="">None</option></select></div>
      </div>
    </div>
    <aside class="dl-tmap-panel dl-tmap-card" aria-label="About the map">
      <button type="button" class="dl-tmap-grab" aria-label="Show or hide the panel"></button>
      <div class="dl-tmap-body"></div>
    </aside>`;
  root.hidden = false;
  const stage = root.querySelector(".dl-tmap-stage");
  const world = root.querySelector(".dl-tmap-svg g");
  const overlay = root.querySelector(".dl-tmap-overlay");
  const leaders = root.querySelector(".dl-tmap-leaders");
  const panel = root.querySelector(".dl-tmap-panel");
  const pbody = root.querySelector(".dl-tmap-body");
  const search = root.querySelector("#dl-tmap-q");
  const results = root.querySelector(".dl-tmap-results");
  const courseSel = root.querySelector("#dl-tmap-course");
  const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches || document.documentElement.dataset.motion === "reduced";

  const view = { k: 0.3, x: 0, y: 0 };
  let selected = null;
  let route = [];
  let courseLine = null;
  let visited = new Set();
  try { visited = new Set(JSON.parse(localStorage.getItem("dewlab:map:visited") || "[]")); } catch (e) { /* private mode */ }
  const saveVisited = () => { try { localStorage.setItem("dewlab:map:visited", JSON.stringify([...visited])); } catch (e) { /* private mode */ } };

  // ---------- the drawing
  const [bx, by, bw, bh] = data.bounds;
  svgEl("rect", { x: bx - 4000, y: by - 4000, width: bw + 8000, height: bh + 8000, fill: "var(--map-sea)" }, world);
  for (const [x, y] of data.waves) svgEl("path", { d: `M${x - 60} ${y}q30 -22 60 0t60 0`, class: "dl-tmap-wave", "vector-effect": "non-scaling-stroke" }, world);
  const defs = svgEl("defs", {}, world);
  for (const [name, [w, h, d]] of Object.entries(TERRAIN)) {
    const pat = svgEl("pattern", { id: `dl-tmap-terrain-${name}`, width: w, height: h, patternUnits: "userSpaceOnUse" }, defs);
    svgEl("path", { d, class: "dl-tmap-terrain-mark" }, pat);
  }
  svgEl("path", { d: data.coast, class: "dl-tmap-coast-fill" }, world);
  svgEl("path", { d: data.plains.land, class: "dl-tmap-plains" }, world);
  for (const r of data.regions) svgEl("path", { d: r.land, class: "dl-tmap-land", style: `fill:${landColour(r, 0)}` }, world);
  for (const d of data.districts) {
    if (d.land) svgEl("path", { d: d.land, class: "dl-tmap-county", style: `fill:${landColour(regionById.get(d.region), d.shade)}`, "vector-effect": "non-scaling-stroke" }, world);
  }
  for (const r of data.regions) {
    if (TERRAIN[r.terrain]) svgEl("path", { d: r.land, fill: `url(#dl-tmap-terrain-${r.terrain})`, "fill-rule": "evenodd" }, world);
  }
  for (const r of data.regions) svgEl("path", { d: r.land, class: "dl-tmap-border", "vector-effect": "non-scaling-stroke" }, world);
  svgEl("path", { d: data.coast, class: "dl-tmap-coast", "vector-effect": "non-scaling-stroke" }, world);

  // A road between two continents crosses the sea by a bridge. Two continents
  // with no bridge of their own are joined by way of the starting island.
  const bridgeEnds = new Map();
  for (const b of data.bridges) {
    bridgeEnds.set(b.a + "|" + b.b, b.ends);
    bridgeEnds.set(b.b + "|" + b.a, [b.ends[1], b.ends[0]]);
  }
  function via(a, b) {
    const la = byCode.get(a).land, lb = byCode.get(b).land;
    if (la === lb) return [];
    const direct = bridgeEnds.get(la + "|" + lb);
    if (direct) return direct;
    const one = bridgeEnds.get(la + "|" + startLand), two = bridgeEnds.get(startLand + "|" + lb);
    return one && two ? [...one, ...two] : [];
  }
  function pathThrough(codes) {
    return codes.map((c, i) => {
      const t = byCode.get(c);
      const bridge = i ? via(codes[i - 1], c).map(([x, y]) => `L${x} ${y}`).join("") : "";
      return `${bridge}${i ? "L" : "M"}${t.x} ${t.y}`;
    }).join("");
  }
  // A bridge is as wide as the traffic it carries, from 4px for one road to 12px for the busiest.
  const busiest = Math.max(2, ...data.bridges.map((b) => b.count));
  const contName = (id) => { const c = contById.get(id); return c ? c.fancy || c.name : id; };
  const bridgeLayer = svgEl("g", {}, world);
  for (const b of data.bridges) {
    const [[x1, y1], [x2, y2]] = b.ends;
    const width = 4 + 8 * Math.sqrt((b.count - 1) / (busiest - 1));
    const g = svgEl("g", {}, bridgeLayer);
    const d = `M${x1} ${y1}L${x2} ${y2}`;
    svgEl("path", { d, class: "dl-tmap-bridge-casing", style: `stroke-width:${(width + 4).toFixed(1)}px`, "vector-effect": "non-scaling-stroke" }, g);
    svgEl("path", { d, class: "dl-tmap-bridge-deck", style: `stroke-width:${width.toFixed(1)}px`, "vector-effect": "non-scaling-stroke" }, g);
    svgEl("path", { d, class: "dl-tmap-bridge-planks", style: `stroke-width:${width.toFixed(1)}px`, "vector-effect": "non-scaling-stroke" }, g);
    svgEl("title", {}, g).textContent = `A bridge between ${contName(b.a)} and ${contName(b.b)}. ${b.count} road${b.count === 1 ? " crosses" : "s cross"} it.`;
  }

  const roadLayer = svgEl("g", {}, world);
  const roads = [];
  for (const t of towns) {
    for (const n of t.needs) {
      const a = byCode.get(n);
      const mx = (a.x + t.x) / 2, my = (a.y + t.y) / 2;
      // bow each road a little, away from the middle, so parallel roads separate
      const len = Math.hypot(t.x - a.x, t.y - a.y) || 1;
      const nx = -(t.y - a.y) / len, ny = (t.x - a.x) / len;
      const side = (mx * nx + my * ny) > 0 ? 1 : -1;
      const bow = Math.min(60, len * 0.12) * side;
      const node = svgEl("path", {
        d: via(n, t.code).length ? pathThrough([n, t.code]) : `M${a.x} ${a.y} Q${mx + nx * bow} ${my + ny * bow} ${t.x} ${t.y}`,
        class: "dl-tmap-road" + (a.region !== t.region ? " is-border" : ""),
        "vector-effect": "non-scaling-stroke",
      }, roadLayer);
      roads.push({ from: n, to: t.code, node });
    }
  }
  const lineLayer = svgEl("g", {}, world);
  const routeLayer = svgEl("g", {}, world);

  // ---------- names, towns, the start
  const contLabels = continents.map((c) => {
    const b = div("dl-tmap-continent", overlay, "button");
    b.type = "button";
    b.innerHTML = c.fancy ? `${esc(c.fancy)}<small>${esc(c.name)}</small>` : esc(c.name);
    b.addEventListener("click", () => { if (!moved) showContinent(c); });
    return { item: c, node: b, spots: null };
  });
  const regionLabels = data.regions.map((r) => {
    const n = div("dl-tmap-region", overlay);
    n.innerHTML = r.fancy ? `${esc(r.fancy)}<small>${esc(r.name)}</small>` : esc(r.name);
    return { item: r, node: n, spots: r.spots };
  });
  const plainsLabel = (() => {
    const n = div("dl-tmap-region dl-tmap-plains-name", overlay);
    n.textContent = plainsName;
    return { item: { id: "plains" }, node: n, spots: data.plains.spots };
  })();
  regionLabels.push(plainsLabel);
  const districtLabels = data.districts.map((d) => {
    const n = div("dl-tmap-district", overlay);
    n.textContent = d.name;
    return { d, node: n };
  });
  const startMark = div("dl-tmap-start", overlay, "button");
  startMark.type = "button";
  startMark.innerHTML = `${TOWER_SVG}<span>Tower of<br>Unknowing</span>`;
  startMark.setAttribute("aria-label", "The Tower of Unknowing, where every traveller starts");
  startMark.addEventListener("click", () => { if (!moved) showTower(); });
  const landmarkNodes = data.landmarks.filter((lm) => !lm.tower).map((lm) => {
    const b = div("dl-tmap-landmark", overlay, "button");
    b.type = "button";
    b.innerHTML = `<span class="dl-tmap-glyph"></span><span class="dl-tmap-lmname">${esc(lm.title)}</span>`;
    b.setAttribute("aria-label", `${lm.title}, a ${lm.kind}`);
    b.addEventListener("click", () => { if (!moved) showLandmark(lm); });
    return { lm, b };
  });
  const streets = div("dl-tmap-streets", overlay, "ol");
  streets.setAttribute("aria-label", "Pages in this topic");

  const maxW = Math.max(...towns.map((t) => t.weight));
  const townNodes = towns.map((t) => {
    const b = div("dl-tmap-town", overlay, "button");
    b.type = "button";
    b.dataset.code = t.code;
    b.dataset.state = t.state;
    const d = 7 + Math.sqrt(t.weight / maxW) * 11;
    b.style.setProperty("--d", d.toFixed(1) + "px");
    b.innerHTML = `<span class="dl-tmap-dot"></span><span class="dl-tmap-name">${esc(t.name)}</span>`;
    b.setAttribute("aria-label", `${t.name}. ${districtById.get(t.district).name}, ${regionById.get(t.region).full}, ${stopsWords(t.tier)}.`);
    b.addEventListener("click", (ev) => { if (moved) { ev.preventDefault(); return; } select(t.code, true, true); });
    return { t, b, d, w: 0 };
  });

  // ---------- view
  // Five levels: continents, countries, districts, towns, and a town's own
  // streets. They are set against the scale that shows the whole map, so the
  // first view is continent names alone, whatever the size of the frame.
  let baseK = null;
  const lodFor = (k) => { const b = baseK || 0.2; return k < b * 1.4 ? 0 : k < b * 2.5 ? 1 : k < b * 4.4 ? 2 : k < b * 8 ? 3 : 4; };
  const frame = () => ({ W: stage.clientWidth, H: stage.clientHeight, phone: root.clientWidth <= PHONE });

  function viewportBox() {
    const { W, H, phone } = frame();
    const shut = panel.classList.contains("is-collapsed");
    return { left: 8, top: phone ? 64 : 8, right: phone ? W - 8 : W - 396, bottom: phone ? (shut ? H - 108 : H * 0.5) : H - 8 };
  }

  // Names are as wide on screen as the type makes them, so where each goes
  // depends on the screen. Each name has places to choose from (a continent's
  // are round its coast, a country's are well inside its land) and takes the
  // one that covers the fewest towns, bridges, other names and controls,
  // inside the view. The choice is kept while the zoom stays about the same,
  // so names do not jump about as the map is moved.
  const bridgeDots = [];
  for (const b of data.bridges) {
    const [[x1, y1], [x2, y2]] = b.ends;
    for (let i = 0; i <= 8; i++) bridgeDots.push([x1 + (x2 - x1) * i / 8, y1 + (y2 - y1) * i / 8]);
  }
  let placedFor = null;
  const placed = new Map();
  function placeNames(labels, kind, at) {
    const vb = viewportBox();
    const boxOf = (el) => { const r = el.getBoundingClientRect(), o = root.getBoundingClientRect(); return [r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top]; };
    const grow = (r, m) => [r[0] - m, r[1] - m, r[2] + m, r[3] + m];
    const inside = (r, [x, y]) => x > r[0] && x < r[2] && y > r[1] && y < r[3];
    const overlap = (a, b) => Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0])) * Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1]));
    const chrome = [boxOf(root.querySelector(".dl-tmap-top")), boxOf(root.querySelector(".dl-tmap-controls"))];
    const townDots = towns.map((t) => at(t.x, t.y));
    const barDots = bridgeDots.map(([x, y]) => at(x, y));
    const shores = continents.map((c) => c.shore.map(([x, y]) => at(x, y)));
    const centres = continents.map((c) => {
      const mine = towns.filter((t) => t.land === c.id).map((t) => at(t.x, t.y));
      return [mine.reduce((a, q) => a + q[0], 0) / mine.length, mine.reduce((a, q) => a + q[1], 0) / mine.length];
    });
    const mid = [centres.reduce((a, q) => a + q[0], 0) / centres.length, centres.reduce((a, q) => a + q[1], 0) / centres.length];
    const taken = [];
    // the big names first, so the small ones fit round them
    const order = labels.slice().sort((a, b) => (b.size || 0) - (a.size || 0));
    for (const label of order) {
      const node = label.node, w = node.offsetWidth, h = node.offsetHeight;
      const ci = kind === "continent" ? continents.indexOf(label.item) : -1;
      const away = ci >= 0 ? [centres[ci][0] - mid[0], centres[ci][1] - mid[1]] : [0, 0];
      const awayLen = Math.hypot(away[0], away[1]) || 1;
      let best = null;
      const spots = kind === "continent" ? label.item.shore : label.spots;
      // a continent's name may stand a little way out to sea as well as at the coast
      const gaps = kind === "continent" ? [8, 60, 130] : [0];
      spots.forEach(([wx, wy], k) => gaps.forEach((gap) => {
        const [sx, sy] = at(wx, wy);
        let x = sx, y = sy, cost = k * 0.15 + gap * 0.05;
        if (kind === "continent") {
          // beside the coast, on the sea side: step out along the direction this point lies in
          const a = 2 * Math.PI * k / spots.length, dx = Math.cos(a), dy = Math.sin(a);
          const reach = Math.min(w / 2 / Math.max(1e-6, Math.abs(dx)), h / 2 / Math.max(1e-6, Math.abs(dy)));
          x = sx + dx * (reach + gap);
          y = sy + dy * (reach + gap);
          cost += 4 * (1 - (dx * away[0] + dy * away[1]) / awayLen);
        }
        const r = [x - w / 2, y - h / 2, x + w / 2, y + h / 2], pad = grow(r, 6);
        cost += 40 * townDots.filter((q) => inside(pad, q)).length;
        cost += 25 * barDots.filter((q) => inside(pad, q)).length;
        // keep off the land of the other continents
        if (kind === "continent") shores.forEach((sh, j) => { if (j !== ci) cost += 30 * sh.filter((q) => inside(pad, q)).length; });
        for (const c of chrome) if (overlap(r, c) > 0) cost += 300;
        for (const q of taken) { const o = overlap(r, q); if (o > 0) cost += 150 + o / 40; }
        // a name cut off by the edge or the panel is worse than one over a town
        cost += 12 * (Math.max(0, vb.left - r[0]) + Math.max(0, r[2] - vb.right) + Math.max(0, vb.top - r[1]) + Math.max(0, r[3] - vb.bottom));
        if (!best || cost < best.cost) best = { cost, x, y, r, anchor: [wx, wy] };
      }));
      taken.push(best.r);
      placed.set(label, { world: [(best.x - view.x) / view.k, (best.y - view.y) / view.k], anchor: best.anchor });
    }
  }
  function placeAll(lod, at) {
    const { W, H } = frame();
    const key = `${lod}|${W}x${H}|${panel.classList.contains("is-collapsed")}`;
    const drift = placedFor && placedFor.key === key ? Math.abs(Math.log(view.k / placedFor.k)) : 9;
    if (drift < 0.12) return;
    placedFor = { key, k: view.k };
    placed.clear();
    for (const l of contLabels) l.size = towns.filter((t) => t.land === l.item.id).length;
    for (const l of regionLabels) l.size = l.item.count || 99;
    if (lod === 0) placeNames(contLabels, "continent", at);
    if (lod === 1 || lod === 2) placeNames(regionLabels, "region", at);
  }

  function render() {
    world.setAttribute("transform", `translate(${view.x} ${view.y}) scale(${view.k})`);
    const lod = lodFor(view.k);
    root.dataset.lod = lod;
    root.classList.toggle("is-phone", root.clientWidth <= PHONE);
    const { W, H } = frame();
    const at = (x, y) => [x * view.k + view.x, y * view.k + view.y];
    if (!townNodes[0].w) for (const n of townNodes) n.w = n.b.querySelector(".dl-tmap-name").offsetWidth;
    placeAll(lod, at);
    const put = (node, [wx, wy]) => { const [sx, sy] = at(wx, wy); node.style.transform = `translate(${sx}px, ${sy}px) translate(-50%, -50%)`; return [sx, sy]; };
    const names = [];
    leaders.replaceChildren();
    for (const l of contLabels) {
      const p = placed.get(l);
      if (!p || lod !== 0) continue;
      const [sx, sy] = put(l.node, p.world);
      names.push([l.node, [sx, sy]]);
      // A name that stands well away from its land is joined to it by a thin line.
      const w = l.node.offsetWidth, h = l.node.offsetHeight, [ax, ay] = at(p.anchor[0], p.anchor[1]);
      const ex = Math.max(sx - w / 2, Math.min(ax, sx + w / 2)), ey = Math.max(sy - h / 2, Math.min(ay, sy + h / 2));
      if (Math.hypot(ax - ex, ay - ey) > 36) svgEl("line", { x1: ax, y1: ay, x2: ex, y2: ey, class: "dl-tmap-leader" }, leaders);
    }
    for (const l of regionLabels) { const p = placed.get(l); if (p && (lod === 1 || lod === 2)) names.push([l.node, put(l.node, p.world)]); }
    for (const { d, node } of districtLabels) put(node, d.label);
    for (const { lm, b } of landmarkNodes) {
      const [sx, sy] = at(lm.x, lm.y);
      b.style.transform = `translate(${sx}px, ${sy}px)`;
      b.classList.toggle("is-lit", selected != null && lm.at.includes(selected));
    }
    startMark.style.transform = `translate(${view.x}px, ${view.y}px) translate(-50%, -50%)`;

    // At the widest views a name is as big as the country it names, so the
    // towns under it are left out, as a street map clears what lies under a label.
    const under = lod <= 1 ? names.map(([node, [sx, sy]]) => [sx - node.offsetWidth / 2 - 12, sy - node.offsetHeight / 2 - 12, sx + node.offsetWidth / 2 + 12, sy + node.offsetHeight / 2 + 12]) : [];
    for (const n of townNodes) {
      const sx = n.t.x * view.k + view.x, sy = n.t.y * view.k + view.y;
      n.b.classList.toggle("is-under-name", under.some((r) => sx > r[0] && sx < r[2] && sy > r[1] && sy < r[3]));
    }

    // Town names go down most important first, and any that would collide
    // with one already down, or with a name that is showing, stay hidden, as
    // on a street map.
    const taken = [];
    const note = (node, sx, sy) => { const w = node.offsetWidth, h = node.offsetHeight; taken.push([sx - w / 2 - 4, sy - h / 2 - 2, sx + w / 2 + 4, sy + h / 2 + 2]); };
    for (const [node, [sx, sy]] of names) note(node, sx, sy);
    if (lod === 2) for (const { d, node } of districtLabels) note(node, ...at(d.label[0], d.label[1]));
    if (lod >= 3 && selected) {
      const t = byCode.get(selected);
      const [sx, sy] = at(t.x, t.y);
      streets.style.transform = `translate(${sx + 10}px, ${sy + 30}px)`;
      taken.push([sx, sy + 20, sx + streets.offsetWidth + 20, sy + 30 + streets.offsetHeight]);
    }
    const minWeight = lod <= 1 ? 1e9 : lod === 2 ? 4 : 0;
    for (const n of townNodes.slice().sort((a, b) => prio(b) - prio(a))) {
      const sx = n.t.x * view.k + view.x, sy = n.t.y * view.k + view.y;
      n.b.style.transform = `translate(${sx}px, ${sy}px)`;
      const off = sx < -200 || sy < -100 || sx > W + 200 || sy > H + 100;
      n.b.style.visibility = off ? "hidden" : "";
      if (off) continue;
      const forced = n.t.code === selected || route.includes(n.t.code);
      let show = forced || n.t.weight >= minWeight || (lod >= 2 && courseLine && courseLine.includes(n.t.code));
      const rect = [sx - n.w / 2 - 3, sy + n.d / 2 + 2, sx + n.w / 2 + 3, sy + n.d / 2 + 20];
      if (show && !forced) for (const p of taken) if (rect[0] < p[2] && rect[2] > p[0] && rect[1] < p[3] && rect[3] > p[1]) { show = false; break; }
      if (show) taken.push(rect);
      n.b.classList.toggle("is-hidden-label", !show);
    }
    // At the town level a district's name gives way to a town's.
    if (lod >= 3) {
      for (const { d, node } of districtLabels) {
        const [sx, sy] = at(d.label[0], d.label[1]);
        const w = node.offsetWidth, h = node.offsetHeight;
        const box = [sx - w / 2, sy - h / 2, sx + w / 2, sy + h / 2];
        let clash = false;
        for (const n of townNodes) {
          if (n.b.classList.contains("is-hidden-label")) continue;
          const tx = n.t.x * view.k + view.x, ty = n.t.y * view.k + view.y;
          const r = [tx - n.w / 2, ty + n.d / 2 + 2, tx + n.w / 2, ty + n.d / 2 + 20];
          if (box[0] < r[2] && box[2] > r[0] && box[1] < r[3] && box[3] > r[1]) { clash = true; break; }
        }
        node.classList.toggle("is-given-way", clash);
      }
    } else for (const { node } of districtLabels) node.classList.remove("is-given-way");
  }
  function prio(n) {
    let p = n.t.weight;
    if (n.t.code === selected) p += 1000;
    if (route.includes(n.t.code)) p += 500;
    if (visited.has(n.t.code)) p += 3;
    return p;
  }
  function fitTo(x0, y0, x1, y1, animate, maxK) {
    const vb = viewportBox(), pad = 32;
    const k = Math.min((vb.right - vb.left - pad * 2) / (x1 - x0), (vb.bottom - vb.top - pad * 2) / (y1 - y0), maxK || 2);
    flyTo(k, (vb.left + vb.right) / 2 - (x0 + x1) / 2 * k, (vb.top + vb.bottom) / 2 - (y0 + y1) / 2 * k, animate);
  }
  function fitAll(animate) {
    const vb = viewportBox(), pad = 32;
    baseK = Math.min((vb.right - vb.left - pad * 2) / bw, (vb.bottom - vb.top - pad * 2) / bh, 2);
    placedFor = null;
    fitTo(bx, by, bx + bw, by + bh, animate);
  }
  let anim = null;
  function flyTo(k, x, y, animate) {
    if (anim) cancelAnimationFrame(anim);
    if (!animate || reduced()) { view.k = k; view.x = x; view.y = y; render(); return; }
    const from = { ...view }, t0 = performance.now(), dur = 520;
    const step = (now) => {
      const u = Math.min(1, (now - t0) / dur);
      const e = u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
      // zoom is interpolated in log space so it feels even
      view.k = Math.exp(Math.log(from.k) + (Math.log(k) - Math.log(from.k)) * e);
      view.x = from.x + (x - from.x) * e;
      view.y = from.y + (y - from.y) * e;
      render();
      if (u < 1) anim = requestAnimationFrame(step);
    };
    anim = requestAnimationFrame(step);
  }
  function zoomAt(factor, px, py) {
    const b = baseK || 0.2;
    const k = Math.max(b * 0.7, Math.min(Math.max(2.6, b * 20), view.k * factor));
    const f = k / view.k;
    view.x = px - (px - view.x) * f;
    view.y = py - (py - view.y) * f;
    view.k = k;
    render();
  }
  function centreOn(t, k) {
    const vb = viewportBox();
    flyTo(k, (vb.left + vb.right) / 2 - t.x * k, (vb.top + vb.bottom) / 2 - t.y * k, true);
  }

  // ---------- pointer: pan, pinch, wheel
  const pts = new Map();
  let moved = false, last = null, pinch0 = null;
  stage.addEventListener("pointerdown", (e) => {
    if (e.button !== 0 && e.pointerType === "mouse") return;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    moved = false;
    last = { x: e.clientX, y: e.clientY };
    if (pts.size === 2) {
      const [a, b] = [...pts.values()];
      pinch0 = { d: Math.hypot(a.x - b.x, a.y - b.y), k: view.k };
    }
  });
  stage.addEventListener("pointermove", (e) => {
    if (!pts.has(e.pointerId)) return;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pts.size === 2 && pinch0) {
      const [a, b] = [...pts.values()];
      const rect = stage.getBoundingClientRect();
      zoomAt((pinch0.k * Math.hypot(a.x - b.x, a.y - b.y) / pinch0.d) / view.k, (a.x + b.x) / 2 - rect.left, (a.y + b.y) / 2 - rect.top);
      moved = true;
      return;
    }
    const dx = e.clientX - last.x, dy = e.clientY - last.y;
    // The pointer is captured only once a press becomes a drag. Capturing on
    // the press would send the click to the stage and never to a town.
    if (!moved && Math.abs(dx) + Math.abs(dy) > 3) {
      moved = true;
      stage.classList.add("is-dragging");
      try { stage.setPointerCapture(e.pointerId); } catch (err) { /* the pointer may already be gone */ }
    }
    if (moved) { view.x += dx; view.y += dy; last = { x: e.clientX, y: e.clientY }; render(); }
  });
  const up = (e) => {
    pts.delete(e.pointerId);
    if (pts.size < 2) pinch0 = null;
    if (pts.size === 1) last = [...pts.values()][0];
    stage.classList.remove("is-dragging");
    setTimeout(() => { moved = false; }, 0);
  };
  stage.addEventListener("pointerup", up);
  stage.addEventListener("pointercancel", up);
  stage.addEventListener("wheel", (e) => {
    e.preventDefault();
    const rect = stage.getBoundingClientRect();
    zoomAt(Math.exp(-e.deltaY * 0.0016), e.clientX - rect.left, e.clientY - rect.top);
  }, { passive: false });
  stage.addEventListener("dblclick", (e) => {
    if (e.target.closest(".dl-tmap-town")) return;
    const rect = stage.getBoundingClientRect();
    zoomAt(1.8, e.clientX - rect.left, e.clientY - rect.top);
  });
  const zoomCentre = (f) => { const vb = viewportBox(); zoomAt(f, (vb.left + vb.right) / 2, (vb.top + vb.bottom) / 2); };
  root.querySelector("[data-zoom=in]").onclick = () => zoomCentre(1.5);
  root.querySelector("[data-zoom=out]").onclick = () => zoomCentre(1 / 1.5);
  root.querySelector("[data-zoom=fit]").onclick = () => fitAll(true);
  root.addEventListener("keydown", (e) => {
    if (e.target.matches("input, select")) return;
    if (e.key === "+" || e.key === "=") zoomCentre(1.3);
    else if (e.key === "-") zoomCentre(1 / 1.3);
    else if (e.key === "Escape") select(null);
  });
  let resizing = null;
  window.addEventListener("resize", () => {
    clearTimeout(resizing);
    resizing = setTimeout(() => { placedFor = null; render(); avoidDocks(); }, 60);
  });

  // The page's corner docks (the search and crumbs on the left, Notes, Python
  // and Settings on the right) and the feedback button stay put as the page
  // scrolls, so they pass over the frame. The map's own controls slide out
  // from under them, so that a button of the map is never one that cannot be pressed.
  function avoidDocks() {
    const f = root.getBoundingClientRect();
    const clear = (id, side) => {
      const el = document.getElementById(id);
      if (!el || !el.offsetParent && getComputedStyle(el).position !== "fixed") return 0;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height || r.right < f.left || r.left > f.right) return 0;
      // never so far that the control leaves the frame
      const room = Math.max(0, f.height - 220);
      if (side === "top") return r.bottom > f.top && r.top < f.bottom ? Math.min(room, Math.max(0, Math.min(r.bottom, f.bottom) - f.top + 8)) : 0;
      return r.top < f.bottom && r.bottom > f.top ? Math.min(room, Math.max(0, f.bottom - Math.max(r.top, f.top) + 8)) : 0;
    };
    const next = [clear("dl-dock-left", "top"), clear("dl-dock-right", "top"), clear("dl-report-toggle", "bottom")];
    root.style.setProperty("--map-clear-left", next[0] + "px");
    root.style.setProperty("--map-clear-right", next[1] + "px");
    root.style.setProperty("--map-clear-bottom", next[2] + "px");
    // A control that has moved may now be over a name, so once the page stops
    // scrolling the names are placed again.
    if (next.some((v, i) => Math.abs(v - cleared[i]) > 24)) {
      cleared = next;
      clearTimeout(settling);
      settling = setTimeout(() => { placedFor = null; render(); }, 150);
    }
  }
  let cleared = [0, 0, 0];
  let settling = null;
  let docking = 0;
  window.addEventListener("scroll", () => { if (!docking) docking = requestAnimationFrame(() => { docking = 0; avoidDocks(); }); }, { passive: true });

  // ---------- the graph
  function ancestors(code) {
    const out = new Set();
    const walk = (c) => { for (const n of byCode.get(c).needs) if (!out.has(n)) { out.add(n); walk(n); } };
    walk(code);
    return out;
  }
  const orderForTravel = (codes) => [...codes].sort((a, b) => byCode.get(a).tier - byCode.get(b).tier || byCode.get(a).name.localeCompare(byCode.get(b).name));
  function light(code) {
    for (const r of roads) {
      r.node.classList.toggle("is-lit-in", code != null && r.to === code);
      r.node.classList.toggle("is-lit-out", code != null && r.from === code);
    }
    // With a town open, the roads that are not its own fade into the land.
    root.classList.toggle("has-focus", code != null);
  }
  function drawRoute(codes) {
    routeLayer.replaceChildren();
    for (const n of townNodes) {
      n.b.classList.toggle("is-on-route", codes.includes(n.t.code));
      const old = n.b.querySelector(".dl-tmap-stop");
      if (old) old.remove();
    }
    if (!codes.length) return;
    const path = pathThrough(codes);
    svgEl("path", { d: path, class: "dl-tmap-route-casing", "vector-effect": "non-scaling-stroke" }, routeLayer);
    svgEl("path", { d: path, class: "dl-tmap-route", "vector-effect": "non-scaling-stroke" }, routeLayer);
    codes.forEach((c, i) => {
      if (i === codes.length - 1) return;
      const s = div("dl-tmap-stop", townNodes.find((x) => x.t.code === c).b, "span");
      s.textContent = i + 1;
    });
  }
  function drawCourse(id) {
    lineLayer.replaceChildren();
    courseLine = null;
    if (!id) return;
    const c = data.courses.find((x) => x.id === id);
    if (!c || !c.path.length) return;
    courseLine = c.path;
    const d = pathThrough(c.path);
    svgEl("path", { d, class: "dl-tmap-line-casing", "vector-effect": "non-scaling-stroke" }, lineLayer);
    svgEl("path", { d, class: "dl-tmap-line", "vector-effect": "non-scaling-stroke" }, lineLayer);
  }
  const paintVisited = () => { for (const n of townNodes) n.b.classList.toggle("is-visited", visited.has(n.t.code)); };

  // ---------- the panel
  const courseLabel = (s) => (s.courses.length ? s.courses.join(" · ") : "on no course yet");
  // consecutive sections of one page read as one street with several doors
  function streetGroups(t) {
    const out = [];
    for (const st of t.steps) {
      const prev = out[out.length - 1];
      if (prev && prev.slug === st.slug && prev.role === st.role) {
        if (st.section) prev.sections.push({ name: st.section, href: st.href });
        continue;
      }
      out.push({ ...st, sections: st.section ? [{ name: st.section, href: st.href }] : [] });
    }
    return out;
  }
  function fillStreets(t) {
    if (!t) { streets.classList.remove("is-on"); streets.replaceChildren(); return; }
    streets.innerHTML = streetGroups(t).map((g) => `<li class="${g.role === "teaches" ? "" : "is-side"}"><a href="${esc(g.href)}">${esc(g.title.split(":")[0])}</a>${g.sections.length > 1 ? `<small>${g.sections.length} parts</small>` : ""}${ROLE[g.role] ? `<small>${ROLE[g.role]}</small>` : ""}</li>`).join("");
    streets.classList.toggle("is-on", t.steps.length > 0);
  }
  const townButton = (code) => `<button type="button" data-go="${esc(code)}"${visited.has(code) ? ' class="is-done"' : ""}>${esc(byCode.get(code).name)}</button>`;
  function select(code, fly, focus) {
    selected = code;
    for (const n of townNodes) n.b.classList.toggle("is-selected", n.t.code === code);
    light(code);
    fillStreets(code ? byCode.get(code) : null);
    if (!code) {
      route = []; drawRoute([]); showHome(); render();
      try { history.replaceState(null, "", location.pathname + location.search); } catch (e) { /* the address stays */ }
      return;
    }
    const t = byCode.get(code);
    if (route.length && !route.includes(code)) { route = []; drawRoute([]); }
    showTown(t);
    try { history.replaceState(null, "", "#town=" + code); } catch (e) { /* the address stays */ }
    if (fly) centreOn(t, Math.max(view.k, (baseK || 0.2) * 4.6)); else render();
    if (focus) pbody.querySelector("h2").focus({ preventScroll: true });
  }
  function showTown(t) {
    const r = regionById.get(t.region);
    const dname = districtById.get(t.district).name;
    const kids = children.get(t.code);
    let n = 0;
    const groups = streetGroups(t);
    const stepsHtml = groups.length
      ? `<ol class="dl-tmap-street-list">${groups.map((g) => {
          const main = g.role === "teaches";
          if (main) n += 1;
          const parts = g.sections.length ? `<em>${g.sections.map((x) => esc(x.name)).join(" · ")}</em>` : "";
          return `<li class="${main ? "" : "is-side"}"><a href="${esc(g.href)}"><span class="dl-tmap-n">${main ? n : "·"}</span><span><b>${esc(g.title)}</b>${parts}<small>${ROLE[g.role] ? esc(ROLE[g.role]) + " · " : ""}${esc(courseLabel(g))}</small></span></a></li>`;
        }).join("")}</ol>`
      : `<p class="dl-tmap-note">No page teaches this yet. It is a town still being built.</p>`;
    const teachingPages = groups.filter((g) => g.role === "teaches").length;
    const lms = landmarksAt.get(t.code);
    const beenHere = visited.has(t.code);
    pbody.innerHTML = `
      <button type="button" class="dl-tmap-close" data-close aria-label="Close">×</button>
      <div class="dl-tmap-eyebrow"><span class="dl-tmap-swatch" style="background:${landColour(r, 0)}"></span>${t.plains ? plainsName + " · " : ""}${esc(r.full)} · ${esc(dname)}${t.plains ? "" : " · " + stopsWords(t.tier)}</div>
      <h2 tabindex="-1">${esc(t.name)}</h2>
      <p>${esc(t.plain)}</p>
      ${r.lore ? `<p class="dl-tmap-lore"><em>${esc(r.fancy || r.name)}. ${esc(r.lore)}</em></p>` : ""}
      <div class="dl-tmap-actions">
        <button type="button" class="dl-tmap-primary" data-directions>How do I get here?</button>
        <button type="button" class="dl-tmap-secondary" data-been aria-pressed="${beenHere}">${beenHere ? "✓ I have been here" : "I have been here"}</button>
      </div>
      <div data-dir></div>
      <h3>The streets · ${teachingPages} page${teachingPages === 1 ? "" : "s"}</h3>
      ${stepsHtml}
      <h3>Needs first</h3>
      ${t.needs.length ? `<div class="dl-tmap-links">${t.needs.map(townButton).join("")}</div>` : "<p>Nothing. You could start here today.</p>"}
      ${kids.length ? `<h3>Leads to</h3><div class="dl-tmap-links">${kids.map(townButton).join("")}</div>` : ""}
      ${lms.length ? `<h3>Landmarks that use it</h3><div class="dl-tmap-links">${lms.map((lm) => `<button type="button" data-lm="${esc(lm.slug)}">◆ ${esc(lm.title)}</button>`).join("")}</div>` : ""}
    `;
    if (route.length && route[route.length - 1] === t.code) showDirections(t);
    openPanel();
  }
  function showDirections(t) {
    const todo = orderForTravel([...ancestors(t.code)].filter((c) => !visited.has(c)));
    route = [...todo, t.code];
    drawRoute(route);
    const box = pbody.querySelector("[data-dir]");
    const doneCount = [...ancestors(t.code)].filter((c) => visited.has(c)).length;
    if (!todo.length) {
      box.innerHTML = `<p class="dl-tmap-note">${t.needs.length ? "You have been to every town this needs. You can start here." : "Nothing comes first. You can start here."}</p>`;
    } else {
      box.innerHTML = `
        <h3>The road here · ${todo.length} stop${todo.length === 1 ? "" : "s"} first</h3>
        ${doneCount ? `<p class="dl-tmap-note">You have been to ${doneCount} of the towns on the way, so they are not on this list.</p>` : ""}
        <ol class="dl-tmap-steps">${todo.map((c) => {
          const s = byCode.get(c);
          const first = s.steps.find((x) => x.role === "teaches");
          return `<li><div><button type="button" data-go="${esc(c)}">${esc(s.name)}</button><small>${first ? esc(first.title) : "no page yet"}</small></div></li>`;
        }).join("")}</ol>`;
    }
    const xs = route.map((c) => byCode.get(c).x), ys = route.map((c) => byCode.get(c).y);
    fitTo(Math.min(...xs) - 80, Math.min(...ys) - 80, Math.max(...xs) + 80, Math.max(...ys) + 80, true, (baseK || 0.2) * 6);
  }
  function countryItems(ids) {
    return ids.map((id) => {
      const r = regionById.get(id);
      const ds = data.districts.filter((d) => d.region === r.id);
      const inR = towns.filter((t) => t.region === r.id);
      const been = inR.filter((t) => visited.has(t.code)).length;
      return `<li><details><summary class="dl-tmap-country"><span class="dl-tmap-swatch" style="background:${landColour(r, 0)}"></span><span class="dl-tmap-cname">${esc(r.full)}${r.lore ? `<em>${esc(r.lore)}</em>` : ""}</span><small>${been ? been + " of " : ""}${inR.length}</small></summary><p class="dl-tmap-lore">${esc(r.blurb || "")}</p>${ds.map((d) => {
        const list = towns.filter((t) => t.district === d.id).sort((a, b) => a.tier - b.tier || a.name.localeCompare(b.name));
        return `<details><summary>${esc(d.name)}<small>${list.length}</small></summary><div class="dl-tmap-links">${list.map((t) => townButton(t.code)).join("")}</div></details>`;
      }).join("")}</details></li>`;
    }).join("");
  }
  function plainsItem() {
    const here = towns.filter((t) => t.plains).sort((a, b) => a.name.localeCompare(b.name));
    return `<li><details><summary class="dl-tmap-country"><span class="dl-tmap-swatch" style="background:var(--map-plains)"></span><span class="dl-tmap-cname">${esc(plainsName)}<em>${esc((tower.plains || {}).plain || "")}</em></span><small>${here.length}</small></summary><div class="dl-tmap-links">${here.map((t) => townButton(t.code)).join("")}</div></details></li>`;
  }
  function showHome() {
    pbody.innerHTML = `
      <div class="dl-tmap-eyebrow">A map of dewlab</div>
      <h2 tabindex="-1">Comath, the land of maths and computing</h2>
      <p>Every topic on dewlab is a town. Towns that belong together are in the same country, and countries that share many roads are on the same continent.</p>
      <p>Every traveller starts at the Tower of Unknowing, on the Island of First Steps. The Prerequisite Plains round it have the towns that need nothing first. No road is closed. You can go to any town, and the map will show you the way.</p>
      <p class="dl-tmap-lore"><em>${esc(tower.lore || "")}</em></p>
      <p>Zoom in to see countries, then districts, then every town.</p>
      <h3>How to read the map</h3>
      <div class="dl-tmap-key">
        <i style="width:16px;height:19px;color:var(--dl-link)">${TOWER_SVG}</i><span>The Tower of Unknowing, where every traveller starts.</span>
        <i style="width:14px;height:14px;border-radius:50%;background:var(--map-town)"></i><span>A town is one topic. A bigger town has more topics built on it.</span>
        <i style="width:12px;height:12px;border-radius:50%;border:2px dashed var(--map-town)"></i><span>A town still being built. No page teaches it yet.</span>
        <i style="width:9px;height:9px;transform:rotate(45deg);border:2px solid var(--dl-link)"></i><span>A landmark: a project, or a place to begin. It uses the towns near it.</span>
        <i style="width:12px;height:12px;border-radius:50%;background:var(--map-visited)"></i><span>A town you have been to.</span>
        <i style="width:20px;border-top:2px dashed var(--dl-link)"></i><span>A road into another country.</span>
        <i style="width:22px;height:4px;background:var(--dl-bg);border:2px solid var(--map-coast);border-left:0;border-right:0"></i><span>A bridge. A road between two continents crosses the sea on a bridge. A wider bridge carries more roads.</span>
        <i style="width:18px;height:12px;background:var(--map-plains);border:1px solid var(--dl-cell-border)"></i><span>The Prerequisite Plains. Their towns need nothing first.</span>
        <i style="width:20px;border-top:1.5px dashed var(--map-border)"></i><span>A border between two countries.</span>
        <i style="width:20px;border-top:1px dotted var(--map-county)"></i><span>A border between two counties. A county is a district inside a country.</span>
      </div>
      <h3>The continents and their countries</h3>
      ${continents.map((c) => `
        <div class="dl-tmap-cont-head"><span class="dl-tmap-swatch" style="background:${contColour(c)}"></span><span><button type="button" data-cont="${esc(c.id)}">${esc(c.kind === "islands" ? c.fancy || c.name : c.full)}</button>${c.lore && c.kind !== "islands" ? `<em>${esc(c.lore)}</em>` : ""}</span></div>
        <ul class="dl-tmap-regions">${c.kind === "start" ? plainsItem() : ""}${countryItems(c.regions)}</ul>`).join("")}
    `;
  }
  function showContinent(c) {
    select(null);
    const here = towns.filter((t) => t.land === c.id);
    const out = data.bridges.filter((b) => b.a === c.id || b.b === c.id);
    const kind = c.kind === "islands" ? "Islands" : c.kind === "start" ? "Where every traveller starts" : "Continent";
    pbody.innerHTML = `
      <button type="button" class="dl-tmap-close" data-close aria-label="Close">×</button>
      <div class="dl-tmap-eyebrow"><span class="dl-tmap-swatch" style="background:${contColour(c)}"></span>${kind} · ${here.length} towns</div>
      <h2 tabindex="-1">${esc(c.full)}</h2>
      <p>${esc(c.blurb || "")}</p>
      ${c.lore ? `<p class="dl-tmap-lore"><em>${esc(c.lore)}</em></p>` : ""}
      <h3>${c.kind === "start" ? "On the island" : "Countries"}</h3>
      <ul class="dl-tmap-regions">${c.kind === "start" ? plainsItem() : ""}${countryItems(c.regions)}</ul>
      ${out.length ? `<h3>Bridges to</h3><ul>${out.map((b) => { const o = contById.get(b.a === c.id ? b.b : b.a); return `<li>${esc(o.fancy || o.name)} · ${b.count} road${b.count === 1 ? "" : "s"}</li>`; }).join("")}</ul>` : ""}
    `;
    const xs = here.map((t) => t.x), ys = here.map((t) => t.y);
    if (c.kind === "start") { xs.push(0); ys.push(0); }
    fitTo(Math.min(...xs) - 150, Math.min(...ys) - 150, Math.max(...xs) + 150, Math.max(...ys) + 150, true);
    openPanel();
  }
  function showTower() {
    select(null);
    const first = towns.filter((t) => t.plains);
    const pages = data.landmarks.filter((lm) => lm.tower);
    pbody.innerHTML = `
      <button type="button" class="dl-tmap-close" data-close aria-label="Close">×</button>
      <div class="dl-tmap-eyebrow">Landmark · where every traveller starts</div>
      <h2 tabindex="-1">${esc(tower.name || "The Tower of Unknowing")}</h2>
      <p>${esc(tower.plain || "")}</p>
      <p class="dl-tmap-lore"><em>${esc(tower.lore || "")}</em></p>
      ${pages.length ? `<h3>Pages kept in the tower</h3><ul class="dl-tmap-ways">${pages.map((lm) => `<li><a href="${esc(lm.href)}"><b>${esc(lm.title)}</b></a></li>`).join("")}</ul>` : ""}
      <h3>${esc(plainsName)} · ${first.length} towns</h3>
      <p>${esc((tower.plains || {}).plain || "")}</p>
      ${data.regions.map((r) => {
        const here = first.filter((t) => t.region === r.id);
        return here.length ? `<p class="dl-tmap-lore dl-tmap-sub">${esc(r.full)}</p><div class="dl-tmap-links">${here.map((t) => townButton(t.code)).join("")}</div>` : "";
      }).join("")}
    `;
    openPanel();
  }
  function showLandmark(lm) {
    select(null);
    pbody.innerHTML = `
      <button type="button" class="dl-tmap-close" data-close aria-label="Close">×</button>
      <div class="dl-tmap-eyebrow">Landmark · ${esc(lm.kind)}</div>
      <h2 tabindex="-1">${esc(lm.title)}</h2>
      <ul class="dl-tmap-ways"><li><a href="${esc(lm.href)}"><b>Open the page</b></a></li></ul>
      ${lm.at.length ? `<h3>It draws on</h3><div class="dl-tmap-links">${lm.at.map(townButton).join("")}</div>` : ""}
    `;
    openPanel();
  }
  const openPanel = () => panel.classList.remove("is-collapsed");
  pbody.addEventListener("click", (e) => {
    const go = e.target.closest("[data-go]");
    if (go) { select(go.dataset.go, true, true); return; }
    const cont = e.target.closest("[data-cont]");
    if (cont) { showContinent(contById.get(cont.dataset.cont)); return; }
    const lmb = e.target.closest("[data-lm]");
    if (lmb) { const lm = data.landmarks.find((x) => x.slug === lmb.dataset.lm); if (lm) showLandmark(lm); return; }
    if (e.target.closest("[data-close]")) { select(null); return; }
    if (e.target.closest("[data-directions]")) { showDirections(byCode.get(selected)); render(); return; }
    if (e.target.closest("[data-been]")) {
      if (visited.has(selected)) visited.delete(selected); else visited.add(selected);
      saveVisited(); paintVisited();
      const keep = route.length && route[route.length - 1] === selected;
      showTown(byCode.get(selected));
      if (keep) showDirections(byCode.get(selected));
      render();
    }
  });
  panel.querySelector(".dl-tmap-grab").onclick = () => { panel.classList.toggle("is-collapsed"); placedFor = null; render(); };
  const toggle = root.querySelector(".dl-tmap-layers-toggle");
  toggle.onclick = () => { const c = root.querySelector(".dl-tmap-controls"); c.classList.toggle("is-open"); toggle.setAttribute("aria-expanded", c.classList.contains("is-open")); };

  // ---------- layers
  root.querySelector("[data-roads]").onchange = (e) => root.classList.toggle("no-roads", !e.target.checked);
  for (const c of data.courses) {
    const o = document.createElement("option");
    o.value = c.id;
    o.textContent = c.path.length ? `${c.title} (${c.path.length} towns)` : c.title;
    courseSel.appendChild(o);
  }
  courseSel.onchange = () => {
    drawCourse(courseSel.value);
    const c = data.courses.find((x) => x.id === courseSel.value);
    if (c && !c.path.length) {
      select(null);
      pbody.insertAdjacentHTML("afterbegin", `<p class="dl-tmap-note">The road for <b>${esc(c.title)}</b> is not on the map yet.</p>`);
    } else if (c) {
      const xs = c.path.map((x) => byCode.get(x).x), ys = c.path.map((x) => byCode.get(x).y);
      fitTo(Math.min(...xs) - 60, Math.min(...ys) - 60, Math.max(...xs) + 60, Math.max(...ys) + 60, true, (baseK || 0.2) * 5);
    }
    render();
  };

  // ---------- search
  search.addEventListener("input", () => {
    const s = search.value.trim().toLowerCase();
    if (!s) { results.replaceChildren(); return; }
    const words = s.split(/\s+/);
    const hits = towns.map((t) => {
      const name = t.name.toLowerCase();
      const hay = [t.name, t.plain, districtById.get(t.district).name, ...t.steps.map((x) => x.title + " " + (x.section || ""))].join(" ").toLowerCase();
      if (!words.every((w) => hay.includes(w))) return null;
      return { t, score: (name.startsWith(s) ? 3 : 0) + (name.includes(s) ? 2 : 0) + t.weight / 100 };
    }).filter(Boolean).sort((a, b) => b.score - a.score).slice(0, 8);
    results.innerHTML = hits.length
      ? hits.map(({ t }) => `<li><button type="button" data-go="${esc(t.code)}">${esc(t.name)}<small>${esc(districtById.get(t.district).name)}</small></button></li>`).join("")
      : '<li class="dl-tmap-none">Nothing called that yet.</li>';
  });
  search.addEventListener("keydown", (e) => { if (e.key === "Enter") { const b = results.querySelector("button"); if (b) b.click(); } });
  results.addEventListener("click", (e) => {
    const b = e.target.closest("[data-go]");
    if (b) { select(b.dataset.go, true, true); results.replaceChildren(); search.value = ""; }
  });

  // ---------- open
  paintVisited();
  showHome();
  // On a phone the map comes first: the panel starts as a bar that opens with a tap.
  if (root.clientWidth <= PHONE) panel.classList.add("is-collapsed");
  fitAll(false);
  avoidDocks();
  requestAnimationFrame(() => { for (const n of townNodes) n.w = n.b.querySelector(".dl-tmap-name").offsetWidth; placedFor = null; render(); });
  const m = /^#town=(.+)$/.exec(decodeURIComponent(location.hash));
  if (m && byCode.has(m[1])) select(m[1], true);
}

// The map's type sizes come from map.css, and names are placed by their size,
// so nothing is measured until the stylesheet has loaded.
function whenStyled(fn) {
  const link = document.querySelector('link[rel="stylesheet"][href*="map.css"]');
  if (!link || link.sheet) { fn(); return; }
  link.addEventListener("load", fn, { once: true });
  link.addEventListener("error", fn, { once: true });
}

const dataEl = document.getElementById("dewlab-map");
const rootEl = document.getElementById("dl-tmap");
if (dataEl && rootEl) {
  let data = null;
  try { data = JSON.parse(dataEl.textContent); } catch (err) { /* the list under the map still works */ }
  if (data) whenStyled(() => start(rootEl, data));
}
