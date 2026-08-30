/* The topic tree: every topic in planning/curriculum/topics.yaml, what
 * needs what, and what each one is for.
 *
 * Nodes and edges are positioned by build.py and arrive as data in the page —
 * there is no layout to do here and nothing to fetch. What this file adds is
 * the three things a static picture cannot do: move around it, look closer, and
 * open a topic to read about it.
 *
 * Deliberately dependency-free. A pan-and-zoom library would be larger than the
 * whole of this and would still need the same forty lines of pointer handling.
 */

/* Low enough that the whole vertical tree fits a phone. The old floor of 0.35
 * was set against a tree 756px tall; this one is 1768, and a floor that stops
 * "fit" from fitting is worse than small text you can zoom into. */
const MIN_SCALE = 0.2;
const MAX_SCALE = 2.4;

function readData() {
  const el = document.getElementById("dewlab-tree");
  if (!el) return null;
  try {
    return JSON.parse(el.textContent);
  } catch (err) {
    return null;
  }
}

/* --------------------------------------------------------------- drawing */

function edgePath(from, to, node) {
  /* Out of the bottom of the earlier topic and into the top of the later one.
   * Prerequisites always run downwards, so an edge never has to double back and
   * every curve can use the same shape. */
  const x1 = from.x + node.w / 2;
  const y1 = from.y + node.h;
  const x2 = to.x + node.w / 2;
  const y2 = to.y;
  const reach = Math.max(30, (y2 - y1) / 2);
  return `M${x1} ${y1} C${x1} ${y1 + reach}, ${x2} ${y2 - reach}, ${x2} ${y2}`;
}

function draw(data, canvas) {
  const byCode = new Map(data.nodes.map((n) => [n.code, n]));
  const svgNS = "http://www.w3.org/2000/svg";

  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("class", "dl-tree-edges");
  svg.setAttribute("width", data.width);
  svg.setAttribute("height", data.height);
  svg.setAttribute("viewBox", `0 0 ${data.width} ${data.height}`);

  for (const band of data.bands) {
    const rect = document.createElementNS(svgNS, "rect");
    rect.setAttribute("class", "dl-tree-band");
    rect.setAttribute("x", 0);
    rect.setAttribute("y", band.y - 12);
    rect.setAttribute("width", data.width);
    rect.setAttribute("height", band.height + 24);
    svg.appendChild(rect);

    const label = document.createElementNS(svgNS, "text");
    label.setAttribute("class", "dl-tree-band-label");
    label.setAttribute("x", 10);
    label.setAttribute("y", band.y - 18);
    label.textContent = band.label;
    svg.appendChild(label);
  }

  for (const node of data.nodes) {
    for (const need of node.needs) {
      const from = byCode.get(need);
      if (!from) continue;
      const path = document.createElementNS(svgNS, "path");
      path.setAttribute("class", "dl-tree-edge");
      path.setAttribute("d", edgePath(from, node, data.node));
      path.dataset.from = need;
      path.dataset.to = node.code;
      svg.appendChild(path);
    }
  }
  canvas.appendChild(svg);

  for (const node of data.nodes) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "dl-tree-node";
    button.dataset.code = node.code;
    button.dataset.state = node.state;
    /* Subject is no longer an axis, so it has to live on the node itself — a
     * coloured edge is enough to follow one thread down the tree. */
    button.dataset.strand = node.strand;
    button.style.left = `${node.x}px`;
    button.style.top = `${node.y}px`;
    button.style.width = `${data.node.w}px`;
    button.style.height = `${data.node.h}px`;
    button.setAttribute("aria-describedby", "dl-tree-detail");
    button.innerHTML = `<span>${node.name}</span>`;
    canvas.appendChild(button);
  }
  return byCode;
}

/* ------------------------------------------------------- pan and zoom */

function controlView(frame, canvas, data) {
  const view = { x: 0, y: 0, scale: 1 };

  function apply() {
    canvas.style.transform =
      `translate(${view.x}px, ${view.y}px) scale(${view.scale})`;
  }

  function clamp() {
    view.scale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, view.scale));
    /* Always leave part of the tree on screen. Panning it entirely out of view
     * looks exactly like the page having gone blank. */
    const w = data.width * view.scale;
    const h = data.height * view.scale;
    const box = frame.getBoundingClientRect();
    const slack = 120;
    view.x = Math.min(box.width - slack, Math.max(slack - w, view.x));
    view.y = Math.min(box.height - slack, Math.max(slack - h, view.y));
  }

  function zoomAt(factor, clientX, clientY) {
    const box = frame.getBoundingClientRect();
    const px = clientX - box.left;
    const py = clientY - box.top;
    const before = view.scale;
    view.scale *= factor;
    clamp();
    /* Keep whatever was under the pointer under the pointer. */
    const ratio = view.scale / before;
    view.x = px - (px - view.x) * ratio;
    view.y = py - (py - view.y) * ratio;
    clamp();
    apply();
  }

  function fit() {
    /* Fit the width and go to the top, rather than squeezing the whole tree
     * into the frame. The tree is deliberately taller than it is wide, so
     * fitting its height would shrink every label past reading. Starting at
     * the top also starts where the tree does: nothing up there needs
     * anything. */
    const box = frame.getBoundingClientRect();
    view.scale = Math.min(1, (box.width - 32) / data.width);
    view.scale = Math.max(MIN_SCALE, view.scale);
    view.x = 16;
    view.y = 16;
    clamp();
    apply();
  }

  /* Drag to pan, with a pointer capture so a fast drag that leaves the frame
   * does not strand the tree half-moved. */
  let dragging = null;
  frame.addEventListener("pointerdown", (ev) => {
    if (ev.target.closest(".dl-tree-node")) return;
    dragging = { id: ev.pointerId, x: ev.clientX - view.x, y: ev.clientY - view.y };
    frame.setPointerCapture(ev.pointerId);
    frame.classList.add("dl-tree-dragging");
  });
  frame.addEventListener("pointermove", (ev) => {
    if (!dragging || ev.pointerId !== dragging.id) return;
    view.x = ev.clientX - dragging.x;
    view.y = ev.clientY - dragging.y;
    clamp();
    apply();
  });
  for (const end of ["pointerup", "pointercancel"]) {
    frame.addEventListener(end, (ev) => {
      if (!dragging || ev.pointerId !== dragging.id) return;
      dragging = null;
      frame.classList.remove("dl-tree-dragging");
    });
  }

  frame.addEventListener(
    "wheel",
    (ev) => {
      ev.preventDefault();
      zoomAt(ev.deltaY < 0 ? 1.12 : 1 / 1.12, ev.clientX, ev.clientY);
    },
    { passive: false }
  );

  return { fit, zoomAt, view, apply, clamp };
}

/* ------------------------------------------------------------- the panel */

function opensUp(node, byCode) {
  /* What this topic unlocks. The map's whole reason for existing is a student
   * asking "where can I go next?", and that question is answered by the edges
   * pointing away from a topic rather than towards it — which nothing in the
   * panel said until now. */
  const out = [];
  for (const other of byCode.values()) {
    if (other.needs.includes(node.code)) out.push(other);
  }
  return out.sort((a, b) => a.name.localeCompare(b.name));
}

function showDetail(node, byCode, panel) {
  if (!node) {
    panel.innerHTML =
      '<p class="dl-tree-hint">Choose a topic to see what it is, ' +
      "where it turns up in computing, and what it needs first.</p>";
    return;
  }

  const needs = node.needs
    .map((code) => byCode.get(code))
    .filter(Boolean)
    .map(
      (n) =>
        `<li><button type="button" class="dl-tree-jump" data-code="${n.code}">` +
        `${n.name}</button></li>`
    )
    .join("");

  const uses = node.uses.map((u) => `<li>${u}</li>`).join("");

  const opens = opensUp(node, byCode)
    .map(
      (n) =>
        `<li><button type="button" class="dl-tree-jump" data-code="${n.code}">` +
        `${n.name}</button></li>`
    )
    .join("");

  const state = {
    taught: node.where
      ? `<a class="dl-tree-goto" href="${node.where.href}">Read it in ` +
        `${node.where.title}</a>`
      : "",
    planned:
      '<p class="dl-tree-state">Not written yet. It is on the plan — see ' +
      "<code>planning/outlines/</code>.</p>",
    excluded:
      '<p class="dl-tree-state">Deliberately not covered on this course. ' +
      "It is here so you know it exists.</p>",
    groundwork:
      '<p class="dl-tree-state">Groundwork. No module descriptor names this ' +
      "on its own, but the topics below it do not make sense without it, so " +
      "it turns up wherever it is first needed.</p>",
  }[node.state];

  panel.innerHTML =
    `<h2>${node.name}</h2>` +
    `<p class="dl-tree-code"><span class="dl-tree-hue" data-strand="${node.strand}">` +
    `</span>${node.strand} · ${node.code}</p>` +
    `<p class="dl-tree-plain">${node.plain}</p>` +
    (uses ? `<h3>Where it turns up</h3><ul class="dl-tree-uses">${uses}</ul>` : "") +
    (needs ? `<h3>Needs first</h3><ul class="dl-tree-needs">${needs}</ul>` : "") +
    (opens ? `<h3>Opens up</h3><ul class="dl-tree-opens">${opens}</ul>` : "") +
    (state || "");
}

/* ------------------------------------------------------------------ start */

function start() {
  const data = readData();
  const frame = document.getElementById("dl-tree");
  const canvas = document.getElementById("dl-tree-canvas");
  const panel = document.getElementById("dl-tree-detail");
  if (!data || !frame || !canvas || !panel) return;

  const byCode = draw(data, canvas);
  const control = controlView(frame, canvas, data);
  control.fit();
  showDetail(null, byCode, panel);

  let chosen = null;

  function choose(code) {
    chosen = code;
    for (const el of canvas.querySelectorAll(".dl-tree-node")) {
      el.classList.toggle("is-chosen", el.dataset.code === code);
      el.classList.remove("is-related");
    }
    for (const edge of canvas.querySelectorAll(".dl-tree-edge")) {
      edge.classList.remove("is-lit");
    }
    const node = byCode.get(code);
    if (node) {
      /* Light the path in and the paths out, so a topic's place in the tree is
       * visible without reading the whole diagram. */
      for (const edge of canvas.querySelectorAll(".dl-tree-edge")) {
        if (edge.dataset.to === code || edge.dataset.from === code) {
          edge.classList.add("is-lit");
          const other = edge.dataset.to === code ? edge.dataset.from : edge.dataset.to;
          const el = canvas.querySelector(`.dl-tree-node[data-code="${other}"]`);
          if (el) el.classList.add("is-related");
        }
      }
    }
    showDetail(node, byCode, panel);
  }

  canvas.addEventListener("click", (ev) => {
    const button = ev.target.closest(".dl-tree-node");
    if (button) choose(button.dataset.code);
  });

  panel.addEventListener("click", (ev) => {
    const jump = ev.target.closest(".dl-tree-jump");
    if (!jump) return;
    choose(jump.dataset.code);
    const el = canvas.querySelector(`.dl-tree-node[data-code="${jump.dataset.code}"]`);
    if (el) el.focus();
  });

  document.getElementById("dl-tree-in").addEventListener("click", () => {
    const box = frame.getBoundingClientRect();
    control.zoomAt(1.25, box.left + box.width / 2, box.top + box.height / 2);
  });
  document.getElementById("dl-tree-out").addEventListener("click", () => {
    const box = frame.getBoundingClientRect();
    control.zoomAt(1 / 1.25, box.left + box.width / 2, box.top + box.height / 2);
  });
  document.getElementById("dl-tree-fit").addEventListener("click", control.fit);

  window.addEventListener("resize", () => {
    control.clamp();
    control.apply();
  });

  /* For the browser tests, and for anybody poking at it from the console. */
  globalThis.dewlabTree = { data, choose, view: control.view, chosen: () => chosen };
}

start();
